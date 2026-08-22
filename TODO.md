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

## CURRENT — CONTINUOUS_TAG_SITE_MODELING_005

Status: **AUTHORIZED / CONTINUITY-FIRST COMPUTATIONAL TASK**

Task:

- `tasks/CONTINUOUS_TAG_SITE_MODELING_005.md`

The task moves from all-320 discovery into a compact site × tag structural perturbation panel.

### Main missing computational methods to add

1. insertion-specific structure-prediction ensembles;
2. loop/backbone closure and conformational feasibility modeling;
3. local energetic/frustration analysis;
4. oligomer-context compatibility analysis;
5. residue-contact-network perturbation analysis;
6. targeted phylogeny-aware site-rate / coevolution / flexibility checks where defensible;
7. cross-method robustness analysis.

### Continuity policy

Do not stop the project because one tool, package, GPU, network route, scheduler context or Git push fails.

- If GPU is absent in the current shell, inspect Slurm and obtain/submit GPU execution where needed.
- Continue independent CPU modules while GPU jobs wait where useful.
- If compute-node network is blocked, prepare dependencies/checkpoints from a network-capable login context.
- If one preferred package fails, try another mature method in the same evidence class.
- If no mature substitute exists, mark only that module deferred and continue all independent work.
- If remote push fails, preserve local commits and continue.
- Do not rerun completed global analyses without a concrete QC reason.

### Planned outputs

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

### Final state expected

- `READY_FOR_TARGETED_DYNAMIC_ANALYSIS`
- `NO_COMPUTATIONAL_CONSENSUS_SITE`
- `TAG_SITE_MODELING_PARTIALLY_COMPLETE`

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
