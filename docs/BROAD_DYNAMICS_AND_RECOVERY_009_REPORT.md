# BROAD_DYNAMICS_AND_RECOVERY_009 Report

Generated: 2026-08-24T14:26:04+08:00

Final task state: `BROAD_DYNAMICS_PARTIALLY_COMPLETE`.

Partial classification: `COMPUTE_JOBS_RUNNING_OR_QUEUED`.

## Completed

- repository/branch/input/software audit completed;
- `248|249 x HA` OpenMM NaN classified as `MODEL_SPECIFIC_GEOMETRY_FAILURE`;
- disorder layer recovered for all 321 residues and all 320 junctions;
- PA14/AGIA exploratory ColabFold completed: 8 constructs x 2 seeds = 16 PDB rows;
- local multimer target manifest prepared and Slurm job submitted;
- balanced dynamics panel V2 created before MD;
- WT/tagged 112-321 system manifest and residue mapping created;
- WT GROMACS pilot completed through topology, solvation, ions, EM, restrained NVT, restrained NPT and 100 ps smoke production;
- all 12 tagged balanced-panel systems completed the same GROMACS preproduction/smoke workflow;
- 39 production replicas have been submitted through Slurm for the 20 ns broad minimum-coverage stage;
- trajectory-dependent outputs remain placeholders until production trajectories complete and pass QC.

## Balanced Dynamics Panel V2

Tagged systems: 12 plus WT reference.
Site-region counts: `{"155-156 hard-negative RNA/pore context": 1, "203-204 mechanistic/conflict region": 1, "224 neighborhood / non-C-terminal core": 2, "248-249 historical insertion region": 2, "256-257 oligomer-conflict control": 1, "C-terminal 287-291 cluster": 5}`.
Tag counts: `{"G196_minimal": 2, "HA": 3, "MAP8": 7}`.

## Answers To Required Questions

1. `248|249 x HA` NaN: `MODEL_SPECIFIC_GEOMETRY_FAILURE`; not treated as biological failure.
2. Disorder layer: recovered with metapredict if import succeeded, otherwise explicit composition proxy fallback recorded in `docs/DISORDER_LAYER_RECOVERY_V1.md`.
3. Local multimer: Slurm job `164291` is running; no completed local multimer model is available yet and no rigid-placement conclusion changed.
4. PA14/AGIA: single-sequence ColabFold completed, but mean CA pLDDT was low (~35-38 across constructs); none is promoted.
5. MD panel: `data/balanced_targeted_dynamics_panel_v2.tsv`.
6. Replicas/ns: 0 completed at this checkpoint; 39 submitted for 20 ns broad minimum coverage (`164351_0-3`, `164359_4` running; `164359_5-38` queued).
7. Stable candidates across replicas: not assessable yet.
8. Persistent tag exposure: not assessable yet.
9. Local/native perturbation from dynamics: not assessable yet.
10. Dynamic/network propagation: not assessable yet.
11. 288/289/290/291 dynamics ordering: not assessable yet.
12. 224|225 and 248|249 competitiveness: retained for dynamics; final evidence pending.
13. Tier A bias: rebalanced pre-MD panel groups 287-291 as one region and includes non-C-terminal regions/controls.
14. MAP8 bias: reduced but MAP8 remains common because inherited structural evidence is strongest there.
15. Remaining uncertainty: exact nucleotide/RNA context and HRV-A89 wet-lab phenotype remain required.

## GROMACS Status

- force field/water: cluster GROMACS `charmm36.ff` with TIP3P, used consistently for WT and all tagged systems;
- system: comparative A89 2C native residues `112-321`, exact inserted tags retained;
- preproduction QC: `13/13` systems passed topology, EM, NVT, NPT and 100 ps smoke production;
- production target: 3 replicas per system; current submitted MDP covers the required 20 ns minimum-coverage stage before selective extension;
- `164330` failed only because the first production launch incorrectly used checkpoint append before a checkpoint existed; the script was repaired;
- `164351_0-3` are running on `gpu16/gpu17`;
- `164359_4-5` are running; `164374_6` and `164375_7` are pending after explicit GPU-backfill split; `164359_8-38` remain queued with generic `gpu:1` across account-accessible `A40,RTX3090` partitions;
- `yukang` is the Linux/Slurm user; `chengtong` is the scheduler/project accounting account on these jobs;
- `RTX3090-autoEM` was not usable from the current Slurm accounting account (`chengtong`) because that partition allows only `cryosparc,cryoem`;
- GPU backfill helper added: `scripts/broad_dynamics_009_gpu_backfill_submit.py`.

## Current Limitation

Replicated GROMACS production MD and trajectory/network analysis are not complete in this checkpoint. PA14/AGIA exploratory modeling completed but remains method-limited by single-sequence low confidence.
Do not use `final_candidate_panel_v2_dynamics.tsv` as a dynamics-informed final panel until trajectories finish and QC passes.
