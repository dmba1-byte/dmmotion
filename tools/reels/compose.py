import subprocess
def overlay(base, items, out, fade=0.25):
    """items: [(scene_mp4, t0, dur)] -> scenes cross-fade over the base video; base audio kept."""
    cmd = ['ffmpeg', '-y', '-loglevel', 'error', '-i', base]
    for sc, t0, d in items: cmd += ['-i', sc]
    fc = []; last = '0:v'
    for i, (sc, t0, d) in enumerate(items, 1):
        fc.append(f"[{i}:v]setpts=PTS-STARTPTS+{t0}/TB,format=yuva420p,fade=t=in:st={t0}:d={fade}:alpha=1,fade=t=out:st={t0+d-fade}:d={fade}:alpha=1[s{i}]")
        fc.append(f"[{last}][s{i}]overlay=eof_action=pass:format=auto[v{i}]"); last = f'v{i}'
    cmd += ['-filter_complex', ';'.join(fc), '-map', f'[{last}]', '-map', '0:a', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20', '-pix_fmt', 'yuv420p', '-c:a', 'copy', '-movflags', '+faststart', out]
    subprocess.run(cmd, check=True); return out
