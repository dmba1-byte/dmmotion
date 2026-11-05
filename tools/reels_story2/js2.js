const NS='http://www.w3.org/2000/svg',$=id=>document.getElementById(id);
const ST=__STARTS__;
const cl=(x,a,b)=>Math.min(b,Math.max(a,x)),ez=x=>x<.5?2*x*x:1-Math.pow(-2*x+2,2)/2,seg=(t,a,b)=>cl((t-a)/(b-a),0,1),lerp=(a,b,u)=>a+(b-a)*u;
const mk=(p,tag,at)=>{const e=document.createElementNS(NS,tag);for(const k in at)e.setAttribute(k,at[k]);p.appendChild(e);return e};
document.querySelectorAll('.spk').forEach(g=>{for(let i=0;i<36;i++){const a=i*10*Math.PI/180;mk(g,'line',{x1:Math.cos(a)*26,y1:Math.sin(a)*26,x2:Math.cos(a)*156,y2:Math.sin(a)*156})}});
// ---------- geometry
const R=230,H=150,X0=1000,NST=17;
const tread=n=>n<=0?{x:X0+(n-1)*R+R/2,y:0}:{x:X0+(n-1)*R+R/2,y:-n*H};
const yl=x=>{const u=(x-X0)/R; const k=Math.log(1+Math.exp(u*4))/4; return -k*H}; // smooth stair line
// ---------- world static
(()=>{const g=$('stairG');
 let d='M-1600,0 L'+X0+',0';
 for(let n=1;n<=NST;n++){d+=` L${X0+(n-1)*R},${-n*H} L${X0+n*R},${-n*H}`}
 d+=` L${X0+NST*R},900 L-1600,900 Z`;
 mk(g,'path',{d,fill:'url(#stone)'});
 // risers (dark) + edges
 for(let n=1;n<=NST;n++){mk(g,'rect',{x:X0+(n-1)*R-6,y:-n*H,width:10,height:H,fill:'#111218',opacity:.9});mk(g,'rect',{x:X0+(n-1)*R,y:-n*H,width:R,height:5,fill:'#f0dcc0',opacity:.55});mk(g,'path',{d:`M${X0+(n-1)*R},${-n*H} L${X0+(n-1)*R},${-(n-1)*H}`,stroke:'#0a0b0e',"stroke-width":9})}
 mk(g,'rect',{x:-1600,y:0,width:X0+1600,height:6,fill:'#c9bda8',opacity:.45});
 // shade lower
 mk(g,'rect',{x:-1600,y:6,width:5200,height:900,fill:'#0b0c10',opacity:.55});
 // chairs left behind
 const cw=$('chairsW');[[-900,.6],[-640,.55],[-1180,.6],[-380,.58]].forEach(([x,sc])=>{const gg=mk(cw,'g',{transform:`translate(${x},0) scale(${sc})`,opacity:.9});mk(gg,'use',{href:'#chairsym'})});
 // photographers at top
 const ph=$('photog');[[10,0],[11,40],[12,-30],[13,20],[14,-10],[12.6,70]].forEach(([n,dx],i)=>{const t=tread(n);const x=t.x+dx,y=t.y;const gg=mk(ph,'g',{transform:`translate(${x},${y})`,opacity:.9});
  mk(gg,'path',{d:'M0,0 L0,-170 M0,-170 L40,-210',stroke:'#0f1116',"stroke-width":46,"stroke-linecap":'round',fill:'none'});mk(gg,'circle',{cx:2,cy:-250,r:36,fill:'#0f1116'});mk(gg,'rect',{x:30,y:-240,width:70,height:50,rx:6,fill:'#0a0b0e'});mk(gg,'circle',{cx:104,cy:-215,r:20,fill:'#1d2028'})});
 // far columns (screen space)
 const fc=$('farcol');for(let i=0;i<9;i++){mk(fc,'rect',{x:60+i*140,y:300,width:56,height:700,fill:'#2c3542'})}mk(fc,'rect',{x:0,y:260,width:1080,height:50,fill:'#222a35'});
})();
// ---------- rig
const COL={jacket:'#223f4b',pants:'#171922',shoe:'#0c0c10',skin:'#9c6a4a',hair:'#150e0b',head:'#7a523b'};
function buildFig(parent,dim){
 const o={};
 const part=(name,wid,col)=>{const g=mk(parent,'g',{});o[name]={rim:mk(g,'path',{fill:'none',stroke:'#ffd9a8',"stroke-width":wid+5,"stroke-linecap":'round',"stroke-linejoin":'round',opacity:.55*dim,transform:'translate(5,-6)'}),dk:mk(g,'path',{fill:'none',stroke:col,"stroke-width":wid,"stroke-linecap":'round',"stroke-linejoin":'round',opacity:dim}),w:wid};return o[name]};
 part('armF',40,'#162d37');part('legF',56,'#101118');
 o.handF=mk(parent,'ellipse',{rx:34,ry:19,fill:'#6e4a35',opacity:dim});o.shoeF=mk(parent,'ellipse',{rx:46,ry:22,fill:'#090a0d',opacity:dim});
 part('torso',118,COL.jacket);part('legN',60,COL.pants);part('armN',44,'#2a4c5a');
 o.handN=mk(parent,'ellipse',{rx:36,ry:20,fill:COL.skin,opacity:dim});o.shoeN=mk(parent,'ellipse',{rx:48,ry:23,fill:COL.shoe,opacity:dim});
 o.tail=mk(parent,'path',{fill:'none',stroke:COL.hair,"stroke-width":30,"stroke-linecap":'round',opacity:dim});
 o.head=mk(parent,'circle',{r:80,fill:COL.head,opacity:dim});o.hair=mk(parent,'path',{fill:COL.hair,opacity:dim});
 o.brace=mk(parent,'path',{fill:'none',stroke:'#d6d9de',"stroke-width":6,"stroke-linecap":'round',opacity:.55*dim});
 return o}
const P=(a,b)=>`M${a.x.toFixed(1)},${a.y.toFixed(1)} L${b.x.toFixed(1)},${b.y.toFixed(1)}`;
const P3=(a,b,c)=>`M${a.x.toFixed(1)},${a.y.toFixed(1)} L${b.x.toFixed(1)},${b.y.toFixed(1)} L${c.x.toFixed(1)},${c.y.toFixed(1)}`;
function setFig(o,p){
 const set=(k,d)=>{o[k].rim.setAttribute('d',d);o[k].dk.setAttribute('d',d)};
 set('armF',P3(p.sh,p.elbF,p.handF));set('legF',P3(p.hip,p.kneeF,p.ankF));set('torso',P(p.hip,p.sh));set('legN',P3(p.hip,p.kneeN,p.ankN));set('armN',P3(p.sh,p.elbN,p.handN));
 o.handF.setAttribute('cx',p.handF.x);o.handF.setAttribute('cy',p.handF.y+6);o.handN.setAttribute('cx',p.handN.x);o.handN.setAttribute('cy',p.handN.y+6);
 const ang=(a,b)=>Math.atan2(b.y-a.y,b.x-a.x)*180/Math.PI;
 o.shoeN.setAttribute('transform',`translate(${p.ankN.x},${p.ankN.y}) rotate(${p.shoeAng||0})`);o.shoeF.setAttribute('transform',`translate(${p.ankF.x},${p.ankF.y}) rotate(${p.shoeAng||0})`);
 o.head.setAttribute('cx',p.head.x);o.head.setAttribute('cy',p.head.y);
 // hair cap + ponytail trailing back (away from travel dir = -x)
 const hx=p.head.x,hy=p.head.y; const bx=p.back||{x:-1,y:.2};
 o.hair.setAttribute('d',`M${hx-84},${hy+6} A84,84 0 0 1 ${hx+70},${hy-40} Q${hx+10},${hy-70} ${hx-30},${hy-20} Q${hx-60},${hy+10} ${hx-84},${hy+6} Z`);
 o.tail.setAttribute('d',`M${hx-70},${hy-18} Q${hx-130},${hy+10+(p.sway||0)} ${hx-150},${hy+80+(p.sway||0)*1.4}`);
 o.brace.setAttribute('d',P(p.kneeN,p.ankN));
}
// ---------- IK
function ik(a,t,l1,l2,pickUp){
 let dx=t.x-a.x,dy=t.y-a.y;let d=Math.hypot(dx,dy);const mx=l1+l2-2,mn=Math.abs(l1-l2)+2;const dd=cl(d,mn,mx);
 const tx={x:a.x+dx/(d||1)*dd,y:a.y+dy/(d||1)*dd};const ang=Math.atan2(dy,dx);
 const A=Math.acos(cl((l1*l1+dd*dd-l2*l2)/(2*l1*dd),-1,1));
 const e1={x:a.x+l1*Math.cos(ang+A),y:a.y+l1*Math.sin(ang+A)},e2={x:a.x+l1*Math.cos(ang-A),y:a.y+l1*Math.sin(ang-A)};
 const e=pickUp?(e1.y<e2.y?e1:e2):(e1.y>e2.y?e1:e2);return {mid:e,end:tx}}
// ---------- crawl pose from stair progress s
const HIPX0=470;
const surf=x=>{if(x<X0)return 0;return -(Math.floor((x-X0)/R)+1)*H};
function swingPt(n,p,a,b,off,hold,arc){ // limb moves tread(n)->tread(n+1) when p in [a,b]
 const u=ez(seg(p,a,b)),A=tread(n),B=tread(n+1);
 return {x:lerp(A.x,B.x,u)+off,y:lerp(A.y,B.y,u)-hold-Math.sin(Math.PI*u)*arc};
}
function crawlPose(s,rest,tt){
 const n=Math.floor(s),p=s-n;
 const hipx=HIPX0+s*R;
 const frac=cl((yl(hipx)-yl(hipx+330))/(330*H/R),0,1);
 const th=Math.atan(H/R)*frac+.44+(rest?-.06:0);
 const breath=rest?Math.sin(tt*2.6)*9:0;
 const sway=rest?0:Math.sin(p*Math.PI*2);
 const hip={x:hipx+(rest?0:Math.sin(p*Math.PI*2+1)*10),y:Math.min(yl(hipx),yl(hipx+60))-185+(rest?38:0)+(rest?0:Math.abs(Math.sin(p*Math.PI))*-10)};
 const sh={x:hip.x+380*Math.cos(th),y:hip.y-380*Math.sin(th)+(rest?34:0)+breath+(rest?0:sway*10)};
 // diagonal gait: handA+kneeB swing first half, handB+kneeA second half
 const hA=swingPt(n,p,0,.5,-10,24,95), hB=swingPt(n,p,.5,1,24,24,95);
 const kB=swingPt(n,p,0,.5,40,30,70),   kA=swingPt(n,p,.5,1,10,30,70);
 // hands/knees one tread ahead of where they stand at p=0: shift targets forward by one tread offset
 const aH=ik(sh,hA,225,205,true),bH=ik(sh,hB,225,205,true);
 const clampK=k=>{const dx=k.x-hip.x,dy=k.y-hip.y,d=Math.hypot(dx,dy),m=250;return d>m?{x:hip.x+dx/d*m,y:hip.y+dy/d*m}:k};
 const KA=clampK(kA),KB=clampK(kB);
 const foot=k=>{const fx=k.x-215;return {x:fx,y:Math.min(surf(fx)-26,k.y+10)}};
 const hl=rest?-.55:0;
 const head={x:sh.x+112*Math.cos(th+.22+hl),y:sh.y-112*Math.sin(th+.22+hl)+(rest?30:0)};
 return {hip,sh,head,kneeN:KA,ankN:foot(KA),elbN:aH.mid,handN:aH.end,kneeF:KB,ankF:foot(KB),elbF:bH.mid,handF:bH.end,shoeAng:-4,sway:Math.sin(s*Math.PI*2+1)*10};
}
// ---------- seated / transfer keyframes (ox = chair origin)
const OX=-250;
const sp=(x,y)=>({x:OX+x,y});
const seated={hip:sp(330,-330),sh:sp(300,-730),head:sp(318,-830),kneeN:sp(560,-350),ankN:sp(655,-130),elbN:sp(345,-520),handN:sp(352,-382),kneeF:sp(585,-345),ankF:sp(675,-128),elbF:sp(365,-520),handF:sp(372,-384),shoeAng:70,sway:0};
const lean={hip:sp(405,-380),sh:sp(500,-700),head:sp(585,-770),kneeN:sp(630,-320),ankN:sp(700,-120),elbN:sp(440,-520),handN:sp(395,-388),kneeF:sp(655,-315),ankF:sp(722,-118),elbF:sp(458,-520),handF:sp(415,-392),shoeAng:70,sway:10};
const slide={hip:sp(640,-200),sh:sp(830,-470),head:sp(930,-500),kneeN:sp(790,-110),ankN:sp(690,-40),elbN:sp(840,-290),handN:sp(905,-110),kneeF:sp(815,-105),ankF:sp(712,-42),elbF:sp(862,-300),handF:sp(930,-108),shoeAng:20,sway:25};
function mixPose(a,b,u){const o={};for(const k in a){if(typeof a[k]==='number')o[k]=lerp(a[k],b[k],u);else o[k]={x:lerp(a[k].x,b[k].x,u),y:lerp(a[k].y,b[k].y,u)}}return o}
function girlPose(t){
 const rest0=crawlPose(0,false,0);
 if(t<5.3){const m=Math.sin(t*2)*4;const p=JSON.parse(JSON.stringify(seated));p.sh.y+=m;p.head.y+=m*1.2;p.head.x+=Math.min(1,t/4)*14;return p}
 if(t<6.3)return mixPose(seated,lean,ez(seg(t,5.3,6.3)));
 if(t<7.3)return mixPose(lean,slide,ez(seg(t,6.3,7.3)));
 if(t<8.6)return mixPose(slide,rest0,ez(seg(t,7.3,8.6)));
 return crawlPose(sT(t),isRest(t),t);
}
const GAIT=1.9;const sT=t=>{ if(t<16.25)return 0; if(t<24.6)return (t-16.25)/GAIT; if(t<26.4)return (24.6-16.25)/GAIT; return (24.6-16.25)/GAIT+(t-26.4)/GAIT };
const isRest=t=>t>=24.6&&t<26.4;
// build main girl + crowd
const girl=buildFig($('girl'),1);
const crowdS=[-3.6,-2.4,2.6,3.5,4.6,5.7,6.9,8.1,9.3,10.5,11.7],crowd=[];
crowdS.forEach((s0,i)=>{const g=mk($('crowd'),'g',{});g.setAttribute('style','filter:brightness(.55)');g.setAttribute('opacity',.8);crowd.push({o:buildFig(g,1),s0})});
// camera
function cam(t){
 if(t<10.5){ // hook
  const k=[[0,620,-1000,.5],[5.3,520,-760,.78],[8.4,700,-460,.95],[10.5,1250,-1050,.62]];
  for(let i=0;i<k.length-1;i++){if(t<=k[i+1][0]){const u=ez(seg(t,k[i][0],k[i+1][0]));return {cx:lerp(k[i][1],k[i+1][1],u),cy:lerp(k[i][2],k[i+1][2],u),z:lerp(k[i][3],k[i+1][3],u)}}}
 }
 const s=sT(t),hx=HIPX0+s*R,hy=yl(hx)-175;
 const fol={cx:hx+190,cy:hy-330,z:.78};
 const wide={cx:900,cy:-1150,z:.46};
 let b=0; // wide blend
 if(t<20.4)b=1-ez(seg(t,16.05,16.9))*0; // start wide
 const w1=1-ez(seg(t,19.6,21.4)); // wide->follow
 const topv=ez(seg(t,28.0,29.9)); // tilt up to the top
 let c={cx:lerp(fol.cx,wide.cx,w1),cy:lerp(fol.cy,wide.cy,w1),z:lerp(fol.z,wide.z,w1)};
 c={cx:lerp(c.cx,hx+420,topv),cy:lerp(c.cy,hy-720,topv),z:lerp(c.z,.66,topv)};
 return c}
// flashes
const FL=[17.4,18.9,19.8,21.5,22.7,24.2,27.1,28.4,29.2];
const flashEls=[];(()=>{const g=$('flashes');const spots=[[10,0],[11,40],[12,-30],[13,20],[14,-10],[12.6,70]];spots.forEach(([n,dx],i)=>{const t=tread(n);flashEls.push(mk(g,'circle',{cx:t.x+dx+105,cy:t.y-215,r:150,fill:'#fff6e0',opacity:0,filter:'url(#blur)'}))})})();
// ---------- doors scene helpers
(()=>{const g=$('ticks');for(let i=0;i<12;i++){const a=i*30*Math.PI/180;mk(g,'line',{x1:Math.sin(a)*100,y1:-Math.cos(a)*100,x2:Math.sin(a)*112,y2:-Math.cos(a)*112})}})();
(()=>{const g=$('lines');for(let i=0;i<16;i++){mk(g,'rect',{x:-300,y:-350+i*30,width:600-((i*97)%140),height:8,rx:3})}})();
(()=>{const g=$('grid');for(let x=0;x<=1080;x+=90)mk(g,'line',{x1:x,y1:0,x2:x,y2:1920});for(let y=0;y<=1920;y+=90)mk(g,'line',{x1:0,y1:y,x2:1080,y2:y})})();
const T={s2:ST[2]-.2,s3:ST[3]-.2,s5:ST[4]+5.7,s6:ST[5],s7:ST[6]-.1,s8:ST[7]-.1,s9:ST[8]-.2};
const SC=['wsc','s2','s6','s7','s9'];
const show=id=>SC.forEach(s=>$(s).style.display=s===id?'':'none');
function setT(t){
 const cap=$('cap'),qt=$('quote'),at=$('attr'),dt=$('date'),lab=$('lab'),ld=$('lead'),cta=$('cta');
 cap.style.opacity=0;qt.style.opacity=0;at.style.opacity=0;dt.style.opacity=0;lab.style.opacity=0;ld.setAttribute('opacity',0);cta.style.opacity=0;
 $('black').style.display='none';cap.style.top='230px';lab.style.left='60px';lab.style.top='1560px';
 let scene='wsc';
 if(t>=T.s2&&t<T.s3)scene='s2'; if(t>=T.s6)scene='s6'; if(t>=T.s7)scene='s7'; if(t>=T.s9)scene='s9';
 show(scene);
 if(t>=T.s5&&t<T.s6){$('black').style.display='';}
 if(scene==='wsc'){
  const c=cam(t);$('world').setAttribute('transform',`translate(${540-c.cx*c.z},${960-c.cy*c.z}) scale(${c.z})`);
  $('farcol').setAttribute('transform',`translate(${-c.cx*.06},${c.cy*.05})`);
  setFig(girl,girlPose(t));
  const s=sT(t);
  crowd.forEach((c0,i)=>{const ss=c0.s0+ (t>=T.s3? (t-T.s3)/GAIT*(.92+.04*(i%4)):0);const p=crawlPose(ss,false,t);setFig(c0.o,p);});
  $('crowd').style.opacity=t>=T.s3?1:0;
  $('chairsW').style.opacity=1;
  flashEls.forEach((e,i)=>{let o=0;FL.forEach((f,j)=>{if((i+j)%3===0||(i*2+j)%4===1){const d=t-f-i*.07;if(d>0&&d<.18)o=Math.max(o,1-d/.18)}});e.setAttribute('opacity',o*.9)});
  $('mainChair').setAttribute('transform',`translate(${OX},0)`);
  const sl=t<10.5;
  if(sl){
   dt.textContent='MARCH 12, 1990 · 6:40 AM';dt.style.opacity=seg(t,.3,1)*(1-seg(t,9.5,10.2));
   if(t<7.0){cap.textContent='Eight years old.';cap.style.opacity=seg(t,3.2,3.7)*(1-seg(t,6.3,6.8))}
   else{cap.textContent='Why leave the chair?';cap.style.opacity=seg(t,8.0,8.5)*(1-seg(t,10.0,10.5))}
  } else {
   if(t<ST[4]){cap.textContent='About sixty people.';cap.style.opacity=seg(t,ST[3]+.3,ST[3]+.9)*(1-seg(t,ST[3]+3.4,ST[3]+4.0));
     lab.textContent='≈60 CHAIRS LEFT AT THE BOTTOM';lab.style.top='1540px';lab.style.opacity=seg(t,ST[3]+.6,ST[3]+1.2)*(1-seg(t,ST[3]+3.4,ST[3]+4.0))}
   else if(t<ST[4]+2.0){cap.textContent='She stops. Asks for water.';cap.style.opacity=seg(t,24.7,25.2)*(1-seg(t,26.0,26.4))}
   else if(t<ST[4]+3.6){cap.textContent='Then keeps going.';cap.style.opacity=seg(t,26.5,27.0)*(1-seg(t,27.8,28.1))}
   if(t>=27.9){$('quoteG').firstElementChild.setAttribute('opacity',.6*seg(t,27.9,28.7));qt.innerHTML='“I’ll take all night,<br>if I have to.”';qt.style.opacity=seg(t,28.1,28.8);at.style.opacity=seg(t,29.0,29.6)}
   else $('quoteG').firstElementChild.setAttribute('opacity',0);
  }
 }
 if(scene==='s2'){
  const u=t-T.s2;
  const z=1+.07*seg(u,0,5.8);$('doorsG').setAttribute('transform',`translate(${540-540*z},${1000-1000*z}) scale(${z})`);
  const sp=u*.35;$('mh').setAttribute('transform',`rotate(${sp*360*2})`);$('hh').setAttribute('transform',`rotate(${sp*60})`);
  const b=$('bars');b.style.opacity=1;
  const k1=seg(t,14.0,14.18),k2=seg(t,15.0,15.18);
  const kids=b.children; // [rect,text,text,rect,text,text]
  const set=(i,o)=>{kids[i].setAttribute('opacity',o)};
  [0,1,2].forEach(i=>set(i,k1)); [3,4,5].forEach(i=>set(i,k2));
  const sc1=1+.35*(1-k1),sc2=1+.35*(1-k2);
  b.children[0].parentNode;
  cap.style.top='1660px';
  cap.textContent=t<13.6?'A law. Sitting still.':'Senate: yes. House: wait.';cap.style.opacity=seg(u,.6,1.1)*(1-seg(u,5.0,5.4));
 }
 if(scene==='s6'){
  const u=t-T.s6;
  $('sig').setAttribute('stroke-dashoffset',900*(1-ez(seg(u,1.0,3.4))));
  dt.textContent='JULY 26, 1990';dt.style.opacity=seg(u,.2,.8);
  cap.textContent='Four months later.';cap.style.opacity=seg(u,.3,.8)*(1-seg(u,3.2,3.7));
  const z=1+.03*seg(u,0,4.6);$('s6').setAttribute('transform',`translate(${540-540*z},${960-960*z}) scale(${z})`);
 }
 if(scene==='s7'){
  const u=t-T.s7;
  $('rampSurf').setAttribute('stroke-dasharray',1000);$('rampSurf').setAttribute('stroke-dashoffset',1000*(1-seg(u,.2,1.6)));$('rampFill').setAttribute('opacity',seg(u,1,1.8));
  $('railG').setAttribute('opacity',seg(u,3.6,4.8));
  $('c1').setAttribute('opacity',seg(u,1.6,2.2));$('c2').setAttribute('opacity',seg(u,5.2,5.8)*(1-.8*seg(t,T.s8,T.s8+1.2)));
  $('ghost').setAttribute('opacity',seg(t,T.s8,T.s8+1.6)*.9);
  if(t<T.s8){cap.textContent='Every ramp has a number.';cap.style.opacity=seg(u,.1,.7)}
  else{cap.textContent='You’re on her steps.';cap.style.opacity=seg(t,T.s8+1.4,T.s8+2.0)}
 }
 if(scene==='s9'){cta.style.opacity=seg(t-T.s9,.2,.9)}
}
setT(0);
