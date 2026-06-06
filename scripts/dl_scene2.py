import requests, base64, os
TOKEN=os.environ["GH_TOKEN"]; REPO="Sacha30650/livres-kdp-sacha"
url="https://d8j0ntlcm91z4.cloudfront.net/user_33ZLmugzCzPZPElXa3iEZVG6Gq0/hf_20260606_133127_ce738aab-e50c-4338-b7f5-bb7a4e091ee1.png"
path="tests_layout/scene_riche_p08.png"
img=requests.get(url).content; print("img",len(img),"bytes")
b64=base64.b64encode(img).decode()
hh={"Authorization":f"token {TOKEN}","Accept":"application/vnd.github+json"}
api=f"https://api.github.com/repos/{REPO}/contents/{path}"
r=requests.get(api,headers=hh,params={"ref":"main"})
p={"message":"fix scene riche","content":b64,"branch":"main"}
if r.status_code==200: p["sha"]=r.json()["sha"]
print("PUT",requests.put(api,headers=hh,json=p).status_code,"DONE")
