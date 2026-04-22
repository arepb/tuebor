"""
Abstract duotone renders for Tuebor founder portraits.

Two variants per source image:
  - *-halftone.png   (classic newspaper circles — editorial, graphic)
  - *-bayer.png      (coarse 8-bit ordered dither — chunky, pixelated)

Ink on paper so they blend with the page.

Sources are cropped to make the face occupy roughly the same relative size
in each output. Tune `face_y` (0..1 vertical centre of the face) and
`scale` (1.0 = min side, <1 = tighter crop) per subject.
"""

from PIL import Image, ImageOps, ImageEnhance, ImageDraw, ImageFilter
import numpy as np
from pathlib import Path

HERE = Path(__file__).resolve().parent

INK = (0, 85, 164)        # Michigan blue — used for the halftone dots
PAPER = (244, 241, 234)
OUT_SIZE = 900  # @2x; display size ~450px

# Tuned so both subjects land with similar face scale after cropping.
SOURCES = [
    # filename,            out_prefix, face_y, scale
    ("reilly-source.jpg",  "reilly",   0.40,   0.66),
    ("chris-source2.jpeg", "chris",    0.40,   0.72),
]


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


# ---------- Halftone (circles) ----------

def halftone(im_gray, cell=22, max_r=12.5, blur=6, levels=5):
    """
    Abstract newspaper halftone. Render black circles on paper bg.

    Tuned to lose photographic detail and read as a graphic mark:
    - `blur`: Gaussian blur applied before sampling wipes out fine detail.
    - `levels`: brightness is quantized to this many steps so dots snap to
      discrete sizes (rather than a continuous photographic ramp).
    - `cell` / `max_r`: big cells and radii give a bold, posterized feel.
    """
    w, h = im_gray.size
    blurred = im_gray.filter(ImageFilter.GaussianBlur(radius=blur))
    small = blurred.resize((w // cell, h // cell), Image.LANCZOS)
    arr = np.asarray(small, dtype=np.float32) / 255.0  # 0 dark .. 1 light

    # Posterize darkness into discrete levels so the dots snap to steps.
    darkness = 1.0 - arr
    darkness = darkness ** 0.75  # lift midtones
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


# ---------- Coarse Bayer ordered dither ----------

BAYER8 = np.array([
    [ 0, 32,  8, 40,  2, 34, 10, 42],
    [48, 16, 56, 24, 50, 18, 58, 26],
    [12, 44,  4, 36, 14, 46,  6, 38],
    [60, 28, 52, 20, 62, 30, 54, 22],
    [ 3, 35, 11, 43,  1, 33,  9, 41],
    [51, 19, 59, 27, 49, 17, 57, 25],
    [15, 47,  7, 39, 13, 45,  5, 37],
    [63, 31, 55, 23, 61, 29, 53, 21],
], dtype=np.float32) / 64.0


def bayer_dither(im_gray, grid=160):
    """
    Coarse 8-bit feel: downscale, ordered-dither with Bayer 8x8, then upscale
    with nearest neighbour so the resulting pixel squares are visible.
    `grid` = logical resolution of the dither pattern.
    """
    w, h = im_gray.size
    small = im_gray.resize((grid, grid), Image.LANCZOS)
    arr = np.asarray(small, dtype=np.float32) / 255.0

    threshold = np.tile(BAYER8, (grid // 8 + 1, grid // 8 + 1))[:grid, :grid]
    binary = (arr > threshold).astype(np.uint8)  # 1 = light, 0 = dark

    out_rgb = np.empty((grid, grid, 3), dtype=np.uint8)
    out_rgb[binary == 1] = PAPER
    out_rgb[binary == 0] = INK
    small_rgb = Image.fromarray(out_rgb, "RGB")
    return small_rgb.resize((w, h), Image.NEAREST)


# ---------- Driver ----------

def process(src_name, prefix, face_y, scale):
    src = HERE / src_name
    print(f"Processing {src.name} ...")
    im = Image.open(src)
    im = square_crop(im, face_y=face_y, scale=scale)
    im = im.resize((OUT_SIZE, OUT_SIZE), Image.LANCZOS)
    g = prepare(im)

    halftone(g).save(HERE / f"{prefix}-halftone.png", optimize=True)
    print(f"  → {prefix}-halftone.png")


if __name__ == "__main__":
    for src, prefix, fy, sc in SOURCES:
        process(src, prefix, fy, sc)
