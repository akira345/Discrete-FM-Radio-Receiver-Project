exec(open('sch.py').read())

RED, GRN, BLU = '#c0392b', '#0a7d3f', '#1f6feb'
s = Sch(9.2, 5.4, dpi=175)
A = s.ax

def note(t, x, y, c='#f0f9f7', ec='#8fcfc7', tc='#0a5d55', size=7.4, ha='left'):
    A.text(x, y, t, ha=ha, va='top', fontsize=size, color=tc, zorder=8,
           bbox=dict(boxstyle='round,pad=0.42', fc=c, ec=ec, lw=0.9))
    s._t(x, y)

YIN, YB, YE, YG = 6.10, 5.10, 3.60, 1.60
XP = 4.30                                   # 基準点

s.lbl(4.6, 8.15, '1段目のグランド基準点 — ここが 76 dB の基準です',
      ha='center', bold=True, size=11)

# --- 入力
s.w((-0.6, YIN), (1.35, YIN))
s.lbl(-0.7, YIN, 'セラミック\nフィルタ出力', ha='right', va='center', size=7.6, bold=True)
s.dot(0.30, YIN)
s.res((0.30, YIN), (0.30, YG), '330Ω\n終端', ofs=0.60, side=1)
s.cap((1.35, YIN), (2.35, YIN), 'CIA 100p', ofs=0.40, side=1)
s.w((2.35, YIN), (2.75, YIN), (2.75, YB + 0.55))

# --- 1段目ブロック
A.add_patch(plt.Rectangle((2.35, YB - 0.55), 4.1, 1.10, fc='#eef2f7', ec=BLU,
                          lw=1.3, zorder=2))
A.text(4.40, YB, '1段目 差動対', ha='center', va='center', fontsize=9.5,
       color='#111', fontweight='bold', zorder=4)
s._t(2.35, YB - 0.55); s._t(6.45, YB + 0.55)

# INB
s.w((6.05, YB + 0.55), (6.05, YIN), (7.15, YIN))
s.cap((7.15, YIN), (8.15, YIN), 'CIB 100p', ofs=0.40, side=1)
s.w((8.15, YIN), (8.55, YIN), (8.55, YG))
s.lbl(6.10, YIN + 0.30, 'IN B', size=7.6, bold=True)

# エミッタ → RT
s.w((4.30, YB - 0.55), (4.30, YE))
s.res((XP, YE), (XP, YG), 'RT 150Ω', ofs=0.60, side=1)

# デカップリング
s.w((1.55, YB + 1.45), (1.55, YG))
s.lbl(1.55, YB + 1.62, 'VK1', ha='center', size=7.6, bold=True)
s.cap((1.55, YB + 1.05), (1.55, YG + 0.95), '10µF\n+0.1µF', ofs=0.62, side=1)

# --- 基準点（1点に集める）
s.w((0.30, YG), (8.55, YG), lw=2.6)
for x in (0.30, 1.55, XP, 8.55):
    s.dot(x, YG, r=0.075)
A.add_patch(Circle((XP, YG), 0.42, fc='none', ec=GRN, lw=2.2, zorder=6))
s.lbl(XP, YG - 0.75, '★ 基準点（1〜2ピッチ以内に集める）', ha='center',
      size=8.4, bold=True, c=GRN)

# 電源側へ
s.w((8.55, YG), (9.55, YG), lw=2.6)
s.lbl(9.65, YG, '→ 2・3・4段目\n→ 電源グランド（4段目の端）', va='center', size=7.8, bold=True)

note('この4本は必ず同じ1点に落とす\n'
     '  ① 330Ω 終端の GND\n'
     '  ② CIB（IN B）の GND  ← 最重要\n'
     '  ③ RT 150Ω の GND\n'
     '  ④ VK1 デカップリングの GND',
     -0.9, 0.55)

note('なぜ ② が最重要か\n'
     '1段目だけはシングルエンド駆動なので、IN B の\n'
     'グランドと RT のグランドの間に生じた電圧は\n'
     '「差動入力そのもの」として 76 dB 増幅される。\n'
     '必要なのは 0.2 mV。バス上で数 mm 離れれば足りる。',
     4.15, 0.55, c='#fff5f5', ec='#e8a0a0', tc='#7a1010')

s.save('gnd1.png')
