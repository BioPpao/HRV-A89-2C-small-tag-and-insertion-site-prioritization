# Project State

Last updated: 2026-08-22

Project: **HRV-A89 2C small-tag and insertion-site prioritization**

## Scientific objective

Identify a small set of experimentally testable internal-tag constructs for HRV-A89 2C that minimize predicted perturbation of native 2C biology while remaining detectable in downstream mechanistic experiments.

The computational endpoint is **relative candidate prioritization and perturbation comparison**, not proof of a safe insertion site.

## Current project-level decision state

`TAG_SITE_MODELING_PARTIALLY_COMPLETE`

CONTINUOUS_TAG_SITE_MODELING_005 completed all available WT-anchor/context analyses for the 33-junction x 4-tag panel but lacked mature inserted-structure, loop-remodeling and local energy workflows.

The main remaining computational blocker is therefore now an environment/method-stack problem rather than another global site-scoring problem.

## Current active task

`STRUCTURE_STACK_RECOVERY_006`

Status: **AUTHORIZED / CONTINUITY-FIRST ENVIRONMENT + MODELING TASK**

Branch: `analysis/conservation-002`

Task specification:

- `tasks/STRUCTURE_STACK_RECOVERY_006.md`

## Structure-engine decision

For the current project, **ColabFold / `colabfold_batch` is the primary required structure-prediction engine**.

Standalone AlphaFold, OpenFold and ESMFold are not installed by default because they are largely redundant for the present evidence class and add unnecessary environment/storage complexity. An alternative structure engine is only warranted if ColabFold cannot be made scientifically usable after reasonable recovery attempts.

## Storage/runtime policy

Repository path:

`/public/home/yukang/wf/HRV-A89-2C-small-tag-and-insertion-site-prioritization`

The shared `/public` filesystem has substantial absolute free space but high utilization. The task must audit quota/storage before installation and avoid a full local ColabFold/MMseqs database unless clearly required.

Preferred workflow:

- obtain/cache MSAs from a network-capable login context using the public ColabFold MSA service;
- keep A3M/MSA and model caches in a controlled user/project location;
- run GPU inference on Slurm compute nodes using cached inputs when compute-node networking is restricted.

## Additional methods

The task also attempts to recover orthogonal methods where legally/technically available:

- OpenMM relaxation/minimization and structural QC;
- MDTraj/MDAnalysis and structural comparison utilities;
- Rosetta/PyRosetta for loop/backbone remodeling if an existing licensed installation or legitimate user-provided access is available;
- FoldX for an orthogonal energetic layer if an existing licensed installation or legitimate user-provided access is available;
- local-frustration analysis if a mature reproducible workflow is available.

Rosetta/FoldX license requirements must not cause the whole task to stop. If user license action is required, only that module is deferred.

## Continuity-first execution rule

The task must continue through independent work when one local resource fails.

Expected recovery behavior:

- login node without GPU → use Slurm rather than stopping;
- GPU partition unavailable → inspect alternatives and continue CPU preparation;
- compute-node internet blocked → download/cache from login context and execute offline on compute node;
- preferred package fails → try another mature method in the same evidence class;
- licensed package unavailable → mark only that module `DEFERRED_LICENSE_USER_ACTION`;
- Git push unavailable → preserve local commits/results and retry later;
- do not rerun completed global all-320 analyses unless a concrete QC defect is found.

## Current scientific interpretation entering STRUCTURE_STACK_RECOVERY_006

The strongest relative constructs from completed non-fabricated layers are:

- `289|290 × MAP8`;
- `289|290 × G196_minimal`;
- `290|291 × MAP8`;
- `290|291 × G196_minimal`.

These remain direct-homolog-conflicted and are not validated or safe.

Important conflict/control rows include:

- `203|204`;
- `224|225`;
- `248|249`;
- `256|257`;
- `287|288`;
- `288|289`;
- `289|290`;
- `290|291`.

The next task must generate real inserted structural ensembles before these relative rankings can be strengthened.

## Evidence hierarchy

When evidence conflicts, use:

1. direct HRV-A89 insertion/replicon phenotype, if generated;
2. direct homolog 2C insertion phenotype with high-confidence A89 mapping;
3. direct homolog substitution/deletion phenotype and direct 2C genetics/biochemistry;
4. established functional motifs and experimental homolog structures;
5. A89 continuous structural-ensemble evidence;
6. phylogeny-aware HRV-A evolutionary / independent-indel evidence;
7. tag-specific PLM scores;
8. insertion-specific loop/structure/energy/network analyses;
9. targeted dynamics only after a reduced construct set survives perturbation screening.

No lower-level method may silently override stronger evidence.

## Expected STRUCTURE_STACK_RECOVERY_006 outputs

Primary outputs include:

- `results/structure_stack_006/environment_inventory.tsv`
- `results/structure_stack_006/colabfold_smoke_test.tsv`
- `data/tag_site_structure_panel_v2.tsv`
- `results/structure_stack_006/prediction_manifest.tsv`
- `data/tag_site_structure_ensemble_metrics_v2.tsv`
- `data/tag_site_structure_perturbation_v2.tsv`
- `data/tag_site_loop_feasibility_v2.tsv`
- `data/tag_site_energy_context_v2.tsv`
- `data/tag_site_hexamer_context_v2_tagged.tsv`
- `data/tag_site_contact_network_v2_tagged.tsv`
- `data/tag_site_integrated_perturbation_v2_structure.tsv`
- `results/structure_stack_006/cross_method_robustness_v2.tsv`
- `docs/STRUCTURE_STACK_RECOVERY_006_REPORT.md`

## Final task state expected

Return exactly one of:

- `READY_FOR_TARGETED_DYNAMIC_ANALYSIS`
- `NO_COMPUTATIONAL_CONSENSUS_SITE`
- `STRUCTURE_STACK_PARTIALLY_COMPLETE`

Do not automatically escalate to long MD, final experimental construct recommendation, experimental protocol design, or final RNA/codon design.

## Required future user input

Before final construct recommendation, obtain the exact nucleotide sequence of the experimental HRV-A89 2C region / replicon plasmid. Protein back-translation is not an acceptable substitute for RNA/codon-level auditing.
