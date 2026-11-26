# Gives every queued pin without a style a design style, rotating per layout so neighbours differ.
# Run: python3 tools/assign_styles.py [--reset]   (--reset re-assigns all queued pins and deletes their images)
import json, os, sys
ROT = {'product': ['cream', 'dark', 'color', 'minimal'], 'photo': ['card', 'darkphoto', 'cream', 'color'], 'collage': ['color', 'cream', 'dark']}
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
q = json.load(open(os.path.join(root, 'queue.json')))
reset = '--reset' in sys.argv
idx = {k: 0 for k in ROT}; prev = None
for e in q:
    if e['status'] != 'queued' or (e.get('style') and not reset):
        continue
    kind = e.get('layout') if e.get('layout') in ('product', 'collage') else 'photo'
    s = ROT[kind][idx[kind] % len(ROT[kind])]; idx[kind] += 1
    if s == prev:
        s = ROT[kind][idx[kind] % len(ROT[kind])]; idx[kind] += 1
    e['style'] = s; prev = s
    if reset:
        f = os.path.join(root, 'pins', e['slug'] + '.jpg')
        if os.path.exists(f): os.remove(f)
json.dump(q, open(os.path.join(root, 'queue.json'), 'w'), ensure_ascii=False, indent=2)
print('styled', sum(idx.values()))
