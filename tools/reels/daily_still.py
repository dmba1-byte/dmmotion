"""One static post a day for @dm_motion1.

There is no image-publishing API available on this account — vidIQ publishes
reels only, and no Instagram connector in the registry posts images. So these
are built here and handed to David to upload. The point of the generator is
that building them costs him nothing and he only has to tap "post".

1080x1350, the tallest feed crop, same palette and type as the reels so the
grid reads as one body of work.
"""
import datetime as dt, pathlib, subprocess, sys, zlib

sys.path.insert(0, '/home/claude/reels')
from playwright.sync_api import sync_playwright
from gen import rules as RL

W, H = 1080, 1350
INK, BLUE, GRN, RED, PAPER, SUB = '#141414', '#1d4e89', '#2e9b62', '#c0392b', '#ffffff', '#8a8a8a'
OUT = pathlib.Path('/home/claude/reels/stills'); OUT.mkdir(exist_ok=True)

HEAD = f"""<meta charset="utf-8"><style>
@page{{margin:0}} html,body{{margin:0;width:{W}px;height:{H}px;background:{PAPER};
 font-family:Helvetica,Arial,sans-serif;color:{INK};overflow:hidden}}
.grid{{position:absolute;inset:0;background-image:linear-gradient(#0000000a 1px,transparent 1px),
 linear-gradient(90deg,#0000000a 1px,transparent 1px);background-size:45px 45px}}
.wrap{{position:absolute;inset:0;padding:60px 58px;box-sizing:border-box;display:flex;flex-direction:column}}
.kicker{{font:700 23px Helvetica;letter-spacing:4px;color:{BLUE}}}
h1{{font-size:70px;line-height:1.03;letter-spacing:-2.4px;margin:12px 0 0;font-weight:800}}
h1 em{{font-style:normal;color:{RED}}}
.sub{{font-size:27px;line-height:1.36;color:#444;margin-top:16px}}
.foot{{margin-top:auto;display:flex;align-items:center;gap:14px;border-top:3px solid {INK};padding-top:20px}}
.foot .h{{font:700 26px Helvetica;letter-spacing:.5px}}
.foot .r{{margin-left:auto;font:700 23px Helvetica;color:{BLUE}}}
</style>"""


def foot(right='dmba04@gmail.com'):
    return (f'<div class="foot"><div class="h">@dm_motion1</div>'
            f'<div class="r">{right}</div></div>')


def frame(topic, t, out_png, box=(1, 1), pad=0.06):
    """Grab one frame out of the real reel for this topic and crop to the drawing."""
    from PIL import Image, ImageChops
    src = RL.render(topic, '/home/claude/reels/stillsrc', stills=[t])[0]
    im = Image.open(src).convert('RGB')
    y0, y1 = 470, min(1620, im.height)
    strip = im.crop((0, y0, im.width, y1))
    bg = strip.getpixel((4, 4))
    mask = ImageChops.difference(strip, Image.new('RGB', strip.size, bg)).convert('L')
    bb = mask.point(lambda v: 255 if v > 18 else 0).getbbox() or (0, 0, strip.width, strip.height)
    l, tp, r, bt = bb
    cx, cy = (l + r) / 2, (tp + bt) / 2 + y0
    aw, ah = box
    w = max(r - l, (bt - tp) * aw / ah) * (1 + 2 * pad)
    h = w * ah / aw
    x0, yy0 = cx - w / 2, cy - h / 2
    canvas = Image.new('RGB', (int(w), int(h)), bg)
    sx0, sy0 = max(0, int(x0)), max(0, int(yy0))
    sx1, sy1 = min(im.width, int(x0 + w)), min(im.height, int(yy0 + h))
    canvas.paste(im.crop((sx0, sy0, sx1, sy1)), (sx0 - int(x0), sy0 - int(yy0)))
    canvas.resize((1000, int(1000 * ah / aw)), Image.LANCZOS).save(out_png)
    return out_png


def clearance_card(topic):
    """The strongest frame from a reel, with the standard spelled out under it."""
    s = RL.TOPICS[topic]
    delta = s['right'] - s['wrong']
    # the stakes beat, where the required zone is drawn over what it collides with
    img = frame(topic, 11.2, OUT / f'f_{topic}.png', box=(10, 8))
    rule = s['rule'].replace('<br>', ' &middot; ')
    return f"""<!doctype html><html><head>{HEAD}</head><body><div class="grid"></div>
<div class="wrap">
 <div class="kicker">{s['topic']}</div>
 <h1>{delta}&Prime; <em>short</em>.</h1>
 <div class="sub">{s['vo_stakes']}</div>
 <div style="margin:26px -58px 0;border-top:2.5px solid {INK};border-bottom:2.5px solid {INK}">
  <img src="{img.as_uri()}" style="width:100%;display:block"></div>
 <div style="margin-top:24px;font:800 31px Helvetica;line-height:1.34">{rule}</div>
 <div style="font:600 20px Helvetica;color:{SUB};letter-spacing:1.4px;margin-top:9px">{s['source']}</div>
 {foot()}
</div></body></html>"""


def checklist_card():
    rows = ''.join(
        f'<div style="display:flex;gap:18px;align-items:baseline;padding:21px 0;'
        f'border-top:2px solid #e2e0da">'
        f'<div style="font:800 27px Helvetica;color:{GRN};min-width:52px">{i+1:02d}</div>'
        f'<div><div style="font:700 29px Helvetica">{s["topic"].title()}</div>'
        f'<div style="font-size:22px;color:#555;margin-top:3px">{s["right"]}&Prime; minimum</div></div></div>'
        for i, s in enumerate(RL.TOPICS.values()))
    return f"""<!doctype html><html><head>{HEAD}</head><body><div class="grid"></div>
<div class="wrap">
 <div class="kicker">BEFORE I ANIMATE ANYTHING</div>
 <h1>Seven things<br>I check on<br>every <em>plan</em>.</h1>
 <div style="margin-top:22px">{rows}</div>
 {foot('from $450')}
</div></body></html>"""


def process_card():
    steps = [('01', 'Send the drawing', 'PDF, DWG, AI or SVG — whatever you already have.'),
             ('02', 'I animate it', 'Your linework, your titles, built in order.'),
             ('03', 'You get the file', 'MP4 for listings, socials or a client meeting.')]
    rows = ''.join(
        f'<div style="display:flex;gap:20px;align-items:baseline;padding:34px 0;'
        f'border-top:2px solid #e2e0da">'
        f'<div style="font:800 36px Helvetica;color:{GRN};min-width:60px">{n}</div>'
        f'<div><div style="font:700 30px Helvetica">{t}</div>'
        f'<div style="font-size:23px;color:#555;margin-top:4px">{d}</div></div></div>'
        for n, t, d in steps)
    return f"""<!doctype html><html><head>{HEAD}</head><body><div class="grid"></div>
<div class="wrap">
 <div class="kicker">HOW IT WORKS</div>
 <h1>Your flat plan,<br>in <em>motion</em>.</h1>
 <div style="margin-top:20px">{rows}</div>
 <div style="margin-top:auto;margin-bottom:20px;background:{INK};color:#fff;padding:24px 28px;border-radius:14px">
  <div style="font:700 22px Helvetica;letter-spacing:2px;color:#9fd9b8">EMAIL YOUR DRAWING</div>
  <div style="font:800 38px Helvetica;margin-top:7px;letter-spacing:-1px">dmba04@gmail.com</div>
 </div>
 {foot('from $450')}
</div></body></html>"""


def shoot(html, name):
    p = OUT / f'{name}.html'; p.write_text(html)
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        pg = b.new_page(viewport={'width': W, 'height': H})
        errs = []; pg.on('pageerror', lambda e: errs.append(str(e)))
        pg.goto(p.resolve().as_uri()); pg.wait_for_timeout(400)
        pg.screenshot(path=str(OUT / f'{name}.png')); b.close()
        if errs: print('ERR', name, errs[:2])
    return OUT / f'{name}.png'


def build(day=None):
    """Today's post. Clearance cards five days in seven; the other two rotate
    the checklist and the process card so the grid isn't all one thing."""
    d = day or dt.date.today()
    topics = list(RL.TOPICS)
    slot = d.toordinal() % 7
    if slot == 3:
        return shoot(checklist_card(), f'still_{d:%m%d}_checklist'), 'Seven things I check on every plan'
    if slot == 6:
        return shoot(process_card(), f'still_{d:%m%d}_process'), 'How it works — from $450'
    topic = topics[(d.toordinal() // 1) % len(topics)]
    s = RL.TOPICS[topic]
    cap = f"{s['right'] - s['wrong']}″ short — {s['vo_stakes']}"
    return shoot(clearance_card(topic), f'still_{d:%m%d}_{topic}'), cap


if __name__ == '__main__':
    p, cap = build()
    print(p); print(cap)
