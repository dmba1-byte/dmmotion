"""First-person walk-through engine (perspective camera).
The camera drops from over the plan, arcs over the wall, walks in through the door, drops to
wheelchair eye height and tries to turn, then pulls out and orbits the finished room while a
wheelchair spins inside the green circle. Same contract as rules.build."""
import json, sys
sys.path.insert(0, '/home/claude/reels/gen'); sys.path.insert(0, '/home/claude/reels')


def build(spec, cues=None, total=None):
    import rules
    html0, dur, T, SCRIPT = rules.build(dict(spec, iso=False, walk=False), cues, total)
    RW, RD = spec['room']
    mv = spec['mov']; fx = spec['fixed'][0]
    wrong, right = spec['wrong'], spec['right']; delta = right - wrong
    VQ = spec.get('vo_q', 'Now picture yourself in it. What goes wrong first?')
    L = [f"Would you approve this {spec['room_word']}?",
         spec.get('cap_hunt', f"How much {spec['gapname']} does it have?"),
         f"The {spec['gapname']} is {wrong}″.",
         f"It needs {right}″. {delta}″ short.",
         spec.get('cap_q', VQ),
         "One drag on paper. Tear-out once it's built.",
         "Would your plan pass?"]
    data = dict(T={k: v for k, v in T.items() if not isinstance(v, tuple)}, move=list(T['move']),
                RW=RW, RD=RD, fx=dict(w=fx[2], d=fx[3], label=fx[4]),
                mv=dict(w=mv['w'], d=mv['d'], label=mv['label']),
                wrong=wrong, right=right, dur=dur, L=L, tag=spec['topic'], rule=spec['rule'],
                source=spec['source'], verdict=spec.get('verdict', 'OK'), idx=spec['idx'])
    return HTML.replace('__DATA__', json.dumps(data)), dur, T, SCRIPT


HTML = r"""<!doctype html><html><head><meta charset="utf-8"><style>
html,body{margin:0;width:1080px;height:1920px;background:#f6f4ee;overflow:hidden;font-family:Helvetica,Arial,sans-serif}
svg{position:absolute;left:0;top:0}
#tag{position:absolute;top:70px;left:0;width:1080px;text-align:center}
#tag span{display:inline-block;font:800 26px Helvetica;letter-spacing:3px;padding:8px 19px;border-radius:8px;background:#fff;border:2px solid #161616}
.ln{position:absolute;top:140px;left:50px;width:980px;text-align:center;font:900 64px/1.08 Helvetica;letter-spacing:-1.5px;color:#161616;opacity:0;
  text-shadow:0 0 18px #f6f4ee,0 0 8px #f6f4ee,0 0 3px #f6f4ee}
.ln.red{color:#c0392b}.ln.sm{font-size:50px}
#cd{position:absolute;top:420px;left:0;width:1080px;text-align:center;font:900 200px Helvetica;color:#c0392b;opacity:0;text-shadow:0 0 22px #f6f4ee}
#vd{position:absolute;top:350px;left:0;width:1080px;text-align:center;opacity:0}
#vd span{display:inline-block;font:900 52px Helvetica;letter-spacing:2px;color:#fff;padding:14px 34px;border-radius:14px}
#rule{position:absolute;left:90px;width:900px;top:1560px;border:4px solid #161616;border-radius:16px;background:#fff;box-shadow:9px 9px 0 #161616;text-align:center;padding:22px 26px;opacity:0}
#rule b{display:block;font:800 36px/1.25 Helvetica;color:#161616}#rule i{display:block;margin-top:10px;font:700 22px Helvetica;letter-spacing:3px;color:#666;font-style:normal}
#cta{position:absolute;left:0;width:1080px;top:1520px;text-align:center;opacity:0}
#cta .a{display:inline-block;font:800 34px Helvetica;background:#fff;border:3px solid #161616;border-radius:14px;padding:16px 28px;box-shadow:8px 8px 0 #161616}
#cta .b{margin-top:30px;font:900 56px Helvetica;letter-spacing:2px;color:#1f9d63;text-shadow:0 0 14px #f6f4ee}
#cta .c{display:inline-block;margin-top:24px;font:800 30px Helvetica;background:#161616;color:#fff;border-radius:12px;padding:14px 28px}
#ser{position:absolute;bottom:34px;left:0;width:1080px;text-align:center;font:800 22px Helvetica;letter-spacing:4px;color:#bbb5a4}
#flash{position:absolute;inset:0;background:#c0392b;opacity:0}
#vig{position:absolute;inset:0;background:radial-gradient(ellipse at 50% 52%,rgba(0,0,0,0) 55%,rgba(20,20,20,.26) 100%)}
</style></head><body>
<svg id="sv" width="1080" height="1920" viewBox="0 0 1080 1920"></svg>
<div id="vig"></div>
<div id="tag"><span id="tg"></span></div>
<div class="ln" id="l0"></div><div class="ln" id="l1"></div><div class="ln" id="l2"></div>
<div class="ln red" id="l3"></div><div class="ln red sm" id="l4"></div><div class="ln sm" id="l5"></div><div class="ln" id="l6"></div>
<div id="cd"></div><div id="vd"><span id="vds"></span></div>
<div id="rule"><b id="rb"></b><i id="ri"></i></div>
<div id="cta"><div class="a">I animate plans and elevations &middot; from $450</div><br><div class="b">Comment MOTION</div><div class="c">Send this to whoever drew it</div></div>
<div id="ser"></div><div id="flash"></div>
<script>
const D=__DATA__, T=D.T, MV=D.move, $=id=>document.getElementById(id), SV=$('sv');
const cl=(x,a,b)=>Math.max(a,Math.min(b,x)), P=(t,a,d)=>cl((t-a)/d,0,1);
const eo=x=>1-Math.pow(1-x,3), eio=x=>x<.5?4*x*x*x:1-Math.pow(-2*x+2,3)/2, ss=x=>x*x*(3-2*x), lerp=(a,b,k)=>a+(b-a)*k;
const RW=D.RW, RD=D.RD, WT=0.6, WH=8, FOC=820, CYS=960, NEAR=0.25;
const DOOR=[2.5,5.7], DOORH=6.8, HL=7;
const FXD=D.fx.d, FXW=D.fx.w, TW=D.mv.w, TD=D.mv.d, G0=D.wrong/12, G1=D.right/12;
$('tg').textContent=D.tag; $('ser').textContent='CLEARANCE '+String(D.idx).padStart(2,'0');
$('rb').innerHTML=D.rule; $('ri').innerHTML=D.source; D.L.forEach((s,i)=>{$('l'+i).innerHTML=s;});
const LT=[[T.setup+.02,T.hunt],[T.hunt+.06,T.reveal],[T.reveal+.06,T.stakes],[T.stakes+.06,T.door],[T.door+.08,T.turn],[T.turn+.07,T.sell],[T.sell+.1,D.dur+.5]];
const dot=(a,b)=>a[0]*b[0]+a[1]*b[1]+a[2]*b[2];
function gapAt(t){return G0+(G1-G0)*eio(P(t,MV[0],MV[1]-MV[0]));}
/* ---------------- camera: keyframes + Hermite (continuous velocity, no stop-start) ---------------- */
const CY0=FXD+G0/2, CY1=FXD+G1/2, M0=MV[0], M1=MV[1];
const KEYS=[
 [0,            5.0,5.5,13.6,  -90,-90],
 [T.hunt,       5.0,5.5,12.2,  -96,-90],
 [(T.hunt+T.reveal)/2+.2, 8.0,5.0,8.8, -150,-48],
 [T.reveal-.25, 9.0,4.0,5.5,  -178,-8],
 [T.reveal+1.7, 8.4,4.0,5.4,  -180,-12],
 [T.stakes,     7.8,4.0,5.3,  -176,-18],
 [T.stakes+1.4, 6.9,4.0,5.2,  -193,-44],
 [T.stakes+2.7, 6.1,4.0,5.2,  -166,-40],
 [T.door-.15,   5.4,4.0,5.1,  -180,-26],
 [T.door+.8,    5.4,4.0,3.9,  -180,-6],
 [T.door+1.55,  5.4,4.0,3.9,  -262,-6],
 [T.door+1.8,   5.4,4.0,3.9,  -266,-7],
 [T.door+2.4,   5.4,4.0,3.9,  -257,-6],
 [M0+.2,        5.4,4.0,3.9,  -257,-6],
 [M0+2.1,       5.4,4.0+(CY1-CY0)*.6,3.9, -350,-6],
 [T.sell, 5.4,CY1,3.9, -364,-5],
];
const ORB={cx:5,cy:5.5,R:10.7,ph0:Math.atan2(14-5.5,11.5-5),w:0.13,z:12.4};
function key(t){
  const K=KEYS; if(t<=K[0][0]) return K[0].slice(1);
  for(let i=0;i<K.length-1;i++){ if(t<K[i+1][0]){
    const a=K[i], b=K[i+1], h=b[0]-a[0], u=(t-a[0])/h;
    const pr=K[i-1]||a, nx=K[i+2]||b, out=[];
    for(let j=1;j<6;j++){
      const m0=((b[j]-pr[j])/(Math.max(b[0]-pr[0],1e-3)))*h, m1=((nx[j]-a[j])/(Math.max(nx[0]-a[0],1e-3)))*h;
      const u2=u*u,u3=u2*u; out.push((2*u3-3*u2+1)*a[j]+(u3-2*u2+u)*m0+(-2*u3+3*u2)*b[j]+(u3-u2)*m1); }
    return out; } }
  return K[K.length-1].slice(1);
}
function camAt(t){
  let [x,y,z,a,p]=key(Math.min(t,KEYS[KEYS.length-1][0]));
  if(t>KEYS[KEYS.length-1][0]){ [x,y,z,a,p]=KEYS[KEYS.length-1].slice(1); }
  // walking bob that fades in at the door and out when we sit down
  const walk=ss(P(t,T.reveal,.5))*(1-ss(P(t,T.door-.2,.5))); z+=0.055*Math.sin(t*7.2)*walk; x+=0.02*Math.sin(t*3.6)*walk;
  // the jolt when the chair hits the tub
  const j=1-P(t,T.door+1.7,.8); if(t>T.door+1.7&&t<T.door+2.5){ z+=0.10*j*Math.sin(t*60); a+=2.2*j*Math.sin(t*47); }
  // pull back out, then orbit the finished room
  if(t>T.sell){
    const k=ss(P(t,T.sell,3.4)), ph=ORB.ph0+ORB.w*(t-T.sell);
    const px=ORB.cx+ORB.R*Math.cos(ph), py=ORB.cy+ORB.R*Math.sin(ph);
    const F=KEYS[KEYS.length-1], fx=F[1], fy=F[2], fz=F[3], fa=F[4];
    x=lerp(fx,px,k); y=lerp(fy,py,k); z=lerp(fz,ORB.z,k);
    // look point slides from "straight ahead" to the room centre, so the view never snaps
    const fwd=[fx+8*Math.cos(fa*Math.PI/180), fy+8*Math.sin(fa*Math.PI/180), fz-0.7], lk=[lerp(fwd[0],ORB.cx,k),lerp(fwd[1],ORB.cy,k),lerp(fwd[2],0.5,k)];
    let ta=Math.atan2(lk[1]-y,lk[0]-x)*180/Math.PI; while(ta-fa>180) ta-=360; while(ta-fa<-180) ta+=360;
    a=ta; p=-Math.atan2(z-lk[2],Math.hypot(lk[0]-x,lk[1]-y))*180/Math.PI;
  }
  return {x,y,z,a:a*Math.PI/180,p:p*Math.PI/180};
}
function basis(c){const ca=Math.cos(c.a),sa=Math.sin(c.a),cp=Math.cos(c.p),sp=Math.sin(c.p);return {f:[cp*ca,cp*sa,sp],r:[-sa,ca,0],u:[-sp*ca,-sp*sa,cp]};}
let C,B;
const toCam=P3=>{const d=[P3[0]-C.x,P3[1]-C.y,P3[2]-C.z];return [dot(d,B.r),dot(d,B.u),dot(d,B.f)];};
function clipNear(q){const o=[];for(let i=0;i<q.length;i++){const a=q[i],b=q[(i+1)%q.length],ia=a[2]>=NEAR,ib=b[2]>=NEAR;
  if(ia)o.push(a); if(ia!==ib){const k=(NEAR-a[2])/(b[2]-a[2]);o.push([a[0]+(b[0]-a[0])*k,a[1]+(b[1]-a[1])*k,NEAR]);}}return o;}
const scr=q=>[540+FOC*q[0]/q[2], CYS-FOC*q[1]/q[2]];
function poly(pts){const q=clipNear(pts.map(toCam));if(q.length<3)return null;return q.map(scr);}
function col(hex,f,dist){const n=parseInt(hex.slice(1),16);let r=((n>>16)&255)*f,g=((n>>8)&255)*f,b=(n&255)*f;const fog=cl((dist-8)/28,0,0.5);
  r=r+(246-r)*fog;g=g+(244-g)*fog;b=b+(238-b)*fog;return 'rgb('+[r,g,b].map(v=>Math.round(cl(v,0,255))).join(',')+')';}
/* ---------------- geometry ---------------- */
function boxR(cx,cy,w,d,z0,z1,ang,fill,o={}){
  const ca=Math.cos(ang), sa=Math.sin(ang), R=(x,y)=>[cx+x*ca-y*sa, cy+x*sa+y*ca], Nn=(x,y)=>[x*ca-y*sa,x*sa+y*ca,0];
  const c=[R(-w/2,-d/2),R(w/2,-d/2),R(w/2,d/2),R(-w/2,d/2)], F=[];
  F.push({n:[0,0,1],c:c.map(q=>[q[0],q[1],z1]),fill,o});
  const ns=[[0,-1],[1,0],[0,1],[-1,0]];
  for(let i=0;i<4;i++){const A=c[i],Bq=c[(i+1)%4]; F.push({n:Nn(...ns[i]),c:[[A[0],A[1],z0],[Bq[0],Bq[1],z0],[Bq[0],Bq[1],z1],[A[0],A[1],z1]],fill,o});}
  return F;
}
const box=(x0,x1,y0,y1,z0,z1,fill,o)=>boxR((x0+x1)/2,(y0+y1)/2,x1-x0,y1-y0,z0,z1,0,fill,o);
function subdiv(f,nu,nv){const [a,b,c,d]=f.c, out=[]; const L=(p,q,k)=>[lerp(p[0],q[0],k),lerp(p[1],q[1],k),lerp(p[2],q[2],k)];
  for(let i=0;i<nu;i++)for(let j=0;j<nv;j++){const u0=i/nu,u1=(i+1)/nu,v0=j/nv,v1=(j+1)/nv;
    out.push({n:f.n,c:[L(L(a,b,u0),L(d,c,u0),v0),L(L(a,b,u1),L(d,c,u1),v0),L(L(a,b,u1),L(d,c,u1),v1),L(L(a,b,u0),L(d,c,u0),v1)],fill:f.fill,o:f.o});}return out;}
const shadeOf=n=>n[2]>0?1.02:0.80+0.10*n[0]-0.06*n[1];
const pts2=q=>q.map(v=>v[0].toFixed(1)+','+v[1].toFixed(1)).join(' ');
function chairFaces(x,y,ang,k){
  const f=[], rot=(lx,ly)=>[x+lx*Math.cos(ang)-ly*Math.sin(ang), y+lx*Math.sin(ang)+ly*Math.cos(ang)];
  const add=(lx,ly,w,d,z0,z1,fill)=>{const p=rot(lx,ly);f.push(...boxR(p[0],p[1],w,d,z0*k,z1*k,ang,fill,{thin:1}));};
  add(-1.05,0,.16,2.1,0,1.95,'#3d3d3d'); add(1.05,0,.16,2.1,0,1.95,'#3d3d3d');
  add(0,.1,1.9,2.4,1.2,1.45,'#2a5fa8'); add(0,.95,1.9,.18,1.2,2.8,'#2a5fa8'); add(0,-1.05,1.0,.7,.35,.65,'#555555');
  add(0,.1,1.1,.85,1.45,3.2,'#6b7280'); add(0,.05,.62,.62,3.2,3.8,'#c9a27e');
  return f;
}
/* ---------------- frame ---------------- */
function setT(t){
  C=camAt(t); B=basis(C);
  const rise=eo(P(t,0.1,1.0)), wh=WH*rise, gap=gapAt(t), cy0=FXD+gap/2, ok=gap>=G1-0.01;
  let floorS='', decS='', labS='', wallF=[], objF=[];
  const fl=poly([[0,0,0],[RW,0,0],[RW,RD,0],[0,RD,0]]);
  if(fl) floorS+=`<polygon points="${pts2(fl)}" fill="#fcfbf8" stroke="#161616" stroke-width="2"/>`;
  const hf=poly([[RW,DOOR[0],0],[RW+HL,DOOR[0],0],[RW+HL,DOOR[1],0],[RW,DOOR[1],0]]);
  if(hf) floorS+=`<polygon points="${pts2(hf)}" fill="#f1eee4" stroke="#bdb8a8" stroke-width="2"/>`;
  const seg=(A,Bp,color,w,dash)=>{let q=[toCam(A),toCam(Bp)];if(q[0][2]<NEAR&&q[1][2]<NEAR)return '';
    if(q[0][2]<NEAR){const k=(NEAR-q[0][2])/(q[1][2]-q[0][2]);q[0]=[lerp(q[0][0],q[1][0],k),lerp(q[0][1],q[1][1],k),NEAR];}
    if(q[1][2]<NEAR){const k=(NEAR-q[1][2])/(q[0][2]-q[1][2]);q[1]=[lerp(q[1][0],q[0][0],k),lerp(q[1][1],q[0][1],k),NEAR];}
    const s0=scr(q[0]),s1=scr(q[1]);return `<line x1="${s0[0].toFixed(1)}" y1="${s0[1].toFixed(1)}" x2="${s1[0].toFixed(1)}" y2="${s1[1].toFixed(1)}" stroke="${color}" stroke-width="${w}" stroke-linecap="round" ${dash?'stroke-dasharray="'+dash+'"':''}/>`;};
  for(let i=1;i<RW;i++) floorS+=seg([i,0,0],[i,RD,0],'#e1ddd0',1.5);
  for(let j=1;j<RD;j++) floorS+=seg([0,j,0],[RW,j,0],'#e1ddd0',1.5);
  // walls, tiled so the painter's sort holds; caps included so nothing looks hollow from above
  const cutK=ss(P(t,T.sell+.2,1.4)), nearH=wh*(1-0.94*cutK);
  const mkWall=(x0,x1,y0,y1,z1)=>{ for(const f of box(x0,x1,y0,y1,0,z1,'#e9e6db',{wall:1})){
      const L=Math.max(Math.hypot(f.c[1][0]-f.c[0][0],f.c[1][1]-f.c[0][1]),0.01), H=Math.abs(f.c[3][2]-f.c[0][2]);
      if(f.n[2]>0){ wallF.push({...f,fill:'#58584f',o:{wall:1,cap:1}}); continue; }
      const nu=Math.max(1,Math.round(L/1.0));
      if(H<=4.05){ wallF.push(...subdiv(f,nu,Math.max(1,Math.round(H))).map(q=>({...q,o:{wall:1,grout:1}}))); continue; }
      const a=f.c[0], b=f.c[1], c=f.c[2], d=f.c[3], Lp=(p,q,k)=>[lerp(p[0],q[0],k),lerp(p[1],q[1],k),lerp(p[2],q[2],k)], kz=4/H;
      const lo={n:f.n,c:[a,b,Lp(b,c,kz),Lp(a,d,kz)],fill:f.fill,o:f.o}, hi={n:f.n,c:[Lp(a,d,kz),Lp(b,c,kz),c,d],fill:f.fill,o:f.o};
      wallF.push(...subdiv(lo,nu,4).map(q=>({...q,o:{wall:1,grout:1}})), ...subdiv(hi,Math.max(1,Math.round(L/2.4)),Math.max(1,Math.round((H-4)/2.2)))); } };
  mkWall(-WT,RW+WT,-WT,0,wh);                    // north
  mkWall(-WT,RW+WT,RD,RD+WT,nearH);              // south
  mkWall(-WT,0,0,RD,wh);                         // west
  mkWall(RW,RW+WT,-WT,DOOR[0],nearH);            // east, north of the door
  mkWall(RW,RW+WT,DOOR[1],RD+WT,nearH);          // east, south of the door
  for(const f of box(RW,RW+WT,DOOR[0],DOOR[1],DOORH*rise,Math.max(nearH,DOORH*rise+0.01),'#e9e6db',{wall:1})) if(f.n[2]<=0) wallF.push(f);
  mkWall(RW+WT,RW+HL,DOOR[0]-WT,DOOR[0],wh); mkWall(RW+WT,RW+HL,DOOR[1],DOOR[1]+WT,wh); mkWall(RW+HL,RW+HL+WT,DOOR[0]-WT,DOOR[1]+WT,wh);
  // door frame as real geometry (sorted with everything else)
  objF.push(...box(RW-.05,RW+WT+.05,DOOR[0]-.18,DOOR[0],0,DOORH*rise,'#2b2b2b',{thin:1}));
  objF.push(...box(RW-.05,RW+WT+.05,DOOR[1],DOOR[1]+.18,0,DOORH*rise,'#2b2b2b',{thin:1}));
  objF.push(...box(RW-.05,RW+WT+.05,DOOR[0]-.18,DOOR[1]+.18,DOORH*rise,DOORH*rise+.18,'#2b2b2b',{thin:1}));
  // mirror above the vanity and a window on the west wall (flat, in front of the paint)
  objF.push({n:[0,1,0],c:[[RW/2-1.8,.03,3.7],[RW/2+1.8,.03,3.7],[RW/2+1.8,.03,6.7],[RW/2-1.8,.03,6.7]],fill:'#dbe6ef',o:{bias:.8,thin:1}});
  objF.push({n:[1,0,0],c:[[.03,4.2,4.3],[.03,6.4,4.3],[.03,6.4,6.6],[.03,4.2,6.6]],fill:'#cfe0f2',o:{bias:.8,thin:1}});
  // fixtures
  objF.push(...box((RW-FXW)/2,(RW+FXW)/2,0,FXD,0,2.9*rise,'#d9d5c8'));
  const tx0=(RW-TW)/2, ty0=FXD+gap;
  objF.push(...box(tx0,tx0+TW,ty0,ty0+TD,0,1.7*rise,'#c3c9d2'));
  objF.push({n:[0,0,1],c:[[tx0+.25,ty0+.22,1.7*rise+.01],[tx0+TW-.25,ty0+.22,1.7*rise+.01],[tx0+TW-.25,ty0+TD-.22,1.7*rise+.01],[tx0+.25,ty0+TD-.22,1.7*rise+.01]],fill:'#8fa6c6',o:{flat:1,bias:.6}});
  // the wheelchair spinning in the green circle once there is room
  const chK=ss(P(t,T.sell+.6,.9));
  if(chK>0) objF.push(...chairFaces(RW/2,cy0,(t-T.sell)*1.5,chK));
  // turning circle (drawn on the floor, 60 in)
  const cc=ok?'#1f9d63':'#c0392b', cf=ok?'rgba(31,157,99,.22)':'rgba(192,57,43,.20)', pre=t<T.reveal;
  const drawn=P(t,T.hunt,1.2);
  if(t>T.hunt){ const n=Math.max(3,Math.round(72*drawn)), pts=[];for(let i=0;i<=n;i++){const aa=-Math.PI/2+i/72*Math.PI*2;pts.push([RW/2+2.5*Math.cos(aa),cy0+2.5*Math.sin(aa),0.02]);}
    const q=poly(pts); if(q) decS+=`<polygon points="${pts2(q)}" fill="${pre?'rgba(22,22,22,.06)':cf}" stroke="${pre?'#161616':cc}" stroke-width="6" stroke-dasharray="${pre?'12 9':(ok?'':'14 10')}" stroke-linejoin="round"/>`; }
  // dimension line (in the world)
  const dim=ss(P(t,T.reveal,.35)), dx=RW*0.30;
  const badge=(p3,txt,color,size)=>{const q=toCam(p3); if(q[2]<NEAR) return ''; let s=scr(q); const k=cl(7/q[2],0.55,1.5), fs=size*k, w=txt.length*fs*0.62+30, h=fs*1.45;
    if(s[0]<-60||s[0]>1140||s[1]<250||s[1]>1700) return ''; s=[cl(s[0],w/2+50,1030-w/2),cl(s[1],300,1650)];
    return `<g><rect x="${(s[0]-w/2).toFixed(1)}" y="${(s[1]-h/2).toFixed(1)}" width="${w.toFixed(1)}" height="${h.toFixed(1)}" rx="12" fill="#fff" stroke="${color}" stroke-width="5"/><text x="${s[0].toFixed(1)}" y="${(s[1]+fs*0.36).toFixed(1)}" text-anchor="middle" font-family="Helvetica" font-weight="900" font-size="${fs.toFixed(1)}" fill="${color}">${txt}</text></g>`;};
  if(dim>0){ const dc=ok?'#1f9d63':'#c0392b', grow=eo(P(t,T.reveal,.5));
    decS+=`<g opacity="${dim}">`+seg([dx,FXD,.05],[dx,FXD+gap*grow,.05],dc,8)+seg([dx-.7,FXD,.05],[dx+.7,FXD,.05],dc,6)+seg([dx-.7,FXD+gap*grow,.05],[dx+.7,FXD+gap*grow,.05],dc,6)+`</g>`;
    if(grow>.6) labS+=`<g opacity="${dim}">`+badge([dx,FXD+gap/2,1.4],Math.round(gap*12)+'″',dc,54)+`</g>`;
    if(t>=T.stakes&&t<M0+.6){ // the 12 missing inches: a pulsing slab on the floor
      const sh=(G1-G0)*eo(P(t,T.stakes,.6)), pu=0.55+0.45*Math.sin((t-T.stakes)*6);
      const sl=poly([[tx0,FXD+G0,.04],[tx0+TW,FXD+G0,.04],[tx0+TW,FXD+G0+sh,.04],[tx0,FXD+G0+sh,.04]]);
      if(sl) decS+=`<polygon points="${pts2(sl)}" fill="rgba(22,22,22,${(0.10+0.18*pu).toFixed(3)})" stroke="#161616" stroke-width="3" stroke-dasharray="10 8"/>`;
      decS+=seg([dx,FXD+G0,.06],[dx,FXD+G0+sh,.06],'#161616',9,'3 9');
      labS+=badge([dx,FXD+G0+sh+.2,2.4],(D.right-D.wrong)+'″ SHORT','#161616',34); } }
  if(rise>.5){ labS+=badge([RW/2,FXD*0.5,3.6],D.fx.label,'#555',28)+badge([RW/2,ty0+TD/2,2.5],D.mv.label,'#555',28); }
  // sort (far to near); caps/walls first by distance, fixtures biased forward
  const outF=[];
  for(const f of wallF.concat(objF)){ const c0=f.c[0];
    if(dot(f.n,[C.x-c0[0],C.y-c0[1],C.z-c0[2]])<=0) continue;
    const q=poly(f.c); if(!q) continue;
    const cx=f.c.reduce((s,p)=>s+p[0],0)/f.c.length, cy=f.c.reduce((s,p)=>s+p[1],0)/f.c.length, cz=f.c.reduce((s,p)=>s+p[2],0)/f.c.length;
    const dist=Math.hypot(cx-C.x,cy-C.y,cz-C.z)-((f.o&&f.o.bias)||0);
    outF.push({q,dist,fill:col(f.fill,shadeOf(f.n),dist),o:f.o||{}}); }
  outF.sort((a,b)=>b.dist-a.dist);
  let body='';
  for(const f of outF){ const o=f.o; const stroke=o.grout?'#cbc6b8':((o.wall&&!o.cap)||o.flat?f.fill:'#161616'); const sw=o.grout?1.3:((o.wall&&!o.cap)||o.flat?1.4:(o.thin?1.6:2.2));
    body+=`<polygon points="${pts2(f.q)}" fill="${f.fill}" stroke="${stroke}" stroke-width="${sw}" stroke-linejoin="round"/>`; }
  // wheelchair rims in the corners while we are "in the chair"
  const inCh=ss(P(t,T.door+.2,.6))*(1-ss(P(t,T.sell+.3,.7)));
  let rims='';
  if(inCh>0){ const spin=(t>=M0?(t-M0)*60:0), wob=(t<M0&&t>T.door+.9&&t<T.door+1.55)?Math.sin(t*9)*5:0;
    const rim=cx=>`<g opacity="${inCh.toFixed(3)}"><circle cx="${cx}" cy="1830" r="400" fill="none" stroke="#161616" stroke-width="22"/><circle cx="${cx}" cy="1830" r="372" fill="none" stroke="#8a8a8a" stroke-width="8"/>`+[0,1,2,3,4,5].map(i=>{const aa=(i*60+spin+wob)*Math.PI/180;return `<line x1="${cx}" y1="1830" x2="${(cx+372*Math.cos(aa)).toFixed(1)}" y2="1830" stroke="none"/><line x1="${cx}" y1="1830" x2="${(cx+372*Math.cos(aa)).toFixed(1)}" y2="${(1830+372*Math.sin(aa)).toFixed(1)}" stroke="#8a8a8a" stroke-width="5"/>`;}).join('')+`</g>`;
    rims=rim(-190)+rim(1270); }
  const bump=(t>T.door+1.7&&t<T.door+3.1)?ss(P(t,T.door+1.7,.25))*(1-ss(P(t,T.door+2.7,.4))):0;
  if(bump>0) labS+=`<g opacity="${bump.toFixed(3)}"><rect x="360" y="900" width="360" height="110" rx="14" fill="#c0392b"/><text x="540" y="978" text-anchor="middle" font-family="Helvetica" font-weight="900" font-size="64" fill="#fff">STUCK</text></g>`;
  SV.innerHTML=floorS+decS+body+labS+rims;
  // ---- overlay text ----
  for(let i=0;i<7;i++){ const [a,b]=LT[i], d=$('l'+i), q=P(t,a,.22), out=1-P(t,b-.2,.18); d.style.opacity=q*out; d.style.transform='translateY('+((1-eo(q))*30).toFixed(1)+'px)'; }
  const cd=$('cd'); if(t>T.hunt+.2&&t<T.reveal-.05){ const r=T.reveal-T.hunt-.4, n=Math.max(1,Math.ceil(3*(1-(t-T.hunt-.2)/r))); cd.textContent=n; const fr=((t-T.hunt-.2)/r*3)%1; cd.style.opacity=1-fr*.7; cd.style.transform='scale('+(1.12-.12*fr)+')'; } else cd.style.opacity=0;
  const vd=$('vd'), vs=$('vds');
  if(t>=T.reveal&&t<T.sell){ vs.textContent=ok?'✓ '+D.verdict:'✕ TOO TIGHT'; vs.style.background=ok?'#1f9d63':'#c0392b'; vd.style.opacity=P(t,T.reveal,.2)*(1-P(t,T.sell-.1,.2)); }
  else if(t>=T.sell){ vs.textContent='✓ '+D.verdict; vs.style.background='#1f9d63'; vd.style.opacity=P(t,T.sell,.2); } else vd.style.opacity=0;
  $('rule').style.opacity=P(t,T.turn+.5,.3)*(1-P(t,T.sell-.1,.25));
  $('cta').style.opacity=P(t,T.cta,.3);
  $('flash').style.opacity=.5*(1-cl((t-T.reveal)/.08,0,1))*(t>=T.reveal?1:0);
}
setT(0);
</script></body></html>"""
