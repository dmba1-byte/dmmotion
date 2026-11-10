import wave,json,numpy as np
from scipy.signal import butter,lfilter
T=json.load(open('timing.json'));V=T['VT'];END=T['END']
w=wave.open('vo.wav');SR=w.getframerate();w.close()
def wr(n,x):
    f=wave.open(n,'wb');f.setnchannels(1);f.setsampwidth(2);f.setframerate(SR);f.writeframes((np.clip(x,-1,1)*32767).astype('<i2').tobytes());f.close()
s=np.zeros(int((END+1)*SR),np.float32)
def tone(t0,f,d,v=.2,f2=None,att=.01):
    n=int(d*SR);t=np.arange(n)/SR;fr=np.linspace(f,f2 or f,n);ph=2*np.pi*np.cumsum(fr)/SR
    env=np.minimum(1,t/att)*np.exp(-t/(d*.35));i=int(t0*SR);s[i:i+n]+=(np.sin(ph)+.25*np.sin(2*ph))*env*v
for i in [1,2,3,4,5,12,13,14,15,16]: tone(V[i][0]-.12,330,.16,.05,220)
for k,i in enumerate([6,8,10]): tone(V[i][0]-.2,[523,587,659][k],.3,.13);tone(V[i][0]-.1,[784,880,988][k],.3,.08)
m=V[11][1]+.25
for k in range(3): tone(m+.25+k*.9,440 if k<2 else 660,.22,.14)
tone(V[3][2][0][1]+.45 if V[3][2] else V[3][0]+3,150,.5,.2,85)
tone(V[12][2][0][0]-.3,150,.5,.2,85)
for k,f in enumerate([523,659,784]): tone(V[13][0]+1.3+k*.09,f,.3,.1)
for k,f in enumerate([523,659,784]): tone(V[14][0]+1.5+k*.09,f,.3,.1)
for k,f in enumerate([523,659,784,1047,1319]): tone(V[16][0]+k*.09,f,.45,.11)
b,a_=butter(2,2500/(SR/2));s=lfilter(b,a_,s).astype(np.float32);wr('sfx.wav',s*.9)
