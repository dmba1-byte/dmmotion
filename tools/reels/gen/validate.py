"""Hard gate on plan correctness. Every rule cites a published source.

Nothing here is a judgement call about whether a plan "looks right". A plan
either satisfies these or it is rejected and regenerated.

  IRC R304.1/.2  habitable room >= 70 sq ft, no horizontal dimension under 7 ft
  IRC R310.1     every sleeping room needs an emergency escape opening
  IRC R311.6     hallway not less than 36 in wide
  IRC R307.1     water closet 15 in centreline to any wall/fixture, 21 in clear front
  IRC P2705.1    shower compartment clear of obstruction
  NKBA 2022      kitchen work aisle 42 in, landing areas at sink/range/fridge
  Circulation    a sleeping room is not reached only by passing through another
"""
from . import fixturedata as F

IN = 1.0 / 12.0


def _ovl(a, b):
    return a and b and a[0] < b[0] + b[2] and b[0] < a[0] + a[2] and a[1] < b[1] + b[3] and b[1] < a[1] + a[3]


def _room_openings(plan, rm, items):
    out = []
    for it in items:
        o, c, a, b = it[0], it[1], it[2], it[3]
        on = ((o == 'h' and (abs(c - rm.y) < .01 or abs(c - rm.y2) < .01) and a >= rm.x - .01 and b <= rm.x2 + .01)
              or (o == 'v' and (abs(c - rm.x) < .01 or abs(c - rm.x2) < .01) and a >= rm.y - .01 and b <= rm.y2 + .01))
        if on: out.append(it)
    return out


def _swing_box(d):
    """Bounding box of a door's swing quarter-circle."""
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


def _adjacency(plan):
    """Rooms joined by a door."""
    adj = {id(r): set() for r in plan.rooms}
    for d in plan.doors:
        o, c, a, b = d[0], d[1], d[2], d[3]
        touching = []
        for r in plan.rooms:
            if o == 'h' and (abs(c - r.y) < .01 or abs(c - r.y2) < .01) and a >= r.x - .01 and b <= r.x2 + .01:
                touching.append(r)
            if o == 'v' and (abs(c - r.x) < .01 or abs(c - r.x2) < .01) and a >= r.y - .01 and b <= r.y2 + .01:
                touching.append(r)
        for i in range(len(touching)):
            for j in range(i + 1, len(touching)):
                adj[id(touching[i])].add(id(touching[j])); adj[id(touching[j])].add(id(touching[i]))
    return adj


def check(plan):
    """Return [] if the plan is sound, else a list of (rule, detail)."""
    bad = []
    fixes, missing = F.place(plan)

    for rname, kind in missing:
        bad.append(('fixture fit', f'{rname}: no legal position for {kind}'))

    # R304 habitable rooms
    for rm in plan.rooms:
        if rm.kind in ('bed', 'living', 'dining'):
            if rm.w * rm.h < 70:      bad.append(('IRC R304.1', f'{rm.name} is {rm.w*rm.h:.0f} sq ft, under 70'))
            if min(rm.w, rm.h) < 7:   bad.append(('IRC R304.2', f'{rm.name} is {min(rm.w,rm.h):.1f} ft across, under 7'))
        if rm.kind == 'hall' and min(rm.w, rm.h) < 3:
            bad.append(('IRC R311.6', f'hallway {min(rm.w,rm.h)*12:.0f} in wide, under 36'))

    # R310 egress from every sleeping room
    for rm in plan.rooms:
        if rm.kind != 'bed': continue
        wins = _room_openings(plan, rm, plan.windows)
        if not wins:
            bad.append(('IRC R310.1', f'{rm.name} has no emergency escape opening'))
        elif max(w[3] - w[2] for w in wins) < 20 * IN:
            bad.append(('IRC R310.2.1', f'{rm.name} escape opening under 20 in clear width'))
        if not _room_openings(plan, rm, plan.doors):
            bad.append(('access', f'{rm.name} has no door'))

    # fixture clearances vs door swings and each other
    swings = [(_swing_box(d), d) for d in plan.doors]
    for f in fixes:
        for sb, d in swings:
            if _ovl(f.clear, sb) or _ovl((f.x, f.y, f.w, f.h), sb):
                bad.append((f.cite, f'{f.room} {f.kind} fouls a door swing'))
                break
    for i, a in enumerate(fixes):
        for b in fixes[i + 1:]:
            if a.room != b.room: continue
            if _ovl((a.x, a.y, a.w, a.h), (b.x, b.y, b.w, b.h)):
                bad.append((a.cite, f'{a.room}: {a.kind} and {b.kind} overlap'))
            elif _ovl(a.clear, (b.x, b.y, b.w, b.h)) or _ovl(b.clear, (a.x, a.y, a.w, a.h)):
                bad.append((a.cite, f'{a.room}: {a.kind} clearance blocked by {b.kind}'))

    # doors must not swing into each other
    for i in range(len(plan.doors)):
        for j in range(i + 1, len(plan.doors)):
            if _ovl(_swing_box(plan.doors[i]), _swing_box(plan.doors[j])):
                bad.append(('door swing', 'two doors swing into the same space'))

    # glazing must not sit on a door
    for w in plan.windows:
        for d in plan.doors:
            if w[0] == d[0] and abs(w[1] - d[1]) < .01 and min(w[3], d[3]) - max(w[2], d[2]) > 0.05:
                bad.append(('opening conflict', 'window placed over a door'))

    # circulation: no sleeping room reached only through another sleeping room
    adj = _adjacency(plan)
    beds = [r for r in plan.rooms if r.kind == 'bed']
    public = [r for r in plan.rooms if r.kind in ('living', 'hall', 'foyer', 'dining', 'kitchen')]
    if public:
        for b in beds:
            seen, stack, ok = set(), [id(b)], False
            while stack:
                n = stack.pop()
                if n in seen: continue
                seen.add(n)
                if n in (id(r) for r in public): ok = True; break
                for m in adj[n]:
                    if m == id(b) or m not in (id(x) for x in beds): stack.append(m)
            if not ok:
                bad.append(('circulation', f'{b.name} is only reachable through another bedroom'))

    seen = set(); uniq = []
    for r in bad:
        if r not in seen: seen.add(r); uniq.append(r)
    return uniq


class PlanRejected(Exception):
    """Raised when no seed produces a code-compliant plan."""


def build_validated(plan_cls, seed, typ, tries=200):
    """The gate. Returns the first plan that passes every rule, or raises.

    Deliberately loud: if a plan type cannot produce a compliant layout, that
    must stop the pipeline rather than quietly ship a plan that does not work.
    """
    first = None
    for i in range(tries):
        try: p = plan_cls(seed + i * 7919, typ).build()
        except Exception: continue
        bad = check(p)
        if not bad: return p
        if first is None: first = bad
    raise PlanRejected(f'{typ}: no compliant layout in {tries} seeds; '
                       f'first failure: {first[:3]}')
