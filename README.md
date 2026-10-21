# pablodpavon.com

Portfolio of Pablo Pavon, freelance Senior Business & Data Analyst in Berlin. Static site on GitHub Pages, in English (`/`) and Spanish (`/es/`).

## How it is built

- `src/` holds the bilingual sources (`src/index.html`, `src/proyectos/*.html`). Both languages sit side by side in the markup (`<p lang="es">…</p><p lang="en">…</p>`).
- `tools/build_site.py` writes one page per language with a single `<h1>`, the right `<html lang>`, a full `<head>` (title, description, canonical, `hreflang`, Open Graph, JSON-LD) and language-aware links, plus `sitemap.xml`, `robots.txt` and `llms.txt`. It calls `tools/build_cases.py`, which generates the case-study sources from one template.
- `tools/build_og.py` renders the Open Graph images (`assets/og/`) and the favicons (needs Pillow).
- `tools/build_data.py` generates the synthetic datasets behind the dashboards (`assets/data/`).

```sh
python3 tools/build_site.py   # regenerate the published pages (stdlib only)
python3 tools/build_og.py     # optional: Open Graph images and favicons
```

Edit `src/` or the build scripts, never the generated files at the root, `proyectos/` or `es/`.

## Notes

- Dashboards and case studies use synthetic data from fictional companies. The code of each case is public in its own repository.
- ECharts (Apache-2.0) and the Geist fonts (SIL OFL) are self-hosted in `assets/vendor/` and `assets/fonts/`.
