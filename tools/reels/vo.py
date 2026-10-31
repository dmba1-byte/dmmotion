"""Voiceover for DM Motion reels.

Piper neural TTS running locally in this container — no API, no account, no
credits. The voice model came off a GitHub release, which is one of the few
hosts this sandbox can reach, and is cached on disk. Lines are synthesized
once and reused, so a re-render costs nothing but CPU.
"""
import hashlib, pathlib, wave
import numpy as np
from scipy.signal import resample_poly

SR = 48000
VOICE = '/home/claude/reels/voices/en-us-ryan-high.onnx'
CACHE = pathlib.Path('/home/claude/reels/voices/cache'); CACHE.mkdir(parents=True, exist_ok=True)
_v = None


def _voice():
    global _v
    if _v is None:
        from piper import PiperVoice
        _v = PiperVoice.load(VOICE)
    return _v


def say(text):
    """One line as float32 mono at 48 kHz. Cached by content hash."""
    p = CACHE / f'{hashlib.sha1(text.encode()).hexdigest()[:16]}.wav'
    if not p.exists():
        with wave.open(str(p), 'wb') as w:
            _voice().synthesize_wav(text, w)
    f = wave.open(str(p))
    a = np.frombuffer(f.readframes(f.getnframes()), dtype=np.int16).astype(np.float32) / 32768.0
    if f.getnchannels() == 2:
        a = a.reshape(-1, 2).mean(1)
    sr = f.getframerate(); f.close()
    if sr != SR:
        a = resample_poly(a, SR, sr)
    # trim the silence piper leaves on both ends so placement is exact
    nz = np.nonzero(np.abs(a) > 0.004)[0]
    if len(nz):
        a = a[max(0, nz[0] - 960):min(len(a), nz[-1] + 960)]
    return a.astype(np.float32)


def duration(text):
    return len(say(text)) / SR


def mix_into(wav_path, lines, gain=0.92, duck=0.34):
    """Lay (time, text) lines over an existing soundtrack, ducking the bed under each."""
    if not lines:
        return
    f = wave.open(str(wav_path)); ch = f.getnchannels(); n = f.getnframes()
    bed = np.frombuffer(f.readframes(n), dtype=np.int16).astype(np.float32) / 32768.0
    f.close()
    bed = bed.reshape(-1, ch).T if ch > 1 else bed.reshape(1, -1)
    N = bed.shape[1]
    voice = np.zeros(N, dtype=np.float32)
    env = np.ones(N, dtype=np.float32)       # 1 = music at full, duck = music pulled down
    ramp = int(0.14 * SR)
    for t, txt in lines:
        a = say(txt) * gain
        s0 = int(t * SR); m = min(len(a), N - s0)
        if m <= 0:
            continue
        voice[s0:s0 + m] += a[:m]
        lo = max(0, s0 - ramp); hi = min(N, s0 + m + ramp)
        seg = np.full(hi - lo, duck, dtype=np.float32)
        r = min(ramp, len(seg) // 2)
        if r:
            seg[:r] = np.linspace(1, duck, r)
            seg[-r:] = np.linspace(duck, 1, r)
        env[lo:hi] = np.minimum(env[lo:hi], seg)
    out = bed * env + voice
    peak = np.max(np.abs(out))
    if peak > 0.97:
        out *= 0.97 / peak
    pcm = (np.clip(out, -1, 1) * 32767).astype(np.int16)
    w = wave.open(str(wav_path), 'wb')
    w.setnchannels(bed.shape[0]); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes(pcm.T.tobytes() if bed.shape[0] > 1 else pcm.tobytes())
    w.close()
