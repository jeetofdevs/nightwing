"""Images for the 5-post launch series. Output: social/series-1.png ... series-5.png (1600x900).

Batman appears only as a generic caped silhouette (no logos). Platforms are plain text pills.
"""
import math, random
from pathlib import Path
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parent.parent
BANG = str(ROOT / "tools/fonts/Bangers-Regular.ttf")
INTER = "/usr/share/fonts/opentype/inter/Inter-ExtraBold.otf"
W, H = 1600, 900
BLUE, NEAR, YEL, ORANGE = (40, 120, 255), (0, 236, 151), (255, 214, 64), (234, 88, 12)
WHITE, BLACK = (255, 255, 255), (0, 0, 0)
SRC = Image.open(ROOT / "assets/nightwing-doge.jpg").convert("RGB")

def F(size, inter=False): return ImageFont.truetype(INTER if inter else BANG, size)

def text(d, xy, s, size, fill=WHITE, stroke=6, sfill=BLACK, anchor="la", inter=False):
    d.text(xy, s, font=F(size, inter), fill=fill, stroke_width=stroke, stroke_fill=sfill, anchor=anchor)

def gradient(c1, c2):
    im = Image.new("RGB", (W, H)); px = im.load()
    for y in range(H):
        t = y / H; c = tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))
        for x in range(W): px[x, y] = c
    return im

def stars(im, n=140, seed=1):
    d = ImageDraw.Draw(im, "RGBA"); random.seed(seed)
    for _ in range(n):
        x, y, r = random.randint(0, W), random.randint(0, H), random.random() * 2 + .5
        d.ellipse([x - r, y - r, x + r, y + r], fill=(255, 255, 255, random.randint(80, 200)))

def glow(im, box, col, blur=60, alpha=150):
    g = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(g).ellipse(box, fill=(*col, alpha))
    g = g.filter(ImageFilter.GaussianBlur(blur)); im.paste(g, (0, 0), g)

def doge(im, cx, cy, size, ring=BLUE, grey=False):
    s = SRC.resize((size, size), Image.LANCZOS)
    if grey: s = ImageEnhance.Brightness(ImageOps.grayscale(s).convert("RGB")).enhance(.6)
    m = Image.new("L", (size, size), 0); ImageDraw.Draw(m).ellipse([0, 0, size - 1, size - 1], fill=255)
    im.paste(s, (cx - size // 2, cy - size // 2), m)
    if ring: ImageDraw.Draw(im).ellipse([cx - size // 2, cy - size // 2, cx + size // 2, cy + size // 2], outline=ring, width=8)

def bat(im, cx, top, h, fill=(5, 6, 10), eyes=True, angle=0):
    """Generic pointy-eared caped silhouette."""
    pts = [(-.06, 0), (-.045, .06), (.045, .06), (.06, 0), (.075, .10), (.07, .17), (.04, .20), (.20, .24),
           (.42, .95), (.28, .90), (.18, 1), (.06, .92), (0, 1), (-.06, .92), (-.18, 1), (-.28, .90),
           (-.42, .95), (-.20, .24), (-.04, .20), (-.07, .17), (-.075, .10)]
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(layer)
    d.polygon([(cx + x * h, top + y * h) for x, y in pts], fill=(*fill, 255))
    if eyes:
        for sx in (-1, 1):
            d.polygon([(cx + sx * .018 * h, top + .105 * h), (cx + sx * .055 * h, top + .095 * h), (cx + sx * .05 * h, top + .115 * h)], fill=(255, 255, 255, 255))
    if angle: layer = layer.rotate(angle, center=(cx, top + h / 2), resample=Image.BICUBIC)
    im.paste(layer, (0, 0), layer)

def pill(d, cx, cy, label, bg, fg=BLACK, size=34):
    f = F(size, inter=True); w = d.textlength(label, font=f)
    d.rounded_rectangle([cx - w / 2 - 26, cy - size * .75, cx + w / 2 + 26, cy + size * .75], radius=size, fill=bg, outline=BLACK, width=4)
    d.text((cx, cy), label, font=f, fill=fg, anchor="mm")

def frame(im):
    d = ImageDraw.Draw(im); d.rectangle([0, 0, W - 1, H - 1], outline=BLACK, width=14)
    d.rectangle([14, 14, W - 15, H - 15], outline=WHITE, width=6)

def footer(d, y=H - 70):
    text(d, (W / 2, y), "$NIGHTWING", 64, fill=WHITE, stroke=6, sfill=BLUE, anchor="mm")

out = ROOT / "social"

# ---------- 1: Every Batman needs a partner
im = gradient((10, 14, 30), (25, 40, 80)); stars(im, seed=11)
d = ImageDraw.Draw(im, "RGBA")
d.rectangle([W // 2, 0, W, H], fill=(234, 88, 12, 255))
d.polygon([(W // 2 - 60, 0), (W // 2 + 60, 0), (W // 2 - 20, H), (W // 2 - 140, H)], fill=(*YEL, 255))
glow(im, [140, 220, 660, 760], (120, 160, 255), alpha=90)
d = ImageDraw.Draw(im)
d.ellipse([480, 170, 640, 330], fill=(230, 236, 255))
bat(im, 400, 260, 470)
glow(im, [980, 200, 1500, 740], BLUE, alpha=170)
doge(im, 1210, 470, 430)
d = ImageDraw.Draw(im)
text(d, (W / 2, 95), "EVERY BATMAN NEEDS A PARTNER", 92, anchor="mm")
pill(d, 400, 770, "nearly.trade", WHITE)
pill(d, 1210, 770, "justhoot.fun", NEAR)
text(d, (W / 2 - 40, 480), "&", 150, fill=YEL, stroke=8, anchor="mm")
text(d, (W / 2 - 60, 845), "$NIGHTWING", 64, fill=WHITE, stroke=6, sfill=BLUE, anchor="mm")
frame(im); im.save(out / "series-1.png", optimize=True)

# ---------- 2: The partner is suiting up
im = gradient((8, 10, 20), (20, 30, 60)); stars(im, seed=22)
d = ImageDraw.Draw(im, "RGBA")
d.polygon([(W * .62, -40), (W * .74, -40), (W * .98, H), (W * .38, H)], fill=(255, 240, 200, 40))  # spotlight
d.rectangle([60, 120, 700, 780], fill=(0, 0, 0, 0))
bat(im, 260, 470, 330, fill=(30, 34, 46), eyes=False)
d = ImageDraw.Draw(im)
text(d, (90, 160), "BATMAN GOT", 88, fill=(200, 205, 215), stroke=5)
text(d, (90, 255), "THE SPOTLIGHT.", 88, fill=(200, 205, 215), stroke=5)
pill(d, 270, 400, "on nearly.trade", (200, 205, 215), size=30)
glow(im, [800, 140, 1520, 860], BLUE, alpha=190)
doge(im, 1080, 450, 520)
d = ImageDraw.Draw(im)
text(d, (1080, 95), "THE PARTNER IS SUITING UP", 76, fill=YEL, stroke=7, anchor="mm")
pill(d, 1080, 765, "on justhoot.fun", NEAR, size=32)
text(d, (90, 820), "NO CAPE. JUST A BLUE WING.", 58, fill=WHITE, stroke=5, anchor="ls")
text(d, (1520, 830), "$NIGHTWING", 64, fill=WHITE, stroke=6, sfill=BLUE, anchor="rs")
frame(im); im.save(out / "series-2.png", optimize=True)

# ---------- 3: Who caught him? (3-panel comic)
im = Image.new("RGB", (W, H), (10, 10, 12)); d = ImageDraw.Draw(im)
G, PY = 22, 22; PW = (W - 4 * G) // 3; PH = H - 2 * G
panels = []
# p1: on the rooftop
p = Image.new("RGB", (PW, PH), (18, 24, 46)); pd = ImageDraw.Draw(p)
for i, x in enumerate(range(0, PW, 70)):
    bh = 160 + (i * 53) % 140; pd.rectangle([x, PH - bh, x + 62, PH], fill=(8, 10, 20))
q = Image.new("RGB", (W, H), (0, 0, 0)); q.paste(p, (0, 0)); bat(q, PW // 2, 300, 420); p = q.crop((0, 0, PW, PH)); pd = ImageDraw.Draw(p)
pd.ellipse([40, 40, PW - 40, 210], fill=WHITE, outline=BLACK, width=5)
pd.polygon([(PW // 2 - 20, 200), (PW // 2 + 30, 200), (PW // 2 + 10, 300)], fill=WHITE)
pd.line([(PW // 2 - 20, 205), (PW // 2 + 10, 300), (PW // 2 + 30, 205)], fill=BLACK, width=5)
text(pd, (PW // 2, 125), "“I WORK ALONE.”", 66, fill=BLACK, stroke=0, anchor="mm")
panels.append(p)
# p2: falling
p = Image.new("RGB", (W, H), (60, 20, 10)); pd = ImageDraw.Draw(p, "RGBA")
for i in range(40):
    x = random.randint(0, PW); pd.line([x, 0, x, PH], fill=(255, 200, 150, 60), width=random.randint(2, 6))
bat(p, PW // 2, 230, 400, angle=150)
p = p.crop((0, 0, PW, PH)); pd = ImageDraw.Draw(p)
pd.rectangle([18, 18, PW - 18, 130], fill=YEL, outline=BLACK, width=5)
text(pd, (PW // 2, 76), "ALSO BATMAN:", 62, fill=BLACK, stroke=0, anchor="mm")
text(pd, (PW // 2, PH - 110), "WHOOPS!", 120, fill=YEL, stroke=8, anchor="mm")
panels.append(p)
# p3: the doge catches him
p = Image.new("RGB", (W, H), (12, 30, 70)); cx, cy = PW // 2, PH // 2 + 30; pd = ImageDraw.Draw(p, "RGBA")
for i in range(40):
    a, a2 = i / 40 * 2 * math.pi, i / 40 * 2 * math.pi + .07
    pd.polygon([(cx, cy), (cx + 1500 * math.cos(a), cy + 1500 * math.sin(a)), (cx + 1500 * math.cos(a2), cy + 1500 * math.sin(a2))], fill=(*BLUE, 150) if i % 2 else (20, 50, 120, 255))
doge(p, cx, cy, 440)
p = p.crop((0, 0, PW, PH)); pd = ImageDraw.Draw(p)
pd.rectangle([18, 18, PW - 18, 130], fill=WHITE, outline=BLACK, width=5)
text(pd, (PW // 2, 76), "WHO CAUGHT HIM?", 62, fill=BLACK, stroke=0, anchor="mm")
pd.rectangle([18, PH - 150, PW - 18, PH - 18], fill=BLACK)
text(pd, (PW // 2, PH - 112), "nearly.trade has the Bat.", 34, fill=WHITE, stroke=0, anchor="mm", inter=True)
text(pd, (PW // 2, PH - 58), "justhoot.fun has the hero.", 34, fill=NEAR, stroke=0, anchor="mm", inter=True)
panels.append(p)
for i, p in enumerate(panels):
    x = G + i * (PW + G); im.paste(p, (x, PY)); d.rectangle([x - 3, PY - 3, x + PW + 2, PY + PH + 2], outline=WHITE, width=5)
im.save(out / "series-3.png", optimize=True)

# ---------- 4: Rules of the partnership
im = gradient((194, 65, 12), (124, 45, 18)); stars(im, 80, seed=44)
glow(im, [1000, 160, 1560, 720], BLUE, alpha=170)
d = ImageDraw.Draw(im, "RGBA")
d.rounded_rectangle([70, 80, 960, 820], radius=30, fill=(255, 248, 235, 255), outline=BLACK, width=8)
text(d, (515, 160), "RULES OF THE PARTNERSHIP", 70, fill=BLACK, stroke=0, anchor="mm")
d.line([140, 210, 890, 210], fill=BLUE, width=8)
rules = [("1", "The Bat takes nearly.trade"), ("2", "The doge takes justhoot.fun"), ("3", "Nobody touches the cape"), ("4", "100% to holders")]
for i, (n, r) in enumerate(rules):
    y = 290 + i * 125
    d.ellipse([130, y - 40, 210, y + 40], fill=BLUE, outline=BLACK, width=4)
    text(d, (170, y + 2), n, 60, fill=WHITE, stroke=0, anchor="mm")
    d.text((245, y), r, font=F(44, inter=True), fill=(20, 20, 20), anchor="lm")
doge(im, 1280, 420, 470)
d = ImageDraw.Draw(im)
text(d, (1280, 735), "DYNAMIC DUO.", 66, fill=YEL, stroke=7, anchor="mm")
text(d, (1280, 810), "ONE NEAR.", 66, fill=WHITE, stroke=7, anchor="mm")
frame(im); im.save(out / "series-4.png", optimize=True)

# ---------- 5: Gotham had one hero. NEAR has two.
im = gradient((10, 14, 30), (30, 20, 50)); stars(im, seed=55)
d = ImageDraw.Draw(im, "RGBA")
d.ellipse([W // 2 - 330, 120, W // 2 + 330, 780], fill=(255, 240, 210, 40))
glow(im, [200, 220, 700, 760], (120, 160, 255), alpha=80)
bat(im, 450, 270, 440)
glow(im, [900, 200, 1420, 740], BLUE, alpha=170)
doge(im, 1150, 470, 420)
d = ImageDraw.Draw(im)
text(d, (W / 2, 80), "GOTHAM HAD ONE HERO.", 84, fill=(200, 205, 215), stroke=6, anchor="mm")
text(d, (W / 2, 170), "NEAR HAS TWO.", 100, fill=YEL, stroke=8, anchor="mm")
pill(d, 450, 735, "Batman · nearly.trade", WHITE, size=30)
pill(d, 1150, 735, "Nightwing · justhoot.fun", NEAR, size=30)
d.rounded_rectangle([W / 2 - 430, 790, W / 2 + 430, 860], radius=35, fill=BLUE, outline=BLACK, width=5)
d.text((W / 2, 825), "JOIN THE PATROL: FOLLOW @NightwingOnNear", font=F(30, inter=True), fill=WHITE, anchor="mm")
frame(im); im.save(out / "series-5.png", optimize=True)
print("ok")
