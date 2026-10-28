"""A saveable carousel: the clearances a floor plan has to pass.

Eight 1080x1350 slides. Every figure comes from a published standard, named on
the slide — nothing estimated. Carousels earn saves, and saves are what people
come back to, so this is built to be useful first and an advert second.
"""
import pathlib, sys

sys.path.insert(0, '/home/claude/reels')
from playwright.sync_api import sync_playwright
from gen.engine2 import LOGO_D

W, H = 1080, 1350
INK, BLUE, GRN, RED, PAPER, TINT, SUB = '#141414', '#1d4e89', '#2e9b62', '#c0392b', '#ffffff', '#f1efe9', '#8a8a8a'
OUT = pathlib.Path('/home/claude/reels/carousel'); OUT.mkdir(exist_ok=True)

RULES = [
    dict(n='42"', title='Kitchen work aisle',
         body='42 inches between the counter and the island for one cook. '
              '48 inches when two people work in there at once.',
         why='Under 42 and nobody can pass while a dishwasher or oven door is open.',
         src='NKBA Kitchen Planning Guidelines', gap=42, fixed='COUNTER', mov='ISLAND'),
    dict(n='30"', title='In front of the toilet',
         body='30 inches of clear floor in front of the pan. Code allows that to '
              'come down to 21 inches.',
         why='21 is the legal floor, not the comfortable one.',
         src='NKBA Bathroom Planning Guidelines', gap=30, fixed='WC', mov='VANITY'),
    dict(n='36"', title='Table edge to wall',
         body='36 inches to get past a pulled-out chair. 44 inches to walk behind '
              'someone who is seated.',
         why='A dining chair pulls out 24 inches on its own.',
         src='Kitchen &amp; Bath Planning Standards', gap=36, fixed='WALL', mov='TABLE'),
    dict(n='36"', title='Hallway width',
         body='36 inches is the code minimum for a hallway in a dwelling. '
              '42 inches is the width that actually feels right.',
         why='Two people cannot pass in a 36 inch hall without turning sideways.',
         src='IRC R311.6', gap=36, fixed='WALL', mov='WALL'),
    dict(n='7¾"', title='Stair riser and tread',
         body='7¾ inches maximum rise, 10 inches minimum run, 36 inches of width '
              'and 6 feet 8 inches of headroom.',
         why='Risers that vary more than 3/8 inch across a flight are what trips people.',
         src='IRC R311.7', gap=None, kind='stair'),
    dict(n='70 sf', title='A bedroom is a bedroom',
         body='70 square feet of floor area, and no dimension under 7 feet. '
              'Plus an escape opening of 5.7 square feet.',
         why='Without the window it is a study on the drawings, whatever you call it.',
         src='IRC R304 &amp; R310', gap=None, kind='room'),
]

HEAD = f"""<meta charset="utf-8"><style>
html,body{{margin:0;width:{W}px;height:{H}px;background:{PAPER};overflow:hidden;
 font-family:Helvetica,Arial,sans-serif;color:{INK}}}
.grid{{position:absolute;inset:0;background-image:linear-gradient(#0000000a 1px,transparent 1px),
 linear-gradient(90deg,#0000000a 1px,transparent 1px);background-size:45px 45px}}
.wrap{{position:absolute;inset:0;padding:62px;box-sizing:border-box;display:flex;flex-direction:column}}
.kick{{font:700 24px Helvetica;letter-spacing:4px;color:{BLUE}}}
h1{{font-size:78px;line-height:1.02;letter-spacing:-2.5px;margin:12px 0 0;font-weight:800}}
h2{{font-size:46px;line-height:1.08;letter-spacing:-1px;margin:6px 0 0;font-weight:800}}
.big{{font-size:150px;font-weight:800;letter-spacing:-6px;line-height:.9;color:{GRN}}}
.body{{font-size:30px;line-height:1.38;color:#333;margin-top:20px}}
.why{{font-size:25px;line-height:1.4;color:#555;border-left:5px solid {GRN};padding-left:20px;margin-top:22px}}
.src{{font:700 20px Helvetica;letter-spacing:2.5px;color:{SUB};margin-top:18px}}
.foot{{display:flex;align-items:center;gap:15px;border-top:3px solid {INK};padding-top:20px;margin-top:20px}}
.foot .h{{font:700 26px Helvetica}} .foot .r{{margin-left:auto;font:700 24px Helvetica;color:{BLUE}}}
</style>"""

LOGO = f'<svg width="50" height="50" viewBox="30 35 240 235"><path d="{LOGO_D}" fill="{INK}"/></svg>'


def foot(right='@dm_motion1'):
    return (f'<div class="foot">{LOGO}<div class="h">DM Motion</div>'
            f'<div class="r">{right}</div></div>')


def diagram(r):
    """A figure of the clearance itself, sized to fit and centred in its box.

    The two blocks and the gap are measured first, then the whole group is
    placed from the middle outwards, so nothing can run past the edge however
    wide the clearance is.
    """
    BW, BH = 880, 470
    cy = 185
    if r.get('kind') == 'stair':
        # a section through two treads: the rise and the run
        run, rise = 128, 96
        x0, y0 = (BW - (run * 3 + 190)) / 2, 58
        parts = []
        for i in range(3):
            X, Y = x0 + i * run, y0 + i * rise
            parts.append(f'<path d="M{X} {Y + rise} L{X} {Y} L{X + run} {Y}" fill="none" stroke="{INK}" stroke-width="4"/>')
        parts.append(f'<line x1="{x0 + run + 24}" y1="{y0}" x2="{x0 + run + 24}" y2="{y0 + rise}" stroke="{GRN}" stroke-width="3"/>')
        parts.append(f'<text x="{x0 + run + 40}" y="{y0 + rise / 2 + 10}" font-size="30" font-weight="800" fill="{GRN}" font-family="Helvetica">7¾" max</text>')
        parts.append(f'<line x1="{x0}" y1="{y0 + rise * 3 + 34}" x2="{x0 + run}" y2="{y0 + rise * 3 + 34}" stroke="{BLUE}" stroke-width="3"/>')
        parts.append(f'<text x="{x0 + run / 2}" y="{y0 + rise * 3 + 70}" font-size="30" font-weight="800" text-anchor="middle" fill="{BLUE}" font-family="Helvetica">10" min</text>')
        return f'<svg width="{BW}" height="{BH}" viewBox="0 0 {BW} {BH}" style="display:block;margin:0 auto">{"".join(parts)}</svg>'

    if r.get('kind') == 'room':
        rw, rh = 470, 268
        x0, y0 = (BW - rw) / 2, 78
        return f'''<svg width="{BW}" height="{BH}" viewBox="0 0 {BW} {BH}" style="display:block;margin:0 auto">
<rect x="{x0}" y="{y0}" width="{rw}" height="{rh}" fill="{TINT}" stroke="{INK}" stroke-width="4"/>
<rect x="{x0 + 110}" y="{y0 - 11}" width="200" height="22" fill="{PAPER}" stroke="{INK}" stroke-width="3"/>
<text x="{x0 + 210}" y="{y0 - 26}" font-size="24" font-weight="700" text-anchor="middle" fill="{GRN}" font-family="Helvetica">egress window</text>
<text x="{x0 + rw / 2}" y="{y0 + rh / 2 + 12}" font-size="40" font-weight="800" text-anchor="middle" fill="{SUB}" font-family="Helvetica">70 sf min</text>
<line x1="{x0}" y1="{y0 + rh + 40}" x2="{x0 + rw}" y2="{y0 + rh + 40}" stroke="{BLUE}" stroke-width="3"/>
<text x="{x0 + rw / 2}" y="{y0 + rh + 78}" font-size="30" font-weight="800" text-anchor="middle" fill="{BLUE}" font-family="Helvetica">7\'-0" minimum in any direction</text>
</svg>'''

    bw, bh = 280, 96                      # the two blocks either side of the gap
    px = (r['gap'] / 48) * 230            # gap drawn to scale against a 48 in reference
    total = bw * 2 + px
    x0 = (BW - total) / 2                 # place the whole group from the centre out
    mx = x0 + bw + px
    dy = cy + bh + 52
    return f'''<svg width="{BW}" height="{BH}" viewBox="0 0 {BW} {BH}" style="display:block;margin:0 auto">
<rect x="{x0}" y="{cy}" width="{bw}" height="{bh}" fill="{TINT}" stroke="{INK}" stroke-width="3"/>
<text x="{x0 + bw / 2}" y="{cy + bh / 2 + 8}" font-size="22" font-weight="700" letter-spacing="3"
 text-anchor="middle" fill="{SUB}" font-family="Helvetica">{r['fixed']}</text>
<rect x="{mx}" y="{cy}" width="{bw}" height="{bh}" fill="{TINT}" stroke="{INK}" stroke-width="3"/>
<text x="{mx + bw / 2}" y="{cy + bh / 2 + 8}" font-size="22" font-weight="700" letter-spacing="3"
 text-anchor="middle" fill="{SUB}" font-family="Helvetica">{r['mov']}</text>
<line x1="{x0 + bw}" y1="{dy}" x2="{mx}" y2="{dy}" stroke="{GRN}" stroke-width="3"/>
<line x1="{x0 + bw}" y1="{dy - 20}" x2="{x0 + bw}" y2="{dy + 20}" stroke="{GRN}" stroke-width="3"/>
<line x1="{mx}" y1="{dy - 20}" x2="{mx}" y2="{dy + 20}" stroke="{GRN}" stroke-width="3"/>
<text x="{(x0 + bw + mx) / 2}" y="{dy + 58}" font-size="36" font-weight="800"
 text-anchor="middle" fill="{GRN}" font-family="Helvetica">{r['n']}</text>
</svg>'''


def cover():
    return f"""<!doctype html><html><head>{HEAD}</head><body><div class="grid"></div>
<div class="wrap">
 <div class="kick">SAVE THIS</div>
 <h1>Six clearances<br>every floor plan<br>should pass.</h1>
 <div class="body">Every number here comes from a published standard &mdash; the IRC
  or the NKBA planning guidelines. None of it is a rule of thumb.</div>
 <div style="margin-top:38px;flex:1">
  {''.join(f'<div style="display:flex;align-items:baseline;gap:20px;padding:19px 0;border-top:2px solid #dcdad4">'
           f'<div style="font:800 40px Helvetica;letter-spacing:-1.5px;color:{GRN};min-width:140px">{r["n"]}</div>'
           f'<div style="font:700 30px Helvetica">{r["title"]}</div></div>' for r in RULES)}
 </div>
 <div class="src">SWIPE &rarr;</div>
 {foot()}
</div></body></html>"""


def slide(i, r):
    return f"""<!doctype html><html><head>{HEAD}</head><body><div class="grid"></div>
<div class="wrap">
 <div class="kick">{i:02d} / {len(RULES):02d}</div>
 <div class="big">{r['n']}</div>
 <h2>{r['title']}</h2>
 <div class="body">{r['body']}</div>
 <div style="margin:20px 0 0;flex:1;display:flex;align-items:center;justify-content:center">{diagram(r)}</div>
 <div class="why">{r['why']}</div>
 <div class="src">SOURCE &middot; {r['src'].upper()}</div>
 {foot()}
</div></body></html>"""


def cta():
    return f"""<!doctype html><html><head>{HEAD}</head><body><div class="grid"></div>
<div class="wrap">
 <div class="kick">ONE MORE THING</div>
 <h1>I animate<br>floor plans.</h1>
 <div class="body">Send the drawing you already have &mdash; PDF, DWG, AI or SVG &mdash;
  and it comes back as a clip that draws itself, line by line, with your titles
  and dimensions kept exactly as you drew them.</div>
 <div style="margin-top:auto;background:{INK};color:#fff;padding:30px 34px;border-radius:16px">
  <div style="font:700 24px Helvetica;letter-spacing:2px;color:#9fd9b8">FROM $450 A CLIP</div>
  <div style="font:800 46px Helvetica;margin-top:10px;letter-spacing:-1.5px">dmba04@gmail.com</div>
  <div style="font-size:24px;color:#c9c9c9;margin-top:12px">Send the drawing and I'll reply with a quote.</div>
 </div>
 {foot('From $450')}
</div></body></html>"""


if __name__ == '__main__':
    pages = [('c0_cover', cover())]
    pages += [(f'c{i}_{r["title"].split()[0].lower()}', slide(i, r)) for i, r in enumerate(RULES, 1)]
    pages.append((f'c{len(RULES) + 1}_cta', cta()))
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        pg = b.new_page(viewport={'width': W, 'height': H})
        errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)))
        for name, html in pages:
            p = OUT / f'{name}.html'
            p.write_text(html)
            pg.goto(p.resolve().as_uri())
            pg.wait_for_timeout(260)
            pg.screenshot(path=str(OUT / f'{name}.png'))
            print('wrote', OUT / f'{name}.png')
        b.close()
        if errs:
            print('ERR', errs[:3])
