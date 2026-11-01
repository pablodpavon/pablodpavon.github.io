"""Build the bilingual sources of three pages added on 1-nov-2026 (vitrina, part B):

    src/systems.html  -> /systems.html  /es/systems.html   hub "Systems I built and run"
    src/status.html   -> /status.html   /es/status.html    Systems status, rendered from /assets/data/status.json
    src/links.html    -> /links.html    /es/links.html     short link-in-bio page for profiles and forms

GitHub Pages also serves them without the extension (pablodpavon.com/links), so that is the address to share;
canonical URLs keep .html like the rest of the site. Called by tools/build_site.py, which writes the <head>.

Sources of the numbers on /systems (all already public on this site or verified on 1-nov-2026):
- ~3,800 tests, 4 languages, 98.1 %, 66 runs, 12 rules, 1,260 invoices, 12 checks, 4,060/6,500, 4 error types,
  ~47,000 orders: tools/build_cases.py (the published case studies).
- US$ 0.23 for one full scan: Diario/2026-11-01.md 00:03 (US$ 0.2333, one re-scan with 15 engine runs).
- 155 decisions: 02_Estrategia_y_Decisiones.md (D1-D155). 197 of 197 files: GEO/CLAUDE.md (deploy of 30-oct).
- Two background workers: the public https://searchedby.com/healthz answer.
"""
from pathlib import Path

from build_cases import ICON_BACK, ICON_GH, ICON_NEXT, bi

ROOT = Path(__file__).resolve().parents[1]
PUBLISHED = "2026-11-01"
GH = "https://github.com/pablodpavon"
ENG_REPO = GH + "/searchedby-engineering"
STATUS_SRC = GH + "/pablodpavon.github.io/blob/main/tools/status/build_status.py"

PAGES = {
    "systems.html": {
        "title": {"en": "Systems I built and run", "es": "Sistemas que construí y que corren"},
        "description": {"en": "AI and automation systems by Pablo Pavon: what each one does, what runs on its own, and links to the case study and the code.",
                        "es": "Sistemas de IA y automatización de Pablo Pavon: qué hace cada uno, qué corre solo y links al caso y al código."},
        "image_alt": {"en": "Systems built and run by Pablo Pavon", "es": "Sistemas construidos y operados por Pablo Pavon"},
        "type": "CollectionPage",
    },
    "status.html": {
        "title": {"en": "Systems status", "es": "Estado de los sistemas"},
        "description": {"en": "Last run, items processed, cost and state of the systems Pablo Pavon runs on a schedule, generated once a day from their logs.",
                        "es": "Última corrida, ítems procesados, costo y estado de los sistemas que Pablo Pavon corre de forma programada, generado una vez por día desde sus logs."},
        "image_alt": {"en": "Status of the systems run by Pablo Pavon", "es": "Estado de los sistemas que opera Pablo Pavon"},
        "type": "WebPage",
    },
    "links.html": {
        "title": {"en": "Links", "es": "Links"},
        "description": {"en": "Pablo Pavon, freelance Senior Business & Data Analyst in Berlin: website, systems, SearchedBy, GitHub, LinkedIn, Upwork and email.",
                        "es": "Pablo Pavon, Senior Business & Data Analyst freelance en Berlín: sitio, sistemas, SearchedBy, GitHub, LinkedIn, Upwork y email."},
        "image_alt": {"en": "Links of Pablo Pavon", "es": "Links de Pablo Pavon"},
        "type": "WebPage",
    },
}
for _p in PAGES.values():
    _p["published"] = PUBLISHED

ICON = {
    "web": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.5 2.6 3.8 5.6 3.8 9s-1.3 6.4-3.8 9c-2.5-2.6-3.8-5.6-3.8-9S9.5 5.6 12 3z"/></svg>',
    "sys": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="7" rx="2"/><rect x="3" y="13" width="18" height="7" rx="2"/><path d="M7 7.5h.01M7 16.5h.01"/></svg>',
    "pulse": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 12h4l3-7 4 14 3-7h4"/></svg>',
    "search": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>',
    "gh": ICON_GH,
    "in": '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M4.98 3.5a2.5 2.5 0 1 1 0 5 2.5 2.5 0 0 1 0-5zM3 9.5h4V21H3zM9.5 9.5h3.8v1.6h.1c.5-1 1.8-2 3.8-2 4 0 4.8 2.6 4.8 6V21h-4v-5.2c0-1.2 0-2.9-1.8-2.9s-2 1.4-2 2.8V21h-4z"/></svg>',
    "up": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 5v6a5 5 0 0 0 10 0V5"/><path d="M15 11c1 2.5 2.5 4 4 4a3 3 0 0 0 0-6c-2 0-3.2 2-4 4l-2 8"/></svg>',
    "mail": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/></svg>',
    "cv": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 2h9l5 5v15H6z"/><path d="M14 2v6h6M9 13h6M9 17h4"/></svg>',
}


# ------------------------------------------------------------------ shell
def nav(current: str = "") -> str:
    def a(href, es, en, key=""):
        cur = ' aria-current="page"' if key and key == current else ""
        return f'<a href="{href}"{cur}>{bi(es, en) if es != en else es}</a>'
    return "\n      ".join([
        a("index.html#servicios", "Servicios", "Services"),
        a("index.html#lab", "Dashboards", "Dashboards"),
        a("index.html#proyectos", "Proyectos", "Work"),
        a("systems.html", "Sistemas", "Systems", "systems"),
        a("index.html#experiencia", "Experiencia", "Experience"),
        a("index.html#contacto", "Contacto", "Contact"),
    ])


def head(title_en: str, current: str = "", full_nav: bool = True) -> str:
    # The published <head> is generated by tools/build_site.py; this one only keeps the source previewable.
    top = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title_en} · Pablo Pavon · bilingual source</title>
<link rel="stylesheet" href="assets/css/site.css">
<link rel="stylesheet" href="assets/css/vitrina.css">
<script>(function(){{try{{var t=localStorage.getItem('theme');if(t)document.documentElement.setAttribute('data-theme',t);}}catch(e){{}}}})();</script>
</head>
"""
    if not full_nav:
        return top + '<body data-base="" class="lk-page">\n'
    return top + f"""<body data-base="">
<header class="nav">
  <div class="nav-inner">
    <a class="brand" href="index.html"><span class="logo">PP</span>Pablo Pavon</a>
    <nav class="links" aria-label-es="Secciones" aria-label-en="Sections">
      {nav(current)}
    </nav>
    <div class="nav-tools">
      <!--LANGSWITCH-->
      <button class="icon-btn" id="themeBtn" type="button" aria-label-es="Tema" aria-label-en="Theme"></button>
      <button class="btn btn-primary btn-sm" type="button" data-open-contact>{bi('Hablemos', 'Let’s talk')}</button>
      <button class="icon-btn menu-btn" id="menuBtn" type="button" aria-label-es="Menú" aria-label-en="Menu" aria-expanded="false"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M4 7h16M4 12h16M4 17h16"/></svg></button>
    </div>
  </div>
</header>
"""


def foot(note: str = "", scripts=("assets/js/shell.js", "assets/js/contact.js")) -> str:
    tags = "\n".join(f'<script src="{s}"></script>' for s in scripts)
    return f"""
<footer class="site" style="margin-top:0;padding-top:0"><div class="container"><div class="f-bot" style="margin-top:0">
  <span>© <span data-year>2026</span> Pablo Pavon</span>
  {note}
  <span class="f-legal"><a href="impressum.html">Impressum</a> · <a href="privacy.html">{bi('Privacidad', 'Privacy')}</a></span>
</div></div></footer>
{tags}
</body>
</html>
"""


def hero(title, lede_es, lede_en, pill=None, extra=""):
    p = f'<span class="pill"><span class="dot"></span>{bi(*pill)}</span>\n' if pill else ""
    return f"""<section class="cs-hero v-hero">
  <div class="mesh" aria-hidden="true"><span></span><span></span><span></span><span></span></div>
  <div class="grid-bg" aria-hidden="true"></div>
  <div class="container">
    <a class="cs-back" href="index.html">{ICON_BACK}{bi('Inicio', 'Home')}</a><br>
    {p}<h1 lang="es">{title['es']}</h1><h1 lang="en">{title['en']}</h1>
    <p class="lede" lang="es">{lede_es}</p><p class="lede" lang="en">{lede_en}</p>
    {extra}
  </div>
</section>
"""


# ------------------------------------------------------------------ /systems
SYN = ("Caso con datos sintéticos", "Case study on synthetic data")

# Each system: chips, (title es, en), (what es, en), (runs alone es, en), figures [(value es, value en, label es, label en)],
# links [(href, label es, label en, kind)], feature (full width)
SYSTEMS = [
    dict(
        chips=[("own", "Producto propio · beta abierta", "Own product · open beta"), ("", "Python", "Python"), ("", "FastAPI", "FastAPI"), ("", "LLM APIs", "LLM APIs")],
        title=("SearchedBy: cómo te presentan los asistentes de IA", "SearchedBy: how AI assistants present a business"),
        what=("Muestra a un negocio qué responden ChatGPT, Perplexity y Google con IA cuando un cliente pregunta por su rubro, y qué le falta a su sitio para que lo citen.",
              "Shows a business what ChatGPT, Perplexity and Google's AI answer when a customer asks about its field, and what its site is missing to be cited."),
        runs=("Cada scan corre en dos procesos de fondo: uno lee el sitio y el otro les pregunta a los motores de IA. La salud del servicio se revisa todos los días en la página de estado.",
              "Each scan runs on two background workers: one reads the site, the other asks the AI engines. The service health is checked every day on the status page."),
        figs=[("~3.800", "~3,800", "tests antes de cada deploy", "tests before every deploy"),
              ("US$ 0,23", "US$ 0.23", "costo de IA de un scan completo reciente", "AI cost of a recent full scan"),
              ("4", "4", "idiomas en la interfaz", "interface languages")],
        links=[("proyectos/geo-scan.html", "Leer el caso", "Read the case", "case"),
               ("https://searchedby.com/", "Abrir SearchedBy", "Open SearchedBy", "ext"),
               (ENG_REPO, "Ingeniería en GitHub", "Engineering on GitHub", "code")],
        feature=True,
    ),
    dict(
        chips=[("", "Método", "Method"), ("", "QA", "QA"), ("", "Claude Code", "Claude Code")],
        title=("Cómo llevo sistemas de IA a producción", "How I ship AI systems"),
        what=("El método detrás de SearchedBy contado como caso: cada decisión registrada, los tests antes que el código, una checklist y una comparación de archivos por checksum en cada deploy, revisores nativos para cada idioma y el costo de cada corrida a la vista.",
              "The method behind SearchedBy, written up as a case: every decision logged, tests before code, a checklist and a checksum comparison of every file on each deploy, native-speaker reviewers for each language, and the cost of every run on record."),
        runs=("No agrega nada que corra: documenta cómo se construyen, se despliegan y se controlan los demás sistemas.",
              "It adds nothing that runs: it documents how the other systems are built, deployed and checked."),
        figs=[("155", "155", "decisiones registradas", "decisions logged"),
              ("197 de 197", "197 of 197", "archivos iguales en servidor y origen, último control", "files identical on server and source, last check")],
        links=[("proyectos/ai-systems-operating-model.html", "Leer el caso", "Read the case", "case"),
               (ENG_REPO, "Ver en GitHub", "View on GitHub", "code")],
    ),
    dict(
        chips=[("", "IA", "AI"), ("syn", *SYN), ("", "Python", "Python")],
        title=("Reporte de KPIs con IA que verifica sus números", "AI KPI report that checks its own numbers"),
        what=("Un LLM redacta el comentario de KPIs y un control prueba cada cifra contra los datos: que exista, que sea de la métrica y el período correctos, y que \"subió\" coincida con el dato. Si un número falla, no se publica nada.",
              "An LLM drafts the KPI commentary and a checker tests every figure against the data: it must exist, belong to the right metric and period, and \"rose\" must match the data. If one number fails, nothing is published."),
        runs=("Una corrida programada genera datos nuevos de la tienda sintética, recalcula los KPIs, redacta el comentario y pasa el control. La última corrida figura en la página de estado.",
              "A scheduled run generates new data for the synthetic store, recomputes the KPIs, drafts the commentary and runs the check. The last run is on the status page."),
        figs=[("4", "4", "tipos de error que detecta", "error types it detects"),
              ("~47.000", "~47,000", "órdenes en los datos de prueba", "orders in the test data")],
        links=[("proyectos/reporte-con-ia.html", "Leer el caso", "Read the case", "case"),
               (GH + "/ai-kpi-commentary", "Código", "Code", "code")],
    ),
    dict(
        chips=[("", "Business analysis", "Business analysis"), ("syn", *SYN)],
        title=("De requerimientos a backlog", "Requirements to backlog"),
        what=("Convierte la transcripción de un workshop en user stories con criterios de aceptación, preguntas abiertas y una matriz de trazabilidad. Cada story cita la frase de la que sale, y un control marca las que no tienen origen.",
              "Turns a workshop transcript into user stories with acceptance criteria, open questions and a traceability matrix. Every story quotes the sentence it comes from, and a check flags any story without a source."),
        runs=("Tres casos ya procesados para recorrer. No hay campo de texto libre, así que no hay costo por visita.",
              "Three precomputed cases to browse. There is no free-text input, so there is no cost per visit."),
        figs=[],
        links=[("proyectos/requirements-to-backlog.html", "Leer el caso", "Read the case", "case")],
    ),
    dict(
        chips=[("", "Finanzas", "Finance"), ("syn", *SYN), ("", "Python", "Python")],
        title=("Conciliación y caja diaria", "Daily reconciliation and cash"),
        what=("Concilia los extractos de dos bancos contra el sistema, marca las cobranzas sin imputar con la factura sugerida, lista los clientes atrasados y proyecta la caja de cuatro semanas.",
              "Reconciles two bank statements against the ERP, flags unbooked receipts with the suggested invoice, lists late customers and projects four weeks of cash."),
        runs=("Corre cada mañana y deja listos el resumen del día, la lista de pendientes y el Excel de control antes de que llegue el equipo.",
              "Runs every morning and leaves the daily summary, the open-items list and the control workbook ready before the team arrives."),
        figs=[("98,1 %", "98.1%", "conciliado o registrado solo", "reconciled or booked automatically"),
              ("66", "66", "corridas diarias en el caso de prueba", "daily runs in the test case")],
        links=[("proyectos/conciliacion-y-caja.html", "Leer el caso", "Read the case", "case"),
               (GH + "/daily-cash-control", "Código", "Code", "code")],
    ),
    dict(
        chips=[("", "Finanzas", "Finance"), ("syn", *SYN), ("", "Python", "Python")],
        title=("Control de facturas antes de pagar", "Supplier invoice control before payment"),
        what=("Doce reglas revisan CUIT, duplicados, IVA, orden de compra, recepción y CAE, y clasifican cada factura en pagar, revisar o bloquear.",
              "Twelve rules check tax ID, duplicates, VAT, purchase order, goods receipt and CAE, and sort each invoice into pay, review or block."),
        runs=("Corre antes de cada corrida de pagos y entrega la lista de excepciones con el motivo de cada una.",
              "Runs before each payment run and hands over the exception list with the reason for each one."),
        figs=[("12", "12", "reglas documentadas", "documented rules"),
              ("1.260", "1,260", "facturas en los datos de prueba", "invoices in the test data")],
        links=[("proyectos/cuentas-a-pagar.html", "Leer el caso", "Read the case", "case"),
               (GH + "/ap-invoice-control", "Código", "Code", "code")],
    ),
    dict(
        chips=[("", "Migración", "Migration"), ("syn", *SYN), ("", "Python", "Python")],
        title=("Migración de datos con conciliación", "Data migration with reconciliation"),
        what=("Migra un sistema de facturación heredado siguiendo una especificación de mapeo, unifica duplicados y cierra con doce controles de conciliación.",
              "Moves a legacy billing system following a mapping spec, merges duplicates and closes with twelve reconciliation checks."),
        runs=("Cada corrida repite los doce controles y deja cada registro con su destino o con el motivo por el que quedó afuera.",
              "Every run repeats the twelve checks and traces each record to its target or to the reason it was left out."),
        figs=[("12", "12", "controles en cada corrida", "checks on every run"),
              ("4.060 · 6.500", "4,060 · 6,500", "clientes y contratos de prueba", "test customers and contracts")],
        links=[("proyectos/migracion-de-datos.html", "Leer el caso", "Read the case", "case"),
               (GH + "/data-migration-toolkit", "Código", "Code", "code")],
    ),
    dict(
        chips=[("", "Repositorio público", "Public repository"), ("", "GitHub", "GitHub")],
        title=("searchedby-engineering", "searchedby-engineering"),
        what=("La parte pública de la ingeniería de SearchedBy: cómo se prueba, cómo se despliega y cómo se controla. El código del producto sigue siendo privado.",
              "The public side of SearchedBy's engineering: how it is tested, deployed and checked. The product code stays private."),
        runs=("Es la referencia de los sistemas de esta página, no un proceso que corra.",
              "It is the reference for the systems on this page, not a process that runs."),
        figs=[],
        links=[(ENG_REPO, "Abrir en GitHub", "Open on GitHub", "code")],
    ),
]


def system_card(s) -> str:
    chips = "".join(f'<span class="chip{(" " + c) if c else ""}">{bi(es, en) if es != en else es}</span>' for c, es, en in s["chips"])
    figs = ""
    if s["figs"]:
        figs = '<ul class="sys-figs">' + "".join(
            f"<li><b>{bi(ve, vn) if ve != vn else ve}</b><span>{bi(le, ln)}</span></li>" for ve, vn, le, ln in s["figs"]) + "</ul>"
    links = []
    for href, les, len_, kind in s["links"]:
        icon = ICON_GH if kind == "code" else ICON_NEXT
        cls = "btn btn-brand" if kind == "case" else "btn"
        ext = ' rel="noopener"' if href.startswith("http") else ""
        links.append(f'<a class="{cls}" href="{href}"{ext}>{icon}{bi(les, len_)}</a>')
    t_es, t_en = s["title"]
    title = f'<h2 lang="es">{t_es}</h2><h2 lang="en">{t_en}</h2>' if t_es != t_en else f"<h2>{t_es}</h2>"
    return f"""<article class="sys-card{' feature' if s.get('feature') else ''}">
  <div class="sys-top">{chips}</div>
  {title}
  <div><span class="v-label">{bi('Qué hace', 'What it does')}</span><p lang="es">{s['what'][0]}</p><p lang="en">{s['what'][1]}</p></div>
  <div class="sys-run"><span class="v-label">{bi('Qué corre solo', 'What runs on its own')}</span><p lang="es">{s['runs'][0]}</p><p lang="en">{s['runs'][1]}</p></div>
  {figs}
  <div class="sys-links">{''.join(links)}</div>
</article>"""


def systems_page() -> str:
    cards = "\n".join(system_card(s) for s in SYSTEMS)
    return head("Systems I built and run", "systems") + "\n<main>\n" + hero(
        PAGES["systems.html"]["title"],
        "Cada tarjeta dice qué hace el sistema, qué parte corre sin mí y dónde leer el caso y el código. SearchedBy es un producto en uso; los demás casos usan datos sintéticos de empresas ficticias.",
        "Each card says what the system does, which part runs without me, and where to read the case and the code. SearchedBy is a product in use; the other cases use synthetic data from fictional companies.",
        extra=f'<div class="cs-actions"><a class="btn" href="status.html">{ICON["pulse"]}{bi("Ver el estado de cada sistema", "See the status of each system")}</a></div>',
    ) + f"""
<div class="container">
<div class="sys-grid">
{cards}
</div>
<div class="sys-foot">
  <p lang="es">La última corrida, lo que procesó, cuánto costó y si terminó bien: una página que se genera sola una vez por día desde los logs.</p>
  <p lang="en">Last run, what it processed, what it cost and whether it worked: a page that rebuilds itself once a day from the logs.</p>
  <a class="btn btn-brand" href="status.html">{ICON_NEXT}{bi('Estado de los sistemas', 'Systems status')}</a>
</div>
</div>
</main>
""" + foot(bi("Los casos marcados usan datos sintéticos y empresas ficticias.", "Cases marked as such use synthetic data and fictional companies."))


# ------------------------------------------------------------------ /status
def status_page() -> str:
    return head("Systems status") + "\n<main>\n" + hero(
        PAGES["status.html"]["title"],
        "Los sistemas que corren de forma programada, con su última corrida, lo que procesaron, cuánto costó y si terminó bien. Un script en mi máquina lee los logs una vez por día y publica estos datos; nada se carga a mano.",
        "The systems that run on a schedule, with their last run, what they processed, what it cost and whether it worked. A script on my machine reads the logs once a day and publishes this data; nothing is typed in by hand.",
        extra='<p class="st-meta" id="st-meta" hidden></p>',
    ) + f"""
<div class="container">
<div class="st-grid" id="st-grid" aria-live="polite">
  <p class="st-empty"><span lang="es">Los datos de estado no se pudieron cargar. El archivo está en <a href="assets/data/status.json">status.json</a>.</span><span lang="en">The status data could not be loaded. The file is at <a href="assets/data/status.json">status.json</a>.</span></p>
</div>
<p class="st-how" lang="es">Fuentes: el log de cada corrida, un chequeo público de salud de SearchedBy (un GET a /healthz), los archivos de estado que escriben otros sistemas y la fecha del último cambio de este sitio. Datos crudos: <a href="assets/data/status.json">status.json</a>. Generador: <a href="{STATUS_SRC}" rel="noopener">build_status.py</a>. Los sistemas y sus casos: <a href="systems.html">Sistemas</a>.</p>
<p class="st-how" lang="en">Sources: the log of each run, a public health check of SearchedBy (a GET to /healthz), status files written by other systems and the date of the last change to this site. Raw data: <a href="assets/data/status.json">status.json</a>. Generator: <a href="{STATUS_SRC}" rel="noopener">build_status.py</a>. The systems and their cases: <a href="systems.html">Systems</a>.</p>
</div>
</main>
""" + foot(scripts=("assets/js/shell.js", "assets/js/contact.js", "assets/js/status.js"))


# ------------------------------------------------------------------ /links
LINKS = [  # (href, icon, title es, title en, sub es, sub en, extra attrs)
    ("index.html", "web", "Sitio web", "Website", "Casos, dashboards en vivo y servicios · pablodpavon.com", "Case studies, live dashboards and services · pablodpavon.com", ' class="lk-main-link"'),
    ("systems.html", "sys", "Sistemas que construí", "Systems I built", "Qué hace cada uno y qué corre solo", "What each one does and what runs on its own", ""),
    ("status.html", "pulse", "Estado de los sistemas", "Systems status", "Última corrida, costo y estado", "Last run, cost and state", ""),
    ("https://searchedby.com/", "search", "SearchedBy", "SearchedBy", "Mi producto con IA, en beta abierta", "My AI product, in open beta", ' rel="noopener"'),
    ("https://github.com/pablodpavon", "gh", "GitHub", "GitHub", "github.com/pablodpavon", "github.com/pablodpavon", ' rel="noopener"'),
    ("https://www.linkedin.com/in/pablo-damian-pavon", "in", "LinkedIn", "LinkedIn", "linkedin.com/in/pablo-damian-pavon", "linkedin.com/in/pablo-damian-pavon", ' rel="noopener"'),
    ("https://www.upwork.com/freelancers/pablopavon", "up", "Upwork", "Upwork", "upwork.com/freelancers/pablopavon", "upwork.com/freelancers/pablopavon", ' rel="noopener"'),
    ("mailto:contact@pablodpavon.com", "mail", "Email", "Email", "contact@pablodpavon.com", "contact@pablodpavon.com", ""),
]

ARROW = '<svg class="lk-go" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14m-6-6 6 6-6 6"/></svg>'


def links_page() -> str:
    items = []
    for href, ic, tes, ten, ses, sen, attrs in LINKS:
        t = bi(tes, ten, "b") if tes != ten else f"<b>{tes}</b>"
        s = bi(ses, sen, "small") if ses != sen else f"<small>{ses}</small>"
        items.append(f'<li><a href="{href}"{attrs}><span class="lk-ic" aria-hidden="true">{ICON[ic]}</span>'
                     f'<span class="lk-t">{t}{s}</span>{ARROW}</a></li>')
    return head("Links", full_nav=False) + f"""<div class="lk-bar">
  <!--LANGSWITCH-->
  <button class="icon-btn" id="themeBtn" type="button" aria-label-es="Tema" aria-label-en="Theme"></button>
</div>
<main class="lk-main">
  <div class="lk-who">
    <span class="logo" aria-hidden="true">PP</span>
    <h1>Pablo Pavon</h1>
    <p lang="es">Senior Business &amp; Data Analyst freelance en Berlín. Construyo sistemas de IA y automatización que corren solos, con cada número verificado.</p>
    <p lang="en">Freelance Senior Business &amp; Data Analyst in Berlin. I build AI and automation systems that run on their own, with every number checked.</p>
  </div>
  <ul class="lk-list">
{chr(10).join('    ' + i for i in items)}
  </ul>
</main>
<footer class="lk-foot">© <span data-year>2026</span> Pablo Pavon · <a href="impressum.html">Impressum</a> · <a href="privacy.html">{bi('Privacidad', 'Privacy')}</a></footer>
<script src="assets/js/shell.js"></script>
</body>
</html>
"""


def build():
    src = ROOT / "src"
    (src / "systems.html").write_text(systems_page(), encoding="utf-8")
    (src / "status.html").write_text(status_page(), encoding="utf-8")
    (src / "links.html").write_text(links_page(), encoding="utf-8")
    print("wrote src/systems.html, src/status.html, src/links.html")


if __name__ == "__main__":
    build()
