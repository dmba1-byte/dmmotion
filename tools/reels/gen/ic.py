"""Icon-man reel: '5 ADA numbers to check before you send a plan'. Diagrams on top, an icon-man host below, word captions.
python3 gen/ic.py            -> out2/r_ic_walk.mp4
python3 gen/ic.py stills t1,t2
python3 gen/ic.py sheet      -> out2/ada5_sheet.png / .pdf  (the free cheat sheet, drawn from the same diagrams)"""
import json, sys, pathlib, subprocess, zlib
import numpy as np
sys.path.insert(0, '/home/claude/reels'); sys.path.insert(0, '/home/claude/reels/gen')
from playwright.sync_api import sync_playwright
import soundtrack, sfx
import vo as VOICE

W, H, FPS = 1080, 1920, 30
ROOT = pathlib.Path('/home/claude/reels')
DIAG = (ROOT / 'gen' / 'ic_diagrams.js').read_text()

import os
EP = json.load(open(os.environ['EP'])) if os.environ.get('EP') else None
SCRIPT = [
    "Five numbers every architecture student should know before sending a plan. Miss one, and your plan can fail review.",
    "One. Reach range. Switches and outlets must sit between fifteen and forty-eight inches high.",
    "Two. Clear floor space. Every fixture needs thirty by forty-eight inches to park a wheelchair.",
    "Three. Turning space. A sixty inch circle lets a wheelchair turn all the way around.",
    "Four. Sink height. The rim or counter can be no higher than thirty-four inches.",
    "Five. Door width. Open it ninety degrees, and you still need thirty-two inches of clear width.",
    "Comment REACH, and I'll send you the free one page cheat sheet with all five.",
]
if EP: SCRIPT = EP['script']
NSEG = len(SCRIPT) - 2


def lines_timing(starts, total):
    en = [starts[i + 1] - 0.22 for i in range(len(starts) - 1)] + [total]
    return list(starts), en


def amp_env(audio, n):
    SR = VOICE.SR; out = []
    for f in range(n):
        c = int(f / FPS * SR); a = audio[max(0, c - 800):c + 800]
        out.append(float(np.sqrt(np.mean(a.astype(float) ** 2))) if len(a) else 0.0)
    out = np.array(out); m = np.percentile(out, 95) or 1.0
    out = np.clip(out / m, 0, 1)
    k = np.array([.2, .6, .2]); return np.convolve(out, k, mode='same').round(3).tolist()


def build(starts, total, audio):
    st, en = lines_timing(starts, total); dur = total + 0.6; n = int(FPS * dur) + 2
    data = dict(st=st, en=en, dur=dur, amp=amp_env(audio, n), lines=SCRIPT, ep=EP)
    return HTML.replace('__DATA__', json.dumps(data)).replace('__DIAG__', DIAG), dur, dict(st=st, en=en)


HOST = r"""
<div style="position:absolute;left:140px;width:800px;bottom:14px;height:3px;background:#161616"></div>
<div style="position:absolute;left:420px;width:240px;bottom:6px;height:16px;border-radius:50%;background:#161616;opacity:.12"></div>
<img id="wA" src="__WA__" style="position:absolute;bottom:17px;opacity:0"><img id="wB" src="__WB__" style="position:absolute;bottom:17px;opacity:0"><img id="figP" src="__FIGPT__" style="position:absolute;bottom:17px;opacity:0">"""

HTML = r"""<!doctype html><html><head><meta charset="utf-8"><style>
html,body{margin:0;width:1080px;height:1920px;background:#f6f4ee;overflow:hidden;font-family:Helvetica,Arial,sans-serif}
#tag{position:absolute;top:44px;left:0;width:1080px;text-align:center}
#tag span{display:inline-block;font:800 26px Helvetica;letter-spacing:3px;padding:8px 19px;border-radius:8px;background:#fff;border:2px solid #161616}
#card{position:absolute;left:50px;top:110px;width:980px;height:870px;background:#fcfbf8;border:5px solid #161616;border-radius:22px;box-shadow:10px 10px 0 #161616;overflow:hidden}
#hd{position:absolute;left:0;top:0;width:980px;height:104px;border-bottom:5px solid #161616;display:flex;align-items:center;gap:22px;padding:0 30px;box-sizing:border-box}
#cnt{font:900 78px Helvetica;color:#1f9d63;letter-spacing:-2px;min-width:140px}
#nm{font:900 50px Helvetica;color:#161616;letter-spacing:-1px}
#rule{position:absolute;left:0;top:112px;width:980px;text-align:center;font:800 34px Helvetica;color:#1f6d45}
#dg{position:absolute;left:10px;top:162px;width:960px;height:640px}
#src{position:absolute;left:0;top:812px;width:980px;text-align:center;font:800 22px Helvetica;letter-spacing:3px;color:#8d8777}
#hook{position:absolute;left:0;top:104px;width:980px;height:766px}
#hook .t{position:absolute;left:0;width:980px;top:0;text-align:center;font:900 96px/1 Helvetica;letter-spacing:-3px;color:#161616;margin-top:18px}
.th{position:absolute;width:290px;height:194px;border:4px solid #161616;border-radius:12px;background:#fff;opacity:0;overflow:hidden}
.th svg{width:290px;height:194px}
#cta{position:absolute;left:0;top:104px;width:980px;height:766px;opacity:0}
#cta img{position:absolute;left:215px;top:12px;width:550px;height:711px;border:4px solid #161616;box-shadow:8px 8px 0 #161616;object-fit:cover;background:#fff}
#cm{position:absolute;left:0;width:1080px;top:560px;text-align:center;font:900 150px/.9 Helvetica;letter-spacing:-5px;color:#161616;opacity:0;text-shadow:0 0 14px #f6f4ee,0 0 6px #f6f4ee}
#cm small{display:block;font:900 70px Helvetica;letter-spacing:0;color:#161616}
#cm b{color:#1f9d63}
#cap{position:absolute;left:30px;top:1010px;width:1020px;text-align:center;font:900 76px/1.05 Helvetica;letter-spacing:-2px;color:#161616;height:160px}
#cap .w{display:inline-block;margin:0 9px;opacity:.28}
#cap .w.on{opacity:1;color:#1f9d63;transform:scale(1.08)}
#cap .w.done{opacity:1}
#ser{position:absolute;bottom:20px;left:0;width:1080px;text-align:center;font:800 20px Helvetica;letter-spacing:4px;color:#bbb5a4}
#flash{position:absolute;inset:0;background:#1f9d63;opacity:0}
</style></head><body>
<div id="tag"><span id="tagt">ADA IN 5 NUMBERS</span></div>
<div id="card">
 <div id="hd"><div id="cnt"></div><div id="nm"></div></div>
 <div id="rule"></div><svg id="dg" viewBox="0 0 960 640"></svg><div id="src"></div>
 <div id="hook"><div class="t">5 numbers<br>to check</div></div>
 <div id="cta"><img id="sheet" src="__SHEET__"></div>
</div>
<div id="cm"><small>Comment</small><b>REACH</b></div>
<div id="cap"></div>
__HOST__
<div id="flash"></div>
<script>
__DIAG__
const D=__DATA__, NSEG=D.lines.length-2, CT=NSEG+1, $=id=>document.getElementById(id); const ST=D.st, EN=D.en;
// word chunks per line, timed by letter count across the spoken span
const CH=D.lines.map((txt,i)=>{const ws=txt.split(/\s+/); const wt=ws.map(w=>w.length+2.5), tot=wt.reduce((a,b)=>a+b,0); let t=ST[i]; const span=EN[i]-ST[i]; const out=[]; ws.forEach((w,k)=>{const d=span*wt[k]/tot; out.push({w,a:t,b:t+d}); t+=d;});
  const chunks=[]; let cur=[]; out.forEach(o=>{cur.push(o); if(cur.length>=3||/[.,]$/.test(o.w)){chunks.push(cur);cur=[];}}); if(cur.length)chunks.push(cur); return chunks;}).flat();
// hook thumbnails
const hook=$('hook'); const TH=[]; const pos=[[30,130],[345,130],[660,130],[190,350],[500,350]];
SCENES.forEach((f,i)=>{const d=document.createElement('div'); d.className='th'; d.style.left=pos[i][0]+'px'; d.style.top=(pos[i][1]+170)+'px'; d.innerHTML='<svg viewBox="0 0 960 640">'+f(1)+'</svg>'; hook.appendChild(d); TH.push(d);});

function setT(t){
  const f=Math.min(D.amp.length-1,Math.floor(t*30)), A=D.amp[f]||0;
  // which segment
  let k=-1; for(let i=0;i<ST.length;i++){ if(t>=ST[i]-0.08) k=i; }
  const sc=k>=1&&k<=NSEG?(D.ep?D.ep.scene:k-1):-1;
  const enter=(i)=>ss(P(t,ST[i]-0.08,0.32));
  $('hd').style.opacity=1;
  if(D.ep&&(k===0||k<0)){ const m=META[D.ep.scene]; hook.style.display='none'; $('cta').style.opacity=0; $('cnt').textContent=D.ep.big; $('nm').textContent=m.n; $('rule').textContent=D.ep.hookRule; $('rule').style.opacity=1; $('src').textContent=m.s.toUpperCase(); $('dg').innerHTML=SCENES[D.ep.scene](.3+.2*P(t,0,3)); $('dg').style.opacity=1; $('dg').style.transform='none'; }
  else if(k===0||k<0){ $('cnt').textContent=''; $('nm').textContent='ADA CHEAT SHEET'; $('rule').textContent=''; $('src').textContent=''; $('dg').innerHTML=''; hook.style.display='block'; $('cta').style.opacity=0; }
  else if(sc>=0){ hook.style.display='none'; $('cta').style.opacity=0; const e=enter(k), p=P(t,ST[k]+.1,(EN[k]-ST[k])*.82);
    $('cnt').textContent=D.ep?D.ep.big:((k)+'/5'); $('nm').textContent=META[sc].n; $('rule').textContent=META[sc].r; $('src').textContent=META[sc].s.toUpperCase();
    $('dg').innerHTML=SCENES[sc](p); $('dg').style.opacity=e; $('dg').style.transform='translateX('+((1-e)*60).toFixed(1)+'px)'; $('rule').style.opacity=e; }
  else { hook.style.display='none'; $('cnt').textContent=''; $('nm').textContent='THE FREE CHEAT SHEET'; $('rule').textContent=''; $('src').textContent='ALL FIVE ON ONE PAGE'; $('dg').innerHTML=''; $('cta').style.opacity=ss(P(t,ST[CT]-.05,.3)); }
  // hook thumbs pop
  TH.forEach((d,i)=>{const q=bk(P(t,.9+i*.38,.4)); d.style.opacity=q>0?1:0; d.style.transform='scale('+Math.max(.01,q).toFixed(3)+')';});
  const ht=hook.querySelector('.t'); ht.style.opacity=ss(P(t,.05,.3));
  $('cm').style.opacity=(k>=CT)?ss(P(t,ST[CT]+.4,.3)):0;
  // captions
  const cur=CH.find(c=>t>=c[0].a-0.02&&t<c[c.length-1].b+0.1);
  const cap=$('cap'); if(cur&&k<CT){ if(cap.dataset.k!==cur[0].a+''){cap.dataset.k=cur[0].a+''; cap.innerHTML=cur.map(o=>'<span class="w">'+o.w+'</span>').join('');}
    [...cap.children].forEach((s,i)=>{const o=cur[i]; s.className='w '+(t>=o.b?'done':(t>=o.a?'on':''));}); cap.style.opacity=1; } else if(k>=CT){cap.style.opacity=0;} else cap.style.opacity=0;
  // host: a scale figure, gestures follow the voice
  const hop=(()=>{let h=0; for(let i=1;i<=NSEG;i++){const q=P(t,ST[i],.35); if(q>0&&q<1) h=Math.sin(q*Math.PI)*8;} return h;})();
  // walk between stops, point while the card explains
  const XS=[300].concat(Array.from({length:NSEG},(_,i)=>i%2?360:740)).concat([540]); if(!D.ep) XS.splice(0,XS.length,300,330,740,360,740,360,540); let kk=Math.max(k,0), x0=kk===0?-130:XS[kk-1], x1=XS[kk];
  const w0=kk===0?0:ST[kk]-0.25, wd=kk===0?1.5:1.25, w=P(t,w0,wd), walking=w>0&&w<1;
  const dir=(x1>=x0)?1:-1, X=lerp(x0,x1,w), ph=Math.floor(t*5.5)%2, step=Math.abs(Math.sin(t*5.5*Math.PI));
  const sh=(walking?-step*9:-(Math.sin(t*8)*2*A)-hop*.5);
  const set=(id,on,dy,fl)=>{const e=$(id); e.style.opacity=on?1:0; e.style.left=X.toFixed(1)+'px'; e.style.transform='translate(-50%,'+dy.toFixed(1)+'px) scaleX('+(dir*fl)+')';};
  set('wA',walking&&ph===0,sh,-1); set('wB',walking&&ph===1,sh,-1); set('figP',!walking,sh,1);
  $('flash').style.opacity=.2*(1-cl((t-ST[0])/.12,0,1))*(t<.2?1:0)*0;
  window.__t=t;
}
if(D.ep) $('tagt').textContent='ADA NUMBER TO KNOW'; window.setT=setT; setT(0); window.ready=true;
</script></body></html>""".replace('__HOST__', HOST)

SHEET = r"""<!doctype html><html><head><meta charset="utf-8"><style>
@page{size:8.5in 11in;margin:0}
html,body{margin:0;width:1275px;height:1650px;background:#f6f4ee;font-family:Helvetica,Arial,sans-serif;color:#161616}
#t{position:absolute;left:60px;top:44px;width:1155px}
#t h1{margin:0;font:900 88px/.95 Helvetica;letter-spacing:-3px}#t h1 b{color:#1f9d63}
#t p{margin:14px 0 0;font:700 30px Helvetica;color:#555}
.pn{position:absolute;width:567px;height:420px;border:5px solid #161616;border-radius:18px;background:#fcfbf8;box-shadow:8px 8px 0 #161616;overflow:hidden}
.pn .n{position:absolute;left:18px;top:14px;width:62px;height:62px;border-radius:50%;background:#1f9d63;color:#fff;font:900 40px/62px Helvetica;text-align:center;border:4px solid #161616}
.pn .h{position:absolute;left:96px;top:14px;font:900 33px Helvetica;letter-spacing:-.5px}
.pn .r{position:absolute;left:96px;top:52px;font:800 22px Helvetica;color:#1f6d45}
.pn svg{position:absolute;left:31px;top:84px;width:504px;height:336px}
.pn .s{position:absolute;right:16px;top:66px;font:800 15px Helvetica;letter-spacing:2px;color:#8d8777}
#f{position:absolute;left:60px;top:1530px;width:1155px;font:700 19px/1.4 Helvetica;color:#555}
#f b{color:#161616}
</style></head><body>
<div id="t"><h1>ADA in <b>5 numbers</b></h1><p>Check these before you send a plan. One page, five diagrams.</p></div>
<div id="g"></div>
<div id="f"><b>Source:</b> 2010 ADA Standards for Accessible Design. Section numbers are shown on each diagram. Your jurisdiction's adopted code can add requirements, so check it for your project. &nbsp;·&nbsp; <b>@dm_motion1</b></div>
<script>
__DIAG__
const g=document.getElementById('g'); const pos=[[60,200],[648,200],[60,640],[648,640],[60,1080]];
SCENES.forEach((f,i)=>{const d=document.createElement('div'); d.className='pn'; d.style.left=pos[i][0]+'px'; d.style.top=pos[i][1]+'px';
 d.innerHTML='<div class="n">'+(i+1)+'</div><div class="h">'+META[i].n+'</div><div class="r">'+META[i].r+'</div><svg viewBox="0 0 960 640">'+f(1)+'</svg><div class="s">'+META[i].s.toUpperCase()+'</div>'; g.appendChild(d);});
const k=document.createElement('div'); k.className='pn'; k.style.left='648px'; k.style.top='1080px';
k.innerHTML='<div class="h" style="left:24px;top:22px;font-size:38px">How to use it</div><div style="position:absolute;left:24px;top:84px;width:520px;font:700 25px/1.4 Helvetica;color:#333">Check each number against your plan before a review.<br><br><span style="color:#1f9d63;font-weight:900">1</span> Switches and outlets between 15 and 48 in.<br><span style="color:#1f9d63;font-weight:900">2</span> A 30 x 48 in space at each fixture.<br><span style="color:#1f9d63;font-weight:900">3</span> A 60 in turning circle.<br><span style="color:#1f9d63;font-weight:900">4</span> Sink rim 34 in max.<br><span style="color:#1f9d63;font-weight:900">5</span> 32 in clear at every door.</div>'; g.appendChild(k);
window.ready=true;
</script></body></html>"""

import http.server, socketserver, threading, functools
class _Q(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass
_srv = socketserver.TCPServer(('127.0.0.1', 0), functools.partial(_Q, directory='/home/claude/reels')); PORT = _srv.server_address[1]
threading.Thread(target=_srv.serve_forever, daemon=True).start()
ARGS = ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist']


def make_sheet(out='/home/claude/reels/out2'):
    o = pathlib.Path(out); o.mkdir(exist_ok=True)
    hp = o / 'ada5_sheet.html'; hp.write_text(SHEET.replace('__DIAG__', DIAG))
    with sync_playwright() as pw:
        b = pw.chromium.launch(args=ARGS); pg = b.new_page(viewport={'width': 1275, 'height': 1650}, device_scale_factor=2)
        pg.goto(f'http://127.0.0.1:{PORT}/out2/ada5_sheet.html'); pg.wait_for_function('window.ready===true')
        pg.screenshot(path=str(o / 'ada5_sheet.png')); pg.pdf(path=str(o / 'ada5_sheet.pdf'), width='8.5in', height='11in', print_background=True); b.close()
    return str(o / 'ada5_sheet.png'), str(o / 'ada5_sheet.pdf')


def render(outdir='/home/claude/reels/out2', stills=None, name=(EP['name'] if EP else 'r_ic_walk')):
    out = pathlib.Path(outdir); out.mkdir(exist_ok=True)
    narration, starts, total = VOICE.narrate(SCRIPT)
    html, dur, T = build(starts, total, narration)
    sheet = f'http://127.0.0.1:{PORT}/out2/ada5_sheet.png'
    html = html.replace('__SHEET__', sheet).replace('__WA__', f'http://127.0.0.1:{PORT}/photo/walk_a.png').replace('__WB__', f'http://127.0.0.1:{PORT}/photo/walk_b.png').replace('__FIGPT__', f'http://127.0.0.1:{PORT}/photo/fig_point.png')
    hp = out / f'{name}.html'; hp.write_text(html)
    fr = out / f'fr_{name}'; fr.mkdir(exist_ok=True); N = int(FPS * dur)
    with sync_playwright() as pw:
        b = pw.chromium.launch(args=ARGS); pg = b.new_page(viewport={'width': W, 'height': H}); errs = []
        pg.on('pageerror', lambda e: (errs.append(str(e)), print('PE', str(e)[:300]))); pg.on('console', lambda m: print('C', m.text) if m.type in ('error', 'warning') else None)
        pg.goto(f'http://127.0.0.1:{PORT}/{hp.relative_to(ROOT)}'); pg.wait_for_function('window.ready===true', timeout=30000)
        ts = stills or [i / FPS for i in range(N)]
        for i, t in enumerate(ts):
            pg.evaluate(f'setT({t})'); pg.screenshot(path=str(fr / (f's_{t:05.2f}.png' if stills else f'{i:04d}.png')))
        b.close()
        if errs: print('ERR', errs[:3])
    if stills: return T, [str(fr / f's_{t:05.2f}.png') for t in stills]
    wav = str(out / f'{name}.wav')
    soundtrack.make(dur, draw=(0.2, 1.1), end=dur, mood='bright', bpm=100, seed=zlib.crc32(name.encode()) % 999, out=wav, pen=False, beat=True)
    ev = [(0.05, 'whoosh')]
    for k in range(1, NSEG + 1): ev += [(T['st'][k] - 0.05, 'whoosh'), (T['st'][k] + 0.2, 'tick')]
    ev += [(T['st'][NSEG + 1], 'hit'), (T['st'][NSEG + 1] + 0.6, 'chime')]
    sfx.add(wav, ev); VOICE.lay_under(wav, narration)
    mp4 = str(out / f'{name}.mp4')
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-framerate', str(FPS), '-i', str(fr / '%04d.png'), '-i', wav, '-c:v', 'libx264',
                    '-preset', 'veryfast', '-pix_fmt', 'yuv420p', '-crf', '20', '-c:a', 'aac', '-b:a', '192k', '-shortest', '-movflags', '+faststart', mp4], check=True)
    return mp4


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'sheet':
        print(make_sheet())
    elif len(sys.argv) > 1 and sys.argv[1] == 'stills':
        T, fs = render('/home/claude/reels/outT', stills=[float(x) for x in sys.argv[2].split(',')], name=(EP['name'] if EP else 'r_ic_walk'))
        print(T); print('\n'.join(fs))
    else:
        print(render())
