"""Voiced story reel: a flat elevation builds itself."""
import sys, zlib, json, pathlib, subprocess, numpy as np, wave
sys.path.insert(0,'/home/claude/reels')
from gen import engine2, jobs as J, elevs as EV
from gen.draw import fmt_ft
import vo, soundtrack
kind, style, name = sys.argv[1], sys.argv[2], sys.argv[3]
seed = zlib.crc32(name.encode()) % 9999
job, label = J.job_elev(name, seed, kind, style, 'Nobody reads<br>a flat elevation.', 'so watch this one build itself', 'Send me your drawing')
ee = EV.LAST['e']; top = max([z for z, n in ee.levels] or [ee.Hmax])
job['spec'] = f"{fmt_ft(ee.W)} WIDE · {fmt_ft(top)} TALL"
job.update(mood='warm', bpm=92, seed=seed, hook_out=2.0, cam_y=0)
import os
FC=engine2.fit_cam([job['layers'][0]['svg']], margin=84)
job.update(cam_y=FC['cam_y'], layers_meta=[{'id':'Le','cam':[[0,FC['s']*0.97,FC['cx'],FC['cy']]]}]); print('FIT',FC)
if os.environ.get('FX'): job['fx']=os.environ['FX']
art = 'an' if label[0].lower() in 'aeiou' else 'a'
MODE = sys.argv[4] if len(sys.argv) > 4 else 'nobody'
if MODE == 'name':
    job['hook'] = 'Name this<br>house style.'; job['sub'] = 'you get ten seconds'; job['hook_out'] = 4.0
    LINES = ["Name this house style.", "You've get ten seconds.".replace("get","got"), "Watch the roofline. Watch the windows.",
             f"It's {art} {label}. Did you get it?", "Now imagine your drawing doing this.", "Send me your drawing."]
    starts = [0.1, 2.0, 4.2, 8.4, 10.6, 12.3]
    subs = [[0.1,1.9,'Name this<br>house style.'],[2.0,4.1,'You get<br>ten seconds.'],[4.2,8.3,'Watch the roofline.<br>Watch the windows.'],
            [8.4,10.5,f"{art.capitalize()} {label}.<br>Did you get it?"],[10.6,12.2,'Now imagine<br>your drawing<br>doing this.'],[12.3,15.5,'Send me your drawing.']]
else:
    LINES = ["Nobody reads a flat elevation.", "Watch it build itself.", "Walls, roof, every window where you drew it.",
             "Siding, trim, the front door.", "Now they see a house, not lines.", "Send me your drawing."]
    starts = [0.1, 2.2, 3.7, 6.2, 8.1, 12.3]
    subs = [[0.1,2.1,'Nobody reads<br>a flat elevation.'],[2.2,3.6,'Watch it build itself.'],[3.7,6.1,'Every window<br>where you drew it.'],
            [6.2,8.0,'Siding, trim,<br>the front door.'],[8.1,11.0,'Now they see<br>a house, not lines.'],[12.3,15.5,'Send me your drawing.']]
job['subs'] = subs
dur = job['end'] + 3.6
audio = np.zeros(int((dur+0.2)*vo.SR), dtype=np.float32)
for L, s in zip(LINES, starts):
    a = vo._line(L); i = int(s*vo.SR); audio[i:i+len(a)] += a[:len(audio)-i]
out = pathlib.Path('/home/claude/reels/out3'); out.mkdir(exist_ok=True)
mp4 = engine2.render(job, str(out))
# swap soundtrack: music bed + narration
wav = str(out/f'{name}_mix.wav')
soundtrack.make(dur, draw=job.get('draw_window',(0.4,job['end']-0.8)), end=job['end'], mood='warm', bpm=92, seed=seed, out=wav, pen=False, beat=True)
vo.lay_under(wav, audio)
final = str(out/f'{name}_voiced.mp4')
subprocess.run(['ffmpeg','-y','-loglevel','error','-i',str(out/f'{name}_silent.mp4'),'-i',wav,'-c:v','copy','-c:a','aac','-b:a','192k','-shortest','-movflags','+faststart',final],check=True)
print(final, label)
