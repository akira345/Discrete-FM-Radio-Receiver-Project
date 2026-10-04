exec(open('sch.py').read())

BLU = '#1f6feb'
ORG = '#d97706'

def vbox(s, x, y, ax, ha='center', va='center', c=BLU, size=7.2):
    ax.text(x, y, s, ha=ha, va=va, fontsize=size, color='white', zorder=6,
            fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.25', fc=c, ec='none'))

def num(s, x, y, ax, c=ORG):
    ax.add_patch(Circle((x, y), 0.20, fc=c, ec='none', zorder=6))
    ax.text(x, y, s, ha='center', va='center', fontsize=7.5, color='white',
            zorder=7, fontweight='bold')

def note(s, x, y, ax, w=5.4, c='#f6f8fa', ec='#d0d7de', size=7.2, tc=C):
    ax.text(x, y, s, ha='left', va='top', fontsize=size, color=tc, zorder=6,
            bbox=dict(boxstyle='round,pad=0.45', fc=c, ec=ec, lw=0.9))

# =====================================================================
#  FIG 1 : 1段分の詳細 ＋ 期待DC電圧
# =====================================================================
s = Sch(10.6, 8.0, dpi=170)
A = s.ax

YVK  = 9.0
YRC  = 8.15
YOUT = 7.30
YB   = 6.00
YE   = 4.65
YG   = 3.75
YVB  = 2.35

XA, XB = 3.76, 6.24
s.lbl(5.0, 10.25, 'リミッタ 1段分（LIMST）　配線チェックシート',
      ha='center', bold=True, size=10.5)
s.lbl(5.0, 9.80, '数値は検波部を未実装のときの期待 DC 電圧（ngspice .op で確認済）',
      ha='center', size=7.2, c='#555')

# ---- VK レール
s.w((0.2, YVK), (9.8, YVK))
s.lbl(0.1, YVK, 'VK', ha='right', bold=True)
vbox('\u2460  4.655 V', -0.60, YVK, A, ha='right')

# ---- コレクタ負荷
s.res((XA, YVK), (XA, YRC), 'RCA\n330\u03a9', ofs=0.62, side=1)
s.res((XB, YVK), (XB, YRC), 'RCB\n330\u03a9', ofs=0.62, side=-1)
s.ind((XA, YRC), (XA, YOUT), 'LA', ofs=0.40, side=1)
s.ind((XB, YRC), (XB, YOUT), 'LB', ofs=0.40, side=-1)
s.lbl(6.95, 3.35, '\u203b LA / LB は\n1・2段 = 6.8\u00b5H\n3・4段 = 0\u03a9 ジャンパ',
      ha='center', va='center', size=7.0, c='#b00')

# ---- トランジスタ
cA, eA = s.npn(3.0, YB, '', size=8)
cB, eB = s.npn(7.0, YB, '', flip=True, size=8)
s.lbl(XA + 0.32, YB + 0.05, 'QA', bold=True, size=8.5)
s.lbl(XB - 0.32, YB + 0.05, 'QB', ha='right', bold=True, size=8.5)
s.w(cA, (XA, YOUT)); s.w(cB, (XB, YOUT))

# ---- コレクタ取り出し
s.w((XA, YOUT), (1.10, YOUT)); s.dot(XA, YOUT)
s.w((XB, YOUT), (8.90, YOUT)); s.dot(XB, YOUT)
s.lbl(1.00, YOUT, 'OUT A', ha='right', bold=True)
s.lbl(9.00, YOUT, 'OUT B', bold=True)
vbox('\u2464  3.231 V', -0.15, YOUT, A, ha='right')
vbox('3.231 V  \u2465', 10.15, YOUT, A, ha='left')

# ---- エミッタ共通 → RT
s.w(eA, (XA, YE), (XB, YE), eB)
s.dot(5.0, YE)
s.res((5.0, YE), (5.0, YG), 'RT\n150\u03a9', ofs=0.62, side=1)
s.gnd(5.0, YG)
s.lbl(5.22, YE + 0.24, 'E', bold=True)
vbox('\u2463  1.299 V', 5.85, YE - 0.62, A, ha='left')

# ---- ベース回路 A
XBA = 1.55
s.res((XBA, YB), (3.0, YB), 'RBA 47\u03a9', ofs=0.34, side=1)
s.cap((0.05, YB), (XBA, YB), 'CIA\n100p', ofs=0.44, side=1)
s.dot(XBA, YB)
s.res((XBA, YB), (XBA, YVB), 'RGA\n10k', ofs=0.56, side=1)
s.lbl(XBA - 0.08, YB + 0.44, 'BA', ha='right', bold=True)
s.lbl(-0.05, YB, 'IN A', ha='right', bold=True)
vbox('\u2462  1.971 V \u2190 最重要', -0.95, YB, A, ha='right', c='#b00')

# ---- ベース回路 B
XBB = 8.45
s.res((XBB, YB), (7.0, YB), 'RBB 47\u03a9', ofs=0.34, side=-1)
s.cap((9.95, YB), (XBB, YB), 'CIB\n100p', ofs=0.44, side=-1)
s.dot(XBB, YB)
s.res((XBB, YB), (XBB, YVB), 'RGB\n10k', ofs=0.56, side=-1)
s.lbl(XBB + 0.08, YB + 0.44, 'BB', bold=True)
s.lbl(10.05, YB, 'IN B', bold=True)
vbox('1.971 V \u2190 最重要', 10.95, YB, A, ha='left', c='#b00')

# ---- VB レール
s.w((XBA, YVB), (XBB, YVB))
s.dot(XBA, YVB); s.dot(XBB, YVB)
s.w((XBA, YVB), (0.2, YVB))
s.lbl(0.1, YVB, 'VB', ha='right', bold=True)
vbox('\u2461  2.121 V', -0.75, YVB, A, ha='right')

# ---- 下段の注記
note('［DC の判定基準］\n'
     '\u2460 VK   4.60 \u2013 4.70 V\n'
     '\u2461 VB   2.08 \u2013 2.16 V\n'
     '\u2462 BA \u2248 BB   1.94 \u2013 2.00 V（左右差 \u2264 20 mV）★発振検査\n'
     '   BA = VB \u2212 Ib\u00d7RGA。1.5\u20131.6 V ならベース整流＝発振している\n'
     '\u2463 E    1.26 \u2013 1.34 V  \u2192 テール電流 = E \u00f7 150\u03a9 = 8.66 mA\n'
     '   ※ E は何石導通しているかの判定には使えない\n'
     '     （Vbe は電流2倍でも 18 mV しか動かない）\n'
     '\u2464\u2465 OUT A \u2248 OUT B   3.18 \u2013 3.28 V（左右差 \u2264 50 mV）\n'
     '   VK \u2212 OUT = 1.424 V ＝ RC の電圧降下',
     -1.90, 1.55, A)

note('［SOT-23 の向き：最頻出ミス］\n'
     'ピン1 = B ／ ピン2 = E ／ ピン3 = C。\n'
     'B と E が同じ側、C が単独。したがって\n'
     'QA と QB を「鏡像」に置くことはできない。\n'
     '差動対は必ず 点対称（180\u00b0 回転）で配置する。\n'
     '鏡像に置くと B と C が入れ替わる。',
     5.10, 1.55, A, c='#fff5f5', ec='#f0b0b0', tc='#7a1010')

s.save('chk_stage.png')

# =====================================================================
#  FIG 2 : バイアス部 ＋ 4段の結線マップ
# =====================================================================
s = Sch(9.6, 7.4, dpi=170)
A = s.ax

YV  = 6.60
YBR = 5.10
YVB2 = 3.70
YG2 = 2.10

s.lbl(4.4, 7.55, 'バイアス部（TA7061 方式）と 4段の結線', ha='center', bold=True, size=10)

# VCC レール
s.w((0.2, YV), (8.6, YV))
s.lbl(0.1, YV, 'VCC', ha='right', bold=True)
vbox('5.000 V', -0.70, YV, A, ha='right')

# RS 10Ω -> VK
s.res((1.4, YV), (1.4, YBR), 'RS\n10Ω', ofs=0.55, side=1)
s.w((1.4, YBR), (1.4, YG2 + 0.9)); s.dot(1.4, YBR)
s.w((0.35, YBR), (1.4, YBR))
s.lbl(0.25, YBR, 'VK', ha='right', bold=True)
vbox('4.655 V', -0.60, YBR, A, ha='right')
s.lbl(0.25, YBR - 0.45, '\u2192 全4段の RCA/RCB \u3078', ha='right', size=7.0, c='#555')
s.cap((1.4, YG2 + 0.9), (1.4, YG2), 'CS 10µ', ofs=0.52, side=1)
s.gnd(1.4, YG2)

# RD1 / RD2 分圧
s.res((3.3, YV), (3.3, YBR), 'RD1\n8.2k', ofs=0.55, side=1)
s.dot(3.3, YBR)
s.res((3.3, YBR), (3.3, YG2), 'RD2\n10k', ofs=0.55, side=1)
s.gnd(3.3, YG2)
s.lbl(3.05, YBR + 0.30, 'BREF', ha='right', bold=True)
vbox('2.738 V', 2.30, YBR, A, ha='right')
s.cap((3.3, YBR), (4.25, YBR), 'CD 0.1µ', ofs=0.40, side=-1)
s.gnd(4.25, YBR)

# Q9 エミッタフォロア
cQ, eQ = s.npn(4.9, YBR, 'Q9')
s.w((3.3, YBR), (4.9, YBR))
s.w(cQ, (cQ[0], YV)); s.dot(cQ[0], YV)
s.w(eQ, (eQ[0], YVB2), (7.9, YVB2))
s.dot(eQ[0], YVB2)
s.res((eQ[0], YVB2), (eQ[0], YG2), 'RB9\n4.7k', ofs=0.55, side=1)
s.gnd(eQ[0], YG2)
s.cap((7.0, YVB2), (7.0, YG2), 'CB 0.1µ', ofs=0.52, side=1)
s.gnd(7.0, YG2); s.dot(7.0, YVB2)
s.lbl(8.0, YVB2, 'VB → 全4段の RGA/RGB へ', bold=True)
vbox('2.121 V', 8.0, YVB2 - 0.45, A, ha='left')

s.lbl(0.2, 1.05,
      '［総電源電流の目安］  4段のみ実装時 = 35.4 mA\n'
      '   1段あたり 8.66 mA × 4 = 34.6 mA、＋ バイアス部 0.8 mA\n'
      '   30 mA を切る → どこかの段が死んでいる ／ 42 mA 超 → 電流過大か短絡',
      ha='left', va='top', size=7.4)

s.save('chk_bias.png')
