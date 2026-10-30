"""Circulation-first layout.

The old generator packed rooms into a grid and then looked for leftover wall to
put doors and windows in. That is backwards, and it is why bedrooms ended up
sealed behind closet strips. Here the corridor exists first, every habitable
room is sized from the fixtures it must legally hold plus their clearances, and
doors are hung onto the corridor wall by construction with casing room and a
leaf that can swing clear.

Band layout, front of house at the bottom (y = D):

    y 0 .. BD          private band: bedrooms and bathroom, rear wall for egress
    y BD .. BD+HD      corridor, 4 ft (IRC R311.6 wants 36 in minimum)
    y BD+HD .. D       public band: living / dining / kitchen, open plan
"""
from .plans import Plan

LEAF = 2.7          # interior door leaf
BATH_LEAF = 2.4
JAMB = 0.6          # casing offset from a corner, well over the 4 in minimum


class Ranch(Plan):
    """A single-storey ranch that satisfies the validator by construction."""

    def build(self):
        r = self.rng
        self.typ = 'ranch'

        BD = r.choice([12.0, 12.5, 13.0])        # bedroom depth
        HD = 4.0                                  # corridor
        PD = r.choice([19.0, 20.0, 21.0])         # public band depth
        D = BD + HD + PD

        w_b2 = r.choice([11.5, 12.0, 12.5])
        w_b3 = r.choice([11.5, 12.0, 12.5])
        w_ba = r.choice([10.5, 11.0])   # three fixtures ganged along one wall need the run
        w_pr = r.choice([14.0, 15.0])
        W = w_b2 + w_b3 + w_ba + w_pr

        # ---- private band ----
        x = 0.0
        b2 = self.add('BEDROOM 2', 'bed', x, 0, w_b2, BD); x += w_b2
        b3 = self.add('BEDROOM 3', 'bed', x, 0, w_b3, BD); x += w_b3
        # a hall bath is not the full depth of the band; the rest becomes a
        # walk-in closet opening off the primary bedroom next door
        BA_D = 8.0
        ba = self.add('BATH', 'bath', x, BD - BA_D, w_ba, BA_D)
        wic = self.add('W.I.C.', 'wic', x, 0, w_ba, BD - BA_D)
        x += w_ba
        pr = self.add('PRIMARY BEDROOM', 'bed', x, 0, w_pr, BD)

        # ---- corridor, spanning the private rooms ----
        hall = self.add('HALL', 'hall', 0, BD, W, HD)

        # ---- public band ----
        w_lv = round(W * 0.40, 2); w_dn = round(W * 0.26, 2); w_kt = round(W - w_lv - w_dn, 2)
        y0 = BD + HD
        lv = self.add('LIVING', 'living', 0, y0, w_lv, PD)
        dn = self.add('DINING', 'dining', w_lv, y0, w_dn, PD)
        kt = self.add('KITCHEN', 'kitchen', w_lv + w_dn, y0, w_kt, PD)

        self.W, self.D = W, D
        self.beds = 3
        self.sf = int(W * D)

        # ---- doors onto the corridor, hinged clear of the corner ----
        for rm, leaf in ((b2, LEAF), (b3, LEAF), (ba, BATH_LEAF), (pr, LEAF)):
            a = rm.x + JAMB
            self.doors.append(('h', BD, a, a + leaf, True, 'up'))

        # walk-in closet opens off the primary bedroom
        self.doors.append(('v', wic.x2, wic.y + 0.6, wic.y + 0.6 + 2.4, True, 'right'))

        # front door into the living room, swinging in
        fa = lv.x + lv.w / 2 - 1.5
        self.doors.append(('h', D, fa, fa + 3.0, True, 'up'))

        # ---- corridor opens to the public band through a cased opening ----
        op_lo = lv.x + lv.w * 0.45
        for u in self._units(op_lo, op_lo + 6.0):
            self.open.add(('h', round(BD + HD, 2), u))
        # living / dining / kitchen are one open space
        for c in (w_lv, w_lv + w_dn):
            for u in self._units(y0, D):
                self.open.add(('v', round(c, 2), u))

        # ---- egress glazing on the rear wall, one per sleeping room ----
        for rm in (b2, b3, pr):
            m = rm.x + rm.w / 2
            self.windows.append(('h', 0.0, m - 1.75, m + 1.75))
        self.windows.append(('h', 0.0, ba.x + ba.w / 2 - 1.0, ba.x + ba.w / 2 + 1.0))

        # public glazing: front wall either side of the entry, plus the gable ends
        self.windows.append(('h', D, lv.x + 1.5, lv.x + 5.5))
        self.windows.append(('h', D, kt.x + kt.w / 2 - 2.0, kt.x + kt.w / 2 + 2.0))
        self.windows.append(('v', 0.0, y0 + 3.0, y0 + 8.0))
        self.windows.append(('v', W, y0 + 3.0, y0 + 8.0))
        return self

    @staticmethod
    def _units(a, b):
        from .plans import RES
        return [round(a + i * RES, 2) for i in range(int(round((b - a) / RES)))]
