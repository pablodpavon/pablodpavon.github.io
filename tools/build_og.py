"""Generate the Open Graph / Twitter images (1200x630) and the favicons.

Needs Pillow (pip install pillow). Fonts: uses Geist when available on the machine,
otherwise Inter or DejaVu Sans. Output:
    assets/og/home-{en,es}.png, assets/og/<slug>-{en,es}.png
    favicon.svg, favicon.ico (16/32/48), apple-touch-icon.png (180x180)
Run after tools/build_site.py:  python3 tools/build_og.py
"""
from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_cases  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
OG = ROOT / "assets" / "og"
W, H = 1200, 630

# palette = the site's light theme tokens (assets/css/site.css)
BG, CARD, INK, INK2, MUTED, LINE = "#f6f7f5", "#ffffff", "#0d1714", "#46534e", "#7d8984", "#e2e7e3"
BRAND, BRAND_TINT, BG2 = "#0e7a58", "#e3f3ec", "#eef1ee"

FONT_DIRS = [Path("/usr/share/fonts"), Path.home() / "Library/Fonts", Path("/Library/Fonts"), Path("/System/Library/Fonts")]


def find_font(names: list[str]) -> str | None:
    for d in FONT_DIRS:
        if not d.exists():
            continue
        for n in names:
            hits = list(d.rglob(n))
            if hits:
                return str(hits[0])
    return None


BOLD = find_font(["Geist-Bold.otf", "Geist-Bold.ttf", "Inter-Bold.otf", "Inter-Bold.ttf", "DejaVuSans-Bold.ttf"])
SEMI = find_font(["Geist-SemiBold.otf", "Geist-SemiBold.ttf", "Inter-SemiBold.otf", "Inter-SemiBold.ttf", "DejaVuSans-Bold.ttf"])
REG = find_font(["Geist-Regular.otf", "Geist-Regular.ttf", "Inter-Regular.otf", "Inter-Regular.ttf", "DejaVuSans.ttf"])
MED = find_font(["Geist-Medium.otf", "Geist-Medium.ttf", "Inter-Medium.otf", "Inter-Medium.ttf", "DejaVuSans.ttf"])
if not (BOLD and REG):
    raise SystemExit("no usable font found")


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= max_w or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def rounded_mask(size, r):
    m = Image.new("L", size, 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, size[0] - 1, size[1] - 1], r, fill=255)
    return m


def dots(img):
    """Subtle dot grid like the hero background."""
    d = ImageDraw.Draw(img)
    for x in range(40, W, 36):
        for y in range(40, H, 36):
            d.ellipse([x, y, x + 2, y + 2], fill="#dfe5e1")


def logo(img, x, y, size=56):
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([x, y, x + size, y + size], int(size * 0.28), fill=BRAND)
    f = font(BOLD, int(size * 0.42))
    tw = d.textlength("PP", font=f)
    d.text((x + (size - tw) / 2, y + size * 0.25), "PP", font=f, fill="white")


def chip(img, x, y, text, fnt):
    d = ImageDraw.Draw(img)
    tw = d.textlength(text, font=fnt)
    d.rounded_rectangle([x, y, x + tw + 28, y + 38], 19, fill=CARD, outline=LINE)
    d.text((x + 14, y + 8), text, font=fnt, fill=INK2)
    return x + tw + 28 + 10


def shot(src: Path, box_w: int, box_h: int) -> Image.Image:
    im = Image.open(src).convert("RGB")
    scale = box_w / im.width
    im = im.resize((box_w, max(1, round(im.height * scale))), Image.LANCZOS)
    if im.height > box_h:
        im = im.crop((0, 0, box_w, box_h))
    return im


def card(title, sub, chips, image: Path, out: Path, url_label="pablodpavon.com"):
    img = Image.new("RGB", (W, H), BG)
    dots(img)
    d = ImageDraw.Draw(img)
    # header: logo + name + url
    logo(img, 64, 56)
    d.text((136, 58), "Pablo Pavon", font=font(SEMI, 28), fill=INK)
    d.text((136, 94), url_label, font=font(MED, 17), fill=MUTED)
    # title
    y = 170
    tf = font(BOLD, 50)
    lines = wrap(d, title, tf, 560)
    if len(lines) > 3:
        tf = font(BOLD, 42)
        lines = wrap(d, title, tf, 560)[:3]
    for ln in lines:
        d.text((64, y), ln, font=tf, fill=INK)
        y += int(tf.size * 1.12)
    # subtitle
    y += 14
    sf = font(REG, 22)
    for ln in wrap(d, sub, sf, 560)[:3]:
        d.text((64, y), ln, font=sf, fill=INK2)
        y += 32
    # chips at the bottom-left
    cx, cy = 64, H - 56 - 38
    cf = font(MED, 16)
    for c in chips:
        cx = chip(img, cx, cy, c, cf)
    # right: framed screenshot ("window")
    bw = 456
    sh = shot(image, bw - 24, H - 112 - 56 - 38 - 24)
    bh = sh.height + 38 + 24
    bx, by = 680, (H - bh) // 2
    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(shadow).rounded_rectangle([bx + 6, by + 18, bx + bw + 6, by + bh + 18], 22, fill=(13, 23, 20, 70))
    shadow = shadow.filter(ImageFilter.GaussianBlur(22))
    img.paste(shadow, (0, 0), shadow)
    frame = Image.new("RGB", (bw, bh), CARD)
    fd = ImageDraw.Draw(frame)
    fd.rectangle([0, 0, bw, 38], fill=BG2)
    for i, col in enumerate(("#ff5f57", "#febc2e", "#28c840")):
        fd.ellipse([16 + i * 20, 13, 28 + i * 20, 25], fill=col)
    fd.rounded_rectangle([90, 10, bw - 90, 28], 9, fill=CARD)
    uf = font(MED, 12)
    fd.text((bw / 2 - fd.textlength(url_label, font=uf) / 2, 12), url_label, font=uf, fill=MUTED)
    frame.paste(sh, (12, 50))
    img.paste(frame, (bx, by), rounded_mask((bw, bh), 20))
    d.rounded_rectangle([bx, by, bx + bw - 1, by + bh - 1], 20, outline=LINE, width=1)
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out, optimize=True)
    print("wrote", out.relative_to(ROOT), f"{out.stat().st_size // 1024} KB")


def favicons():
    svg = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="18" fill="#0e7a58"/>'
           '<text x="32" y="42" text-anchor="middle" font-family="Geist,Inter,Arial,sans-serif" font-weight="700" font-size="26" fill="#fff">PP</text></svg>\n')
    (ROOT / "favicon.svg").write_text(svg, encoding="utf-8")
    base = Image.new("RGBA", (256, 256), (0, 0, 0, 0))
    d = ImageDraw.Draw(base)
    d.rounded_rectangle([0, 0, 255, 255], 72, fill=BRAND)
    f = font(BOLD, 104)
    tw = d.textlength("PP", font=f)
    d.text(((256 - tw) / 2, 66), "PP", font=f, fill="white")
    base.save(ROOT / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])
    apple = Image.new("RGB", (180, 180), BRAND)
    d = ImageDraw.Draw(apple)
    f = font(BOLD, 74)
    tw = d.textlength("PP", font=f)
    d.text(((180 - tw) / 2, 46), "PP", font=f, fill="white")
    apple.save(ROOT / "apple-touch-icon.png", optimize=True)
    print("wrote favicon.svg, favicon.ico, apple-touch-icon.png")


def main():
    A = ROOT / "assets"
    card("Freelance Data & Business Analyst in Berlin",
         "Power BI and SQL dashboards · data migration · finance automation · AI reporting, with every number verified.",
         ["Berlin · remote", "EN · ES · DE", "Power BI · SQL · Python"], A / "case_retention.jpg", OG / "home-en.png")
    card("Analista de datos y procesos freelance en Berlín",
         "Dashboards en Power BI y SQL · migraciones · automatización financiera · reportes con IA, con cada número verificado.",
         ["Berlín · remoto", "ES · EN · DE", "Power BI · SQL · Python"], A / "case_retention.jpg", OG / "home-es.png")
    for c in build_cases.CASES:
        for lang in ("en", "es"):
            title = c["h1_" + lang].rstrip(".")
            sub = (c["title_en"] + " · Case study on synthetic data, open code") if lang == "en" else \
                  (c["title_es"] + " · Caso de estudio con datos sintéticos, código abierto")
            chips = c["tags"][:3] + (["Synthetic data"] if lang == "en" else ["Datos sintéticos"])
            card(title, sub, chips, A / c["image"], OG / f"{c['slug']}-{lang}.png")
    favicons()


if __name__ == "__main__":
    main()
