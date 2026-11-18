# Generates the static Fit Essentials website (English) from data/products.json.
# Run from the repo root: python3 site-build/build.py
import html, json, os, re, shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = '/fit-pins'
products = json.load(open(os.path.join(ROOT, 'data', 'products.json')))

# Titles with hype or health promises are cut back to the product name.
HYPE = re.compile(r'\s*[–|-]\s*[^–|-]*!\s*$')
BANNED = re.compile(r'lose|burn|fat|abnehm|heil|cure', re.I)
TITLES = json.load(open(os.path.join(ROOT, 'data', 'titles_en.json')))
for p in products:
    t = TITLES.get(p['asin']) or HYPE.sub('', p['title']).strip()
    if BANNED.search(t):
        t = re.split(r'\s[–|-]\s', t)[0]
    p['title'] = t

CATS = [
    ('damen-outfits', "Women's Gym Outfits"),
    ('leggings', 'Leggings'),
    ('damen-tops', "Women's Tops & Sports Bras"),
    ('damen-shorts', "Women's Shorts"),
    ('herren-outfits', "Men's Gym Outfits"),
    ('schuhe', 'Shoes'),
    ('equipment', 'Gym Equipment'),
    ('recovery', 'Recovery'),
]
CATNAME = dict(CATS)
for p in products:
    p['catname'] = CATNAME.get(p['cat'], 'Other')
CATS = [(k, n) for k, n in CATS if any(p['cat'] == k for p in products)]
by_asin = {p['asin']: p for p in products}

# Old German URLs are removed so only the English site is served.
for old in ('produkte', 'impressum', 'blog'):
    shutil.rmtree(os.path.join(ROOT, old), ignore_errors=True)

def esc(s):
    return html.escape(s, quote=True)

def page(path, title, desc, body, current=''):
    def nav(href, label, key):
        cur = ' aria-current="page"' if key == current else ''
        return f'<a href="{BASE}{href}"{cur}>{label}</a>'
    doc = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title><meta name="description" content="{esc(desc)}">
<link rel="stylesheet" href="{BASE}/assets/style.css"></head>
<body>
<header class="site"><div class="wrap"><a class="logo" href="{BASE}/"><b>FE</b>FIT ESSENTIALS</a>
<nav class="main">{nav('/products/', 'Products', 'products')}{nav('/blog/', 'Blog', 'blog')}</nav></div></header>
<main>{body}</main>
<footer class="site"><div class="wrap">
<p><strong>Advertising / affiliate links:</strong> Links to Amazon are affiliate links (marked with *). As an Amazon Associate I earn from qualifying purchases. The price stays the same for you.</p>
<nav><a href="https://www.instagram.com/fit.finds.de">Instagram</a><a href="https://www.pinterest.com/Lildesports/">Pinterest</a><a href="{BASE}/legal-notice/">Legal Notice (Impressum)</a><a href="{BASE}/privacy/">Privacy Policy</a></nav>
<p>© 2026 Fit Essentials</p></div></footer>
</body></html>
'''
    full = os.path.join(ROOT, path.strip('/'), 'index.html') if path != '/' else os.path.join(ROOT, 'index.html')
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, 'w').write(doc)

def card(p):
    return f'''<div class="card" data-cat="{p['cat']}"><div class="ph"><img src="{esc(p['img'])}" alt="{esc(p['title'])}" loading="lazy"></div>
<div class="body"><div class="c">{esc(p['catname'])}</div><h3>{esc(p['title'])}</h3>
<a class="btn" href="{esc(p['url'])}" rel="nofollow sponsored noopener" target="_blank">View on Amazon*</a></div></div>'''

def pbox(asin):
    p = by_asin.get(asin)
    if not p:
        return ''
    return f'''<div class="pbox"><img src="{esc(p['img'])}" alt="{esc(p['title'])}" loading="lazy"><div><h3>{esc(p['title'])}</h3>
<a class="btn" href="{esc(p['url'])}" rel="nofollow sponsored noopener" target="_blank">View on Amazon*</a></div></div>'''

def pick(cat, n, skip=()):
    return [p['asin'] for p in products if p['cat'] == cat and p['asin'] not in skip][:n]

# ---------- blog posts ----------
POSTS = []

def post(slug, title, desc, body_html):
    POSTS.append((slug, title, desc))
    page(f'/blog/{slug}/', f'{title} | Fit Essentials', desc,
         f'<article><div class="eyebrow">Guide</div><h1>{esc(title)}</h1>'
         f'<p class="note">This article contains affiliate links (advertising). The products are a curated selection, not test reports.</p>'
         f'{body_html}<p style="margin-top:40px"><a class="btn ghost" href="{BASE}/products/">See all products</a></p></article>',
         current='blog')

leg = ['B0D9WJTBHR'] + pick('leggings', 3, skip=('B0D9WJTBHR',))
post('how-to-choose-gym-leggings', 'Gym Leggings: What to Look for Before You Buy',
     'High waist, squat proof, with pockets: how to find gym leggings that stay in place during training – plus a selection of popular styles.',
     f'''<p>Leggings are the part of your gym outfit that has to handle the most: squats, lunges, cardio. Before you buy, check these four things.</p>
<h2>1. Squat proof</h2><p>Stretch the fabric in front of a light or do a deep squat in front of a mirror. Thicker, matte fabrics are usually more opaque than thin, shiny ones.</p>
<h2>2. High waist</h2><p>A high waistband stays in place better when you move and is easy to pair with crop tops and sports bras.</p>
<h2>3. Seams and fit</h2><p>Seamless leggings have hardly any seams and chafe less. Scrunch styles shape the look but are a matter of taste.</p>
<h2>4. Pockets</h2><p>Side pockets for your phone are more useful for running and the gym than you might think.</p>
<h2>Popular styles</h2>{''.join(pbox(a) for a in leg)}''')

wo = ['B0FJ4NKKYM', 'B0FJRKHXQP'] + pick('damen-outfits', 2, skip=('B0FJ4NKKYM', 'B0FJRKHXQP'))
post('gym-outfit-ideas-for-women', 'Gym Outfit Ideas for Women: 4 Looks That Always Work',
     'Matching sets, all black or sporty casual: four easy gym outfit ideas for women to recreate.',
     f'''<p>A good gym outfit doesn't have to be complicated. These four looks work for training and on the way there.</p>
<h2>1. The matching set</h2><p>Top and leggings in the same color instantly look put together. Dark grey, black and brown are easy to combine.</p>
<h2>2. All black</h2><p>Black leggings, black top, white socks and white sneakers – the classic that never goes wrong.</p>
<h2>3. Shorts instead of leggings</h2><p>For cardio and warm days: high waisted shorts with a sports bra or crop top.</p>
<h2>4. Gym to street</h2><p>Throw a zip jacket or an oversized hoodie over your set and you're ready for the way home.</p>
<h2>Sets and outfits to shop</h2>{''.join(pbox(a) for a in wo)}{pbox('B0GKNDGC6G')}''')

mo = ['B0HB8Y3GLY', 'B0BCGR2CP1', 'B0B2DC5Y2Y', 'B0GHZ3CXNB', 'B0H3KL31X9']
post('gym-outfit-for-men', "Gym Outfits for Men: Clean, Simple, No Overthinking",
     'How to put together a simple gym outfit as a man: basics, colors and combinations – with product picks.',
     f'''<p>Most good gym outfits for men are built from a few basics in black, grey and white. That way everything goes with everything.</p>
<h2>The basics</h2><ul><li>2–3 fitted or regular training shirts</li><li>Shorts or joggers</li><li>A hoodie or zip jacket for the way there</li><li>Simple sneakers and sports socks</li></ul>
<h2>Colors</h2><p>Stick to black, grey and white. An all black outfit always looks clean, and grey sweatpants with a white tee are the streetwear classic.</p>
<h2>Fit</h2><p>Compression shirts fit tight, regular training shirts sit looser. Baggy sweatpants are great for everyday wear after training.</p>
<h2>Products to shop</h2>{''.join(pbox(a) for a in mo)}''')

eq = pick('equipment', 5)
post('gym-bag-checklist', 'What to Pack in Your Gym Bag: The Complete Checklist',
     'What belongs in your gym bag? A simple checklist from water bottle to towel – plus useful products.',
     f'''<p>Nothing is more annoying than realizing at the gym that something is missing. With this list you're ready in two minutes.</p>
<h2>Always</h2><ul><li>Water bottle or shaker</li><li>Towel</li><li>Headphones</li><li>Spare shirt and socks</li><li>Lock for the locker</li></ul>
<h2>Depending on your workout</h2><ul><li>Lifting straps or gloves for heavy pulls</li><li>Resistance bands for warming up</li><li>Weightlifting shoes for squats</li></ul>
<h2>After training</h2><ul><li>Shower gel and deodorant</li><li>Bag for wet clothes</li></ul>
<h2>Useful products</h2>{''.join(pbox(a) for a in eq)}''')

# ---------- blog index ----------
page('/blog/', 'Blog | Fit Essentials', 'Guides to gym outfits, leggings and training essentials.',
     '<section><div class="wrap"><div class="eyebrow">Blog</div><h1>Guides</h1><p class="lead">Outfit ideas and buying guides for your training.</p></div></section>'
     '<section style="padding-top:0"><div class="wrap"><div class="posts">'
     + ''.join(f'<a class="post-card" href="{BASE}/blog/{s}/"><h3>{esc(t)}</h3><p>{esc(d)}</p></a>' for s, t, d in POSTS)
     + '</div></div></section>', current='blog')

# ---------- products ----------
filters = '<button type="button" data-f="all" aria-pressed="true">All</button>' + ''.join(
    f'<button type="button" data-f="{k}" aria-pressed="false">{esc(n)}</button>' for k, n in CATS)
script = '''<script>
(function(){var bs=document.querySelectorAll('.filters button'),cs=document.querySelectorAll('.grid .card');
function apply(f){bs.forEach(function(b){b.setAttribute('aria-pressed',b.dataset.f===f)});
cs.forEach(function(c){c.classList.toggle('hidden',f!=='all'&&c.dataset.cat!==f)});}
bs.forEach(function(b){b.addEventListener('click',function(){apply(b.dataset.f);history.replaceState(null,'',b.dataset.f==='all'?location.pathname:'#'+b.dataset.f)})});
var h=location.hash.slice(1);if(h&&document.querySelector('[data-f="'+h+'"]'))apply(h);})();
</script>'''
page('/products/', 'All Products | Fit Essentials',
     "Gym outfits for women and men, leggings, shoes and gym equipment – all Fit Essentials favorites in one place.",
     f'<section><div class="wrap"><div class="eyebrow">Shop the look</div><h1>All Products</h1><p class="lead">{len(products)} favorites from gym fashion and equipment. Filter by category.</p></div></section>'
     f'<section style="padding-top:0"><div class="wrap"><div class="filters">{filters}</div><div class="grid">'
     + ''.join(card(p) for p in products) + f'</div></div></section>{script}', current='products')

# ---------- home ----------
TOP = ['B0HB8Y3GLY', 'B0D9WJTBHR', 'B0FJ4NKKYM', 'B0BCGR2CP1', 'B0GKNDGC6G', 'B0B2DC5Y2Y', 'B0FJRKHXQP', 'B0GHZ3CXNB']
featured = [by_asin[a] for a in TOP if a in by_asin][:8]
cats_html = ''.join(f'<a class="cat" href="{BASE}/products/#{k}">{esc(n)}<span>{sum(p["cat"] == k for p in products)}</span></a>' for k, n in CATS)
page('/', 'Fit Essentials | Gym Outfits & Fitness Finds',
     'Gym outfits for women and men, leggings, activewear and gym equipment – outfit ideas and guides from Fit Essentials.',
     f'''<section class="hero"><div class="wrap"><div class="eyebrow">Fit Essentials</div>
<h1>Gym Outfits &amp;<br>Fitness Finds</h1><p class="lead">Activewear, outfit ideas and gym essentials for women and men – handpicked so you don't have to search for hours.</p>
<div class="btns"><a class="btn" href="{BASE}/products/">Shop products</a><a class="btn ghost" href="{BASE}/blog/">Read the guides</a></div></div></section>
<section><div class="wrap"><div class="section-head"><h2>Categories</h2></div><div class="cats">{cats_html}</div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="section-head"><h2>Popular Outfits</h2><a href="{BASE}/products/">See all →</a></div>
<div class="grid">{''.join(card(p) for p in featured)}</div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="section-head"><h2>From the Blog</h2><a href="{BASE}/blog/">All articles →</a></div>
<div class="posts">{''.join(f'<a class="post-card" href="{BASE}/blog/{s}/"><h3>{esc(t)}</h3><p>{esc(d)}</p></a>' for s, t, d in POSTS[:3])}</div></div></section>''')

# ---------- legal notice (German Impressum, required by § 5 DDG) ----------
page('/legal-notice/', 'Legal Notice (Impressum) | Fit Essentials', 'Legal notice',
     '''<article><h1>Legal Notice (Impressum)</h1><p>Information according to § 5 DDG (German Digital Services Act)</p>
<p>Leon Haupt<br>Hohlweiler 44<br>91443 Scheinfeld<br>Germany</p>
<p>Email: <a href="mailto:leon.haupt08@gmail.com">leon.haupt08@gmail.com</a></p>
<p>Responsible for the content: Leon Haupt, address as above.</p>
<h2>Affiliate links</h2><p>This website contains affiliate links. As an Amazon Associate I earn from qualifying purchases.</p></article>''')

print('built', len(products), 'products,', len(POSTS), 'posts')
