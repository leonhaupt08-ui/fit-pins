// Renders pin images (1000x1500) from queue.json entries that have no image yet.
// Usage: node tools/render.js   (run from repo root)
//
// Every entry has a `layout` (product = cut-out product photo, collage = 4 images, otherwise a lifestyle
// photo) and a `style`. Styles rotate (see tools/assign_styles.py) so pins in a row never look the same:
//   dark / darkphoto – black background, big white caps headline (the original look)
//   cream            – warm cream background, serif headline, product in an arch-shaped white card
//   color            – colored background by category (blush / slate / sage), big dark headline below
//   card             – full photo with a white text card at the bottom
//   minimal          – product or photo almost without text, small label strip only
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const { execFileSync } = require('child_process');
const root = path.resolve(__dirname, '..');
const queue = JSON.parse(fs.readFileSync(path.join(root, 'queue.json'), 'utf8'));

const BOARD_COLOR = {
  '1110207814332818565': '#f1dcd5', '1110207814332818580': '#ead7cf', '1110207814332850044': '#f3e1dc',
  '1110207814332820674': '#efd9d2', '1110207814332963572': '#efdcd6',            // women: blush
  '1110207814332820701': '#d9dfe4', '1110207814332971379': '#dce1e5',            // men: slate
  '1110207814332816389': '#dfe5d6',                                               // gear: sage
};
const plain = h => h.replace(/<br>/g, ' ').replace(/\s+/g, ' ').trim().toLowerCase();
const base = `*{margin:0;padding:0;box-sizing:border-box}body{width:1000px;height:1500px;overflow:hidden;position:relative;font-family:'Inter',sans-serif}`;
const media = (p, uris, fit) => p.layout === 'collage'
  ? `<div class="grid">${uris.map(u => `<div><img src="${u}"></div>`).join('')}</div>`
  : `<img class="hero" src="${uris[0]}" style="object-fit:${fit}">`;
const ctaText = p => p.cta || (p.layout === 'collage' ? 'SEE THE LIST' : p.layout === 'product' ? 'SHOP NOW' : 'SHOP THE LOOK');

const T = {
  dark: (p, u) => `<style>${base}body{background:#0b0b0b}
.head{position:absolute;top:66px;left:66px;right:60px}
.tag{color:#fff;font-weight:600;letter-spacing:.35em;font-size:24px;opacity:.85}
.tag:before{content:'';display:inline-block;width:46px;height:3px;background:#fff;vertical-align:middle;margin-right:18px}
h1{margin-top:24px;color:#fff;font-family:'Inter Display','Inter';font-weight:900;font-size:${p.layout === 'collage' ? 96 : 104}px;line-height:.95;letter-spacing:-.02em;text-transform:uppercase}
.sub{margin-top:22px;margin-left:4px;color:#fff;font-size:33px;font-weight:500;opacity:.9}
.box{position:absolute;left:50px;right:50px;top:${p.layout === 'collage' ? 560 : 620}px;bottom:170px;border-radius:36px;overflow:hidden;background:${p.layout === 'collage' ? '#0b0b0b' : '#f4f4f2'};display:flex;align-items:center;justify-content:center;padding:${p.layout === 'product' ? 40 : 0}px}
.box .hero{width:100%;height:100%;mix-blend-mode:multiply}
.grid{width:100%;height:100%;display:grid;grid-template-columns:1fr 1fr;grid-template-rows:1fr 1fr;gap:18px}
.grid div{background:#f4f4f2;border-radius:28px;display:flex;align-items:center;justify-content:center;padding:18px;overflow:hidden}
.grid img{max-width:100%;max-height:100%;object-fit:contain;mix-blend-mode:multiply;border-radius:12px}
.brand{position:absolute;bottom:64px;left:70px;color:#fff;font-weight:800;letter-spacing:.42em;font-size:26px}
.brand span{font-weight:500;opacity:.7;letter-spacing:.2em;font-size:20px;display:block;margin-top:10px}
.cta{position:absolute;bottom:70px;right:70px;background:#fff;color:#000;font-weight:800;font-size:26px;padding:20px 30px;border-radius:999px;letter-spacing:.04em}
</style><div class="head"><div class="tag">${p.tag}</div><h1>${p.headline}</h1><div class="sub">${p.subline}</div></div>
<div class="box">${media(p, u, p.layout === 'product' ? 'contain' : 'cover')}</div>
<div class="brand">FIT ESSENTIALS<span>@fit.finds.de</span></div><div class="cta">${ctaText(p)} →</div>`,

  darkphoto: (p, u) => `<style>${base}body{background:#0b0b0b}
.img{position:absolute;inset:0;background:url('${u[0]}') ${p.position || 'center 35%'}/cover no-repeat}
.top{position:absolute;left:0;right:0;top:0;height:640px;background:linear-gradient(180deg,rgba(0,0,0,.92) 0%,rgba(0,0,0,.75) 45%,rgba(0,0,0,0) 100%)}
.bot{position:absolute;left:0;right:0;bottom:0;height:260px;background:linear-gradient(0deg,rgba(0,0,0,.9),rgba(0,0,0,0))}
.head{position:absolute;top:70px;left:66px;right:60px}
.tag{color:#fff;font-weight:600;letter-spacing:.35em;font-size:24px;opacity:.85}
.tag:before{content:'';display:inline-block;width:46px;height:3px;background:#fff;vertical-align:middle;margin-right:18px}
h1{margin-top:26px;color:#fff;font-family:'Inter Display','Inter';font-weight:900;font-size:112px;line-height:.95;letter-spacing:-.02em;text-transform:uppercase}
.sub{margin-top:28px;margin-left:4px;color:#fff;font-size:36px;font-weight:500;opacity:.92}
.brand{position:absolute;bottom:64px;left:70px;color:#fff;font-weight:800;letter-spacing:.42em;font-size:26px}
.brand span{font-weight:500;opacity:.7;letter-spacing:.2em;font-size:20px;display:block;margin-top:10px}
.cta{position:absolute;bottom:70px;right:70px;background:#fff;color:#000;font-weight:800;font-size:26px;padding:20px 30px;border-radius:999px;letter-spacing:.04em}
</style><div class="img"></div><div class="top"></div><div class="bot"></div>
<div class="head"><div class="tag">${p.tag}</div><h1>${p.headline}</h1><div class="sub">${p.subline}</div></div>
<div class="brand">FIT ESSENTIALS<span>@fit.finds.de</span></div><div class="cta">${ctaText(p)} →</div>`,

  cream: (p, u) => `<style>${base}body{background:#efe8de;color:#2a211b}
.head{position:absolute;top:72px;left:70px;right:70px;text-align:center}
.tag{font-size:22px;letter-spacing:.4em;font-weight:600;color:#8a6f5a}
h1{margin-top:22px;font-family:'Caladea','Liberation Serif',serif;font-weight:700;font-size:88px;line-height:1.02;text-transform:capitalize;letter-spacing:-.01em}
.sub{margin-top:16px;font-size:31px;color:#6b5646;font-style:italic;font-family:'Caladea',serif}
.box{position:absolute;left:70px;right:70px;top:500px;bottom:190px;background:#fff;border-radius:300px 300px 28px 28px;overflow:hidden;display:flex;align-items:center;justify-content:center;padding:${p.layout === 'product' ? '90px 50px 40px' : '0'}}
.box .hero{width:100%;height:100%;mix-blend-mode:multiply}
.grid{width:100%;height:100%;display:grid;grid-template-columns:1fr 1fr;grid-template-rows:1fr 1fr;gap:10px;padding:90px 26px 26px}
.grid div{display:flex;align-items:center;justify-content:center;overflow:hidden;background:#f7f3ee;border-radius:18px;padding:10px}
.grid img{max-width:100%;max-height:100%;object-fit:contain;mix-blend-mode:multiply}
.foot{position:absolute;left:0;right:0;bottom:62px;text-align:center}
.cta{display:inline-block;background:#2a211b;color:#efe8de;font-weight:700;font-size:26px;padding:20px 44px;border-radius:999px;letter-spacing:.12em}
.brand{margin-top:18px;font-size:20px;letter-spacing:.38em;color:#8a6f5a;font-weight:600}
</style><div class="head"><div class="tag">${p.tag}</div><h1>${plain(p.headline)}</h1><div class="sub">${p.subline}</div></div>
<div class="box">${media(p, u, p.layout === 'product' ? 'contain' : 'cover')}</div>
<div class="foot"><div class="cta">${ctaText(p)}</div><div class="brand">FIT ESSENTIALS</div></div>`,

  color: (p, u) => `<style>${base}body{background:${BOARD_COLOR[p.board_id] || '#e5e1da'};color:#111}
.box{position:absolute;left:60px;right:60px;top:60px;height:860px;background:#fff;border-radius:40px;overflow:hidden;display:flex;align-items:center;justify-content:center;padding:${p.layout === 'product' ? 50 : 0}px}
.box .hero{width:100%;height:100%;mix-blend-mode:multiply}
.grid{width:100%;height:100%;display:grid;grid-template-columns:1fr 1fr;grid-template-rows:1fr 1fr;gap:12px;padding:24px}
.grid div{display:flex;align-items:center;justify-content:center;background:#f5f5f3;border-radius:22px;padding:14px;overflow:hidden}
.grid img{max-width:100%;max-height:100%;object-fit:contain;mix-blend-mode:multiply}
.pill{position:absolute;top:90px;left:90px;background:#111;color:#fff;font-weight:800;font-size:22px;letter-spacing:.2em;padding:14px 22px;border-radius:999px}
.head{position:absolute;left:70px;right:70px;top:965px}
h1{font-family:'Inter Display','Inter';font-weight:900;font-size:${p.layout === 'collage' ? 92 : 100}px;line-height:.93;letter-spacing:-.03em;text-transform:uppercase}
.sub{margin-top:18px;font-size:30px;font-weight:500;opacity:.75}
.bar{position:absolute;left:70px;right:70px;bottom:60px;display:flex;justify-content:space-between;align-items:center;border-top:2px solid rgba(0,0,0,.15);padding-top:24px}
.bar b{font-size:22px;letter-spacing:.38em}
.bar span{font-weight:800;font-size:24px;letter-spacing:.06em}
</style><div class="box">${media(p, u, p.layout === 'product' ? 'contain' : 'cover')}</div><div class="pill">${p.tag}</div>
<div class="head"><h1>${p.headline}</h1><div class="sub">${p.subline}</div></div>
<div class="bar"><b>FIT ESSENTIALS</b><span>${ctaText(p)} →</span></div>`,

  card: (p, u) => `<style>${base}body{background:#ddd}
.img{position:absolute;inset:0;background:url('${u[0]}') ${p.position || 'center 30%'}/cover no-repeat}
.card{position:absolute;left:50px;right:50px;bottom:50px;background:#fff;border-radius:34px;padding:46px 50px 44px}
.tag{font-size:21px;font-weight:700;letter-spacing:.32em;color:#777}
h1{margin-top:14px;font-family:'Inter Display','Inter';font-weight:900;font-size:76px;line-height:.98;letter-spacing:-.02em;color:#111;text-transform:uppercase}
.sub{margin-top:14px;font-size:28px;color:#444}
.row{margin-top:28px;display:flex;justify-content:space-between;align-items:center}
.row b{font-size:19px;letter-spacing:.36em;color:#111}
.row span{background:#111;color:#fff;font-weight:800;font-size:23px;padding:16px 26px;border-radius:999px;letter-spacing:.04em}
</style><div class="img"></div><div class="card"><div class="tag">${p.tag}</div><h1>${p.headline}</h1><div class="sub">${p.subline}</div>
<div class="row"><b>FIT ESSENTIALS</b><span>${ctaText(p)} →</span></div></div>`,

  minimal: (p, u) => `<style>${base}body{background:#fff}
.wrap{position:absolute;left:0;right:0;top:0;bottom:150px;display:flex;align-items:center;justify-content:center;padding:${p.layout === 'product' ? '70px' : '0'};background:${p.layout === 'product' ? '#f6f6f4' : '#fff'}}
.wrap .hero{width:100%;height:100%;mix-blend-mode:multiply}
.strip{position:absolute;left:0;right:0;bottom:0;height:150px;background:#fff;display:flex;align-items:center;justify-content:space-between;padding:0 60px}
.strip h1{font-weight:800;font-size:38px;letter-spacing:-.01em;color:#111;text-transform:capitalize}
.strip span{font-size:19px;letter-spacing:.34em;font-weight:700;color:#888}
</style><div class="wrap">${media(p, u, p.layout === 'product' ? 'contain' : 'cover')}</div>
<div class="strip"><h1>${plain(p.headline)}</h1><span>FIT ESSENTIALS</span></div>`,
};

// Variants: every style has 4 color palettes x 2 text alignments, so pins of the same style still differ.
const PAL = {
  dark: [null, ['#14213d', '#fca311'], ['#2b1d17', '#e9c46a'], ['#13261f', '#a7c957']],
  darkphoto: [null, ['#14213d', '#fca311'], ['#2b1d17', '#e9c46a'], ['#13261f', '#a7c957']],
  cream: [null, ['#f4e4e1', '#7a3e3a'], ['#e7edf0', '#264653'], ['#eef0e4', '#4a5a2a']],
  color: [null, ['#111111', '#ffffff'], ['#f2e8cf', '#3d2b1f'], ['#cfe1f2', '#0d2c4a']],
  card: [null, ['#111111', '#ffffff'], ['#f6efe6', '#3d2b1f'], ['#e63946', '#ffffff']],
  minimal: [null, ['#111111', '#ffffff'], ['#efe8de', '#2a211b'], ['#dfe5d6', '#1f2b12']],
};
function variantCss(style, v) {
  const pal = PAL[style][v % 4], left = Math.floor(v / 4) % 2 === 1;
  let c = '';
  if (pal) {
    const [bg, ac] = pal;
    if (style === 'dark') c += `body{background:${bg}}.cta{background:${ac}}.tag:before{background:${ac}}.grid,.box{background:${bg}}`;
    if (style === 'dark' && true) c += `.box{background:#f4f4f2}.box:has(.grid){background:${bg}}`;
    if (style === 'darkphoto') c += `.top{background:linear-gradient(180deg,${bg}f0 0%,${bg}c0 45%,${bg}00 100%)}.bot{background:linear-gradient(0deg,${bg}e6,${bg}00)}.cta{background:${ac}}.tag:before{background:${ac}}`;
    if (style === 'cream') c += `body{background:${bg};color:${ac}}.cta{background:${ac};color:${bg}}.tag,.brand,.sub{color:${ac};opacity:.8}`;
    if (style === 'color') c += `body{background:${bg};color:${ac}}.pill{background:${ac};color:${bg}}.bar{border-color:${ac}33}`;
    if (style === 'card') c += `.card{background:${bg}}.card h1,.card .row b{color:${ac}}.card .tag,.card .sub{color:${ac};opacity:.8}.row span{background:${ac};color:${bg}}`;
    if (style === 'minimal') c += `.strip{background:${bg}}.strip h1{color:${ac}}.strip span{color:${ac};opacity:.6}`;
  }
  if (left) {
    if (style === 'cream') c += `.head{text-align:left}.foot{text-align:left;left:70px}`;
    if (style === 'dark' || style === 'darkphoto') c += `.head{text-align:right;right:66px;left:60px}.tag:before{display:none}.tag:after{content:'';display:inline-block;width:46px;height:3px;background:currentColor;vertical-align:middle;margin-left:18px}`;
    if (style === 'color') c += `.head{text-align:right}.pill{left:auto;right:90px}`;
    if (style === 'card') c += `.card{bottom:auto;top:50px}`;
    if (style === 'minimal') c += `.strip{top:0;bottom:auto}.wrap{top:150px;bottom:0}`;
  }
  return c ? `<style>${c}</style>` : '';
}

(async () => {
  const only = process.argv[2];   // optional: render a single slug (overwrites)
  const todo = queue.filter(p => only ? p.slug === only : !fs.existsSync(path.join(root, 'pins', p.slug + '.jpg')));
  if (!todo.length) { console.log('nothing to render'); return; }
  const b = await chromium.launch();
  const page = await b.newPage({ viewport: { width: 1000, height: 1500 }, deviceScaleFactor: 1 });
  const get = u => 'data:image/jpeg;base64,' + execFileSync('curl', ['-sSfL', u], { maxBuffer: 50e6 }).toString('base64');
  for (const p of todo) {
    const kind = p.layout === 'collage' ? 'collage' : p.layout === 'product' ? 'product' : 'photo';
    const style = p.style || (kind === 'photo' ? 'darkphoto' : 'dark');
    let uris;
    try { uris = (kind === 'collage' ? p.images : [p.source_image]).map(get); }
    catch (e) { console.log('SKIP (image download failed)', p.slug); continue; }
    const q = Object.assign({ tag: kind === 'product' ? 'GYM ESSENTIALS' : 'OUTFIT IDEA', subline: '' }, p);
    await page.setContent(`<!doctype html><html><head><meta charset="utf-8"></head><body>${T[style](q, uris)}${variantCss(style, p.variant || 0)}</body></html>`, { waitUntil: 'load' });
    await page.waitForTimeout(250);
    await page.screenshot({ path: path.join(root, 'pins', p.slug + '.jpg'), type: 'jpeg', quality: 90 });
    console.log('rendered', p.slug, style);
  }
  await b.close();
})();
