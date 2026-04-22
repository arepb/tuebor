"""
Generate the Tuebor Open Graph share image.

Output: assets/images/og-image.png (1200x630, the standard OG size).
Style echoes the homepage hero: Michigan blue, white BidenBold TUEBOR wordmark,
tan accent period.
"""

from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

HERE = Path(__file__).resolve().parent
FONT_PATH = HERE.parent / "fonts" / "BidenBold-Regular.otf"

W, H = 1200, 630
BLUE = (0, 85, 164)
TAN = (196, 161, 94)
WHITE = (255, 255, 255)
PAPER_MUTED = (255, 255, 255, 178)  # translucent for the tagline

PADDING = 72


def make():
    img = Image.new("RGB", (W, H), BLUE)
    draw = ImageDraw.Draw(img, "RGBA")

    # --- Big TUEBOR wordmark, auto-fit to leave room for the tan period ---
    wordmark = "TUEBOR"
    target_width = W - PADDING * 2 - 80  # reserve ~80px for the tan square + gap
    size = 360
    while size > 80:
        font_main = ImageFont.truetype(str(FONT_PATH), size)
        bbox = draw.textbbox((0, 0), wordmark, font=font_main)
        if (bbox[2] - bbox[0]) <= target_width:
            break
        size -= 4
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]

    # Left-aligned, vertically biased slightly above center for visual balance.
    x = PADDING
    y = (H - th) // 2 - 30 - bbox[1]
    draw.text((x, y), wordmark, font=font_main, fill=WHITE)

    # --- Tan accent square "period" to match the hero ---
    # Size the square proportional to cap height; place it tight to the R.
    dot_side = int(th * 0.20)
    dot_x = x + tw + 18
    dot_y = y + bbox[1] + th - dot_side  # bottom-align with baseline-ish
    draw.rectangle((dot_x, dot_y, dot_x + dot_side, dot_y + dot_side), fill=TAN)

    # --- Eyebrow: AN HONOR PLEDGE · EST. 2023 (top-left) ---
    font_mono = ImageFont.truetype(str(FONT_PATH), 22)
    draw.text((PADDING, PADDING), "AN HONOR PLEDGE  ·  EST. 2023", font=font_mono, fill=(255, 255, 255, 178))
    draw.text((W - PADDING - 120, PADDING), "MICHIGAN", font=font_mono, fill=(255, 255, 255, 178))

    # --- Tagline: below wordmark ---
    font_tag = ImageFont.truetype(str(FONT_PATH), 34)
    tag_y = y + bbox[1] + th + 60
    # Two-line tagline — the tan parenthetical keeps continuity with the site.
    draw.text((PADDING, tag_y), "An honor-pledge commitment by the",
              font=font_tag, fill=WHITE)
    draw.text((PADDING, tag_y + 44), "people who really love Michigan.",
              font=font_tag, fill=TAN)

    # --- URL bottom-right ---
    font_url = ImageFont.truetype(str(FONT_PATH), 22)
    draw.text((W - PADDING - 140, H - PADDING - 6), "TUEBOR.ORG", font=font_url, fill=(255, 255, 255, 210))

    out = HERE / "og-image.png"
    img.save(out, optimize=True)
    print(f"wrote {out} ({W}x{H})")


if __name__ == "__main__":
    make()
