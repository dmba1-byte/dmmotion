import json, random, sys, datetime as dt
sys.path.insert(0, '/home/claude/reels')
from gen.jobs import BUILDERS
from gen.plans import TYPE_NAME

PLAN = [  # (concept, plan type, style)
 ('pop3d', 'courtyard', 'color'), ('elev', 'a_frame', 'dark'), ('tour', 'split', 'bluewhite'), ('site2plan', 'lshape', 'blueprint'),
 ('elev', 'butterfly', 'light'), ('draw', 'shotgun', 'color'), ('pop3d', 'dogtrot', 'dark'), ('elev', 'charleston', 'bluewhite'),
 ('draw', 'narrow', 'blueprint'), ('elev', 'gambrel', 'light'), ('tour', 'lshape', 'color'), ('elev', 'farmhouse', 'dark'),
 ('pop3d', 'split', 'blueprint'), ('elev', 'cape', 'bluewhite'), ('site2plan', 'courtyard', 'light'), ('elev', 'craftsman', 'color'),
]
WORD = {0: 'studio', 1: 'one', 2: 'two', 3: 'three', 4: 'four'}
HOOKS = {
 'pop3d': [("From flat plan<br>to 3D in 10 seconds", "watch the walls go up"), ("This plan<br>stands up", "2D → 3D, from one drawing")],
 'tour': [("Take a quick tour<br>of this plan", "room by room"), ("Zoom into<br>every room", "a plan that walks you through")],
 'site2plan': [("From the street<br>to the floor plan", "site plan → house plan"), ("Start with the lot.<br>End inside the house.", "one continuous drawing")],
 'draw': [("Watch this plan<br>draw itself", "walls → doors → fixtures → labels"), ("A {t}<br>in 11 seconds", "{sf} square feet, line by line")],
 'elev': [("Watch {a} {t}<br>draw itself", "front elevation, line by line"), ("Name this<br>house style", "answer in the comments"), ("The {t},<br>line by line", "roof → siding → windows"), ("Would you live<br>in this {t}?", "yes or no in the comments")],
}
STYLE_TXT = {'courtyard': 'courtyard house', 'split': 'split-bedroom ranch', 'lshape': 'ranch with garage', 'shotgun': 'shotgun house', 'dogtrot': 'dogtrot house', 'narrow': 'narrow-lot home', 'ranch': 'ranch', 'adu': 'backyard cottage'}
TAGS = ['#houseplan', '#dreamhome', '#floorplan', '#homedesign', '#homebuilder', '#architecture', '#newconstruction', '#customhomes', '#realestate', '#houseplans', '#architecturaldesign', '#housedesign']
CTAS = ["Comment \u201cPLAN\u201d for pricing", "Comment \u201cLOGO\u201d for a free trial", "Comment \u201cPLAN\u201d for pricing"]
LORE = {
 'courtyard': "Courtyard houses wrap the rooms around a private outdoor room, so every space gets light and air.",
 'split': "Split-bedroom ranches put the primary suite on the opposite side of the house from the kids' rooms.",
 'lshape': "The attached garage turns a simple ranch into an L, and shelters the front walk.",
 'shotgun': "Shotgun houses line every room up front to back, so a breeze could pass straight through. A New Orleans classic.",
 'dogtrot': "Dogtrot houses split into two cabins under one roof, with an open breezeway between them to catch the wind.",
 'narrow': "Narrow-lot homes stack the plan front to back to fit tight city lots.",
 'a_frame': "The A-frame: the roof is the wall. Mid-century cabin icon.",
 'butterfly': "The butterfly roof dips in the middle. Mid-century modern at its most optimistic.",
 'charleston': "The Charleston single house turns its narrow end to the street and runs a two-story piazza down the side.",
 'gambrel': "The gambrel roof comes from barns: two slopes per side means a full second floor under the roof.",
 'farmhouse': "Modern farmhouse: a steep front gable, board and batten, and a long porch with a metal roof.",
 'cape': "The Cape Cod: one and a half stories, steep roof, twin dormers, center door. New England since the 1700s.",
 'craftsman': "The Craftsman bungalow: low front gable, deep eaves, exposed brackets, tapered porch columns.",
}
VO = {
 'pop3d': "Here's a flat floor plan. Now watch it stand up. Same drawing, now in three dimensions. Send me your plan, and I'll animate it.",
 'elev': "This one starts with a single line. Then the roof, the siding, the windows. A front elevation, drawn in about ten seconds. Your drawing, in motion.",
 'draw': "Most floor plans sit in a PDF nobody opens. Watch this one draw itself. Walls, doors, fixtures, labels. Send me yours, and I'll bring it to life.",
}

def caption(concept, sub, info, rng, hook='', kw='PLAN'):
    lore = LORE.get(sub, '')
    what = {'pop3d': 'Flat plan to 3D, from the same drawing.', 'tour': 'A floor plan that walks you through it.', 'site2plan': 'From the lot down into the house plan.',
            'draw': 'Drawn line by line.', 'elev': 'A front elevation, built line by line.'}[concept]
    first = hook.replace('<br>', ' ')
    ask = ("Want your plan or elevation animated like this? Comment PLAN and I'll DM you pricing." if kw == 'PLAN'
           else "Want your logo animated like this? Comment LOGO and I'll make you a free 5-second trial.")
    return f"{first} 👀\n{ask}\n\n{lore}\n{what} Original drawing, animated from vector linework. From $450.\n.\n{' '.join(rng.sample(TAGS, 7))}"

def make(start, slots, seed0=11, voiced=(0, 4, 8, 12)):
    rng = random.Random(seed0); jobs = []; cnt = {}
    for i, (concept, sub, style) in enumerate(PLAN):
        day = start + dt.timedelta(days=i // len(slots)); hh, mm = slots[i % len(slots)]
        when = dt.datetime(day.year, day.month, day.day, hh, mm); seed = seed0 * 100 + i
        n = cnt.get(concept, 0); cnt[concept] = n + 1
        hk, sb = HOOKS[concept][n % len(HOOKS[concept])]
        name = f"r{when:%m%d_%H%M}_{concept}_{sub}"
        job, info = BUILDERS[concept](name, seed, sub, style, 'x', 'x', CTAS[i % 3])
        if concept == 'elev':
            label = info; hk = hk.format(t=label, a='an' if label[0].lower() in 'aeiou' else 'a'); sb = sb
        else:
            p = info; tname = STYLE_TXT.get(p.typ, p.typ)
            hk = hk.format(t=tname, sf=f"{p.sf:,}"); sb = sb.format(t=tname, sf=f"{p.sf:,}")
        if concept == 'elev':
            from gen import elevs as EV
            from gen.draw import fmt_ft
            ee = EV.LAST['e']; top = max([z for z, n in ee.levels] or [ee.Hmax])
            spec = f"{fmt_ft(ee.W)} WIDE · {fmt_ft(top)} TALL"
        else:
            nb = sum(r.kind == 'bed' for r in p.rooms); nba = sum(r.kind == 'bath' for r in p.rooms)
            spec = f"{p.sf:,} SQ FT · {nb} BED · {nba} BATH"
        kw = 'LOGO' if 'LOGO' in CTAS[i % 3] else 'PLAN'
        job.update(hook=hk, sub=sb, spec=spec, mood=['calm', 'warm', 'bright'][i % 3], bpm=[88, 92, 96][(i // 3) % 3], seed=seed,
                   when=when.isoformat(), caption=caption(concept, sub, info, rng, hk, kw), concept=concept, subject=sub,
                   voice=VO.get(concept, VO['draw']) if i in voiced else None)
        if job['voice']:
            from gen.figs import subs_from
            job['subs'] = subs_from(job['voice'])
        jobs.append(job)
    return jobs

if __name__ == '__main__':
    jobs = make(dt.date(2026, 10, 28), [(8, 41), (12, 23)])
    json.dump(jobs, open('/home/claude/reels/batch2.json', 'w'))
    for j in jobs: print(j['name'], '|', j['hook'].replace('<br>', ' '), '| voice' if j['voice'] else '')
