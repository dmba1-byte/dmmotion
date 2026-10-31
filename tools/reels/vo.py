"""Voiceover for DM Motion reels.

Piper neural TTS running locally in this container — no API, no account, no
credits. The voice model came off a GitHub release, which is one of the few
hosts this sandbox can reach, and is cached on disk.

The whole script is read as one continuous take. An earlier version synthesized
each line separately, trimmed the breath off both ends and dropped the pieces
onto fixed timestamps; it sounded chopped up, because it was. Here the narration
is built once, end to end, with real pauses between sentences, and the picture
is cut to where the words actually land.
"""
import hashlib, pathlib, wave
import numpy as np
from scipy.signal import resample_poly

SR = 48000
VOICE = '/home/claude/reels/voices/en-us-ryan-high.onnx'
CACHE = pathlib.Path('/home/claude/reels/voices/cache'); CACHE.mkdir(parents=True, exist_ok=True)
_v = None

LEN_SCALE = 1.00      # natural pace; slower read sounded laboured
PAUSE = 0.24          # between lines of the script
SUB_PAUSE = 0.15      # between sentences inside one line
EDGE = 0.045          # silence kept either side of a line, so nothing clips


def _voice():
    global _v
    if _v is None:
        from piper import PiperVoice
        _v = PiperVoice.load(VOICE)
    return _v


def _tidy(a):
    """Trim piper's padding down to a consistent sliver — never into the speech."""
    nz = np.nonzero(np.abs(a) > 0.0035)[0]
    if not len(nz):
        return a
    pad = int(EDGE * SR)
    return a[max(0, nz[0] - pad):min(len(a), nz[-1] + pad)]


def _line(text):
    """One line of script. Piper splits it into sentences; we keep them together
    with a natural beat between, instead of letting them butt up or drift apart."""
    key = hashlib.sha1(f'{text}|{LEN_SCALE}|{SUB_PAUSE}'.encode()).hexdigest()[:16]
    p = CACHE / f'{key}.npy'
    if p.exists():
        return np.load(p)
    from piper import SynthesisConfig
    cfg = SynthesisConfig(length_scale=LEN_SCALE, normalize_audio=True)
    parts, rate = [], None
    for ch in _voice().synthesize(text, syn_config=cfg):
        rate = ch.sample_rate
        parts.append(_tidy(np.asarray(ch.audio_float_array, dtype=np.float32)))
    if not parts:
        return np.zeros(0, dtype=np.float32)
    gap = np.zeros(int(SUB_PAUSE * rate), dtype=np.float32)
    a = parts[0]
    for q in parts[1:]:
        a = np.concatenate([a, gap, q])
    if rate != SR:
        a = resample_poly(a, SR, rate)
    a = a.astype(np.float32)
    np.save(p, a)
    return a


def narrate(lines, lead=0.10, pause=PAUSE):
    """Read the whole script as one take.

    Returns (audio, starts, total) — starts[i] is when line i begins, in seconds
    from the top of the reel, so the visual beats can be cut to the voice.
    """
    gap = np.zeros(int(pause * SR), dtype=np.float32)
    out = [np.zeros(int(lead * SR), dtype=np.float32)]
    starts, t = [], lead
    for i, L in enumerate(lines):
        a = _line(L)
        starts.append(round(t, 3))
        out.append(a)
        t += len(a) / SR
        if i < len(lines) - 1:
            out.append(gap); t += pause
    return np.concatenate(out), starts, round(t, 3)


def duration(text):
    return len(_line(text)) / SR


def lay_under(wav_path, narration, duck=0.30):
    """Put a finished narration over a finished soundtrack, ducking the bed."""
    f = wave.open(str(wav_path)); ch = f.getnchannels(); n = f.getnframes()
    bed = np.frombuffer(f.readframes(n), dtype=np.int16).astype(np.float32) / 32768.0
    f.close()
    bed = bed.reshape(-1, ch).T if ch > 1 else bed.reshape(1, -1)
    N = bed.shape[1]
    v = np.zeros(N, dtype=np.float32)
    m = min(len(narration), N)
    v[:m] = narration[:m]
    # follow the voice envelope so the music lifts in the gaps instead of
    # staying flattened for the whole reel
    win = int(0.09 * SR)
    env = np.convolve(np.abs(v), np.ones(win) / win, mode='same')
    env = env / (env.max() + 1e-9)
    gain = 1.0 - (1.0 - duck) * np.clip(env * 3.2, 0, 1)
    k = int(0.05 * SR)
    gain = np.convolve(gain, np.ones(k) / k, mode='same')
    out = bed * gain + v * 0.96
    peak = np.max(np.abs(out))
    if peak > 0.97:
        out *= 0.97 / peak
    pcm = (np.clip(out, -1, 1) * 32767).astype(np.int16)
    w = wave.open(str(wav_path), 'wb')
    w.setnchannels(bed.shape[0]); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes(pcm.T.tobytes() if bed.shape[0] > 1 else pcm.tobytes())
    w.close()
