# CORRECTED_PROTOCOL_VALIDATION_V1

Date: 2026-08-25

Task: `DYNAMICS_ANALYSIS_AUDIT_AND_CANDIDATE_RERANK_010`

Final validation state: `AUDITED_CANDIDATE_PANEL_READY_FOR_EXPERIMENTAL_REVIEW`

## Completion QC

All 18 corrected CHARMM36 validation trajectories were audited at the trajectory level. Slurm completion was not used as a substitute for trajectory QC.

|   array_index | construct_id        |   replica | sacct_state   | sacct_exit_code   |   frame_count |   final_time_ns | finished_mdrun   | finite_coordinates   | energy_status   | integrity_status   |
|--------------:|:--------------------|----------:|:--------------|:------------------|--------------:|----------------:|:-----------------|:---------------------|:----------------|:-------------------|
|             0 | WT_112_321          |         1 | COMPLETED     | 0:0               |           201 |              20 | True             | True                 | finite          | pass               |
|             1 | WT_112_321          |         2 | COMPLETED     | 0:0               |           201 |              20 | True             | True                 | finite          | pass               |
|             2 | WT_112_321          |         3 | COMPLETED     | 0:0               |           201 |              20 | True             | True                 | finite          | pass               |
|             3 | A89_2C_289_290_MAP8 |         1 | COMPLETED     | 0:0               |           201 |              20 | True             | True                 | finite          | pass               |
|             4 | A89_2C_289_290_MAP8 |         2 | COMPLETED     | 0:0               |           201 |              20 | True             | True                 | finite          | pass               |
|             5 | A89_2C_289_290_MAP8 |         3 | COMPLETED     | 0:0               |           201 |              20 | True             | True                 | finite          | pass               |
|             6 | A89_2C_248_249_HA   |         1 | COMPLETED     | 0:0               |           201 |              20 | True             | True                 | finite          | pass               |
|             7 | A89_2C_248_249_HA   |         2 | COMPLETED     | 0:0               |           201 |              20 | True             | True                 | finite          | pass               |
|             8 | A89_2C_248_249_HA   |         3 | COMPLETED     | 0:0               |           201 |              20 | True             | True                 | finite          | pass               |
|             9 | A89_2C_256_257_MAP8 |         1 | COMPLETED     | 0:0               |           201 |              20 | True             | True                 | finite          | pass               |
|            10 | A89_2C_256_257_MAP8 |         2 | COMPLETED     | 0:0               |           201 |              20 | True             | True                 | finite          | pass               |
|            11 | A89_2C_256_257_MAP8 |         3 | COMPLETED     | 0:0               |           201 |              20 | True             | True                 | finite          | pass               |
|            12 | A89_2C_224_225_MAP8 |         1 | COMPLETED     | 0:0               |           201 |              20 | True             | True                 | finite          | pass               |
|            13 | A89_2C_224_225_MAP8 |         2 | COMPLETED     | 0:0               |           201 |              20 | True             | True                 | finite          | pass               |
|            14 | A89_2C_224_225_MAP8 |         3 | COMPLETED     | 0:0               |           201 |              20 | True             | True                 | finite          | pass               |
|            15 | A89_2C_155_156_MAP8 |         1 | COMPLETED     | 0:0               |           201 |              20 | True             | True                 | finite          | pass               |
|            16 | A89_2C_155_156_MAP8 |         2 | COMPLETED     | 0:0               |           201 |              20 | True             | True                 | finite          | pass               |
|            17 | A89_2C_155_156_MAP8 |         3 | COMPLETED     | 0:0               |           201 |              20 | True             | True                 | finite          | pass               |

## Corrected Validation Dynamics

| construct_id        | junction   | tag_form   |   validation_wt_reference_rmsd_mean_A | validation_delta_local_rmsf_vs_wt_A   |   validation_wt_defined_contact_retention |   validation_tag_nonlocal_contact_fraction | validation_md_review_status   | validation_md_caution_flags   |
|:--------------------|:-----------|:-----------|--------------------------------------:|:--------------------------------------|------------------------------------------:|-------------------------------------------:|:------------------------------|:------------------------------|
| A89_2C_155_156_MAP8 | 155\|156   | MAP8       |                               2.04661 | 0.552512001858388                     |                                  0.897061 |                                  0.91874   | md_caution                    | high_nonlocal_tag_contact     |
| A89_2C_224_225_MAP8 | 224\|225   | MAP8       |                               2.20344 | -0.31635514252229013                  |                                  0.898426 |                                  1         | md_caution                    | high_nonlocal_tag_contact     |
| A89_2C_248_249_HA   | 248\|249   | HA         |                               1.59898 | 0.03584514314139157                   |                                  0.910257 |                                  0.59204   | md_neutral_or_supportive      | none                          |
| A89_2C_256_257_MAP8 | 256\|257   | MAP8       |                               1.72676 | 0.6976042969183833                    |                                  0.908797 |                                  0.0845771 | md_neutral_or_supportive      | none                          |
| A89_2C_289_290_MAP8 | 289\|290   | MAP8       |                               1.93838 | 0.12133628270898604                   |                                  0.902259 |                                  0.0281924 | md_neutral_or_supportive      | none                          |
| WT_112_321          | WT         | WT         |                               1.39667 | NA                                    |                                  0.92626  |                                  0         | md_neutral_or_supportive      | none                          |

## Protocol Sensitivity

The corrected protocol was compared against the legacy Task 009 trajectories without concatenating the two trajectory sets as six replicas.

Key conclusion: Task 009 candidate/control interpretation is broadly stable for the directly validated rows. Corrected validation keeps `289|290 x MAP8` and `248|249 x HA` as candidate hypotheses, reproduces `224|225 x MAP8` and `155|156 x MAP8` nonlocal-tag-contact cautions, and keeps `256|257 x MAP8` as MD-neutral but biologically conflicted.

## Sampling Decisions

| construct_id        | role                                   | corrected_protocol_md_status   | classification_changed_vs_legacy   | directional_drift_metrics   | sampling_decision   | decision_basis                                              |
|:--------------------|:---------------------------------------|:-------------------------------|:-----------------------------------|:----------------------------|:--------------------|:------------------------------------------------------------|
| WT_112_321          | WT baseline                            | baseline                       | no                                 | none                        | STOP_AT_20NS        | classification_stable_for_screening;no_blanket_50ns_trigger |
| A89_2C_289_290_MAP8 | candidate_hypothesis_C_terminal_MAP8   | md_neutral_or_supportive       | no                                 | none                        | STOP_AT_20NS        | classification_stable_for_screening;no_blanket_50ns_trigger |
| A89_2C_248_249_HA   | candidate_hypothesis_non_C_terminal_HA | md_neutral_or_supportive       | no                                 | none                        | STOP_AT_20NS        | classification_stable_for_screening;no_blanket_50ns_trigger |
| A89_2C_256_257_MAP8 | conflict_control_oligomer_function     | md_neutral_or_supportive       | no                                 | none                        | STOP_AT_20NS        | classification_stable_for_screening;no_blanket_50ns_trigger |
| A89_2C_224_225_MAP8 | conflict_control_MD_caution_retest     | md_caution                     | no                                 | none                        | STOP_AT_20NS        | classification_stable_for_screening;no_blanket_50ns_trigger |
| A89_2C_155_156_MAP8 | hard_negative_control                  | md_caution                     | no                                 | none                        | STOP_AT_20NS        | classification_stable_for_screening;no_blanket_50ns_trigger |

No blanket 50 ns extension is supported.
