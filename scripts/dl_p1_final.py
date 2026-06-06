import requests, base64, os
TOKEN=os.environ["GH_TOKEN"]; REPO="Sacha30650/livres-kdp-sacha"
B="https://d8j0ntlcm91z4.cloudfront.net/user_33ZLmugzCzPZPElXa3iEZVG6Gq0/"
imgs={
 "illustrations_P1/p06_ouverture.png":"hf_20260606_143230_7f0b7a1b-3cf2-4609-840b-74c20381218a.png",
 "illustrations_P1/p07_tri.png":"hf_20260606_143236_78b380d6-7e2b-4e09-8ca9-d285856fbc3f.png",
 "illustrations_P1/p09_secondemain.png":"hf_20260606_143244_6ea979f2-4a67-4b87-8ec6-0ab6903b481f.png",
 "illustrations_P1/p10_chambre.png":"hf_20260606_143250_30937221-b3b0-4f57-bdef-cbc796969961.png",
 "illustrations_P1/p11_sommeil.png":"hf_20260606_143256_ad498089-5251-4abe-bad1-d33abb278d3e.png",
 "illustrations_P1/p12_sacs.png":"hf_20260606_143303_834e6117-1ec0-4c45-9f23-680bea778ece.png",
 "illustrations_P1/p13_kit.png":"hf_20260606_143319_e2049604-9267-4594-942f-d098302fefe4.png",
 "illustrations_P1/p17_admin.png":"hf_20260606_143326_02954d1c-51c0-4e39-ad8a-211a0d30986a.png",
 "illustrations_P1/p18_pochette.png":"hf_20260606_143332_634cda68-3390-49e9-b706-9c739690697c.png",
 "illustrations_P1/p14_typeD.png":"hf_20260606_143339_045cfbcc-141b-466c-aa4e-8350794bbb51.png",
}
hh={"Authorization":f"token {TOKEN}","Accept":"application/vnd.github+json"}
ok=0
for path,fn in imgs.items():
    img=requests.get(B+fn).content
    if len(img)<10000: print("SKIP",path,"(",len(img),"b)"); continue
    b64=base64.b64encode(img).decode()
    api=f"https://api.github.com/repos/{REPO}/contents/{path}"
    r=requests.get(api,headers=hh,params={"ref":"main"})
    p={"message":f"add {path}","content":b64,"branch":"main"}
    if r.status_code==200: p["sha"]=r.json()["sha"]
    s=requests.put(api,headers=hh,json=p).status_code
    print(path.split("/")[-1], len(img),"b ->", s)
    if s in (200,201): ok+=1
print(f"DONE {ok}/10")
