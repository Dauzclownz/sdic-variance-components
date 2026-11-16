# Fold assignments

`neu_cls_900_folds.csv` gives, for each of the 900 NEU-CLS images used in the paper, its test fold (0 to 4) in the partition of the re-run (`fold_G1`) and in the nine further partitions (`fold_G1-split1` to `fold_G1-split9`).

`image_id` is the position of the image in the class-stratified subset (150 per class, seed 20260821) exactly as the notebooks build it in the variable `S_paths`. The file `neu_cls_900_subset.csv`, which maps each position to the NEU-CLS file name and class, is written by this cell, run after the feature-extraction cell of `notebooks/PHASE0_11_family_uncertainty_revision.ipynb`:

```python
import pandas as pd
pd.DataFrame({"image_id": range(len(S_paths)),
              "file": [p.name for p in S_paths],
              "class": [p.parent.name for p in S_paths]}).to_csv("neu_cls_900_subset.csv", index=False)
```

Magnetic Tile uses all 1,344 images; its five folds are built in `PHASE2_second_dataset_and_span.ipynb` by `StratifiedKFold(5, shuffle=True, random_state=20260821)`.
