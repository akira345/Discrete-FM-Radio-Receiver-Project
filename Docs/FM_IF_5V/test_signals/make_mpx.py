#!/usr/bin/env python3
"""FMステレオ コンポジット（MPX）テスト信号ジェネレータ
   Digilent WaveForms の WaveGen "Custom" へ読み込む CSV を生成する。

   規格: m(t) = 0.45(L+R) + 0.45(L-R)*sin(2*wp*t) + 0.10*sin(wp*t)
         wp = 2*pi*19000

   バッファ1周期 = 音声1周期(1 kHz) = パイロット19周期 = 副搬送波38周期
   -> WaveGen の Frequency を 1 kHz にすると 19k / 38k が正確に出る
"""
import numpy as np

N      = 4096      # サンプル数（1周期）
F_AUD  = 1         # バッファ内の音声サイクル数 -> 1 kHz
F_PIL  = 19        # パイロット
F_SUB  = 38        # 副搬送波
PILOT  = 0.10
MAIN   = 0.45

n = np.arange(N)
ph = 2*np.pi*n/N

def composite(L, R, pilot=PILOT):
    return MAIN*(L+R) + MAIN*(L-R)*np.sin(F_SUB*ph) + pilot*np.sin(F_PIL*ph)

aud  = np.sin(F_AUD*ph)
zero = np.zeros(N)

PATTERNS = {
    "mpx_L1k"   : ("L のみ 1 kHz（L->R セパレーション）", aud,  zero),
    "mpx_R1k"   : ("R のみ 1 kHz（R->L セパレーション）", zero, aud ),
    "mpx_mono1k": ("L = R 1 kHz（L-R=0。RV2 が効かないことの確認）", aud,  aud ),
    "mpx_diff1k": ("L = -R 1 kHz（L+R=0。L-R 経路だけの確認）",      aud, -aud ),
    "mpx_pilot" : ("パイロットのみ（漏れ量の測定）",              zero, zero),
}

# 100% 変調（L のみ）のピークを共通の正規化基準にする
ref_peak = np.abs(composite(aud, zero)).max()
print(f"正規化基準 = L のみ 100% 変調時のピーク = {ref_peak:.4f}\n")
print(f"{'ファイル':<16}{'内容':<42}{'ピーク':>8}")
for name,(desc,L,R) in PATTERNS.items():
    c = composite(L,R)/ref_peak
    np.savetxt(f"{name}.csv", c, fmt="%.6f")
    print(f"{name+'.csv':<16}{desc:<42}{np.abs(c).max():8.4f}")

# --- 診断用：パイロットの位相だけをずらした信号 ---------------------------
# 「パイロット経路が遅れている」仮説の検証用（MPX_DECODER.md 3.3 節）。
# p+37 = パイロットを 37° 進めておく（経路の遅れを打ち消す）
# p-37 = さらに 37° 遅らせる
# 各ファイルは自身のピークで 1.0 に正規化（WaveForms がどのみちそうするため）
def composite_ph(L, R, deg):
    return (MAIN*(L+R) + MAIN*(L-R)*np.sin(F_SUB*ph)
            + PILOT*np.sin(F_PIL*ph + np.deg2rad(deg)))

print()
for tag, deg in (("p+37", 37), ("p-37", -37)):
    for ch, (L, R) in (("L1k", (aud, zero)), ("R1k", (zero, aud))):
        c = composite_ph(L, R, deg)
        c = c/np.abs(c).max()
        np.savetxt(f"mpx_{ch}_{tag}.csv", c, fmt="%.6f")
        print(f"mpx_{ch}_{tag}.csv  パイロット位相 {deg:+d}°")
