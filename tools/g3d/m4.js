// v4 additions: smooth clean geometry, rebuilt piano and bicycle, spinning wheels, lit sprites, a posable Kit rig.
function wuv(geo){const p=geo.attributes.position,n=geo.attributes.normal,uv=new Float32Array(p.count*2);for(let i=0;i<p.count;i++){const ax=Math.abs(n.getX(i)),ay=Math.abs(n.getY(i)),az=Math.abs(n.getZ(i));let u,v;if(ay>=ax&&ay>=az){u=p.getX(i);v=p.getZ(i)}else if(ax>=az){u=p.getZ(i);v=p.getY(i)}else{u=p.getX(i);v=p.getY(i)}uv[i*2]=u;uv[i*2+1]=v}geo.setAttribute('uv',new T.BufferAttribute(uv,2));return geo}
function FX(o){o.userData.fx=true;return o}
// glows, light pools and contact shadows are marked so the outline pass ignores them
const _glow=glow,_pool=pool,_blob=blob;
glow=function(x,y,z,s,a,c){const before=scene.children.length;const r=_glow(x,y,z,s,a,c);FX(scene.children[scene.children.length-1]);return r};
pool=function(x,z,rx,rz,a,y){_pool(x,z,rx,rz,a,y);FX(scene.children[scene.children.length-1])};
blob=function(x,z,rx,rz,a,y){_blob(x,z,rx,rz,a,y);FX(scene.children[scene.children.length-1])};
function spokeTex(n,c){const cv=document.createElement('canvas');cv.width=cv.height=32;const g=cv.getContext('2d');g.clearRect(0,0,32,32);g.fillStyle=c;for(let i=0;i<n;i++){const a=i/n*6.283;for(let r=2;r<15;r+=.5){g.fillRect(Math.round(16+Math.cos(a)*r-.5),Math.round(16+Math.sin(a)*r-.5),2,2)}}g.beginPath();g.arc(16,16,4,0,7);g.fill();const d=g.getImageData(0,0,32,32),p=d.data;for(let i=3;i<p.length;i+=4)p[i]=p[i]>100?255:0;g.putImageData(d,0,0);const t=new T.CanvasTexture(cv);t.magFilter=t.minFilter=T.NearestFilter;return t}
let SPK5,SPK12;
function wheel(g,x,y,z,r,w){SPK5=SPK5||spokeTex(5,'#8f88a8');const p=new T.Group();p.position.set(x,y,z);g.add(p);const t=new T.Mesh(new T.CylinderGeometry(r,r,w,20),col('#17132a'));t.rotation.x=Math.PI/2;t.castShadow=true;p.add(t);const rim=new T.Mesh(new T.CylinderGeometry(r*.62,r*.62,w+.6,16),col('#3a3454'));rim.rotation.x=Math.PI/2;p.add(rim);
 for(const s of [-1,1]){const d=new T.Mesh(new T.PlaneGeometry(r*1.2,r*1.2),new T.MeshLambertMaterial({map:SPK5,alphaTest:.5,side:T.DoubleSide}));d.position.z=s*(w/2+.5);p.add(d)}(g.userData.wheels=g.userData.wheels||[]).push(p);return p}
function piano(x,z,ry){const g=G(x,z,ry),bl=lam({color:'#1d1828'}),bl2=lam({color:'#2c2640'}),br=col('#c9a24a');
 const s=new T.Shape();s.moveTo(m(-.75),0);s.lineTo(m(.75),0);s.lineTo(m(.75),m(.75));s.bezierCurveTo(m(.75),m(1.25),m(.5),m(1.35),m(.38),m(1.62));s.bezierCurveTo(m(.25),m(1.95),m(-.1),m(2.12),m(-.42),m(2.02));s.bezierCurveTo(m(-.68),m(1.94),m(-.75),m(1.7),m(-.75),m(1.4));s.lineTo(m(-.75),0);
 const mk=(d,bev)=>{const geo=new T.ExtrudeGeometry(s,{depth:d,bevelEnabled:!!bev,bevelSize:bev||0,bevelThickness:bev||0,bevelSegments:2,curveSegments:14});geo.rotateX(-Math.PI/2);return wuv(geo)};
 add(g,new T.Mesh(mk(m(.3),1),bl),0,m(.7),0);                         // case
 {const inner=new T.Mesh(mk(m(.02)),col('#b8923c'));inner.scale.set(.93,1,.95);inner.position.set(0,m(1.0),m(-.05));g.add(inner);bx(g,m(1.2),m(.03),m(.06),col('#7a5a20'),0,m(1.02),m(-.42))}
 const lg=new T.Group();lg.position.set(m(-.75),m(1.02),0);lg.rotation.z=.62;g.add(lg);const L=new T.Mesh(mk(m(.03),.6),bl2);L.position.set(m(.75),0,0);L.castShadow=true;lg.add(L);
 tube(g,[m(.55),m(1.0),m(-.75)],[m(.47),m(1.86),m(-.75)],.8,br);                         // prop stick
 bx(g,m(1.56),m(.1),m(.34),bl,0,m(.66),m(.13));bx(g,m(1.56),m(.2),m(.05),bl,0,m(.8),m(.3));    // keybed + key slip
 for(const sx of [-1,1])bx(g,m(.06),m(.34),m(.36),bl,sx*m(.75),m(.78),m(.12));
 const kc=document.createElement('canvas');kc.width=104;kc.height=10;const kg=kc.getContext('2d');kg.fillStyle='#f3ecd8';kg.fillRect(0,0,104,10);kg.fillStyle='#b0a898';for(let i=0;i<52;i++)kg.fillRect(i*2,0,1,10);kg.fillStyle='#17132a';for(let i=0;i<51;i++)if([0,1,3,4,5].includes(i%7))kg.fillRect(i*2+1,0,2,6);const kt=new T.CanvasTexture(kc);kt.magFilter=T.NearestFilter;
 add(g,new T.Mesh(new T.BoxGeometry(m(1.4),m(.03),m(.16)),[bl,bl,lam({map:kt}),bl,bl,bl]),0,m(.735),m(.2));
 bx(g,m(1.44),m(.16),m(.03),bl2,0,m(.84),m(.03));const md=bx(g,m(.62),m(.3),m(.02),bl2,0,m(1.2),m(-.12));md.rotation.x=-.25;bx(g,m(.3),m(.2),m(.01),col('#f3ecd8'),0,m(1.2),m(-.105)).rotation.x=-.25;
 for(const [lx,lz] of [[-.62,.12],[.62,.12],[-.12,-1.75]]){const leg=cy(g,m(.065),m(.04),m(.62),10,bl,m(lx),m(.39),m(lz));cy(g,m(.075),m(.075),m(.04),10,bl,m(lx),m(.68),m(lz));cy(g,m(.03),m(.03),m(.06),8,br,m(lx),m(.04),m(lz))}
 bx(g,m(.06),m(.5),m(.05),bl,m(-.09),m(.4),m(.02));bx(g,m(.06),m(.5),m(.05),bl,m(.09),m(.4),m(.02));bx(g,m(.3),m(.06),m(.1),bl,0,m(.14),m(.04));for(const px of [-.08,0,.08])bx(g,m(.035),m(.015),m(.12),br,m(px),m(.1),m(.13));
 const bn=new T.Group();bn.position.set(0,0,m(.82));g.add(bn);rb(bn,m(.9),m(.1),m(.36),3,pm('fabric','#7a3346'),0,m(.5),0);bx(bn,m(.86),m(.05),m(.32),bl,0,m(.43),0);for(const sx of [-1,1])for(const sz of [-1,1])cy(bn,m(.025),m(.018),m(.42),8,bl,sx*m(.38),m(.21),sz*m(.13));return g}
// bicycle with real proportions; kid=true sizes it for Kit. Wheels and cranks are separate so they can turn.
function bicycle(x,z,ry,c,y,kit){const g=G(x,z,ry,y||0),f=lam({color:c}),bl=col('#17132a'),ch=col('#c8c0d8');SPK12=SPK12||spokeTex(12,'#c8c0d8');const k=kit?.88:1,R=m(.33)*k,WB=m(.52)*k;g.userData.wheels=[];
 for(const wx of [-1,1]){const p=new T.Group();p.position.set(wx*WB,R,0);g.add(p);const t=new T.Mesh(new T.TorusGeometry(R-m(.025),m(.03),8,28),bl);t.castShadow=true;p.add(t);const rim=new T.Mesh(new T.TorusGeometry(R-m(.06),m(.012),6,24),ch);p.add(rim);const d=new T.Mesh(new T.PlaneGeometry((R-m(.06))*2,(R-m(.06))*2),new T.MeshLambertMaterial({map:SPK12,alphaTest:.5,side:T.DoubleSide}));p.add(d);g.userData.wheels.push(p);
  const fd=new T.Mesh(new T.TorusGeometry(R+m(.025),m(.016),5,16,Math.PI*.55),f);fd.position.set(wx*WB,R,0);fd.rotation.z=wx<0?Math.PI*.35:Math.PI*.1;g.add(fd)}
 const BB=[-WB*.12,R*.92,0],ST=[-WB*.42,R*2.42,0],HT=[WB*.62,R*2.5,0],RA=[-WB,R,0],FA=[WB,R,0],r=m(.03);g.userData.BB=BB;g.userData.saddle=[ST[0]-m(.03),ST[1]+m(.14)];g.userData.grip=[HT[0]-m(.02),HT[1]+m(.2)];
 for(const [a,b,rr] of [[BB,ST,r],[BB,HT,r*1.1],[ST,HT,r],[RA,BB,r*.8],[RA,ST,r*.75],[HT,FA,r*.9]])tube(g,a,b,rr,f).geometry=new T.CylinderGeometry(rr,rr,new T.Vector3(...a).distanceTo(new T.Vector3(...b)),10);
 tube(g,ST,[ST[0]-m(.03),ST[1]+m(.12),0],r*.7,ch);rb(g,m(.26),m(.055),m(.14),2.2,pm('fabric','#3a261c'),ST[0]-m(.05),ST[1]+m(.15),0);
 tube(g,HT,[HT[0]-m(.02),HT[1]+m(.2),0],r*.7,ch);tube(g,[HT[0]-m(.02),HT[1]+m(.2),-m(.26)],[HT[0]-m(.02),HT[1]+m(.2),m(.26)],r*.7,ch);for(const s of [-1,1])tube(g,[HT[0]-m(.02),HT[1]+m(.2),s*m(.18)],[HT[0]-m(.02),HT[1]+m(.2),s*m(.27)],r*.95,bl);
 const cr=new T.Group();cr.position.set(...BB);g.add(cr);const ring=new T.Mesh(new T.CylinderGeometry(m(.09),m(.09),m(.012),16),ch);ring.rotation.x=Math.PI/2;ring.position.z=m(.05);cr.add(ring);const CL=m(.16)*k;g.userData.CL=CL;
 for(const s of [-1,1]){const arm=new T.Mesh(new T.BoxGeometry(CL,m(.03),m(.016)),bl);arm.position.set(s*CL/2,0,s*m(.07));cr.add(arm);const pd=new T.Mesh(new T.BoxGeometry(m(.1),m(.025),m(.09)),bl);pd.position.set(s*CL,0,s*m(.12));cr.add(pd);(cr.userData.pedals=cr.userData.pedals||[]).push(pd)}g.userData.crank=cr;
 rb(g,m(.32),m(.02),m(.16),1,ch,-WB*.95,R*2.08,0);tube(g,RA,[-WB*.95-m(.1),R*2.06,0],r*.5,ch);blob(x,z,m(.9),m(.25),.35,y||0);return g}
// ---------- sprites that read as volume: baked 3-tone light + rim, and a real silhouette shadow ----------
function litCanvas(src,opt){opt=opt||{};const w=src.width,h=src.height,c=document.createElement('canvas');c.width=w;c.height=h;const g=c.getContext('2d');g.drawImage(src,0,0);const d=g.getImageData(0,0,w,h),p=d.data,A=(x,y)=>x<0||y<0||x>=w||y>=h?0:p[(y*w+x)*4+3];
 // distance to the silhouette edge, used as a rounded height field
 const dist=new Float32Array(w*h).fill(99);for(let y=0;y<h;y++)for(let x=0;x<w;x++)if(A(x,y)<128)dist[y*w+x]=0;for(let it=0;it<2;it++){for(let y=0;y<h;y++)for(let x=0;x<w;x++){const i=y*w+x;if(x>0)dist[i]=Math.min(dist[i],dist[i-1]+1);if(y>0)dist[i]=Math.min(dist[i],dist[i-w]+1)}for(let y=h-1;y>=0;y--)for(let x=w-1;x>=0;x--){const i=y*w+x;if(x<w-1)dist[i]=Math.min(dist[i],dist[i+1]+1);if(y<h-1)dist[i]=Math.min(dist[i],dist[i+w]+1)}}
 const H=(x,y)=>x<0||y<0||x>=w||y>=h?0:Math.min(4,dist[y*w+x]);const lx=opt.lx===undefined?-.62:opt.lx,ly=-.55,out=new Uint8ClampedArray(p);
 for(let y=0;y<h;y++)for(let x=0;x<w;x++){const i=(y*w+x)*4;if(p[i+3]<128)continue;const lum=p[i]+p[i+1]+p[i+2];if(lum<150)continue;const nx=H(x-1,y)-H(x+1,y),ny=H(x,y-1)-H(x,y+1),dn=nx*lx+ny*ly;let k=0;if(dn>.9)k=.16;else if(dn<-.9)k=-.2;
  const rimSide=lx<0?1:-1;if(A(x+rimSide*2,y)<128&&A(x+rimSide,y)>=128)k=.0;if(k>0){out[i]=p[i]+(255-p[i])*k;out[i+1]=p[i+1]+(250-p[i+1])*k;out[i+2]=p[i+2]+(215-p[i+2])*k}else if(k<0){out[i]=p[i]*(1+k)+40*-k;out[i+1]=p[i+1]*(1+k)+25*-k;out[i+2]=p[i+2]*(1+k)+80*-k}}
 // warm rim light on the side away from the key light
 for(let y=0;y<h;y++)for(let x=0;x<w;x++){const i=(y*w+x)*4;if(p[i+3]<128)continue;const rs=lx<0?1:-1;if(A(x+rs,y)>=128&&A(x+rs*2,y)<128&&(p[i]+p[i+1]+p[i+2])<150&&y%1===0){/* keep outline */}
  if(A(x+rs*2,y)>=128&&A(x+rs*3,y)<128&&(p[i]+p[i+1]+p[i+2])>=150){out[i]=Math.min(255,out[i]+38);out[i+1]=Math.min(255,out[i+1]+24);out[i+2]=Math.min(255,out[i+2]+6)}}
 d.data.set(out);g.putImageData(d,0,0);return c}
const LIT={};function litTex(n,flip){const k=n+(flip?'~':'');if(LIT[k])return LIT[k];let im=TX[n].image;const c=document.createElement('canvas');c.width=im.width;c.height=im.height;const g=c.getContext('2d');if(flip){g.translate(c.width,0);g.scale(-1,1)}g.drawImage(im,0,0);const t=new T.CanvasTexture(litCanvas(c));t.magFilter=t.minFilter=T.NearestFilter;t.generateMipmaps=false;return LIT[k]=t}
const SUNDIR=new T.Vector3(-700,640,560).normalize();
function shadowCard(sp,w,h){const m2=new T.MeshBasicMaterial({map:sp.material.map,alphaTest:.5,side:T.DoubleSide,colorWrite:false,depthWrite:false});const pl=new T.Mesh(new T.PlaneGeometry(w,h),m2);pl.castShadow=true;pl.customDepthMaterial=new T.MeshDepthMaterial({depthPacking:T.RGBADepthPacking,map:sp.material.map,alphaTest:.5});pl.rotation.y=Math.atan2(SUNDIR.x,SUNDIR.z);pl.userData.fx=true;scene.add(pl);sp.userData.card=pl;return pl}
function who(n,x,z,y,flip,sc){const t=litTex(n,flip);const s=new T.Sprite(new T.SpriteMaterial({map:t,alphaTest:.5}));sc=sc||1;s.scale.set(t.image.width*sc,t.image.height*sc,1);s.center.set(.5,11/80);s.position.set(x,(y||0)+1,z);s.userData.chr=true;scene.add(s);const c=shadowCard(s,t.image.width*sc,t.image.height*sc);c.position.set(x,(y||0)+1+t.image.height*sc*(.5-11/80),z);
 const b=new T.Mesh(new T.CircleGeometry(1,16),new T.MeshBasicMaterial({color:'#0a0618',transparent:true,opacity:.3,depthWrite:false}));b.rotation.x=-Math.PI/2;b.scale.set(7*sc,3*sc,1);b.position.set(x,(y||0)+.4,z);b.userData.fx=true;scene.add(b);s.userData.blob=b;return s}
function moveWho(s,x,z,y,n,flip){s.position.set(x,(y||0)+1,z);if(n){const t=litTex(n,flip);s.material.map=t;s.userData.card.material.map=t;s.userData.card.customDepthMaterial.map=t}const h=s.scale.y;s.userData.card.position.set(x,(y||0)+1+h*(.5-11/80),z);s.userData.blob.position.set(x,(y||0)+.4,z)}
// ---------- posable Kit (side view), drawn in his own palette at sprite resolution ----------
const KP={out:'#1a162e',skin:'#c98b69',skinD:'#a86f52',shirt:'#e6b84c',shirtL:'#f4d27a',shirtD:'#b88a30',pant:'#5b5f7a',pantD:'#474a5f',shoe:'#e8dcc8',shoeD:'#b5ac9c',pack:'#5c8a7a',packL:'#7fb09e'};
function capsule(d,w,h,ax,ay,bx_,by,r,c,outline){const x0=Math.floor(Math.min(ax,bx_)-r-2),x1=Math.ceil(Math.max(ax,bx_)+r+2),y0=Math.floor(Math.min(ay,by)-r-2),y1=Math.ceil(Math.max(ay,by)+r+2),C=hx(c),O=hx(KP.out),vx=bx_-ax,vy=by-ay,L=vx*vx+vy*vy||1;
 for(let y=y0;y<=y1;y++)for(let x=x0;x<=x1;x++){if(x<0||y<0||x>=w||y>=h)continue;let t=((x-ax)*vx+(y-ay)*vy)/L;t=Math.max(0,Math.min(1,t));const dd=Math.hypot(x-(ax+vx*t),y-(ay+vy*t)),i=(y*w+x)*4;if(dd<=r){d[i]=C[0];d[i+1]=C[1];d[i+2]=C[2];d[i+3]=255}else if(outline&&dd<=r+1.05&&d[i+3]<255){d[i]=O[0];d[i+1]=O[1];d[i+2]=O[2];d[i+3]=254}}}
function ik(ax,ay,bx_,by,l1,l2,bend){let dx=bx_-ax,dy=by-ay,d=Math.hypot(dx,dy);const mx=l1+l2-.01;if(d>mx){dx*=mx/d;dy*=mx/d;d=mx}const a=Math.acos(Math.max(-1,Math.min(1,(l1*l1+d*d-l2*l2)/(2*l1*d)))),base=Math.atan2(dy,dx)+bend*a;return[ax+Math.cos(base)*l1,ay+Math.sin(base)*l1]}
// pose: all points in px, x forward, y up, origin = anchor. Returns {far,near} canvases facing +x.
function rigDraw(P){const W=64,Hh=80,OX=28,OY=64,X=x=>OX+x,Y=y=>OY-y;const mk=()=>{const c=document.createElement('canvas');c.width=W;c.height=Hh;return c};const far=mk(),near=mk();
 const lay=(c,fn)=>{const g=c.getContext('2d'),im=g.getImageData(0,0,W,Hh);fn(im.data);for(let i=3;i<im.data.length;i+=4)if(im.data[i]===254)im.data[i]=255;g.putImageData(im,0,0);return g};
 const limb=(d,a,b,c2,l1,l2,bend,r,c1,cc2,foot)=>{const k=ik(a[0],a[1],b[0],b[1],l1,l2,bend);capsule(d,W,Hh,X(a[0]),Y(a[1]),X(k[0]),Y(k[1]),r,c1,true);capsule(d,W,Hh,X(k[0]),Y(k[1]),X(b[0]),Y(b[1]),r-.2,cc2,true);if(foot)capsule(d,W,Hh,X(b[0]-1),Y(b[1]-.6),X(b[0]+3.4),Y(b[1]-.6),1.5,foot,true)};
 lay(far,d=>{if(P.footF)limb(d,P.hip,P.footF,0,8.3,8.3,1,2.1,KP.pantD,KP.pantD,KP.shoeD);if(P.handF)limb(d,P.sh,P.handF,0,6.3,6.3,-1,1.5,KP.shirtD,KP.skinD)});
 const g=lay(near,d=>{const pk=[P.hip[0]+(P.sh[0]-P.hip[0])*.55-3.6*Math.cos(P.lean||0),P.hip[1]+(P.sh[1]-P.hip[1])*.55+3.6*Math.sin(P.lean||0)];if(!P.noPack){capsule(d,W,Hh,X(pk[0]),Y(pk[1]-2.5),X(pk[0]),Y(pk[1]+2.5),2.6,KP.pack,true);capsule(d,W,Hh,X(pk[0]-.6),Y(pk[1]+2.4),X(pk[0]+.4),Y(pk[1]+2.4),1.4,KP.packL,false)}
  capsule(d,W,Hh,X(P.hip[0]),Y(P.hip[1]+1),X(P.sh[0]),Y(P.sh[1]),4,KP.shirt,true);capsule(d,W,Hh,X(P.hip[0]+1.6),Y(P.hip[1]+3),X(P.sh[0]+1.6),Y(P.sh[1]-1),1.3,KP.shirtL,false);
  if(P.footN)limb(d,P.hip,P.footN,0,8.3,8.3,1,2.2,KP.pant,KP.pant,KP.shoe)});
 // head: Kit's real side-view head art
 const hd=TX.kit_ri.image;g.imageSmoothingEnabled=false;g.drawImage(hd,23,24,18,18,Math.round(X(P.sh[0])-8+(P.headX||0)),Math.round(Y(P.sh[1])-16-(P.headY||0)),18,18);
 lay(near,d=>{if(P.handN)limb(d,P.sh,P.handN,0,6.3,6.3,-1,1.6,KP.shirt,KP.skin)});
 return {far:litCanvas(far,{}),near:litCanvas(near,{}),ox:OX/W,oy:1-OY/Hh}}
function rigSprite(x,y,z){const mk=()=>{const t=new T.CanvasTexture(document.createElement('canvas'));t.magFilter=t.minFilter=T.NearestFilter;t.generateMipmaps=false;const s=new T.Sprite(new T.SpriteMaterial({map:t,alphaTest:.5}));s.scale.set(64,80,1);s.userData.chr=true;scene.add(s);return s};const o={far:mk(),near:mk(),x,y,z};return o}
function rigSet(o,P,x,y,z,dz){const r=rigDraw(P);for(const k of ['far','near']){const s=o[k];s.material.map.image=r[k];s.material.map.needsUpdate=true;s.center.set(r.ox,r.oy);s.position.set(x,y,z+(k==='far'?-(dz||3):(dz||3)))}}
// dog: four-frame trot (diagonal pairs), drawn in the game's palette
function dogFrames(){const fr=[];for(let f=0;f<4;f++){const c=document.createElement('canvas');c.width=30;c.height=22;const g=c.getContext('2d'),R=(x,y,w,h,cc)=>{g.fillStyle=cc;g.fillRect(x,y,w,h)},O='#1c1630',B='#c9905a',L='#e8b888',D='#8a5a34';const bob=(f%2)?0:1,by=6+bob;
  const leg=(x,ph,farL)=>{const s=[[2,0],[0,1],[-2,0],[0,0]][(ph)%4];const lx=x+s[0],ly=by+7,len=6-s[1];R(lx-1,ly-1,4,len+1,O);R(lx,ly,2,len-1,farL?D:B);R(lx+(s[0]>0?1:0),ly+len-2,2,1,farL?D:L)};
  leg(8,f+2,true);leg(19,f,true);                                   // far legs
  R(5,by,17,8,O);R(6,by+1,15,6,B);R(6,by+1,15,2,L);R(6,by+5,15,2,D);   // body
  R(18,by-5,9,10,O);R(19,by-4,7,8,B);R(19,by-4,7,2,L);R(25,by-1,4,5,O);R(25,by,4,3,L);R(28,by,1,1,O);R(22,by-2,1,1,O);   // head, muzzle, eye
  R(18,by-6+(f%2),4,6,O);R(19,by-5+(f%2),2,5,D);                      // ear flops
  const tw=[0,-1,0,1][f];R(1,by-3+tw,5,4,O);R(2,by-2+tw,4,2,B);R(0,by-5+tw,3,3,O);R(1,by-4+tw,1,1,L);   // tail wags
  R(17,by+3,5,2,'#d9695f');                                           // collar
  leg(9,f,false);leg(20,f+2,false);                                   // near legs
  fr.push(litCanvas(c))}return fr.map(c=>{const t=new T.CanvasTexture(c);t.magFilter=t.minFilter=T.NearestFilter;return t})}
