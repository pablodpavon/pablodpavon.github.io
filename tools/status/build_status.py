"""Build assets/data/status.json, the data behind /status (Systems status).

Runs on Pablo's Mac (launchd, daily 09:30 Berlin), never on GitHub Actions: two of the sources are local files.
Stdlib only. Every source is independent: if one fails, the others are still published and the script exits 0.

Sources
(a) Scheduled LLM scoring pipeline: the last line written by the script (contains "Script (" and "US$") in the
    logs listed in the private config (outside this repository). Only the number of public sources, the items in
    scope, the cost, the duration and the date are published. Nothing else from that line leaves this machine.
(b) SearchedBy: one public GET to https://searchedby.com/healthz (only "ok" and the response time are published).
(c) Web/status_inputs/*.json written by other systems (contract in Web/status_inputs/README.md).
    Files whose name starts with "_" are examples and are ignored.
(d) The date of the last commit of this site, ignoring assets/data/status.json itself.

The published JSON never carries local paths, e-mail addresses, banned words or the raw log text; validate() enforces it.

Run:   python3 tools/status/build_status.py                 (writes assets/data/status.json)
       python3 tools/status/build_status.py --stdout        (print, write nothing)
Tests: python3 -m unittest discover -s tools/status -p "test_*.py"
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import ssl
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "assets" / "data" / "status.json"
UPWORK = Path.home() / "Documents" / "UpWork"
INPUTS = UPWORK / "Web" / "status_inputs"
# Local settings that must not be public (log locations, the list of words that may never be published) live
# outside the repository: {"pipeline_logs": ["/abs/path/log.md", ...], "banned": ["word", ...]}.
PRIVATE_CONFIG = UPWORK / "Web" / "status_private.json"
HEALTH_URL = "https://searchedby.com/healthz"
STALE_HOURS = 48
SCHEMA = 1


def load_private(path: Path = PRIVATE_CONFIG) -> tuple[list, tuple]:
    try:
        cfg = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return [], ()
    logs = [(Path(p).expanduser(), f"log {i + 1}") for i, p in enumerate(cfg.get("pipeline_logs", []))]
    return logs, tuple(str(w).lower() for w in cfg.get("banned", []))


# Pipeline logs in priority order (on a date tie the first wins) and banned words, checked case-insensitively
# over every published string.
RADAR_LOGS, BANNED = load_private()
PATH_RE = re.compile(r"(/Users/|/home/|~/|[A-Za-z]:\\\\|\.env\b)")
EMAIL_RE = re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+")

CONTRACT = {  # field: (type(s), required)
    "system": (str, True), "title_en": (str, True), "title_es": (str, True), "last_run_utc": (str, True),
    "ok": (bool, True), "items": ((int, float, type(None)), False), "items_label_en": (str, False),
    "items_label_es": (str, False), "cost_usd": ((int, float, type(None)), False),
    "schedule_en": (str, False), "schedule_es": (str, False), "note": (str, False),
}
RESERVED = {"scoring-pipeline", "searchedby", "website"}


def utc_now() -> dt.datetime:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0)


def iso(t: dt.datetime) -> str:
    return t.astimezone(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def parse_iso(s: str) -> dt.datetime | None:
    try:
        if re.fullmatch(r"\d{4}-\d{2}-\d{2}", s):
            return dt.datetime.fromisoformat(s).replace(tzinfo=dt.timezone.utc)
        t = dt.datetime.fromisoformat(s.replace("Z", "+00:00"))
        return t if t.tzinfo else t.replace(tzinfo=dt.timezone.utc)
    except (ValueError, AttributeError):
        return None


def warn(msg: str) -> None:
    print("status:", msg, file=sys.stderr)


def sentence(parts: list[str]) -> str:
    return (parts[0][:1].upper() + "; ".join(parts)[1:] + ".") if parts else ""


# ------------------------------------------------------------------ (a) scoring pipeline log
LINE_RE = re.compile(r"^(?P<date>\d{4}-\d{2}-\d{2}): (?P<sources>\d+) fuentes leídas, (?P<items>\d+) avisos")
COST_RE = re.compile(r"US\$ (?P<v>\d+(?:,\d+)?)")
DUR_RE = re.compile(r"duración (?:(?P<m>\d+) min )?(?P<s>\d+) s")
FAILS_RE = re.compile(r"fallas: (?P<f>.*?)\. Script \(")


def parse_radar_line(line: str) -> dict | None:
    """Return the publishable facts of one log line, or None if it is not a real script run."""
    line = line.strip()
    m = LINE_RE.match(line)
    if not m or "Script (" not in line or "SIMULADO" in line:
        return None
    script_part = line.split("Script (", 1)[1]
    if "costo FALTA" in script_part:
        cost = None
    else:
        c = COST_RE.search(script_part)
        if not c:
            return None
        cost = float(c.group("v").replace(",", "."))
    d = DUR_RE.search(script_part)
    duration = int(d.group("m") or 0) * 60 + int(d.group("s")) if d else None
    f = FAILS_RE.search(line)
    fails_txt = f.group("f").strip() if f else ""
    failed = 0 if fails_txt in ("", "ninguna") else len(re.findall(r"\([^()]*(?:\([^()]*\)[^()]*)*\)", fails_txt)) or 1
    return {"date": m.group("date"), "sources": int(m.group("sources")), "items": int(m.group("items")),
            "cost_usd": cost, "duration_s": duration, "sources_failed": failed}


def last_radar_run(logs: list[tuple[Path, str]]) -> tuple[dict, Path] | None:
    best = None
    for rank, (path, _label) in enumerate(logs):
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except OSError:
            continue
        for line in reversed(lines):
            run = parse_radar_line(line)
            if run:
                key = (run["date"], -rank)          # latest date wins; on a tie the first log (final) wins
                if best is None or key > best[0]:
                    best = (key, run, path)
                break
    return (best[1], best[2]) if best else None


def radar_status(logs, now: dt.datetime) -> dict:
    base = {"system": "scoring-pipeline", "title_en": "Hiring-signal radar · 16 public sources",
            "title_es": "Radar de señales de contratación · 16 fuentes públicas",
            "items_label_en": "items in scope", "items_label_es": "ítems en alcance",
            "schedule_en": "Daily, 08:40 Berlin", "schedule_es": "Diario, 08:40 Berlín",
            "kind_en": "Scheduled LLM scoring pipeline", "kind_es": "Pipeline programado de puntaje con LLM"}
    found = last_radar_run(logs)
    if not found:
        return {**base, "last_run_utc": None, "ok": False, "items": None, "cost_usd": None,
                "note": "No run recorded yet.", "note_es": "Todavía no hay corridas registradas."}
    run, path = found
    n = run["sources"]
    base["title_en"] = f"Hiring-signal radar · {n} public sources"
    base["title_es"] = f"Radar de señales de contratación · {n} fuentes públicas"
    last = run["date"]
    try:   # the log line only has the date; the file time gives the hour when it is the same day
        mtime = dt.datetime.fromtimestamp(path.stat().st_mtime, dt.timezone.utc)
        if mtime.astimezone().date().isoformat() == run["date"]:
            last = iso(mtime)
    except OSError:
        pass
    when = parse_iso(last)
    fresh = when is not None and now - when <= dt.timedelta(hours=STALE_HOURS + (24 if len(last) == 10 else 0))
    notes, notes_es = [], []
    if run["sources_failed"]:
        k = run["sources_failed"]
        notes.append(f"{k} of {n} sources did not answer")
        notes_es.append(f"{k} de {n} fuentes no respondi{'ó' if k == 1 else 'eron'}")
    if run["cost_usd"] is None:
        notes.append("cost not reported")
        notes_es.append("costo no informado")
    if not fresh:
        notes.append(f"no run in the last {STALE_HOURS} h")
        notes_es.append(f"sin corridas en las últimas {STALE_HOURS} h")
    return {**base, "last_run_utc": last, "ok": bool(fresh and run["cost_usd"] is not None),
            "items": run["items"], "cost_usd": run["cost_usd"], "duration_s": run["duration_s"],
            "sources_total": n, "sources_failed": run["sources_failed"],
            "note": sentence(notes), "note_es": sentence(notes_es)}


# ------------------------------------------------------------------ (b) SearchedBy health
def tls_context() -> ssl.SSLContext:
    """Verified TLS. The python.org build on macOS ships without CA certificates; add the system bundle."""
    ctx = ssl.create_default_context()
    if Path("/etc/ssl/cert.pem").exists():
        ctx.load_verify_locations("/etc/ssl/cert.pem")
    return ctx


NOTE_ES = {  # Spanish for the notes fetch_health() can return
    "Health check answered without ok.": "El chequeo de salud respondió sin ok.",
    "Not checked in this run.": "No se revisó en esta corrida.",
}


def note_es(note: str) -> str:
    if note in NOTE_ES:
        return NOTE_ES[note]
    m = re.match(r"Health check answered HTTP (\d+)\.", note)
    if m:
        return f"El chequeo de salud respondió HTTP {m.group(1)}."
    if note.startswith("Health check did not answer"):
        return "El chequeo de salud no respondió" + note[len("Health check did not answer"):]
    return note


def fetch_health(url: str = HEALTH_URL, timeout: float = 8.0) -> tuple[bool, int | None, str]:
    """GET only. Returns (ok, latency_ms, note)."""
    req = urllib.request.Request(url, method="GET", headers={"User-Agent": "pablodpavon.com status check"})
    t0 = time.monotonic()
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=tls_context()) as r:
            body = r.read(4096)
            ms = int((time.monotonic() - t0) * 1000)
            try:
                ok = r.status == 200 and json.loads(body).get("ok") is True
            except (ValueError, AttributeError):
                ok = False
            return ok, ms, "" if ok else "Health check answered without ok."
    except urllib.error.HTTPError as e:
        return False, int((time.monotonic() - t0) * 1000), f"Health check answered HTTP {e.code}."
    except Exception as e:  # noqa: BLE001  (timeout, DNS, TLS: the page must still be built)
        return False, None, "Health check did not answer (" + type(e).__name__ + ")."


def searchedby_status(now: dt.datetime, fetch=fetch_health) -> dict:
    ok, ms, note = fetch()
    return {"system": "searchedby", "title_en": "SearchedBy · public web app", "title_es": "SearchedBy · aplicación web pública",
            "kind_en": "Own product, open beta", "kind_es": "Producto propio, beta abierta",
            "last_run_utc": iso(now), "ok": ok, "items": None, "cost_usd": None, "latency_ms": ms,
            "schedule_en": "Health checked once a day", "schedule_es": "Salud revisada una vez por día",
            "link": "https://searchedby.com/", "note": note, "note_es": note_es(note)}


# ------------------------------------------------------------------ (c) status inputs from other systems
def strings(obj):
    if isinstance(obj, str):
        yield obj
    elif isinstance(obj, dict):
        for k, v in obj.items():
            yield str(k)
            yield from strings(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from strings(v)


def problems(obj) -> list[str]:
    out = []
    for s in strings(obj):
        low = s.lower()
        if PATH_RE.search(s):
            out.append(f"local path in {s[:40]!r}")
        if EMAIL_RE.search(s):
            out.append(f"e-mail address in {s[:40]!r}")
        for w in BANNED:
            if w in low:
                out.append(f"banned word {w.strip()!r} in {s[:40]!r}")
    return out


def check_input(d) -> list[str]:
    if not isinstance(d, dict):
        return ["not a JSON object"]
    errs = []
    for k, (typ, req) in CONTRACT.items():
        if k not in d:
            if req:
                errs.append(f"missing {k}")
            continue
        if isinstance(d[k], bool) and typ in ((int, float, type(None)),):
            errs.append(f"{k} must be a number")
        elif not isinstance(d[k], typ):
            errs.append(f"{k} has the wrong type")
    if isinstance(d.get("system"), str):
        if not re.fullmatch(r"[a-z0-9][a-z0-9-]{1,40}", d["system"]):
            errs.append("system must be a short lowercase slug")
        elif d["system"] in RESERVED:
            errs.append("system name is reserved")
    if isinstance(d.get("last_run_utc"), str) and parse_iso(d["last_run_utc"]) is None:
        errs.append("last_run_utc is not ISO 8601")
    for k, v in d.items():
        if isinstance(v, str) and len(v) > 200:
            errs.append(f"{k} longer than 200 characters")
    return errs + problems(d)


def input_statuses(folder: Path) -> list[dict]:
    out = []
    if not folder.is_dir():
        return out
    for f in sorted(folder.glob("*.json")):
        if f.name.startswith("_"):
            continue
        try:
            d = json.loads(f.read_text(encoding="utf-8"))
        except (OSError, ValueError) as e:
            warn(f"{f.name}: unreadable ({type(e).__name__}), skipped")
            continue
        errs = check_input(d)
        if errs:
            warn(f"{f.name}: skipped: " + "; ".join(errs))
            continue
        out.append({k: d[k] for k in CONTRACT if k in d})   # unknown fields are dropped
    return out


# ------------------------------------------------------------------ (d) the site itself
def site_status(repo: Path = ROOT) -> dict:
    base = {"system": "website", "title_en": "pablodpavon.com", "title_es": "pablodpavon.com",
            "kind_en": "Static site, built from source by a script", "kind_es": "Sitio estático, generado por un script",
            "schedule_en": "Updated on every change", "schedule_es": "Se actualiza con cada cambio",
            "items": None, "cost_usd": None, "link": "https://github.com/pablodpavon/pablodpavon.github.io"}
    try:
        r = subprocess.run(["git", "-C", str(repo), "log", "-1", "--format=%cI", "--", ".", ":(exclude)assets/data/status.json"],
                           capture_output=True, text=True, timeout=10, check=True)
        t = parse_iso(r.stdout.strip())
    except (OSError, subprocess.SubprocessError):
        t = None
    if t is None:
        return {**base, "last_run_utc": None, "ok": False, "note": "Last commit date not available.",
                "note_es": "La fecha del último commit no está disponible."}
    return {**base, "last_run_utc": iso(t), "ok": True, "note": "", "note_es": ""}


# ------------------------------------------------------------------ assemble
def build(now: dt.datetime | None = None, logs=None, inputs: Path = INPUTS, repo: Path = ROOT, fetch=fetch_health) -> dict:
    now = now or utc_now()
    systems = []
    for name, fn in (("pipeline", lambda: radar_status(RADAR_LOGS if logs is None else logs, now)),
                     ("searchedby", lambda: searchedby_status(now, fetch)),
                     ("inputs", lambda: input_statuses(inputs)),
                     ("site", lambda: site_status(repo))):
        try:
            res = fn()
        except Exception as e:  # noqa: BLE001  (one broken source never blocks the others)
            warn(f"{name}: {type(e).__name__}: {e}")
            continue
        systems.extend(res if isinstance(res, list) else [res])
    data = {"schema": SCHEMA, "generated_utc": iso(now), "systems": systems}
    bad = validate(data)
    if bad:   # last line of defence: drop any system that still carries something it should not
        keep = [s for s in systems if not problems(s)]
        warn("dropped systems that failed the publish check: " + "; ".join(bad))
        data["systems"] = keep
    return data


def validate(data: dict) -> list[str]:
    return problems(data)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--out", type=Path, default=OUT)
    ap.add_argument("--inputs", type=Path, default=INPUTS)
    ap.add_argument("--stdout", action="store_true", help="print the JSON instead of writing it")
    ap.add_argument("--offline", action="store_true", help="skip the SearchedBy GET (marks it as not checked)")
    a = ap.parse_args(argv)
    fetch = (lambda: (False, None, "Not checked in this run.")) if a.offline else fetch_health
    data = build(inputs=a.inputs, fetch=fetch)
    text = json.dumps(data, ensure_ascii=False, indent=1) + "\n"
    if a.stdout:
        sys.stdout.write(text)
    else:
        a.out.parent.mkdir(parents=True, exist_ok=True)
        a.out.write_text(text, encoding="utf-8")
        print(f"status: wrote {a.out.name} with {len(data['systems'])} systems")
    return 0


if __name__ == "__main__":
    sys.exit(main())
