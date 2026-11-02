"""Yea Protein monthly budget plan Nov 2026 - Oct 2027: budget, predicted orders, blended CPA, tubs needed.
Actuals: GA4 orders/revenue (RSD), Meta spend on the Yea account minus the EasyGut campaign, Google Ads spend.
"""
from pathlib import Path
from build2 import CSS, t, PLUM, GRAY, INK, INK2, MUTED, CHERRY

OUT = Path(__file__).parent
RSD_EUR = 117.2

# month, orders, revenue RSD, Meta Yea EUR (account minus EasyGut campaign), Google EUR, fast month?
ACT = [
    ("Sep 25", 302, 1338823, 4642 - 0, 545, False),
    ("Oct 25", 298, 1360046, 3909, 397, False),
    ("Nov 25", 430, 1870744, 3783, 312, True),
    ("Dec 25", 385, 1621082, 6423, 405, False),
    ("Jan 26", 276, 1271591, 4114, 386, False),
    ("Feb 26", 528, 2269484, 2928 - 78, 759, True),
    ("Mar 26", 601, 2563886, 3630 - 405, 991, True),
    ("Apr 26", 258, 1190632, 3521 - 963, 660, False),
    ("May 26", 229, 1034337, 3089 - 636, 252, False),
    ("Jun 26", 235, 1127850, 2903 - 1380, 289, False),
    ("Jul 26", 184, 953790, 1211 - 156, 243, False),
    ("Aug 26", 137, 627629, 1015, 195, False),
    ("Sep 26", 118, 470543, 527, 147, False),
    ("Oct 26", 81, 346401, 507, 100, False),
]
for i, (m, o, r, me, g, f) in enumerate(ACT):
    ACT[i] = dict(m=m, orders=o, rev=r / RSD_EUR, meta=me, google=g, spend=me + g, cpa=(me + g) / o, fast=f)

AOV = sum(a["rev"] for a in ACT) / sum(a["orders"] for a in ACT)

# month, days, what happens, Meta, Google, planned blended CPA, tubs per order, max budget if CPA holds, kind
PLAN = [
    ("Nov 26", 30, "Restock, then Black Friday 27.11 and Božićni post from 28.11", 2500, 300, 11.0, 1.7, 3400, "fast"),
    ("Dec 26", 31, "Božićni post: strong 1–15 Dec, weak over the holidays", 2700, 300, 11.5, 1.8, 3600, "fast"),
    ("Jan 27", 31, "Fast ends 6 Jan. Off-season, new-year routine", 1550, 250, 10.0, 1.6, 2200, "off"),
    ("Feb 27", 28, "Off-season. Test Lent ads from mid-Feb", 1550, 250, 10.0, 1.6, 2200, "off"),
    ("Mar 27", 31, "Build-up 1–14 Mar, Lent from 15 Mar (week 1 = peak)", 3600, 600, 8.0, 1.9, 5000, "peak"),
    ("Apr 27", 30, "Lent all month (Easter 2 May)", 3400, 600, 8.5, 1.9, 5000, "peak"),
    ("May 27", 31, "Easter, then the post-fast drop", 1350, 250, 10.0, 1.6, 2000, "off"),
    ("Jun 27", 30, "Summer off-season", 1250, 250, 10.0, 1.6, 1800, "off"),
    ("Jul 27", 31, "Summer off-season", 1250, 250, 10.0, 1.6, 1800, "off"),
    ("Aug 27", 31, "Summer off-season", 1250, 250, 10.0, 1.6, 1800, "off"),
    ("Sep 27", 30, "Autumn off-season. Test new ads", 1550, 250, 10.0, 1.6, 2200, "off"),
    ("Oct 27", 31, "Off-season. Brief Black Friday + fast creatives", 1550, 250, 10.0, 1.6, 2200, "off"),
]


def eur(v, k=False):
    if k:
        return f"€{v / 1000:.1f}k"
    return "€{:,.0f}".format(v)


def chart_history():
    W, H, x0, x1, yb, yt = 400, 182, 26, 396, 150, 14
    n = len(ACT)
    bw = (x1 - x0) / n
    vmax = 20
    y = lambda v: yb - v / vmax * (yb - yt)
    s = []
    for v in (5, 10, 15, 20):
        s.append(f'<line x1="{x0}" x2="{x1}" y1="{y(v)}" y2="{y(v)}" stroke="#ebe5dc"/>')
        s.append(t(x0 - 4, y(v) + 2.5, f"€{v}", 6.2, MUTED, "end"))
    # target band
    s.append(f'<rect x="{x0}" y="{y(12)}" width="{x1 - x0}" height="{y(0) - y(12)}" fill="#e5f3ea" opacity=".55"/>')
    s.append(t(x1 - 2, y(12) - 3, "target: €12 or less", 6.2, "#2f7d4a", "end", 700))
    for i, a in enumerate(ACT):
        cx = x0 + bw * i + bw / 2
        col = PLUM if a["fast"] else ("#c9c1d6" if a["spend"] < 2000 else "#9a92ab")
        s.append(f'<rect x="{cx - bw * .32:.1f}" y="{y(a["cpa"]):.1f}" width="{bw * .64:.1f}" height="{yb - y(a["cpa"]):.1f}" rx="2" fill="{col}"/>')
        s.append(t(cx, y(a["cpa"]) - 3, f"{a['cpa']:.0f}", 6.4, INK, "middle", 700))
        s.append(t(cx, yb + 9, a["m"].split()[0], 6.2, INK2, "middle"))
        s.append(t(cx, yb + 17, f"{a['spend'] / 1000:.1f}k", 5.8, MUTED, "middle"))
    s.append(f'<line x1="{x0}" x2="{x1}" y1="{yb}" y2="{yb}" stroke="{MUTED}"/>')
    s.append(t(x0 - 4, yb + 17, "spend", 5.8, MUTED, "end"))
    s.append(t(x0 + bw * 0.1, yb + 27, "2025", 5.8, MUTED))
    s.append(t(x0 + bw * 4.1, yb + 27, "2026", 5.8, MUTED))
    return f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="Cost per order by month">{"".join(s)}</svg>'


def plan_rows():
    out, tot = [], dict(b=0, o=0, rev=0, tubs=0, mx=0)
    for m, days, what, meta, goog, cpa, upo, mx, kind in PLAN:
        b = meta + goog
        o = b / cpa
        rev = o * AOV
        tubs = o * upo
        tot["b"] += b; tot["o"] += o; tot["rev"] += rev; tot["tubs"] += tubs; tot["mx"] += mx
        tag = {"peak": '<span class="pill no">peak</span>', "fast": '<span class="pill q">fast</span>', "off": ""}[kind]
        out.append(
            f'<tr class="{kind}"><td><b>{m}</b> {tag}</td><td>{what}</td>'
            f'<td class="r"><b>{eur(b)}</b></td><td class="r">{eur(meta / days)}/day</td><td class="r">{eur(goog)}</td>'
            f'<td class="r"><b>{o:.0f}</b> <span class="rng">{o * .8:.0f}–{o * 1.2:.0f}</span></td>'
            f'<td class="r"><b>€{cpa:.0f}</b><span class="rng">{"" if cpa == int(cpa) else ""}</span></td>'
            f'<td class="r">{eur(rev, True)}</td><td class="r">{tubs:.0f}</td><td class="r">{eur(mx)}</td></tr>')
    out.append(
        f'<tr class="tot"><td>12 months</td><td></td><td class="r">{eur(tot["b"])}</td><td></td><td></td>'
        f'<td class="r">{tot["o"]:,.0f}</td><td class="r">€{tot["b"] / tot["o"]:.1f}</td>'
        f'<td class="r">{eur(tot["rev"], True)}</td><td class="r">{tot["tubs"]:,.0f}</td><td class="r">{eur(tot["mx"])}</td></tr>')
    return "".join(out), tot


rows, TOT = plan_rows()
last12 = ACT[:12]
L_SPEND = sum(a["spend"] for a in last12)
L_ORD = sum(a["orders"] for a in last12)
L_REV = sum(a["rev"] for a in last12)

CSS5 = CSS + """
  .kpis{display:grid;grid-template-columns:repeat(4,1fr);gap:6px;margin-top:6px}
  .kpi{background:var(--card);border:1px solid var(--line);border-radius:9px;padding:6px 9px}
  .kpi .v{font-family:Fraunces,serif;font-size:15pt;font-weight:600;line-height:1.1;color:var(--plum)}
  .kpi .s{font-size:6.8pt;color:var(--ink2);line-height:1.3}
  .kpi .s b{color:var(--ink)}
  .rules{display:grid;gap:5px}
  .rule{background:var(--card);border:1px solid var(--line);border-radius:9px;padding:6px 9px;font-size:7pt;color:var(--ink2);line-height:1.38}
  .rule h4{font-size:8pt;color:var(--ink);font-weight:800;margin-bottom:2px}
  .rule b{color:var(--ink)}
  .rule .g{color:#2f7d4a;font-weight:800} .rule .y{color:#8a5a00;font-weight:800} .rule .r{color:var(--cherry);font-weight:800}
  table.plan td{font-size:6.9pt;padding:3.4px 5px;vertical-align:middle;line-height:1.25}
  table.plan th{font-size:5.9pt;padding:4px 5px}
  table.plan tr.peak td{background:#f6f2fb} table.plan tr.fast td{background:#fcf8f0}
  .rng{display:block;font-size:5.8pt;color:var(--muted);font-weight:500}
  .pill{display:inline-block;font-size:5.6pt;font-weight:800;text-transform:uppercase;letter-spacing:.04em;padding:0 5px;border-radius:8px;margin-left:2px;vertical-align:1px}
  .leg{display:flex;gap:10px;font-size:6.3pt;color:var(--ink2);margin-top:2px}
  .leg i{display:inline-block;width:9px;height:9px;border-radius:2px;margin-right:4px;vertical-align:-1px}
"""

html = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Yea Budget Plan</title>
<link href="fonts/fonts.css" rel="stylesheet"><style>{CSS5}</style></head><body>
<section class="page">
  <div class="hero"><div class="txt">
    <div class="eyebrow">Yea Protein · ads budget · Nov 2026 – Oct 2027</div>
    <h1>Budget plan, month by month</h1>
    <p>Built from 14 months of real spend and shop orders.</p>
  </div></div>

  <div class="kpis">
    <div class="kpi"><div class="v">{eur(TOT['b'])}</div><div class="s">ads for 12 months (Meta + Google). Last 12 months: <b>{eur(L_SPEND)}</b></div></div>
    <div class="kpi"><div class="v">~{TOT['o']:,.0f}</div><div class="s">orders predicted. Last 12 months: <b>{L_ORD:,}</b></div></div>
    <div class="kpi"><div class="v">€{TOT['b'] / TOT['o']:.1f}</div><div class="s">blended cost per order. Last 12 months: <b>€{L_SPEND / L_ORD:.1f}</b></div></div>
    <div class="kpi"><div class="v">{TOT['rev'] / TOT['b']:.1f}×</div><div class="s">revenue ÷ ad spend. Last 12 months: <b>{L_REV / L_SPEND:.1f}×</b></div></div>
  </div>

  <div class="grid2" style="grid-template-columns:1.25fr 1fr;margin-top:7px">
    <div class="card">
      <h2 style="margin:0 0 2px">What an order really cost <small>all ad spend ÷ all shop orders, per month</small></h2>
      {chart_history()}
      <div class="leg"><span><i style="background:{PLUM}"></i>fast months</span><span><i style="background:#9a92ab"></i>off-season, €2k+ spend</span><span><i style="background:#c9c1d6"></i>off-season, under €2k</span></div>
      <p class="note">Fasts cost €7–10 an order. Off-season months with €4–7k budgets cost €14–18, because extra money off-season buys few extra orders. Under €2k off-season stays at €7–9.</p>
    </div>
    <div class="rules">
      <div class="rule"><h4>How much per season</h4>
        <b>Peak (Lent):</b> €4–5k a month, about €115–150 a day on Meta.<br>
        <b>Fast (Božićni post, BF):</b> €2.8–3.6k a month.<br>
        <b>Off-season:</b> €1.5–1.8k a month. More than ~€2k off-season wastes money.<br>
        <b>Google:</b> Brand €250 every month, +€350 "posni protein" search in Lent.</div>
      <div class="rule"><h4>Weekly check: cost per order</h4>
        Total ad spend that week ÷ all WooCommerce orders that week.<br>
        <span class="g">Under €10</span> → raise budget +20% (up to the "max" column).<br>
        <span class="y">€10–13</span> → hold, swap in fresh ads.<br>
        <span class="r">Over €13 for 7 days</span> → cut 20%. Never above €15 (that is under 2.5× return).</div>
      <div class="rule"><h4>Stock decides first</h4>
        If Chocolate or Vanilla Caramel is out, run the off-season budget whatever the month says. Order tubs for the next two months before each fast (column "Tubs").</div>
    </div>
  </div>

  <h2>The plan, month by month <small>budget = Meta + Google · orders = budget ÷ planned cost per order, ±20%</small></h2>
  <table class="plan">
    <colgroup><col style="width:58px"><col><col style="width:46px"><col style="width:54px"><col style="width:40px"><col style="width:52px"><col style="width:38px"><col style="width:42px"><col style="width:34px"><col style="width:48px"></colgroup>
    <tr><th>Month</th><th>What happens</th><th class="r">Budget</th><th class="r">Meta</th><th class="r">Google</th><th class="r">Orders</th><th class="r">€/order</th><th class="r">Revenue</th><th class="r">Tubs</th><th class="r">Max budget</th></tr>
    {rows}
  </table>

  <div class="grid2" style="grid-template-columns:1fr 1fr 1fr;margin-top:6px">
    <div class="callout amber" style="font-size:7pt;line-height:1.4"><b>Lent moves later in 2027.</b> In 2026 Lent ran 23 Feb – 11 Apr, so Feb + Mar peaked. In 2027 it is 15 Mar – 1 May, so the peak is <b>mid-March + April</b>. Keep February at off-season budget.</div>
    <div class="callout amber" style="font-size:7pt;line-height:1.4"><b>Stock to have ready:</b> by 20 Nov about <b>{round(sum(o * u for (m, d, w, me, g, c, u, mx, k) in PLAN[:2] for o in [(me + g) / c]), -1):,.0f} tubs</b> for Nov–Dec. By 1 Mar about <b>{round(sum(o * u for (m, d, w, me, g, c, u, mx, k) in PLAN[4:6] for o in [(me + g) / c]), -1):,.0f} tubs</b> for Mar–Apr. Over half should be Chocolate + Vanilla Caramel.</div>
    <div class="callout amber" style="font-size:7pt;line-height:1.4"><b>Why ~€{(L_SPEND - TOT['b']) / 1000:.0f}k less than last year.</b> The cut comes from off-season months that cost €14–18 an order (Sep–Oct 2025, Dec, Jan). Fast months keep about last year's budget, and can go to the "Max budget" column if cost per order holds.</div>
  </div>

  <div class="foot"><span>Actuals Sep 2025 – Oct 2026: GA4 orders, Meta (minus EasyGut), Google Ads. Average order {AOV * RSD_EUR:,.0f} RSD ≈ €{AOV:.0f} at {RSD_EUR} RSD/€. Tubs assume Combos are back (1.6–1.9 per order). Conservative: orders are lower now (81 in Oct).</span><span style="white-space:nowrap">Nov 2026</span></div>
</section>
</body></html>"""

(OUT / "yea_budget_plan.html").write_text(html)
print("built", round(TOT["b"]), round(TOT["o"]), round(TOT["b"] / TOT["o"], 2), round(AOV, 2), round(L_SPEND), L_ORD)
