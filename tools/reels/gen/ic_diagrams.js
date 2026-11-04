/* Five ADA diagrams, each drawn as SVG markup for a 960x640 viewBox. s?(p) with p in 0..1 animates; p=1 is the finished state. */
const INK='#161616', GRN='#1f9d63', GRND='#1f6d45', RED='#b02a22', GRAY='#bfc3bb', CREAM='#f6f4ee', PAPER='#fcfbf8', WALL='#e9e6db';
const cl=(x,a,b)=>Math.max(a,Math.min(b,x)), P=(p,a,d)=>cl((p-a)/d,0,1), ss=x=>x*x*(3-2*x), lerp=(a,b,k)=>a+(b-a)*k;
const bk=x=>{const c1=1.70158,c3=c1+1,y=x-1;return 1+c3*y*y*y+c1*y*y;};
const T_=(x,y,txt,sz,col,anchor,w)=>`<text x="${x}" y="${y}" font-family="Helvetica,Arial,sans-serif" font-weight="${w||800}" font-size="${sz}" fill="${col}" text-anchor="${anchor||'middle'}">${txt}</text>`;
function pill(x,y,txt,col,op,sz){sz=sz||34; const w=txt.length*sz*.56+36, h=sz+22; return `<g opacity="${op}"><rect x="${x-w/2}" y="${y-h/2}" width="${w}" height="${h}" rx="10" fill="#fff" stroke="${col}" stroke-width="5"/>${T_(x,y+sz*.36,txt,sz,col)}</g>`;}
function dimLine(x1,y1,x2,y2,txt,col,op,lx,ly){const dx=x2-x1,dy=y2-y1,L=Math.hypot(dx,dy)||1,nx=-dy/L*14,ny=dx/L*14;
  return `<g opacity="${op}"><line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${col}" stroke-width="5"/><line x1="${x1-nx}" y1="${y1-ny}" x2="${x1+nx}" y2="${y1+ny}" stroke="${col}" stroke-width="5"/><line x1="${x2-nx}" y1="${y2-ny}" x2="${x2+nx}" y2="${y2+ny}" stroke="${col}" stroke-width="5"/></g>`+pill(lx==null?(x1+x2)/2:lx,ly==null?(y1+y2)/2:ly,txt,col,op);}
const tick=(x,y,col,op)=>`<g opacity="${op}"><circle cx="${x}" cy="${y}" r="24" fill="${col}"/><path d="M${x-11} ${y+1} l8 9 l15 -18" stroke="#fff" stroke-width="6" fill="none" stroke-linecap="round" stroke-linejoin="round"/></g>`;
const cross=(x,y,col,op)=>`<g opacity="${op}"><circle cx="${x}" cy="${y}" r="24" fill="${col}"/><path d="M${x-10} ${y-10} l20 20 M${x+10} ${y-10} l-20 20" stroke="#fff" stroke-width="6" fill="none" stroke-linecap="round"/></g>`;

// wheelchair in plan view: centre (cx,cy), width w, length h (px), rot in degrees. front of chair points "up" (-y).
function wcPlan(cx,cy,w,h,rot){return `<g transform="translate(${cx} ${cy}) rotate(${rot})">
  <rect x="${-w/2}" y="${-h/2}" width="${w}" height="${h}" rx="26" fill="#fff" stroke="${INK}" stroke-width="6"/>
  <rect x="${-w/2-10}" y="${-h*.05}" width="16" height="${h*.42}" rx="8" fill="${INK}"/><rect x="${w/2-6}" y="${-h*.05}" width="16" height="${h*.42}" rx="8" fill="${INK}"/>
  <circle cx="${-w*.32}" cy="${-h/2+22}" r="11" fill="${INK}"/><circle cx="${w*.32}" cy="${-h/2+22}" r="11" fill="${INK}"/>
  <circle cx="0" cy="${h*.12}" r="${w*.2}" fill="${GRN}" stroke="${INK}" stroke-width="5"/></g>`;}

/* 1 — reach range (elevation) */
function s1(p){const S=9.5,Y=h=>600-S*h; let o='';
  const a=ss(P(p,0,.12)), band=ss(P(p,.12,.18)), d1=ss(P(p,.28,.15)), m=ss(P(p,.52,.28)), ok=ss(P(p,.78,.12));
  o+=`<line x1="40" y1="600" x2="920" y2="600" stroke="${INK}" stroke-width="7"/>`;
  o+=`<rect x="560" y="30" width="360" height="570" fill="${WALL}" stroke="${INK}" stroke-width="6"/>`;
  o+=`<rect x="560" y="${Y(48)}" width="360" height="${Y(15)-Y(48)}" fill="${GRN}" opacity="${.24*band}"/>`;
  o+=`<line x1="560" y1="${Y(48)}" x2="920" y2="${Y(48)}" stroke="${GRN}" stroke-width="5" stroke-dasharray="14 10" opacity="${band}"/><line x1="560" y1="${Y(15)}" x2="920" y2="${Y(15)}" stroke="${GRN}" stroke-width="5" stroke-dasharray="14 10" opacity="${band}"/>`;
  // seated pictogram + wheelchair
  o+=`<g opacity="${a}"><circle cx="210" cy="${Y(12)}" r="${S*12}" fill="#fff" stroke="${INK}" stroke-width="7"/><circle cx="210" cy="${Y(12)}" r="14" fill="${INK}"/>
    <rect x="262" y="${Y(19)}" width="130" height="18" rx="6" fill="${INK}"/><rect x="262" y="${Y(40)}" width="22" height="${Y(19)-Y(40)}" rx="8" fill="${INK}"/>
    <rect x="285" y="${Y(39)}" width="64" height="${Y(19)-Y(39)}" rx="26" fill="${GRN}" stroke="${INK}" stroke-width="6"/><circle cx="316" cy="${Y(46)}" r="34" fill="#fff" stroke="${INK}" stroke-width="6"/>
    <path d="M338 ${Y(36)} L390 ${Y(22)}" stroke="${INK}" stroke-width="16" stroke-linecap="round"/></g>`;
  // dimensions at x=500
  o+=`<g opacity="${band}"><line x1="500" y1="${Y(48)}" x2="500" y2="600" stroke="${GRN}" stroke-width="5"/><line x1="486" y1="${Y(48)}" x2="514" y2="${Y(48)}" stroke="${GRN}" stroke-width="5"/><line x1="486" y1="${Y(15)}" x2="514" y2="${Y(15)}" stroke="${GRN}" stroke-width="5"/></g>`;
  o+=pill(470,Y(48),'48 in max',GRND,band,30)+pill(470,Y(15),'15 in min',GRND,band,30);
  // switch + outlet
  const sy=lerp(Y(54),Y(46),m), oy=lerp(Y(12),Y(18),m), col=m<.5?RED:GRN;
  o+=`<rect x="678" y="${sy-34}" width="44" height="68" rx="6" fill="#fff" stroke="${INK}" stroke-width="5"/><rect x="692" y="${sy-18}" width="16" height="36" rx="5" fill="${INK}"/>`;
  o+=`<rect x="778" y="${oy-30}" width="44" height="60" rx="6" fill="#fff" stroke="${INK}" stroke-width="5"/><rect x="792" y="${oy-12}" width="5" height="14" fill="${INK}"/><rect x="803" y="${oy-12}" width="5" height="14" fill="${INK}"/>`;
  const tx1=m<.5?'54 in':'46 in', tx2=m<.5?'12 in':'18 in';
  o+=pill(700,sy-64,tx1,col,d1,30)+pill(800,oy+62,tx2,col,d1,30);
  o+=cross(700,sy+60,RED,d1*(1-ok))+cross(800,oy-58,RED,d1*(1-ok))+tick(700,sy+60,GRN,ok)+tick(800,oy-58,GRN,ok);
  return o;}

/* 2 — clear floor space (plan) */
function s2(p){const S=7; let o=''; const a=ss(P(p,0,.12)), r=ss(P(p,.14,.22)), c=ss(P(p,.4,.4)), ok=ss(P(p,.82,.12));
  o+=`<rect x="140" y="40" width="680" height="30" fill="${WALL}" stroke="${INK}" stroke-width="6"/>`;
  o+=`<rect x="360" y="70" width="${30*S}" height="${20*S}" fill="#fff" stroke="${INK}" stroke-width="6" opacity="${a}"/><ellipse cx="480" cy="${70+10*S}" rx="70" ry="48" fill="none" stroke="${INK}" stroke-width="5" opacity="${a}"/>`;
  const y0=70+20*S, hh=48*S; o+=`<rect x="360" y="${y0}" width="${30*S}" height="${hh}" fill="${GRN}" opacity="${.2*r}" stroke="${GRN}" stroke-width="6" stroke-dasharray="16 10"/>`;
  o+=`<rect x="360" y="${y0}" width="${30*S}" height="${hh}" fill="none" stroke="${GRN}" stroke-width="6" stroke-dasharray="16 10" opacity="${r}"/>`;
  const wx=lerp(-160,480,ease(c)); o+=wcPlan(wx,y0+hh/2-8,26*S,42*S,0);
  o+=dimLine(320,y0,320,y0+hh,'48 in',GRND,r,248,y0+hh/2);
  o+=dimLine(360,y0+hh+22,360+30*S,y0+hh+22,'30 in',GRND,r,480,y0+hh+22);
  o+=T_(480,150,'FIXTURE',28,'#9a9a8e','middle',800);
  o+=tick(740,y0+60,GRN,ok);
  return o;}
function ease(x){return 1-Math.pow(1-x,3);}

/* 3 — turning space (plan): 48 in room fails, widens to the 60 in circle */
function s3(p){const S=5; let o=''; const a=ss(P(p,0,.1)), r=ss(P(p,.52,.1)), fail=P(p,.1,.2), grow=ss(P(p,.46,.16)), spin=P(p,.64,.26), ok=ss(P(p,.9,.08)), cx=480, cy=410, R=30*S, hw=lerp(24*S,45*S,grow);
  const rot=p<.5? 36*Math.sin(fail*Math.PI/2)*(1-0.0) : ease(spin)*360, x1=cx-hw, x2=cx+hw;
  o+=`<rect x="${x1}" y="20" width="${2*hw}" height="${120*S}" fill="${PAPER}" stroke="${INK}" stroke-width="9" opacity="${a}"/>`;
  const fx=ss(P(p,.56,.1));
  o+=`<g opacity="${fx}"><rect x="300" y="20" width="${20*S}" height="${28*S}" rx="10" fill="#fff" stroke="${INK}" stroke-width="5"/><rect x="560" y="20" width="${24*S}" height="${20*S}" rx="8" fill="#fff" stroke="${INK}" stroke-width="5"/></g>`;
  o+=`<line x1="255" y1="620" x2="400" y2="620" stroke="${PAPER}" stroke-width="12" opacity="${grow}"/>`;
  o+=`<circle cx="${cx}" cy="${cy}" r="${R}" fill="${GRN}" opacity="${.18*r}"/><circle cx="${cx}" cy="${cy}" r="${R}" fill="none" stroke="${GRN}" stroke-width="6" stroke-dasharray="16 10" opacity="${r}"/>`;
  o+=wcPlan(cx,cy,26*S,42*S,rot);
  if(p<.5){o+=pill(cx,cy+R+30,'48 in: it can not turn',RED,ss(P(p,.2,.1)),30); o+=cross(x2-34,cy-40,RED,ss(P(p,.22,.08)));}
  else o+=dimLine(cx-R,cy+R+30,cx+R,cy+R+30,'60 in',GRND,r,cx,cy+R+30)+tick(660,330,GRN,ok);
  return o;}

/* 4 — sink height (elevation) */
function s4(p){const S=9.5,Y=h=>600-S*h; let o=''; const a=ss(P(p,0,.12)), ln=ss(P(p,.14,.18)), m=ss(P(p,.5,.3)), ok=ss(P(p,.82,.12));
  const top=lerp(Y(36),Y(34),m), col=m<.5?RED:GRN, num=m<.5?'36 in':'34 in';
  o+=`<line x1="40" y1="600" x2="920" y2="600" stroke="${INK}" stroke-width="7"/>`;
  o+=`<rect x="640" y="30" width="280" height="570" fill="${WALL}" stroke="${INK}" stroke-width="6" opacity="${a}"/>`;
  o+=`<g opacity="${a}"><rect x="300" y="${top+22}" width="340" height="${600-top-22}" fill="#fff" stroke="${INK}" stroke-width="6"/><rect x="290" y="${top}" width="360" height="22" rx="4" fill="${INK}"/>
    <path d="M360 ${top} q0 34 60 34 h100 q60 0 60 -34" fill="#fff" stroke="${INK}" stroke-width="6"/><rect x="498" y="${top-58}" width="14" height="58" fill="${INK}"/><path d="M505 ${top-58} h60" stroke="${INK}" stroke-width="12" stroke-linecap="round"/></g>`;
  o+=`<line x1="160" y1="${Y(34)}" x2="640" y2="${Y(34)}" stroke="${GRN}" stroke-width="6" stroke-dasharray="16 10" opacity="${ln}"/>`;
  o+=pill(200,Y(34)-44,'34 in max',GRND,ln,32);
  o+=`<g opacity="${ln}"><line x1="130" y1="${Y(34)}" x2="130" y2="600" stroke="${GRN}" stroke-width="5"/><line x1="116" y1="${Y(34)}" x2="144" y2="${Y(34)}" stroke="${GRN}" stroke-width="5"/></g>`;
  o+=pill(700,top-6,num,col,ln,34);
  o+=cross(770,top+60,RED,ln*(1-ok))+tick(770,top+60,GRN,ok);
  return o;}

/* 5 — door clear width (plan): 28 in fails, opening widens to 32 in */
function s5(p){const S=9; let o=''; const a=ss(P(p,0,.1)), open=ss(P(p,.06,.22)), dm=ss(P(p,.3,.14)), grow=ss(P(p,.5,.2)), ok=ss(P(p,.86,.08));
  const hx=330, wy=230, wh=45, LEAF=33*S, th=16, faceX=hx+th, jr=lerp(faceX+28*S+5,638,grow), stopX=jr-5, wid=lerp(28,32,grow);
  o+=`<rect x="90" y="${wy}" width="${hx-90}" height="${wh}" fill="${WALL}" stroke="${INK}" stroke-width="6"/><rect x="${jr}" y="${wy}" width="${870-jr}" height="${wh}" fill="${WALL}" stroke="${INK}" stroke-width="6"/>`;
  o+=`<rect x="${jr-5}" y="${wy+wh-5}" width="5" height="12" fill="${INK}"/>`;
  const px=hx, py=wy+wh, col=grow<.5?RED:GRN;
  o+=`<path d="M ${px+LEAF} ${py} A ${LEAF} ${LEAF} 0 0 1 ${px} ${py+LEAF}" fill="none" stroke="${GRAY}" stroke-width="4" stroke-dasharray="10 8" opacity="${a}"/>`;
  o+=`<g transform="translate(${px} ${py}) rotate(${open*90})"><rect x="0" y="${-th}" width="${LEAF}" height="${th}" fill="#fff" stroke="${INK}" stroke-width="6"/></g>`;
  o+=`<line x1="${faceX}" y1="${py+10}" x2="${faceX}" y2="${py+130}" stroke="${col}" stroke-width="4" stroke-dasharray="8 6" opacity="${dm}"/><line x1="${stopX}" y1="${py+10}" x2="${stopX}" y2="${py+130}" stroke="${col}" stroke-width="4" stroke-dasharray="8 6" opacity="${dm}"/>`;
  o+=dimLine(faceX,py+100,stopX,py+100,Math.round(wid)+' in',col,dm,(faceX+stopX)/2,py+100);
  o+=`<rect x="${faceX}" y="${wy}" width="${stopX-faceX}" height="${wh}" fill="${col}" opacity="${.2*dm}"/>`;
  o+=cross((faceX+stopX)/2,py+190,RED,dm*(1-grow))+tick((faceX+stopX)/2,py+190,GRN,ok);
  return o;}

/* 6 — Modulor man vs wheelchair reach (elevation) */
function s6(p){const S=6.4,Y=h=>600-S*h; let o=''; const a=ss(P(p,0,.12)), ln=ss(P(p,.14,.16)), band=ss(P(p,.5,.14)), mv=ss(P(p,.6,.2)), ok=ss(P(p,.86,.08));
  o+=`<line x1="40" y1="600" x2="920" y2="600" stroke="${INK}" stroke-width="7"/><rect x="640" y="30" width="280" height="570" fill="${WALL}" stroke="${INK}" stroke-width="6"/>`;
  // Modulor man: 6 ft, arm raised to 89 in
  o+=`<g opacity="${a}" stroke="${INK}" stroke-linecap="round"><rect x="108" y="${Y(33)}" width="14" height="${600-Y(33)}" fill="${INK}"/><rect x="132" y="${Y(33)}" width="14" height="${600-Y(33)}" fill="${INK}"/><rect x="102" y="${Y(60)}" width="50" height="${Y(33)-Y(60)}" rx="14" fill="${INK}"/><circle cx="127" cy="${Y(67)}" r="24" fill="${INK}"/><path d="M142 ${Y(58)} L176 ${Y(89)}" stroke-width="16" fill="none"/></g>`;
  o+=`<line x1="176" y1="${Y(89)}" x2="640" y2="${Y(89)}" stroke="${GRAY}" stroke-width="5" stroke-dasharray="14 10" opacity="${ln}"/>`+pill(400,Y(89)+34,'Modulor man: 89 in',INK,ln,30);
  // seated user
  o+=`<g opacity="${a}"><circle cx="360" cy="${Y(12)}" r="${S*12}" fill="#fff" stroke="${INK}" stroke-width="7"/><circle cx="360" cy="${Y(12)}" r="10" fill="${INK}"/><rect x="396" y="${Y(19)}" width="96" height="14" rx="5" fill="${INK}"/><rect x="396" y="${Y(40)}" width="16" height="${Y(19)-Y(40)}" rx="6" fill="${INK}"/><rect x="412" y="${Y(39)}" width="46" height="${Y(19)-Y(39)}" rx="20" fill="${GRN}" stroke="${INK}" stroke-width="5"/><circle cx="435" cy="${Y(46)}" r="24" fill="#fff" stroke="${INK}" stroke-width="5"/><path d="M450 ${Y(36)} L ${lerp(490,600,band*0)} ${Y(30)}" stroke="${INK}" stroke-width="12" stroke-linecap="round"/></g>`;
  o+=`<rect x="640" y="${Y(48)}" width="280" height="${Y(15)-Y(48)}" fill="${GRN}" opacity="${.24*band}"/><line x1="640" y1="${Y(48)}" x2="920" y2="${Y(48)}" stroke="${GRN}" stroke-width="5" stroke-dasharray="14 10" opacity="${band}"/><line x1="640" y1="${Y(15)}" x2="920" y2="${Y(15)}" stroke="${GRN}" stroke-width="5" stroke-dasharray="14 10" opacity="${band}"/>`;
  o+=pill(780,Y(15)+44,'wheelchair: 48 in max',GRND,band,26);
  const sy=lerp(Y(60),Y(44),mv), col=mv<.5?RED:GRN;
  o+=`<rect x="760" y="${sy-30}" width="40" height="60" rx="6" fill="#fff" stroke="${INK}" stroke-width="5"/><rect x="772" y="${sy-16}" width="16" height="32" rx="5" fill="${INK}"/>`;
  o+=pill(780,sy-60,mv<.5?'60 in':'44 in',col,band,28)+cross(780,sy+56,RED,band*(1-ok))+tick(780,sy+56,GRN,ok);
  return o;}

const SCENES=[s1,s2,s3,s4,s5,s6];
const META=[{n:'REACH RANGE',r:'15 to 48 in',s:'ADA 308.2.1 and 308.3.1'},{n:'CLEAR FLOOR SPACE',r:'30 x 48 in at every fixture',s:'ADA 305.3'},{n:'TURNING SPACE',r:'60 in circle',s:'ADA 304.3.1'},{n:'SINK HEIGHT',r:'34 in max to rim or counter',s:'ADA 606.3'},{n:'DOOR WIDTH',r:'32 in clear, door open 90 degrees',s:'ADA 404.2.3'},{n:'REACH RANGE',r:'15 to 48 in',s:'ADA 308.2.1 and 308.3.1'}];
