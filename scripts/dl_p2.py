import requests, base64, os
TOKEN=os.environ["GH_TOKEN"]; REPO="Sacha30650/livres-kdp-sacha"
B="https://d8j0ntlcm91z4.cloudfront.net/user_33ZLmugzCzPZPElXa3iEZVG6Gq0/"
imgs={
 "illustrations_P2/p22_canape.png":"hf_20260606_185852_63428d65-3de8-4191-85e1-036b0964bfd8.png",
 "illustrations_P2/p23_porte.png":"hf_20260606_185858_8cd15cb4-6aa0-48f5-9f3b-7be842acc7f0.png",
 "illustrations_P2/p24_cuisine.png":"hf_20260606_185904_7c8925ed-2ab0-44d7-a0b7-c3ef0bf7d559.png",
 "illustrations_P2/p25_bebe.png":"hf_20260606_185910_294d37a2-c52c-47e8-834a-76c69585fcdc.png",
 "illustrations_P2/p26_nuit.png":"hf_20260606_185917_cb3da1c4-adf7-424f-97b9-a005c4165a5d.png",
 "illustrations_P2/p27_change.png":"hf_20260606_185924_b4222380-9270-499e-b18c-7092477e7a82.png",
 "illustrations_P2/p28_bain.png":"hf_20260606_185931_d6505abd-d8b2-434e-bc76-3463894d4441.png",
 "illustrations_P2/p29_soins.png":"hf_20260606_185936_c34127ef-8fbc-4940-85db-a49cbf81502c.png",
 "illustrations_P2/p30_visites.png":"hf_20260606_185943_a1e34da8-9947-4cc2-84e2-2404ace2c735.png",
 "illustrations_P2/p32_relais.png":"hf_20260606_185950_9c82a072-2531-4c96-a2c9-2deb32167f15.png",
 "illustrations_P2/p33_passage.png":"hf_20260606_190011_00f816c0-fdf2-4744-83e7-1b2271020483.png",
 "illustrations_P2/p34_retour.png":"hf_20260606_190018_5f70237f-5530-473a-b3ac-0a3835a66e3a.png",
 "illustrations_P2/p35_telephone.png":"hf_20260606_190024_a2683b81-16d4-4ba6-84e3-60c015e20846.png",
 "illustrations_P2/p36_dosados.png":"hf_20260606_190031_b9f46805-3da1-4c59-a860-6c1a60345aa5.png",
 "illustrations_P2/p37_sourire.png":"hf_20260606_190037_d50b91e0-9ad9-40b3-ae2d-d84d4819f34f.png",
}
hh={"Authorization":f"token {TOKEN}","Accept":"application/vnd.github+json"}
ok=0
for path,fn in imgs.items():
    try:
        img=requests.get(B+fn,timeout=60).content
    except Exception as e:
        print("ERR dl",path,e); continue
    if len(img)<10000: print("SKIP",path,len(img),"b"); continue
    b64=base64.b64encode(img).decode()
    api=f"https://api.github.com/repos/{REPO}/contents/{path}"
    r=requests.get(api,headers=hh,params={"ref":"main"})
    p={"message":f"add {path}","content":b64,"branch":"main"}
    if r.status_code==200: p["sha"]=r.json()["sha"]
    s=requests.put(api,headers=hh,json=p).status_code
    print(path.split("/")[-1], len(img),"b ->", s)
    if s in (200,201): ok+=1
print(f"DONE {ok}/15")
