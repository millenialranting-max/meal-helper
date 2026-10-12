# NXT · Meta Pixel + Lead u GTM-u (GTM-5CDGJP32)

Pixel: **1732336671184657** · Stranica: https://nxtschool.edu.rs/upis/

**Šta se dobija:**
- Pixel se pali tek kad posetilac klikne „Prihvatam“ u cookie banneru. Banner je već ugrađen u sajt, ali je trenutno uspavan; GTM ga budi.
- **Lead** se šalje kad je Elementor forma uspešno poslata: odmah ako nema redirekcije, ili na sledećoj stranici (npr. /hvala) ako je ima.
- Ako neko direktno otvori /hvala, Lead se ne broji.
- Svaki Lead ima `eventID`, pa kasnije CAPI može da se doda bez duplih konverzija.

> Pre početka: u skripti sajta (`CFG = { ga4: "", pixel: "" }`) **ostavi pixel prazan** i ne dodaj pixel ni preko plugina, inače će događaji biti duplirani. Proveri i da u GTM-u već ne postoji neki Meta Pixel tag.

## 1. Varijable (Variables → User-Defined Variables → New)

| Ime | Tip | Vrednost |
|---|---|---|
| `const - Meta Pixel ID` | Constant | `1732336671184657` |
| `cjs - NXT consent` | Custom JavaScript | `function(){ try { return localStorage.getItem('nxt_consent_v1'); } catch(e) { return null; } }` |
| `dlv - nxt_consent` | Data Layer Variable | `nxt_consent` |
| `dlv - nxt_event_id` | Data Layer Variable | `nxt_event_id` |
| `dlv - nxt_form_type` | Data Layer Variable | `nxt_form_type` |

## 2. Okidači (Triggers → New)

| Ime | Tip | Uslov |
|---|---|---|
| `DOM Ready - All pages` | DOM Ready | All DOM Ready Events |
| `Page View - consent granted` | Page View | Some Page Views: `cjs - NXT consent` **equals** `1` |
| `CE - nxt_consent granted` | Custom Event, event name `nxt_consent` | Some Custom Events: `dlv - nxt_consent` **equals** `1` |
| `CE - nxt_lead` | Custom Event, event name `nxt_lead` | Some Custom Events: `cjs - NXT consent` **equals** `1` |

## 3. Tagovi (Tags → New → Custom HTML)

**Tag 1 · `cHTML - NXT consent + form listener`**
- Okidač: `DOM Ready - All pages`
- Advanced Settings → Tag firing options: **Once per page**

```html
<style>
/* NXT cookie banner: bigger, clearer, "Prihvatam" as the main action (desktop + mobile). "Samo neophodni" stays visible. */
html body #nxt-cc{left:50%!important;right:auto!important;bottom:24px!important;transform:translateX(-50%);width:calc(100% - 32px);max-width:680px!important;margin:0!important;padding:28px 30px 26px!important;border-radius:24px!important;border:0!important;font-size:16px!important;line-height:1.55!important;color:#334155!important;
  box-shadow:0 0 0 100vmax rgba(15,23,42,.32),0 30px 80px -20px rgba(15,23,42,.6)!important;animation:nxtccIn .45s cubic-bezier(.2,.9,.3,1.15) both}
html body #nxt-cc::before{content:"";position:absolute;left:0;right:0;top:0;height:6px;border-radius:24px 24px 0 0;background:linear-gradient(90deg,#007BFF,#7A5CFF)}
html body #nxt-cc p{margin:0 0 20px!important}
html body #nxt-cc strong{display:block;font-size:21px!important;color:#0F172A!important;margin-bottom:8px!important}
html body #nxt-cc strong::before{content:"\1F36A  "}
html body #nxt-cc div{display:flex!important;flex-direction:row!important;flex-wrap:nowrap!important;justify-content:stretch!important;gap:12px!important}
html body #nxt-cc button{margin:0!important;border-radius:999px!important;cursor:pointer;transition:transform .15s,filter .15s}
html body #nxt-cc .nxt-cc-no{flex:1 1 0;font-size:15px!important;font-weight:600!important;padding:15px 18px!important;color:#475569!important;background:#fff!important;border:1px solid #CBD5E1!important}
html body #nxt-cc .nxt-cc-yes{flex:2 1 0;font-size:18px!important;font-weight:800!important;padding:17px 24px!important;color:#fff!important;border:0!important;background:linear-gradient(90deg,#007BFF,#7A5CFF)!important;
  box-shadow:0 14px 30px -10px rgba(0,123,255,.75);animation:nxtccPulse 1.6s ease-out 1.2s 2}
html body #nxt-cc .nxt-cc-yes::before{content:"\2713  "}
html body #nxt-cc .nxt-cc-yes:hover{filter:brightness(1.08);transform:translateY(-1px)}
@keyframes nxtccIn{from{opacity:0;transform:translate(-50%,40px)}to{opacity:1;transform:translate(-50%,0)}}
@keyframes nxtccPulse{0%{box-shadow:0 14px 30px -10px rgba(0,123,255,.75),0 0 0 0 rgba(122,92,255,.55)}100%{box-shadow:0 14px 30px -10px rgba(0,123,255,.75),0 0 0 16px rgba(122,92,255,0)}}
@media (max-width:600px){html body #nxt-cc{bottom:12px!important;padding:22px 20px 18px!important;font-size:15px!important}html body #nxt-cc strong{font-size:19px!important}html body #nxt-cc div{flex-direction:column-reverse!important}html body #nxt-cc button{width:100%;flex:none}}
</style>
<script>
/* NXT | Consent + form listener (GTM Custom HTML, DOM Ready, all pages).
   1) shows the site's own cookie banner (it stays hidden while the site script has no pixel ID),
   2) pushes the visitor's choice to the dataLayer,
   3) pushes nxt_lead when the Elementor form is sent: right away, or on the next page if the form redirects (thank-you page). */
(function () {
  var KEY = 'nxt_consent_v1', dl = window.dataLayer = window.dataLayer || [];
  function get(k, store) { try { return (store || localStorage).getItem(k); } catch (e) { return null; } }

  // Banner copy (also applied when the banner is reopened from "Podešavanja kolačića")
  function customize() {
    var d = document.getElementById('nxt-cc'); if (!d || d.getAttribute('data-nxt')) return;
    d.setAttribute('data-nxt', '1');
    var p = d.querySelector('p');
    if (p) p.innerHTML = '<strong>Da li prihvatate kolačiće?</strong>Koristimo kolačiće da bi sajt ispravno radio i, uz vašu saglasnost, za analitiku, unapređenje sadržaja i merenje oglasa. <a href="/politika-privatnosti/#kolacici">Saznajte više</a>';
    var y = d.querySelector('[data-a="1"]'), n = d.querySelector('[data-a="0"]');
    if (y) y.textContent = 'Prihvatam'; if (n) n.textContent = 'Samo neophodni';
  }
  if (get(KEY) === null && window.nxtConsent && window.nxtConsent.open) window.nxtConsent.open();
  customize();
  if (window.MutationObserver) new MutationObserver(customize).observe(document.body, { childList: true });

  // /upis/ uses a short footer without "Podešavanja kolačića": add the link next to "Politika privatnosti"
  var pol = document.querySelector('.paid-footer a[href*="politika-privatnosti"]');
  if (pol && !document.querySelector('.paid-footer a[href="#kolacici-podesavanja"]')) {
    var cl = document.createElement('a'); cl.href = '#kolacici-podesavanja'; cl.textContent = 'Podešavanja kolačića';
    pol.parentNode.insertBefore(cl, pol.nextSibling);
  }
  document.addEventListener('click', function (e) {
    var a = e.target && e.target.closest && e.target.closest('.paid-footer a[href="#kolacici-podesavanja"]');
    if (a && window.nxtConsent) { e.preventDefault(); window.nxtConsent.open(); }
  });

  document.addEventListener('click', function (e) {
    var b = e.target && e.target.closest && e.target.closest('#nxt-cc [data-a]');
    if (b) setTimeout(function () { dl.push({ event: 'nxt_consent', nxt_consent: b.getAttribute('data-a') }); }, 0);
  }, true);

  var pending = get('nxt_lead_pending', sessionStorage);
  if (pending) {
    try { sessionStorage.removeItem('nxt_lead_pending'); } catch (e) {}
    var p = pending.split('|');
    dl.push({ event: 'nxt_lead', nxt_event_id: p[0], nxt_form_type: p[1] || 'prijava' });
  }

  if (window.jQuery) jQuery(document).on('submit_success', function (e, resp) {
    var f = e.target, t = f && f.querySelector ? f.querySelector('[name="form_fields[form_type]"]') : null;
    var type = (t && t.value) || 'prijava';
    var id = 'lead.' + Date.now() + '.' + Math.random().toString(36).slice(2, 10);
    var redirect = resp && resp.data && resp.data.redirect_url;
    if (redirect) { try { sessionStorage.setItem('nxt_lead_pending', id + '|' + type); return; } catch (x) {} }
    dl.push({ event: 'nxt_lead', nxt_event_id: id, nxt_form_type: type });
  });
})();
</script>
```

**Tag 2 · `Meta Pixel - Base (PageView)`**
- Okidači: `Page View - consent granted` **i** `CE - nxt_consent granted`
- Advanced Settings → Tag firing options: **Once per page**

```html
<script>
/* Meta Pixel | Base + PageView. Fires only with marketing consent (see triggers). */
!function(f,b,e,v,n,t,s){if(f.fbq)return;n=f.fbq=function(){n.callMethod?n.callMethod.apply(n,arguments):n.queue.push(arguments)};if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';n.queue=[];t=b.createElement(e);t.async=!0;t.src=v;s=b.getElementsByTagName(e)[0];s.parentNode.insertBefore(t,s)}(window,document,'script','https://connect.facebook.net/en_US/fbevents.js');
fbq('init', {{const - Meta Pixel ID}});
fbq('track', 'PageView');
</script>
```

**Tag 3 · `Meta Pixel - Lead`**
- Okidač: `CE - nxt_lead`
- Advanced Settings → Tag Sequencing: ✔ *Fire a tag before Meta Pixel - Lead fires* → `Meta Pixel - Base (PageView)`

```html
<script>
/* Meta Pixel | Lead (form "prijava") or CompleteRegistration (Open Day form). eventID is kept for CAPI deduplication later. */
(function () {
  if (!window.fbq) return;
  var type = {{dlv - nxt_form_type}} || 'prijava';
  var name = type.indexOf('open') > -1 ? 'CompleteRegistration' : 'Lead';
  fbq('track', name, { content_name: type }, { eventID: {{dlv - nxt_event_id}} });
})();
</script>
```

## 4. Test pre objave

1. GTM → **Preview** → otvori `https://nxtschool.edu.rs/upis/`.
2. Treba da se pojavi cookie banner. Klikni **Prihvatam** → u Tag Assistant-u se pali `Meta Pixel - Base`. Chrome ekstenzija *Meta Pixel Helper* treba da prikaže PageView.
3. Pošalji jednu test prijavu (u ime upiši „TEST“ i javi klijentu da je obriše) → pali se `Meta Pixel - Lead` (na /hvala, ako forma radi redirekciju).
4. Uporedo otvori Events Manager → **Test events** da vidiš PageView i Lead uživo.
5. Klikni „Samo neophodni“ u novom inkognito prozoru → ne sme da se upali nijedan Meta tag.

## 5. Objava i Meta podešavanja

1. GTM → **Submit → Publish**, verzija „Meta Pixel + Lead (consent)“.
2. Events Manager → pixel → Settings: uključi **Automatic advanced matching** (bolje uparivanje konverzija).
3. Business Settings → Brand safety → **Domains**: verifikuj `nxtschool.edu.rs` (preporuka).
4. U kampanjama: optimizacija na **Lead**, na ovom pixelu.

Napomena: posle objave cookie banner (uvećan, centriran, blago zatamnjenje, novi tekst „Da li prihvatate kolačiće?“, „✓ Prihvatam“ kao glavno dugme; vidi `cookie_banner_preview.jpg`) će se prikazivati na celom sajtu. To je ispravno; bez pristanka pixel se ne pali.
