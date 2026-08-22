# METHOD_HARDENING_002

Status: **AUTHORIZED / NEXT EXECUTION TASK**

Date: 2026-08-22

Branch: `analysis/conservation-002`

## Objective

Re-rank all 320 HRV-A89 2C peptide junctions after `DIRECT_INDEL_001` using higher-resolution continuous and orthogonal evidence, without prematurely entering Tag × Site structural modeling.

The task must distinguish:

- strong direct homolog negative evidence;
- hard biological exclusions;
- continuous WT structural risk;
- evolutionary/indel evidence;
- tag-specific sequence perturbation.

The endpoint is a revised evidence matrix and candidate classes, not a final experimental site.

## Scientific state entering the task

- `DIRECT_INDEL_001` is complete.
- EV-A71 2C direct 8-aa handle insertion phenotype is unfavorable at all mapped A89 junctions.
- `287|288–290|291` is no longer a supported targeted shortlist; it is a structure/evolution-favored but direct-homolog-conflicted cluster.
- `248|249` and `256|257` are historical insertion-support / modern-conflict controls.
- Current project-level state is `NO_HIGH_CONFIDENCE_TARGETED_SITE_YET`, not proof that all A89 insertions are impossible.

Read before execution:

1. `PROJECT_STATE.md`
2. `docs/METHOD_GAP_AND_NEXT_EVIDENCE_AUDIT_V2.md`
3. `docs/EV71_2C_DIRECT_INDEL_MAPPING_V1.md`
4. `docs/CONSERVATION_SCREEN_V2.md`
5. `data/candidate_junctions_v3_direct_indel.tsv`
6. `AGENTS.md`
7. `WORKFLOW.md`

## Module 1 — EV-A71 substitution-tolerance integration

Use the already acquired direct EV-A71 dataset/provenance from `DIRECT_INDEL_001`.

Required work:

- verify which substitution measurements belong to mature EV-A71 2C;
- preserve residue-level and local-window substitution metrics separately from insertion and deletion scores;
- map substitution-tolerance summaries to A89 using the existing mature-2C alignment/mapping;
- summarize around each A89 junction using transparent local windows (at minimum flanking residues and one broader local window);
- record mapping confidence and missingness;
- do not combine substitution and insertion into one score.

Suggested outputs:

- `data/evA71_2C_substitution_tolerance_to_A89_v1.tsv`
- `results/method_hardening_002/substitution_mapping_qc.tsv`

## Module 2 — continuous/Pareto all-320 ranking

Rebuild the site-discovery layer without using `strict_structural_pass` as the candidate gate.

Rules:

- retain all 320 junctions except explicitly documented hard biological exclusions;
- retain `strict_structural_pass` as an annotation only;
- use the continuous structural variables from `junction_structural_metrics_v2.tsv`;
- keep functional risk, direct phenotype, evolution and structure as separate dimensions;
- do not create an opaque weighted scalar score as the primary ranking;
- implement a Pareto/non-dominated analysis with clearly documented directionality for each metric;
- explicitly report sensitivity to reasonable metric subsets/scaling choices.

Required candidate classes should at least distinguish:

- hard-excluded;
- direct-homolog strongly unfavorable;
- conflict-aware review;
- Pareto-reviewable;
- unresolved/insufficient evidence.

Suggested outputs:

- `data/candidate_junctions_v4_method_hardening.tsv`
- `data/pareto_junction_frontier_v1.tsv`
- `results/method_hardening_002/pareto_sensitivity.tsv`

## Module 3 — phylogeny-aware natural-indel analysis

Improve on type-count-based V2 indel evidence.

Required work:

- use the curated HRV-A 2C panel from CONSERVATION_002;
- build or reuse a defensible HRV-A phylogeny with recorded method/software/version;
- reconstruct local insertion/deletion presence/absence histories;
- estimate the number of independent indel events for each relevant junction/window;
- distinguish recurrent independent events from one ancestral event inherited by many descendants;
- report uncertainty where alignment/ancestral reconstruction is ambiguous;
- do not treat descendant count as independent-event count.

Suggested outputs:

- `data/hrvA_independent_indel_events_v1.tsv`
- `results/method_hardening_002/phylogeny_qc.tsv`
- `docs/PHYLOGENY_AWARE_INDEL_V1.md`

## Module 4 — tag-specific protein-language-model insertion scan

Target tags:

- MAP8
- HA
- G196

Required work:

- define and record the exact amino-acid sequence used for each tag/modeling form;
- generate A89 WT-vs-inserted protein sequences for all 320 junctions for each tag;
- use a mature indel-capable protein-language-model scoring method if practically available;
- if using an ESM-family pseudo-log-likelihood approach, document the exact formulation, masking/scoring strategy and limitations for insertion sequences;
- report raw and normalized per-tag scores separately;
- include reproducibility metadata (model name/version/checkpoint/software);
- do not let PLM scores override direct homolog phenotype or hard functional exclusions.

Suggested outputs:

- `data/tag_specific_plm_scores_v1.tsv`
- `results/method_hardening_002/plm_qc.tsv`
- `docs/TAG_SPECIFIC_PLM_SCAN_V1.md`

## Integration

Create a new all-320 evidence matrix that retains, at minimum:

- junction;
- hard functional exclusion;
- graded functional tier;
- historical direct 2C genetics/insertion evidence;
- EV-A71 direct insertion score/context;
- EV-A71 deletion context;
- EV-A71 substitution-tolerance metrics;
- continuous monomer structural metrics;
- continuous hexamer/interface metrics;
- local secondary-structure metrics;
- HRV-A conservation V2 metrics;
- natural-indel V2 category;
- independent indel-event metrics;
- MAP8 PLM score;
- HA PLM score;
- G196 PLM score;
- Pareto membership/rank class;
- unresolved conflicts;
- mapping/QC flags.

Do not overwrite V1/V2/V3 tables.

Primary integrated output:

- `data/candidate_junctions_v4_method_hardening.tsv`

## Required report

Create:

- `docs/METHOD_HARDENING_002_REPORT.md`

The report must answer:

1. Did any site outside the old strict 10 become Pareto-reviewable?
2. Did substitution tolerance materially change the interpretation of any candidate region?
3. Did phylogeny-aware independent-indel analysis change the old natural-indel interpretation?
4. Do MAP8/HA/G196 show materially different site-specific PLM landscapes?
5. Are `287|288–290|291` still worth modeling as conflict controls?
6. Are `248|249` / `256|257` still worth retaining as historical-conflict controls?
7. Is there now enough evidence to authorize a reduced insertion-specific loop/AlphaFold modeling task?
8. If not, should the project state become `NO_HIGH_CONFIDENCE_TARGETED_SITE` and pivot to empirical validation?

## Guardrails

Do not:

- call any site safe, validated or experimentally proven for HRV-A89;
- start Tag × Site AlphaFold/ColabFold/Rosetta structural modeling;
- start MD;
- perform RNA/codon design without the exact experimental nucleotide construct;
- silently replace missing mature software with a materially weaker custom approximation;
- overwrite previous versioned outputs;
- collapse conflicting evidence into one hidden weighted score.

## Stop conditions

Stop and return for ChatGPT/user review when:

- all four modules are complete, or a blocker is documented;
- `candidate_junctions_v4_method_hardening.tsv` exists;
- the Pareto/evidence-class candidate set exists;
- the old C-terminal and literature-rescue hypotheses have been explicitly re-audited;
- `METHOD_HARDENING_002_REPORT.md` is complete;
- `PROJECT_STATE.md`, `TODO.md`, `ANALYSIS_INDEX.md`, `DECISIONS.md` and `ACTIVE_TASK.md` are updated consistently;
- no downstream modeling task has started automatically.

## Final decision state expected from this task

Use one of:

- `READY_FOR_CONFLICT_AWARE_TAG_SITE_MODELING`
- `NO_HIGH_CONFIDENCE_TARGETED_SITE`
- `METHOD_HARDENING_BLOCKED`

Do not invent another final state without documenting the reason.
