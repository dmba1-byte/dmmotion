// ===== Mission 01 : "The door a crowd can open" — Carl Prinzler and the panic bar =====
const T={s2:4.85,s3:7.38,s3b:9.87,s4:14.42,s4b:16.15,s5:19.26,s5b:20.55,s6:23.61,s6b:26.39,s6c:28.08,s7:29.85,s7b:34.3,s8:36.36,end:39.4};
const SUBS=[[0.13,0.75,"Your mission:"],[0.84,2.95,"build a locked door that opens with no key,"],[3.15,4.6,"no knob, and no hands."],
[4.85,5.85,"In 1903,"],[6.03,7.1,"that was impossible."],
[7.38,9.4,"Carl Prinzler sold door hardware."],[9.87,12.55,"He planned to see a show at Chicago's Iroquois Theatre,"],[12.8,14.15,"then changed his plans."],
[14.42,15.75,"That afternoon, it burned."],[16.15,17.1,"The exits were locked,"],[17.16,18.95,"and about 600 people died."],
[19.26,20.2,"He couldn't let it go."],[20.55,23.15,"But how do you let a crowd out, and still keep the door locked?"],
[23.61,25.05,"Five years later, with an architect neighbor,"],[25.09,26.0,"he had it."],[26.39,27.8,"One bar, across the door."],[28.08,29.55,"Lean on it, and it opens."],
[29.85,31.9,"Today, building codes require that bar"],[31.9,34.15,"on the exits of theaters and schools"],[34.46,36.05,"that hold 50 people or more."],
[36.36,37.2,"Mission complete."],[37.41,38.65,"Follow for mission two."]];
LOOK.carl={id:'carl',skin:'#e9c3a3',skinD:'#c99d7e',hair:'#3a2a20',top:'#6a4a3a',topL:'#8a6a54',pants:'#3a3540',shoe:'#1e1c24'};
LOOK.dup={id:'dup',skin:'#f0caa8',skinD:'#d2a886',hair:'#8a6a3a',top:'#5a6478',topL:'#76829a',pants:'#3a4050',shoe:'#1e1c24'};
const KID={hw:10,hh:10,th:7,sh:6,tl:8,ua:5,fa:5,tw:7,foot:4,lw:3};
LOOK.k1=Object.assign({},LOOK.girl,{id:'k1'});LOOK.k2=Object.assign({},LOOK.a1,KID,{id:'k2'});LOOK.k3=Object.assign({},LOOK.a2,KID,{id:'k3'});LOOK.k4=Object.assign({},LOOK.a4,KID,{id:'k4',top:'#e07a5a',topL:'#f09a7a'});
const HAT='#2a2430';
const carlF=hat=>(g,i)=>{R(g,i.hx+i.hw-6,i.hy+8,5,1,LOOK.carl.hair);if(hat){R(g,i.hx-1,i.hy-6,i.hw+2,5,HAT);R(g,i.hx-1,i.hy-6,i.hw+2,1,'#423a4c');R(g,i.hx-3,i.hy-1,i.hw+7,1,HAT)}};
const dupF=(g,i)=>{glasses(g,i)};

// front/back character with shadow + QA
function personFB(P,ox,oy,look,v){const sv=Object.assign({},K);Object.assign(K,look||{});if(look&&P.nobag==null)P.nobag=true;
 const cx=Math.round(ox)+CX,gy=FL-Math.round(oy||0);wg.globalAlpha=.22;R(wg,cx-8,gy,16,1,'#000');R(wg,cx-6,gy+1,12,1,'#000');wg.globalAlpha=1;
 const ch=mk();let inf;try{inf=kitFB(ch.getContext('2d'),P,v)}finally{Object.assign(K,sv)}outline(ch);wg.drawImage(ch,Math.round(ox),OY-Math.round(oy||0));
 QA.chars.push({k:'fb'+((look&&look.id)||'kit'),x:Math.round(ox),cx,oy:0,flip:false,fb:true,ok:!!P.okOverlap,bent:!(P.sl&&(P.sa||P.armJ)),sig:JSON.stringify([P.hip,P.feet,P.hands,P.hy,P.mouth])});return inf}

// big face close-up
function portrait(g,L,o){o=o||{};const cx=45+(o.dx||0),top=72+(o.dy||0);
 R(g,cx-27,top+52,54,60,L.top);R(g,cx-27,top+52,54,2,L.topL);R(g,cx-27,top+52,3,60,shade(L.top,.8));R(g,cx+24,top+52,3,60,shade(L.top,.8));
 if(o.shirt){R(g,cx-9,top+52,18,60,'#f4ecd8');line(g,cx-9,top+52,cx-3,top+74,2,shade(L.top,.7));line(g,cx+8,top+52,cx+2,top+74,2,shade(L.top,.7));R(g,cx-2,top+54,4,5,o.tie||'#8a3c2c');R(g,cx-1,top+59,3,30,o.tie||'#8a3c2c')}
 R(g,cx-6,top+42,12,11,L.skinD);
 R(g,cx-18,top,36,44,L.skin);R(g,cx-17,top+44,34,1,L.skinD);R(g,cx-20,top+17,2,9,L.skinD);R(g,cx+18,top+17,2,9,L.skinD);
 R(g,cx-19,top-4,38,9,L.hair);R(g,cx-19,top,4,16,L.hair);R(g,cx+15,top,4,16,L.hair);R(g,cx-10,top+4,14,2,L.hair);
 if(o.hat){R(g,cx-18,top-16,36,15,HAT);R(g,cx-18,top-16,36,2,'#423a4c');R(g,cx-16,top-18,32,2,HAT);R(g,cx-25,top-2,50,3,HAT);R(g,cx-18,top-5,36,3,'#6a5a4a')}
 const br=o.brow||0;R(g,cx-12,top+14,8,2,L.hair);R(g,cx+4,top+14,8,2,L.hair);
 if(br){R(g,cx-12,top+14,3,1,L.skin);R(g,cx+9,top+14,3,1,L.skin);R(g,cx-6,top+13,2,1,L.hair);R(g,cx+4,top+13,2,1,L.hair)}
 if(o.blink){R(g,cx-11,top+22,7,1,INKC);R(g,cx+4,top+22,7,1,INKC)}
 else{R(g,cx-11,top+19,7,6,'#fffaf0');R(g,cx+4,top+19,7,6,'#fffaf0');const ex=o.ex||0,ey=o.ey||0;R(g,cx-9+ex,top+20+ey,3,4,INKC);R(g,cx+6+ex,top+20+ey,3,4,INKC);px(g,cx-9+ex,top+20+ey,'#fff');px(g,cx+6+ex,top+20+ey,'#fff')}
 R(g,cx-1,top+24,3,6,L.skinD);
 const m=o.mouth||'flat';
 if(m=='smile'){R(g,cx-6,top+37,12,2,'#8a4a40');R(g,cx-8,top+36,2,1,'#8a4a40');R(g,cx+6,top+36,2,1,'#8a4a40')}
 if(m=='flat')R(g,cx-5,top+37,10,2,'#8a4a40');
 if(m=='open'){R(g,cx-5,top+35,10,6,'#6a2630');R(g,cx-4,top+35,8,2,'#fffaf0')}
 if(o.stache){R(g,cx-9,top+31,18,3,L.hair);R(g,cx-11,top+33,4,3,L.hair);R(g,cx+7,top+33,4,3,L.hair)}
 if(o.glasses){for(const gx of[cx-13,cx+2]){R(g,gx,top+17,11,1,INKC);R(g,gx,top+26,11,1,INKC);R(g,gx,top+17,1,10,INKC);R(g,gx+10,top+17,1,10,INKC)}R(g,cx-2,top+20,4,1,INKC)}
 g.globalAlpha=.25;R(g,cx-14,top+29,5,3,'#e07a6a');R(g,cx+9,top+29,5,3,'#e07a6a');g.globalAlpha=1;
}

// ---------- the mission hall: a world drawn on blueprint ----------
function blueprintWall(g,t){
 R(g,0,0,WW,56,NAVY);
 for(let y=56;y<FL;y++)R(g,0,y,WW,1,mixc('#21468a','#17336e',(y-56)/64));
 g.globalAlpha=.16;for(let x=2;x<WW;x+=8)R(g,x,56,1,64,'#9fc3ff');for(let y=60;y<FL;y+=8)R(g,0,y,WW,1,'#9fc3ff');g.globalAlpha=1;
 const c='#cfe2ff';g.globalAlpha=.6;
 for(let k=0;k<5;k++){R(g,3+k*4,104-k*4,4,1,c);R(g,3+k*4,104-k*4,1,4,c)}R(g,2,108,22,1,c); // stair section
 R(g,3,113,20,1,c);R(g,3,111,1,5,c);R(g,22,111,1,5,c); // dimension
 for(let k=0;k<2;k++){const x=6+k*12;R(g,x,62,3,1,c);R(g,x,64,3,1,c);px(g,x-1,63,c);px(g,x+3,63,c);R(g,x+1,65,1,6,c)} // grid bubbles
 for(let a=0;a<=90;a+=8)px(g,68+Math.cos(rad(a))*14,100-Math.sin(rad(a))*14,c);R(g,68,86,1,15,c);R(g,68,100,15,1,c); // door swing symbol
 R(g,66,64,20,1,c);R(g,66,64,1,10,c);R(g,85,64,1,10,c);R(g,66,73,20,1,c);R(g,70,67,12,1,c);R(g,70,70,8,1,c); // title block
 g.globalAlpha=1;
 const sx=(t*16)%130-20;g.globalAlpha=.09;R(g,sx,56,7,64,'#e8f3ff');g.globalAlpha=1;
 for(let y=FL;y<WH;y++)R(g,0,y,WW,1,mixc('#142d62','#0c1c44',(y-FL)/40));
 g.globalAlpha=.3;R(g,0,FL,WW,1,'#cfe2ff');for(let y=FL+5;y<WH;y+=8)R(g,0,y,WW,1,'#9fc3ff');for(let x=-60;x<WW+60;x+=12)line(g,45+(x-45)*.6,FL,45+(x-45)*1.7,WH,1,'#9fc3ff');g.globalAlpha=1;
 for(let k=0;k<9;k++){const x=(k*23+7)%WW,y=118-((t*6+k*17)%60);g.globalAlpha=.5;px(g,x,y,'#e8f3ff');g.globalAlpha=1}
}
function bigDoor(g,x,jit,o){o=o||{};x+=jit||0;const y=58,w=30,h=62,lf=o.leaf||'#7a5434',pn=o.panel||'#6b4a2e',hi=o.hi||'#9a7250';
 R(g,x,y,w,h,lf);R(g,x,y,w,1,hi);R(g,x,y,1,h,hi);R(g,x+w-1,y,1,h,'#4a3220');
 for(const[px0,py0,pw,ph]of[[3,4,10,22],[17,4,10,22],[3,31,10,27],[17,31,10,27]]){R(g,x+px0,y+py0,pw,ph,pn);R(g,x+px0,y+py0,pw,1,'#4a3220');R(g,x+px0,y+py0,1,ph,'#4a3220');R(g,x+px0+pw-1,y+py0,1,ph,hi)}
 R(g,x,y+9,2,4,'#9a9aa6');R(g,x,y+48,2,4,'#9a9aa6');
 if(o.bar){R(g,x+2,y+37,w-4,3,BRASS);R(g,x+2,y+37,w-4,1,'#f4dc8a');R(g,x+2,y+35,2,7,'#8a6a2a');R(g,x+w-4,y+35,2,7,'#8a6a2a')}
 else{R(g,x+25,y+40,3,3,BRASS);px(g,x+25,y+40,'#f4dc8a');R(g,x+26,y+45,1,2,INKC)}
}
function padlock(g,x,y,a){g.globalAlpha=a;R(g,x+1,y,5,1,'#f4ecd8');R(g,x,y+1,1,4,'#f4ecd8');R(g,x+6,y+1,1,4,'#f4ecd8');R(g,x-1,y+4,9,7,CORAL);R(g,x-1,y+4,9,1,'#ffb0a0');R(g,x+3,y+6,1,3,INKC);g.globalAlpha=1}
const SHY=GY-24;
function sceneMission(t){const g=wg;blueprintWall(g,t);
 const rat=(t<1.25||(t>2.2&&t<2.85))?Math.round(Math.sin(t*46)):((t>3.3&&t<3.4)||(t>3.62&&t<3.72)?1:0);
 R(g,27,55,36,65,'#0c1c44');R(g,27,55,36,1,'#cfe2ff');R(g,27,55,1,65,'#cfe2ff');R(g,62,55,1,65,'#cfe2ff');
 bigDoor(g,30,rat);padlock(g,41,62,.75+.25*Math.sin(t*5));
 const br=Math.sin(t*2.4)>.5?-1:0;
 if(t<3.95){let hands=[[CX-8,SHY+10],[CX+8,SHY+10]];
  if(t<1.25||(t>2.2&&t<2.85))hands=[[CX-8,SHY+10],[CX+10+rat,SHY+3]];
  else if(t>=3.15)hands=[[CX-6,SHY-1+(rat?1:0)],[CX+6,SHY-1+(rat?1:0)]];
  else hands=[[CX-8,SHY+10+br],[CX+8,SHY+10+br]];
  personFB({hip:GY-17,feet:[[-3,0],[3,0]],sl:1,sa:[1,1],hands,hy:(t>1.25&&t<2.2)?-1:br},13,(t>=3.15&&rat)?1:0,null,'b')}
 else{const sh=Math.round(Math.sin((t-3.95)*7)*1);
  personFB({hip:GY-17,feet:[[-3,0],[3,0]],sl:1,sa:[1,1],hands:[[CX-14,SHY+5+sh],[CX+13,SHY+5+sh]],mouth:'open',hy:br},13,0,null,'f')}
 if(t>=T.s2&&t>6.4){} return{}}
// ---------- Carl, close-up, in the shop ----------
function shelves(g,dim){
 for(let y=56;y<WH;y++)R(g,0,y,WW,1,'#6a4c30');for(let x=0;x<WW;x+=15)R(g,x,56,1,104,'#5a3e28');
 for(const s of[80,108,138]){R(g,0,s,WW,3,'#4a3220');R(g,0,s,WW,1,'#8a6a4a');
  for(let k=0;k<8;k++){const x=1+k*12,h=10+((k*7+s)%9),col=['#b8865a','#8a9aa8','#c9a24a','#6e7a7a','#a8503c'][(k+s)%5];R(g,x,s-h,9,h,col);R(g,x,s-h,9,2,shade(col,1.25));R(g,x+2,s-h+4,5,3,'#f4ecd8')}}
 for(let k=0;k<7;k++){const x=5+k*13;R(g,x,57,1,5,'#3a3a44');R(g,x-1,62,3,3,BRASS);R(g,x,65,1,5,BRASS);px(g,x+1,68,BRASS)} // keys on hooks
 g.globalAlpha=dim;R(g,0,56,WW,104,'#1a1008');g.globalAlpha=1}
function sceneCarl(t){const g=wg;R(g,0,0,WW,56,NAVY);shelves(g,.42);
 const bl=(t%2.6)<.12,bob=Math.round(Math.sin(t*2.2));
 portrait(g,LOOK.carl,{stache:1,shirt:1,blink:bl,ex:t<8.5?1:0,ey:t<8.5?1:0,mouth:'smile',dy:bob>0?1:0});
 // he holds up a brass doorknob
 const hy=106+Math.round(Math.sin(t*3)*1.5),hx=74;
 R(g,hx-1,hy+6,11,40,INKC);R(g,hx,hy+7,9,40,LOOK.carl.top);R(g,hx,hy+7,9,2,'#f4ecd8');
 R(g,hx-1,hy-1,11,9,INKC);R(g,hx,hy,9,7,LOOK.carl.skin);R(g,hx,hy+2,9,1,LOOK.carl.skinD);R(g,hx,hy+4,9,1,LOOK.carl.skinD);
 R(g,hx+2,hy-5,5,5,INKC);R(g,hx+3,hy-4,3,4,'#8a6a2a');
 R(g,hx-2,hy-15,13,11,INKC);R(g,hx-1,hy-14,11,9,BRASS);R(g,hx-1,hy-14,11,2,'#f4dc8a');R(g,hx+7,hy-12,2,6,'#b08a2a');
 const gl=Math.floor(t*6)%5;px(g,hx+1+gl,hy-12,'#fffbe0');px(g,hx+2+gl,hy-11,'#fffbe0');
 return{}}
// ---------- Chicago street, Dec 30 1903 ----------
function theatre(g,x,t,fire){const st=fire?'#8a8592':'#cfc6b4',stL=fire?'#a19caa':'#e4dccb',stD=fire?'#68636f':'#b0a692';
 R(g,x,58,84,62,st);R(g,x,58,84,1,stL);R(g,x-2,56,88,3,stD);R(g,x-2,56,88,1,stL);
 for(const p of[2,22,58,78]){R(g,x+p,60,4,60,stL);R(g,x+p+3,60,1,60,stD)}
 const fl=fire?.6+.4*Math.sin(t*9)*Math.sin(t*5.3):0;const wcol=fire?mixc('#c8501e','#ffb040',cl01(fl)):'#f0d890';
 for(let i=0;i<24;i++){const hh=Math.round(Math.sqrt(144-(i-12)*(i-12))*.9);R(g,x+30+i,76-hh,1,hh+4,'#2a2a3a');if(i>1&&i<22)R(g,x+30+i,77-hh,1,hh+1,wcol)}
 R(g,x+41,64,1,16,'#2a2a3a');R(g,x+32,72,20,1,'#2a2a3a');
 for(const p of[8,14,64,70]){R(g,x+p,62,5,12,'#2a2a3a');R(g,x+p+1,63,3,10,fire?mixc('#8a3a1e','#ff9a40',cl01(fl*.8+.1*Math.sin(t*7+p))):'#f0d890')}
 R(g,x+22,82,40,9,HAT);R(g,x+22,82,40,1,'#4a4254');ptext(g,'IROQUOIS',x+27,84,fire?'#8a8490':'#ffe6a0');
 R(g,x+14,92,56,3,'#3a3040');R(g,x+14,92,56,1,'#5a4e62');
 if(!fire)for(let k=0;k<18;k++)px(g,x+16+k*3,95,(k+Math.floor(t*6))%3?'#8a7a50':'#fff2b0');
 for(let k=0;k<4;k++){const dx=x+19+k*12;R(g,dx,98,10,22,'#3a2a20');R(g,dx+1,99,8,20,'#5a3e28');R(g,dx+2,100,6,8,fire?'#2a2228':'#b9c8d8');R(g,dx+5,99,1,20,'#3a2a20');if(fire){R(g,dx+3,110,5,4,CORAL);R(g,dx+4,108,3,2,'#f4ecd8');px(g,dx+5,109,'#3a2a20')}}
 for(const p of[7,70]){R(g,x+p,100,8,13,'#3a3040');R(g,x+p+1,101,6,11,fire?'#6a6470':'#e8d8a8');R(g,x+p+2,103,4,4,fire?'#5a5560':'#c45a5a')}
 R(g,x+12,118,60,2,stL);
 if(fire){for(let k=0;k<18;k++){const age=((t*.32+k/18)%1),sx=x+26+((k*13)%30)+age*16+Math.sin(t+k)*2,sy=58-age*50,sz=5+Math.round(age*9);g.globalAlpha=.55*(1-age);R(g,sx,sy,sz,sz-2,'#3e3a46');R(g,sx+1,sy-1,sz-2,sz,'#3e3a46');g.globalAlpha=1}
  for(let k=0;k<8;k++){const age=((t*.7+k/8)%1);g.globalAlpha=1-age;px(g,x+30+((k*11)%26)+Math.sin(t*2+k)*3,60-age*34,'#ffb040');g.globalAlpha=1}}
}
function street(g,cam,t){
 for(let y=0;y<FL;y++)R(g,0,y,WW,1,mixc('#7f8fb0','#d8cfd2',y/FL));R(g,0,0,WW,56,NAVY);
 for(let k=0;k<10;k++){const x=((k*16-Math.round(cam*.25))%160+160)%160-16,h=18+(k*37)%20;R(g,x,FL-28-h,13,h+28,'#8d93ad');R(g,x,FL-28-h,13,1,'#a3a9c0');for(let j=0;j<4;j++)if((k+j)%3)px(g,x+3+(j%2)*5,FL-24-h+j*5,'#f0d890')}
 const S_=wx=>wx-Math.round(cam);
 let x=S_(-12);R(g,x,58,56,62,'#8a5040');R(g,x,58,56,1,'#a86654');for(let y=62;y<98;y+=4)R(g,x,y,56,1,'#7a4436');
 for(let r=0;r<3;r++)for(let c=0;c<4;c++){R(g,x+5+c*13,62+r*12,7,9,'#3a3a4a');R(g,x+6+c*13,63+r*12,5,7,(r+c)%2?'#f0d890':'#6a7a9a');R(g,x+5+c*13,71+r*12,7,1,'#f6f8ff')}
 R(g,x+2,99,52,3,'#2f6a3a');R(g,x+2,99,52,1,'#f6f8ff');R(g,x+6,104,22,14,'#3a3a4a');R(g,x+7,105,20,12,'#e8c87a');R(g,x+34,102,12,18,'#5a3e28');R(g,x+36,104,8,7,'#b9c8d8');
 theatre(g,S_(50),t,false);
 x=S_(140);R(g,x,58,100,62,'#b9b2a6');R(g,x,58,100,1,'#d3ccc0');
 for(let i=0;i<20;i++){const hh=Math.round(Math.sqrt(100-(i-10)*(i-10)));R(g,x+30+i,96-hh,1,hh+24,'#3a3040')}R(g,x+36,66,8,8,'#f4ecd8');px(g,x+40,70,INKC);R(g,x+40,67,1,3,INKC);R(g,x+40,70,2,1,INKC);
 R(g,x+2,70,38,10,'#1f3a2a');R(g,x+2,70,38,1,'#f6f8ff');ptext(g,'TRAINS >',x+6,73,'#ffe6a0');
 R(g,0,FL,WW,40,'#dfe4ec');R(g,0,FL,WW,1,'#b9c0cc');for(let y=FL+4;y<WH;y+=6)for(let x2=((y*7)%13)-(Math.round(cam)%13);x2<WW;x2+=13)R(g,x2,y,3,1,'#c9d0dc');
 for(const lx of[36,128,206]){const x3=S_(lx);R(g,x3,74,1,46,'#2a2a34');R(g,x3-2,70,5,5,'#2a2a34');R(g,x3-1,71,3,3,'#ffe6a0');R(g,x3-2,69,5,1,'#f6f8ff');R(g,x3-1,119,3,1,'#2a2a34')}
}
function sceneStreet(t){const g=wg,u=seg(t,T.s3b,T.s4),cam=lerp(0,96,u);street(g,cam,t);
 const ox=lerp(-8,24,u),dist=ox+cam;const has=t<12.9;
 const P=walkP(dist,has?{armRel:[[6,lerp(1,7,ease(seg(t,12.5,12.9)))],null]}:{});P.look=t<12.2?1:0;
 const inf=person(P,ox,0,LOOK.carl,carlF(true));
 if(has){const h=handW(inf,0,ox);R(g,h[0]-1,h[1]-6,7,5,INKC);R(g,h[0],h[1]-5,5,3,'#f4ecd8');px(g,h[0]+1,h[1]-4,'#c43c3c');px(g,h[0]+3,h[1]-4,'#c43c3c');R(g,h[0]-1,h[1]-1,3,3,LOOK.carl.skin)}
 snow(g,t,44,cam);
 // foreground: a lamp post passing close to the camera
 const fx=150-Math.round(cam*1.9);R(g,fx,56,3,104,'#16141f');R(g,fx-3,150,9,10,'#16141f');
 return{cam}}
function sceneFire(t){const g=wg;
 for(let y=0;y<FL;y++)R(g,0,y,WW,1,mixc('#3a3a5a','#8a6a6a',y/FL));R(g,0,0,WW,56,NAVY);
 R(g,-10,62,14,58,'#4a3a44');R(g,86,60,10,60,'#4a3a44');
 theatre(g,3,t,true);
 R(g,0,FL,WW,40,'#aab0bc');R(g,0,FL,WW,1,'#8a90a0');for(let y=FL+4;y<WH;y+=6)for(let x2=(y*7)%13;x2<WW;x2+=13)R(g,x2,y,3,1,'#9aa0ae');
 snow(g,t,30,0);return{}}
function sceneLocked(t){const g=wg;R(g,0,0,WW,56,NAVY);
 R(g,0,56,WW,104,'#2e2a38');for(let y=60;y<WH;y+=9)R(g,0,y,WW,1,'#26222e');
 const fl=.6+.4*Math.sin(t*9)*Math.sin(t*5.3);
 R(g,6,56,78,8,mixc('#8a3a1e','#ffa040',cl01(fl)));for(let x=6;x<84;x+=13)R(g,x,56,1,8,'#1e1a22');R(g,6,64,78,2,'#1e1a22');
 for(const dx of[6,46]){R(g,dx,66,38,86,'#2f4a3a');R(g,dx,66,38,1,'#46685a');R(g,dx,66,1,86,'#46685a');R(g,dx+37,66,1,86,'#1c2e24');
  for(const[a,b,c,d]of[[5,6,28,30],[5,44,28,36]]){R(g,dx+a,66+b,c,d,'#284034');R(g,dx+a,66+b,c,1,'#1c2e24');R(g,dx+a,66+b,1,d,'#1c2e24');R(g,dx+a+c-1,66+b,1,d,'#46685a')}}
 R(g,44,66,2,86,'#16141c');
 R(g,6,152,78,2,mixc('#8a3a1e','#ffb050',cl01(fl*.9)));R(g,0,154,WW,6,'#3a3644');
 // iron slide bolt across both leaves, thrown
 R(g,26,102,38,7,'#16141c');R(g,27,103,36,5,'#4a4a56');R(g,27,103,36,1,'#7a7a88');for(const bx of[30,40,50,58]){R(g,bx,101,3,9,'#2a2a34');px(g,bx+1,102,'#8a8a96');px(g,bx+1,108,'#8a8a96')}
 R(g,43,98,5,5,'#2a2a34');R(g,44,99,3,3,'#7a7a88');
 // padlock hanging from the bolt, swaying a little
 const sw=Math.round(Math.sin(t*2.2)*1.2),lx=40+sw;
 R(g,lx+2,109,2,6,'#c9ccd4');R(g,lx+9,109,2,6,'#c9ccd4');R(g,lx+2,109,9,2,'#c9ccd4');
 R(g,lx-1,114,15,13,'#16141c');R(g,lx,115,13,11,CORAL);R(g,lx,115,13,2,'#ffb0a0');R(g,lx+5,118,3,3,INKC);R(g,lx+6,121,1,3,INKC);
 for(let k=0;k<10;k++){const age=((t*.4+k/10)%1);g.globalAlpha=.4*(1-age);R(g,10+((k*17)%70)+Math.sin(t+k)*2,64-age*10,6,3,'#5a5662');g.globalAlpha=1}
 return{}}
// ---------- the puzzle ----------
function brick(g,night){for(let y=56;y<FL;y++){R(g,0,y,WW,1,(y-56)%4==0?(night?'#3a2420':'#5a3428'):(night?'#5a3830':'#8a5040'))}
 for(let r=0;r<16;r++)for(let x=(r%2)*5;x<WW;x+=10)R(g,x,56+r*4,1,4,night?'#3a2420':'#5a3428')}
function sceneThink(t){const g=wg;R(g,0,0,WW,56,NAVY);
 for(let y=56;y<WH;y++)R(g,0,y,WW,1,(y-56)%8==0?'#2e1c18':'#4a2e28');for(let r=0;r<13;r++)for(let x=(r%2)*10;x<WW;x+=20)R(g,x,56+r*8,1,8,'#2e1c18');
 // pinned sketches behind him, crossed out
 for(let k=0;k<2;k++){const x=4+k*62;R(g,x,62,20,26,'#d9cfb8');px(g,x+10,63,'#c43c3c');for(let j=0;j<4;j++)R(g,x+3,68+j*4,14-(j%2)*4,1,'#8a8478');line(g,x+3,66,x+16,84,2,CORAL);line(g,x+16,66,x+3,84,2,CORAL)}
 const bl=(t%1.9)<.12,fl=Math.sin(t*8)*Math.sin(t*3.1);
 portrait(g,LOOK.carl,{stache:1,shirt:1,blink:bl,brow:1,ex:t<19.9?-1:1,ey:1,mouth:'flat',dy:0});
 g.globalAlpha=.10+.04*fl;R(g,45,56,45,104,'#ffb860');g.globalAlpha=.22;R(g,0,56,36,104,'#0a0814');g.globalAlpha=1;
 return{}}
function scenePlan(t){const g=wg;R(g,0,0,WW,56,NAVY);
 // top-down: the workbench
 for(let y=56;y<WH;y++)R(g,0,y,WW,1,((y-56)%13==0)?'#5a3e28':(((y-56)/13|0)%2?'#8a6640':'#916c44'));for(let k=0;k<14;k++)R(g,(k*29)%WW,58+k*7,8,1,'#7a5836');
 // drafting sheet
 g.globalAlpha=.3;R(g,10,66,60,54,'#1a1008');g.globalAlpha=1;R(g,8,63,60,54,'#efe6d0');R(g,8,63,60,1,'#fffaf0');for(const[a,b]of[[9,64],[65,64],[9,114],[65,114]])R(g,a,b,2,2,'#c43c3c');
 const ink='#2f4a7a';
 R(g,12,106,14,3,ink);R(g,52,106,12,3,ink); // wall both sides of the opening
 R(g,25,104,2,7,ink);R(g,51,104,2,7,ink); // jambs
 const u=ease(seg(t,20.7,22.5)),A=u*90;
 R(g,25,80,2,26,ink); // door leaf, open
 for(let a=0;a<=A;a+=3)px(g,26+Math.sin(rad(a))*26,106-Math.cos(rad(a))*26,ink);
 
 for(let k=0;k<3;k++)R(g,12,68+k*3,10+k*3,1,'#a9a090');
 // rejected ideas on small cards
 const cards=[[72,62,'KEY'],[72,82,'KNOB'],[72,102,'ROPE']];cards.forEach(([x,y,s],i)=>{g.globalAlpha=.3;R(g,x+1,y+2,17,16,'#1a1008');g.globalAlpha=1;R(g,x,y,17,16,'#efe6d0');ptext(g,s,x+1,y+2,'#5a5448');
  if(i==0){R(g,x+3,y+10,4,4,'#8a6a2a');R(g,x+7,y+11,7,1,'#8a6a2a');px(g,x+12,y+12,'#8a6a2a')}if(i==1){R(g,x+5,y+9,6,5,'#8a6a2a');R(g,x+7,y+14,2,1,'#8a6a2a')}if(i==2){for(let j=0;j<6;j++)px(g,x+3+j*2,y+11+(j%2),'#8a6a2a')}
  line(g,x+2,y+8,x+14,y+14,1,CORAL);line(g,x+14,y+8,x+2,y+14,1,CORAL)});
 // lock parts and an oil lamp on the bench
 R(g,4,122,8,6,INKC);R(g,5,123,6,4,BRASS);R(g,11,124,4,2,'#9a9aa6');px(g,18,126,'#9a9aa6');px(g,21,123,'#9a9aa6');
 // Carl from above: head, shoulders, both arms on the sheet
 const tipx=26+Math.sin(rad(A))*26,tipy=106-Math.cos(rad(A))*26,wob=t>22.5?Math.round(Math.sin(t*5)):0;
 const hx=tipx+3,hy=tipy+4+wob;
 R(g,27,150,36,10,INKC);R(g,28,151,34,9,LOOK.carl.top);R(g,28,151,34,1,LOOK.carl.topL);
 line(g,56,152,hx,hy,5,INKC);line(g,56,152,hx,hy,3,LOOK.carl.topL);line(g,34,152,18,116,5,INKC);line(g,34,152,18,116,3,LOOK.carl.topL);
 R(g,16,112,5,5,INKC);R(g,17,113,3,3,LOOK.carl.skin);
 R(g,hx-2,hy-2,5,5,INKC);R(g,hx-1,hy-1,3,3,LOOK.carl.skin);line(g,tipx,tipy+wob,hx+4,hy+5,1,'#e0b24a');px(g,tipx,tipy+wob,INKC);
 R(g,37,141,16,13,INKC);R(g,38,142,14,11,LOOK.carl.hair);R(g,40,143,6,1,'#5a4434');R(g,44,153,2,1,LOOK.carl.skin);
 return{}}
// ---------- five years later ----------
function workshop(g,t){R(g,0,0,WW,56,NAVY);brick(g,false);
 R(g,5,61,23,29,'#4a3220');R(g,7,63,19,25,'#bfe0f2');R(g,7,63,19,7,'#e4f3fa');R(g,16,63,1,25,'#4a3220');R(g,7,75,19,1,'#4a3220');R(g,4,90,25,2,'#6a4a30');
 // the drawing that finally worked, pinned up
 R(g,33,62,22,26,'#efe6d0');R(g,33,62,22,1,'#fffaf0');px(g,44,63,'#c43c3c');R(g,38,66,12,20,'#2f4a7a');R(g,39,67,10,18,'#efe6d0');R(g,39,76,10,2,'#c9902a');check(g,45,80,'#2f9a5a');
 R(g,60,62,19,13,'#f4ecd8');R(g,60,62,19,4,'#c43c3c');ptext(g,'1908',62,68,INKC);
 R(g,56,97,34,2,'#8a6a4a');R(g,56,97,34,1,'#a88a66');R(g,58,99,32,3,'#6a4a30');R(g,58,102,2,18,'#5a3e28');R(g,86,102,2,18,'#5a3e28');solid('table',57,90);
 R(g,62,92,8,5,'#4a4a56');R(g,63,90,3,2,'#4a4a56');R(g,74,93,10,4,BRASS);R(g,74,93,10,1,'#f4dc8a');
 for(const[x,h]of[[66,10],[72,13],[79,9],[84,12]]){R(g,x,78,1,h,'#6a4a30');R(g,x-1,78+h,3,3,'#8a8a96')}R(g,62,77,26,1,'#4a3220');
 woodFloor(g,'#8a6640','#946e46','#6b4a2e');glowRect(g,56,FL,34,4,'#2a1a10',.25)}
function sceneTwo(t){const g=wg;workshop(g,t);
 const u=ease(seg(t,T.s6,25.0)),dx=lerp(-40,-17,u),got=t>25.09;
 const pump=got?Math.round(Math.abs(Math.sin((t-25.09)*7))*3):0;
 const C_={legs:stand2,arms:[{ua:10,fa:24},{ua:8,fa:18}],lean:got?2:4,face:got?'happy':'n',mouth:'smile',look:1,dy:Math.sin(t*2.3)>.6?-1:0};
 if(got)C_.armRel=[[10,-7-pump],null];
 person(C_,14,0,LOOK.carl,carlF(false),true);
 const P=u<1?walkP(dx+40,{armRel:[[6,3],null]}):{legs:stand2,arms:[{ua:10,fa:24},{ua:8,fa:18}],armRel:[[7,got?-2:2],null],lean:4,face:got?'happy':'n',mouth:'smile',dy:Math.sin(t*2.3+1)>.6?-1:0};
 const inf=person(P,dx,0,LOOK.dup,dupF);const h=handW(inf,0,dx);
 R(g,h[0]-1,h[1]-8,4,13,INKC);R(g,h[0],h[1]-7,2,11,'#f4ecd8');R(g,h[0],h[1]-7,2,1,'#c9c0a8');R(g,h[0]-1,h[1]-1,3,3,LOOK.dup.skin);
 return{}}
function sceneBar(t){const g=wg;R(g,0,0,WW,56,NAVY);
 R(g,0,56,WW,104,'#d9cdb8');for(let x=0;x<WW;x+=18)R(g,x,56,1,104,'#cfc2ab');R(g,0,150,WW,2,'#8a7a5e');R(g,0,152,WW,8,'#7a5836');
 R(g,17,56,56,96,'#4a3220');R(g,20,56,50,96,'#7a5434');R(g,20,56,1,96,'#9a7250');R(g,69,56,1,96,'#4a3220');
 for(const x of[25,48]){R(g,x,62,18,30,'#3a2a20');R(g,x+1,63,16,28,'#cfe6f2');R(g,x+1,63,16,8,'#eaf6fb');R(g,x+9,63,1,28,'#3a2a20');R(g,x+1,77,16,1,'#3a2a20')}
 for(const x of[25,48]){R(g,x,116,18,30,'#6b4a2e');R(g,x,116,18,1,'#4a3220');R(g,x,116,1,30,'#4a3220');R(g,x+17,116,1,30,'#9a7250')}
 R(g,20,70,3,6,'#9a9aa6');R(g,20,132,3,6,'#9a9aa6');
 const u=ease(seg(t,26.45,27.0)),w=Math.round(u*44);
 if(w>0){g.globalAlpha=.3;R(g,23,106,w,3,'#1a1008');g.globalAlpha=1;R(g,22,99,w+2,7,INKC);R(g,23,100,w,5,BRASS);R(g,23,100,w,1,'#fff2b0');R(g,23,104,w,1,'#a8802a');
  R(g,22,96,6,13,INKC);R(g,23,97,4,11,'#8a6a2a');if(u>=1){R(g,62,96,6,13,INKC);R(g,63,97,4,11,'#8a6a2a');
   const gx=23+((t-27.0)*60)%60;if(gx<64){R(g,gx,100,3,5,'#fffbe0')}
   const p=Math.round((Math.sin(t*6)+1)*1.5);for(let k=0;k<3;k++){const ax=30+k*12,ay=112+p;px(g,ax,ay,MINT);px(g,ax+1,ay-1,MINT);px(g,ax+2,ay-2,MINT);px(g,ax+3,ay-1,MINT);px(g,ax+4,ay,MINT);R(g,ax+2,ay-1,1,5,MINT)}}}
 return{}}
function sceneLean(t){const g=wg;R(g,0,0,WW,56,NAVY);brick(g,false);
 R(g,4,64,16,3,'#6a4a30');for(let k=0;k<4;k++)R(g,5+k*4,58+(k%2),3,6,['#b8865a','#8a9aa8','#c9a24a','#a8503c'][k]);
 R(g,70,62,14,20,'#4a3220');R(g,71,63,12,18,'#bfe0f2');R(g,77,63,1,18,'#4a3220');
 woodFloor(g,'#8a6640','#946e46','#6b4a2e');
 const u=ease(seg(t,28.72,29.1));
 R(g,27,55,36,65,'#3a2420');
 // what is outside
 for(let y=58;y<104;y++)R(g,30,y,30,1,mixc('#8fc4ee','#e6f4fb',(y-58)/46));R(g,48,62,6,6,'#fff6c0');R(g,30,104,30,16,'#7fb060');R(g,30,104,30,1,'#9ccf7c');for(let k=0;k<6;k++)R(g,43-k,108+k*2,4+k*2,2,'#d8d2c6');
 R(g,32,96,5,8,'#5a3a24');R(g,29,88,11,9,'#4f7a3c');R(g,31,86,7,3,'#6a9a52');
 const w=Math.round(30*(1-u*.82));
 if(w>=28)bigDoor(g,30,0,{bar:true});else{R(g,30,58,w,62,'#6b4a2e');R(g,30,58,w,1,'#9a7250');R(g,30+w-1,58,1,62,'#3a2616');R(g,31,95,Math.max(1,w-2),3,BRASS)}
 const fr=t*30/2,tt=((t-T.s6c)*1.25)%1;const B=FB[3].f(tt,fr,'b');delete B.scene;
 const bump=(t>28.66&&t<28.8)?1:0;B.okOverlap=true;B.front=(gg,i)=>{R(gg,CX-7,i.hy-6,14,5,HAT);R(gg,CX-7,i.hy-6,14,1,'#423a4c');R(gg,CX-9,i.hy-1,18,1,HAT)};
 personFB(B,13,bump,LOOK.carl,'b');
 return{u}}
// ---------- today ----------
function school(g,t,u){
 for(let y=56;y<FL;y++)R(g,69,y,21,1,mixc('#8fc4ee','#e6f4fb',(y-56)/64));R(g,80,61,7,7,'#fff6c0');
 R(g,69,112,21,8,'#7fb060');R(g,69,112,21,1,'#9ccf7c');R(g,84,98,3,14,'#5a3a24');R(g,79,88,12,11,'#4f7a3c');R(g,81,85,8,4,'#6a9a52');
 R(g,69,FL,21,40,'#d8d2c6');R(g,69,FL,21,1,'#b8b0a1');for(let y=FL+6;y<WH;y+=7)R(g,69,y,21,1,'#c4bcad');
 R(g,0,0,WW,56,NAVY);
 R(g,0,56,64,42,'#e9ecf0');R(g,0,96,64,3,'#3f8fb0');R(g,0,99,64,21,'#d5dae2');
 for(let k=0;k<6;k++){const x=2+k*7,c=k%2?'#e0b24a':'#5c8a7a';R(g,x,70,6,46,c);R(g,x,70,6,1,shade(c,1.25));R(g,x+5,70,1,46,shade(c,.75));for(let j=0;j<3;j++)R(g,x+1,73+j*2,4,1,shade(c,.75));R(g,x+4,92,1,3,'#2a2a34')}
 R(g,2,116,42,4,'#8a8f9a');
 R(g,4,58,34,9,'#c43c3c');R(g,4,58,34,1,'#e06a5a');ptext(g,'GO BEARS',6,60,'#fff6e0');
 R(g,44,57,19,10,'#14401f');R(g,45,58,17,8,'#2fa85a');ptext(g,'EXIT',46,60,'#f0fff4');
 R(g,46,74,14,14,'#f4ecd8');R(g,46,74,14,1,'#fffaf0');R(g,48,77,10,6,'#6a9ac4');R(g,48,84,8,1,'#a9a090');
 for(let y=FL;y<WH;y++)R(g,0,y,69,1,((y-FL)%7==0)?'#b99a5e':'#d6b878');R(g,0,FL,69,1,'#a8884e');for(let k=0;k<6;k++)for(let x=(k*9)%19;x<69;x+=19)R(g,x,FL+1+k*7,1,6,'#b99a5e');
 R(g,0,FL+18,69,2,'#c43c3c');
 pdoor(g,64,u,{bar:true,wall:'#b9c0cc',wallL:'#d5dae2',leaf:'#3f6f9a',leafL:'#5f8fba',trim:'#6a7280'});
}
function sceneSchool(t){const g=wg,t0=T.s7,sp=21;
 const u=ease(seg(t,31.2,31.55));school(g,t,u);
 const reach=22,tr=t0+(reach+10)/sp; // Kit reaches the door
 let ox,P;
 if(t<tr){ox=-10+sp*(t-t0);P=walkP(ox+10)}
 else if(t<31.6){ox=reach;P={legs:stand2,arms:[{ua:10,fa:20},{ua:8,fa:16}],armIK:[[62-ox+(t>31.2?2:0),BARY-OY+1],null],lean:t>31.2?9:5,face:'n',mouth:'smile',dy:0}}
 else{ox=reach+sp*(t-31.6);P=walkP(ox+10,{face:'happy'})}
 const kids=[['k1',-36],['k2',-56],['k3',-76],['k4',-96],['k2',-116],['k1',-136]];
 for(let i=kids.length-1;i>=0;i--){const[l,off]=kids[i];const f=off+sp*(t-t0),q=reach-20-i*17+sp*Math.max(0,t-31.6);const kx=Math.min(f,q);
  if(kx<-46||kx>WW)continue;const mov=f<=q||t>=31.6;
  const KP=mov?walkP(kx*1.35+i*5):{legs:stand2,arms:[{ua:8,fa:16},{ua:-6,fa:6}],lean:3,face:'n',mouth:'smile',dy:Math.sin(t*3+i)>.5?-1:0};
  if(l=='k1')KP.pre=longHair(LOOK.girl.hair);person(KP,kx,0,Object.assign({},LOOK[l],{id:l+i}))}
 if(ox<WW)kitp(P,ox,0);
 return{u}}
function sceneCount(t){const g=wg;R(g,0,0,WW,56,NAVY);
 // top-down plan of a small theatre; the exit is in the top wall and its doors swing out
 R(g,0,56,WW,104,'#7fb060');for(let k=0;k<20;k++)px(g,(k*29)%WW,57+(k*7)%12,'#6a9a52');R(g,36,56,18,14,'#d8d2c6');
 R(g,6,70,78,84,INKC);R(g,9,73,72,78,'#e9e3d4');
 R(g,22,138,46,10,'#8a6640');R(g,22,138,46,1,'#a88a66');ptext(g,'STAGE',35,141,'#4a3220');
 for(let r=0;r<6;r++)for(let c=0;c<12;c++){if(c==5||c==6)continue;R(g,13+c*5.4,90+r*7,4,4,'#a8503c');R(g,13+c*5.4,93+r*7,4,1,'#7a3a2c')}
 const u=ease(seg(t,T.s7b+.15,T.s7b+.6));
 R(g,37,70,16,3,'#e9e3d4');
 const a=u*90;line(g,37,70,37-Math.sin(rad(a))*0+Math.cos(rad(a))*7,70-Math.sin(rad(a))*7,2,'#3f6f9a');line(g,53,70,53-Math.cos(rad(a))*7,70-Math.sin(rad(a))*7,2,'#3f6f9a');
 // people leave: seat -> aisle -> door -> outside
 const cols=[MINT,AMBER,'#ff9d8a','#9fc3ff'];let outN=0;
 for(let k=0;k<54;k++){const r=k%6,c=(k/6|0);const cc=c>=5?c+2:c;if(cc>11)continue;const sx=15+cc*5.4,sy=92+r*7;
  const start=T.s7b+.22+((5-r)*.1)+Math.abs(cc-5.5)*.045+(k%3)*.03;const v=cl01((t-start)/.85);
  let x,y;const ax=cc<6?43:47;
  if(v<=0){x=sx;y=sy}else if(v<.3){x=lerp(sx,ax,v/.3);y=sy-3}else if(v<.8){x=ax;y=lerp(sy-3,74,(v-.3)/.5)}else{x=lerp(ax,ax+(cc<6?-8:8)*((k%4)+1)/3,(v-.8)/.2);y=lerp(74,60+(k%3)*2,(v-.8)/.2);}
  if(v>=.8)outN++;R(g,x-1,y-1,3,3,INKC);px(g,x,y,cols[k%4]);px(g,x,y-1,cols[k%4]);px(g,x-1,y,cols[k%4]);px(g,x+1,y,cols[k%4]);px(g,x,y+1,cols[k%4])}
 return{outN}}
function sceneWin(t){const g=wg;
 for(let y=0;y<FL;y++)R(g,0,y,WW,1,mixc('#6fb0ea','#e6f4fb',y/FL));R(g,0,0,WW,56,NAVY);
 R(g,66,62,9,9,'#fff6c0');cloud(g,8,66,16);cloud(g,50,74,14);
 for(let x=0;x<WW;x++){const h=8+Math.round(4*Math.sin(x*.09)+2*Math.sin(x*.23));R(g,x,FL-14-h,1,h+14,'#8fc07c')}
 tree(g,10,FL,18,t,1);tree(g,76,FL,15,t,4);
 R(g,0,FL,WW,40,'#7fb060');R(g,0,FL,WW,1,'#9ccf7c');for(let k=0;k<30;k++)px(g,(k*31)%WW,FL+3+(k*7)%36,'#6a9a52');
 for(let k=0;k<7;k++)R(g,38-k*2,FL+k*6,14+k*4,6,k%2?'#d8d2c6':'#cfc8ba');
 const ph=((t-T.s8)*1.6)%1,air=Math.round(Math.sin(ph*PI)*7);
 const lift=Math.round(Math.sin(ph*PI)*3);
 personFB({hip:GY-17-air,feet:[[-3,air],[3,air]],sl:1,sa:[1,1],hands:[[CX-14,SHY-air-6-lift],[CX+13,SHY-air-6-lift]],mouth:'open',nobag:false},13,0,null,'f');
 for(let k=0;k<26;k++){const y=56+((t*22+k*29)%104),x=(k*37+Math.round(Math.sin(t*2+k)*3))%WW;R(g,x,y,2,1,[MINT,AMBER,CORAL,'#9fc3ff'][k%4])}
 return{}}

// ---------- overlays ----------
const HEADS=[
 [0.05,T.s2,"MISSION 01",["OPEN THE","LOCKED DOOR"]],
 [7.42,T.s3b,"MEET",["CARL PRINZLER"]],
 [9.9,12.78,"CHICAGO · DEC 30, 1903",["A TICKET TO","THE IROQUOIS"]],
 [12.8,T.s4,"BUT",["HE CHANGED","HIS PLANS."]],
 [14.45,T.s4b,"THAT AFTERNOON",["FIRE."]],
 [16.18,17.14,"THE EXITS",["LOCKED."]],
 [17.16,T.s5,"THE EXITS WERE LOCKED",["ABOUT 600","DIED."]],
 [19.3,T.s5b,"CARL",["COULDN'T","LET IT GO."]],
 [20.58,T.s6,"THE PUZZLE",["LET THEM OUT.","KEEP IT LOCKED."]],
 [23.65,25.07,"5 YEARS LATER",["1908"]],
 [25.09,T.s6b,"WITH HIS NEIGHBOR",["HE HAD IT."]],
 [26.42,T.s6c,"THE ANSWER",["ONE BAR."]],
 [28.12,T.s7,"NO HANDS",["LEAN ON IT."]],
 [29.9,T.s7b,"RULE UNLOCKED",["PANIC BAR"],{tc:MINT}],
 [T.s7b+.03,T.s8,"THEATERS + SCHOOLS",["50+ PEOPLE"]],
 [36.4,T.end,"MISSION 01",["COMPLETE"],{tc:MINT}]];
function tiles(t){ // mission tracker: five tiles, the collectible
 const done=t>=T.s8,pr=cl01(t/T.s8),y=566,s=84,gap=22,x0=540-(5*s+4*gap)/2;
 for(let i=0;i<5;i++){const x=x0+i*(s+gap);og.globalAlpha=1;
  og.fillStyle=i==0&&done?'#173a2c':'#1b1838';rrect(og,x,y,s,s,12);og.fill();
  if(i==0&&!done){og.save();rrect(og,x,y,s,s,12);og.clip();og.fillStyle='#2a4a7a';og.fillRect(x,y+s*(1-pr),s,s*pr);og.restore()}
  const nxt=i==1&&t>37.41;og.lineWidth=4;og.strokeStyle=i==0?(done?MINT:CORAL):(nxt&&Math.sin(t*10)>0?AMBER:'#3a3668');rrect(og,x,y,s,s,12);og.stroke();
  if(i==0&&done){og.strokeStyle=MINT;og.lineWidth=9;og.lineCap='round';og.beginPath();og.moveTo(x+22,y+44);og.lineTo(x+37,y+59);og.lineTo(x+63,y+27);og.stroke()}
  else mdraw(i==0?"01":"?",x+s/2,y+s/2+2,i==0?34:38,i==0?CREAM:(nxt?AMBER:'#5a568a'),'center',false,'',0,1)}
}
function xmark(x,y,a){og.globalAlpha=a;og.strokeStyle=CORAL;og.lineWidth=10;og.lineCap='round';og.beginPath();og.moveTo(x-18,y-18);og.lineTo(x+18,y+18);og.moveTo(x+18,y-18);og.lineTo(x-18,y+18);og.stroke();og.globalAlpha=1}

function frameAt(t){
 QA.chars=[];QA.solids=[];QA.shot='';
 og.imageSmoothingEnabled=false;og.clearRect(0,0,1080,1920);
 let sh=0,z=1,inf={};
 if(t<T.s3){inf=sceneMission(t);QA.shot=t<3.95?'back':'front'}
 else if(t<T.s3b){sceneCarl(t);QA.shot='closeup'}
 else if(t<T.s4){inf=sceneStreet(t);QA.shot='side'}
 else if(t<T.s4b){sceneFire(t);QA.shot='elevation'}
 else if(t<T.s5){sceneLocked(t);QA.shot='detail'}
 else if(t<T.s5b){sceneThink(t);QA.shot='closeup'}
 else if(t<T.s6){scenePlan(t);QA.shot='plan'}
 else if(t<T.s6b){sceneTwo(t);QA.shot='side'}
 else if(t<T.s6c){sceneBar(t);QA.shot='detail'}
 else if(t<T.s7){inf=sceneLean(t);QA.shot='back';z=lerp(1,1.16,ease(seg(t,T.s6c,T.s7)));sh=shake(t,28.7)}
 else if(t<T.s7b){inf=sceneSchool(t);QA.shot='side'}
 else if(t<T.s8){inf=sceneCount(t);QA.shot='plan'}
 else{sceneWin(t);QA.shot='front'}
 if(z>1){const sw=WW/z,shh=104/z;og.fillStyle=NAVY;og.fillRect(0,0,1080,672);og.save();og.beginPath();og.rect(0,672,1080,1248);og.clip();og.drawImage(wc,(WW-sw)/2,56+(104-shh)*.55,sw,shh,sh,672,1080,1248);og.restore()}
 else og.drawImage(wc,0,0,WW,WH,sh,0,1080,1920);
 // ---- lighting pass ----
 lit(()=>{
  if(t<T.s3){glow(45*12,68*12,260,RED,.22+.12*Math.sin(t*5));glow(540,1500,700,COOL,.12);
   if(t>=T.s2){const a=ease(seg(t,4.9,5.9));grade('#c8a070',.35*a,'multiply')}}
  else if(t<T.s3b){glow(260,780,620,WARM,.30);glow(77*12,104*12,170,WARM,.35)}
  else if(t<T.s4){const cam=inf.cam||0;for(const lx of[36,128,206])glow((lx-cam)*12,72*12,230,WARM,.34);grade('#b8c4e8',.22,'multiply')}
  else if(t<T.s4b){const f=.6+.4*Math.sin(t*9)*Math.sin(t*5.3);glow(45*12,70*12,520,FIRE,.30+.14*f);grade('#6a5a8a',.38,'multiply')}
  else if(t<T.s5){const f=.6+.4*Math.sin(t*9)*Math.sin(t*5.3);glow(540,56*12,560,FIRE,.34+.16*f);glow(540,153*12,420,FIRE,.22+.1*f);grade('#3a3050',.30,'multiply')}
  else if(t<T.s5b){glow(900,900,640,WARM,.26);grade('#4a4470',.34,'multiply')}
  else if(t<T.s6){glow(1000,760,520,WARM,.30);grade('#c8a880',.20,'multiply')}
  else if(t<T.s6b){shaft(7,26,63,24,70,160,'#fff4c8',.13);glow(16*12,75*12,330,SUN,.3)}
  else if(t<T.s6c){glow(540,76*12,460,SUN,.28)}
  else if(t<T.s7){const u=inf.u||0;if(u>0){glow(540,1560,620,SUN,.22*u);shaft(34,58,118,14,76,160,'#fff4c8',.2*u)}}
  else if(t<T.s7b){glow(53*12,62*12,170,GREEN,.4);const u=inf.u||0;if(u>0){glow(76*12,90*12,520,SUN,.2*u);shaft(69,88,62,40,90,160,'#fff4c8',.14*u)}}
  else if(t<T.s8){glow(540,60*12,380,SUN,.25)}
  else{glow(70*12,66*12,520,SUN,.45)}
 });
 const v=og.createLinearGradient(0,0,0,1920);v.addColorStop(0,'rgba(0,0,0,.22)');v.addColorStop(.3,'rgba(0,0,0,0)');v.addColorStop(.8,'rgba(0,0,0,0)');v.addColorStop(1,'rgba(0,0,0,.35)');og.fillStyle=v;og.fillRect(0,0,1080,1920);
 // ---- header band + mission tracker ----
 og.globalAlpha=.6;og.fillStyle='#0f0d22';og.fillRect(0,110,1080,562);og.globalAlpha=1;
 let h=HEADS.find(h=>t>=h[0]&&t<h[1]);
 if(t>=T.s2&&t<T.s3){const yr=Math.round(lerp(2026,1903,ease(seg(t,4.9,5.85))));header("REWIND TO",[String(yr)],1,{tc:t>5.85?AMBER:CREAM})}
 else if(h)header(h[2],h[3],(t-h[0])/.2,h[4]);
 tiles(t);
 // ---- scene-specific overlays ----
 if(t<T.s2){[["NO KEY",2.3],["NO KNOB",3.2],["NO HANDS",3.9]].forEach(([s,t0],i)=>{if(t<t0)return;const a=ease(seg(t,t0,t0+.15)),y=770+i*96,pop=1+.3*(1-a);
   og.globalAlpha=.9*a;og.fillStyle='#0f0d22';rrect(og,24,y-40,330,80,16);og.fill();og.globalAlpha=1;og.save();og.translate(66,y);og.scale(pop,pop);xmark(0,0,a);og.restore();mdraw(s,104,y+2,34,CREAM,'left',false,'',0,a)})}
 if(t>=22.6&&t<T.s6){const a=ease(seg(t,22.6,22.85)),pp=1+.08*Math.sin(t*7);og.save();og.translate(44*12,93*12);og.scale(pp,pp);mdraw("?",0,0,150,CORAL,"center",true,"#efe6d0",16,a);og.restore()}
 if(t>=6.03&&t<T.s3)stamp("IMPOSSIBLE",'#e0473c',540,800,6.03,t,-.08,74);
 if(t>=26.42&&t<T.s6c&&t>27.0){const a=ease(seg(t,27.0,27.2));tag("PUSH",540,1470,MINT,a)}
 if(t>=T.s7b&&t<T.s8){const n=Math.min(50,inf.outN||0);mdraw(n>=50?"50+":String(n),170,740,64,AMBER,'center',true,INKC,12,1);mdraw("OUT",170,800,28,CREAM,'center',true,INKC,8,1)}
 if(t>=T.s8){const xp=Math.round(100*ease(seg(t,36.5,37.2)));mdraw("+"+xp+" XP",540,800,70,AMBER,'center',true,INKC,14,1);
  if(t>37.41)tag("FOLLOW FOR MISSION 02",540,1400,MINT,ease(seg(t,37.41,37.6)))}
 subtitle(t,false);
 for(const c of [T.s3,T.s3b,T.s4,T.s4b,T.s5,T.s5b,T.s6,T.s6b,T.s6c,T.s7,T.s7b,T.s8])wipe(t,c,.12);
}
window.frame=i=>frameAt(i/30);
Promise.all([document.fonts.load('700 40px Silk'),document.fonts.load('400 40px PS2P')]).then(()=>{window.READY=true});
