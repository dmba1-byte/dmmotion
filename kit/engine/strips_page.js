// transparent frame strips for the website
function charFrame(P,view){const ch=mk(),g=ch.getContext('2d');let inf;if(view=='side')inf=kit(g,P);else inf=kitFB(g,P,view);let src=ch;if(P.rot&&view=='side')src=rotSprite(ch,Math.round(inf.hipX),Math.round(inf.hipY),P.rot);outline(src);if(P.overlay)P.overlay(src.getContext('2d'),inf||{h:[[0,0]]});return src}
function strip(fn,view,N){N=N||16;const c2=document.createElement('canvas');c2.width=W*N;c2.height=H;const g=c2.getContext('2d');for(let k=0;k<N;k++){const P=fn(k/N,k);delete P.scene;delete P.pre_scene;g.drawImage(charFrame(P,view||'side'),k*W,0)}return c2.toDataURL('image/png')}
const AI=(i)=>(t,fr)=>A[i].f(t,fr);
// ---- wheelchair (side) ----
const WHEEL=(t,fr)=>{const hx=CX-4,hy=GY-12,WX=CX-5,WY=GY-8,RR=8;
 const ph=frac(t*1),push=ph<.6,u=push?ph/.6:(ph-.6)/.4;
 const a=push?lerp(-65,18,u):lerp(18,-65,u)*1,rad_=push?RR:RR+1.5+S(u*PI)*1.5;
 const hand=[WX+Math.sin(rad(a))*rad_,WY-Math.cos(rad(a))*rad_];
 const spin=t*60;
 const wheel=(g)=>{ // ring + 8 spokes, rotating 45deg per loop (seamless)
  for(let d=0;d<360;d+=4){px(g,WX+Math.cos(rad(d))*RR,WY+Math.sin(rad(d))*RR,'#c8c8dc')}
  
  for(let k=0;k<6;k++){const an=rad(spin+k*60);for(let r_=1;r_<RR-1;r_+=1)px(g,WX+Math.cos(an)*r_,WY+Math.sin(an)*r_,'#8a8aa8')}
  R(g,WX-1,WY-1,2,2,'#e0534a')};
  return{hip:[hx,hy],legRel:[[11,8],[12,8]],armIK:[[hand[0]-0.5,hand[1]-.5],[hx+9,hy-3]],arms:[{ua:0,fa:0},{ua:10,fa:20}],lean:7,face:'n',mouth:'smile',nobag:0,
  propBack:(g)=>{ // chair frame behind rider
   line(g,hx-5,hy-1,hx-5,hy-14,2,'#3a3a54');R(g,hx-5,hy-14,4,2,'#2a2a3c');R(g,hx-4,hy+1,12,2,'#3a3a54');R(g,hx+9,hy+4,2,6,'#3a3a54');R(g,hx+9,hy+9,6,2,'#2a2a3c');
   line(g,hx+2,hy+3,WX,WY,2,'#3a3a54');R(g,hx+6,GY-5,4,4,'#6a6a88');R(g,hx+7,GY-4,2,2,'#2a2a3c')},
  prop:(g)=>{wheel(g);R(g,Math.round(hand[0])-1,Math.round(hand[1])-1,3,3,K.skin)}}};
function R_fn(g,x,y,w,h,c){R(g,x,y,w,h,c)}
// ---- front wave ----
const FWAVE=(t,fr)=>{const th=t*PI2,sy=GY-16.5-7;return{hip:GY-16.5+(S(th*2)>0?0:0),feet:[[-3,0],[3,0]],hands:[[CX-7.5,sy+10.5],[CX+9.5+2.5*S(th),sy-9+1.2*C(th)]],sl:1,sa:[1,0],mouth:'open'}};
const FIDLE=(t,fr)=>{const th=t*PI2,sy=GY-16.5-7;return{hip:GY-16.5+(S(th)>.6?-0:0),feet:[[-3,0],[3,0]],hands:[[CX-7.5,sy+10.5+.7*S(th)],[CX+6.5,sy+10.5-.7*S(th)]],sl:1,sa:[1,1],mouth:'smile'}};
window.STRIPS={
 fwave:()=>strip(FWAVE,'f'),
 wheel:()=>strip(WHEEL,'side'),
 walk:()=>strip((t,fr)=>{const P=sideWalk.f(t,fr);return P},'side'),
 read:()=>strip(AI(8),'side'),box:()=>strip(AI(14),'side'),cart:()=>strip(AI(15),'side'),photo:()=>strip(AI(18),'side'),dance:()=>strip(AI(19),'side'),rope:()=>strip(AI(11),'side'),umb:()=>strip(AI(7),'side')
};
