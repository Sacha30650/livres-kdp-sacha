import requests, base64, os
TOKEN=os.environ["GH_TOKEN"]; REPO="Sacha30650/livres-kdp-sacha"
url="https://d8j0ntlcm91z4.cloudfront.net/user_33ZLmugzCzPZPElXa3iEZVG6Gq0/hf_20260606_143250_30937221-b3b0-4f57-bdef-cbc796969961.png"
path="illustrations_P1/p10_chambre.png"
img=requests.get(url).content
print("img",len(img),"bytes")
b64=base64.b64encode(img).decode()
hh={"Authorization":f"token {TOKEN}","Accept":"application/vnd.github+json"}
api=f"https://api.github.com/repos/{REPO}/contents/{path}"
r=requests.get(api,headers=hh,params={"ref":"main"})
p={"message":"add p10_chambre","content":b64,"branch":"main"}
if r.status_code==200: p["sha"]=r.json()["sha"]
print("PUT",requests.put(api,headers=hh,json=p).status_code,"DONE")
