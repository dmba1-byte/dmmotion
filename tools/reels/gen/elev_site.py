import math, random
from .draw import L, R, C, P, T, G, dashed, dimH, dimV, fmt_ft

def elevation(seed, ink, sub, tint, tint2, box=(70, 640, 940, 640)):
    r = random.Random(seed)
    W = r.choice([36, 40, 44, 48, 52, 56]); plate = r.choice([9, 9, 10])
    roof = r.choice(['side_gable', 'hip', 'cross_gable'])
    pitch = r.choice([5, 6, 7, 8]) / 12; depth = r.choice([28, 30, 32, 34])
    siding = r.choice(['lap', 'lap', 'batten'])
    rise = (depth / 2) * pitch * (0.6 if roof == 'hip' else 1)
    OV = 1.5; tot_h = 1.5 + plate + rise
    bx, by, bw, bh = box
    S = min(bw / (W + 2 * OV + 6), bh / (tot_h + 6)); X0 = bx + (bw - (W) * S) / 2
    FF = by + bh * 0.72
    x = lambda f: X0 + f * S; y = lambda f: FF - f * S
    GR, PL, EAVE, RID = y(-1.5), y(plate), y(plate - 0.4), y(plate - 0.4 + rise)
    tg = [R(x(0), PL, W * S, FF - PL, 0, tint, 'none')]
    if roof == 'hip':
        ins = (depth / 2) * 0.9
        roofd = f'M{x(-OV):.1f} {EAVE:.1f} L{x(ins):.1f} {RID:.1f} L{x(W - ins):.1f} {RID:.1f} L{x(W + OV):.1f} {EAVE:.1f} Z'
        tg.append(P(roofd, 0, tint2, 'none'))
    else:
        tg.append(R(x(-OV), RID, (W + 2 * OV) * S, EAVE - RID, 0, tint2, 'none'))
    grade = G('grade', L(30, GR, 1050, GR, 5, ink), L(x(0), FF, x(W), FF, 2.5, ink), L(x(0), FF, x(0), GR, 2.5, ink), L(x(W), FF, x(W), GR, 2.5, ink))
    walls = G('walls', L(x(0), FF, x(0), EAVE, 4, ink), L(x(W), FF, x(W), EAVE, 4, ink))
    rf = [L(x(-OV), EAVE, x(W + OV), EAVE, 4, ink), L(x(-OV), EAVE + 8, x(W + OV), EAVE + 8, 2, ink)]
    if roof == 'hip':
        ins = (depth / 2) * 0.9
        rf += [L(x(-OV), EAVE, x(ins), RID, 4, ink), L(x(ins), RID, x(W - ins), RID, 4, ink), L(x(W - ins), RID, x(W + OV), EAVE, 4, ink)]
        for k in range(1, int((EAVE - RID) / 16)):
            yy = RID + k * 16; t = (yy - RID) / (EAVE - RID)
            xa = x(ins) + (x(-OV) - x(ins)) * t; xb = x(W - ins) + (x(W + OV) - x(W - ins)) * t
            rf.append(L(xa, yy, xb, yy, 1, sub, 'butt'))
    else:
        rf += [L(x(-OV), RID, x(W + OV), RID, 4, ink), L(x(-OV), RID, x(-OV), EAVE, 4, ink), L(x(W + OV), RID, x(W + OV), EAVE, 4, ink)]
        rf += [L(x(-OV), yy, x(W + OV), yy, 1, sub, 'butt') for yy in [RID + k * 16 for k in range(1, int((EAVE - RID) / 16))]]
    door_c = r.choice([W * 0.5, W * 0.62, W * 0.38])
    if roof == 'cross_gable':
        gw = 8; gl, gr = x(door_c - gw), x(door_c + gw); apex = EAVE - gw * S * pitch * 1.1
        rf.append(P(f'M{gl - 14:.1f} {EAVE:.1f} L{x(door_c):.1f} {apex - 8:.1f} L{gr + 14:.1f} {EAVE:.1f} Z', 4, tint, ink))
        rf.append(R(x(door_c) - 13, apex + (EAVE - apex) * 0.35, 26, 32, 2, 'none', ink))
    roofg = G('roof', *rf)
    sid = []
    if siding == 'lap':
        sid = [L(x(0), yy, x(W), yy, 1, sub, 'butt') for yy in [FF - 12 * k for k in range(1, int((FF - EAVE - 8) / 12) + 1)]]
    else:
        sid = [L(xx, EAVE + 10, xx, FF, 1, sub, 'butt') for xx in [x(0) + k * 16 for k in range(1, int(W * S / 16))]]
    sidingg = G('siding', *sid)
    op = []
    dw = 3.0
    op += [R(x(door_c - dw / 2), y(7), dw * S, 7 * S, 3, tint, ink), C(x(door_c + dw / 2) - 7, y(3.5), 3, 1.5, 'none', ink)]
    op += [R(x(door_c - dw / 2 - 1), FF, (dw + 2) * S, 0.75 * S, 2, 'none', ink)]
    n = max(2, int(W / 9)); slots = [W * (i + 0.5) / (n + 1) for i in range(n + 1)]
    slots = [s for s in slots if abs(s - door_c) > 5] or [W * 0.2, W * 0.8]
    ww = r.choice([3, 3, 4]); twin = r.random() < 0.35
    for s in slots:
        for k in ([-0.55, 0.55] if twin else [0]):
            cx = s + k * (ww + 0.3); a, b = x(cx - ww / 2), x(cx + ww / 2); top, bot = y(7), y(3)
            op += [R(a, top, b - a, bot - top, 3, 'none', ink), L((a + b) / 2, top, (a + b) / 2, bot, 1.5, ink), L(a, (top + bot) / 2, b, (top + bot) / 2, 1.5, ink)]
        op.append(L(x(s - ww / 2 - (ww * 0.55 if twin else 0)) - 6, y(3) + 5, x(s + ww / 2 + (ww * 0.55 if twin else 0)) + 6, y(3) + 5, 3, ink))
    if roof == 'cross_gable':
        for px_ in (door_c - 6.6, door_c + 6):
            op.append(R(x(px_), EAVE + 8, 0.6 * S, FF - EAVE - 8, 2.5, 'none', ink))
    openings = G('openings', *op)
    dims = G('dims', dimH(x(0), x(W), GR + 48, fmt_ft(W), sub), dimV(x(W + OV) + 26, FF, PL, fmt_ft(plate), sub, off=26), dimV(x(W + OV) + 26, PL, RID, fmt_ft(rise), sub, off=26))
    rname = {'side_gable': 'SIDE-GABLE ROOF', 'hip': 'HIP ROOF', 'cross_gable': 'CROSS-GABLE PORCH'}[roof]
    labels = G('labels', T(x(0), GR + 120, 'FRONT ELEVATION', 26, 'start', ink, 600, 4),
               T(x(0), GR + 152, f'{rname} · {int(pitch * 12)}/12 PITCH · {"LAP" if siding == "lap" else "BOARD & BATTEN"} SIDING', 18, 'start', sub, 500, 1.5))
    order = ['grade', 'walls', 'roof', 'siding', 'openings', 'dims', 'labels']
    return ''.join([G('tint', *tg), grade, walls, roofg, sidingg, openings, dims, labels]), order


def site(seed, ink, sub, tint, lawn, road):
    r = random.Random(seed)
    lw = r.choice([70, 80, 90]); ld = r.choice([110, 120, 130]); S = min(640 / lw, 980 / ld)
    X0 = (1080 - lw * S) / 2; Y0 = 560
    x = lambda f: X0 + f * S; y = lambda f: Y0 + f * S
    fs, rs, ss = 30, 25, 8
    hw = r.choice([44, 48, 52]); hw = min(hw, lw - 2 * ss - 14); hd = r.choice([30, 32, 34])
    drive_right = r.random() < 0.5
    hx = ss + 2 if drive_right else lw - ss - 2 - hw
    hy = ld - fs - 4 - hd
    tint_parts = [R(x(0), y(0), lw * S, ld * S, 0, lawn, 'none'), R(x(hx), y(hy), hw * S, hd * S, 0, tint, 'none'), R(x(-40), y(ld + 2), (lw + 80) * S, 25 * S, 0, road, 'none')]
    lot = G('lot', L(x(0), y(0), x(lw), y(0), 5, ink), L(x(lw), y(0), x(lw), y(ld), 5, ink), L(x(lw), y(ld), x(0), y(ld), 5, ink), L(x(0), y(ld), x(0), y(0), 5, ink))
    setb = G('setbacks', dashed(x(ss), y(rs), x(lw - ss), y(rs), sub), dashed(x(lw - ss), y(rs), x(lw - ss), y(ld - fs), sub), dashed(x(lw - ss), y(ld - fs), x(ss), y(ld - fs), sub), dashed(x(ss), y(ld - fs), x(ss), y(rs), sub))
    street = G('street', L(10, y(ld + 2), 1070, y(ld + 2), 2.5, ink), L(10, y(ld + 7), 1070, y(ld + 7), 2.5, ink), L(10, y(ld + 9), 1070, y(ld + 9), 4, ink),
               *[L(xx, y(ld + 20), xx + 40, y(ld + 20), 3, sub, 'butt') for xx in range(30, 1060, 80)])
    hxx = lambda f: x(hx + f); hyy = lambda f: y(hy + f); q = hd / 2
    house = G('house', L(hxx(0), hyy(0), hxx(hw), hyy(0), 6, ink), L(hxx(hw), hyy(0), hxx(hw), hyy(hd), 6, ink), L(hxx(hw), hyy(hd), hxx(0), hyy(hd), 6, ink), L(hxx(0), hyy(hd), hxx(0), hyy(0), 6, ink),
              L(hxx(q), hyy(q), hxx(hw - q), hyy(q), 2.5, ink), L(hxx(0), hyy(0), hxx(q), hyy(q), 2, ink), L(hxx(0), hyy(hd), hxx(q), hyy(q), 2, ink), L(hxx(hw), hyy(0), hxx(hw - q), hyy(q), 2, ink), L(hxx(hw), hyy(hd), hxx(hw - q), hyy(q), 2, ink))
    dx = lw - 4 - 12 if drive_right else 4
    pat_x = hx + hw * 0.25
    hard = G('hardscape', R(x(dx), y(hy + 6), 12 * S, (ld - hy - 6) * S, 2.5, 'none', ink),
             L(x(dx), y(ld), x(dx), y(ld + 9), 2.5, ink), L(x(dx + 12), y(ld), x(dx + 12), y(ld + 9), 2.5, ink),
             R(x(min(hx + hw * 0.5, dx + 12)), y(hy + hd + 1), abs((hx + hw * 0.5) - (dx if drive_right else dx + 12)) * S, 4 * S, 2, 'none', ink),
             R(x(pat_x), y(hy - 12), 18 * S, 12 * S, 2.5, 'none', ink))
    trees, placed = [], []
    for k in range(r.randint(5, 8)):
        for _ in range(40):
            rr = r.uniform(5, 9); tx = r.uniform(rr + 1, lw - rr - 1); ty = r.uniform(rr + 1, ld - rr - 1)
            if hx - rr - 2 < tx < hx + hw + rr + 2 and hy - 14 - rr < ty < hy + hd + rr + 3: continue
            if dx - rr - 1 < tx < dx + 12 + rr + 1 and ty > hy: continue
            if any(math.hypot(tx - a, ty - b) < rr + c + 2 for a, b, c in placed): continue
            placed.append((tx, ty, rr)); break
    for tx, ty, rr in placed:
        cx, cy, R0 = x(tx), y(ty), rr * S
        d = 'M' + ' L'.join(f'{cx + R0 * (1 + 0.08 * math.sin(a * 9)) * math.cos(a):.1f} {cy + R0 * (1 + 0.08 * math.sin(a * 9)) * math.sin(a):.1f}' for a in [i * 2 * math.pi / 72 for i in range(73)])
        trees += [P(d, 2, lawn, ink), C(cx, cy, 3, 2, 'none', ink)] + [L(cx, cy, cx + R0 * 0.55 * math.cos(a), cy + R0 * 0.55 * math.sin(a), 1, sub, 'round') for a in (0.4, 1.9, 3.2, 4.6)]
    nx, ny = (x(lw - 7), y(7)) if drive_right else (x(7), y(7))
    north = G('north', C(nx, ny, 22, 2, 'none', ink), P(f'M{nx:.1f} {ny - 18:.1f} L{nx + 9:.1f} {ny + 10:.1f} L{nx:.1f} {ny + 4:.1f} L{nx - 9:.1f} {ny + 10:.1f} Z', 1.5, ink, ink))
    sf = hw * hd
    labels = G('labels', T(hxx(hw / 2), hyy(hd / 2) - 4, 'RESIDENCE', 24, color=ink, w=700, ls=3), T(hxx(hw / 2), hyy(hd / 2) + 26, f'{sf:,} SF', 18, color=sub, w=500, ls=1.5),
               T(x(pat_x + 9), y(hy - 5), 'PATIO', 18, color=ink, ls=2), T(x(dx + 6), y((hy + 6 + ld) / 2), 'DRIVE', 18, color=ink, ls=2, rot=-90),
               T(x(lw / 2), y(ld - fs + 4), f"FRONT SETBACK {fs}'", 15, color=sub, w=500, ls=1.5), T(540, y(ld + 16), 'STREET', 20, color=sub, ls=5), T(nx, ny + 46, 'N', 18, color=ink, ls=1))
    dims = G('dims', dimH(x(0), x(lw), y(0) - 30, fmt_ft(lw), sub), dimV(x(0) - 40, y(0), y(ld), fmt_ft(ld), sub))
    order = ['lot', 'setbacks', 'street', 'house', 'hardscape', 'trees', 'north', 'labels', 'dims']
    return ''.join([G('tint', *tint_parts), lot, setb, street, house, hard, G('trees', *trees), north, labels, dims]), order
