"""
PDF Partie 1 - DA croquis legere type "Guide zero tabou"
Guide parentalite "Notre premiere annee a 3"
- Maquette magazine : texte en colonnes, illustrations detourees, beaucoup de blanc
- Titres manuscrits (Amatic SC), texte Lora, intertitres Poppins
- Format portrait 8.5 x 11 in
"""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

IMG = Path("/home/claude/parent_croquis")
OUT = Path("/home/claude/parentalite_partie1_croquis.pdf")

DPI = 200
PAGE_W = round(8.5 * DPI)    # 1700
PAGE_H = round(11.0 * DPI)   # 2200
MARGIN = round(0.8 * DPI)
CONTENT_W = PAGE_W - 2 * MARGIN
COL_GAP = round(0.35 * DPI)
COL_W = (CONTENT_W - COL_GAP) // 2

# Palette douce
PAPER   = (253, 251, 246)
INK     = (60, 54, 50)
INK_SOFT= (120, 110, 102)
PEACH   = (232, 158, 130)
ROSE    = (210, 150, 145)
SAGE    = (150, 168, 140)
GOLD    = (222, 178, 110)
RETAIN_BG = (250, 240, 224)
PRO_BG    = (231, 237, 227)

AMATIC_B = "/usr/share/fonts/truetype/google-fonts/AmaticSC-Bold.ttf"
# fallback si chemin different
import os
if not os.path.exists(AMATIC_B):
    for c in ["/usr/local/lib/python3.12/dist-packages/font_amatic_sc/files/AmaticSC-Bold.ttf"]:
        if os.path.exists(c):
            AMATIC_B = c
AMATIC_R = AMATIC_B.replace("Bold", "Regular")
LORA     = "/usr/share/fonts/truetype/google-fonts/Lora-Variable.ttf"
LORA_IT  = "/usr/share/fonts/truetype/google-fonts/Lora-Italic-Variable.ttf"
POPPINS_B= "/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf"
POPPINS_M= "/usr/share/fonts/truetype/google-fonts/Poppins-Medium.ttf"

def F(path, size):
    return ImageFont.truetype(path, size)

pages = []

# ---------- helpers ----------

def wrap(text, fnt, max_w, draw):
    out = []
    for para in text.split("\n"):
        words = para.split()
        cur = ""
        for w in words:
            t = (cur + " " + w).strip()
            if draw.textlength(t, font=fnt) <= max_w:
                cur = t
            else:
                if cur:
                    out.append(cur)
                cur = w
        out.append(cur)
    return out

def draw_text_block(draw, text, fnt, x, y, max_w, fill, line_sp=1.5, para_gap=16):
    asc, desc = fnt.getmetrics()
    lh = int((asc + desc) * line_sp)
    for para in text.split("\n\n"):
        for ln in wrap(para.replace("\n", " "), fnt, max_w, draw):
            draw.text((x, y), ln, font=fnt, fill=fill)
            y += lh
        y += para_gap
    return y

def paste_cut(page, img_name, box_w, box_h, x, y):
    """Pose une illustration detouree (RGBA) redimensionnee dans box, centree."""
    im = Image.open(IMG / img_name).convert("RGBA")
    iw, ih = im.size
    scale = min(box_w / iw, box_h / ih)
    nw, nh = int(iw * scale), int(ih * scale)
    im = im.resize((nw, nh), Image.LANCZOS)
    ox = x + (box_w - nw) // 2
    oy = y + (box_h - nh) // 2
    page.paste(im, (ox, oy), im)
    return nh

def new_page():
    return Image.new("RGB", (PAGE_W, PAGE_H), PAPER)

def hero_corner(page, draw, chapter_label):
    """Petit hero detoure en haut a droite, discret."""
    hsize = round(1.05 * DPI)
    paste_cut(page, "hero_bebe_clean_cut.png", hsize, hsize,
              PAGE_W - MARGIN - hsize, MARGIN - round(0.25 * DPI))

def page_num(draw, n):
    f = F(POPPINS_M, 22)
    t = str(n)
    w = draw.textlength(t, font=f)
    draw.text(((PAGE_W - w) // 2, PAGE_H - MARGIN + 28), t, font=f, fill=INK_SOFT)
    # petit trait decoratif
    draw.line((PAGE_W // 2 - 60, PAGE_H - MARGIN + 18,
               PAGE_W // 2 - 30, PAGE_H - MARGIN + 18), fill=GOLD, width=3)
    draw.line((PAGE_W // 2 + 30, PAGE_H - MARGIN + 18,
               PAGE_W // 2 + 60, PAGE_H - MARGIN + 18), fill=GOLD, width=3)

def wavy_underline(draw, x1, x2, y, color, amp=4, step=14, w=4):
    import math
    pts = []
    x = x1
    while x <= x2:
        pts.append((x, y + amp * math.sin((x - x1) / step)))
        x += 4
    for i in range(len(pts) - 1):
        draw.line([pts[i], pts[i + 1]], fill=color, width=w)

def callout(page, draw, x, y, w, kind, head, text):
    """Encadre doux facon note manuscrite."""
    bg = RETAIN_BG if kind == "retain" else PRO_BG
    accent = GOLD if kind == "retain" else SAGE
    f_head = F(POPPINS_B, 24)
    f_body = F(LORA, 28)
    lines = wrap(text, f_body, w - 2 * round(0.3 * DPI), draw)
    asc, desc = f_body.getmetrics()
    lh = int((asc + desc) * 1.4)
    pad = round(0.3 * DPI)
    box_h = pad * 2 + 50 + len(lines) * lh
    draw.rounded_rectangle((x, y, x + w, y + box_h), radius=26, fill=bg)
    # petit rond accent + titre
    draw.ellipse((x + pad, y + pad + 4, x + pad + 22, y + pad + 26), fill=accent)
    draw.text((x + pad + 38, y + pad), head, font=f_head, fill=accent)
    yy = y + pad + 54
    for ln in lines:
        draw.text((x + pad, yy), ln, font=f_body, fill=INK)
        yy += lh
    return box_h


# ================= PAGE 1 — Ouverture de partie =================
p = new_page()
d = ImageDraw.Draw(p)

# grande illustration trio detouree, centree haut
trio_h = paste_cut(p, "p1_trio_cut.png", CONTENT_W, round(5.6 * DPI),
                   MARGIN, round(0.7 * DPI))

# bloc titre
ty = round(0.7 * DPI) + round(5.6 * DPI) + round(0.15 * DPI)
f_part = F(POPPINS_B, 30)
t = "PARTIE 1"
d.text(((PAGE_W - d.textlength(t, font=f_part)) // 2, ty), t, font=f_part, fill=ROSE)
ty += 56

f_title = F(AMATIC_B, 180)
t = "On y est presque"
tw = d.textlength(t, font=f_title)
d.text(((PAGE_W - tw) // 2, ty), t, font=f_title, fill=INK)
ty += 178
wavy_underline(d, (PAGE_W - 360) // 2, (PAGE_W + 360) // 2, ty, GOLD, amp=5, w=5)
ty += 46

f_sub = F(LORA_IT, 34)
t = "Le dernier trimestre, et tout ce qui se prepare en douceur"
d.text(((PAGE_W - d.textlength(t, font=f_sub)) // 2, ty), t, font=f_sub, fill=INK_SOFT)

pages.append(p)


# ================= PAGE 2 — Ouverture narrative =================
p = new_page()
d = ImageDraw.Draw(p)
hero_corner(p, d, "On y est presque")

y = MARGIN + round(0.2 * DPI)
# grande accroche manuscrite
f_hook = F(AMATIC_B, 110)
for ln in ["Vous y etes", "presque."]:
    d.text((MARGIN, y), ln, font=f_hook, fill=INK)
    y += 92
y += 30

intro = ("Plus que quelques semaines, peut-etre quelques jours, et cette petite "
         "personne dont vous parlez depuis des mois sera la, pour de vrai.\n\n"
         "C'est vertigineux. On a hate, on a peur, on se sent pret le matin et "
         "completement depasse le soir. Tout ca en meme temps, c'est normal. "
         "Personne n'arrive « fin pret » a l'arrivee d'un bebe : on arrive en "
         "chemin, et c'est tres bien comme ca.\n\n"
         "Cette premiere partie n'est pas une liste d'obligations. C'est une "
         "boite a outils dans laquelle vous piochez ce qui vous rassure, a "
         "votre rythme. Rien ici n'est un examen.")
f_body = F(LORA, 33)
y = draw_text_block(d, intro, f_body, MARGIN, y, CONTENT_W, INK, line_sp=1.55)

y += 20
f_close = F(AMATIC_B, 68)
t = "On respire, et on y va ensemble."
d.text((MARGIN, y), t, font=f_close, fill=PEACH)

page_num(d, 8)
pages.append(p)


# ================= util chapitre 2 colonnes =================
def chapter_2col(num, title, illo, body_text, callout_kind=None,
                 callout_head="", callout_text="", page_no=0, illo_side="right"):
    p = new_page()
    d = ImageDraw.Draw(p)
    hero_corner(p, d, title if len(title) < 26 else "On y est presque")

    y = MARGIN + round(0.15 * DPI)
    # numero
    f_n = F(POPPINS_B, 26)
    d.text((MARGIN, y), num, font=f_n, fill=ROSE)
    y += 44
    # titre manuscrit
    f_t = F(AMATIC_B, 118)
    for ln in wrap(title, f_t, CONTENT_W - round(1.3 * DPI), d):
        d.text((MARGIN, y), ln, font=f_t, fill=INK)
        y += 96
    y += 26
    wavy_underline(d, MARGIN, MARGIN + 240, y, GOLD, amp=4, w=4)
    y += 44

    top_text = y
    # illustration sur un cote
    illo_box = round(2.7 * DPI)
    if illo_side == "right":
        paste_cut(p, illo, illo_box, illo_box,
                  PAGE_W - MARGIN - illo_box, top_text - 20)
        text_w = CONTENT_W - illo_box - COL_GAP
        text_x = MARGIN
    else:
        paste_cut(p, illo, illo_box, illo_box, MARGIN, top_text - 20)
        text_w = CONTENT_W - illo_box - COL_GAP
        text_x = MARGIN + illo_box + COL_GAP

    f_b = F(LORA, 31)
    # texte qui longe l'illustration puis reprend pleine largeur
    asc, desc = f_b.getmetrics()
    lh = int((asc + desc) * 1.5)
    narrow_lines_max = int((illo_box) / lh) + 1

    all_lines = []
    for para in body_text.split("\n\n"):
        wl = wrap(para.replace("\n", " "), f_b, text_w, d)
        all_lines.append(("para", wl))

    # Phase 1 : a cote de l'illo (largeur reduite)
    yy = top_text
    line_count = 0
    full_lines = []
    narrow_done = False
    for kind, wl in all_lines:
        for ln in wl:
            if not narrow_done and line_count < narrow_lines_max:
                d.text((text_x, yy), ln, font=f_b, fill=INK)
                yy += lh
                line_count += 1
            else:
                narrow_done = True
                full_lines.append(ln)
        if not narrow_done:
            yy += 14
        else:
            full_lines.append("")

    # Phase 2 : pleine largeur sous l'illustration
    yy = max(yy, top_text + illo_box + 10)
    fw_lines_wrapped = []
    for ln in full_lines:
        if ln == "":
            fw_lines_wrapped.append("")
        else:
            # rewrap en pleine largeur
            for w2 in wrap(ln, f_b, CONTENT_W, d):
                fw_lines_wrapped.append(w2)
    for ln in fw_lines_wrapped:
        if ln == "":
            yy += 14
            continue
        d.text((MARGIN, yy), ln, font=f_b, fill=INK)
        yy += lh

    # encadre
    if callout_kind:
        yy += 24
        callout(p, d, MARGIN, yy, CONTENT_W, callout_kind, callout_head, callout_text)

    page_num(d, page_no)
    return p


# ================= PAGE 3 — 1.1 Preparer le nid =================
pages.append(chapter_2col(
    "1.1", "Preparer le nid", "p1_materiel_cut.png",
    "L'industrie de la puericulture est tres douee pour vous faire croire "
    "qu'il vous faut trois cents objets. La verite, plus tranquille, c'est "
    "qu'un nouveau-ne a besoin de tres peu : etre nourri, etre au chaud, "
    "dormir en securite, et etre aime.\n\n"
    "Le reste, c'est du confort. Utile parfois, superflu souvent. Beaucoup de "
    "parents rachetent apres coup ce qu'ils pensaient indispensable, et ne "
    "touchent jamais a la moitie de la liste « ideale ». Vous ajusterez en "
    "rencontrant votre bebe : lui seul vous dira ce dont il a besoin.",
    callout_kind="retain", callout_head="A RETENIR",
    callout_text="Vous n'avez pas a tout avoir. Vous avez juste a avoir de quoi commencer.",
    page_no=9, illo_side="right"))


# ================= PAGE 4 — 1.2 Le coin sommeil =================
pages.append(chapter_2col(
    "1.2", "La chambre et le coin sommeil", "p1_sommeil_cut.png",
    "Que bebe ait sa chambre ou dorme dans la votre les premiers mois, l'idee "
    "est la meme : un endroit calme, a temperature moderee, sans superflu "
    "autour du couchage.\n\n"
    "Un coin sommeil serein, c'est un espace de couchage degage, une ambiance "
    "douce, une lumiere tamisee. Pas besoin d'une chambre de magazine : le "
    "calme compte bien plus que la decoration.",
    callout_kind="pro", callout_head="CE QUI RELEVE DU PROFESSIONNEL",
    callout_text="L'amenagement du couchage et les recommandations de securite du "
    "sommeil evoluent et sont precises. Demandez a votre sage-femme, votre "
    "pediatre ou a la PMI les consignes a jour : ce sont les bonnes sources, "
    "et elles repondront sans vous juger.",
    page_no=10, illo_side="left"))


# ================= PAGE 5 — 1.3 La valise de maternite =================
pages.append(chapter_2col(
    "1.3", "La valise de maternite", "p1_valise_cut.png",
    "Preparee vers la fin du parcours, posee pres de la porte, elle transforme "
    "un depart stressant en simple geste. On la prepare en trois temps : pour "
    "vous, pour bebe, pour le co-parent.\n\n"
    "Pour le parent qui accouche : tenues confortables, affaires de toilette, "
    "de quoi s'occuper pendant les temps d'attente, les documents. Pour bebe : "
    "tenues selon la saison, de quoi le couvrir. Pour le co-parent : de quoi "
    "tenir quelques heures, voire une nuit.",
    callout_kind="retain", callout_head="A RETENIR",
    callout_text="Une valise « presque prete » a l'avance vaut mieux qu'une "
    "valise parfaite faite dans la panique.",
    page_no=11, illo_side="right"))


# ================= PAGE 6 — 1.4 Les demarches =================
pages.append(chapter_2col(
    "1.4", "Les demarches administratives", "p1_demarches_cut.png",
    "Personne n'aime cette partie. La bonne nouvelle : la plupart des "
    "demarches se font apres la naissance, et beaucoup de structures vous "
    "accompagnent.\n\n"
    "Le but ici n'est pas de tout regler maintenant, c'est de savoir ce qui "
    "vous attend pour ne pas etre pris au depourvu. Reperez simplement ou se "
    "trouvent vos documents importants et qui sont vos interlocuteurs. Le "
    "reste se fera, etape par etape.",
    callout_kind="pro", callout_head="CE QUI RELEVE DU PROFESSIONNEL",
    callout_text="Les demarches precises, les delais et les droits dependent de "
    "votre situation et changent regulierement. Votre maternite, votre caisse "
    "d'allocations et votre mairie sont les interlocuteurs fiables. N'hesitez "
    "jamais a leur poser des questions, meme « betes ».",
    page_no=12, illo_side="left"))


# ================= util check-list =================
def checklist_page(num, title, intro, sections, page_no, illo=None):
    p = new_page()
    d = ImageDraw.Draw(p)
    hero_corner(p, d, "On y est presque")

    y = MARGIN + round(0.15 * DPI)
    f_n = F(POPPINS_B, 26)
    d.text((MARGIN, y), num, font=f_n, fill=ROSE)
    y += 44
    f_t = F(AMATIC_B, 118)
    for ln in wrap(title, f_t, CONTENT_W - round(1.3 * DPI), d):
        d.text((MARGIN, y), ln, font=f_t, fill=INK)
        y += 96
    y += 6
    wavy_underline(d, MARGIN, MARGIN + 240, y, GOLD, amp=4, w=4)
    y += 36

    f_intro = F(LORA_IT, 29)
    y = draw_text_block(d, intro, f_intro, MARGIN, y, CONTENT_W, INK_SOFT, line_sp=1.4)
    y += 14

    # illustration optionnelle en haut a droite
    if illo:
        paste_cut(p, illo, round(1.9 * DPI), round(1.9 * DPI),
                  PAGE_W - MARGIN - round(1.9 * DPI), MARGIN + round(0.1 * DPI))

    f_sec = F(POPPINS_B, 26)
    f_item = F(LORA, 30)
    box = 34
    for sec_title, items in sections:
        d.text((MARGIN, y), sec_title.upper(), font=f_sec, fill=PEACH)
        y += 50
        for it in items:
            d.rounded_rectangle((MARGIN, y, MARGIN + box, y + box),
                                radius=9, outline=ROSE, width=3)
            il = wrap(it, f_item, CONTENT_W - box - 30, d)
            asc, desc = f_item.getmetrics()
            ilh = int((asc + desc) * 1.32)
            ty = y + (box - (asc + desc)) // 2 - 2
            for k, ln in enumerate(il):
                d.text((MARGIN + box + 26, ty + k * ilh), ln, font=f_item, fill=INK)
            y += max(box, len(il) * ilh) + 20
        y += 20

    page_num(d, page_no)
    return p


# ================= PAGE 7 — 1.5 Check-list de preparation =================
pages.append(checklist_page(
    "1.5", "Check-list de preparation",
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
    page_no=13))


# ================= PAGE 8 — 1.6 Check-list du co-parent =================
p = new_page()
d = ImageDraw.Draw(p)
hero_corner(p, d, "On y est presque")

y = MARGIN + round(0.15 * DPI)
d.text((MARGIN, y), "1.6", font=F(POPPINS_B, 26), fill=ROSE)
y += 44
f_t = F(AMATIC_B, 118)
d.text((MARGIN, y), "Check-list du co-parent", font=f_t, fill=INK)
y += 96
wavy_underline(d, MARGIN, MARGIN + 240, y + 26, GOLD, amp=4, w=4)
y += 66

# illustration co-parent a droite + intro a gauche
co_box = round(2.5 * DPI)
paste_cut(p, "p1_coparent_cut.png", co_box, co_box,
          PAGE_W - MARGIN - co_box, y - 20)

intro_co = ("Pendant des mois, l'attention se porte, legitimement, sur la "
            "personne qui porte l'enfant. Mais le co-parent n'est pas un "
            "spectateur : il a un role reel, precieux, et souvent mal "
            "explique. Cette page est la sienne.")
f_intro = F(LORA_IT, 29)
y2 = draw_text_block(d, intro_co, f_intro, MARGIN, y,
                     CONTENT_W - co_box - COL_GAP, INK_SOFT, line_sp=1.45)
y = max(y2, y + co_box - 20) + 24

f_sec = F(POPPINS_B, 26)
f_item = F(LORA, 30)
box = 34
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
    d.text((MARGIN, y), sec_title.upper(), font=f_sec, fill=PEACH)
    y += 50
    for it in items:
        d.rounded_rectangle((MARGIN, y, MARGIN + box, y + box),
                            radius=9, outline=ROSE, width=3)
        il = wrap(it, f_item, CONTENT_W - box - 30, d)
        asc, desc = f_item.getmetrics()
        ilh = int((asc + desc) * 1.32)
        ty = y + (box - (asc + desc)) // 2 - 2
        for k, ln in enumerate(il):
            d.text((MARGIN + box + 26, ty + k * ilh), ln, font=f_item, fill=INK)
        y += max(box, len(il) * ilh) + 18
    y += 16

y += 8
callout(p, d, MARGIN, y, CONTENT_W, "retain", "A RETENIR",
        "Le plus beau cadeau du co-parent dans les premiers jours, ce n'est pas "
        "un geste heroique. C'est mille petits gestes ordinaires qui permettent "
        "a l'autre de souffler.")

page_num(d, 14)
pages.append(p)


# ================= EXPORT =================
print(f"Pages : {len(pages)}")
pages[0].save(OUT, save_all=True, append_images=pages[1:], format="PDF", resolution=DPI)
print(f"OK -> {OUT}  ({os.path.getsize(OUT)/1024/1024:.1f} MB)")
