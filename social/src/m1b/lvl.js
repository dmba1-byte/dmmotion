// ===== Level 01, playable cut =====
const END=50.0;
const SUBS=[[0.13,0.85,"Level one."],[0.98,3.08,"Hundreds of people need out through this door."],[3.19,3.9,"It's locked."],[4.09,5.0,"How do you open it?"],
[5.29,6.4,"This was a real level."],[6.58,8.1,"Chicago, 1903."],
[8.39,10.45,"Carl Prinzler sold door hardware."],[10.88,13.05,"He planned to see a show at the Iroquois Theatre,"],[13.23,14.55,"then changed his plans."],
[14.85,16.2,"That afternoon, it burned."],[16.57,17.5,"The exits were locked,"],[17.58,19.35,"and about 600 people died."],
[19.68,20.7,"Carl couldn't let it go."],[20.75,21.75,"So, pick your fix."],[22.21,23.88,"A: a key by every door."],[23.98,25.17,"B: a guard at every exit."],[25.28,26.75,"C: a bar across the door."],
[29.04,29.75,"A fails."],[29.8,31.22,"Nobody finds a key in the dark."],[31.64,32.36,"B fails."],[32.4,34.1,"One guard can't be at every door."],
[34.42,36.98,"C took Carl five years, and an architect neighbor."],[37.41,39.9,"The crowd pushes the bar, and the door opens."],
[40.2,42.52,"Today, codes require it on the exits"],[42.59,43.7,"of theaters and schools"],[43.96,45.52,"that hold 50 people or more."],
[45.84,46.62,"Level cleared."],[46.9,47.78,"Comment what you picked,"],[47.83,49.27,"and follow for level two."]];
// [new start, new end, old start, old end, scene, shot type]
const SEG=[[0,5.29,0,4.85,'mission','back'],[5.29,8.39,4.85,7.38,'mission','front'],[8.39,10.88,7.38,9.87,'carl','closeup'],[10.88,14.85,9.87,14.42,'street','side'],
[14.85,16.57,14.42,16.15,'fire','elevation'],[16.57,19.68,16.15,19.26,'locked','detail'],[19.68,20.75,19.26,20.55,'think','closeup'],
[20.75,29.04,0,8.29,'choice','menu'],[29.04,31.64,0,2.6,'A','back'],[31.64,34.42,0,2.78,'B','plan'],
[34.42,37.41,23.61,26.39,'two','side'],[37.41,38.6,26.39,28.08,'bar','detail'],[38.6,40.2,28.08,29.85,'lean','back'],
[40.2,43.96,29.85,34.3,'school','side'],[43.96,45.84,34.3,36.36,'count','plan'],[45.84,END,36.36,40.52,'win','front']];
const CUTS=SEG.slice(1).map(s=>s[0]);
function keyBox(g,x,y){R(g,x-1,y-1,12,14,INKC);R(g,x,y,10,12,'#cfe6f2');R(g,x,y,10,2,'#eaf6fb');R(g,x+3,y+3,4,4,BRASS);R(g,x+4,y+4,2,2,'#cfe6f2');R(g,x+4,y+7,2,4,BRASS);px(g,x+6,y+9,BRASS)}
function guardIcon(g,x,y){R(g,x+3,y,6,2,'#2a3a6a');R(g,x+2,y+2,8,1,'#2a3a6a');R(g,x+3,y+3,6,4,'#e9c3a3');px(g,x+7,y+4,INKC);R(g,x+2,y+7,8,6,'#3f5fa8');px(g,x+4,y+9,BRASS);R(g,x+3,y+13,2,1,'#2a2a34');R(g,x+7,y+13,2,1,'#2a2a34')}
function doorIcon(g,x,y){R(g,x+1,y,10,14,'#4a3220');R(g,x+2,y+1,8,13,'#7a5434');R(g,x+2,y+7,8,2,BRASS);R(g,x+2,y+7,8,1,'#f4dc8a')}
function sceneChoice(q,t){const g=wg;blueprintWall(g,t);g.globalAlpha=.6;R(g,0,56,WW,104,'#0a1433');g.globalAlpha=1;
 const at=[1.46,3.23,4.53],sel=q>=6.15?Math.min(2,Math.floor((q-6.15)/.68)):-1;
 for(let k=0;k<3;k++){const y=60+k*20,on=q>=at[k];
  if(!on){g.globalAlpha=.5;for(let x=6;x<84;x+=4){px(g,x,y,'#9fc3ff');px(g,x,y+17,'#9fc3ff')}g.globalAlpha=1;continue}
  const pop=q-at[k]<.12?1:0,hot=sel==k;
  R(g,5-pop,y-pop,80+2*pop,18+2*pop,hot?MINT:INKC);R(g,6,y+1,78,16,hot?'#1c3a6e':'#14265a');R(g,6,y+1,78,1,'#2c4a8a');
  R(g,8,y+2,14,14,'#0c1c44');if(k==0)keyBox(g,10,y+3);if(k==1)guardIcon(g,9,y+2);if(k==2)doorIcon(g,9,y+2);
  if(hot){const b=Math.round(Math.sin(t*12));for(let i=0;i<4;i++)R(g,1+b,y+5+i,i<2?i+1:4-i,1,MINT)}}
 return{}}
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
const HEADS=[
 [0.05,3.19,"LEVEL 01",["GET THEM OUT"]],[3.19,5.29,"LEVEL 01",["THE DOOR","IS LOCKED."],{tc:CORAL}],
 [8.42,10.88,"MEET",["CARL PRINZLER"]],
 [10.9,13.21,"CHICAGO · DEC 30, 1903",["A TICKET TO","THE IROQUOIS"]],[13.23,14.85,"BUT",["HE CHANGED","HIS PLANS."]],
 [14.88,16.57,"THAT AFTERNOON",["FIRE."]],[16.6,17.56,"THE EXITS",["LOCKED."]],[17.58,19.68,"THE EXITS WERE LOCKED",["ABOUT 600","DIED."]],
 [19.7,20.75,"CARL",["COULDN'T","LET IT GO."]],
 [29.06,31.64,"ATTEMPT A",["KEY BY THE DOOR"]],[31.66,34.42,"ATTEMPT B",["A GUARD"]],
 [34.45,37.41,"ATTEMPT C · 5 YEARS",["CARL + AN","ARCHITECT"]],[37.43,38.6,"ATTEMPT C",["ONE BAR."]],[38.62,40.2,"THE CROWD PUSHES",["IT OPENS."],{tc:MINT}],
 [40.22,43.96,"RULE UNLOCKED",["PANIC BAR"],{tc:MINT}],[43.98,45.84,"THEATERS + SCHOOLS",["50+ PEOPLE"]],
 [45.88,END,"LEVEL 01",["CLEARED"],{tc:MINT}]];
function heart(x,y,full){const c=full?CORAL:'#3a3668';og.fillStyle=c;const u=7;[[1,0,2,1],[4,0,2,1],[0,1,7,2],[1,3,5,1],[2,4,3,1],[3,5,1,1]].forEach(([a,b,w,h])=>og.fillRect(x+a*u,y+b*u,w*u,h*u))}
function hud(t){const done=t>=45.84,pr=cl01(t/45.84),y=566,s=84,gap=18,x0=250;
 mdraw("LV 1",60,y+s/2+2,40,MINT,'left',false,'',0,1);
 for(let i=0;i<5;i++){const x=x0+i*(s+gap);og.globalAlpha=1;og.fillStyle=i==0&&done?'#173a2c':'#1b1838';rrect(og,x,y,s,s,12);og.fill();
  if(i==0&&!done){og.save();rrect(og,x,y,s,s,12);og.clip();og.fillStyle='#2a4a7a';og.fillRect(x,y+s*(1-pr),s,s*pr);og.restore()}
  const nxt=i==1&&t>47.83;og.lineWidth=4;og.strokeStyle=i==0?(done?MINT:CORAL):(nxt&&Math.sin(t*10)>0?AMBER:'#3a3668');rrect(og,x,y,s,s,12);og.stroke();
  if(i==0&&done){og.strokeStyle=MINT;og.lineWidth=9;og.lineCap='round';og.beginPath();og.moveTo(x+22,y+44);og.lineTo(x+37,y+59);og.lineTo(x+63,y+27);og.stroke()}
  else mdraw(i==0?"01":"?",x+s/2,y+s/2+2,i==0?34:38,i==0?CREAM:(nxt?AMBER:'#5a568a'),'center',false,'',0,1)}
 const lives=t<29.9?3:t<32.6?2:1;for(let i=0;i<3;i++){const lost=i>=lives,jx=(!lost||0)?0:0;heart(800+i*76,y+20,!lost)}
}
function frameAt(t){
 QA.chars=[];QA.solids=[];
 og.imageSmoothingEnabled=false;og.clearRect(0,0,1080,1920);
 const sg=SEG.find(s=>t>=s[0]&&t<s[1])||SEG[SEG.length-1],id=sg[4];
 const o=sg[2]+(t-sg[0])*(sg[3]-sg[2])/(sg[1]-sg[0]); // the scene's own clock
 QA.shot=sg[5];let sh=0,z=1,inf={};
 if(id=='mission'){inf=sceneMission(o)}
 else if(id=='carl')sceneCarl(o);else if(id=='street')inf=sceneStreet(o);else if(id=='fire')sceneFire(o);else if(id=='locked')sceneLocked(o);
 else if(id=='think')sceneThink(o);else if(id=='choice')sceneChoice(o,t);else if(id=='A'){inf=sceneA(o,t);sh=shake(t,29.74)}else if(id=='B'){sceneB(o,t);sh=shake(t,32.5)}
 else if(id=='two')sceneTwo(o);else if(id=='bar')sceneBar(o);else if(id=='lean'){inf=sceneLean(o);z=lerp(1,1.16,ease(seg(o,28.08,29.85)));sh=shake(o,28.7)}
 else if(id=='school')inf=sceneSchool(o);else if(id=='count')inf=sceneCount(o);else sceneWin(o);
 if(z>1){const sw=WW/z,shh=104/z;og.fillStyle=NAVY;og.fillRect(0,0,1080,672);og.save();og.beginPath();og.rect(0,672,1080,1248);og.clip();og.drawImage(wc,(WW-sw)/2,56+(104-shh)*.55,sw,shh,sh,672,1080,1248);og.restore()}
 else og.drawImage(wc,0,0,WW,WH,sh,0,1080,1920);
 lit(()=>{const f=.6+.4*Math.sin(t*9)*Math.sin(t*5.3);
  if(id=='mission'){glow(45*12,68*12,260,RED,.22+.12*Math.sin(t*5));glow(540,1500,700,COOL,.12);if(t>=5.29)grade('#c8a070',.35*ease(seg(t,6.58,7.6)),'multiply')}
  else if(id=='carl'){glow(260,780,620,WARM,.30);glow(77*12,94*12,170,WARM,.35)}
  else if(id=='street'){const cam=inf.cam||0;for(const lx of[36,128,206])glow((lx-cam)*12,72*12,230,WARM,.34);grade('#b8c4e8',.22,'multiply')}
  else if(id=='fire'){glow(45*12,70*12,520,FIRE,.30+.14*f);grade('#6a5a8a',.38,'multiply')}
  else if(id=='locked'){glow(540,56*12,560,FIRE,.34+.16*f);glow(540,153*12,420,FIRE,.22+.1*f);grade('#3a3050',.30,'multiply')}
  else if(id=='think'){glow(900,900,640,WARM,.26);grade('#4a4470',.34,'multiply')}
  else if(id=='choice'){glow(540,1000,700,COOL,.16)}
  else if(id=='A'){grade('#10122a',.66,'multiply');glow((inf.kx||45)*12,98*12,230,COOL,.30);glow(75*12,92*12,90,WARM,.5)}
  else if(id=='B'){glow(540,60*12,300,SUN,.2)}
  else if(id=='two'){shaft(7,26,63,24,70,160,'#fff4c8',.13);glow(16*12,75*12,330,SUN,.3)}
  else if(id=='bar'){glow(540,76*12,460,SUN,.28)}
  else if(id=='lean'){const u=inf.u||0;if(u>0){glow(540,1560,620,SUN,.22*u);shaft(34,58,118,14,76,160,'#fff4c8',.2*u)}}
  else if(id=='school'){glow(53*12,62*12,170,GREEN,.4);const u=inf.u||0;if(u>0){glow(76*12,90*12,520,SUN,.2*u);shaft(69,88,62,40,90,160,'#fff4c8',.14*u)}}
  else if(id=='count'){glow(540,60*12,380,SUN,.25)}
  else{glow(70*12,66*12,520,SUN,.45)}
 });
 const v=og.createLinearGradient(0,0,0,1920);v.addColorStop(0,'rgba(0,0,0,.22)');v.addColorStop(.3,'rgba(0,0,0,0)');v.addColorStop(.8,'rgba(0,0,0,0)');v.addColorStop(1,'rgba(0,0,0,.35)');og.fillStyle=v;og.fillRect(0,0,1080,1920);
 og.globalAlpha=.6;og.fillStyle='#0f0d22';og.fillRect(0,110,1080,562);og.globalAlpha=1;
 const h=HEADS.find(h=>t>=h[0]&&t<h[1]);
 if(t>=5.29&&t<8.39){const yr=Math.round(lerp(2026,1903,ease(seg(t,6.58,7.6))));header(t<6.58?"THIS WAS A":"REWIND TO",[t<6.58?"REAL LEVEL":String(yr)],(t-5.29)/.2,{tc:t>7.6||t<6.58?AMBER:CREAM})}
 else if(id=='choice'){const q=t-20.75;if(q<6.15)header("YOUR TURN",["PICK YOUR FIX"],q/.2);else{const n=3-Math.min(2,Math.floor((q-6.15)/.68)),p=1+.25*(1-ease(seg(((q-6.15)%.68),0,.2)));header("PICK ONE",[],1);og.save();og.translate(540,330);og.scale(p,p);mdraw(String(n),0,0,220,AMBER,'center',true,INKC,20,1);og.restore()}}
 else if(h)header(h[2],h[3],(t-h[0])/.2,h[4]);
 hud(t);
 if(t<5.29){const left=Math.max(0,10-t*.9);mdraw("TIME",150,760,30,CREAM,'center',true,INKC,8,1);mdraw("0:"+String(Math.ceil(left)).padStart(2,'0'),150,830,64,Math.ceil(left)<=6?CORAL:AMBER,'center',true,INKC,12,1);
  if(t>=3.19)stamp("LOCKED",'#e0473c',760,800,3.19,t,.08,56)}
 if(id=='choice'){const q=t-20.75,at=[1.46,3.23,4.53],L=[["A","KEY BY EVERY DOOR"],["B","GUARD AT EVERY EXIT"],["C","BAR ACROSS THE DOOR"]];
  L.forEach(([a,s],k)=>{if(q<at[k])return;const al=ease(seg(q,at[k],at[k]+.15)),y=(69+k*20)*12;mdraw(a,26.5*12,y+2,56,AMBER,'center',true,INKC,10,al);mdraw(s,31*12,y+2,fit(s,40,600),CREAM,'left',false,'',0,al)})}
 if(id=='A'&&t>=29.74)stamp("ATTEMPT A FAILED",'#e0473c',540,900,29.74,t,-.07,58);
 if(id=='B'&&t>=32.5)stamp("ATTEMPT B FAILED",'#e0473c',540,960,32.5,t,-.07,52);
 if(id=='bar'&&t>37.9)tag("PUSH",540,1470,MINT,ease(seg(t,37.9,38.05)));
 if(id=='count'){const n=Math.min(50,inf.outN||0);mdraw(n>=50?"50+":String(n),170,740,64,AMBER,'center',true,INKC,12,1);mdraw("OUT",170,800,28,CREAM,'center',true,INKC,8,1)}
 if(id=='win'){const xp=Math.round(100*ease(seg(t,46.0,46.7)));mdraw("+"+xp+" XP",540,800,70,AMBER,'center',true,INKC,14,1);
  if(t>46.9&&t<47.83)tag("COMMENT A, B OR C",540,1400,AMBER,ease(seg(t,46.9,47.05)));if(t>=47.83)tag("FOLLOW FOR LEVEL 02",540,1400,MINT,ease(seg(t,47.83,48.0)))}
 subtitle(t,false);
 for(const c of CUTS)wipe(t,c,.12);
}
window.frame=i=>frameAt(i/30);
Promise.all([document.fonts.load('700 40px Silk'),document.fonts.load('400 40px PS2P')]).then(()=>{window.READY=true});
