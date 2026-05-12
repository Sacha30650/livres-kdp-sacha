"""
Génère le PDF intérieur KDP de 'Lila et le grenier des autres' (Tome 2) VERSION 2 (avec bleed)

CORRECTIONS PAR RAPPORT V1 :
- Canvas PDF passe de 8.972" à 9.222" (= trim 8.972" + bleed 0.125" tout autour)
- Les illustrations sont étendues jusqu'au bord du bleed (full bleed)
- Le texte est positionné dans la zone safe à >= 0.375" des bords trim
"""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

# ============================================================
# CONSTANTES KDP
# ============================================================
IMG_DIR = Path("/home/claude/lila_tome2")
OUT_PDF = Path("/home/claude/lila_tome2_interieur_v2.pdf")

TRIM_IN = 8.972
BLEED_IN = 0.125
SAFETY_IN = 0.375

PAGE_IN = TRIM_IN + 2 * BLEED_IN

DPI = 228
PAGE_PX = round(PAGE_IN * DPI)
BLEED_PX = round(BLEED_IN * DPI)
SAFETY_PX = round(SAFETY_IN * DPI)

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
print(f"   Trim : {TRIM_IN}\", bleed 0.125\", safety {SAFETY_IN}\"")
print()

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


def make_caption_overlay(width, height, banner_start_y, fade_height=80):
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
    src = Image.open(img_path).convert("RGB")
    canvas = Image.new("RGB", (PAGE_PX, PAGE_PX), CREAM)
    img_scaled = src.resize((PAGE_PX, PAGE_PX), Image.LANCZOS)
    canvas.paste(img_scaled, (0, 0))
    canvas = canvas.convert("RGBA")

    banner_start_y = TRIM_TOP + int((TRIM_BOTTOM - TRIM_TOP) * 0.78)
    overlay = make_caption_overlay(PAGE_PX, PAGE_PX, banner_start_y, fade_height=80)
    canvas = Image.alpha_composite(canvas, overlay)
    canvas = canvas.convert("RGB")

    draw = ImageDraw.Draw(canvas)
    font_caption = ImageFont.truetype(FONT_BODY, 56)
    font_caption.set_variation_by_axes([600])

    n_lines = len(text.split("\n"))
    text_block_h = n_lines * 72
    text_zone_center_y = (banner_start_y + SAFE_BOTTOM) // 2
    text_y_start = text_zone_center_y - text_block_h // 2

    draw_centered_text_in_safe_zone(draw, text, font_caption, text_y_start,
                                     fill=INK, line_spacing=1.28)

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
    intro = "Une histoire à lire le soir,\nquand on a très envie de voyager"
    draw_centered_text_in_safe_zone(draw, intro, f_intro,
                                     int(PAGE_PX * 0.14), INK_SOFT, 1.3)
    draw_ornament(int(PAGE_PX * 0.27))

    # Titre étagé
    f_title_main = ImageFont.truetype(FONT_BODY, 160)
    f_title_main.set_variation_by_axes([600])
    f_title_it = ImageFont.truetype(FONT_BODY_ITALIC, 105)
    f_title_it.set_variation_by_axes([500])

    center_x = (SAFE_LEFT + SAFE_RIGHT) // 2
    y = int(PAGE_PX * 0.34)

    bbox = draw.textbbox((0, 0), "Lila", font=f_title_main)
    tw = bbox[2] - bbox[0]
    draw.text((center_x - tw // 2, y), "Lila", font=f_title_main, fill=INK)
    y += int(PAGE_PX * 0.085)

    bbox = draw.textbbox((0, 0), "et le grenier", font=f_title_it)
    tw = bbox[2] - bbox[0]
    draw.text((center_x - tw // 2, y), "et le grenier", font=f_title_it, fill=INK_SOFT)
    y += int(PAGE_PX * 0.065)

    bbox = draw.textbbox((0, 0), "des autres", font=f_title_main)
    tw = bbox[2] - bbox[0]
    draw.text((center_x - tw // 2, y), "des autres", font=f_title_main, fill=INK)

    draw_ornament(int(PAGE_PX * 0.79))

    f_aud = ImageFont.truetype(FONT_BODY_ITALIC, 52)
    f_aud.set_variation_by_axes([450])
    aud = "Pour les petits explorateurs\nde 6 à 8 ans"
    draw_centered_text_in_safe_zone(draw, aud, f_aud,
                                     int(PAGE_PX * 0.87), INK_SOFT, 1.3)
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

    f_final = ImageFont.truetype(FONT_BODY_ITALIC, 60)
    f_final.set_variation_by_axes([450])
    final_text = "… mais les cinq clés restent là,\nchacune au fond de son coffre,\nprêtes pour la prochaine aventure."
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
    title = "Lila et le grenier des autres"
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
    coll = "Collection « Au seuil des merveilles » · Tome 2"
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
print(f"✓ {OUT_PDF}")
print(f"  Pages : {len(pages)} · Taille : {os.path.getsize(OUT_PDF) / 1024 / 1024:.1f} MB")
