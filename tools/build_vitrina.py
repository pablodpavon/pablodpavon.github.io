"""Build the bilingual sources of three pages added on 1-nov-2026 (vitrina, part B):

    src/systems.html  -> /systems.html  /es/systems.html   hub "Systems I built and run"
    src/status.html   -> /status.html   /es/status.html    Systems status, rendered from /assets/data/status.json
    src/links.html    -> /links.html    /es/links.html     short link-in-bio page for profiles and forms

and, since 15-nov-2026 (D231), the service page

    src/ai-process-review.html -> /ai-process-review.html  /es/ai-process-review.html   "AI process review" / "Procesos con IA"

and, since 19-nov-2026, the portfolio with every project grouped by kind (sources of its figures above portfolio_page)

    src/portfolio.html -> /portfolio.html  /es/portfolio.html   "Portfolio"

GitHub Pages also serves them without the extension (pablodpavon.com/links), so that is the address to share;
canonical URLs keep .html like the rest of the site. Called by tools/build_site.py, which writes the <head>.

Sources of the numbers on /systems (all already public on this site or verified on 1-nov-2026):
- 7,700+ tests (19-nov-2026, see /portfolio), 4 AI assistants, 98.1 %, 66 runs, 12 rules, 1,260 invoices, 12 checks, 4,060/6,500, 4 error types,
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
    "ai-process-review.html": {   # D231 (15-nov-2026): texts from Servicio_Optimizacion_IA/Borradores/Web_Procesos_con_IA_v1.md
        "title": {"en": "AI process review", "es": "Procesos con IA"},
        "seo_title": {"en": "AI process review for small teams | Pablo Pavon",
                      "es": "Procesos con IA para equipos chicos | Pablo Pavon"},
        "description": {"en": "I find the work your team repeats every month and hand it to AI with checks: a review, a plan, the setup, and one number per change.",
                        "es": "Encuentro el trabajo que tu equipo repite cada mes y lo paso a la IA con controles: diagnóstico, plan, implementación y un número por cambio."},
        "image_alt": {"en": "AI process review for small teams, by Pablo Pavon", "es": "Procesos con IA para equipos chicos, de Pablo Pavon"},
        "type": "WebPage",
        "service": {"en": "AI process review", "es": "Revisión de procesos con IA"},
        "published": "2026-11-15",
    },
    "portfolio.html": {   # 19-nov-2026: Web/Portfolio_proyectos_brief_v1.md
        "title": {"en": "Portfolio", "es": "Portfolio"},
        "seo_title": {"en": "Portfolio: AI projects, products and demos | Pablo Pavon",
                      "es": "Portfolio: proyectos con IA, productos y demos | Pablo Pavon"},
        "description": {"en": "What I've built with AI: a real pilot, products, 15+ automations I run, a prototype and demos, with what each one does and how it is checked.",
                        "es": "Lo que construí con IA: un piloto real, productos, más de 15 automatizaciones propias, un prototipo y demos, con lo que hace cada uno y cómo se controla."},
        "image_alt": {"en": "Portfolio of Pablo Pavon: AI projects, products and demos", "es": "Portfolio de Pablo Pavon: proyectos con IA, productos y demos"},
        "type": "CollectionPage",
        "published": "2026-11-19",
        "og": "portfolio",
    },
    "links.html": {
        "title": {"en": "Links", "es": "Links"},
        "description": {"en": "Pablo Pavon, freelance business analyst in Berlin, AI process automation for small teams: website, systems, SearchedBy, GitHub, LinkedIn, Upwork and email.",
                        "es": "Pablo Pavon, business analyst freelance en Berlín, procesos con IA para equipos chicos: sitio, sistemas, SearchedBy, GitHub, LinkedIn, Upwork y email."},
        "image_alt": {"en": "Links of Pablo Pavon", "es": "Links de Pablo Pavon"},
        "type": "WebPage",
    },
}
for _p in PAGES.values():
    _p.setdefault("published", PUBLISHED)

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
        a("ai-process-review.html", "Procesos", "Processes", "process"),
        a("index.html#servicios", "Servicios", "Services"),
        a("portfolio.html", "Portfolio", "Portfolio", "portfolio"),
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
        # HOY-6 (Pablo, 19-nov-2026): "ambos NexYn-AI como searchedBy son productos desarrollados por mi"
        chips=[("own", "Producto · lo desarrollé yo", "Product · developed by me"), ("", "Python", "Python"), ("", "FastAPI", "FastAPI"), ("", "LLM APIs", "LLM APIs")],
        title=("SearchedBy: cómo te presentan los asistentes de IA", "SearchedBy: how AI assistants present a business"),
        what=("Muestra a un negocio qué responden ChatGPT, Perplexity, Claude y la IA de Google cuando un cliente pregunta por su rubro, y qué le falta a su sitio para que lo citen.",
              "Shows a business what ChatGPT, Perplexity, Claude and Google's AI answer when a customer asks about its field, and what its site is missing to be cited."),
        runs=("Cada scan corre en dos procesos de fondo: uno lee el sitio y el otro les pregunta a los motores de IA. La salud del servicio se revisa todos los días en la página de estado.",
              "Each scan runs on two background workers: one reads the site, the other asks the AI engines. The service health is checked every day on the status page."),
        figs=[("7.700+", "7,700+", "tests antes de cada deploy", "tests before every deploy"),
              ("US$ 0,23", "US$ 0.23", "costo de IA de un scan completo reciente", "AI cost of a recent full scan"),
              ("4", "4", "asistentes de IA consultados", "AI assistants asked")],
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
        "Cada tarjeta dice qué hace el sistema, qué parte corre sin mí y dónde leer el caso y el código. SearchedBy es un producto en producción; los demás casos usan datos sintéticos de empresas ficticias.",
        "Each card says what the system does, which part runs without me, and where to read the case and the code. SearchedBy is a live product; the other cases use synthetic data from fictional companies.",
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


# ------------------------------------------------------------------ /ai-process-review (D231, 15-nov-2026)
# Texts: Servicio_Optimizacion_IA/Borradores/Web_Procesos_con_IA_v1.md (ES and EN, as written there). No prices,
# no unmeasured figures, the pilot client is anonymised ("a construction supervision firm in Israel").
ICON_CHAT = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12a8 8 0 0 1-11.6 7.1L4 20l1-4.6A8 8 0 1 1 21 12z"/><path d="M8.5 10.5h7M8.5 13.5h4"/></svg>'
# OP-P17 (NX-11a, D237): since nexyn-ai.com went live (19-nov-2026), this page sends companies to NexYn; the pilot case stays
# (NexYn names nobody outside its legal pages). Spanish goes to /es/, English to the root.
NEXYN_ES, NEXYN_EN = "https://nexyn-ai.com/es/", "https://nexyn-ai.com/"
ICON_DOWN = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 5v14m-6-6 6 6 6-6"/></svg>'

PR_FOR = [
    ("Equipos de 3 a 50 personas donde todo pasa por el dueño o por una sola persona.",
     "Teams of 3 to 50 people where everything goes through the owner or one person."),
    ("El mismo informe, liquidación o reporte se arma a mano todos los meses.",
     "The same report, statement or summary is built by hand every month."),
    ("La información del campo o de los clientes llega tarde, por WhatsApp o por mail, y alguien la ordena después.",
     "Information from the field or from clients arrives late, on WhatsApp or by email, and someone sorts it out later."),
    ("Hay varias planillas con el mismo dato, y ninguna está al día.",
     "Several spreadsheets hold the same data, and none is up to date."),
    ("Ya usan ChatGPT o Claude, pero cada uno a su manera, y nada avisa cuando algo falla.",
     "You already use ChatGPT or Claude, but everyone in their own way, and nothing tells you when something breaks."),
]

PR_STEPS = [
    ("Tu IA hace el inventario.", "Your AI does the inventory.",
     "Si ya usás Claude o ChatGPT, te paso una tarea para que tu propia IA escriba cómo trabajan hoy: procesos, planillas, automatizaciones, qué falló. Si no la usás, lo hacemos en una llamada de una hora.",
     "If you already use Claude or ChatGPT, I give you a task so your own AI writes down how you work today: processes, spreadsheets, automations, what broke. If you don't, we do it on a one-hour call."),
    ("Reviso área por área, y cada hallazgo se chequea.", "I review it area by area, and every finding is checked.",
     "Separo lo que funciona de lo que no, con la evidencia de tus propios archivos. Una segunda revisión independiente vuelve a mirar las conclusiones antes de que lleguen a vos.",
     "I separate what works from what doesn't, with evidence from your own files. A second, independent review checks the conclusions before they reach you."),
    ("Te doy pocas decisiones, no un informe eterno.", "You get a few decisions, not an endless report.",
     "Como máximo siete, cada una con una opción recomendada. Contestás \"ok 1, 3\" y tu IA aplica solo lo que aprobaste.",
     "Seven at most, each with a recommended option. You answer \"ok 1, 3\" and your AI applies only what you approved."),
    ("Lo dejamos andando y lo medimos.", "We set it up and measure it.",
     "Todo en un solo lugar, con los envíos bloqueados por defecto y un backup cada noche. Cada cambio lleva su número: cuánto tarda hoy y cuánto después.",
     "Everything in one place, sending blocked by default, and a backup every night. Every change has its number: how long it takes today and how long after."),
]

PR_PILOT = [
    ("el material de la obra llegaba días después;", "field material arrived days late;"),
    ("ninguna automatización avisaba cuando fallaba;", "no automation said when it failed;"),
    ("todo dependía de una sola computadora.", "everything depended on one computer."),
]

PR_FAQ = [
    ("¿Necesito Claude?", "Do I need Claude?",
     "No para empezar: trabajo con lo que ya usás. Para dejar todo ordenado en un solo lugar uso y recomiendo Claude Code, en tu cuenta y en tu computadora.",
     "Not to start: I work with what you use. To put everything in one place I use and recommend Claude Code, in your account and on your computer."),
    ("¿Qué pasa con mis datos y los de mis clientes?", "What about my data and my clients' data?",
     "No necesito contraseñas. El inventario se hace con los datos de terceros reemplazados, y lo que toca temas legales va como preguntas para tu abogado.",
     "I don't need passwords. The inventory is done with third-party details replaced, and anything legal goes as questions for your lawyer."),
    ("¿Cuánto tiempo me lleva a mí?", "How much of my time does it take?",
     "Contestar unas preguntas, pegar una tarea en tu IA y decidir. En la implementación, unas horas repartidas en dos o tres semanas.",
     "Answering a few questions, pasting one task into your AI, and deciding. During the setup, a few hours spread over two or three weeks."),
    ("¿Y si después no estás?", "What if you're not around later?",
     "Todo queda en tu cuenta, con backup y documentado para que lo siga otra persona.",
     "Everything stays in your account, backed up and documented so someone else can carry on."),
    ("¿Cuánto cuesta?", "What does it cost?",
     "Precio fijo por etapa, acordado por escrito antes de empezar.",
     "A fixed price per stage, agreed in writing before we start."),
]

PR_TOC = [("para-quien", "Para quién es", "Who it is for"), ("como-trabajo", "Cómo trabajo", "How I work"),
          ("que-no-automatizo", "Qué no automatizo", "What I don't automate"), ("caso-piloto", "Caso piloto", "Pilot case"),
          ("preguntas", "Preguntas frecuentes", "FAQ")]


def process_page() -> str:
    def ul(items):
        return ('<ul lang="es">' + "".join(f"<li>{es}</li>" for es, _ in items) + "</ul>"
                + '<ul lang="en">' + "".join(f"<li>{en}</li>" for _, en in items) + "</ul>")

    def h2(es, en):
        return f'<h2 lang="es">{es}</h2><h2 lang="en">{en}</h2>'

    toc = "\n".join(f'      <a href="#{i}">{bi(es, en)}</a>' for i, es, en in PR_TOC)
    steps = "".join(f"<div><b>{bi(tes, ten)}</b><span>{bi(des, den)}</span></div>" for tes, ten, des, den in PR_STEPS)
    faq = "".join(f'<details><summary>{bi(qes, qen)}<i aria-hidden="true"></i></summary>'
                  f'<div class="a"><p lang="es">{aes}</p><p lang="en">{aen}</p></div></details>' for qes, qen, aes, aen in PR_FAQ)
    hero_html = f"""<section class="cs-hero v-hero">
  <div class="mesh" aria-hidden="true"><span></span><span></span><span></span><span></span></div>
  <div class="grid-bg" aria-hidden="true"></div>
  <div class="container">
    <a class="cs-back" href="index.html">{ICON_BACK}{bi('Inicio', 'Home')}</a><br>
    <span class="pill"><span class="dot"></span>{bi('Procesos con IA · Diagnóstico · Implementación', 'AI process review · Diagnostic · Setup')}</span>
    <h1 lang="es" style="max-width:22ch">Encuentro el trabajo que tu equipo repite todos los meses y se lo paso a la IA, con controles.</h1><h1 lang="en" style="max-width:22ch">I find the work your team repeats every month and hand it to AI, with checks.</h1>
    <p class="lede" lang="es">Informes, planillas, mails, seguimientos, fotos y audios que llegan por WhatsApp. Reviso cómo trabaja tu equipo, automatizo con IA la parte repetitiva y la dejo andando y medida. Así tu gente usa su tiempo en lo que la IA no hace: criterio, conocimiento del negocio y la relación con tus clientes.</p><p class="lede" lang="en">Reports, spreadsheets, emails, follow-ups, photos and voice notes arriving on WhatsApp. I look at how your team works, automate the repetitive part with AI, and leave it running and measured. Your people keep their time for what AI doesn't do: judgement, knowledge of the business and your client relationships.</p>
    <div class="v-nexyn"><p lang="es"><strong>Para empresas, este servicio ahora está en NexYn:</strong> automatización de procesos con o sin IA, con el mismo método que se cuenta abajo.</p><p lang="en"><strong>For companies, this service now lives at NexYn:</strong> process automation with or without AI, with the same method described below.</p></div>
    <div class="cs-actions"><a class="btn btn-brand" lang="es" href="{NEXYN_ES}" rel="noopener">{ICON_NEXT}Ir a NexYn</a><a class="btn btn-brand" lang="en" href="{NEXYN_EN}" rel="noopener">{ICON_NEXT}Go to NexYn</a><a class="btn" href="#como-trabajo">{ICON_DOWN}{bi('Ver cómo trabajo', 'See how I work')}</a></div>
  </div>
</section>
"""
    return head("AI process review for small teams", "process") + "\n<main>\n" + hero_html + f"""
<div class="container">
  <div class="cs-body">
    <nav class="toc" aria-label-es="Contenido" aria-label-en="Contents">
{toc}
    </nav>
    <article class="prose">
<section id="para-quien">
{h2('Para quién es', 'Who it is for')}
{ul(PR_FOR)}
</section>
<section id="como-trabajo">
{h2('Cómo trabajo', 'How I work')}
<div class="steps">{steps}</div>
</section>
<section id="que-no-automatizo">
{h2('Qué no automatizo', 'What I don\'t automate')}
<div class="callout"><span lang="es">Tu firma, el criterio profesional, los borrados ni los envíos a tus clientes sin tu OK. La IA prepara y avisa; decide una persona.</span><span lang="en">Your signature, professional judgement, deletions, or anything sent to your clients without your OK. AI prepares and flags; a person decides.</span></div>
</section>
<section id="caso-piloto">
{h2('Caso piloto', 'Pilot case')}
<p lang="es">Una firma de supervisión de obra en Israel que entrega un informe técnico mensual por obra. Su IA hizo el inventario en unas doce horas. La revisión encontró lo que andaba bien, el motor de informes, y lo que no:</p><p lang="en">A construction supervision firm in Israel that delivers a monthly technical report per site. Its AI did the inventory in about twelve hours. The review found what worked, the report engine, and what didn't:</p>
{ul(PR_PILOT)}
<p lang="es">Al día siguiente tenía siete decisiones y un plan por etapas. Los resultados medidos todavía no están; los publico cuando existan.</p><p lang="en">The next day the owner had seven decisions and a staged plan. Measured results are not in yet; I will publish them when they exist.</p>
</section>
<section id="preguntas">
{h2('Preguntas frecuentes', 'FAQ')}
<div class="faq">{faq}</div>
</section>
    </article>
  </div>
  <div class="sys-foot" style="margin-bottom:20px">
    <p lang="es"><strong>¿Tenés una empresa y querés empezar?</strong> El servicio sigue en NexYn: ahí contás qué tarea se repite más y te responden por escrito.</p>
    <p lang="en"><strong>Running a company and want to start?</strong> The service continues at NexYn: tell them which task repeats most and you get a written answer.</p>
    <a class="btn btn-brand" lang="es" href="{NEXYN_ES}" rel="noopener">{ICON_NEXT}Ir a NexYn</a><a class="btn btn-brand" lang="en" href="{NEXYN_EN}" rel="noopener">{ICON_NEXT}Go to NexYn</a>
  </div>
  <p class="st-how" lang="es">Si además querés saber cómo te encuentran en Google y en los asistentes de IA, mirá <a href="https://searchedby.com/" rel="noopener">SearchedBy</a>.</p>
  <p class="st-how" lang="en">If you also want to know how Google and AI assistants find you, see <a href="https://searchedby.com/" rel="noopener">SearchedBy</a>.</p>
</div>
</main>
""" + foot()


# ------------------------------------------------------------------ /portfolio (19-nov-2026)
# One page with every project, grouped by what it is: client work described without the client's name, my own
# products and tools, prototypes, demos on synthetic data, and what I can build that I have not built for a client yet.
# Nothing invented: a real project keeps its full size, a demo says it is a demo, an offer says it is an offer.
# Sources of the figures (checked on 19-nov-2026):
# - pilot: ~12 h and 7 decisions, already public on /ai-process-review; 25 claims, 21 confirmed and 4 corrected by an
#   independent check before delivery (work log of 15-nov-2026).
# - migration: 116 sessions on one computer and ~80 pastes in the first plan (independent review, 15-nov-2026).
# - SearchedBy: 7,700+ tests (2,961 webapp + 4,819 pipeline in release v10c, 18-nov-2026; more in v10d);
#   21 automated checks and the four assistants: the public home of https://searchedby.com/ (19-nov-2026).
# - control tower: 13 projects in its database (19-nov-2026).
# - KPI report: 4 error types, as in its case study; the runs themselves are on /status.
# - own automations: 15 recurring scheduled tasks + 2 LaunchAgents (19-nov-2026); the four cards follow their prompts.
#   The personal-finance task stays out (its prompt says the data is private).
# - field app: 230 tests (npm test, 19-nov-2026) and a 36-screen check as a new phone (18-nov-2026).
ICON_EXT = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 4h6v6M20 4l-9 9"/><path d="M18 14v5a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V7a1 1 0 0 1 1-1h5"/></svg>'

PF_KIND = {  # chip class, es, en
    "client": ("cli", "Piloto real, sin nombre", "Real pilot, unnamed"),
    "own": ("own", "Lo construí", "Built by me"),
    "proto": ("pro", "Prototipo", "Prototype"),
    "syn": ("syn", "Datos sintéticos", "Synthetic data"),
}

PF_CLIENT = [
    dict(
        id="piloto", kind="client", status=("Diagnóstico entregado", "Diagnostic delivered"), stack=["Claude", "Claude Code"],
        title=("Revisión de procesos con IA para una firma de supervisión de obra",
               "AI process review for a construction supervision firm"),
        what=("Una firma de Israel que entrega un informe técnico mensual por cada obra. Su propia IA escribió el inventario de cómo trabajan, a partir de una tarea que le pasé, en unas doce horas. Al día siguiente el dueño tenía siete decisiones y un plan por etapas.",
              "A firm in Israel that delivers a monthly technical report for each site. Its own AI wrote the inventory of how the team works, from a task I sent, in about twelve hours. The next day the owner had seven decisions and a staged plan."),
        checks=("Antes de entregar, una verificación independiente revisó las 25 afirmaciones principales contra los archivos de la firma: 21 se confirmaron y 4 se ajustaron en la redacción. Lo que tocaba temas legales salió como preguntas para su abogado.",
                "Before delivery, an independent check tested the 25 main claims against the firm's own files: 21 were confirmed and 4 were reworded. Anything legal went out as questions for their lawyer."),
        figs=[("~12 h", "~12 h", "hasta tener el inventario de su propia IA", "until its own AI's inventory was ready"),
              ("7", "7", "decisiones, al día siguiente", "decisions, the next day"),
              ("25", "25", "afirmaciones verificadas antes de entregar", "claims checked before delivery")],
        links=[("ai-process-review.html#caso-piloto", "Leer el caso piloto", "Read the pilot case", "case")],
    ),
    dict(
        id="migracion", kind="client", status=("En curso", "In progress"), stack=["Claude Code", "Google Docs"],
        title=("La IA de todo un equipo, pasada a un solo proyecto de Claude Code",
               "A whole team's AI work, moved into one Claude Code project"),
        what=("Para la misma firma. El plan pasa sus chats, sus proyectos de Claude, las tareas de Cowork y 116 sesiones guardadas en una computadora a un solo proyecto de Claude Code, con una carpeta por área. Cuando una conversación se llena, deja escrito su traspaso y sigue en una nueva.",
              "For the same firm. The plan moves its chats, its Claude projects, the Cowork tasks and 116 sessions stored on one computer into a single Claude Code project, with a folder per area. When a conversation fills up, it writes its handover and carries on in a new one."),
        checks=("El plan bloquea los borrados y deja una copia local desde el primer día. Una revisión independiente de la primera versión encontró que le pedía al dueño unas 80 pegadas de texto; la rehice para que la IA escriba la mayoría de los traspasos a partir del historial y de la exportación de datos.",
                "The plan blocks deletions and keeps a local copy from day one. An independent review of the first version found it asked the owner for about 80 text pastes; I rebuilt it so the AI writes most handovers from the history and the data export."),
        figs=[],
        links=[],
        note=("En curso: lo cuento entero cuando termine.", "In progress: I will write it up in full when it is done."),
    ),
]

PF_OWN = [
    dict(
        id="searchedby", kind="own", kind_label=("Producto", "Product"), status=("En producción", "Live"),
        stack=["Python", "FastAPI", "Stripe", "LLM APIs"],
        title=("SearchedBy: qué dicen las IA cuando alguien busca lo que vendés",
               "SearchedBy: what AI assistants say when someone looks for what you sell"),
        what=("Un chequeo gratis que les hace a ChatGPT, Perplexity, Claude y la IA de Google las preguntas que haría un cliente, y muestra si nombran a tu negocio o a tu competencia. Después ofrece un informe pago, que se cobra con Stripe. Lo diseñé y lo desarrollé con Claude Code; hoy se vende junto con NexYn, el otro producto que desarrollé.",
              "A free check that asks ChatGPT, Perplexity, Claude and Google's AI the questions a customer would ask, and shows whether they name your business or your competitors. It then offers a paid report, charged through Stripe. I designed and developed it with Claude Code; today it is sold together with NexYn, the other product I developed."),
        checks=("Antes de cada versión corren más de 7.700 pruebas automáticas, y las subidas se ensayan primero en una copia descartable, con la vuelta atrás incluida. Cada seis horas, otra tarea revisa los resultados nuevos sin gastar en las APIs y marca cualquier error grave; una persona del equipo los revisa igual.",
                "More than 7,700 automated tests run before every release, and releases are rehearsed first on a throwaway copy, rollback included. Every six hours, another task reviews the new results without spending on the APIs and flags any serious error; a person on the team reviews them too."),
        figs=[("7.700+", "7,700+", "pruebas automáticas antes de cada versión", "automated tests before every release"),
              ("21", "21", "controles automáticos en el chequeo gratis", "automated checks in the free scan"),
              ("4", "4", "asistentes de IA consultados", "AI assistants asked")],
        links=[("https://searchedby.com/", "Abrir SearchedBy", "Open SearchedBy", "ext"),
               ("proyectos/geo-scan.html", "Leer el caso", "Read the case", "case"),
               ("proyectos/ai-systems-operating-model.html", "Cómo lo construyo", "How I build it", "go")],
        feature=True,
    ),
    dict(
        id="nexyn", kind="own", kind_label=("Producto", "Product"), status=("En línea desde el 19-nov", "Live since 19 Nov"),
        stack=["Python", "Cloudflare Workers", "Claude Code"],
        title=("NexYn: automatización de procesos para pymes, con o sin IA",
               "NexYn: process automation for small businesses, with or without AI"),
        what=("Un sitio y un servicio para empresas de 3 a 50 personas, de cualquier país: primera lectura gratis por escrito en 48 horas hábiles, diagnóstico y armado en la cuenta del cliente. Lo desarrollé yo y está en línea en español e inglés desde el 19 de noviembre.",
              "A website and a service for companies of 3 to 50 people, in any country: a free first reading in writing within 48 business hours, a diagnostic, and the setup in the client's own account. I developed it, and it has been live in Spanish and English since 19 November."),
        checks=("196 pruebas automáticas en el sitio, una prueba que impide publicar precios y nada se envía ni se borra sin el OK del cliente.",
                "196 automated tests on the site, a test that blocks publishing prices, and nothing is sent or deleted without the client's OK."),
        figs=[("196", "196", "pruebas automáticas", "automated tests"),
              ("48 h", "48 h", "hábiles para la primera lectura gratis", "business hours for the free first reading")],
        links=[((NEXYN_ES, NEXYN_EN), "Abrir NexYn", "Open NexYn", "ext")],
        feature=True,
    ),
    dict(
        id="torre", kind="own", kind_label=("Herramienta propia", "My own tool"), status=("En uso diario", "In daily use"),
        stack=["Claude", "Claude Code"],
        title=("Una torre de control para varias sesiones de IA a la vez",
               "A control tower for many AI sessions at once"),
        what=("Un tablero privado donde veo, proyecto por proyecto, qué tiene abierto cada sesión de IA, qué me toca a mí y qué espera de otra persona. Las decisiones se contestan con un botón, y la respuesta le llega a la sesión que preguntó.",
              "A private dashboard where I see, project by project, what each AI session has open, what is on me and what is waiting on someone else. Decisions are answered with one button, and the answer reaches the session that asked."),
        checks=("Cada sesión actualiza su tema antes de contestarme, y cada cambio lleva la versión que leyó, así dos sesiones no se pisan. Un botón vale solo para esa decisión y para nada más.",
                "Each session updates its topic before answering me, and every write carries the version it read, so two sessions never overwrite each other. A button counts for that one decision and nothing else."),
        figs=[("13", "13", "proyectos en un solo tablero", "projects on one board")],
        links=[],
        note=("Es privado: lo muestro en una llamada.", "It is private: I can show it on a call."),
    ),
    dict(
        id="reporte-kpi", kind="own", kind_label=("Sistema propio", "My own system"), status=("Corre solo cada lunes", "Runs every Monday"),
        stack=[("syn", "Datos sintéticos", "Synthetic data"), "Python"],
        title=("Un reporte de KPIs que redacta la IA y se frena si un número no cierra",
               "A KPI report drafted by AI that stops when a number is off"),
        what=("Cada lunes a las 7:30, una tarea programada genera la semana de una tienda ficticia, recalcula los KPIs y le pide a un modelo de lenguaje el comentario. Antes de publicarlo, prueba cada cifra contra los datos.",
              "Every Monday at 7:30, a scheduled job generates the week for a fictional store, recomputes the KPIs and asks a language model for the commentary. Before releasing it, it tests every figure against the data."),
        checks=("Antes de llamar al modelo, un control de la carga frena la semana si los datos vienen mal, por ejemplo un día cargado dos veces. Después, si una cifra del texto no existe, es de otra métrica o de otro período, o dice que algo subió cuando bajó, no se publica nada.",
                "Before the model is called, a load check stops the week if the data is wrong, for example a day loaded twice. Then, if a figure in the text does not exist, belongs to another metric or period, or says something rose when it fell, nothing is released."),
        figs=[("4", "4", "tipos de error que detecta", "error types it detects")],
        links=[("proyectos/reporte-con-ia.html", "Leer el caso", "Read the case", "case"),
               ("status.html", "Ver la última corrida", "See the last run", "go")],
    ),
]

PF_AUTO = [  # 19-nov-2026, Pablo: "subir más automatizaciones". Real scheduled tasks on his Mac (list_scheduled_tasks): 15 recurring
    # tasks plus 2 LaunchAgents (status page, KPI report). Job-search and LinkedIn tasks are left out on purpose.
    dict(
        id="plataformas", kind="own", kind_label=("Automatización propia", "My own automation"), status=("Dos veces por día", "Twice a day"),
        stack=["Claude Code", "Chrome", "Gmail"],
        title=("Las bandejas de clientes, revisadas solas", "Client inboxes, checked on their own"),
        what=("Dos veces por día, una tarea revisa los mensajes y pedidos de las plataformas de trabajo freelance y del mail. A cada novedad le pone un veredicto (responder, esperar, rechazar o posible estafa) con su motivo y, si conviene responder, deja el borrador listo.",
              "Twice a day, a task reads the messages and orders on the freelance platforms and in the mail. Each new item gets a verdict (reply, wait, decline or likely scam) with its reason and, when a reply makes sense, the draft is ready."),
        checks=("Solo lectura: no inicia sesión, no acepta ni envía nada, y frena ante cualquier verificación. Una respuesta sale recién cuando contesto \"ok\".",
                "Read-only: it doesn't log in, accept or send anything, and it stops at any verification check. A reply goes out only after I answer \"ok\"."),
        figs=[("4", "4", "plataformas en la web, más el mail", "platforms on the web, plus the mail")],
    ),
    dict(
        id="estado", kind="own", kind_label=("Automatización propia", "My own automation"), status=("Cada mañana", "Every morning"),
        stack=["Python", "GitHub Pages"],
        title=("Una página que dice si todo corrió", "A page that says whether everything ran"),
        what=("Cada mañana, un script lee los registros de los sistemas que corren solos y publica, para cada uno, la última corrida, lo que procesó, cuánto costó y si terminó bien. Nadie carga nada a mano.",
              "Every morning, a script reads the logs of the systems that run on their own and publishes, for each one, the last run, what it processed, what it cost and whether it worked. Nobody types anything in."),
        checks=("Un dato con más de 48 horas aparece marcado como viejo, y solo se publica desde la rama principal sin otros cambios pendientes, para que no se cuele nada más.",
                "Any figure older than 48 hours is flagged as stale, and it only publishes from the main branch with nothing else pending, so no other change slips through."),
        figs=[],
        links=[("status.html", "Ver la página de estado", "See the status page", "go")],
    ),
    dict(
        id="ferias", kind="own", kind_label=("Automatización propia", "My own automation"), status=("Cada lunes y dos veces por día", "Mondays and twice a day"),
        stack=["Claude Code", "Todoist", "Gmail"],
        title=("Ferias: buscar, anotar y seguir las respuestas", "Markets: find them, log them, follow up"),
        what=("Para un negocio chico que vende en ferias de Berlín. Cada lunes busca mercados y ferias nuevos, los anota con fecha y precio, crea hasta cinco tareas y deja hasta cinco mails de inscripción como borrador. Dos veces por día revisa las respuestas de organizadores y proveedores y avisa qué llegó.",
              "For a small business that sells at Berlin markets. Every Monday it looks for new markets and fairs, logs them with date and price, creates up to five tasks and leaves up to five sign-up emails as drafts. Twice a day it checks replies from organisers and suppliers and says what came in."),
        checks=("Nunca se inscribe, compra, completa formularios ni manda mensajes: busca, anota y prepara. El mail lo manda una persona.",
                "It never signs up, buys, fills in forms or sends messages: it searches, logs and prepares. A person sends the email."),
        figs=[],
    ),
    dict(
        id="memoria", kind="own", kind_label=("Automatización que uso", "An automation I run"), status=("Cada noche", "Every night"),
        stack=["Claude Code", ("Agentes", "Agents")],
        title=("Una memoria que se ordena sola de noche", "A memory that tidies itself every night"),
        what=("La configuré para que, a las 2 de la mañana, varios agentes lean las conversaciones de IA del día, sumen a la memoria de cada proyecto lo que se aprendió y corrijan lo que resultó falso. A la mañana, la IA arranca sabiendo lo de ayer.",
              "I set it up so that at 2 a.m. several agents read the day's AI conversations, add what was learned to each project's memory and fix what turned out to be wrong. In the morning, the AI starts out knowing what happened yesterday."),
        checks=("Hace un respaldo antes de tocar nada, nunca borra una nota, controla que no se cuele ninguna clave y deja en espera las reglas generales hasta mi OK.",
                "It backs up before touching anything, never deletes a note, checks that no key or password slips in, and holds general rules until I approve them."),
        figs=[],
    ),
]

PF_PROTO = [
    dict(
        id="app-de-campo", kind="proto", status=("Demo lista", "Demo ready"),
        stack=[("syn", "Datos sintéticos", "Synthetic data"), "JavaScript", "PWA"],
        title=("Una app de campo para inspecciones de obra", "A field app for site inspections"),
        what=("Dos apps que se instalan en el teléfono. La del inspector muestra las tareas de cada edificio, guarda fotos y notas de voz por tarea, manda reportes de problemas y sigue andando sin señal. En la demo, las dos apps comparten el teléfono: lo que manda el inspector aparece enseguida, ordenado, en la del dueño, que además le agrega tareas.",
              "Two apps that install on a phone. The inspector's app shows the tasks for each building, keeps photos and voice notes per task, sends problem reports and keeps working without signal. In the demo both apps share one phone: what the inspector sends shows up right away, in order, in the owner's app, which can also add tasks for the inspector."),
        checks=("230 pruebas automáticas y un recorrido de 36 pantallas como si fuera un teléfono nuevo. La demo usa datos inventados y no tiene servidor: lo que se carga queda en ese teléfono.",
                "230 automated tests and a 36-screen walkthrough as a brand-new phone. The demo uses invented data and has no server: whatever you enter stays on that phone."),
        figs=[("2", "2", "apps instalables", "installable apps"),
              ("230", "230", "pruebas automáticas", "automated tests")],
        links=[],
        note=("La muestro en una llamada, en la computadora o en tu teléfono.", "I can show it on a call, on a laptop or on your phone."),
        feature=True,
    ),
]

PF_DEMO_LINKS = ["proyectos/requirements-to-backlog.html", "proyectos/conciliacion-y-caja.html",
                 "proyectos/cuentas-a-pagar.html", "proyectos/migracion-de-datos.html"]


def pf_demos() -> list:
    by_link = {s["links"][0][0]: s for s in SYSTEMS}
    out = []
    for link in PF_DEMO_LINKS:
        s = by_link[link]
        links = list(s["links"])
        if not any(k == "code" for *_, k in links):      # the demo's code is public too
            links.append((GH + "/requirements-to-backlog", "Código", "Code", "code"))
        out.append(dict(id=link.split("/")[-1].removesuffix(".html"), kind="syn",
                        stack=[(es, en) if es != en else es for c, es, en in s["chips"] if c != "syn"],
                        title=s["title"], what=s["what"], figs=s["figs"], links=links))
    return out


PF_OFFERS = [  # title es, en, text es, en, (prefix es, link text es, prefix en, link text en, anchor or "")
    ("Una app para tu equipo en la calle", "An app for your team in the field",
     "Tareas, fotos y audios desde el teléfono, aunque no haya señal, y un panel para la oficina.",
     "Tasks, photos and voice notes from the phone, even without signal, and a dashboard for the office.",
     ("Sale de la ", "app de campo", "Built from ", "the field app", "app-de-campo")),
    ("Un tablero para las IA de tu equipo", "A dashboard for your team's AI",
     "Si usan varias sesiones de IA, un solo lugar para ver qué tiene abierto cada una y decidir con un botón.",
     "If you run several AI sessions, one place to see what each one has open and to decide with a button.",
     ("Sale de la ", "torre de control", "Built from ", "the control tower", "torre")),
    ("Presupuestos en minutos", "Quotes in minutes",
     "Una planilla donde marcás qué hay que hacer y arma la cotización con tus tarifas. Vos la revisás y la mandás.",
     "A spreadsheet where you tick what needs doing and it builds the quote with your rates. You review it and send it.",
     ("Sale de una planilla de cotización de arreglos web que ya armé", "", "Built from a quote sheet for website fixes I already built", "", "")),
    ("Tu IA, en un solo lugar", "One place for your AI work",
     "Chats, proyectos y tareas de Claude o ChatGPT en un solo proyecto, con backup cada noche y envíos bloqueados por defecto.",
     "Chats, projects and tasks from Claude or ChatGPT in one project, with a nightly backup and sending blocked by default.",
     ("Sale de la ", "migración en curso", "Built from ", "the migration in progress", "migracion")),
    ("Informes que se frenan si algo no cierra", "Reports that stop when something is off",
     "El informe mensual que hoy armás a mano, redactado por la IA y controlado número por número antes de salir.",
     "The monthly report you build by hand today, drafted by AI and checked number by number before it goes out.",
     ("Sale del ", "reporte de KPIs", "Built from ", "the KPI report", "reporte-kpi")),
    ("Tu mail, leído y ordenado", "Your inbox, read and sorted",
     "Facturas, vencimientos y pedidos de clientes anotados solos, con la acción sugerida y el borrador listo para que vos decidas.",
     "Invoices, due dates and client requests logged on their own, with the suggested action and a draft ready for you to decide.",
     ("Sale de ", "mis propias revisiones de mail", "Built from ", "my own mail checks", "plataformas")),
    ("Un radar de oportunidades", "An opportunity radar",
     "Cada semana busca clientes, licitaciones o eventos de tu rubro, los anota con su fecha y deja listo el primer mail.",
     "Every week it looks for clients, tenders or events in your field, logs them with their date and drafts the first email.",
     ("Sale del ", "radar de ferias", "Built from ", "the markets radar", "ferias")),
    ("Respuestas a clientes, en borrador", "Client replies, drafted",
     "Cada consulta nueva con un veredicto y una respuesta preparada. Vos la leés y la mandás con un \"ok\".",
     "Every new enquiry with a verdict and a prepared reply. You read it and send it with an \"ok\".",
     ("Sale de la ", "revisión de las bandejas de clientes", "Built from ", "the client-inbox check", "plataformas")),
    ("Requerimientos que el equipo de sistemas puede construir", "Requirements IT can build from",
     "De una reunión grabada a user stories con criterios de aceptación, cada una con la frase de la que sale.",
     "From a recorded meeting to user stories with acceptance criteria, each one quoting the sentence it comes from.",
     ("Sale de la ", "demo de requerimientos a backlog", "Built from ", "the requirements-to-backlog demo", "requirements-to-backlog")),
]

PF_GROUPS = [  # id, kicker es, en, heading es, en, intro es, en, items
    ("piloto-real", "Piloto real", "Real pilot",
     "Trabajo real, contado sin el nombre de la firma.", "Real work, described without the firm's name.",
     "Qué se hizo, con qué y cómo se controló. Los resultados medidos se publican cuando existan.",
     "What was done, with what, and how it was checked. Measured results get published once they exist.", PF_CLIENT),
    ("construidos", "Productos y herramientas que construí", "Products and tools I built",
     "Lo que construí y sigue andando.", "Things I built that keep running.",
     "Están en producción, corren solos o los uso todos los días.",
     "They are live, run on their own, or I use them every day.", PF_OWN),
    ("automatizaciones", "Automatizaciones propias", "My own automations",
     "Más de 15 tareas que corren solas en mi computadora.", "More than 15 tasks that run on their own on my computer.",
     "Estas cuatro siguen la misma regla que aplico con clientes: leen, ordenan y preparan; enviar, pagar o borrar queda para una persona.",
     "These four follow the rule I apply for clients: they read, sort and prepare; sending, paying or deleting stays with a person.", PF_AUTO),
    ("prototipos", "Prototipos", "Prototypes",
     "Armado de verdad, todavía sin uso diario.", "Built for real, not in daily use yet.",
     "Funciona y la muestro en una llamada, pero todavía no la usa un equipo todos los días.",
     "It works and I can show it on a call, but no team uses it every day yet.", PF_PROTO),
    ("demos", "Demos con datos sintéticos", "Demos on synthetic data",
     "Casos completos, con el código publicado.", "Full case studies, with the code published.",
     "Empresas ficticias y datos inventados, para mostrar el método entero: contexto, enfoque, controles y entregables.",
     "Fictional companies and invented data, to show the whole method: context, approach, checks and deliverables.", None),
]


def pf_chip(cls, es, en) -> str:
    return f'<span class="chip{(" " + cls) if cls else ""}">{bi(es, en) if es != en else es}</span>'


def pf_card(it) -> str:
    cls, kes, ken = PF_KIND[it["kind"]]
    if it.get("kind_label"):
        kes, ken = it["kind_label"]
    chips = [pf_chip(cls, kes, ken)]
    if it.get("status"):
        chips.append(pf_chip("st", *it["status"]))
    for s in it.get("stack", []):
        if isinstance(s, tuple):
            chips.append(pf_chip(*s) if len(s) == 3 else pf_chip("", *s))
        else:
            chips.append(pf_chip("", s, s))
    t_es, t_en = it["title"]
    title = f'<h3 lang="es">{t_es}</h3><h3 lang="en">{t_en}</h3>' if t_es != t_en else f"<h3>{t_es}</h3>"
    checks = ""
    if it.get("checks"):
        checks = (f'<div class="sys-run"><span class="v-label">{bi("Controles", "Checks")}</span>'
                  f'<p lang="es">{it["checks"][0]}</p><p lang="en">{it["checks"][1]}</p></div>')
    figs = ""
    if it.get("figs"):
        figs = '<ul class="sys-figs">' + "".join(
            f"<li><b>{bi(ve, vn) if ve != vn else ve}</b><span>{bi(le, ln)}</span></li>" for ve, vn, le, ln in it["figs"]) + "</ul>"
    links = []
    for href, les, len_, kind in it.get("links", []):
        icon = {"code": ICON_GH, "ext": ICON_EXT}.get(kind, ICON_NEXT)
        btn = "btn btn-brand" if kind == "case" else "btn"
        if isinstance(href, tuple):               # one address per language (es, en)
            links.append(f'<a class="{btn}" lang="es" href="{href[0]}" rel="noopener">{icon}{les}</a>'
                         f'<a class="{btn}" lang="en" href="{href[1]}" rel="noopener">{icon}{len_}</a>')
            continue
        rel = ' rel="noopener"' if href.startswith("http") else ""
        links.append(f'<a class="{btn}" href="{href}"{rel}>{icon}{bi(les, len_)}</a>')
    tail = f'<div class="sys-links">{"".join(links)}</div>' if links else ""
    if it.get("note"):
        tail += f'<p class="pf-note" lang="es">{it["note"][0]}</p><p class="pf-note" lang="en">{it["note"][1]}</p>'
    return f"""<article class="sys-card pf-card{' feature' if it.get('feature') else ''}" id="{it['id']}">
  <div class="sys-top">{''.join(chips)}</div>
  {title}
  <p lang="es">{it['what'][0]}</p><p lang="en">{it['what'][1]}</p>
  {checks}
  {figs}
  {tail}
</article>"""


def portfolio_page() -> str:
    toc = [(g[0], g[1], g[2]) for g in PF_GROUPS] + [("puedo-armarte", "Lo que puedo armarte", "What I can build for you")]
    toc_html = '<nav class="pf-toc" aria-label-es="Secciones del portfolio" aria-label-en="Portfolio sections">' + "".join(
        f'<a href="#{i}">{bi(es, en)}</a>' for i, es, en in toc) + "</nav>"
    legend = ('<div class="pf-legend">' + "".join(pf_chip(c, es, en) for c, es, en in PF_KIND.values()) + "</div>"
              + '<p class="pf-legend-note" lang="es">El piloto real va sin el nombre de la firma; las demos usan datos sintéticos de empresas ficticias y lo dicen.</p>'
              + '<p class="pf-legend-note" lang="en">The real pilot is described without the firm\'s name; demos use synthetic data from fictional companies and say so.</p>')
    groups = []
    for gid, kes, ken, hes, hen, ies, ien, items in PF_GROUPS:
        cards = "\n".join(pf_card(it) for it in (items if items is not None else pf_demos()))
        groups.append(f"""<section class="pf-group" id="{gid}">
  <div class="pf-head">
    <div class="kicker">{bi(kes, ken)}</div>
    <h2 lang="es">{hes}</h2><h2 lang="en">{hen}</h2>
    <p lang="es">{ies}</p><p lang="en">{ien}</p>
  </div>
  <div class="sys-grid">
{cards}
  </div>
</section>""")
    offers = []
    for tes, ten, pes, pen, (pre_es, les, pre_en, len_, anchor) in PF_OFFERS:
        src_es = pre_es + (f'<a href="#{anchor}">{les}</a>' if anchor else les)
        src_en = pre_en + (f'<a href="#{anchor}">{len_}</a>' if anchor else len_)
        offers.append(f"""<div class="pf-offer">
  <h3 lang="es">{tes}</h3><h3 lang="en">{ten}</h3>
  <p lang="es">{pes}</p><p lang="en">{pen}</p>
  <small lang="es">{src_es}.</small><small lang="en">{src_en}.</small>
</div>""")
    return head("Portfolio", "portfolio") + "\n<main>\n" + hero(
        {"es": "Lo que construí con IA, y cómo sé que funciona.", "en": "What I've built with AI, and how I know it works."},
        "Si en tu empresa alguien hace a mano lo mismo todas las semanas, te armo un sistema que haga esa parte solo, con controles, para que esa persona use su tiempo y su cabeza en lo que pide criterio. Esto es lo que ya construí, con qué y cómo lo controlo.",
        "If someone at your company does the same thing by hand every week, I'll build a system that does that part on its own, with checks, so that person can spend their time and attention on what needs judgement. This is what I've already built, with what, and how I check it.",
        pill=("Portfolio · proyectos, productos y demos", "Portfolio · projects, products and demos"),
        extra=legend + toc_html,
    ) + f"""
<div class="container">
{chr(10).join(groups)}
<section class="pf-group" id="puedo-armarte">
  <div class="pf-head">
    <div class="kicker">{bi('Lo que puedo armarte', 'What I can build for you')}</div>
    <h2 lang="es">Lo que puedo armarte con piezas que ya funcionan.</h2><h2 lang="en">What I can build from parts that already work.</h2>
    <p lang="es">Son ofertas, no casos hechos: cada una sale de algo que ya existe.</p><p lang="en">These are offers, not finished cases: each one comes from something that already exists.</p>
  </div>
  <div class="pf-offers">
{chr(10).join(offers)}
  </div>
</section>
<div class="sys-foot">
  <p lang="es"><strong>¿Qué hace tu equipo a mano todas las semanas?</strong> Contámelo en dos líneas y te digo qué parte puede hacer un sistema solo.</p>
  <p lang="en"><strong>What does your team do by hand every week?</strong> Tell me in two lines and I'll tell you which part a system can do on its own.</p>
  <button class="btn btn-brand" type="button" data-open-contact>{ICON_CHAT}{bi('Escribime', 'Message me')}</button>
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
    ("index.html", "web", "Sitio web", "Website", "Servicios, casos y cómo trabajo · pablodpavon.com", "Services, case studies and how I work · pablodpavon.com", ' class="lk-main-link"'),
    ("systems.html", "sys", "Sistemas que construí", "Systems I built", "Qué hace cada uno y qué corre solo", "What each one does and what runs on its own", ""),
    ("status.html", "pulse", "Estado de los sistemas", "Systems status", "Última corrida, costo y estado", "Last run, cost and state", ""),
    ("portfolio.html", "web", "Portfolio", "Portfolio", "Proyectos, productos y demos", "Projects, products and demos", ""),
    ("https://searchedby.com/", "search", "SearchedBy", "SearchedBy", "Producto con IA que desarrollé", "An AI product I developed", ' rel="noopener"'),
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
    <p lang="es">Business analyst freelance en Berlín. Encuentro el trabajo que tu equipo repite todos los meses y se lo paso a la IA, con controles.</p>
    <p lang="en">Freelance business analyst in Berlin. I find the work your team repeats every month and hand it to AI, with checks.</p>
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
    (src / "ai-process-review.html").write_text(process_page(), encoding="utf-8")
    (src / "portfolio.html").write_text(portfolio_page(), encoding="utf-8")
    print("wrote src/systems.html, src/status.html, src/links.html, src/ai-process-review.html, src/portfolio.html")


if __name__ == "__main__":
    build()
