const walkLegs=(p,a=28,k=45)=>[st(a*S(p),a*S(p)-k*mx0(0,C(p))),st(-a*S(p),-a*S(p)-k*mx0(0,-C(p)))];
const BGS={dusk:['#2a2545','#5a3f6b','#d58a74'],night:['#10142a','#1c2447','#2f3a66'],day:['#7fb6e0','#b8dcf0','#f2e7c9'],rain:['#3a4458','#56627a','#7d8aa0'],warm:['#3d2f55','#8a5a6a','#f0b07a'],mtn:['#5a6fa0','#9ab0d0','#f2d9b5'],pool:['#79c0e6','#bfe6f5','#f5f0d8'],wall:['#2b2a3a','#4a4560','#c97b6a'],park:['#6fa8d8','#a8d4ec','#e8e0b8']};
const frac=x=>x-Math.floor(x);
const A=[];
// 1 BIKE -------------------------------------------------
A.push({n:'1  Ride a bike',bg:'dusk',f:(t,fr)=>{const a=t*PI2*2,bb=[31,62],pe=(k)=>[bb[0]+Math.cos(a+k*PI)*4,bb[1]+Math.sin(a+k*PI)*4];
 const hip=[29,50],grip=[44,48];
 return{hip,lean:34,legIK:[pe(0),pe(1)],armIK:[grip,grip],arms:[{ua:0,fa:0},{ua:0,fa:0}],face:'n',mouth:'smile',dy:Math.round(S(a*2)*.5),
  scene:(g)=>{city(g,fr*5,'#38305a');ground(g,'#3a2a3f','#5a4560')},
  propBack:(g)=>{const wa=a*1.5;
   [[19,60],[43,60]].forEach(w=>{ring(g,w[0],w[1],9,'#8a8aa8');ring(g,w[0],w[1],8,'#2a2a3c');for(let k=0;k<3;k++){const q=wa+k*PI/3;line(g,w[0]-Math.cos(q)*8,w[1]-Math.sin(q)*8,w[0]+Math.cos(q)*8,w[1]+Math.sin(q)*8,1,'#b8b8cc')}});
   line(g,19,60,31,62,1,'#e0534a');line(g,31,62,28,51,1,'#e0534a');line(g,28,51,41,50,1,'#e0534a');line(g,41,50,31,62,1,'#e0534a');line(g,41,50,43,60,1,'#c0443c');line(g,41,50,43,46,1,'#c0443c');line(g,43,46,45,47,2,'#2a2a3c');R(g,25,49,6,2,'#2a2a3c');
   const p0=pe(1);R(g,p0[0]-1,p0[1],3,1,'#2a2a3c')}}}});
// 2 DRINK ------------------------------------------------
A.push({n:'2  Drink from a cup',bg:'warm',f:(t)=>{
 const lift=sm(t<.3?t/.3:t<.7?1:t<.92?1-(t-.7)/.22:0),sip=t>.38&&t<.62?sm((t-.38)/.06)*(1-sm((t-.56)/.06)):0;
 const phi=lift*58+sip*14;const dr=lift>.9;
 const hand=[lerp(8,9.2,lift),lerp(7,-3.6,lift)];
 return{legs:[st(5,5),st(-5,-5)],arms:[{ua:0,fa:0},{ua:6,fa:12}],armRel:[hand,null],lean:dr?-3:2,hy:dr?-1:0,face:dr?'closed':'n',mouth:'flat',
  scene:(g)=>{city(g,0,'#4a3a66');ground(g,'#3a2a3f','#5a4560')},
  prop:(g,i)=>{const h=i.h[0],r=rad(phi);const rim=[h[0]-Math.sin(r)*3.5,h[1]-Math.cos(r)*3.5],bs=[h[0]+Math.sin(r)*2.5,h[1]+Math.cos(r)*2.5];
   line(g,bs[0],bs[1],rim[0],rim[1],4,'#f2efe6');line(g,rim[0]+Math.sin(r)*.5,rim[1]+Math.cos(r)*.5,rim[0]+Math.sin(r)*.5,rim[1]+Math.cos(r)*.5,3,'#7a4a2a');
   line(g,bs[0]+2,bs[1]-1,bs[0]+3,bs[1]+1,1,'#d8d0c4');
   if(lift<.8&&lift>.1){px(g,rim[0]-1,rim[1]-3-((t*32)%4),'#e8e0f0');px(g,rim[0]+1,rim[1]-5-((t*32+2)%4),'#e8e0f0')}
   R(g,h[0]-1,h[1]-1,3,3,K.skin)}}}});
// 3 FLASHLIGHT -------------------------------------------
A.push({n:'3  Flashlight on',bg:'night',f:(t,fr)=>{const on=t>.45,s=sm(t/.3),aim=on?S(t*PI2)*4:0;
 return{legs:[st(6,6),st(-6,-6)],arms:[{ua:0,fa:0},{ua:6,fa:12}],armRel:[[lerp(6,12,s),lerp(9,3,s)],null],lean:2,face:on?'happy':'n',mouth:on?'smile':'flat',
  scene:(g)=>{ground(g,'#1c2038','#2f3a66');R(g,52,22,12,47,'#2c3050');R(g,53,23,10,46,'#33385a');R(g,55,38,7,9,on?'#3d7fc4':'#27456b');if(on){R(g,57,40,3,1,'#fff');R(g,58,41,1,3,'#fff');R(g,57,44,1,2,'#fff');R(g,59,44,1,2,'#fff')}for(let k=0;k<10;k++)px(g,3+k*6,4+(k*13)%20,'#cfd6ff')},
  prop:(g,i)=>{const h=i.h[0];R(g,h[0],h[1]-1,6,3,'#7a7f99');R(g,h[0]+5,h[1]-2,2,5,on?'#fff3b0':'#9aa0b8');R(g,h[0]-1,h[1]-1,3,3,K.skin)},
  overlay:(g,i)=>{if(!on)return;const hh=i.h[0],x=hh[0]+7,y=hh[1];g.fillStyle='rgba(255,240,170,.28)';g.beginPath();g.moveTo(x,y);g.lineTo(64,y-18+aim);g.lineTo(64,y+18+aim);g.closePath();g.fill();g.fillStyle='rgba(255,240,170,.22)';g.beginPath();g.moveTo(x,y);g.lineTo(64,y-9+aim);g.lineTo(64,y+9+aim);g.closePath();g.fill();g.fillStyle='rgba(255,240,170,.25)';g.fillRect(0,GY-1,64,3)}}}});
// 4 THROW -------------------------------------------------
A.push({n:'4  Throw a ball',bg:'day',f:(t,fr)=>{const w=t<.4?sm(t/.4):1,th=t>=.4&&t<.55?sm((t-.4)/.15):t>=.55?1:0,fo=t>.55?sm((t-.55)/.35):0;
 let ua=lerp(20,-120,w);ua=lerp(ua,125,th);ua=lerp(ua,40,fo);const lean=lerp(0,-9,w)+lerp(0,22,th)-lerp(0,10,fo);
 const legs=[st(lerp(6,22,w),lerp(6,10,w)),st(lerp(-6,-24,w),lerp(-6,-28,w))];
 return{legs,arms:[{ua,fa:ua-(th<1?15:-20)},{ua:lerp(10,80,w)-th*60,fa:lerp(10,95,w)-th*50}],lean,face:th>0?'o':'n',mouth:th>0?'small':'flat',
  scene:(g)=>{city(g,0,'#a8c8de');ground(g,'#7aa86a','#8fc07c');for(let k=0;k<8;k++)px(g,4+k*8,GY+3+(k%3),'#6a9a5a')},
  prop:(g,i)=>{const h=i.h[0];if(t<.52){R(g,h[0]-1,h[1]-1,4,4,'#e0534a');R(g,h[0]-1,h[1]-1,3,3,K.skin);R(g,h[0],h[1],3,3,'#e0534a')}else{const tau=(t-.52)*16;const rx=infoRel.rx+tau*6,ry=infoRel.ry-tau*1.5+.35*tau*tau;for(let k=1;k<4;k++)px(g,rx-k*5,ry+k*1.1,'rgba(255,255,255,.5)');R(g,rx,ry,4,4,'#e0534a');px(g,rx+1,ry+1,'#f78a7e')}}}}});
// 5 STAIRS ------------------------------------------------
A.push({n:'5  Climb stairs',bg:'dusk',f:(t,fr)=>{const U=t*4,u=U%1,par=Math.floor(U)%2;
 const stance=[3-6*u,14+4*u],swing=[-3+6*u,18-4*u-5*S(PI*u)];const rel=par==0?[stance,swing]:[swing,stance];
 const top=(x)=>{const j=Math.round((x-35+6*U)/6);return 53-4*j+4*U};
 return{hip:[32,38-S(u*PI)*1],legRel:rel,arms:[{ua:-22*(par?1:-1)*S(u*PI),fa:20},{ua:22*(par?1:-1)*S(u*PI),fa:30}],lean:12,face:'n',mouth:'smile',
  scene:(g)=>{g.fillStyle='#2e2848';for(let x=0;x<64;x++)g.fillRect(x,Math.round(top(x)),1,80);g.fillStyle='#5a4a78';for(let x=0;x<64;x++)g.fillRect(x,Math.round(top(x)),1,1);line(g,0,Math.round(top(0)-24),64,Math.round(top(64)-24),1,'#9aa0c8')}}}});
// 6 HIKE (on the slope) ----------------------------------
A.push({n:'6  Hike up a mountain',bg:'mtn',f:(t,fr)=>{const U=t*4,u=U%1,par=Math.floor(U)%2,K0=.55,yS=(x)=>62-K0*(x-32),H0=16.6,hipX=32,hipY=yS(32)-H0;
 const foot=(rx,lift)=>[rx,H0-1-K0*rx-lift];
 const st_=foot(6-12*u,0),sw_=foot(-6+12*u,4*S(PI*u));const legRel=par==0?[st_,sw_]:[sw_,st_];
 const ph=frac(U/2);let tipRel,lift=0;if(ph<.6)tipRel=12-20*ph;else{const q=(ph-.6)/.4;tipRel=lerp(0,12,sm(q));lift=3*S(PI*q)}
 const tip=[hipX+tipRel,yS(hipX+tipRel)-lift];
 return{hip:[hipX,hipY-S(u*PI)*1],legRel,arms:[{ua:0,fa:0},{ua:-26*(par?-1:1)*S(u*PI)+10,fa:30}],armRel:[[8,6],null],lean:23,face:'n',mouth:'smile',
  scene:(g)=>{g.fillStyle='#8a90b8';[[10,30,20],[34,18,26],[56,32,18]].forEach(m=>{g.beginPath();g.moveTo(m[0]-m[2],60);g.lineTo(m[0],m[1]);g.lineTo(m[0]+m[2],60);g.fill()});
   g.fillStyle='#f4f4fb';g.beginPath();g.moveTo(29,28);g.lineTo(34,18);g.lineTo(39,28);g.fill();
   g.fillStyle='#6a5a4a';g.beginPath();g.moveTo(0,80);for(let x=0;x<=64;x++)g.lineTo(x,yS(x));g.lineTo(64,80);g.fill();
   for(let k=-1;k<8;k++){const x=k*12-(12*U)%12;R(g,x,yS(x)+4,2,1,'#4e4034');R(g,x+5,yS(x+5)+8,3,1,'#8a7a66')}
   g.fillStyle='#8a7a66';for(let x=0;x<64;x++)g.fillRect(x,Math.round(yS(x)),1,1)},
  prop:(g,i)=>{const h=i.h[0];line(g,h[0],h[1],tip[0],tip[1],1,'#d9d2c0');R(g,h[0]-1,h[1]-1,3,3,K.skin)}}}});
// 7 DIVE ---------------------------------------------------
A.push({n:'7  Dive into a pool',bg:'pool',f:(t,fr)=>{
 let hip=[20,31],rot=0,face='n',arms=[{ua:12,fa:18},{ua:8,fa:14}],legs=[st(4,4),st(-4,-4)],lean=0,hide=0,dip=0,mask=1;
 const T0=.26,T1=.72;
 if(t<.1){}
 else if(t<.2){const k=sm((t-.1)/.1);arms=[{ua:lerp(12,-70,k),fa:lerp(18,-70,k)},{ua:lerp(8,-62,k),fa:lerp(14,-55,k)}];legs=[st(lerp(4,34,k),lerp(4,-40,k)),st(lerp(-4,26,k),lerp(-4,-44,k))];lean=lerp(0,14,k);dip=1}
 else if(t<T0){const k=sm((t-.2)/(T0-.2));arms=[{ua:lerp(-70,165,k),fa:lerp(-70,172,k)},{ua:lerp(-62,160,k),fa:lerp(-55,168,k)}];legs=[st(lerp(34,0,k),lerp(-40,0,k)),st(lerp(26,-2,k),lerp(-44,-2,k))];lean=lerp(14,-2,k);dip=k<.5?1:0}
 else if(t<T1){const u=(t-T0)/(T1-T0);hip=[20+30*u,31-28*u+80*u*u];const tuck=S(PI*mn(1,u/.7))*mx0(0,1-u*1.1);
   arms=[{ua:172,fa:178},{ua:168,fa:175}];legs=[st(8+38*tuck,8-60*tuck),st(2+34*tuck,2-56*tuck)];rot=170*sm(u/.62);face='closed';lean=0}
 else if(t<.9){hide=1}
 else{mask=t<.95?.4:1;hip=[20,31]}
 return{hip,legs,arms,lean,rot,face,mouth:'small',nobag:1,hide,mask,
  scene:(g)=>{g.fillStyle='#d9cfae';g.fillRect(0,70,26,10);R(g,6,48+dip,19,2,'#e8e0c8');R(g,6,50+dip,19,1,'#a89f80');R(g,7,51,3,19,'#8a8470');g.fillStyle='#e8dcc0';g.fillRect(24,64,2,16)},
  overlay:(g,i)=>{g.fillStyle='rgba(60,140,205,.62)';g.fillRect(26,64,38,16);g.fillStyle='rgba(190,235,250,.8)';for(let x=26;x<64;x+=4)g.fillRect(x+Math.floor(fr%4),64,2,1);
   if(t>=.53&&t<.98){const tau=(t-.53)*32/2,ex=47;for(let k=0;k<7;k++){const vx=(k-3)*.8,vy=-3.4+(k%3)*.4;const x=ex+vx*tau,y=64+vy*tau+.4*tau*tau;if(y<64)R(g,x,y,2,2,'#e8f8ff')}
    g.fillStyle='rgba(235,250,255,.85)';const rr=2+tau*2.4;if(rr<20)g.fillRect(Math.round(ex-rr),63,Math.round(rr*2),1)}}}}});
// 8 UMBRELLA -----------------------------------------------
A.push({n:'8  Umbrella in the rain',bg:'rain',f:(t,fr)=>{const p=t*PI2*2;return{legs:walkLegs(p),arms:[{ua:0,fa:0},{ua:26*S(p),fa:26*S(p)+25}],armRel:[[7,-6],null],lean:3,dy:(Math.abs(C(p))>.5?0:-1),face:'n',mouth:'smile',
  scene:(g)=>{city(g,fr*2,'#454e66');ground(g,'#2f3548','#4a5470');g.fillStyle='#6a7490';g.fillRect(0,GY+3,64,1)},
  prop:(g,i)=>{const h=i.h[0];line(g,h[0],h[1]-1,h[0],h[1]-14,1,'#d9d9e6');for(let r=0;r<6;r++){const w=[4,8,12,16,20,22][r];R(g,h[0]-w/2+1,h[1]-19+r,w,1,r<2?'#f06a60':'#e0534a')}R(g,h[0]-11,h[1]-14,2,1,'#c0443c');R(g,h[0]-1,h[1]-1,3,3,K.skin)},
  overlay:(g,i)=>{g.fillStyle='rgba(190,215,240,.75)';for(let k=0;k<26;k++){const x=(k*5+fr*3)%72-4,y=(k*17+fr*7)%76;const h=i.h[0];if(x>h[0]-12&&x<h[0]+14&&y<h[1]-6)continue;g.fillRect(x,y,1,3)}g.fillStyle='rgba(200,225,245,.9)';for(let k=0;k<5;k++){const x=(k*13+fr*5)%60+2;g.fillRect(x,GY+1+Math.floor((fr+k)%2),2,1)}}}}});
// 9 BOOK ---------------------------------------------------
A.push({n:'9  Read a book',bg:'warm',f:(t)=>{const flip=t>.55&&t<.8,fp=(t-.55)/.25;return{legs:[st(4,4),st(-4,-4)],arms:[{ua:0,fa:0},{ua:0,fa:0}],armRel:[[9,6],[7,7]],lean:3+S(t*PI2)*.5,hy:1,look:1,face:'n',mouth:'flat',hx:1,
  scene:(g)=>{city(g,0,'#4a3a66');ground(g,'#3a2a3f','#5a4560')},
  mid:(g,i)=>{const h=i.h[0],b=[h[0]-3,h[1]-6];R(g,b[0]-1,b[1]-1,11,8,'#3f6a8a');R(g,b[0],b[1],4,6,'#f2efe6');R(g,b[0]+5,b[1],4,6,'#f2efe6');R(g,b[0]+4,b[1],1,6,'#b8b0a0');for(let r=0;r<3;r++){R(g,b[0]+1,b[1]+1+r*2,2,1,'#a8a090');R(g,b[0]+6,b[1]+1+r*2,2,1,'#a8a090')}
   if(flip){const w=Math.max(1,Math.round(5*Math.abs(C(fp*PI))));R(g,fp<.5?b[0]+4:b[0]+4-w+1,b[1]-1,w,7,'#fffaf0')}
   }}}});
// 10 HAMMER ------------------------------------------------
A.push({n:'10  Hammer a nail',bg:'dusk',f:(t,fr)=>{const k=(t*2)%1;
 const up=k<.45?sm(k/.45):k<.6?1-sm((k-.45)/.15):0;const raised=[41,30],hitHand=[40.5,52.5];const hnd=[lerp(hitHand[0],raised[0],up),lerp(hitHand[1],raised[1],up)];const dir=lerp(45,150,up);const nails=(t<.5)?3:2;
 return{legs:[st(10,10),st(-12,-12)],arms:[{ua:0,fa:0},{ua:20,fa:50}],armIK:[hnd,null],lean:lerp(16,2,up),face:k>.58&&k<.7?'closed':'n',mouth:'flat',dx:4,
  scene:(g)=>{city(g,0,'#38305a');ground(g,'#3a2a3f','#5a4560');R(g,42,62,21,3,'#a8764a');R(g,42,62,21,1,'#c8946a');R(g,44,65,3,5,'#8a5e3a');R(g,58,65,3,5,'#8a5e3a');R(g,49,62-nails,1,nails,'#c8c8d4');R(g,48,62-nails,3,1,'#e8e8f0')},
  prop:(g,i)=>{const h=i.h[0],d=rad(dir);const e=[h[0]+Math.sin(d)*7,h[1]+Math.cos(d)*7];line(g,h[0],h[1],e[0],e[1],1,'#c8946a');const pxn=Math.cos(d),pyn=-Math.sin(d);for(let q=-2;q<=2;q++)R(g,e[0]+pxn*q-1,e[1]-pyn*q-1,3,2,'#8a90a8');R(g,h[0]-1,h[1]-1,3,3,K.skin)},
  overlay:(g)=>{if(k>.56&&k<.7){const tau=(k-.56)*20;for(let q=0;q<4;q++)px(g,49+(q-1.5)*tau*1.2,60-tau*(1+q%2),'#ffe9a0')}}}}});
