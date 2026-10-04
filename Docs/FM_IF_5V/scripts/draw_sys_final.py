"""FM IF ストリップ 全体回路図  rev.A"""
exec(open('sch.py').read())

d = Sch(17.0, 13.2, dpi=150)
CC = '#111'

def njf(x, y, label='', size=8.0):
    bx = x + 0.32
    d.w((x, y), (bx, y))
    d.ax.plot([bx, bx], [y - 0.52, y + 0.52], '-', c=CC, lw=1.9, zorder=3)
    cx = bx + 0.50
    d.w((bx, y + 0.40), (cx, y + 0.40), (cx, y + 0.95))
    d.w((bx, y - 0.40), (cx, y - 0.40), (cx, y - 0.95))
    d.ax.add_patch(Polygon([(bx - 0.02, y), (bx - 0.26, y + 0.10),
                            (bx - 0.26, y - 0.10)], fc=CC, ec='none', zorder=4))
    if label:
        d.lbl(cx + 0.14, y + 0.42, label, size=size, bold=True)
    return (cx, y + 0.95), (cx, y - 0.95)

def tag(x, y, s, side='l', fc='#e8eef7', size=6.6):
    ha = {'l': 'right', 'r': 'left', 'd': 'center'}[side]
    dx = {'l': -0.12, 'r': 0.12, 'd': 0.0}[side]
    dy = {'l': 0.0, 'r': 0.0, 'd': -0.20}[side]
    va = 'top' if side == 'd' else 'center'
    d.ax.text(x + dx, y + dy, s, ha=ha, va=va, fontsize=size, zorder=6,
              bbox=dict(boxstyle='round,pad=0.16', fc=fc, ec='#556', lw=0.8))
    d._t(x + dx + {'l': -1.0, 'r': 1.0, 'd': 0.0}[side], y + dy - (0.5 if side == 'd' else 0))

def rail(y, x0, x1, name, tx):
    d.ax.plot([x0, x1], [y, y], '-', c=CC, lw=1.9, zorder=2)
    d._t(x0, y); d._t(x1, y)
    d.lbl(tx, y + 0.20, name, ha='left', size=7.6, bold=True)

def v5(x, y, up=0.45, s='+5V'):
    d.w((x, y), (x, y + up))
    d.ax.plot([x - 0.22, x + 0.22], [y + up, y + up], '-', c=CC, lw=1.9)
    d.lbl(x, y + up + 0.10, s, ha='center', va='bottom', size=6.6, bold=True)

# =====================================================================
#  ROW A : 入力 ＋ 差動リミッタ 4段
# =====================================================================
YB, YVK, YVB = 16.0, 20.4, 12.3
PITCH = 5.9
X0 = [4.4 + i * PITCH for i in range(4)]

rail(YVK, 1.2, 27.9, 'VK', 28.05)
rail(YVB, 3.9, 27.9, 'VB', 28.05)
d.lbl(0.0, 22.6, 'FM IF ストリップ 全体回路図   5V / 10.7MHz', ha='left', bold=True, size=13)
d.lbl(0.0, 22.0,
      '差動リミッタ4段（Q1〜Q8）＋ ギルバート型クワドラチャ検波（QL1,QL2 / QU1〜QU4）  '
      '／ Q は全て MMBT3904（QL・QU は MMDT3904 デュアル3個でも可）', ha='left', size=8)

v5(1.2, 20.55)
d.res((1.2, 20.55), (1.2, YVK), 'Rs 10', ofs=0.45, side=1, size=7)
d.dot(1.2, YVK)
d.cap((2.3, YVK), (2.3, 19.3), 'CS 10µ', side=1, size=6.8)
d.gnd(2.3, 19.3); d.dot(2.3, YVK); d.w((1.2, YVK), (2.3, YVK))

# --- 入力 ---
d.lbl(0.0, 18.1, '■ 入力', ha='left', bold=True, size=9)
tag(0.05, YB, 'フロントエンド出力\n10.7MHz / 10mVrms', side='l')
d.w((0.05, YB), (0.55, YB))
d.box(0.55, 15.35, 2.55, 16.65)
d.lbl(1.55, 16.20, 'セラミックフィルタ', ha='center', va='center', size=6.6)
d.lbl(1.55, 15.70, 'SFELF10M7GA00', ha='center', va='center', size=6.2)
d.w((1.55, 15.35), (1.55, 14.95)); d.gnd(1.55, 14.95)
d.w((2.55, YB), (3.35, YB)); d.dot(3.35, YB)
d.res((3.35, YB), (3.35, 14.7), 'RTERM\n330', ofs=0.62, side=1, size=6.6)
d.gnd(3.35, 14.7)
d.w((3.35, YB), (X0[0] + 0.15, YB))

def stage(X, n, L):
    qa = X + 1.45
    ca, ea = d.npn(qa, YB, '', size=8.5)
    cb, eb = d.npn(X + 4.05, YB, '', flip=True, size=8.5)
    d.lbl(X + 1.32, YB - 1.02, f'Q{2*n-1}', ha='right', size=8, bold=True)
    d.lbl(X + 4.18, YB - 1.02, f'Q{2*n}', ha='left', size=8, bold=True)
    d.w(ea, (ea[0], YB - 0.78), eb)
    xe = (ea[0] + cb[0]) / 2
    d.dot(xe, YB - 0.78)
    d.res((xe, YB - 0.78), (xe, 13.55), f'RT{n} 150', ofs=0.58, side=-1, size=6.4)
    d.gnd(xe, 13.55)
    for c, sd, ln, rn, ox in ((ca, 1, f'L{2*n-1}', f'RC{2*n-1}', -0.85),
                              (cb, -1, f'L{2*n}', f'RC{2*n}', 0.85)):
        d.w(c, (c[0], 17.55)); d.dot(c[0], 17.55)
        d.ind((c[0], 17.55), (c[0], 18.55), f'{ln}\n{L}', ofs=0.52, side=sd, size=6.2)
        d.res((c[0], 18.55), (c[0], YVK), f'{rn}\n330', ofs=0.52, side=sd, size=6.2)
        d.dot(c[0], YVK)
        d.w((c[0], 17.55), (c[0] + ox, 17.55))
    tag(ca[0] - 0.85, 17.55, f'S{n}A', side='l')
    tag(cb[0] + 0.85, 17.55, f'S{n}B', side='r')
    d.cap((X + 0.15, YB), (X + 0.85, YB), f'C{2*n-1}\n100p', side=1, size=6.2)
    d.dot(X + 0.85, YB)
    d.res((X + 0.85, YB), (qa, YB), '47', ofs=0.26, side=1, size=6.2)
    d.res((X + 0.85, YB), (X + 0.85, YVB), f'RG{2*n-1}\n10k', ofs=0.56, side=1, size=6.2)
    d.dot(X + 0.85, YVB)
    d.cap((X + 5.35, YB), (X + 4.65, YB), f'C{2*n}\n100p', side=1, size=6.2)
    d.dot(X + 4.65, YB)
    d.res((X + 4.65, YB), (X + 4.05, YB), '47', ofs=0.26, side=1, size=6.2)
    d.res((X + 4.65, YB), (X + 4.65, YVB), f'RG{2*n}\n10k', ofs=0.56, side=-1, size=6.2)
    d.dot(X + 4.65, YVB)
    d.lbl(X + 2.75, 12.80, f'STAGE {n}', ha='center', size=7.4, bold=True)

for i, X in enumerate(X0):
    stage(X, i + 1, '6.8µH' if i < 2 else '0Ω')
    if i == 0:
        d.w((X + 5.35, YB), (X + 5.60, YB), (X + 5.60, 15.10))
        d.gnd(X + 5.60, 15.10)
        d.lbl(X + 5.72, 15.55, '交流接地', ha='left', size=6.2)
    else:
        tag(X + 0.15, YB, f'S{i}A', side='l')
        d.w((X + 5.35, YB), (X + 5.35, YB - 0.55))
        tag(X + 5.35, YB - 0.55, f'S{i}B', side='d')
# ---------- 4段目出力の終端（実機で追加） ----------
d.lbl(0.05, 13.85, '■ 4段目出力の終端', ha='left', bold=True, size=8)
for k, (nm, yy) in enumerate((('S4A', 13.20), ('S4B', 12.30))):
    tag(0.10, yy, nm, side='l')
    d.w((0.10, yy), (0.45, yy))
    d.cap((0.45, yy), (1.25, yy), '1000p', side=1, size=6.0)
    d.res((1.25, yy), (2.35, yy), '1k', ofs=0.26, side=1, size=6.0)
    d.w((2.35, yy), (2.70, yy), (2.70, 11.90))
d.gnd(2.70, 11.90)
d.lbl(0.05, 11.55,
      '検波基板を繋がない状態で 4段目を測るときに必要。\n'
      '検波基板接続後も付けたままでよい（実測で影響なし）。',
      ha='left', va='top', size=6.4)

d.lbl(X0[1] + 2.75, 11.75,
      'L は STAGE1・2 のみ 6.8µH（小信号でのピーキング）、STAGE3・4 は 0Ω ジャンパ\n'
      '── 飽和動作中のインダクタは電源電圧を超えるリンギングを起こすため（シミュレーションで確認）',
      ha='center', va='top', size=7)

# =====================================================================
#  ROW B
# =====================================================================
# ---------- バイアス生成 ----------
d.lbl(0.0, 9.55, '■ バイアス生成', ha='left', bold=True, size=9)
v5(1.0, 9.85)
d.res((1.0, 9.85), (1.0, 8.35), 'RD1 8.2k', ofs=0.50, side=1, size=6.6)
d.dot(1.0, 8.35)
d.res((1.0, 8.35), (1.0, 6.95), 'RD2 10k', ofs=0.50, side=1, size=6.6)
d.gnd(1.0, 6.95)
d.w((1.0, 8.35), (2.55, 8.35)); d.dot(1.85, 8.35)
d.cap((1.85, 8.35), (1.85, 7.40), '0.1µ', side=1, size=6.2)
d.gnd(1.85, 7.40)
c9, e9 = d.npn(2.55, 8.35, 'Q9', size=8.5)
d.w(c9, (c9[0], 9.85)); v5(c9[0], 9.85)
d.w(e9, (e9[0], 6.55)); d.dot(e9[0], 6.55)
d.res((e9[0], 6.55), (e9[0], 5.25), 'RB 4.7k', ofs=0.50, side=1, size=6.6)
d.gnd(e9[0], 5.25)
d.dot(4.30, 6.55); d.w((e9[0], 6.55), (4.30, 6.55))
d.cap((4.30, 6.55), (4.30, 5.60), '0.1µ', side=1, size=6.2)
d.gnd(4.30, 5.60)
d.w((4.30, 6.55), (4.75, 6.55))
tag(4.75, 6.55, 'VB 2.12V', side='r')

# ---------- 検波器バイアス ----------
for xx, r1, r2, nm, vv in ((6.6, '10k', '9.1k', 'VBU', '2.36V'),
                           (9.7, '10k', '4.7k', 'VBL', '1.59V')):
    v5(xx, 9.85)
    d.res((xx, 9.85), (xx, 8.35), r1, ofs=0.46, side=1, size=6.4)
    d.dot(xx, 8.35)
    d.res((xx, 8.35), (xx, 6.95), r2, ofs=0.46, side=1, size=6.4)
    d.gnd(xx, 6.95)
    d.dot(xx + 0.75, 8.35); d.w((xx, 8.35), (xx + 0.75, 8.35))
    d.cap((xx + 0.75, 8.35), (xx + 0.75, 7.40), '0.1µ', side=1, size=6.2)
    d.gnd(xx + 0.75, 7.40)
    d.w((xx + 0.75, 8.35), (xx + 1.20, 8.35))
    tag(xx + 1.20, 8.35, f'{nm} {vv}', side='r')

# ---------- 移相回路（IFT タンク） ----------
d.lbl(5.1, 5.55, '■ 移相回路（クワドラチャ／自作 IFT タンク）', ha='left', bold=True, size=9)
YQ = 4.30
tag(5.25, YQ, 'S4A', side='l')
d.w((5.25, YQ), (5.55, YQ))
d.cap((5.55, YQ), (6.35, YQ), 'Cc 1p', side=1, size=6.4)
d.w((6.35, YQ), (10.30, YQ))
d.lbl(5.95, YQ + 0.78, '必ず検波基板側に実装', ha='center', size=6.0, c='#b03030', bold=True)
# IFT
d.dot(6.90, YQ)
d.ind((6.90, YQ), (6.90, 2.85), 'LP 2.21µH\n(18T 自作IFT)', ofs=0.98, side=-1, size=6.2)
d.gnd(6.90, 2.85)
# 同調容量
d.dot(8.30, YQ)
d.cap((8.30, YQ), (8.30, 3.25), 'CP 100p', side=-1, size=6.2)
d.gnd(8.30, 3.25)
# ダンピング
d.dot(9.60, YQ)
d.res((9.60, YQ), (9.60, 3.05), 'Rp\n4.7k', ofs=0.48, side=-1, size=6.2)
d.gnd(9.60, 3.05)
d.lbl(8.25, YQ + 0.62, 'QD', size=6.6, bold=True)
# ソースフォロア
dr, sr = njf(10.30, YQ, 'J17')
d.w(dr, (dr[0], 5.60)); v5(dr[0], 5.60)
d.lbl(dr[0] + 0.16, YQ - 0.60, '2SK3557', size=6.2)
d.w(sr, (sr[0], 2.90)); d.dot(sr[0], 2.90)
d.res((sr[0], 2.90), (sr[0], 1.65), 'RSF 2.2k', ofs=0.54, side=-1, size=6.2)
d.gnd(sr[0], 1.65)
d.w((sr[0], 2.90), (11.30, 2.90))
d.cap((11.30, 2.90), (12.05, 2.90), 'CQ 1000p', side=1, size=6.2)
d.w((12.05, 2.90), (12.35, 2.90))
tag(12.35, 2.90, 'SF', side='r')
d.lbl(6.35, 1.55,
      'タンクを ×10 プローブで直接見ない\n'
      '（15pF で共振点が数 % 動く）。観測は SF 側。',
      ha='left', va='top', size=6.6, c='#b03030')

# ---------- ギルバート型位相検波器 ----------
GX, GY = 17.2, 0.10
YOB, YOA, YU, YT = GY + 9.2, GY + 8.6, GY + 7.1, GY + 5.85
YG1, YG2, YL, YE = GY + 5.15, GY + 4.25, GY + 3.1, GY + 1.85
d.lbl(GX - 0.3, 10.55, '■ ギルバート型 位相検波器', ha='left', bold=True, size=9)

cU = [d.npn(GX + xx, YU, f'QU{i+1}', size=8.0) for i, xx in enumerate((1.0, 3.0, 6.0, 8.0))]
(c1, e1), (c2, e2), (c3, e3), (c4, e4) = cU
d.w(e1, (e1[0], YT), (e2[0], YT), e2)
d.w(e3, (e3[0], YT), (e4[0], YT), e4)
x_cl1 = (e1[0] + e2[0]) / 2
x_cl2 = (e3[0] + e4[0]) / 2
cL1, eL1 = d.npn(GX + 2.0, YL, 'QL1', size=8.0)
cL2, eL2 = d.npn(GX + 8.52, YL, 'QL2', flip=True, size=8.0)
d.w((x_cl1, YT), (x_cl1, cL1[1])); d.dot(x_cl1, YT)
d.w((x_cl2, YT), (x_cl2, cL2[1])); d.dot(x_cl2, YT)
d.w(eL1, (eL1[0], YE), (eL2[0], YE), eL2)
xt = (eL1[0] + eL2[0]) / 2
d.dot(xt, YE)
d.res((xt, YE), (xt, GY + 0.85), 'RT 390', ofs=0.56, side=1, size=6.4)
d.gnd(xt, GY + 0.85)
d.w(c1, (c1[0], YOA), (c4[0], YOA), c4)
d.w(c2, (c2[0], YOB), (c3[0], YOB), c3)
for p in ((c1[0], YOA), (c4[0], YOA), (c2[0], YOB), (c3[0], YOB)):
    d.dot(*p)
d.w((GX + 0.7, YOA), (c1[0], YOA)); d.dot(GX + 0.7, YOA)
d.res((GX + 0.7, YOA), (GX + 0.7, 9.85), 'RLA 1.5k', ofs=0.56, side=-1, size=6.4)
v5(GX + 0.7, 9.85)
d.w((c3[0], YOB), (GX + 10.0, YOB)); d.dot(GX + 10.0, YOB)
d.res((GX + 10.0, YOB), (GX + 10.0, 9.85), 'RLB 1.5k', ofs=0.56, side=1, size=6.4)
v5(GX + 10.0, 9.85)
d.w((GX + 0.7, YOA), (GX + 0.10, YOA))
d.cap((GX + 0.10, YOA), (GX + 0.10, YOA - 1.00), '1000p', side=-1, size=6.2)
d.gnd(GX + 0.10, YOA - 1.00)
d.lbl(GX - 0.18, YOA - 0.95, 'OUT A\n（未使用）', ha='right', va='center', size=6.4, bold=True)
d.dot(GX + 10.60, YOB); d.w((GX + 10.0, YOB), (GX + 10.60, YOB))
d.cap((GX + 10.60, YOB), (GX + 10.60, YOB - 1.00), '1000p', size=6.2)
d.gnd(GX + 10.60, YOB - 1.00)
d.w((GX + 10.60, YOB), (GX + 11.15, YOB))
tag(GX + 11.15, YOB, 'OB', side='r')
d.w((GX + 1.0, YU), (GX + 0.45, YU), (GX + 0.45, YG1),
    (GX + 5.45, YG1), (GX + 5.45, YU), (GX + 6.0, YU))
d.w((GX + 3.0, YU), (GX + 2.45, YU), (GX + 2.45, YG2),
    (GX + 7.45, YG2), (GX + 7.45, YU), (GX + 8.0, YU))
d.dot(GX + 0.45, YG1); d.dot(GX + 2.45, YG2)
d.w((GX + 0.45, YG1), (GX - 0.25, YG1))
d.w((GX + 2.45, YG2), (GX - 0.25, YG2))
d.lbl(GX - 0.35, YG1, 'BU1', ha='right', size=6.6, bold=True)
d.lbl(GX - 0.35, YG2, 'BU2', ha='right', size=6.6, bold=True)
d.w((GX + 2.0, YL), (GX + 0.45, YL))
d.lbl(GX + 0.35, YL, 'BL1', ha='right', size=6.6, bold=True)
d.w((GX + 8.52, YL), (GX + 10.1, YL))
d.lbl(GX + 9.6, YL + 0.24, 'BL2', size=6.6, bold=True)
d.lbl(GX + 5.2, GY + 0.10, 'QU がスイッチングする限り出力は位相のみで決まる（＝AM に不感）',
      ha='center', size=6.6)

# ---------- 上段ドライブ ----------
XA = GX - 4.60
d.lbl(XA - 0.35, YG1 + 1.45, '■ 上段ドライブ\n（1/6.6 分圧＝500mVpp 差動）',
      ha='left', va='bottom', size=7.4, bold=True)
for yy, src, sd in ((YG1, 'S4A', 1), (YG2, 'S4B', -1)):
    tag(XA - 0.35, yy, src, side='l')
    d.w((XA - 0.35, yy), (XA - 0.10, yy))
    d.cap((XA - 0.10, yy), (XA + 0.70, yy), '1000p', side=sd, size=6.2)
    d.res((XA + 0.70, yy), (XA + 1.80, yy), '5.6k', ofs=0.26, side=sd, size=6.2)
    d.dot(XA + 1.80, yy)
    d.w((XA + 1.80, yy), (GX - 0.25, yy))
d.res((XA + 1.80, YG1), (XA + 1.80, YG1 + 1.30), '1k', ofs=0.34, side=-1, size=6.2)
tag(XA + 1.80, YG1 + 1.30, 'VBU', side='r')
d.res((XA + 1.80, YG2), (XA + 1.80, YG2 - 1.30), '1k', ofs=0.34, side=-1, size=6.2)
tag(XA + 1.80, YG2 - 1.30, 'VBU', side='r')

# ---------- 下段ドライブ ----------
tag(GX - 4.60, YL, 'SF', side='l')
d.w((GX - 4.60, YL), (GX - 4.25, YL))
d.res((GX - 4.25, YL), (GX - 3.15, YL), 'RQ1 470', ofs=0.28, side=1, size=6.2)
d.dot(GX - 3.15, YL)
d.w((GX - 3.15, YL), (GX + 0.45, YL))
d.res((GX - 3.15, YL), (GX - 3.15, YL - 1.30), 'RQ2 10k', ofs=0.54, side=-1, size=6.2)
tag(GX - 3.15, YL - 1.30, 'VBL', side='r')
d.res((GX + 10.1, YL), (GX + 11.25, YL), 'RQ3 10k', ofs=0.28, side=1, size=6.2)
tag(GX + 11.25, YL, 'VBL', side='r')
d.dot(GX + 10.65, YL)
d.cap((GX + 10.65, YL), (GX + 10.65, YL - 1.05), '1000p', size=6.2)
d.gnd(GX + 10.65, YL - 1.05)

# ---------- 検波後 LPF ＋ 出力 ----------
d.lbl(0.0, 5.20, '■ 検波後 LPF ＋ 出力バッファ', ha='left', bold=True, size=9)
YO = 3.30
tag(0.20, YO, 'OB', side='l')
d.w((0.20, YO), (0.50, YO))
d.res((0.50, YO), (1.40, YO), 'RF 1k', ofs=0.28, side=1, size=6.4)
d.dot(1.40, YO)
d.cap((1.40, YO), (1.40, 2.30), 'CF 1000p', side=-1, size=6.2)
d.gnd(1.40, 2.30)
d.w((1.40, YO), (1.90, YO))
c16, e16 = d.npn(1.90, YO, 'Q16', size=8.0)
d.w(c16, (c16[0], 3.95)); v5(c16[0], 3.95)
d.w(e16, (e16[0], 1.80)); d.dot(e16[0], 1.80)
d.res((e16[0], 1.80), (e16[0], 0.60), 'RE 4.7k', ofs=0.54, side=1, size=6.2)
d.gnd(e16[0], 0.60)
d.cap((e16[0], 1.80), (e16[0] + 1.00, 1.80), '10µ', side=1, size=6.2)
d.w((e16[0] + 1.00, 1.80), (e16[0] + 1.35, 1.80))
tag(e16[0] + 1.35, 1.80, 'MPX OUT → 74HC4046 ステレオデコーダへ', side='r')
d.lbl(0.0, 1.05,
      'fc1 = 1.5k×1000p = 106kHz / fc2 = 1k×1000p = 159kHz\n'
      '19kHz・38kHz を通すので、デエンファシスと 15kHz LPF はここには入れない',
      ha='left', va='top', size=6.8)

d.lbl(0.0, -0.35, '○のない交差は接続なし。同じ名前のタグどうしが接続される。',
      ha='left', size=7.2)
d.save('sys_final.png')
