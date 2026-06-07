import requests, base64, os
TOKEN=os.environ["GH_TOKEN"]; REPO="Sacha30650/livres-kdp-sacha"
B="https://d8j0ntlcm91z4.cloudfront.net/user_33ZLmugzCzPZPElXa3iEZVG6Gq0/"
imgs={
 "illustrations_P6/p98_enlaces.png":"hf_20260607_064343_75257fed-9ab5-441e-ab95-d676970b0d68.png",
 "illustrations_P6/p99_miroir.png":"hf_20260607_064349_55d695a6-8f81-4854-acf5-0520925e8fa6.png",
 "illustrations_P6/p100_matrescence.png":"hf_20260607_064354_4a0733ca-2424-4fa9-9fd8-34fb9d9cea61.png",
 "illustrations_P6/p101_multitache.png":"hf_20260607_064400_3715cc66-de02-494d-92e8-47703655a60e.png",
 "illustrations_P6/p102_cafe.png":"hf_20260607_064405_a69c68e0-d28f-4e41-b87c-61c135e0cebf.png",
 "illustrations_P6/p103_chargementale.png":"hf_20260607_064411_d7c653e3-a38c-4810-9c5b-adfb36279b1b.png",
 "illustrations_P6/p104_bouderie.png":"hf_20260607_064417_aa12395a-2151-439d-8029-7a1db6a2d1d2.png",
 "illustrations_P6/p106_relais.png":"hf_20260607_064423_88140dfb-5981-4c9e-a26f-a42ce6a365b5.png",
 "illustrations_P6/p107_frontcommun.png":"hf_20260607_064429_4c504f58-cd83-42a1-83f8-ddfdedd30f00.png",
 "illustrations_P6/p108_visiteutile.png":"hf_20260607_064434_662247ee-5c33-4b61-bb40-59fe3d602f41.png",
 "illustrations_P6/p109_corps.png":"hf_20260607_064441_6a602712-de45-48b3-bbc2-0746d0c07168.png",
 "illustrations_P6/p110_santementale.png":"hf_20260607_064446_405580f7-bdf9-45a9-9ee6-3c3e2d388e75.png",
 "illustrations_P6/p111_bureau.png":"hf_20260607_064453_7397292c-26c1-4420-b51f-5612449be2e1.png",
 "illustrations_P6/p112_maison.png":"hf_20260607_064458_16cc306e-12c5-4747-ac26-ca8ed2dd7d25.png",
 "illustrations_P6/p113_creche.png":"hf_20260607_064505_83520c2e-49fa-4d9d-8eb2-66adfae1094b.png",
 "illustrations_P6/p114_culpabilite.png":"hf_20260607_064511_a5860dc1-bf11-4afa-9e5e-ed1b1bc5554d.png",
 "illustrations_P6/p115_pacte.png":"hf_20260607_064517_32fd02da-ad46-40bf-a2b6-a37b5adbaddc.png",
 "illustrations_P6/p116_album.png":"hf_20260607_064523_01e0170d-2933-473c-9ef5-763fcf0326db.png",
 "illustrations_P6/p117_trinque.png":"hf_20260607_064529_cfc6c0fa-6125-42c2-82b8-c19dff59d0d5.png",
 "illustrations_P6/p118_serein.png":"hf_20260607_064535_1c738002-447d-4ae4-8b27-eb99335b4428.png",
 "illustrations_P6/p119_famille.png":"hf_20260607_064738_4241d976-4cc5-4cc0-8e73-0c84387b85e3.png",
}
hh={"Authorization":f"token {TOKEN}","Accept":"application/vnd.github+json"}
ok=0
for path,fn in imgs.items():
    try: img=requests.get(B+fn,timeout=60).content
    except Exception as e: print("ERR",path,e); continue
    if len(img)<10000: print("SKIP",path,len(img)); continue
    b64=base64.b64encode(img).decode()
    api=f"https://api.github.com/repos/{REPO}/contents/{path}"
    r=requests.get(api,headers=hh,params={"ref":"main"})
    p={"message":f"add {path}","content":b64,"branch":"main"}
    if r.status_code==200: p["sha"]=r.json()["sha"]
    s=requests.put(api,headers=hh,json=p).status_code
    print(path.split("/")[-1], len(img),"->",s)
    if s in (200,201): ok+=1
print(f"DONE {ok}/21")
