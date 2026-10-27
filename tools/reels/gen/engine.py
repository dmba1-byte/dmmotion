import re, json, pathlib, subprocess, shutil
from playwright.sync_api import sync_playwright
import sys; sys.path.insert(0, '/home/claude/reels')
import soundtrack
W, H, FPS = 1080, 1920, 30
LOGO_D = re.search(r'<path d="([^"]+)"', open('/home/claude/logo/DM_logo_mark-black.svg').read()).group(1)
STYLES = {
  'light':     dict(bg='#ffffff', ink='#1f1f1f', sub='#8a8a8a', tint='#f1efe9', tint2='#e6e3dc', lawn='#eef0e8', road='#ecebe7', hook='#1f1f1f', hook2='#6b6b6b'),
  'blueprint': dict(bg='#0e2a47', ink='#eaf2ff', sub='#8fb0d6', tint='#12365a', tint2='#173f68', lawn='#113353', road='#0f2f4d', hook='#ffffff', hook2='#9fc0e6'),
  'dark':      dict(bg='#141414', ink='#f2f2f2', sub='#8c8c8c', tint='#1e1e1e', tint2='#272727', lawn='#1b1e1a', road='#1d1d1d', hook='#ffffff', hook2='#9a9a9a'),
}
def sched_for(order, kind):
    base = {'plan': {'walls-ext': (0.4, 2.8, 'seq'), 'walls-int': (2.6, 4.6, 'seq'), 'openings': (4.4, 6.4, 0.35), 'fixtures': (6.2, 9.0, 0.3), 'labels': (8.8, 10.0, 0.4), 'dims': (9.8, 10.8, 0.4)},
            'elev': {'grade': (0.4, 1.6, 'seq'), 'walls': (1.4, 2.2, 'seq'), 'roof': (2.0, 4.8, 0.35), 'siding': (4.4, 6.4, 0.3), 'openings': (6.0, 8.6, 0.35), 'dims': (8.4, 9.6, 0.4), 'labels': (9.2, 10.2, 0.4)},
            'site': {'lot': (0.4, 2.0, 'seq'), 'setbacks': (1.8, 3.2, 0.12), 'street': (2.6, 3.8, 0.4), 'house': (3.6, 5.6, 0.35), 'hardscape': (5.2, 6.8, 0.35), 'trees': (6.4, 8.6, 0.3), 'north': (8.2, 8.8, 0.4), 'labels': (8.6, 9.8, 0.4), 'dims': (9.4, 10.4, 0.4)}}[kind]
    tint = {'plan': (8.4, 9.6), 'elev': (8.0, 9.2), 'site': (7.6, 8.8)}[kind]
    return {k: base[k] for k in order if k in base}, tint
def build_html(svg, sched, tint, st, hook, sub, cta, end=11.6):
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>
html,body{{margin:0;width:{W}px;height:{H}px;background:{st['bg']};overflow:hidden;font-family:Helvetica,Arial,sans-serif}}
svg{{position:absolute;left:0;top:0}} .t{{position:absolute;left:60px;right:60px;text-align:center}}
#hook{{top:250px;font-size:64px;font-weight:700;letter-spacing:-1px;line-height:1.1;color:{st['hook']}}} #sub{{top:420px;font-size:34px;color:{st['hook2']}}}
#end{{position:absolute;inset:0;background:#141414;opacity:0}}
#e1{{top:820px;font-size:70px;font-weight:700;color:#fff;letter-spacing:-1px;opacity:0}} #e2{{top:930px;font-size:38px;color:#bdbdbd;opacity:0;line-height:1.35}}
#e3{{top:1140px;opacity:0}} #e3 span{{display:inline-block;background:#fff;color:#141414;font-size:40px;font-weight:700;padding:24px 44px;border-radius:14px}}
</style></head><body>
<div class="t" id="hook">{hook}</div><div class="t" id="sub">{sub}</div>
<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}"><g id="cam" style="transform-origin:540px 960px">{svg}</g></svg>
<div id="end"></div>
<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}"><g transform="translate(435 470) scale(0.68)"><svg viewBox="-2.18 -2.45 309.7 309.7" width="309.7" height="309.7" overflow="visible">
<path id="lfill" d="{LOGO_D}" fill="#fff" opacity="0"/><path id="link" d="{LOGO_D}" fill="none" stroke="#fff" stroke-width="5" stroke-linejoin="round"/></svg></g></svg>
<div class="t" id="e1">Your drawing, in motion.</div><div class="t" id="e2">Send your plan, elevation or logo.<br>Clip back in 5 business days.</div>
<div class="t" id="e3"><span>{cta}</span></div>
<script>
const SCHED={json.dumps(sched)}, TINT={json.dumps(tint)}, E={end};
const ease=t=>t<.5?2*t*t:1-Math.pow(-2*t+2,2)/2, cl=(x,a,b)=>Math.max(a,Math.min(b,x)), $=i=>document.getElementById(i);
const items=[];
for(const [id,[s,e,d]] of Object.entries(SCHED)){{
 const g=$(id); if(!g) continue;
 const els=[...g.querySelectorAll('line,path,rect,circle,text')]; const n=els.length, span=d==='seq'?0:Math.max(0,(e-s)-d);
 let lens=[],tot=0; if(d==='seq'){{lens=els.map(el=>{{try{{return el.getTotalLength()}}catch(x){{return 0}}}});tot=lens.reduce((a,b)=>a+b,0)||1}}
 let cum=0;
 els.forEach((el,i)=>{{let t0,dd; if(d==='seq'){{t0=s+(e-s)*cum/tot;dd=Math.max(0.001,(e-s)*lens[i]/tot);cum+=lens[i]}}else{{t0=s+span*(n>1?i/(n-1):0);dd=d}}
  const isT=el.tagName==='text', f=el.getAttribute('fill')&&el.getAttribute('fill')!=='none'; let L=0;
  if(!isT){{try{{L=el.getTotalLength()}}catch(x){{}}}} if(!isT&&L>0){{el.style.strokeDasharray=L;el.style.strokeDashoffset=L}}
  if(f&&!isT)el.style.fillOpacity=0; if(isT)el.style.opacity=0; items.push({{el,t0,d:dd,L,isT,f,seq:d==='seq'}})}});
}}
const tints=$('tint')?[...$('tint').children]:[]; tints.forEach(t=>t.style.opacity=0);
const lk=$('link'),LL=lk.getTotalLength(); lk.style.strokeDasharray=LL;
window.setT=t=>{{
 for(const it of items){{const p=cl((t-it.t0)/it.d,0,1); if(it.isT)it.el.style.opacity=p; else{{
  if(it.L>0)it.el.style.strokeDashoffset=it.L*(1-(it.seq?p:ease(p))); if(it.f)it.el.style.fillOpacity=cl((t-it.t0-it.d*.6)/(it.d*.6),0,1)}}}}
 tints.forEach(x=>x.style.opacity=cl((t-TINT[0])/(TINT[1]-TINT[0]),0,1));
 const pp=ease(cl((t-(E-3))/3,0,1)); $('cam').style.transform=`scale(${{1+0.035*pp}})`;
 $('sub').style.opacity=1-cl((t-(E-2.4))/.6,0,1);
 $('end').style.opacity=cl((t-E)/.6,0,1);
 const lp=cl((t-E-.4)/1.8,0,1); lk.style.strokeDashoffset=LL*(1-ease(cl(lp/.8,0,1)));
 $('lfill').style.opacity=cl((lp-.7)/.3,0,1); lk.style.opacity=1-cl((lp-.85)/.15,0,1);
 $('e1').style.opacity=cl((t-E-1.6)/.5,0,1); $('e2').style.opacity=cl((t-E-2.1)/.5,0,1); $('e3').style.opacity=cl((t-E-2.6)/.5,0,1);
}}; setT(0);
</script></body></html>"""
def render(job, outdir='out', stills=None):
    out = pathlib.Path(outdir); out.mkdir(exist_ok=True)
    name = job['name']; end = job.get('end', 11.6); dur = end + 4.6; N = int(FPS * dur)
    html = build_html(job['svg'], job['sched'], job['tint'], STYLES[job['style']], job['hook'], job['sub'], job['cta'], end)
    hp = out / f'{name}.html'; hp.write_text(html)
    fr = out / f'fr_{name}'; fr.mkdir(exist_ok=True)
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': W, 'height': H})
        errs = []; pg.on('pageerror', lambda e: errs.append(str(e)))
        pg.goto(hp.resolve().as_uri()); pg.wait_for_timeout(300)
        ts = stills if stills else [i / FPS for i in range(N)]
        for i, t in enumerate(ts):
            pg.evaluate(f"setT({t})"); pg.screenshot(path=str(fr / (f'{i:04d}.png' if not stills else f's_{t:05.2f}.png')))
        b.close()
        if errs: print('ERR', name, errs[:2])
    if stills: return [str(fr / f's_{t:05.2f}.png') for t in stills]
    wav = str(out / f'{name}.wav')
    soundtrack.make(dur, draw=(0.4, end - 0.8), end=end, mood=job['mood'], bpm=job['bpm'], seed=job['seed'], out=wav)
    mp4 = str(out / f'{name}.mp4')
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-framerate', str(FPS), '-i', str(fr / '%04d.png'), '-i', wav, '-c:v', 'libx264', '-preset', 'veryfast',
                    '-pix_fmt', 'yuv420p', '-crf', '20', '-c:a', 'aac', '-b:a', '192k', '-shortest', '-movflags', '+faststart', mp4], check=True)
    # silent copy for voiced compositions
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', mp4, '-an', '-c:v', 'copy', str(out / f'{name}_silent.mp4')], check=True)
    ffmpeg_mp3 = str(out / f'{name}_music.mp3')
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', wav, '-c:a', 'libmp3lame', '-b:a', '192k', ffmpeg_mp3], check=True)
    shutil.rmtree(fr); pathlib.Path(wav).unlink()
    return mp4
