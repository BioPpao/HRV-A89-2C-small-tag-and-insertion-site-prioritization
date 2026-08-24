# BROAD_DYNAMICS_AND_RECOVERY_009 Run Log

Task: `BROAD_DYNAMICS_AND_RECOVERY_009`

Branch: `analysis/broad-dynamics-009`

Start state: `BROAD_DYNAMICS_AND_RECOVERY_009_AUTHORIZED`

## 2026-08-24 checkpoint

Repository and scheduler checks were run on `admin1`. GPU work was submitted through Slurm rather than assuming login-node GPU visibility.

Completed outputs:

- `results/broad_dynamics_009/environment_inventory.tsv`
- `results/broad_dynamics_009/input_integrity_qc.tsv`
- `results/broad_dynamics_009/software_versions.tsv`
- `results/broad_dynamics_009/openmm_248_249_HA_root_cause.tsv`
- `docs/OPENMM_248_249_HA_FAILURE_AUDIT.md`
- `data/hrvA89_2C_disorder_v1.tsv`
- `data/junction_feature_matrix_v7_pre_dynamics.tsv`
- `docs/DISORDER_LAYER_RECOVERY_V1.md`
- `data/local_multimer_tag_context_v2.tsv`
- `results/broad_dynamics_009/local_multimer_manifest.tsv`
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

Software notes:

- GROMACS 2024.2 CUDA module is available.
- Existing `.tools/envs/open_structure_007` has ColabFold 1.5.3, OpenMM, PDBFixer, MDAnalysis, MDTraj, pandas, SciPy and NetworkX.
- `metapredict` installation was attempted but cancelled after a slow 526 MB PyTorch dependency download; no lightweight `iupred2a` or `metapredict-lite` pip package was available. Disorder V1 therefore uses an explicit lower-quality composition proxy and is not decision-grade.

OpenMM failure audit:

- `248|249 x HA`, seed `032`, rank `001` reproducibly fails OpenMM CPU implicit minimization with `Particle coordinate is nan`.
- `248|249 x HA`, seed `031`, rank `002` completes the same repeat.
- Final class: `MODEL_SPECIFIC_GEOMETRY_FAILURE`.
- This is not biological evidence against `248|249 x HA`.

Slurm jobs:

- `164287`: `bd009_extag`, `scripts/broad_dynamics_009_exploratory_colabfold.sbatch`, RTX3090 `gpu16`, completed `0:0`; produced 16 PDB rows.

Blockers / pending:

- local multimer ColabFold modeling is defined but not completed;
- PA14/AGIA single-sequence ColabFold completed, but no construct is competitive with core tags because model confidence is low and exploratory OpenMM QC was not completed in this checkpoint;
- GROMACS system preparation and replicated MD are not started;
- trajectory QC, dynamics metrics and network outputs are placeholders with explicit `not_available_no_completed_md` / `excluded_no_trajectory` status.

Current final state for this checkpoint:

`BROAD_DYNAMICS_PARTIALLY_COMPLETE`
