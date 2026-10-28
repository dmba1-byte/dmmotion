"""'How DM Motion works' explainer reel — paper-card motion graphics on a dot grid, synced to a voiceover script."""
import sys, json, pathlib, subprocess, math
sys.path.insert(0, '/home/claude/reels')
from playwright.sync_api import sync_playwright
from gen.plans import Plan
from gen.elevs import make as make_elev
from gen.engine2 import STYLES, prefix_ids, LOGO_D
from gen.figs import subs_from
import soundtrack
import numpy as np, scipy.io.wavfile as wavfile

W, H, FPS = 1080, 1920, 30
SCRIPT = ("Your floor plans are stuck in PDFs nobody opens. Here's the fix. One: send me your plan. PDF, CAD, Revit, or Illustrator. "
          "Two: I animate it. Lines draw on, walls go up, people move in. Three: you post it. Listings, socials, client pitches. "
          "Animations start at four fifty, and the five-second logo trial is free. Email me your plan, and I'll send you pricing.")
INK, PAPER, ORANGE, GREEN = '#141414', '#ffffff', '#1d4e89', '#2e9b62'


def assets():
    lt = STYLES['light']
    p = Plan(1208, 'split').build()
    plan = prefix_ids(p.svg(lt['ink'], lt['sub'], lt['tint'], box=(20, 20, 860, 660), title=False), 'pl_')
    plan2 = prefix_ids(p.svg(lt['ink'], lt['sub'], lt['tint'], box=(20, 20, 860, 660), title=False), 'pz_')
    ev, _, _ = make_elev('craftsman', 1300, lt); ev = prefix_ids(ev, 'ev_')
    ev2, _, _ = make_elev('cape', 1301, STYLES['bluewhite']); ev2 = prefix_ids(ev2, 'ec_')
    return plan, plan2, ev, ev2


def build_html():
    plan, plan2, ev, ev2 = assets()
    subs = subs_from(SCRIPT)
    st = lambda key: next(a for a, b, w in subs if w.startswith(key))
    T = dict(s2=st("One:"), files=[st('PDF,'), st('CAD'), st('Revit'), st('or Illus')], s3=st('Two:'), draw=st('Lines'), walls=st('walls'), people=st('people'),
             s4=st('Three:'), posts=[st('Listings'), st('socials'), st('client')], s5=st('Animations'), logo=st('and the five'), free=st('is free'),
             s6=st('Email me'), dm=st("and I'll send"))
    T['end'] = subs[-1][1] + 0.4
    dur = T['end'] + 2.6
    data = dict(T=T, subs=subs, dur=dur)
    html = f"""<!doctype html><html><head><meta charset="utf-8"><style>
html,body{{margin:0;width:{W}px;height:{H}px;overflow:hidden;font-family:Helvetica,Arial,sans-serif;color:{INK}}}
body{{background:{PAPER};background-image:linear-gradient(#e3e9f1 1.5px,transparent 1.5px),linear-gradient(90deg,#e3e9f1 1.5px,transparent 1.5px),linear-gradient(#f0f3f7 1px,transparent 1px),linear-gradient(90deg,#f0f3f7 1px,transparent 1px);background-size:120px 120px,120px 120px,24px 24px,24px 24px;background-position:0 0}}
.a{{position:absolute}} .card{{position:absolute;background:#fff;border:3.5px solid {INK};border-radius:18px;box-shadow:9px 9px 0 {INK}}}
.pill{{display:inline-block;background:#fff;border:3.5px solid {INK};border-radius:12px;box-shadow:6px 6px 0 {INK};padding:12px 22px;font-weight:800;letter-spacing:1px}}
.hd{{position:absolute;left:0;right:0;top:190px;text-align:center;font-size:66px;font-weight:900;letter-spacing:-1px;line-height:1.05;text-transform:uppercase}}
.hd b{{color:{ORANGE}}}
#bar{{position:absolute;left:70px;right:70px;top:96px;height:26px;display:flex;gap:10px}} #bar div{{flex:1;border:3px solid {INK};border-radius:6px;background:#fff;overflow:hidden}} #bar i{{display:block;height:100%;width:0;background:{ORANGE}}}
#subs{{position:absolute;left:60px;right:60px;top:1600px;text-align:center}} #subs span{{display:inline-block;background:{INK};color:#fff;font-size:46px;font-weight:900;text-transform:uppercase;padding:14px 26px;border-radius:12px;letter-spacing:.5px}}
#subs span b{{color:#5ccf8e}}
.chip{{position:absolute;font-size:34px}} .tick{{display:inline-block;width:34px;height:34px;border-radius:50%;background:{GREEN};color:#fff;font-size:24px;line-height:34px;text-align:center;margin-right:12px;vertical-align:2px}}
.file{{position:absolute;width:150px;height:184px}} .file .card{{inset:0;border-radius:14px}} .file .lab{{position:absolute;left:0;right:0;bottom:22px;text-align:center;font-size:36px;font-weight:900}}
.file .fold{{position:absolute;right:-3px;top:-3px;width:44px;height:44px;background:#ffffff;border-left:3.5px solid {INK};border-bottom:3.5px solid {INK};border-bottom-left-radius:10px}}
.phone{{position:absolute;width:300px;height:560px}} .phone .card{{inset:0;border-radius:34px;overflow:hidden}} .phone .tag{{position:absolute;left:0;right:0;bottom:-78px;text-align:center}}
</style></head><body>
<div id="bar">{''.join('<div><i></i></div>' for _ in range(6))}</div>
<div class="hd" id="h0">Static PDFs<br>get <b>skipped</b></div>
<div class="hd" id="h1" style="opacity:0"><b>01</b> Send your plan</div>
<div class="hd" id="h2" style="opacity:0"><b>02</b> I animate it</div>
<div class="hd" id="h3" style="opacity:0"><b>03</b> You post it</div>
<div class="hd" id="h4" style="opacity:0">The <b>price</b></div>
<div class="hd" id="h5" style="opacity:0">Get <b>pricing</b></div>

<!-- S1: the PDF nobody opens -->
<div class="card" id="pdf" style="left:150px;top:470px;width:780px;height:860px">
  <div class="a" style="left:0;right:0;top:0;height:86px;border-bottom:3.5px solid {INK};font:800 30px Menlo,monospace;line-height:86px;padding-left:30px">FLOOR_PLAN_FINAL_v7.pdf</div>
  <svg class="a" style="left:40px;top:120px;opacity:.55;filter:grayscale(1)" width="700" height="540" viewBox="0 0 900 700">{plan2}</svg>
  <div class="a" style="left:40px;right:40px;top:700px;height:20px;background:#e9edf2;border-radius:6px"></div><div class="a" style="left:40px;width:420px;top:740px;height:20px;background:#e9edf2;border-radius:6px"></div><div class="a" style="left:40px;width:560px;top:780px;height:20px;background:#e9edf2;border-radius:6px"></div>
</div>
<div class="a" id="stamp" style="left:170px;top:760px;width:740px;text-align:center;opacity:0"><span style="display:inline-block;border:8px solid {ORANGE};color:{ORANGE};font-size:84px;font-weight:900;padding:12px 30px;border-radius:14px;letter-spacing:2px;background:rgba(255,255,255,.88)">NOBODY OPENS THIS</span></div>

<!-- S2: send your plan -->
<div class="card" id="drop" style="left:130px;top:640px;width:820px;height:640px;opacity:0">
  <div class="a" style="left:40px;right:40px;top:40px;bottom:150px;border:4px dashed #9fb3cc;border-radius:16px"></div>
  <div class="a" style="left:0;right:0;top:200px;text-align:center;font-size:34px;color:#7f8a99;font-weight:700" id="droptxt">Drop your drawing here</div>
  <div class="a" style="left:40px;right:40px;bottom:50px;height:56px;border:3.5px solid {INK};border-radius:12px;overflow:hidden"><i id="prog" style="display:block;height:100%;width:0;background:{ORANGE}"></i></div>
  <div class="a" id="sent" style="left:0;right:0;bottom:56px;text-align:center;font-size:30px;font-weight:900;color:#fff;opacity:0;line-height:44px">SENT TO DM MOTION ✓</div>
</div>
{''.join(f'<div class="file" id="f{i}" style="opacity:0"><div class="card"></div><div class="fold"></div><div class="lab">{n}</div></div>' for i, n in enumerate(['PDF', 'DWG', 'RVT', 'AI']))}

<!-- S3: animate -->
<div class="card" id="anim" style="left:90px;top:430px;width:900px;height:700px;opacity:0;overflow:hidden"><svg id="plansvg" width="900" height="700" viewBox="0 0 900 700">{plan}</svg>
  </div>
<div class="card" id="elev" style="left:380px;top:860px;width:640px;height:470px;opacity:0;overflow:hidden"><svg width="640" height="470" viewBox="0 520 1080 793">{ev}</svg></div>
<div class="chip pill" id="c0" style="left:70px;top:1180px;opacity:0"><span class="tick">✓</span>Lines draw on</div>
<div class="chip pill" id="c1" style="left:70px;top:1290px;opacity:0"><span class="tick">✓</span>Walls go up</div>
<div class="chip pill" id="c2" style="left:70px;top:1400px;opacity:0"><span class="tick">✓</span>People move in</div>

<!-- S4: post it -->
{''.join(f'<div class="phone" id="ph{i}" style="opacity:0"><div class="card">{c}</div><div class="tag"><span class="pill" style="font-size:30px">{t}</span></div></div>' for i, (t, c) in enumerate([
    ('LISTING', f'<div class="a" style="left:20px;right:20px;top:40px;font:800 22px Helvetica">3 BED · 2 BATH</div><svg class="a" style="left:6px;top:90px" width="238" height="190" viewBox="0 0 900 700">{plan.replace(chr(34)+"pl_", chr(34)+"q1_").replace("#pl_", "#q1_")}</svg><div class="a" style="left:20px;right:20px;top:310px;height:54px;background:{ORANGE};border-radius:10px;color:#fff;font:800 24px Helvetica;text-align:center;line-height:54px">BOOK A TOUR</div>'),
    ('INSTAGRAM', f'<svg class="a" style="left:-60px;top:70px" width="370" height="290" viewBox="0 520 1080 793">{ev2}</svg><div class="a" id="likes" style="left:22px;bottom:36px;font:800 26px Helvetica">♥ 0</div>'),
    ('CLIENT PITCH', f'<div class="a" style="left:20px;right:20px;top:40px;font:800 22px Helvetica">PROPOSAL · LOT 14</div><svg class="a" style="left:-50px;top:110px" width="350" height="260" viewBox="0 520 1080 793">{ev.replace(chr(34)+"ev_", chr(34)+"q3_").replace("#ev_", "#q3_")}</svg>')]))}

<!-- S5: price sign -->
<div class="a" id="sign" style="left:240px;top:560px;width:600px;height:560px;opacity:0;transform-origin:300px 0px">
  <svg class="a" style="left:0;top:0" width="600" height="200"><line x1="300" y1="0" x2="80" y2="170" stroke="{INK}" stroke-width="5"/><line x1="300" y1="0" x2="520" y2="170" stroke="{INK}" stroke-width="5"/><circle cx="300" cy="0" r="16" fill="{INK}"/></svg>
  <div class="card" style="left:0;top:160px;width:592px;height:380px;text-align:center"><div style="font-size:52px;font-weight:900;margin-top:50px;letter-spacing:2px">ANIMATIONS FROM</div><div style="font-size:170px;font-weight:900;letter-spacing:-6px;line-height:1.1;color:{ORANGE}">$450</div></div>
</div>
<div class="a" id="trial" style="left:0;right:0;top:1230px;text-align:center;opacity:0"><span class="pill" style="font-size:44px">5-SECOND LOGO TRIAL</span></div>
<div class="a" id="free" style="left:0;right:0;top:1350px;text-align:center;opacity:0"><span style="display:inline-block;border:7px solid {GREEN};color:{GREEN};font-size:84px;font-weight:900;padding:4px 34px;border-radius:14px;background:{PAPER}">FREE</span></div>

<!-- S6: email -> reply -->
<div class="card" id="cbox" style="left:90px;top:560px;width:900px;height:250px;opacity:0">
  <div class="a" style="left:30px;top:26px;font:800 34px Helvetica"><span style="color:#7f8a99">To</span>&nbsp; dmba04@gmail.com</div>
  <div class="a" style="left:30px;right:30px;top:86px;border-top:2.5px solid #e3e9f1"></div>
  <div class="a" id="ctext" style="left:30px;top:106px;font-size:40px;font-weight:800;color:#9aa3ad">Subject</div>
  <div class="a" id="clip" style="left:30px;top:172px;opacity:0;border:2.5px solid {INK};border-radius:10px;padding:6px 14px;font:800 26px Helvetica">📎 floor_plan.pdf</div>
  <div class="a" id="post" style="right:26px;top:150px;height:78px;width:170px;border-radius:12px;background:{INK};color:#fff;font:900 34px Helvetica;text-align:center;line-height:78px">SEND</div>
</div>
<div class="card" id="dm" style="left:90px;top:860px;width:900px;height:330px;opacity:0">
  <div class="a" style="left:30px;top:26px;font:800 26px Helvetica;letter-spacing:2px;color:{ORANGE}">RE: MY FLOOR PLAN</div>
  <svg class="a" style="left:30px;top:80px" width="90" height="90" viewBox="-2.18 -2.45 309.7 309.7"><rect x="-2" y="-2" width="310" height="310" rx="60" fill="{INK}"/><path d="{LOGO_D}" fill="#fff" transform="translate(50 50) scale(0.68)"/></svg>
  <div class="a" style="left:150px;top:84px;font:900 40px Helvetica">DM Motion</div>
  <div class="a" style="left:150px;top:140px;right:40px;font:600 36px Helvetica;line-height:1.3">Here's the pricing for your plan, plus a free logo trial.</div>
</div>
<div class="a" id="endc" style="left:0;right:0;top:0;bottom:0;opacity:0;background:{INK}">
  <svg class="a" style="left:420px;top:640px" width="240" height="240" viewBox="-2.18 -2.45 309.7 309.7"><path id="endlogo" d="{LOGO_D}" fill="#fff"/></svg>
  <div class="a" style="left:0;right:0;top:940px;text-align:center;color:#fff;font:900 70px Helvetica;letter-spacing:-1px">Your drawing, in motion.</div>
  <div class="a" style="left:0;right:0;top:1050px;text-align:center"><span class="pill" style="font-size:40px;box-shadow:6px 6px 0 {GREEN}">Pricing: dmba04@gmail.com</span></div>
</div>
<div id="subs"></div>
<script>
const D={json.dumps(data)}, T=D.T;
const $=i=>document.getElementById(i), cl=(x,a,b)=>Math.max(a,Math.min(b,x)), P=(t,a,d)=>cl((t-a)/d,0,1);
const eo=x=>1-Math.pow(1-x,3), back=x=>{{const c=1.9;return 1+(c+1)*Math.pow(x-1,3)+c*Math.pow(x-1,2)}};
const ease=t=>t<.5?2*t*t:1-Math.pow(-2*t+2,2)/2;
function pop(el,t,a,dx=0,dy=60,rot=0){{ const p=P(t,a,0.42); el.style.opacity=cl(p*3,0,1); el.style.transform=`translate(${{dx*(1-eo(p))}}px,${{dy*(1-back(p))}}px) scale(${{0.86+0.14*back(p)}}) rotate(${{rot*(1-eo(p))}}deg)`; }}
function out(el,t,a,dx=-1200){{ if(t<a) return; const p=ease(P(t,a,0.45)); el.style.transform=(el.style.transform||'')+` translateX(${{dx*p}}px)`; el.style.opacity=String(parseFloat(el.style.opacity||1)*(1-p)); }}
// plan draw setup
const PG=['pl_walls-ext','pl_walls-int','pl_openings','pl_fixtures','pl_labels','pl_dims'].map(id=>$(id)).filter(Boolean);
const PE=[]; PG.forEach((g,gi)=>[...g.querySelectorAll('line,path,rect,circle,text')].forEach(el=>{{ let L=0; if(el.tagName!=='text'){{try{{L=el.getTotalLength()}}catch(e){{}}}} if(L>0){{el.style.strokeDasharray=L;el.style.strokeDashoffset=L}} else el.style.opacity=0; PE.push({{el,L,gi}}); }}));
const pt=$('pl_tint'); if(pt) pt.style.opacity=0;
const phones=[[60,1000,-6],[390,960,0],[720,1000,6]];
const files=[[200,330],[380,300],[560,330],[740,300]];
window.setT=t=>{{
 // progress bar
 const segs=[0,T.s2,T.s3,T.s4,T.s5,T.s6,T.end]; [...document.querySelectorAll('#bar i')].forEach((b,i)=>b.style.width=(100*P(t,segs[i],segs[i+1]-segs[i]))+'%');
 // headers
 const hs=[0,T.s2-0.2,T.s3-0.2,T.s4-0.2,T.s5-0.2,T.s6-0.2,1e9];
 for(let i=0;i<6;i++){{ const el=$('h'+i), a=P(t,hs[i],0.3), b=P(t,hs[i+1],0.25); el.style.opacity=i==0?1-b:a*(1-b); el.style.transform=`translateY(${{(1-eo(a))*(i?40:0)-30*b}}px)`; }}
 // S1
 pop($('pdf'),t,0.15,0,90,-3); $('pdf').style.transform+=` rotate(${{-2+Math.sin(t*1.3)*0.6}}deg)`;
 {{ const p=P(t,T.s2-3.3,0.28); const s=$('stamp'); s.style.opacity=p; s.style.transform=`rotate(-9deg) scale(${{1.7-0.7*eo(p)}})`; }}
 out($('pdf'),t,T.s2-1.2); out($('stamp'),t,T.s2-1.2);
 // S2
 pop($('drop'),t,T.s2,0,80); out($('drop'),t,T.s3-0.15);
 T.files.forEach((a,i)=>{{ const el=$('f'+i), [fx,fy]=files[i], p=P(t,a,0.5), q=ease(P(t,T.files[3]+0.25,0.4));
   const x=fx+(1-eo(p))*(i%2?260:-260), y=fy+(1-eo(p))*-120+q*(520-fy); el.style.left=(x+(q*(470-fx)))+'px'; el.style.top=(470+y)+'px';
   el.style.opacity=cl(p*3,0,1)*(1-P(t,T.files[3]+0.6,0.15))*(t<T.s3?1:0); el.style.transform=`rotate(${{(i-1.5)*8*(1-q)}}deg) scale(${{1-0.35*q}})`; }});
 $('droptxt').style.opacity=1-P(t,T.files[0],0.3);
 const pr=P(t,T.files[3]+0.45,0.6); $('prog').style.width=(100*ease(pr))+'%'; $('sent').style.opacity=P(t,T.files[3]+1.05,0.15);
 // S3 animate
 pop($('anim'),t,T.s3,0,80); out($('anim'),t,T.s4-0.35);
 const d0=T.s3+0.35, d1=T.walls+0.2, n=PE.length;
 let act=null;
 PE.forEach((e,i)=>{{ const a=d0+(d1-d0)*(e.gi/PG.length)+ (d1-d0)/PG.length*0.9*((i%40)/40), p=P(t,a,0.35);
   if(e.L>0){{ e.el.style.strokeDashoffset=e.L*(1-ease(p)); if(p>0&&p<1&&(!act||a<act.a)) act={{e,a,p}}; }} else e.el.style.opacity=p; }});
 if(pt) pt.style.opacity=P(t,d1-0.6,0.8);
 pop($('elev'),t,T.walls,120,60,4); out($('elev'),t,T.s4-0.35);
 // elevation reveal inside its card: walls/roof draw quickly, figures at 'people'
 ['ev_figs','ev_figs2'].forEach((id,k)=>{{ const g=$(id); if(g) g.style.opacity=P(t,T.people+k*0.3,0.4); }});
 [['c0',T.draw],['c1',T.walls],['c2',T.people]].forEach(([id,a])=>{{ pop($(id),t,a,-80,0); out($(id),t,T.s4-0.35); }});
 // S4 phones
 T.posts.forEach((a,i)=>{{ const el=$('ph'+i), [px,py,r]=phones[i]; el.style.left=px+'px'; el.style.top=(py-430)+'px'; pop(el,t,a,0,140,r*2); el.style.transform+=` rotate(${{r}}deg)`; out(el,t,T.s5-0.35); }});
 $('likes').textContent='♥ '+Math.floor(2400*eo(P(t,T.posts[1]+0.3,2.4))).toLocaleString();
 // S5 sign
 {{ const p=P(t,T.s5,0.35), s=$('sign'), sw=Math.exp(-(t-T.s5)*1.4)*Math.sin((t-T.s5)*6)*14; s.style.opacity=cl(p*3,0,1)*(t>=T.s5?1:0); s.style.transform=`translateY(${{-500*(1-eo(p))}}px) rotate(${{t>T.s5?sw:0}}deg)`; out(s,t,T.s6-0.35); }}
 pop($('trial'),t,T.logo,0,60); out($('trial'),t,T.s6-0.35);
 {{ const p=P(t,T.free,0.25), f=$('free'); f.style.opacity=p; f.style.transform=`rotate(-6deg) scale(${{1.6-0.6*eo(p)}})`; out(f,t,T.s6-0.35); }}
 // S6 comment -> DM
 pop($('cbox'),t,T.s6,0,60);
 const SUBJ='My floor plan', typed=SUBJ.slice(0,Math.floor(cl((t-T.s6-0.35)/0.06,0,SUBJ.length))); $('ctext').textContent=typed||'Subject'; $('ctext').style.color=typed?'{INK}':'#9aa3ad'; $('clip').style.opacity=P(t,T.s6+1.2,0.2);
 const pp=P(t,T.dm-0.5,0.12)*(1-P(t,T.dm-0.3,0.12)); $('post').style.transform=`scale(${{1-0.08*pp}})`; $('post').style.background=t>T.dm-0.5?'{GREEN}':'{INK}';
 pop($('dm'),t,T.dm,0,240);
 // end card
 $('endc').style.opacity=P(t,T.end,0.5);
 // subs
 let txt=''; for(const [a,b,w] of D.subs){{ if(t>=a&&t<b){{ txt=w; break; }} }}
 txt=txt.replace(/\\b(PLAN|four fifty|free|nobody|fix)\\b/g,'<b>$1</b>');
 $('subs').innerHTML=txt&&t<T.end?`<span>${{txt}}</span>`:'';
}};
setT(0);
</script></body></html>"""
    return html, data


def sfx_track(data, music_wav, out_wav):
    sr, m = wavfile.read(music_wav); m = m.astype(np.float32) / 32768.0
    if m.ndim == 1: m = np.stack([m, m], 1)
    T = data['T']; rng = np.random.default_rng(5)
    def add(t, sig, g=1.0):
        i = int(t * sr); j = min(len(m), i + len(sig)); m[i:j] += (sig[:j - i, None] * g)
    def pop(f=880, d=0.09):
        n = int(sr * d); tt = np.arange(n) / sr; return np.sin(2 * np.pi * f * tt * (1 + 0.6 * np.exp(-tt * 40))) * np.exp(-tt * 38) * 0.35
    def thud():
        n = int(sr * 0.25); tt = np.arange(n) / sr; return (np.sin(2 * np.pi * 70 * tt) * np.exp(-tt * 16) * 0.7 + rng.normal(0, 1, n) * np.exp(-tt * 60) * 0.15)
    def whoosh(d=0.35):
        n = int(sr * d); x = rng.normal(0, 1, n); env = np.sin(np.linspace(0, np.pi, n)) ** 2
        from scipy.signal import butter, lfilter
        b, a = butter(2, [600 / (sr / 2), 4000 / (sr / 2)], 'band'); return lfilter(b, a, x) * env * 0.12
    def click():
        n = int(sr * 0.03); tt = np.arange(n) / sr; return rng.normal(0, 1, n) * np.exp(-tt * 220) * 0.22
    add(0.15, pop(660)); add(T['s2'] - 3.3, thud())
    for a in (T['s2'] - 1.2, T['s3'] - 0.35, T['s4'] - 0.35, T['s5'] - 0.35, T['s6'] - 0.35): add(a, whoosh())
    add(T['s2'], pop(740))
    for k, a in enumerate(T['files']): add(a, pop(700 + 90 * k))
    add(T['files'][3] + 1.05, pop(1320, 0.14))
    add(T['s3'], pop(740)); add(T['walls'], pop(820)); [add(a, pop(1050, 0.07)) for a in (T['draw'], T['walls'], T['people'])]
    for k, a in enumerate(T['posts']): add(a, pop(760 + 120 * k))
    add(T['s5'], whoosh(0.3)); add(T['s5'] + 0.3, thud()); add(T['logo'], pop(900)); add(T['free'], thud())
    add(T['s6'], pop(740))
    for k in range(13): add(T['s6'] + 0.35 + k * 0.06, click())
    add(T['dm'] - 0.5, click()); add(T['dm'], pop(1180, 0.16), 1.2); add(T['end'], whoosh(0.5))
    m = np.clip(m, -1, 1); wavfile.write(out_wav, sr, (m * 32767).astype(np.int16))


def render(outdir='/home/claude/reels/out2', name='r_explainer_how', stills=None):
    out = pathlib.Path(outdir); html, data = build_html(); hp = out / f'{name}.html'; hp.write_text(html)
    fr = out / f'fr_{name}'; fr.mkdir(exist_ok=True, parents=True)
    N = int(FPS * data['dur'])
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': W, 'height': H}); errs = []
        pg.on('pageerror', lambda e: errs.append(str(e))); pg.goto(hp.resolve().as_uri()); pg.wait_for_timeout(400)
        ts = stills or [i / FPS for i in range(N)]
        for i, t in enumerate(ts):
            pg.evaluate(f'setT({t})'); pg.screenshot(path=str(fr / (f's_{t:05.2f}.png' if stills else f'{i:04d}.png')))
        b.close()
        if errs: print('ERR', errs[:3])
    if stills: return [str(fr / f's_{t:05.2f}.png') for t in stills], data
    mw = str(out / f'{name}_bed.wav'); soundtrack.make(data['dur'], draw=(data['T']['s3'] + 0.3, data['T']['walls'] + 0.3), end=data['T']['end'], mood='bright', bpm=100, seed=77, out=mw, pen=True, beat=True)
    wav = str(out / f'{name}.wav'); sfx_track(data, mw, wav)
    mp4 = str(out / f'{name}.mp4')
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-framerate', str(FPS), '-i', str(fr / '%04d.png'), '-i', wav, '-c:v', 'libx264', '-preset', 'veryfast', '-pix_fmt', 'yuv420p', '-crf', '20',
                    '-c:a', 'aac', '-b:a', '192k', '-shortest', '-movflags', '+faststart', mp4], check=True)
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', mp4, '-an', '-c:v', 'copy', str(out / f'{name}_silent.mp4')], check=True)
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', wav, '-c:a', 'libmp3lame', '-b:a', '192k', str(out / f'{name}_music.mp3')], check=True)
    return mp4, data


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'stills':
        ts = [float(x) for x in sys.argv[2].split(',')]
        paths, d = render('/home/claude/reels/outT', stills=ts); print(json.dumps(d['T'])); print('\n'.join(paths))
    else:
        print(render())
