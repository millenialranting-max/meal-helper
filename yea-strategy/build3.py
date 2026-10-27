"""Yea Protein, simplified one-pagers (v2):
  yea_rules.html     - budget rules by season and stock, what ads when, where ads lead
  yea_calendar.html  - season calendar with relative budget levels, message, ads, offer, page
No fixed euro amounts: budgets are multiples of a base level (1x = a normal week).
"""
from pathlib import Path
from build2 import CSS, page, t, PLUM, GRAY, INK, INK2, MUTED, CHERRY

OUT = Path(__file__).parent
GREEN, AMBER = "#2f7d4a", "#b77900"

CSS2 = CSS + """
  .rule-h{display:flex;align-items:center;gap:7px;margin:8px 0 4px}
  .rule-h .k{width:20px;height:20px;border-radius:50%;background:var(--plum);color:#fff;font-weight:800;font-size:8pt;display:grid;place-items:center;flex:none}
  .rule-h h2{margin:0}
  .lights{display:grid;grid-template-columns:repeat(3,1fr);gap:6px}
  .light{border-radius:9px;padding:7px 9px;background:var(--card);border:1px solid var(--line);border-top:5px solid}
  .light.g{border-top-color:#2f7d4a} .light.y{border-top-color:#d39a00} .light.r{border-top-color:var(--cherry)}
  .light .h{display:flex;align-items:center;gap:6px;font-weight:800;font-size:8.4pt;margin-bottom:2px}
  .dot{width:11px;height:11px;border-radius:50%;flex:none}
  .light .c{font-size:7.2pt;color:var(--ink);font-weight:600;margin-bottom:2px}
  .light .a{font-size:7.2pt;color:var(--ink2)}
  .gauge{display:grid;grid-template-columns:repeat(3,1fr);gap:0;border-radius:9px;overflow:hidden;border:1px solid var(--line)}
  .gauge div{padding:6px 9px;font-size:7.2pt;color:var(--ink2)}
  .gauge b{display:block;font-size:9pt;margin-bottom:1px}
  .gauge .lo{background:#f9e6e9} .gauge .lo b{color:var(--cherry)}
  .gauge .mid{background:#fbf1dc} .gauge .mid b{color:#8a5a00}
  .gauge .hi{background:#e5f3ea} .gauge .hi b{color:#2f7d4a}
  .split{display:flex;height:22px;border-radius:6px;overflow:hidden;gap:2px;margin-top:3px}
  .split div{display:flex;align-items:center;padding:0 8px;color:#fff;font-weight:700;font-size:7.4pt;white-space:nowrap}
  table.mx td,table.mx th{text-align:center;padding:4px 5px} table.mx td:first-child,table.mx th:first-child{text-align:left}
  .m{font-size:11pt;line-height:1} .m.full{color:var(--plum)} .m.half{color:#a99bd0} .m.off{color:#d8d2e0}
  .flow{display:grid;grid-template-columns:1fr 18px 1fr;gap:4px 4px;align-items:center}
  .flow .ad{background:var(--plum-soft);border-radius:7px;padding:4px 8px;font-weight:700;font-size:7.4pt;color:var(--plum)}
  .flow .arr{color:var(--muted);text-align:center;font-size:10pt}
  .flow .pg{background:var(--card);border:1px solid var(--line);border-radius:7px;padding:4px 8px;font-size:7.3pt;color:var(--ink)}
  .chips span{display:inline-block;border-radius:20px;padding:2px 8px;font-size:7pt;font-weight:700;margin:2px 3px 0 0}
  .chips .no{background:var(--cherry-soft);color:var(--cherry)}
  .stat{background:var(--plum);color:#efeaf8;border-radius:9px;padding:7px 10px;font-size:7.3pt}
  .stat b{font-family:Fraunces,serif;font-size:15pt;color:#fff;display:block;line-height:1.1}
  .dt{display:inline-block;width:11px;height:11px;border-radius:50%;border:1.6px solid var(--plum);vertical-align:-2px}
  .dt.f{background:var(--plum)} .dt.h{background:linear-gradient(90deg,var(--plum) 50%,#fff 50%)} .dt.o{border-color:#d3cbe0;background:#fff}
  .gl{display:block;font-style:normal;font-weight:400;color:var(--muted);font-size:6.6pt;margin-top:1px}
  .lvl{display:inline-flex;gap:2px;vertical-align:middle;margin-right:4px}
  .lvl i{width:6px;height:11px;border-radius:2px;background:#e3dcef;display:block}
  .lvl i.on{background:var(--plum)}
  .bud2{font-weight:800;color:var(--plum);font-size:8pt;white-space:nowrap}
  .msg{font-style:italic;color:var(--ink);font-weight:600}
  .lanes4{display:grid;grid-template-columns:repeat(4,1fr);gap:6px;margin-top:6px}
"""


def page2(body, title):
    return page(body, title).replace(f"<style>{CSS}</style>", f"<style>{CSS2}</style>")


# ---------- season level chart (relative budget) ----------
def chart_levels():
    rows = [("Off-season", "Jan–Feb, May–Oct", 1.0, False),
            ("Build-up", "1–2 weeks before a fast", 1.5, False),
            ("Christmas fast", "28 Nov – 6 Jan", 2.0, True),
            ("Rest of Lent", "week 4 to Easter", 2.0, True),
            ("Black Friday", "4 days", 3.0, True),
            ("Lent, weeks 1–3", "from Clean Monday", 3.0, True)]
    lx, bx, bmax, rh, y0 = 118, 124, 170, 18, 4
    s = []
    for i, (lab, sub, v, peak) in enumerate(rows):
        y = y0 + i * rh
        w = v / 3 * bmax
        s.append(t(lx, y + 9, lab, 8.2, INK, "end", 700))
        s.append(t(lx, y + 16.5, sub, 6.6, MUTED, "end"))
        s.append(f'<path d="M{bx},{y+3} L{bx+w-4},{y+3} Q{bx+w},{y+3} {bx+w},{y+7} L{bx+w},{y+12} Q{bx+w},{y+16} {bx+w-4},{y+16} L{bx},{y+16} Z" fill="{PLUM if peak else GRAY}"/>')
        s.append(t(bx + w + 5, y + 13, f"{v:g}×", 9, INK, "start", 800))
    return f'<svg viewBox="0 0 330 {y0 + len(rows) * rh + 2}" role="img" aria-label="Budget level by season as a multiple of a normal week">{"".join(s)}</svg>'


def lvl(n):
    return '<span class="lvl">' + "".join(f'<i class="{"on" if k < n else ""}"></i>' for k in range(4)) + "</span>"


M = {"F": '<span class="dt f"></span>', "H": '<span class="dt h"></span>', "O": '<span class="dt o"></span>'}

# =================== PAGE 1: rules ===================
p1 = f"""
<section class="page">
  <div class="hero"><div class="txt">
    <div class="eyebrow">Yea Protein · how to run the ads</div>
    <h1>Budget rules &amp; landing pages</h1>
    <p>How much to spend and when, which ads to run, where they lead.</p>
  </div></div>

  <div class="grid2" style="grid-template-columns:1fr 1fr">
    <div>
      <div class="rule-h"><span class="k">1</span><h2>Spend follows the season</h2></div>
      <div class="card">{chart_levels()}
        <p class="note"><b style="color:var(--ink)">1× = your normal week.</b> Set it from what stock and margin allow, then multiply. In the first week of Lent orders were 3.5× the weeks before, and they fell ~60% the week after Easter, in both years.</p>
      </div>
    </div>
    <div>
      <div class="rule-h"><span class="k">2</span><h2>Stock decides how far you go</h2></div>
      <div class="lights" style="grid-template-columns:1fr">
        <div class="light g"><div class="h"><span class="dot" style="background:#2f7d4a"></span>Green: go to the season level</div><div class="c">Chocolate and Vanilla Caramel each have 6+ weeks of stock</div><div class="a">Run the full season level from rule 1.</div></div>
        <div class="light y"><div class="h"><span class="dot" style="background:#d39a00"></span>Yellow: hold at 1×</div><div class="c">2–6 weeks of stock, or one size missing</div><div class="a">Push the flavors and Combos you have; order more now.</div></div>
        <div class="light r"><div class="h"><span class="dot" style="background:var(--cherry)"></span>Red: retargeting only</div><div class="c">Under 2 weeks, or a top flavor sold out</div><div class="a">Pause ads for missing flavors. Restock before you spend.</div></div>
      </div>
      <p class="note"><b style="color:var(--ink)">Weeks of stock</b> = units in stock ÷ units sold in a normal week. In a fast, stock runs out about twice as fast, so halve it.</p>
    </div>
  </div>

  <div class="grid2" style="grid-template-columns:1fr 1fr">
    <div>
      <div class="rule-h"><span class="k">3</span><h2>Scale or cut every week, on real revenue</h2></div>
      <div class="gauge">
        <div class="lo"><b>Under 2×</b>2 weeks in a row: cut 20%, check stock, offer and page</div>
        <div class="mid"><b>2–3×</b>Hold the budget, swap in fresh ads</div>
        <div class="hi"><b>3× or more</b>Add 20%, at most twice a week</div>
      </div>
      <p class="note">× = shop revenue (WooCommerce) ÷ total ad spend, that week. 3× was the 2025 level; set your own line from margin. Don't use Meta's purchase count for this.</p>
    </div>
    <div>
      <div class="rule-h"><span class="k">4</span><h2>Split the money the same way, always</h2></div>
      <div class="split"><div style="flex:80;background:var(--plum)">~80% new customers (one prospecting campaign)</div><div style="flex:20;background:var(--cherry)">~20% retargeting</div></div>
      <p class="note">Retargeting covers cart, site visitors and refill (500g lasts ~2 weeks, 1kg ~4 weeks). It never stops, even in Red. Test new ads off-season; in peaks, run the winners.</p>
    </div>
  </div>

  <h2>Which ads, when</h2>
  <table class="mx">
    <tr><th>Ad type</th><th>Off-season</th><th>Build-up</th><th>Black Friday</th><th>Fasts (Božićni post, Lent)</th></tr>
    <tr><td><b>Posni story</b> · recipes, morning routine, creators</td><td>{M['H']}</td><td>{M['F']}</td><td>{M['H']}</td><td>{M['F']}</td></tr>
    <tr><td><b>Best-seller flavors</b> · Chocolate, Vanilla Caramel</td><td>{M['F']}</td><td>{M['H']}</td><td>{M['H']}</td><td>{M['H']}</td></tr>
    <tr><td><b>Combo value / offer</b> · 2× pack, price per kg</td><td>{M['H']}</td><td>{M['F']}</td><td>{M['F']}</td><td>{M['F']}</td></tr>
    <tr><td><b>New ad tests</b> · 4–6 at a time</td><td>{M['F']}</td><td>{M['O']}</td><td>{M['O']}</td><td>{M['O']}</td></tr>
    <tr><td><b>Retargeting</b> · reviews, FAQ, refill reminder</td><td>{M['F']}</td><td>{M['F']}</td><td>{M['F']}</td><td>{M['F']}</td></tr>
  </table>
  <p class="note"><span class="dt f"></span> main &nbsp; <span class="dt h"></span> support &nbsp; <span class="dt o"></span> not now</p>

  <h2>Where ads should lead</h2>
  <div class="grid2" style="grid-template-columns:1.5fr 1fr">
    <div class="card">
      <div class="flow">
        <div class="ad">Posni / season ads</div><div class="arr">→</div><div class="pg"><b>/posni-protein</b> (new landing page)</div>
        <div class="ad">One-flavor ads</div><div class="arr">→</div><div class="pg">Product page with that flavor pre-selected</div>
        <div class="ad">Combo / offer ads</div><div class="arr">→</div><div class="pg">2× Combo page (rebuild; old one is 404)</div>
        <div class="ad">Retargeting</div><div class="arr">→</div><div class="pg">Cart · the product they viewed · refill</div>
      </div>
      <div class="chips" style="margin-top:5px"><b style="font-size:7.2pt;margin-right:4px">Never:</b><span class="no">homepage</span><span class="no">3× packs</span><span class="no">sold-out flavors</span></div>
    </div>
    <div>
      <div class="stat"><b>~2× more per visit</b>2× Combo pages earn 94–114 RSD per Meta visit; the homepage earns 54.</div>
      <ul class="tight" style="margin-top:6px">
        <li><b>Same promise as the ad</b> on the first screen</li>
        <li><b>Buy without scrolling</b> on a phone</li>
        <li><b>Only in-stock flavors</b>, price per kg</li>
        <li><b>Real reviews</b> near the top</li>
      </ul>
    </div>
  </div>

  <div class="foot"><span>Based on Yea Protein GA4 and Meta Ads, Sep 2025 – Oct 2026. Multipliers are starting points; adjust with rule 3.</span><span>1 / 2</span></div>
</section>
"""

# =================== PAGE 2: calendar ===================
# (n, when, name, level 1-4, label, peak, message, ads, offer, landing)
rows = [
    (1, "now – 19 Nov", "Restock + test", 1, "1×", False,
     "„Omiljeni ukus je opet tu.“<span class=gl>Your favorite flavor is back.</span>",
     "Best-seller flavors + test 4–6 posni ads (recipe, routine, flavor carousel, Combo value, creators)",
     "Sour Cherry + EasyGut gift to 8 Nov · 2× Combos back after restock",
     "Product page, flavor pre-selected · Sour Cherry → /akcije"),
    (2, "20 – 26 Nov", "Spremi se za post", 2, "1.5×", False,
     "„Post počinje 28.11. Spremi se.“<span class=gl>The fast starts 28 Nov. Get ready.</span>",
     "Winning posni ads + Combo carousel and stories",
     "2× Combo, any two flavors",
     "<b>/posni-protein</b> (goes live) · Combo ads → 2× Combo page"),
    (3, "27 – 30 Nov", "Black Friday", 4, "3×", True,
     "„Najbolja cena ove godine.“<span class=gl>Best price of the year.</span>",
     "Offer static + carousel, countdown stories, best sellers",
     "Black Friday discount incl. Combos · needs client OK",
     "/posni-protein with a code banner"),
    (4, "1 Dec – 6 Jan", "Božićni post", 3, "2×", True,
     "„Posni protein za ceo post.“<span class=gl>Protein for the whole fast.</span>",
     "Posni winners, posni breakfast recipes, creator partnership ads; new hooks every 2 weeks",
     "2× Combos, no extra discount",
     "<b>/posni-protein</b>"),
    (5, "7 Jan – 28 Feb", "Off-season", 1, "1×", False,
     "„Protein za svaki dan.“<span class=gl>Protein for every day.</span>",
     "Best sellers, breakfast and training use · from mid-Feb test the next Lent ads",
     "Singles + 2× Combos",
     "Product pages · 2× Combo page"),
    (6, "1 – 14 Mar", "Build-up to Lent", 2, "1.5×", False,
     "„Veliki post počinje 15.3. Spremi se.“<span class=gl>Lent starts 15 Mar. Stock up.</span>",
     "Lent teaser + the best new Lent test ads",
     "2× Combo; 3× only as an upsell on the page",
     "<b>/posni-protein</b> (Lent version)"),
    (7, "15 Mar – 4 Apr", "Lent weeks 1–3", 4, "3×", True,
     "„Posni protein koji je stvarno ukusan.“<span class=gl>Posni protein that actually tastes good.</span>",
     "Posni hero ads, recipe carousel, creators · scale while revenue holds",
     "Lent 2× Combo bundle (needs client OK if discounted)",
     "<b>/posni-protein</b>"),
    (8, "5 Apr – 1 May", "Rest of Lent", 3, "2×", True,
     "„Pola posta je iza tebe. Ne ostani bez zaliha.“<span class=gl>Halfway through. Don't run out.</span>",
     "Same winners with fresh hooks weekly · refill ads for March buyers",
     "2× Combos",
     "<b>/posni-protein</b> · refill → their flavor"),
    (9, "from 2 May", "After Easter", 1, "1×", False,
     "„Protein za svaki dan.“<span class=gl>Protein for every day.</span>",
     "Everyday protein: breakfast, training, taste · test new ads",
     "Singles + 2× Combos",
     "Product pages · 2× Combo page"),
]
LV = {1: 1.0, 2: 1.5, 3: 2.0, 4: 3.0}
PH = [(1, 24), (2, 7), (3, 4), (4, 37), (5, 53), (6, 14), (7, 21), (8, 27), (9, 30)]


def strip():
    W, x0, x1, yb, yt = 700, 6, 694, 88, 40
    total = sum(d for _, d in PH)
    sx = (x1 - x0) / total
    y = lambda v: yb - v / 3 * (yb - yt)
    s, x = [], x0
    for (n, days), r in zip(PH, rows):
        lev, lab, peak = LV[r[3]], r[4], r[5]
        w = days * sx
        s.append(f'<rect x="{x+1}" y="{y(lev)}" width="{w-2}" height="{yb-y(lev)}" rx="3" fill="{PLUM if peak else GRAY}"/>')
        cx = x + w / 2
        s.append(f'<circle cx="{cx}" cy="{y(lev)-11}" r="6.5" fill="{PLUM if peak else "#b9b1c9"}"/>')
        s.append(t(cx, y(lev) - 8.5, str(n), 7.4, "#fff", "middle", 800))
        if w > 24:
            s.append(t(cx, yb - 4, lab, 7.8, "#fff" if peak else INK2, "middle", 800))
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
    return f'<svg viewBox="0 0 {W} 102" role="img" aria-label="Season phases and relative budget level">{"".join(s)}</svg>'


tr = []
for n, when, name, lv, lab, peak, msg, ads, offer, lp in rows:
    tr.append(f'<tr class="{"peak" if peak else ""}"><td class="when"><span class="num{"" if peak else " base"}">{n}</span><b>{name}</b>{when}</td>'
              f'<td><span class="bud2">{lab}</span><br>{lvl(lv)}</td><td class="msg">{msg}</td><td>{ads}</td><td>{offer}</td><td>{lp}</td></tr>')

p2 = f"""
<section class="page">
  <div class="head2">
    <div><div class="eyebrow">Yea Protein · ads calendar</div><h1>What runs when, and what we say</h1></div>
    <div style="font-size:7pt;color:var(--muted);text-align:right">Budget = multiple of a normal week (1×)<br>Purple = fasting peaks</div>
  </div>
  <div class="card" style="margin-top:6px">{strip()}</div>

  <table class="cal" style="margin-top:6px">
    <colgroup><col style="width:80px"><col style="width:42px"><col style="width:17%"><col style="width:24%"><col style="width:19%"><col></colgroup>
    <tr><th>When</th><th>Budget</th><th>What we say</th><th>Ads</th><th>Offer</th><th>Landing page</th></tr>
    {"".join(tr)}
  </table>

  <div class="lanes4">
    <div class="lane"><b>Always on</b><p>One prospecting campaign (Advantage+ Sales, broad Serbia) + one retargeting campaign. Add new ads to them; don't relaunch.</p></div>
    <div class="lane c"><b>Retargeting</b><p>~20% of budget in every phase: cart, visitors, and refill (500g after ~2 weeks, 1kg after ~4).</p></div>
    <div class="lane g"><b>Google Search</b><p>Brand terms all year. Add "posni protein" and "veganski protein" during the fasts and their build-up.</p></div>
    <div class="lane c"><b>Before every phase</b><p>Check the stock light on page 1. Red overrides the calendar: retargeting only until restocked.</p></div>
  </div>

  <div class="foot"><span>Orthodox calendar: Božićni post 28 Nov – 6 Jan, Lent 15 Mar – 1 May 2027 (Easter 2 May). Offers marked "needs client OK" change prices.</span><span>2 / 2</span></div>
</section>
"""

(OUT / "yea_rules.html").write_text(page2(p1, "Yea Budget Rules"))
(OUT / "yea_calendar.html").write_text(page2(p2, "Yea Ads Calendar"))
print("built")
