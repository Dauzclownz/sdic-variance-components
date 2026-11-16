Extra tables computed from the per-image data of the Colab re-run (1 November 2026)

submitted_vs_rerun.csv            submitted (Phase 0.11 output in the repository) versus re-run, per comparison
training_variability.csv          spread of each mean over the ten fold partitions and the derived shares
per_family_deltas_rerun.csv       per-family mean NLL differences (A minus B), all twelve comparisons
amplitude_matched_all_comparisons.csv
                                  amplitude-matched analysis for all twelve comparisons, plus the unmatched
                                  reference on the same four families

This results folder replaces the one in sdic_revision_G1.zip from Colab: every number is the same
except the amplitude_matched.csv files, which the Colab run computed with degenerate defaults
(targets of 0.07% to 0.37% accuracy loss and interpolation toward the clean condition).
