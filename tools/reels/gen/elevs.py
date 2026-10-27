"""Drafted front elevations in nine real-world house types, as layered SVG.

Drafting conventions used:
  line hierarchy  - ground 4.6, building profile 3.0, roof/trim 1.9, sash 1.3, texture 0.8
  shadows         - 45 deg sun from upper left: eave, rake, porch, window-head and jamb recesses
  glass           - light tone with two diagonal reflection strokes
  base            - exposed block foundation, stoops with treads, grade band
  entourage       - transparent deciduous tree, foundation shrubs, traced scale figures
  annotation      - level datums (F.F. / PLATE / RIDGE), overall width dim, graphic scale
"""
import random, math, json, os
import numpy as np, cv2
from .draw import L, T, G, fmt_ft

SIL = json.load(open(os.path.join(os.path.dirname(__file__), 'silhouettes.json')))
GR = -1.5  # grade, ft below finished floor


def _lum(hexc):
    h = hexc.lstrip('#'); r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    return 0.299 * r + 0.587 * g + 0.114 * b


class E:
    def __init__(s, W, Hmax, st, box=(30, 540, 1020, 800), left=13.5, right=3.5):
        bx, by, bw, bh = box
        s.S = min((bw - 120) / (W + left + right), bh / (Hmax + 5)); s.W = W; s.Hmax = Hmax
        s.X0 = bx + left * s.S + max(0, (bw - 120 - (W + left + right) * s.S) / 2); s.GY = by + bh - 70
        s.st = st; s.ink = st['ink']; s.sub = st['sub']
        dark = _lum(st['bg']) < 0.45
        s.shc, s.sho = ('#000000', 0.34) if dark else (st['ink'], 0.13)
        s.glc, s.glo = (st['ink'], 0.07) if dark else (st['ink'], 0.055)
        s.g = {k: [] for k in ('tint', 'shade', 'grade', 'walls', 'roof', 'siding', 'openings', 'details', 'ent', 'figs', 'figs2', 'dims', 'labels')}
        s.clips = []; s.levels = []; s.door_x = W / 2; s.wall_poly = None

    # ---------- primitives (ft coords, z up) ----------
    def x(s, f): return s.X0 + f * s.S
    def y(s, z): return s.GY - z * s.S
    def _d(s, pts, close=True): return 'M' + ' L'.join(f'{s.x(a):.1f} {s.y(b):.1f}' for a, b in pts) + (' Z' if close else '')
    def ln(s, grp, x1, z1, x2, z2, w=1.9, c=None, cap='butt'): s.g[grp].append(L(s.x(x1), s.y(z1), s.x(x2), s.y(z2), w, c or s.ink, cap))
    def pl(s, grp, pts, w=1.9, fill='none', close=True, c=None, fo=1):
        f = f' fill-opacity="{fo}"' if fill != 'none' and fo != 1 else ''
        s.g[grp].append(f'<path d="{s._d(pts, close)}" fill="{fill}"{f} stroke="{c or s.ink}" stroke-width="{w}" stroke-linejoin="miter" stroke-miterlimit="6"/>')
    def box(s, grp, x1, z1, x2, z2, w=1.9, fill='none', fo=1): s.pl(grp, [(x1, z1), (x2, z1), (x2, z2), (x1, z2)], w, fill, fo=fo)
    def fillp(s, grp, pts, fill, op=1):
        s.g[grp].append(f'<path d="{s._d(pts)}" fill="{fill}" fill-opacity="{op}" stroke="none"/>')
    def shade(s, pts, clip=True):
        s.fillp('shade', pts, s.shc, s.sho) if not clip or not s.wall_poly else s.g['shade'].append(
            f'<g clip-path="url(#wclip)"><path d="{s._d(pts)}" fill="{s.shc}" fill-opacity="{s.sho}"/></g>')
    def tint(s, pts, fill=None): s.fillp('tint', pts, fill or s.st['tint'])
    def clip(s, pts):
        cid = f'c{len(s.clips)}'; s.clips.append(f'<clipPath id="{cid}"><path d="{s._d(pts)}"/></clipPath>'); return cid

    # ---------- building blocks ----------
    def walls(s, pts):
        """main wall profile: tint + heavy outline; also becomes the shadow clip"""
        s.wall_poly = pts; s.tint(pts)
        s.clips.append(f'<clipPath id="wclip"><path d="{s._d(pts)}"/></clipPath>')
        s.pl('walls', pts, 3.0)

    def foundation(s, x1, x2):
        s.fillp('tint', [(x1, GR), (x2, GR), (x2, 0), (x1, 0)], s.st['tint2'])
        s.box('walls', x1, GR, x2, 0, 2.4)
        cid = s.clip([(x1, GR), (x2, GR), (x2, 0), (x1, 0)]); out = []
        for k, z in enumerate((GR + 0.67, GR + 1.34)):
            if z < -0.05: out.append(L(s.x(x1), s.y(z), s.x(x2), s.y(z), 0.8, s.sub))
        for k in range(3):
            z0, z1 = GR + k * 0.67, min(0, GR + (k + 1) * 0.67); off = (k % 2) * 0.67; v = x1 + off
            while v < x2: out.append(L(s.x(v), s.y(z0), s.x(v), s.y(z1), 0.8, s.sub)); v += 1.33
        s.g['siding'].append(f'<g clip-path="url(#{cid})">' + ''.join(out) + '</g>')

    def siding(s, region, kind='lap', step=0.6):
        cid = s.clip(region); xs = [p[0] for p in region]; zs = [p[1] for p in region]; out = []
        a, b, lo, hi = min(xs), max(xs), min(zs), max(zs)
        if kind == 'lap':
            v = lo + step
            while v < hi: out.append(L(s.x(a), s.y(v), s.x(b), s.y(v), 0.8, s.sub)); v += step
        elif kind == 'bb':  # board and batten
            v = a + step
            while v < b: out.append(L(s.x(v), s.y(lo), s.x(v), s.y(hi), 1.1, s.sub)); v += step
        elif kind == 'shingle':
            v, k = lo + step, 0
            while v < hi:
                out.append(L(s.x(a), s.y(v), s.x(b), s.y(v), 0.8, s.sub)); u = a + (k % 2) * 0.45
                while u < b: out.append(L(s.x(u), s.y(v - step), s.x(u), s.y(v), 0.6, s.sub)); u += 0.9 + (int(u * 7) % 3) * 0.15
                v += step; k += 1
        elif kind == 'stone':
            r = random.Random(7); v = lo
            while v < hi:
                hh = r.choice((0.55, 0.7, 0.85)); out.append(L(s.x(a), s.y(v), s.x(b), s.y(v), 0.8, s.sub)); u = a + r.random() * 1.2
                while u < b: out.append(L(s.x(u), s.y(v), s.x(u), s.y(min(hi, v + hh)), 0.8, s.sub)); u += r.uniform(1.1, 2.4)
                v += hh
        elif kind == 'seam':
            v = a + step
            while v < b: out.append(L(s.x(v), s.y(lo), s.x(v), s.y(hi), 0.9, s.sub)); v += step
        s.g['siding'].append(f'<g clip-path="url(#{cid})">' + ''.join(out) + '</g>')

    def glass(s, x1, z1, x2, z2, refl=True):
        s.fillp('tint', [(x1, z1), (x2, z1), (x2, z2), (x1, z2)], s.glc, s.glo * 2.2)
        if refl and (x2 - x1) > 1.2 and (z2 - z1) > 1.6:
            w, h = x2 - x1, z2 - z1; k = min(w, h)
            for f, ln_ in ((0.18, 0.5), (0.34, 0.28)):
                ax, az = x1 + w * f, z2 - h * 0.12; s.ln('openings', ax, az, ax + k * ln_ * 0.7, az - k * ln_ * 0.7, 0.8, s.sub)

    def window(s, x1, z1, x2, z2, cols=2, rows=2, trim=0.33, shutters=False, head=True, sill=True, d=0.35):
        t = trim
        s.glass(x1, z1, x2, z2)
        s.shade([(x1, z2), (x2, z2), (x2, z2 - d), (x1 + d, z2 - d), (x1 + d, z1), (x1, z1)], clip=False)
        if t: s.box('openings', x1 - t, z1, x2 + t, z2 + t, 1.9)
        s.box('openings', x1, z1, x2, z2, 1.3)
        for i in range(1, cols): xx = x1 + (x2 - x1) * i / cols; s.ln('openings', xx, z1, xx, z2, 1.1)
        for j in range(1, rows): zz = z1 + (z2 - z1) * j / rows; s.ln('openings', x1, zz, x2, zz, 1.1)
        if head and t: s.box('openings', x1 - t - 0.18, z2 + t, x2 + t + 0.18, z2 + t + 0.28, 1.6); s.shade([(x1 - t, z2 + t), (x2 + t + 0.18, z2 + t), (x2 + t + 0.46, z2 + t - 0.28), (x1 - t + 0.28, z2 + t - 0.28)])
        if sill: s.box('openings', x1 - t - 0.25, z1 - 0.28, x2 + t + 0.25, z1, 1.6); s.shade([(x1 - t, z1 - 0.28), (x2 + t + 0.25, z1 - 0.28), (x2 + t + 0.5, z1 - 0.55), (x1 - t + 0.25, z1 - 0.55)])
        if shutters:
            sw = (x2 - x1) / max(2, cols) * 0.95
            for a in (x1 - t - 0.15 - sw, x2 + t + 0.15):
                s.box('details', a, z1, a + sw, z2 + t, 1.4, s.st['tint2'])
                zz = z1 + 0.35
                while zz < z2 + t - 0.2: s.ln('details', a + 0.15, zz, a + sw - 0.15, zz, 0.7, s.sub); zz += 0.3

    def door(s, xc, w=3, h=6.9, kind='panel', stoop=True, side=0.0, transom=False):
        s.door_x = xc; x1, x2 = xc - w / 2, xc + w / 2; t = 0.4
        s.fillp('tint', [(x1, 0), (x2, 0), (x2, h), (x1, h)], s.st['tint2'])
        s.shade([(x1, h), (x2, h), (x2, h - 0.5), (x1 + 0.5, h - 0.5), (x1 + 0.5, 0), (x1, 0)], clip=False)
        s.box('openings', x1, 0, x2, h, 1.6)
        if kind == 'panel':
            for (a, b) in ((0.6, 3.0), (3.6, h - 0.5)):
                s.box('openings', x1 + 0.45, a, xc - 0.2, b, 0.9); s.box('openings', xc + 0.2, a, x2 - 0.45, b, 0.9)
        elif kind == 'glass':
            s.glass(x1 + 0.45, 0.6, x2 - 0.45, h - 0.5); s.box('openings', x1 + 0.45, 0.6, x2 - 0.45, h - 0.5, 1.0)
        elif kind == 'craft':
            s.glass(x1 + 0.4, h - 2.3, x2 - 0.4, h - 0.45, refl=False); s.box('openings', x1 + 0.4, h - 2.3, x2 - 0.4, h - 0.45, 1.0)
            for k in (1, 2): xx = x1 + 0.4 + (w - 0.8) * k / 3; s.ln('openings', xx, h - 2.3, xx, h - 0.45, 0.8)
            for k in range(3): xx = x1 + 0.5 + k * (w - 1.0) / 3; s.box('openings', xx + 0.08, 0.6, xx + (w - 1.0) / 3 - 0.08, h - 2.8, 0.8)
        elif kind == 'slab':
            s.ln('openings', x1 + 0.5, 3.2, x1 + 0.5, 4.6, 2.2, cap='round')
        if kind != 'slab': s.g['openings'].append(f'<circle cx="{s.x(x2 - 0.42):.1f}" cy="{s.y(3.2):.1f}" r="{max(2.2, 0.12 * s.S):.1f}" fill="{s.ink}"/>')
        s.box('openings', x1 - t, 0, x2 + t, h + t, 1.9)
        if side:
            for a in (x1 - t - side, x2 + t):
                s.glass(a + 0.15, 1.0, a + side - 0.15, h - 0.3, refl=False); s.box('openings', a, 0, a + side, h + t, 1.4); s.box('openings', a + 0.15, 1.0, a + side - 0.15, h - 0.3, 0.9)
        if transom:
            a, b = x1 - t - side, x2 + t + side
            s.glass(a + 0.15, h + t + 0.15, b - 0.15, h + t + 1.3, refl=False); s.box('openings', a, h + t, b, h + t + 1.45, 1.6)
            for k in range(1, 5): s.ln('openings', a + (b - a) * k / 5, h + t + 0.15, a + (b - a) * k / 5, h + t + 1.3, 0.8)
        if stoop:
            sw = w / 2 + t + side + 1.2
            s.fillp('tint', [(xc - sw, GR), (xc + sw, GR), (xc + sw, 0), (xc - sw, 0)], s.st['tint2'])
            s.box('details', xc - sw, -0.75, xc + sw, 0, 1.9); s.box('details', xc - sw - 0.9, GR, xc + sw + 0.9, -0.75, 1.9)

    def rake(s, a, over=1.2, th=0.75, fascia=True):
        """roof edge band along the polyline a-b-...(ridge profile), drawn as thick band with soffit shadow"""
        pts = a
        up = [(px, pz + th) for px, pz in pts]
        s.pl('roof', up + pts[::-1], 1.9, s.st['tint2'])
        s.pl('roof', up, 2.6, close=False)
        sh = [(px + over * 0.6, pz - over) for px, pz in pts]
        s.shade(pts + sh[::-1])

    def eave_shadow(s, x1, x2, z, depth):
        s.shade([(x1, z), (x2, z), (x2 + depth, z - depth), (x1 + depth, z - depth)])

    def vent(s, xc, zc, r=1.1):
        pts = [(xc - r, zc - r * 0.55), (xc, zc + r * 0.55), (xc + r, zc - r * 0.55)]
        s.pl('details', pts, 1.6, s.st['tint2'])
        for k in range(1, 4):
            zz = zc - r * 0.55 + k * r * 0.27; hw = r * (1 - (zz - (zc - r * 0.55)) / (r * 1.1))
            s.ln('details', xc - hw + 0.1, zz, xc + hw - 0.1, zz, 0.8, s.sub)

    def chimney(s, x1, x2, zbase, ztop):
        s.fillp('tint', [(x1, zbase), (x2, zbase), (x2, ztop), (x1, ztop)], s.st['tint2'])
        s.box('details', x1, zbase, x2, ztop, 2.2); s.box('details', x1 - 0.25, ztop, x2 + 0.25, ztop + 0.45, 1.8)
        z = zbase + 0.45
        while z < ztop - 0.1:
            s.ln('siding', x1, z, x2, z, 0.7, s.sub); z += 0.45
        s.shade([(x1, ztop), (x1 + 0.5, ztop), (x1 + 0.5, zbase), (x1, zbase)], clip=False)

    # ---------- entourage ----------
    def _blob(s, cx, cz, rx, rz, seed, n=14, rmin=0.32, rmax=0.5, flat=False):
        r = random.Random(seed); K = 12
        Wd, Hd = int((rx * 2 + 4) * K), int((rz * 2 + 4) * K); img = np.zeros((Hd, Wd), np.uint8)
        for i in range(n):
            a = r.uniform(0, 2 * math.pi); d = math.sqrt(r.uniform(0, 1)) * 0.72
            px, pz = math.cos(a) * d * rx, math.sin(a) * d * rz; rr = r.uniform(rmin, rmax) * min(rx, rz)
            cv2.circle(img, (int((px + rx + 2) * K), int((-pz + rz + 2) * K)), int(rr * K), 255, -1)
        img = cv2.GaussianBlur(img, (0, 0), K * 0.08); cs, _ = cv2.findContours((img > 127).astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        c = max(cs, key=cv2.contourArea); ap = cv2.approxPolyDP(c, K * 0.05, True)[:, 0, :].astype(float)
        pts = [(cx + p[0] / K - rx - 2, cz - (p[1] / K - rz - 2)) for p in ap]
        for _ in range(2):  # Chaikin smoothing
            q = []
            for i in range(len(pts)):
                (x1, z1), (x2, z2) = pts[i], pts[(i + 1) % len(pts)]
                q += [(0.75 * x1 + 0.25 * x2, 0.75 * z1 + 0.25 * z2), (0.25 * x1 + 0.75 * x2, 0.25 * z1 + 0.75 * z2)]
            pts = q
        return pts

    def tree(s, xc, h, seed):
        r = random.Random(seed); cw = h * r.uniform(0.27, 0.31); cz = h - cw * 1.05
        can = s._blob(xc, cz, cw, cw * 1.08, seed, n=34, rmin=0.2, rmax=0.34)
        s.pl('ent', can, 1.3, s.ink, fo=0.04)
        # interior canopy texture: a few small scallops on the shaded (right/lower) side
        for k in range(7):
            a = r.uniform(-1.2, 0.4); d = r.uniform(0.35, 0.8); ax, az = xc + math.cos(a) * d * cw, cz + math.sin(a) * d * cw; rr = cw * r.uniform(0.1, 0.16)
            s.g['ent'].append(f'<path d="M{s.x(ax - rr):.1f} {s.y(az):.1f} A{rr * s.S:.1f} {rr * s.S:.1f} 0 0 0 {s.x(ax + rr):.1f} {s.y(az):.1f}" fill="none" stroke="{s.sub}" stroke-width="0.8"/>')
        tw = 0.3 + h * 0.01; fork = cz - cw * 0.35
        s.pl('ent', [(xc - tw, GR), (xc - tw * 0.55, fork), (xc - cw * 0.42, cz + cw * 0.3)], 1.4, close=False)
        s.pl('ent', [(xc + tw, GR), (xc + tw * 0.55, fork), (xc + cw * 0.38, cz + cw * 0.5)], 1.4, close=False)
        s.pl('ent', [(xc - tw * 0.2, fork + 0.3), (xc + r.uniform(-0.15, 0.15) * cw, cz + cw * 0.75)], 1.1, close=False)
        s.pl('ent', [(xc - tw * 0.4, cz - cw * 0.05), (xc - cw * 0.5, cz + cw * 0.42)], 0.9, close=False)
        s.pl('ent', [(xc + tw * 0.4, cz + cw * 0.1), (xc + cw * 0.48, cz + cw * 0.62)], 0.9, close=False)
        s.g['ent'].append(L(s.x(xc - cw * 0.7), s.y(GR), s.x(xc + cw * 0.9), s.y(GR), 0.01, s.ink))

    def shrub(s, xc, w, h, seed):
        w, h = w * 1.25, h * 1.15
        pts = s._blob(xc, GR + h * 0.5, w / 2, h / 2, seed, n=16, rmin=0.3, rmax=0.5)
        pts = [(px, max(GR, pz)) for px, pz in pts]
        s.pl('ent', pts, 1.3, s.st['bg'])
        r = random.Random(seed)
        for k in range(3):
            ax = xc + r.uniform(-0.3, 0.3) * w; az = GR + h * r.uniform(0.35, 0.6); rr = w * 0.12
            s.g['ent'].append(f'<path d="M{s.x(ax - rr):.1f} {s.y(az):.1f} A{rr * s.S:.1f} {rr * s.S:.1f} 0 0 0 {s.x(ax + rr):.1f} {s.y(az):.1f}" fill="none" stroke="{s.sub}" stroke-width="0.8"/>')

    def fig(s, name, xf, zf=GR, flip=False, grp='figs', scale=1.0):
        d = SIL[name]['d']; sx = -s.S * scale if flip else s.S * scale
        s.g[grp].append(f'<g transform="translate({s.x(xf):.1f} {s.y(zf):.1f}) scale({sx:.3f} {s.S * scale:.3f})"><path d="{d}" fill="{s.ink}" fill-opacity="0.9" fill-rule="evenodd"/></g>')

    # ---------- annotation ----------
    def level(s, z, name):
        s.levels.append((z, name))

    def finish(s, title, subtitle, figs_spec=None, trees=('L',), shrubs=()):
        W = s.W
        # ground
        s.fillp('grade', [(-9, GR), (W + 5, GR), (W + 5, GR - 0.7), (-9, GR - 0.7)], s.ink, 0.06)
        s.g['grade'].append(L(s.x(-9), s.y(GR), s.x(W + 5.5), s.y(GR), 4.6, s.ink, 'butt'))
        r = random.Random(int(W * 31))
        th = max(15, min(s.Hmax * 0.8, 21)) + r.uniform(-1, 1)
        if 'L' in trees: s.tree(-1.0 - th * 0.3, th, int(W * 7))
        for k, (xc, w) in enumerate(shrubs): s.shrub(xc, w, r.uniform(1.6, 2.4), int(W * 13 + k))
        for spec in (figs_spec or []): s.fig(*spec)
        # levels
        mx = W + 2.6
        for z, name in [(0, 'F.F.')] + s.levels:
            yy = s.y(z); s.g['dims'].append(f'<line x1="{s.x(W + 0.6):.1f}" y1="{yy:.1f}" x2="{s.x(mx) - 9:.1f}" y2="{yy:.1f}" stroke="{s.sub}" stroke-width="1" stroke-dasharray="7 5"/>')
            cx, rr = s.x(mx), 9
            s.g['dims'].append(f'<circle cx="{cx:.1f}" cy="{yy:.1f}" r="{rr}" fill="none" stroke="{s.ink}" stroke-width="1.4"/>'
                               f'<path d="M{cx:.1f} {yy - rr:.1f} A{rr} {rr} 0 0 1 {cx + rr:.1f} {yy:.1f} L{cx:.1f} {yy:.1f} Z M{cx:.1f} {yy + rr:.1f} A{rr} {rr} 0 0 1 {cx - rr:.1f} {yy:.1f} L{cx:.1f} {yy:.1f} Z" fill="{s.ink}"/>')
            s.g['dims'].append(T(cx + 16, yy - 5, name, 15, 'start', s.ink, 700, 1.5))
            s.g['dims'].append(T(cx + 16, yy + 15, '+' + fmt_ft(z) if z > 0 else "&#177;0'-0\"", 14, 'start', s.sub, 500, 1))
        # overall width dim
        yd = s.y(GR) + 46; x1, x2 = s.x(0), s.x(W); c = s.sub
        s.g['dims'].append(L(x1 - 14, yd, x2 + 14, yd, 1.1, c) + L(x1, s.y(GR) + 12, x1, yd + 10, 1, c) + L(x2, s.y(GR) + 12, x2, yd + 10, 1, c)
                           + L(x1 - 6, yd + 6, x1 + 6, yd - 6, 2, s.ink) + L(x2 - 6, yd + 6, x2 + 6, yd - 6, 2, s.ink) + T((x1 + x2) / 2, yd - 9, fmt_ft(W), 18, color=s.ink, w=500, ls=1))
        # title block + graphic scale
        ty = s.y(GR) + 112
        s.g['labels'] += [T(s.x(-8), ty, title, 26, 'start', s.ink, 700, 4), T(s.x(-8), ty + 30, subtitle, 16, 'start', s.sub, 500, 1.5)]
        sx0, sy = s.x(-8), ty + 58; seg = 4 * s.S
        sc = [f'<rect x="{sx0 + i * seg:.1f}" y="{sy:.1f}" width="{seg:.1f}" height="6" fill="{s.ink if i % 2 == 0 else "none"}" stroke="{s.ink}" stroke-width="1"/>' for i in range(4)]
        sc += [T(sx0 + i * seg, sy + 24, str(i * 4) + ("'" if i == 4 else ''), 12, 'middle', s.sub, 500, 0.5) for i in (0, 1, 2, 4)]
        s.g['labels'] += sc
        defs = '<defs>' + ''.join(s.clips) + '</defs>'
        order = ['grade', 'walls', 'roof', 'openings', 'details', 'siding', 'ent', 'dims', 'labels']
        return defs + G('tint', *s.g['tint']) + ''.join(G(k, *s.g[k]) for k in ['grade', 'walls', 'roof', 'siding', 'openings', 'details']) \
            + G('shade', *s.g['shade']) + G('ent', *s.g['ent']) + G('figs', *s.g['figs']) + G('figs2', *s.g['figs2']) + G('dims', *s.g['dims']) + G('labels', *s.g['labels']), order


# ====================== house types ======================

def a_frame(st, r):
    W = r.choice([26, 28]); Hh = W * 0.92; m = W / 2; e = E(W + 2, Hh + 2, st)
    e.X0 += e.S  # A-frame legs extend 1 ft past walls
    slope = Hh / m; inner = lambda xx: (xx, (m - abs(xx - m)) * slope - 0.9)
    gable = [(0.6, 0), (W - 0.6, 0), (m, Hh - 1.6)]
    e.walls([(0.6, 0), (W - 0.6, 0), (m, Hh - 1.6)])
    gl = [(m - W * 0.33, 0.4), (m + W * 0.33, 0.4), (m, 0.4 + W * 0.33 * slope * 0.95)]
    e.fillp('tint', gl, e.glc, e.glo * 2.2); e.pl('openings', gl, 1.9)
    top = gl[2][1]
    for k in (-0.5, 0.5):
        xx = m + k * W * 0.33; zt = 0.4 + (W * 0.33 - abs(k * W * 0.33)) * slope * 0.95; e.ln('openings', xx, 0.4, xx, zt, 1.1)
    for zz in (7.6, 14.5):
        if zz < top - 1.2:
            half = W * 0.33 * (1 - (zz - 0.4) / (top - 0.4)); e.ln('openings', m - half, zz, m + half, zz, 1.1)
    for f, l_ in ((0.42, 3.2), (0.5, 2.0)):
        ax = m - W * 0.18; az = top * f + 2; e.ln('openings', ax, az, ax + l_, az - l_, 0.8, e.sub)
    e.door(m, 3.2, 7.2, 'glass', stoop=False)
    # roof legs
    outer = [(-1.0, -0.2), (m, Hh + 0.9), (W + 1.0, -0.2)]
    e.pl('roof', [(-1.0, -0.2), (m, Hh + 0.9), (W + 1.0, -0.2), (W - 0.2, -0.2), (m, Hh - 0.6), (0.2, -0.2)], 2.8, e.st['tint2'])
    e.ln('roof', -0.6, 0.1, m, Hh + 0.45, 0.9, e.sub); e.ln('roof', m, Hh + 0.45, W + 0.6, 0.1, 0.9, e.sub)
    e.shade([(0.2, -0.2), (m, Hh - 0.6), (m + 1.2, Hh - 1.8), (1.4, -0.2)])
    # flue on right slope
    fx = m + W * 0.17; fz = (m - (fx - m)) * slope + 0.9
    e.box('details', fx - 0.35, fz - 0.6, fx + 0.35, fz + 3.6, 1.6, e.st['tint2']); e.pl('details', [(fx - 0.75, fz + 3.6), (fx, fz + 4.3), (fx + 0.75, fz + 3.6)], 1.6, e.st['tint2'])
    # deck with railing in front of glass
    e.foundation(-1.5, W + 1.5)
    e.box('details', -1.5, -0.25, W + 1.5, 0.15, 1.9, e.st['tint2'])
    e.ln('details', -1.5, 3.2, m - 4, 3.2, 2.2); e.ln('details', m + 4, 3.2, W + 1.5, 3.2, 2.2)
    for xx in [-1.5 + k * 0.45 for k in range(int((W + 3) / 0.45) + 1)]:
        if not (m - 4 < xx < m + 4): e.ln('details', xx, 0.15, xx, 3.2, 0.7, e.sub)
    for xx in (-1.5, m - 4, m + 4, W + 1.5): e.box('details', xx - 0.22, 0.15, xx + 0.22, 3.5, 1.4, e.st['bg'])
    e.box('details', m - 3.2, -0.75, m + 3.2, -0.25, 1.6); e.box('details', m - 3.6, GR, m + 3.6, -0.75, 1.6)
    e.level(Hh + 0.9, 'RIDGE')
    return e.finish('FRONT ELEVATION', 'A-FRAME CABIN · FULL-HEIGHT GLASS GABLE · TIMBER DECK',
                    [('man_dog', m - 8.5, GR, False), ('woman_stand', m + 6.3, 0.15, True, 'figs2'), ('kid_b', m + 8.2, 0.15, True, 'figs2')],
                    shrubs=[(W + 3.2, 3.2)]), 'A-frame cabin'


def butterfly(st, r):
    W = r.choice([46, 50]); lo, hi = 10.4, 13.4; mid = W * 0.55; e = E(W, hi + 2, st)
    prof = [(0, 0), (W, 0), (W, hi - 0.6), (mid, lo - 0.6), (0, hi - 0.6)]
    e.walls(prof)
    zs = lo - 0.6 + (W * 0.62 - mid) * (hi - lo) / (W - mid)
    e.siding([(0, 0), (W * 0.62, 0), (W * 0.62, zs), (mid, lo - 0.6), (0, hi - 0.6)], 'bb', 0.9)
    e.fillp('tint', [(W * 0.62, 0), (W, 0), (W, hi - 0.6), (W * 0.62, zs)], e.st['tint2'])
    e.siding([(W * 0.62, 0), (W, 0), (W, hi - 0.6), (mid, lo - 0.6)], 'stone')
    e.ln('walls', W * 0.62, 0, W * 0.62, lo - 0.6 + (W * 0.62 - mid) * (hi - lo) / (W - mid), 2.2)
    # roof
    e.pl('roof', [(-3, hi), (mid, lo), (W + 3, hi), (W + 3, hi + 0.85), (mid, lo + 0.85), (-3, hi + 0.85)], 2.2, e.st['tint2'])
    e.ln('roof', -3, hi + 0.85, mid, lo + 0.85, 2.8); e.ln('roof', mid, lo + 0.85, W + 3, hi + 0.85, 2.8)
    e.shade([(0, hi - 0.6 + 0.2), (mid, lo - 0.6 + 0.2), (W, hi - 0.4), (W, hi - 3.2), (mid + 2.6, lo - 3.4), (0, hi - 3.2)])
    # clerestory band following the roof
    for a, b in ((1.5, mid - 2.5), (mid + 1.5, W * 0.62 - 1)):
        za = lo - 0.6 + abs(mid - a) * (hi - lo) / (mid if a < mid else W - mid) - 0.6
        zb = lo - 0.6 + abs(mid - b) * (hi - lo) / (mid if b < mid else W - mid) - 0.6
        q = [(a, 8.6), (b, 8.6), (b, zb), (a, za)]; e.fillp('tint', q, e.glc, e.glo * 2.2); e.pl('openings', q, 1.3)
        for k in range(1, 4): xx = a + (b - a) * k / 4; e.ln('openings', xx, 8.6, xx, za + (zb - za) * k / 4, 0.9)
    e.window(2.0, 1.2, W * 0.34, 7.8, cols=4, rows=1, trim=0, head=False, sill=False)
    e.door(W * 0.45, 3.4, 7.8, 'slab', side=1.2)
    e.window(W * 0.66, 3.0, W * 0.66 + 6.5, 7.8, cols=3, rows=1, trim=0, head=False, sill=False)
    e.foundation(-0.3, W + 0.3)
    e.level(lo - 0.6, 'PLATE'); e.level(hi + 0.85, 'T.O. ROOF')
    return e.finish('FRONT ELEVATION', 'MID-CENTURY · BUTTERFLY ROOF · STONE & BOARD-AND-BATTEN',
                    [('man_walk', W * 0.45 - 6, GR, False), ('woman_coat', W * 0.78, GR, True, 'figs2'), ('kid_a', W * 0.78 + 2.2, GR, True, 'figs2')],
                    shrubs=[(W * 0.9, 3.0), (W * 0.24, 3.4)]), 'butterfly-roof house'


def gambrel(st, r):
    W = r.choice([30, 32]); wall, knee, ridge = 10, 17.5, 23; m = W / 2; e = E(W, ridge + 4, st)
    pr = [(-0.9, wall - 0.4), (W * 0.17, knee), (m, ridge), (W * 0.83, knee), (W + 0.9, wall - 0.4)]
    prof = [(0, 0), (W, 0), (W, wall - 0.1), (W * 0.83 - 0.4, knee - 0.6), (m, ridge - 0.8), (W * 0.17 + 0.4, knee - 0.6), (0, wall - 0.1)]
    e.walls(prof); e.siding(prof, 'bb', 1.0)
    e.rake(pr, over=1.3)
    # sliding barn doors + track
    e.ln('details', m - 9, 9.2, m + 5, 9.2, 2.6)
    for a in (m - 4, m):
        e.fillp('tint', [(a, 0), (a + 4, 0), (a + 4, 8.8), (a, 8.8)], e.st['tint2']); e.box('openings', a, 0, a + 4, 8.8, 2.0)
        e.box('openings', a + 0.3, 0.3, a + 3.7, 8.5, 1.0); e.ln('openings', a + 0.3, 4.4, a + 3.7, 4.4, 1.0)
        e.ln('openings', a + 0.3, 0.3, a + 3.7, 4.4, 1.0); e.ln('openings', a + 0.3, 4.4, a + 3.7, 0.3, 1.0)
        e.ln('openings', a + 0.3, 4.4, a + 3.7, 8.5, 1.0); e.ln('openings', a + 0.3, 8.5, a + 3.7, 4.4, 1.0)
        e.g['openings'].append(f'<circle cx="{e.x(a + 0.8):.1f}" cy="{e.y(9.2):.1f}" r="3" fill="{e.ink}"/><circle cx="{e.x(a + 3.2):.1f}" cy="{e.y(9.2):.1f}" r="3" fill="{e.ink}"/>')
    e.shade([(m - 4, 8.8), (m + 4, 8.8), (m + 4.5, 8.3), (m - 3.5, 8.3)], clip=False)
    e.door_x = m
    # hayloft
    e.window(m - 2.2, 12.2, m + 2.2, 16.4, 2, 2, shutters=False)
    e.ln('details', m - 0.3, 18.0, m + 0.3, 18.0, 1.6); e.box('details', m - 0.4, 17.6, m + 0.4, 19.2, 1.6, e.st['tint2'])
    e.window(2.6, 2.8, 6.4, 7.4, 2, 2); e.window(W - 6.4, 2.8, W - 2.6, 7.4, 2, 2)
    # cupola
    e.box('details', m - 1.6, ridge - 0.6, m + 1.6, ridge + 2.4, 1.9, e.st['tint2'])
    for k in range(1, 6): e.ln('details', m - 1.3, ridge - 0.3 + k * 0.45, m + 1.3, ridge - 0.3 + k * 0.45, 0.8, e.sub)
    e.pl('details', [(m - 2.3, ridge + 2.4), (m, ridge + 4.0), (m + 2.3, ridge + 2.4)], 1.9, e.st['tint2'])
    e.foundation(-0.2, W + 0.2)
    e.level(wall - 0.4, 'EAVE'); e.level(ridge + 0.75, 'RIDGE')
    return e.finish('FRONT ELEVATION', 'GAMBREL BARN HOUSE · BOARD & BATTEN · SLIDING BARN DOORS',
                    [('woman_dog', m - 6.5, GR, False), ('man_stand', W - 4.5, GR, True, 'figs2'), ('kid_b', W - 2.8, GR, True, 'figs2')],
                    shrubs=[(1.8, 3.2), (W - 1.0, 2.6)]), 'gambrel barn house'


def saltbox(st, r):
    W = r.choice([36, 38]); fr, ridge, back = 18, 25, 9; rx = W * 0.36; e = E(W, ridge + 4, st)
    prof = [(0, 0), (W, 0), (W, back), (rx, ridge - 0.8), (0, fr - 0.6)]
    e.walls(prof); e.siding(prof, 'lap', 0.55)
    e.rake([(-0.9, fr - 1.0), (rx, ridge), (W + 0.9, back - 0.4)], over=1.1)
    e.chimney(rx + 2.5, rx + 5.2, ridge - 2.5, ridge + 3.0)
    for (z1, z2) in ((2.6, 7.4), (11, 15.2)):
        for xx in (3, 9.5, 23.5, 30):
            zt = fr - 0.6 + (xx - 0) * 0 if xx < rx else back + (W - xx - 3.2) * (ridge - back) / (W - rx)
            if xx + 3.2 < W - 0.8 and (z2 < 8 or z2 + 1.2 < (fr if xx < rx else zt)): e.window(xx, z1, xx + 3.2, z2, 2, 3, shutters=True)
    e.door(17.6, 3.2, 7.0, 'panel', transom=True)
    e.foundation(-0.2, W + 0.2)
    e.level(fr - 0.6, 'PLATE'); e.level(ridge + 0.75, 'RIDGE')
    return e.finish('SIDE ELEVATION', 'NEW ENGLAND SALTBOX · CENTER CHIMNEY · CLAPBOARD',
                    [('elder', 12.5, GR, False), ('woman_walk', 25, GR, False, 'figs2')], shrubs=[(7, 3.0), (28, 3.0)]), 'saltbox'


def farmhouse(st, r):
    W = r.choice([44, 48]); wall, ridge = 10, 22; gw = 9.5; m = W * 0.36; e = E(W, ridge + 3, st)
    prof = [(0, 0), (W, 0), (W, wall), (m + gw, wall), (m + gw, 13.5), (m, ridge - 1), (m - gw, 13.5), (m - gw, wall), (0, wall)]
    e.walls(prof); e.siding(prof, 'bb', 1.2)
    # side wing roof (eave side visible: standing seam)
    wr = [(m + gw - 0.2, wall), (W + 1, wall), (W + 1, wall + 5.2), (m + gw - 0.2, wall + 5.2)]
    e.fillp('tint', wr, e.st['tint2']); e.pl('roof', wr, 2.2); e.siding(wr, 'seam', 1.25)
    wl = [(-1, wall), (m - gw + 0.2, wall), (m - gw + 0.2, wall + 3.2), (-1, wall + 3.2)]
    e.fillp('tint', wl, e.st['tint2']); e.pl('roof', wl, 2.2); e.siding(wl, 'seam', 1.25)
    e.eave_shadow(0, W, wall, 1.1)
    # main gable rake
    e.rake([(m - gw - 1.0, 12.9), (m, ridge), (m + gw + 1.0, 12.9)], over=1.2)
    e.window(m - 2.2, 14.0, m + 2.2, 18.4, 2, 3)
    # porch: shed standing-seam roof, posts
    pz = 9.0; pr = [(-1.6, pz - 0.2), (W + 1.6, pz - 0.2), (W + 1.6, pz + 0.7), (-1.6, pz + 0.7)]
    e.fillp('tint', pr, e.st['tint2']); e.pl('roof', pr, 2.4)
    e.shade([(0, pz - 0.2), (W, pz - 0.2), (W, pz - 3.6), (0, pz - 3.6)])
    for xx in [0.6 + k * (W - 1.2) / 5 for k in range(6)]:
        e.fillp('details', [(xx - 0.3, 0), (xx + 0.3, 0), (xx + 0.3, pz - 0.2), (xx - 0.3, pz - 0.2)], e.st['bg'])
        e.box('details', xx - 0.3, 0, xx + 0.3, pz - 0.2, 1.7)
    e.door(m, 3.4, 7.6, 'glass', side=0)
    for xx in (3.5, m + 4.5, W - 13, W - 7.5):
        e.window(xx, 1.6, xx + 3.6, 7.4, 2, 3, trim=0.22)
    e.foundation(-0.2, W + 0.2)
    e.level(wall, 'PLATE'); e.level(ridge + 0.75, 'RIDGE')
    return e.finish('FRONT ELEVATION', 'MODERN FARMHOUSE · STANDING-SEAM PORCH · BOARD & BATTEN',
                    [('man_stride', m - 7.5, GR, True), ('wave_b', m + 2.6, 0, True, 'figs2'), ('woman_dog', W - 3.5, GR, False, 'figs2')],
                    shrubs=[(W * 0.6, 3.4)]), 'modern farmhouse'


def charleston(st, r):
    hw = 20; pz = 9; W = hw + pz; fl = 11; ridge = 2 * fl + 8; e = E(W, ridge + 2, st)
    hx = 0; px0 = hw
    prof = [(hx, 0), (hx + hw, 0), (hx + hw, 2 * fl), (hx + hw / 2, ridge - 0.7), (hx, 2 * fl)]
    e.walls(prof); e.siding(prof, 'lap', 0.55)
    e.rake([(hx - 0.9, 2 * fl - 0.5), (hx + hw / 2, ridge), (hx + hw + 0.9, 2 * fl - 0.5)], over=1.0)
    cx, cz = hx + hw / 2, 2 * fl + 3.4
    e.fillp('tint', [(cx + 1.3 * math.cos(a / 16 * 2 * math.pi), cz + 1.3 * math.sin(a / 16 * 2 * math.pi)) for a in range(16)], e.glc, e.glo * 2.2)
    e.g['openings'].append(f'<circle cx="{e.x(cx):.1f}" cy="{e.y(cz):.1f}" r="{1.3 * e.S:.1f}" fill="none" stroke="{e.ink}" stroke-width="1.9"/><circle cx="{e.x(cx):.1f}" cy="{e.y(cz):.1f}" r="{1.6 * e.S:.1f}" fill="none" stroke="{e.ink}" stroke-width="1.3"/>')
    for lvl in (0, 1):
        z0 = lvl * fl
        for xx in (hx + 3.6, hx + hw - 6.6): e.window(xx, z0 + 2.2, xx + 3, z0 + 8.6, 2, 3, shutters=True)
        e.ln('details', hx, z0 + fl, hx + hw, z0 + fl, 1.6)
    # piazza: two stories of columns, rails, shed roof
    e.fillp('tint', [(px0, 0), (W, 0), (W, 2 * fl - 0.6), (px0, 2 * fl + 0.2)], e.st['tint2'])
    e.g['shade'].append(f'<path d="{e._d([(px0, 2 * fl + 0.2), (W, 2 * fl - 0.6), (W, 0), (px0, 0)])}" fill="{e.shc}" fill-opacity="{e.sho * 0.6}"/>')
    for lvl in (0, 1):
        z0 = lvl * fl
        e.box('details', px0, z0 + fl - 0.7, W, z0 + fl, 1.9, e.st['bg'])
        e.ln('details', px0, z0 + 3.0, W - 0.5, z0 + 3.0, 1.9); e.ln('details', px0, z0 + 0.4, W - 0.5, z0 + 0.4, 1.2)
        for k in range(1, 16): xx = px0 + k * (pz - 0.5) / 16; e.ln('details', xx, z0 + 0.4, xx, z0 + 3.0, 0.7, e.sub)
        for xx in (px0 + 0.45, W - 0.5):
            e.fillp('details', [(xx - 0.35, z0), (xx + 0.35, z0), (xx + 0.35, z0 + fl - 0.7), (xx - 0.35, z0 + fl - 0.7)], e.st['bg'])
            e.box('details', xx - 0.35, z0, xx + 0.35, z0 + fl - 0.7, 1.7)
            e.box('details', xx - 0.5, z0 + fl - 1.1, xx + 0.5, z0 + fl - 0.7, 1.2); e.box('details', xx - 0.5, z0, xx + 0.5, z0 + 0.4, 1.2)
    e.pl('roof', [(px0, 2 * fl + 0.9), (W + 0.9, 2 * fl + 0.1), (W + 0.9, 2 * fl - 0.6), (px0, 2 * fl + 0.2)], 2.4, e.st['tint2'])
    # street door into the piazza (the Charleston "privacy door")
    e.box('openings', px0 + 2.2, 0, px0 + 6.0, 8.0, 1.0, e.st['bg']); e.door(px0 + 4.1, 3.0, 7.3, 'panel', transom=True, stoop=False)
    e.foundation(-0.2, W + 0.2)
    e.level(fl, '2ND FL.'); e.level(ridge + 0.75, 'RIDGE')
    return e.finish('STREET ELEVATION', 'CHARLESTON SINGLE HOUSE · TWO-STORY SIDE PIAZZA',
                    [('man_walk', 15.0, GR, True), ('woman_coat', 6.0, GR, True, 'figs2'), ('kid_a', 8.0, GR, True, 'figs2')],
                    shrubs=[(12.5, 2.8), (3.0, 2.6)]), 'Charleston single house'


def shed_modern(st, r):
    W = r.choice([42, 46]); lo, hi = 11, 18; wing = W * 0.34; e = E(W, hi + 3, st)
    prof = [(0, 0), (W, 0), (W, hi - 0.2), (wing, lo + 0.2), (wing, 10), (0, 10)]
    e.walls(prof); e.siding([(wing, 0), (W, 0), (W, hi), (wing, lo)], 'bb', 0.75)
    e.pl('roof', [(-1, 10), (wing + 0.2, 10), (wing + 0.2, 10.8), (-1, 10.8)], 2.4, e.st['tint2'])
    e.pl('roof', [(wing - 0.6, lo), (W + 2, hi + 0.25), (W + 2, hi + 1.05), (wing - 0.6, lo + 0.8)], 2.6, e.st['tint2'])
    e.shade([(wing, lo + 0.2), (W, hi), (W, hi - 2.2), (wing + 1.6, lo - 1.6)])
    e.eave_shadow(0, wing, 10, 1.0)
    e.window(W - 9, 1.2, W - 1, hi - 2.6, 2, 3, trim=0, head=False, sill=False)
    e.window(wing + 2, 6.4, wing + 10, 9.0, 4, 1, trim=0, head=False, sill=False)
    e.door(wing + 6, 3.4, 8, 'slab')
    e.fillp('tint', [(1.5, 0), (wing - 1.5, 0), (wing - 1.5, 8.2), (1.5, 8.2)], e.st['tint2']); e.box('openings', 1.5, 0, wing - 1.5, 8.2, 1.9)
    for k in range(1, 5): e.ln('openings', 1.5, k * 8.2 / 5, wing - 1.5, k * 8.2 / 5, 0.9)
    e.shade([(1.5, 8.2), (wing - 1.5, 8.2), (wing - 1.5, 7.7), (2.0, 7.7), (2.0, 0), (1.5, 0)], clip=False)
    e.foundation(-0.2, W + 0.2)
    e.level(10, 'GARAGE'); e.level(hi + 1.05, 'T.O. ROOF')
    return e.finish('FRONT ELEVATION', 'MODERN SHED ROOF · CORNER GLAZING · GARAGE WING',
                    [('man_dog', wing + 1.2, GR, True), ('woman_stand', W - 5, GR, True, 'figs2')], shrubs=[(wing + 11.5, 3.0)]), 'modern shed-roof house'


def craftsman(st, r):
    W = r.choice([34, 36]); wall, ridge = 9.5, 17.5; m = W / 2; e = E(W, ridge + 3, st)
    prof = [(0, 0), (W, 0), (W, wall), (m, ridge - 0.9), (0, wall)]
    e.walls(prof)
    e.siding([(0, wall), (W, wall), (m, ridge)], 'shingle', 0.5)
    e.siding([(0, 0), (W, 0), (W, wall), (0, wall)], 'lap', 0.6)
    e.ln('details', 0, wall, W, wall, 1.9)
    over = 2.4; ext = over * (ridge - wall) / m
    e.rake([(-over, wall - ext), (m, ridge), (W + over, wall - ext)], over=2.0, th=0.9)
    # knee braces under the rake at each wall corner
    rz = lambda xx: wall - ext + (xx + over) * (ridge - wall + ext) / (m + over) if xx < m else wall - ext + (W + over - xx) * (ridge - wall + ext) / (m + over)
    for x0, sd in ((0, -1), (W, 1)):
        xo = x0 + sd * 1.8; e.box('details', x0 - 0.18, wall - 2.2, x0 + 0.18, rz(x0), 1.4, e.st['bg'])
        e.pl('details', [(x0, wall - 2.0), (xo, rz(xo)), (x0, rz(x0) - 0.2)], 1.6, e.st['bg'])
    e.vent(m, ridge - 3.6, 1.6)
    # porch: beam on tapered columns over brick piers
    pb = 8.0
    e.box('details', -0.6, pb, W + 0.6, pb + 0.9, 1.9, e.st['bg']); e.shade([(0, pb), (W, pb), (W, pb - 3.0), (0, pb - 3.0)])
    for xx in (2.4, W - 2.4, m - 7, m + 7) if W > 35 else (2.4, W - 2.4):
        e.fillp('details', [(xx - 1.4, 0), (xx + 1.4, 0), (xx + 1.4, 3.0), (xx - 1.4, 3.0)], e.st['tint2'])
        e.box('details', xx - 1.4, 0, xx + 1.4, 3.0, 1.9); e.box('details', xx - 1.6, 3.0, xx + 1.6, 3.3, 1.6)
        for zz in (0.5, 1.0, 1.5, 2.0, 2.5): e.ln('details', xx - 1.4, zz, xx + 1.4, zz, 0.7, e.sub)
        e.fillp('details', [(xx - 0.95, 3.3), (xx + 0.95, 3.3), (xx + 0.55, pb), (xx - 0.55, pb)], e.st['bg'])
        e.pl('details', [(xx - 0.95, 3.3), (xx + 0.95, 3.3), (xx + 0.55, pb), (xx - 0.55, pb)], 1.7)
    e.door(9.0, 3.0, 6.9, 'craft')
    e.window(m - 3.6, 2.2, m + 3.6, 6.8, 3, 1); e.ln('openings', m - 3.6, 5.3, m + 3.6, 5.3, 1.0)
    e.window(W - 11.5, 2.2, W - 8.0, 6.8, 1, 2)
    e.foundation(-0.2, W + 0.2)
    e.level(wall, 'PLATE'); e.level(ridge + 0.9, 'RIDGE')
    return e.finish('FRONT ELEVATION', 'CRAFTSMAN BUNGALOW · TAPERED COLUMNS · KNEE BRACES',
                    [('woman_dog', 9.0 - 5.0, GR, False), ('man_stand', W - 5.6, 0, True, 'figs2'), ('kid_a', W - 4.2, 0, False, 'figs2')],
                    shrubs=[(m, 3.2)]), 'Craftsman bungalow'


def cape(st, r):
    W = r.choice([36, 38]); wall, ridge = 9, 19.5; m = W / 2; e = E(W, ridge + 4, st)
    e.walls([(0, 0), (W, 0), (W, wall), (0, wall)]); e.siding([(0, 0), (W, 0), (W, wall), (0, wall)], 'lap', 0.55)
    roof = [(-1.2, wall - 0.3), (W + 1.2, wall - 0.3), (W + 0.6, ridge), (-0.6, ridge)]
    e.fillp('tint', roof, e.st['tint2']); e.pl('roof', roof, 2.6); e.siding(roof, 'shingle', 0.62)
    e.ln('roof', -1.3, ridge + 0.35, W + 1.3, ridge + 0.35, 2.6); e.ln('roof', -1.3, ridge, W + 1.3, ridge, 1.2)
    e.eave_shadow(0, W, wall, 1.0)
    for dc in (W * 0.27, W * 0.73):
        dp = [(dc - 2.6, wall + 3.4), (dc - 2.6, wall + 7.2), (dc, wall + 9.2), (dc + 2.6, wall + 7.2), (dc + 2.6, wall + 3.4)]
        e.fillp('roof', dp, e.st['tint']); e.pl('roof', dp, 2.2); e.siding(dp, 'lap', 0.55)
        e.pl('roof', [(dc - 3.1, wall + 6.9), (dc, wall + 9.6), (dc + 3.1, wall + 6.9)], 2.4, close=False)
        e.shade([(dc - 2.6, wall + 7.2), (dc, wall + 9.2), (dc + 2.6, wall + 7.2), (dc + 2.6, wall + 6.6), (dc, wall + 8.4), (dc - 2.0, wall + 6.6)], clip=False)
        e.window(dc - 1.4, wall + 3.9, dc + 1.4, wall + 6.6, 2, 2, trim=0.22, sill=False, head=False)
    e.chimney(m - 1.4, m + 1.4, ridge - 1.2, ridge + 3.4)
    for xx in (W * 0.1, W * 0.27 - 1.5, W * 0.73 - 1.5, W * 0.9 - 3):
        e.window(xx, 2.4, xx + 3, 7.0, 2, 3, shutters=True)
    e.door(m, 3.2, 7.0, 'panel', side=1.1)
    e.pl('details', [(m - 3.4, 7.8), (m, 8.6), (m + 3.4, 7.8)], 1.9, e.st['bg'], close=True)
    e.foundation(-0.2, W + 0.2)
    e.level(wall, 'PLATE'); e.level(ridge + 0.35, 'RIDGE')
    return e.finish('FRONT ELEVATION', 'CAPE COD · TWIN DORMERS · SHUTTERS & CENTER CHIMNEY',
                    [('woman_walk', m - 5.5, GR, False), ('man_dog', W * 0.84, GR, True, 'figs2')],
                    shrubs=[(W * 0.17, 2.8), (W * 0.62, 2.6)]), 'Cape Cod'


TYPES = {'a_frame': a_frame, 'butterfly': butterfly, 'gambrel': gambrel, 'saltbox': saltbox, 'farmhouse': farmhouse,
         'charleston': charleston, 'shed_modern': shed_modern, 'craftsman': craftsman, 'cape': cape}

LAST = {}
def make(kind, seed, st):
    r = random.Random(seed)
    orig = E.__init__
    def init(self, *a, **k): orig(self, *a, **k); LAST['e'] = self
    E.__init__ = init
    try: (svg, order), label = TYPES[kind](st, r)
    finally: E.__init__ = orig
    return svg, order, label
