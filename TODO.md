# TODO

Last updated: 2026-08-22

Priority order is scientific, not cosmetic.

## CONTINUOUS_TAG_SITE_MODELING_005 — COMPLETED / PARTIAL

Status: **TAG_SITE_MODELING_PARTIALLY_COMPLETE**

Primary report:

- `docs/CONTINUOUS_TAG_SITE_MODELING_005_REPORT.md`

Completed:

- 33-junction x 4-tag compact panel;
- WT oligomer-context analysis;
- WT residue-contact-network anchors;
- direct/evolutionary/PLM evidence integration;
- cross-method robustness with explicit deferred flags.

Deferred by missing mature software:

- actual inserted-structure ensembles;
- mature loop/backbone remodeling;
- local FoldX/Rosetta/frustration energy analysis;
- WT-vs-tagged contact-map deltas;
- tagged hexamer clash/interface deltas.

## CURRENT — STRUCTURE_STACK_RECOVERY_006

Status: **AUTHORIZED / CONTINUITY-FIRST ENVIRONMENT + MODELING TASK**

Task:

- `tasks/STRUCTURE_STACK_RECOVERY_006.md`

### Primary engine decision

Install/configure **ColabFold / `colabfold_batch`** as the main structure-prediction engine.

Do not install standalone AlphaFold, OpenFold and ESMFold by default because they duplicate the same evidence class and increase environment/storage complexity. Only use an alternative structure engine if ColabFold cannot be made scientifically usable after reasonable recovery attempts.

### Required blocker-removal work

1. storage/quota audit;
2. Slurm/GPU and network-context audit;
3. ColabFold/JAX/OpenMM environment installation;
4. real WT A89 2C GPU smoke test;
5. tiered inserted-construct panel;
6. multi-model/multi-seed ColabFold ensembles;
7. actual WT-vs-tagged perturbation metrics;
8. OpenMM relaxation/QC;
9. tagged hexamer clash/interface analysis;
10. tagged contact-network delta analysis;
11. integrated structural re-ranking and robustness.

### Additional orthogonal methods

Attempt when legally/technically available:

- Rosetta/PyRosetta loop/backbone remodeling;
- FoldX energetic analysis;
- local-frustration analysis;
- US-align/TM-align structural comparison.

Rosetta and FoldX are license-governed. If manual user license/download action is required, mark only that module `DEFERRED_LICENSE_USER_ACTION` and continue the remaining task.

### Storage policy

- do not install full local ColabFold/MMseqs databases unless clearly required and quota/storage is verified;
- prefer public MSA-server generation from the network-capable login context;
- cache A3M/MSA/model parameters in user/project-controlled paths;
- execute GPU inference via Slurm from cached inputs when compute-node networking is restricted;
- do not commit package caches, checkpoints or bulk prediction directories.

### Continuity policy

Do not stop the whole task because one tool, GPU partition, network route, licensed package or Git push fails.

Continue independent work, try mature alternatives, use login-node download/cache plus compute-node execution, and preserve local commits/results.

### Expected outputs

- `results/structure_stack_006/environment_inventory.tsv`
- `results/structure_stack_006/colabfold_smoke_test.tsv`
- `data/tag_site_structure_panel_v2.tsv`
- `results/structure_stack_006/prediction_manifest.tsv`
- `data/tag_site_structure_ensemble_metrics_v2.tsv`
- `data/tag_site_structure_perturbation_v2.tsv`
- `data/tag_site_loop_feasibility_v2.tsv`
- `data/tag_site_energy_context_v2.tsv`
- `data/tag_site_hexamer_context_v2_tagged.tsv`
- `data/tag_site_contact_network_v2_tagged.tsv`
- `data/tag_site_integrated_perturbation_v2_structure.tsv`
- `results/structure_stack_006/cross_method_robustness_v2.tsv`
- `docs/STRUCTURE_STACK_RECOVERY_006_REPORT.md`

### Final state expected

- `READY_FOR_TARGETED_DYNAMIC_ANALYSIS`
- `NO_COMPUTATIONAL_CONSENSUS_SITE`
- `STRUCTURE_STACK_PARTIALLY_COMPLETE`

## Later work

### Targeted dynamic analysis

Only after a reduced site × tag set survives real inserted-structure perturbation screening.

### Exact nucleotide/RNA audit

Mandatory before final construct recommendation, but blocked until the exact experimental nucleotide construct/context is supplied.

## Repository maintenance

- keep `PROJECT_STATE.md`, `ACTIVE_TASK.md`, `ANALYSIS_INDEX.md`, `DECISIONS.md` and this file consistent;
- preserve versioned historical outputs;
- record software/environment versions and commands;
- commit small/medium scientific data/reports, not package caches, checkpoints, full databases or bulk trajectories.
