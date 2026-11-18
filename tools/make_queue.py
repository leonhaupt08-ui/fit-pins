# Adds redesigned pins for existing catalog products to queue.json.
# Usage (repo root): python3 tools/make_queue.py <thumbs_dir>
import json, re, sys, os
from itertools import zip_longest
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
THUMBS = sys.argv[1]
catalog = json.load(open(os.path.join(ROOT, 'data', 'catalog.json')))
queue = json.load(open(os.path.join(ROOT, 'queue.json')))
done = {e['product_url'].split('/dp/')[1][:10] for e in queue}

SKIP_CAT = {'supplements', 'm-basics'}
SKIP_ASIN = {'B0872L92RV', 'B09YRHZZKC', 'B0H6FDTPXG', 'B0F541N2KD', 'B0CG6TG1LH', 'B0GVDXQVHJ', 'B0DZ2QM27X',
             'B00YMG2ZNI', 'B0CMTKCM4R', 'B0BGVZ9KHD', 'B01F2OGJQM', 'B093LQ8W49', 'B0C7GWGLWV', 'B0CFYC4BQT',
             'B0D8PVH6H8', 'B0DW8VRHQH', 'B0D5M7HHNY', 'B0DNTWJJV2', 'B0CF1VMW9X', 'B0FCSSND2X'}

B_WOUT, B_LEG, B_WTOP, B_WSHORT = '1110207814332818565', '1110207814332818580', '1110207814332850044', '1110207814332820674'
B_MEN, B_MSHOE, B_GEAR = '1110207814332820701', '1110207814332971379', '1110207814332816389'

CFG = {
 'w-sets':      (B_WOUT,  'OUTFIT IDEA',   'Matching set · gym to street', "Women's Matching Gym Set",
                 "{n} for women – a matching workout set that looks put together in the gym and on the way there. Style it with white sneakers and a zip jacket.",
                 '#MatchingSet #GymOutfitWomen #WorkoutSet #Activewear #GymOutfit'),
 'w-leggings':  (B_LEG,   'OUTFIT IDEA',   'Leggings outfit idea', "Women's Workout Leggings",
                 "{n} – easy to style with a sports bra, crop top or oversized tee for the gym, yoga and everyday athleisure.",
                 '#LeggingsOutfit #GymLeggings #WorkoutOutfit #Athleisure #GymOutfitWomen'),
 'w-tops':      (B_WTOP,  'OUTFIT IDEA',   'Gym top for women', "Women's Gym Top Outfit",
                 "{n} for women – pair it with high waisted leggings or shorts for a clean workout outfit that also works outside the gym.",
                 '#GymTop #SportsBra #WorkoutOutfit #GymOutfitWomen #Activewear'),
 'w-bottoms':   (B_WOUT,  'OUTFIT IDEA',   'Comfy · sporty · easy to style', "Women's Athleisure Outfit",
                 "{n} for women – comfortable for workouts, errands and lazy days. Combine with a fitted top and sneakers.",
                 '#AthleisureOutfit #WorkoutOutfit #ComfyOutfit #GymOutfitWomen #Activewear'),
 'm-tops':      (B_MEN,   'OUTFIT IDEA',   'Clean gym basic for men', "Men's Gym Outfit",
                 "{n} for men – a simple gym basic that goes with every pair of shorts or joggers. Keep it neutral: black, grey and white.",
                 '#GymOutfitMen #MensActivewear #GymWear #MensFashion #WorkoutClothes'),
 'm-long':      (B_MEN,   'OUTFIT IDEA',   'Layer up for training', "Men's Training Layer",
                 "{n} for men – a sporty layer for cold gym days, running or a clean casual outfit with joggers and sneakers.",
                 '#GymOutfitMen #MensStyle #Athleisure #MensActivewear #TrainingWear'),
 'm-bottoms':   (B_MEN,   'OUTFIT IDEA',   'Gym & streetwear for men', "Men's Gym Outfit",
                 "{n} for men – comfortable for training and easy to wear after the gym with a plain tee and sneakers.",
                 '#GymOutfitMen #MensActivewear #Streetwear #GymShorts #MensFashion'),
 'm-sets':      (B_MEN,   'OUTFIT IDEA',   'Complete outfit for men', "Men's Matching Set",
                 "{n} – a complete matching outfit for men. No styling needed: put it on and go.",
                 '#MensOutfit #MatchingSet #GymOutfitMen #Athleisure #MensFashion'),
 'shoes':       (B_MSHOE, 'GYM ESSENTIALS', 'Train · run · lift', 'Gym & Running Shoes',
                 "{n} – a solid pick for training and running. Check the size chart before ordering.",
                 '#GymShoes #RunningShoes #TrainingShoes #FitnessGear #GymEssentials'),
 'accessories': (B_GEAR,  'GYM ESSENTIALS', 'Gym bag essential', 'Gym Bag Essentials',
                 "{n} – a practical gym bag essential for everyday training.",
                 '#GymEssentials #GymBag #FitnessGear #WhatsInMyGymBag #GymAccessories'),
 'equipment':   (B_GEAR,  'HOME GYM',       'Train anywhere', 'Home Gym Equipment',
                 "{n} – useful equipment for home workouts and the gym.",
                 '#HomeGym #HomeWorkout #FitnessEquipment #WorkoutAtHome #GymEssentials'),
 'recovery':    (B_GEAR,  'RECOVERY',       'Rest day essential', 'Recovery Tools',
                 "{n} – a simple tool for your rest day and post-workout routine.",
                 '#RestDay #Recovery #SelfCare #GymEssentials #MobilityWork'),
}
DROP = re.compile(r"\b(Men's|Women's|for Women|for Men|\d-Pack|\(Pair\)|Set of \d+)\b", re.I)
BRANDS = re.compile(r'^(SMILODOX|CAMBIVO|Odizli|Under Armour|Nike|adidas|Adidas|BALENNZ|JAKO|Salomon|ABOVE|BlenderBottle|Super Sparrow|720°DGREE|Harbinger|BLACKROLL|BetterYou|Calvin Klein|BOSS|Hummel|Stanley|Pink Stanley)\s+')

def headline(name, cat):
    t = BRANDS.sub('', name)
    t = DROP.sub('', t)
    t = re.sub(r'\s{2,}', ' ', t).strip(' -&')
    words, lines, cur = t.upper().split(), [], ''
    for w in words:
        if len(cur) + len(w) + (1 if cur else 0) <= 12:
            cur = (cur + ' ' + w).strip()
        else:
            lines.append(cur); cur = w
    lines.append(cur)
    lines = [l for l in lines if l]
    if len(lines) > 3 or any(len(l) > 13 for l in lines):
        lines = {'w-leggings': ['LEGGINGS', 'OUTFIT IDEA'], 'w-sets': ['MATCHING', 'GYM SET'], 'w-tops': ['GYM TOP', 'OUTFIT'],
                 'w-bottoms': ['COMFY', 'GYM OUTFIT'], 'm-tops': ["MEN'S GYM", 'BASICS'], 'm-long': ['GYM', 'LAYERS'],
                 'm-bottoms': ["MEN'S GYM", 'BOTTOMS'], 'm-sets': ["MEN'S", 'GYM SET'], 'shoes': ['GYM', 'SHOES'],
                 'accessories': ['GYM BAG', 'ESSENTIAL'], 'equipment': ['HOME GYM', 'ESSENTIAL'], 'recovery': ['REST DAY', 'ESSENTIAL']}[cat]
    return '<br>'.join(lines)

buckets = {}
for p in catalog:
    if p['asin'] in done or p['asin'] in SKIP_ASIN or p['cat'] in SKIP_CAT:
        continue
    w, h = Image.open(os.path.join(THUMBS, p['asin'] + '.jpg')).size
    board, tag, sub, suffix, desc, tags = CFG[p['cat']]
    if p['cat'] == 'w-bottoms' and 'Short' in p['title']:
        board = B_WSHORT
    name = p['title']
    title = f"{name} | {suffix}"
    if len(title) > 100:
        title = name[:100]
    slug_base = re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-')[:40].strip('-')
    e = {'slug': slug_base, 'status': 'queued',
         'product_url': p['url'], 'source_image': p['img'].replace('/564x/', '/1200x/'),
         'board_id': board, 'tag': tag, 'headline': headline(name, p['cat']), 'subline': sub,
         'title': title,
         'description': desc.format(n=name) + '\n\nWerbung | Affiliate-Link\n\n' + tags}
    if h / w < 1.15:
        e['layout'] = 'product'
        e['tag'] = 'GYM ESSENTIALS' if p['cat'] in ('accessories', 'equipment', 'shoes', 'recovery') else 'OUTFIT IDEA'
    else:
        e['position'] = 'center 30%'
    group = 'w' if p['cat'].startswith('w-') else 'm' if p['cat'].startswith('m-') else 'g'
    buckets.setdefault(group, []).append(e)

# interleave women / men / gear so every day is mixed
order = [x for trio in zip_longest(buckets.get('w', []), buckets.get('m', []), buckets.get('g', [])) for x in trio if x]
seen, merged = set(), []
for e in order:
    if e['product_url'] not in seen:
        seen.add(e['product_url']); merged.append(e)
n = max(int(re.match(r'(\d+)', q['slug']).group(1)) for q in queue)
for e in merged:
    n += 1
    e['slug'] = f"{n:03d}-{e['slug']}"
queue.extend(merged)
json.dump(queue, open(os.path.join(ROOT, 'queue.json'), 'w'), ensure_ascii=False, indent=2)
open(os.path.join(ROOT, 'queue.json'), 'a').write('\n')
print('added', len(merged), {k: len(v) for k, v in buckets.items()})
