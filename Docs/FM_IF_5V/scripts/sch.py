import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Polygon
import matplotlib.font_manager as fm
import numpy as np

for f in ['Noto Sans CJK JP', 'IPAGothic', 'DejaVu Sans']:
    if any(f in x.name for x in fm.fontManager.ttflist):
        plt.rcParams['font.family'] = f
        break
plt.rcParams['font.size'] = 7.5

LW = 1.1
C = '#111'


class Sch:
    def __init__(self, w, h, dpi=170):
        self.fig, self.ax = plt.subplots(figsize=(w, h), dpi=dpi)
        self.ax.set_aspect('equal'); self.ax.axis('off')
        self.xs, self.ys = [], []

    def _t(self, x, y):
        self.xs.append(x); self.ys.append(y)

    def w(self, *pts, lw=LW, c=C):
        xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
        self.ax.plot(xs, ys, '-', c=c, lw=lw, solid_capstyle='round', zorder=2)
        for p in pts:
            self._t(*p)

    def dot(self, x, y, r=0.055):
        self.ax.add_patch(Circle((x, y), r, fc=C, ec='none', zorder=4)); self._t(x, y)

    def lbl(self, x, y, s, ha='left', va='center', size=7.5, c=C, bold=False, rot=0):
        self.ax.text(x, y, s, ha=ha, va=va, fontsize=size, color=c, zorder=5,
                     fontweight='bold' if bold else 'normal', rotation=rot)
        self._t(x, y)

    def box(self, x0, y0, x1, y1, label='', fc='none', ec=C, ls='-', lw=LW, size=7.5):
        self.ax.add_patch(plt.Rectangle((x0, y0), x1 - x0, y1 - y0, fc=fc, ec=ec,
                                        ls=ls, lw=lw, zorder=1))
        if label:
            self.ax.text((x0 + x1) / 2, (y0 + y1) / 2, label, ha='center',
                         va='center', fontsize=size, zorder=5)
        self._t(x0, y0); self._t(x1, y1)

    def _axis(self, p0, p1):
        p0 = np.array(p0, float); p1 = np.array(p1, float)
        v = p1 - p0; L = np.hypot(*v); u = v / L; n = np.array([-u[1], u[0]])
        return p0, p1, L, u, n

    def res(self, p0, p1, label='', ofs=0.30, side=1, size=7.5, body=0.62):
        p0, p1, L, u, n = self._axis(p0, p1)
        a = p0 + u * (L - body) / 2; b = p1 - u * (L - body) / 2
        self.w(p0, a); self.w(b, p1)
        pts = [a]; k = 6; h = 0.10
        for i in range(k):
            pts.append(a + u * body * (i + 0.5) / k + n * h * (1 if i % 2 == 0 else -1))
        pts.append(b)
        self.ax.plot([p[0] for p in pts], [p[1] for p in pts], '-', c=C, lw=LW, zorder=2)
        if label:
            m = (a + b) / 2 + n * ofs * side
            self.lbl(*m, label, ha='center', va='center', size=size)

    def cap(self, p0, p1, label='', side=1, size=7.5, gap=0.10, plate=0.24, ofs=0.34):
        p0, p1, L, u, n = self._axis(p0, p1)
        m = (p0 + p1) / 2
        a = m - u * gap; b = m + u * gap
        self.w(p0, a); self.w(b, p1)
        for q in (a, b):
            self.ax.plot([q[0] - n[0] * plate, q[0] + n[0] * plate],
                         [q[1] - n[1] * plate, q[1] + n[1] * plate],
                         '-', c=C, lw=LW * 1.35, zorder=2)
        if label:
            self.lbl(*(m + n * ofs * side), label, ha='center', va='center', size=size)

    def ind(self, p0, p1, label='', ofs=0.30, side=1, size=7.5, body=0.70):
        p0, p1, L, u, n = self._axis(p0, p1)
        a = p0 + u * (L - body) / 2; b = p1 - u * (L - body) / 2
        self.w(p0, a); self.w(b, p1)
        k = 4; r = body / (2 * k)
        th = np.linspace(0, np.pi, 24)
        for i in range(k):
            c = a + u * body * (i + 0.5) / k
            pts = [c + u * (-r * np.cos(t)) + n * (r * np.sin(t)) * side for t in th]
            self.ax.plot([p[0] for p in pts], [p[1] for p in pts], '-', c=C, lw=LW, zorder=2)
        if label:
            self.lbl(*((a + b) / 2 + n * ofs * side), label, ha='center', va='center', size=size)

    def gnd(self, x, y, s=0.20):
        self.w((x, y), (x, y - 0.18))
        for i, k in enumerate([1.0, 0.6, 0.25]):
            yy = y - 0.18 - i * 0.10
            self.ax.plot([x - s * k, x + s * k], [yy, yy], '-', c=C, lw=LW * 1.2, zorder=2)
        self._t(x, y - 0.5)

    def npn(self, x, y, label='', flip=False, size=7.5):
        s = -1 if flip else 1
        bx = x + s * 0.30
        self.w((x, y), (bx, y))
        self.ax.plot([bx, bx], [y - 0.34, y + 0.34], '-', c=C, lw=LW * 1.7, zorder=3)
        cx = bx + s * 0.46
        self.w((bx, y + 0.16), (cx, y + 0.52), (cx, y + 0.78))
        self.w((bx, y - 0.16), (cx, y - 0.52), (cx, y - 0.78))
        dv = np.array([cx - bx, -0.36]); dv = dv / np.hypot(*dv)
        tip = np.array([bx, y - 0.16]) + dv * 0.30
        nn = np.array([-dv[1], dv[0]])
        self.ax.add_patch(Polygon([tip + dv * 0.11, tip - dv * 0.09 + nn * 0.075,
                                   tip - dv * 0.09 - nn * 0.075], fc=C, ec='none', zorder=4))
        if label:
            self.lbl(cx + s * 0.16, y + 0.32, label,
                     ha='left' if s > 0 else 'right', size=size, bold=True)
        return (cx, y + 0.78), (cx, y - 0.78)

    def save(self, fn, pad=0.45):
        self.ax.set_xlim(min(self.xs) - pad, max(self.xs) + pad)
        self.ax.set_ylim(min(self.ys) - pad, max(self.ys) + pad)
        self.fig.savefig(fn, bbox_inches='tight', facecolor='white')
        print('wrote', fn)
