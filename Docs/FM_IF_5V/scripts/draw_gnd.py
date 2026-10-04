import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt, matplotlib.font_manager as fm
from matplotlib.patches import FancyArrowPatch, Rectangle
import numpy as np

for f in ['Noto Sans CJK JP', 'IPAGothic', 'DejaVu Sans']:
    if any(f in x.name for x in fm.fontManager.ttflist):
        plt.rcParams['font.family'] = f; break

BLU, ORG, TEA = '#1f6feb', '#d97706', '#10998a'
INK, SUB, MUT = '#1c1c1a', '#55534e', '#8a8781'
SURF = '#fcfcfb'
BAD, GOOD = '#c0392b', '#0a7d3f'

fig, axes = plt.subplots(2, 1, figsize=(9.6, 6.4), dpi=175)
fig.patch.set_facecolor(SURF)

XS = [1.0, 3.0, 5.0, 7.0]          # 4段の位置
YB, YG = 2.55, 1.05                # ブロック下端 / GNDバス


def panel(ax, supply_x, title, ok, note):
    ax.set_facecolor(SURF); ax.axis('off')
    ax.set_xlim(-0.4, 9.8); ax.set_ylim(0.1, 4.65)

    # GND バス
    ax.plot([0.4, 8.2], [YG, YG], '-', color=INK, lw=3.2, solid_capstyle='round', zorder=2)
    ax.text(0.3, YG, 'GND', ha='right', va='center', fontsize=9, color=INK, fontweight='bold')

    # 段ブロック
    for i, x in enumerate(XS):
        ax.add_patch(Rectangle((x - 0.62, YB), 1.24, 1.05, fc='#eef2f7',
                               ec=BLU, lw=1.3, zorder=3))
        ax.text(x, YB + 0.52, f'{i+1}段目', ha='center', va='center',
                fontsize=9.5, color=INK, fontweight='bold', zorder=4)
        ax.plot([x, x], [YB, YG], '-', color=INK, lw=1.6, zorder=2)
        ax.plot([x], [YG], 'o', ms=6, color=INK, zorder=4)
        # 信号の流れ
        if i < 3:
            ax.add_patch(FancyArrowPatch((x + 0.62, YB + 0.52), (XS[i+1] - 0.62, YB + 0.52),
                                         arrowstyle='-|>', mutation_scale=11,
                                         color=MUT, lw=1.2, zorder=3))

    # 電源グランドの接続点
    ax.plot([supply_x, supply_x], [YG, YG - 0.62], '-', color=INK, lw=3.2, zorder=2)
    for k, w in enumerate([0.30, 0.19, 0.09]):
        ax.plot([supply_x - w, supply_x + w], [YG - 0.62 - k * 0.11] * 2, '-',
                color=INK, lw=2.4, zorder=2)
    ax.text(supply_x, YG - 1.06, '電源グランド', ha='center', va='top',
            fontsize=8.5, color=INK, fontweight='bold')

    # 4段目の帰還電流の経路
    c = BAD if not ok else GOOD
    x4 = XS[3]
    if supply_x < x4:
        ax.add_patch(FancyArrowPatch((x4 - 0.08, YG + 0.20), (supply_x + 0.08, YG + 0.20),
                                     arrowstyle='-|>', mutation_scale=14,
                                     color=c, lw=2.4, zorder=5))
        ax.text((x4 + supply_x) / 2, YG + 0.40, '4段目の帰還電流', ha='center',
                fontsize=8.5, color=c, fontweight='bold')
        for x in XS[:3]:
            ax.text(x, YG - 0.34, 'ここが持ち上がる', ha='center', va='top',
                    fontsize=7.6, color=c)
    else:
        ax.add_patch(FancyArrowPatch((x4 - 0.08, YG + 0.20), (supply_x - 0.08, YG + 0.20),
                                     arrowstyle='-|>', mutation_scale=14,
                                     color=c, lw=2.4, zorder=5))
        ax.text(x4 + 0.45, YG + 0.42, '4段目の帰還電流は\nすぐ電源へ抜ける', ha='center',
                va='bottom', fontsize=8.5, color=c, fontweight='bold')
        ax.text(XS[0], YG - 0.34, '1段目の基準は汚れない', ha='center', va='top',
                fontsize=8.2, color=c, fontweight='bold')

    ax.text(-0.3, 4.42, title, ha='left', va='top', fontsize=11,
            color=BAD if not ok else GOOD, fontweight='bold')
    ax.text(-0.3, 4.00, note, ha='left', va='top', fontsize=8.6, color=SUB)


panel(axes[0], XS[0], 'NG  電源グランドを入力側（1段目の端）に付けた場合',
      False,
      '4段目の帰還電流がバス全体を流れ、1〜3段目のグランド基準を持ち上げる。\n'
      '1段目のグランドが揺れる＝入力に信号を注入しているのと同じ。必要なのは 0.2 mV だけ。')

panel(axes[1], XS[3] + 0.9, 'OK  電源グランドを出力側（4段目の端）に付ける',
      True,
      '4段目の帰還電流はバスを通らずに電源へ戻る。1段目のグランドには流れない。\n'
      '配線を1本移すだけ。部品の追加は不要。')

fig.text(0.012, 0.012,
         '※ さらに確実にするなら、各段のGNDを1点（電源のGND端子）へ個別に配線するスター接続',
         fontsize=8, color=MUT)
fig.tight_layout(rect=[0, 0.025, 1, 1])
fig.savefig('gndpath.png', facecolor=SURF)
print('wrote gndpath.png')
