"""
Per-pledgee Open Graph image generator.

For each published pledgee in _pledgees/*.md, composites:
  - Michigan-blue background
  - The halftone portrait (produced by _dither.py) on the left
  - Name, city · joined <year>, small TUEBOR wordmark on the right

Outputs to /assets/images/pledgees/<slug>-og.png at 1200x630. Each profile's
front matter references its own image via `og_image:`.

Skip logic: if both the portrait and source .md are older than the output,
skip. Keeps re-runs fast.

Run: `python assets/images/_ogimage_pledgee.py`
"""

from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

from _dither import read_front_matter, PLEDGEES_DIR, OUT_DIR

HERE = Path(__file__).resolve().parent
FONT_PATH = HERE.parent / "fonts" / "BidenBold-Regular.otf"

W, H = 1200, 630
BLUE = (0, 85, 164)
TAN = (196, 161, 94)
WHITE = (255, 255, 255)
WHITE_MUTED = (255, 255, 255, 178)

PADDING = 72
PORTRAIT_SIZE = 420     # square portrait on the left


def _fit_font(draw, text, font_path, max_size, max_width):
    size = max_size
    while size > 24:
        font = ImageFont.truetype(str(font_path), size)
        bbox = draw.textbbox((0, 0), text, font=font)
        if (bbox[2] - bbox[0]) <= max_width:
            return font
        size -= 2
    return ImageFont.truetype(str(font_path), size)


def make_og(pledgee: dict, halftone_path: Path, out_path: Path):
    img = Image.new("RGB", (W, H), BLUE)
    draw = ImageDraw.Draw(img, "RGBA")

    # Eyebrow top-left
    font_mono = ImageFont.truetype(str(FONT_PATH), 22)
    draw.text((PADDING, PADDING), "AN HONOR PLEDGE  ·  EST. 2023", font=font_mono, fill=WHITE_MUTED)
    draw.text((W - PADDING - 120, PADDING), "MICHIGAN", font=font_mono, fill=WHITE_MUTED)

    # Portrait on the left — halftone is blue-on-paper; drop it on the blue bg
    # inside a paper-colored square so the dots remain visible.
    portrait = Image.open(halftone_path).convert("RGB")
    portrait = portrait.resize((PORTRAIT_SIZE, PORTRAIT_SIZE), Image.LANCZOS)
    px = PADDING
    py = (H - PORTRAIT_SIZE) // 2 + 10
    img.paste(portrait, (px, py))

    # Right column: name, meta, wordmark
    text_x = px + PORTRAIT_SIZE + 56
    text_w = W - text_x - PADDING

    name = str(pledgee.get("name", ""))
    font_name = _fit_font(draw, name, FONT_PATH, 96, text_w)
    name_bbox = draw.textbbox((0, 0), name, font=font_name)
    name_h = name_bbox[3] - name_bbox[1]
    name_y = py + 24
    draw.text((text_x, name_y - name_bbox[1]), name, font=font_name, fill=WHITE)

    # Meta line: joined <year>
    year = pledgee.get("year_joined", "")
    meta = f"JOINED {year}".upper()
    font_meta = ImageFont.truetype(str(FONT_PATH), 26)
    meta_y = name_y + name_h + 24
    draw.text((text_x, meta_y), meta, font=font_meta, fill=WHITE_MUTED)

    # Small TUEBOR wordmark bottom-right of the right column, with tan period
    font_mark = ImageFont.truetype(str(FONT_PATH), 72)
    mark_bbox = draw.textbbox((0, 0), "TUEBOR", font=font_mark)
    mark_w = mark_bbox[2] - mark_bbox[0]
    mark_h = mark_bbox[3] - mark_bbox[1]
    mark_x = text_x
    mark_y = py + PORTRAIT_SIZE - mark_h - 20
    draw.text((mark_x, mark_y - mark_bbox[1]), "TUEBOR", font=font_mark, fill=WHITE)
    dot_side = int(mark_h * 0.22)
    dot_x = mark_x + mark_w + 12
    dot_y = mark_y + mark_h - dot_side
    draw.rectangle((dot_x, dot_y, dot_x + dot_side, dot_y + dot_side), fill=TAN)

    # URL bottom-right
    font_url = ImageFont.truetype(str(FONT_PATH), 22)
    draw.text((W - PADDING - 140, H - PADDING - 6), "TUEBOR.ORG", font=font_url, fill=(255, 255, 255, 210))

    img.save(out_path, optimize=True)
    print(f"  → {out_path.name}")


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for md in sorted(PLEDGEES_DIR.glob("*.md")):
        if md.name.startswith("_"):
            continue
        fm = read_front_matter(md)
        if fm.get("published") is False:
            continue
        slug = fm.get("slug")
        if not slug:
            continue
        halftone_path = OUT_DIR / f"{slug}-halftone.png"
        out_path = OUT_DIR / f"{slug}-og.png"
        if not halftone_path.exists():
            print(f"skip {md.name}: halftone not found — run _dither.py first")
            continue
        if out_path.exists():
            newest_src = max(halftone_path.stat().st_mtime, md.stat().st_mtime)
            if newest_src <= out_path.stat().st_mtime:
                print(f"  skip {out_path.name} (up-to-date)")
                continue
        print(f"Processing {md.name} ({slug})")
        make_og(fm, halftone_path, out_path)


if __name__ == "__main__":
    main()
