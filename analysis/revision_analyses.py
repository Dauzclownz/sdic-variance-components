#!/usr/bin/env python3
"""Per-image analyses for the PAA revision of the SDIC manuscript.

Each function answers a reviewer point and runs on the per-image NLL table that the
notebooks already compute but do not save (run `--export-help` for the lines to add).

    python revision_analyses.py per_image_nll_G1.csv.gz per_image_nll_G2.csv.gz --out results
    python revision_analyses.py --selftest      # checks every method on simulated data

Model (manuscript Eq. 1): d_if = mu + a_f + b_i + e_if, where d_if is the paired per-image
NLL difference (arm A minus arm B) for image i under test family f, averaged over the
severity levels, exactly as paired_matrix() builds it. m images, F families.

    MS_A = m sum_f (dbar_.f - dbar)^2 / (F-1)                     E[MS_A] = s_e^2 + m s_a^2
    MS_B = F sum_i (dbar_i. - dbar)^2 / (m-1)                     E[MS_B] = s_e^2 + F s_b^2
    MS_E = sum (d_if - dbar_i. - dbar_.f + dbar)^2 / ((m-1)(F-1))  E[MS_E] = s_e^2

    SE_family^2 = MS_A/(mF)   t interval over the F family means
    SE_image^2  = MS_B/(mF)   analytic counterpart of the image bootstrap
    SE ratio R  = sqrt(MS_A/MS_B), and R^2 (s_e^2 + F s_b^2)/(s_e^2 + m s_a^2) ~ F(F-1, m-1)
    variance of the grand mean over all three sources:
        s_a^2/F + s_b^2/m + s_e^2/(mF), estimated by (MS_A + MS_B - MS_E)/(mF)

Function             what it gives                                         review point
two_way              components, exact F test, exact CI for the SE ratio,   R2.2 R2.5 R3.1
                     generalized CI for crossed rho_family, full crossed SE
table5_row           the two-component quantities printed in Table 5        R2.1
perm_test            within-image permutation test of Section 6.5           R2.3 R3.2
hotelling_rm         Hotelling T^2 for repeated measures (any covariance)   R2.3 R3.2
wts_perm_test        studentized permutation test, Friedrich et al. (2017)  R2.3 R3.2
lofo                 leave-one-family-out, with SE ratios                   R2.6
fold_clustered       effect of shared fold models on the image-level SE     R2.6 R3.5
split_variability    movement of the mean over repeated fold partitions     R2.6 R3.5
per_severity         components at each severity level                      R1.3 R3.4
amplitude_matched    components with families matched on probe accuracy     R3.4

Input: one row per (image, test family, severity, arm); CSV, CSV.GZ or Parquet; columns
    dataset, backbone, run, fold, image_id, family, severity, arm, nll [, correct]
`run` separates calibration grids or seeds ("G1" = Phase 0.11, "G2" = Phases 1 to 4).
`arm` may be the long notebook name; only its first word is used ("C4 linear / raw q" -> C4).
`correct` (0/1: probe prediction correct) is needed only for amplitude matching. Rows with
family == "clean" and severity == 0 are optional; when present they anchor the amplitude
interpolation at zero damage.

References
    Bates S, Hastie T, Tibshirani R (2024) Cross-validation: what does it estimate and how well
        does it do it? J Am Stat Assoc 119(546):1434-1445
    Burdick RK, Borror CM, Montgomery DC (2005) Design and Analysis of Gauge R&R Studies:
        Making Decisions with Confidence Intervals in Random and Mixed ANOVA Models. SIAM
    Chung E, Romano JP (2013) Exact and asymptotically robust permutation tests.
        Ann Stat 41(2):484-507
    Friedrich S, Brunner E, Pauly M (2017) Permuting longitudinal data in spite of the
        dependencies. J Multivar Anal 153:255-265
"""
from __future__ import annotations

import argparse
import math
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

ALPHA = 0.05
SEED = 20261101
TREATMENTS = ["C4", "C6c", "C7", "C7q", "C8", "C8b"]
BASELINES = ["C2", "C5"]
REQUIRED = ["dataset", "backbone", "run", "fold", "image_id", "family", "severity", "arm", "nll"]

EXPORT_HELP = r'''
WHAT TO SAVE FROM THE NOTEBOOKS (one long table per grid; adapt variable names if needed)

1. Grid G1, PHASE0_11_family_uncertainty.ipynb (source of Tables 3 to 5).
   Easiest: run PHASE0_11_family_uncertainty_revision.ipynb, which saves these tables, adds
   the oracle arm and the fold partitions, and runs every analysis of this script itself.
   By hand: add this cell at the end of the original notebook, after section 5.

    import pandas as pd
    n = [len(f) for f in FOLDS]
    fold = np.concatenate([np.full(len(SEVERITIES) * nk, k) for k, nk in enumerate(n)])
    sev = np.concatenate([np.repeat(np.asarray(SEVERITIES), nk) for nk in n])
    rows = [pd.DataFrame(dict(dataset="NEU-CLS", backbone=BACKBONE, run="G1", fold=fold,
                              image_id=d["im"], family=fam, severity=sev, arm=arm.split()[0],
                              nll=d["nll"], correct=(d["p"].argmax(1) == d["y"]).astype("int8")))
            for (arm, fam), d in POOLF.items()]
    pd.concat(rows).to_csv(OUT / "per_image_nll_G1.csv.gz", index=False)

   The section 3 loop concatenates the five folds in POOLF, each fold severity-major, which
   is what `fold` and `sev` reproduce. `correct` uses the calibrated argmax, which equals the
   probe's argmax because every arm rescales the logits by a positive temperature; this
   script checks that it is the same for every arm and warns if not.

   Oracle-class arm (R2.6): in gather() add
        HO = np.zeros((len(L), NC), np.float32); HO[np.arange(len(L)), Y] = 1.0
   return it as ho=HO, and add to ARM_SPECS
        "C5o linear / true-class one-hot": ("scalar", LinearT, "ho"),
   The arm sees the true class at test time: an upper bound on what class information
   alone can do, not a deployable calibrator. Comparisons against it are added automatically.

2. Grid G2, paired_matrix() in PHASE4_crossed_effects / PHASE3_1 / PHASE1 / PHASE2_1.
   Define ROWS = [] before the fold loop, replace the loop over TEST_FAMILIES with

        for fi, fam in enumerate(TEST_FAMILIES):
            Lt, Qt, Ht, Yt = gather(te, [(fam, s) for s in SEVERITIES]); ft = {"q": Qt, "h": Ht}
            for nm, (mdl, f_) in arms.items():
                with torch.no_grad():
                    p = softmax(mdl(torch.as_tensor(Lt, dtype=torch.float32),
                                    torch.as_tensor(ft[f_], dtype=torch.float32)).numpy())
                ROWS.append(pd.DataFrame(dict(
                    dataset=DATASET, backbone=BACKBONE, run="G2", fold=k,
                    image_id=np.tile(te, len(SEVERITIES)), family=fam,
                    severity=np.repeat(SEVERITIES, len(te)), arm=nm, nll=nll_pi(p, Yt),
                    correct=(Lt.argmax(1) == Yt).astype("int8"))))

   and after the loop: pd.concat(ROWS).to_csv(OUT / "per_image_nll_G2_<backbone>.csv.gz", index=False)
   Rows are ordered severity-major within a fold, as in gather(): row j is severity
   SEVERITIES[j // len(te)] and image te[j % len(te)].

3. Repeated fold partitions (R3.5). Rerun the export with only the fold split changed,
   StratifiedKFold(5, shuffle=True, random_state=SEED + 1000 * r) for r = 0, 1, ..., 9;
   r = 0 reproduces the original split. Name the runs "G1-split0" ... "G1-split9", or keep the
   original as "G1" and name the others "G1-split1" ... "G1-split9" (same for G2). The script
   then reports how far each mean moves across partitions, next to the image-level and
   family-level SEs.
'''


# ----------------------------------------------------------------------------- data
def load_long(paths):
    frames = []
    for p in paths:
        p = str(p)
        frames.append(pd.read_parquet(p) if p.endswith(".parquet") else pd.read_csv(p))
    df = pd.concat(frames, ignore_index=True)
    missing = [c for c in REQUIRED if c not in df.columns]
    if missing:
        raise SystemExit(f"input is missing columns {missing}; run --export-help")
    df["arm"] = df["arm"].astype(str).str.split().str[0]
    for c in ("dataset", "backbone", "run", "family"):
        df[c] = df[c].astype(str)
    dup = df.duplicated(["dataset", "backbone", "run", "image_id", "family", "severity", "arm"])
    if dup.any():
        raise SystemExit(f"{int(dup.sum())} duplicated (image, family, severity, arm) rows")
    return df


def paired_cube(g, A, B):
    """Complete image x family x severity cube of nll[A] - nll[B] for one dataset/backbone/run."""
    arms = set(g["arm"].unique())
    if A not in arms or B not in arms:
        return None
    test = g[g["family"] != "clean"]
    fams = list(pd.unique(test["family"]))
    sevs = np.sort(test["severity"].unique())
    imgs = np.sort(test["image_id"].unique())
    a = test[test["arm"] == A].set_index(["image_id", "family", "severity"])["nll"]
    b = test[test["arm"] == B].set_index(["image_id", "family", "severity"])["nll"]
    full = pd.MultiIndex.from_product([imgs, fams, sevs], names=["image_id", "family", "severity"])
    d = (a - b).reindex(full)
    if d.isna().any():
        raise ValueError(f"{A} vs {B}: {int(d.isna().sum())} of {len(d)} image x family x severity "
                         "cells are missing; the crossed analysis needs the complete design")
    D3 = d.to_numpy().reshape(len(imgs), len(fams), len(sevs))

    nf = test.groupby("image_id")["fold"].nunique()
    if (nf > 1).any():
        raise ValueError("an image appears in more than one test fold")
    folds = test.groupby("image_id")["fold"].first().reindex(imgs).to_numpy()

    out = dict(D3=D3, families=fams, severities=sevs, images=imgs, folds=folds,
               D_clean=None, acc=None, acc_clean=None, warnings=[])
    clean = g[g["family"] == "clean"]
    if len(clean):
        ca = clean[clean["arm"] == A].set_index("image_id")["nll"].reindex(imgs)
        cb = clean[clean["arm"] == B].set_index("image_id")["nll"].reindex(imgs)
        if not (ca.isna().any() or cb.isna().any()):
            out["D_clean"] = (ca - cb).to_numpy()
    if "correct" in g.columns:
        sub = g[g["arm"].isin([A, B])]
        varies = sub.groupby(["image_id", "family", "severity"])["correct"].nunique()
        if (varies > 1).any():
            out["warnings"].append(f"'correct' differs between {A} and {B} in {int((varies > 1).sum())} "
                                   f"cells, so some arm changes predictions; accuracy is taken from {B}")
        cb_ = test[test["arm"] == B].set_index(["image_id", "family", "severity"])["correct"].reindex(full)
        if not cb_.isna().any():
            out["acc"] = cb_.to_numpy().reshape(len(imgs), len(fams), len(sevs)).mean(0)
        if len(clean) and "correct" in clean.columns:
            cc = clean[clean["arm"] == B].set_index("image_id")["correct"].reindex(imgs)
            if not cc.isna().any():
                out["acc_clean"] = float(cc.mean())
    return out


# ----------------------------------------------------------------------------- core
def mean_squares(D):
    D = np.asarray(D, float)
    m, F = D.shape
    gm = D.mean(); rm = D.mean(1); cm = D.mean(0)
    MSA = m * ((cm - gm) ** 2).sum() / (F - 1)
    MSB = F * ((rm - gm) ** 2).sum() / (m - 1)
    res = D - rm[:, None] - cm[None, :] + gm
    MSE = (res ** 2).sum() / ((m - 1) * (F - 1))
    return m, F, gm, MSA, MSB, MSE


def _satterthwaite(terms):
    """terms: list of (coefficient, mean square, df). Returns (value, df)."""
    v = sum(c * ms for c, ms, _ in terms)
    den = sum((c * ms) ** 2 / nu for c, ms, nu in terms)
    return v, (v ** 2 / den if den > 0 else float("inf"))


def two_way(D, alpha=ALPHA, n_gpq=20000, seed=SEED):
    """Crossed two-way random-effects analysis of a complete m x F matrix."""
    m, F, gm, MSA, MSB, MSE = mean_squares(D)
    nA, nB, nE = F - 1, m - 1, (m - 1) * (F - 1)
    s2a = max((MSA - MSE) / m, 0.0); s2b = max((MSB - MSE) / F, 0.0); s2e = MSE
    tot = s2a + s2b + s2e
    se_fam = math.sqrt(MSA / (m * F)); se_img = math.sqrt(MSB / (m * F))
    R = se_fam / se_img if se_img > 0 else float("inf")
    fq = lambda p, a, b: stats.f.ppf(p, a, b)
    r_lo = R / math.sqrt(fq(1 - alpha / 2, nA, nB)); r_hi = R / math.sqrt(fq(alpha / 2, nA, nB))
    FA = MSA / MSE
    lam_lo = max((FA / fq(1 - alpha / 2, nA, nE) - 1) / m, 0.0)
    lam_hi = max((FA / fq(alpha / 2, nA, nE) - 1) / m, 0.0)

    # two-component quantities (Table 5 definitions): s_e^2 = mF SE_image^2 = MS_B,
    # s_a^2 = var(family means) - s_e^2/m = (MS_A - MS_B)/m; the SE ratio maps one to one to rho
    s2a_2c = max((MSA - MSB) / m, 0.0); s2e_2c = MSB
    rho_2c = s2a_2c / (s2a_2c + s2e_2c) if s2a_2c + s2e_2c > 0 else 0.0
    g = lambda th: max(((th - 1) / m) / (1 + (th - 1) / m), 0.0)

    # variance of the grand mean over all three sources (truncated moment estimates)
    terms = []
    if MSA > MSE: terms.append((1.0, MSA, nA))
    if MSB > MSE: terms.append((1.0, MSB, nB))
    k = 1 - int(MSA > MSE) - int(MSB > MSE)
    if k: terms.append((float(k), MSE, nE))
    v_full, df_full = _satterthwaite(terms)
    se_full = math.sqrt(max(v_full, 0.0) / (m * F))
    t_full = stats.t.ppf(1 - alpha / 2, df_full) if np.isfinite(df_full) else stats.norm.ppf(1 - alpha / 2)
    t_fam = stats.t.ppf(1 - alpha / 2, nA); z = stats.norm.ppf(1 - alpha / 2)

    out = dict(m=m, F=F, mean=gm, MS_A=MSA, MS_B=MSB, MS_E=MSE,
               sigma_a=math.sqrt(s2a), sigma_b=math.sqrt(s2b), sigma_e=math.sqrt(s2e),
               rho_family=s2a / tot if tot > 0 else 0.0, rho_image=s2b / tot if tot > 0 else 0.0,
               F_family=FA, p_F_family=stats.f.sf(FA, nA, nE),
               var_ratio_a_e_lo=lam_lo, var_ratio_a_e_hi=lam_hi,
               se_family=se_fam, se_image=se_img, se_ratio=R, se_ratio_lo=r_lo, se_ratio_hi=r_hi,
               p_se_ratio=stats.f.sf(R ** 2, nA, nB),
               sigma_a_2c=math.sqrt(s2a_2c), sigma_e_2c=math.sqrt(s2e_2c), rho_2c=rho_2c,
               rho_2c_lo=g(r_lo ** 2), rho_2c_hi=g(r_hi ** 2),
               se_full=se_full, df_full=df_full, full_over_family=se_full / se_fam if se_fam > 0 else float("nan"),
               ci_family=(gm - t_fam * se_fam, gm + t_fam * se_fam),
               ci_image=(gm - z * se_img, gm + z * se_img),
               ci_full=(gm - t_full * se_full, gm + t_full * se_full))
    if n_gpq:
        rng = np.random.default_rng(seed)
        GE = nE * MSE / rng.chisquare(nE, n_gpq)
        GA = nA * MSA / rng.chisquare(nA, n_gpq)
        GB = nB * MSB / rng.chisquare(nB, n_gpq)
        ga = np.maximum((GA - GE) / m, 0.0); gb = np.maximum((GB - GE) / F, 0.0)
        rho = ga / (ga + gb + GE)
        out["rho_family_lo"], out["rho_family_hi"] = np.quantile(rho, [alpha / 2, 1 - alpha / 2])
    return out


def table5_row(tw):
    """The four quantities printed in Table 5, from a two_way() result."""
    return dict(sigma_a=tw["sigma_a_2c"], sigma_e=tw["sigma_e_2c"], rho=tw["rho_2c"],
                se_ratio=tw["se_ratio"], se_ratio_lo=tw["se_ratio_lo"], se_ratio_hi=tw["se_ratio_hi"])


def image_bootstrap(D, B=2000, alpha=ALPHA, seed=SEED):
    """Percentile bootstrap over images, as in the manuscript (families held fixed)."""
    r = np.asarray(D, float).mean(1); m = len(r)
    rng = np.random.default_rng(seed)
    means = np.empty(B)
    for s in range(0, B, 500):
        b = min(500, B - s)
        means[s:s + b] = r[rng.integers(0, m, (b, m))].mean(1)
    lo, hi = np.quantile(means, [alpha / 2, 1 - alpha / 2])
    return dict(se_boot=float(means.std(ddof=1)), ci_boot=(float(lo), float(hi)),
                se_from_width=float((hi - lo) / (2 * stats.norm.ppf(1 - alpha / 2))))


# ----------------------------------------------------------------------------- tests of the family effect
def _permuted(D, rng, b):
    m, F = D.shape
    idx = np.argsort(rng.random((b, m, F)), axis=2)
    return np.take_along_axis(np.broadcast_to(D, (b, m, F)), idx, axis=2)


def perm_test(D, n_perm=20000, seed=SEED, batch=500):
    """Section 6.5 test: variance of the family means, family labels permuted within images.

    Exact under H0: within each image, the joint law of (d_i1, ..., d_iF) is invariant under
    permutation of the family index (images independent). Family-specific variances violate
    this, which is why the studentized version below is also reported."""
    D = np.asarray(D, float)
    rng = np.random.default_rng(seed)
    obs = float(D.mean(0).var(ddof=1))
    null = np.empty(n_perm)
    for s in range(0, n_perm, batch):
        b = min(batch, n_perm - s)
        null[s:s + b] = _permuted(D, rng, b).mean(1).var(axis=1, ddof=1)
    med = float(np.median(null))
    return dict(stat=obs, null_median=med, ratio_to_median=obs / med if med > 0 else float("inf"),
                p=float((1 + np.sum(null >= obs)) / (n_perm + 1)), n_perm=n_perm)


def _contrast(F):
    return np.hstack([np.eye(F - 1), -np.ones((F - 1, 1))])


def _t2(P):
    """Hotelling T^2 for H0: equal family means, for a stack P of shape (b, m, F)."""
    b, m, F = P.shape
    Y = P @ _contrast(F).T
    yb = Y.mean(1)
    Yc = Y - yb[:, None, :]
    S = np.einsum("bmi,bmj->bij", Yc, Yc) / (m - 1)
    sol = np.linalg.solve(S, yb[..., None])[..., 0]
    return m * np.einsum("bi,bi->b", yb, sol)


def hotelling_rm(D):
    """Repeated-measures Hotelling T^2: equal family means, any within-image covariance
    (no sphericity, no equal variances). Exact under multivariate normality of the image
    vectors; the chi-square reference is its large-m (Wald-type statistic) limit."""
    D = np.asarray(D, float)
    m, F = D.shape
    T2 = float(_t2(D[None])[0])
    Fst = (m - F + 1) / ((m - 1) * (F - 1)) * T2
    return dict(T2=T2, F=Fst, df1=F - 1, df2=m - F + 1, p_F=float(stats.f.sf(Fst, F - 1, m - F + 1)),
                p_chi2=float(stats.chi2.sf(T2, F - 1)))


def wts_perm_test(D, n_perm=5000, seed=SEED, batch=250):
    """Studentized permutation test (Friedrich, Brunner and Pauly 2017): the Wald-type
    statistic recomputed, covariance included, on every within-image permutation. Exact when
    the within-image exchangeability of perm_test holds and asymptotically valid for equal
    family means under any covariance when it does not (Chung and Romano 2013)."""
    D = np.asarray(D, float)
    rng = np.random.default_rng(seed + 1)
    obs = float(_t2(D[None])[0])
    null = np.empty(n_perm)
    for s in range(0, n_perm, batch):
        b = min(batch, n_perm - s)
        null[s:s + b] = _t2(_permuted(D, rng, b))
    return dict(T2=obs, p=float((1 + np.sum(null >= obs)) / (n_perm + 1)), n_perm=n_perm)


# ----------------------------------------------------------------------------- sensitivity analyses
def lofo(D, families, alpha=ALPHA):
    """Leave one family out: family-level t test, image-level z test, SE ratio and F test."""
    D = np.asarray(D, float)
    rows = []
    for j in [None] + list(range(D.shape[1])):
        Dj = D if j is None else np.delete(D, j, axis=1)
        tw = two_way(Dj, alpha=alpha, n_gpq=0)
        t = stats.ttest_1samp(Dj.mean(0), 0.0)
        zi = tw["mean"] / tw["se_image"]
        rows.append(dict(omitted="none" if j is None else families[j], n_families=Dj.shape[1],
                         mean=tw["mean"], t_family=float(t.statistic), p_family=float(t.pvalue),
                         ci_family_lo=tw["ci_family"][0], ci_family_hi=tw["ci_family"][1],
                         p_image=float(2 * stats.norm.sf(abs(zi))),
                         se_ratio=tw["se_ratio"], se_ratio_lo=tw["se_ratio_lo"], se_ratio_hi=tw["se_ratio_hi"],
                         F_family=tw["F_family"], p_F_family=tw["p_F_family"]))
    return pd.DataFrame(rows)


def fold_clustered(D, folds, alpha=ALPHA, B=2000, seed=SEED):
    """Does sharing the probe and calibrators within a fold inflate the image-level SE?

    One-way ANOVA of the image means on fold gives the within-fold intraclass correlation and
    the design effect 1 + (n0 - 1) ICC; a cluster-robust SE and a two-stage bootstrap (folds,
    then images within folds) are reported as cross-checks. With five folds all three are
    rough; the upper confidence limit of the design effect is the conservative figure."""
    D = np.asarray(D, float)
    r = D.mean(1); m = len(r)
    ks = np.unique(folds); K = len(ks)
    groups = [r[folds == k] for k in ks]
    nk = np.array([len(x) for x in groups])
    gm = r.mean(); mk = np.array([x.mean() for x in groups])
    MSb = (nk * (mk - gm) ** 2).sum() / (K - 1)
    MSw = sum(((x - x.mean()) ** 2).sum() for x in groups) / (m - K)
    n0 = (m - (nk ** 2).sum() / m) / (K - 1)
    s2f = max((MSb - MSw) / n0, 0.0); icc = s2f / (s2f + MSw)
    Fo = MSb / MSw
    FL = Fo / stats.f.ppf(1 - alpha / 2, K - 1, m - K); FU = Fo / stats.f.ppf(alpha / 2, K - 1, m - K)
    icc_lo = max((FL - 1) / (FL + n0 - 1), 0.0); icc_hi = max((FU - 1) / (FU + n0 - 1), 0.0)
    se_iid = r.std(ddof=1) / math.sqrt(m)
    u = np.array([(x - gm).sum() for x in groups])
    se_cr = math.sqrt(K / (K - 1) * (u ** 2).sum()) / m
    rng = np.random.default_rng(seed + 2)
    bm = np.empty(B)
    for b in range(B):
        pick = rng.integers(0, K, K)
        bm[b] = np.concatenate([groups[c][rng.integers(0, nk[c], nk[c])] for c in pick]).mean()
    deff = 1 + (n0 - 1) * icc; deff_hi = 1 + (n0 - 1) * icc_hi
    s2f_hi = icc_hi * MSw / (1 - icc_hi) if icc_hi < 1 else float("inf")
    return dict(n_folds=K, images_per_fold=n0, icc_fold=icc, icc_fold_lo=icc_lo, icc_fold_hi=icc_hi,
                F_fold=Fo, p_fold=float(stats.f.sf(Fo, K - 1, m - K)),
                var_fold=s2f / K, var_fold_hi=s2f_hi / K,     # added to the variance of the grand mean
                design_effect=deff, design_effect_hi=deff_hi,
                se_image_iid=se_iid, se_image_deff=se_iid * math.sqrt(deff),
                se_image_deff_hi=se_iid * math.sqrt(deff_hi),
                se_image_cluster_robust=se_cr, se_image_two_stage=float(bm.std(ddof=1)))


def split_stem(run, tag):
    """'G1-split3' -> 'G1'; a run without the tag is its own stem."""
    return run.split(tag)[0] if tag and tag in run else run


def split_variability(rows, tag="-split"):
    """How far does each mean move when only the fold partition changes?

    Partitions of one grid are the runs '<grid><tag><k>' plus the base run '<grid>' (counted as
    partition 0 unless '<grid><tag>0' also exists, which would be the same split twice). The SD
    over partitions measures training-sample variability that the image-level interval ignores;
    it is a lower bound, because the partitions share most training images (Bates, Hastie and
    Tibshirani 2024)."""
    df = pd.DataFrame(rows)
    if df.empty or not tag:
        return None
    df["grid"] = [split_stem(r, tag) for r in df["run"]]
    tagged = df["run"].str.contains(tag, regex=False)
    stems = set(zip(df.loc[tagged, "dataset"], df.loc[tagged, "backbone"], df.loc[tagged, "grid"]))
    if not stems:
        return None
    runs = set(zip(df["dataset"], df["backbone"], df["run"]))
    keep = []
    for i, r in df.iterrows():
        if (r["dataset"], r["backbone"], r["grid"]) not in stems:
            continue
        if tag in r["run"] or (r["dataset"], r["backbone"], f"{r['grid']}{tag}0") not in runs:
            keep.append(i)
    out = []
    for (ds, bb, gr, comp), g in df.loc[keep].groupby(["dataset", "backbone", "grid", "comparison"], sort=False):
        if len(g) < 2:
            continue
        sd = float(g["mean"].std(ddof=1))
        se_i, se_f = float(g["se_image"].mean()), float(g["se_family"].mean())
        out.append(dict(dataset=ds, backbone=bb, grid=gr, comparison=comp, n_splits=len(g),
                        mean_of_means=float(g["mean"].mean()), sd_across_splits=sd, se_image=se_i,
                        se_family=se_f, sd_over_se_image=sd / se_i, sd_over_se_family=sd / se_f,
                        se_ratio_min=float(g["se_ratio"].min()), se_ratio_max=float(g["se_ratio"].max())))
    return pd.DataFrame(out) if out else None


def per_severity(D3, severities, alpha=ALPHA, n_gpq=20000, seed=SEED):
    """Crossed components separately at each severity level, plus the severity average."""
    D3 = np.asarray(D3, float)
    rows = []
    labels = [str(s) for s in severities] + ["mean"]
    for j, s in enumerate(labels):
        tw = two_way(D3[:, :, j] if s != "mean" else D3.mean(2), alpha=alpha, n_gpq=n_gpq, seed=seed)
        rows.append(dict(severity=s, mean=tw["mean"], sigma_a=tw["sigma_a"], sigma_b=tw["sigma_b"],
                         sigma_e=tw["sigma_e"], rho_family=tw["rho_family"],
                         rho_family_lo=tw.get("rho_family_lo"), rho_family_hi=tw.get("rho_family_hi"),
                         se_ratio=tw["se_ratio"], se_ratio_lo=tw["se_ratio_lo"], se_ratio_hi=tw["se_ratio_hi"],
                         F_family=tw["F_family"], p_F_family=tw["p_F_family"]))
    return pd.DataFrame(rows)


def _locate(loss, tau):
    """First crossing of tau on a severity ladder of losses -> (j0, j1, w) or None."""
    for j in range(1, len(loss)):
        lo, hi = loss[j - 1], loss[j]
        if lo <= tau <= hi and hi > lo:
            return j - 1, j, (tau - lo) / (hi - lo)
    return None


def amplitude_matched(D3, acc, families, severities, targets=None, D_clean=None, acc_clean=None,
                      use_clean=False, method="interp", alpha=ALPHA, n_gpq=20000, seed=SEED,
                      min_families=3):
    """Re-estimate the family component with families compared at matched damage.

    Damage is the probe's accuracy loss, which no arm changes (all arms rescale logits by a
    positive temperature), so the matching variable is not the analysed NLL difference.
    method="interp": for each family, interpolate the per-image differences linearly between
    the two severity levels whose losses bracket the target; families whose ladder does not
    reach the target are left out at that target (at least min_families are needed).
    method="nearest": use each family's level closest to the target and report the mismatch.
    use_clean=True also interpolates toward the clean condition (zero loss). It is off by
    default: the clean column is the same for every family, so mixing it in shrinks family
    differences mechanically at low targets. Default targets: accuracy losses 0.05 to 0.40."""
    D3 = np.asarray(D3, float); acc = np.asarray(acc, float)
    m, F, S = D3.shape
    base = acc_clean if acc_clean is not None else float(np.max(acc))
    loss = base - acc                                   # F x S, larger = more damage
    levels = list(severities)
    if use_clean and D_clean is not None and acc_clean is not None:
        loss = np.hstack([np.zeros((F, 1)), loss])
        D3 = np.concatenate([np.asarray(D_clean, float)[:, None, None].repeat(F, 1), D3], axis=2)
        levels = [0] + levels
    if targets is None:
        targets = [0.05, 0.10, 0.20, 0.30, 0.40]
    rows = []
    for tau in targets:
        cols, used, where, mism = [], [], [], []
        for f in range(F):
            if method == "nearest":
                j = int(np.argmin(np.abs(loss[f] - tau)))
                cols.append(D3[:, f, j]); used.append(families[f]); where.append(str(levels[j]))
                mism.append(float(loss[f, j] - tau))
                continue
            hit = _locate(loss[f], tau)
            if hit is None:
                continue
            j0, j1, w = hit
            cols.append((1 - w) * D3[:, f, j0] + w * D3[:, f, j1]); used.append(families[f])
            where.append(f"{levels[j0]}+{w:.2f}")
        row = dict(target_loss=float(tau), n_families=len(cols), families=";".join(used),
                   position=";".join(where))
        if method == "nearest":
            row["max_abs_mismatch"] = float(np.max(np.abs(mism)))
        if len(cols) >= min_families:
            tw = two_way(np.column_stack(cols), alpha=alpha, n_gpq=n_gpq, seed=seed)
            row.update(mean=tw["mean"], sigma_a=tw["sigma_a"], sigma_b=tw["sigma_b"], sigma_e=tw["sigma_e"],
                       rho_family=tw["rho_family"], rho_family_lo=tw.get("rho_family_lo"),
                       rho_family_hi=tw.get("rho_family_hi"), se_ratio=tw["se_ratio"],
                       se_ratio_lo=tw["se_ratio_lo"], se_ratio_hi=tw["se_ratio_hi"],
                       F_family=tw["F_family"], p_F_family=tw["p_F_family"])
        rows.append(row)
    return pd.DataFrame(rows), loss


# ----------------------------------------------------------------------------- driver
def default_pairs(arms):
    pairs = [(a, b) for b in BASELINES for a in TREATMENTS if a in arms and b in arms]
    extra = sorted(x for x in arms if x.endswith("o") and x.startswith("C5"))   # oracle arms
    pairs += [(a, o) for o in extra for a in TREATMENTS if a in arms]
    return pairs


def analyse_pair(cube, A, B, args):
    D3 = cube["D3"]; D = D3.mean(2); fams = cube["families"]
    tw = two_way(D, alpha=args.alpha, n_gpq=args.n_gpq, seed=args.seed)
    bt = image_bootstrap(D, B=args.n_boot, alpha=args.alpha, seed=args.seed)
    pm = perm_test(D, n_perm=args.n_perm, seed=args.seed)
    t2 = hotelling_rm(D)
    wt = wts_perm_test(D, n_perm=args.n_perm_wts, seed=args.seed)
    fc = fold_clustered(D, cube["folds"], alpha=args.alpha, B=args.n_boot, seed=args.seed)
    lf = lofo(D, fams, alpha=args.alpha)
    ps = per_severity(D3, cube["severities"], alpha=args.alpha, n_gpq=args.n_gpq, seed=args.seed)
    am = None
    if cube["acc"] is not None:
        am, _ = amplitude_matched(D3, cube["acc"], fams, cube["severities"], targets=args.targets,
                                  D_clean=cube["D_clean"], acc_clean=cube["acc_clean"],
                                  method=args.amp_method, alpha=args.alpha, n_gpq=args.n_gpq, seed=args.seed)
    row = dict(comparison=f"{A} vs {B}", m=tw["m"], F=tw["F"], S=D3.shape[2], mean=tw["mean"],
               se_family=tw["se_family"], se_image=tw["se_image"], se_image_boot=bt["se_from_width"],
               se_ratio=tw["se_ratio"], se_ratio_lo=tw["se_ratio_lo"], se_ratio_hi=tw["se_ratio_hi"],
               p_se_ratio=tw["p_se_ratio"],
               t5_sigma_a=tw["sigma_a_2c"], t5_sigma_e=tw["sigma_e_2c"], t5_rho=tw["rho_2c"],
               t5_rho_lo=tw["rho_2c_lo"], t5_rho_hi=tw["rho_2c_hi"],
               sigma_a=tw["sigma_a"], sigma_b=tw["sigma_b"], sigma_e=tw["sigma_e"],
               rho_family=tw["rho_family"], rho_family_lo=tw.get("rho_family_lo"),
               rho_family_hi=tw.get("rho_family_hi"), F_family=tw["F_family"], p_F_family=tw["p_F_family"],
               se_full=tw["se_full"], df_full=tw["df_full"], full_over_family=tw["full_over_family"],
               ci_family_lo=tw["ci_family"][0], ci_family_hi=tw["ci_family"][1],
               ci_full_lo=tw["ci_full"][0], ci_full_hi=tw["ci_full"][1],
               ci_image_boot_lo=bt["ci_boot"][0], ci_image_boot_hi=bt["ci_boot"][1],
               perm_p=pm["p"], perm_ratio_to_median=pm["ratio_to_median"],
               T2=t2["T2"], T2_p_F=t2["p_F"], wts_perm_p=wt["p"],
               icc_fold=fc["icc_fold"], icc_fold_hi=fc["icc_fold_hi"], design_effect=fc["design_effect"],
               design_effect_hi=fc["design_effect_hi"],
               se_ratio_fold_adjusted=tw["se_family"] / fc["se_image_deff"],
               se_ratio_fold_adjusted_conservative=tw["se_family"] / fc["se_image_deff_hi"],
               se_image_cluster_robust=fc["se_image_cluster_robust"],
               se_image_two_stage=fc["se_image_two_stage"],
               fold_share_of_family_var=fc["var_fold"] / tw["se_family"] ** 2,
               fold_share_of_family_var_hi=fc["var_fold_hi"] / tw["se_family"] ** 2,
               se_full_with_fold=math.sqrt(tw["se_full"] ** 2 + fc["var_fold"]),
               se_full_with_fold_hi=math.sqrt(tw["se_full"] ** 2 + fc["var_fold_hi"]),
               lofo_min_p_family=float(lf["p_family"].iloc[1:].min()),
               lofo_family_at_min=str(lf.iloc[1:].loc[lf["p_family"].iloc[1:].idxmin(), "omitted"]),
               lofo_min_se_ratio=float(lf["se_ratio"].iloc[1:].min()))
    return row, dict(lofo=lf, per_severity=ps, amplitude_matched=am,
                     family_by_severity_means=pd.DataFrame(D3.mean(0), index=fams,
                                                           columns=[str(s) for s in cube["severities"]]))


def _f(x, d=3):
    if x is None or (isinstance(x, float) and not np.isfinite(x)):
        return "n/a"
    return f"{x:.{d}f}"


def _p(x):
    return "n/a" if x is None else (f"{x:.1e}" if x < 1e-3 else f"{x:.3f}")


def write_report(path, groups, args, split=None):
    L = ["# Revision analyses", "",
         f"alpha {args.alpha}; {args.n_perm} permutations (plain), {args.n_perm_wts} (studentized); "
         f"{args.n_gpq} generalized-pivot draws; {args.n_boot} bootstrap replicates; seed {args.seed}.", ""]
    for key, rows, warns in groups:
        if not rows:
            continue
        L += [f"## {' / '.join(key)}", "",
              f"m = {rows[0]['m']} images, F = {rows[0]['F']} families, {rows[0]['S']} severity levels.", ""]
        for w in warns:
            L += [f"Warning: {w}", ""]
        L += ["### Table 5 quantities, recomputed (two-component, Section 5.3 definitions)", "",
              "| comparison | sigma_a | sigma_e | rho [95% exact] | SE ratio [95% exact] | SE ratio, bootstrap SE |",
              "|---|---|---|---|---|---|"]
        for r in rows:
            L.append(f"| {r['comparison']} | {_f(r['t5_sigma_a'])} | {_f(r['t5_sigma_e'])} | {_f(r['t5_rho'])} "
                     f"[{_f(r['t5_rho_lo'])}, {_f(r['t5_rho_hi'])}] | {_f(r['se_ratio'], 2)} "
                     f"[{_f(r['se_ratio_lo'], 2)}, {_f(r['se_ratio_hi'], 2)}] | "
                     f"{_f(r['se_family'] / r['se_image_boot'], 2)} |")
        L += ["", "### Crossed decomposition and tests of the family effect", "",
              "| comparison | sigma_a | sigma_b | sigma_e | rho_family [95% GCI] | F test p | permutation p "
              "(obs/median) | Hotelling p | studentized perm p | full SE / family SE |",
              "|---|---|---|---|---|---|---|---|---|---|"]
        for r in rows:
            L.append(f"| {r['comparison']} | {_f(r['sigma_a'])} | {_f(r['sigma_b'])} | {_f(r['sigma_e'])} | "
                     f"{_f(r['rho_family'])} [{_f(r['rho_family_lo'])}, {_f(r['rho_family_hi'])}] | "
                     f"{_p(r['p_F_family'])} | {_p(r['perm_p'])} ({_f(r['perm_ratio_to_median'], 1)}) | "
                     f"{_p(r['T2_p_F'])} | {_p(r['wts_perm_p'])} | {_f(r['full_over_family'], 4)} |")
        L += ["", "### Intervals for the mean difference", "",
              "| comparison | mean | image bootstrap 95% | family t 95% | full crossed 95% (df) |",
              "|---|---|---|---|---|"]
        for r in rows:
            L.append(f"| {r['comparison']} | {_f(r['mean'], 4)} | [{_f(r['ci_image_boot_lo'], 4)}, "
                     f"{_f(r['ci_image_boot_hi'], 4)}] | [{_f(r['ci_family_lo'], 4)}, {_f(r['ci_family_hi'], 4)}] "
                     f"| [{_f(r['ci_full_lo'], 4)}, {_f(r['ci_full_hi'], 4)}] ({_f(r['df_full'], 1)}) |")
        L += ["", "### Leave one family out and fold dependence", "",
              "| comparison | smallest LOFO family p (family omitted) | smallest LOFO SE ratio | fold ICC [upper] "
              "| design effect [upper] | SE ratio, fold-adjusted [conservative] |",
              "|---|---|---|---|---|---|"]
        for r in rows:
            L.append(f"| {r['comparison']} | {_p(r['lofo_min_p_family'])} ({r['lofo_family_at_min']}) | "
                     f"{_f(r['lofo_min_se_ratio'], 2)} | {_f(r['icc_fold'], 4)} [{_f(r['icc_fold_hi'], 4)}] | "
                     f"{_f(r['design_effect'], 2)} [{_f(r['design_effect_hi'], 2)}] | "
                     f"{_f(r['se_ratio_fold_adjusted'], 2)} [{_f(r['se_ratio_fold_adjusted_conservative'], 2)}] |")
        L += ["", "Fold component as a share of the family-level variance: "
              + "; ".join(f"{r['comparison']} {_f(r['fold_share_of_family_var'], 3)} "
                          f"[upper {_f(r['fold_share_of_family_var_hi'], 3)}]" for r in rows) + ".", "",
              "Per-comparison tables (LOFO, per severity, amplitude matched, family x severity means) "
              "are in the comparison folders.", ""]
    if split is not None and len(split):
        L += ["## Repeated fold partitions", "",
              "| dataset / backbone / grid | comparison | splits | SD of the mean over splits | SE image | "
              "SE family | SD / SE image | SD / SE family | SE ratio range |", "|---|---|---|---|---|---|---|---|---|"]
        for _, r in split.iterrows():
            L.append(f"| {r['dataset']} / {r['backbone']} / {r['grid']} | {r['comparison']} | {r['n_splits']} | "
                     f"{_f(r['sd_across_splits'], 4)} | {_f(r['se_image'], 4)} | {_f(r['se_family'], 4)} | "
                     f"{_f(r['sd_over_se_image'], 2)} | {_f(r['sd_over_se_family'], 2)} | "
                     f"{_f(r['se_ratio_min'], 2)} to {_f(r['se_ratio_max'], 2)} |")
        L.append("")
    Path(path).write_text("\n".join(L))


def run(args):
    df = load_long(args.inputs)
    out = Path(args.out); out.mkdir(parents=True, exist_ok=True)
    groups, allrows = [], []
    for key, g in df.groupby(["dataset", "backbone", "run"], sort=False):
        arms = set(g["arm"].unique())
        pairs = [tuple(p.split(":")) for p in args.pairs] if args.pairs else default_pairs(arms)
        rows, warns = [], []
        for A, B in pairs:
            t0 = time.time()
            try:
                cube = paired_cube(g, A, B)
            except ValueError as e:
                warns.append(str(e)); print("  skipped:", e); continue
            if cube is None:
                continue
            warns += cube["warnings"]
            row, tabs = analyse_pair(cube, A, B, args)
            row.update(dataset=key[0], backbone=key[1], run=key[2])
            rows.append(row)
            d = out / "_".join(key).replace("/", "-") / f"{A}_vs_{B}"
            d.mkdir(parents=True, exist_ok=True)
            for name, tab in tabs.items():
                if tab is not None:
                    tab.to_csv(d / f"{name}.csv", index=(name == "family_by_severity_means"))
            print(f"  {' / '.join(key)}  {A} vs {B}: SE ratio {row['se_ratio']:.2f} "
                  f"[{row['se_ratio_lo']:.2f}, {row['se_ratio_hi']:.2f}], studentized perm p {row['wts_perm_p']:.1e} "
                  f"({time.time() - t0:.0f} s)")
        groups.append((key, rows, sorted(set(warns))))
        allrows += rows
    split = None
    if allrows:
        cols = ["dataset", "backbone", "run"] + [c for c in allrows[0] if c not in ("dataset", "backbone", "run")]
        pd.DataFrame(allrows)[cols].to_csv(out / "summary.csv", index=False)
        split = split_variability(allrows, args.split_tag)
        if split is not None:
            split.to_csv(out / "split_variability.csv", index=False)
    write_report(out / "report.md", groups, args, split)
    print(f"wrote {out / 'summary.csv'} and {out / 'report.md'}")


# ----------------------------------------------------------------------------- self-test
def selftest(quick=False):
    rng = np.random.default_rng(7)
    R = 0.25 if quick else 1.0
    ok = True

    def check(name, cond, detail):
        nonlocal ok
        ok &= bool(cond)
        print(f"  [{'pass' if cond else 'FAIL'}] {name}: {detail}")

    print("1. moment estimators recover known components (m = 900, F = 6; mean over replicates)")
    for s2a, s2b, s2e in [(0.0, 0.5, 1.0), (0.08, 0.0, 1.0), (0.3, 0.2, 0.5)]:
        est = []
        for _ in range(int(300 * R)):
            D = (rng.normal(0, math.sqrt(s2a), 6)[None] + rng.normal(0, math.sqrt(s2b), 900)[:, None]
                 + rng.normal(0, math.sqrt(s2e), (900, 6)))
            m_, F_, gm, MSA, MSB, MSE = mean_squares(D)
            est.append(((MSA - MSE) / 900, (MSB - MSE) / 6, MSE))
        e = np.mean(est, 0)
        check(f"(s2a, s2b, s2e) = ({s2a}, {s2b}, {s2e})",
              abs(e[0] - s2a) < 0.03 + 0.25 * s2a and abs(e[1] - s2b) < 0.02 and abs(e[2] - s2e) < 0.02,
              f"recovered ({e[0]:.3f}, {e[1]:.3f}, {e[2]:.3f}), unbiased moment estimators")

    print("2. coverage of the exact SE-ratio CI, the generalized CI for rho_family, and the full crossed CI")
    n = int(1000 * R)
    for s2a, s2b, s2e in [(0.05, 0.3, 1.0), (0.01, 0.0, 1.0), (0.2, 1.0, 0.5)]:
        true_R = math.sqrt((900 * s2a + s2e) / (6 * s2b + s2e)); true_rho = s2a / (s2a + s2b + s2e)
        cr = cg = cf = 0; ng = max(int(n * 0.5), 150)
        for k in range(n):
            D = 0.1 + (rng.normal(0, math.sqrt(s2a), 6)[None] + rng.normal(0, math.sqrt(s2b), 900)[:, None]
                       + rng.normal(0, math.sqrt(s2e), (900, 6)))
            tw = two_way(D, n_gpq=2000 if k < ng else 0, seed=k)
            cr += tw["se_ratio_lo"] <= true_R <= tw["se_ratio_hi"]
            cf += tw["ci_full"][0] <= 0.1 <= tw["ci_full"][1]
            if k < ng:
                cg += tw["rho_family_lo"] <= true_rho <= tw["rho_family_hi"]
        mc = 2 * math.sqrt(0.95 * 0.05 / n)
        check(f"SE ratio CI, true ratio {true_R:.2f}", abs(cr / n - 0.95) < mc + 0.005, f"coverage {cr / n:.3f} (n = {n})")
        check(f"rho_family GCI, true rho {true_rho:.3f}", cg / ng > 0.90, f"coverage {cg / ng:.3f} (n = {ng})")
        check("full crossed CI for the mean", cf / n > 0.92, f"coverage {cf / n:.3f} (n = {n})")

    print("3. tests of the family effect under a heteroskedastic null (no family effect)")
    sd = np.array([0.4, 0.6, 0.8, 1.0, 1.5, 2.2]); reps = int(400 * R)
    rej = np.zeros(3)
    for k in range(reps):
        common = rng.normal(0, 1, (900, 1))
        D = 0.1 + rng.normal(0, 0.3, (900, 1)) + (0.5 * common + math.sqrt(0.75) * rng.normal(0, 1, (900, 6))) * sd
        rej += [perm_test(D, n_perm=200, seed=k)["p"] < 0.05, hotelling_rm(D)["p_F"] < 0.05,
                wts_perm_test(D, n_perm=200, seed=k)["p"] < 0.05]
    r = rej / reps; mc = 2 * math.sqrt(0.05 * 0.95 / reps)
    print(f"       rejection at 0.05: plain permutation {r[0]:.3f}, Hotelling {r[1]:.3f}, "
          f"studentized permutation {r[2]:.3f}  ({reps} replicates)")
    check("Hotelling T^2 holds its level", r[1] < 0.05 + mc, f"{r[1]:.3f}")
    check("studentized permutation holds its level", r[2] < 0.05 + mc, f"{r[2]:.3f}")
    a = np.zeros(6); a[4] = 0.25
    D = 0.1 + a[None] + rng.normal(0, 0.3, (900, 1)) + rng.normal(0, 1, (900, 6))
    pw = (perm_test(D, n_perm=2000)["p"], hotelling_rm(D)["p_F"], wts_perm_test(D, n_perm=2000)["p"])
    check("all three detect a single shifted family (shift 0.25 SD)", max(pw) < 0.01,
          "p = " + ", ".join(f"{x:.1e}" for x in pw))

    print("4. amplitude matching separates ladder calibration from mechanism")
    fams = [f"f{j}" for j in range(6)]; sevs = [1, 2, 3, 4, 5]
    steep = np.array([0.03, 0.05, 0.08, 0.11, 0.15, 0.20])          # loss per level, unequal ladders
    loss = steep[:, None] * np.arange(1, 6)[None]                       # 6 x 5
    acc = 0.95 - loss
    for label, mech in [("ladder only", np.zeros(6)), ("ladder + mechanism", rng.normal(0, 0.15, 6))]:
        b = rng.normal(0, 0.3, (900, 1, 1))
        D3 = 0.8 * loss[None] + mech[None, :, None] * np.arange(1, 6)[None, None] / 3 + b \
            + rng.normal(0, 0.5, (900, 6, 5))
        un = two_way(D3.mean(2), n_gpq=0)
        am, _ = amplitude_matched(D3, acc, fams, sevs, targets=[0.15, 0.25], D_clean=None, acc_clean=0.95,
                                  n_gpq=0)
        pmin = am["p_F_family"].min()
        print(f"       {label:20s} unmatched sigma_a {un['sigma_a']:.3f} (F test p {un['p_F_family']:.1e}); "
              f"matched sigma_a {', '.join(f'{x:.3f}' for x in am['sigma_a'])} (smallest p {pmin:.1e})")
        if label == "ladder only":
            check("ladder-only heterogeneity disappears after matching", un["p_F_family"] < 1e-6 and pmin > 0.001,
                  "unmatched significant, matched not")
        else:
            check("mechanism heterogeneity survives matching", pmin < 1e-3, "matched still significant")

    print("5. fold dependence")
    folds = np.repeat(np.arange(5), 180)
    for label, sf in [("no fold effect", 0.0), ("fold effect, true ICC 0.02", 0.0725)]:
        D = rng.normal(0, 1, (900, 6)) + rng.normal(0, sf, 5)[folds][:, None] + rng.normal(0, 0.3, (900, 1))
        fc = fold_clustered(D, folds, B=500)
        print(f"       {label:28s} ICC {fc['icc_fold']:.4f} [upper {fc['icc_fold_hi']:.4f}], design effect "
              f"{fc['design_effect']:.2f}; SE iid {fc['se_image_iid']:.4f}, cluster-robust "
              f"{fc['se_image_cluster_robust']:.4f}, two-stage {fc['se_image_two_stage']:.4f}")
    check("fold module runs and reports a design effect", np.isfinite(fc["design_effect"]), "ok")

    print("6. end to end on a simulated long table (two fold partitions)")
    import tempfile
    tmp = Path(tempfile.mkdtemp(prefix="sdic_selftest_"))
    rows = []
    m, imgs = 900, np.arange(900)
    for split in (0, 1):
        folds = rng.permutation(np.repeat(np.arange(5), 180))
        for arm, shift in [("C2 scalar / augmented", 0.0), ("C4 linear / raw q", 0.05),
                           ("C5 linear / class one-hot", 0.02)]:
            for fi, fam in enumerate(fams[:6]):
                for s in sevs:
                    nll = 0.5 + 0.1 * s + 0.05 * fi + shift * (1 + 0.5 * fi) + rng.normal(0, 0.2, m)
                    rows.append(pd.DataFrame(dict(
                        dataset="SIM", backbone="toy", run=f"G2-split{split}", fold=folds, image_id=imgs,
                        family=fam, severity=s, arm=arm, nll=nll,
                        correct=(rng.random(m) < 0.95 - loss[fi, s - 1]).astype(int))))
    sim = pd.concat(rows)
    sim["correct"] = sim.groupby(["run", "image_id", "family", "severity"])["correct"].transform("first")
    sim.to_csv(tmp / "sim.csv.gz", index=False)
    ns = argparse.Namespace(inputs=[str(tmp / "sim.csv.gz")], out=str(tmp / "results"), pairs=None,
                            alpha=ALPHA, n_perm=500, n_perm_wts=300, n_gpq=2000, n_boot=300, seed=SEED,
                            targets=None, amp_method="interp", split_tag="-split")
    run(ns)
    S = pd.read_csv(tmp / "results" / "summary.csv")
    check("summary has the default comparisons for both partitions",
          len(S) == 4 and set(S.comparison) == {"C4 vs C2", "C4 vs C5"}, ", ".join(S.comparison))
    sv = pd.read_csv(tmp / "results" / "split_variability.csv")
    check("repeated-partition table", len(sv) == 2 and (sv.n_splits == 2).all(), f"{len(sv)} rows")
    ps = pd.read_csv(tmp / "results" / "SIM_toy_G2-split0" / "C4_vs_C2" / "per_severity.csv")
    am = pd.read_csv(tmp / "results" / "SIM_toy_G2-split0" / "C4_vs_C2" / "amplitude_matched.csv")
    check("per-severity and amplitude tables written", len(ps) == 6 and len(am) >= 1,
          f"{len(ps)} severity rows, {len(am)} amplitude targets")
    print(f"       outputs in {tmp / 'results'}")
    print("\nSELF-TEST", "PASSED" if ok else "FAILED")
    return ok


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("inputs", nargs="*", help="long per-image table(s): CSV, CSV.GZ or Parquet")
    ap.add_argument("--out", default="revision_results")
    ap.add_argument("--pairs", nargs="*", help="comparisons as A:B, e.g. C4:C2 C4:C5o (default: the twelve)")
    ap.add_argument("--alpha", type=float, default=ALPHA)
    ap.add_argument("--n-perm", type=int, default=20000)
    ap.add_argument("--n-perm-wts", type=int, default=5000)
    ap.add_argument("--n-gpq", type=int, default=20000)
    ap.add_argument("--n-boot", type=int, default=2000)
    ap.add_argument("--seed", type=int, default=SEED)
    ap.add_argument("--targets", type=float, nargs="*", help="accuracy-loss targets for amplitude matching")
    ap.add_argument("--amp-method", choices=["interp", "nearest"], default="interp")
    ap.add_argument("--split-tag", default="-split", help="run-name tag marking repeated fold partitions")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--quick", action="store_true", help="smaller self-test")
    ap.add_argument("--export-help", action="store_true")
    a = ap.parse_args(argv)
    if a.export_help:
        print(EXPORT_HELP); return 0
    if a.selftest:
        return 0 if selftest(quick=a.quick) else 1
    if not a.inputs:
        ap.error("give at least one input table, or --selftest, or --export-help")
    run(a)
    return 0


if __name__ == "__main__":
    sys.exit(main())
