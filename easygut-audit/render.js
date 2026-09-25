// usage: node render.js <name>  -> <name>.pdf + preview PNGs in scratchpad
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const name = process.argv[2];
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  const p = await b.newPage({ viewport: { width: 794, height: 1123 }, deviceScaleFactor: 2 });
  await p.goto('file://' + path.resolve(__dirname, name + '.html'), { waitUntil: 'networkidle' });
  await p.evaluate(() => document.fonts.ready);
  await p.pdf({ path: path.resolve(__dirname, (process.argv[3] || name) + '.pdf'), format: 'A4', printBackground: true, preferCSSPageSize: true });
  const pages = await p.$$('.page');
  for (let i = 0; i < pages.length; i++)
    await pages[i].screenshot({ path: `${process.env.SHOTS}/${name}_p${i + 1}.png` });
  // overflow check: content taller than page?
  const over = await p.$$eval('.page', ps => ps.map(pg => { const r = pg.getBoundingClientRect(); let m = 0; pg.querySelectorAll('*').forEach(e => { const b = e.getBoundingClientRect(); if (!e.closest('.foot')) m = Math.max(m, b.bottom - r.top); }); return Math.round(m) + '/' + Math.round(r.height); }));
  console.log('content bottom / page height:', over.join('  '));
  await b.close();
})();
