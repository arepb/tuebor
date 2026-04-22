"""Generate a 180x180 Apple touch icon: blue field, white T, tan dot accent."""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

HERE = Path(__file__).resolve().parent
FONT = HERE.parent / "fonts" / "BidenBold-Regular.otf"

S = 180
BLUE = (0, 85, 164)
TAN = (196, 161, 94)
WHITE = (255, 255, 255)

img = Image.new("RGB", (S, S), BLUE)
d = ImageDraw.Draw(img)

# Big white "T"
f = ImageFont.truetype(str(FONT), 200)
bbox = d.textbbox((0, 0), "T", font=f)
tw = bbox[2] - bbox[0]
th = bbox[3] - bbox[1]
x = (S - tw) // 2 - bbox[0]
y = (S - th) // 2 - bbox[1] - 6
d.text((x, y), "T", font=f, fill=WHITE)

# Tan dot bottom-right
r = 14
pad = 22
d.rectangle((S - pad - r, S - pad - r, S - pad, S - pad), fill=TAN)

out = HERE / "apple-touch-icon.png"
img.save(out, optimize=True)
print(f"wrote {out}")
