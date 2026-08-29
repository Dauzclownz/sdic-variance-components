# SDI-C: corruption families as the unit of uncertainty

Code, derived data and audit artifacts for the paper:

> **For cross-corruption claims, the corruption family is the relevant unit of uncertainty: a variance-components analysis for surface-defect inspection**
> Muhammad Nur Firdaus, Universitas Nusa Mandiri
> Submitted to *Machine Vision and Applications*

---

## What this is about

A corruption-robustness result is usually reported with a confidence interval obtained by
resampling test images while holding the set of corruption types fixed. That interval is correct
for the corruptions actually tested, but it answers a narrower question than a claim about
robustness to acquisition degradation *in general*.

In a design where every image is evaluated under every corruption family, the family effect is
constant down a column and therefore contributes **no variance at all** to an image-level
bootstrap. The consequence has a closed form. Writing `m` for images per family and `F` for the
number of families, under the crossed model

```
d_if = μ + a_f + b_i + e_if
```

the ratio of the two standard errors is

```
SE_family / SE_image = sqrt( (m·σ_a² + σ_e²) / (F·σ_b² + σ_e²) )
```

At `σ_a² = 0` this ratio is **at most one**. An observed widening therefore cannot be an artefact
of having few clusters, which is the objection the result exists to answer. And because the ratio
grows as `sqrt(m)`, adding images widens the gap while only adding families closes it.

On this benchmark, family-level standard errors exceed image-level ones by **5.6 to 10.1×**
across five backbones, with family-level intraclass correlations of **0.033 to 0.101** and every
interval excluding zero.

---

## Repository contents

```
sdic/                    SDI-C corruption suite: twelve families, five severities
audit/                   thirteen-check pre-training audit protocol
analysis/                variance components, intervals, permutation test, power
notebooks/               two Colab notebooks, runnable without any local setup
data/
  folds/                 fold assignments for NEU-CLS and Magnetic Tile
  predictions/           per-image predictions, every condition and model run
  per_family/            per-family metric tables underlying Tables 3-11
artifacts/
  OR1_audit_report.*     PASS / FAIL / BLOCKED verdict and evidence, all 13 checks
  OR2_severity_audit.*   severity-monotonicity audit, per family and severity
  OR3_duplicate_flags.*  near-duplicate analysis, both datasets
  OR4_per_fold.*         per-fold, per-family results behind every table
```

> **Note.** The four `artifacts/` files are the Online Resources cited in the paper. The original
> image data are **not** redistributed here; see [Datasets](#datasets).

---

## Quickstart

Neither notebook needs a local install, a Google Drive mount, or a Kaggle token.

### Regenerate every table and figure

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Dauzclownz/sdic-variance-components/blob/main/notebooks/sdic_tables_and_figures.ipynb)

Runs in about a minute. It rebuilds Tables 1 and 3-11 and Figures 1-4. More usefully, it
**recomputes every derived quantity from its inputs and checks the result against the number
printed in the paper**. Confidence intervals, standard-error ratios, the crossed decomposition,
the power curve and the design curve are all regenerated rather than transcribed. The check
accounts for the fact that ρ is printed to three decimals, so it asks whether the published value
is attainable from some ρ consistent with its display precision, not whether it matches to an
arbitrary tolerance.

Current status: **79 / 79 published values reproduce from the stated estimator.**

Figures are written as EPS, PDF and 600-dpi PNG at the journal's column widths, with no titles
inside the illustrations.

### Reproduce the fine-tuning control (Table 10)

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://github.com/Dauzclownz/sdic-variance-components/blob/main/table10_reproduction.ipynb)

Downloads NEU-CLS directly, verifies what arrived against a content checksum, builds a corruption
cache, fine-tunes ResNet-50 across three seeds and five folds, and recomputes ρ per seed. About
an hour on a T4.

Training is made deterministic: cuDNN is pinned, `CUBLAS_WORKSPACE_CONFIG` is set before CUDA
initialises, and the augmentation RNG is seeded from `(seed, epoch, image index)` rather than
from the global NumPy state, which otherwise varies with DataLoader worker scheduling. A built-in
probe trains the same seed twice and compares weights, so a runtime that cannot be made
deterministic reports itself in two minutes instead of after a full run.

---

## Datasets

Neither dataset is redistributed here. Both are public:

| Dataset | Images | Classes | Notes |
|---|---|---|---|
| **NEU-CLS** | 1,800 | 6, balanced (300 each) | Hot-rolled steel strip, 200×200 greyscale. Distributed without an official split; ours is in `data/folds/`. |
| **Magnetic Tile** | 1,344 | 6, severely imbalanced (952 defect-free, 57-image crack class) | Different material, localized rather than textural defects. |

`notebooks/table10_reproduction.ipynb` fetches NEU-CLS automatically and verifies the download
against a content checksum before use, so a mirror serving a resized or partial copy is caught
rather than silently accepted.

---

## SDI-C

Twelve corruption families at five severities, each mapped to a documented line-camera failure
mode. Six are held out for testing; the augmentation-time and evaluation-time sets are disjoint.

| Split | Families |
|---|---|
| **train** | defocus blur, read noise, banding, JPEG artefacts, window contamination, perspective drift |
| **test** | motion blur, shot noise, brightness drift, contrast loss, vignetting, vibration jitter |

```python
from sdic import apply_corruption

out = apply_corruption(img_uint8, family="vignetting", severity=3, image_id="Sc_042")
```

Two implementation details are load-bearing and are not conventions you should change casually:

- **Nuisance parameters are seeded from `(image_id, family)` and deliberately *not* from
  severity.** Without this, the random draw changes with severity and the ladder is no longer a
  pure amplitude sweep. Fixing it moved the banding family's monotonicity score from 0.20 to 1.00.
- **Brightness drift is a gamma transform, not an additive offset.** The additive version
  saturated 32.7% of pixels at the top severity; the gamma version maps `[0,1]` onto itself and
  cannot clip.

Severities are verified monotone within a family against a pre-declared metric. They are **not**
amplitude-matched *across* families: nothing establishes that severity 3 of defocus blur damages a
classifier as much as severity 3 of vignetting. This matters when interpreting ρ, and is discussed
in the paper.

---

## Audit protocol

Thirteen checks that run before any model is trained, each with a pre-declared failure criterion
and one of three verdicts: `PASS`, `FAIL`, or `BLOCKED`.

```bash
python -m audit.run --dataset neu-cls --config configs/neu.yaml
```

`BLOCKED` is the design point worth borrowing. A check that cannot be validly executed must not
return `PASS`. The near-duplicate detector, for instance, is required to pass a validity
precondition (same- versus different-class AUROC ≥ 0.70) before its flags are trusted. On
Magnetic Tile it scored 0.649 and emitted nothing, so those folds carry no grouping constraint,
which is reported rather than resolved.

The protocol caught six defects in this pipeline before training, including a preprocessing
mismatch, a pixel-saturating corruption family, non-monotone severity, and a descriptor-leakage
failure that invalidated the study's original method. Full evidence is in
`artifacts/OR1_audit_report.*`.

---

## Analysis

```bash
python -m analysis.variance_components --input data/per_family/ --out results/
```

Design parameters: `F = 6` held-out families, `m = 900` images per family on NEU-CLS and
`m = 1344` on Magnetic Tile, α = 0.05.

- **Intraclass correlation** and its interval: exact one-way random-effects construction on the
  F distribution. Reported as a two-component reduction, which is a *lower bound* on the family
  ICC; a crossed refit puts it roughly 1.5× higher.
- **Permutation test**: family labels permuted within each image, 20,000 permutations. Exact at
  any number of families, so unaffected by `F = 6`. The test excludes image-level noise as the
  source of the observed between-family variance; it does not adjudicate a contested hypothesis,
  since σ_a² = 0 is not a proposition anyone holds a priori.
- **Power**: one-sample t test at the observed effect size `d = 0.425`. Power is 0.14 at six
  families; reaching 0.80 would need roughly 46.

---

## Caveats

Kept here rather than buried, because a repository for a paper about audit discipline should
surface its own limits.

- **The near-duplicate audit could not be validated on Magnetic Tile.** Its folds carry no
  grouping constraint. NEU-CLS is the primary analysis throughout, and every conclusion in the
  paper holds without Magnetic Tile.
- **Six families is the binding constraint.** Every interval here is wide for that reason, and the
  paper's own prescription is that more families, not more images, is the only lever.
- **The families were enumerated purposively, not sampled.** ρ describes heterogeneity among the
  degradations implemented here, at the severities implemented here. Extension beyond them is an
  extrapolation supported by physical motivation, not by a sampling design.
- **The primary estimand is a paired difference between calibration arms**, not model robustness.
  Table 10 gives the model-level evidence on an accuracy-deficit metric, where the values are
  larger.
- **KolektorSDD2 is absent.** It could not be obtained from a verified source, so the audit gate
  returned `BLOCKED` and the pipeline never ran on it.

---

## Environment

```bash
pip install -r requirements.txt
```

Python 3.10+. Core dependencies: `numpy`, `scipy`, `pandas`, `matplotlib`, `torch`,
`torchvision`, `pillow`. A GPU is needed only for the fine-tuning control; everything else runs
on CPU in minutes because features are cached once and every downstream analysis reads the cache
rather than touching an image again.

---

## License

Code is released under the MIT License (`LICENSE`). Derived data and audit artifacts are released
under CC BY 4.0 (`LICENSE-data`). The underlying image datasets remain under their original
licenses and are not redistributed here.

---

## Citation

```bibtex
@unpublished{firdaus2026sdic,
  author = {Firdaus, Muhammad Nur},
  title  = {For cross-corruption claims, the corruption family is the relevant
            unit of uncertainty: a variance-components analysis for
            surface-defect inspection},
  note   = {Manuscript submitted for publication},
  year   = {2026}
}
```

This entry will be replaced with the published reference and the archive DOI on acceptance.

---

## Notes on preparation

A large language model was used in preparing the manuscript and parts of the analysis and
plotting scripts, beyond the scope of AI-assisted copy editing. Its use is documented in
Section 5.4 of the paper. The experimental design, the corruption suite, the audit protocol and
all reported results are the author's own.
