"""Build the JSON behind the site's dashboards.

- sales.json: synthetic monthly sales cube for a fictional Argentine retailer
  (region x channel x category), plus a synthetic price index to deflate to real pesos.
- ap.json: invoice-level results of github.com/pablodpavon/ap-invoice-control (synthetic data).
- retention.json: synthetic customer cohorts with acquisition channel and RFM segment.
Run: python tools/build_data.py  (needs pandas, numpy; AP data needs the ap-invoice-control repo next to this one)
"""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

OUT = Path(__file__).resolve().parents[1] / "assets" / "data"
rng = np.random.default_rng(2026)


def sales():
    months = pd.period_range("2024-01", "2026-09", freq="M")
    # synthetic monthly inflation path: high at the start, easing over time
    infl = np.clip(0.21 * np.exp(-np.arange(len(months)) / 4.2) + 0.019 + rng.normal(0, 0.002, len(months)), 0.012, None)
    cpi = np.cumprod(1 + infl)
    cpi = cpi / cpi[-1]  # last month = 1 -> real values in pesos of the last month
    regions = {"AMBA": 0.46, "Centro": 0.17, "Cuyo": 0.08, "NOA": 0.09, "NEA": 0.07, "Patagonia": 0.13}
    channels = {"Tiendas": 0.48, "E-commerce": 0.27, "Marketplace": 0.15, "Mayorista": 0.10}
    cats = {"Electro": (0.30, 0.22), "Hogar": (0.22, 0.34), "Indumentaria": (0.18, 0.46), "Alimentos": (0.20, 0.18), "Juguetería": (0.10, 0.39)}
    ch_trend = {"Tiendas": -0.004, "E-commerce": 0.012, "Marketplace": 0.016, "Mayorista": -0.002}
    cat_trend = {"Electro": -0.009, "Hogar": 0.003, "Indumentaria": 0.011, "Alimentos": 0.001, "Juguetería": -0.004}
    reg_trend = {"AMBA": 0.002, "Centro": 0.004, "Cuyo": -0.003, "NOA": 0.001, "NEA": -0.002, "Patagonia": 0.008}
    rows = []
    base_units = 52000
    for i, m in enumerate(months):
        season = 1 + 0.28 * (m.month == 12) + 0.08 * (m.month == 11) - 0.12 * (m.month in (1, 2)) + 0.10 * (m.month in (6, 7))
        recovery = 0.86 + 0.20 / (1 + np.exp(-(i - 12) / 3))  # volumes dip in 2024, recover in 2025
        for r, rs in regions.items():
            for c, cs in channels.items():
                for k, (ks, margin) in cats.items():
                    units = base_units * rs * cs * ks * season * recovery * ((1 + ch_trend[c]) * (1 + cat_trend[k]) * (1 + reg_trend[r])) ** i * rng.lognormal(0, 0.06)
                    real_price = {"Electro": 410000, "Hogar": 96000, "Indumentaria": 54000, "Alimentos": 21000, "Juguetería": 38000}[k]
                    real_price *= 1 + rng.normal(0, 0.03) + (0.06 if c == "Marketplace" else 0) - (0.12 if c == "Mayorista" else 0)
                    nominal = units * real_price * cpi[i]
                    gm = margin + rng.normal(0, 0.012) - (0.05 if c == "Mayorista" else 0)
                    orders = units / (1.15 if c != "Mayorista" else 6.5)
                    rows.append([i, r, c, k, round(nominal), round(units), round(nominal * gm), round(orders)])
    return {"months": [str(m) for m in months], "cpi": [round(x, 6) for x in cpi],
            "dims": {"region": list(regions), "channel": list(channels), "category": list(cats)},
            "cols": ["m", "region", "channel", "category", "rev", "units", "gm", "orders"], "rows": rows}


def ap():
    root = Path(__file__).resolve().parents[2] / "ap-invoice-control"
    sys.path.insert(0, str(root / "src"))
    from apcontrol import pipeline  # noqa: E402
    src = pipeline.load(root / "data")
    df = pipeline.prepare(src, "2026-09-01")
    res, flags = pipeline.run_rules(df)
    rules = pipeline.summarize(res, flags)[["rule", "short", "severity"]].to_dict("records")
    res["month"] = res.invoice_date.dt.strftime("%Y-%m")
    rows = [[r.invoice_id, r.supplier_name_master if isinstance(r.supplier_name_master, str) else "(no está en el maestro)",
             r.supplier_cuit, r.month, r.invoice_date.strftime("%Y-%m-%d"), r.status, r.rules_hit, round(float(r.total_amount), 2)]
            for r in res.itertuples()]
    return {"rules": rules, "cols": ["id", "supplier", "cuit", "month", "date", "status", "rules", "amount"], "rows": rows}


def retention():
    cohorts = pd.period_range("2025-01", "2026-08", freq="M")
    last = pd.Period("2026-09", "M")
    channels = {"Orgánico": (0.36, 0.40), "Paid social": (0.27, 0.27), "Búsqueda paga": (0.22, 0.33), "Referidos": (0.15, 0.47)}
    out = []
    for ci, c in enumerate(cohorts):
        for ch, (share, base_ret) in channels.items():
            n = int(rng.normal(1500, 120) * share * (1 + 0.012 * ci))
            ret = base_ret * (1 - 0.006 * ci)  # newer cohorts retain slightly worse
            curve = []
            for k in range(0, (last - c).n + 1):
                if k == 0:
                    curve.append(n)
                else:
                    r = ret * (0.82 ** (k - 1)) * 0.95 + ret * 0.32 * (1 - 0.82 ** (k - 1))
                    curve.append(int(n * min(1, max(0.02, r + rng.normal(0, 0.008)))))
            spend = round(rng.normal(41000, 3000) * (1 + 0.03 * ci))
            out.append({"cohort": str(c), "channel": ch, "customers": n, "active": curve, "aov": spend})
    segments = [
        {"seg": "Campeones", "customers": 0.11, "revenue": 0.38},
        {"seg": "Leales", "customers": 0.17, "revenue": 0.27},
        {"seg": "Prometedores", "customers": 0.21, "revenue": 0.14},
        {"seg": "En riesgo", "customers": 0.14, "revenue": 0.13},
        {"seg": "Dormidos", "customers": 0.37, "revenue": 0.08},
    ]
    return {"cohorts": out, "segments": segments}


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    for name, fn in [("sales", sales), ("ap", ap), ("retention", retention)]:
        data = fn()
        (OUT / f"{name}.json").write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
        print(name, (OUT / f"{name}.json").stat().st_size // 1024, "KB")
