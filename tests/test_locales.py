import json
import re
import pathlib
import subprocess
import sys
import unittest
from urllib.parse import urlparse
import xml.etree.ElementTree as ET
from html.parser import HTMLParser

ROOT = pathlib.Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
APP = json.loads((ROOT / "content/app.json").read_text(encoding="utf-8"))
STRATEGY = json.loads((ROOT / "content/market-strategy.json").read_text(encoding="utf-8"))
BASE = APP["website_url"].rstrip("/")
NS = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
XHTML = "{http://www.w3.org/1999/xhtml}"

class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.alternates = {}
        self.canonical = None
        self.links = []
        self.title = ""
        self.description = None
        self.in_title = False
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "title":
            self.in_title = True
        if tag == "meta" and attrs.get("name") == "description":
            self.description = attrs.get("content")
        if tag == "link" and attrs.get("rel") == "canonical":
            self.canonical = attrs.get("href")
        if tag == "link" and attrs.get("rel") == "alternate":
            self.alternates[attrs.get("hreflang")] = attrs.get("href")
        if tag == "a" and attrs.get("href"):
            self.links.append(attrs["href"])
    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False
    def handle_data(self, data):
        if self.in_title:
            self.title += data

class MarketLocaleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        subprocess.run([sys.executable, str(ROOT / "scripts/build.py")], check=True)
        subprocess.run([sys.executable, str(ROOT / "scripts/validate.py")], check=True)

    def test_locale_titles_and_descriptions_are_localized_and_within_snippet_bounds(self):
        for locale in STRATEGY["published_locales"]:
            bundle = json.loads((ROOT / "content/locales.json").read_text(encoding="utf-8"))[locale]
            observed_titles = set()
            for section in ("", "about", "features", "download", "faq"):
                path = DIST / locale.lower() / section / "index.html" if section else DIST / locale.lower() / "index.html"
                parser = Links()
                parser.feed(path.read_text(encoding="utf-8"))
                key = section or "home"
                self.assertEqual(parser.title, bundle["titles"][key], f"{locale}/{key} title")
                self.assertEqual(parser.description, bundle["descriptions"][key], f"{locale}/{key} description")
                self.assertLessEqual(len(parser.title), 60, f"{locale}/{key} title too long")
                self.assertLessEqual(len(parser.description), 160, f"{locale}/{key} description too long")
                self.assertNotIn(parser.title, observed_titles, f"Duplicate title in {locale}")
                observed_titles.add(parser.title)

    def test_market_keyword_clusters_are_relevant_and_avoid_unverified_promises(self):
        clusters = STRATEGY["initial_keyword_clusters"]
        expected = set(STRATEGY["published_locales"])
        self.assertEqual(set(clusters), expected)
        for locale, config in clusters.items():
            self.assertTrue(config["primary"])
            self.assertTrue(config["secondary"])
            self.assertTrue(config["clusters"])
            self.assertTrue(all(item["primary"] for item in config["clusters"]))
            bundle = json.loads((ROOT / "content/locales.json").read_text(encoding="utf-8"))[locale]
            metadata = " ".join(bundle["titles"].values()) + " " + " ".join(bundle["descriptions"].values())
            folded = metadata.casefold()
            for term in config["excluded_terms"]:
                self.assertNotIn(term.casefold(), folded, f"Unsupported keyword claim in {locale}: {term}")
        self.assertIn("fruit match 3 game", " ".join(clusters["en-US"]["primary"]))
        self.assertIn("fruit match 3 game Canada", " ".join(clusters["en-CA"]["primary"]))
        self.assertIn("jeu de puzzle de fruits", " ".join(clusters["fr-CA"]["primary"]))

    def test_only_explicitly_published_locales_are_generated(self):
        expected = {x.lower() for x in STRATEGY["published_locales"]}
        bundle_locales = json.loads((ROOT / "content/locales.json").read_text(encoding="utf-8"))
        self.assertEqual(expected, {x.lower() for x in bundle_locales})
        for locale in expected:
            self.assertTrue((DIST / locale / "index.html").is_file())
        for locale in ("nl-nl", "pl-pl", "en-gb"):
            self.assertFalse((DIST / locale).exists(), f"Unpublished locale was generated: {locale}")

    def test_all_core_routes_exist_and_have_self_canonical(self):
        for locale in STRATEGY["published_locales"]:
            slug = locale.lower()
            for section in ("", "about", "features", "download", "faq"):
                path = DIST / slug / (section or "") / "index.html"
                self.assertTrue(path.is_file(), f"Missing {locale}/{section}")
                parser = Links()
                parser.feed(path.read_text(encoding="utf-8"))
                expected = f"{BASE}/{slug}/" + ("" if not section else f"{section}/")
                self.assertEqual(parser.canonical, expected)

    def test_hreflang_is_complete_and_reciprocal_for_every_equivalent_page(self):
        expected_locales = set(STRATEGY["published_locales"])
        for locale in expected_locales:
            slug = locale.lower()
            for section in ("", "about", "features", "download", "faq"):
                path = DIST / slug / (section or "") / "index.html"
                parser = Links()
                parser.feed(path.read_text(encoding="utf-8"))
                tail = "" if not section else f"{section}/"
                expected = {code: f"{BASE}/{code.lower()}/{tail}" for code in expected_locales}
                expected["x-default"] = f"{BASE}/en-us/{tail}"
                self.assertEqual(parser.alternates, expected, f"{locale}/{section}")

    def test_localized_navigation_stays_within_the_market_locale_family(self):
        for locale in STRATEGY["published_locales"]:
            source = (DIST / locale.lower() / "index.html").read_text(encoding="utf-8")
            parser = Links()
            parser.feed(source)
            for target in {x.lower() for x in STRATEGY["published_locales"]}:
                self.assertTrue(
                    any(link.startswith(f"{BASE}/{target}/") for link in parser.links),
                    f"{locale} has no flag link for {target}",
                )
            self.assertNotIn(f"{BASE}/ar/", parser.links)
            self.assertNotIn(f"{BASE}/en/", parser.links)

    def test_navigation_groups_keep_related_pages_in_two_dropdowns(self):
        expected_paths = {
            "primary": ("about/", "features/", "download/", "faq/"),
            "resources": ("tips/", "blog/", "guide/", "comparison/"),
        }
        for locale in STRATEGY["published_locales"]:
            slug = locale.lower()
            source = (DIST / slug / "index.html").read_text(encoding="utf-8")
            groups = re.findall(r'<details class="nav-menu" data-nav-group="([^"]+)">(.*?)</details>', source, re.DOTALL)
            self.assertEqual([name for name, _ in groups], ["primary", "resources"], locale)
            for name, markup in groups:
                self.assertEqual(len(re.findall(r'<a data-nav-item="[^"]+"', markup)), 4, f"{locale}/{name}")
                for suffix in expected_paths[name]:
                    self.assertIn(f'href="{BASE}/{slug}/{suffix}"', markup, f"{locale}/{name}/{suffix}")
                self.assertIn("<summary>", markup)
            nav_markup = source[source.index("<nav"):source.index("</nav>")]
            self.assertEqual(nav_markup.count("<details "), 2, locale)
    def test_french_pages_have_genuine_french_content_and_metadata(self):
        for locale in ("fr-CA", "fr-FR"):
            source = (DIST / locale.lower() / "index.html").read_text(encoding="utf-8")
            self.assertIn(f'<html lang="{locale}"', source)
            self.assertIn("Découvrez", source)
            self.assertIn("Jeu de puzzle de fruits", source)
            self.assertIn("Foire aux questions", (DIST / locale.lower() / "faq" / "index.html").read_text(encoding="utf-8"))
            self.assertNotIn("Discover your next opportunity", source)
            self.assertNotIn("Frequently asked questions", source)

    def test_localized_feature_detail_routes_are_real_and_reciprocal(self):
        from scripts.build import FEATURES
        for locale in STRATEGY["published_locales"]:
            slug = locale.lower()
            for feature in FEATURES:
                tail = f"features/{feature['id']}/"
                path = DIST / slug / tail / "index.html"
                self.assertTrue(path.is_file(), f"Missing {locale}/{tail}")
                parser = Links()
                parser.feed(path.read_text(encoding="utf-8"))
                self.assertEqual(parser.canonical, f"{BASE}/{slug}/{tail}")
                self.assertEqual(parser.alternates, {
                    **{code: f"{BASE}/{code.lower()}/{tail}" for code in STRATEGY["published_locales"]},
                    "x-default": f"{BASE}/en-us/{tail}",
                })

    def test_sitemaps_contain_exactly_published_locale_routes(self):
        from scripts.build import FEATURES
        expected = {
            f"{BASE}/{locale.lower()}/{tail}"
            for locale in STRATEGY["published_locales"]
            for tail in ("", "about/", "features/", "download/", "faq/")
        }
        expected.update(
            f"{BASE}/{locale.lower()}/features/{feature['id']}/"
            for locale in STRATEGY["published_locales"] for feature in FEATURES
        )
        xml_root = ET.parse(DIST / "sitemap.xml").getroot()
        entries = xml_root.findall(f"{NS}url")
        xml_urls = {node.findtext(f"{NS}loc") for node in entries}
        text_urls = set((DIST / "sitemap.txt").read_text(encoding="utf-8").splitlines())
        self.assertTrue(expected.issubset(xml_urls))
        self.assertTrue(expected.issubset(text_urls))
        self.assertEqual(len(xml_urls), len(entries))
        self.assertEqual(len(text_urls), len((DIST / "sitemap.txt").read_text(encoding="utf-8").splitlines()))
        for locale in ("nl-NL", "pl-PL", "en-GB"):
            self.assertFalse(any(f"/{locale.lower()}/" in url for url in xml_urls | text_urls))

    def test_sitemap_hreflang_reciprocity(self):
        root = ET.parse(DIST / "sitemap.xml").getroot()
        expected_locales = set(STRATEGY["published_locales"])
        for node in root.findall(f"{NS}url"):
            loc = node.findtext(f"{NS}loc") or ""
            if not any(f"/{code.lower()}/" in loc for code in expected_locales):
                continue
            base_path = urlparse(BASE).path.rstrip("/") + "/"
            relative = urlparse(loc).path[len(base_path):]
            parts = relative.split("/", 1)
            rest = parts[1] if len(parts) > 1 else ""
            base_tail = rest
            alternates = {item.get("hreflang"): item.get("href") for item in node.findall(f"{XHTML}link")}
            expected = {code: f"{BASE}/{code.lower()}/{base_tail}" for code in expected_locales}
            expected["x-default"] = f"{BASE}/en-us/{base_tail}"
            self.assertEqual(alternates, expected, loc)

    def test_flags_are_above_site_name_only_on_home_and_inline_elsewhere(self):
        expected_flags = {
            "en-US": ("us", "United States"), "en-CA": ("ca", "Canada"), "fr-CA": ("ca", "Canada"),
            "es-ES": ("es", "Spain"), "pt-PT": ("pt", "Portugal"), "fr-FR": ("fr", "France"),
            "de-DE": ("de", "Germany"), "it-IT": ("it", "Italy"),
        }
        for locale in STRATEGY["published_locales"]:
            home = (DIST / locale.lower() / "index.html").read_text(encoding="utf-8")
            self.assertIn('<header class="home-header">', home)
            self.assertLess(home.index('<div class="locale-switch"'), home.index('<div class="header-main">'))
            for code, (flag, country_name) in expected_flags.items():
                self.assertIn(f'lang="{code}"', home)
                self.assertIn(f'<img src="https://flagcdn.com/w80/{flag}.png" alt="{country_name} flag" width="40" height="30"', home)
                self.assertNotIn(f'<span aria-hidden="true">{flag}</span>', home)
            for tail in ("about", "features", "download", "faq"):
                page = (DIST / locale.lower() / tail / "index.html").read_text(encoding="utf-8")
                self.assertIn('<header class="standard-header">', page)
                self.assertLess(page.index('<div class="header-main">'), page.index('<div class="locale-switch"'))
                self.assertLess(page.index('<div class="locale-switch"'), page.index('<a class="brand"'))
                for code, (flag, country_name) in expected_flags.items():
                    self.assertIn(f'lang="{code}"', page)
                    self.assertIn(f'<img src="https://flagcdn.com/w80/{flag}.png" alt="{country_name} flag" width="40" height="30"', page)
                self.assertNotRegex(page, r'<a class="locale-flag"[^>]*>\\s*<span')
        root = (DIST / "index.html").read_text(encoding="utf-8")
        self.assertIn(f'<meta http-equiv="refresh" content="0; url={BASE}/en-us/about/">', root)
        self.assertNotIn('class="locale-switch"', root)
        css = (DIST / "assets/style.css").read_text(encoding="utf-8")
        self.assertIn(".header-main>nav{margin-inline-start:auto;justify-content:flex-end}", css)
        self.assertIn(".home-header>.header-main{align-self:stretch;width:100%}", css)
        for locale in STRATEGY["published_locales"]:
            for tail in ("", "about", "features", "download", "faq"):
                path = DIST / locale.lower() / ("" if not tail else tail) / "index.html"
                source = path.read_text(encoding="utf-8")
                self.assertLess(source.index('<a class="brand"'), source.index('<nav aria-label="Primary navigation">'))


    def test_social_links_are_present_on_every_published_locale_page(self):
        expected = {
            "Facebook": "https://www.facebook.com/",
            "X": "https://x.com/",
            "TikTok": "https://www.tiktok.com/",
            "Instagram": "https://www.instagram.com/",
        }
        for locale in STRATEGY["published_locales"]:
            for tail in ("", "about", "features", "download", "faq"):
                path = DIST / locale.lower() / (tail or "") / "index.html"
                source = path.read_text(encoding="utf-8")
                self.assertEqual(source.count('<div class="social-links" aria-label="Social media">'), 1)
                for label, url in expected.items():
                    self.assertIn(f'href="{url}" target="_blank" rel="noopener noreferrer" aria-label="{label}"', source)

    def test_root_redirect_has_no_language_selector(self):
        source = (DIST / "index.html").read_text(encoding="utf-8")
        self.assertIn(f'<link rel="canonical" href="{BASE}/en-us/about/">', source)
        self.assertIn(f'<meta http-equiv="refresh" content="0; url={BASE}/en-us/about/">', source)
        self.assertNotIn('class="locale-switch"', source)
        self.assertNotIn("Choose your language", source)
        self.assertNotIn("اختر لغتك", source)

if __name__ == "__main__":
    unittest.main()
