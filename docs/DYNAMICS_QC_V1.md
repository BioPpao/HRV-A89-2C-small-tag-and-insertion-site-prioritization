# Dynamics QC V1

Generated: 2026-08-24

Task: `BROAD_DYNAMICS_AND_RECOVERY_009`

## Summary

Real trajectory QC is complete for the broad minimum-coverage screen.

- Systems: WT `112-321` plus 12 tagged constructs.
- Replicas: 39 / 39 analyzed.
- Sampling: 3 x 20 ns per system, 780 ns total.
- Included for comparative ranking: 39 / 39.
- Excluded for technical QC failure: 0 / 39.

Machine-readable QC:

- `data/dynamics_replica_qc_v1.tsv`
- `results/broad_dynamics_009/production_manifest.tsv`
- `results/broad_dynamics_009/replica_completion.tsv`

## QC Criteria

Each replica was checked for trajectory presence, frame count, achieved production time, `prod_20ns.log` completion text, finite native-CA coordinates, finite box vectors and GROMACS energy terms.

All 39 replicas reached `20.0 ns` with 201 frames and 210 native A89 CA atoms.

## Provenance Caveat

A CPU watcher submitted duplicate backfill attempts after trajectories were already complete. Some latest Slurm log names therefore correspond to final file-touching restart attempts rather than clean first completion jobs. The trajectory endpoint, `prod_20ns.log`, `.xtc`, `.edr` and `.cpt` files are the authoritative completion evidence.

This caveat is preserved in `job_id_provenance`, `slurm_completion_log` and `docs/BROAD_DYNAMICS_AND_RECOVERY_009_RUN_LOG.md`.

## Boundary

This is a comparative apo protein-only perturbation screen of A89 2C residues `112-321`. It is not viral fitness validation and no insertion site is called safe.
