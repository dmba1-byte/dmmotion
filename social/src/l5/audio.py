"""L5 SFX — rebuilt for the trimmed timeline (voice_t.wav, video END=141.0)"""
import wave, numpy as np
from scipy.signal import butter, lfilter

END=141.0
w=wave.open('/home/claude/vox/l5/audio/voice_t.wav');SR=w.getframerate();w.close()
s=np.zeros(int((END+1)*SR),np.float32)

def wr(n,x):
    f=wave.open(n,'wb');f.setnchannels(1);f.setsampwidth(2);f.setframerate(SR)
    f.writeframes((np.clip(x,-1,1)*32767).astype('<i2').tobytes());f.close()

def tone(t0,f,d,v=.2,f2=None,att=.01):
    n=int(d*SR);t=np.arange(n)/SR;fr=np.linspace(f,f2 or f,n)
    ph=2*np.pi*np.cumsum(fr)/SR
    env=np.minimum(1,t/att)*np.exp(-t/(d*.35))
    i=int(t0*SR)
    if i+n<=len(s): s[i:i+n]+=(np.sin(ph)+.25*np.sin(2*ph))*env*v

# cut swishes at every SEG cut
cuts=[3.50,9.20,12.20,14.90,23.20,26.15,34.39,41.21,49.62,57.16,64.04,70.21,71.81,76.80,81.74,83.77,92.58,97.67,102.61,108.73,110.55]
for c in cuts: tone(c-.10,330,.16,.04,220)

# hook: low tension drone under the crowd / platform
tone(0.3,98,3.0,.045)
tone(3.6,110,5.2,.04)
tone(9.3,92,2.6,.05)             # he looks down
tone(12.25,220,.5,.10,110)       # axe out: low sting
for k in range(3): tone(12.5+k*.75,110,.3,.06)
tone(14.55,60,.5,.14,42)         # smash-cut hit
# title reveal chime
for k,f in enumerate([784,988,1175,1568]): tone(15.0+k*.07,f,.25,.07)
# hoist creak
tone(23.3,80,2.6,.05,95)
# fall: fray ticks, snap, crash
for k in range(5): tone(26.4+k*.2,1400-k*120,.05,.05)
tone(27.50,200,.14,.16,50)       # SNAP
tone(28.35,55,.9,.22,35)         # impact
tone(28.35,300,.12,.15,100)
for k in range(3): tone(28.7+k*.3,80-k*15,.3,.10,40)
# low city: quiet
tone(34.6,160,.4,.05,200)
# brake diagram reveal
tone(41.3,659,.4,.09,784)
# snap diagram: slack, arms out, ratchet bite
tone(50.15,180,.12,.12,60)       # rope slack thunk
for k in range(4): tone(50.55+k*.09,900+k*140,.07,.09)  # arms click out
tone(51.0,523,.35,.10,659)
for k in range(3): tone(50.95+k*.12,1300-k*90,.06,.07)  # BRAKE ENGAGED ratchet
# physics chips
for k,at in enumerate([57.26,59.74,62.09]): tone(at,659+k*120,.25,.08)
# demo: tension again
tone(64.2,98,4.2,.04)
tone(68.7,110,1.4,.05,120)       # axe raised
tone(70.26,200,.14,.16,50)       # cut! snap
tone(70.45,70,.5,.14,45)         # drop
for k in range(4): tone(71.86+k*.09,900+k*140,.07,.10)  # brake bites
tone(72.3,523,.4,.10)            # caught chord
tone(72.42,659,.4,.09)
# all safe: warm arpeggio
for k,f in enumerate([523,659,784,1047]): tone(77.1+k*.09,f,.35,.09)
tone(78.6,1319,.5,.10)
# value flip
tone(92.68,523,.3,.09,659)
tone(93.0,784,.3,.08)
for k in range(4): tone(92.9+k*.22,880+k*110,.2,.06)    # penthouse sparkle
# desk writing scratches
for k in range(5): tone(98.0+k*1.0,2100,.05,.03,1700)
# accident sting
tone(102.75,200,.14,.14,50)
tone(102.95,60,.7,.18,40)
# question stings / option reveals
for k,at in enumerate([110.55,117.66,126.31]): tone(at,659-k*66,.3,.11,784-k*66)
# countdown pulses
for k in range(3): tone(134.91+k*.8,440,.22,.10)
# lock in
tone(137.31,523,.25,.12,659)
tone(137.45,784,.3,.10)
# CTA chimes in the tail
tone(139.6,1047,.35,.10)
tone(139.75,1319,.4,.09)
tone(139.9,1568,.5,.11)

b,a_=butter(2,2500/(SR/2))
s=lfilter(b,a_,s).astype(np.float32)
wr('/home/claude/dmmotion/social/src/l5/sfx.wav',s*.88)
print(f"sfx.wav SR={SR} dur={len(s)/SR:.2f}s")
