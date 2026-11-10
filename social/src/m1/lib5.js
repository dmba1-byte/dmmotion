// ---------- people ----------
const LOOK={
 judy:{skin:'#e9c3a3',skinD:'#c99d7e',hair:'#5a3426',top:'#d9564f',topL:'#ee7d74',pants:'#3f4a6b',shoe:'#2c2a3a'},
 girl:{skin:'#e9c3a3',skinD:'#c99d7e',hair:'#5a3426',top:'#e7a3b8',topL:'#f4c2d2',pants:'#7a8fb8',shoe:'#e8dcc8',hw:10,hh:10,th:7,sh:6,tl:8,ua:5,fa:5,tw:7,foot:4,lw:3},
 a1:{skin:'#8a5a3c',skinD:'#6e452d',hair:'#1c1418',top:'#3f8fb0',topL:'#66b1cf',pants:'#4b4b5e',shoe:'#d8d0c0'},
 a2:{skin:'#f0caa8',skinD:'#d2a886',hair:'#c9a24a',top:'#7ab36a',topL:'#9ccf8c',pants:'#3a3550',shoe:'#5a4a3a'},
 a3:{skin:'#c98b69',skinD:'#a86f52',hair:'#2a1f28',top:'#e0b24a',topL:'#f0cf7a',pants:'#5b5f7a',shoe:'#e8dcc8'},
 a4:{skin:'#6e4430',skinD:'#563322',hair:'#121014',top:'#8a5cc4',topL:'#a983db',pants:'#2f3248',shoe:'#cfc6b6'},
 p1:{skin:'#5e3a28',skinD:'#4a2c1e',hair:'#111014',top:'#26232e',topL:'#3a3644',pants:'#1f1d26',shoe:'#121016'},
 p2:{skin:'#7a4c33',skinD:'#5f3a26',hair:'#111014',top:'#2e2a36',topL:'#433e4e',pants:'#24212c',shoe:'#121016'}};
function longHair(col){return(g,i)=>{R(g,i.hx-2,i.hy-2,i.hw+3,4,col);R(g,i.hx-2,i.hy,4,11,col);R(g,i.hx-1,i.hy+10,3,2,col)}}
function glasses(g,i){const x=i.hx+i.hw-6,y=i.hy+4;R(g,x,y,5,1,'#2a1f28');R(g,x,y+3,5,1,'#2a1f28');R(g,x,y,1,4,'#2a1f28');R(g,x+4,y,1,4,'#2a1f28')}
function person(P,ox,oy,look,front,flip){
 const sv=Object.assign({},K);Object.assign(K,look||{});P.nobag=P.nobag!==false;
 const ch=mk(),cg=ch.getContext('2d');let inf;
 try{inf=kit(cg,P);front&&front(cg,inf)}finally{Object.assign(K,sv)}
 outline(ch);
 if(flip){wg.save();wg.translate(Math.round(ox)+W,OY-Math.round(oy||0));wg.scale(-1,1);wg.drawImage(ch,0,0);wg.restore();inf.fx=Math.round(ox)+W-inf.nx}
 else wg.drawImage(ch,Math.round(ox),OY-Math.round(oy||0));return inf}
function roll(t,dist,moving){
 if(!moving){const br=Math.sin(t*PI2/3.1);const blink=((t+dist*.01)%3.4)<.12;return seated({mode:'rest',spin:dist/8*57.3,face:blink?'closed':'n',mouth:'smile',lean:4+br*.8,dy:br>0.6?-1:0})}
 const ph=(q12(t)*1.15)%1,push=ph<.6,u=push?ph/.6:(ph-.6)/.4,a=push?lerp(-65,18,u):lerp(18,-65,u),r=push?8:9.5+Math.sin(u*PI)*1.5;
 return seated({mode:'push',a,r,spin:dist/8*57.3,face:'n',mouth:'smile'})}
function judyP(P){P.pre=longHair(LOOK.judy.hair);return P}
function sign(g,hx,hy,txtc,skin){
 // board held up by the hand at (hx,hy): pole from the fist up to the board
 const bw=15,bh=9,bx=Math.round(hx)-7,by=Math.round(hy)-24;
 R(g,Math.round(hx),by+bh,1,Math.round(hy)-by-bh+3,'#7a5a3a');
 R(g,bx-1,by-1,bw+2,bh+2,'#1a162e');R(g,bx,by,bw,bh,'#f4e9d0');R(g,bx,by,bw,1,'#fff8e6');
 const glyph={'5':[7,4,6,1,6],'0':[7,5,5,5,7],'4':[5,5,7,1,1]};let cx=bx+2;
 for(const ch of txtc){const rows=glyph[ch];if(rows)rows.forEach((m,r)=>{for(let b=0;b<3;b++)if(m&(4>>b))px(g,cx+b,by+2+r,'#c43c3c')});cx+=4}
 // fist wraps the pole
 R(g,Math.round(hx)-1,Math.round(hy)-1,3,3,'#1a162e');R(g,Math.round(hx)-1,Math.round(hy),3,2,skin)}
const lamp=(g,x,y,on)=>{R(g,x-2,y,5,2,'#3a3560');if(on){g.globalAlpha=.16;R(g,x-8,y+2,17,20,'#fff2c8');g.globalAlpha=1;R(g,x-1,y+2,3,1,'#fff2c8')}};
function floorStripes(g,a,b){for(let y=FL+1;y<WH;y++)R(g,0,y,WW,1,((y-FL-1)%6==0)?a:b);R(g,0,FL,WW,1,shade(b,.7))}

function lobby(g,dim){
 R(g,0,0,WW,FL,mixc('#3c3a58','#1c1a30',dim));for(let x=0;x<WW;x+=12)R(g,x,0,2,FL,mixc('#46446a','#24223c',dim));
 R(g,0,104,WW,16,mixc('#4b4868','#26243e',dim));
 floorStripes(g,mixc('#2a2846','#16142a',dim),mixc('#34325a','#1e1c36',dim));
}
function crate(g,x,y,steam,t,w){w=w||14;R(g,x,y,w,8,'#a87a4a');R(g,x,y,w,1,'#c99a62');R(g,x+2,y+3,w-4,2,'#7a5432');
 if(steam)for(let k=0;k<2;k++){const yy=y-1-((Math.floor(t*8)+k*2)%4);g.globalAlpha=.75;px(g,x+1+k*2,yy,'#e8e4f0');g.globalAlpha=1}}
function zee(x,y){R(wg,x,y,4,1,'#cfd6ff');px(wg,x+2,y+1,'#cfd6ff');px(wg,x+1,y+2,'#cfd6ff');R(wg,x,y+3,4,1,'#cfd6ff')}
function parked(g,WX,WY){R(g,WX-4,WY-16,2,12,'#3a3a54');R(g,WX-4,WY-16,4,2,'#2a2a3c');R(g,WX-4,WY-5,11,2,'#3a3a54');R(g,WX+6,WY-5,2,5,'#3a3a54');R(g,WX+6,WY-1,4,1,'#2a2a3c');
 chairWheel(g,WX,WY,7,20);R(g,WX+7,WY+5,3,3,'#6a6a88')}

function drawKitY(P,ox,oy){const ch=mk(),cg=ch.getContext('2d');kit(cg,P);outline(ch);wg.drawImage(ch,Math.round(ox),OY-Math.round(oy))}

function stamp(s,col,x,y,t0,t,rot,sz){sz=sz||64;const u=seg(t,t0,t0+.14);if(u<=0)return;const sc=lerp(2.2,1,ease(u));
 og.save();og.translate(x,y);og.rotate(rot);og.scale(sc,sc);og.globalAlpha=Math.min(1,u*1.5);
 const w=mw(s,sz)+sz*.9,h=sz*1.75;og.strokeStyle=col;og.lineWidth=sz*.16;rrect(og,-w/2,-h/2,w,h,10);og.stroke();
 mdraw(s,0,sz*.06,sz,col,'center',false,'',0,Math.min(1,u*1.5));og.restore()}
function shake(t,t0){const u=seg(t,t0,t0+.25);return u>0&&u<1?Math.round(Math.sin(u*40)*(1-u)*14):0}


function glowRect(g,x,y,w,h,col,a){g.globalAlpha=a;R(g,x,y,w,h,col);g.globalAlpha=1}
function cloud(g,x,y,w){R(g,x,y,w,3,'#f6fbff');R(g,x+3,y-2,w-6,2,'#f6fbff');R(g,x+2,y+3,w-4,1,'#e4eef8')}
function tree(g,x,base,h,t,k){ // trunk + layered canopy, leaves shimmer
 R(g,x,base-h,3,h,'#5a3a24');R(g,x+1,base-h,1,h,'#7a5434');
 const w=Math.round(h*.9),cy=base-h-2;const sw=Math.round(Math.sin(t*1.1+k))*(h>14?1:0);
 R(g,x+1-w/2+sw,cy,w,Math.round(h*.45),'#4f7a3c');R(g,x+1-w/2+2+sw,cy-3,w-4,4,'#5a8a44');R(g,x+1-w/2+4+sw,cy-5,w-8,3,'#6a9a52');
 R(g,x+1-w/2+2+sw,cy+Math.round(h*.45)-2,w-4,2,'#3f6630');
 for(let i=0;i<4;i++)px(g,x+1-w/2+2+((i*5+k*3)%(w-4))+sw,cy+1+((i*3+k)%(Math.round(h*.4))),'#7fb060');
}

function sit(o){o=o||{};const hx=CX-2,hy=GY-13;const P={hip:[hx,hy],legRel:[[8,7],[9,7]],arms:[{ua:20,fa:40},{ua:10,fa:30}],lean:o.lean==null?8:o.lean,face:o.face||'closed',mouth:o.mouth||'flat',look:o.look};
 if(o.hand)P.armIK=[o.hand,null];return P}
function bench(g,x,dim){const m=(a,b)=>mixc(a,b,dim||0);R(g,x,107,16,2,m('#6b4e36','#15132a'));R(g,x+1,109,2,11,m('#5a3e28','#100e1e'));R(g,x+13,109,2,11,m('#5a3e28','#100e1e'))}
