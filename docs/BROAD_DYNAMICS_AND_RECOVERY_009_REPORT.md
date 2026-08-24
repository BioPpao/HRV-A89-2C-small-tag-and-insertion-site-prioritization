# BROAD_DYNAMICS_AND_RECOVERY_009 Report

Generated: 2026-08-24T04:03:45.972280+00:00

Final task state: `BROAD_DYNAMICS_PARTIALLY_COMPLETE`.

## Completed

- repository/branch/input/software audit completed;
- `248|249 x HA` OpenMM NaN classified as `MODEL_SPECIFIC_GEOMETRY_FAILURE`;
- disorder layer recovered for all 321 residues and all 320 junctions;
- PA14/AGIA exploratory ColabFold completed: 8 constructs x 2 seeds = 16 PDB rows;
- local multimer target manifest prepared;
- balanced dynamics panel V2 created before MD;
- WT/tagged 112-321 system manifest and residue mapping created;
- trajectory-dependent outputs created with explicit no-trajectory status.

## Balanced Dynamics Panel V2

Tagged systems: 12 plus WT reference.
Site-region counts: `{"155-156 hard-negative RNA/pore context": 1, "203-204 mechanistic/conflict region": 1, "224 neighborhood / non-C-terminal core": 2, "248-249 historical insertion region": 2, "256-257 oligomer-conflict control": 1, "C-terminal 287-291 cluster": 5}`.
Tag counts: `{"G196_minimal": 2, "HA": 3, "MAP8": 7}`.

## Answers To Required Questions

1. `248|249 x HA` NaN: `MODEL_SPECIFIC_GEOMETRY_FAILURE`; not treated as biological failure.
2. Disorder layer: recovered with metapredict if import succeeded, otherwise explicit composition proxy fallback recorded in `docs/DISORDER_LAYER_RECOVERY_V1.md`.
3. Local multimer: not completed yet; no rigid-placement conclusion changed.
4. PA14/AGIA: single-sequence ColabFold completed, but mean CA pLDDT was low (~35-38 across constructs); none is promoted.
5. MD panel: `data/balanced_targeted_dynamics_panel_v2.tsv`.
6. Replicas/ns: 0 completed; manifests preserve planned 3 replicas per system.
7. Stable candidates across replicas: not assessable yet.
8. Persistent tag exposure: not assessable yet.
9. Local/native perturbation from dynamics: not assessable yet.
10. Dynamic/network propagation: not assessable yet.
11. 288/289/290/291 dynamics ordering: not assessable yet.
12. 224|225 and 248|249 competitiveness: retained for dynamics; final evidence pending.
13. Tier A bias: rebalanced pre-MD panel groups 287-291 as one region and includes non-C-terminal regions/controls.
14. MAP8 bias: reduced but MAP8 remains common because inherited structural evidence is strongest there.
15. Remaining uncertainty: exact nucleotide/RNA context and HRV-A89 wet-lab phenotype remain required.

## Blocker

Replicated GROMACS production MD and trajectory/network analysis are not complete in this checkpoint. PA14/AGIA exploratory modeling completed but remains method-limited by single-sequence low confidence.
Do not use `final_candidate_panel_v2_dynamics.tsv` as a dynamics-informed final panel until trajectories finish and QC passes.
