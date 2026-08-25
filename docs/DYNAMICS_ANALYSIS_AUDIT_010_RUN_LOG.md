# DYNAMICS_ANALYSIS_AUDIT_010_RUN_LOG

Task: `DYNAMICS_ANALYSIS_AUDIT_AND_CANDIDATE_RERANK_010`

Branch: `analysis/dynamics-audit-010`

Start date: 2026-08-24

## Initial Repository State

- `git fetch origin` completed.
- Current branch confirmed as `analysis/dynamics-audit-010`.
- Working tree contained historical untracked Task 009 local multimer raw outputs under `results/broad_dynamics_009/local_multimer/output/`.
- Those raw files were not deleted, overwritten or staged.

## Required Files Read

Read in task-specified order:

1. `WORKFLOW.md`
2. `AGENTS.md`
3. `PROJECT_STATE.md`
4. `DECISIONS.md`
5. `ANALYSIS_INDEX.md`
6. `ACTIVE_TASK.md`
7. `tasks/DYNAMICS_ANALYSIS_AUDIT_AND_CANDIDATE_RERANK_010.md`
8. `docs/DYNAMICS_009_POSTHOC_AUDIT_V1.md`
9. `codex/TASK_010_OVERNIGHT_PROMPT.md`

Additional Task 010 inputs read:

- `docs/BROAD_DYNAMICS_AND_RECOVERY_009_REPORT.md`
- `docs/DYNAMICS_QC_V1.md`
- `docs/FINAL_CANDIDATE_PANEL_STRATEGY_V1.md`
- `docs/EV71_2C_DIRECT_INDEL_MAPPING_V1.md`
- `docs/2C_FUNCTIONAL_EXCLUSION_MAP_V3.md`
- `data/balanced_targeted_dynamics_panel_v2.tsv`
- `data/final_candidate_panel_v2_dynamics.tsv`
- `scripts/broad_dynamics_009_analyze_md.py`
- `scripts/broad_dynamics_009_gromacs_setup.py`
- `scripts/broad_dynamics_009_gmx_production.sbatch`
- `references/LITERATURE_EVIDENCE_REGISTRY.md`
- `INPUT_PROVENANCE.md`
- `TODO.md`

## Task 009 Untracked Local Multimer Inventory

Inventory file:

- `results/dynamics_audit_010/local_multimer_untracked_inventory.tsv`

Summary:

- 62 untracked files inventoried.
- Total size: 93,049,919 bytes.
- Types: 6 `.a3m`, 1 `.bibtex`, 19 `.json`, 12 `.pdb`, 18 `.png`, 6 `.txt`.

Handling decision:

- Preserve server-side as Task 009 provenance.
- Do not git-add raw local multimer output files because they are bulky/reproducible and all interpretable local multimer results are already captured in compact tables/reports.
- Commit only the Task 010 inventory and compact metrics/provenance files.

## Software Snapshot

Created:

- `results/dynamics_audit_010/software_versions.tsv`
- `results/dynamics_audit_010/environment_inventory.tsv`

Available mature tools confirmed:

- GROMACS 2024.2
- MDAnalysis 2.9.0
- MDTraj 1.10.3 with `shrake_rupley`

## PBC/RMSD Pilot

Pilot checks:

- MDAnalysis `unwrap(protein)` plus `center_in_box(protein)` worked on WT replica 1.
- GROMACS-native `trjconv -pbc mol -center` plus `gmx rms` worked with a custom `native_ca` index.
- MDTraj Shrake-Rupley SASA worked when fed MDAnalysis-corrected protein coordinates.

Important implementation note:

- MDTraj residue `resSeq` does not match project `sim_resid` for inserted-tag systems. Task 010 SASA mapping must use protein residue order from MDAnalysis/project mapping rather than MDTraj residue numbers.

## Corrected 20 ns Reanalysis

Script:

- `scripts/dynamics_audit_010_reanalyze.py`

Outputs:

- `data/broad_dynamics_metrics_v2_corrected.tsv`
- `data/contact_persistence_dynamics_v2_corrected.tsv`
- `data/tag_exposure_dynamics_v2_sasa.tsv`
- `data/dynamic_network_perturbation_v2_corrected.tsv`
- `results/dynamics_audit_010/time_truncation_stability.tsv`
- `results/dynamics_audit_010/replica_stability.tsv`
- `results/dynamics_audit_010/dynamics_rank_stability.tsv`
- `results/dynamics_audit_010/control_discrimination_audit.tsv`
- `results/dynamics_audit_010/pbc_rmsd_crossvalidation.tsv`

Summary:

- 39 / 39 legacy 20 ns trajectories were reanalyzed after MDAnalysis unwrap/center PBC handling.
- GROMACS-native RMSD cross-validation passed for WT, `289|290 x MAP8`, `224|225 x MAP8` and `155|156 x MAP8`.
- Old Task 009 Tier A/B interpretation is superseded.
- Corrected MD flagged persistent nonlocal tag-contact concerns for `155|156 x MAP8`, `224|225 x HA/MAP8` and `203|204 x G196_minimal`.

Checkpoint:

- `9ff753d task010: add corrected dynamics reanalysis outputs`

## Audited Candidate Rerank

Script:

- `scripts/dynamics_audit_010_finalize.py`

Generated:

- `data/final_candidate_panel_v3_audited.tsv`
- `results/dynamics_audit_010/final_panel_leave_one_layer_out.tsv`
- `results/dynamics_audit_010/final_panel_without_md.tsv`
- `docs/DYNAMIC_NETWORK_ANALYSIS_V2_AUDITED.md`
- `docs/FINAL_CANDIDATE_PRIORITY_V1_AUDITED.md`
- `docs/DYNAMICS_ANALYSIS_AUDIT_010_REPORT.md`

Provisional Priority A:

- `289|290 x MAP8`
- `289|290 x G196_minimal`
- `248|249 x HA`
- `248|249 x MAP8`

No construct is safe or experimentally validated.

## Corrected CHARMM36 Validation Submission

Prepared:

- `results/dynamics_audit_010/corrected_validation_subset.tsv`
- `results/dynamics_audit_010/corrected_validation_manifest.tsv`
- `scripts/dynamics_audit_010_corrected_validation.sbatch`

Submitted:

- Slurm array job `164594`
- 18 array rows: 6 systems x 3 replicas.
- Initial queue state: tasks `0-2` running on `gpu17`; tasks `3-17` pending for resources.
- Slurm identity: `UserId=yukang(10035)`, `GroupId=yukang(10035)`, `Account=chengtong`.
- Health check at 2026-08-25 00:05 Asia/Shanghai: array tasks `0-2` passed EM/NVT/NPT and entered corrected 20 ns production on `gpu17`; tasks `3-17` remained pending for resources.

Interpretation:

- The account field is a Slurm allocation/account label, not a Linux user switch.
- Corrected validation results are not complete at this checkpoint and must not be fabricated.

## Previous Task 010 Checkpoint State

State:

`CANDIDATE_PRIORITY_PROVISIONAL_PENDING_CORRECTED_PROTOCOL_VALIDATION`

Superseded below after corrected validation job `164594` completed and was analyzed.

## Corrected CHARMM36 Validation Completion And Analysis

Date: 2026-08-25

Slurm completion:

- Job `164594` completed 18 / 18 array rows.
- All array rows reported `COMPLETED` with exit code `0:0`.
- Node used: `gpu17`.
- Slurm accounting provenance: `results/dynamics_audit_010/corrected_validation_slurm_sacct_164594_v1.tsv`.

Analysis script:

- `scripts/dynamics_audit_010_validation_analysis.py`

Generated outputs:

- `results/dynamics_audit_010/corrected_validation_completion_v1.tsv`
- `data/corrected_validation_broad_dynamics_v1.tsv`
- `data/corrected_validation_contact_persistence_v1.tsv`
- `data/corrected_validation_tag_exposure_v1.tsv`
- `data/corrected_validation_dynamic_network_v1.tsv`
- `results/dynamics_audit_010/corrected_validation_input_trajectory_inventory_v1.tsv`
- `results/dynamics_audit_010/corrected_validation_time_truncation_v1.tsv`
- `results/dynamics_audit_010/corrected_validation_replica_stability_v1.tsv`
- `results/dynamics_audit_010/corrected_validation_block_stability_v1.tsv`
- `results/dynamics_audit_010/corrected_validation_network_replica_stability_v1.tsv`
- `results/dynamics_audit_010/corrected_validation_dynamics_rank_v1.tsv`
- `results/dynamics_audit_010/protocol_sensitivity_v1.tsv`
- `results/dynamics_audit_010/final_sampling_decision_v1.tsv`
- `data/final_candidate_panel_v4_corrected_validation.tsv`
- `docs/CORRECTED_PROTOCOL_VALIDATION_V1.md`
- `docs/FINAL_CANDIDATE_PRIORITY_V2_CORRECTED_VALIDATION.md`

QC notes:

- 18 / 18 corrected-protocol trajectories passed trajectory readability, finite coordinate/box, completed production, and finite energy checks.
- GROMACS log text `epsilon-rf = inf` was treated as a normal reaction-field parameter, not a nonfinite trajectory failure.
- Raw corrected-validation trajectories under `results/dynamics_audit_010/gromacs/validation_systems/` were left untracked.

Scientific summary:

- `289|290 x MAP8`, `248|249 x HA` and `256|257 x MAP8` were MD-neutral/supportive in corrected validation.
- `224|225 x MAP8` and `155|156 x MAP8` reproduced high nonlocal tag-contact caution.
- Directly validated rows were classification-stable versus the corrected legacy analysis.
- Adaptive sampling decision was `STOP_AT_20NS` for all corrected-validation systems.
- No additional replicas or selected 50 ns extension were triggered.
- No construct is safe or experimentally validated.

Final Task 010 state:

`AUDITED_CANDIDATE_PANEL_READY_FOR_EXPERIMENTAL_REVIEW`
