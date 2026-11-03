"""Line-weight reel: a flat floor plan (every line the same weight) gets its line weights, then the
camera drops into the drawing and walks through it in 3D. Heavy cut lines become walls.
Standard cited on screen: University of Memphis architecture drawing standards
(heavy = cut profiles, medium = edges below the cut plane, light = surface lines).
python3 gen/lw.py  -> out2/r_lw_walk.mp4"""
import json, sys, pathlib, subprocess, zlib
sys.path.insert(0, '/home/claude/reels'); sys.path.insert(0, '/home/claude/reels/gen')
from playwright.sync_api import sync_playwright
import soundtrack, sfx
import vo as VOICE

W, H, FPS = 1080, 1920, 30

SCRIPT = [
    "Look at this plan. Could you tell what's wall and what's furniture?",
    "Every line is the same weight. So where does the wall end and the sofa begin?",
    "Now give the cut lines the heaviest weight.",
    "Edges below the cut get medium. Surface lines go light. Now the plan reads at a glance.",
    "Step inside. Which of these lines would you have to knock down?",
    "The heavy ones. Those are the cut walls. Everything lighter, you can move.",
    "Same drawing. Different weights. That's what I do.",
    "Would your drawing hold up? Comment MOTION and I'll send you the details.",
]
CAPS = ["Could you build from this plan?", "Where does the wall end?", "Cut lines go heaviest.",
        "Medium below the cut. Light for surfaces.", "Which line would you knock down?",
        "The heavy ones are the walls.", "Same drawing. Different weights.", "Would your drawing hold up?"]


def times(c, total):
    return dict(setup=0.0, hunt=c[1] - 0.14, reveal=c[2] + 0.8, stakes=c[3] - 0.10, door=c[4] - 0.12,
                turn=c[5] - 0.12, sell=c[6] - 0.14, cta=c[7] - 0.10, end=total + 0.55)


def build(c, total):
    T = times(c, total)
    html = HTML.replace('__DATA__', json.dumps(dict(T=T, dur=T['end'], caps=CAPS)))
    return html, T['end'], T


HTML = r"""<!doctype html><html><head><meta charset="utf-8"><style>
html,body{margin:0;width:1080px;height:1920px;background:#f6f4ee;overflow:hidden;font-family:Helvetica,Arial,sans-serif}
svg{position:absolute;left:0;top:0}
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
<svg id="sv" width="1080" height="1920" viewBox="0 0 1080 1920"></svg><div id="vig"></div>
<div id="tag"><span>LINE WEIGHT</span></div>
<div class="ln" id="l0"></div><div class="ln" id="l1"></div><div class="ln blue" id="l2"></div><div class="ln" id="l3"></div>
<div class="ln" id="l4"></div><div class="ln blue" id="l5"></div><div class="ln" id="l6"></div><div class="ln" id="l7"></div>
<div id="cd"></div>
<div id="leg"><div><i style="height:12px"></i>HEAVY &mdash; cut lines</div><div><i style="height:6px"></i>MEDIUM &mdash; edges below the cut</div><div><i style="height:2.5px;background:#8a8a8a"></i>LIGHT &mdash; surface lines</div><small>UNIV. OF MEMPHIS ARCHITECTURE DRAWING STANDARDS</small></div>
<div id="cta"><div class="a">I set line weights on your drawings &middot; from $30</div><br><div class="b">Comment MOTION</div><div class="c">Send this to whoever drew it</div></div>
<div id="ser"></div><div id="flash"></div>
<script>
const D=__DATA__, T=D.T, $=id=>document.getElementById(id), SV=$('sv');
const cl=(x,a,b)=>Math.max(a,Math.min(b,x)), P=(t,a,d)=>cl((t-a)/d,0,1);
const eo=x=>1-Math.pow(1-x,3), eio=x=>x<.5?4*x*x*x:1-Math.pow(-2*x+2,3)/2, ss=x=>x*x*(3-2*x), lerp=(a,b,k)=>a+(b-a)*k;
const FOC=820, CYS=960, NEAR=0.25, WT=0.6, WH=8, HW=20, HD=14;
D.caps.forEach((s,i)=>{$('l'+i).innerHTML=s;}); $('ser').textContent='LINE WEIGHT 01';
const LT=[[T.setup+.02,T.hunt],[T.hunt+.06,T.reveal],[T.reveal+.06,T.stakes],[T.stakes+.06,T.door],[T.door+.08,T.turn],[T.turn+.07,T.sell],[T.sell+.1,T.cta],[T.cta,D.dur+.5]];
const dot=(a,b)=>a[0]*b[0]+a[1]*b[1]+a[2]*b[2];
/* ------------- the plan ------------- */
const DOORS=[{x0:3,x1:6,wall:'S'},{y0:5.2,y1:8.2,wall:'P'}];
const WALLS=[ // x0,x1,y0,y1
 [-WT,HW+WT,-WT,0],[-WT,3,HD,HD+WT],[6,HW+WT,HD,HD+WT],[-WT,0,0,HD],[HW,HW+WT,0,HD],[10.7,11.3,0,5.2],[10.7,11.3,8.2,HD]];
const FURN=[ // x0,x1,y0,y1,h,label
 [2,8.2,0.4,3.2,2.6,'SOFA'],[4.6,7.6,6,9,2.4,'TABLE'],[14.6,19.6,0.4,6.8,1.8,'BED'],[18.4,19.9,9,14,6.5,'WARDROBE']];
/* ------------- camera: keyframes with Hermite tangents ------------- */
const KEYS=[
 [0,10,7,19.6,-90,-90],
 [T.hunt,10,7,19.2,-90,-90],
 [T.reveal,10,7,18.6,-90,-90],
 [T.stakes,10,7.4,17.2,-92,-84],
 [T.stakes+2.3,9.2,10.6,13.2,-98,-58],
 [T.door-.2,4.6,13.2,9.2,-92,-38],
 [T.door+1.1,2.5,5.8,5.2,0,-8],
 [T.turn-.6,9.5,5.8,5.4,0,-8],
 [T.turn+1.4,12.4,5.8,5.6,-22,-24],
 [T.sell,12.8,6.2,5.8,-35,-28],
];
const ORB={cx:10,cy:7,R:25,ph0:Math.atan2(26-7,22-10),w:0.12,z:17};
function key(t){const K=KEYS; if(t<=K[0][0])return K[0].slice(1);
  for(let i=0;i<K.length-1;i++){ if(t<K[i+1][0]){const a=K[i],b=K[i+1],h=b[0]-a[0],u=(t-a[0])/h,pr=K[i-1]||a,nx=K[i+2]||b,out=[];
    for(let j=1;j<6;j++){const m0=((b[j]-pr[j])/Math.max(b[0]-pr[0],1e-3))*h,m1=((nx[j]-a[j])/Math.max(nx[0]-a[0],1e-3))*h,u2=u*u,u3=u2*u;
      out.push((2*u3-3*u2+1)*a[j]+(u3-2*u2+u)*m0+(-2*u3+3*u2)*b[j]+(u3-u2)*m1);} return out;}}
  return K[K.length-1].slice(1);}
function camAt(t){
  const F=KEYS[KEYS.length-1]; let [x,y,z,a,p]=t<=F[0]?key(t):F.slice(1);
  const walk=ss(P(t,T.door+1.1,.5))*(1-ss(P(t,T.turn+1.4,.6))); z+=0.05*Math.sin(t*7.2)*walk;
  if(t>T.sell){ const k=ss(P(t,T.sell,3.6)), ph=ORB.ph0+ORB.w*(t-T.sell), px=ORB.cx+ORB.R*Math.cos(ph), py=ORB.cy+ORB.R*Math.sin(ph);
    const fx=F[1],fy=F[2],fz=F[3],fa=F[4]; x=lerp(fx,px,k); y=lerp(fy,py,k); z=lerp(fz,ORB.z,k);
    const fwd=[fx+8*Math.cos(fa*Math.PI/180),fy+8*Math.sin(fa*Math.PI/180),fz+8*Math.tan(F[5]*Math.PI/180)], lk=[lerp(fwd[0],ORB.cx,k),lerp(fwd[1],ORB.cy,k),lerp(fwd[2],0.5,k)];
    let ta=Math.atan2(lk[1]-y,lk[0]-x)*180/Math.PI; while(ta-fa>180)ta-=360; while(ta-fa<-180)ta+=360;
    a=ta; p=-Math.atan2(z-lk[2],Math.hypot(lk[0]-x,lk[1]-y))*180/Math.PI; }
  return {x,y,z,a:a*Math.PI/180,p:p*Math.PI/180};
}
let C,B;
function basis(c){const ca=Math.cos(c.a),sa=Math.sin(c.a),cp=Math.cos(c.p),sp=Math.sin(c.p);return {f:[cp*ca,cp*sa,sp],r:[-sa,ca,0],u:[-sp*ca,-sp*sa,cp]};}
const toCam=P3=>{const d=[P3[0]-C.x,P3[1]-C.y,P3[2]-C.z];return [dot(d,B.r),dot(d,B.u),dot(d,B.f)];};
function clipNear(q){const o=[];for(let i=0;i<q.length;i++){const a=q[i],b=q[(i+1)%q.length],ia=a[2]>=NEAR,ib=b[2]>=NEAR;
  if(ia)o.push(a);if(ia!==ib){const k=(NEAR-a[2])/(b[2]-a[2]);o.push([a[0]+(b[0]-a[0])*k,a[1]+(b[1]-a[1])*k,NEAR]);}}return o;}
const scr=q=>[540+FOC*q[0]/q[2],CYS-FOC*q[1]/q[2]];
const poly=pts=>{const q=clipNear(pts.map(toCam));return q.length<3?null:q.map(scr);};
const pts2=q=>q.map(v=>v[0].toFixed(1)+','+v[1].toFixed(1)).join(' ');
function col(hex,f,dist){const n=parseInt(hex.slice(1),16);let r=((n>>16)&255)*f,g=((n>>8)&255)*f,b=(n&255)*f;const fog=cl((dist-10)/34,0,0.5);
  r+=(246-r)*fog;g+=(244-g)*fog;b+=(238-b)*fog;return 'rgb('+[r,g,b].map(v=>Math.round(cl(v,0,255))).join(',')+')';}
function boxF(x0,x1,y0,y1,z0,z1,fill,o={}){const F=[],add=(n,c)=>F.push({n,c,fill,o,bx:[x0,x1,y0,y1,z0,z1]});
  add([0,0,1],[[x0,y0,z1],[x1,y0,z1],[x1,y1,z1],[x0,y1,z1]]);
  if(z1-z0>0.03){add([1,0,0],[[x1,y0,z0],[x1,y1,z0],[x1,y1,z1],[x1,y0,z1]]);add([-1,0,0],[[x0,y0,z0],[x0,y1,z0],[x0,y1,z1],[x0,y0,z1]]);
    add([0,1,0],[[x0,y1,z0],[x1,y1,z0],[x1,y1,z1],[x0,y1,z1]]);add([0,-1,0],[[x0,y0,z0],[x1,y0,z0],[x1,y0,z1],[x0,y0,z1]]);}
  return F;}
function subdiv(f,nu,nv){const [a,b,c,d]=f.c,out=[],L=(p,q,k)=>[lerp(p[0],q[0],k),lerp(p[1],q[1],k),lerp(p[2],q[2],k)];
  for(let i=0;i<nu;i++)for(let j=0;j<nv;j++){const u0=i/nu,u1=(i+1)/nu,v0=j/nv,v1=(j+1)/nv;
    out.push({n:f.n,c:[L(L(a,b,u0),L(d,c,u0),v0),L(L(a,b,u1),L(d,c,u1),v0),L(L(a,b,u1),L(d,c,u1),v1),L(L(a,b,u0),L(d,c,u0),v1)],fill:f.fill,o:f.o,bx:f.bx});}return out;}
const shadeOf=n=>n[2]>0?1.0:0.82+0.10*n[0]-0.06*n[1];
function seg(A,Bp,color,w,dash){let q=[toCam(A),toCam(Bp)];if(q[0][2]<NEAR&&q[1][2]<NEAR)return '';
  if(q[0][2]<NEAR){const k=(NEAR-q[0][2])/(q[1][2]-q[0][2]);q[0]=[lerp(q[0][0],q[1][0],k),lerp(q[0][1],q[1][1],k),NEAR];}
  if(q[1][2]<NEAR){const k=(NEAR-q[1][2])/(q[0][2]-q[1][2]);q[1]=[lerp(q[1][0],q[0][0],k),lerp(q[1][1],q[0][1],k),NEAR];}
  const s0=scr(q[0]),s1=scr(q[1]);return `<line x1="${s0[0].toFixed(1)}" y1="${s0[1].toFixed(1)}" x2="${s1[0].toFixed(1)}" y2="${s1[1].toFixed(1)}" stroke="${color}" stroke-width="${w}" stroke-linecap="round" ${dash?'stroke-dasharray="'+dash+'"':''}/>`;}
function arc(cx,cy,r,a0,a1,color,w){let s='',n=18,prev=null;for(let i=0;i<=n;i++){const a=a0+(a1-a0)*i/n,p=[cx+r*Math.cos(a),cy+r*Math.sin(a),0.03];if(prev)s+=seg(prev,p,color,w);prev=p;}return s;}
function badge(p3,txt,color,size){const q=toCam(p3);if(q[2]<NEAR)return '';let s=scr(q);const k=cl(8/q[2],0.55,1.5),fs=size*k,w=txt.length*fs*0.62+30,h=fs*1.45;
  if(s[0]<-60||s[0]>1140||s[1]<250||s[1]>1700)return '';s=[cl(s[0],w/2+50,1030-w/2),cl(s[1],300,1650)];
  return `<g><rect x="${(s[0]-w/2).toFixed(1)}" y="${(s[1]-h/2).toFixed(1)}" width="${w.toFixed(1)}" height="${h.toFixed(1)}" rx="12" fill="#fff" stroke="${color}" stroke-width="5"/><text x="${s[0].toFixed(1)}" y="${(s[1]+fs*0.36).toFixed(1)}" text-anchor="middle" font-family="Helvetica" font-weight="900" font-size="${fs.toFixed(1)}" fill="${color}">${txt}</text></g>`;}
/* ------------- frame ------------- */

function bxOf(f){ if(f.bx) return f.bx; const mn=[1e9,1e9,1e9],mx=[-1e9,-1e9,-1e9]; for(const p of f.c) for(let k=0;k<3;k++){mn[k]=Math.min(mn[k],p[k]);mx[k]=Math.max(mx[k],p[k]);} return [mn[0],mx[0],mn[1],mx[1],mn[2],mx[2]]; }
function sortOut(out){
  const gm=new Map();
  out.forEach((o,i)=>{const f=o.f,k=f.bx?f.bx.map(v=>v.toFixed(3)).join(','):'u'+i; let g=gm.get(k); if(!g){g={b:bxOf(f),items:[],d:0};gm.set(k,g);} g.items.push(o);});
  const G=[...gm.values()], n=G.length, adj=G.map(()=>[]), indeg=new Array(n).fill(0), cam=[C.x,C.y,C.z], E=1e-4;
  for(const g of G){ g.items.sort((a,b)=>b.dist-a.dist); g.d=g.items[0].dist; }
  for(let i=0;i<n;i++)for(let j=i+1;j<n;j++){
    const a=G[i].b,b=G[j].b; let rel=0,sep=false;
    for(let ax=0;ax<3&&!rel;ax++){
      const a0=a[ax*2],a1=a[ax*2+1],b0=b[ax*2],b1=b[ax*2+1];
      if(a1<=b0+E){ sep=true; if(cam[ax]>=b0-E) rel=-1; else if(cam[ax]<=a1+E) rel=1; }
      else if(b1<=a0+E){ sep=true; if(cam[ax]>=a0-E) rel=1; else if(cam[ax]<=b1+E) rel=-1; }
    }
    if(!rel&&!sep) rel=G[i].d>=G[j].d?-1:1;
    if(rel===-1){adj[i].push(j);indeg[j]++;} else if(rel===1){adj[j].push(i);indeg[i]++;}
  }
  const done=new Array(n).fill(false), res=[];
  for(let c=0;c<n;c++){ let best=-1;
    for(let i=0;i<n;i++) if(!done[i]&&indeg[i]===0&&(best<0||G[i].d>G[best].d)) best=i;
    if(best<0) for(let i=0;i<n;i++) if(!done[i]&&(best<0||G[i].d>G[best].d)) best=i;
    done[best]=true; res.push(...G[best].items); for(const j of adj[best]) indeg[j]--; }
  return res;
}
function setT(t){
  C=camAt(t); B=basis(C);
  const wk=ss(P(t,T.reveal,1.4));                   // 0 = every line the same, 1 = weighted
  const wRise=ss(P(t,T.stakes+1.0,1.9)), fRise=ss(P(t,T.stakes+1.7,1.9)), wh=WH*wRise;
  const cutK=ss(P(t,T.sell+.2,1.6)), nearH=wh*(1-0.94*cutK);
  let floorS='',decS='',labS='',F=[];
  const flat='#161616', FW=lerp(3.6,4.6,wk), SW=lerp(3.6,1.5,wk), scol=wk>.5?'#9a9a8e':'#161616';
  // floor + surface lines (wood boards in the living room, tile grid in the bedroom)
  const fl=poly([[0,0,0],[HW,0,0],[HW,HD,0],[0,HD,0]]); if(fl) floorS+=`<polygon points="${pts2(fl)}" fill="#fcfbf8" stroke="none"/>`;
  for(let x=1;x<10.7;x+=1) floorS+=seg([x,0,.01],[x,HD,.01],scol,SW);
  for(let y=1;y<HD;y+=2) floorS+=seg([11.3,y,.01],[HW,y,.01],scol,SW);
  for(let x=12.3;x<HW;x+=2) floorS+=seg([x,0,.01],[x,HD,.01],scol,SW);
  // door swings (medium)
  decS+=arc(3,HD,3,-Math.PI/2,0,flat,FW)+seg([3,HD,.03],[3,HD-3,.03],flat,FW);
  decS+=arc(11,5.2,3,0,Math.PI/2,flat,FW)+seg([11,5.2,.03],[14,5.2,.03],flat,FW);
  // walls: caps turn to solid poche as the weights go on; they rise into 3D after
  const pocheCol=wk<.02?'#fcfbf8':'rgb('+[0,1,2].map(()=>Math.round(lerp(252,22,wk))).join(',')+')';
  for(const [x0,x1,y0,y1] of WALLS){ const near=(y0>=HD-.1||x0>=HW-.1); const top=near?nearH:wh;
    for(const f of boxF(x0,x1,y0,y1,0,top,'#e9e6db',{wall:1})){
      if(f.n[2]>0) F.push({...f,fill:'#161616',o:{wall:1,cap:1,poche:1,wipe:x0/HW}});
      else F.push(...subdiv(f,Math.max(1,Math.round(Math.hypot(f.c[1][0]-f.c[0][0],f.c[1][1]-f.c[0][1])/1.8)),Math.max(1,Math.round(top/1.8))).map(q=>({...q,o:{wall:1}}))); } }
  // headers over the two doors
  for(const d of DOORS){ const hz=6.8*wRise; if(hz<.1)continue;
    const b=d.wall==='S'?[d.x0,d.x1,HD,HD+WT]:[10.7,11.3,d.y0,d.y1];
    for(const f of boxF(b[0],b[1],b[2],b[3],hz,Math.max(nearH,hz+.02),'#e9e6db',{wall:1})) if(f.n[2]<=0) F.push(f);
    F.push(...boxF(b[0],b[1],b[2],b[3],hz,hz+.01,'#161616',{wall:1,cap:1,poche:1,wipe:b[0]/HW}).filter(f=>f.n[2]>0)); }
  // furniture (medium line) - drawn flat first, then rising
  for(const [x0,x1,y0,y1,h,lab] of FURN){ for(const f of boxF(x0,x1,y0,y1,0,h*fRise,'#dfdbcf',{furn:1})) F.push(f); }
  // windows drawn on the inside of the walls (elevation lines: heavy frame, light glazing)
  if(wRise>.6){ const g=(c,fill,b)=>F.push({n:c.n,c:c.c,fill,o:{thin:1,bias:b}});
    const winN=(x0,x1,z0,z1)=>{const e=.25; g({n:[0,1,0],c:[[x0,.03,z0],[x1,.03,z0],[x1,.03,z1],[x0,.03,z1]]},'#161616',.8); g({n:[0,1,0],c:[[x0+e,.04,z0+e],[x1-e,.04,z0+e],[x1-e,.04,z1-e],[x0+e,.04,z1-e]]},'#dbe6ef',1.0); g({n:[0,1,0],c:[[(x0+x1)/2-.04,.05,z0+e],[(x0+x1)/2+.04,.05,z0+e],[(x0+x1)/2+.04,.05,z1-e],[(x0+x1)/2-.04,.05,z1-e]]},'#8a8a8a',1.2);};
    winN(3,7,3.4,6.6);
    const e=.25; F.push({n:[-1,0,0],c:[[HW-.03,4,3.4],[HW-.03,8,3.4],[HW-.03,8,6.6],[HW-.03,4,6.6]],fill:'#161616',o:{thin:1,bias:.8}});
    F.push({n:[-1,0,0],c:[[HW-.04,4+e,3.4+e],[HW-.04,8-e,3.4+e],[HW-.04,8-e,6.6-e],[HW-.04,4+e,6.6-e]],fill:'#dbe6ef',o:{thin:1,bias:1.0}}); }
  // in-world tags while we walk the drawing
  const tg=ss(P(t,T.turn-.2,.6))*(1-ss(P(t,T.sell-.4,.5)));
  if(tg>0){ labS+=`<g opacity="${tg.toFixed(3)}">`+badge([11,6.7,7.4],'HEAVY = CUT','#161616',34)+badge([17,3.6,2.4],'MEDIUM','#2a5fa8',34)+badge([6,3.0,0.3],'LIGHT','#6b6b60',34)+`</g>`; }
  // sort + draw
  const out=[];
  for(const f of F){const c0=f.c[0]; if(dot(f.n,[C.x-c0[0],C.y-c0[1],C.z-c0[2]])<=0)continue; const q=poly(f.c);if(!q)continue;
    const cx=f.c.reduce((s,p)=>s+p[0],0)/f.c.length,cy=f.c.reduce((s,p)=>s+p[1],0)/f.c.length,cz=f.c.reduce((s,p)=>s+p[2],0)/f.c.length;
    out.push({q,dist:Math.hypot(cx-C.x,cy-C.y,cz-C.z)-((f.o&&f.o.bias)||0),f}); }
  out.splice(0,out.length,...sortOut(out));
  let body='';
  for(const {q,dist,f} of out){ const o=f.o||{}; let fill,stroke,sw;
    if(o.poche){ const k=cl((wk*1.5)-o.wipe*0.5,0,1); const g=Math.round(lerp(252,22,ss(k))); fill=`rgb(${g},${g},${g})`; stroke='#161616'; sw=lerp(3.6,2.5,wk); }
    else if(o.furn){ const top=f.n[2]>0; fill=top?col(wk>.5?'#e4e0d4':'#fcfbf8',1.0,dist):col(f.fill,shadeOf(f.n),dist); stroke='#161616'; sw=lerp(3.6,FW*.8,wk); if(fRise>.02&&!top){sw=2.2;} }
    else if(o.thin){ fill=col(f.fill,1,dist); stroke='none'; sw=0; }
    else { fill=col(f.fill,shadeOf(f.n),dist); stroke=fill; sw=1.4; }
    body+=`<polygon points="${pts2(q)}" fill="${fill}" stroke="${stroke}" stroke-width="${sw}" stroke-linejoin="round"/>`; }
  SV.innerHTML=floorS+decS+body+labS;
  // overlay text
  for(let i=0;i<8;i++){const [a,b]=LT[i],d=$('l'+i),q=P(t,a,.22),o=i===7?1:1-P(t,b-.2,.18);d.style.opacity=q*o;d.style.transform='translateY('+((1-eo(q))*30).toFixed(1)+'px)';}
  const cd=$('cd'); if(t>T.hunt+.2&&t<T.reveal-.1){const r=T.reveal-T.hunt-.5,n=Math.max(1,Math.ceil(3*(1-(t-T.hunt-.2)/r)));cd.textContent=n;const fr=((t-T.hunt-.2)/r*3)%1;cd.style.opacity=1-fr*.7;cd.style.transform='scale('+(1.12-.12*fr)+')';}else cd.style.opacity=0;
  $('leg').style.opacity=P(t,T.stakes+.1,.35)*(1-P(t,T.door-.5,.3));
  $('cta').style.opacity=P(t,T.cta,.3);
  $('flash').style.opacity=.32*(1-cl((t-T.reveal)/.1,0,1))*(t>=T.reveal?1:0);
}
setT(0);
</script></body></html>"""


def render(outdir='/home/claude/reels/out2', stills=None, name='r_lw_walk'):
    out = pathlib.Path(outdir); out.mkdir(exist_ok=True)
    narration, cues, total = VOICE.narrate(SCRIPT)
    html, dur, T = build(cues, total)
    hp = out / f'{name}.html'; hp.write_text(html)
    fr = out / f'fr_{name}'; fr.mkdir(exist_ok=True); N = int(FPS * dur)
    with sync_playwright() as pw:
        b = pw.chromium.launch(); pg = b.new_page(viewport={'width': W, 'height': H}); errs = []
        pg.on('pageerror', lambda e: errs.append(str(e))); pg.goto(hp.resolve().as_uri()); pg.wait_for_timeout(300)
        ts = stills or [i / FPS for i in range(N)]
        for i, t in enumerate(ts):
            pg.evaluate(f'setT({t})'); pg.screenshot(path=str(fr / (f's_{t:05.2f}.png' if stills else f'{i:04d}.png')))
        b.close()
        if errs: print('ERR', errs[:3])
    if stills: return T, [str(fr / f's_{t:05.2f}.png') for t in stills]
    wav = str(out / f'{name}.wav')
    soundtrack.make(dur, draw=(0.2, 1.1), end=dur, mood='bright', bpm=100, seed=zlib.crc32(name.encode()) % 999, out=wav, pen=False, beat=True)
    ev = [(0.05, 'whoosh')]; tt = T['hunt']
    while tt < T['reveal'] - 0.4: ev.append((tt, 'tick')); tt += 1.0
    ev += [(T['reveal'] - 0.5, 'riser'), (T['reveal'], 'hit'), (T['stakes'], 'whoosh'), (T['stakes'] + 2.2, 'whoosh'),
           (T['door'], 'whoosh'), (T['turn'], 'whoosh'), (T['turn'] + 0.1, 'chime'), (T['sell'], 'whoosh')]
    sfx.add(wav, ev)
    VOICE.lay_under(wav, narration)
    mp4 = str(out / f'{name}.mp4')
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-framerate', str(FPS), '-i', str(fr / '%04d.png'), '-i', wav, '-c:v', 'libx264',
                    '-preset', 'veryfast', '-pix_fmt', 'yuv420p', '-crf', '20', '-c:a', 'aac', '-b:a', '192k', '-shortest', '-movflags', '+faststart', mp4], check=True)
    return mp4


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'stills':
        T, fs = render('/home/claude/reels/outT', stills=[float(x) for x in sys.argv[2].split(',')], name='r_lw_walk')
        print({k: round(v, 1) for k, v in T.items()}); print('\n'.join(fs))
    else:
        print(render())
