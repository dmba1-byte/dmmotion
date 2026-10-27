"""Education reel: kitchen work triangle, WRONG vs RIGHT, with a walking path and measured distances.
Rule shown on screen (NKBA kitchen planning guideline): each leg 4'-9', total of the three legs 26' or less, no island cutting the triangle."""
import sys, json, math, pathlib, subprocess
sys.path.insert(0, '/home/claude/reels')
from playwright.sync_api import sync_playwright
from gen.engine2 import LOGO_D
from gen.draw import fmt_ft
import soundtrack

W, H, FPS = 1080, 1920, 30
INK, SUB, RED, GRN, BG, TINT = '#1f1f1f', '#8a8a8a', '#3a3a3a', '#2e9b62', '#ffffff', '#f1efe9'
S, X0, Y0 = 60, 120, 560            # px per ft, origin of room interior
RW, RD = 14, 13
ISL = (5, 6.5, 9.5, 9.0)

APP = {  # name: (w, d) footprint, drawn facing +y (front at bottom)
    'ref': (3.0, 2.6), 'sink': (3.2, 2.0), 'range': (2.6, 2.0)}
STATE = {
    'wrong': {'ref': (1.3, 11.3, -90), 'sink': (11.6, 1.0, 0), 'range': (1.0, 3.6, -90)},
    'right': {'ref': (1.3, 3.0, -90), 'sink': (7.6, 1.0, 0), 'range': (13.0, 4.6, 90)}}
STAND = {'wrong': {'ref': (3.3, 11.3), 'sink': (11.6, 2.7), 'range': (2.7, 3.6)},
         'right': {'ref': (3.3, 3.0), 'sink': (7.6, 2.7), 'range': (11.3, 4.6)}}
ROUTE = {'wrong': [STAND['wrong']['ref'], (10.6, 10.9), STAND['wrong']['sink'], STAND['wrong']['range'], STAND['wrong']['ref']],
         'right': [STAND['right']['ref'], STAND['right']['sink'], STAND['right']['range'], STAND['right']['ref']]}


def plen(pts): return sum(math.dist(pts[i], pts[i + 1]) for i in range(len(pts) - 1))
def X(f): return X0 + f * S
def Y(f): return Y0 + f * S


def room_svg():
    out = []
    ln = lambda x1, y1, x2, y2, w, c=INK: out.append(f'<line x1="{X(x1):.1f}" y1="{Y(y1):.1f}" x2="{X(x2):.1f}" y2="{Y(y2):.1f}" stroke="{c}" stroke-width="{w}" stroke-linecap="square"/>')
    t = 0.5
    # walls (outer face), door at bottom right 9.5-12.5, window on top 4.5-9.5
    ln(-t / 2, -t / 2, 4.5, -t / 2, 14); ln(9.5, -t / 2, RW + t / 2, -t / 2, 14)
    ln(-t / 2, -t / 2, -t / 2, RD + t / 2, 14); ln(RW + t / 2, -t / 2, RW + t / 2, RD + t / 2, 14)
    ln(-t / 2, RD + t / 2, 9.5, RD + t / 2, 14); ln(12.5, RD + t / 2, RW + t / 2, RD + t / 2, 14)
    win = f'<rect x="{X(4.5):.1f}" y="{Y(-t):.1f}" width="{5 * S}" height="{t * S}" fill="{BG}" stroke="{INK}" stroke-width="2"/><line x1="{X(4.5):.1f}" y1="{Y(-t / 2):.1f}" x2="{X(9.5):.1f}" y2="{Y(-t / 2):.1f}" stroke="{INK}" stroke-width="1.5"/>'
    door = f'<path d="M{X(12.5):.1f} {Y(RD):.1f} L{X(12.5):.1f} {Y(RD - 3):.1f} A{3 * S} {3 * S} 0 0 0 {X(9.5):.1f} {Y(RD):.1f}" fill="none" stroke="{INK}" stroke-width="1.6"/>'
    cnt = [f'<path d="M{X(0):.1f} {Y(2):.1f} L{X(RW):.1f} {Y(2):.1f}" stroke="{INK}" stroke-width="2.4" fill="none"/>',
           f'<path d="M{X(2):.1f} {Y(2):.1f} L{X(2):.1f} {Y(9):.1f} L{X(0):.1f} {Y(9):.1f}" stroke="{INK}" stroke-width="2.4" fill="none"/>',
           f'<path d="M{X(12):.1f} {Y(2):.1f} L{X(12):.1f} {Y(9):.1f} L{X(RW):.1f} {Y(9):.1f}" stroke="{INK}" stroke-width="2.4" fill="none"/>']
    a, b, c, d = ISL
    isl = f'<rect x="{X(a):.1f}" y="{Y(b):.1f}" width="{(c - a) * S}" height="{(d - b) * S}" fill="{TINT}" stroke="{INK}" stroke-width="2.6"/>' + \
          ''.join(f'<circle cx="{X(a + 0.9 + k * 1.35):.1f}" cy="{Y(d + 0.75):.1f}" r="{0.55 * S:.1f}" fill="none" stroke="{SUB}" stroke-width="1.6"/>' for k in range(4))
    lab = f'<text x="{X((a + c) / 2):.1f}" y="{Y((b + d) / 2) + 8:.1f}" font-size="22" font-weight="700" letter-spacing="3" text-anchor="middle" fill="{SUB}" font-family="Helvetica">ISLAND</text>'
    tint = f'<rect x="{X(0):.1f}" y="{Y(0):.1f}" width="{RW * S}" height="{RD * S}" fill="#fbfaf7"/>' + \
           f'<path d="M{X(0):.1f} {Y(0):.1f} H{X(RW):.1f} V{Y(9):.1f} H{X(12):.1f} V{Y(2):.1f} H{X(2):.1f} V{Y(9):.1f} H{X(0):.1f} Z" fill="{TINT}"/>'
    return tint, ''.join(out) + win + door, ''.join(cnt) + isl + lab


def app_svg(name):
    w, d = APP[name]; hw, hd = w / 2 * S, d / 2 * S; o = []
    o.append(f'<rect x="{-hw:.1f}" y="{-hd:.1f}" width="{2 * hw:.1f}" height="{2 * hd:.1f}" fill="#fff" stroke="{INK}" stroke-width="2.6"/>')
    if name == 'ref':
        o.append(f'<line x1="{-hw:.1f}" y1="{-hd:.1f}" x2="{hw:.1f}" y2="{hd:.1f}" stroke="{SUB}" stroke-width="1.4"/><line x1="{hw:.1f}" y1="{-hd:.1f}" x2="{-hw:.1f}" y2="{hd:.1f}" stroke="{SUB}" stroke-width="1.4"/>')
    if name == 'sink':
        for sx in (-1, 1): o.append(f'<rect x="{sx * 0.75 * S - 0.62 * S:.1f}" y="{-0.55 * S:.1f}" width="{1.24 * S:.1f}" height="{1.25 * S:.1f}" rx="10" fill="none" stroke="{INK}" stroke-width="1.8"/>')
        o.append(f'<circle cx="0" cy="{-0.75 * S:.1f}" r="5" fill="{INK}"/>')
    if name == 'range':
        for cx, cy, r in ((-0.6, -0.45, 0.42), (0.6, -0.45, 0.34), (-0.6, 0.5, 0.34), (0.6, 0.5, 0.42)):
            o.append(f'<circle cx="{cx * S:.1f}" cy="{cy * S:.1f}" r="{r * S:.1f}" fill="none" stroke="{INK}" stroke-width="1.8"/><circle cx="{cx * S:.1f}" cy="{cy * S:.1f}" r="{r * S * 0.45:.1f}" fill="none" stroke="{SUB}" stroke-width="1.2"/>')
    lab = {'ref': 'FRIDGE', 'sink': 'SINK', 'range': 'RANGE'}[name]
    o.append(f'<g class="lab"><text x="0" y="{hd + 30:.1f}" font-size="22" font-weight="800" letter-spacing="2.5" text-anchor="middle" fill="{INK}" font-family="Helvetica">{lab}</text></g>')
    return ''.join(o)


def build():
    wl, rl = plen(ROUTE['wrong']), plen(ROUTE['right'])
    legs = [math.dist(STAND['right'][a], STAND['right'][b]) for a, b in (('ref', 'sink'), ('sink', 'range'), ('range', 'ref'))]
    T = dict(draw=(0.3, 2.4), wrong=2.6, walk1=(3.0, 6.4), note1=6.5, move=(7.6, 8.8), right=8.9, walk2=(9.2, 11.4), tri=11.5, rule=12.2, end=14.6)
    dur = T['end'] + 3.6
    tint, walls, cnt = room_svg()
    st = lambda k: {n: [X(v[0]), Y(v[1]), v[2]] for n, v in STATE[k].items()}
    route = {k: [[X(a), Y(b)] for a, b in v] for k, v in ROUTE.items()}
    tri = [[X(a), Y(b)] for a, b in (STAND['right']['ref'], STAND['right']['sink'], STAND['right']['range'])]
    data = dict(T=T, st={k: st(k) for k in STATE}, route=route, wl=round(wl, 1), rl=round(rl, 1), legs=[fmt_ft(l) for l in legs], tri=tri, S=S)
    html = f"""<!doctype html><html><head><meta charset="utf-8"><style>
html,body{{margin:0;width:{W}px;height:{H}px;background:{BG};overflow:hidden;font-family:Helvetica,Arial,sans-serif;color:{INK}}}
.t{{position:absolute;left:60px;right:60px;text-align:center}}
#spec{{top:150px}} #spec span{{display:inline-block;border:2.5px solid {INK};font:700 27px Helvetica;letter-spacing:3px;padding:9px 20px;border-radius:8px}}
#hook{{top:235px;font-size:64px;font-weight:800;letter-spacing:-1px;line-height:1.1}}
.verdict{{position:absolute;left:0;right:0;top:400px;text-align:center;opacity:0}} .verdict span{{display:inline-flex;align-items:center;gap:14px;color:#fff;font:900 48px Helvetica;letter-spacing:3px;padding:12px 30px;border-radius:12px}}
#ctr{{position:absolute;left:0;right:0;top:1430px;text-align:center;font:700 34px Helvetica;letter-spacing:2px;color:{SUB}}} #ctr b{{display:block;font:900 96px Helvetica;letter-spacing:-2px;color:{INK}}}
.note{{position:absolute;left:0;right:0;text-align:center;opacity:0}} .note span{{display:inline-block;border:2.5px solid {RED};color:{RED};font:800 32px Helvetica;padding:10px 22px;border-radius:10px;background:#fff}}
#rule{{position:absolute;left:110px;right:110px;top:1630px;opacity:0;border:3px solid {INK};border-radius:16px;padding:22px 28px;background:#fff;box-shadow:8px 8px 0 {INK}}}
#rule div{{font:800 36px Helvetica;line-height:1.35}} #rule small{{display:block;font:600 24px Helvetica;color:{SUB};letter-spacing:1.5px;margin-top:8px}}
#end{{position:absolute;inset:0;background:#141414;opacity:0}}
#e1{{top:820px;font-size:70px;font-weight:700;color:#fff;letter-spacing:-1px;opacity:0}} #e2{{top:930px;font-size:38px;color:#bdbdbd;opacity:0;line-height:1.35}}
#e3{{top:1140px;opacity:0}} #e3 span{{display:inline-block;background:#fff;color:#141414;font-size:40px;font-weight:700;padding:24px 44px;border-radius:14px}}
</style></head><body>
<div class="t" id="spec"><span>THE KITCHEN WORK TRIANGLE</span></div>
<div class="t" id="hook">Your kitchen layout<br>is costing you steps</div>
<div class="verdict" id="vw"><span style="background:{RED}"><svg width="34" height="34"><path d="M6 6 L28 28 M28 6 L6 28" stroke="#fff" stroke-width="7" stroke-linecap="round"/></svg>WRONG</span></div>
<div class="verdict" id="vr"><span style="background:{GRN}"><svg width="38" height="34"><path d="M5 18 L15 28 L33 6" stroke="#fff" stroke-width="7" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>RIGHT</span></div>
<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" style="position:absolute;left:0;top:0">
 <g id="tint" opacity="0">{tint}</g><g id="walls">{walls}</g><g id="cnt">{cnt}</g>
 <path id="p1" fill="none" stroke="#6b6b6b" stroke-width="7" stroke-dasharray="2 16" stroke-linecap="round" opacity="0"/>
 <path id="p2" fill="none" stroke="{GRN}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round" opacity="0"/>
 <g id="tri" opacity="0"></g>
 {''.join(f'<g id="a_{n}" opacity="0">{app_svg(n)}</g>' for n in APP)}
 <g id="man" opacity="0"><ellipse rx="{0.95 * S:.1f}" ry="{0.45 * S:.1f}" fill="#fff" stroke="{INK}" stroke-width="3"/><circle r="{0.42 * S:.1f}" fill="{INK}"/></g>
</svg>
<div class="note" id="n1" style="top:1300px"><span>Island blocks the path</span></div>
<div class="note" id="n2" style="top:1300px"><span style="border-color:{GRN};color:{GRN}">Every leg between 4 and 9 ft</span></div>
<div id="ctr">WALKED PER LOOP<b id="ctrv">0.0 FT</b></div>
<div id="rule"><div>Each leg 4–9 ft · total under 26 ft · nothing blocking the triangle</div><small>NKBA KITCHEN PLANNING GUIDELINE</small></div>
<div id="end"></div>
<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" style="position:absolute;left:0;top:0"><g transform="translate(435 470) scale(0.68)"><svg viewBox="-2.18 -2.45 309.7 309.7" width="309.7" height="309.7" overflow="visible">
<path id="lfill" d="{LOGO_D}" fill="#fff" opacity="0"/><path id="link" d="{LOGO_D}" fill="none" stroke="#fff" stroke-width="5" stroke-linejoin="round"/></svg></g></svg>
<div class="t" id="e1">Your drawing, in motion.</div><div class="t" id="e2">Your plan, animated · from $450<br>Free 5-second logo trial</div>
<div class="t" id="e3"><span>Comment “PLAN” for pricing</span></div>
<script>
const D={json.dumps(data)}, T=D.T, E=T.end;
const $=i=>document.getElementById(i), cl=(x,a,b)=>Math.max(a,Math.min(b,x)), P=(t,a,d)=>cl((t-a)/d,0,1);
const ease=t=>t<.5?2*t*t:1-Math.pow(-2*t+2,2)/2, eo=x=>1-Math.pow(1-x,3);
const dr=[]; ['walls','cnt'].forEach((g,gi)=>[...$(g).querySelectorAll('line,path,rect,circle')].forEach((el,i,arr)=>{{ let L=0; try{{L=el.getTotalLength()}}catch(e){{}}
  el.style.strokeDasharray=L; el.style.strokeDashoffset=L; const f=el.getAttribute('fill'); if(f&&f!=='none') el.style.fillOpacity=0; dr.push({{el,L,a:T.draw[0]+(gi?0.9:0)+(i/arr.length)*(gi?0.9:0.9),f:f&&f!=='none'}}); }}));
const pd=pts=>'M'+pts.map(p=>p.join(' ')).join(' L');
$('p1').setAttribute('d',pd(D.route.wrong)); $('p2').setAttribute('d',pd(D.route.right));
const L1=$('p1').getTotalLength(), L2=$('p2').getTotalLength();
// triangle with leg labels
(()=>{{ const g=$('tri'), NS='http://www.w3.org/2000/svg', p=D.tri; const pl=document.createElementNS(NS,'path'); pl.setAttribute('d',pd(p)+' Z'); pl.setAttribute('fill','{GRN}'); pl.setAttribute('fill-opacity','0.10'); pl.setAttribute('stroke','{GRN}'); pl.setAttribute('stroke-width','3'); pl.setAttribute('stroke-dasharray','12 9'); g.appendChild(pl);
  for(let i=0;i<3;i++){{ const a=p[i], b=p[(i+1)%3]; const tx=document.createElementNS(NS,'text'); const mx=(a[0]+b[0])/2, my=(a[1]+b[1])/2; const cx=(p[0][0]+p[1][0]+p[2][0])/3, cy=(p[0][1]+p[1][1]+p[2][1])/3;
    const dx=mx-cx, dy=my-cy, dl=Math.hypot(dx,dy)||1; tx.setAttribute('x',mx+dx/dl*34); tx.setAttribute('y',my+dy/dl*34+10); tx.setAttribute('text-anchor','middle'); tx.setAttribute('font-size','30'); tx.setAttribute('font-weight','900'); tx.setAttribute('fill','{GRN}'); tx.setAttribute('font-family','Helvetica'); tx.textContent=D.legs[i];
    const bgw=document.createElementNS(NS,'rect'); bgw.setAttribute('x',mx+dx/dl*34-62); bgw.setAttribute('y',my+dy/dl*34-18); bgw.setAttribute('width',124); bgw.setAttribute('height',40); bgw.setAttribute('rx',8); bgw.setAttribute('fill','#fff'); g.appendChild(bgw); g.appendChild(tx); }} }})();
function along(path,L,u){{ const q=path.getPointAtLength(L*u), q2=path.getPointAtLength(Math.min(L,L*u+2)); return [q.x,q.y,Math.atan2(q2.y-q.y,q2.x-q.x)]; }}
window.setT=t=>{{
 dr.forEach(o=>{{ const p=P(t,o.a,0.35); o.el.style.strokeDashoffset=o.L*(1-ease(p)); if(o.f) o.el.style.fillOpacity=P(t,o.a+0.2,0.3); }});
 $('tint').setAttribute('opacity',P(t,T.draw[1]-0.4,0.6));
 const m=ease(P(t,T.move[0],T.move[1]-T.move[0]));
 ['ref','sink','range'].forEach((n,k)=>{{ const a=D.st.wrong[n], b=D.st.right[n], g=$('a_'+n); const x=a[0]+(b[0]-a[0])*m, y=a[1]+(b[1]-a[1])*m, r=a[2]+(b[2]-a[2])*m;
   const pop=P(t,T.draw[1]-0.5+k*0.15,0.35); g.setAttribute('opacity',pop); g.setAttribute('transform',`translate(${{x}} ${{y}}) rotate(${{r}}) scale(${{0.8+0.2*eo(pop)}})`);
   g.querySelector('.lab').setAttribute('transform',`rotate(${{-r}} 0 0)`); }});
 $('vw').style.opacity=P(t,T.wrong,0.25)*(1-P(t,T.move[0]-0.2,0.3)); $('vw').style.transform=`scale(${{1.3-0.3*eo(P(t,T.wrong,0.3))}})`;
 $('vr').style.opacity=P(t,T.right,0.25)*(1-P(t,E-0.3,0.3)); $('vr').style.transform=`scale(${{1.3-0.3*eo(P(t,T.right,0.3))}})`;
 // walk 1
 const u1=P(t,T.walk1[0],T.walk1[1]-T.walk1[0]), u2=P(t,T.walk2[0],T.walk2[1]-T.walk2[0]);
 $('p1').setAttribute('opacity',(t>=T.walk1[0]?1:0)*(1-P(t,T.move[0]-0.3,0.4))); $('p1').style.strokeDasharray=`2 16`; $('p1').setAttribute('stroke-dashoffset',0);
 $('p1').style.clipPath='none'; $('p1').setAttribute('d',pd(D.route.wrong));
 // reveal p1 progressively using a second dasharray trick: draw only up to u1
 const vis1=L1*u1; $('p1').style.strokeDasharray=Array.from({{length:Math.ceil(vis1/18)}},()=> '2 16').join(' ')+` 0 ${{L1+40}}`;
 $('p2').setAttribute('opacity',(t>=T.walk2[0]?1:0)*(1-P(t,E-0.3,0.3))); $('p2').style.strokeDasharray=`${{L2*u2}} ${{L2+40}}`;
 const man=$('man'); let mx,my,ma,mo;
 if(t<T.move[0]){{ [mx,my,ma]=along($('p1'),L1,ease(u1)); mo=P(t,T.walk1[0]-0.3,0.3)*(1-P(t,T.move[0]-0.3,0.3)); }}
 else {{ [mx,my,ma]=along($('p2'),L2,ease(u2)); mo=P(t,T.walk2[0]-0.3,0.3)*(1-P(t,E-0.3,0.3)); }}
 man.setAttribute('opacity',mo); man.setAttribute('transform',`translate(${{mx}} ${{my}}) rotate(${{ma*180/Math.PI+90}})`);
 // counter
 let v=0, col='{INK}'; if(t<T.move[0]){{ v=D.wl*ease(u1); col=u1>0.99?'{RED}':'{INK}'; }} else {{ v=D.rl*ease(u2); col=u2>0.99?'{GRN}':'{INK}'; }}
 $('ctrv').textContent=v.toFixed(1)+' FT'; $('ctrv').style.color=col; $('ctr').style.opacity=P(t,T.walk1[0]-0.3,0.3)*(1-P(t,E-0.3,0.3));
 $('n1').style.opacity=P(t,T.note1,0.3)*(1-P(t,T.move[0]-0.2,0.3));
 $('n2').style.opacity=P(t,T.tri+0.2,0.3)*(1-P(t,E-0.3,0.3));
 $('tri').setAttribute('opacity',P(t,T.tri,0.5)*(1-P(t,E-0.3,0.3)));
 const rp=P(t,T.rule,0.4); $('rule').style.opacity=rp*(1-P(t,E-0.3,0.3)); $('rule').style.transform=`translateY(${{40*(1-eo(rp))}}px)`;
 const ho=1-P(t,E-0.4,0.4); $('hook').style.opacity=ho; $('spec').style.opacity=ho;
 $('end').style.opacity=P(t,E,0.6);
 const lp=P(t,E+0.15,1.3), lk=$('link'), LL=lk.getTotalLength(); lk.style.strokeDasharray=LL; lk.style.strokeDashoffset=LL*(1-ease(cl(lp/.8,0,1)));
 $('lfill').style.opacity=cl((lp-.7)/.3,0,1); lk.style.opacity=1-cl((lp-.85)/.15,0,1);
 $('e1').style.opacity=P(t,E+0.9,0.4); $('e2').style.opacity=P(t,E+1.25,0.4); $('e3').style.opacity=P(t,E+1.6,0.4);
}}; setT(0);
</script></body></html>"""
    return html, data


def render(outdir='/home/claude/reels/out2', name='r_edu_kitchen', stills=None):
    out = pathlib.Path(outdir); out.mkdir(exist_ok=True); html, data = build(); hp = out / f'{name}.html'; hp.write_text(html)
    fr = out / f'fr_{name}'; fr.mkdir(exist_ok=True); dur = data['T']['end'] + 3.6; N = int(FPS * dur)
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': W, 'height': H}); errs = []
        pg.on('pageerror', lambda e: errs.append(str(e))); pg.goto(hp.resolve().as_uri()); pg.wait_for_timeout(300)
        ts = stills or [i / FPS for i in range(N)]
        for i, t in enumerate(ts):
            pg.evaluate(f'setT({t})'); pg.screenshot(path=str(fr / (f's_{t:05.2f}.png' if stills else f'{i:04d}.png')))
        b.close()
        if errs: print('ERR', errs[:3])
    if stills: return [str(fr / f's_{t:05.2f}.png') for t in stills], data
    wav = str(out / f'{name}.wav'); soundtrack.make(dur, draw=(0.3, 2.4), end=data['T']['end'], mood='bright', bpm=104, seed=91, out=wav, pen=True, beat=True)
    mp4 = str(out / f'{name}.mp4')
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-framerate', str(FPS), '-i', str(fr / '%04d.png'), '-i', wav, '-c:v', 'libx264', '-preset', 'veryfast', '-pix_fmt', 'yuv420p', '-crf', '20',
                    '-c:a', 'aac', '-b:a', '192k', '-shortest', '-movflags', '+faststart', mp4], check=True)
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', mp4, '-an', '-c:v', 'copy', str(out / f'{name}_silent.mp4')], check=True)
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', wav, '-c:a', 'libmp3lame', '-b:a', '192k', str(out / f'{name}_music.mp3')], check=True)
    return mp4, data


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'stills':
        paths, d = render('/home/claude/reels/outT', stills=[float(x) for x in sys.argv[2].split(',')])
        print(d['wl'], d['rl'], d['legs']); print('\n'.join(paths))
    else:
        print(render())
