# OPEN_STRUCTURE_PIPELINE_007

Status: **AUTHORIZED / OPEN-LICENSE CONTINUITY-FIRST TASK**

Date: 2026-08-22

Branch: `analysis/conservation-002`

## Objective

Replace the partially blocked structure stack with a workflow that does **not depend on commercial, restricted, or manually licensed Rosetta/FoldX components**. Generate real inserted HRV-A89 2C structure ensembles and derive WT-vs-tagged structural, oligomer-context and contact-network perturbation results.

This task supersedes `STRUCTURE_STACK_RECOVERY_006` as the execution task while preserving it as planning provenance.

## Primary open/reproducible stack

Use the following stack as the default route:

1. **ColabFold / `colabfold_batch`** — primary inserted-structure ensemble engine.
2. **OpenMM** — geometry cleanup/minimization and clash-relief QC only; not MD evidence.
3. **US-align and/or TM-align** — global WT-vs-tagged structural comparison.
4. **MDAnalysis and/or MDTraj** — RMSD, distances, contacts, exposure and batch structure analysis.
5. **DSSP-compatible tooling** — local secondary-structure preservation.
6. **Biopython / standard scientific Python stack** — sequence, mapping and data integration.
7. **Open contact-network analysis implemented transparently from coordinates** — WT-vs-tagged contact-map and graph perturbation.
8. **Existing A89 hexamer hypotheses** — comparative tagged-oligomer clash/interface context only.

Do not require Rosetta, PyRosetta or FoldX. Do not stop to pursue restricted-license software.

## Structure-engine decision

ColabFold is the primary and normally sufficient structure-prediction engine for this stage.

Do not install standalone AlphaFold, OpenFold and ESMFold by default. They are largely redundant for the present evidence class and increase environment/storage complexity.

Only add an alternative open structure engine if ColabFold cannot be made scientifically usable after multiple reasonable recovery attempts.

## Storage policy

Repository path:

`/public/home/yukang/wf/HRV-A89-2C-small-tag-and-insertion-site-prioritization`

The shared `/public` filesystem is highly utilized despite large absolute free capacity. Therefore:

- audit quota, inode and cache use before installation;
- do **not** download a full local ColabFold/MMseqs sequence database unless clearly necessary and explicitly justified;
- prefer public ColabFold MSA-server generation from a network-capable login node;
- cache A3M/MSA and required model parameters under controlled user/project paths;
- run GPU inference on Slurm nodes using cached inputs when compute-node networking is restricted;
- do not commit package caches, model checkpoints, local sequence databases or bulk redundant prediction directories.

## Continuity-first execution policy

The task must continue when one technical path fails.

### GPU not visible in current shell

- detect login-node context;
- inspect `sinfo`, `squeue`, `scontrol` as useful;
- submit/enter a suitable GPU allocation;
- any working CUDA-capable allocated GPU is acceptable;
- continue CPU preparation while waiting.

### Compute node has no internet

- use login-node network access to install/download packages, model parameters and MSA inputs;
- cache them;
- run GPU inference offline on compute nodes.

### ColabFold install/runtime fails

- inspect Python/JAX/CUDA compatibility;
- try isolated user-space environments;
- try compatible ColabFold/JAX versions;
- separate MSA generation from GPU inference;
- reuse cached MSA/parameters;
- only after multiple documented recovery attempts may ColabFold be considered unavailable.

If ColabFold remains unavailable, try one mature **open** alternative structure engine. Do not use a materially weaker ad hoc predictor.

### One analysis utility fails

Use another mature open utility where possible and continue independent modules.

### Git push fails

Continue local analysis, preserve commits/results, and retry from a network-capable context.

A single local method failure is not a global blocker.

## Stage 0 — environment and storage audit

Record:

- `pwd`
- `df -h`
- `df -i`
- `quota -s` if supported
- project/user cache sizes
- Slurm partitions and GPU resources
- relevant environment modules
- existing ColabFold/JAX/OpenMM/US-align/TM-align/MDAnalysis/MDTraj/DSSP installations

Create:

- `results/open_structure_007/environment_inventory.tsv`
- `envs/open_structure_007.yml` or equivalent reproducible environment specification.

## Stage 1 — install and prove ColabFold

Install/configure a reproducible user-space ColabFold GPU environment.

Required proof-of-life:

- real WT HRV-A89 2C, 321 aa;
- successful MSA acquisition or valid cached MSA;
- successful Slurm GPU inference;
- valid predicted structure and parsed confidence outputs;
- exact ColabFold/JAX/CUDA/model/settings recorded.

Create:

- `results/open_structure_007/colabfold_smoke_test.tsv`.

Do not proceed to large batches until this WT smoke test succeeds.

## Stage 2 — tiered structural panel

Reuse previous review data and create:

- `data/tag_site_structure_panel_v3_open.tsv`.

Mandatory Tier 1 junctions:

- `203|204`
- `224|225`
- `248|249`
- `256|257`
- `287|288`
- `288|289`
- `289|290`
- `290|291`

Model fixed tag forms:

- MAP8
- HA
- G196_minimal
- G196_practical_GS

Also include WT and at least one or two hard-exclusion negative controls.

Use shallow ensemble coverage for all Tier 1 constructs and adaptive deeper replication for the best/most informative subset. Do not automatically run all 132 constructs at maximum depth.

## Stage 3 — real inserted ColabFold ensembles

For each modeled construct record:

- exact sequence;
- insertion junction;
- tag form;
- MSA source/cache path;
- model type;
- seeds/models;
- recycles;
- template setting;
- GPU/node/job provenance;
- confidence metrics.

Create:

- `results/open_structure_007/prediction_manifest.tsv`
- `data/tag_site_structure_ensemble_metrics_v3_open.tsv`.

## Stage 4 — WT-vs-tagged perturbation metrics

Compute across ensemble members:

- native 2C backbone RMSD excluding tag residues;
- local insertion-window RMSD/displacement;
- TM-score/US-align style global similarity;
- native 2C confidence change;
- local confidence change;
- secondary-structure preservation;
- tag solvent exposure;
- tag-to-native severe clash/proximity metrics;
- ensemble convergence;
- local contact-map change.

Create:

- `data/tag_site_structure_perturbation_v3_open.tsv`.

## Stage 5 — OpenMM geometry cleanup/QC

Use OpenMM minimization/relaxation only as local geometry cleanup/QC.

Compare pre/post:

- severe clash count;
- local geometry;
- backbone distortion;
- whether a prediction depends on unresolved steric overlap.

Do not interpret this as dynamics, thermodynamic stability, or viral fitness.

Create:

- `data/tag_site_openmm_qc_v1.tsv`.

## Stage 6 — secondary structure and accessibility

Use DSSP-compatible tooling and structural analysis to quantify:

- local helix/sheet/coil preservation;
- changes within defined windows around the insertion;
- tag accessibility/exposure;
- native local burial/exposure changes.

Create:

- `data/tag_site_secondary_structure_accessibility_v1.tsv`.

## Stage 7 — actual tagged hexamer context

For tagged monomer ensemble members:

- superpose the native 2C portion onto both existing A89 hexamer hypotheses;
- quantify tag-neighbor clashes;
- minimum inter-protomer distances;
- interface contact gain/loss;
- local pore/context orientation as a comparative metric only;
- consistency between both hexamer hypotheses.

Create:

- `data/tag_site_hexamer_context_v3_open.tsv`.

Do not claim current no-membrane/no-RNA hexamers are the native functional state.

## Stage 8 — WT-vs-tagged contact-network perturbation

Construct transparent residue-contact networks from coordinates.

Quantify:

- contact loss/gain;
- local degree change;
- insertion-neighborhood network perturbation;
- perturbation propagation toward known functional neighborhoods;
- ensemble consistency.

Create:

- `data/tag_site_contact_network_v3_open.tsv`.

## Stage 9 — open-only integrated evidence and robustness

Create:

- `data/tag_site_integrated_perturbation_v3_open.tsv`
- `results/open_structure_007/cross_method_robustness_v3.tsv`.

Retain separate evidence columns for:

- functional tier;
- EV-A71 direct insertion phenotype;
- historical insertion evidence;
- phylogeny-aware indel context;
- tag-specific PLM;
- inserted-structure ensemble perturbation;
- OpenMM geometry QC;
- secondary-structure/accessibility change;
- tagged hexamer context;
- tagged contact-network perturbation;
- method/QC status;
- unresolved conflicts.

Do not collapse evidence into one opaque weighted score.

## Stage 10 — scientific synthesis

Explicitly test whether these remain relatively least disruptive after real inserted-structure modeling:

- `289|290 × MAP8`
- `289|290 × G196_minimal`
- `290|291 × MAP8`
- `290|291 × G196_minimal`

Also re-evaluate:

- `203|204`
- `224|225`
- `248|249`
- `256|257`
- `287|288`
- `288|289`.

Allow real inserted structures to overturn weaker prior rankings.

## Final report

Create:

- `docs/OPEN_STRUCTURE_PIPELINE_007_REPORT.md`.

It must answer:

1. Was the open ColabFold stack successfully installed and executed?
2. Which exact versions, model settings, MSA settings and GPU nodes were used?
3. How many constructs and ensemble members were successfully modeled?
4. Which constructs show the lowest relative perturbation across real inserted models?
5. Are conclusions consistent across seeds/models?
6. Does G196_minimal outperform MAP8/HA globally or only locally?
7. Did actual tagged-hexamer analysis change the WT-proxy interpretation?
8. Did actual contact-network perturbation change ranking?
9. Which modules remained technically unavailable despite open-tool recovery attempts?
10. Is remaining uncertainty now dominated by absent HRV-A89-specific phenotype rather than missing computational structure evidence?

## Final state

Return exactly one of:

- `READY_FOR_TARGETED_DYNAMIC_ANALYSIS`
- `NO_COMPUTATIONAL_CONSENSUS_SITE`
- `OPEN_STRUCTURE_PIPELINE_PARTIALLY_COMPLETE`

## Prohibited automatic escalation

Do not automatically start long MD.
Do not make final experimental construct recommendations.
Do not perform experimental protocol design.
Do not perform final RNA/codon design without exact experimental nucleotide sequence.
Do not call any site safe or experimentally validated.

## Repository updates

Before completion update consistently:

- `PROJECT_STATE.md`
- `ACTIVE_TASK.md`
- `TODO.md`
- `ANALYSIS_INDEX.md`
- `DECISIONS.md`

Commit scientifically meaningful outputs and push to `origin analysis/conservation-002` when possible. If push fails, preserve local commits and continue.
