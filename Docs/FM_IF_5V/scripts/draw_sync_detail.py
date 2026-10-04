exec(open('sch.py').read())
RED, GRY = '#c0392b', '#8a8781'
d = Sch(16.0, 10.4, dpi=160); A = d.ax

def opamp(cx, cy, name, top='−', bot='+', size=0.62, npos='bot'):
    """triangle pointing right; returns (in_top, in_bot, out)"""
    x0, x1 = cx - size, cx + size
    A.add_patch(Polygon([(x0, cy + size), (x0, cy - size), (x1, cy)], fc='white', ec=C, lw=LW, zorder=3))
    A.text(x0 + 0.13, cy + 0.30, top, fontsize=9, ha='center', va='center', zorder=5)
    A.text(x0 + 0.13, cy - 0.30, bot, fontsize=9, ha='center', va='center', zorder=5)
    if npos == 'bot':
        A.text(cx - 0.12, cy - size - 0.20, name, fontsize=7.6, ha='center', va='top', fontweight='bold', zorder=5)
    elif npos == 'top':
        A.text(cx - 0.12, cy + size + 0.12, name, fontsize=7.6, ha='center', va='bottom', fontweight='bold', zorder=5)
    else:
        A.text(cx + 0.30, cy - size + 0.05, name, fontsize=7.6, ha='left', va='top', fontweight='bold', zorder=5)
    d._t(x0, cy + size); d._t(x1, cy - size)
    return (x0, cy + 0.30), (x0, cy - 0.30), (x1, cy)

def sw(p0, p1, name, ctl, cside=1):
    """analog switch between p0 and p1 (straight), control label"""
    p0 = np.array(p0, float); p1 = np.array(p1, float)
    v = p1 - p0; L = np.hypot(*v); u = v / L; n = np.array([-u[1], u[0]])
    a = p0 + u * (L / 2 - 0.22); b = p1 - u * (L / 2 - 0.22)
    d.w(p0, a); d.w(b, p1)
    for q in (a, b):
        A.add_patch(Circle(q, 0.045, fc='white', ec=C, lw=LW, zorder=4))
    tip = b + n * 0.20 * cside
    A.plot([a[0], tip[0]], [a[1], tip[1]], '-', c=C, lw=LW, zorder=3)
    m = (a + b) / 2 + n * 0.12 * cside
    q = m + n * 0.42 * cside
    A.plot([m[0], q[0]], [m[1], q[1]], ':', c=RED, lw=1.1, zorder=3)
    A.text(*(q + n * 0.10 * cside), ctl, fontsize=7.4, ha='center', va='bottom' if cside * n[1] > 0 else 'top',
           color=RED, fontweight='bold', zorder=5)
    A.text(*((a + b) / 2 - n * 0.28 * cside), name, fontsize=7.0, ha='center', va='center', zorder=5)
    d._t(*q)

def tag(x, y, s, side='l', c='#e8eef7', ec='#556', size=7.4):
    ha = {'l': 'right', 'r': 'left', 'c': 'center'}[side]
    dx = {'l': -0.08, 'r': 0.08, 'c': 0}[side]
    A.text(x + dx, y, s, ha=ha, va='center', fontsize=size, zorder=6, fontweight='bold',
           bbox=dict(boxstyle='round,pad=0.18', fc=c, ec=ec, lw=0.8))
    d._t(x + dx + (-1.2 if side == 'l' else 1.2), y)

def vref(x, y):
    tag(x, y, 'VREF 2.5V', side='c', c='#eef5e8', ec='#6a6')

def v5(x, y, up=0.35):
    d.w((x, y), (x, y + up)); A.plot([x - 0.18, x + 0.18], [y + up, y + up], '-', c=C, lw=1.8)
    d.lbl(x, y + up + 0.10, '+5V', ha='center', va='bottom', size=6.8, bold=True)

def section(x0, y0, x1, y1, title):
    A.add_patch(plt.Rectangle((x0, y0), x1 - x0, y1 - y0, fc='none', ec=GRY, ls=(0, (4, 3)), lw=1.0, zorder=0))
    A.text(x0 + 0.12, y1 - 0.12, title, fontsize=8.4, ha='left', va='top', fontweight='bold', color='#333')
    d._t(x0, y0); d._t(x1, y1)

d.lbl(8.0, 10.95, 'MPX デコーダ 次期案 ── 新規部分の回路（位相比較・ループフィルタ・分周・ステレオ検出）', ha='center', bold=True, size=11.5)
d.lbl(8.0, 10.55, '定数は ngspice で動作確認した値（理想スイッチ・単極オペアンプモデル）。VCO 利得は仮定値のため実測して再調整すること', ha='center', size=7.8, c='#555')

# ============ COMP bus ============
XB = 0.9
tag(XB - 0.05, 8.6, 'COMP（U2C 出力）', side='l', c='#fdecea', ec=RED)
d.w((XB - 0.05, 8.6), (XB, 8.6)); d.w((XB, 8.6), (XB, 1.2))

# ============ (1) phase detector : +-1 multiplier ============
section(0.25, 5.35, 6.35, 10.2, '① 位相比較（±1 乗算器）')
im, ip, out = opamp(4.3, 7.3, 'U2A（NJM2747）')
d.dot(XB, 8.6); d.res((XB, 8.6), (2.9, 8.6), 'R61 10k', ofs=0.25)
d.dot(2.9, 8.6); d.w((2.9, 8.6), (2.9, im[1]), im)
d.w((2.9, 8.6), (2.9, 9.25)); d.res((2.9, 9.25), (5.4, 9.25), 'R62 10k', ofs=0.25)
d.w((5.4, 9.25), (5.4, out[1])); d.w(out, (5.4, out[1])); d.dot(5.4, out[1])
d.dot(XB, ip[1]); d.res((XB, ip[1]), (2.6, ip[1]), 'R60 10k', ofs=0.25)
d.dot(2.6, ip[1]); d.w((2.6, ip[1]), ip)
sw((2.6, ip[1]), (2.6, 5.85), 'U8A', 'Q', cside=-1)
vref(2.6, 5.62)
d.w((5.4, out[1]), (6.35, out[1]))
A.text(3.3, 5.62, 'Q=H → −1 倍\nQ=L → +1 倍', fontsize=7.0, ha='left', va='center', color='#333')
d.lbl(5.55, out[1] + 0.18, 'PD', size=7.6, bold=True)

# ============ (2) loop filter ============
section(6.55, 5.35, 10.35, 10.2, '② ループフィルタ（PI 積分）')
im2, ip2, out2 = opamp(8.9, 6.6, 'U2B（NJM2747）', npos='right')
d.res((6.35, out[1]), (7.75, out[1]), 'R63 47k', ofs=0.25)
d.w((7.75, out[1]), (7.75, im2[1])); d.w((7.75, im2[1]), im2); d.dot(7.75, im2[1])
d.w(ip2, (7.95, ip2[1]), (7.95, 5.75)); vref(7.95, 5.62)
XR = 9.95
d.w(out2, (XR, out2[1])); d.dot(XR, out2[1])
# three feedback branches
for yy in (7.85, 8.55, 9.25):
    d.dot(7.75, yy) if yy < 9.25 else None
    d.dot(XR, yy) if yy < 9.25 else None
d.w((7.75, im2[1]), (7.75, 9.25)); d.w((XR, out2[1]), (XR, 9.25))
d.res((7.75, 7.85), (8.85, 7.85), 'R64 7.5k', ofs=0.25); d.cap((8.85, 7.85), (XR, 7.85), 'C40 1µ', ofs=0.32)
d.cap((7.75, 8.55), (XR, 8.55), 'C41 10n', ofs=0.32)
d.res((7.75, 9.25), (XR, 9.25), 'R65 4.7M（要検討）', ofs=0.25)
d.w((XR, out2[1]), (10.35, out2[1]))

# ============ (3) VCO & dividers ============
section(10.55, 3.05, 15.95, 10.2, '③ VCO と分周（74HC4046 は VCO のみ）')
bx0, bx1, by0, by1 = 11.25, 12.95, 5.55, 8.35
A.add_patch(plt.Rectangle((bx0, by0), bx1 - bx0, by1 - by0, fc='#f6f6f4', ec=C, lw=LW, zorder=1))
A.text((bx0 + bx1) / 2, by1 - 0.22, 'U3 74HC4046', fontsize=7.8, ha='center', va='center', fontweight='bold')
d.w((10.35, out2[1]), (10.8, out2[1]), (10.8, 7.5), (bx0, 7.5))
A.text(bx0 + 0.08, 7.5, '9 VCOin', fontsize=6.8, ha='left', va='center')
A.text(10.6, 7.62, 'VCTL', fontsize=7.2, ha='right', va='bottom', fontweight='bold')
pins = [(7.05, '5 INH → GND（常時動作）'), (6.70, '6・7  C4 1n'), (6.35, '11 R1 43k+RV1 / 12 R2 470k'),
        (6.00, '3・14 使わない → GND'), (5.72, '13 PC2 オープン')]
for yy, s in pins:
    A.text(bx0 + 0.08, yy, s, fontsize=6.2, ha='left', va='center', color='#333')
A.text(bx1 - 0.08, 7.9, '4 VCOout', fontsize=6.8, ha='right', va='center')
d.w((bx1, 7.9), (13.6, 7.9)); d.lbl(13.35, 8.02, '76k', size=6.8, bold=True, ha='center', va='bottom')

def ff(x0, y0, name, d_lbl, ck_lbl, q_lbl, qb_lbl):
    w, h = 1.25, 1.35
    A.add_patch(plt.Rectangle((x0, y0), w, h, fc='#f6f6f4', ec=C, lw=LW, zorder=1))
    A.text(x0 + w / 2, y0 + h + 0.12, name, fontsize=7.4, ha='center', va='bottom', fontweight='bold')
    A.text(x0 + 0.08, y0 + h - 0.35, 'D', fontsize=7, ha='left', va='center')
    A.text(x0 + 0.08, y0 + 0.35, '>CK', fontsize=7, ha='left', va='center')
    A.text(x0 + w - 0.08, y0 + h - 0.35, 'Q', fontsize=7, ha='right', va='center')
    A.text(x0 + w - 0.08, y0 + 0.35, '/Q', fontsize=7, ha='right', va='center')
    d._t(x0, y0); d._t(x0 + w, y0 + h)
    return dict(D=(x0, y0 + h - 0.35), CK=(x0, y0 + 0.35), Q=(x0 + w, y0 + h - 0.35), QB=(x0 + w, y0 + 0.35))

f1 = ff(13.6, 7.25 - 0.95, 'U5B（現行）', '', '', '', '')
d.w((13.6, 7.9), (13.45, 7.9), (13.45, f1['CK'][1]), f1['CK'])
d.w(f1['Q'], (15.3, f1['Q'][1])); tag(15.3, f1['Q'][1], '38KHz-PLL', side='r')
d.w(f1['QB'], (15.1, f1['QB'][1])); tag(15.1, f1['QB'][1], '/38k', side='r')

f2 = ff(13.6, 4.25, 'U5A（現行）', '', '', '', '')
d.dot(15.1, f1['Q'][1]); d.w((15.1, f1['Q'][1]), (15.1, 5.95), (13.35, 5.95), (13.35, f2['CK'][1]), f2['CK'])
A.text(10.7, 9.62, 'U5A・U5B は現行どおり（D ← /Q のトグル分周）', fontsize=6.8, ha='left', va='center', color='#333')
d.w(f2['Q'], (15.3, f2['Q'][1])); tag(15.3, f2['Q'][1], 'I', side='r')
d.w(f2['QB'], (15.3, f2['QB'][1])); tag(15.3, f2['QB'][1], '/I', side='r')

f3 = ff(11.3, 3.4, 'U9A（新規 74HC74）', '', '', '', '')
A.add_patch(plt.Rectangle((11.3, 3.4), 1.25, 1.35, fc='#fdecea', ec=RED, lw=1.4, zorder=1))
for s_, yy, ha, xx in (('D', 3.4 + 1.0, 'left', 11.38), ('>CK', 3.75, 'left', 11.38), ('Q', 4.4, 'right', 12.47)):
    A.text(xx, yy, s_, fontsize=7, ha=ha, va='center', zorder=5)
tag(f3['D'][0] - 0.05, f3['D'][1], 'I', side='l')
tag(f3['CK'][0] - 0.05, f3['CK'][1], '/38k', side='l')
d.w(f3['Q'], (13.1, f3['Q'][1])); tag(13.1, f3['Q'][1], 'Q', side='r', c='#fdecea', ec=RED)
A.text(11.92, 3.2, '/S・/R → +5V', fontsize=6.2, ha='center', va='center', color='#333')

# ============ (4) stereo detect ============
section(0.25, 0.05, 10.35, 5.1, '④ ステレオ検出（切替 RC ＋ コンパレータ）')
YA, YBb = 4.0, 2.2
d.dot(XB, YA); sw((XB, YA), (2.1, YA), 'U8B', 'I', cside=-1)
d.res((2.1, YA), (3.4, YA), 'R66 10k', ofs=-0.28)
d.dot(3.6, YA); d.w((3.4, YA), (3.6, YA)); d.cap((3.6, YA), (3.6, 3.05), 'C42 1µ', ofs=0.42); d.gnd(3.6, 3.05)
d.lbl(3.72, YA + 0.20, 'SA', size=7.6, bold=True)
d.w((XB, YBb), (XB, 1.2))
d.dot(XB, YBb); sw((XB, YBb), (2.1, YBb), 'U8C', '/I', cside=-1)
d.res((2.1, YBb), (3.4, YBb), 'R67 10k', ofs=-0.28)
d.dot(3.6, YBb); d.w((3.4, YBb), (3.6, YBb)); d.cap((3.6, YBb), (3.6, 1.25), 'C43 1µ', ofs=0.42); d.gnd(3.6, 1.25)
d.lbl(3.72, YBb + 0.20, 'SB', size=7.6, bold=True)
im3, ip3, out3 = opamp(6.3, 3.1, 'U4B（LM393）', top='−', bot='+', npos='top')
d.w((3.6, YA), (5.2, YA), (5.2, im3[1]), im3)
d.res((3.6, YBb), (4.9, YBb), 'R68 10k', ofs=-0.28)
d.dot(5.2, YBb); d.w((4.9, YBb), (5.2, YBb), (5.2, ip3[1]), ip3)
d.res((5.2, YBb), (5.2, 0.85), 'R69\n2.2M', ofs=0.45, side=1); d.gnd(5.2, 0.85)
XO = 7.6
d.w(out3, (XO, out3[1])); d.dot(XO, out3[1])
d.res((5.2, YBb), (XO, YBb), 'R70 4.7M', ofs=-0.28)
d.w((XO, YBb), (XO, out3[1]))
d.res((XO, out3[1]), (XO, 4.35), 'R24 1k', ofs=0.40, side=-1); v5(XO, 4.35)
d.w((XO, out3[1]), (8.5, out3[1])); tag(8.5, out3[1], 'STEREO（旧 VCO_ENABLE）', side='r', c='#fdecea', ec=RED)
A.text(8.4, 2.25, '→ ゲート駆動 R34・R36\n→ U1B（STEREO LED）', fontsize=6.8, ha='left', va='center', color='#333')
A.text(5.65, 0.55, 'しきい値（計算値）：SB−SA ＞ 約 50 mV で ON、約 18 mV で OFF\n（シミュレーション：2 Vpp 入力で SB−SA 約 130 mV）',
       fontsize=6.8, ha='left', va='center', color=RED)

# ============ notes ============
nx, ny = 10.55, 0.05
A.add_patch(plt.Rectangle((nx, ny), 5.4, 2.85, fc='white', ec=GRY, lw=1.0, zorder=0))
notes = ['シミュレーション結果（COMP 1 Vpp・L のみ 1 kHz 100%）',
         '38 kHz 位相誤差 0.4°（現行 NJM2747 構成は約 74°）',
         'ロック時間 約 80 ms（自走 ±1 % ずれで約 220 ms、±3 % でもロック）',
         '入力 0.5〜2 Vpp で誤差 1° 以内／バイアス誤差 20 mV でも 0.7°',
         'オペアンプ Vos ±3 mV で 6〜11°（固定分は RV2 で吸収）',
         '空き：U8D・U9B・U4A・U1C（ctrl は GND へ）',
         'COMP で 2 Vpp（100 % 変調）：U2C を 2.5 倍に（R71 15k／R72 10k）']
for i, s in enumerate(notes):
    A.text(nx + 0.14, ny + 2.6 - i * 0.37, s, fontsize=7.6 if i else 7.9, ha='left', va='center',
           fontweight='bold' if i == 0 else 'normal', color='#333' if i != 6 else RED)
d._t(nx + 5.4, ny)

d.save('../figures/mpx_sync_detail.png')
