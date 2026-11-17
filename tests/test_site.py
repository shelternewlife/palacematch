import json
import pathlib
import subprocess
import sys
import unittest
from html.parser import HTMLParser

ROOT = pathlib.Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
APP = json.loads((ROOT / "content/app.json").read_text(encoding="utf-8"))
BASE = APP["website_url"].rstrip("/")
from scripts.build_resources import routes as resource_routes, DATA, GUIDES
FAQ = json.loads((ROOT / "content/faq.json").read_text(encoding="utf-8"))
FEATURES = json.loads((ROOT / "content/features.json").read_text(encoding="utf-8"))
STRATEGY = json.loads((ROOT / "content/market-strategy.json").read_text(encoding="utf-8"))

class PageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.tracked_ctas = []
        self.images = []
        self.all_images = []
        self.h1 = []
        self.in_h1 = False
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "a" and attrs.get("href"):
            self.links.append(attrs["href"])
            if attrs.get("data-analytics-event") == "google_play_click":
                self.tracked_ctas.append(attrs)
        if tag == "img":
            self.all_images.append(attrs)
            image_src = attrs.get("src", "")
            if image_src.startswith("https://play-lh.googleusercontent.com/") or "/assets/screens/" in image_src:
                self.images.append(attrs)
        if tag == "h1":
            self.in_h1 = True
    def handle_endtag(self, tag):
        if tag == "h1":
            self.in_h1 = False
    def handle_data(self, data):
        if self.in_h1:
            self.h1.append(data)

def output_path(lang, section="home"):
    return DIST / lang / ("" if section == "home" else section) / "index.html"

class SiteTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        subprocess.run([sys.executable, str(ROOT / "scripts/build.py")], check=True)
        subprocess.run([sys.executable, str(ROOT / "scripts/validate.py")], check=True)

    def test_google_site_verification_tag(self):
        source = (DIST / "index.html").read_text(encoding="utf-8")
        self.assertIn('name="google-site-verification"', source)
        self.assertIn("8mOiNMu4Tn477yFaR-IWrNQGhdqH1TpF6NKKoN94Oms", source)

    def test_identity_and_store_url(self):
        self.assertEqual(APP["name"], "Palace Match")
        self.assertIn(APP["package_id"], APP["google_play_url"])

    def test_all_expected_routes_exist(self):
        self.assertTrue((DIST / "index.html").is_file())
        for lang in ("en", "ar"):
            for section in ("home", "about", "features", "download", "faq"):
                self.assertTrue(output_path(lang, section).is_file(), f"{lang}/{section}")

    def test_page_content_is_section_specific(self):
        expected = {
            "en": {"about": "About Palace Match", "features": "Explore the features", "faq": "Frequently asked questions"},
            "ar": {"about": "عن Palace Match", "features": "استكشف المزايا", "faq": "الأسئلة الشائعة"},
        }
        for lang in ("en", "ar"):
            headings = []
            for section in ("about", "features", "faq"):
                parser = PageParser()
                parser.feed(output_path(lang, section).read_text(encoding="utf-8"))
                heading = "".join(parser.h1).strip()
                self.assertIn(expected[lang][section], heading)
                headings.append(heading)
            self.assertEqual(len(set(headings)), 3, f"Duplicate page headings for {lang}")

    def test_navigation_uses_project_root_urls(self):
        for lang in ("en", "ar"):
            for section in ("home", "about", "features", "download", "faq"):
                parser = PageParser()
                parser.feed(output_path(lang, section).read_text(encoding="utf-8"))
                self.assertIn(f"{BASE}/{lang}/about/", parser.links)
                self.assertIn(f"{BASE}/{lang}/features/", parser.links)
                self.assertIn(f"{BASE}/{lang}/faq/", parser.links)
                self.assertIn(f"{BASE}/", parser.links)

    def test_language_switch_preserves_page(self):
        for lang in ("en", "ar"):
            for section in ("home", "about", "features", "download", "faq"):
                parser = PageParser()
                parser.feed(output_path(lang, section).read_text(encoding="utf-8"))
                suffix = "" if section == "home" else f"{section}/"
                for locale in STRATEGY["published_locales"]:
                    expected = f"{BASE}/{locale.lower()}/" + suffix
                    self.assertIn(expected, parser.links)

    def test_primary_and_resource_navigation_are_grouped_in_dropdowns(self):
        import re
        for lang in ("en", "ar"):
            for page in ("", "about", "features", "download", "faq", "blog"):
                path = DIST / lang / page / "index.html" if page else DIST / lang / "index.html"
                source = path.read_text(encoding="utf-8")
                groups = re.findall(r'<details class="nav-menu" data-nav-group="([^"]+)">(.*?)</details>', source, re.DOTALL)
                self.assertEqual([name for name, _ in groups], ["primary", "resources"], f"{lang}/{page}")
                for name, markup in groups:
                    self.assertEqual(len(re.findall(r'<a data-nav-item="[^"]+"', markup)), 4, f"{lang}/{page}/{name}")
                    self.assertIn("<summary>", markup)
                self.assertIn(".nav-dropdown", (DIST / "assets/style.css").read_text(encoding="utf-8"))

    def test_sitemap_contains_root_and_all_language_routes(self):
        import xml.etree.ElementTree as ET
        root = ET.parse(DIST / "sitemap.xml").getroot()
        ns = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
        urls = [node.find(f"{ns}loc").text for node in root.findall(f"{ns}url")]
        self.assertEqual(len(urls), len(resource_routes()) + (len(STRATEGY["published_locales"]) * 14))
        self.assertEqual(len(urls), len(set(urls)))
        self.assertNotIn(f"{BASE}/", urls)
        for lang in ("en", "ar"):
            for section in ("home", "about", "features", "download", "faq"):
                expected = f"{BASE}/{lang}/" + ("" if section == "home" else f"{section}/")
                self.assertIn(expected, urls)

    def test_root_redirects_to_us_english_about_and_preserves_verification(self):
        source = (DIST / "index.html").read_text(encoding="utf-8")
        target = f"{BASE}/en-us/about/"
        self.assertIn(f'<link rel="canonical" href="{target}">', source)
        self.assertIn(f'<meta http-equiv="refresh" content="0; url={target}">', source)
        self.assertIn(f'window.location.replace("{target}")', source)
        self.assertIn('name="google-site-verification"', source)
        self.assertIn('name="robots" content="noindex,follow"', source)
        self.assertNotIn("Choose your language", source)
        self.assertNotIn("اختر لغتك", source)

    def test_sitemap_contains_reciprocal_language_alternates(self):
        import xml.etree.ElementTree as ET
        root = ET.parse(DIST / "sitemap.xml").getroot()
        ns = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
        xhtml = "{http://www.w3.org/1999/xhtml}"
        entries = root.findall(f"{ns}url")
        self.assertEqual(len(entries), len(resource_routes()) + (len(STRATEGY["published_locales"]) * 14))
        for entry in entries:
            loc = entry.find(f"{ns}loc").text
            alternates = {
                node.get("hreflang"): node.get("href")
                for node in entry.findall(f"{xhtml}link")
            }
            route = loc[len(BASE) + 1:].strip("/")
            parts = route.split("/")
            if parts[0] in {code.lower() for code in STRATEGY["published_locales"]}:
                tail = "/".join(parts[1:])
                suffix = f"{tail}/" if tail else ""
                self.assertEqual(alternates, {
                    **{code: f"{BASE}/{code.lower()}/{suffix}" for code in STRATEGY["published_locales"]},
                    "x-default": f"{BASE}/en-us/{suffix}",
                })
            else:
                tail = "/".join(parts[1:])
                self.assertEqual(alternates, {
                    "en": f"{BASE}/en/" + (f"{tail}/" if tail else ""),
                    "ar": f"{BASE}/ar/" + (f"{tail}/" if tail else ""),
                    "x-default": f"{BASE}/en/" + (f"{tail}/" if tail else ""),
                })

    def test_robots_txt_references_both_canonical_sitemaps(self):
        lines = [line.strip() for line in (DIST / "robots.txt").read_text(encoding="utf-8").splitlines() if line.strip()]
        self.assertIn("User-agent: *", lines)
        self.assertIn("Allow: /", lines)
        self.assertEqual([line for line in lines if line.lower().startswith("sitemap:")], [f"Sitemap: {BASE}/sitemap.xml", f"Sitemap: {BASE}/sitemap.txt"])

    def test_text_sitemap_contains_root_and_all_language_routes(self):
        urls = [line.strip() for line in (DIST / "sitemap.txt").read_text(encoding="utf-8").splitlines() if line.strip()]
        self.assertEqual(len(urls), len(resource_routes()) + (len(STRATEGY["published_locales"]) * 14))
        self.assertEqual(len(urls), len(set(urls)))
        self.assertNotIn(f"{BASE}/", urls)
        for lang in ("en", "ar"):
            for section in ("home", "about", "features", "download", "faq"):
                expected = f"{BASE}/{lang}/" + ("" if section == "home" else f"{section}/")
                self.assertIn(expected, urls)

    def test_screenshot_asset_exists(self):
        self.assertTrue((DIST / "assets/screens/screen-1.webp").is_file())

    def test_homepage_uses_five_distinct_google_play_screenshots(self):
        for lang in ("en", "ar"):
            parser = PageParser()
            parser.feed(output_path(lang).read_text(encoding="utf-8"))
            gallery_images = parser.images[1:6]
            self.assertEqual(len(parser.images), 11)
            self.assertEqual(len(gallery_images), 5)
            self.assertEqual(len({image.get("src") for image in gallery_images}), 5)
            self.assertTrue(all(image.get("src", "").startswith("https://play-lh.googleusercontent.com/") for image in gallery_images))
            self.assertTrue(all(image.get("alt", "").strip() for image in gallery_images))
            self.assertIn('id="screenshots"', output_path(lang).read_text(encoding="utf-8"))


    def test_download_pages_have_official_store_cta_and_seo(self):
        for lang in ("en", "ar"):
            source = output_path(lang, "download").read_text(encoding="utf-8")
            parser = PageParser()
            parser.feed(source)
            self.assertIn(APP["google_play_url"], parser.links)
            self.assertIn('rel="canonical"', source)
            self.assertIn('hreflang="ar"', source)
            self.assertIn('hreflang="en"', source)
            self.assertIn('hreflang="x-default"', source)
            self.assertIn('name="description"', source)
            self.assertIn('name="robots" content="index,follow', source)
            self.assertIn('property="og:image"', source)
            self.assertIn('name="twitter:card"', source)
            self.assertIn('"@type": "SoftwareApplication"', source)
            self.assertIn('"@type": "Organization"', source)
            self.assertIn(APP["package_id"], source)
            self.assertIn("target=\"_blank\"", source)

    def test_features_pages_show_each_feature_and_download_cta(self):
        for lang in ("en", "ar"):
            source = output_path(lang, "features").read_text(encoding="utf-8")
            parser = PageParser()
            parser.feed(source)
            self.assertEqual(len(parser.images), 5)
            self.assertIn(APP["google_play_url"], parser.links)
            self.assertIn('id="feature-discovery"', source)
            self.assertIn('id="feature-collections"', source)

    def test_ga4_tracks_google_play_ctas_with_page_context(self):
        measurement_id = APP["ga4_measurement_id"]
        expected_locations = {
            "home": ["home_hero"],
            "about": ["about_intro"],
            "features": ["features_end"],
            "download": ["download_hero", "download_end"],
            "faq": ["faq_end"],
        }
        for lang in ("en", "ar"):
            for section, locations in expected_locations.items():
                source = output_path(lang, section).read_text(encoding="utf-8")
                parser = PageParser()
                parser.feed(source)
                self.assertIn(f"https://www.googletagmanager.com/gtag/js?id={measurement_id}", source)
                self.assertIn(f"gtag('config', '{measurement_id}')", source)
                self.assertIn("gtag('event', 'google_play_click'", source)
                self.assertEqual([cta.get("data-cta-location") for cta in parser.tracked_ctas], locations)
                for cta in parser.tracked_ctas:
                    self.assertEqual(cta.get("href"), APP["google_play_url"])
                    self.assertEqual(cta.get("data-analytics-event"), "google_play_click")
        root = (DIST / "index.html").read_text(encoding="utf-8")

    def test_pages_have_skip_links_and_single_main_heading(self):
        for lang in ("en", "ar"):
            for section in ("home", "about", "features", "download", "faq"):
                source = output_path(lang, section).read_text(encoding="utf-8")
                self.assertIn('<a class="skip-link" href="#main-content">', source)
                self.assertIn('<main id="main-content">', source)
                self.assertEqual(source.count("<h1"), 1)
        root = (DIST / "index.html").read_text(encoding="utf-8")

    def test_all_images_have_alt_text_and_intrinsic_dimensions(self):
        for path in DIST.rglob("*.html"):
            parser = PageParser()
            parser.feed(path.read_text(encoding="utf-8"))
            for image in parser.all_images:
                self.assertTrue(image.get("alt", "").strip(), str(path))
                self.assertTrue(image.get("width", "").isdigit(), str(path))
                self.assertTrue(image.get("height", "").isdigit(), str(path))

    def test_navigation_sits_opposite_the_unchanged_brand(self):
        css = (DIST / "assets/style.css").read_text(encoding="utf-8")
        self.assertIn(".header-main>nav{margin-inline-start:auto;justify-content:flex-end}", css)
        self.assertIn(".home-header>.header-main{align-self:stretch;width:100%}", css)
        for lang in ("en", "ar"):
            for section in ("home", "about", "features", "download", "faq", "blog", "guide", "tips", "comparison"):
                path = DIST / lang / ("" if section == "home" else section) / "index.html"
                source = path.read_text(encoding="utf-8")
                self.assertLess(source.index('<a class="brand"'), source.index("<nav aria-label="))

    def test_navigation_has_keyboard_focus_and_touch_targets(self):
        css = (DIST / "assets/style.css").read_text(encoding="utf-8")
        self.assertIn("a:focus-visible{outline:", css)
        self.assertIn("min-height:44px;padding:8px 0", css)
        self.assertIn(".btn{min-height:48px", css)

    def test_gallery_images_keep_landscape_aspect_ratio(self):
        css = (DIST / "assets/style.css").read_text(encoding="utf-8")
        self.assertIn(".shot img{display:block;width:100%;height:auto;aspect-ratio:auto;", css)
        for lang in ("en", "ar"):
            parser = PageParser()
            parser.feed(output_path(lang).read_text(encoding="utf-8"))
            for image in parser.images[1:6]:
                self.assertEqual(image.get("width"), "526")
                self.assertEqual(image.get("height"), "296")

    def test_faq_has_measurable_google_play_cta(self):
        for lang in ("en", "ar"):
            parser = PageParser()
            parser.feed(output_path(lang, "faq").read_text(encoding="utf-8"))
            self.assertIn(APP["google_play_url"], parser.links)
            self.assertEqual([cta.get("data-cta-location") for cta in parser.tracked_ctas], ["faq_end"])

    def test_bilingual_blog_and_resource_pages_exist(self):
        for lang in ("en", "ar"):
            for tail in ("blog", "guide", "tips", "comparison"):
                self.assertTrue((DIST / lang / tail / "index.html").is_file())
            for article in DATA:
                path = DIST / lang / "blog" / article[0] / "index.html"
                self.assertTrue(path.is_file())
                source = path.read_text(encoding="utf-8")
                self.assertIn(article[1] if lang == "en" else article[2], source)
                self.assertIn('"@type": "Article"', source)
                self.assertIn('hreflang="ar"', source)
                self.assertIn('hreflang="en"', source)

    def test_guide_uses_all_five_real_store_screenshots(self):
        for lang in ("en", "ar"):
            parser = PageParser()
            parser.feed((DIST / lang / "guide" / "index.html").read_text(encoding="utf-8"))
            self.assertEqual(len(parser.images), 5)
            self.assertTrue(all(image.get("alt") and image.get("width") == "526" for image in parser.images))
            manifest = json.loads((ROOT / "content/screenshots.json").read_text(encoding="utf-8"))
            self.assertEqual({i.get("src") for i in parser.images}, {s["src"] for s in manifest})

    def test_flags_are_inline_on_non_home_pages(self):
        for lang in ("en", "ar"):
            for tail in ("about", "features", "download", "faq", "blog", "guide", "tips", "comparison"):
                source = (DIST / lang / tail / "index.html").read_text(encoding="utf-8")
                self.assertIn('class="standard-header"', source)
                self.assertLess(source.index('<div class="header-main">'), source.index('<div class="locale-switch"'))


    def test_social_platform_links_are_present_on_legacy_pages(self):
        expected = {
            "Facebook": "https://www.facebook.com/",
            "X": "https://x.com/",
            "TikTok": "https://www.tiktok.com/",
            "Instagram": "https://www.instagram.com/",
        }
        for lang in ("en", "ar"):
            for tail in ("about", "features", "download", "faq", "blog", "guide", "tips", "comparison"):
                path = DIST / lang / tail / "index.html" if tail else DIST / lang / "index.html"
                source = path.read_text(encoding="utf-8")
                self.assertEqual(source.count('<div class="social-links" aria-label="Social media">'), 1)
                for label, url in expected.items():
                    self.assertIn(f'href="{url}" target="_blank" rel="noopener noreferrer" aria-label="{label}"', source)

    def test_resource_navigation_is_present(self):
        for lang in ("en", "ar"):
            for tail in ("", "about", "features", "download", "faq", "blog", "guide", "tips", "comparison"):
                path = DIST / lang / tail / "index.html" if tail else DIST / lang / "index.html"
                source = path.read_text(encoding="utf-8")
                for section in ("blog", "guide", "tips", "comparison"):
                    self.assertIn(f'href="{BASE}/{lang}/{section}/"', source)

    def test_comparison_is_qualified_not_a_performance_benchmark(self):
        for lang in ("en", "ar"):
            source = (DIST / lang / "comparison" / "index.html").read_text(encoding="utf-8")
            self.assertIn("independent performance study" if lang == "en" else "مقارنة وصفية", source)


    def test_jsonld_software_organization_and_faqpage_are_valid(self):
        import re
        for lang in ("en", "ar"):
            for section in ("home", "about", "features", "download", "faq"):
                source = output_path(lang, section).read_text(encoding="utf-8")
                scripts = re.findall(r'<script type="application/ld\+json">(.*?)</script>', source, re.S)
                self.assertTrue(scripts, f"Missing JSON-LD on {lang}/{section}")
                graph = json.loads(scripts[0])["@graph"]
                types = [node.get("@type") for node in graph]
                self.assertIn("Organization", types)
                self.assertIn("SoftwareApplication", types)
                self.assertNotIn("MobileApplication", types)
                faq_nodes = [node for node in graph if node.get("@type") == "FAQPage"]
                if section == "faq":
                    self.assertEqual(len(faq_nodes), 1)
                    self.assertEqual(len(faq_nodes[0]["mainEntity"]), len(FAQ))
                    for item in FAQ:
                        self.assertTrue(any(q["name"] == item["q"][lang] for q in faq_nodes[0]["mainEntity"]))
                        self.assertIn(item["q"][lang], source)
                        self.assertIn(item["a"][lang], source)
                else:
                    self.assertFalse(faq_nodes)

    def test_feature_detail_pages_are_bilingual_and_in_sitemap(self):
        urls = [line.strip() for line in (DIST / "sitemap.txt").read_text(encoding="utf-8").splitlines()]
        for lang in ("en", "ar"):
            for feature in FEATURES:
                path = DIST / lang / "features" / feature["id"] / "index.html"
                self.assertTrue(path.is_file())
                source = path.read_text(encoding="utf-8")
                self.assertIn(feature["title"][lang], source)
                self.assertIn('"@type": "Organization"', source)
                self.assertIn('hreflang="ar"', source)
                self.assertIn('hreflang="en"', source)
                self.assertIn(f"{BASE}/{lang}/features/{feature['id']}/", urls)

    def test_keyword_targets_are_documented_without_fake_volume_claims(self):
        targets = json.loads((ROOT / "content/seo-keywords.json").read_text(encoding="utf-8"))
        self.assertIn("fruit match 3 game", targets["en"]["primary"])
        self.assertIn("البحث عن عمل", targets["ar"]["primary"])
        self.assertIn("not verified", targets["note"])


    def test_every_language_selector_uses_eight_real_country_flag_images(self):
        import re
        expected = set(STRATEGY["published_locales"])
        for path in DIST.rglob("*.html"):
            source = path.read_text(encoding="utf-8")
            if 'class="locale-switch"' not in source:
                continue
            flags = re.findall(
                r'<a class="locale-flag" lang="([^"]+)"[^>]*>(.*?)</a>',
                source,
                re.DOTALL,
            )
            self.assertEqual({code for code, _ in flags}, expected, str(path))
            self.assertEqual(len(flags), 8, str(path))
            for code, markup in flags:
                self.assertRegex(
                    markup,
                    r'<img src="https://flagcdn\.com/w80/[a-z]{2}\.png" alt="[^"]+ flag" width="40" height="30"',
                    f"{path}: {code}",
                )

    def test_no_previous_brand(self):
        for path in DIST.rglob("*.html"):
            self.assertNotIn("Mingle", path.read_text(encoding="utf-8"))

if __name__ == "__main__":
    unittest.main()
