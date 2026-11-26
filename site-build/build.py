# Builds the static Fit Essentials website (English) from data/catalog.json.
# Run from the repo root: python3 site-build/build.py
# legal-notice/ and privacy/ are hand-maintained static pages and are not generated here.
import html, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = '/fit-pins'
SITE = 'https://leonhaupt08-ui.github.io' + BASE
UPDATED = 'November 2026'

catalog = json.load(open(os.path.join(ROOT, 'data', 'catalog.json')))
HIDE = {'B0872L92RV'}  # duplicate of another Under Armour compression short
products = [p for p in catalog if p['asin'] not in HIDE]
by_asin = {p['asin']: p for p in products}

GROUPS = [
    ('women', 'Women', 'Matching sets, leggings, tops and shorts for training and everyday athleisure.', [
        ('w-sets', 'Sets & Outfits'), ('w-leggings', 'Leggings & Flares'),
        ('w-tops', 'Tops, Bras & Jackets'), ('w-bottoms', 'Shorts & Pants')]),
    ('men', 'Men', 'Clean gym basics: tees, tanks, long sleeves, shorts and joggers.', [
        ('m-tops', 'T-Shirts & Tanks'), ('m-long', 'Long Sleeves & Hoodies'),
        ('m-bottoms', 'Shorts & Joggers'), ('m-sets', 'Sets'), ('m-basics', 'Underwear')]),
    ('gear', 'Shoes & Accessories', 'Shoes, gym bags, bottles, shakers, caps, socks and running gear.', [
        ('shoes', 'Shoes'), ('accessories', 'Bags, Bottles & Accessories')]),
    ('home-gym', 'Home Gym & Recovery', 'Dumbbells, bands, training gear, recovery tools and supplements.', [
        ('equipment', 'Home Gym & Training Gear'), ('recovery', 'Recovery'), ('supplements', 'Supplements')]),
]
SUB = {k: n for _, _, _, subs in GROUPS for k, n in subs}
BEST = ['B0HB8Y3GLY', 'B0D9WJTBHR', 'B0FJ4NKKYM', 'B0BCGR2CP1', 'B0GKNDGC6G', 'B0B2DC5Y2Y', 'B0FJRKHXQP', 'B0GHZ3CXNB']
BEST_SET = set(BEST)
for p in products:
    assert p['cat'] in SUB, p

def esc(s):
    return html.escape(s, quote=True)

def group_items(g):
    subs = [k for gg, _, _, ss in GROUPS if gg == g for k, _ in ss]
    items = [p for p in products if p['cat'] in subs]
    return sorted(items, key=lambda p: (not p.get('new'), p['asin'] not in BEST_SET, subs.index(p['cat'])))

NEW = [p for p in products if p.get('new')]

def cover(g):
    pref = {'women': 'B0FJ4NKKYM', 'men': 'B0BCGR2CP1', 'gear': 'B0C46MDL41', 'home-gym': 'B0D1P694JJ'}[g]
    return by_asin[pref]['img'] if pref in by_asin else group_items(g)[0]['img']

SITEMAP = [SITE + '/legal-notice/', SITE + '/privacy/']

def write(path, doc):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, 'w').write(doc)

def page(path, title, desc, body, current='', image=None):
    url = SITE + path
    if path != '/404.html':
        SITEMAP.append(url)
    def nav(href, label, key):
        cur = ' aria-current="page"' if key == current else ''
        return f'<a href="{BASE}{href}"{cur}>{label}</a>'
    og = f'<meta property="og:image" content="{esc(image)}">' if image else ''
    doc = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website"><meta property="og:site_name" content="Fit Essentials">
<meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(desc)}"><meta property="og:url" content="{url}">{og}
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#0b0b0b">
<link rel="icon" href="{BASE}/assets/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="{BASE}/assets/style.css"></head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site"><div class="wrap"><a class="logo" href="{BASE}/"><b>FE</b>FIT ESSENTIALS</a>
<nav class="main" aria-label="Main">{nav('/products/women/', 'Women', 'women')}{nav('/products/men/', 'Men', 'men')}{nav('/products/', 'Shop', 'products')}{nav('/blog/', 'Guides', 'blog')}</nav></div></header>
<main id="main">{body}</main>
<footer class="site"><div class="wrap">
<div class="fcols">
<div><a class="logo" href="{BASE}/"><b>FE</b>FIT ESSENTIALS</a><p>Gym outfits, activewear and fitness finds for women and men.</p></div>
<div><h4>Shop</h4>{''.join(f'<a href="{BASE}/products/{g}/">{esc(n)}</a>' for g, n, _, _ in GROUPS)}</div>
<div><h4>Guides</h4><a href="{BASE}/blog/">All guides</a><a href="{BASE}/blog/gift-ideas-for-him-gym/">Gifts for him</a><a href="{BASE}/blog/gift-ideas-for-her-gym/">Gifts for her</a><a href="{BASE}/blog/home-gym-essentials/">Home gym</a></div>
<div><h4>Follow</h4><a href="https://www.pinterest.com/Lildesports/">Pinterest</a><a href="https://www.instagram.com/fit.finds.de">Instagram</a></div>
</div>
<p class="disc"><strong>Affiliate disclosure:</strong> Links marked with * are affiliate links. As an Amazon Associate I earn from qualifying purchases. The price stays the same for you.</p>
<p class="legal"><a href="{BASE}/legal-notice/">Legal Notice (Impressum)</a><a href="{BASE}/privacy/">Privacy Policy</a><span>© 2026 Fit Essentials</span></p>
</div></footer>
</body></html>
'''
    write('index.html' if path == '/' else ('404.html' if path == '/404.html' else path.strip('/') + '/index.html'), doc)

def card(p):
    badge = '<span class="badge">New</span>' if p.get('new') else ('<span class="badge">Best seller</span>' if p['asin'] in BEST_SET else '')
    return f'''<div class="card" data-cat="{p['cat']}"><div class="ph">{badge}<img src="{esc(p['img'])}" alt="{esc(p['title'])}" loading="lazy" width="300" height="400"></div>
<div class="body"><div class="c">{esc(SUB[p['cat']])}</div><h3>{esc(p['title'])}</h3>
<a class="btn" href="{esc(p['url'])}" rel="nofollow sponsored noopener" target="_blank">View on Amazon*</a></div></div>'''

def pbox(asin, note):
    p = by_asin[asin]
    return f'''<div class="pbox"><img src="{esc(p['img'])}" alt="{esc(p['title'])}" loading="lazy" width="120" height="160"><div>
<div class="c">{esc(SUB[p['cat']])}</div><h3>{esc(p['title'])}</h3><p>{esc(note)}</p>
<a class="btn" href="{esc(p['url'])}" rel="nofollow sponsored noopener" target="_blank">View on Amazon*</a></div></div>'''

# ---------- guides ----------
POSTS_META = [
    ('gift-ideas-for-him-gym', 'Christmas Gift Ideas for Him: 10 Gym Gifts Men Actually Use', 'Gym gift ideas for boyfriends, brothers and dads who train – clothes, shoes and home gym gear.'),
    ('gift-ideas-for-her-gym', 'Christmas Gift Ideas for Her: 10 Gym Gifts She Will Love', 'Gift ideas for gym girls – matching sets, leggings, bottles and recovery tools.'),
    ('all-black-gym-outfit-men', 'All Black Gym Outfit for Men: The Easiest Look in the Gym', 'How to build an all black gym outfit for men – compression shirt, shorts or baggy pants and black sneakers.'),
    ('home-gym-essentials', 'Home Gym Essentials: What You Really Need to Start', 'Build a small home gym step by step – dumbbells, a cable machine, bands and a mat.'),
    ('gym-gift-ideas', 'Gym Gift Ideas: 10 Presents Every Fitness Lover Will Use', 'Practical gift ideas for people who love the gym – from recovery tools to the perfect gym bag.'),
    ('gym-outfit-ideas-for-women', 'Gym Outfit Ideas for Women: 4 Looks That Always Work', 'Matching sets, all black, shorts or gym-to-street: four easy gym outfit ideas for women.'),
    ('gym-outfit-for-men', 'Gym Outfits for Men: Clean, Simple, No Overthinking', 'How to build a simple gym wardrobe as a man – basics, colors and fits.'),
    ('how-to-choose-gym-leggings', 'Gym Leggings: What to Look for Before You Buy', 'High waist, squat proof, pockets: how to find leggings that stay put during training.'),
    ('gym-bag-checklist', 'What to Pack in Your Gym Bag: The Complete Checklist', 'Everything that belongs in your gym bag, from water bottle to headphones.'),
]
META = {s: (t, d) for s, t, d in POSTS_META}

def post(slug, minutes, intro, sections):
    title, desc = META[slug]
    first = None
    parts = [f'<p class="intro">{intro}</p>']
    for h, text, picks in sections:
        parts.append(f'<h2>{esc(h)}</h2>')
        if text:
            parts.append(text)
        for a, note in picks:
            assert a in by_asin, a
            first = first or by_asin[a]['img']
            parts.append(pbox(a, note))
    others = [x for x in POSTS_META if x[0] != slug][:2]
    related = ''.join(f'<a class="post-card" href="{BASE}/blog/{s}/"><span class="eyebrow">Guide</span><h3>{esc(t)}</h3><p>{esc(d)}</p></a>' for s, t, d in others)
    page(f'/blog/{slug}/', f'{title} | Fit Essentials', desc,
         f'''<article><nav class="crumbs" aria-label="Breadcrumb"><a href="{BASE}/">Home</a> / <a href="{BASE}/blog/">Guides</a></nav>
<h1>{esc(title)}</h1><p class="meta">Updated {UPDATED} · {minutes} min read</p>
<p class="note">This guide contains affiliate links (*). The products are a curated selection, not tested reviews.</p>
{''.join(parts)}
<div class="endcta"><a class="btn" href="{BASE}/products/">Browse all products</a></div></article>
<section class="related"><div class="wrap"><h2>More guides</h2><div class="posts">{related}</div></div></section>''',
         current='blog', image=first)

post('gym-gift-ideas', 4,
     'Looking for a present for someone who never misses a workout? These gifts are useful in everyday training – no gimmicks, just things that get used.',
     [('For recovery days', '', [
         ('B0127BIK1U', 'Small enough for any bag – great for shoulders, glutes and feet after training.'),
         ('B003BP5AGA', 'A classic foam roller for rolling out legs and back on rest days.')]),
      ('For the gym bag', '', [
         ('B07P8R34H7', 'Separate shoe compartment keeps sweaty sneakers away from clean clothes.'),
         ('B0DS94YFTC', "Stainless steel shaker that does not keep the smell of last week's protein."),
         ('B0CNTWY3VM', 'The tumbler everyone carries around – a safe pick for gym girls.')]),
      ('For runners', '', [
         ('B0HN7WY9WS', 'Open-ear headphones so you still hear traffic while running.'),
         ('B07WH7JH6W', 'Holds phone and keys without bouncing.')]),
      ('For lifting and home workouts', '', [
         ('B0CKK4VG26', 'Popular with lifters for squat and leg days.'),
         ('B0D1P694JJ', 'One adjustable dumbbell instead of a whole rack – ideal for small home gyms.'),
         ('B0FNX3X992', 'A thick mat for stretching, core work and yoga at home.')])])

post('gym-outfit-ideas-for-women', 3,
     'A good gym outfit does not have to be complicated. These four looks work for training and on the way there.',
     [('1. The matching set', '<p>Top and leggings in the same color instantly look put together. Dark grey, black and brown are the easiest to style.</p>', [
         ('B0FJ4NKKYM', 'Cropped zip jacket, sports bra and leggings in one set.'),
         ('B0F6CVXKR5', 'Charcoal set with shorts – great for warmer gyms.')]),
      ('2. All black', '<p>Black leggings, a black top, white socks and white sneakers – the classic that never goes wrong.</p>', [
         ('B0FJRKHXQP', 'Racerback top and high waist leggings – sleek from gym to street.')]),
      ('3. Shorts instead of leggings', '<p>For cardio and warm days: high waisted shorts with a sports bra or crop top.</p>', [
         ('B0GKNDGC6G', 'Biker-style shorts that stay in place.'),
         ('B0GF8CKZ5N', 'Simple black sports bra that goes with every pair of shorts.')]),
      ('4. Gym to street', '<p>Throw a fitted jacket over your set and you are ready for the way home.</p>', [
         ('B0CL1YFTZB', 'Fitted zip-up jacket with thumb holes.')])])

post('gym-outfit-for-men', 3,
     'Most good gym outfits for men are built from a few basics in black, grey and white. That way everything goes with everything.',
     [('The basics', '<ul><li>2–3 fitted or regular training shirts</li><li>Shorts or joggers</li><li>A hoodie or zip jacket for the way there</li><li>Simple sneakers and sports socks</li></ul>', []),
      ('Start with a full set', '<p>The easiest way to look put together is a set that already matches.</p>', [
         ('B0BCGR2CP1', 'Hoodie, compression tee, long sleeve, shorts and leggings in black.')]),
      ('Tops', '<p>Compression shirts fit tight, regular training shirts sit looser. Keep the colors neutral.</p>', [
         ('B0GHZ3CXNB', 'Black, white and grey – three tees that cover the whole week.'),
         ('B0B2DC5Y2Y', 'Ribbed long sleeve that works in the gym and for going out.')]),
      ('Bottoms', '<p>Baggy sweatpants are the streetwear classic for before and after training.</p>', [
         ('B0HB8Y3GLY', 'Wide-leg grey sweatpants – pair with a white tee.'),
         ('B0H3KL31X9', 'The same relaxed fit in black.')])])

post('how-to-choose-gym-leggings', 4,
     'Leggings are the part of your gym outfit that has to handle the most: squats, lunges, cardio. Before you buy, check these four things.',
     [('1. Squat proof', '<p>Stretch the fabric in front of a light or do a deep squat in front of a mirror. Thicker, matte fabrics are usually more opaque than thin, shiny ones.</p>', [
         ('B0D9WJTBHR', 'Seamless, matte and one of the most saved leggings on our Pinterest.')]),
      ('2. High waist', '<p>A high waistband stays in place better when you move and is easy to pair with crop tops and sports bras.</p>', [
         ('B0F9FXN2PF', 'High waist, simple and easy to combine.')]),
      ('3. Seams and shape', '<p>Seamless leggings have hardly any seams and chafe less. Scrunch styles shape the look but are a matter of taste.</p>', [
         ('B0CDFP7M3T', 'Scrunch detail at the back for a sculpted look.')]),
      ('4. Pockets', '<p>Side pockets for your phone are more useful for running and the gym than you might think.</p>', [
         ('B0D6B1PGNH', 'Black high waist leggings with side pockets.')])])

post('gym-bag-checklist', 3,
     'Nothing is more annoying than realizing at the gym that something is missing. With this list you are ready in two minutes.',
     [('Always', '<ul><li>Water bottle or shaker</li><li>Towel</li><li>Headphones</li><li>Spare shirt and socks</li><li>Lock for the locker</li></ul>', [
         ('B0DS94YFTC', 'Stainless steel shaker for water or protein.'),
         ('B0HN7WY9WS', 'Open-ear headphones for training and running.')]),
      ('Depending on your workout', '<ul><li>Lifting straps or gloves for heavy pulls</li><li>Resistance bands for warming up</li><li>Weightlifting shoes for squats</li></ul>', [
         ('B01F2OGJQM', 'Padded straps for deadlifts and rows.'),
         ('B0D1DV9NHZ', 'Bands for warm-ups and home workouts.')]),
      ('The bag itself', '<p>A separate shoe compartment is the feature you will appreciate every day.</p>', [
         ('B07P8R34H7', 'Duffel bag with shoe compartment and wet pocket.')])])

post('gift-ideas-for-him-gym', 4,
     'Shopping for a guy who lives in the gym? These gifts get used every week – from clean basics to gear for training at home.',
     [('Clothes he will wear every day', '', [
         ('B0874X72WP', 'The classic black compression shirt – fits close for lifting and running.'),
         ('B0H36333FW', 'Wide leg grey sweatpants with zip pockets – the cozy streetwear favorite.'),
         ('B0GPVM1CVP', 'Washed black sweatpants for a vintage look after training.')]),
      ('Sneakers', '', [
         ('B077MQ6C7S', 'Clean white sneakers that go with joggers, shorts and jeans.'),
         ('B07S8PT36G', 'Light all black sneakers for the gym and everyday wear.')]),
      ('For his home gym', '', [
         ('B0HBPGRX4G', 'A compact digital cable machine with handles and ankle strap.'),
         ('B06X95DP1K', 'Cast iron plates with two dumbbell bars and an EZ curl bar.')]),
      ('Small gifts and stocking fillers', '', [
         ('B0DS94YFTC', 'A stainless steel shaker that does not keep the smell.'),
         ('B01F2OGJQM', 'Padded lifting straps for heavy pulls.'),
         ('B0127BIK1U', 'A massage ball for tight shoulders after training.')])])

post('gift-ideas-for-her-gym', 4,
     'For the girl who never skips leg day: these gifts look good, feel good and actually get used in the gym.',
     [('Matching sets', '<p>A matching set is the gift that always works – pick a neutral color if you are unsure.</p>', [
         ('B0FJ4NKKYM', 'Cropped zip jacket, sports bra and leggings in dark grey.'),
         ('B0FJRKHXQP', 'Black racerback top and high waist leggings.')]),
      ('Leggings', '', [
         ('B0D9WJTBHR', 'Seamless, matte leggings – one of the most saved on our Pinterest.'),
         ('B0G6YGJBWB', 'Black flared leggings for yoga, pilates and everyday outfits.')]),
      ('For the gym bag', '', [
         ('B0CNTWY3VM', 'The tumbler every gym girl carries around.'),
         ('B0FD2J6MF7', 'White backpack with a separate shoe compartment.')]),
      ('Recovery and cozy days', '', [
         ('B0DDQ11QGJ', 'Soft grey lounge set for rest days.'),
         ('B0127BIK1U', 'Massage ball for glutes, shoulders and feet.'),
         ('B003BP5AGA', 'A classic foam roller for legs and back.')])])

post('all-black-gym-outfit-men', 3,
     'All black is the easiest gym outfit there is: everything matches, sweat shows less and it looks clean from the gym to the street.',
     [('1. The top', '<p>Choose between a compression shirt, a tank top or a regular tee. All three work in black.</p>', [
         ('B0874X72WP', 'Short sleeve compression shirt that fits close to the body.'),
         ('B0G3WM2CGJ', 'Ribbed tank top for arm day and warm gyms.'),
         ('B0C5D5N75W', 'A multipack of plain black tees for the whole week.')]),
      ('2. Shorts or pants', '<p>Shorts for leg day and cardio, baggy pants for the old-school look.</p>', [
         ('B0714D4Q4B', 'Training shorts with the big side logo.'),
         ('B075GQLGGG', 'Baggy bodybuilding pants with a tapered leg.')]),
      ('3. The shoes', '<p>Black sneakers keep the look clean – white ones add contrast.</p>', [
         ('B07S8PT36G', 'Light mesh sneakers in all black.')])])

post('home-gym-essentials', 4,
     'You do not need a full garage gym to train at home. Start with a few pieces that cover strength, cardio and mobility – and add more later.',
     [('1. Weights', '<p>Plate-loaded dumbbells are the cheapest way to get lots of weight options.</p>', [
         ('B06X95DP1K', 'Cast iron plates with dumbbell bars and an EZ curl bar.'),
         ('B0D1P694JJ', 'One adjustable dumbbell instead of a whole rack.')]),
      ('2. Cable training', '<p>Cable exercises are hard to copy at home – a compact cable machine fills that gap.</p>', [
         ('B0HBPGRX4G', 'Portable digital cable machine with handles and ankle strap.')]),
      ('3. Bands and bodyweight', '', [
         ('B0D1DV9NHZ', 'Resistance bands for warm-ups and full workouts.'),
         ('B0DNTWJJV2', 'Pull-up bar for the door frame, no drilling needed.')]),
      ('4. Mat and recovery', '', [
         ('B0FNX3X992', 'A thick mat for core work and stretching.'),
         ('B003BP5AGA', 'Foam roller for rest days.')])])

# ---------- guides index ----------
page('/blog/', 'Guides | Fit Essentials', 'Gym outfit ideas, buying guides and gift ideas from Fit Essentials.',
     '<section class="phead"><div class="wrap"><div class="eyebrow">Guides</div><h1>Outfit ideas &amp; buying guides</h1><p class="lead">Short, practical guides that help you pick the right gym clothes and gear.</p></div></section>'
     '<section class="tight"><div class="wrap"><div class="posts">'
     + ''.join(f'<a class="post-card" href="{BASE}/blog/{s}/"><span class="eyebrow">Guide</span><h3>{esc(t)}</h3><p>{esc(d)}</p></a>' for s, t, d in POSTS_META)
     + '</div></div></section>', current='blog')

# ---------- shop pages ----------
script = '''<script>
(function(){var bs=document.querySelectorAll('.filters button'),cs=document.querySelectorAll('.grid .card'),n=document.getElementById('count');
function apply(f){var v=0;bs.forEach(function(b){b.setAttribute('aria-pressed',b.dataset.f===f)});
cs.forEach(function(c){var on=f==='all'||c.dataset.cat===f;c.classList.toggle('hidden',!on);if(on)v++});if(n)n.textContent=v;}
bs.forEach(function(b){b.addEventListener('click',function(){apply(b.dataset.f);history.replaceState(null,'',b.dataset.f==='all'?location.pathname:'#'+b.dataset.f)})});
var h=location.hash.slice(1);if(h&&document.querySelector('[data-f="'+h+'"]'))apply(h);})();
</script>'''
for g, name, desc, subs in GROUPS:
    items = group_items(g)
    chips = '<button type="button" data-f="all" aria-pressed="true">All</button>' + ''.join(
        f'<button type="button" data-f="{k}" aria-pressed="false">{esc(n)} <span>{sum(p["cat"] == k for p in items)}</span></button>' for k, n in subs)
    page(f'/products/{g}/', f'{name} | Fit Essentials', f'{name}: {desc}',
         f'''<section class="phead"><div class="wrap"><nav class="crumbs" aria-label="Breadcrumb"><a href="{BASE}/">Home</a> / <a href="{BASE}/products/">Shop</a></nav>
<h1>{esc(name)}</h1><p class="lead">{esc(desc)}</p></div></section>
<section class="tight"><div class="wrap"><div class="filters" role="group" aria-label="Filter by category">{chips}</div>
<p class="count"><span id="count">{len(items)}</span> products</p><div class="grid">{''.join(card(p) for p in items)}</div></div></section>{script}''',
         current=g if g in ('women', 'men') else 'products', image=cover(g))

tiles = ''.join(f'''<a class="tile" href="{BASE}/products/{g}/"><img src="{esc(cover(g))}" alt="" loading="lazy" width="400" height="500">
<span><strong>{esc(n)}</strong><em>{len(group_items(g))} products</em></span></a>''' for g, n, _, _ in GROUPS)
page('/products/', 'Shop | Fit Essentials', 'Shop gym outfits for women and men, shoes, accessories, home gym equipment and recovery tools.',
     f'''<section class="phead"><div class="wrap"><div class="eyebrow">Shop</div><h1>Shop by category</h1><p class="lead">{len(products)} handpicked products. Pick a category to start.</p></div></section>
<section class="tight"><div class="wrap"><div class="tiles">{tiles}</div></div></section>
<section><div class="wrap"><div class="section-head"><h2>Best sellers</h2></div><div class="grid">{''.join(card(by_asin[a]) for a in BEST)}</div></div></section>''',
     current='products', image=cover('women'))

# ---------- home ----------
collage = ''.join(f'<img src="{esc(by_asin[a]["img"])}" alt="{esc(by_asin[a]["title"])}" width="300" height="400">' for a in ['B0FJ4NKKYM', 'B0HB8Y3GLY', 'B0D9WJTBHR', 'B0BCGR2CP1'])
page('/', 'Fit Essentials | Gym Outfits & Fitness Finds',
     'Gym outfits for women and men, leggings, activewear and gym essentials – outfit ideas and buying guides from Fit Essentials.',
     f'''<section class="hero"><div class="wrap hero-grid"><div><div class="eyebrow">Fit Essentials</div>
<h1>Gym outfits &amp; fitness finds</h1><p class="lead">Activewear, outfit ideas and gym essentials for women and men – handpicked, so you don't have to search for hours.</p>
<div class="btns"><a class="btn" href="{BASE}/products/women/">Shop women</a><a class="btn" href="{BASE}/products/men/">Shop men</a><a class="btn ghost" href="{BASE}/blog/">Read the guides</a></div></div>
<div class="collage">{collage}</div></div></section>
<section><div class="wrap"><div class="section-head"><h2>Shop by category</h2><a href="{BASE}/products/">View shop →</a></div><div class="tiles">{tiles}</div></div></section>
<section class="tight"><div class="wrap"><div class="banners"><a class="banner" href="{BASE}/blog/gift-ideas-for-him-gym/"><span class="eyebrow">Christmas gift guide</span><strong>Gym gifts for him</strong><span class="arrow">See the ideas →</span></a><a class="banner" href="{BASE}/blog/gift-ideas-for-her-gym/"><span class="eyebrow">Christmas gift guide</span><strong>Gym gifts for her</strong><span class="arrow">See the ideas →</span></a></div></div></section>
<section><div class="wrap"><div class="section-head"><h2>New in</h2><a href="{BASE}/products/men/">Shop men →</a></div><div class="grid">{''.join(card(p) for p in NEW[:8])}</div></div></section>
<section><div class="wrap"><div class="section-head"><h2>Best sellers</h2><a href="{BASE}/products/">See all →</a></div><div class="grid">{''.join(card(by_asin[a]) for a in BEST)}</div></div></section>
<section class="tight"><div class="wrap"><div class="section-head"><h2>Latest guides</h2><a href="{BASE}/blog/">All guides →</a></div>
<div class="posts">{''.join(f'<a class="post-card" href="{BASE}/blog/{s}/"><span class="eyebrow">Guide</span><h3>{esc(t)}</h3><p>{esc(d)}</p></a>' for s, t, d in POSTS_META[:3])}</div></div></section>''',
     image=by_asin['B0FJ4NKKYM']['img'])

page('/404.html', 'Page not found | Fit Essentials', 'Page not found.',
     f'<section class="phead"><div class="wrap"><div class="eyebrow">404</div><h1>Page not found</h1><p class="lead">This page does not exist (anymore).</p><div class="btns"><a class="btn" href="{BASE}/products/">Go to the shop</a><a class="btn ghost" href="{BASE}/">Home</a></div></div></section>')

# ---------- sitemap / robots ----------
write('sitemap.xml', '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
      + ''.join(f'  <url><loc>{u}</loc></url>\n' for u in SITEMAP) + '</urlset>\n')
write('robots.txt', f'User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n')

print('built', len(products), 'products,', len(POSTS_META), 'guides,', len(SITEMAP), 'pages')
