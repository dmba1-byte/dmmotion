import json, random, sys, datetime as dt
sys.path.insert(0, '/home/claude/reels')
from gen.plans import Plan
from gen.elev_site import elevation, site
from gen.engine import STYLES, sched_for

WORD = {1: 'one', 2: 'two', 3: 'three', 4: 'four'}
PLAN_HOOKS = [
    ("Watch this plan<br>draw itself", "walls → doors → fixtures → labels"),
    ("A {w}-bedroom plan<br>in 11 seconds", "{sf} square feet, line by line"),
    ("Your listing photos<br>can't do this", "a floor plan that moves"),
    ("Stop posting<br>flat PDFs", "animate the plan instead"),
    ("How the house<br>comes together", "one layer at a time"),
    ("Which room would<br>you change?", "tell me in the comments"),
    ("{sf} square feet,<br>drawn live", "a {w}-bedroom plan"),
]
ELEV_HOOKS = [("A front elevation,<br>built line by line", "grade → roof → siding → windows"),
              ("The front of the house<br>in 10 seconds", "from your elevation file"),
              ("Gable or hip?<br>Watch it draw", "{roof}")]
SITE_HOOKS = [("The whole lot,<br>in 10 seconds", "setbacks · drive · trees"),
              ("Where the house sits<br>on the lot", "a site plan, animated"),
              ("Site plans are hard to read.<br>Not this one.", "lot lines first, then the rest")]
TAGS = {'plan': ['#floorplan', '#homedesign', '#homebuilder', '#architecture', '#newconstruction', '#customhomes', '#realestate', '#houseplans'],
        'elev': ['#elevation', '#homebuilder', '#customhomes', '#architecture', '#newconstruction', '#housedesign'],
        'site': ['#siteplan', '#landdevelopment', '#homebuilder', '#architecture', '#realestate', '#newconstruction']}
CTAS = ["Free logo trial · link in bio", "Send your plan · link in bio", "DM me your drawing"]

def caption(kind, info, rng):
    if kind == 'plan':
        lead = rng.choice([f"A {WORD[info['beds']]}-bedroom plan, {info['sf']:,} SF, drawn layer by layer.",
                           f"{info['sf']:,} square feet. Walls, doors, fixtures, labels.",
                           f"This {WORD[info['beds']]}-bedroom plan took 11 seconds to read. A PDF takes a lot longer."])
        mid = rng.choice(["Builders and small firms: this is what your plans can do on your site, listings and socials.",
                          "Every line comes from the drawing file. Nothing is invented.",
                          "Send me your Illustrator, PDF, DWG or Revit export and I'll animate it."])
    elif kind == 'elev':
        lead = rng.choice(["A front elevation, built line by line.", f"{info['roof'].title()}, drawn from grade to ridge."])
        mid = rng.choice(["Builders: this is your listing's first 10 seconds.", "Your elevation file, in motion."])
    else:
        lead = rng.choice(["The whole lot in 10 seconds: lot lines, setbacks, drive, trees.", "A site plan, animated."])
        mid = rng.choice(["Site plans are the hardest drawing to read and the easiest one to animate.", "Show buyers where the house sits."])
    end = rng.choice(["Link in bio for pricing and the brief.", "Free 5-second logo trial: DM me your logo.", "Send me yours → link in bio."])
    tags = ' '.join(rng.sample(TAGS[kind], 5))
    return f"{lead}\n\n{mid}\n{end}\n{tags}"

VO = {
 'plan': ["Most floor plans sit in a PDF nobody opens. Watch this one draw itself. Walls, doors, fixtures, labels. Send me yours, and I'll bring it to life. Your drawing, in motion.",
          "Here's a {w}-bedroom plan, drawn in about ten seconds. Every line comes straight from the drawing file. If you build homes, your plans can do this too. Link in bio."],
 'elev': ["This is a front elevation, built line by line. Grade, roof, siding, windows. Put this on your listing and people actually watch it. Your drawing, in motion."],
 'site': ["Site plans are hard to read. So let's draw it. Lot lines, setbacks, the drive, the trees. Send me your site plan, and I'll animate it. Link in bio."],
}

def make_jobs(start_date, days, slots, seed0, voiced_n=4):
    rng = random.Random(seed0)
    kinds_cycle = ['plan', 'elev', 'plan', 'site', 'plan', 'elev', 'plan', 'site']
    styles = ['light', 'blueprint', 'dark']
    jobs = []; i = 0
    for d in range(days):
        day = start_date + dt.timedelta(days=d)
        for (hh, mm) in slots:
            kind = kinds_cycle[i % len(kinds_cycle)]; st = styles[(i + d) % 3]; S = STYLES[st]
            seed = seed0 * 100 + i
            info = {}
            if kind == 'plan':
                p = Plan(seed).build(); svg = p.svg(S['ink'], S['sub'], S['tint']); order = ['walls-ext', 'walls-int', 'openings', 'fixtures', 'labels', 'dims']
                info = {'beds': p.beds, 'sf': p.W * p.D}
                hk, sb = PLAN_HOOKS[i % len(PLAN_HOOKS)]
                hk = hk.format(w=WORD[p.beds], sf=f"{p.W * p.D:,}"); sb = sb.format(w=WORD[p.beds], sf=f"{p.W * p.D:,}")
            elif kind == 'elev':
                svg, order = elevation(seed, S['ink'], S['sub'], S['tint'], S['tint2'])
                roof = 'hip roof' if 'HIP ROOF' in svg else ('cross-gable porch' if 'CROSS-GABLE' in svg else 'side-gable roof')
                info = {'roof': roof}
                hk, sb = ELEV_HOOKS[i % len(ELEV_HOOKS)]; sb = sb.format(roof=roof)
            else:
                svg, order = site(seed, S['ink'], S['sub'], S['tint'], S['lawn'], S['road'])
                hk, sb = SITE_HOOKS[i % len(SITE_HOOKS)]
            sched, tint = sched_for(order, kind)
            when = dt.datetime(day.year, day.month, day.day, hh, mm)
            jobs.append(dict(name=f"r{when:%m%d_%H%M}_{kind}", kind=kind, style=st, svg=svg, sched=sched, tint=tint, hook=hk, sub=sb,
                             cta=CTAS[i % len(CTAS)], mood=['calm', 'warm', 'bright'][i % 3], bpm=[88, 92, 96][(i // 3) % 3], seed=seed,
                             when=when.isoformat(), caption=caption(kind, info, rng), voice=None, info=info))
            i += 1
    # choose voiced reels spread across the batch
    step = max(1, len(jobs) // voiced_n)
    for k, j in enumerate(jobs[::step][:voiced_n]):
        script = rng.choice(VO[j['kind']]).format(w=WORD.get(j['info'].get('beds', 3), 'three'))
        j['voice'] = script
    return jobs

if __name__ == '__main__':
    jobs = make_jobs(dt.date(2026, 10, 28), 8, [(8, 41), (12, 23)], seed0=7)
    json.dump(jobs, open('/home/claude/reels/batch1.json', 'w'), indent=1)
    print(len(jobs), sum(1 for j in jobs if j['voice']))
