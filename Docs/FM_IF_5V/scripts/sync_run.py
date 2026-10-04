# Transient sim of the synchronous-detector PLL (docs/MPX_DECODER.md ch.8).
# Run from scripts/:  python3 sync_run.py   (needs ngspice; ~30 s per case)
# psi = phase of I relative to pilot; 38k error = angle(exp(2j*psi)) (0 or 180 deg lock both OK)
import subprocess, numpy as np, sys
def run(tag, AMP=0.5, PILOT=0.10, DFREQ=0.005, VOS=0.0, VBERR=0.0, RI='47k', RZ='7.5k', CI='1u', CP='10n', TSTOP=0.3, PH0=0.5, SR=3e6, RL='1e12', VOSB=None):
    if VOSB is None: VOSB=VOS
    s=open('../netlist/sync_pll.tmpl').read()
    for k,v in dict(AMP=AMP,PILOT=PILOT,DFREQ=DFREQ,VOS=VOS,VBERR=VBERR,RI=RI,RZ=RZ,CI=CI,CP=CP,TSTOP=TSTOP,PH0=PH0,SR=SR,RL=RL,VOSB=VOSB,TAG=tag).items():
        s=s.replace('{%s}'%k, str(v))
    open(tag+'.cir','w').write(s)
    subprocess.run(['ngspice','-b',tag+'.cir'],capture_output=True)
    d=np.loadtxt(tag+'.dat')
    t=d[:,0]; th=d[:,1]; vc=d[:,3]; sa=d[:,5]; sb=d[:,7]
    psi=np.angle(np.exp(1j*th))    # I phase minus pilot phase
    return t,psi,vc,sa,sb
if __name__=='__main__':
    t,psi,vc,sa,sb=run('base')
    for tt in (0.02,0.05,0.1,0.2,0.29):
        i=np.searchsorted(t,tt)
        print(f"t={tt:5.2f}  psi={np.degrees(psi[i]):8.2f} deg  38k err={np.degrees(np.angle(np.exp(2j*psi[i]))):7.2f}  vctl={vc[i]:.3f}  SA-SB={1000*(sa[i]-sb[i]):7.1f} mV")
