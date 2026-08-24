# Project State

Last updated: 2026-08-24

Project: **HRV-A89 2C small-tag and insertion-site prioritization**

## Final scientific objective

Build a **ranked, redundant, multi-junction × multi-tag experimental candidate panel** for HRV-A89 2C internal tagging that minimizes predicted perturbation while remaining experimentally detectable.

The endpoint is not one computationally optimal site. The endpoint is a diversified panel with primary candidates, secondary/rescue candidates, conflict controls and hard-negative controls for downstream wet-lab validation.

No computational result may be described as safe or experimentally validated.

## Current project-level state

`BROAD_DYNAMICS_PARTIALLY_COMPLETE`

## Current active branch and task

Branch:

`analysis/broad-dynamics-009`

Active task:

`BROAD_DYNAMICS_AND_RECOVERY_009`

Execution state:

**AUTONOMOUS CONTINUATION AUTHORIZED / GROMACS PREPRODUCTION COMPLETE / PRODUCTION MD RUNNING OR QUEUED**

Primary task specification:

- `tasks/BROAD_DYNAMICS_AND_RECOVERY_009.md`

Continuation authority:

- `tasks/BROAD_DYNAMICS_AND_RECOVERY_009_CONTINUATION.md`

The 009 task remains active. The previous Codex session ended at a checkpoint but this is not a scientific stop gate and does not authorize creation of a new task/branch.

## Branch provenance

Current branch chain:

`analysis/conservation-002`
→ `analysis/candidate-panel-008`
→ `analysis/broad-dynamics-009`

`analysis/candidate-panel-008` remains the stable completed pre-dynamics candidate-panel checkpoint.

## Completed evidence inherited by 009

The repository contains:

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
- tag-portfolio/binder-accessibility review;
- expanded 18-construct / 36-model ColabFold replication;
- preliminary Tier A / Tier B / control panel and ranking robustness.

## 009 checkpoint completed work

Completed in the partial 009 checkpoint:

- repository/environment/input/software audit;
- `248|249 × HA` OpenMM failure audit, classified `MODEL_SPECIFIC_GEOMETRY_FAILURE` rather than biological failure;
- all-320 disorder placeholder layer, explicitly low-evidence because the mature predictor installation did not complete;
- focused PA14/AGIA single-sequence exploratory ColabFold screen;
- balanced dynamics panel V2;
- WT/tagged `112–321` system manifest and residue mapping;
- explicit placeholder/no-trajectory outputs for trajectory-dependent tables.

Primary 009 report:

- `docs/BROAD_DYNAMICS_AND_RECOVERY_009_REPORT.md`

Run log:

- `docs/BROAD_DYNAMICS_AND_RECOVERY_009_RUN_LOG.md`

## Important unresolved items

1. local tagged dimer/trimer ColabFold models remain pending;
2. current disorder layer uses a composition/low-complexity proxy and is not decision-grade;
3. PA14/AGIA low-pLDDT results are method-limited single-sequence predictions, not biological rejection;
4. GROMACS 2024.2 is available and WT plus all 12 tagged systems passed topology/minimization/NVT/NPT/100 ps smoke preproduction;
5. 39 production replicas have been submitted for the 20 ns broad minimum-coverage stage, with rows `0-3` under Slurm job `164351` and rows `4-38` under Slurm job `164359`;
6. trajectory-dependent metrics remain placeholders and must not be interpreted as dynamics evidence until production trajectories complete and pass QC.

## Execution authority now granted

Within task 009, Codex may proceed without routine user confirmation to:

- create/repair user-space open-source environments;
- install open-source packages;
- repair PDBFixer/setuptools/pkg_resources or equivalent environment defects;
- load cluster modules and compile small open utilities;
- troubleshoot ColabFold/OpenMM/GROMACS workflows;
- submit Slurm jobs/job arrays;
- cancel/resubmit Codex-owned failed or stuck jobs when justified;
- restart GROMACS from checkpoints;
- make consistent routine MD implementation choices and record them;
- commit compact scientific outputs and retry Git pushes.

Do not use `sudo`, restricted-license software, fabricated credentials or destructive actions outside project-owned files.

## Dynamics-system decision

Primary broad comparative screening system:

**native HRV-A89 2C residues `112–321`**, retaining the exact inserted tag and using equivalent terminal treatment for WT and every construct.

This is a comparative perturbation assay, not a complete native-state model.

Broad screening remains apo/protein-only. ATP/Mg, membrane, RNA and antibody/binder states remain outside task 009.

## Replicate policy

Primary target:

- 3 independent replicas × 50 ns per valid system.

Minimum broad-coverage milestone before selective extension:

- 3 × 20 ns per valid system.

Replica breadth has priority over one long trajectory.

## Continuation requirement

Codex must not stop the overall task for one recoverable package/model/job/network/push failure.

Required behavior:

`diagnose → repair/fallback → record → continue independent work → revisit`

Stopping before minimum coverage is acceptable only for a genuine hard blocker defined in `tasks/BROAD_DYNAMICS_AND_RECOVERY_009_CONTINUATION.md` or when all remaining work is already submitted and legitimately running/queued under Slurm.

## Current 009 Slurm checkpoint

- Local multimer: `164291`, running on RTX3090 `gpu16`.
- Production stage 1: `164351_0-3`, running on RTX3090 `gpu16/gpu17`.
- Production stage 2: `164359_4` running and `164359_5-38` queued with generic `gpu:1` across account-accessible `A40,RTX3090` partitions.
- `RTX3090-autoEM` was checked but is not usable by the current `chengtong` account because that partition allows only `cryosparc,cryoem`.

## Ranking policy

Do not use one opaque weighted scalar.

Final ranking must retain separate evidence axes and use:

- Pareto/non-dominated membership;
- evidence classes;
- leave-one-layer-out sensitivity;
- bootstrap/rank stability where meaningful;
- explicit unresolved-conflict labels;
- site-region diversity and tag-family diversity checks.

No lower-level computational method may silently override stronger direct phenotype or hard biological constraints.

## Required real 009 completion outputs

A dynamics-informed completion requires real trajectory-derived values in:

- `results/broad_dynamics_009/production_manifest.tsv`
- `results/broad_dynamics_009/replica_completion.tsv`
- `data/dynamics_replica_qc_v1.tsv`
- `data/broad_dynamics_metrics_v1.tsv`
- `data/tag_exposure_dynamics_v1.tsv`
- `data/contact_persistence_dynamics_v1.tsv`
- `data/dynamic_network_perturbation_v1.tsv`
- `data/final_candidate_panel_v2_dynamics.tsv`
- `results/broad_dynamics_009/ranking_robustness_v2.tsv`
- `docs/BROAD_DYNAMICS_AND_RECOVERY_009_REPORT.md`

Placeholder rows do not count as completion.

## Current stop gate after 009

Do not automatically proceed to:

- wet-lab construct synthesis/design;
- exact RNA/codon design without the real experimental nucleotide context;
- membrane/RNA/ATP/antibody mechanistic MD;
- experimental protocols.

## Required future user input

Before final nucleotide-level construct design, obtain the exact experimental HRV-A89 2C/replicon/plasmid nucleotide context. Protein back-translation is not an acceptable substitute.
