"""
Generate the Tuebor wordmark logo in multiple formats and colorways.

Outputs (assets/images/logo/):
  SVG (vector, no font dependency — glyphs converted to <path>):
    tuebor-logo.svg             ink on transparent (master)
    tuebor-logo-blue.svg        blue on transparent
    tuebor-logo-white.svg       white on transparent
    tuebor-logo-on-blue.svg     white on Michigan-blue field
    tuebor-logo-on-paper.svg    ink on paper field

  PNG (rasterized from source font at high DPI):
    tuebor-logo-{512,1024,2048}.png              transparent, ink
    tuebor-logo-white-{512,1024,2048}.png        transparent, white
    tuebor-logo-blue-{512,1024,2048}.png         transparent, blue
    tuebor-logo-on-blue-{512,1024,2048}.png      white on blue
    tuebor-logo-on-paper-{512,1024,2048}.png     ink on paper

Run:
    python3 assets/images/_logo.py
"""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen

HERE = Path(__file__).resolve().parent
FONT_PATH = HERE.parent / "fonts" / "BidenBold-Regular.otf"
OUT_DIR = HERE / "logo"
OUT_DIR.mkdir(exist_ok=True)

WORDMARK = "TUEBOR"

# Brand colors (match style.scss tokens)
INK = "#0A0A0A"
BLUE = "#0055A4"
TAN = "#C4A15E"
WHITE = "#FFFFFF"
PAPER = "#F4F1EA"

# Period (accent square) is always tan, regardless of wordmark color
ACCENT = TAN


# ---------------------------------------------------------------------------
# SVG generation via fontTools glyph outlines
# ---------------------------------------------------------------------------

def build_svg(fg: str, bg: str | None, pad: int = 40) -> str:
    """Build a self-contained SVG of 'TUEBOR.' with glyph outlines as paths.

    fg: wordmark color (hex)
    bg: background color (hex) or None for transparent
    pad: padding around the artwork in font units (scaled by upem ratio later)
    """
    font = TTFont(str(FONT_PATH))
    cmap = font.getBestCmap()
    glyf = font.getGlyphSet()
    upem = font["head"].unitsPerEm
    hmtx = font["hmtx"]

    # Walk the string, collect glyph paths with their x offsets + widths.
    x_cursor = 0
    glyph_paths = []  # list of (svg_path_d, x_offset)
    for ch in WORDMARK:
        gname = cmap[ord(ch)]
        glyph = glyf[gname]
        pen = SVGPathPen(glyf)
        glyph.draw(pen)
        d = pen.getCommands()
        adv_width, _ = hmtx[gname]
        glyph_paths.append((d, x_cursor))
        x_cursor += adv_width
    wordmark_width = x_cursor

    # Cap height from OS/2 if available, else font bbox
    os2 = font["OS/2"]
    cap_height = getattr(os2, "sCapHeight", None) or font["head"].yMax

    # Accent square — side = ~20% of cap height, placed snug to the R.
    dot_side = int(cap_height * 0.20)
    dot_gap = int(cap_height * 0.05)
    dot_x = wordmark_width + dot_gap
    dot_y_bottom = 0  # baseline — we'll flip Y below, so this is the baseline

    total_width = dot_x + dot_side
    total_height = cap_height

    # SVG coordinates are y-down; font coordinates are y-up. We flip with a
    # transform on a <g> so we can keep glyph paths natural.
    vb_x = -pad
    vb_y = -pad
    vb_w = total_width + pad * 2
    vb_h = total_height + pad * 2

    bg_layer = ""
    if bg:
        bg_layer = (
            f'<rect x="{vb_x}" y="{vb_y}" '
            f'width="{vb_w}" height="{vb_h}" fill="{bg}"/>\n  '
        )

    # Build glyph path group (flipped vertically via scale(1,-1))
    glyph_elems = []
    for d, x_off in glyph_paths:
        glyph_elems.append(
            f'<path d="{d}" transform="translate({x_off} 0)" fill="{fg}"/>'
        )
    glyphs_svg = "\n    ".join(glyph_elems)

    # Accent square — also inside the flipped group, so y goes up from baseline.
    accent_svg = (
        f'<rect x="{dot_x}" y="0" width="{dot_side}" height="{dot_side}" '
        f'fill="{ACCENT}"/>'
    )

    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'viewBox="{vb_x} {vb_y} {vb_w} {vb_h}" '
        f'width="{vb_w}" height="{vb_h}" '
        f'role="img" aria-label="Tuebor">\n  '
        f'{bg_layer}'
        f'<g transform="scale(1 -1) translate(0 -{total_height})">\n    '
        f'{glyphs_svg}\n    '
        f'{accent_svg}\n  '
        f'</g>\n'
        f'</svg>\n'
    )
    return svg


# ---------------------------------------------------------------------------
# PNG generation via Pillow + the OTF directly
# ---------------------------------------------------------------------------

def build_png(fg, bg, height: int, pad_ratio: float = 0.18) -> Image.Image:
    """Render 'TUEBOR.' to a PNG at the requested height.

    fg: (r,g,b) or (r,g,b,a) foreground
    bg: (r,g,b) or (r,g,b,a) background; use (0,0,0,0) for transparent
    height: total image height in px
    pad_ratio: vertical padding as a fraction of height (each side)
    """
    pad = int(height * pad_ratio)
    target_cap_h = height - pad * 2

    # Binary search the font size that gives us the target cap-height-ish.
    # ImageFont sizes are in points at 72dpi, but for OTF Pillow treats the
    # value as the pixel EM size; rendered text height ≈ 0.70 * em for caps.
    lo, hi = 10, height * 3
    for _ in range(30):
        mid = (lo + hi) // 2
        font = ImageFont.truetype(str(FONT_PATH), mid)
        bbox = font.getbbox(WORDMARK)
        cap_h = bbox[3] - bbox[1]
        if cap_h < target_cap_h:
            lo = mid + 1
        else:
            hi = mid - 1
    size = max(lo - 1, 10)
    font = ImageFont.truetype(str(FONT_PATH), size)
    bbox = font.getbbox(WORDMARK)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]

    # Accent square sits tight to R at ~20% of cap height
    dot_side = max(int(th * 0.20), 2)
    dot_gap = max(int(th * 0.05), 1)
    total_w = tw + dot_gap + dot_side + pad * 2
    total_h = height

    img = Image.new("RGBA", (total_w, total_h), bg)
    draw = ImageDraw.Draw(img, "RGBA")

    # Place wordmark: left-padded, vertically centered
    x = pad - bbox[0]
    y = (total_h - th) // 2 - bbox[1]
    draw.text((x, y), WORDMARK, font=font, fill=fg)

    # Accent square, bottom-aligned to baseline of the R
    dot_x = pad + tw + dot_gap
    dot_y = y + bbox[1] + th - dot_side
    tan_rgb = tuple(int(TAN[i : i + 2], 16) for i in (1, 3, 5))
    draw.rectangle((dot_x, dot_y, dot_x + dot_side, dot_y + dot_side), fill=tan_rgb)
    return img


def hex_to_rgba(hex_str: str, alpha: int = 255):
    h = hex_str.lstrip("#")
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), alpha)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

VARIANTS = [
    # name,          fg,    bg (None for transparent)
    ("tuebor-logo",          INK,   None),
    ("tuebor-logo-white",    WHITE, None),
    ("tuebor-logo-blue",     BLUE,  None),
    ("tuebor-logo-on-blue",  WHITE, BLUE),
    ("tuebor-logo-on-paper", INK,   PAPER),
]

PNG_HEIGHTS = [512, 1024, 2048]


def main():
    for name, fg_hex, bg_hex in VARIANTS:
        # SVG
        svg = build_svg(fg_hex, bg_hex)
        svg_path = OUT_DIR / f"{name}.svg"
        svg_path.write_text(svg)
        print(f"wrote {svg_path.relative_to(HERE.parent.parent)}")

        # PNGs
        fg_rgba = hex_to_rgba(fg_hex)
        bg_rgba = hex_to_rgba(bg_hex) if bg_hex else (0, 0, 0, 0)
        for h in PNG_HEIGHTS:
            img = build_png(fg_rgba, bg_rgba, h)
            out = OUT_DIR / f"{name}-{h}.png"
            img.save(out, optimize=True)
            print(f"wrote {out.relative_to(HERE.parent.parent)} ({img.size[0]}x{img.size[1]})")


if __name__ == "__main__":
    main()
