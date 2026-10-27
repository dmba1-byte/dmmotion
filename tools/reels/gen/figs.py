"""Scale figures: top-down people for plans, side silhouettes for elevations."""
ACCENT = '#2e9b62'
def _path(pts_list, S):
    d = ''
    for pts in pts_list:
        d += 'M' + ' L'.join(f'{x * S:.1f} {-y * S:.1f}' for x, y in pts) + ' Z '
    return d
def adult_d(S, k=1.0):
    q = lambda pts: [(x * k, y * k) for x, y in pts]
    body = q([(-0.66, 4.75), (0.66, 4.75), (0.84, 2.95), (0.64, 2.9), (0.47, 4.2), (0.45, 2.95), (0.4, 0), (0.1, 0), (0.0, 2.45), (-0.1, 0), (-0.4, 0), (-0.45, 2.95), (-0.47, 4.2), (-0.64, 2.9), (-0.84, 2.95)])
    import math
    head = [(0.4 * k * math.cos(a / 12 * 2 * math.pi), 5.3 * k + 0.4 * k * math.sin(a / 12 * 2 * math.pi)) for a in range(12)]
    return _path([body, head], S)
def dog_d(S):
    body = [(-1.1, 1.3), (0.7, 1.3), (1.0, 1.75), (1.35, 1.7), (1.2, 1.25), (0.9, 1.0), (0.85, 0), (0.65, 0), (0.6, 0.85), (-0.7, 0.85), (-0.75, 0), (-0.95, 0), (-1.0, 1.0), (-1.4, 1.5)]
    return _path([body], S)

def plan_figs(p, layer, t_walk, fade, out=None):
    S, X0, Y0 = p.S, p.X0, p.Y0
    X = lambda f: X0 + f * S; Y = lambda f: Y0 + f * S
    figs = []
    liv = [r for r in p.rooms if r.kind == 'living']; kit = [r for r in p.rooms if r.kind == 'kitchen']; din = [r for r in p.rooms if r.kind == 'dining']
    if liv:
        lv = liv[0]
        ent = [d for d in p.doors if d[0] == 'h' and abs(d[1] - lv.y2) < 1e-6 and lv.x - 1e-6 <= d[2] <= lv.x2]
        tgt = kit[0] if kit else lv
        if ent:
            dx = (ent[0][2] + ent[0][3]) / 2
            pts = [(dx, lv.y2 + 3), (dx, lv.y2 - 2.5), (lv.x + lv.w * 0.5, lv.y + lv.h * 0.5), (tgt.x + tgt.w / 2, tgt.y + tgt.h * 0.55)]
            figs.append(dict(layer=layer, type='top', s=S, pts=[[X(a), Y(b)] for a, b in pts], t0=t_walk[0], t1=t_walk[1], fade=fade, accent=ACCENT, ease=True, out=out))
        sx, sy = lv.x + lv.w / 2 - 1.2, lv.y + lv.h - 3.9 if lv.h >= 12 else lv.y + lv.h - 2.5
        figs.append(dict(layer=layer, type='top', s=S, pts=[[X(sx), Y(sy)], [X(sx), Y(sy) - 0.01]], t0=0, t1=0, fade=[fade[0] + 0.2, fade[1] + 0.2], out=out))
    if din:
        dn = din[0]; tx, ty = dn.x + dn.w / 2, dn.y + dn.h / 2 + 0.6 - 2.0
        figs.append(dict(layer=layer, type='top', s=S, pts=[[X(tx), Y(ty)], [X(tx), Y(ty) + 0.01]], t0=0, t1=0, fade=[fade[0] + 0.4, fade[1] + 0.4], out=out))
    return figs

def elev_figs(e, layer, t_walk, fade):
    S = e.S; X = e.x; Yg = e.y(0); dx = getattr(e, 'door_x', e.W / 2)
    start = -5 if dx > e.W / 2 else e.W + 5; stop = dx + (-2.5 if start < 0 else 2.5)
    figs = [dict(layer=layer, type='side', s=S, d=adult_d(S), pts=[[X(start), Yg], [X(stop), Yg]], t0=t_walk[0], t1=t_walk[1], fade=fade, accent=ACCENT, flip=start > 0),
            dict(layer=layer, type='side', s=S, d=dog_d(S), pts=[[X(start - (2.2 if start < 0 else -2.2)), Yg], [X(stop - (2.4 if start < 0 else -2.4)), Yg]], t0=t_walk[0] + 0.15, t1=t_walk[1] + 0.15, fade=fade, flip=start > 0)]
    side = e.W * (0.82 if dx < e.W / 2 else 0.18)
    figs += [dict(layer=layer, type='side', s=S, d=adult_d(S), pts=[[X(side), Yg]], t0=0, t1=0, fade=[fade[0] + 0.3, fade[1] + 0.3]),
             dict(layer=layer, type='side', s=S, d=adult_d(S, 0.62), pts=[[X(side + 1.6), Yg]], t0=0, t1=0, fade=[fade[0] + 0.45, fade[1] + 0.45])]
    return figs

def subs_from(script, start=0.5, cps=11.8):
    import re
    parts = re.split(r'(?<=[.,!?])\s+', script.strip()); out = []; t = start
    for ph in parts:
        words = ph.split(); chunk = []
        for w in words:
            chunk.append(w)
            if len(' '.join(chunk)) > 26:
                txt = ' '.join(chunk); out.append([round(t, 2), round(t + len(txt) / cps + 0.15, 2), txt]); t += len(txt) / cps + 0.15; chunk = []
        if chunk:
            txt = ' '.join(chunk); out.append([round(t, 2), round(t + len(txt) / cps + 0.25, 2), txt]); t += len(txt) / cps + 0.25
    return out
