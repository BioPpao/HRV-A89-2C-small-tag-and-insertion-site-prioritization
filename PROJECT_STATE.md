# Project State

Last updated: 2026-08-24

Project: **HRV-A89 2C small-tag and insertion-site prioritization**

## Final scientific objective

Build a **ranked, redundant, multi-junction × multi-tag experimental candidate panel** for HRV-A89 2C internal tagging that minimizes predicted perturbation while remaining experimentally detectable.

The endpoint is not one computationally optimal site. The endpoint is a diversified panel with primary candidates, secondary/rescue candidates, conflict controls and hard-negative controls for downstream wet-lab validation.

No computational result may be described as safe or experimentally validated.

## Current project-level state

`BROAD_DYNAMICS_AND_RECOVERY_009_AUTHORIZED`

## Current active branch and task

Branch:

`analysis/broad-dynamics-009`

Active task:

`BROAD_DYNAMICS_AND_RECOVERY_009`

Status:

**AUTHORIZED / PRE-DYNAMICS RECOVERY + BROAD REPLICATED DYNAMICS**

Task specification:

- `tasks/BROAD_DYNAMICS_AND_RECOVERY_009.md`

## Branch provenance

Current branch chain:

`analysis/conservation-002`
→ `analysis/candidate-panel-008`
→ `analysis/broad-dynamics-009`

`analysis/candidate-panel-008` remains the stable completed `CANDIDATE_PANEL_EXPANSION_008` checkpoint. New recovery/dynamics work is isolated on `analysis/broad-dynamics-009`.

## Completed evidence stack inherited by 009

The project already contains:

- A89 functional constraint/exclusion mapping;
- all-320 WT structural metrics;
- HRV-A conservation and natural-indel context;
- phylogeny-aware independent-indel analysis;
- EV-A71 direct insertion/deletion/substitution phenotype mapping;
- continuous/Pareto all-320 ranking;
- tag-specific ESM2 PLM scores;
- real ColabFold inserted-structure modeling;
- OpenMM geometry QC;
- WT-vs-tagged structural perturbation metrics;
- rigid tagged-hexamer context;
- tagged contact-network analysis;
- RNA-holoenzyme residue-neighborhood mapping;
- protease/polyprotein boundary-risk annotations;
- realistic tag portfolio review;
- binder-accessibility geometry proxies;
- expanded 18-construct / 36-model ColabFold replication;
- preliminary Tier A / Tier B / control panel and ranking robustness.

## CANDIDATE_PANEL_EXPANSION_008 checkpoint

Primary report:

- `docs/CANDIDATE_PANEL_EXPANSION_008_REPORT.md`

Current draft panel:

- Tier A: 8 constructs;
- Tier B: 8 constructs;
- Controls: 2 constructs.

Important limitation: although Tier A contains 6 junctions, 6/8 Tier A constructs come from the contiguous `287|288–290|291` C-terminal neighborhood. The current proposed dynamics panel is also MAP8-heavy. These are selection-bias issues, not proof that the C-terminal cluster is globally superior.

## Technical gaps explicitly carried into 009

1. `248|249 × HA` had one OpenMM failure: `Particle coordinate is nan`;
2. local tagged dimer/trimer accommodation modeling remained deferred;
3. disorder/disordered-binding prediction was incomplete;
4. PA14 and AGIA were literature-reviewed but not actually structure-modeled;
5. rigid placement into WT hexamer does not allow neighboring-protomer accommodation;
6. dynamics has not yet tested replicate stability, tag-exposure persistence or dynamic-network propagation.

Task 009 must resolve these where technically possible before producing a revised candidate panel.

## Dynamics-system decision

For broad candidate comparison, do **not** use full-length 2C in bulk-water MD as the primary system because the N-terminal region is membrane-associated and would introduce a major non-physiological artifact.

Primary comparative screening system:

**native HRV-A89 2C residues 112–321**, retaining the exact inserted tag and using equivalent terminal treatment for WT and every candidate.

This is explicitly a comparative perturbation assay, not a complete native-state model.

Broad screening remains apo/protein-only. ATP/Mg, membrane, RNA and antibody/binder states are reserved for later mechanistic sensitivity tasks.

## Replicate policy

Default production target:

- 3 independent replicas × 50 ns per system;
- WT reference under the identical protocol;
- if resources prevent full completion, first obtain at least 3 × 20 ns for all systems before selectively extending any construct.

Independent replicate breadth has priority over one long trajectory.

## Candidate-panel diversity policy

Before dynamics, generate `data/balanced_targeted_dynamics_panel_v2.tsv` with approximately 10–12 tagged constructs plus WT.

Require:

- at least 4 genuinely distinct site regions;
- at least 3 tag systems;
- reduced dominance of the contiguous `287–291` region;
- at least one hard-negative/control and one mechanistic conflict control;
- pre-MD selection rationale frozen before trajectories are analyzed.

Focused PA14/AGIA modeling may add at most one or two new-tag constructs to dynamics only if the pre-MD structure/oligomer/binder evidence is competitive.

## Ranking policy

Do not use one opaque weighted scalar.

Final ranking must retain separate evidence axes and use:

- Pareto/non-dominated membership;
- evidence classes;
- leave-one-layer-out sensitivity;
- bootstrap/rank stability where meaningful;
- explicit unresolved-conflict labels;
- explicit site-region diversity and tag-family diversity checks.

No lower-level computational method may silently override stronger direct phenotype or hard biological constraints.

## Expected 009 outputs

Core outputs include:

- `results/broad_dynamics_009/openmm_248_249_HA_root_cause.tsv`
- `data/hrvA89_2C_disorder_v1.tsv`
- `data/junction_feature_matrix_v7_pre_dynamics.tsv`
- `data/local_multimer_tag_context_v2.tsv`
- `data/exploratory_tag_structure_panel_v1.tsv`
- `data/exploratory_tag_structure_metrics_v1.tsv`
- `data/balanced_targeted_dynamics_panel_v2.tsv`
- `results/broad_dynamics_009/system_manifest.tsv`
- `results/broad_dynamics_009/production_manifest.tsv`
- `data/dynamics_replica_qc_v1.tsv`
- `data/broad_dynamics_metrics_v1.tsv`
- `data/tag_exposure_dynamics_v1.tsv`
- `data/contact_persistence_dynamics_v1.tsv`
- `data/dynamic_network_perturbation_v1.tsv`
- `data/final_candidate_panel_v2_dynamics.tsv`
- `results/broad_dynamics_009/ranking_robustness_v2.tsv`
- `docs/BROAD_DYNAMICS_AND_RECOVERY_009_REPORT.md`

## Current stop gate

Do not automatically proceed after task 009 to:

- wet-lab construct synthesis/design;
- final RNA/codon design without the exact experimental nucleotide context;
- membrane/RNA/ATP mechanistic MD;
- experimental protocols.

## Required future user input

Before final construct design, obtain the exact experimental HRV-A89 2C/replicon/plasmid nucleotide context. Protein back-translation is not an acceptable substitute.
