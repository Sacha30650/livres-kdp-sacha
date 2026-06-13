#!/usr/bin/env python3
# a-Shell : telecharge les 21 images 4K depuis CloudFront et les POUSSE sur GitHub.
# Raison : le sandbox Claude ne peut pas lire CloudFront (403) mais lit GitHub.
# Apres execution, Claude recupere les images directement depuis le repo.
import os, base64, json, urllib.request, urllib.error

TOKEN = os.environ.get("GH_TOKEN", "")
REPO  = "Sacha30650/livres-kdp-sacha"
GHDIR = "zola/images"
if not TOKEN:
    raise SystemExit("ERREUR : exporte ton token avant -> export GH_TOKEN=ghp_xxx puis relance.")

BASE  = "https://d8j0ntlcm91z4.cloudfront.net/user_33ZLmugzCzPZPElXa3iEZVG6Gq0/"

IMAGES = {
    "P01_fauxtitre.jpeg":        BASE+"hf_20260613_075009_936881c0-7627-4969-9206-138006dbaac6.jpeg",
    "P05_grimpe_matin.png":      BASE+"hf_20260613_080414_c92c0d57-e6bb-488e-8648-a0bb364c5c74.png",
    "P06_arrivee.png":           BASE+"hf_20260613_075015_e754a227-85ee-422d-ab9b-427095e34cbd.png",
    "P07_fresque_excite.png":    BASE+"hf_20260613_075021_d9229249-77c4-4f88-b9d4-2ec247df438d.png",
    "P08_tous_ensemble.png":     BASE+"hf_20260613_075026_2d10bdc0-f724-4dc1-8ed8-bd884a1fb7e1.png",
    "P09_gros_plan_complice.png":BASE+"hf_20260613_080420_f34c7d7c-0ab0-4345-bc17-0272a00044a5.png",
    "P10_tao_oiseau.png":        BASE+"hf_20260613_075033_1ebdd233-46dc-4e99-a188-11de7e90e7bf.png",
    "P11_amis_admirent.png":     BASE+"hf_20260613_080426_6abe312e-5956-45be-9c38-30ce0f280279.png",
    "P12_nuage_passe.png":       BASE+"hf_20260613_075039_ba6812ed-31a9-443a-bfc7-de83554c2163.png",
    "P13_bouderie_nuage.png":    BASE+"hf_20260613_075045_8c99eb95-1c96-4e84-b9c6-f9bf46f23f92.png",
    "P14_creux_nuage_sombre.png":BASE+"hf_20260613_080433_f2456c84-5bf3-42d6-964c-46fdcef9a90c.png",
    "P15_chouette_assoit.png":   BASE+"hf_20260613_075053_b4b40220-0c24-4e25-b746-e1cc641d29e5.png",
    "P16_chouette_souffle.png":  BASE+"hf_20260613_080440_dcac25b2-d690-4303-aa2a-51f33f602d40.png",
    "P17_methode_3etapes.png":   BASE+"hf_20260613_075100_c92dff18-5777-42c8-9d52-6700e3966b3c.png",
    "P18_regarde_allege.png":    BASE+"hf_20260613_075105_a2486970-f870-4cde-a477-186a337b8d10.png",
    "P19_souffle_retrecit.jpeg": BASE+"hf_20260613_080446_f18144f1-320e-45df-a65b-aeba38f99b88.jpeg",
    "P20_vers_tao.png":          BASE+"hf_20260613_075111_cff0ffe8-31d3-4838-a585-1c81663957d3.png",
    "P21_grimpe_soleil.jpeg":    BASE+"hf_20260613_075119_ea774ee7-2e7c-417d-9aaf-ba25ed464f20.jpeg",
    "P22_fresque_finie.png":     BASE+"hf_20260613_080452_0e78f660-429f-4cdc-a5d9-05e535abd456.png",
    "P23_soir_papa.png":         BASE+"hf_20260613_075125_3015bc4b-8a53-4a4d-b12f-a2f140158e48.png",
    "P24_recap.png":             BASE+"hf_20260613_075132_38cdc8a2-cedf-4053-a4f5-b23a0ccf014d.png",
}

def gh_sha(path):
    url=f"https://api.github.com/repos/{REPO}/contents/{path}"
    req=urllib.request.Request(url,headers={"Authorization":f"token {TOKEN}","Accept":"application/vnd.github+json"})
    try:
        with urllib.request.urlopen(req) as r: return json.load(r).get("sha")
    except Exception: return None

def gh_put(path, raw, msg):
    url=f"https://api.github.com/repos/{REPO}/contents/{path}"
    data={"message":msg,"content":base64.b64encode(raw).decode()}
    sha=gh_sha(path)
    if sha: data["sha"]=sha
    req=urllib.request.Request(url,data=json.dumps(data).encode(),method="PUT",
        headers={"Authorization":f"token {TOKEN}","Accept":"application/vnd.github+json"})
    with urllib.request.urlopen(req) as r: return json.load(r)

print("Transfert CloudFront -> GitHub :", len(IMAGES), "images\n")
ok=0
for name,url in IMAGES.items():
    try:
        req=urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0"})
        with urllib.request.urlopen(req,timeout=120) as r: img=r.read()
        gh_put(f"{GHDIR}/{name}", img, f"Add image {name}")
        print("OK  ",name,f"({len(img)//1024} Ko)"); ok+=1
    except urllib.error.HTTPError as e:
        print("ERR ",name,"HTTP",e.code,e.read().decode()[:120])
    except Exception as e:
        print("ERR ",name,"->",e)

print(f"\nTermine : {ok}/{len(IMAGES)} images poussees dans {GHDIR}/ sur {REPO}")
