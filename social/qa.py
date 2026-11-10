# Pre-render gate. Fails the reel if any set-in-stone rule is broken.
import sys,json
from playwright.sync_api import sync_playwright
html=sys.argv[1];dur=float(sys.argv[2]);cuts=[float(x) for x in sys.argv[3].split(',')] if len(sys.argv)>3 else []
near=lambda t:any(abs(t-c)<0.16 for c in cuts)
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page(viewport={'width':1080,'height':1920});errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto('file://'+html);pg.wait_for_function('window.READY===true',timeout=8000)
    prev={};still={};bad=[];shots={};n=int(dur*10)
    for i in range(n):
        t=i/10;pg.evaluate(f'frame({round(t*30)})');q=pg.evaluate('window.QA')
        shots[q.get('shot','')]=shots.get(q.get('shot',''),0)+1
        cur={c['k']:c for c in q['chars']}
        for k,c in cur.items():
            # 1 facing
            if k in prev and abs(t-prev[k]['t'])<0.15 and not near(t) and not c.get('fb'):
                dx=c['x']-prev[k]['x']
                if abs(dx)>=1 and dx*(-1 if c['flip'] else 1)<0: bad.append((t,'FACING',k,dx))
            # 4 furniture overlap
            if not c.get('ok'):
                for s in q['solids']:
                    if s['x0']-5<c['cx']<s['x1']+5: bad.append((t,'IN FURNITURE',k,s['name']))
            # 7 idle life
            key=(c['sig'],c['x'])
            if k in still and still[k][0]==key and not near(t):
                if t-still[k][1]>1.6: bad.append((t,'FROZEN',k,round(t-still[k][1],1)))
            else: still[k]=(key,t)
        for k in list(still):
            if k not in cur: del still[k]
        for k,c in cur.items(): prev[k]=dict(c,t=t)
    b.close()
kinds=[k for k in shots if k]
if len(kinds)<5: bad.append((0,'VANTAGE','only %d shot types: %s'%(len(kinds),kinds),''))
if shots.get('closeup',0)<2: bad.append((0,'VANTAGE','fewer than 2 face close-up beats',''))
for e in errs: bad.append((0,'JS ERROR',e,''))
seen=set();out=[]
for x in bad:
    key=(x[1],x[2],x[3] if x[1]!='FROZEN' else '')
    if key in seen: continue
    seen.add(key);out.append(x)
print('shot types:',{k:round(v/10,1) for k,v in shots.items()})
print('FAIL' if out else 'PASS',len(out))
for x in out[:40]: print(x)
sys.exit(1 if out else 0)
