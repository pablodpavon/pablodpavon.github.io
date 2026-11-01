"""Build the bilingual sources of the legal pages: src/impressum.html and src/privacy.html (AJ-47, 1-nov-2026).

DRAFT, pending legal review (IT-Recht Kanzlei Schutzpaket, D148 2a). Not legal advice. The facts are the ones the site
really uses, checked in the code on 1-nov-2026: GitHub Pages (hosting), Cloudflare (DNS only, no proxy), FormSubmit (the
contact form, assets/js/contact.js), Zoho Mail (contact@pablodpavon.com), localStorage (theme and the unsent draft of the
form), self-hosted fonts and charts, no cookies, no analytics. The Impressum repeats the data of searchedby.com/legal/impressum.
The pages are noindex and stay out of the sitemap (tools/build_site.py): they are linked from every footer.
Run through tools/build_site.py (it calls build()).
"""
from pathlib import Path

from build_cases import bi

ROOT = Path(__file__).resolve().parents[1]
UPDATED = "2026-11-01"
NAME = "Pablo Pavon"
ADDRESS = "Zähringerstraße 24, 10707 Berlin, Germany"   # as on searchedby.com/legal/impressum (31-oct-2026)
EMAIL = "contact@pablodpavon.com"

PAGES = {
    "impressum.html": {
        "title": {"en": "Impressum (legal notice)", "es": "Impressum (aviso legal)"},
        "description": {"en": "Legal notice of pablodpavon.com under § 5 DDG: who runs this site and how to contact him.",
                        "es": "Aviso legal de pablodpavon.com según el § 5 DDG: quién está detrás de este sitio y cómo contactarlo."},
        "published": UPDATED,
    },
    "privacy.html": {
        "title": {"en": "Privacy notice", "es": "Aviso de privacidad"},
        "description": {"en": "What data pablodpavon.com processes when you visit it or write through the contact form, who processes it and your rights.",
                        "es": "Qué datos procesa pablodpavon.com cuando lo visitás o escribís por el formulario, quién los procesa y cuáles son tus derechos."},
        "published": UPDATED,
    },
}


def head(title_en):
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title_en} · Pablo Pavon · bilingual source</title>
<link rel="stylesheet" href="assets/css/site.css">
<script>(function(){{try{{var t=localStorage.getItem('theme');if(t)document.documentElement.setAttribute('data-theme',t);}}catch(e){{}}}})();</script>
</head>
<body data-base="">
<header class="nav">
  <div class="nav-inner">
    <a class="brand" href="index.html"><span class="logo">PP</span>Pablo Pavon</a>
    <div class="nav-tools">
      <!--LANGSWITCH-->
      <button class="icon-btn" id="themeBtn" type="button" aria-label-es="Tema" aria-label-en="Theme"></button>
    </div>
  </div>
</header>
"""


FOOT = f"""
<footer class="site"><div class="container"><div class="f-bot">
  <span>© <span data-year>2026</span> Pablo Pavon</span>
  <span class="f-legal"><a href="impressum.html">Impressum</a> · <a href="privacy.html">{bi('Privacidad', 'Privacy')}</a></span>
</div></div></footer>
<script src="assets/js/shell.js"></script>
</body>
</html>
"""


def doc(title, body):
    return head(title["en"]) + f"""
<main>
<section class="cs-hero"><div class="container">
  <h1 lang="es">{title['es']}</h1><h1 lang="en">{title['en']}</h1>
  <span class="cs-updated">{bi('Actualizado: 1 de noviembre de 2026', 'Updated: 1 November 2026')}</span>
</div></section>
<div class="container"><article class="prose">
{body}
</article></div>
</main>
""" + FOOT


def s(h_es, h_en, *paras):
    return f'<section>\n<h2 lang="es">{h_es}</h2><h2 lang="en">{h_en}</h2>\n' + "\n".join(
        f'<p lang="es">{es}</p><p lang="en">{en}</p>' for es, en in paras) + "\n</section>"


IMPRESSUM = "\n".join([
    s("Datos según el § 5 DDG", "Information under § 5 DDG",
      (f"{NAME}<br>{ADDRESS.replace('Germany', 'Alemania')}", f"{NAME}<br>{ADDRESS}")),
    s("Contacto", "Contact",
      (f'Email: <a href="mailto:{EMAIL}">{EMAIL}</a>', f'Email: <a href="mailto:{EMAIL}">{EMAIL}</a>')),
    s("Responsable del contenido según el § 18 (2) MStV", "Responsible for the content under § 18(2) MStV",
      (f"{NAME}, dirección como arriba.", f"{NAME}, address as above.")),
    s("Resolución de conflictos con consumidores", "Consumer dispute resolution",
      ("No estoy dispuesto ni obligado a participar en un procedimiento de resolución de conflictos ante una junta de arbitraje de consumo (§ 36 VSBG).",
       "I am neither willing nor obliged to take part in dispute resolution proceedings before a consumer arbitration board (§ 36 VSBG).")),
    s("Producto propio", "Own product",
      ('SearchedBy (<a href="https://searchedby.com/">searchedby.com</a>) tiene su propio <a href="https://searchedby.com/legal/impressum?lang=es">Impressum</a>.',
       'SearchedBy (<a href="https://searchedby.com/">searchedby.com</a>) has its own <a href="https://searchedby.com/legal/impressum?lang=en">Impressum</a>.')),
])

PRIVACY = "\n".join([
    s("1. Responsable", "1. Controller",
      (f'{NAME}, {ADDRESS.replace("Germany", "Alemania")} · <a href="mailto:{EMAIL}">{EMAIL}</a>.',
       f'{NAME}, {ADDRESS} · <a href="mailto:{EMAIL}">{EMAIL}</a>.')),
    s("2. Visitar el sitio", "2. Visiting the site",
      ("El sitio está alojado en GitHub Pages (GitHub, Inc., EE. UU.). Al pedir una página, GitHub procesa tu dirección IP, la hora, la dirección pedida y datos del navegador para entregar la página y proteger el servicio, y puede guardarlos en registros técnicos. Base legal: interés legítimo en publicar el sitio de forma segura (art. 6.1.f RGPD). GitHub puede tratar datos en EE. UU.; más información en su <a href=\"https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement\">declaración de privacidad</a>.",
       "The site is hosted on GitHub Pages (GitHub, Inc., USA). When you request a page, GitHub processes your IP address, the time, the address requested and browser details to deliver the page and protect the service, and may keep them in technical logs. Legal basis: legitimate interest in running the site securely (Art. 6(1)(f) GDPR). GitHub may process data in the USA; see its <a href=\"https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement\">privacy statement</a>."),
      ("Cloudflare solo resuelve el nombre del dominio (DNS); el tráfico de la página no pasa por Cloudflare. No hay cookies, ni herramientas de analítica, ni publicidad. Las fuentes y los gráficos se cargan desde este mismo sitio, no desde terceros.",
       "Cloudflare only resolves the domain name (DNS); the page traffic does not pass through Cloudflare. There are no cookies, no analytics and no advertising. Fonts and charts load from this site, not from third parties.")),
    s("3. En tu navegador", "3. In your browser",
      ("El sitio guarda en el almacenamiento local de tu navegador (localStorage) el tema que elegís (claro u oscuro) y el borrador de un mensaje que todavía no enviaste, para que no se pierda. No sale de tu navegador y lo podés borrar desde la configuración del navegador.",
       "The site keeps in your browser's local storage (localStorage) the theme you choose (light or dark) and the draft of a message you have not sent yet, so it is not lost. It never leaves your browser and you can delete it in your browser settings.")),
    s("4. Formulario de contacto y email", "4. Contact form and email",
      ("Si escribís por el formulario, tu nombre, tu email y tu mensaje se envían a FormSubmit (formsubmit.co), que los reenvía por email a mi casilla. Si escribís directamente, el email lo recibe mi proveedor de correo, Zoho Mail. Uso esos datos solo para responderte y, si hay un proyecto, para prepararlo. Base legal: medidas precontractuales a tu pedido (art. 6.1.b RGPD) o interés legítimo en responder (art. 6.1.f). Borro la conversación cuando ya no hace falta, salvo que la ley me obligue a guardarla.",
       "If you write through the form, your name, email and message go to FormSubmit (formsubmit.co), which forwards them by email to my inbox. If you write directly, the email is received by my mail provider, Zoho Mail. I use that data only to answer you and, if there is a project, to prepare it. Legal basis: steps you asked for before a contract (Art. 6(1)(b) GDPR) or legitimate interest in answering (Art. 6(1)(f)). I delete the conversation when it is no longer needed, unless the law requires me to keep it.")),
    s("5. Enlaces a otros sitios", "5. Links to other sites",
      ("Los enlaces a LinkedIn, GitHub, Upwork y SearchedBy abren sitios de terceros con sus propias reglas de privacidad. Este sitio no carga nada de ellos hasta que hacés clic.",
       "Links to LinkedIn, GitHub, Upwork and SearchedBy open third-party sites with their own privacy rules. This site loads nothing from them until you click.")),
    s("6. Tus derechos", "6. Your rights",
      ("Podés pedir acceso, rectificación, supresión, limitación del tratamiento y portabilidad de tus datos, y oponerte a un tratamiento basado en interés legítimo (arts. 15 a 21 RGPD), escribiendo al email de arriba. También podés reclamar ante una autoridad de protección de datos; la competente para mí es la Berliner Beauftragte für Datenschutz und Informationsfreiheit.",
       "You can ask for access, rectification, erasure, restriction and portability of your data, and object to processing based on legitimate interest (Arts. 15 to 21 GDPR), by writing to the email above. You can also complain to a data protection authority; the one responsible for me is the Berliner Beauftragte für Datenschutz und Informationsfreiheit.")),
])


def build():
    (ROOT / "src" / "impressum.html").write_text(doc(PAGES["impressum.html"]["title"], IMPRESSUM), encoding="utf-8")
    (ROOT / "src" / "privacy.html").write_text(doc(PAGES["privacy.html"]["title"], PRIVACY), encoding="utf-8")
    print("wrote src/impressum.html, src/privacy.html")


if __name__ == "__main__":
    build()
