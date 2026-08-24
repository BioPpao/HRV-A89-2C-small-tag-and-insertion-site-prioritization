# TODO

Last updated: 2026-08-24

Priority order is scientific, not cosmetic.

## CANDIDATE_PANEL_EXPANSION_008 — COMPLETE

Status: **READY_FOR_BROAD_TARGETED_DYNAMICS**

Stable checkpoint branch:

`analysis/candidate-panel-008`

Primary report:

- `docs/CANDIDATE_PANEL_EXPANSION_008_REPORT.md`

Current review package:

- `data/final_candidate_panel_draft_v1.tsv`
- `data/proposed_targeted_dynamics_panel_v1.tsv`
- `results/candidate_panel_008/ranking_robustness_v1.tsv`

The draft is useful but remains biased toward the contiguous C-terminal `287–291` neighborhood and MAP8, and several technical layers remained incomplete.

## CURRENT — BROAD_DYNAMICS_AND_RECOVERY_009

Status: **AUTHORIZED / PRE-DYNAMICS RECOVERY + BROAD REPLICATED DYNAMICS**

Branch:

`analysis/broad-dynamics-009`

Task:

- `tasks/BROAD_DYNAMICS_AND_RECOVERY_009.md`

### Phase A — resolve unfinished 008 work

1. audit/recover the `248|249 × HA` OpenMM `Particle coordinate is nan` failure;
2. install/configure an open disorder predictor and complete the missing all-320 disorder layer;
3. run focused local tagged dimer/trimer ColabFold accommodation modeling;
4. structure-model PA14 and AGIA at representative candidate junctions;
5. update pre-dynamics feature/ranking evidence.

### Phase B — remove panel-selection bias

Create a balanced dynamics panel with approximately 10–12 tagged constructs plus WT.

Require:

- at least 4 genuinely distinct site regions;
- at least 3 tag systems;
- no automatic domination by adjacent `287–291` junctions;
- at least one hard-negative/control and one mechanistic conflict control;
- selection rationale frozen before MD results are generated.

### Phase C — broad replicated dynamics

Primary comparative system:

- native A89 2C residues `112–321`;
- exact tag retained;
- equivalent terminal treatment across WT and tagged constructs;
- explicit solvent;
- one consistent force field/solvent model;
- broad apo/protein-only screening state.

Default production target:

- 3 independent replicas × 50 ns per system.

Minimum fallback before selective extension:

- 3 × 20 ns for every panel member.

Prefer independent replica breadth over one long trajectory.

### Phase D — dynamics analysis

Required analyses include:

- native-domain RMSD;
- per-residue/local RMSF;
- tag RMSF;
- tag exposure persistence;
- secondary-structure persistence;
- native/local contact persistence;
- tag-native distance distributions;
- replica convergence;
- bootstrap/effect estimates versus WT;
- dynamic cross-correlation/covariance;
- residue-network/community/path perturbation where reproducible.

### Phase E — revised candidate panel

Create:

- `data/final_candidate_panel_v2_dynamics.tsv`
- `results/broad_dynamics_009/ranking_robustness_v2.tsv`
- `docs/BROAD_DYNAMICS_AND_RECOVERY_009_REPORT.md`

Final ranking must remain multi-objective and conflict-aware; no opaque total score.

## Required open software stack

Reuse functioning tools where possible and install missing tools in user space only when needed:

- GROMACS 2024.x or best working cluster module;
- ColabFold existing environment;
- OpenMM / PDBFixer for structural sanitation/QC;
- MDAnalysis / MDTraj;
- DSSP-compatible analysis;
- NumPy / SciPy / pandas;
- NetworkX;
- IUPred2A/ANCHOR2 only if accessible without restricted/manual license, otherwise a mature open disorder predictor such as metapredict.

Do not pursue Rosetta/FoldX or other restricted-license dependencies.

## Expected 009 outputs

- `results/broad_dynamics_009/environment_inventory.tsv`
- `results/broad_dynamics_009/input_integrity_qc.tsv`
- `results/broad_dynamics_009/openmm_248_249_HA_root_cause.tsv`
- `docs/OPENMM_248_249_HA_FAILURE_AUDIT.md`
- `data/hrvA89_2C_disorder_v1.tsv`
- `data/junction_feature_matrix_v7_pre_dynamics.tsv`
- `docs/DISORDER_LAYER_RECOVERY_V1.md`
- `data/local_multimer_tag_context_v2.tsv`
- `docs/LOCAL_MULTIMER_RECOVERY_V2.md`
- `data/exploratory_tag_structure_panel_v1.tsv`
- `data/exploratory_tag_structure_metrics_v1.tsv`
- `docs/EXPLORATORY_TAG_SCREEN_V1.md`
- `data/balanced_targeted_dynamics_panel_v2.tsv`
- `results/broad_dynamics_009/system_manifest.tsv`
- `results/broad_dynamics_009/residue_mapping.tsv`
- `results/broad_dynamics_009/preproduction_qc.tsv`
- `results/broad_dynamics_009/production_manifest.tsv`
- `results/broad_dynamics_009/replica_completion.tsv`
- `data/dynamics_replica_qc_v1.tsv`
- `docs/DYNAMICS_QC_V1.md`
- `data/broad_dynamics_metrics_v1.tsv`
- `data/tag_exposure_dynamics_v1.tsv`
- `data/contact_persistence_dynamics_v1.tsv`
- `data/dynamic_network_perturbation_v1.tsv`
- `docs/DYNAMIC_NETWORK_ANALYSIS_V1.md`
- `data/final_candidate_panel_v2_dynamics.tsv`
- `results/broad_dynamics_009/ranking_robustness_v2.tsv`
- `docs/BROAD_DYNAMICS_AND_RECOVERY_009_REPORT.md`

## Later — exact nucleotide/RNA gate

Mandatory before final wet-lab construct design. Requires the real experimental nucleotide context.

## Repository maintenance

Keep `PROJECT_STATE.md`, `ACTIVE_TASK.md`, `ANALYSIS_INDEX.md`, `DECISIONS.md` and this file consistent. Preserve historical outputs and avoid committing bulk trajectories, model checkpoints, package caches or large databases.
