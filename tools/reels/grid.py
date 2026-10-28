"""Three pinned profile posts for @dm_motion1 — the storefront at the top of the grid.

1080x1350 (Instagram's tallest feed crop). Same palette and type as the reels so the
grid reads as one body of work: ink, blueprint blue, green, paper. No orange.
"""
import pathlib, random, subprocess, sys

sys.path.insert(0, '/home/claude/reels')
from playwright.sync_api import sync_playwright
from gen import elevs
from gen.engine2 import STYLES, LOGO_D

W, H = 1080, 1350
INK, BLUE, GRN, PAPER, TINT, SUB = '#141414', '#1d4e89', '#2e9b62', '#ffffff', '#f1efe9', '#8a8a8a'
OUT = pathlib.Path('/home/claude/reels/grid'); OUT.mkdir(exist_ok=True)
Q = pathlib.Path('/home/claude/dmmotion/social/q')

HEAD = f"""<meta charset="utf-8"><style>
@page{{margin:0}} html,body{{margin:0;width:{W}px;height:{H}px;background:{PAPER};
 font-family:Helvetica,Arial,sans-serif;color:{INK};overflow:hidden}}
.grid{{position:absolute;inset:0;background-image:linear-gradient(#0000000a 1px,transparent 1px),
 linear-gradient(90deg,#0000000a 1px,transparent 1px);background-size:45px 45px}}
.wrap{{position:absolute;inset:0;padding:64px 64px;box-sizing:border-box;display:flex;
 flex-direction:column}}
.kicker{{font:700 24px Helvetica;letter-spacing:4px;color:{BLUE}}}
h1{{font-size:76px;line-height:1.02;letter-spacing:-2.5px;margin:14px 0 0;font-weight:800}}
h1 em{{font-style:normal;color:{BLUE}}}
.sub{{font-size:29px;line-height:1.35;color:#444;margin-top:20px;max-width:800px}}
.foot{{margin-top:auto;display:flex;align-items:center;gap:16px;
 border-top:3px solid {INK};padding-top:22px}}
.foot .h{{font:700 28px Helvetica;letter-spacing:.5px}}
.foot .r{{margin-left:auto;font:700 25px Helvetica;color:{BLUE}}}
</style>"""

LOGO = (f'<svg width="54" height="54" viewBox="30 35 240 235">'
        f'<path d="{LOGO_D}" fill="{INK}"/></svg>')


def foot(right='dmba04@gmail.com'):
    return (f'<div class="foot">{LOGO}<div class="h">@dm_motion1</div>'
            f'<div class="r">{right}</div></div>')


def elevation_svg(kind='craftsman', seed=11, style='light'):
    (svg, _groups), _label = getattr(elevs, kind)(STYLES[style], random.Random(seed))
    # every stage visible at once — these are stills, nothing animates
    svg = svg.replace('opacity="0"', 'opacity="1"')
    return f'<svg viewBox="0 0 1080 1920" width="100%" height="100%">{svg}</svg>'


def post1():
    return f"""<!doctype html><html><head>{HEAD}</head><body><div class="grid"></div>
<div class="wrap">
 <div class="kicker">DM MOTION</div>
 <h1>I animate<br>your <em>drawings</em>.</h1>
 <div class="sub">Floor plans, elevations and 3D — built from your own vector
  linework, not from a template and not from a stock library.</div>
 <div style="flex:1;margin:10px -64px 0;overflow:hidden;position:relative">
   <div style="position:absolute;left:0;right:0;top:-560px;height:1680px">{elevation_svg()}</div>
 </div>
 {foot()}
</div></body></html>"""


def post2(frames):
    cells = ''.join(
        f'<div style="flex:1;border:2.5px solid {INK};background:{PAPER};overflow:hidden;'
        f'position:relative"><img src="{f}" style="width:100%;height:100%;object-fit:cover"></div>'
        for f in frames)
    return f"""<!doctype html><html><head>{HEAD}</head><body><div class="grid"></div>
<div class="wrap">
 <div class="kicker">BEFORE &rarr; AFTER</div>
 <h1>Your flat plan,<br><em>drawn on screen</em>.</h1>
 <div class="sub">Same drawing. The lines build in order, the way it would be
  drafted — walls, then doors, then fixtures, then labels.</div>
 <div style="display:flex;gap:14px;flex:1;margin-top:26px">{cells}</div>
 {foot()}
</div></body></html>"""


def post3(shots=()):
    steps = [('01', 'Send the drawing', 'PDF, DWG, AI or SVG — whatever you already have.'),
             ('02', 'I animate it', 'Your linework, built in order, with your titles kept.'),
             ('03', 'You get the file', 'MP4 ready for listings, socials or a client meeting.')]
    rows = ''.join(
        f'<div style="display:flex;gap:22px;align-items:baseline;padding:40px 0;'
        f'border-top:2px solid #dcdad4">'
        f'<div style="font:800 40px Helvetica;color:{GRN};min-width:66px">{n}</div>'
        f'<div><div style="font:700 33px Helvetica">{t}</div>'
        f'<div style="font-size:24px;color:#555;margin-top:5px">{d}</div></div></div>'
        for n, t, d in steps)
    strip = ''.join(
        f'<div style="flex:1;border:2.5px solid {INK};overflow:hidden;background:{PAPER}">'
        f'<img src="{sh}" style="width:100%;height:100%;object-fit:cover"></div>' for sh in shots)
    return f"""<!doctype html><html><head>{HEAD}</head><body><div class="grid"></div>
<div class="wrap">
 <div class="kicker">HOW IT WORKS</div>
 <h1>From <em>$450</em><br>a clip.</h1>
 <div style="margin-top:30px">{rows}</div>
 <div style="display:flex;gap:12px;flex:1;margin-top:26px;min-height:0">{strip}</div>
 <div style="margin-top:14px;background:{INK};color:#fff;padding:26px 30px;border-radius:14px">
  <div style="font:700 25px Helvetica;letter-spacing:2px;color:#9fd9b8">EMAIL YOUR PLAN</div>
  <div style="font:800 42px Helvetica;margin-top:8px;letter-spacing:-1px">dmba04@gmail.com</div>
  <div style="font-size:23px;color:#c9c9c9;margin-top:12px">Send the drawing and I'll reply with a quote.</div>
 </div>
 {foot('From $450')}
</div></body></html>"""


def shoot(html, name):
    p = OUT / f'{name}.html'; p.write_text(html)
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        pg = b.new_page(viewport={'width': W, 'height': H})
        errs = []; pg.on('pageerror', lambda e: errs.append(str(e)))
        pg.goto(p.resolve().as_uri()); pg.wait_for_timeout(350)
        pg.screenshot(path=str(OUT / f'{name}.png'))
        b.close()
        if errs: print('ERR', name, errs[:2])
    return OUT / f'{name}.png'


if __name__ == '__main__':
    # real frames out of a real reel — a still can't show motion, so show the stages
    src = Q / 'r1030_1223_draw_shotgun.mp4'
    frames = []
    for i, t in enumerate((3.0, 7.0, 11.5)):
        f = OUT / f'f{i}.png'
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-ss', str(t), '-i', str(src),
                        '-frames:v', '1', '-vf', 'crop=1000:1080:40:560', str(f)], check=True)
        frames.append(f.as_uri())
    shots = []
    for i, (clip, t) in enumerate((('r1030_0841_elev_butterfly.mp4', 11.0),
                                   ('r1031_0841_pop3d_dogtrot.mp4', 10.0),
                                   ('r1029_1223_site2plan_lshape.mp4', 12.0))):
        f = OUT / f's{i}.png'
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-ss', str(t), '-i', str(Q / clip),
                        '-frames:v', '1', '-vf', 'crop=1000:1000:40:620', str(f)], check=True)
        shots.append(f.as_uri())
    for name, html in (('pin1_what', post1()), ('pin2_before_after', post2(frames)), ('pin3_pricing', post3(shots))):
        print('wrote', shoot(html, name))
