"""First-post meme: Gotham sidekick vs NEAR main character. Output: social/first-post-meme.png (1200x1200)."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parent.parent
W, PH = 1200, 600
XB = "/usr/share/fonts/opentype/inter/Inter-ExtraBold.otf"
SB = "/usr/share/fonts/opentype/inter/Inter-SemiBold.otf"
BLUE, NEAR = (40, 120, 255), (0, 236, 151)

def f(p, s): return ImageFont.truetype(p, s)

def text_block(d, x, y, lines, maxw):
    for txt, fnt, col in lines:
        words, line = txt.split(), ""
        for w in words:
            t = (line + " " + w).strip()
            if d.textlength(t, font=fnt) > maxw and line:
                d.text((x, y), line, font=fnt, fill=col, stroke_width=4, stroke_fill=(0, 0, 0)); y += fnt.size + 8; line = w
            else:
                line = t
        d.text((x, y), line, font=fnt, fill=col, stroke_width=4, stroke_fill=(0, 0, 0)); y += fnt.size + 22
    return y

src = Image.open(ROOT / "assets/nightwing-doge.jpg").convert("RGB").resize((PH, PH), Image.LANCZOS)
img = Image.new("RGB", (W, PH * 2), (0, 0, 0))

# Panel 1 — Gotham: grey, rainy, sad
sad = ImageEnhance.Brightness(ImageOps.grayscale(src).convert("RGB")).enhance(0.55)
p1 = Image.new("RGB", (W, PH), (22, 24, 26)); p1.paste(sad, (W - PH, 0))
d1 = ImageDraw.Draw(p1, "RGBA")
for i in range(0, W, 23):                       # rain
    for j in range(-40, PH, 70):
        o = (i * 37) % 70
        d1.line([i, j + o, i - 8, j + o + 30], fill=(200, 210, 220, 60), width=2)
d1.text((40, 40), "IN GOTHAM", font=f(SB, 30), fill=(170, 175, 180))
text_block(d1, 40, 100, [
    ("Batman: “You're just the sidekick.”", f(XB, 58), (255, 255, 255)),
    ("chart: flat. bags: heavy. cape: still not allowed.", f(SB, 32), (190, 195, 200)),
], 600)

# Panel 2 — NEAR: full colour, glowing
p2 = Image.new("RGB", (W, PH), (8, 24, 16))
glow = Image.new("RGBA", (W, PH), (0, 0, 0, 0))
ImageDraw.Draw(glow).ellipse([W - PH - 40, -40, W + 40, PH + 40], fill=(*BLUE, 120))
glow = glow.filter(ImageFilter.GaussianBlur(70))
p2.paste(glow, (0, 0), glow)
m = Image.new("L", (PH, PH), 0); ImageDraw.Draw(m).ellipse([20, 20, PH - 20, PH - 20], fill=255)
p2.paste(src, (W - PH, 0), m.filter(ImageFilter.GaussianBlur(6)))
d2 = ImageDraw.Draw(p2, "RGBA")
d2.ellipse([W - PH + 18, 18, W - 18, PH - 18], outline=BLUE, width=6)
d2.text((40, 40), "ON NEAR", font=f(SB, 30), fill=NEAR)
y = text_block(d2, 40, 100, [
    ("NEAR: “Welcome, main character.”", f(XB, 58), (255, 255, 255)),
    ("$NIGHTWING", f(XB, 76), (110, 170, 255)),
], 600)

img.paste(p1, (0, 0)); img.paste(p2, (0, PH))
d = ImageDraw.Draw(img)
d.rectangle([0, PH - 4, W, PH + 4], fill=(0, 0, 0))
img.save(ROOT / "social/first-post-meme.png", optimize=True)
print("ok")
