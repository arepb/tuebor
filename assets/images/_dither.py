"""
Halftone portrait generator for Tuebor pledgees.

Reads `_pledgees/*.md` front matter and renders a Michigan-blue halftone for
each published pledgee. Halftones go to /assets/images/pledgees/ and are
committed; raw sources live in /assets/images/pledgees/_sources/ and are
gitignored.

Front-matter fields consumed:
  portrait_source   — filename inside _sources/ (e.g. reilly-source.jpg)
  portrait_face_y   — 0..1 vertical center of face (default 0.5)
  portrait_scale    — <1 = tighter crop around face (default 1.0)
  slug              — output filename is <slug>-halftone.png

Skip logic: if the source file's mtime is older than the output file's mtime,
the output is left alone (fast incremental runs).

Run: `python assets/images/_dither.py`
"""

from PIL import Image, ImageOps, ImageEnhance, ImageDraw, ImageFilter
import numpy as np
from pathlib import Path
import re

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent
PLEDGEES_DIR = REPO / "_pledgees"
SOURCES_DIR = HERE / "pledgees" / "_sources"
OUT_DIR = HERE / "pledgees"

INK = (0, 85, 164)        # Michigan blue — used for the halftone dots
PAPER = (244, 241, 234)
OUT_SIZE = 900            # @2x; display size ~450px


# ---------- Front-matter parsing ----------
# Lightweight YAML-ish reader: we only need simple scalar fields, no nested
# structures or flow syntax. Avoids a PyYAML dependency for contributors.

_FRONT_MATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)


def _coerce(v):
    v = v.strip()
    if (v.startswith('"') and v.endswith('"')) or (v.startswith("'") and v.endswith("'")):
        return v[1:-1]
    if v in ("true", "True"): return True
    if v in ("false", "False"): return False
    try: return int(v)
    except ValueError: pass
    try: return float(v)
    except ValueError: pass
    return v


def read_front_matter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    m = _FRONT_MATTER_RE.match(text)
    if not m:
        return {}
    data = {}
    for line in m.group(1).splitlines():
        if not line or line.startswith("#") or line.startswith(" ") or line.startswith("-"):
            continue
        if ":" not in line:
            continue
        key, _, val = line.partition(":")
        key = key.strip()
        val = val.split(" #", 1)[0].strip()  # strip trailing comment
        if val == "":
            continue
        data[key] = _coerce(val)
    return data


# ---------- Image pipeline ----------

def square_crop(im, face_y=0.5, scale=1.0):
    w, h = im.size
    side = int(min(w, h) * scale)
    cx = w // 2
    cy = int(h * face_y)
    x0 = max(0, min(w - side, cx - side // 2))
    y0 = max(0, min(h - side, cy - side // 2))
    return im.crop((x0, y0, x0 + side, y0 + side))


def prepare(im):
    im = ImageOps.exif_transpose(im).convert("L")
    im = ImageOps.autocontrast(im, cutoff=2)
    im = ImageEnhance.Contrast(im).enhance(1.25)
    im = ImageEnhance.Brightness(im).enhance(1.05)
    return im


def halftone(im_gray, cell=22, max_r=12.5, blur=6, levels=5):
    """Abstract newspaper halftone: blue circles on paper background."""
    w, h = im_gray.size
    blurred = im_gray.filter(ImageFilter.GaussianBlur(radius=blur))
    small = blurred.resize((w // cell, h // cell), Image.LANCZOS)
    arr = np.asarray(small, dtype=np.float32) / 255.0

    darkness = 1.0 - arr
    darkness = darkness ** 0.75
    steps = np.clip(np.round(darkness * (levels - 1)) / (levels - 1), 0.0, 1.0)

    canvas = Image.new("RGB", (w, h), PAPER)
    draw = ImageDraw.Draw(canvas)
    for gy in range(steps.shape[0]):
        for gx in range(steps.shape[1]):
            d = steps[gy, gx]
            if d < 0.05:
                continue
            r = d * max_r
            cx = gx * cell + cell / 2
            cy = gy * cell + cell / 2
            draw.ellipse((cx - r, cy - r, cx + r, cy + r), fill=INK)
    return canvas


# ---------- Driver ----------

def process(src_path: Path, out_path: Path, face_y: float, scale: float):
    if out_path.exists() and src_path.stat().st_mtime <= out_path.stat().st_mtime:
        print(f"  skip {out_path.name} (up-to-date)")
        return
    im = Image.open(src_path)
    im = square_crop(im, face_y=face_y, scale=scale)
    im = im.resize((OUT_SIZE, OUT_SIZE), Image.LANCZOS)
    g = prepare(im)
    halftone(g).save(out_path, optimize=True)
    print(f"  → {out_path.name}")


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    md_files = sorted(PLEDGEES_DIR.glob("*.md"))
    for md in md_files:
        if md.name.startswith("_"):
            continue
        fm = read_front_matter(md)
        if fm.get("published") is False:
            continue
        slug = fm.get("slug")
        src_name = fm.get("portrait_source")
        if not slug or not src_name:
            print(f"skip {md.name}: missing slug or portrait_source")
            continue
        src = SOURCES_DIR / src_name
        if not src.exists():
            print(f"skip {md.name}: source {src} not found (raw photos are gitignored — ask the pledgee)")
            continue
        face_y = float(fm.get("portrait_face_y", 0.5))
        scale = float(fm.get("portrait_scale", 1.0))
        out = OUT_DIR / f"{slug}-halftone.png"
        print(f"Processing {md.name} ({slug})")
        process(src, out, face_y, scale)


if __name__ == "__main__":
    main()
