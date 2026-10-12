// Final pre-publish check: real GTM workspace preview on the LIVE site. Meta /tr requests and form POSTs are intercepted (nothing is sent).
const { chromium, devices } = require('playwright');
const ENV = '&gtm_auth=z9n2djVKe7XBN0x2yK8THA&gtm_preview=env-15&gtm_cookies_win=x';
const S = 'https://nxtschool.edu.rs';
let b, HUA;
async function ctxFor(mobile, redirect) {
  const opt = mobile ? { ...devices['iPhone 13'] } : { viewport: { width: 1366, height: 820 } };
  opt.userAgent = (mobile ? devices['iPhone 13'].userAgent : HUA.replace('HeadlessChrome', 'Chrome'));
  const ctx = await b.newContext(opt); const fb = [], blocked = [];
  await ctx.addInitScript(() => Object.defineProperty(navigator, 'webdriver', { get: () => false }));
  await ctx.route('**/*', async r => { const q = r.request(), u = q.url();
    if (/facebook\.com\/tr/.test(u)) { const m = u + ' ' + (q.postData() || ''); const ev = (m.match(/[?&]ev=([^&\s]+)/) || [])[1]; if (ev) fb.push(ev + ((m.match(/[?&]eid=([^&\s]+)/) || [])[1] ? '(eid)' : '')); return r.fulfill({ status: 200, body: '' }); }
    if (q.method() === 'POST' && /nxtschool\.edu\.rs/.test(u)) {
      if (/admin-ajax\.php/.test(u) && /elementor_pro_forms_send_form/.test(q.postData() || '')) return r.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ success: true, data: { message: 'OK', data: redirect ? { redirect_url: S + redirect } : {} } }) });
      blocked.push(u); return r.abort(); }
    if (/googletagmanager\.com\/gtm\.js\?id=GTM-5CDGJP32/.test(u) && !/gtm_auth/.test(u)) return r.continue({ url: u + ENV });
    if (/nxtschool\.edu\.rs/.test(u)) return r.continue({ headers: { ...q.headers(), 'user-agent': HUA } });
    return r.continue(); });
  const p = await ctx.newPage(); const errs = []; p.on('pageerror', e => errs.push(e.message));
  return { ctx, p, fb, blocked, errs };
}
const bannerInfo = p => p.evaluate(() => { const d = document.getElementById('nxt-cc'); if (!d || d.hidden) return 'no banner';
  const y = d.querySelector('.nxt-cc-yes').getBoundingClientRect(), n = d.querySelector('.nxt-cc-no').getBoundingClientRect(), a = d.querySelector('p a');
  return `banner ok, title="${d.querySelector('strong').textContent}", Prihvatam ${Math.round(y.width)}x${Math.round(y.height)} vs Samo neophodni ${Math.round(n.width)}x${Math.round(n.height)}, link=${a.getAttribute('href')}`; });
async function fillSubmit(p) {
  await p.evaluate(() => { const f = document.querySelector('form.elementor-form');
    f.querySelectorAll('input:not([type=hidden]):not([type=checkbox]):not([type=radio]), textarea').forEach(i => { i.value = i.type === 'email' ? 'test@example.com' : (i.type === 'tel' ? '0601234567' : 'TEST'); });
    f.querySelectorAll('select').forEach(s => { if (s.options.length > 1) s.selectedIndex = 1; });
    f.querySelectorAll('input[type=checkbox]').forEach(c => c.checked = true);
    const r = f.querySelector('input[type=radio]'); if (r) r.checked = true; });
  await p.evaluate(() => document.querySelector('form.elementor-form button[type=submit]').click());
}
(async () => {
  b = await chromium.launch(); HUA = await (await b.newPage()).evaluate(() => navigator.userAgent);
  const out = [];
  // D1 desktop /upis/: banner, accept, form with redirect to /hvala
  { const t = await ctxFor(false, '/hvala/'); await t.p.goto(S + '/upis/', { waitUntil: 'load' }); await t.p.waitForTimeout(1500);
    const bi = await bannerInfo(t.p); await t.p.click('#nxt-cc .nxt-cc-yes'); await t.p.waitForTimeout(1500); const a = t.fb.join(','); 
    await fillSubmit(t.p); await t.p.waitForTimeout(5000);
    out.push(`D1 desktop /upis/ | ${bi} | after accept: ${a} | after form: ${t.fb.slice(a.split(',').length).join(',')} | now on ${t.p.url().replace(S, '')} | errors ${t.errs.length} | real POSTs blocked ${t.blocked.length}`); await t.ctx.close(); }
  // D2 desktop /upis/: reject, nothing fires; footer link visible and reopens banner with new copy
  { const t = await ctxFor(false, '/hvala/'); await t.p.goto(S + '/upis/', { waitUntil: 'load' }); await t.p.waitForTimeout(1500);
    await t.p.click('#nxt-cc .nxt-cc-no'); await t.p.waitForTimeout(800);
    const link = await t.p.evaluate(() => { const a = [...document.querySelectorAll('a[href="#kolacici-podesavanja"]')].find(x => x.getBoundingClientRect().width > 0); return a ? a.textContent : null; });
    if (link) { await t.p.evaluate(() => [...document.querySelectorAll('a[href="#kolacici-podesavanja"]')].find(x => x.getBoundingClientRect().width > 0).click()); await t.p.waitForTimeout(800); }
    const reopened = await bannerInfo(t.p);
    await t.p.click('#nxt-cc .nxt-cc-no').catch(() => {}); await fillSubmit(t.p); await t.p.waitForTimeout(5000);
    out.push(`D2 desktop reject | Meta requests: ${t.fb.join(',') || 'none'} | visible footer link: ${link} | reopened: ${reopened.slice(0, 50)} | errors ${t.errs.length}`); await t.ctx.close(); }
  // D3 Open Day form -> CompleteRegistration on /hvala-open-day/
  { const t = await ctxFor(false, '/hvala-open-day/'); await t.p.goto(S + '/open-day/', { waitUntil: 'load' }); await t.p.waitForTimeout(1500);
    await t.p.click('#nxt-cc .nxt-cc-yes'); await t.p.waitForTimeout(1200); await fillSubmit(t.p); await t.p.waitForTimeout(5000);
    out.push(`D3 desktop /open-day/ | Meta: ${t.fb.join(',')} | now on ${t.p.url().replace(S, '')} | errors ${t.errs.length}`); await t.ctx.close(); }
  // D4 homepage: banner + accept
  { const t = await ctxFor(false); await t.p.goto(S + '/', { waitUntil: 'load' }); await t.p.waitForTimeout(1500);
    const bi = await bannerInfo(t.p); await t.p.click('#nxt-cc .nxt-cc-yes'); await t.p.waitForTimeout(1500);
    out.push(`D4 homepage | ${bi.slice(0, 40)} | Meta: ${t.fb.join(',')} | errors ${t.errs.length}`); await t.ctx.close(); }
  // D5 direct /hvala/ visit with consent stored -> PageView only, no Lead
  { const t = await ctxFor(false); await t.p.goto(S + '/upis/'); await t.p.evaluate(() => localStorage.setItem('nxt_consent_v1', '1'));
    await t.p.goto(S + '/hvala/', { waitUntil: 'load' }); await t.p.waitForTimeout(2500);
    out.push(`D5 direct /hvala/ (consent=1) | Meta: ${t.fb.join(',')} | errors ${t.errs.length}`); await t.ctx.close(); }
  // M1 mobile /upis/: banner, accept, form with redirect
  { const t = await ctxFor(true, '/hvala/'); await t.p.goto(S + '/upis/', { waitUntil: 'load' }); await t.p.waitForTimeout(1500);
    const bi = await bannerInfo(t.p); await t.p.tap('#nxt-cc .nxt-cc-yes'); await t.p.waitForTimeout(1500); const n = t.fb.length;
    const link = await t.p.evaluate(() => !![...document.querySelectorAll('a[href="#kolacici-podesavanja"]')].find(x => x.getBoundingClientRect().width > 0));
    await fillSubmit(t.p); await t.p.waitForTimeout(5000);
    out.push(`M1 mobile /upis/ | ${bi} | after accept: ${t.fb.slice(0, n).join(',')} | after form: ${t.fb.slice(n).join(',')} | footer link visible: ${link} | errors ${t.errs.length}`); await t.ctx.close(); }
  console.log(out.join('\n'));
  await b.close();
})();
