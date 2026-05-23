"""Livre parentalité Partie 1 : upload de l'illustration trio vers GitHub (retry + reprise)."""
import urllib.request as u, urllib.error, os, json, base64, time

T = os.environ.get('GHTOK', '')
A = 'https://api.github.com/repos/Sacha30650/livres-kdp-sacha/contents/'
P = 'Livre-parentalite_Notre-premiere-annee-a-3/Sources/images/'

IMGS = [
    ('p1_trio', 'https://d8j0ntlcm91z4.cloudfront.net/user_33ZLmugzCzPZPElXa3iEZVG6Gq0/hf_20260523_045700_f27555e0-3312-4198-b043-3abce16ba7dd.png'),
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

print('Upload illustration trio Partie 1 vers GitHub...')
print()
ok = skip = fail = 0
for name, url in IMGS:
    path = P + name + '.png'
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
print(f'Resume: {ok} uploadee, {skip} deja la, {fail} echouee')
if fail > 0:
    print('--> Relance la commande')
else:
    print('DONE - illustration trio sur GitHub')
