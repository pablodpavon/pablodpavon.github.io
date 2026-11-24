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
import build_legal  # noqa: E402  (Impressum and privacy notice, AJ-47, 1-nov-2026)
import build_vitrina  # noqa: E402  (/systems, /status, /links, 1-nov-2026)
import build_notes  # noqa: E402  (/notes/, English only, 24-nov-2026)

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"

SITE = "https://pablodpavon.com"
LANGS = ("en", "es")
DEFAULT = "en"                     # served at the root and used as x-default
UPDATED = "2026-10-21"             # base dateModified / lastmod: the last change that touched every page
HOME_UPDATED = "2026-11-24"        # the home: band with the link to /notes/ (24-nov-2026); bump with each home change


def modified(published: str, updated: str = UPDATED) -> str:
    """dateModified is never before datePublished (the GEO Scan case had 2026-10-31 > 2026-10-21; audit 31-oct-2026)."""
    return max(updated, published)

PERSON_ID = SITE + "/#person"
WEBSITE_ID = SITE + "/#website"
NAME = "Pablo Pavon"
JOB_TITLE = "Business Analyst"         # no "Senior" since D187; AI process automation since D231
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
    "title": {   # D231 (15-nov-2026): Servicio_Optimizacion_IA/Borradores/Web_cambios_pablodpavon_v1.md §0
        "en": "Pablo Pavon · AI process automation for small teams · Berlin",
        "es": "Pablo Pavon · Procesos con IA para equipos chicos · Berlín",
    },
    "description": {
        "en": "I find the work your team repeats every month and hand it to AI, with checks: process review, setup in Claude Code, automations that report their failures.",
        "es": "Encuentro el trabajo que tu equipo repite cada mes y lo paso a la IA con controles: revisión de procesos, implementación en Claude Code y automatizaciones.",
    },
    "image_alt": {
        "en": "Pablo Pavon, freelance business analyst in Berlin: AI process automation for small teams",
        "es": "Pablo Pavon, business analyst freelance en Berlín: procesos con IA para equipos chicos",
    },
    "published": "2026-10-13",
}

PERSON_DESCRIPTION = {   # D231: spec §8 (experience intro) in the third person + the SearchedBy line of the hero (§2)
    "en": "Pablo Pavon is a freelance business analyst based in Berlin, Germany, originally from Argentina. "
          "He works remotely with small and mid-sized companies and teams in Argentina, Latin America, Israel and Europe, "
          "in Spanish, English and German. He specialises in reviewing how teams work and moving the repetitive part to AI "
          "with controls: one place for the team's AI work, automations that report their own failures, and finance processes "
          "that run themselves. He developed two products that are already live: SearchedBy and NexYn. "
          "He has ten years of experience across banking, e-commerce, marketing analytics and insurance.",
    "es": "Pablo Pavon es business analyst freelance con base en Berlín, Alemania, y origen argentino. "
          "Trabaja en remoto con empresas chicas y medianas y con equipos de Argentina, Latinoamérica, Israel y Europa, "
          "en español, inglés y alemán. Se especializa en revisar cómo trabajan los equipos y pasar a la IA la parte repetitiva, "
          "con controles: la IA del equipo en un solo lugar, automatizaciones que avisan cuando fallan y procesos de finanzas "
          "que corren solos. Desarrolló dos productos que ya están en línea: SearchedBy y NexYn. "
          "Tiene diez años de experiencia en banca, e-commerce, analítica de marketing y seguros.",
}

SERVICES = [  # (en name, es name, en description, es description, anchor) · the six cards of the home, D231 (spec §3)
    ("AI process review", "Revisión de procesos con IA",
     "An inventory of your recurring work, written by your own AI from a task I send; a review area by area; up to seven decisions, each with a recommended option.",
     "Un inventario del trabajo que se repite, escrito por tu propia IA a partir de una tarea que te paso; una revisión área por área; hasta siete decisiones, cada una con una opción recomendada.",
     "ai-process-review.html"),
    ("One place for your AI work", "Tu IA, en un solo lugar",
     "Chats, projects and scheduled tasks moved into one Claude Code project: clear rules, a folder per area, nightly backups, sending and deleting blocked by default.",
     "Chats, proyectos y tareas programadas en un solo proyecto de Claude Code: reglas claras, una carpeta por área, backup cada noche, envíos y borrados bloqueados por defecto.",
     "#ia-en-un-lugar"),
    ("Automations with controls", "Automatizaciones con controles",
     "Recurring reports, field notes sorted the same day, reminders to the team as drafts, a check on every draft before it goes out. Each one says whether it ran and alerts you when it fails.",
     "Informes recurrentes, notas de campo ordenadas el mismo día, recordatorios al equipo como borradores, un chequeo de cada borrador antes de que salga. Cada una dice si corrió y avisa cuando falla.",
     "#ia"),
    ("Finance processes that run themselves", "Procesos de finanzas que corren solos",
     "Bank reconciliation, supplier invoice control, collections and cash forecasting that update themselves every morning, for SMEs and accounting firms.",
     "Conciliación bancaria, control de facturas de proveedores, cobranzas y caja proyectada que se actualizan solos cada mañana, para pymes y estudios contables.",
     "#automatizacion-financiera"),
    ("Requirements and process maps", "Requerimientos y mapas de procesos",
     "Discovery, user stories with acceptance criteria, functional specs and process maps that IT can build without guessing, and a manual your team can follow.",
     "Relevamiento, user stories con criterios de aceptación, especificaciones funcionales y mapeo de procesos, y un manual que tu equipo pueda seguir.",
     "#requerimientos"),
    ("Your team and AI", "Tu equipo y la IA",
     "A short, practical course by role, built on your team's real tasks, and a map of who already uses AI and how.",
     "Un curso corto y práctico por rol, armado con las tareas reales de tu equipo, y un mapa de quién ya usa IA y cómo.",
     "#equipo-e-ia"),
]

KNOWS_ABOUT = ["AI process automation", "Business process analysis", "Claude Code", "Workflow automation", "Business analysis",
               "Requirements engineering", "User stories", "Process mapping", "Bank reconciliation", "Accounts payable control",
               "Cash flow forecasting", "Data migration", "Data quality", "AI-assisted reporting", "Python", "SQL", "GDPR"]  # D231

AREA_SERVED = ["Germany", "European Union", "Argentina", "Latin America", "Israel", "United States"]

EN_ONLY = ("notes/",)               # folders published in English only: no /es/ copy, links from ES pages go to the English page

UI = {
    "en": {"home": "Home", "work": "Portfolio", "switch_label": "Language"},
    "es": {"home": "Inicio", "work": "Portfolio", "switch_label": "Idioma"},
}


# ------------------------------------------------------------------ URL helpers
def lang_root(lang: str) -> str:
    return "/" if lang == DEFAULT else f"/{lang}/"


def page_url(rel: str, lang: str) -> str:
    """rel is the source path relative to src/, e.g. 'index.html' or 'proyectos/x.html'."""
    root = lang_root(lang)
    if rel.endswith("/index.html"):                 # /notes/ instead of /notes/index.html
        rel = rel[: -len("index.html")]
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
    elif norm.startswith(EN_ONLY) or norm + "/" in EN_ONLY:
        new = "/" + (norm[: -len("index.html")] if norm.endswith("/index.html") else norm)
        if norm + "/" in EN_ONLY:
            new += "/"
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
            "@type": "Occupation", "name": "Business Analyst",
            "occupationLocation": {"@type": "City", "name": "Berlin"},
            "skills": "AI process review, Claude Code, workflow automation, finance automation, requirements analysis, process mapping, Python, SQL",
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
         "datePublished": HOME["published"], "dateModified": modified(HOME["published"], HOME_UPDATED),
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
         "datePublished": c["published"], "dateModified": modified(c["published"], c.get("updated", UPDATED)), "isPartOf": {"@id": WEBSITE_ID},
         "keywords": c["keywords_en"] if lang == "en" else c["keywords_es"], "isAccessibleForFree": True,
         "genre": c.get("genre", "Case study on synthetic data"),
         "about": {"@type": "SoftwareSourceCode", "name": repo_name, "codeRepository": c["repo"],
                   "programmingLanguage": "Python", "author": {"@id": PERSON_ID}},
         "isBasedOn": c["repo"], **({"mentions": c["product"]} if c.get("product") else {})},   # SearchedBy's Organization (1-nov-2026)
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": UI[lang]["home"], "item": page_url("index.html", lang)},
            {"@type": "ListItem", "position": 2, "name": UI[lang]["work"], "item": page_url("portfolio.html", lang)},
            {"@type": "ListItem", "position": 3, "name": title, "item": url}]},
        person_node(lang, full=False),
    ]}


def vitrina_jsonld(rel: str, page: dict, lang: str) -> dict:
    url = page_url(rel, lang)
    graph = [
        {"@type": page["type"], "@id": url + "#webpage", "url": url, "name": page["title"][lang],
         "description": page["description"][lang], "inLanguage": lang, "isPartOf": {"@id": WEBSITE_ID},
         "about": {"@id": PERSON_ID}, "author": {"@id": PERSON_ID},
         "datePublished": page["published"], "dateModified": page["published"]},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": UI[lang]["home"], "item": page_url("index.html", lang)},
            {"@type": "ListItem", "position": 2, "name": page["title"][lang], "item": url}]},
        person_node(lang, full=False),
    ]
    if page.get("service"):                          # service page (D231): the page is about one Service
        graph[0]["mainEntity"] = {"@id": url + "#service"}
        graph.insert(1, {"@type": "Service", "@id": url + "#service", "name": page["service"][lang],
                         "serviceType": page["service"]["en"], "description": page["description"][lang], "url": url,
                         "provider": {"@id": PERSON_ID}, "areaServed": AREA_SERVED})
    return {"@context": "https://schema.org", "@graph": graph}


def notes_index_jsonld(notes: list[dict]) -> dict:
    url = page_url("notes/index.html", "en")
    return {"@context": "https://schema.org", "@graph": [
        {"@type": "Blog", "@id": url + "#blog", "url": url, "name": "Notes · " + NAME,
         "description": build_notes.INDEX_DESCRIPTION, "inLanguage": "en", "isPartOf": {"@id": WEBSITE_ID},
         "author": {"@id": PERSON_ID}, "publisher": {"@id": PERSON_ID},
         "blogPost": [{"@id": page_url(f"notes/{n['slug']}.html", "en") + "#post"} for n in notes]},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": UI["en"]["home"], "item": page_url("index.html", "en")},
            {"@type": "ListItem", "position": 2, "name": "Notes", "item": url}]},
        person_node("en", full=False),
    ]}


def note_jsonld(n: dict) -> dict:
    url = page_url(f"notes/{n['slug']}.html", "en")
    post = {"@type": "BlogPosting", "@id": url + "#post", "headline": n["title"], "description": n["description"],
            "inLanguage": "en", "url": url, "mainEntityOfPage": {"@type": "WebPage", "@id": url},
            "datePublished": n["date"], "dateModified": n.get("update", {}).get("date", n["date"]),
            "author": {"@id": PERSON_ID}, "publisher": {"@id": PERSON_ID},
            "isPartOf": {"@id": page_url("notes/index.html", "en") + "#blog"},
            "image": SITE + "/assets/og/home-en.png", "isAccessibleForFree": True,
            "articleBody": "\n\n".join(n["body"])}
    if n.get("linkedin_url"):
        post["sameAs"] = n["linkedin_url"]
    return {"@context": "https://schema.org", "@graph": [
        post,
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": UI["en"]["home"], "item": page_url("index.html", "en")},
            {"@type": "ListItem", "position": 2, "name": "Notes", "item": page_url("notes/index.html", "en")},
            {"@type": "ListItem", "position": 3, "name": n["title"], "item": url}]},
        person_node("en", full=False),
    ]}


def head_html(rel: str, lang: str, meta: dict) -> str:
    url = page_url(rel, lang)
    langs = meta.get("langs", LANGS)
    alt = {l: page_url(rel, l) for l in langs}
    other = ([l for l in langs if l != lang] or [None])[0]
    is_article = rel != "index.html" and not meta.get("legal") and meta.get("kind") != "page"
    lines = [
        '<meta charset="utf-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1">',
        f"<title>{esc(meta['title'])}</title>",
        f'<meta name="description" content="{esc(meta["description"])}">',
        f'<meta name="author" content="{NAME}">',
        f'<meta name="robots" content="{meta.get("robots", "index, follow, max-image-preview:large")}">',
        f'<link rel="canonical" href="{url}">',
    ] + [f'<link rel="alternate" hreflang="{l}" href="{alt[l]}">' for l in langs] + [
        f'<link rel="alternate" hreflang="x-default" href="{alt[DEFAULT]}">',
        f'<meta property="og:type" content="{"article" if is_article else "website"}">',
        f'<meta property="og:site_name" content="{NAME}">',
        f'<meta property="og:locale" content="{OG_LOCALE[lang]}">',
    ] + ([f'<meta property="og:locale:alternate" content="{OG_LOCALE[other]}">'] if other else []) + [
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
            f'<meta property="article:modified_time" content="{meta.get("modified", UPDATED)}">',
            f'<meta property="article:author" content="{SITE}/">',
            f'<meta property="article:section" content="{meta.get("section", "Case studies")}">',
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
    ] + [f'<link rel="stylesheet" href="{css}">' for css in meta.get("css", [])] + [
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
    html = html.replace("<!--LANGSWITCH-->", lang_switch(rel, lang) if len(meta.get("langs", LANGS)) > 1 else "")
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
            "published": HOME["published"], "css": ["/assets/css/vitrina.css"], "jsonld": home_jsonld(l)} for l in LANGS}))
    for c in build_cases.CASES:
        rel = f"proyectos/{c['slug']}.html"
        items.append((rel, {
            l: {"title": (c["title_en"] if l == "en" else c["title_es"]) + " · " + NAME,
                "description": c["desc"] if l == "en" else c["desc_es"],
                "image": f"/assets/og/{c['slug']}-{l}.png",
                "image_alt": c["alt_en"] if l == "en" else c["alt"],
                "published": c["published"], "modified": modified(c["published"], c.get("updated", UPDATED)),
                "css": ["/assets/css/vitrina.css"],          # nav with the Systems link (1-nov-2026)
                "jsonld": case_jsonld(c, l)} for l in LANGS}))
    for rel, page in build_vitrina.PAGES.items():     # /systems, /status, /links (1-nov-2026), /ai-process-review (D231): indexed, in the sitemap
        items.append((rel, {
            l: {"title": page.get("seo_title", {}).get(l) or page["title"][l] + " · " + NAME, "description": page["description"][l],
                "image": f"/assets/og/{page.get('og', 'home')}-{l}.png", "image_alt": page["image_alt"][l],
                "published": page["published"], "modified": page["published"], "kind": "page",
                "css": ["/assets/css/vitrina.css"], "jsonld": vitrina_jsonld(rel, page, l)} for l in LANGS}))
    notes = build_notes.published()                  # /notes/ (24-nov-2026): English only, in the sitemap
    if notes:
        newest = notes[0]["date"]
        items.append(("notes/index.html", {"en": {
            "title": "Notes · " + NAME, "description": build_notes.INDEX_DESCRIPTION,
            "image": "/assets/og/home-en.png", "image_alt": HOME["image_alt"]["en"], "published": "2026-11-24",
            "modified": max("2026-11-24", newest), "kind": "page", "langs": ("en",),
            "css": ["/assets/css/vitrina.css", "/assets/css/notes.css"], "jsonld": notes_index_jsonld(notes)}}))
        for n in notes:
            items.append((f"notes/{n['slug']}.html", {"en": {
                "title": n["title"] + " · " + NAME, "description": n["description"],
                "image": "/assets/og/home-en.png", "image_alt": HOME["image_alt"]["en"], "published": n["date"],
                "modified": n.get("update", {}).get("date", n["date"]), "langs": ("en",), "section": "Notes",
                "css": ["/assets/css/vitrina.css", "/assets/css/notes.css"], "jsonld": note_jsonld(n)}}))
    for rel, page in build_legal.PAGES.items():       # AJ-47 (1-nov-2026): noindex, outside the sitemap
        items.append((rel, {
            l: {"title": page["title"][l] + " · " + NAME, "description": page["description"][l],
                "image": f"/assets/og/home-{l}.png", "image_alt": HOME["image_alt"][l], "published": page["published"],
                "robots": "noindex, follow", "legal": True,
                "jsonld": {"@context": "https://schema.org", "@type": "WebPage", "url": page_url(rel, l), "name": page["title"][l],
                           "inLanguage": l, "isPartOf": {"@id": WEBSITE_ID}, "about": {"@id": PERSON_ID},
                           "dateModified": page["published"]}} for l in LANGS}))
    return items


def write_sitemap(items):
    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">']
    for rel, meta in items:
        if meta[DEFAULT].get("legal"):               # noindex pages stay out of the sitemap
            continue
        langs = meta[DEFAULT].get("langs", LANGS)
        for lang in langs:
            lines.append("  <url>")
            lines.append(f"    <loc>{page_url(rel, lang)}</loc>")
            day = modified(meta[lang]["published"], HOME_UPDATED) if rel == "index.html" else meta[lang]["modified"]
            lines.append(f"    <lastmod>{day}</lastmod>")
            for l in langs:
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
    notes = build_notes.published()
    notes_txt = "\n".join(f"- [{n['title']}]({page_url('notes/' + n['slug'] + '.html', 'en')}) ({n['date']}): {n['description']}"
                          for n in notes) or "- (none yet)"
    txt = f"""# Pablo Pavon: AI process automation for small teams; business analyst, Berlin

> {PERSON_DESCRIPTION['en']}

Facts: based in Berlin, Germany (CET); from Argentina; languages: Spanish (native), English (C1), German (B2);
fully remote; engagement models: process review, setup at a fixed price, monthly follow-up; replies within 1–2 business days.
The case studies on the site use synthetic data from fictional companies, and the code is public on GitHub. The exceptions are SearchedBy (formerly GEO Scan), an AI product Pablo designed and developed, sold together with NexYn, live at https://searchedby.com/ (private code, public case study), and the pilot case on the AI process review page, a real engagement described without the client's name.
Site last updated: {max([HOME_UPDATED, UPDATED] + [modified(c["published"], c.get("updated", UPDATED)) for c in build_cases.CASES] + [n["date"] for n in notes])}.

## Site
- [Home, English]({page_url('index.html', 'en')}): services, case studies, how I work, three ways to start, experience, FAQ, contact
- [Inicio, español]({page_url('index.html', 'es')}): la misma página en español
- [AI process review]({page_url('ai-process-review.html', 'en')}): the service page: who it is for, how it works in four steps, what is not automated, a pilot case with a construction supervision firm, FAQ. For companies, the service now lives at NexYn: https://nexyn-ai.com/
- [Procesos con IA, español]({page_url('ai-process-review.html', 'es')}): la misma página en español
- [Portfolio]({page_url('portfolio.html', 'en')}): every project grouped by kind: a real pilot without names, products and tools I built, automations that run on their own, a prototype, demos on synthetic data, and what I can build
- [Portfolio, español]({page_url('portfolio.html', 'es')}): la misma página en español
- [Systems I built and run]({page_url('systems.html', 'en')}): what each system does, what runs on its own, links to the case and the code
- [Systems status]({page_url('status.html', 'en')}): last run, items processed, cost and state of each scheduled system, generated daily (data: {SITE}/assets/data/status.json)
- [Notes]({page_url('notes/index.html', 'en')}): short notes in English on what Pablo builds with AI, how he checks it and what broke; each one first posted on LinkedIn
- [Links]({page_url('links.html', 'en')}): all profiles on one page
- [CV (English, PDF)]({SITE}/assets/CV_Pablo_Pavon_EN.pdf)
- [CV (español, PDF)]({SITE}/assets/CV_Pablo_Pavon_ES.pdf)

## Services
{services}

## Case studies (English)
{cases_en}

## Casos de estudio (español)
{cases_es}

## Notes (English, first posted on LinkedIn)
{notes_txt}

## Products
- SearchedBy: {"https://searchedby.com/"}: shows a business how AI assistants (ChatGPT, Perplexity, Claude, Google's AI) present it, and whether its site can be read, cited and recommended. Designed and developed by Pablo Pavon; sold together with NexYn; formerly called GEO Scan. About: https://searchedby.com/about/
- NexYn: https://nexyn-ai.com/ (Spanish: https://nexyn-ai.com/es/): process automation for small businesses, with or without AI; free first reading in writing within 48 business hours. Developed by Pablo Pavon.

## Profiles
- LinkedIn: {LINKEDIN}
- GitHub: {GITHUB}
- Upwork: {UPWORK}

## Contact
- Email: {EMAIL}
- Contact form: {page_url('index.html', 'en')}#contacto
- Legal notice (Impressum): {page_url('impressum.html', 'en')} · Privacy: {page_url('privacy.html', 'en')}
"""
    (ROOT / "llms.txt").write_text(txt, encoding="utf-8")


def main():
    build_cases.build()
    build_legal.build()
    build_vitrina.build()
    build_notes.build()
    items = pages()
    keep = {rel for rel, _ in items if rel.startswith("notes/")}
    for old in (ROOT / "notes").glob("*.html") if (ROOT / "notes").exists() else []:
        if "notes/" + old.name not in keep:          # a note taken back disappears from the site too
            old.unlink()
            print("removed", old.relative_to(ROOT))
    missing_og = []
    for rel, by_lang in items:
        for lang in by_lang:
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
