"""
Génère le PDF intérieur KDP de 'Lila et la clé du grenier' (Tome 2)
VERSION 2 : avec bleed 0.125" inclus + safety zone 0.375" respectée pour le texte

Specs KDP :
- Trim : 8.972 × 8.972 in
- Bleed : 0.125 in sur les 4 côtés
- Canvas total PDF : 9.222 × 9.222 in (= 663.984 pts)
- Safety zone texte : >= 0.375 in depuis bord trim (donc >= 0.5 in depuis bord PDF)
"""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

# ============================================================
# CONSTANTES — DIMENSIONS KDP
# ============================================================
IMG_DIR = Path("/home/claude/lila_tome2")
OUT_PDF = Path("/home/claude/lila_tome2_interieur.pdf")

# Cible en pouces
TRIM_IN = 8.972          # taille finale visible après coupe
BLEED_IN = 0.125         # débordement sur chaque bord
SAFETY_IN = 0.375        # zone à respecter pour le texte depuis le bord trim
CANVAS_IN = TRIM_IN + 2 * BLEED_IN  # 9.222"

# Travail à 228 DPI (cohérent avec couverture)
DPI = 228
CANVAS_PX = round(CANVAS_IN * DPI)       # 2103 px
TRIM_PX = round(TRIM_IN * DPI)            # 2046 px
BLEED_PX = round(BLEED_IN * DPI)          # 29 px
SAFETY_PX = round(SAFETY_IN * DPI)        # 86 px

# Coordonnées clés sur le canvas (en px)
TRIM_LEFT = BLEED_PX
TRIM_TOP = BLEED_PX
TRIM_RIGHT = BLEED_PX + TRIM_PX           # 2075
TRIM_BOTTOM = BLEED_PX + TRIM_PX

SAFE_LEFT = TRIM_LEFT + SAFETY_PX         # 115
SAFE_TOP = TRIM_TOP + SAFETY_PX
SAFE_RIGHT = TRIM_RIGHT - SAFETY_PX       # 1989
SAFE_BOTTOM = TRIM_BOTTOM - SAFETY_PX
SAFE_WIDTH = SAFE_RIGHT - SAFE_LEFT

# Fonts
FONT_BODY = "/usr/share/fonts/truetype/google-fonts/Lora-Variable.ttf"
FONT_BODY_ITALIC = "/usr/share/fonts/truetype/google-fonts/Lora-Italic-Variable.ttf"
FONT_HANDWRITTEN = "/usr/local/lib/python3.12/dist-packages/font_amatic_sc/files/AmaticSC-Bold.ttf"

INK = (58, 31, 16)
INK_SOFT = (90, 53, 32)
CREAM = (251, 246, 236)

print(f"📐 Canvas total : {CANVAS_IN:.3f}\" ({CANVAS_PX}×{CANVAS_PX} px @ {DPI} DPI)")
print(f"📐 Zone trim    : {TRIM_IN:.3f}\" ({TRIM_PX}×{TRIM_PX} px), offset {BLEED_PX} px")
print(f"📐 Zone safety  : {SAFE_RIGHT - SAFE_LEFT} px de large, à {SAFETY_PX} px du trim")
print()

# ============================================================
# TEXTES TOME 1
# ============================================================
PAGES_TEXT = {
    1:  "Au grenier de Mamie, la clé en bronze se met à trembler.\n« C'est qu'elle a senti les autres », murmure Mamie en souriant.",
    2:  "« Il y a quatre autres greniers dans le monde, Lila.\nQuatre autres enfants. Quatre autres clés. »",
    3:  "Lila tourne sa clé… et atterrit dans un autre grenier !\nUn garçon en kimono la regarde sans bouger.",
    4:  "« Je m'appelle Akira », dit-il en souriant.\nSa clé en argent brille à son cou.",
    5:  "Sa clé ouvre un monde tout en papier de soie.\nUne grue géante les emporte sous une pluie de pétales roses.",
    6:  "Akira souffle sur un origami : un dragon prend vie !\nLila apprend à plier la patience comme un origami.",
    7:  "Cette fois, c'est la clé d'Akira qui s'est mise à chanter.\n« Au sud », a-t-il dit. « Quelqu'un nous appelle. »",
    8:  "Le grenier de Zola sent le bois chaud et les épices.\nDes tambours et des masques peints tapissent les murs.",
    9:  "Zola court partout, elle n'a peur de rien.\nSa clé en or scintille comme un petit soleil.",
    10: "Dans sa savane miniature, l'herbe est haute comme des cathédrales.\nUn troupeau de zèbres minuscules passe en galopant.",
    11: "Un baobab parle avec une voix de grand-père.\n« Les petits courageux deviennent les plus grands. »",
    12: "Un lion de poussière de soleil rugit doucement.\nLila n'a plus peur du tout.",
    13: "Inès peignait un papillon orange sur le mur.\n« Vous êtes en retard », dit-elle sans se retourner.",
    14: "Son grenier est plein de papiers découpés et d'alebrijes.\nDes animaux fantastiques aux mille couleurs.",
    15: "Sa clé en cuivre ouvre une grande calabaza orange.\nÀ l'intérieur : toute une cité magique illuminée !",
    16: "Des squelettes-musiciens jouent du mariachi.\nLes rues sentent le chocolat chaud et la cannelle.",
    17: "Un alebrije-jaguar bleu et rose les invite à danser.\nLa nuit s'allume de mille lanternes papier.",
    18: "Inès chante, et sa timidité s'envole.\n« C'est ici que j'apprends à être moi. »",
    19: "Noor regardait par la lucarne quand ils arrivent.\n« Cette étoile, là-bas… elle nous attend depuis longtemps. »",
    20: "Son grenier surplombe la Méditerranée bleue.\nDes cartes du ciel et des télescopes anciens partout.",
    21: "Sa clé turquoise ouvre un désert d'étoiles.\nLe sable scintille comme la Voie lactée.",
    22: "Des pyramides flottent doucement au-dessus des dunes.\nC'est silencieux, c'est immense, c'est magique.",
    23: "Des chats sacrés bleus surgissent du sable étoilé.\nIls les guident, en clignant des yeux dorés.",
    24: "Au pied d'un Sphinx, ils s'arrêtent enfin.\n« Il existe une porte… qu'aucun de vous ne peut ouvrir seul. »",
    25: "Les cinq enfants se retrouvent, pour la première fois ensemble.\nUne aurore boréale danse au-dessus de l'océan.",
    26: "Au centre : une immense porte de bois sculpté.\nCinq serrures différentes scintillent sur sa face.",
    27: "Ils tournent leurs cinq clés en même temps.\nClic ! Le bois s'ouvre dans un soupir d'étoiles.",
    28: "Derrière la porte : un globe de cristal géant.\nTous leurs mondes y tournent en même temps.",
    29: "« Nous sommes les fenêtres d'une même grande maison. »\nLes cinq amis se tiennent par la main, émerveillés.",
    30: "Chez Mamie, la clé est tiède dans la paume de Lila.\nAu loin, quatre autres enfants reposent leur clé en souriant.",
}


def make_caption_overlay(canvas_width, canvas_height, banner_top_y, banner_bottom_y, fade_px):
    """Crée un bandeau crème opaque positionné précisément en px, avec transition douce au-dessus."""
    overlay = Image.new("RGBA", (canvas_width, canvas_height), (0, 0, 0, 0))
    px = overlay.load()
    fade_start = banner_top_y - fade_px

    for y in range(canvas_height):
        if y < fade_start:
            alpha = 0
        elif y < banner_top_y:
            t = (y - fade_start) / fade_px
            t = t * t * (3 - 2 * t)  # smoothstep
            alpha = int(t * 250)
        elif y <= banner_bottom_y:
            alpha = 250
        else:
            alpha = 250  # le bandeau peut s'étendre jusqu'au bord du bleed
        for x in range(canvas_width):
            px[x, y] = (*CREAM, alpha)
    return overlay


def draw_centered_text_block(draw, text, font, y_start, x_left, x_right,
                              fill, line_spacing=1.28):
    """Dessine du texte centré horizontalement dans la zone [x_left, x_right]."""
    lines = text.split("\n")
    bbox_ref = draw.textbbox((0, 0), "Ag", font=font)
    line_h = bbox_ref[3] - bbox_ref[1]
    line_h_with_spacing = int(line_h * line_spacing)
    y = y_start
    panel_center_x = (x_left + x_right) // 2
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        text_w = bbox[2] - bbox[0]
        x = panel_center_x - text_w // 2
        draw.text((x, y), line, font=font, fill=fill)
        y += line_h_with_spacing
    return y


def render_story_page(img_path, text, page_num):
    """Rendre une page d'histoire au format canvas (avec bleed)."""
    # 1) Charger l'image source (2048×2048)
    img_src = Image.open(img_path).convert("RGB")
    # 2) Redimensionner pour remplir tout le CANVAS (donc déborder dans le bleed)
    img_src = img_src.resize((CANVAS_PX, CANVAS_PX), Image.LANCZOS)

    # 3) Le bandeau crème occupe la partie basse, SE TERMINANT à TRIM_BOTTOM pour respecter safety
    # Le bandeau doit occuper environ 20% de la hauteur du trim
    banner_height_px = round(0.22 * TRIM_PX)
    banner_top_y = TRIM_BOTTOM - banner_height_px
    banner_bottom_y = CANVAS_PX  # va jusqu'au bord du PDF (dans le bleed)
    fade_px = round(0.04 * TRIM_PX)

    overlay = make_caption_overlay(CANVAS_PX, CANVAS_PX,
                                    banner_top_y, banner_bottom_y, fade_px)
    canvas = img_src.convert("RGBA")
    canvas = Image.alpha_composite(canvas, overlay)
    canvas = canvas.convert("RGB")

    draw = ImageDraw.Draw(canvas)

    # 4) Texte de l'histoire : DANS LA SAFETY ZONE
    # Police 56 pt à 228 DPI ~ 178 px de haut
    font_caption = ImageFont.truetype(FONT_BODY, 56)
    font_caption.set_variation_by_axes([600])

    # On centre verticalement le texte dans le bandeau
    n_lines = len(text.split("\n"))
    line_h_total = n_lines * round(56 * 1.28 * (DPI / 72))  # estimation
    # Centre vertical du bandeau visible (au-dessus du bord trim)
    banner_visible_center_y = (banner_top_y + TRIM_BOTTOM) // 2

    text_y_start = banner_visible_center_y - line_h_total // 2 - 30
    # Mais on s'assure de rester DANS la safety zone
    text_y_start = max(text_y_start, banner_top_y + 30)

    draw_centered_text_block(draw, text, font_caption,
                              text_y_start,
                              SAFE_LEFT, SAFE_RIGHT,
                              fill=INK, line_spacing=1.28)

    # 5) Numéro de page : à l'intérieur de la safety zone, en bas à droite
    font_pagenum = ImageFont.truetype(FONT_BODY_ITALIC, 28)
    page_label = str(page_num)
    bbox = draw.textbbox((0, 0), page_label, font=font_pagenum)
    pw = bbox[2] - bbox[0]
    # Position : à SAFE_RIGHT, à 30 px de SAFE_BOTTOM
    draw.text((SAFE_RIGHT - pw, SAFE_BOTTOM - 35),
              page_label, font=font_pagenum, fill=INK_SOFT)

    return canvas


def render_blank_canvas():
    """Canvas crème uni avec bleed."""
    return Image.new("RGB", (CANVAS_PX, CANVAS_PX), CREAM)


def render_title_page():
    """Page de titre, texte dans safety zone."""
    img = render_blank_canvas()
    draw = ImageDraw.Draw(img)

    # Ornement
    def draw_ornament(y_center):
        cx = CANVAS_PX // 2
        line_w, gap, thickness = 80, 30, 4
        for offset in [-1, 0, 1]:
            x_start = cx + offset * (line_w + gap) - line_w // 2
            draw.rectangle([x_start, y_center - thickness // 2,
                            x_start + line_w, y_center + thickness // 2],
                           fill=INK_SOFT)

    # Calculs verticaux : on travaille dans la safety zone
    inner_h = SAFE_BOTTOM - SAFE_TOP

    # Intro
    f_intro = ImageFont.truetype(FONT_BODY_ITALIC, 52)
    f_intro.set_variation_by_axes([450])
    intro = "Une histoire à lire le soir,\nquand on a très envie de voyager"
    draw_centered_text_block(draw, intro, f_intro,
                              SAFE_TOP + round(inner_h * 0.10),
                              SAFE_LEFT, SAFE_RIGHT, INK_SOFT, 1.3)

    draw_ornament(SAFE_TOP + round(inner_h * 0.27))

    # Titre principal
    f_title_main = ImageFont.truetype(FONT_BODY, 160)
    f_title_main.set_variation_by_axes([600])
    f_title_it = ImageFont.truetype(FONT_BODY_ITALIC, 105)
    f_title_it.set_variation_by_axes([500])

    panel_center = CANVAS_PX // 2
    y = SAFE_TOP + round(inner_h * 0.33)

    bbox = draw.textbbox((0, 0), "Lila", font=f_title_main)
    tw = bbox[2] - bbox[0]
    draw.text((panel_center - tw // 2, y), "Lila", font=f_title_main, fill=INK)
    y += round(inner_h * 0.11)

    bbox = draw.textbbox((0, 0), "et le grenier des autres", font=f_title_it)
    tw = bbox[2] - bbox[0]
    draw.text((panel_center - tw // 2, y), "et le grenier des autres",
              font=f_title_it, fill=INK_SOFT)

    draw_ornament(SAFE_TOP + round(inner_h * 0.78))

    # Audience
    f_aud = ImageFont.truetype(FONT_BODY_ITALIC, 52)
    f_aud.set_variation_by_axes([450])
    aud = "Pour les petits explorateurs\nde 6 à 8 ans"
    draw_centered_text_block(draw, aud, f_aud,
                              SAFE_TOP + round(inner_h * 0.85),
                              SAFE_LEFT, SAFE_RIGHT, INK_SOFT, 1.3)

    return img


def render_copyright_page():
    img = render_blank_canvas()
    draw = ImageDraw.Draw(img)

    f_title = ImageFont.truetype(FONT_BODY, 56)
    f_title.set_variation_by_axes([600])
    f_body = ImageFont.truetype(FONT_BODY, 44)
    f_body.set_variation_by_axes([400])
    f_body_it = ImageFont.truetype(FONT_BODY_ITALIC, 44)
    f_body_it.set_variation_by_axes([400])

    inner_h = SAFE_BOTTOM - SAFE_TOP
    y = SAFE_TOP + round(inner_h * 0.20)

    def center_text(text, font, y_pos, fill):
        bbox = draw.textbbox((0, 0), text, font=font)
        draw.text(((CANVAS_PX - (bbox[2] - bbox[0])) // 2, y_pos),
                  text, font=font, fill=fill)

    center_text("Lila et le grenier des autres", f_title, y, INK)
    y += 100
    center_text("Apolline Verger", f_body_it, y, INK_SOFT)
    y += 180

    f_small = ImageFont.truetype(FONT_BODY, 38)
    f_small.set_variation_by_axes([400])
    center_text("Collection « Au seuil des merveilles » · Tome 2",
                f_small, y, INK_SOFT)
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
        center_text(text, font, y, INK_SOFT)
        y += 56

    return img


def render_end_page():
    img = render_blank_canvas()
    draw = ImageDraw.Draw(img)
    inner_h = SAFE_BOTTOM - SAFE_TOP

    f_fin = ImageFont.truetype(FONT_BODY, 280)
    f_fin.set_variation_by_axes([600])
    fin = "Fin"
    bbox = draw.textbbox((0, 0), fin, font=f_fin)
    fw = bbox[2] - bbox[0]
    fh = bbox[3] - bbox[1]
    draw.text(((CANVAS_PX - fw) // 2,
               SAFE_TOP + round(inner_h * 0.32) - fh // 2),
              fin, font=f_fin, fill=INK)

    f_final = ImageFont.truetype(FONT_BODY_ITALIC, 60)
    f_final.set_variation_by_axes([450])
    final_text = "… mais les cinq clés restent là,\nchacune au fond de son coffre,\nprêtes pour la prochaine aventure."
    draw_centered_text_block(draw, final_text, f_final,
                              SAFE_TOP + round(inner_h * 0.56),
                              SAFE_LEFT, SAFE_RIGHT, INK_SOFT, 1.4)
    return img


# ============================================================
# BUILD PDF
# ============================================================
print(f"📖 Génération du PDF intérieur 'Lila et le grenier des autres' (Tome 2) V2")
print()

pages = []
print("  → Page de titre")
pages.append(render_title_page())

print("  → Page copyright")
pages.append(render_copyright_page())

for p in range(1, 31):
    print(f"  → Page {p:02d}")
    pages.append(render_story_page(IMG_DIR / f"p{p:02d}.png", PAGES_TEXT[p], p))

print("  → Page Fin")
pages.append(render_end_page())

print()
print(f"💾 Écriture PDF…")
pages[0].save(OUT_PDF, save_all=True, append_images=pages[1:],
              format="PDF", resolution=DPI)

import os
print(f"✓ PDF intérieur Tome 2 sauvegardé : {OUT_PDF}")
print(f"  Pages : {len(pages)}")
print(f"  Taille : {os.path.getsize(OUT_PDF) / 1024 / 1024:.1f} MB")
print(f"  Format : {CANVAS_IN:.3f}\" × {CANVAS_IN:.3f}\" (bleed 0.125\" inclus)")
