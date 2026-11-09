// ===== FRONT/BACK ENGINE =====
function kitFB(g,P,v){
 const cx=CX,back=v=='b',hipY=P.hip!=null?P.hip:GY-17;
 const fx=P.feet.map((f,i)=>[cx+f[0],GY-f[1]]);
 const L=fx.map((f,i)=>{const jx=cx+(i?3:-3);if(P.sl)return{jx,k:[(jx+f[0])/2,(hipY+f[1])/2],a:f};const r=ik(jx,hipY,f[0],f[1],9,8,i?1:-1);const k=pt(jx,hipY,9,r.th),a=pt(k[0],k[1],8,r.sh);return{jx,k,a}});
 const ny=hipY-10,shY=ny+3,hy=ny-12;
 const SX=[cx-6,cx+5];
 const Ar=P.hands.map((h,i)=>{if(P.sa&&P.sa[i])return{e:[(SX[i]+h[0])/2,(shY+h[1])/2],h};const r=ik(SX[i],shY,h[0],h[1],6,6,i?1:-1);const e=pt(SX[i],shY,6,r.th),hh=pt(e[0],e[1],6,r.sh);return{e,h:hh}});
 const info={hipY,ny,shY,hy,h:Ar.map(a=>a.h),SX};
 P.back&&P.back(g,info);
 (P.order||[0,1]).forEach(i=>{const l=L[i],d=P.dL&&P.dL[i],pc=d?shade(K.pants,.66):K.pants,sc=d?shade(K.shoe,.66):K.shoe,sw=(P.sw&&P.sw[i])||5;line(g,l.jx,hipY,l.k[0],l.k[1],4,pc);line(g,l.k[0],l.k[1],l.a[0],l.a[1],4,pc);R(g,Math.round(l.a[0])-Math.floor(sw/2),Math.round(l.a[1]),sw,2,sc)});
 P.low&&P.low(g,info);
 R(g,cx-5,hipY-2,10,3,K.pants);
 R(g,cx-5,ny+1,10,hipY-ny-2,K.top);R(g,cx-4,ny+1,8,1,K.topL);
 if(back&&!P.nobag){R(g,cx-4,ny+2,8,9,K.bag);R(g,cx-4,ny+2,8,1,K.bagL);R(g,cx-4,ny+2,1,9,shade(K.bag,.8))}
 if(!back&&!P.nobag){R(g,cx-4,ny+1,1,6,K.bag);R(g,cx+3,ny+1,1,6,K.bag)} // straps
 R(g,cx-1,ny-1,3,3,K.skinD);
 const hdy=P.hy||0;
 if(back){R(g,cx-6,hy+hdy,12,12,K.hair);R(g,cx-7,hy-3+hdy,14,6,K.hair);R(g,cx-6,hy+9+hdy,12,3,K.hair);R(g,cx-3,hy+10+hdy,6,2,shade(K.hair,.7))}
 else{R(g,cx-6,hy+hdy,12,12,K.skin);R(g,cx-7,hy+3+hdy,1,3,K.skinD);R(g,cx+6,hy+3+hdy,1,3,K.skinD);
  R(g,cx-7,hy-3+hdy,14,5,K.hair);R(g,cx-7,hy+hdy,2,6,K.hair);R(g,cx+5,hy+hdy,2,6,K.hair);R(g,cx-5,hy+2+hdy,3,1,K.hair);
  const ey=hy+5+hdy;R(g,cx-3,ey,1,2,INK);R(g,cx+2,ey,1,2,INK);
  const m=P.mouth||'smile';if(m=='smile'){R(g,cx-1,hy+9+hdy,3,1,'#8a4a40');R(g,cx-2,hy+8+hdy,1,1,'#8a4a40');R(g,cx+2,hy+8+hdy,1,1,'#8a4a40')}else if(m=='open'){R(g,cx-1,hy+8+hdy,3,3,'#6a2630')}}
 P.mid&&P.mid(g,info);
 (P.aorder||[0,1]).forEach(i=>{const a=Ar[i],d=P.dA&&P.dA[i],s=d?shade(K.top,.74):K.top;line(g,SX[i],shY,a.e[0],a.e[1],3,s);line(g,a.e[0],a.e[1],a.h[0],a.h[1],3,s);R(g,a.h[0]-1,a.h[1]-1,3,3,d?shade(K.skin,.8):K.skin)});
 P.front&&P.front(g,info);
 return info;
}
const FB=[]; // each {n,side:animIndex or obj, f:(t,fr,v)=>P}
const PH=(A_)=>A_;
const walkFB=(t,v)=>{const p=t*PI2*2,sg=v=='f'?1:-1,z=[S(p),-S(p)],lf=[mx0(0,C(p)),mx0(0,-C(p))];
 // front: leg moving toward camera (z>0) lower+bigger+nearer; trailing raised, darker. back: reversed.
 const feet=[0,1].map(i=>{const zz=z[i]*sg;return[(i?1:-1)*(zz>0?3.8:2.4),5*mx0(0,-zz)+2.5*lf[i]]});
 const hip=GY-14.8-2.2*Math.abs(C(p));const sy=hip-7;
 const hands=[0,1].map(i=>{const za=-z[i]*sg;return[CX+(i?6.5:-7.5)+(i?.5:-.5)*(za>0?1:0),sy+10-2.4*za]});
 const near=i=>z[i]*sg>0;
 return{p,hip,feet,hands,sl:1,sa:[1,1],order:near(0)?[1,0]:[0,1],aorder:(-z[0]*sg>0)?[1,0]:[0,1],dL:[!near(0),!near(1)],dA:[-z[0]*sg<=0,-z[1]*sg<=0],sw:[near(0)?5:4,near(1)?5:4]}};
const wlk=(t)=>{const p=t*PI2*2;const l0=mx0(0,C(p)),l1=mx0(0,-C(p));return{p,l0,l1,hip:GY-16.5-.8*(1-mx0(l0,l1))}};
const sideWalk={n:'Walk',bg:'dusk',f:(t,fr)=>{const p=t*PI2*2,bob=(Math.abs(C(p))>.5?0:-1);return{legs:walkLegs(p,28,45),arms:[{ua:-26*S(p),fa:-26*S(p)-14},{ua:26*S(p),fa:26*S(p)-14}],lean:3,dy:bob,face:'n',mouth:'smile',scene:(g)=>{city(g,fr*2,'#38305a');ground(g,'#3a2a3f','#5a4560')}}}};
FB.push({n:'Walk',side:sideWalk,f:(t,fr,v)=>({...walkFB(t,v),scene:(g)=>{city(g,fr*2,'#38305a');ground(g,'#3a2a3f','#5a4560')}})});
FB.push({n:'Ride a bike',side:0,f:(t,fr,v)=>{const p=t*PI2*2,hip=GY-19,ny=hip-10,bar=ny+8;
 return{hip,feet:[[-5,4+3*S(p)],[5,4-3*S(p)]],hands:[[CX-8,bar],[CX+8,bar]],
  scene:(g)=>{city(g,fr*2,'#38305a');ground(g,'#3a2a3f','#5a4560')},
  back:(g)=>{if(v=='b')R(g,CX-9,bar-1,18,2,'#c8c8dc')},
  low:(g)=>{R(g,CX-1,GY-16,3,17,'#2a2a3c');R(g,CX-1,GY-16,1,17,'#4a4a64');for(let k=0;k<4;k++)R(g,CX,GY-14+((k*4+Math.floor(fr*2))%16),1,1,'#b8b8cc');
   if(v=='f'){R(g,CX-2,GY-9,1,0,'#000')}},
  mid:(g)=>{if(v=='f'){R(g,CX-1,bar,1,GY-9-bar,'#e0534a');R(g,CX+1,bar,1,GY-9-bar,'#e0534a');R(g,CX-9,bar-1,18,2,'#c8c8dc');R(g,CX-9,bar-1,18,1,'#e8e8f4')}}}}});
FB.push({n:'Skateboard',side:10,f:(t,fr,v)=>{const back=v=='b',m=back?-1:1;
 // one foot pushes off the ground (comes toward camera & down), other rides the deck
 const ph=frac(t*2),push=ph<.55?S(ph/.55*PI):0; // two pushes per loop
 const pf=back?0:1,gf=1-pf; // pusher index / guide index
 const hip=GY-18+Math.round(S(t*PI2*2)*.6),ny=hip-10,sy=hip-7;
 const feet=[[0,0],[0,0]];
 feet[gf]=[(gf?3:-3),6]; feet[pf]=[(pf?4:-4)+(push>0?(pf?1.5:-1.5)*push:0),6-6*push];
 const hands=[[CX-8,sy+9.5-(pf==0&&push>0?1.5*push:0)],[CX+7,sy+9.5-(pf==1&&push>0?1.5*push:0)]];
 const pusherNear=push>.15; // pusher on ground is nearest camera in front view
 const nearIdx=(back?!pusherNear:pusherNear)?pf:gf;
 const farIdx=1-nearIdx;
 return{hip,feet,hands,sl:1,sa:[1,1],order:[farIdx,nearIdx],dL:[farIdx==0,farIdx==1],aorder:[farIdx,nearIdx],dA:[farIdx==0,farIdx==1],sw:[nearIdx==0?5:4,nearIdx==1?5:4],
  scene:(g)=>{city(g,fr*2,'#38305a');ground(g,'#3a2a3f','#5a4560')},
  low:(g)=>{R(g,CX-5,GY-4,10,2,'#e0534a');R(g,CX-5,GY-4,10,1,'#f0766c');R(g,CX-6,GY-2,3,3,'#e8dcc8');R(g,CX+3,GY-2,3,3,'#e8dcc8')}}}});
FB.push({n:'Carry a box',side:14,f:(t,fr,v)=>{const w=wlk(t),ny=walkFB(t,v).hip-10;
 const box=(g)=>{const x=CX-7;R(g,x,ny+2,14,11,'#b8864f');R(g,x,ny+2,14,2,'#d4a26a');R(g,x+6,ny+2,2,11,'#e8d8a8');R(g,x,ny+11,14,2,'#9a6e3d');R(g,x+1,ny+7,4,2,'#f2efe6')};
 const wf=walkFB(t,v);return{hip:wf.hip,feet:wf.feet,sl:1,order:wf.order,dL:wf.dL,sw:wf.sw,hands:[[CX-9,ny+9],[CX+9,ny+9]],
  scene:(g)=>{city(g,fr*2,'#38305a');ground(g,'#3a2a3f','#5a4560')},
  back:(g)=>{if(v=='b')R(g,CX-8,ny+2,16,11,'#b8864f')},
  mid:(g)=>{if(v=='f')box(g)}}}});
FB.push({n:'Jump rope',side:11,f:(t,fr,v)=>{const th=t*PI2*3,air=Math.round(3*Math.pow(mx0(0,-C(th)),2));const hip=GY-17-air,ny=hip-10;
 const hy=ny+11+Math.round(1.5*S(th)),hxx=9;
 const rope=(g,col)=>{const ap=C(th)>=0?lerp(hy,ny-18,C(th)):lerp(hy,GY-1,-C(th));g.fillStyle=col;for(let x=-hxx;x<=hxx;x++){const u=x/hxx,y=hy+(ap-hy)*(1-u*u);g.fillRect(CX+x,Math.round(y),1,1)}};
 const front=(v=='f')?S(th)>0:S(th)<=0;
 return{hip,feet:[[-2.5,air],[2.5,air]],hands:[[CX-hxx,hy],[CX+hxx,hy]],
  scene:(g)=>{ground(g,'#7aa86a','#8fc07c');for(let k=0;k<8;k++)px(g,4+k*8,GY+3+(k%3),'#6a9a5a');for(let k=0;k<4;k++){R(g,3+k*17,GY-6,2,6,'#8a5e3a');R(g,2+k*17,GY-9,4,4,'#4e9a5a')}},
  back:(g)=>{if(!front)rope(g,'#c8bf9c')},front:(g)=>{if(front)rope(g,'#fff7d8')}}}});
FB.push({n:'Umbrella in the rain',side:7,f:(t,fr,v)=>{const wf=walkFB(t,v),ny=wf.hip-10,y0=ny-22,c0=CX+5;
 return{hip:wf.hip,feet:wf.feet,sl:1,order:wf.order,dL:wf.dL,sw:wf.sw,sa:[1,0],aorder:wf.aorder,dA:[wf.dA[0],0],hands:[wf.hands[0],[CX+8,ny+4]],
  scene:(g)=>{const sc=A[7].f(t,fr).scene;sc&&sc(g)},
  mid:(g)=>{R(g,CX+8,y0+5,1,ny-y0-1,'#c8c8dc')},
  front:(g)=>{[[10,0],[16,1],[20,2],[22,3],[22,4]].forEach(([w_,d])=>R(g,c0-w_/2,y0+d,w_,1,d%2?'#e0534a':'#f06a5e'));for(let k=0;k<5;k++)R(g,c0-11+k*5,y0+5,2,1,'#c03e38');R(g,c0-1,y0-1,2,1,'#c8c8dc')}}}});
window.drawFB=function(frame,set){
 const rows=FB.slice(set*3,set*3+3);const CW=288,CH=360,GAP=24,X0=48;
 ctx.fillStyle='#14121f';ctx.fillRect(0,0,1008,1080);
 rows.forEach((a,r)=>{const t=(frame%32)/32,fr=(frame%32)/2,bgc=BGS[(typeof a.side=='number'?A[a.side]:a.side).bg];
  ['f','s','b'].forEach((v,c)=>{const x=X0+c*(CW+GAP),y=r*CH;
   const gr=ctx.createLinearGradient(0,y,0,y+CH);gr.addColorStop(0,bgc[0]);gr.addColorStop(.6,bgc[1]);gr.addColorStop(1,bgc[2]);ctx.fillStyle=gr;ctx.fillRect(x,y,CW,CH);
   let L;
   if(v=='s'){L=render(typeof a.side=='number'?A[a.side]:a.side,frame)}
   else{const P=a.f(t,fr,v);L=mk();const g=L.getContext('2d');P.scene&&P.scene(g);const ch=mk();kitFB(ch.getContext('2d'),P,v);outline(ch);g.drawImage(ch,0,0)}
   ctx.imageSmoothingEnabled=false;ctx.drawImage(L,0,0,W,H,x,y,CW,CH);
   ctx.fillStyle='#fff';ctx.shadowColor='rgba(0,0,0,.6)';ctx.shadowBlur=4;ctx.font='bold 20px Inter, sans-serif';ctx.fillText(a.n+' · '+({f:'FRONT',s:'SIDE',b:'BACK'})[v],x+10,y+26);ctx.shadowBlur=0});
 });
};
