# TODO

Last updated: 2026-08-24

Priority order is scientific, not cosmetic.

## CURRENT — BROAD_DYNAMICS_AND_RECOVERY_009 CONTINUATION

Status: **AUTONOMOUS CONTINUATION AUTHORIZED / BROAD_DYNAMICS_PARTIALLY_COMPLETE / COMPUTE_JOBS_RUNNING_OR_QUEUED**

Branch:

`analysis/broad-dynamics-009`

Primary task:

- `tasks/BROAD_DYNAMICS_AND_RECOVERY_009.md`

Continuation authority:

- `tasks/BROAD_DYNAMICS_AND_RECOVERY_009_CONTINUATION.md`

The previous Codex execution stopped at a partial checkpoint. Do not create a new branch/task. Continue 009 until real replicated MD evidence exists or a genuine documented hard blocker remains.

### Immediate priority order

1. repair PDBFixer/setuptools and other straightforward environment defects needed downstream;
2. attempt a mature open disorder predictor without letting it block MD;
3. monitor focused local multimer ColabFold job `164291`, then run `scripts/broad_dynamics_009_integrate_local_multimer.py`;
4. WT `112–321` GROMACS pipeline has passed minimization/NVT/NPT/short production;
5. all valid balanced-panel systems have passed the same GROMACS preproduction/smoke protocol;
6. monitor submitted Slurm production arrays: `164351_0-3` and `164359_4` running; `164359_5-38` queued;
7. achieve at least `3 × 20 ns` broad coverage per valid system before selective extension;
8. extend toward `3 × 50 ns` where feasible;
9. run trajectory QC and comparative dynamics/network analyses;
10. update the dynamics-informed Tier A / Tier B / control panel and robustness analysis.

### Explicit authority

Codex may perform routine project-contained technical actions without waiting for user approval:

- create/repair user-space environments;
- install open-source packages;
- load cluster modules;
- compile small open utilities;
- troubleshoot GROMACS/ColabFold/OpenMM/PDBFixer;
- submit/cancel/resubmit Codex-owned Slurm jobs and arrays;
- restart GROMACS from checkpoints;
- choose consistent routine MD implementation details and document them;
- commit compact scientific outputs and retry pushes.

Do not use `sudo`, restricted-license tools, fabricated credentials, or destructive actions outside project-owned paths.

### Do-not-stop rule

A single package/model/job/push/network failure is not a project stop condition.

Use:

`diagnose → repair/fallback → record → continue → revisit`

If Slurm jobs remain queued/running, preserve exact job IDs, paths and restart instructions rather than claiming completion.

### Current known checkpoint facts

- `248|249 × HA` OpenMM failure is classified `MODEL_SPECIFIC_GEOMETRY_FAILURE`; do not treat it as biological rejection;
- local multimer rows remain pending and must be replaced with actual results or explicit exhausted-blocker status;
- current disorder V1 is a low-quality composition proxy and not decision-grade;
- PA14/AGIA single-sequence low-pLDDT screen is method-limited and not biological rejection;
- GROMACS 2024.2 is available and WT plus all 12 tagged systems passed preproduction QC;
- production rows are submitted, not completed: `164351_0-3` running and `164359_4` running and `164359_5-38` queued on account-accessible generic GPU partitions;
- `RTX3090-autoEM` was tested but is not account-accessible for `chengtong`;
- placeholder dynamics tables must never be interpreted as real trajectory evidence.

### Current monitor commands

```bash
squeue -u "$USER"
sacct -j 164291 --format=JobID,JobName,State,ExitCode,Elapsed,NodeList -P
sacct -j 164351 --format=JobID,JobName,Partition,State,ExitCode,Elapsed,NodeList -P
sacct -j 164359 --format=JobID,JobName,Partition,State,ExitCode,Elapsed,NodeList -P
.tools/envs/open_structure_007/bin/python scripts/broad_dynamics_009_update_gmx_status.py
```

### GPU backfill helper

Use the helper to keep remaining production replicas moving when account-accessible GPUs open:

```bash
.tools/envs/open_structure_007/bin/python scripts/broad_dynamics_009_gpu_backfill_submit.py --dry-run
.tools/envs/open_structure_007/bin/python scripts/broad_dynamics_009_gpu_backfill_submit.py --loop --interval 300
```

Default mode preserves existing pending queue priority and submits only missing/orphaned indices. Use `--rescue-pending` only when intentionally splitting pending array tasks onto detected free GPU nodes.

Current watcher:

- `164379` runs `scripts/broad_dynamics_009_gpu_backfill_loop.sbatch` on `computer1`.

### Dynamics system

Primary broad comparison:

- native A89 2C `112–321`;
- exact inserted tag retained;
- equivalent terminal treatment across WT and tagged constructs;
- explicit solvent;
- one consistent mature force field/water model;
- apo protein-only state.

Default target:

- `3 × 50 ns` per system.

Minimum broad-coverage milestone:

- `3 × 20 ns` per valid system before selective extension.

### Required real dynamics outputs

- `results/broad_dynamics_009/preproduction_qc.tsv`
- `results/broad_dynamics_009/production_manifest.tsv`
- `results/broad_dynamics_009/replica_completion.tsv`
- `data/dynamics_replica_qc_v1.tsv`
- `data/broad_dynamics_metrics_v1.tsv`
- `data/tag_exposure_dynamics_v1.tsv`
- `data/contact_persistence_dynamics_v1.tsv`
- `data/dynamic_network_perturbation_v1.tsv`
- `data/final_candidate_panel_v2_dynamics.tsv`
- `results/broad_dynamics_009/ranking_robustness_v2.tsv`
- `docs/BROAD_DYNAMICS_AND_RECOVERY_009_REPORT.md`

## Stable previous checkpoint — CANDIDATE_PANEL_EXPANSION_008

Status: **READY_FOR_BROAD_TARGETED_DYNAMICS**

Stable branch:

`analysis/candidate-panel-008`

Primary report:

- `docs/CANDIDATE_PANEL_EXPANSION_008_REPORT.md`

Keep this branch unchanged as the pre-dynamics candidate-panel checkpoint.

## Later — exact nucleotide/RNA gate

Mandatory before final wet-lab construct design. Requires the real experimental nucleotide context.

## Repository maintenance

Keep `PROJECT_STATE.md`, `ACTIVE_TASK.md`, `ANALYSIS_INDEX.md`, `DECISIONS.md` and this file consistent. Preserve historical outputs and avoid committing bulk trajectories, model checkpoints, package caches or large databases.
