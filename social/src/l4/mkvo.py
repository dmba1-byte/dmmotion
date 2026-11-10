import sys,json,wave,re,numpy as np
sys.path.insert(0,'/home/claude/reels')
import vo
from scipy.signal import resample_poly
k=vo._kokoro();L=json.load(open('script.json'))
def line(t):
    if 'ption ' in t:
        ph=k.tokenizer.phonemize(t,'en-us').replace('ˈɑːpʃən ɐ','ˈɑːpʃən ˈeɪ')
        a,r=k.create(ph,voice=vo.KVOICE,speed=0.92 if len(t)<12 else vo.SPEED,is_phonemes=True)
        a=vo._tidy(np.asarray(a,np.float32));return resample_poly(a,vo.SR,r).astype(np.float32)
    return vo._line(t)
PRE={6:.5,8:.55,10:.55,12:3.3};POST={6:.45,8:.45,10:.45}
out=[np.zeros(int(.1*vo.SR),np.float32)];t=.1;VT=[];SUBS=[]
def sil(d):
    global t
    out.append(np.zeros(int(d*vo.SR),np.float32));t+=d
for i,l in enumerate(L):
    if i: sil(PRE.get(i,POST.get(i-1,.26)))
    a=line(l);s=t;out.append(a);t+=len(a)/vo.SR
    e=np.abs(a);w=int(.02*vo.SR);env=np.convolve(e,np.ones(w)/w,'same')<0.012;gaps=[];j=0;n=len(a)
    while j<n:
        if env[j]:
            j0=j
            while j<n and env[j]: j+=1
            if (j-j0)/vo.SR>.15 and j0>0 and j<n: gaps.append((round(s+j0/vo.SR,2),round(s+j/vo.SR,2)))
        else: j+=1
    VT.append([round(s,2),round(t,2),gaps])
    # subtitle chunks
    parts=[p.strip() for p in re.split(r'(?<=[.?!,])\s+',l) if p.strip()]
    disp=lambda x:x.replace('nineteen forty-two','1942').replace('Four hundred and ninety-two','492').replace('nine hundred and fifteen','915').replace('nineteen seventy-eight','1978').replace('nineteen seventy','1970').replace('nineteen oh five','1905').replace('a hundred and twelve','112').replace('seventy-two','72').replace('Saint','St.')
    # merge parts to match gaps+1 groups by nearest char proportion
    bounds=[s]+[ (g[0]+g[1])/2 for g in gaps]+[t]
    if len(parts)==len(gaps)+1: groups=parts
    else:
        tot=sum(len(p) for p in parts);groups=[];acc=0;cur=[];gi=1
        for p in parts:
            cur.append(p);acc+=len(p)
            frac=(bounds[gi]-s)/(t-s) if gi<len(bounds)-1 else 2
            if acc/tot>=frac-0.08 and gi<len(bounds)-1: groups.append(' '.join(cur));cur=[];gi+=1
        if cur: groups.append(' '.join(cur))
        while len(groups)<len(gaps)+1: groups.append('')
        if len(groups)>len(gaps)+1: groups=groups[:len(gaps)]+[' '.join(groups[len(gaps):])]
    for gi,gp in enumerate(groups):
        if gp: SUBS.append([round(bounds[gi]+(0 if gi==0 else .12),2),round(bounds[gi+1]-(0.05 if gi<len(groups)-1 else 0),2),disp(gp)])
a=np.concatenate(out+[np.zeros(int(.8*vo.SR),np.float32)])
w=wave.open('vo.wav','wb');w.setnchannels(1);w.setsampwidth(2);w.setframerate(vo.SR);w.writeframes((np.clip(a,-1,1)*32767).astype('<i2').tobytes());w.close()
json.dump({'VT':VT,'SUBS':SUBS,'END':round(t+.8,2)},open('timing.json','w'))
for i,v in enumerate(VT): print(i,v[:2])
for x in SUBS: print(x)
print('END',round(t+.8,2))
