import requests, base64, os

TOKEN = os.environ["GH_TOKEN"]
REPO = "Sacha30650/livres-kdp-sacha"

images = {
    "couverture_v4/face_avant.png": "https://d8j0ntlcm91z4.cloudfront.net/user_33ZLmugzCzPZPElXa3iEZVG6Gq0/hf_20260605_185648_ef8fc113-8ce3-40b5-a7a3-22a75b7c4d64.png",
    "couverture_v4/quatrieme.png":  "https://d8j0ntlcm91z4.cloudfront.net/user_33ZLmugzCzPZPElXa3iEZVG6Gq0/hf_20260605_185830_0677155a-1369-40ff-994f-fd4834f50a96.png",
    "couverture_v4/dos.png":        "https://d8j0ntlcm91z4.cloudfront.net/user_33ZLmugzCzPZPElXa3iEZVG6Gq0/hf_20260605_190126_fad0cde3-6240-4245-91de-8a723e771a90.png",
}

h = {"Authorization": f"token {TOKEN}", "Accept": "application/vnd.github+json"}
for path, url in images.items():
    img = requests.get(url).content
    print(path, len(img), "bytes")
    b64 = base64.b64encode(img).decode()
    api = f"https://api.github.com/repos/{REPO}/contents/{path}"
    r = requests.get(api, headers=h, params={"ref": "main"})
    payload = {"message": f"add {path}", "content": b64, "branch": "main"}
    if r.status_code == 200:
        payload["sha"] = r.json()["sha"]
    pr = requests.put(api, headers=h, json=payload)
    print("  ", path, "->", pr.status_code)
print("DONE")
