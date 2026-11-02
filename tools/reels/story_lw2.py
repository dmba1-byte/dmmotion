"""Voiced story reel for the line-weight service: 2 a.m. pin-up -> same-weight drawing -> send file -> weights snap."""
import sys, zlib, re, pathlib, subprocess, numpy as np, os
sys.path.insert(0,'/home/claude/reels')
from gen import engine2, jobs as J
from gen.engine2 import STYLES, prefix_ids
from gen import elevs as EV
import vo, soundtrack
kind, style, name = sys.argv[1], sys.argv[2], sys.argv[3]
fx = os.environ.get('FX','blue')
seed = zlib.crc32(name.encode()) % 9999
st = STYLES[style]
svgw, order, label = EV.make(kind, seed, st)
wsvg = prefix_ids(svgw, 'e_')
usvg = prefix_ids(svgw, 'u_')
usvg = re.sub(r'stroke-width="[\d.]+"', 'stroke-width="0.9"', usvg)
K, O = 0.62, 2.6   # build-time scale/offset
base = {'grade': (0.05, 0.8, 'seq'), 'walls': (0.7, 2.0, 'seq'), 'roof': (1.8, 3.6, 0.5), 'openings': (3.3, 6.4, 0.35), 'details': (4.8, 7.6, 0.3),
        'siding': (6.2, 8.2, 0.25), 'ent': (7.8, 9.4, 0.5), 'dims': (9.4, 10.4, 0.3), 'labels': (9.8, 10.6, 0.3)}
sched = {}
for pre in ('e_', 'u_'):
    for k, (a, b, d) in base.items():
        sched[pre+k] = (round(O+a*K, 2), round(O+b*K, 2), d)
SNAP = 11.6
FC = engine2.fit_cam([wsvg], margin=84); FS=FC['s']*0.97; CX,CY=FC['cx'],FC['cy']; print('FIT',FC)
LINES = ["Three days before the jury.", "The model is right. The drawing looks like a CAD export.", "You can spend tonight on line weights. Or on the idea.",
         "Send me the file, the scale, your degrees.", "Profile. Detail. Hatch. Done.", "Simple sheets, for thirty dollars. Spend tonight designing.", "Message me your file."]
starts = [0.1, 2.5, 6.3, 9.3, 11.7, 14.0, 17.0]
subs = [[0.1,2.4,"Three days<br>before the jury."],[2.5,6.2,"The model is right.<br>The drawing looks like<br>a CAD export."],[6.3,9.2,"Tonight: line weights,<br>or the idea?"],
        [9.3,11.5,"Send me the file,<br>the scale,<br>your degrees."],[11.7,13.9,"Profile. Detail.<br>Hatch. Done."],[14.0,16.9,"Simple sheets<br>for $30. Spend<br>tonight designing."],[17.0,19.5,"Message me<br>your file."]]
job = dict(name=name, style=style, hook="Three days<br>before the jury.", sub="and it still looks like a CAD export", cta='Line weights from $30', end=18.6, sched=sched, timer=[0.05, 11.5], subs_top=1580,
           layers=[{'id':'Lu','svg':usvg}, {'id':'Le','svg':wsvg,'op0':0}],
           layers_meta=[{'id':'Lu','cam':[[0,FS,CX,CY],[SNAP-0.15,FS,CX,CY],[SNAP+0.2,FS*1.03,CX,CY],[SNAP+1.1,FS,CX,CY]],'op':[[0,0.62],[SNAP,0.62],[SNAP+0.3,0]]}, {'id':'Le','cam':[[0,FS,CX,CY],[SNAP-0.15,FS,CX,CY],[SNAP+0.2,FS*1.03,CX,CY],[SNAP+1.1,FS,CX,CY]],'op':[[0,0],[SNAP,0],[SNAP+0.3,1]]}],
           tint_windows=[['u_tint',O+5.8*K,O+7.0*K],['e_tint',O+5.8*K,O+7.0*K],['e_shade',O+7.4*K,O+8.4*K],['u_shade',O+7.4*K,O+8.4*K],['e_figs',O+8.9*K,O+9.5*K],['u_figs',O+8.9*K,O+9.5*K]],
           cam_y=FC['cam_y'], mood='warm', bpm=92, seed=seed, hook_out=2.7, fx=fx, subs=subs)
dur = job['end'] + 3.6
audio = np.zeros(int((dur+0.2)*vo.SR), dtype=np.float32)
for L, s in zip(LINES, starts):
    a = vo._line(L); i = int(s*vo.SR); audio[i:i+len(a)] += a[:len(audio)-i]
out = pathlib.Path('/home/claude/reels/out3'); out.mkdir(exist_ok=True)
mp4 = engine2.render(job, str(out))
wav = str(out/f'{name}_mix.wav')
soundtrack.make(dur, draw=(0.4,job['end']-0.8), end=job['end'], mood='warm', bpm=92, seed=seed, out=wav, pen=False, beat=True)
vo.lay_under(wav, audio)
final = str(out/f'{name}_voiced.mp4')
subprocess.run(['ffmpeg','-y','-loglevel','error','-i',str(out/f'{name}_silent.mp4'),'-i',wav,'-c:v','copy','-c:a','aac','-b:a','192k','-shortest','-movflags','+faststart',final],check=True)
print(final, label)
