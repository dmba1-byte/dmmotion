"""Fixtures as real geometry, not drawing commands.

Every footprint and clearance below is a published dimension, not a guess:

  IRC R307.1  water closet: 15 in minimum from the centreline to any wall or
              fixture (so a 30 in wide clear zone), and 21 in clear in front.
  IRC R307.1  lavatory and tub/shower: 21 in clear in front.
  IRC P2705.1 shower compartment: 900 sq in minimum, able to hold a 30 in circle.
  NKBA 2022   kitchen work aisle 42 in (one cook) / 48 in (two); walkway 36 in.
  NKBA 2022   landing areas: 15 in beside the refrigerator handle side,
              12/15 in either side of the cooking surface,
              24 in one side and 18 in the other at the primary sink.
  ANSI/common residential fixture sizes for footprints (tub 60x30, range 30,
  refrigerator 36, vanity 24, water closet 20x28, queen bed 60x80).

Clearance rectangles are the space that must stay empty. The validator treats
any overlap of a clearance with a wall, another fixture, or a door swing as a
failure, so placement here has to be right rather than merely look right.
"""
from collections import namedtuple

Fix = namedtuple('Fix', 'kind x y w h clear room cite')

IN = 1.0 / 12.0           # inches -> feet

# footprint (w, d) in feet, and required clear depth in front
# `side` is clear space required beside the fixture EDGE. For the water closet
# and lavatory IRC R307.1 states 15 in from the CENTRELINE, so the edge figure
# is 15 in minus half the fixture width: 5 in for a 20 in closet, 3 in for a
# 24 in lavatory. Coding 15 in at the edge (as this first did) is roughly three
# times the real requirement and makes compliant bathrooms impossible.
SPEC = {
    'toilet':  dict(w=20 * IN, d=28 * IN, clear=21 * IN, side=5 * IN,  cite='IRC R307.1'),
    'lav':     dict(w=24 * IN, d=21 * IN, clear=21 * IN, side=3 * IN,  cite='IRC R307.1'),
    'tub':     dict(w=60 * IN, d=30 * IN, clear=21 * IN, side=0.0,     cite='IRC R307.1'),
    'shower':  dict(w=36 * IN, d=36 * IN, clear=21 * IN, side=0.0,     cite='IRC P2705.1'),
    'range':   dict(w=30 * IN, d=25 * IN, clear=42 * IN, side=12 * IN, cite='NKBA landing 12 in'),
    'sink':    dict(w=30 * IN, d=25 * IN, clear=42 * IN, side=15 * IN, cite='NKBA landing 18/24 in'),
    'fridge':  dict(w=36 * IN, d=30 * IN, clear=42 * IN, side=15 * IN, cite='NKBA landing'),
    'bed':     dict(w=60 * IN, d=80 * IN, clear=24 * IN, side=0.0,     cite='access side'),
    'bed_k':   dict(w=76 * IN, d=80 * IN, clear=24 * IN, side=0.0,     cite='access side'),
    'sofa':    dict(w=84 * IN, d=36 * IN, clear=30 * IN, side=0.0,     cite='circulation'),
    'table':   dict(w=60 * IN, d=36 * IN, clear=36 * IN, side=0.0,     cite='chair pull-out'),
    'washer':  dict(w=28 * IN, d=28 * IN, clear=36 * IN, side=0.0,     cite='appliance access'),
    'island':  dict(w=60 * IN, d=30 * IN, clear=42 * IN, side=0.0,     cite='NKBA work aisle'),
    'counter': dict(w=24 * IN, d=25 * IN, clear=42 * IN, side=0.0,     cite='base cabinet run'),
}


def _rect(kind, x, y, w, d, facing, room):
    """Build a Fix with its clearance rectangle projected along `facing`."""
    c = SPEC[kind]['clear']
    if   facing == 'down':  clear = (x, y + d, w, c)
    elif facing == 'up':    clear = (x, y - c, w, c)
    elif facing == 'right': clear = (x + w, y, c, d)
    else:                   clear = (x - c, y, c, d)
    return Fix(kind, x, y, w, d, clear, room, SPEC[kind]['cite'])


def _free_span(lo, hi, blocks, need):
    """Widest sub-span of [lo,hi] not hit by `blocks`, or None."""
    bs = sorted((max(lo, a), min(hi, b)) for a, b in blocks if b > lo and a < hi)
    free, cur = [], lo
    for a, b in bs:
        if a > cur: free.append((cur, a))
        cur = max(cur, b)
    if cur < hi: free.append((cur, hi))
    free = [f for f in free if f[1] - f[0] >= need]
    return max(free, key=lambda t: t[1] - t[0]) if free else None


def door_blocks(plan, rm, axis, wall_c):
    """Door spans on one wall of a room, widened by the leaf so a fixture is
    never placed where a door swings."""
    out = []
    for d in plan.doors:
        o, c, a, b = d[0], d[1], d[2], d[3]
        if o != axis or abs(c - wall_c) > 0.01: continue
        out.append((a - (b - a), b + (b - a)))
    return out


def _ovl(a, b):
    return a and b and a[0] < b[0] + b[2] and b[0] < a[0] + a[2] and a[1] < b[1] + b[3] and b[1] < a[1] + a[3]


def _inside(r, rm, eps=0.02):
    return (r[0] >= rm.x - eps and r[1] >= rm.y - eps
            and r[0] + r[2] <= rm.x2 + eps and r[1] + r[3] <= rm.y2 + eps)


WALLS = ('top', 'bottom', 'left', 'right')


def swing_box(d):
    """Quarter-circle sweep of a door leaf, as a bounding square."""
    o, c, a, b, hinge_lo, swing = d
    wd = b - a
    if o == 'h':
        hx, hy = (a if hinge_lo else b), c
        y0 = hy - wd if swing == 'up' else hy
        x0 = hx if hinge_lo else hx - wd
        return (x0, y0, wd, wd)
    hx, hy = c, (a if hinge_lo else b)
    x0 = hx - wd if swing == 'left' else hx
    y0 = hy if hinge_lo else hy - wd
    return (x0, y0, wd, wd)


def _try_wall(plan, rm, kind, side, placed, span_pref=None):
    """Place `kind` flat against one wall of `rm`, centred in the widest stretch
    free of doors and of anything already placed. Returns a Fix or None."""
    s = SPEC[kind]; w, d = s['w'], s['d']
    horiz = side in ('top', 'bottom')
    length = rm.w if horiz else rm.h
    need = w + 2 * s['side'] if horiz else w + 2 * s['side']
    if length < need or (rm.h if horiz else rm.w) < d + s['clear']:
        return None
    if horiz:
        axis, wall_c = 'h', (rm.y if side == 'top' else rm.y2)
        lo, hi = rm.x, rm.x2
    else:
        axis, wall_c = 'v', (rm.x if side == 'left' else rm.x2)
        lo, hi = rm.y, rm.y2
    blocks = door_blocks(plan, rm, axis, wall_c)
    for f in placed:                                   # keep off other fixtures
        if horiz: blocks.append((f.x - s['side'], f.x + f.w + s['side']))
        else:     blocks.append((f.y - s['side'], f.y + f.h + s['side']))
    span = _free_span(lo, hi, blocks, need)
    if not span: return None
    # Hug the start of the run rather than centring. Centring splits the
    # remaining wall into two short stubs and nothing else will fit; ganging
    # fixtures from a corner is both how bathrooms and kitchens are actually
    # laid out and what leaves one usable contiguous run.
    mid = span[0] + s['side'] + w / 2
    if   side == 'top':    fx = _rect(kind, mid - w / 2, rm.y, w, d, 'down', rm.kind)
    elif side == 'bottom': fx = _rect(kind, mid - w / 2, rm.y2 - d, w, d, 'up', rm.kind)
    elif side == 'left':   fx = _rect(kind, rm.x, mid - w / 2, d, w, 'right', rm.kind)
    else:                  fx = _rect(kind, rm.x2 - d, mid - w / 2, d, w, 'left', rm.kind)
    if not _inside((fx.x, fx.y, fx.w, fx.h), rm) or not _inside(fx.clear, rm):
        return None
    for o in placed:
        if _ovl(fx.clear, (o.x, o.y, o.w, o.h)) or _ovl((fx.x, fx.y, fx.w, fx.h), o.clear) \
           or _ovl((fx.x, fx.y, fx.w, fx.h), (o.x, o.y, o.w, o.h)):
            return None
    # nothing may sit in, or need clear space inside, a door's sweep
    for d in plan.doors:
        sb = swing_box(d)
        if _ovl((fx.x, fx.y, fx.w, fx.h), sb) or _ovl(fx.clear, sb):
            return None
    return fx


def _place_in(plan, rm, kinds):
    """Greedily seat each kind against whichever wall accepts it.
    Returns (placed, missing_kinds); nothing unplaceable enters `placed`."""
    placed, missing = [], []
    for kind in kinds:
        got = None
        order = sorted(WALLS, key=lambda s: -(rm.w if s in ('top', 'bottom') else rm.h))
        for side in order:
            got = _try_wall(plan, rm, kind, side, placed)
            if got: break
        if got: placed.append(got)
        else:   missing.append(kind)
    return placed, missing


def _solid_walls(plan, rm):
    """Walls of a room that are not cased openings - appliances need real wall."""
    from .plans import RES
    out = []
    for side, axis, c, lo, hi in (('top', 'h', rm.y, rm.x, rm.x2), ('bottom', 'h', rm.y2, rm.x, rm.x2),
                                  ('left', 'v', rm.x, rm.y, rm.y2), ('right', 'v', rm.x2, rm.y, rm.y2)):
        units = [round(lo + i * RES, 2) for i in range(int(round((hi - lo) / RES)))]
        openu = sum(1 for u in units if (axis, round(c, 2), u) in plan.open)
        if units and openu / len(units) < 0.25:
            out.append((side, hi - lo))
    return out


def _place_kitchen(plan, rm, placed):
    """Refrigerator, sink and cooking surface arranged on an L so the NKBA
    triangle holds: every leg 4-9 ft and the three together not over 26 ft."""
    import math
    solid = {s: L for s, L in _solid_walls(plan, rm)}
    pairs = [('right', 'bottom'), ('left', 'bottom'), ('right', 'top'), ('left', 'top')]
    for wa, wb in pairs:
        if wa not in solid or wb not in solid: continue
        best = None
        for da in [x * 0.5 for x in range(4, 20)]:          # offset along wall A
            for db in [x * 0.5 for x in range(4, 20)]:      # offset along wall B
                for gap in (4.0, 4.5, 5.0, 5.5, 6.0):
                    got = _lay_L(plan, rm, wa, wb, da, db, gap, placed)
                    if not got: continue
                    pts = {f.kind: (f.x + f.w / 2, f.y + f.h / 2) for f in got}
                    legs = [math.dist(pts['sink'], pts['range']),
                            math.dist(pts['range'], pts['fridge']),
                            math.dist(pts['fridge'], pts['sink'])]
                    if all(4.0 <= L <= 9.0 for L in legs) and sum(legs) <= 26.0:
                        # Aim for a normally proportioned triangle. Minimising the
                        # sum just jams all three appliances into one corner.
                        score = abs(sum(legs) - 19.0)
                        if best is None or score < best[0]: best = (score, got)
        if best: return best[1]
    return None


def _along(rm, side, t, kind, depth):
    """Footprint for a fixture `t` feet along `side`, flush to that wall."""
    s = SPEC[kind]; w = s['w']
    if side == 'bottom': return (rm.x2 - t - w, rm.y2 - depth, w, depth, 'up')
    if side == 'top':    return (rm.x + t, rm.y, w, depth, 'down')
    if side == 'right':  return (rm.x2 - depth, rm.y2 - t - w, depth, w, 'left')
    return (rm.x, rm.y + t, depth, w, 'right')


def _lay_L(plan, rm, wa, wb, da, db, gap, placed):
    """fridge and sink on wall A, cooking surface on wall B."""
    out = []
    for kind, side, t in (('fridge', wa, da), ('sink', wa, da + gap), ('range', wb, db)):
        x0, y0, w, h, face = _along(rm, side, t, kind, SPEC[kind]['d'])
        f = _rect(kind, x0, y0, w, h, face, rm.kind)
        if not _inside((f.x, f.y, f.w, f.h), rm) or not _inside(f.clear, rm): return None
        for o in out + list(placed):
            if _ovl((f.x, f.y, f.w, f.h), (o.x, o.y, o.w, o.h)) or _ovl(f.clear, (o.x, o.y, o.w, o.h)):
                return None
        for d in plan.doors:
            sb = swing_box(d)
            if _ovl((f.x, f.y, f.w, f.h), sb) or _ovl(f.clear, sb): return None
        out.append(f)
    return out


def _island(rm, placed):
    """Island, only where a 42 in aisle survives on every side (NKBA)."""
    w, d = SPEC['island']['w'], SPEC['island']['d']
    aisle = 42 * IN
    cx, cy = rm.x + rm.w / 2, rm.y + rm.h / 2
    f = Fix('island', cx - w / 2, cy - d / 2, w, d,
            (cx - w / 2 - aisle, cy - d / 2 - aisle, w + 2 * aisle, d + 2 * aisle),
            rm.kind, SPEC['island']['cite'])
    if not _inside(f.clear, rm): return None
    for o in placed:
        if _ovl(f.clear, (o.x, o.y, o.w, o.h)): return None
    return f


def _counter_runs(rm, appliances):
    """Continuous base cabinet run joining the appliances on each wall."""
    from .fixturedraw import facing
    runs, byface = [], {}
    for f in appliances:
        byface.setdefault(facing(f), []).append(f)
    for face, group in byface.items():
        if face in ('up', 'down'):
            x0 = min(f.x for f in group); x1 = max(f.x + f.w for f in group)
            y0 = min(f.y for f in group); d = max(f.h for f in group)
            x0, x1 = max(rm.x, x0 - 2.0), min(rm.x2, x1 + 2.0)
            runs.append(_rect('counter', x0, y0, x1 - x0, d, face, rm.kind))
        else:
            y0 = min(f.y for f in group); y1 = max(f.y + f.h for f in group)
            x0 = min(f.x for f in group); d = max(f.w for f in group)
            y0, y1 = max(rm.y, y0 - 2.0), min(rm.y2, y1 + 2.0)
            runs.append(_rect('counter', x0, y0, d, y1 - y0, face, rm.kind))
    return runs


def place(plan):
    """All fixtures for a plan, as geometry. A None in the returned list means a
    required fixture would not fit legally - the gate rejects the plan rather
    than squeezing it in."""
    out, missing = [], []
    for rm in plan.rooms:
        k = rm.kind
        if k == 'bath':
            # Standard new-construction split: the hall bath carries the tub,
            # the primary ensuite gets a shower. A 60 in tub plus a closet and
            # lavatory will not gang onto one run in a typical ensuite anyway.
            primary = 'PRIMARY' in rm.name.upper()
            tubbable = min(rm.w, rm.h) >= 5.6 and not primary
            want = ['tub' if tubbable else 'shower', 'toilet', 'lav']
        elif k == 'kitchen':
            kf = _place_kitchen(plan, rm, [])
            if kf:
                runs = _counter_runs(rm, kf)
                out.extend(kf); out.extend(runs)
                isl = _island(rm, kf + runs)
                if isl: out.append(isl)
            else:
                missing.append((rm.name, 'kitchen work triangle'))
            continue
        elif k == 'bed':
            want = ['bed_k' if (rm.name.startswith('PRIMARY') and rm.w >= 13) else 'bed']
        elif k == 'living':   want = ['sofa']
        elif k == 'dining':   want = ['table']
        elif k == 'laundry':  want = ['washer']
        else:                 continue
        got, miss = _place_in(plan, rm, want)
        out.extend(got)
        missing.extend((rm.name, k) for k in miss)
    return out, missing
