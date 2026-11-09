let infoRel={rx:0,ry:0};
function rotSprite(src,cx,cy,deg){const Q=4,b1=document.createElement('canvas');b1.width=W*Q;b1.height=H*Q;const g1=b1.getContext('2d');g1.imageSmoothingEnabled=false;g1.drawImage(src,0,0,W*Q,H*Q);
 const b2=document.createElement('canvas');b2.width=W*Q;b2.height=H*Q;const g2=b2.getContext('2d');g2.imageSmoothingEnabled=false;g2.translate(cx*Q,cy*Q);g2.rotate(rad(deg));g2.translate(-cx*Q,-cy*Q);g2.drawImage(b1,0,0);
 const d=g2.getImageData(0,0,W*Q,H*Q).data,out=mk(),og=out.getContext('2d'),o=og.createImageData(W,H);
 for(let y=0;y<H;y++)for(let x=0;x<W;x++){const i=((y*Q+2)*W*Q+x*Q+2)*4,j=(y*W+x)*4;if(d[i+3]>127){o.data[j]=d[i];o.data[j+1]=d[i+1];o.data[j+2]=d[i+2];o.data[j+3]=255}}
 og.putImageData(o,0,0);return out}
function render(a,frame){
 const t=(frame%32)/32,fr=(frame%32)/2;const L=mk(),g=L.getContext('2d');
 if(a.n.startsWith('4 ')){const T=A[3].f(.5,8);const tmp=mk().getContext('2d');const inf=kit(tmp,{...T,prop:null});infoRel={rx:inf.h[0][0],ry:inf.h[0][1]}}
 const P=a.f(t,fr);P.scene&&P.scene(g);
 const ch=mk(),cg=ch.getContext('2d');let inf=null;
 if(!P.hide){inf=kit(cg,P);let src=ch;
  if(P.rot)src=rotSprite(ch,Math.round(inf.hipX),Math.round(inf.hipY),P.rot);
  if(P.mask!=null&&P.mask<1){const sg=src.getContext('2d'),d=sg.getImageData(0,0,W,H);for(let y=0;y<H;y++)for(let x=0;x<W;x++)if((x+y)%2)d.data[(y*W+x)*4+3]=0;sg.putImageData(d,0,0)}
  outline(src);g.drawImage(src,0,0);}
 if(P.overlay)P.overlay(g,inf||{h:[[0,0]]});
 return L;
}
window.render=render;window.ANIMS=A;
window.draw=function(frame){
 A.slice(window.SET*10,window.SET*10+10).forEach((a,i)=>{const cx=(i%5)*384,cy=Math.floor(i/5)*540,bgc=BGS[a.bg];
  const gr=ctx.createLinearGradient(0,cy,0,cy+500);gr.addColorStop(0,bgc[0]);gr.addColorStop(.6,bgc[1]);gr.addColorStop(1,bgc[2]);ctx.fillStyle=gr;ctx.fillRect(cx,cy,384,540);
  const L=render(a,frame);ctx.imageSmoothingEnabled=false;ctx.drawImage(L,0,0,W,H,cx,cy+50,384,480);
  ctx.fillStyle='#fff';ctx.shadowColor='rgba(0,0,0,.5)';ctx.shadowBlur=4;ctx.font='bold 26px Inter, sans-serif';ctx.fillText(a.n,cx+16,cy+36);ctx.shadowBlur=0;ctx.fillStyle='rgba(255,255,255,.25)';ctx.fillRect(cx+383,cy,1,540)});
}
window.SET=0;
