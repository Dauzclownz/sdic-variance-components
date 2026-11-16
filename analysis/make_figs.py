"""Figures 2 to 4 of the revised manuscript, from the re-run of grid G1.

Usage: python3 -I make_figs.py <comparisons_rerun.csv> <ms_numbers.json> <out_dir>
Style follows the submitted figures (sdic_tables_and_figures.ipynb).
"""
import sys, json, math
import numpy as np, pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
from scipy import stats

comp_csv, num_json, out = sys.argv[1], sys.argv[2], sys.argv[3]
R = pd.read_csv(comp_csv)
N = json.load(open(num_json))

MM = 1 / 25.4
plt.rcParams.update({"font.family": "sans-serif", "font.sans-serif": ["DejaVu Sans", "Helvetica", "Arial"],
                     "font.size": 8, "axes.labelsize": 8, "axes.titlesize": 8, "xtick.labelsize": 7,
                     "ytick.labelsize": 7, "legend.fontsize": 7, "axes.linewidth": 0.6, "grid.linewidth": 0.4,
                     "lines.linewidth": 1.2, "savefig.bbox": "tight", "savefig.pad_inches": 0.02,
                     "pdf.fonttype": 42, "ps.fonttype": 42, "axes.spines.top": False, "axes.spines.right": False})
BLUE, DBLUE, RED, GREY = "#3a7fc1", "#1f5fa8", "#b2182b", "#555555"
MINUS = "−"

def save(fig, name):
    for ext in ("png", "pdf", "eps"):
        fig.savefig(f"{out}/{name}.{ext}", dpi=300 if ext == "png" else None)
    plt.close(fig)

# ----------------------------------------------------------------------------- Fig. 2
FAM = ["motion_blur", "shot_noise", "brightness_drift", "contrast_loss", "vignetting", "vibration_jitter"]
FLAB = ["motion blur", "shot noise", "bright. drift", "contrast loss", "vignetting", "vibr. jitter"]
ARMS = ["C4", "C6c", "C7", "C7q", "C8", "C8b"]
fig, axes = plt.subplots(2, 6, figsize=(174 * MM, 82 * MM), sharex=True, sharey=True)
x = np.arange(6)
for r, base in enumerate(["C2", "C5"]):
    for c, arm in enumerate(ARMS):
        ax = axes[r, c]
        row = R[(R.A == arm) & (R.B == base)].iloc[0]
        d = np.array([row[f"d_{f}"] for f in FAM])
        cols = [BLUE] * 6
        bars = ax.bar(x, d, width=0.72, color=cols, edgecolor="white", linewidth=0.4, zorder=2)
        v = FAM.index("vignetting")
        bars[v].set_facecolor("#f4d3d6"); bars[v].set_edgecolor(RED); bars[v].set_hatch("////")
        bars[v].set_linewidth(0.8)
        ax.axhline(0, color="black", lw=0.6, zorder=3)
        ax.axhline(row["mean"], color=GREY, lw=0.8, ls=(0, (3, 2)), zorder=4)
        ax.grid(axis="y", ls=":", color="#bbbbbb", zorder=0)
        ax.set_ylim(-0.65, 1.95)
        ax.set_yticks([-0.5, 0, 0.5, 1.0, 1.5])
        ax.set_yticklabels([f"{MINUS}0.5", "0", "0.5", "1.0", "1.5"])
        ax.tick_params(axis="x", length=0)
        if r == 0:
            ax.set_title(arm, fontsize=8, pad=3)
        if c == 5:
            ax.text(1.04, 0.5, f"against {base}", transform=ax.transAxes, rotation=270,
                    ha="left", va="center", fontsize=8)
        ax.text(0.03, 0.97, f"{row['mean']:+.3f}".replace("-", MINUS), transform=ax.transAxes,
                ha="left", va="top", fontsize=6.5, color=GREY)
for ax in axes[1]:
    ax.set_xticks(x)
    ax.set_xticklabels(FLAB, rotation=90, fontsize=6.5)
fig.supylabel("ΔNLL (negative favours the quality-conditioned arm)", fontsize=8, x=0.01)
handles = [Patch(facecolor=BLUE, edgecolor="white", label="per-family difference"),
           Patch(facecolor="#f4d3d6", edgecolor=RED, hatch="////", label="vignetting"),
           Line2D([0], [0], color=GREY, lw=0.8, ls=(0, (3, 2)), label="mean over the six families (value at top left)")]
fig.legend(handles=handles, loc="upper center", ncol=3, frameon=False, bbox_to_anchor=(0.53, 1.06))
fig.subplots_adjust(wspace=0.12, hspace=0.12, left=0.085, right=0.955)
save(fig, "Fig2")

# ----------------------------------------------------------------------------- Fig. 3
def power(d, n, alpha=0.05):
    df_ = n - 1; nc = d * math.sqrt(n); tc = stats.t.ppf(1 - alpha / 2, df_)
    return stats.nct.sf(tc, df_, nc) + stats.nct.cdf(-tc, df_, nc)
def n80(d):
    n = 3
    while power(d, n) < 0.8: n += 1
    return n
d0 = N["d_C7q_C5"]; n0 = n80(d0)
ns = np.logspace(np.log10(3), np.log10(400), 400)
fig, ax = plt.subplots(figsize=(105 * MM, 70 * MM))
for dref, lab in [(0.8, "d = 0.8"), (0.4, "d = 0.4")]:
    p = [power(dref, n) for n in ns]
    ax.plot(ns, p, color="#a9a9a9", lw=1.0, zorder=2)
    n_half = next(n for n in ns if power(dref, n) >= 0.5)
    ax.text(n_half * 1.13, 0.47, lab, color="#7a7a7a", fontsize=7, ha="left", va="center")
p0 = [power(d0, n) for n in ns]
ax.plot(ns, p0, color=DBLUE, lw=1.6, zorder=3)
ax.axhline(0.8, color=GREY, ls="--", lw=0.8, zorder=1)
ax.text(3.15, 0.81, "power 0.80", ha="left", va="bottom", fontsize=7, color="#333333")
pw6 = power(d0, 6)
ax.plot([6], [pw6], "o", color=RED, ms=6, zorder=4)
ax.annotate(f"SDI-C, six families\n(power {pw6:.2f})", xy=(6, pw6), xytext=(9.5, 0.27), color=RED, fontsize=7.5,
            arrowprops=dict(arrowstyle="->", color=RED, lw=0.8))
ax.plot([n0], [power(d0, n0)], "o", color=DBLUE, ms=6, zorder=4)
ax.annotate(f"{n0} families", xy=(n0, power(d0, n0)), xytext=(60, 0.55), color=DBLUE, fontsize=7.5,
            arrowprops=dict(arrowstyle="->", color=DBLUE, lw=0.8))
ax.text(150, 0.30, f"d = {d0:.3f}\n(C7q vs. C5)", color=DBLUE, fontsize=7, ha="center")
ax.set_xscale("log")
ax.set_xlim(3, 400); ax.set_ylim(0, 1.0)
ax.set_xticks([3, 6, 10, 20, 50, 100, 200, 400]); ax.set_xticklabels(["3", "6", "10", "20", "50", "100", "200", "400"])
ax.minorticks_off()
ax.grid(True, ls="--", color="#dddddd", lw=0.4)
ax.set_xlabel("number of test corruption families (log scale)")
ax.set_ylabel("power")
save(fig, "Fig3")

# ----------------------------------------------------------------------------- Fig. 4
sr = lambda rho, m: np.sqrt(1 + m * rho / (1 - rho))
rho_lo, rho_hi = N["rho_2c_range"]; rho_med = N["rho_2c_median"]
m = np.logspace(np.log10(20), 5, 400)
fig, ax = plt.subplots(figsize=(105 * MM, 100 * MM))
ax.fill_between(m, sr(rho_lo, m), sr(rho_hi, m), facecolor="#dceaf6", edgecolor="#9ec3e6", hatch="///", lw=0, zorder=1)
ax.plot(m, sr(rho_med, m), color=DBLUE, ls="--", lw=1.8, zorder=3)
ax.axhline(1, color=GREY, ls=":", lw=0.9, zorder=1)
ax.axvline(900, color=RED, ls=":", lw=0.9, zorder=1)
obs = np.sort(R.se_ratio.values)
ax.plot(np.full(len(obs), 900), obs, "o", color=RED, ms=4.5, mec="white", mew=0.5, zorder=5)
# Magnetic Tile (Table 8, original runs, not re-run): median rho 0.118 and SE-ratio range 5.0 to 25.4 at m = 1,344
mt_med = float(np.sqrt(1 + 1344 * 0.118 / (1 - 0.118)))
ax.plot([1344, 1344], [5.0, 25.4], color=GREY, lw=1.4, zorder=4)
ax.plot([1344], [mt_med], "D", mfc="white", mec=GREY, ms=7, mew=1.2, zorder=5)
for mm_, ha, dx, dy in [(50, "left", 0, 3.4), (50000, "right", 0, 0.17)]:
    y = sr(rho_med, mm_)
    ax.plot([mm_], [y], "o", mfc="white", mec=DBLUE, ms=7, mew=1.4, zorder=6)
    lbl = f"extrapolated,\nEq. (2): {y:.1f}" if y < 10 else f"extrapolated,\nEq. (2): {y:.0f}"
    ty = y * dy
    ax.annotate(lbl, xy=(mm_, y), xytext=(mm_ * (0.5 if mm_ == 50 else 1.0), ty), color=DBLUE, fontsize=8,
                ha=ha, va="bottom" if dy > 1 else "top",
                arrowprops=dict(arrowstyle="-", color=DBLUE, lw=0.8, shrinkA=0, shrinkB=4))
ax.annotate("observed: twelve\ncomparisons at m = 900\n(Table 5)", xy=(900, obs.max()), xytext=(560, 42),
            color=RED, fontsize=8, ha="right", va="bottom",
            arrowprops=dict(arrowstyle="-", color=RED, lw=0.8, shrinkB=3))
ax.annotate("observed range,\nsensitivity dataset,\nm = 1,344 (Table 8)", xy=(1344, 25.4), xytext=(1700, 135),
            color=GREY, fontsize=8, ha="left", va="bottom",
            arrowprops=dict(arrowstyle="-", color=GREY, lw=0.8, shrinkB=2))
ax.set_xscale("log"); ax.set_yscale("log")
ax.set_xlim(20, 1.1e5); ax.set_ylim(0.7, 300)
ax.grid(True, which="both", color="#e3e3e3", lw=0.5)
ax.set_xlabel("images per corruption family, $m$", fontsize=9)
ax.set_ylabel("SE$_{\\mathrm{family}}$ / SE$_{\\mathrm{image}}$", fontsize=9)
handles = [Line2D([0], [0], marker="o", color="none", mfc=RED, mec="white", ms=6, label="observed, NEU-CLS (m = 900, Table 5)"),
           Line2D([0], [0], marker="D", color=GREY, mfc="white", mec=GREY, ms=6, lw=1.4,
                  label="observed range, Magnetic Tile (m = 1,344, Table 8)"),
           Line2D([0], [0], color=DBLUE, ls="--", lw=1.8, label=f"Eq. (2), median ρ = {rho_med:.3f}, extrapolated in m"),
           Patch(facecolor="#dceaf6", edgecolor="#9ec3e6", hatch="///",
                 label=f"Eq. (2), observed ρ range {rho_lo:.3f} to {rho_hi:.3f}, extrapolated")]
ax.legend(handles=handles, loc="upper left", bbox_to_anchor=(-0.02, -0.11), frameon=False, fontsize=8, handlelength=2.2)
save(fig, "Fig4")
print("ok", n0, round(pw6, 4), round(mt_med, 2), [round(float(sr(rho_med, k)), 2) for k in (50, 900, 50000)])
