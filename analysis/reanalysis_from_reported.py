"""Re-analyses for the PAA revision that need only numbers already reported in the
manuscript or printed in the released notebooks (no per-image data required).

Updated 16 Nov 2026: Table 10 uses the unrounded standard-error ratios printed by PHASE3_1 and PHASE3_2,
the three fine-tuning seeds are added, and sections 4 and 5 use the per-family means of the re-run
(results/revision_G1/extra/per_family_deltas_rerun.csv; override with SDIC_PER_FAMILY).

Outputs: printed tables, plus CSVs in ./out/.
"""
import math, os
import numpy as np
from scipy import stats

os.makedirs('out', exist_ok=True)
Fm = 6  # test families

# ---------------------------------------------------------------- 1. Table 5 labels (R2.1)
# Phase 0.11 notebook output: family-level t CI and image-level bootstrap CI per comparison
P011 = {  # comparison: (family CI lo, hi, image CI lo, hi)
 'C4 vs C2':  (-0.2107, 0.2290, -0.0096, 0.0289), 'C4 vs C5':  (-0.3765, 0.2276, -0.1012, -0.0489),
 'C6c vs C2': (-0.6016, 1.1038,  0.2137, 0.2887), 'C6c vs C5': (-0.7489, 1.0839,  0.1321,  0.2023),
 'C7 vs C2':  (-0.3626, 0.5420,  0.0703, 0.1097), 'C7 vs C5':  (-0.5228, 0.5350, -0.0235,  0.0354),
 'C7q vs C2': (-0.1720, 0.1393, -0.0278, -0.0049),'C7q vs C5': (-0.3467, 0.1468, -0.1263, -0.0739),
 'C8 vs C2':  (-0.1693, 0.5002,  0.1181, 0.2149), 'C8 vs C5':  (-0.1415, 0.3052,  0.0574,  0.1079),
 'C8b vs C2': (-0.1475, 0.2315,  0.0162, 0.0685), 'C8b vs C5': (-0.1670, 0.0837, -0.0525, -0.0308)}
T5_PUBLISHED = [  # label as printed, sigma_a, sigma_e, rho, ratio
 ('C4 vs C2', .313, 1.815, .029, 5.28), ('C8b vs C2', .178, .981, .032, 5.55),
 ('C4 vs C5', .211, .947, .047, 6.74), ('C7q vs C5', .233, .984, .053, 7.17),
 ('C6c vs C2', .208, .721, .077, 8.72), ('C6c vs C5', .286, .980, .079, 8.84),
 ('C8b vs C5', .119, .406, .079, 8.84), ('C7q vs C2', .148, .428, .106, 10.38),
 ('C8 vs C5', .503, 1.103, .172, 13.71), ('C7 vs C2', .811, 1.405, .250, 17.35),
 ('C8 vs C2', .430, .738, .253, 17.49), ('C7 vs C5', .872, 1.315, .305, 19.90)]
m = 900; tq = stats.t.ppf(.975, Fm - 1)
recon = {}
for k, (flo, fhi, ilo, ihi) in P011.items():
    sd_f = (fhi - flo) / 2 * math.sqrt(Fm) / tq          # SD of the six family means
    se_img = (ihi - ilo) / (2 * 1.96)                      # image-level SE (percentile CI)
    s_e = se_img * math.sqrt(m * Fm)                       # two-component sigma_e
    s_a = math.sqrt(max(sd_f ** 2 - s_e ** 2 / m, 0))      # moment estimator
    recon[k] = (s_a, s_e)
print('== 1. Table 5: printed label -> comparison whose recomputed (sigma_a, sigma_e) matches')
rows = []
for lab, sa, se, rho, ratio in T5_PUBLISHED:
    best = min(recon, key=lambda k: (recon[k][0] - sa) ** 2 + ((recon[k][1] - se) / 2) ** 2)
    ra, re_ = recon[best]
    flag = '' if best == lab else '   <-- label differs'
    print(f'  printed {lab:9s} (sa {sa:.3f}, se {se:.3f})  matches {best:9s} (sa {ra:.3f}, se {re_:.3f}){flag}')
    rows.append((lab, best, sa, se, rho, ratio))
np.savetxt('out/table5_label_map.csv', np.array(rows, dtype=object), fmt='%s', delimiter=',',
           header='printed_label,true_comparison,sigma_a,sigma_e,rho,se_ratio', comments='')

# ---------------------------------------------------------------- 2. exact crossed-model inference (R2.2, R3.1)
# Under d_if = mu + a_f + b_i + e_if (balanced, complete, normal), MS_A/MS_I = R^2 and
# R^2 * (sigma_e^2 + F sigma_b^2)/(sigma_e^2 + m sigma_a^2) ~ F(F-1, m-1).
def exact(R, m, F=Fm):
    fu, fl = stats.f.ppf(.975, F - 1, m - 1), stats.f.ppf(.025, F - 1, m - 1)
    th_lo, th_hi = R ** 2 / fu, R ** 2 / fl
    p = stats.f.sf(R ** 2, F - 1, m - 1)                  # conservative p for sigma_a^2 = 0
    g = lambda th: ((th - 1) / m) / (1 + (th - 1) / m)     # lower bound map to rho
    return math.sqrt(th_lo), math.sqrt(th_hi), p, g(th_lo), math.sqrt(1 + 1 / R ** 2) - 1
SETS = {
 'NEU-CLS ResNet-50, twelve-arm grid (Table 5)': (900, [5.28, 5.55, 6.74, 7.17, 8.72, 8.84, 8.84, 10.38, 13.71, 17.35, 17.49, 19.90]),
 'NEU-CLS five backbones (Table 7)': (900, [8.2482, 5.8476, 10.1276, 7.7852, 6.7123, 5.6172, 9.5768, 5.6429, 9.3010, 8.3923]),
 'Magnetic Tile five backbones (Table 8)': (1344, [14.8324, 13.9611, 25.4338, 21.7108, 12.9842, 16.1735, 9.6222, 8.6081, 7.2011, 4.9978]),
 'Fine-tuning control (Table 10; median seed for the fine-tuned row)': (900, [8.2482, 13.7441, 20.2721]),
 'Fine-tuned, three seeds (Section 6.10)': (900, [18.2442, 20.2721, 23.1819]),
}
print('\n== 2. Exact 95% CI for the SE ratio under the crossed model, conservative test of sigma_a^2 = 0,')
print('      97.5% lower confidence bound on rho, and bound on the full-crossed SE inflation')
allrows = []
for name, (mm, Rs) in SETS.items():
    print(f'  {name} (m = {mm}, df = 5, {mm - 1})')
    for R in Rs:
        lo, hi, p, rlo, infl = exact(R, mm)
        allrows.append((name, R, lo, hi, p, rlo, infl))
        print(f'    ratio {R:6.2f}  95% CI [{lo:5.2f}, {hi:6.2f}]  p <= {p:.1e}  rho >= {rlo:.3f}  full SE <= +{100*infl:.1f}%')
mins = min(r[2] for r in allrows); maxinfl = max(r[6] for r in allrows); maxp = max(r[4] for r in allrows)
print(f'  smallest lower CI limit on any SE ratio: {mins:.2f}; largest p: {maxp:.1e}; largest full-SE inflation: {100*maxinfl:.1f}%')

# ---------------------------------------------------------------- 3. two-way ANOVA F tests for Table 6 (pipeline B)
print('\n== 3. Exact two-way ANOVA F tests, crossed decomposition (Table 6, Phase 4 output)')
for lab, sa, sb, se in [('C4 vs C2', .0441, .0396, .1257), ('C4 vs C5', .2135, .3042, .8449)]:
    MSA = se ** 2 + m * sa ** 2; MSE = se ** 2; FA = MSA / MSE; d2 = (m - 1) * (Fm - 1)
    lam_lo = (FA / stats.f.ppf(.975, Fm - 1, d2) - 1) / m; lam_hi = (FA / stats.f.ppf(.025, Fm - 1, d2) - 1) / m
    sefam2 = sa ** 2 / Fm + se ** 2 / (m * Fm); sefull2 = sefam2 + sb ** 2 / m; seimg2 = sb ** 2 / m + se ** 2 / (m * Fm)
    print(f'  {lab}: F = {FA:.1f} on (5, {d2}) df, p = {stats.f.sf(FA, Fm - 1, d2):.1e}; '
          f'sigma_a^2/sigma_e^2 in [{lam_lo:.3f}, {lam_hi:.3f}]; '
          f'SE full/family = {math.sqrt(sefull2 / sefam2):.4f}, full/image = {math.sqrt(sefull2 / seimg2):.2f}')

# ---------------------------------------------------------------- 4. leave-one-family-out from the re-run per-family means (R2.6)
FAM = ['motion_blur', 'shot_noise', 'brightness_drift', 'contrast_loss', 'vignetting', 'vibration_jitter']
PFD = os.environ.get('SDIC_PER_FAMILY', 'results/revision_G1/extra/per_family_deltas_rerun.csv')
import csv
T4 = {}
with open(PFD, newline='') as f:
    for row in csv.DictReader(f):
        T4[row['']] = [float(row[k]) for k in FAM]
print(f'\n== 4. Leave-one-family-out family-level t tests (df = 4), re-run per-family means ({PFD})')
for k, v in T4.items():
    v = np.array(v); res = []
    for i, fam in enumerate(FAM):
        w = np.delete(v, i); t, p = stats.ttest_1samp(w, 0); res.append((fam, w.mean(), t, p))
    sig = [f'{fam} (mean {mn:+.3f}, p = {p:.3f})' for fam, mn, t, p in res if p < 0.05]
    other = min(p for fam, mn, t, p in res if fam != 'vignetting')
    print(f'  {k}: significant when omitting: {sig or "none"}; smallest p when omitting another family = {other:.3f}')

# ---------------------------------------------------------------- 5. power and design table (R1.6, R2.6)
def power(d, n, a=.05):
    df = n - 1; tc = stats.t.ppf(1 - a / 2, df); nc = d * math.sqrt(n)
    return 1 - stats.nct.cdf(tc, df, nc) + stats.nct.cdf(-tc, df, nc)
def n_needed(d, target=.8):
    for n in range(3, 2000):
        if power(d, n) >= target: return n
print('\n== 5. Families needed for 80% power (two-sided one-sample t test on family means, alpha = 0.05)')
for d in (0.185, 0.2, 0.3, 0.4, 0.6, 0.8, 1.0, 1.2):
    print(f'  d = {d:<5}  power at F=6: {power(d, 6):.2f}   F needed: {n_needed(d)}')
# 95% CI for d from six families: C7q vs C5 in the re-run (Table 4)
v = np.array(T4['C7q vs C5']); tobs = abs(v.mean()) / v.std(ddof=1) * math.sqrt(6)
f_lo = lambda nc: stats.nct.sf(tobs, 5, nc) - 0.025
f_hi = lambda nc: stats.nct.cdf(tobs, 5, nc) - 0.025
from scipy.optimize import brentq
nc_lo = brentq(f_lo, -10, 10); nc_hi = brentq(f_hi, -10, 10)
print(f'  C7q vs C5: |d| = {tobs / math.sqrt(6):.3f}; 95% CI for d (sign of the observed effect): '
      f'[{nc_lo / math.sqrt(6):.2f}, {nc_hi / math.sqrt(6):.2f}]; power at F=6: {power(tobs / math.sqrt(6), 6):.2f}; '
      f'F for 80%: {n_needed(tobs / math.sqrt(6))}')

# ---------------------------------------------------------------- 6. heteroskedastic null check for the permutation test (R2.3, R3.2)
print('\n== 6. Within-image permutation test under a heteroskedastic null (no family effect)')
rng = np.random.default_rng(20261101)
mm, FF, B, reps = 900, 6, 400, 300
sd_f = np.array([0.4, 0.6, 0.8, 1.0, 1.5, 2.2])            # family-specific residual SDs
rej = 0; ratios = []
for r in range(reps):
    b = rng.normal(0, 0.3, (mm, 1))
    common = rng.normal(0, 1, (mm, 1))                       # correlated residuals within image
    e = (0.5 * common + math.sqrt(1 - 0.25) * rng.normal(0, 1, (mm, FF))) * sd_f
    D = 0.1 + b + e
    obs = D.mean(0).var(ddof=1)
    null = np.empty(B)
    for j in range(B):
        idx = np.argsort(rng.random((mm, FF)), axis=1)
        null[j] = np.take_along_axis(D, idx, axis=1).mean(0).var(ddof=1)
    p = (np.sum(null >= obs) + 1) / (B + 1); rej += p < 0.05; ratios.append(obs / np.median(null))
ratios = np.array(ratios)
print(f'  family residual SDs {sd_f.tolist()}, within-image residual correlation 0.25, {reps} replicates x {B} permutations')
print(f'  type-I error at 0.05: {rej / reps:.3f};  observed/permutation-median ratio: median {np.median(ratios):.2f}, 99th pct {np.quantile(ratios, .99):.2f}, max {ratios.max():.2f}')
