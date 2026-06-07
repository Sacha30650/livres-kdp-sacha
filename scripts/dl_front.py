import requests, base64, os
TOKEN=os.environ["GH_TOKEN"]; REPO="Sacha30650/livres-kdp-sacha"
B="https://d8j0ntlcm91z4.cloudfront.net/user_33ZLmugzCzPZPElXa3iEZVG6Gq0/"
imgs={
 "illustrations_FRONT/p1_titre.png":"hf_20260607_083748_2a14e083-8fad-4039-b7e8-a0377f0b7a18.png",
 "illustrations_FRONT/p2_team.png":"hf_20260607_083754_58500f14-bdda-4eca-923c-2b60e77cabbc.png",
 "illustrations_FRONT/p3_spot.png":"hf_20260607_083758_9cb2d5f1-3c5e-4a56-be8f-220915dc4b71.png",
 "illustrations_FRONT/p4_lecture.png":"hf_20260607_083803_dd99774a-b016-40d3-a54a-d6a5937eee32.png",
 "illustrations_FRONT/p5_nouveaune.png":"hf_20260607_083809_88b4af83-ae13-44c9-9387-0db05006bac0.png",
}
hh={"Authorization":f"token {TOKEN}","Accept":"application/vnd.github+json"}
ok=0
for path,fn in imgs.items():
    img=requests.get(B+fn,timeout=60).content
    if len(img)<10000: print("SKIP",path,len(img)); continue
    b64=base64.b64encode(img).decode()
    api=f"https://api.github.com/repos/{REPO}/contents/{path}"
    r=requests.get(api,headers=hh,params={"ref":"main"})
    p={"message":f"add {path}","content":b64,"branch":"main"}
    if r.status_code==200: p["sha"]=r.json()["sha"]
    s=requests.put(api,headers=hh,json=p).status_code
    print(path.split("/")[-1], len(img),"->",s)
    if s in (200,201): ok+=1
print(f"DONE {ok}/5")
