"""Re-render queued reels after an engine change, straight into the repo folder.

Usage:  python3 rerender.py <name> [<name> ...]
        python3 rerender.py --all-pending
"""
import json, pathlib, shutil, subprocess, sys, time

sys.path.insert(0, '/home/claude/reels')
Q = pathlib.Path('/home/claude/dmmotion/social/q')
OUT = pathlib.Path('/home/claude/reels/rr')
OUT.mkdir(exist_ok=True)

batch = {j['name']: j for j in json.load(open('/home/claude/reels/batch2.json'))}
extras = {e['name']: e for e in json.load(open('/home/claude/reels/extras.json'))}
queue = json.load(open(Q / 'queue.json'))


def render_one(name):
    if name in batch:
        from gen import engine2
        engine2.render(batch[name], str(OUT))
    elif name in extras:
        src = extras[name]['src']
        if src == 'r_explainer_how':
            from gen import explainer
            explainer.render(str(OUT), name=name)
        elif src == 'r_edu_kitchen':
            from gen import kitchen
            kitchen.render(str(OUT), name=name)
        elif src.startswith('r_rule_'):
            from gen import rules
            rules.render(src.replace('r_rule_', ''), str(OUT))
            for suf in ('.mp4', '_silent.mp4', '_music.mp3'):
                p = OUT / f'{src}{suf}'
                if p.exists():
                    p.rename(OUT / f'{name}{suf}')
        else:
            raise SystemExit(f'unknown src {src}')
    else:
        raise SystemExit(f'{name} not in batch2.json or extras.json')

    moved = []
    for suf in ('.mp4', '_silent.mp4', '_music.mp3'):
        s = OUT / f'{name}{suf}'
        if not s.exists():
            raise SystemExit(f'missing output {s}')
        shutil.copy2(s, Q / f'{name}{suf}')
        moved.append(f'{name}{suf}')
    return moved


if __name__ == '__main__':
    args = sys.argv[1:]
    if args == ['--all-pending']:
        args = [e['name'] for e in queue if e['status'] == 'approved']
    for i, n in enumerate(args, 1):
        t0 = time.time()
        files = render_one(n)
        dur = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
                              '-of', 'csv=p=0', str(Q / f'{n}_silent.mp4')],
                             capture_output=True, text=True).stdout.strip()
        print(f'[{i}/{len(args)}] {n}  {float(dur):.1f}s  ({time.time()-t0:.0f}s render)', flush=True)
