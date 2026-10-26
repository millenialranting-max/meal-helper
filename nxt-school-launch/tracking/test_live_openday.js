// Final pre-publish check: real GTM workspace preview on the LIVE site. Meta /tr requests and form POSTs are intercepted (nothing is sent).
const { chromium, devices } = require('playwright');
let ENV = '&gtm_auth=F39YIXte5K3V37CNYHRDLQ&gtm_preview=env-16&gtm_cookies_win=x';
const S = 'https://nxtschool.edu.rs';
let b, HUA;
async function ctxFor(mobile, redirect) {
  const opt = mobile ? { ...devices['iPhone 13'] } : { viewport: { width: 1366, height: 820 } };
  opt.userAgent = (mobile ? devices['iPhone 13'].userAgent : HUA.replace('HeadlessChrome', 'Chrome'));
  const ctx = await b.newContext(opt); const fb = [], blocked = [];
  await ctx.addInitScript(() => Object.defineProperty(navigator, 'webdriver', { get: () => false }));
  await ctx.route('**/*', async r => { const q = r.request(), u = q.url();
    if (/facebook\.com\/tr/.test(u)) { const m = u + ' ' + (q.postData() || ''); const ev = (m.match(/[?&]ev=([^&\s]+)/) || [])[1]; if (ev) { const cn = decodeURIComponent((m.match(/cd%5Bcontent_name%5D=([^&\s]+)|cd\[content_name\]=([^&\s]+)/) || []).slice(1).find(Boolean) || ''); fb.push(ev + (cn ? '[' + cn + ']' : '')); } return r.fulfill({ status: 200, body: '' }); }
    if (q.method() === 'POST' && /nxtschool\.edu\.rs/.test(u)) {
      if (/admin-ajax\.php/.test(u) && /elementor_pro_forms_send_form/.test(q.postData() || '')) return r.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ success: true, data: { message: 'OK', data: redirect ? { redirect_url: S + redirect } : {} } }) });
      blocked.push(u); return r.abort(); }
    if (ENV && /googletagmanager\.com\/gtm\.js\?id=GTM-5CDGJP32/.test(u) && !/gtm_auth/.test(u)) return r.continue({ url: u + ENV });
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
  const SIM = '/nxt-experience-simultanka-sa-vladimirom-potkinom/';
  async function flow(label, path, redirect, live) {
    ENV = live ? '' : '&gtm_auth=F39YIXte5K3V37CNYHRDLQ&gtm_preview=env-16&gtm_cookies_win=x';
    const t = await ctxFor(false, redirect); await t.p.goto(S + path, { waitUntil: 'load' }); await t.p.waitForTimeout(1500);
    await t.p.click('#nxt-cc .nxt-cc-yes'); await t.p.waitForTimeout(1200); const n = t.fb.length;
    await fillSubmit(t.p); await t.p.waitForTimeout(redirect ? 5000 : 2500);
    out.push(`${label} | after form: ${t.fb.slice(n).join(', ')} | now on ${t.p.url().replace(S, '').slice(0, 40)} | errors ${t.errs.length} | real POSTs blocked ${t.blocked.length}`); await t.ctx.close();
  }
  await flow('LIVE v4 · /open-day/ (redirect na /hvala-open-day/)', '/open-day/', '/hvala-open-day/', true);
  await flow('LIVE v4 · /open-day/ (bez redirekcije)          ', '/open-day/', null, true);
  console.log(out.join('\n'));
  await b.close();
})();
