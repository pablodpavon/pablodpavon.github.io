"""Tests for build_status.py with simulated data (no network, no real logs).

Run: python3 -m unittest discover -s tools/status -p "test_*.py"
"""
import datetime as dt
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_status as bs  # noqa: E402

bs.BANNED = ("secret-word", "employer-x")   # the real list lives in the private config, outside the repo
NOW = dt.datetime(2026, 11, 1, 9, 30, tzinfo=dt.timezone.utc)

# Simulated lines in the log format of the pipeline (names and categories are placeholders).
REAL = ('2026-11-01: 16 fuentes leídas, 114 avisos vigentes, CAT_A 27, CAT_B 87, nuevos 5; fallas: '
        'Fuente Ejemplo (HTTP 403 ({"error":"Public API disabled"})). Script (modo_x, modelo-x): 1 llamada(s), '
        'US$ 0,1954; pendientes 0; duración 5 min 16 s.')
NO_CALLS = ('2026-11-02: 16 fuentes leídas, 110 avisos vigentes , CAT_A 20, CAT_B 90, nuevos 0; fallas: ninguna. '
            'Script (real, modelo-x): 0 llamada(s), US$ 0; pendientes 0; duración 48 s.')
NO_COST = ('2026-11-02: 16 fuentes leídas, 110 avisos vigentes , CAT_A 20, CAT_B 90, nuevos 3; fallas: ninguna. '
           'Script (real, modelo-x): 2 llamada(s), costo FALTA; pendientes 0; duración 2 min 03 s.')
DRY = ('2026-11-03: 16 fuentes leídas, 99 avisos vigentes , CAT_A 1, CAT_B 98, nuevos 9; fallas: ninguna. '
       'Script (seco, modelo-x): 3 llamada(s), US$ 0,5000, SIMULADO; pendientes 0; duración 1 min 00 s.')
TASK = ('2026-11-01: 16 fuentes leídas, 32 avisos vigentes  (30 anteriores + 2 nuevos), CAT_A 11, CAT_B 21, '
        'nuevos 2; fallas: Fuente Ejemplo (HTTP 403).')


def no_net():
    return True, 81, ""


def write(folder: Path, name: str, text: str) -> Path:
    p = folder / name
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")
    return p


def touch(p: Path, when: dt.datetime):
    ts = when.timestamp()
    os.utime(p, (ts, ts))


class ParseLine(unittest.TestCase):
    def test_real_line(self):
        r = bs.parse_radar_line(REAL)
        self.assertEqual(r, {"date": "2026-11-01", "sources": 16, "items": 114, "cost_usd": 0.1954,
                             "duration_s": 316, "sources_failed": 1})

    def test_no_calls_costs_zero(self):
        r = bs.parse_radar_line(NO_CALLS)
        self.assertEqual((r["cost_usd"], r["duration_s"], r["sources_failed"]), (0.0, 48, 0))

    def test_missing_cost_is_none(self):
        self.assertIsNone(bs.parse_radar_line(NO_COST)["cost_usd"])

    def test_dry_run_and_task_lines_are_ignored(self):
        self.assertIsNone(bs.parse_radar_line(DRY))
        self.assertIsNone(bs.parse_radar_line(TASK))
        self.assertIsNone(bs.parse_radar_line("# Log"))
        self.assertIsNone(bs.parse_radar_line(""))


class PickLog(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())

    def test_final_log_with_only_task_lines_falls_back_to_shadow(self):
        final = write(self.tmp, "final/log.md", TASK + "\n")
        shadow = write(self.tmp, "shadow/log.md", REAL + "\n")
        run, path = bs.last_radar_run([(final, "final"), (shadow, "shadow")])
        self.assertEqual(path, shadow)
        self.assertEqual(run["items"], 114)

    def test_newest_date_wins_and_dry_runs_are_skipped(self):
        final = write(self.tmp, "final/log.md", NO_CALLS + "\n")
        shadow = write(self.tmp, "shadow/log.md", REAL + "\n" + DRY + "\n")
        run, path = bs.last_radar_run([(final, "final"), (shadow, "shadow")])
        self.assertEqual((run["date"], path), ("2026-11-02", final))

    def test_missing_files(self):
        self.assertIsNone(bs.last_radar_run([(self.tmp / "nope.md", "x")]))


class RadarStatus(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())

    def test_publishes_only_the_allowed_facts(self):
        p = write(self.tmp, "log.md", REAL + "\n")
        touch(p, dt.datetime(2026, 11, 1, 7, 45, 16, tzinfo=dt.timezone.utc))
        s = bs.radar_status([(p, "shadow")], NOW)
        self.assertTrue(s["ok"])
        self.assertEqual((s["items"], s["cost_usd"], s["duration_s"]), (114, 0.1954, 316))
        self.assertEqual(s["last_run_utc"], "2026-11-01T07:45:16Z")
        self.assertEqual(s["title_en"], "Hiring-signal radar · 16 public sources")
        self.assertEqual(s["note"], "1 of 16 sources did not answer.")
        self.assertEqual(s["note_es"], "1 de 16 fuentes no respondió.")
        text = json.dumps(s, ensure_ascii=False)
        for word in ("Fuente Ejemplo", "CAT_A", "CAT_B", "avisos", "nuevos", "pendientes", "fallas", "modo_x",
                     "modelo-x", "403"):
            self.assertNotIn(word, text)
        self.assertEqual(bs.problems(s), [])

    def test_stale_run_is_not_ok(self):
        p = write(self.tmp, "log.md", REAL + "\n")
        touch(p, dt.datetime(2026, 11, 1, 7, 45, tzinfo=dt.timezone.utc))
        s = bs.radar_status([(p, "shadow")], NOW + dt.timedelta(days=4))
        self.assertFalse(s["ok"])
        self.assertIn("no run in the last 48 h", s["note"])
        self.assertIn("sin corridas en las últimas 48 h", s["note_es"])

    def test_missing_cost_is_not_ok(self):
        p = write(self.tmp, "log.md", NO_COST + "\n")
        s = bs.radar_status([(p, "shadow")], dt.datetime(2026, 11, 2, 12, tzinfo=dt.timezone.utc))
        self.assertFalse(s["ok"])
        self.assertIsNone(s["cost_usd"])

    def test_no_log_at_all(self):
        s = bs.radar_status([(self.tmp / "none.md", "x")], NOW)
        self.assertFalse(s["ok"])
        self.assertIsNone(s["last_run_utc"])


class Inputs(unittest.TestCase):
    GOOD = {"system": "kpi-report", "title_en": "Live KPI report", "title_es": "Reporte de KPIs en vivo",
            "last_run_utc": "2026-11-01T07:00:00Z", "ok": True, "items": 12, "items_label_en": "numbers checked",
            "items_label_es": "números verificados", "cost_usd": 0.01, "schedule_en": "Daily", "schedule_es": "Diario",
            "note": ""}

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())

    def test_valid_file_is_published_and_extra_fields_dropped(self):
        write(self.tmp, "kpi.json", json.dumps({**self.GOOD, "secret_path": "x"}))
        out = bs.input_statuses(self.tmp)
        self.assertEqual(out, [self.GOOD])

    def test_examples_and_broken_files_are_skipped(self):
        write(self.tmp, "_example.json", json.dumps(self.GOOD))
        write(self.tmp, "broken.json", "{not json")
        write(self.tmp, "list.json", "[1, 2]")
        self.assertEqual(bs.input_statuses(self.tmp), [])

    def test_contract_violations(self):
        cases = {
            "missing": {k: v for k, v in self.GOOD.items() if k != "ok"},
            "bool_items": {**self.GOOD, "items": True},
            "bad_date": {**self.GOOD, "last_run_utc": "yesterday"},
            "path": {**self.GOOD, "note": "read from /Users/someone/data.csv"},
            "email": {**self.GOOD, "note": "ask someone@example.com"},
            "banned": {**self.GOOD, "title_en": "Secret-word report"},
            "employer": {**self.GOOD, "note": "built at Employer-X"},
            "reserved": {**self.GOOD, "system": "website"},
            "slug": {**self.GOOD, "system": "KPI Report!"},
            "long": {**self.GOOD, "note": "x" * 201},
        }
        for name, d in cases.items():
            with self.subTest(name):
                self.assertTrue(bs.check_input(d), name)

    def test_missing_folder(self):
        self.assertEqual(bs.input_statuses(self.tmp / "nope"), [])


class PrivateConfig(unittest.TestCase):
    def test_missing_config_means_no_logs_and_no_extra_words(self):
        self.assertEqual(bs.load_private(Path(tempfile.mkdtemp()) / "none.json"), ([], ()))

    def test_config_is_read(self):
        p = Path(tempfile.mkdtemp()) / "cfg.json"
        p.write_text(json.dumps({"pipeline_logs": ["/tmp/a.md"], "banned": ["Word"]}))
        logs, banned = bs.load_private(p)
        self.assertEqual((logs[0][0], banned), (Path("/tmp/a.md"), ("word",)))


class Health(unittest.TestCase):
    def test_failure_is_reported_not_raised(self):
        s = bs.searchedby_status(NOW, lambda: (False, None, "Health check did not answer (URLError)."))
        self.assertFalse(s["ok"])
        self.assertIsNone(s["latency_ms"])
        self.assertEqual(s["note_es"], "El chequeo de salud no respondió (URLError).")

    def test_unreachable_url_does_not_raise(self):
        ok, ms, note = bs.fetch_health("http://127.0.0.1:9/healthz", timeout=1)
        self.assertFalse(ok)
        self.assertTrue(note)


class Assemble(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.repo = self.tmp / "repo"
        self.repo.mkdir()
        env = {**os.environ, "GIT_AUTHOR_DATE": "2026-10-31T10:00:00+01:00", "GIT_COMMITTER_DATE": "2026-10-31T10:00:00+01:00"}
        run = lambda *a: subprocess.run(["git", "-C", str(self.repo), *a], check=True, capture_output=True, env=env)
        run("init", "-q")
        run("config", "user.email", "test@invalid")
        run("config", "user.name", "test")
        write(self.repo, "index.html", "x")
        run("add", ".")
        run("commit", "-qm", "site")
        env2 = {**env, "GIT_AUTHOR_DATE": "2026-11-01T10:00:00+01:00", "GIT_COMMITTER_DATE": "2026-11-01T10:00:00+01:00"}
        write(self.repo, "assets/data/status.json", "{}")
        subprocess.run(["git", "-C", str(self.repo), "add", "."], check=True, env=env2)
        subprocess.run(["git", "-C", str(self.repo), "commit", "-qm", "status"], check=True, env=env2, capture_output=True)

    def test_site_date_ignores_status_commits(self):
        self.assertEqual(bs.site_status(self.repo)["last_run_utc"], "2026-10-31T09:00:00Z")

    def test_full_build_is_clean_and_has_every_source(self):
        log = write(self.tmp, "log.md", REAL + "\n")
        inputs = self.tmp / "inputs"
        write(inputs, "kpi.json", json.dumps(Inputs.GOOD))
        data = bs.build(now=NOW, logs=[(log, "shadow")], inputs=inputs, repo=self.repo, fetch=no_net)
        self.assertEqual([s["system"] for s in data["systems"]], ["scoring-pipeline", "searchedby", "kpi-report", "website"])
        self.assertEqual(bs.validate(data), [])
        text = json.dumps(data, ensure_ascii=False)
        self.assertNotIn("/Users/", text)
        self.assertNotIn(str(self.tmp), text)

    def test_a_broken_source_does_not_stop_the_rest(self):
        def boom():
            raise RuntimeError("down")
        data = bs.build(now=NOW, logs=[], inputs=self.tmp / "none", repo=self.repo, fetch=boom)
        self.assertEqual([s["system"] for s in data["systems"]], ["scoring-pipeline", "website"])

    def test_main_writes_file(self):
        out = self.tmp / "out" / "status.json"
        bs.RADAR_LOGS = []
        rc = bs.main(["--out", str(out), "--inputs", str(self.tmp / "none"), "--offline"])
        self.assertEqual(rc, 0)
        self.assertEqual(json.loads(out.read_text())["schema"], 1)


if __name__ == "__main__":
    unittest.main()
