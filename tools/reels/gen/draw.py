import math
FONT = 'Helvetica, Arial, sans-serif'

def L(x1, y1, x2, y2, w=3, c='#1f1f1f', cap='square'):
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{c}" stroke-width="{w:.2f}" stroke-linecap="{cap}"/>'
def R(x, y, w, h, sw=2.5, fill='none', c='#1f1f1f', rx=0):
    return f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" fill="{fill}" stroke="{c}" stroke-width="{sw}"/>'
def C(x, y, r, sw=2, fill='none', c='#1f1f1f'):
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="{fill}" stroke="{c}" stroke-width="{sw}"/>'
def P(d, sw=2.5, fill='none', c='#1f1f1f'):
    return f'<path d="{d}" fill="{fill}" stroke="{c}" stroke-width="{sw}" stroke-linejoin="round"/>'
def T(x, y, s, size=22, anchor='middle', color='#1f1f1f', w=600, ls=2, rot=None):
    tr = f' transform="rotate({rot} {x:.1f} {y:.1f})"' if rot is not None else ''
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-family="{FONT}" font-size="{size:.1f}" font-weight="{w}" '
            f'letter-spacing="{ls}" text-anchor="{anchor}" fill="{color}"{tr}>{s}</text>')
def G(i, *parts): return f'<g id="{i}">' + ''.join(parts) + '</g>'
def dashed(x1, y1, x2, y2, c, dash=14, gap=10, w=2):
    n = math.hypot(x2 - x1, y2 - y1); ux, uy = (x2 - x1) / n, (y2 - y1) / n; out = []; t = 0
    while t < n:
        e = min(t + dash, n); out.append(L(x1 + ux * t, y1 + uy * t, x1 + ux * e, y1 + uy * e, w, c, 'butt')); t += dash + gap
    return ''.join(out)
def fmt_ft(v):
    ft = int(v); inch = int(round((v - ft) * 12))
    if inch == 12: ft += 1; inch = 0
    return f"{ft}'-{inch}\""
def dimH(x1, x2, y, label, c):
    return (L(x1, y, x2, y, 1.5, c) + L(x1 - 6, y + 6, x1 + 6, y - 6, 1.5, c) + L(x2 - 6, y + 6, x2 + 6, y - 6, 1.5, c)
            + L(x1, y - 12, x1, y + 12, 1.2, c) + L(x2, y - 12, x2, y + 12, 1.2, c) + T((x1 + x2) / 2, y - 10, label, 20, color=c, w=500, ls=1))
def dimV(x, y1, y2, label, c, off=-10):
    return (L(x, y1, x, y2, 1.5, c) + L(x - 6, y1 + 6, x + 6, y1 - 6, 1.5, c) + L(x - 6, y2 + 6, x + 6, y2 - 6, 1.5, c)
            + L(x - 12, y1, x + 12, y1, 1.2, c) + L(x - 12, y2, x + 12, y2, 1.2, c) + T(x + off, (y1 + y2) / 2, label, 20, color=c, w=500, ls=1, rot=-90))
