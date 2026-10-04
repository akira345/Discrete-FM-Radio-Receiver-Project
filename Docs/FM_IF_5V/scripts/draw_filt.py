exec(open('sch.py').read())

GRN, RED, BLU = '#0a7d3f', '#c0392b', '#1f6feb'
s = Sch(9.0, 4.2, dpi=175)
A = s.ax

def note(t, x, y, c='#f0f9f7', ec='#8fcfc7', tc='#0a5d55', size=7.4):
    A.text(x, y, t, ha='left', va='top', fontsize=size, color=tc, zorder=8,
           bbox=dict(boxstyle='round,pad=0.42', fc=c, ec=ec, lw=0.9))
    s._t(x, y)

YS, YG = 5.20, 2.60          # 信号ライン / GND
XI, XO = 3.00, 5.40          # フィルタの入出力ピン

s.lbl(4.3, 7.15, 'セラミックフィルタの入れ方（フロントエンドはまだ繋がない）',
      ha='center', bold=True, size=10.5)

# --- 信号ライン
s.w((0.40, YS), (XI, YS))
s.w((XO, YS), (8.60, YS))

# --- フィルタ本体
A.add_patch(plt.Rectangle((XI, YS - 0.62), XO - XI, 1.24, fc='#eef2f7',
                          ec=BLU, lw=1.4, zorder=3))
A.text((XI + XO) / 2, YS + 0.16, 'SFELF10M7', ha='center', va='center',
       fontsize=9, color='#111', fontweight='bold', zorder=4)
A.text((XI + XO) / 2, YS - 0.26, 'IN    GND    OUT', ha='center', va='center',
       fontsize=7.4, color='#555', zorder=4)
s._t(XI, YS - 0.62); s._t(XO, YS + 0.62)
# GND ピン
s.w(((XI + XO) / 2, YS - 0.62), ((XI + XO) / 2, YG))

# --- 入力側 330Ω（新規追加）
s.dot(1.50, YS)
s.res((1.50, YS), (1.50, YG), '330Ω', ofs=0.52, side=1)
s.lbl(1.50, YS + 0.95, '新規に追加', ha='center', size=7.6, bold=True, c=RED)
s.w((1.50, YS), (1.50, YS + 0.70))

# 将来のフロントエンド
s.w((0.40, YS), (-0.30, YS))
s.lbl(-0.42, YS, 'あとで\nフロントエンドへ', ha='right', va='center',
      size=7.6, c='#777')

# --- 出力側 330Ω（いま付いている物を流用）
s.dot(6.60, YS)
s.res((6.60, YS), (6.60, YG), '330Ω', ofs=0.52, side=-1)
s.lbl(6.60, YS + 0.95, 'いまの終端を流用', ha='center', size=7.6, bold=True, c=GRN)
s.w((6.60, YS), (6.60, YS + 0.70))

# --- CIA → 1段目
s.cap((7.40, YS), (8.30, YS), 'CIA 100p', ofs=0.42, side=1)
s.lbl(8.70, YS, '→ 1段目\n   IN A', va='center', size=8, bold=True)

# --- GND
s.w((1.50, YG), (6.60, YG), lw=2.6)
for x in (1.50, (XI + XO) / 2, 6.60):
    s.dot(x, YG, r=0.075)
A.add_patch(Circle((6.60, YG), 0.40, fc='none', ec=GRN, lw=2.2, zorder=6))
s.w((6.60, YG), (7.60, YG), lw=2.6)
s.lbl(7.70, YG, '★ 1段目の基準点へ', va='center', size=8, bold=True, c=GRN)

# --- 強調枠
A.add_patch(plt.Rectangle((6.15, YS - 1.15), 2.55, 2.30, fc='none', ec=RED,
                          ls=(0, (5, 3)), lw=1.4, zorder=1))
s.lbl(7.42, YG - 0.55, 'この範囲は 1〜2 ピッチ以内', ha='center', size=7.8,
      bold=True, c=RED)

note('・フロントエンドはまだ繋がない。リミッタ単体の雑音の床を測るため\n'
     '・入力側の 330Ω は「終端」と「フィルタが必要とする信号源インピーダンス」を兼ねる\n'
     '・フィルタの GND ピンも ★ の基準点へ',
     0.15, 1.60)

note('赤枠が肝心です\n'
     'フィルタより後ろで拾ったノイズは濾過されません。\n'
     'OUT ピン → 330Ω → CIA を最短で詰めてください。\n'
     'ここを詰めてもパルスが残るなら、原因は配線の\n'
     'アンテナ効果ではなくプローブか電源側です。',
     5.05, 0.10, c='#fff5f5', ec='#e8a0a0', tc='#7a1010')

s.save('filt.png')
