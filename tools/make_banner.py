"""Generate the X/Twitter header (1500x500 and 3000x1000) from assets/nightwing-doge.jpg."""
import math, random
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parent.parent
S = 2                      # render at 2x, downscale for the 1500x500 version
W, H = 1500 * S, 500 * S
BG = (26, 60, 43)
BLUE = (40, 120, 255)
FONT = "/usr/share/fonts/opentype/inter/Inter-ExtraBold.otf"
FONT_B = "/usr/share/fonts/opentype/inter/Inter-Bold.otf"
FONT_M = "/usr/share/fonts/opentype/inter/Inter-SemiBold.otf"

def font(path, size): return ImageFont.truetype(path, size * S)

# --- background: dark-to-green horizontal gradient + vignette
base = Image.new("RGB", (W, H))
px = base.load()
for x in range(W):
    t = x / W
    c = tuple(int(8 + (BG[i] - 8) * min(1, t * 1.35)) if i != 1 else int(18 + (BG[1] - 18) * min(1, t * 1.35)) for i in range(3))
    for y in range(H):
        px[x, y] = c
d = ImageDraw.Draw(base, "RGBA")

def skyline():
  random.seed(7)
  x = 0
  while x < W:
    bw = random.randint(30, 90) * S
    bh = random.randint(40, 170) * S
    if 1010 * S < x + bw and x < 1440 * S:   # keep the hero's legs clear
        bh = min(bh, 50 * S)
    d.rectangle([x, H - bh, x + bw, H], fill=(6, 20, 14, 235))
    for wy in range(H - bh + 14 * S, H - 10 * S, 18 * S):      # lit windows
        for wx in range(x + 8 * S, x + bw - 8 * S, 16 * S):
            if random.random() < 0.18:
                d.rectangle([wx, wy, wx + 5 * S, wy + 7 * S], fill=(255, 210, 120, 120))
    x += bw + random.randint(0, 8) * S

# --- moon glow (top-right of the text area)
glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
gd = ImageDraw.Draw(glow)
cx, cy, r = 1075 * S, 95 * S, 62 * S
gd.ellipse([cx - r * 2, cy - r * 2, cx + r * 2, cy + r * 2], fill=(120, 180, 255, 40))
glow = glow.filter(ImageFilter.GaussianBlur(40 * S))
base.paste(glow, (0, 0), glow)
d = ImageDraw.Draw(base, "RGBA")
moon = Image.new("L", (W, H), 0)
md = ImageDraw.Draw(moon)
md.ellipse([cx - r, cy - r, cx + r, cy + r], fill=235)
md.ellipse([cx - r + 30 * S, cy - r - 10 * S, cx + r + 30 * S, cy + r - 10 * S], fill=0)

# --- blue speed streaks behind the hero
for i in range(14):
    y0 = random.randint(120, 420) * S
    x0 = random.randint(700, 1050) * S
    ln = random.randint(120, 320) * S
    d.line([x0, y0, x0 + ln, y0 - ln // 6], fill=(*BLUE, random.randint(40, 110)), width=random.randint(2, 5) * S)

# --- hero: the doge photo, feathered into the background on the right side
hero = Image.open(ROOT / "assets/nightwing-doge.jpg").convert("RGB").resize((H, H), Image.LANCZOS)
mask = Image.new("L", (H, H), 0)
mp = mask.load()
for yy in range(H):
    for xx in range(H):
        ex = min(xx, H - 1 - xx) / (H * 0.22)
        ey = min(yy, H - 1 - yy) / (H * 0.10)
        mp[xx, yy] = int(255 * max(0, min(1, ex, ey if yy < H * 0.5 else min(yy and (H - 1 - yy) / (H * 0.14), 1))))
mask = mask.filter(ImageFilter.GaussianBlur(10 * S))
hx = W - H - 40 * S
base.paste(hero, (hx, 0), mask)
d = ImageDraw.Draw(base, "RGBA")
skyline()
base.paste((222, 234, 255), (0, 0), moon)
d = ImageDraw.Draw(base, "RGBA")

# --- wing chevron accent (Nightwing-blue "V" stroke) behind the title
def chevron(x, y, w, h, t, fill):
    d.polygon([(x, y), (x + w / 2, y + h), (x + w, y), (x + w - t, y), (x + w / 2, y + h - t * 1.3), (x + t, y)], fill=fill)

# Text block starts right of where the profile picture sits (bottom-left on desktop)
tx = 300 * S
d.text((tx, 70 * S), "THE PARTNER BATMAN NEVER SAW COMING", font=font(FONT_M, 22), fill=(150, 195, 255))
title = font(FONT, 96)
d.text((tx + 4 * S, 118 * S + 4 * S), "$NIGHTWING", font=title, fill=(0, 0, 0, 140))
d.text((tx, 118 * S), "$NIGHTWING", font=title, fill=(255, 255, 255))
tw = d.textlength("$NIGHTWING", font=title)
chevron(tx, 258 * S, tw, 42 * S, 20 * S, (*BLUE, 255))
d.text((tx, 312 * S), "Nightwing Doge  •  Gotham's sidekick, NEAR's hero", font=font(FONT_B, 28), fill=(235, 240, 245))

# NEAR pill
pill = font(FONT_B, 20)
label = "BUILT ON NEAR"
pw = d.textlength(label, font=pill) + 40 * S
d.rounded_rectangle([tx, 370 * S, tx + pw, 412 * S], radius=21 * S, fill=(0, 236, 151, 255))
d.text((tx + 20 * S, 379 * S), label, font=pill, fill=(5, 20, 14))

base.save(ROOT / "assets/twitter-banner@2x.png", optimize=True)
base.resize((1500, 500), Image.LANCZOS).save(ROOT / "assets/twitter-banner.png", optimize=True)
print("ok")
