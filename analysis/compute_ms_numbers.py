"""Every number the revised manuscript quotes from grid G1, computed from the re-run per-image table.

Usage: python3 -I compute_ms_numbers.py <per_image_nll_G1.csv.gz> <revision_analyses.py> <out_dir>
"""
import sys, json, math, importlib.util
import numpy as np, pandas as pd
from scipy import stats

csv, lib_path, out = sys.argv[1], sys.argv[2], sys.argv[3]
spec = importlib.util.spec_from_file_location("ra", lib_path)
ra = importlib.util.module_from_spec(spec); spec.loader.exec_module(ra)

df = ra.load_long([csv])
g = df[(df.dataset == "NEU-CLS") & (df.run == "G1")]
test = g[g.family != "clean"]
FAM = ["motion_blur", "shot_noise", "brightness_drift", "contrast_loss", "vignetting", "vibration_jitter"]
ARMS_T = ["C4", "C6c", "C7", "C7q", "C8", "C8b"]
PAIRS = [(a, "C2") for a in ARMS_T] + [(a, "C5") for a in ARMS_T]
res = {}

# ---- Table 3: NLL fold mean +/- SD (fold mean over its images x families x severities)
fm = test.groupby(["arm", "fold"]).nll.mean().unstack()
t3 = pd.DataFrame(dict(nll_mean=fm.mean(1), nll_sd=fm.std(1, ddof=1)))
res["table3_nll"] = t3.round(4).to_dict("index")

# ---- per comparison
rows = []
cubes = {}
for A, B in PAIRS:
    c = ra.paired_cube(g, A, B)
    assert c["families"] == FAM, c["families"]
    D = c["D3"].mean(2)                        # m x F, averaged over severities
    cubes[(A, B)] = (c, D)
    tw = ra.two_way(D, n_gpq=2_000_000, seed=ra.SEED)
    m, F = D.shape
    fam = D.mean(0)
    se_img = tw["se_image"]; z = tw["mean"] / se_img
    p_img = 2 * stats.norm.sf(abs(z))
    s_f = fam.std(ddof=1); t = tw["mean"] / (s_f / math.sqrt(F))
    p_fam = 2 * stats.t.sf(abs(t), F - 1)
    bt = ra.image_bootstrap(D, B=2000, seed=ra.SEED)
    rows.append(dict(comparison=f"{A} vs {B}", A=A, B=B,
                     **{f"d_{f}": fam[i] for i, f in enumerate(FAM)},
                     mean=tw["mean"], se_image=se_img, z_image=z, p_image=p_img,
                     ci_image_z=tw["ci_image"], ci_boot=bt["ci_boot"],
                     se_family=tw["se_family"], ci_family=tw["ci_family"], p_family=p_fam,
                     d_family=tw["mean"] / s_f,
                     sigma_a_2c=tw["sigma_a_2c"], sigma_e_2c=tw["sigma_e_2c"], rho_2c=tw["rho_2c"],
                     rho_2c_lo=tw["rho_2c_lo"], rho_2c_hi=tw["rho_2c_hi"],
                     se_ratio=tw["se_ratio"], se_ratio_lo=tw["se_ratio_lo"], se_ratio_hi=tw["se_ratio_hi"],
                     rho_family=tw["rho_family"], rho_family_lo=tw["rho_family_lo"], rho_family_hi=tw["rho_family_hi"],
                     rho_image=tw["rho_image"], sigma_a=tw["sigma_a"], sigma_b=tw["sigma_b"], sigma_e=tw["sigma_e"],
                     MS_A=tw["MS_A"], MS_B=tw["MS_B"], MS_E=tw["MS_E"],
                     F_family=tw["F_family"], p_F_family=tw["p_F_family"],
                     full_over_family=tw["full_over_family"]))
R = pd.DataFrame(rows)

# Holm over the twelve image-level p-values
order = np.argsort(R.p_image.values); k = len(R)
holm = np.empty(k); run_max = 0
for rank, i in enumerate(order):
    run_max = max(run_max, (k - rank) * R.p_image.values[i]); holm[i] = min(1.0, run_max)
R["p_image_holm"] = holm
R["sig_image"] = R.p_image < 0.05
R["sig_image_holm"] = R.p_image_holm < 0.05
R["sig_family"] = R.p_family < 0.05
R.to_csv(f"{out}/comparisons_rerun.csv", index=False)

# ---- vignetting dominance
dcols = [f"d_{f}" for f in FAM]
vig = R["d_vignetting"]
res["vignetting_range"] = [float(vig.min()), float(vig.max())]
res["vignetting_is_max_in_all"] = bool((R[dcols].idxmax(axis=1) == "d_vignetting").all())
res["n_vignetting_only_positive"] = int(((R[dcols] > 0).sum(1).eq(1) & (vig > 0)).sum())
res["only_positive_list"] = R.loc[((R[dcols] > 0).sum(1).eq(1) & (vig > 0)), "comparison"].tolist()
res["n_positive_families"] = dict(zip(R.comparison, (R[dcols] > 0).sum(1).astype(int)))
res["n_mean_positive"] = int((R["mean"] > 0).sum())
res["other_families_range"] = [float(R[[c for c in dcols if c != "d_vignetting"]].min().min()),
                               float(R[[c for c in dcols if c != "d_vignetting"]].max().max())]

# ---- summary for text
res["n_sig_image"] = int(R.sig_image.sum())
res["n_sig_image_against_arm"] = int((R.sig_image & (R["mean"] > 0)).sum())
res["n_sig_image_for_arm"] = int((R.sig_image & (R["mean"] < 0)).sum())
res["n_sig_image_holm"] = int(R.sig_image_holm.sum())
res["max_p_image_among_sig"] = float(R.loc[R.sig_image, "p_image"].max())
res["max_p_holm_among_sig"] = float(R.loc[R.sig_image, "p_image_holm"].max())
res["n_sig_family"] = int(R.sig_family.sum())
res["min_p_family"] = float(R.p_family.min())
res["rho_2c_range"] = [float(R.rho_2c.min()), float(R.rho_2c.max())]
res["rho_2c_median"] = float(R.rho_2c.median())
res["rho_2c_lo_range"] = [float(R.rho_2c_lo.min()), float(R.rho_2c_lo.max())]
res["se_ratio_range"] = [float(R.se_ratio.min()), float(R.se_ratio.max())]
res["se_ratio_median"] = float(R.se_ratio.median())
res["se_ratio_ci_factor"] = float((R.se_ratio_hi / R.se_ratio_lo).median())
res["se_ratio_lo_range"] = [float(R.se_ratio_lo.min()), float(R.se_ratio_lo.max())]
res["rho_family_range"] = [float(R.rho_family.min()), float(R.rho_family.max())]
res["rho_family_median"] = float(R.rho_family.median())
res["rho_family_lo_range"] = [float(R.rho_family_lo.min()), float(R.rho_family_lo.max())]
res["rho_family_width_range"] = [float((R.rho_family_hi - R.rho_family_lo).min()), float((R.rho_family_hi - R.rho_family_lo).max())]
res["F_range"] = [float(R.F_family.min()), float(R.F_family.max())]
res["max_p_F"] = float(R.p_F_family.max())
res["crossed_over_2c"] = dict(zip(R.comparison, (R.rho_family / R.rho_2c).round(3)))
res["crossed_over_2c_range"] = [float((R.rho_family / R.rho_2c).min()), float((R.rho_family / R.rho_2c).max())]
res["n_MSB_below_MSE"] = int((R.MS_B < R.MS_E).sum())
res["MSB_below_MSE"] = R.loc[R.MS_B < R.MS_E, "comparison"].tolist()
res["n_crossed_below_2c"] = int((R.rho_family < R.rho_2c).sum())
res["crossed_below_2c"] = R.loc[R.rho_family < R.rho_2c, "comparison"].tolist()
res["rho_image_range"] = [float(R.rho_image.min()), float(R.rho_image.max())]
res["full_over_family_max"] = float(R.full_over_family.max())
# width ratio family t-interval / image bootstrap percentile interval (as in the notebook)
wf = R.ci_family.apply(lambda c: c[1] - c[0]); wb = R.ci_boot.apply(lambda c: c[1] - c[0])
res["width_ratio_boot"] = [float((wf / wb).min()), float((wf / wb).median()), float((wf / wb).max())]
wz = R.ci_image_z.apply(lambda c: c[1] - c[0])
res["width_ratio_z"] = [float((wf / wz).min()), float((wf / wz).median()), float((wf / wz).max())]

# ---- power at the per-family effect size (one-sample t, two-sided 0.05)
def power(d, n, alpha=0.05):
    df_ = n - 1; nc = d * math.sqrt(n); tc = stats.t.ppf(1 - alpha / 2, df_)
    return float(stats.nct.sf(tc, df_, nc) + stats.nct.cdf(-tc, df_, nc))
def n80(d):
    n = 3
    while power(d, n) < 0.8: n += 1
    return n
dq = abs(float(R.loc[R.comparison == "C7q vs C5", "d_family"].iloc[0]))
res["d_C7q_C5"] = dq
res["power_at"] = {n: power(dq, n) for n in (6, 12, 20, 30, 50, 100)}
res["n80_d"] = n80(dq)
res["abs_d_all"] = dict(zip(R.comparison, R.d_family.abs().round(3)))
res["abs_d_median"] = float(R.d_family.abs().median())
res["power_median_d_6"] = power(res["abs_d_median"], 6)
res["n80_median_d"] = n80(res["abs_d_median"])
# 95% CI for d (noncentral t inversion) for C7q vs C5
tobs = dq * math.sqrt(6)
from scipy.optimize import brentq
lo = brentq(lambda nc: stats.nct.sf(tobs, 5, nc) - 0.025, -20, 20)
hi = brentq(lambda nc: stats.nct.cdf(tobs, 5, nc) - 0.025, -20, 20)
res["d_ci"] = [lo / math.sqrt(6), hi / math.sqrt(6)]

# ---- Fig 4 extrapolation at the median two-component rho
rho_med = res["rho_2c_median"]
sr = lambda rho, m: math.sqrt(1 + m * rho / (1 - rho))
res["se_ratio_at_median_rho"] = {m: sr(rho_med, m) for m in (50, 900, 1344, 50000)}
res["se_ratio_band"] = {m: [sr(res["rho_2c_range"][0], m), sr(res["rho_2c_range"][1], m)] for m in (50, 900, 50000)}

# ---- vignetting mechanism: accuracy and NLL split by correctness (C2 vs quality arms)
v = test[test.family == "vignetting"]
acc = v[v.arm == "C2"].groupby("severity").correct.mean()
clean_acc = g[(g.family == "clean") & (g.arm == "C2")].correct.mean()
res["vignetting_acc_by_sev"] = acc.round(4).to_dict()
res["clean_acc"] = float(clean_acc)
mech = {}
for arm in ["C2", "C5", "C4", "C7q", "C7", "C6c"]:
    s = v[v.arm == arm]
    mech[arm] = dict(nll_correct=float(s[s.correct == 1].nll.mean()), nll_wrong=float(s[s.correct == 0].nll.mean()),
                     nll_all=float(s.nll.mean()))
res["vignetting_nll_by_correct"] = mech
# per fold vignetting NLL for C2 and C7q
res["vignetting_fold_nll"] = {arm: v[v.arm == arm].groupby("fold").nll.mean().round(3).to_dict() for arm in ["C2", "C5", "C7q", "C4", "C6c"]}
res["vignetting_fold_acc"] = v[v.arm == "C2"].groupby("fold").correct.mean().round(3).to_dict()
# accuracy loss per family at severity 5 (clean minus corrupted)
res["acc_loss_sev5"] = {f: float(clean_acc - test[(test.arm == "C2") & (test.family == f) & (test.severity == 5)].correct.mean()) for f in FAM}

# ---- all arms vs C2 for the Table 3 verdict column
verd = {}
for A in ["C1", "C3", "C4", "C5", "C5o", "C6c", "C7", "C7q", "C8", "C8b"]:
    c = ra.paired_cube(g, A, "C2"); D = c["D3"].mean(2)
    tw = ra.two_way(D, n_gpq=0)
    bt = ra.image_bootstrap(D, B=2000, seed=ra.SEED)
    lo_i, hi_i = bt["ci_boot"]; lo_f, hi_f = tw["ci_family"]
    verd[A] = dict(mean=tw["mean"], ci_boot=bt["ci_boot"], ci_family=tw["ci_family"],
                   image=("better" if hi_i < 0 else "worse" if lo_i > 0 else "n.s."),
                   family=("better" if hi_f < 0 else "worse" if lo_f > 0 else "n.s."))
res["vs_C2_all_arms"] = verd
# C5o vs C5 and arms vs C5o
for A, B in [("C5o", "C5"), ("C7q", "C5o"), ("C4", "C5o")]:
    c = ra.paired_cube(g, A, B); D = c["D3"].mean(2); tw = ra.two_way(D, n_gpq=0)
    bt = ra.image_bootstrap(D, B=2000, seed=ra.SEED)
    res[f"{A}_vs_{B}"] = dict(mean=tw["mean"], ci_boot=bt["ci_boot"], ci_family=tw["ci_family"])

json.dump(res, open(f"{out}/ms_numbers.json", "w"), indent=1, default=lambda o: o if not isinstance(o, (np.floating, np.integer)) else o.item())
pd.set_option("display.width", 250); pd.set_option("display.max_columns", 60)
print(t3.round(4))
print(R[["comparison"] + dcols + ["mean", "p_image", "p_image_holm", "p_family", "d_family"]].round(4).to_string())
print(R[["comparison", "sigma_a_2c", "sigma_e_2c", "rho_2c", "rho_2c_lo", "rho_2c_hi", "se_ratio", "se_ratio_lo", "se_ratio_hi",
         "rho_family", "rho_family_lo", "rho_family_hi", "rho_image", "F_family", "p_F_family", "MS_B", "MS_E"]].round(4).to_string())
print(json.dumps({k: v for k, v in res.items() if k not in ("table3_nll",)}, indent=1, default=str))
