import sys
sys.path.insert(0, '/home/claude/reels')
from gen.plans import Plan, TYPE_NAME
from gen.elevs import make as make_elev
from gen.elev_site import site as make_site
from gen.engine2 import STYLES, prefix_ids
from gen import figs as F
from gen import elevs as EV

def _plan(seed, typ, st):
    p = Plan(seed, typ).build()
    svg = p.svg(st['ink'], st['sub'], st['tint'], fills=st.get('fills'))
    return p, svg

def plan_sched(pre, t0, scale=1.0):
    s = lambda a: round(t0 + a * scale, 2)
    return {f'{pre}walls-ext': (s(0), s(2.4), 'seq'), f'{pre}walls-int': (s(2.2), s(4.2), 'seq'), f'{pre}openings': (s(4.0), s(6.0), 0.35),
            f'{pre}fixtures': (s(5.8), s(8.6), 0.3), f'{pre}labels': (s(8.4), s(9.6), 0.4), f'{pre}dims': (s(9.4), s(10.4), 0.4)}

def job_draw(name, seed, typ, style, hook, sub, cta):
    st = STYLES[style]; p, svg = _plan(seed, typ, st); svg = prefix_ids(svg, 'p_')
    return dict(name=name, style=style, hook=hook, sub=sub, cta=cta, end=12.0, sched=plan_sched('p_', 0.05), timer=[0.05, 10.5],
                figs=F.plan_figs(p, 'Lp', (9.4, 11.6), (9.2, 9.6)),
                layers=[{'id': 'Lp', 'svg': svg}], layers_meta=[], tint_windows=[['p_tint', 7.8, 9.0]]), p

def job_tour(name, seed, typ, style, hook, sub, cta):
    st = STYLES[style]; p, svg = _plan(seed, typ, st); svg = prefix_ids(svg, 'p_')
    rooms = sorted([r for r in p.rooms if r.kind in ('kitchen', 'living', 'bed')], key=lambda r: -r.w * r.h)[:2]
    def c(rm): return (p.X0 + (rm.x + rm.w / 2) * p.S, p.Y0 + (rm.y + rm.h / 2) * p.S)
    a, b = c(rooms[0]), c(rooms[1]); z = min(2.1, 720 / (max(rooms[0].w, rooms[0].h) * p.S))
    cam = [[0, 1, 540, 960], [9.4, 1, 540, 960], [10.4, z, *a], [11.2, z, *a], [12.2, z, *b], [12.9, z, *b], [13.7, 1, 540, 960]]
    return dict(name=name, style=style, hook=hook, sub=sub, cta=cta, end=14.0, hook_out=9.2, sched=plan_sched('p_', 0.05, 0.9), timer=[0.05, 9.4],
                figs=F.plan_figs(p, 'Lp', (8.9, 12.6), (8.6, 9.0)),
                layers=[{'id': 'Lp', 'svg': svg}], layers_meta=[{'id': 'Lp', 'cam': cam}], tint_windows=[['p_tint', 7.4, 8.4]]), p

def job_pop3d(name, seed, typ, style, hook, sub, cta):
    st = STYLES[style]; p, svg = _plan(seed, typ, st); svg = prefix_ids(svg, 'p_')
    segs = p.walls(); Hh = 8.5; walls = []
    for ext, lst in segs.items():
        for o, c, a, b in lst:
            x1, y1, x2, y2 = (a, c, b, c) if o == 'h' else (c, a, c, b); walls.append([x1, y1, x2, y2, 0, Hh, 1 if ext else 0])
    for o, c, a, b in p.windows:
        x1, y1, x2, y2 = (a, c, b, c) if o == 'h' else (c, a, c, b); walls += [[x1, y1, x2, y2, 0, 3, 1], [x1, y1, x2, y2, 7, Hh, 1]]
    for o, c, a, b, *_ in p.doors:
        x1, y1, x2, y2 = (a, c, b, c) if o == 'h' else (c, a, c, b); walls.append([x1, y1, x2, y2, 7, Hh, 0])
    fills = st.get('fills') or {}
    rooms = [[r.x, r.y, r.w, r.h, fills.get(r.kind, st['tint'])] for r in p.rooms] + [[e[1], e[2], e[3], e[4], st['tint2']] for e in p.extras]
    W, D = p.W, p.D; k = min(880 / ((W + D) * 0.866), 820 / ((W + D) * 0.5 + Hh))
    ox = 540 - (W - D) / 2 * k * 0.866; oy = 1010 - (W + D) * k * 0.25 + Hh * k / 2
    iso = dict(walls=walls, rooms=rooms, S=p.S, X0=p.X0, Y0=p.Y0, k=k, ox=ox, oy=oy, H=Hh, tilt=[6.6, 8.0], rise=[8.0, 9.8])
    sched = plan_sched('p_', 0.05, 0.6)
    return dict(name=name, style=style, hook=hook, sub=sub, cta=cta, end=11.8, sched=sched, iso=iso, timer=[0.05, 9.8],
                layers=[{'id': 'Lp', 'svg': svg}], layers_meta=[{'id': 'Lp', 'op': [[0, 1], [6.5, 1], [6.9, 0]]}], tint_windows=[['p_tint', 4.6, 5.6]]), p

def job_site2plan(name, seed, typ, style, hook, sub, cta):
    st = STYLES[style]
    ssvg, order = make_site(seed, st['ink'], st['sub'], st['tint'], st['lawn'], st['road']); ssvg = prefix_ids(ssvg, 's_')
    p, psvg = _plan(seed, typ, st); psvg = prefix_ids(psvg, 'p_')
    import re
    m = re.search(r'id="s_house"><line x1="([\d.]+)" y1="([\d.]+)" x2="([\d.]+)"', ssvg); hx1, hy1, hx2 = map(float, m.groups())
    m2 = re.search(r'id="s_house">(?:<line[^>]+>){1}<line x1="[\d.]+" y1="[\d.]+" x2="[\d.]+" y2="([\d.]+)"', ssvg); hy2 = float(m2.group(1))
    cx, cy = (hx1 + hx2) / 2, (hy1 + hy2) / 2; z = min(4, 820 / (hx2 - hx1))
    ss = {'s_lot': (0.3, 1.4, 'seq'), 's_setbacks': (1.2, 2.2, 0.12), 's_street': (1.8, 2.6, 0.4), 's_house': (2.4, 3.6, 0.3), 's_hardscape': (3.4, 4.4, 0.3),
          's_trees': (4.0, 5.2, 0.25), 's_north': (5.0, 5.4, 0.3), 's_labels': (5.2, 5.8, 0.3), 's_dims': (5.4, 5.9, 0.3)}
    ss.update(plan_sched('p_', 7.0, 0.42))
    meta = [{'id': 'Ls', 'cam': [[0, 1, 540, 960], [5.9, 1, 540, 960], [7.2, z, cx, cy]], 'op': [[0, 1], [6.5, 1], [7.1, 0]]},
            {'id': 'Lp', 'op': [[0, 0], [6.8, 0], [7.1, 1]], 'cam': [[0, 0.7, 540, 960], [6.8, 0.7, 540, 960], [7.4, 1, 540, 960]]}]
    return dict(name=name, style=style, hook=hook, sub=sub, cta=cta, end=12.6, hook_out=5.8, sched=ss, timer=[0.05, 11.1],
                figs=F.plan_figs(p, 'Lp', (10.6, 12.4), (10.4, 10.8)),
                layers=[{'id': 'Ls', 'svg': ssvg}, {'id': 'Lp', 'svg': psvg, 'op0': 0}], layers_meta=meta,
                tint_windows=[['s_tint', 3.8, 4.8], ['p_tint', 10.0, 10.8]]), p

def job_elev(name, seed, kind, style, hook, sub, cta):
    st = STYLES[style]; svg, order, label = make_elev(kind, seed, st); svg = prefix_ids(svg, 'e_')
    sched = {'e_grade': (0.05, 0.8, 'seq'), 'e_walls': (0.7, 2.0, 'seq'), 'e_roof': (1.8, 3.6, 0.5), 'e_openings': (3.3, 6.4, 0.35),
             'e_details': (4.8, 7.6, 0.3), 'e_siding': (6.2, 8.2, 0.25), 'e_ent': (7.8, 9.4, 0.5), 'e_dims': (9.4, 10.4, 0.3), 'e_labels': (9.8, 10.6, 0.3)}
    return dict(name=name, style=style, hook=hook, sub=sub, cta=cta, end=12.4, sched=sched, timer=[0.05, 10.4], subs_top=1580,
                layers=[{'id': 'Le', 'svg': svg}], layers_meta=[],
                tint_windows=[['e_tint', 5.8, 7.0], ['e_shade', 7.4, 8.4], ['e_figs', 8.9, 9.5], ['e_figs2', 9.3, 9.9]]), label

BUILDERS = {'draw': job_draw, 'tour': job_tour, 'pop3d': job_pop3d, 'site2plan': job_site2plan, 'elev': job_elev}
