#!/usr/bin/env python3
# Telechargement des 14 images 4K du livre "Zola et le petit nuage gris"
# A executer dans a-Shell sur iPhone.
import os, urllib.request

DEST = os.path.expanduser("~/Documents/Zola_nuage_gris")
os.makedirs(DEST, exist_ok=True)

IMAGES = {
    "00_couverture.jpeg": "https://d8j0ntlcm91z4.cloudfront.net/user_33ZLmugzCzPZPElXa3iEZVG6Gq0/hf_20260613_075009_936881c0-7627-4969-9206-138006dbaac6.jpeg",
    "01_arrivee.png": "https://d8j0ntlcm91z4.cloudfront.net/user_33ZLmugzCzPZPElXa3iEZVG6Gq0/hf_20260613_075015_e754a227-85ee-422d-ab9b-427095e34cbd.png",
    "02_fresque_excite.png": "https://d8j0ntlcm91z4.cloudfront.net/user_33ZLmugzCzPZPElXa3iEZVG6Gq0/hf_20260613_075021_d9229249-77c4-4f88-b9d4-2ec247df438d.png",
    "03_tous_ensemble.png": "https://d8j0ntlcm91z4.cloudfront.net/user_33ZLmugzCzPZPElXa3iEZVG6Gq0/hf_20260613_075026_2d10bdc0-f724-4dc1-8ed8-bd884a1fb7e1.png",
    "04_tao_oiseau.png": "https://d8j0ntlcm91z4.cloudfront.net/user_33ZLmugzCzPZPElXa3iEZVG6Gq0/hf_20260613_075033_1ebdd233-46dc-4e99-a188-11de7e90e7bf.png",
    "05_nuage_passe.png": "https://d8j0ntlcm91z4.cloudfront.net/user_33ZLmugzCzPZPElXa3iEZVG6Gq0/hf_20260613_075039_ba6812ed-31a9-443a-bfc7-de83554c2163.png",
    "06_bouderie_nuage.png": "https://d8j0ntlcm91z4.cloudfront.net/user_33ZLmugzCzPZPElXa3iEZVG6Gq0/hf_20260613_075045_8c99eb95-1c96-4e84-b9c6-f9bf46f23f92.png",
    "07_chouette.png": "https://d8j0ntlcm91z4.cloudfront.net/user_33ZLmugzCzPZPElXa3iEZVG6Gq0/hf_20260613_075053_b4b40220-0c24-4e25-b746-e1cc641d29e5.png",
    "08_methode_3etapes.png": "https://d8j0ntlcm91z4.cloudfront.net/user_33ZLmugzCzPZPElXa3iEZVG6Gq0/hf_20260613_075100_c92dff18-5777-42c8-9d52-6700e3966b3c.png",
    "09_regarde_allege.png": "https://d8j0ntlcm91z4.cloudfront.net/user_33ZLmugzCzPZPElXa3iEZVG6Gq0/hf_20260613_075105_a2486970-f870-4cde-a477-186a337b8d10.png",
    "10_vers_tao.png": "https://d8j0ntlcm91z4.cloudfront.net/user_33ZLmugzCzPZPElXa3iEZVG6Gq0/hf_20260613_075111_cff0ffe8-31d3-4838-a585-1c81663957d3.png",
    "11_grimpe_soleil.jpeg": "https://d8j0ntlcm91z4.cloudfront.net/user_33ZLmugzCzPZPElXa3iEZVG6Gq0/hf_20260613_075119_ea774ee7-2e7c-417d-9aaf-ba25ed464f20.jpeg",
    "12_soir_papa.png": "https://d8j0ntlcm91z4.cloudfront.net/user_33ZLmugzCzPZPElXa3iEZVG6Gq0/hf_20260613_075125_3015bc4b-8a53-4a4d-b12f-a2f140158e48.png",
    "13_recap.png": "https://d8j0ntlcm91z4.cloudfront.net/user_33ZLmugzCzPZPElXa3iEZVG6Gq0/hf_20260613_075132_38cdc8a2-cedf-4053-a4f5-b23a0ccf014d.png",
}

print("Telechargement de", len(IMAGES), "images vers", DEST)
for name, url in IMAGES.items():
    out = os.path.join(DEST, name)
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=60) as r, open(out, "wb") as f:
            f.write(r.read())
        kb = os.path.getsize(out) // 1024
        print("OK  ", name, f"({kb} Ko)")
    except Exception as e:
        print("ERR ", name, "->", e)

print("Termine. Dossier:", DEST)
