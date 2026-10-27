"""Builds two one-pagers for Yea Protein:
  yea_budget_lp.html  - ad budget the stock can carry + landing pages
  yea_calendar.html   - which ads run when, with which offer and landing page
Data: Yea GA4 + Meta Ads (Sep 2025 - Oct 2026), live yeaprotein.rs catalog (27 Oct 2026).
"""
from pathlib import Path

OUT = Path(__file__).parent
PLUM, GRAY, INK, INK2, MUTED, CHERRY = "#5b3fa0", "#d6d0de", "#1f1a2e", "#4d475c", "#847e92", "#a3263b"

CSS = """
  :root{--ink:#1f1a2e;--ink2:#4d475c;--muted:#847e92;--bg:#fbf8f3;--card:#fff;--line:#e9e3da;
    --plum:#5b3fa0;--plum-soft:#efeaf8;--cherry:#a3263b;--cherry-soft:#f9e6e9;--good:#2f7d4a;--good-soft:#e5f3ea;--amber:#8a5a00;--amber-soft:#fbf1dc}
  @page{size:A4;margin:0} *{box-sizing:border-box;margin:0;padding:0} html,body{background:var(--bg)}
  body{font-family:Inter,system-ui,sans-serif;color:var(--ink);font-size:7.6pt;line-height:1.34;-webkit-print-color-adjust:exact;print-color-adjust:exact}
  .page{width:210mm;height:297mm;position:relative;overflow:hidden;padding:0 11mm 10mm;background:var(--bg)}
  h1,h2,h3{font-family:Fraunces,Georgia,serif;font-weight:600;letter-spacing:-.01em}
  .eyebrow{font-size:6.8pt;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:var(--plum)}
  .hero{margin:0 -11mm;height:27mm;background:url(img/hero.jpg) right 55%/cover no-repeat;position:relative}
  .hero::before{content:"";position:absolute;inset:0;background:linear-gradient(90deg,rgba(251,248,243,.97) 0%,rgba(251,248,243,.9) 50%,rgba(251,248,243,0) 66%)}
  .hero .txt{position:absolute;left:11mm;top:5.5mm;width:118mm}
  .hero h1{font-size:20pt;line-height:1.05;margin:3px 0 3px}
  .hero p{font-size:8pt;color:var(--ink2)}
  h2{font-size:11.5pt;margin:7px 0 4px;display:flex;align-items:baseline;gap:8px}
  h2 small{font-family:Inter;font-size:6.9pt;color:var(--muted);font-weight:500}
  h3{font-size:9.5pt;margin-bottom:3px}
  .card{background:var(--card);border:1px solid var(--line);border-radius:9px;padding:7px 9px}
  .card svg{width:100%;height:auto;display:block;font-family:Inter,sans-serif}
  .grid2{display:grid;grid-template-columns:1.12fr 1fr;gap:7px}
  .formula{background:var(--plum);color:#efeaf8;border-radius:9px;padding:7px 10px;font-size:7.6pt}
  .formula b{color:#fff;font-size:8.6pt;display:block;margin-bottom:2px;font-family:Fraunces,serif;font-weight:600}
  .formula code{font-family:Inter;font-weight:700;color:#fff;background:rgba(255,255,255,.14);border-radius:4px;padding:1px 5px}
  .tiles{display:grid;grid-template-columns:repeat(3,1fr);gap:5px;margin-top:5px}
  .tile{background:var(--card);border:1px solid var(--line);border-radius:8px;padding:5px 7px}
  .tile .v{font-family:Fraunces,serif;font-size:13.5pt;font-weight:600;color:var(--plum);line-height:1.1}
  .tile .s{font-size:6.8pt;color:var(--ink2)}
  table{width:100%;border-collapse:separate;border-spacing:0;background:var(--card);border:1px solid var(--line);border-radius:9px;overflow:hidden}
  th{font-size:6.2pt;text-transform:uppercase;letter-spacing:.06em;color:var(--muted);text-align:left;padding:4px 6px;background:#f7f3ec;font-weight:700}
  td{padding:3.5px 6px;border-top:1px solid var(--line);font-size:7.2pt;color:var(--ink2);vertical-align:top}
  td b{color:var(--ink)} td.r,th.r{text-align:right} tr.tot td{background:#faf7f2;font-weight:700;color:var(--ink)}
  tr.peak td:first-child{box-shadow:inset 3px 0 0 var(--plum)}
  .pill{display:inline-block;border-radius:4px;padding:0 5px;font-size:6.4pt;font-weight:800;letter-spacing:.03em}
  .pill.ok{background:var(--good-soft);color:var(--good)} .pill.no{background:var(--cherry-soft);color:var(--cherry)} .pill.q{background:var(--amber-soft);color:var(--amber)}
  .note{font-size:6.8pt;color:var(--muted);margin-top:4px;line-height:1.35}
  .callout{border-radius:8px;padding:5px 8px;font-size:7.1pt;margin-top:5px;line-height:1.35}
  .callout.amber{background:var(--amber-soft);color:#5c4a1c} .callout.amber b{color:#8a5a00}
  .callout.cherry{background:var(--cherry-soft);color:#6b1c2a} .callout.cherry b{color:var(--cherry)}
  .wire{display:grid;grid-template-columns:50mm 1fr;gap:9px;align-items:start}
  .phone{border:2px solid #cfc7dc;border-radius:12px;padding:5px;background:#fff;position:relative}
  .blk{border-radius:5px;padding:2.5px 5px;margin-bottom:2.5px;font-size:6.2pt;line-height:1.25;color:var(--ink2);background:#f6f2fb;border:1px dashed #d9cfe9}
  .blk b{color:var(--ink);font-size:6.4pt}
  .blk.top{background:var(--plum);color:#efeaf8;border:0} .blk.top b{color:#fff;display:inline}
  .sticky{background:var(--cherry);color:#fff;border-radius:5px;text-align:center;font-weight:800;font-size:6.6pt;padding:3px}
  ul.tight{padding-left:11px} ul.tight li{font-size:7.2pt;color:var(--ink2);margin-bottom:2px} ul.tight li b{color:var(--ink)}
  .foot{position:absolute;left:11mm;right:11mm;bottom:6mm;font-size:6.3pt;color:var(--muted);display:flex;justify-content:space-between;border-top:1px solid var(--line);padding-top:4px}
  /* calendar */
  .head2{padding-top:8mm;display:flex;justify-content:space-between;align-items:flex-end;border-bottom:1px solid var(--line);padding-bottom:5px}
  .head2 h1{font-size:20pt}
  table.cal td{font-size:7pt;padding:4px 5px;line-height:1.3}
  table.cal td.when b{display:block;font-family:Fraunces,serif;font-size:8.6pt;font-weight:600}
  table.cal td.bud{font-weight:800;color:var(--plum);white-space:nowrap;font-size:7.6pt}
  .num{display:inline-grid;place-items:center;width:15px;height:15px;border-radius:50%;background:var(--plum);color:#fff;font-size:6.8pt;font-weight:800;margin-bottom:2px}
  .num.base{background:#b9b1c9}
  .lanes{display:grid;grid-template-columns:repeat(3,1fr);gap:6px;margin-top:6px}
  .lane{background:var(--card);border:1px solid var(--line);border-radius:9px;padding:6px 8px;border-top:3px solid var(--plum)}
  .lane.c{border-top-color:var(--cherry)} .lane.g{border-top-color:var(--good)}
  .lane b{display:block;font-size:6.8pt;letter-spacing:.1em;text-transform:uppercase;margin-bottom:2px}
  .lane.c b{color:var(--cherry)} .lane.g b{color:var(--good)} .lane b{color:var(--plum)}
  .lane p{font-size:7.1pt;color:var(--ink2)}
"""


def page(body, title):
    return (f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>{title}</title>'
            f'<link href="fonts/fonts.css" rel="stylesheet"><style>{CSS}</style></head><body>{body}</body></html>')


def t(x, y, s, size=8, fill=INK2, anchor="start", weight=400):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" font-weight="{weight}">{s}</text>'


# ---------- landing page chart: revenue per Meta visit (RSD), Nov 2025 - Oct 2026 ----------
def chart_lp():
    rows = [("2× Combo 500g page", 114, "2.8% buy · 599 visits", "best"),
            ("2× Combo 1kg page", 94, "1.7% buy · 1,605 visits", "best"),
            ("1kg product page", 81, "1.7% buy · 3,455 visits", "ok"),
            ("/shop", 75, "1.8% buy · 16,838 visits", "ok"),
            ("500g product page", 72, "2.0% buy · 5,133 visits", "ok"),
            ("Homepage", 54, "1.4% buy · 7,686 visits", "bad"),
            ("3× Combo pages", 28, "0.6% buy · 636 visits", "bad")]
    lx, bx, bmax, rh, y0 = 104, 110, 140, 15.5, 3
    s = []
    for i, (lab, v, sub, k) in enumerate(rows):
        y = y0 + i * rh
        w = v / 114 * bmax
        col = PLUM if k == "best" else (CHERRY if k == "bad" else GRAY)
        s.append(t(lx, y + 10.5, lab, 7.8, INK if k != "ok" else INK2, "end", 600 if k != "ok" else 400))
        s.append(f'<path d="M{bx},{y+2} L{bx+w-3},{y+2} Q{bx+w},{y+2} {bx+w},{y+5} L{bx+w},{y+11} Q{bx+w},{y+14} {bx+w-3},{y+14} L{bx},{y+14} Z" fill="{col}"/>')
        s.append(t(bx + w + 4, y + 11, f"{v} RSD", 7.8, INK, "start", 700))
        s.append(t(360, y + 11, sub, 7, MUTED, "end"))
    return f'<svg viewBox="0 0 362 {y0 + len(rows) * rh + 2}" role="img" aria-label="Revenue per visit from Meta ads by landing page">{"".join(s)}</svg>'


# ---------- calendar strip ----------
PH = [(1, "27 Oct", 24, 25, False), (2, "20 Nov", 7, 25, False), (3, "BF", 4, 90, True), (4, "1 Dec", 37, 80, True),
      (5, "7 Jan", 53, 30, False), (6, "1 Mar", 14, 50, False), (7, "15 Mar", 21, 100, True), (8, "5 Apr", 27, 60, True), (9, "2 May", 30, 30, False)]


def strip():
    W, x0, x1, yb, yt = 700, 6, 694, 88, 38
    total = sum(p[2] for p in PH)
    sx = (x1 - x0) / total
    y = lambda v: yb - v / 100 * (yb - yt)
    s, x = [], x0
    for n, d, days, eur, peak in PH:
        w = days * sx
        if n == 2:  # ramp: 20-23 Nov at 25, 24-26 Nov at 80
            pass
        s.append(f'<rect x="{x+1}" y="{y(eur)}" width="{w-2}" height="{yb-y(eur)}" rx="3" fill="{PLUM if peak else GRAY}"/>')
        cx = x + w / 2
        s.append(f'<circle cx="{cx}" cy="{y(eur)-11}" r="6.5" fill="{PLUM if peak else "#b9b1c9"}"/>')
        s.append(t(cx, y(eur) - 8.5, str(n), 7.4, "#fff", "middle", 800))
        if w > 30:
            s.append(t(cx, yb - 4, f"€{eur}", 7.6, "#fff" if peak else INK2, "middle", 700))
        x += w
    s.append(f'<line x1="{x0}" x2="{x1}" y1="{yb}" y2="{yb}" stroke="{MUTED}"/>')
    for d, m in [(5, "Nov"), (35, "Dec"), (66, "Jan"), (97, "Feb"), (125, "Mar"), (156, "Apr"), (186, "May")]:
        xx = x0 + d * sx
        s.append(f'<line x1="{xx}" x2="{xx}" y1="{yb}" y2="{yb+4}" stroke="{MUTED}"/>')
        s.append(t(xx + 2, yb + 12, m, 7.2, MUTED))
    for d, lab in [(31, "BF 27 Nov · fast 28 Nov"), (139, "Lent 15 Mar"), (187, "Easter 2 May")]:
        xx = x0 + d * sx
        s.append(f'<line x1="{xx}" x2="{xx}" y1="3" y2="{yb}" stroke="{CHERRY}" stroke-dasharray="2 2"/>')
        s.append(t(xx + 3, 9, lab, 7, CHERRY, "start", 700))
    return f'<svg viewBox="0 0 {W} 102" role="img" aria-label="Campaign phases and Meta budget per day">{"".join(s)}</svg>'


# =================== PAGE 1: budget by stock + landing pages ===================
p1 = f"""
<section class="page">
  <div class="hero"><div class="txt">
    <div class="eyebrow">Yea Protein · Nov 2026 – May 2027</div>
    <h1>Budget by stock &amp; landing pages</h1>
    <p>How much ad money the stock can carry, and where every ad should send people.</p>
  </div></div>

  <h2>How much ad budget the stock can carry <small>rough model, built from last year's sales</small></h2>
  <div class="grid2">
    <div>
      <div class="formula"><b>The rule</b>
        Max ad budget for a period = <code>(units in stock ÷ units per order − orders you get without ads) × cost per extra order</code></div>
      <div class="tiles">
        <div class="tile"><div class="v">€470</div><div class="s">of ads per 100 units in <b>Lent</b> (€7 per extra order)</div></div>
        <div class="tile"><div class="v">€800</div><div class="s">per 100 units in <b>Božićni post</b> (€12 per extra order)</div></div>
        <div class="tile"><div class="v">€1,300</div><div class="s">per 100 units <b>off-season</b> (€15 per extra order)</div></div>
      </div>
      <h3 style="margin-top:7px">Units the budget calendar needs</h3>
      <table>
        <tr><th>Phase</th><th class="r">€/day</th><th class="r">Ad spend</th><th class="r">Orders</th><th class="r">Units</th></tr>
        <tr><td>Restock + test · 27 Oct – 23 Nov</td><td class="r">25</td><td class="r">€700</td><td class="r">~100</td><td class="r">~120</td></tr>
        <tr class="peak"><td><b>BF + Božićni post</b> · 24 Nov – 6 Jan</td><td class="r">80</td><td class="r">€3,520</td><td class="r">~380</td><td class="r"><b>~570</b></td></tr>
        <tr><td>Baseline · 7 Jan – 28 Feb</td><td class="r">30</td><td class="r">€1,590</td><td class="r">~210</td><td class="r">~240</td></tr>
        <tr><td>Pre-Lent · 1 – 14 Mar</td><td class="r">50</td><td class="r">€700</td><td class="r">~100</td><td class="r">~140</td></tr>
        <tr class="peak"><td><b>Lent weeks 1–3</b> · 15 Mar – 4 Apr</td><td class="r">100</td><td class="r">€2,100</td><td class="r">~340</td><td class="r"><b>~510</b></td></tr>
        <tr class="peak"><td><b>Rest of Lent</b> · 5 Apr – 1 May</td><td class="r">60</td><td class="r">€1,620</td><td class="r">~290</td><td class="r"><b>~430</b></td></tr>
        <tr><td>After Easter · May</td><td class="r">30</td><td class="r">€900</td><td class="r">~120</td><td class="r">~140</td></tr>
        <tr class="tot"><td>Total, 7 months</td><td></td><td class="r">€11,130</td><td class="r">~1,540</td><td class="r">~2,150</td></tr>
      </table>
    </div>
    <div>
      <h3>Units needed per flavor vs stock today</h3>
      <table>
        <tr><th>Flavor</th><th class="r">Share</th><th class="r">Nov–May</th><th>In stock now</th></tr>
        <tr><td><b>Vanilla Caramel</b></td><td class="r">34%</td><td class="r"><b>~740</b></td><td><span class="pill q">500g + 1kg · qty ?</span></td></tr>
        <tr><td><b>Chocolate</b></td><td class="r">24%</td><td class="r"><b>~520</b></td><td><span class="pill q">1kg only · qty ?</span></td></tr>
        <tr><td>Neutral</td><td class="r">14%</td><td class="r">~300</td><td><span class="pill no">out</span></td></tr>
        <tr><td>Vanilla Cherry</td><td class="r">13%</td><td class="r">~280</td><td><span class="pill no">out</span></td></tr>
        <tr><td>Strawberry</td><td class="r">10%</td><td class="r">~220</td><td><span class="pill q">500g · qty ?</span></td></tr>
        <tr><td>Sour Cherry</td><td class="r">4.5%</td><td class="r">~100</td><td><span class="pill ok">500g · 141</span></td></tr>
      </table>
      <div class="callout amber"><b>Only Sour Cherry shows a quantity.</b> Turn on stock tracking for every flavor in WooCommerce, then use the rule above before each phase. If Chocolate + Vanilla Caramel can't cover ~60% of a phase's units, lower that phase's budget to what stock carries.</div>
      <div class="callout cherry"><b>Sour Cherry is leaving the range:</b> 141 units is ~1.4× its whole Nov–May demand. Keep the EasyGut-gift offer to 8 Nov, then sell the rest in a mixed 2×500g with Vanilla Caramel. Never make it the main ad.</div>
      <p class="note">Assumptions: ~60 orders a month without ads · 1.15 units per order (1.5 when Combos are on) · cost per extra order from Lent 2026 and Aug–Oct 2025 vs 2026 · flavor shares from Sep 2025 – Mar 2026 sales. Confirm against margin.</p>
    </div>
  </div>

  <h2>Landing pages <small>where ads lead, and what the page needs</small></h2>
  <div class="grid2">
    <div class="card">
      <h3>Revenue per visit from Meta ads, by page <small style="font-family:Inter;font-weight:500;color:var(--muted);font-size:6.8pt">Nov 2025 – Oct 2026</small></h3>
      {chart_lp()}
      <p class="note">2× Combo pages earn the most per visit; the homepage and 3× packs the least. The old Combo pages now return 404, so rebuild them before any Combo ad runs.</p>
    </div>
    <div>
      <table>
        <tr><th>Ad type</th><th>Send to</th></tr>
        <tr><td><b>Combo / offer ads</b></td><td>The 2× Combo page (rebuild: 2×1kg and 2×500g, pick any two flavors)</td></tr>
        <tr><td><b>One-flavor ads</b></td><td>Product page with the flavor pre-selected: <code style="font-size:6.6pt">/proizvod/yea-protein-1kg/?attribute_ukus=Chocolate+Flavor</code></td></tr>
        <tr><td><b>"Posni" + season ads</b></td><td>New page <b>/posni-protein</b>, live by 20 Nov</td></tr>
        <tr><td><b>Broad, many flavors</b></td><td>/shop, until /posni-protein is live</td></tr>
        <tr><td><b>Retargeting</b></td><td>Cart → /cart · visitors → the product they viewed · refill → their flavor or the 2× Combo</td></tr>
        <tr><td><b>Never</b></td><td><span class="pill no">homepage</span> <span class="pill no">3× Combo pages</span> <span class="pill no">out-of-stock flavors</span></td></tr>
      </table>
    </div>
  </div>

  <div class="wire" style="margin-top:7px">
    <div class="phone">
      <div class="blk top"><b>1 · Posni protein</b> · pack photo · price per kg · free delivery · [Izaberi ukus]</div>
      <div class="blk"><b>2 · Pick</b> · in-stock flavors + 2× Combo with the saving</div>
      <div class="blk"><b>3 · Why posni</b> · yeast protein · 9 amino acids · no added sugar</div>
      <div class="blk"><b>4 · 3 posni breakfasts</b> · oats, smoothie, pancakes</div>
      <div class="blk"><b>5 · Real reviews</b> · photos + names</div>
      <div class="blk"><b>6 · FAQ</b> · delivery 2–3 days · card −5% · returns 14 days</div>
      <div class="sticky">Dodaj u korpu · sticky on mobile</div>
    </div>
    <div>
      <h3>How every landing page should look</h3>
      <ul class="tight">
        <li><b>Same promise as the ad.</b> A Chocolate ad opens on Chocolate, a Combo ad on the Combo, a posni ad on "Posni protein".</li>
        <li><b>Buy on the first screen.</b> Price, flavor picker and add-to-cart visible on a phone without scrolling; the button stays pinned.</li>
        <li><b>Only what's in stock.</b> Hide sold-out flavors and drop "6 ukusa" while there are 3.</li>
        <li><b>Show value per kg.</b> Put the 2× Combo next to single packs with price per kg and the saving in dinars.</li>
        <li><b>Real reviews near the top.</b> Every product page shows 0 reviews today.</li>
        <li><b>Allowed claims only.</b> Say what's in it; skip immunity, diabetes and skin claims until a lawyer approves them.</li>
        <li><b>Fast on mobile.</b> The homepage takes ~1.4 s to start loading; check PageSpeed.</li>
      </ul>
    </div>
  </div>

  <div class="foot"><span>Sources: Yea Protein GA4 and Meta Ads (Sep 2025 – Oct 2026), live catalog and /akcije on yeaprotein.rs, 27 Oct 2026. Budgets are estimates.</span><span>1 / 2</span></div>
</section>
"""

# =================== PAGE 2: ads calendar ===================
rows = [
    (1, "27 Oct – 19 Nov", "Restock + test", "€25", False,
     "Test 5–6 posni ads (posni breakfast, shaker routine, flavor carousel, Combo value static, 2 creator videos) + Chocolate and Vanilla Caramel ads",
     "Sour Cherry + free EasyGut to 8 Nov · 2× Combos back after restock",
     "Flavor ads → product page, flavor pre-selected · Sour Cherry → /akcije",
     "€5: cart 14d, visitors 30d"),
    (2, "20 – 26 Nov", "Spremi se za post", "€25 → €80", False,
     "Test winners + \"Post počinje 28.11.\" Combo carousel and stories",
     "2× Combo, any two flavors · leftover Sour Cherry as a mixed 2×500g with Vanilla Caramel",
     "<b>/posni-protein</b> (goes live) · Combo ads → 2× Combo page",
     "€8 + \"post starts Saturday\" reminder"),
    (3, "27 – 30 Nov", "Black Friday", "€80–100", True,
     "BF static + carousel, countdown stories, best sellers",
     "−10% on everything incl. Combos (last year's yeabw10 brought 42 orders) · needs client OK",
     "/posni-protein with a code banner",
     "€15: cart + visitors 30d"),
    (4, "1 Dec – 6 Jan", "Božićni post", "€80", True,
     "Posni winners at full budget, posni breakfast recipes, creator partnership ads; new hooks every 2 weeks",
     "2× Combos, no extra discount",
     "<b>/posni-protein</b>",
     "€15 + refill: 500g buyers day 10–20, 1kg day 25–40"),
    (5, "7 Jan – 28 Feb", "Baseline", "€30", False,
     "Best sellers + everyday use (breakfast, training) · from 9 Feb test the next 5 Lent ads",
     "Singles + 2× Combos",
     "Product pages · 2× Combo page",
     "€5 + refill"),
    (6, "1 – 14 Mar", "Pre-Lent", "€50", False,
     "\"Veliki post počinje 15.3.\" teaser + best Lent test ads",
     "\"Spremi se za Veliki post\": 2× Combo; 3× shown only as an upsell on the page",
     "<b>/posni-protein</b> (Lent version)",
     "€8"),
    (7, "15 Mar – 4 Apr", "Lent weeks 1–3", "€100", True,
     "Posni hero ads at max budget, recipe carousel, creators; scale +20% steps while revenue holds",
     "Lent 2× Combo bundle (if discounted, needs client OK)",
     "<b>/posni-protein</b>",
     "€15"),
    (8, "5 Apr – 1 May", "Rest of Lent", "€60", True,
     "Same winners, refresh hooks weekly; cut ads that slip",
     "2× Combos",
     "<b>/posni-protein</b>",
     "€15, refill is the priority (March buyers run out in April)"),
    (9, "2 – 31 May", "After Easter", "€30", False,
     "Everyday protein: breakfast, training, taste",
     "Singles + 2× Combos",
     "Product pages · 2× Combo page",
     "€5 + refill"),
]
tr = []
for n, when, name, bud, peak, ads, offer, lp, rt in rows:
    tr.append(f'<tr class="{"peak" if peak else ""}"><td class="when"><span class="num{"" if peak else " base"}">{n}</span><b>{name}</b>{when}</td>'
              f'<td class="bud">{bud}</td><td>{ads}</td><td>{offer}</td><td>{lp}</td><td>{rt}</td></tr>')

p2 = f"""
<section class="page">
  <div class="head2">
    <div><div class="eyebrow">Yea Protein · ads calendar</div><h1>What runs when: Nov 2026 – May 2027</h1></div>
    <div style="font-size:7pt;color:var(--muted);text-align:right">Meta €/day includes retargeting<br>Purple = fasting peaks</div>
  </div>
  <div class="card" style="margin-top:6px">{strip()}</div>

  <table class="cal" style="margin-top:6px">
    <colgroup><col style="width:82px"><col style="width:48px"><col style="width:26%"><col style="width:22%"><col style="width:20%"><col></colgroup>
    <tr><th>When</th><th>€/day</th><th>Prospecting ads</th><th>Offer</th><th>Landing page</th><th>Retargeting (€/day)</th></tr>
    {"".join(tr)}
  </table>

  <div class="lanes">
    <div class="lane"><b>Always on</b><p>One Advantage+ Sales prospecting campaign (broad Serbia) + one retargeting campaign. Add new ads to these campaigns; don't keep launching new campaigns.</p></div>
    <div class="lane g"><b>Google Search</b><p>Brand terms all year. Add "posni protein" and "veganski protein" from 20 Nov – 6 Jan and 1 Mar – 1 May. Same landing pages as Meta.</p></div>
    <div class="lane c"><b>Before every phase</b><p>Check stock against page 1. Pause any ad whose flavor is out. If the top two flavors run low, cut budget, not quality.</p></div>
  </div>

  <div class="foot"><span>Offers marked "needs client OK" change prices. Dates: Orthodox calendar (Božićni post 28 Nov – 6 Jan, Lent 15 Mar – 1 May 2027).</span><span>2 / 2</span></div>
</section>
"""

(OUT / "yea_budget_lp.html").write_text(page(p1, "Yea Budget and Pages"))
(OUT / "yea_calendar.html").write_text(page(p2, "Yea Ads Calendar"))
print("built")
