# FINAL_SCIENTIFIC_CLEANUP_010A

Date: 2026-08-25

Status: `EXPERIMENTAL_REVIEW_SHORTLIST_READY_FOR_DISCUSSION`

## Scope

Task 010A is a reporting/statistical-semantics cleanup only. No new MD was launched. Priority classes remain hypotheses for experimental review, not claims of safety or validation.

## 1. Directional drift semantics

The revised sampling table separates observed same-direction drift from threshold-crossing extension triggers. `directional_drift_observed_metrics` is descriptive; `extension_trigger_metrics` is the actual sampling trigger layer. Therefore a metric can show directional drift while the sampling decision remains `STOP_AT_20NS`.

| construct_id        | directional_drift_observed_metrics                                      | extension_trigger_metrics   | wt_differential_excess_metrics   | sampling_decision_v2   | revised_drift_statement                                                                                               |
|:--------------------|:------------------------------------------------------------------------|:----------------------------|:---------------------------------|:-----------------------|:----------------------------------------------------------------------------------------------------------------------|
| WT_112_321          | self_drift_rmsd;wt_reference_ensemble_rmsd                              | none                        | none                             | STOP_AT_20NS           | directional_drift_observed_but_below_absolute_extension_trigger                                                       |
| A89_2C_289_290_MAP8 | self_drift_rmsd;wt_reference_ensemble_rmsd;wt_defined_contact_retention | none                        | none                             | STOP_AT_20NS           | directional_drift_observed_but_below_absolute_extension_trigger;no_decision_relevant_excess_drift_after_WT_comparison |
| A89_2C_248_249_HA   | none                                                                    | none                        | none                             | STOP_AT_20NS           | no_same_direction_drift_detected                                                                                      |
| A89_2C_256_257_MAP8 | self_drift_rmsd;wt_reference_ensemble_rmsd;wt_defined_contact_retention | none                        | none                             | STOP_AT_20NS           | directional_drift_observed_but_below_absolute_extension_trigger;no_decision_relevant_excess_drift_after_WT_comparison |
| A89_2C_224_225_MAP8 | self_drift_rmsd;tag_total_sasa                                          | none                        | none                             | STOP_AT_20NS           | directional_drift_observed_but_below_absolute_extension_trigger;no_decision_relevant_excess_drift_after_WT_comparison |
| A89_2C_155_156_MAP8 | self_drift_rmsd;wt_reference_ensemble_rmsd;wt_defined_contact_retention | none                        | none                             | STOP_AT_20NS           | directional_drift_observed_but_below_absolute_extension_trigger;no_decision_relevant_excess_drift_after_WT_comparison |

## 2. Candidate-vs-WT differential drift

For directly validated systems, RMSD/contact late-minus-early drift is compared against the corresponding WT drift. This separates fragment-wide relaxation shared with WT from candidate-specific excess drift. Tag SASA has no WT-tag baseline and is not assigned a WT differential.

Focused `289|290 x MAP8` comparison:

| metric                       |   late_minus_early_mean |   wt_late_minus_early_mean |   candidate_minus_wt_late_minus_early | candidate_specific_excess_drift_vs_wt   | candidate_vs_wt_drift_interpretation        |
|:-----------------------------|------------------------:|---------------------------:|--------------------------------------:|:----------------------------------------|:--------------------------------------------|
| self_drift_rmsd              |               0.48716   |                 0.631285   |                            -0.144125  | no                                      | candidate_drift_comparable_to_WT_relaxation |
| wt_reference_ensemble_rmsd   |               0.415816  |                 0.364263   |                             0.0515526 | no                                      | candidate_drift_comparable_to_WT_relaxation |
| wt_defined_contact_retention |              -0.0338151 |                -0.00598549 |                            -0.0278297 | no                                      | candidate_contact_change_comparable_to_WT   |

The cleanup does not identify a decision-relevant multi-metric excess-drift pattern requiring additional sampling for `289|290 x MAP8`.

## 3. `248|249 x HA` replica heterogeneity

replica values=0.761194;0.263682;0.751244; mean=0.592; SD=0.284; range=0.264-0.761; heterogeneity=yes

The correct interpretation is **Priority A with accessibility/contact heterogeneity caution**, not automatic demotion and not an unqualified `no flags` statement. The caution concerns replica-dependent tag-protein nonlocal contact behavior; global structural perturbation metrics remain comparatively mild.

## 4. Why 20 ns remains the screening stop point

`STOP_AT_20NS` remains a screening decision because candidate/control classifications are stable across corrected protocol validation and no directly validated decision-critical system shows a multi-observable candidate-specific excess-drift pattern after WT comparison that triggers the predeclared extension logic. This does not imply mechanistic convergence or biological validation.

## 5. Metric roles

Ranking-relevant downstream MD evidence:

- persistent nonlocal tag-contact behavior;
- tag exposure/SASA context;
- WT-defined native-contact preservation as a perturbation check;
- candidate-vs-WT differential drift as a sampling adequacy check.

Primarily QC or exploratory here:

- global self-drift RMSD alone;
- global Rg;
- DCCM/network over this sampling window.

## 6. Priority methodology

Priority A/B is `multi_evidence_expert_adjudication`.

No validated algorithmic total score is used. MD is a downstream comparative perturbation layer and does not override higher-weight direct homolog insertion fitness, functional constraints, evolutionary evidence or the absence of direct HRV-A89 phenotype data.

## 7. Frozen experimental-review shortlist

|   shortlist_order | construct_id                | junction   | tag_form     | panel_role   | design_role                       | corrected_protocol_validation_status         | experimental_review_annotation                     |
|------------------:|:----------------------------|:-----------|:-------------|:-------------|:----------------------------------|:---------------------------------------------|:---------------------------------------------------|
|                 1 | A89_2C_289_290_MAP8         | 289\|290   | MAP8         | candidate    | primary_C_terminal_MAP8           | directly_corrected_protocol_validated_3x20ns | none                                               |
|                 2 | A89_2C_289_290_G196_minimal | 289\|290   | G196_minimal | candidate    | same_site_tag_identity_comparator | not_directly_corrected_protocol_validated    | not_directly_corrected_protocol_validated          |
|                 3 | A89_2C_248_249_HA           | 248\|249   | HA           | candidate    | primary_non_C_terminal_HA         | directly_corrected_protocol_validated_3x20ns | replica_heterogeneous_nonlocal_tag_contact_caution |
|                 4 | A89_2C_248_249_MAP8         | 248\|249   | MAP8         | candidate    | crossed_site_tag_comparator       | not_directly_corrected_protocol_validated    | not_directly_corrected_protocol_validated          |
|                 5 | A89_2C_224_225_MAP8         | 224\|225   | MAP8         | control      | conflict_control_MD_caution       | directly_corrected_protocol_validated_3x20ns | none                                               |
|                 6 | A89_2C_155_156_MAP8         | 155\|156   | MAP8         | control      | hard_negative_control             | directly_corrected_protocol_validated_3x20ns | none                                               |

The four candidate constructs implement a compact 2-site x 2-tag logic:

- `289|290`: MAP8 + G196_minimal;
- `248|249`: HA + MAP8.

Controls:

- `224|225 x MAP8`: corrected-MD conflict control;
- `155|156 x MAP8`: hard-negative control.

## 8. Direct corrected-protocol validation coverage

Directly corrected-protocol validated among the shortlist:

- `289|290 x MAP8`;
- `248|249 x HA`;
- `224|225 x MAP8`;
- `155|156 x MAP8`.

Not directly corrected-protocol validated:

- `289|290 x G196_minimal`;
- `248|249 x MAP8`.

No direct corrected-protocol evidence is imputed to those two constructs.

## Internal consistency audit

| check                                                       | status   | detail                                                                                                                                |
|:------------------------------------------------------------|:---------|:--------------------------------------------------------------------------------------------------------------------------------------|
| v5_priority_changes_vs_v4                                   | pass     | no priority class changes                                                                                                             |
| 248_249_HA_heterogeneity_not_averaged_away                  | pass     | 0.761194;0.263682;0.751244                                                                                                            |
| 289_290_MAP8_no_decision_relevant_wt_excess                 | pass     | self_drift_rmsd:-0.14412470376050857;wt_reference_ensemble_rmsd:0.05155255731504865;wt_defined_contact_retention:-0.02782965784235336 |
| shortlist_exact_4_candidates_2_controls                     | pass     | A89_2C_289_290_MAP8;A89_2C_289_290_G196_minimal;A89_2C_248_249_HA;A89_2C_248_249_MAP8;A89_2C_224_225_MAP8;A89_2C_155_156_MAP8         |
| unsimulated_shortlist_rows_not_imputed_corrected_validation | pass     | 289\|290_G196_minimal and 248\|249_MAP8 remain not directly corrected-protocol validated                                              |
| sampling_stops_without_new_compute                          | pass     | cleanup is analysis-only; no Slurm/GPU/MD submission                                                                                  |

## Boundary

This shortlist is ready for experimental discussion only. Exact nucleotide/codon/RNA-level design remains blocked until the real experimental HRV-A89 replicon/plasmid nucleotide context is available.
