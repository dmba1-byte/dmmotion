// ===== fx.js : QA registry, auto contact shadows, pixel font, lighting, proper sitting, profile door =====
window.QA={chars:[],solids:[]};
function solid(name,x0,x1){QA.solids.push({name,x0,x1})}
const _person0=person;
person=function(P,ox,oy,look,front,flip){
 const cx=Math.round(ox)+CX,gy=FL-Math.round(oy||0);
 if(!P.noShadow){wg.globalAlpha=.22;R(wg,cx-8,gy,16,1,'#000');R(wg,cx-6,gy+1,12,1,'#000');wg.globalAlpha=1}
 const inf=_person0(P,ox,oy,look,front,flip);
 QA.chars.push({k:(look&&look.id)||(look&&look.top)||'kit',x:Math.round(ox),cx,oy:Math.round(oy||0),flip:!!flip,sit:!!P.hip,ok:!!P.okOverlap,
  sig:JSON.stringify([P.legs,P.arms,P.armIK,P.armRel,P.lean,P.face,P.dy,P.legRel,P.air,P.look])});
 return inf};
function kitp(P,ox,oy,flip){P.nobag=false;return person(P,ox,oy,null,null,flip)}
// world coords of a hand
function handW(inf,i,ox,flip){return flip?[Math.round(ox)+W-inf.h[i][0],OY+inf.h[i][1]]:[Math.round(ox)+inf.h[i][0],OY+inf.h[i][1]]}

// 3x5 pixel font for signs inside the world
const GL={A:[2,5,7,5,5],B:[6,5,6,5,6],C:[3,4,4,4,3],D:[6,5,5,5,6],E:[7,4,6,4,7],F:[7,4,6,4,4],G:[3,4,5,5,3],H:[5,5,7,5,5],I:[7,2,2,2,7],J:[1,1,1,5,2],K:[5,5,6,5,5],L:[4,4,4,4,7],M:[5,7,7,5,5],N:[6,5,5,5,5],O:[2,5,5,5,2],P:[6,5,6,4,4],Q:[2,5,5,6,3],R:[6,5,6,5,5],S:[3,4,2,1,6],T:[7,2,2,2,2],U:[5,5,5,5,7],V:[5,5,5,5,2],W:[5,5,7,7,5],X:[5,5,2,5,5],Y:[5,5,2,2,2],Z:[7,1,2,4,7],
 0:[7,5,5,5,7],1:[2,6,2,2,7],2:[6,1,2,4,7],3:[6,1,2,1,6],4:[5,5,7,1,1],5:[7,4,6,1,6],6:[3,4,7,5,7],7:[7,1,2,2,2],8:[7,5,7,5,7],9:[7,5,7,1,6],'+':[0,2,7,2,0],'-':[0,0,7,0,0],'?':[6,1,2,0,2],'.':[0,0,0,0,2],'>':[4,2,1,2,4]};
function ptext(g,s,x,y,col){let cx=Math.round(x);for(const ch of s){const r=GL[ch];if(r)r.forEach((m,j)=>{for(let b=0;b<3;b++)if(m&(4>>b))px(g,cx+b,y+j,col)});cx+=4}}
const ptw=s=>s.length*4-1;

// output-resolution lighting, clipped to the scene window
function lit(fn){og.save();og.beginPath();og.rect(0,672,1080,1248);og.clip();fn();og.restore()}
function grade(col,a,mode){og.save();og.globalCompositeOperation=mode||'multiply';og.globalAlpha=a;og.fillStyle=col;og.fillRect(0,672,1080,1248);og.restore()}
function shaft(x0,x1,y0,x2,x3,y1,col,a){og.save();og.globalAlpha=a;og.fillStyle=col;og.beginPath();og.moveTo(x0*12,y0*12);og.lineTo(x1*12,y0*12);og.lineTo(x3*12,y1*12);og.lineTo(x2*12,y1*12);og.fill();og.restore()}
const WARM='rgba(255,214,140,A)',COOL='rgba(170,200,255,A)',FIRE='rgba(255,140,60,A)',GREEN='rgba(120,255,170,A)',SUN='rgba(255,244,200,A)',RED='rgba(255,120,110,A)';

// proper sitting: hips on the seat, knees bent, both feet flat on the floor
const SEAT=FL-10; // world y of a seat top
function sitP(o){o=o||{};const hx=CX-2,hy=GY-12;
 const P={hip:[hx,hy],legRel:[[9,12],[11,12]],arms:[{ua:20,fa:50},{ua:12,fa:40}],lean:o.lean==null?6:o.lean,face:o.face||'n',mouth:o.mouth||'flat',look:o.look,dy:o.dy||0};
 if(o.hands)P.armIK=o.hands;return P}
function stool(g,ox){const x=Math.round(ox)+CX-8;R(g,x,SEAT,11,2,'#8a6a4a');R(g,x,SEAT,11,1,'#a88a66');R(g,x+1,SEAT+2,1,8,'#5a3e28');R(g,x+9,SEAT+2,1,8,'#5a3e28');R(g,x+1,SEAT+6,9,1,'#5a3e28')}

// door seen in profile: wall cut at x, interior on the left, exterior on the right. u = 0 closed .. 1 swung outward.
const BRASS='#d9b24a',BARY=95;
function pdoor(g,x,u,o){o=o||{};const top=62,h=FL-top,lf=o.leaf||'#7a5434',lfL=o.leafL||'#9a7250',j=o.jit||0;
 R(g,x,56,5,top-56,o.wall||'#4a4458');R(g,x,56,1,top-56,o.wallL||'#6a6480');R(g,x+4,56,1,top-56,'#2a2634');
 R(g,x-1,top-2,7,2,o.trim||'#5a3e28');R(g,x,FL,5,1,'#9a9aa6');
 const w=Math.round(u*19);
 if(w<2){R(g,x+1+j,top,3,h,lf);R(g,x+1+j,top,1,h,lfL);R(g,x+3+j,top,1,h,'#4a3220');
  if(o.bar){R(g,x-2+j,BARY,3,2,BRASS);R(g,x-2+j,BARY,3,1,'#f4dc8a');R(g,x+j,BARY-2,1,6,'#8a6a2a')}
  if(o.knob){R(g,x-2+j,BARY+3,3,3,BRASS);px(g,x-2+j,BARY+3,'#f4dc8a')}
 }else{const x0=x+5;R(g,x0,top,w,h,lf);R(g,x0,top,w,1,lfL);R(g,x0+w-1,top,1,h,'#4a3220');R(g,x0,top,1,h,'#3a2616');
  if(w>8){R(g,x0+2,top+4,w-4,22,shade(lf,.86));R(g,x0+2,top+38,w-4,16,shade(lf,.86))}
  if(o.bar){R(g,x0+1,BARY,w-2,2,BRASS);R(g,x0+1,BARY,w-2,1,'#f4dc8a');R(g,x0+1,BARY-1,1,4,'#8a6a2a');R(g,x0+w-2,BARY-1,1,4,'#8a6a2a')}
  if(o.knob)R(g,x0+w-4,BARY+3,3,3,BRASS)}
}
function woodFloor(g,a,b,c){R(g,0,FL,WW,1,c);for(let y=FL+1;y<WH;y++){const band=Math.floor((y-FL-1)/6);R(g,0,y,WW,1,(y-FL-1)%6==0?c:(band%2?a:b))}for(let k=0;k<7;k++){const y=FL+1+k*6;for(let x=((k*11)%17);x<WW;x+=17)R(g,x,y,1,6,c)}}
function snow(g,t,n,cam){for(let k=0;k<n;k++){const sp=7+(k%5)*2.5,x=(((k*37+11)-((cam||0)*(.6+(k%3)*.3))+Math.sin(t*1.3+k)*3)%WW+WW)%WW,y=56+((t*sp+k*23)%104);g.globalAlpha=k%3?.9:.55;px(g,x,y,'#f6f8ff');g.globalAlpha=1}}
