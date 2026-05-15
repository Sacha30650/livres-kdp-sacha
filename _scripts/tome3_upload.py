"""Tome 3 : upload résilient (retry + reprise)."""
import urllib.request as u, urllib.error, os, json, base64, time

T = os.environ.get('GHTOK', '')
B = 'https://d8j0ntlcm91z4.cloudfront.net/user_33ZLmugzCzPZPElXa3iEZVG6Gq0/'
A = 'https://api.github.com/repos/Sacha30650/livres-kdp-sacha/contents/'
P = 'Tome-3_Lila-et-la-cle-qui-chante/Sources/images/'

def headers_get():
    return {'Authorization': 'token ' + T, 'Accept': 'application/vnd.github+json'}

def file_exists(path):
    try:
        req = u.Request(A + path, headers=headers_get())
        u.urlopen(req, timeout=15).read()
        return True
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return False
        return False
    except:
        return False

def download_img(url, retries=3):
    for i in range(retries):
        try:
            return u.urlopen(url, timeout=30).read()
        except Exception as e:
            print('  retry dl', i+1, str(e)[:50])
            time.sleep(2)
    return None

def upload(path, data, retries=3):
    body = json.dumps({
        'message': 'T3 ' + path,
        'content': base64.b64encode(data).decode(),
        'branch': 'main',
    }).encode()
    for i in range(retries):
        try:
            req = u.Request(A + path, data=body, method='PUT',
                            headers={**headers_get(), 'Content-Type': 'application/json'})
            u.urlopen(req, timeout=30).read()
            return True
        except Exception as e:
            print('  retry up', i+1, str(e)[:50])
            time.sleep(3)
    return False

# Récupérer la liste depuis le repo
print('Lecture liste...')
lst_url = A + '_scripts/tome3_urls.txt'
lst = u.urlopen(u.Request(lst_url, headers={**headers_get(), 'Accept': 'application/vnd.github.v3.raw'}), timeout=15).read().decode().strip().split('\n')

print('Total:', len(lst), 'images')
print()

ok = 0
skip = 0
fail = 0
for line in lst:
    name, fname = line.strip().split(' ', 1)
    path = P + name + '.png'
    if file_exists(path):
        print('SKIP', name, '(deja sur github)')
        skip += 1
        continue
    print('DL  ', name, '...', end=' ', flush=True)
    data = download_img(B + fname)
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
