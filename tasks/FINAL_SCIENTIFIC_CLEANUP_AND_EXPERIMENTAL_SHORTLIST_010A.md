# FINAL_SCIENTIFIC_CLEANUP_AND_EXPERIMENTAL_SHORTLIST_010A

Date: 2026-08-25

Branch: `analysis/experimental-review-cleanup-010a`

Status: `AUTHORIZED`

Parent checkpoint: `analysis/dynamics-audit-010` at Task 010 state `AUDITED_CANDIDATE_PANEL_READY_FOR_EXPERIMENTAL_REVIEW`.

## Objective

Perform a final scientific cleanup of Task 010 reporting without launching new MD. The goal is to make the experimental-review package more precise, auditable and resistant to over-interpretation before wet-lab discussion.

This task must not change biological priority classes merely to make the outputs look cleaner. It must expose uncertainty and method semantics explicitly.

## Required corrections

### 1. Separate observed directional drift from extension-trigger drift

The current `final_sampling_decision_v1.tsv` uses `directional_drift_metrics=none` when an observable shows same-direction drift across all three replicas but does not cross a hard extension threshold. This is semantically misleading.

Create a revised sampling table that distinguishes:

- `directional_drift_observed_metrics`: metrics with same-direction late-vs-early drift across all three replicas;
- `extension_trigger_metrics`: metrics that additionally cross the predefined absolute extension threshold;
- `wt_differential_excess_metrics`: candidate-specific drift that exceeds the corresponding WT drift by a decision-relevant amount;
- `sampling_decision`: preserve `STOP_AT_20NS` unless the corrected evidence actually justifies more sampling.

Do not label an observed directional drift as `none` simply because it is below the extension threshold.

### 2. Add candidate-vs-WT differential block drift

Use `results/dynamics_audit_010/corrected_validation_block_stability_v1.tsv`.

For each directly validated construct and each applicable observable, compute:

`candidate late-minus-early drift - WT late-minus-early drift`

At minimum include:

- self-drift RMSD;
- WT-reference ensemble RMSD;
- WT-defined contact retention.

`tag_total_sasa` has no WT tag baseline and must be marked not applicable for candidate-vs-WT differential comparison.

Output:

- `results/dynamics_audit_010/differential_block_drift_vs_wt_v1.tsv`
- `results/dynamics_audit_010/final_sampling_decision_v2_cleanup.tsv`

Interpretation must distinguish relaxation shared with WT from candidate-specific excess drift.

### 3. Explicitly detect replica heterogeneity in tag nonlocal-contact behavior

Use replica-level values from `data/corrected_validation_tag_exposure_v1.tsv` rather than only the construct mean.

For each tagged corrected-validation construct report:

- replica values;
- mean / SD / min / max;
- number of replicas with fraction > 0.75;
- number with fraction < 0.50;
- heterogeneity flag.

A construct can remain a priority candidate while carrying an accessibility/contact heterogeneity caution.

The known review target is `248|249 x HA`, where corrected replicas show heterogeneous nonlocal-contact fractions. Do not automatically demote it; annotate the uncertainty.

Output:

- `results/dynamics_audit_010/tag_nonlocal_contact_replica_heterogeneity_v1.tsv`

### 4. Make priority methodology explicit

Priority A/B is a **multi-evidence expert adjudication**, not the output of a hidden or validated algorithmic total score.

The final panel must state explicitly:

- `priority_method = multi_evidence_expert_adjudication`;
- `algorithmic_total_score_used = no`;
- MD is downstream comparative perturbation evidence;
- direct homolog insertion phenotype, functional constraints and other higher-level evidence are not overridden by MD;
- corrected-protocol validation directly covers only the six systems that were actually simulated.

Create:

- `data/final_candidate_panel_v5_experimental_review_cleanup.tsv`

Do not silently assign corrected-protocol evidence to constructs not in the validation subset.

### 5. Freeze a practical 4-construct + 2-control experimental-review shortlist

The shortlist is for discussion and experimental prioritization only. It is not a nucleotide construct design and not a wet-lab procedural protocol.

Candidate constructs:

1. `A89_2C_289_290_MAP8` — primary C-terminal MAP8 candidate; directly corrected-protocol validated.
2. `A89_2C_289_290_G196_minimal` — same-site tag-identity comparator; not directly corrected-protocol validated.
3. `A89_2C_248_249_HA` — primary non-C-terminal HA candidate; directly corrected-protocol validated; carry replica-heterogeneous tag-contact caution if reproduced by the audit.
4. `A89_2C_248_249_MAP8` — crossed site/tag comparator; not directly corrected-protocol validated.

Controls:

5. `A89_2C_224_225_MAP8` — conflict control with reproduced high nonlocal tag-contact caution.
6. `A89_2C_155_156_MAP8` — hard-negative control with independent functional exclusion and reproduced MD caution.

Create:

- `data/experimental_review_shortlist_v1.tsv`
- `docs/EXPERIMENTAL_REVIEW_SHORTLIST_V1.md`

The shortlist should explain the 2-site x 2-tag logic:

- C-terminal region: 289|290 with MAP8 and G196_minimal;
- non-C-terminal region: 248|249 with HA and MAP8.

This provides site diversity and tag-identity comparison without treating adjacent C-terminal junctions as independent biological hypotheses.

## Required report

Create:

- `docs/FINAL_SCIENTIFIC_CLEANUP_010A.md`

The report must answer:

1. Which systems show observed directional drift even though they do not trigger extension?
2. After subtracting WT relaxation, is `289|290 x MAP8` showing decision-relevant excess drift?
3. Does `248|249 x HA` show replica heterogeneity in nonlocal tag contact, and how should that affect interpretation?
4. Why does the project still stop at 20 ns for screening?
5. Which metrics are ranking-relevant versus QC/exploratory?
6. Why are Priority A/B expert adjudication classes rather than algorithmically validated labels?
7. What exact 4 candidate constructs and 2 controls should be carried into experimental discussion?
8. Which four of those six have direct corrected-protocol validation and which two do not?

## Sampling boundary

Task 010A is analysis-only.

Do not submit:

- more replicas;
- 50 ns extensions;
- new membrane/RNA/ATP/antibody MD;
- new local-multimer jobs.

If the cleanup unexpectedly reveals a decision-changing candidate-specific drift after WT subtraction, stop and document it rather than automatically launching compute.

## Biological boundary

No construct may be called safe, compatible, validated or fitness-neutral.

The exact experimental HRV-A89 nucleotide/replicon/plasmid context is still required before nucleotide/codon/RNA-level construct design.

## Repository updates on completion

Update:

- `ACTIVE_TASK.md`
- `PROJECT_STATE.md`
- `ANALYSIS_INDEX.md`
- `DECISIONS.md`
- `TODO.md`
- `docs/DYNAMICS_ANALYSIS_AUDIT_010_RUN_LOG.md`

Commit and push the current branch after verification.

Expected completion state:

`EXPERIMENTAL_REVIEW_SHORTLIST_READY_FOR_DISCUSSION`
