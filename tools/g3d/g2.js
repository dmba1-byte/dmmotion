
// ---------- helpers added for the playable build ----------
const cyl=(rt,rb,h,seg,m,x,y,z)=>{const c=new T.Mesh(new T.CylinderGeometry(rt,rb,h,seg),m);c.position.set(x,y,z);c.castShadow=true;c.receiveShadow=true;scene.add(c);return c};
const bas=c=>new T.MeshBasicMaterial({color:c});
const M_={};const col=c=>M_[c]||(M_[c]=lam({color:c}));
let OBSC=[];const OBS_S=[],OBS_L=[];const ob=(x0,z0,x1,z1)=>OBSC.push([x0,z0,x1,z1]);
function fl(n){const k=n+'~';if(TX[k])return TX[k];const im=TX[n].image,c=document.createElement('canvas');c.width=im.width;c.height=im.height;const g=c.getContext('2d');g.translate(c.width,0);g.scale(-1,1);g.drawImage(im,0,0);const t=new T.CanvasTexture(c);t.magFilter=t.minFilter=T.NearestFilter;t.generateMipmaps=false;return TX[k]=t}
function setChar(sp,n,size,flip){const t=flip?fl(n):TX[n];if(sp.material.map!==t){sp.material.map=t;sp.material.needsUpdate=true}sp.scale.set(t.image.width*size,t.image.height*size,1)}
function mkBlob(sc_,rx,rz){const m=new T.MeshBasicMaterial({color:'#0a0618',transparent:true,opacity:.42,depthWrite:false});const c=new T.Mesh(new T.CircleGeometry(1,20),m);c.rotation.x=-Math.PI/2;c.scale.set(rx,rz,1);sc_.add(c);return c}
const NPCS=[];
function npc(sc_,look,size,pts,speed,gy){scene=sc_;const s=sprite('n_'+look+'_di',size,pts[0][0],gy,pts[0][1]);const b=mkBlob(sc_,11*size,5*size);NPCS.push({sc:sc_,look,size,pts,i:1%pts.length,x:pts[0][0],z:pts[0][1],sp:speed,walk:Math.random()*8,wait:Math.random()*2,s,b,gy,face:'d'})}
function lights(pts,cols){const g=new T.BoxGeometry(4,5,4);pts.forEach((p,i)=>{const m=new T.Mesh(g,bas(cols[i%cols.length]));m.position.set(p[0],p[1],p[2]);scene.add(m)})}
function strand(a,b,n,sag,cols){const pts=[];for(let i=0;i<=n;i++){const u=i/n;pts.push([a[0]+(b[0]-a[0])*u,a[1]+(b[1]-a[1])*u-Math.sin(u*Math.PI)*sag,a[2]+(b[2]-a[2])*u])}lights(pts,cols);
 const geo=new T.BufferGeometry().setFromPoints(pts.map(p=>new T.Vector3(p[0],p[1]+2,p[2])));scene.add(new T.Line(geo,new T.LineBasicMaterial({color:'#1c1630'})));glow((a[0]+b[0])/2,(a[1]+b[1])/2-sag,(a[2]+b[2])/2,Math.hypot(b[0]-a[0],b[2]-a[2])*.6,.18)}
function lampPost2(x,z,noOb){const dk=col('#221c3c');box(8,6,8,dk,x,9,z);box(4,150,4,dk,x,81,z);box(14,4,14,dk,x,160,z);box(18,2,18,col('#c9a24a'),x,157,z);box(12,14,12,bas('#fff2c8'),x,150,z,{noCast:true});glow(x,150,z,150,.9);pool(x,z,130,95,.55,6);if(!noOb)ob(x-6,z-6,x+6,z+6)}
function planter(x,z,w){box(w,12,18,col('#5a3a48'),x,12,z);box(w+2,3,20,col('#8a6272'),x,19,z);box(w-4,6,14,lam({map:rep('flowers',Math.max(1,Math.round(w/24)),1)}),x,22,z);ob(x-w/2-2,z-11,x+w/2+2,z+11)}
function facadeRelief(k,B,cx){const b=B[k],gh=b.gh,cor=20,fh=Math.floor((b.h-gh-cor)/b.floors),bay=b.w/b.cols,trim=col(b.trim),x0=cx-b.w/2;
 for(let f=0;f<b.floors;f++)for(let c=0;c<b.cols;c++){const ww=Math.round(bay*.46),wh=Math.round(fh*.58),x=x0+c*bay+bay/2,yTop=cor+f*fh+Math.round(fh*.2),y=b.h-(yTop+wh)-5;
  box(ww+14,4,7,trim,x,y,3.5,{noCast:true});box(ww+10,4,5,trim,x,b.h-yTop+5,2.5,{noCast:true});
  if(k==='hotel'&&f===1){box(ww+22,3,18,col('#3a3454'),x,y-3,9);const r=col('#1c1630');box(ww+22,14,2,r,x,y+6,17);box(2,14,16,r,x-(ww+22)/2,y+6,9);box(2,14,16,r,x+(ww+22)/2,y+6,9);box(ww+24,2,3,col('#c9a24a'),x,y+14,17)}
  else if((f*7+c*3+b.seed)%3===0){box(ww+8,7,8,col('#6b4329'),x,y+5,6);box(ww+4,5,6,lam({map:rep('flowers',2,1)}),x,y+10,6)}}
 if(b.pil)for(let i=0;i<=b.cols;i++){const x=x0+i*bay+(i===0?5:i===b.cols?-5:0);box(11,b.h-gh-cor,4,trim,x,gh+(b.h-gh-cor)/2,2)}
 box(b.w+6,8,6,trim,cx,gh+1,3,{noCast:true});box(4,b.h-10,4,col('#2a2440'),x0+b.w+4,b.h/2,4)}
function blade(ic,x,y){box(3,3,26,col('#221c3c'),x,y+14,13);const t=lam({map:TX[ic]}),d=col('#221c3c');const m=new T.Mesh(new T.BoxGeometry(3,22,22),[t,t,d,d,d,d]);m.position.set(x,y,22);m.castShadow=true;scene.add(m)}
function cafeSet(x,z,umb){box(4,16,4,col('#3a3454'),x,14,z);box(24,3,24,lam({map:TX.wood}),x,23,z);for(const dx of [-22,22]){box(11,2,11,col('#d9695f'),x+dx,16,z);box(2,10,2,col('#3a3454'),x+dx,11,z);box(11,12,2,col('#d9695f'),x+dx+(dx<0?-5:5),22,z)}
 box(5,6,5,col('#f3ecd8'),x-4,27,z+2);box(4,5,4,col('#a8584a'),x+6,27,z-3);
 if(umb){box(3,64,3,col('#f3ecd8'),x,38,z-1);const c=new T.Mesh(new T.ConeGeometry(34,16,8),lam({map:rep('umb',2,1)}));c.position.set(x,76,z-1);c.castShadow=true;scene.add(c)}ob(x-30,z-14,x+30,z+14)}
function crate(x,z,p,y){box(26,16,22,lam({map:TX.crate}),x,(y||6)+8,z);const t=lam({map:TX[p]}),s=lam({map:TX.crate});const m=new T.Mesh(new T.BoxGeometry(24,5,20),[s,s,t,s,s,s]);m.position.set(x,(y||6)+17,z);scene.add(m)}
function trafficLight(x,z,ry){const d=col('#221c3c');box(4,120,4,d,x,66,z);const g=new T.Group();const hb=new T.Mesh(new T.BoxGeometry(12,34,10),d);g.add(hb);[['#e2564f',10,1],['#4a3a20',0,0],['#1d4a3a',-10,0]].forEach(([c,y,on])=>{const l=new T.Mesh(new T.BoxGeometry(7,7,2),bas(c));l.position.set(0,y,6);g.add(l)});g.position.set(x,128,z);g.rotation.y=ry;scene.add(g);glow(x,138,z,40,.5);ob(x-5,z-5,x+5,z+5)}

async function street2(){scene=S_STREET;OBSC=OBS_S;
 const names=['pave','asph','grass','awn','cross','marq','marq_e','carpet','plant','bench','stanchions','car1_s','car2_s','car3_s','roof2','manhole','grate','arrow','umb','wood','barrel','hedge','flowers','water','stone','fence','crate','prod1','prod2','prod3','prod4','st_sign','bus_sign','atm','atm_e','open','open_e','bill','bill_e','bill2','bill2_e','park_sign','ic_cafe','ic_books','ic_market','bike0','bike1','ad','mail','news','dec_books'];
 const B=await (await fetch('art/bmeta.json')).json();for(const k in B)names.push(k+'_f',k+'_fe',k+'_s',k+'_se',k+'_r');
 await Promise.all(names.map(tex));mkGlow();sky();scene.fog=new T.Fog('#3a2c62',1400,3400);
 for(const k in B)TX[k+'_r']=TX.roof2;
 scene.add(new T.AmbientLight('#a59be0',.66));scene.add(new T.HemisphereLight('#ffb890','#2a2050',.4));
 const sun=new T.DirectionalLight('#ffb27a',.78);sun.position.set(-700,620,560);sun.castShadow=true;sun.shadow.mapSize.set(4096,4096);const sc=sun.shadow.camera;sc.left=-1500;sc.right=1500;sc.top=1300;sc.bottom=-1300;sc.near=10;sc.far=3400;sun.shadow.bias=-.0006;sun.shadow.normalBias=1.5;scene.add(sun);scene.add(sun.target);
 // ---- ground ----
 plane(6000,6000,lam({map:rep('grass',120,120)}),0,-.5,0,true);
 box(6000,6,140,lam({map:rep('pave',125,140/48)}),0,3,50,{noCast:true});box(6000,6,94,lam({map:rep('pave',125,94/48)}),0,3,425,{noCast:true});
 box(6000,7,5,col('#b8b0d0'),0,3.5,121,{noCast:true});box(6000,7,5,col('#b8b0d0'),0,3.5,379,{noCast:true});
 plane(6000,256,lam({map:rep('asph',6000/96,256/96)}),0,.2,250,true);
 const yl=bas('#c9a24a'),wl=bas('#b8b0d0');for(let x=-2400;x<2400;x+=110)if(x<-320||x>-210)plane(56,5,yl,x,.5,281,true);
 for(let x=-2000;x<2000;x+=190)if(Math.abs(x+262)>80){plane(4,66,wl,x,.5,160,true)}plane(4000,3,wl,0,.5,196,true);
 {const cw=new T.MeshBasicMaterial({map:rep('cross',14,1),transparent:true,color:'#cfc8e0'});const p=plane(256,90,cw,-262,.6,250,true);p.rotation.z=Math.PI/2}
 for(const [x,z] of [[-90,240],[380,318],[-700,236],[760,322]]){const m=new T.MeshBasicMaterial({map:TX.manhole,transparent:true});plane(34,34,m,x,.7,z,true)}
 for(const x of [-560,-40,330,820]){plane(34,16,new T.MeshBasicMaterial({map:TX.grate}),x,.7,134,true);plane(34,16,new T.MeshBasicMaterial({map:TX.grate}),x+120,.7,366,true)}
 for(const [x,z,r] of [[140,240,-Math.PI/2],[-520,240,-Math.PI/2],[620,320,Math.PI/2],[-120,320,Math.PI/2]]){const m=new T.MeshBasicMaterial({map:TX.arrow,transparent:true,opacity:.8});const p=plane(24,48,m,x,.6,z,true);p.rotation.z=r}
 plane(6000,900,col('#2c2844'),0,.1,-480,true);
 // ---- buildings ----
 const row=[['hotel',0],['cafe',-376],['books',-651],['bank',396],['apts',716],['bank',-941],['cafe',1011]];
 for(const [k,x] of row){building(k,B,x,0);facadeRelief(k,B,x)}
 building('books',B,-200,-430);building('bank',B,120,-450);building('cafe',B,460,-440);building('apts',B,-520,-440);building('apts',B,820,-450);building('books',B,-860,-450);
 for(let i=0;i<9;i++){const k=['bank','apts','books','bank','hotel'][i%5],b=B[k];const m=lam({map:TX[k+'_s'],emissiveMap:TX[k+'_se'],emissive:'#ffffff',emissiveIntensity:.5});const g=new T.Mesh(new T.BoxGeometry(b.d,b.h,200),m);g.scale.y=1.5+((i*7)%5)*.22;g.position.set(-1500+i*370,b.h*g.scale.y/2,-960-(i%3)*120);scene.add(g)}
 // ---- hotel entrance ----
 const gold=col('#c9a24a'),dkp=col('#221c3c');
 box(132,6,84,dkp,0,92,42);box(136,3,88,gold,0,96,42);box(5,90,5,gold,-60,46,80);box(5,90,5,gold,60,46,80);ob(-64,76,-56,84);ob(56,76,64,84);
 {const mq=new T.Mesh(new T.BoxGeometry(165,34,8),[dkp,dkp,dkp,dkp,lam({map:TX.marq,emissiveMap:TX.marq_e,emissive:'#ffffff',emissiveIntensity:.8}),dkp]);mq.position.set(0,116,82);mq.castShadow=true;scene.add(mq);glow(0,116,90,260,.35)}
 for(let i=-3;i<=3;i++)box(4,4,4,bas('#fff2c8'),i*18,88,60,{noCast:true});pool(0,60,120,70,.55,6);
 plane(64,112,lam({map:rep('carpet',1,7)}),0,6.3,62,true);
 awning(-140,74,0,112,34);awning(140,74,0,112,34);pool(-140,40,90,50,.4,6);pool(140,40,90,50,.4,6);
 for(const x of [-84,84]){solid('plant',1.6,16,x,26,{y:6});blob(x,24,20,10,.4,6);ob(x-18,10,x+18,30)}
 for(const x of [-36,36]){solid('stanchions',1.5,5,x,100,{y:6})}
 for(const x of [-196,196]){solid('bench',1.5,22,x,44,{y:6});blob(x,40,40,14,.35,6);ob(x-38,18,x+38,48)}
 box(34,3,22,col('#c9a24a'),0,7.5,14);
 // water tower, skylights, roof hut on the hotel
 {const h=B.hotel.h;for(const [dx,dz] of [[-14,-14],[14,-14],[-14,14],[14,14]])box(4,40,4,col('#3a3454'),120+dx,h+26,-200+dz);cyl(30,30,46,10,lam({map:rep('barrel',6,1)}),120,h+68,-200);const c=new T.Mesh(new T.ConeGeometry(34,20,10),col('#4e2f1c'));c.position.set(120,h+101,-200);c.castShadow=true;scene.add(c);
  for(const [x,z] of [[-120,-90],[-60,-90],[-120,-150]]){box(40,8,34,col('#55497e'),x,h+10,z);box(34,3,28,bas('#ffe2a0'),x,h+15,z,{noCast:true});glow(x,h+20,z,90,.4)}
  box(60,44,50,col('#6a5f98'),-130,h+28,-240);box(64,4,54,col('#d8d0e8'),-130,h+52,-240);box(16,30,2,col('#8a6c2c'),-130,h+21,-214);
  strand([-200,h+40,-20],[200,h+40,-20],22,14,['#fff2c8','#ff8a7a','#6df2c4','#f2c14e'])}
 // rooftop garden on the cafe, billboard on the bank
 {const h=B.cafe.h;for(const [x,z] of [[-440,-60],[-380,-60],[-320,-60]]){box(40,10,26,col('#5a3a48'),x,h+11,z);box(36,8,22,lam({map:rep('hedge',2,1)}),x,h+20,z)}cafeSet(-400,-140,true);OBSC.pop();cafeSet(-330,-150,false);OBSC.pop();strand([-490,h+50,-20],[-262,h+50,-20],14,12,['#fff2c8','#f2c14e'])}
 {const h=B.bank.h,d=col('#221c3c');for(const x of [300,400,500])box(5,60,5,d,x,h+36,-40);const mb=new T.Mesh(new T.BoxGeometry(250,56,6),[d,d,d,d,lam({map:TX.bill,emissiveMap:TX.bill_e,emissive:'#ffffff',emissiveIntensity:.9}),d]);mb.position.set(400,h+84,-36);mb.castShadow=true;scene.add(mb);
  const m2=new T.Mesh(new T.BoxGeometry(120,30,6),[d,d,d,d,lam({map:TX.bill2,emissiveMap:TX.bill2_e,emissive:'#ffffff',emissiveIntensity:.9}),d]);m2.position.set(400,h+38,-34);scene.add(m2);glow(400,h+80,-20,330,.3)}
 // ---- shops ----
 awning(-340,96,0,150,38);awning(-640,96,0,120,38);awning(700,96,0,170,38);pool(-340,40,110,50,.4,6);pool(-640,40,90,50,.35,6);pool(410,40,120,50,.35,6);pool(700,40,120,50,.35,6);
 blade('ic_cafe',-500,150);blade('ic_books',-760,150);blade('ic_market',850,150);
 cafeSet(-400,56,true);cafeSet(-320,48,true);cafeSet(-282,96,false);
 {const g=solid('dec_books',1.5,16,-630,34,{y:6});ob(-670,14,-590,38);crate(-570,30,'prod4');ob(-585,18,-555,42)}
 {const d=col('#141026');box(40,56,8,d,470,34,4);const s=new T.Mesh(new T.BoxGeometry(34,22,2),[d,d,d,d,lam({map:TX.atm,emissiveMap:TX.atm_e,emissive:'#ffffff'}),d]);s.position.set(470,44,9);scene.add(s);box(22,6,6,col('#55506a'),470,24,8);glow(470,44,14,70,.4);pool(470,30,50,36,.3,6);
  for(const x of [276,326]){cyl(7,7,100,8,col('#c8d0e8'),x,56,10);box(18,6,18,col('#c8d0e8'),x,9,10);box(18,6,18,col('#c8d0e8'),x,106,10)}}
 for(const [x,z,p] of [[660,26,'prod1'],[692,26,'prod2'],[724,26,'prod3'],[756,26,'prod4'],[676,50,'prod3'],[740,50,'prod1']])crate(x,z,p);ob(645,12,772,62);
 {const d=col('#141026');const s=new T.Mesh(new T.BoxGeometry(40,20,2),[d,d,d,d,lam({map:TX.open,emissiveMap:TX.open_e,emissive:'#ffffff'}),d]);s.position.set(-430,78,2);scene.add(s);glow(-430,78,8,60,.4)}
 // ---- sidewalk furniture ----
 lampPost2(-330,108);lampPost2(262,108);lampPost2(-760,108);lampPost2(780,108);lampPost2(0,392);lampPost2(-520,392);lampPost2(520,392);lampPost2(-960,392);lampPost2(960,392);
 for(const [x,z,s] of [[-420,100,2],[430,100,2.1],[-600,100,1.8],[640,100,1.9],[-880,100,2],[900,100,2],[-760,440,2],[790,440,2.1],[-300,446,1.9],[320,446,2]]){tree(x,z,s);ob(x-13,z-13,x+13,z+13)}
 strand([-330,150,108],[-66,100,86],12,10,['#fff2c8','#f2c14e','#ff8a7a']);strand([66,100,86],[262,150,108],12,10,['#fff2c8','#f2c14e','#6df2c4']);
 box(8,16,8,col('#d9695f'),118,14,106);box(12,4,6,col('#d9695f'),118,16,106);box(6,4,6,col('#e88a98'),118,24,106);ob(112,100,124,112);
 box(16,24,16,col('#346a88'),-128,18,104);box(18,3,18,col('#1f4258'),-128,31,104);ob(-137,95,-119,113);
 {const d=col('#346a88'),t=lam({map:TX.mail});const m=new T.Mesh(new T.BoxGeometry(18,28,16),[d,d,col('#6fb0d0'),d,t,d]);m.position.set(-210,22,104);m.castShadow=true;scene.add(m);box(4,4,4,col('#1f4258'),-210,8,104);ob(-220,95,-200,113)}
 {const d=col('#d9695f'),t=lam({map:TX.news});const m=new T.Mesh(new T.BoxGeometry(18,26,14),[d,d,col('#f09088'),d,t,d]);m.position.set(-184,19,104);m.castShadow=true;scene.add(m);ob(-194,96,-174,112)}
 planter(-540,112,60);planter(340,112,60);planter(700,112,60);planter(-860,112,60);planter(-90,404,60);planter(90,404,60);
 trafficLight(-205,112,0);trafficLight(-320,388,Math.PI);
 {const t=lam({map:TX.st_sign}),d=col('#1f6a55');const m=new T.Mesh(new T.BoxGeometry(50,11,2),[d,d,d,d,t,t]);m.position.set(-205,104,115);scene.add(m)}
 // bus stop
 {const d=col('#221c3c'),x=545,z=100;for(const dx of [-36,36])box(3,64,3,d,x+dx,38,z-10);const gl=new T.MeshLambertMaterial({color:'#8cc8e0',transparent:true,opacity:.35});box(78,3,30,d,x,71,z-2);const bk=box(72,50,1.5,gl,x,40,z-11,{noCast:true});
  const ad=new T.Mesh(new T.BoxGeometry(2,44,26),[lam({map:TX.ad,emissiveMap:TX.ad,emissive:'#ffffff',emissiveIntensity:.5}),lam({map:TX.ad}),d,d,d,d]);ad.position.set(x+37,34,z-1);scene.add(ad);box(60,3,10,lam({map:rep('wood',3,1)}),x,20,z-4);box(3,12,3,d,x-26,13,z-4);box(3,12,3,d,x+26,13,z-4);
  box(3,90,3,d,x-56,51,z+6);const s=new T.Mesh(new T.BoxGeometry(26,14,2),[d,d,d,d,lam({map:TX.bus_sign}),lam({map:TX.bus_sign})]);s.position.set(x-56,92,z+8);scene.add(s);pool(x,z,70,40,.3,6);ob(x-40,z-14,x+40,z+2);ob(x-59,z+3,x-53,z+9)}
 // bike rack
 {const d=col('#9a94b0');for(const dx of [0,22,44]){box(2,14,2,d,150+dx,13,108);box(2,14,2,d,150+dx,13,98);box(2,2,12,d,150+dx,20,103)}ob(146,96,198,110)}
 // ---- park across the street ----
 {const hm=lam({map:rep('hedge',8,1)}),fm=new T.MeshLambertMaterial({map:rep('fence',20,1),alphaTest:.5,side:T.DoubleSide});
  for(const s of [-1,1]){const p=plane(480,24,fm,s*300,18,474);const h=box(480,20,18,lam({map:rep('hedge',20,1)}),s*300,16,488);ob(s*300-240,466,s*300+240,498)}
  for(const s of [-1,1]){box(10,44,10,lam({map:rep('stone',1,2)}),s*56,28,476);box(14,4,14,col('#c8c0e0'),s*56,52,476);box(8,8,8,bas('#fff2c8'),s*56,58,476,{noCast:true});glow(s*56,58,476,70,.6);ob(s*56-7,469,s*56+7,483)}
  {const d=col('#3a261c');const s=new T.Mesh(new T.BoxGeometry(84,18,3),[d,d,d,d,lam({map:TX.park_sign}),lam({map:TX.park_sign})]);s.position.set(0,66,476);scene.add(s);box(112,3,3,d,0,56,476)}
  plane(90,330,lam({map:rep('pave',2,7)}),0,.4,640,true);const ring=new T.Mesh(new T.RingGeometry(74,120,24),lam({map:rep('pave',6,6)}));ring.rotation.x=-Math.PI/2;ring.position.set(0,.5,690);ring.receiveShadow=true;scene.add(ring);
  cyl(76,80,16,12,lam({map:rep('stone',10,1)}),0,8,690);cyl(68,68,2,12,lam({map:rep('water',4,4),emissive:'#3f7c9c',emissiveIntensity:.35}),0,16,690);cyl(10,14,40,8,lam({map:rep('stone',2,2)}),0,28,690);cyl(26,10,6,10,lam({map:rep('stone',3,1)}),0,50,690);cyl(22,22,2,10,lam({map:rep('water',2,2),emissive:'#6fb0d0',emissiveIntensity:.4}),0,53,690);box(4,16,4,bas('#d6ecf8'),0,62,690,{noCast:true});glow(0,60,690,150,.4);pool(0,690,150,150,.3);ob(-80,612,80,768);
  for(const [x,z] of [[-150,640],[150,640],[-150,740],[150,740]]){solid('bench',1.5,22,x,z,{y:0});blob(x,z-4,40,14,.35,0);ob(x-38,z-26,x+38,z+4)}
  for(const [x,z,w,d] of [[-260,560,120,50],[260,560,120,50],[-280,800,150,50],[280,800,150,50]]){box(w,8,d,lam({map:rep('stone',Math.round(w/24),1)}),x,4,z);box(w-8,6,d-8,lam({map:rep('flowers',Math.round(w/24),2)}),x,9,z);ob(x-w/2,z-d/2,x+w/2,z+d/2)}
  for(const [x,z,s] of [[-380,620,2.3],[380,640,2.2],[-200,860,2.4],[210,870,2.2],[-420,820,2],[430,830,2.1],[-60,900,2.2],[100,910,2]]){tree(x,z,s);ob(x-13,z-13,x+13,z+13)}
  lampPost2(-110,560);lampPost2(110,560);lampPost2(-110,820);lampPost2(110,820)}
 // ---- cars ----
 car('car1',-640,162,1,0);car('car3',330,162,1,0);car('car2',-80,162,1,0);car('car2',840,162,1,0);
 car('car1',-900,240,1,120);car('car3',200,240,1,120);car('car2',600,320,-1,105);car('car1',-300,320,-1,105);car('car3',-1100,320,-1,105);
 // ---- people ----
 const looks=['judy','girl','a1','a2','a3','a4','p1','p2'];
 npc(S_STREET,'judy',1.9,[[-560,70],[820,74]],46,11);npc(S_STREET,'a1',1.9,[[900,92],[-820,88]],52,11);npc(S_STREET,'girl',1.9,[[-240,62],[-240,440],[420,440],[-240,440]],44,11);
 npc(S_STREET,'a3',1.9,[[640,430],[-700,426]],50,11);npc(S_STREET,'p1',1.9,[[-40,560],[-40,600],[-150,612],[-40,600]],36,5);npc(S_STREET,'a4',1.9,[[-360,84],[-360,84]],0,11);
}
async function lobby2(){scene=S_LOBBY;OBSC=OBS_L;
 const names=['floor','wall','wallp','wallup','door','plant','armchair','bench','sofa','desk','cart','lamp','table','stanchions','dec_wing','dec_piano','dec_aqua','dec_cat','dec_dog','dec_bird','dec_palm','dec_side','dec_books'];
 await Promise.all(names.filter(n=>!TX[n]).map(tex));scene.background=new T.Color('#0a0818');
 scene.add(new T.AmbientLight('#ffffff',.86));const sun=new T.DirectionalLight('#fff0d0',.26);sun.position.set(180,520,260);sun.target.position.set(216,0,200);sun.castShadow=true;sun.shadow.mapSize.set(2048,2048);const sc=sun.shadow.camera;sc.left=-420;sc.right=420;sc.top=420;sc.bottom=-420;sc.near=10;sc.far=1500;sun.shadow.bias=-.001;scene.add(sun);scene.add(sun.target);
 const ft=TX.floor;ft.minFilter=T.NearestFilter;const fg=new T.PlaneGeometry(432,456);const uv=fg.attributes.uv;for(let i=0;i<uv.count;i++)uv.setY(i,uv.getY(i)*(456/528));
 const fm=new T.Mesh(fg,lam({map:ft}));fm.rotation.x=-Math.PI/2;fm.position.set(216,0,228);fm.receiveShadow=true;scene.add(fm);
 const HW=112;TX.wall.minFilter=T.NearestFilter;
 {const a=plane(432,72,new T.MeshBasicMaterial({map:TX.wall}),216,36,.8);a.receiveShadow=false;const u=plane(432,40,new T.MeshBasicMaterial({map:rep('wallup',9,1)}),216,92,.8);u.receiveShadow=false}
 const wp=lam({map:rep('wallp',456/48,1)}),top=col('#1c1630'),outc=col('#2b2444');
 box(24,HW,480,[wp,wp,top,top,outc,outc],-12,HW/2,216);box(24,HW,480,[wp,wp,top,top,outc,outc],444,HW/2,216);box(480,HW,24,[outc,outc,top,top,outc,outc],216,HW/2,-12);
 box(432,5,3,col('#1c1630'),216,2.5,2.5,{noCast:true});box(436,4,6,col('#c9a24a'),216,HW+2,2,{noCast:true});
 const lt=col('#4a3f72');box(189,18,24,[outc,outc,lt,top,outc,outc],94.5,9,468);box(189,18,24,[outc,outc,lt,top,outc,outc],337.5,9,468);
 const gd=col('#c9a24a');box(5,74,6,gd,187,37,468);box(5,74,6,gd,245,37,468);box(63,6,6,gd,216,75,468);{const gl=new T.MeshLambertMaterial({color:'#8cc8e0',transparent:true,opacity:.3});const a=box(3,66,26,gl,191,34,452,{noCast:true}),b2=box(3,66,26,gl,241,34,452,{noCast:true})}
 box(54,1.5,24,col('#6e4a5a'),216,.8,468,{noCast:true});
 const sm=new T.MeshBasicMaterial({color:'#fff2c8',transparent:true,opacity:.13,blending:T.AdditiveBlending,depthWrite:false});
 for(const wx of [134,296]){const s=new T.Shape();s.moveTo(wx,0);s.lineTo(wx+44,0);s.lineTo(wx+92,-164);s.lineTo(wx-14,-164);const m=new T.Mesh(new T.ShapeGeometry(s),sm);m.rotation.x=-Math.PI/2;m.position.set(0,.5,0);scene.add(m);glow(wx+22,30,4,90,.25)}
 for(const sx of [195,289])glow(sx,54,6,70,.6);
 const M=await (await fetch('art/meta.json')).json();
 const put=(n,gx,gyBase,depth,o)=>{const m=M[n],x=gx+m.w/2,z=gyBase-72;solid(n,1,depth,x,z,Object.assign({step:2},o));blob(x,z-depth/2+2,m.w*.55,depth*.5+5,.3);if(!(o&&o.pass))ob(gx-2,z-depth-2,gx+m.w+2,z+3)};
 put('desk',188,121,30);put('plant',21,97,12);put('plant',381,217,12);put('plant',21,505,12);put('plant',381,505,12);
 put('armchair',70,337,22);put('armchair',190,337,22);put('table',119,336,22);put('sofa',237,361,24);put('cart',359,169,16);put('lamp',338,264,6);pool(350,196,70,60,.35);glow(348,44,190,90,.5);
 put('bench',120,480,18);put('bench',264,480,18);put('stanchions',167,504,4,{pass:true});
 // extra decor from the game's own catalogue
 const dec=(n,cx,z,depth)=>{const w=TX[n].image.width;solid(n,1,depth,cx,z,{step:2});blob(cx,z-depth/2+2,w*.55,depth*.5+5,.3);ob(cx-w/2-2,z-depth-2,cx+w/2+2,z+3)};
 dec('dec_piano',356,372,40);dec('dec_aqua',52,208,16);dec('dec_wing',40,150,20);dec('dec_books',50,300,14);dec('dec_bird',318,222,6);dec('dec_cat',304,330,10);dec('dec_dog',150,74,10);dec('dec_palm',408,330,10);dec('dec_side',96,150,14);
 glow(52,30,200,80,.35);pool(52,214,50,30,.3);
 npc(S_LOBBY,'a2',1,[[250,62],[250,62]],0,3);npc(S_LOBBY,'girl',1,[[150,400],[60,380],[90,250],[150,230],[60,380]],26,3);npc(S_LOBBY,'p2',1,[[330,410],[300,250],[200,180],[300,250]],24,3);
}
// ---------- game ----------
const K={x:0,z:104,face:'d',walk:0,in:false,busy:false,j:0,p:0,bike:false,lastH:'r'};const keys={};let jx=0,jz=0;
const $=id=>document.getElementById(id);
let AC;function beep(f,d,type,vol,when){try{AC=AC||new (window.AudioContext||window.webkitAudioContext)();const o=AC.createOscillator(),g=AC.createGain();o.type=type||'square';o.frequency.value=f;const t=AC.currentTime+(when||0);g.gain.setValueAtTime(vol||.05,t);g.gain.exponentialRampToValueAtTime(.0001,t+d);o.connect(g);g.connect(AC.destination);o.start(t);o.stop(t+d)}catch(e){}}
let tipT=0;function tip(s,hold){$('tip').textContent=s;$('tip').style.opacity=1;tipT=hold||2.6}
function doJump(){if(K.j>0||K.busy||K.bike)return;K.j=.001;beep(420,.12,'square',.04);beep(640,.1,'square',.03,.07)}
function doPunch(){if(K.p>0||K.busy||K.bike||K.j>0)return;K.p=.001;beep(160,.08,'sawtooth',.05)}
let ACT=null;function doAct(){if(K.busy||!ACT)return;ACT.fn()}
addEventListener('keydown',e=>{const k=e.key.toLowerCase();if(!keys[k]){if(k===' ')doJump();if(k==='f')doPunch();if(k==='e'||k==='enter')doAct()}keys[k]=1;if(e.key.startsWith('Arrow')||k===' ')e.preventDefault()});addEventListener('keyup',e=>{keys[e.key.toLowerCase()]=0});
{const joy=$('joy'),nub=$('nub');let id=null,ox=0,oy=0;
 addEventListener('touchstart',e=>{document.body.classList.add('touch');for(const t of e.changedTouches){if(t.target.closest&&t.target.closest('.btn'))continue;if(id!==null)continue;id=t.identifier;ox=t.clientX;oy=t.clientY;joy.style.display='block';joy.style.left=(ox-60)+'px';joy.style.top=(oy-60)+'px';nub.style.left='35px';nub.style.top='35px'}e.preventDefault()},{passive:false});
 addEventListener('touchmove',e=>{for(const t of e.changedTouches)if(t.identifier===id){let dx=t.clientX-ox,dy=t.clientY-oy;const m=Math.hypot(dx,dy),R=48;if(m>R){dx*=R/m;dy*=R/m}nub.style.left=(35+dx)+'px';nub.style.top=(35+dy)+'px';jx=Math.abs(dx)<7?0:dx/R;jz=Math.abs(dy)<7?0:dy/R}e.preventDefault()},{passive:false});
 const end=e=>{for(const t of e.changedTouches)if(t.identifier===id){id=null;jx=jz=0;joy.style.display='none'}};addEventListener('touchend',end);addEventListener('touchcancel',end);
 const bind=(el,fn)=>{el.addEventListener('touchstart',e=>{e.preventDefault();e.stopPropagation();el.classList.add('on');fn()},{passive:false});el.addEventListener('touchend',e=>{el.classList.remove('on')});el.addEventListener('mousedown',e=>{fn()})};
 bind($('bA'),doAct);bind($('bJ'),doJump);bind($('bP'),doPunch);
 $('bF').addEventListener('click',()=>{const d=document.documentElement;if(!document.fullscreenElement){(d.requestFullscreen||d.webkitRequestFullscreen||(()=>{})).call(d);try{screen.orientation.lock('landscape').catch(()=>{})}catch(e){}}else document.exitFullscreen()})}
function resize(){W=innerWidth;H=innerHeight;rn.setSize(W,H,false);cam.aspect=W/H;cam.updateProjectionMatrix()}addEventListener('resize',resize);
let kitS,kitL,blobS,blobL,bikeObj,hearts=[];
function mkKit(sc_,size){scene=sc_;const s=sprite('kit_di',size,0,0,0);return[s,mkBlob(sc_,11*size,5*size)]}
function swap(to){if(K.busy)return;K.busy=true;const f=$('fade');f.style.opacity=1;beep(520,.15,'triangle',.05);setTimeout(()=>{K.in=to;if(to){K.x=216;K.z=426;K.face='u'}else{K.x=0;K.z=40;K.face='d'}camInit=false;$('place').textContent=to?'THE MERIDIAN  -  LOBBY':'MERIDIAN STREET';f.style.opacity=0;setTimeout(()=>K.busy=false,250)},260)}
function heart(sc_,x,y,z){const c=document.createElement('canvas');c.width=9;c.height=8;const g=c.getContext('2d');g.fillStyle='#e2564f';[[1,0,3,1],[5,0,3,1],[0,1,9,3],[1,4,7,1],[2,5,5,1],[3,6,3,1],[4,7,1,1]].forEach(r=>g.fillRect(...r));g.fillStyle='#ffb0a8';g.fillRect(1,1,2,1);const t=new T.CanvasTexture(c);t.magFilter=T.NearestFilter;const s=new T.Sprite(new T.SpriteMaterial({map:t,transparent:true}));s.scale.set(14,12,1);s.position.set(x,y,z);sc_.add(s);hearts.push({s,t:0,sc:sc_})}
function carHit(x,z){for(const c of CARS){const p=c.G.position;if(Math.abs(x-p.x)<92&&Math.abs(z-p.z)<40)return true}return false}
const hitS=(x,z)=>OBS_S.some(o=>x>o[0]-8&&x<o[2]+8&&z>o[1]-2&&z<o[3]+6)||carHit(x,z);
const hitL=(x,z)=>OBS_L.some(o=>x>o[0]-7&&x<o[2]+7&&z>o[1]&&z<o[3]+4);
function context(){ACT=null;
 if(K.in){if(K.z>410&&Math.abs(K.x-216)<40)ACT={l:'EXIT',fn:()=>swap(false)};
  else if(Math.hypot(K.x-304,K.z-336)<34)ACT={l:'PET',fn:()=>{heart(S_LOBBY,304,34,326);beep(880,.1,'triangle',.05);beep(1100,.12,'triangle',.05,.1);tip('The cat purrs.')}};
  else if(Math.hypot(K.x-150,K.z-82)<34)ACT={l:'PET',fn:()=>{heart(S_LOBBY,150,34,72);beep(300,.08,'square',.05);beep(360,.1,'square',.05,.12);tip('Good dog.')}};
  else if(Math.abs(K.x-356)<50&&K.z>372&&K.z<400)ACT={l:'PLAY',fn:()=>{[523,659,784,1047,784,659].forEach((f,i)=>beep(f,.3,'triangle',.06,i*.16));tip('Kit plays a little tune.')}};
  else if(K.z<84&&K.x>230&&K.x<340)ACT={l:'RING',fn:()=>{beep(1568,.5,'sine',.07);beep(2093,.6,'sine',.04,.02);tip('"Welcome to The Meridian!"')}}}
 else{if(K.bike)ACT={l:'PARK',fn:()=>{K.bike=false;bikeObj.position.set(K.x+(K.lastH==='l'?-30:30),K.z>122&&K.z<378?0:6,K.z);bikeObj.visible=true;beep(300,.1,'square',.04);tip('Bike parked.')}};
  else if(bikeObj.visible&&Math.hypot(K.x-bikeObj.position.x,K.z-bikeObj.position.z)<52)ACT={l:'RIDE',fn:()=>{K.bike=true;bikeObj.visible=false;beep(600,.08,'square',.04);beep(800,.1,'square',.04,.08);tip('Ring ring! Ride anywhere on the street.')}};
  else if(Math.abs(K.x)<44&&K.z<60)ACT={l:'ENTER',fn:()=>swap(true)}}
 const b=$('bA');b.textContent=ACT?ACT.l:'';b.style.opacity=ACT?1:.25}
let camInit=false;const cp=new T.Vector3(),ct=new T.Vector3(),ctc=new T.Vector3();
let last=0,tt=0;function loop(ms){requestAnimationFrame(loop);const dt=Math.min(.05,(ms-last)/1000||0);last=ms;tt+=dt;
 let dx=(keys['d']||keys['arrowright']?1:0)-(keys['a']||keys['arrowleft']?1:0)+jx,dz=(keys['s']||keys['arrowdown']?1:0)-(keys['w']||keys['arrowup']?1:0)+jz;const m=Math.hypot(dx,dz);const moving=m>.12&&!K.busy;
 if(moving){const k=Math.min(1,m);dx/=m;dz/=m;const sp=(K.in?100:K.bike?340:175)*k;let nx=K.x+dx*sp*dt,nz=K.z+dz*sp*dt;
  if(K.in){nx=Math.max(12,Math.min(420,nx));nz=Math.max(52,Math.min(446,nz));if(hitL(nx,nz)){if(!hitL(nx,K.z))nz=K.z;else if(!hitL(K.x,nz))nx=K.x;else{nx=K.x;nz=K.z}}if(nz>442&&Math.abs(nx-216)<30)swap(false)}
  else{nx=Math.max(-1000,Math.min(1000,nx));nz=Math.max(16,nz);
   if(K.z<=464){if(nz>464&&Math.abs(nx)>46)nz=464}else{nx=Math.max(-450,Math.min(450,nx));nz=Math.min(930,nz);if(nz<=464&&Math.abs(nx)>46)nz=465}
   if(hitS(nx,nz)&&!hitS(K.x,K.z)){if(!hitS(nx,K.z))nz=K.z;else if(!hitS(K.x,nz))nx=K.x;else{nx=K.x;nz=K.z}}
   if(nz<22&&Math.abs(nx)<34){if(K.bike){nz=22;if(tipT<=0)tip('Park the bike before you go in.')}else swap(true)}}
  K.x=nx;K.z=nz;K.walk+=dt*(K.bike?14:10);K.face=Math.abs(dx)>=Math.abs(dz)*.9?(dx>0?'r':'l'):(dz>0?'d':'u');if(K.face==='r'||K.face==='l')K.lastH=K.face}
 if(K.j>0){K.j+=dt/.55;if(K.j>=1)K.j=0}if(K.p>0){K.p+=dt/.32;if(K.p>=1){K.p=0}}
 // Kit sprite
 const size=K.in?1:1.9,sp=K.in?kitL:kitS;let nm,flip=false,f=K.face;
 if(K.bike){nm='ride'+(moving?Math.floor(K.walk)%2:0);flip=K.lastH==='l'}
 else{if(f==='l'){f='r';flip=true}const u=K.j;if(u>0)nm='kit_'+f+'j'+(u<.14?0:u<.3?1:u<.68?2:u<.86?3:4);else if(K.p>0)nm='kit_'+f+'p'+(K.p<.55?0:1);else nm='kit_'+f+(moving?Math.floor(K.walk)%8:'i')}
 setChar(sp,nm,size,flip);const onRoad=!K.in&&K.z>122&&K.z<378;const gy=K.in?3:(onRoad?5:11);sp.position.set(K.x,gy+(K.j>0?Math.sin(Math.PI*K.j)*30*size:0),K.z);const bl=K.in?blobL:blobS;bl.position.set(K.x,(K.in?0:onRoad?0:6)+.5,K.z);const bs=K.j>0?1-.35*Math.sin(Math.PI*K.j):1;bl.scale.set(11*size*bs*(K.bike?1.7:1),5*size*bs,1);
 // people
 for(const n of NPCS){if((n.sc===S_LOBBY)!==K.in)continue;let mv=false;if(n.sp>0){if(n.wait>0)n.wait-=dt;else{const p=n.pts[n.i],ddx=p[0]-n.x,ddz=p[1]-n.z,d=Math.hypot(ddx,ddz);if(d<3){n.i=(n.i+1)%n.pts.length;n.wait=.4+Math.random()*2.2}else{const near=Math.hypot(K.x-n.x,K.z-n.z)<26*n.size*.6;if(!near){n.x+=ddx/d*n.sp*dt;n.z+=ddz/d*n.sp*dt;mv=true;n.walk+=dt*8}n.face=Math.abs(ddx)>=Math.abs(ddz)?(ddx>0?'r':'l'):(ddz>0?'d':'u')}}}
  else n.face=n.sc===S_LOBBY?'u':'d';
  let ff=n.face,fp=false;if(ff==='l'){ff='r';fp=true}setChar(n.s,'n_'+n.look+'_'+ff+(mv?Math.floor(n.walk)%8:'i'),n.size,fp);const road=n.sc===S_STREET&&n.z>122&&n.z<378;const y=n.sc===S_LOBBY?3:(n.z>470?5:road?5:11);n.s.position.set(n.x,y,n.z);n.b.position.set(n.x,(n.sc===S_LOBBY||road||n.z>470?0:6)+.5,n.z)}
 // cars: drive, keep distance, stop for people
 if(!K.in)for(const c of CARS){if(!c.v0)continue;const p=c.G.position;let stop=false;const ahead=(x,z,r)=>{const d=(x-p.x)*c.dir;return Math.abs(z-p.z)<52&&d>60&&d<(r||230)};
  if(K.z>118&&K.z<382&&ahead(K.x,K.z))stop=true;for(const n of NPCS)if(n.sc===S_STREET&&n.z>122&&n.z<378&&ahead(n.x,n.z))stop=true;for(const o of CARS)if(o!==c&&o.v0&&Math.abs(o.G.position.z-p.z)<10){const d=(o.G.position.x-p.x)*c.dir;if(d>0&&d<260)stop=true}
  c.v+=((stop?0:c.v0)-c.v)*Math.min(1,dt*(stop?7:2));p.x+=c.v*c.dir*dt;if(p.x>1700)p.x=-1700;if(p.x<-1700)p.x=1700}
 for(let i=hearts.length-1;i>=0;i--){const h=hearts[i];h.t+=dt;h.s.position.y+=dt*26;h.s.material.opacity=1-h.t/1.2;if(h.t>1.2){h.sc.remove(h.s);hearts.splice(i,1)}}
 if(tipT>0){tipT-=dt;if(tipT<=0)$('tip').style.opacity=0}
 context();
 const zo=K.bike?1.18:1;if(K.in){cp.set(216+(K.x-216)*.55,300,K.z+430);ct.set(216+(K.x-216)*.7,30,K.z-90)}else{cp.set(K.x+50*zo,330*zo,K.z+560*zo);ct.set(K.x,70,K.z-70)}
 if(!camInit){cam.position.copy(cp);ctc.copy(ct);camInit=true}else{const a=1-Math.pow(.002,dt);cam.position.lerp(cp,a);ctc.lerp(ct,a)}cam.lookAt(ctc);
 rn.render(K.in?S_LOBBY:S_STREET,cam)}
(async()=>{const kn=[];for(const f of ['d','u','r']){for(let i=0;i<8;i++)kn.push('kit_'+f+i);kn.push('kit_'+f+'i');for(let i=0;i<5;i++)kn.push('kit_'+f+'j'+i);kn.push('kit_'+f+'p0','kit_'+f+'p1')}
 for(const l of ['judy','girl','a1','a2','a3','a4','p1','p2'])for(const f of ['d','u','r']){for(let i=0;i<8;i++)kn.push('n_'+l+'_'+f+i);kn.push('n_'+l+'_'+f+'i')}
 await Promise.all(kn.map(tex));
 await street2();await lobby2();
 // Kit on the bike: the game's own crouch pose on top of the bike
 for(const i of [0,1]){const c=document.createElement('canvas');c.width=64;c.height=80;const g=c.getContext('2d');g.imageSmoothingEnabled=false;g.drawImage(TX['bike'+i].image,10,43);g.drawImage(TX.kit_rj2.image,-1,-9);g.drawImage(TX['bike'+i].image,0,14,44,14,10,57,44,14);const t=new T.CanvasTexture(c);t.magFilter=t.minFilter=T.NearestFilter;t.generateMipmaps=false;TX['ride'+i]=t}
 scene=S_STREET;bikeObj=solid('bike0',1.9,3,172,104,{y:6,noCast:true});
 [kitS,blobS]=mkKit(S_STREET,1.9);[kitL,blobL]=mkKit(S_LOBBY,1);
 for(const sc_ of [S_STREET,S_LOBBY])sc_.traverse(o=>{if(o.isDirectionalLight){o.shadow.autoUpdate=false;o.shadow.needsUpdate=true}});
 resize();$('load').remove();tip(('ontouchstart' in window)?'Drag to walk. Buttons on the right.':'Arrows or WASD to walk.  E = action   Space = jump   F = punch',6);window.K=K;window.DONE=true;requestAnimationFrame(loop)})().catch(e=>{window.ERR=String(e&&e.stack||e);$('load').textContent='Could not start: '+e});
