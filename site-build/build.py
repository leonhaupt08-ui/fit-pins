# Generates the static Fit Essentials website from data/products.json.
# Run from the repo root: python3 site-build/build.py
import html, json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = '/fit-pins'
products = json.load(open(os.path.join(ROOT, 'data', 'products.json')))

# Titles with hype or health promises are cut back to the product name.
HYPE = re.compile(r'\s*[–|-]\s*[^–|-]*!\s*$')
BANNED = re.compile(r'lose|burn|fat|abnehm|heil|cure', re.I)
for p in products:
    t = HYPE.sub('', p['title']).strip()
    if BANNED.search(t):
        t = re.split(r'\s[–|-]\s', t)[0]
    p['title'] = t

CATS = [
    ('damen-outfits', 'Damen Gym Outfits'),
    ('leggings', 'Leggings'),
    ('damen-tops', 'Damen Tops & Sport-BHs'),
    ('damen-shorts', 'Damen Shorts'),
    ('herren-outfits', 'Herren Gym Outfits'),
    ('schuhe', 'Schuhe'),
    ('equipment', 'Gym Equipment'),
    ('recovery', 'Recovery'),
]
CATS = [(k, n) for k, n in CATS if any(p['cat'] == k for p in products)]
by_asin = {p['asin']: p for p in products}

def esc(s):
    return html.escape(s, quote=True)

def page(path, title, desc, body, current=''):
    def nav(href, label, key):
        cur = ' aria-current="page"' if key == current else ''
        return f'<a href="{BASE}{href}"{cur}>{label}</a>'
    doc = f'''<!doctype html>
<html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title><meta name="description" content="{esc(desc)}">
<link rel="stylesheet" href="{BASE}/assets/style.css"></head>
<body>
<header class="site"><div class="wrap"><a class="logo" href="{BASE}/"><b>FE</b>FIT ESSENTIALS</a>
<nav class="main">{nav('/produkte/', 'Produkte', 'produkte')}{nav('/blog/', 'Blog', 'blog')}</nav></div></header>
<main>{body}</main>
<footer class="site"><div class="wrap">
<p><strong>Werbung / Affiliate-Links:</strong> Links zu Amazon sind Affiliate-Links (mit * gekennzeichnet). Als Amazon-Partner verdiene ich an qualifizierten Verkäufen. Für dich ändert sich der Preis nicht.</p>
<nav><a href="https://www.instagram.com/fit.finds.de">Instagram</a><a href="https://www.pinterest.com/Lildesports/">Pinterest</a><a href="{BASE}/impressum/">Impressum</a><a href="{BASE}/privacy/">Datenschutz</a></nav>
<p>© 2026 Fit Essentials</p></div></footer>
</body></html>
'''
    full = os.path.join(ROOT, path.strip('/'), 'index.html') if path != '/' else os.path.join(ROOT, 'index.html')
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, 'w').write(doc)

def card(p):
    return f'''<div class="card" data-cat="{p['cat']}"><div class="ph"><img src="{esc(p['img'])}" alt="{esc(p['title'])}" loading="lazy"></div>
<div class="body"><div class="c">{esc(p['catname'])}</div><h3>{esc(p['title'])}</h3>
<a class="btn" href="{esc(p['url'])}" rel="nofollow sponsored noopener" target="_blank">Bei Amazon ansehen*</a></div></div>'''

def pbox(asin, note=''):
    p = by_asin.get(asin)
    if not p:
        return ''
    n = f'<p style="margin:2px 0 0;font-size:15px">{esc(note)}</p>' if note else ''
    return f'''<div class="pbox"><img src="{esc(p['img'])}" alt="{esc(p['title'])}" loading="lazy"><div><h3>{esc(p['title'])}</h3>{n}
<a class="btn" href="{esc(p['url'])}" rel="nofollow sponsored noopener" target="_blank">Bei Amazon ansehen*</a></div></div>'''

def pick(cat, n, skip=()):
    return [p['asin'] for p in products if p['cat'] == cat and p['asin'] not in skip][:n]

# ---------- blog posts ----------
POSTS = []

def post(slug, title, desc, body_html):
    POSTS.append((slug, title, desc))
    page(f'/blog/{slug}/', f'{title} | Fit Essentials', desc,
         f'<article><div class="eyebrow">Ratgeber</div><h1>{esc(title)}</h1>'
         f'<p class="note">Dieser Artikel enthält Affiliate-Links (Werbung). Die Produkte sind eine Auswahl, keine Testberichte.</p>'
         f'{body_html}<p style="margin-top:40px"><a class="btn ghost" href="{BASE}/produkte/">Alle Produkte ansehen</a></p></article>',
         current='blog')

leg = pick('leggings', 4)
post('beste-gym-leggings', 'Gym Leggings: Darauf solltest du beim Kauf achten',
     'High Waist, blickdicht, mit Taschen: So findest du Gym Leggings, die beim Training sitzen – plus eine Auswahl beliebter Modelle.',
     f'''<p>Leggings sind das Teil im Gym-Outfit, das am meisten aushalten muss: Kniebeugen, Ausfallschritte, Cardio. Bevor du kaufst, lohnt sich ein Blick auf vier Punkte.</p>
<h2>1. Blickdicht beim Squat</h2><p>Halte die Leggings beim Anprobieren gedehnt ins Licht oder mach eine tiefe Kniebeuge vor dem Spiegel. Dickere, matte Stoffe sind meist blickdichter als dünne, glänzende.</p>
<h2>2. High Waist</h2><p>Ein hoher Bund bleibt bei Bewegung besser an Ort und Stelle und lässt sich leicht mit Crop Tops und Sport-BHs kombinieren.</p>
<h2>3. Nähte und Passform</h2><p>Seamless-Leggings haben kaum Nähte und scheuern weniger. Scrunch-Modelle formen optisch, sind aber Geschmackssache.</p>
<h2>4. Taschen</h2><p>Seitliche Taschen für das Handy sind beim Laufen und im Gym praktischer, als man denkt.</p>
<h2>Beliebte Modelle</h2>{''.join(pbox(a) for a in leg)}''')

wo = pick('damen-outfits', 4)
post('gym-outfit-ideen-damen', 'Gym Outfit Ideen für Frauen: 4 Looks, die immer funktionieren',
     'Matching Sets, All Black oder sportlich-casual: Vier einfache Gym-Outfit-Ideen für Frauen zum Nachstylen.',
     f'''<p>Ein gutes Gym-Outfit muss nicht kompliziert sein. Diese vier Looks funktionieren im Training und auf dem Weg dorthin.</p>
<h2>1. Das Matching Set</h2><p>Top und Leggings in derselben Farbe wirken sofort aufgeräumt. Dunkelgrau, Schwarz und Braun sind leicht zu kombinieren.</p>
<h2>2. All Black</h2><p>Schwarze Leggings, schwarzes Top, weiße Socken und weiße Sneaker – der Klassiker, der nie falsch ist.</p>
<h2>3. Shorts statt Leggings</h2><p>Für Cardio und warme Tage: High-Waist-Shorts mit Sport-BH oder Crop Top.</p>
<h2>4. Gym to Street</h2><p>Eine Zip-Jacke oder ein Oversized-Hoodie über dem Set – fertig für den Weg nach Hause.</p>
<h2>Sets und Outfits zum Nachshoppen</h2>{''.join(pbox(a) for a in wo)}{''.join(pbox(a) for a in pick('damen-shorts', 1))}''')

mo = pick('herren-outfits', 5)
post('gym-outfit-herren', 'Gym Outfit für Männer: Clean, simpel, ohne viel Nachdenken',
     'So stellst du dir als Mann ein schlichtes Gym-Outfit zusammen: Basics, Farben und Kombinationen – mit Produktauswahl.',
     f'''<p>Die meisten guten Gym-Outfits für Männer bestehen aus wenigen Basics in Schwarz, Grau und Weiß. Damit passt alles zu allem.</p>
<h2>Die Basics</h2><ul><li>2–3 enge oder normale Trainingsshirts</li><li>Shorts oder Jogginghose</li><li>Ein Hoodie oder eine Zip-Jacke für den Weg</li><li>Schlichte Sneaker und Sportsocken</li></ul>
<h2>Farben</h2><p>Bleib bei Schwarz, Grau und Weiß. Ein komplett schwarzes Outfit wirkt immer clean, graue Sweatpants mit weißem Shirt sind der Streetwear-Klassiker.</p>
<h2>Passform</h2><p>Kompressionsshirts liegen eng an, normale Trainingsshirts sitzen lockerer. Für den Alltag nach dem Training eignen sich Baggy-Sweatpants.</p>
<h2>Produkte zum Nachshoppen</h2>{''.join(pbox(a) for a in mo)}''')

eq = pick('equipment', 5)
post('gym-tasche-checkliste', 'Gym-Tasche packen: Die Checkliste für jedes Training',
     'Was gehört in die Gym-Tasche? Eine einfache Checkliste von Trinkflasche bis Handtuch – plus praktische Produkte.',
     f'''<p>Nichts ist nerviger, als im Gym zu merken, dass etwas fehlt. Mit dieser Liste bist du in zwei Minuten startklar.</p>
<h2>Immer dabei</h2><ul><li>Trinkflasche oder Shaker</li><li>Handtuch</li><li>Kopfhörer</li><li>Wechselshirt und Socken</li><li>Schloss für den Spind</li></ul>
<h2>Je nach Training</h2><ul><li>Zughilfen oder Handschuhe fürs schwere Ziehen</li><li>Fitnessbänder fürs Aufwärmen</li><li>Gewichtheberschuhe für Kniebeugen</li></ul>
<h2>Nach dem Training</h2><ul><li>Duschgel und Deo</li><li>Beutel für nasse Sachen</li></ul>
<h2>Praktische Produkte</h2>{''.join(pbox(a) for a in eq)}''')

# ---------- blog index ----------
page('/blog/', 'Blog | Fit Essentials', 'Ratgeber zu Gym Outfits, Leggings und Trainings-Essentials.',
     '<section><div class="wrap"><div class="eyebrow">Blog</div><h1>Ratgeber</h1><p class="lead">Outfit-Ideen und Kaufhilfen für dein Training.</p></div></section>'
     '<section style="padding-top:0"><div class="wrap"><div class="posts">'
     + ''.join(f'<a class="post-card" href="{BASE}/blog/{s}/"><h3>{esc(t)}</h3><p>{esc(d)}</p></a>' for s, t, d in POSTS)
     + '</div></div></section>', current='blog')

# ---------- products ----------
filters = '<button type="button" data-f="all" aria-pressed="true">Alle</button>' + ''.join(
    f'<button type="button" data-f="{k}" aria-pressed="false">{esc(n)}</button>' for k, n in CATS)
script = '''<script>
(function(){var bs=document.querySelectorAll('.filters button'),cs=document.querySelectorAll('.grid .card');
function apply(f){bs.forEach(function(b){b.setAttribute('aria-pressed',b.dataset.f===f)});
cs.forEach(function(c){c.classList.toggle('hidden',f!=='all'&&c.dataset.cat!==f)});}
bs.forEach(function(b){b.addEventListener('click',function(){apply(b.dataset.f);history.replaceState(null,'',b.dataset.f==='all'?location.pathname:'#'+b.dataset.f)})});
var h=location.hash.slice(1);if(h&&document.querySelector('[data-f="'+h+'"]'))apply(h);})();
</script>'''
page('/produkte/', 'Alle Produkte | Fit Essentials',
     'Gym Outfits für Damen und Herren, Leggings, Schuhe und Gym Equipment – alle Fit-Essentials-Favoriten an einem Ort.',
     f'<section><div class="wrap"><div class="eyebrow">Shop the Look</div><h1>Alle Produkte</h1><p class="lead">{len(products)} Favoriten aus Gym-Mode und Equipment. Filtere nach Kategorie.</p></div></section>'
     f'<section style="padding-top:0"><div class="wrap"><div class="filters">{filters}</div><div class="grid">'
     + ''.join(card(p) for p in products) + f'</div></div></section>{script}', current='produkte')

# ---------- home ----------
TOP = ['B0HB8Y3GLY', 'B0D9WJTBHR', 'B0FJ4NKKYM', 'B0BCGR2CP1', 'B0GKNDGC6G', 'B0B2DC5Y2Y', 'B0FJRKHXQP', 'B0GHZ3CXNB']
featured = [by_asin[a] for a in TOP if a in by_asin][:8]
cats_html = ''.join(f'<a class="cat" href="{BASE}/produkte/#{k}">{esc(n)}<span>{sum(p["cat"] == k for p in products)}</span></a>' for k, n in CATS)
page('/', 'Fit Essentials | Gym Outfits & Fitness Finds',
     'Gym Outfits für Damen und Herren, Leggings, Activewear und Gym Equipment – Outfit-Ideen und Ratgeber von Fit Essentials.',
     f'''<section class="hero"><div class="wrap"><div class="eyebrow">Fit Essentials</div>
<h1>Gym Outfits &amp;<br>Fitness Finds</h1><p class="lead">Activewear, Outfit-Ideen und Gym-Essentials für Damen und Herren – ausgewählt, damit du nicht stundenlang suchen musst.</p>
<div class="btns"><a class="btn" href="{BASE}/produkte/">Produkte entdecken</a><a class="btn ghost" href="{BASE}/blog/">Zum Ratgeber</a></div></div></section>
<section><div class="wrap"><div class="section-head"><h2>Kategorien</h2></div><div class="cats">{cats_html}</div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="section-head"><h2>Beliebte Outfits</h2><a href="{BASE}/produkte/">Alle ansehen →</a></div>
<div class="grid">{''.join(card(p) for p in featured)}</div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="section-head"><h2>Aus dem Blog</h2><a href="{BASE}/blog/">Alle Artikel →</a></div>
<div class="posts">{''.join(f'<a class="post-card" href="{BASE}/blog/{s}/"><h3>{esc(t)}</h3><p>{esc(d)}</p></a>' for s, t, d in POSTS[:3])}</div></div></section>''')

# ---------- impressum (owner must fill in) ----------
page('/impressum/', 'Impressum | Fit Essentials', 'Impressum',
     '''<article><h1>Impressum</h1><p>Angaben gemäß § 5 DDG</p>
<p>[VORNAME NACHNAME]<br>[STRASSE HAUSNUMMER]<br>[PLZ ORT]<br>Deutschland</p>
<p>E-Mail: [E-MAIL-ADRESSE]</p>
<p>Verantwortlich für den Inhalt: [VORNAME NACHNAME], Anschrift wie oben.</p></article>''')

print('built', len(products), 'products,', len(POSTS), 'posts')
