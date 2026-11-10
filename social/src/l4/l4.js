// ===== Level 04 : the door beside the revolving door (Cocoanut Grove, 1942) =====
const V=i=>VT[i][0]-.12,MENU0=VT[11][1]+.25;
const SEG=[[0,V(1),'lobby','back'],[V(1),V(2),'rewind','front'],[V(2),VT[2][2].length?VT[2][2][0][1]-.05:V(2)+2.4,'club','wide'],[0,V(3),'spin','plan'],[V(3),0,'rush','wide'],[0,V(4),'jam','plan'],[V(4),V(5),'face1','closeup'],[V(5),V(6),'ask','front'],
 [V(6),V(8),'pA','elevation'],[V(8),V(10),'pB','plan'],[V(10),MENU0,'pC','elevation'],[MENU0,V(12),'choice','menu'],
 [V(12),0,'A1','elevation'],[0,V(13),'A','detail'],[V(13),V(14),'B','plan'],[V(14),V(15),'C','side'],[V(15),0,'face2','closeup'],[0,V(16),'lobby2','back'],[V(16),END,'win','front']];
SEG[3][0]=SEG[2][1];SEG[4][1]=VT[3][2].length?VT[3][2][0][1]-.05:V(3)+2.7;SEG[5][0]=SEG[4][1];SEG[12][1]=VT[12][2][0][1]-.05;SEG[13][0]=SEG[12][1];SEG[16][1]=VT[15][2][0][1]-.05;SEG[17][0]=SEG[16][1];
const CUTS=SEG.slice(1).map(s=>s[0]);
LOOK.inv={id:'inv',skin:'#e9c3a3',skinD:'#c99d7e',hair:'#4a3a30',top:'#3a4a6a',topL:'#56688a',pants:'#2a2a34',shoe:'#121016'};
const GLASS='#9cc4ec',GLASSD='#6f9cc8',FRAME='#3a3f4c';
function box(g,x,y,w,h,c){R(g,x,y,w,1,c);R(g,x,y+h-1,w,1,c);R(g,x,y,1,h,c);R(g,x+w-1,y,1,h,c)}
// revolving door in elevation: a glass drum with wings that pass the eye
function revDoor(g,cx,top,h,rot,o){o=o||{};const r=12,fr=o.frame||FRAME;R(g,cx-r-2,top-3,r*2+4,3,fr);R(g,cx-r-1,top,r*2+2,h,o.dark?'#1a2238':'#cfe4f6');
 for(let x=-r;x<=r;x++){const sh=Math.abs(x)/r;R(g,cx+x,top,1,h,mixc(o.dark?'#2a3658':'#dff0fb',o.dark?'#141a30':'#8fb6dc',sh*sh))}
 for(let k=0;k<4;k++){const a=rot+k*Math.PI/2,x=Math.round(cx+Math.cos(a)*(r-1)),front=Math.sin(a)>0;if(!o.flat){R(g,x,top+1,1,h-1,front?'#f4fbff':'#7f9cc0');if(front)R(g,x+(Math.cos(a)>0?-1:1),top+h*.45,1,5,'#d9b24a')}}
 if(o.flat){R(g,cx-1,top+1,2,h-1,'#f4fbff')}
 R(g,cx,top,1,h,fr);R(g,cx-r-2,top,1,h,fr);R(g,cx+r+1,top,1,h,fr);R(g,cx-r-2,top+h,r*2+4,1,fr)}
function sideDoor(g,x,top,h,u,o){o=o||{};R(g,x-1,top-1,13,h+1,FRAME);R(g,x,top,11,h,o.dark?'#141a30':'#2a3040');const w=Math.round(11*(1-u*.75));R(g,x,top,w,h,o.dark?'#2a3658':'#bfdcf2');R(g,x,top,1,h,'#f4fbff');if(w>3)R(g,x+w-3,top+h*.5,2,1,'#d9b24a');
 if(o.bar&&w>5){R(g,x+1,top+h*.55,w-2,2,'#d9b24a')}}
function facade(g,t,night){R(g,0,0,WW,56,NAVY);for(let y=56;y<FL;y++)R(g,0,y,WW,1,night?'#2a2434':'#c9ced6');
 for(let x=2;x<WW;x+=22){R(g,x,58,18,20,FRAME);R(g,x+1,59,16,18,night?'#3a3458':GLASS);R(g,x+9,59,1,18,FRAME);if(!night){R(g,x+2,60,5,1,'#e4f2fc')}}
 R(g,0,80,WW,2,night?'#1a1620':'#9aa2ae');for(let y=FL;y<WH;y++)R(g,0,y,WW,1,(y-FL)%7==0?(night?'#1e1a28':'#8d939c'):(night?'#2a2434':'#aeb4bd'));for(let x=-60;x<WW+60;x+=13)line(g,45+(x-45)*.6,FL,45+(x-45)*1.7,WH,1,night?'#1e1a28':'#8d939c')}
function sceneLobby(q,t,done){const g=wg;facade(g,t,false);revDoor(g,done?36:46,84,36,t*1.6);if(done)sideDoor(g,58,86,34,0,{bar:1});
 if(!done){if(q>1.8&&Math.sin(t*7)>0)box(g,31,80,31,42,AMBER)}else{box(g,56,83,15,39,MINT);R(g,54,72,19,9,INKC);R(g,55,73,17,7,'#2fbf8f');ptext(g,'EXIT',56,74,'#fffaf0')}
 const br=Math.sin(t*2.4)>.4?-1:0,pt=q>1.2?Math.round(ease(seg(q,1.2,1.6))*12):0;
 personFB({hip:GY-17,feet:[[-3,0],[3,0]],sl:1,sa:[1,1],hands:[[CX-8,SHY+10],[CX+10+(pt?4:0),SHY+10-pt]],hy:br,nobag:false},-16,-2,null,'b');return{}}
function sceneRewind(q,t){const g=wg;blueprintWall(g,t);const br=Math.sin(t*2.4)>.5?-1:0,sh=Math.round(Math.sin(q*7));
 personFB({hip:GY-17,feet:[[-3,0],[3,0]],sl:1,sa:[1,1],hands:[[CX-14,SHY+5+sh],[CX+13,SHY+5+sh]],mouth:'open',hy:br,nobag:false},13,0,null,'f');return{}}
function club(g,t,fire){R(g,0,0,WW,56,NAVY);for(let y=56;y<FL;y++)R(g,0,y,WW,1,mixc('#141834','#2c2a4c',(y-56)/64));for(let k=0;k<16;k++)px(g,(k*37)%WW,58+(k*11)%20,'#cfd6ff');
 R(g,4,74,82,46,'#3a2a30');R(g,4,74,82,2,'#523a42');for(let y=80;y<120;y+=5)for(let x=4+((y/5)%2?0:5);x<86;x+=10)R(g,x,y,1,5,'#2e2026');
 // neon sign with a palm
 R(g,16,58,58,14,INKC);R(g,17,59,56,12,'#1a1020');const on=Math.sin(t*9)>-.7;ptext(g,'COCOANUT',20,60,on?'#ff8ab0':'#7a3a50');ptext(g,'GROVE',44,66,on?'#7df0c0':'#2a6a54');
 R(g,22,66,1,5,'#7df0c0');for(const[a,b]of[[-3,0],[-2,-1],[2,-1],[3,0],[0,-2]])px(g,22+a,66+b,'#7df0c0');
 for(const x of[10,70]){R(g,x,84,10,14,'#1a1020');R(g,x+1,85,8,12,fire?'#ff9040':'#e8c860');R(g,x+5,85,1,12,'#1a1020')}
 revDoor(g,45,88,32,fire?0:t*2.2,{dark:!fire,frame:'#d9b24a'});if(fire){g.globalAlpha=.55;R(g,32,88,26,32,'#ff9040');g.globalAlpha=1}
 for(let y=FL;y<WH;y++)R(g,0,y,WW,1,(y-FL)%7==0?'#1e1a28':'#2a2636');for(let x=-60;x<WW+60;x+=13)line(g,45+(x-45)*.6,FL,45+(x-45)*1.7,WH,1,'#1e1a28')}
function tiny(g,x,y,k,s){R(g,x,y-6,2,2,['#e9c3a3','#8a5a3c','#f0caa8','#c98b69'][k%4]);R(g,x,y-4,2,3,['#d9564f','#3f8fb0','#e0b24a','#8a5cc4','#f4ecd8'][k%5]);px(g,x+s,y-1,'#121016');px(g,x+1-s,y-1,'#121016');g.globalAlpha=.25;R(g,x-1,y,4,1,'#000');g.globalAlpha=1}
function sceneClub(q,t){const g=wg;club(g,t,false);for(let k=0;k<7;k++){const side=k%2?1:-1,ph=((q*.35+k*.17)%1),x=45+side*(40-ph*36),y=FL+3+(k%3)*5-Math.round(ph*3);tiny(g,Math.round(x),y,k,Math.floor(q*6+k)%2)}return{}}
function sceneRush(q,t){const g=wg;club(g,t,true);for(let k=0;k<8;k++){const a=k*.8+t*5,r=4+(t*26+k*9)%26;g.globalAlpha=.8-r/40;R(g,45+Math.cos(a)*6+(k-4)*5,86-r,3,3,k%2?'#ff9040':'#ffd27a');g.globalAlpha=1}
 for(let k=0;k<6;k++){g.globalAlpha=.35;R(g,20+k*9+Math.round(Math.sin(t*2+k)*2),60+((t*9+k*7)%16)-8,12,5,'#6a6680');g.globalAlpha=1}return{}}
function planDoor(g,cx,cy,r,rot,flat,c){for(let a=0;a<360;a+=5){if((a>60&&a<120)||(a>240&&a<300))continue;px(g,cx+Math.cos(a*Math.PI/180)*r,cy+Math.sin(a*Math.PI/180)*r,c||'#cfe2ff')}
 if(flat){line(g,cx,cy-r+1,cx,cy+r-1,2,MINT)}else for(let k=0;k<4;k++){const a=rot+k*Math.PI/2;line(g,cx,cy,cx+Math.cos(a)*(r-1),cy+Math.sin(a)*(r-1),1,'#f4fbff')}R(g,cx-1,cy-1,2,2,'#d9b24a')}
function crowdDots(g,n,fn,t){const cols=[MINT,AMBER,'#ff9d8a','#9fc3ff'];for(let k=0;k<n;k++){const[x,y]=fn(k);R(g,x-1,y-1,3,3,INKC);px(g,x,y,cols[k%4]);px(g,x,y-1,cols[k%4]);px(g,x-1,y,cols[k%4]);px(g,x+1,y,cols[k%4]);px(g,x,y+1,cols[k%4])}}
function planRoom(g,inside){R(g,0,0,WW,56,NAVY);R(g,0,56,WW,30,'#3a3f4c');for(let x=3;x<WW;x+=11)R(g,x,66,6,1,'#cfd3da');R(g,0,86,WW,74,inside||'#e9e3d4');R(g,0,84,WW,4,INKC);R(g,29,84,32,4,inside||'#e9e3d4');ptext(g,'STREET',33,58,'#9aa2ae')}
function sceneSpin(q,t){const g=wg;planRoom(g);planDoor(g,45,86,15,t*2.4,false,INKC);
 crowdDots(g,10,k=>{const ph=((q*.5+k*.1)%1),a=Math.PI/2-ph*Math.PI*1.0;return ph<.3?[45+(k%3-1)*4,120-ph*80]:ph<.7?[45+Math.cos(a)*9,86+Math.sin(a)*9]:[45+(k%3-1)*5,78-(ph-.7)*60]},t);
 ptext(g,'ONE AT A TIME',20,146,'#5a5448');return{}}
function sceneJam(q,t){const g=wg;planRoom(g,'#f0d8c8');const j=Math.round(Math.sin(t*28));planDoor(g,45+ (q>.4?j:0)*0,86,15,.5+(q<.5?q*2:1)+Math.sin(t*20)*.03,false,INKC);
 const press=cl01(q/1.3);crowdDots(g,80,k=>{const hx=6+((k*13)%78),hy=100+((k*7)%56),row=Math.floor(k/10),col=k%10;const tx=27+col*4+(row%2)*2,ty=95+row*4.1;return[lerp(hx,tx,press)+(press>=1?Math.round(Math.sin(t*13+k))*.6:0),lerp(hy,ty,press)]},t);
 for(let k=0;k<8;k++){g.globalAlpha=.3;R(g,(k*23+t*6)%100-8,120+((k*13)%36),14,5,'#6a6680');g.globalAlpha=1}return{}}
function sceneFace(q,t,m){const g=wg;R(g,0,0,WW,56,NAVY);for(let y=56;y<WH;y++)R(g,0,y,WW,1,m==1?mixc('#2a2434','#1a1620',(y-56)/104):mixc('#b9ad96','#9c907b',(y-56)/104));
 if(m==1){for(let k=0;k<5;k++){g.globalAlpha=.25;R(g,(k*27+t*5)%100-8,60+k*9,16,5,'#6a6680');g.globalAlpha=1}}else{R(g,58,62,26,30,'#3a3340');R(g,59,63,24,28,'#9cc4ec');R(g,71,63,1,28,'#3a3340')}
 portrait(g,LOOK.inv,{hat:1,shirt:1,brow:m==1?1:0,blink:(t%2.4)<.11,ey:m==1?1:0,mouth:m==1?'flat':'smile',dy:8+(Math.sin(t*2.2)>.4?1:0)});return{}}
function sceneAsk(q,t){const g=wg;blueprintWall(g,t);const br=Math.sin(t*2.4)>.5?-1:0,sh=Math.round(Math.sin(q*6));
 personFB({hip:GY-17,feet:[[-3,0],[3,0]],sl:1,sa:[1,1],hands:[[CX-14,SHY+5+sh],[CX+13,SHY+5+sh]],mouth:'open',hy:br,nobag:false},13,0,null,'f');
 [[14,70,.9],[38,62,1.2],[62,70,1.5]].forEach(([x,y,a],k)=>{if(q<a)return;const b=Math.round(Math.sin(t*5+k));R(g,x,y+b,14,13,INKC);R(g,x+1,y+1+b,12,11,'#14265a');ptext(g,'ABC'[k],x+6,y+4+b,AMBER)});return{}}
function scenePA(q,t,play){const g=wg;facade(g,t,false);revDoor(g,45,82,38,play?t*1.6:(q<1.6?t*1.6:1.1));
 if(!play&&q>1.6){const a=ease(seg(q,1.6,1.9));g.globalAlpha=a;for(let d=0;d<360;d+=3){const x=45+Math.cos(d*Math.PI/180)*20,y=100+Math.sin(d*Math.PI/180)*20;R(g,x,y,2,2,'#e0473c')}line(g,31,86,59,114,3,'#e0473c');g.globalAlpha=1}return{}}
function sceneWinter(q,t){const g=wg;R(g,0,0,WW,56,NAVY);for(let y=56;y<WH;y++)R(g,0,y,45,1,mixc('#39406e','#6a7298',(y-56)/104));for(let y=56;y<WH;y++)R(g,45,y,45,1,mixc('#e9c890','#c9a066',(y-56)/104));
 R(g,0,128,45,32,'#dfe6f2');R(g,45,128,45,32,'#8a5a3c');for(let x=47;x<WW;x+=9)R(g,x,128,1,32,'#7a4c30');
 R(g,60,70,22,28,'#5a3e28');R(g,62,72,18,24,'#f0c24a');for(let k=0;k<3;k++)R(g,66+k*4,80-((Math.floor(t*6)+k)%3),2,8,'#ff9040');R(g,60,98,22,3,'#3a2616');
 revDoor(g,45,78,50,t*1.4);
 for(let k=0;k<40;k++){const x=((k*13+t*22)%52)-8,y=56+((t*18+k*23+Math.sin(t*2+k)*6)%74);if(x<31)px(g,x,y,'#f6f8ff')}
 ptext(g,'COLD',24,60,'#cfe2ff');ptext(g,'WARM',62,60,'#7a3a14');return{}}
function scenePB(q,t,play){const g=wg;planRoom(g);const fold=cl01((q-(play?.6:1.4))/.6);planDoor(g,45,86,15,lerp(.6,Math.PI/2,ease(fold)),fold>=1,INKC);
 const flow=fold>=1?q:0;crowdDots(g,36,k=>{const hx=14+((k*13)%62),hy=104+((k*7)%44);if(fold<1)return[hx,hy-fold*4];const ph=((flow*.45+k*.028)%1);const side=k%2?4:-4;return[lerp(hx,45+side,Math.min(1,ph*2.2))+(ph>.45?(k%5-2)*(ph-.45)*10:0),lerp(hy,62,ph)]},t);
 if(fold>=1){ptext(g,'WINGS FOLD',25,146,'#2f8f5f')}return{}}
function scenePC(q,t){const g=wg;facade(g,t,false);revDoor(g,34,84,36,t*1.6);const u=ease(seg(q,1.5,2.3));sideDoor(g,56,86,34,u,{bar:1});R(g,54,72,19,9,INKC);R(g,55,73,17,7,'#2fbf8f');ptext(g,'EXIT',56,74,'#fffaf0');
 if(Math.sin(t*7)>0)box(g,54,83,17,39,AMBER);return{}}
function sceneC(q,t){const g=wg;R(g,0,0,WW,56,NAVY);R(g,0,56,66,64,'#b9ad96');R(g,0,56,66,1,'#cdc2ac');R(g,0,100,66,2,'#8a7f6c');for(let y=56;y<FL;y++)R(g,71,y,19,1,mixc('#6fb0ea','#e6f4fb',(y-56)/64));
 R(g,44,62,19,9,INKC);R(g,45,63,17,7,'#2fbf8f');ptext(g,'EXIT',46,64,'#fffaf0');
 // the revolving drum, seen edge-on behind
 R(g,6,70,22,50,FRAME);R(g,7,71,20,49,'#cfe4f6');R(g,16+Math.round(Math.cos(t*2)*8),71,1,49,'#f4fbff');R(g,17,71,1,49,FRAME);
 const ox=lerp(-4,44,cl01(q/2.6)),u=ease(seg(q,.9,1.5));
 for(let y=FL;y<WH;y++)R(g,0,y,WW,1,(y-FL)%7==0?'#8a7f6c':'#a89c86');R(g,71,FL,19,40,'#aeb4bd');
 pdoor(g,66,u,{bar:1,wall:'#8a7f6c',wallL:'#b9ad96'});
 const P=walkP(ox+4,{armRel:u<1&&ox>20?[[8,2],null]:null});if(!P.armRel)delete P.armRel;kitp(P,ox,0,false);return{u}}
function icoA(g,x,y){R(g,x+4,y+2,6,11,'#cfe4f6');R(g,x+7,y+2,1,11,FRAME);for(let d=0;d<360;d+=20)px(g,x+7+Math.cos(d*Math.PI/180)*6,y+7+Math.sin(d*Math.PI/180)*6,'#e0473c');line(g,x+3,y+3,x+11,y+11,1,'#e0473c')}
function icoB(g,x,y){for(let d=0;d<360;d+=24)px(g,x+7+Math.cos(d*Math.PI/180)*6,y+7+Math.sin(d*Math.PI/180)*6,'#cfe2ff');R(g,x+7,y+2,1,11,MINT)}
function icoC(g,x,y){R(g,x+1,y+3,6,11,'#cfe4f6');R(g,x+4,y+3,1,11,FRAME);R(g,x+9,y+4,4,10,'#bfdcf2');R(g,x+9,y+9,3,1,'#d9b24a');R(g,x+8,y+1,6,2,'#2fbf8f')}
function sceneChoice(q,t){const g=wg;blueprintWall(g,t);g.globalAlpha=.6;R(g,0,56,WW,104,'#0a1433');g.globalAlpha=1;const sel=q>=.25?Math.min(2,Math.floor((q-.25)/.9)):-1;
 for(let k=0;k<3;k++){const y=60+k*20,hot=sel==k;R(g,5,y,80,18,hot?MINT:INKC);R(g,6,y+1,78,16,hot?'#1c3a6e':'#14265a');R(g,6,y+1,78,1,'#2c4a8a');R(g,8,y+2,14,14,'#0c1c44');[icoA,icoB,icoC][k](g,8,y+2);
  if(hot){const b=Math.round(Math.sin(t*12));for(let i=0;i<4;i++)R(g,1+b,y+5+i,i<2?i+1:4-i,1,MINT)}}return{}}

const HEADS=[[0.05,VT[0][2][0][1]-.1,"YOU'VE WALKED THROUGH",["THIS DOOR A","HUNDRED TIMES"]],[VT[0][2][0][1]-.1,V(1),"ONE NIGHT",["IT TRAPPED","HUNDREDS"],{tc:CORAL}],
 [V(2)+.02,SEG[2][1],"THE COCOANUT GROVE",["PACKED."]],[SEG[3][0]+.02,V(3),"ITS MAIN ENTRANCE",["ONE REVOLVING","DOOR"]],
 [V(3)+.02,SEG[4][1],"FIRE",["THE CROWD","RUSHES THE DOOR"],{tc:CORAL}],[SEG[5][0]+.02,V(4),"THE DOOR",["JAMMED."],{tc:CORAL}],[V(4)+.02,V(5),"NOVEMBER 28, 1942",["492 DIED."],{tc:CORAL}],
 [V(5)+.02,V(5)+1.5,"YOU WRITE",["THE FIRE CODE"]],[V(5)+1.5,V(6),"THREE OPTIONS",["WHICH ONE?"],{tc:AMBER}],
 [V(6)+.02,V(8),"OPTION A",["BAN REVOLVING","DOORS"],{tc:AMBER}],[V(8)+.02,V(10),"OPTION B",["MAKE THE WINGS","FOLD FLAT"],{tc:AMBER}],[V(10)+.02,MENU0,"OPTION C",["ADD A NORMAL","DOOR BESIDE IT"],{tc:AMBER}],
 [V(12)+.02,SEG[12][1],"PLAY OUT A",["NOT WHAT","THEY PICKED"],{tc:CORAL}],[SEG[13][0]+.02,V(13),"BUILT TO KEEP OUT",["WIND AND SNOW.","IT STAYED."]],
 [V(13)+.02,V(14),"PLAY OUT B",["RIGHT.","WINGS COLLAPSE"],{tc:MINT}],[V(14)+.02,V(15),"PLAY OUT C",["RIGHT TOO.","THE CODE TOOK BOTH"],{tc:MINT}],
 [V(15)+.02,SEG[16][1],"B OR C?",["YOU CLEARED IT"],{tc:MINT}],[SEG[17][0]+.02,V(16),"RULE UNLOCKED",["A SWING DOOR","BESIDE EVERY ONE"],{tc:MINT}],[V(16)+.04,END,"LEVEL 04",["CLEARED"],{tc:MINT}]];
function heart(x,y,full){og.fillStyle=full?CORAL:'#3a3668';const u=7;[[1,0,2,1],[4,0,2,1],[0,1,7,2],[1,3,5,1],[2,4,3,1],[3,5,1,1]].forEach(([a,b,w,h])=>og.fillRect(x+a*u,y+b*u,w*u,h*u))}
function badge(L,t0,t){const a=ease(seg(t,t0,t0+.18));if(a<=0)return;const p=1+.35*(1-a);og.save();og.translate(150,830);og.scale(p,p);og.globalAlpha=a;og.fillStyle=INKC;rrect(og,-78,-78,156,156,24);og.fill();og.fillStyle=AMBER;rrect(og,-66,-66,132,132,18);og.fill();mdraw(L,0,6,110,INKC,'center',false,'',0,a);og.restore()}
const TA=VT[12][2][0][0]-.3;
function hud(t){const DONE=V(16),done=t>=DONE,pr=cl01(t/DONE),y=566,s=84,gap=18,x0=250,a=ease(seg(t,V(1),V(1)+.35));if(a<=0)return;og.save();og.globalAlpha=a;
 mdraw("LV 4",60,y+s/2+2,40,MINT,'left',false,'',0,a);
 for(let i=0;i<5;i++){const x=x0+i*(s+gap),ok=i<3||(i==3&&done),cur=i==3&&!done;og.globalAlpha=a;og.fillStyle=ok?'#173a2c':'#1b1838';rrect(og,x,y,s,s,12);og.fill();
  if(cur){og.save();rrect(og,x,y,s,s,12);og.clip();og.fillStyle='#2a4a7a';og.fillRect(x,y+s*(1-pr),s,s*pr);og.restore()}
  const nxt=i==4&&t>VT[16][1]-1.6;og.lineWidth=4;og.strokeStyle=ok?MINT:cur?CORAL:(nxt&&Math.sin(t*10)>0?AMBER:'#3a3668');rrect(og,x,y,s,s,12);og.stroke();
  if(ok){og.strokeStyle=MINT;og.lineWidth=9;og.lineCap='round';og.beginPath();og.moveTo(x+22,y+44);og.lineTo(x+37,y+59);og.lineTo(x+63,y+27);og.stroke()}
  else mdraw(cur?"04":"?",x+s/2,y+s/2+2,cur?34:38,cur?CREAM:(nxt?AMBER:'#5a568a'),'center',false,'',0,a)}
 const lives=t<TA?3:2;for(let i=0;i<3;i++)heart(800+i*76,y+20,i<lives);og.restore()}
function frameAt(t){
 QA.chars=[];QA.solids=[];og.imageSmoothingEnabled=false;og.clearRect(0,0,1080,1920);
 const sg=SEG.find(s=>t>=s[0]&&t<s[1])||SEG[SEG.length-1],id=sg[2],o=t-sg[0];QA.shot=sg[3];let sh=0,inf={};
 ({lobby:()=>sceneLobby(o,t,false),rewind:()=>sceneRewind(o,t),club:()=>sceneClub(o,t),spin:()=>sceneSpin(o,t),rush:()=>sceneRush(o,t),jam:()=>sceneJam(o,t),face1:()=>sceneFace(o,t,1),ask:()=>sceneAsk(o,t),
  pA:()=>scenePA(o,t,false),pB:()=>scenePB(o,t,false),pC:()=>scenePC(o,t),choice:()=>sceneChoice(o,t),A1:()=>scenePA(o+2.2,t,false),A:()=>sceneWinter(o,t),B:()=>scenePB(o,t,true),C:()=>{inf=sceneC(o,t)},
  face2:()=>sceneFace(o,t,2),lobby2:()=>sceneLobby(o+2,t,true),win:()=>sceneWin(36.36+o)})[id]();
 if(id=='jam')sh=shake(t,sg[0]+.5);if(id=='A1')sh=shake(t,TA);
 og.drawImage(wc,0,0,WW,WH,sh,0,1080,1920);
 lit(()=>{const f=.6+.4*Math.sin(t*9)*Math.sin(t*5.3);
  if(id=='lobby'||id=='lobby2'||id=='pA'||id=='pC'||id=='A1')glow(900,760,640,SUN,.24);
  else if(id=='rewind'||id=='ask'||id=='choice')glow(540,1300,700,COOL,.14);
  else if(id=='club'){glow(540,760,420,RED,.2);glow(540,1250,380,WARM,.2)}
  else if(id=='rush'){glow(540,1150,620,FIRE,.4+.15*f);grade('#6a3a3a',.25,'multiply')}
  else if(id=='jam'){glow(540,1500,700,FIRE,.22+.1*f)}
  else if(id=='face1'){glow(820,1000,520,FIRE,.22+.08*f);grade('#3a3050',.25,'multiply')}
  else if(id=='A'){glow(800,1000,480,WARM,.3);glow(220,1000,480,COOL,.2)}
  else if(id=='C'){glow(960,900,520,SUN,.2+.2*(inf.u||0))}
  else if(id=='face2')glow(820,900,560,SUN,.3);
  else if(id=='win')glow(70*12,66*12,520,SUN,.45);
  else glow(540,1100,760,COOL,.12)});
 const v=og.createLinearGradient(0,0,0,1920);v.addColorStop(0,'rgba(0,0,0,.22)');v.addColorStop(.3,'rgba(0,0,0,0)');v.addColorStop(.8,'rgba(0,0,0,0)');v.addColorStop(1,'rgba(0,0,0,.35)');og.fillStyle=v;og.fillRect(0,0,1080,1920);
 og.globalAlpha=.6;og.fillStyle='#0f0d22';og.fillRect(0,110,1080,562);og.globalAlpha=1;
 const h=HEADS.find(h=>t>=h[0]&&t<h[1]);
 if(id=='rewind'){const t0=VT[1][2][0]?VT[1][2][0][1]:V(1)+1,yr=Math.round(lerp(2026,1942,ease(seg(t,t0,t0+1.1))));header(t<t0?"LEVEL 04":"BOSTON",[t<t0?"THE REVOLVING DOOR":String(yr)],(t-V(1))/.2,{tc:t>t0+1.1||t<t0?AMBER:CREAM})}
 else if(id=='choice'){const q=t-MENU0,n=3-Math.min(2,Math.floor(Math.max(0,q-.25)/.9)),p=1+.25*(1-ease(seg(((Math.max(0,q-.25))%.9),0,.2)));header("LOCK IT IN",[],1);og.save();og.translate(540,330);og.scale(p,p);mdraw(String(n),0,0,220,AMBER,'center',true,INKC,20,1);og.restore()}
 else if(h)header(h[2],h[3],(t-h[0])/.2,h[4]);
 hud(t);
 if(id=='pA')badge("A",VT[6][0]+.45,t);if(id=='pB')badge("B",VT[8][0]+.45,t);if(id=='pC')badge("C",VT[10][0]+.45,t);
 if(id=='A1'||id=='A')badge("A",V(12)+.05,t);if(id=='B')badge("B",V(13)+.05,t);if(id=='C')badge("C",V(14)+.05,t);
 if(id=='jam'&&o>.5)stamp("JAMMED",'#e0473c',540,900,sg[0]+.5,t,-.07,64);
 if(id=='choice'){const L=[["A","BAN REVOLVING DOORS"],["B","WINGS THAT FOLD FLAT"],["C","A NORMAL DOOR BESIDE IT"]];
  L.forEach(([a,s],k)=>{const y=(69+k*20)*12;mdraw(a,26.5*12,y+2,56,AMBER,'center',true,INKC,10,1);mdraw(s,31*12,y+2,fit(s,40,600),CREAM,'left',false,'',0,1)})}
 if((id=='A1'||id=='A')&&t>=TA)stamp("NOT PICKED",'#e0473c',540,1300,TA,t,-.07,56);
 if(id=='B'&&o>1.4)stamp("B IS RIGHT",'#2fbf8f',540,1330,sg[0]+1.4,t,-.07,56);
 if(id=='C'&&o>1.6)stamp("C IS RIGHT TOO",'#2fbf8f',420,1010,sg[0]+1.6,t,-.07,46);
 if(id=='win'){const w0=V(16);const xp=Math.round(100*ease(seg(t,w0+.2,w0+.9)));mdraw("+"+xp+" XP",540,800,70,AMBER,'center',true,INKC,14,1);
  const c0=VT[16][2][0]?VT[16][2][0][1]:w0+1;if(t>c0&&t<c0+1.2)tag("COMMENT A, B OR C",540,1400,AMBER,ease(seg(t,c0,c0+.15)));if(t>=c0+1.2)tag("FOLLOW FOR LEVEL 05",540,1400,MINT,ease(seg(t,c0+1.2,c0+1.37)))}
 subtitle(t,false);for(const c of CUTS)wipe(t,c,.12);
}
window.frame=i=>frameAt(i/30);
Promise.all([document.fonts.load('700 40px Silk'),document.fonts.load('400 40px PS2P')]).then(()=>{window.READY=true});
