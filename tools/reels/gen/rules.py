"""WRONG vs RIGHT clearance reels — the format that dominates this niche.

Each reel: a top-down room, one thing in the wrong place with a red dimension,
then it slides to the correct place and the dimension turns green. Every number
comes from a published standard, named on screen.
"""
import sys, json, math, pathlib, subprocess
sys.path.insert(0, '/home/claude/reels')
from playwright.sync_api import sync_playwright
from gen.engine2 import LOGO_D
import soundtrack

W, H, FPS = 1080, 1920, 30
INK, SUB, RED, GRN, BG, TINT, TINT2 = '#1f1f1f', '#8a8a8a', '#c0392b', '#2e9b62', '#ffffff', '#f1efe9', '#e4e1d9'


def inches(v):
    ft, i = int(v // 12), int(round(v % 12))
    if i == 12: ft, i = ft + 1, 0
    return f'{ft}\'-{i}"' if ft else f'{i}"'


TOPICS = {
 'island': dict(
    topic='KITCHEN ISLAND AISLE', hook='Your island is<br>too close', sub='the aisle rule most kitchens break',
    room=(16, 13), wrong=30, right=42, door_d=2.0, door_label='DISHWASHER',
    fixed=[(0, 0, 16, 2, 'COUNTER', 'counter'), (0, 2, 2, 7, '', 'counter'), (14, 2, 2, 7, '', 'counter')],
    mov=dict(w=8, d=3.5, label='ISLAND', axis='y', base=2.0),
    rule='42" minimum aisle for one cook<br>48" when two people cook', source='NKBA KITCHEN PLANNING GUIDELINES', verdict='NKBA',
    note='Under 42" and two people can\'t pass while a dishwasher or oven door is open.'),
 'fridge': dict(
    topic='FRIDGE DOOR SWING', hook='Your fridge<br>can\'t open', sub='the clearance people forget',
    room=(16, 13), wrong=30, right=42, door_d=2.3, door_label='FRIDGE DOOR',
    fixed=[(0, 0, 16, 2, 'COUNTER', 'counter'), (0, 2, 2, 7, '', 'counter'), (14, 2, 2, 7, '', 'counter')],
    mov=dict(w=8, d=3.5, label='ISLAND', axis='y', base=2.0),
    rule='42" minimum aisle for one cook<br>48" when two people cook', source='NKBA KITCHEN PLANNING GUIDELINES', verdict='NKBA',
    note='A fridge or dishwasher door eats 24-28" of the aisle before anyone stands in it.'),
 'toilet': dict(
    topic='TOILET CLEARANCE', hook='Your toilet has<br>no room in front', sub='the bathroom number people guess at',
    room=(9, 8), wrong=21, right=30,
    fixed=[(0, 0, 9, 1.6, '', 'counter'), (3.1, 0.4, 1.6, 2.1, 'WC', 'counter')],
    mov=dict(w=6.5, d=1.9, label='VANITY', axis='y', base=2.5),
    rule='30" clear in front of the toilet<br>code allows a reduction to 21"', source='NKBA BATHROOM PLANNING GUIDELINES', verdict='NKBA',
    note='21" is the legal floor, not the comfortable one. At 21" your knees are in the vanity.'),
 'hallway': dict(
    topic='HALLWAY WIDTH', hook='Two people can\'t<br>pass in this hall', sub='the number code sets, and the one that works',
    room=(13, 11), wrong=30, right=42, verdict='IRC',
    fixed=[(0, 0, 13, 2.4, 'BEDROOM', 'counter')],
    mov=dict(w=13, d=2.4, label='BEDROOM', axis='y', base=2.4),
    rule='36" is the code minimum for a hallway<br>42" is the width that actually works',
    source='IRC R311.6', note='At 36" two people turn sideways. At 42" they don\'t.'),
 'vanity': dict(
    topic='IN FRONT OF THE SINK', hook='You can\'t stand<br>at this sink', sub='the clearance a small bath always loses',
    room=(10, 9), wrong=21, right=30, verdict='NKBA',
    fixed=[(0, 0, 10, 2.0, 'VANITY', 'counter')],
    mov=dict(w=7, d=2.6, label='TUB', axis='y', base=2.0),
    rule='30" of clear floor in front of a sink<br>measured from the front edge of the bowl',
    source='NKBA BATHROOM PLANNING GUIDELINES',
    note='Lean over a sink to wash your face and you need every inch of it.'),
 'shower': dict(
    topic='IN FRONT OF THE SHOWER', hook='Nowhere to dry<br>off in this bath', sub='the gap people find out about too late',
    room=(11, 10), wrong=20, right=30, verdict='NKBA',
    fixed=[(0, 0, 11, 2.8, 'SHOWER', 'counter')],
    mov=dict(w=8, d=2.0, label='VANITY', axis='y', base=2.8),
    rule='30" of clear floor in front of a shower or tub<br>same figure as in front of a sink',
    source='NKBA BATHROOM PLANNING GUIDELINES',
    note='You step out, you turn, you reach for a towel. That takes 30 inches.'),
 'dining': dict(
    topic='DINING TABLE CLEARANCE', hook='Nobody can get<br>out of this chair', sub='the gap every dining room gets wrong',
    room=(14, 12), wrong=24, right=36,
    fixed=[(0, 0, 14, 1.5, '', 'counter'), (0, 1.5, 1.4, 5, '', 'counter')],
    mov=dict(w=6, d=3.2, label='TABLE', axis='y', base=1.5),
    rule='36" from table edge to wall to pass a chair<br>44" to walk behind someone seated', source='KITCHEN &amp; BATH PLANNING STANDARDS', verdict='CLEARS',
    note='A dining chair pulls out 24" on its own. Anything less and the chair hits the wall.'),
}


def build(spec):
    RW, RD = spec['room']
    S = min(960 / RW, 700 / RD)
    X0 = 540 - RW * S / 2
    Y0 = 560
    X = lambda f: X0 + f * S
    Y = lambda f: Y0 + f * S
    T = dict(draw=(-0.4, 0.1), place=-0.35, wrong=-0.2, person=0.65, move=(2.5, 3.5),
             right=3.6, ok=3.8, rule=4.5, end=7.6)
    dur = T['end'] + 0.4
    mv = spec['mov']
    VERDICT = spec.get('verdict', 'CLEARS')
    gap_w, gap_r = spec['wrong'] / 12, spec['right'] / 12   # feet
    out = []
    ln = lambda x1, y1, x2, y2, w, c=INK: out.append(f'<line x1="{X(x1):.1f}" y1="{Y(y1):.1f}" x2="{X(x2):.1f}" y2="{Y(y2):.1f}" stroke="{c}" stroke-width="{w}" stroke-linecap="square"/>')
    # room walls
    for a, b, c, d in ((0, 0, RW, 0), (0, RD, RW, RD), (0, 0, 0, RD), (RW, 0, RW, RD)): ln(a, b, c, d, 13)
    fixed = []
    for fx, fy, fw, fh, lab, kind in spec['fixed']:
        fixed.append(f'<rect x="{X(fx):.1f}" y="{Y(fy):.1f}" width="{fw * S:.1f}" height="{fh * S:.1f}" fill="{TINT}" stroke="{INK}" stroke-width="2.6"/>')
        if lab: fixed.append(f'<text x="{X(fx + fw / 2):.1f}" y="{Y(fy + fh / 2) + 8:.1f}" font-size="22" font-weight="700" letter-spacing="3" text-anchor="middle" fill="{SUB}" font-family="Helvetica">{lab}</text>')
    # movable object: wrong and right positions along y (distance from the fixed counter at y=base)
    base = mv['base']
    yw, yr = base + gap_w, base + gap_r
    mx = (RW - mv['w']) / 2
    stair = mv.get('stair')
    data = dict(T=T, S=S, X0=X0, Y0=Y0, RW=RW, RD=RD, mw=mv['w'], md=mv['d'], mx=mx, yw=yw, yr=yr,
                gw=gap_w, gr=gap_r, base=base, label=mv['label'], stair=bool(stair),
                wrong_t=inches(spec['wrong']), right_t=inches(spec['right']),
                door_w=2.0, door_d=spec.get('door_d', 0.0), door_label=spec.get('door_label', ''),
                # the person reads green once the usable space left is enough to stand in.
                # with an appliance door open that is a body's width; without one it is the
                # standard itself, so the figure turns green exactly at the correct clearance.
                fit_min=spec.get('fit_min', 1.4 if spec.get('door_d') else spec['right'] / 12 - 0.01))
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>
html,body{{margin:0;width:{W}px;height:{H}px;background:{BG};overflow:hidden;font-family:Helvetica,Arial,sans-serif;color:{INK}}}
.t{{position:absolute;left:55px;right:55px;text-align:center}}
#spec{{top:140px}} #spec span{{display:inline-block;border:2.5px solid {INK};font:700 26px Helvetica;letter-spacing:3px;padding:9px 20px;border-radius:8px}}
#hook{{top:225px;font-size:64px;font-weight:800;line-height:1.08;letter-spacing:-1px}}
#sub{{top:390px;font-size:32px;color:{SUB};font-weight:600}}
.verdict{{position:absolute;left:0;right:0;top:470px;text-align:center;opacity:0}}
.verdict span{{display:inline-flex;align-items:center;gap:14px;color:#fff;font:900 46px Helvetica;letter-spacing:3px;padding:12px 30px;border-radius:12px}}
#note{{position:absolute;left:70px;right:70px;top:1330px;text-align:center;opacity:0;font:600 32px Helvetica;color:{RED};line-height:1.3}}
#rule{{position:absolute;left:95px;right:95px;top:1430px;opacity:0;border:3px solid {INK};border-radius:16px;padding:24px 28px;background:#fff;box-shadow:9px 9px 0 {INK};text-align:center}}
#rule div{{font:800 36px Helvetica;line-height:1.35}} #rule small{{display:block;font:600 22px Helvetica;color:{SUB};letter-spacing:1.5px;margin-top:10px}}
#end{{position:absolute;inset:0;background:#141414;opacity:0}}
#e1{{top:820px;font-size:70px;font-weight:700;color:#fff;letter-spacing:-1px;opacity:0}} #e2{{top:930px;font-size:38px;color:#bdbdbd;opacity:0;line-height:1.35}}
#e3{{top:1140px;opacity:0}} #e3 span{{display:inline-block;background:#fff;color:#141414;font-size:40px;font-weight:700;padding:24px 44px;border-radius:14px}}
</style></head><body>
<div class="t" id="spec"><span>{spec['topic']}</span></div>
<div class="t" id="hook">{spec['hook']}</div>
<div class="t" id="sub">{spec['sub']}</div>
<div class="verdict" id="vw"><span style="background:{RED}"><svg width="32" height="32"><path d="M6 6 L26 26 M26 6 L6 26" stroke="#fff" stroke-width="7" stroke-linecap="round"/></svg>TOO TIGHT</span></div>
<div class="verdict" id="vr"><span style="background:{GRN}"><svg width="36" height="32"><path d="M5 17 L14 26 L31 6" stroke="#fff" stroke-width="7" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>{VERDICT}</span></div>
<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" style="position:absolute;left:0;top:0"><g id="cam" style="transform-origin:540px 760px">
 <g id="walls">{''.join(out)}</g>
 <g id="fixed" opacity="0">{''.join(fixed)}</g>
 <g id="mov" opacity="0"></g>
 <g id="dim" opacity="0"></g>
 <g id="per" opacity="0"></g>
</svg>
<div id="note"></div>
<div id="rule"><div>{spec['rule']}</div><small>{spec['source']}</small></div>
<div id="end"></div>
<div class="t" id="send" style="top:1700px;opacity:0"><span style="display:inline-block;background:{INK};color:#fff;font:800 34px Helvetica;letter-spacing:-0.5px;padding:18px 30px;border-radius:14px">Send this to whoever drew it</span></div>
<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" style="position:absolute;left:0;top:0"><g transform="translate(435 470) scale(0.68)"><svg viewBox="-2.18 -2.45 309.7 309.7" width="309.7" height="309.7" overflow="visible">
<path id="lfill" d="{LOGO_D}" fill="#fff" opacity="0"/><path id="link" d="{LOGO_D}" fill="none" stroke="#fff" stroke-width="5" stroke-linejoin="round"/></svg></g></svg>
<div class="t" id="e1">Your drawing, in motion.</div><div class="t" id="e2">Your plan, animated · from $450<br>Free 5-second logo trial</div>
<div class="t" id="e3"><span>Pricing: dmba04@gmail.com</span></div>
<script>
const D={json.dumps(data)}, T=D.T, E=T.end, NS='http://www.w3.org/2000/svg';
const $=i=>document.getElementById(i), cl=(x,a,b)=>Math.max(a,Math.min(b,x)), P=(t,a,d)=>cl((t-a)/d,0,1);
const ease=t=>t<.5?2*t*t:1-Math.pow(-2*t+2,2)/2, eo=x=>1-Math.pow(1-x,3);
const X=f=>D.X0+f*D.S, Y=f=>D.Y0+f*D.S, S=D.S;
const NOTE={json.dumps(spec['note'])};
// walls draw on
const wl=[...$('walls').querySelectorAll('line')].map(el=>{{const L=el.getTotalLength();el.style.strokeDasharray=L;el.style.strokeDashoffset=L;return{{el,L}};}});
const fx=[...$('fixed').children];fx.forEach(e=>e.style.opacity=0);$('fixed').setAttribute('opacity','1');
// movable
const g=$('mov');
const box=document.createElementNS(NS,'rect');box.setAttribute('fill','{TINT2}');box.setAttribute('stroke','{INK}');box.setAttribute('stroke-width','3');g.appendChild(box);
const lab=document.createElementNS(NS,'text');lab.setAttribute('font-size','24');lab.setAttribute('font-weight','800');lab.setAttribute('letter-spacing','3');lab.setAttribute('text-anchor','middle');lab.setAttribute('fill','{SUB}');lab.setAttribute('font-family','Helvetica');lab.textContent=D.label;g.appendChild(lab);
const treads=[];
if(D.stair){{ for(let i=1;i<9;i++){{const l=document.createElementNS(NS,'line');l.setAttribute('stroke','{SUB}');l.setAttribute('stroke-width','2');g.appendChild(l);treads.push(l);}} }}
// dimension group
const dg=$('dim');
const dl=document.createElementNS(NS,'line'),t1=document.createElementNS(NS,'line'),t2=document.createElementNS(NS,'line');
[dl,t1,t2].forEach(e=>{{e.setAttribute('stroke-width','3');dg.appendChild(e);}});
const dt=document.createElementNS(NS,'text');dt.setAttribute('font-size','40');dt.setAttribute('font-weight','900');dt.setAttribute('text-anchor','middle');dt.setAttribute('font-family','Helvetica');dg.appendChild(dt);
const dbg=document.createElementNS(NS,'rect');dbg.setAttribute('fill','#fff');dg.insertBefore(dbg,dt);
// person in the gap
const pg=$('per');
const door=document.createElementNS(NS,'rect');door.setAttribute('fill','#fff');door.setAttribute('stroke','{INK}');door.setAttribute('stroke-width','2.6');pg.appendChild(door);
const dlab=document.createElementNS(NS,'text');dlab.setAttribute('font-size','19');dlab.setAttribute('font-weight','700');dlab.setAttribute('text-anchor','middle');dlab.setAttribute('fill','{SUB}');dlab.setAttribute('font-family','Helvetica');dlab.textContent=D.door_label;pg.appendChild(dlab);
const sh=document.createElementNS(NS,'ellipse');sh.setAttribute('stroke-width','3');pg.appendChild(sh);
const hd=document.createElementNS(NS,'circle');pg.appendChild(hd);
window.setT=t=>{{
 wl.forEach((o,i)=>{{const a=T.draw[0]+i*0.018,p=P(t,a,0.22);o.el.style.strokeDashoffset=o.L*(1-ease(p));}});
 fx.forEach((e,i)=>e.style.opacity=P(t,T.place+i*0.05,0.18));
 const m=ease(P(t,T.move[0],T.move[1]-T.move[0]));
 const gap=D.gw+(D.gr-D.gw)*m, y=D.base+gap;
 $('mov').setAttribute('opacity',P(t,T.place+0.08,0.18));
 box.setAttribute('x',X(D.mx));box.setAttribute('y',Y(y));box.setAttribute('width',D.mw*S);box.setAttribute('height',D.md*S);
 lab.setAttribute('x',X(D.mx+D.mw/2));lab.setAttribute('y',Y(y+D.md/2)+8);
 treads.forEach((l,i)=>{{const yy=y+D.md*(i+1)/9;l.setAttribute('x1',X(D.mx));l.setAttribute('y1',Y(yy));l.setAttribute('x2',X(D.mx+D.mw));l.setAttribute('y2',Y(yy));}});
 // dimension between fixed edge (base) and object
 const col=m>0.98?'{GRN}':(m>0.02?'{INK}':'{RED}');
 const cx=X(D.mx+D.mw*0.18), ya=Y(D.base), yb=Y(y);
 [dl,t1,t2].forEach(e=>e.setAttribute('stroke',col));
 dl.setAttribute('x1',cx);dl.setAttribute('y1',ya);dl.setAttribute('x2',cx);dl.setAttribute('y2',yb);
 t1.setAttribute('x1',cx-26);t1.setAttribute('y1',ya);t1.setAttribute('x2',cx+26);t1.setAttribute('y2',ya);
 t2.setAttribute('x1',cx-26);t2.setAttribute('y1',yb);t2.setAttribute('x2',cx+26);t2.setAttribute('y2',yb);
 const inch=Math.round(gap*12); dt.textContent=inch+'"';
 dt.setAttribute('fill',col);dt.setAttribute('x',cx-90);dt.setAttribute('y',(ya+yb)/2+14);
 dbg.setAttribute('x',cx-90-58);dbg.setAttribute('y',(ya+yb)/2-22);dbg.setAttribute('width',116);dbg.setAttribute('height',46);dbg.setAttribute('rx',8);
 dg.setAttribute('opacity',P(t,T.wrong,0.18)*(1-P(t,E-0.3,0.3)));
 // open appliance door + a person standing in what's left of the aisle
 const dOpen=P(t,T.person,0.5)*D.door_d;
 door.setAttribute('x',X(D.mx+D.mw*0.56));door.setAttribute('y',Y(D.base));
 door.setAttribute('width',D.door_d?D.door_w*S:0);door.setAttribute('height',D.door_d?Math.max(1,dOpen*S):0);
 dlab.setAttribute('x',X(D.mx+D.mw*0.56+D.door_w/2));dlab.setAttribute('y',Y(D.base+dOpen/2)+7);
 dlab.setAttribute('opacity',dOpen>D.door_d*0.7?1:0);
 const left=gap-D.door_d, fits=left>=D.fit_min;
 const pcx=X(D.mx+D.mw*0.56+D.door_w/2), pcy=Y(D.base+D.door_d+Math.max(0.35,left/2));
 sh.setAttribute('cx',pcx);sh.setAttribute('cy',pcy);sh.setAttribute('rx',0.83*S);sh.setAttribute('ry',0.5*S);
 sh.setAttribute('fill','#fff');sh.setAttribute('stroke',fits?'{GRN}':'{RED}');
 hd.setAttribute('cx',pcx);hd.setAttribute('cy',pcy);hd.setAttribute('r',0.42*S);hd.setAttribute('fill',fits?'{GRN}':'{RED}');
 pg.setAttribute('opacity',P(t,T.person,0.35)*(1-P(t,E-0.3,0.3)));
 $('vw').style.opacity=P(t,T.wrong,0.25)*(1-P(t,T.move[0]-0.2,0.3));
 $('vw').style.transform=`scale(${{1.25-0.25*eo(P(t,T.wrong,0.3))}})`;
 $('vr').style.opacity=P(t,T.ok,0.25)*(1-P(t,E-0.3,0.3));
 $('vr').style.transform=`scale(${{1.25-0.25*eo(P(t,T.ok,0.3))}})`;
 const nv=P(t,T.person+0.5,0.3)*(1-P(t,T.move[0]-0.2,0.3));
 $('note').style.opacity=nv; $('note').textContent=NOTE;
 $('send').style.opacity=P(t,T.rule+1.0,0.3)*(1-P(t,E-0.15,0.2));
 // camera: a slow push through the problem, a punch on the fix, then settle
 {{ const push = 1 + 0.055*ease(P(t,0.1,3.6));
    const punch = 0.045*(1-Math.min(1,Math.max(0,(t-T.right)/0.55)))*(t>=T.right?1:0);
    const c=$('cam'); if(c) c.style.transform=`scale(${{push+punch}})`; }}
 // hook words snap in one after another instead of the block fading
 {{ const hk=$('hook'); if(hk&&!hk.dataset.split){{ hk.dataset.split='1';
      hk.innerHTML=hk.innerHTML.split('<br>').map(line=>line.split(' ').map((w,i)=>
        `<span class="wd" style="display:inline-block">${{w}}</span>`).join(' ')).join('<br>'); }}
    [...document.querySelectorAll('#hook .wd')].forEach((w,i)=>{{
      const p=P(t,0.12+i*0.055,0.26), e=ease(p);
      w.style.opacity=p; w.style.transform=`translateY(${{(1-e)*26}}px)`; }}); }}

 const rp=P(t,T.rule,0.4); $('rule').style.opacity=rp*(1-P(t,E-0.3,0.3)); $('rule').style.transform=`translateY(${{40*(1-eo(rp))}}px)`;
 const ho=1-P(t,E-0.4,0.4); $('hook').style.opacity=ho; $('spec').style.opacity=ho; $('sub').style.opacity=ho*(1-P(t,T.wrong-0.2,0.3));
 $('end').style.opacity=P(t,E,0.6);
 const lp=P(t,E+0.15,1.3), lk=$('link'), LL=lk.getTotalLength(); lk.style.strokeDasharray=LL; lk.style.strokeDashoffset=LL*(1-ease(cl(lp/.8,0,1)));
 $('lfill').style.opacity=cl((lp-.7)/.3,0,1); lk.style.opacity=1-cl((lp-.85)/.15,0,1);
 $('e1').style.opacity=P(t,E+0.9,0.4); $('e2').style.opacity=P(t,E+1.25,0.4); $('e3').style.opacity=P(t,E+1.6,0.4);
}}; setT(0);
</script></body></html>""", dur, T


def render(key, outdir='/home/claude/reels/out2', stills=None):
    spec = TOPICS[key]; name = f'r_rule_{key}'
    out = pathlib.Path(outdir); out.mkdir(exist_ok=True)
    html, dur, T = build(spec); hp = out / f'{name}.html'; hp.write_text(html)
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
    soundtrack.make(dur, draw=(0.2, 2.2), end=T['end'], mood='bright', bpm=100, seed=hash(key) % 999, out=wav, pen=True, beat=True)
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
