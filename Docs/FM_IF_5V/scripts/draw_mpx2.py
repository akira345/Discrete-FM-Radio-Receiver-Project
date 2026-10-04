exec(open('sch.py').read())
RED,GRN,BLU='#c0392b','#0a7d3f','#1f6feb'
d = Sch(14.2, 6.0, dpi=170); A = d.ax
def v5(x,y,up=0.42):
    d.w((x,y),(x,y+up)); A.plot([x-0.20,x+0.20],[y+up,y+up],'-',c='#111',lw=1.9)
    d.lbl(x,y+up+0.12,'+5V',ha='center',va='bottom',size=6.8,bold=True)
def tag(x,y,s,side='l',size=7.6):
    ha={'l':'right','r':'left'}[side]; dx={'l':-0.13,'r':0.13}[side]
    A.text(x+dx,y,s,ha=ha,va='center',fontsize=size,zorder=6,fontweight='bold',
           bbox=dict(boxstyle='round,pad=0.17',fc='#e8eef7',ec='#556',lw=0.8))
    d._t(x+dx+(-1.5 if side=='l' else 1.5),y)

d.lbl(7.1, 9.55, 'MPX コンポジット出力段 rev.E ── LPF 定数見直し ＋ 非反転2段利得', ha='center', bold=True, size=11)
d.lbl(7.1, 9.15, '利得 3.05倍・非反転（+0.6°）／53kHz で −0.30dB（セパレーション上限 35dB）／フル変調で THD 0.39%',
      ha='center', size=8, c='#555')

YS, YG, YV = 5.30, 1.05, 7.55

# ===== 既存部（LPF 定数のみ変更）=====
tag(0.25, YS, 'OB', side='l')
d.w((0.25, YS), (0.55, YS)); d.dot(0.55, YS)
d.cap((0.55, YS), (0.55, YG+0.50), 'CLB 220p', ofs=0.46, side=1, size=6.2)
d.gnd(0.55, YG+0.50)
d.res((0.55, YS), (1.55, YS), 'RF1 1k', ofs=0.28, side=1, size=6.6)
d.dot(1.55, YS)
d.cap((1.55, YS), (1.55, YG+0.50), 'CF1 220p', ofs=0.46, side=1, size=6.2)
d.gnd(1.55, YG+0.50)
d.w((1.55, YS), (2.20, YS))
c16,e16 = d.npn(2.20, YS, 'Q16', size=8.2)
d.w(c16,(c16[0], YV)); v5(c16[0], YV)
d.w(e16,(e16[0], YS-1.30)); d.dot(e16[0], YS-1.30)
d.lbl(e16[0]+0.14, YS-1.08, 'AFE', size=6.8, bold=True)
d.res((e16[0], YS-1.30),(e16[0], YG+0.20),'RE16\n4.7k', ofs=0.50, side=1, size=6.2)
d.gnd(e16[0], YG+0.20)
A.add_patch(plt.Rectangle((0.02, YG-0.15), 3.15, 7.0, fc='none', ec='#8a8781', ls=(0,(4,3)), lw=1.1, zorder=0))
d.lbl(0.10, YG-0.55, '既存（CLB・CF1 を 1000p→220p に変更するだけ）', ha='left', size=7.4, c='#555')

# ===== 追加 1段目 =====
def ce(x, lab, RE, RB2, qn):
    d.cap((x-0.95, YS-1.30),(x-0.15, YS-1.30), 'C 1µ', side=1, size=6.4)
    d.dot(x-0.15, YS-1.30)
    d.w((x-0.15, YS-1.30),(x-0.15, YS))
    d.res((x-0.15, YS),(x-0.15, YV-0.35), f'{lab}A\n100k', ofs=0.50, side=1, size=6.2)
    v5(x-0.15, YV-0.35)
    d.res((x-0.15, YS-1.30),(x-0.15, YG+0.20), f'{lab}B\n{RB2}', ofs=0.50, side=1, size=6.2)
    d.gnd(x-0.15, YG+0.20)
    d.w((x-0.15, YS-1.30),(x+0.60, YS-1.30))
    c,e = d.npn(x+0.60, YS-1.30, '', size=8.2)
    d.lbl(x+0.74, YS-0.95, qn, ha='left', size=8.5, bold=True)
    d.w(c,(c[0], YS+0.55)); d.dot(c[0], YS+0.55)
    d.res((c[0], YS+0.55),(c[0], YV), f'{lab}C 2.2k', ofs=0.50, side=-1, size=6.2)
    v5(c[0], YV)
    d.w(e,(e[0], YG+0.95))
    d.res((e[0], YG+0.95),(e[0], YG+0.20), f'{lab}E {RE}', ofs=0.52, side=-1, size=6.2)
    d.gnd(e[0], YG+0.20)
    return c[0]

d.w((e16[0], YS-1.30),(4.30, YS-1.30))
x1 = ce(5.25, 'R1', '1.2k', '47k', 'Q17')
d.w((x1, YS+0.55),(x1+0.50, YS+0.55),(x1+0.50, YS-1.30))
x2 = ce(x1+1.45, 'R2', '1.1k', '47k', 'Q18')

# 出力
d.w((x2, YS+0.55),(x2+0.45, YS+0.55))
d.cap((x2+0.45, YS+0.55),(x2+1.25, YS+0.55), 'COUT 10µ', side=1, size=6.4)
d.w((x2+1.25, YS+0.55),(x2+1.75, YS+0.55)); d.dot(x2+1.75, YS+0.55)
d.res((x2+1.75, YS+0.55),(x2+1.75, YG+0.20), 'VR\n50k', ofs=0.50, side=-1, size=6.2)
d.gnd(x2+1.75, YG+0.20)
d.w((x2+1.75, YS+0.55),(x2+2.35, YS+0.55))
tag(x2+2.35, YS+0.55, 'MPX 入力へ\n（非反転）', side='r', size=7.4)

A.add_patch(plt.Rectangle((4.05, YG-0.15), x2+2.05-4.05, 7.0, fc='none', ec=RED, ls=(0,(4,3)), lw=1.3, zorder=0))
d.lbl(6.40, YG-0.55, '追加（TR 2個・抵抗6本・コンデンサ2個）', ha='left', size=7.4, c=RED, bold=True)
d.w((0.55, YG),(x2+1.75, YG), lw=2.3)

A.text(0.02, -1.35,
 'DC: AFE 2.66V ／ B17 1.52V・E17 0.89V・C17 3.37V ／ B18 1.51V・E18 0.88V・C18 3.24V ／ 各 0.74〜0.80mA（追加電流 1.5mA）\n'
 'フル変調（AFE 796mVpp）で出力 2.39Vpp。クリップは入力 1004mVpp から＝26% の余裕。',
 ha='left', va='top', fontsize=7.6, color='#7a1010', zorder=8,
 bbox=dict(boxstyle='round,pad=0.4', fc='#fff5f5', ec='#e8a0a0', lw=0.9))
d._t(0.02,-1.35); d._t(13.9,-1.35)
d.save('mpx2stage.png')
