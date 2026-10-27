"""Procedural, original residential floor plans (several house types) as layered SVG.
Front of house faces the bottom of the canvas. Units: feet."""
import random
from .draw import L, R, C, P, T, G, dimH, dimV, fmt_ft

RES = 0.5
PUBLIC = ('living', 'dining', 'kitchen', 'hall', 'foyer')
WORD = {0: 'STUDIO', 1: 'ONE', 2: 'TWO', 3: 'THREE', 4: 'FOUR'}
TYPES = ['ranch', 'split', 'narrow', 'lshape', 'adu', 'shotgun', 'dogtrot', 'courtyard']
TYPE_NAME = {'ranch': 'RANCH', 'split': 'SPLIT-BEDROOM RANCH', 'narrow': 'NARROW-LOT HOME', 'lshape': 'RANCH WITH GARAGE', 'adu': 'BACKYARD COTTAGE', 'shotgun': 'SHOTGUN HOUSE', 'dogtrot': 'DOGTROT HOUSE', 'courtyard': 'COURTYARD HOUSE'}

def _u(a, b): return [round(a + i * RES, 2) for i in range(int(round((b - a) / RES)))]

class Room:
    def __init__(s, name, kind, x, y, w, h): s.name, s.kind, s.x, s.y, s.w, s.h = name, kind, x, y, w, h
    @property
    def x2(s): return s.x + s.w
    @property
    def y2(s): return s.y + s.h

def shared(a, b):
    """shared edge between rooms: (orient, coord, lo, hi) or None"""
    for c in (a.x2,):
        if abs(c - b.x) < 1e-6:
            lo, hi = max(a.y, b.y), min(a.y2, b.y2)
            if hi - lo > 1e-6: return ('v', c, lo, hi)
    if abs(a.x - b.x2) < 1e-6:
        lo, hi = max(a.y, b.y), min(a.y2, b.y2)
        if hi - lo > 1e-6: return ('v', a.x, lo, hi)
    if abs(a.y2 - b.y) < 1e-6:
        lo, hi = max(a.x, b.x), min(a.x2, b.x2)
        if hi - lo > 1e-6: return ('h', a.y2, lo, hi)
    if abs(a.y - b.y2) < 1e-6:
        lo, hi = max(a.x, b.x), min(a.x2, b.x2)
        if hi - lo > 1e-6: return ('h', a.y, lo, hi)
    return None

class Plan:
    def __init__(self, seed, typ=None):
        self.rng = random.Random(seed); self.seed = seed
        self.typ = typ or self.rng.choice(TYPES)
        self.rooms, self.doors, self.windows, self.open = [], [], [], set()
        self.garage_door = None
        self.extras = []  # (kind, x, y, w, h, label) non-walled areas: porch/court

    def add(self, *a): self.rooms.append(Room(*a)); return self.rooms[-1]

    # ---------------- house types ----------------
    def build(self):
        getattr(self, '_' + self.typ)()
        self.W = max([r.x2 for r in self.rooms] + [e[1] + e[3] for e in self.extras]); self.D = max([r.y2 for r in self.rooms] + [e[2] + e[4] for e in self.extras])
        self.beds = sum(1 for r in self.rooms if r.kind == 'bed')
        self.sf = int(sum(r.w * r.h for r in self.rooms if r.kind != 'garage'))
        self._open_plan(); self._doors(); self._windows()
        return self

    def _public_row(self, x0, y0, W, D, allow_laundry=True):
        r = self.rng
        kit = r.choice([11, 12, 13]); din = r.choice([10, 11, 12]) if W - kit >= 24 else 0
        lw = 7 if allow_laundry and W - kit - din >= 21 and r.random() < 0.6 else 0
        liv = W - kit - din - lw
        seq = [('LIVING', 'living', liv), ('DINING', 'dining', din), ('KITCHEN', 'kitchen', kit)]
        seq = [s for s in seq if s[2] > 0]
        if r.random() < 0.5: seq = seq[::-1]
        if lw: seq = ([('LAUNDRY', 'laundry', lw)] + seq) if seq[0][1] != 'living' else (seq + [('LAUNDRY', 'laundry', lw)])
        x = x0
        for name, kind, w in seq:
            if kind == 'laundry':
                self.add(name, kind, x, y0, w, 8); self.add('PANTRY', 'pantry', x, y0 + 8, w, D - 8)
            else: self.add(name, kind, x, y0, w, D)
            x += w

    def _bed_row(self, x0, y0, W, D, beds, flip):
        r = self.rng; prim = r.choice([14, 15, 16]); bath = 8
        others = beds - 1; ow = (W - prim - bath) / max(1, others)
        if others and ow < 10.5: prim = 13; ow = (W - prim - bath) / others
        seq = [('PRIMARY BEDROOM' if beds > 1 else 'BEDROOM', 'bed', prim), ('BATH', 'bath', bath)] + [(f'BEDROOM {i + 2}', 'bed', ow) for i in range(others)]
        if beds == 1: seq = [('BEDROOM', 'bed', W - bath), ('BATH', 'bath', bath)]
        if flip: seq = seq[::-1]
        x = x0
        for name, kind, w in seq: self.add(name, kind, x, y0, w, D); x += w

    def _ranch(self):
        r = self.rng; beds = r.choice([2, 3, 3, 4])
        W = {2: r.choice([34, 36, 38]), 3: r.choice([44, 46, 48, 50]), 4: r.choice([54, 56, 58])}[beds]
        Dp = r.choice([12, 13, 14]); Dpub = r.choice([16, 18, 20])
        self._bed_row(0, 0, W, Dp, beds, r.random() < 0.5)
        self.add('HALL', 'hall', 0, Dp, W, 4)
        self._public_row(0, Dp + 4, W, Dpub)

    def _split(self):
        r = self.rng; D = r.choice([32, 34, 36]); lw = r.choice([15, 16]); rw = r.choice([13, 14]); mw = r.choice([24, 26, 28])
        left = r.random() < 0.5
        Lx, Mx, Rx = (0, lw, lw + mw) if left else (rw + mw, rw, 0)
        bedD = r.choice([14, 15]); self.add('PRIMARY BEDROOM', 'bed', Lx, 0, lw, bedD)
        self.add('PRIMARY BATH', 'bath', Lx, bedD, lw, 9); self.add('W.I.C.', 'wic', Lx, bedD + 9, lw, D - bedD - 9)
        b1 = r.choice([12, 13]); self.add('BEDROOM 2', 'bed', Rx, 0, rw, b1)
        self.add('BATH', 'bath', Rx, b1, rw, 8); self.add('BEDROOM 3', 'bed', Rx, b1 + 8, rw, D - b1 - 8)
        kd = r.choice([12, 13, 14]); kw = r.choice([13, 14])
        self.add('KITCHEN', 'kitchen', Mx, 0, kw, kd); self.add('DINING', 'dining', Mx + kw, 0, mw - kw, kd)
        self.add('LIVING', 'living', Mx, kd, mw, D - kd)

    def _narrow(self):
        r = self.rng; W = r.choice([20, 22, 24]); hall = 4
        liv = r.choice([15, 16, 17]); kit = r.choice([13, 14])
        y = 0; beds = r.choice([2, 3])
        side = r.random() < 0.5  # hall on left?
        bw = W - hall; hx, bx = (0, hall) if side else (W - hall, 0)
        bd = [r.choice([12, 13]) for _ in range(beds)]
        names = ['PRIMARY BEDROOM'] + [f'BEDROOM {i + 2}' for i in range(beds - 1)]
        for i in range(beds):
            self.add(names[i], 'bed', bx, y, bw, bd[i]); y += bd[i]
            if i == 0: self.add('BATH', 'bath', bx, y, bw, 8); y += 8
        top = 0; self.add('HALL', 'hall', hx, top, hall, y - top)
        self.add('KITCHEN', 'kitchen', 0, y, W * 0.55, kit); self.add('DINING', 'dining', W * 0.55, y, W * 0.45, kit); y += kit
        self.add('LIVING', 'living', 0, y, W, liv)

    def _lshape(self):
        r = self.rng; beds = r.choice([3, 3, 4]); W = 44 if beds == 3 else 52
        Dp = 13; Dpub = r.choice([17, 18])
        gar_left = r.random() < 0.5; G = r.choice([22, 24])
        x0 = G if gar_left else 0
        self._bed_row(x0, 0, W, Dp, beds, not gar_left)
        self.add('HALL', 'hall', x0, Dp, W, 4)
        self._public_row(x0, Dp + 4, W, Dpub, allow_laundry=False)
        gy = Dp + 4 + Dpub - G + 4
        gx = 0 if gar_left else W
        self.add('GARAGE', 'garage', gx, gy, G, G)

    def _adu(self):
        r = self.rng; W = r.choice([20, 22, 24]); D = r.choice([24, 26, 28])
        bd = r.choice([10, 11]); bath = 8
        self.add('BEDROOM', 'bed', 0, 0, W - bath, bd); self.add('BATH', 'bath', W - bath, 0, bath, bd)
        self.add('KITCHEN', 'kitchen', 0, bd, W, 8); self.add('LIVING', 'living', 0, bd + 8, W, D - bd - 8)


    def _shotgun(self):
        r = self.rng; W = r.choice([14, 15, 16]); y = 0
        seq = [('KITCHEN', 'kitchen', r.choice([12, 13])), ('BATH', 'bath', 8), ('BEDROOM 2', 'bed', 12), ('PRIMARY BEDROOM', 'bed', 13), ('LIVING', 'living', r.choice([14, 15]))]
        if r.random() < 0.5: seq.pop(2)
        for name, kind, d in seq:
            if kind == 'bath':
                self.add('BATH', 'bath', 0, y, W - 5, d); self.add('HALL', 'hall', W - 5, y, 5, d)
            else: self.add(name, kind, 0, y, W, d)
            y += d
        self.extras.append(('porch', 0, y, W, 6, 'FRONT PORCH'))
        self.chain = True

    def _dogtrot(self):
        r = self.rng; pw = r.choice([16, 17, 18]); bz = r.choice([10, 12]); D = r.choice([28, 30, 32])
        L0, R0 = 0, pw + bz
        kd = r.choice([12, 13]); self.add('KITCHEN', 'kitchen', L0, 0, pw, kd); self.add('LIVING', 'living', L0, kd, pw, D - kd)
        b1 = r.choice([12, 13]); self.add('PRIMARY BEDROOM', 'bed', R0, 0, pw, b1); self.add('HALL', 'hall', R0, b1, 4, 7)
        self.add('BATH', 'bath', R0 + 4, b1, pw - 4, 7); self.add('BEDROOM 2', 'bed', R0, b1 + 7, pw, D - b1 - 7)
        self.extras.append(('porch', pw, 0, bz, D, 'BREEZEWAY'))
        self.extras.append(('porch', 0, D, 2 * pw + bz, 6, 'FRONT PORCH'))
        self.trot = (pw, bz, D, kd, b1)

    def _courtyard(self):
        r = self.rng; ww = r.choice([15, 16]); cw = r.choice([20, 22, 24]); W = 2 * ww + cw; back = r.choice([16, 18]); wing = r.choice([24, 26])
        self.add('KITCHEN', 'kitchen', 0, 0, ww, back)
        self.add('DINING', 'dining', ww, 0, cw * 0.45, back); self.add('LIVING', 'living', ww + cw * 0.45, 0, W - ww - cw * 0.45, back)
        self.add('BEDROOM 2', 'bed', 0, back, ww - 4, 13); self.add('BATH', 'bath', 0, back + 13, ww - 4, wing - 13); self.add('HALL', 'hall', ww - 4, back, 4, wing)
        self.add('HALL', 'hall', W - ww, back, 4, wing); self.add('PRIMARY BEDROOM', 'bed', W - ww + 4, back, ww - 4, 14); self.add('PRIMARY BATH', 'bath', W - ww + 4, back + 14, ww - 4, wing - 14)
        self.extras.append(('court', ww, back, cw, wing, 'COURTYARD'))

    # ---------------- openings ----------------
    def _open_plan(self):
        pub = [r for r in self.rooms if r.kind in PUBLIC]
        for a in pub:
            for b in pub:
                if a is b: continue
                s = shared(a, b)
                if s:
                    o, c, lo, hi = s
                    for u in _u(lo, hi): self.open.add((o, round(c, 2), u))

    def _neighbors(self, rm):
        out = []
        for o in self.rooms:
            if o is rm: continue
            s = shared(rm, o)
            if s: out.append((o, s))
        return out

    def _door_on(self, s, width, rm, near_start):
        o, c, lo, hi = s
        if hi - lo < width + 1: return
        a = lo + 0.8 if near_start else hi - 0.8 - width
        # swing into rm
        if o == 'h': swing = 'up' if abs(rm.y2 - c) < 1e-6 else 'down'
        else: swing = 'left' if abs(rm.x2 - c) < 1e-6 else 'right'
        self.doors.append((o, c, a, a + width, near_start, swing))

    def _doors(self):
        r = self.rng
        for rm in self.rooms:
            nb = self._neighbors(rm)
            if rm.kind in ('bed', 'bath', 'laundry', 'pantry', 'wic', 'garage'):
                if rm.kind == 'bath' and rm.name == 'PRIMARY BATH':
                    pref = [x for x in nb if x[0].kind == 'bed']
                elif rm.kind == 'wic':
                    pref = [x for x in nb if x[0].kind == 'bath']
                elif rm.kind == 'garage':
                    pref = [x for x in nb if x[0].kind in ('laundry', 'kitchen', 'living', 'dining', 'hall')]
                else:
                    pref = [x for x in nb if x[0].kind in PUBLIC]
                if not pref: continue
                o, s = max(pref, key=lambda x: x[1][3] - x[1][2])
                self._door_on(s, 2.5 if rm.kind in ('bath', 'pantry', 'wic') else 3, rm, r.random() < 0.5)
        # entry door on front edge of living
        liv = [x for x in self.rooms if x.kind == 'living']
        if liv:
            lv = liv[0]
            if abs(lv.y2 - self.D) < 1e-6 or not any(abs(o.y - lv.y2) < 1e-6 and o.x < lv.x2 and o.x2 > lv.x for o in self.rooms):
                ex = lv.x + lv.w * r.choice([0.2, 0.7]); self.doors.append(('h', lv.y2, ex, ex + 3, True, 'up'))
        if self.typ == 'dogtrot':
            pw, bz, D, kd, b1 = self.trot
            lv = [x for x in self.rooms if x.kind == 'living'][0]
            self.doors.append(('v', pw, kd + 3, kd + 6, True, 'left'))
            self.doors.append(('v', pw + bz, b1 + 2, b1 + 5, True, 'right'))
            self.doors = [d for d in self.doors if not (d[0] == 'h' and abs(d[1] - lv.y2) < 1e-6 and d[2] >= lv.x - 1e-6 and d[3] <= lv.x2 + 1e-6 and self.typ == 'dogtrot')]
        gar = [x for x in self.rooms if x.kind == 'garage']
        if gar:
            g = gar[0]; self.garage_door = (g.x + 3, g.x2 - 3, g.y2)

    def _ext_edges(self):
        """unit edges that are on the exterior (belong to exactly one room)"""
        cnt = {}
        for rm in self.rooms:
            for (o, c, a, b) in [('h', rm.y, rm.x, rm.x2), ('h', rm.y2, rm.x, rm.x2), ('v', rm.x, rm.y, rm.y2), ('v', rm.x2, rm.y, rm.y2)]:
                for u in _u(a, b): k = (o, round(c, 2), u); cnt[k] = cnt.get(k, 0) + 1
        return {k for k, v in cnt.items() if v == 1}

    def _windows(self):
        ext = self._ext_edges()
        for rm in self.rooms:
            if rm.kind in ('hall', 'pantry', 'wic', 'garage'): continue
            for (o, c, a, b) in [('h', rm.y, rm.x, rm.x2), ('h', rm.y2, rm.x, rm.x2), ('v', rm.x, rm.y, rm.y2), ('v', rm.x2, rm.y, rm.y2)]:
                units = [u for u in _u(a, b) if (o, round(c, 2), u) in ext]
                if len(units) * RES < 6: continue
                lo, hi = min(units), max(units) + RES
                if any(d[0] == o and abs(d[1] - c) < 1e-6 and d[2] < hi and d[3] > lo for d in self.doors):
                    if hi - lo < 14: continue
                    lo, hi = (lo, lo + (hi - lo) / 2 - 2) if True else (lo, hi)
                wl = {'bath': 3, 'kitchen': 4, 'laundry': 3}.get(rm.kind, 6 if rm.kind == 'living' else 5)
                wl = min(wl, hi - lo - 2)
                if wl < 2.5: continue
                m = (lo + hi) / 2; self.windows.append((o, c, m - wl / 2, m + wl / 2))

    # ---------------- walls ----------------
    def walls(self):
        ext = self._ext_edges(); edges = {}
        for rm in self.rooms:
            for (o, c, a, b) in [('h', rm.y, rm.x, rm.x2), ('h', rm.y2, rm.x, rm.x2), ('v', rm.x, rm.y, rm.y2), ('v', rm.x2, rm.y, rm.y2)]:
                for u in _u(a, b):
                    k = (o, round(c, 2), u); edges[k] = k in ext
        for k in list(edges):
            if k in self.open and not edges[k]: del edges[k]
        for (o, c, a, b, *_) in self.doors + self.windows:
            for u in _u(a, b): edges.pop((o, round(c, 2), u), None)
        if self.garage_door:
            a, b, yy = self.garage_door
            for u in _u(a, b): edges.pop(('h', round(yy, 2), u), None)
        segs = {True: [], False: []}; cur = None
        for k in sorted(edges):
            o, c, u = k; e = edges[k]
            if cur and cur[0] == o and abs(cur[1] - c) < 1e-6 and abs(cur[3] - u) < 1e-6 and cur[4] == e: cur[3] = u + RES
            else:
                if cur: segs[cur[4]].append(tuple(cur[:4]))
                cur = [o, c, u, u + RES, e]
        if cur: segs[cur[4]].append(tuple(cur[:4]))
        return segs

    def _solid(self, rm, side):
        """True if the given side of rm is a full wall (not open plan)"""
        o, c, a, b = {'top': ('h', rm.y, rm.x, rm.x2), 'bottom': ('h', rm.y2, rm.x, rm.x2), 'left': ('v', rm.x, rm.y, rm.y2), 'right': ('v', rm.x2, rm.y, rm.y2)}[side]
        return not any((o, round(c, 2), u) in self.open for u in _u(a, b))

    # ---------------- svg ----------------
    def svg(self, ink, sub, tint, box=(70, 560, 940, 980), title=True, fills=None, sketch=False):
        W, D = self.W, self.D; bx, by, bw, bh = box
        S = min(bw / W, bh / D); X0 = bx + (bw - W * S) / 2; Y0 = by + (bh - D * S) / 2
        self.S, self.X0, self.Y0 = S, X0, Y0
        x = lambda f: X0 + f * S; y = lambda f: Y0 + f * S
        EW = max(8, min(14, S * 0.45)); IW = max(5, min(8, S * 0.26))
        segs = self.walls()
        def lines(lst, w):
            return [L(x(a), y(c), x(b), y(c), w, ink) if o == 'h' else L(x(c), y(a), x(c), y(b), w, ink) for o, c, a, b in lst]
        tg = []
        for rm in self.rooms:
            col = (fills or {}).get(rm.kind, tint) if rm.kind != 'garage' else (fills or {}).get('garage', tint)
            tg.append(R(x(rm.x), y(rm.y), rm.w * S, rm.h * S, 0, col, 'none'))
        we = G('walls-ext', *lines(segs[True], EW)); wi = G('walls-int', *lines(segs[False], IW))
        op = []
        for o, c, a, b in self.windows:
            off = EW * 0.35
            if o == 'h': op += [L(x(a), y(c) - off, x(b), y(c) - off, 1.4, ink), L(x(a), y(c) + off, x(b), y(c) + off, 1.4, ink)]
            else: op += [L(x(c) - off, y(a), x(c) - off, y(b), 1.4, ink), L(x(c) + off, y(a), x(c) + off, y(b), 1.4, ink)]
        for o, c, a, b, hinge_lo, swing in self.doors:
            wd = (b - a) * S
            if o == 'h':
                hx = x(a) if hinge_lo else x(b); hy = y(c); sg = -1 if swing == 'up' else 1
                lx, ly = hx, hy + sg * wd; ax = x(b) if hinge_lo else x(a)
                sw = 1 if hinge_lo == (swing == 'up') else 0
                op += [L(hx, hy, lx, ly, 2.2, ink), P(f'M{lx:.1f} {ly:.1f} A{wd:.1f} {wd:.1f} 0 0 {sw} {ax:.1f} {hy:.1f}', 1.1, 'none', sub)]
            else:
                hx = x(c); hy = y(a) if hinge_lo else y(b); sg = -1 if swing == 'left' else 1
                lx, ly = hx + sg * wd, hy; ay = y(b) if hinge_lo else y(a)
                sw = 0 if hinge_lo == (swing == 'right') else 1
                op += [L(hx, hy, lx, ly, 2.2, ink), P(f'M{lx:.1f} {ly:.1f} A{wd:.1f} {wd:.1f} 0 0 {sw} {hx:.1f} {ay:.1f}', 1.1, 'none', sub)]
        if self.garage_door:
            a, b, yy = self.garage_door
            op += [L(x(a), y(yy) - 3, x(b), y(yy) - 3, 2, ink, 'butt'), L(x(a), y(yy) - 9, x(b), y(yy) - 9, 1, sub, 'butt')]
        fx = self._fixtures(x, y, S, ink, sub)
        from .draw import dashed as _dash
        for kind, ex, ey, ew, eh, lbl in self.extras:
            tg.insert(0, R(x(ex), y(ey), ew * S, eh * S, 0, (fills or {}).get('porch', tint), 'none'))
            if kind == 'porch':
                for (a1, b1, a2, b2) in [(ex, ey, ex + ew, ey), (ex + ew, ey, ex + ew, ey + eh), (ex + ew, ey + eh, ex, ey + eh), (ex, ey + eh, ex, ey)]:
                    fx.append(_dash(x(a1), y(b1), x(a2), y(b2), sub, 10, 8, 1.6))
                for cx_, cy_ in [(ex + 0.6, ey + eh - 0.6), (ex + ew - 0.6, ey + eh - 0.6)] + ([(ex + ew / 2, ey + eh - 0.6)] if ew > 20 else []):
                    fx.append(R(x(cx_) - S * 0.4, y(cy_) - S * 0.4, S * 0.8, S * 0.8, 1.6, 'none', ink))
            else:
                step = 3
                for k in range(1, int(ew / step)): fx.append(L(x(ex + k * step), y(ey + 1), x(ex + k * step), y(ey + eh - 1), 0.8, sub, 'butt'))
                for k in range(1, int(eh / step)): fx.append(L(x(ex + 1), y(ey + k * step), x(ex + ew - 1), y(ey + k * step), 0.8, sub, 'butt'))
                fx.append(C(x(ex + ew / 2), y(ey + eh / 2), 4.5 * S, 2, 'none', ink)); fx.append(C(x(ex + ew / 2), y(ey + eh / 2), 0.6 * S, 1.6, 'none', ink))
            lab_y = y(ey + eh / 2) + (6.2 * S if kind == 'court' else 6)
            self._extra_labels = getattr(self, '_extra_labels', []) + [T(x(ex + ew / 2), lab_y if kind == 'court' else y(ey + eh / 2) + 7, lbl, max(14, min(20, S * 0.6)), color=sub, w=700, ls=3)]
        lab = []; fs = max(15, min(24, S * 0.7))
        for rm in self.rooms:
            if rm.kind == 'hall': continue
            cx = x(rm.x + rm.w / 2)
            cy = {'bed': rm.y + rm.h * 0.68, 'living': rm.y + rm.h * 0.32, 'kitchen': rm.y + rm.h * 0.5, 'dining': rm.y + rm.h * 0.5 - 3.4}.get(rm.kind, rm.y + rm.h / 2)
            if rm.kind == 'kitchen': cy = rm.y + (3.4 if not self._kitchen_top(rm) else rm.h - 3.0)
            nm = rm.name if rm.w * S > len(rm.name) * fs * 0.72 else rm.name.split(' ')[-1] if rm.name.startswith('PRIMARY') else rm.name.split(' ')[0]
            lab.append(T(cx, y(cy), nm, fs, color=ink, w=700, ls=2))
            if rm.kind in ('bed', 'living', 'kitchen', 'garage') and rm.w >= 9:
                lab.append(T(cx, y(cy) + fs * 1.15, f"{fmt_ft(rm.w)} × {fmt_ft(rm.h)}", fs * 0.68, color=sub, w=500, ls=1))
        lab += getattr(self, '_extra_labels', []); self._extra_labels = []
        dims = [dimH(x(0), x(W), y(0) - 34, fmt_ft(W), sub), dimV(x(0) - 34, y(0), y(D), fmt_ft(D), sub)]
        if title:
            word = WORD.get(self.beds, str(self.beds))
            dims += [T(x(0), y(D) + 74, 'FLOOR PLAN', 26, 'start', ink, 600, 4),
                     T(x(0), y(D) + 104, f'{TYPE_NAME[self.typ]} · {word}-BEDROOM · {self.sf:,} SF', 18, 'start', sub, 500, 1.5)]
        parts = [G('tint', *tg), we, wi, G('openings', *op), G('fixtures', *fx), G('labels', *lab), G('dims', *dims)]
        return ''.join(parts)

    def _kitchen_top(self, rm):
        return not self._solid(rm, 'bottom') or abs(rm.y2 - self.D) > 1e-6 and self._solid(rm, 'top')

    def _fixtures(self, x, y, S, ink, sub):
        r = self.rng; out = []
        def rect(a, b, w, h, sw=1.8, rx=0): out.append(R(x(a), y(b), w * S, h * S, sw, 'none', ink, rx))
        def circ(a, b, rr, sw=1.4): out.append(C(x(a), y(b), rr * S, sw, 'none', ink))
        for rm in self.rooms:
            X, Y, w, h, k = rm.x, rm.y, rm.w, rm.h, rm.kind
            if k == 'bed':
                bw = 5 if (rm.name.startswith('PRIMARY') or w >= 13) else 4.5
                if w < bw + 1.5: bw = w - 1.5
                bx = X + w / 2 - bw / 2; by = Y + 0.6
                rect(bx, by, bw, 6.7, 2.2); rect(bx + 0.3, by + 0.3, bw / 2 - 0.45, 1.1, 1.3, 5); rect(bx + bw / 2 + 0.15, by + 0.3, bw / 2 - 0.45, 1.1, 1.3, 5)
                out.append(L(x(bx), y(by + 2), x(bx + bw), y(by + 2), 1.2, ink))
                if w - bw >= 5: rect(bx - 2, by, 1.6, 1.6, 1.4); rect(bx + bw + 0.4, by, 1.6, 1.6, 1.4)
            elif k == 'bath':
                tw = min(5, w - 0.6)
                rect(X + 0.3, Y + 0.3, tw, 2.6, 1.8, 4); rect(X + 0.6, Y + 0.6, tw - 0.6, 2.0, 1.1, 12)
                tx = X + w - 2
                rect(tx - 0.2, Y + h - 2.6, 1.6, 0.6, 1.5)
                out.append(P(f'M{x(tx):.1f} {y(Y + h - 2.6):.1f} C{x(tx - 0.2):.1f} {y(Y + h - 4.4):.1f} {x(tx + 1.6):.1f} {y(Y + h - 4.4):.1f} {x(tx + 1.4):.1f} {y(Y + h - 2.6):.1f}', 1.5, 'none', ink))
                if w >= 8: rect(X + 0.3, Y + h - 4.2, 1.8, 2.6, 1.5); circ(X + 1.2, Y + h - 2.9, 0.45)
            elif k == 'kitchen':
                top = self._kitchen_top(rm)
                cy = Y + 0.2 if top else Y + h - 2.2
                rect(X + 0.2, cy, w - 0.4, 2, 2)
                rect(X + w / 2 - 1.2, cy + 0.3, 2.4, 1.4, 1.3, 4)
                for ox in (1.0, 2.2):
                    for oy in (0.7, 1.5): circ(X + ox, cy + oy, 0.35)
                rect(X + w - 2.8, cy, 2.6, 2.0, 1.8)
                if w >= 11 and h >= 13:
                    iy = cy + 4.6 if top else cy - 5.0
                    rect(X + 2.5, iy, w - 5, 2.6, 1.8)
                    for i in range(3): circ(X + 3.6 + i * (w - 7.2) / 2, iy + (3.5 if top else -0.9), 0.5)
            elif k == 'dining':
                tw, th = min(6, w - 4), 3.2; tx = X + w / 2 - tw / 2; ty = Y + h / 2 - th / 2 + 0.6
                rect(tx, ty, tw, th, 1.8, 4); n = 3 if tw >= 6 else 2
                for i in range(n):
                    cxp = tx + (i + 0.5) * tw / n - 0.6; rect(cxp, ty - 1.4, 1.2, 1.0, 1.2, 3); rect(cxp, ty + th + 0.4, 1.2, 1.0, 1.2, 3)
            elif k == 'living':
                sw = min(8, w - 5); sx = X + w / 2 - sw / 2; sy = Y + h - 5.4 if h >= 12 else Y + h - 4
                rect(sx - 1, sy - 4.2, sw + 2, 7.2, 1.0, 2)  # rug
                rect(sx, sy, sw, 3, 2, 6); out.append(L(x(sx), y(sy + 0.9), x(sx + sw), y(sy + 0.9), 1.2, ink))
                rect(sx + 1.5, sy - 3.2, sw - 3, 1.9, 1.5, 4)
                if w - sw >= 7: rect(sx + sw + 0.8, sy - 3.0, 2.4, 2.4, 1.4, 4)
                if self._solid(rm, 'top'): rect(X + w / 2 - 3, Y + 0.4, 6, 1.2, 1.5)
            elif k == 'laundry':
                if w >= 5.5 and h >= 3: rect(X + 0.4, Y + 0.4, 2.3, 2.3, 1.6); circ(X + 1.55, Y + 1.55, 0.8, 1.2); rect(X + 3.0, Y + 0.4, 2.3, 2.3, 1.6); circ(X + 4.15, Y + 1.55, 0.8, 1.2)
            elif k in ('pantry', 'wic'):
                for i in range(1, 4): out.append(L(x(X + 0.3), y(Y + i * (h / 4)), x(X + 1.6), y(Y + i * (h / 4)), 1, ink))
                if k == 'wic': out.append(L(x(X + w - 1.6), y(Y + 0.6), x(X + w - 1.6), y(Y + h - 0.6), 1, ink))
            elif k == 'garage':
                for cx_ in (X + w * 0.27, X + w * 0.73):
                    rect(cx_ - 3, Y + 2.5, 6, 14.5, 1.2, 10)
        return out
