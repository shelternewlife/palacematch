#!/usr/bin/env python3
"""Generate the four game-resource hub routes for every published market locale."""
import html
import json
import pathlib
import xml.etree.ElementTree as ET

ROOT = pathlib.Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
APP = json.loads((ROOT / "content/app.json").read_text(encoding="utf-8"))
STRATEGY = json.loads((ROOT / "content/market-strategy.json").read_text(encoding="utf-8"))
BASE = APP["website_url"].rstrip("/")
NS = "http://www.sitemaps.org/schemas/sitemap/0.9"
XHTML = "http://www.w3.org/1999/xhtml"
HUBS = ("tips", "blog", "guide", "comparison")
EXTRA_CONTENT = json.loads((ROOT / "content/resource-locales.json").read_text(encoding="utf-8"))

CONTENT = {
    "en-US": {
        "language_name": "US English",
        "nav": {"tips": "Tips", "blog": "Blog", "guide": "User guide", "comparison": "Compare"},
        "pages": {
            "tips": ("Fruit Puzzle Tips | Palace Match", "Practical fruit-puzzle tips for reviewing fruit matches, checking listings and organizing your next steps.", "Job search tips", "Build a focused search, verify the original listing and use app indicators as context—not guarantees.", [
                ("Set a focused search", "Choose relevant roles and priorities so you can assess fruit matches consistently.", "guide"),
                ("Verify every listing", "Check the employer, requirements, location and application instructions at the original source.", "blog"),
                ("Use indicators carefully", "Treat freshness, match and competition signals as supporting information, not promises.", "comparison")]),
            "blog": ("Fruit Puzzle Blog & Career Resources | Palace Match", "Career resources from Palace Match: practical tips, a user guide and a clear workflow comparison.", "Palace Match game resources", "Explore practical resources to make your fruit puzzle more organized, informed and careful.", [
                ("Job search tips", "Practical habits for evaluating fruit matches and protecting your time and information.", "tips"),
                ("User guide", "A concise walkthrough of discovering, reviewing and organizing fruit matches with Palace Match.", "guide"),
                ("Compare workflows", "Understand how an fruit match-discovery app fits alongside traditional fruit-puzzle methods.", "comparison")]),
            "guide": ("Palace Match User Guide | Fruit Puzzle App", "Learn how to explore fruit matches, review role context and organize levels with Palace Match.", "Palace Match user guide", "Follow a simple workflow for discovering fruit matches, reviewing details and keeping track of roles.", [
                ("Discover fruit matches", "Explore the discovery experience and decide which roles deserve a closer look.", "tips"),
                ("Review role details", "Read responsibilities and requirements, and verify important details with the employer.", "blog"),
                ("Organize your search", "Use personal collections to group fruit matches you want to revisit.", "comparison")]),
            "comparison": ("Fruit Puzzle Workflow Comparison | Palace Match", "A qualitative comparison of app-based fruit match discovery and traditional fruit-puzzle routines.", "Compare fruit-puzzle workflows", "See where an fruit match-discovery app can help—and what still requires independent verification.", [
                ("Finding fruit matches", "A dedicated discovery view can reduce the need to revisit scattered sources manually.", "guide"),
                ("Reviewing context", "App indicators add context, while the original employer listing remains the source to verify.", "tips"),
                ("Organizing roles", "Personal collections can keep fruit matches together for later review and follow-up.", "blog")])
        }
    },
    "en-CA": {
        "language_name": "English (Canada)",
        "nav": {"tips": "Tips", "blog": "Blog", "guide": "User guide", "comparison": "Compare"},
        "pages": {
            "tips": ("Fruit Puzzle Tips | Palace Match", "Practical fruit-puzzle tips for reviewing fruit matches, checking fruit pieces and organizing next steps.", "Job search tips", "Build a focused search, verify the original fruit piece and use app indicators as context—not guarantees.", [
                ("Set a focused search", "Choose relevant roles and priorities so you can assess fruit matches consistently.", "guide"),
                ("Verify every posting", "Check the employer, requirements, location and application instructions at the original source.", "blog"),
                ("Use indicators carefully", "Treat freshness, match and competition signals as supporting information, not promises.", "comparison")]),
            "blog": ("Fruit Puzzle Blog & Career Resources | Palace Match", "Career resources from Palace Match: practical tips, a user guide and a clear workflow comparison.", "Palace Match game resources", "Explore practical resources to make your fruit puzzle more organized, informed and careful.", [
                ("Job search tips", "Practical habits for evaluating fruit matches and protecting your time and information.", "tips"),
                ("User guide", "A concise walkthrough of discovering, reviewing and organizing fruit matches with Palace Match.", "guide"),
                ("Compare workflows", "Understand how an fruit match-discovery app fits alongside traditional fruit-puzzle methods.", "comparison")]),
            "guide": ("Palace Match User Guide | Fruit Puzzle App", "Learn how to explore fruit matches, review role context and organize levels with Palace Match.", "Palace Match user guide", "Follow a simple workflow for discovering fruit matches, reviewing details and keeping track of roles.", [
                ("Discover fruit matches", "Explore the discovery experience and decide which roles deserve a closer look.", "tips"),
                ("Review puzzle details", "Read responsibilities and requirements, and verify important details with the employer.", "blog"),
                ("Organize your search", "Use personal collections to group fruit matches you want to revisit.", "comparison")]),
            "comparison": ("Fruit Puzzle Workflow Comparison | Palace Match", "A qualitative comparison of app-based fruit match discovery and traditional fruit-puzzle routines.", "Compare fruit-puzzle workflows", "See where an fruit match-discovery app can help—and what still requires independent verification.", [
                ("Finding fruit matches", "A dedicated discovery view can reduce the need to revisit scattered sources manually.", "guide"),
                ("Reviewing context", "App indicators add context, while the original employer posting remains the source to verify.", "tips"),
                ("Organizing roles", "Personal collections can keep fruit matches together for later review and follow-up.", "blog")])
        }
    },
    "fr-CA": {
        "language_name": "Français (Canada)",
        "nav": {"tips": "Conseils", "blog": "Blogue", "guide": "Guide", "comparison": "Comparer"},
        "pages": {
            "tips": ("Conseils sur les puzzles de fruits | Palace Match", "Des conseils pratiques pour associer les fruits, créer des combos et progresser dans les niveaux du palais.", "Conseils sur les puzzles de fruits", "Échangez les fruits voisins, associez-en trois ou plus et observez les cascades pour préparer votre prochain coup.", [
                ("Ciblez votre recherche", "Repérez les associations possibles sur le plateau et choisissez les coups qui peuvent déclencher de nouvelles cascades.", "guide"),
                ("Créez des combos", "Enchaînez les associations pour augmenter votre score et dégager davantage de cases.", "blog"),
                ("Progressez à chaque partie", "Gagnez des pièces et des XP au fil des parties pour avancer dans les niveaux du palais.", "comparison")]),
            "blog": ("Blogue Palace Match : puzzles de fruits | Palace Match", "Des ressources Palace Match : conseils de jeu, guide des fonctionnalités et explications des modes.", "Ressources jeu Palace Match", "Découvrez des conseils pour les puzzles de fruits, les combos et la progression dans Palace Match.", [
                ("Conseils de jeu de puzzle fruité", "Des habitudes utiles pour évaluer les possibilités et protéger votre temps et vos renseignements.", "tips"),
                ("Guide d’utilisation", "Un parcours simple pour découvrir, examiner et organiser les possibilités avec Palace Match.", "guide"),
                ("Comparer les méthodes", "Comprenez comment une application de découverte complète les méthodes traditionnelles de recherche.", "comparison")]),
            "guide": ("Guide Palace Match : jouer et progresser | Android", "Apprenez à associer des fruits, déclencher des cascades, gagner des pièces et progresser avec Palace Match.", "Guide d’utilisation de Palace Match", "Suivez un parcours simple pour maîtriser les associations de fruits, les combos et les modes de jeu.", [
                ("Découvrir des possibilités", "Explorez l’écran de découverte et repérez les postes qui méritent un examen plus approfondi.", "tips"),
                ("Examiner les détails", "Lisez les responsabilités et les exigences, puis vérifiez les renseignements importants auprès de l’employeur.", "blog"),
                ("Organiser votre recherche", "Utilisez les collections personnelles pour regrouper les possibilités à consulter de nouveau.", "comparison")]),
            "comparison": ("Comparer les modes de jeu Palace Match | Puzzle de fruits", "Découvrez les différences entre les parties à coups limités et le mode sans fin de Palace Match.", "Comparer les méthodes de jeu de puzzle fruité", "Choisissez le mode qui convient à votre rythme : défi à coups limités ou associations sans fin.", [
                ("Repérer des possibilités", "Un fil de découverte dédié peut réduire les recherches manuelles sur plusieurs sources.", "guide"),
                ("Examiner le contexte", "Les indicateurs ajoutent du contexte, mais l’offre originale de l’employeur reste la source à vérifier.", "tips"),
                ("Organiser les postes", "Les collections personnelles regroupent les possibilités à consulter et à suivre plus tard.", "blog")])
        }
    }
}
CONTENT.update(EXTRA_CONTENT)

FLAG_DATA = {
    "en-US": ("us", "United States", "United States · English"),
    "en-CA": ("ca", "Canada", "Canada · English"),
    "fr-CA": ("ca", "Canada", "Canada · Français"),
    "es-ES": ("es", "Spain", "España · Español"),
    "pt-PT": ("pt", "Portugal", "Portugal · Português"),
    "fr-FR": ("fr", "France", "France · Français"),
    "de-DE": ("de", "Germany", "Deutschland · Deutsch"),
    "it-IT": ("it", "Italy", "Italia · Italiano"),
}
NAV_GROUPS = {
    "en-US": ("Explore", "Resources"), "en-CA": ("Explore", "Resources"),
    "fr-CA": ("Explorer", "Ressources"), "es-ES": ("Explorar", "Recursos"),
    "pt-PT": ("Explorar", "Recursos"), "fr-FR": ("Explorer", "Ressources"),
    "de-DE": ("Entdecken", "Ressourcen"), "it-IT": ("Esplora", "Risorse"),
}
LOCALE_TEXT = json.loads((ROOT / "content/locales.json").read_text(encoding="utf-8"))

def render_locale_flags(locale, tail):
    links = []
    for code in STRATEGY["published_locales"]:
        country, country_name, label = FLAG_DATA[code]
        current = ' aria-current="page"' if code == locale else ""
        flag_url = f"https://flagcdn.com/w80/{country}.png"
        links.append(
            f'<a class="locale-flag" lang="{code}" href="{route(code, tail)}" '
            f'title="{esc(label)}" aria-label="{esc(label)}"{current}>'
            f'<img src="{flag_url}" alt="{esc(country_name)} flag" width="40" height="30" loading="eager" decoding="async"></a>'
        )
    import build
    return '<div class="locale-switch" aria-label="Country and region">' + "".join(links) + build.render_social_links() + '</div>'

def esc(value):
    return html.escape(str(value), quote=True)

def route(locale, tail):
    return f"{BASE}/{locale.lower()}/{tail}/"

def render_page(locale, tail, data):
    language = locale.split("-", 1)[0]
    labels = CONTENT[locale].get("labels", {
        "features": "Fonctionnalités" if language == "fr" else "Features",
        "more": "En savoir plus" if language == "fr" else "Explore this resource",
        "skip": "Passer au contenu principal" if language == "fr" else "Skip to main content",
        "resource": "RESSOURCES DE JEU" if language == "fr" else "FRUIT PUZZLE RESOURCES",
        "home": "Retour à l’accueil" if language == "fr" else "Back to the home page",
        "privacy": "Politique de confidentialité" if language == "fr" else "Privacy policy",
        "support": "Soutien" if language == "fr" else "Support",
        "nav_aria": "Navigation principale" if language == "fr" else "Primary navigation"
    })
    title, description, heading, intro, cards = data
    slug = locale.lower()
    alternates = "".join(
        f'<link rel="alternate" hreflang="{code}" href="{route(code, tail)}">\n'
        for code in STRATEGY["published_locales"]
    )
    alternates += f'<link rel="alternate" hreflang="x-default" href="{route("en-US", tail)}">'
    nav_groups = NAV_GROUPS[locale]
    primary_text = LOCALE_TEXT.get(locale, {}).get("text", {})
    primary_items = (
        ("about", primary_text.get("about", "About")),
        ("features", primary_text.get("features", labels["features"])),
        ("download", primary_text.get("download_nav", "Download")),
        ("faq", primary_text.get("faq", "FAQ")),
    )
    primary_links = "".join(
        f'<a data-nav-item="{key}" href="{BASE}/{slug}/{key}/">{esc(label)}</a>'
        for key, label in primary_items
    )
    resource_links = "".join(
        f'<a data-nav-item="{item}" href="{route(locale, item)}">{esc(CONTENT[locale]["nav"][item])}</a>'
        for item in ("tips", "blog", "guide", "comparison")
    )
    nav = (
        f'<details class="nav-menu" data-nav-group="primary"><summary>{esc(nav_groups[0])}</summary>'
        f'<div class="nav-dropdown">{primary_links}</div></details>'
        f'<details class="nav-menu" data-nav-group="resources"><summary>{esc(nav_groups[1])}</summary>'
        f'<div class="nav-dropdown">{resource_links}</div></details>'
    )
    cards_html = "".join(
        f'<article class="item"><h2><a href="{route(locale, target)}">{esc(card_title)}</a></h2>'
        f'<p>{esc(card_text)}</p><a href="{route(locale, target)}">'
        f'{esc(labels["more"])}</a></article>'
        for card_title, card_text, target in cards
    )
    locale_links = " · ".join(
        f'<a lang="{code}" href="{route(code, tail)}">{esc(CONTENT[code]["language_name"])}</a>'
        for code in STRATEGY["published_locales"] if code != locale
    )
    schema = {
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "name": title,
        "description": description,
        "inLanguage": locale,
        "url": route(locale, tail),
        "publisher": {"@type": "Organization", "name": APP["developer"], "url": BASE + "/"}
    }
    return f'''<!doctype html>
<html lang="{esc(locale)}" dir="ltr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(description)}">
<meta name="robots" content="index,follow,max-image-preview:large">
<link rel="canonical" href="{route(locale, tail)}">
{alternates}
<meta property="og:type" content="website">
<meta property="og:locale" content="{"fr_CA" if locale == "fr-CA" else locale.replace("-", "_")}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(description)}">
<meta property="og:url" content="{route(locale, tail)}">
<link rel="stylesheet" href="{BASE}/assets/style.css">
<script type="application/ld+json">{json.dumps(schema, ensure_ascii=False)}</script>
</head>
<body data-page-section="{tail}">
<a class="skip-link" href="#main-content">{esc(labels["skip"])}</a>
<header class="standard-header"><div class="header-main">{render_locale_flags(locale, tail)}<a class="brand" href="{BASE}/{slug}/">PALACE <b>MATCH</b></a>
<nav aria-label="{esc(labels["nav_aria"])}">{nav}</nav></div></header>
<main id="main-content"><section class="section resource-hub">
<div class="tag">PALACE MATCH · {esc(labels["resource"])}</div>
<h1>{esc(heading)}</h1><p class="lead">{esc(intro)}</p>
<div class="grid">{cards_html}</div>
<p class="locale-links">{locale_links}</p>
<p><a href="{BASE}/{slug}/">{esc(labels["home"])}</a></p>
</section></main>
<footer><span>© DevImpact · PALACE MATCH</span><span><a href="{esc(APP["privacy_policy_url"])}">{esc(labels["privacy"])}</a> · <a href="mailto:{esc(APP["support_email"])}">{esc(labels["support"])}</a></span></footer>
</body>
</html>'''

def build_localized_resource_pages():
    published = STRATEGY.get("published_locales", [])
    if set(published) != set(CONTENT):
        raise ValueError("Localized resource content must exist for every published locale")
    css = DIST / "assets/style.css"
    css.write_text(
        css.read_text(encoding="utf-8")
        + "\n.resource-hub{max-width:1000px}.resource-hub h1{font-size:clamp(2.2rem,5vw,3.6rem);line-height:1.15}.resource-hub .grid{margin-top:28px}.resource-hub .item h2{font-size:1.3rem}.locale-links{margin-top:30px;color:#aab6c8}\n",
        encoding="utf-8"
    )
    for locale in published:
        for tail in HUBS:
            target = DIST / locale.lower() / tail / "index.html"
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(render_page(locale, tail, CONTENT[locale]["pages"][tail]), encoding="utf-8")

    sitemap_path = DIST / "sitemap.xml"
    tree = ET.parse(sitemap_path)
    root = tree.getroot()
    ET.register_namespace("", NS)
    ET.register_namespace("xhtml", XHTML)
    existing = {
        node.findtext(f"{{{NS}}}loc")
        for node in root.findall(f"{{{NS}}}url")
    }
    for locale in published:
        for tail in HUBS:
            loc = route(locale, tail)
            if loc in existing:
                continue
            node = ET.SubElement(root, f"{{{NS}}}url")
            ET.SubElement(node, f"{{{NS}}}loc").text = loc
            for alternate_locale in published:
                ET.SubElement(node, f"{{{XHTML}}}link", {
                    "rel": "alternate", "hreflang": alternate_locale,
                    "href": route(alternate_locale, tail)
                })
            ET.SubElement(node, f"{{{XHTML}}}link", {
                "rel": "alternate", "hreflang": "x-default",
                "href": route("en-US", tail)
            })
    tree.write(sitemap_path, encoding="utf-8", xml_declaration=True)

    text_path = DIST / "sitemap.txt"
    urls = [line.strip() for line in text_path.read_text(encoding="utf-8").splitlines() if line.strip()]
    for locale in published:
        for tail in HUBS:
            loc = route(locale, tail)
            if loc not in urls:
                urls.append(loc)
    text_path.write_text("\n".join(urls) + "\n", encoding="utf-8")

    llms_path = DIST / "llms.txt"
    llms = llms_path.read_text(encoding="utf-8")
    llms += "\n## Localized game resources\n"
    for locale in published:
        for tail in HUBS:
            llms += f"- {locale} {tail}: {route(locale, tail)}\n"
    llms_path.write_text(llms, encoding="utf-8")

if __name__ == "__main__":
    build_localized_resource_pages()
