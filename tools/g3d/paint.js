()=>{
const out={};
const mkc=(w,h)=>{const c=document.createElement('canvas');c.width=w;c.height=h;return c};
const AMB='#f2c14e',OUT='#1c1630',CREAM='#fff2c8';
const hx=c=>{const n=parseInt(c.slice(1),16);return[(n>>16)&255,(n>>8)&255,n&255]};
const mix=(a,b,k)=>{const A=hx(a),B=hx(b);return'#'+A.map((v,i)=>Math.round(v+(B[i]-v)*k).toString(16).padStart(2,'0')).join('')};
const rnd=s=>{let x=Math.sin(s*127.1+311.7)*43758.5453;return x-Math.floor(x)};
function pen(g){return(x,y,w,h,c)=>{g.fillStyle=c;g.fillRect(Math.round(x),Math.round(y),Math.round(w),Math.round(h))}}
function text2(g,s,cx,y,col,sc){const w=ptw(s),t=mkc(w+2,8),tg=t.getContext('2d');ptext(tg,s,0,0,col);g.imageSmoothingEnabled=false;g.drawImage(t,Math.round(cx-w*sc/2),y,(w+2)*sc,8*sc)}

function windowLit(R,E,x,y,w,h,lit,seed,curt){
 R(x-3,y-3,w+6,h+6,OUT);R(x-2,y-2,w+4,h+4,'#c9a24a');R(x-2,y-2,w+4,1,'#f2dd9e');
 if(lit){for(let i=0;i<h;i++)R(x,y+i,w,1,mix('#fff2c8','#f0b040',i/h));
  E(x,y,w,h,'#ffffff');
  if(rnd(seed)>.45){const px=x+4+Math.floor(rnd(seed+1)*(w-14));R(px,y+h-16,7,16,'#7a4e30');R(px+1,y+h-21,5,6,'#7a4e30');E(px,y+h-21,7,21,'#553018')}
  else if(rnd(seed)>.2){const px=x+w-12;R(px,y+h-12,6,12,'#a8623e');R(px-2,y+h-20,10,9,'#237a4c');R(px,y+h-23,5,5,'#2f9c63');E(px-2,y+h-23,10,23,'#405030')}
 }else{for(let i=0;i<h;i++)R(x,y+i,w,1,mix('#3a3560','#231d40',i/h));
  for(let i=0;i<5;i++){R(x+3+i,y+h-8-i*3,2,3,'#5a5488');R(x+w-12+i,y+12-i*2,2,2,'#4a4478')}}
 if(curt){const cc=lit?'#b85a6a':'#5a3048',ch=lit?'#d87888':'#6e3c58';R(x,y,5,h,cc);R(x,y,1,h,ch);R(x+3,y,1,h,mix(cc,'#000000',.25));R(x+w-5,y,5,h,cc);R(x+w-5,y,1,h,ch);R(x+w-2,y,1,h,mix(cc,'#000000',.25));
  if(lit){E(x,y,5,h,'#8a4a50');E(x+w-5,y,5,h,'#8a4a50')}}
 R(x+Math.floor(w/2)-1,y,2,h,OUT);R(x,y+Math.floor(h*.42),w,2,OUT);if(lit){E(x+Math.floor(w/2)-1,y,2,h,'#000');E(x,y+Math.floor(h*.42),w,2,'#000')}
 R(x-6,y+h+3,w+12,4,'#d8d0e8');R(x-6,y+h+3,w+12,1,'#ffffff');R(x-5,y+h+7,w+10,2,'#1f1a36');
 R(x-4,y-7,w+8,4,'#d8d0e8');R(x-4,y-7,w+8,1,'#ffffff')}

function facade(o){
 const w=o.w,h=o.h,c=mkc(w,h),e=mkc(w,h),g=c.getContext('2d'),eg=e.getContext('2d');const R=pen(g),E0=pen(eg);E0(0,0,w,h,'#000');
 const E=(x,y,ww,hh,col)=>E0(x,y,ww,hh,col);
 const W=o.wall,WD=mix(W,'#000000',.22),WL=mix(W,'#ffffff',.14);
 R(0,0,w,h,W);
 for(let y=0;y<h;y+=6){R(0,y+5,w,1,WD);const off=(y/6%2)*7;for(let x=off;x<w;x+=14){R(x,y,1,5,WD);const r=rnd(x*3.1+y*7.7+o.seed);if(r>.82)R(x+1,y,13,5,WL);else if(r<.12)R(x+1,y,13,5,mix(W,'#000000',.1));if(r>.95)R(x+3,y+1,4,1,mix(W,'#ffffff',.3))}}
 for(let y=0;y<h;y++){const k=y/h;g.globalAlpha=.16*k;R(0,y,w,1,'#120a2a')}g.globalAlpha=1;
 const gh=o.gh||86,cor=20,fh=Math.floor((h-gh-cor)/o.floors),bay=w/o.cols;
 // pilasters
 for(let i=0;i<=o.cols;i++){const x=Math.round(i*bay)-(i===0?0:i===o.cols?10:5);if(o.pil||i===0||i===o.cols){R(x,cor,10,h-cor,o.trim);R(x,cor,2,h-cor,mix(o.trim,'#ffffff',.3));R(x+8,cor,2,h-cor,mix(o.trim,'#000000',.3));for(let y=cor+20;y<h;y+=24)R(x+2,y,6,1,mix(o.trim,'#000000',.18))}}
 // floors
 for(let f=0;f<o.floors;f++){const y0=cor+f*fh;
  for(let cI=0;cI<o.cols;cI++){const ww=Math.round(bay*.46),wh=Math.round(fh*.58),x=Math.round(cI*bay+bay/2-ww/2),y=y0+Math.round(fh*.2),sd=o.seed+f*17+cI*5;
   const lit=rnd(sd)>(o.dark||.35);windowLit(R,E,x,y,ww,wh,lit,sd,true);
   const r=rnd(sd+9);if(r>.7){R(x-4,y+wh+7,ww+8,6,'#6b4329');R(x-4,y+wh+7,ww+8,1,'#8a5e3c');for(let i=0;i<ww+4;i+=5){R(x-3+i,y+wh+2,4,5,'#237a4c');R(x-2+i,y+wh+1,2,2,i%10?'#e88a98':'#f4d27a')}}
   else if(r<.14){R(x+4,y+wh+6,18,11,OUT);R(x+5,y+wh+7,16,9,'#9a94b0');for(let i=0;i<4;i++)R(x+6,y+wh+8+i*2,14,1,'#6a6488')}}
  R(0,y0+fh-4,w,4,o.trim);R(0,y0+fh-4,w,1,mix(o.trim,'#ffffff',.35));R(0,y0+fh,w,2,mix(W,'#000000',.4))}
 // cornice
 R(0,0,w,cor,mix(o.trim,'#000000',.1));R(0,0,w,3,mix(o.trim,'#ffffff',.4));R(0,3,w,3,o.trim);for(let x=2;x<w;x+=8){R(x,8,5,6,mix(o.trim,'#ffffff',.2));R(x+4,8,1,6,mix(o.trim,'#000000',.3))}R(0,cor-4,w,2,mix(o.trim,'#000000',.35));R(0,cor-2,w,3,mix(W,'#000000',.45));
 // ground floor
 const gy=h-gh;R(0,gy,w,gh,mix(W,'#1f1a36',.45));for(let y=gy;y<h;y+=12){R(0,y+11,w,1,mix(W,'#000000',.6));const off=(y/12%2)*14;for(let x=off;x<w;x+=28)R(x,y,1,11,mix(W,'#000000',.6))}
 R(0,gy-2,w,8,o.trim);R(0,gy-2,w,2,mix(o.trim,'#ffffff',.4));R(0,gy+6,w,2,mix(o.trim,'#000000',.4));
 R(0,h-9,w,9,'#2b2444');R(0,h-9,w,1,'#55497e');
 if(o.kind==='hotel'){
  const dx=Math.round(w/2-36),dy=h-78;
  // big lobby windows
  for(const bx of [Math.round(w*.11),Math.round(w*.89-104)]){const by=h-70,bw=104,bh=54;R(bx-4,by-4,bw+8,bh+8,OUT);R(bx-3,by-3,bw+6,bh+6,'#c9a24a');R(bx-3,by-3,bw+6,1,'#f2dd9e');
   for(let i=0;i<bh;i++)R(bx,by+i,bw,1,mix('#fff0c0','#e8a040',i/bh));E(bx,by,bw,bh,'#fff');
   R(bx+10,by+bh-22,22,22,'#7a3346');R(bx+12,by+bh-30,18,10,'#8a3f52');R(bx+70,by+bh-30,3,30,'#8a6c2c');R(bx+64,by+bh-40,15,11,'#fff8dc');R(bx+44,by+bh-14,10,14,'#a8623e');R(bx+41,by+bh-26,16,13,'#237a4c');R(bx+45,by+bh-31,8,6,'#2f9c63');
   E(bx+10,by+bh-30,22,30,'#6a3030');E(bx+41,by+bh-31,16,31,'#405030');
   R(bx+34,by,2,bh,OUT);R(bx+69,by,2,bh,OUT);E(bx+34,by,2,bh,'#000');E(bx+69,by,2,bh,'#000');
   R(bx-7,by+bh+4,bw+14,5,'#d8d0e8');R(bx-7,by+bh+4,bw+14,1,'#fff')}
  // door
  R(dx-5,dy-5,82,83,OUT);R(dx-4,dy-4,80,82,AMB);R(dx-4,dy-4,80,2,'#f2dd9e');R(dx-4,dy-4,2,82,'#f2dd9e');R(dx+74,dy-4,2,82,'#8a6c2c');
  for(const ox of [0,37]){for(let i=0;i<64;i++)R(dx+ox,dy+12+i,35,1,mix('#d6ecf8','#6f9cc0',Math.min(1,i/26)));E(dx+ox,dy+12,35,64,'#4a5a78');
   g.globalAlpha=.4;R(dx+ox+5,dy+18,3,50,'#fff');R(dx+ox+10,dy+18,1,50,'#fff');g.globalAlpha=1;R(dx+ox+(ox?3:29),dy+40,3,12,AMB);R(dx+ox+(ox?3:29),dy+40,1,12,'#f2dd9e')}
  R(dx+35,dy+12,2,64,'#8a6c2c');R(dx,dy,72,10,'#221c3c');text2(g,'LOBBY',dx+36,dy+2,AMB,1);E(dx,dy,72,10,'#604a10');
  // sconces
  for(const sx of [dx-22,dx+86]){R(sx,dy+16,8,4,'#8a6c2c');R(sx+1,dy+4,6,12,'#fff8dc');R(sx,dy+3,8,2,AMB);E(sx,dy+3,8,14,'#fff')}
 }else{
  const dx=Math.round(w*.12),dy=h-68;R(dx-4,dy-4,44,72,OUT);R(dx-3,dy-3,42,71,o.trim);R(dx,dy,36,68,'#3a2a22');for(let i=0;i<40;i++)R(dx+4,dy+4+i,28,1,mix('#fff0c0','#d89038',i/40));E(dx+4,dy+4,28,40,'#fff');R(dx+17,dy+4,2,40,'#3a2a22');R(dx+30,dy+50,3,3,AMB);
  const bx=dx+56,bw=w-bx-Math.round(w*.1),by=h-66,bh=48;R(bx-4,by-4,bw+8,bh+8,OUT);R(bx-3,by-3,bw+6,bh+6,o.trim);for(let i=0;i<bh;i++)R(bx,by+i,bw,1,mix('#fff0c0','#e8a040',i/bh));E(bx,by,bw,bh,'#fff');
  for(let i=0;i<Math.floor(bw/22);i++){const px=bx+6+i*22,ph=10+Math.floor(rnd(o.seed+i)*16),col=['#d9695f','#5a9cba','#2f9c63','#a88be0','#f4d27a'][Math.floor(rnd(o.seed+i*3)*5)];R(px,by+bh-ph,12,ph,col);R(px,by+bh-ph,12,2,mix(col,'#ffffff',.4));E(px,by+bh-ph,12,ph,mix(col,'#000000',.4))}
  R(bx-6,by+bh+4,bw+12,5,'#d8d0e8');R(bx+Math.floor(bw/2),by,2,bh,OUT);E(bx+Math.floor(bw/2),by,2,bh,'#000');
 }
 // sign
 if(o.sign){const sc=o.signScale||2,sw=ptw(o.sign)*sc+20,sx=Math.round(w/2-sw/2),sy=o.kind==='hotel'?gy+12-30:gy+10-26;const sh=8*sc+6;
  const yy=gy+10;R(sx-2,yy-2,sw+4,sh+4,'#141026');R(sx,yy,sw,sh,'#221c3c');R(sx,yy,sw,1,AMB);R(sx,yy+sh-1,sw,1,AMB);R(sx,yy,1,sh,AMB);R(sx+sw-1,yy,1,sh,AMB);
  text2(g,o.sign,w/2,yy+4,o.signCol||AMB,sc);E(sx,yy,sw,sh,'#3a2c08');text2(eg,o.sign,w/2,yy+4,'#fff0b0',sc)}
 return[c,e]}

function side(o){const p=Object.assign({},o,{kind:'none',sign:null,cols:o.scols||3,w:o.d});const w=p.w,h=p.h;const [c,e]=facade(Object.assign(p,{kind:'blank'}));
 // blank ground floor: repaint ground without door (facade's else-branch drew a shop; cover it)
 const g=c.getContext('2d'),R=pen(g),eg=e.getContext('2d'),E=pen(eg);const gh=o.gh||86,gy=h-gh,W=o.wall;
 R(0,gy+8,w,gh-17,mix(W,'#1f1a36',.45));E(0,gy+8,w,gh-8,'#000');for(let y=gy+8;y<h-9;y+=12){R(0,y+11,w,1,mix(W,'#000000',.6));const off=(y/12%2)*14;for(let x=off;x<w;x+=28)R(x,y,1,11,mix(W,'#000000',.6))}
 for(let i=0;i<p.cols;i++){const bw=40,bx=Math.round((i+.5)*w/p.cols-bw/2),by=gy+20;windowLit(R,E,bx,by,bw,36,rnd(o.seed+i*7+50)>.5,o.seed+i,false)}
 g.globalAlpha=.22;R(0,0,w,h,'#120a2a');g.globalAlpha=1;return[c,e]}

const B={
 hotel:{w:432,h:372,d:300,floors:3,cols:6,scols:4,wall:'#6a5f98',trim:'#d8d0e8',pil:true,kind:'hotel',sign:null,signScale:2,seed:3,dark:.3,gh:96},
 cafe:{w:260,h:210,d:240,floors:1,cols:3,scols:3,wall:'#a8584a',trim:'#f0d0a0',pil:false,kind:'shop',sign:'CORNER CAFE',signScale:2,seed:11,dark:.3,gh:112},
 books:{w:230,h:290,d:260,floors:2,cols:3,scols:3,wall:'#3f7c6c',trim:'#e8d9b0',pil:false,kind:'shop',sign:'BOOKS',signScale:2,seed:23,dark:.45,gh:112},
 bank:{w:300,h:450,d:280,floors:4,cols:4,scols:4,wall:'#4a5a88',trim:'#c8d0e8',pil:true,kind:'shop',sign:'ATLAS BANK',signScale:2,seed:31,dark:.5,gh:112},
 apts:{w:280,h:330,d:260,floors:3,cols:4,scols:3,wall:'#b88a5a',trim:'#f3ecd8',pil:false,kind:'shop',sign:'MARKET',signScale:2,seed:47,dark:.4,gh:112}};
for(const k in B){const [c,e]=facade(B[k]);out[k+'_f']=c.toDataURL();out[k+'_fe']=e.toDataURL();const [s,se]=side(B[k]);out[k+'_s']=s.toDataURL();out[k+'_se']=se.toDataURL();
 const r=mkc(128,128),R=pen(r.getContext('2d'));R(0,0,128,128,'#3a3454');for(let i=0;i<900;i++){const x=rnd(i+B[k].seed)*128,y=rnd(i*1.7+3)*128;R(x,y,1,1,rnd(i*2.3)>.5?'#4a4468':'#2e2846')}
 R(0,0,128,6,'#55497e');R(0,122,128,6,'#55497e');R(0,0,6,128,'#55497e');R(122,0,6,128,'#55497e');R(6,6,116,2,'#1f1a36');R(6,6,2,116,'#1f1a36');out[k+'_r']=r.toDataURL()}
out.meta=B;

// sidewalk pavers (48x48 = 2x2 pavers)
{const c=mkc(48,48),R=pen(c.getContext('2d'));for(let j=0;j<2;j++)for(let i=0;i<2;i++){const x=i*24,y=j*24,cc=(i+j)%2?'#8f88a8':'#9a93b2';R(x,y,24,24,cc);R(x,y,24,1,mix(cc,'#ffffff',.25));R(x,y,1,24,mix(cc,'#ffffff',.12));R(x,y+23,24,1,mix(cc,'#000000',.25));R(x+23,y,1,24,mix(cc,'#000000',.18));
  R(x+5+i*6,y+7,5,1,mix(cc,'#000000',.12));R(x+9+j*4,y+8,4,1,mix(cc,'#000000',.12));R(x+14,y+16-j*3,1,4,mix(cc,'#000000',.1));R(x+8,y+15,2,1,mix(cc,'#ffffff',.2))}out.pave=c.toDataURL()}
// asphalt 96x96
{const c=mkc(96,96),R=pen(c.getContext('2d'));R(0,0,96,96,'#2c2844');for(let i=0;i<700;i++){const x=rnd(i)*96,y=rnd(i*1.9+7)*96,r=rnd(i*3.3);R(x,y,r>.9?2:1,1,r>.6?'#3a3658':r>.3?'#242038':'#34304e')}
 for(let i=0;i<14;i++)R(20+i,60+Math.round(Math.sin(i*.7)*3),1,1,'#1a1630');for(let i=0;i<9;i++)R(66+Math.round(Math.sin(i)*2),14+i,1,1,'#1a1630');out.asph=c.toDataURL()}
// grass 48
{const c=mkc(48,48),R=pen(c.getContext('2d'));R(0,0,48,48,'#2f6a4a');for(let i=0;i<260;i++){const x=rnd(i+5)*48,y=rnd(i*2.1+1)*48,r=rnd(i*4.4);R(x,y,1,r>.5?2:1,r>.7?'#49a068':r>.35?'#237a4c':'#3c8458')}out.grass=c.toDataURL()}
// tree foliage cutout 72x84
{const c=mkc(72,84),g=c.getContext('2d'),R=pen(g);const L=(x,y,w,h,col)=>{R(x-1,y-1,w+2,h+2,OUT);R(x,y,w,h,col)};
 R(32,56,8,28,OUT);R(33,56,6,28,'#5a3a24');R(34,56,2,28,'#7a5434');R(28,62,6,3,'#5a3a24');R(38,58,7,3,'#5a3a24');
 L(10,26,52,30,'#1c6240');L(4,34,22,18,'#1c6240');L(46,32,22,20,'#1c6240');L(16,10,40,26,'#237a4c');L(8,20,24,20,'#237a4c');L(40,18,24,22,'#237a4c');L(22,2,28,18,'#2f9c63');L(14,12,18,14,'#2f9c63');L(42,10,16,14,'#2f9c63');
 R(26,4,12,6,'#49d08a');R(16,14,8,5,'#49d08a');R(44,12,7,5,'#49d08a');R(30,18,10,4,'#49d08a');R(10,24,6,4,'#2f9c63');R(48,24,8,5,'#2f9c63');R(22,36,10,4,'#237a4c');R(40,40,12,4,'#237a4c');
 for(let i=0;i<26;i++){const x=8+rnd(i+70)*54,y=6+rnd(i*2+71)*44;const d=g.getImageData(x,y,1,1).data;if(d[3]>0&&d[1]>80)R(x,y,2,1,'#7fe0a8')}out.tree=c.toDataURL()}
// cars: side 96x40, top 96x44, end 44x40
function car(col,name){const D=mix(col,'#000000',.3),L=mix(col,'#ffffff',.35);
 {const c=mkc(96,40),R=pen(c.getContext('2d'));R(2,16,92,16,OUT);R(3,17,90,14,col);R(3,17,90,2,L);R(3,27,90,4,D);R(20,2,50,16,OUT);R(21,3,48,15,col);R(21,3,48,2,L);R(25,6,18,11,'#2a3148');R(46,6,19,11,'#2a3148');R(25,6,18,2,'#8cc8e0');R(46,6,19,2,'#8cc8e0');R(28,9,4,6,'#5a9cba');R(50,9,4,6,'#5a9cba');
  R(44,18,1,12,D);R(48,22,5,1,OUT);R(89,19,5,4,'#fff2c8');R(2,19,3,4,'#e2564f');R(2,30,92,3,'#55506a');
  for(const wx of [16,68]){R(wx-1,24,16,16,OUT);R(wx,25,14,14,'#17132a');R(wx+3,28,8,8,'#9a94b0');R(wx+5,30,4,4,'#55506a')}out[name+'_s']=c.toDataURL()}
 {const c=mkc(96,44),R=pen(c.getContext('2d'));R(0,0,96,44,OUT);R(1,1,94,42,col);R(1,1,94,2,L);R(1,40,94,3,D);R(22,5,46,34,D);R(24,7,42,30,col);R(26,9,38,26,L);R(28,11,34,22,col);R(68,6,10,32,'#2a3148');R(69,7,3,30,'#8cc8e0');R(16,7,7,30,'#2a3148');R(80,4,1,36,D);R(92,4,3,8,'#fff2c8');R(92,32,3,8,'#fff2c8');R(1,4,2,8,'#e2564f');R(1,32,2,8,'#e2564f');out[name+'_t']=c.toDataURL()}
 {const c=mkc(44,40),R=pen(c.getContext('2d'));R(0,16,44,16,OUT);R(1,17,42,14,col);R(1,17,42,2,L);R(5,2,34,16,OUT);R(6,3,32,15,col);R(8,5,28,11,'#2a3148');R(8,5,28,2,'#8cc8e0');R(3,20,8,5,'#fff2c8');R(33,20,8,5,'#fff2c8');R(15,21,14,6,'#17132a');R(16,22,12,1,'#55506a');R(16,24,12,1,'#55506a');R(0,30,44,3,'#55506a');R(2,32,8,8,'#17132a');R(34,32,8,8,'#17132a');out[name+'_f']=c.toDataURL();
  const b=mkc(44,40),Rb=pen(b.getContext('2d'));Rb(0,16,44,16,OUT);Rb(1,17,42,14,col);Rb(1,17,42,2,L);Rb(5,2,34,16,OUT);Rb(6,3,32,15,col);Rb(8,5,28,11,'#2a3148');Rb(8,5,28,2,'#5a6a90');Rb(3,20,8,5,'#e2564f');Rb(33,20,8,5,'#e2564f');Rb(16,22,12,5,'#f3ecd8');Rb(0,30,44,3,'#55506a');Rb(2,32,8,8,'#17132a');Rb(34,32,8,8,'#17132a');out[name+'_b']=b.toDataURL()}}
car('#d9695f','car1');car('#5a9cba','car2');car('#f4d27a','car3');
// wallpaper for lobby side walls and upper band 48x112
{const c=mkc(48,112),R=pen(c.getContext('2d'));R(0,0,48,112,'#4a3f72');R(0,0,48,8,'#1f1a36');R(0,8,48,1,'#7166a0');R(0,9,48,2,'#3c3262');for(let x=6;x<48;x+=12){R(x,12,1,72,'#453a6c');if((x/12|0)%2)for(let y=14;y<84;y+=8){R(x+5,y,3,1,'#55497e');R(x+6,y-1,1,3,'#55497e')}}
 R(0,84,48,3,'#7166a0');R(0,84,48,1,'#9086bc');R(0,87,48,1,'#2c2450');R(0,88,48,22,'#3a305e');for(let x=4;x<48;x+=24){R(x,91,17,16,'#2f2752');R(x,91,17,1,'#4a3f72');R(x,91,1,16,'#4a3f72');R(x+2,93,13,12,'#352c58');R(x+2,104,13,1,'#28204a')}R(0,110,48,2,'#1c1630');out.wallp=c.toDataURL()}
// upper band (40 tall) to extend the back wall
{const c=mkc(48,40),R=pen(c.getContext('2d'));R(0,0,48,40,'#4a3f72');R(0,0,48,8,'#1f1a36');R(0,8,48,1,'#7166a0');R(0,9,48,2,'#3c3262');for(let x=6;x<48;x+=12){R(x,12,1,28,'#453a6c');if((x/12|0)%2)for(let y=14;y<40;y+=8){R(x+5,y,3,1,'#55497e');R(x+6,y-1,1,3,'#55497e')}}out.wallup=c.toDataURL()}
// awning stripes 32x16
{const c=mkc(32,16),R=pen(c.getContext('2d'));for(let i=0;i<4;i++){R(i*8,0,4,16,'#b85a6a');R(i*8+4,0,4,16,'#f3ecd8');R(i*8,0,1,16,'#d87888')}R(0,13,32,3,'#8f4252');out.awn=c.toDataURL()}
// crosswalk + lane
{const c=mkc(16,64),R=pen(c.getContext('2d'));c.getContext('2d').clearRect(0,0,16,64);for(let i=0;i<4;i++)R(0,i*16+3,16,10,'#d8d0e8');out.cross=c.toDataURL()}
{const sw=ptw('THE MERIDIAN')*3+24,c=mkc(sw,34),e=mkc(sw,34),g=c.getContext('2d'),R=pen(g);R(0,0,sw,34,'#141026');R(2,2,sw-4,30,'#221c3c');R(2,2,sw-4,1,AMB);R(2,31,sw-4,1,AMB);R(2,2,1,30,AMB);R(sw-3,2,1,30,AMB);for(let x=6;x<sw-6;x+=6){R(x,4,2,2,'#fff2c8');R(x,28,2,2,'#fff2c8')}text2(g,'THE MERIDIAN',sw/2,9,AMB,3);const eg=e.getContext('2d');pen(eg)(0,0,sw,34,'#000');for(let x=6;x<sw-6;x+=6){pen(eg)(x,4,2,2,'#fff');pen(eg)(x,28,2,2,'#fff')}text2(eg,'THE MERIDIAN',sw/2,9,'#ffe9a0',3);out.marq=c.toDataURL();out.marq_e=e.toDataURL()}
{const c=mkc(64,16),R=pen(c.getContext('2d'));R(0,0,64,16,'#7a3346');R(0,0,4,16,'#c9a24a');R(60,0,4,16,'#c9a24a');R(4,0,1,16,'#5a2434');R(59,0,1,16,'#5a2434');for(let i=0;i<2;i++){R(30,i*8+2,4,4,'#8a3f52');R(31,i*8+3,2,2,'#c9a24a')}out.carpet=c.toDataURL()}
return out}
