import wave,numpy as np
from scipy.signal import butter,lfilter
w=wave.open('vo2.wav');SR=w.getframerate();w.close();END=88.0
def wr(n,x):
    f=wave.open(n,'wb');f.setnchannels(1);f.setsampwidth(2);f.setframerate(SR);f.writeframes((np.clip(x,-1,1)*32767).astype('<i2').tobytes());f.close()
s=np.zeros(int(END*SR),np.float32)
def tone(t0,f,d,v=.2,f2=None,att=.01):
    n=int(d*SR);t=np.arange(n)/SR;fr=np.linspace(f,f2 or f,n);ph=2*np.pi*np.cumsum(fr)/SR
    env=np.minimum(1,t/att)*np.exp(-t/(d*.35));i=int(t0*SR);s[i:i+n]+=(np.sin(ph)+.25*np.sin(2*ph))*env*v
for c in [2.88,5.81,10.23,12.78,14.63,15.98,19.75,22.3,25.76,48.9,51.95,59.6,64.83,66.6,70.85,74.19,77.76,80.51,83.7]: tone(c,330,.16,.05,220)
for k,tt in enumerate([28.95,34.87,41.76]): tone(tt,[523,587,659][k],.3,.13);tone(tt+.1,[784,880,988][k],.3,.08)
for k in range(3): tone(49.15+k*.92,440 if k<2 else 660,.22,.14)
tone(22.4,150,.4,.18,90);tone(69.9,150,.4,.18,90)
tone(54.25,220,.7,.16,60,att=.02)
tone(58.0,150,.5,.22,85);tone(63.6,150,.5,.22,85)
for k in range(4): tone(61.8+k*.35,392,.12,.07)
for k,f in enumerate([523,659,784]): tone(73.1+k*.09,f,.3,.1)
for k,f in enumerate([523,659,784,1047]): tone(80.65+k*.1,f,.35,.1)
for k,f in enumerate([523,659,784,1047,1319]): tone(83.84+k*.09,f,.45,.11)
b,a_=butter(2,2500/(SR/2));s=lfilter(b,a_,s).astype(np.float32);wr('sfx.wav',s*.9)
