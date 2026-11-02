"""Yea Protein one-page budget rules: daily budget per period and campaign type, targets, raise/lower rules.
Reference numbers: Meta campaigns Aug 1 - Nov 1 2026, Google Ads, GA4 weekly orders.
"""
from pathlib import Path
from build2 import CSS

OUT = Path(__file__).parent

CSS6 = CSS + """
  .top{display:flex;justify-content:space-between;align-items:flex-end;padding-top:9mm;border-bottom:2px solid var(--plum);padding-bottom:5px}
  .top h1{font-size:21pt;line-height:1.05;margin-top:3px}
  .top p{font-size:7.6pt;color:var(--ink2);max-width:72mm;text-align:right}
  h2{margin:9px 0 4px}
  table.g td{font-size:7.4pt;padding:4.5px 6px;vertical-align:middle;line-height:1.3}
  table.g th{font-size:6.2pt;padding:4.5px 6px}
  table.g td.n{font-family:Fraunces,serif;font-size:10pt;font-weight:600;color:var(--ink);text-align:right;white-space:nowrap}
  table.g td.tot{font-family:Fraunces,serif;font-size:10pt;font-weight:700;color:var(--plum);text-align:right;background:#f6f2fb}
  table.g td small{display:block;font-size:6.3pt;color:var(--muted);line-height:1.25}
  table.g tr.peak td{background:#fbf6f7} table.g tr.peak td.tot{background:#f3e9f6}
  .ok{color:#2f7d4a;font-weight:800} .hold{color:#8a5a00;font-weight:800} .bad{color:var(--cherry);font-weight:800}
  .rules2{display:grid;grid-template-columns:1fr 1fr;gap:5px 8px}
  .r2{display:grid;grid-template-columns:18px 1fr;gap:6px;background:var(--card);border:1px solid var(--line);border-radius:8px;padding:5px 8px;font-size:7.2pt;color:var(--ink2);line-height:1.35}
  .r2 .k{width:17px;height:17px;border-radius:50%;background:var(--plum);color:#fff;font-weight:800;font-size:7.4pt;display:grid;place-items:center}
  .r2 b{color:var(--ink)}
  .now{background:var(--plum);color:#efeaf8;border-radius:9px;padding:7px 11px;margin-top:8px}
  .now h3{color:#fff;font-size:10.5pt;margin-bottom:3px}
  .now ul{list-style:none;display:grid;grid-template-columns:1fr 1fr;gap:2px 14px;font-size:7.2pt;line-height:1.4}
  .now li::before{content:"→ ";color:#cbb8f0;font-weight:800}
  .now b{color:#fff}
"""

html = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Yea Budget Rules</title>
<link href="fonts/fonts.css" rel="stylesheet"><style>{CSS6}</style></head><body>
<section class="page">
  <div class="top">
    <div><div class="eyebrow">Yea Protein · Meta + Google · from Nov 2026</div><h1>Daily budget rules</h1></div>
    <p>How much to spend per day, by period and campaign type, and when to raise or lower it. Reference numbers are from Aug – Oct 2026.</p>
  </div>

  <h2>1. Daily budget by period <small>starting points · special sales go on top, never instead of Regular</small></h2>
  <table class="g">
    <colgroup><col style="width:30%"><col><col><col><col><col style="width:13%"><col style="width:15%"></colgroup>
    <tr><th>Period</th><th class="r">Regular</th><th class="r">Retargeting</th><th class="r">Google</th><th class="r">Total / day</th><th class="r">Special sale</th><th class="r">Expect orders / week</th></tr>
    <tr><td><b>Off-season</b><small>now – 15 Nov · 7 Jan – 28 Feb · from 3 May</small></td><td class="n">€20</td><td class="n">€5</td><td class="n">€4</td><td class="tot">€29</td><td class="n">+€15–25</td><td class="n">30–40</td></tr>
    <tr><td><b>Pre-season</b><small>16 – 26 Nov · 1 – 14 Mar</small></td><td class="n">€25</td><td class="n">€7</td><td class="n">€5</td><td class="tot">€37</td><td class="n">+€15–25</td><td class="n">35–45</td></tr>
    <tr class="peak"><td><b>Peak</b><small>27 Nov – 13 Dec (Black Friday + fast weeks 1–2) · 15 Mar – 4 Apr (Lent weeks 1–3)</small></td><td class="n">€40</td><td class="n">€10</td><td class="n">€8</td><td class="tot">€58</td><td class="n">+€25–35 <small>Black Friday 4 days</small></td><td class="n">50–80</td></tr>
    <tr><td><b>After peak</b><small>14 Dec – 6 Jan (holidays) · 5 Apr – 1 May (rest of Lent)</small></td><td class="n">€25</td><td class="n">€7</td><td class="n">€5</td><td class="tot">€37</td><td class="n">—</td><td class="n">25–40</td></tr>
  </table>
  <p class="note"><b>Regular</b> = one always-on campaign for the best sellers (Chocolate, Vanilla Caramel, 2× Combos), broad or lookalike audiences. <b>Retargeting</b> = site visitors, cart, and past buyers 25–45 days after their order. <b>Google</b> = Brand all year, plus "posni protein" search in pre-season and peak. Reference: Aug–Sep ran about €33/day on Meta + €6 on Google and brought 30–40 orders a week. Rules can take each number up to <b>1.5× its start</b> before the next period.</p>

  <h2>2. Targets by campaign type <small>Meta cost per purchase, last 7 days, in Ads Manager</small></h2>
  <table class="g">
    <colgroup><col style="width:17%"><col style="width:11%"><col style="width:11%"><col style="width:14%"><col style="width:20%"><col></colgroup>
    <tr><th>Type</th><th class="r">Raise if</th><th class="r">Hold</th><th class="r">Lower if</th><th>Stop when</th><th>Reference now</th></tr>
    <tr><td><b>Regular</b></td><td class="r ok">≤ €18</td><td class="r hold">€18–30</td><td class="r bad">&gt; €30</td><td>An ad spends €40 with 0–1 purchases → turn that ad off</td><td>Broad, Aug–Sep: <b>€24</b>, while all orders cost €7–9</td></tr>
    <tr><td><b>Retargeting</b></td><td class="r ok">≤ €6</td><td class="r hold">€6–10</td><td class="r bad">&gt; €10</td><td>7-day frequency over 3 → new ads, no raise</td><td>Remarketing €2/day: <b>€3.5</b>, but frequency 11</td></tr>
    <tr><td><b>Special sale</b></td><td class="r ok">≤ €10</td><td class="r hold">€10–18</td><td class="r bad">&gt; €18 <small>after 3 days</small></td><td>Over €30 after €100 spent → stop, money back to Regular</td><td>Cherry −1.000 din, Sep: <b class="ok">€10.5</b> ✓ · Cherry + EasyGut, Oct: <b class="bad">€48</b> ✗</td></tr>
    <tr><td><b>Test</b> <small>new angles</small></td><td colspan="3" class="r">fixed €10–15/day for 7 days</td><td>Ad over €40 with 0–1 purchases → off. Winner ≤ €25 → move to Regular</td><td>Angle test, Oct: <b class="bad">€39</b> ✗ (all Sour Cherry)</td></tr>
    <tr class="peak"><td><b>Everything together</b> <small>check this first</small></td><td class="r ok">≤ €10</td><td class="r hold">€10–14</td><td class="r bad">&gt; €14 <small>2 weeks</small></td><td>All ad spend ÷ all WooCommerce orders, per week</td><td>Aug–Sep <b class="ok">€7–9</b> · last week <b class="bad">€27</b></td></tr>
  </table>

  <h2>3. Rules for raising and lowering</h2>
  <div class="rules2">
    <div class="r2"><span class="k">1</span><div><b>When:</b> Regular and Retargeting once a week (Monday, last 7 days). Special sales every 2 days, because they are short.</div></div>
    <div class="r2"><span class="k">2</span><div><b>How much:</b> +20% up or −20% down, one step per check. The only bigger jump is the planned switch on the first day of a period.</div></div>
    <div class="r2"><span class="k">3</span><div><b>Raise only if all 3 are true:</b> the type is in "Raise if", everything together is ≤ €10, and Chocolate + Vanilla Caramel are in stock.</div></div>
    <div class="r2"><span class="k">4</span><div><b>Undo a raise</b> if the next week brings less than 1 extra order per €12 of extra spend. Go back to the last budget that worked.</div></div>
    <div class="r2"><span class="k">5</span><div><b>Special sales:</b> max 14 days, max 40% of total spend, on top of Regular. Lead with best sellers or Combos. A sale on a flavor with ~5% of demand (Sour Cherry) stays at the low end (€15/day).</div></div>
    <div class="r2"><span class="k">6</span><div><b>Stock first:</b> if a best seller is out, Regular drops to €10/day and nothing is raised until it is back. Never advertise what is out.</div></div>
  </div>

  <div class="now">
    <h3>Do this week (2 – 8 Nov) · about €37/day</h3>
    <ul>
      <li><b>Start a Regular campaign at €20/day</b> for Chocolate, Vanilla Caramel and Combos. Nothing always-on has run since late Sep.</li>
      <li><b>Pause the Sour Cherry angle test</b> (€39 per purchase). Its €16/day pays for Regular.</li>
      <li><b>Cherry + EasyGut until 8 Nov:</b> pause Lookalikes (€92 → 1 purchase), keep Sajt i Korpa €5 + Kupci €3.</li>
      <li><b>Remarketing €2 → €5/day</b> with new ads (frequency is 11). Google Brand €4/day.</li>
    </ul>
  </div>

  <div class="foot"><span>Reference: Meta campaigns 1 Aug – 1 Nov 2026 (Meta's own purchase counts, for comparing campaigns), Google Ads, GA4 weekly orders (for the totals).</span><span style="white-space:nowrap">Nov 2026</span></div>
</section>
</body></html>"""

(OUT / "yea_budget_rules.html").write_text(html)
print("built")
