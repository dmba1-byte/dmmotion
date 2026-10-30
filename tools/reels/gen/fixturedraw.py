"""Draw fixtures from fixturedata geometry, at real sizes.

The previous renderer sized furniture as a function of room width - a sofa was
min(8, w-5) feet, a tub min(5, w-0.6) - so the same object changed size from
plan to plan and nothing read at a consistent scale. Everything here is drawn
from the Fix rectangle, whose dimensions come from published fixture sizes.
"""
from .draw import L, R, C, P

EPS = 0.01


def facing(f):
    """Which way the fixture faces, recovered from its clearance rectangle."""
    cx, cy, cw, ch = f.clear
    if cy >= f.y + f.h - EPS: return 'down'
    if cy + ch <= f.y + EPS:  return 'up'
    if cx >= f.x + f.w - EPS: return 'right'
    return 'left'


def _mk(x, y, S, ink, sub):
    def rect(a, b, w, h, sw=1.8, rx=0, c=None):
        return R(x(a), y(b), w * S, h * S, sw, 'none', c or ink, rx)
    def circ(a, b, r, sw=1.4, c=None):
        return C(x(a), y(b), r * S, sw, 'none', c or ink)
    def line(a, b, a2, b2, sw=1.2, c=None):
        return L(x(a), y(b), x(a2), y(b2), sw, c or ink)
    return rect, circ, line


def _bed(f, x, y, S, ink, sub):
    rect, circ, line = _mk(x, y, S, ink, sub)
    fc = facing(f); out = [rect(f.x, f.y, f.w, f.h, 2.2, 2)]
    # pillows along the head wall (opposite the clear side)
    if fc in ('down', 'up'):
        hy = f.y + 0.35 if fc == 'down' else f.y + f.h - 1.45
        pw = (f.w - 0.9) / 2
        out += [rect(f.x + 0.3, hy, pw, 1.1, 1.3, 5), rect(f.x + 0.6 + pw, hy, pw, 1.1, 1.3, 5)]
        ty = f.y + 2.1 if fc == 'down' else f.y + f.h - 2.1
        out.append(line(f.x, ty, f.x + f.w, ty))
    else:
        hx = f.x + 0.35 if fc == 'right' else f.x + f.w - 1.45
        ph = (f.h - 0.9) / 2
        out += [rect(hx, f.y + 0.3, 1.1, ph, 1.3, 5), rect(hx, f.y + 0.6 + ph, 1.1, ph, 1.3, 5)]
        tx = f.x + 2.1 if fc == 'right' else f.x + f.w - 2.1
        out.append(line(tx, f.y, tx, f.y + f.h))
    return out


def _sofa(f, x, y, S, ink, sub):
    rect, circ, line = _mk(x, y, S, ink, sub)
    fc = facing(f); out = [rect(f.x, f.y, f.w, f.h, 2, 6)]
    if fc == 'down':    out.append(line(f.x, f.y + 0.75, f.x + f.w, f.y + 0.75))
    elif fc == 'up':    out.append(line(f.x, f.y + f.h - 0.75, f.x + f.w, f.y + f.h - 0.75))
    elif fc == 'right': out.append(line(f.x + 0.75, f.y, f.x + 0.75, f.y + f.h))
    else:               out.append(line(f.x + f.w - 0.75, f.y, f.x + f.w - 0.75, f.y + f.h))
    return out


def _table(f, x, y, S, ink, sub):
    rect, circ, line = _mk(x, y, S, ink, sub)
    out = [rect(f.x, f.y, f.w, f.h, 1.8, 4)]
    n = max(2, int(f.w / 2.0))
    for i in range(n):
        cx = f.x + (i + 0.5) * f.w / n - 0.6
        out += [rect(cx, f.y - 1.3, 1.2, 1.0, 1.2, 3), rect(cx, f.y + f.h + 0.3, 1.2, 1.0, 1.2, 3)]
    return out


def _toilet(f, x, y, S, ink, sub):
    rect, circ, line = _mk(x, y, S, ink, sub)
    fc = facing(f)
    if fc in ('down', 'up'):
        tank_y = f.y if fc == 'down' else f.y + f.h - 0.58
        out = [rect(f.x, tank_y, f.w, 0.58, 1.5)]
        by = f.y + 0.58 if fc == 'down' else f.y
        out.append(rect(f.x + 0.12, by, f.w - 0.24, f.h - 0.58, 1.5, 9))
    else:
        tank_x = f.x if fc == 'right' else f.x + f.w - 0.58
        out = [rect(tank_x, f.y, 0.58, f.h, 1.5)]
        bx = f.x + 0.58 if fc == 'right' else f.x
        out.append(rect(bx, f.y + 0.12, f.w - 0.58, f.h - 0.24, 1.5, 9))
    return out


def _lav(f, x, y, S, ink, sub):
    rect, circ, line = _mk(x, y, S, ink, sub)
    return [rect(f.x, f.y, f.w, f.h, 1.6),
            circ(f.x + f.w / 2, f.y + f.h / 2, min(f.w, f.h) * 0.28, 1.2)]


def _tub(f, x, y, S, ink, sub):
    rect, circ, line = _mk(x, y, S, ink, sub)
    return [rect(f.x, f.y, f.w, f.h, 1.8, 4),
            rect(f.x + 0.3, f.y + 0.3, f.w - 0.6, f.h - 0.6, 1.1, 10)]


def _shower(f, x, y, S, ink, sub):
    rect, circ, line = _mk(x, y, S, ink, sub)
    return [rect(f.x, f.y, f.w, f.h, 1.8),
            line(f.x, f.y, f.x + f.w, f.y + f.h, 1.0, sub),
            circ(f.x + f.w / 2, f.y + f.h / 2, 0.22, 1.1)]


def _range(f, x, y, S, ink, sub):
    rect, circ, line = _mk(x, y, S, ink, sub)
    out = [rect(f.x, f.y, f.w, f.h, 1.8)]
    for dx in (0.28, 0.72):
        for dy in (0.3, 0.7):
            out.append(circ(f.x + f.w * dx, f.y + f.h * dy, 0.3, 1.2))
    return out


def _sink(f, x, y, S, ink, sub):
    rect, circ, line = _mk(x, y, S, ink, sub)
    return [rect(f.x, f.y, f.w, f.h, 1.8),
            rect(f.x + 0.2, f.y + 0.3, f.w - 0.4, f.h - 0.6, 1.2, 3),
            circ(f.x + f.w / 2, f.y + f.h / 2, 0.16, 1.0)]


def _fridge(f, x, y, S, ink, sub):
    rect, circ, line = _mk(x, y, S, ink, sub)
    fc = facing(f); out = [rect(f.x, f.y, f.w, f.h, 1.8)]
    if fc in ('down', 'up'):
        out.append(line(f.x + f.w / 2, f.y, f.x + f.w / 2, f.y + f.h, 1.1))
    else:
        out.append(line(f.x, f.y + f.h / 2, f.x + f.w, f.y + f.h / 2, 1.1))
    return out


def _washer(f, x, y, S, ink, sub):
    rect, circ, line = _mk(x, y, S, ink, sub)
    return [rect(f.x, f.y, f.w, f.h, 1.6), circ(f.x + f.w / 2, f.y + f.h / 2, min(f.w, f.h) * 0.33, 1.2)]


def _island(f, x, y, S, ink, sub):
    rect, circ, line = _mk(x, y, S, ink, sub)
    return [rect(f.x, f.y, f.w, f.h, 1.8)]


DRAW = {'bed': _bed, 'bed_k': _bed, 'sofa': _sofa, 'table': _table, 'toilet': _toilet,
        'lav': _lav, 'tub': _tub, 'shower': _shower, 'range': _range, 'sink': _sink,
        'fridge': _fridge, 'washer': _washer, 'island': _island}


def draw(fixes, x, y, S, ink, sub):
    out = []
    for f in fixes:
        fn = DRAW.get(f.kind)
        if fn: out += fn(f, x, y, S, ink, sub)
    return out
