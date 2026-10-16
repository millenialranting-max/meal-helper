// GA4 check: GTM workspace preview on the LIVE site. Meta /tr and GA4 /g/collect requests and form POSTs are intercepted (nothing is sent).
const { chromium } = require('playwright');
const ENV = process.env.GTM_ENV !== undefined ? process.env.GTM_ENV : '&gtm_auth=42EVsmqYQ952TT9PC6I81g&gtm_preview=env-26&gtm_cookies_win=x';
const RAW = [];
const S = 'https://nxtschool.edu.rs';
let b, HUA;
async function ctxFor(redirect) {
  const ctx = await b.newContext({ viewport: { width: 1366, height: 820 }, userAgent: HUA.replace('HeadlessChrome', 'Chrome') });
  const log = []; let phase = 'before consent';
  await ctx.addInitScript(() => Object.defineProperty(navigator, 'webdriver', { get: () => false }));
  await ctx.route('**/*', async r => { const q = r.request(), u = q.url();
    if (/facebook\.com\/tr/.test(u)) { const ev = ((u + ' ' + (q.postData() || '')).match(/[?&]ev=([^&\s]+)/) || [])[1]; if (ev) log.push([phase, 'Meta ' + ev]); return r.fulfill({ status: 200, body: '' }); }
    if (/google-analytics\.com\/g\/collect|analytics\.google\.com\/g\/collect/.test(u)) {
      const all = u + '\n' + (q.postData() || '');
      RAW.push(phase + ' | ' + all.replace(/\n/g, ' || '));
      all.split(/\n|\r/).forEach(line => { const en = (line.match(/(?:^|[?&])en=([^&\s]+)/) || [])[1]; if (en) { const ft = (line.match(/(?:^|[?&])ep\.form_type=([^&\s]+)/) || [])[1]; const tid = (all.match(/[?&]tid=([^&\s]+)/) || [])[1]; const em = /[?&](em|ecid|_em)=/.test(line) ? ' +user-data' : ''; const gcs = (all.match(/[?&]gcs=([^&\s]+)/) || [])[1], cid = (all.match(/[?&]cid=([^&\s]+)/) || [])[1], dl = decodeURIComponent((all.match(/[?&]dl=([^&\s]+)/) || [])[1] || '').replace(S, ''); log.push([phase, 'GA4 ' + decodeURIComponent(en) + (ft ? '[' + decodeURIComponent(ft) + ']' : '') + ' tid=' + tid + ' consent=' + (gcs === 'G111' ? 'granted' : gcs) + ' cid=' + cid + ' page=' + dl + em]); } });
      return r.fulfill({ status: 204, body: '' }); }
    if (/googletagmanager\.com\/gtag\/js/.test(u)) log.push([phase, 'load gtag.js ' + (u.match(/id=([^&]+)/) || [])[1]]);
    if (q.method() === 'POST' && /nxtschool\.edu\.rs/.test(u)) {
      if (/admin-ajax\.php/.test(u) && /elementor_pro_forms_send_form/.test(q.postData() || '')) return r.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ success: true, data: { message: 'OK', data: redirect ? { redirect_url: S + redirect } : {} } }) });
      return r.abort(); }
    if (ENV && /googletagmanager\.com\/gtm\.js\?id=GTM-5CDGJP32/.test(u) && !/gtm_auth/.test(u)) return r.continue({ url: u + ENV });
    if (/nxtschool\.edu\.rs/.test(u)) return r.continue({ headers: { ...q.headers(), 'user-agent': HUA } });
    return r.continue(); });
  const p = await ctx.newPage(); const errs = []; p.on('pageerror', e => errs.push(e.message));
  return { ctx, p, log, errs, set: v => { phase = v; } };
}
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
  async function flow(label, path, redirect, choice) {
    if (process.env.ONLY && !label.includes(process.env.ONLY)) return;
    const t = await ctxFor(redirect); await t.p.goto(S + path, { waitUntil: 'load' }); await t.p.waitForTimeout(3000);
    t.set(choice === 'no' ? 'after Samo neophodni' : 'after Prihvatam');
    await t.p.click(choice === 'no' ? '#nxt-cc .nxt-cc-no' : '#nxt-cc .nxt-cc-yes'); await t.p.waitForTimeout(2500);
    t.set('after form'); await fillSubmit(t.p); await t.p.waitForTimeout(redirect ? 12000 : 7000); t.log.push(['', 'ended on ' + t.p.url().replace(S, '') + ' · readyState=' + await t.p.evaluate(() => document.readyState).catch(() => '?')]);
    t.set('on leave (flush)'); await t.p.goto('about:blank').catch(() => {}); await t.p.waitForTimeout(1500);
    out.push(`\n## ${label} (errors ${t.errs.length})\n` + (t.log.length ? t.log.map(([ph, x]) => `  ${ph.padEnd(22)} ${x}`).join('\n') : '  (no Google/Meta requests)'));
    await t.ctx.close();
  }
  await flow('/upis/ (sa UTM) · Prihvatam · form redirects to /hvala/', '/upis/?utm_source=fb&utm_medium=paid_social&utm_campaign=nxt_upis_2026&utm_content=test', '/hvala/');
  await flow('/open-day/ · Prihvatam · redirect', '/open-day/', '/hvala-open-day/');
  await flow('simultanka · Prihvatam · no redirect', '/nxt-experience-simultanka-sa-vladimirom-potkinom/', null);
  await flow('/upis/ · Samo neophodni', '/upis/', '/hvala/', 'no');
  console.log(out.join('\n'));
  if (process.env.RAW_OUT) require('fs').writeFileSync(process.env.RAW_OUT, RAW.join('\n\n'));
  await b.close();
})();
