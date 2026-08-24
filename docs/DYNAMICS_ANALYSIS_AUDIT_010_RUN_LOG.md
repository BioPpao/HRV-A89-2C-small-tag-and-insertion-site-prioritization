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
