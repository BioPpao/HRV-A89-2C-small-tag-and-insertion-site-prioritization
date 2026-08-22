# TODO

Last updated: 2026-08-22

Priority order is scientific, not cosmetic.

## CURRENT — ONE_SHOT_COMPUTATIONAL_AUDIT_003

Status: **AUTHORIZED / LONG-RUN COMPUTATIONAL TASK**

Task:

- `tasks/ONE_SHOT_COMPUTATIONAL_AUDIT_003.md`

This task supersedes `METHOD_HARDENING_002` as the active execution wrapper and incorporates all of its mandatory modules.

The intended use is an unattended run on the 3090 server so the computational evidence layer can be pushed as far as scientifically justified in one session.

Mandatory stages:

1. EV-A71 substitution-tolerance integration.
2. Continuous/Pareto all-320 junction re-ranking.
3. Phylogeny-aware independent natural-indel-event analysis.
4. MAP8/HA/G196 tag-specific PLM insertion scans.
5. Ranking robustness and negative-control audits.
6. Cross-tag consensus/disagreement analysis.
7. Reduced computational review-set construction.
8. Final synthesis and repository updates.

Optional stage:

- lightweight insertion-specific structural feasibility triage for the reduced review set, only if a mature reproducible method is available without derailing the run.

Do not automatically start long MD, experimental protocol design, final RNA/codon design, or final experimental construct recommendation.

Primary outputs expected:

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

Final state must be exactly one of:

- `READY_FOR_CONFLICT_AWARE_TAG_SITE_MODELING`
- `NO_HIGH_CONFIDENCE_TARGETED_SITE`
- `METHOD_HARDENING_BLOCKED`

## Completed upstream work

- CONSERVATION_001 — complete/provisional.
- CONSERVATION_002 — complete/decision-grade.
- DIRECT_INDEL_001 — complete; direct EV-A71 2C insertion phenotype requires shortlist revision.
- METHOD_GAP_AND_NEXT_EVIDENCE_AUDIT_V2 — complete; current state `NO_HIGH_CONFIDENCE_TARGETED_SITE_YET`.

## Later work — blocked pending ONE_SHOT_COMPUTATIONAL_AUDIT_003 review

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
