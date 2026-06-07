import requests, base64, os
TOKEN=os.environ["GH_TOKEN"]; REPO="Sacha30650/livres-kdp-sacha"
B="https://d8j0ntlcm91z4.cloudfront.net/user_33ZLmugzCzPZPElXa3iEZVG6Gq0/"
imgs={
 "illustrations_P5/p76_emerveille.png":"hf_20260606_215517_4a70b01b-065f-468f-9f85-7f35b6b89336.png",
 "illustrations_P5/p77_observe.png":"hf_20260606_215522_c3761e54-4711-4bae-8b33-d449fb77b4b1.png",
 "illustrations_P5/p78_porte.png":"hf_20260606_215528_7ccc8305-c0b9-4172-9aae-4244d1313452.png",
 "illustrations_P5/p79_sourire.png":"hf_20260606_215533_d90c68e0-c24a-4f1f-8705-5c77baa6d6d1.png",
 "illustrations_P5/p80_mains.png":"hf_20260606_215539_01a5eb5b-708a-40ea-bb8d-25f2803bdb54.png",
 "illustrations_P5/p81_attrape.png":"hf_20260606_215545_8567c4a7-9dd9-4049-84c1-dc795cce0e93.png",
 "illustrations_P5/p82_textures.png":"hf_20260606_215551_77408a55-5e10-4270-aa7b-1caba3bc06c5.png",
 "illustrations_P5/p83_assis.png":"hf_20260606_215558_71c79407-f584-40f4-a807-43a75927d3ee.png",
 "illustrations_P5/p84_bouche.png":"hf_20260606_215604_64329db1-9c61-415f-8ac1-b67bcb7d9de6.png",
 "illustrations_P5/p85_coucou.png":"hf_20260606_215657_64148fed-d631-45ae-b709-5c0be43015aa.png",
 "illustrations_P5/p86_quatrepattes.png":"hf_20260606_215627_78571068-2d2d-4dd5-a67c-711965cd1615.png",
 "illustrations_P5/p87_imite.png":"hf_20260606_215633_95992a74-c059-4d5a-8682-9628eddb00c2.png",
 "illustrations_P5/p88_debout.png":"hf_20260606_215642_ff6d0a2d-4cb4-405b-b051-d343a02617b2.png",
 "illustrations_P5/p89_bougie.png":"hf_20260606_215649_91fdc165-5d7a-46ca-8a2b-bc45f4be74d8.png",
 "illustrations_P5/p90_jouets.png":"hf_20260606_215704_53225415-6683-4879-abe6-60a76f914813.png",
 "illustrations_P5/p91_lire.png":"hf_20260606_215710_e5c1cfad-80f2-4940-9a07-b3390f874788.png",
 "illustrations_P5/p92_chanson.png":"hf_20260606_215718_b695e381-9154-45fc-b540-bdbeec80e855.png",
 "illustrations_P5/p93_balade.png":"hf_20260606_215725_71db1021-060d-4645-a2ce-44600a653473.png",
 "illustrations_P5/p94_trop.png":"hf_20260606_215734_7659b44e-0a0f-4616-9910-324a5f150722.png",
 "illustrations_P5/p95_journeedouce.png":"hf_20260607_063225_274c5a0b-42af-42dc-a273-11dbea05269c.png",
 "illustrations_P5/p97_competition.png":"hf_20260606_215747_632aace8-8e2c-47fe-90c3-b1f08d3ff608.png",
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
