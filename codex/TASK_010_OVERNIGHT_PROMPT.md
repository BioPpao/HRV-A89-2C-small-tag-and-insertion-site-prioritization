# Codex Overnight Prompt — Task 010

You are executing the authorized repository task `DYNAMICS_ANALYSIS_AUDIT_AND_CANDIDATE_RERANK_010` on branch `analysis/dynamics-audit-010`.

Read and obey, in order:

1. `WORKFLOW.md`
2. `AGENTS.md`
3. `PROJECT_STATE.md`
4. `DECISIONS.md`
5. `ANALYSIS_INDEX.md`
6. `ACTIVE_TASK.md`
7. `tasks/DYNAMICS_ANALYSIS_AUDIT_AND_CANDIDATE_RERANK_010.md`
8. `docs/DYNAMICS_009_POSTHOC_AUDIT_V1.md`

Then execute Task 010 end-to-end.

## Core objective

Repair the Task 009 trajectory-analysis defects, reanalyze all existing 39 x 20 ns trajectories using physically correct PBC handling and junction-matched WT comparisons, harden convergence/statistical analysis, audit the CHARMM36 protocol, run the authorized reduced corrected-protocol validation subset when feasible, and produce a transparent audited candidate-priority panel.

The final scientific deliverable is a defensible **priority candidate list for experimental review**, not proof that any insertion is safe or validated.

## Critical rules

- Preserve all Task 009 trajectories and outputs. Never overwrite historical raw data.
- Create Task 010 outputs under new versioned paths.
- Fix PBC/make-whole/center/fit before geometry-dependent analysis.
- Cross-check representative RMSD with GROMACS-native analysis.
- Separate self-drift RMSD from WT-reference RMSD.
- Use site/junction-matched WT local RMSF baselines.
- Use WT-defined contact retention in addition to candidate-start contact persistence.
- Calculate real tag SASA; do not rely only on the old distance proxy.
- Do not treat trajectory frames as independent statistical replicates.
- Perform block/time-truncation/replica/leave-one-replica-out stability analyses.
- Treat DCCM/network analysis as exploratory unless replicated and stable.
- Audit and correct CHARMM36 nonbonded settings before any new MD.
- Do not automatically extend all legacy trajectories to 50 ns.
- Decide adaptively between no extension, more replicas, or 50 ns extension only for decision-critical corrected-protocol systems.
- Do not select several adjacent C-terminal junctions and count them as independent biological regions.
- Do not invent a hidden weighted total score. Preserve evidence components and conflicts.
- Direct biological/genetic evidence outranks MD convenience metrics.
- Do not design exact nucleotide constructs or wet-lab protocols.
- Do not launch membrane/RNA/ATP/antibody mechanism MD.
- Do not claim safety or validation.
- Do not merge to `main`.

## Execution behavior

Work autonomously. Do not stop for routine progress questions.

When a recoverable issue occurs:

`diagnose -> repair/fallback -> record -> continue independent work -> revisit`

Do not silently substitute an inferior method when a mature installed/obtainable method is appropriate.

If an optional dependency cannot be installed, document the blocker and continue all independent modules.

If Slurm jobs are needed, submit only jobs authorized by Task 010, avoid duplicate submissions, and verify existing outputs before any restart.

If corrected validation MD is still running when all independent analysis is complete, commit/push the completed corrected legacy reanalysis and clearly mark validation state as pending. Never fabricate completion.

## Git behavior

Before changing files:

- confirm current branch is `analysis/dynamics-audit-010`;
- inspect `git status`;
- do not discard unrelated local work;
- commit meaningful checkpoints;
- push the branch after meaningful checkpoints when network/authentication allows.

Suggested checkpoint messages are defined in the task specification.

## Required end-state outputs

At minimum, ensure these exist or have a documented blocker:

- `results/dynamics_audit_010/input_trajectory_inventory.tsv`
- `results/dynamics_audit_010/input_provenance.tsv`
- `results/dynamics_audit_010/pbc_rmsd_crossvalidation.tsv`
- `data/broad_dynamics_metrics_v2_corrected.tsv`
- `data/contact_persistence_dynamics_v2_corrected.tsv`
- `data/tag_exposure_dynamics_v2_sasa.tsv`
- `data/dynamic_network_perturbation_v2_corrected.tsv`
- `results/dynamics_audit_010/time_truncation_stability.tsv`
- `results/dynamics_audit_010/replica_stability.tsv`
- `results/dynamics_audit_010/dynamics_rank_stability.tsv`
- `results/dynamics_audit_010/control_discrimination_audit.tsv`
- `results/dynamics_audit_010/forcefield_protocol_audit.tsv`
- `results/dynamics_audit_010/extension_decision.tsv`
- `results/dynamics_audit_010/final_panel_leave_one_layer_out.tsv`
- `results/dynamics_audit_010/final_panel_without_md.tsv`
- `data/final_candidate_panel_v3_audited.tsv`
- `docs/DYNAMIC_NETWORK_ANALYSIS_V2_AUDITED.md`
- `docs/FINAL_CANDIDATE_PRIORITY_V1_AUDITED.md`
- `docs/DYNAMICS_ANALYSIS_AUDIT_010_REPORT.md`
- `docs/DYNAMICS_ANALYSIS_AUDIT_010_RUN_LOG.md`

Update `ACTIVE_TASK.md`, `PROJECT_STATE.md`, `ANALYSIS_INDEX.md`, `DECISIONS.md` and `TODO.md` at the final checkpoint.

## Final response required from Codex

When you finish or become genuinely blocked, report concisely:

1. current git commit and branch;
2. corrected-analysis completion state;
3. corrected validation MD completion/submission state;
4. top Priority A constructs;
5. top Priority B/rescue constructs;
6. controls;
7. whether any system needs 50 ns and why;
8. major remaining scientific uncertainties;
9. files that contain the authoritative final results.

Do not stop merely because the task is long. Continue until complete or until a genuine blocker prevents further authorized progress.
