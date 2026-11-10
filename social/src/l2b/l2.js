// ===== Level 02 (rebuilt) : Ed Roberts — three plausible options =====
const END=84.0;
const SUBS=[[0.12,1.53,"You got into your dream college."],[1.96,3.5,"But the machine that keeps you breathing"],[3.5,5.03,"weighs eight hundred pounds."],
[5.29,5.92,"Level two."],[6.12,7.57,"Berkeley, 1962."],
[7.83,9.61,"Ed Roberts got polio at fourteen."],[10.13,11.9,"It paralyzed him from the neck down,"],[11.9,13.51,"and he slept in an iron lung."],
[13.77,16.6,"The state said he was too disabled to ever hold a job."],[17.17,19.64,"And the university said no dorm could take him."],
[19.9,20.5,"You're Ed."],[20.5,21.19,"Three options."],[21.42,22.29,"Which one would you pick?"],
[22.81,23.73,"Option A."],[24.2,25.78,"Take the university to court,"],[26.06,27.25,"and make it give you a room."],
[27.82,28.8,"Option B."],[29.27,30.4,"Study from home,"],[30.4,32.11,"and take your classes by telephone."],
[32.68,33.66,"Option C."],[34.13,35.65,"Move into the campus hospital,"],[35.9,37.01,"and call it your dorm."],
[40.33,41.58,"Option A sounds right."],[42.08,44.76,"But in 1962, there was no law to sue under."],[45.28,47.59,"The first federal one came eleven years later."],
[47.85,49.26,"Option B sounds easy."],[49.74,51.3,"But that's how he did high school,"],[51.3,52.72,"by telephone, from his bedroom."],[53.16,54.38,"He wanted to be in the room."],
[54.64,56.01,"Option C is what he did."],[56.51,59.17,"The head of campus health offered an empty hospital wing."],[59.72,61.44,"Ed said yes, on one condition."],[61.76,63.64,"Treat it as a dorm, not a ward."],
[63.9,65.56,"More disabled students followed."],[66.0,68.0,"They called themselves the Rolling Quads."],
[68.26,69.86,"And in 1976,"],[70.3,72.4,"the state that said he couldn't hold a job"],[72.4,74.38,"made him director of that same agency."],
[74.64,75.77,"Today, the A.D.A. says"],[76.27,79.44,"a curb ramp can rise one inch for every twelve, at most."],
[79.7,80.42,"Level cleared."],[80.78,81.75,"Comment what you picked,"],[81.75,83.18,"and follow for level three."]];
const SEG=[[0,5.15,0,5.15,'fit','plan'],[5.15,7.69,0,2.54,'shrug','front'],[7.69,9.9,3.97,5.9,'lung','side'],[9.9,11.9,0,2.0,'face1','closeup'],[11.9,13.63,5.9,7.2,'lung','side'],
[13.63,16.9,0,2.97,'file','detail'],[16.9,19.76,7.85,11.6,'dean','side'],[19.76,22.55,0,2.79,'ask','front'],
[22.55,27.55,0,5.0,'pA','wide'],[27.55,32.4,0,4.85,'pB','detail'],[32.4,37.25,0,4.85,'pC','wide'],[37.25,40.25,0,3.0,'choice','menu'],
[40.25,42.0,5.0,6.75,'A1','wide'],[42.0,47.71,0,5.71,'A','detail'],[47.71,49.5,4.85,6.64,'B1','detail'],[49.5,52.9,4.2,6.84,'B','side'],[52.9,54.5,0,1.6,'face1b','closeup'],
[54.5,56.3,4.85,6.65,'C1','wide'],[56.3,59.5,14.92,17.5,'wing','side'],[59.5,61.6,0,2.1,'face3','closeup'],[61.6,63.76,17.5,19.6,'wing','side'],
[63.76,66.0,19.6,21.8,'quads','side'],[66.0,68.12,0,2.12,'quadsF','front'],[68.12,71.5,30.06,33.08,'director','side'],[71.5,74.5,0,3.0,'face2','closeup'],
[74.5,77.6,35.47,40.53,'today','side'],[77.6,79.56,0,1.6,'slope','diagram'],[79.56,END,36.36,40.5,'win','front']];
const CUTS=SEG.slice(1).map(s=>s[0]);
function lungTop(g,x,y){ // iron lung seen from above, head end at the left
 R(g,x-1,y-1,46,18,INKC);for(let i=0;i<44;i++){const e=Math.min(i,43-i),r=e<2?2:e<4?1:0;R(g,x+i,y+r,1,16-2*r,'#aeb0b6');R(g,x+i,y+r,1,2,'#d8dadf');R(g,x+i,y+13-r,1,3,'#7e8088')}
 for(const sx of[x+12,x+28])R(g,sx,y+1,1,14,'#8a8c94');for(const p of[x+17,x+24,x+34]){R(g,p,y+6,4,4,'#5e6068');R(g,p+1,y+7,2,2,'#8aa3c8')}
 R(g,x-3,y+1,3,14,'#7e8088');R(g,x-15,y+3,12,10,INKC);R(g,x-14,y+4,11,8,'#e8e0cc');R(g,x-11,y+5,7,6,LOOK.ed.skin);R(g,x-13,y+5,3,6,LOOK.ed.hair)}
function sceneFit(q,t){const g=wg;R(g,0,0,WW,56,NAVY);
 for(let y=56;y<WH;y++)R(g,0,y,WW,1,'#cfc5b0');for(let y=56;y<WH;y+=8)R(g,0,y,54,1,'#bdb39e');for(let x=4;x<54;x+=8)R(g,x,56,1,104,'#bdb39e');
 R(g,54,60,34,96,INKC);R(g,57,63,28,90,'#efe6d0');for(let y=63;y<153;y+=6)R(g,57,y,28,1,'#e4dac2');
 R(g,54,98,3,14,'#efe6d0');line(g,57,98,67,105,1,'#6b4e36');for(let a=0;a<=60;a+=10)px(g,57+Math.cos(rad(a))*13,98+Math.sin(rad(a))*13,'#a9a090');
 R(g,66,66,18,28,INKC);R(g,67,67,16,26,'#9ab0c8');R(g,67,67,16,7,'#f4ecd8');R(g,69,69,12,3,'#fffaf0');
 R(g,62,138,20,12,INKC);R(g,63,139,18,10,'#8a6a4a');R(g,66,141,7,5,'#f4ecd8');R(g,74,118,9,14,INKC);R(g,75,119,7,12,'#7a5a3c');ptext(g,'DORM',62,112,'#a9a090');
 const hit=9;let x=lerp(-62,hit,ease(seg(q,.1,1.5)));if(q>1.5){const b=(q-1.5)%1.1;x=hit-(b<.25?Math.sin(b/.25*PI)*5:0)}
 const jx=(q>1.5&&((q-1.5)%1.1)<.08)?1:0;lungTop(g,Math.round(x)+jx,97);
 if(q>1.4){ptext(g,'IRON LUNG',10,86,'#5a5448');ptext(g,'DOOR',59,90,'#c0503f')}
 return{}}
function sceneShrug(q,t){const g=wg;blueprintWall(g,t);const br=Math.sin(t*2.4)>.5?-1:0,sh=Math.round(Math.sin(q*7));
 personFB({hip:GY-17,feet:[[-3,0],[3,0]],sl:1,sa:[1,1],hands:[[CX-14,SHY+5+sh],[CX+13,SHY+5+sh]],mouth:'open',hy:br,nobag:false},13,0,null,'f');return{}}
function sceneFace1(q,t){const g=wg;R(g,0,0,WW,56,NAVY);for(let x=0;x<WW;x++)R(g,x,56,1,104,x%6==0?'#8f7d5c':'#9a8866');R(g,58,60,26,40,'#2a2018');R(g,60,62,22,36,'#101a3a');R(g,70,62,2,36,'#2a2018');R(g,74,68,5,5,'#f2f0d8');
 R(g,0,128,WW,32,'#e8e0cc');R(g,0,128,WW,2,'#f6f0e2');
 portrait(g,LOOK.ed,{blink:(t%2.3)<.12,brow:1,ex:q<1.2?0:1,ey:-1,mouth:'flat'});return{}}
function sceneFace2(q,t){const g=wg;office(g,t,true);g.globalAlpha=.3;R(g,0,56,WW,104,'#1a1008');g.globalAlpha=1;
 portrait(g,LOOK.ed,{blink:(t%2.6)<.12,mouth:'smile',dy:Math.sin(t*2.2)>.4?1:0});
 R(g,22,146,46,12,INKC);R(g,23,147,44,10,'#e9d9a6');ptext(g,'DIRECTOR',29,150,'#3a2a14');return{}}
function sceneCal(q,t){const g=wg;R(g,0,0,WW,56,NAVY);for(let y=56;y<WH;y++)R(g,0,y,WW,1,'#9aa58f');R(g,0,128,WW,3,'#6a6a5a');R(g,0,131,WW,29,'#6a6658');
 R(g,43,60,4,6,'#3a3a44');g.globalAlpha=.3;R(g,19,70,56,60,'#1a1008');g.globalAlpha=1;R(g,17,66,56,60,INKC);R(g,18,67,54,58,'#f4ecd8');R(g,18,67,54,12,'#c43c3c');ptext(g,'NEW DORM',30,71,'#fff6e0');
 for(let k=0;k<5;k++)R(g,22+k*10,112,7,1,'#c9c0a8');for(let k=0;k<5;k++)R(g,22+k*10,118,7,1,'#c9c0a8');
 const f=(q*3.2)%1;if(f<.5){const h=Math.round(f*2*30);R(g,18,125-h,54,1,'#c9c0a8');g.globalAlpha=.25;R(g,18,125-h,54,h,'#8a8478');g.globalAlpha=1}
 for(let k=0;k<3;k++){const a=((q*.9+k/3)%1),x=20+k*24+a*14,y=126+a*30;R(g,x,y,8,6,'#f4ecd8');R(g,x,y,8,1,'#c43c3c')}
 return{yr:1962+Math.min(8,Math.floor(q*3.2))}}
function chairF(g,i){const hy=i.hipY;for(const x of[CX-12,CX+9]){R(g,x,hy-9,3,GY-hy+10,'#c8c8dc');R(g,x+1,hy-7,1,GY-hy+6,'#8a8aa8')}R(g,CX-7,i.ny,14,12,'#3a3a54');R(g,CX-6,GY-1,4,2,'#6a6a88');R(g,CX+2,GY-1,4,2,'#6a6a88')}
function sceneQuadsF(q,t){const g=wg;campus(g,60,t);
 [['a1',-13,0],['ed',13,1],['a2',39,2]].forEach(([l,ox,k])=>{const wv=k==1?Math.round(Math.sin(q*8)*2):0,hip=GY-12,br=Math.sin(t*3.3+k*1.3)>.2?-1:0;
  const P={hip,feet:[[-3,0],[3,0]],sl:1,sa:[1,1],hands:k==1?[[CX-10,hip-3],[CX+12,hip-22+wv]]:[[CX-10,hip-3],[CX+9,hip-3]],mouth:k==1?'open':'smile',hy:br,back:chairF,okOverlap:true};
  personFB(P,ox,0,Object.assign({},LOOK[l],{id:'q'+l}),'f')});return{}}
function sceneSlope(q,t){const g=wg;blueprintWall(g,t);g.globalAlpha=.55;R(g,0,56,WW,104,'#0a1433');g.globalAlpha=1;
 const x0=9,y0=112,u=6;for(let i=0;i<12;i++){R(g,x0+i*u,y0,u,u,i%2?'#3f8fb0':'#5fb0d0');R(g,x0+i*u,y0,1,u,'#0a1433')}
 line(g,x0,y0-1,x0+72,y0-7,1,CREAM);R(g,x0+72,y0-7,u,u+1,MINT);ptext(g,'12',x0+32,y0+9,'#cfe2ff');ptext(g,'1',x0+81,y0-6,MINT);
 const ox=lerp(-30,22,seg(q,0,1.6)),wx=ox+37,yy=Math.max(0,Math.min(6,(wx-x0)/12))+ (FL-(y0-1));drawKitY(roll(t,ox+40,true),ox,yy);return{}}
function sceneCourt(q,t){const g=wg;R(g,0,0,WW,56,NAVY);for(let y=56;y<FL;y++)R(g,0,y,WW,1,mixc('#6fb0ea','#e6f4fb',(y-56)/64));cloud(g,(10+t*2)%110-14,62,16);cloud(g,(60+t*1.4)%110-14,72,12);
 R(g,8,84,74,36,'#e4dccb');R(g,8,84,74,2,'#f4eee0');for(let k=0;k<16;k++)R(g,8+k*2.3,83-k,74-k*4.6,1,'#d2c9b6');R(g,43,70,4,8,'#b0a692');
 for(let c=0;c<6;c++){const x=13+c*12;R(g,x,88,6,28,'#f4eee0');R(g,x,88,1,28,'#fffaf0');R(g,x+5,88,1,28,'#cfc6b4');R(g,x-1,86,8,2,'#d2c9b6');R(g,x-1,116,8,2,'#d2c9b6')}
 R(g,38,98,14,18,'#5a3e28');R(g,44,98,1,18,'#3a2616');R(g,24,76,42,9,INKC);R(g,25,77,40,7,'#d9b24a');ptext(g,'COURT',36,78,'#3a2a14');
 for(let k=0;k<4;k++)R(g,4-k*0+k*1,118+k*0,82-k*2,1,'#cfc6b4');for(let y=FL;y<WH;y++)R(g,0,y,WW,1,(y-FL)%6==0?'#b9b2a4':'#cfc8ba');for(let k=0;k<5;k++)R(g,14+k*3,FL+k*5,62-k*6+k*12,5,k%2?'#d8d2c6':'#cfc8ba');
 R(g,84,62,1,58,'#6a6a78');const w=Math.round(Math.sin(t*3)*1);R(g,74,63+w,10,3,'#c0503f');R(g,74,66+w,10,3,'#f4eee0');R(g,74,63+w,4,4,'#3f5fa0');
 if(q>5.2){const a=ease(seg(q,5.2,5.6));g.globalAlpha=a;R(g,36,96,18,22,INKC);R(g,37,97,16,20,'#3a2a20');ptext(g,'NO',41,100,CORAL);ptext(g,'LAW',39,108,CORAL);g.globalAlpha=1}return{}}
function sceneTel(q,t){const g=wg;R(g,0,0,WW,56,NAVY);for(let y=56;y<110;y++)R(g,0,y,WW,1,(y%7==0)?'#8f7d5c':'#9a8866');R(g,56,60,28,34,'#2a2018');R(g,58,62,24,30,'#8ec0ee');R(g,69,62,2,30,'#2a2018');R(g,58,76,24,1,'#2a2018');
 R(g,0,110,WW,50,'#7a5434');R(g,0,110,WW,2,'#9a7250');for(let y=118;y<WH;y+=9)R(g,0,y,WW,1,'#6b4a2e');
 // rotary phone
 R(g,10,96,34,16,INKC);R(g,11,97,32,14,'#2a2a34');R(g,11,97,32,2,'#44444e');R(g,20,99,14,10,'#c9c9d2');R(g,23,101,8,6,'#2a2a34');for(let k=0;k<8;k++)px(g,27+Math.cos(k*.8+q)*5,104+Math.sin(k*.8+q)*4,'#f4ecd8');
 R(g,8,90,38,5,INKC);R(g,9,91,36,3,'#3a3a48');R(g,8,90,8,8,'#3a3a48');R(g,38,90,8,8,'#3a3a48');
 // speaker box carrying the class
 R(g,52,92,26,20,INKC);R(g,53,93,24,18,'#8a6a4a');R(g,53,93,24,2,'#a88a66');for(let r=0;r<4;r++)for(let c=0;c<6;c++)px(g,56+c*3,98+r*3,'#3a2616');ptext(g,'CLASS',55,115,'#f4ecd8');
 for(let k=0;k<3;k++){const r=5+((q*6+k*4)%12);g.globalAlpha=1-r/17;for(let a=-.9;a<=.9;a+=.25)px(g,78+Math.cos(a)*r,101+Math.sin(a)*r,'#fffaf0');g.globalAlpha=1}
 line(g,44,104,52,104,1,'#2a2a34');return{}}
function sceneHosp(q,t){const g=wg;R(g,0,0,WW,56,NAVY);for(let y=56;y<FL;y++)R(g,0,y,WW,1,mixc('#6fb0ea','#e6f4fb',(y-56)/64));cloud(g,(30+t*2)%110-14,62,15);
 R(g,6,74,78,46,'#e8d9bf');R(g,6,74,78,2,'#f6ecd6');R(g,4,72,82,3,'#a8503c');R(g,38,62,14,12,'#e8d9bf');R(g,36,60,18,3,'#a8503c');R(g,43,64,4,8,'#d84040');R(g,41,66,8,4,'#d84040');
 for(let r=0;r<3;r++)for(let c=0;c<8;c++){const x=10+c*9+(c>3?3:0),y=79+r*11,empty=c>3&&r<2;R(g,x,y,6,7,'#5a4a3a');R(g,x+1,y+1,4,5,empty?'#2a3040':'#bfe0f2');if(!empty)px(g,x+1,y+1,'#ffffff')}
 R(g,40,104,10,16,'#5a3e28');R(g,45,104,1,16,'#3a2616');R(g,27,95,36,9,INKC);R(g,28,96,34,7,'#f4ecd8');ptext(g,'HOSPITAL',30,97,'#7a3a2c');
 if(Math.sin(t*6)>0){box2(g,48,77,37,24,AMBER)}
 R(g,0,FL,WW,40,'#7fb060');R(g,0,FL,WW,1,'#9ccf7c');for(let k=0;k<7;k++)R(g,38-k*2,FL+k*6,14+k*4,6,k%2?'#d8d2c6':'#cfc8ba');tree(g,2,FL,14,t,1);tree(g,84,FL,13,t,4);return{}}
function box2(g,x,y,w,h,c){R(g,x,y,w,1,c);R(g,x,y+h-1,w,1,c);R(g,x,y,1,h,c);R(g,x+w-1,y,1,h,c)}
function sceneLaw(q,t){const g=wg;R(g,0,0,WW,56,NAVY);for(let y=56;y<WH;y++)R(g,0,y,WW,1,'#9aa58f');R(g,0,128,WW,3,'#6a6a5a');R(g,0,131,WW,29,'#6a6658');
 const yr=1962+Math.min(11,Math.floor(Math.max(0,q-.4)*2.6)),done=yr>=1973;
 R(g,43,60,4,6,'#3a3a44');g.globalAlpha=.3;R(g,19,70,56,60,'#1a1008');g.globalAlpha=1;R(g,17,66,56,60,INKC);R(g,18,67,54,58,'#f4ecd8');R(g,18,67,54,12,done?'#2f8f5f':'#c43c3c');ptext(g,done?'A LAW':'NO LAW',done?35:33,71,'#fff6e0');
 for(let k=0;k<5;k++)R(g,22+k*10,112,7,1,'#c9c0a8');for(let k=0;k<5;k++)R(g,22+k*10,118,7,1,'#c9c0a8');
 if(!done){const f=(Math.max(0,q-.4)*2.6)%1;if(f>.5){const h=Math.round((f-.5)*2*30);R(g,18,125-h,54,1,'#c9c0a8');g.globalAlpha=.25;R(g,18,125-h,54,h,'#8a8478');g.globalAlpha=1}}
 return{yr,done}}
function sceneFace3(q,t){const g=wg;R(g,0,0,WW,56,NAVY);for(let y=56;y<WH;y++)R(g,0,y,WW,1,'#cfe0d8');R(g,0,104,WW,2,'#9ab0a8');R(g,60,62,22,28,'#5a6a66');R(g,61,63,20,26,'#bfe0f2');R(g,70,63,1,26,'#5a6a66');
 portrait(g,LOOK.ed,{blink:(t%2.6)<.12,mouth:q>.5?'smile':'flat',ex:q<.6?1:0,dy:Math.sin(t*2.2)>.4?1:0});return{}}
function sceneAsk(q,t){const g=wg;blueprintWall(g,t);const br=Math.sin(t*2.4)>.5?-1:0,sh=Math.round(Math.sin(q*6));
 personFB({hip:GY-17,feet:[[-3,0],[3,0]],sl:1,sa:[1,1],hands:[[CX-14,SHY+5+sh],[CX+13,SHY+5+sh]],mouth:'open',hy:br,nobag:false},13,0,null,'f');
 [[14,70,.9],[38,62,1.2],[62,70,1.5]].forEach(([x,y,a],k)=>{if(q<a)return;const b=Math.round(Math.sin(t*5+k));R(g,x,y+b,14,13,INKC);R(g,x+1,y+1+b,12,11,'#14265a');ptext(g,'ABC'[k],x+6,y+4+b,AMBER)});return{}}
function icoA(g,x,y){R(g,x+1,y+11,12,2,'#e4dccb');for(const c of[2,6,10])R(g,x+c,y+5,2,6,'#f4eee0');R(g,x+1,y+3,12,2,'#d2c9b6');R(g,x+5,y+1,4,2,'#d2c9b6')}
function icoB(g,x,y){R(g,x+2,y+6,10,7,'#2a2a34');R(g,x+1,y+3,12,3,'#3a3a48');R(g,x+5,y+8,4,3,'#c9c9d2')}
function icoC(g,x,y){R(g,x+1,y+2,12,12,'#e8d9bf');R(g,x,y+1,14,2,'#a8503c');R(g,x+6,y+5,2,7,'#d84040');R(g,x+4,y+7,6,2,'#d84040')}
function sceneChoice(q,t){const g=wg;blueprintWall(g,t);g.globalAlpha=.6;R(g,0,56,WW,104,'#0a1433');g.globalAlpha=1;const sel=q>=.25?Math.min(2,Math.floor((q-.25)/.9)):-1;
 for(let k=0;k<3;k++){const y=60+k*20,hot=sel==k;R(g,5,y,80,18,hot?MINT:INKC);R(g,6,y+1,78,16,hot?'#1c3a6e':'#14265a');R(g,6,y+1,78,1,'#2c4a8a');R(g,8,y+2,14,14,'#0c1c44');[icoA,icoB,icoC][k](g,8,y+2);
  if(hot){const b=Math.round(Math.sin(t*12));for(let i=0;i<4;i++)R(g,1+b,y+5+i,i<2?i+1:4-i,1,MINT)}}return{}}
const HEADS=[[0.05,1.9,"YOU GOT IN",["YOUR DREAM COLLEGE"]],[1.9,5.15,"BUT YOUR BREATHING MACHINE",["WEIGHS 800 LB"],{tc:CORAL}],
 [7.71,13.63,"MEET ED ROBERTS",["POLIO AT 14."]],[13.65,16.9,"THE STATE SAID",["CAN'T HOLD","A JOB."]],[16.92,19.76,"THE UNIVERSITY SAID",["NO DORM","CAN TAKE YOU."]],
 [19.78,20.5,"YOU ARE",["ED"]],[20.5,22.55,"THREE OPTIONS",["WHICH ONE?"],{tc:AMBER}],
 [22.57,27.55,"OPTION A",["TAKE THEM","TO COURT"],{tc:AMBER}],[27.57,32.4,"OPTION B",["STUDY FROM HOME","BY TELEPHONE"],{tc:AMBER}],[32.42,37.25,"OPTION C",["MOVE INTO THE","CAMPUS HOSPITAL"],{tc:AMBER}],
 [40.27,42.0,"PLAY OUT A",["TAKE THEM TO COURT"]],[47.73,49.5,"PLAY OUT B",["STUDY FROM HOME"]],[49.52,52.9,"HE ALREADY DID",["HIGH SCHOOL","BY TELEPHONE"],{tc:CORAL}],[52.92,54.5,"HE WANTED",["TO BE IN THE ROOM"]],
 [54.52,56.3,"PLAY OUT C",["THE CAMPUS HOSPITAL"],{tc:MINT}],[56.32,59.5,"AN EMPTY WING",["OFFERED TO ED"]],[59.52,61.6,"HE SAID YES",["ON ONE CONDITION"],{tc:AMBER}],[61.62,63.76,"TREAT IT AS",["A DORM,","NOT A WARD"],{tc:MINT}],
 [63.78,68.12,"THEY CALLED THEMSELVES",["THE ROLLING","QUADS."]],[68.14,71.5,"THE SAME AGENCY",["1976"],{tc:AMBER}],[71.52,74.5,"MADE HIM",["ITS DIRECTOR."],{tc:MINT}],
 [74.52,77.6,"RULE UNLOCKED",["CURB RAMP"],{tc:MINT}],[77.62,79.56,"MAX SLOPE",["1 IN 12"]],[79.6,END,"LEVEL 02",["CLEARED"],{tc:MINT}]];
function heart(x,y,full){og.fillStyle=full?CORAL:'#3a3668';const u=7;[[1,0,2,1],[4,0,2,1],[0,1,7,2],[1,3,5,1],[2,4,3,1],[3,5,1,1]].forEach(([a,b,w,h])=>og.fillRect(x+a*u,y+b*u,w*u,h*u))}
function badge(L,t0,t){const a=ease(seg(t,t0,t0+.18));if(a<=0)return;const p=1+.35*(1-a);og.save();og.translate(150,830);og.scale(p,p);og.globalAlpha=a;og.fillStyle=INKC;rrect(og,-78,-78,156,156,24);og.fill();og.fillStyle=AMBER;rrect(og,-66,-66,132,132,18);og.fill();mdraw(L,0,6,110,INKC,'center',false,'',0,a);og.restore()}
function hud(t){const DONE=79.56,done=t>=DONE,pr=cl01(t/DONE),y=566,s=84,gap=18,x0=250,a=ease(seg(t,5.15,5.5));if(a<=0)return;og.save();og.globalAlpha=a;
 mdraw("LV 2",60,y+s/2+2,40,MINT,'left',false,'',0,a);
 for(let i=0;i<5;i++){const x=x0+i*(s+gap),ok=i==0||(i==1&&done),cur=i==1&&!done;og.globalAlpha=a;og.fillStyle=ok?'#173a2c':'#1b1838';rrect(og,x,y,s,s,12);og.fill();
  if(cur){og.save();rrect(og,x,y,s,s,12);og.clip();og.fillStyle='#2a4a7a';og.fillRect(x,y+s*(1-pr),s,s*pr);og.restore()}
  const nxt=i==2&&t>81.75;og.lineWidth=4;og.strokeStyle=ok?MINT:cur?CORAL:(nxt&&Math.sin(t*10)>0?AMBER:'#3a3668');rrect(og,x,y,s,s,12);og.stroke();
  if(ok){og.strokeStyle=MINT;og.lineWidth=9;og.lineCap='round';og.beginPath();og.moveTo(x+22,y+44);og.lineTo(x+37,y+59);og.lineTo(x+63,y+27);og.stroke()}
  else mdraw(cur?"02":"?",x+s/2,y+s/2+2,cur?34:38,cur?CREAM:(nxt?AMBER:'#5a568a'),'center',false,'',0,a)}
 const lives=t<44.3?3:t<52.0?2:1;for(let i=0;i<3;i++)heart(800+i*76,y+20,i<lives);og.restore()}
function frameAt(t){
 QA.chars=[];QA.solids=[];og.imageSmoothingEnabled=false;og.clearRect(0,0,1080,1920);
 const sg=SEG.find(s=>t>=s[0]&&t<s[1])||SEG[SEG.length-1],id=sg[4],o=sg[2]+(t-sg[0])*(sg[3]-sg[2])/(sg[1]-sg[0]);QA.shot=sg[5];let sh=0,inf={};
 if(id=='fit'){sceneFit(o,t);sh=shake(t,3.0)}else if(id=='shrug')sceneShrug(o,t);else if(id=='lung'||id=='B')sceneLung(o);else if(id=='face1'||id=='face1b')sceneFace1(o+(id=='face1b'?1.3:0),t);
 else if(id=='file'){sceneV(o);sh=shake(t,15.4)}else if(id=='dean')sceneDean(o);else if(id=='ask')sceneAsk(o,t);
 else if(id=='pA'||id=='A1')sceneCourt(o,t);else if(id=='pB'||id=='B1')sceneTel(o,t);else if(id=='pC'||id=='C1')sceneHosp(o,t);else if(id=='choice')sceneChoice(o,t);
 else if(id=='A'){inf=sceneLaw(o,t);sh=shake(t,44.3)}
 else if(id=='wing')sceneWing(o);else if(id=='face3')sceneFace3(o,t);else if(id=='quads')sceneQuads(o);else if(id=='quadsF')sceneQuadsF(o,t);else if(id=='director')sceneDirector(o);else if(id=='face2')sceneFace2(o,t);
 else if(id=='today')sceneToday6(o);else if(id=='slope')sceneSlope(o,t);else sceneWin(o);
 if(id=='B')sh=shake(t,52.0);
 og.drawImage(wc,0,0,WW,WH,sh,0,1080,1920);
 lit(()=>{
  if(id=='fit')glow(540,1200,700,SUN,.14);
  else if(id=='shrug'||id=='ask'||id=='choice'||id=='slope')glow(540,1300,700,COOL,.14);
  else if(id=='lung'){glow(60,960,420,WARM,.34);glow(840,1500,520,COOL,.16)}
  else if(id=='face1'||id=='face1b'){glow(180,900,560,WARM,.28);grade('#4a4470',.3,'multiply')}
  else if(id=='file')glow(540,1100,800,WARM,.22);
  else if(id=='dean'||id=='quads'||id=='quadsF'||id=='today'||id=='pA'||id=='A1'||id=='pC'||id=='C1')glow(900,760,520,SUN,.22);
  else if(id=='pB'||id=='B1')glow(820,820,520,SUN,.26);
  else if(id=='B'){grade('#10122a',.55,'multiply');glow(60,960,300,WARM,.3)}
  else if(id=='A')glow(540,1100,700,WARM,.16);
  else if(id=='wing'||id=='face3')glow(840,820,520,SUN,.2);
  else if(id=='director'||id=='face2')glow(820,860,560,WARM,.26);
  else glow(70*12,66*12,520,SUN,.45)});
 const v=og.createLinearGradient(0,0,0,1920);v.addColorStop(0,'rgba(0,0,0,.22)');v.addColorStop(.3,'rgba(0,0,0,0)');v.addColorStop(.8,'rgba(0,0,0,0)');v.addColorStop(1,'rgba(0,0,0,.35)');og.fillStyle=v;og.fillRect(0,0,1080,1920);
 og.globalAlpha=.6;og.fillStyle='#0f0d22';og.fillRect(0,110,1080,562);og.globalAlpha=1;
 const h=HEADS.find(h=>t>=h[0]&&t<h[1]);
 if(id=='shrug'){const yr=Math.round(lerp(2026,1962,ease(seg(t,6.1,7.2))));header(t<6.1?"LEVEL 02":"BERKELEY",[t<6.1?"MOVE IN":String(yr)],(t-5.15)/.2,{tc:t>7.2||t<6.1?AMBER:CREAM})}
 else if(id=='choice'){const q=t-37.25,n=3-Math.min(2,Math.floor(Math.max(0,q-.25)/.9)),p=1+.25*(1-ease(seg(((Math.max(0,q-.25))%.9),0,.2)));header("LOCK IT IN",[],1);og.save();og.translate(540,330);og.scale(p,p);mdraw(String(n),0,0,220,AMBER,'center',true,INKC,20,1);og.restore()}
 else if(id=='A'){header(inf.done?"THE FIRST FEDERAL LAW":"NO LAW TO SUE UNDER",[String(inf.yr)],(t-42.0)/.2,{tc:inf.done?MINT:CORAL})}
 else if(h)header(h[2],h[3],(t-h[0])/.2,h[4]);
 hud(t);
 if(id=='pA')badge("A",23.2,t);if(id=='pB')badge("B",28.2,t);if(id=='pC')badge("C",33.1,t);
 if(id=='A1'||id=='A')badge("A",40.3,t);if(id=='B1'||id=='B'||id=='face1b')badge("B",47.76,t);if(id=='C1'||id=='wing'||id=='face3')badge("C",54.55,t);
 if(id=='fit'&&t>=3.0)stamp("WON'T FIT",'#e0473c',400,880,3.0,t,-.08,64);
 if(id=='file'){mdraw("REHABILITATION CASE FILE",540,980,26,'#3a3a4a','center',false,'',0,1);if(t>=15.4)stamp("TOO DISABLED",'#e0473c',540,1330,15.4,t,-.1,60)}
 if(id=='choice'){const L=[["A","TAKE THEM TO COURT"],["B","STUDY BY TELEPHONE"],["C","THE CAMPUS HOSPITAL"]];
  L.forEach(([a,s],k)=>{const y=(69+k*20)*12;mdraw(a,26.5*12,y+2,56,AMBER,'center',true,INKC,10,1);mdraw(s,31*12,y+2,fit(s,40,600),CREAM,'left',false,'',0,1)})}
 if(id=='A'){mdraw(String(inf.yr),540,1215,150,'#2a2846','center',false,'',0,1);if(t>=44.3)stamp("A FAILS",'#e0473c',540,1420,44.3,t,-.07,64)}
 if(id=='B'&&t>=52.0)stamp("B FAILS",'#e0473c',640,860,52.0,t,-.07,64);
 if(id=='wing'&&t>=62.6)stamp("C WORKED",'#2fbf8f',640,1290,62.6,t,-.07,60);
 if(id=='win'){const xp=Math.round(100*ease(seg(t,79.8,80.5)));mdraw("+"+xp+" XP",540,800,70,AMBER,'center',true,INKC,14,1);
  if(t>80.78&&t<81.75)tag("COMMENT A, B OR C",540,1400,AMBER,ease(seg(t,80.78,80.93)));if(t>=81.75)tag("FOLLOW FOR LEVEL 03",540,1400,MINT,ease(seg(t,81.75,81.92)))}
 subtitle(t,false);for(const c of CUTS)wipe(t,c,.12);
}
window.frame=i=>frameAt(i/30);
Promise.all([document.fonts.load('700 40px Silk'),document.fonts.load('400 40px PS2P')]).then(()=>{window.READY=true});
