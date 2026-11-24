"""Notes: English posts first published on LinkedIn, republished on the site (24-nov-2026).

    src/notes/notes.json        -> the data: one entry per post, in any order
    src/notes/index.html        -> /notes/              list of notes (written by this script)
    src/notes/<slug>.html       -> /notes/<slug>.html   one page per note (written by this script)

English only: tools/build_site.py writes these pages for "en" alone (no /es/ copy, no es hreflang).

notes.json is public, so it only ever holds posts that have already gone out on LinkedIn, each with
"on_linkedin": true (checked here as a second guard). "linkedin_url" is optional: when it is empty, the
"Originally posted on LinkedIn" line links to the profile's activity page.

To add a note: append its entry to notes.json and run `python3 tools/build_site.py`.
"""
from __future__ import annotations

import datetime as dt
import html
import json
import re
from pathlib import Path

from build_cases import ICON_BACK, ICON_NEXT, bi
import build_vitrina

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "src" / "notes" / "notes.json"
LINKEDIN_ACTIVITY = "https://www.linkedin.com/in/pablo-damian-pavon/recent-activity/all/"
ICON_OUT = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" '
            'stroke-linejoin="round" aria-hidden="true"><path d="M7 17 17 7M9 7h8v8"/></svg>')

INDEX_TITLE = "Notes"
INDEX_DESCRIPTION = ("Short notes by Pablo Pavon on what he builds with AI, how he checks it and what broke along the way. "
                     "Each one was first posted on LinkedIn.")


def esc(s: str) -> str:
    return html.escape(s, quote=False)


def all_notes() -> list[dict]:
    return json.loads(DATA.read_text(encoding="utf-8"))


def published() -> list[dict]:
    """Newest first. Only posts confirmed as gone out on LinkedIn."""
    notes = [n for n in all_notes() if n.get("on_linkedin") is True]
    seen = set()
    for n in notes:
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", n["slug"]) or n["slug"] in seen:
            raise SystemExit(f"notes.json: bad or repeated slug {n['slug']!r}")
        seen.add(n["slug"])
        dt.date.fromisoformat(n["date"])
    return sorted(notes, key=lambda n: (n["date"], n["slug"]), reverse=True)


def long_date(iso: str) -> str:
    d = dt.date.fromisoformat(iso)
    return f"{d.day} {d.strftime('%B')} {d.year}"


def short_date(iso: str) -> str:
    d = dt.date.fromisoformat(iso)
    return f"{d.day} {d.strftime('%b')} {d.year}"


def bare(url: str) -> str:
    return re.sub(r"^https?://(www\.)?", "", url).rstrip("/")


# ------------------------------------------------------------------ shell (subfolder: every path one level up)
def head(title: str, current: str = "") -> str:
    top = build_vitrina.head(title, current)
    top = top.replace('href="assets/', 'href="../assets/').replace('data-base=""', 'data-base="../"')
    top = top.replace('class="brand" href="index.html"', 'class="brand" href="../index.html"')
    nav = build_vitrina.nav(current)
    return top.replace(nav, re.sub(r'href="(?!https?:|#|/)', 'href="../', nav))


def foot() -> str:
    f = build_vitrina.foot(scripts=("../assets/js/shell.js", "../assets/js/contact.js"))
    return f.replace('href="impressum.html"', 'href="../impressum.html"').replace('href="privacy.html"', 'href="../privacy.html"')


def note_list(notes: list[dict]) -> str:
    rows = []
    for n in notes:
        rows.append(f"""  <li class="reveal"><a class="nt-item" href="{n['slug']}.html">
    <time datetime="{n['date']}">{short_date(n['date'])}</time>
    <div class="nt-txt"><h2>{esc(n["title"])}</h2><span class="nt-first">{esc(n["body"][0])}</span></div>
    <span class="nt-go" aria-hidden="true">{ICON_NEXT}</span>
  </a></li>""")
    return '<ol class="nt-list" reversed>\n' + "\n".join(rows) + "\n</ol>"


def portfolio_band() -> str:
    return f"""<div class="sys-band nt-band reveal">
  <div>
    <h3>What I build</h3>
    <p>Products, automations that run on their own and demos, with what each one does and how it is checked.</p>
  </div>
  <div class="row">
    <a class="btn btn-brand" href="../portfolio.html">{ICON_NEXT}See the portfolio</a>
  </div>
</div>"""


# ------------------------------------------------------------------ pages
def index_page(notes: list[dict]) -> str:
    return head("Notes") + f"""
<main>
<section class="cs-hero v-hero nt-hero">
  <div class="mesh" aria-hidden="true"><span></span><span></span><span></span><span></span></div>
  <div class="grid-bg" aria-hidden="true"></div>
  <div class="container">
    <a class="cs-back" href="../index.html">{ICON_BACK}{bi('Inicio', 'Home')}</a><br>
    <h1>{INDEX_TITLE}</h1>
    <p class="lede">Short notes on what I build with AI, how I check it and what broke along the way. Each one was first posted on LinkedIn.</p>
    <div class="cs-actions"><a class="btn" href="{LINKEDIN_ACTIVITY}" rel="noopener">{ICON_OUT}Follow on LinkedIn</a></div>
  </div>
</section>
<div class="container nt-wrap">
{note_list(notes)}
{portfolio_band()}
</div>
</main>
""" + foot()


def note_page(n: dict, notes: list[dict]) -> str:
    li = n.get("linkedin_url") or LINKEDIN_ACTIVITY
    paras = "\n".join(f"<p>{esc(p)}</p>" for p in n["body"])
    link = n["link"]
    link_html = (f'<p class="nt-link">{esc(link["lead"])}: <a href="{link["url"]}" rel="noopener">'
                 f'{esc(bare(link["url"]))}{ICON_OUT}</a></p>')
    upd = ""
    if n.get("update"):
        u = n["update"]
        see = ""
        target = next((m for m in notes if m["slug"] == u.get("see")), None)
        if target:
            see = f' More in <a href="{target["slug"]}.html">{esc(target["title"])}</a>.'
        upd = (f'<aside class="nt-update"><b>Update, {long_date(u["date"])}.</b> {esc(u["text"])}{see}</aside>')
    others = [m for m in notes if m["slug"] != n["slug"]][:3]
    more = ""
    if others:
        more = f'<section class="nt-more" aria-labelledby="more-notes"><h2 id="more-notes">More notes</h2>\n{note_list(others)}\n</section>'
    return head(n["title"]) + f"""
<main>
<section class="cs-hero v-hero nt-hero nt-hero-post">
  <div class="mesh" aria-hidden="true"><span></span><span></span><span></span><span></span></div>
  <div class="grid-bg" aria-hidden="true"></div>
  <div class="container">
    <a class="cs-back" href="index.html">{ICON_BACK}All notes</a><br>
    <h1>{esc(n['title'])}</h1>
    <p class="nt-origin">Originally posted on <a href="{li}" rel="noopener">LinkedIn</a> on <time datetime="{n['date']}">{long_date(n['date'])}</time>.</p>
  </div>
</section>
<div class="container nt-wrap">
<article class="nt-body">
{paras}
{link_html}
{upd}
</article>
{more}
{portfolio_band()}
</div>
</main>
""" + foot()


def build() -> list[dict]:
    notes = published()
    out = ROOT / "src" / "notes"
    out.mkdir(parents=True, exist_ok=True)
    keep = {"notes.json", "index.html"} | {n["slug"] + ".html" for n in notes}
    for old in out.glob("*.html"):            # a note taken back (on_linkedin false) disappears from the source too
        if old.name not in keep:
            old.unlink()
    (out / "index.html").write_text(index_page(notes), encoding="utf-8")
    for n in notes:
        (out / f"{n['slug']}.html").write_text(note_page(n, notes), encoding="utf-8")
    print(f"wrote src/notes/index.html and {len(notes)} note(s)")
    return notes


if __name__ == "__main__":
    build()
