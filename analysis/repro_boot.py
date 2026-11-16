"""Reproduce the notebook's image-level bootstrap intervals (seed 20260821, 10,000 resamples of images)
at full precision from the per-image table, and give the NLL fold means at full precision.

Usage: python3 -I repro_boot.py <per_image_nll_G1.csv.gz> <out_dir>
"""
import sys, json
import numpy as np, pandas as pd

csv, out = sys.argv[1], sys.argv[2]
df = pd.read_csv(csv)
df["arm"] = df["arm"].astype(str)
test = df[df.family != "clean"]
SEED = 20260821
ARMS_T = ["C4", "C6c", "C7", "C7q", "C8", "C8b"]
res = {}
for A in ARMS_T:
    for B in ["C2", "C5"]:
        key = ["image_id", "family", "severity"]
        a = test[test.arm == A].set_index(key).nll
        b = test[test.arm == B].set_index(key).nll.reindex(a.index)
        d = (a - b)
        im = d.index.get_level_values("image_id").to_numpy()
        dv = d.to_numpy()
        uniq = np.unique(im)
        # image means (each image has 30 rows, so the mean of rows = mean of image means)
        s = pd.Series(dv).groupby(im).agg(["sum", "count"]).reindex(uniq)
        sums, cnts = s["sum"].to_numpy(), s["count"].to_numpy()
        rng = np.random.default_rng(SEED)
        bs = np.empty(10000)
        idx_all = np.arange(len(uniq))
        for k in range(10000):
            pick = rng.choice(uniq, len(uniq), True)
            pos = np.searchsorted(uniq, pick)
            bs[k] = sums[pos].sum() / cnts[pos].sum()
        res[f"{A} vs {B}"] = dict(mean=float(dv.mean()), lo=float(np.quantile(bs, .025)), hi=float(np.quantile(bs, .975)))
# NLL fold means at full precision
fm = test.groupby(["arm", "fold"]).nll.mean().unstack()
nll = {a: dict(mean=float(fm.loc[a].mean()), sd=float(fm.loc[a].std(ddof=1))) for a in fm.index}
json.dump(dict(boot=res, nll=nll), open(f"{out}/repro_boot.json", "w"), indent=1)
for k, v in res.items():
    print(f"{k:12s} mean {v['mean']:+.6f}  [{v['lo']:+.6f}, {v['hi']:+.6f}]")
for a, v in nll.items():
    print(f"{a:5s} {v['mean']:.6f} +/- {v['sd']:.6f}")
