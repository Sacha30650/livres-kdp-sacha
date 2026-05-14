#!/usr/bin/env python3
"""Tome 3 : download images Higgsfield + upload sur GitHub via API HTTPS (sans git)."""
import urllib.request, json, base64, os, sys

TOKEN = os.environ.get('GHTOK', '')
REPO = 'Sacha30650/livres-kdp-sacha'
BRANCH = 'main'
BASE = 'https://d8j0ntlcm91z4.cloudfront.net/user_33ZLmugzCzPZPElXa3iEZVG6Gq0'

IMGS = [
    ('p01', 'hf_20260514_214819_0151adb7-7a8c-4934-b532-edfe0783174d.png'),
    ('p02', 'hf_20260514_214827_dbc048b9-adb9-49a8-b4d4-a2628a22074c.png'),
    ('p03', 'hf_20260514_214835_64ad8062-e69b-46ae-b60c-15bab3613a41.png'),
    ('p04', 'hf_20260514_214843_a27fde6c-fa05-44c4-97fd-835b389bf15f.png'),
    ('p05', 'hf_20260514_214852_c03d171d-390a-4b84-8964-ac470b599b66.png'),
    ('p06', 'hf_20260514_214900_694f30f6-0c36-43c6-9ff7-83bc0b040aab.png'),
    ('p07', 'hf_20260514_214910_c09d1bbd-a854-40bd-b7c1-3bf8b47e1c9c.png'),
    ('p08', 'hf_20260514_214919_59c62027-443c-4eba-8a37-3e196832d4f7.png'),
    ('p09', 'hf_20260514_214927_bf47302d-2c74-4cd6-84ac-2b953346b94f.png'),
    ('p10', 'hf_20260514_214936_48e21812-aa65-4d04-8890-258db3dfd49f.png'),
    ('p11', 'hf_20260514_214945_e850c88d-6004-4526-a094-3db663c2bc19.png'),
    ('p12', 'hf_20260514_214953_96a83f7f-4807-4456-bf6c-e9bfb41b067c.png'),
    ('p13', 'hf_20260514_215002_c683bb1a-d5c4-4919-a32a-295b01d08924.png'),
    ('p14', 'hf_20260514_215012_40c6b955-59a8-475e-95ec-1ca94ed37d7b.png'),
    ('p15', 'hf_20260514_215021_55268b6a-98ee-4b4f-90b3-68852bbb20ed.png'),
    ('p16', 'hf_20260514_215030_0f4145b2-88f3-4a03-84f8-0711a71ccb76.png'),
    ('p17', 'hf_20260514_215039_b186eef8-ceff-4453-b4ec-f56c8a0e368e.png'),
    ('p18', 'hf_20260514_215048_af69ea3a-5ed6-4d4a-a596-2848f3a8eb72.png'),
    ('p19', 'hf_20260514_215056_00da4062-f36a-4ef6-b6c0-739debcd00c8.png'),
    ('p20', 'hf_20260514_215105_e3b89a96-f066-480a-a12d-0657e1f22d3d.png'),
    ('p21', 'hf_20260514_215114_ba0f64e0-5a9e-473d-b823-1d5c35a21cd8.png'),
    ('p22', 'hf_20260514_215123_a59fb0a0-8deb-45c7-860b-d53fb40e1215.png'),
    ('p23', 'hf_20260514_215131_b7269c4e-70d0-4ed3-bb06-dcb49005aa19.png'),
    ('p24', 'hf_20260514_215140_e6eedc3a-5733-424c-90c7-20e5bd681392.png'),
    ('p25', 'hf_20260514_215149_5f09d28c-a8c4-4b06-81f3-28ee663ea7dc.png'),
    ('p26', 'hf_20260514_215157_476ed811-4ce3-46bf-a39e-0022ca9abda7.png'),
    ('p27', 'hf_20260514_215205_6efca114-2dfc-4c3a-896a-4a6a4c2b0855.png'),
    ('p28', 'hf_20260514_215214_8b3aa83a-6429-4c72-9748-ff890fcf8a8a.png'),
    ('p29', 'hf_20260514_215223_b6019e27-f57f-4d34-8435-97fae4ad17fe.png'),
    ('p30', 'hf_20260514_215231_a706187c-a5f7-4a47-a49d-dbd70c1f493d.png'),
    ('cover_front', 'hf_20260514_215244_d45506b3-7413-46cb-9ebd-240cee21fde8.png'),
    ('cover_back', 'hf_20260514_215253_5518faf8-da1e-4d12-9189-d01cf3e65874.png'),
]


def gh_put(path, content_bytes, message):
    """Upload un fichier via l'API GitHub (PUT /contents)."""
    url = 'https://api.github.com/repos/' + REPO + '/contents/' + path
    body = json.dumps({
        'message': message,
        'content': base64.b64encode(content_bytes).decode('ascii'),
        'branch': BRANCH,
    }).encode('utf-8')
    req = urllib.request.Request(url, data=body, method='PUT')
    req.add_header('Authorization', 'token ' + TOKEN)
    req.add_header('Accept', 'application/vnd.github+json')
    req.add_header('Content-Type', 'application/json')
    try:
        with urllib.request.urlopen(req) as resp:
            return 'HTTP ' + str(resp.status)
    except urllib.error.HTTPError as e:
        body = e.read().decode()[:300]
        return 'HTTP ' + str(e.code) + ' BODY=' + body
    except Exception as e:
        return 'EXC ' + str(e)[:200]


print('Telechargement et upload des 32 images vers GitHub...')
print('(chaque upload prend 1-2 sec, total ~1 min)')
print()

target_base = 'Tome-3_Lila-et-la-cle-qui-chante/Sources/images/'

for name, fname in IMGS:
    src_url = BASE + '/' + fname
    try:
        # 1) Telecharger depuis Higgsfield
        with urllib.request.urlopen(src_url) as r:
            data = r.read()
        # 2) Upload vers GitHub via API
        result = gh_put(target_base + name + '.png', data, 'Tome 3 image ' + name)
        print('+ ' + name + '.png (' + str(result) + ')')
    except Exception as e:
        print('! ' + name + ' ERR ' + str(e)[:100])

print()
print('Done')
