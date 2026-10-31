"""WRONG vs RIGHT clearance reels.

Built as a shot sequence, not a single animated diagram. Five hard cuts in eight
seconds: macro on the violation, wide to place it, mid on the person who can't
fit, wide for the correction, then the plan tilts up into 3D. Every number comes
from a published standard, named on screen.
"""
import sys, json, math, pathlib, subprocess, zlib
sys.path.insert(0, '/home/claude/reels')
from playwright.sync_api import sync_playwright
import soundtrack

W, H, FPS = 1080, 1920, 30
INK, SUB, RED, GRN, BG, TINT, TINT2 = '#1f1f1f', '#8a8a8a', '#c0392b', '#2e9b62', '#ffffff', '#f1efe9', '#e4e1d9'
WALL = 0.5            # 6" wall, drawn as solid poché
EXTRUDE = 96          # px the wall tops lift by in the 3D shot


def inches(v):
    ft, i = int(v // 12), int(round(v % 12))
    if i == 12: ft, i = ft + 1, 0
    return f'{ft}\'-{i}"' if ft else f'{i}"'


TOPICS = {
 'island': dict(
    vo_stakes='Open the dishwasher and nobody gets through.', room_word='kitchen', setup='This kitchen looks fine.', question='Watch the aisle.', gapname='aisle', idx=1,
    topic='KITCHEN ISLAND AISLE', hook='Your island is<br>too close', sub='the aisle rule most kitchens break',
    room=(16, 13), wrong=30, right=42, door_d=2.0, door_label='DISHWASHER',
    fixed=[(0, 0, 16, 2, 'COUNTER', 'counter'), (0, 2, 2, 7, '', 'counter'), (14, 2, 2, 7, '', 'counter')],
    mov=dict(w=8, d=3.5, label='ISLAND', axis='y', base=2.0),
    rule='42" minimum aisle for one cook<br>48" when two people cook', source='NKBA KITCHEN PLANNING GUIDELINES', verdict='NKBA',
    note='Two people can\'t pass with a dishwasher door open.'),
 'fridge': dict(
    vo_stakes='Open the fridge and the aisle disappears.', room_word='kitchen', setup='This kitchen looks fine.', question='Now open the fridge.', gapname='aisle', idx=2,
    topic='FRIDGE DOOR SWING', hook='Your fridge<br>can\'t open', sub='the clearance people forget',
    room=(16, 13), wrong=30, right=42, door_d=2.3, door_label='FRIDGE DOOR',
    fixed=[(0, 0, 16, 2, 'COUNTER', 'counter'), (0, 2, 2, 7, '', 'counter'), (14, 2, 2, 7, '', 'counter')],
    mov=dict(w=8, d=3.5, label='ISLAND', axis='y', base=2.0),
    rule='42" minimum aisle for one cook<br>48" when two people cook', source='NKBA KITCHEN PLANNING GUIDELINES', verdict='NKBA',
    note='A fridge door eats 24-28" before anyone stands in it.'),
 'toilet': dict(
    vo_stakes='Your knees are in the vanity.', room_word='bathroom', setup='This bathroom looks fine.', question='Watch in front of the toilet.', gapname='space in front of the toilet', idx=3,
    topic='TOILET CLEARANCE', hook='Your toilet has<br>no room in front', sub='the bathroom number people guess at',
    room=(9, 8), wrong=21, right=30,
    fixed=[(0, 0, 9, 1.6, '', 'counter'), (3.1, 0.4, 1.6, 2.1, 'WC', 'counter')],
    mov=dict(w=6.5, d=1.9, label='VANITY', axis='y', base=2.5),
    rule='30" clear in front of the toilet<br>code allows a reduction to 21"', source='NKBA BATHROOM PLANNING GUIDELINES', verdict='NKBA',
    note='21" is the legal floor, not the comfortable one. At 21" your knees are in the vanity.'),
 'hallway': dict(
    vo_stakes='Two people have to turn sideways.', room_word='hallway', setup='This hall looks fine.', question='Send two people down it.', gapname='hall', idx=4,
    topic='HALLWAY WIDTH', hook='Two people can\'t<br>pass in this hall', sub='the number code sets, and the one that works',
    room=(13, 11), wrong=30, right=42, verdict='IRC',
    fixed=[(0, 0, 13, 2.4, 'BEDROOM', 'counter')],
    mov=dict(w=13, d=2.4, label='BEDROOM', axis='y', base=2.4),
    rule='36" is the code minimum for a hallway<br>42" is the width that actually works',
    source='IRC R311.6', note='At 36" two people turn sideways. At 42" they don\'t.'),
 'vanity': dict(
    vo_stakes="You can't lean over the sink.", room_word='bathroom', setup='This bathroom looks fine.', question='Watch the space at the sink.', gapname='space at the sink', idx=5,
    topic='IN FRONT OF THE SINK', hook='You can\'t stand<br>at this sink', sub='the clearance a small bath always loses',
    room=(10, 9), wrong=21, right=30, verdict='NKBA',
    fixed=[(0, 0, 10, 2.0, 'VANITY', 'counter')],
    mov=dict(w=7, d=2.6, label='TUB', axis='y', base=2.0),
    rule='30" of clear floor in front of a sink<br>measured from the front edge of the bowl',
    source='NKBA BATHROOM PLANNING GUIDELINES',
    note='Lean over a sink to wash your face and you need every inch of it.'),
 'shower': dict(
    vo_stakes='You step out into the vanity.', room_word='bathroom', setup='This bath looks fine.', question='Now step out of the shower.', gapname='space you dry off in', idx=6,
    topic='IN FRONT OF THE SHOWER', hook='Nowhere to dry<br>off in this bath', sub='the gap people find out about too late',
    room=(11, 10), wrong=20, right=30, verdict='NKBA',
    fixed=[(0, 0, 11, 2.8, 'SHOWER', 'counter')],
    mov=dict(w=8, d=2.0, label='VANITY', axis='y', base=2.8),
    rule='30" of clear floor in front of a shower or tub<br>same figure as in front of a sink',
    source='NKBA BATHROOM PLANNING GUIDELINES',
    note='You step out, you turn, you reach for a towel. That takes 30 inches.'),
 'dining': dict(
    vo_stakes='The chair hits the wall before you stand up.', room_word='dining room', setup='This dining room looks fine.', question='Now pull out a chair.', gapname='space behind the chair', idx=7,
    topic='DINING TABLE CLEARANCE', hook='Nobody can get<br>out of this chair', sub='the gap every dining room gets wrong',
    room=(14, 12), wrong=24, right=36,
    fixed=[(0, 0, 14, 1.5, '', 'counter'), (0, 1.5, 1.4, 5, '', 'counter')],
    mov=dict(w=6, d=3.2, label='TABLE', axis='y', base=1.5),
    rule='36" from table edge to wall to pass a chair<br>44" to walk behind someone seated', source='KITCHEN &amp; BATH PLANNING STANDARDS', verdict='CLEARS',
    note='A dining chair pulls out 24" on its own. Anything less and the chair hits the wall.'),
}


EXN = 14              # stacked layers that make the walls read as solid when they rise


def build(spec):
    RW, RD = spec['room']
    S = min(820 / RW, 620 / RD)
    X0 = 540 - RW * S / 2
    Y0 = 700
    X = lambda f: X0 + f * S
    Y = lambda f: Y0 + f * S

    # ---- beats are cut to the voiceover, not the other way round ----
    T = dict(setup=0.00, hunt=1.20, reveal=3.05, stakes=4.50, door=7.05,
             turn=9.65, sell=12.05, end=15.10)
    T['found'] = T['hunt']; T['open'] = T['sell']
    T['move'] = (9.75, 10.70)
    dur = T['end']

    mv = spec['mov']
    VERDICT = spec.get('verdict', 'CLEARS')
    gap_w, gap_r = spec['wrong'] / 12, spec['right'] / 12
    base = mv['base']
    yw, yr = base + gap_w, base + gap_r
    mx = (RW - mv['w']) / 2
    delta = spec['right'] - spec['wrong']

    N = {6:'six',8:'eight',9:'nine',10:'ten',12:'twelve',15:'fifteen',18:'eighteen',
         20:'twenty',21:'twenty-one',24:'twenty-four',30:'thirty',36:'thirty-six',
         42:'forty-two',48:'forty-eight'}
    w_w, w_r, w_d = N.get(spec['wrong'], spec['wrong']), N.get(spec['right'], spec['right']), N.get(delta, delta)

    wall_d = (f'M{X(-WALL):.1f} {Y(-WALL):.1f} H{X(RW + WALL):.1f} V{Y(RD + WALL):.1f} '
              f'H{X(-WALL):.1f} Z '
              f'M{X(0):.1f} {Y(0):.1f} H{X(RW):.1f} V{Y(RD):.1f} H{X(0):.1f} Z')
    floor = (f'<rect x="{X(0):.1f}" y="{Y(0):.1f}" width="{RW * S:.1f}" '
             f'height="{RD * S:.1f}" fill="#fcfbf8"/>')
    # the extrusion: stacked copies of the wall ring, darkest at the base.
    # drawn far-to-near so the rise reads solid once the plan tilts.
    ex = []
    for i in range(EXN - 1, -1, -1):
        f = i / max(1, EXN - 1)
        g = int(58 + 96 * f)
        ex.append(f'<path class="ex" d="{wall_d}" fill="rgb({g},{g-4},{g-14})" fill-rule="evenodd"/>')
    fixed = []
    for fx, fy, fw, fh, lab, kind in spec['fixed']:
        fixed.append(f'<g class="fx"><rect x="{X(fx):.1f}" y="{Y(fy):.1f}" width="{fw * S:.1f}" '
                     f'height="{fh * S:.1f}" fill="url(#hatch)" stroke="{INK}" stroke-width="2.6"/>')
        if lab:
            fixed.append(f'<text x="{X(fx + fw / 2):.1f}" y="{Y(fy + fh / 2) + 8:.1f}" font-size="22" '
                         f'font-weight="700" letter-spacing="3" text-anchor="middle" fill="{SUB}" '
                         f'font-family="Helvetica">{lab}</text>')
        fixed.append('</g>')

    L1 = f"You'd approve this {spec['room_word']}."
    L2 = "Find what's wrong."
    L3 = f"The {spec['gapname']} is {spec['wrong']}″."
    L4 = f"It needs {spec['right']}″. {delta}″ short."
    L5 = spec['vo_stakes']
    L6 = "Free to move on paper. Not after the pour."
    L7 = "You didn't see it until it moved."

    # every reel is voiced, end to end — silence is where viewers leave
    VO = [(0.08, L1),
          (1.26, "Three seconds. Find what's wrong."),
          (3.11, f"The {spec['gapname']} is {w_w} inches."),
          (4.56, f"It needs {w_r}. {str(w_d).capitalize()} inches short."),
          (7.13, L5),
          (9.72, "Free to move on paper. Not after the pour."),
          (12.15, L7),
          (13.83, "Send me your drawing.")]

    data = dict(T=T, S=S, X0=X0, Y0=Y0, RW=RW, RD=RD, mw=mv['w'], md=mv['d'], mx=mx,
                yw=yw, yr=yr, gw=gap_w, gr=gap_r, base=base, label=mv['label'],
                right_in=spec['right'], wrong_in=spec['wrong'], extrude=EXTRUDE, exn=EXN,
                door_w=2.0, door_d=spec.get('door_d', 0.0), door_label=spec.get('door_label', ''),
                fit_min=spec.get('fit_min', 1.4 if spec.get('door_d') else spec['right'] / 12 - 0.01))

    return f"""<!doctype html><html><head><meta charset="utf-8"><style>
html,body{{margin:0;width:{W}px;height:{H}px;background:{BG};overflow:hidden;
 font-family:Helvetica,Arial,sans-serif;color:{INK}}}
#grid{{position:absolute;inset:-200px;background-image:
 linear-gradient(#1f1f1f0d 1px,transparent 1px),linear-gradient(90deg,#1f1f1f0d 1px,transparent 1px);
 background-size:54px 54px}}
#stage{{position:absolute;inset:0;perspective:1450px;perspective-origin:540px 860px}}
#world{{position:absolute;inset:0;transform-style:preserve-3d}}
#scrimT{{position:absolute;left:0;right:0;top:0;height:530px;pointer-events:none;
 background:linear-gradient(#fff 0,#fff 78%,#ffffff00 100%)}}
#scrimB{{position:absolute;left:0;right:0;bottom:0;height:680px;pointer-events:none;
 background:linear-gradient(#ffffff00 0,#fff 34%,#fff 100%);opacity:0}}
#spec{{position:absolute;left:55px;right:55px;top:112px;text-align:center}}
#spec span{{display:inline-block;border:2.5px solid {INK};font:700 25px Helvetica;
 letter-spacing:3px;padding:8px 19px;border-radius:8px;background:#fff}}
.ln{{position:absolute;left:52px;right:52px;top:188px;text-align:center;opacity:0;
 font-size:62px;font-weight:800;line-height:1.07;letter-spacing:-1.6px}}
.ln .wd{{display:inline-block}}
.ln.sm{{font-size:46px;letter-spacing:-0.8px;line-height:1.18;top:200px}}
.ln.red{{color:{RED}}}
.verdict{{position:absolute;left:0;right:0;top:404px;text-align:center;opacity:0}}
.verdict span{{display:inline-flex;align-items:center;gap:14px;color:#fff;font:900 48px Helvetica;
 letter-spacing:3px;padding:13px 32px;border-radius:12px}}
#dimnum{{position:absolute;opacity:0;transform-origin:50% 50%;will-change:transform}}
#dimnum b{{display:inline-block;font:900 58px Helvetica;letter-spacing:-2px;padding:6px 16px;
 border-radius:10px;background:#fff;border:3px solid {RED};color:{RED}}}
#cd{{position:absolute;left:0;right:0;top:350px;text-align:center;opacity:0;
 font:900 94px Helvetica;letter-spacing:-4px;color:{RED};transform-origin:50% 50%}}
#rule{{position:absolute;left:92px;right:92px;top:1462px;opacity:0;border:3px solid {INK};
 border-radius:16px;padding:22px 26px;background:#fff;box-shadow:9px 9px 0 {INK};text-align:center}}
#rule div{{font:800 35px Helvetica;line-height:1.34}}
#rule small{{display:block;font:600 21px Helvetica;color:{SUB};letter-spacing:1.5px;margin-top:9px}}
#offer{{position:absolute;left:46px;right:46px;top:1548px;text-align:center;opacity:0}}
#offer span{{display:inline-block;border:3px solid {INK};background:#fff;border-radius:14px;
 font:800 34px Helvetica;letter-spacing:-0.5px;padding:18px 26px;box-shadow:8px 8px 0 {INK}}}
#more{{position:absolute;left:55px;right:55px;top:1678px;text-align:center;opacity:0;
 font:700 31px Helvetica;letter-spacing:0.5px}}
#send{{position:absolute;left:55px;right:55px;top:1760px;text-align:center;opacity:0}}
#send span{{display:inline-block;background:{INK};color:#fff;font:800 33px Helvetica;
 letter-spacing:-0.5px;padding:17px 29px;border-radius:14px}}
#ser{{position:absolute;left:0;right:0;top:1856px;text-align:center;
 font:700 22px Helvetica;letter-spacing:5px;color:#b0aca2}}
#flash{{position:absolute;inset:0;background:#fff;opacity:0;pointer-events:none}}
</style></head><body>
<div id="grid"></div>
<div id="stage"><div id="world">
<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" style="position:absolute;left:0;top:0">
 <defs>
  <pattern id="hatch" width="9" height="9" patternTransform="rotate(45)" patternUnits="userSpaceOnUse">
   <rect width="9" height="9" fill="{TINT}"/><line x1="0" y1="0" x2="0" y2="9" stroke="#c9c4b8" stroke-width="2"/>
  </pattern>
  <pattern id="warn" width="16" height="16" patternTransform="rotate(45)" patternUnits="userSpaceOnUse">
   <rect width="16" height="16" fill="{RED}" fill-opacity="0.13"/>
   <line x1="0" y1="0" x2="0" y2="16" stroke="{RED}" stroke-width="5" stroke-opacity="0.34"/>
  </pattern>
  <pattern id="safe" width="16" height="16" patternTransform="rotate(45)" patternUnits="userSpaceOnUse">
   <rect width="16" height="16" fill="{GRN}" fill-opacity="0.13"/>
   <line x1="0" y1="0" x2="0" y2="16" stroke="{GRN}" stroke-width="5" stroke-opacity="0.34"/>
  </pattern>
  <pattern id="sheet" width="46" height="46" patternUnits="userSpaceOnUse">
   <rect width="46" height="46" fill="#fcfbf8"/>
   <path d="M46 0 V46 M0 46 H46" stroke="#1f1f1f" stroke-opacity="0.07" stroke-width="1.4"/>
  </pattern>
  <marker id="ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="5" markerHeight="5" orient="auto">
   <path d="M0 0 L10 5 L0 10 z" fill="context-stroke"/></marker>
  <marker id="ar2" viewBox="0 0 10 10" refX="1" refY="5" markerWidth="5" markerHeight="5" orient="auto">
   <path d="M10 0 L0 5 L10 10 z" fill="context-stroke"/></marker>
 </defs>
 <g id="cam">
  <rect x="{X(-9):.1f}" y="{Y(-9):.1f}" width="{(RW + 18) * S:.1f}" height="{(RD + 18) * S:.1f}" fill="url(#sheet)"/>
  {floor}
  <g id="exg" opacity="0">{''.join(ex)}</g>
  <path id="walls" d="{wall_d}" fill="{INK}" fill-rule="evenodd"/>
  <g id="zone"></g>
  <g id="fixed">{''.join(fixed)}</g>
  <g id="ghost" opacity="0"></g>
  <g id="streak" opacity="0"></g>
  <g id="mov"></g>
  <g id="per" opacity="0"></g>
  <g id="clash"></g>
  <g id="req"></g>
  <g id="dim"></g>
  <g id="ret" opacity="0"></g>
 </g>
</svg>
</div></div>
<div id="scrimB"></div>
<div id="scrimT"></div>
<div id="spec"><span>{spec['topic']}</span></div>
<div class="ln" id="l1">{L1}</div>
<div class="ln" id="l2">{L2}</div>
<div class="ln" id="l3">{L3}</div>
<div class="ln red" id="l4">{L4}</div>
<div class="ln sm red" id="l5">{L5}</div>
<div class="ln sm" id="l6">{L6}</div>
<div class="ln" id="l7">{L7}</div>
<div id="cd">3</div>
<div class="verdict" id="vw"><span style="background:{RED}"><svg width="32" height="32"><path d="M6 6 L26 26 M26 6 L6 26" stroke="#fff" stroke-width="7" stroke-linecap="round"/></svg>TOO TIGHT</span></div>
<div class="verdict" id="vr"><span style="background:{GRN}"><svg width="36" height="32"><path d="M5 17 L14 26 L31 6" stroke="#fff" stroke-width="7" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>{VERDICT}</span></div>
<div id="dimnum"><b></b></div>
<div id="rule"><div>{spec['rule']}</div><small>{spec['source']}</small></div>
<div id="offer"><span>I animate plans and elevations &middot; from $450</span></div>
<div id="more">dmba04@gmail.com</div>
<div id="send"><span>Send this to whoever drew it</span></div>
<div id="ser">CLEARANCE &nbsp;{spec['idx']:02d}&nbsp;/&nbsp;07</div>
<div id="flash"></div>
<script>
const D={json.dumps(data)}, T=D.T, E=T.end, NS='http://www.w3.org/2000/svg';
const $=i=>document.getElementById(i), cl=(x,a,b)=>Math.max(a,Math.min(b,x)), P=(t,a,d)=>cl((t-a)/d,0,1);
const ease=t=>t<.5?2*t*t:1-Math.pow(-2*t+2,2)/2, eo=x=>1-Math.pow(1-x,3), eob=x=>1-Math.pow(1-x,5);
const X=f=>D.X0+f*D.S, Y=f=>D.Y0+f*D.S, S=D.S;
const EXL=[...document.querySelectorAll('#exg .ex')];   // far -> near
const FX=[...document.querySelectorAll('#fixed .fx')];

const rg=$('ret');
const rc=document.createElementNS(NS,'circle');
rc.setAttribute('fill','none');rc.setAttribute('stroke','{INK}');rc.setAttribute('stroke-width','3.5');rg.appendChild(rc);
const rx1=document.createElementNS(NS,'line'),rx2=document.createElementNS(NS,'line');
[rx1,rx2].forEach(e=>{{e.setAttribute('stroke','{INK}');e.setAttribute('stroke-width','3');rg.appendChild(e);}});
const rq=document.createElementNS(NS,'rect');
rq.setAttribute('fill','none');rq.setAttribute('stroke','{INK}');rq.setAttribute('stroke-width','3');
rq.setAttribute('stroke-dasharray','14 8');$('req').appendChild(rq);
const rqbg=document.createElementNS(NS,'rect');rqbg.setAttribute('fill','#fff');rqbg.setAttribute('rx','6');$('req').appendChild(rqbg);
const rqt=document.createElementNS(NS,'text');
rqt.setAttribute('font-size','22');rqt.setAttribute('font-weight','800');rqt.setAttribute('letter-spacing','2');
rqt.setAttribute('text-anchor','middle');rqt.setAttribute('fill','{INK}');rqt.setAttribute('font-family','Helvetica');
rqt.textContent=D.right_in+'" REQUIRED';$('req').appendChild(rqt);
const cls=document.createElementNS(NS,'rect');cls.setAttribute('fill','{RED}');cls.setAttribute('fill-opacity','0.62');$('clash').appendChild(cls);
const clt=document.createElementNS(NS,'text');
clt.setAttribute('font-size','24');clt.setAttribute('font-weight','900');clt.setAttribute('letter-spacing','1');
clt.setAttribute('text-anchor','middle');clt.setAttribute('fill','#fff');clt.setAttribute('font-family','Helvetica');$('clash').appendChild(clt);
const zr=document.createElementNS(NS,'rect');$('zone').appendChild(zr);
const gh=document.createElementNS(NS,'rect');
gh.setAttribute('fill','none');gh.setAttribute('stroke','{RED}');gh.setAttribute('stroke-width','3');
gh.setAttribute('stroke-dasharray','11 9');$('ghost').appendChild(gh);
const ghl=document.createElementNS(NS,'text');
ghl.setAttribute('font-size','20');ghl.setAttribute('font-weight','700');ghl.setAttribute('letter-spacing','2');
ghl.setAttribute('text-anchor','middle');ghl.setAttribute('fill','{RED}');ghl.setAttribute('font-family','Helvetica');
ghl.textContent='WAS HERE';$('ghost').appendChild(ghl);
const streaks=[];
for(let i=0;i<7;i++){{const l=document.createElementNS(NS,'line');
 l.setAttribute('stroke','{INK}');l.setAttribute('stroke-width','2');l.setAttribute('stroke-linecap','round');
 $('streak').appendChild(l);streaks.push(l);}}
const box=document.createElementNS(NS,'rect');
box.setAttribute('fill','{TINT2}');box.setAttribute('stroke','{INK}');box.setAttribute('stroke-width','3.4');$('mov').appendChild(box);
const lab=document.createElementNS(NS,'text');
lab.setAttribute('font-size','25');lab.setAttribute('font-weight','800');lab.setAttribute('letter-spacing','3');
lab.setAttribute('text-anchor','middle');lab.setAttribute('fill','{SUB}');lab.setAttribute('font-family','Helvetica');
lab.textContent=D.label;$('mov').appendChild(lab);
const dg=$('dim');
const dl=document.createElementNS(NS,'line'),t1=document.createElementNS(NS,'line'),t2=document.createElementNS(NS,'line');
dl.setAttribute('marker-start','url(#ar2)');dl.setAttribute('marker-end','url(#ar)');
[dl,t1,t2].forEach(e=>{{e.setAttribute('stroke-width','3');dg.appendChild(e);}});
const pg=$('per');
const door=document.createElementNS(NS,'rect');
door.setAttribute('fill','#fff');door.setAttribute('stroke','{INK}');door.setAttribute('stroke-width','2.6');pg.appendChild(door);
const dlab=document.createElementNS(NS,'text');
dlab.setAttribute('font-size','19');dlab.setAttribute('font-weight','700');dlab.setAttribute('text-anchor','middle');
dlab.setAttribute('fill','{SUB}');dlab.setAttribute('font-family','Helvetica');dlab.textContent=D.door_label;pg.appendChild(dlab);
const sh=document.createElementNS(NS,'rect');sh.setAttribute('stroke-width','3.4');pg.appendChild(sh);
const hd=document.createElementNS(NS,'circle');pg.appendChild(hd);

const LINES=[['l1',T.setup+0.02,T.hunt],['l2',T.hunt+0.06,T.reveal],
             ['l3',T.reveal+0.06,T.stakes],['l4',T.stakes+0.06,T.door],
             ['l5',T.door+0.08,T.turn],['l6',T.turn+0.07,T.sell],
             ['l7',T.sell+0.10,E+0.5]];
LINES.forEach(([id])=>{{const d=$(id);
  d.innerHTML=d.innerHTML.split('<br>').map(L=>L.split(' ').map(w=>
    `<span class="wd">${{w}}</span>`).join(' ')).join('<br>');}});

const gapCy=Y(D.base+D.gw/2), cxMid=X(D.mx+D.mw*0.5);
const kM=cl(268/(D.gw*S),1.65,2.95);
const SH=[
 {{t:T.setup,  k:1.26,    cx:540,   cy:1010,      ay:1075, drift:0.06}},
 {{t:T.hunt,   k:1.34,    cx:540,   cy:1010,      ay:1075, drift:0.10}},
 {{t:T.reveal, k:kM,      cx:cxMid, cy:gapCy+58,  ay:1040, drift:0.09}},
 {{t:T.stakes, k:kM*0.74, cx:cxMid, cy:gapCy+34,  ay:1040, drift:0.07}},
 {{t:T.door,   k:kM*0.92, cx:X(D.mx+D.mw*0.56)+D.door_w*S*0.5, cy:gapCy+20, ay:1030, drift:0.08}},
 {{t:T.turn,   k:1.30,    cx:540,   cy:1010,      ay:1000, drift:0.05}},
 {{t:T.sell,   k:1.00,    cx:540,   cy:960,       ay:950,  drift:0.03, axo:1}},
];

window.setT=t=>{{
 let si=0; for(let i=0;i<SH.length;i++) if(t>=SH[i].t) si=i;
 const s=SH[si], nxt=SH[si+1], span=(nxt?nxt.t:E)-s.t, pr=cl((t-s.t)/span,0,1);
 const k=s.k*(1+s.drift*ease(pr));
 const tx=540-s.cx*k, ty=s.ay-s.cy*k;
 $('cam').setAttribute('transform',`translate(${{tx.toFixed(1)}} ${{ty.toFixed(1)}}) scale(${{k.toFixed(4)}})`);

 // the plan lifts into 3D and turns — this is the thing being sold
 const ax=s.axo?eo(cl(pr/0.40,0,1)):0;
 const orbit=s.axo?(-7+11*ease(cl((pr-0.25)/0.75,0,1))):0;
 $('world').style.transform=
   `rotateX(${{(ax*49).toFixed(2)}}deg) rotateY(${{orbit.toFixed(2)}}deg) translateY(${{(ax*-60).toFixed(1)}}px)`;
 EXL.forEach((e,i)=>{{ // EXL[0] is the top layer (drawn first, furthest away)
   const lv=(EXL.length-i)/EXL.length;
   e.setAttribute('transform',`translate(0 ${{(-D.extrude*ax*lv).toFixed(1)}})`);}});
 $('exg').setAttribute('opacity',ax);
 $('grid').style.transform=`translate(${{(-18*pr).toFixed(1)}}px,${{(-10*pr).toFixed(1)}}px)`;

 // fixtures drop in at the top so frame one already moves
 FX.forEach((e,i)=>{{const q=P(t,0.04+i*0.07,0.26);
   e.setAttribute('opacity',q);
   e.setAttribute('transform',`translate(0 ${{((1-eo(q))*-18).toFixed(1)}})`);}});

 const m=eob(P(t,T.move[0],T.move[1]-T.move[0]));
 const gap=D.gw+(D.gr-D.gw)*m, y=D.base+gap;
 const fixing=m>0.015&&m<0.985, done=m>=0.985;

 box.setAttribute('x',X(D.mx));box.setAttribute('y',Y(y));
 box.setAttribute('width',D.mw*S);box.setAttribute('height',D.md*S);
 lab.setAttribute('x',X(D.mx+D.mw/2));lab.setAttribute('y',Y(y+D.md/2)+8);
 $('mov').setAttribute('opacity',P(t,0.10,0.28));

 {{const ax0=D.RW*0.24*S, ay0=D.RD*0.22*S;
   let rcx=X(D.RW*0.5)+ax0*Math.sin(t*3.1+0.6), rcy=Y(D.RD*0.5)+ay0*Math.sin(t*4.3);
   const snap=eo(P(t,T.reveal-0.22,0.30));
   rcx+=(cxMid-rcx)*snap; rcy+=(gapCy-rcy)*snap;
   const rr=(152-54*snap)*(1+0.05*Math.sin(t*9));
   rc.setAttribute('cx',rcx);rc.setAttribute('cy',rcy);rc.setAttribute('r',rr);
   rx1.setAttribute('x1',rcx-rr-20);rx1.setAttribute('y1',rcy);rx1.setAttribute('x2',rcx-rr+16);rx1.setAttribute('y2',rcy);
   rx2.setAttribute('x1',rcx+rr-16);rx2.setAttribute('y1',rcy);rx2.setAttribute('x2',rcx+rr+20);rx2.setAttribute('y2',rcy);
   const rcol=snap>0.5?'{RED}':'{INK}';
   rc.setAttribute('stroke',rcol);rx1.setAttribute('stroke',rcol);rx2.setAttribute('stroke',rcol);
   rg.setAttribute('opacity',P(t,0.30,0.2)*(1-P(t,T.reveal+0.45,0.3)));}}

 {{const cd=$('cd'), el=cl(t-T.hunt,0,99), n=Math.max(1,3-Math.floor(el/0.58));
   cd.textContent=n;
   cd.style.transform=`scale(${{(1+0.26*(1-cl((el%0.58)/0.22,0,1))).toFixed(3)}})`;
   cd.style.opacity=P(t,T.hunt+0.04,0.14)*(1-P(t,T.reveal-0.16,0.16));}}

 const pulse=0.5+0.5*Math.sin(t*Math.PI*2*1.45);
 zr.setAttribute('x',X(D.mx));zr.setAttribute('y',Y(D.base));
 zr.setAttribute('width',D.mw*S);zr.setAttribute('height',Math.max(1,gap*S));
 zr.setAttribute('fill',done?'url(#safe)':'url(#warn)');
 zr.setAttribute('opacity',(done?0.95:0.62+0.38*pulse)*P(t,T.reveal,0.22));

 gh.setAttribute('x',X(D.mx));gh.setAttribute('y',Y(D.yw));
 gh.setAttribute('width',D.mw*S);gh.setAttribute('height',D.md*S);
 ghl.setAttribute('x',X(D.mx+D.mw/2));ghl.setAttribute('y',Y(D.yw+D.md/2)+7);
 $('ghost').setAttribute('opacity',P(t,T.move[0]+0.10,0.3)*(1-P(t,T.sell,0.3)));

 streaks.forEach((l,i)=>{{
   const fr=i/(streaks.length-1), yy=D.yw+(y-D.yw)*fr;
   const xx=X(D.mx+D.mw*(0.10+0.80*((i*0.37)%1)));
   l.setAttribute('x1',xx);l.setAttribute('y1',Y(yy));
   l.setAttribute('x2',xx);l.setAttribute('y2',Y(yy)+22);
   l.setAttribute('opacity',0.10+0.45*fr);}});
 $('streak').setAttribute('opacity',fixing?1:0);

 const col=done?'{GRN}':(fixing?'{INK}':'{RED}');
 const cx=X(D.mx+D.mw*0.17), ya=Y(D.base), yb=Y(y);
 [dl,t1,t2].forEach(e=>e.setAttribute('stroke',col));
 dl.setAttribute('x1',cx);dl.setAttribute('y1',ya+2);dl.setAttribute('x2',cx);dl.setAttribute('y2',yb-2);
 t1.setAttribute('x1',cx-30);t1.setAttribute('y1',ya);t1.setAttribute('x2',cx+30);t1.setAttribute('y2',ya);
 t2.setAttribute('x1',cx-30);t2.setAttribute('y1',yb);t2.setAttribute('x2',cx+30);t2.setAttribute('y2',yb);
 dg.setAttribute('opacity',P(t,T.reveal,0.2)*(1-P(t,T.sell,0.25)));

 {{const inch=Math.round(gap*12), dn=$('dimnum'), bb=dn.firstElementChild;
   bb.textContent=inch+'"'; bb.style.borderColor=col; bb.style.color=col;
   let anx=cx-118, sx=anx*k+tx;
   if(sx-70<46){{ anx=cx+96; sx=anx*k+tx; }}
   const sy=((ya+yb)/2)*k+ty;
   dn.style.left=cl(sx-70,34,{W}-212)+'px'; dn.style.top=cl(sy-44,512,1430)+'px';
   const pop=1+0.18*(1-cl((t-T.move[1])/0.3,0,1))*(t>=T.move[1]?1:0)
              +0.22*(1-cl((t-T.reveal)/0.3,0,1))*(t>=T.reveal?1:0);
   dn.style.transform=`scale(${{pop.toFixed(3)}})`;
   dn.style.opacity=P(t,T.reveal,0.18)*(1-P(t,T.sell,0.25));}}

 const dOpen=P(t,T.door,0.42)*D.door_d;
 door.setAttribute('x',X(D.mx+D.mw*0.56));door.setAttribute('y',Y(D.base));
 door.setAttribute('width',D.door_d?D.door_w*S:0);
 door.setAttribute('height',D.door_d?Math.max(1,dOpen*S):0);
 dlab.setAttribute('x',X(D.mx+D.mw*0.56+D.door_w/2));dlab.setAttribute('y',Y(D.base+dOpen/2)+7);
 dlab.setAttribute('opacity',dOpen>D.door_d*0.7?1:0);
 const left=gap-D.door_d, fits=left>=D.fit_min;
 const sq=fits?0:1, jit=sq*Math.sin(t*33)*2.2;
 const pcx=X(D.mx+D.mw*0.56+D.door_w/2)+jit;
 const pcy=Y(D.base+D.door_d+Math.max(0.35,left/2));
 {{const bw=1.66*S, bh=1.08*S, cR=fits?'{GRN}':'{RED}';
   sh.setAttribute('x',pcx-bw/2);sh.setAttribute('y',pcy-bh/2);
   sh.setAttribute('width',bw);sh.setAttribute('height',bh);
   sh.setAttribute('rx',Math.min(bh/2,0.5*S));
   sh.setAttribute('fill',cR);sh.setAttribute('fill-opacity','0.16');sh.setAttribute('stroke',cR);
   sh.setAttribute('stroke-opacity','0.75');
   hd.setAttribute('cx',pcx);hd.setAttribute('cy',pcy);hd.setAttribute('r',0.30*S);
   hd.setAttribute('fill',cR);hd.setAttribute('fill-opacity','0.9');}}
 pg.setAttribute('opacity',P(t,T.door,0.26)*(1-P(t,T.sell,0.3)));

 {{const yreq=D.base+D.gr, short=Math.max(0,(yreq-y)*12);
   rq.setAttribute('x',X(D.mx));rq.setAttribute('y',Y(D.base));
   rq.setAttribute('width',D.mw*S);rq.setAttribute('height',D.gr*S);
   rq.setAttribute('stroke',done?'{GRN}':'{INK}');rqt.setAttribute('fill',done?'{GRN}':'{INK}');
   const tw=(D.right_in+'" REQUIRED').length*13.2;
   rqbg.setAttribute('x',X(D.mx+D.mw*0.5)-tw/2-10);rqbg.setAttribute('y',Y(D.base)-35);
   rqbg.setAttribute('width',tw+20);rqbg.setAttribute('height',30);
   rqt.setAttribute('x',X(D.mx+D.mw*0.5));rqt.setAttribute('y',Y(D.base)-14);
   $('req').setAttribute('opacity',P(t,T.stakes-0.05,0.25)*(1-P(t,T.sell,0.25)));
   cls.setAttribute('x',X(D.mx));cls.setAttribute('y',Y(y));
   cls.setAttribute('width',D.mw*S);cls.setAttribute('height',Math.max(0,(yreq-y)*S));
   clt.textContent=Math.round(short)+'" SHORT';
   clt.setAttribute('x',X(D.mx+D.mw*0.5));clt.setAttribute('y',Y((y+yreq)/2)+9);
   clt.setAttribute('opacity',short>5?1:0);
   $('clash').setAttribute('opacity',P(t,T.stakes-0.05,0.25)*(1-P(t,T.sell,0.25)));}}

 $('vw').style.opacity=P(t,T.stakes+0.15,0.2)*(1-P(t,T.turn-0.1,0.18));
 $('vw').style.transform=`scale(${{1.3-0.3*eo(P(t,T.stakes+0.15,0.26))}})`;
 $('vr').style.opacity=P(t,T.move[1]-0.1,0.2)*(1-P(t,E-0.25,0.25));
 $('vr').style.transform=`scale(${{1.3-0.3*eo(P(t,T.move[1]-0.1,0.26))}})`;
 $('flash').style.opacity=0.6*(1-cl((t-T.turn)/0.07,0,1))*(t>=T.turn?1:0);

 LINES.forEach(([id,a,b])=>{{
   const d=$(id), ws=d.querySelectorAll('.wd'), out=1-P(t,b-0.20,0.18);
   d.style.opacity=out;
   ws.forEach((w,i)=>{{const q=P(t,a+i*0.05,0.22), e=eo(q);
     w.style.opacity=q;
     w.style.transform=`translateY(${{((1-e)*32).toFixed(1)}}px) scale(${{(0.88+0.12*e).toFixed(3)}})`;}});}});

 const rp=P(t,T.turn+0.5,0.3);
 $('rule').style.opacity=rp*(1-P(t,T.sell-0.1,0.25));
 $('rule').style.transform=`translateY(${{(44*(1-eob(rp))).toFixed(1)}}px)`;
 $('offer').style.opacity=P(t,T.sell+0.9,0.3);
 $('more').style.opacity=P(t,T.sell+1.3,0.3);
 $('send').style.opacity=P(t,T.sell+1.7,0.3);
 $('scrimB').style.opacity=Math.max(P(t,T.turn+0.35,0.3),P(t,T.sell,0.3));
 $('spec').style.opacity=1-P(t,T.sell+0.2,0.3);
 $('ser').style.opacity=0.55+0.45*P(t,T.sell+0.5,0.4);
}}; setT(0);
</script></body></html>""", dur, T, VO


def render(key, outdir='/home/claude/reels/out2', stills=None, voice=True):
    spec = TOPICS[key]; name = f'r_rule_{key}'
    out = pathlib.Path(outdir); out.mkdir(exist_ok=True)
    html, dur, T, VO = build(spec); hp = out / f'{name}.html'; hp.write_text(html)
    fr = out / f'fr_{name}'; fr.mkdir(exist_ok=True); N = int(FPS * dur)
    with sync_playwright() as pw:
        b = pw.chromium.launch(); pg = b.new_page(viewport={'width': W, 'height': H}); errs = []
        pg.on('pageerror', lambda e: errs.append(str(e))); pg.goto(hp.resolve().as_uri()); pg.wait_for_timeout(300)
        ts = stills or [i / FPS for i in range(N)]
        for i, t in enumerate(ts):
            pg.evaluate(f'setT({t})'); pg.screenshot(path=str(fr / (f's_{t:05.2f}.png' if stills else f'{i:04d}.png')))
        b.close()
        if errs: print('ERR', errs[:3])
    if stills: return [str(fr / f's_{t:05.2f}.png') for t in stills]
    wav = str(out / f'{name}.wav')
    # end == dur so the beat runs the whole clip and no end-card chime is added
    soundtrack.make(dur, draw=(0.2, 1.1), end=dur, mood='bright', bpm=100,
                    seed=zlib.crc32(key.encode()) % 999, out=wav, pen=False, beat=True)
    if voice:
        import vo as VOICE
        VOICE.mix_into(wav, VO)
    mp4 = str(out / f'{name}.mp4')
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-framerate', str(FPS), '-i', str(fr / '%04d.png'), '-i', wav, '-c:v', 'libx264',
                    '-preset', 'veryfast', '-pix_fmt', 'yuv420p', '-crf', '20', '-c:a', 'aac', '-b:a', '192k', '-shortest', '-movflags', '+faststart', mp4], check=True)
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', mp4, '-an', '-c:v', 'copy', str(out / f'{name}_silent.mp4')], check=True)
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', wav, '-c:a', 'libmp3lame', '-b:a', '192k', str(out / f'{name}_music.mp3')], check=True)
    return mp4


if __name__ == '__main__':
    if sys.argv[1] == 'stills':
        print('\n'.join(render(sys.argv[2], '/home/claude/reels/outT', stills=[float(x) for x in sys.argv[3].split(',')])))
    else:
        print(render(sys.argv[1]))
