// Renders pin images (1000x1500) from queue.json entries that have no image yet.
// Usage: node tools/render.js   (run from repo root)
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const { execFileSync } = require('child_process');
const root = path.resolve(__dirname, '..');
const queue = JSON.parse(fs.readFileSync(path.join(root, 'queue.json'), 'utf8'));
const htmlProduct = (dataUri, tag, head, sub) => `<!doctype html><html><head><style>
*{margin:0;padding:0;box-sizing:border-box}
body{width:1000px;height:1500px;background:#0b0b0b;font-family:'Inter',sans-serif;overflow:hidden;position:relative}
.head{position:absolute;top:70px;left:66px;right:60px}
.tag{color:#fff;font-weight:600;letter-spacing:.35em;font-size:24px;opacity:.85}
.tag:before{content:'';display:inline-block;width:46px;height:3px;background:#fff;vertical-align:middle;margin-right:18px}
h1{margin-top:26px;color:#fff;font-family:'Inter Display','Inter';font-weight:900;font-size:104px;line-height:.95;letter-spacing:-.02em;text-transform:uppercase}
.sub{margin-top:24px;margin-left:4px;color:#fff;font-size:34px;font-weight:500;opacity:.9}
.panel{position:absolute;left:50px;right:50px;top:620px;bottom:170px;background:#f4f4f2;border-radius:36px;display:flex;align-items:center;justify-content:center;padding:40px}
.panel img{max-width:100%;max-height:100%;object-fit:contain;mix-blend-mode:multiply}
.brand{position:absolute;bottom:64px;left:70px;color:#fff;font-weight:800;letter-spacing:.42em;font-size:26px}
.brand span{font-weight:500;opacity:.7;letter-spacing:.2em;font-size:20px;display:block;margin-top:10px}
.cta{position:absolute;bottom:70px;right:70px;background:#fff;color:#000;font-weight:800;font-size:26px;padding:20px 30px;border-radius:999px;letter-spacing:.04em}
</style></head><body><div class="head"><div class="tag">${tag}</div><h1>${head}</h1><div class="sub">${sub}</div></div>
<div class="panel"><img src="${dataUri}"></div>
<div class="brand">FIT ESSENTIALS<span>@fit.finds.de</span></div><div class="cta">SHOP NOW →</div></body></html>`;
const htmlCollage = (uris, tag, head, sub, cta) => `<!doctype html><html><head><style>
*{margin:0;padding:0;box-sizing:border-box}
body{width:1000px;height:1500px;background:#0b0b0b;font-family:'Inter',sans-serif;overflow:hidden;position:relative}
.head{position:absolute;top:66px;left:66px;right:60px}
.tag{color:#fff;font-weight:600;letter-spacing:.35em;font-size:24px;opacity:.85}
.tag:before{content:'';display:inline-block;width:46px;height:3px;background:#fff;vertical-align:middle;margin-right:18px}
h1{margin-top:24px;color:#fff;font-family:'Inter Display','Inter';font-weight:900;font-size:96px;line-height:.95;letter-spacing:-.02em;text-transform:uppercase}
.sub{margin-top:22px;margin-left:4px;color:#fff;font-size:32px;font-weight:500;opacity:.9}
.grid{position:absolute;left:50px;right:50px;top:560px;bottom:170px;display:grid;grid-template-columns:1fr 1fr;grid-template-rows:1fr 1fr;gap:18px}
.grid div{background:#f4f4f2;border-radius:28px;display:flex;align-items:center;justify-content:center;padding:18px;overflow:hidden}
.grid img{max-width:100%;max-height:100%;object-fit:contain;mix-blend-mode:multiply;border-radius:12px}
.brand{position:absolute;bottom:64px;left:70px;color:#fff;font-weight:800;letter-spacing:.42em;font-size:26px}
.brand span{font-weight:500;opacity:.7;letter-spacing:.2em;font-size:20px;display:block;margin-top:10px}
.cta{position:absolute;bottom:70px;right:70px;background:#fff;color:#000;font-weight:800;font-size:26px;padding:20px 30px;border-radius:999px;letter-spacing:.04em}
</style></head><body><div class="head"><div class="tag">${tag}</div><h1>${head}</h1><div class="sub">${sub}</div></div>
<div class="grid">${uris.map(u => `<div><img src="${u}"></div>`).join('')}</div>
<div class="brand">FIT ESSENTIALS<span>@fit.finds.de</span></div><div class="cta">${cta} →</div></body></html>`;
const html = (dataUri, tag, head, sub, pos) => `<!doctype html><html><head><style>
*{margin:0;padding:0;box-sizing:border-box}
body{width:1000px;height:1500px;background:#0b0b0b;font-family:'Inter',sans-serif;overflow:hidden;position:relative}
.img{position:absolute;inset:0;background:url('${dataUri}') ${pos}/cover no-repeat}
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
</style></head><body><div class="img"></div><div class="top"></div><div class="bot"></div>
<div class="head"><div class="tag">${tag}</div><h1>${head}</h1><div class="sub">${sub}</div></div>
<div class="brand">FIT ESSENTIALS<span>@fit.finds.de</span></div><div class="cta">SHOP THE LOOK →</div>
</body></html>`;
(async () => {
  const todo = queue.filter(p => !fs.existsSync(path.join(root, 'pins', p.slug + '.jpg')));
  if (!todo.length) { console.log('nothing to render'); return; }
  const b = await chromium.launch();
  const page = await b.newPage({ viewport: { width: 1000, height: 1500 }, deviceScaleFactor: 1 });
  for (const p of todo) {
    const get = u => 'data:image/jpeg;base64,' + execFileSync('curl', ['-sSfL', u], { maxBuffer: 50e6 }).toString('base64');
    let uri, uris;
    try { if (p.layout === 'collage') uris = p.images.map(get); else uri = get(p.source_image); }
    catch (e) { console.log('SKIP (image download failed)', p.slug); continue; }
    const doc = p.layout === 'collage' ? htmlCollage(uris, p.tag || 'OUTFIT IDEA', p.headline, p.subline, p.cta || 'SEE THE LIST')
      : p.layout === 'product' ? htmlProduct(uri, p.tag || 'GYM ESSENTIALS', p.headline, p.subline) : html(uri, p.tag || 'OUTFIT IDEA', p.headline, p.subline, p.position || 'center 35%');
    await page.setContent(doc, { waitUntil: 'load' });
    await page.waitForTimeout(300);
    await page.screenshot({ path: path.join(root, 'pins', p.slug + '.jpg'), type: 'jpeg', quality: 90 });
    console.log('rendered', p.slug);
  }
  await b.close();
})();
