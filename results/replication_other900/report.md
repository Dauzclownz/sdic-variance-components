# Revision analyses

alpha 0.05; 20000 permutations (plain), 5000 (studentized); 20000 generalized-pivot draws; 2000 bootstrap replicates; seed 20261101.

## NEU-CLS / resnet50.a1_in1k / G1

m = 900 images, F = 6 families, 5 severity levels.

### Table 5 quantities, recomputed (two-component, Section 5.3 definitions)

| comparison | sigma_a | sigma_e | rho [95% exact] | SE ratio [95% exact] | SE ratio, bootstrap SE |
|---|---|---|---|---|---|
| C4 vs C2 | 0.635 | 1.056 | 0.266 [0.122, 0.686] | 18.07 [11.25, 44.35] | 18.69 |
| C6c vs C2 | 0.797 | 1.177 | 0.315 [0.151, 0.735] | 20.35 [12.67, 49.94] | 20.26 |
| C7 vs C2 | 0.438 | 0.620 | 0.333 [0.161, 0.750] | 21.20 [13.20, 52.04] | 21.05 |
| C7q vs C2 | 0.391 | 0.622 | 0.283 [0.132, 0.704] | 18.88 [11.75, 46.32] | 19.03 |
| C8 vs C2 | 0.794 | 2.144 | 0.120 [0.050, 0.454] | 11.15 [6.94, 27.36] | 11.37 |
| C8b vs C2 | 0.440 | 1.138 | 0.130 [0.054, 0.475] | 11.63 [7.24, 28.55] | 11.49 |
| C4 vs C5 | 0.751 | 1.234 | 0.270 [0.125, 0.691] | 18.28 [11.38, 44.87] | 18.74 |
| C6c vs C5 | 0.907 | 1.263 | 0.340 [0.166, 0.757] | 21.57 [13.43, 52.93] | 21.82 |
| C7 vs C5 | 0.567 | 1.015 | 0.238 [0.107, 0.653] | 16.79 [10.45, 41.20] | 16.59 |
| C7q vs C5 | 0.522 | 1.009 | 0.211 [0.094, 0.618] | 15.57 [9.69, 38.21] | 15.64 |
| C8 vs C5 | 0.804 | 1.536 | 0.215 [0.095, 0.623] | 15.73 [9.79, 38.60] | 15.84 |
| C8b vs C5 | 0.448 | 0.746 | 0.265 [0.122, 0.686] | 18.06 [11.24, 44.32] | 18.84 |
| C4 vs C5o | 0.601 | 0.962 | 0.281 [0.131, 0.702] | 18.77 [11.69, 46.07] | 19.35 |
| C6c vs C5o | 0.763 | 1.065 | 0.339 [0.165, 0.756] | 21.50 [13.39, 52.77] | 21.41 |
| C7 vs C5o | 0.404 | 0.549 | 0.351 [0.173, 0.765] | 22.08 [13.75, 54.20] | 22.08 |
| C7q vs C5o | 0.357 | 0.550 | 0.297 [0.140, 0.718] | 19.51 [12.15, 47.88] | 19.25 |
| C8 vs C5o | 0.747 | 1.958 | 0.127 [0.053, 0.469] | 11.49 [7.15, 28.20] | 11.71 |
| C8b vs C5o | 0.391 | 0.974 | 0.139 [0.058, 0.494] | 12.08 [7.52, 29.65] | 12.02 |

### Crossed decomposition and tests of the family effect

| comparison | sigma_a | sigma_b | sigma_e | rho_family [95% GCI] | F test p | permutation p (obs/median) | Hotelling p | studentized perm p | full SE / family SE |
|---|---|---|---|---|---|---|---|---|---|
| C4 vs C2 | 0.635 | 0.000 | 1.134 | 0.239 [0.107, 0.655] | 6.8e-264 | 5.0e-05 (247.5) | 4.7e-74 | 2.0e-04 | 1.0000 |
| C6c vs C2 | 0.797 | 0.000 | 1.262 | 0.285 [0.132, 0.707] | 0.0e+00 | 5.0e-05 (296.0) | 6.7e-84 | 2.0e-04 | 1.0000 |
| C7 vs C2 | 0.438 | 0.000 | 0.710 | 0.275 [0.127, 0.697] | 2.8e-312 | 5.0e-05 (286.0) | 1.3e-93 | 2.0e-04 | 1.0000 |
| C7q vs C2 | 0.391 | 0.000 | 0.691 | 0.242 [0.109, 0.660] | 1.7e-268 | 5.0e-05 (250.9) | 2.7e-76 | 2.0e-04 | 1.0000 |
| C8 vs C2 | 0.795 | 0.601 | 1.559 | 0.185 [0.079, 0.579] | 1.7e-223 | 5.0e-05 (215.6) | 9.9e-70 | 2.0e-04 | 1.0019 |
| C8b vs C2 | 0.440 | 0.257 | 0.948 | 0.167 [0.071, 0.550] | 1.4e-188 | 5.0e-05 (184.8) | 1.9e-68 | 2.0e-04 | 1.0011 |
| C4 vs C5 | 0.751 | 0.000 | 1.501 | 0.200 [0.087, 0.603] | 1.1e-215 | 5.0e-05 (207.7) | 1.8e-59 | 2.0e-04 | 1.0000 |
| C6c vs C5 | 0.906 | 0.000 | 1.620 | 0.238 [0.107, 0.655] | 1.9e-263 | 5.0e-05 (247.1) | 8.1e-74 | 2.0e-04 | 1.0000 |
| C7 vs C5 | 0.566 | 0.000 | 1.180 | 0.187 [0.081, 0.583] | 3.4e-200 | 5.0e-05 (194.9) | 2.3e-71 | 2.0e-04 | 1.0000 |
| C7q vs C5 | 0.522 | 0.000 | 1.150 | 0.171 [0.073, 0.556] | 6.4e-181 | 5.0e-05 (177.5) | 2.9e-58 | 2.0e-04 | 1.0000 |
| C8 vs C5 | 0.804 | 0.306 | 1.341 | 0.255 [0.115, 0.675] | 8.6e-298 | 5.0e-05 (274.8) | 1.6e-64 | 2.0e-04 | 1.0005 |
| C8b vs C5 | 0.448 | 0.000 | 0.872 | 0.209 [0.091, 0.616] | 1.1e-226 | 5.0e-05 (216.2) | 4.0e-56 | 2.0e-04 | 1.0000 |
| C4 vs C5o | 0.601 | 0.000 | 1.113 | 0.226 [0.100, 0.639] | 2.1e-247 | 5.0e-05 (234.8) | 1.2e-68 | 2.0e-04 | 1.0000 |
| C6c vs C5o | 0.763 | 0.000 | 1.237 | 0.275 [0.127, 0.697] | 5.4e-312 | 5.0e-05 (285.7) | 1.5e-81 | 2.0e-04 | 1.0000 |
| C7 vs C5o | 0.404 | 0.000 | 0.697 | 0.251 [0.114, 0.671] | 2.7e-280 | 5.0e-05 (261.1) | 6.2e-88 | 2.0e-04 | 1.0000 |
| C7q vs C5o | 0.357 | 0.000 | 0.673 | 0.220 [0.097, 0.631] | 6.3e-240 | 5.0e-05 (227.0) | 7.8e-71 | 2.0e-04 | 1.0000 |
| C8 vs C5o | 0.748 | 0.527 | 1.473 | 0.186 [0.080, 0.582] | 5.0e-222 | 5.0e-05 (213.7) | 2.1e-67 | 2.0e-04 | 1.0016 |
| C8b vs C5o | 0.391 | 0.184 | 0.863 | 0.164 [0.069, 0.544] | 2.4e-180 | 5.0e-05 (176.1) | 3.3e-66 | 2.0e-04 | 1.0007 |

### Intervals for the mean difference

| comparison | mean | image bootstrap 95% | family t 95% | full crossed 95% (df) |
|---|---|---|---|---|
| C4 vs C2 | 0.1973 | [0.1700, 0.2244] | [-0.4703, 0.8649] | [-0.4703, 0.8649] (5.0) |
| C6c vs C2 | 0.2671 | [0.2356, 0.2987] | [-0.5707, 1.1048] | [-0.5707, 1.1048] (5.0) |
| C7 vs C2 | 0.1136 | [0.0967, 0.1300] | [-0.3463, 0.5735] | [-0.3463, 0.5735] (5.0) |
| C7q vs C2 | 0.0955 | [0.0794, 0.1123] | [-0.3150, 0.5061] | [-0.3150, 0.5061] (5.0) |
| C8 vs C2 | 0.4447 | [0.3887, 0.5008] | [-0.3916, 1.2809] | [-0.3913, 1.2806] (5.0) |
| C8b vs C2 | 0.2181 | [0.1874, 0.2489] | [-0.2449, 0.6810] | [-0.2448, 0.6809] (5.0) |
| C4 vs C5 | 0.0616 | [0.0301, 0.0944] | [-0.7278, 0.8511] | [-0.7278, 0.8511] (5.0) |
| C6c vs C5 | 0.1314 | [0.0979, 0.1645] | [-0.8213, 1.0841] | [-0.8213, 1.0841] (5.0) |
| C7 vs C5 | -0.0221 | [-0.0516, 0.0032] | [-0.6179, 0.5737] | [-0.6179, 0.5737] (5.0) |
| C7q vs C5 | -0.0402 | [-0.0675, -0.0139] | [-0.5894, 0.5091] | [-0.5894, 0.5091] (5.0) |
| C8 vs C5 | 0.3090 | [0.2688, 0.3502] | [-0.5364, 1.1543] | [-0.5363, 1.1543] (5.0) |
| C8b vs C5 | 0.0824 | [0.0630, 0.1012] | [-0.3887, 0.5534] | [-0.3887, 0.5534] (5.0) |
| C4 vs C5o | 0.1501 | [0.1253, 0.1751] | [-0.4817, 0.7820] | [-0.4817, 0.7820] (5.0) |
| C6c vs C5o | 0.2199 | [0.1913, 0.2484] | [-0.5816, 1.0214] | [-0.5816, 1.0214] (5.0) |
| C7 vs C5o | 0.0664 | [0.0514, 0.0807] | [-0.3581, 0.4909] | [-0.3581, 0.4909] (5.0) |
| C7q vs C5o | 0.0483 | [0.0335, 0.0632] | [-0.3269, 0.4236] | [-0.3269, 0.4236] (5.0) |
| C8 vs C5o | 0.3975 | [0.3461, 0.4486] | [-0.3894, 1.1844] | [-0.3892, 1.1842] (5.0) |
| C8b vs C5o | 0.1709 | [0.1448, 0.1970] | [-0.2407, 0.5824] | [-0.2406, 0.5824] (5.0) |

### Leave one family out and fold dependence

| comparison | smallest LOFO family p (family omitted) | smallest LOFO SE ratio | fold ICC [upper] | design effect [upper] | SE ratio, fold-adjusted [conservative] |
|---|---|---|---|---|---|
| C4 vs C2 | 0.046 (vignetting) | 5.62 | 0.2293 [0.7142] | 42.05 [128.85] | 2.79 [1.59] |
| C6c vs C2 | 0.045 (vignetting) | 4.83 | 0.0915 [0.4661] | 17.39 [84.44] | 4.88 [2.21] |
| C7 vs C2 | 0.041 (vignetting) | 5.84 | 0.0554 [0.3444] | 10.92 [62.65] | 6.42 [2.68] |
| C7q vs C2 | 0.047 (vignetting) | 6.07 | 0.1200 [0.5386] | 22.48 [97.41] | 3.98 [1.91] |
| C8 vs C2 | 0.208 (shot_noise) | 7.83 | 0.0993 [0.4877] | 18.78 [88.29] | 2.57 [1.19] |
| C8b vs C2 | 0.228 (shot_noise) | 10.21 | 0.0300 [0.2283] | 6.37 [41.87] | 4.61 [1.80] |
| C4 vs C5 | 0.129 (vignetting) | 6.86 | 0.2487 [0.7351] | 45.51 [132.59] | 2.71 [1.59] |
| C6c vs C5 | 0.133 (vignetting) | 6.76 | 0.1965 [0.6734] | 36.17 [121.53] | 3.59 [1.96] |
| C7 vs C5 | 0.126 (vignetting) | 6.77 | 0.1601 [0.6177] | 29.66 [111.57] | 3.08 [1.59] |
| C7q vs C5 | 0.123 (vignetting) | 6.84 | 0.1763 [0.6440] | 32.55 [116.27] | 2.73 [1.44] |
| C8 vs C5 | 0.368 (shot_noise) | 4.15 | 0.1807 [0.6507] | 33.35 [117.48] | 2.72 [1.45] |
| C8b vs C5 | 0.004 (vignetting) | 2.02 | 0.1592 [0.6162] | 29.50 [111.29] | 3.33 [1.71] |
| C4 vs C5o | 0.026 (vignetting) | 5.10 | 0.2922 [0.7754] | 53.30 [139.79] | 2.57 [1.59] |
| C6c vs C5o | 0.021 (vignetting) | 4.31 | 0.1403 [0.5814] | 26.11 [105.07] | 4.21 [2.10] |
| C7 vs C5o | 0.021 (vignetting) | 4.90 | 0.1280 [0.5563] | 23.91 [100.57] | 4.52 [2.20] |
| C7q vs C5o | 0.023 (vignetting) | 5.16 | 0.1928 [0.6683] | 35.51 [120.62] | 3.27 [1.78] |
| C8 vs C5o | 0.214 (shot_noise) | 7.74 | 0.1137 [0.5240] | 21.35 [94.79] | 2.49 [1.18] |
| C8b vs C5o | 0.241 (shot_noise) | 10.03 | 0.0306 [0.2315] | 6.48 [42.43] | 4.75 [1.85] |

Fold component as a share of the family-level variance: C4 vs C2 0.132 [upper 1.112]; C6c vs C2 0.041 [upper 0.351]; C7 vs C2 0.022 [upper 0.201]; C7q vs C2 0.062 [upper 0.532]; C8 vs C2 0.147 [upper 1.267]; C8b vs C2 0.040 [upper 0.384]; C4 vs C5 0.141 [upper 1.181]; C6c vs C5 0.079 [upper 0.667]; C7 vs C5 0.106 [upper 0.895]; C7q vs C5 0.136 [upper 1.147]; C8 vs C5 0.136 [upper 1.152]; C8b vs C5 0.091 [upper 0.769]; C4 vs C5o 0.158 [upper 1.325]; C6c vs C5o 0.056 [upper 0.478]; C7 vs C5o 0.048 [upper 0.414]; C7q vs C5o 0.095 [upper 0.800]; C8 vs C5o 0.159 [upper 1.361]; C8b vs C5o 0.038 [upper 0.362].

Per-comparison tables (leave one family out, per severity, amplitude matched, family x severity means) are in the comparison folders of the output directory.

## NEU-CLS / resnet50.a1_in1k / G1-split1

Repeated fold partition, light mode: only the mean, the standard errors and the fold check were computed. See the repeated-partition table at the end.

## NEU-CLS / resnet50.a1_in1k / G1-split2

Repeated fold partition, light mode: only the mean, the standard errors and the fold check were computed. See the repeated-partition table at the end.

## NEU-CLS / resnet50.a1_in1k / G1-split3

Repeated fold partition, light mode: only the mean, the standard errors and the fold check were computed. See the repeated-partition table at the end.

## NEU-CLS / resnet50.a1_in1k / G1-split4

Repeated fold partition, light mode: only the mean, the standard errors and the fold check were computed. See the repeated-partition table at the end.

## NEU-CLS / resnet50.a1_in1k / G1-split5

Repeated fold partition, light mode: only the mean, the standard errors and the fold check were computed. See the repeated-partition table at the end.

## NEU-CLS / resnet50.a1_in1k / G1-split6

Repeated fold partition, light mode: only the mean, the standard errors and the fold check were computed. See the repeated-partition table at the end.

## NEU-CLS / resnet50.a1_in1k / G1-split7

Repeated fold partition, light mode: only the mean, the standard errors and the fold check were computed. See the repeated-partition table at the end.

## NEU-CLS / resnet50.a1_in1k / G1-split8

Repeated fold partition, light mode: only the mean, the standard errors and the fold check were computed. See the repeated-partition table at the end.

## NEU-CLS / resnet50.a1_in1k / G1-split9

Repeated fold partition, light mode: only the mean, the standard errors and the fold check were computed. See the repeated-partition table at the end.

## Repeated fold partitions

| dataset / backbone / grid | comparison | partitions | SD of the mean over partitions | SE image | SE family | SD / SE image | SD / SE family | SE ratio range |
|---|---|---|---|---|---|---|---|---|
| NEU-CLS / resnet50.a1_in1k / G1 | C4 vs C2 | 10 | 0.0898 | 0.0139 | 0.2185 | 6.45 | 0.41 | 10.91 to 21.72 |
| NEU-CLS / resnet50.a1_in1k / G1 | C6c vs C2 | 10 | 0.1166 | 0.0166 | 0.3077 | 7.05 | 0.38 | 12.61 to 23.18 |
| NEU-CLS / resnet50.a1_in1k / G1 | C7 vs C2 | 10 | 0.0591 | 0.0096 | 0.1727 | 6.13 | 0.34 | 12.78 to 21.99 |
| NEU-CLS / resnet50.a1_in1k / G1 | C7q vs C2 | 10 | 0.0512 | 0.0090 | 0.1399 | 5.71 | 0.37 | 11.14 to 21.59 |
| NEU-CLS / resnet50.a1_in1k / G1 | C8 vs C2 | 10 | 0.1303 | 0.0243 | 0.2557 | 5.36 | 0.51 | 7.61 to 16.91 |
| NEU-CLS / resnet50.a1_in1k / G1 | C8b vs C2 | 10 | 0.0572 | 0.0155 | 0.1653 | 3.69 | 0.35 | 8.16 to 13.44 |
| NEU-CLS / resnet50.a1_in1k / G1 | C4 vs C5 | 10 | 0.0845 | 0.0160 | 0.2511 | 5.30 | 0.34 | 10.59 to 25.34 |
| NEU-CLS / resnet50.a1_in1k / G1 | C6c vs C5 | 10 | 0.1176 | 0.0174 | 0.3358 | 6.77 | 0.35 | 12.14 to 26.93 |
| NEU-CLS / resnet50.a1_in1k / G1 | C7 vs C5 | 10 | 0.0633 | 0.0134 | 0.2041 | 4.72 | 0.31 | 9.79 to 22.32 |
| NEU-CLS / resnet50.a1_in1k / G1 | C7q vs C5 | 10 | 0.0512 | 0.0131 | 0.1765 | 3.90 | 0.29 | 8.91 to 20.16 |
| NEU-CLS / resnet50.a1_in1k / G1 | C8 vs C5 | 10 | 0.1217 | 0.0185 | 0.2483 | 6.56 | 0.49 | 8.42 to 23.25 |
| NEU-CLS / resnet50.a1_in1k / G1 | C8b vs C5 | 10 | 0.0534 | 0.0104 | 0.1530 | 5.13 | 0.35 | 10.03 to 22.43 |
| NEU-CLS / resnet50.a1_in1k / G1 | C4 vs C5o | 10 | 0.0904 | 0.0129 | 0.2074 | 7.01 | 0.44 | 10.15 to 22.95 |
| NEU-CLS / resnet50.a1_in1k / G1 | C6c vs C5o | 10 | 0.1145 | 0.0152 | 0.2955 | 7.55 | 0.39 | 10.44 to 25.39 |
| NEU-CLS / resnet50.a1_in1k / G1 | C7 vs C5o | 10 | 0.0571 | 0.0090 | 0.1601 | 6.37 | 0.36 | 9.03 to 23.77 |
| NEU-CLS / resnet50.a1_in1k / G1 | C7q vs C5o | 10 | 0.0520 | 0.0085 | 0.1290 | 6.15 | 0.40 | 8.84 to 23.11 |
| NEU-CLS / resnet50.a1_in1k / G1 | C8 vs C5o | 10 | 0.1300 | 0.0223 | 0.2375 | 5.84 | 0.55 | 7.08 to 17.78 |
| NEU-CLS / resnet50.a1_in1k / G1 | C8b vs C5o | 10 | 0.0568 | 0.0135 | 0.1462 | 4.22 | 0.39 | 7.19 to 14.40 |
