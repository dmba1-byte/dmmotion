"""Pause-challenge loop reel: a floor plan rises into 3D and settles for exactly one frame.
Pause on that frame and a hidden offer shows. Near-miss frames taunt, so people replay.
Short, seamless loop — repeat watch time is the whole point."""
import sys, json, math, pathlib, subprocess
sys.path.insert(0, '/home/claude/reels')
from playwright.sync_api import sync_playwright
from gen.plans import Plan
from gen.engine2 import STYLES, prefix_ids, LOGO_D
import numpy as np, scipy.io.wavfile as wavfile

W, H, FPS = 1080, 1920, 30
DUR = 4.0
N = int(W and FPS * DUR)
WIN = 64                      # the one winning frame (of 0..N-1)
NEAR = 7                      # frames either side that get the taunt
GREEN, INK, PAPER = '#2e9b62', '#f2f2f2', '#141414'


def build_html(seed=2201, typ='courtyard', style='dark'):
    st = STYLES[style]
    p = Plan(seed, typ).build()
    svg = prefix_ids(p.svg(st['ink'], st['sub'], st['tint'], box=(70, 430, 940, 980), fills=st.get('fills')), 'p_')
    segs = p.walls(); Hh = 8.5; walls = []
    for ext, lst in segs.items():
        for o, c, a, b in lst:
            x1, y1, x2, y2 = (a, c, b, c) if o == 'h' else (c, a, c, b)
            walls.append([x1, y1, x2, y2, 0, Hh, 1 if ext else 0])
    for o, c, a, b in p.windows:
        x1, y1, x2, y2 = (a, c, b, c) if o == 'h' else (c, a, c, b)
        walls += [[x1, y1, x2, y2, 0, 3, 1], [x1, y1, x2, y2, 7, Hh, 1]]
    for o, c, a, b, *_ in p.doors:
        x1, y1, x2, y2 = (a, c, b, c) if o == 'h' else (c, a, c, b)
        walls.append([x1, y1, x2, y2, 7, Hh, 0])
    fills = st.get('fills') or {}
    rooms = [[r.x, r.y, r.w, r.h, fills.get(r.kind, st['tint'])] for r in p.rooms] + [[e[1], e[2], e[3], e[4], st['tint2']] for e in p.extras]
    PW, PD = p.W, p.D
    k = min(830 / ((PW + PD) * 0.866), 760 / ((PW + PD) * 0.5 + Hh))
    ox = 540 - (PW - PD) / 2 * k * 0.866
    oy = 1010 - (PW + PD) * k * 0.25 + Hh * k / 2
    iso = dict(walls=walls, rooms=rooms, S=p.S, X0=p.X0, Y0=p.Y0, k=k, ox=ox, oy=oy, H=Hh)
    data = dict(iso=iso, N=N, win=WIN, near=NEAR)
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>
html,body{{margin:0;width:{W}px;height:{H}px;background:{PAPER};overflow:hidden;font-family:Helvetica,Arial,sans-serif;color:{INK}}}
.t{{position:absolute;left:50px;right:50px;text-align:center}}
#hook{{top:150px;font-size:62px;font-weight:900;line-height:1.1;letter-spacing:-1px}} #hook b{{color:{GREEN}}}
#sub{{top:320px;font-size:34px;color:#9a9a9a;font-weight:600}}
#miss{{top:1480px;opacity:0}} #miss span{{display:inline-block;background:#b33;color:#fff;font-size:52px;font-weight:900;padding:14px 30px;border-radius:14px;letter-spacing:1px}}
#missb{{top:1570px;opacity:0;font-size:36px;color:#d88;font-weight:700}}
#win{{position:absolute;inset:0;opacity:0;background:rgba(10,10,10,.72)}}
#w1{{top:620px;font-size:92px;font-weight:900;color:{GREEN};letter-spacing:-2px}}
#w2{{top:760px;font-size:46px;font-weight:700;line-height:1.35;color:#fff}}
#w3{{top:1000px}} #w3 span{{display:inline-block;background:#fff;color:#141414;font-size:40px;font-weight:800;padding:22px 38px;border-radius:14px}}
#w4{{top:1180px;font-size:30px;color:#bdbdbd;line-height:1.4}}
#bar{{position:absolute;left:0;right:0;top:1380px;height:10px;background:#2a2a2a}} #bar i{{display:block;height:100%;width:0;background:{GREEN}}}
#mark{{position:absolute;top:1366px;width:5px;height:38px;background:{GREEN};box-shadow:0 0 14px {GREEN}}}
#logo{{position:absolute;left:470px;top:1700px;width:140px;opacity:.5}}
</style></head><body>
<div class="t" id="hook">Only <b>1%</b> can pause<br>on the exact frame</div>
<div class="t" id="sub">the plan is fully 3D for one frame</div>
<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" style="position:absolute;left:0;top:0">
  <g id="flat" style="opacity:1">{svg}</g><g id="iso"></g>
</svg>
<div id="bar"><i id="fill"></i></div><div id="mark"></div>
<div class="t" id="miss"><span id="misst">SOOOO CLOSE</span></div>
<div class="t" id="missb">1 frame off — swipe back and try again</div>
<svg id="logo" viewBox="-2.18 -2.45 309.7 309.7" width="140" height="140"><path d="{LOGO_D}" fill="#fff"/></svg>
<div id="win">
  <div class="t" id="w1">YOU GOT IT</div>
  <div class="t" id="w2">Screenshot this frame.<br>Email it with your floor plan and<br>your animation is <b style="color:{GREEN}">$100 off</b>.</div>
  <div class="t" id="w3"><span>dmba04@gmail.com</span></div>
  <div class="t" id="w4">DM Motion · animated plans, elevations &amp; 3D<br>Subject line: PAUSED</div>
</div>
<script>
const D={json.dumps(data)}, I=D.iso, NS='http://www.w3.org/2000/svg';
const $=i=>document.getElementById(i), lerp=(a,b,t)=>a+(b-a)*t, cl=(x,a,b)=>Math.max(a,Math.min(b,x));
const g=$('iso'), ST={json.dumps(st)};
const floors=I.rooms.map(r=>{{const q=document.createElementNS(NS,'polygon');q.setAttribute('fill',r[4]);q.setAttribute('stroke',ST.sub);q.setAttribute('stroke-width','0.8');g.appendChild(q);return{{r,q}};}});
const ws=I.walls.slice().sort((a,b)=>(a[0]+a[2]+a[1]+a[3])-(b[0]+b[2]+b[1]+b[3])).map(w=>{{const q=document.createElementNS(NS,'polygon');q.setAttribute('fill',ST.wall);q.setAttribute('stroke',ST.ink);q.setAttribute('stroke-width',w[6]?'1.6':'1.1');q.setAttribute('stroke-linejoin','round');g.appendChild(q);return{{w,q}};}});
function isoPt(x,y,z,m){{const tx=I.X0+x*I.S,ty=I.Y0+y*I.S;const ix=I.ox+(x-y)*I.k*0.866,iy=I.oy+(x+y)*I.k*0.5-z*I.k;return [lerp(tx,ix,m),lerp(ty,iy,m)];}}
const ease=t=>t<.5?2*t*t:1-Math.pow(-2*t+2,2)/2;
window.setF=f=>{{
 // ping-pong: flat -> full 3D at the win frame -> back to flat, so the clip loops seamlessly
 const u=f<=D.win? f/D.win : (D.N-f)/(D.N-D.win);
 const m=ease(cl(u,0,1)), h=ease(cl((u-0.18)/0.82,0,1))*I.H;
 $('flat').style.opacity=String(cl(1-u*2.2,0,1));
 $('iso').style.opacity=String(cl(u*3,0,1));
 floors.forEach(({{r,q}})=>{{const[x,y,w,hh]=r;q.setAttribute('points',[[x,y],[x+w,y],[x+w,y+hh],[x,y+hh]].map(z=>isoPt(z[0],z[1],0,m).join(',')).join(' '));}});
 ws.forEach(({{w,q}})=>{{const[x1,y1,x2,y2,z0,z1]=w;const za=Math.min(z0,h),zb=Math.min(z1,h);
   if(zb<=za+0.01){{q.setAttribute('points','');return;}}
   q.setAttribute('points',[isoPt(x1,y1,za,m),isoPt(x2,y2,za,m),isoPt(x2,y2,zb,m),isoPt(x1,y1,zb,m)].map(z=>z.join(',')).join(' '));}});
 const d=Math.abs(f-D.win);
 $('fill').style.width=(100*f/(D.N-1))+'%';
 $('mark').style.left=(100*D.win/(D.N-1))+'%';
 const hit=d===0;
 $('win').style.opacity=hit?'1':'0';
 const near=!hit&&d<=D.near;
 $('miss').style.opacity=near?'1':'0'; $('missb').style.opacity=near?'1':'0';
 $('misst').textContent=d<=2?'SOOOO CLOSE':(d<=4?'ALMOST':'NOT YET');
 $('missb').textContent=d+' frame'+(d===1?'':'s')+' off — try again';
 $('hook').style.opacity=hit?'0':'1'; $('sub').style.opacity=hit?'0':'1';
}};
setF(0);
</script></body></html>"""


def audio(out):
    sr = 44100; n = int(sr * DUR); t = np.arange(n) / sr; rng = np.random.default_rng(3)
    bpm = 120; beat = 60 / bpm
    x = np.zeros(n)
    # pulse that speeds toward the winning frame, so the ear expects the moment
    for k in range(int(DUR / 0.25)):
        at = k * 0.25; i = int(at * sr); d = int(sr * 0.06); tt = np.arange(d) / sr
        f = 900 + 500 * (1 - abs(at - WIN / FPS) / 2.2)
        x[i:i + d] += np.sin(2 * np.pi * f * tt) * np.exp(-tt * 70) * 0.18
    # sub pulse on the beat
    for k in range(int(DUR / beat) + 1):
        i = int(k * beat * sr); d = int(sr * 0.22); tt = np.arange(d) / sr
        if i + d < n: x[i:i + d] += np.sin(2 * np.pi * 62 * tt) * np.exp(-tt * 16) * 0.5
    # chime on the winning frame
    i = int(WIN / FPS * sr); d = int(sr * 0.7); tt = np.arange(d) / sr
    for f, a in ((880, .3), (1320, .22), (1760, .14)):
        x[i:i + d] += np.sin(2 * np.pi * f * tt) * np.exp(-tt * 5) * a
    pad = (np.sin(2 * np.pi * 220 * t) + np.sin(2 * np.pi * 330 * t) * .6) * 0.05
    x = x + pad
    x = np.clip(x / max(1e-9, np.abs(x).max()) * 0.86, -1, 1)
    st = np.stack([x, x], 1)
    wavfile.write(out, sr, (st * 32767).astype(np.int16))


def render(outdir='/home/claude/reels/out2', name='r_pause_3d', stills=None):
    out = pathlib.Path(outdir); out.mkdir(exist_ok=True)
    hp = out / f'{name}.html'; hp.write_text(build_html())
    fr = out / f'fr_{name}'; fr.mkdir(exist_ok=True)
    with sync_playwright() as pw:
        b = pw.chromium.launch(); pg = b.new_page(viewport={'width': W, 'height': H}); errs = []
        pg.on('pageerror', lambda e: errs.append(str(e))); pg.goto(hp.resolve().as_uri()); pg.wait_for_timeout(400)
        idx = stills if stills is not None else range(N)
        for f in idx:
            pg.evaluate(f'setF({f})'); pg.screenshot(path=str(fr / f'{f:04d}.png'))
        b.close()
        if errs: print('ERR', errs[:3])
    if stills is not None: return [str(fr / f'{f:04d}.png') for f in stills]
    wav = str(out / f'{name}.wav'); audio(wav)
    mp4 = str(out / f'{name}.mp4')
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-framerate', str(FPS), '-i', str(fr / '%04d.png'), '-i', wav,
                    '-c:v', 'libx264', '-preset', 'veryfast', '-pix_fmt', 'yuv420p', '-crf', '18', '-c:a', 'aac', '-b:a', '192k',
                    '-shortest', '-movflags', '+faststart', mp4], check=True)
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', mp4, '-an', '-c:v', 'copy', str(out / f'{name}_silent.mp4')], check=True)
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', wav, '-c:a', 'libmp3lame', '-b:a', '192k', str(out / f'{name}_music.mp3')], check=True)
    return mp4


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'stills':
        print('\n'.join(render('/home/claude/reels/outT', stills=[int(x) for x in sys.argv[2].split(',')])))
    else:
        print(render())
