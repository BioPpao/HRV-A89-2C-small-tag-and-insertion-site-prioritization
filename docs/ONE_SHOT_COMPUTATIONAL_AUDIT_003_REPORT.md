# ONE_SHOT_COMPUTATIONAL_AUDIT_003_REPORT

Status: **completed as far as scientifically valid; blocked at mandatory PLM stage**

Date: 2026-08-22

Final decision state: `METHOD_HARDENING_BLOCKED`

## Scope completed

Mandatory stages:

- Stage A1 EV-A71 substitution-tolerance integration: completed.
- Stage A2 continuous/Pareto all-320 re-ranking: completed.
- Stage A3 phylogeny-aware independent natural-indel analysis: completed.
- Stage A4 MAP8/HA/G196 tag-specific PLM scan: blocked by missing mature PLM/GPU software and rejected package installation.
- Stage A5 integrated V4 matrix/report: completed with PLM-blocker columns.
- Stage B robustness / negative-control audit: completed for non-PLM evidence layers.
- Stage C cross-tag consensus/disagreement: blocked because PLM scores are unavailable.
- Stage D reduced computational review set: completed as a conflict-aware review set, not an experimental recommendation.
- Stage E lightweight structural feasibility triage: deferred because no mature reproducible ColabFold/Rosetta/PyRosetta workflow was available.
- Stage F final synthesis: completed.

No long MD, experimental protocol design, final construct recommendation, RNA/codon design, or safe/validated-site claim was made.

## Software and environment

User-space environment:

- `.tools/envs/hrv2c-one-shot`
- `envs/hrv2c-one-shot.yml`
- `results/one_shot_003/one_shot_003_micromamba_list.tsv`

Core versions:

- Python 3.11.15
- pandas 3.0.5
- Biopython 1.88
- numpy 2.4.6
- scipy 1.17.1
- scikit-learn 1.9.0
- MAFFT 7.526
- FastTree 2.2.0
- IQ-TREE 3.1.3

GPU/PLM status:

- no `nvidia-smi`;
- no visible `/dev/nvidia*`;
- no visible `/proc/driver/nvidia/gpus`;
- no existing `torch`, `transformers`, or `esm`;
- attempted `torch transformers safetensors` installation was rejected by platform usage-limit escalation.

## Generated files

Core data:

- `data/evA71_2C_substitution_tolerance_to_A89_v1.tsv`
- `data/pareto_junction_frontier_v1.tsv`
- `data/hrvA_independent_indel_events_v1.tsv`
- `data/tag_specific_plm_scores_v1.tsv`
- `data/tag_specific_consensus_v1.tsv`
- `data/computational_review_set_v1.tsv`
- `data/candidate_junctions_v4_method_hardening.tsv`
- `data/hrvA_2C_alignment_v2_sanitized_for_tree.fasta`
- `data/hrvA_2C_tree_name_map_v1.tsv`
- `data/hrvA_2C_fasttree_v1.nwk`

QC/results:

- `results/method_hardening_002/substitution_mapping_qc.tsv`
- `results/method_hardening_002/pareto_sensitivity.tsv`
- `results/method_hardening_002/phylogeny_qc.tsv`
- `results/method_hardening_002/phylogeny_fasttree_v1.txt`
- `results/method_hardening_002/plm_qc.tsv`
- `results/one_shot_003/ranking_robustness.tsv`
- `results/one_shot_003/negative_control_audit.tsv`
- `results/one_shot_003/tag_landscape_correlations.tsv`
- `results/one_shot_003/lightweight_structural_triage_status.tsv`

Reports:

- `docs/METHOD_HARDENING_002_REPORT.md`
- `docs/PHYLOGENY_AWARE_INDEL_V1.md`
- `docs/TAG_SPECIFIC_PLM_SCAN_V1.md`
- `docs/RANKING_ROBUSTNESS_AUDIT_V1.md`
- `docs/TAG_SPECIFIC_CONSENSUS_V1.md`
- `docs/COMPUTATIONAL_REVIEW_SET_V1.md`
- `docs/LIGHTWEIGHT_STRUCTURAL_TRIAGE_V1.md`
- `docs/ONE_SHOT_COMPUTATIONAL_AUDIT_003_RUN_LOG.md`

## QC summary

Substitution mapping:

- EV-A71 2C substitution rows: 6,580.
- A89 junction rows: 320.
- exact-aligned rows: 315.
- ambiguous rows: 5.
- rows with flank/window substitution scores: 320.

Phylogeny-aware indels:

- FastTree tips: 77.
- A89 junction rows: 320.
- insertion tip-presence junctions: 1.
- insertion parsimony-change junctions: 1.
- local-deletion tip-presence junctions: 12.
- local-deletion parsimony-change junctions: 12.

Pareto sensitivity:

- structure_only: 18 Pareto rows.
- structure_plus_direct: 37 Pareto rows.
- no_conservation: 81 Pareto rows.
- no_substitution: 67 Pareto rows.
- full: 103 Pareto rows.

V4 class counts:

- `direct_homolog_strongly_unfavorable`: 151.
- `hard_excluded`: 61.
- `pareto_reviewable_direct_conflicted`: 49.
- `weak_pareto_reviewable_direct_conflicted`: 46.
- `conflict_control`: 8.
- `mapping_uncertain`: 5.

PLM:

- planned rows: 1,280.
- completed PLM rows: 0.
- status: `blocked_software_unavailable`.

## Required synthesis answers

### 1. Did any junction outside the previous strict 10 become robustly Pareto-reviewable?

Yes, but none becomes high-confidence.

Several outside-strict rows are Pareto-reviewable across multiple non-PLM metric subsets. Examples in the review set include:

- `203|204`: least-deleterious EV-A71 handle-insertion outside-strict row, but still unfavorable (`-3.061137`);
- `224|225`: CORE_CAUTION and tied with `289|290` for a less-deleterious insertion score (`-3.518970`), but still unfavorable;
- `245|246`, `249|250`, `251|252`: Pareto/context rows around the historical-conflict region.

These remain direct-homolog-conflicted and are not promoted as targeted sites.

### 2. Did EV-A71 substitution tolerance materially change site interpretation?

No decisive promotion.

Substitution tolerance adds local context, especially around some N-terminal/C-terminal windows, but it does not override globally unfavorable EV-A71 handle-insertion phenotype or hard functional tiers.

### 3. Did phylogeny-aware independent-indel reconstruction change V2 indel conclusions?

Yes, it made indel support more conservative.

V2 type-aware indel support does not usually translate into repeated independent events. `248|249` remains the strongest useful conflict row with independent indel lower bound 2, but direct insertion phenotype remains unfavorable.

### 4. How different are MAP8, HA and G196 PLM landscapes?

Unknown.

PLM scoring was blocked. `data/tag_specific_plm_scores_v1.tsv` records all planned MAP8/HA/G196 rows with blocked status and no fabricated scores.

### 5. Are old `287|288-290|291` sites still scientifically useful?

Yes, but only as conflict controls.

They retain structural/evolutionary interest, and `289|290` is among the less-deleterious EV-A71 insertion rows, but all remain unfavorable in direct homolog insertion phenotype.

### 6. Are `248|249` and `256|257` still useful historical-conflict controls?

Yes.

`248|249` retains historical/rescue and sparse independent-indel context. `256|257` remains a historical-conflict control. Neither becomes a preferred targeted site.

### 7. Is the candidate landscape robust to reasonable metric choices?

No.

Pareto membership varies substantially by metric subset, and many Pareto rows are biologically high-risk or direct-homolog-conflicted.

### 8. What reduced computational review set should move forward?

Use `data/computational_review_set_v1.tsv` only as a review set, not a modeling authorization.

It contains 17 rows spanning:

- least-deleterious direct-insertion outside-strict controls;
- old strict C-terminal conflict controls;
- historical/indel conflict controls;
- near-miss/mapping-uncertain controls;
- negative-control hard exclusions;
- representative Pareto-reviewable direct-conflicted rows.

### 9. Did lightweight structural triage materially change the review set?

No. Stage E was deferred because no mature reproducible structure-prediction or loop-remodeling workflow was available.

### 10. Final state

`METHOD_HARDENING_BLOCKED`

Reason:

- CPU method-hardening modules completed;
- mandatory PLM module could not be run;
- cross-tag consensus therefore cannot be assessed;
- Stage E mature structural triage was unavailable;
- evidence remains insufficient for `READY_FOR_CONFLICT_AWARE_TAG_SITE_MODELING`.

### 11. Unresolved uncertainties

- MAP8/HA/G196 tag-specific PLM landscapes are missing.
- No HRV-A89-specific insertion phenotype exists.
- EV-A71 insertional-handle phenotype is homolog and insertion-sequence specific.
- Stage E insertion-specific structural feasibility remains deferred.
- Exact experimental RNA/codon context remains unavailable.

## Git checkpoint note

During this run, package/environment setup succeeded, but `git add` for the setup checkpoint was rejected by the platform escalation reviewer due usage-limit state. Work continued locally as instructed, and the failure is recorded in `docs/ONE_SHOT_COMPUTATIONAL_AUDIT_003_RUN_LOG.md`.

Final repository push may require a future session with Git-write approval available.
