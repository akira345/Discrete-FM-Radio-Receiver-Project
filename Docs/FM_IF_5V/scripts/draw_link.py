import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt, matplotlib.font_manager as fm
from matplotlib.patches import Rectangle, FancyArrowPatch
import numpy as np
for f in ['Noto Sans CJK JP','IPAGothic','DejaVu Sans']:
    if any(f in x.name for x in fm.fontManager.ttflist):
        plt.rcParams['font.family']=f; break

BLU,ORG,TEA='#1f6feb','#d97706','#10998a'
INK,SUB,MUT='#1c1c1a','#55534e','#8a8781'; SURF='#fcfcfb'
BAD,GOOD='#c0392b','#0a7d3f'

fig,(a1,a2)=plt.subplots(2,1,figsize=(9.4,6.6),dpi=175)
fig.patch.set_facecolor(SURF)

def board(ax,x,y,w,h,label,fc='#eef2f7',ec=BLU):
    ax.add_patch(Rectangle((x,y),w,h,fc=fc,ec=ec,lw=1.4,zorder=2))
    ax.text(x+w/2,y+h-0.28,label,ha='center',va='top',fontsize=9,
            color=INK,fontweight='bold',zorder=4)

def twist(ax,x0,x1,y,n=14,amp=0.10,c=GOOD,lw=2.0):
    t=np.linspace(0,1,400); x=x0+(x1-x0)*t
    ax.plot(x,y+amp*np.sin(2*np.pi*n*t),'-',color=c,lw=lw,zorder=5)
    ax.plot(x,y-amp*np.sin(2*np.pi*n*t),'-',color=c,lw=lw,zorder=5)

# ================= NG =================
a1.set_facecolor(SURF); a1.axis('off'); a1.set_xlim(0,10); a1.set_ylim(0,3.9)
board(a1,0.6,1.1,4.6,1.7,'リミッタ基板')
a1.text(0.95,1.45,'IN',fontsize=8.5,color=INK,fontweight='bold')
a1.text(4.75,1.45,'S4A/B',fontsize=8.5,color=INK,fontweight='bold',ha='right')
board(a1,0.6,0.1,3.2,0.75,'検波基板',fc='#f6f8fa',ec=MUT)
# 戻る配線
a1.plot([5.0,6.2,6.2,1.0,1.0,1.4],[1.55,1.55,0.62,0.62,0.62,0.62],'-',
        color=BAD,lw=2.2,zorder=5)
a1.plot([5.0,6.4,6.4,0.8,0.8],[1.35,1.35,0.42,0.42,0.48],'-',color=BAD,lw=2.2,zorder=5)
a1.text(6.6,1.0,'入力側のすぐ横を\n3 Vpp が通る',fontsize=8.5,color=BAD,
        fontweight='bold',va='center')
a1.text(0.55,3.75,'NG  検波基板を入力側に置き、配線が戻ってくる配置',
        fontsize=11,color=BAD,fontweight='bold',ha='left')
a1.text(0.55,3.35,'必要な結合は 0.035 pF。1 cm 以内を 5 cm 並走すれば 0.1〜0.3 pF に達し、また発振します。',
        fontsize=8.6,color=SUB,ha='left')

# ================= OK =================
a2.set_facecolor(SURF); a2.axis('off'); a2.set_xlim(0,10); a2.set_ylim(0,3.9)
board(a2,0.6,1.0,4.2,1.7,'リミッタ基板')
a2.text(0.95,1.35,'IN',fontsize=8.5,color=INK,fontweight='bold')
a2.text(4.45,1.35,'S4A/B',fontsize=8.5,color=INK,fontweight='bold',ha='right')
board(a2,6.2,1.0,3.2,1.7,'検波基板')
a2.text(6.45,1.35,'IN',fontsize=8.5,color=INK,fontweight='bold')
twist(a2,4.8,6.2,1.95)
a2.text(5.5,2.30,'S4A / S4B\nツイストペア',ha='center',fontsize=8.6,
        color=GOOD,fontweight='bold')
a2.plot([4.8,6.2],[1.35,1.35],'-',color=INK,lw=2.6,zorder=5)
a2.text(5.5,1.13,'GND（太く短く・信号対のすぐ横）',ha='center',fontsize=8.2,color=INK)
a2.annotate('',xy=(6.2,0.72),xytext=(4.8,0.72),
            arrowprops=dict(arrowstyle='<->',color=MUT,lw=1.2))
a2.text(5.5,0.50,'5 cm 以内',ha='center',fontsize=8.2,color=MUT)
a2.text(0.55,3.75,'OK  基板を端どうしで並べ、ツイストペアで最短に',
        fontsize=11,color=GOOD,fontweight='bold',ha='left')
a2.text(0.55,3.35,'S4A と S4B は逆相・同振幅。撚れば放射が打ち消し合い、20〜30 dB 稼げます。',
        fontsize=8.6,color=SUB,ha='left')

fig.text(0.012,0.012,
 '10.7 MHz の波長は 28 m。5 cm は λ/560 なので伝送線路ではなく完全な集中定数。整合は不要。',
 fontsize=8,color=MUT)
fig.tight_layout(rect=[0,0.03,1,1]); fig.savefig('link.png',facecolor=SURF)
print('wrote link.png')
