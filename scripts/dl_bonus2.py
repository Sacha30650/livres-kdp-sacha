import requests, base64, os
TOKEN=os.environ["GH_TOKEN"]; REPO="Sacha30650/livres-kdp-sacha"
B="https://d8j0ntlcm91z4.cloudfront.net/user_33ZLmugzCzPZPElXa3iEZVG6Gq0/"
imgs={
 "illustrations_BONUS2/spot_sommeil.png":"hf_20260607_081653_f50ea546-d990-402c-a4c8-d85dbb09f26b.png",
 "illustrations_BONUS2/spot_pleure.png":"hf_20260607_081657_f128630c-0db0-4921-afa5-284f60be092e.png",
 "illustrations_BONUS2/spot_repas.png":"hf_20260607_081702_55232226-dd8f-489a-a382-77f372b70755.png",
 "illustrations_BONUS2/spot_numeros.png":"hf_20260607_081708_0786879a-c3fc-490b-b47e-90a747013cdb.png",
 "illustrations_BONUS2/spot_pactes.png":"hf_20260607_081712_259c87fc-d1ce-44eb-af6a-2a4f2a216044.png",
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
