import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt, matplotlib.font_manager as fm
import numpy as np
for f in ['Noto Sans CJK JP','IPAGothic','DejaVu Sans']:
    if any(f in x.name for x in fm.fontManager.ttflist):
        plt.rcParams['font.family']=f; break

awg = np.array([400,200,100,50,25,12.5,6.25,3.15,1.55,0.8])      # mV peak
c1  = np.array([93.941,48.240,26.659,16.186,10.791,8.2516,7.9342,6.6648,6.6648,6.9821])
c2  = np.array([2.3748,2.3494,2.3049,2.2922,2.2858,2.2508,2.2953,2.3017,2.2667,2.2699])
K   = 93.941/800.0
ideal = 2*awg*K

BLU,ORG,TEA='#1f6feb','#d97706','#10998a'
INK,SUB,MUT='#1c1c1a','#55534e','#8a8781'; SURF='#fcfcfb'
FLOOR = 6.8

fig,(ax1,ax2)=plt.subplots(1,2,figsize=(10.4,4.6),dpi=175)
fig.patch.set_facecolor(SURF)

# ---- 左：C1
ax1.set_facecolor(SURF)
ax1.plot(awg, ideal,'--',color=MUT,lw=1.6,zorder=2)
ax1.plot(awg, c1,'-o',color=BLU,lw=2,ms=7,mec=SURF,mew=1.6,zorder=4)
ax1.axhline(FLOOR,color=ORG,lw=1.4,ls=(0,(5,3)),zorder=3)
ax1.text(1.0, FLOOR*1.22, f'測定系の床 ≈ {FLOOR:.1f} mVpp', color=ORG,
         fontsize=8.5, fontweight='bold')
ax1.text(90, 150,'理想（K=0.1174 の直線）', color=MUT, fontsize=8.5, ha='right')
ax1.set_xscale('log'); ax1.set_yscale('log')
ax1.set_xlim(0.6,600); ax1.set_ylim(0.1,300)
ax1.set_xlabel('AWG Amplitude (mV peak)',fontsize=9.5,color=SUB)
ax1.set_ylabel('C1 リミッタ入力 (mVpp)',fontsize=9.5,color=SUB)
ax1.set_title('C1：50 mV より下は床に張り付く',fontsize=11,color=INK,
              fontweight='bold',loc='left',pad=10)

# ---- 右：C2
ax2.set_facecolor(SURF)
ax2.plot(awg, c2,'-o',color=TEA,lw=2,ms=7,mec=SURF,mew=1.6,zorder=4)
ax2.axhspan(2.24,2.40,color=TEA,alpha=0.08,lw=0)
ax2.set_xscale('log'); ax2.set_xlim(0.6,600); ax2.set_ylim(0,3.0)
ax2.set_xlabel('AWG Amplitude (mV peak)',fontsize=9.5,color=SUB)
ax2.set_ylabel('C2  S4A (Vpp)',fontsize=9.5,color=SUB)
ax2.set_title('C2：54 dB 振っても 0.3 dB しか動かない',fontsize=11,color=INK,
              fontweight='bold',loc='left',pad=10)
ax2.annotate('本来ならここで落ちるはず\n（設計値 AWG 6.8 mV）',
             xy=(6.8,2.30), xytext=(6.8,1.15), ha='center', fontsize=8.5, color=ORG,
             fontweight='bold',
             arrowprops=dict(arrowstyle='-|>',color=ORG,lw=1.4))
ax2.axvspan(12.5,25,color=ORG,alpha=0.10,lw=0)
ax2.text(17,2.62,'ここで波形が\n10.7 MHz → 約2 MHz に\n化ける',ha='center',
         fontsize=8.2,color=ORG,fontweight='bold')

for ax in (ax1,ax2):
    ax.grid(True,which='major',color='#e6e4df',lw=0.8)
    ax.grid(True,which='minor',color='#f1efea',lw=0.5)
    ax.tick_params(colors=SUB,labelsize=8.5)
    for sp in ('top','right'): ax.spines[sp].set_visible(False)
    for sp in ('left','bottom'): ax.spines[sp].set_color('#d8d5cf')

fig.text(0.012,0.015,'AD3 実測（2026-09-21）／ 10.7 MHz 無変調・セラミックフィルタ経由',
         fontsize=8,color=MUT)
fig.tight_layout(rect=[0,0.035,1,1]); fig.savefig('sweep.png',facecolor=SURF)
print('wrote sweep.png')
