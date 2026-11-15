// ===== Level 05 : Elisha Otis — "All safe, gentlemen" (Crystal Palace, 1854) =====
// Voice: voice_t.wav (trimmed intro+body, 138.98s). Video END=141.0 (2s CTA tail).
const END=141.0,VEND=138.98;

const SUBS=[
 [1.89,3.31,"You're standing in a crowd."],
 [3.69,8.74,"There's a man on a wooden platform thirty feet in the air. One rope holding him up."],
 [9.24,14.41,"He looks down at everyone watching. Then he nods. And someone cuts the rope."],
 [15.31,17.40,"New York. 1854."],
 [17.63,19.22,"Crystal Palace Exhibition."],
 [19.86,22.70,"Elisha Otis didn't invent the elevator."],
 [23.20,25.64,"Hoists had existed for centuries."],
 [26.15,33.94,"The problem was ropes break. And when they did, the platform fell. Fast. All the way down."],
 [34.39,37.07,"So buildings couldn't go higher than four or five floors."],
 [37.39,40.61,"If the stairs were too far, people just didn't go up."],
 [41.21,46.44,"Otis invented something different. A safety brake."],
 [46.94,49.12,"While the rope is taut, it holds back two spring-loaded arms."],
 [49.62,56.61,"The second the rope goes slack, they snap outward. Lock into a toothed rail in the shaft wall."],
 [57.16,59.28,"Platform stops. Instantly."],
 [59.64,61.60,"No power needed. No operator."],
 [61.99,63.61,"Physics does the work."],
 [64.04,70.21,"But nobody believed it. So he put himself on a platform, in front of a crowd, and told someone to cut the rope."],
 [71.81,76.36,"The platform dropped a few inches... and stopped."],
 [76.80,81.14,"He took off his hat and said: All safe, gentlemen. All safe."],
 [81.74,83.25,"Here's what I want you to think about."],
 [83.77,86.69,"That moment changed what cities could look like."],
 [87.08,90.11,"Before Otis, the top floor was worthless."],
 [90.55,92.12,"Nobody wanted to climb that high."],
 [92.58,97.17,"After Otis, the penthouse became the most valuable address in the building."],
 [97.67,99.60,"But the question isn't about elevators."],
 [100.10,102.11,"You're writing the building code. Right now."],
 [102.61,106.88,"In 1854, a rope just broke on a passenger elevator."],
 [107.36,108.29,"Someone is hurt."],
 [108.73,110.05,"How do you respond?"],
 [110.55,117.06,"Option A: Ban passenger elevators entirely. Freight only. Too dangerous for people."],
 [117.66,125.71,"Option B: Require a trained human operator in every elevator car, at all times."],
 [126.31,134.91,"Option C: Require every elevator to have an automatic safety device that stops the car with no human input."],
 [137.31,138.30,"Lock it in."],
];

// scene boundaries (trimmed timeline)
const SEG=[
 [0,     3.50, 'crowd',   'back'],
 [3.50,  9.20, 'platform','wide'],
 [9.20, 12.20, 'nod',     'closeup'],
 [12.20, 14.90,'axe',     'detail'],
 [14.90, 23.20,'palace',  'front'],
 [23.20, 26.15,'hoist',   'side'],
 [26.15, 34.39,'fall',    'side'],
 [34.39, 41.21,'lowcity', 'wide'],
 [41.21, 49.62,'brakediag','elevation'],
 [49.62, 57.16,'snapdiag','detail'],
 [57.16, 64.04,'physics', 'front'],
 [64.04, 70.21,'demo',    'wide'],
 [70.21, 71.81,'drop',    'closeup'],
 [71.81, 76.80,'caught',  'side'],
 [76.80, 81.74,'hat',     'closeup'],
 [81.74, 83.77,'think',   'front'],
 [83.77, 92.58,'value',   'elevation'],
 [92.58, 97.67,'penthouse','elevation'],
 [97.67,102.61,'desk',    'plan'],
 [102.61,108.73,'accident','side'],
 [108.73,110.55,'ask',    'front'],
 [110.55,END,  'choice',  'menu'],
];
const CUTS=SEG.slice(1).map(s=>s[0]);
const TA=110.55,TB=117.66,TC=126.31,CDN=134.91,LOCK=137.31; // option reveals, countdown, lock

LOOK.otis={id:'otis',skin:'#e9c3a3',skinD:'#c99d7e',hair:'#3a2a20',top:'#4a3a56',topL:'#685878',pants:'#2a2a34',shoe:'#121016'};
const RPC='#c8b48a',WOOD='#8a7a60',WOODD='#6a5a48',IRON='#4a4458';

// small Otis for wide shots — stands on the high plank
function otisMan(g,x,y,t,pose){ // feet at (x,y); pose: 0 stand, 1 wave, 2 arms up
 const b=Math.sin(t*2.2)>.5?-1:0;
 g.globalAlpha=.25;R(g,x-3,y,8,1,'#000');g.globalAlpha=1;
 R(g,x-1,y-5,2,5,'#2a2a34');R(g,x+1,y-5,2,5,'#2a2a34');        // legs
 R(g,x-2,y-11,6,6,'#4a3a56');R(g,x-2,y-11,6,1,'#685878');      // coat
 if(pose==2){R(g,x-4,y-14,2,4,'#4a3a56');R(g,x+4,y-14,2,4,'#4a3a56');R(g,x-4,y-15,2,2,'#e9c3a3');R(g,x+4,y-15,2,2,'#e9c3a3')}
 else if(pose==1){R(g,x+4,y-12,2,3,'#4a3a56');R(g,x+4,y-13,2,2,'#e9c3a3');R(g,x-3,y-10,1,4,'#4a3a56')}
 else{R(g,x-3,y-10,1,4,'#4a3a56');R(g,x+4,y-10,1,4,'#4a3a56')}
 R(g,x-1,y-15+b,4,4,'#e9c3a3');px(g,x,y-13+b,'#3a2a20');        // head + stache hint
 R(g,x-2,y-17+b,6,2,'#2a2430');R(g,x-3,y-15+b,8,1,'#2a2430');   // top hat
 R(g,x-2,y-19+b,6,2,'#2a2430');
}
function box(g,x,y,w,h,c){R(g,x,y,w,1,c);R(g,x,y+h-1,w,1,c);R(g,x,y,1,h,c);R(g,x+w-1,y,1,h,c)}

// ---- Crystal Palace hall: iron arches, warm gaslight, crowd ----
function hall(g,t,dim){
 R(g,0,0,WW,56,NAVY);
 for(let y=56;y<FL;y++)R(g,0,y,WW,1,mixc('#3a2f4e','#241c36',(y-56)/64*(1-(dim||0)*.0)+ (dim||0)*.2>1?1:(y-56)/64));
 // arched windows along the back wall
 for(let k=0;k<4;k++){const x=4+k*22;
  R(g,x,60,14,26,IRON);R(g,x+1,61,12,24,'#2a3652');
  for(let i=0;i<12;i++){const hh=Math.round(Math.sqrt(36-(i-6)*(i-6)));R(g,x+1+i,61+6-hh,1,hh,'#2a3652')}
  R(g,x+1,61,12,2,'#44588a');R(g,x+6,61,1,24,IRON);R(g,x+1,72,12,1,IRON);
  const fl=.5+.5*Math.sin(t*7+k*2);px(g,x+3,66+Math.round(fl),'#ffd98a');px(g,x+9,66,'#f0c070');}
 // gas lamps between windows
 for(const x of[22,44,66]){R(g,x,78,1,8,'#1e1a28');R(g,x-1,76,3,3,'#1e1a28');px(g,x,77,'#ffd98a');
  g.globalAlpha=.12;R(g,x-5,76,11,12,'#ffd98a');g.globalAlpha=1}
 // floor
 for(let y=FL;y<WH;y++)R(g,0,y,WW,1,(y-FL)%7==0?'#3a3048':'#4a3f5c');
 for(let x=-60;x<WW+60;x+=13)line(g,45+(x-45)*.6,FL,45+(x-45)*1.7,WH,1,'#3a3048');
}
// crowd of tiny onlookers along the floor, facing x=cx
function crowd(g,t,n,y0){
 for(let k=0;k<n;k++){
  const x=4+((k*83)%82),y=(y0||FL)-((k*7)%3),b=Math.sin(t*2+k*1.7)>.6?-1:0;
  const sk=['#e9c3a3','#8a5a3c','#c98b69','#6e4430'][k%4],cl=['#5a4a66','#3f4a6b','#6b4a2e','#4a5a4e','#7a3a44'][k%5];
  R(g,x,y-10+b,4,6,cl);R(g,x,y-4,1,4,'#1e1a28');R(g,x+3,y-4,1,4,'#1e1a28');
  R(g,x+1,y-14+b,3,4,sk);R(g,x,y-16+b,5,3,'#2a2430');  // hat
  g.globalAlpha=.2;R(g,x-1,y,6,1,'#000');g.globalAlpha=1}
}
// platform rig: plank at py with posts and a rope up to the beam
function rig(g,py,ropeTop,slack,sway){
 const sx=sway||0;
 R(g,20,57,50,2,IRON);R(g,20,57,50,1,'#5c5470');       // overhead beam
 if(!slack)R(g,54+sx,59,2,py-59,RPC);                  // taut rope
 else{R(g,54,59,2,6,RPC);R(g,53,65+Math.round(slack),3,3,RPC)} // cut stub
 R(g,24+sx,py,42,3,WOOD);R(g,24+sx,py,42,1,'#a89878');  // plank
 R(g,26+sx,py+3,2,FL-py-3,WOODD);R(g,62+sx,py+3,2,FL-py-3,WOODD); // legs
 line(g,26+sx,py+3,34+sx,py+14,1,WOODD);line(g,64+sx,py+3,56+sx,py+14,1,WOODD); // braces
}
function sceneCrowd(q,t){const g=wg;hall(g,t);
 rig(g,78,59,0,0);
 otisMan(g,45,77,t,0);
 crowd(g,t,10);
 // Kit seen from behind, in the crowd, looking up
 personFB({hip:GY-17,feet:[[-3,0],[3,0]],sl:1,sa:[1,1],hands:[[CX-8,SHY+10+(Math.sin(t*2.6)>.4?1:0)],[CX+8,SHY+10]],hy:Math.sin(t*2.1)>.3?-1:0,nobag:false},-20,0,null,'b');
 return{}}
function scenePlatform(q,t){const g=wg;hall(g,t);
 rig(g,78,59,0,0);
 otisMan(g,45,77,t,q>2.5?1:0);
 crowd(g,t,12);
 R(g,10,79,1,39,'#9a8fb8');R(g,8,79,5,1,'#9a8fb8');R(g,8,118,5,1,'#9a8fb8');
 R(g,4,93,23,9,INKC);ptext(g,'30 FT',6,95,AMBER);
 return{}}
function sceneNod(q,t){const g=wg;hall(g,t,1);
 g.globalAlpha=.5;R(g,0,56,WW,104,'#140f22');g.globalAlpha=1;
 const nod=q>1.6?Math.round(ease(seg(q,1.6,2.0))*3-ease(seg(q,2.2,2.6))*3):0;
 portrait(g,LOOK.otis,{hat:1,stache:1,shirt:1,blink:(t%2.6)<.12,ey:q<1.6?1:0,mouth:'flat',dy:nod});
 return{}}
function sceneAxe(q,t){const g=wg;hall(g,t,1);
 g.globalAlpha=.4;R(g,0,56,WW,104,'#140f22');g.globalAlpha=1;
 // taut rope through frame center, beam above
 R(g,20,58,50,3,IRON);R(g,20,58,50,1,'#5c5470');
 R(g,43,61,4,55,RPC);R(g,43,61,1,55,'#dcc89e');R(g,28,116,38,4,WOOD);R(g,28,116,38,1,'#a89878');
 // the axe rises, starts the swing — freeze before contact
 const lift=ease(seg(q,.2,1.2)),swing=ease(seg(q,1.9,2.7))*.5;
 const ax=Math.round(66-swing*14),ay=Math.round(96-lift*22+swing*6);
 line(g,ax+4,ay+4,ax+16,ay+18,3,'#7a5434');            // handle
 R(g,ax-3,ay-3,10,8,'#9aa2b2');R(g,ax-3,ay-3,10,2,'#c8d0dc');R(g,ax-5,ay-1,2,4,'#c8d0dc'); // head
 // hands gripping the handle
 R(g,ax+10,ay+11,4,4,'#8a5a3c');R(g,ax+14,ay+15,4,4,'#8a5a3c');
 line(g,ax+16,ay+18,90,ay+34,4,'#3a3044');line(g,ax+16,ay+18,90,ay+34,2,'#4a3a56');
 crowd(g,t,8);
 return{}}
function scenePalace(q,t){const g=wg;
 R(g,0,0,WW,56,NAVY);
 for(let y=56;y<FL;y++)R(g,0,y,WW,1,mixc('#2c3a5e','#1a2440',(y-56)/64));
 // Crystal Palace: glass + iron exhibition front with a dome
 for(let i=0;i<30;i++){const hh=Math.round(Math.sqrt(225-(i-15)*(i-15))*.8);R(g,30+i,86-hh,1,hh,'#3a4a74');if(i>1&&i<28)R(g,30+i,87-hh,1,hh-2,'#55699c')}
 px(g,45,73,'#ffd98a');R(g,44,70,2,3,IRON);
 R(g,8,86,74,30,'#3a4a74');R(g,8,86,74,1,'#55699c');
 for(let x=10;x<80;x+=7)for(let y=88;y<114;y+=6){R(g,x,y,5,4,(x+y)%3?'#9cc0e8':'#cfe4f6');R(g,x,y,5,1,'#e4f2fc')}
 for(let x=8;x<84;x+=14)R(g,x,86,2,30,IRON);
 R(g,40,108,10,8,'#2a3652');R(g,40,108,10,1,'#55699c');
 // banner
 R(g,18,60,54,12,INKC);R(g,19,61,52,10,'#6b2f3a');R(g,19,61,52,1,'#8a4a56');
 ptext(g,'CRYSTAL PALACE',23,62,'#f4dc8a');ptext(g,'NEW YORK 1854',25,67,'#e8c070');
 for(let y=FL;y<WH;y++)R(g,0,y,WW,1,(y-FL)%7==0?'#1e2a48':'#26334f');
 for(let x=-60;x<WW+60;x+=13)line(g,45+(x-45)*.6,FL,45+(x-45)*1.7,WH,1,'#1e2a48');
 crowd(g,t,7);
 const br=Math.sin(t*2.4)>.5?-1:0,sh=Math.round(Math.sin(q*6));
 personFB({hip:GY-17,feet:[[-3,0],[3,0]],sl:1,sa:[1,1],hands:[[CX-14,SHY+5+sh],[CX+13,SHY+5+sh]],mouth:'open',hy:br,nobag:false},13,0,null,'f');
 return{}}
// warehouse shaft shared by hoist / fall / caught / accident
function shaft(g,t,o){o=o||{};
 R(g,0,0,WW,56,NAVY);
 for(let y=56;y<FL;y++)R(g,0,y,WW,1,(y-56)%4==0?'#4a3426':'#5e4230');
 for(let r=0;r<16;r++)for(let x=(r%2)*5;x<WW;x+=10)R(g,x,56+r*4,1,4,'#4a3426'); // brick
 // shaft opening
 R(g,26,56,38,64,'#17121f');R(g,25,56,1,64,'#2a2230');R(g,64,56,1,64,'#2a2230');
 // guide rails
 R(g,28,56,3,64,o.rail||'#6a6478');R(g,59,56,3,64,o.rail||'#6a6478');
 if(o.teeth)for(let y=58;y<118;y+=4){R(g,31,y,2,2,'#c9a24a');R(g,57,y,2,2,'#c9a24a')}
 // crates stacked beside
 R(g,4,104,16,16,'#8a6a40');R(g,4,104,16,2,'#a8854e');R(g,8,109,8,3,'#6a4e2c');
 R(g,70,96,15,24,'#8a6a40');R(g,70,96,15,2,'#a8854e');R(g,74,104,8,3,'#6a4e2c');
 for(let y=FL;y<WH;y++)R(g,0,y,WW,1,(y-FL)%6==0?'#2a2018':'#36291c');
 for(let x=-60;x<WW+60;x+=13)line(g,45+(x-45)*.6,FL,45+(x-45)*1.7,WH,1,'#2a2018');
}
function cab(g,y,o){o=o||{};                            // hoist platform + cargo
 R(g,30,y,30,3,WOOD);R(g,30,y,30,1,'#a89878');
 if(!o.empty){R(g,34,y-8,9,8,'#c9a24a');R(g,34,y-8,9,1,'#e0bc60');R(g,47,y-6,8,6,'#8a9aa8');R(g,47,y-6,8,1,'#aebccc')}
}
function sceneHoist(q,t){const g=wg;shaft(g,t);
 const py=Math.round(96-Math.sin(q*.9)*8);
 R(g,44,56,2,py-56,RPC);
 cab(g,py);
 // worker hauling at the side
 const pull=Math.round(Math.sin(t*4)*2);
 personFB({hip:GY-17,feet:[[-3,0],[3,0]],sl:1,sa:[1,1],hands:[[CX-10,SHY-2+pull],[CX-6,SHY+6+pull]],hy:0,nobag:true},-22,0,LOOK.a1,'f');
 return{}}
function sceneFall(q,t){const g=wg;shaft(g,t);
 const snapT=1.35,sn=q>=snapT;
 if(!sn){                                               // fraying
  const fr=Math.round(Math.sin(t*26)*1);
  R(g,44+fr,56,2,16,RPC);R(g,44,72,2,8,RPC);
  for(let k=0;k<3;k++)px(g,43+((k*3+Math.floor(t*10))%5),70+k,'#dcc89e');
  cab(g,80);
 }else{
  R(g,44,56,2,7+Math.round(Math.sin(t*9)*2),RPC);      // stub whips
  const fy=Math.round(lerp(80,116,ease(seg(q,snapT,snapT+.9))));
  cab(g,fy);
  if(q>snapT+.35){const k1=ease(seg(q,snapT+.35,snapT+1.0));
   R(g,36,Math.round(lerp(72,114,k1)),9,8,'#c9a24a');R(g,49,Math.round(lerp(74,112,k1*1.05>1?1:k1*1.05)),8,6,'#8a9aa8')}
  if(q>snapT+.8){const du=cl01((q-snapT-.8)/1.2);       // dust
   g.globalAlpha=.5*(1-du);for(let k=0;k<7;k++)R(g,30+k*5,114-du*12-(k%3)*3,4,3,'#7a6a56');g.globalAlpha=1}
 }
 return{sn}}
function sceneLowcity(q,t){const g=wg;
 R(g,0,0,WW,56,NAVY);
 for(let y=56;y<FL;y++)R(g,0,y,WW,1,mixc('#35406a','#222c4e',(y-56)/64));
 for(let k=0;k<14;k++)px(g,(k*41)%WW,58+(k*13)%18,'#cfd6ff');
 // squat 1850s blocks, none above the cap line
 const CAP=78;
 g.globalAlpha=.5;for(let x=0;x<WW;x+=6)R(g,x,CAP,3,1,'#e0837a');g.globalAlpha=1; // dashed height cap
 ptext(g,'5 FLOORS',52,72,'#e0837a');
 const B=[[2,16,'#5a4a66'],[20,20,'#6b4a2e'],[42,18,'#4a5a4e'],[62,14,'#5a4a66'],[78,12,'#6b4a2e']];
 B.forEach(([x,w,c],i)=>{const h=34+(i%3)*4,y0=FL-h;
  R(g,x,y0,w,h,c);R(g,x,y0,w,1,shade(c,1.3));
  for(let fy=y0+3;fy<FL-4;fy+=7)for(let fx=x+2;fx<x+w-2;fx+=5)R(g,fx,fy,3,4,(fx+fy)%3?'#f0d890':'#2a2430');});
 for(let y=FL;y<WH;y++)R(g,0,y,WW,1,(y-FL)%7==0?'#262038':'#302a44');
 // stairs up the side of one block; a walker turns back
 for(let k=0;k<5;k++)R(g,44+k*3,FL-3-k*3,3,3,'#3a3048');
 const back=q>3.2,wx=back?Math.round(27-(q-3.2)*7):Math.round(8+Math.min(q,3.2)*6);
 kitp(walkP(wx+10),wx,0,back);
 return{}}
// ---- the brake, drawn as a blueprint ----
function brakeDraw(g,cx,cy,u,slack){
 // u: 0 arms held in, 1 arms snapped out
 R(g,cx-20,58,4,58,'#4a6a9a');R(g,cx+16,58,4,58,'#4a6a9a');   // rails
 for(let y=60;y<114;y+=4){R(g,cx-16,y,2,2,'#f3c969');R(g,cx+14,y,2,2,'#f3c969')} // teeth
 if(!slack){R(g,cx-1,58,2,cy-10-58,RPC)}                      // taut rope
 else{R(g,cx-1,58,2,8,RPC);R(g,cx-2,67,4,3,RPC)}             // cut stub
 R(g,cx-12,cy-10,24,18,'#5f8fb0');R(g,cx-11,cy-9,22,16,INKC);  // car
 R(g,cx-11,cy-9,22,1,'#2c4a8a');
 // spring across the top of the car
 R(g,cx-8,cy-7,16,2,'#aab8d0');for(let k=0;k<8;k++)px(g,cx-8+k*2,cy-8+(k%2),'#f3c969');
 // the two arms
 const a=Math.round(u*6);
 line(g,cx-6,cy-5,cx-14-a,cy-2,2,u>0?'#5ee08a':'#9fc3ff');
 line(g,cx+6,cy-5,cx+14+a,cy-2,2,u>0?'#5ee08a':'#9fc3ff');
 if(u>0){R(g,cx-18,cy-3,3,3,'#5ee08a');R(g,cx+15,cy-3,3,3,'#5ee08a')}
}
function sceneBrakediag(q,t){const g=wg;blueprintWall(g,t);
 brakeDraw(g,45,92,0,false);
 // labels in clear space
 ptext(g,'RAIL',4,60,'#9fc3ff');line(g,20,62,25,62,1,'#9fc3ff');
 ptext(g,'ROPE',66,60,'#f3c969');line(g,64,62,47,62,1,'#f3c969');
 if(q>5.7){ptext(g,'SPRING',4,108,'#5ee08a');line(g,28,110,36,104,1,'#5ee08a');
  ptext(g,'ARMS',70,108,'#5ee08a');line(g,68,110,56,104,1,'#5ee08a')}
 return{}}
function sceneSnapdiag(q,t){const g=wg;blueprintWall(g,t);
 const u=ease(seg(q,.9,1.25));
 brakeDraw(g,45,92+Math.round((1-u)*(q<.9?Math.sin(t*30)*0:0)),u,q>.55);
 if(u>=1){ptext(g,'LOCKED',33,110,'#5ee08a');box(g,31,108,28,9,'#5ee08a')}
 return{}}
function scenePhysics(q,t){const g=wg;blueprintWall(g,t);
 brakeDraw(g,66,92,1,true);
 const chips=[['NO POWER',0],['NO OPERATOR',2.48],['PHYSICS',4.83]];
 chips.forEach(([s,at],k)=>{if(q<at)return;const a=ease(seg(q,at,at+.2)),y=62+k*13;
  g.globalAlpha=a;R(g,3,y,s.length*4+6,11,INKC);R(g,4,y+1,s.length*4+4,9,'#14265a');R(g,4,y+1,s.length*4+4,1,'#2c4a8a');
  ptext(g,s,6,y+3,k<2?'#9fc3ff':'#5ee08a');check(g,s.length*4+2,y+5,MINT);g.globalAlpha=1});
 const br=Math.sin(t*2.4)>.5?-1:0;
 personFB({hip:GY-17,feet:[[-3,0],[3,0]],sl:1,sa:[1,1],hands:[[CX-14,SHY+5+(Math.sin(t*3.1)>.3?1:0)],[CX+13,SHY-2]],mouth:'open',hy:br,nobag:false},-14,0,null,'f');
 return{}}
function sceneDemo(q,t){const g=wg;hall(g,t);
 rig(g,78,59,0,0);
 otisMan(g,42,77,t,2);
 crowd(g,t,12);
 // assistant on a ladder beside the rope, axe ready
 R(g,66,70,2,50,'#6a5a48');R(g,72,70,2,50,'#6a5a48');
 for(let y=74;y<118;y+=6)R(g,66,y,8,2,'#8a7a60');
 const raise=ease(seg(q,4.6,5.6));
 R(g,68,68,2,6,'#2a2a34');R(g,67,63,4,5,'#5a3a2c');R(g,67,60,4,4,'#c98b69');
 line(g,66,64,59-raise*3,60-raise*4,2,'#7a5434');
 R(g,56-raise*3,57-raise*4,6,4,'#9aa2b2');
 return{}}
function sceneDrop(q,t){const g=wg;hall(g,t,1);
 g.globalAlpha=.4;R(g,0,56,WW,104,'#140f22');g.globalAlpha=1;
 // rope cut close-up: stub whips, platform edge slides down and bites
 R(g,20,58,50,3,IRON);
 R(g,56,61,3,8+Math.round(Math.sin(t*22)*3),RPC);
 const dy=Math.round(ease(seg(q,.15,.8))*6);
 R(g,18,62,3,56,'#6a6478');R(g,69,62,3,56,'#6a6478');
 for(let y=64;y<116;y+=4){R(g,21,y,2,2,'#c9a24a');R(g,67,y,2,2,'#c9a24a')}
 R(g,24,96+dy,42,4,WOOD);R(g,24,96+dy,42,1,'#a89878');
 line(g,30,98+dy,21,102+dy,2,'#5ee08a');line(g,60,98+dy,69,102+dy,2,'#5ee08a');
 personFB({hip:GY-17,feet:[[-3,0],[3,0]],sl:1,sa:[1,1],hands:[[CX-8,SHY+10],[CX+8,SHY+10]],hy:0,nobag:true},13,24-dy,LOOK.otis,'f');
 return{}}
function sceneCaught(q,t){const g=wg;shaft(g,t,{teeth:1,rail:'#6a6478'});
 R(g,44,56,2,8,RPC);R(g,43,65,4,3,RPC);               // cut stub
 cab(g,96,{empty:1});
 // Otis stands on it, steady
 personFB({hip:GY-17,feet:[[-3,0],[3,0]],sl:1,sa:[1,1],hands:[[CX-8,SHY+10+(Math.sin(t*2.8)>.5?1:0)],[CX+8,SHY+10]],hy:Math.sin(t*2.3)>.4?-1:0,nobag:true},13,24,LOOK.otis,'f');
 // arms biting the rails
 line(g,36,98,30,102,2,'#5ee08a');line(g,54,98,60,102,2,'#5ee08a');
 R(g,28,100,4,4,'#5ee08a');R(g,58,100,4,4,'#5ee08a');
 // settling dust
 if(q<1.6){g.globalAlpha=.35*(1-q/1.6);for(let k=0;k<6;k++)R(g,32+k*5,112-(k%3)*4-q*6,3,2,'#7a6a56');g.globalAlpha=1}
 crowd(g,t,9);
 return{}}
function sceneHat(q,t){const g=wg;hall(g,t,1);
 g.globalAlpha=.35;R(g,0,56,WW,104,'#140f22');g.globalAlpha=1;
 const up=ease(seg(q,.6,1.3));
 portrait(g,LOOK.otis,{hat:up<.5?1:0,stache:1,shirt:1,blink:(t%2.6)<.12,mouth:'smile',dy:Math.sin(t*2.2)>.4?1:0});
 if(up>=.5){const hx=70,hhy=Math.round(84-up*12);   // hat raised beside him
  R(g,hx-6,hhy,22,9,'#2a2430');R(g,hx-6,hhy,22,2,'#423a4c');R(g,hx-10,hhy+7,30,3,'#2a2430');}
 return{}}
function sceneThink(q,t){const g=wg;blueprintWall(g,t);
 const br=Math.sin(t*2.4)>.5?-1:0;
 personFB({hip:GY-17,feet:[[-3,0],[3,0]],sl:1,sa:[1,1],hands:[[CX-14,SHY+5+(Math.sin(t*3.2)>.3?1:0)],[CX+13,SHY-4]],mouth:'open',hy:br,nobag:false},13,0,null,'f');
 return{}}
// building cross-section: six floors, value flips top-to-bottom
function sceneValue(q,t,after){const g=wg;
 R(g,0,0,WW,56,NAVY);
 for(let y=56;y<FL;y++)R(g,0,y,WW,1,mixc('#35406a','#222c4e',(y-56)/64));
 for(let k=0;k<10;k++)px(g,(k*37)%WW,58+(k*11)%16,'#cfd6ff');
 const x0=22,wB=46,fh=10,top=58;
 R(g,x0-2,top-2,wB+4,fh*6+4,INKC);
 for(let f=0;f<6;f++){const y=top+f*fh;
  const prized=after?f==0:f>=4;        // before: only low floors valued; after: penthouse
  const colr=prized?'#8a6a2a':'#3a3448';
  R(g,x0,y,wB,fh-1,colr);R(g,x0,y,wB,1,shade(colr,1.3));
  for(let wx=x0+3;wx<x0+wB-3;wx+=7)R(g,wx,y+3,4,4,prized?'#ffd98a':'#242030');
  if(after&&f==0){box(g,x0-1,y-1,wB+2,fh+1,AMBER);
   const tw=Math.sin(t*6)>0;if(tw)px(g,x0+wB+3,y+2,AMBER);px(g,x0-4,y+4,AMBER)}
 }
 if(after){R(g,2,top,30,9,INKC);ptext(g,'PRIZED',4,top+2,AMBER)}else ptext(g,'EMPTY',68,top+2,'#8a84a0');
 ptext(g,after?'':'FULL',x0+wB+4,top+46,'#9fc3ff');
 if(after)ptext(g,'$',x0+8,top+3,'#ffd98a');
 for(let y=FL;y<WH;y++)R(g,0,y,WW,1,(y-FL)%7==0?'#262038':'#302a44');
 for(let x=-60;x<WW+60;x+=13)line(g,45+(x-45)*.6,FL,45+(x-45)*1.7,WH,1,'#262038');
 const br=Math.sin(t*2.4)>.5?-1:0;
 personFB({hip:GY-17,feet:[[-3,0],[3,0]],sl:1,sa:[1,1],hands:[[CX-10,SHY+8+(Math.sin(t*3.0)>.3?1:0)],[CX+12,SHY-6+(after?-2:6)]],mouth:'open',hy:br,nobag:false},-18,0,null,'f');
 return{}}
function sceneDesk(q,t){const g=wg;R(g,0,0,WW,56,NAVY);
 // top-down drafting desk
 for(let y=56;y<WH;y++)R(g,0,y,WW,1,((y-56)%13==0)?'#5a3e28':(((y-56)/13|0)%2?'#8a6640':'#916c44'));
 g.globalAlpha=.3;R(g,12,64,62,56,'#1a1008');g.globalAlpha=1;
 R(g,10,61,62,56,'#efe6d0');R(g,10,61,62,1,'#fffaf0');
 for(const[a,b]of[[11,62],[69,62],[11,114],[69,114]])R(g,a,b,2,2,'#c43c3c');
 ptext(g,'BUILDING',20,66,'#2f4a7a');ptext(g,'CODE 1854',20,72,'#2f4a7a');
 R(g,14,80,54,1,'#a9a090');
 const lines=Math.min(5,Math.floor(q/1.0)+1);
 for(let k=0;k<lines;k++){const wln=k==lines-1?Math.round(((q%1.0))*44):44;R(g,16,86+k*5,Math.min(44,wln+8),1,'#2f4a7a')}
 // hand with pen at the writing point
 const hx=16+Math.min(44,Math.round(((q%1.0))*44)),hy=86+(lines-1)*5;
 R(g,hx-2,hy-2,5,5,INKC);R(g,hx-1,hy-1,3,3,'#c98b69');line(g,hx,hy,hx+4,hy+5,1,'#e0b24a');
 // inkwell
 R(g,74,66,8,8,INKC);R(g,75,67,6,6,'#14265a');px(g,77,66,'#9a9aa6');
 return{}}
function sceneAccident(q,t){const g=wg;shaft(g,t);
 R(g,44,56,2,10+Math.round(Math.sin(t*7)*2),RPC);
 // wrecked platform at the bottom
 R(g,28,112,16,3,WOOD);R(g,47,114,14,3,WOOD);line(g,42,110,48,116,2,WOODD);
 R(g,34,104,9,8,'#c9a24a');R(g,50,108,8,5,'#8a9aa8');
 // warning lamp
 const fl=Math.sin(t*8)>0;R(g,8,60,10,10,INKC);R(g,9,61,8,8,fl?'#e04040':'#5a2020');
 crowd(g,t,6,FL);
 return{}}
function sceneAsk(q,t){const g=wg;blueprintWall(g,t);
 const br=Math.sin(t*2.4)>.5?-1:0,sh=Math.round(Math.sin(q*6));
 personFB({hip:GY-17,feet:[[-3,0],[3,0]],sl:1,sa:[1,1],hands:[[CX-14,SHY+5+sh],[CX+13,SHY+5+sh]],mouth:'open',hy:br,nobag:false},13,0,null,'f');
 [[14,70,.3],[38,62,.7],[62,70,1.1]].forEach(([x,y,a],k)=>{if(q<a)return;const b=Math.round(Math.sin(t*5+k));
  R(g,x,y+b,14,13,INKC);R(g,x+1,y+1+b,12,11,'#14265a');ptext(g,'ABC'[k],x+6,y+4+b,AMBER)});
 return{}}
function icoBan(g,x,y){R(g,x+4,y+3,6,8,'#9fc3ff');R(g,x+6,y+5,2,2,INKC);
 for(let d=0;d<360;d+=24)px(g,x+7+Math.cos(d*Math.PI/180)*6,y+7+Math.sin(d*Math.PI/180)*6,'#e05a4a');
 line(g,x+2,y+2,x+12,y+12,1,'#e05a4a')}
function icoOp(g,x,y){R(g,x+5,y+1,4,4,'#e9c3a3');R(g,x+4,y+5,6,6,'#3f8fb0');
 R(g,x+3,y+11,2,3,'#2a2a34');R(g,x+9,y+11,2,3,'#2a2a34');R(g,x+10,y+4,3,2,'#f3c969')}
function icoAuto(g,x,y){R(g,x+5,y+2,4,8,'#9fc3ff');
 line(g,x+5,y+6,x+1,y+9,2,'#5ee08a');line(g,x+9,y+6,x+13,y+9,2,'#5ee08a');
 R(g,x+1,y+3,1,8,'#f3c969');R(g,x+12,y+3,1,8,'#f3c969')}
function sceneChoice(q,t){const g=wg;blueprintWall(g,t);
 g.globalAlpha=.6;R(g,0,56,WW,104,'#0a1433');g.globalAlpha=1;
 const at=[0,TB-TA,TC-TA];
 const allhot=(t>=LOCK)&&Math.sin(t*6)>.2;               // after lock: all pulse together, none singled out
 for(let k=0;k<3;k++){
  const y=60+k*20,on=q>=at[k];
  if(!on){g.globalAlpha=.4;for(let x=6;x<84;x+=4){px(g,x,y,'#9fc3ff');px(g,x,y+17,'#9fc3ff')}g.globalAlpha=1;continue}
  const hot=allhot;
  R(g,5,y,80,18,hot?MINT:INKC);R(g,6,y+1,78,16,hot?'#1c3a6e':'#14265a');
  R(g,6,y+1,78,1,'#2c4a8a');R(g,8,y+2,14,14,'#0c1c44');
  [icoBan,icoOp,icoAuto][k](g,8,y+2);
 }
 return{}}

const HEADS=[
 [0.10,3.50,"LEVEL 05",["WOULD YOU","RIDE IT?"],{tc:AMBER}],
 [3.60,9.20,"30 FEET UP",["ONE ROPE."]],
 [9.30,12.20,"HE LOOKS DOWN",["THEN NODS."]],
 [12.30,14.90,"AND THE AXE",["COMES OUT"],{tc:CORAL}],
 [15.00,23.20,"NEW YORK 1854",["CRYSTAL PALACE"]],
 [23.30,26.15,"HOISTS EXISTED",["FOR CENTURIES"]],
 [26.25,34.39,"ROPES BREAK",["PLATFORMS FELL."],{tc:CORAL}],
 [34.49,41.21,"SO CITIES STOPPED",["AT 5 FLOORS"]],
 [41.31,49.62,"THE SAFETY BRAKE",["TWO SPRING ARMS"]],
 [49.72,57.16,"ROPE GOES SLACK",["ARMS SNAP OUT"],{tc:MINT}],
 [57.26,64.04,"NO POWER",["JUST PHYSICS"],{tc:MINT}],
 [64.14,70.21,"NOBODY BELIEVED IT",["SO HE PROVED IT"]],
 [70.31,71.81,"THE ROPE",["IS CUT"],{tc:CORAL}],
 [71.91,76.80,"IT DROPS...",["AND STOPS."],{tc:MINT}],
 [76.90,81.74,"ALL SAFE,",["GENTLEMEN."],{tc:MINT}],
 [81.84,83.77,"NOW",["THINK."]],
 [83.87,92.58,"BEFORE OTIS",["TOP FLOOR: EMPTY"]],
 [92.68,97.67,"AFTER OTIS",["PENTHOUSE: PRIZED"],{tc:AMBER}],
 [97.77,102.61,"YOUR TURN",["WRITE THE CODE"],{tc:AMBER}],
 [102.71,108.73,"1854. A ROPE BREAKS.",["SOMEONE IS HURT."],{tc:CORAL}],
 [108.83,110.55,"HOW DO YOU",["RESPOND?"],{tc:AMBER}],
];

function heart(x,y,full){og.fillStyle=full?CORAL:'#3a3668';const u=7;[[1,0,2,1],[4,0,2,1],[0,1,7,2],[1,3,5,1],[2,4,3,1],[3,5,1,1]].forEach(([a,b,w,h])=>og.fillRect(x+a*u,y+b*u,w*u,h*u))}
function hud(t){const y=566,s=84,gap=18,x0=250,a=ease(seg(t,3.5,3.85));if(a<=0)return;og.save();og.globalAlpha=a;
 mdraw("LV 5",60,y+s/2+2,40,MINT,'left',false,'',0,a);
 const pr=cl01(t/END);
 for(let i=0;i<5;i++){const x=x0+i*(s+gap),ok=i<4,cur=i==4;og.globalAlpha=a;
  og.fillStyle=ok?'#173a2c':'#1b1838';rrect(og,x,y,s,s,12);og.fill();
  if(cur){og.save();rrect(og,x,y,s,s,12);og.clip();og.fillStyle='#2a4a7a';og.fillRect(x,y+s*(1-pr),s,s*pr);og.restore()}
  const hotq=cur&&t>=LOCK;
  og.lineWidth=4;og.strokeStyle=ok?MINT:(hotq&&Math.sin(t*10)>0?AMBER:cur?CORAL:'#3a3668');rrect(og,x,y,s,s,12);og.stroke();
  if(ok){og.strokeStyle=MINT;og.lineWidth=9;og.lineCap='round';og.beginPath();og.moveTo(x+22,y+44);og.lineTo(x+37,y+59);og.lineTo(x+63,y+27);og.stroke()}
  else mdraw(hotq?"?":"05",x+s/2,y+s/2+2,hotq?38:34,hotq?AMBER:CREAM,'center',false,'',0,a)}
 for(let i=0;i<3;i++)heart(800+i*76,y+20,true);
 og.restore()}

function frameAt(t){
 QA.chars=[];QA.solids=[];og.imageSmoothingEnabled=false;og.clearRect(0,0,1080,1920);
 const sg=SEG.find(s=>t>=s[0]&&t<s[1])||SEG[SEG.length-1],id=sg[2],o=t-sg[0];QA.shot=sg[3];let sh=0,inf={};
 ({crowd:()=>sceneCrowd(o,t),platform:()=>scenePlatform(o,t),nod:()=>sceneNod(o,t),axe:()=>sceneAxe(o,t),
  palace:()=>scenePalace(o,t),hoist:()=>sceneHoist(o,t),fall:()=>{inf=sceneFall(o,t)},lowcity:()=>sceneLowcity(o,t),
  brakediag:()=>sceneBrakediag(o,t),snapdiag:()=>sceneSnapdiag(o,t),physics:()=>scenePhysics(o,t),
  demo:()=>sceneDemo(o,t),drop:()=>sceneDrop(o,t),caught:()=>sceneCaught(o,t),hat:()=>sceneHat(o,t),
  think:()=>sceneThink(o,t),value:()=>sceneValue(o,t,false),penthouse:()=>sceneValue(o,t,true),
  desk:()=>sceneDesk(o,t),accident:()=>sceneAccident(o,t),ask:()=>sceneAsk(o,t),choice:()=>sceneChoice(o,t)})[id]();
 if(id=='fall'&&inf.sn)sh=shake(t,26.15+1.35+.9);
 if(id=='drop')sh=shake(t,70.21);
 if(id=='accident')sh=shake(t,102.75);
 og.drawImage(wc,0,0,WW,WH,sh,0,1080,1920);
 lit(()=>{const f=.6+.4*Math.sin(t*9)*Math.sin(t*5.3);
  if(id=='crowd'||id=='platform'||id=='demo'){glow(540,900,620,WARM,.2);grade('#2a1a3a',.18,'multiply')}
  else if(id=='nod'||id=='hat')glow(820,1000,560,WARM,.26);
  else if(id=='axe'||id=='drop'){glow(540,1000,620,WARM,.22);grade('#2a1a3a',.25,'multiply')}
  else if(id=='palace')glow(540,1150,700,COOL,.2);
  else if(id=='hoist'||id=='accident')glow(540,1000,520,WARM,.18);
  else if(id=='fall'){glow(540,1250,620,FIRE,.16+.08*f);grade('#2a1420',.3,'multiply')}
  else if(id=='lowcity')glow(540,800,640,COOL,.16);
  else if(id=='brakediag'||id=='snapdiag'||id=='physics'||id=='ask'||id=='think'||id=='choice')glow(540,1100,700,COOL,.14);
  else if(id=='caught')glow(540,950,560,SUN,.26);
  else if(id=='value')glow(540,1300,600,COOL,.14);
  else if(id=='penthouse')glow(540,780,520,SUN,.3);
  else if(id=='desk')glow(700,1000,520,WARM,.24);
  else glow(540,1100,700,COOL,.12)});
 const v=og.createLinearGradient(0,0,0,1920);v.addColorStop(0,'rgba(0,0,0,.22)');v.addColorStop(.3,'rgba(0,0,0,0)');v.addColorStop(.8,'rgba(0,0,0,0)');v.addColorStop(1,'rgba(0,0,0,.35)');og.fillStyle=v;og.fillRect(0,0,1080,1920);
 og.globalAlpha=.6;og.fillStyle='#0f0d22';og.fillRect(0,110,1080,562);og.globalAlpha=1;
 const h=HEADS.find(h=>t>=h[0]&&t<h[1]);
 if(id=='choice'){
  if(t<CDN)header("WRITE THE CODE",["A, B OR C?"],(t-TA)/.2,{tc:AMBER});
  else if(t<LOCK){const n=Math.max(1,3-Math.floor((t-CDN)/.8)),p=1+.25*(1-ease(seg(((t-CDN)%.8),0,.2)));
   header("LOCK IT IN",[],1);og.save();og.translate(540,330);og.scale(p,p);mdraw(String(n),0,0,220,AMBER,'center',true,INKC,20,1);og.restore()}
  else header("LOCKED.",["ANSWER: LEVEL 06"],(t-LOCK)/.2,{tc:MINT});}
 else if(h)header(h[2],h[3],(t-h[0])/.2,h[4]);
 hud(t);
 if(id=='fall'&&o>2.3)stamp("SNAP",'#e0473c',540,850,26.15+2.3,t,-.07,64);
 if(id=='caught'&&o>.3)stamp("CAUGHT",'#2fbf8f',540,1270,71.81+.3,t,-.05,64);
 if(id=='hat'&&o>1.5)stamp("ALL SAFE",'#2fbf8f',190,1290,76.80+1.5,t,.04,40);
 if(id=='snapdiag'&&o>1.3)stamp("BRAKE ENGAGED",'#2fbf8f',540,860,49.62+1.3,t,-.04,48);
 if(id=='choice'){
  const L=[["A","BAN THEM. FREIGHT ONLY."],["B","A TRAINED OPERATOR IN EVERY CAR"],["C","AN AUTOMATIC SAFETY DEVICE"]];
  const at=[TA,TB,TC];
  L.forEach(([a,s],k)=>{if(t<at[k])return;const al=ease(seg(t,at[k],at[k]+.18)),y=(69+k*20)*12;
   mdraw(a,26.5*12,y+2,56,AMBER,'center',true,INKC,10,al);
   mdraw(s,31*12,y+2,fit(s,40,580),CREAM,'left',false,'',0,al)});
  if(t>=LOCK+.5&&t<LOCK+2.2)tag("COMMENT A, B OR C",540,1430,AMBER,ease(seg(t,LOCK+.5,LOCK+.67)));
  if(t>=LOCK+2.2)tag("FOLLOW — ANSWER IN LEVEL 06",540,1430,MINT,ease(seg(t,LOCK+2.2,LOCK+2.37)));}
 subtitle(t,false);for(const c of CUTS)wipe(t,c,.12);
}
window.frame=i=>frameAt(i/30);
Promise.all([document.fonts.load('700 40px Silk'),document.fonts.load('400 40px PS2P')]).then(()=>{window.READY=true});
