#!/usr/bin/env python3
"""Flag Meta ads against the playbook benchmarks.

Input: a CSV with one row per ad (Ads Manager export, or rows built from the
Meta Ads MCP). Column names are matched loosely, so a raw Ads Manager export works.

Usage:
  python meta_flags.py ads.csv --mode daily|weekly|test \
      [--target-cpa 30] [--breakeven-cpa 60] [--aov 100] [--cap 1000] \
      [--prev prev_period.csv] [--json out.json]

Prints a markdown report to stdout.
"""
import argparse, csv, json, re, sys

# ---- thresholds (from the playbook; edit here to change every skill) ----
CTR_MIN = 0.02        # CTR (all)
LINK_RATIO_MIN = 0.5  # link CTR / CTR (all)
CPM_REF = 30.0        # typical CPM; flag if > 1.5x this (or > 1.3x own prior period)
LPV_MIN = 0.9         # landing page views / link clicks  (assumption: "small gap")
ATC_MIN = 0.10        # adds to cart / landing page views
CART_MIN = 0.5        # checkouts / adds to cart
CHK_MIN = 0.5         # purchases / checkouts
FREQ_MAX = 3.0        # prospecting frequency warning over 7 days (assumption)
CPM_SPIKE = 1.3       # vs prior period
CTR_DROP = 0.75       # CTR now < 75% of prior period -> fatigue signal

ALIASES = {
    "ad": ["ad name", "ad_name", "name"],
    "adset": ["ad set name", "adset name", "adset_name", "ad set"],
    "campaign": ["campaign name", "campaign_name", "campaign"],
    "status": ["ad delivery", "delivery", "effective_status", "status"],
    "spend": ["amount spent", "spend", "amount_spent"],
    "impr": ["impressions"],
    "reach": ["reach"],
    "freq": ["frequency"],
    "clicks_all": ["clicks (all)", "clicks_all", "clicks"],
    "link_clicks": ["link clicks", "link_clicks", "inline_link_clicks"],
    "lpv": ["landing page views", "landing_page_views", "content views", "content_views"],
    "atc": ["adds to cart", "add to cart", "adds_to_cart", "add_to_cart"],
    "chk": ["checkouts initiated", "initiate checkout", "checkouts_initiated", "initiate_checkout"],
    "purch": ["purchases", "purchase", "website purchases"],
    "rev": ["purchases conversion value", "purchase conversion value", "conversion value", "revenue", "purchase_value"],
}


def norm(s):
    return re.sub(r"\s+", " ", re.sub(r"\(.*?\)", "", s or "").strip().lower())


def map_columns(header):
    m = {}
    nh = [(h, norm(h)) for h in header]
    for key, names in ALIASES.items():
        for name in names:
            hit = next((h for h, n in nh if n == name), None) or \
                  next((h for h, n in nh if n.startswith(name)), None)
            if hit and hit not in m.values():
                m[key] = hit
                break
    return m


def num(v):
    if v is None:
        return 0.0
    v = str(v).replace(",", "").replace("$", "").replace("€", "").replace("%", "").strip()
    try:
        return float(v)
    except ValueError:
        return 0.0


def load(path):
    with open(path, newline="", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        return [], {}
    m = map_columns(rows[0].keys())
    out = []
    for r in rows:
        d = {k: (r.get(m[k]) if k in m else None) for k in ALIASES}
        for k in ["spend", "impr", "reach", "freq", "clicks_all", "link_clicks", "lpv", "atc", "chk", "purch", "rev"]:
            d[k] = num(d[k])
        d["ad"] = d["ad"] or "(unnamed ad)"
        if d["impr"] > 0 or d["spend"] > 0:
            out.append(d)
    return out, m


def div(a, b):
    return a / b if b else None


def metrics(d):
    d["ctr"] = div(d["clicks_all"], d["impr"])
    d["lctr"] = div(d["link_clicks"], d["impr"])
    d["ratio"] = div(d["lctr"], d["ctr"]) if d["ctr"] else None
    d["cpm"] = div(d["spend"], d["impr"] / 1000) if d["impr"] else None
    d["cpc"] = div(d["spend"], d["link_clicks"])
    d["lpv_rate"] = div(d["lpv"], d["link_clicks"])
    d["atc_rate"] = div(d["atc"], d["lpv"])
    d["cart_rate"] = div(d["chk"], d["atc"])
    d["chk_rate"] = div(d["purch"], d["chk"])
    d["cpa"] = div(d["spend"], d["purch"])
    d["roas"] = div(d["rev"], d["spend"])
    d["aov"] = div(d["rev"], d["purch"])
    return d


STAGES = [  # (name, metric key, threshold, min denominator to judge, what to check)
    ("Attention", "ctr", CTR_MIN, ("impr", 500),
     "Hook / first 1–3 seconds / first frame. Lead with the customer's problem, not the brand."),
    ("Interest", "ratio", LINK_RATIO_MIN, ("clicks_all", 20),
     "People engage but don't click: benefit unclear, weak offer or CTA. Run a copy test on this ad."),
    ("Page load", "lpv_rate", LPV_MIN, ("link_clicks", 20),
     "Clicks never become page views: page speed, mobile layout, pixel/tracking, accidental clicks."),
    ("Buying intent", "atc_rate", ATC_MIN, ("lpv", 50),
     "Page doesn't continue the ad's promise: check ad-to-page match, reviews, in-use photos, price, CTA. Try a landing page test."),
    ("Cart", "cart_rate", CART_MIN, ("atc", 10),
     "Cart friction: shipping shown late, upsell clutter, checkout button hidden on mobile."),
    ("Checkout", "chk_rate", CHK_MIN, ("chk", 6),
     "Last-step doubt: payment options, trust, delivery time. Bottom retargeting with reviews / 5% off 24h."),
]


def first_leak(d):
    for name, key, th, (den, mn), check in STAGES:
        if d[den] < mn:
            return None, f"not enough data yet ({den.replace('_', ' ')} < {mn})"
        v = d[key]
        if v is not None and v < th:
            return name, check
    return "OK", ""


def pct(v, dp=1):
    return "–" if v is None else f"{v*100:.{dp}f}%"


def money(v):
    return "–" if v is None else f"${v:,.2f}" if v < 100 else f"${v:,.0f}"


def classify(d, a, prev):
    """Return (severity, headline, where, check). severity: RED / AMBER / GREEN / GREY."""
    tcpa, becpa, cap, mode = a.target_cpa, a.breakeven_cpa, a.cap, a.mode
    issues = []
    # --- money bleed (most urgent) ---
    kill_line = becpa or (tcpa * 2 if tcpa else None)
    if kill_line and d["purch"] == 0 and d["spend"] >= kill_line:
        issues.append(("RED", f"Spent {money(d['spend'])} with 0 purchases (≥ {'break-even' if becpa else '2× target'} CPA)",
                       "Result", "Turn off unless it's a new test still below the impression cap. Check where it leaks below."))
    elif becpa and d["cpa"] and d["cpa"] > becpa and d["purch"] >= 1:
        issues.append(("RED", f"CPA {money(d['cpa'])} above break-even {money(becpa)}",
                       "Result", "Losing money on every sale. Cut or fix the first leak below; raise AOV if the whole account is here."))
    elif tcpa and d["cpa"] and d["cpa"] > tcpa:
        issues.append(("AMBER", f"CPA {money(d['cpa'])} above target {money(tcpa)}",
                       "Result", "Profitable but off target. Watch 3 more days; if it stays, cut it and move budget to winners."))
    # --- test ads past the cap ---
    if mode == "test" or "ct" in (d.get("campaign") or "").lower().split() or "creative test" in (d.get("campaign") or "").lower():
        if d["impr"] >= cap:
            issues.append(("AMBER", f"Test ad reached {int(d['impr']):,} impressions (cap {cap:,})",
                           "Test", "Should be off now so other ads get spend. Check the rule is set to run 'continuously'."))
    # --- funnel ---
    leak, check = first_leak(d)
    if leak and leak != "OK":
        sev = "RED" if leak in ("Attention", "Buying intent") and d["spend"] >= (tcpa or 30) else "AMBER"
        issues.append((sev, f"First leak: {leak}", leak, check))
    # --- cost ---
    if d["cpm"] and d["cpm"] > CPM_REF * 1.5:
        issues.append(("AMBER", f"CPM {money(d['cpm'])} is high", "Cost",
                       "Judge against CTR: fine if CTR/link CTR are strong. Otherwise the creative or audience is costly to deliver."))
    # --- trends vs previous period ---
    p = prev.get(d["ad"]) if prev else None
    if p:
        if p["cpm"] and d["cpm"] and d["cpm"] > p["cpm"] * CPM_SPIKE:
            issues.append(("AMBER", f"CPM up {((d['cpm']/p['cpm'])-1)*100:.0f}% vs last period", "Cost",
                           "Possible fatigue or audience saturation. Check frequency and CTR trend."))
        if p["ctr"] and d["ctr"] and d["ctr"] < p["ctr"] * CTR_DROP:
            issues.append(("AMBER", f"CTR down {(1-d['ctr']/p['ctr'])*100:.0f}% vs last period", "Attention",
                           "Creative fatigue: brief a variation of this winner (new hook, creator or format; one change)."))
    if d["freq"] and d["freq"] > FREQ_MAX and mode != "daily":
        issues.append(("AMBER", f"Frequency {d['freq']:.1f}", "Fatigue",
                       "Same people seeing it too often. Refresh creative or widen the audience (prospecting only)."))
    if not issues:
        if leak is None:
            return "GREY", "Too little data to judge", "–", check
        return "GREEN", "Healthy", "–", "Keep. Candidate for more budget if CPA ≤ target."
    order = {"RED": 0, "AMBER": 1}
    issues.sort(key=lambda x: order[x[0]])
    sev = issues[0][0]
    return sev, "; ".join(i[1] for i in issues), " → ".join(dict.fromkeys(i[2] for i in issues)), " ".join(dict.fromkeys(i[3] for i in issues))


def verdict_test(d, a):
    if d["impr"] < a.cap:
        return "RUNNING", f"{int(d['impr']):,}/{a.cap:,} impressions"
    ok_attn = (d["ctr"] or 0) >= CTR_MIN
    ok_int = (d["ratio"] or 0) >= LINK_RATIO_MIN
    buys = d["purch"] > 0 or d["atc"] > 0
    if ok_attn and ok_int and buys:
        return "WINNER", "passes CTR + link CTR and shows buying"
    if ok_attn and ok_int:
        return "WATCH", "good attention/click, no carts or sales yet: retest or use in retargeting"
    if not ok_attn:
        return "CUT", "CTR below 2%: doesn't stop the scroll"
    return "CUT", "link CTR under half of CTR: attention without intent"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("csv")
    ap.add_argument("--mode", choices=["daily", "weekly", "test"], default="weekly")
    ap.add_argument("--target-cpa", type=float)
    ap.add_argument("--breakeven-cpa", type=float)
    ap.add_argument("--aov", type=float)
    ap.add_argument("--cap", type=int, default=1000)
    ap.add_argument("--prev")
    ap.add_argument("--json")
    a = ap.parse_args()

    ads, colmap = load(a.csv)
    missing = [k for k in ["spend", "impr", "clicks_all", "link_clicks", "purch"] if k not in colmap]
    ads = [metrics(d) for d in ads]
    prev = {}
    if a.prev:
        prev = {d["ad"]: metrics(d) for d in load(a.prev)[0]}

    out = []
    if missing:
        out.append(f"> ⚠️ Missing columns: {', '.join(missing)}. Flags that need them are skipped.\n")

    # account totals
    tot = {k: sum(d[k] for d in ads) for k in ["spend", "impr", "clicks_all", "link_clicks", "lpv", "atc", "chk", "purch", "rev"]}
    tot.update(ad="ACCOUNT", freq=0, campaign="", adset="", status="")
    tot = metrics(tot)
    leak, check = first_leak(tot)
    be_roas = (a.aov / a.breakeven_cpa) if a.aov and a.breakeven_cpa else None
    out.append("## Account snapshot")
    out.append(f"Spend {money(tot['spend'])} · Purchases {int(tot['purch'])} · CPA {money(tot['cpa'])} · ROAS {tot['roas']:.2f}x" if tot['roas'] else
               f"Spend {money(tot['spend'])} · Purchases {int(tot['purch'])} · CPA {money(tot['cpa'])}")
    out.append(f"CTR {pct(tot['ctr'],2)} · Link CTR {pct(tot['lctr'],2)} (ratio {pct(tot['ratio'],0)}) · CPM {money(tot['cpm'])} · "
               f"LPV/click {pct(tot['lpv_rate'],0)} · ATC {pct(tot['atc_rate'])} · Cart→checkout {pct(tot['cart_rate'],0)} · Checkout→purchase {pct(tot['chk_rate'],0)}")
    if be_roas and tot["roas"]:
        state = "below break-even (losing money)" if tot["roas"] < be_roas else ("in scale zone" if tot["roas"] >= be_roas * 1.5 else "profitable, below scale zone")
        out.append(f"Break-even ROAS {be_roas:.2f}x → account is **{state}**.")
    out.append(f"**Account first leak: {leak or 'not enough data'}**" + (f" — {check}" if leak and leak != 'OK' else ""))
    active = [d for d in ads if d["spend"] > 0]
    out.append(f"Ads with spend: {len(active)}. Top 3 ads take {pct(sum(sorted([d['spend'] for d in active], reverse=True)[:3]) / tot['spend'] if tot['spend'] else None, 0)} of spend.\n")

    rows = []
    if a.mode == "test":
        out.append("## Creative test verdicts")
        out.append("| Verdict | Ad | Impr. | CTR | Link CTR | Ratio | CPM | Carts | Purch. | Why |")
        out.append("|---|---|---|---|---|---|---|---|---|---|")
        ranked = []
        for d in ads:
            v, why = verdict_test(d, a)
            ranked.append((v, d, why))
        order = {"WINNER": 0, "WATCH": 1, "RUNNING": 2, "CUT": 3}
        ranked.sort(key=lambda x: (order[x[0]], x[1]["cpc"] or 9e9))
        icon = {"WINNER": "🟢", "WATCH": "🟡", "RUNNING": "⏳", "CUT": "🔴"}
        for v, d, why in ranked:
            out.append(f"| {icon[v]} {v} | {d['ad']} | {int(d['impr']):,} | {pct(d['ctr'],2)} | {pct(d['lctr'],2)} | {pct(d['ratio'],0)} | {money(d['cpm'])} | {int(d['atc'])} | {int(d['purch'])} | {why} |")
            rows.append({"ad": d["ad"], "verdict": v, "why": why})
        winners = [d["ad"] for v, d, _ in ranked if v == "WINNER"]
        if winners:
            out.append("\n**Allocation:** " + " · ".join(
                f"#{i+1} {w} → " + ("copy + landing page tests, prospecting" if i == 0 else "prospecting" if i < 3 else "middle retargeting" if i < 5 else "bottom retargeting")
                for i, w in enumerate(winners)))
    else:
        out.append("## Ad flags")
        out.append("| | Ad | Campaign | Spend | CTR | Link CTR | CPM | ATC | CPA | Problem | Where | What to check |")
        out.append("|---|---|---|---|---|---|---|---|---|---|---|---|")
        icon = {"RED": "🔴", "AMBER": "🟡", "GREEN": "🟢", "GREY": "⚪"}
        res = []
        for d in ads:
            sev, head, where, check = classify(d, a, prev)
            res.append((sev, d, head, where, check))
        order = {"RED": 0, "AMBER": 1, "GREEN": 2, "GREY": 3}
        res.sort(key=lambda x: (order[x[0]], -x[1]["spend"]))
        for sev, d, head, where, check in res:
            out.append(f"| {icon[sev]} | {d['ad']} | {d.get('campaign') or ''} | {money(d['spend'])} | {pct(d['ctr'],2)} | {pct(d['lctr'],2)} | {money(d['cpm'])} | {pct(d['atc_rate'])} | {money(d['cpa'])} | {head} | {where} | {check} |")
            rows.append({"ad": d["ad"], "campaign": d.get("campaign"), "severity": sev, "problem": head, "where": where, "check": check,
                         "spend": d["spend"], "cpa": d["cpa"], "ctr": d["ctr"], "link_ctr": d["lctr"], "atc_rate": d["atc_rate"]})
        counts = {s: sum(1 for r in res if r[0] == s) for s in order}
        out.insert(0, f"**{counts['RED']} 🔴 act now · {counts['AMBER']} 🟡 watch · {counts['GREEN']} 🟢 healthy · {counts['GREY']} ⚪ too early**\n")

    print("\n".join(out))
    if a.json:
        with open(a.json, "w") as f:
            json.dump({"account": {k: tot[k] for k in tot if isinstance(tot[k], (int, float)) or tot[k] is None}, "account_first_leak": leak, "ads": rows}, f, indent=1, default=str)


if __name__ == "__main__":
    main()
