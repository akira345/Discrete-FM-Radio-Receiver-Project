exec(open('sch.py').read())
from matplotlib.patches import FancyArrowPatch
RED, BLU, GRY = '#c0392b', '#1f6feb', '#8a8781'
FNEW, FOLD = '#fdecea', '#f1f1ef'

d = Sch(16.0, 9.6, dpi=160); A = d.ax

def blk(x, y, w, h, title, sub='', new=False, size=8.2):
    ec = RED if new else '#555'; fc = FNEW if new else FOLD
    A.add_patch(plt.Rectangle((x, y), w, h, fc=fc, ec=ec, lw=1.5 if new else 1.0, zorder=1))
    A.text(x + w/2, y + h/2 + (0.13 if sub else 0), title, ha='center', va='center',
           fontsize=size, fontweight='bold', zorder=5)
    if sub:
        A.text(x + w/2, y + h/2 - 0.20, sub, ha='center', va='center', fontsize=6.6,
               color='#444', zorder=5)
    d._t(x, y); d._t(x + w, y + h)
    return dict(l=(x, y + h/2), r=(x + w, y + h/2), t=(x + w/2, y + h), b=(x + w/2, y),
                x=x, y=y, w=w, h=h)

def arr(*pts, c='#222', lw=1.2, lab=None, lpos=0.5, lofs=(0, 0.14), lsize=6.8, lc=None):
    for p, q in zip(pts[:-2], pts[1:-1]):
        A.plot([p[0], q[0]], [p[1], q[1]], '-', c=c, lw=lw, zorder=2)
    p, q = pts[-2], pts[-1]
    A.add_patch(FancyArrowPatch(p, q, arrowstyle='-|>', mutation_scale=9, color=c, lw=lw, zorder=3))
    for pp in pts: d._t(*pp)
    if lab:
        i = int(lpos * (len(pts) - 1)); i = min(i, len(pts) - 2)
        m = ((pts[i][0] + pts[i+1][0]) / 2 + lofs[0], (pts[i][1] + pts[i+1][1]) / 2 + lofs[1])
        A.text(*m, lab, ha='center', va='bottom', fontsize=lsize, color=lc or c, zorder=6,
               fontweight='bold')

d.lbl(8.0, 10.25, 'MPX デコーダ 次期案 ── コンポジット同期検波 PLL（全体構成）', ha='center', bold=True, size=12)
d.lbl(8.0, 9.85, '灰色＝現行のまま　／　赤＝新規・変更　／　19 kHz パイロット BPF 経路は全廃', ha='center', size=8.2, c='#555')

# ---------------- 音声経路（現行のまま） ----------------
YL, YR = 8.55, 7.35
j1 = blk(0.0, 7.65, 1.15, 0.65, 'J1', 'MPX IN')
buf = blk(1.55, 7.65, 1.75, 0.65, 'U2C バッファ', 'C10 / R22・R23（2.5 V）')
arr(j1['r'], buf['l'])
XC = 3.85
A.plot([buf['r'][0], XC], [7.975, 7.975], '-', c='#222', lw=1.8, zorder=2)
d.dot(XC, 7.975, r=0.07)
A.text(XC + 0.05, 8.10, 'COMP', fontsize=7.4, fontweight='bold', color=RED, ha='left', va='bottom')
sa = blk(4.35, YL - 0.30, 1.2, 0.60, 'U1A', '38k=H で ON')
sd = blk(4.35, YR - 0.30, 1.2, 0.60, 'U1D', '38k=L で ON')
A.plot([XC, XC], [YR, YL], '-', c='#222', lw=1.8, zorder=2)
arr((XC, YL), sa['l']); arr((XC, YR), sd['l'])
lpl = blk(6.05, YL - 0.30, 1.75, 0.60, 'SK-LPF（L）', 'U6 / R40・R42…')
lpr = blk(6.05, YR - 0.30, 1.75, 0.60, 'SK-LPF（R）', 'U6 / R41・R43…')
arr(sa['r'], lpl['l'], lab='SIG-L', lofs=(0, 0.04)); arr(sd['r'], lpr['l'], lab='SIG-R', lofs=(0, 0.04))
mx = blk(8.35, YR - 0.30, 1.85, YL - YR + 0.60, 'マトリクス', 'U7 ／ RV2 → 固定＋半固定')
arr(lpl['r'], (mx['x'], YL)); arr(lpr['r'], (mx['x'], YR))
del_ = blk(10.75, YL - 0.30, 1.6, 0.60, 'デエンファシス', '10k / 4700p')
der = blk(10.75, YR - 0.30, 1.6, 0.60, 'デエンファシス', '10k / 4700p')
arr((mx['x'] + mx['w'], YL), del_['l']); arr((mx['x'] + mx['w'], YR), der['l'])
ol = blk(12.9, YL - 0.30, 1.1, 0.60, 'OUT-L', '')
orr = blk(12.9, YR - 0.30, 1.1, 0.60, 'OUT-R', '')
arr(del_['r'], ol['l']); arr(der['r'], orr['l'])
gd = blk(4.10, 9.05, 1.7, 0.55, 'ゲート駆動', 'Q3〜Q6（NAND）')
arr((sa['x'] + 0.6, gd['y']), (sa['x'] + 0.6, sa['y'] + sa['h']))
A.text(sa['x'] + 0.68, gd['y'] - 0.12, 'CTL-A', fontsize=6.4, ha='left', va='center', color='#333')
arr((sd['x'] + 0.6, sd['y'] - 0.45), (sd['x'] + 0.6, sd['y']))
A.text(sd['x'] + 0.68, sd['y'] - 0.38, 'CTL-D（ゲート駆動より）', fontsize=6.4, ha='left', va='center', color='#333')

# ---------------- PLL（新規） ----------------
YP = 5.25
pd = blk(4.35, YP - 0.45, 2.2, 0.90, '位相比較', 'U8A スイッチ ＋ U2A（±1 乗算）', new=True)
lf = blk(7.10, YP - 0.45, 2.0, 0.90, 'ループフィルタ', 'U2B（PI 積分）', new=True)
vco = blk(9.65, YP - 0.45, 2.0, 0.90, 'VCO 76 kHz', '74HC4046（VCO のみ使用）')
d2a = blk(12.25, YP - 0.45, 1.55, 0.90, '÷2', 'U5B')
arr((XC, YR), (XC, YP), pd['l'], lab='', )
arr(pd['r'], lf['l'], lab='PD', lofs=(0, 0.05)); arr(lf['r'], vco['l'], lab='VCOin', lofs=(0, 0.05))
arr(vco['r'], d2a['l'], lab='76k', lofs=(0, 0.05))
YD = 3.35
d2b = blk(12.25, YD - 0.45, 1.55, 0.90, '÷2', 'U5A')
q90 = blk(9.65, YD - 0.45, 2.0, 0.90, '90° 遅延 FF', 'U9A（D=I, CK=/38k）', new=True)
arr(d2a['b'], d2b['t'], lab='38KHz-PLL', lofs=(0.62, -0.05))
arr(d2b['l'], (q90['x'] + q90['w'], YD), lab='I', lofs=(0, 0.05))
arr((q90['x'], YD), (5.45, YD), (5.45, pd['y']), lab='Q（19k・90°遅れ）', lpos=0.0, lofs=(-1.0, 0.05), c=RED)
# 38k to gate drive
A.plot([13.8, 14.45], [YP, YP], '-', c='#222', lw=1.2, zorder=2)
arr((14.45, YP), (14.45, 9.33), (gd['x'] + gd['w'], 9.33))
A.text(14.55, 6.9, '38KHz-PLL\n38KHz-PLL-INV', fontsize=6.8, ha='left', va='center', fontweight='bold')

# ---------------- ステレオ検出（新規） ----------------
st = blk(4.35, 1.25, 2.6, 0.95, 'ステレオ検出', 'U8B/U8C 切替RC ＋ U4B', new=True)
arr((XC, YP), (XC, st['y'] + st['h'] / 2), st['l'])
# I and /I from U5A
A.plot([d2b['x'] + d2b['w'] / 2, d2b['x'] + d2b['w'] / 2, st['x'] + st['w'] - 0.5], [d2b['y'], 2.55, 2.55], '-', c='#222', lw=1.2)
arr((st['x'] + st['w'] - 0.5, 2.55), (st['x'] + st['w'] - 0.5, st['y'] + st['h']))
A.text(9.2, 2.62, 'I ／ /I（U5A の Q・/Q）', fontsize=6.8, ha='center', va='bottom', fontweight='bold')
led = blk(8.35, 1.25, 1.6, 0.95, 'STEREO LED', 'U1B / D2（現行）')
arr(st['r'], led['l'], lab='STEREO', lofs=(0, 0.05), c=RED)
A.plot([7.45, 7.45], [st['y'] + st['h'] / 2, 0.75], '-', c=RED, lw=1.2)
A.plot([7.45, 3.55, 3.55], [0.75, 0.75, 9.32], '-', c=RED, lw=1.2)
arr((3.55, 9.32), (gd['x'], 9.32), c=RED)
A.text(3.40, 4.9, 'STEREO\n（旧 VCO_ENABLE）\n＝ L で両スイッチ ON\n＝モノラル', fontsize=6.6, ha='right', va='center', color=RED)

# ---------------- 削除リスト ----------------
rx, ry = 10.3, 0.05
A.add_patch(plt.Rectangle((rx, ry), 5.7, 2.25, fc='white', ec=GRY, ls=(0, (4, 3)), lw=1.1, zorder=1))
lines = ['削除（パイロット BPF 経路）',
         'Q1・R6・R9・R10・C2・C9',
         'U2A/U2B の BPF（R20・R21・R25〜R27・R29・C11〜C15）',
         'C16・R32・U4A・R37（19KHzRect）',
         'Q2・C1・R3・R7・R11・D1・R14・R15・C6・R18・R19（旧判定）',
         '4046 の PC2 ループ（R16・R17・C8）、VCO 停止（U1C・R8）']
for i, s in enumerate(lines):
    A.text(rx + 0.15, ry + 2.02 - i * 0.33, s, fontsize=7.6 if i else 8.0, ha='left', va='center',
           fontweight='bold' if i == 0 else 'normal', color='#333')
d._t(rx + 5.7, ry)

# note on VCO free-run
A.text(10.65, 4.22, 'VCO は常時動作（パイロット無しでも自走）\n→ 同期検波でステレオ判定するため',
       fontsize=6.8, ha='center', va='center', color=RED)

d.save('../figures/mpx_sync_block.png')
