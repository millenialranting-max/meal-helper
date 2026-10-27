const { chromium } = require('playwright'); const path = require('path');
(async () => {
  const [name, out] = process.argv.slice(2);
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1243/chrome-linux64/chrome' });
  const p = await b.newPage({ viewport: { width: 794, height: 1123 }, deviceScaleFactor: 2 });
  await p.goto('file://' + path.resolve(__dirname, name), { waitUntil: 'networkidle' });
  await p.evaluate(() => document.fonts.ready);
  await p.pdf({ path: path.resolve(__dirname, out), format: 'A4', printBackground: true, preferCSSPageSize: true });
  await (await p.$('.page')).screenshot({ path: process.env.SHOT });
  const m = await p.$eval('.page', pg => { const r = pg.getBoundingClientRect(); let m = 0; pg.querySelectorAll('*').forEach(e => { if (!e.closest('.foot')) m = Math.max(m, e.getBoundingClientRect().bottom - r.top); }); return Math.round(m); });
  console.log('content bottom', m, '/ 1123 (footer ~1085)');
  await b.close();
})();
