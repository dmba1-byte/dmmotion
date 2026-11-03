"""Blueprint-blue theme: post-process a walkthrough engine's HTML string."""
import re
BG1, BG2 = '#0a2a5e', '#14478f'
def theme(h):
    h = h.replace('background:#f6f4ee;overflow:hidden',
        f'background:linear-gradient(180deg,{BG1} 0%,{BG2} 52%,#0b2f69 100%);overflow:hidden')
    h = h.replace('246,244,238', '10,42,94').replace('#f6f4ee', BG1)
    # text
    h = h.replace('letter-spacing:-1.5px;color:#161616', 'letter-spacing:-1.5px;color:#ffffff')
    h = h.replace('.ln.red{color:#c0392b}.ln.grn{color:#1f9d63}', '.ln.red{color:#ff8f86}.ln.grn{color:#58e6a4}')
    h = h.replace('color:#2a5fa8;opacity:0', 'color:#9fcbff;opacity:0')
    h = h.replace('background:#fff;border:2px solid #161616', 'background:#0a2a5e;color:#e8f3ff;border:2px solid #9fcbff')
    h = h.replace('border:3px solid #161616;border-radius:14px;padding:16px 28px;box-shadow:8px 8px 0 #161616',
                  'border:3px solid #9fcbff;border-radius:14px;padding:16px 28px;box-shadow:8px 8px 0 #06193d')
    h = h.replace('letter-spacing:2px;color:#1f9d63', 'letter-spacing:2px;color:#58e6a4')
    h = h.replace('background:#161616;color:#fff;border-radius:12px', 'background:#e8f3ff;color:#0a2a5e;border-radius:12px')
    h = h.replace('color:#666;opacity:0', 'color:#9fbbe0;opacity:0').replace('color:#bbb5a4', 'color:#7fa3d6')
    h = h.replace('rgba(20,20,20,.26)', 'rgba(2,12,35,.45)')
    # strokes -> pale blueprint line
    h = h.replace("'#161616'", "'#cfe6ff'").replace('"#161616"', '"#cfe6ff"')
    h = h.replace('#e6e2d6', '#2a5fa8').replace('fill="#fcfbf8"', 'fill="#123d82"')
    # fills: neutrals -> blueprint ramp, saturated colours keep their hue
    new_col = ("function col(hex,f,dist){const n=parseInt(hex.slice(1),16);let r=(n>>16)&255,g=(n>>8)&255,b=n&255;"
      "const mx=Math.max(r,g,b),mn=Math.min(r,g,b),sat=mx?(mx-mn)/mx:0,lum=(0.3*r+0.59*g+0.11*b)/255;"
      "if(sat<0.30){const k=cl((lum-.25)/.75,0,1);r=16+k*70;g=62+k*105;b=130+k*100;}else{r*=.9;g*=.9;b*=.9;}"
      "r*=f;g*=f;b*=f;const fog=cl((dist-10)/34,0,0.5);r+=(14-r)*fog;g+=(52-g)*fog;b+=(116-b)*fog;"
      "return 'rgb('+[r,g,b].map(v=>Math.round(cl(v,0,255))).join(',')+')';}")
    h = re.sub(r"function col\(hex,f,dist\)\{.*?\n.*?return 'rgb\('.*?\}\n", new_col + "\n", h, count=1, flags=re.S)
    return h
