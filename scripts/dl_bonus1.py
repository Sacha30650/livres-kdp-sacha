import requests, base64, os
TOKEN=os.environ["GH_TOKEN"]; REPO="Sacha30650/livres-kdp-sacha"
B="https://d8j0ntlcm91z4.cloudfront.net/user_33ZLmugzCzPZPElXa3iEZVG6Gq0/"
imgs={
 "illustrations_BONUS1/p120_titre.png":"hf_20260607_070517_9afdbafc-9a30-4234-9f71-58a36e6b710a.png",
 "illustrations_BONUS1/p121_soir.png":"hf_20260607_070522_fb69c360-786b-4a20-af76-9fa866bdc577.png",
 "illustrations_BONUS1/p122_eveille.png":"hf_20260607_070527_8b30a2e9-79c7-4c30-bea1-2054712a5ec0.png",
 "illustrations_BONUS1/p123_oiseaux.png":"hf_20260607_070532_97f5f9af-452c-4b04-a31d-4c883e30835b.png",
 "illustrations_BONUS1/p124_renard.png":"hf_20260607_070537_99732b83-91d3-4495-b970-4d905fab5986.png",
 "illustrations_BONUS1/p125_riviere.png":"hf_20260607_070542_154b97fc-9649-4428-a2c4-2e71696af4ba.png",
 "illustrations_BONUS1/p126_biche.png":"hf_20260607_070546_bac44a79-4f1e-42dc-9943-8a2402d5a6e3.png",
 "illustrations_BONUS1/p127_hibou.png":"hf_20260607_070552_48dc6d61-42b6-4254-847b-014a82f193a8.png",
 "illustrations_BONUS1/p128_ours.png":"hf_20260607_070557_d583882b-3f19-47a2-948d-b93717dc3185.png",
 "illustrations_BONUS1/p129_lucioles.png":"hf_20260607_070602_b412ec60-291a-427b-8544-30b9ba97c543.png",
 "illustrations_BONUS1/p130_foret.png":"hf_20260607_070607_5add1101-66b7-4d85-873f-83211a013a8a.png",
 "illustrations_BONUS1/p131_retour.png":"hf_20260607_070612_3efaabda-60d8-4bc2-9edd-624bf256047e.png",
 "illustrations_BONUS1/p132_calin.png":"hf_20260607_070617_05fba6b2-51ad-4834-a8d9-c41ad0a71bed.png",
 "illustrations_BONUS1/p133_blotti.png":"hf_20260607_070622_1d8fef8c-b28d-4aa1-9d8d-2860ba77d235.png",
 "illustrations_BONUS1/p134_terrier.png":"hf_20260607_070812_27ece56b-e758-452b-b587-b0705a2e8810.png",
 "illustrations_BONUS1/p135_endormi.png":"hf_20260607_070627_1b0beb32-5fdb-4b5b-908f-31962fbc4fdf.png",
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
print(f"DONE {ok}/16")
