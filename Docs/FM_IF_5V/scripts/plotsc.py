import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt, matplotlib.font_manager as fm
import numpy as np
for f in ['Noto Sans CJK JP','IPAGothic','DejaVu Sans']:
    if any(f in x.name for x in fm.fontManager.ttflist):
        plt.rcParams['font.family']=f; break

BLU,ORG,TEA='#1f6feb','#d97706','#10998a'
INK,SUB,MUT='#1c1c1a','#55534e','#8a8781'; SURF='#fcfcfb'
BAD,GOOD='#c0392b','#0a7d3f'

f=np.array([10.550,10.600,10.625,10.650,10.700,10.750,10.775,10.800,10.850,10.900])
v=np.array([2.126,2.262,2.368,2.488,2.760,3.041,3.164,3.279,3.446,3.546])
d=(f-10.700)*1000.0            # kHz

m=np.abs(d)<=75.5
A=np.polyfit(d[m],v[m],1); k=A[0]; b=A[1]
res=(v-np.polyval(A,d))*1000.0

fig,(a1,a2)=plt.subplots(1,2,figsize=(11.2,4.5),dpi=175,
                         gridspec_kw={'width_ratios':[1.45,1]})
fig.patch.set_facecolor(SURF)

# ---- S curve
a1.set_facecolor(SURF)
a1.axvspan(-75,75,color=TEA,alpha=0.09,zorder=0)
xx=np.linspace(-160,210,200)
a1.plot(xx,np.polyval(A,xx),'--',color=MUT,lw=1.2,zorder=2,
        label=f'直線近似  {k*1000:.2f} mV/kHz')
a1.plot(d,v,'-o',color=BLU,lw=1.8,ms=5.5,zorder=4,label='実測')
a1.plot([0],[2.760],'o',color=ORG,ms=10,mfc='none',mew=2.2,zorder=5)
a1.annotate('中心 10.700 MHz\n2.760 V',xy=(0,2.760),xytext=(-150,3.15),
            fontsize=8.6,color=ORG,fontweight='bold',
            arrowprops=dict(arrowstyle='->',color=ORG,lw=1.2))
a1.annotate('',xy=(-75,2.368),xytext=(-75,3.164),
            arrowprops=dict(arrowstyle='<->',color=GOOD,lw=1.5))
a1.text(-70,2.79,'±75 kHz\n796 mVpp',fontsize=8.8,color=GOOD,fontweight='bold')
a1.set_xlabel('中心からの離調  Δf  [kHz]',fontsize=9,color=INK)
a1.set_ylabel('AFE  [V]',fontsize=9,color=INK)
a1.set_title('S カーブ（実測）',fontsize=10.5,color=INK,fontweight='bold',loc='left')
a1.grid(alpha=0.22,lw=0.6); a1.legend(fontsize=8.2,loc='lower right',framealpha=0.9)
a1.set_xlim(-170,220)
for s in a1.spines.values(): s.set_color(MUT); s.set_linewidth(0.8)
a1.tick_params(labelsize=8, colors=SUB)

# ---- residual
a2.set_facecolor(SURF)
a2.axvspan(-75,75,color=TEA,alpha=0.09,zorder=0)
a2.axhline(0,color=MUT,lw=1.0)
a2.plot(d,res,'-o',color=BAD,lw=1.6,ms=5.5,zorder=4)
for x,y in zip(d,res):
    if abs(x)<=75.5:
        a2.annotate(f'{y:+.1f}',xy=(x,y),xytext=(0,9 if y>0 else -16),
                    textcoords='offset points',ha='center',fontsize=7.6,color=BAD)
a2.set_xlabel('Δf  [kHz]',fontsize=9,color=INK)
a2.set_ylabel('直線からのずれ  [mV]',fontsize=9,color=INK)
a2.set_title('直線性（±75 kHz 内で最大 8 mV = 1.0 %）',fontsize=10.5,
             color=INK,fontweight='bold',loc='left')
a2.grid(alpha=0.22,lw=0.6); a2.set_xlim(-170,220)
for s in a2.spines.values(): s.set_color(MUT); s.set_linewidth(0.8)
a2.tick_params(labelsize=8, colors=SUB)
a2.text(90,res[np.argmax(np.abs(res))]*0.4,'±100 kHz を\n超えると圧縮',
        fontsize=8.2,color=SUB)

fig.tight_layout()
fig.savefig('scurve.png',facecolor=SURF)

print(f'slope(±75k LSQ) = {k*1000:.3f} mV/kHz')
print(f'±75kHz swing    = {(np.interp(75,d,v)-np.interp(-75,d,v))*1000:.0f} mVpp')
print(f'max |residual| in ±75k = {np.max(np.abs(res[m])):.1f} mV '
      f'({np.max(np.abs(res[m]))/796*100:.2f} %)')
print('resid:', np.round(res,1))
