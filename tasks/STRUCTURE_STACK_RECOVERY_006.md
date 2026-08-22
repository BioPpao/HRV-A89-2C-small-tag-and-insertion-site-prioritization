# STRUCTURE_STACK_RECOVERY_006

Status: **AUTHORIZED / CONTINUITY-FIRST ENVIRONMENT + MODELING TASK**

Date: 2026-08-22

Branch: `analysis/conservation-002`

## Objective

Resolve the main remaining computational blockers from `CONTINUOUS_TAG_SITE_MODELING_005`, generate actual inserted HRV-A89 2C structural ensembles, and convert the current WT-anchor proxies into WT-vs-tagged perturbation results.

The task must prioritize scientific continuity. A failure of one package or one scheduler/network path must not terminate independent work.

## Core decision: ColabFold is the primary structure engine

For the current project, installing full standalone AlphaFold, OpenFold and ESMFold in parallel is **not required**.

Primary structure-prediction stack:

1. **ColabFold / `colabfold_batch`** — required primary engine.
2. AlphaFold/OpenFold/ESMFold — do not install by default because they largely duplicate the same structure-prediction evidence class and increase environment/storage complexity.
3. Install an alternative structure engine only if ColabFold cannot be made scientifically usable after reasonable recovery attempts.

ColabFold should be used for multi-model / multi-seed inserted-construct ensembles and WT controls.

## Storage policy

Current repository path:

`/public/home/yukang/wf/HRV-A89-2C-small-tag-and-insertion-site-prioritization`

The shared `/public` filesystem has large absolute free space but is already highly utilized. Avoid unnecessary bulk installation and database replication.

Before installation, record:

- `df -h`
- `quota -s` if supported;
- `du -sh . .tools ~/.cache 2>/dev/null`;
- free inode information if relevant.

Do **not** install a full local ColabFold/MMseqs sequence database unless clearly necessary and storage/quota has been explicitly verified. For this small targeted project, prefer the public ColabFold MSA server from a network-capable login context, cache the generated A3M/MSA results, and run GPU inference on Slurm compute nodes offline if necessary.

Do not commit:

- package caches;
- model checkpoints;
- full local sequence databases;
- bulk redundant prediction directories.

Commit only scripts, provenance, compact metrics, selected representative structures when repository-size appropriate, and reports.

## Additional tool stack

### Required open/reproducible support stack

Install/configure as needed:

- ColabFold + AlphaFold backend dependencies;
- JAX CUDA build compatible with the available RTX 3090 driver/runtime;
- OpenMM for relaxation/minimization where supported;
- HH-suite / kalign / MMseqs2 components needed by ColabFold;
- MDTraj and/or MDAnalysis;
- Biopython;
- DSSP-compatible secondary-structure tooling if available;
- structural comparison utilities such as TM-align/US-align where reproducibly obtainable;
- standard Python scientific stack.

### Rosetta / PyRosetta

Scientifically useful for loop/backbone remodeling and energy terms, but installation is license-governed.

Workflow:

1. Check whether Rosetta/PyRosetta already exists in modules, shared software, user paths, or an existing licensed installation.
2. If legally/licensably available, configure it and run the loop/backbone module.
3. If a manual academic-license download/credential action is required, do not fabricate access or accept a license on the user's behalf. Record `DEFERRED_LICENSE_USER_ACTION` and continue the rest of the task.

### FoldX

Scientifically useful as an orthogonal energetic layer but also license-governed.

Use the same logic:

1. check for an existing licensed installation;
2. configure if available;
3. if user license/download action is required, record `DEFERRED_LICENSE_USER_ACTION` and continue.

### Local frustration

Attempt a mature local-frustration workflow only if it can be installed reproducibly. If unavailable, do not fabricate an energy/frustration substitute. Continue with ColabFold ensemble, OpenMM minimization, network and oligomer analyses.

## Continuity-first scheduler/network policy

### Login node versus compute node

The login node may not expose GPU devices. This is expected and is not a blocker.

When GPU work is required:

- inspect Slurm partitions/resources (`sinfo`, `squeue`, `scontrol` as useful);
- submit GPU jobs rather than requiring the current shell to have `nvidia-smi`;
- any allocated CUDA-capable GPU that passes runtime checks is acceptable;
- use the RTX3090 partitions when available.

### Network asymmetry

If login nodes have internet but compute nodes do not:

- download/install packages, model parameters or MSA inputs from the permitted network-capable login context;
- cache them under a user/project-controlled path;
- run prediction/inference from cached resources within Slurm jobs.

Do not stop the task because a compute node cannot reach pip/GitHub/MSA endpoints.

### Slurm waiting

If GPU allocation is pending:

- continue CPU-side sequence preparation, MSA preparation, panel generation, QC scripts, structural metric code and report scaffolding;
- submit jobs and poll at reasonable intervals;
- do not abort the project merely because a GPU is temporarily busy.

### Git/network failure

If push fails:

- continue computation;
- preserve local commits and results;
- retry from a network-capable context at the end.

## Stage 0 — environment recovery and proof-of-life

Required checks:

1. storage/quota audit;
2. Slurm/GPU inventory;
3. existing module/software inventory;
4. ColabFold installation/configuration;
5. model-parameter/cache location;
6. MSA-server reachability from login context;
7. GPU ColabFold smoke test on one WT A89 2C sequence.

The proof-of-life gate is successful only if an actual 321-aa WT A89 2C prediction finishes and produces a parseable structure/result bundle.

Create:

- `results/structure_stack_006/environment_inventory.tsv`
- `results/structure_stack_006/colabfold_smoke_test.tsv`
- `envs/structure_stack_006.yml` or equivalent reproducible environment specification.

If ColabFold fails initially, troubleshoot installation/runtime/MSA/cache/Slurm issues and keep working. Only classify ColabFold as blocked after multiple reasonable recovery paths have been exhausted and documented.

## Stage 1 — modeling panel

Reuse `data/tag_site_modeling_panel_v1.tsv`, but do not spend equal GPU time on all 132 constructs initially.

Create a tiered panel.

### Tier 1 — mandatory structural panel

Model all four fixed tag forms for the required re-audit junctions:

- `203|204`
- `224|225`
- `248|249`
- `256|257`
- `287|288`
- `288|289`
- `289|290`
- `290|291`

Also include at least one or two hard-exclusion/negative-control junctions from the existing panel for calibration.

Include WT A89 2C controls.

### Tier 2 — adaptive expansion

After Tier 1 results are parsed, expand to additional V2-review junctions only when they add a distinct evidence class or outperform Tier 1 under completed structural metrics.

Do not automatically run all 132 constructs at maximum ensemble depth if Tier 1 already resolves the scientific ranking.

Create:

- `data/tag_site_structure_panel_v2.tsv`

## Stage 2 — ColabFold ensemble prediction

For each modeled construct:

- preserve exact sequence and insertion junction;
- generate/reuse MSA with auditable cache/provenance;
- use multiple models/seeds where supported;
- record recycles, model type, MSA mode, templates setting and random seed;
- retain WT controls under equivalent settings;
- separate tag confidence from native 2C confidence.

Use at least a shallow ensemble for all Tier 1 constructs and deeper ensemble replication for the best/most informative subset as resources permit.

Do not use one single AlphaFold/ColabFold model as the final structural conclusion.

Create:

- `results/structure_stack_006/prediction_manifest.tsv`
- `data/tag_site_structure_ensemble_metrics_v2.tsv`
- selected representative structures under a clearly versioned results directory.

## Stage 3 — WT-vs-tagged structural perturbation metrics

Compute per construct and per ensemble:

- native 2C backbone RMSD excluding inserted tag residues;
- local RMSD/displacement around the insertion window;
- TM-score/US-align style global similarity where available;
- native 2C pLDDT/confidence change;
- local secondary-structure preservation;
- tag solvent exposure;
- inserted-tag proximity to native 2C atoms;
- severe clash counts before/after optional relaxation;
- model/seed convergence;
- local contact-map changes.

Create:

- `data/tag_site_structure_perturbation_v2.tsv`

## Stage 4 — relaxation / local geometry

Use OpenMM relaxation/minimization where scientifically appropriate and reproducible.

Compare pre/post-relaxation severe clashes and local geometry. Treat minimization as geometry cleanup, not biological sampling or MD evidence.

If Rosetta/PyRosetta is already licensed/available, add loop/backbone remodeling for the best reduced subset and record closure/conformer/energy metrics.

If Rosetta is not available because of license/user action, continue without stopping.

Create:

- `data/tag_site_loop_feasibility_v2.tsv`
- `results/structure_stack_006/loop_method_status.tsv`

## Stage 5 — energetic layer

If FoldX or Rosetta is legally and technically available, calculate an orthogonal local energetic/stability context for inserted models.

If neither is available, retain explicit `DEFERRED_LICENSE_USER_ACTION` or `DEFERRED_SOFTWARE` status and continue. Do not fabricate approximate FoldX/Rosetta energies.

OpenMM potential energy/minimization diagnostics may be reported separately as geometry/QC metrics but must not be presented as a FoldX/Rosetta-equivalent stability predictor.

Create:

- `data/tag_site_energy_context_v2.tsv`
- `results/structure_stack_006/energy_method_status.tsv`

## Stage 6 — actual tagged oligomer/context analysis

Replace the previous WT-anchor proxy wherever tagged monomer structures now exist.

Using the existing A89 hexamer hypotheses as comparative context only:

- superpose native 2C portions of tagged monomers onto each protomer;
- quantify inserted-tag clashes with neighboring protomers;
- quantify interface-contact changes;
- quantify proximity to pore/context regions;
- identify tag-dependent differences;
- compare the two hexamer hypotheses for robustness.

Do not claim the no-membrane/no-RNA hexamers are the native functional state.

Create:

- `data/tag_site_hexamer_context_v2_tagged.tsv`

## Stage 7 — actual WT-vs-tagged contact-network perturbation

For constructs with inserted structures:

- compute contact maps/networks for WT and tagged structures;
- quantify local contact loss/gain;
- quantify perturbation propagation from insertion neighborhood;
- compare important functional-neighborhood connectivity;
- aggregate across ensemble members rather than relying on one model.

Create:

- `data/tag_site_contact_network_v2_tagged.tsv`

## Stage 8 — integrated re-ranking and robustness

Create a new versioned integrated table:

- `data/tag_site_integrated_perturbation_v2_structure.tsv`

Keep separate columns for:

- functional tier;
- EV-A71 direct insertion phenotype;
- historical insertion evidence;
- phylogeny-aware indel context;
- PLM tag-specific score;
- inserted-structure ensemble perturbation;
- loop/relaxation metrics;
- energy method/status;
- tagged hexamer clash/interface context;
- tagged contact-network perturbation;
- method availability/QC;
- unresolved conflicts.

Do not reduce everything to one opaque weighted score.

Run cross-seed and cross-method robustness.

Create:

- `results/structure_stack_006/cross_method_robustness_v2.tsv`

## Stage 9 — final synthesis

Create:

- `docs/STRUCTURE_STACK_RECOVERY_006_REPORT.md`

The report must answer:

1. Was ColabFold successfully installed and used on Slurm GPU nodes?
2. Which exact ColabFold/JAX/model/MSA settings were used?
3. Which site × tag constructs obtained real inserted 3D ensembles?
4. Which constructs show the lowest relative perturbation across multiple seeds/models?
5. Do `289|290` and `290|291` with MAP8/G196_minimal remain favored relative to the conflict-aware panel?
6. Do `203|204`, `224|225`, `248|249`, `256|257` remain disfavored after actual insertion modeling?
7. Does G196_minimal outperform MAP8 or HA consistently, or only locally?
8. Did actual tagged-hexamer clash/interface analysis change the prior WT-proxy interpretation?
9. Did actual WT-vs-tagged contact-network analysis change ranking?
10. Which modules were completed versus deferred by license/software/resource constraints?
11. Is remaining uncertainty now dominated by absent HRV-A89-specific phenotype rather than missing computational structure evidence?

## Final task state

Return exactly one of:

- `READY_FOR_TARGETED_DYNAMIC_ANALYSIS`
- `NO_COMPUTATIONAL_CONSENSUS_SITE`
- `STRUCTURE_STACK_PARTIALLY_COMPLETE`

A missing licensed Rosetta/FoldX module alone must not force a global blocked state if ColabFold/tagged-structure analyses and other independent modules complete.

## Repository updates

Before completion update:

- `PROJECT_STATE.md`
- `ACTIVE_TASK.md`
- `TODO.md`
- `ANALYSIS_INDEX.md`
- `DECISIONS.md`

Commit scientifically meaningful outputs and push to `origin analysis/conservation-002` when possible.
