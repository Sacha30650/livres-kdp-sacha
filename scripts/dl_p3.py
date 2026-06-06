import requests, base64, os
TOKEN=os.environ["GH_TOKEN"]; REPO="Sacha30650/livres-kdp-sacha"
B="https://d8j0ntlcm91z4.cloudfront.net/user_33ZLmugzCzPZPElXa3iEZVG6Gq0/"
imgs={
 "illustrations_P3/p38_litlarge.png":"hf_20260606_194736_6c7bf8a5-011a-433e-b0a8-04e44db44576.png",
 "illustrations_P3/p39_question.png":"hf_20260606_194742_db8aaa78-c0b3-472b-9a85-74405db06c09.png",
 "illustrations_P3/p40_berceau.png":"hf_20260606_194747_98eae972-1c4b-442b-b0fe-20aeae56971a.png",
 "illustrations_P3/p41_torse.png":"hf_20260606_194752_33e53cd4-3bad-4d6a-8e82-1fa50238f3e4.png",
 "illustrations_P3/p42_profil.png":"hf_20260606_194758_b8bc43ec-ebf0-4c7c-a389-54a3faa641ab.png",
 "illustrations_P3/p43_peaupeau.png":"hf_20260606_194803_3b6fe692-6984-4878-836c-2f42fbfbfa91.png",
 "illustrations_P3/p44_solnuit.png":"hf_20260606_194809_d671c6f5-5559-450c-a287-f50c7ecb45f2.png",
 "illustrations_P3/p45_rituel.png":"hf_20260606_194815_72d0beff-abe6-4188-8641-90244421e9cb.png",
 "illustrations_P3/p46_barreaux.png":"hf_20260606_194820_4a546f74-b5c2-4eab-911c-f4bc7b476005.png",
 "illustrations_P3/p47_matincafe.png":"hf_20260606_194826_73659877-8a5d-4623-be95-7195d26517f1.png",
 "illustrations_P3/p48_sieste.png":"hf_20260606_194831_07699348-1e63-49ee-b7f4-f8f3eb85f280.png",
 "illustrations_P3/p49_silhouette.png":"hf_20260606_194835_f4a99b11-c3e7-473b-b16d-47e279872ba5.png",
 "illustrations_P3/p50_pacte.png":"hf_20260606_194841_210052d5-dfaa-4c87-b04a-abc02d578663.png",
 "illustrations_P3/p51_histoire.png":"hf_20260606_194847_432485e7-eebb-4c37-865f-0bf8fee17439.png",
 "illustrations_P3/p52_bercedebout.png":"hf_20260606_194854_62e834fb-e417-4bce-bb05-cdf8d333ac13.png",
 "illustrations_P3/p53_epaule.png":"hf_20260606_194859_badb42c9-a925-4b41-a67f-a806e740d010.png",
 "illustrations_P3/p54_objetsnuit.png":"hf_20260606_194911_93b995e3-6a11-4ca2-aaab-a0f628a35866.png",
 "illustrations_P3/p57_dispute.png":"hf_20260606_194916_4907496b-b716-4e1a-8089-1d12260ed3f8.png",
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
print(f"DONE {ok}/18")
