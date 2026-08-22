# TODO

Last updated: 2026-08-22

Priority order is scientific, not cosmetic. Do not jump to Tag × Site structural modeling before `METHOD_HARDENING_002` is completed and reviewed.

## P0 — CONSERVATION_001 — COMPLETE / PROVISIONAL

Preserve all V1 outputs for provenance only. Decision-making uses CONSERVATION_002/V2.

## P0 — CONSERVATION_002 — COMPLETE

Decision-grade conservation/taxonomy/structural QC hardening completed.

Primary outputs:

- `docs/CONSERVATION_SCREEN_V2.md`
- `docs/CANDIDATE_JUNCTION_QC_V1.md`
- `data/candidate_junctions_v2.tsv`
- `data/hrvA_conservation_per_junction_v2.tsv`
- `data/junction_structural_metrics_v2.tsv`

## P0 — DIRECT_INDEL_001 — COMPLETE

Direct EV-A71 2C insertion/deletion/substitution phenotype was mapped to the complete HRV-A89 all-320 junction landscape.

Primary conclusion:

`DIRECT_EVIDENCE_REQUIRES_SHORTLIST_REVISION`

Key interpretation:

- no mapped A89 junction has favorable EV-A71 2C 8-aa insertion score;
- the old `287|288–290|291` C-terminal working cluster is experimentally conflicted;
- no favorable outside-strict candidate was rescued by the direct insertion phenotype;
- direct homolog phenotype is stronger than WT structure/conservation proxies, but is not universal proof of A89-specific tag failure.

Primary outputs:

- `tasks/DIRECT_INDEL_001.md`
- `docs/EV71_2C_DIRECT_INDEL_MAPPING_V1.md`
- `data/evA71_2C_direct_indel_to_A89_v1.tsv`
- `data/candidate_junctions_v3_direct_indel.tsv`

## P0 — CURRENT: METHOD_HARDENING_002

Status: **AUTHORIZED / NEXT EXECUTION TASK**

Task:

- `tasks/METHOD_HARDENING_002.md`

Strategic audit:

- `docs/METHOD_GAP_AND_NEXT_EVIDENCE_AUDIT_V2.md`

Current project state entering the task:

`NO_HIGH_CONFIDENCE_TARGETED_SITE_YET`

### Module 1 — EV-A71 substitution-tolerance integration

- extract mature-2C substitution measurements from the existing direct dataset;
- map local substitution tolerance to all A89 junctions;
- keep substitution, deletion and insertion signals separate;
- record mapping confidence and missingness.

Planned outputs:

- `data/evA71_2C_substitution_tolerance_to_A89_v1.tsv`
- `results/method_hardening_002/substitution_mapping_qc.tsv`

### Module 2 — Continuous/Pareto all-320 re-ranking

- retain the complete 320-junction landscape;
- use `strict_structural_pass` only as an annotation;
- preserve continuous structure/interface/exposure metrics;
- use explicit evidence classes and Pareto/non-dominated ranking;
- do not use one opaque weighted scalar score as the primary decision rule;
- perform sensitivity checks for reasonable metric subsets/scaling choices.

Planned outputs:

- `data/candidate_junctions_v4_method_hardening.tsv`
- `data/pareto_junction_frontier_v1.tsv`
- `results/method_hardening_002/pareto_sensitivity.tsv`

### Module 3 — Phylogeny-aware independent natural-indel events

- use the curated CONSERVATION_002 HRV-A panel;
- build/reuse a documented HRV-A phylogeny;
- infer independent insertion/deletion events rather than counting inherited descendant states as repeated events;
- report ancestral-reconstruction/alignment uncertainty.

Planned outputs:

- `data/hrvA_independent_indel_events_v1.tsv`
- `results/method_hardening_002/phylogeny_qc.tsv`
- `docs/PHYLOGENY_AWARE_INDEL_V1.md`

### Module 4 — MAP8 / HA / G196 tag-specific PLM insertion scan

- record exact tag amino-acid sequences/forms;
- construct WT-vs-inserted A89 sequences at all 320 junctions;
- use an indel-capable protein-language-model method where practical;
- otherwise use a documented ESM-family pseudo-log-likelihood method with explicit limitations;
- output separate per-tag landscapes;
- never allow PLM to override direct phenotype or hard functional constraints.

Planned outputs:

- `data/tag_specific_plm_scores_v1.tsv`
- `results/method_hardening_002/plm_qc.tsv`
- `docs/TAG_SPECIFIC_PLM_SCAN_V1.md`

### METHOD_HARDENING_002 integration report

Required:

- `docs/METHOD_HARDENING_002_REPORT.md`

The report must explicitly re-audit:

- `287|288`, `288|289`, `289|290`, `290|291` as structure/evolution-favored but direct-homolog-conflicted controls;
- `248|249`, `256|257` as historical insertion-support / modern-conflict controls;
- potential Pareto-reviewable sites outside the previous strict 10.

Stop and return for ChatGPT/user review after this task. Do not start downstream modeling automatically.

Expected task-end state:

- `READY_FOR_CONFLICT_AWARE_TAG_SITE_MODELING`, or
- `NO_HIGH_CONFIDENCE_TARGETED_SITE`, or
- `METHOD_HARDENING_BLOCKED`.

## P1 — Insertion-specific Tag × Site structural modeling — BLOCKED PENDING METHOD_HARDENING_002

Only if the next review authorizes a reduced modeling set:

- model selected MAP8/HA/G196 site × tag pairs;
- use insertion-specific loop/conformer sampling rather than one AlphaFold model;
- where practical combine mature loop-remodel/KIC-like sampling with AlphaFold/ColabFold ensembles;
- compare closure success, local strain, native-domain RMSD, local backbone displacement, clashes, native-contact changes, interface effects and tag exposure;
- use current A89 hexamers for comparative oligomer-interface risk, not proof of native pore geometry.

## P2 — Targeted MD

Only after a small number of tagged constructs survive insertion-specific structural perturbation analysis.

Do not return to generic WT-only MD as the current priority.

## P2 — Exact nucleotide/RNA audit

Mandatory before final construct recommendation, but blocked until the exact experimental nucleotide construct/context is supplied.

Do not infer the experimental RNA by back-translation.

## Experimental gold-standard option

If computation remains conflicted, prefer HRV-A89-specific empirical insertion-tolerance evidence over indefinite computational refinement.

Conceptual options:

- broad A89 2C insertion-tolerance mapping if resources permit;
- otherwise a reduced empirical validation panel spanning distinct evidence classes and negative controls.

The computational workflow should identify the most informative classes to validate, not claim that a site is safe.

## Repository maintenance

- keep `PROJECT_STATE.md` current after every decision-changing phase;
- update `ANALYSIS_INDEX.md` whenever a new report supersedes or changes the workflow;
- append decisions to `DECISIONS.md` rather than silently reversing them;
- store raw numerical outputs under `data/` or `results/`;
- record source accession/DOI and evidence class for every literature-derived constraint;
- record software/environment versions for decision-changing analyses;
- install missing mature software in user space rather than silently substituting weaker custom approximations;
- do not commit software installations, package caches, bulk MD trajectories or restart files.
