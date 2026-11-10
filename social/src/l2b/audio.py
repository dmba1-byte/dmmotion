import wave,numpy as np
from scipy.signal import butter,lfilter
w=wave.open('vo2.wav');SR=w.getframerate();w.close();END=84.0
def wr(n,x):
    f=wave.open(n,'wb');f.setnchannels(1);f.setsampwidth(2);f.setframerate(SR);f.writeframes((np.clip(x,-1,1)*32767).astype('<i2').tobytes());f.close()
s=np.zeros(int(END*SR),np.float32)
def tone(t0,f,d,v=.2,f2=None,att=.01):
    n=int(d*SR);t=np.arange(n)/SR;fr=np.linspace(f,f2 or f,n);ph=2*np.pi*np.cumsum(fr)/SR
    env=np.minimum(1,t/att)*np.exp(-t/(d*.35));i=int(t0*SR);s[i:i+n]+=(np.sin(ph)+.25*np.sin(2*ph))*env*v
for c in [5.15,7.69,9.9,11.9,13.63,16.9,19.76,37.25,40.25,42.0,47.71,49.5,52.9,54.5,56.3,59.5,61.6,63.76,66.0,68.12,71.5,74.5,77.6,79.56]: tone(c,330,.16,.05,220)
for k,tt in enumerate([22.6,27.6,32.45]): tone(tt,[523,587,659][k],.3,.13);tone(tt+.1,[784,880,988][k],.3,.08)
for k in range(3): tone(37.5+k*.9,440 if k<2 else 660,.22,.14)
tone(3.0,150,.4,.18,90);tone(15.4,150,.4,.18,90)
tone(44.3,150,.5,.22,85);tone(52.0,150,.5,.22,85)
for k,f in enumerate([523,659,784]): tone(62.6+k*.09,f,.3,.1)
for k,f in enumerate([523,659,784,1047]): tone(74.64+k*.1,f,.35,.1)
for k,f in enumerate([523,659,784,1047,1319]): tone(79.7+k*.09,f,.45,.11)
b,a_=butter(2,2500/(SR/2));s=lfilter(b,a_,s).astype(np.float32);wr('sfx.wav',s*.9)
