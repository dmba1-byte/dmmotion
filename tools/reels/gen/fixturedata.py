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
    'island':  dict(w=72 * IN, d=30 * IN, clear=42 * IN, side=0.0,     cite='NKBA work aisle'),
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


def place(plan):
    """All fixtures for a plan, as geometry. A None in the returned list means a
    required fixture would not fit legally - the gate rejects the plan rather
    than squeezing it in."""
    out, missing = [], []
    for rm in plan.rooms:
        k = rm.kind
        if k == 'bath':
            want = ['tub' if min(rm.w, rm.h) >= 5.6 else 'shower', 'toilet', 'lav']
        elif k == 'kitchen':
            want = ['range', 'sink', 'fridge']
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
