// 11 SKATEBOARD --------------------------------------------
A.push({n:'11  Skateboard',bg:'dusk',f:(t,fr)=>{const k=frac(t*2),deck=GY-5;
 const hipX=31;let hipY,bx,by,lean,arms;
 const push=k<.42,ret=k>=.42&&k<.58;
 hipY=push?lerp(55,56,sm(k/.2)):ret?lerp(56,51,sm((k-.42)/.16)):lerp(51,49,sm((k-.58)/.2))+ (k>.9?lerp(0,5,sm((k-.9)/.1)):0);
 const front=[3,deck-1-hipY];
 let back;
 if(push){back=[lerp(-3,-12,k/.42),GY-1-hipY]}
 else if(ret){const q=sm((k-.42)/.16);back=[lerp(-12,-5,q),lerp(GY-1-hipY,deck-1-hipY,q)-5*S(PI*q)]}
 else back=[-5,deck-1-hipY];
 lean=push?18:ret?10:6;
 arms=push?[{ua:50,fa:70},{ua:-45,fa:-20}]:[{ua:70,fa:90},{ua:-30,fa:-10}];
 return{hip:[hipX,hipY],legRel:[back,front],arms,lean,face:'n',mouth:'smile',nobag:0,
  scene:(g)=>{city(g,fr*(push?3:5),'#38305a');ground(g,'#3a2a3f','#5a4560')},
  propBack:(g)=>{R(g,hipX-9,deck,18,2,'#e0534a');R(g,hipX-9,deck,18,1,'#f2796f');R(g,hipX-10,deck-1,2,1,'#e0534a');R(g,hipX+8,deck-1,2,1,'#e0534a');R(g,hipX-6,deck+2,3,3,'#e8e0c8');R(g,hipX+4,deck+2,3,3,'#e8e0c8')}}}});
// 12 JUMP ROPE ---------------------------------------------
const ROPE=(g,hand,L,ang,w,half,col)=>{const ux=Math.sin(ang),uy=-Math.cos(ang),vx=-uy,vy=ux;g.fillStyle=col;let last=null;for(let s=0;s<=1.0001;s+=.015){const a=Math.PI*s*(half>0?1:-1);const e=(1-Math.cos(a*2))/2*L;const x=hand[0]+ux*(L/2)*(1-Math.cos(a))+vx*w*Math.sin(a),y=hand[1]+uy*(L/2)*(1-Math.cos(a))+vy*w*Math.sin(a);const k=Math.round(x)+','+Math.round(y);if(k!=last){g.fillRect(Math.round(x),Math.round(y),1,1);last=k}}};
A.push({n:'12  Jump rope',bg:'park',f:(t,fr)=>{const th=t*PI2*3,air=Math.round(3*Math.pow(mx0(0,-C(th)),2));const kn=air*5;const front=S(th)>0;
 const apexOf=(i)=>{const hh=i.h[0],hy=hh[1]-0;const up=C(th)>=0?27:20;return[hh[0]+10*S(th),hy-up*C(th)]};
 return{legs:[st(2+kn*.4,2-kn*.9),st(-2+kn*.3,-2-kn*.8)],arms:[{ua:0,fa:0},{ua:0,fa:0}],armRel:[[3+2*Math.cos(th),9+2*S(th)],[2+2*Math.cos(th),9+2*S(th)]],lean:2,air,face:air>1?'happy':'n',mouth:'smile',nobag:0,
  scene:(g)=>{ground(g,'#7aa86a','#8fc07c');for(let k=0;k<8;k++)px(g,4+k*8,GY+3+(k%3),'#6a9a5a');for(let k=0;k<4;k++){R(g,3+k*17,GY-6,2,6,'#8a5e3a');R(g,2+k*17,GY-9,4,4,'#4e9a5a')}},
  propBack:(g,i)=>{const L=C(th)>=0?32:19;ROPE(g,[i.h[1][0]-1,i.h[1][1]],L,th,3,-1,'#c8bf9c')},
  prop:(g,i)=>{const L=C(th)>=0?32:19;ROPE(g,i.h[0],L,th,3,1,'#fff7d8')}}}});
// 13 KICK A BALL --------------------------------------------
A.push({n:'13  Kick a ball',bg:'day',f:(t,fr)=>{
 let th0=5,sh0=5,lean=0,arms=[{ua:20,fa:30},{ua:-20,fa:-10}];
 if(t<.2){}else if(t<.42){const k=sm((t-.2)/.22);th0=lerp(5,-48,k);sh0=lerp(5,-90,k);lean=lerp(0,-6,k);arms=[{ua:lerp(20,70,k),fa:70},{ua:lerp(-20,-50,k),fa:-30}]}
 else if(t<.5){const k=sm((t-.42)/.08);th0=lerp(-48,50,k);sh0=lerp(-90,18,k);lean=lerp(-6,6,k);arms=[{ua:lerp(70,-40,k),fa:-20},{ua:lerp(-50,60,k),fa:70}]}
 else if(t<.72){const k=sm((t-.5)/.22);th0=lerp(50,82,k);sh0=lerp(18,40,k);lean=lerp(6,10,k);arms=[{ua:-40,fa:-20},{ua:60,fa:70}]}
 else{const k=sm((t-.72)/.26);th0=lerp(82,5,k);sh0=lerp(40,5,k);lean=lerp(10,0,k);arms=[{ua:lerp(-40,20,k),fa:30},{ua:lerp(60,-20,k),fa:-10}]}
 // ball
 let bx=42,by=GY-3;
 if(t>=.5&&t<.8){let x=42,y=GY-3,vx=2.9,vy=-3.4;const n=Math.round((t-.5)*32);for(let i=0;i<n;i++){x+=vx;y+=vy;vy+=.42;if(y>GY-3){y=GY-3;vy*=-.55}vx*=.985}bx=x;by=y}
 else if(t>=.8){bx=lerp(70,42,sm((t-.8)/.2));by=GY-3}
 return{legs:[st(th0,sh0),st(-5,-5)],arms,lean,face:t>.42&&t<.6?'o':'n',mouth:t>.42&&t<.6?'small':'smile',dx:-4,
  scene:(g)=>{city(g,0,'#a8c8de');ground(g,'#7aa86a','#8fc07c');for(let k=0;k<8;k++)px(g,4+k*8,GY+3+(k%3),'#6a9a5a');R(g,0,GY-5,3,5,'#d9d2c0');R(g,0,GY-12,2,8,'#d9d2c0')},
  prop:(g)=>{const f=Math.floor(fr%4);R(g,bx,by,4,4,'#f4f4fb');R(g,bx+(f<2?0:2),by+(f%2?0:2),2,2,'#2a2a3c');px(g,bx+3,by,'#c0c0d0');if(t>=.5&&t<.62)for(let q=1;q<3;q++)px(g,bx-q*4,by+2,'rgba(255,255,255,.5)')}}}});
// 14 SIT + PHONE --------------------------------------------
A.push({n:'14  Sit and scroll',bg:'warm',f:(t,fr)=>{const p=t*PI2*2,laugh=t>.62&&t<.8,seat=GY-8;
 const sway=S(p)*1.5,sc=S(t*PI2*4),th2=Math.round(fr);
 const PH=(i)=>[i.h[1][0],i.h[1][1]];
 return{hip:[27,seat-2],legIK:[[37+sway*.3,GY-1],[35-sway*.3,GY-1]],arms:[{ua:0,fa:0},{ua:0,fa:0}],armRel:[[11,-6.5+sc*1.5],[11,-8]],lean:11,hx:1,hy:2,look:true,face:'n',mouth:'flat',nobag:1,
  scene:(g)=>{city(g,0,'#4a3a66');ground(g,'#3a2a3f','#5a4560');R(g,14,seat+1,27,2,'#a8764a');R(g,14,seat+1,27,1,'#c8946a');R(g,17,seat+3,2,GY-seat-3,'#6a4a30');R(g,36,seat+3,2,GY-seat-3,'#6a4a30');R(g,14,seat-14,2,16,'#a8764a');R(g,14,seat-14,2,1,'#c8946a')},
  propBack:(g,i)=>{const h=PH(i),x=Math.round(h[0])-2,y=Math.round(h[1])-5;
   R(g,x,y,5,9,'#2a2a3c');R(g,x,y,5,1,'#4a4a64');
   R(g,x,y+1,2,7,'#c8ecff');
   for(let k=0;k<4;k++){const yy=((k*2-(th2%8))+8)%8;R(g,x,y+1+yy,2,1,k%2?'#6fb4e8':'#ffffff')}},
  overlay:(g,i)=>{const h=PH(i),x=Math.round(h[0])-2,y=Math.round(h[1])-5;g.save();g.globalAlpha=.10;R(g,x-4,y-3,11,15,'#8fd3ff');g.globalAlpha=.12;R(g,x-2,y-1,7,11,'#c8ecff');g.restore();R(g,x,y+1,2,7,'#c8ecff');for(let k=0;k<4;k++){const yy=((k*2-(th2%8))+8)%8;R(g,x,y+1+yy,2,1,k%2?'#6fb4e8':'#ffffff')}}}}});
// 15 CARRY A BOX -----------------------------------------------
A.push({n:'15  Carry a box',bg:'dusk',f:(t,fr)=>{const p=t*PI2*2,bob=(Math.abs(C(p))>.5?0:-1);
 return{legs:walkLegs(p,22,38),arms:[{ua:0,fa:0},{ua:0,fa:0}],armRel:[[9,9],[7,10]],lean:-4,dy:bob,face:'n',mouth:'smile',
  scene:(g)=>{city(g,fr*2,'#38305a');ground(g,'#3a2a3f','#5a4560')},
  mid:(g,i)=>{const b=[i.nx+5,i.ny+1+bob*0];R(g,b[0],b[1]+0,13,11,'#b8864f');R(g,b[0],b[1]+0,13,2,'#d4a26a');R(g,b[0]+5,b[1],3,11,'#e8d8a8');R(g,b[0]+1,b[1]+7,4,2,'#f2efe6');R(g,b[0]+9,b[1]+2,3,2,'#8a5e3a');R(g,b[0],b[1]+9,13,2,'#9a6e3d')}}}});
// 16 SHOPPING CART ---------------------------------------------
A.push({n:'16  Push a cart',bg:'wall',f:(t,fr)=>{const p=t*PI2*2,bob=(Math.abs(C(p))>.5?0:-1);const wa=fr*.9;
 return{legs:walkLegs(p,22,36),arms:[{ua:0,fa:0},{ua:0,fa:0}],armRel:[[9,5],[8,6]],lean:9,dy:bob,face:'n',mouth:'smile',dx:-10,
  scene:(g)=>{city(g,fr*2,'#3e3a54');ground(g,'#3a2a3f','#5a4560')},
  mid:(g,i)=>{const hx=i.nx+10,hy=i.ny+6;line(g,hx,hy,hx+2,hy,2,'#c8c8d4');line(g,hx+1,hy,hx+3,hy+8,1,'#c8c8d4');
   R(g,hx+2,hy+2,16,9,'#8a90a8');R(g,hx+2,hy+2,16,1,'#b4bad0');for(let q=0;q<4;q++)R(g,hx+4+q*4,hy+3,1,7,'#5a607a');R(g,hx+2,hy+8,16,1,'#5a607a');
   R(g,hx+4,hy-1,4,3,'#e0534a');R(g,hx+9,hy-2,4,4,'#e8d8a8');R(g,hx+13,hy,3,3,'#5bd16a');
   line(g,hx+4,hy+11,hx+4,GY-3,1,'#8a90a8');line(g,hx+16,hy+11,hx+16,GY-3,1,'#8a90a8');
   [hx+3,hx+16].forEach(x=>{ring(g,x,GY-3,2.5,'#2a2a3c');px(g,x+Math.cos(wa)*1.5,GY-3+Math.sin(wa)*1.5,'#b8b8cc')})}}}});
// 17 LADDER ------------------------------------------------------
A.push({n:'17  Climb a ladder',bg:'wall',f:(t,fr)=>{const d=8;
 const Y=(s,base)=>{const tau=frac(t-s);return tau<.25?lerp(base+d,base+.25*d,sm(tau/.25)):base+d*tau};
 const X=(s,base)=>{const tau=frac(t-s);return tau<.25?S(PI*tau/.25)*2:0};
 const handY=(s)=>Y(s,-14),footY=(s)=>Y(s,6);
 return{hip:[28,44],legRel:[[6+X(.25,0),footY(.25)+4],[5+X(.75,0),footY(.75)+4]],arms:[{ua:0,fa:0},{ua:0,fa:0}],armRel:[[8+X(0,0),handY(0)+0],[8+X(.5,0),handY(.5)]],lean:8,hy:-1,look:1,face:'n',mouth:'smile',nobag:0,
  scene:(g)=>{R(g,40,0,24,80,'#6a4a52');for(let r=0;r<10;r++){const y=((r*10+Math.round(8*t*1.25))%80);R(g,40,y,24,1,'#5a3e46')}R(g,46,18,10,13,'#2d3358');R(g,47,19,8,11,'#3d4a80');
   R(g,35,0,2,80,'#7a7a98');for(let k=-1;k<11;k++){const y=k*d+(d*t);R(g,35,Math.round(y),6,1,'#9a9ab8')}ground(g,'#3a2a3f','#5a4560')},
  mid:(g)=>{R(g,38,0,2,GY+1,'#b0b0c8');R(g,38,0,1,GY+1,'#e0e0f0')}}}});
// 18 WHITEBOARD ------------------------------------------------------
A.push({n:'18  Sketch on a board',bg:'wall',f:(t,fr)=>{const pts=[[43,52],[52,52],[52,46],[43,52]],segs=[];let tot=0;for(let i=0;i<3;i++){const l=Math.hypot(pts[i+1][0]-pts[i][0],pts[i+1][1]-pts[i][1]);segs.push(l);tot+=l}
 const d0=.1,d1=.62;const prog=cl((t-d0)/(d1-d0));let L=prog*tot;let pen=[pts[0][0],pts[0][1]];{let r=L;for(let i=0;i<3;i++){if(r<=segs[i]){pen=[lerp(pts[i][0],pts[i+1][0],r/segs[i]),lerp(pts[i][1],pts[i+1][1],r/segs[i])];break}r-=segs[i];pen=[pts[i+1][0],pts[i+1][1]]}}
 const rest=[4,9];const reach=t<d0?sm(t/d0):t<d1?1:1-sm((t-d1)/.1);
 const wipe=t>.9?(t-.9)/.1:0;
 return{hip:[36,52],legs:[st(5,5),st(-5,-5)],arms:[{ua:0,fa:0},{ua:6,fa:12}],armIK:[[lerp(36+rest[0]+3,pen[0],reach),lerp(45+rest[1]-2,pen[1],reach)],null],lean:t>d0&&t<d1?10:4,face:'n',mouth:'smile',dx:0,nobag:0,
  scene:(g)=>{city(g,0,'#3e3a54');ground(g,'#3a2a3f','#5a4560');R(g,41,30,19,30,'#e8e4dc');R(g,41,30,19,1,'#b8b4aa');R(g,41,59,19,2,'#8a8680');
   g.fillStyle='#3d7fc4';let r=L;for(let i=0;i<3;i++){const n=Math.min(segs[i],r);if(n<=0)break;for(let s=0;s<=n;s+=.5){const x=lerp(pts[i][0],pts[i+1][0],s/segs[i]),y=lerp(pts[i][1],pts[i+1][1],s/segs[i]);if(!(wipe>0&&x<41+wipe*19))g.fillRect(Math.round(x),Math.round(y),1,1)}r-=segs[i]}
   if(prog>=1&&wipe==0){R(g,44,36,6,1,'#3d7fc4');R(g,44,39,10,1,'#3d7fc4');R(g,44,41,4,1,'#c8d0e0')}},
  prop:(g,i)=>{const h=i.h[0];R(g,h[0]-1,h[1]-1,3,3,K.skin);R(g,h[0]+1,h[1]-1,3,1,'#3d7fc4')}}}});
// 19 TAKE A PHOTO -----------------------------------------------------
A.push({n:'19  Take a photo',bg:'dusk',f:(t,fr)=>{const up=t<.22?sm(t/.22):t<.82?1:1-sm((t-.82)/.16);const fl=t>.5&&t<.56;
 const tgt=[lerp(8,12,up),lerp(8,-5,up)];
 return{legs:[st(6,6),st(-6,-6)],arms:[{ua:0,fa:0},{ua:0,fa:0}],armRel:[tgt,[tgt[0]-1,tgt[1]+1]],lean:lerp(2,-2,up),face:t>.58&&t<.8?'happy':'n',mouth:'smile',
  scene:(g)=>{city(g,0,'#38305a');ground(g,'#3a2a3f','#5a4560');R(g,50,30,10,39,'#4a3f70');for(let r=0;r<5;r++){R(g,52,33+r*7,2,3,'#f0c987');R(g,56,33+r*7,2,3,'#f0c987')}
   if(up>.8){[[47,28],[47,56],[62,28],[62,56]].forEach(c=>{R(g,c[0],c[1],3,1,'#fff');R(g,c[0]+(c[0]>50?0:0),c[1]+(c[1]>40?-2:0),1,3,'#fff')})}},
  mid:(g,i)=>{const h=i.h[0];R(g,h[0]-1,h[1]-4,4,8,'#2a2a3c');R(g,h[0],h[1]-3,2,6,'#8fd3ff');if(fl){R(g,h[0]+2,h[1]-4,3,1,'#fff');R(g,h[0]+3,h[1]-5,1,3,'#fff')}},
  overlay:(g)=>{if(fl){g.fillStyle='rgba(255,255,255,.35)';g.fillRect(0,0,64,80)}}}}});
// 20 DANCE ------------------------------------------------------------
A.push({n:'20  Dance',bg:'night',f:(t,fr)=>{const p=t*PI2*2,b=Math.abs(S(p));
 return{legs:[st(14*S(p),14*S(p)-30*mx0(0,C(p))),st(-14*S(p),-14*S(p)-30*mx0(0,-C(p)))],arms:[{ua:105+55*S(p),fa:105+55*S(p)+35},{ua:105-55*S(p),fa:105-55*S(p)+35}],lean:S(p)*6,dy:-Math.round(b*1.5),hy:-Math.round(b),face:'happy',mouth:'smile',
  scene:(g)=>{ground(g,'#1c2038','#2f3a66');for(let k=0;k<10;k++)px(g,3+k*6,4+(k*13)%20,'#cfd6ff');const c=['#e86fb0','#6df2c4','#ffd23f'];for(let k=0;k<3;k++){const q=(t*3+k/3)%1;const x=44+k*5-q*2,y=40-q*30;g.fillStyle=c[k];g.fillRect(Math.round(x),Math.round(y),2,3);g.fillRect(Math.round(x)+2,Math.round(y)-1,1,2)}},
  head:(g,h)=>{R(g,h.hx-1,h.hy-3,h.hw+2,2,'#e86fb0');R(g,h.hx+4,h.hy+3,4,6,'#e86fb0');R(g,h.hx+5,h.hy+4,2,4,'#ff9ad0')}}}});
