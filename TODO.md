# TODO

Last updated: 2026-08-25

Priority order is scientific, not cosmetic.

## Current Gate — Task 010A Final Scientific Cleanup

Status: `AUTHORIZED / SERVER VERIFICATION PENDING`

Branch:

`analysis/experimental-review-cleanup-010a`

Primary task:

- `tasks/FINAL_SCIENTIFIC_CLEANUP_AND_EXPERIMENTAL_SHORTLIST_010A.md`

Execution script:

- `scripts/dynamics_audit_010a_cleanup.py`

Codex prompt:

- `codex/TASK_010A_CLEANUP_PROMPT.md`

## Parent Task 010 — Complete

Task 010 has already completed:

- 39 / 39 legacy 20 ns corrected reanalysis;
- PBC/RMSD/reference/contact/SASA audit;
- corrected CHARMM36 validation;
- 18 / 18 corrected-validation 20 ns trajectories;
- candidate/control classification stability review;
- `STOP_AT_20NS` screening decision;
- V4 candidate panel.

Do not rerun or extend MD as part of Task 010A.

## P0 — Cleanup Analysis

Required:

1. distinguish observed directional drift from extension-trigger drift;
2. calculate candidate-vs-WT differential block drift for RMSD/contact metrics;
3. preserve WT tag-SASA comparison as not applicable;
4. audit replica-level nonlocal tag-contact heterogeneity;
5. specifically verify `248|249 x HA` replica heterogeneity;
6. state that Priority A/B is multi-evidence expert adjudication, not a validated total-score classifier.

Expected outputs:

- `results/dynamics_audit_010/differential_block_drift_vs_wt_v1.tsv`
- `results/dynamics_audit_010/final_sampling_decision_v2_cleanup.tsv`
- `results/dynamics_audit_010/tag_nonlocal_contact_replica_heterogeneity_v1.tsv`

## P1 — Experimental Review Panel Freeze

Generate:

- `data/final_candidate_panel_v5_experimental_review_cleanup.tsv`
- `data/experimental_review_shortlist_v1.tsv`
- `docs/FINAL_SCIENTIFIC_CLEANUP_010A.md`
- `docs/EXPERIMENTAL_REVIEW_SHORTLIST_V1.md`

Shortlist must contain exactly four candidate constructs plus two controls:

Candidates:

- `289|290 x MAP8`
- `289|290 x G196_minimal`
- `248|249 x HA`
- `248|249 x MAP8`

Controls:

- `224|225 x MAP8`
- `155|156 x MAP8`

## P2 — Scientific Review Rules

- Do not hide below-threshold directional drift by writing `none`.
- Do not convert a construct mean into a claim of replica consistency.
- Do not auto-demote `248|249 x HA` solely because replica contact behavior is heterogeneous; annotate the caution.
- Do not impute corrected-protocol validation to `289|290 x G196_minimal` or `248|249 x MAP8`.
- Do not use a hidden weighted score.
- Do not call any construct safe or validated.

## P3 — Repository Governance After Successful Run

Update:

- `ACTIVE_TASK.md`
- `PROJECT_STATE.md`
- `ANALYSIS_INDEX.md`
- `DECISIONS.md`
- `TODO.md`
- `docs/DYNAMICS_ANALYSIS_AUDIT_010_RUN_LOG.md`

Expected final state:

`EXPERIMENTAL_REVIEW_SHORTLIST_READY_FOR_DISCUSSION`

## Explicit Non-Goals

Do not proceed automatically to:

- new MD replicas;
- 50 ns extension;
- membrane/RNA/ATP/antibody mechanistic MD;
- exact nucleotide/RNA/codon design;
- wet-lab procedural protocol design;
- merge to `main`.

## Required Future Input

Before final nucleotide-level construct design, obtain the exact experimental HRV-A89 2C/replicon/plasmid nucleotide context.
