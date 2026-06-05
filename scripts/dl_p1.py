import requests, base64, os

TOKEN = os.environ["GH_TOKEN"]
REPO = "Sacha30650/livres-kdp-sacha"
BASE = "https://d8j0ntlcm91z4.cloudfront.net/user_33ZLmugzCzPZPElXa3iEZVG6Gq0/"

# page -> fichier source CloudFront
images = {
    "illustrations_P1/p06_carons_couple.png":      "hf_20260605_200543_dd93c32d-0576-4e59-9e91-c8a786300b43.png",
    "illustrations_P1/p07_tri_affaires.png":       "hf_20260605_200549_ab2c3518-f235-4a90-a9c1-b77fa940646c.png",
    "illustrations_P1/p08_choix_body.png":         "hf_20260605_200555_744efadd-df32-4cfa-ae15-eb3dc03f21b3.png",
    "illustrations_P1/p09_seconde_main.png":       "hf_20260605_200602_3ee22395-ddab-4e42-98db-2a30b16cad3d.png",
    "illustrations_P1/p10_coin_bebe.png":          "hf_20260605_200607_ed493262-7f63-4eae-b37e-ac2e01365107.png",
    "illustrations_P1/p11_berceau_securise.png":   "hf_20260605_200613_9a7bf6e7-939f-400b-b98f-d6e8772c2695.png",
    "illustrations_P1/p12_trois_sacs.png":         "hf_20260605_200620_41e12d0a-1221-433d-8355-a79ad931da21.png",
    "illustrations_P1/p13_kit_coparent.png":       "hf_20260605_200626_83b415ac-bf12-430f-8779-a15c03becd3b.png",
    "illustrations_P1/p17_papiers_admin.png":      "hf_20260605_200631_5be36b91-98c0-46cb-b2bc-eeccb06b4b56.png",
    "illustrations_P1/p18_pochette_naissance.png": "hf_20260605_200637_3d1279fb-e2f5-4d41-9d45-e423b469519c.png",
    "illustrations_P1/p20_ENTRE_NOUS_terracotta.png":"hf_20260605_200644_073a7102-aee1-4fcb-acff-a486f0a78837.png",
}

h = {"Authorization": f"token {TOKEN}", "Accept": "application/vnd.github+json"}
ok = 0
for path, fname in images.items():
    url = BASE + fname
    img = requests.get(url).content
    print(path, len(img), "bytes")
    b64 = base64.b64encode(img).decode()
    api = f"https://api.github.com/repos/{REPO}/contents/{path}"
    r = requests.get(api, headers=h, params={"ref": "main"})
    payload = {"message": f"add {path}", "content": b64, "branch": "main"}
    if r.status_code == 200:
        payload["sha"] = r.json()["sha"]
    pr = requests.put(api, headers=h, json=payload)
    print("  ->", pr.status_code)
    if pr.status_code in (200, 201): ok += 1
print(f"DONE {ok}/{len(images)}")
