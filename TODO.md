# TODO

Last updated: 2026-08-22

Priority order is scientific, not cosmetic. Do not jump to Tag × Site modeling before higher-information direct insertion evidence is integrated.

## P0 — CONSERVATION_001 completed, V1 provisional

Preserve all V1 outputs for provenance only. Decision-making uses CONSERVATION_002/V2.

## P0 — CONSERVATION_002 decision-grade QC hardening — COMPLETE

Completed in:

- `docs/CONSERVATION_SCREEN_V2.md`
- `docs/CANDIDATE_JUNCTION_QC_V1.md`
- `data/candidate_junctions_v2.tsv`
- `data/hrvA_conservation_per_junction_v2.tsv`
- `data/junction_structural_metrics_v2.tsv`

## P0 — DIRECT_INDEL_001 — COMPLETE

Rationale:

The present shortlist is based mainly on WT structural geometry, functional mapping and near-HRV evolutionary context. These are useful proxies but do not directly measure insertion tolerance.

Before Tag × Site modeling, direct enterovirus 2C insertion/deletion viral-fitness evidence was integrated.

Completed work:

- verified the EV-A71 proteome-scale deep insertion/deletion study and data provenance;
- acquired processed mutation-fitness data from the publication code/data repository and Dryad metadata;
- confirmed EV-A71 Tainan/4643/98 accession `MW298156`, mature 2C nt `4079-5065`, 329 aa;
- extracted mature EV-A71 2C insertion/deletion/substitution data;
- mapped EV-A71 2C junctions to HRV-A89 2C with MAFFT mature-sequence alignment;
- projected direct evidence to all 320 A89 junctions;
- rebuilt an integrated V3 candidate table without overwriting V2;
- identified no favorable direct insertion-supported sites, either in the current strict cluster or outside it.

Task specification:

- `tasks/DIRECT_INDEL_001.md`

Strategic audit:

- `docs/METHOD_GAP_AND_NEXT_EVIDENCE_AUDIT_V1.md`

Outputs:

- `docs/EV71_2C_DIRECT_INDEL_MAPPING_V1.md`
- `docs/DIRECT_INDEL_001_RUN_LOG.md`
- `data/evA71_2C_direct_indel_to_A89_v1.tsv`
- `data/candidate_junctions_v3_direct_indel.tsv`
- `references/direct_indel_001/source_records_v1.tsv`

Decision state:

- `DIRECT_EVIDENCE_REQUIRES_SHORTLIST_REVISION`

Do not start Tag × Site modeling automatically after completion; ChatGPT/user review remains mandatory.

## P0 — CURRENT: Candidate-junction shortlist re-audit after direct InDel evidence

After `DIRECT_INDEL_001`:

- review `DIRECT_EVIDENCE_REQUIRES_SHORTLIST_REVISION`;
- decide whether `NO_TARGETED_SITE` / targeted empirical insertion-library strategy is the next project move;
- decide whether any conflict-aware modeling/control set is still worth authorizing despite unfavorable direct insertion evidence;
- if ambiguity remains, authorize a new explicit method-hardening task rather than starting Tag × Site modeling automatically.

Planned deliverable:

- ChatGPT/user decision and a new task file if further execution is authorized.

## P1 — Optional method hardening if ambiguity remains

Only if direct InDel evidence leaves material uncertainty:

- phylogeny-aware site-rate analysis rather than relying only on entropy/identity;
- infer independent natural-indel events rather than counting inherited descendant sequences as repeated events;
- continuous/Pareto structural ranking to reduce hard-threshold bias;
- protein-language-model generic insertion scan as an orthogonal secondary signal.

These are supporting analyses. They must not override direct phenotype or hard functional evidence.

## P2 — Tag × Site insertion-specific modeling

Only after the direct-evidence shortlist review:

- model MAP8, HA and selected G196 forms only on a reduced site set;
- use insertion-specific conformational sampling rather than relying only on one tagged AlphaFold model;
- where practical, combine Rosetta loop/remodel/KIC-like sampling with AlphaFold/ColabFold ensembles;
- compare loop closure/strain, native-domain RMSD, secondary structure, clashes, interface/pore effects and tag exposure;
- keep tag flexibility/low confidence separate from native 2C perturbation.

Planned deliverables:

- `data/tag_site_perturbation_metrics_v1.tsv`
- `docs/TAG_SITE_MODELING_V1.md`

## P3 — Targeted MD

Use MD only after a small number of tagged constructs survive structural perturbation screening.

Do not return to generic WT-only MD as the current priority.

## P3 — Exact nucleotide/RNA audit

Mandatory before final construct recommendation, but blocked until the exact experimental nucleotide construct/context is supplied.

Do not infer the experimental RNA by back-translation.

## Experimental gold-standard option

If resources allow, prioritize HRV-A89-specific insertion-tolerance data over indefinite computational refinement:

- ideal: full 320-junction 2C deep insertion scan;
- practical alternative: targeted 20–30-junction panel spanning positive, conflict and negative evidence classes;
- use replicon/viral fitness as the biological acceptance/training layer.

## Repository maintenance

- keep `PROJECT_STATE.md` current after every decision-changing phase;
- update `ANALYSIS_INDEX.md` whenever a new report supersedes or changes the workflow;
- append changes to `DECISIONS.md` rather than silently reversing them;
- store raw numerical outputs under `data/` or `results/`, not only inside prose reports;
- record source accession/DOI and evidence class for every new literature-derived constraint;
- record software/environment versions for decision-changing analyses;
- if appropriate software is absent, install it in user space rather than silently replacing it with a materially weaker method;
- do not commit software installations, package caches, bulk MD trajectories or restart files.
