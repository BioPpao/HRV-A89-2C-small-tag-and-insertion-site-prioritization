# Active Task

Current task: `FINAL_SCIENTIFIC_CLEANUP_AND_EXPERIMENTAL_SHORTLIST_010A` — **COMPLETED / WAITING FOR CHATGPT REVIEW**

Branch: `analysis/experimental-review-cleanup-010a`

Primary specification:

- `tasks/FINAL_SCIENTIFIC_CLEANUP_AND_EXPERIMENTAL_SHORTLIST_010A.md`

Execution script:

- `scripts/dynamics_audit_010a_cleanup.py`

Codex prompt:

- `codex/TASK_010A_CLEANUP_PROMPT.md`

## Current Scientific State

Parent Task 010 achieved:

`AUDITED_CANDIDATE_PANEL_READY_FOR_EXPERIMENTAL_REVIEW`

Task 010A did not reopen the MD campaign. It completed the final scientific cleanup before experimental discussion.

## Why Task 010A Exists

Post-review identified four reporting/methodology refinements that do not justify new MD but should be corrected before freezing the wet-lab review shortlist:

1. `directional_drift_metrics=none` can hide same-direction drift that is present but below the extension threshold;
2. candidate drift should be interpreted relative to WT fragment relaxation where a WT comparator exists;
3. `248|249 x HA` has replica-heterogeneous nonlocal tag-contact behavior that should be annotated rather than averaged away;
4. Priority A/B must be explicitly described as multi-evidence expert adjudication, not an algorithmically validated total score.

Task 010A also freezes a practical 4-candidate + 2-control experimental-review shortlist.

## Completed Work

Task 010A completed:

- reprocess existing Task 010 TSV outputs;
- compute candidate-vs-WT differential block drift;
- revise drift/extension terminology;
- audit replica-level nonlocal tag-contact heterogeneity;
- add priority-method provenance fields;
- generate V5 candidate panel and 4+2 shortlist;
- update reports and repository governance files;
- commit and push verified outputs.

## Explicitly Not Authorized

Do not submit:

- new MD replicas;
- 50 ns extensions;
- new Slurm/GPU jobs;
- membrane/RNA/ATP/antibody MD;
- local multimer recovery jobs.

If cleanup reveals a genuinely decision-changing candidate-specific excess drift after WT subtraction, document it and stop for review rather than launching compute.

## Required Outputs

- `results/dynamics_audit_010/differential_block_drift_vs_wt_v1.tsv`
- `results/dynamics_audit_010/final_sampling_decision_v2_cleanup.tsv`
- `results/dynamics_audit_010/tag_nonlocal_contact_replica_heterogeneity_v1.tsv`
- `results/dynamics_audit_010/task010a_internal_consistency_audit_v1.tsv`
- `data/final_candidate_panel_v5_experimental_review_cleanup.tsv`
- `data/experimental_review_shortlist_v1.tsv`
- `docs/FINAL_SCIENTIFIC_CLEANUP_010A.md`
- `docs/EXPERIMENTAL_REVIEW_SHORTLIST_V1.md`

## Completion State

`EXPERIMENTAL_REVIEW_SHORTLIST_READY_FOR_DISCUSSION`

## Biological Boundary

No construct is safe or experimentally validated. Exact HRV-A89 nucleotide/replicon/plasmid context is still required before nucleotide/codon/RNA-level construct design.
