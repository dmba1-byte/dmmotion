// ===== Level 03 : the tower on stilts (Citicorp Center, 1978) =====
const END=88.0;
const SUBS=[[0.12,2.64,"Why does this skyscraper stand on four stilts?"],
[2.9,3.58,"Level three."],[3.86,5.57,"New York, 1978."],
[5.83,7.09,"A church sat on the corner."],[7.54,9.99,"So the tower's legs went in the middle of each side."],
[10.25,12.36,"Then a student called the engineer with a question."],[12.8,14.39,"What if the wind hits the corner?"],
[14.65,15.54,"He ran the numbers."],[16.0,17.6,"Against a corner wind,"],[17.6,19.51,"his tower was far weaker than he'd designed."],
[19.77,21.88,"By his math, even with everything working,"],[22.34,23.9,"a storm that could topple it"],[23.9,25.64,"came once every fifty-five years."],
[25.9,26.9,"You're the engineer."],[26.9,27.57,"Three options."],[27.77,28.68,"Which one would you pick?"],
[29.2,30.11,"Option A."],[30.58,31.37,"Trust the damper."],[31.8,34.55,"A giant block on the roof already steadies the tower."],
[35.12,36.11,"Option B."],[36.58,37.4,"Wait for winter."],[37.95,39.2,"Big storms are rare,"],[39.2,41.44,"so fix it properly after hurricane season."],
[42.01,42.99,"Option C."],[43.46,44.15,"Confess."],[44.2,46.4,"Tell the bank your tower is flawed,"],[46.82,48.74,"and fix it at night, with thousands still working inside."],
[52.06,53.33,"Option A sounds smart."],[53.81,55.62,"But the damper runs on electricity."],[56.15,57.5,"If a storm cuts the power,"],[57.5,59.48,"his odds drop to one in sixteen."],
[59.74,61.16,"Option B sounds careful."],[61.65,62.75,"But that same season,"],[62.75,64.71,"Hurricane Ella headed for New York."],
[64.97,66.38,"Option C is what he did."],[66.85,68.12,"The flaw was in the joints."],[68.43,69.5,"They were drawn as welds,"],[69.5,70.73,"but built with bolts."],
[70.99,72.91,"So welders covered them with steel plates,"],[73.1,74.07,"night after night."],
[74.33,76.09,"They were only half done when Ella came."],[76.48,77.64,"Then it turned out to sea."],
[77.9,80.39,"The city didn't hear the story for seventeen years."],
[80.65,83.58,"Today, engineers have to check diagonal wind too."],
[83.84,84.56,"Level cleared."],[84.91,85.9,"Comment what you picked,"],[85.9,87.32,"and follow for level four."]];
const SEG=[[0,2.88,0,2.88,'tower','wide'],[2.88,5.81,0,2.93,'legs','low'],[5.81,10.23,0,4.42,'plan','plan'],[10.23,12.78,0,2.55,'phone','side'],[12.78,14.63,0,1.85,'wind','diagram'],
[14.63,15.98,0,1.35,'face1','closeup'],[15.98,19.75,0,3.77,'storm','wide'],[19.75,22.3,1.4,3.95,'face1','closeup'],[22.3,25.76,3.77,7.23,'storm','wide'],[25.76,28.93,0,3.17,'ask','front'],
[28.93,34.83,0,5.9,'pA','cutaway'],[34.83,41.72,0,6.89,'pB','detail'],[41.72,48.9,0,7.18,'pC','wide'],[48.9,51.95,0,3.05,'choice','menu'],
[51.95,59.6,0,7.65,'A','cutaway'],[59.6,64.83,0,2.75,'B','map'],[64.83,66.6,0,1.9,'bank','side'],[66.6,69.5,0,1.9,'joint','detail'],[69.5,70.85,1.93,3.3,'joint','detail'],[70.85,74.19,0,3.34,'weld','back'],
[74.19,77.76,2.3,4.48,'ella','map'],[77.76,80.51,0,2.75,'face2','closeup'],[80.51,83.7,0,3.19,'today','diagram'],[83.7,END,36.36,40.66,'win','front']];
const CUTS=SEG.slice(1).map(s=>s[0]).filter(c=>c!=69.5);
LOOK.bill={id:'bill',skin:'#efc9a6',skinD:'#d0a684',hair:'#c9c9d2',top:'#56627a',topL:'#74819c',pants:'#3a3f52',shoe:'#1e1c24'};
LOOK.w1=Object.assign({},LOOK.a1,{id:'w1'});LOOK.w2=Object.assign({},LOOK.a2,{id:'w2',top:'#c9695a',topL:'#e08a7a'});LOOK.w3=Object.assign({},LOOK.a3,{id:'w3'});
LOOK.weld={id:'weld',skin:'#c98b69',skinD:'#a86f52',hair:'#3a3a44',top:'#6a5a3a',topL:'#8a7850',pants:'#3a4052',shoe:'#1e1c24',bag:'#6a5a3a',bagL:'#8a7850'};
const STEEL='#6f7887',STEELL='#97a2b3',STEELD='#4a5262';

// ---------- the tower, seen from its corner ----------
function skyline(g,night,t,g0,g1){const c1=night?'#1a1c34':'#8fa8c8',c2=night?'#23264a':'#a9bfd8';
 const H=[20,31,16,26,38,22,14,30,24,34,18,28];for(let k=0;k<12;k++){const x=k*8-2,h=H[k];if(x+7>g0&&x<g1)continue;R(g,x,114-h,7,h,k%2?c1:c2);
  for(let y=114-h+2;y<112;y+=3)for(let xx=x+1;xx<x+6;xx+=2)if((xx*7+y*3+k)%5<2)px(g,xx,y,night?'#e8c860':'#dbe8f4')}}
function tower(g,x,base,sway,night,dark){const fw=22,st=18,bh=30,yb=base-st,yt=yb-bh,rf=10;
 // stilts: one under the middle of each visible face, plus the core
 R(g,x+fw-4,yb,8,st,night?'#3a4060':'#77808f');
 R(g,x+8,yb,6,st,night?'#6a7290':'#c9ced6');R(g,x+8,yb,2,st,night?'#8089a8':'#e6e9ee');R(g,x+7,yb,1,st,night?'#23264a':'#5c6470');R(g,x+14,yb,1,st,night?'#23264a':'#5c6470');
 R(g,x+fw+8,yb,6,st,night?'#565e7c':'#a3aab5');R(g,x+fw+13,yb,1,st,night?'#3a4060':'#858c98');R(g,x+fw+7,yb,1,st,night?'#23264a':'#5c6470');R(g,x+fw+14,yb,1,st,night?'#23264a':'#5c6470');R(g,x-1,yb,fw*2+2,1,night?'#23264a':'#4b5563');
 for(let y=yb-1;y>=yt-rf;y--){const fr=(yb-y)/(bh+rf),off=Math.round(sway*fr);
  let x0=x,x1=x+fw*2;if(y<yt){x0=x+Math.round((yt-y)*fw*2/rf)}if(x0>=x1)continue;
  const band=(yb-y)%2==0;
  for(let xx=x0;xx<x1;xx++){const left=xx<x+fw;let c;
   if(y<yt)c=left?(night?'#7a84a6':'#dfe4ea'):(night?'#5c6688':'#b9c0ca');
   else if(band)c=left?(night?'#7a84a6':'#e3e7ec'):(night?'#5c6688':'#bcc3cd');
   else{const lit=!dark&&((xx*13+y*7)%9<5);c=night?(lit?'#f6d878':'#1c2240'):(left?'#6f8fb4':'#56769a')}
   px(g,xx+off,y,c)}
  px(g,x+fw+off,y,night?'#3a4060':'#98a1ad')}
 // the church, tucked under the corner
 const cx=x+fw;for(let k=0;k<9;k++)R(g,cx-7+Math.floor(k*.5),base-1-k,14-Math.floor(k*1.2),1,night?'#4a4350':'#8c7f77');R(g,cx-7,base-1,14,1,night?'#3a3340':'#6f645d');R(g,cx-1,base-7,1,4,night?'#e0c870':'#f1e6c4');R(g,cx-2,base-6,3,1,night?'#e0c870':'#f1e6c4')}
function sceneTower(q,t){const g=wg;R(g,0,0,WW,56,NAVY);
 for(let y=56;y<116;y++)R(g,0,y,WW,1,mixc('#5f9fe0','#dcecf7',(y-56)/60));
 cloud(g,(60+t*2)%110-14,64,16);cloud(g,(8+t*1.4)%110-14,78,13);
 skyline(g,false,t,0,52);tower(g,4,116,0,false);
 R(g,0,114,WW,2,'#7c8794');for(let y=116;y<WH;y++)R(g,0,y,WW,1,(y-116)%7==0?'#8d939c':'#a9afb8');for(let x=-40;x<WW+40;x+=14)line(g,45+(x-45)*.7,116,45+(x-45)*1.8,WH,1,'#8d939c');
 // Kit stops and looks up
 const u=seg(q,0,.9),br=Math.sin(t*2.4)>.4?-1:0,tilt=q>.9?-1:0;
 const P=u<1?Object.assign(walkFB(q*.9,'b'),{nobag:false}):{hip:GY-17,feet:[[-3,0],[3,0]],sl:1,sa:[1,1],hands:[[CX-8,SHY+10],[CX+8,SHY+10+(q>1.6?-Math.round(ease(seg(q,1.6,2))*14):0)]],hy:br+tilt,nobag:false};
 personFB(P,43,-Math.round(lerp(18,10,ease(u))),null,'b');return{}}
// low angle: the stilts and the church
function sceneLegs(q,t){const g=wg;R(g,0,0,WW,56,NAVY);
 for(let y=56;y<FL;y++)R(g,0,y,WW,1,mixc('#6fa8e2','#e2eff8',(y-56)/64));cloud(g,(20+t*2)%120-16,100,14);
 R(g,0,104,WW,16,'#9fb2c8');for(let k=0;k<9;k++){R(g,k*11-3,108-(k*5)%9,9,12+(k*5)%9,k%2?'#8aa0ba':'#96aac2')}
 // core, then the tower floor overhead
 R(g,37,74,16,46,'#6b7380');R(g,37,74,2,46,'#7f8896');for(let y=78;y<120;y+=6)R(g,37,y,16,1,'#5c6470');
 for(let y=56;y<76;y++){const b=(y%3==0);R(g,0,y,45,1,b?'#e3e7ec':'#6f8fb4');R(g,45,y,45,1,b?'#bcc3cd':'#56769a')}R(g,0,74,WW,2,'#4b5563');R(g,45,56,1,20,'#98a1ad');
 // two stilts, one under the middle of each face
 for(const[x,l,d]of[[15,'#e6e9ee','#c2c8d1'],[64,'#b9c0ca','#98a1ad']]){R(g,x,76,11,44,d);R(g,x,76,3,44,l);R(g,x+10,76,1,44,'#7c8592');for(let y=84;y<120;y+=9)R(g,x,y,11,1,'#a9b0bb')}
 // the church under the hanging corner
 const up=ease(seg(q,.5,1.2));for(let k=0;k<22;k++)R(g,31+Math.floor(k*.5),119-k,29-Math.floor(k*1.1),1,k%5==4?'#7d716a':'#94877f');
 R(g,31,119,29,1,'#6f645d');R(g,44,103,1,8,'#f1e6c4');R(g,42,105,5,1,'#f1e6c4');R(g,38,112,4,8,'#4a3f3a');
 for(let y=FL;y<WH;y++)R(g,0,y,WW,1,(y-FL)%8==0?'#8d939c':'#aeb4bd');for(let x=-60;x<WW+60;x+=12)line(g,45+(x-45)*.6,FL,45+(x-45)*1.7,WH,1,'#8d939c');
 // passers-by, far smaller than the stilts
 for(let k=0;k<4;k++){const dir=k%2?1:-1,x=((k*29+q*6*dir)%100+100)%100-5,y=FL+2+k*3,s=Math.floor(q*5+k)%2;R(g,x,y-6,2,2,['#e9c3a3','#8a5a3c','#f0caa8','#c98b69'][k]);R(g,x,y-4,2,3,['#d9564f','#3f8fb0','#e0b24a','#8a5cc4'][k]);px(g,x+s,y-1,'#2c2a3a');px(g,x+1-s,y-1,'#2c2a3a');g.globalAlpha=.2;R(g,x-1,y,4,1,'#000');g.globalAlpha=1}
 if(q>1.3){g.globalAlpha=ease(seg(q,1.3,1.6));ptext(g,'CHURCH',34,92,'#3a2f2a');g.globalAlpha=1}
 return{}}
function bpFlat(g,t){R(g,0,0,WW,56,NAVY);for(let y=56;y<WH;y++)R(g,0,y,WW,1,mixc('#21468a','#12285a',(y-56)/104));
 g.globalAlpha=.14;for(let x=5;x<WW;x+=8)R(g,x,56,1,104,'#9fc3ff');for(let y=60;y<WH;y+=8)R(g,0,y,WW,1,'#9fc3ff');g.globalAlpha=1;
 const sx=(t*16)%130-20;g.globalAlpha=.07;R(g,sx,56,7,104,'#e8f3ff');g.globalAlpha=1}
function box(g,x,y,w,h,c){R(g,x,y,w,1,c);R(g,x,y+h-1,w,1,c);R(g,x,y,1,h,c);R(g,x+w-1,y,1,h,c)}
// plan view: the legs slide from the corners to the middle of each side
function scenePlanT(q,t){const g=wg;bpFlat(g,t);const x0=24,y0=72,s=44,c='#cfe2ff';
 box(g,x0,y0,s,s,c);box(g,x0+1,y0+1,s-2,s-2,'#6f95d8');box(g,x0+16,y0+16,12,12,c);for(let k=0;k<12;k+=3)line(g,x0+16,y0+16+k,x0+16+k,y0+16,1,'#6f95d8');
 // church on the corner
 R(g,x0-6,y0-6,22,22,'#2a1c1a');R(g,x0-5,y0-5,20,20,'#94877f');for(let k=0;k<20;k+=4)line(g,x0-5,y0-5+k,x0-5+k,y0-5,1,'#7d716a');R(g,x0+4,y0+1,1,7,'#f1e6c4');R(g,x0+2,y0+3,5,1,'#f1e6c4');
 const u=ease(seg(q,1.9,3.0)),m=s/2-3,C=[[0,0,m,0],[s-6,0,s-6,m],[s-6,s-6,m,s-6],[0,s-6,0,m]];
 C.forEach(([ax,ay,bx,by],k)=>{const x=Math.round(x0+lerp(ax,bx,u)),y=Math.round(y0+lerp(ay,by,u)),bad=k==0&&q<1.9&&q>.5&&Math.sin(t*16)>0;
  if(u<1&&u>0){g.globalAlpha=.3;R(g,x0+ax,y0+ay,6,6,c);g.globalAlpha=1}
  R(g,x-1,y-1,8,8,INKC);R(g,x,y,6,6,bad?CORAL:u>=1?MINT:AMBER);R(g,x,y,6,1,'#fffaf0')});
 ptext(g,'CHURCH',x0-8,y0-13,'#f1e6c4');if(q>3)ptext(g,'CORE',x0+15,y0+30,c);
 if(q>3.1){g.globalAlpha=ease(seg(q,3.1,3.4));for(const[cx,cy]of[[x0+s-1,y0],[x0+s-1,y0+s-1],[x0,y0+s-1]]){box(g,cx-3,cy-3,7,7,CORAL)}g.globalAlpha=1}
 return{}}
function officeB(g,t,night){R(g,0,0,WW,56,NAVY);R(g,0,56,WW,64,night?'#2a2c44':'#b9ad96');R(g,0,56,WW,1,night?'#3a3c58':'#cdc2ac');R(g,0,104,WW,2,night?'#1c1e34':'#8a7f6c');R(g,0,106,WW,14,night?'#23253c':'#9c907b');
 // window with the skyline
 R(g,4,60,30,34,'#3a3340');R(g,5,61,28,32,night?'#141a3a':'#9cc4ec');for(let k=0;k<6;k++){const h=[10,16,8,20,12,15][k];R(g,6+k*4.5,93-h,4,h,night?'#23264a':'#7f9cc0')}R(g,19,61,1,32,'#3a3340');R(g,5,77,28,1,'#3a3340');
 // framed tower elevation
 R(g,66,62,16,24,'#3a3340');R(g,67,63,14,22,'#f4ecd8');R(g,71,66,6,13,'#7f97b4');R(g,72,79,1,4,'#56627a');R(g,75,79,1,4,'#56627a');
 woodFloor(g,night?'#3a2e2a':'#8a6a4a',night?'#43362f':'#96744f',night?'#2a201c':'#6f5238')}
function scenePhone(q,t){const g=wg;officeB(g,t,false);
 // drafting table with a rotary phone
 solid('table',54,82);R(g,54,100,28,2,'#6b4e36');R(g,54,100,28,1,'#8a6a4a');R(g,56,102,2,18,'#5a3e28');R(g,78,102,2,18,'#5a3e28');R(g,57,96,14,4,'#f4ecd8');R(g,57,96,14,1,'#fffaf0');
 R(g,72,95,8,5,'#2a2a34');R(g,73,93,6,2,'#3a3a48');px(g,75,97,'#c9c9d2');
 const talk=Math.floor(q*5)%2,br=Math.sin(t*2.6)>.5?-1:0;
 const P={legs:stand2,arms:[{ua:0,fa:0},{ua:6,fa:14}],armRel:[[5,-9],null],lean:2,face:q>1.5?'o':'n',mouth:q>1.5?'flat':(talk?'open':'smile'),look:1,dy:br};
 const inf=person(P,8,0,LOOK.bill,(gg,i)=>{glasses(gg,i);const h=i.h[0];R(gg,h[0]-1,h[1]-4,3,8,'#2a2a34');R(gg,h[0]-1,h[1]-1,3,3,LOOK.bill.skin)},false);
 const h=handW(inf,0,8,false);line(g,h[0]+1,h[1]+4,62,104,1,'#2a2a34');line(g,62,104,74,99,1,'#2a2a34');
 if(q>.3){const a=ease(seg(q,.3,.5));g.globalAlpha=a;R(g,46,62,18,13,INKC);R(g,47,63,16,11,'#fffaf0');px(g,48,74,'#fffaf0');px(g,47,75,INKC);R(g,54,65,3,1,INKC);R(g,56,66,1,2,INKC);R(g,55,68,1,2,INKC);R(g,55,71,1,1,INKC);g.globalAlpha=1}
 return{}}
function arrow(g,x,y,dx,dy,len,c){line(g,x,y,x+dx*len,y+dy*len,1,c);const ex=x+dx*len,ey=y+dy*len;line(g,ex,ey,ex-dx*3-dy*2,ey-dy*3+dx*2,1,c);line(g,ex,ey,ex-dx*3+dy*2,ey-dy*3-dx*2,1,c)}
function sceneWind(q,t,ok){const g=wg;bpFlat(g,t);const x0=40,y0=80,s=34,c='#cfe2ff',col=ok?MINT:CORAL;
 box(g,x0,y0,s,s,c);box(g,x0+1,y0+1,s-2,s-2,'#6f95d8');box(g,x0+12,y0+12,10,10,c);
 const m=s/2-2;[[m,0],[s-4,m],[m,s-4],[0,m]].forEach(([a,b],k)=>{const hit=!ok&&k!=1&&k!=2&&Math.sin(t*14)>0;R(g,x0+a-1,y0+b-1,6,6,INKC);R(g,x0+a,y0+b,4,4,ok?MINT:hit?CORAL:AMBER)});
 const d=.7071;for(let k=0;k<5;k++){const o=(k-2)*9,ph=(q*1.3+k*.17)%1,bx=x0-30+o*d+ph*14,by=y0-30-o*d+ph*14;
  if(bx<x0-3||by<y0-3){g.globalAlpha=.4+.6*ph;arrow(g,Math.round(bx),Math.round(by),d,d,9,col);g.globalAlpha=1}}
 ptext(g,'WIND',6,104,col);
 if(!ok&&q>.6){const j=Math.round(Math.sin(t*30));box(g,x0+j,y0,s,s,CORAL)}
 if(ok&&q>1){const a=ease(seg(q,1,1.3));g.globalAlpha=a;line(g,x0+11,y0+17,x0+15,y0+22,2,MINT);line(g,x0+15,y0+22,x0+24,y0+10,2,MINT);g.globalAlpha=1;}
 return{}}
function sceneFace(q,t,m){const g=wg;officeB(g,t,m==1);g.globalAlpha=m==1?.35:.15;R(g,0,56,WW,104,'#0c0a1c');g.globalAlpha=1;
 if(m==1){portrait(g,LOOK.bill,{glasses:1,shirt:1,brow:1,blink:(t%2.3)<.1,ex:Math.round(Math.sin(q*9)),ey:1,mouth:q>.6?'open':'flat'});
  const dy=Math.round(((q*1.2)%1)*8);R(g,68,84+dy,2,3,'#9fd4ff');px(g,68,83+dy,'#9fd4ff')}
 else portrait(g,LOOK.bill,{glasses:1,shirt:1,blink:(t%2.6)<.12||(q>.5&&q<.9),mouth:'smile',dy:Math.sin(t*2.2)>.4?1:0});
 return{}}
// close on one brace joint: welded as drawn, bolted as built
function sceneJoint(q,t){const g=wg;R(g,0,0,WW,56,NAVY);for(let y=56;y<WH;y++)R(g,0,y,WW,1,mixc('#2a3040','#12151f',(y-56)/104));
 for(let k=0;k<5;k++){line(g,-10+k*30,56,-40+k*30,160,3,'#232836')}
 const bolted=q>=1.93,y=92,h=30;
 for(const[x,w]of[[0,45],[45,45]]){R(g,x,y,w,h,STEEL);R(g,x,y,w,5,STEELL);R(g,x,y+5,w,1,STEELD);R(g,x,y+h-5,w,5,shade(STEEL,.8));R(g,x,y+h-6,w,1,STEELD);R(g,x,y,w,1,'#c4cddb')}
 R(g,44,y,2,h,'#12151f');
 if(!bolted){const n=Math.floor(ease(seg(q,.15,1.2))*h);for(let k=0;k<n;k++){const zz=(k%4<2)?0:1;R(g,43+zz,y+k,3,1,k>n-4?'#fff6c0':'#f0a040');px(g,44+zz,y+k,k>n-4?'#ffffff':'#ffd27a')}
  if(n<h&&n>0){for(let k=0;k<7;k++){const a=k*.9+t*20,r=3+(k*5+Math.floor(t*30))%7;px(g,44+Math.cos(a)*r,y+n+Math.sin(a)*r*.6,k%2?'#fff6c0':'#ffb040')}}
  ptext(g,'WELD',52,y-9,'#ffd27a')}
 else{const dz=Math.round((1-ease(seg(q,1.93,2.15)))*-30);R(g,29,y+4+dz,32,h-8,INKC);R(g,30,y+5+dz,30,h-10,'#8a94a6');R(g,30,y+5+dz,30,1,'#c4cddb');R(g,30,y+h-6+dz,30,1,STEELD);
  for(let r=0;r<3;r++)for(const bx of[33,38,50,55]){const by=y+8+r*6+dz;R(g,bx-1,by-1,4,4,INKC);R(g,bx,by,2,2,'#d9dee8');px(g,bx,by,'#ffffff')}
  if(q>2.3)ptext(g,'BOLTS',36,y-9,CORAL)}
 return{}}
function sceneStorm(q,t,calm){const g=wg;R(g,0,0,WW,56,NAVY);const fl=!calm&&((q>1.2&&q<1.32)||(q>3.9&&q<4.0))?1:0,dark=false;
 for(let y=56;y<116;y++)R(g,0,y,WW,1,fl?'#aab4e0':mixc('#1a1e40','#39406e',(y-56)/60));
 for(let k=0;k<3;k++){const x=((k*40-q*14)%130+130)%130-30;R(g,x,62+k*7,30,5,fl?'#c8d0f0':'#2a2f58');R(g,x+5,60+k*7,18,3,fl?'#c8d0f0':'#2a2f58')}
 if(calm){for(let a=0;a<7;a++)for(let b=0;b<7;b++){const d=(a-3)*(a-3)+(b-3)*(b-3),d2=(a-5)*(a-5)+(b-2)*(b-2);if(d<=10&&d2>8)px(g,70+a,61+b,'#f4ecd8')}for(let k=0;k<14;k++)px(g,(k*29)%WW,58+(k*13)%40,'#cfd6ff')}
 skyline(g,true,t,20,70);const sw=calm?0:Math.sin(q*3.1)*2.6*cl01(q/1.2);tower(g,23,116,sw,true,dark);
 R(g,0,114,WW,2,'#23264a');for(let y=116;y<WH;y++)R(g,0,y,WW,1,(y-116)%7==0?'#2a2e52':'#353a62');
 if(!calm)for(let k=0;k<46;k++){const sp=70+(k%5)*14,x=((k*23+q*sp*.9)%110+110)%110-10,y=56+((k*37+q*sp)%104);g.globalAlpha=.55;line(g,x,y,x+3,y+4,1,'#b9c8f0');g.globalAlpha=1}
 if(!calm)for(let k=0;k<5;k++){const x=((q*90+k*31)%150)-30,y=64+k*9;g.globalAlpha=.35;R(g,x,y,12,1,'#dfe6ff');g.globalAlpha=1}
 return{}}
// the roof damper, in section
function sceneDamper(q,t,cut){const g=wg;R(g,0,0,WW,56,NAVY);const off=cut&&q>2.3,fl=cut&&((q>2.1&&q<2.2)||(q>2.26&&q<2.3));
 for(let y=56;y<WH;y++)R(g,0,y,WW,1,mixc('#1a1e40','#39406e',(y-56)/104));
 for(let k=0;k<3;k++){const x=((k*40-q*14)%130+130)%130-30;R(g,x,60+k*6,30,5,'#2a2f58')}
 const amp=off?4:1,sw=Math.round(Math.sin(q*3.1)*amp);
 // tower top, cut open
 for(let y=132;y<WH;y++)R(g,6+Math.round(sw*(160-y)/60),y,78,1,(y%3==0)?'#7a84a6':((y*7)%5<2&&!off?'#f6d878':'#1c2240'));
 for(let i=0;i<78;i++){const h=Math.round(i*.22);R(g,6+i+sw,74-h,1,58+h,'#565e7c')}
 R(g,9+sw,78,72,50,off?'#12142a':'#e9dfc8');R(g,9+sw,78,72,2,off?'#1c1e38':'#f6f0e2');R(g,9+sw,126,72,4,'#4a5262');
 for(let x=14;x<78;x+=12)R(g,x+sw,78,1,48,off?'#1a1c34':'#d6ccb4');
 // rails, pistons, block
 R(g,12+sw,124,66,2,'#2a2e44');const bx=off?31:31-Math.round(Math.sin(q*3.1)*7);
 R(g,12+sw,104,bx-12,3,off?'#3a3f52':'#9aa3b2');R(g,bx+28+sw,104,78-bx-28,3,off?'#3a3f52':'#9aa3b2');R(g,10+sw,98,3,16,'#4a5262');R(g,77+sw,98,3,16,'#4a5262');
 R(g,bx-1+sw,87,30,37,INKC);R(g,bx+sw,88,28,35,off?'#3a3d4c':'#8f939c');R(g,bx+sw,88,28,2,off?'#4a4d5c':'#b4b8c0');R(g,bx+sw,120,28,3,off?'#2a2d3a':'#6f737c');for(let k=0;k<4;k++)px(g,bx+4+k*7+sw,93+(k*5)%20,off?'#2a2d3a':'#7c8089');
 ptext(g,'DAMPER',bx+3+sw,103,off?'#6a6e7c':'#2a2e44');
 R(g,43+sw,80,5,3,off?'#3a3a44':'#fff6c0');if(off&&Math.sin(t*9)>0){R(g,14+sw,82,3,3,'#e0473c')}
 if(fl){g.globalAlpha=.5;R(g,0,56,WW,104,'#ffffff');g.globalAlpha=1}
 for(let k=0;k<30;k++){const sp=70+(k%5)*14,x=((k*23+q*sp*.9)%110+110)%110-10,y=56+((k*37+q*sp)%26);g.globalAlpha=.5;line(g,x,y,x+3,y+4,1,'#b9c8f0');g.globalAlpha=1}
 return{off}}
// wait for winter: the calendar runs on
function sceneCalW(q,t){const g=wg;R(g,0,0,WW,56,NAVY);for(let y=56;y<WH;y++)R(g,0,y,WW,1,'#9aa58f');R(g,0,128,WW,3,'#6a6a5a');R(g,0,131,WW,29,'#6a6658');
 const M=['AUG','SEP','OCT','NOV','DEC'],f=Math.max(0,q-1.6)*1.15,mi=Math.min(4,Math.floor(f)),fr=mi<4?f-mi:0,win=mi==4;
 R(g,43,60,4,6,'#3a3a44');g.globalAlpha=.3;R(g,19,70,56,60,'#1a1008');g.globalAlpha=1;R(g,17,66,56,60,INKC);R(g,18,67,54,58,'#f4ecd8');R(g,18,67,54,12,win?'#3f6fb0':'#c43c3c');ptext(g,M[mi]+' 1978',29,71,'#fff6e0');
 for(let r=0;r<5;r++)for(let c2=0;c2<7;c2++){const x=21+c2*7,y=83+r*8;R(g,x,y,5,5,win?'#cfe0f2':'#e6dcc4')}
 if(!win)spiral(g,45,104,11,-t*4,'#3f6fb0');else{line(g,36,104,42,111,2,'#2f8f5f');line(g,42,111,55,95,2,'#2f8f5f')}
 if(fr>.55){const h=Math.round((fr-.55)/.45*58);R(g,18,125-h,54,1,'#c9c0a8');g.globalAlpha=.3;R(g,18,125-h,54,h,'#8a8478');g.globalAlpha=1}
 if(win)for(let k=0;k<22;k++){const x=(k*37+Math.round(Math.sin(t*1.5+k)*3))%WW,y=56+((t*14+k*23)%104);px(g,x,y,'#f6f8ff')}
 return{}}
function sceneAsk(q,t){const g=wg;blueprintWall(g,t);const br=Math.sin(t*2.4)>.5?-1:0,sh=Math.round(Math.sin(q*6));
 personFB({hip:GY-17,feet:[[-3,0],[3,0]],sl:1,sa:[1,1],hands:[[CX-14,SHY+5+sh],[CX+13,SHY+5+sh]],mouth:'open',hy:br,nobag:false},13,0,null,'f');
 [[14,70,1.2],[38,62,1.5],[62,70,1.8]].forEach(([x,y,a],k)=>{if(q<a)return;const b=Math.round(Math.sin(t*5+k));R(g,x,y+b,14,13,INKC);R(g,x+1,y+1+b,12,11,'#14265a');ptext(g,'ABC'[k],x+6,y+4+b,AMBER)});return{}}
function icoA(g,x,y){R(g,x+1,y+2,12,11,'#39406e');R(g,x+4,y+5,6,6,'#8f939c');R(g,x+4,y+5,6,1,'#b4b8c0');R(g,x+1,y+7,3,1,'#9aa3b2');R(g,x+10,y+7,3,1,'#9aa3b2')}
function icoB(g,x,y){R(g,x+1,y+2,12,11,'#f4ecd8');R(g,x+1,y+2,12,3,'#3f6fb0');for(let r=0;r<2;r++)for(let c2=0;c2<3;c2++)R(g,x+2+c2*4,y+7+r*3,2,2,'#cfc6b0');px(g,x+4,y+1,INKC);px(g,x+9,y+1,INKC)}
function icoC(g,x,y){R(g,x+1,y+2,12,8,'#f4ecd8');px(g,x+3,y+10,'#f4ecd8');px(g,x+3,y+11,'#f4ecd8');R(g,x+6,y+3,2,4,'#e0473c');R(g,x+6,y+8,2,1,'#e0473c');R(g,x+10,y+10,3,3,'#f4ecd8');R(g,x+11,y+10,2,2,'#0c1c44')}
function sceneChoice(q,t){const g=wg;blueprintWall(g,t);g.globalAlpha=.6;R(g,0,56,WW,104,'#0a1433');g.globalAlpha=1;
 const sel=q>=.25?Math.min(2,Math.floor((q-.25)/.92)):-1;
 for(let k=0;k<3;k++){const y=60+k*20,hot=sel==k;R(g,5,y,80,18,hot?MINT:INKC);R(g,6,y+1,78,16,hot?'#1c3a6e':'#14265a');R(g,6,y+1,78,1,'#2c4a8a');R(g,8,y+2,14,14,'#0c1c44');[icoA,icoB,icoC][k](g,8,y+2);
  if(hot){const b=Math.round(Math.sin(t*12));for(let i=0;i<4;i++)R(g,1+b,y+5+i,i<2?i+1:4-i,1,MINT)}}
 return{}}
function spiral(g,cx,cy,r,rot,c){for(let a=0;a<14;a+=.35){const rr=r*a/14;px(g,cx+Math.cos(a+rot)*rr,cy+Math.sin(a+rot)*rr*.9,c);px(g,cx-Math.cos(a+rot)*rr,cy-Math.sin(a+rot)*rr*.9,c)}R(g,Math.round(cx)-1,Math.round(cy)-1,2,2,'#0c1c44')}
function sceneBank(q,t){const g=wg;R(g,0,0,WW,56,NAVY);R(g,0,56,WW,64,'#d8d2c4');for(let x=0;x<WW;x+=18){R(g,x,56,5,64,'#ebe6da');R(g,x,56,1,64,'#f6f2ea');R(g,x+4,56,1,64,'#bdb6a6')}
 R(g,56,66,28,54,'#3a3340');R(g,58,68,11,52,'#5a4a3a');R(g,71,68,11,52,'#5a4a3a');R(g,60,72,7,20,'#7a6650');R(g,73,72,7,20,'#7a6650');R(g,68,94,1,6,'#d9b24a');R(g,71,94,1,6,'#d9b24a');
 R(g,58,58,24,7,INKC);R(g,59,59,22,5,'#d9b24a');ptext(g,'BANK',62,59,'#3a2a14');
 for(let y=FL;y<WH;y++)R(g,0,y,WW,1,(y-FL)%8==0?'#b9b2a4':'#cfc8ba');for(let x=-60;x<WW+60;x+=14)line(g,45+(x-45)*.6,FL,45+(x-45)*1.7,WH,1,'#b9b2a4');
 const ox=lerp(-30,14,q/1.92),P=walkP(ox+30,{armRel:[[5,5],null],face:'n',mouth:'flat'});
 person(P,ox,0,LOOK.bill,(gg,i)=>{glasses(gg,i);const h=i.h[0];R(gg,h[0]-6,h[1]-1,13,3,'#f4ecd8');R(gg,h[0]-6,h[1]-1,1,3,'#9fb6d8');R(gg,h[0]+6,h[1]-1,1,3,'#9fb6d8');R(gg,h[0]-1,h[1]-1,3,3,LOOK.bill.skin)},false);return{}}
// night shift: a welder plates over the bolted joint
function sceneWeld(q,t){const g=wg;R(g,0,0,WW,56,NAVY);for(let y=56;y<FL;y++)R(g,0,y,WW,1,mixc('#10142a','#1c2240',(y-56)/64));
 R(g,2,60,20,26,'#0c0e1c');R(g,3,61,18,24,'#141a3a');for(let k=0;k<5;k++)R(g,4+k*3.5,85-[6,11,5,13,8][k],3,[6,11,5,13,8][k],'#23264a');for(let k=0;k<7;k++)px(g,5+(k*5)%15,74+(k*3)%9,'#e8c860');R(g,15,63,3,3,'#f4ecd8');
 // chevron brace and the joint
 line(g,-6,120,45,70,9,STEELD);line(g,96,120,45,70,9,STEELD);line(g,-6,118,45,68,5,STEEL);line(g,96,118,45,68,5,STEEL);line(g,-6,116,45,66,1,STEELL);line(g,96,116,45,66,1,STEELL);
 R(g,0,62,WW,8,STEEL);R(g,0,62,WW,2,STEELL);R(g,0,69,WW,1,STEELD);
 R(g,32,60,26,20,INKC);R(g,33,61,24,18,'#8a94a6');for(const bx of[36,41,48,53])for(const by of[64,70,75]){R(g,bx,by,2,2,'#d9dee8')}
 const n=Math.floor(cl01(q/3.6)*24);R(g,33,61,n,18,'#b9c2d2');R(g,33,61,n,1,'#e6ebf4');if(n>1){R(g,33+n-1,61,1,18,'#f0a040')}
 for(let y=FL;y<WH;y++)R(g,0,y,WW,1,(y-FL)%6==0?'#2a2e44':'#343a54');for(let x=0;x<WW;x+=9)R(g,x,FL,1,40,'#2a2e44');
 // work light on a stand
 R(g,78,96,1,24,'#4a5262');R(g,75,92,7,5,'#f4ecd8');R(g,74,119,9,1,'#4a5262');
 const j=Math.round(Math.sin(q*11)),br=Math.sin(t*2.3)>.5?-1:0,HY=GY-39,rx=CX+8+Math.round(Math.sin(q*1.7)*1.5);
 // seen from behind: both arms reach up and forward past the head, so only the raised forearms show, outside the head
 const P={hip:GY-17,feet:[[-4,0],[4,0]],sl:1,sa:[1,1],hands:[[CX-9,HY-3],[rx,HY-2+j]],hy:br,nobag:true,
  back:(gg,i)=>{const h=i.h[1];line(gg,h[0],h[1],h[0]-2,h[1]-5,1,'#c9c9d2')},
  front:(gg,i)=>{R(gg,CX-7,i.hy-4+br,14,5,'#3a3a44');R(gg,CX-7,i.hy-4+br,14,1,'#5a5a66')}};
 const inf=personFB(P,13,0,LOOK.weld,'b');
 const sx=13+inf.h[1][0]-2,sy=OY+inf.h[1][1]-6;if(Math.floor(t*30)%3!=0){R(g,sx-1,sy-1,3,3,'#ffffff');for(let k=0;k<12;k++){const a=k*1.7+t*9,r=((t*40+k*7)%14);px(g,sx+Math.cos(a)*r*.7,sy+Math.abs(Math.sin(a))*r+r*.5,k%2?'#fff6c0':'#ffb040')}}
 return{sx,sy}}
// the storm track
function coastX(y){return 16+(160-y)*.36+(y>122&&y<134?5-Math.abs(y-128)*.8:0)+Math.round(Math.sin(y*.35)*1.2)}
function sceneElla(q,t){const g=wg;R(g,0,0,WW,56,NAVY);for(let y=56;y<WH;y++){R(g,0,y,WW,1,mixc('#1f4f8a','#17396b',(y-56)/104));const cx=Math.round(coastX(y));R(g,0,y,cx,1,(y%9<5)?'#7da06a':'#74976a');px(g,cx,y,'#d9cfa0');px(g,cx+1,y,'#3f77b8')}
 g.globalAlpha=.12;for(let x=5;x<WW;x+=14)R(g,x,56,1,104,'#cfe2ff');for(let y=62;y<WH;y+=14)R(g,0,y,WW,1,'#cfe2ff');g.globalAlpha=1;
 const ny=88,nx=Math.round(coastX(ny));R(g,nx+3,ny-2,13,2,'#7da06a');R(g,nx+3,ny,10,1,'#d9cfa0');
 const bl=Math.sin(t*8)>0;R(g,nx-3,ny-2,5,5,INKC);R(g,nx-2,ny-1,3,3,bl?CORAL:'#fffaf0');ptext(g,'NEW YORK',3,ny-10,'#fffaf0');
 // track: north along the coast, then a hard turn east
 const pts=[[62,156],[61,140],[58,124],[55,110],[57,100],[66,93],[80,88],[98,84]],u=cl01(q/4.3),turn=q>2.9;
 const pos=u=>{const f=u*(pts.length-1),i=Math.min(pts.length-2,Math.floor(f)),a=f-i;return[lerp(pts[i][0],pts[i+1][0],a),lerp(pts[i][1],pts[i+1][1],a)]};
 for(let k=0;k<=40;k++){const v=k/40;if(v>u)break;const p=pos(v);if(k%2==0)px(g,p[0],p[1],'#fffaf0')}
 if(!turn){const p0=pos(u);for(let k=1;k<7;k++)if((k+Math.floor(t*6))%2)px(g,lerp(p0[0],nx+2,k/7),lerp(p0[1],ny,k/7),CORAL)}
 const p=pos(u);spiral(g,p[0],p[1],11,-t*5,'#eef4ff');ptext(g,'ELLA',Math.min(72,Math.round(p[0])-7),Math.round(p[1])-19,'#eef4ff');
 return{}}
const HEADS=[[0.05,2.88,"WHY IS THIS TOWER",["ON STILTS?"]],
 [5.83,7.5,"THE CORNER",["WAS TAKEN."]],[7.5,10.23,"SO THE LEGS MOVED",["TO THE MIDDLE","OF EACH SIDE"]],
 [10.25,12.78,"A STUDENT CALLS",["ONE QUESTION"]],[12.8,14.63,"WHAT IF THE WIND",["HITS THE CORNER?"],{tc:CORAL}],
 [14.65,15.98,"THE ENGINEER",["RAN THE NUMBERS"]],[16.0,19.75,"AGAINST A CORNER WIND",["FAR WEAKER","THAN DESIGNED"],{tc:CORAL}],
 [19.77,22.3,"BY HIS MATH",["EVEN WITH","EVERYTHING WORKING"]],[22.32,25.76,"A TOPPLING STORM",["1 IN 55","EACH YEAR"],{tc:CORAL}],
 [25.78,26.9,"YOU ARE",["THE ENGINEER"]],[26.9,28.93,"THREE OPTIONS",["WHICH ONE?"],{tc:AMBER}],
 [28.95,34.83,"OPTION A",["TRUST THE","DAMPER"],{tc:AMBER}],[34.85,41.72,"OPTION B",["WAIT FOR","WINTER"],{tc:AMBER}],[41.74,48.9,"OPTION C",["CONFESS, AND","FIX IT AT NIGHT"],{tc:AMBER}],
 [51.97,53.75,"PLAY OUT A",["TRUST THE DAMPER"]],[53.77,56.1,"BUT IT RUNS ON",["ELECTRICITY"],{tc:CORAL}],[56.12,59.6,"POWER OUT",["1 IN 16","EACH YEAR"],{tc:CORAL}],
 [59.62,61.6,"PLAY OUT B",["WAIT FOR WINTER"]],[61.62,64.83,"THAT SAME SEASON",["HURRICANE ELLA"],{tc:CORAL}],
 [64.85,66.6,"PLAY OUT C",["HE CONFESSED"],{tc:MINT}],[66.62,68.4,"THE FLAW",["WAS IN THE JOINTS"]],[68.42,69.5,"DRAWN AS",["WELDS"],{tc:MINT}],[69.5,70.85,"BUILT WITH",["BOLTS"],{tc:CORAL}],
 [70.87,74.19,"NIGHT AFTER NIGHT",["STEEL PLATES","OVER THE BOLTS"]],
 [74.21,76.4,"HALF DONE WHEN",["ELLA CAME"],{tc:CORAL}],[76.42,77.76,"THEN IT",["TURNED AWAY"],{tc:MINT}],
 [80.53,83.7,"RULE UNLOCKED",["CHECK THE","DIAGONAL WIND"],{tc:MINT}],[83.74,END,"LEVEL 03",["CLEARED"],{tc:MINT}]];
function heart(x,y,full){og.fillStyle=full?CORAL:'#3a3668';const u=7;[[1,0,2,1],[4,0,2,1],[0,1,7,2],[1,3,5,1],[2,4,3,1],[3,5,1,1]].forEach(([a,b,w,h])=>og.fillRect(x+a*u,y+b*u,w*u,h*u))}
function badge(L,t0,t){const a=ease(seg(t,t0,t0+.18));if(a<=0)return;const p=1+.35*(1-a);og.save();og.translate(150,830);og.scale(p,p);og.globalAlpha=a;og.fillStyle=INKC;rrect(og,-78,-78,156,156,24);og.fill();og.fillStyle=AMBER;rrect(og,-66,-66,132,132,18);og.fill();mdraw(L,0,6,110,INKC,'center',false,'',0,a);og.restore()}
function hud(t){const DONE=83.7,done=t>=DONE,pr=cl01(t/DONE),y=566,s=84,gap=18,x0=250,a=ease(seg(t,2.91,3.3));if(a<=0)return;og.save();og.globalAlpha=a;
 mdraw("LV 3",60,y+s/2+2,40,MINT,'left',false,'',0,a);
 for(let i=0;i<5;i++){const x=x0+i*(s+gap),ok=i<2||(i==2&&done),cur=i==2&&!done;og.globalAlpha=a;og.fillStyle=ok?'#173a2c':'#1b1838';rrect(og,x,y,s,s,12);og.fill();
  if(cur){og.save();rrect(og,x,y,s,s,12);og.clip();og.fillStyle='#2a4a7a';og.fillRect(x,y+s*(1-pr),s,s*pr);og.restore()}
  const nxt=i==3&&t>85.9;og.lineWidth=4;og.strokeStyle=ok?MINT:cur?CORAL:(nxt&&Math.sin(t*10)>0?AMBER:'#3a3668');rrect(og,x,y,s,s,12);og.stroke();
  if(ok){og.strokeStyle=MINT;og.lineWidth=9;og.lineCap='round';og.beginPath();og.moveTo(x+22,y+44);og.lineTo(x+37,y+59);og.lineTo(x+63,y+27);og.stroke()}
  else mdraw(cur?"03":"?",x+s/2,y+s/2+2,cur?34:38,cur?CREAM:(nxt?AMBER:'#5a568a'),'center',false,'',0,a)}
 const lives=t<58.0?3:t<63.6?2:1;for(let i=0;i<3;i++)heart(800+i*76,y+20,i<lives);og.restore()}
function frameAt(t){
 QA.chars=[];QA.solids=[];og.imageSmoothingEnabled=false;og.clearRect(0,0,1080,1920);
 const sg=SEG.find(s=>t>=s[0]&&t<s[1])||SEG[SEG.length-1],id=sg[4],o=sg[2]+(t-sg[0])*(sg[3]-sg[2])/(sg[1]-sg[0]);QA.shot=sg[5];let sh=0,inf={};
 if(id=='tower')sceneTower(o,t);else if(id=='legs')sceneLegs(o,t);else if(id=='plan')scenePlanT(o,t);else if(id=='phone')scenePhone(o,t);else if(id=='wind')sceneWind(o,t,false);
 else if(id=='face1')sceneFace(o,t,1);else if(id=='joint'){sceneJoint(o,t);sh=shake(t,69.9)}else if(id=='storm'){sceneStorm(o,t);sh=shake(t,22.4)}else if(id=='ask')sceneAsk(o,t);
 else if(id=='pA')sceneDamper(o,t,false);else if(id=='pB')sceneCalW(o,t);else if(id=='pC')sceneStorm(o,t,true);else if(id=='choice')sceneChoice(o,t);
 else if(id=='A'){inf=sceneDamper(o,t,true);sh=shake(t,54.25)+shake(t,58.0)}else if(id=='B'){sceneElla(o,t);sh=shake(t,63.6)}else if(id=='bank')sceneBank(o,t);else if(id=='weld')inf=sceneWeld(o,t);
 else if(id=='ella')sceneElla(o,t);else if(id=='face2')sceneFace(o,t,2);else if(id=='today')sceneWind(o,t,true);else sceneWin(o);
 og.drawImage(wc,0,0,WW,WH,sh,0,1080,1920);
 lit(()=>{
  if(id=='tower'||id=='legs')glow(900,760,640,SUN,.26);
  else if(id=='plan'||id=='wind'||id=='today'||id=='choice'||id=='ask')glow(540,1100,760,COOL,.16);
  else if(id=='phone'){glow(230,920,460,SUN,.24);glow(840,1250,420,WARM,.14)}
  else if(id=='face1'){glow(200,900,520,COOL,.2);grade('#3a3a70',.28,'multiply')}
  else if(id=='joint'){if(o<1.93)glow(540,1100+o*180,420,FIRE,.4);else glow(540,1250,620,RED,.14*ease(seg(o,2.1,2.6)))}
  else if(id=='storm')glow(540,1000,700,COOL,.14);
  else if(id=='pA')glow(540,1380,620,WARM,.3);
  else if(id=='A'){if(inf.off){glow(200,1000,300,RED,.3*(Math.sin(t*9)>0?1:.2))}else glow(540,1380,620,WARM,.3)}
  else if(id=='pB')glow(540,1100,700,WARM,.16);
  else if(id=='pC'){glow(860,790,300,SUN,.2);glow(540,1000,520,WARM,.16)}
  else if(id=='bank')glow(840,900,560,WARM,.24);
  else if(id=='weld'){const f=Math.floor(t*30)%3!=0?1:.35;glow(inf.sx*12,inf.sy*12,520,FIRE,.5*f);glow(inf.sx*12,inf.sy*12,160,SUN,.6*f);glow(940,1130,300,SUN,.25);grade('#0a0c1e',.18,'multiply')}
  else if(id=='ella'||id=='B'){glow(540,1100,800,COOL,.12);if(id=='B')grade('#c0503f',.18*ease(seg(t,63.6,64.1)),'multiply')}
  else if(id=='face2'){glow(200,900,620,SUN,.34)}
  else glow(70*12,66*12,520,SUN,.45)});
 const v=og.createLinearGradient(0,0,0,1920);v.addColorStop(0,'rgba(0,0,0,.22)');v.addColorStop(.3,'rgba(0,0,0,0)');v.addColorStop(.8,'rgba(0,0,0,0)');v.addColorStop(1,'rgba(0,0,0,.35)');og.fillStyle=v;og.fillRect(0,0,1080,1920);
 og.globalAlpha=.6;og.fillStyle='#0f0d22';og.fillRect(0,110,1080,562);og.globalAlpha=1;
 const h=HEADS.find(h=>t>=h[0]&&t<h[1]);
 if(id=='legs'){const yr=Math.round(lerp(2026,1978,ease(seg(t,3.86,5.0))));header(t<3.86?"LEVEL 03":"NEW YORK",[t<3.86?"THE TOWER":String(yr)],(t-2.91)/.2,{tc:t>5.0||t<3.86?AMBER:CREAM})}
 else if(id=='choice'){const q=t-48.9,n=3-Math.min(2,Math.floor(Math.max(0,q-.25)/.92)),p=1+.25*(1-ease(seg(((Math.max(0,q-.25))%.92),0,.2)));header("LOCK IT IN",[],1);og.save();og.translate(540,330);og.scale(p,p);mdraw(String(n),0,0,220,AMBER,'center',true,INKC,20,1);og.restore()}
 else if(id=='face2'){const yr=Math.round(lerp(1978,1995,ease(seg(t,78.0,79.7))));header("KEPT QUIET UNTIL",[String(yr)],(t-77.76)/.2,{tc:AMBER})}
 else if(h)header(h[2],h[3],(t-h[0])/.2,h[4]);
 hud(t);
 if(id=='pA')badge("A",29.6,t);if(id=='pB')badge("B",35.55,t);if(id=='pC')badge("C",42.45,t);
 if(id=='A')badge("A",52.0,t);if(id=='B')badge("B",59.65,t);if(id=='bank'||id=='joint'||id=='weld')badge("C",64.9,t);
 if(id=='joint'&&t>=69.9)stamp("NOT AS DRAWN",'#e0473c',640,860,69.9,t,-.07,56);
 if(id=='choice'){const L=[["A","TRUST THE DAMPER"],["B","WAIT FOR WINTER"],["C","CONFESS, FIX AT NIGHT"]];
  L.forEach(([a,s],k)=>{const y=(69+k*20)*12;mdraw(a,26.5*12,y+2,56,AMBER,'center',true,INKC,10,1);mdraw(s,31*12,y+2,fit(s,40,600),CREAM,'left',false,'',0,1)})}
 if(id=='A'&&t>=58.0)stamp("A FAILS",'#e0473c',640,860,58.0,t,-.07,64);
 if(id=='B'&&t>=63.6)stamp("B FAILS",'#e0473c',640,860,63.6,t,-.07,64);
 if(id=='weld'&&t>=73.1)stamp("C WORKED",'#2fbf8f',640,1330,73.1,t,-.07,60);
 if(id=='win'){const xp=Math.round(100*ease(seg(t,83.9,84.6)));mdraw("+"+xp+" XP",540,800,70,AMBER,'center',true,INKC,14,1);
  if(t>84.91&&t<85.9)tag("COMMENT A, B OR C",540,1400,AMBER,ease(seg(t,84.91,85.06)));if(t>=85.9)tag("FOLLOW FOR LEVEL 04",540,1400,MINT,ease(seg(t,85.9,86.07)))}
 subtitle(t,false);for(const c of CUTS)wipe(t,c,.12);
}
window.frame=i=>frameAt(i/30);
Promise.all([document.fonts.load('700 40px Silk'),document.fonts.load('400 40px PS2P')]).then(()=>{window.READY=true});
