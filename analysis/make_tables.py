"""Markdown for revised Tables 3, 4 and 5 from the re-run (full-precision inputs, rounded once).

Usage: python3 -I make_tables.py <ms_numbers_dir>
"""
import sys, json, re
import pandas as pd

S = sys.argv[1]
R = pd.read_csv(f"{S}/comparisons_rerun.csv")
RB = json.load(open(f"{S}/repro_boot.json"))
num = lambda s: [float(x) for x in re.findall(r"-?\d+\.\d+(?:e-?\d+)?", s)]
M = "−"

def sg(x, d=3):          # signed, explicit plus, true minus
    s = f"{x:+.{d}f}"
    return s.replace("-", M)
def us(x, d=3):          # unsigned format, true minus
    return f"{x:.{d}f}".replace("-", M)

# ---- Table 3: NLL from per-image data (full precision); ECE/AURC as printed by the notebook (4 dp)
nll = RB["nll"]
ece = {"C0": (0.1257, 0.0126, 0.1051), "C1": (0.1160, 0.0212, 0.1017), "C2": (0.0482, 0.0253, 0.1091),
       "C3": (0.1185, 0.0115, 0.1101), "C4": (0.0407, 0.0194, 0.0860), "C5": (0.0490, 0.0124, 0.0990),
       "C6c": (0.0500, 0.0171, 0.0949), "C7": (0.0445, 0.0139, 0.0879), "C7q": (0.0390, 0.0163, 0.0823),
       "C8": (0.0500, 0.0209, 0.0832), "C8b": (0.0419, 0.0187, 0.0834)}
nll["C0"] = dict(mean=1.2024, sd=0.2463)    # C0 is not in the per-image export; notebook value (4 dp)
labels = [("C0", "C0 uncalibrated"), ("C1", "C1 scalar, clean fit"), ("C2", "C2 scalar, augmented fit"),
          ("C3", "C3 MLP, raw q"), ("C4", "C4 linear, raw q"), ("C5", "C5 linear, class one-hot"),
          ("C6c", "C6c linear, standardised q"), ("C7", "C7 bounded, standardised q"),
          ("C7q", "C7q bounded, raw q"), ("C8", "C8 linear, class + q"), ("C8b", "C8b bounded, class + q")]
t3 = ["| Arm | NLL | ECE | AURC |", "| --- | --- | --- | --- |"]
for k, lab in labels:
    e = ece[k]
    t3.append(f"| {lab} | {nll[k]['mean']:.3f} ± {nll[k]['sd']:.3f} | {e[0]:.4f} ± {e[1]:.4f} | {e[2]:.4f} |")

# ---- Table 4
FAM = ["motion_blur", "shot_noise", "brightness_drift", "contrast_loss", "vignetting", "vibration_jitter"]
t4 = ["| Comparison | Motion | Shot | Bright. | Contrast | Vignet. | Vibrat. | Mean | Image-level 95% CI | Family-level 95% CI |",
      "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
for _, r in R.iterrows():
    b = RB["boot"][r["comparison"]]; cf = num(r["ci_family"])
    cells = [sg(r[f"d_{f}"]) for f in FAM]
    t4.append(f"| {r['A']} vs. {r['B']} | " + " | ".join(cells) +
              f" | {sg(r['mean'])} | [{us(b['lo'])}, {us(b['hi'])}] | [{us(cf[0])}, {us(cf[1])}] |")

# ---- Table 5
t5 = ["| Comparison | σ_a | σ_e | ρ (lower bound) | SE ratio [95% CI] | ρ_family [95% CI] | F |",
      "| --- | --- | --- | --- | --- | --- | --- |"]
for _, r in R.iterrows():
    t5.append(f"| {r['A']} vs. {r['B']} | {r['sigma_a_2c']:.3f} | {r['sigma_e_2c']:.3f} | "
              f"{r['rho_2c']:.3f} ({r['rho_2c_lo']:.3f}) | {r['se_ratio']:.2f} [{r['se_ratio_lo']:.2f}, {r['se_ratio_hi']:.2f}] | "
              f"{r['rho_family']:.3f} [{r['rho_family_lo']:.2f}, {r['rho_family_hi']:.2f}] | {r['F_family']:.1f} |")

out = {"t3": "\n".join(t3), "t4": "\n".join(t4), "t5": "\n".join(t5)}
json.dump(out, open(f"{S}/tables_md.json", "w"), ensure_ascii=False, indent=1)
for k in ("t3", "t4", "t5"):
    print(out[k]); print()
