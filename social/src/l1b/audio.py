import wave,numpy as np
from scipy.signal import butter,lfilter
w=wave.open('vo2.wav');SR=w.getframerate();w.close();END=69.4
def wr(n,x):
    f=wave.open(n,'wb');f.setnchannels(1);f.setsampwidth(2);f.setframerate(SR);f.writeframes((np.clip(x,-1,1)*32767).astype('<i2').tobytes());f.close()
s=np.zeros(int(END*SR),np.float32)
def tone(t0,f,d,v=.2,f2=None,att=.01):
    n=int(d*SR);t=np.arange(n)/SR;fr=np.linspace(f,f2 or f,n);ph=2*np.pi*np.cumsum(fr)/SR
    env=np.minimum(1,t/att)*np.exp(-t/(d*.35));i=int(t0*SR);s[i:i+n]+=(np.sin(ph)+.25*np.sin(2*ph))*env*v
for c in [5.0,7.59,10.0,13.03,14.2,16.3,17.7,33.87,36.87,38.8,45.0,46.6,51.5,54.8,56.5,59.37,63.1,65.02]: tone(c,330,.16,.05,220)
for k,tt in enumerate([20.5,24.5,28.57]): tone(tt,[523,587,659][k],.3,.13);tone(tt+.1,[784,880,988][k],.3,.08)
for k in range(3): tone(34.12+k*.9,440 if k<2 else 660,.22,.14)
tone(2.35,150,.4,.18,90)
tone(43.3,150,.5,.22,85);tone(50.2,150,.5,.22,85)
for k,f in enumerate([523,659,784]): tone(58.4+k*.09,f,.3,.1)
for k,f in enumerate([523,659,784,1047]): tone(59.51+k*.1,f,.35,.1)
for k,f in enumerate([523,659,784,1047,1319]): tone(65.16+k*.09,f,.45,.11)
b,a_=butter(2,2500/(SR/2));s=lfilter(b,a_,s).astype(np.float32);wr('sfx.wav',s*.9)
