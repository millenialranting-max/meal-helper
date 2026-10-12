const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch(); const ctx = await b.newContext({ viewport: { width: 1366, height: 820 } });
  await ctx.route('**/*', r => { const u = r.request().url();
    if (/facebook\.com\/tr/.test(u)) return r.fulfill({ status: 200, body: '' });
    if (/googletagmanager\.com\/gtm\.js\?id=GTM-5CDGJP32/.test(u) && !/gtm_auth/.test(u)) return r.continue({ url: u + '&gtm_auth=z9n2djVKe7XBN0x2yK8THA&gtm_preview=env-15&gtm_cookies_win=x' });
    return r.continue(); });
  const p = await ctx.newPage(); await p.goto('https://nxtschool.edu.rs/upis/'); await p.evaluate(() => localStorage.setItem('nxt_consent_v1', '0'));
  await p.goto('https://nxtschool.edu.rs/upis/', { waitUntil: 'load' }); await p.waitForTimeout(1500);
  const before = await p.evaluate(() => !!document.getElementById('nxt-cc'));
  await p.evaluate(() => document.querySelector('a[href="#kolacici-podesavanja"]').click()); await p.waitForTimeout(800);
  const t = await p.evaluate(() => { const d = document.getElementById('nxt-cc'); return d && !d.hidden ? d.querySelector('p').textContent.slice(0, 60) : 'not shown'; });
  console.log('reopen | banner before click:', before, '| after footer click:', t); await b.close();
})();
