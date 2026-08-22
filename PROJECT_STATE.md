# Project State

Last updated: 2026-08-22

Project: **HRV-A89 2C small-tag and insertion-site prioritization**

## Scientific objective

Identify a small set of experimentally testable internal-tag constructs for HRV-A89 2C that minimize predicted perturbation of native 2C biology while remaining detectable in downstream mechanistic experiments.

The computational endpoint is **relative candidate prioritization and perturbation comparison**, not proof of a safe insertion site.

## Current project-level decision state

`TAG_SITE_MODELING_PARTIALLY_COMPLETE`

CONTINUOUS_TAG_SITE_MODELING_005 completed WT-anchor/context analyses but lacked real inserted-structure ensembles. The current priority is therefore to build a fully open/reproducible inserted-structure pipeline rather than depend on restricted-license Rosetta/FoldX components.

## Current active task

`OPEN_STRUCTURE_PIPELINE_007`

Status: **AUTHORIZED / OPEN-LICENSE CONTINUITY-FIRST TASK**

Branch: `analysis/conservation-002`

Task specification:

- `tasks/OPEN_STRUCTURE_PIPELINE_007.md`

`STRUCTURE_STACK_RECOVERY_006` is retained as planning provenance but is superseded as the execution task.

## Open-tool decision

Primary route:

- ColabFold / `colabfold_batch` for inserted-structure ensembles;
- OpenMM for geometry cleanup/QC only;
- US-align/TM-align for structural comparison;
- MDAnalysis/MDTraj for batch structural metrics;
- DSSP-compatible tooling for secondary-structure preservation;
- transparent coordinate-derived contact-network analysis;
- existing A89 hexamer hypotheses for tagged oligomer-context comparison.

Do not require Rosetta, PyRosetta or FoldX. Do not delay the project to obtain restricted licenses.

Standalone AlphaFold, OpenFold and ESMFold are not installed by default because they largely duplicate the same structure-prediction evidence class. Add an alternative open engine only if ColabFold cannot be made scientifically usable after multiple reasonable recovery attempts.

## Storage/runtime policy

Repository path:

`/public/home/yukang/wf/HRV-A89-2C-small-tag-and-insertion-site-prioritization`

The shared `/public` filesystem has large absolute free capacity but high utilization. Therefore:

- audit storage/quota/inodes before installation;
- do not install a full local ColabFold/MMseqs database unless clearly necessary and explicitly justified;
- prefer public MSA-server generation from a network-capable login context;
- cache A3M/MSA and required parameters under user/project-controlled paths;
- run GPU inference on Slurm compute nodes from cached inputs when compute-node networking is restricted;
- do not commit package caches, checkpoints, local sequence databases or bulk redundant prediction directories.

## Continuity-first execution rule

The task must continue through recoverable technical failures.

Expected behavior:

- login node without GPU → inspect Slurm and submit/enter a GPU job;
- GPU queue pending → continue CPU preparation and QC work;
- compute node without internet → download/cache from login context and execute offline on compute node;
- one ColabFold/JAX install path fails → troubleshoot compatibility and try another isolated compatible environment;
- one analysis utility fails → use another mature open utility where possible;
- Git push unavailable → preserve local commits/results and retry from a network-capable context;
- do not rerun completed all-320 global analyses without a concrete QC defect.

A single local failure is not a project-wide blocker.

## Current scientific interpretation entering OPEN_STRUCTURE_PIPELINE_007

The strongest relative constructs from completed non-fabricated layers are:

- `289|290 × MAP8`;
- `289|290 × G196_minimal`;
- `290|291 × MAP8`;
- `290|291 × G196_minimal`.

These remain direct-homolog-conflicted and are not validated or safe.

Mandatory re-audit rows include:

- `203|204`;
- `224|225`;
- `248|249`;
- `256|257`;
- `287|288`;
- `288|289`;
- `289|290`;
- `290|291`.

Real inserted-structure ensembles are allowed to overturn previous weaker rankings.

## Evidence hierarchy

When evidence conflicts, use:

1. direct HRV-A89 insertion/replicon phenotype, if generated;
2. direct homolog 2C insertion phenotype with high-confidence A89 mapping;
3. direct homolog substitution/deletion phenotype and direct 2C genetics/biochemistry;
4. established functional motifs and experimental homolog structures;
5. A89 continuous structural-ensemble evidence;
6. phylogeny-aware HRV-A evolutionary / independent-indel evidence;
7. tag-specific PLM scores;
8. inserted-structure/OpenMM/secondary-structure/contact-network/oligomer-context analyses;
9. targeted dynamics only after a reduced construct set survives perturbation screening.

No lower-level method may silently override stronger evidence.

## Expected OPEN_STRUCTURE_PIPELINE_007 outputs

- `results/open_structure_007/environment_inventory.tsv`
- `results/open_structure_007/colabfold_smoke_test.tsv`
- `data/tag_site_structure_panel_v3_open.tsv`
- `results/open_structure_007/prediction_manifest.tsv`
- `data/tag_site_structure_ensemble_metrics_v3_open.tsv`
- `data/tag_site_structure_perturbation_v3_open.tsv`
- `data/tag_site_openmm_qc_v1.tsv`
- `data/tag_site_secondary_structure_accessibility_v1.tsv`
- `data/tag_site_hexamer_context_v3_open.tsv`
- `data/tag_site_contact_network_v3_open.tsv`
- `data/tag_site_integrated_perturbation_v3_open.tsv`
- `results/open_structure_007/cross_method_robustness_v3.tsv`
- `docs/OPEN_STRUCTURE_PIPELINE_007_REPORT.md`

## Final task state expected

Return exactly one of:

- `READY_FOR_TARGETED_DYNAMIC_ANALYSIS`
- `NO_COMPUTATIONAL_CONSENSUS_SITE`
- `OPEN_STRUCTURE_PIPELINE_PARTIALLY_COMPLETE`

Do not automatically escalate to long MD, final experimental construct recommendation, experimental protocol design, or final RNA/codon design.

## Required future user input

Before final construct recommendation, obtain the exact nucleotide sequence of the experimental HRV-A89 2C region / replicon plasmid. Protein back-translation is not an acceptable substitute for RNA/codon-level auditing.
