import sys,json,wave,numpy as np
sys.path.insert(0,'/home/claude/reels')
import vo
from scipy.signal import resample_poly
k=vo._kokoro()
L=json.load(open('script.json'))
def line(t):
    if 'A.D.A.' in t:
        ph=k.tokenizer.phonemize(t,'en-us').replace('ˈeɪ.dˈiː.ˈeɪ','ˌeɪdiːˈeɪ')
        a,r=k.create(ph,voice=vo.KVOICE,speed=vo.SPEED,is_phonemes=True)
        a=vo._tidy(np.asarray(a,np.float32));return resample_poly(a,vo.SR,r).astype(np.float32)
    return vo._line(t)
gap=np.zeros(int(vo.PAUSE*vo.SR),np.float32);out=[np.zeros(int(.1*vo.SR),np.float32)];starts=[];t=.1
for i,l in enumerate(L):
    a=line(l);starts.append(round(t,3));out.append(a);t+=len(a)/vo.SR
    if i<len(L)-1: out.append(gap);t+=vo.PAUSE
a=np.concatenate(out)
w=wave.open('vo.wav','wb');w.setnchannels(1);w.setsampwidth(2);w.setframerate(vo.SR);w.writeframes((np.clip(a,-1,1)*32767).astype('<i2').tobytes());w.close()
json.dump({'lines':L,'starts':starts,'total':round(t,3)},open('timing.json','w'));print(starts,round(t,3),sum(len(l.split()) for l in L))
