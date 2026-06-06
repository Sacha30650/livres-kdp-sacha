import requests, base64, os
TOKEN=os.environ["GH_TOKEN"]; REPO="Sacha30650/livres-kdp-sacha"
B="https://d8j0ntlcm91z4.cloudfront.net/user_33ZLmugzCzPZPElXa3iEZVG6Gq0/"
imgs={
 "illustrations_P4/p58_table.png":"hf_20260606_213103_8cfbbf39-8b03-418b-9a73-7ee80f02e5aa.png",
 "illustrations_P4/p59_allaite.png":"hf_20260606_213109_5ab1ef2c-18f0-4e8d-b57f-5f621c29f3ff.png",
 "illustrations_P4/p60_biberonnuit.png":"hf_20260606_213114_2fed6241-196b-4ede-a8bb-322b871048d4.png",
 "illustrations_P4/p61_rot.png":"hf_20260606_213119_64b08b51-9642-4953-8d14-5d2dc23b4ea8.png",
 "illustrations_P4/p62_prep.png":"hf_20260606_213125_9d287b0c-116d-488e-99f0-7743f29f811b.png",
 "illustrations_P4/p63_cuillere.png":"hf_20260606_213131_63443362-ad03-4971-b5c6-60185ce03294.png",
 "illustrations_P4/p64_textures.png":"hf_20260606_213136_853c7e62-7d66-4e2a-8654-4b5826fc14a3.png",
 "illustrations_P4/p65_dme.png":"hf_20260606_213143_294f1fc2-c1eb-48db-b429-2f7c75acb87f.png",
 "illustrations_P4/p66_securite.png":"hf_20260606_213148_2353b9be-6587-4853-8bac-7ef516d1e0a9.png",
 "illustrations_P4/p67_allergenes.png":"hf_20260606_213154_e0290746-5488-46f1-9f7e-1a71f6f7346c.png",
 "illustrations_P4/p68_quantites.png":"hf_20260606_213200_f66568c7-9118-44d7-88ca-27fec00414ac.png",
 "illustrations_P4/p69_bazar.png":"hf_20260606_213205_d70a53e5-899a-4227-bef5-a2756fe864b5.png",
 "illustrations_P4/p70_refus.png":"hf_20260606_213211_fd0a95e5-4b08-4aca-9ba7-7f06a26b54c4.png",
 "illustrations_P4/p71_rayon.png":"hf_20260606_213219_e9219d3c-03fa-427a-9097-4a5a2e366a2c.png",
 "illustrations_P4/p72_recettes.png":"hf_20260606_213225_d663d8e2-21f2-4d6d-86de-5e422ed11e35.png",
 "illustrations_P4/p73_legumes.png":"hf_20260606_213230_2cee8988-856d-4c29-b5b3-7d76088e196d.png",
 "illustrations_P4/p75_jugement.png":"hf_20260606_213236_462d4f88-97dd-450f-bff6-e14ce09aaaf9.png",
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
print(f"DONE {ok}/17")
