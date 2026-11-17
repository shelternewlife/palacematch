#!/usr/bin/env python3
import html
import json
import pathlib
import shutil

ROOT = pathlib.Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
APP = json.loads((ROOT / "content/app.json").read_text(encoding="utf-8"))
FEATURES = json.loads((ROOT / "content/features.json").read_text(encoding="utf-8"))
FAQ = json.loads((ROOT / "content/faq.json").read_text(encoding="utf-8"))
SCREENSHOTS = json.loads((ROOT / "content/screenshots.json").read_text(encoding="utf-8"))
BASE_URL = APP["website_url"].rstrip("/")
GA_MEASUREMENT_ID = APP["ga4_measurement_id"]

TEXT = {
    "en": {
        "about": "About Palace Match",
        "skip_to_content": "Skip to main content",
        "features": "Explore the features",
        "faq": "Frequently asked questions",
        "download_nav": "Download",
        "download_title": "Download Palace Match for Android",
        "download_intro": "Get the official Palace Match Android app from Google Play and start exploring job opportunities, useful context and personal collections.",
        "download_steps_title": "Install in three simple steps",
        "download_step_1": "Open the official Google Play listing.",
        "download_step_2": "Tap Install on your Android device.",
        "download_step_3": "Open Palace Match and explore opportunities.",
        "download_note": "For your security, install the app only through its official Google Play listing.",
        "download_facts": "App information",
        "platform": "Platform",
        "developer": "Developer",
        "package": "Package ID",
        "home": "Match colorful fruit and rise through the palace",
        "cta": "Open on Google Play",
        "tag": "FRUIT MATCH-3 PUZZLE",
        "gallery": "A look inside the app",
        "gallery_intro": "Real screenshots from the Google Play listing.",
        "download": "Get started with Palace Match",
        "privacy": "Privacy policy",
        "support": "Support",
        "about_intro": "Learn about the fruit match-3 puzzle gameplay, modes and progression in Palace Match.",
        "features_intro": "Explore fruit matching, combos, coins, XP progression and game modes in Palace Match.",
        "faq_intro": "Answers to common questions about playing Palace Match.",
        "language": "Choose your language",
        "english": "English",
        "arabic": "العربية",
        "home_intro": "Swap fruit, create combos, collect coins and progress through palace levels.",
    },
    "ar": {
        "about": "عن Palace Match",
        "skip_to_content": "تجاوز إلى المحتوى الرئيسي",
        "features": "استكشف المزايا",
        "faq": "الأسئلة الشائعة",
        "download_nav": "تنزيل التطبيق",
        "download_title": "تنزيل Palace Match لنظام Android",
        "download_intro": "احصل على تطبيق Palace Match الرسمي لنظام Android من Google Play، وابدأ باستكشاف فرص العمل وسياقها المفيد ومجموعاتك الشخصية.",
        "download_steps_title": "ثبّت التطبيق في ثلاث خطوات بسيطة",
        "download_step_1": "افتح صفحة التطبيق الرسمية على Google Play.",
        "download_step_2": "اضغط على تثبيت من جهاز Android.",
        "download_step_3": "افتح Palace Match وابدأ استكشاف الفرص.",
        "download_note": "لحمايتك، ثبّت التطبيق من صفحته الرسمية على Google Play فقط.",
        "download_facts": "معلومات التطبيق",
        "platform": "النظام",
        "developer": "المطور",
        "package": "معرّف الحزمة",
        "home": "اكتشف فرصتك المهنية القادمة",
        "cta": "افتح التطبيق على Google Play",
        "tag": "اكتشاف فرص العمل",
        "gallery": "نظرة إلى واجهة التطبيق",
        "gallery_intro": "لقطات شاشة فعلية منشورة في صفحة التطبيق على Google Play.",
        "download": "ابدأ مع Palace Match",
        "privacy": "سياسة الخصوصية",
        "support": "الدعم",
        "about_intro": "تعرّف على Palace Match وما صُمم لمساعدتك على اكتشافه وتنظيمه.",
        "features_intro": "استكشف إمكانات الاكتشاف والتنظيم الموضحة لتطبيق Palace Match.",
        "faq_intro": "إجابات عن الأسئلة الشائعة حول Palace Match.",
        "language": "اختر لغتك",
        "english": "English",
        "arabic": "العربية",
        "home_intro": "استكشف فرص العمل وراجع سياقها المفيد واحتفظ بالوظائف التي تهمك للمتابعة.",
    },
}

PAGE_TITLES = {
    "en": {
        "home": "Job Search App for Finding Work Opportunities | Palace Match",
        "about": "Palace Match: About the Job Search and Opportunity Discovery App",
        "features": "Job Search App Features: Discover, Compare and Organize Jobs | Palace Match",
        "download": "Download Palace Match: Android Job Search App | Google Play",
        "faq": "Palace Match FAQ: Job Search, Job Listings and App Features",
    },
    "ar": {
        "home": "البحث عن عمل واكتشاف الوظائف | Palace Match",
        "about": "Palace Match: تطبيق للبحث عن عمل واكتشاف الوظائف",
        "features": "مزايا تطبيق Palace Match لاكتشاف فرص العمل وتنظيمها",
        "download": "تنزيل تطبيق Palace Match للبحث عن عمل | Google Play",
        "faq": "الأسئلة الشائعة حول Palace Match والبحث عن الوظائف",
    },
}

PAGE_DESCRIPTIONS = {
    "en": {
        "home": "Explore job opportunities, compare role details and organize jobs to follow with Palace Match, an Android job search app.",
        "about": "Learn how the Palace Match Android app helps you discover job listings, review opportunity details and organize roles to follow.",
        "features": "Explore job search tools for discovering fresh opportunities, comparing job details, reviewing indicators and organizing job listings.",
        "download": "Download Palace Match, an Android job search app for discovering and organizing job opportunities. Install it from Google Play.",
        "faq": "Get answers about job listings, opportunity indicators, personal collections and downloading the Palace Match Android app.",
    },
    "ar": {
        "home": "اكتشف فرص العمل والوظائف الشاغرة، وراجع تفاصيلها ونظّم الفرص التي تريد متابعتها باستخدام تطبيق Palace Match لنظام Android.",
        "about": "تعرّف على تطبيق Palace Match للبحث عن عمل واكتشاف إعلانات الوظائف ومراجعة تفاصيل الفرص وتنظيمها.",
        "features": "اكتشف أدوات البحث عن وظائف: متابعة الفرص الحديثة ومقارنة تفاصيل الوظائف ومراجعة المؤشرات وتنظيم إعلانات العمل.",
        "download": "نزّل تطبيق Palace Match للبحث عن عمل واكتشاف فرص العمل على Android من صفحة Google Play الرسمية.",
        "faq": "إجابات عن البحث عن وظائف وإعلانات العمل ومؤشرات الفرص والمجموعات وتنزيل تطبيق Palace Match.",
    },
}

CSS = """*{box-sizing:border-box}body{margin:0;background:#080b12;color:#f4f7fb;font:16px/1.75 system-ui,sans-serif}a{color:inherit}a:focus-visible{outline:3px solid #00c4df;outline-offset:4px}.btn{min-height:48px;display:inline-flex;align-items:center;justify-content:center}.skip-link{position:absolute;z-index:10;top:8px;left:8px;padding:10px 14px;background:#00c4df;color:#061018;border-radius:8px;font-weight:800;transform:translateY(-160%)}.skip-link:focus{transform:translateY(0)}header,main,footer{width:min(1120px,calc(100% - 36px));margin:auto}header{display:flex;flex-direction:row;justify-content:flex-start;align-items:center;gap:18px;flex-wrap:wrap;padding:22px 0;border-bottom:1px solid #263246}.home-header{flex-direction:column;align-items:flex-start;gap:0}.home-header>.header-main{align-self:stretch;width:100%}.standard-header .locale-switch{margin:0;flex:0 0 auto}.home-header .locale-switch{margin:0 0 12px}.brand{font-weight:900;text-decoration:none;letter-spacing:.08em}.brand b,.tag{color:#00c4df}nav{display:flex;gap:22px;flex-wrap:wrap}nav a{color:#c4ccda;text-decoration:none;display:inline-flex;align-items:center;min-height:44px;padding:8px 0}.hero{padding:70px 0;display:grid;grid-template-columns:1fr .8fr;gap:44px;align-items:center}.tag{font-size:.8rem;letter-spacing:.16em;font-weight:700}.hero h1{font-size:clamp(2.5rem,6vw,4.6rem);line-height:1.12;margin:18px 0}.lead,.muted{color:#aab6c8}.btn{display:inline-block;background:#00c4df;color:#061018;text-decoration:none;padding:13px 20px;border-radius:9px;font-weight:800;margin-top:20px}.preview{padding:16px;background:#121a28;border:1px solid #29364b;border-radius:22px;text-align:center}.preview img{height:480px;max-width:100%;object-fit:contain;border-radius:12px}.section{padding:48px 0;border-top:1px solid #ffffff18}.section h2{font-size:2rem}.grid{display:grid;grid-template-columns:repeat(2,1fr);gap:16px}.item,.faq{background:#111925;border:1px solid #283449;border-radius:14px;padding:22px}.item h3,.faq h3{margin-top:0}.item p,.faq p{color:#aab6c8}.feature-shot{display:block;width:100%;max-height:230px;object-fit:contain;object-position:left center;background:#080b12;border-radius:9px;margin:0 0 16px}.steps{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}.step{background:#111925;border:1px solid #283449;border-radius:14px;padding:20px}.step b{display:block;color:#00c4df;font-size:1.3rem}.facts{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}.fact{padding:16px;background:#111925;border:1px solid #283449;border-radius:12px;overflow-wrap:anywhere}.fact small{display:block;color:#aab6c8}.download-hero{padding:58px 0;display:grid;grid-template-columns:1fr .65fr;gap:36px;align-items:center}.download-hero h1{font-size:clamp(2.2rem,5vw,3.8rem);line-height:1.15}.num{color:#00c4df;font:700 .8rem monospace}.faqgrid{display:grid;grid-template-columns:repeat(2,1fr);gap:14px}.gallery{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:16px}.shot{margin:0;padding:12px;background:#111925;border:1px solid #283449;border-radius:14px}.shot img{display:block;width:100%;height:auto;aspect-ratio:auto;object-fit:contain;background:#080b12;border-radius:9px}.shot figcaption{padding:10px 2px 2px;color:#d6deeb;font-size:.92rem;line-height:1.5}.end{text-align:center;background:#11242d;border:1px solid #236071;border-radius:18px;padding:34px}.language{min-height:70vh;display:grid;place-items:center;text-align:center}.language a{display:inline-block;margin:8px;padding:14px 22px;border:1px solid #236071;border-radius:10px;text-decoration:none}footer{padding:30px 0;color:#aab6c8;border-top:1px solid #ffffff18;display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap}.locale-switch{display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:9px;width:100%;margin:0 0 12px}.header-main>.locale-switch{flex:0 0 100%;margin:0 0 10px}.social-links{display:flex;align-items:center;justify-content:flex-end;gap:10px;margin-inline-start:auto}.social-link{width:36px;height:36px;display:inline-flex;align-items:center;justify-content:center;border:1px solid #34445c;border-radius:9px;background:#111925;color:#dce6f4;text-decoration:none;transition:border-color .15s,transform .15s}.social-link:hover,.social-link:focus-visible{border-color:#00c4df;color:#00c4df;transform:translateY(-1px)}.social-link svg{width:19px;height:19px;fill:currentColor}.social-link:focus-visible{outline:3px solid #00c4df;outline-offset:3px}.locale-flag{width:42px;height:34px;display:inline-flex;align-items:center;justify-content:center;border:1px solid #34445c;border-radius:9px;background:#111925;text-decoration:none;line-height:1;transition:border-color .15s,transform .15s}.locale-flag img{display:block;width:28px;height:21px;object-fit:cover;border-radius:2px}.locale-flag:hover,.locale-flag:focus-visible{border-color:#00c4df;transform:translateY(-1px)}.locale-flag[aria-current="page"]{border-color:#00c4df;box-shadow:0 0 0 1px #00c4df55}.header-main{display:flex;justify-content:space-between;align-items:center;gap:18px;flex:1;min-width:0;flex-wrap:wrap}.header-main>nav{margin-inline-start:auto;justify-content:flex-end}.language-header{justify-content:flex-start;align-items:flex-start}.language-header .locale-switch{margin:0}html[dir=rtl] body{text-align:right}html[dir=rtl] header{direction:rtl}html[dir=rtl] .locale-switch{justify-content:flex-start}@media(max-width:760px){.hero,.download-hero{grid-template-columns:1fr;padding:42px 0}.preview img{height:360px}.grid,.faqgrid,.steps,.facts{grid-template-columns:1fr}header.standard-header{flex-direction:row;align-items:center;gap:10px}.standard-header .header-main{flex:1 1 260px;align-items:center;flex-direction:row;flex-wrap:wrap}.home-header{align-items:flex-start;flex-direction:column}.home-header .header-main{align-items:flex-start;flex-direction:column}nav{gap:14px}}"""

def render_analytics():
    return """<script async src="https://www.googletagmanager.com/gtag/js?id=__GA_ID__"></script>
<script>
window.dataLayer = window.dataLayer || [];
function gtag(){dataLayer.push(arguments);}
gtag('js', new Date());
gtag('config', '__GA_ID__');
document.addEventListener('click', function(event) {
    const target = event.target instanceof Element ? event.target : event.target.parentElement;
    const link = target && target.closest('a[data-analytics-event="google_play_click"]');
    if (!link) return;
    gtag('event', 'google_play_click', {
        page_path: window.location.pathname,
        page_language: document.documentElement.lang || 'unknown',
        page_section: document.body.dataset.pageSection || 'unknown',
        cta_location: link.dataset.ctaLocation || 'unknown',
        link_url: link.href,
        link_text: link.textContent.trim()
    });
});
</script>""".replace("__GA_ID__", GA_MEASUREMENT_ID)

def esc(value):
    return html.escape(str(value), quote=True)

def page_url(lang, section="home"):
    suffix = "" if section == "home" else f"{section}/"
    return f"{BASE_URL}/{lang}/{suffix}"


def render_social_links():
    items = (
        ("Facebook", "https://www.facebook.com/", '<path d="M13.5 21v-8h2.7l.4-3h-3.1V8.1c0-.9.3-1.5 1.6-1.5h1.7V3.9c-.3 0-1.3-.1-2.5-.1-2.5 0-4.2 1.5-4.2 4.2V10H7.3v3h2.8v8z"/>'),
        ("X", "https://x.com/", '<path d="M18.9 2H22l-6.8 7.8L23.2 22h-6.3L12 14.6 5.5 22H2.4l7.3-8.4L1.9 2h6.5l4.4 6.8zm-1.1 18h1.7L7.4 3.9H5.6z"/>'),
        ("TikTok", "https://www.tiktok.com/", '<path d="M19.6 7.2a6.9 6.9 0 0 1-4.2-1.4v8.1a6.1 6.1 0 1 1-6.1-6.1c.4 0 .8 0 1.2.1v3.4a2.8 2.8 0 1 0 1.6 2.6V2h3.4a3.9 3.9 0 0 0 4.1 3.7z"/>'),
        ("Instagram", "https://www.instagram.com/", '<rect x="3" y="3" width="18" height="18" rx="5" fill="none" stroke="currentColor" stroke-width="2.2"/><circle cx="12" cy="12" r="4" fill="none" stroke="currentColor" stroke-width="2.2"/><circle cx="18" cy="6.5" r="1.2"/>'),
    )
    links = []
    for label, url, artwork in items:
        links.append(
            f'<a class="social-link" href="{url}" target="_blank" rel="noopener noreferrer" '
            f'aria-label="{label}" title="{label}"><svg viewBox="0 0 24 24" aria-hidden="true" '
            f'focusable="false">{artwork}</svg></a>'
        )
    return '<div class="social-links" aria-label="Social media">' + "".join(links) + '</div>'

def render_market_flags(tail="", current=None):
    import build_locales
    return build_locales.render_locale_flags(
        build_locales.STRATEGY["published_locales"], tail, current
    )

def render_header(lang, section):
    t = TEXT[lang]
    nav_items = (("about", t["about"]), ("features", t["features"]),
                 ("download", t["download_nav"]), ("faq", t["faq"]))
    nav = "".join(
        f'<a data-nav-item="{key}" href="{page_url(lang, key)}">{esc(label)}</a>'
        for key, label in nav_items
    )
    tail = "" if section == "home" else f"{section}/"
    switch = render_market_flags(tail)
    return (
        f'<header class="{"home-header" if section == "home" else "standard-header"}"><div class="locale-switch" aria-label="Country and region">{switch}{render_social_links()}</div>'
        f'<div class="header-main"><a class="brand" href="{BASE_URL}/">JOB <b>CONNECT</b></a>'
        f'<nav aria-label="Primary navigation">'
        f'<details class="nav-menu" data-nav-group="primary"><summary>{"Explore" if lang == "en" else "استكشف"}</summary>'
        f'<div class="nav-dropdown">{nav}</div></details>'
        f'</nav></div></header>'
    )

def render_features(lang):
    cards = []
    for index, feature in enumerate(FEATURES, 1):
        detail_url = page_url(lang, "features/" + feature["id"])
        cards.append(
            f'<article class="item" id="feature-{esc(feature["id"])}">'
            f'<div class="num">{index:02d} / FEATURE</div>'
            f'<img class="feature-shot" src="{esc(SCREENSHOTS[index - 1]["src"])}" width="526" height="296" '
            f'alt="{esc(SCREENSHOTS[index - 1]["alt"][lang])}" loading="lazy" decoding="async">'
            f'<h2><a href="{detail_url}">{esc(feature["title"][lang])}</a></h2>'
            f'<p>{esc(feature["description"][lang])}</p>'
            f'<p><a href="{detail_url}">{"Explore this feature" if lang == "en" else "اكتشف تفاصيل الميزة"}</a></p></article>'
        )
    return '<div class="grid">' + "".join(cards) + "</div>"

def render_faq(lang):
    cards = []
    for item in FAQ:
        cards.append(
            f'<article class="faq"><h3>{esc(item["q"][lang])}</h3>'
            f'<p>{esc(item["a"][lang])}</p></article>'
        )
    return '<div class="faqgrid">' + "".join(cards) + "</div>"

def render_gallery(lang):
    t = TEXT[lang]
    cards = []
    for screenshot in SCREENSHOTS:
        cards.append(
            f'<figure class="shot"><img src="{esc(screenshot["src"])}" width="526" height="296" '
            f'alt="{esc(screenshot["alt"][lang])}" loading="lazy" decoding="async">'
            f'<figcaption>{esc(screenshot["caption"][lang])}</figcaption></figure>'
        )
    return (
        f'<section class="section" id="screenshots"><h2>{t["gallery"]}</h2>'
        f'<p class="muted">{t["gallery_intro"]}</p>'
        f'<div class="gallery">{"".join(cards)}</div></section>'
    )

def render_download(lang):
    t = TEXT[lang]
    return (
        f'<section class="download-hero"><div><div class="tag">PALACE MATCH · ANDROID</div>'
        f'<h1>{t["download_title"]}</h1><p class="lead">{esc(t["download_intro"])}</p>'
        f'<a class="btn" href="{esc(APP["google_play_url"])}" '
        f'target="_blank" rel="noopener noreferrer" aria-label="{esc(t["cta"])}" '
        f'data-analytics-event="google_play_click" data-cta-location="download_hero">{t["cta"]}</a>'
        f'<p class="muted">{esc(t["download_note"])}</p></div>'
        f'<div class="preview"><img src="{esc(SCREENSHOTS[0]["src"])}" width="526" height="296" '
        f'alt="{esc(SCREENSHOTS[0]["alt"][lang])}" loading="eager" decoding="async"></div></section>'
        f'<section class="section"><h2>{t["download_steps_title"]}</h2><div class="steps">'
        f'<article class="step"><b>01</b>{esc(t["download_step_1"])}</article>'
        f'<article class="step"><b>02</b>{esc(t["download_step_2"])}</article>'
        f'<article class="step"><b>03</b>{esc(t["download_step_3"])}</article>'
        f'</div></section>'
        f'<section class="section"><h2>{t["download_facts"]}</h2><div class="facts">'
        f'<div class="fact"><small>{t["platform"]}</small>Android</div>'
        f'<div class="fact"><small>{t["developer"]}</small>{esc(APP["developer"])}</div>'
        f'<div class="fact"><small>{t["package"]}</small>{esc(APP["package_id"])}</div>'
        f'</div></section>'
        f'<section class="section end"><h2>{t["download"]}</h2>'
        f'<p>{esc(APP["tagline"][lang])}</p>'
        f'<a class="btn" href="{esc(APP["google_play_url"])}" target="_blank" '
        f'rel="noopener noreferrer" data-analytics-event="google_play_click" '
        f'data-cta-location="download_end">{t["cta"]}</a></section>'
    )

def render_content(lang, section):
    t = TEXT[lang]
    if section == "home":
        image = SCREENSHOTS[0]["src"]
        return (
            f'<section class="hero"><div><div class="tag">{t["tag"]}</div>'
            f'<h1>{esc(t["home"])}</h1><p class="lead">{esc(t["home_intro"])}</p>'
            f'<a class="btn" href="{esc(APP["google_play_url"])}" '
            f'data-analytics-event="google_play_click" data-cta-location="home_hero">{t["cta"]}</a></div>'
            f'<div class="preview"><img src="{image}" width="526" height="296" alt="{esc(SCREENSHOTS[0]["alt"][lang])}" loading="eager" fetchpriority="high" decoding="async"></div></section>'
            f'{render_gallery(lang)}'
            f'<section class="section"><h2>{t["features"]}</h2>{render_features(lang)}'
            f'<p><a href="{page_url(lang, "features")}">{t["features"]}</a></p></section>'
        )
    if section == "about":
        return (
            f'<section class="section"><div class="tag">PALACE MATCH</div>'
            f'<h1>{t["about"]}</h1><p class="lead">{esc(APP["description"][lang])}</p>'
            f'<p>{esc(t["about_intro"])}</p>'
            f'<p><strong>{esc(APP["developer"])}</strong></p>'
            f'<p><a class="btn" href="{esc(APP["google_play_url"])}" '
            f'data-analytics-event="google_play_click" data-cta-location="about_intro">{t["cta"]}</a></p></section>'
        )
    if section == "features":
        return (
            f'<section class="section"><div class="tag">PALACE MATCH · ANDROID</div>'
            f'<h1>{t["features"]}</h1><p class="lead">{t["features_intro"]}</p>'
            f'{render_features(lang)}'
            f'<section class="section end"><h2>{t["download"]}</h2>'
            f'<p>{esc(APP["tagline"][lang])}</p>'
            f'<a class="btn" href="{esc(APP["google_play_url"])}" '
            f'data-analytics-event="google_play_click" data-cta-location="features_end">{t["cta"]}</a></section></section>'
        )
    if section == "download":
        return render_download(lang)
    if section == "faq":
        return (
            f'<section class="section"><div class="tag">PALACE MATCH</div>'
            f'<h1>{t["faq"]}</h1><p class="lead">{t["faq_intro"]}</p>'
            f'{render_faq(lang)}</section>'
            f'<section class="section end"><h2>{t["download"]}</h2>'
            f'<p>{esc(APP["tagline"][lang])}</p>'
            f'<a class="btn" href="{esc(APP["google_play_url"])}" target="_blank" rel="noopener noreferrer" '
            f'data-analytics-event="google_play_click" data-cta-location="faq_end">{t["cta"]}</a></section>'
        )
    raise ValueError(f"Unknown page section: {section}")

def render_page(lang, section):
    t = TEXT[lang]
    direction = "rtl" if lang == "ar" else "ltr"
    canonical = page_url(lang, section)
    description = PAGE_DESCRIPTIONS[lang][section]
    other = "ar" if lang == "en" else "en"
    organization = {
        "@type": "Organization", "@id": f"{BASE_URL}/#organization",
        "name": APP["developer"], "url": BASE_URL + "/", "email": APP["support_email"],
    }
    software = {
        "@type": "SoftwareApplication", "@id": f"{BASE_URL}/#softwareapplication",
        "name": APP["name"], "operatingSystem": "Android",
        "applicationCategory": "GameApplication",
        "description": APP["description"][lang],
        "downloadUrl": APP["google_play_url"], "installUrl": APP["google_play_url"],
        "url": canonical, "image": SCREENSHOTS[0]["src"],
        "author": {"@id": f"{BASE_URL}/#organization"},
    }
    graph = [organization, software]
    if section == "faq":
        graph.append({
            "@type": "FAQPage", "@id": canonical + "#faq", "url": canonical, "inLanguage": lang,
            "mainEntity": [
                {"@type": "Question", "name": item["q"][lang],
                 "acceptedAnswer": {"@type": "Answer", "text": item["a"][lang]}}
                for item in FAQ
            ],
        })
    schema = {"@context": "https://schema.org", "@graph": graph}
    content = render_content(lang, section)
    return f'''<!doctype html>
<html lang="{lang}" dir="{direction}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(PAGE_TITLES[lang][section])}</title>
<meta name="description" content="{esc(description)}">
<meta name="robots" content="index,follow,max-image-preview:large">
<meta name="theme-color" content="#080b12">
<link rel="canonical" href="{canonical}">
<link rel="alternate" hreflang="en" href="{page_url("en", section)}">
<link rel="alternate" hreflang="ar" href="{page_url("ar", section)}">
<link rel="alternate" hreflang="x-default" href="{page_url("en", section)}">
<meta property="og:locale" content="{"ar" if lang == "ar" else "en_US"}">
<meta property="og:image" content="{esc(SCREENSHOTS[0]["src"])}">
<meta property="og:image:alt" content="{esc(SCREENSHOTS[0]["alt"][lang])}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(PAGE_TITLES[lang][section])}">
<meta name="twitter:description" content="{esc(description)}">
<meta name="twitter:image" content="{esc(SCREENSHOTS[0]["src"])}">
<meta property="og:type" content="website">
<meta property="og:title" content="{esc(PAGE_TITLES[lang][section])}">
<meta property="og:description" content="{esc(description)}">
<meta property="og:url" content="{canonical}">
<link rel="preconnect" href="https://play-lh.googleusercontent.com" crossorigin>
<link rel="preconnect" href="https://www.googletagmanager.com" crossorigin>
<link rel="stylesheet" href="{BASE_URL}/assets/style.css">
<script type="application/ld+json">{json.dumps(schema, ensure_ascii=False)}</script>
{render_analytics()}
</head>
<body data-page-section="{section}">
<a class="skip-link" href="#main-content">{t["skip_to_content"]}</a>
{render_header(lang, section)}
<main id="main-content">{content}</main>
<footer><span>© DevImpact · PALACE MATCH</span>
<span><a href="{esc(APP["privacy_policy_url"])}">{t["privacy"]}</a> ·
<a href="mailto:{esc(APP["support_email"])}">{t["support"]}</a></span></footer>
</body>
</html>'''

def render_language_root():
    target = f"{BASE_URL}/en-us/about/"
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="google-site-verification" content="8mOiNMu4Tn477yFaR-IWrNQGhdqH1TpF6NKKoN94Oms">
<meta name="robots" content="noindex,follow">
<title>Palace Match</title>
<link rel="canonical" href="{target}">
<meta http-equiv="refresh" content="0; url={target}">
<script>window.location.replace("{target}");</script>
</head>
<body><p><a href="{target}">Continue to Palace Match</a></p></body>
</html>'''

def write(relative_path, content):
    target = DIST / relative_path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")

def main():
    if DIST.exists():
        shutil.rmtree(DIST)
    write(pathlib.Path("assets/style.css"), CSS)
    shutil.copytree(ROOT / "assets/screens", DIST / "assets/screens")
    write(pathlib.Path("index.html"), render_language_root())
    for lang in ("en", "ar"):
        for section in ("home", "about", "features", "download", "faq"):
            relative = pathlib.Path(lang) / ("" if section == "home" else section) / "index.html"
            write(relative, render_page(lang, section))
    write(pathlib.Path("robots.txt"), f"User-agent: *\nAllow: /\n\nSitemap: {BASE_URL}/sitemap.xml\nSitemap: {BASE_URL}/sitemap.txt\n")
    sitemap_entries = []
    sitemap_entries.extend(
        (page_url(lang, section), lang, section)
        for lang in ("en", "ar")
        for section in ("home", "about", "features", "download", "faq")
    )
    sitemap = '<?xml version="1.0" encoding="UTF-8"?>'
    sitemap += (
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
        'xmlns:xhtml="http://www.w3.org/1999/xhtml">'
    )
    for url, lang, section in sitemap_entries:
        english_url = page_url("en", section)
        arabic_url = page_url("ar", section)
        default_url = english_url
        sitemap += f"<url><loc>{esc(url)}</loc>"
        sitemap += f'<xhtml:link rel="alternate" hreflang="en" href="{esc(english_url)}"/>'
        sitemap += f'<xhtml:link rel="alternate" hreflang="ar" href="{esc(arabic_url)}"/>'
        sitemap += f'<xhtml:link rel="alternate" hreflang="x-default" href="{esc(default_url)}"/>'
        sitemap += "</url>"
    sitemap += "</urlset>"
    write(pathlib.Path("sitemap.xml"), sitemap)
    sitemap_txt = "\n".join(url for url, _, _ in sitemap_entries) + "\n"
    write(pathlib.Path("sitemap.txt"), sitemap_txt)
    write(pathlib.Path("llms.txt"), (
        f"# Palace Match\n\n{APP['description']['en']}\n\n"
        f"- Google Play: {APP['google_play_url']}\n"
        f"- English: {page_url('en')}\n- Arabic: {page_url('ar')}\n"
    ))


    from build_resources import build_extra_pages
    build_extra_pages()
    from build_locales import build_localized_pages
    build_localized_pages()
    from build_locale_resources import build_localized_resource_pages
    build_localized_resource_pages()

if __name__ == "__main__":
    main()
