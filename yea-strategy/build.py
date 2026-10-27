"""Builds the budget-calendar SVG into yea_next.html -> yea_next.out.html"""
from pathlib import Path
OUT = Path(__file__).parent
PLUM, GRAY, INK, INK2, MUTED, GRID = "#5b3fa0", "#d6d0de", "#1f1a2e", "#4d475c", "#847e92", "#ece7df"
# (days, €/day, label, peak?)  starting 27 Oct 2026
phases = [(27, 25, "Restock + test", False), (44, 80, "Black Friday + Božićni post", True),
          (53, 30, "Baseline", False), (14, 50, "Pre-Lent", False),
          (21, 100, "Lent wk 1–3", True), (27, 60, "Rest of Lent", True), (30, 30, "After Easter", False)]
W, x0, x1, yb, yt, vmax = 700, 8, 692, 114, 36, 100
total = sum(p[0] for p in phases)
sx = (x1 - x0) / total
y = lambda v: yb - v / vmax * (yb - yt)
s = []
x = x0
for days, eur, lab, peak in phases:
    w = days * sx
    h = yb - y(eur)
    r = 4
    s.append(f'<path d="M{x+1},{yb} L{x+1},{y(eur)+r} Q{x+1},{y(eur)} {x+1+r},{y(eur)} L{x+w-1-r},{y(eur)} Q{x+w-1},{y(eur)} {x+w-1},{y(eur)+r} L{x+w-1},{yb} Z" fill="{PLUM if peak else GRAY}"/>')
    cx = x + w / 2
    s.append(f'<text x="{cx}" y="{y(eur)-4}" font-size="9" font-weight="700" fill="{INK}" text-anchor="middle">€{eur}</text>')
    if w > 60:
        s.append(f'<text x="{cx}" y="{y(eur)+13}" font-size="7.6" font-weight="600" fill="{"#fff" if peak else INK2}" text-anchor="middle">{lab}</text>')
    else:
        s.append(f'<text x="{cx}" y="{y(eur)-14}" font-size="7.2" fill="{INK2}" text-anchor="middle">{lab}</text>')
    x += w
s.append(f'<line x1="{x0}" x2="{x1}" y1="{yb}" y2="{yb}" stroke="{MUTED}"/>')
# month ticks (days from 27 Oct)
for d, m in [(5, "Nov"), (35, "Dec"), (66, "Jan"), (97, "Feb"), (125, "Mar"), (156, "Apr"), (186, "May")]:
    xx = x0 + d * sx
    s.append(f'<line x1="{xx}" x2="{xx}" y1="{yb}" y2="{yb+4}" stroke="{MUTED}"/>')
    s.append(f'<text x="{xx+2}" y="{yb+13}" font-size="7.4" fill="{MUTED}">{m}</text>')
# event markers
for d, lab in [(31, "BF 27 Nov"), (32, "Fast starts 28 Nov"), (139, "Lent starts 15 Mar"), (187, "Easter 2 May")]:
    pass
ev = [(31, "Black Friday 27 Nov · fast starts 28 Nov"), (139, "Lent starts 15 Mar"), (187, "Easter 2 May")]
for d, lab in ev:
    xx = x0 + d * sx
    s.append(f'<line x1="{xx}" x2="{xx}" y1="4" y2="{yb}" stroke="#a3263b" stroke-width="1" stroke-dasharray="2 2"/>')
    s.append(f'<text x="{xx+3}" y="11" font-size="7.2" font-weight="700" fill="#a3263b">{lab}</text>')
svg = f'<svg viewBox="0 0 {W} 132" role="img" aria-label="Suggested Meta budget per day by season">{"".join(s)}</svg>'
html = (OUT / "yea_next.html").read_text().replace("{{calendar}}", svg)
(OUT / "yea_next.out.html").write_text(html)
print("built")
