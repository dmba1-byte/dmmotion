"""Original soundtrack for DM Motion reels: soft pad + felt-piano arpeggio + light beat,
pencil-on-paper texture while lines draw, and a soft chime on the end card. Fully synthesized."""
import numpy as np, subprocess, sys
from scipy.signal import butter, sosfilt

SR = 48000
def midi(n): return 440.0 * 2 ** ((n - 69) / 12)

PROGS = {  # (root midi, chord intervals) per bar
    'calm':   [(60, [0, 4, 7, 11]), (57, [0, 3, 7, 10, 14]), (53, [0, 4, 7, 11]), (55, [0, 4, 7, 9])],
    'warm':   [(62, [0, 3, 7, 10]), (58, [0, 4, 7, 11]), (55, [0, 4, 7, 14]), (57, [0, 3, 7, 10])],
    'bright': [(65, [0, 4, 7, 11]), (62, [0, 3, 7, 10]), (58, [0, 4, 7, 11]), (60, [0, 4, 7, 9])],
}

def lp(x, f, order=2):
    return sosfilt(butter(order, f, 'low', fs=SR, output='sos'), x)
def bp(x, lo, hi):
    return sosfilt(butter(2, [lo, hi], 'band', fs=SR, output='sos'), x)

def env_adsr(n, a, r):
    e = np.ones(n); A = min(int(a * SR), n // 2); R = min(int(r * SR), n // 2)
    if A: e[:A] = np.linspace(0, 1, A)
    if R: e[-R:] *= np.linspace(1, 0, R)
    return e

def make(dur, draw=(0.4, 10.6), end=11.4, mood='calm', bpm=92, seed=1, out='track.wav', pen=True, beat=True):
    rng = np.random.default_rng(seed)
    N = int(dur * SR); t = np.arange(N) / SR
    mix = np.zeros((2, N))
    prog = PROGS[mood]; bar = 4 * 60 / bpm
    # pad
    for i in range(int(np.ceil(dur / bar))):
        root, iv = prog[i % len(prog)]
        s0 = int(i * bar * SR); n = min(int(bar * SR) + int(0.5 * SR), N - s0)
        if n <= 0: break
        tt = np.arange(n) / SR; sig = np.zeros(n)
        for k, v in enumerate(iv):
            f = midi(root - 12 + v)
            det = 1 + 0.003 * (k - 2)
            sig += 0.5 * np.sin(2 * np.pi * f * tt) + 0.18 * np.sin(2 * np.pi * f * det * 2 * tt)
        sig = lp(sig, 1400) * env_adsr(n, 0.9, 0.9) * 0.05
        mix[0, s0:s0 + n] += sig; mix[1, s0:s0 + n] += sig * 0.92
    # felt piano arpeggio (8ths), starts after 1 bar fraction
    step = 60 / bpm / 2
    pattern = [0, 2, 1, 3, 2, 1, 3, 2]
    j = 0; ts = 0.6
    while ts < dur - 0.3:
        bi = int(ts // bar); root, iv = prog[bi % len(prog)]
        note = root + iv[pattern[j % len(pattern)] % len(iv)]
        n = int(1.6 * SR); s0 = int(ts * SR); n = min(n, N - s0)
        tt = np.arange(n) / SR; f = midi(note)
        tone = (np.sin(2*np.pi*f*tt) + 0.35*np.sin(2*np.pi*2*f*tt)*np.exp(-tt*6) + 0.12*np.sin(2*np.pi*3*f*tt)*np.exp(-tt*9))
        tone *= np.exp(-tt * 2.6) * (1 - np.exp(-tt * 400))
        vel = 0.055 * (0.8 + 0.4 * rng.random())
        pan = 0.5 + 0.3 * np.sin(j * 1.3)
        mix[0, s0:s0 + n] += tone * vel * (1 - pan) * 2; mix[1, s0:s0 + n] += tone * vel * pan * 2
        ts += step; j += 1
    # light beat after first bar
    if beat:
        b = 60 / bpm; tb = bar * 0.5
        k = 0
        while tb < end:
            s0 = int(tb * SR)
            if k % 2 == 0:  # soft kick
                n = int(0.35 * SR); n = min(n, N - s0); tt = np.arange(n) / SR
                f = 50 + 70 * np.exp(-tt * 30)
                kick = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 9) * 0.22
                mix[:, s0:s0 + n] += kick
            # hat on offbeat
            s1 = int((tb + b / 2) * SR); n = int(0.05 * SR)
            if s1 + n < N:
                hat = bp(rng.standard_normal(n), 7000, 12000) * np.exp(-np.arange(n) / SR * 90) * 0.05
                mix[0, s1:s1 + n] += hat * 0.8; mix[1, s1:s1 + n] += hat
            tb += b; k += 1
    # pencil texture while drawing: strokes of band-limited noise
    if pen:
        a, z = draw; ts = a
        while ts < z:
            ln = 0.12 + 0.35 * rng.random(); n = int(ln * SR); s0 = int(ts * SR)
            n = min(n, N - s0)
            if n <= 0: break
            tt = np.arange(n) / SR
            nz = bp(rng.standard_normal(n), 1800 + 900 * rng.random(), 6500)
            grain = 0.6 + 0.4 * np.sign(np.sin(2 * np.pi * (30 + 40 * rng.random()) * tt))
            e = np.sin(np.pi * tt / ln) ** 0.6
            st = lp(nz, 4500) * grain * e * 0.011
            mix[0, s0:s0 + n] += st * 0.9; mix[1, s0:s0 + n] += st
            ts += ln + 0.03 + 0.12 * rng.random()
    # end-card chime + soft whoosh
    s0 = int(end * SR); n = min(int(3.5 * SR), N - s0)
    if n > 0:
        tt = np.arange(n) / SR; root, iv = prog[0]
        ch = sum(np.sin(2 * np.pi * midi(root + 12 + v) * tt) * np.exp(-tt * (1.4 + 0.2 * i)) for i, v in enumerate(iv[:3]))
        ch *= (1 - np.exp(-tt * 300)) * 0.06
        wn = int(0.6 * SR); wh = lp(rng.standard_normal(wn), 2500) * np.hanning(wn) * 0.04
        mix[:, s0:s0 + n] += ch
        w0 = max(0, s0 - int(0.3 * SR)); mix[:, w0:w0 + wn] += wh[:min(wn, N - w0)]
    # master fade in/out
    fade = np.ones(N); fi = int(0.25 * SR); fo = int(1.2 * SR)
    fade[:fi] = np.linspace(0, 1, fi); fade[-fo:] = np.linspace(1, 0, fo)
    mix *= fade
    mix /= max(1e-9, np.abs(mix).max()) / 0.8
    pcm = (mix.T * 32767).astype(np.int16)
    raw = out + '.raw'; pcm.tofile(raw)
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 's16le', '-ar', str(SR), '-ac', '2', '-i', raw,
                    '-af', 'loudnorm=I=-16:TP=-1.5:LRA=11', '-ar', str(SR), out], check=True)
    import os; os.remove(raw)
    return out

if __name__ == '__main__':
    make(16.0, out=sys.argv[1] if len(sys.argv) > 1 else 'test.wav')
