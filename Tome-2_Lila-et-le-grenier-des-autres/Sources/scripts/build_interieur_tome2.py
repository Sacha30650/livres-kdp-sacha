"""
Génère le PDF intérieur KDP de 'Lila et le grenier des autres' (Tome 2)
Format : 646.016 × 646.016 pts (= 8.972" carré, format Iggy/Tome 1)
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from pathlib import Path
import io

# ============================================================
# CONSTANTES
# ============================================================
IMG_DIR = Path("/home/claude/lila_tome2")
OUT_PDF = Path("/home/claude/lila_tome2_interieur.pdf")

W = H = 2048

# Fonts
FONT_BODY = "/usr/share/fonts/truetype/google-fonts/Lora-Variable.ttf"
FONT_BODY_ITALIC = "/usr/share/fonts/truetype/google-fonts/Lora-Italic-Variable.ttf"
FONT_HANDWRITTEN = "/usr/local/lib/python3.12/dist-packages/font_amatic_sc/files/AmaticSC-Bold.ttf"

# Couleurs
INK = (58, 31, 16)
INK_SOFT = (90, 53, 32)

# ============================================================
# TEXTES TOME 2 — 30 pages
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


def make_caption_overlay(width, height, banner_height_ratio=0.20, fade_height_ratio=0.04):
    """Crée un bandeau crème opaque en bas avec transition douce vers l'image."""
    overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    px = overlay.load()
    cream = (251, 246, 236)

    banner_top = int(height * (1 - banner_height_ratio))
    fade_top = int(banner_top - height * fade_height_ratio)

    for y in range(height):
        if y < fade_top:
            alpha = 0
        elif y < banner_top:
            t = (y - fade_top) / (banner_top - fade_top)
            t = t * t * (3 - 2 * t)  # smoothstep
            alpha = int(t * 250)
        else:
            alpha = 250
        for x in range(width):
            px[x, y] = (*cream, alpha)
    return overlay


def draw_centered_text_block(draw, text, font, y_start, image_width, fill, line_spacing=1.25):
    lines = text.split("\n")
    bbox = draw.textbbox((0, 0), "Ag", font=font)
    line_h = (bbox[3] - bbox[1])
    line_h_with_spacing = int(line_h * line_spacing)

    y = y_start
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        text_w = bbox[2] - bbox[0]
        x = (image_width - text_w) // 2
        draw.text((x, y), line, font=font, fill=fill)
        y += line_h_with_spacing
    return y


def render_story_page(img_path, text, page_num, out_size=W):
    img = Image.open(img_path).convert("RGB")
    if img.size != (out_size, out_size):
        img = img.resize((out_size, out_size), Image.LANCZOS)

    # Bandeau crème en bas
    overlay = make_caption_overlay(out_size, out_size,
                                    banner_height_ratio=0.20,
                                    fade_height_ratio=0.04)
    img = img.convert("RGBA")
    img = Image.alpha_composite(img, overlay)
    img = img.convert("RGB")

    draw = ImageDraw.Draw(img)
    font_caption = ImageFont.truetype(FONT_BODY, 56)
    font_caption.set_variation_by_axes([600])

    n_lines = len(text.split("\n"))
    text_block_h = n_lines * 72
    text_y_start = int(out_size * 0.89) - text_block_h // 2
    draw_centered_text_block(draw, text, font_caption, text_y_start, out_size,
                              fill=INK, line_spacing=1.28)

    # Numéro de page
    font_pagenum = ImageFont.truetype(FONT_BODY_ITALIC, 28)
    page_label = str(page_num)
    bbox = draw.textbbox((0, 0), page_label, font=font_pagenum)
    pw = bbox[2] - bbox[0]
    draw.text((out_size - pw - 80, out_size - 55), page_label,
              font=font_pagenum, fill=INK_SOFT)

    return img


def render_title_page(out_size=W):
    img = Image.new("RGB", (out_size, out_size), (251, 246, 236))
    draw = ImageDraw.Draw(img)

    # Ornement haut
    def draw_ornament(y_center):
        line_color = INK_SOFT
        center_x = out_size // 2
        line_w = 80
        gap = 30
        thickness = 4
        for offset in [-1, 0, 1]:
            x_start = center_x + offset * (line_w + gap) - line_w // 2
            draw.rectangle([x_start, y_center - thickness // 2,
                            x_start + line_w, y_center + thickness // 2],
                           fill=line_color)

    # Petite intro
    f_intro = ImageFont.truetype(FONT_BODY_ITALIC, 52)
    f_intro.set_variation_by_axes([450])
    intro = "Une histoire à lire le soir,\nquand on a très envie de voyager"
    draw_centered_text_block(draw, intro, f_intro,
                              int(out_size * 0.12), out_size, INK_SOFT, 1.3)

    draw_ornament(int(out_size * 0.26))

    # Titre central
    f_title_main = ImageFont.truetype(FONT_BODY, 160)
    f_title_main.set_variation_by_axes([600])
    f_title_it = ImageFont.truetype(FONT_BODY_ITALIC, 105)
    f_title_it.set_variation_by_axes([500])

    panel_center = out_size // 2
    y = int(out_size * 0.32)

    # Ligne 1 : Lila
    bbox = draw.textbbox((0, 0), "Lila", font=f_title_main)
    tw = bbox[2] - bbox[0]
    draw.text((panel_center - tw // 2, y), "Lila", font=f_title_main, fill=INK)
    y += int(out_size * 0.10)

    # Ligne 2 : et le grenier (italique)
    bbox = draw.textbbox((0, 0), "et le grenier", font=f_title_it)
    tw = bbox[2] - bbox[0]
    draw.text((panel_center - tw // 2, y), "et le grenier", font=f_title_it, fill=INK_SOFT)
    y += int(out_size * 0.075)

    # Ligne 3 : des autres
    bbox = draw.textbbox((0, 0), "des autres", font=f_title_main)
    tw = bbox[2] - bbox[0]
    draw.text((panel_center - tw // 2, y), "des autres", font=f_title_main, fill=INK)

    # Ornement bas
    draw_ornament(int(out_size * 0.78))

    # Audience
    f_aud = ImageFont.truetype(FONT_BODY_ITALIC, 52)
    f_aud.set_variation_by_axes([450])
    aud = "Pour les petits explorateurs\nde 6 à 8 ans"
    draw_centered_text_block(draw, aud, f_aud,
                              int(out_size * 0.86), out_size, INK_SOFT, 1.3)

    return img


def render_end_page(out_size=W):
    img = Image.new("RGB", (out_size, out_size), (251, 246, 236))
    draw = ImageDraw.Draw(img)

    f_fin = ImageFont.truetype(FONT_BODY, 280)
    f_fin.set_variation_by_axes([600])
    fin = "Fin"
    bbox = draw.textbbox((0, 0), fin, font=f_fin)
    fw = bbox[2] - bbox[0]
    fh = bbox[3] - bbox[1]
    draw.text(((out_size - fw) // 2, int(out_size * 0.34) - fh // 2),
              fin, font=f_fin, fill=INK)

    # Phrase finale en italique
    f_final = ImageFont.truetype(FONT_BODY_ITALIC, 60)
    f_final.set_variation_by_axes([450])
    final_text = "… mais les cinq clés restent là,\nchacune au fond de son coffre,\nprêtes pour la prochaine aventure."
    draw_centered_text_block(draw, final_text, f_final,
                              int(out_size * 0.56), out_size, INK_SOFT, 1.4)
    return img


def render_copyright_page(out_size=W):
    img = Image.new("RGB", (out_size, out_size), (251, 246, 236))
    draw = ImageDraw.Draw(img)

    f_title = ImageFont.truetype(FONT_BODY, 56)
    f_title.set_variation_by_axes([600])
    f_body = ImageFont.truetype(FONT_BODY, 44)
    f_body.set_variation_by_axes([400])
    f_body_it = ImageFont.truetype(FONT_BODY_ITALIC, 44)
    f_body_it.set_variation_by_axes([400])

    y = int(out_size * 0.22)

    title = "Lila et le grenier des autres"
    bbox = draw.textbbox((0, 0), title, font=f_title)
    draw.text(((out_size - (bbox[2] - bbox[0])) // 2, y),
              title, font=f_title, fill=INK)
    y += 100

    auteur = "Apolline Verger"
    bbox = draw.textbbox((0, 0), auteur, font=f_body_it)
    draw.text(((out_size - (bbox[2] - bbox[0])) // 2, y),
              auteur, font=f_body_it, fill=INK_SOFT)
    y += 180

    f_small = ImageFont.truetype(FONT_BODY, 38)
    f_small.set_variation_by_axes([400])
    coll = "Collection « Au seuil des merveilles » · Tome 2"
    bbox = draw.textbbox((0, 0), coll, font=f_small)
    draw.text(((out_size - (bbox[2] - bbox[0])) // 2, y),
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
        draw.text(((out_size - (bbox[2] - bbox[0])) // 2, y),
                  text, font=font, fill=INK_SOFT)
        y += 56

    return img


# ============================================================
# BUILD PDF
# ============================================================
print("📖 Génération du PDF intérieur 'Lila et le grenier des autres' (Tome 2)…")
print(f"   Format cible : 8.972\" × 8.972\" carré")
print()

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

DPI = 2048 / 8.972

print()
print(f"💾 Écriture PDF (DPI effectif : {DPI:.1f})…")
pages[0].save(
    OUT_PDF,
    save_all=True,
    append_images=pages[1:],
    format="PDF",
    resolution=DPI,
)

import os
print(f"✓ PDF intérieur sauvegardé : {OUT_PDF}")
print(f"  Nombre de pages : {len(pages)}")
print(f"  Taille : {os.path.getsize(OUT_PDF) / 1024 / 1024:.1f} MB")
