const T6={s2:3.97,s3:7.79,s4:14.92,s5:19.6,s6:23.98,s7:30.06,s8:35.47,s9:40.53,end:43.04};
LOOK.ed={skin:'#efc9a6',skinD:'#d0a684',hair:'#3a2a20',top:'#4a7ab8',topL:'#6e9bd4',pants:'#3a3550',shoe:'#2c2a3a'};
LOOK.dean={skin:'#e9c3a3',skinD:'#c99d7e',hair:'#9a9aa6',top:'#4a4a5a',topL:'#5e5e70',pants:'#3a3a48',shoe:'#1e1c24'};
LOOK.att={skin:'#c98b69',skinD:'#a86f52',hair:'#2a1f28',top:'#b8865a',topL:'#d4a676',pants:'#4b5f7a',shoe:'#d8d0c0'};

// ---------- S1 : the verdict (0-3.97) ----------
function office(g,t,dir){
 t=t||0;
 R(g,0,0,WW,56,NAVY);
 // wall: institutional green, with a dado rail
 R(g,0,56,WW,42,dir?'#8f9a8a':'#9aa58f');R(g,0,56,WW,1,dir?'#a7b0a2':'#b0baa5');R(g,0,86,WW,2,'#6a6a5a');R(g,0,88,WW,32,dir?'#5e5a4e':'#6a6658');
 for(let x=4;x<WW;x+=11)R(g,x,89,1,30,dir?'#544f45':'#5e5a4e');
 // window with venetian blind, late-afternoon light
 R(g,56,58,28,30,'#4a4a4a');R(g,57,59,26,28,'#e9d9a6');for(let y=60;y<87;y+=2)R(g,57,y,26,1,'#cfc08a');R(g,69,59,1,28,'#4a4a4a');
 glowRect(g,50,88,40,32,'#ffe6a0',.10);
 // wall clock
 R(g,40,62,9,9,'#3a3a44');R(g,41,63,7,7,'#f4ecd8');px(g,44,66,'#1a162e');const ca=t*.6;px(g,44+Math.round(Math.sin(ca)*2),66-Math.round(Math.cos(ca)*2),'#1a162e');R(g,44,64,1,2,'#1a162e');
 // framed state seal
 R(g,10,60,12,12,'#5a4a3a');R(g,11,61,10,10,'#e9d9a6');R(g,13,63,6,6,'#b89a5a');px(g,15,65,'#8a6a3a');
 // filing cabinets against the left wall
 for(let k=0;k<(dir?0:2);k++){const x=2+k*11;R(g,x,88,10,32,'#6e7a7a');R(g,x,88,10,1,'#8a9696');for(let d=0;d<4;d++){R(g,x+1,90+d*8,8,6,'#7c8888');R(g,x+4,92+d*8,2,1,'#2a2a34')}}
 // floor: linoleum tiles
 R(g,0,FL,WW,40,'#9a8e78');R(g,0,FL,WW,1,'#7a6e58');
 for(let y=FL+1;y<WH;y+=6)for(let x=((y/6|0)%2)*6;x<WW;x+=12)R(g,x,y,6,6,'#8f8370');
 // the desk, front and center
 if(!dir){R(g,24,96,44,3,'#6b4e36');R(g,24,96,44,1,'#8a6a4a');R(g,24,99,44,20,'#5a3e28');R(g,26,101,18,16,'#6b4e36');R(g,46,101,20,16,'#6b4e36');for(let d=0;d<3;d++)R(g,48,103+d*5,16,1,'#4a3220');
 glowRect(g,22,FL,48,6,'#2a1a10',.3);
 // typewriter and a lamp on the desk
 R(g,52,89,12,7,'#3a3a44');R(g,53,90,10,2,'#4a4a56');for(let k=0;k<4;k++)px(g,54+k*2,93,'#d8d8e0');R(g,52,87,12,2,'#f4ecd8');
 R(g,28,88,1,8,'#3a3a44');R(g,25,86,7,3,'#2f5f3a');glowRect(g,22,89,14,8,'#ffe6a0',.18);}
 if(dir){ // door with a frosted glass panel and the nameplate on the left wall; flag beside it
  R(g,2,60,18,60,'#6b4e36');R(g,4,62,14,58,'#8a6a4a');R(g,5,64,12,22,'#cfe0e8');R(g,5,64,12,1,'#e8f0f4');R(g,16,96,2,3,AMBER);
  R(g,5,88,12,6,'#e9d9a6');R(g,5,88,12,1,'#fff2c8');
  R(g,24,70,1,50,'#8a8a96');R(g,25,70,6,4,'#c43c3c');R(g,25,71,6,1,'#f4ecd8');R(g,25,73,6,1,'#f4ecd8');R(g,25,70,3,2,'#3a4f8a');R(g,25,74,6,3,'#c43c3c');}
}
function sceneV(t){
 const g=wg;R(g,0,0,WW,56,NAVY);
 // looking down at a desk: wood grain
 for(let y=56;y<WH;y++)R(g,0,y,WW,1,(y%7==0)?'#5a3e28':(((y/7|0)%2)?'#6b4e36':'#70523a'));
 for(let k=0;k<12;k++)R(g,(k*23)%WW,60+k*8,9,1,'#5a3e28');
 glowRect(g,0,56,WW,104,'#ffe6a0',.06);
 // manila folder, slightly rotated feel via a stepped left edge, with a tab
 const fx=12,fy=72,fw=66,fh=72;
 glowRect(g,fx+3,fy+3,fw,fh,'#1a1008',.35);
 R(g,fx,fy,fw,fh,'#d9b878');R(g,fx,fy,fw,1,'#ecd092');R(g,fx+fw-1,fy,1,fh,'#b89858');R(g,fx,fy+fh-1,fw,1,'#b89858');
 R(g,fx+fw-22,fy-5,20,5,'#d9b878');R(g,fx+fw-22,fy-5,20,1,'#ecd092');for(let k=0;k<4;k++)R(g,fx+fw-19+k*4,fy-3,3,1,'#7a5a2a'); // tab with a name
 // typed form inside: header block, ruled lines, a photo corner, a paper clip
 R(g,fx+6,fy+8,fw-12,fh-16,'#f4ecd8');R(g,fx+6,fy+8,fw-12,1,'#fffaf0');
 R(g,fx+36,fy+12,18,20,'#9aa4b0');R(g,fx+37,fy+13,16,18,'#cfd6dc');R(g,fx+42,fy+16,6,7,LOOK.ed.skin);R(g,fx+42,fy+15,6,2,LOOK.ed.hair); // photo
 for(let k=0;k<7;k++)R(g,fx+10,fy+20+k*4,k%3==2?14:22,1,'#a9a090');
 for(let k=0;k<5;k++)R(g,fx+10,fy+40+k*4,(k*17%30)+18,1,'#a9a090');
 R(g,fx+8,fy+6,3,9,'#8a8a96');R(g,fx+9,fy+7,1,7,'#d8d8e0'); // paper clip
 // a fountain pen laid across the corner
 line(g,fx+40,fy+fh-6,fx+64,fy+fh-18,2,'#1a162e');R(g,fx+62,fy+fh-19,3,2,AMBER);
 return{}}
// ---------- S2 : iron lung (3.97-7.79) ----------
// A 1953 bedroom at night. Ed sleeps in an Emerson-type tank respirator:
// long steel cylinder on a wheeled frame, head out of the collar on a padded
// headrest, a mirror angled above so he can see the room, portholes along the
// side, bellows at the foot end that pump the air, and a gauge on top.
function glowRect(g,x,y,w,h,col,a){g.globalAlpha=a;R(g,x,y,w,h,col);g.globalAlpha=1}
function bedroom(g,t){
 // header band
 R(g,0,0,WW,56,NAVY);
 // wallpaper: warm, faint stripe, slightly darker toward the left corner
 for(let x=0;x<WW;x++){const d=1-Math.max(0,(28-x))/90;R(g,x,56,1,42,shade('#c9b58d',d));if(x%6==0)R(g,x,56,1,42,shade('#bfa982',d))}
 R(g,0,56,WW,2,'#a8936c'); // picture rail
 // small wallpaper motif
 for(let y=62;y<96;y+=10)for(let x=3;x<WW;x+=12){px(g,x,y,'#b9a378');px(g,x+1,y+1,'#b9a378');px(g,x-1,y+1,'#b9a378')}
 // wainscot
 R(g,0,98,WW,22,'#7a5a3c');R(g,0,98,WW,1,'#9a7a54');for(let x=2;x<WW;x+=9)R(g,x,100,1,17,'#6a4c30');R(g,0,117,WW,3,'#5a4028');
 // window with curtains, night outside
 R(g,58,60,24,32,'#5a4028');R(g,60,62,20,28,'#101a3a');R(g,60,62,20,8,'#162452');
 R(g,69,62,2,28,'#5a4028');R(g,60,75,20,2,'#5a4028');
 R(g,74,66,4,4,'#f2f0d8');px(g,73,67,'#f2f0d8');px(g,75,65,'#f2f0d8'); // moon
 for(const[sx,sy]of[[62,65],[66,70],[77,80],[63,84],[72,86]])px(g,sx,sy,'#cfd6ff');
 // curtains, a 1 px sway
 const sw=Math.round(Math.sin(t*1.3));R(g,55+sw,58,5,36,'#8a3f3a');R(g,56+sw,58,1,36,'#a85450');R(g,80-sw,58,5,36,'#8a3f3a');R(g,83-sw,58,1,36,'#a85450');
 R(g,54,57,32,2,'#5a4028');
 // moonlight falling onto the floor through the window
 glowRect(g,52,120,34,40,'#b9c4e8',.10);glowRect(g,56,120,26,40,'#b9c4e8',.08);
 // floor planks
 R(g,0,FL,WW,1,'#5a4028');
 for(let y=FL+1;y<WH;y++){const band=Math.floor((y-FL-1)/6);R(g,0,y,WW,1,(y-FL-1)%6==0?'#6b4a2e':(band%2?'#8a6640':'#946e46'))}
 for(let b=0;b<7;b++){const y=FL+1+b*6;for(let x=((b*11)%17);x<WW;x+=17)R(g,x,y,1,6,'#6b4a2e')}
 // baseball pennant on the wall
 R(g,6,62,2,14,'#5a4028');for(let k=0;k<14;k++)R(g,8,62+k,Math.max(1,10-Math.abs(k-7)*1.4|0)+0,1,'#2f5fa0');R(g,8,62,3,1,'#f4ecd8');
 // bedside table with lamp, radio and schoolbooks
 R(g,2,96,16,2,'#8a6a4a');R(g,3,98,2,22,'#6a4a30');R(g,15,98,2,22,'#6a4a30');R(g,2,96,16,1,'#a88a66');
 R(g,10,82,7,5,'#4a3a30');R(g,11,83,5,3,'#e8c87a');px(g,13,84,'#c43c3c');R(g,10,87,7,9,'#4a3a30'); // radio
 for(let k=0;k<3;k++)R(g,3,93-k*1,6,1,['#c45a5a','#5c8a7a','#e0b24a'][k]); // books
 // lamp
 R(g,5,76,1,17,'#3a3a44');R(g,2,72,7,5,'#e8d8a8');R(g,2,72,7,1,'#f6ecc8');
 const fl=.9+.1*Math.sin(t*7.3)*Math.sin(t*3.1);glowRect(g,0,70,22,30,'#ffd890',.14*fl);glowRect(g,0,76,14,20,'#ffd890',.12*fl);
}
function tank(g,x,y,t){
 // x,y: left-top of the cylinder body. Body 48 wide, 16 tall. Head end at left.
 const L=48,H=16;
 // undercarriage first: frame rails, casters, bellows
 R(g,x+4,y+H,L-8,2,'#4a4a56');R(g,x+8,y+H+2,2,12,'#5a5a66');R(g,x+L-10,y+H+2,2,12,'#5a5a66');
 R(g,x+6,y+H+12,6,2,'#3a3a44');R(g,x+L-12,y+H+12,6,2,'#3a3a44');
 for(const cx of [x+7,x+11,x+L-11,x+L-7]){R(g,cx,y+H+14,3,3,'#2a2a34');px(g,cx+1,y+H+15,'#8a8a96')} // casters
 // bellows at the foot end, pumping. 2.6 s cycle.
 const br=(Math.sin(t*PI2/2.6)+1)/2,bh=4+Math.round(br*5);
 const bx=x+L-26,by=y+H+3;
 R(g,bx,by,14,bh,'#6a4a3a');for(let k=1;k<bh;k+=2)R(g,bx,by+k,14,1,'#8a6a56');R(g,bx-1,by+bh,16,2,'#4a4a56');R(g,bx-1,by-1,16,1,'#4a4a56');
 // motor box
 R(g,bx+16,by+2,8,8,'#4a4a56');R(g,bx+17,by+3,6,6,'#5e5e6c');px(g,bx+18,by+4,'#c43c3c');
 // cylinder body with shading bands to read as a tube
 for(let i=0;i<L;i++){const end=Math.min(i,L-1-i),r=end<2?2:end<4?1:0;
  R(g,x+i,y+r,1,H-2*r,'#aeb0b6');R(g,x+i,y+r,1,2,'#d8dadf');R(g,x+i,y+r+2,1,2,'#c6c8ce');R(g,x+i,y+H-r-3,1,3,'#7e8088');R(g,x+i,y+H-r-1,1,1,'#5e6068')}
 // seams and rivets
 for(const sx of [x+12,x+30]){R(g,sx,y+1,1,H-2,'#8a8c94');for(let k=2;k<H-2;k+=4)px(g,sx,y+k,'#e2e4e8')}
 // portholes
 for(const px0 of [x+18,x+26,x+36]){R(g,px0,y+5,6,6,'#5e6068');R(g,px0+1,y+6,4,4,'#3a4a66');px(g,px0+2,y+7,'#8aa3c8');R(g,px0,y+5,6,1,'#8a8c94')}
 // collar at the head end: a thick flange ring
 R(g,x-2,y-2,4,H+4,'#7e8088');R(g,x-2,y-2,4,1,'#b8babf');R(g,x-1,y+3,2,H-6,'#2e2e36');
 // gauge on top
 R(g,x+38,y-6,7,6,'#4a4a56');R(g,x+39,y-5,5,4,'#f4ecd8');
 const ga=lerp(-.9,.9,br);px(g,x+41+Math.round(Math.sin(ga)*1.6),y-3-Math.round(Math.cos(ga)*1.6),'#c43c3c');px(g,x+41,y-3,'#2a2a34');
 // headrest tray and pillow outside the collar
 R(g,x-14,y+9,13,2,'#8a8c94');R(g,x-13,y+11,1,8,'#5a5a66');R(g,x-13,y+4,12,5,'#e8e0cc');R(g,x-13,y+4,12,1,'#f6f0e2');
 // mirror on an arm above the head, angled toward the room
 R(g,x-6,y-9,1,9,'#5a5a66');R(g,x-12,y-12,10,5,'#5a5a66');R(g,x-11,y-11,8,3,'#cfe0f0');px(g,x-10,y-10,'#ffffff');
 // power cord to the wall
 line(g,x+L-6,y+H+10,x+L+8,y+H+22,1,'#2a2a34');R(g,x+L+8,y+H+20,3,3,'#4a3a30');
}
function sceneLung(t){
 const g=wg;bedroom(g,t);
 const x=30,y=90;
 // shadow under the tank
 glowRect(g,x-10,FL,L_(62),8,'#2a1a10',.35);
 tank(g,x,y,t);
 // Ed lies on his back: top of the head toward the room (left), face toward the ceiling, chin at the collar.
 const sk=LOOK.ed.skin,hr=LOOK.ed.hair;
 const bob=Math.round((Math.sin(t*PI2/2.6)+1)/2*.6);
 const hx=x-13,hy=y+1-bob; // 10 wide, 7 tall, lying on the pillow
 R(g,hx,hy,10,7,sk);R(g,hx-1,hy-1,4,9,hr);R(g,hx+2,hy-1,6,1,hr); // hair: back of the head and a fringe
 px(g,hx+8,hy-1,sk);px(g,hx+9,hy,sk); // nose, pointing up
 const blink=(t%3.1)<.14;
 if(blink)R(g,hx+5,hy+1,2,1,'#1a162e');else R(g,hx+5,hy+1,2,1,'#1a162e'),px(g,hx+6,hy,'#1a162e'); // eye looking up at the mirror
 R(g,hx+9,hy+2,1,2,'#8a4a40'); // mouth on the chin side
 px(g,hx+3,hy+4,'#e0a08a'); // ear
 // reflection of his face in the mirror
 R(g,x-10,y-10,3,1,sk);px(g,x-8,y-10,hr);
 // dust motes in the moonlight
 for(let k=0;k<5;k++){const mx=60+((k*7+Math.floor(t*2))%22),my=100+((k*13+Math.floor(t*3))%50);g.globalAlpha=.5;px(g,mx,my,'#dfe6ff');g.globalAlpha=1}
 return{}}
const L_=v=>v;
// ---------- S3 : Berkeley, the dean (7.79-14.92) ----------
function cloud(g,x,y,w){R(g,x,y,w,3,'#f6fbff');R(g,x+3,y-2,w-6,2,'#f6fbff');R(g,x+2,y+3,w-4,1,'#e4eef8')}
function tree(g,x,base,h,t,k){ // trunk + layered canopy, leaves shimmer
 R(g,x,base-h,3,h,'#5a3a24');R(g,x+1,base-h,1,h,'#7a5434');
 const w=Math.round(h*.9),cy=base-h-2;const sw=Math.round(Math.sin(t*1.1+k))*(h>14?1:0);
 R(g,x+1-w/2+sw,cy,w,Math.round(h*.45),'#4f7a3c');R(g,x+1-w/2+2+sw,cy-3,w-4,4,'#5a8a44');R(g,x+1-w/2+4+sw,cy-5,w-8,3,'#6a9a52');
 R(g,x+1-w/2+2+sw,cy+Math.round(h*.45)-2,w-4,2,'#3f6630');
 for(let i=0;i<4;i++)px(g,x+1-w/2+2+((i*5+k*3)%(w-4))+sw,cy+1+((i*3+k)%(Math.round(h*.4))),'#7fb060');
}
function campus(g,cam,t,mir){
 t=t||0;
 // sky: pale at the horizon, deeper above
 for(let y=0;y<FL;y++)R(g,0,y,WW,1,mixc('#8fb9e3','#d9ecf7',y/FL));
 R(g,0,0,WW,56,NAVY);
 cloud(g,10-Math.round(cam*.05),64,14);cloud(g,52-Math.round(cam*.05),70,18);
 // far hills
 for(let x=0;x<WW;x++){const h=6+Math.round(3*Math.sin((x+cam*.1)*.08)+2*Math.sin((x+cam*.1)*.21));R(g,x,FL-30-h,1,h+2,'#9db9c9')}
 // the Campanile, far, slow parallax
 const tx=(mir?14:62)-Math.round(cam*.15);
 R(g,tx,30,9,64,'#e9e3d4');R(g,tx,30,2,64,'#d6cfbe');R(g,tx+7,30,2,64,'#f4efe3');
 R(g,tx-1,27,11,3,'#cfc8b8');R(g,tx+2,19,5,8,'#b9c6d1');R(g,tx+3,15,3,4,'#8a9aa8');px(g,tx+4,13,'#8a9aa8');
 R(g,tx+3,36,3,5,'#3a3a4a');R(g,tx+4,37,1,3,'#d9c27a'); // clock
 for(let y=46;y<90;y+=8)R(g,tx+3,y,3,4,'#cfc8b8');
 // mid trees, medium parallax
 for(let k=0;k<4;k++){const x=((k*31+8-Math.round(cam*.45))%120+120)%120-15;tree(g,x,FL-18,12,t,k)}
 // lawn behind the path
 R(g,0,FL-20,WW,20,'#6f9a4e');R(g,0,FL-20,WW,1,'#86b060');for(let x=0;x<WW;x+=7)px(g,x+((cam|0)%7),FL-12+(x%3),'#5f8a40');
 // the hall: stone, with a columned portico and steps down to the path
 const bx=(mir?34:-4)-Math.round(cam);
 R(g,bx,52,62,68,'#e6dfcf');R(g,bx,52,62,1,'#f2ede1');R(g,bx,50,62,3,'#cfc8b8');
 // pediment
 for(let k=0;k<8;k++)R(g,bx+8+k,50-k,46-2*k,1,'#d8d1c0');R(g,bx+30,44,2,2,'#b8b0a0');
 // columns with shadow side
 for(let k=0;k<5;k++){const cx=bx+6+k*12;R(g,cx,58,5,44,'#efe9dc');R(g,cx,58,1,44,'#d6cfbe');R(g,cx+4,58,1,44,'#c4bcab');R(g,cx-1,56,7,2,'#d8d1c0');R(g,cx-1,102,7,2,'#cfc8b8')}
 // dark doorway behind the columns
 R(g,bx+25,60,16,42,'#4a3a2e');R(g,bx+26,61,14,40,'#6a4e3a');R(g,bx+32,62,2,39,'#4a3a2e');R(g,bx+36,82,1,2,'#d9c27a');R(g,bx+27,64,4,6,'#8a7a9a');R(g,bx+35,64,4,6,'#8a7a9a');
 // steps: six risers, each with a lit tread and a shaded riser
 for(let k=0;k<6;k++){const y=FL-3*(k+1);const w=52+k*3,x0=bx+5-k*1.5;R(g,x0,y,w,3,'#c9c2b4');R(g,x0,y,w,1,'#e7e1d8');R(g,x0,y+2,w,1,'#aea798')}
 // building shadow on the path
 glowRect(g,bx-2,FL,66,6,'#3a3a4a',.18);
 // path: paving, with a soft worn line
 R(g,0,FL,WW,40,'#c4bcad');R(g,0,FL,WW,1,'#a9a193');
 for(let y=FL+2;y<WH;y+=5){R(g,0,y,WW,1,'#b8b0a1');for(let x=((y*7)%9)-Math.round(cam)%9;x<WW;x+=9)R(g,x,y-4,1,4,'#b8b0a1')}
 // a few students far away on the lawn path (silhouettes with parallax)
 for(let k=0;k<3;k++){const x=((k*37+20-Math.round(cam*.5)+Math.round(t*4*(k%2?1:-1)))%130+130)%130-20;R(g,x,FL-24,2,6,['#3a5a8a','#8a3a3a','#3a6a4a'][k]);R(g,x,FL-26,2,2,'#3a2a20')}
}
function sceneDean(t){
 const cam=0;campus(wg,cam,t,true);
 const u=ease(seg(t,7.85,9.6)),ox=lerp(-34,-6,u); // rolls in from the left, stops short of the first step
 if(t>9.6){const dn=ease(seg(t,9.6,10.1));const P={legs:stand2,arms:[{ua:35,fa:118},{ua:30,fa:112}],lean:lerp(0,4,dn),face:'n',mouth:'flat',look:t>11?1:0,dy:0};
  // dean at the top of the steps, facing Ed (left), so his sprite is flipped
  person(P,38-Math.round(cam),18,LOOK.dean,(g,i)=>{R(g,i.hx-1,i.hy-2,i.hw+2,3,LOOK.dean.hair);R(g,i.hx+i.hw-6,i.hy+4,5,1,'#2a1f28')},true);}
 const P=roll(t,ox+34,u<1);if(u>=1){P.face=t>12?'o':'n';P.mouth=t>12?'flat':'smile';P.look=t>10?1:0}
 person(P,ox,0,LOOK.ed);
 return{}}
// ---------- S4 : hospital wing (14.92-19.6) ----------
function sceneWing(t){
 const g=wg;
 if(t<16.4){
  // Cowell Hospital: stucco, tile roof, a canopy over the entrance, hedges, a cross sign
  for(let y=0;y<FL;y++)R(g,0,y,WW,1,mixc('#8fb9e3','#d9ecf7',y/FL));R(g,0,0,WW,56,NAVY);
  cloud(g,8,66,16);
  for(let k=0;k<3;k++)tree(g,2+k*40,FL-2,13,t,k+3);
  R(g,10,46,74,74,'#e8d9bf');R(g,10,46,74,1,'#f4ead4');R(g,8,42,78,5,'#a8503c');R(g,8,42,78,1,'#c4664c');for(let x=9;x<86;x+=4)px(g,x,44,'#8a3c2c');
  for(let y=54;y<100;y+=14)for(let x=16;x<80;x+=12){R(g,x,y,8,9,'#4a4a5a');R(g,x+1,y+1,6,7,'#9ec0d8');R(g,x+1,y+1,6,2,'#c8dfe8');R(g,x+4,y+1,1,7,'#4a4a5a')}
  R(g,36,84,22,36,'#3a3a4a');R(g,38,86,18,34,'#6a7a8a');R(g,46,86,2,34,'#3a3a4a');R(g,40,90,5,10,'#cfe0e8');R(g,49,90,5,10,'#cfe0e8');
  R(g,32,80,30,4,'#c9c2b4');R(g,32,80,30,1,'#e7e1d8');R(g,34,84,1,10,'#9a9284');R(g,59,84,1,10,'#9a9284');
  R(g,40,62,14,14,'#f6f2ea');R(g,46,64,2,10,'#d84040');R(g,42,68,10,2,'#d84040');
  R(g,10,110,22,10,'#4f7a3c');R(g,10,110,22,1,'#6a9a52');R(g,62,110,22,10,'#4f7a3c');R(g,62,110,22,1,'#6a9a52');
  R(g,0,FL,WW,40,'#c4bcad');R(g,0,FL,WW,1,'#a9a193');for(let y=FL+2;y<WH;y+=5){R(g,0,y,WW,1,'#b8b0a1')}
  glowRect(g,10,FL,74,5,'#3a3a4a',.18);
  const u=ease(seg(t,14.95,16.3)),ox=lerp(-32,8,u);person(roll(t,ox+32,u<1),ox,0,LOOK.ed);
 }else{
  // the converted hospital room: bed with rails, his own things on the walls, the lung parked in the corner
  R(g,0,0,WW,56,NAVY);
  for(let x=0;x<WW;x++)R(g,x,56,1,42,x%8==0?'#d6e0dd':'#e4ecea');R(g,0,56,WW,1,'#c4d0cc');R(g,0,96,WW,24,'#b9c4c2');R(g,0,96,WW,1,'#cdd6d4');
  R(g,60,60,20,26,'#4a4a5a');R(g,61,61,18,24,'#9ec0d8');R(g,61,61,18,8,'#c8dfe8');R(g,69,61,2,24,'#4a4a5a');R(g,61,72,18,2,'#4a4a5a');
  // posters and a pennant: his room now
  R(g,8,60,14,18,'#e07a5a');R(g,10,62,10,6,'#f4d27a');R(g,10,70,10,6,'#2f5fa0');R(g,26,62,2,14,'#5a4028');for(let k=0;k<12;k++)R(g,28,62+k,Math.max(1,(9-Math.abs(k-6)*1.3)|0),1,'#c43c3c');
  R(g,40,64,16,10,'#4a4a5a');R(g,41,65,14,8,'#f4ecd8');for(let k=0;k<3;k++)R(g,43,67+k*2,10,1,'#a9a090'); // a framed admission letter
  // bookshelf, record player
  R(g,4,84,20,2,'#8a6a4a');for(let k=0;k<7;k++)R(g,5+k*3,76+(k%2),2,8,['#c45a5a','#5c8a7a','#e0b24a','#6a6aa0'][k%4]);R(g,4,86,1,34,'#6a4a30');R(g,23,86,1,34,'#6a4a30');
  // hospital bed with rails
  R(g,50,90,38,4,'#f4ecd8');R(g,50,94,38,3,'#9aa4b0');R(g,50,97,2,23,'#9aa4b0');R(g,86,97,2,23,'#9aa4b0');R(g,52,84,8,6,'#f4ecd8');
  R(g,48,78,2,16,'#9aa4b0');R(g,48,78,14,1,'#9aa4b0');R(g,48,82,14,1,'#9aa4b0');R(g,48,86,14,1,'#9aa4b0');
  R(g,60,88,28,2,'#6a8ac4');
  floorStripes(g,'#9aa7a5','#a9b5b3');
  glowRect(g,48,FL,42,4,'#2a2a3a',.25);
  const P=roll(t,0,false);if(P.face!='closed')P.face='happy';person(P,14,0,LOOK.ed);
 }
 return{}}
// ---------- S5 : the Rolling Quads (19.6-23.98) ----------
function sceneQuads(t){
 const cam=lerp(0,40,seg(t,19.6,24));campus(wg,cam+30,t);
 const crew=[{l:'ed',x:0},{l:'a1',x:-23},{l:'a2',x:-46},{l:'a4',x:-69}];
 const prog=ease(seg(t,19.6,23.8))*92;
 crew.forEach((c,k)=>{const x=-10+c.x+prog;if(x<-44||x>WW)return;person(roll(t+k*.17,x+40,true),x,0,LOOK[c.l])});
 return{}}

// ---------- S6 : the curb (23.98-30.06) ----------
const CURB=8; // 8 px = 12 in
function telegraph(g,t,edge){
 for(let y=0;y<FL;y++)R(g,0,y,WW,1,mixc('#8fb9e3','#d9ecf7',y/FL));R(g,0,0,WW,56,NAVY);
 cloud(g,60,64,16);
 // shopfronts: bookstore and a cafe, with awnings and signs
 R(g,0,46,edge+10,74,'#d9cdb8');R(g,0,46,edge+10,1,'#e7dfcf');
 R(g,2,50,26,8,'#2f5fa0');R(g,2,50,26,1,'#4a7ac8');for(let k=0;k<5;k++)R(g,5+k*4,53,3,2,'#f4ecd8'); // BOOKS sign
 R(g,0,58,30,4,'#c43c3c');for(let k=0;k<6;k++)R(g,k*5,58,3,4,'#e8e0cc');R(g,0,62,30,1,'#8a3c2c'); // striped awning
 R(g,4,66,22,30,'#3a3a4a');R(g,5,67,20,28,'#6a7a8a');for(let k=0;k<4;k++)R(g,7+k*5,70,3,6,['#c45a5a','#5c8a7a','#e0b24a','#6a6aa0'][k]);R(g,5,80,20,1,'#4a4a5a'); // window with books
 R(g,34,50,20,8,'#2f6a3a');R(g,34,50,20,1,'#4a8a52');for(let k=0;k<4;k++)R(g,37+k*4,53,3,2,'#f4ecd8'); // CAFE sign
 R(g,32,58,24,4,'#2f6a3a');R(g,32,62,24,1,'#1f4a2a');
 R(g,34,66,8,30,'#3a3a4a');R(g,35,67,6,28,'#6a7a8a');R(g,44,66,10,30,'#5a4028');R(g,45,68,8,28,'#7a5434');R(g,51,82,1,2,AMBER); // cafe window and door
 for(let y=96;y<FL-CURB;y++)R(g,0,y,edge+10,1,'#b9ad98');
 // lamp post
 R(g,edge-6,60,1,52,'#3a3a44');R(g,edge-8,58,5,3,'#3a3a44');R(g,edge-7,59,3,1,'#fff6d0');
 // a mailbox on the corner
 R(g,edge-16,FL-CURB-14,7,10,'#2f5fa0');R(g,edge-16,FL-CURB-14,7,2,'#4a7ac8');R(g,edge-15,FL-CURB-4,5,4,'#3a3a44');
 // sidewalk slabs, then the curb face and the street
 R(g,0,FL-CURB,edge,CURB+40,'#cfc8ba');R(g,0,FL-CURB,edge,1,'#e7e1d8');for(let x=0;x<edge;x+=10)R(g,x,FL-CURB+1,1,CURB-1,'#bdb5a6');
 for(let y=FL+2;y<WH;y+=6){R(g,0,y,edge,1,'#bdb5a6');for(let x=((y*5)%10);x<edge;x+=10)R(g,x,y-5,1,5,'#bdb5a6')}
 R(g,edge-1,FL-CURB,2,CURB+1,'#a9a090');R(g,edge-1,FL-CURB,2,1,'#e7e1d8');
 R(g,edge,FL,WW-edge,40,'#55555f');R(g,edge,FL,WW-edge,2,'#3a3a44');for(let y=FL+2;y<WH;y++)for(let x=edge+((y*7)%5);x<WW;x+=5)px(g,x,y,(x+y)%3?'#5c5c66':'#4c4c56');
 R(g,edge,FL+2,3,38,'#6a6a74'); // gutter
 R(g,edge+10,FL+12,8,2,'#e8e4d8');R(g,edge+26,FL+12,8,2,'#e8e4d8'); // lane dashes
 // a parked 1960s sedan at the far right
 const cx=edge+18;R(g,cx,FL-10,26,8,'#7a9ab8');R(g,cx+5,FL-15,14,5,'#7a9ab8');R(g,cx+6,FL-14,5,4,'#cfe0e8');R(g,cx+13,FL-14,5,4,'#cfe0e8');R(g,cx,FL-10,26,1,'#9ab8d0');
 R(g,cx+3,FL-2,5,4,'#2a2a34');R(g,cx+18,FL-2,5,4,'#2a2a34');px(g,cx+5,FL,'#8a8a96');px(g,cx+20,FL,'#8a8a96');R(g,cx,FL-8,2,2,'#f4ecd8');
}
function sceneCurb(t){
 const g=wg,edge=52;telegraph(g,t,edge);
 // the poured ramp grows after 26.8
 const pour=ease(seg(t,26.8,29.0));
 if(pour>0){const L=Math.round(pour*24);for(let i=0;i<L;i++){const h=Math.round(CURB*(1-i/24));R(g,edge-6+i,FL-h,1,h,'#a7a19a');R(g,edge-6+i,FL-h,1,1,'#d8d2c8')}}
 if(t<26.36){
  const u=ease(seg(t,24.0,25.2)),ox=lerp(-30,6,u);const P=roll(t,ox+30,u<1);if(u>=1){P.face='o';P.mouth='flat'}
  person(P,ox,CURB,LOOK.ed);
  if(t>25.2){const a=ease(seg(t,25.2,25.5));wg.globalAlpha=a;const bx=ox+38,by=FL-CURB-38;R(g,bx,by,2,5,CORAL);R(g,bx,by+6,2,2,CORAL);wg.globalAlpha=1}
 }else{
  const ax=t<29.0?40:lerp(40,64,ease(seg(t,29.0,29.6)));const P=Object.assign({},t<29.0?{legs:stand2}:walkP(ax*3),t<29.0?{arms:[{ua:0,fa:0},{ua:0,fa:0}],armRel:[[8,9],[7,10]],lean:10,face:'n',mouth:'smile',look:1}:{face:'happy',mouth:'smile',armRel:[[6,6],null]});
  const pouring=t<29.0;const inf=person(P,ax,0,LOOK.att,null,pouring);
  const hx=pouring?Math.round(ax)+W-inf.h[0][0]:Math.round(ax)+inf.h[0][0],hy=OY+inf.h[0][1];
  // the bag, tilted, mouth toward the curb; both hands on it
  if(pouring){R(g,hx-8,hy-5,9,7,'#e8e0cc');R(g,hx-7,hy-4,6,2,'#c43c3c');R(g,hx-9,hy-2,2,3,'#d8d0bc');R(g,hx-1,hy-1,2,3,LOOK.att.skin);R(g,hx-4,hy+1,2,2,LOOK.att.skin)}
  else{R(g,hx-2,hy-1,7,6,'#e8e0cc');R(g,hx-1,hy,5,2,'#c43c3c');R(g,hx-1,hy-2,3,3,LOOK.att.skin)}
  if(t<29.0){for(let k=0;k<7;k++)px(g,hx-10-Math.round(k*.5),hy+1+k*2+((Math.floor(t*14)+k)%2),'#8e8e94')}
  const roll2=ease(seg(t,29.2,30.05));const ox=lerp(-36,-18,ease(seg(t,26.4,27.2)))+roll2*38;
  const wx=ox+37;const yy=wx<edge-6?CURB:Math.max(0,CURB*(1-(wx-(edge-6))/24));
  const Q=roll(t,ox+40,t<27.2||t>29.0);if(t>29.2){Q.face='happy'}person(Q,ox,yy,LOOK.ed);
 }
 return{}}
// ---------- S7 : director (30.06-35.47) ----------
function sceneDirector(t){
 const g=wg;office(g,t,true);
 // the desk sits left of centre; Ed is at its end, fully in view, the file in front of him
 R(g,28,96,32,3,'#6b4e36');R(g,28,96,32,1,'#8a6a4a');R(g,28,99,32,20,'#5a3e28');R(g,30,101,12,16,'#6b4e36');R(g,44,101,14,16,'#6b4e36');for(let d=0;d<3;d++)R(g,46,103+d*5,10,1,'#4a3220');
 glowRect(g,26,FL,36,6,'#2a1a10',.3);
 R(g,30,89,7,7,'#3a3a44');R(g,31,90,5,2,'#4a4a56');R(g,30,87,7,2,'#f4ecd8'); // typewriter
 R(g,42,90,16,7,'#e9d9a6');R(g,42,90,16,1,'#fff2c8');for(let k=0;k<3;k++)R(g,44,92+k*2,12,1,'#a9a090'); // the old file
 const P=roll(t,0,false);if(P.face!='closed'&&t>32.4)P.face='happy';
 person(P,34,0,LOOK.ed);
 return{}}
// ---------- S8 : today's curb ramp (35.47-40.53) ----------
function sceneToday6(t){
 const g=wg;for(let y=0;y<FL;y++)R(g,0,y,WW,1,mixc('#8fb9e3','#d9ecf7',y/FL));R(g,0,0,WW,56,NAVY);
 cloud(g,14,64,18);
 // a modern street corner: glass storefront, planter, signal pole with a push button
 R(g,0,44,WW,76,'#e6e1d6');R(g,0,44,WW,1,'#f2ede4');R(g,0,48,WW,3,'#c9c2b4');
 for(let x=4;x<WW;x+=22){R(g,x,56,18,40,'#3a3a4a');R(g,x+1,57,16,38,'#9ec0d8');R(g,x+1,57,16,10,'#c8dfe8');R(g,x+9,57,1,38,'#3a3a4a')}
 R(g,36,64,20,32,'#3a3a4a');R(g,37,65,18,30,'#9ec0d8');R(g,45,65,2,30,'#3a3a4a');R(g,42,80,2,2,'#2f6fd0'); // entrance with the access sign
 R(g,41,76,6,6,'#2f6fd0');R(g,43,77,2,2,'#f6fbff');R(g,42,80,4,1,'#f6fbff');
 R(g,2,100,16,12,'#6a6a7a');R(g,2,100,16,1,'#8a8a9a');R(g,3,96,14,5,'#4f7a3c');R(g,4,94,12,3,'#6a9a52'); // planter
 const edge=30,RL=48;
 R(g,0,FL-CURB,edge,CURB+40,'#cfc8ba');R(g,0,FL-CURB,edge,1,'#e7e1d8');
 for(let i=0;i<RL;i++){const h=Math.round(CURB*(1-i/RL));R(g,edge+i,FL-h,1,h+40,'#b9b1a2');R(g,edge+i,FL-h,1,1,'#e7e1d8');R(g,edge+i,FL-h+1,1,1,'#cfc8ba');if(i%8==0)R(g,edge+i,FL-h+2,1,h+38,'#a9a193')}
 for(let y=FL+2;y<WH;y+=6)R(g,0,y,edge,1,'#bdb5a6');R(g,edge-1,FL-CURB,1,CURB+40,'#a9a193');
 // detectable warning: truncated domes, 2 px grid
 R(g,edge+RL-14,FL-2,14,2,'#e0a63a');for(let i=0;i<7;i++){px(g,edge+RL-13+i*2,FL-2,'#f0c24a')}
 R(g,edge+RL,FL,WW-edge-RL,40,'#4a4a56');R(g,edge+RL,FL,WW-edge-RL,1,'#3a3a44');for(let y=FL+2;y<WH;y+=3)R(g,edge+RL,y,WW-edge-RL,1,'#4e4e5a');
 for(let k=0;k<3;k++)R(g,edge+RL+2,FL+6+k*8,10,3,'#e8e4d8'); // crosswalk bars
 R(g,edge+RL+2,70,1,50,'#3a3a44');R(g,edge+RL,66,5,6,'#3a3a44');px(g,edge+RL+2,67,'#c43c3c');px(g,edge+RL+2,70,'#3fa650');R(g,edge+RL+1,96,3,4,'#8a8a96');px(g,edge+RL+2,97,'#f4ecd8'); // signal + push button
 glowRect(g,0,FL-4,WW,4,'#2a2a3a',.12);
 const u=seg(t,35.6,40.3),ox=lerp(-24,46,u),wx=ox+37;
 const yy=wx<edge?CURB:wx>edge+RL?0:CURB*(1-(wx-edge)/RL);
 drawKitY(roll(t,ox+40,true),ox,yy);
 return{}}
