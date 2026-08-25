# DYNAMICS_ANALYSIS_AUDIT_010_REPORT

Date: 2026-08-25

Final state: `CANDIDATE_PRIORITY_PROVISIONAL_PENDING_CORRECTED_PROTOCOL_VALIDATION`

Supersession note: this report records the corrected legacy reanalysis and corrected-validation submission checkpoint. Current candidate-priority authority is `docs/FINAL_CANDIDATE_PRIORITY_V2_CORRECTED_VALIDATION.md` and `data/final_candidate_panel_v4_corrected_validation.tsv`.

## Executive Summary

Task 010 repaired the decision-changing analysis defects in Task 009 by applying explicit PBC unwrapping/centering, separating self-drift from WT-reference deviation, adding junction-matched WT RMSF baselines, replacing candidate-start contact preservation with WT-defined contacts, adding tag SASA, and adding replica/time-window/convergence sensitivity outputs.

The old Task 009 Tier A/B classification is superseded. The corrected provisional priority panel is:

| construct_id                | junction   | tag_form     | priority_class        | corrected_MD_status      | unresolved_conflicts                                                                                                                                                                                                     |
|:----------------------------|:-----------|:-------------|:----------------------|:-------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| A89_2C_289_290_MAP8         | 289\|290   | MAP8         | Priority_A            | md_neutral_or_supportive | no_direct_HRV_A89_insertion_phenotype;exact_nucleotide_RNA_context_missing;direct_EV_A71_homolog_insertion_unfavorable                                                                                                   |
| A89_2C_289_290_G196_minimal | 289\|290   | G196_minimal | Priority_A            | md_neutral_or_supportive | no_direct_HRV_A89_insertion_phenotype;exact_nucleotide_RNA_context_missing;direct_EV_A71_homolog_insertion_unfavorable                                                                                                   |
| A89_2C_248_249_HA           | 248\|249   | HA           | Priority_A            | md_neutral_or_supportive | no_direct_HRV_A89_insertion_phenotype;exact_nucleotide_RNA_context_missing;direct_EV_A71_homolog_insertion_unfavorable;structure_or_oligomer_context_unfavorable                                                         |
| A89_2C_248_249_MAP8         | 248\|249   | MAP8         | Priority_A            | md_neutral_or_supportive | no_direct_HRV_A89_insertion_phenotype;exact_nucleotide_RNA_context_missing;direct_EV_A71_homolog_insertion_unfavorable;structure_or_oligomer_context_unfavorable                                                         |
| A89_2C_288_289_MAP8         | 288\|289   | MAP8         | Priority_B            | md_neutral_or_supportive | no_direct_HRV_A89_insertion_phenotype;exact_nucleotide_RNA_context_missing;direct_EV_A71_homolog_insertion_unfavorable                                                                                                   |
| A89_2C_288_289_HA           | 288\|289   | HA           | Priority_B            | md_neutral_or_supportive | no_direct_HRV_A89_insertion_phenotype;exact_nucleotide_RNA_context_missing;direct_EV_A71_homolog_insertion_unfavorable                                                                                                   |
| A89_2C_290_291_MAP8         | 290\|291   | MAP8         | Priority_B            | md_neutral_or_supportive | no_direct_HRV_A89_insertion_phenotype;exact_nucleotide_RNA_context_missing;direct_EV_A71_homolog_insertion_unfavorable                                                                                                   |
| A89_2C_256_257_MAP8         | 256\|257   | MAP8         | Conflict_control      | md_neutral_or_supportive | no_direct_HRV_A89_insertion_phenotype;exact_nucleotide_RNA_context_missing;direct_EV_A71_homolog_insertion_unfavorable;structure_or_oligomer_context_unfavorable                                                         |
| A89_2C_224_225_MAP8         | 224\|225   | MAP8         | Conflict_control      | md_caution               | no_direct_HRV_A89_insertion_phenotype;exact_nucleotide_RNA_context_missing;direct_EV_A71_homolog_insertion_unfavorable;corrected_MD_nonlocal_tag_contact_caution;structure_or_oligomer_context_unfavorable               |
| A89_2C_224_225_HA           | 224\|225   | HA           | Conflict_control      | md_caution               | no_direct_HRV_A89_insertion_phenotype;exact_nucleotide_RNA_context_missing;direct_EV_A71_homolog_insertion_unfavorable;corrected_MD_nonlocal_tag_contact_caution;structure_or_oligomer_context_unfavorable               |
| A89_2C_203_204_G196_minimal | 203\|204   | G196_minimal | Conflict_control      | md_caution               | no_direct_HRV_A89_insertion_phenotype;exact_nucleotide_RNA_context_missing;direct_EV_A71_homolog_insertion_unfavorable;corrected_MD_nonlocal_tag_contact_caution;structure_or_oligomer_context_unfavorable               |
| A89_2C_155_156_MAP8         | 155\|156   | MAP8         | Hard_negative_control | md_caution               | no_direct_HRV_A89_insertion_phenotype;exact_nucleotide_RNA_context_missing;direct_EV_A71_homolog_insertion_unfavorable;corrected_MD_nonlocal_tag_contact_caution;tag_specific_PLM_disagreement;hard_functional_exclusion |

## Required Report Answers

1. The 009 trajectories were technically usable after PBC correction: 39/39 were reanalyzed.
2. PBC/RMSD correction was cross-validated against GROMACS for four representative systems; all passed with mean absolute differences below 0.001 A. Rg/tag/contact/DCCM were recomputed rather than patched from V1.
3. The old Tier A/B classification changed: `224|225` and `203|204` rows moved from candidate-like status to conflict-control status; `248|249 x HA` moved up as the strongest non-C-terminal HA candidate; `256|257` remains conflict control.
4. Invalid or biased old metrics: raw-coordinate geometry without PBC repair, self-drift mislabeled as WT-like stability, non-junction-matched local RMSF, candidate-start contact retention, and distance-only tag exposure. Old DCCM was PBC/convergence sensitive and is superseded.
5. Corrected priorities are in `data/final_candidate_panel_v3_audited.tsv`.
6. Strongest C-terminal option: `289|290 x MAP8`, with `289|290 x G196_minimal` as the strongest G196_minimal partner at the same junction.
7. Strongest non-C-terminal option: `248|249 x HA`, with `248|249 x MAP8` as MAP8 backup.
8. Best per tag: MAP8 `289|290` and `248|249`; HA `248|249`; G196_minimal `289|290`.
9. The hard-negative `155|156 x MAP8` is lower priority because of independent functional evidence and also shows corrected-MD nonlocal tag-contact caution.
10. Corrected MD has partial biological discrimination: it flags `155|156`, `224|225`, and `203|204` nonlocal-contact concerns, but does not override direct/functional evidence.
11. Time-truncation/stability outputs are in `results/dynamics_audit_010/time_truncation_stability.tsv` and `results/dynamics_audit_010/replica_stability.tsv`; rankings are stable enough for screening but not final validation.
12. Three replicas are adequate for broad screening of top candidates, not for mechanistic validation.
13. More replicas are most useful for corrected-protocol validation subset rows if rank or drift disagreement appears.
14. No system currently requires 50 ns based solely on corrected legacy reanalysis; extension is conditional on corrected-protocol validation disagreement or persistent drift.
15. There is no scientific reason to extend all systems to 50 ns.
16. Corrected CHARMM36 validation has been prepared and submitted as Slurm array job `164594`, but not completed; legacy 009 protocol differs from recommended force-switch/DispCorr settings.
17. Exact nucleotide/RNA context remains blocked until the real experimental sequence is supplied.
18. The recommended construct-identity-level experimental review panel is the Priority_A/Priority_B/control table above. This is not a wet-lab protocol.

## PBC Cross-Validation

| construct_id        |   replica | gromacs_status   |   frame_count_compared |   mean_abs_difference_A | qualitative_agreement   |
|:--------------------|----------:|:-----------------|-----------------------:|------------------------:|:------------------------|
| WT_112_321          |         1 | ok               |                    201 |             0.000177218 | pass                    |
| A89_2C_289_290_MAP8 |         1 | ok               |                    201 |             0.000181358 | pass                    |
| A89_2C_224_225_MAP8 |         1 | ok               |                    201 |             7.29103e-05 | pass                    |
| A89_2C_155_156_MAP8 |         1 | ok               |                    201 |             0.000159867 | pass                    |

## Control Discrimination

| construct_id        | control_type     | corrected_md_review_status   | md_caution_flags          | interpretation                            | overall_control_discrimination   |
|:--------------------|:-----------------|:-----------------------------|:--------------------------|:------------------------------------------|:---------------------------------|
| A89_2C_155_156_MAP8 | hard_negative    | md_caution                   | high_nonlocal_tag_contact | md_identifies_perturbation                | partial_discrimination           |
| A89_2C_256_257_MAP8 | conflict_control | md_neutral_or_supportive     | none                      | md_does_not_strongly_discriminate_control | partial_discrimination           |

## CHARMM36 Protocol Audit

| setting       | task009_value   | task010_recommended_value   | status             |
|:--------------|:----------------|:----------------------------|:-------------------|
| constraints   | h-bonds         | h-bonds                     | matches            |
| cutoff-scheme | Verlet          | Verlet                      | matches            |
| vdwtype       | MISSING         | cutoff                      | differs_or_missing |
| vdw-modifier  | MISSING         | force-switch                | differs_or_missing |
| rlist         | MISSING         | 1.2                         | differs_or_missing |
| rvdw-switch   | MISSING         | 1.0                         | differs_or_missing |
| rvdw          | 1.2             | 1.2                         | matches            |
| coulombtype   | PME             | PME                         | matches            |
| rcoulomb      | 1.2             | 1.2                         | matches            |
| DispCorr      | EnerPres        | no                          | differs_or_missing |

## Corrected Validation Subset

| construct_id        | system_id                   | junction   | tag_form   | selection_reason                       |   replicas_planned |   production_length_ns | submission_status          |
|:--------------------|:----------------------------|:-----------|:-----------|:---------------------------------------|-------------------:|-----------------------:|:---------------------------|
| WT_112_321          | WT_112_321                  | WT         | WT         | WT baseline                            |                  3 |                     20 | submitted_array_job_164594 |
| A89_2C_289_290_MAP8 | A89_2C_289_290_MAP8_112_321 | 289\|290   | MAP8       | strongest C-terminal candidate         |                  3 |                     20 | submitted_array_job_164594 |
| A89_2C_248_249_HA   | A89_2C_248_249_HA_112_321   | 248\|249   | HA         | strongest non-C-terminal candidate     |                  3 |                     20 | submitted_array_job_164594 |
| A89_2C_256_257_MAP8 | A89_2C_256_257_MAP8_112_321 | 256\|257   | MAP8       | oligomer/function conflict control     |                  3 |                     20 | submitted_array_job_164594 |
| A89_2C_224_225_MAP8 | A89_2C_224_225_MAP8_112_321 | 224\|225   | MAP8       | corrected-MD nonlocal-contact conflict |                  3 |                     20 | submitted_array_job_164594 |
| A89_2C_155_156_MAP8 | A89_2C_155_156_MAP8_112_321 | 155\|156   | MAP8       | hard negative control                  |                  3 |                     20 | submitted_array_job_164594 |

Validation jobs were submitted as Slurm array job `164594`. Initial state: tasks `0-2` running on `gpu17`, tasks `3-17` pending for resources. Results are not yet complete and must not be interpreted until analyzed with the Task 010 corrected pipeline.
