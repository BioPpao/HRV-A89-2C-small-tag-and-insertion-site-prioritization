# Active Task

Current task: `DYNAMICS_ANALYSIS_AUDIT_AND_CANDIDATE_RERANK_010` — **CHECKPOINTED / CORRECTED VALIDATION RUNNING**

Branch: `analysis/dynamics-audit-010`

Primary task specification:

- `tasks/DYNAMICS_ANALYSIS_AUDIT_AND_CANDIDATE_RERANK_010.md`

Primary audit:

- `docs/DYNAMICS_009_POSTHOC_AUDIT_V1.md`

## Current State

`CANDIDATE_PRIORITY_PROVISIONAL_PENDING_CORRECTED_PROTOCOL_VALIDATION`

## Why Task 010 Exists

Task 009 completed 39 / 39 independent 20 ns production replicas, but posthoc review identified decision-changing analysis/protocol concerns:

- raw trajectory analysis lacked an explicit PBC make-whole/unwrap/center step before geometry-dependent metrics;
- reported RMSD is primarily self-drift versus each system's own first frame, not direct WT-reference preservation;
- local RMSF lacks junction-matched WT baselines;
- contact retention primarily preserves each candidate's starting contacts rather than WT-defined contacts;
- tag exposure relies on a minimum-distance proxy rather than mature SASA;
- the current Tier A/B penalty heuristic can over-interpret incomplete metrics;
- CHARMM36 nonbonded settings must be audited/corrected before any new MD extension.

The historical 009 trajectories remain valuable and must be preserved.

## Authorized Work

Task 010 may autonomously:

1. inventory and hash 009 inputs;
2. repair PBC-aware trajectory preprocessing;
3. reanalyze all 39 x 20 ns trajectories;
4. recompute corrected RMSD/RMSF/Rg/contact/SASA/tag-contact metrics;
5. add junction-matched WT baselines;
6. perform replica/time-block/truncation/convergence analysis;
7. downgrade/harden dynamic-network evidence;
8. audit and correct CHARMM36 production settings;
9. run a reduced corrected-protocol validation subset;
10. decide adaptively whether any reduced-subset system needs more replicas or extension to 50 ns;
11. produce `data/final_candidate_panel_v3_audited.tsv` and an audited priority report;
12. commit and push meaningful checkpoints.

## Completed In Current Checkpoint

- Historical Task 009 local multimer raw outputs were inventoried and left untracked.
- 39 / 39 legacy 20 ns trajectories were reanalyzed with explicit PBC unwrap/center handling.
- Representative RMSD was cross-validated against GROMACS-native analysis.
- Corrected RMSD/RMSF/Rg/contact/SASA/tag-contact/network tables were generated.
- Old Task 009 Tier A/B dynamics classification is superseded.
- `data/final_candidate_panel_v3_audited.tsv` and audited reports were generated.
- Corrected CHARMM36 validation subset was prepared and submitted as Slurm array job `164594`.

## Running Work

Corrected-validation job `164594`:

- 18 array rows: 6 systems x 3 replicas.
- Initial state: tasks `0-2` running on `gpu17`, tasks `3-17` pending for resources.
- Results are pending and must not be interpreted until completed and analyzed.

## Important Execution Rule

Do **not** automatically extend all 39 legacy trajectories to 50 ns.

Corrected 20 ns can be sufficient for screening-level candidate prioritization when independent evidence agrees and the relevant observables are stable. Additional replicas or extension are reserved for decision-critical unstable systems.

## Expected Final States

Preferred if corrected-protocol validation completes without overturning the ranking:

`AUDITED_CANDIDATE_PANEL_READY_FOR_EXPERIMENTAL_REVIEW`

Current provisional checkpoint because corrected validation jobs remain incomplete but the corrected legacy reanalysis is complete:

`CANDIDATE_PRIORITY_PROVISIONAL_PENDING_CORRECTED_PROTOCOL_VALIDATION`

## Stop Boundary

Task 010 does not authorize:

- exact nucleotide/codon construct design;
- wet-lab procedural protocol design;
- broad membrane/RNA/ATP/antibody mechanistic MD;
- claims that any site is safe or experimentally validated;
- merge into `main` without explicit review.
