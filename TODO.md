# TODO

Last updated: 2026-08-22

Priority order is scientific, not cosmetic.

## GPU_RECOVERY_004 — COMPLETED

Status: **READY_FOR_CONFLICT_AWARE_TAG_SITE_MODELING**

Primary report:

- `docs/GPU_RECOVERY_004_REPORT.md`

Primary outputs:

- `data/tag_specific_plm_scores_v2_gpu.tsv`
- `data/tag_specific_consensus_v2_gpu.tsv`
- `data/candidate_junctions_v5_plm_gpu.tsv`
- `data/computational_review_set_v2_plm_gpu.tsv`

## CONTINUOUS_TAG_SITE_MODELING_005 — COMPLETED / PARTIAL

Status: **TAG_SITE_MODELING_PARTIALLY_COMPLETE**

Task:

- `tasks/CONTINUOUS_TAG_SITE_MODELING_005.md`

The task moved from all-320 discovery into a compact site × tag structural perturbation panel.

Primary report:

- `docs/CONTINUOUS_TAG_SITE_MODELING_005_REPORT.md`

Run log:

- `docs/CONTINUOUS_TAG_SITE_MODELING_005_RUN_LOG.md`

### Completed / deferred methods

Completed:

- compact 33-junction x 4-tag panel;
- WT oligomer-context compatibility;
- WT residue-contact-network anchor analysis;
- targeted reuse of V5/V2 direct/evolutionary/PLM layers;
- cross-method robustness with deferred-method flags.

Deferred:

- insertion-specific structure-prediction ensembles: no mature local ColabFold/AlphaFold/OpenFold/ESMFold workflow found;
- mature loop/backbone remodeling: no Rosetta/KIC-like workflow found;
- local energetic/frustration analysis: no FoldX/Rosetta/local-frustration workflow found.

### Outputs

- `data/tag_site_modeling_panel_v1.tsv`
- `results/tag_site_modeling_005/environment_and_method_inventory.tsv`
- `data/tag_site_structure_ensemble_metrics_v1.tsv`
- `data/tag_site_loop_feasibility_v1.tsv`
- `data/tag_site_energy_context_v1.tsv`
- `data/tag_site_contact_network_v1.tsv`
- `data/tag_site_hexamer_context_v1.tsv`
- `data/tag_site_integrated_perturbation_v1.tsv`
- `results/tag_site_modeling_005/cross_method_robustness.tsv`
- `docs/CONTINUOUS_TAG_SITE_MODELING_005_REPORT.md`

## CURRENT — ChatGPT/User Review Gate

Status: **REVIEW REQUIRED**

ChatGPT/user should decide whether to:

- authorize a dedicated mature structure-prediction / loop-remodeling recovery task;
- authorize targeted dynamics only after reviewing the partial evidence;
- prioritize HRV-A89-specific insertion phenotype generation;
- provide exact nucleotide construct context for later RNA/codon audit.

## Later work

### Targeted dynamic analysis

Only after a reduced site × tag set survives insertion-specific perturbation modeling.

### Exact nucleotide/RNA audit

Mandatory before final construct recommendation, but blocked until the exact experimental nucleotide construct/context is supplied.

## Repository maintenance

- keep `PROJECT_STATE.md`, `ACTIVE_TASK.md`, `ANALYSIS_INDEX.md`, `DECISIONS.md` and this file consistent;
- preserve versioned historical outputs;
- record software/environment versions and commands;
- commit small/medium data and reports, not package caches, model checkpoints, bulk structure ensembles or MD trajectories.
