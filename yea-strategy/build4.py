"""Yea Protein ads playbook: one 2-page document that replaces the rules page and the calendar.
Page 1: what 1x means, budget/stock rules, landing pages (look + why).
Page 2: season calendar with budget, expected sales, stock, message, ads, offer and landing page.
Data: Yea GA4 weekly orders and Meta weekly spend (Sep 2025 - May 2026), live shop (27 Oct 2026).
"""
from pathlib import Path
from build2 import CSS, t, PLUM, GRAY, INK, INK2, MUTED, CHERRY

OUT = Path(__file__).parent
TEAL = "#2e8f6a"

CSS4 = CSS + """
  .fix{display:flex;flex-wrap:wrap;gap:4px;align-items:center;margin-top:6px}
  .fix strong{font-family:Fraunces,serif;font-size:9pt;margin-right:3px}
  .fix span{background:var(--plum-soft);color:var(--plum);border-radius:20px;padding:2px 8px;font-size:7pt;font-weight:700}
  .base{background:var(--plum);color:#efeaf8;border-radius:9px;padding:8px 10px}
  .base h3{color:#fff;font-size:10.5pt;margin-bottom:4px}
  .bstats{display:grid;grid-template-columns:repeat(3,1fr);gap:5px;margin:4px 0 6px}
  .bstats div{background:rgba(255,255,255,.12);border-radius:7px;padding:5px 6px;font-size:6.8pt;line-height:1.25}
  .bstats b{display:block;font-family:Fraunces,serif;font-size:13pt;color:#fff;line-height:1.1}
  .base p{font-size:7.3pt;line-height:1.38;margin-top:3px}
  .base p b{color:#fff}
  .rules3{display:grid;grid-template-columns:1.15fr 1fr 1fr;gap:6px}
  .rc{background:var(--card);border:1px solid var(--line);border-radius:9px;padding:6px 8px}
  .rc h4{font-size:8.2pt;font-weight:800;margin-bottom:3px;display:flex;align-items:center;gap:5px}
  .rc h4 .k{width:15px;height:15px;border-radius:50%;background:var(--plum);color:#fff;font-size:7pt;display:grid;place-items:center}
  .tl{display:grid;grid-template-columns:9px 1fr;gap:2px 5px;align-items:start;font-size:7pt;color:var(--ink2);line-height:1.3;margin-bottom:2px}
  .tl i{width:9px;height:9px;border-radius:50%;margin-top:2px}
  .tl b{color:var(--ink)}
  .lpwrap{display:grid;grid-template-columns:47mm 1fr;gap:9px;align-items:start}
  .phone{border:2px solid #cfc7dc;border-radius:13px;padding:5px;background:#fff}
  .blk{border-radius:5px;padding:3px 5px;margin-bottom:3px;font-size:6.3pt;line-height:1.25;color:var(--ink2);background:#f6f2fb;border:1px dashed #d9cfe9;display:grid;grid-template-columns:12px 1fr;gap:3px}
  .blk .bn{width:12px;height:12px;border-radius:50%;background:var(--plum);color:#fff;font-size:6pt;font-weight:800;display:grid;place-items:center}
  .blk.top{background:var(--plum);color:#efeaf8;border:0} .blk.top .bn{background:#fff;color:var(--plum)} .blk b{color:var(--ink)} .blk.top b{color:#fff}
  .sticky{background:var(--cherry);color:#fff;border-radius:5px;text-align:center;font-weight:800;font-size:6.5pt;padding:3px}
  table.why td{font-size:7pt;padding:3px 6px;line-height:1.3} table.why td:first-child{white-space:nowrap}
  .bn2{display:inline-grid;place-items:center;width:13px;height:13px;border-radius:50%;background:var(--plum);color:#fff;font-size:6.2pt;font-weight:800;margin-right:3px}
  .lead td{font-size:7pt;padding:3px 6px;line-height:1.3}
  table.cal td{font-size:6.9pt;padding:4px 5px;line-height:1.3}
  table.cal td.when b{display:block;font-family:Fraunces,serif;font-size:8.4pt;font-weight:600}
  .bud{font-weight:800;color:var(--plum);font-size:8.2pt;white-space:nowrap}
  .sub{display:block;font-size:6.5pt;color:var(--muted);line-height:1.3;margin-top:2px}
  .sub b{color:var(--ink2)}
  .msg{font-style:italic;color:var(--ink);font-weight:600}
  .gl{display:block;font-style:normal;font-weight:400;color:var(--muted);font-size:6.4pt;margin-top:1px}
  .num{display:inline-grid;place-items:center;width:15px;height:15px;border-radius:50%;background:var(--plum);color:#fff;font-size:6.8pt;font-weight:800;margin-bottom:2px}
  .num.base2{background:#b9b1c9}
  .ready{display:grid;grid-template-columns:1fr 1fr;gap:6px;margin-top:6px}
  .ready div{background:var(--amber-soft);border-radius:8px;padding:5px 9px;font-size:7.2pt;color:#5c4a1c}
  .ready b{color:#8a5a00}
  .lanes4{display:grid;grid-template-columns:repeat(4,1fr);gap:6px;margin-top:6px}
  .lane{background:var(--card);border:1px solid var(--line);border-radius:9px;padding:5px 8px;border-top:3px solid var(--plum)}
  .lane b{display:block;font-size:6.6pt;letter-spacing:.1em;text-transform:uppercase;margin-bottom:2px;color:var(--plum)}
  .lane.c{border-top-color:var(--cherry)} .lane.c b{color:var(--cherry)} .lane.g{border-top-color:var(--good)} .lane.g b{color:var(--good)}
  .lane p{font-size:6.9pt;color:var(--ink2);line-height:1.3}
  .adlib{display:grid;grid-template-columns:repeat(4,1fr);gap:5px}
  .ad{background:var(--card);border:1px solid var(--line);border-radius:8px;padding:5px 7px;font-size:6.8pt;color:var(--ink2);line-height:1.3}
  .ad h5{font-size:7.6pt;color:var(--ink);font-weight:800;margin-bottom:1px}
  .ad .ph{display:block;margin-top:2px;font-size:6.3pt;font-weight:700;color:var(--plum)}
  .offers{display:grid;grid-template-columns:repeat(4,1fr);gap:5px;margin-top:5px}
  .offers div{background:var(--plum-soft);border-radius:8px;padding:5px 7px;font-size:6.8pt;color:var(--ink2);line-height:1.3}
  .offers b{color:var(--plum);display:block;font-size:7.4pt}
"""


def bar(x, y, w, h, col, r=3):
    w = max(w, 2)
    return f'<path d="M{x},{y} L{x+w-r},{y} Q{x+w},{y} {x+w},{y+r} L{x+w},{y+h-r} Q{x+w},{y+h} {x+w-r},{y+h} L{x},{y+h} Z" fill="{col}"/>'


# ---------- page 1 chart: last year's sales vs suggested budget, both as x normal week ----------
def chart_season():
    rows = [("Black Friday week", 3.9, 3.0), ("Christmas fast, wk 1–2", 1.8, 2.0), ("Christmas fast, holidays", 1.0, 1.0),
            ("Off-season", 1.0, 1.0), ("Week before Lent", 2.0, 1.5), ("Lent, week 1", 4.0, 3.0),
            ("Lent, weeks 2–3", 2.2, 3.0), ("Rest of Lent", 1.5, 1.5), ("After Easter", 0.8, 1.0)]
    lx, bx, bmax, rh, y0, vmax = 112, 118, 190, 19, 16, 4.0
    s = [f'<rect x="{bx}" y="2" width="9" height="9" rx="2" fill="{PLUM}"/>', t(bx + 13, 10, "last year's orders", 7.4, INK2),
         f'<rect x="{bx+98}" y="2" width="9" height="9" rx="2" fill="{TEAL}"/>', t(bx + 111, 10, "suggested ad budget", 7.4, INK2)]
    for g in (1, 2, 3, 4):
        xx = bx + g / vmax * bmax
        s.append(f'<line x1="{xx}" x2="{xx}" y1="14" y2="{y0+len(rows)*rh}" stroke="#ece7df"/>')
    for i, (lab, sales, bud) in enumerate(rows):
        y = y0 + i * rh
        s.append(t(lx, y + 11, lab, 7.6, INK, "end", 600))
        s.append(bar(bx, y + 2, sales / vmax * bmax, 7, PLUM))
        s.append(t(bx + sales / vmax * bmax + 4, y + 8.5, f"{sales:g}×", 7.2, INK, "start", 700))
        s.append(bar(bx, y + 10.5, bud / vmax * bmax, 7, TEAL))
        s.append(t(bx + bud / vmax * bmax + 4, y + 17, f"{bud:g}×", 7.2, TEAL, "start", 700))
    s.append(f'<line x1="{bx}" x2="{bx}" y1="14" y2="{y0+len(rows)*rh}" stroke="{MUTED}"/>')
    return f'<svg viewBox="0 0 340 {y0 + len(rows) * rh + 2}" role="img" aria-label="Last year sales and suggested budget as multiples of a normal week">{"".join(s)}</svg>'


# ---------- page 2: calendar ----------
# (n, when, name, peak, budget, sales_last_year, stock, message_sr, message_en, ads, offer, landing)
ROWS = [
    (1, "now – 19 Nov", "Restock + test", False, "1×",
     "1× (autumn 2025)", "6+ wks",
     "Omiljeni ukus je opet tu.", "Your favorite flavor is back.",
     "<b>“Back in stock” statics</b> for Chocolate and Vanilla Caramel (pack, flavor, price per kg). <b>Test 4–6 posni concepts</b>: posni breakfast Reel, morning shaker routine, flavor carousel, Combo value static, 2 creator partnership videos.",
     "<b>Sour Cherry 500g + free EasyGut</b> until 8 Nov (/akcije). <b>2× Combos return</b> at the usual Combo price once restocked (~25–30% under two singles).",
     "Flavor ads → product page, flavor pre-selected · Sour Cherry → /akcije"),
    (2, "20 – 26 Nov", "Spremi se za post", False, "1.5×",
     "~1× (no pre-fast bump in 2025)", "6+ wks, plus 4 for BF",
     "Post počinje 28.11. Spremi se.", "The fast starts 28 Nov. Get ready.",
     "Move the <b>2–3 test winners</b> into the main campaign. <b>Countdown stories</b> “još 7 dana do posta”. <b>Combo carousel</b>: two packs = the whole fast.",
     "<b>2× Combo, any two flavors</b>, pitched as “one 2×1kg covers the whole 40-day fast”. Leftover Sour Cherry as a mixed 2×500g with Vanilla Caramel.",
     "<b>/posni-protein</b> goes live · Combo ads → 2× Combo page"),
    (3, "27 – 30 Nov", "Black Friday", True, "3×",
     "~4× (BF week 2025: 242 orders)", "4 wks for this week",
     "Najbolja cena ove godine.", "Best price of the year.",
     "<b>Offer static</b> with the discount and the Combo, <b>best-seller carousel</b> with BF prices, <b>countdown stories</b> Fri → Mon, retargeting to cart abandoners with the code.",
     "<b>Black Friday code on everything incl. Combos</b>, 4 days only. Last year's 10% code (yeabw10) brought 42 orders. Needs client OK.",
     "/posni-protein with a code banner · cart → /cart"),
    (4, "1 Dec – 6 Jan", "Božićni post", True, "2× → 1×",
     "~1.8× in wks 1–2, ~1× over the holidays", "~7 wks for the period",
     "Posni protein za ceo post.", "Protein for the whole fast.",
     "<b>3 posni breakfast Reels</b> (oats, smoothie, pancakes), <b>“a fasting day” UGC</b>, creator partnership ads, Combo value static. New hooks every 2 weeks. <b>Drop to 1× from ~15 Dec</b>, when holiday sales fall.",
     "<b>2× Combo, no extra discount</b>, free delivery. Refill reminders for November buyers (500g lasts ~2 weeks, 1kg ~4).",
     "<b>/posni-protein</b> · refill → their flavor"),
    (5, "7 Jan – 28 Feb", "Off-season", False, "1×",
     "1× (Jan–Feb 2026: ~65 orders/wk)", "6+ wks",
     "Protein za svaki dan.", "Protein for every day.",
     "<b>Everyday use</b>: breakfast and training, taste-led flavor ads, a “new year, new routine” angle in early January. <b>From mid-Feb test 4–6 new Lent concepts</b> at small budget.",
     "<b>Singles + 2× Combos</b>, card −5%. No discounts: save them for the fasts.",
     "Product pages · 2× Combo page"),
    (6, "1 – 14 Mar", "Build-up to Lent", False, "1.5×",
     "1× → 2× in the last week", "~3 wks, plus 14 for Lent",
     "Veliki post počinje 15.3. Spremi se.", "Lent starts 15 Mar. Stock up.",
     "<b>Lent teaser</b> ads and stories, <b>best Lent test ads</b> move into the main campaign, Combo carousel “za ceo post”.",
     "<b>2× Combo “za ceo post”</b> (Lent is 7 weeks). 3× shown only as an upsell on the page, never as the ad's offer.",
     "<b>/posni-protein</b> (Lent version)"),
    (7, "15 Mar – 4 Apr", "Lent weeks 1–3", True, "3×",
     "4× in wk 1, ~2.2× in wks 2–3", "~8.5 wks for 3 weeks",
     "Posni protein koji je stvarno ukusan.", "Posni protein that actually tastes good.",
     "<b>The biggest weeks of the year.</b> Posni hero ads at full budget, recipe carousel, creator videos. Scale +20% while revenue holds; don't test new ads now.",
     "<b>Lent 2× Combo bundle</b> (a discount only with client OK). Free delivery.",
     "<b>/posni-protein</b>"),
    (8, "5 Apr – 1 May", "Rest of Lent", True, "1.5×",
     "~1.75×, Easter week ~0.8×", "~6 wks",
     "Pola posta je iza tebe. Ne ostani bez zaliha.", "Halfway through. Don't run out.",
     "<b>Same winners with fresh hooks weekly.</b> <b>Refill ads</b> to March buyers (their packs run out now). Cut to 1× in Easter week.",
     "<b>2× Combos</b> + refill reminder with their last flavor.",
     "<b>/posni-protein</b> · refill → their flavor"),
    (9, "from 2 May", "After Easter", False, "1×",
     "~0.8× (May 2026)", "6+ wks",
     "Protein za svaki dan.", "Protein for every day.",
     "<b>Everyday protein</b>: breakfast, training, summer, taste. <b>Test new ads</b> again.",
     "<b>Singles + 2× Combos</b>.",
     "Product pages · 2× Combo page"),
]
# strip segments: (phase n, days, level, peak)
SEG = [(1, 24, 1.0, False), (2, 7, 1.5, False), (3, 4, 3.0, True), (4, 14, 2.0, True), (4, 23, 1.0, True), (5, 53, 1.0, False),
       (6, 14, 1.5, False), (7, 21, 3.0, True), (8, 27, 1.5, True), (9, 30, 1.0, False)]


def strip():
    W, x0, x1, yb, yt = 700, 6, 694, 80, 36
    total = sum(s[1] for s in SEG)
    sx = (x1 - x0) / total
    y = lambda v: yb - v / 3 * (yb - yt)
    s, x, shown = [], x0, set()
    for n, days, lev, peak in SEG:
        w = days * sx
        s.append(f'<rect x="{x+1}" y="{y(lev)}" width="{w-2}" height="{yb-y(lev)}" rx="3" fill="{PLUM if peak else GRAY}"/>')
        if n not in shown:
            shown.add(n)
            cx = x + w / 2
            s.append(f'<circle cx="{cx}" cy="{y(lev)-10}" r="6.3" fill="{PLUM if peak else "#b9b1c9"}"/>')
            s.append(t(cx, y(lev) - 7.6, str(n), 7.2, "#fff", "middle", 800))
        if w > 24:
            s.append(t(x + w / 2, yb - 4, f"{lev:g}×", 7.6, "#fff" if peak else INK2, "middle", 800))
        x += w
    s.append(f'<line x1="{x0}" x2="{x1}" y1="{yb}" y2="{yb}" stroke="{MUTED}"/>')
    for d, m in [(5, "Nov"), (35, "Dec"), (66, "Jan"), (97, "Feb"), (125, "Mar"), (156, "Apr"), (186, "May")]:
        xx = x0 + d * sx
        s.append(f'<line x1="{xx}" x2="{xx}" y1="{yb}" y2="{yb+4}" stroke="{MUTED}"/>')
        s.append(t(xx + 2, yb + 12, m, 7, MUTED))
    for d, lab in [(31, "BF 27 Nov · fast 28 Nov"), (139, "Lent 15 Mar"), (187, "Easter 2 May")]:
        xx = x0 + d * sx
        s.append(f'<line x1="{xx}" x2="{xx}" y1="3" y2="{yb}" stroke="{CHERRY}" stroke-dasharray="2 2"/>')
        s.append(t(xx + 3, 9, lab, 6.8, CHERRY, "start", 700))
    return f'<svg viewBox="0 0 {W} 94" role="img" aria-label="Season phases and budget level">{"".join(s)}</svg>'


def cal_rows():
    out = []
    for n, when, name, peak, bud, sales, stock, msr, men, ads, offer, lp in ROWS:
        out.append(
            f'<tr class="{"peak" if peak else ""}"><td class="when"><span class="num{"" if peak else " base2"}">{n}</span><b>{name}</b>{when}</td>'
            f'<td><span class="bud">{bud}</span><span class="sub">Last year: <b>{sales}</b></span><span class="sub">Stock: <b>{stock}</b></span></td>'
            f'<td class="msg">„{msr}“<span class="gl">{men}</span></td><td>{ads}</td><td>{offer}</td><td>{lp}</td></tr>')
    return "".join(out)


html = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Yea Ads Playbook</title>
<link href="fonts/fonts.css" rel="stylesheet"><style>{CSS4}</style></head><body>

<section class="page">
  <div class="hero"><div class="txt">
    <div class="eyebrow">Yea Protein · ads playbook · Nov 2026 – May 2027</div>
    <h1>How much to spend, when, and where</h1>
    <p>Budget rules, landing pages, and the season calendar on page 2.</p>
  </div></div>

  <div class="fix"><strong>Fix first</strong><span>Restock Chocolate + Vanilla Caramel</span><span>Bring back 2× Combos</span><span>Build /posni-protein</span><span>Turn on stock tracking</span><span>Keep EasyGut's budget separate</span><span>Judge by shop revenue, not Meta</span></div>

  <div class="grid2" style="grid-template-columns:1fr 1.08fr;margin-top:6px">
    <div class="base">
      <h3>What “1×” means: a normal week</h3>
      <div class="bstats">
        <div><b>~65</b>orders a week</div>
        <div><b>~70–100</b>units a week (more with Combos)</div>
        <div><b>~€850</b>a week on Meta</div>
      </div>
      <p>That was a <b>normal off-season week in autumn 2025</b>, with every flavor in stock. Today it's ~20 orders a week on ~€70, because the ads are nearly off.</p>
      <p><b>Set 1×</b> to the weekly budget your stock can carry for 6+ weeks, and rebuild toward last year's level in +20% steps. Every other level is a multiple of it.</p>
      <p><b>Why spend more in fasts:</b> last year Meta spend stayed ~flat through Lent, yet orders jumped 4× in week 1. The same money buys far more orders then.</p>
    </div>
    <div class="card">
      <h3 style="font-size:9.5pt">Last year's orders vs the budget to plan, × a normal week</h3>
      {chart_season()}
    </div>
  </div>

  <div class="rules3" style="margin-top:6px">
    <div class="rc"><h4><span class="k">1</span>Stock light: check before every phase</h4>
      <div class="tl"><i style="background:#2f7d4a"></i><span><b>Green</b>: Chocolate and Vanilla Caramel have 6+ normal weeks → run the planned level.</span></div>
      <div class="tl"><i style="background:#d39a00"></i><span><b>Yellow</b>: 2–6 weeks or a size missing → hold at 1×, push what you have, reorder.</span></div>
      <div class="tl"><i style="background:var(--cherry)"></i><span><b>Red</b>: under 2 weeks or a top flavor sold out → retargeting only.</span></div>
      <p class="note" style="margin-top:1px">Weeks of stock = units ÷ units sold in a normal week. In a fast, divide by the "last year" multiple on page 2.</p></div>
    <div class="rc"><h4><span class="k">2</span>Every week: scale or cut</h4>
      <div class="tl"><i style="background:#2f7d4a"></i><span><b>3× or more</b> revenue ÷ ad spend → add 20% (max twice a week).</span></div>
      <div class="tl"><i style="background:#d39a00"></i><span><b>2–3×</b> → hold, swap in fresh ads.</span></div>
      <div class="tl"><i style="background:var(--cherry)"></i><span><b>Under 2×</b> two weeks running → cut 20%; check stock, offer, page.</span></div>
      <p class="note" style="margin-top:1px">Use WooCommerce revenue. 3× was the 2025 level; set your own line from margin.</p></div>
    <div class="rc"><h4><span class="k">3</span>Always the same setup</h4>
      <p style="font-size:7pt;color:var(--ink2);line-height:1.35"><b style="color:var(--ink)">~80%</b> to one prospecting campaign, <b style="color:var(--ink)">~20%</b> to retargeting (cart, visitors, refill). Retargeting never stops, even in Red.<br><b style="color:var(--ink)">Test new ads off-season</b>, 4–6 at a time; in peaks, run only the winners.</p></div>
  </div>

  <h2>Landing pages <small>99% of ad visitors are on a phone, and 63% leave after one page</small></h2>
  <div class="lpwrap">
    <div class="phone">
      <div class="blk top"><span class="bn">1</span><span><b>Posni protein</b> · pack photo · price per kg · free delivery · [Dodaj u korpu]</span></div>
      <div class="blk"><span class="bn">2</span><span><b>Pick flavor + pack</b> · in-stock only · 2× Combo with saving</span></div>
      <div class="blk"><span class="bn">3</span><span><b>Why it's posni</b> · yeast protein · 9 amino acids · no added sugar</span></div>
      <div class="blk"><span class="bn">4</span><span><b>3 posni breakfasts</b> · oats, smoothie, pancakes</span></div>
      <div class="blk"><span class="bn">5</span><span><b>Real reviews</b> · photos + names</span></div>
      <div class="blk"><span class="bn">6</span><span><b>FAQ</b> · delivery 2–3 days · card −5% · 14-day returns · how long a pack lasts</span></div>
      <div class="sticky">Dodaj u korpu · pinned on mobile</div>
    </div>
    <div>
      <table class="why">
        <tr><th>Block</th><th>Why it's there</th></tr>
        <tr><td><span class="bn2">1</span>First screen sells</td><td>Most ad visitors see one phone screen and leave, so the promise, price and buy button must be on it.</td></tr>
        <tr><td><span class="bn2">2</span>In stock + Combo</td><td>Combos were 40–66% of revenue at their peak. A sold-out flavor is a paid click with nothing to buy.</td></tr>
        <tr><td><span class="bn2">3</span>Posni facts</td><td>The fast is why people buy (4× orders in Lent week 1). Facts only, no health claims.</td></tr>
        <tr><td><span class="bn2">4</span>Recipes</td><td>Answers "how do I use it while fasting", which none of the current pages do.</td></tr>
        <tr><td><span class="bn2">5</span>Reviews</td><td>Every product page shows 0 reviews today, next to "10.000 zadovoljnih kupaca".</td></tr>
        <tr><td><span class="bn2">6</span>FAQ</td><td>Removes the last doubts: delivery time, payment, returns.</td></tr>
      </table>
      <table class="lead" style="margin-top:5px">
        <tr><th>Ad</th><th>Goes to</th><th>Why</th></tr>
        <tr><td><b>Posni / season</b></td><td>/posni-protein</td><td>Same reason to buy as the ad</td></tr>
        <tr><td><b>One flavor</b></td><td>Product page, flavor pre-selected</td><td>One tap less, same promise</td></tr>
        <tr><td><b>Combo / offer</b></td><td>2× Combo page (rebuild, now 404)</td><td>Best revenue per visit: 94–114 RSD</td></tr>
        <tr><td><b>Never</b></td><td>Homepage · 3× packs · sold-out</td><td>Homepage earns 54 RSD; 3× packs 0.6% buy</td></tr>
      </table>
    </div>
  </div>

  <h2>The ads and offers <small>numbers = calendar phases on page 2 · show only in-stock flavors · facts, no health claims</small></h2>
  <div class="adlib">
    <div class="ad"><h5>Posni breakfast Reel</h5>15–20s, hands only: oats, smoothie or pancakes with Yea in 2 minutes. Text on screen, ends on pack + price per kg.<span class="ph">Phases 1 · 4 · 7</span></div>
    <div class="ad"><h5>"A fasting day" creator video</h5>A creator's real morning in the fast, shaker in hand. Runs as a partnership ad from their profile.<span class="ph">Phases 1 · 4 · 7 · 8</span></div>
    <div class="ad"><h5>Flavor carousel</h5>One card per in-stock flavor: pack cut-out + one taste line. Last card is the 2× Combo.<span class="ph">Phases 2 · 3 · 5</span></div>
    <div class="ad"><h5>Combo value static</h5>Two packs side by side, price per kg vs a single, "dovoljno za ceo post".<span class="ph">Phases 1 · 2 · 4 · 6 · 7</span></div>
    <div class="ad"><h5>"Back in stock" static</h5>The restocked flavor big, "Vratio se omiljeni ukus", price per kg. Run for 2–3 weeks after a restock.<span class="ph">Phase 1, and after any restock</span></div>
    <div class="ad"><h5>Countdown stories</h5>"Još 7 dana do posta" or "BF još 2 dana". 3 frames: date, Combo, buy button.<span class="ph">Phases 2 · 3 · 6</span></div>
    <div class="ad"><h5>Offer static</h5>Only for Black Friday: the code, the price, the end date. Nothing else on it.<span class="ph">Phase 3</span></div>
    <div class="ad"><h5>Refill ad (retargeting)</h5>"Tvoj [ukus] je pri kraju?" to buyers 2 weeks (500g) or 4 weeks (1kg) after the order, with their flavor.<span class="ph">Always on</span></div>
  </div>
  <div class="offers">
    <div><b>2× Combo = the default</b>Cheaper per kg than two singles, and covers a whole fast. Lead with it in every season.</div>
    <div><b>3× pack = upsell only</b>Show it on the page, never as the ad's offer: 0.6% of its visitors bought.</div>
    <div><b>Codes = Black Friday only</b>Plus one Lent bundle with client OK. Off-season discounts teach people to wait.</div>
    <div><b>Always in the ad</b>Free delivery, card −5%, delivery in 2–3 days. Leftover Sour Cherry goes out as a mixed 2×500g.</div>
  </div>

  <div class="foot"><span>Data: Yea Protein GA4 and Meta Ads (weekly, Sep 2025 – May 2026), live shop on yeaprotein.rs, 27 Oct 2026.</span><span>1 / 2</span></div>
</section>

<section class="page">
  <div class="head2" style="padding-top:7mm">
    <div><div class="eyebrow">Yea Protein · ads playbook</div><h1>Season calendar: what runs, what we say</h1></div>
    <div style="font-size:6.8pt;color:var(--muted);text-align:right">Budget = × a normal week (page 1)<br>Stock = normal weeks of sales to have ready</div>
  </div>
  <div class="card" style="margin-top:5px;padding:5px 9px">{strip()}</div>

  <table class="cal" style="margin-top:5px">
    <colgroup><col style="width:74px"><col style="width:76px"><col style="width:15%"><col style="width:27%"><col style="width:22%"><col></colgroup>
    <tr><th>When</th><th>Budget</th><th>What we say</th><th>Ads</th><th>Offer</th><th>Landing page</th></tr>
    {cal_rows()}
  </table>

  <div class="ready">
    <div><b>By 20 Nov, have ~12 normal weeks of stock</b> for Black Friday + Božićni post, most of it Chocolate and Vanilla Caramel.</div>
    <div><b>By 1 Mar, have ~18 normal weeks of stock</b> for the build-up and all of Lent. Order in January.</div>
  </div>
  <div class="lanes4">
    <div class="lane"><b>Always on</b><p>One prospecting campaign (Advantage+ Sales, broad Serbia) + one retargeting campaign. Add ads; don't relaunch.</p></div>
    <div class="lane c"><b>Retargeting</b><p>~20% of budget: cart, visitors, refill (500g after ~2 weeks, 1kg after ~4).</p></div>
    <div class="lane g"><b>Google Search</b><p>Brand all year. Add "posni protein" and "veganski protein" in fasts and their build-up.</p></div>
    <div class="lane c"><b>Stock light wins</b><p>Red overrides this calendar: retargeting only until restocked.</p></div>
  </div>

  <div class="foot"><span>Orthodox calendar: Božićni post 28 Nov – 6 Jan, Lent 15 Mar – 1 May 2027 (Easter 2 May). Offers marked "needs client OK" change prices.</span><span>2 / 2</span></div>
</section>
</body></html>"""

(OUT / "yea_playbook.html").write_text(html)
print("built")
