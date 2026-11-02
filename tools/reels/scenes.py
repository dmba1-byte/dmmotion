"""Animated cutaway scenes (1080x1920). render(kind, dur, pal, caption, out) -> silent mp4. Deterministic setT(t)."""
import sys, json, pathlib, subprocess, shutil
from playwright.sync_api import sync_playwright
W, H, FPS = 1080, 1920, 30
PAL = {
 'blue':  dict(bg1='#050f20', bg2='#0f3d78', glow='#6db8ff', ink='#dbe9fb', acc='#6db8ff', dim='#16365f'),
 'green': dict(bg1='#04150f', bg2='#0d5a3f', glow='#58e0a4', ink='#e2f6ec', acc='#58e0a4', dim='#12392b'),
 'gray':  dict(bg1='#08090a', bg2='#33373c', glow='#e8e8e8', ink='#f2f2f2', acc='#e8e8e8', dim='#25282b'),
}
HTML = r"""<!doctype html><meta charset=utf-8><style>
html,body{margin:0;width:1080px;height:1920px;overflow:hidden;background:#000;font-family:Helvetica,Arial,sans-serif}
#cap{position:absolute;left:70px;right:70px;bottom:360px;text-align:center;z-index:9}
#cap span{display:inline-block;color:#f7f2e6;font-size:46px;font-weight:700;line-height:1.16;letter-spacing:-.4px;padding:20px 38px 24px;border-radius:24px;background:linear-gradient(180deg,rgba(10,32,60,.80),rgba(6,20,40,.88));border:1.5px solid rgba(247,242,230,.30);box-shadow:0 16px 44px rgba(0,0,0,.38)}
#cap span::before{content:'';display:block;width:64px;height:5px;border-radius:3px;background:__ACC__;margin:0 auto 14px} #cap em{font-style:normal;color:__ACC__}
#tag{position:absolute;left:0;right:0;top:230px;text-align:center;z-index:9;font:700 40px Menlo,Consolas,monospace;letter-spacing:6px;color:__INK__}
</style><svg id="s" width="1080" height="1920" viewBox="0 0 1080 1920" style="position:absolute;left:0;top:0"></svg><div id=tag></div><div id=cap></div>
<script>
const P=__PAL__, K=__KIND__, DUR=__DUR__, CAP=__CAP__, TAG=__TAG__;
const NS='http://www.w3.org/2000/svg', S=document.getElementById('s');
const cl=(x,a,b)=>Math.max(a,Math.min(b,x)), ease=t=>t<.5?2*t*t:1-Math.pow(-2*t+2,2)/2, lerp=(a,b,t)=>a+(b-a)*t;
function E(n,a,p){const e=document.createElementNS(NS,n);for(const k in a)e.setAttribute(k,a[k]);(p||S).appendChild(e);return e}
const defs=E('defs',{});
defs.innerHTML=`<linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="${P.bg1}"></stop><stop offset="1" stop-color="${P.bg2}"></stop></linearGradient>
<radialGradient id="vg" cx=".5" cy=".5" r=".75"><stop offset=".55" stop-color="#000" stop-opacity="0"></stop><stop offset="1" stop-color="#000" stop-opacity=".7"></stop></radialGradient>
<radialGradient id="gl" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="${P.glow}" stop-opacity=".55"></stop><stop offset="1" stop-color="${P.glow}" stop-opacity="0"></stop></radialGradient>
<filter id="bl"><feGaussianBlur stdDeviation="14"></feGaussianBlur></filter><filter id="bl2"><feGaussianBlur stdDeviation="3"></feGaussianBlur></filter>`;
E('rect',{width:1080,height:1920,fill:'url(#bg)'});
const world=E('g',{});               // camera group
let upd=()=>{};
const F={};
// ---------------- DESK AT 2 A.M. ----------------
F.desk=()=>{
 const w=world;
 // window with rain + city lights
 E('rect',{x:70,y:300,width:420,height:520,fill:P.dim,opacity:.9,stroke:P.ink,'stroke-opacity':.25,'stroke-width':3},w);
 const lights=[];for(let i=0;i<26;i++){lights.push(E('rect',{x:90+(i*53)%380,y:640+((i*37)%150),width:12,height:12+(i%3)*6,fill:P.glow,opacity:.5},w))}
 const rain=[];for(let i=0;i<22;i++)rain.push(E('line',{x1:0,y1:0,x2:-5,y2:34,stroke:P.ink,'stroke-opacity':.4,'stroke-width':2},w));
 E('line',{x1:280,y1:300,x2:280,y2:820,stroke:P.ink,'stroke-opacity':.25,'stroke-width':3},w);
 // wall clock
 const cx=830,cy=420;E('circle',{cx,cy,r:112,fill:P.bg1,stroke:P.ink,'stroke-width':6,opacity:.95},w);
 for(let i=0;i<12;i++){const a=i*Math.PI/6;E('line',{x1:cx+Math.sin(a)*92,y1:cy-Math.cos(a)*92,x2:cx+Math.sin(a)*104,y2:cy-Math.cos(a)*104,stroke:P.ink,'stroke-width':4},w)}
 const hh=E('line',{stroke:P.ink,'stroke-width':8,'stroke-linecap':'round'},w),mh=E('line',{stroke:P.ink,'stroke-width':5,'stroke-linecap':'round'},w),sh=E('line',{stroke:P.acc,'stroke-width':3},w);
 // lamp cone
 const cone=E('polygon',{points:'820,830 600,1300 1060,1300',fill:P.glow,opacity:.12,filter:'url(#bl2)'},w);
 // desk
 E('rect',{x:0,y:1230,width:1080,height:700,fill:'#05080d'},w);E('rect',{x:0,y:1226,width:1080,height:8,fill:P.ink,opacity:.18},w);
 // monitor
 const mon=E('rect',{x:300,y:760,width:520,height:360,rx:14,fill:'#071a33',stroke:P.ink,'stroke-opacity':.4,'stroke-width':4},w);
 E('rect',{x:540,y:1120,width:40,height:110,fill:'#0a1424'},w);E('rect',{x:470,y:1220,width:180,height:16,rx:8,fill:'#0a1424'},w);
 const scr=E('rect',{x:316,y:776,width:488,height:328,fill:P.glow,opacity:.16},w);
 const glow=E('ellipse',{cx:560,cy:960,rx:560,ry:460,fill:'url(#gl)'},w);
 // elevation lines on screen (all the same weight)
 const sl=[];[[350,1060,770,1060],[380,1060,380,930],[740,1060,740,930],[380,930,560,860],[560,860,740,930],[420,1010,500,1010],[420,960,500,960],[420,960,420,1010],[500,960,500,1010],[620,1010,700,1010],[620,960,700,960],[620,960,620,1010],[700,960,700,1010]].forEach(l=>sl.push(E('line',{x1:l[0],y1:l[1],x2:l[2],y2:l[3],stroke:P.ink,'stroke-width':3,opacity:.85},w)));
 const cur=E('rect',{x:700,y:1068,width:3,height:22,fill:P.ink},w);
 // person (silhouette, head in hands)
 const body=E('path',{d:'M120 1300 C120 1100 230 1020 330 1030 C430 1020 520 1100 520 1300 Z',fill:'#03060b',stroke:P.glow,'stroke-opacity':.35,'stroke-width':3},w);
 const head=E('g',{},w);E('circle',{cx:0,cy:0,r:78,fill:'#03060b',stroke:P.glow,'stroke-opacity':.4,'stroke-width':3},head);
 const hand1=E('path',{d:'M-84 -10 C-110 -60 -60 -110 -10 -70 C-60 -60 -70 -30 -60 10 Z',fill:'#03060b',stroke:P.glow,'stroke-opacity':.4,'stroke-width':3},head);
 const hand2=E('path',{d:'M84 -10 C110 -60 60 -110 10 -70 C60 -60 70 -30 60 10 Z',fill:'#03060b',stroke:P.glow,'stroke-opacity':.4,'stroke-width':3},head);
 // cup + steam, papers
 E('rect',{x:880,y:1170,width:90,height:64,rx:10,fill:'#0b1220',stroke:P.ink,'stroke-opacity':.4,'stroke-width':3},w);
 const steam=[0,1,2].map(i=>E('path',{fill:'none',stroke:P.ink,'stroke-width':4,'stroke-linecap':'round','stroke-opacity':.35},w));
 [[640,1250,-6],[700,1262,4],[760,1252,-2]].forEach(p=>E('rect',{x:p[0],y:p[1],width:200,height:130,fill:'#0a1424',stroke:P.ink,'stroke-opacity':.3,'stroke-width':2,transform:`rotate(${p[2]} ${p[0]} ${p[1]})`},w));
 upd=(t)=>{
  const f=.5+.5*Math.sin(t*9.0)*Math.sin(t*3.1);
  scr.setAttribute('opacity',.14+.07*f);glow.setAttribute('opacity',.85+.15*f);cone.setAttribute('opacity',.10+.04*Math.sin(t*5));
  lights.forEach((l,i)=>l.setAttribute('opacity',.25+.5*Math.abs(Math.sin(t*1.3+i*1.7))));
  rain.forEach((r,i)=>{const y=((t*520+i*97)%700),x=90+((i*61)%400);r.setAttribute('transform',`translate(${x} ${300+y})`);r.setAttribute('opacity',.8)});
  const a=t*.22; mh.setAttribute('x1',cx);mh.setAttribute('y1',cy);mh.setAttribute('x2',cx+Math.sin(a)*86);mh.setAttribute('y2',cy-Math.cos(a)*86);
  hh.setAttribute('x1',cx);hh.setAttribute('y1',cy);hh.setAttribute('x2',cx+Math.sin(2.2+a/12)*58);hh.setAttribute('y2',cy-Math.cos(2.2+a/12)*58);
  const sa=t*2.4*Math.PI/6*3;sh.setAttribute('x1',cx);sh.setAttribute('y1',cy);sh.setAttribute('x2',cx+Math.sin(sa)*98);sh.setAttribute('y2',cy-Math.cos(sa)*98);
  const br=Math.sin(t*1.6), tilt=Math.sin(t*.7)*3;
  head.setAttribute('transform',`translate(${330+Math.sin(t*.5)*6} ${925+br*7}) rotate(${tilt})`);
  body.setAttribute('transform',`translate(0 ${br*3})`);
  cur.setAttribute('opacity',Math.floor(t*2)%2?0:1);
  steam.forEach((s,i)=>{const x=905+i*20,ph=t*2+i;s.setAttribute('d',`M${x} 1165 q ${10*Math.sin(ph)} -30 0 -55 q ${-10*Math.sin(ph+1)} -30 0 -55`);s.setAttribute('stroke-opacity',.18+.2*Math.abs(Math.sin(ph*.7)))});
  const z=1+.07*t/DUR; world.setAttribute('transform',`translate(${540-540*z+Math.sin(t*.6)*6} ${960-960*z-t*6}) scale(${z})`);
 };
};
// ---------------- JURY ----------------
F.jury=()=>{
 const w=world;
 E('rect',{x:0,y:1280,width:1080,height:640,fill:'#04070c'},w);
 E('rect',{x:130,y:330,width:820,height:560,fill:P.bg1,stroke:P.ink,'stroke-opacity':.5,'stroke-width':5},w);
 E('rect',{x:150,y:350,width:780,height:520,fill:'#eaf1fa',opacity:.92},w);
 // drawing on the board: uniform weight (nothing reads first)
 [[220,760,860,760],[260,760,260,590],[820,760,820,590],[260,590,540,460],[540,460,820,590],[340,700,440,700],[340,630,440,630],[340,630,340,700],[440,630,440,700],[640,700,740,700],[640,630,740,630],[640,630,640,700],[740,630,740,700],[500,760,500,640],[580,760,580,640],[500,640,580,640]].forEach(l=>E('line',{x1:l[0],y1:l[1],x2:l[2],y2:l[3],stroke:'#1d4e89','stroke-width':3},w));
 [[150,350],[930,350],[150,870],[930,870]].forEach(p=>E('circle',{cx:p[0],cy:p[1],r:9,fill:P.acc},w));
 const dot=E('circle',{r:16,fill:P.acc},w),halo=E('circle',{r:44,fill:P.acc,opacity:.25,filter:'url(#bl2)'},w);
 // jurors
 const jur=[];[[240,1100],[540,1070],[840,1100]].forEach((p,i)=>{const g=E('g',{},w);E('path',{d:'M-120 260 C-120 120 -80 60 0 60 C80 60 120 120 120 260 Z',fill:'#03060b',stroke:P.glow,'stroke-opacity':.3,'stroke-width':3},g);E('circle',{cx:0,cy:-10,r:62,fill:'#03060b',stroke:P.glow,'stroke-opacity':.35,'stroke-width':3},g);jur.push([g,p])});
 const pen=E('line',{stroke:P.ink,'stroke-width':4},w);
 upd=(t)=>{
  const u=t*.7;const x=540+Math.sin(u*2.1)*330*Math.cos(u*.6), y=600+Math.sin(u*1.7+1)*190; // the eye wanders
  dot.setAttribute('cx',x);dot.setAttribute('cy',y);halo.setAttribute('cx',x);halo.setAttribute('cy',y);halo.setAttribute('r',44+8*Math.sin(t*6));
  jur.forEach(([g,p],i)=>{const look=Math.sin(u*2.1+i*.4)*5;g.setAttribute('transform',`translate(${p[0]} ${p[1]+Math.sin(t*1.3+i)*4}) rotate(${look})`)});
  const pt=Math.sin(t*14)>.4?6:0;pen.setAttribute('x1',840);pen.setAttribute('y1',1150+pt);pen.setAttribute('x2',880);pen.setAttribute('y2',1190);
  const z=1+.08*t/DUR;world.setAttribute('transform',`translate(${540-540*z} ${960-960*z}) scale(${z})`);
 };
};
// ---------------- SUN ARC ----------------
F.sunarc=()=>{
 const w=world;const gy=1240;
 const sky=E('rect',{width:1080,height:gy,fill:P.glow,opacity:.0},w);
 const sun=E('circle',{r:70,fill:P.ink},w),sunh=E('circle',{r:190,fill:P.glow,opacity:.25,filter:'url(#bl)'},w);
 E('rect',{x:0,y:gy,width:1080,height:700,fill:'#05080d'},w);E('line',{x1:0,y1:gy,x2:1080,y2:gy,stroke:P.ink,'stroke-opacity':.5,'stroke-width':4},w);
 const hx=470,hw=300,hh=190;
 const shadow=E('polygon',{fill:'#000',opacity:.55},w);
 E('polygon',{points:`${hx},${gy} ${hx},${gy-hh} ${hx+hw/2},${gy-hh-130} ${hx+hw},${gy-hh} ${hx+hw},${gy}`,fill:P.dim,stroke:P.ink,'stroke-width':5,'stroke-linejoin':'round'},w);
 const lit=E('polygon',{fill:P.ink,opacity:0},w);
 [[hx+40,gy-110],[hx+hw-110,gy-110]].forEach(p=>E('rect',{x:p[0],y:p[1],width:70,height:70,fill:'none',stroke:P.ink,'stroke-width':4},w));
 E('rect',{x:hx+hw/2-28,y:gy-100,width:56,height:100,fill:'none',stroke:P.ink,'stroke-width':4},w);
 const clk=E('text',{x:540,y:300,'text-anchor':'middle','font-size':84,'font-weight':800,fill:P.ink,'font-family':'Helvetica,Arial'},w);
 const arcp=E('path',{d:`M110 ${gy-60} A430 ${gy-420} 0 0 1 970 ${gy-60}`,fill:'none',stroke:P.ink,'stroke-opacity':.25,'stroke-width':3,'stroke-dasharray':'8 14'},w);
 upd=(t)=>{
  const u=ease(cl(t/DUR,0,1));const ang=Math.PI*(1-u);const sx=540+Math.cos(ang)*430,sy=(gy-60)-Math.sin(ang)*(gy-420)*0.95;
  sun.setAttribute('cx',sx);sun.setAttribute('cy',sy);sunh.setAttribute('cx',sx);sunh.setAttribute('cy',sy);
  const len=(1-Math.sin(Math.PI*u))*1.0+.25;const dir=Math.cos(ang)>0?-1:1;const sxl=Math.abs(Math.cos(ang))*hh*3.2*1.0+40;
  const side=Math.cos(ang)>0?-1:1; // shadow falls away from the sun
  const base1=side>0?hx+hw:hx, tip=base1+side*(60+ (1-Math.sin(Math.PI*u))*520);
  shadow.setAttribute('points',`${hx},${gy} ${hx+hw},${gy} ${side>0?hx+hw:hx},${gy} ${tip},${gy+0} ${tip},${gy+26} ${base1},${gy+26}`);
  shadow.setAttribute('points',`${base1},${gy} ${tip},${gy} ${tip+side*0},${gy+30} ${base1},${gy+30}`);
  sky.setAttribute('opacity',.1+.22*Math.sin(Math.PI*u));
  const hr=9+Math.floor(u*7);clk.textContent=(hr>12?hr-12:hr)+':00 '+(hr>=12?'PM':'AM');
  const z=1+.06*t/DUR;world.setAttribute('transform',`translate(${540-540*z} ${960-960*z}) scale(${z})`);
 };
};
// ---------------- SCROLL PAST ----------------
F.scroll=()=>{
 const w=world;
 E('rect',{x:230,y:330,width:620,height:1260,rx:70,fill:'#02050a',stroke:P.ink,'stroke-opacity':.5,'stroke-width':6},w);
 const clip=E('clipPath',{id:'pc'},defs);E('rect',{x:250,y:360,width:580,height:1200,rx:46},clip);
 const g=E('g',{'clip-path':'url(#pc)'},w);
 const cards=[];const N=9, CH=420;
 for(let i=0;i<N;i++){const c=E('g',{},g);E('rect',{x:270,y:0,width:540,height:CH-30,rx:18,fill:i===N-3?P.bg2:'#0e1a2b',stroke:P.ink,'stroke-opacity':.25,'stroke-width':2},c);
  const k=i===N-3;[[330,300,750,300],[350,300,350,200],[730,300,730,200],[350,200,540,120],[540,120,730,200],[420,260,480,260],[420,220,480,220],[420,220,420,260],[480,220,480,260]].forEach(l=>E('line',{x1:l[0],y1:l[1],x2:l[2],y2:l[3],stroke:P.ink,'stroke-width':k?5:2,opacity:k?1:.55},c));
  cards.push(c)}
 const ring=E('rect',{x:262,y:0,width:556,height:CH-14,rx:24,fill:'none',stroke:P.acc,'stroke-width':6,opacity:0},w);
 const thumb=E('ellipse',{cx:540,cy:1700,rx:70,ry:110,fill:'#05080d',stroke:P.ink,'stroke-opacity':.4,'stroke-width':3},w);
 const stop=E('text',{x:540,y:290,'text-anchor':'middle','font-size':54,'font-weight':800,fill:P.acc,'font-family':'Helvetica,Arial',opacity:0,'letter-spacing':4},w);stop.textContent='STOPPED.';
 upd=(t)=>{
  const target=(N-3)*CH-(1560-360)/2+CH/2-20; // scroll offset that centres the target card
  const q=cl(t/(DUR*.78),0,1);const off=target*(1-Math.pow(1-q,3));
  cards.forEach((c,i)=>c.setAttribute('transform',`translate(0 ${360+i*CH-off})`));
  const ty=360+(N-3)*CH-off;ring.setAttribute('y',ty-8);ring.setAttribute('opacity',cl((q-.85)/.15,0,1));stop.setAttribute('opacity',cl((q-.9)/.1,0,1));
  const sw=(1-q)>.05?Math.abs(Math.sin(t*5)):0;thumb.setAttribute('cy',1720-sw*180);
  const z=.78*(1+.04*t/DUR);world.setAttribute('transform',`translate(540 790) scale(${z}) translate(-540 -960)`);
 };
};
// ---------------- TAPE MEASURE (clearance) ----------------
F.tape=()=>{
 const w=world;
 E('rect',{x:120,y:420,width:840,height:220,fill:'#0e1a2b',stroke:P.ink,'stroke-width':5},w);
 E('text',{x:540,y:545,'text-anchor':'middle','font-size':52,'font-weight':800,fill:P.ink,'letter-spacing':8,'font-family':'Helvetica,Arial',opacity:.8},w).textContent='COUNTER';
 E('rect',{x:240,y:1010,width:600,height:300,fill:'#16263d',stroke:P.ink,'stroke-width':5},w);
 E('text',{x:540,y:1180,'text-anchor':'middle','font-size':52,'font-weight':800,fill:P.ink,'letter-spacing':8,'font-family':'Helvetica,Arial',opacity:.8},w).textContent='ISLAND';
 const door=E('g',{},w);E('rect',{x:0,y:0,width:240,height:26,fill:P.acc},door);
 const arc=E('path',{fill:'none',stroke:P.acc,'stroke-width':3,'stroke-dasharray':'10 12',opacity:.7},w);
 const tp=E('rect',{x:600,y:640,width:34,height:0,fill:P.ink},w), ticks=[];for(let i=0;i<30;i++)ticks.push(E('line',{x1:600,x2:i%5?620:640,stroke:'#0c1624','stroke-width':3},w));
 const num=E('text',{x:700,y:820,'font-size':130,'font-weight':800,fill:P.acc,'font-family':'Helvetica,Arial'},w);
 const need=E('text',{x:700,y:900,'font-size':44,'font-weight':700,fill:P.ink,'font-family':'Helvetica,Arial',opacity:0},w);need.textContent='42" NEEDED';
 upd=(t)=>{
  const d=ease(cl(t/(DUR*.5),0,1)), ext=d*370; tp.setAttribute('height',ext);
  ticks.forEach((l,i)=>{const y=640+i*(370/30);l.setAttribute('y1',y);l.setAttribute('y2',y);l.setAttribute('opacity',y<640+ext?1:0)});
  num.textContent=Math.round(d*30)+'"';
  const open=ease(cl((t-DUR*.45)/(DUR*.3),0,1));const hit=cl((t-DUR*.75)/.25,0,1);
  const a=open*80;door.setAttribute('transform',`translate(${400} ${640}) rotate(${a})`);
  arc.setAttribute('d',`M${400+240} 640 A240 240 0 0 1 ${400+240*Math.cos(a*Math.PI/180)} ${640+240*Math.sin(a*Math.PI/180)}`);
  need.setAttribute('opacity',cl((t-DUR*.75)/.3,0,1));
  const sh=hit>0&&hit<1?Math.sin(t*60)*6*(1-hit):0;world.setAttribute('transform',`translate(${sh} 0)`);
 };
};

// ---------------- PHOTO (AI image, animated) ----------------
F.photo=()=>{
 const w=world, IM=__IMGS__;
 const els=IM.map(u=>E('image',{href:u,x:-80,y:-140,width:1240,height:2200,preserveAspectRatio:'xMidYMid slice','style':'filter:brightness(1.75) contrast(1.08) saturate(1.1)'},w));
 const wash=E('rect',{x:-100,y:-100,width:1300,height:2200,fill:P.glow,opacity:0,'style':'mix-blend-mode:soft-light'},S);
 const tint=E('rect',{x:-100,y:-100,width:1300,height:2200,fill:P.bg2,opacity:.22,'style':'mix-blend-mode:multiply'},S);
 const dust=[];for(let i=0;i<34;i++)dust.push(E('circle',{r:2+(i%4),fill:P.ink,opacity:.0},S));
 const n=IM.length;
 upd=(t)=>{
  const u=cl(t/DUR,0,1);
  els.forEach((e,i)=>{const seg=1/n, a=i*seg, o=n===1?1:(i===0?1-cl((u-(a+seg-.08))/.08,0,1):cl((u-(a-.0))/.08,0,1)); e.setAttribute('opacity',o);
    const lu=cl((u-a)/seg,0,1.2), dir=i%2?-1:1, z=1.04+.10*(n===1?u:lu); e.setAttribute('transform',`translate(${540} ${960}) scale(${z}) translate(${-540+dir*(-30+60*(n===1?u:lu))} ${-960-20*(n===1?u:lu)})`)});
  const fl=.5+.5*Math.sin(t*7.3)*Math.sin(t*2.9);wash.setAttribute('opacity',.08+.10*fl);
  dust.forEach((d,i)=>{const x=(i*97+t*(14+i%5*6))%1100,y=(i*181+t*(-20-i%3*9)+4000)%1960;d.setAttribute('cx',x);d.setAttribute('cy',y);d.setAttribute('opacity',.12+.25*Math.abs(Math.sin(t*1.7+i)))});
 };
};
F[K]();
const capEl=document.getElementById('cap'),tagEl=document.getElementById('tag');tagEl.textContent=TAG||'';
E('rect',{width:1080,height:1920,fill:'url(#vg)'});
window.setT=t=>{upd(t);capEl.innerHTML=CAP?`<span>${CAP}</span>`:'';
 const p=ease(cl(t/0.35,0,1));capEl.firstChild&&(capEl.firstChild.style.opacity=p,capEl.firstChild.style.transform=`translateY(${(1-p)*22}px)`);
 tagEl.style.opacity=ease(cl(t/0.4,0,1));};
setT(0);
</script>"""
def render(kind, dur, pal, caption, out, tag='', imgs=None):
    out = pathlib.Path(out); fr = out.with_suffix('.frames'); shutil.rmtree(fr, ignore_errors=True); fr.mkdir(parents=True)
    p = PAL[pal]
    html = (HTML.replace('__PAL__', json.dumps(p)).replace('__KIND__', json.dumps(kind)).replace('__DUR__', str(dur)).replace('__CAP__', json.dumps(caption))
            .replace('__TAG__', json.dumps(tag)).replace('__IMGS__', json.dumps([pathlib.Path(i).resolve().as_uri() for i in (imgs or [])])).replace('__ACC__', p['acc']).replace('__INK__', p['ink']))
    hp = out.with_suffix('.html'); hp.write_text(html)
    N = int(dur * FPS)
    with sync_playwright() as pw:
        b = pw.chromium.launch(); pg = b.new_page(viewport={'width': W, 'height': H}); pg.goto(hp.resolve().as_uri()); pg.wait_for_timeout(300)
        for i in range(N):
            pg.evaluate(f'setT({i/FPS})'); pg.screenshot(path=str(fr / f'{i:05d}.jpg'), type='jpeg', quality=92)
        b.close()
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-framerate', str(FPS), '-i', str(fr / '%05d.jpg'), '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20', '-pix_fmt', 'yuv420p', str(out)], check=True)
    shutil.rmtree(fr, ignore_errors=True); return str(out)
if __name__ == '__main__':
    k, d, pal, out = sys.argv[1], float(sys.argv[2]), sys.argv[3], sys.argv[4]
    print(render(k, d, pal, sys.argv[5] if len(sys.argv) > 5 else '', out))
