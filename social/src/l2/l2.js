// ===== Level 02 : Ed Roberts — "Where do you live?" =====
const END=56.5;
const SUBS=[[0.15,1.75,"Level two. You got into Berkeley."],[2.01,4.4,"But your iron lung won't fit in a dorm room."],[4.68,5.45,"Where do you live?"],
[5.72,6.8,"This was a real level."],[7.09,8.9,"California, 1962."],
[9.18,11.05,"Ed Roberts got polio at fourteen."],[11.46,13.75,"It paralyzed him from the neck down,"],[13.82,14.85,"and he slept in an iron lung."],
[15.14,17.75,"The state called him too disabled to hold a job."],[18.11,20.25,"And Berkeley said its dorms couldn't take him."],
[20.55,21.5,"So, pick your fix."],[21.77,22.8,"A: study from home."],[23.06,24.6,"B: wait for a bigger dorm."],[24.6,26.45,"C: move into the campus hospital."],
[29.04,29.8,"A fails."],[29.85,31.4,"You can't get to class from your bedroom."],[31.68,32.5,"B fails."],[32.55,33.7,"Nobody was building one."],
[34.0,34.52,"C worked."],[34.61,37.05,"Ed moved into an empty hospital wing."],[37.52,39.4,"More disabled students followed,"],[39.4,41.28,"and called themselves the Rolling Quads."],
[41.58,42.9,"In 1976,"],[43.03,45.3,"the state agency that said he couldn't hold a job"],[45.3,47.35,"made him its director."],
[47.35,48.55,"Today, the A.D.A. says"],[48.94,52.1,"a curb ramp can rise one inch for every twelve, at most."],
[52.4,53.18,"Level cleared."],[53.45,54.34,"Comment what you picked,"],[54.38,55.83,"and follow for level three."]];
const SEG=[[0,5.72,0,5.72,'fit','plan'],[5.72,9.18,0,3.46,'shrug','front'],[9.18,11.46,3.97,5.9,'lung','side'],[11.46,13.82,0,2.36,'face1','closeup'],[13.82,15.14,5.9,7.2,'lung','side'],
[15.14,18.11,0,2.97,'file','detail'],[18.11,20.55,7.85,11.6,'dean','side'],[20.55,29.04,0,8.49,'choice','menu'],[29.04,31.68,4.2,6.84,'A','side'],[31.68,34.0,0,2.32,'B','detail'],
[34.0,37.52,14.92,19.6,'wing','side'],[37.52,39.5,19.6,21.8,'quads','side'],[39.5,41.58,0,2.08,'quadsF','front'],[41.58,44.6,30.06,33.08,'director','side'],[44.6,47.35,0,2.75,'face2','closeup'],
[47.35,50.8,35.47,40.53,'today','side'],[50.8,52.4,0,1.6,'slope','diagram'],[52.4,END,36.36,40.46,'win','front']];
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
 [['a1',-13,0],['ed',13,1],['a2',39,2]].forEach(([l,ox,k])=>{const wv=k==1?Math.round(Math.sin(q*8)*2):0,hip=GY-12,br=Math.sin(t*2.2+k)>.6?-1:0;
  const P={hip,feet:[[-3,0],[3,0]],sl:1,sa:[1,1],hands:k==1?[[CX-10,hip-3],[CX+12,hip-22+wv]]:[[CX-10,hip-3],[CX+9,hip-3]],mouth:k==1?'open':'smile',hy:br,back:chairF,okOverlap:true};
  personFB(P,ox,0,Object.assign({},LOOK[l],{id:'q'+l}),'f')});return{}}
function sceneSlope(q,t){const g=wg;blueprintWall(g,t);g.globalAlpha=.55;R(g,0,56,WW,104,'#0a1433');g.globalAlpha=1;
 const x0=9,y0=112,u=6;for(let i=0;i<12;i++){R(g,x0+i*u,y0,u,u,i%2?'#3f8fb0':'#5fb0d0');R(g,x0+i*u,y0,1,u,'#0a1433')}
 line(g,x0,y0-1,x0+72,y0-7,1,CREAM);R(g,x0+72,y0-7,u,u+1,MINT);ptext(g,'12',x0+32,y0+9,'#cfe2ff');ptext(g,'1',x0+81,y0-6,MINT);
 const ox=lerp(-30,22,seg(q,0,1.6)),wx=ox+37,yy=Math.max(0,Math.min(6,(wx-x0)/12))+ (FL-(y0-1));drawKitY(roll(t,ox+40,true),ox,yy);return{}}
function icoA(g,x,y){for(let k=0;k<6;k++)R(g,x+6-k,y+1+k,2*k+1,1,'#c0503f');R(g,x+2,y+7,10,7,'#e9d9a6');R(g,x+5,y+9,3,5,'#6b4e36')}
function icoB(g,x,y){R(g,x+1,y+3,11,11,'#8a8f99');for(let r=0;r<3;r++)for(let c2=0;c2<3;c2++)R(g,x+2+c2*3,y+5+r*3,2,2,'#bfe0f2');R(g,x+4,y,6,3,'#f3c969');px(g,x+6,y+1,INKC)}
function icoC(g,x,y){R(g,x+1,y+2,12,12,'#e8d9bf');R(g,x,y+1,14,2,'#a8503c');R(g,x+6,y+5,2,7,'#d84040');R(g,x+4,y+7,6,2,'#d84040')}
function sceneChoice(q,t){const g=wg;blueprintWall(g,t);g.globalAlpha=.6;R(g,0,56,WW,104,'#0a1433');g.globalAlpha=1;
 const at=[1.22,2.51,4.05],sel=q>=6.2?Math.min(2,Math.floor((q-6.2)/.72)):-1;
 for(let k=0;k<3;k++){const y=60+k*20,on=q>=at[k];
  if(!on){g.globalAlpha=.5;for(let x=6;x<84;x+=4){px(g,x,y,'#9fc3ff');px(g,x,y+17,'#9fc3ff')}g.globalAlpha=1;continue}
  const hot=sel==k;R(g,5,y,80,18,hot?MINT:INKC);R(g,6,y+1,78,16,hot?'#1c3a6e':'#14265a');R(g,6,y+1,78,1,'#2c4a8a');R(g,8,y+2,14,14,'#0c1c44');[icoA,icoB,icoC][k](g,8,y+2);
  if(hot){const b=Math.round(Math.sin(t*12));for(let i=0;i<4;i++)R(g,1+b,y+5+i,i<2?i+1:4-i,1,MINT)}}
 return{}}
const HEADS=[[0.05,2.0,"LEVEL 02",["MOVE IN"]],[2.0,5.72,"LEVEL 02",["IT WON'T FIT."],{tc:CORAL}],
 [9.2,15.14,"MEET ED ROBERTS",["POLIO AT 14."]],[15.16,18.11,"THE STATE SAID",["CAN'T HOLD","A JOB."]],[18.13,20.55,"BERKELEY SAID",["NO ROOM."]],
 [29.06,31.68,"ATTEMPT A",["STUDY FROM HOME"]],[31.7,34.0,"ATTEMPT B",["WAIT FOR A DORM"]],
 [34.02,37.52,"ATTEMPT C",["A HOSPITAL WING"],{tc:MINT}],[37.54,41.58,"THEY CALLED THEMSELVES",["THE ROLLING","QUADS."]],
 [41.6,44.6,"THE SAME AGENCY",["1976"],{tc:AMBER}],[44.62,47.35,"MADE HIM",["ITS DIRECTOR."],{tc:MINT}],
 [47.37,50.8,"RULE UNLOCKED",["CURB RAMP"],{tc:MINT}],[50.82,52.4,"MAX SLOPE",["1 IN 12"]],[52.44,END,"LEVEL 02",["CLEARED"],{tc:MINT}]];
function heart(x,y,full){og.fillStyle=full?CORAL:'#3a3668';const u=7;[[1,0,2,1],[4,0,2,1],[0,1,7,2],[1,3,5,1],[2,4,3,1],[3,5,1,1]].forEach(([a,b,w,h])=>og.fillRect(x+a*u,y+b*u,w*u,h*u))}
function hud(t){const DONE=52.4,done=t>=DONE,pr=cl01(t/DONE),y=566,s=84,gap=18,x0=250;
 mdraw("LV 2",60,y+s/2+2,40,MINT,'left',false,'',0,1);
 for(let i=0;i<5;i++){const x=x0+i*(s+gap),ok=i==0||(i==1&&done),cur=i==1&&!done;og.globalAlpha=1;og.fillStyle=ok?'#173a2c':'#1b1838';rrect(og,x,y,s,s,12);og.fill();
  if(cur){og.save();rrect(og,x,y,s,s,12);og.clip();og.fillStyle='#2a4a7a';og.fillRect(x,y+s*(1-pr),s,s*pr);og.restore()}
  const nxt=i==2&&t>54.38;og.lineWidth=4;og.strokeStyle=ok?MINT:cur?CORAL:(nxt&&Math.sin(t*10)>0?AMBER:'#3a3668');rrect(og,x,y,s,s,12);og.stroke();
  if(ok){og.strokeStyle=MINT;og.lineWidth=9;og.lineCap='round';og.beginPath();og.moveTo(x+22,y+44);og.lineTo(x+37,y+59);og.lineTo(x+63,y+27);og.stroke()}
  else mdraw(cur?"02":"?",x+s/2,y+s/2+2,cur?34:38,cur?CREAM:(nxt?AMBER:'#5a568a'),'center',false,'',0,1)}
 const lives=t<29.9?3:t<32.55?2:1;for(let i=0;i<3;i++)heart(800+i*76,y+20,i<lives)}
function frameAt(t){
 QA.chars=[];QA.solids=[];og.imageSmoothingEnabled=false;og.clearRect(0,0,1080,1920);
 const sg=SEG.find(s=>t>=s[0]&&t<s[1])||SEG[SEG.length-1],id=sg[4],o=sg[2]+(t-sg[0])*(sg[3]-sg[2])/(sg[1]-sg[0]);QA.shot=sg[5];let sh=0,inf={};
 if(id=='fit'){sceneFit(o,t);sh=shake(t,3.0)}else if(id=='shrug')sceneShrug(o,t);else if(id=='lung'||id=='A')sceneLung(o);else if(id=='face1')sceneFace1(o,t);
 else if(id=='file'){sceneV(o);sh=shake(t,16.0)}else if(id=='dean')sceneDean(o);else if(id=='choice')sceneChoice(o,t);else if(id=='B'){inf=sceneCal(o,t);sh=shake(t,32.6)}
 else if(id=='wing')sceneWing(o);else if(id=='quads')sceneQuads(o);else if(id=='quadsF')sceneQuadsF(o,t);else if(id=='director')sceneDirector(o);else if(id=='face2')sceneFace2(o,t);
 else if(id=='today')sceneToday6(o);else if(id=='slope')sceneSlope(o,t);else sceneWin(o);
 if(id=='A')sh=shake(t,29.9);
 og.drawImage(wc,0,0,WW,WH,sh,0,1080,1920);
 lit(()=>{
  if(id=='fit')glow(540,1200,700,SUN,.14);
  else if(id=='shrug'){glow(540,1500,700,COOL,.12);grade('#c8a070',.3*ease(seg(t,7.09,8.2)),'multiply')}
  else if(id=='lung'){glow(60,960,420,WARM,.34);glow(840,1500,520,COOL,.16)}
  else if(id=='face1'){glow(180,900,560,WARM,.28);grade('#4a4470',.3,'multiply')}
  else if(id=='file'){glow(540,1100,800,WARM,.22)}
  else if(id=='dean'||id=='quads'||id=='quadsF'||id=='today'){glow(900,760,520,SUN,.22)}
  else if(id=='choice'||id=='slope')glow(540,1000,700,COOL,.16);
  else if(id=='A'){grade('#10122a',.6,'multiply');glow(60,960,300,WARM,.3)}
  else if(id=='B')glow(540,1100,700,WARM,.16);
  else if(id=='wing')glow(840,820,520,SUN,.2);
  else if(id=='director'||id=='face2'){glow(820,860,560,WARM,.26)}
  else glow(70*12,66*12,520,SUN,.45)});
 const v=og.createLinearGradient(0,0,0,1920);v.addColorStop(0,'rgba(0,0,0,.22)');v.addColorStop(.3,'rgba(0,0,0,0)');v.addColorStop(.8,'rgba(0,0,0,0)');v.addColorStop(1,'rgba(0,0,0,.35)');og.fillStyle=v;og.fillRect(0,0,1080,1920);
 og.globalAlpha=.6;og.fillStyle='#0f0d22';og.fillRect(0,110,1080,562);og.globalAlpha=1;
 const h=HEADS.find(h=>t>=h[0]&&t<h[1]);
 if(id=='shrug'){const yr=Math.round(lerp(2026,1962,ease(seg(t,7.09,8.2))));header(t<7.09?"THIS WAS A":"REWIND TO",[t<7.09?"REAL LEVEL":String(yr)],(t-5.72)/.2,{tc:t>8.2||t<7.09?AMBER:CREAM})}
 else if(id=='choice'){const q=t-20.55;if(q<6.2)header("YOUR TURN",["PICK YOUR FIX"],q/.2);else{const n=3-Math.min(2,Math.floor((q-6.2)/.72)),p=1+.25*(1-ease(seg(((q-6.2)%.72),0,.2)));header("PICK ONE",[],1);og.save();og.translate(540,330);og.scale(p,p);mdraw(String(n),0,0,220,AMBER,'center',true,INKC,20,1);og.restore()}}
 else if(h)header(h[2],h[3],(t-h[0])/.2,h[4]);
 hud(t);
 if(id=='fit'&&t>=3.0)stamp("WON'T FIT",'#e0473c',400,880,3.0,t,-.08,64);
 if(id=='file'){mdraw("REHABILITATION CASE FILE",540,980,26,'#3a3a4a','center',false,'',0,1);if(t>=16.0)stamp("TOO DISABLED",'#e0473c',540,1330,16.0,t,-.1,60)}
 if(id=='choice'){const q=t-20.55,at=[1.22,2.51,4.05],L=[["A","STUDY FROM HOME"],["B","WAIT FOR A DORM"],["C","THE CAMPUS HOSPITAL"]];
  L.forEach(([a,s],k)=>{if(q<at[k])return;const al=ease(seg(q,at[k],at[k]+.15)),y=(69+k*20)*12;mdraw(a,26.5*12,y+2,56,AMBER,'center',true,INKC,10,al);mdraw(s,31*12,y+2,fit(s,40,600),CREAM,'left',false,'',0,al)})}
 if(id=='A'&&t>=29.9)stamp("ATTEMPT A FAILED",'#e0473c',540,900,29.9,t,-.07,58);
 if(id=='B'){mdraw(String(inf.yr||1962),540,1210,150,'#2a2846','center',false,'',0,1);if(t>=32.6)stamp("ATTEMPT B FAILED",'#e0473c',540,1440,32.6,t,-.07,52)}
 if(id=='win'){const xp=Math.round(100*ease(seg(t,52.6,53.3)));mdraw("+"+xp+" XP",540,800,70,AMBER,'center',true,INKC,14,1);
  if(t>53.45&&t<54.38)tag("COMMENT A, B OR C",540,1400,AMBER,ease(seg(t,53.45,53.6)));if(t>=54.38)tag("FOLLOW FOR LEVEL 03",540,1400,MINT,ease(seg(t,54.38,54.55)))}
 subtitle(t,false);for(const c of CUTS)wipe(t,c,.12);
}
window.frame=i=>frameAt(i/30);
Promise.all([document.fonts.load('700 40px Silk'),document.fonts.load('400 40px PS2P')]).then(()=>{window.READY=true});
