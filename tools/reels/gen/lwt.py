"""Line-weight reel: a flat floor plan (every line the same weight) gets its line weights, then the
camera drops into the drawing and walks through it in 3D. Heavy cut lines become walls.
Standard cited on screen: University of Memphis architecture drawing standards
(heavy = cut profiles, medium = edges below the cut plane, light = surface lines).
python3 gen/lw.py  -> out2/r_lwc_walk.mp4"""
import json, sys, pathlib, subprocess, zlib
sys.path.insert(0, '/home/claude/reels'); sys.path.insert(0, '/home/claude/reels/gen')
from playwright.sync_api import sync_playwright
import soundtrack, sfx
import vo as VOICE

W, H, FPS = 1080, 1920, 30

SCRIPT = [
    "Walk into this room. Which object is the tallest?",
    "Hard to tell? Flatten it into a plan. Now every outline is the same weight.",
    "The greater the drop from one surface to the next, the heavier the line.",
    "A rug drops one inch. A bookcase drops six feet.",
    "Now the plan reads in depth. Which outlines show the biggest drops?",
    "The tall ones. Bigger drop, heavier line.",
    "Same drawing. Different weights. That's what I do.",
    "Would your drawing hold up? Comment MOTION and I'll send you the details.",
]
CAPS = ["Which object is the tallest?", "Flat plan: every line the same.", "Bigger drop. Heavier line.",
        "Rug: 1 in. Bookcase: 6 ft.", "Which drops the most?",
        "The tall ones.", "Same drawing. Different weights.", "Would your drawing hold up?"]


def times(c, total):
    return dict(setup=0.0, hunt=c[1] - 0.14, reveal=c[2] + 0.8, stakes=c[3] - 0.10, door=c[4] - 0.12,
                turn=c[5] - 0.12, sell=c[6] - 0.14, cta=c[7] - 0.10, end=total + 0.55)


def build(c, total):
    T = times(c, total)
    html = HTML.replace('__DATA__', json.dumps(dict(T=T, dur=T['end'], caps=CAPS)))
    return html, T['end'], T


HTML = r"""<!doctype html><html><head><meta charset="utf-8"><style>
html,body{margin:0;width:1080px;height:1920px;background:#f6f4ee;overflow:hidden;font-family:Helvetica,Arial,sans-serif}
canvas{position:absolute;left:0;top:0}
.bd{position:absolute;white-space:nowrap;font:800 40px Helvetica;background:#fff;border:4px solid #161616;border-radius:10px;padding:4px 14px;opacity:0;transform-origin:50% 50%}
#tag{position:absolute;top:70px;left:0;width:1080px;text-align:center}
#tag span{display:inline-block;font:800 26px Helvetica;letter-spacing:3px;padding:8px 19px;border-radius:8px;background:#fff;border:2px solid #161616}
.ln{position:absolute;top:140px;left:50px;width:980px;text-align:center;font:900 62px/1.08 Helvetica;letter-spacing:-1.5px;color:#161616;opacity:0;text-shadow:0 0 18px #f6f4ee,0 0 8px #f6f4ee,0 0 3px #f6f4ee}
.ln.blue{color:#2a5fa8}
#cd{position:absolute;top:400px;left:0;width:1080px;text-align:center;font:900 200px Helvetica;color:#2a5fa8;opacity:0;text-shadow:0 0 22px #f6f4ee}
#leg{position:absolute;left:90px;width:900px;top:1500px;border:4px solid #161616;border-radius:16px;background:#fff;box-shadow:9px 9px 0 #161616;padding:20px 26px;opacity:0}
#leg div{display:flex;align-items:center;gap:22px;font:800 32px Helvetica;color:#161616;margin:8px 0}
#leg i{display:inline-block;width:150px;background:#161616;border-radius:3px}
#leg small{display:block;margin-top:8px;font:700 20px Helvetica;letter-spacing:3px;color:#666;text-align:center}
#cta{position:absolute;left:0;width:1080px;top:1520px;text-align:center;opacity:0}
#cta .a{display:inline-block;font:800 34px Helvetica;background:#fff;border:3px solid #161616;border-radius:14px;padding:16px 28px;box-shadow:8px 8px 0 #161616}
#cta .b{margin-top:30px;font:900 56px Helvetica;letter-spacing:2px;color:#1f9d63;text-shadow:0 0 14px #f6f4ee}
#cta .c{display:inline-block;margin-top:24px;font:800 30px Helvetica;background:#161616;color:#fff;border-radius:12px;padding:14px 28px}
#ser{position:absolute;bottom:34px;left:0;width:1080px;text-align:center;font:800 22px Helvetica;letter-spacing:4px;color:#bbb5a4}
#vig{position:absolute;inset:0;background:radial-gradient(ellipse at 50% 52%,rgba(0,0,0,0) 55%,rgba(20,20,20,.26) 100%)}
#flash{position:absolute;inset:0;background:#2a5fa8;opacity:0}
</style></head><body>
<div id="vig"></div>
<div id="tag"><span>LINE WEIGHT</span></div>
<div class="ln" id="l0"></div><div class="ln" id="l1"></div><div class="ln blue" id="l2"></div><div class="ln" id="l3"></div>
<div class="ln" id="l4"></div><div class="ln blue" id="l5"></div><div class="ln" id="l6"></div><div class="ln" id="l7"></div>
<div id="cd"></div>
<div id="leg"><div><i style="height:12px"></i>HEAVY &mdash; big drop</div><div><i style="height:6px"></i>MEDIUM &mdash; small drop</div><div><i style="height:2.5px;background:#8a8a8a"></i>LIGHT &mdash; flat on the floor</div><small>UNIV. OF MEMPHIS ARCHITECTURE DRAWING STANDARDS</small></div>
<div id="cta"><div class="a">I set line weights on your drawings &middot; from $30</div><br><div class="b">Comment MOTION</div><div class="c">Send this to whoever drew it</div></div>
<div id="ser"></div><div id="flash"></div>
<script type="importmap">{"imports":{"three":"/t3/node_modules/three/build/three.module.js","three/addons/":"/t3/node_modules/three/examples/jsm/"}}</script>
<script type="module">
import * as THREE from 'three';
import {LineSegments2} from 'three/addons/lines/LineSegments2.js';
import {LineSegmentsGeometry} from 'three/addons/lines/LineSegmentsGeometry.js';
import {LineMaterial} from 'three/addons/lines/LineMaterial.js';
const D=__DATA__, T=D.T, $=id=>document.getElementById(id);
const cl=(x,a,b)=>Math.max(a,Math.min(b,x)), P=(t,a,d)=>cl((t-a)/d,0,1);
const eo=x=>1-Math.pow(1-x,3), ss=x=>x*x*(3-2*x), lerp=(a,b,k)=>a+(b-a)*k;
const WT=0.6, WH=8, HW=20, HD=14, RES=new THREE.Vector2(1080,1920);
D.caps.forEach((s,i)=>{$('l'+i).innerHTML=s;}); $('ser').textContent='LINE WEIGHT 03';
const LT=[[T.setup+.02,T.hunt],[T.hunt+.06,T.reveal],[T.reveal+.06,T.stakes],[T.stakes+.06,T.door],[T.door+.08,T.turn],[T.turn+.07,T.sell],[T.sell+.1,T.cta],[T.cta,D.dur+.5]];
const DOORS=[{b:[15,18,HD,HD+WT]},{b:[6.7,7.3,3,6]},{b:[11,14,8.7,9.3]}];
const WALLS=[[-WT,HW+WT,-WT,0],[-WT,15,HD,HD+WT],[18,HW+WT,HD,HD+WT],[-WT,0,0,HD],[HW,HW+WT,0,HD],[6.7,7.3,0,3],[6.7,7.3,6,HD],[7.3,11,8.7,9.3],[14,HW,8.7,9.3]];
const FURN=[[10.5,17.5,3.4,7.4,0.08,'RUG'],[12.2,15.8,4.6,6.2,1.2,'LOW TABLE'],[9,17,0.4,1.4,6.0,'BOOKCASE'],[0.4,5.4,0.4,6.4,1.0,'PLATFORM BED'],[0.4,6.0,12.2,13.9,6.5,'WARDROBE'],[18.2,19.8,9.6,13.6,3.0,'COUNTER']];
const KEYS=[
 [0,16.5,16.0,5.4,-105,-5,75],
 [T.hunt-1.2,13.2,11.4,5.4,-90,-6,75],
 [T.hunt+.1,12.6,7.6,5.4,-90,-8,75],
 [T.hunt+1.8,12.2,9.0,13,-90,-50,70],
 [T.reveal-.9,10,7,60,-90,-90,42],
 [T.door+.1,10,7,60,-90,-90,42],
 [T.door+2.0,10,29,24,-90,-45,72],
 [T.turn+.8,8,29,24,-84,-45,72],
 [T.sell,10,30,25,-90,-45,72],
];
const ORB={cx:10,cy:7,R:25,ph0:Math.atan2(26-7,22-10),w:0.12,z:17};
function key(t){const K=KEYS; if(t<=K[0][0])return K[0].slice(1);
  for(let i=0;i<K.length-1;i++){ if(t<K[i+1][0]){const a=K[i],b=K[i+1],h=b[0]-a[0],u=(t-a[0])/h,pr=K[i-1]||a,nx=K[i+2]||b,out=[];
    for(let j=1;j<7;j++){const m0=((b[j]-pr[j])/Math.max(b[0]-pr[0],1e-3))*h,m1=((nx[j]-a[j])/Math.max(nx[0]-a[0],1e-3))*h,u2=u*u,u3=u2*u;
      out.push((2*u3-3*u2+1)*a[j]+(u3-2*u2+u)*m0+(-2*u3+3*u2)*b[j]+(u3-u2)*m1);} return out;}}
  return K[K.length-1].slice(1);}
function camAt(t){
  const F=KEYS[KEYS.length-1]; let [x,y,z,a,p,fov]=t<=F[0]?key(t):F.slice(1);
  const walk=ss(P(t,.3,.4))*(1-ss(P(t,T.hunt-.2,.5))); z+=0.05*Math.sin(t*7.2)*walk;
  if(t>T.sell){ const k=ss(P(t,T.sell,3.6)), ph=ORB.ph0+ORB.w*(t-T.sell), px=ORB.cx+ORB.R*Math.cos(ph), py=ORB.cy+ORB.R*Math.sin(ph);
    const fx=F[1],fy=F[2],fz=F[3],fa=F[4]; x=lerp(fx,px,k); y=lerp(fy,py,k); z=lerp(fz,ORB.z,k);
    const fwd=[fx+8*Math.cos(fa*Math.PI/180),fy+8*Math.sin(fa*Math.PI/180),fz+8*Math.tan(F[5]*Math.PI/180)], lk=[lerp(fwd[0],ORB.cx,k),lerp(fwd[1],ORB.cy,k),lerp(fwd[2],0.5,k)];
    let ta=Math.atan2(lk[1]-y,lk[0]-x)*180/Math.PI; while(ta-fa>180)ta-=360; while(ta-fa<-180)ta+=360;
    a=ta; p=-Math.atan2(z-lk[2],Math.hypot(lk[0]-x,lk[1]-y))*180/Math.PI; }
  return {x,y,z,a:a*Math.PI/180,p:p*Math.PI/180,fov};
}
/* ---------- three.js scene (plan y is flipped so the world is right-handed, z up) ---------- */
const R=new THREE.WebGLRenderer({antialias:true,preserveDrawingBuffer:true}); R.setPixelRatio(1); R.setSize(1080,1920); document.body.prepend(R.domElement);
const scene=new THREE.Scene(); scene.background=new THREE.Color('#f6f4ee'); scene.fog=new THREE.Fog('#f6f4ee',10,70);
scene.add(new THREE.AmbientLight(0xffffff,2.3)); const dl=new THREE.DirectionalLight(0xffffff,0.9); dl.position.set(-4,-6,12); scene.add(dl);
const cam=new THREE.PerspectiveCamera(75,1080/1920,0.3,300);
const PO={polygonOffset:true,polygonOffsetFactor:1,polygonOffsetUnits:1};
const lineMats=[];
function fat(arr,w,color){const g=new LineSegmentsGeometry(); g.setPositions(arr); const m=new LineMaterial({color,linewidth:w,resolution:RES}); lineMats.push(m); const l=new LineSegments2(g,m); return l;}
function loopTop(w,d,h){const x=w/2,y=d/2,z=h/2; return [-x,-y,z,x,-y,z, x,-y,z,x,y,z, x,y,z,-x,y,z, -x,y,z,-x,-y,z];}
function loopRest(w,d,h){const x=w/2,y=d/2,z=h/2,o=[]; const c=[[-x,-y],[x,-y],[x,y],[-x,y]];
  for(let i=0;i<4;i++){const a=c[i],b=c[(i+1)%4]; o.push(a[0],a[1],-z,b[0],b[1],-z); o.push(a[0],a[1],-z,a[0],a[1],z);} return o;}
function addBox(x0,x1,y0,y1,z0,z1,side,top){const w=x1-x0,d=y1-y0,h=z1-z0;
  const sm=new THREE.MeshLambertMaterial({color:side,...PO}), tm=new THREE.MeshBasicMaterial({color:top,...PO}), bm=new THREE.MeshBasicMaterial({color:side,...PO});
  const m=new THREE.Mesh(new THREE.BoxGeometry(w,d,h),[sm,sm,sm,sm,tm,bm]); m.position.set((x0+x1)/2,-(y0+y1)/2,(z0+z1)/2); scene.add(m); return {m,tm,sm,w,d,h,z0};}
const col=new THREE.Color();
// floor
const fl=new THREE.Mesh(new THREE.PlaneGeometry(HW,HD),new THREE.MeshBasicMaterial({color:'#fcfbf8',...PO})); fl.position.set(HW/2,-HD/2,0); scene.add(fl);
const fp=[]; const L=(x0,y0,x1,y1,z=.01)=>fp.push(x0,-y0,z,x1,-y1,z);
for(let x=8;x<HW;x+=1)L(x,0,x,8.7); for(let y=1;y<HD;y+=2)L(0,y,6.7,y); for(let x=1;x<6.7;x+=2)L(x,0,x,HD);
for(let y=10;y<HD;y+=2)L(7.3,y,HW,y); for(let x=9;x<HW;x+=2)L(x,9.3,x,HD);
const floorLines=fat(fp,3.6,'#161616'); scene.add(floorLines);
// door swings
const dp=[]; const arc=(cx,cy,r,a0,a1)=>{let pv=null;for(let i=0;i<=24;i++){const a=a0+(a1-a0)*i/24,p=[cx+r*Math.cos(a),-(cy+r*Math.sin(a)),.03]; if(pv)dp.push(...pv,...p); pv=p;}};
arc(15,HD,3,-Math.PI/2,0); dp.push(15,-HD,.03,15,-(HD-3),.03);
arc(7,3,3,0,Math.PI/2); dp.push(7,-3,.03,10,-3,.03);
arc(11,9,3,0,Math.PI/2); dp.push(11,-9,.03,14,-9,.03);
const doorLines=fat(dp,3.6,'#161616'); scene.add(doorLines);
// walls (+ headers over doors)
const walls=[], capEdges=[];
for(const [x0,x1,y0,y1] of WALLS){const near=(y0>=HD-.1||x0>=HW-.1); const b=addBox(x0,x1,y0,y1,0,WH,'#e9e6db','#fcfbf8'); const e=fat(loopTop(b.w,b.d,b.h),3.6,'#161616'); b.m.add(e); walls.push({...b,near,wipe:x0/HW,e,hdr:false});}
for(const d of DOORS){const bb=d.b, near=bb[2]>=HD-.1; const b=addBox(bb[0],bb[1],bb[2],bb[3],6.8,WH,'#e9e6db','#fcfbf8'); const e=fat(loopTop(b.w,b.d,b.h),3.6,'#161616'); b.m.add(e); walls.push({...b,near,wipe:bb[0]/HW,e,hdr:true});}
// furniture
const furn=[];
for(const [x0,x1,y0,y1,h,lab] of FURN){const zb=lab==='LOW TABLE'?.08:0; const b=addBox(x0,x1,y0,y1,zb,zb+h,'#dfdbcf','#fcfbf8');
  const et=fat(loopTop(b.w,b.d,b.h),3.6,'#161616'); b.m.add(et); const er=fat(loopRest(b.w,b.d,b.h),2.2,'#161616'); b.m.add(er); furn.push({...b,h,et,er});}
// windows (inside faces)
function pane(cx,cy,cz,w,h,color,east){const g=new THREE.PlaneGeometry(w,h); g.rotateX(Math.PI/2); if(east) g.rotateZ(Math.PI/2);
  const m=new THREE.Mesh(g,new THREE.MeshBasicMaterial({color,side:THREE.DoubleSide,polygonOffset:true,polygonOffsetFactor:-2,polygonOffsetUnits:-2})); m.position.set(cx,-cy,cz); scene.add(m);}
function winN(x0,x1,z0,z1){const e=.25,cx=(x0+x1)/2,cz=(z0+z1)/2; pane(cx,-.03,cz,x1-x0,z1-z0,'#161616'); pane(cx,-.05,cz,x1-x0-2*e,z1-z0-2*e,'#dbe6ef'); pane(cx,-.07,cz,.08,z1-z0-2*e,'#8a8a8a');}
winN(1.5,4.5,3.4,6.6); winN(11,16,3.4,6.6);
pane(HW-.03,4.5,5,3,3.2,'#161616',true); pane(HW-.05,4.5,5,3-.5,3.2-.5,'#dbe6ef',true);
/* ---------- HUD badges (DOM, positioned from 3D points) ---------- */
const BD={}; function badge(id,p3,txt,color,alpha,fs=1){let e=BD[id]; if(!e){e=document.createElement('div'); e.className='bd'; document.body.appendChild(e); BD[id]=e;}
  if(alpha<=.01){e.style.opacity=0;return;}
  const v=new THREE.Vector3(p3[0],-p3[1],p3[2]); const dv=v.clone().sub(cam.position); const f=new THREE.Vector3(); cam.getWorldDirection(f); const depth=dv.dot(f);
  if(depth<.5){e.style.opacity=0;return;} const pr=v.clone().project(cam); const sx=(pr.x*.5+.5)*1080, sy=(-pr.y*.5+.5)*1920;
  const focal=960/Math.tan(cam.fov*Math.PI/360); const k=cl(8*(focal/820)/depth,.55,1.5)*fs;
  e.textContent=txt; e.style.color=color; e.style.borderColor=color; e.style.left=sx+'px'; e.style.top=sy+'px'; e.style.transform=`translate(-50%,-50%) scale(${k.toFixed(3)})`; e.style.opacity=alpha;}
function setT(t){
  const c=camAt(t); const a=-c.a,p=c.p;
  const f=new THREE.Vector3(Math.cos(p)*Math.cos(a),Math.cos(p)*Math.sin(a),Math.sin(p)), r=new THREE.Vector3(Math.sin(a),-Math.cos(a),0), u=new THREE.Vector3().crossVectors(r,f);
  cam.position.set(c.x,-c.y,c.z); cam.quaternion.setFromRotationMatrix(new THREE.Matrix4().makeBasis(r,u,f.clone().negate())); cam.fov=c.fov; cam.updateProjectionMatrix(); cam.updateMatrixWorld(true);
  scene.fog.near=Math.max(10,c.z+4); scene.fog.far=scene.fog.near+60;
  const wk=ss(P(t,T.reveal,1.4)), cutK=ss(P(t,T.door+.1,1.6)), nearF=1-0.94*cutK;
  const FW=lerp(3.6,4.6,wk), SW=lerp(3.6,1.5,wk);
  floorLines.material.linewidth=SW; floorLines.material.color.set(wk>.5?'#9a9a8e':'#161616'); doorLines.material.linewidth=FW;
  const g=Math.round(lerp(252,22,1));
  for(const w of walls){const k=cl((wk*1.5)-w.wipe*0.5,0,1), gg=Math.round(lerp(252,22,ss(k))); w.tm.color.set(`rgb(${gg},${gg},${gg})`); w.e.material.linewidth=lerp(3.6,2.5,wk);
    const sc=w.near?nearF:1; if(w.hdr){w.m.visible=!(w.near&&nearF<.5); w.m.scale.set(1,1,1);} else {w.m.scale.set(1,1,sc); w.m.position.z=w.z0+w.h*sc/2;}}
  for(const q of furn){q.tm.color.set(wk>.5?'#e4e0d4':'#fcfbf8'); q.et.material.linewidth=lerp(3.6,Math.min(8.5,1.0+q.h*1.15),wk);}
  // in-world tags
  const tgA=ss(P(t,T.door+.5,.5))*(1-ss(P(t,T.turn-.5,.4))), tgB=ss(P(t,T.turn+.5,.5))*(1-ss(P(t,T.sell-.2,.4)));
  badge('A',[13,1.0,7.4],'BIGGEST DROP · 6′','#161616',tgA); badge('B',[3.0,3.5,1.9],'SMALL DROP · 12″','#2a5fa8',tgB);
  const lb=ss(P(t,T.stakes,.5))*(1-ss(P(t,T.door,.5)));
  badge('1',[12.2,7.0,.1],'RUG · 1″','#161616',lb); badge('2',[14,5.4,.1],'LOW TABLE · 14″','#161616',lb); badge('3',[13,0.9,.1],'BOOKCASE · 6′','#161616',lb);
  badge('4',[2.9,3.4,.1],'BED · 12″','#161616',lb); badge('5',[3.2,13.0,.1],'WARDROBE · 6′6″','#161616',lb); badge('6',[18.8,11.6,.1],'COUNTER · 3′','#161616',lb);
  R.render(scene,cam);
  for(let i=0;i<8;i++){const [a,b]=LT[i],d=$('l'+i),q=P(t,a,.22),o=i===7?1:1-P(t,b-.2,.18);d.style.opacity=q*o;d.style.transform='translateY('+((1-eo(q))*30).toFixed(1)+'px)';}
  const cd=$('cd'); if(t>.9&&t<T.hunt-.1){const r=T.hunt-1.0,n=Math.max(1,Math.ceil(3*(1-(t-.9)/r)));cd.textContent=n;const fr=((t-.9)/r*3)%1;cd.style.opacity=1-fr*.7;cd.style.transform='scale('+(1.12-.12*fr)+')';}else cd.style.opacity=0;
  $('leg').style.opacity=P(t,T.reveal+.6,.35)*(1-P(t,T.stakes-.2,.3));
  $('cta').style.opacity=P(t,T.cta,.3);
  $('flash').style.opacity=.32*(1-cl((t-T.reveal)/.1,0,1))*(t>=T.reveal?1:0);
}
window.setT=setT; setT(0); window.ready=true;
</script></body></html>"""


import http.server, socketserver, threading, functools
class _Q(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass
_srv = socketserver.TCPServer(('127.0.0.1', 0), functools.partial(_Q, directory='/home/claude/reels')); PORT = _srv.server_address[1]
threading.Thread(target=_srv.serve_forever, daemon=True).start()


def render(outdir='/home/claude/reels/out2', stills=None, name='r_lwt_walk'):
    out = pathlib.Path(outdir); out.mkdir(exist_ok=True)
    narration, cues, total = VOICE.narrate(SCRIPT)
    html, dur, T = build(cues, total)
    hp = out / f'{name}.html'; hp.write_text(html)
    fr = out / f'fr_{name}'; fr.mkdir(exist_ok=True); N = int(FPS * dur)
    with sync_playwright() as pw:
        b = pw.chromium.launch(args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist']); pg = b.new_page(viewport={'width': W, 'height': H}); errs = []
        pg.on('pageerror', lambda e: (errs.append(str(e)), print('PE', str(e)[:300]))); pg.on('console', lambda m: print('C', m.text) if m.type in ('error', 'warning') else None); pg.on('response', lambda r: print('R', r.status, r.url) if r.status >= 400 else None)
        pg.goto(f'http://127.0.0.1:{PORT}/{hp.relative_to('/home/claude/reels')}'); pg.wait_for_function('window.ready===true', timeout=30000)
        ts = stills or [i / FPS for i in range(N)]
        for i, t in enumerate(ts):
            pg.evaluate(f'setT({t})'); pg.screenshot(path=str(fr / (f's_{t:05.2f}.png' if stills else f'{i:04d}.png')))
        b.close()
        if errs: print('ERR', errs[:3])
    if stills: return T, [str(fr / f's_{t:05.2f}.png') for t in stills]
    wav = str(out / f'{name}.wav')
    soundtrack.make(dur, draw=(0.2, 1.1), end=dur, mood='bright', bpm=100, seed=zlib.crc32(name.encode()) % 999, out=wav, pen=False, beat=True)
    ev = [(0.05, 'whoosh')]; tt = 0.9
    while tt < T['hunt'] - 0.3: ev.append((tt, 'tick')); tt += 1.0
    ev += [(T['reveal'] - 0.5, 'riser'), (T['reveal'], 'hit'), (T['hunt'], 'whoosh'), (T['stakes'], 'whoosh'), (T['door'] + 0.6, 'whoosh'),
           (T['door'], 'whoosh'), (T['turn'], 'whoosh'), (T['turn'] + 0.1, 'chime'), (T['sell'], 'whoosh')]
    sfx.add(wav, ev)
    VOICE.lay_under(wav, narration)
    mp4 = str(out / f'{name}.mp4')
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-framerate', str(FPS), '-i', str(fr / '%04d.png'), '-i', wav, '-c:v', 'libx264',
                    '-preset', 'veryfast', '-pix_fmt', 'yuv420p', '-crf', '20', '-c:a', 'aac', '-b:a', '192k', '-shortest', '-movflags', '+faststart', mp4], check=True)
    return mp4


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'stills':
        T, fs = render('/home/claude/reels/outT', stills=[float(x) for x in sys.argv[2].split(',')], name='r_lwt_walk')
        print({k: round(v, 1) for k, v in T.items()}); print('\n'.join(fs))
    else:
        print(render())
