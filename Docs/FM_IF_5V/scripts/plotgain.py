import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt, matplotlib.font_manager as fm
import numpy as np, subprocess

for f in ['Noto Sans CJK JP','IPAGothic','DejaVu Sans']:
    if any(f in x.name for x in fm.fontManager.ttflist):
        plt.rcParams['font.family']=f; break

base = open('lim_op.cir').read().split('.control')[0]
base = base.replace('VIN  SRC 0 DC 0 SFFM(0 14.1m 10.7Meg 7.5 10k)','VIN  SRC 0 DC 0 AC 1')
open('g.cir','w').write(base + ".control\nset noaskquit\nac dec 200 30k 300meg\n"
    "let g=db(v(o4a))-db(v(fout))\nwrdata gn.txt g\n.endc\n.end\n")
subprocess.run(['ngspice','-b','g.cir'],capture_output=True)
a=np.loadtxt('gn.txt'); f,g=a[:,0]/1e6, a[:,1]

BLU,ORG,TEA='#1f6feb','#d97706','#10998a'
INK,SUB,MUT='#1c1c1a','#55534e','#8a8781'
SURF='#fcfcfb'

fig,ax=plt.subplots(figsize=(9.2,5.2),dpi=175)
fig.patch.set_facecolor(SURF); ax.set_facecolor(SURF)

pk=g.argmax(); band=f[g>g[pk]-3]
ax.axvspan(band.min(),band.max(),color=BLU,alpha=0.07,lw=0)
ax.plot(f,g,'-',color=BLU,lw=2,solid_capstyle='round',zorder=3)

def at(x): return g[np.argmin(abs(f-x))]

# 実測された発振周波数
osc=[(0.62,'620 kHz'),(1.39,'1.39 MHz'),(3.05,'3.05 MHz')]
ax.plot([o[0] for o in osc],[at(o[0]) for o in osc],'o',ms=9,color=ORG,
        mec=SURF,mew=2,zorder=5)
for x,lab in osc:
    ax.annotate(lab,(x,at(x)),textcoords='offset points',xytext=(0,-16),
                ha='center',va='top',fontsize=8.5,color=ORG,fontweight='bold')

# 設計周波数
ax.plot([10.7],[at(10.7)],'o',ms=9,color=TEA,mec=SURF,mew=2,zorder=5)
ax.annotate(f'10.7 MHz（設計）{at(10.7):.1f} dB',(10.7,at(10.7)),
            textcoords='offset points',xytext=(16,10),ha='left',
            fontsize=8.5,color=TEA,fontweight='bold',va='center',
            arrowprops=dict(arrowstyle='-',color=TEA,lw=1))

# ピーク
ax.annotate(f'ピーク {g[pk]:.1f} dB @ {f[pk]:.2f} MHz',(f[pk],g[pk]),
            textcoords='offset points',xytext=(0,26),ha='center',
            fontsize=9.5,color=INK,fontweight='bold',
            arrowprops=dict(arrowstyle='-',color=MUT,lw=1))

ax.annotate('', xy=(10.7,g[pk]), xytext=(10.7,at(10.7)),
            arrowprops=dict(arrowstyle='<->',color=SUB,lw=1.2))
ax.text(9.2,(g[pk]+at(10.7))/2,f'{g[pk]-at(10.7):.1f} dB 余分',fontsize=8.5,
        color=SUB,va='center',ha='right')
ax.axhline(g[pk],color=MUT,lw=0.8,ls=(0,(4,4)),zorder=1)

ax.text(np.sqrt(band.min()*band.max()),18,
        f'利得が最大の帯域\n{band.min():.2f} – {band.max():.1f} MHz',
        ha='center',fontsize=8.5,color=BLU)

ax.set_xscale('log'); ax.set_xlim(0.05,300); ax.set_ylim(10,88)
ax.set_xlabel('周波数 (MHz)',fontsize=9.5,color=SUB)
ax.set_ylabel('総利得 (dB)',fontsize=9.5,color=SUB)
ax.set_title('4段リミッタの総利得 — 最大利得は 10.7 MHz ではなく 2.6 MHz',
             fontsize=12,color=INK,fontweight='bold',pad=14,loc='left')
ax.set_xticks([0.1,0.3,1,3,10,30,100]); ax.set_xticklabels(['0.1','0.3','1','3','10','30','100'])
ax.grid(True,which='major',color='#e6e4df',lw=0.8)
ax.tick_params(colors=SUB,labelsize=8.5)
for sp in ('top','right'): ax.spines[sp].set_visible(False)
for sp in ('left','bottom'): ax.spines[sp].set_color('#d8d5cf')
fig.text(0.012,0.015,'ngspice .ac / 入力330Ω終端・無信号　オレンジ＝実測された発振周波数',
         fontsize=8,color=MUT)
fig.tight_layout(rect=[0,0.03,1,1]); fig.savefig('gainshape.png',facecolor=SURF)
print('wrote gainshape.png')
