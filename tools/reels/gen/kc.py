"""Knee-clearance reel (ADA 606.2/606.3, Access Board guide to lavatories and sinks): break-room sink with a 36 in
counter and a cabinet where the knees go. python3 gen/kc.py [stills t1,..] -> out2/r_kc_walk.mp4"""
import json, sys, pathlib, subprocess, zlib
sys.path.insert(0, '/home/claude/reels'); sys.path.insert(0, '/home/claude/reels/gen')
from playwright.sync_api import sync_playwright
import soundtrack, sfx
import vo as VOICE

W, H, FPS = 1080, 1920, 30
SCRIPT = [
    "Would you approve this break room sink? Most people would.",
    "Take three seconds. Can someone in a wheelchair use it?",
    "Time's up. The counter is thirty-six inches. The limit for a sink is thirty-four.",
    "And there's a cabinet right where the knees go. A chair can't roll in.",
    "Now roll up to the sink. Where do your knees go?",
    "An open space, at least twenty-seven inches high and thirty wide. That's ADA section six oh six.",
    "On paper, it's one drag of the mouse. After the cabinets are in, it's a tear-out. I animate plans and elevations. That's what I do.",
    "Would your plan pass? Comment MOTION and I'll send you the details.",
]
CAPS = ["Would you approve this sink?", "Can a wheelchair user use it?", "36 inches. Limit: 34.",
        "A cabinet where the knees go.", "Where do your knees go?", "27 in high. 30 in wide. Open.",
        "One drag on paper. A tear-out once it's built.", "Would your plan pass?"]


def times(c, total):
    return dict(setup=0.0, hunt=c[1] - 0.14, reveal=c[2] + 1.9, stakes=c[3] - 0.10, door=c[4] - 0.12,
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
.ln.red{color:#c0392b}.ln.grn{color:#1f9d63}
#cd{position:absolute;top:400px;left:0;width:1080px;text-align:center;font:900 200px Helvetica;color:#2a5fa8;opacity:0;text-shadow:0 0 22px #f6f4ee}
#src{position:absolute;left:90px;width:900px;top:1800px;text-align:center;font:800 20px Helvetica;letter-spacing:3px;color:#666;opacity:0}
#cta{position:absolute;left:0;width:1080px;top:1520px;text-align:center;opacity:0}
#cta .a{display:inline-block;font:800 34px Helvetica;background:#fff;border:3px solid #161616;border-radius:14px;padding:16px 28px;box-shadow:8px 8px 0 #161616}
#cta .b{margin-top:30px;font:900 56px Helvetica;letter-spacing:2px;color:#1f9d63;text-shadow:0 0 14px #f6f4ee}
#cta .c{display:inline-block;margin-top:24px;font:800 30px Helvetica;background:#161616;color:#fff;border-radius:12px;padding:14px 28px}
#ser{position:absolute;bottom:34px;left:0;width:1080px;text-align:center;font:800 22px Helvetica;letter-spacing:4px;color:#bbb5a4}
#topfade{position:absolute;left:0;top:0;width:1080px;height:340px;background:linear-gradient(180deg,rgba(246,244,238,.94) 0,rgba(246,244,238,.82) 55%,rgba(246,244,238,0) 100%)}
#vig{position:absolute;inset:0;background:radial-gradient(ellipse at 50% 52%,rgba(0,0,0,0) 55%,rgba(20,20,20,.26) 100%)}
#flash{position:absolute;inset:0;background:#c0392b;opacity:0}
</style></head><body>
<svg id="sv" width="1080" height="1920" viewBox="0 0 1080 1920"></svg><div id="vig"></div><div id="topfade"></div>
<div id="tag"><span>KNEE CLEARANCE</span></div>
<div class="ln" id="l0"></div><div class="ln" id="l1"></div><div class="ln red" id="l2"></div><div class="ln red" id="l3"></div>
<div class="ln" id="l4"></div><div class="ln grn" id="l5"></div><div class="ln" id="l6"></div><div class="ln" id="l7"></div>
<div id="cd"></div><div id="src">ADA 2010 STANDARDS &sect;606 &middot; ACCESS BOARD</div>
<div id="cta"><div class="a">I animate plans and elevations &middot; from $450</div><br><div class="b">Comment MOTION</div><div class="c">Send this to whoever drew it</div></div>
<div id="ser"></div><div id="flash"></div>
<script>
const D=__DATA__, T=D.T, $=id=>document.getElementById(id), SV=$('sv');
const cl=(x,a,b)=>Math.max(a,Math.min(b,x)), P=(t,a,d)=>cl((t-a)/d,0,1);
const eo=x=>1-Math.pow(1-x,3), ss=x=>x*x*(3-2*x), lerp=(a,b,k)=>a+(b-a)*k;
const FOC=820, CYS=960, NEAR=0.25, WT=0.6, WH=8, RW=12, RD=11;
const DX0=8, DX1=11, DH=6.8;            // door opening in the SOUTH wall, hinge at x=11, swings into the room
const CHX=4.6, SX=4.6, CABD=2.0;
D.caps.forEach((s,i)=>{$('l'+i).innerHTML=s;}); $('ser').textContent='CLEARANCE 09';
const LT=[[T.setup+.02,T.hunt],[T.hunt+.06,T.reveal],[T.reveal+.06,T.stakes],[T.stakes+.06,T.door],[T.door+.08,T.turn],[T.turn+.07,T.sell],[T.sell+.1,T.cta],[T.cta,D.dur+.5]];
const dot=(a,b)=>a[0]*b[0]+a[1]*b[1]+a[2]*b[2];

const mvK=t=>ss(P(t,T.turn+.35,1.1));
const CHY=t=>lerp(3.75,2.15,mvK(t));
const KEYS=[
 [0,6,5.5,13.8,-90,-90],
 [T.hunt,6,5.5,13.4,-90,-90],
 [T.reveal-.4,6,5.5,12.8,-90,-90],
 [T.reveal+.6,6,5.9,12.0,-90,-86],
 [T.stakes+1.6,6,8.4,8.2,-90,-48],
 [T.door-.4,6,10.4,5.0,-90,-12],
 [T.door+1.0,5.8,9.4,4.5,-90,-7],
 [T.turn-.5,7.7,6.2,4.65,-121,-13],
 [T.turn+1.6,7.4,5.4,4.6,-118,-17],
 [T.sell,7.0,5.6,5.0,-108,-20],
];
const ORB={cx:6,cy:5.5,R:17,ph0:Math.atan2(22-5.5,18-6),w:0.2,z:12.5};
function key(t){const K=KEYS; if(t<=K[0][0])return K[0].slice(1);
  for(let i=0;i<K.length-1;i++){ if(t<K[i+1][0]){const a=K[i],b=K[i+1],h=b[0]-a[0],u=(t-a[0])/h,pr=K[i-1]||a,nx=K[i+2]||b,out=[];
    for(let j=1;j<6;j++){const m0=((b[j]-pr[j])/Math.max(b[0]-pr[0],1e-3))*h,m1=((nx[j]-a[j])/Math.max(nx[0]-a[0],1e-3))*h,u2=u*u,u3=u2*u;
      out.push((2*u3-3*u2+1)*a[j]+(u3-2*u2+u)*m0+(-2*u3+3*u2)*b[j]+(u3-u2)*m1);} return out;}}
  return K[K.length-1].slice(1);}
function camAt(t){
  const F=KEYS[KEYS.length-1]; let [x,y,z,a,p]=t<=F[0]?key(t):F.slice(1);
  const walk=ss(P(t,T.door+.6,.5))*(1-ss(P(t,T.door+2.5,.6))); z+=0.05*Math.sin(t*7.2)*walk;
  if(t>T.sell){ const k=ss(P(t,T.sell,3.6)), ph=ORB.ph0+ORB.w*(t-T.sell), px=ORB.cx+ORB.R*Math.cos(ph), py=ORB.cy+ORB.R*Math.sin(ph);
    const fx=F[1],fy=F[2],fz=F[3],fa=F[4]; const kz=ss(P(t,T.sell,2.2)); x=lerp(fx,px,k); y=lerp(fy,py,k); z=lerp(fz,ORB.z,kz);
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
function boxF(x0,x1,y0,y1,z0,z1,fill,o={}){const F=[],add=(n,c)=>F.push({n,c,fill,o});
  add([0,0,1],[[x0,y0,z1],[x1,y0,z1],[x1,y1,z1],[x0,y1,z1]]);
  if(z1-z0>0.005){add([1,0,0],[[x1,y0,z0],[x1,y1,z0],[x1,y1,z1],[x1,y0,z1]]);add([-1,0,0],[[x0,y0,z0],[x0,y1,z0],[x0,y1,z1],[x0,y0,z1]]);
    add([0,1,0],[[x0,y1,z0],[x1,y1,z0],[x1,y1,z1],[x0,y1,z1]]);add([0,-1,0],[[x0,y0,z0],[x1,y0,z0],[x1,y0,z1],[x0,y0,z1]]);}
  return F;}
function subdiv(f,nu,nv){const [a,b,c,d]=f.c,out=[],L=(p,q,k)=>[lerp(p[0],q[0],k),lerp(p[1],q[1],k),lerp(p[2],q[2],k)];
  for(let i=0;i<nu;i++)for(let j=0;j<nv;j++){const u0=i/nu,u1=(i+1)/nu,v0=j/nv,v1=(j+1)/nv;
    out.push({n:f.n,c:[L(L(a,b,u0),L(d,c,u0),v0),L(L(a,b,u1),L(d,c,u1),v0),L(L(a,b,u1),L(d,c,u1),v1),L(L(a,b,u0),L(d,c,u0),v1)],fill:f.fill,o:f.o});}return out;}
const shadeOf=n=>n[2]>0?1.0:0.82+0.10*n[0]-0.06*n[1];
function seg(A,Bp,color,w,dash){let q=[toCam(A),toCam(Bp)];if(q[0][2]<NEAR&&q[1][2]<NEAR)return '';
  if(q[0][2]<NEAR){const k=(NEAR-q[0][2])/(q[1][2]-q[0][2]);q[0]=[lerp(q[0][0],q[1][0],k),lerp(q[0][1],q[1][1],k),NEAR];}
  if(q[1][2]<NEAR){const k=(NEAR-q[1][2])/(q[0][2]-q[1][2]);q[1]=[lerp(q[1][0],q[0][0],k),lerp(q[1][1],q[0][1],k),NEAR];}
  const s0=scr(q[0]),s1=scr(q[1]);return `<line x1="${s0[0].toFixed(1)}" y1="${s0[1].toFixed(1)}" x2="${s1[0].toFixed(1)}" y2="${s1[1].toFixed(1)}" stroke="${color}" stroke-width="${w}" stroke-linecap="round" ${dash?'stroke-dasharray="'+dash+'"':''}/>`;}
function badge(p3,txt,color,size){const q=toCam(p3);if(q[2]<NEAR)return '';let s=scr(q);const k=cl(8/q[2],0.6,1.4),fs=size*k,w=txt.length*fs*0.62+30,h=fs*1.45;
  if(s[0]<-60||s[0]>1140||s[1]<250||s[1]>1700)return '';s=[cl(s[0],w/2+40,1040-w/2),cl(s[1],300,1650)];
  return `<g><rect x="${(s[0]-w/2).toFixed(1)}" y="${(s[1]-h/2).toFixed(1)}" width="${w.toFixed(1)}" height="${h.toFixed(1)}" rx="12" fill="#fff" stroke="${color}" stroke-width="5"/><text x="${s[0].toFixed(1)}" y="${(s[1]+fs*0.36).toFixed(1)}" text-anchor="middle" font-family="Helvetica" font-weight="900" font-size="${fs.toFixed(1)}" fill="${color}">${txt}</text></g>`;}
function boxR(cx,cy,w,d,z0,z1,ang,fill,o){const ca=Math.cos(ang),sa=Math.sin(ang),hw=w/2,hd=d/2;
  const c=[[-hw,-hd],[hw,-hd],[hw,hd],[-hw,hd]].map(([x,y])=>[cx+x*ca-y*sa,cy+x*sa+y*ca]),F=[];
  F.push({n:[0,0,1],c:c.map(p=>[p[0],p[1],z1]),fill,o});
  const ns=[[0,-1],[1,0],[0,1],[-1,0]];
  for(let i=0;i<4;i++){const A=c[i],Bq=c[(i+1)%4],n=[ns[i][0]*ca-ns[i][1]*sa,ns[i][0]*sa+ns[i][1]*ca,0];F.push({n,c:[[A[0],A[1],z0],[Bq[0],Bq[1],z0],[Bq[0],Bq[1],z1],[A[0],A[1],z1]],fill,o});}
  return F;}
/* ------------- frame ------------- */
function setT(t){
  C=camAt(t); B=basis(C);
  const rise=Math.max(0.03,eo(P(t,T.stakes-.4,1.8))), wh=WH*rise;
  
  const redC='#c0392b', grnC='#1f9d63';
  let floorS='',decS='',labS='',F=[],overS='';
  const fl=poly([[0,0,0],[RW,0,0],[RW,RD,0],[0,RD,0]]); if(fl) floorS+=`<polygon points="${pts2(fl)}" fill="#fcfbf8" stroke="#161616" stroke-width="2"/>`;
  for(let i=1;i<RW;i++) floorS+=seg([i,0,.01],[i,RD,.01],'#e6e2d6',1.5);
  for(let j=1;j<RD;j++) floorS+=seg([0,j,.01],[RW,j,.01],'#e6e2d6',1.5);
  // door swing arc on the floor (hinge at 11,RD; leaf swings into the room to 11,RD-3)
  let prev=null; for(let i=0;i<=20;i++){const th=(i/20)*Math.PI/2, p=[DX1-3*Math.cos(th),RD-3*Math.sin(th),.03]; if(prev) decS+=seg(prev,p,'#161616',3); prev=p;}
  const mk=(x0,x1,y0,y1,z1,z0=0)=>{ for(const f of boxF(x0,x1,y0,y1,z0,z1,'#e9e6db',{wall:1})){
      if(f.n[2]>0){F.push({...f,fill:'#58584f',o:{wall:1,cap:1}});continue;}
      const L=Math.max(Math.hypot(f.c[1][0]-f.c[0][0],f.c[1][1]-f.c[0][1]),.01),H=Math.abs(f.c[3][2]-f.c[0][2]);
      F.push(...subdiv(f,Math.max(1,Math.round(L/2)),Math.max(1,Math.round(H/2))).map(q=>({...q,o:{wall:1}}))); } };
  mk(-WT,RW+WT,-WT,0,wh);                                   // north (sink wall)
  mk(-WT,0,0,RD,wh); mk(RW,RW+WT,0,RD,wh);                  // west, east
  const nearH=wh*(1-0.9*ss(P(t,T.sell+.2,1.4)));
  mk(DX0-.6,DX0,RD+WT,RD+3.6,nearH); mk(DX1,DX1+.6,RD+WT,RD+3.6,nearH); mk(DX0-.6,DX1+.6,RD+3.6,RD+4.2,nearH);
  mk(-WT,DX0,RD,RD+WT,nearH); mk(DX1,RW+WT,RD,RD+WT,nearH); mk(DX0,DX1,RD,RD+WT,Math.max(nearH,DH*rise+.01),DH*rise);   // south either side of the door, header
  
  F.push({n:[0,0,1],c:[[DX0,RD+WT,.02],[DX1,RD+WT,.02],[DX1,RD+3.6,.02],[DX0,RD+3.6,.02]],fill:'#e4dfd0',o:{thin:1,bias:.3}});
  // door frame + open leaf standing at x=11
  F.push(...boxF(DX0-.18,DX0,RD-.02,RD+WT+.02,0,DH*rise,'#2b2b2b',{thin:1}));
  F.push(...boxF(DX1,DX1+.18,RD-.02,RD+WT+.02,0,DH*rise,'#2b2b2b',{thin:1}));
  F.push(...boxF(DX0-.18,DX1+.18,RD-.02,RD+WT+.02,DH*rise,DH*rise+.18,'#2b2b2b',{thin:1}));
  F.push(...boxF(DX1-.14,DX1,RD-3.0,RD-.05,0,DH*rise,'#b79b74',{leaf:1}));
  // window above the sink
  F.push({n:[0,1,0],c:[[3.3,.03,3.6*rise],[5.9,.03,3.6*rise],[5.9,.03,6.6*rise],[3.3,.03,6.6*rise]],fill:'#cfe0f2',o:{bias:.8,thin:1}});
  // fridge, table (clear of the door swing and the path to the sink)
  F.push(...boxF(9.3,11.9,0.1,2.6,0,6.0*rise,'#d9d5c8',{furn:1}));
  F.push(...boxF(5.0,8.0,6.6,8.6,0,2.5*rise,'#d6cdb9',{furn:1}));
  // the sink run: counter slab at 36 in -> 34 in; cabinets at either side; the middle cabinet goes away
  const mv=mvK(t), chH=lerp(36,34,mv)/12, slab=.14, cabH=(chH-slab)*rise, midH=cabH*(1-ss(P(t,T.turn+.35,.9)));
  F.push(...boxF(1.0,3.1,0,CABD,0,cabH,'#c9bfa8',{furn:1}));
  F.push(...boxF(6.1,9.0,0,CABD,0,cabH,'#c9bfa8',{furn:1}));
  if(midH>.02) F.push(...boxF(3.1,6.1,0,CABD,0,midH,'#c9bfa8',{furn:1}));
  F.push(...boxF(1.0,9.0,0,CABD+.1,cabH,cabH+slab*rise,'#8f8a7c',{furn:1}));
  F.push({n:[0,0,1],c:[[3.8,.35,cabH+slab*rise+.01],[5.4,.35,cabH+slab*rise+.01],[5.4,1.65,cabH+slab*rise+.01],[3.8,1.65,cabH+slab*rise+.01]],fill:'#a9b6c4',o:{thin:1,bias:.5}});
  F.push(...boxF(4.55,4.65,.18,.28,cabH+slab*rise,cabH+slab*rise+.5,'#555',{thin:1}));
  if(mv>.5) F.push(...boxF(4.3,4.9,.15,.7,.25,cabH-.05,'#d9d5c8',{wrap:1}));        // pipe wrap behind the open knee space
  // 34 in limit line on the counter edge, and the open knee space after the fix
  const lineA=ss(P(t,T.reveal-.3,.6));
  if(lineA>.01) decS+=`<g opacity="${lineA.toFixed(3)}">`+seg([1.0,CABD+.12,34/12],[9.0,CABD+.12,34/12],'#1f9d63',6,'14 9')+`</g>`;
  if(mv>.3) F.push({n:[0,1,0],c:[[3.1,CABD+.02,.05],[6.1,CABD+.02,.05],[6.1,CABD+.02,27/12],[3.1,CABD+.02,27/12]],fill:'raw',raw:'rgba(31,157,99,'+(0.30*Math.min(1,(mv-.3)*3)).toFixed(3)+')',o:{thin:1,bias:1.5}});
  const hC=chH*12<=34.01?'#1f9d63':'#c0392b';
  if(t>T.reveal-.2){ labS+=badge([2.0,CABD+.1,chH+.9],Math.round(chH*12)+'″',hC,42);
    if(mv<.3) labS+=badge([4.6,CABD+.1,1.3],'KNEES BLOCKED','#c0392b',34);
    else labS+=badge([7.6,CABD+.1,1.5],'27″ HIGH × 30″ WIDE','#1f9d63',30); }
  // the seated person rolling up to the sink
  const chK=ss(P(t,T.door+.4,.6)); const cy=CHY(t);
  if(chK>0){ const k=chK, add=(lx,ly,w,d,z0,z1,fill)=>{F.push(...boxR(CHX+lx,cy+ly,w,d,z0*k,z1*k,0,fill,{thin:1}));};
    add(-1.05,0,.16,2.1,0,1.95,'#3d3d3d'); add(1.05,0,.16,2.1,0,1.95,'#3d3d3d');
    add(0,.1,1.9,2.4,1.2,1.45,'#2a5fa8'); add(0,.95,1.9,.18,1.2,2.8,'#2a5fa8'); add(0,-1.05,1.0,.7,.35,.65,'#555555');
    add(0,.1,1.1,.85,1.45,3.2,'#6b7280'); add(0,.05,.62,.62,3.2,3.8,'#c9a27e'); add(0,-.55,.8,1.0,1.45,1.9,'#6b7280'); }
  let armS='';
  // sort + draw
  const out=[];
  for(const f of F){const c0=f.c[0]; if(dot(f.n,[C.x-c0[0],C.y-c0[1],C.z-c0[2]])<=0)continue; const q=poly(f.c);if(!q)continue;
    const cx=f.c.reduce((s,p)=>s+p[0],0)/f.c.length,cy=f.c.reduce((s,p)=>s+p[1],0)/f.c.length,cz=f.c.reduce((s,p)=>s+p[2],0)/f.c.length;
    out.push({q,dist:Math.hypot(cx-C.x,cy-C.y,cz-C.z)-((f.o&&f.o.bias)||0),f}); }
  out.sort((a,b)=>b.dist-a.dist);
  let body='';
  for(const {q,dist,f} of out){ const o=f.o||{}; let fill,stroke,sw2;
    if(f.fill==='raw'){fill=f.raw;stroke='none';sw2=0;}
    else if(o.cap){fill=col(f.fill,1,dist);stroke='#161616';sw2=2.2;}
    else if(o.plate){fill=col(f.fill,shadeOf(f.n),dist);stroke=o.edge||'#161616';sw2=o.edge?4:2;}
    else if(o.wall){fill=col(f.fill,shadeOf(f.n),dist);stroke=fill;sw2=1.4;}
    else if(o.thin){fill=col(f.fill,1,dist);stroke='#161616';sw2=1.6;}
    else {fill=col(f.fill,shadeOf(f.n),dist);stroke='#161616';sw2=2.2;}
    body+=`<polygon points="${pts2(q)}" fill="${fill}" stroke="${stroke}" stroke-width="${sw2}" stroke-linejoin="round"/>`; }
  SV.innerHTML=floorS+decS+body+armS+labS;
  for(let i=0;i<8;i++){const [a,b]=LT[i],d=$('l'+i),q=P(t,a,.22),o=i===7?1:1-P(t,b-.2,.18);d.style.opacity=q*o;d.style.transform='translateY('+((1-eo(q))*30).toFixed(1)+'px)';}
  const cd=$('cd'); if(t>T.hunt+.2&&t<T.reveal-.1){const r=T.reveal-T.hunt-.5,n=Math.max(1,Math.ceil(3*(1-(t-T.hunt-.2)/r)));cd.textContent=n;const fr=((t-T.hunt-.2)/r*3)%1;cd.style.opacity=1-fr*.7;cd.style.transform='scale('+(1.12-.12*fr)+')';}else cd.style.opacity=0;
  $('src').style.opacity=P(t,T.turn,.4)*(1-P(t,T.sell+.6,.4));
  $('cta').style.opacity=P(t,T.cta,.3);
  $('flash').style.opacity=.30*(1-cl((t-T.reveal)/.12,0,1))*(t>=T.reveal?1:0);
}
setT(0);
</script></body></html>"""


def render(outdir='/home/claude/reels/out2', stills=None, name='r_kc_walk'):
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
        T, fs = render('/home/claude/reels/outT', stills=[float(x) for x in sys.argv[2].split(',')], name='r_kc_walk')
        print({k: round(v, 1) for k, v in T.items()}); print('\n'.join(fs))
    else:
        print(render())
