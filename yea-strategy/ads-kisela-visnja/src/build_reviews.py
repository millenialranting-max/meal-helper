"""Review-led versions of the gift concept (quotes from the existing Yea gift ad, titles removed)."""
from build import page, tub, box, BG2, INK, OUT

REV = {
    "day": ("EasyGut Day", "Uz doručak", "2.549", "Ivana Š.", "#8a3fb0",
            "EasyGut Day je deo moje svakodnevne rutine, posebno kad jedem obilnije ili putujem."),
    "night": ("EasyGut Night", "Pre spavanja", "2.799", "Andrea I.", "#3b3f8f",
              "Najviše mi prija EasyGut Night. Nekoliko dana ga već koristim i baš sam lepo spavala."),
    "forte": ("EasyGut Forte", "Uz težak obrok", "3.499", "Marija M.", "#1f6a43",
              "Kada menjam sredinu uvek kao podršku nosim EasyGut Forte, jer nikad ne znam kako će stomak da mi reaguje."),
}

RCSS = """
.rv{position:absolute;background:#fff;border-radius:26px;box-shadow:0 16px 36px rgba(120,40,50,.16);display:grid;align-items:center;color:#2b0710}
.rv .q{font-family:Inter,sans-serif;font-weight:500;color:#3d1f26;line-height:1.36}
.rv .who{display:flex;align-items:center;gap:12px;margin-top:12px;font-family:Inter,sans-serif;font-weight:700;color:#2b0710}
.av{width:44px;height:44px;border-radius:50%;color:#fff;display:grid;place-items:center;font-weight:800;font-family:Montserrat,sans-serif;font-size:18px}
.pc{display:inline-flex;align-items:center;gap:8px;font-family:Inter,sans-serif;font-weight:700;font-size:20px;color:#6d4a52;border:1.5px solid #ead7d9;border-radius:30px;padding:4px 14px 5px;margin-bottom:10px}
.pc i{width:10px;height:10px;border-radius:50%}
.val{text-align:center;background:#fbe7ec;border-radius:18px;padding:12px 8px;color:#8f1325}
.val small{display:block;font-size:18px;font-weight:800;text-transform:uppercase;letter-spacing:.06em}
.val b{display:block;font-size:34px;font-weight:900;line-height:1.1}
.val em{display:block;font-style:normal;font-size:15px;font-weight:700;color:#b04a62}
"""


def initials(name):
    return "".join(p[0] for p in name.replace(".", "").split())


def row(k, x, y, w, h, img_w=180, qsize=24):
    prod, use, val, name, col, q = REV[k]
    return f"""<div class="rv" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;grid-template-columns:{img_w + 20}px 1fr 170px;padding:0 22px 0 16px;gap:16px">
  <img src="img/cut_{k}.png" style="width:{img_w}px;filter:drop-shadow(0 10px 12px rgba(0,0,0,.18))">
  <div><span class="pc"><i style="background:{col}"></i>{prod} · {use}</span>
    <div class="q" style="font-size:{qsize}px">„{q}“</div>
    <div class="who" style="font-size:21px"><span class="av" style="background:{col}">{initials(name)}</span>{name}</div></div>
  <div class="val"><small>Vredan</small><b>{val}</b><em>RSD · na poklon</em></div>
</div>"""


# ---------------------------------------------------------------- R1: three reviews = three gifts (4:5)
r1 = page(1080, 1350, BG2 + f"""
<div class="abs" style="left:70px;top:62px;font-size:26px"><span class="chip red">Uz Kiselu višnju 500g</span></div>
<div class="abs" style="left:70px;top:118px;color:{INK};font-size:84px;font-weight:900;text-transform:uppercase;line-height:1.04">Biraš 1 EasyGut<br><span class="hb red" style="color:#fff;font-size:80px;padding:0 18px 4px">na poklon</span></div>
<div class="abs" style="left:72px;top:328px;color:#5a2a33;font-family:Inter,sans-serif;font-size:27px;font-weight:600">Puno pakovanje, 30 kapsula. Evo šta kažu oni koji ga koriste:</div>
{row('day', 50, 392, 980, 212)}
{row('night', 50, 622, 980, 212)}
{row('forte', 50, 852, 980, 232, qsize=22)}
<div class="abs" style="left:0;right:0;bottom:0;height:226px;background:{INK};z-index:8"></div>
{tub(18, 1050, 330, 9)}
<div class="abs" style="left:300px;top:1148px;z-index:10">
  <div style="font-size:24px;font-weight:800;text-transform:uppercase;letter-spacing:.04em;opacity:.85">Plaćaš samo protein</div>
  <div style="font-size:66px;font-weight:900;line-height:1.05">2.999 RSD</div>
  <div style="font-family:Inter,sans-serif;font-size:22px;font-weight:600;opacity:.8;margin-top:4px">Kisela višnja 500g · do nedelje 8.11.</div></div>
<div class="abs" style="right:50px;top:1150px;z-index:10;font-size:22px"><span class="lime">Besplatna dostava</span></div>
""", RCSS)

# ---------------------------------------------------------------- R2: hero review + "others pay full price" (4:5)
QCSS = RCSS + """
.big{position:absolute;left:60px;top:330px;width:600px;background:#fff;border-radius:30px;padding:34px 38px 30px;box-shadow:0 20px 44px rgba(120,40,50,.18);z-index:5}
.big .q{font-family:Inter,sans-serif;font-size:36px;font-weight:600;line-height:1.34;color:#2b0710}
.big .who{display:flex;align-items:center;gap:12px;font-family:Inter,sans-serif;font-weight:700;color:#2b0710}
.big .mark{position:absolute;left:28px;top:-46px;font-family:Montserrat,sans-serif;font-weight:900;font-size:150px;color:#f45b84;line-height:1}
"""
r2 = page(1080, 1350, BG2 + f"""
<div class="abs" style="left:60px;top:58px;color:{INK};font-size:68px;font-weight:900;text-transform:uppercase;line-height:1.06">Kupci ga plaćaju<br>2.799 RSD.<br><span class="hb red" style="color:#fff;font-size:64px;padding:0 16px 4px">Ti ga dobijaš na poklon.</span></div>
<div class="big"><div class="mark">“</div>
  <span class="pc"><i style="background:#3b3f8f"></i>EasyGut Night · pre spavanja</span>
  <div class="q">Najviše mi prija EasyGut Night. Nekoliko dana ga već koristim i baš sam lepo spavala.</div>
  <div class="who" style="font-size:24px;margin-top:18px"><span class="av" style="background:#3b3f8f">AI</span>Andrea I.</div></div>
{tub(560, 470, 560, 2)}
{box('night', 560, 790, 470, -4, 4)}
<div class="abs" style="left:60px;top:800px;width:470px;color:#5a2a33;font-family:Inter,sans-serif;font-size:28px;line-height:1.4;font-weight:500;z-index:5">
  Uz <b style="color:{INK}">Kiselu višnju 500g (2.999 RSD)</b> biraš jedan pun EasyGut: <b style="color:{INK}">Day, Night ili Forte</b>.</div>
<div class="abs" style="left:0;right:0;bottom:0;height:120px;background:{INK};display:flex;align-items:center;justify-content:space-between;padding:0 60px;z-index:10">
  <span style="font-size:28px;font-weight:800;text-transform:uppercase">Do nedelje 8.11.</span>
  <span class="lime" style="font-size:24px">Besplatna dostava</span></div>
""", QCSS)

# ---------------------------------------------------------------- R3: story version, stacked reviews (9:16)
r3 = page(1080, 1920, BG2.replace("height:330px", "height:420px").replace("bottom:318px", "bottom:408px") + f"""
<div class="abs" style="top:270px;left:0;right:0;text-align:center;font-size:30px"><span class="chip red">Kisela višnja odlazi</span> <span class="chip blk">do nedelje 8.11.</span></div>
<div class="abs" style="top:340px;left:0;right:0;text-align:center;color:{INK};font-size:96px;font-weight:900;text-transform:uppercase;line-height:1.05">EasyGut<br><span class="hb red" style="color:#fff">na poklon</span></div>
<div class="abs" style="top:575px;left:0;right:0;text-align:center;color:#5a2a33;font-family:Inter,sans-serif;font-size:30px;font-weight:600">Biraš jedan. Evo šta kažu oni koji ga koriste:</div>
{row('day', 40, 640, 1000, 228)}
{row('night', 40, 886, 1000, 228)}
{row('forte', 40, 1132, 1000, 250, qsize=23)}
{tub(40, 1395, 330, 3)}
<div class="abs" style="left:330px;top:1430px;color:{INK}">
  <div style="font-size:28px;font-weight:800;text-transform:uppercase;letter-spacing:.04em">Plaćaš samo protein</div>
  <div style="font-size:92px;font-weight:900;line-height:1.05">2.999 RSD</div>
  <div style="margin-top:14px;font-size:24px"><span class="lime">Besplatna dostava</span></div></div>
""", RCSS)

for name, html in [("c2d_recenzije_3", r1), ("c2e_recenzija_night", r2), ("c2f_recenzije_story", r3)]:
    (OUT / f"{name}.html").write_text(html)
print("built reviews")
