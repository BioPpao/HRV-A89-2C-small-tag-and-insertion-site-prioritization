# TODO

Last updated: 2026-08-24

Priority order is scientific, not cosmetic.

## Current Gate — Task 010 Dynamics Audit And Candidate Rerank

Status: `AUTHORIZED_FOR_AUTONOMOUS_SERVER_EXECUTION`

Branch:

`analysis/dynamics-audit-010`

Primary task:

- `tasks/DYNAMICS_ANALYSIS_AUDIT_AND_CANDIDATE_RERANK_010.md`

Primary audit:

- `docs/DYNAMICS_009_POSTHOC_AUDIT_V1.md`

## P0 — Must Complete Before Any Final Candidate Priority Call

1. Freeze/hash/inventory all 39 legacy 009 trajectories and critical inputs.
2. Repair PBC handling; make protein whole and apply explicit centering/fitting.
3. Cross-validate representative RMSD with GROMACS-native analysis.
4. Recompute self-drift RMSD and common WT-reference RMSD separately.
5. Build junction-matched WT local RMSF baselines.
6. Recompute WT-defined contact retention rather than only candidate-start contact persistence.
7. Calculate true tag SASA and corrected nonlocal tag contacts.
8. Recompute corrected Rg and geometry metrics.
9. Perform time-block, 10/15/20-ns truncation and leave-one-replica-out stability analysis.
10. Mark DCCM/network evidence exploratory unless replicated/stable.
11. Audit the CHARMM36 MDP and prepare corrected nonbonded settings.
12. Supersede old Tier A/B dynamics classification with an audited multi-objective panel.

## P1 — Corrected-Protocol Validation

After corrected legacy reanalysis:

1. select a compact diverse validation subset containing WT, best C-terminal candidate, best non-C-terminal candidate, one additional conflict/tag rationale and the `155|156 x MAP8` hard-negative control;
2. use corrected GROMACS CHARMM36 settings;
3. use independent velocity seeds;
4. run at least 3 replicas per system at an initial 20 ns checkpoint;
5. analyze with the new Task 010 pipeline.

Do not select only neighboring C-terminal junctions.

## P2 — Adaptive Sampling Decision

For each corrected-validation system determine whether the dominant uncertainty favors:

- no additional sampling;
- more independent replicas;
- extension of corrected replicas toward 50 ns;
- both.

Do **not** extend all 39 legacy trajectories to 50 ns.

Create a machine-readable extension decision table.

## P3 — Final Audited Candidate Package

Required outputs:

- `data/final_candidate_panel_v3_audited.tsv`
- `docs/FINAL_CANDIDATE_PRIORITY_V1_AUDITED.md`
- `docs/DYNAMICS_ANALYSIS_AUDIT_010_REPORT.md`
- `results/dynamics_audit_010/final_panel_leave_one_layer_out.tsv`
- `results/dynamics_audit_010/final_panel_without_md.tsv`

The final panel must include:

- Priority A candidates;
- Priority B/rescue candidates;
- conflict controls;
- hard-negative controls;
- per-tag best junctions;
- per-junction best tag where supported;
- unresolved conflict labels;
- explicit statement that `safe_or_validated = no`.

## P4 — Repository Hygiene

At meaningful checkpoints update and push:

- `ACTIVE_TASK.md`
- `PROJECT_STATE.md`
- `ANALYSIS_INDEX.md`
- `DECISIONS.md`
- `TODO.md`
- literature registry when required.

Avoid duplicate Slurm submission/watchers.

## Explicit Non-Goals For Task 010

Do not proceed automatically to:

- exact nucleotide/RNA/codon design;
- wet-lab procedural protocol design;
- membrane/RNA/ATP/antibody mechanistic MD;
- final claims of biological compatibility or safety;
- merge to `main`.

## Required Future Input

Before final nucleotide-level construct design, obtain the exact experimental HRV-A89 2C/replicon/plasmid nucleotide context.
