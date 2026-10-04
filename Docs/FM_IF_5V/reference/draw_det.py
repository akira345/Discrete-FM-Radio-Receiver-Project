"""検波部 独立基板 配置図"""
from pcb import *

NC, NR = 18, 11
b = Board(NC, NR, w=15.5, h=9.6, dpi=175)
for x in range(NC): b.lbl(x, NR + 0.62, f'c{x}', ha='center', size=6.4, c='#8a8a8a')
for y in range(NR): b.lbl(-1.15, y, f'r{y}', ha='right', size=6.4, c='#8a8a8a')
b.lbl(-1.2, NR + 1.70, '検波部 独立基板 配置図  ── 2.54mm ユニバーサル基板／1608・SOT-23',
      size=12.5, bold=True)
b.lbl(-1.2, NR + 1.20, '青実線＝表面すずメッキ線　赤破線＝裏面ジャンパ（被覆線・途中の穴には付けない）',
      size=8, c='#5a5a5a')

# ===== バス =====
b.wire((-0.45, 10), (17.45, 10), lw=3.4)
b.lbl(-0.55, 10.42, '+5V', ha='left', size=8.5, bold=True)
b.wire((-0.45, 5), (17.45, 5), lw=3.4, c=GNDC)
b.lbl(-0.55, 4.58, 'GND バス①', ha='left', size=8, bold=True, c=GNDC)
b.wire((-0.45, 0), (17.45, 0), lw=3.4, c=GNDC)
b.lbl(-0.55, -0.50, 'GND バス②', ha='left', size=8, bold=True, c=GNDC)
b.wire((0, 5), (0, 0), lw=3.0, c=GNDC)
for y, nm in ((9, 'S4A'), (8, 'S4B')):
    b.node(0, y); b.lbl(-0.42, y, nm, ha='right', size=8, bold=True, c=WIRE)

# ===================== 上半分 =====================
b.zone(6.45, 5.45, 13.55, 9.55, '', c='#3a6ea5', a=0.05)
b.lbl(9.5, 9.70, 'ギルバート型 位相検波器', ha='center', size=9, bold=True, c='#3a6ea5')

# --- 上段ドライブ ---
b.wire((0, 9), (2, 9)); b.wire((0, 8), (2, 8))
b.smd((2, 9), (3, 9), 'CUA 1000p', lab_side=1, size=6.4, lab_off=0.46)
b.smd((3, 9), (4, 9), 'RUA1 5.6k', lab_side=1, size=6.4, lab_off=0.46)
b.smd((4, 9), (5, 9), 'RUA2 1k', lab_side=1, size=6.4, lab_off=0.46)
b.smd((2, 8), (3, 8), 'CUB 1000p', lab_side=-1, size=6.4, lab_off=0.46)
b.smd((3, 8), (4, 8), 'RUB1 5.6k', lab_side=-1, size=6.4, lab_off=0.46)
b.smd((4, 8), (5, 8), 'RUB2 1k', lab_side=-1, size=6.4, lab_off=0.46)
b.node(4, 9); b.node(4, 8)
b.wire((5, 9), (5, 7)); b.node(5, 9); b.node(5, 8); b.node(5, 7)
b.smd((5, 10), (5, 9), 'RVBU1\n10k', lab_side=1, size=6.0, lab_off=0.40)
b.smd((5, 7), (5, 6), 'RVBU2\n9.1k', lab_side=1, size=6.2, lab_off=0.50)
b.wire((5, 6), (5, 5)); b.node(5, 6)
b.wire((5, 6), (6, 6)); b.smd((6, 6), (6, 5), 'CVBU\n0.1µ', lab_side=-1, size=6.2, lab_off=0.50)
b.lbl(4.62, 7.0, 'VBU', ha='right', size=7.2, bold=True, c='#b03030')
b.lbl(1.9, 9.62, '上段ドライブ', ha='left', size=8, bold=True, c='#5a5a5a')

# --- ギルバート ---
b.smd((6, 10), (6, 9), 'CLA\n1000p', lab_side=1, size=6.0, lab_off=0.50)
b.smd((7, 10), (7, 9), 'RLA\n1.5k', lab_side=1, size=6.0, lab_off=0.44)
b.smd((10, 10), (10, 9), 'RLB\n1.5k', lab_side=-1, size=6.2, lab_off=0.46)
b.smd((11, 10), (11, 9), 'CLB\n1000p', lab_side=1, size=6.2, lab_off=0.52)
b.wire((6, 9), (7, 9)); b.wire((9, 9), (11, 9))
for p in ((6,9),(7,9),(9,9),(10,9),(11,9)): b.node(*p)
b.jump((7, 9), (13, 9))
b.lbl(8.3, 9.30, 'OA（裏）', ha='center', size=6.4, c=JUMP, bold=True)
b.lbl(10.0, 8.74, 'OB', ha='center', size=7.0, c=WIRE, bold=True)
for nm, cx, cy, C, B, E in (('QU1',7.5,8.5,(7,9),(7,8),(8,8)), ('QU2',8.5,8.5,(9,9),(9,8),(8,8)),
                            ('QU3',11.5,8.5,(11,9),(11,8),(12,8)), ('QU4',12.5,8.5,(13,9),(13,8),(12,8)),
                            ('QL1',8.5,7.5,(8,8),(8,7),(9,7)), ('QL2',11.5,7.5,(12,8),(12,7),(11,7))):
    b.tr3(cx, cy, nm, {'C': (C[0], C[1], 0, 0.36, 'center'),
                       'B': (B[0], B[1], -0.30, -0.02, 'right'),
                       'E': (E[0], E[1], 0.30, -0.02, 'left')}, size=6.8, w=0.90, h=0.58)
b.jump((7, 8), (11, 8)); b.jump((9, 8), (13, 8))
b.lbl(9.5, 10.55, 'BU1・BU2 は裏面（r8 上で交差するので互いに絶縁のこと）',
      ha='center', size=7.0, c=JUMP, bold=True)
b.wire((9, 7), (11, 7)); b.node(10, 7)
b.smd((10, 7), (10, 6), 'RTG 390', lab_side=1, size=6.4, lab_off=0.48)
b.wire((10, 6), (10, 5)); b.node(10, 6)
b.lbl(8.0, 8.42, 'CL1', ha='center', size=6.4, c='#b03030', bold=True)
b.lbl(12.0, 8.42, 'CL2', ha='center', size=6.4, c='#b03030', bold=True)
b.lbl(10.0, 7.42, 'ET', ha='center', size=6.4, c='#b03030', bold=True)
b.jump((4, 9), (7, 8)); b.jump((4, 8), (9, 8))

# --- 下段ドライブ ---
b.smd((7, 7), (8, 7), 'RQ1 470', lab_side=1, size=6.2, lab_off=0.52)
b.smd((8, 7), (8, 6), 'RQ2\n10k', lab_side=1, size=6.0, lab_off=0.48)
b.smd((12, 7), (12, 6), 'RQ3\n10k', lab_side=-1, size=6.0, lab_off=0.48)
b.wire((12, 7), (13, 7)); b.node(12, 7)
b.smd((13, 7), (13, 6), 'CG2\n1000p', lab_side=-1, size=6.0, lab_off=0.50)
b.wire((13, 6), (13, 5)); b.node(13, 6); b.node(8, 6); b.node(12, 6)
b.lbl(7.6, 6.60, 'BL1', ha='right', size=6.4, c='#b03030', bold=True)
b.lbl(12.6, 7.42, 'BL2', ha='left', size=6.4, c='#b03030', bold=True)

# --- VBL 分圧 ---
b.smd((14, 10), (14, 9), 'RVBL1\n10k', lab_side=1, size=6.2, lab_off=0.50)
b.wire((14, 9), (14, 6)); b.node(14, 9); b.node(14, 6)
b.smd((14, 6), (14, 5), 'RVBL2\n4.7k', lab_side=1, size=6.2, lab_off=0.50)
b.wire((14, 6), (15, 6)); b.smd((15, 6), (15, 5), 'CVBL\n0.1µ', lab_side=1, size=6.2, lab_off=0.52)
b.lbl(14.72, 6.42, 'VBL', ha='left', size=7.0, bold=True, c='#b03030')
b.jump((14, 6), (12, 6), (8, 6))
# --- 電源デカップリング ---
b.smd((16, 10), (16, 9), 'C0\n10µ', lab_side=1, size=6.2, lab_off=0.46)
b.wire((16, 9), (16, 5)); b.node(16, 9)

# ===================== 下半分 =====================
b.zone(0.55, 0.55, 3.45, 3.45, '', c='#a5722a', a=0.12)
b.lbl(2.0, 2.0, 'IFT\n18T\n3×3', ha='center', size=8, bold=True, c='#8a5a18')
b.node(1, 1); b.wire((1, 1), (1, 0))
b.node(3, 2); b.wire((3, 2), (4, 2))
b.wire((4, 2), (4, 4)); b.node(4, 3); b.node(4, 4)
b.lbl(4.30, 4.38, 'QD', ha='left', size=7.2, c='#b03030', bold=True)
b.jump((1, 9), (1, 4)); b.wire((1, 4), (3, 4)); b.node(1, 4)
b.lbl(1.15, 4.40, 'S4A（裏）', ha='left', size=6.4, c=JUMP, bold=True)
b.smd((3, 4), (4, 4), 'Cc 1p', lab_side=1, size=6.4, lab_off=0.44)
b.smd((4, 3), (5, 3), 'CP 100p', lab_side=1, size=6.4, lab_off=0.44)
b.smd((4, 2), (5, 2), 'Rp 4.7k', lab_side=-1, size=6.4, lab_off=0.44)
b.wire((5, 3), (5, 0)); b.node(5, 3); b.node(5, 2)
b.wire((4, 4), (6, 4))
b.tr3(6.5, 3.55, 'J17', {'G': (6, 4, -0.30, 0.02, 'right'),
                         'D': (7, 4, 0.30, 0.02, 'left'),
                         'S': (6, 3, -0.30, 0.02, 'right')}, size=6.8, w=0.90, h=0.58)
b.wire((7, 4), (8, 4)); b.node(7, 4); b.jump((8, 4), (8, 10))
b.lbl(8.15, 4.40, '+5V（裏）', ha='left', size=6.4, c=JUMP, bold=True)
b.smd((6, 3), (6, 2), 'RSF\n2.2k', lab_side=-1, size=6.2, lab_off=0.50)
b.wire((6, 2), (6, 0)); b.node(6, 2)
b.smd((6, 3), (7, 3), 'C26 1000p', lab_side=-1, size=6.4, lab_off=0.44)
b.node(7, 3); b.jump((7, 3), (7, 7))
b.lbl(7.15, 2.40, 'SF（裏で RQ1 へ）', ha='left', size=6.4, c=JUMP, bold=True)
b.lbl(0.55, 3.62, '位相シフト（IFT タンク ＋ ソースフォロア）', ha='left', size=8, bold=True, c='#8a5a18')

b.jump((10, 9), (10, 4))
b.lbl(9.85, 4.40, 'OB（裏）', ha='right', size=6.4, c=JUMP, bold=True)
b.smd((10, 4), (11, 4), 'RF 1k', lab_side=1, size=6.4, lab_off=0.44)
b.smd((11, 4), (11, 3), 'CF\n1000p', lab_side=-1, size=6.2, lab_off=0.52)
b.wire((11, 3), (11, 0)); b.node(11, 3); b.node(11, 4)
b.wire((11, 4), (12, 4))
b.tr3(12.5, 3.55, 'Q16', {'B': (12, 4, -0.30, 0.02, 'right'),
                          'E': (13, 4, 0.30, 0.02, 'left'),
                          'C': (12, 3, -0.30, 0.02, 'right')}, size=6.8, w=0.90, h=0.58)
b.jump((12, 3), (12, 10))
b.smd((13, 4), (13, 3), 'RE\n4.7k', lab_side=1, size=6.2, lab_off=0.50)
b.wire((13, 3), (13, 0)); b.node(13, 3)
b.smd((13, 4), (14, 4), 'COUT 10µ', lab_side=1, size=6.4, lab_off=0.44)
b.wire((14, 4), (15, 4)); b.node(15, 4)
b.lbl(15.25, 4.0, 'MPX OUT\n→ 74HC4046', ha='left', size=7.2, bold=True, c=WIRE)
b.lbl(9.6, 1.30, '検波後 LPF ＋ 出力バッファ', ha='left', size=8, bold=True, c='#5a5a5a')
b.save('det_board.png')
