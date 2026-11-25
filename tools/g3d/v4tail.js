
// ================= pixel pipeline: low-res render + depth/normal outlines + gentle dither, upscaled x2 =================
const rtC=new T.WebGLRenderTarget(LW,LH),rtN=new T.WebGLRenderTarget(LW,LH),rtD=new T.WebGLRenderTarget(LW,LH),rtM=new T.WebGLRenderTarget(LW,LH);
const bC=new Uint8Array(LW*LH*4),bN=new Uint8Array(LW*LH*4),bD=new Uint8Array(LW*LH*4),bM=new Uint8Array(LW*LH*4);
const matN=new T.MeshNormalMaterial(),matD=new T.MeshDepthMaterial({depthPacking:T.RGBADepthPacking}),matK=new T.MeshBasicMaterial({color:0x000000});
const low=document.createElement('canvas');low.width=LW;low.height=LH;const lg=low.getContext('2d'),lim=lg.createImageData(LW,LH);
const BAY=[0,8,2,10,12,4,14,6,3,11,1,9,15,7,13,5];
function pass(rt,buf){rn.setRenderTarget(rt);rn.render(scene,cam);rn.readRenderTargetPixels(rt,0,0,LW,LH,buf);rn.setRenderTarget(null)}
function frame(){cam.updateProjectionMatrix();cam.updateMatrixWorld();rn.shadowMap.needsUpdate=true;pass(rtC,bC);
 const bg=scene.background,fog=scene.fog,hid=[];scene.traverse(o=>{if(!o.visible)return;const mt=o.material;if(o.isSprite||o.isLine||o.userData.fx||(mt&&!Array.isArray(mt)&&(mt.alphaTest>0||mt.transparent))){o.visible=false;hid.push(o)}});
 scene.fog=null;scene.background=new T.Color(0x8080ff);scene.overrideMaterial=matN;pass(rtN,bN);scene.background=new T.Color(0xffffff);scene.overrideMaterial=matD;pass(rtD,bD);scene.overrideMaterial=null;for(const o of hid)o.visible=true;
 // mask of the 2D characters so outlines never cut across them
 const sw=[],hid2=[];scene.traverse(o=>{if(o.isMesh&&o.visible){if(o.userData.fx){o.visible=false;hid2.push(o)}else{sw.push([o,o.material]);o.material=matK}}else if((o.isSprite&&!o.userData.chr||o.isLine)&&o.visible){o.visible=false;hid2.push(o)}});
 scene.background=new T.Color(0x000000);pass(rtM,bM);for(const [o,mt] of sw)o.material=mt;for(const o of hid2)o.visible=true;scene.background=bg;scene.fog=fog;
 const nr=cam.near,fr=cam.far,Z=i=>{const d=(bD[i+3]+bD[i+2]/256+bD[i+1]/65536+bD[i]/16777216)/256;return nr*fr/(fr-d*(fr-nr))};
 const out=lim.data;for(let y=0;y<LH;y++){const sy=LH-1-y;for(let x=0;x<LW;x++){const i=(sy*LW+x)*4,o=(y*LW+x)*4;let r=bC[i],g=bC[i+1],b=bC[i+2];
   let edge=0;if(x<LW-1&&sy>0&&!(bM[i]|bM[i+1]|bM[i+2])){const j=i+4,k=i-LW*4;if(!(bM[j]|bM[j+1]|bM[j+2])&&!(bM[k]|bM[k+1]|bM[k+2])){const z=Z(i),z1=Z(j),z2=Z(k),th=.035*Math.min(z,z1,z2)+2.2;if(Math.abs(z-z1)>th||Math.abs(z-z2)>th)edge=1;else{const d1=((bN[i]-128)*(bN[j]-128)+(bN[i+1]-128)*(bN[j+1]-128)+(bN[i+2]-128)*(bN[j+2]-128))/16129,d2=((bN[i]-128)*(bN[k]-128)+(bN[i+1]-128)*(bN[k+1]-128)+(bN[i+2]-128)*(bN[k+2]-128))/16129;if(d1<.55||d2<.55)edge=.55}}}
   if(edge){const k=edge===1?.34:.62;r=r*k+14*(1-k)*.6;g=g*k+10*(1-k)*.6;b=b*k+30*(1-k)*.6}
   const t=(BAY[(y&3)*4+(x&3)]-7.5)*.7;r=Math.round((r+t)/9)*9;g=Math.round((g+t)/9)*9;b=Math.round((b+t)/9)*9;out[o]=r;out[o+1]=g;out[o+2]=b;out[o+3]=255}}
 lg.putImageData(lim,0,0);const oc=document.getElementById('out'),g=oc.getContext('2d');g.imageSmoothingEnabled=false;g.globalAlpha=1;g.drawImage(low,0,0,W,H);
 const v=g.createRadialGradient(W/2,H/2,H*.5,W/2,H/2,H*.98);v.addColorStop(0,'rgba(16,10,36,0)');v.addColorStop(1,'rgba(16,10,36,.32)');g.fillStyle=v;g.fillRect(0,0,W,H);if(HUD&&!Q.get('nohud'))hud(g,HUD)}
// ================= asset sheets =================
async function studio(){await Promise.all(['kit_di','kit_ri'].map(tex));mkGlow();scene.background=new T.Color('#6a5f98');scene.add(new T.AmbientLight('#e8e0ff',.62));scene.add(new T.HemisphereLight('#fff0d8','#6a5f98',.35));sun(-500,700,520,'#ffe8c8',.7,700);
 const f=new T.Mesh(wuv(new T.BoxGeometry(4000,2,4000)),pm('conc','#8f86b0'));f.position.y=-1;f.receiveShadow=true;scene.add(f)}
S.furniture=async function(){await studio();sofa(-m(3.2),0,0,'#346a88',3);sofa(-m(.4),m(.2),-.35,'#7a3346',1);coffeeTable(-m(2.9),m(1.6));floorLamp(-m(5.4),-m(.2));plant(m(.9),-m(.3),1.2);plant(m(1.9),m(.2),1.3,'palm');piano(m(4.2),m(.9),-.6);luggageCart(-m(.6),m(2.3),.3);who('kit_di',m(1.6),m(2),0);
 cam.fov=30;cam.position.set(m(-.2),m(4.6),m(13.4));cam.lookAt(m(-.2),m(.8),m(.6));HUD={obj:'Modelled furniture at true scale, rendered in pixel style',tag:'ASSETS'}};
S.vehicles=async function(){await studio();car(-m(4.6),-m(.6),.3,'#d9695f','sedan');car(m(4.2),-m(.8),-.25,'#e2564f','sport');motorcycle(-m(1),m(2.4),.2,'#346a88');bicycle(m(2.6),m(2.6),-.15,'#d9695f');car(-m(.2),-m(3.6),.1,'#f4d27a','taxi');who('kit_di',m(.6),m(2.1),0);
 cam.fov=30;cam.position.set(m(.2),m(5.2),m(14.6));cam.lookAt(m(.1),m(.6),m(-.3));HUD={obj:'Cars, motorcycle and bicycle: real profiles, round wheels, clean tubes',tag:'ASSETS'}};
// ================= animated clips: step(i) renders frame i =================
const FPS=20;let STEP=null;
function walker(look,x,z,y,dir,speed){const s=who('n_'+look+'_ri',x,z,y,dir<0);return{s,look,x,z,y,dir,speed,ph:rnd(x)*8}}
function walkStep(w,dt){w.x+=w.dir*w.speed*dt;w.ph+=dt*w.speed/24*8;moveWho(w.s,w.x,w.z,w.y,'n_'+w.look+'_r'+(Math.floor(w.ph)%8),w.dir<0)}
async function clipCity(extra){SM=2048;const B=await city({noBike:true,noNear:!extra});const nm=[];for(const l of ['judy','girl','a1','a3','p1'])for(let i=0;i<8;i++)nm.push('n_'+l+'_r'+i);for(let i=0;i<8;i++)nm.push('kit_r'+i);await Promise.all(nm.map(tex));return B}
function spin(g,ang){for(const p of g.userData.wheels||[])p.rotation.z=-ang}
S.bike=async function(){await clipCity();const bz=226,g=bicycle(0,bz,0,'#d9695f',0,true),rig=rigSprite();const U2=g.userData,R=m(.33)*.88,v=118,cad=1.12;
 const cars=[[car(520,318,Math.PI,'#5a9cba','sedan'),-150],[car(-760,318,Math.PI,'#f4d27a','taxi'),-150]];car(-330,158,0,'#a88be0','sedan');car(120,158,0,'#f3ecd8','van');car(470,158,0,'#3f7c6c','suv');
 const ws=[walker('judy',-260,84,KERB,1,34),walker('a1',260,70,KERB,-1,36),walker('girl',40,96,KERB,1,30),walker('a3',-60,430,KERB,-1,34)];
 HUD={rank:'JUNIOR DESIGNER',xp:.4,cash:'1,240',obj:'Legs follow the pedals; wheels turn at road speed',tag:'CYCLING'};
 STEP=i=>{const t=i/FPS,dt=1/FPS,x=-230+v*t,th=-2*Math.PI*cad*t;g.position.set(x,0,bz+Math.sin(t*1.3)*2);g.rotation.z=Math.sin(t*2*Math.PI*cad)*.012;spin(g,v*t/R);U2.crank.rotation.z=th;for(const p of U2.crank.userData.pedals)p.rotation.z=-th;g.userData;scene.children.forEach(o=>{});
  const BB=U2.BB,CL=U2.CL,pn=[BB[0]+Math.cos(th)*CL,BB[1]+Math.sin(th)*CL],pf=[BB[0]-Math.cos(th)*CL,BB[1]-Math.sin(th)*CL],hip=[U2.saddle[0]+.5,U2.saddle[1]+1.6],lean=.5,sh=[hip[0]+Math.sin(lean)*11.5,hip[1]+Math.cos(lean)*11.5+Math.sin(th*2)*.25];
  rigSet(rig,{hip,sh,lean,footN:[pn[0]-.6,pn[1]+1.6],footF:[pf[0]-.6,pf[1]+1.6],handN:[U2.grip[0],U2.grip[1]+.6],handF:[U2.grip[0]+.4,U2.grip[1]+.4],headY:Math.sin(th*2)*.3},x,0,g.position.z,3.2);
  for(const [c,cv] of cars){c.position.x+=cv*dt;spin(c,-(c.position.x)/m(.33))}for(const w of ws)walkStep(w,dt);
  cam.fov=30;cam.position.set(x+70,138,bz+318);cam.lookAt(x+18,34,bz-34);frame()}};
S.dogwalk=async function(){await clipCity(true);const kz=884,kit=who('kit_ri',0,kz,0),df=dogFrames(),dog=new T.Sprite(new T.SpriteMaterial({map:df[0],alphaTest:.5}));dog.scale.set(30,22,1);dog.center.set(.5,0);dog.userData.chr=true;scene.add(dog);const dc=shadowCard(dog,30,22);
 const db=new T.Mesh(new T.CircleGeometry(1,16),new T.MeshBasicMaterial({color:'#0a0618',transparent:true,opacity:.3,depthWrite:false}));db.rotation.x=-Math.PI/2;db.scale.set(11,3.5,1);db.userData.fx=true;scene.add(db);
 const ws=[walker('girl',160,560,0,-1,30),walker('p1',-260,700,0,1,32),walker('a3',-120,430,KERB,1,34)];who('n_a1_di',-150-2,740,m(.2));who('n_judy_di',150+2,640,m(.2));const cars=[[car(-600,238,0,'#d9695f','sedan'),150],[car(500,318,Math.PI,'#f4d27a','taxi'),-150]];
 let leash=null;const lm=col('#d9695f');HUD={rank:'JUNIOR DESIGNER',xp:.35,cash:'1,240',obj:'Dog trots on diagonal pairs; the leash swings with each step',tag:'DOG WALK'};
 STEP=i=>{const t=i/FPS,dt=1/FPS,v=38,x=-170+v*t,ph=t*v/24*8,kf=Math.floor(ph)%8;moveWho(kit,x,kz,0,'kit_r'+kf,false);
  const lead=44+Math.sin(t*1.7)*5,dx=x+lead,dzz=kz+7+Math.sin(t*.9)*3,f=Math.floor(t*9)%4;dog.material.map=df[f];dog.position.set(dx,1+((f%2)?0:.6),dzz);dc.material.map=df[f];dc.customDepthMaterial.map=df[f];dc.position.set(dx,12,dzz);db.position.set(dx,.4,dzz);
  if(leash){scene.remove(leash);leash.geometry.dispose()}const hand=[x+6+Math.sin(ph*Math.PI/4)*2.2,22+Math.cos(ph*Math.PI/4)*.6,kz+2],colr=[dx+7,11.5+((f%2)?0:.6),dzz],sag=5+Math.sin(t*2*Math.PI*1.3)*2.2,pts=[];for(let k=0;k<=8;k++){const u=k/8;pts.push(new T.Vector3(hand[0]+(colr[0]-hand[0])*u,hand[1]+(colr[1]-hand[1])*u-Math.sin(u*Math.PI)*sag,hand[2]+(colr[2]-hand[2])*u))}
  leash=new T.Mesh(new T.TubeGeometry(new T.CatmullRomCurve3(pts),8,.9,5),lm);scene.add(leash);
  for(const [c,cv] of cars){c.position.x+=cv*dt;spin(c,c.position.x*Math.sign(cv)/m(.33))}for(const w of ws)walkStep(w,dt);
  cam.fov=30;cam.position.set(x+70,132,kz+318);cam.lookAt(x+24,30,kz-30);frame()}};
S.driving=async function(){await clipCity();const cz=240,c=car(0,cz,0,'#e2564f','sport'),rig=rigSprite(),v=290,Rw=m(.33);
 const cars=[[car(900,318,Math.PI,'#5a9cba','sedan'),-170],[car(200,318,Math.PI,'#f3ecd8','van'),-170],[car(-200,318,Math.PI,'#f4d27a','taxi'),-170]];for(const [x,cc,ty] of [[-700,'#a88be0','sedan'],[-330,'#3f7c6c','suv'],[60,'#f3ecd8','van'],[330,'#d9695f','sedan'],[640,'#5a9cba','suv']])car(x,158,0,cc,ty);
 const ws=[walker('judy',-460,84,KERB,1,34),walker('a1',-80,70,KERB,-1,36),walker('girl',240,96,KERB,1,30),walker('a3',420,430,KERB,-1,34),walker('p1',-300,438,KERB,1,32)];
 HUD={rank:'PROJECT ARCHITECT',xp:.55,next:'ASSOCIATE',cash:'18,450',obj:'Body rocks on its springs; wheels match road speed; hands steer',tag:'DRIVING'};
 STEP=i=>{const t=i/FPS,dt=1/FPS,x=-600+v*t,drift=Math.sin(t*1.25)*7,yaw=-Math.atan2(Math.cos(t*1.25)*7*1.25,v);c.position.set(x,Math.sin(t*9.5)*.35+Math.sin(t*23)*.12,cz+drift);c.rotation.set(Math.cos(t*1.25)*.012,yaw,Math.sin(t*9.5+1)*.004,'YXZ');spin(c,v*t/Rw);if(c.userData.sw)c.userData.sw.rotation.x=Math.cos(t*1.25)*.5;
  const st=Math.cos(t*1.25)*1.3,seat=new T.Vector3(m(-.36),m(.8),m(-.42)).applyEuler(c.rotation).add(c.position);
  rigSet(rig,{hip:[0,0],sh:[-2.4,11+Math.sin(t*9.5)*.2],lean:-.2,noPack:true,handN:[10.5,7.6+st],handF:[10.5,7.6-st],footN:[10,-5],footF:[11,-5],headY:Math.sin(t*9.5+.6)*.3},seat.x,seat.y,seat.z,1);
  for(const [o,cv] of cars){o.position.x+=cv*dt;spin(o,o.position.x*-1/Rw)}for(const w of ws)walkStep(w,dt);
  cam.fov=30;cam.position.set(x-40,150,cz+330);cam.lookAt(x+46,30,cz-34);frame()}};
S[V]().then(()=>{window.step=i=>{if(STEP)STEP(i);else frame();return document.getElementById('out').toDataURL('image/jpeg',.93)};if(!STEP)frame();window.DONE=true}).catch(e=>{window.ERR=String(e&&e.stack||e)});
