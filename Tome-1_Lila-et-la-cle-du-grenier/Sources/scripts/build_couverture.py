"""
Génère le PDF de COUVERTURE KDP wrap-around pour 'Lila et la clé du grenier' V2

CORRECTIONS V2 vs V1 :
- Augmentation des marges de safety à 0.5" minimum (KDP demande 0.375" min)
- Resserrement des textes vers le centre
- Garantit que AUCUN texte ne soit à moins de 0.5" des bords trim
"""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import math

IMG_DIR = Path("/home/claude/lila_images")
OUT_PDF = Path("/home/claude/lila_couverture_v2.pdf")

DPI = 228

TRIM_W_IN = 8.972
TRIM_H_IN = 8.972
BLEED_IN = 0.125
SPINE_IN = 0.072  # 32 pages
SAFETY_IN = 0.5  # MARGE DE SÉCURITÉ KDP (au lieu de 0.375" min) -- garde une bonne marge supplémentaire

COVER_W_IN = (TRIM_W_IN + BLEED_IN) * 2 + SPINE_IN
COVER_H_IN = TRIM_H_IN + 2 * BLEED_IN


def in2px(inches): return round(inches * DPI)


COVER_W = in2px(COVER_W_IN)
COVER_H = in2px(COVER_H_IN)
BLEED_PX = in2px(BLEED_IN)
SPINE_PX = in2px(SPINE_IN)
TRIM_W_PX = in2px(TRIM_W_IN)
TRIM_H_PX = in2px(TRIM_H_IN)
SAFETY_PX = in2px(SAFETY_IN)

# Layout x
BACK_X_START = 0
BACK_X_TRIM_START = BLEED_PX
BACK_X_END = BACK_X_TRIM_START + TRIM_W_PX
SPINE_X_START = BACK_X_END
SPINE_X_END = SPINE_X_START + SPINE_PX
FRONT_X_TRIM_START = SPINE_X_END
FRONT_X_TRIM_END = FRONT_X_TRIM_START + TRIM_W_PX
FRONT_X_END = COVER_W

# Safety zones (depuis bord PDF)
# Back panel safe zone
BACK_SAFE_LEFT = BACK_X_TRIM_START + SAFETY_PX
BACK_SAFE_RIGHT = BACK_X_END - SAFETY_PX
# Front panel safe zone
FRONT_SAFE_LEFT = FRONT_X_TRIM_START + SAFETY_PX
FRONT_SAFE_RIGHT = FRONT_X_TRIM_END - SAFETY_PX
# Vertical safe zone
SAFE_TOP = BLEED_PX + SAFETY_PX
SAFE_BOTTOM = COVER_H - BLEED_PX - SAFETY_PX

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
print(f"📐 Couverture wrap-around Tome 1 V2 : {COVER_W_IN:.3f} × {COVER_H_IN:.3f} in")
print(f"   Safety zone : {SAFETY_IN}\" (= {SAFETY_PX}px) depuis tous bords trim")
print()

canvas = Image.new("RGB", (COVER_W, COVER_H), CREAM)

# Back panel
print("→ Composition back panel (4e de couv)")
back_img = Image.open(IMG_DIR / "cover_back.png").convert("RGB")
back_img_resized = back_img.resize((BACK_X_END, COVER_H), Image.LANCZOS)
canvas.paste(back_img_resized, (0, 0))

# Front panel
print("→ Composition front panel (1re de couv)")
front_img = Image.open(IMG_DIR / "cover_front.png").convert("RGB")
front_target_w = FRONT_X_END - FRONT_X_TRIM_START
front_img_resized = front_img.resize((front_target_w, COVER_H), Image.LANCZOS)
canvas.paste(front_img_resized, (FRONT_X_TRIM_START, 0))

# Spine
print("→ Composition spine (cream)")
spine_color = (245, 236, 220)
for x in range(SPINE_X_START, SPINE_X_END):
    for y in range(COVER_H):
        canvas.putpixel((x, y), spine_color)

canvas = canvas.convert("RGBA")

# ============================================================
# TEXTE BACK PANEL — TOUS À >= 0.5" DES BORDS TRIM
# ============================================================
print("→ Textes back panel (safety zone respectée)")

# Synopsis : zone réduite et centrée
# Width max = TRIM_W - 2 × SAFETY = 8.972 - 1.0 = 7.972"
synopsis_box_w = TRIM_W_PX - 2 * SAFETY_PX   # = 1818 px (7.972")
synopsis_box_h = in2px(4.0)
synopsis_x = BACK_X_TRIM_START + SAFETY_PX
synopsis_y = Y_TRIM_TOP + in2px(1.4)
synopsis_halo = make_ellipse_halo(synopsis_box_w, synopsis_box_h,
                                  opacity_center=0.88)
canvas.paste(synopsis_halo, (synopsis_x, synopsis_y), synopsis_halo)

draw = ImageDraw.Draw(canvas)
f_synopsis = ImageFont.truetype(FONT_BODY_ITALIC, 42)
f_synopsis.set_variation_by_axes([500])

synopsis_lines = [
    "Lila passe l'été chez sa grand-mère.",
    "Un après-midi, dans la poussière du grenier,",
    "elle découvre une vieille clé en bronze…",
    "et une petite porte qui n'avait jamais existé.",
    "",
    "De jardins minuscules en cités sous-marines,",
    "de royaumes de nuages en horlogeries infinies,",
    "Lila ouvre cinq mondes — et apprend",
    "que les plus grandes aventures commencent",
    "toujours par une porte qu'on n'avait pas vue.",
]
synopsis_text = "\n".join(synopsis_lines)
draw_centered_text_block(
    draw, synopsis_text, f_synopsis,
    synopsis_y + in2px(0.3),
    BACK_SAFE_LEFT, BACK_SAFE_RIGHT,
    fill=INK_DEEP, line_spacing=1.35
)

# Phrase de clôture
f_closing = ImageFont.truetype(FONT_HANDWRITTEN, 88)
closing_text = "Un conte tendre et lumineux,\npour les rêveurs de 6 à 8 ans."
closing_y = synopsis_y + synopsis_box_h + in2px(0.1)
closing_halo_w = TRIM_W_PX - 2 * SAFETY_PX
closing_halo_h = in2px(1.5)
closing_halo_x = BACK_X_TRIM_START + SAFETY_PX
closing_halo = make_ellipse_halo(closing_halo_w, closing_halo_h, opacity_center=0.85)
canvas.paste(closing_halo, (closing_halo_x, closing_y), closing_halo)
draw = ImageDraw.Draw(canvas)
draw_centered_text_block(
    draw, closing_text, f_closing,
    closing_y + in2px(0.15),
    BACK_SAFE_LEFT, BACK_SAFE_RIGHT,
    fill=INK, line_spacing=1.15
)

# Auteur sur le back — bien remonté pour rester loin du bord bas + ne pas toucher zone code-barres KDP
f_author_back = ImageFont.truetype(FONT_HANDWRITTEN, 100)
author_text = "Apolline Verger"
# Bord inférieur trim = Y_TRIM_BOTTOM. Safety = 0.5". Code-barres KDP en bas-droite (~2"×1.2").
# On positionne l'auteur centré horizontalement et à 1.8" du bord bas trim pour être safe.
author_y = Y_TRIM_BOTTOM - in2px(1.8)
author_halo_w = in2px(4.5)
author_halo_h = in2px(0.9)
author_halo_x = BACK_X_TRIM_START + (TRIM_W_PX - author_halo_w) // 2
author_halo = make_ellipse_halo(author_halo_w, author_halo_h, opacity_center=0.85)
canvas.paste(author_halo, (author_halo_x, author_y), author_halo)
draw = ImageDraw.Draw(canvas)
bbox = draw.textbbox((0, 0), author_text, font=f_author_back)
aw = bbox[2] - bbox[0]
center_x = BACK_X_TRIM_START + TRIM_W_PX // 2
draw.text((center_x - aw // 2, author_y + in2px(0.05)),
          author_text, font=f_author_back, fill=INK)

# ============================================================
# TEXTE FRONT PANEL
# ============================================================
print("→ Textes front panel (safety zone respectée)")

# Collection en haut à droite — bien à 0.5" du bord trim haut et droit
f_collection_label = ImageFont.truetype(FONT_BODY, 22)
f_collection_label.set_variation_by_axes([600])
f_collection_name = ImageFont.truetype(FONT_BODY_ITALIC, 42)
f_collection_name.set_variation_by_axes([500])

coll_halo_w = in2px(2.8)
coll_halo_h = in2px(0.7)
# Position: à 0.5" du bord trim droit ET à 0.5" du bord trim haut
coll_halo_x = FRONT_X_TRIM_END - coll_halo_w - SAFETY_PX
coll_halo_y = Y_TRIM_TOP + SAFETY_PX
coll_halo = make_ellipse_halo(coll_halo_w, coll_halo_h, opacity_center=0.82)
canvas.paste(coll_halo, (coll_halo_x, coll_halo_y), coll_halo)
draw = ImageDraw.Draw(canvas)

labeled = " ".join("COLLECTION")
bbox2 = draw.textbbox((0, 0), labeled, font=f_collection_label)
lw2 = bbox2[2] - bbox2[0]
draw.text((coll_halo_x + coll_halo_w - lw2 - in2px(0.2), coll_halo_y + in2px(0.15)),
          labeled, font=f_collection_label, fill=INK_DEEP)

coll_name = "Au seuil des merveilles"
bbox = draw.textbbox((0, 0), coll_name, font=f_collection_name)
nw = bbox[2] - bbox[0]
draw.text((coll_halo_x + coll_halo_w - nw - in2px(0.2), coll_halo_y + in2px(0.32)),
          coll_name, font=f_collection_name, fill=INK_DEEP)

# Titre principal centré
title_halo_w = TRIM_W_PX - 2 * SAFETY_PX
title_halo_h = in2px(3.0)
title_halo_x = FRONT_X_TRIM_START + SAFETY_PX
title_halo_y = Y_TRIM_TOP + in2px(1.3)
title_halo = make_ellipse_halo(title_halo_w, title_halo_h, opacity_center=0.92)
canvas.paste(title_halo, (title_halo_x, title_halo_y), title_halo)
draw = ImageDraw.Draw(canvas)

f_title_main = ImageFont.truetype(FONT_BODY, 200)
f_title_main.set_variation_by_axes([600])
f_title_it = ImageFont.truetype(FONT_BODY_ITALIC, 120)
f_title_it.set_variation_by_axes([500])

panel_center = FRONT_X_TRIM_START + TRIM_W_PX // 2
y = title_halo_y + in2px(0.25)

# Lila
bbox = draw.textbbox((0, 0), "Lila", font=f_title_main)
tw = bbox[2] - bbox[0]
draw.text((panel_center - tw // 2, y), "Lila", font=f_title_main, fill=INK_DEEP)
y += in2px(0.95)

# et la clé (italique)
bbox = draw.textbbox((0, 0), "et la clé", font=f_title_it)
tw = bbox[2] - bbox[0]
draw.text((panel_center - tw // 2, y), "et la clé", font=f_title_it, fill=INK_SOFT)
y += in2px(0.65)

# du grenier
bbox = draw.textbbox((0, 0), "du grenier", font=f_title_main)
tw = bbox[2] - bbox[0]
draw.text((panel_center - tw // 2, y), "du grenier", font=f_title_main, fill=INK_DEEP)
y += in2px(1.0)

# Sous-titre
sub_halo_w = TRIM_W_PX - 2 * SAFETY_PX
sub_halo_h = in2px(0.8)
sub_halo_x = FRONT_X_TRIM_START + SAFETY_PX
sub_halo_y = y - in2px(0.1)
sub_halo = make_ellipse_halo(sub_halo_w, sub_halo_h, opacity_center=0.85)
canvas.paste(sub_halo, (sub_halo_x, sub_halo_y), sub_halo)
draw = ImageDraw.Draw(canvas)

f_subtitle = ImageFont.truetype(FONT_BODY_ITALIC, 52)
f_subtitle.set_variation_by_axes([500])
sub_text = "Une aventure à travers cinq mondes"
bbox = draw.textbbox((0, 0), sub_text, font=f_subtitle)
tw = bbox[2] - bbox[0]
draw.text((panel_center - tw // 2, sub_halo_y + in2px(0.2)),
          sub_text, font=f_subtitle, fill=INK_DEEP)

# Auteur en bas du front — à au moins 0.6" du bord trim bas (safety 0.5" + un peu)
author_front_y = Y_TRIM_BOTTOM - in2px(1.3)
author_halo_front_w = in2px(5.5)
author_halo_front_h = in2px(1.0)
author_halo_front_x = FRONT_X_TRIM_START + (TRIM_W_PX - author_halo_front_w) // 2
author_halo_front = make_ellipse_halo(author_halo_front_w, author_halo_front_h, opacity_center=0.85)
canvas.paste(author_halo_front, (author_halo_front_x, author_front_y), author_halo_front)
draw = ImageDraw.Draw(canvas)

f_author_front = ImageFont.truetype(FONT_HANDWRITTEN, 130)
bbox = draw.textbbox((0, 0), author_text, font=f_author_front)
aw = bbox[2] - bbox[0]
draw.text((panel_center - aw // 2, author_front_y + in2px(0.05)),
          author_text, font=f_author_front, fill=INK)

# ============================================================
# SAUVEGARDE
# ============================================================
canvas_rgb = canvas.convert("RGB")
print()
print("💾 Écriture PDF couverture wrap-around v2…")
canvas_rgb.save(OUT_PDF, format="PDF", resolution=DPI)
import os
print(f"✓ {OUT_PDF}")
print(f"  Taille : {os.path.getsize(OUT_PDF) / 1024 / 1024:.1f} MB")
print(f"  Dimensions : {COVER_W_IN:.3f} × {COVER_H_IN:.3f} in")
