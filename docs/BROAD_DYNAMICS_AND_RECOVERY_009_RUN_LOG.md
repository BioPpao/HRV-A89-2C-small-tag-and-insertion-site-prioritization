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

## 2026-08-24 continuation checkpoint: GROMACS preproduction and production submission

Repository/session state:

- branch confirmed: `analysis/broad-dynamics-009`;
- orchestration host: `admin1`;
- Slurm GPU inventory showed account-usable `RTX3090` and `A40` partitions plus `*-autoEM` partitions with additional nodes;
- `RTX3090-autoEM` was tested but rejected by scheduler/account configuration because the partition allows only `cryosparc,cryoem`, while the current account is `chengtong`.

Environment/tool recovery:

- repaired the existing `.tools/envs/open_structure_007` environment by restoring compatible `setuptools/pkg_resources`;
- verified `PDBFixer` import after repair;
- reused GROMACS `2024.2` CUDA module and existing ColabFold `1.5.3` environment.

GROMACS setup:

- added reproducible setup and Slurm scripts under `scripts/`;
- generated shared MDP protocol under `results/broad_dynamics_009/gromacs/mdp/`;
- selected one consistent force-field/water policy for every compared system: cluster GROMACS `charmm36.ff` with TIP3P water, dodecahedron box, neutralization plus 0.15 M NaCl, consistent charged termini;
- prepared WT and 12 tagged systems as the comparative native A89 2C `112-321` segment with exact inserted tags retained;
- corrected a tagged-system directory mismatch so `system_manifest.tsv` IDs and GROMACS system directories match exactly.

WT pilot:

- Slurm job `164290` failed because `gmx mdrun` was called with `-ntomp` but without explicit `-ntmpi`;
- script fixed to use `-ntmpi 1 -ntomp ${SLURM_CPUS_PER_TASK}`;
- Slurm job `164292` completed WT topology, solvation, ionization, EM, restrained NVT, restrained NPT and 100 ps smoke production;
- WT smoke output exists at `results/broad_dynamics_009/gromacs/systems/WT_112_321/prod_smoke.xtc`.

Tagged preproduction:

- Slurm array `164295` exposed the first tagged-directory mismatch;
- Slurm array `164308` exposed the expected pre-ion net-charge warning before neutralization;
- script fixed with `grompp -maxwarn 1` only for the ion-generation step;
- Slurm array `164321` completed all 12 tagged preproduction jobs;
- `results/broad_dynamics_009/preproduction_qc.tsv` now has 13/13 rows with topology, EM, NVT, NPT and smoke production completed.

Production submission:

- first production array `164330` used `-cpi ... -append` on the first production start and failed immediately for early rows because no production checkpoint existed yet;
- `scripts/broad_dynamics_009_gmx_production.sbatch` was repaired to use checkpoint append only when `prod_20ns.cpt` already exists;
- replacement array `164351` was submitted; array indices `0-3` are running on `gpu16/gpu17`;
- pending indices `4-38` from `164351` were cancelled and redistributed after the user requested use of any idle GPU rather than waiting on one GPU type;
- `164356` tested `RTX3090-autoEM` but was cancelled because the partition is not account-accessible;
- `164357` was replaced to avoid mixed autoEM account ambiguity;
- current remaining array `164359` covers indices `4-38` and requests generic `gpu:1` on account-accessible partitions `A40,RTX3090`.

Current production manifest:

- 39 planned production rows = WT plus 12 tagged systems x 3 replicas;
- rows 0-3: job IDs `164351_0` to `164351_3`;
- rows 4-38: job IDs `164359_4` to `164359_38` (`164359_4` running at checkpoint, `164359_5-38` queued);
- target remains 50 ns; submitted production MDP is the 20 ns broad minimum-coverage stage.

Local multimer:

- focused local multimer job `164291` is still running on `gpu16`;
- output currently contains only `log.txt`; no model PDB has completed yet;
- this remains independent of GROMACS production and is not blocking MD.

Current checkpoint state:

`BROAD_DYNAMICS_PARTIALLY_COMPLETE`

Partial classification:

`COMPUTE_JOBS_RUNNING_OR_QUEUED`

Exact restart/monitor commands:

```bash
squeue -u "$USER"
sacct -j 164291 --format=JobID,JobName,State,ExitCode,Elapsed,NodeList -P
sacct -j 164351 --format=JobID,JobName,Partition,State,ExitCode,Elapsed,NodeList -P
sacct -j 164359 --format=JobID,JobName,Partition,State,ExitCode,Elapsed,NodeList -P
.tools/envs/open_structure_007/bin/python scripts/broad_dynamics_009_update_gmx_status.py
```

After `164291` finishes:

```bash
.tools/envs/open_structure_007/bin/python scripts/broad_dynamics_009_integrate_local_multimer.py
```

After production replicas finish:

```bash
.tools/envs/open_structure_007/bin/python scripts/broad_dynamics_009_update_gmx_status.py
```

Trajectory QC and dynamics/network analysis remain pending until real production trajectories complete.

## 2026-08-24 clarification and GPU backfill helper

Account clarification:

- Linux user is `yukang` (`whoami`, `id`);
- Slurm job field `UserId=yukang(10035)` confirms the running owner;
- Slurm job field `Account=chengtong` is the scheduler/project accounting account, not the login user;
- `RTX3090-autoEM` remains inaccessible for these jobs because its partition policy allows only accounting accounts `cryosparc,cryoem`.

Added helper:

- `scripts/broad_dynamics_009_gpu_backfill_submit.py`

Purpose:

- detect account-accessible free GPUs from `scontrol show node`;
- avoid duplicate submission by parsing current `squeue` task indices;
- submit only missing/orphaned `bd009_prod20` array indices by default;
- optionally split pending array tasks with `--rescue-pending` when explicitly desired.

Important behavior:

- default mode does not cancel existing pending jobs, preserving queue priority;
- `--rescue-pending` cancels selected pending task IDs and resubmits singleton array tasks to detected GPU nodes;
- backfill submissions are logged in `results/broad_dynamics_009/gpu_backfill_submissions.tsv`;
- command-line `--cpus-per-task` and `--mem` can reduce CPU demand for GPU backfill without changing MD scientific parameters.

Observed run:

- dry-run identified two RTX3090 free-GPU slots on `gpu16` and `gpu17`;
- an initial rescue run split indices `6` and `7` from the pending `164359` array and submitted them as `164374_6` and `164375_7`;
- those singleton jobs became `PENDING (Priority)`, not `PENDING (Resources)`;
- therefore the script default was changed to avoid cancelling existing pending work unless `--rescue-pending` is explicitly supplied.

Current known queue after this checkpoint:

- `164351_0-3`: running;
- `164359_4-5`: running;
- `164374_6`, `164375_7`: pending by priority after backfill split;
- `164359_8-38`: pending in the generic `A40,RTX3090` array.

Useful commands:

```bash
.tools/envs/open_structure_007/bin/python scripts/broad_dynamics_009_gpu_backfill_submit.py --dry-run
.tools/envs/open_structure_007/bin/python scripts/broad_dynamics_009_gpu_backfill_submit.py --loop --interval 300
.tools/envs/open_structure_007/bin/python scripts/broad_dynamics_009_gpu_backfill_submit.py --rescue-pending --max-submit 2
```

Watcher:

- Slurm job `164379` started `scripts/broad_dynamics_009_gpu_backfill_loop.sbatch` on `computer1`;
- it runs conservative loop mode every 300 s and preserves existing pending queue priority.

## 2026-08-24 continuation after network interruption

Account/GPU check:

- `whoami` returned `yukang`.
- `squeue -u yukang` initially showed watcher job `164379` plus duplicate backfill jobs `164556_0`, `164557_1`, `164558_2`, `164559_3`.
- `sinfo` showed account-visible GPU nodes including idle `gpu16` and `gpu17`.

Corrective action:

- Canceled watcher `164379` and duplicate reruns `164556_0`, `164557_1`, `164558_2`, `164559_3`.
- Verified `squeue -u yukang` was empty after cancellation.
- Patched `scripts/broad_dynamics_009_gpu_backfill_submit.py` so it skips rows with completed output/log evidence before checking free GPU nodes or submitting new work.
- Dry-run after patch returned `submitted=0`, confirming completed replicas are not resubmitted.

Local multimer integration:

- Ran `scripts/broad_dynamics_009_integrate_local_multimer.py` after patching it to handle non-finite model coordinates.
- Output status: all focused local multimer constructs are `completed_all_models_nonfinite_coordinates`.
- Interpretation: local multimer output is inconclusive and cannot override rigid-context evidence.

Trajectory analysis:

- Added `scripts/broad_dynamics_009_analyze_md.py`.
- Ran real analysis over 39 GROMACS production trajectories and `.edr` files.
- Fixed an energy-column parsing bug after detecting that `gmx energy` wrote Potential/Kinetic/Total/Temperature/Pressure order rather than the initial assumed order.
- Fixed tag exposure proxy to exclude local insertion-window native atoms so covalent tag flanks do not force collapse = 1.0.
- Final analyzed state:
  - 39 / 39 replicas included;
  - 20.0 ns per replica;
  - 201 frames per replica;
  - 780 ns total analyzed production sampling;
  - 0 technical exclusions.

Generated/updated compact outputs:

- `data/dynamics_replica_qc_v1.tsv`
- `data/broad_dynamics_metrics_v1.tsv`
- `data/tag_exposure_dynamics_v1.tsv`
- `data/contact_persistence_dynamics_v1.tsv`
- `data/dynamic_network_perturbation_v1.tsv`
- `data/final_candidate_panel_v2_dynamics.tsv`
- `results/broad_dynamics_009/ranking_robustness_v2.tsv`
- `results/broad_dynamics_009/forcefield_provenance.tsv`
- `docs/DYNAMICS_QC_V1.md`
- `docs/DYNAMIC_NETWORK_ANALYSIS_V1.md`
- `docs/BROAD_DYNAMICS_AND_RECOVERY_009_REPORT.md`

Final state:

`READY_FOR_FINAL_CANDIDATE_PANEL_REVIEW`
