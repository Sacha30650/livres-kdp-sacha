import requests, base64, os
TOKEN=os.environ["GH_TOKEN"]; REPO="Sacha30650/livres-kdp-sacha"
B="https://d8j0ntlcm91z4.cloudfront.net/user_33ZLmugzCzPZPElXa3iEZVG6Gq0/"
imgs={
 "illustrations_BONUS1/p121_soir.png":"hf_20260607_072627_5d602a60-ecaf-4cb1-9dd3-8903fbdff254.png",
 "illustrations_BONUS1/p133_blotti.png":"hf_20260607_072633_5efc5b32-d10a-4329-b900-e443198d4b50.png",
}
hh={"Authorization":f"token {TOKEN}","Accept":"application/vnd.github+json"}
ok=0
for path,fn in imgs.items():
    img=requests.get(B+fn,timeout=60).content
    if len(img)<10000: print("SKIP",path,len(img)); continue
    b64=base64.b64encode(img).decode()
    api=f"https://api.github.com/repos/{REPO}/contents/{path}"
    r=requests.get(api,headers=hh,params={"ref":"main"})
    p={"message":f"upd {path}","content":b64,"branch":"main"}
    if r.status_code==200: p["sha"]=r.json()["sha"]
    s=requests.put(api,headers=hh,json=p).status_code
    print(path.split("/")[-1], len(img),"->",s)
    if s in (200,201): ok+=1
print(f"DONE {ok}/2")
