import sys, zlib, re, pathlib, subprocess, json, numpy as np
sys.path.insert(0, '/home/claude/reels')
from gen import engine2, jobs as J, elevs as EV
from gen.engine2 import STYLES, prefix_ids
import vo, soundtrack, scenes, compose

SP = {
 'farm': dict(kind='farmhouse', style='dark', fx='green', acc='#58e0a4', mode='scale', scene=('scroll','green',''),
   hook='Would a client stop<br>for this drawing?', chip='FLAT = SCROLLED PAST', rings=['e_roof','e_openings','e_walls'], price='CLIPS FROM $450', cta='Send me your drawing',
   lines=["Would a client stop for this drawing?", "Take three seconds.", "Probably not. A flat PDF looks like every other PDF.", "In a feed, the one that moves is the one that stops the thumb.",
          "Now watch.", "A person. A door. A dimension. It moves, and it feels lived in.", "I animate your drawings like this. Clips start at four hundred fifty dollars.", "Send me your drawing."],
   caps=["Would a client<br>stop for this<br>drawing?", "Take three<br>seconds.", "Probably not.<br>A flat PDF looks like<br>every other <em>PDF</em>.", "In a feed, the one<br>that <em>moves</em> stops<br>the thumb.", "Now watch.", "A person. A door.<br>A dimension.<br>It <em>moves</em>.", "Clips start<br>at <em>$450</em>.", "Send me<br>your drawing."]),
 'wt': dict(kind='saltbox', style='blueprint', fx='blue', acc='#6db8ff', mode='weights', scene=('desk','blue','2:07 AM'),
   hook='Which part of this<br>house is closest?', chip='ALL LINES: SAME WEIGHT', rings=['e_roof','e_openings','e_walls'], price='SIMPLE SHEETS · $30', cta='Line weights for $30',
   lines=["Which part of this house is closest to you?", "Take three seconds.", "You can't tell. Every line has the same weight.", "So at two a.m. you're still fixing it, line by line.",
          "Now watch the profile.", "Heavy profile. Light detail. The closest edge finally comes forward.", "Line weights to your spec. Simple sheets are thirty dollars.", "Message me your file."],
   caps=["Which part of this<br>house is closest<br>to you?", "Take three<br>seconds.", "You can't tell.<br>Every line has the<br><em>same weight</em>.", "So at 2 a.m.<br>you're still fixing it<br><em>line by line</em>.", "Now watch<br>the profile.", "Heavy profile.<br>Light detail.<br>The edge <em>comes forward</em>.", "Simple sheets<br>are <em>$30</em>.", "Message me<br>your file."]),
 'sun': dict(kind='craftsman', style='dark', fx='gray', acc='#e8e8e8', mode='light', scene=('sunarc','gray','SUN PATH'),
   hook='Why does this drawing<br>feel flat?', chip='NO LIGHT ON IT', rings=['e_roof','e_openings','e_walls'], price='CLIPS FROM $450', cta='Send me your drawing',
   lines=["Why does this drawing feel flat?", "Take three seconds.", "No light. No shade. Nothing pushes back.", "In real life, light moves across a building all day.",
          "Now let the sun in.", "Shade. Depth. Now it's a place.", "I animate your drawings like this. Clips start at four hundred fifty dollars.", "Send me your drawing."],
   caps=["Why does this<br>drawing feel flat?", "Take three<br>seconds.", "No light. No shade.<br>Nothing <em>pushes back</em>.", "In real life, light<br>moves across a<br>building <em>all day</em>.", "Now let the<br>sun in.", "Shade. Depth.<br>Now it's a <em>place</em>.", "Clips start<br>at <em>$450</em>.", "Send me<br>your drawing."]),
 'jury': dict(kind='cape', style='bluewhite', fx=None, acc='#1f5fae', mode='weights', split=True, scene=('jury','blue','THE REVIEW'),
   hook='What does a jury<br>see first?', chip='NOTHING LEADS THE EYE', rings=['e_roof','e_openings','e_walls'], price='SIMPLE SHEETS · $30', cta='Line weights for $30',
   lines=["What does a jury see first?", "Take three seconds.", "The model is right. But with every line the same weight, nothing leads the eye.", "A jury looks at many boards. Hierarchy decides which one gets read.",
          "Now watch it get a hand.", "Profile. Detail. Hatch. Now the eye knows where to go.", "Line weights to your spec. Simple sheets are thirty dollars.", "Message me your file."],
   caps=["What does a jury<br>see first?", "Take three<br>seconds.", "Every line the same<br>weight. <em>Nothing leads</em><br>the eye.", "A jury looks at<br>many boards.<br><em>Hierarchy</em> decides.", "Now watch it<br>get a hand.", "Profile. Detail. Hatch.<br>The eye knows<br>where to <em>go</em>.", "Simple sheets<br>are <em>$30</em>.", "Message me<br>your file."]),
}
key, name = sys.argv[1], sys.argv[2]
c = SP[key]; st = STYLES[c['style']]
seed = zlib.crc32(name.encode()) % 9999
svgw, order, label = EV.make(c['kind'], seed, st)
wsvg = prefix_ids(svgw, 'e_'); usvg = prefix_ids(svgw, 'u_')
if c['mode'] == 'weights': usvg = re.sub(r'stroke-width="[\d.]+"', 'stroke-width="0.9"', usvg)
hide = {'scale': 'u_figs,#u_figs2,#u_dims,#u_labels', 'light': 'u_shade,#u_tint,#u_figs2'}.get(c['mode'])
if hide: usvg = f'<style>#{hide}{{display:none}}</style>' + usvg
FC = engine2.fit_cam([wsvg], margin=96); S = FC['s'] * 0.97; CX, CY, CAMY = FC['cx'], FC['cy'], FC['cam_y']
sx = lambda x: round(540 + (x - CX) * S, 1); sy = lambda y: round(CAMY + (y - CY) * S, 1)
GB = FC['groups']
# narration first -> timeline follows the voice
auds = [vo._line(L) for L in c['lines']]
durs = [len(a) / vo.SR for a in auds]
starts = [0.25]
for d in durs[:-1]: starts.append(round(starts[-1] + d + 0.32, 2))
ends = [round(a + d, 2) for a, d in zip(starts, durs)]
E = round(ends[-1] + 0.5, 2)
K, O = 0.34, 0.2
base = {'grade': (0.05, 0.8, 'seq'), 'walls': (0.7, 2.0, 'seq'), 'roof': (1.8, 3.6, 0.5), 'openings': (3.3, 6.4, 0.35), 'details': (4.8, 7.6, 0.3),
        'siding': (6.2, 8.2, 0.25), 'ent': (7.8, 9.4, 0.5), 'dims': (9.4, 10.4, 0.3), 'labels': (9.8, 10.6, 0.3)}
sched = {pre + k: (round(O + a * K, 2), round(O + b * K, 2), d) for pre in ('e_', 'u_') for k, (a, b, d) in base.items()}
tw = [['u_tint', O + 5.8 * K, O + 7 * K], ['e_tint', O + 5.8 * K, O + 7 * K], ['e_shade', O + 7.4 * K, O + 8.4 * K], ['u_shade', O + 7.4 * K, O + 8.4 * K],
      ['e_figs', O + 8.9 * K, O + 9.5 * K], ['u_figs', O + 8.9 * K, O + 9.5 * K], ['e_figs2', O + 8.9 * K, O + 9.5 * K]]
# overlays
col = c['acc']; ov = []
bx = lambda g: GB[g]
for i, g in enumerate(c['rings']):
    x0, y0, x1, y1 = bx(g); cxs, cys = sx((x0 + x1) / 2), sy((y0 + y1) / 2)
    ov.append(dict(type='ring', x=cxs, y=cys, r=round(min(150, max(70, (x1 - x0) * S * 0.28)), 1), t0=round(starts[1] + 0.15 + i * (durs[1] / 3.2), 2), t1=round(starts[1] + 0.15 + (i + 1) * (durs[1] / 3.2) + 0.1, 2), col=col))
x0, y0, x1, y1 = FC['bbox']; X0, X1, Y0, Y1 = sx(x0) - 10, sx(x1) + 10, sy(y0) - 14, sy(y1) + 14
ov.append(dict(type='path', d=f'M{X0} {Y0} H{X1} V{Y1} H{X0} Z', t0=starts[2] + 0.2, t1=starts[3] - 0.05, d1=0.9, col=col, w=4))
t0s, t1s = round(starts[4] + 0.25, 2), round(ends[5] - 0.3, 2)
ov.append(dict(type='scan', t0=t0s, t1=t1s, x0=X0, x1=X1, y0=Y0, y1=Y1, col=col, clip='Le'))
if c.get('split'):
    ov.append(dict(type='label', x=round(X0 + 80), y=round(Y0 - 34), text='AFTER', t0=t0s + 0.6, t1=ends[5], col=col, fs=30))
    ov.append(dict(type='label', x=round(X1 - 80), y=round(Y0 - 34), text='BEFORE', t0=t0s + 0.6, t1=ends[5], col=col, fs=30))
tags = [[starts[1] + durs[1] * i / 3, starts[1] + durs[1] * (i + 1) / 3, str(3 - i), 'cd'] for i in range(3)]
tags += [[starts[2] + 0.1, ends[2] + 0.25, c['chip'], 'chip'], [starts[6] + 0.15, ends[6] + 0.3, c['price'], 'chip']]
subs = [[a, round(b + 0.12, 2), cap] for a, b, cap in zip(starts, ends, c['caps'])]
job = dict(name=name, style=c['style'], hook=c['hook'], sub='', cta=c['cta'], end=E, sched=sched, subs=subs, tags=tags, ov=ov, accent=col,
           layers=[{'id': 'Lu', 'svg': usvg}, {'id': 'Le', 'svg': wsvg}],
           layers_meta=[{'id': 'Lu', 'cam': [[0, S, CX, CY]]}, {'id': 'Le', 'cam': [[0, S, CX, CY]]}], cam_y=CAMY,
           tint_windows=tw, mood='warm', bpm=92, seed=seed, hook_out=starts[1] - 0.5, fx=c['fx'])
dur = E + 3.6
audio = np.zeros(int((dur + 0.2) * vo.SR), dtype=np.float32)
for a, s in zip(auds, starts):
    i = int(s * vo.SR); audio[i:i + len(a)] += a[:len(audio) - i]
out = pathlib.Path('/home/claude/reels/out5'); out.mkdir(exist_ok=True)
engine2.render(job, str(out))
wav = str(out / f'{name}_mix.wav')
soundtrack.make(dur, draw=(0.4, E - 0.8), end=E, mood='warm', bpm=92, seed=seed, out=wav, pen=False, beat=True)
vo.lay_under(wav, audio)
final0 = str(out / f'{name}_voiced0.mp4')
final = str(out / f'{name}_voiced.mp4')
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', str(out / f'{name}_silent.mp4'), '-i', wav, '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-shortest', '-movflags', '+faststart', final0], check=True)
import scenes, compose
sk, sp, stag = c['scene']; sd = round(ends[3] - starts[3] + 0.25, 2)
scp = scenes.render(sk, sd, sp, c['caps'][3], str(out / f'{name}_scene.mp4'), stag)
compose.overlay(final0, [(scp, starts[3] - 0.05, sd)], final)
print('FINAL', final, round(dur, 1), json.dumps(dict(starts=starts, ends=ends)))
