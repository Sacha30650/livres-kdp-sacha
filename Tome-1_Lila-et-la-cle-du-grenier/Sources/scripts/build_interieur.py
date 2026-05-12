"""
Génère le PDF intérieur KDP de 'Lila et la clé du grenier' VERSION 2 (avec bleed)

CORRECTIONS PAR RAPPORT V1 :
- Canvas PDF passe de 8.972" à 9.222" (= trim 8.972" + bleed 0.125" tout autour)
- Les images sont étendues jusqu'au bord du bleed (full bleed)
- Le texte est positionné dans une zone safe à >= 0.375" des bords trim
- Le bandeau crème reste en bas mais le texte ne touche jamais la zone de coupe
"""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

# ============================================================
# CONSTANTES KDP
# ============================================================
IMG_DIR = Path("/home/claude/lila_images")
OUT_PDF = Path("/home/claude/lila_interieur_v2.pdf")

TRIM_IN = 8.972
BLEED_IN = 0.125
SAFETY_IN = 0.375

PAGE_IN = TRIM_IN + 2 * BLEED_IN

DPI = 228
PAGE_PX = round(PAGE_IN * DPI)
BLEED_PX = round(BLEED_IN * DPI)
SAFETY_PX = round(SAFETY_IN * DPI)

# Coordonnées dans le canvas PAGE_PX × PAGE_PX
SAFE_LEFT = BLEED_PX + SAFETY_PX
SAFE_RIGHT = PAGE_PX - BLEED_PX - SAFETY_PX
SAFE_TOP = BLEED_PX + SAFETY_PX
SAFE_BOTTOM = PAGE_PX - BLEED_PX - SAFETY_PX
SAFE_WIDTH = SAFE_RIGHT - SAFE_LEFT

TRIM_TOP = BLEED_PX
TRIM_BOTTOM = PAGE_PX - BLEED_PX

FONT_BODY = "/usr/share/fonts/truetype/google-fonts/Lora-Variable.ttf"
FONT_BODY_ITALIC = "/usr/share/fonts/truetype/google-fonts/Lora-Italic-Variable.ttf"

INK = (58, 31, 16)
INK_SOFT = (90, 53, 32)
CREAM = (251, 246, 236)

print(f"📐 Format PDF cible : {PAGE_IN}\" × {PAGE_IN}\" ({PAGE_PX}×{PAGE_PX} px à {DPI} DPI)")
print(f"   Trim : {TRIM_IN}\" centré, bleed 0.125\" tout autour")
print(f"   Safety zone : {SAFETY_IN}\" depuis le trim")
print(f"   Zone safe utilisable : {SAFE_WIDTH}×{SAFE_WIDTH} px ({SAFE_WIDTH/DPI:.2f}\")")
print()

PAGES_TEXT = {
    1:  "Lila arrive chez sa grand-mère.\nCet été, une aventure magique l'attend.",
    2:  "Au grenier, la poussière danse dans la lumière.\nQuel mystère se cache ici ?",
    3:  "Une vieille clé en bronze brille au fond d'un coffre.\nEt soudain, une petite porte apparaît…",
    4:  "Clic ! La clé tourne dans la serrure.\nUne lumière verte tourbillonne autour d'elle.",
    5:  "Lila est devenue toute petite !\nUne marguerite la dépasse, immense comme un arbre.",
    6:  "« Bonjour ! » lui dit une coccinelle.\n« Veux-tu monter sur mon dos ? »",
    7:  "Elles survolent l'étang.\nLes gouttes de rosée brillent comme des perles.",
    8:  "Au pied d'un trèfle, une porte miroitante l'attend.\nLila la pousse doucement.",
    9:  "Plouf ! Lila plonge dans l'océan turquoise.\nQuelle surprise : elle peut respirer sous l'eau !",
    10: "Une ville en corail s'éclaire de mille feux.\nDes méduses dansent tout autour d'elle.",
    11: "Un hippocampe doré lui remet un message\ncaché dans une petite bouteille.",
    12: "Le roi-pieuvre l'invite à son banquet.\nLes algues lumineuses sont délicieuses !",
    13: "Au cœur d'un nautile géant,\nune porte nacrée attend Lila.",
    14: "Lila pose le pied sur un nuage rose.\nLe ciel s'étend à l'infini.",
    15: "Les Nuagets bondissent autour d'elle, tout doux.\nQu'est-ce qu'on rit !",
    16: "Elle traverse un pont arc-en-ciel.\nTout est si haut, si beau !",
    17: "L'orage gronde dans le ciel.\nLila aide les Nuagets à récolter la pluie dans des seaux.",
    18: "Une porte est gravée dans un éclair.\nLila prend son courage à deux mains.",
    19: "La voilà dans une forêt nocturne.\nDes milliers de lucioles éclairent son chemin.",
    20: "Un renard argenté apparaît.\n« Suis-moi », semble-t-il dire.",
    21: "Dans la clairière, un cerf majestueux la regarde.\nSes bois brillent comme des étoiles.",
    22: "Autour du feu, Lila danse avec lapins,\nchouette et hérisson.",
    23: "Dans le tronc d'un vieux chêne,\nune porte sculptée s'ouvre devant elle.",
    24: "Lila entre dans une horlogerie sans fin.\nLes engrenages dorés tournent tout autour.",
    25: "« Chaque porte est un instant »,\nlui dit la vieille horlogère.",
    26: "Lila grimpe sur l'aiguille géante.\nLa ville en dessous ressemble à un rêve.",
    27: "Dans le sablier, une grande Lila\nlui fait un clin d'œil complice.",
    28: "L'horlogère lui tend une dernière porte :\ncelle du retour à la maison.",
    29: "De retour au grenier, la clé est tiède dans sa main.\nAu loin, le soleil se couche.",
    30: "Lila range la clé dans le coffre.\nMamie sourit : « Tu as fait de beaux rêves ? »",
}


def make_caption_overlay(width, height, banner_start_y, fade_height=70):
    """Bandeau crème opaque qui démarre à banner_start_y (en pixels) jusqu'au bas."""
    overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    px = overlay.load()
    fade_start_y = banner_start_y - fade_height

    for y in range(height):
        if y < fade_start_y:
            alpha = 0
        elif y < banner_start_y:
            t = (y - fade_start_y) / fade_height
            t = t * t * (3 - 2 * t)
            alpha = int(t * 250)
        else:
            alpha = 250
        for x in range(width):
            px[x, y] = (*CREAM, alpha)
    return overlay


def draw_centered_text_in_safe_zone(draw, text, font, y_start, fill, line_spacing=1.28):
    """Texte centré horizontalement, contraint à la zone safe."""
    lines = text.split("\n")
    bbox = draw.textbbox((0, 0), "Ag", font=font)
    line_h = bbox[3] - bbox[1]
    line_h_with_spacing = int(line_h * line_spacing)

    y = y_start
    center_x = (SAFE_LEFT + SAFE_RIGHT) // 2
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        text_w = bbox[2] - bbox[0]
        x = center_x - text_w // 2
        draw.text((x, y), line, font=font, fill=fill)
        y += line_h_with_spacing
    return y


def render_story_page(img_path, text, page_num):
    """Pose l'illustration en full-bleed + texte dans la zone safe."""
    src = Image.open(img_path).convert("RGB")

    canvas = Image.new("RGB", (PAGE_PX, PAGE_PX), CREAM)
    img_scaled = src.resize((PAGE_PX, PAGE_PX), Image.LANCZOS)
    canvas.paste(img_scaled, (0, 0))
    canvas = canvas.convert("RGBA")

    # Bandeau crème : démarre au niveau correspondant à 78% du trim
    banner_start_y = TRIM_TOP + int((TRIM_BOTTOM - TRIM_TOP) * 0.78)
    overlay = make_caption_overlay(PAGE_PX, PAGE_PX, banner_start_y, fade_height=80)
    canvas = Image.alpha_composite(canvas, overlay)
    canvas = canvas.convert("RGB")

    draw = ImageDraw.Draw(canvas)
    font_caption = ImageFont.truetype(FONT_BODY, 56)
    font_caption.set_variation_by_axes([600])

    n_lines = len(text.split("\n"))
    text_block_h = n_lines * 72

    # Centrer le texte verticalement entre le début du bandeau et SAFE_BOTTOM
    text_zone_center_y = (banner_start_y + SAFE_BOTTOM) // 2
    text_y_start = text_zone_center_y - text_block_h // 2

    draw_centered_text_in_safe_zone(draw, text, font_caption, text_y_start,
                                     fill=INK, line_spacing=1.28)

    # Numéro de page dans la zone safe
    font_pagenum = ImageFont.truetype(FONT_BODY_ITALIC, 28)
    page_label = str(page_num)
    bbox = draw.textbbox((0, 0), page_label, font=font_pagenum)
    pw = bbox[2] - bbox[0]
    draw.text((SAFE_RIGHT - pw, SAFE_BOTTOM - 35), page_label,
              font=font_pagenum, fill=INK_SOFT)

    return canvas


def render_title_page():
    img = Image.new("RGB", (PAGE_PX, PAGE_PX), CREAM)
    draw = ImageDraw.Draw(img)

    def draw_ornament(y_center):
        center_x = PAGE_PX // 2
        line_w = 80
        gap = 30
        thickness = 4
        for offset in [-1, 0, 1]:
            x_start = center_x + offset * (line_w + gap) - line_w // 2
            draw.rectangle([x_start, y_center - thickness // 2,
                            x_start + line_w, y_center + thickness // 2],
                           fill=INK_SOFT)

    f_intro = ImageFont.truetype(FONT_BODY_ITALIC, 52)
    f_intro.set_variation_by_axes([450])
    intro = "Une histoire à lire le soir,\nquand on a très envie de rêver"
    draw_centered_text_in_safe_zone(draw, intro, f_intro,
                                     int(PAGE_PX * 0.14), INK_SOFT, 1.3)

    draw_ornament(int(PAGE_PX * 0.27))

    f_title = ImageFont.truetype(FONT_BODY, 180)
    f_title.set_variation_by_axes([600])
    title = "Lila\net la clé\ndu grenier"
    n_lines = 3
    block_h = 200 * n_lines
    draw_centered_text_in_safe_zone(draw, title, f_title,
                                     int((PAGE_PX - block_h) // 2), INK, 1.05)

    draw_ornament(int(PAGE_PX * 0.78))

    f_aud = ImageFont.truetype(FONT_BODY_ITALIC, 52)
    f_aud.set_variation_by_axes([450])
    aud = "Pour les petits explorateurs\nde 6 à 8 ans"
    draw_centered_text_in_safe_zone(draw, aud, f_aud,
                                     int(PAGE_PX * 0.86), INK_SOFT, 1.3)
    return img


def render_end_page():
    img = Image.new("RGB", (PAGE_PX, PAGE_PX), CREAM)
    draw = ImageDraw.Draw(img)

    f_fin = ImageFont.truetype(FONT_BODY, 280)
    f_fin.set_variation_by_axes([600])
    fin = "Fin"
    bbox = draw.textbbox((0, 0), fin, font=f_fin)
    fw = bbox[2] - bbox[0]
    fh = bbox[3] - bbox[1]
    draw.text(((PAGE_PX - fw) // 2, int(PAGE_PX * 0.34) - fh // 2),
              fin, font=f_fin, fill=INK)

    f_final = ImageFont.truetype(FONT_BODY_ITALIC, 64)
    f_final.set_variation_by_axes([450])
    final_text = "… mais la clé reste là,\nau fond du coffre,\nprête pour la prochaine aventure."
    draw_centered_text_in_safe_zone(draw, final_text, f_final,
                                     int(PAGE_PX * 0.56), INK_SOFT, 1.4)
    return img


def render_copyright_page():
    img = Image.new("RGB", (PAGE_PX, PAGE_PX), CREAM)
    draw = ImageDraw.Draw(img)

    f_title = ImageFont.truetype(FONT_BODY, 56)
    f_title.set_variation_by_axes([600])
    f_body_it = ImageFont.truetype(FONT_BODY_ITALIC, 44)
    f_body_it.set_variation_by_axes([400])

    y = int(PAGE_PX * 0.23)

    title = "Lila et la clé du grenier"
    bbox = draw.textbbox((0, 0), title, font=f_title)
    draw.text(((PAGE_PX - (bbox[2] - bbox[0])) // 2, y),
              title, font=f_title, fill=INK)
    y += 100

    auteur = "Apolline Verger"
    bbox = draw.textbbox((0, 0), auteur, font=f_body_it)
    draw.text(((PAGE_PX - (bbox[2] - bbox[0])) // 2, y),
              auteur, font=f_body_it, fill=INK_SOFT)
    y += 180

    f_small = ImageFont.truetype(FONT_BODY, 38)
    f_small.set_variation_by_axes([400])
    coll = "Collection « Au seuil des merveilles »"
    bbox = draw.textbbox((0, 0), coll, font=f_small)
    draw.text(((PAGE_PX - (bbox[2] - bbox[0])) // 2, y),
              coll, font=f_small, fill=INK_SOFT)
    y += 220

    mentions = [
        ("© 2026 Apolline Verger", f_small),
        ("Tous droits réservés.", f_body_it.font_variant(size=36)),
        ("", None),
        ("Aucune partie de ce livre ne peut être", f_body_it.font_variant(size=32)),
        ("reproduite sans l'autorisation écrite de l'auteur.", f_body_it.font_variant(size=32)),
        ("", None),
        ("Première édition", f_small),
        ("", None),
        ("Imprimé via Amazon KDP", f_body_it.font_variant(size=32)),
    ]
    for text, font in mentions:
        if not text:
            y += 36
            continue
        bbox = draw.textbbox((0, 0), text, font=font)
        draw.text(((PAGE_PX - (bbox[2] - bbox[0])) // 2, y),
                  text, font=font, fill=INK_SOFT)
        y += 56
    return img


# ============================================================
# BUILD PDF
# ============================================================
pages = []

print("  → Page de titre")
pages.append(render_title_page())

print("  → Page copyright")
pages.append(render_copyright_page())

for p in range(1, 31):
    print(f"  → Page {p:02d}")
    pages.append(render_story_page(
        IMG_DIR / f"p{p:02d}.png",
        PAGES_TEXT[p],
        p,
    ))

print("  → Page Fin")
pages.append(render_end_page())

print()
print(f"💾 Écriture PDF (DPI : {DPI})…")
pages[0].save(
    OUT_PDF,
    save_all=True,
    append_images=pages[1:],
    format="PDF",
    resolution=DPI,
)

import os
print(f"✓ PDF intérieur v2 : {OUT_PDF}")
print(f"  Pages : {len(pages)}")
print(f"  Taille : {os.path.getsize(OUT_PDF) / 1024 / 1024:.1f} MB")
