"""Compare two runs of the re-run notebook (Section 5.1 of the paper).

Usage:
    python3 -I analysis/compare_runs.py RUN1_PER_IMAGE RUN2_PER_IMAGE RUN1_SUMMARY RUN2_SUMMARY

RUN*_PER_IMAGE are per-image tables (per_image_nll_G1.csv.gz) and RUN*_SUMMARY the summary.csv
files written by the revision analyses. The script prints how far the second run moves the
per-image values, the mean NLL of each arm (Table 3) and the comparison-level quantities of
Table 5 (mean difference, standard-error ratio, two-component rho, crossed rho_family and their
lower bounds).
"""
import sys

import pandas as pd

KEY = ["dataset", "backbone", "run", "fold", "image_id", "family", "severity", "arm"]


def arm_means(d):
    """Table 3 style: mean NLL over the held-out conditions in each fold, then mean over folds."""
    d = d[d["family"] != "clean"]
    per_fold = d.groupby(["arm", "fold"])["nll"].mean().unstack()
    return per_fold.mean(axis=1)


def main(run1, run2, sum1, sum2):
    a = pd.read_csv(run1)
    b = pd.read_csv(run2)
    m = a.merge(b, on=KEY, how="outer", suffixes=("_1", "_2"), indicator=True)
    unmatched = int((m["_merge"] != "both").sum())
    m = m[m["_merge"] == "both"]
    dn = (m["nll_2"] - m["nll_1"]).abs()
    flips = m[m["correct_1"] != m["correct_2"]][["fold", "image_id", "family", "severity"]].drop_duplicates()
    n_pairs = a[["image_id", "family", "severity"]].drop_duplicates().shape[0]
    print("Per-image values")
    print(f"  rows: {len(a)} and {len(b)}, unmatched: {unmatched}")
    print(f"  rows whose NLL differs by more than 1e-6: {int((dn > 1e-6).sum())} ({(dn > 1e-6).mean():.1%})")
    print(f"  mean |difference in NLL|: {dn.mean():.4f}, largest: {dn.max():.2f}")
    print(f"  image-condition pairs whose predicted class changed: {len(flips)} of {n_pairs}")
    for _, r in flips.iterrows():
        print(f"    fold {r.fold}, image {r.image_id}, {r.family}, severity {r.severity}")

    t1, t2 = arm_means(a), arm_means(b)
    t = pd.DataFrame({"run1": t1, "run2": t2})
    t["difference"] = t["run2"] - t["run1"]
    print("\nMean NLL of each arm under the held-out families (Table 3)")
    print(t.round(4).to_string())

    s1 = pd.read_csv(sum1)
    s2 = pd.read_csv(sum2)
    k = ["dataset", "backbone", "run", "comparison", "light"]
    s = s1.merge(s2, on=k, suffixes=("_1", "_2"))
    s = s[(s["run"] == "G1") & (~s["light"].astype(bool))]
    print(f"\nComparison-level quantities, grid G1, {len(s)} comparisons (largest absolute change)")
    for c in ["mean", "se_ratio", "se_ratio_lo", "t5_rho", "t5_rho_lo", "rho_family", "rho_family_lo"]:
        d = (s[c + "_2"] - s[c + "_1"]).abs()
        print(f"  {c:14s} {d.max():.4f}")


if __name__ == "__main__":
    if len(sys.argv) != 5:
        sys.exit(__doc__)
    main(*sys.argv[1:5])
