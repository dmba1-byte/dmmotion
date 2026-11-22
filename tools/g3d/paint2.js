()=>{
const out={};
const mkc=(w,h)=>{const c=document.createElement('canvas');c.width=w;c.height=h;return c};
const AMB='#f2c14e',OUT='#1c1630';
const hx=c=>{const n=parseInt(c.slice(1),16);return[(n>>16)&255,(n>>8)&255,n&255]};
const mix=(a,b,k)=>{const A=hx(a),B=hx(b);return'#'+A.map((v,i)=>Math.round(v+(B[i]-v)*k).toString(16).padStart(2,'0')).join('')};
const rnd=s=>{let x=Math.sin(s*127.1+311.7)*43758.5453;return x-Math.floor(x)};
const pen=g=>(x,y,w,h,c)=>{g.fillStyle=c;g.fillRect(Math.round(x),Math.round(y),Math.round(w),Math.round(h))};
function text2(g,s,cx,y,col,sc){const w=ptw(s),t=mkc(w+2,8),tg=t.getContext('2d');ptext(tg,s,0,0,col);g.imageSmoothingEnabled=false;g.drawImage(t,Math.round(cx-w*sc/2),y,(w+2)*sc,8*sc)}
const save=(n,c)=>{out[n]=c.toDataURL()};
// roof 128: tar paper with seams, patches, drain, gravel
{const c=mkc(128,128),R=pen(c.getContext('2d'));R(0,0,128,128,'#3a3454');for(let i=0;i<1400;i++){const x=rnd(i)*128,y=rnd(i*1.7+3)*128,r=rnd(i*2.3);R(x,y,1,1,r>.6?'#48426a':r>.3?'#2e2846':'#403a5e')}
 for(let y=0;y<128;y+=32){R(0,y,128,1,'#2a2440');R(0,y+1,128,1,'#4a4468')}for(let i=0;i<4;i++){const x=10+rnd(i+9)*90,y=8+rnd(i+19)*100;R(x,y,18,12,'#332d4c');R(x,y,18,1,'#4a4468');R(x,y+11,18,1,'#241e3a')}
 R(60,60,8,8,OUT);R(61,61,6,6,'#55506a');R(63,61,1,6,OUT);R(61,63,6,1,OUT);save('roof2',c)}
// manhole 32, grate 32x16
{const c=mkc(32,32),g=c.getContext('2d'),R=pen(g);g.fillStyle=OUT;g.beginPath();g.arc(16,16,15,0,7);g.fill();g.fillStyle='#4a4468';g.beginPath();g.arc(16,16,13,0,7);g.fill();g.fillStyle='#3a3454';g.beginPath();g.arc(16,16,11,0,7);g.fill();for(let i=-8;i<=8;i+=4){R(16+i-1,8,2,16,'#2a2440');R(8,16+i-1,16,2,'#2a2440')}R(15,15,2,2,'#6a6488');save('manhole',c)}
{const c=mkc(32,16),R=pen(c.getContext('2d'));R(0,0,32,16,OUT);R(1,1,30,14,'#3a3454');for(let i=3;i<30;i+=4)R(i,3,2,10,'#120e22');save('grate',c)}
// road arrow 24x48, parking line handled by plain planes
{const c=mkc(24,48),g=c.getContext('2d'),R=pen(g);const col='#cfc8e0';for(let i=0;i<12;i++)R(12-i,i,i*2,1,col);R(8,12,8,34,col);save('arrow',c)}
// umbrella stripes 64x16
{const c=mkc(64,16),R=pen(c.getContext('2d'));for(let i=0;i<8;i++){R(i*8,0,8,16,i%2?'#f3ecd8':'#2f9c7a');R(i*8,0,1,16,i%2?'#ffffff':'#49d08a')}R(0,14,64,2,'#1f6a55');save('umb',c)}
// wood top 24
{const c=mkc(24,24),R=pen(c.getContext('2d'));R(0,0,24,24,'#b98a5e');for(let y=0;y<24;y+=6){R(0,y,24,1,'#e6c08e');R(0,y+5,24,1,'#8a5e3c');R(3+y,y+2,8,1,'#a87a50')}save('wood',c)}
// barrel wood (water tower) 32
{const c=mkc(32,32),R=pen(c.getContext('2d'));R(0,0,32,32,'#7a4e30');for(let x=0;x<32;x+=4){R(x,0,1,32,'#5a3820');R(x+1,0,1,32,'#8f6040')}R(0,6,32,2,'#3a3454');R(0,24,32,2,'#3a3454');R(0,6,32,1,'#6a6488');save('barrel',c)}
// hedge 24, flowers 24, water 32, stone 24
{const c=mkc(24,24),R=pen(c.getContext('2d'));R(0,0,24,24,'#1c6240');for(let i=0;i<50;i++){const x=rnd(i+3)*24,y=rnd(i*2+5)*24,r=rnd(i*3.1);R(x,y,2,2,r>.6?'#2f9c63':r>.3?'#237a4c':'#17503a')}save('hedge',c)}
{const c=mkc(24,24),R=pen(c.getContext('2d'));R(0,0,24,24,'#237a4c');const cs=['#e88a98','#f4d27a','#d9695f','#a88be0','#f3ecd8'];for(let i=0;i<22;i++){const x=1+rnd(i+13)*21,y=1+rnd(i*2+15)*21;R(x,y,2,2,cs[i%5]);R(x,y,1,1,'#ffffff')}for(let i=0;i<20;i++)R(rnd(i+40)*24,rnd(i+50)*24,1,2,'#2f9c63');save('flowers',c)}
{const c=mkc(32,32),R=pen(c.getContext('2d'));R(0,0,32,32,'#3f7c9c');for(let i=0;i<26;i++){const x=rnd(i+23)*30,y=rnd(i*2+25)*30;R(x,y,4+rnd(i)*4,1,i%3?'#6fb0d0':'#d6ecf8')}save('water',c)}
{const c=mkc(24,24),R=pen(c.getContext('2d'));R(0,0,24,24,'#9a93b2');R(0,0,24,1,'#c8c0e0');R(0,23,24,1,'#6a6488');R(0,0,1,24,'#b0a8c8');R(23,0,1,24,'#6a6488');R(5,8,6,1,'#8078a0');R(13,15,5,1,'#8078a0');R(11,0,1,24,'#8078a0');save('stone',c)}
// iron fence 24x24 (transparent)
{const c=mkc(24,24),g=c.getContext('2d'),R=pen(g);for(let x=2;x<24;x+=6){R(x,3,2,21,OUT);R(x,1,2,2,AMB)}R(0,6,24,2,OUT);R(0,19,24,2,OUT);save('fence',c)}
// crate with produce 24x24 top, crate side 24x16
{const c=mkc(24,16),R=pen(c.getContext('2d'));R(0,0,24,16,'#6b4329');for(let y=0;y<16;y+=5){R(0,y,24,4,'#b98a5e');R(0,y,24,1,'#e6c08e')}R(0,0,2,16,'#8a5e3c');R(22,0,2,16,'#8a5e3c');save('crate',c)}
for(const [n,a,b] of [['prod1','#f09a3c','#ffd08a'],['prod2','#d9695f','#f09088'],['prod3','#49d08a','#a8ecc4'],['prod4','#f4d27a','#fff0b8']]){const c=mkc(24,24),g=c.getContext('2d'),R=pen(g);R(0,0,24,24,'#3a261c');for(let j=0;j<4;j++)for(let i=0;i<4;i++){const x=1+i*6-(j%2),y=1+j*6;g.fillStyle=a;g.beginPath();g.arc(x+3,y+3,3,0,7);g.fill();R(x+1,y+1,2,1,b)}R(0,0,24,1,'#8a5e3c');R(0,23,24,1,'#8a5e3c');R(0,0,1,24,'#8a5e3c');R(23,0,1,24,'#8a5e3c');save(n,c)}
// small plaques with text
function plaque(n,s,bg,fg,sc,em){const w=ptw(s)*sc+12,h=8*sc+6,c=mkc(w,h),g=c.getContext('2d'),R=pen(g);R(0,0,w,h,OUT);R(1,1,w-2,h-2,bg);R(1,1,w-2,1,mix(bg,'#ffffff',.3));text2(g,s,w/2,3,fg,sc);save(n,c);if(em){const e=mkc(w,h),eg=e.getContext('2d');pen(eg)(0,0,w,h,'#000');text2(eg,s,w/2,3,em,sc);save(n+'_e',e)}}
plaque('st_sign','MERIDIAN ST','#1f6a55','#f3ecd8',1);plaque('bus_sign','BUS','#346a88','#f3ecd8',2);plaque('atm','ATM','#141026','#6df2c4',2,'#6df2c4');plaque('open','OPEN','#141026','#ff8a7a',2,'#ff8a7a');
plaque('bill','UP TO CODE','#221c3c',AMB,5,'#ffe9a0');plaque('bill2','PLAY FREE','#221c3c','#6df2c4',3,'#6df2c4');plaque('park_sign','ODESSA PARK','#3a261c','#f3ecd8',2);
// blade sign icons 20x20
{const c=mkc(20,20),R=pen(c.getContext('2d'));R(0,0,20,20,OUT);R(1,1,18,18,'#f3ecd8');R(5,8,9,8,'#a8584a');R(5,8,9,1,'#d9695f');R(14,10,3,4,'#a8584a');R(15,11,1,2,'#f3ecd8');R(7,4,1,3,'#9a94b0');R(10,3,1,4,'#9a94b0');save('ic_cafe',c)}
{const c=mkc(20,20),R=pen(c.getContext('2d'));R(0,0,20,20,OUT);R(1,1,18,18,'#f3ecd8');R(4,5,5,11,'#3f7c6c');R(9,4,3,12,'#d9695f');R(12,6,4,10,'#f4d27a');R(4,7,5,1,'#f3ecd8');R(12,8,4,1,'#8a6c2c');save('ic_books',c)}
{const c=mkc(20,20),R=pen(c.getContext('2d'));R(0,0,20,20,OUT);R(1,1,18,18,'#f3ecd8');R(4,9,12,7,'#b88a5a');R(6,5,3,4,'#49d08a');R(10,4,3,5,'#f09a3c');R(13,6,2,3,'#d9695f');save('ic_market',c)}
// bike 2 frames, 44x28 transparent
for(const f of [0,1]){const c=mkc(44,28),g=c.getContext('2d'),R=pen(g);const wheel=(cx,cy)=>{g.strokeStyle=OUT;g.lineWidth=3;g.beginPath();g.arc(cx,cy,7.5,0,7);g.stroke();g.strokeStyle='#9a94b0';g.lineWidth=1;g.beginPath();g.arc(cx,cy,5.5,0,7);g.stroke();g.strokeStyle='#d8d0e8';g.beginPath();if(f){g.moveTo(cx-5,cy);g.lineTo(cx+5,cy);g.moveTo(cx,cy-5);g.lineTo(cx,cy+5)}else{g.moveTo(cx-4,cy-4);g.lineTo(cx+4,cy+4);g.moveTo(cx-4,cy+4);g.lineTo(cx+4,cy-4)}g.stroke();R(cx-1,cy-1,2,2,OUT)};
 wheel(9,19);wheel(34,19);g.strokeStyle=OUT;g.lineWidth=4;g.beginPath();g.moveTo(9,19);g.lineTo(18,8);g.lineTo(30,8);g.lineTo(34,19);g.moveTo(18,8);g.lineTo(21,19);g.lineTo(30,8);g.moveTo(21,19);g.lineTo(9,19);g.stroke();
 g.strokeStyle='#d9695f';g.lineWidth=2;g.beginPath();g.moveTo(9,19);g.lineTo(18,8);g.lineTo(30,8);g.lineTo(34,19);g.moveTo(18,8);g.lineTo(21,19);g.lineTo(30,8);g.moveTo(21,19);g.lineTo(9,19);g.stroke();
 R(13,4,9,3,OUT);R(14,5,7,1,'#6b4329');R(17,6,2,3,OUT);R(29,2,2,7,OUT);R(28,1,7,3,OUT);R(29,2,5,1,'#d8d0e8');R(19,17,5,4,OUT);R(20,18,3,2,AMB);
 const d=g.getImageData(0,0,44,28),p=d.data;for(let i=3;i<p.length;i+=4)p[i]=p[i]>110?255:0;g.putImageData(d,0,0);save('bike'+f,c)}
// bus shelter glass ad 32x40, newspaper/mailbox faces 16x24
{const c=mkc(32,40),R=pen(c.getContext('2d'));R(0,0,32,40,OUT);R(1,1,30,38,'#fff2c8');R(3,3,26,16,'#5a9cba');R(3,3,26,3,'#8cc8e0');R(8,10,6,9,'#f4d27a');R(18,8,8,11,'#d9695f');R(3,22,26,2,'#1c1630');R(3,26,20,2,'#55506a');R(3,30,24,2,'#55506a');R(3,34,14,2,'#55506a');save('ad',c)}
{const c=mkc(16,24),R=pen(c.getContext('2d'));R(0,0,16,24,'#346a88');R(0,0,16,2,'#6fb0d0');R(2,6,12,3,'#1f4258');R(3,7,10,1,'#0a0818');R(4,13,8,6,'#f3ecd8');R(5,14,6,1,'#346a88');R(5,16,4,1,'#346a88');save('mail',c)}
{const c=mkc(16,24),R=pen(c.getContext('2d'));R(0,0,16,24,'#d9695f');R(0,0,16,2,'#f09088');R(2,4,12,10,'#2a3148');R(3,5,10,8,'#f3ecd8');R(4,6,8,2,'#1c1630');R(4,9,5,1,'#55506a');R(4,11,7,1,'#55506a');R(6,17,4,2,'#f4d27a');save('news',c)}
return out}
