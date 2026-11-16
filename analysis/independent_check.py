"""Independent recomputation of the revised Table 4/5 values and the power figures, without the
revision_analyses library (plain pandas/numpy/scipy, different GCI seed, statsmodels power).

Usage: python3 -I independent_check.py <per_image_nll_G1.csv.gz>
"""
import sys, math
import numpy as np, pandas as pd
from scipy import stats

df = pd.read_csv(sys.argv[1]); df["arm"] = df.arm.astype(str)
t = df[df.family != "clean"]
FAM = ["motion_blur", "shot_noise", "brightness_drift", "contrast_loss", "vignetting", "vibration_jitter"]
wide = t.pivot_table(index=["image_id", "family", "severity"], columns="arm", values="nll")
out = []
for B in ["C2", "C5"]:
    for A in ["C4", "C6c", "C7", "C7q", "C8", "C8b"]:
        d = (wide[A] - wide[B]).groupby(level=["image_id", "family"]).mean().unstack("family")[FAM]
        D = d.to_numpy(); m, F = D.shape
        fam = D.mean(0); img = D.mean(1); g = D.mean()
        MSA = m * ((fam - g) ** 2).sum() / (F - 1); MSB = F * ((img - g) ** 2).sum() / (m - 1)
        MSE = ((D - img[:, None] - fam[None, :] + g) ** 2).sum() / ((m - 1) * (F - 1))
        s2a2 = max((MSA - MSB) / m, 0); rho2 = s2a2 / (s2a2 + MSB)
        R = math.sqrt(MSA / MSB)
        lo = R / math.sqrt(stats.f.ppf(0.975, F - 1, m - 1)); hi = R / math.sqrt(stats.f.ppf(0.025, F - 1, m - 1))
        rho_lo = (lo ** 2 - 1) / (lo ** 2 - 1 + m)
        rng = np.random.default_rng(12345); n = 40000
        GA = (F - 1) * MSA / rng.chisquare(F - 1, n); GB = (m - 1) * MSB / rng.chisquare(m - 1, n)
        GE = (m - 1) * (F - 1) * MSE / rng.chisquare((m - 1) * (F - 1), n)
        ga = np.maximum((GA - GE) / m, 0); gb = np.maximum((GB - GE) / F, 0); rr = ga / (ga + gb + GE)
        s2a = max((MSA - MSE) / m, 0); s2b = max((MSB - MSE) / F, 0)
        rhof = s2a / (s2a + s2b + MSE)
        Fst = MSA / MSE; p = stats.f.sf(Fst, F - 1, (m - 1) * (F - 1))
        sd = fam.std(ddof=1); tt = g / (sd / math.sqrt(F)); pf = 2 * stats.t.sf(abs(tt), F - 1)
        out.append(dict(cmp=f"{A} vs {B}", **{f[:4]: round(x, 3) for f, x in zip(FAM, fam)}, mean=round(g, 3),
                        sa=round(math.sqrt(s2a2), 3), se=round(math.sqrt(MSB), 3), rho=round(rho2, 3), rho_lo=round(rho_lo, 3),
                        R=round(R, 2), Rlo=round(lo, 2), Rhi=round(hi, 2), rhof=round(rhof, 3),
                        gci=(round(float(np.quantile(rr, .025)), 3), round(float(np.quantile(rr, .975)), 3)),
                        F=round(Fst, 1), p=f"{p:.1e}", p_fam=round(pf, 3), d=round(g / sd, 3)))
pd.set_option("display.width", 250); pd.set_option("display.max_columns", 40)
print(pd.DataFrame(out).to_string(index=False))
try:
    from statsmodels.stats.power import TTestPower
    tp = TTestPower()
    for d in (0.185, 0.2002):
        print("statsmodels d=%.4f" % d, [round(tp.power(effect_size=d, nobs=n, alpha=0.05), 3) for n in (6, 12, 20, 30)],
              "n80=%.1f" % tp.solve_power(effect_size=d, power=0.8, alpha=0.05))
except Exception as e:
    print("statsmodels unavailable:", e)
