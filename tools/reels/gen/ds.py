"""Door-swing reel: which door fails inspection? Flat plan with swing arcs, then the camera drops into 3D where each door
opens on its hinge. ADA 603.2.3: doors shall not swing into the clear floor space required for any fixture.
python3 gen/ds.py -> out2/r_ds_walk.mp4   (stills: python3 gen/ds.py stills t1,t2)"""
import json, sys, pathlib, subprocess, zlib
sys.path.insert(0, '/home/claude/reels'); sys.path.insert(0, '/home/claude/reels/gen')
from playwright.sync_api import sync_playwright
import soundtrack, sfx
import vo as VOICE

W, H, FPS = 1080, 1920, 30

SCRIPT = [
    "One of these three doors fails inspection. Which one? Take a guess.",
    "Hard to tell? Flatten it into a plan. Every door draws its swing.",
    "A door can't swing into the clear floor space a fixture needs.",
    "Now watch them open. The office door swings clear. So does storage.",
    "The restroom door swings right into the sink's clear floor space.",
    "Fail. A D A six oh three point two point three.",
    "Move the sink, and the same door passes.",
    "I animate plans like this, so the problem shows up before the inspector does. Comment MOTION.",
]
CAPS = ["Which door fails inspection?", "Flat plan: every door draws its swing.", "A swing can't enter a fixture's clear space.",
        "Office: clear. Storage: clear.", "Restroom: swings into the sink's space.",
        "ADA 603.2.3: fail.", "Move the sink. Same door passes.", "Would your plan pass?"]


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
.ln.blue{color:#1f8a57}
.ln.red{color:#b02a22}
#cd{position:absolute;top:400px;left:0;width:1080px;text-align:center;font:900 200px Helvetica;color:#1f8a57;opacity:0;text-shadow:0 0 22px #f6f4ee}
#leg{position:absolute;left:90px;width:900px;top:1500px;border:4px solid #161616;border-radius:16px;background:#fff;box-shadow:9px 9px 0 #161616;padding:20px 26px;opacity:0}
#leg div{display:flex;align-items:center;gap:22px;font:800 32px Helvetica;color:#161616;margin:8px 0}
#leg .sw{display:inline-block;width:70px;height:42px;border-radius:6px;flex:none}
#leg small{display:block;margin-top:8px;font:700 20px Helvetica;letter-spacing:3px;color:#666;text-align:center}
#cta{position:absolute;left:0;width:1080px;top:1520px;text-align:center;opacity:0}
#cta .a{display:inline-block;font:800 34px Helvetica;background:#fff;border:3px solid #161616;border-radius:14px;padding:16px 28px;box-shadow:8px 8px 0 #161616}
#cta .b{margin-top:30px;font:900 56px Helvetica;letter-spacing:2px;color:#1f9d63;text-shadow:0 0 14px #f6f4ee}
#cta .c{display:inline-block;margin-top:24px;font:800 30px Helvetica;background:#161616;color:#fff;border-radius:12px;padding:14px 28px}
#ser{position:absolute;bottom:34px;left:0;width:1080px;text-align:center;font:800 22px Helvetica;letter-spacing:4px;color:#bbb5a4}
#vig{position:absolute;inset:0;background:radial-gradient(ellipse at 50% 52%,rgba(0,0,0,0) 55%,rgba(20,20,20,.26) 100%)}
#flash{position:absolute;inset:0;background:#1f9d63;opacity:0}
</style></head><body>
<div id="vig"></div>
<div id="tag"><span>DOOR SWING</span></div>
<div class="ln" id="l0"></div><div class="ln" id="l1"></div><div class="ln blue" id="l2"></div><div class="ln" id="l3"></div>
<div class="ln" id="l4"></div><div class="ln red" id="l5"></div><div class="ln blue" id="l6"></div><div class="ln" id="l7"></div>
<div id="cd"></div>
<div id="leg"><div><b class="sw" style="background:#d2d5cf"></b>Door swing</div><div><b class="sw" style="background:#d9f0e2;border:4px solid #1f9d63;box-sizing:border-box"></b>Fixture clear floor space · 30 × 48 in</div><small>ADA 603.2.3 · DOORS SHALL NOT SWING INTO IT</small></div>
<div id="cta"><div class="a">I animate plans like this &middot; from $450</div><br><div class="b">Comment MOTION</div><div class="c">Send this to whoever drew it</div></div>
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
D.caps.forEach((s,i)=>{$('l'+i).innerHTML=s;}); $('ser').textContent='DOOR SWING 01';
const LT=[[T.setup+.02,T.hunt],[T.hunt+.06,T.reveal],[T.reveal+.06,T.stakes],[T.stakes+.06,T.door],[T.door+.08,T.turn],[T.turn+.07,T.sell],[T.sell+.1,T.cta],[T.cta,D.dur+.5]];
const HY0=4.4, HY1=5.0, PY=4.925, LD=2.95;             // hall wall y-range; hinge pin y; leaf length
const OPN=[[5.5,8.5],[9.8,12.8],[14.6,17.6]];            // office, storage, restroom openings (hall wall)
const PIN=[5.575,9.875,17.525], HE=[0,0,1];              // hinge pin x; 1 = hinge on east jamb
const DOORS=OPN.map(o=>({b:[o[0],o[1],HY0,HY1]}));
const WALLS=[[-WT,HW+WT,-WT,0],[-WT,HW+WT,HD,HD+WT],[-WT,0,0,9],[-WT,0,12,HD],[HW,HW+WT,0,HD],
  [0,5.5,HY0,HY1],[8.5,9.8,HY0,HY1],[12.8,14.6,HY0,HY1],[17.6,HW,HY0,HY1],[9.0,9.6,HY1,HD],[13.0,13.6,HY1,HD]];
const WINS=[{x0:-WT,x1:0,y0:9,y1:12,near:false}];        // office window, west wall, nothing in front of it
const FURN=[[3.5,7.5,12.4,13.8,2.5,'DESK'],[0.4,1.6,5.4,7.2,4.0,'FILES'],[9.9,12.7,12.8,13.8,3.0,'CABINET'],[15.3,16.7,12.0,13.7,1.4,'TOILET'],[18.2,19.6,6.0,8.0,2.8,'SINK']];
const KEYS=[
 [0,19.4,2.7,5.4,-198,-3,78],
 [T.hunt-2.4,16.6,2.6,5.4,-200,-3,78],
 [T.hunt-1.2,14.4,2.5,5.4,-208,-4,78],
 [T.hunt+.1,13.0,2.6,5.4,-218,-6,76],
 [T.hunt+1.2,12.0,4.6,10,-190,-35,72],
 [T.hunt+1.8,11.2,8,44,-150,-74,64],
 [T.hunt+3.0,10,7,78,-105,-88,42],
 [T.reveal-.9,10,7,60,-90,-90,42],
 [T.reveal+1.5,10,7,60,-90,-90,42],
 [T.stakes-.2,10,7,60,-90,-90,42],
 [T.stakes+1.8,10,29,24,-90,-45,90],
 [T.turn+.8,8,29,24,-84,-45,90],
 [T.sell,10,30,25,-90,-45,90],
];
const ORB={cx:10,cy:7,R:28,ph0:Math.atan2(26-7,22-10),w:0.12,z:17};
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
function fat(arr,w,color){const g=new LineSegmentsGeometry(); g.setPositions(arr); const m=new LineMaterial({color,linewidth:w,resolution:RES}); lineMats.push(m); return new LineSegments2(g,m);}
function loopTop(w,d,h){const x=w/2,y=d/2,z=h/2; return [-x,-y,z,x,-y,z, x,-y,z,x,y,z, x,y,z,-x,y,z, -x,y,z,-x,-y,z];}
function loopRest(w,d,h){const x=w/2,y=d/2,z=h/2,o=[]; const c=[[-x,-y],[x,-y],[x,y],[-x,y]];
  for(let i=0;i<4;i++){const a=c[i],b=c[(i+1)%4]; o.push(a[0],a[1],-z,b[0],b[1],-z); o.push(a[0],a[1],-z,a[0],a[1],z);} return o;}
function addBox(x0,x1,y0,y1,z0,z1,side,top){const w=x1-x0,d=y1-y0,h=z1-z0;
  const sm=new THREE.MeshLambertMaterial({color:side,...PO}), tm=new THREE.MeshBasicMaterial({color:top,...PO}), bm=new THREE.MeshBasicMaterial({color:side,...PO});
  const m=new THREE.Mesh(new THREE.BoxGeometry(w,d,h),[sm,sm,sm,sm,tm,bm]); m.position.set((x0+x1)/2,-(y0+y1)/2,(z0+z1)/2); scene.add(m); return {m,tm,sm,w,d,h,z0};}
const col=new THREE.Color();
// floor + finish lines (office planks, tile elsewhere)
const fl=new THREE.Mesh(new THREE.PlaneGeometry(HW,HD),new THREE.MeshBasicMaterial({color:'#fcfbf8',...PO})); fl.position.set(HW/2,-HD/2,0); scene.add(fl);
const fp=[]; const L=(x0,y0,x1,y1,z=.01)=>fp.push(x0,-y0,z,x1,-y1,z);
for(let x=1;x<9;x+=1)L(x,HY1,x,HD);                                   // office planks
for(let x=10;x<HW;x+=2)L(x,HY1,x,HD); for(let y=7;y<HD;y+=2)L(9.6,y,HW,y);   // storage + restroom tile
for(let x=2;x<HW;x+=2)L(x,0,x,HY0); L(0,2.2,HW,2.2);                  // hall tile
const floorLines=fat(fp,3.6,'#161616'); scene.add(floorLines);
// door swing symbols (plan): arc + open leaf line, exactly the leaf that is modeled below
const dp=[]; const arc=(cx,cy,r,a0,a1)=>{let pv=null;for(let i=0;i<=24;i++){const a=a0+(a1-a0)*i/24,p=[cx+r*Math.cos(a),-(cy+r*Math.sin(a)),.03]; if(pv)dp.push(...pv,...p); pv=p;}};
arc(PIN[0],PY,LD,0,Math.PI/2); arc(PIN[1],PY,LD,0,Math.PI/2); arc(PIN[2],PY,LD,Math.PI/2,Math.PI);
for(let i=0;i<3;i++) dp.push(PIN[i],-PY,.03,PIN[i],-(PY+LD),.03);
const doorLines=fat(dp,3.6,'#161616'); scene.add(doorLines);
// swing sectors (floor decals) + the sink's clear floor space
const sectors=[]; const SECT=[[1.5*Math.PI,Math.PI/2],[1.5*Math.PI,Math.PI/2],[Math.PI,Math.PI/2]];
for(let i=0;i<3;i++){const mt=new THREE.MeshBasicMaterial({color:'#bfc3bb',transparent:true,opacity:0,depthWrite:false,polygonOffset:true,polygonOffsetFactor:-2,polygonOffsetUnits:-2});
  const m=new THREE.Mesh(new THREE.CircleGeometry(LD,40,SECT[i][0],SECT[i][1]),mt); m.position.set(PIN[i],-PY,.02); scene.add(m); sectors.push(m);}
const cfsMat=new THREE.MeshBasicMaterial({color:'#1f9d63',transparent:true,opacity:0,depthWrite:false,polygonOffset:true,polygonOffsetFactor:-3,polygonOffsetUnits:-3});
const cfs=new THREE.Mesh(new THREE.PlaneGeometry(4,2.5),cfsMat); cfs.position.set(16.2,-7.0,.025); scene.add(cfs);
const cfsLn=fat([-2,-1.25,0,2,-1.25,0, 2,-1.25,0,2,1.25,0, 2,1.25,0,-2,1.25,0, -2,1.25,0,-2,-1.25,0],4,'#1f9d63'); cfs.add(cfsLn);
// walls (+ headers over doors)
const walls=[];
for(const [x0,x1,y0,y1] of WALLS){const near=(y0>=HD-.1||x0>=HW-.1); const b=addBox(x0,x1,y0,y1,0,WH,'#e9e6db','#fcfbf8'); const e=fat(loopTop(b.w,b.d,b.h),3.6,'#161616'); b.m.add(e); walls.push({...b,near,wipe:x0/HW,e,hdr:false});}
for(const d of DOORS){const bb=d.b; const b=addBox(bb[0],bb[1],bb[2],bb[3],6.8,WH,'#e9e6db','#fcfbf8'); const e=fat(loopTop(b.w,b.d,b.h),3.6,'#161616'); b.m.add(e); walls.push({...b,near:false,wipe:bb[0]/HW,e,hdr:true});}
// furniture
const furn=[]; const FORD={'DESK':0,'FILES':1,'CABINET':2,'TOILET':3,'SINK':4};
for(const [x0,x1,y0,y1,h,lab] of FURN){const b=addBox(x0,x1,y0,y1,0,h,'#dfdbcf','#fcfbf8');
  b.m.add(fat(loopTop(b.w,b.d,b.h),3.6,'#161616')); b.m.add(fat(loopRest(b.w,b.d,b.h),2.2,'#161616'));
  const W=b.w,Dd=b.d,Hh=b.h,zt=Hh/2+.012,dl=[],fy=-Dd/2-.02;
  const rect=(cx,cy,w,d)=>dl.push(cx-w/2,cy-d/2,zt,cx+w/2,cy-d/2,zt, cx+w/2,cy-d/2,zt,cx+w/2,cy+d/2,zt, cx+w/2,cy+d/2,zt,cx-w/2,cy+d/2,zt, cx-w/2,cy+d/2,zt,cx-w/2,cy-d/2,zt);
  if(lab==='DESK'){rect(0,0,W-.5,Dd-.4); dl.push(-W/2+.9,fy,-Hh/2+.1,-W/2+.9,fy,Hh/2-.1, W/2-.9,fy,-Hh/2+.1,W/2-.9,fy,Hh/2-.1);}
  if(lab==='FILES'){for(let k=1;k<4;k++){const z=-Hh/2+k*Hh/4; dl.push(-W/2+.1,fy,z,W/2-.1,fy,z);} }
  if(lab==='CABINET'){dl.push(0,fy,-Hh/2+.1,0,fy,Hh/2-.1); rect(0,0,W-.4,Dd-.3);}
  if(lab==='TOILET'){rect(0,.3,.9,1.1); dl.push(-.45,-.2,zt,.45,-.2,zt);}
  if(lab==='SINK'){rect(0,0,Dd*.55,W-.4);}
  if(dl.length) b.m.add(fat(dl,1.8,'#161616'));
  furn.push({...b,h,lab,ord:FORD[lab],y0,y1});}
// window: sill + head with cream caps, glass pane, frame as child of the glass; three plan lines across the wall thickness
const panes=[];
for(const wn of WINS){const sill=addBox(wn.x0,wn.x1,wn.y0,wn.y1,0,3.4,'#e9e6db','#fcfbf8'); sill.m.add(fat(loopTop(sill.w,sill.d,sill.h),2,'#161616'));
  const head=addBox(wn.x0,wn.x1,wn.y0,wn.y1,6.6,WH,'#e9e6db','#fcfbf8'); head.m.add(fat(loopTop(head.w,head.d,head.h),2,'#161616'));
  walls.push({...sill,near:wn.near,wipe:0,e:null,hdr:false,win:true}); walls.push({...head,near:wn.near,wipe:0,e:null,hdr:true,win:true});
  const xm=(wn.x0+wn.x1)/2, ym=(wn.y0+wn.y1)/2; const g=new THREE.PlaneGeometry(wn.y1-wn.y0,3.2); g.rotateX(Math.PI/2); g.rotateZ(Math.PI/2);
  const gm=new THREE.Mesh(g,new THREE.MeshBasicMaterial({color:'#cfe3f2',transparent:true,opacity:.55,side:THREE.DoubleSide,depthWrite:false})); gm.position.set(xm,-ym,5); scene.add(gm); panes.push({gm,near:wn.near});
  {const eg=new LineSegmentsGeometry().fromEdgesGeometry(new THREE.EdgesGeometry(g)); const fm=new LineMaterial({color:'#161616',linewidth:2.5,resolution:RES}); lineMats.push(fm); gm.add(new LineSegments2(eg,fm));
   const mg=new LineSegmentsGeometry(); mg.setPositions([0,0,-1.6,0,0,1.6]); gm.add(new LineSegments2(mg,fm));}
  const pl=[]; for(const xx of [wn.x0,xm,wn.x1]) pl.push(xx,-wn.y0,.25,xx,-wn.y1,.25); scene.add(fat(pl,2.6,'#161616'));}
// door leaves: hinge pin on the jamb, 3 hinges, lever on the latch edge; they rotate on the pin from closed to open
const leaves=[];
{const Ld=LD,th=.146,Hd=6.67; const dm=new THREE.MeshLambertMaterial({color:'#e8e2d2',...PO}), tm=new THREE.MeshBasicMaterial({color:'#f4efe2',...PO}), hm=new THREE.MeshBasicMaterial({color:'#161616'});
 for(let i=0;i<3;i++){const g=new THREE.Group(); g.position.set(PIN[i],-PY,0); scene.add(g);
  const m=new THREE.Mesh(new THREE.BoxGeometry(Ld,th,Hd),[dm,dm,dm,dm,tm,tm]); m.position.set(Ld/2,0,Hd/2); g.add(m);
  m.add(fat(loopTop(Ld,th,Hd),2.4,'#161616')); m.add(fat(loopRest(Ld,th,Hd),2.2,'#161616'));
  const pl=[]; for(const fy of [-1,1]){const y=fy*(th/2+.012); for(const [za,zb] of [[-Hd/2+.5,-Hd/2+3.0],[-Hd/2+3.6,Hd/2-.5]]){const xa=-Ld/2+.35,xb=Ld/2-.35; pl.push(xa,y,za,xb,y,za, xb,y,za,xb,y,zb, xb,y,zb,xa,y,zb, xa,y,zb,xa,y,za);}} m.add(fat(pl,1.4,'#161616'));
  const zl=3.0-Hd/2, xl=Ld/2-.3;
  for(const fy of [-1,1]){const st=new THREE.Mesh(new THREE.BoxGeometry(.07,.2,.07),hm); st.position.set(xl,fy*(th/2+.1),zl); m.add(st); const br=new THREE.Mesh(new THREE.BoxGeometry(.42,.05,.05),hm); br.position.set(xl-.2,fy*(th/2+.2),zl); m.add(br);}
  for(const zh of [.7,3.3,6.1]){const hg=new THREE.Mesh(new THREE.BoxGeometry(.1,th+.05,.5),hm); hg.position.set(-Ld/2+.05,0,zh-Hd/2); m.add(hg);}
  leaves.push(g);}}
/* ---------- HUD badges ---------- */
const BD={}; function badge(id,p3,txt,color,alpha,fs=1){let e=BD[id]; if(!e){e=document.createElement('div'); e.className='bd'; document.body.appendChild(e); BD[id]=e;}
  if(alpha<=.01){e.style.opacity=0;return;}
  const v=new THREE.Vector3(p3[0],-p3[1],p3[2]); const dv=v.clone().sub(cam.position); const f=new THREE.Vector3(); cam.getWorldDirection(f); const depth=dv.dot(f);
  if(depth<.5){e.style.opacity=0;return;} const pr=v.clone().project(cam); const sx=(pr.x*.5+.5)*1080, sy=(-pr.y*.5+.5)*1920;
  const focal=960/Math.tan(cam.fov*Math.PI/360); const k=cl(8*(focal/820)/depth,.55,1.5)*fs;
  e.textContent=txt; e.style.color=color; e.style.borderColor=color; e.style.left=sx+'px'; e.style.top=sy+'px'; e.style.transform=`translate(-50%,-50%) scale(${k.toFixed(3)})`; e.style.opacity=alpha;}
const bk=x=>{const c1=1.70158,c3=c1+1,y=x-1; return 1+c3*y*y*y+c1*y*y;};
const scanGroup=new THREE.Group(); scene.add(scanGroup);
{const sl=fat([0,1,.06,0,-15,.06],7,'#1f9d63'); scanGroup.add(sl); const gm=new THREE.Mesh(new THREE.PlaneGeometry(.5,16),new THREE.MeshBasicMaterial({color:'#1f9d63',transparent:true,opacity:.18,depthWrite:false})); gm.position.set(0,-7,.05); scanGroup.add(gm);}
const GREEN='#1f9d63', RED='#c8372d', GRAY='#bfc3bb';
const OPEN_T=[()=>T.stakes+1.1,()=>T.stakes+2.7,()=>T.door+.35];       // when each door starts to swing
function setT(t){
  const c=camAt(t); const a=-c.a,p=c.p;
  const f=new THREE.Vector3(Math.cos(p)*Math.cos(a),Math.cos(p)*Math.sin(a),Math.sin(p)), r=new THREE.Vector3(Math.sin(a),-Math.cos(a),0), u=new THREE.Vector3().crossVectors(r,f);
  cam.position.set(c.x,-c.y,c.z); cam.quaternion.setFromRotationMatrix(new THREE.Matrix4().makeBasis(r,u,f.clone().negate())); cam.fov=c.fov; cam.updateProjectionMatrix(); cam.updateMatrixWorld(true);
  scene.fog.near=Math.max(10,c.z+4); scene.fog.far=scene.fog.near+60;
  const flat=ss(P(t,T.hunt+.4,1.8)), sqBase=1-.98*flat;
  const wallRise=ss(P(t,T.stakes+2.4,1.3)), sqW=Math.min(1,sqBase+(1-sqBase)*wallRise);
  const nearF=1-0.94*ss(P(t,T.stakes+2.4,1.4));
  const sw=ss(P(t,T.reveal,2.6)), sx=lerp(-2,22,sw), wl=x=>ss(cl((sx-x)/2.4+.5,0,1));
  const wkG=ss(P(t,T.reveal+1.0,1.6));
  floorLines.material.linewidth=lerp(3.6,1.5,wkG); floorLines.material.color.set(wkG>.5?'#9a9a8e':'#161616'); doorLines.material.linewidth=lerp(3.6,4.6,wkG);
  scanGroup.visible=sw>0.001&&sw<0.999; scanGroup.position.x=sx;
  for(const w of walls){const k=wl(w.m.position.x), gg=Math.round(lerp(252,22,k)); if(!w.win){w.tm.color.set(`rgb(${gg},${gg},${gg})`); w.e.material.linewidth=lerp(3.6,2.5,k);}
    const s2=w.near?Math.max(.02,sqW*nearF):Math.max(.02,sqW);
    w.m.visible=!(w.hdr&&w.near&&nearF<.5&&t>T.stakes+2.0)&&!(w.hdr&&flat>.5&&wallRise<.02);
    w.m.scale.set(1,1,s2); w.m.position.z=(w.z0+w.h/2)*s2;}
  for(const pn of panes){const s2=pn.near?Math.max(.02,sqW*nearF):Math.max(.02,sqW); pn.gm.scale.set(1,1,s2); pn.gm.position.z=5*s2; pn.gm.visible=!(pn.near&&nearF<.5&&t>T.stakes+2.0);}
  // doors: closed until their cue, then rotate open on the hinge pin
  const op=[0,1,2].map(i=>ss(P(t,OPEN_T[i](),1.1)));
  for(let i=0;i<3;i++){const g=leaves[i]; g.scale.set(1,1,Math.max(.02,sqW)); const closed=HE[i]?Math.PI:0, open=HE[i]?1.5*Math.PI:-Math.PI/2; g.rotation.z=lerp(closed,open,op[i]);}
  // sink slides to a clear spot at the end; its clear floor space and the decals follow
  const mv=ss(P(t,T.sell+.5,1.3)), shift=4.4*mv;
  const conflict=cl(op[2]*1,0,1)*(1-mv);
  const swA=ss(P(t,T.reveal+.8,.8));
  sectors[0].material.opacity=.20*swA; sectors[1].material.opacity=.20*swA; sectors[2].material.opacity=.20*swA;
  sectors[0].material.color.set(GRAY).lerp(col.set(GREEN),op[0]*1); sectors[1].material.color.set(GRAY).lerp(col.set(GREEN),op[1]*1);
  sectors[2].material.color.set(GRAY).lerp(col.set(RED),conflict).lerp(col.set(GREEN),mv);
  for(const i of [0,1]) sectors[i].material.opacity=lerp(.20,.34,op[i])*swA;
  sectors[2].material.opacity=lerp(.20,.38,Math.max(conflict,mv))*swA;
  const cA=ss(P(t,T.reveal+1.2,.7)); cfsMat.opacity=(.16+.10*conflict)*cA; cfs.position.y=-7.0-shift;
  const cc=new THREE.Color(GREEN).lerp(new THREE.Color(RED),conflict); cfsMat.color.copy(cc); cfsLn.material.color.copy(cc);
  cfs.visible=cA>.01;
  for(const q of furn){const pop=bk(P(t,T.stakes+.2+q.ord*.28,.9)); const fs=Math.max(.02,sqBase+(1-sqBase)*pop);
    q.m.scale.set(1,1,fs); q.m.position.z=q.h*fs/2; if(q.lab==='SINK') q.m.position.y=-((q.y0+q.y1)/2)-shift;}
  const wtag=(id,x,txt,color,a)=>badge(id,[x,5.0,1.0+7.9*Math.max(.02,sqW*nearF*0+sqW)],txt,color,a*ss(P(t,T.stakes+3.4,.4)),.85);
  wtag('o',7.0,'CLEAR','#1f6d45',ss(P(t,OPEN_T[0]()+1.0,.3))*(1-ss(P(t,T.sell+.1,.4))));
  wtag('s',11.3,'CLEAR','#1f6d45',ss(P(t,OPEN_T[1]()+1.0,.3))*(1-ss(P(t,T.sell+.1,.4))));
  wtag('r',16.1,'BLOCKED','#b02a22',ss(P(t,T.door+1.35,.3))*(1-mv));
  badge('cf',[16.2,7.0-shift*0,0.6],'SINK CLEAR SPACE','#1f6d45',ss(P(t,T.reveal+1.4,.4))*(1-ss(P(t,T.stakes+.2,.3)))*(1-mv),.8);
  badge('F',[16.2,9.2,1.0],'FAIL · ADA 603.2.3','#b02a22',ss(P(t,T.turn+.15,.35))*(1-mv),1.0);
  badge('P',[16.2,9.2+shift*0,1.0],'PASS','#1f6d45',ss(P(t,T.sell+1.6,.35)),1.1);
  R.render(scene,cam);
  for(let i=0;i<8;i++){const [a,b]=LT[i],d=$('l'+i),q=P(t,a,.22),o=i===7?1:1-P(t,b-.2,.18);d.style.opacity=q*o;d.style.transform='translateY('+((1-eo(q))*30).toFixed(1)+'px)';}
  const cd=$('cd'); if(t>2.3&&t<T.hunt-.1){const r=T.hunt-2.4,n=Math.max(1,Math.ceil(3*(1-(t-2.3)/r)));cd.textContent=n;const fr=((t-2.3)/r*3)%1;cd.style.opacity=1-fr*.7;cd.style.transform='scale('+(1.12-.12*fr)+')';}else cd.style.opacity=0;
  $('leg').style.opacity=P(t,T.reveal+.6,.35)*(1-P(t,T.stakes-.2,.3));
  $('cta').style.opacity=P(t,T.cta,.3);
  $('flash').style.opacity=.22*(1-cl((t-T.reveal)/.1,0,1))*(t>=T.reveal?1:0);
}
window.setT=setT; setT(0); window.ready=true;
</script></body></html>"""




import http.server, socketserver, threading, functools
class _Q(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass
_srv = socketserver.TCPServer(('127.0.0.1', 0), functools.partial(_Q, directory='/home/claude/reels')); PORT = _srv.server_address[1]
threading.Thread(target=_srv.serve_forever, daemon=True).start()


def render(outdir='/home/claude/reels/out2', stills=None, name='r_ds_walk'):
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
    ev = [(0.05, 'whoosh')]; tt = 2.3
    while tt < T['hunt'] - 0.3: ev.append((tt, 'tick')); tt += 1.0
    ev += [(T['hunt'] + 0.4, 'whoosh'), (T['reveal'] - 0.5, 'riser'), (T['reveal'], 'hit')]
    ev += [(T['stakes'] + 0.2 + k * 0.28, 'tick') for k in range(5)] + [(T['stakes'] + 1.1, 'whoosh'), (T['stakes'] + 2.7, 'whoosh'), (T['stakes'] + 2.4, 'whoosh'),
           (T['door'] + 0.35, 'whoosh'), (T['door'] + 1.2, 'hit'), (T['turn'], 'hit'), (T['sell'] + 0.5, 'whoosh'), (T['sell'] + 1.8, 'chime')]
    sfx.add(wav, ev)
    VOICE.lay_under(wav, narration)
    mp4 = str(out / f'{name}.mp4')
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-framerate', str(FPS), '-i', str(fr / '%04d.png'), '-i', wav, '-c:v', 'libx264',
                    '-preset', 'veryfast', '-pix_fmt', 'yuv420p', '-crf', '20', '-c:a', 'aac', '-b:a', '192k', '-shortest', '-movflags', '+faststart', mp4], check=True)
    return mp4


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'stills':
        T, fs = render('/home/claude/reels/outT', stills=[float(x) for x in sys.argv[2].split(',')], name='r_ds_walk')
        print({k: round(v, 1) for k, v in T.items()}); print('\n'.join(fs))
    else:
        print(render())
