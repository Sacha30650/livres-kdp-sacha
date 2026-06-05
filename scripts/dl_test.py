import requests, base64, os
TOKEN = os.environ["GH_TOKEN"]
REPO = "Sacha30650/livres-kdp-sacha"
url = "https://d8j0ntlcm91z4.cloudfront.net/user_33ZLmugzCzPZPElXa3iEZVG6Gq0/hf_20260605_202735_b0c68d15-ffa6-4320-bbfe-756bd448bbf0.png"
path = "tests_layout/scene_haut_vide.png"
img = requests.get(url).content
print("img", len(img), "bytes")
b64 = base64.b64encode(img).decode()
h = {"Authorization": f"token {TOKEN}", "Accept": "application/vnd.github+json"}
api = f"https://api.github.com/repos/{REPO}/contents/{path}"
r = requests.get(api, headers=h, params={"ref":"main"})
payload = {"message": f"add {path}", "content": b64, "branch":"main"}
if r.status_code == 200: payload["sha"] = r.json()["sha"]
pr = requests.put(api, headers=h, json=payload)
print("PUT", pr.status_code, "DONE")
