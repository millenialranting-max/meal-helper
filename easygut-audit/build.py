"""Builds audit.html + concepts.html for the EasyGut Meta audit PDFs.

Data: Meta Ads account "GenoMAX/EasyGut", 28 Aug - 25 Sep 2026 (pulled 25 Sep 2026).
"""
from pathlib import Path

OUT = Path(__file__).parent

# ---------- tokens ----------
PLUM, TEAL, GRAY = "#5b3fa0", "#2e8f6a", "#d6d0de"
INK, INK2, MUTED, GRID = "#1f1a2e", "#4d475c", "#847e92", "#ece7df"
CRIT = "#c0392b"


def bar_up(x, y, w, h, r=4):
    """Vertical bar with rounded top, anchored flat on the baseline."""
    r = min(r, h, w / 2)
    return (f"M{x},{y+h} L{x},{y+r} Q{x},{y} {x+r},{y} L{x+w-r},{y} "
            f"Q{x+w},{y} {x+w},{y+r} L{x+w},{y+h} Z")


def bar_right(x, y, w, h, r=4):
    """Horizontal bar with rounded right end, anchored flat on the left."""
    w = max(w, 2)
    r = min(r, w, h / 2)
    return (f"M{x},{y} L{x+w-r},{y} Q{x+w},{y} {x+w},{y+r} L{x+w},{y+h-r} "
            f"Q{x+w},{y+h} {x+w-r},{y+h} L{x},{y+h} Z")


def t(x, y, s, size=9, fill=INK2, anchor="start", weight=400, extra=""):
    return (f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" '
            f'text-anchor="{anchor}" font-weight="{weight}" {extra}>{s}</text>')


# ---------- chart 1: weekly ROAS ----------
def chart_weekly():
    weeks = [("W1", "28 Aug", 146, 5, 1.00), ("W2", "4 Sep", 153, 5, 1.16),
             ("W3", "11 Sep", 184, 4, 0.77), ("W4", "18 Sep", 282, 4, 0.31)]
    x0, x1, yb, yt, vmax = 34, 352, 150, 22, 2.0
    y = lambda v: yb - v / vmax * (yb - yt)
    s = []
    for g in (0, 0.5, 1.0, 1.5, 2.0):
        s.append(f'<line x1="{x0}" x2="{x1}" y1="{y(g)}" y2="{y(g)}" stroke="{GRID}" stroke-width="1"/>')
        s.append(t(x0 - 6, y(g) + 3, f"{g:.1f}", 8, MUTED, "end"))
    band = (x1 - x0) / 4
    bw = 36
    for i, (w, d, spend, sales, roas) in enumerate(weeks):
        cx = x0 + band * i + band / 2
        s.append(f'<path d="{bar_up(cx-bw/2, y(roas), bw, yb-y(roas))}" fill="{PLUM}"/>')
        s.append(t(cx, y(roas) - 5, f"{roas:.2f}", 10, INK, "middle", 700))
        s.append(t(cx, yb + 13, f"{w} · {d}", 8.5, INK2, "middle", 600))
        s.append(t(cx, yb + 25, f"€{spend} · {sales} sales", 8, MUTED, "middle"))
    be = y(1.67)
    s.append(f'<line x1="{x0}" x2="{x1}" y1="{be}" y2="{be}" stroke="{CRIT}" stroke-width="1.5" stroke-dasharray="4 3"/>')
    s.append(t(x1, be - 5, "break-even ≈ 1.7*", 8.5, CRIT, "end", 600))
    s.append(f'<line x1="{x0}" x2="{x1}" y1="{yb}" y2="{yb}" stroke="{MUTED}" stroke-width="1"/>')
    return f'<svg viewBox="0 0 360 180" role="img" aria-label="Weekly ROAS: 1.00, 1.16, 0.77, 0.31 against break-even 1.7">{"".join(s)}</svg>'


# ---------- chart 2: funnel ----------
def chart_funnel():
    rows = [("Link clicks", 1627, "", None), ("Page views", 382, "23%", False),
            ("Add to cart", 48, "12.6%", True), ("Checkout", 25, "52%", True),
            ("Purchase", 18, "72%", True)]
    lx, bx, bmax, rh, y0 = 78, 84, 176, 31, 16
    s = [t(356, 8, "step rate", 8, MUTED, "end")]
    for i, (lab, v, rate, ok) in enumerate(rows):
        yy = y0 + i * rh
        w = v / 1627 * bmax
        s.append(t(lx, yy + 14, lab, 9, INK2, "end", 500))
        s.append(f'<path d="{bar_right(bx, yy+3, w, 16)}" fill="{PLUM}"/>')
        s.append(t(bx + max(w, 2) + 5, yy + 15, f"{v:,}", 9.5, INK, "start", 700))
        if rate:
            col = CRIT if ok is False else "#2f7d4a"
            mark = "✗" if ok is False else "✓"
            s.append(t(356, yy + 15, f"{rate} {mark}", 9.5, col, "end", 700))
    # leak annotation
    s.append(f'<rect x="{bx+80}" y="{y0+rh+2}" width="124" height="19" rx="4" fill="#fbe9e7"/>')
    s.append(t(bx + 142, y0 + rh + 15, "← first leak: 77% not recorded", 8.2, CRIT, "middle", 700))
    return f'<svg viewBox="0 0 360 172" role="img" aria-label="Funnel 1627 clicks, 382 page views, 48 add to cart, 25 checkout, 18 purchases">{"".join(s)}</svg>'


# ---------- chart 3: spend by ad ----------
def chart_ads():
    ads = [("Day · pinned testimonial", "V", 392.69, "10 sales · ROAS 0.87", True),
           ("Forte · Miloš", "V", 66.54, "0 sales", False),
           ("Night · Tamara testimonial", "V", 60.15, "4 sales · ROAS 2.08", True),
           ("Day · Nataša", "V", 51.99, "1 sale · 0.42", False),
           ("Day · Teodora", "V", 48.33, "2 sales · 0.90", False),
           ("Day · “nadutost”", "V", 44.74, "1 sale · 0.46", False),
           ("Forte · pizza", "S", 44.41, "0 sales", False),
           ("Night · kasna večera", "S", 38.41, "0 sales", False),
           ("Combo Day+Night", "S", 26.34, "0 sales", False),
           ("Night · Tamara relaunch", "V", 8.99, "0 sales", False)]
    lx, bx, bmax, rh, y0 = 118, 136, 88, 17, 4
    s = []
    for i, (lab, f, v, res, hi) in enumerate(ads):
        yy = y0 + i * rh
        w = v / 392.69 * bmax
        s.append(t(lx, yy + 11, lab, 8.3, INK if hi else INK2, "end", 600 if hi else 400))
        badge_fill = "#ece6f7" if f == "V" else "#f3efe8"
        s.append(f'<rect x="{lx+3}" y="{yy+2}" width="12" height="11" rx="2.5" fill="{badge_fill}"/>')
        s.append(t(lx + 9, yy + 10.5, f, 7, PLUM if f == "V" else INK2, "middle", 700))
        s.append(f'<path d="{bar_right(bx, yy+2, w, 12, 3)}" fill="{PLUM if hi else GRAY}"/>')
        s.append(t(bx + w + 4, yy + 11, f"€{v:.0f}", 8.3, INK, "start", 600))
        s.append(t(358, yy + 11, res, 8.2, INK if hi else MUTED, "end", 600 if hi else 400))
    return f'<svg viewBox="0 0 360 176" role="img" aria-label="Spend by ad">{"".join(s)}</svg>'


# ---------- chart 4: age ----------
def chart_age():
    groups = [("18–34", 14.2, 16.7, 0.92), ("35–44", 34.6, 27.8, 0.40),
              ("45–54", 37.0, 27.8, 0.62), ("55+", 14.2, 27.8, 1.47)]
    x0, x1, yb, yt, vmax = 26, 356, 128, 26, 40
    y = lambda v: yb - v / vmax * (yb - yt)
    s = []
    for g in (0, 20, 40):
        s.append(f'<line x1="{x0}" x2="{x1}" y1="{y(g)}" y2="{y(g)}" stroke="{GRID}"/>')
        s.append(t(x0 - 5, y(g) + 3, f"{g}%", 7.5, MUTED, "end"))
    # legend
    s.append(f'<rect x="{x0}" y="2" width="9" height="9" rx="2" fill="{PLUM}"/>')
    s.append(t(x0 + 13, 10, "share of spend", 8.3, INK2))
    s.append(f'<rect x="{x0+92}" y="2" width="9" height="9" rx="2" fill="{TEAL}"/>')
    s.append(t(x0 + 105, 10, "share of purchases", 8.3, INK2))
    band = (x1 - x0) / 4
    bw = 26
    for i, (lab, sp, pu, roas) in enumerate(groups):
        cx = x0 + band * i + band / 2
        hi = lab == "55+"
        s.append(f'<path d="{bar_up(cx-bw-1, y(sp), bw, yb-y(sp))}" fill="{PLUM}"/>')
        s.append(f'<path d="{bar_up(cx+1, y(pu), bw, yb-y(pu))}" fill="{TEAL}"/>')
        s.append(t(cx - bw / 2 - 1, y(sp) - 4, f"{sp:.0f}%", 8, INK, "middle", 600))
        s.append(t(cx + bw / 2 + 1, y(pu) - 4, f"{pu:.0f}%", 8, INK, "middle", 600))
        s.append(t(cx, yb + 12, lab, 8.8, INK, "middle", 700))
        s.append(t(cx, yb + 23, f"ROAS {roas:.2f}", 8, "#2f7d4a" if hi else MUTED, "middle", 700 if hi else 400))
    s.append(f'<line x1="{x0}" x2="{x1}" y1="{yb}" y2="{yb}" stroke="{MUTED}"/>')
    return f'<svg viewBox="0 0 360 156" role="img" aria-label="Spend share vs purchase share by age">{"".join(s)}</svg>'


def fill(template, **kw):
    html = (OUT / template).read_text()
    for k, v in kw.items():
        html = html.replace("{{" + k + "}}", v)
    return html


(OUT / "audit.html").write_text(fill("audit.tpl.html", weekly=chart_weekly(), funnel=chart_funnel(),
                                     ads=chart_ads(), age=chart_age()))
if (OUT / "concepts.tpl.html").exists():
    (OUT / "concepts.html").write_text((OUT / "concepts.tpl.html").read_text())
print("built")
