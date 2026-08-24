# BROAD_DYNAMICS_AND_RECOVERY_009_CONTINUATION

Status: **AUTHORIZED / AUTONOMOUS CONTINUATION UNTIL MD MINIMUM-COVERAGE OR HARD BLOCKER**

Date: 2026-08-24

Branch: `analysis/broad-dynamics-009`

Parent task: `tasks/BROAD_DYNAMICS_AND_RECOVERY_009.md`

## Purpose

The previous 009 execution stopped at a partial checkpoint even though major authorized work remained. This continuation addendum explicitly authorizes Codex to keep solving routine technical problems and proceed through the pending computational stages without waiting for user confirmation after each checkpoint.

This addendum does **not** expand the scientific scope beyond task 009. It increases execution autonomy within the already authorized computational scope.

## Current inherited checkpoint

Current state:

`BROAD_DYNAMICS_PARTIALLY_COMPLETE`

Already completed:

- environment/input audit;
- `248|249 × HA` OpenMM failure classification as `MODEL_SPECIFIC_GEOMETRY_FAILURE`;
- all-320 disorder placeholder layer;
- PA14/AGIA single-sequence exploratory structure screen;
- balanced dynamics panel V2;
- WT/tagged 112–321 system manifest and residue mapping.

Still mandatory before normal completion:

1. repair relevant environment/tool issues that are straightforward and needed for the remaining work;
2. complete focused local multimer modeling if technically tractable;
3. prepare all WT/tagged GROMACS systems;
4. pass minimization/NVT/NPT QC for as many panel members as technically valid;
5. submit non-interactive replicated production MD;
6. obtain at least the minimum broad-coverage target before selective extension where resources permit;
7. run trajectory QC and comparative dynamics analyses;
8. run dynamic correlation/network analysis where trajectories pass QC;
9. update the dynamics-informed candidate panel and robustness analysis;
10. update repository state and push compact outputs.

## Expanded execution authority

Codex is explicitly authorized to perform the following actions without asking the user for routine confirmation:

### Environment/tool recovery

- create or repair isolated user-space Python/conda/micromamba environments;
- install open-source Python packages needed for the task;
- repair `setuptools/pkg_resources` or equivalent environment defects affecting PDBFixer;
- install a mature open disorder predictor if practical;
- use cluster `module load` for available scientific software;
- compile small open-source analysis utilities in user space when straightforward;
- select a compatible GROMACS 2024.x module and one consistent mature protein force-field/water combination after verifying availability;
- reuse working caches/environments from tasks 007/008/009.

Do not use `sudo`, system-wide package modification, restricted-license software, or actions requiring fabricated credentials.

### Slurm/GPU execution

Codex may:

- inspect scheduler/resource state;
- submit `sbatch` jobs and job arrays;
- use any currently suitable authorized GPU partition/node, not only historical `gpu15`;
- cancel and resubmit its own failed/stuck jobs when justified;
- restart GROMACS production from checkpoints;
- resubmit individual failed replicas rather than restarting successful work;
- continue CPU-side preparation/analysis while GPU jobs are queued or running.

Do not hold an interactive GPU allocation while waiting for reasoning or user input.

### Scientific implementation choices

Codex may make routine implementation decisions when the repository/task already defines the scientific objective, including:

- exact box dimensions within accepted GROMACS practice, provided all systems use the same policy;
- a consistent physiological-range ionic strength if used;
- consistent terminal treatment for WT and all constructs;
- reasonable minimization/equilibration lengths;
- output stride sufficient for RMSD/RMSF/contact/network analysis without excessive storage;
- conservative troubleshooting choices for topology/coordinate preparation;
- local dimer versus trimer modeling based on tractability and the existing hexamer hypotheses.

All such choices must be documented in manifests/configuration files and applied consistently across compared systems.

## Tool-specific recovery requirements

### PDBFixer

Current import failure is due to missing `pkg_resources`, not evidence that PDBFixer is unavailable.

Repair the environment first, e.g. by restoring a compatible `setuptools`, then verify PDBFixer import/functionality. If another open sanitation route is more robust, document and use it.

### ColabFold

Do not classify ColabFold as missing merely because `colabfold.__version__` is absent. Verify operational status using the executable/import path actually used successfully in tasks 007/008/009.

For local multimer work, reuse the working ColabFold installation and cached resources where possible.

### Disorder predictor

The composition/low-complexity proxy from the partial checkpoint is not decision-grade.

Attempt a real mature open predictor. Prefer installation that reuses an existing compatible PyTorch environment or avoids redundant multi-hundred-MB downloads when possible. If a mature predictor remains impractical after reasonable attempts, retain the proxy with explicit low-evidence status and continue; this must not block MD.

### PA14/AGIA

Current single-sequence low-pLDDT results are method-limited and are not biological rejection.

Do not spend the entire continuation trying to rescue these exploratory tags. If an MSA-consistent focused rerun is readily possible, do it for the most informative subset. Otherwise preserve them as exploratory/deferred and prioritize the core dynamics panel.

## GROMACS continuation requirement

GROMACS 2024.2 is already available and task 009 must not stop again with every production row still `not_started` unless a concrete topology/system blocker has been demonstrated and documented.

Proceed in this order:

1. build and validate one WT `112–321` pilot system;
2. run minimization, NVT and NPT for WT;
3. run a short production smoke test to prove the complete workflow;
4. apply the same reproducible preparation pipeline to the balanced tagged panel;
5. submit 3 independent replicas per valid system through Slurm;
6. prioritize broad minimum coverage across all valid systems before selective extension.

Primary production target:

- `3 × 50 ns` per system.

Minimum broad-coverage milestone:

- `3 × 20 ns` per system.

If full target cannot complete during one Codex session because Slurm jobs are still legitimately running, Codex must still:

- ensure the jobs are correctly submitted and restartable;
- write accurate job IDs/statuses/paths;
- avoid falsely marking the task complete;
- leave continuation scripts/checkpoints so the next Codex session can resume without reconstruction.

## Do-not-stop rules

Codex must **not** stop the overall task merely because of:

- login node lacking GPU;
- one pip/conda installation failure;
- one missing optional package;
- one failed ColabFold model;
- one OpenMM failure;
- one GROMACS topology/preparation failure for a single construct;
- one failed MD replica;
- one pending GPU queue;
- temporary Git push/network failure;
- one unavailable optional analysis method.

For each recoverable problem:

1. diagnose;
2. attempt a reasonable repair/fallback;
3. record the failure/recovery;
4. continue independent work;
5. return to pending jobs later.

Do not ask the user to approve routine technical decisions already inside this scope.

## When Codex is allowed to stop early

Stopping before the minimum MD milestone is acceptable only if one of the following is true:

1. a genuine cluster-wide scheduler/storage failure prevents computation;
2. no reproducible GROMACS topology can be built even for the WT pilot after multiple documented attempts;
3. required source structures/files are corrupt or absent and cannot be reconstructed from repository inputs;
4. user credentials/permissions outside Codex control are genuinely required;
5. continuing would require restricted-license software, `sudo`, destructive operations, or expansion into a non-authorized scientific task;
6. all remaining work consists of already-submitted Slurm jobs that are still running/pending and cannot be accelerated by further independent preparation/analysis.

If stopping for one of these reasons, provide exact commands/logs/error messages and preserve restartable state.

## Required completion evidence

Do not claim dynamics completion from placeholder files.

A valid dynamics-informed completion requires actual trajectory evidence recorded in:

- `results/broad_dynamics_009/production_manifest.tsv`
- `results/broad_dynamics_009/replica_completion.tsv`
- `data/dynamics_replica_qc_v1.tsv`
- `data/broad_dynamics_metrics_v1.tsv`
- `data/tag_exposure_dynamics_v1.tsv`
- `data/contact_persistence_dynamics_v1.tsv`
- `data/dynamic_network_perturbation_v1.tsv`
- `data/final_candidate_panel_v2_dynamics.tsv`
- `results/broad_dynamics_009/ranking_robustness_v2.tsv`

All placeholder/no-trajectory rows must remain explicitly distinguishable from real results.

## Repository/storage policy

Codex may commit and push:

- scripts;
- `.mdp` files;
- manifests;
- small topology/provenance metadata where appropriate;
- compact TSV/CSV metrics;
- reports;
- environment specifications;
- Slurm scripts/log summaries.

Do not commit:

- bulk `.xtc`/`.trr` trajectories;
- large checkpoint collections;
- package caches;
- model parameter caches;
- local sequence databases;
- other bulky reproducible intermediates.

Record server paths for large trajectory/checkpoint data in manifests.

## Scientific boundaries remain unchanged

Do not automatically proceed to:

- membrane-state MD;
- RNA-bound mechanistic MD;
- ATP/Mg mechanistic MD;
- antibody/9A5 mechanistic MD;
- exact nucleotide/codon design without the real experimental construct;
- wet-lab protocol design;
- final experimental validation claims.

No site may be called safe or experimentally validated.

## Final state

Return exactly one of:

- `READY_FOR_FINAL_CANDIDATE_PANEL_REVIEW`
- `READY_FOR_EXACT_NUCLEOTIDE_AUDIT`
- `BROAD_DYNAMICS_PARTIALLY_COMPLETE`

A partial state must now include an explicit classification:

- `COMPUTE_JOBS_RUNNING_OR_QUEUED`
- `TECHNICAL_BLOCKER_WITH_RECOVERY_EXHAUSTED`
- `MINIMUM_COVERAGE_NOT_YET_REACHED`

and exact restart instructions.
