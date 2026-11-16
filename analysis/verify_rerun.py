"""Independent check of the Colab run and the extra numbers the response needs.

Reads the ten per-image tables from the user's zip, recomputes with revision_analyses.py, and
compares with the notebook's summary.csv and split_variability.csv; then computes the
published-versus-rerun comparison, training-variability shares, a corrected amplitude-matched
analysis (no clean anchor, explicit targets) and the oracle contrast C5o vs C5."""
import sys, math
sys.path.insert(0, "/home/claude/revision")
import numpy as np, pandas as pd
from scipy import stats
import revision_analyses as ra

Z = "/home/claude/colab_run/zip"
OUT = sys.argv[1]
pd.set_option("display.width", 250); pd.set_option("display.max_columns", 40)
runs = ["G1"] + [f"G1-split{r}" for r in range(1, 10)]
df = ra.load_long([f"{Z}/per_image_nll_{r}.csv.gz" for r in runs])
MAIN = [(a, b) for b in ("C2", "C5") for a in ("C4", "C6c", "C7", "C7q", "C8", "C8b")]
ORAC = [(a, "C5o") for a in ("C4", "C6c", "C7", "C7q", "C8", "C8b")]
groups = {r: g for (_, _, r), g in df.groupby(["dataset", "backbone", "run"], sort=False)}

# 1. recompute two_way for every run and pair; compare G1 with the notebook summary
rows, cubes = [], {}
for r in runs:
    for A, B in MAIN + ORAC:
        cube = ra.paired_cube(groups[r], A, B)
        D = cube["D3"].mean(2)
        tw = ra.two_way(D, n_gpq=0)
        rows.append(dict(run=r, comparison=f"{A} vs {B}", mean=tw["mean"], se_family=tw["se_family"],
                         se_image=tw["se_image"], se_ratio=tw["se_ratio"], se_lo=tw["se_ratio_lo"],
                         sigma_a=tw["sigma_a"], sigma_b=tw["sigma_b"], sigma_e=tw["sigma_e"], rho=tw["rho_family"],
                         t5_sa=tw["sigma_a_2c"], t5_se=tw["sigma_e_2c"], t5_rho=tw["rho_2c"], p_F=tw["p_F_family"],
                         ci_fam_lo=tw["ci_family"][0], ci_fam_hi=tw["ci_family"][1]))
        if r == "G1":
            cubes[(A, B)] = cube
R = pd.DataFrame(rows)
S = pd.read_csv(f"{Z}/results/summary.csv")
m = R.merge(S, on=["run", "comparison"], suffixes=("", "_nb"))
cols = ["mean", "se_family", "se_image", "se_ratio", "sigma_a", "sigma_b", "sigma_e"]
dif = max(float((m[c] - m[c + "_nb"]).abs().max()) for c in cols)
print(f"1. recomputation vs notebook summary: {len(m)} rows matched, largest absolute difference {dif:.2e}")

# 2. split variability recomputed
SV = pd.read_csv(f"{Z}/results/split_variability.csv")
sd = R.groupby("comparison").agg(sd=("mean", lambda x: x.std(ddof=1)), se_i=("se_image", "mean"),
                                  se_f=("se_family", "mean"), mean_all=("mean", "mean"),
                                  r_min=("se_ratio", "min"), r_max=("se_ratio", "max")).reset_index()
chk = sd.merge(SV, on="comparison")
print(f"2. split SD vs notebook: largest difference {float((chk['sd'] - chk['sd_across_splits']).abs().max()):.2e}")
sd["family_share"] = sd.se_f ** 2 / (sd.se_f ** 2 + sd.sd ** 2)
sd["fam_over_img_train"] = sd.se_f / np.sqrt(sd.se_i ** 2 + sd.sd ** 2)
sd["full_over_family"] = np.sqrt(sd.se_f ** 2 + sd.sd ** 2 + sd.se_i ** 2) / sd.se_f
sd["full_over_image"] = np.sqrt(sd.se_f ** 2 + sd.sd ** 2 + sd.se_i ** 2) / sd.se_i
sd["train_var_mult"] = 1 + (sd.sd / sd.se_i) ** 2
sd["sd_over_se_i"] = sd.sd / sd.se_i
sd["sd_over_se_f"] = sd.sd / sd.se_f
main_names = [f"{a} vs {b}" for a, b in MAIN]
SDm = sd[sd.comparison.isin(main_names)]
print("\n2b. training variability (10 partitions), 12 main comparisons")
print(SDm[["comparison", "mean_all", "sd", "se_i", "se_f", "sd_over_se_i", "sd_over_se_f", "family_share",
           "fam_over_img_train", "full_over_family", "full_over_image", "train_var_mult"]].round(4).to_string(index=False))
for c in ["sd", "sd_over_se_i", "sd_over_se_f", "family_share", "fam_over_img_train", "full_over_family", "full_over_image", "train_var_mult"]:
    print(f"   {c:20s} range {SDm[c].min():.4f} to {SDm[c].max():.4f}")
print("   oracle comparisons:", sd[~sd.comparison.isin(main_names)][["comparison", "sd_over_se_i", "sd_over_se_f", "family_share"]].round(3).to_dict("records"))

# 3. published (submitted) versus rerun G1
PUB_D = {"C4 vs C2": 0.0091, "C4 vs C5": -0.0745, "C6c vs C2": 0.2511, "C6c vs C5": 0.1675, "C7 vs C2": 0.0897,
         "C7 vs C5": 0.0061, "C7q vs C2": -0.0164, "C7q vs C5": -0.0999, "C8 vs C2": 0.1655, "C8 vs C5": 0.0819,
         "C8b vs C2": 0.0420, "C8b vs C5": -0.0416}
PUB_IMG = {"C4 vs C2": (-0.0096, 0.0289), "C4 vs C5": (-0.1012, -0.0489), "C6c vs C2": (0.2137, 0.2887),
           "C6c vs C5": (0.1321, 0.2023), "C7 vs C2": (0.0703, 0.1097), "C7 vs C5": (-0.0235, 0.0354),
           "C7q vs C2": (-0.0278, -0.0049), "C7q vs C5": (-0.1263, -0.0739), "C8 vs C2": (0.1181, 0.2149),
           "C8 vs C5": (0.0574, 0.1079), "C8b vs C2": (0.0162, 0.0685), "C8b vs C5": (-0.0525, -0.0308)}
PUB_T5 = {"C8 vs C2": (.313, 1.815, .029, 5.28), "C8b vs C2": (.178, .981, .032, 5.55), "C8 vs C5": (.211, .947, .047, 6.74),
          "C7q vs C5": (.233, .984, .053, 7.17), "C4 vs C2": (.208, .721, .077, 8.72), "C4 vs C5": (.286, .980, .079, 8.84),
          "C8b vs C5": (.119, .406, .079, 8.84), "C7q vs C2": (.148, .428, .106, 10.38), "C7 vs C5": (.503, 1.103, .172, 13.71),
          "C6c vs C2": (.811, 1.405, .250, 17.35), "C7 vs C2": (.430, .738, .253, 17.49), "C6c vs C5": (.872, 1.315, .305, 19.90)}
G1 = R[R.run == "G1"].set_index("comparison")
bt = {}
cmp_rows = []
for c in main_names:
    A, B = c.split(" vs ")
    b = ra.image_bootstrap(cubes[(A, B)]["D3"].mean(2), B=2000)
    lo, hi = b["ci_boot"]
    srow = SDm.set_index("comparison").loc[c]
    p = PUB_T5[c]
    cmp_rows.append(dict(comparison=c, pub_mean=PUB_D[c], rerun_mean=G1.loc[c, "mean"],
                         diff=G1.loc[c, "mean"] - PUB_D[c], diff_in_split_sd=(G1.loc[c, "mean"] - PUB_D[c]) / srow["sd"],
                         pub_img_sig=("win" if PUB_IMG[c][1] < 0 else "loss" if PUB_IMG[c][0] > 0 else "ns"),
                         rerun_img_ci=f"[{lo:.4f}, {hi:.4f}]",
                         rerun_img_sig=("win" if hi < 0 else "loss" if lo > 0 else "ns"),
                         rerun_fam_ci=f"[{G1.loc[c, 'ci_fam_lo']:.3f}, {G1.loc[c, 'ci_fam_hi']:.3f}]",
                         pub_sa=p[0], rerun_sa=G1.loc[c, "t5_sa"], pub_se=p[1], rerun_se=G1.loc[c, "t5_se"],
                         pub_rho=p[2], rerun_rho=G1.loc[c, "t5_rho"], pub_ratio=p[3], rerun_ratio=G1.loc[c, "se_ratio"],
                         rerun_ratio_lo=G1.loc[c, "se_lo"]))
C = pd.DataFrame(cmp_rows)
print("\n3. submitted versus rerun (G1)")
print(C.round(4).to_string(index=False))
print(f"   |diff| / split SD: median {C.diff_in_split_sd.abs().median():.2f}, max {C.diff_in_split_sd.abs().max():.2f}")
print(f"   rerun SE ratio range {C.rerun_ratio.min():.2f} to {C.rerun_ratio.max():.2f}; lower limits {C.rerun_ratio_lo.min():.2f} to {C.rerun_ratio_lo.max():.2f}")
print(f"   submitted image-level 'wins': {list(C[C.pub_img_sig == 'win'].comparison)}; rerun wins: {list(C[C.rerun_img_sig == 'win'].comparison)}")
print(f"   rerun image-level significant (either sign): {int((C.rerun_img_sig != 'ns').sum())} of 12; family-level CIs containing 0: "
      f"{int(((G1.loc[main_names, 'ci_fam_lo'] < 0) & (G1.loc[main_names, 'ci_fam_hi'] > 0)).sum())} of 12")

# 4. per-family deltas of the rerun (a full Table 4)
fams = cubes[MAIN[0]]["families"]
T4 = pd.DataFrame({c: cubes[tuple(c.split(" vs "))]["D3"].mean(2).mean(0) for c in main_names}, index=fams).T
print("\n4. rerun per-family mean differences (A minus B)"); print(T4.round(3).to_string())

# 5. oracle: C5o vs C5 and the quality arms against C5o
cube = ra.paired_cube(groups["G1"], "C5o", "C5"); D = cube["D3"].mean(2)
tw = ra.two_way(D, n_gpq=0); b = ra.image_bootstrap(D, B=2000)
print(f"\n5. C5o vs C5: mean {tw['mean']:.4f}, image CI [{b['ci_boot'][0]:.4f}, {b['ci_boot'][1]:.4f}], "
      f"family CI [{tw['ci_family'][0]:.3f}, {tw['ci_family'][1]:.3f}], per-family {np.round(D.mean(0), 3).tolist()}")
for A, B in ORAC:
    cb = cubes[(A, B)]; Dq = cb["D3"].mean(2); twq = ra.two_way(Dq, n_gpq=0); bq = ra.image_bootstrap(Dq, B=2000)
    print(f"   {A} vs C5o: mean {twq['mean']:+.4f}, image CI [{bq['ci_boot'][0]:+.4f}, {bq['ci_boot'][1]:+.4f}], "
          f"family CI [{twq['ci_family'][0]:+.3f}, {twq['ci_family'][1]:+.3f}]")

# 6. corrected amplitude matching: no clean anchor, explicit targets, families that reach them
acc = cubes[MAIN[0]]["acc"]; acc_clean = cubes[MAIN[0]]["acc_clean"]
loss = acc_clean - acc
print("\n6. accuracy loss ladders (clean minus corrupted):")
print(pd.DataFrame(loss, index=fams, columns=cubes[MAIN[0]]["severities"]).round(3).to_string())
targets = [0.05, 0.10, 0.20, 0.30, 0.40]
am_rows = []
for c in main_names:
    A, B = c.split(" vs "); cb = cubes[(A, B)]
    am, _ = ra.amplitude_matched(cb["D3"], cb["acc"], fams, cb["severities"], targets=targets, D_clean=None,
                                 acc_clean=cb["acc_clean"], method="interp", n_gpq=20000)
    am["comparison"] = c; am_rows.append(am)
    # unmatched reference on the four families that reach every target from 0.10 up
    four = [fams.index(f) for f in ("motion_blur", "shot_noise", "vibration_jitter", "vignetting")]
    tw4 = ra.two_way(cb["D3"][:, four, :].mean(2), n_gpq=20000)
    am_rows.append(pd.DataFrame([dict(comparison=c, target_loss="unmatched 4 families", n_families=4,
                                      sigma_a=tw4["sigma_a"], rho_family=tw4["rho_family"], rho_family_lo=tw4["rho_family_lo"],
                                      rho_family_hi=tw4["rho_family_hi"], se_ratio=tw4["se_ratio"], se_ratio_lo=tw4["se_ratio_lo"],
                                      p_F_family=tw4["p_F_family"])]))
AM = pd.concat(am_rows, ignore_index=True)
print("\n   families used per target:", AM[AM.comparison == "C4 vs C2"][["target_loss", "n_families", "families"]].to_string(index=False))
for col in ["sigma_a", "rho_family", "se_ratio", "se_ratio_lo", "p_F_family"]:
    print(f"\n   {col}"); print(AM.pivot_table(index="comparison", columns="target_loss", values=col, aggfunc="first").round(4).to_string())
AM.to_csv(f"{OUT}/amplitude_matched_corrected.csv", index=False)
C.to_csv(f"{OUT}/submitted_vs_rerun.csv", index=False)
SDm.to_csv(f"{OUT}/training_variability.csv", index=False)
T4.to_csv(f"{OUT}/per_family_deltas_rerun.csv")
