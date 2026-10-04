import subprocess, numpy as np, os
def sim(order, cv, c5):
    src=f"""* Colpitts LO rev3
.model JF3557 NJF(VTO=-0.7 BETA=25m CGS=7.1p CGD=2.9p IS=1e-14)
V1 VDD 0 5
L2 N009 L2X 56n
RL2 L2X 0 0.6
C5 N009 0 {c5}p
CVLO N009 0 {cv}p
CSTR2 N009 0 3p
C6 N009 N011 27p
C7 N011 0 27p
J2 {order} JF3557
R5 N011 0 2.2k
VD N010 VDD 0
IK 0 N009 PULSE(0 3m 100n 1n 1n 4n 0)
.control
tran 5p 8u
let y = v(n009)
let z = v(n011)
wrdata /tmp/lo.dat y z
.endc
.end
"""
    open('/tmp/lo.cir','w').write(src)
    if os.path.exists('/tmp/lo.dat'): os.remove('/tmp/lo.dat')
    subprocess.run(['ngspice','-b','/tmp/lo.cir'],capture_output=True)
    d=np.loadtxt('/tmp/lo.dat'); t,y,z=d[:,0],d[:,1],d[:,3]
    m=t>7e-6; t,y,z=t[m],y[m],z[m]
    yy=y-y.mean()
    zc=[t[i-1]+(t[i]-t[i-1])*(-yy[i-1])/(yy[i]-yy[i-1]) for i in range(1,len(yy)) if yy[i-1]<0<=yy[i]]
    return 1/np.mean(np.diff(np.array(zc))), np.ptp(y), np.ptp(z)

N='N010 N009 N011'; S='N011 N009 N010'
print("C5 による補正の探索（逆接続のまま）")
print(f"{'バリコン':>7} {'正常 C5=11p':>13} | " + " ".join(f"{'逆 C5='+str(c)+'p':>13}" for c in (11,9,8.2,7.5)))
for cv in (30,24,15,10):
    fn,_,_ = sim(N,cv,11)
    row=[]
    for c5 in (11,9,8.2,7.5):
        fs,_,_ = sim(S,cv,c5)
        row.append(f"{fs/1e6:8.2f}({(fs-fn)/1e6:+5.2f})")
    print(f"{cv:5d}p  {fn/1e6:9.3f}MHz | " + " ".join(row))
print()
print("推奨値でのタップ振幅（LOバッファ入力 N011）")
for cv in (24,10):
    fn,an,sn = sim(N,cv,11); fs,as_,ss = sim(S,cv,8.2)
    print(f"  {cv:2d}p 正常: {fn/1e6:7.2f}MHz タンク{an*1000:5.0f} タップ{sn*1000:5.0f}mVpp"
          f" / 逆+C5 8.2p: {fs/1e6:7.2f}MHz タンク{as_*1000:5.0f} タップ{ss*1000:5.0f}mVpp")
