"""Build the published site from the bilingual sources in src/.

Why: Google indexes one language per URL. The sources keep both languages side
by side (<x lang="es">…</x><x lang="en">…</x>); this script writes one page per
language with a single <h1>, the right <html lang>, a complete <head> (title,
description, canonical, hreflang, Open Graph, Twitter card, JSON-LD) and
language-aware internal links:

    src/index.html            -> index.html            (EN, x-default)   es/index.html            (ES)
    src/proyectos/<slug>.html -> proyectos/<slug>.html (EN)              es/proyectos/<slug>.html (ES)

It also writes sitemap.xml, robots.txt and llms.txt.

Source conventions
- Elements with lang="es"/lang="en" are kept only in that language's page
  (the attribute is removed). Works for any tag, including <img> (one per language).
- Per-language attributes: foo-es="…" foo-en="…" become foo="…".
- Internal links are normalised to root-relative URLs (/assets/…, /proyectos/…,
  /es/…). External, mailto: and #anchor links are untouched.
- <!--LANGSWITCH--> marks where the ES/EN link switcher goes.
- Elements with data-cv get the CV of the page language.

Run:  python3 tools/build_site.py        (stdlib only; Python 3.9+)
Then: python3 tools/build_og.py           (optional, needs Pillow: Open Graph images)
"""
from __future__ import annotations

import json
import posixpath
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_cases  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"

SITE = "https://pablodpavon.com"
LANGS = ("en", "es")
DEFAULT = "en"                     # served at the root and used as x-default
UPDATED = "2026-10-21"             # dateModified / lastmod for this build
PERSON_ID = SITE + "/#person"
WEBSITE_ID = SITE + "/#website"
NAME = "Pablo Pavon"
JOB_TITLE = "Senior Business & Data Analyst"
EMAIL = "contact@pablodpavon.com"
LINKEDIN = "https://www.linkedin.com/in/pablo-damian-pavon"
GITHUB = "https://github.com/pablodpavon"
UPWORK = "https://www.upwork.com/freelancers/pablopavon"
OG_LOCALE = {"en": "en_US", "es": "es_AR"}

VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta",
        "source", "track", "wbr"}
URL_ATTRS = {"href", "src", "data-zoom-src", "poster"}

# ------------------------------------------------------------------ page metadata
HOME = {
    "title": {
        "en": "Pablo Pavon · Freelance Data & Business Analyst in Berlin",
        "es": "Pablo Pavon · Analista de datos y procesos freelance · Berlín",
    },
    "description": {
        "en": "Freelance Senior Business & Data Analyst in Berlin, from Argentina. Power BI dashboards, data migration, finance automation, AI reporting: numbers verified.",
        "es": "Analista de datos y procesos freelance en Berlín, argentino. Conciliación bancaria y caja automáticas, control de facturas, Power BI y reportes con IA.",
    },
    "image_alt": {
        "en": "Pablo Pavon, freelance Senior Business & Data Analyst in Berlin: dashboards, data migration, finance automation",
        "es": "Pablo Pavon, Senior Business & Data Analyst freelance en Berlín: dashboards, migraciones, automatización financiera",
    },
    "published": "2026-10-13",
}

PERSON_DESCRIPTION = {
    "en": "Pablo Pavon is a freelance Senior Business & Data Analyst based in Berlin, Germany, originally from Argentina. "
          "He works remotely with small and mid-sized companies, accounting firms and corporate teams in Argentina, "
          "Latin America, Europe and the United States, in English, Spanish and German. He specialises in Power BI and "
          "SQL dashboards, data migration with reconciliation, finance automation (bank reconciliation, supplier invoice "
          "control, cash forecasting) and AI-assisted reporting where every number is verified before release. "
          "Background: banking, e-commerce, marketing analytics and insurance; 10+ years of experience.",
    "es": "Pablo Pavon es Senior Business & Data Analyst freelance con base en Berlín, Alemania, y origen argentino. "
          "Trabaja en remoto con pymes, estudios contables y equipos corporativos de Argentina, América Latina, Europa y "
          "Estados Unidos, en español, inglés y alemán. Se especializa en dashboards en Power BI y SQL, migraciones de "
          "datos con conciliación, automatización financiera (conciliación bancaria, control de facturas de proveedores, "
          "caja proyectada) y reportes asistidos por IA en los que cada número se verifica antes de publicarse. "
          "Experiencia en banca, e-commerce, analítica de marketing y seguros; más de 10 años.",
}

SERVICES = [  # (en name, es name, en description, es description, anchor)
    ("Dashboards & BI", "Dashboards y BI",
     "Power BI, Tableau or web dashboards that replace manual reports: defined KPIs, meaningful filters, one version of the numbers.",
     "Tableros en Power BI, Tableau o web que reemplazan reportes manuales: KPIs definidos, filtros con sentido y una sola versión de los números.",
     "#servicios"),
    ("Finance automation", "Automatización financiera",
     "Bank reconciliation, supplier invoice control, collections and cash forecasting that update themselves every morning, for SMEs and accounting firms.",
     "Conciliación bancaria, control de facturas de proveedores, cobranzas y caja proyectada que se actualizan solos cada mañana, para pymes y estudios contables.",
     "#automatizacion-financiera"),
    ("AI applied to processes", "IA aplicada a procesos",
     "Reports and repetitive work automated with AI, with checks that verify every figure before anyone reads it.",
     "Reportes y tareas repetitivas automatizados con IA, con controles que verifican cada cifra antes de que alguien la lea.",
     "#servicios"),
    ("Data analysis", "Análisis de datos",
     "SQL and Python to answer concrete business questions, with assumptions and limits stated.",
     "SQL y Python para responder preguntas concretas del negocio, con supuestos y limitaciones a la vista.",
     "#servicios"),
    ("Requirements & processes", "Requerimientos y procesos",
     "Discovery, user stories with acceptance criteria, functional specs and process maps that IT can build without guessing.",
     "Relevamiento, user stories con criterios de aceptación, especificaciones funcionales y mapeo de procesos.",
     "#servicios"),
    ("Pricing & customer analytics", "Pricing y analítica de clientes",
     "Pricing by market and channel, elasticity, cohorts, RFM segmentation, churn and customer lifetime value.",
     "Precios por mercado y canal, elasticidad, cohortes, segmentación RFM, churn y valor de vida del cliente.",
     "#servicios"),
    ("Data migration & quality", "Migración y calidad de datos",
     "Data mapping for system changes, cleansing, deduplication and reconciliations that prove nothing was lost; operational GDPR data management.",
     "Mapeo de datos para cambios de sistema, limpieza, deduplicación y conciliaciones que prueban que no se perdió nada; gestión operativa de datos personales (GDPR).",
     "#servicios"),
]

KNOWS_ABOUT = ["Business analysis", "Data analysis", "Power BI", "Tableau", "Looker Studio", "SQL", "Python", "pandas",
               "Data migration", "Data quality", "Bank reconciliation", "Accounts payable control", "Cash flow forecasting",
               "Pricing analytics", "Customer analytics", "Cohort analysis", "RFM segmentation", "Customer churn",
               "Requirements engineering", "User stories", "GDPR", "AI-assisted reporting"]

AREA_SERVED = ["Germany", "European Union", "Argentina", "Latin America", "United States"]

UI = {
    "en": {"home": "Home", "work": "Work", "switch_label": "Language"},
    "es": {"home": "Inicio", "work": "Proyectos", "switch_label": "Idioma"},
}


# ------------------------------------------------------------------ URL helpers
def lang_root(lang: str) -> str:
    return "/" if lang == DEFAULT else f"/{lang}/"


def page_url(rel: str, lang: str) -> str:
    """rel is the source path relative to src/, e.g. 'index.html' or 'proyectos/x.html'."""
    root = lang_root(lang)
    return SITE + (root if rel == "index.html" else root + rel)


def out_path(rel: str, lang: str) -> Path:
    return ROOT / rel if lang == DEFAULT else ROOT / lang / rel


def rewrite_url(url: str, src_dir: str, lang: str) -> str:
    if not url or re.match(r"^(?:[a-zA-Z][a-zA-Z0-9+.-]*:|#|//)", url):
        return url  # external, mailto:, data:, anchors
    path, _, frag = url.partition("#")
    norm = posixpath.normpath(posixpath.join(src_dir, path)) if path else ""
    if norm.startswith("assets/") or norm in ("favicon.svg", "favicon.ico", "apple-touch-icon.png", "sitemap.xml", "llms.txt"):
        new = "/" + norm
    elif norm in ("index.html", ".", ""):
        new = lang_root(lang)
    else:
        new = lang_root(lang) + norm
    return new + (f"#{frag}" if frag else "")


# ------------------------------------------------------------------ start-tag rewriting
ATTR_RE = re.compile(r"""([^\s"'=<>`/]+)(?:\s*=\s*(?:"([^"]*)"|'([^']*)'|([^\s"'=<>`]+)))?""")


def rewrite_start_tag(raw: str, lang: str, src_dir: str) -> str:
    """Rewrite attributes on the raw start-tag text; preserves tag/attribute case and order."""
    m = re.match(r"<([^\s/>]+)", raw)
    tag = m.group(1)
    body = raw[m.end():]
    selfclosing = body.rstrip().endswith("/>")
    body = body.rstrip()[:-2] if selfclosing else body.rstrip()[:-1]
    attrs = []
    for am in ATTR_RE.finditer(body):
        name = am.group(1)
        val = am.group(2) if am.group(2) is not None else am.group(3) if am.group(3) is not None else am.group(4)
        attrs.append([name, val])
    out = []
    lname = tag.lower()
    for name, val in attrs:
        lower = name.lower()
        if lower == "lang":
            if lname == "html":
                out.append(["lang", lang])
            continue  # single-language page: the attribute is redundant
        if lower.endswith(("-es", "-en")) and lower not in ("data-es", "data-en"):
            if lower.endswith("-" + lang):
                out.append([name[:-3], val])
            continue
        if lower in URL_ATTRS and val is not None:
            val = rewrite_url(val, src_dir, lang)
        if lower == "data-base":
            val = "/"
        out.append([name, val])
    if any(n.lower() == "data-cv" for n, _ in out):
        for a in out:
            if a[0].lower() == "href":
                a[1] = f"/assets/CV_Pablo_Pavon_{lang.upper()}.pdf"
    parts = [tag] + [n if v is None else f'{n}="{v}"' for n, v in out]
    return "<" + " ".join(parts) + ("/>" if selfclosing else ">")


class Splitter(HTMLParser):
    """Re-emits an HTML document verbatim, keeping only one language."""

    def __init__(self, lang: str, src_dir: str):
        super().__init__(convert_charrefs=False)
        self.lang, self.src_dir = lang, src_dir
        self.out: list[str] = []
        self.skip = 0           # nesting depth inside an element of the other language
        self.stack: list[str] = []  # open tags (original case) for well-formedness + end-tag case

    # -- tags
    def handle_starttag(self, tag, attrs):
        raw = self.get_starttag_text()
        if self.skip:
            if tag not in VOID:
                self.skip += 1
            return
        lang = dict(attrs).get("lang")
        if lang and lang != self.lang and tag != "html":
            if tag not in VOID:
                self.skip = 1
            return
        if tag not in VOID:
            self.stack.append(re.match(r"<([^\s/>]+)", raw).group(1))
        self.out.append(rewrite_start_tag(raw, self.lang, self.src_dir))

    def handle_startendtag(self, tag, attrs):  # <x … />
        if self.skip:
            return
        lang = dict(attrs).get("lang")
        if lang and lang != self.lang:
            return
        self.out.append(rewrite_start_tag(self.get_starttag_text(), self.lang, self.src_dir))

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        if self.skip:
            self.skip -= 1
            return
        if not self.stack or self.stack[-1].lower() != tag:
            raise SystemExit(f"unbalanced </{tag}> at line {self.getpos()[0]} (open: {self.stack[-3:]})")
        self.out.append(f"</{self.stack.pop()}>")

    # -- everything else, verbatim
    def handle_data(self, data):
        if not self.skip:
            self.out.append(data)

    def handle_entityref(self, name):
        if not self.skip:
            self.out.append(f"&{name};")

    def handle_charref(self, name):
        if not self.skip:
            self.out.append(f"&#{name};")

    def handle_comment(self, data):
        if not self.skip:
            self.out.append(f"<!--{data}-->")

    def handle_decl(self, decl):
        self.out.append(f"<!{decl}>")

    def handle_pi(self, data):
        self.out.append(f"<?{data}>")

    def result(self) -> str:
        if self.stack:
            raise SystemExit(f"unclosed tags: {self.stack}")
        return "".join(self.out)


# ------------------------------------------------------------------ head + JSON-LD
def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;").replace(">", "&gt;")


def jsonld(obj) -> str:
    # </script> cannot appear inside a JSON string that we write; escape "<" and "&" to be safe.
    return json.dumps(obj, ensure_ascii=False, indent=1).replace("<", "\\u003c").replace("&", "\\u0026")


def person_node(lang: str, full: bool) -> dict:
    node = {
        "@type": "Person", "@id": PERSON_ID, "name": NAME, "givenName": "Pablo", "familyName": "Pavon",
        "alternateName": ["Pablo Pavón", "Pablo Damián Pavón", "Pablo D. Pavon"],
        "url": SITE + "/", "jobTitle": JOB_TITLE, "sameAs": [LINKEDIN, GITHUB, UPWORK],
    }
    if not full:
        return node
    node.update({
        "description": PERSON_DESCRIPTION[lang],
        "email": "mailto:" + EMAIL,
        "image": SITE + "/assets/og/home-" + lang + ".png",
        "address": {"@type": "PostalAddress", "addressLocality": "Berlin", "addressCountry": "DE"},
        "workLocation": {"@type": "Place", "name": "Berlin, Germany",
                         "address": {"@type": "PostalAddress", "addressLocality": "Berlin", "addressCountry": "DE"}},
        "nationality": {"@type": "Country", "name": "Argentina"},
        "knowsLanguage": [
            {"@type": "Language", "name": "Spanish", "alternateName": "es"},
            {"@type": "Language", "name": "English", "alternateName": "en"},
            {"@type": "Language", "name": "German", "alternateName": "de"},
        ],
        "knowsAbout": KNOWS_ABOUT,
        "hasOccupation": {
            "@type": "Occupation", "name": "Business and Data Analyst",
            "occupationLocation": {"@type": "City", "name": "Berlin"},
            "skills": "Power BI, Tableau, SQL, Python, data migration, bank reconciliation, finance automation, requirements analysis",
        },
        "alumniOf": [
            {"@type": "EducationalOrganization", "name": "CEUPE European Business School"},
            {"@type": "EducationalOrganization", "name": "USI"},
        ],
        "makesOffer": [
            {"@type": "Offer",
             "url": SITE + lang_root(lang) + anchor,
             "itemOffered": {"@type": "Service", "name": (en if lang == "en" else es), "serviceType": en,
                             "description": (den if lang == "en" else des),
                             "provider": {"@id": PERSON_ID}, "areaServed": AREA_SERVED}}
            for en, es, den, des, anchor in SERVICES
        ],
    })
    return node


def home_jsonld(lang: str) -> dict:
    url = page_url("index.html", lang)
    return {"@context": "https://schema.org", "@graph": [
        {"@type": "WebSite", "@id": WEBSITE_ID, "url": SITE + "/", "name": NAME,
         "description": HOME["description"][lang], "inLanguage": ["en", "es"],
         "publisher": {"@id": PERSON_ID}, "author": {"@id": PERSON_ID}},
        {"@type": "ProfilePage", "@id": url + "#profilepage", "url": url, "name": HOME["title"][lang],
         "description": HOME["description"][lang], "inLanguage": lang, "isPartOf": {"@id": WEBSITE_ID},
         "about": {"@id": PERSON_ID}, "mainEntity": {"@id": PERSON_ID},
         "datePublished": HOME["published"], "dateModified": UPDATED,
         "primaryImageOfPage": {"@type": "ImageObject", "url": SITE + f"/assets/og/home-{lang}.png", "width": 1200, "height": 630}},
        person_node(lang, full=True),
    ]}


def case_jsonld(c: dict, lang: str) -> dict:
    rel = f"proyectos/{c['slug']}.html"
    url = page_url(rel, lang)
    title = c["title_en"] if lang == "en" else c["title_es"]
    repo_name = c["repo"].rstrip("/").rsplit("/", 1)[-1]
    return {"@context": "https://schema.org", "@graph": [
        {"@type": "Article", "@id": url + "#article", "headline": title + " · " + NAME,
         "alternativeHeadline": c["h1_en"] if lang == "en" else c["h1_es"],
         "description": c["desc"] if lang == "en" else c["desc_es"], "inLanguage": lang, "url": url,
         "mainEntityOfPage": {"@type": "WebPage", "@id": url},
         "image": [SITE + f"/assets/og/{c['slug']}-{lang}.png", SITE + "/assets/" + c["image"]],
         "author": {"@id": PERSON_ID}, "publisher": {"@id": PERSON_ID},
         "datePublished": c["published"], "dateModified": UPDATED, "isPartOf": {"@id": WEBSITE_ID},
         "keywords": c["keywords_en"] if lang == "en" else c["keywords_es"], "isAccessibleForFree": True,
         "genre": "Case study on synthetic data",
         "about": {"@type": "SoftwareSourceCode", "name": repo_name, "codeRepository": c["repo"],
                   "programmingLanguage": "Python", "author": {"@id": PERSON_ID}},
         "isBasedOn": c["repo"]},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": UI[lang]["home"], "item": page_url("index.html", lang)},
            {"@type": "ListItem", "position": 2, "name": UI[lang]["work"], "item": page_url("index.html", lang) + "#proyectos"},
            {"@type": "ListItem", "position": 3, "name": title, "item": url}]},
        person_node(lang, full=False),
    ]}


def head_html(rel: str, lang: str, meta: dict) -> str:
    url = page_url(rel, lang)
    alt = {l: page_url(rel, l) for l in LANGS}
    other = [l for l in LANGS if l != lang][0]
    is_article = rel != "index.html"
    lines = [
        '<meta charset="utf-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1">',
        f"<title>{esc(meta['title'])}</title>",
        f'<meta name="description" content="{esc(meta["description"])}">',
        f'<meta name="author" content="{NAME}">',
        '<meta name="robots" content="index, follow, max-image-preview:large">',
        f'<link rel="canonical" href="{url}">',
    ] + [f'<link rel="alternate" hreflang="{l}" href="{alt[l]}">' for l in LANGS] + [
        f'<link rel="alternate" hreflang="x-default" href="{alt[DEFAULT]}">',
        f'<meta property="og:type" content="{"article" if is_article else "website"}">',
        f'<meta property="og:site_name" content="{NAME}">',
        f'<meta property="og:locale" content="{OG_LOCALE[lang]}">',
        f'<meta property="og:locale:alternate" content="{OG_LOCALE[other]}">',
        f'<meta property="og:url" content="{url}">',
        f'<meta property="og:title" content="{esc(meta["title"])}">',
        f'<meta property="og:description" content="{esc(meta["description"])}">',
        f'<meta property="og:image" content="{SITE}{meta["image"]}">',
        '<meta property="og:image:type" content="image/png">',
        '<meta property="og:image:width" content="1200">',
        '<meta property="og:image:height" content="630">',
        f'<meta property="og:image:alt" content="{esc(meta["image_alt"])}">',
        '<meta name="twitter:card" content="summary_large_image">',
        f'<meta name="twitter:title" content="{esc(meta["title"])}">',
        f'<meta name="twitter:description" content="{esc(meta["description"])}">',
        f'<meta name="twitter:image" content="{SITE}{meta["image"]}">',
        f'<meta name="twitter:image:alt" content="{esc(meta["image_alt"])}">',
    ]
    if is_article:
        lines += [
            f'<meta property="article:published_time" content="{meta["published"]}">',
            f'<meta property="article:modified_time" content="{UPDATED}">',
            f'<meta property="article:author" content="{SITE}/">',
            '<meta property="article:section" content="Case studies">',
        ]
    lines += [
        '<meta name="msvalidate.01" content="26A77F480A2263EBDD3125FC7D7DB2BD">',  # Bing Webmaster Tools verification
        '<meta name="theme-color" content="#0e7a58">',
        '<link rel="icon" href="/favicon.ico" sizes="48x48">',
        '<link rel="icon" href="/favicon.svg" type="image/svg+xml">',
        '<link rel="apple-touch-icon" href="/apple-touch-icon.png">',
        '<link rel="sitemap" type="application/xml" href="/sitemap.xml">',
        '<link rel="preload" href="/assets/fonts/Geist-Variable.woff2" as="font" type="font/woff2" crossorigin>',
        '<link rel="stylesheet" href="/assets/css/site.css">',
        "<script>(function(){try{var t=localStorage.getItem('theme');if(t)document.documentElement.setAttribute('data-theme',t);}catch(e){}})();</script>",
        '<script type="application/ld+json">' + jsonld(meta["jsonld"]) + "</script>",
    ]
    return "<head>\n" + "\n".join(lines) + "\n</head>"


GLOBE = ('<svg class="seg-ic" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" '
         'stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.5 2.6 3.8 5.6 3.8 '
         '9s-1.3 6.4-3.8 9c-2.5-2.6-3.8-5.6-3.8-9S9.5 5.6 12 3z"/></svg>')


def lang_switch(rel: str, lang: str) -> str:
    links = []
    for l, label in (("es", "ES"), ("en", "EN")):
        cur = ' aria-current="page"' if l == lang else ""
        href = page_url(rel, l).replace(SITE, "")
        title = {"es": "Versión en español", "en": "English version"}[l]
        links.append(f'<a data-lang="{l}" href="{href}" hreflang="{l}" title="{title}"{cur}>{label}</a>')
    return f'<div class="seg" role="group" aria-label="{UI[lang]["switch_label"]}">{GLOBE}{"".join(links)}</div>'


# ------------------------------------------------------------------ build
def build_page(rel: str, lang: str, meta: dict) -> Path:
    src = (SRC / rel).read_text(encoding="utf-8")
    sp = Splitter(lang, posixpath.dirname(rel))
    sp.feed(src)
    sp.close()
    html = sp.result()
    html = re.sub(r"<head>.*?</head>", lambda _: head_html(rel, lang, meta), html, count=1, flags=re.S)
    html = html.replace("<!--LANGSWITCH-->", lang_switch(rel, lang))
    # sanity checks
    if html.count("<h1") != 1:
        raise SystemExit(f"{rel} [{lang}]: expected exactly one <h1>, found {html.count('<h1')}")
    if re.search(r'\slang="(?!' + lang + r'")', html):
        raise SystemExit(f"{rel} [{lang}]: leftover lang attribute of another language")
    if "<!--LANGSWITCH-->" in html or 'data-base=""' in html:
        raise SystemExit(f"{rel} [{lang}]: placeholder not replaced")
    out = out_path(rel, lang)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    return out


def pages() -> list[tuple[str, dict]]:
    """[(rel, meta-by-lang)] for every source page."""
    items = []
    items.append(("index.html", {
        l: {"title": HOME["title"][l], "description": HOME["description"][l],
            "image": f"/assets/og/home-{l}.png", "image_alt": HOME["image_alt"][l],
            "published": HOME["published"], "jsonld": home_jsonld(l)} for l in LANGS}))
    for c in build_cases.CASES:
        rel = f"proyectos/{c['slug']}.html"
        items.append((rel, {
            l: {"title": (c["title_en"] if l == "en" else c["title_es"]) + " · " + NAME,
                "description": c["desc"] if l == "en" else c["desc_es"],
                "image": f"/assets/og/{c['slug']}-{l}.png",
                "image_alt": c["alt_en"] if l == "en" else c["alt"],
                "published": c["published"], "jsonld": case_jsonld(c, l)} for l in LANGS}))
    return items


def write_sitemap(items):
    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">']
    for rel, _ in items:
        for lang in LANGS:
            lines.append("  <url>")
            lines.append(f"    <loc>{page_url(rel, lang)}</loc>")
            lines.append(f"    <lastmod>{UPDATED}</lastmod>")
            for l in LANGS:
                lines.append(f'    <xhtml:link rel="alternate" hreflang="{l}" href="{page_url(rel, l)}"/>')
            lines.append(f'    <xhtml:link rel="alternate" hreflang="x-default" href="{page_url(rel, DEFAULT)}"/>')
            lines.append("  </url>")
    lines.append("</urlset>")
    (ROOT / "sitemap.xml").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_robots():
    (ROOT / "robots.txt").write_text(
        "# pablodpavon.com\n"
        "# All crawlers are welcome, including AI search crawlers (OAI-SearchBot, Claude-SearchBot, PerplexityBot)\n"
        "# and AI training crawlers (GPTBot, ClaudeBot, Google-Extended). A summary for language models is at /llms.txt.\n"
        "User-agent: *\n"
        "Allow: /\n\n"
        f"Sitemap: {SITE}/sitemap.xml\n", encoding="utf-8")


def write_llms_txt():
    cases_en = "\n".join(
        f"- [{c['title_en']}]({page_url('proyectos/' + c['slug'] + '.html', 'en')}): {c['desc'].replace('Case study on synthetic data: ', '')} "
        f"Code: {c['repo']}" for c in build_cases.CASES)
    cases_es = "\n".join(
        f"- [{c['title_es']}]({page_url('proyectos/' + c['slug'] + '.html', 'es')}): {c['desc_es'].replace('Caso de estudio con datos sintéticos: ', '')}"
        for c in build_cases.CASES)
    services = "\n".join(f"- {en} / {es}: {den}" for en, es, den, des, _ in SERVICES)
    txt = f"""# Pablo Pavon — Freelance Senior Business & Data Analyst, Berlin

> {PERSON_DESCRIPTION['en']}

Facts: based in Berlin, Germany (CET); from Argentina; languages: Spanish (native), English (C1), German (B2);
fully remote; engagement models: diagnostic, fixed-scope project, monthly support; replies within 1–2 business days.
All dashboards and case studies on the site use synthetic data from fictional companies, and the code is public on GitHub.
Site last updated: {UPDATED}.

## Site
- [Home, English]({page_url('index.html', 'en')}): services, three live dashboards (retail sales nominal vs real, accounts payable control, cohort retention), case studies, experience, FAQ, contact
- [Inicio, español]({page_url('index.html', 'es')}): la misma página en español
- [CV (English, PDF)]({SITE}/assets/CV_Pablo_Pavon_EN.pdf)
- [CV (español, PDF)]({SITE}/assets/CV_Pablo_Pavon_ES.pdf)

## Services
{services}

## Case studies (English; synthetic data, open code)
{cases_en}

## Casos de estudio (español)
{cases_es}

## Profiles
- LinkedIn: {LINKEDIN}
- GitHub: {GITHUB}
- Upwork: {UPWORK}

## Contact
- Email: {EMAIL}
- Contact form: {page_url('index.html', 'en')}#contacto
"""
    (ROOT / "llms.txt").write_text(txt, encoding="utf-8")


def main():
    build_cases.build()
    items = pages()
    missing_og = []
    for rel, by_lang in items:
        for lang in LANGS:
            meta = by_lang[lang]
            out = build_page(rel, lang, meta)
            print("wrote", out.relative_to(ROOT))
            if not (ROOT / meta["image"].lstrip("/")).exists():
                missing_og.append(meta["image"])
    write_sitemap(items)
    write_robots()
    write_llms_txt()
    print("wrote sitemap.xml, robots.txt, llms.txt")
    if missing_og:
        print("WARNING: Open Graph images missing (run tools/build_og.py):", ", ".join(sorted(set(missing_og))))


if __name__ == "__main__":
    main()
