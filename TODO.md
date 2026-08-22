# TODO

Last updated: 2026-08-23

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
- cross-method robustness with deferred flags.

The major remaining gap is real inserted-structure modeling.

## STRUCTURE_STACK_RECOVERY_006 — SUPERSEDED AS EXECUTION TASK

Retained as planning provenance. It included Rosetta/FoldX options, but the current project should not depend on restricted-license software.

## OPEN_STRUCTURE_PIPELINE_007 — COMPLETE

Status: **READY_FOR_TARGETED_DYNAMIC_ANALYSIS**

Task:

- `tasks/OPEN_STRUCTURE_PIPELINE_007.md`

### Primary open stack

- ColabFold / `colabfold_batch`;
- OpenMM geometry cleanup/QC;
- US-align/TM-align;
- MDAnalysis/MDTraj;
- DSSP-compatible secondary-structure analysis;
- transparent WT-vs-tagged contact networks;
- actual tagged placement into existing A89 hexamer hypotheses.

Do not require Rosetta, PyRosetta or FoldX.

### Completed blocker-removal work

1. storage/quota/inode audit;
2. Slurm/GPU/network-context audit;
3. ColabFold/JAX/OpenMM open environment installation;
4. real WT 321-aa A89 2C smoke test;
5. tiered inserted-construct panel;
6. multi-model/multi-seed ColabFold ensembles;
7. WT-vs-tagged structural perturbation metrics;
8. OpenMM geometry QC;
9. secondary-structure/accessibility changes;
10. actual tagged hexamer clash/interface analysis;
11. actual WT-vs-tagged contact-network analysis;
12. integrated open-tool re-ranking and robustness.

### Storage policy

- do not install full local ColabFold/MMseqs databases unless clearly necessary and explicitly justified;
- prefer public MSA-server generation from the network-capable login node;
- cache A3M/MSA/model parameters under controlled paths;
- run GPU inference via Slurm from cached inputs when compute-node networking is restricted;
- do not commit package caches, checkpoints, databases or bulk redundant prediction outputs.

### Continuity policy

Do not stop the whole task because the current shell has no GPU, a GPU job is pending, a compute node lacks internet, one package path fails, or Git push temporarily fails.

Use Slurm, login-node downloads/cache, isolated compatible environments, mature open alternatives, CPU-side preparation while GPU work waits, and local commits/results.

### Expected outputs

- `results/open_structure_007/environment_inventory.tsv`
- `results/open_structure_007/colabfold_smoke_test.tsv`
- `data/tag_site_structure_panel_v3_open.tsv`
- `results/open_structure_007/prediction_manifest.tsv`
- `data/tag_site_structure_ensemble_metrics_v3_open.tsv`
- `data/tag_site_structure_perturbation_v3_open.tsv`
- `data/tag_site_openmm_qc_v1.tsv`
- `data/tag_site_secondary_structure_accessibility_v1.tsv`
- `data/tag_site_hexamer_context_v3_open.tsv`
- `data/tag_site_contact_network_v3_open.tsv`
- `data/tag_site_integrated_perturbation_v3_open.tsv`
- `results/open_structure_007/cross_method_robustness_v3.tsv`
- `docs/OPEN_STRUCTURE_PIPELINE_007_REPORT.md`

All generated. Use `docs/OPEN_STRUCTURE_PIPELINE_007_REPORT.md` and `data/tag_site_integrated_perturbation_v3_open.tsv` as the current open-structure evidence source.

### Final state expected

- `READY_FOR_TARGETED_DYNAMIC_ANALYSIS`
- `NO_COMPUTATIONAL_CONSENSUS_SITE`
- `OPEN_STRUCTURE_PIPELINE_PARTIALLY_COMPLETE`

## Later work

### Targeted dynamic analysis

Now eligible for ChatGPT/user decision. Do not start without a new authorized task. The likely review focus is `289|290 x MAP8`, `289|290 x G196_minimal`, and conflict checks around `288|289`, `290|291`, `224|225`, and `248|249`.

### Exact nucleotide/RNA audit

Mandatory before final construct recommendation, but blocked until the exact experimental nucleotide construct/context is supplied.

## Repository maintenance

Keep `PROJECT_STATE.md`, `ACTIVE_TASK.md`, `ANALYSIS_INDEX.md`, `DECISIONS.md` and this file consistent. Preserve versioned historical outputs and record software/environment versions and commands.
