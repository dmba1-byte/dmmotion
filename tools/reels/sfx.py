"""Reveal sound effects, synthesized. sfx.add(wav, events): events = [(t, kind)]."""
import numpy as np, wave
from scipy.signal import butter, sosfilt
SR = 48000
def _lp(x, f): return sosfilt(butter(2, f, 'low', fs=SR, output='sos'), x)
def _bp(x, a, b): return sosfilt(butter(2, [a, b], 'band', fs=SR, output='sos'), x)
def tick():
    n = int(.06*SR); t = np.arange(n)/SR
    return np.sin(2*np.pi*1800*t)*np.exp(-t*70)*.5
def whoosh(d=.45):
    n = int(d*SR); r = np.random.default_rng(3).standard_normal(n)
    return _bp(r, 400, 5000)*np.sin(np.pi*np.arange(n)/n)**2*.35
def riser(d=.7):
    n = int(d*SR); t = np.arange(n)/SR; f = 300+900*(t/d)**2
    return np.sin(2*np.pi*np.cumsum(f)/SR)*(t/d)**2*.28
def hit():
    n = int(.7*SR); t = np.arange(n)/SR
    return (np.sin(2*np.pi*(70-30*t)*t)*np.exp(-t*7)*.9 + _lp(np.random.default_rng(5).standard_normal(n), 900)*np.exp(-t*20)*.4)
def buzz():
    n = int(.35*SR); t = np.arange(n)/SR
    return np.sign(np.sin(2*np.pi*110*t))*np.exp(-t*5)*.22
def chime():
    n = int(1.4*SR); t = np.arange(n)/SR
    return sum(np.sin(2*np.pi*f*t)*np.exp(-t*(3+i)) for i, f in enumerate([784, 988, 1175]))*.22*(1-np.exp(-t*400))
KINDS = dict(tick=tick, whoosh=whoosh, riser=riser, hit=hit, buzz=buzz, chime=chime)
def add(path, events, gain=.8):
    f = wave.open(str(path)); ch = f.getnchannels(); n = f.getnframes()
    x = np.frombuffer(f.readframes(n), dtype=np.int16).astype(np.float32)/32768; f.close()
    x = x.reshape(-1, ch).T.copy(); N = x.shape[1]
    for t, k in events:
        s = KINDS[k](); i = int(t*SR)
        if i >= N: continue
        m = min(len(s), N-i)
        for c in range(ch): x[c, i:i+m] += s[:m]*gain
    x /= max(1, np.abs(x).max()/.95)
    w = wave.open(str(path), 'wb'); w.setnchannels(ch); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((x.T*32767).astype(np.int16).tobytes()); w.close()
