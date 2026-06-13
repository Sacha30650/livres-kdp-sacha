#!/usr/bin/env python3
# Recupere P22 depuis CloudFront, la compresse en JPEG, la pousse sur GitHub.
# a-Shell possede Pillow. Token via env: export GH_TOKEN=ghp_xxx
import os, io, base64, json, urllib.request, urllib.error
from PIL import Image

TOKEN = os.environ.get("GH_TOKEN", "")
if not TOKEN:
    raise SystemExit("ERREUR : export GH_TOKEN=ghp_xxx puis relance.")
REPO = "Sacha30650/livres-kdp-sacha"
SRC  = "https://d8j0ntlcm91z4.cloudfront.net/user_33ZLmugzCzPZPElXa3iEZVG6Gq0/hf_20260613_080452_0e78f660-429f-4cdc-a5d9-05e535abd456.png"
DST  = "zola/images/P22_fresque_finie.jpeg"   # version JPEG

print("Telechargement P22 depuis CloudFront...")
req = urllib.request.Request(SRC, headers={"User-Agent":"Mozilla/5.0"})
with urllib.request.urlopen(req, timeout=180) as r:
    raw = r.read()
print(f"  source PNG : {len(raw)//1024} Ko")

img = Image.open(io.BytesIO(raw)).convert("RGB")
buf = io.BytesIO()
img.save(buf, format="JPEG", quality=92, optimize=True)
jpg = buf.getvalue()
print(f"  JPEG q92   : {len(jpg)//1024} Ko")

def gh_sha(path):
    u=f"https://api.github.com/repos/{REPO}/contents/{path}"
    rq=urllib.request.Request(u,headers={"Authorization":f"token {TOKEN}","Accept":"application/vnd.github+json"})
    try:
        with urllib.request.urlopen(rq) as rr: return json.load(rr).get("sha")
    except Exception: return None

u=f"https://api.github.com/repos/{REPO}/contents/{DST}"
data={"message":"Add P22 (compressed JPEG)","content":base64.b64encode(jpg).decode()}
sha=gh_sha(DST)
if sha: data["sha"]=sha
rq=urllib.request.Request(u,data=json.dumps(data).encode(),method="PUT",
    headers={"Authorization":f"token {TOKEN}","Accept":"application/vnd.github+json"})
try:
    with urllib.request.urlopen(rq) as rr:
        print("PUSH OK ->", json.load(rr)["content"]["path"])
except urllib.error.HTTPError as e:
    print("HTTP", e.code, e.read().decode()[:200])
