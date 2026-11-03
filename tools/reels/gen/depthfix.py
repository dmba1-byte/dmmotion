"""Box-level depth ordering for the SVG engines (fixes objects clipping into each other / popping during the 2D->3D rise).
Faces carry bx=[x0,x1,y0,y1,z0,z1] (their box). Boxes that are separated by an axis plane are ordered exactly by which
side the camera is on; overlapping boxes fall back to far-first. Applied in-place to engine source files (idempotent)."""
import re, sys
SORT_JS = r"""
function bxOf(f){ if(f.bx) return f.bx; const mn=[1e9,1e9,1e9],mx=[-1e9,-1e9,-1e9]; for(const p of f.c) for(let k=0;k<3;k++){mn[k]=Math.min(mn[k],p[k]);mx[k]=Math.max(mx[k],p[k]);} return [mn[0],mx[0],mn[1],mx[1],mn[2],mx[2]]; }
function sortOut(out){
  const gm=new Map();
  out.forEach((o,i)=>{const f=o.f,k=f.bx?f.bx.map(v=>v.toFixed(3)).join(','):'u'+i; let g=gm.get(k); if(!g){g={b:bxOf(f),items:[],d:0};gm.set(k,g);} g.items.push(o);});
  const G=[...gm.values()], n=G.length, adj=G.map(()=>[]), indeg=new Array(n).fill(0), cam=[C.x,C.y,C.z], E=1e-4;
  for(const g of G){ g.items.sort((a,b)=>b.dist-a.dist); g.d=g.items[0].dist; }
  for(let i=0;i<n;i++)for(let j=i+1;j<n;j++){
    const a=G[i].b,b=G[j].b; let rel=0,sep=false;
    for(let ax=0;ax<3&&!rel;ax++){
      const a0=a[ax*2],a1=a[ax*2+1],b0=b[ax*2],b1=b[ax*2+1];
      if(a1<=b0+E){ sep=true; if(cam[ax]>=b0-E) rel=-1; else if(cam[ax]<=a1+E) rel=1; }
      else if(b1<=a0+E){ sep=true; if(cam[ax]>=a0-E) rel=1; else if(cam[ax]<=b1+E) rel=-1; }
    }
    if(!rel&&!sep) rel=G[i].d>=G[j].d?-1:1;
    if(rel===-1){adj[i].push(j);indeg[j]++;} else if(rel===1){adj[j].push(i);indeg[i]++;}
  }
  const done=new Array(n).fill(false), res=[];
  for(let c=0;c<n;c++){ let best=-1;
    for(let i=0;i<n;i++) if(!done[i]&&indeg[i]===0&&(best<0||G[i].d>G[best].d)) best=i;
    if(best<0) for(let i=0;i<n;i++) if(!done[i]&&(best<0||G[i].d>G[best].d)) best=i;
    done[best]=true; res.push(...G[best].items); for(const j of adj[best]) indeg[j]--; }
  return res;
}
"""
def patch(src):
    if 'function sortOut' in src: return src
    n=0
    def sub(a,b,count=1):
        nonlocal src,n
        if a in src: src=src.replace(a,b,count); n+=1
    sub("add=(n,c)=>F.push({n,c,fill,o})","add=(n,c)=>F.push({n,c,fill,o,bx:[x0,x1,y0,y1,z0,z1]})")
    sub("fill:f.fill,o:f.o}","fill:f.fill,o:f.o,bx:f.bx}",5)
    sub("out.sort((a,b)=>b.dist-a.dist);","out.splice(0,out.length,...sortOut(out));")
    # boxR: tag with its bounds
    if 'function boxR' in src:
        i=src.index('function boxR'); j=src.index('  return F;}',i)
        src=src[:j]+"  {const xs=c.map(p=>p[0]),ys=c.map(p=>p[1]),bb=[Math.min(...xs),Math.max(...xs),Math.min(...ys),Math.max(...ys),Math.min(z0,z1),Math.max(z0,z1)];F.forEach(f=>f.bx=bb);}\n"+src[j:]
        n+=1
    k=src.index('function setT'); 
    src=src[:k]+SORT_JS+src[k:]
    return src
if __name__=='__main__':
    for f in sys.argv[1:]:
        s=open(f).read(); t=patch(s)
        open(f,'w').write(t); print(f,'patched' if t!=s else 'unchanged')
