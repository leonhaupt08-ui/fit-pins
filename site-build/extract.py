# Builds data/products.json from saved Pinterest API pin listings (paths passed as args).
import json, re, sys
BOARDS = {
 '1110207814332820701': ('herren-outfits', 'Herren Gym Outfits'),
 '1110207814332818580': ('leggings', 'Leggings'),
 '1110207814332818565': ('damen-outfits', 'Damen Gym Outfits'),
 '1110207814332820674': ('damen-shorts', 'Damen Shorts'),
 '1110207814332850044': ('damen-tops', 'Damen Tops & Sport-BHs'),
 '1110207814332971379': ('schuhe', 'Schuhe'),
 '1110207814332963572': ('schuhe', 'Schuhe'),
 '1110207814332816389': ('equipment', 'Gym Equipment'),
 '1110207814332963633': ('recovery', 'Recovery'),
}
emoji = re.compile('[\U0001F000-\U0001FAFF☀-➿️‍]+')
items = []
for f in sys.argv[1:]:
    items += json.load(open(f))['results'][0]['body']['items']
out, seen = [], set()
for p in sorted(items, key=lambda x: x['created_at'], reverse=True):
    m = re.search(r'/dp/([A-Z0-9]{10})', p.get('link') or '')
    if not m or 'amazon.de' not in p['link']:
        continue
    asin = m.group(1)
    if asin in seen:
        continue
    seen.add(asin)
    cat, catname = BOARDS.get(p['board_id'], ('sonstiges', 'Sonstiges'))
    title = emoji.sub('', p.get('title') or '').strip(' –-|')
    title = re.sub(r'\s{2,}', ' ', title)
    if not title:
        continue
    desc = (p.get('description') or '').split('Werbung')[0]
    desc = emoji.sub('', desc.split('#')[0]).strip()
    img = p['media']['images']['600x']['url']
    out.append({'asin': asin, 'title': title, 'desc': desc[:220], 'cat': cat, 'catname': catname,
                'img': img, 'url': f'https://www.amazon.de/dp/{asin}?tag=lilmedia-21'})
json.dump(out, open('data/products.json', 'w'), ensure_ascii=False, indent=1)
from collections import Counter
print(len(out), Counter(o['cat'] for o in out))
