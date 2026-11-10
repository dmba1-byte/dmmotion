# Direction rule check: every character must face the way it travels.
import sys,json
from playwright.sync_api import sync_playwright
html=sys.argv[1];dur=float(sys.argv[2])
inject="""
window.TRACK=[];const _person=person;person=function(P,ox,oy,look,front,flip){const r=_person(P,ox,oy,look,front,flip);window.TRACK.push({k:(look&&look.top)||'kit',x:Math.round(ox),flip:!!flip});return r};
const _dk=drawKitY;drawKitY=function(P,ox,oy){window.TRACK.push({k:'kit',x:Math.round(ox),flip:false});return _dk(P,ox,oy)};0;
"""
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page(viewport={'width':1080,'height':1920})
    pg.goto('file://'+html);pg.wait_for_function('window.READY===true',timeout=8000)
    pg.evaluate(inject)
    prev={};bad=[]
    n=int(dur*10)
    for i in range(n):
        t=i/10
        pg.evaluate('window.TRACK=[]');pg.evaluate(f'frame({round(t*30)})')
        tr=pg.evaluate('window.TRACK')
        cur={}
        for e in tr: cur[e['k']]=e
        for k,e in cur.items():
            if k in prev and abs(t-prev[k]['t'])<0.15:
                dx=e['x']-prev[k]['x']
                if abs(dx)>=1:
                    facing=-1 if e['flip'] else 1
                    if dx*facing<0: bad.append((round(t,1),k,dx,'flip' if e['flip'] else 'right'))
        for k,e in cur.items(): prev[k]=dict(e,t=t)
    b.close()
print('violations:',len(bad))
for x in bad[:40]: print(x)
