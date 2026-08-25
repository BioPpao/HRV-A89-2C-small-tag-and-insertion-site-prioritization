# FINAL_CANDIDATE_PRIORITY_V2_CORRECTED_VALIDATION

Date: 2026-08-25

Final state: `AUDITED_CANDIDATE_PANEL_READY_FOR_EXPERIMENTAL_REVIEW`

No construct is safe or experimentally validated.

## Priority Panel

| construct_id                | junction   | tag_form     | priority_class_v4   | corrected_protocol_validation_status_v4      | corrected_protocol_md_status_v4   | sampling_decision_v4                                 | v4_change_vs_v3   |
|:----------------------------|:-----------|:-------------|:--------------------|:---------------------------------------------|:----------------------------------|:-----------------------------------------------------|:------------------|
| A89_2C_289_290_MAP8         | 289\|290   | MAP8         | Priority_A          | directly_corrected_protocol_validated_3x20ns | md_neutral_or_supportive          | STOP_AT_20NS                                         | unchanged         |
| A89_2C_289_290_G196_minimal | 289\|290   | G196_minimal | Priority_A          | not_directly_corrected_protocol_validated    | not_directly_validated            | not_applicable_without_direct_corrected_protocol_run | unchanged         |
| A89_2C_248_249_HA           | 248\|249   | HA           | Priority_A          | directly_corrected_protocol_validated_3x20ns | md_neutral_or_supportive          | STOP_AT_20NS                                         | unchanged         |
| A89_2C_248_249_MAP8         | 248\|249   | MAP8         | Priority_A          | not_directly_corrected_protocol_validated    | not_directly_validated            | not_applicable_without_direct_corrected_protocol_run | unchanged         |
| A89_2C_288_289_MAP8         | 288\|289   | MAP8         | Priority_B          | not_directly_corrected_protocol_validated    | not_directly_validated            | not_applicable_without_direct_corrected_protocol_run | unchanged         |
| A89_2C_288_289_HA           | 288\|289   | HA           | Priority_B          | not_directly_corrected_protocol_validated    | not_directly_validated            | not_applicable_without_direct_corrected_protocol_run | unchanged         |
| A89_2C_290_291_MAP8         | 290\|291   | MAP8         | Priority_B          | not_directly_corrected_protocol_validated    | not_directly_validated            | not_applicable_without_direct_corrected_protocol_run | unchanged         |

## Controls

| construct_id                | junction   | tag_form     | priority_class_v4     | corrected_protocol_validation_status_v4      | corrected_protocol_md_status_v4   | sampling_decision_v4                                 | v4_change_vs_v3                         |
|:----------------------------|:-----------|:-------------|:----------------------|:---------------------------------------------|:----------------------------------|:-----------------------------------------------------|:----------------------------------------|
| A89_2C_256_257_MAP8         | 256\|257   | MAP8         | Conflict_control      | directly_corrected_protocol_validated_3x20ns | md_neutral_or_supportive          | STOP_AT_20NS                                         | MD_neutral_biological_conflict_retained |
| A89_2C_224_225_MAP8         | 224\|225   | MAP8         | Conflict_control      | directly_corrected_protocol_validated_3x20ns | md_caution                        | STOP_AT_20NS                                         | conflict_control_reinforced             |
| A89_2C_224_225_HA           | 224\|225   | HA           | Conflict_control      | not_directly_corrected_protocol_validated    | not_directly_validated            | not_applicable_without_direct_corrected_protocol_run | unchanged                               |
| A89_2C_203_204_G196_minimal | 203\|204   | G196_minimal | Conflict_control      | not_directly_corrected_protocol_validated    | not_directly_validated            | not_applicable_without_direct_corrected_protocol_run | unchanged                               |
| A89_2C_155_156_MAP8         | 155\|156   | MAP8         | Hard_negative_control | directly_corrected_protocol_validated_3x20ns | md_caution                        | STOP_AT_20NS                                         | hard_negative_MD_caution_reproduced     |

## Required Answers

1. Priority A does not change after corrected CHARMM36 validation. Directly validated Priority A rows `289|290 x MAP8` and `248|249 x HA` remain supported as screening candidates; `289|290 x G196_minimal` and `248|249 x MAP8` remain Priority A but are explicitly `not_directly_corrected_protocol_validated`.
2. `289|290 x MAP8` remains the strongest C-terminal MAP8 candidate hypothesis.
3. `248|249 x HA` remains the strongest non-C-terminal HA candidate hypothesis.
4. `155|156 x MAP8` shows a reproduced MD caution signature and remains a hard-negative control because of independent biological evidence.
5. `224|225 x MAP8` corrected-MD caution is reproduced in the independent corrected-protocol simulations.
6. `256|257 x MAP8` remains MD-neutral but biologically conflicted.
7. The most discriminating MD observable is persistent nonlocal tag-contact fraction, supported by tag exposure/contact context. WT-defined contact retention and global RMSD are useful QC/perturbation metrics but weak candidate/control discriminators here.
8. DCCM/network, global Rg and raw self-drift RMSD should be downweighted for ranking; they are exploratory or nonspecific over 20 ns.
9. Three replicas are adequate for the current screening objective, not for mechanistic validation.
10. No system currently requires 50 ns.
11. Because no system shows a decision-relevant shared slow drift requiring extension, 50 ns is not selected. If later uncertainty arises, independent replicas should be preferred when between-replica variance dominates.
12. Recommended wet-experiment review constructs remain: `289|290 x MAP8`, `289|290 x G196_minimal`, `248|249 x HA`, and `248|249 x MAP8`, with `288|289 x MAP8/HA` and `290|291 x MAP8` as backups and the listed conflict/hard-negative controls.

## Evidence Boundary

Corrected MD remains downstream comparative perturbation evidence. It does not override direct homolog insertion fitness, functional exclusions, or the absence of direct HRV-A89 insertion phenotype and exact nucleotide/RNA context.
