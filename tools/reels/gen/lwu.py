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
    "Which object in this room is the tallest? Take a guess.",
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
.ln.blue{color:#1f8a57}
#cd{position:absolute;top:400px;left:0;width:1080px;text-align:center;font:900 200px Helvetica;color:#1f8a57;opacity:0;text-shadow:0 0 22px #f6f4ee}
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
#flash{position:absolute;inset:0;background:#1f9d63;opacity:0}
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
const WALLS=[[-WT,HW+WT,-WT,0],[-WT,15,HD,HD+WT],[18,HW+WT,HD,HD+WT],[-WT,0,0,8],[-WT,0,11,HD],[HW,HW+WT,0,3],[HW,HW+WT,6,HD],[6.7,7.3,0,3],[6.7,7.3,6,HD],[7.3,11,8.7,9.3],[14,HW,8.7,9.3]];
const WINS=[{x0:HW,x1:HW+WT,y0:3,y1:6,near:true},{x0:-WT,x1:0,y0:8,y1:11,near:false}]; // east living-room window, west bedroom window: both clear of furniture
const FURN=[[10.5,17.5,3.4,7.4,0.08,'RUG'],[12.2,15.8,4.6,6.2,1.2,'LOW TABLE'],[9,17,0.4,1.4,6.0,'BOOKCASE'],[0.4,5.4,0.4,6.4,1.0,'PLATFORM BED'],[0.4,6.0,12.2,13.9,6.5,'WARDROBE'],[18.4,20.0,9.5,10.5,3.0,'COUNTER']];
const KEYS=[
 [0,16.7,16.0,5.4,-102,-5,75],
 [T.hunt-2.4,16.5,12.8,5.4,-96,-6,75],
 [T.hunt-1.2,13.4,11.2,5.4,-90,-6,75],
 [T.hunt+.1,12.6,7.6,5.4,-90,-8,75],
 [T.hunt+1.8,12.2,9.0,13,-90,-50,70],
 [T.reveal-.9,10,7,60,-90,-90,42],
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
arc(18,HD,3,Math.PI,Math.PI*1.5); dp.push(18,-HD,.03,18,-(HD-3),.03);
arc(7,3,3,0,Math.PI/2); dp.push(7,-3,.03,10,-3,.03);
arc(11,9,3,0,Math.PI/2); dp.push(11,-9,.03,11,-12,.03);
const doorLines=fat(dp,3.6,'#161616'); scene.add(doorLines);
// walls (+ headers over doors)
const walls=[], capEdges=[];
for(const [x0,x1,y0,y1] of WALLS){const near=(y0>=HD-.1||x0>=HW-.1); const b=addBox(x0,x1,y0,y1,0,WH,'#e9e6db','#fcfbf8'); const e=fat(loopTop(b.w,b.d,b.h),3.6,'#161616'); b.m.add(e); walls.push({...b,near,wipe:x0/HW,e,hdr:false});}
for(const d of DOORS){const bb=d.b, near=bb[2]>=HD-.1; const b=addBox(bb[0],bb[1],bb[2],bb[3],6.8,WH,'#e9e6db','#fcfbf8'); const e=fat(loopTop(b.w,b.d,b.h),3.6,'#161616'); b.m.add(e); walls.push({...b,near,wipe:bb[0]/HW,e,hdr:true});}
// furniture (+ drawn details), each one can squash flat / pop up
const furn=[]; const FORD={'RUG':0,'LOW TABLE':1,'PLATFORM BED':2,'COUNTER':3,'WARDROBE':4,'BOOKCASE':5};
const DIMS={'RUG':[10.1,3.9,'RUG · 1″'],'LOW TABLE':[14,6.9,'LOW TABLE · 14″'],'PLATFORM BED':[5.8,3.4,'BED · 12″'],'COUNTER':[19.2,11.6,'COUNTER · 3′'],'WARDROBE':[6.3,13.0,'WARDROBE · 6′6″'],'BOOKCASE':[8.6,0.9,'BOOKCASE · 6′']};
let _seed=7; const rnd=()=>{_seed=(_seed*16807)%2147483647; return _seed/2147483647;};
function detail(m,arr,w){const l=fat(arr,w,'#161616'); m.add(l); return l;}
for(const [x0,x1,y0,y1,h,lab] of FURN){const zb=lab==='LOW TABLE'?.08:0; const b=addBox(x0,x1,y0,y1,zb,zb+h,'#dfdbcf','#fcfbf8');
  const et=fat(loopTop(b.w,b.d,b.h),3.6,'#161616'); b.m.add(et); const er=fat(loopRest(b.w,b.d,b.h),2.2,'#161616'); b.m.add(er);
  const W=b.w,Dd=b.d,Hh=b.h; const dl=[];
  if(lab==='BOOKCASE'){const fy=-Dd/2-.02; for(let k=1;k<6;k++){const z=-Hh/2+k*Hh/6; dl.push(-W/2+.08,fy,z,W/2-.08,fy,z);}
    for(let k=0;k<6;k++){const zb0=-Hh/2+k*Hh/6+.03; let x=-W/2+.25; while(x<W/2-.4){const bh=(.45+rnd()*.4)*Hh/6; dl.push(x,fy,zb0,x,fy,zb0+bh); x+=.22+rnd()*.35;}}}
  if(lab==='WARDROBE'){const fy=-Dd/2-.02; dl.push(0,fy,-Hh/2+.05,0,fy,Hh/2-.05, -.35,fy,-.4,-.35,fy,.4, .35,fy,-.4,.35,fy,.4);}
  if(lab==='PLATFORM BED'){const zt=Hh/2+.012; for(const yy of [-1.6,1.6]){dl.push(-W/2+.35,yy-.9,zt,-W/2+1.45,yy-.9,zt, -W/2+1.45,yy-.9,zt,-W/2+1.45,yy+.9,zt, -W/2+1.45,yy+.9,zt,-W/2+.35,yy+.9,zt, -W/2+.35,yy+.9,zt,-W/2+.35,yy-.9,zt);}}
  if(lab==='COUNTER'){const zt=Hh/2+.012; dl.push(-.45,-.9,zt,.45,-.9,zt, .45,-.9,zt,.45,.9,zt, .45,.9,zt,-.45,.9,zt, -.45,.9,zt,-.45,-.9,zt);}
  if(lab==='RUG'){const zt=Hh/2+.006; const i=.55; dl.push(-W/2+i,-Dd/2+i,zt,W/2-i,-Dd/2+i,zt, W/2-i,-Dd/2+i,zt,W/2-i,Dd/2-i,zt, W/2-i,Dd/2-i,zt,-W/2+i,Dd/2-i,zt, -W/2+i,Dd/2-i,zt,-W/2+i,-Dd/2+i,zt);}
  const det=dl.length?detail(b.m,dl,1.8):null;
  const dm=DIMS[lab]; const dim=fat([0,0,0,0,0,1],4,'#161616'); dim.position.set(dm[0],-dm[1],zb); scene.add(dim);
  furn.push({...b,h,zb,lab,et,er,det,dim,ord:FORD[lab],dm});}
// windows: sill + head pieces with CREAM caps (glass is not solid wall), glass pane, and three thin plan lines across the wall
const panes=[];
for(const wn of WINS){const sill=addBox(wn.x0,wn.x1,wn.y0,wn.y1,0,3.4,'#e9e6db','#fcfbf8'); sill.m.add(fat(loopTop(sill.w,sill.d,sill.h),2,'#161616'));
  const head=addBox(wn.x0,wn.x1,wn.y0,wn.y1,6.6,WH,'#e9e6db','#fcfbf8'); head.m.add(fat(loopTop(head.w,head.d,head.h),2,'#161616'));
  walls.push({...sill,near:wn.near,wipe:0,e:null,hdr:false,win:true}); walls.push({...head,near:wn.near,wipe:0,e:null,hdr:true,win:true});
  const xm=(wn.x0+wn.x1)/2, ym=(wn.y0+wn.y1)/2; const g=new THREE.PlaneGeometry(wn.y1-wn.y0,3.2); g.rotateX(Math.PI/2); g.rotateZ(Math.PI/2);
  const gm=new THREE.Mesh(g,new THREE.MeshBasicMaterial({color:'#cfe3f2',transparent:true,opacity:.55,side:THREE.DoubleSide,depthWrite:false})); gm.position.set(xm,-ym,5); scene.add(gm); panes.push({gm,near:wn.near});
  {const eg=new LineSegmentsGeometry().fromEdgesGeometry(new THREE.EdgesGeometry(g)); const fm=new LineMaterial({color:'#161616',linewidth:2.5,resolution:RES}); lineMats.push(fm); gm.add(new LineSegments2(eg,fm));
   const mg=new LineSegmentsGeometry(); mg.setPositions([0,0,-1.6,0,0,1.6]); gm.add(new LineSegments2(mg,fm));}
  const pl=[]; for(const xx of [wn.x0,xm,wn.x1]) pl.push(xx,-wn.y0,.25,xx,-wn.y1,.25); scene.add(fat(pl,2.6,'#161616'));}
// doors: leaf drawn open at 90 degrees exactly as in the plan symbol
const doorsG=[];
{const LEAF=[{h:[18,14],d:[0,-1],s:1},{h:[7,3],d:[1,0],s:-1},{h:[11,9],d:[0,1],s:1}]; const Ld=3,th=.146,Hd=6.67;
 const dm=new THREE.MeshLambertMaterial({color:'#e8e2d2',...PO}), tm=new THREE.MeshBasicMaterial({color:'#f4efe2',...PO}), hm=new THREE.MeshBasicMaterial({color:'#161616'});
 for(const D of LEAF){const g=new THREE.Group(); g.position.set(D.h[0],-D.h[1],0); g.rotation.z=Math.atan2(-D.d[1],D.d[0]); scene.add(g);
  const m=new THREE.Mesh(new THREE.BoxGeometry(Ld,th,Hd),[dm,dm,dm,dm,tm,tm]); m.position.set(Ld/2,D.s*th/2,Hd/2); g.add(m);
  m.add(fat(loopTop(Ld,th,Hd),2.4,'#161616')); m.add(fat(loopRest(Ld,th,Hd),2.2,'#161616'));
  const pl=[]; for(const fy of [-1,1]){const y=fy*(th/2+.012); for(const [za,zb] of [[-Hd/2+.5,-Hd/2+3.0],[-Hd/2+3.6,Hd/2-.5]]){const xa=-Ld/2+.35,xb=Ld/2-.35; pl.push(xa,y,za,xb,y,za, xb,y,za,xb,y,zb, xb,y,zb,xa,y,zb, xa,y,zb,xa,y,za);}} m.add(fat(pl,1.4,'#161616'));
  const zl=3.0-Hd/2, xl=Ld/2-.3;
  for(const fy of [-1,1]){const st=new THREE.Mesh(new THREE.BoxGeometry(.07,.2,.07),hm); st.position.set(xl,fy*(th/2+.1),zl); m.add(st); const br=new THREE.Mesh(new THREE.BoxGeometry(.42,.05,.05),hm); br.position.set(xl-.2,fy*(th/2+.2),zl); m.add(br);}
  for(const zh of [.7,3.3,6.1]){const hg=new THREE.Mesh(new THREE.BoxGeometry(.1,th+.05,.5),hm); hg.position.set(-Ld/2+.05,0,zh-Hd/2); m.add(hg);}
  doorsG.push(g);}}
/* ---------- HUD badges (DOM, positioned from 3D points) ---------- */
const BD={}; function badge(id,p3,txt,color,alpha,fs=1){let e=BD[id]; if(!e){e=document.createElement('div'); e.className='bd'; document.body.appendChild(e); BD[id]=e;}
  if(alpha<=.01){e.style.opacity=0;return;}
  const v=new THREE.Vector3(p3[0],-p3[1],p3[2]); const dv=v.clone().sub(cam.position); const f=new THREE.Vector3(); cam.getWorldDirection(f); const depth=dv.dot(f);
  if(depth<.5){e.style.opacity=0;return;} const pr=v.clone().project(cam); const sx=(pr.x*.5+.5)*1080, sy=(-pr.y*.5+.5)*1920;
  const focal=960/Math.tan(cam.fov*Math.PI/360); const k=cl(8*(focal/820)/depth,.55,1.5)*fs;
  e.textContent=txt; e.style.color=color; e.style.borderColor=color; e.style.left=sx+'px'; e.style.top=sy+'px'; e.style.transform=`translate(-50%,-50%) scale(${k.toFixed(3)})`; e.style.opacity=alpha;}
const bk=x=>{const c1=1.70158,c3=c1+1,y=x-1; return 1+c3*y*y*y+c1*y*y;};
const scanGroup=new THREE.Group(); scene.add(scanGroup);
{const sl=fat([0,1,.06,0,-15,.06],7,'#1f9d63'); scanGroup.add(sl); const gm=new THREE.Mesh(new THREE.PlaneGeometry(.5,16),new THREE.MeshBasicMaterial({color:'#1f9d63',transparent:true,opacity:.18,depthWrite:false})); gm.position.set(0,-7,.05); scanGroup.add(gm);}
function setT(t){
  const c=camAt(t); const a=-c.a,p=c.p;
  const f=new THREE.Vector3(Math.cos(p)*Math.cos(a),Math.cos(p)*Math.sin(a),Math.sin(p)), r=new THREE.Vector3(Math.sin(a),-Math.cos(a),0), u=new THREE.Vector3().crossVectors(r,f);
  cam.position.set(c.x,-c.y,c.z); cam.quaternion.setFromRotationMatrix(new THREE.Matrix4().makeBasis(r,u,f.clone().negate())); cam.fov=c.fov; cam.updateProjectionMatrix(); cam.updateMatrixWorld(true);
  scene.fog.near=Math.max(10,c.z+4); scene.fog.far=scene.fog.near+60;
  const flat=ss(P(t,T.hunt+.4,1.8)), sqBase=1-.98*flat;                       // 1 -> .02 while the camera lifts out
  const wallRise=ss(P(t,T.stakes+2.4,1.3)), sqW=Math.min(1,sqBase+(1-sqBase)*wallRise);
  const nearF=1-0.94*ss(P(t,T.stakes+2.4,1.4));
  const sw=ss(P(t,T.reveal,2.6)), sx=lerp(-2,22,sw), wl=x=>ss(cl((sx-x)/2.4+.5,0,1));
  const wkG=ss(P(t,T.reveal+1.0,1.6));
  floorLines.material.linewidth=lerp(3.6,1.5,wkG); floorLines.material.color.set(wkG>.5?'#9a9a8e':'#161616'); doorLines.material.linewidth=lerp(3.6,4.6,wkG);
  scanGroup.visible=sw>0.001&&sw<0.999; scanGroup.position.x=sx;
  for(const w of walls){const xc=(w.m.position.x), k=wl(xc), gg=Math.round(lerp(252,22,k)); if(!w.win){w.tm.color.set(`rgb(${gg},${gg},${gg})`); w.e.material.linewidth=lerp(3.6,2.5,k);}
    const sc=Math.max(.02,sqW*(w.near?lerp(1,nearF,wallRise>.001||t>T.stakes+2.4?1:0):1)); const sc2=w.near?Math.max(.02,sqW*Math.min(1,nearF+ (1-wallRise)*0)):Math.max(.02,sqW);
    const s2=w.near?Math.max(.02,sqW*nearF):Math.max(.02,sqW);
    w.m.visible=!(w.hdr&&w.near&&nearF<.5&&t>T.stakes+2.0)&&!(w.hdr&&flat>.5&&wallRise<.02);
    w.m.scale.set(1,1,s2); w.m.position.z=(w.z0+w.h/2)*s2;}
  for(const g of doorsG){g.scale.set(1,1,Math.max(.02,sqW));}
  for(const pn of panes){const s2=pn.near?Math.max(.02,sqW*nearF):Math.max(.02,sqW); pn.gm.scale.set(1,1,s2); pn.gm.position.z=(pn.gm.isMesh?5:0)*s2; pn.gm.visible=!(pn.near&&nearF<.5&&t>T.stakes+2.0);}
  const gk=ss(P(t,T.turn-.2,.5))*(1-ss(P(t,T.sell+.2,.6)));
  for(const q of furn){const k=wl(q.m.position.x); const pop=bk(P(t,T.stakes+.2+q.ord*.28,.9)); const fs=Math.max(.02,sqBase+(1-sqBase)*pop);
    q.m.scale.set(1,1,fs); q.m.position.z=q.zb+q.h*fs/2;
    const hk=cl(q.h/6.5,0,1), cc=ss(P(t,T.stakes+.3+q.ord*.28,.6));            // colour = drop height: gray (low) -> green (tall)
    const tint=cc*Math.pow(hk,.7);
    q.sm.color.set('#dfdbcf').lerp(col.set(new THREE.Color('#d4d6d2').lerp(new THREE.Color('#5fbf86'),hk)),cc); q.tm.color.set(k>.5?'#e4e0d4':'#fcfbf8').lerp(col.set(new THREE.Color('#e6e8e4').lerp(new THREE.Color('#bfe6cd'),hk)),cc);
    q.et.material.linewidth=lerp(3.6,Math.min(8.5,1.0+q.h*1.15),k);
    q.dim.scale.z=Math.max(.001,q.h*fs*(pop>0.02?1:0)); q.dim.visible=(pop>.02);
    const la=ss(P(t,T.stakes+.45+q.ord*.28,.3))*(1-ss(P(t,T.door+1.4,.6))); badge('D'+q.ord,[q.dm[0],q.dm[1],q.zb+q.h*fs+.55],q.dm[2],(q.h>=3?'#1f6d45':'#6b6b66'),la);}
  const tgA=ss(P(t,T.door+.5,.5))*(1-ss(P(t,T.turn-.5,.4))), tgB=ss(P(t,T.turn+.5,.5))*(1-ss(P(t,T.sell-.2,.4)));
  badge('A',[13,1.0,7.6],'BIGGEST DROP · 6′','#1f6d45',tgA); badge('B',[3.0,3.5,2.2],'SMALL DROP · 12″','#6b6b66',tgB);
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


def render(outdir='/home/claude/reels/out2', stills=None, name='r_lwu_walk'):
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
    ev += [(T['stakes'] + 0.2 + k * 0.28, 'tick') for k in range(5)] + [(T['stakes'] + 0.2 + 5 * 0.28, 'hit'), (T['stakes'] + 2.4, 'whoosh'),
           (T['turn'], 'whoosh'), (T['turn'] + 0.1, 'chime'), (T['sell'], 'whoosh')]
    sfx.add(wav, ev)
    VOICE.lay_under(wav, narration)
    mp4 = str(out / f'{name}.mp4')
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-framerate', str(FPS), '-i', str(fr / '%04d.png'), '-i', wav, '-c:v', 'libx264',
                    '-preset', 'veryfast', '-pix_fmt', 'yuv420p', '-crf', '20', '-c:a', 'aac', '-b:a', '192k', '-shortest', '-movflags', '+faststart', mp4], check=True)
    return mp4


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'stills':
        T, fs = render('/home/claude/reels/outT', stills=[float(x) for x in sys.argv[2].split(',')], name='r_lwu_walk')
        print({k: round(v, 1) for k, v in T.items()}); print('\n'.join(fs))
    else:
        print(render())
