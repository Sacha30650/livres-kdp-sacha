"""Livre parentalite Partie 1 - DA croquis : upload des 7 illustrations vers GitHub (retry + reprise)."""
import urllib.request as u, urllib.error, os, json, base64, time

T = os.environ.get('GHTOK', '')
A = 'https://api.github.com/repos/Sacha30650/livres-kdp-sacha/contents/'
P = 'Livre-parentalite_Notre-premiere-annee-a-3/Sources/images-croquis/'
CDN = 'https://d8j0ntlcm91z4.cloudfront.net/user_33ZLmugzCzPZPElXa3iEZVG6Gq0/'

IMGS = [
    ('hero_bebe',    CDN + 'hf_20260523_051454_cb934ac5-fb61-46b9-a233-e94086cb4331.png'),
    ('p1_trio',      CDN + 'hf_20260523_051621_3db459c3-da45-4150-8b73-8a42b2e630ee.png'),
    ('p1_materiel',  CDN + 'hf_20260523_052122_1a374aaa-9ae4-4cf8-a5b2-dd9e2e5012f4.png'),
    ('p1_sommeil',   CDN + 'hf_20260523_051635_20601fff-e5ac-4a71-bef4-35002e1dbc4e.png'),
    ('p1_valise',    CDN + 'hf_20260523_052132_9797604d-4eb8-44ff-97b1-611cc1922832.png'),
    ('p1_demarches', CDN + 'hf_20260523_051648_bf4b066f-d2e5-4135-b60b-3d1b8d5cf06d.png'),
    ('p1_coparent',  CDN + 'hf_20260523_052139_9d391505-02c8-491f-96da-337921abfa4c.png'),
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
        'message': 'Parentalite P1 croquis ' + path,
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

print('Upload des 7 illustrations croquis Partie 1 vers GitHub...')
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
print(f'Resume: {ok} uploadees, {skip} deja la, {fail} echouees')
if fail > 0:
    print('--> Relance la commande, les SKIP iront vite')
else:
    print('DONE - tout est sur GitHub')
