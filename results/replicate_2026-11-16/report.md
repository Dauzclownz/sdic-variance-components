# Revision analyses

alpha 0.05; 20000 permutations (plain), 5000 (studentized); 20000 generalized-pivot draws; 2000 bootstrap replicates; seed 20261101.

## NEU-CLS / resnet50.a1_in1k / G1

m = 900 images, F = 6 families, 5 severity levels.

### Table 5 quantities, recomputed (two-component, Section 5.3 definitions)

| comparison | sigma_a | sigma_e | rho [95% exact] | SE ratio [95% exact] | SE ratio, bootstrap SE |
|---|---|---|---|---|---|
| C4 vs C2 | 0.386 | 0.952 | 0.141 [0.059, 0.499] | 12.20 [7.59, 29.93] | 12.56 |
| C6c vs C2 | 0.764 | 1.321 | 0.251 [0.114, 0.669] | 17.38 [10.82, 42.65] | 17.60 |
| C7 vs C2 | 0.417 | 0.733 | 0.245 [0.111, 0.662] | 17.12 [10.66, 42.02] | 17.35 |
| C7q vs C2 | 0.248 | 0.588 | 0.151 [0.064, 0.519] | 12.70 [7.91, 31.17] | 12.99 |
| C8 vs C2 | 0.398 | 1.940 | 0.040 [0.015, 0.206] | 6.23 [3.88, 15.29] | 6.45 |
| C8b vs C2 | 0.249 | 1.105 | 0.048 [0.019, 0.237] | 6.82 [4.25, 16.75] | 7.00 |
| C4 vs C5 | 0.453 | 1.135 | 0.137 [0.058, 0.491] | 12.02 [7.48, 29.50] | 12.18 |
| C6c vs C5 | 0.825 | 1.261 | 0.300 [0.142, 0.721] | 19.64 [12.23, 48.20] | 20.35 |
| C7 vs C5 | 0.490 | 1.130 | 0.158 [0.067, 0.532] | 13.04 [8.12, 32.00] | 13.24 |
| C7q vs C5 | 0.325 | 1.083 | 0.083 [0.033, 0.354] | 9.06 [5.64, 22.24] | 9.02 |
| C8 vs C5 | 0.343 | 1.132 | 0.084 [0.034, 0.358] | 9.14 [5.69, 22.43] | 9.56 |
| C8b vs C5 | 0.225 | 0.606 | 0.121 [0.050, 0.455] | 11.18 [6.96, 27.44] | 11.17 |
| C4 vs C5o | 0.392 | 0.988 | 0.136 [0.057, 0.489] | 11.96 [7.44, 29.34] | 12.03 |
| C6c vs C5o | 0.768 | 1.299 | 0.259 [0.119, 0.678] | 17.76 [11.05, 43.57] | 18.12 |
| C7 vs C5o | 0.425 | 0.832 | 0.207 [0.091, 0.612] | 15.36 [9.56, 37.69] | 15.22 |
| C7q vs C5o | 0.258 | 0.717 | 0.115 [0.047, 0.441] | 10.85 [6.76, 26.64] | 11.00 |
| C8 vs C5o | 0.360 | 1.802 | 0.038 [0.015, 0.198] | 6.08 [3.79, 14.93] | 6.14 |
| C8b vs C5o | 0.218 | 1.009 | 0.044 [0.017, 0.222] | 6.55 [4.08, 16.07] | 6.69 |

### Crossed decomposition and tests of the family effect

| comparison | sigma_a | sigma_b | sigma_e | rho_family [95% GCI] | F test p | permutation p (obs/median) | Hotelling p | studentized perm p | full SE / family SE |
|---|---|---|---|---|---|---|---|---|---|
| C4 vs C2 | 0.385 | 0.000 | 1.007 | 0.128 [0.053, 0.471] | 1.2e-131 | 5.0e-05 (132.1) | 9.8e-78 | 2.0e-04 | 1.0000 |
| C6c vs C2 | 0.764 | 0.000 | 1.377 | 0.235 [0.105, 0.651] | 6.3e-260 | 5.0e-05 (244.5) | 4.5e-66 | 2.0e-04 | 1.0000 |
| C7 vs C2 | 0.417 | 0.000 | 0.775 | 0.225 [0.100, 0.637] | 2.4e-246 | 5.0e-05 (233.6) | 1.3e-72 | 2.0e-04 | 1.0000 |
| C7q vs C2 | 0.248 | 0.000 | 0.623 | 0.137 [0.057, 0.491] | 1.2e-141 | 5.0e-05 (142.3) | 3.4e-78 | 2.0e-04 | 1.0000 |
| C8 vs C2 | 0.401 | 0.561 | 1.370 | 0.068 [0.027, 0.309] | 1.4e-78 | 5.0e-05 (81.8) | 5.8e-32 | 2.0e-04 | 1.0064 |
| C8b vs C2 | 0.250 | 0.278 | 0.869 | 0.070 [0.027, 0.314] | 6.4e-76 | 5.0e-05 (78.4) | 1.1e-37 | 2.0e-04 | 1.0041 |
| C4 vs C5 | 0.453 | 0.000 | 1.327 | 0.104 [0.042, 0.415] | 9.7e-106 | 5.0e-05 (107.7) | 2.8e-29 | 2.0e-04 | 1.0000 |
| C6c vs C5 | 0.824 | 0.000 | 1.664 | 0.197 [0.085, 0.598] | 8.5e-212 | 5.0e-05 (204.6) | 6.5e-63 | 2.0e-04 | 1.0000 |
| C7 vs C5 | 0.489 | 0.000 | 1.179 | 0.147 [0.061, 0.511] | 2.5e-153 | 5.0e-05 (152.3) | 3.0e-60 | 2.0e-04 | 1.0000 |
| C7q vs C5 | 0.325 | 0.106 | 1.052 | 0.087 [0.034, 0.367] | 1.1e-87 | 5.0e-05 (91.1) | 9.2e-34 | 2.0e-04 | 1.0003 |
| C8 vs C5 | 0.343 | 0.276 | 0.907 | 0.116 [0.047, 0.445] | 4.3e-129 | 5.0e-05 (129.8) | 5.9e-35 | 2.0e-04 | 1.0021 |
| C8b vs C5 | 0.225 | 0.000 | 0.610 | 0.120 [0.049, 0.452] | 9.9e-123 | 5.0e-05 (124.4) | 1.3e-34 | 2.0e-04 | 1.0000 |
| C4 vs C5o | 0.392 | 0.000 | 1.070 | 0.119 [0.048, 0.450] | 2.1e-121 | 5.0e-05 (122.7) | 2.2e-41 | 2.0e-04 | 1.0000 |
| C6c vs C5o | 0.768 | 0.000 | 1.426 | 0.225 [0.100, 0.637] | 2.8e-246 | 5.0e-05 (232.7) | 1.6e-59 | 2.0e-04 | 1.0000 |
| C7 vs C5o | 0.425 | 0.000 | 0.864 | 0.195 [0.084, 0.594] | 1.8e-209 | 5.0e-05 (201.8) | 1.9e-63 | 2.0e-04 | 1.0000 |
| C7q vs C5o | 0.258 | 0.000 | 0.720 | 0.114 [0.046, 0.438] | 2.4e-116 | 5.0e-05 (118.3) | 2.8e-45 | 2.0e-04 | 1.0000 |
| C8 vs C5o | 0.363 | 0.501 | 1.319 | 0.062 [0.024, 0.288] | 8.9e-70 | 5.0e-05 (73.1) | 5.9e-33 | 2.0e-04 | 1.0063 |
| C8b vs C5o | 0.219 | 0.227 | 0.842 | 0.059 [0.023, 0.278] | 2.4e-62 | 5.0e-05 (66.0) | 1.6e-35 | 2.0e-04 | 1.0035 |

### Intervals for the mean difference

| comparison | mean | image bootstrap 95% | family t 95% | full crossed 95% (df) |
|---|---|---|---|---|
| C4 vs C2 | 0.0848 | [0.0608, 0.1101] | [-0.3212, 0.4909] | [-0.3212, 0.4909] (5.0) |
| C6c vs C2 | 0.2378 | [0.2036, 0.2731] | [-0.5655, 1.0411] | [-0.5655, 1.0411] (5.0) |
| C7 vs C2 | 0.0900 | [0.0713, 0.1098] | [-0.3489, 0.5289] | [-0.3489, 0.5289] (5.0) |
| C7q vs C2 | 0.0280 | [0.0131, 0.0437] | [-0.2331, 0.2891] | [-0.2331, 0.2891] (5.0) |
| C8 vs C2 | 0.2260 | [0.1766, 0.2766] | [-0.1970, 0.6491] | [-0.1965, 0.6486] (5.1) |
| C8b vs C2 | 0.0925 | [0.0642, 0.1217] | [-0.1713, 0.3563] | [-0.1711, 0.3561] (5.1) |
| C4 vs C5 | -0.0042 | [-0.0346, 0.0252] | [-0.4814, 0.4729] | [-0.4814, 0.4729] (5.0) |
| C6c vs C5 | 0.1488 | [0.1160, 0.1809] | [-0.7176, 1.0152] | [-0.7176, 1.0152] (5.0) |
| C7 vs C5 | 0.0009 | [-0.0290, 0.0304] | [-0.5143, 0.5162] | [-0.5143, 0.5162] (5.0) |
| C7q vs C5 | -0.0610 | [-0.0901, -0.0321] | [-0.4045, 0.2824] | [-0.4045, 0.2824] (5.0) |
| C8 vs C5 | 0.1370 | [0.1085, 0.1662] | [-0.2248, 0.4988] | [-0.2247, 0.4986] (5.0) |
| C8b vs C5 | 0.0034 | [-0.0127, 0.0196] | [-0.2335, 0.2403] | [-0.2335, 0.2403] (5.0) |
| C4 vs C5o | 0.0070 | [-0.0190, 0.0334] | [-0.4063, 0.4202] | [-0.4063, 0.4202] (5.0) |
| C6c vs C5o | 0.1600 | [0.1263, 0.1942] | [-0.6472, 0.9671] | [-0.6472, 0.9671] (5.0) |
| C7 vs C5o | 0.0121 | [-0.0100, 0.0348] | [-0.4349, 0.4591] | [-0.4349, 0.4591] (5.0) |
| C7q vs C5o | -0.0498 | [-0.0688, -0.0311] | [-0.3220, 0.2223] | [-0.3220, 0.2223] (5.0) |
| C8 vs C5o | 0.1482 | [0.1006, 0.1959] | [-0.2353, 0.5316] | [-0.2349, 0.5312] (5.1) |
| C8b vs C5o | 0.0146 | [-0.0112, 0.0415] | [-0.2166, 0.2458] | [-0.2165, 0.2457] (5.1) |

### Leave one family out and fold dependence

| comparison | smallest LOFO family p (family omitted) | smallest LOFO SE ratio | fold ICC [upper] | design effect [upper] | SE ratio, fold-adjusted [conservative] |
|---|---|---|---|---|---|
| C4 vs C2 | 0.031 (vignetting) | 4.98 | 0.3125 [0.7915] | 56.93 [142.68] | 1.62 [1.02] |
| C6c vs C2 | 0.016 (vignetting) | 3.18 | 0.2219 [0.7056] | 40.71 [127.30] | 2.72 [1.54] |
| C7 vs C2 | 0.016 (vignetting) | 3.42 | 0.1459 [0.5921] | 27.11 [106.99] | 3.29 [1.66] |
| C7q vs C2 | 0.030 (vignetting) | 4.72 | 0.2551 [0.7416] | 46.66 [133.75] | 1.86 [1.10] |
| C8 vs C2 | 0.183 (shot_noise) | 5.78 | 0.1309 [0.5624] | 24.44 [101.68] | 1.26 [0.62] |
| C8b vs C2 | 0.301 (contrast_loss) | 6.27 | 0.1457 [0.5918] | 27.08 [106.93] | 1.31 [0.66] |
| C4 vs C5 | 0.086 (vignetting) | 4.49 | 0.1746 [0.6415] | 32.26 [115.82] | 2.12 [1.12] |
| C6c vs C5 | 0.108 (vignetting) | 4.97 | 0.1238 [0.5471] | 23.16 [98.93] | 4.08 [1.97] |
| C7 vs C5 | 0.101 (vignetting) | 4.93 | 0.0420 [0.2870] | 8.52 [52.38] | 4.47 [1.80] |
| C7q vs C5 | 0.086 (vignetting) | 4.49 | 0.0864 [0.4512] | 16.47 [81.77] | 2.23 [1.00] |
| C8 vs C5 | 0.298 (shot_noise) | 7.21 | 0.1961 [0.6728] | 36.11 [121.44] | 1.52 [0.83] |
| C8b vs C5 | 0.002 (vignetting) | 1.65 | 0.2574 [0.7439] | 47.08 [134.16] | 1.63 [0.97] |
| C4 vs C5o | 0.032 (vignetting) | 4.78 | 0.2825 [0.7671] | 51.56 [138.31] | 1.67 [1.02] |
| C6c vs C5o | 0.034 (vignetting) | 4.70 | 0.1827 [0.6537] | 33.70 [118.01] | 3.06 [1.63] |
| C7 vs C5o | 0.031 (vignetting) | 4.75 | 0.0702 [0.3992] | 13.57 [72.46] | 4.17 [1.80] |
| C7q vs C5o | 0.029 (vignetting) | 4.64 | 0.1593 [0.6164] | 29.52 [111.33] | 2.00 [1.03] |
| C8 vs C5o | 0.215 (shot_noise) | 5.23 | 0.1311 [0.5629] | 24.47 [101.75] | 1.23 [0.60] |
| C8b vs C5o | 0.399 (vignetting) | 4.85 | 0.1390 [0.5789] | 25.88 [104.62] | 1.29 [0.64] |

Fold component as a share of the family-level variance: C4 vs C2 0.403 [upper 3.368]; C6c vs C2 0.138 [upper 1.163]; C7 vs C2 0.092 [upper 0.784]; C7q vs C2 0.300 [upper 2.514]; C8 vs C2 0.623 [upper 5.316]; C8b vs C2 0.580 [upper 4.930]; C4 vs C5 0.225 [upper 1.906]; C6c vs C5 0.059 [upper 0.506]; C7 vs C5 0.045 [upper 0.412]; C7q vs C5 0.193 [upper 1.675]; C8 vs C5 0.440 [upper 3.707]; C8b vs C5 0.391 [upper 3.274]; C4 vs C5o 0.377 [upper 3.153]; C6c vs C5o 0.108 [upper 0.914]; C7 vs C5o 0.054 [upper 0.478]; C7q vs C5o 0.251 [upper 2.131]; C8 vs C5o 0.655 [upper 5.588]; C8b vs C5o 0.600 [upper 5.110].

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
| NEU-CLS / resnet50.a1_in1k / G1 | C4 vs C2 | 10 | 0.0641 | 0.0114 | 0.1202 | 5.64 | 0.53 | 2.63 to 13.37 |
| NEU-CLS / resnet50.a1_in1k / G1 | C6c vs C2 | 10 | 0.0690 | 0.0191 | 0.3321 | 3.61 | 0.21 | 13.45 to 19.77 |
| NEU-CLS / resnet50.a1_in1k / G1 | C7 vs C2 | 10 | 0.0493 | 0.0109 | 0.1740 | 4.51 | 0.28 | 11.28 to 19.85 |
| NEU-CLS / resnet50.a1_in1k / G1 | C7q vs C2 | 10 | 0.0542 | 0.0083 | 0.0804 | 6.55 | 0.67 | 3.75 to 13.11 |
| NEU-CLS / resnet50.a1_in1k / G1 | C8 vs C2 | 10 | 0.1021 | 0.0263 | 0.2062 | 3.89 | 0.50 | 6.23 to 9.98 |
| NEU-CLS / resnet50.a1_in1k / G1 | C8b vs C2 | 10 | 0.0527 | 0.0164 | 0.1401 | 3.23 | 0.38 | 6.60 to 11.06 |
| NEU-CLS / resnet50.a1_in1k / G1 | C4 vs C5 | 10 | 0.0990 | 0.0188 | 0.1929 | 5.27 | 0.51 | 5.85 to 13.65 |
| NEU-CLS / resnet50.a1_in1k / G1 | C6c vs C5 | 10 | 0.1026 | 0.0211 | 0.3813 | 4.85 | 0.27 | 15.00 to 22.10 |
| NEU-CLS / resnet50.a1_in1k / G1 | C7 vs C5 | 10 | 0.0909 | 0.0175 | 0.2373 | 5.19 | 0.38 | 11.36 to 17.15 |
| NEU-CLS / resnet50.a1_in1k / G1 | C7q vs C5 | 10 | 0.0924 | 0.0175 | 0.1613 | 5.28 | 0.57 | 6.26 to 11.42 |
| NEU-CLS / resnet50.a1_in1k / G1 | C8 vs C5 | 10 | 0.0818 | 0.0169 | 0.1429 | 4.85 | 0.57 | 5.21 to 11.46 |
| NEU-CLS / resnet50.a1_in1k / G1 | C8b vs C5 | 10 | 0.0533 | 0.0096 | 0.0837 | 5.53 | 0.64 | 6.24 to 13.20 |
| NEU-CLS / resnet50.a1_in1k / G1 | C4 vs C5o | 10 | 0.0649 | 0.0115 | 0.1167 | 5.62 | 0.56 | 2.96 to 14.05 |
| NEU-CLS / resnet50.a1_in1k / G1 | C6c vs C5o | 10 | 0.0797 | 0.0179 | 0.3264 | 4.44 | 0.24 | 14.34 to 20.83 |
| NEU-CLS / resnet50.a1_in1k / G1 | C7 vs C5o | 10 | 0.0587 | 0.0106 | 0.1687 | 5.55 | 0.35 | 10.35 to 19.19 |
| NEU-CLS / resnet50.a1_in1k / G1 | C7q vs C5o | 10 | 0.0568 | 0.0088 | 0.0767 | 6.47 | 0.74 | 2.71 to 11.94 |
| NEU-CLS / resnet50.a1_in1k / G1 | C8 vs C5o | 10 | 0.1064 | 0.0240 | 0.1818 | 4.43 | 0.59 | 5.99 to 9.66 |
| NEU-CLS / resnet50.a1_in1k / G1 | C8b vs C5o | 10 | 0.0609 | 0.0142 | 0.1144 | 4.30 | 0.53 | 5.43 to 10.85 |
