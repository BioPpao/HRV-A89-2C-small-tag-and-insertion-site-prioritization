# TODO

Last updated: 2026-08-22

Priority order is scientific, not cosmetic.

## ONE_SHOT_COMPUTATIONAL_AUDIT_003 — COMPLETED WITH BLOCKER

Status: **METHOD_HARDENING_BLOCKED**

Task:

- `tasks/ONE_SHOT_COMPUTATIONAL_AUDIT_003.md`

This task superseded `METHOD_HARDENING_002` as the active execution wrapper and incorporated all of its mandatory modules.

The run pushed the CPU-valid computational evidence as far as scientifically justified. Mandatory PLM scoring remained blocked.

Stage status:

1. EV-A71 substitution-tolerance integration: complete.
2. Continuous/Pareto all-320 junction re-ranking: complete.
3. Phylogeny-aware independent natural-indel-event analysis: complete.
4. MAP8/HA/G196 tag-specific PLM insertion scans: blocked.
5. Ranking robustness and negative-control audits: complete for non-PLM layers.
6. Cross-tag consensus/disagreement analysis: blocked.
7. Reduced computational review-set construction: complete as review set only.
8. Final synthesis and repository updates: complete locally.

Optional stage:

- lightweight insertion-specific structural feasibility triage: deferred because no mature reproducible workflow was available.

Do not automatically start long MD, experimental protocol design, final RNA/codon design, or final experimental construct recommendation.

Primary outputs generated:

- `data/candidate_junctions_v4_method_hardening.tsv`
- `data/pareto_junction_frontier_v1.tsv`
- `data/hrvA_independent_indel_events_v1.tsv`
- `data/tag_specific_plm_scores_v1.tsv`
- `data/tag_specific_consensus_v1.tsv`
- `data/computational_review_set_v1.tsv`
- `results/one_shot_003/ranking_robustness.tsv`
- `results/one_shot_003/negative_control_audit.tsv`
- `docs/METHOD_HARDENING_002_REPORT.md`
- `docs/RANKING_ROBUSTNESS_AUDIT_V1.md`
- `docs/TAG_SPECIFIC_CONSENSUS_V1.md`
- `docs/COMPUTATIONAL_REVIEW_SET_V1.md`
- `docs/ONE_SHOT_COMPUTATIONAL_AUDIT_003_REPORT.md`

Final state:

- `METHOD_HARDENING_BLOCKED`

## GPU_RECOVERY_004 — COMPLETED

Status: **READY_FOR_CONFLICT_AWARE_TAG_SITE_MODELING**

Task:

- `tasks/GPU_RECOVERY_004.md`

Report:

- `docs/GPU_RECOVERY_004_REPORT.md`

Successful GPU run:

- Slurm node: `gpu15`
- GPU: NVIDIA GeForce RTX 3090
- PyTorch: 2.4.1+cu118
- PLM: ESM2 `esm2_t6_8M_UR50D`
- completed rows: 1,280 / 1,280

Primary outputs:

- `data/tag_specific_plm_scores_v2_gpu.tsv`
- `data/tag_specific_consensus_v2_gpu.tsv`
- `data/candidate_junctions_v5_plm_gpu.tsv`
- `data/computational_review_set_v2_plm_gpu.tsv`
- `docs/TAG_SPECIFIC_PLM_SCAN_V2_GPU.md`
- `docs/TAG_SPECIFIC_CONSENSUS_V2_GPU.md`

## CURRENT — Review / modeling authorization decision

ChatGPT/user must decide one of:

1. authorize conflict-aware Tag x Site structural modeling from `data/computational_review_set_v2_plm_gpu.tsv`;
2. stop computational escalation and pivot to HRV-A89-specific empirical validation planning;
3. request a narrower/manual review of the V5 PLM evidence before modeling.

Until then, do not start long MD, final construct recommendation or RNA/codon design.

## Completed upstream work

- CONSERVATION_001 — complete/provisional.
- CONSERVATION_002 — complete/decision-grade.
- DIRECT_INDEL_001 — complete; direct EV-A71 2C insertion phenotype requires shortlist revision.
- METHOD_GAP_AND_NEXT_EVIDENCE_AUDIT_V2 — complete; current state `NO_HIGH_CONFIDENCE_TARGETED_SITE_YET`.

## Later work — blocked pending review

### Insertion-specific Tag × Site structural modeling

Only after `data/computational_review_set_v2_plm_gpu.tsv` is reviewed and authorized.

### Targeted MD

Only after a very small number of tagged constructs survive insertion-specific structural perturbation analysis.

### Exact nucleotide/RNA audit

Mandatory before final construct recommendation, but blocked until the exact experimental nucleotide construct/context is supplied.

## Repository maintenance

- keep `PROJECT_STATE.md`, `ACTIVE_TASK.md`, `ANALYSIS_INDEX.md`, `DECISIONS.md` and this file consistent;
- preserve versioned historical outputs;
- record software/environment versions and commands;
- commit small/medium data and reports, not package caches, model checkpoints, bulk structure ensembles or MD trajectories.
