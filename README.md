# SDI-C: corruption families as a unit of uncertainty

Code, derived data and audit artifacts for the paper

> **Image-level intervals understate uncertainty in cross-corruption robustness claims: a variance-components analysis for surface-defect inspection**
> Muhammad Nur Firdaus, Universitas Nusa Mandiri. Under revision at *Pattern Analysis and Applications*.

The original image data are not redistributed. NEU-CLS and Magnetic Tile are public; the notebooks download NEU-CLS from Kaggle.

## What is here

| Path | Contents | Paper |
| --- | --- | --- |
| `PHASE0_*.ipynb` … `PHASE4_*.ipynb` (top level) | The original notebooks, with the printed outputs from which Tables 6 to 11 and the audit results were taken. The SDI-C implementation is embedded in each notebook (`CORE_V2`). | Sections 3, 4, 6 |
| `PHASE0_reviewer_proof_audit.ipynb`, `phase0_artifacts/` | The thirteen-check audit protocol and its artifacts. | Section 4 |
| `notebooks/PHASE0_11_family_uncertainty_revision.ipynb` | The notebook of the re-run (grid G1), with the printed outputs of the run that produced the per-image tables: the original Phase 0.11 notebook plus a section that exports per-image values, refits the oracle arm C5o and nine further fold partitions, and runs the revision analyses. Its copy of the amplitude-matched analysis uses default targets that proved degenerate; the corrected version is in `analysis/revision_analyses.py` and the stand-alone notebook, with results in `results/revision_G1/extra/`. | Sections 5.1, 6.4 to 6.7 |
| `notebooks/SDIC_revision_analyses_colab.ipynb` | The same analyses as a stand-alone notebook that reads the per-image tables. | |
| `notebooks/replicate_2026-11-16/`, `data/replicate_2026-11-16/`, `results/replicate_2026-11-16/` | A second run of the same notebook, unchanged, on 16 Nov 2026: the executed notebook, its per-image table for the original fold partition and its result tables. `comparison.txt` is the output of `analysis/compare_runs.py` against the first run: the predicted class changes for 2 of 27,900 image-condition pairs, and no standard-error ratio or ρ moves by more than 0.07 or 0.002. The released analyses use the first run. | Section 5.1 |
| `data/predictions/per_image_nll_G1.csv.gz` | Per-image negative log-likelihood of every calibrated arm (C1 to C8b and C5o) on clean images and under every held-out family and severity, for the re-run behind Tables 3 to 5 (900 images, 306,900 rows). Columns: `dataset, backbone, run, fold, image_id, family, severity, arm, nll, correct`. | Tables 3 to 5 |
| `data/predictions/per_image_nll_G1-split1` … `split9.csv.gz` | The same for the nine further fold partitions (only the seed of the split changes). | Section 6.7 |
| `data/folds/neu_cls_900_folds.csv` | Fold of each of the 900 NEU-CLS images in the ten partitions. `image_id` is the position of the image in the subset as the notebook builds it (`S_paths`); see `data/folds/README.md` for the file names. | Section 5.1 |
| `results/revision_G1/` | Report and tables of the revision analyses: permutation, Hotelling and studentized tests, leave one family out, fold dependence, per severity, family-by-severity means, repeated fold partitions; `extra/` holds the corrected amplitude-matched analysis, the training-variability shares and the per-family means. | Sections 6.4 to 6.7 |
| `results/*.json`, `results/comparisons_rerun.csv` | Every number quoted from the re-run, the reproduced image-level bootstrap and Tables 3 to 5 as markdown. | Tables 3 to 5 |
| `analysis/revision_analyses.py` | Library behind the revision analyses; both notebooks carry a copy of it. | |
| `analysis/compute_ms_numbers.py`, `repro_boot.py`, `make_tables.py`, `make_figs.py`, `independent_check.py` | Rebuild Tables 3 to 5 and Figs. 2 to 4 from `per_image_nll_G1.csv.gz`; `independent_check.py` recomputes Tables 4 and 5 without the library. | Tables 3 to 5, Figs. 2 to 4 |
| `analysis/verify_rerun.py` | Checks the notebook's report against a recomputation from the per-image tables. | |
| `analysis/compare_runs.py` | Compares two runs of the re-run notebook: per-image values, the mean NLL of each arm (Table 3) and the quantities of Table 5. | Section 5.1 |
| `analysis/reanalysis_from_reported.py` | Analyses that need only reported numbers: exact crossed-model bounds for Tables 5, 7, 8 and 10, the bound on the full crossed standard error, leave one family out from the per-family means, the power values of Table 12 and the simulation of the permutation test under a heteroskedastic null. | Sections 5.3, 6.5, 6.7, 6.10, 7.3 |
| `tables/revised/` | Tables 3 to 5, 7, 10 and 12 as revised. | |
| `tables/Table01` … `Table11` (`.csv`, `.md`, `.tex`; top level) | Tables of the submitted version, kept for the record; the submitted Table 5 carries eight wrong row labels (see the response to Reviewer 2). | |
| `sdic_tables_and_figures.ipynb`, `tables/verification.csv` | The notebook that built the submitted tables and figures. It does not re-run experiments: the measured values are entered in its Cell 2 from the submitted manuscript, everything derivable from them is recomputed, and `verification.csv` checks each recomputed value against the published one. | Submitted version |
| `table10_reproduction.ipynb` | A diagnostic of the fine-tuned interval in a draft of Table 10, [0.125, 0.782]. Its useful result is that the exact interval at ρ = 0.313 is [0.150, 0.733], the value in the submitted Table 10; the draft value matches the envelope of the three per-seed intervals printed in `PHASE3_1_selfcontained.ipynb`. Its own fine-tuning run used a reference corruption implementation instead of SDI-C, a rebuilt fold split and all 1,800 images, so its ρ values (0.47 to 0.52) are not comparable with any number in the paper, as the notebook itself states. | Section 6.10 |
| `figures/` | Fig. 1 (unchanged) and Figs. 2 to 4 from the re-run. | |

The notebooks were written with two large language models, Claude (Anthropic) and ChatGPT (OpenAI), and run by the author, as Section 5.4 of the paper documents; their text therefore addresses the author directly.

## What is not here

- Per-image values of the original runs behind Tables 6 to 11 (grid G2, Magnetic Tile, the backbone and suite comparisons, fine-tuning). Those runs did not save them; their notebooks are here with their printed outputs, and rerunning them repeats the analyses, although the re-run of Section 5.1 shows that a rerun need not reproduce the numbers exactly.
- Cached backbone features. The notebooks rebuild them.

## Reproduce

```
pip install numpy pandas scipy matplotlib
python3 -I analysis/compute_ms_numbers.py data/predictions/per_image_nll_G1.csv.gz analysis/revision_analyses.py results
python3 -I analysis/repro_boot.py data/predictions/per_image_nll_G1.csv.gz results
python3 -I analysis/make_tables.py results
python3 -I analysis/make_figs.py results/comparisons_rerun.csv results/ms_numbers.json figures
python3 -I analysis/independent_check.py data/predictions/per_image_nll_G1.csv.gz
SDIC_PER_FAMILY=results/revision_G1/extra/per_family_deltas_rerun.csv python3 -I analysis/reanalysis_from_reported.py
python3 -I analysis/compare_runs.py data/predictions/per_image_nll_G1.csv.gz data/replicate_2026-11-16/per_image_nll_G1.csv.gz results/revision_G1/summary.csv results/replicate_2026-11-16/summary.csv
```

The generalized intervals for the crossed ρ_family use 2,000,000 draws (seed 20261101); the library default of 20,000 moves the third decimal.

## License

MIT; see `LICENSE`.
