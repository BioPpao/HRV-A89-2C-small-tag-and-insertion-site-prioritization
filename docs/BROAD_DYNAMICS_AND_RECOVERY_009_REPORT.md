# BROAD_DYNAMICS_AND_RECOVERY_009 Report

Generated: 2026-08-24

Final task state: `READY_FOR_FINAL_CANDIDATE_PANEL_REVIEW`.

## Completed Outputs

- `results/broad_dynamics_009/production_manifest.tsv`
- `results/broad_dynamics_009/replica_completion.tsv`
- `data/dynamics_replica_qc_v1.tsv`
- `data/broad_dynamics_metrics_v1.tsv`
- `data/tag_exposure_dynamics_v1.tsv`
- `data/contact_persistence_dynamics_v1.tsv`
- `data/dynamic_network_perturbation_v1.tsv`
- `data/final_candidate_panel_v2_dynamics.tsv`
- `results/broad_dynamics_009/ranking_robustness_v2.tsv`
- `results/broad_dynamics_009/forcefield_provenance.tsv`
- `results/broad_dynamics_009/local_multimer/local_multimer_model_metrics.tsv`
- `data/local_multimer_tag_context_v2.tsv`

## Broad MD Coverage

The 20 ns broad minimum-coverage milestone is complete.

- WT: 3 x 20 ns.
- Tagged constructs: 12 constructs x 3 x 20 ns.
- Total production sampling analyzed: 780 ns.
- Replica QC inclusion: 39 / 39.
- Technical exclusions: 0 / 39.

The original 50 ns target remains a possible later extension, but the task-defined minimum broad screen was met and analyzed.

## Provenance Caveat

A CPU watcher continued to submit duplicate backfill attempts after outputs were already present. Codex canceled watcher job `164379` and duplicate jobs `164556_0`, `164557_1`, `164558_2`, `164559_3`.

Because some duplicate restarts touched files, Slurm job attribution is imperfect. The authoritative completion evidence is the trajectory endpoint, `prod_20ns.log`, `.xtc`, `.edr` and `.cpt` files. This is recorded in the manifests and run log.

## Local Multimer Recovery

Focused local trimer ColabFold output was generated for:

- `289|290 x MAP8`
- `289|290 x G196_minimal`
- `288|289 x HA`
- `224|225 x HA`
- `248|249 x MAP8`
- `256|257 x MAP8`

All parsed multimer PDB coordinates and score JSON confidence fields were non-finite (`nan`). Therefore local multimer recovery is `completed_all_models_nonfinite_coordinates` and remains inconclusive. It neither rescues nor worsens the previous rigid-placement interpretation.

## Dynamics-Informed Panel

The dynamics panel contains 12 tagged constructs plus WT. Final dynamics tiers in `data/final_candidate_panel_v2_dynamics.tsv`:

- Tier A dynamics retained: 9 constructs.
- Tier B dynamics secondary: 1 construct.
- Controls after dynamics: 2 constructs.

Tier A retained:

- `289|290 x MAP8`
- `289|290 x G196_minimal`
- `288|289 x HA`
- `288|289 x MAP8`
- `290|291 x MAP8`
- `224|225 x HA`
- `224|225 x MAP8`
- `248|249 x MAP8`
- `203|204 x G196_minimal`

Tier B secondary:

- `248|249 x HA`

Controls:

- `256|257 x MAP8`
- `155|156 x MAP8`

No construct is called safe or experimentally validated.

## Key Readouts

Relative to WT, `248|249 x HA` showed the clearest dynamics penalty in this compact heuristic: native RMSD effect was about `+1.02 A`, with elevated local RMSF and moderate nonlocal tag-collapse fraction. It was moved to Tier B secondary.

`289|290 x G196_minimal` had the lowest native RMSD mean among candidates and low nonlocal tag-collapse fraction, but it also had one of the larger raw local-to-functional DCCM values and remains direct-homolog conflicted.

`224|225` and `248|249 x MAP8` remain competitive non-C-terminal candidates by the 20 ns screen, but `224|225` constructs showed high nonlocal tag proximity/collapse in this distance-proxy analysis.

The C-terminal `288|289-290|291` neighborhood remains represented, but it is not treated as multiple independent biological regions. Non-C-terminal candidates remain necessary for a diversified panel.

## Answers To Required Questions

1. `248|249 x HA` OpenMM NaN: classified earlier as `MODEL_SPECIFIC_GEOMETRY_FAILURE`; not biological rejection.
2. Disorder layer: recovered only as a low-evidence fallback/proxy; not decision-grade.
3. Local multimer: completed computationally but all model coordinates/confidence fields were non-finite; no rigid-placement conclusion changed.
4. PA14/AGIA: exploratory single-sequence screen was low-confidence and did not produce a construct competitive with core tags.
5. Simulated panel: WT plus 12 tagged constructs from `data/balanced_targeted_dynamics_panel_v2.tsv`, spanning C-terminal, 224, 248, 203 and control regions.
6. Replicas: yes, 3 independent 20 ns replicas per system were obtained and analyzed.
7. Stable candidates: all simulated candidate constructs had 3 included replicas; `248|249 x HA` is the main dynamics-deprioritized candidate.
8. Tag exposure: measured with a nonlocal heavy-atom distance proxy, not SASA. C-terminal tags generally remained more separated from nonlocal native atoms than 224/203/155-region tags.
9. Elevated perturbation: `248|249 x HA` showed the clearest native RMSD/local RMSF concern among candidates.
10. Network perturbation: dynamic CA DCCM/contact-network metrics were generated; high raw DCCM values are review flags, not functional proof.
11. `288|289`, `289|290`, `290|291`: all remain retained in the 20 ns screen; `289|290 x G196_minimal` looks favorable on native RMSD, while `290|291 x MAP8` has higher collapse than neighboring C-terminal MAP8 rows.
12. Non-C-terminal candidates: `224|225` and `248|249 x MAP8` remain competitive; `248|249 x HA` is secondary.
13. C-terminal bias: still present, but now explicitly balanced by retained 224, 248 and 203 candidates.
14. Final Tier A / Tier B / controls: listed above and machine-readable in `data/final_candidate_panel_v2_dynamics.tsv`.
15. Remaining uncertainty: exact nucleotide/RNA context, HRV-A89-specific insertion phenotype, membrane/RNA/ATP states and direct wet-lab readout remain unresolved.

## Final Boundary

This task completes a computational review package. It does not authorize final RNA/codon design, wet-lab construct design, long MD, membrane/RNA/ATP mechanistic MD, antibody/binder-state modeling, or experimental protocol design.
