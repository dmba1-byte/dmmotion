"""True 3D isometric engine for clearance reels.
The plan view is only the first beat: the camera pitches from top-down into a cut-away
isometric room, orbits, and dives to eye level while a wheelchair figure tries to turn.
build(spec, cues, total) -> (html, dur, T, SCRIPT), same contract as rules.build."""
import json, sys
sys.path.insert(0, '/home/claude/reels/gen'); sys.path.insert(0, '/home/claude/reels')

W, H = 1080, 1920
INK, GRN, BLUE, RED = '#161616', '#1f9d63', '#2a5fa8', '#c0392b'


def build(spec, cues=None, total=None):
    import rules
    html0, dur, T, SCRIPT = rules.build(dict(spec, iso=False), cues, total)
    RW, RD = spec['room']
    mv = spec['mov']
    wrong, right = spec['wrong'], spec['right']
    delta = right - wrong
    fx = spec['fixed'][0]                      # (x, y, w, d, label, kind) along the back wall
    VQ = spec.get('vo_q', 'Now picture yourself in it. What goes wrong first?')
    L = [f"Would you approve this {spec['room_word']}?",
         spec.get('cap_hunt', f"How much {spec['gapname']} does it have?"),
         f"The {spec['gapname']} is {wrong}″.",
         f"It needs {right}″. {delta}″ short.",
         spec.get('cap_q', VQ),
         "Free to move on paper. Not after the pour.",
         "Would your plan pass?"]
    data = dict(T={k: v for k, v in T.items() if not isinstance(v, tuple)}, move=list(T['move']),
                RW=RW, RD=RD, fx=dict(w=fx[2], d=fx[3], label=fx[4]),
                mv=dict(w=mv['w'], d=mv['d'], label=mv['label'], base=mv['base']),
                wrong=wrong, right=right, dur=dur, L=L, tag=spec['topic'], rule=spec['rule'],
                source=spec['source'], verdict=spec.get('verdict', 'OK'), idx=spec['idx'])
    html = HTML.replace('__DATA__', json.dumps(data))
    return html, dur, T, SCRIPT


HTML = r"""<!doctype html><html><head><meta charset="utf-8"><style>
html,body{margin:0;width:1080px;height:1920px;background:#f6f4ee;overflow:hidden;font-family:Helvetica,Arial,sans-serif}
#bg{position:absolute;inset:0;background-image:linear-gradient(#e7e3d8 1px,transparent 1px),linear-gradient(90deg,#e7e3d8 1px,transparent 1px);background-size:54px 54px;opacity:.55}
svg{position:absolute;left:0;top:0}
#tag{position:absolute;top:70px;left:0;width:1080px;text-align:center}
#tag span{display:inline-block;font:800 26px Helvetica;letter-spacing:3px;padding:8px 19px;border-radius:8px;background:#fff;border:2px solid #161616}
.ln{position:absolute;top:150px;left:60px;width:960px;text-align:center;font:900 64px/1.08 Helvetica;letter-spacing:-1.5px;color:#161616;opacity:0}
.ln.red{color:#c0392b}.ln.sm{font-size:50px}
#cd{position:absolute;top:400px;left:0;width:1080px;text-align:center;font:900 190px Helvetica;color:#c0392b;opacity:0}
#vd{position:absolute;top:360px;left:0;width:1080px;text-align:center;opacity:0}
#vd span{display:inline-block;font:900 52px Helvetica;letter-spacing:2px;color:#fff;padding:14px 34px;border-radius:14px}
#rule{position:absolute;left:90px;width:900px;top:1560px;border:4px solid #161616;border-radius:16px;background:#fff;box-shadow:9px 9px 0 #161616;text-align:center;padding:22px 26px;opacity:0}
#rule b{display:block;font:800 36px/1.25 Helvetica;color:#161616}#rule i{display:block;margin-top:10px;font:700 22px Helvetica;letter-spacing:3px;color:#666;font-style:normal}
#cta{position:absolute;left:0;width:1080px;top:1560px;text-align:center;opacity:0}
#cta .a{display:inline-block;font:800 34px Helvetica;background:#fff;border:3px solid #161616;border-radius:14px;padding:16px 28px;box-shadow:8px 8px 0 #161616}
#cta .b{margin-top:30px;font:900 56px Helvetica;letter-spacing:2px;color:#1f9d63}
#cta .c{display:inline-block;margin-top:24px;font:800 30px Helvetica;background:#161616;color:#fff;border-radius:12px;padding:14px 28px}
#ser{position:absolute;bottom:34px;left:0;width:1080px;text-align:center;font:800 22px Helvetica;letter-spacing:4px;color:#bbb5a4}
#flash{position:absolute;inset:0;background:#c0392b;opacity:0}
</style></head><body><div id="bg"></div>
<svg id="sv" width="1080" height="1920" viewBox="0 0 1080 1920"></svg>
<div id="tag"><span id="tg"></span></div>
<div class="ln" id="l0"></div><div class="ln" id="l1"></div><div class="ln" id="l2"></div>
<div class="ln red" id="l3"></div><div class="ln red sm" id="l4"></div><div class="ln sm" id="l5"></div><div class="ln" id="l6"></div>
<div id="cd"></div><div id="vd"><span id="vds"></span></div>
<div id="rule"><b id="rb"></b><i id="ri"></i></div>
<div id="cta"><div class="a">I animate plans and elevations &middot; from $450</div><br><div class="b">Comment MOTION</div><div class="c">Send this to whoever drew it</div></div>
<div id="ser"></div><div id="flash"></div>
<script>
const D=__DATA__, T=D.T, NS='http://www.w3.org/2000/svg', $=id=>document.getElementById(id);
const cl=(x,a,b)=>Math.max(a,Math.min(b,x)), P=(t,a,d)=>cl((t-a)/d,0,1);
const eo=x=>1-Math.pow(1-x,3), eio=x=>x<.5?4*x*x*x:1-Math.pow(-2*x+2,3)/2;
const RW=D.RW, RD=D.RD, CX=RW/2, CY=RD/2, WALL=0.6, WH=7;
$('tg').textContent=D.tag; $('ser').textContent='CLEARANCE '+String(D.idx).padStart(2,'0');
const LT=[[T.setup+.02,T.hunt],[T.hunt+.06,T.reveal],[T.reveal+.06,T.stakes],[T.stakes+.06,T.door],[T.door+.08,T.turn],[T.turn+.07,T.sell],[T.sell+.1,D.dur+.5]];
D.L.forEach((s,i)=>{$('l'+i).innerHTML=s;});
$('rb').innerHTML=D.rule; $('ri').innerHTML=D.source;

/* ---------- camera ---------- */
function cam(t){
  const k=(a,b,x0,x1,tt)=>a+(b-a)*eio(P(t,x0,x1-x0));
  let ph=90, th=0;
  ph=90; ph=k(90,60,T.hunt,T.reveal);
  ph=t<T.reveal? ph : t<T.stakes? k(60,40,T.reveal,T.stakes) : t<T.door? 40-3*P(t,T.stakes,T.door-T.stakes)
     : t<T.turn? k(37,22,T.door,T.turn) : t<T.sell? k(22,36,T.turn,T.sell) : 36-2*P(t,T.sell,D.dur-T.sell);
  th=t<T.hunt?0:t<T.reveal?k(0,40,T.hunt,T.reveal):40+22*P(t,T.reveal,D.dur-T.reveal);
  if(t>=T.door&&t<T.turn) th=40+22*P(t,T.reveal,D.dur-T.reveal)-10*eio(P(t,T.door,T.turn-T.door));
  const rp=Math.max(0,ph)*Math.PI/180, tr=th*Math.PI/180;
  const f=cl((ph-35)/55,0,1);
  return {ph:rp,phd:ph,th:tr,sc:60+22*f*f, cy:1030+30*(1-f)};
}
function pr(p,c){
  const x=p[0]-CX, y=p[1]-CY, z=p[2];
  const cs=Math.cos(c.th), sn=Math.sin(c.th), x1=x*cs-y*sn, y1=x*sn+y*cs;
  const cp=Math.cos(c.ph), sp=Math.sin(c.ph);
  return {X:540+c.sc*x1, Y:c.cy+c.sc*(y1*sp-z*cp), d:y1*cp+z*sp, x1, y1};
}
/* ---------- faces ---------- */
function boxFaces(c,o){ // o: x,y,w,d,h,z0,ang,fill,pal
  const a=o.ang||0, ca=Math.cos(a), sa=Math.sin(a), z0=o.z0||0, h=o.h;
  if(h<=0.001) return [];
  const loc=[[-1,-1],[1,-1],[1,1],[-1,1]].map(([i,j])=>{const lx=i*o.w/2, ly=j*o.d/2; return [o.x+lx*ca-ly*sa, o.y+lx*sa+ly*ca];});
  const out=[], cs=Math.cos(c.th), sn=Math.sin(c.th), cp=Math.cos(c.ph), sp=Math.sin(c.ph);
  const poly=(pts,shade,nz)=>{const q=pts.map(p=>pr(p,c)); out.push({q,d:q.reduce((s,v)=>s+v.d,0)/q.length,fill:shade,sw:o.sw||2});};
  const mix=(hex,f)=>{const n=parseInt(hex.slice(1),16);let r=(n>>16)&255,g=(n>>8)&255,b=n&255;
     if(f<1){r*=f;g*=f;b*=f}else{r+=(255-r)*(f-1);g+=(255-g)*(f-1);b+=(255-b)*(f-1)}
     return 'rgb('+[r,g,b].map(v=>Math.round(cl(v,0,255))).join(',')+')';};
  poly(loc.map(p=>[p[0],p[1],z0+h]),mix(o.fill,1.10));
  for(let i=0;i<4;i++){
    const p0=loc[i], p1=loc[(i+1)%4], ex=p1[0]-p0[0], ey=p1[1]-p0[1];
    let nx=ey, ny=-ex; const L=Math.hypot(nx,ny); nx/=L; ny/=L;
    const mx=(p0[0]+p1[0])/2-o.x, my=(p0[1]+p1[1])/2-o.y; if(nx*mx+ny*my<0){nx=-nx;ny=-ny;}
    const rx=(nx-CX*0)*cs-ny*sn, ry=nx*sn+ny*cs; // rotated normal (relative)
    if(ry*cp<=0.0001) continue;                       // back face (side faces have no z comp)
    poly([[p0[0],p0[1],z0],[p1[0],p1[1],z0],[p1[0],p1[1],z0+h],[p0[0],p0[1],z0+h]],mix(o.fill,0.78+0.16*rx));
  }
  return out;
}
const SV=$('sv');
let FACES=[], DECALS=[], LABELS=[];
function emit(){
  FACES.sort((a,b)=>a.d-b.d);
  let s='';
  const path=(q,fill,stroke,sw,extra='')=>`<path d="M${q.map(v=>v.X.toFixed(1)+' '+v.Y.toFixed(1)).join('L')}Z" fill="${fill}" stroke="${stroke}" stroke-width="${sw}" stroke-linejoin="round" ${extra}/>`;
  for(const f of DECALS) s+=f;
  for(const f of FACES) s+=path(f.q,f.fill,'#161616',f.sw);
  for(const l of LABELS) s+=l;
  SV.innerHTML=s;
}
/* ---------- decals / labels ---------- */
function line3(c,pts,col,w,dash){const q=pts.map(p=>pr(p,c));return `<polyline points="${q.map(v=>v.X.toFixed(1)+','+v.Y.toFixed(1)).join(' ')}" fill="none" stroke="${col}" stroke-width="${w}" ${dash?'stroke-dasharray="'+dash+'"':''} stroke-linecap="round" stroke-linejoin="round"/>`;}
function circle3(c,cx,cy,r,col,fillcol,dash,w){
  const pts=[];for(let i=0;i<=72;i++){const a=i/72*Math.PI*2;pts.push([cx+r*Math.cos(a),cy+r*Math.sin(a),0.02]);}
  const q=pts.map(p=>pr(p,c));
  return `<polygon points="${q.map(v=>v.X.toFixed(1)+','+v.Y.toFixed(1)).join(' ')}" fill="${fillcol}" stroke="${col}" stroke-width="${w||5}" ${dash?'stroke-dasharray="'+dash+'"':''}/>`;
}
function badge(c,p,txt,col,sz){
  const q=pr(p,c), w=txt.length*sz*0.62+34, h=sz*1.45;
  return `<g><rect x="${q.X-w/2}" y="${q.Y-h/2}" width="${w}" height="${h}" rx="12" fill="#fff" stroke="${col}" stroke-width="5"/><text x="${q.X}" y="${q.Y+sz*0.36}" text-anchor="middle" font-family="Helvetica" font-weight="900" font-size="${sz}" fill="${col}">${txt}</text></g>`;
}
/* ---------- the figure ---------- */
function chair(c,x,y,ang,k){
  const f=[]; const rot=(lx,ly)=>[x+lx*Math.cos(ang)-ly*Math.sin(ang), y+lx*Math.sin(ang)+ly*Math.cos(ang)];
  const add=(lx,ly,w,d,h,z0,fill)=>{const p=rot(lx,ly);f.push(...boxFaces(c,{x:p[0],y:p[1],w,d,h:h*k,z0:z0*k,ang,fill,sw:1.6}));};
  add(-1.05,0,0.14,2.0,1.9,0,'#3d3d3d'); add(1.05,0,0.14,2.0,1.9,0,'#3d3d3d');     // wheels
  add(0,0.1,1.9,2.4,0.25,1.2,'#2a5fa8');                                            // seat
  add(0,0.95,1.9,0.18,1.6,1.2,'#2a5fa8');                                           // back
  add(0,-1.0,1.0,0.8,0.3,0.35,'#555555');                                           // footplate
  add(0,0.1,1.1,0.8,1.8,1.45,'#6b7280');                                            // torso
  add(0,0.05,0.62,0.62,0.62,3.3,'#c9a27e');                                         // head
  return f;
}
/* ---------- frame ---------- */
const FX=D.fx, MV=D.mv;
function yTub(t){ // gap between fixture front and tub back
  const g0=D.wrong/12, g1=D.right/12, m=D.move;
  const e=eio(P(t,m[0],m[1]-m[0]));
  return [g0+(g1-g0)*e, e];
}
function setT(t){
  const c=cam(t); FACES=[]; DECALS=[]; LABELS=[];
  const rise=eo(P(t,0.15,0.9));
  // floor
  const fl=[[0,0,0],[RW,0,0],[RW,RD,0],[0,RD,0]].map(p=>pr(p,c));
  DECALS.push(`<polygon points="${fl.map(v=>v.X.toFixed(1)+','+v.Y.toFixed(1)).join(' ')}" fill="#fcfbf8" stroke="#bdb8a8" stroke-width="2"/>`);
  // grid on floor
  for(let i=1;i<RW;i++) DECALS.push(line3(c,[[i,0,0],[i,RD,0]],'#e4e0d3',1.5));
  for(let j=1;j<RD;j++) DECALS.push(line3(c,[[0,j,0],[RW,j,0]],'#e4e0d3',1.5));
  // walls: near walls drop to a cut-away sill as the camera pitches down
  const cut=cl((90-c.phd)/24,0,1);
  const wallDefs=[[RW/2,-WALL/2,RW+2*WALL,WALL,'N'],[RW/2,RD+WALL/2,RW+2*WALL,WALL,'S'],[-WALL/2,RD/2,WALL,RD,'W'],[RW+WALL/2,RD/2,WALL,RD,'E']];
  const cd0=pr([CX,CY,0],c).d;
  for(const [x,y,w,d] of wallDefs){
    const near=pr([x,y,0],c).d>cd0+0.3; const hh=(near?WH-(WH-0.45)*cut:WH)*rise;
    FACES.push(...boxFaces(c,{x,y,w,d,h:hh,z0:0,fill:'#2b2b2b',sw:2.2}));
  }
  // fixed fixture (vanity) along the back wall
  FACES.push(...boxFaces(c,{x:FX.w/2+(RW-FX.w)/2,y:FX.d/2,w:FX.w,d:FX.d,h:2.9*rise,z0:0,fill:'#d9d5c8'}));
  // tub
  const [gap,e]=yTub(t); const ty=FX.d+gap+MV.d/2;
  FACES.push(...boxFaces(c,{x:RW/2,y:ty,w:MV.w,d:MV.d,h:1.7*rise,z0:0,fill:'#c8ccd2'}));
  // labels on the fixtures (upright billboards)
  LABELS.push(`<text x="${pr([RW/2,FX.d/2,2.9*rise+0.3],c).X}" y="${pr([RW/2,FX.d/2,2.9*rise+0.3],c).Y}" text-anchor="middle" font-family="Helvetica" font-weight="800" font-size="26" letter-spacing="3" fill="#555" opacity="${rise}">${FX.label}</text>`);
  const tp=pr([RW/2,ty,1.7*rise+0.3],c);
  LABELS.push(`<text x="${tp.X}" y="${tp.Y}" text-anchor="middle" font-family="Helvetica" font-weight="800" font-size="26" letter-spacing="3" fill="#555" opacity="${rise}">${MV.label}</text>`);
  // turning circle on the floor
  const cy0=FX.d+gap/2, ok=gap>=D.right/12-0.01, appear=P(t,T.hunt+.1,.4);
  const cdash=ok?'':'14 10';
  const col=ok?'#1f9d63':'#c0392b', fillc=ok?'rgba(31,157,99,.18)':'rgba(192,57,43,.16)';
  const circT=t<T.reveal?P(t,T.hunt,.5)*0.8:1;
  if(t>T.hunt-.1) DECALS.push(circle3(c,RW/2,cy0,2.5,t<T.reveal?'#161616':col,t<T.reveal?'rgba(22,22,22,.06)':fillc,cdash||(t<T.reveal?'10 8':''),5));
  // dimension line between vanity and tub (3D, on the floor, left of the circle)
  const dx=RW*0.14; const dim=P(t,T.reveal,.3);
  if(dim>0){
    const dc=ok?'#1f9d63':'#c0392b';
    DECALS.push(line3(c,[[dx,FX.d,.03],[dx,FX.d+gap,.03]],dc,6));
    DECALS.push(line3(c,[[dx-.5,FX.d,.03],[dx+.5,FX.d,.03]],dc,5));
    DECALS.push(line3(c,[[dx-.5,FX.d+gap,.03],[dx+.5,FX.d+gap,.03]],dc,5));
    LABELS.push(badge(c,[dx-0.2,FX.d+gap/2,.9],Math.round(gap*12)+'″',dc,46).replace('<g>','<g opacity="'+dim+'">'));
    if(t>=T.stakes&&!ok){ // the missing inches, drawn as a red slab in the gap
      const sh=(D.right-D.wrong)/12*eo(P(t,T.stakes,.5));
      DECALS.push(line3(c,[[dx,FX.d+gap,.04],[dx,FX.d+gap+sh,.04]],'#161616',6,'4 8'));
      LABELS.push(badge(c,[dx-0.2,FX.d+gap+sh+0.55,.9],(D.right-D.wrong)+'″ SHORT','#161616',32));
    }
  }
  // wheelchair figure appears for the "sit in the chair" question
  const cp=P(t,T.door-0.1,.5)*(t<T.sell+.4?1:1-P(t,T.sell+.4,.5));
  let bump=0;
  if(cp>0){
    let ang;
    if(ok){ ang=Math.PI*eio(P(t,T.move[0]+.2,1.7)); }
    else { const w=P(t,T.door,1.1); ang=1.15*eo(w)+0.035*Math.sin(t*38)*P(t,T.door+1.1,1.2); bump=P(t,T.door+1.0,1.3); }
    FACES.push(...chair(c,RW/2,cy0,ang,cp));
    if(!ok&&bump>0) LABELS.push(badge(c,[RW/2,cy0,4.6],'STUCK','#c0392b',44).replace('<g>','<g opacity="'+bump+'">'));
  }
  emit();
  // ---- overlay text ----
  for(let i=0;i<7;i++){ const [a,b]=LT[i], d=$('l'+i), q=P(t,a,.22), out=1-P(t,b-.2,.18);
    d.style.opacity=q*out; d.style.transform='translateY('+((1-eo(q))*30).toFixed(1)+'px)'; }
  // countdown 3-2-1 with a hidden number
  const cd=$('cd'); if(t>T.hunt+.2&&t<T.reveal-.05){ const r=T.reveal-T.hunt-.4, n=Math.max(1,Math.ceil(3*(1-(t-T.hunt-.2)/r)));
     cd.textContent=n; const fr=((t-T.hunt-.2)/r*3)%1; cd.style.opacity=1-fr*0.7; cd.style.transform='scale('+(1.12-0.12*fr)+')'; } else cd.style.opacity=0;
  const vd=$('vd'), vs=$('vds');
  if(t>=T.reveal&&t<T.sell){ const ok2=ok; vs.textContent=ok2?'✓ '+D.verdict:'✕ TOO TIGHT'; vs.style.background=ok2?'#1f9d63':'#c0392b'; vd.style.opacity=P(t,ok2?T.move[1]:T.reveal,.2)*(1-P(t,T.sell-.1,.2)); }
  else if(t>=T.sell){ vs.textContent='✓ '+D.verdict; vs.style.background='#1f9d63'; vd.style.opacity=P(t,T.sell,.2); } else vd.style.opacity=0;
  $('rule').style.opacity=P(t,T.turn+.5,.3)*(1-P(t,T.sell-.1,.25));
  $('cta').style.opacity=P(t,T.cta,.3);
  $('flash').style.opacity=0.55*(1-cl((t-T.reveal)/0.08,0,1))*(t>=T.reveal?1:0);
  const sh=t>=T.reveal&&t<T.reveal+.35?(1-P(t,T.reveal,.35))*10*Math.sin(t*90):0; SV.style.transform='translate('+sh.toFixed(1)+'px,'+(sh*.6).toFixed(1)+'px)';
}
setT(0);
</script></body></html>"""
