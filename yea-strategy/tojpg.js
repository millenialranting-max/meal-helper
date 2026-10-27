// usage: node tojpg.js in.png out.jpg width
const { chromium } = require('playwright'); const path = require('path');
(async () => {
  const [inp, out, w] = process.argv.slice(2);
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1243/chrome-linux64/chrome' });
  const p = await b.newPage({ viewport: { width: +w, height: 2000 } });
  await p.setContent(`<html><body style="margin:0"><img id=i src="file://${path.resolve(inp)}" style="width:${w}px;display:block"></body></html>`);
  await p.goto('file://' + path.resolve(inp)).catch(()=>{});
  await p.setContent(`<body style="margin:0"></body>`);
  const data = require('fs').readFileSync(inp).toString('base64');
  await p.setContent(`<html><body style="margin:0"><img id=i src="data:image/png;base64,${data}" style="width:${w}px;display:block"></body></html>`);
  await p.waitForSelector('#i'); await p.evaluate(() => document.getElementById('i').decode());
  await (await p.$('#i')).screenshot({ path: out, type: 'jpeg', quality: 82 });
  await b.close();
})();
