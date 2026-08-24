# DYNAMICS_009_POSTHOC_AUDIT_V1

Date: 2026-08-24

Status: **DECISION-CHANGING AUDIT — TASK 009 DYNAMICS RANKING IS PROVISIONAL**

Branch: `analysis/dynamics-audit-010`

## Purpose

This audit reviews the completed `BROAD_DYNAMICS_AND_RECOVERY_009` trajectory-analysis layer before any long-MD extension or wet-lab prioritization is finalized.

The 39 completed trajectories remain valuable raw data. This audit does **not** declare the trajectories invalid. It identifies analysis/protocol defects that can alter the reported dynamics-derived ranking and therefore must be corrected before the dynamics layer is considered decision-grade.

## Executive conclusion

Do **not** extend all 39 replicas from 20 ns to 50 ns under the existing pipeline.

First:

1. preserve the 009 trajectories as immutable provenance;
2. correct periodic-boundary-condition handling and recompute geometry-dependent metrics;
3. replace generic WT comparisons with junction-matched WT baselines;
4. distinguish self-drift from deviation from the WT structural reference;
5. redefine contact preservation against WT-defined contacts;
6. treat dynamic-network metrics as exploratory unless convergence/replica consistency is demonstrated;
7. audit the CHARMM36 nonbonded settings before any new production extension;
8. re-rank candidates using corrected, multi-objective evidence rather than the current heuristic penalty count.

The current project state should therefore be interpreted as:

`MD_ANALYSIS_AUDIT_REQUIRED__PRELIMINARY_WET_PANEL_EVIDENCE_AVAILABLE`

## Confirmed defect A — no explicit PBC make-whole/unwrap/center step in the 009 Python analysis

`scripts/broad_dynamics_009_analyze_md.py` loads the production `xtc` directly with MDAnalysis and immediately extracts coordinates for RMSD, RMSF, radius of gyration, tag–native minimum distance, native-contact retention and DCCM/network analysis.

The script does not first make the protein whole across periodic boundaries or otherwise apply a documented molecule-unwrapping/centering transformation.

Consequences:

- RMSD can be inflated when atoms/fragments cross the periodic box;
- radius of gyration can be inflated;
- Euclidean tag–native distances can be wrong;
- contact-retention metrics can be wrong;
- DCCM/covariance/network metrics can inherit coordinate artifacts.

The unusually large 009 RMSD values are therefore not trustworthy until this is corrected.

Required correction:

- preprocess or transform every trajectory so the protein is whole and consistently centered before structural analysis;
- use the same transformation for WT and every tagged construct;
- independently cross-check representative RMSD outputs with GROMACS-native tools.

## Confirmed defect B — current RMSD is self-drift, not WT-reference preservation

The 009 script aligns each trajectory to its own first frame and reports RMSD relative to that first frame.

Therefore a low mutant RMSD means only that the mutant stayed close to its own starting predicted structure. It does **not** mean the mutant stayed close to the WT 2C conformation.

A distorted insertion model can remain trapped near its starting structure and appear favorable under this metric.

Required correction:

Report at least two separate quantities:

1. `self_drift_rmsd_A` — each trajectory versus its own equilibrated reference;
2. `wt_reference_rmsd_A` — native A89 residues versus an explicitly defined WT reference after the same core fit.

Do not describe a negative `mutant_mean - WT_mean` self-drift value as improved WT-like stability.

## Confirmed defect C — local RMSF WT baseline is not junction-matched

For a candidate at `224|225`, the biologically meaningful comparison is local native-residue fluctuation in the `224|225` neighborhood of the mutant versus the same native-residue window in WT.

The existing summary does not provide a valid site-specific WT local-RMSF baseline for each junction, leaving important `local_rmsf_effect_vs_WT` fields unavailable or non-informative.

Required correction:

For every candidate junction `i|i+1`, define the same native A89 residue window in WT and calculate:

`delta_local_rmsf = mutant_window_mean - WT_same_window_mean`.

WT trajectories must be reused for every site-specific baseline rather than inventing a generic insertion window.

## Confirmed defect D — current contact retention preserves candidate starting contacts, not WT-defined contacts

The existing script defines native contacts from each system's first frame, then asks whether those same contacts persist.

This answers:

`Does the candidate preserve its own starting-model contact graph?`

It does not directly answer:

`Does the candidate preserve the WT 2C contact graph?`

Required correction:

Calculate both:

- `candidate_start_contact_persistence`;
- `WT_defined_contact_retention` using a WT reference/WT ensemble contact list mapped to native A89 residues.

The WT-defined metric is the decision-relevant perturbation quantity.

## Confirmed defect E — tag-exposure proxy is not mature exposure/detectability evidence

The 009 tag metric is based primarily on nonlocal heavy-atom minimum distance and a collapse threshold. It is not SASA and does not directly establish antibody/binder accessibility.

Required correction:

Add at minimum:

- tag SASA and per-residue SASA;
- fraction of tag residues with meaningful solvent exposure;
- persistent nonlocal native contacts involving the tag;
- tag end-to-end distance/orientation as descriptive geometry;
- explicit separation of `protein perturbation` from `tag detectability/accessibility`.

Binder-specific accessibility from previous static modeling should remain a separate evidence layer.

## Confirmed defect F — current Tier A/B heuristic over-interprets incomplete metrics

The current penalty logic assigns fixed thresholds to several metrics and keeps a construct in Tier A when the total penalty count is <=1.

Some intended effect-size terms are unavailable, and a severe value in one metric can be reduced to a single penalty. This can create counterintuitive Tier A calls.

Required correction:

Do not replace the heuristic with another opaque score.

Use:

- hard biological exclusion status;
- direct homolog insertion phenotype;
- structure/evolution/PLM evidence;
- corrected MD effect estimates with replica uncertainty;
- tag exposure/accessibility;
- explicit conflict labels;
- Pareto/non-dominated review;
- leave-one-replica-out and time-truncation rank stability.

## Confirmed protocol concern G — CHARMM36 production nonbonded settings require correction before new MD

The 009 production MDP uses PME with `rvdw = 1.2` and `DispCorr = EnerPres`, but does not document the CHARMM36 force-switch settings recommended in the GROMACS documentation.

For GROMACS CHARMM36, the documented settings include:

- `constraints = h-bonds`
- `cutoff-scheme = Verlet`
- `vdwtype = cutoff`
- `vdw-modifier = force-switch`
- `rlist = 1.2`
- `rvdw = 1.2`
- `rvdw-switch = 1.0`
- `coulombtype = PME`
- `rcoulomb = 1.2`
- `DispCorr = no`

Reference: GROMACS documentation, CHARMM section, Release 2024.

The existing 009 trajectories should remain as a legacy comparative dataset, but should not simply be extended to 50 ns before a corrected-protocol sensitivity test is performed.

## Protocol concern H — artificial charged N terminus at residue 112

Task 009 simulated residues `112-321` and used default `pdb2gmx` charged termini.

Residue 112 is not a biological N terminus in full-length 2C. This creates an artificial terminal charge and removes the native N-terminal context.

Interpretation boundary:

- the system can still serve as a controlled comparative core-fragment screen;
- it should not be treated as a full native-state model;
- corrected validation should document this model limitation;
- later mechanism MD should use a biologically better-defined construct/state if the question moves beyond insertion-screen triage.

## Protocol concern I — equilibration/production transition needs convergence-based validation

Task 009 used short restrained NVT/NPT preparation before unrestrained production.

For inserted 5–9 aa peptides built from predicted structures, the adequacy of this equilibration cannot be assumed from a fixed time alone.

Task 010 must inspect time-series relaxation and perform sensitivity to burn-in choice. Do not choose a burn-in solely because it is a conventional round number.

## Statistical concern J — frames are not independent replicates

Trajectory frames are temporally correlated. Statistical confidence must be based primarily on independent simulation replicas and block/convergence analysis, not on treating hundreds of frames as independent observations.

References:

- Knapp B, Ospina L, Deane CM. *Avoiding False Positive Conclusions in Molecular Simulation: The Importance of Replicas*. J Chem Theory Comput. 2018. DOI: `10.1021/acs.jctc.8b00391`.
- *Reliability and reproducibility checklist for molecular dynamics simulations*. Communications Biology. 2023. DOI: `10.1038/s42003-023-04653-0`.

## Dynamic-network concern K

DCCM and residue-network results from 20 ns trajectories are mechanistic/exploratory unless their stability is demonstrated across replicas, analysis blocks and time windows.

Task 010 must not allow DCCM/network metrics to decide a candidate tier when:

- the sign/magnitude is unstable across replicas;
- the metric changes materially between 10, 15 and 20 ns truncations;
- covariance/subspace agreement is poor;
- effective sampling is insufficient.

## Positive aspects retained from Task 009

The following are valuable and should be preserved:

- 39/39 trajectories reached 20 ns;
- there are three independent velocity seeds per system;
- WT is replicated;
- candidate-panel diversity includes C-terminal and non-C-terminal regions plus conflict controls;
- provenance/manifests are extensive;
- the project already labels MD as comparative perturbation evidence rather than viral-fitness proof.

## Decision on 20 ns versus 50 ns

There is no scientific requirement that every construct must reach 50 ns before wet-lab prioritization.

For this project stage, the decision criterion is convergence and ranking robustness of the observables used for candidate prioritization.

Task 010 must implement an adaptive rule:

- corrected 20 ns may be sufficient for a preliminary experimental priority panel if multiple independent evidence layers agree and MD metrics are stable across replicas/time windows;
- ambiguous or unstable candidates may receive additional replicas and/or extension;
- do not automatically extend all systems to 50 ns;
- any new MD must use the corrected force-field protocol.

## Current scientific boundary

The repository already contains enough non-MD evidence to support a preliminary multi-site experimental panel once the dynamics layer is corrected or down-weighted appropriately.

Task 010 is authorized to produce a **prioritized experimental candidate list**, but not nucleotide-level construct design, experimental protocol design or claims of safety/validation.