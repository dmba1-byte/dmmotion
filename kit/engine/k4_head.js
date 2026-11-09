
const ctx=c.getContext('2d');const W=64,H=80,GY=69,CX=32;const QS=new URLSearchParams(location.search);
function mk(){const o=document.createElement('canvas');o.width=W;o.height=H;return o}
function R(g,x,y,w,h,col){g.fillStyle=col;g.fillRect(Math.round(x),Math.round(y),w,h)}
function px(g,x,y,col){g.fillStyle=col;g.fillRect(Math.round(x),Math.round(y),1,1)}
function line(g,x0,y0,x1,y1,w,col){x0=Math.round(x0);y0=Math.round(y0);x1=Math.round(x1);y1=Math.round(y1);
 const dx=Math.abs(x1-x0),dy=-Math.abs(y1-y0),sx=x0<x1?1:-1,sy=y0<y1?1:-1;let e=dx+dy;g.fillStyle=col;
 for(;;){g.fillRect(x0-Math.floor(w/2),y0-Math.floor(w/2),w,w);if(x0==x1&&y0==y1)break;const e2=2*e;if(e2>=dy){e+=dy;x0+=sx}if(e2<=dx){e+=dx;y0+=sy}}}
function outline(o){const g=o.getContext('2d');const d=g.getImageData(0,0,W,H),s=d.data,n=new Uint8ClampedArray(s);
 const a=(x,y)=>x<0||y<0||x>=W||y>=H?0:s[(y*W+x)*4+3];
 for(let y=0;y<H;y++)for(let x=0;x<W;x++)if(!a(x,y)&&(a(x+1,y)||a(x-1,y)||a(x,y+1)||a(x,y-1))){const i=(y*W+x)*4;n[i]=0x1a;n[i+1]=0x16;n[i+2]=0x2e;n[i+3]=255}
 g.putImageData(new ImageData(n,W,H),0,0)}
const rad=d=>d*Math.PI/180,pt=(x,y,l,a)=>[x+Math.sin(rad(a))*l,y+Math.cos(rad(a))*l];
function shade(h,k){const n=parseInt(h.slice(1),16);const c=v=>Math.max(0,Math.min(255,Math.round(v*k)));return `rgb(${c((n>>16)&255)},${c((n>>8)&255)},${c(n&255)})`}
const K={skin:'#c98b69',skinD:'#a86f52',top:'#e6b84c',topL:'#f4d27a',pants:'#5b5f7a',shoe:'#e8dcc8',bag:'#5c8a7a',bagL:'#7fb09e',hair:'#2a1f28',hw:12,hh:12,tl:10,th:9,sh:8,ua:6,fa:6,tw:8,lw:4,aw:3,foot:5};
const INK='#1a162e',S=Math.sin,C=Math.cos,PI=Math.PI,PI2=PI*2,mx0=Math.max,mn=Math.min;
const st=(a,b)=>({th:a,sh:b}),lerp=(a,b,u)=>a+(b-a)*u,sm=u=>{u=mx0(0,mn(1,u));return u*u*(3-2*u)},cl=(u)=>mx0(0,mn(1,u));
function ik(jx,jy,tx,ty,l1,l2,side){let dx=tx-jx,dy=ty-jy,d=Math.hypot(dx,dy);d=mn(d,l1+l2-.3);d=mx0(d,.5);const base=Math.atan2(dx,dy)*180/PI;
 const A=Math.acos(mx0(-1,mn(1,(l1*l1+d*d-l2*l2)/(2*l1*d))))*180/PI;const th=base+side*A;const k=pt(jx,jy,l1,th);const sh=Math.atan2(tx-k[0],ty-k[1])*180/PI;return{th,sh}}
function kit(g,P){
 const o=K;let hipX=CX+(P.dx||0),hipY;
 const lean=P.lean||0;
 // legs
 let L=P.legs;
 const hipFix=P.hip;
 if(hipFix){hipX=hipFix[0];hipY=hipFix[1];
   if(P.legIK)L=P.legIK.map(t=>ik(hipX,hipY,t[0],t[1],o.th,o.sh,1));
   if(P.legRel)L=P.legRel.map(t=>ik(hipX,hipY,hipX+t[0],hipY+t[1],o.th,o.sh,1));}
 const J=(l)=>{const k=pt(0,0,o.th,l.th),a=pt(k[0],k[1],o.sh,l.sh);return{k,a}};
 const F=L.map(J);
 if(!hipFix){ {const low=mx0(F[0].a[1],F[1].a[1]);hipY=GY-low-1;} hipY-=(P.air||0)}
 const nx=hipX+Math.sin(rad(lean))*o.tl,ny=hipY-Math.cos(rad(lean))*o.tl+(P.dy||0),shY=ny+3;
 let Aa=P.arms;
 if(P.armIK)Aa=P.armIK.map(t=>t?ik(nx,shY,t[0],t[1],o.ua,o.fa,-1):null).map((a,i)=>a||P.arms[i]);
 if(P.armRel)Aa=P.armRel.map((t,i)=>t?ik(nx,shY,nx+t[0],shY+t[1],o.ua,o.fa,-1):P.arms[i]);
 const arm=(A)=>{const e=pt(nx,shY,o.ua,A.th!=null?A.th:A.ua),h=pt(e[0],e[1],o.fa,A.sh!=null?A.sh:A.fa);return{e,h}};
 const Ar=Aa.map(arm);
 const hx=nx-6+(P.hx||0),hy=ny-o.hh+(P.hy||0),hw=o.hw;
 const info={hipX,hipY,nx,ny,hx,hy,hw,h:Ar.map(a=>a.h),F};
 const dArm=(a,s,sk)=>{line(g,nx,shY,a.e[0],a.e[1],o.aw,s);line(g,a.e[0],a.e[1],a.h[0],a.h[1],o.aw,s);R(g,a.h[0]-1,a.h[1]-1,3,3,sk)};
 const dLeg=(f,pc,sc)=>{line(g,hipX,hipY,hipX+f.k[0],hipY+f.k[1],o.lw,pc);line(g,hipX+f.k[0],hipY+f.k[1],hipX+f.a[0],hipY+f.a[1],o.lw,pc);R(g,Math.round(hipX+f.a[0])-1,Math.round(hipY+f.a[1]),o.foot,2,sc)};
 P.pre&&P.pre(g,info);
 dArm(Ar[1],shade(o.top,.78),shade(o.skin,.85));
 dLeg(F[1],shade(o.pants,.78),shade(o.shoe,.78));
 P.propBack&&P.propBack(g,info);
 line(g,hipX,hipY-1,nx,ny+2,o.tw,o.top);R(g,nx-4,ny+1,8,2,o.topL);
 if(!P.nobag){R(g,nx-8,ny+2,5,9,o.bag);R(g,nx-8,ny+2,5,1,o.bagL)}
 R(g,nx-1,ny-1,3,3,o.skinD);
 R(g,hx,hy,hw,o.hh,o.skin);R(g,hx+hw,hy+6,1,2,o.skin);
 R(g,hx-1,hy-3,hw+2,5,o.hair);R(g,hx-1,hy,3,8,o.hair);R(g,hx+hw-2,hy+2,2,1,o.hair);
 const ex=hx+hw-4,ey=hy+(P.look?4:5),mx=hx+hw-5,my=hy+9,f=P.face||'n';
 if(f=='n'||f=='o'||f=='look'){R(g,ex,ey,1,f=='o'?3:2,INK)}
 if(f=='closed'){R(g,ex-1,ey+1,3,1,INK)}
 if(f=='happy'){R(g,ex-1,ey+1,1,1,INK);R(g,ex,ey,1,1,INK);R(g,ex+1,ey+1,1,1,INK)}
 const m=P.mouth||'smile';
 if(m=='smile'){R(g,mx,my,3,1,'#8a4a40');R(g,mx+3,my-1,1,1,'#8a4a40')}
 if(m=='open'){R(g,mx,my-1,4,3,'#6a2630');R(g,mx+1,my+1,2,1,'#e0707a')}
 if(m=='small'){R(g,mx+1,my,2,2,'#6a2630')}
 if(m=='flat'){R(g,mx,my,3,1,'#8a4a40')}
 if(m=='wide'){R(g,mx-1,my-1,5,3,'#6a2630');R(g,mx,my-1,3,1,'#f6f0e6')}
 P.head&&P.head(g,{hx,hy,hw});
 P.mid&&P.mid(g,info);
 dLeg(F[0],o.pants,o.shoe);
 dArm(Ar[0],o.top,o.skin);
 P.prop&&P.prop(g,info);
 return info;
}
function ring(g,cx,cy,r,col){for(let a=0;a<360;a+=3){px(g,cx+Math.cos(rad(a))*r,cy+Math.sin(rad(a))*r,col)}}
function city(g,sc,col){g.fillStyle=col;for(let k=-1;k<9;k++){const x=k*14-(sc%14);const h=14+((k+Math.floor(sc/14)+20)*37)%22;g.fillRect(Math.round(x),GY-h+1,10,h)}}
function ground(g,col,top){g.fillStyle=col;g.fillRect(0,GY+1,W,H-GY-1);g.fillStyle=top;g.fillRect(0,GY+1,W,1)}
