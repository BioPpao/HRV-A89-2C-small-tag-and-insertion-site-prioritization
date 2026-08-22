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

## GPU_RECOVERY_004 — BLOCKED / NO GPU VISIBLE

Status: **GPU_RECOVERY_BLOCKED_NO_GPU**

Task:

- `tasks/GPU_RECOVERY_004.md`

Report:

- `docs/GPU_RECOVERY_004_REPORT.md`

Required GPU checks were performed:

- `hostname`: `admin1`
- `nvidia-smi`: command not found
- `CUDA_VISIBLE_DEVICES`: empty
- `/dev/nvidia*`: absent

Per task rule, no completed CPU analyses were rerun and no PLM-completed V5/V2 outputs were generated.

## CURRENT — Review / unblock decision

ChatGPT/user must decide one of:

1. rerun `GPU_RECOVERY_004` inside a Slurm GPU allocation where `nvidia-smi` and `/dev/nvidia*` are visible;
2. accept the unresolved PLM blocker and pivot to HRV-A89-specific empirical validation planning;
3. explicitly authorize conflict-aware Tag x Site modeling despite absent PLM evidence.

Until then, do not start Tag x Site modeling, long MD, final construct recommendation or RNA/codon design.

## Completed upstream work

- CONSERVATION_001 — complete/provisional.
- CONSERVATION_002 — complete/decision-grade.
- DIRECT_INDEL_001 — complete; direct EV-A71 2C insertion phenotype requires shortlist revision.
- METHOD_GAP_AND_NEXT_EVIDENCE_AUDIT_V2 — complete; current state `NO_HIGH_CONFIDENCE_TARGETED_SITE_YET`.

## Later work — blocked pending review / PLM unblock

### Insertion-specific Tag × Site structural modeling

Only after a reduced conflict-aware computational set is reviewed and authorized.

### Targeted MD

Only after a very small number of tagged constructs survive insertion-specific structural perturbation analysis.

### Exact nucleotide/RNA audit

Mandatory before final construct recommendation, but blocked until the exact experimental nucleotide construct/context is supplied.

## Repository maintenance

- keep `PROJECT_STATE.md`, `ACTIVE_TASK.md`, `ANALYSIS_INDEX.md`, `DECISIONS.md` and this file consistent;
- preserve versioned historical outputs;
- record software/environment versions and commands;
- commit small/medium data and reports, not package caches, model checkpoints, bulk structure ensembles or MD trajectories.
