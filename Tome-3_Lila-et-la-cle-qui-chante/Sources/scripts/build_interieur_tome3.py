"""
PDF intérieur Tome 3 « Lila et la clé qui chante »
- Format KDP : 9.222 × 9.222 in (trim 8.972 + bleed 0.125 partout)
- Full-bleed agressif (crop 6% pour éviter cadre crème)
- Safety zone 0.375" pour le texte
"""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

IMG_DIR = Path("/home/claude/lila_tome3")
OUT_PDF = Path("/home/claude/lila_tome3_interieur.pdf")

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
SAFE_BOTTOM = PAGE_PX - BLEED_PX - SAFETY_PX
TRIM_TOP = BLEED_PX
TRIM_BOTTOM = PAGE_PX - BLEED_PX

ZOOM_CROP = 0.06

FONT_BODY = "/usr/share/fonts/truetype/google-fonts/Lora-Variable.ttf"
FONT_BODY_ITALIC = "/usr/share/fonts/truetype/google-fonts/Lora-Italic-Variable.ttf"

INK = (58, 31, 16)
INK_SOFT = (90, 53, 32)
CREAM = (251, 246, 236)

print(f"📐 PDF Tome 3 : {PAGE_IN}\" × {PAGE_IN}\" ({PAGE_PX}×{PAGE_PX} px à {DPI} DPI)")

PAGES_TEXT = {
    1:  "Chez Mamie, Lila explore le vieux grenier.\nUn vieux manteau de laine est resté accroché là.",
    2:  "Dans la poche, une petite clé en cristal.\nElle vibre doucement dans la main de Lila.",
    3:  "Lila approche la clé de son oreille.\nLa clé chante, comme un tout petit oiseau.",
    4:  "Le matin, Lila pose la clé près d'une tasse.\nLa tasse résonne… et un portail de lumière s'ouvre !",
    5:  "Bienvenue dans le Monde du Matin.\nDes tasses géantes, du café en cascade, des couverts musique.",
    6:  "Tout ce qui fait bruit le matin chante ici.\nLila touche une cuillère et le tintement s'envole en couleurs.",
    7:  "Sur une tasse géante, une fillette dessine les sons.\nElle s'appelle Mira et elle entend avec ses yeux.",
    8:  "Mira porte un appareil turquoise derrière l'oreille.\nElle prend la main de Lila pour toucher les sons.",
    9:  "Mira ouvre le Monde des Rires.\nDes bulles dorées flottent partout, pleines de joie.",
    10: "Lila attrape une bulle de rire entre ses mains.\nElle scintille, chaude et douce.",
    11: "Plus loin, le Monde du Silence des Montagnes.\nLe vent dessine des spirales blanches dans l'air.",
    12: "Mira ferme les yeux pour mieux ressentir.\nLila apprend à écouter ce qui ne fait pas de bruit.",
    13: "Lila se souvient d'une berceuse de Mamie.\nElle la fredonne. Une rivière dorée jaillit autour d'elles.",
    14: "Le Monde des Berceuses s'ouvre.\nUn ciel doux, des montagnes ouatées, une rivière de musique.",
    15: "Dans le ciel, le visage de Mamie apparaît.\nLila a les yeux qui brillent. Mira lui prend la main.",
    16: "Soudain la clé vibre étrangement.\nUn son grave, profond, mystérieux. Quelque chose l'appelle.",
    17: "Au bord du Grand Silence, l'océan s'étend.\nC'est immense, c'est calme, c'est un peu effrayant.",
    18: "Sous l'eau, des bulles colorées remontent doucement.\nChaque bulle contient un son oublié.",
    19: "Mira touche une bulle du bout du doigt.\nLa bulle s'ouvre : un petit oiseau de lumière s'envole.",
    20: "Ensemble, elles libèrent des dizaines de sons.\nLe ciel se remplit d'oiseaux et de papillons lumineux.",
    21: "Une bulle vient se poser dans la main de Lila.\nDedans, la voix de Mamie qui chante la berceuse.",
    22: "Lila ouvre les mains. La bulle s'envole vers le ciel.\nLa voix de Mamie devient une étoile.",
    23: "L'océan brille maintenant de mille feux.\nLila et Mira s'embrassent. Le jour se lève.",
    24: "Mira pose son oreille contre la clé.\nElle sourit et fait un signe : « À bientôt, mon amie ».",
    25: "Mira offre à Lila un dessin de sons.\nUn portail de musique s'ouvre derrière elles.",
    26: "Lila revient chez Mamie.\nLe grenier semble plus vivant qu'avant.",
    27: "Lila s'arrête sur les marches et ferme les yeux.\nElle entend la pendule, un oiseau, le vent…",
    28: "Dans la cuisine, Mamie fredonne sa berceuse.\nLila l'écoute pour la première fois vraiment.",
    29: "Le soir, sur la table de nuit :\nle dessin de Mira et la clé en cristal côte à côte.",
    30: "Lila s'endort. Dehors, le ciel scintille.\nUne bulle dorée passe à sa fenêtre, comme un bonsoir.",
}


def crop_fit(src, w, h, pct=ZOOM_CROP):
    sw, sh = src.size
    cx, cy = int(sw * pct), int(sh * pct)
    return src.crop((cx, cy, sw - cx, sh - cy)).resize((w, h), Image.LANCZOS)


def caption_overlay(w, h, y_start, fade=80):
    ov = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    px = ov.load()
    f0 = y_start - fade
    for y in range(h):
        if y < f0:
            a = 0
        elif y < y_start:
            t = (y - f0) / fade
            t = t * t * (3 - 2 * t)
            a = int(t * 250)
        else:
            a = 250
        for x in range(w):
            px[x, y] = (*CREAM, a)
    return ov


def centered(draw, text, font, y_start, fill, ls=1.28):
    lines = text.split("\n")
    b = draw.textbbox((0, 0), "Ag", font=font)
    lh = int((b[3] - b[1]) * ls)
    y = y_start
    cx = (SAFE_LEFT + SAFE_RIGHT) // 2
    for line in lines:
        b = draw.textbbox((0, 0), line, font=font)
        draw.text((cx - (b[2] - b[0]) // 2, y), line, font=font, fill=fill)
        y += lh


def render_story(img_path, text, page_num):
    src = Image.open(img_path).convert("RGB")
    canvas = Image.new("RGB", (PAGE_PX, PAGE_PX), CREAM)
    canvas.paste(crop_fit(src, PAGE_PX, PAGE_PX), (0, 0))
    canvas = canvas.convert("RGBA")

    by = TRIM_TOP + int((TRIM_BOTTOM - TRIM_TOP) * 0.78)
    canvas = Image.alpha_composite(canvas, caption_overlay(PAGE_PX, PAGE_PX, by, 80)).convert("RGB")

    draw = ImageDraw.Draw(canvas)
    f = ImageFont.truetype(FONT_BODY, 56)
    f.set_variation_by_axes([600])
    nl = len(text.split("\n"))
    th = nl * 72
    cy = (by + SAFE_BOTTOM) // 2
    centered(draw, text, f, cy - th // 2, INK, 1.28)

    fp = ImageFont.truetype(FONT_BODY_ITALIC, 28)
    b = draw.textbbox((0, 0), str(page_num), font=fp)
    draw.text((SAFE_RIGHT - (b[2] - b[0]), SAFE_BOTTOM - 35), str(page_num), font=fp, fill=INK_SOFT)
    return canvas


def render_title():
    img = Image.new("RGB", (PAGE_PX, PAGE_PX), CREAM)
    draw = ImageDraw.Draw(img)

    def orn(y):
        cx = PAGE_PX // 2
        lw, gap, t = 80, 30, 4
        for o in [-1, 0, 1]:
            xs = cx + o * (lw + gap) - lw // 2
            draw.rectangle([xs, y - t // 2, xs + lw, y + t // 2], fill=INK_SOFT)

    f_in = ImageFont.truetype(FONT_BODY_ITALIC, 52); f_in.set_variation_by_axes([450])
    centered(draw, "Une histoire à lire le soir,\nquand on a très envie d'écouter", f_in,
             int(PAGE_PX * 0.14), INK_SOFT, 1.3)
    orn(int(PAGE_PX * 0.27))

    f_t = ImageFont.truetype(FONT_BODY, 165); f_t.set_variation_by_axes([600])
    f_ti = ImageFont.truetype(FONT_BODY_ITALIC, 108); f_ti.set_variation_by_axes([500])
    cx = (SAFE_LEFT + SAFE_RIGHT) // 2
    y = int(PAGE_PX * 0.34)
    b = draw.textbbox((0, 0), "Lila", font=f_t)
    draw.text((cx - (b[2] - b[0]) // 2, y), "Lila", font=f_t, fill=INK); y += int(PAGE_PX * 0.085)
    b = draw.textbbox((0, 0), "et la clé", font=f_ti)
    draw.text((cx - (b[2] - b[0]) // 2, y), "et la clé", font=f_ti, fill=INK_SOFT); y += int(PAGE_PX * 0.065)
    b = draw.textbbox((0, 0), "qui chante", font=f_t)
    draw.text((cx - (b[2] - b[0]) // 2, y), "qui chante", font=f_t, fill=INK)
    orn(int(PAGE_PX * 0.79))

    f_a = ImageFont.truetype(FONT_BODY_ITALIC, 52); f_a.set_variation_by_axes([450])
    centered(draw, "Pour les petits explorateurs\nde 6 à 8 ans", f_a,
             int(PAGE_PX * 0.87), INK_SOFT, 1.3)
    return img


def render_end():
    img = Image.new("RGB", (PAGE_PX, PAGE_PX), CREAM)
    draw = ImageDraw.Draw(img)
    f_fin = ImageFont.truetype(FONT_BODY, 280); f_fin.set_variation_by_axes([600])
    b = draw.textbbox((0, 0), "Fin", font=f_fin)
    draw.text(((PAGE_PX - (b[2] - b[0])) // 2, int(PAGE_PX * 0.34) - (b[3] - b[1]) // 2),
              "Fin", font=f_fin, fill=INK)
    f_f = ImageFont.truetype(FONT_BODY_ITALIC, 60); f_f.set_variation_by_axes([450])
    centered(draw, "… mais quelque part, dans une poche oubliée,\nune petite clé en cristal\nchante encore doucement.",
             f_f, int(PAGE_PX * 0.56), INK_SOFT, 1.4)
    return img


def render_copyright():
    img = Image.new("RGB", (PAGE_PX, PAGE_PX), CREAM)
    draw = ImageDraw.Draw(img)
    f_t = ImageFont.truetype(FONT_BODY, 56); f_t.set_variation_by_axes([600])
    f_it = ImageFont.truetype(FONT_BODY_ITALIC, 44); f_it.set_variation_by_axes([400])
    y = int(PAGE_PX * 0.23)
    b = draw.textbbox((0, 0), "Lila et la clé qui chante", font=f_t)
    draw.text(((PAGE_PX - (b[2] - b[0])) // 2, y), "Lila et la clé qui chante", font=f_t, fill=INK); y += 100
    b = draw.textbbox((0, 0), "Apolline Verger", font=f_it)
    draw.text(((PAGE_PX - (b[2] - b[0])) // 2, y), "Apolline Verger", font=f_it, fill=INK_SOFT); y += 180
    f_s = ImageFont.truetype(FONT_BODY, 38); f_s.set_variation_by_axes([400])
    b = draw.textbbox((0, 0), "Collection « Au seuil des merveilles » · Tome 3", font=f_s)
    draw.text(((PAGE_PX - (b[2] - b[0])) // 2, y),
              "Collection « Au seuil des merveilles » · Tome 3", font=f_s, fill=INK_SOFT); y += 220
    for text, font in [
        ("© 2026 Apolline Verger", f_s),
        ("Tous droits réservés.", f_it.font_variant(size=36)),
        ("", None),
        ("Aucune partie de ce livre ne peut être", f_it.font_variant(size=32)),
        ("reproduite sans l'autorisation écrite de l'auteur.", f_it.font_variant(size=32)),
        ("", None),
        ("Première édition", f_s),
        ("", None),
        ("Imprimé via Amazon KDP", f_it.font_variant(size=32)),
    ]:
        if not text: y += 36; continue
        b = draw.textbbox((0, 0), text, font=font)
        draw.text(((PAGE_PX - (b[2] - b[0])) // 2, y), text, font=font, fill=INK_SOFT); y += 56
    return img


pages = [render_title(), render_copyright()]
for p in range(1, 31):
    print(f"  → p{p:02d}")
    pages.append(render_story(IMG_DIR / f"p{p:02d}.png", PAGES_TEXT[p], p))
pages.append(render_end())

print(f"\n💾 Écriture PDF…")
pages[0].save(OUT_PDF, save_all=True, append_images=pages[1:], format="PDF", resolution=DPI)
import os
print(f"✓ {OUT_PDF}")
print(f"  Pages: {len(pages)} · Taille: {os.path.getsize(OUT_PDF) / 1024 / 1024:.1f} MB")
