// ===== Level 01 (rebuilt) : the panic bar — three plausible options =====
const END=69.4;
const SUBS=[[0.12,2.06,"Hundreds of people are pushing on this door."],[2.35,3.09,"It won't open."],[3.49,4.88,"How do you fix that for good?"],
[5.14,5.81,"Level one."],[6.0,7.47,"Chicago, 1903."],
[7.73,9.66,"Carl Prinzler sold door hardware."],[10.16,12.91,"He was in Chicago the day the Iroquois Theatre burned."],
[13.17,14.11,"The exits failed,"],[14.32,16.18,"and 602 people died."],
[16.44,17.49,"Carl couldn't let it go."],[17.85,18.5,"You're Carl."],[18.5,19.2,"Three options."],[19.2,20.22,"Which one would you pick?"],
[20.74,21.66,"Option A."],[22.13,24.18,"Unlock every exit before each show."],
[24.75,25.73,"Option B."],[26.2,28.25,"Put an usher at every exit, to open it."],
[28.82,29.8,"Option C."],[30.27,31.5,"Put a bar across the door."],[31.88,33.62,"Push the bar, and the door opens."],
[36.94,38.56,"Option A sounds obvious."],[39.0,40.74,"But some of those doors opened inward."],[41.21,42.65,"With a crowd pressed against it,"],[42.84,44.81,"even an unlocked door won't open."],
[45.07,46.33,"Option B sounds safe."],[46.81,48.05,"But the theatre had ushers."],[48.45,49.8,"They had never had a fire drill,"],[49.8,51.37,"and some didn't know the exits."],
[51.63,53.1,"Option C is what Carl built,"],[53.1,54.52,"with his neighbor, an architect."],[55.02,56.27,"It took them five years."],[56.73,57.9,"The crowd pushes the bar,"],[57.9,59.25,"and the door swings out."],
[59.51,61.6,"Today, codes require it on the exits"],[61.6,62.99,"of theaters and schools"],[63.31,64.9,"that hold 50 people or more."],
[65.16,65.89,"Level cleared."],[66.24,67.2,"Comment what you picked,"],[67.2,68.64,"and follow for level two."]];
const SEG=[[0,5.0,0,4.85,'mission','back'],[5.0,7.59,4.85,7.38,'mission','front'],[7.59,10.0,7.38,9.87,'carl','closeup'],[10.0,13.03,12.9,14.42,'street','side'],
[13.03,14.2,14.42,16.15,'fire','elevation'],[14.2,16.3,16.15,19.26,'locked','detail'],[16.3,17.7,19.26,20.55,'think','closeup'],[17.7,20.47,0,2.77,'ask','front'],
[20.47,24.45,0,3.98,'pA','elevation'],[24.45,28.52,0,4.07,'pB','side'],[28.52,33.87,26.39,28.08,'pC','detail'],[33.87,36.87,0,3.0,'choice','menu'],
[36.87,38.8,3.98,5.9,'A1','elevation'],[38.8,45.0,0,6.2,'A','plan'],[45.0,46.6,4.07,5.67,'B1','side'],[46.6,51.5,0,4.9,'B','plan'],
[51.5,54.8,23.61,26.39,'two','side'],[54.8,56.5,26.39,28.08,'bar','detail'],[56.5,59.37,28.08,29.85,'lean','back'],
[59.37,63.1,29.85,34.3,'school','side'],[63.1,65.02,34.3,36.36,'count','plan'],[65.02,END,36.36,40.6,'win','front']];
const CUTS=SEG.slice(1).map(s=>s[0]);
function keyBox(g,x,y){R(g,x-1,y-1,12,14,INKC);R(g,x,y,10,12,'#cfe6f2');R(g,x,y,10,2,'#eaf6fb');R(g,x+3,y+3,4,4,BRASS);R(g,x+4,y+4,2,2,'#cfe6f2');R(g,x+4,y+7,2,4,BRASS);px(g,x+6,y+9,BRASS)}
function guardIcon(g,x,y){R(g,x+3,y,6,2,'#2a3a6a');R(g,x+2,y+2,8,1,'#2a3a6a');R(g,x+3,y+3,6,4,'#e9c3a3');px(g,x+7,y+4,INKC);R(g,x+2,y+7,8,6,'#3f5fa8');px(g,x+4,y+9,BRASS);R(g,x+3,y+13,2,1,'#2a2a34');R(g,x+7,y+13,2,1,'#2a2a34')}
function doorIcon(g,x,y){R(g,x+1,y,10,14,'#4a3220');R(g,x+2,y+1,8,13,'#7a5434');R(g,x+2,y+7,8,2,BRASS);R(g,x+2,y+7,8,1,'#f4dc8a')}
function sceneA(q,t){const g=wg;blueprintWall(g,t);
 R(g,27,55,36,65,'#0c1c44');R(g,27,55,36,1,'#cfe2ff');R(g,27,55,1,65,'#cfe2ff');R(g,62,55,1,65,'#cfe2ff');
 bigDoor(g,30,0);padlock(g,41,62,1);keyBox(g,70,86);
 const s=Math.sin(q*7),ox=lerp(13,-6,ease(seg(q,0,1.5)));
 personFB({hip:GY-17,feet:[[-3-(s>0?1:0),s>0?1:0],[3,s>0?0:1]],sl:1,sa:[1,1],hands:[[CX-13,SHY+1+Math.round(s*3)],[CX+9,SHY+4-Math.round(s*3)]],hy:s>0?0:-1},ox,0,null,'b');
 for(let k=0;k<12;k++){const age=((t*.25+k/12)%1);g.globalAlpha=.35*(1-age);R(g,((k*31)%96)-6+age*10,70+((k*17)%44)-age*8,14,6,'#6a6680');g.globalAlpha=1}
 return{kx:ox+CX}}
function sceneB(q,t){const g=wg;R(g,0,0,WW,56,NAVY);
 R(g,0,56,WW,104,'#7fb060');for(let k=0;k<20;k++)px(g,(k*29)%WW,57+(k*7)%100,'#6a9a52');R(g,36,56,18,18,'#d8d2c6');
 R(g,6,72,78,82,INKC);R(g,9,75,72,76,'#e9e3d4');
 R(g,24,140,42,9,'#8a6640');ptext(g,'STAGE',35,142,'#4a3220');
 R(g,37,72,16,3,'#e9e3d4');line(g,37,72,37,65,2,'#3f6f9a');line(g,53,72,53,65,2,'#3f6f9a'); // top exit: held open
 R(g,6,104,3,12,'#3f6f9a');R(g,81,104,3,12,'#3f6f9a'); // side exits: shut
 const cols=[MINT,AMBER,'#ff9d8a','#9fc3ff'];
 for(let k=0;k<54;k++){const grp=k%3,i=(k/3|0),hx=14+((k*13)%62),hy=88+((k*7)%44);const v=cl01((q-.1-(i%6)*.05)/1.1);let x,y;
  if(grp==0){const v2=cl01(v*1.2);x=lerp(hx,43+(i%3)*2,Math.min(1,v2/.6));y=lerp(hy,80,Math.min(1,v2/.6));if(v2>.6){y=lerp(80,58+(i%4)*2,(v2-.6)/.4);x+=((i%5)-2)*3*(v2-.6)/.4}}
  else{const side=grp==1?-1:1,row=i%6,col=(i/6|0);const tx=(side<0?12:78)-side*col*-0+ (side<0?col*4:-col*4),ty=100+row*4;x=lerp(hx,tx,v);y=lerp(hy,ty,v);if(v>=1){x+=Math.round(Math.sin(t*14+k))*.6}}
  R(g,x-1,y-1,3,3,INKC);px(g,x,y,cols[k%4]);px(g,x,y-1,cols[k%4]);px(g,x-1,y,cols[k%4]);px(g,x+1,y,cols[k%4]);px(g,x,y+1,cols[k%4])}
 // the one guard, at the one door he can hold
 R(g,33,76,5,5,INKC);R(g,34,77,3,3,'#3f5fa8');px(g,35,78,BRASS);
 if(q>.9){const a=ease(seg(q,.9,1.1));g.globalAlpha=a;for(const cx of[3,86]){line(g,cx-3,106,cx+3,114,2,CORAL);line(g,cx+3,106,cx-3,114,2,CORAL)}g.globalAlpha=1}
 return{}}
LOOK.ush={id:'ush',skin:'#e9c3a3',skinD:'#c99d7e',hair:'#3a2a20',top:'#a8323c',topL:'#c8525a',pants:'#2a2a34',shoe:'#121016'};
function sceneUnlock(q,t){const g=wg;blueprintWall(g,t);
 R(g,27,55,36,65,'#0c1c44');R(g,27,55,36,1,'#cfe2ff');R(g,27,55,1,65,'#cfe2ff');R(g,62,55,1,65,'#cfe2ff');bigDoor(g,30,0);
 R(g,34,57,22,9,INKC);R(g,35,58,20,7,Math.sin(t*4)>-.4?'#2fbf8f':'#1f8f6a');ptext(g,'EXIT',38,59,'#fffaf0');
 const u=ease(seg(q,1.5,2.1)),kx=Math.round(lerp(72,49,ease(seg(q,.5,1.3))));
 if(u<1){g.save();g.translate(0,Math.round(u*40));padlock(g,41,76,1-u*.6);g.restore()}
 if(q<2.3){R(g,kx,80,7,2,BRASS);R(g,kx+7,78,5,6,BRASS);R(g,kx+9,80,2,2,'#0c1c44');px(g,kx+1,82,BRASS);px(g,kx+3,82,BRASS)}
 if(q>2.1){const a=ease(seg(q,2.1,2.5));g.globalAlpha=a;line(g,38,96,43,102,2,MINT);line(g,43,102,54,88,2,MINT);g.globalAlpha=1}
 return{}}
function sceneUsher(q,t){const g=wg;R(g,0,0,WW,56,NAVY);R(g,0,56,WW,64,'#7a2a34');for(let x=0;x<WW;x+=9)R(g,x,56,1,64,'#6a222c');R(g,0,56,WW,2,'#d9b24a');R(g,0,100,WW,2,'#d9b24a');R(g,0,102,WW,18,'#5a1e26');
 R(g,8,62,14,20,'#d9b24a');R(g,10,64,10,16,'#3a2a20');R(g,13,67,4,5,'#e9c3a3');
 R(g,38,60,22,9,INKC);R(g,39,61,20,7,'#2fbf8f');ptext(g,'EXIT',42,62,'#fffaf0');
 pdoor(g,66,0,{knob:1,wall:'#5a1e26',wallL:'#7a2a34'});
 for(let y=FL;y<WH;y++)R(g,0,y,WW,1,(y-FL)%7==0?'#4a1a22':'#6a2630');for(let x=-40;x<WW+40;x+=13)line(g,45+(x-45)*.6,FL,45+(x-45)*1.7,WH,1,'#4a1a22');
 const br=Math.sin(t*2.5)>.4?-1:0,jg=Math.round(Math.sin(q*5));
 const P={legs:stand2,arms:[{ua:0,fa:0},{ua:8,fa:16}],armRel:[[7,-2+jg],null],lean:1,face:q>4.2?'o':'n',mouth:q>4.2?'flat':'smile',look:1,dy:br};
 person(P,10,0,LOOK.ush,(gg,i)=>{R(gg,i.hx-1,i.hy-3,i.hw+2,4,'#a8323c');R(gg,i.hx+i.hw-3,i.hy,5,1,'#2a2a34');R(gg,i.hx-1,i.hy,i.hw+2,1,'#d9b24a');const h=i.h[0];R(gg,h[0]+1,h[1]-1,5,1,BRASS);R(gg,h[0]+5,h[1]-2,3,3,BRASS);R(gg,h[0]-1,h[1]-1,3,3,LOOK.ush.skin)},false);
 return{}}
function sceneInward(q,t){const g=wg;R(g,0,0,WW,56,NAVY);R(g,0,56,WW,26,'#8d939c');for(let x=3;x<WW;x+=11)R(g,x,68,6,1,'#cfd3da');
 R(g,0,82,WW,78,'#e9e3d4');R(g,0,82,WW,4,INKC);R(g,37,82,17,4,'#e9e3d4');R(g,0,86,3,74,INKC);R(g,87,86,3,74,INKC);
 const press=cl01((q-.2)/1.2),j=q>1.4?Math.sin(t*26)*1.2:0,ang=(8+j)*Math.PI/180*press;
 // swing path into the room
 g.globalAlpha=.8;for(let a=0;a<=90;a+=7){px(g,37+Math.cos(a*Math.PI/180)*17,86+Math.sin(a*Math.PI/180)*17,CORAL)}g.globalAlpha=1;
 const cols=[MINT,AMBER,'#ff9d8a','#9fc3ff'];
 for(let k=0;k<70;k++){const hx=8+((k*13)%74),hy=96+((k*7)%58),row=Math.floor(k/9),col=k%9;const tx=27+col*4.4+(row%2)*2,ty=91+row*4.2;const x=lerp(hx,tx,press)+(press>=1?Math.round(Math.sin(t*13+k))*.6:0),y=lerp(hy,ty,press);
  R(g,x-1,y-1,3,3,INKC);px(g,x,y,cols[k%4]);px(g,x,y-1,cols[k%4]);px(g,x-1,y,cols[k%4]);px(g,x+1,y,cols[k%4]);px(g,x,y+1,cols[k%4])}
 line(g,37,86,37+Math.cos(ang)*17,86+Math.sin(ang)*17,3,'#7a5434');R(g,36,85,3,3,BRASS);
 ptext(g,'STREET',33,60,'#3a3f4c');
 if(q>1.6){const a=ease(seg(q,1.6,1.9));g.globalAlpha=a;ptext(g,'OPENS IN',57,74,'#a8323c');g.globalAlpha=1}
 return{}}
function sceneAsk(q,t){const g=wg;blueprintWall(g,t);const br=Math.sin(t*2.4)>.5?-1:0,sh=Math.round(Math.sin(q*6));
 personFB({hip:GY-17,feet:[[-3,0],[3,0]],sl:1,sa:[1,1],hands:[[CX-14,SHY+5+sh],[CX+13,SHY+5+sh]],mouth:'open',hy:br,nobag:false},13,0,null,'f');
 [[14,70,.5],[38,62,.8],[62,70,1.1]].forEach(([x,y,a],k)=>{if(q<a)return;const b=Math.round(Math.sin(t*5+k));R(g,x,y+b,14,13,INKC);R(g,x+1,y+1+b,12,11,'#14265a');ptext(g,'ABC'[k],x+6,y+4+b,AMBER)});return{}}
function sceneChoice(q,t){const g=wg;blueprintWall(g,t);g.globalAlpha=.6;R(g,0,56,WW,104,'#0a1433');g.globalAlpha=1;const sel=q>=.25?Math.min(2,Math.floor((q-.25)/.9)):-1;
 for(let k=0;k<3;k++){const y=60+k*20,hot=sel==k;R(g,5,y,80,18,hot?MINT:INKC);R(g,6,y+1,78,16,hot?'#1c3a6e':'#14265a');R(g,6,y+1,78,1,'#2c4a8a');R(g,8,y+2,14,14,'#0c1c44');if(k==0)keyBox(g,10,y+3);if(k==1)guardIcon(g,9,y+2);if(k==2)doorIcon(g,9,y+2);
  if(hot){const b=Math.round(Math.sin(t*12));for(let i=0;i<4;i++)R(g,1+b,y+5+i,i<2?i+1:4-i,1,MINT)}}return{}}
const HEADS=[[0.05,2.3,"HUNDREDS ARE PUSHING",["ON THIS DOOR"]],[2.3,5.0,"IT WON'T OPEN",["HOW DO YOU","FIX THAT?"],{tc:CORAL}],
 [7.61,10.0,"MEET",["CARL PRINZLER"]],[10.02,13.03,"CHICAGO · DEC 30, 1903",["THE IROQUOIS","THEATRE BURNS"]],
 [13.05,14.2,"THE EXITS",["FAILED."],{tc:CORAL}],[14.22,16.3,"THE EXITS FAILED",["602 DIED."],{tc:CORAL}],[16.32,17.7,"CARL",["COULDN'T","LET IT GO."]],
 [17.72,18.5,"YOU ARE",["CARL"]],[18.5,20.47,"THREE OPTIONS",["WHICH ONE?"],{tc:AMBER}],
 [20.49,24.45,"OPTION A",["UNLOCK EVERY","EXIT"],{tc:AMBER}],[24.47,28.52,"OPTION B",["AN USHER AT","EVERY EXIT"],{tc:AMBER}],[28.54,33.87,"OPTION C",["A BAR ACROSS","THE DOOR"],{tc:AMBER}],
 [36.89,38.8,"PLAY OUT A",["UNLOCK EVERY EXIT"]],[38.82,41.0,"BUT SOME DOORS",["OPENED INWARD"],{tc:CORAL}],[41.02,45.0,"A CROWD PRESSES",["IT STAYS SHUT"],{tc:CORAL}],
 [45.02,46.6,"PLAY OUT B",["AN USHER AT EVERY EXIT"]],[46.62,48.3,"THE THEATRE",["HAD USHERS"],{tc:CORAL}],[48.32,51.5,"NO FIRE DRILL, EVER",["SOME DIDN'T","KNOW THE EXITS"],{tc:CORAL}],
 [51.52,54.8,"PLAY OUT C",["CARL + HIS","NEIGHBOR"],{tc:MINT}],[54.82,56.5,"IT TOOK THEM",["FIVE YEARS"]],[56.52,59.37,"THE CROWD PUSHES",["IT SWINGS OUT."],{tc:MINT}],
 [59.39,63.1,"RULE UNLOCKED",["PANIC BAR"],{tc:MINT}],[63.12,65.02,"THEATERS + SCHOOLS",["50+ PEOPLE"]],[65.06,END,"LEVEL 01",["CLEARED"],{tc:MINT}]];
function heart(x,y,full){og.fillStyle=full?CORAL:'#3a3668';const u=7;[[1,0,2,1],[4,0,2,1],[0,1,7,2],[1,3,5,1],[2,4,3,1],[3,5,1,1]].forEach(([a,b,w,h])=>og.fillRect(x+a*u,y+b*u,w*u,h*u))}
function badge(L,t0,t){const a=ease(seg(t,t0,t0+.18));if(a<=0)return;const p=1+.35*(1-a);og.save();og.translate(150,830);og.scale(p,p);og.globalAlpha=a;og.fillStyle=INKC;rrect(og,-78,-78,156,156,24);og.fill();og.fillStyle=AMBER;rrect(og,-66,-66,132,132,18);og.fill();mdraw(L,0,6,110,INKC,'center',false,'',0,a);og.restore()}
function hud(t){const DONE=65.02,done=t>=DONE,pr=cl01(t/DONE),y=566,s=84,gap=18,x0=250,a=ease(seg(t,5.0,5.35));if(a<=0)return;og.save();og.globalAlpha=a;
 mdraw("LV 1",60,y+s/2+2,40,MINT,'left',false,'',0,a);
 for(let i=0;i<5;i++){const x=x0+i*(s+gap),ok=i==0&&done,cur=i==0&&!done;og.globalAlpha=a;og.fillStyle=ok?'#173a2c':'#1b1838';rrect(og,x,y,s,s,12);og.fill();
  if(cur){og.save();rrect(og,x,y,s,s,12);og.clip();og.fillStyle='#2a4a7a';og.fillRect(x,y+s*(1-pr),s,s*pr);og.restore()}
  const nxt=i==1&&t>67.2;og.lineWidth=4;og.strokeStyle=ok?MINT:cur?CORAL:(nxt&&Math.sin(t*10)>0?AMBER:'#3a3668');rrect(og,x,y,s,s,12);og.stroke();
  if(ok){og.strokeStyle=MINT;og.lineWidth=9;og.lineCap='round';og.beginPath();og.moveTo(x+22,y+44);og.lineTo(x+37,y+59);og.lineTo(x+63,y+27);og.stroke()}
  else mdraw(cur?"01":"?",x+s/2,y+s/2+2,cur?34:38,cur?CREAM:(nxt?AMBER:'#5a568a'),'center',false,'',0,a)}
 const lives=t<43.3?3:t<50.2?2:1;for(let i=0;i<3;i++)heart(800+i*76,y+20,i<lives);og.restore()}
function frameAt(t){
 QA.chars=[];QA.solids=[];og.imageSmoothingEnabled=false;og.clearRect(0,0,1080,1920);
 const sg=SEG.find(s=>t>=s[0]&&t<s[1])||SEG[SEG.length-1],id=sg[4],o=sg[2]+(t-sg[0])*(sg[3]-sg[2])/(sg[1]-sg[0]);QA.shot=sg[5];let sh=0,z=1,inf={};
 if(id=='mission')inf=sceneMission(o);else if(id=='carl')sceneCarl(o);else if(id=='street')inf=sceneStreet(o);else if(id=='fire')sceneFire(o);else if(id=='locked')sceneLocked(o);
 else if(id=='think')sceneThink(o);else if(id=='ask')sceneAsk(o,t);else if(id=='pA'||id=='A1')sceneUnlock(o,t);else if(id=='pB'||id=='B1')sceneUsher(o,t);else if(id=='pC'||id=='bar')sceneBar(o);
 else if(id=='choice')sceneChoice(o,t);else if(id=='A'){sceneInward(o,t);sh=shake(t,43.3)}else if(id=='B'){sceneB(o,t);sh=shake(t,50.2)}
 else if(id=='two')sceneTwo(o);else if(id=='lean'){inf=sceneLean(o);z=lerp(1,1.16,ease(seg(o,28.08,29.85)));sh=shake(o,28.7)}
 else if(id=='school')inf=sceneSchool(o);else if(id=='count')inf=sceneCount(o);else sceneWin(o);
 if(z>1){const sw=WW/z,shh=104/z;og.fillStyle=NAVY;og.fillRect(0,0,1080,672);og.save();og.beginPath();og.rect(0,672,1080,1248);og.clip();og.drawImage(wc,(WW-sw)/2,56+(104-shh)*.55,sw,shh,sh,672,1080,1248);og.restore()}
 else og.drawImage(wc,0,0,WW,WH,sh,0,1080,1920);
 lit(()=>{const f=.6+.4*Math.sin(t*9)*Math.sin(t*5.3);
  if(id=='mission'){glow(45*12,68*12,260,RED,.22+.12*Math.sin(t*5));glow(540,1500,700,COOL,.12);if(t>=5.0)grade('#c8a070',.35*ease(seg(t,6.0,7.1)),'multiply')}
  else if(id=='carl'){glow(260,780,620,WARM,.30);glow(77*12,94*12,170,WARM,.35)}
  else if(id=='street'){const cam=inf.cam||0;for(const lx of[36,128,206])glow((lx-cam)*12,72*12,230,WARM,.34);grade('#b8c4e8',.22,'multiply')}
  else if(id=='fire'){glow(45*12,70*12,520,FIRE,.30+.14*f);grade('#6a5a8a',.38,'multiply')}
  else if(id=='locked'){glow(540,56*12,560,FIRE,.34+.16*f);glow(540,153*12,420,FIRE,.22+.1*f);grade('#3a3050',.30,'multiply')}
  else if(id=='think'){glow(900,900,640,WARM,.26);grade('#4a4470',.34,'multiply')}
  else if(id=='choice'||id=='ask')glow(540,1000,700,COOL,.16);
  else if(id=='pA'||id=='A1'){glow(540,740,300,GREEN,.3);glow(540,1300,700,COOL,.12)}
  else if(id=='pB'||id=='B1'){glow(760,780,300,GREEN,.3);glow(300,1000,560,WARM,.22)}
  else if(id=='A'){glow(540,1300,700,WARM,.12);grade('#c0503f',.16*ease(seg(t,43.3,43.8)),'multiply')}
  else if(id=='B')glow(540,60*12,300,SUN,.2);
  else if(id=='two'){shaft(7,26,63,24,70,160,'#fff4c8',.13);glow(16*12,75*12,330,SUN,.3)}
  else if(id=='bar'||id=='pC')glow(540,76*12,460,SUN,.28);
  else if(id=='lean'){const u=inf.u||0;if(u>0){glow(540,1560,620,SUN,.22*u);shaft(34,58,118,14,76,160,'#fff4c8',.2*u)}}
  else if(id=='school'){glow(53*12,62*12,170,GREEN,.4);const u=inf.u||0;if(u>0){glow(76*12,90*12,520,SUN,.2*u);shaft(69,88,62,40,90,160,'#fff4c8',.14*u)}}
  else if(id=='count')glow(540,60*12,380,SUN,.25);
  else glow(70*12,66*12,520,SUN,.45)});
 const v=og.createLinearGradient(0,0,0,1920);v.addColorStop(0,'rgba(0,0,0,.22)');v.addColorStop(.3,'rgba(0,0,0,0)');v.addColorStop(.8,'rgba(0,0,0,0)');v.addColorStop(1,'rgba(0,0,0,.35)');og.fillStyle=v;og.fillRect(0,0,1080,1920);
 og.globalAlpha=.6;og.fillStyle='#0f0d22';og.fillRect(0,110,1080,562);og.globalAlpha=1;
 const h=HEADS.find(h=>t>=h[0]&&t<h[1]);
 if(t>=5.0&&t<7.59){const yr=Math.round(lerp(2026,1903,ease(seg(t,6.0,7.1))));header(t<6.0?"LEVEL 01":"CHICAGO",[t<6.0?"GET THEM OUT":String(yr)],(t-5.0)/.2,{tc:t>7.1||t<6.0?AMBER:CREAM})}
 else if(id=='choice'){const q=t-33.87,n=3-Math.min(2,Math.floor(Math.max(0,q-.25)/.9)),p=1+.25*(1-ease(seg(((Math.max(0,q-.25))%.9),0,.2)));header("LOCK IT IN",[],1);og.save();og.translate(540,330);og.scale(p,p);mdraw(String(n),0,0,220,AMBER,'center',true,INKC,20,1);og.restore()}
 else if(h)header(h[2],h[3],(t-h[0])/.2,h[4]);
 hud(t);
 if(id=='pA')badge("A",21.15,t);if(id=='pB')badge("B",25.2,t);if(id=='pC')badge("C",29.25,t);
 if(id=='A1'||id=='A')badge("A",36.9,t);if(id=='B1'||id=='B')badge("B",45.03,t);if(id=='two'||id=='bar'||id=='lean')badge("C",51.55,t);
 if(id=='mission'&&t>=2.35&&t<5.0)stamp("WON'T OPEN",'#e0473c',800,880,2.35,t,-.08,40);
 if(id=='choice'){const L=[["A","UNLOCK EVERY EXIT"],["B","AN USHER AT EVERY EXIT"],["C","A BAR ACROSS THE DOOR"]];
  L.forEach(([a,s],k)=>{const y=(69+k*20)*12;mdraw(a,26.5*12,y+2,56,AMBER,'center',true,INKC,10,1);mdraw(s,31*12,y+2,fit(s,40,600),CREAM,'left',false,'',0,1)})}
 if(id=='A'&&t>=43.3)stamp("A FAILS",'#e0473c',540,1040,43.3,t,-.07,64);
 if(id=='B'&&t>=50.2)stamp("B FAILS",'#e0473c',540,1180,50.2,t,-.07,64);
 if(id=='lean'&&t>=58.4)stamp("C WORKED",'#2fbf8f',640,860,58.4,t,-.07,60);
 if(id=='win'){const xp=Math.round(100*ease(seg(t,65.3,66.0)));mdraw("+"+xp+" XP",540,800,70,AMBER,'center',true,INKC,14,1);
  if(t>66.24&&t<67.2)tag("COMMENT A, B OR C",540,1400,AMBER,ease(seg(t,66.24,66.4)));if(t>=67.2)tag("FOLLOW FOR LEVEL 02",540,1400,MINT,ease(seg(t,67.2,67.37)))}
 subtitle(t,false);for(const c of CUTS)wipe(t,c,.12);
}
window.frame=i=>frameAt(i/30);
Promise.all([document.fonts.load('700 40px Silk'),document.fonts.load('400 40px PS2P')]).then(()=>{window.READY=true});
