import sys,json,wave,numpy as np
sys.path.insert(0,'/home/claude/reels')
import vo
from scipy.signal import resample_poly
k=vo._kokoro();L=json.load(open('script.json'))
def line(t):
    if t.startswith('Option ') or 'A.D.A.' in t:
        ph=k.tokenizer.phonemize(t,'en-us').replace('ˈɑːpʃən ɐ','ˈɑːpʃən ˈeɪ').replace('ˈeɪ.dˈiː.ˈeɪ','ˌeɪdiːˈeɪ')
        a,r=k.create(ph,voice=vo.KVOICE,speed=0.92 if len(t)<12 else vo.SPEED,is_phonemes=True)
        a=vo._tidy(np.asarray(a,np.float32));return resample_poly(a,vo.SR,r).astype(np.float32)
    return vo._line(t)
PRE={5:.5,7:.55,9:.55,11:3.3};POST={5:.45,7:.45,9:.45}
out=[np.zeros(int(.1*vo.SR),np.float32)];t=.1;info=[]
def sil(d):
    global t
    out.append(np.zeros(int(d*vo.SR),np.float32));t+=d
for i,l in enumerate(L):
    if i: sil(PRE.get(i,POST.get(i-1,vo.PAUSE)))
    a=line(l);s=t;out.append(a);t+=len(a)/vo.SR
    # internal pauses
    e=np.abs(a);w=int(.02*vo.SR);env=np.convolve(e,np.ones(w)/w,'same')<0.012;gaps=[];j=0;n=len(a)
    while j<n:
        if env[j]:
            j0=j
            while j<n and env[j]: j+=1
            if (j-j0)/vo.SR>.15 and j0>0 and j<n: gaps.append((round(s+j0/vo.SR,2),round(s+j/vo.SR,2)))
        else: j+=1
    info.append((i,round(s,2),round(t,2),gaps))
a=np.concatenate(out)
w=wave.open('vo2.wav','wb');w.setnchannels(1);w.setsampwidth(2);w.setframerate(vo.SR);w.writeframes((np.clip(a,-1,1)*32767).astype('<i2').tobytes());w.close()
for x in info: print(x)
print('total',round(t,2))
