# Active task

Current task: `BROAD_DYNAMICS_AND_RECOVERY_009` — **AUTONOMOUS CONTINUATION AUTHORIZED / PRODUCTION MD RUNNING OR QUEUED**

Branch: `analysis/broad-dynamics-009`

Primary task specification:

`tasks/BROAD_DYNAMICS_AND_RECOVERY_009.md`

Continuation authority:

`tasks/BROAD_DYNAMICS_AND_RECOVERY_009_CONTINUATION.md`

## Current state

`BROAD_DYNAMICS_PARTIALLY_COMPLETE`

The previous execution reached a checkpoint before local multimer completion and before GROMACS MD was started. The continuation has now completed GROMACS preproduction for WT plus all 12 tagged systems and submitted production MD through Slurm.

The 009 task remains active. Do **not** create a new task/branch merely because the previous Codex session ended.

## Already completed

- environment/input/software audit;
- `248|249 × HA` OpenMM audit, classified `MODEL_SPECIFIC_GEOMETRY_FAILURE` rather than biological failure;
- all-320 disorder placeholder layer, explicitly low-evidence because a mature predictor was not installed;
- PA14/AGIA exploratory single-sequence ColabFold screen;
- balanced dynamics panel V2;
- WT/tagged `112–321` system manifest and residue mapping;
- WT and all 12 tagged systems passed GROMACS topology/EM/NVT/NPT/100 ps smoke preproduction;
- production arrays submitted for the 20 ns broad minimum-coverage stage: `164351_0-3` and `164359_4` running; `164359_5-38` queued;
- placeholder trajectory-dependent tables with explicit no-trajectory status.

## Mandatory continuation work

1. monitor focused local multimer ColabFold job `164291` and integrate completed models if produced;
2. monitor submitted production arrays `164351` and `164359`;
3. repair/restart only failed production rows, preserving completed rows;
4. obtain broad minimum coverage (`3 × 20 ns`) across the valid panel before selective extension when resources permit;
5. extend toward `3 × 50 ns` per system as feasible after broad minimum coverage;
6. perform trajectory QC, structural/tag/contact dynamics and dynamic-network analysis;
7. integrate dynamics into the multi-objective candidate panel;
8. update repository state and compact results.

## Execution authority

Codex is authorized to continue without waiting for routine user approval for actions inside task 009, including:

- user-space open-source package/environment installation and repair;
- module loading;
- small open-source utility compilation;
- GROMACS/ColabFold/OpenMM/PDBFixer troubleshooting;
- Slurm `sbatch` submission, job arrays, restart from checkpoints and resubmission of failed replicas;
- cancellation/resubmission of Codex-owned failed/stuck jobs when justified;
- routine consistent choices for box/ions/terminal treatment/equilibration/output stride;
- local commits and push retries.

No `sudo`, no restricted-license software, no fabricated credentials, and no destructive operations outside project-owned files.

## Do-not-stop policy

Do not stop the overall task for a single recoverable package, model, job, network or push failure.

Use:

`diagnose → repair/fallback → record → continue independent work → revisit pending work`

Codex may stop before minimum MD coverage only for a genuine hard blocker defined in the continuation addendum or when all remaining work is already submitted to Slurm and legitimately running/queued.

## Dynamics policy

Primary broad comparative system:

- native HRV-A89 2C residues `112–321`;
- exact inserted tag retained;
- identical preparation/terminal policy across WT and constructs;
- explicit solvent;
- one consistent mature force field/water model;
- apo protein-only comparative screening state.

Target:

- `3 × 50 ns` per system.

Minimum broad-coverage milestone:

- `3 × 20 ns` per valid system before selective extension.

Prefer replica breadth over one long trajectory.

## Stop gate after 009

Do not automatically proceed to:

- final wet-lab construct design;
- exact RNA/codon design without the real nucleotide construct;
- membrane/RNA/ATP/antibody mechanistic MD;
- experimental protocol design.

## Allowed final task states

Return exactly one of:

- `READY_FOR_FINAL_CANDIDATE_PANEL_REVIEW`
- `READY_FOR_EXACT_NUCLEOTIDE_AUDIT`
- `BROAD_DYNAMICS_PARTIALLY_COMPLETE`

If partial, state whether it is due to `COMPUTE_JOBS_RUNNING_OR_QUEUED`, `TECHNICAL_BLOCKER_WITH_RECOVERY_EXHAUSTED`, or `MINIMUM_COVERAGE_NOT_YET_REACHED`, and preserve exact restart instructions.
