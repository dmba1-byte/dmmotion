import sys,re,zlib,pathlib,subprocess
sys.path.insert(0,'/home/claude/reels')
from playwright.sync_api import sync_playwright
from gen import elevs as EV
from gen.engine2 import STYLES, prefix_ids
st=STYLES['blueprint']; svg,o,l=EV.make('craftsman',zlib.crc32(b'r1102_lw_2am')%9999,st)
w=prefix_ids(svg,'w_'); u=re.sub(r'stroke-width="[\d.]+"','stroke-width="0.9"',prefix_ids(svg,'u_'))
with sync_playwright() as pw:
    b=pw.chromium.launch(); pg=b.new_page(); pg.set_content('<svg id=s width=1080 height=1920 viewBox="0 0 1080 1920">'+w+'</svg>')
    bb=pg.evaluate("(()=>{let x0=1e9,y0=1e9,x1=-1e9,y1=-1e9;for(const e of document.querySelectorAll('#s > g')){if(/tint|shade/.test(e.id))continue;const r=e.getBBox();if(!r.width)continue;x0=Math.min(x0,r.x);y0=Math.min(y0,r.y);x1=Math.max(x1,r.x+r.width);y1=Math.max(y1,r.y+r.height)}return [x0,y0,x1,y1]})()"); b.close()
pad=24; vb=f'{bb[0]-pad} {bb[1]-pad} {bb[2]-bb[0]+2*pad} {bb[3]-bb[1]+2*pad}'; print('VB',vb)
html=f'''<!doctype html><meta charset="utf-8"><style>
html,body{{margin:0;width:1080px;height:1350px;background:#0e2a47;color:#f3ecd8;font-family:Helvetica,Arial,sans-serif;overflow:hidden}}
.bg{{position:absolute;inset:0;background:radial-gradient(circle at 25% 15%,rgba(46,124,214,.6),transparent 45%),radial-gradient(circle at 80% 80%,rgba(22,80,160,.55),transparent 50%),linear-gradient(rgba(160,200,255,.08) 1px,transparent 1px) 0 0/54px 54px,linear-gradient(90deg,rgba(160,200,255,.08) 1px,transparent 1px) 0 0/54px 54px}}
.v{{position:absolute;inset:0;background:radial-gradient(ellipse at 50% 50%,transparent 55%,rgba(0,0,0,.55))}}
h1{{position:absolute;left:70px;right:70px;top:62px;margin:0;font-size:68px;line-height:1.04;letter-spacing:-1.5px}}
.tag{{position:absolute;left:70px;font:700 26px Menlo,monospace;letter-spacing:3px;color:#9fc0e6}}
.a{{position:absolute;left:90px;width:900px;height:400px}} .a svg{{width:100%;height:100%;display:block}}
.cta{{position:absolute;left:70px;right:70px;bottom:56px;display:flex;justify-content:space-between;align-items:center}}
.cta b{{font-size:40px}} .cta span{{background:#f3ecd8;color:#0c2745;font-weight:700;font-size:34px;padding:18px 30px;border-radius:14px}}
</style><div class="bg"></div><div class="v"></div>
<h1>The design is done.<br>Now the lines have to look it.</h1>
<div class="tag" style="top:262px">BEFORE · EVERY LINE THE SAME</div>
<div class="a" style="top:292px;opacity:.7"><svg viewBox="{vb}">{u}</svg></div>
<div class="tag" style="top:722px">AFTER · PROFILE · DETAIL · HATCH</div>
<div class="a" style="top:752px"><svg viewBox="{vb}">{w}</svg></div>
<div class="cta"><b>Line weights from $30</b><span>Message me your file</span></div>'''
p=pathlib.Path('stills/still_1102_lw.html'); p.write_text(html)
with sync_playwright() as pw:
    b=pw.chromium.launch(); pg=b.new_page(viewport={'width':1080,'height':1350}); pg.goto(p.resolve().as_uri()); pg.wait_for_timeout(300)
    pg.screenshot(path='stills/still_1102_lw.png'); b.close()
