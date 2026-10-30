"""Circulation-first layout.

The old generator packed rooms into a grid then looked for leftover wall to put
doors and windows in. That is backwards, and it is why bedrooms ended up sealed
behind closet strips. Here the corridor exists first, every habitable room is
sized from the fixtures it must legally hold plus their clearances, and doors
are hung onto the corridor wall by construction.

Dimensional sources
  IRC R311.6   corridor not less than 36 in; 48 in used here
  IRC R310     egress glazing on an exterior wall of every sleeping room
  NKBA         work triangle legs 4-9 ft, sum not over 26 ft; work aisle 42 in
               (one cook); walkway 36 in; landings 15 in at the refrigerator,
               12/15 in at the cooking surface, 24/18 in at the primary sink
  Angi/trade   reach-in closet at least 24 in deep and 3-6 ft wide;
               walk-in from 5 x 5 ft

Band layout, front of house at the bottom (y = D):

    y 0 .. BD          private band: bedrooms, baths, closets
    y BD .. BD+HD      corridor
    y BD+HD .. D       public band: living / dining / kitchen, open plan
"""
from .plans import Plan, RES

LEAF, BATH_LEAF = 2.7, 2.4
JAMB = 0.6                 # casing offset, well over the 4 in minimum
CLOSET_D = 2.2             # reach-in depth, just over the 24 in minimum
CLOSET_W = 5.0


def _units(a, b):
    return [round(a + i * RES, 2) for i in range(int(round((b - a) / RES)))]


class Ranch(Plan):
    """Single-storey three-bed, two-bath ranch that satisfies the validator."""

    def build(self):
        r = self.rng
        self.typ = 'ranch'

        BD = r.choice([12.5, 13.0])          # private band depth
        HD = 4.0                              # corridor
        PD = r.choice([20.0, 21.0, 22.0])     # public band depth
        D = BD + HD + PD

        w_b2 = r.choice([12.0, 12.5])
        w_b3 = r.choice([12.0, 12.5])
        w_ba = r.choice([10.5, 11.0])         # hall bath: three fixtures on one run
        w_pr = r.choice([14.0, 15.0])
        w_pb = 8.5                            # primary ensuite
        W = w_b2 + w_b3 + w_ba + w_pr + w_pb

        BA_D = 8.0                            # bath depth; remainder becomes storage

        # ---------------- private band ----------------
        x = 0.0
        b2 = self.add('BEDROOM 2', 'bed', x, 0, w_b2, BD); x += w_b2
        b3 = self.add('BEDROOM 3', 'bed', x, 0, w_b3, BD); x += w_b3
        ba = self.add('BATH', 'bath', x, BD - BA_D, w_ba, BA_D)
        ld = self.add('LAUNDRY', 'laundry', x, 0, w_ba, BD - BA_D)
        x += w_ba
        pr = self.add('PRIMARY BEDROOM', 'bed', x, 0, w_pr, BD); x_pr = x; x += w_pr
        pb = self.add('PRIMARY BATH', 'bath', x, BD - BA_D, w_pb, BA_D)
        wic = self.add('W.I.C.', 'wic', x, 0, w_pb, BD - BA_D)

        # reach-in closets, recessed into each secondary bedroom's corridor wall
        for bed in (b2, b3):
            cx = bed.x2 - CLOSET_W - 0.5
            self.add('CL.', 'closet', cx, BD - CLOSET_D, CLOSET_W, CLOSET_D)

        # corridor stops at the primary suite; it serves nothing beyond
        hall_w = x_pr + w_pr
        self.add('HALL', 'hall', 0, BD, hall_w, HD)
        # the strip behind the ensuite becomes the kitchen pantry
        pan = self.add('PANTRY', 'pantry', hall_w, BD, W - hall_w, HD)

        # ---------------- public band ----------------
        y0 = BD + HD
        w_lv = round(W * 0.44, 2)
        w_dn = round(W * 0.26, 2)
        w_kt = round(W - w_lv - w_dn, 2)
        lv = self.add('LIVING', 'living', 0, y0, w_lv, PD)
        dn = self.add('DINING', 'dining', w_lv, y0, w_dn, PD)
        kt = self.add('KITCHEN', 'kitchen', w_lv + w_dn, y0, w_kt, PD)

        self.W, self.D = W, D
        self.beds = 3
        self.sf = int(W * D)

        # ---------------- doors ----------------
        for rm, leaf in ((b2, LEAF), (b3, LEAF), (ba, BATH_LEAF)):
            a = rm.x + JAMB
            self.doors.append(('h', BD, a, a + leaf, True, 'up'))
        a = pr.x + JAMB
        self.doors.append(('h', BD, a, a + LEAF, True, 'up'))
        # ensuite and walk-in open off the primary bedroom
        self.doors.append(('v', pb.x, pb.y + JAMB, pb.y + JAMB + BATH_LEAF, True, 'right'))
        self.doors.append(('v', wic.x, wic.y + JAMB, wic.y + JAMB + BATH_LEAF, True, 'right'))
        # laundry off the corridor
        la = ld.x + JAMB
        self.doors.append(('h', ld.y2, la, la + BATH_LEAF, True, 'up'))
        # front door into the living room
        fa = lv.x + lv.w / 2 - 1.5
        self.doors.append(('h', D, fa, fa + 3.0, True, 'up'))

        # ---------------- openings ----------------
        # reach-in closets read as bypass doors, not swinging leaves
        for rm in self.rooms:
            if rm.kind == 'closet':
                for u in _units(rm.x + 0.25, rm.x2 - 0.25):
                    self.open.add(('h', round(rm.y, 2), u))
        # corridor opens into the living room
        op = lv.x + lv.w * 0.5
        for u in _units(op, op + 6.0):
            self.open.add(('h', round(y0, 2), u))
        # living / dining / kitchen are one space
        for c in (w_lv, w_lv + w_dn):
            for u in _units(y0, D):
                self.open.add(('v', round(c, 2), u))
        # pantry opens down into the kitchen
        for u in _units(pan.x + 0.5, pan.x2 - 0.5):
            self.open.add(('h', round(y0, 2), u))

        # ---------------- glazing ----------------
        for rm in (b2, b3, pr):                      # IRC R310 egress
            m = rm.x + rm.w / 2
            self.windows.append(('h', 0.0, m - 1.75, m + 1.75))
        self.windows.append(('h', 0.0, ld.x + ld.w / 2 - 1.0, ld.x + ld.w / 2 + 1.0))
        self.windows.append(('v', 0.0, 2.0, 7.0))
        self.windows.append(('h', D, lv.x + 1.5, lv.x + 5.5))
        self.windows.append(('h', D, dn.x + dn.w / 2 - 2.0, dn.x + dn.w / 2 + 2.0))
        self.windows.append(('v', 0.0, y0 + 4.0, y0 + 9.0))
        return self
