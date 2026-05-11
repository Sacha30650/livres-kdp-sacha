"""
Génère le PDF intérieur KDP de 'Lila et la clé du grenier'
Format : 646.016 × 646.016 pts (= 8.972" carré, format Iggy)
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from pathlib import Path
import io

# ============================================================
# CONSTANTES
# ============================================================
IMG_DIR = Path("/home/claude/lila_images")
OUT_PDF = Path("/home/claude/lila_interieur.pdf")

# Format KDP : 646.016 pts × 646.016 pts (Iggy)
# Travaillons à 2048×2048 px natif (résolution des images générées)
W = H = 2048

# Fonts
FONT_BODY = "/usr/share/fonts/truetype/google-fonts/Lora-Variable.ttf"
FONT_BODY_ITALIC = "/usr/share/fonts/truetype/google-fonts/Lora-Italic-Variable.ttf"
FONT_HANDWRITTEN = "/usr/local/lib/python3.12/dist-packages/font_amatic_sc/files/AmaticSC-Bold.ttf"

# Couleur encre
INK = (58, 31, 16)       # marron foncé chaud
INK_SOFT = (90, 53, 32)

# ============================================================
# TEXTES DU LIVRE
# ============================================================
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


def make_caption_overlay(width, height, banner_height_ratio=0.30, fade_height_ratio=0.06):
    """Crée un bandeau crème opaque en bas avec transition douce vers l'image.
    - banner_height_ratio : hauteur de la zone bien opaque (30% du bas)
    - fade_height_ratio : hauteur de la transition au-dessus du bandeau
    """
    overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    px = overlay.load()
    cream = (251, 246, 236)

    banner_top = int(height * (1 - banner_height_ratio))         # début bandeau opaque
    fade_top = int(banner_top - height * fade_height_ratio)      # début transition

    for y in range(height):
        if y < fade_top:
            alpha = 0
        elif y < banner_top:
            # Transition douce (smoothstep)
            t = (y - fade_top) / (banner_top - fade_top)
            t = t * t * (3 - 2 * t)  # smoothstep
            alpha = int(t * 250)
        else:
            alpha = 250  # bandeau quasi-opaque (légèrement translucide pour ne pas faire "plaqué")
        for x in range(width):
            px[x, y] = (*cream, alpha)
    return overlay


def draw_centered_text_block(draw, text, font, y_start, image_width, fill, line_spacing=1.25):
    """Dessine un bloc de texte multi-lignes centré horizontalement.
    Retourne le y final."""
    lines = text.split("\n")
    # Mesurer la hauteur d'une ligne
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
    """Pose le texte avec dégradé crème sur l'illustration."""
    img = Image.open(img_path).convert("RGB")
    if img.size != (out_size, out_size):
        img = img.resize((out_size, out_size), Image.LANCZOS)

    # 1) Bandeau crème en bas pour zone de texte (compact, ne mange pas l'illustration)
    overlay = make_caption_overlay(out_size, out_size,
                                    banner_height_ratio=0.20,
                                    fade_height_ratio=0.04)
    img = img.convert("RGBA")
    img = Image.alpha_composite(img, overlay)
    img = img.convert("RGB")

    # 2) Texte du caption (Lora ~52pt, poids 600 = SemiBold)
    draw = ImageDraw.Draw(img)
    font_caption = ImageFont.truetype(FONT_BODY, 56)
    font_caption.set_variation_by_axes([600])  # poids 600 (semibold)

    # Texte centré dans le bandeau crème (bandeau commence à 80%, opaque jusqu'à 100%)
    # Centre du bandeau ≈ 90% de la hauteur
    n_lines = len(text.split("\n"))
    text_block_h = n_lines * 72
    text_y_start = int(out_size * 0.89) - text_block_h // 2
    draw_centered_text_block(draw, text, font_caption, text_y_start, out_size,
                              fill=INK, line_spacing=1.28)

    # 3) Numéro de page (bas droit, discret, dans le bandeau)
    font_pagenum = ImageFont.truetype(FONT_BODY_ITALIC, 28)
    page_label = str(page_num)
    bbox = draw.textbbox((0, 0), page_label, font=font_pagenum)
    pw = bbox[2] - bbox[0]
    draw.text((out_size - pw - 80, out_size - 55), page_label,
              font=font_pagenum, fill=INK_SOFT)

    return img


def render_title_page(out_size=W):
    """Page de titre : sur fond crème uni, titre élégant."""
    img = Image.new("RGB", (out_size, out_size), (251, 246, 236))
    draw = ImageDraw.Draw(img)

    # Ornement haut : trois petits filets dessinés (sûr, pas de glyphe manquant)
    def draw_ornament(y_center):
        line_color = INK_SOFT
        center_x = out_size // 2
        line_w = 80
        gap = 30
        thickness = 4
        # 3 petites lignes côte à côte
        for offset in [-1, 0, 1]:
            x_start = center_x + offset * (line_w + gap) - line_w // 2
            draw.rectangle([x_start, y_center - thickness // 2,
                            x_start + line_w, y_center + thickness // 2],
                           fill=line_color)

    draw_ornament(int(out_size * 0.26))

    # Petite intro
    f_intro = ImageFont.truetype(FONT_BODY_ITALIC, 52)
    f_intro.set_variation_by_axes([450])
    intro = "Une histoire à lire le soir,\nquand on a très envie de rêver"
    draw_centered_text_block(draw, intro, f_intro,
                              int(out_size * 0.12), out_size, INK_SOFT, 1.3)

    # Titre central
    f_title = ImageFont.truetype(FONT_BODY, 180)
    f_title.set_variation_by_axes([600])
    title = "Lila\net la clé\ndu grenier"
    n_lines = 3
    block_h = 200 * n_lines
    draw_centered_text_block(draw, title, f_title,
                              int((out_size - block_h) // 2), out_size, INK, 1.05)

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
    """Page Fin"""
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
    f_final = ImageFont.truetype(FONT_BODY_ITALIC, 64)
    f_final.set_variation_by_axes([450])
    final_text = "… mais la clé reste là,\nau fond du coffre,\nprête pour la prochaine aventure."
    draw_centered_text_block(draw, final_text, f_final,
                              int(out_size * 0.56), out_size, INK_SOFT, 1.4)
    return img


def render_copyright_page(out_size=W):
    """Page copyright/colophon obligatoire KDP."""
    img = Image.new("RGB", (out_size, out_size), (251, 246, 236))
    draw = ImageDraw.Draw(img)

    f_title = ImageFont.truetype(FONT_BODY, 56)
    f_title.set_variation_by_axes([600])
    f_body = ImageFont.truetype(FONT_BODY, 44)
    f_body.set_variation_by_axes([400])
    f_body_it = ImageFont.truetype(FONT_BODY_ITALIC, 44)
    f_body_it.set_variation_by_axes([400])

    y = int(out_size * 0.22)
    # Titre
    title = "Lila et la clé du grenier"
    bbox = draw.textbbox((0, 0), title, font=f_title)
    draw.text(((out_size - (bbox[2] - bbox[0])) // 2, y),
              title, font=f_title, fill=INK)
    y += 100

    # Auteur
    auteur = "Apolline Verger"
    bbox = draw.textbbox((0, 0), auteur, font=f_body_it)
    draw.text(((out_size - (bbox[2] - bbox[0])) // 2, y),
              auteur, font=f_body_it, fill=INK_SOFT)
    y += 180

    # Collection
    f_small = ImageFont.truetype(FONT_BODY, 38)
    f_small.set_variation_by_axes([400])
    coll = "Collection « Au seuil des merveilles »"
    bbox = draw.textbbox((0, 0), coll, font=f_small)
    draw.text(((out_size - (bbox[2] - bbox[0])) // 2, y),
              coll, font=f_small, fill=INK_SOFT)
    y += 220

    # Mentions
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
print("📖 Génération du PDF intérieur 'Lila et la clé du grenier'…")
print(f"   Format cible : 8.972\" × 8.972\" carré (= 646pt, format Iggy)")
print(f"   Résolution natif image : {W} × {H} px")
print()

pages = []

# 1) Page de titre
print("  → Page de titre")
pages.append(render_title_page())

# 2) Page copyright
print("  → Page copyright")
pages.append(render_copyright_page())

# 3) Pages d'histoire 1 à 30
for p in range(1, 31):
    print(f"  → Page {p:02d}")
    pages.append(render_story_page(
        IMG_DIR / f"p{p:02d}.png",
        PAGES_TEXT[p],
        p,
    ))

# 4) Page Fin
print("  → Page Fin")
pages.append(render_end_page())

# ============================================================
# SAUVEGARDE PDF AVEC RÉSOLUTION CORRECTE POUR KDP
# ============================================================
# Pour que le PDF s'affiche à 8.972"×8.972" à partir d'images 2048×2048,
# on définit la résolution effective : 2048 / 8.972 = 228.27 DPI
# C'est ce que PIL utilisera pour stocker la taille physique dans le PDF.
DPI = 2048 / 8.972  # ≈ 228.27

print()
print(f"💾 Écriture PDF (DPI effectif : {DPI:.1f})…")
pages[0].save(
    OUT_PDF,
    save_all=True,
    append_images=pages[1:],
    format="PDF",
    resolution=DPI,
)

print(f"✓ PDF intérieur sauvegardé : {OUT_PDF}")
print(f"  Nombre de pages : {len(pages)}")
import os
print(f"  Taille : {os.path.getsize(OUT_PDF) / 1024 / 1024:.1f} MB")
