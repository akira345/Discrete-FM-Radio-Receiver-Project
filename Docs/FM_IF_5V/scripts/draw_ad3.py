exec(open('sch.py').read())

GRN, RED, BLU, ORG = '#0a7d3f', '#c0392b', '#1f6feb', '#d97706'
s = Sch(9.6, 4.6, dpi=175)
A = s.ax

def note(t, x, y, c='#f0f9f7', ec='#8fcfc7', tc='#0a5d55', size=7.3):
    A.text(x, y, t, ha='left', va='top', fontsize=size, color=tc, zorder=8,
           bbox=dict(boxstyle='round,pad=0.42', fc=c, ec=ec, lw=0.9))
    s._t(x, y)

YS, YG = 5.30, 2.40
XI, XO = 3.40, 5.80

s.lbl(4.3, 7.60, 'AD3 の接続（リミット閾値スイープ）', ha='center', bold=True, size=11)

# 信号ライン
s.w((0.10, YS), (XI, YS))
s.w((XO, YS), (8.90, YS))

# AWG + 直列330Ω
s.lbl(-0.05, YS, 'AD3  W1\n(AWG)', ha='right', va='center', size=8, bold=True, c=ORG)
s.res((0.90, YS), (2.20, YS), '330Ω  直列に追加', ofs=0.40, side=1, size=7.6)
s.lbl(1.55, YS + 0.95, '新規', ha='center', size=7.6, bold=True, c=RED)
s.w((1.55, YS + 0.62), (1.55, YS + 0.78))

# フィルタ
A.add_patch(plt.Rectangle((XI, YS - 0.60), XO - XI, 1.20, fc='#eef2f7',
                          ec=BLU, lw=1.4, zorder=3))
A.text((XI + XO) / 2, YS + 0.16, 'SFELF10M7', ha='center', va='center',
       fontsize=9, color='#111', fontweight='bold', zorder=4)
A.text((XI + XO) / 2, YS - 0.24, 'IN   GND   OUT', ha='center', va='center',
       fontsize=7.3, color='#555', zorder=4)
s._t(XI, YS - 0.60); s._t(XO, YS + 0.60)
s.w(((XI + XO) / 2, YS - 0.60), ((XI + XO) / 2, YG))

# 出力側 330Ω（既存）
s.dot(6.70, YS)
s.res((6.70, YS), (6.70, YG), '330Ω', ofs=0.50, side=-1)

# Scope 1 をここに
s.dot(7.30, YS)
s.w((7.30, YS), (7.30, YS + 1.05))
s.lbl(7.30, YS + 1.20, 'AD3  Scope 1', ha='center', size=8, bold=True, c=ORG)
s.lbl(7.30, YS + 1.62, '★ここの実電圧を読む', ha='center', size=7.6, bold=True, c=RED)

# CIA
s.cap((7.95, YS), (8.75, YS), 'CIA', ofs=0.40, side=-1)
s.lbl(9.00, YS, '→ 1段目', va='center', size=8, bold=True)

# GND
s.w((0.90, YG), (7.30, YG), lw=2.6)
for x in ((XI + XO) / 2, 6.70):
    s.dot(x, YG, r=0.075)
s.w((0.90, YG), (0.10, YG), lw=2.6)
s.lbl(-0.05, YG, 'AD3  GND', ha='right', va='center', size=8, bold=True, c=ORG)
A.add_patch(Circle((6.70, YG), 0.38, fc='none', ec=GRN, lw=2.0, zorder=6))
s.lbl(6.70, YG - 0.62, '★ 1段目の基準点', ha='center', size=7.8, bold=True, c=GRN)

# Scope 2
s.lbl(4.60, 0.95, 'AD3  Scope 2  →  S4A（4段目コレクタ）', ha='center',
      size=8.5, bold=True, c=ORG)

note('変更点はこれだけ：入力側の 330Ω を「シャント」から「直列」に付け替える\n'
     'AWG の出力インピーダンスはほぼ 0Ω なので、シャントのままだと\n'
     'フィルタが必要とする 330Ω の信号源インピーダンスが短絡されます',
     -0.55, 0.30, c='#fff5f5', ec='#e8a0a0', tc='#7a1010')

s.save('ad3.png')
