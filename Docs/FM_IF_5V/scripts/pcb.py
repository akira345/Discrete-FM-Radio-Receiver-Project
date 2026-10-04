"""2.54mm ユニバーサル基板 + SMD実装 の配置図を描くための小道具"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyBboxPatch, Rectangle, Polygon
import matplotlib.font_manager as fm
import numpy as np

for f in ['Noto Sans CJK JP', 'IPAGothic', 'DejaVu Sans']:
    if any(f in x.name for x in fm.fontManager.ttflist):
        plt.rcParams['font.family'] = f
        break

INK   = '#15181c'
HOLE  = '#9aa3ad'
BOARD = '#f3efe4'
WIRE  = '#1f4e79'
PART  = '#e8d9b8'
PARTE = '#8a7a54'
GNDC  = '#2f7d32'
JUMP  = '#b03030'


class Board:
    def __init__(self, ncol, nrow, w=16, h=10, dpi=170):
        self.fig, self.ax = plt.subplots(figsize=(w, h), dpi=dpi)
        self.ax.set_aspect('equal'); self.ax.axis('off')
        self.ncol, self.nrow = ncol, nrow
        self.ax.add_patch(Rectangle((-0.8, -0.8), ncol + 0.6, nrow + 0.6,
                                    fc=BOARD, ec='#b9b09a', lw=1.4, zorder=0))
        for x in range(ncol):
            for y in range(nrow):
                self.ax.add_patch(Circle((x, y), 0.13, fc='white', ec=HOLE,
                                         lw=0.7, zorder=1))
        self.xs = [-1.0, ncol + 0.2]; self.ys = [-1.0, nrow + 0.2]

    def t(self, x, y):
        self.xs.append(x); self.ys.append(y)

    # ---------- 配線 ----------
    def wire(self, *pts, c=WIRE, lw=2.6, z=3, ls='-'):
        self.ax.plot([p[0] for p in pts], [p[1] for p in pts], c=c, lw=lw,
                     linestyle=ls, solid_capstyle='round', zorder=z)
        for p in pts:
            self.t(*p)

    def jump(self, *pts):
        self.wire(*pts, c=JUMP, lw=2.0, z=6, ls=(0, (5, 2)))

    def node(self, x, y, c=WIRE, r=0.19):
        self.ax.add_patch(Circle((x, y), r, fc=c, ec='none', zorder=5)); self.t(x, y)

    def gnd(self, x, y, label=None):
        self.ax.add_patch(Circle((x, y), 0.30, fc=GNDC, ec='white', lw=1.0, zorder=5))
        self.ax.plot([x], [y], marker='x', c='white', ms=4.5, mew=1.4, zorder=6)
        self.t(x, y)

    # ---------- 部品 ----------
    def smd(self, p0, p1, label, sub='', size=7.2, wdt=0.42, lab_side=1, lab_off=0.62):
        p0 = np.array(p0, float); p1 = np.array(p1, float)
        m = (p0 + p1) / 2; v = p1 - p0; L = np.hypot(*v); u = v / L
        n = np.array([-u[1], u[0]])
        ang = np.degrees(np.arctan2(*u[::-1]))
        body_l = L * 0.62
        rect = FancyBboxPatch((-body_l / 2, -wdt / 2), body_l, wdt,
                              boxstyle='round,pad=0.02,rounding_size=0.06',
                              fc=PART, ec=PARTE, lw=1.0, zorder=4)
        tr = matplotlib.transforms.Affine2D().rotate_deg(ang).translate(*m) + self.ax.transData
        rect.set_transform(tr); self.ax.add_patch(rect)
        self.wire(p0, m - u * body_l / 2, lw=2.2)
        self.wire(m + u * body_l / 2, p1, lw=2.2)
        txt = label + (('\n' + sub) if sub else '')
        tx = m + n * lab_off * lab_side
        ha = 'center'
        if abs(n[0]) > abs(n[1]):
            ha = 'left' if n[0] * lab_side > 0 else 'right'
        self.ax.text(tx[0], tx[1], txt, ha=ha, va='center', fontsize=size,
                     color=INK, zorder=7, fontweight='bold', linespacing=1.15)
        self.t(tx[0] + (1.4 if ha == 'left' else -1.4), tx[1])

    def tr3(self, cx, cy, label, pins, size=8.5, w=1.35, h=0.85):
        """pins = {'B': (x, y, dx, dy, ha), ...}"""
        self.ax.add_patch(FancyBboxPatch((cx - w / 2, cy - h / 2), w, h,
                          boxstyle='round,pad=0.02,rounding_size=0.08',
                          fc='#3a3f46', ec='#22262b', lw=1.0, zorder=5))
        self.ax.text(cx, cy, label, ha='center', va='center', fontsize=size,
                     color='white', zorder=6, fontweight='bold')
        for k, q in pins.items():
            x, y, dx, dy, ha = q
            self.wire((cx, cy), (x, y), lw=2.2, z=4)
            self.ax.text(x + dx, y + dy, k, ha=ha, va='center',
                         fontsize=6.6, color='#b03030', zorder=7, fontweight='bold')
            self.node(x, y, c='#3a3f46', r=0.16)
        self.t(cx, cy)

    def lbl(self, x, y, s, ha='left', va='center', size=8, c=INK, bold=False, rot=0, bg=None):
        kw = {}
        if bg:
            kw['bbox'] = dict(fc=bg, ec='none', pad=1.6)
        self.ax.text(x, y, s, ha=ha, va=va, fontsize=size, color=c, zorder=8,
                     fontweight='bold' if bold else 'normal', rotation=rot, **kw)
        self.t(x, y)

    def zone(self, x0, y0, x1, y1, label='', c='#3a6ea5', ls='--', a=0.05, size=9):
        self.ax.add_patch(Rectangle((x0, y0), x1 - x0, y1 - y0, fc=c, alpha=a,
                                    ec=c, lw=1.4, ls=ls, zorder=2))
        if label:
            self.ax.text((x0 + x1) / 2, y1 + 0.28, label, ha='center', va='bottom',
                         fontsize=size, color=c, zorder=8, fontweight='bold')
        self.t(x0, y0); self.t(x1, y1)

    def save(self, fn, pad=0.5):
        self.ax.set_xlim(min(self.xs) - pad, max(self.xs) + pad)
        self.ax.set_ylim(min(self.ys) - pad, max(self.ys) + pad)
        self.fig.savefig(fn, bbox_inches='tight', facecolor='white')
        print('wrote', fn)


SOT_L, SOT_W, SOT_PAD, SOT_OFF = 1.15, 0.52, 0.47, 0.19

def sot23_pads(cx, cy, rot):
    """rot: 'Cup'|'Cright'|'Cdown'|'Cleft' → {'C':(x,y),'B':(x,y),'E':(x,y)} と本体角度"""
    base = {'Cup':   (( 0,  1), (-SOT_OFF, -1), ( SOT_OFF, -1), 0),
            'Cright':(( 1,  0), (-1,  SOT_OFF), (-1, -SOT_OFF), 90),
            'Cdown': (( 0, -1), ( SOT_OFF,  1), (-SOT_OFF,  1), 0),
            'Cleft': ((-1,  0), ( 1, -SOT_OFF), ( 1,  SOT_OFF), 90)}[rot]
    (cu, cv), (bu, bv), (eu, ev), ang = base
    def P(u, v):
        return (cx + u * SOT_PAD, cy + v * SOT_PAD)
    return {'C': P(*base[0]), 'B': P(*base[1]), 'E': P(*base[2])}, ang


def sot23(bd, cx, cy, rot, label, holes, size=8.0, note=''):
    """holes = {'B':(x,y), 'C':(x,y), 'E':(x,y)} 実際に配線する穴"""
    pads, ang = sot23_pads(cx, cy, rot)
    w, h = (SOT_L, SOT_W) if ang == 0 else (SOT_W, SOT_L)
    bd.ax.add_patch(Rectangle((cx - w / 2, cy - h / 2), w, h, fc='#3a3f46',
                              ec='#22262b', lw=1.0, zorder=5))
    bd.ax.text(cx, cy, label, ha='center', va='center', fontsize=size,
               color='white', zorder=7, fontweight='bold')
    col = {'B': '#c8503a', 'C': '#3a6ea5', 'E': '#2f7d32'}
    for k in 'BCE':
        px, py = pads[k]
        bd.ax.add_patch(Rectangle((px - 0.12, py - 0.10), 0.24, 0.20,
                                  fc='#c0c6cc', ec='#6b7177', lw=0.7, zorder=6))
        bd.wire((px, py), holes[k], c=col[k], lw=2.0, z=6)
        bd.node(*holes[k], c=col[k], r=0.17)
        bd.ax.text(holes[k][0], holes[k][1] + 0.33, k, ha='center', va='bottom',
                   fontsize=7.0, color=col[k], zorder=8, fontweight='bold')
    if note:
        bd.ax.text(cx, cy - h / 2 - 0.42, note, ha='center', va='top',
                   fontsize=6.6, color='#5a5a5a', zorder=8)
    bd.t(cx, cy)
