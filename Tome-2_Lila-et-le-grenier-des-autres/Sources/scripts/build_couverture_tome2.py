"""
Génère le PDF de COUVERTURE KDP wrap-around pour 'Lila et le grenier des autres' (Tome 2)

KDP paperback, 32 pages, papier blanc :
- Trim chaque panneau : 8.972 × 8.972 in
- Bleed : 0.125 in
- Spine : 0.072 in (32 pages)
- Total : 18.266 × 9.222 in
"""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import math

# ============================================================
# DIMENSIONS
# ============================================================
IMG_DIR = Path("/home/claude/lila_tome2")
OUT_PDF = Path("/home/claude/lila_tome2_couverture.pdf")

DPI = 228

TRIM_W_IN = 8.972
TRIM_H_IN = 8.972
BLEED_IN = 0.125
SPINE_IN = 0.072

COVER_W_IN = (TRIM_W_IN + BLEED_IN) * 2 + SPINE_IN
COVER_H_IN = TRIM_H_IN + 2 * BLEED_IN


def in2px(inches): return round(inches * DPI)


COVER_W = in2px(COVER_W_IN)
COVER_H = in2px(COVER_H_IN)
BLEED_PX = in2px(BLEED_IN)
SPINE_PX = in2px(SPINE_IN)
TRIM_W_PX = in2px(TRIM_W_IN)
TRIM_H_PX = in2px(TRIM_H_IN)

BACK_X_START = 0
BACK_X_TRIM_START = BLEED_PX
BACK_X_END = BACK_X_TRIM_START + TRIM_W_PX
SPINE_X_START = BACK_X_END
SPINE_X_END = SPINE_X_START + SPINE_PX
FRONT_X_TRIM_START = SPINE_X_END
FRONT_X_TRIM_END = FRONT_X_TRIM_START + TRIM_W_PX
FRONT_X_END = COVER_W

Y_TRIM_TOP = BLEED_PX
Y_TRIM_BOTTOM = BLEED_PX + TRIM_H_PX
Y_TOTAL = COVER_H

# Fonts
FONT_BODY = "/usr/share/fonts/truetype/google-fonts/Lora-Variable.ttf"
FONT_BODY_ITALIC = "/usr/share/fonts/truetype/google-fonts/Lora-Italic-Variable.ttf"
FONT_HANDWRITTEN = "/usr/local/lib/python3.12/dist-packages/font_amatic_sc/files/AmaticSC-Bold.ttf"

INK = (58, 31, 16)
INK_DEEP = (45, 24, 12)
INK_SOFT = (90, 53, 32)
CREAM = (251, 246, 236)


def make_ellipse_halo(width, height, opacity_center=0.92, ellipse_w_ratio=1.0, ellipse_h_ratio=1.0):
    halo = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    px = halo.load()
    cx, cy = width / 2, height / 2
    rx = width / 2 * ellipse_w_ratio
    ry = height / 2 * ellipse_h_ratio
    for y in range(height):
        for x in range(width):
            d = math.sqrt(((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2)
            alpha = int(opacity_center * 255 * max(0, (1 - d ** 1.5)))
            alpha = max(0, min(255, alpha))
            px[x, y] = (*CREAM, alpha)
    return halo


def draw_centered_text_block(draw, text, font, y_start, x_left, x_right,
                              fill, line_spacing=1.30):
    lines = text.split("\n")
    bbox_ref = draw.textbbox((0, 0), "Ag", font=font)
    line_h = bbox_ref[3] - bbox_ref[1]
    line_h_with_spacing = int(line_h * line_spacing)
    y = y_start
    panel_center_x = (x_left + x_right) // 2
    for line in lines:
        if not line.strip():
            y += line_h_with_spacing // 2
            continue
        bbox = draw.textbbox((0, 0), line, font=font)
        text_w = bbox[2] - bbox[0]
        x = panel_center_x - text_w // 2
        draw.text((x, y), line, font=font, fill=fill)
        y += line_h_with_spacing
    return y


# ============================================================
# CONSTRUCTION CANVAS
# ============================================================
print(f"📐 Couverture wrap-around Tome 2 : {COVER_W_IN:.3f} × {COVER_H_IN:.3f} in ({COVER_W}×{COVER_H} px à {DPI} DPI)")
print()

canvas = Image.new("RGB", (COVER_W, COVER_H), CREAM)

# BACK PANEL
print("→ Composition back panel (4e de couv)")
back_img = Image.open(IMG_DIR / "cover_back.png").convert("RGB")
back_target_w = BACK_X_END
back_target_h = COVER_H
back_img_resized = back_img.resize((back_target_w, back_target_h), Image.LANCZOS)
canvas.paste(back_img_resized, (BACK_X_START, 0))

# FRONT PANEL
print("→ Composition front panel (1re de couv)")
front_img = Image.open(IMG_DIR / "cover_front.png").convert("RGB")
front_target_w = FRONT_X_END - FRONT_X_TRIM_START
front_target_h = COVER_H
front_img_resized = front_img.resize((front_target_w, front_target_h), Image.LANCZOS)
canvas.paste(front_img_resized, (FRONT_X_TRIM_START, 0))

# SPINE
print("→ Composition spine (cream)")
spine_color = (245, 236, 220)
for x in range(SPINE_X_START, SPINE_X_END):
    for y in range(COVER_H):
        canvas.putpixel((x, y), spine_color)

canvas = canvas.convert("RGBA")

# ============================================================
# TEXTE BACK PANEL (synopsis)
# ============================================================
print("→ Textes back panel")

# Halo synopsis
synopsis_box_w = TRIM_W_PX - in2px(0.8)
synopsis_box_h = in2px(4.5)
synopsis_x = BACK_X_TRIM_START + (TRIM_W_PX - synopsis_box_w) // 2
synopsis_y = Y_TRIM_TOP + in2px(1.2)
synopsis_halo = make_ellipse_halo(synopsis_box_w, synopsis_box_h,
                                  opacity_center=0.88)
canvas.paste(synopsis_halo, (synopsis_x, synopsis_y), synopsis_halo)

draw = ImageDraw.Draw(canvas)

f_synopsis = ImageFont.truetype(FONT_BODY_ITALIC, 46)
f_synopsis.set_variation_by_axes([500])

synopsis_text = """Lila avait sa clé en bronze.
Mais elle ne savait pas qu'ailleurs,
dans le monde, quatre autres enfants
gardaient aussi la leur.

D'un grenier japonais à un désert d'étoiles,
en passant par une savane parlante
et une cité cachée dans une calabaza,
cinq enfants découvrent ensemble
qu'ils n'ont jamais été seuls."""

draw_centered_text_block(
    draw, synopsis_text, f_synopsis,
    synopsis_y + in2px(0.35),
    BACK_X_TRIM_START, BACK_X_END,
    fill=INK_DEEP, line_spacing=1.36
)

# Phrase de clôture (manuscrite Amatic SC)
f_closing = ImageFont.truetype(FONT_HANDWRITTEN, 92)
closing_text = "Un conte d'amitié et de portes secrètes,\npour les rêveurs de 6 à 8 ans."
closing_y = synopsis_y + synopsis_box_h - in2px(0.5)
closing_halo_w = in2px(7)
closing_halo_h = in2px(1.7)
closing_halo_x = BACK_X_TRIM_START + (TRIM_W_PX - closing_halo_w) // 2
closing_halo = make_ellipse_halo(closing_halo_w, closing_halo_h,
                                  opacity_center=0.85)
canvas.paste(closing_halo, (closing_halo_x, closing_y), closing_halo)
draw = ImageDraw.Draw(canvas)
draw_centered_text_block(
    draw, closing_text, f_closing,
    closing_y + in2px(0.2),
    BACK_X_TRIM_START, BACK_X_END,
    fill=INK, line_spacing=1.15
)

# Auteur en bas du back (remonté pour zone code-barres KDP)
f_author_back = ImageFont.truetype(FONT_HANDWRITTEN, 110)
author_text = "Apolline Verger"
author_y = Y_TRIM_BOTTOM - in2px(1.6)
author_halo_w = in2px(5)
author_halo_h = in2px(0.95)
author_halo_x = BACK_X_TRIM_START + (TRIM_W_PX - author_halo_w) // 2
author_halo = make_ellipse_halo(author_halo_w, author_halo_h,
                                opacity_center=0.85)
canvas.paste(author_halo, (author_halo_x, author_y), author_halo)
draw = ImageDraw.Draw(canvas)
bbox = draw.textbbox((0, 0), author_text, font=f_author_back)
aw = bbox[2] - bbox[0]
center_x = BACK_X_TRIM_START + TRIM_W_PX // 2
draw.text((center_x - aw // 2, author_y + in2px(0.05)),
          author_text, font=f_author_back, fill=INK)

# Note : pas de cartouche ISBN — KDP imprime le code-barres en bas-droite

# ============================================================
# TEXTE FRONT PANEL
# ============================================================
print("→ Textes front panel")

# Collection en haut à droite
f_collection_label = ImageFont.truetype(FONT_BODY, 22)
f_collection_label.set_variation_by_axes([600])
f_collection_name = ImageFont.truetype(FONT_BODY_ITALIC, 42)
f_collection_name.set_variation_by_axes([500])

coll_halo_w = in2px(2.8)
coll_halo_h = in2px(0.7)
coll_halo_x = FRONT_X_TRIM_END - coll_halo_w - in2px(0.25)
coll_halo_y = Y_TRIM_TOP + in2px(0.25)
coll_halo = make_ellipse_halo(coll_halo_w, coll_halo_h, opacity_center=0.82)
canvas.paste(coll_halo, (coll_halo_x, coll_halo_y), coll_halo)
draw = ImageDraw.Draw(canvas)

label = "COLLECTION"
labeled = " ".join(label)
bbox2 = draw.textbbox((0, 0), labeled, font=f_collection_label)
lw2 = bbox2[2] - bbox2[0]
draw.text((coll_halo_x + coll_halo_w - lw2 - in2px(0.25), coll_halo_y + in2px(0.15)),
          labeled, font=f_collection_label, fill=INK_DEEP)

coll_name = "Au seuil des merveilles"
bbox = draw.textbbox((0, 0), coll_name, font=f_collection_name)
nw = bbox[2] - bbox[0]
draw.text((coll_halo_x + coll_halo_w - nw - in2px(0.25), coll_halo_y + in2px(0.30)),
          coll_name, font=f_collection_name, fill=INK_DEEP)

# Titre principal centré
title_halo_w = TRIM_W_PX - in2px(0.6)
title_halo_h = in2px(3.5)
title_halo_x = FRONT_X_TRIM_START + (TRIM_W_PX - title_halo_w) // 2
title_halo_y = Y_TRIM_TOP + in2px(1.1)
title_halo = make_ellipse_halo(title_halo_w, title_halo_h, opacity_center=0.92)
canvas.paste(title_halo, (title_halo_x, title_halo_y), title_halo)
draw = ImageDraw.Draw(canvas)

f_title_main = ImageFont.truetype(FONT_BODY, 220)
f_title_main.set_variation_by_axes([600])
f_title_it = ImageFont.truetype(FONT_BODY_ITALIC, 130)
f_title_it.set_variation_by_axes([500])

panel_center = FRONT_X_TRIM_START + TRIM_W_PX // 2
y = title_halo_y + in2px(0.25)

# Lila
bbox = draw.textbbox((0, 0), "Lila", font=f_title_main)
tw = bbox[2] - bbox[0]
draw.text((panel_center - tw // 2, y), "Lila", font=f_title_main, fill=INK_DEEP)
y += in2px(1.0)

# et le grenier (italique)
bbox = draw.textbbox((0, 0), "et le grenier", font=f_title_it)
tw = bbox[2] - bbox[0]
draw.text((panel_center - tw // 2, y), "et le grenier", font=f_title_it, fill=INK_SOFT)
y += in2px(0.7)

# des autres
bbox = draw.textbbox((0, 0), "des autres", font=f_title_main)
tw = bbox[2] - bbox[0]
draw.text((panel_center - tw // 2, y), "des autres", font=f_title_main, fill=INK_DEEP)
y += in2px(1.1)

# Sous-titre
sub_halo_w = in2px(7)
sub_halo_h = in2px(0.8)
sub_halo_x = FRONT_X_TRIM_START + (TRIM_W_PX - sub_halo_w) // 2
sub_halo_y = y - in2px(0.1)
sub_halo = make_ellipse_halo(sub_halo_w, sub_halo_h, opacity_center=0.85)
canvas.paste(sub_halo, (sub_halo_x, sub_halo_y), sub_halo)
draw = ImageDraw.Draw(canvas)

f_subtitle = ImageFont.truetype(FONT_BODY_ITALIC, 56)
f_subtitle.set_variation_by_axes([500])
sub_text = "Cinq clés, cinq mondes, une grande maison"
bbox = draw.textbbox((0, 0), sub_text, font=f_subtitle)
tw = bbox[2] - bbox[0]
draw.text((panel_center - tw // 2, sub_halo_y + in2px(0.18)),
          sub_text, font=f_subtitle, fill=INK_DEEP)

# Auteur en bas du front
author_front_y = Y_TRIM_BOTTOM - in2px(0.85)
author_halo_front_w = in2px(5.5)
author_halo_front_h = in2px(1.0)
author_halo_front_x = FRONT_X_TRIM_START + (TRIM_W_PX - author_halo_front_w) // 2
author_halo_front = make_ellipse_halo(author_halo_front_w, author_halo_front_h, opacity_center=0.85)
canvas.paste(author_halo_front, (author_halo_front_x, author_front_y), author_halo_front)
draw = ImageDraw.Draw(canvas)

f_author_front = ImageFont.truetype(FONT_HANDWRITTEN, 140)
bbox = draw.textbbox((0, 0), author_text, font=f_author_front)
aw = bbox[2] - bbox[0]
draw.text((panel_center - aw // 2, author_front_y + in2px(0.05)),
          author_text, font=f_author_front, fill=INK)

# ============================================================
# SAUVEGARDE
# ============================================================
canvas_rgb = canvas.convert("RGB")
print()
print("💾 Écriture PDF couverture wrap-around…")
canvas_rgb.save(OUT_PDF, format="PDF", resolution=DPI)
import os
print(f"✓ {OUT_PDF}")
print(f"  Taille : {os.path.getsize(OUT_PDF) / 1024 / 1024:.1f} MB")
print(f"  Dimensions : {COVER_W_IN:.3f} × {COVER_H_IN:.3f} in")
