"""Reel engine v2: layered drawings, absolute schedules, camera moves, isometric pop-up, built-in sound."""
import re, json, pathlib, subprocess, shutil, sys
from playwright.sync_api import sync_playwright
sys.path.insert(0, '/home/claude/reels')
import soundtrack
W, H, FPS = 1080, 1920, 30
LOGO_D = re.search(r'<path d="([^"]+)"', open('/home/claude/logo/DM_logo_mark-black.svg').read()).group(1)

STYLES = {
 'light':     dict(bg='#ffffff', ink='#1f1f1f', sub='#8a8a8a', tint='#f1efe9', tint2='#e6e3dc', lawn='#eef0e8', road='#ecebe7', hook='#1f1f1f', hook2='#6b6b6b', wall='#f7f6f2'),
 'blueprint': dict(bg='#0e2a47', ink='#eaf2ff', sub='#8fb0d6', tint='#12365a', tint2='#173f68', lawn='#113353', road='#0f2f4d', hook='#ffffff', hook2='#9fc0e6', wall='#1c4a78'),
 'dark':      dict(bg='#141414', ink='#f2f2f2', sub='#8c8c8c', tint='#1e1e1e', tint2='#272727', lawn='#1b1e1a', road='#1d1d1d', hook='#ffffff', hook2='#9a9a9a', wall='#2c2c2c'),
 'bluewhite': dict(bg='#ffffff', ink='#1d4e89', sub='#7fa3cc', tint='#eef4fb', tint2='#dbe7f5', lawn='#eaf2fa', road='#eef2f7', hook='#1d4e89', hook2='#6b8fb8', wall='#ffffff'),
 'kraft':     dict(bg='#e8dbc2', ink='#3b2f24', sub='#8a7458', tint='#f2e9d6', tint2='#dccaa9', lawn='#ddd1b5', road='#d6c7a8', hook='#3b2f24', hook2='#7a6650', wall='#f6efe1'),
 'sketch':    dict(bg='#fbfaf6', ink='#3d3d3d', sub='#9a9a9a', tint='#f3f1ea', tint2='#e8e5dc', lawn='#eef0e6', road='#ecebe5', hook='#2b2b2b', hook2='#7b7b7b', wall='#ffffff', rough=True),
 'color':     dict(bg='#ffffff', ink='#1f2a36', sub='#8592a0', tint='#f4f4f2', tint2='#e7e9ec', lawn='#e9f2e3', road='#ecedef', hook='#1f2a36', hook2='#6b7684', wall='#ffffff',
                   fills={'bed': '#e6eefa', 'bath': '#dff2ef', 'wic': '#eef0f2', 'living': '#fbefdc', 'kitchen': '#f9e4e0', 'dining': '#f2eafa', 'hall': '#f4f4f1', 'laundry': '#eaf1e1', 'pantry': '#f1f1ee', 'garage': '#ebebeb', 'foyer': '#f4f4f1'}),
}

def prefix_ids(svg, p):
    svg = re.sub(r'id="([^"]+)"', lambda m: f'id="{p}{m.group(1)}"', svg)
    return re.sub(r'url\(#([^)]+)\)', lambda m: f'url(#{p}{m.group(1)})', svg)

def build_html(job):
    st = STYLES[job['style']]
    layers_html = []
    for L in job['layers']:
        filt = ' filter="url(#rough)"' if st.get('rough') else ''
        layers_html.append(f'<g id="{L["id"]}" style="opacity:{L.get("op0", 1)}"><g id="{L["id"]}_cam"{filt}>{L["svg"]}</g></g>')
    iso_html = '<g id="iso" style="opacity:0"></g>' if job.get('iso') else ''
    data = {k: job.get(k) for k in ('layers_meta', 'iso', 'end', 'tint_windows', 'hook_out', 'figs', 'timer', 'subs')}
    sched = job['sched']
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>
html,body{{margin:0;width:{W}px;height:{H}px;background:{st['bg']};overflow:hidden;font-family:Helvetica,Arial,sans-serif}}
svg{{position:absolute;left:0;top:0}} .t{{position:absolute;left:60px;right:60px;text-align:center}}
#hook{{top:{job.get('hook_top', 250)}px;font-size:64px;font-weight:700;letter-spacing:-1px;line-height:1.1;color:{st['hook']}}} #sub{{top:{job.get('hook_top', 250) + 170}px;font-size:34px;color:{st['hook2']}}}
#end{{position:absolute;inset:0;background:#141414;opacity:0}}
#e1{{top:820px;font-size:70px;font-weight:700;color:#fff;letter-spacing:-1px;opacity:0}} #e2{{top:930px;font-size:38px;color:#bdbdbd;opacity:0;line-height:1.35}}
#spec{{position:absolute;left:0;right:0;top:{job.get('hook_top', 250) - 92}px;text-align:center}} #spec span{{display:inline-block;border:2.5px solid {st['hook']};color:{st['hook']};font:700 27px Helvetica,Arial,sans-serif;letter-spacing:3px;padding:9px 20px;border-radius:8px}}
#timer{{position:absolute;top:120px;right:60px;font:600 30px Menlo,monospace;color:{st['hook2']};opacity:0;letter-spacing:1px}}
#subs{{position:absolute;left:90px;right:90px;top:{job.get('subs_top', 1420)}px;text-align:center}} #subs span{{display:inline-block;background:rgba(0,0,0,.72);color:#fff;font-size:40px;font-weight:700;line-height:1.3;padding:12px 22px;border-radius:12px}}
#e3{{top:1140px;opacity:0}} #e3 span{{display:inline-block;background:#fff;color:#141414;font-size:40px;font-weight:700;padding:24px 44px;border-radius:14px}}
</style></head><body>
<div id="spec">{('<span>' + job['spec'] + '</span>') if job.get('spec') else ''}</div><div class="t" id="hook">{job['hook']}</div><div class="t" id="sub">{job['sub']}</div>
<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}"><defs><filter id="rough" x="-5%" y="-5%" width="110%" height="110%"><feTurbulence type="fractalNoise" baseFrequency="0.035" numOctaves="2" seed="3"/><feDisplacementMap in="SourceGraphic" scale="3.2"/></filter></defs>
<g id="cam" style="transform-origin:540px 960px">{''.join(layers_html)}{iso_html}</g></svg>
<div id="timer">0:00</div><div id="subs"></div>
<div id="end"></div>
<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}"><g transform="translate(435 470) scale(0.68)"><svg viewBox="-2.18 -2.45 309.7 309.7" width="309.7" height="309.7" overflow="visible">
<path id="lfill" d="{LOGO_D}" fill="#fff" opacity="0"/><path id="link" d="{LOGO_D}" fill="none" stroke="#fff" stroke-width="5" stroke-linejoin="round"/></svg></g></svg>
<div class="t" id="e1">Your drawing, in motion.</div><div class="t" id="e2">Your drawing, animated · from $450<br>Free 5-second logo trial</div>
<div class="t" id="e3"><span>{job['cta']}</span></div>
<script>
const SCHED={json.dumps(sched)}, D={json.dumps(data)}, ST={json.dumps(st)}, E=D.end;
const ease=t=>t<.5?2*t*t:1-Math.pow(-2*t+2,2)/2, cl=(x,a,b)=>Math.max(a,Math.min(b,x)), $=i=>document.getElementById(i);
const lerp=(a,b,t)=>a+(b-a)*t;
const items=[];
for(const [id,[s,e,d]] of Object.entries(SCHED)){{
 const g=$(id); if(!g) continue;
 const els=[...g.querySelectorAll('line,path,rect,circle,text')]; const n=els.length, span=d==='seq'?0:Math.max(0,(e-s)-d);
 let lens=[],tot=0; if(d==='seq'){{lens=els.map(el=>{{try{{return el.getTotalLength()}}catch(x){{return 0}}}});tot=lens.reduce((a,b)=>a+b,0)||1}}
 let cum=0;
 els.forEach((el,i)=>{{let t0,dd; if(d==='seq'){{t0=s+(e-s)*cum/tot;dd=Math.max(0.001,(e-s)*lens[i]/tot);cum+=lens[i]}}else{{t0=s+span*(n>1?i/(n-1):0);dd=d}}
  const isT=el.tagName==='text', f=el.getAttribute('fill')&&el.getAttribute('fill')!=='none'; let L=0;
  if(!isT){{try{{L=el.getTotalLength()}}catch(x){{}}}} if(!isT&&L>0){{el.style.strokeDasharray=L;el.style.strokeDashoffset=L}}
  if(f&&!isT)el.style.fillOpacity=0; if(isT)el.style.opacity=0; items.push({{el,t0,d:dd,L,isT,f,fo:parseFloat(el.getAttribute('fill-opacity')||'1'),seq:d==='seq'}})}});
}}
// tint groups per layer
const tints=(D.tint_windows||[]).map(([id,a,b])=>({{els:$(id)?[...$(id).children]:[],a,b}})); tints.forEach(o=>o.els.forEach(x=>x.style.opacity=0));
// camera keyframes per layer: [t, scale, cx, cy]
function kf(arr,t){{ if(!arr||!arr.length) return null; if(t<=arr[0][0]) return arr[0].slice(1); for(let i=1;i<arr.length;i++){{ if(t<=arr[i][0]){{ const a=arr[i-1],b=arr[i],p=ease((t-a[0])/(b[0]-a[0])); return a.slice(1).map((v,k)=>lerp(v,b[k+1],p)); }} }} return arr[arr.length-1].slice(1); }}
// isometric pop-up
let ISO=null;
if(D.iso){{
 const I=D.iso, g=$('iso'), NS='http://www.w3.org/2000/svg';
 const floors=I.rooms.map(r=>{{const p=document.createElementNS(NS,'polygon'); p.setAttribute('fill',r[4]); p.setAttribute('stroke',ST.sub); p.setAttribute('stroke-width','0.8'); g.appendChild(p); return {{r,p}}; }});
 const ws=I.walls.slice().sort((a,b)=>(a[0]+a[2]+a[1]+a[3])-(b[0]+b[2]+b[1]+b[3])).map(w=>{{const p=document.createElementNS(NS,'polygon'); p.setAttribute('fill',ST.wall); p.setAttribute('stroke',ST.ink); p.setAttribute('stroke-width', w[6]?'1.6':'1.1'); p.setAttribute('stroke-linejoin','round'); g.appendChild(p); return {{w,p}}; }});
 ISO={{I,floors,ws}};
}}

// scale figures
const FIGS=[];
(D.figs||[]).forEach(f=>{{ const host=$(f.layer+'_cam'); if(!host) return; const NS='http://www.w3.org/2000/svg';
  const g=document.createElementNS(NS,'g'); g.setAttribute('opacity','0'); host.appendChild(g);
  const s=f.s;
  if(f.type==='top'){{ const sh=document.createElementNS(NS,'ellipse'); sh.setAttribute('rx',0.95*s); sh.setAttribute('ry',0.45*s); sh.setAttribute('fill',ST.bg); sh.setAttribute('stroke',ST.ink); sh.setAttribute('stroke-width',Math.max(1.4,s*0.09));
    const hd=document.createElementNS(NS,'circle'); hd.setAttribute('r',0.5*s); hd.setAttribute('fill',f.accent||ST.ink); g.appendChild(sh); g.appendChild(hd); }}
  else {{ const p=document.createElementNS(NS,'path'); p.setAttribute('d',f.d); p.setAttribute('fill',f.accent||ST.ink); p.setAttribute('fill-opacity','0.88'); g.appendChild(p); }}
  FIGS.push({{f,g}}); }});
function along(pts,u){{ if(pts.length===1) return [pts[0][0],pts[0][1],0]; let L=[0]; for(let i=1;i<pts.length;i++) L.push(L[i-1]+Math.hypot(pts[i][0]-pts[i-1][0],pts[i][1]-pts[i-1][1]));
  const T=L[L.length-1]*u; let i=1; while(i<L.length-1&&L[i]<T) i++; const a=pts[i-1],b=pts[i],seg=(L[i]-L[i-1])||1,k=cl((T-L[i-1])/seg,0,1);
  return [a[0]+(b[0]-a[0])*k, a[1]+(b[1]-a[1])*k, Math.atan2(b[1]-a[1],b[0]-a[0])]; }}
function isoPt(x,y,z,m){{ const I=D.iso; const tx=I.X0+x*I.S, ty=I.Y0+y*I.S; const ix=I.ox+(x-y)*I.k*0.866, iy=I.oy+(x+y)*I.k*0.5-z*I.k; return [lerp(tx,ix,m), lerp(ty,iy,m)]; }}
window.setT=t=>{{
 for(const it of items){{const p=cl((t-it.t0)/it.d,0,1); if(it.isT)it.el.style.opacity=p; else{{
  if(it.L>0)it.el.style.strokeDashoffset=it.L*(1-(it.seq?p:ease(p))); if(it.f)it.el.style.fillOpacity=it.fo*cl((t-it.t0-it.d*.6)/(it.d*.6),0,1)}}}}
 tints.forEach(o=>o.els.forEach(x=>x.style.opacity=cl((t-o.a)/(o.b-o.a),0,1)));
 for(const L of (D.layers_meta||[])){{ const g=$(L.id); if(!g) continue;
   if(L.op){{ g.style.opacity=kf(L.op,t)[0]; }}
   if(L.cam){{ const [s,cx,cy]=kf(L.cam,t); $(L.id+'_cam').setAttribute('transform',`translate(540 960) scale(${{s}}) translate(${{-cx}} ${{-cy}})`); }} }}
 if(ISO){{ const I=ISO.I; const m=ease(cl((t-I.tilt[0])/(I.tilt[1]-I.tilt[0]),0,1)); const h=ease(cl((t-I.rise[0])/(I.rise[1]-I.rise[0]),0,1))*I.H;
   $('iso').style.opacity=cl((t-I.tilt[0]+0.05)/0.25,0,1);
   ISO.floors.forEach(({{r,p}})=>{{ const [x,y,w,hh]=r; p.setAttribute('points',[[x,y],[x+w,y],[x+w,y+hh],[x,y+hh]].map(q=>isoPt(q[0],q[1],0,m).join(',')).join(' ')); }});
   ISO.ws.forEach(({{w,p}})=>{{ const [x1,y1,x2,y2,z0,z1]=w; const za=Math.min(z0,h), zb=Math.min(z1,h); if(zb<=za+0.01&&!(z0==0&&h<0.02)){{ p.setAttribute('points',''); return; }}
     p.setAttribute('points',[isoPt(x1,y1,za,m),isoPt(x2,y2,za,m),isoPt(x2,y2,zb,m),isoPt(x1,y1,zb,m)].map(q=>q.join(',')).join(' ')); }});
 }}

 FIGS.forEach(({{f,g}})=>{{ const u=f.t1>f.t0?cl((t-f.t0)/(f.t1-f.t0),0,1):0; const [px,py,ang]=along(f.pts,f.ease?ease(u):u);
   const op=cl((t-f.fade[0])/(f.fade[1]-f.fade[0]),0,1)*(f.out?1-cl((t-f.out)/0.4,0,1):1);
   g.setAttribute('opacity',op);
   if(f.type==='top'){{ g.setAttribute('transform',`translate(${{px}} ${{py}}) rotate(${{ang*180/Math.PI+90}})`); }}
   else {{ const bob=(u>0&&u<1)?Math.abs(Math.sin(t*9))*f.s*0.12:0; g.setAttribute('transform',`translate(${{px}} ${{py-bob}}) scale(${{f.flip?-1:1}} 1)`); }} }});
 if(D.timer){{ const [a,b]=D.timer, tm=$('timer'); const sec=Math.floor(cl(t-a,0,b-a)); tm.textContent='0:'+String(sec).padStart(2,'0'); tm.style.opacity=cl((t-a)/0.3,0,1)*(1-cl((t-E)/0.4,0,1)); }}
 if(D.subs){{ let txt=''; for(const [a,b,w] of D.subs){{ if(t>=a&&t<b){{ txt=w; break; }} }} const el=$('subs'); el.innerHTML=txt?`<span>${{txt}}</span>`:''; el.style.opacity=1-cl((t-E)/0.3,0,1); }}
 const pp=ease(cl((t-(E-3))/3,0,1)); $('cam').style.transform=`scale(${{1+0.03*pp}})`;
 const ho=D.hook_out?1-cl((t-D.hook_out)/0.4,0,1):1; $('hook').style.opacity=ho; $('spec').style.opacity=ho*(1-cl((t-(E-2.4))/.6,0,1)); $('sub').style.opacity=Math.min(ho,1-cl((t-(E-2.4))/.6,0,1));
 $('end').style.opacity=cl((t-E)/.6,0,1);
 const lp=cl((t-E-.15)/1.3,0,1); const lk=$('link'),LL=lk.getTotalLength(); lk.style.strokeDasharray=LL; lk.style.strokeDashoffset=LL*(1-ease(cl(lp/.8,0,1)));
 $('lfill').style.opacity=cl((lp-.7)/.3,0,1); lk.style.opacity=1-cl((lp-.85)/.15,0,1);
 $('e1').style.opacity=cl((t-E-0.9)/.4,0,1); $('e2').style.opacity=cl((t-E-1.25)/.4,0,1); $('e3').style.opacity=cl((t-E-1.6)/.4,0,1);
}}; setT(0);
</script></body></html>"""

def render(job, outdir, stills=None):
    out = pathlib.Path(outdir); out.mkdir(exist_ok=True)
    name = job['name']; end = job['end']; dur = end + 3.6; N = int(FPS * dur)
    hp = out / f'{name}.html'; hp.write_text(build_html(job))
    fr = out / f'fr_{name}'; fr.mkdir(exist_ok=True)
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': W, 'height': H})
        errs = []; pg.on('pageerror', lambda e: errs.append(str(e)))
        pg.goto(hp.resolve().as_uri()); pg.wait_for_timeout(300)
        ts = stills if stills else [i / FPS for i in range(N)]
        for i, t in enumerate(ts):
            pg.evaluate(f"setT({t})"); pg.screenshot(path=str(fr / (f's_{t:05.2f}.png' if stills else f'{i:04d}.png')))
        b.close()
        if errs: print('ERR', name, errs[:2])
    if stills: return [str(fr / f's_{t:05.2f}.png') for t in stills]
    wav = str(out / f'{name}.wav')
    soundtrack.make(dur, draw=job.get('draw_window', (0.4, end - 0.8)), end=end, mood=job['mood'], bpm=job['bpm'], seed=job['seed'], out=wav)
    mp4 = str(out / f'{name}.mp4')
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-framerate', str(FPS), '-i', str(fr / '%04d.png'), '-i', wav, '-c:v', 'libx264', '-preset', 'veryfast',
                    '-pix_fmt', 'yuv420p', '-crf', '20', '-c:a', 'aac', '-b:a', '192k', '-shortest', '-movflags', '+faststart', mp4], check=True)
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', mp4, '-an', '-c:v', 'copy', str(out / f'{name}_silent.mp4')], check=True)
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', wav, '-c:a', 'libmp3lame', '-b:a', '192k', str(out / f'{name}_music.mp3')], check=True)
    shutil.rmtree(fr); pathlib.Path(wav).unlink()
    return mp4
