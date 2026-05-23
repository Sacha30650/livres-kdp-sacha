"""
PDF — Partie 1 « On y est presque »
Guide parentalité « Notre première année à 3 »
Format KDP couleur, 8.5 x 8.5 in (livre carré pratique), Standard Color.
Pipeline : composition PIL page par page -> PDF.
"""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import textwrap

IMG = Path("/home/claude/parent_p1")
OUT = Path("/home/claude/parentalite_partie1.pdf")

# --- Format page : portrait 8.5 x 11 in (guide pratique KDP standard) ---
DPI = 200
PAGE_W_IN = 8.5
PAGE_H_IN = 11.0
PAGE_W = round(PAGE_W_IN * DPI)        # 1700 px
PAGE_H = round(PAGE_H_IN * DPI)        # 2200 px
MARGIN = round(0.85 * DPI)
CONTENT_W = PAGE_W - 2 * MARGIN

# --- Palette ---
CREAM      = (252, 248, 240)
PEACH      = (245, 209, 184)
PEACH_SOFT = (250, 232, 222)
ROSE       = (216, 158, 152)
ROSE_SOFT  = (242, 222, 219)
SAGE       = (158, 178, 150)
SAGE_SOFT  = (255, 255, 255)
SAGE_BG    = (228, 235, 222)
INK        = (74, 55, 46)
INK_SOFT   = (120, 100, 88)
GOLD       = (214, 170, 110)

# --- Polices ---
F = "/usr/share/fonts/truetype/google-fonts/"
def font(name, size):
    return ImageFont.truetype(F + name, size)

POPPINS_B   = "Poppins-Bold.ttf"
POPPINS_SB  = "Poppins-Medium.ttf"
POPPINS_R   = "Poppins-Regular.ttf"
POPPINS_L   = "Poppins-Light.ttf"
LORA        = "Lora-Variable.ttf"
LORA_IT     = "Lora-Italic-Variable.ttf"

pages = []


# ============ helpers ============

def new_page(bg=CREAM):
    return Image.new("RGB", (PAGE_W, PAGE_H), bg)

def rounded(draw, box, radius, fill=None, outline=None, width=1):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)

def wrap_text(text, fnt, max_w, draw):
    """Renvoie une liste de lignes qui tiennent dans max_w."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        test = (cur + " " + w).strip()
        if draw.textlength(test, font=fnt) <= max_w:
            cur = test
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def draw_paragraph(draw, text, fnt, x, y, max_w, fill=INK, line_sp=1.45, para_sp=14):
    """Dessine un paragraphe (gère les \n\n). Renvoie le y final."""
    asc, desc = fnt.getmetrics()
    lh = int((asc + desc) * line_sp)
    for para in text.split("\n\n"):
        para = para.replace("\n", " ").strip()
        if not para:
            y += para_sp
            continue
        for line in wrap_text(para, fnt, max_w, draw):
            draw.text((x, y), line, font=fnt, fill=fill)
            y += lh
        y += para_sp
    return y

def hero_band(page, draw, label):
    """Bandeau hero en haut de page : petit bébé + libellé de chapitre."""
    band_h = round(1.0 * DPI)
    # fond bandeau
    rounded(draw, (MARGIN, MARGIN, PAGE_W - MARGIN, MARGIN + band_h),
            radius=28, fill=PEACH_SOFT)
    # hero image
    hero = Image.open(IMG / "hero_bebe.jpeg").convert("RGB")
    hs = band_h - 28
    hero = hero.resize((hs, hs), Image.LANCZOS)
    # masque rond
    mask = Image.new("L", (hs, hs), 0)
    md = ImageDraw.Draw(mask)
    md.ellipse((0, 0, hs, hs), fill=255)
    page.paste(hero, (MARGIN + 16, MARGIN + 14), mask)
    # libellé
    f_lbl = font(POPPINS_SB, 30)
    f_sub = font(LORA_IT, 26)
    tx = MARGIN + 16 + hs + 28
    draw.text((tx, MARGIN + 30), "PARTIE 1", font=font(POPPINS_B, 26), fill=ROSE)
    draw.text((tx, MARGIN + 62), label, font=f_lbl, fill=INK)
    return MARGIN + band_h + 40

def page_number(draw, n):
    f = font(POPPINS_R, 24)
    t = str(n)
    w = draw.textlength(t, font=f)
    draw.text(((PAGE_W - w) / 2, PAGE_H - MARGIN + 25), t, font=f, fill=INK_SOFT)

def full_bleed_image(page, img_name, crop=0.04):
    """Image plein cadre avec léger crop pour retirer la bordure crème."""
    im = Image.open(IMG / img_name).convert("RGB")
    w, h = im.size
    cx, cy = int(w * crop), int(h * crop)
    im = im.crop((cx, cy, w - cx, h - cy))
    # cover fit
    target = PAGE_W
    scale = max(target / im.width, target / im.height)
    nw, nh = int(im.width * scale), int(im.height * scale)
    im = im.resize((nw, nh), Image.LANCZOS)
    left = (nw - target) // 2
    top = (nh - target) // 2
    im = im.crop((left, top, left + target, top + target))
    page.paste(im, (0, 0))


# ============ PAGE_W 1 — Ouverture de partie (illustration trio plein cadre) ============

p = new_page(CREAM)
d = ImageDraw.Draw(p)

# illustration trio en grand, centree verticalement
trio = Image.open(IMG / "p1_trio.png").convert("RGB")
tw, th = trio.size
disp_w = PAGE_W - 2 * MARGIN
disp_h = int(disp_w * th / tw)
max_h = round(6.5 * DPI)
if disp_h > max_h:
    disp_h = max_h
    disp_w = int(disp_h * tw / th)
trio_r = trio.resize((disp_w, disp_h), Image.LANCZOS)
# coins arrondis
mask = Image.new("L", (disp_w, disp_h), 0)
ImageDraw.Draw(mask).rounded_rectangle((0, 0, disp_w, disp_h), radius=36, fill=255)
px = (PAGE_W - disp_w) // 2
top_img = round(1.0 * DPI)
p.paste(trio_r, (px, top_img), mask)

# bloc titre de partie
ty = top_img + disp_h + 70
d.text((PAGE_W // 2, ty), "PARTIE 1", font=font(POPPINS_B, 42), fill=ROSE, anchor="mm")
ty += 68
f_title = font(POPPINS_B, 84)
d.text((PAGE_W // 2, ty), "On y est presque", font=f_title, fill=INK, anchor="mm")
ty += 76
# filet décoratif
d.line((PAGE_W // 2 - 100, ty, PAGE_W // 2 + 100, ty), fill=GOLD, width=5)
ty += 42
f_sub = font(LORA_IT, 36)
sub = "Le dernier trimestre, et tout ce qui se prepare en douceur"
d.text((PAGE_W // 2, ty), sub, font=f_sub, fill=INK_SOFT, anchor="mm")

pages.append(p)


# ============ PAGE_W 2 — Ouverture narrative (texte) ============

p = new_page(CREAM)
d = ImageDraw.Draw(p)
y = hero_band(p, d, "On y est presque")

# Grande citation d'ouverture dans un cadre doux
intro = ("Vous y etes presque. Plus que quelques semaines, peut-etre quelques "
         "jours, et cette petite personne dont vous parlez depuis des mois "
         "sera la, pour de vrai.")
box_top = y
f_intro = font(LORA_IT, 38)
lines = wrap_text(intro, f_intro, CONTENT_W - 80, d)
asc, desc = f_intro.getmetrics()
lh = int((asc + desc) * 1.4)
box_h = len(lines) * lh + 70
rounded(d, (MARGIN, box_top, PAGE_W - MARGIN, box_top + box_h), 28, fill=ROSE_SOFT)
yy = box_top + 35
for ln in lines:
    d.text((PAGE_W // 2, yy), ln, font=f_intro, fill=INK, anchor="ma")
    yy += lh
y = box_top + box_h + 45

# Suite du texte
body = ("C'est vertigineux. On a hate, on a peur, on se sent pret le matin et "
        "completement depasse le soir. Tout ca en meme temps, c'est normal. "
        "Personne n'arrive « fin pret » a l'arrivee d'un bebe : on arrive en "
        "chemin, et c'est tres bien comme ca.\n\n"
        "Cette premiere partie n'est pas une liste d'obligations. C'est une "
        "boite a outils dans laquelle vous piochez ce qui vous rassure, a "
        "votre rythme. Rien ici n'est un examen. On respire, et on y va "
        "ensemble.")
f_body = font(LORA, 33)
y = draw_paragraph(d, body, f_body, MARGIN, y, CONTENT_W, fill=INK, line_sp=1.5)

page_number(d, 8)
pages.append(p)


# ============ util : page de chapitre avec illustration + texte + encadre ============

def chapter_page(num_label, title, img_name, body_text,
                  callout=None, callout_type="retain", page_no=None,
                  img_crop=0.04):
    """callout_type : 'retain' (jaune/or) ou 'pro' (sauge)."""
    p = new_page(CREAM)
    d = ImageDraw.Draw(p)
    y = hero_band(p, d, title)

    # numero + titre de section
    d.text((MARGIN, y), num_label, font=font(POPPINS_B, 26), fill=ROSE)
    y += 38
    f_h = font(POPPINS_SB, 42)
    for ln in wrap_text(title, f_h, CONTENT_W, d):
        d.text((MARGIN, y), ln, font=f_h, fill=INK)
        asc, desc = f_h.getmetrics()
        y += int((asc + desc) * 1.12)
    y += 14

    # illustration centree (reduite)
    im = Image.open(IMG / img_name).convert("RGB")
    iw, ih = im.size
    cx, cy = int(iw * img_crop), int(ih * img_crop)
    im = im.crop((cx, cy, iw - cx, ih - cy))
    disp = round(2.15 * DPI)
    im_r = im.resize((disp, disp), Image.LANCZOS)
    mask = Image.new("L", (disp, disp), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, disp, disp), radius=26, fill=255)
    p.paste(im_r, ((PAGE_W - disp) // 2, y), mask)
    y += disp + 28

    # texte
    f_body = font(LORA, 30)
    y = draw_paragraph(d, body_text, f_body, MARGIN, y, CONTENT_W, fill=INK,
                       line_sp=1.42, para_sp=12)

    # encadre
    if callout:
        y += 8
        if callout_type == "retain":
            bg, accent, head = (251, 240, 218), GOLD, "A RETENIR"
        else:
            bg, accent, head = SAGE_BG, SAGE, "CE QUI RELEVE DU PROFESSIONNEL"
        f_ch = font(POPPINS_B, 22)
        f_ct = font(LORA, 27)
        ct_lines = wrap_text(callout, f_ct, CONTENT_W - 90, d)
        asc, desc = f_ct.getmetrics()
        clh = int((asc + desc) * 1.36)
        box_h = 62 + len(ct_lines) * clh
        rounded(d, (MARGIN, y, PAGE_W - MARGIN, y + box_h), 22, fill=bg)
        rounded(d, (MARGIN, y, MARGIN + 13, y + box_h), 22, fill=accent)
        d.text((MARGIN + 40, y + 22), head, font=f_ch, fill=accent)
        yy = y + 56
        for ln in ct_lines:
            d.text((MARGIN + 40, yy), ln, font=f_ct, fill=INK)
            yy += clh
        y += box_h

    if page_no:
        page_number(d, page_no)
    return p


# ============ PAGE_W 3 — 1.1 Preparer le nid ============

body_11 = ("L'industrie de la puericulture est tres douee pour vous faire croire "
           "qu'il vous faut trois cents objets. La verite, plus tranquille, c'est "
           "qu'un nouveau-ne a besoin de tres peu : etre nourri, etre au chaud, "
           "dormir en securite, et etre aime. Le reste, c'est du confort, utile "
           "parfois, superflu souvent.\n\n"
           "Un repere qui detend : beaucoup de parents rachetent apres coup ce "
           "qu'ils pensaient indispensable, et ne touchent jamais a la moitie de "
           "la liste « ideale ». Vous ajusterez en rencontrant votre bebe.")
pages.append(chapter_page(
    "1.1", "Preparer le nid", "p1_ouverture.png", body_11,
    callout="Vous n'avez pas a tout avoir. Vous avez juste a avoir de quoi commencer.",
    callout_type="retain", page_no=9))


# ============ PAGE_W 4 — 1.2 La chambre et le coin sommeil ============

body_12 = ("Que bebe ait sa chambre ou dorme dans la votre les premiers mois, "
           "l'idee est la meme : un endroit calme, a temperature moderee, sans "
           "superflu autour du couchage.\n\n"
           "Un coin sommeil serein, c'est un espace de couchage degage, une "
           "ambiance douce, une lumiere tamisee. Pas besoin d'une chambre de "
           "magazine : le calme compte plus que la decoration.")
pages.append(chapter_page(
    "1.2", "La chambre et le coin sommeil", "p1_materiel.png", body_12,
    callout=("L'amenagement du couchage et les recommandations de securite du "
             "sommeil evoluent et sont precises. Demandez a votre sage-femme, "
             "votre pediatre ou a la PMI les consignes a jour : ce sont les "
             "bonnes sources, et elles repondront sans vous juger."),
    callout_type="pro", page_no=10))


# ============ PAGE_W 5 — 1.3 La valise de maternite ============

body_13 = ("Preparee vers la fin du parcours, posee pres de la porte, elle "
           "transforme un depart stressant en simple geste. On la prepare en "
           "trois temps : pour vous, pour bebe, pour le co-parent.\n\n"
           "Pour le parent qui accouche : tenues confortables, affaires de "
           "toilette, de quoi s'occuper pendant les temps d'attente, les "
           "documents administratifs et medicaux.\n\n"
           "Pour bebe : tenues selon la saison, de quoi le couvrir, ce qu'il "
           "portera pour le retour. Pour le co-parent : de quoi tenir quelques "
           "heures, voire une nuit.")
pages.append(chapter_page(
    "1.3", "La valise de maternite", "p1_sommeil.png", body_13,
    callout=("Une valise « presque prete » a l'avance vaut mieux qu'une valise "
             "parfaite faite dans la panique."),
    callout_type="retain", page_no=11))


# ============ PAGE_W 6 — 1.4 Les demarches administratives ============

body_14 = ("Personne n'aime cette partie. La bonne nouvelle : la plupart des "
           "demarches se font apres la naissance, et beaucoup de structures "
           "vous accompagnent. Le but ici n'est pas de tout regler maintenant, "
           "c'est de savoir ce qui vous attend pour ne pas etre pris au "
           "depourvu.\n\n"
           "Reperez simplement, des maintenant, ou se trouvent vos documents "
           "importants et qui sont vos interlocuteurs. Le reste se fera, etape "
           "par etape.")
pages.append(chapter_page(
    "1.4", "Les demarches administratives", "p1_valise.png", body_14,
    callout=("Les demarches precises, les delais et les droits dependent de "
             "votre situation et changent regulierement. Votre maternite, votre "
             "caisse d'allocations et votre mairie sont les interlocuteurs "
             "fiables. N'hesitez jamais a leur poser des questions, meme "
             "« betes » : c'est leur metier d'y repondre."),
    callout_type="pro", page_no=12))


# ============ util : page check-list ============

def checklist_page(num_label, title, intro, sections, page_no, hero_label):
    p = new_page(CREAM)
    d = ImageDraw.Draw(p)
    y = hero_band(p, d, hero_label)

    d.text((MARGIN, y), num_label, font=font(POPPINS_B, 28), fill=ROSE)
    y += 42
    f_h = font(POPPINS_SB, 44)
    for ln in wrap_text(title, f_h, CONTENT_W, d):
        d.text((MARGIN, y), ln, font=f_h, fill=INK)
        asc, desc = f_h.getmetrics()
        y += int((asc + desc) * 1.15)
    y += 14

    # intro en italique
    f_intro = font(LORA_IT, 28)
    y = draw_paragraph(d, intro, f_intro, MARGIN, y, CONTENT_W, fill=INK_SOFT, line_sp=1.4)
    y += 12

    f_sec = font(POPPINS_B, 27)
    f_item = font(LORA, 30)
    box_size = 30
    for sec_title, items in sections:
        # titre de section
        d.text((MARGIN, y), sec_title.upper(), font=f_sec, fill=ROSE)
        y += 48
        for it in items:
            # case a cocher
            d.rounded_rectangle((MARGIN, y, MARGIN + box_size, y + box_size),
                                radius=7, outline=ROSE, width=3)
            # texte item
            it_lines = wrap_text(it, f_item, CONTENT_W - box_size - 28, d)
            asc, desc = f_item.getmetrics()
            ilh = int((asc + desc) * 1.32)
            ty = y + (box_size - (asc + desc)) // 2 - 2
            for k, ln in enumerate(it_lines):
                d.text((MARGIN + box_size + 24, ty + k * ilh), ln, font=f_item, fill=INK)
            y += max(box_size, len(it_lines) * ilh) + 18
        y += 18

    page_number(d, page_no)
    return p


# ============ PAGE_W 7 — 1.5 Check-list de preparation ============

pages.append(checklist_page(
    "1.5", "La check-list de preparation",
    "Vous pouvez cocher a votre rythme. Rien n'est a faire en un jour, et si "
    "tout n'est pas coche le jour J, ce n'est pas grave : bebe ne regarde pas "
    "la liste.",
    [
        ("Le coin sommeil", [
            "Un espace de couchage pret et degage",
            "Une ambiance calme, une lumiere douce",
        ]),
        ("L'essentiel materiel", [
            "De quoi nourrir bebe",
            "De quoi le changer",
            "Quelques tenues adaptees a la saison",
            "De quoi le transporter en securite",
        ]),
        ("La valise et les contacts", [
            "Valise de maternite presque prete pres de la porte",
            "Numeros utiles notes quelque part d'accessible",
            "Trajet vers la maternite repere, avec un plan B",
        ]),
        ("Les premieres demarches", [
            "Documents importants reperes et rassembles",
            "Interlocuteurs identifies (maternite, mairie, caisse)",
        ]),
    ],
    page_no=13, hero_label="La check-list de preparation"))


# ============ PAGE_W 8 — 1.6 Check-list du co-parent ============

p = new_page(CREAM)
d = ImageDraw.Draw(p)
y = hero_band(p, d, "La check-list du co-parent")

d.text((MARGIN, y), "1.6", font=font(POPPINS_B, 28), fill=ROSE)
y += 42
f_h = font(POPPINS_SB, 44)
d.text((MARGIN, y), "La check-list du co-parent", font=f_h, fill=INK)
asc, desc = f_h.getmetrics()
y += int((asc + desc) * 1.15) + 10

# petite illustration co-parent a droite + texte intro a gauche
co = Image.open(IMG / "p1_demarches.png").convert("RGB")
cw, ch = co.size
cc = int(cw * 0.04)
co = co.crop((cc, cc, cw - cc, ch - cc))
co_size = round(2.0 * DPI)
co_r = co.resize((co_size, co_size), Image.LANCZOS)
cmask = Image.new("L", (co_size, co_size), 0)
ImageDraw.Draw(cmask).rounded_rectangle((0, 0, co_size, co_size), radius=26, fill=255)
p.paste(co_r, (PAGE_W - MARGIN - co_size, y), cmask)

intro_co = ("Pendant des mois, l'attention se porte, legitimement, sur la "
            "personne qui porte l'enfant. Mais le co-parent n'est pas un "
            "spectateur : il a un role reel, precieux, et souvent mal "
            "explique. Cette page est la sienne.")
f_intro = font(LORA_IT, 29)
draw_paragraph(d, intro_co, f_intro, MARGIN, y, CONTENT_W - co_size - 40,
               fill=INK_SOFT, line_sp=1.45)
y += co_size + 35

# sections checklist
f_sec = font(POPPINS_B, 27)
f_item = font(LORA, 30)
box_size = 30
co_sections = [
    ("Pendant les dernieres semaines", [
        "Connaitre le contenu et l'emplacement de la valise",
        "Savoir aller a la maternite, avec un plan B",
        "Reperer les documents importants et les numeros utiles",
    ]),
    ("Le jour J", [
        "Rester une presence calme et rassurante",
        "Gerer l'intendance : sacs, trajets, prevenir les proches",
    ]),
    ("Le retour a la maison", [
        "Prendre en charge repas, menage, visites a filtrer",
        "Offrir des temps de repos sans que l'autre ait a les demander",
    ]),
]
for sec_title, items in co_sections:
    d.text((MARGIN, y), sec_title.upper(), font=f_sec, fill=ROSE)
    y += 46
    for it in items:
        d.rounded_rectangle((MARGIN, y, MARGIN + box_size, y + box_size),
                            radius=7, outline=ROSE, width=3)
        it_lines = wrap_text(it, f_item, CONTENT_W - box_size - 28, d)
        asc, desc = f_item.getmetrics()
        ilh = int((asc + desc) * 1.32)
        ty = y + (box_size - (asc + desc)) // 2 - 2
        for k, ln in enumerate(it_lines):
            d.text((MARGIN + box_size + 24, ty + k * ilh), ln, font=f_item, fill=INK)
        y += max(box_size, len(it_lines) * ilh) + 16
    y += 14

# encadre final A retenir
callout = ("Le plus beau cadeau du co-parent dans les premiers jours, ce n'est "
           "pas un geste heroique. C'est mille petits gestes ordinaires qui "
           "permettent a l'autre de souffler.")
f_ch = font(POPPINS_B, 24)
f_ct = font(LORA, 29)
ct_lines = wrap_text(callout, f_ct, CONTENT_W - 100, d)
asc, desc = f_ct.getmetrics()
clh = int((asc + desc) * 1.4)
box_h = 70 + len(ct_lines) * clh
rounded(d, (MARGIN, y, PAGE_W - MARGIN, y + box_h), 24, fill=(251, 240, 218))
rounded(d, (MARGIN, y, MARGIN + 14, y + box_h), 24, fill=GOLD)
d.text((MARGIN + 44, y + 24), "A RETENIR", font=f_ch, fill=GOLD)
yy = y + 64
for ln in ct_lines:
    d.text((MARGIN + 44, yy), ln, font=f_ct, fill=INK)
    yy += clh

page_number(d, 14)
pages.append(p)


# ============ EXPORT PDF ============

print(f"Pages composees : {len(pages)}")
pages[0].save(OUT, save_all=True, append_images=pages[1:], format="PDF",
              resolution=DPI)
import os
print(f"OK -> {OUT}  ({os.path.getsize(OUT)/1024/1024:.1f} MB)")
