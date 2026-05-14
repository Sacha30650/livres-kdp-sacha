import urllib.request, os
T=os.environ.get('GHTOK','')
B='https://d8j0ntlcm91z4.cloudfront.net/user_33ZLmugzCzPZPElXa3iEZVG6Gq0/'
os.system('rm -rf repo')
os.system(f'git clone https://{T}@github.com/Sacha30650/livres-kdp-sacha.git repo')
d='repo/Tome-3_Lila-et-la-cle-qui-chante/Sources/images'
os.makedirs(d, exist_ok=True)
for line in open('repo/_scripts/tome3_urls.txt'):
    n,f=line.strip().split(' ',1)
    urllib.request.urlretrieve(B+f, f'{d}/{n}.png')
    print('+ '+n)
os.chdir('repo')
os.system('git config user.email me@local')
os.system('git config user.name Sacha')
os.system('git add -A && git commit -m "Tome 3 images" && git push')
print('DONE')
