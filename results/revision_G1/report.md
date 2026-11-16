# Revision analyses

alpha 0.05; 20000 permutations (plain), 5000 (studentized); 20000 generalized-pivot draws; 2000 bootstrap replicates; seed 20261101.

## NEU-CLS / resnet50.a1_in1k / G1

m = 900 images, F = 6 families, 5 severity levels.

### Table 5 quantities, recomputed (two-component, Section 5.3 definitions)

| comparison | sigma_a | sigma_e | rho [95% exact] | SE ratio [95% exact] | SE ratio, bootstrap SE |
|---|---|---|---|---|---|
| C4 vs C2 | 0.390 | 0.957 | 0.142 [0.060, 0.501] | 12.26 [7.63, 30.08] | 12.64 |
| C6c vs C2 | 0.765 | 1.322 | 0.251 [0.114, 0.669] | 17.39 [10.83, 42.68] | 17.57 |
| C7 vs C2 | 0.418 | 0.733 | 0.245 [0.111, 0.663] | 17.13 [10.67, 42.04] | 17.34 |
| C7q vs C2 | 0.249 | 0.589 | 0.152 [0.064, 0.520] | 12.73 [7.92, 31.23] | 13.04 |
| C8 vs C2 | 0.400 | 1.944 | 0.041 [0.016, 0.207] | 6.26 [3.90, 15.36] | 6.48 |
| C8b vs C2 | 0.250 | 1.106 | 0.048 [0.019, 0.238] | 6.84 [4.26, 16.79] | 7.02 |
| C4 vs C5 | 0.457 | 1.139 | 0.139 [0.058, 0.494] | 12.08 [7.52, 29.66] | 12.32 |
| C6c vs C5 | 0.825 | 1.261 | 0.300 [0.142, 0.721] | 19.66 [12.24, 48.24] | 20.38 |
| C7 vs C5 | 0.490 | 1.129 | 0.158 [0.067, 0.532] | 13.05 [8.12, 32.03] | 13.30 |
| C7q vs C5 | 0.326 | 1.084 | 0.083 [0.033, 0.355] | 9.08 [5.66, 22.29] | 9.05 |
| C8 vs C5 | 0.346 | 1.137 | 0.085 [0.034, 0.360] | 9.18 [5.72, 22.53] | 9.61 |
| C8b vs C5 | 0.226 | 0.608 | 0.121 [0.050, 0.456] | 11.20 [6.97, 27.48] | 11.15 |
| C4 vs C5o | 0.397 | 0.993 | 0.137 [0.058, 0.491] | 12.02 [7.48, 29.50] | 12.11 |
| C6c vs C5o | 0.769 | 1.301 | 0.259 [0.119, 0.679] | 17.76 [11.06, 43.59] | 18.12 |
| C7 vs C5o | 0.425 | 0.832 | 0.207 [0.091, 0.612] | 15.36 [9.56, 37.71] | 15.24 |
| C7q vs C5o | 0.259 | 0.718 | 0.115 [0.047, 0.442] | 10.88 [6.77, 26.70] | 11.09 |
| C8 vs C5o | 0.363 | 1.806 | 0.039 [0.015, 0.199] | 6.12 [3.81, 15.01] | 6.19 |
| C8b vs C5o | 0.219 | 1.011 | 0.045 [0.017, 0.223] | 6.57 [4.09, 16.13] | 6.72 |

### Crossed decomposition and tests of the family effect

| comparison | sigma_a | sigma_b | sigma_e | rho_family [95% GCI] | F test p | permutation p (obs/median) | Hotelling p | studentized perm p | full SE / family SE |
|---|---|---|---|---|---|---|---|---|---|
| C4 vs C2 | 0.390 | 0.000 | 1.012 | 0.129 [0.053, 0.474] | 4.6e-133 | 5.0e-05 (133.4) | 7.0e-78 | 2.0e-04 | 1.0000 |
| C6c vs C2 | 0.765 | 0.000 | 1.378 | 0.236 [0.105, 0.651] | 3.3e-260 | 5.0e-05 (244.6) | 5.0e-66 | 2.0e-04 | 1.0000 |
| C7 vs C2 | 0.418 | 0.000 | 0.775 | 0.225 [0.100, 0.638] | 1.8e-246 | 5.0e-05 (233.5) | 1.4e-72 | 2.0e-04 | 1.0000 |
| C7q vs C2 | 0.249 | 0.000 | 0.624 | 0.137 [0.057, 0.492] | 3.5e-142 | 5.0e-05 (142.7) | 3.1e-78 | 2.0e-04 | 1.0000 |
| C8 vs C2 | 0.403 | 0.562 | 1.373 | 0.069 [0.027, 0.311] | 3.8e-79 | 5.0e-05 (82.3) | 3.7e-32 | 2.0e-04 | 1.0064 |
| C8b vs C2 | 0.251 | 0.279 | 0.871 | 0.070 [0.027, 0.315] | 2.8e-76 | 5.0e-05 (78.9) | 8.1e-38 | 2.0e-04 | 1.0041 |
| C4 vs C5 | 0.456 | 0.000 | 1.331 | 0.105 [0.043, 0.418] | 6.3e-107 | 5.0e-05 (108.9) | 1.5e-29 | 2.0e-04 | 1.0000 |
| C6c vs C5 | 0.825 | 0.000 | 1.665 | 0.197 [0.086, 0.598] | 4.0e-212 | 5.0e-05 (205.0) | 5.6e-63 | 2.0e-04 | 1.0000 |
| C7 vs C5 | 0.490 | 0.000 | 1.179 | 0.147 [0.062, 0.511] | 1.7e-153 | 5.0e-05 (152.3) | 2.7e-60 | 2.0e-04 | 1.0000 |
| C7q vs C5 | 0.326 | 0.105 | 1.052 | 0.087 [0.035, 0.368] | 4.7e-88 | 5.0e-05 (91.4) | 8.0e-34 | 2.0e-04 | 1.0003 |
| C8 vs C5 | 0.347 | 0.277 | 0.913 | 0.117 [0.048, 0.446] | 7.6e-130 | 5.0e-05 (130.6) | 4.1e-35 | 2.0e-04 | 1.0021 |
| C8b vs C5 | 0.226 | 0.000 | 0.612 | 0.120 [0.049, 0.453] | 2.9e-123 | 5.0e-05 (124.8) | 1.2e-34 | 2.0e-04 | 1.0000 |
| C4 vs C5o | 0.396 | 0.000 | 1.075 | 0.120 [0.049, 0.453] | 9.0e-123 | 5.0e-05 (123.9) | 1.2e-41 | 2.0e-04 | 1.0000 |
| C6c vs C5o | 0.769 | 0.000 | 1.427 | 0.225 [0.100, 0.638] | 1.5e-246 | 5.0e-05 (232.9) | 1.5e-59 | 2.0e-04 | 1.0000 |
| C7 vs C5o | 0.425 | 0.000 | 0.864 | 0.195 [0.084, 0.594] | 1.3e-209 | 5.0e-05 (201.9) | 1.9e-63 | 2.0e-04 | 1.0000 |
| C7q vs C5o | 0.259 | 0.000 | 0.721 | 0.114 [0.046, 0.439] | 8.1e-117 | 5.0e-05 (118.7) | 2.5e-45 | 2.0e-04 | 1.0000 |
| C8 vs C5o | 0.365 | 0.502 | 1.323 | 0.063 [0.024, 0.290] | 2.0e-70 | 5.0e-05 (73.5) | 3.5e-33 | 2.0e-04 | 1.0062 |
| C8b vs C5o | 0.220 | 0.228 | 0.843 | 0.059 [0.023, 0.280] | 8.8e-63 | 5.0e-05 (66.5) | 1.1e-35 | 2.0e-04 | 1.0035 |

### Intervals for the mean difference

| comparison | mean | image bootstrap 95% | family t 95% | full crossed 95% (df) |
|---|---|---|---|---|
| C4 vs C2 | 0.0865 | [0.0624, 0.1119] | [-0.3239, 0.4969] | [-0.3239, 0.4969] (5.0) |
| C6c vs C2 | 0.2383 | [0.2039, 0.2737] | [-0.5660, 1.0426] | [-0.5660, 1.0426] (5.0) |
| C7 vs C2 | 0.0901 | [0.0714, 0.1100] | [-0.3490, 0.5293] | [-0.3490, 0.5293] (5.0) |
| C7q vs C2 | 0.0284 | [0.0134, 0.0440] | [-0.2337, 0.2904] | [-0.2337, 0.2904] (5.0) |
| C8 vs C2 | 0.2275 | [0.1781, 0.2782] | [-0.1980, 0.6531] | [-0.1975, 0.6526] (5.1) |
| C8b vs C2 | 0.0930 | [0.0647, 0.1222] | [-0.1717, 0.3578] | [-0.1715, 0.3576] (5.1) |
| C4 vs C5 | -0.0026 | [-0.0328, 0.0267] | [-0.4839, 0.4787] | [-0.4839, 0.4787] (5.0) |
| C6c vs C5 | 0.1492 | [0.1164, 0.1813] | [-0.7182, 1.0166] | [-0.7182, 1.0166] (5.0) |
| C7 vs C5 | 0.0011 | [-0.0288, 0.0303] | [-0.5145, 0.5167] | [-0.5145, 0.5167] (5.0) |
| C7q vs C5 | -0.0607 | [-0.0897, -0.0317] | [-0.4050, 0.2837] | [-0.4050, 0.2836] (5.0) |
| C8 vs C5 | 0.1385 | [0.1098, 0.1677] | [-0.2267, 0.5037] | [-0.2266, 0.5036] (5.0) |
| C8b vs C5 | 0.0040 | [-0.0122, 0.0204] | [-0.2343, 0.2423] | [-0.2343, 0.2423] (5.0) |
| C4 vs C5o | 0.0085 | [-0.0174, 0.0351] | [-0.4091, 0.4261] | [-0.4091, 0.4261] (5.0) |
| C6c vs C5o | 0.1603 | [0.1264, 0.1945] | [-0.6478, 0.9684] | [-0.6478, 0.9684] (5.0) |
| C7 vs C5o | 0.0122 | [-0.0099, 0.0348] | [-0.4352, 0.4595] | [-0.4352, 0.4595] (5.0) |
| C7q vs C5o | -0.0496 | [-0.0685, -0.0309] | [-0.3227, 0.2235] | [-0.3227, 0.2235] (5.0) |
| C8 vs C5o | 0.1496 | [0.1020, 0.1972] | [-0.2368, 0.5359] | [-0.2363, 0.5354] (5.1) |
| C8b vs C5o | 0.0151 | [-0.0109, 0.0419] | [-0.2174, 0.2475] | [-0.2172, 0.2473] (5.1) |

### Leave one family out and fold dependence

| comparison | smallest LOFO family p (family omitted) | smallest LOFO SE ratio | fold ICC [upper] | design effect [upper] | SE ratio, fold-adjusted [conservative] |
|---|---|---|---|---|---|
| C4 vs C2 | 0.031 (vignetting) | 5.00 | 0.3155 [0.7938] | 57.48 [143.09] | 1.62 [1.02] |
| C6c vs C2 | 0.016 (vignetting) | 3.17 | 0.2223 [0.7062] | 40.80 [127.40] | 2.72 [1.54] |
| C7 vs C2 | 0.016 (vignetting) | 3.41 | 0.1463 [0.5930] | 27.19 [107.14] | 3.29 [1.66] |
| C7q vs C2 | 0.030 (vignetting) | 4.74 | 0.2563 [0.7429] | 46.88 [133.97] | 1.86 [1.10] |
| C8 vs C2 | 0.183 (shot_noise) | 5.81 | 0.1324 [0.5655] | 24.70 [102.22] | 1.26 [0.62] |
| C8b vs C2 | 0.300 (contrast_loss) | 6.29 | 0.1472 [0.5947] | 27.35 [107.45] | 1.31 [0.66] |
| C4 vs C5 | 0.086 (vignetting) | 4.49 | 0.1773 [0.6456] | 32.74 [116.56] | 2.11 [1.12] |
| C6c vs C5 | 0.108 (vignetting) | 4.97 | 0.1242 [0.5480] | 23.24 [99.10] | 4.08 [1.97] |
| C7 vs C5 | 0.101 (vignetting) | 4.93 | 0.0420 [0.2871] | 8.52 [52.39] | 4.47 [1.80] |
| C7q vs C5 | 0.086 (vignetting) | 4.49 | 0.0867 [0.4522] | 16.53 [81.94] | 2.23 [1.00] |
| C8 vs C5 | 0.298 (shot_noise) | 7.20 | 0.1991 [0.6769] | 36.64 [122.16] | 1.52 [0.83] |
| C8b vs C5 | 0.002 (vignetting) | 1.66 | 0.2600 [0.7465] | 47.55 [134.62] | 1.62 [0.96] |
| C4 vs C5o | 0.032 (vignetting) | 4.78 | 0.2855 [0.7697] | 52.11 [138.78] | 1.66 [1.02] |
| C6c vs C5o | 0.034 (vignetting) | 4.70 | 0.1833 [0.6546] | 33.81 [118.18] | 3.05 [1.63] |
| C7 vs C5o | 0.031 (vignetting) | 4.75 | 0.0707 [0.4008] | 13.65 [72.75] | 4.16 [1.80] |
| C7q vs C5o | 0.029 (vignetting) | 4.64 | 0.1604 [0.6182] | 29.71 [111.65] | 2.00 [1.03] |
| C8 vs C5o | 0.215 (shot_noise) | 5.26 | 0.1328 [0.5664] | 24.78 [102.39] | 1.23 [0.60] |
| C8b vs C5o | 0.399 (vignetting) | 4.85 | 0.1408 [0.5825] | 26.21 [105.26] | 1.28 [0.64] |

Fold component as a share of the family-level variance: C4 vs C2 0.403 [upper 3.368]; C6c vs C2 0.138 [upper 1.164]; C7 vs C2 0.092 [upper 0.786]; C7q vs C2 0.300 [upper 2.516]; C8 vs C2 0.625 [upper 5.329]; C8b vs C2 0.583 [upper 4.957]; C4 vs C5 0.227 [upper 1.915]; C6c vs C5 0.059 [upper 0.507]; C7 vs C5 0.045 [upper 0.411]; C7q vs C5 0.193 [upper 1.673]; C8 vs C5 0.443 [upper 3.729]; C8b vs C5 0.394 [upper 3.300]; C4 vs C5o 0.377 [upper 3.156]; C6c vs C5o 0.109 [upper 0.916]; C7 vs C5o 0.055 [upper 0.481]; C7q vs C5o 0.252 [upper 2.135]; C8 vs C5o 0.657 [upper 5.600]; C8b vs C5o 0.604 [upper 5.141].

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
| NEU-CLS / resnet50.a1_in1k / G1 | C4 vs C2 | 10 | 0.0639 | 0.0114 | 0.1206 | 5.62 | 0.53 | 2.63 to 13.36 |
| NEU-CLS / resnet50.a1_in1k / G1 | C6c vs C2 | 10 | 0.0690 | 0.0191 | 0.3324 | 3.61 | 0.21 | 13.45 to 19.74 |
| NEU-CLS / resnet50.a1_in1k / G1 | C7 vs C2 | 10 | 0.0492 | 0.0109 | 0.1741 | 4.51 | 0.28 | 11.28 to 19.85 |
| NEU-CLS / resnet50.a1_in1k / G1 | C7q vs C2 | 10 | 0.0540 | 0.0083 | 0.0807 | 6.53 | 0.67 | 3.75 to 13.12 |
| NEU-CLS / resnet50.a1_in1k / G1 | C8 vs C2 | 10 | 0.1020 | 0.0263 | 0.2063 | 3.88 | 0.49 | 6.26 to 9.97 |
| NEU-CLS / resnet50.a1_in1k / G1 | C8b vs C2 | 10 | 0.0527 | 0.0164 | 0.1402 | 3.22 | 0.38 | 6.58 to 11.06 |
| NEU-CLS / resnet50.a1_in1k / G1 | C4 vs C5 | 10 | 0.0988 | 0.0188 | 0.1930 | 5.26 | 0.51 | 5.93 to 13.57 |
| NEU-CLS / resnet50.a1_in1k / G1 | C6c vs C5 | 10 | 0.1023 | 0.0211 | 0.3813 | 4.84 | 0.27 | 15.00 to 22.12 |
| NEU-CLS / resnet50.a1_in1k / G1 | C7 vs C5 | 10 | 0.0906 | 0.0175 | 0.2372 | 5.17 | 0.38 | 11.35 to 17.15 |
| NEU-CLS / resnet50.a1_in1k / G1 | C7q vs C5 | 10 | 0.0921 | 0.0175 | 0.1614 | 5.27 | 0.57 | 6.24 to 11.41 |
| NEU-CLS / resnet50.a1_in1k / G1 | C8 vs C5 | 10 | 0.0815 | 0.0169 | 0.1432 | 4.83 | 0.57 | 5.21 to 11.46 |
| NEU-CLS / resnet50.a1_in1k / G1 | C8b vs C5 | 10 | 0.0531 | 0.0096 | 0.0839 | 5.52 | 0.63 | 6.24 to 13.09 |
| NEU-CLS / resnet50.a1_in1k / G1 | C4 vs C5o | 10 | 0.0646 | 0.0115 | 0.1171 | 5.60 | 0.55 | 2.96 to 14.04 |
| NEU-CLS / resnet50.a1_in1k / G1 | C6c vs C5o | 10 | 0.0797 | 0.0179 | 0.3266 | 4.44 | 0.24 | 14.34 to 20.80 |
| NEU-CLS / resnet50.a1_in1k / G1 | C7 vs C5o | 10 | 0.0586 | 0.0106 | 0.1688 | 5.54 | 0.35 | 10.35 to 19.19 |
| NEU-CLS / resnet50.a1_in1k / G1 | C7q vs C5o | 10 | 0.0567 | 0.0088 | 0.0770 | 6.47 | 0.74 | 2.71 to 11.94 |
| NEU-CLS / resnet50.a1_in1k / G1 | C8 vs C5o | 10 | 0.1062 | 0.0240 | 0.1819 | 4.42 | 0.58 | 5.98 to 9.64 |
| NEU-CLS / resnet50.a1_in1k / G1 | C8b vs C5o | 10 | 0.0609 | 0.0142 | 0.1145 | 4.29 | 0.53 | 5.40 to 10.83 |
