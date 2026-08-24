# Project State

Last updated: 2026-08-24

Project: **HRV-A89 2C small-tag and insertion-site prioritization**

## Final Scientific Objective

Build a ranked, redundant, multi-junction x multi-tag experimental candidate panel for HRV-A89 2C internal tagging.

No computational result may be described as safe or experimentally validated.

## Current Project-Level State

`MD_ANALYSIS_AUDIT_REQUIRED__PRELIMINARY_WET_PANEL_EVIDENCE_AVAILABLE`

## Current Branch And Task

Branch:

`analysis/dynamics-audit-010`

Task:

`DYNAMICS_ANALYSIS_AUDIT_AND_CANDIDATE_RERANK_010`

Primary specification:

- `tasks/DYNAMICS_ANALYSIS_AUDIT_AND_CANDIDATE_RERANK_010.md`

Primary audit:

- `docs/DYNAMICS_009_POSTHOC_AUDIT_V1.md`

## What Remains Valid From Task 009

Task 009 generated a substantial legacy comparative MD dataset:

- WT plus 12 tagged A89 2C `112-321` systems;
- 3 independent replicas per system;
- 39 / 39 replicas reached 20 ns;
- 780 ns total production sampling;
- trajectory/energy/provenance files exist for reanalysis;
- C-terminal, non-C-terminal and control constructs are represented.

These trajectories are **not discarded**. They are the primary raw input for corrected Task 010 reanalysis.

## Why The Previous Dynamics Ranking Is Provisional

Posthoc audit identified several decision-changing problems:

1. the 009 Python analysis did not explicitly make the protein whole/unwrap/center under periodic boundary conditions before geometry-dependent metrics;
2. the main RMSD is self-drift versus each system's own first frame, not direct deviation from a common WT reference;
3. local RMSF lacks a junction-matched WT baseline for every candidate;
4. contact retention primarily tracks candidate-starting-model contacts rather than preservation of WT-defined native contacts;
5. tag exposure is a minimum-distance proxy rather than mature SASA/accessibility evidence;
6. dynamic Tier A/B penalties use incomplete and threshold-sensitive metrics;
7. DCCM/network signals require stronger replica/time-window stability checks;
8. the Task 009 CHARMM36 production MDP differs from the GROMACS-documented CHARMM36 nonbonded protocol and should not simply be extended to 50 ns.

Therefore these files remain historical/provisional rather than final ranking authority:

- `data/final_candidate_panel_v2_dynamics.tsv`
- `results/broad_dynamics_009/ranking_robustness_v2.tsv`
- `data/broad_dynamics_metrics_v1.tsv`
- `data/tag_exposure_dynamics_v1.tsv`
- `data/contact_persistence_dynamics_v1.tsv`
- `data/dynamic_network_perturbation_v1.tsv`

## Stronger Non-MD Evidence Still Retained

The following project layers remain decision-relevant and are not invalidated by the MD audit:

- A89 functional exclusion/caution map;
- all-320 junction structural/evolutionary landscape;
- HRV-A conservation and phylogeny-aware indel evidence;
- EV-A71 direct insertion/deletion/substitution phenotype mapped to A89;
- tag-specific PLM evidence;
- inserted-structure ensemble modeling;
- historical poliovirus insertion genetics;
- RNA-holoenzyme mapping as homolog/preprint mechanistic context;
- tag/binder accessibility evidence;
- candidate-panel diversification strategy.

The direct homolog insertion signal remains a strong negative prior for all current candidates but is not treated as an absolute HRV-A89 veto.

## Task 010 Required Outputs

Expected core outputs include:

- `results/dynamics_audit_010/input_trajectory_inventory.tsv`
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

## 20 ns Versus 50 ns Decision

There is no project rule that all systems must reach 50 ns.

Task 010 uses an adaptive criterion:

- corrected 20 ns may be sufficient for screening-level wet-lab prioritization if independent evidence agrees and decision-relevant observables are stable across replicas/time windows;
- add replicas when between-replica variability dominates;
- extend selected corrected-protocol replicas toward 50 ns when multiple replicas show continuing slow drift or a decision-critical ambiguity remains;
- never extend all 39 legacy trajectories merely to satisfy a round-number duration target.

## Model Boundary

Current 009 MD is an apo protein-only `112-321` core-fragment screen with an artificial fragment N terminus. It is useful for comparative perturbation triage but cannot represent full-length membrane/RNA/ATP/oligomer biology.

No amount of generic trajectory extension removes this model limitation.

## Current Candidate Interpretation Before Task 010 Rerank

Do not use the old 009 Tier A/B calls as final priorities.

Retain candidate identities as hypotheses only:

- C-terminal cluster: `288|289`, `289|290`, `290|291` with MAP8/HA/G196 variants;
- non-C-terminal alternatives: `224|225`, `248|249`, `203|204`;
- conflict/control region: `256|257`;
- hard-negative control: `155|156`.

The C-terminal adjacent junctions count as one biological region for diversity reporting.

## Final Task 010 Target State

Preferred:

`AUDITED_CANDIDATE_PANEL_READY_FOR_EXPERIMENTAL_REVIEW`

Allowed if corrected-protocol validation is still running at checkpoint:

`CANDIDATE_PRIORITY_PROVISIONAL_PENDING_CORRECTED_PROTOCOL_VALIDATION`

## Stop Boundary

Task 010 does not authorize:

- exact nucleotide/codon design;
- wet-lab procedural protocol design;
- broad membrane/RNA/ATP/antibody mechanistic MD;
- claims of safety/validation;
- automatic merge to `main`.

Before nucleotide-level construct design, obtain the exact experimental HRV-A89 2C/replicon/plasmid nucleotide context.
