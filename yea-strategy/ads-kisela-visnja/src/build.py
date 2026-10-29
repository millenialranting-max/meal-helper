"""Builds 6 ad mockups (3 combo-value 9:16, 3 gift 4:5) as HTML for screenshotting."""
from pathlib import Path

OUT = Path(__file__).parent

BASE = """
@import url(fonts/fonts.css);
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:__W__px;height:__H__px;overflow:hidden}
.c{position:relative;width:__W__px;height:__H__px;overflow:hidden;font-family:Montserrat,sans-serif;color:#fff}
.abs{position:absolute}
.hb{font-weight:900;text-transform:uppercase;line-height:1.3;padding:2px 20px 4px;border-radius:12px;
    -webkit-box-decoration-break:clone;box-decoration-break:clone}
.chip{display:inline-block;font-weight:800;text-transform:uppercase;letter-spacing:.02em;padding:8px 18px 9px;border-radius:10px;line-height:1}
.red{background:#8f1325;color:#fff} .blk{background:#140409;color:#fff} .pink{background:#f45b84;color:#fff} .wht{background:#fff;color:#2b0710}
.lime{display:inline-block;background:#7df03c;color:#0b0b0b;font-weight:900;text-transform:uppercase;border-radius:40px;padding:12px 34px 13px;letter-spacing:.02em;line-height:1}
.prod{filter:drop-shadow(0 28px 34px rgba(0,0,0,.5))}
.strike{position:relative;display:inline-block}
.strike::after{content:"";position:absolute;left:-4%;right:-4%;top:52%;height:7px;background:#f45b84;transform:rotate(-6deg);border-radius:4px}
"""

# --- concept 1 background: deep cherry with real cherries framing top and bottom
BG1 = """
<div class="abs" style="inset:0;background:radial-gradient(110% 65% at 50% 46%,#76122a 0%,#430818 55%,#1f030a 100%)"></div>
<div class="abs" style="left:0;top:0;width:1080px;height:275px;background:url(img/cherry_top.png) center top/1400px auto no-repeat;-webkit-mask-image:linear-gradient(#000 50%,transparent)"></div>
<div class="abs" style="left:0;bottom:0;width:1080px;height:264px;background:url(img/cherry_bot.png) center bottom/1400px auto no-repeat;-webkit-mask-image:linear-gradient(transparent,#000 45%)"></div>
"""

# --- concept 2 background: soft blush studio, window light, surface
BG2 = """
<div class="abs" style="inset:0;background:radial-gradient(90% 70% at 62% 35%,#fbefed 0%,#f1dcda 55%,#e6c6c4 100%)"></div>
<div class="abs" style="inset:-100px;background:repeating-linear-gradient(115deg,rgba(255,255,255,0) 0 140px,rgba(255,255,255,.35) 140px 210px,rgba(255,255,255,0) 210px 330px);filter:blur(26px);opacity:.8"></div>
<div class="abs" style="left:0;right:0;bottom:0;height:330px;background:linear-gradient(#e2bcba,#d6aaa8)"></div>
<div class="abs" style="left:0;right:0;bottom:318px;height:26px;background:linear-gradient(rgba(150,80,80,0),rgba(150,80,80,.18));filter:blur(6px)"></div>
"""

INK = "#3a0a16"


def page(w, h, body, extra_css=""):
    return f"""<!doctype html><html lang="sr"><head><meta charset="utf-8"><style>{BASE.replace('__W__', str(w)).replace('__H__', str(h))}{extra_css}</style></head>
<body><div class="c">{body}</div></body></html>"""


def tub(x, y, h, z=2):
    return f'<img class="abs prod" src="img/tub.png" style="left:{x}px;top:{y}px;height:{h}px;z-index:{z}">'


def box(name, x, y, w, rot=0, z=3, shadow=True):
    cls = "abs prod" if shadow else "abs"
    return f'<img class="{cls}" src="img/cut_{name}.png" style="left:{x}px;top:{y}px;width:{w}px;transform:rotate({rot}deg);z-index:{z}">'


# ---------------------------------------------------------------- 1A equation
a1 = page(1080, 1920, BG1 + f"""
<div class="abs" style="top:278px;left:0;right:0;text-align:center;font-size:34px">
  <span class="chip wht" style="color:#8f1325">Kisela višnja odlazi</span> <span class="chip blk">do nedelje 8.11.</span></div>
<div class="abs" style="top:372px;left:0;right:0;text-align:center;font-size:118px;line-height:1.12;font-weight:900;text-transform:uppercase;letter-spacing:-.01em">
  2 proizvoda<br><span class="hb pink" style="font-size:104px">za cenu 1</span></div>

{tub(20, 640, 640)}
<div class="abs" style="left:468px;top:870px;width:120px;height:120px;border-radius:50%;background:#fff;color:#8f1325;font-size:96px;font-weight:900;display:grid;place-items:center;line-height:1;z-index:5;box-shadow:0 10px 30px rgba(0,0,0,.35)">+</div>
{box('forte', 600, 800, 430, 5, 4)}
<div class="abs" style="left:610px;top:1205px;width:420px;text-align:center;font-size:24px;z-index:6"><span class="chip wht" style="color:#3a0a16">Day</span> <span class="chip wht" style="color:#3a0a16">Night</span> <span class="chip wht" style="color:#3a0a16">Forte</span></div>

<div class="abs" style="left:60px;top:1295px;width:430px;text-align:center">
  <div style="font-size:34px;font-weight:700;opacity:.9">Kisela višnja 500g</div>
  <div style="font-size:64px;font-weight:900">2.999 RSD</div></div>
<div class="abs" style="left:560px;top:1295px;width:470px;text-align:center">
  <div style="font-size:34px;font-weight:700;opacity:.9">EasyGut, biraš 1</div>
  <div style="font-size:64px;font-weight:900"><span class="strike" style="font-size:40px;opacity:.75;font-weight:800;vertical-align:middle">do 3.499</span>&nbsp; 0 RSD</div></div>

<div class="abs" style="left:90px;right:90px;top:1440px;height:118px;border-radius:22px;background:#fff;color:#8f1325;display:flex;align-items:center;justify-content:center;gap:22px;box-shadow:0 18px 40px rgba(0,0,0,.35)">
  <span style="font-size:44px;font-weight:800;text-transform:uppercase">Ukupno</span><span style="font-size:80px;font-weight:900">2.999 RSD</span></div>
<div class="abs" style="top:1584px;left:0;right:0;text-align:center;font-size:30px"><span class="lime">Besplatna dostava</span></div>
""")

# ---------------------------------------------------------------- 1B receipt
RCSS = """
.rc{position:absolute;left:150px;top:585px;width:780px;background:#fffdf8;color:#1d1014;font-family:'JetBrains Mono',monospace;
    padding:46px 54px 70px;transform:rotate(-2.2deg);box-shadow:0 30px 60px rgba(0,0,0,.45);
    -webkit-mask:linear-gradient(#000,#000) top/100% calc(100% - 22px) no-repeat,
                 conic-gradient(from -45deg at bottom,#0000,#000 1deg 89deg,#0000 90deg) bottom/44px 22px repeat-x}
.rc .t{text-align:center;font-weight:800;font-size:34px;letter-spacing:.12em}
.rc .s{text-align:center;font-size:22px;color:#7a6b6f;margin-top:4px}
.rc .hr{border-top:3px dashed #c9bcbf;margin:22px 0}
.rc .row{display:flex;justify-content:space-between;font-size:31px;line-height:1.75;font-weight:500}
.rc .row b{font-weight:800}
.rc .gift{color:#c2183f;font-weight:800}
.rc .tot{display:flex;justify-content:space-between;align-items:baseline;font-weight:800;font-size:40px;margin-top:6px}
.rc .tot span:last-child{font-size:58px}
.rc .n{font-family:Inter,sans-serif;font-size:22px;color:#6c5c60;margin-top:16px;line-height:1.35}
.stamp{position:absolute;left:350px;top:1240px;width:250px;height:250px;border-radius:50%;border:8px solid #c2183f;color:#c2183f;
       display:grid;place-items:center;text-align:center;transform:rotate(-14deg);font-weight:900;text-transform:uppercase;line-height:1.05;
       font-size:30px;background:rgba(255,253,248,.92);z-index:6;box-shadow:0 10px 25px rgba(0,0,0,.25)}
.stamp b{display:block;font-size:50px}
"""
a2 = page(1080, 1920, BG1 + f"""
<div class="abs" style="top:278px;left:0;right:0;text-align:center;font-size:34px"><span class="chip wht" style="color:#8f1325">Kisela višnja odlazi</span></div>
<div class="abs" style="top:360px;left:0;right:0;text-align:center;font-size:92px;font-weight:900;text-transform:uppercase;line-height:1.08">Pogledaj<br>ovaj račun</div>
<div class="rc">
  <div class="t">YEA PROTEIN</div><div class="s">akcija do nedelje 8.11.</div>
  <div class="hr"></div>
  <div class="row"><span>Kisela višnja 500g</span><b>2.999</b></div>
  <div class="row"><span>EasyGut Forte</span><b>3.499</b></div>
  <div class="row gift"><span>Poklon: EasyGut</span><span>−3.499</span></div>
  <div class="row"><span>Dostava</span><b>0</b></div>
  <div class="hr" style="border-top-style:solid;border-color:#1d1014"></div>
  <div class="tot"><span>UKUPNO</span><span>2.999 RSD</span></div>
  <div class="n">Umesto Forte možeš izabrati Day (2.549) ili Night (2.799). Poklon je puno pakovanje.</div>
</div>
<div class="stamp"><div>Ušteda<b>3.499</b>RSD</div></div>
{tub(20, 1150, 470, 5)}
{box('forte', 560, 1290, 420, 6, 5)}
""", RCSS)

# ---------------------------------------------------------------- 1C strike-through value
a3 = page(1080, 1920, BG1 + f"""
<div class="abs" style="top:278px;left:0;right:0;text-align:center;font-size:34px">
  <span class="chip wht" style="color:#8f1325">Kisela višnja odlazi</span> <span class="chip blk">do nedelje 8.11.</span></div>
<div class="abs" style="left:0;right:0;top:350px;height:640px">
  <div class="abs" style="left:300px;top:40px;width:480px;height:520px;border-radius:50%;background:radial-gradient(#f45b84 0%,rgba(244,91,132,0) 68%);opacity:.45"></div>
</div>
{tub(140, 380, 640)}
{box('forte', 520, 690, 430, 6, 4)}
<div class="abs" style="left:0;right:0;top:1060px;text-align:center">
  <div style="font-size:36px;font-weight:800;text-transform:uppercase;letter-spacing:.06em;opacity:.85">Vrednost paketa</div>
  <div style="font-size:84px;font-weight:900;margin-top:2px"><span class="strike">6.498 RSD</span></div>
  <div style="font-size:36px;font-weight:800;text-transform:uppercase;letter-spacing:.06em;margin-top:26px;opacity:.85">Ti plaćaš</div>
  <div style="margin-top:8px"><span class="hb pink" style="font-size:150px;padding:0 34px 8px;border-radius:22px">2.999 RSD</span></div>
  <div style="font-size:34px;font-weight:600;margin-top:26px;line-height:1.35">Kisela višnja 500g + EasyGut Forte<br><span style="opacity:.75;font-size:28px">ili umesto Forte biraš Day ili Night</span></div>
</div>
<div class="abs" style="top:1600px;left:0;right:0;text-align:center;font-size:30px"><span class="lime">Besplatna dostava</span></div>
""")

# ---------------------------------------------------------------- 2A gift tag
GCSS = """
.seal{position:absolute;width:230px;height:230px;border-radius:50%;background:radial-gradient(circle at 35% 30%,#c42a4a,#8f1325 70%);
      color:#fff;display:grid;place-items:center;text-align:center;font-weight:900;text-transform:uppercase;line-height:1.05;z-index:9;
      box-shadow:0 14px 30px rgba(90,10,25,.35),inset 0 0 0 8px rgba(255,255,255,.18);transform:rotate(10deg)}
.seal small{display:block;font-size:20px;font-weight:700;letter-spacing:.06em}
.seal b{display:block;font-size:46px;margin:2px 0}
.rib{position:absolute;background:linear-gradient(90deg,#7d0f22,#b8203f 50%,#7d0f22);z-index:6;box-shadow:0 2px 6px rgba(0,0,0,.25)}
"""
b1 = page(1080, 1350, BG2 + f"""
<div class="abs" style="left:70px;top:70px;font-size:28px"><span class="chip red">Uz Kiselu višnju 500g</span></div>
<div class="abs" style="left:70px;top:132px;color:{INK};font-size:96px;font-weight:900;text-transform:uppercase;line-height:1.02;letter-spacing:-.01em">EasyGut<br>je naš<br>poklon.</div>
<div class="abs" style="left:72px;top:460px;width:430px;color:#5a2a33;font-family:Inter,sans-serif;font-size:31px;line-height:1.38;font-weight:500">
  <b style="color:{INK}">Puno pakovanje, ne uzorak.</b><br>Biraš Day, Night ili Forte.</div>

{tub(30, 640, 600, 2)}
<div class="abs" style="left:440px;top:560px;width:600px;height:520px;z-index:3;transform:rotate(-5deg)">
  <img class="abs prod" src="img/cut_night.png" style="left:0;top:0;width:600px">
  <div class="abs" style="left:0;top:0;width:600px;height:511px;z-index:6;clip-path:polygon(30px 34px,520px 28px,520px 470px,30px 478px)">
    <div class="rib" style="left:-30px;top:84px;width:360px;height:58px;transform:rotate(-45deg);display:grid;place-items:center;color:#fff;font-weight:900;font-size:26px;letter-spacing:.12em">POKLON</div></div>
</div>
<div class="seal" style="left:800px;top:400px"><div><small>Vredan do</small><b>3.499</b><small>RSD</small></div></div>

<div class="abs" style="left:0;right:0;bottom:0;height:120px;background:{INK};display:flex;align-items:center;justify-content:space-between;padding:0 60px;z-index:10">
  <span style="font-size:30px;font-weight:800;text-transform:uppercase">Do nedelje 8.11.</span>
  <span class="lime" style="font-size:26px">Besplatna dostava</span></div>
""", GCSS)

# ---------------------------------------------------------------- 2B farewell / reason why
b2 = page(1080, 1350, BG2 + f"""
<div class="abs" style="left:0;right:0;top:64px;text-align:center;color:{INK};font-size:88px;font-weight:900;text-transform:uppercase;line-height:1.02">Kisela višnja<br><span class="hb red" style="font-size:84px;color:#fff">se oprašta</span></div>
<div class="abs" style="left:110px;right:110px;top:300px;text-align:center;color:#5a2a33;font-family:Inter,sans-serif;font-size:31px;line-height:1.4;font-weight:500">
  Hvala što ste je voleli. Za kraj, <b style="color:{INK}">uz svaku kutiju ide pun EasyGut na poklon</b>, po tvom izboru.</div>
{tub(300, 410, 560, 2)}
{box('day', 40, 800, 330, -4, 4)}
{box('forte', 380, 850, 330, 0, 5)}
{box('night', 715, 800, 330, 4, 4)}
<div class="abs" style="left:40px;right:40px;top:1145px;display:flex;justify-content:space-between;z-index:6;font-size:24px">
  <span class="chip blk" style="width:300px;text-align:center">Uz doručak</span><span class="chip blk" style="width:300px;text-align:center">Uz težak obrok</span><span class="chip blk" style="width:300px;text-align:center">Pre spavanja</span></div>
<div class="abs" style="left:0;right:0;bottom:0;height:110px;background:{INK};display:flex;align-items:center;justify-content:space-between;padding:0 60px;z-index:10">
  <span style="font-size:27px;font-weight:800;text-transform:uppercase">Do 8.11. ili dok traju zalihe</span>
  <span class="lime" style="font-size:24px">Besplatna dostava</span></div>
""")

# ---------------------------------------------------------------- 2C pick your gift
CCSS = """
.card{position:absolute;top:400px;width:310px;height:470px;background:#fff;border-radius:26px;box-shadow:0 18px 40px rgba(120,40,50,.18);
      text-align:center;color:#3a0a16;padding-top:22px}
.card img{width:250px;filter:drop-shadow(0 12px 14px rgba(0,0,0,.18))}
.card h4{font-size:44px;font-weight:900;margin-top:4px;letter-spacing:.02em}
.card p{font-family:Inter,sans-serif;font-size:25px;font-weight:600;color:#7a4a53;margin-top:2px}
.card .v{margin-top:16px;font-size:23px;font-weight:700;color:#7a4a53}
.card .v b{display:block;font-size:34px;color:#3a0a16}
.card .tag{position:absolute;left:50%;top:-20px;transform:translateX(-50%);font-size:20px}
"""
b3 = page(1080, 1350, BG2 + f"""
<div class="abs" style="left:0;right:0;top:66px;text-align:center;color:{INK};font-size:92px;font-weight:900;text-transform:uppercase;line-height:1.02">Izaberi<br><span class="hb red" style="color:#fff">svoj poklon</span></div>
<div class="abs" style="left:0;right:0;top:300px;text-align:center;color:#5a2a33;font-family:Inter,sans-serif;font-size:32px;font-weight:600">uz Yea Kiselu višnju 500g</div>
<div class="card" style="left:40px"><span class="chip red tag">Poklon</span><img src="img/cut_day.png"><h4>DAY</h4><p>Uz doručak</p><div class="v">vrednost<b>2.549 RSD</b></div></div>
<div class="card" style="left:385px"><span class="chip red tag">Poklon</span><img src="img/cut_forte.png"><h4>FORTE</h4><p>Uz težak obrok</p><div class="v">vrednost<b>3.499 RSD</b></div></div>
<div class="card" style="left:730px"><span class="chip red tag">Poklon</span><img src="img/cut_night.png"><h4>NIGHT</h4><p>Pre spavanja</p><div class="v">vrednost<b>2.799 RSD</b></div></div>
{tub(20, 905, 380, 3)}
<div class="abs" style="left:330px;top:935px;color:{INK}">
  <div style="font-size:30px;font-weight:800;text-transform:uppercase;letter-spacing:.03em">Plaćaš samo protein</div>
  <div style="font-size:104px;font-weight:900;line-height:1.05">2.999 RSD</div>
  <div style="font-family:Inter,sans-serif;font-size:26px;font-weight:600;color:#7a4a53;margin-top:6px">Kisela višnja 500g · do nedelje 8.11.</div>
  <div style="margin-top:20px;font-size:26px"><span class="lime">Besplatna dostava</span></div></div>
""", CCSS)

for name, html in [("c1a_jednacina", a1), ("c1b_racun", a2), ("c1c_precrtano", a3),
                   ("c2a_poklon_pecat", b1), ("c2b_oprastanje", b2), ("c2c_izaberi", b3)]:
    (OUT / f"{name}.html").write_text(html)
print("built")
