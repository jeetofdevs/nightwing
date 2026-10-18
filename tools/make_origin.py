"""Second-post image: 3-panel origin-story comic. Output: social/origin-story.png (1600x900)."""
import math, random
from pathlib import Path
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parent.parent
BANG = str(ROOT / "tools/fonts/Bangers-Regular.ttf")   # SIL Open Font License
INTER = "/usr/share/fonts/opentype/inter/Inter-ExtraBold.otf"
W, H, G = 1600, 900, 22
BLUE, NEAR, YEL = (40, 120, 255), (0, 236, 151), (255, 214, 64)

def font(p, s): return ImageFont.truetype(p, s)
src = Image.open(ROOT / "assets/nightwing-doge.jpg").convert("RGB")

img = Image.new("RGB", (W, H), (10, 10, 12))
d = ImageDraw.Draw(img)

# title strip
tf = font(BANG, 92)
title = "ORIGIN STORY"
tw = d.textlength(title, font=tf)
d.text(((W - tw) / 2, 10), title, font=tf, fill=(255, 255, 255), stroke_width=5, stroke_fill=BLUE)

PW = (W - 4 * G) // 3
PY, PH = 120, H - 120 - G
IMG = PW                                  # doge square fills panel width

def caption(p, text, y, bg, fg=(0, 0, 0), size=40):
    dd = ImageDraw.Draw(p)
    f = font(BANG, size)
    words, lines, line = text.split(), [], ""
    for w in words:
        t = (line + " " + w).strip()
        if dd.textlength(t, font=f) > PW - 48 and line: lines.append(line); line = w
        else: line = t
    lines.append(line)
    h = len(lines) * (size + 4) + 24
    dd.rectangle([14, y, PW - 14, y + h], fill=bg, outline=(0, 0, 0), width=4)
    for i, l in enumerate(lines):
        dd.text((28, y + 12 + i * (size + 4)), l, font=f, fill=fg)
    return h

def halftone(p, col, step=18):
    dd = ImageDraw.Draw(p, "RGBA")
    for yy in range(0, PH, step):
        for xx in range(0, PW, step):
            r = 2 + 4 * (yy / PH)
            o = step // 2 if (yy // step) % 2 else 0
            dd.ellipse([xx + o - r, yy - r, xx + o + r, yy + r], fill=(*col, 70))

# ---- panel 1: Gotham, rain, nobody notices
p1 = Image.new("RGB", (PW, PH), (24, 26, 30))
grey = ImageEnhance.Brightness(ImageOps.grayscale(src).convert("RGB")).enhance(0.6).resize((IMG, IMG), Image.LANCZOS)
p1.paste(grey, (0, (PH - IMG) // 2 + 30))
dd = ImageDraw.Draw(p1, "RGBA")
random.seed(3)
for _ in range(260):
    x, y = random.randint(0, PW), random.randint(0, PH)
    dd.line([x, y, x - 7, y + 26], fill=(210, 220, 230, 90), width=2)
caption(p1, "Gotham. Rain. A stray shiba nobody noticed.", 16, (230, 230, 225))

# ---- panel 2: the Bat fell, the doge jumped
p2 = Image.new("RGB", (PW, PH), (12, 30, 70))
cx, cy = PW // 2, PH // 2 + 40
dd = ImageDraw.Draw(p2, "RGBA")
for i in range(48):                                   # radial speed burst
    a = i / 48 * 2 * math.pi
    a2 = a + 0.06
    dd.polygon([(cx, cy), (cx + 1200 * math.cos(a), cy + 1200 * math.sin(a)),
                (cx + 1200 * math.cos(a2), cy + 1200 * math.sin(a2))],
               fill=(*BLUE, 150) if i % 2 else (20, 50, 120, 255))
halftone(p2, (255, 255, 255))
m = Image.new("L", (IMG, IMG), 0)
ImageDraw.Draw(m).ellipse([30, 30, IMG - 30, IMG - 30], fill=255)
p2.paste(src.resize((IMG, IMG), Image.LANCZOS), (0, (PH - IMG) // 2 + 40), m.filter(ImageFilter.GaussianBlur(14)))
caption(p2, "One night the Bat fell. I didn't bark.", 16, YEL)
sfx = font(BANG, 120)
dd = ImageDraw.Draw(p2)
dd.text((PW - 270, PH - 170), "LEAP!", font=sfx, fill=YEL, stroke_width=7, stroke_fill=(0, 0, 0))

# ---- panel 3: "Partner." then solo on NEAR
p3 = Image.new("RGB", (PW, PH), (8, 26, 18))
glow = Image.new("RGBA", (PW, PH), (0, 0, 0, 0))
ImageDraw.Draw(glow).ellipse([-60, 120, PW + 60, PH - 40], fill=(*BLUE, 140))
glow = glow.filter(ImageFilter.GaussianBlur(60))
p3.paste(glow, (0, 0), glow)
iy = (PH - IMG) // 2 + 40
p3.paste(src.resize((IMG, IMG), Image.LANCZOS), (0, iy), m.filter(ImageFilter.GaussianBlur(14)))
dd = ImageDraw.Draw(p3)
# speech bubble from the Bat, who is off-panel to the upper right
bx0, by0, bx1, by1 = 40, 24, PW - 90, 154
dd.ellipse([bx0, by0, bx1, by1], fill=(255, 255, 255), outline=(0, 0, 0), width=5)
tail = [(bx1 - 40, by0 + 40), (PW + 10, by0 - 10), (bx1 - 14, by0 + 84)]
dd.polygon(tail, fill=(255, 255, 255))
dd.line([tail[0], tail[1]], fill=(0, 0, 0), width=5)
dd.line([tail[1], tail[2]], fill=(0, 0, 0), width=5)
bf = font(BANG, 74)
t = "“PARTNER.”"
dd.text(((bx0 + bx1 - dd.textlength(t, font=bf)) / 2, by0 + 24), t, font=bf, fill=(0, 0, 0))
# footer tag
ff = font(BANG, 44)
tag = "$NIGHTWING"
dd.text(((PW - dd.textlength(tag, font=ff)) / 2, PH - 112), tag, font=ff, fill=(255, 255, 255), stroke_width=4, stroke_fill=(0, 0, 0))
sub = font(INTER, 22)
s = "NOW FLYING SOLO ON NEAR"
dd.rounded_rectangle([(PW - dd.textlength(s, font=sub)) / 2 - 16, PH - 58, (PW + dd.textlength(s, font=sub)) / 2 + 16, PH - 22], radius=18, fill=NEAR)
dd.text(((PW - dd.textlength(s, font=sub)) / 2, PH - 54), s, font=sub, fill=(4, 20, 13))

for i, p in enumerate((p1, p2, p3)):
    x = G + i * (PW + G)
    img.paste(p, (x, PY))
    d.rectangle([x - 3, PY - 3, x + PW + 2, PY + PH + 2], outline=(255, 255, 255), width=5)

(ROOT / "social").mkdir(exist_ok=True)
img.save(ROOT / "social/origin-story.png", optimize=True)
print("ok")
