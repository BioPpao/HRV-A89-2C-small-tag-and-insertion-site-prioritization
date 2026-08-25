# Codex Prompt — Task 010A Final Scientific Cleanup

You are executing `FINAL_SCIENTIFIC_CLEANUP_AND_EXPERIMENTAL_SHORTLIST_010A` on branch `analysis/experimental-review-cleanup-010a`.

Read in order:

1. `WORKFLOW.md`
2. `AGENTS.md`
3. `PROJECT_STATE.md`
4. `DECISIONS.md`
5. `ANALYSIS_INDEX.md`
6. `ACTIVE_TASK.md`
7. `tasks/FINAL_SCIENTIFIC_CLEANUP_AND_EXPERIMENTAL_SHORTLIST_010A.md`
8. `docs/CORRECTED_PROTOCOL_VALIDATION_V1.md`
9. `docs/FINAL_CANDIDATE_PRIORITY_V2_CORRECTED_VALIDATION.md`
10. `results/dynamics_audit_010/corrected_validation_block_stability_v1.tsv`
11. `data/corrected_validation_tag_exposure_v1.tsv`
12. `scripts/dynamics_audit_010a_cleanup.py`

Then execute Task 010A end-to-end.

## Critical execution rule

This is an analysis/reporting cleanup only. Do not submit any new Slurm/GPU/MD job.

First inspect the existing files and independently verify the cleanup script logic. Do not blindly trust thresholds or labels merely because they are already coded.

Run:

`python scripts/dynamics_audit_010a_cleanup.py`

Then audit every generated output for internal consistency.

## Required scientific checks

1. Confirm that `directional_drift_observed_metrics` records same-direction drift even when the extension threshold is not crossed.
2. Confirm that `extension_trigger_metrics` is separate from descriptive directional drift.
3. Confirm candidate-vs-WT differential late-minus-early drift for self RMSD, WT-reference RMSD and WT-defined contact retention.
4. Confirm WT comparison is not attempted for tag SASA because WT has no tag.
5. Verify the `289|290 x MAP8` differential drift interpretation numerically from source tables.
6. Recompute replica-level nonlocal tag-contact heterogeneity for every directly validated tagged construct.
7. Specifically verify `248|249 x HA` from the three individual replica values; if the script does not flag the real heterogeneity, repair the script rather than changing the biological conclusion to fit the code.
8. Ensure `248|249 x HA` remains a candidate hypothesis with an explicit heterogeneity caution unless stronger evidence actually justifies demotion.
9. Confirm Priority A/B is described as `multi_evidence_expert_adjudication`, not an algorithmically validated score.
10. Confirm no corrected-protocol evidence is imputed to `289|290 x G196_minimal` or `248|249 x MAP8`.
11. Confirm the final 4+2 shortlist is exactly:
   - `289|290 x MAP8`
   - `289|290 x G196_minimal`
   - `248|249 x HA`
   - `248|249 x MAP8`
   - control `224|225 x MAP8`
   - hard-negative control `155|156 x MAP8`
12. Confirm no new MD is scientifically triggered by the cleanup. If a true decision-changing candidate-specific excess drift appears after WT subtraction, do not submit compute; document it and stop for review.

## Required outputs

The following must exist and be scientifically audited:

- `results/dynamics_audit_010/differential_block_drift_vs_wt_v1.tsv`
- `results/dynamics_audit_010/final_sampling_decision_v2_cleanup.tsv`
- `results/dynamics_audit_010/tag_nonlocal_contact_replica_heterogeneity_v1.tsv`
- `data/final_candidate_panel_v5_experimental_review_cleanup.tsv`
- `data/experimental_review_shortlist_v1.tsv`
- `docs/FINAL_SCIENTIFIC_CLEANUP_010A.md`
- `docs/EXPERIMENTAL_REVIEW_SHORTLIST_V1.md`

## Repository governance

After outputs are verified, update:

- `ACTIVE_TASK.md`
- `PROJECT_STATE.md`
- `ANALYSIS_INDEX.md`
- `DECISIONS.md`
- `TODO.md`
- `docs/DYNAMICS_ANALYSIS_AUDIT_010_RUN_LOG.md`

Final state if no decision-changing issue is found:

`EXPERIMENTAL_REVIEW_SHORTLIST_READY_FOR_DISCUSSION`

Commit with a meaningful message and push `analysis/experimental-review-cleanup-010a`.

Do not merge to `main`.
