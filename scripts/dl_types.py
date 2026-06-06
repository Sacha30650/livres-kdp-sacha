import requests, base64, os
TOKEN=os.environ["GH_TOKEN"]; REPO="Sacha30650/livres-kdp-sacha"
BASE="https://d8j0ntlcm91z4.cloudfront.net/user_33ZLmugzCzPZPElXa3iEZVG6Gq0/"
imgs={
 "tests_layout/typeC_cote.png":"hf_20260606_135751_9620352f-95e2-44e2-9d04-0f5f931d091f.png",
 "tests_layout/typeB_bandeau.png":"hf_20260606_135759_8bb37f52-0fd3-4819-a396-166636999ed6.jpeg",
 "tests_layout/typeD_coin.png":"hf_20260606_135806_46063811-dc29-4fe1-9152-ff12f8be2473.png",
}
hh={"Authorization":f"token {TOKEN}","Accept":"application/vnd.github+json"}
for path,fn in imgs.items():
    img=requests.get(BASE+fn).content
    print(path,len(img),"bytes")
    b64=base64.b64encode(img).decode()
    api=f"https://api.github.com/repos/{REPO}/contents/{path}"
    r=requests.get(api,headers=hh,params={"ref":"main"})
    p={"message":f"add {path}","content":b64,"branch":"main"}
    if r.status_code==200: p["sha"]=r.json()["sha"]
    print("  PUT",requests.put(api,headers=hh,json=p).status_code)
print("DONE")
