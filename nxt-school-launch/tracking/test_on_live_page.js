// Emulates the 3 GTM tags + triggers on the LIVE page. Meta requests and form POSTs are intercepted (nothing leaves).
const { chromium } = require('playwright');
const fs = require('fs');
const T = '/home/user/meal-helper/nxt-school-launch/tracking/';
const strip = s => s.replace(/<\/?script>/g, '');
const A = strip(fs.readFileSync(T + 'tagA_consent_form_listener.html', 'utf8'));
const B = strip(fs.readFileSync(T + 'tagB_meta_pixel_base.html', 'utf8')).replace("'{{const - Meta Pixel ID}}'", "'1732336671184657'");
const C = strip(fs.readFileSync(T + 'tagC_meta_pixel_lead.html', 'utf8')).replace('{{dlv - nxt_form_type}}', 'ev.nxt_form_type').replace('{{dlv - nxt_event_id}}', 'ev.nxt_event_id');
const EMU = `document.addEventListener('DOMContentLoaded', function () { setTimeout(function () {
  window.dataLayer = window.dataLayer || [];
  function consent() { try { return localStorage.getItem('nxt_consent_v1'); } catch (e) { return null; } }
  var baseFired = false; function base() { if (baseFired) return; baseFired = true; ${B} }
  function lead(ev) { if (consent() !== '1') return; base(); ${C} }
  var orig = dataLayer.push; dataLayer.push = function (o) { var r = orig.apply(this, arguments);
    if (o && o.event === 'nxt_consent' && o.nxt_consent === '1') base(); if (o && o.event === 'nxt_lead') lead(o); return r; };
  if (consent() === '1') base();   // trigger: Page View + consent = 1
  ${A}                              // trigger: DOM Ready
}, 50); });`;
const URL = 'https://nxtschool.edu.rs/nxt-school-paid/';
async function run(name, { redirect, accept, direct }) {
  const b = await chromium.launch(); const HUA = (await (await b.newPage()).evaluate(() => navigator.userAgent)); const ctx = await b.newContext({ userAgent: HUA.replace('HeadlessChrome', 'Chrome') });
  await ctx.addInitScript(() => Object.defineProperty(navigator, 'webdriver', { get: () => false })); const fb = []; const blocked = [];
  await ctx.route('**/*', async r => {
    const q = r.request(), u = q.url();
    if (/facebook\.com\/tr/.test(u)) { const m = (u + ' ' + (q.postData() || '')); fb.push(((m.match(/[?&]ev=([^&\s]+)/) || [])[1] || '?') + ' id=' + ((m.match(/[?&]id=(\d+)/) || [])[1]) + ' eid=' + ((m.match(/[?&]eid=([^&\s]+)/) || [])[1] || '-')); return r.fulfill({ status: 200, body: '' }); }
    if (q.method() === 'POST' && /nxtschool\.edu\.rs/.test(u)) {
      if (/admin-ajax\.php/.test(u) && /elementor_pro_forms_send_form/.test(q.postData() || ''))
        return r.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ success: true, data: { message: 'OK', data: redirect ? { redirect_url: 'https://nxtschool.edu.rs/hvala/' } : {} } }) });
      blocked.push(u); return r.abort();
    }
    if (/nxtschool\.edu\.rs/.test(u)) return r.continue({ headers: { ...q.headers(), 'user-agent': HUA } });
    return r.continue();
  });
  await ctx.addInitScript(EMU);
  const p = await ctx.newPage(); const errs = []; p.on('pageerror', e => errs.push(e.message));
  if (direct) { await p.goto('https://nxtschool.edu.rs/'); await p.evaluate(() => localStorage.setItem('nxt_consent_v1', '1')); await p.goto('https://nxtschool.edu.rs/hvala/'); await p.waitForTimeout(2500);
    console.log(name, '| fb:', fb.join(' ; ') || 'none', '| errors:', errs.length); await b.close(); return; }
  await p.goto(URL, { waitUntil: 'load' }); await p.waitForTimeout(1500);
  const banner = await p.evaluate(() => { const d = document.getElementById('nxt-cc'); return !!d && !d.hidden; });
  const before = fb.length;
  await p.click(accept ? '#nxt-cc [data-a="1"]' : '#nxt-cc [data-a="0"]'); await p.waitForTimeout(2000);
  const afterConsent = fb.slice(before).join(' ; ') || 'none';
  // fill the form with dummy data (the POST is intercepted)
  await p.evaluate(() => { const f = document.querySelector('.nxt-form form');
    f.querySelectorAll('input:not([type=hidden]):not([type=checkbox]), textarea').forEach(i => { i.value = i.type === 'email' ? 'test@example.com' : (i.type === 'tel' ? '0601234567' : 'Test'); });
    f.querySelectorAll('select').forEach(s => { if (s.options.length > 1) s.selectedIndex = 1; });
    f.querySelectorAll('input[type=checkbox]').forEach(c => c.checked = true); });
  const n0 = fb.length;
  await p.click('.nxt-form button[type=submit]'); await p.waitForTimeout(redirect ? 5000 : 2500);
  console.log(name, '| banner shown:', banner, '| after consent:', afterConsent, '| after submit:', fb.slice(n0).join(' ; ') || 'none', '| url:', p.url().replace('https://nxtschool.edu.rs', ''), '| blocked POSTs:', blocked.length, '| errors:', errs.length, errs.slice(0, 2).join(' / '));
  await b.close();
}
(async () => {
  await run('S1 accept + form (no redirect)', { accept: true, redirect: false });
  await run('S2 accept + form (redirect to /hvala)', { accept: true, redirect: true });
  await run('S3 reject + form', { accept: false, redirect: true });
  await run('S4 direct /hvala visit (consent=1)', { direct: true });
})();
