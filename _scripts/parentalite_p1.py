"""Livre parentalité Partie 1 : upload résilient des illustrations vers GitHub (retry + reprise)."""
import urllib.request as u, urllib.error, os, json, base64, time

T = os.environ.get('GHTOK', '')
A = 'https://api.github.com/repos/Sacha30650/livres-kdp-sacha/contents/'
P = 'Livre-parentalite_Notre-premiere-annee-a-3/Sources/images/'

# (nom local, URL Higgsfield)
IMGS = [
    ('hero_bebe',     'https://d8j0ntlcm91z4.cloudfront.net/user_33ZLmugzCzPZPElXa3iEZVG6Gq0/hf_20260522_191415_149e129d-cc37-4e1e-a730-246e87824598.jpeg'),
    ('p1_ouverture',  'https://d8j0ntlcm91z4.cloudfront.net/user_33ZLmugzCzPZPElXa3iEZVG6Gq0/hf_20260522_201656_c5b00e3a-a0a0-47e7-bfa2-fae949784b24.png'),
    ('p1_materiel',   'https://d8j0ntlcm91z4.cloudfront.net/user_33ZLmugzCzPZPElXa3iEZVG6Gq0/hf_20260522_201707_3dee538d-b004-4cee-b7a4-6a77a8d5bb86.png'),
    ('p1_sommeil',    'https://d8j0ntlcm91z4.cloudfront.net/user_33ZLmugzCzPZPElXa3iEZVG6Gq0/hf_20260522_201715_fef37eb7-b052-4f8f-ada2-48429d04531b.png'),
    ('p1_valise',     'https://d8j0ntlcm91z4.cloudfront.net/user_33ZLmugzCzPZPElXa3iEZVG6Gq0/hf_20260522_201722_6463dc3a-1c96-4c09-89ad-cc19c797dfa2.png'),
    ('p1_demarches',  'https://d8j0ntlcm91z4.cloudfront.net/user_33ZLmugzCzPZPElXa3iEZVG6Gq0/hf_20260522_201729_b618ce9f-be1d-423c-bd7b-7d297ad112c4.png'),
]

def headers():
    return {'Authorization': 'token ' + T, 'Accept': 'application/vnd.github+json'}

def exists(path):
    try:
        u.urlopen(u.Request(A + path, headers=headers()), timeout=15).read()
        return True
    except:
        return False

def download(url, retries=3):
    for i in range(retries):
        try:
            return u.urlopen(url, timeout=30).read()
        except Exception as e:
            print('  retry dl', i+1, str(e)[:50])
            time.sleep(2)
    return None

def upload(path, data, retries=3):
    body = json.dumps({
        'message': 'Parentalite P1 ' + path,
        'content': base64.b64encode(data).decode(),
        'branch': 'main',
    }).encode()
    for i in range(retries):
        try:
            req = u.Request(A + path, data=body, method='PUT',
                            headers={**headers(), 'Content-Type': 'application/json'})
            u.urlopen(req, timeout=30).read()
            return True
        except Exception as e:
            print('  retry up', i+1, str(e)[:50])
            time.sleep(3)
    return False

print('Upload des 6 illustrations Partie 1 vers GitHub...')
print()
ok = skip = fail = 0
for name, url in IMGS:
    ext = '.jpeg' if url.endswith('.jpeg') else '.png'
    path = P + name + ext
    if exists(path):
        print('SKIP', name, '(deja sur github)')
        skip += 1
        continue
    print('DL  ', name, '...', end=' ', flush=True)
    data = download(url)
    if data is None:
        print('FAIL download')
        fail += 1
        continue
    print('UP', end=' ', flush=True)
    if upload(path, data):
        print('OK')
        ok += 1
    else:
        print('FAIL upload')
        fail += 1

print()
print(f'Resume: {ok} uploadees, {skip} deja la, {fail} echouees')
if fail > 0:
    print('--> Relance la commande, les SKIP iront vite')
else:
    print('DONE - tout est sur GitHub')
