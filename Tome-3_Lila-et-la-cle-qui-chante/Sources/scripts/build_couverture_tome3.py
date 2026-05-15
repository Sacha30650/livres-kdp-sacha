"""Couverture wrap-around Tome 3"""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import math

IMG_DIR = Path("/home/claude/lila_tome3")
OUT_PDF = Path("/home/claude/lila_tome3_couverture.pdf")

DPI = 228
TRIM_W_IN = 8.972
TRIM_H_IN = 8.972
BLEED_IN = 0.125
SPINE_IN = 0.072
SAFETY_IN = 0.5

COVER_W_IN = (TRIM_W_IN + BLEED_IN) * 2 + SPINE_IN
COVER_H_IN = TRIM_H_IN + 2 * BLEED_IN


def in2px(x): return round(x * DPI)


COVER_W = in2px(COVER_W_IN)
COVER_H = in2px(COVER_H_IN)
BLEED_PX = in2px(BLEED_IN)
SPINE_PX = in2px(SPINE_IN)
TRIM_W_PX = in2px(TRIM_W_IN)
TRIM_H_PX = in2px(TRIM_H_IN)
SAFETY_PX = in2px(SAFETY_IN)

BACK_X_TRIM_START = BLEED_PX
BACK_X_END = BACK_X_TRIM_START + TRIM_W_PX
SPINE_X_START = BACK_X_END
SPINE_X_END = SPINE_X_START + SPINE_PX
FRONT_X_TRIM_START = SPINE_X_END
FRONT_X_TRIM_END = FRONT_X_TRIM_START + TRIM_W_PX
FRONT_X_END = COVER_W

BACK_SAFE_LEFT = BACK_X_TRIM_START + SAFETY_PX
BACK_SAFE_RIGHT = BACK_X_END - SAFETY_PX
FRONT_SAFE_LEFT = FRONT_X_TRIM_START + SAFETY_PX
FRONT_SAFE_RIGHT = FRONT_X_TRIM_END - SAFETY_PX
Y_TRIM_TOP = BLEED_PX
Y_TRIM_BOTTOM = BLEED_PX + TRIM_H_PX

FONT_BODY = "/usr/share/fonts/truetype/google-fonts/Lora-Variable.ttf"
FONT_BODY_ITALIC = "/usr/share/fonts/truetype/google-fonts/Lora-Italic-Variable.ttf"
FONT_HANDWRITTEN = "/usr/local/lib/python3.12/dist-packages/font_amatic_sc/files/AmaticSC-Bold.ttf"

INK = (58, 31, 16)
INK_DEEP = (45, 24, 12)
INK_SOFT = (90, 53, 32)
CREAM = (251, 246, 236)


def halo(w, h, op=0.92):
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    px = img.load()
    cx, cy = w / 2, h / 2
    rx, ry = w / 2, h / 2
    for y in range(h):
        for x in range(w):
            d = math.sqrt(((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2)
            a = int(op * 255 * max(0, (1 - d ** 1.5)))
            a = max(0, min(255, a))
            px[x, y] = (*CREAM, a)
    return img


def centered_block(draw, text, font, y_start, xl, xr, fill, ls=1.30):
    lines = text.split("\n")
    b = draw.textbbox((0, 0), "Ag", font=font)
    lh = int((b[3] - b[1]) * ls)
    y = y_start
    cx = (xl + xr) // 2
    for line in lines:
        if not line.strip():
            y += lh // 2
            continue
        b = draw.textbbox((0, 0), line, font=font)
        draw.text((cx - (b[2] - b[0]) // 2, y), line, font=font, fill=fill)
        y += lh


print(f"📐 Couv Tome 3 : {COVER_W_IN:.3f} × {COVER_H_IN:.3f} in")

canvas = Image.new("RGB", (COVER_W, COVER_H), CREAM)

print("→ back panel")
back = Image.open(IMG_DIR / "cover_back.png").convert("RGB")
canvas.paste(back.resize((BACK_X_END, COVER_H), Image.LANCZOS), (0, 0))

print("→ front panel")
front = Image.open(IMG_DIR / "cover_front.png").convert("RGB")
fw = FRONT_X_END - FRONT_X_TRIM_START
canvas.paste(front.resize((fw, COVER_H), Image.LANCZOS), (FRONT_X_TRIM_START, 0))

print("→ spine")
for x in range(SPINE_X_START, SPINE_X_END):
    for y in range(COVER_H):
        canvas.putpixel((x, y), (245, 236, 220))

canvas = canvas.convert("RGBA")

# BACK
print("→ textes back")
syn_w = TRIM_W_PX - 2 * SAFETY_PX
syn_h = in2px(4.2)
syn_x = BACK_X_TRIM_START + SAFETY_PX
syn_y = Y_TRIM_TOP + in2px(1.1)
canvas.paste(halo(syn_w, syn_h, 0.88), (syn_x, syn_y), halo(syn_w, syn_h, 0.88))

draw = ImageDraw.Draw(canvas)
f_syn = ImageFont.truetype(FONT_BODY_ITALIC, 42); f_syn.set_variation_by_axes([500])

syn_text = """Dans la poche d'un vieux manteau,
Lila trouve une petite clé en cristal
qui chante doucement.

D'une cuisine pleine de tasses musicales
à un océan de sons oubliés,
elle rencontre Mira — une fille qui voit
ce que les autres entendent.

Ensemble, elles découvrent que rien
ne se perd vraiment : tout ce qu'on aime
attend qu'on tende l'oreille à nouveau."""

centered_block(draw, syn_text, f_syn, syn_y + in2px(0.3),
               BACK_SAFE_LEFT, BACK_SAFE_RIGHT, INK_DEEP, 1.35)

f_close = ImageFont.truetype(FONT_HANDWRITTEN, 84)
close_text = "Un conte sur l'écoute et l'amitié,\npour les rêveurs de 6 à 8 ans."
close_y = syn_y + syn_h + in2px(0.1)
close_w = TRIM_W_PX - 2 * SAFETY_PX
close_h = in2px(1.4)
close_x = BACK_X_TRIM_START + SAFETY_PX
canvas.paste(halo(close_w, close_h, 0.85), (close_x, close_y), halo(close_w, close_h, 0.85))
draw = ImageDraw.Draw(canvas)
centered_block(draw, close_text, f_close, close_y + in2px(0.15),
               BACK_SAFE_LEFT, BACK_SAFE_RIGHT, INK, 1.15)

f_auth_b = ImageFont.truetype(FONT_HANDWRITTEN, 100)
auth = "Apolline Verger"
auth_y = Y_TRIM_BOTTOM - in2px(1.8)
ahw = in2px(4.5)
ahh = in2px(0.9)
ahx = BACK_X_TRIM_START + (TRIM_W_PX - ahw) // 2
canvas.paste(halo(ahw, ahh, 0.85), (ahx, auth_y), halo(ahw, ahh, 0.85))
draw = ImageDraw.Draw(canvas)
b = draw.textbbox((0, 0), auth, font=f_auth_b)
cx = BACK_X_TRIM_START + TRIM_W_PX // 2
draw.text((cx - (b[2] - b[0]) // 2, auth_y + in2px(0.05)), auth, font=f_auth_b, fill=INK)

# FRONT
print("→ textes front")
f_cl = ImageFont.truetype(FONT_BODY, 22); f_cl.set_variation_by_axes([600])
f_cn = ImageFont.truetype(FONT_BODY_ITALIC, 42); f_cn.set_variation_by_axes([500])

chw = in2px(2.8)
chh = in2px(0.7)
chx = FRONT_X_TRIM_END - chw - SAFETY_PX
chy = Y_TRIM_TOP + SAFETY_PX
canvas.paste(halo(chw, chh, 0.82), (chx, chy), halo(chw, chh, 0.82))
draw = ImageDraw.Draw(canvas)

lbl = " ".join("COLLECTION")
b = draw.textbbox((0, 0), lbl, font=f_cl)
draw.text((chx + chw - (b[2] - b[0]) - in2px(0.2), chy + in2px(0.15)), lbl, font=f_cl, fill=INK_DEEP)
cn = "Au seuil des merveilles"
b = draw.textbbox((0, 0), cn, font=f_cn)
draw.text((chx + chw - (b[2] - b[0]) - in2px(0.2), chy + in2px(0.32)), cn, font=f_cn, fill=INK_DEEP)

# Titre
thw = TRIM_W_PX - 2 * SAFETY_PX
thh = in2px(3.2)
thx = FRONT_X_TRIM_START + SAFETY_PX
thy = Y_TRIM_TOP + in2px(1.3)
canvas.paste(halo(thw, thh, 0.92), (thx, thy), halo(thw, thh, 0.92))
draw = ImageDraw.Draw(canvas)

f_main = ImageFont.truetype(FONT_BODY, 200); f_main.set_variation_by_axes([600])
f_it = ImageFont.truetype(FONT_BODY_ITALIC, 120); f_it.set_variation_by_axes([500])

pc = FRONT_X_TRIM_START + TRIM_W_PX // 2
y = thy + in2px(0.25)

b = draw.textbbox((0, 0), "Lila", font=f_main)
draw.text((pc - (b[2] - b[0]) // 2, y), "Lila", font=f_main, fill=INK_DEEP)
y += in2px(0.95)

b = draw.textbbox((0, 0), "et la clé", font=f_it)
draw.text((pc - (b[2] - b[0]) // 2, y), "et la clé", font=f_it, fill=INK_SOFT)
y += in2px(0.65)

b = draw.textbbox((0, 0), "qui chante", font=f_main)
draw.text((pc - (b[2] - b[0]) // 2, y), "qui chante", font=f_main, fill=INK_DEEP)
y += in2px(1.0)

shw = TRIM_W_PX - 2 * SAFETY_PX
shh = in2px(0.8)
shx = FRONT_X_TRIM_START + SAFETY_PX
shy = y - in2px(0.1)
canvas.paste(halo(shw, shh, 0.85), (shx, shy), halo(shw, shh, 0.85))
draw = ImageDraw.Draw(canvas)

f_sub = ImageFont.truetype(FONT_BODY_ITALIC, 52); f_sub.set_variation_by_axes([500])
sub = "Une amitié au-delà des sons"
b = draw.textbbox((0, 0), sub, font=f_sub)
draw.text((pc - (b[2] - b[0]) // 2, shy + in2px(0.2)), sub, font=f_sub, fill=INK_DEEP)

# Auteur front
af_y = Y_TRIM_BOTTOM - in2px(1.3)
afw = in2px(5.5)
afh = in2px(1.0)
afx = FRONT_X_TRIM_START + (TRIM_W_PX - afw) // 2
canvas.paste(halo(afw, afh, 0.85), (afx, af_y), halo(afw, afh, 0.85))
draw = ImageDraw.Draw(canvas)

f_af = ImageFont.truetype(FONT_HANDWRITTEN, 130)
b = draw.textbbox((0, 0), auth, font=f_af)
draw.text((pc - (b[2] - b[0]) // 2, af_y + in2px(0.05)), auth, font=f_af, fill=INK)

print("\n💾 Écriture PDF couverture…")
canvas.convert("RGB").save(OUT_PDF, format="PDF", resolution=DPI)
import os
print(f"✓ {OUT_PDF}")
print(f"  Taille: {os.path.getsize(OUT_PDF) / 1024 / 1024:.1f} MB · {COVER_W_IN:.3f} × {COVER_H_IN:.3f} in")
