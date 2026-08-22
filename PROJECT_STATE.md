# Project State

Last updated: 2026-08-22

Project: **HRV-A89 2C small-tag and insertion-site prioritization**

## Scientific objective

Identify a small set of experimentally testable internal-tag constructs for HRV-A89 2C that minimize predicted perturbation of native 2C biology while remaining detectable in downstream mechanistic experiments.

The computational endpoint is **relative candidate prioritization and perturbation comparison**, not proof of a safe insertion site.

## Current project-level decision state

`READY_FOR_CONFLICT_AWARE_TAG_SITE_MODELING`

GPU_RECOVERY_004 recovered the previously blocked tag-specific PLM stage on an RTX 3090 Slurm node and completed all 1,280 planned MAP8/HA/G196 tag × junction scores.

The project has now finished the major all-320 global discovery layers. The next priority is reduced insertion-specific structural perturbation modeling rather than adding more global scoring methods.

## Current active task

`CONTINUOUS_TAG_SITE_MODELING_005`

Status: **AUTHORIZED / CONTINUITY-FIRST COMPUTATIONAL TASK**

Branch: `analysis/conservation-002`

Task specification:

- `tasks/CONTINUOUS_TAG_SITE_MODELING_005.md`

## Why this task is next

The current evidence stack already includes:

- A89 functional constraints;
- four-structure WT geometry;
- HRV-A conservation;
- phylogeny-aware independent-indel evidence;
- EV-A71 insertion/deletion/substitution phenotype mapping;
- all-320 Pareto/robustness analysis;
- MAP8/HA/G196 tag-specific ESM2 PLM scores;
- V5 integrated evidence matrix;
- V2 computational review set.

The main unresolved computational question is now construct-specific:

> after inserting a particular tag at a particular review junction, how strongly is the native 2C structural environment perturbed?

## New methods authorized in CONTINUOUS_TAG_SITE_MODELING_005

The task adds missing/underused orthogonal computational layers:

1. insertion-specific structure-prediction ensembles;
2. loop/backbone closure and conformational feasibility modeling;
3. local energetic/frustration analysis;
4. oligomer-context compatibility analysis;
5. residue-contact-network perturbation analysis;
6. targeted phylogeny-aware site-rate / coevolution / flexibility checks where technically defensible;
7. cross-method robustness analysis.

These methods are secondary perturbation-ranking layers and cannot override direct phenotype or hard functional constraints.

## Continuity-first execution rule

The task must not stop merely because one preferred tool, package, GPU, scheduler context, network route, or Git push is unavailable.

Required recovery behavior:

- detect login-node versus Slurm compute-node context;
- request/submit GPU work when needed;
- continue CPU-capable work while GPU jobs are pending when useful;
- use login-node network access to prepare dependencies/checkpoints for compute-node execution when necessary;
- try alternative mature methods within the same evidence class if the preferred package fails;
- mark only the affected module deferred when no mature substitute is available;
- continue independent modules;
- preserve local commits/results if remote push temporarily fails.

A single local method failure is not a project-wide blocker.

## Fixed project constraints

- FLAG remains excluded because the 9A5 construct already uses FLAG.
- Ranking unit remains peptide junction `i|i+1`.
- Monomer-only exposure is insufficient.
- Current A89 hexamers are no-membrane/no-RNA hypotheses and are comparative context models only.
- Conservation and PLM are supporting evidence, not direct insertion-tolerance proof.
- Direct homolog insertion phenotype remains a high-weight prior, not an absolute HRV-A89 veto.
- Structure prediction is a perturbation screen, not biological validation.
- Exact RNA/codon analysis still requires the real experimental nucleotide construct.
- No computational analysis may label a site safe or experimentally validated.

## Current candidate/control interpretation

### `287|288`, `288|289`, `289|290`, `290|291`

`STRUCTURE_EVOLUTION_FAVORED__DIRECT_HOMOLOG_CONFLICT`

### `248|249`, `256|257`

`HISTORICAL_INSERTION_SUPPORT__MODERN_CONFLICT_CONTROL`

### Outside-strict examples such as `203|204`, `224|225`

Remain useful conflict-aware review rows, not preferred sites.

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

## Required outputs from current task

Expected primary outputs include:

- `data/tag_site_modeling_panel_v1.tsv`
- `results/tag_site_modeling_005/environment_and_method_inventory.tsv`
- `data/tag_site_structure_ensemble_metrics_v1.tsv`
- `data/tag_site_loop_feasibility_v1.tsv`
- `data/tag_site_energy_context_v1.tsv`
- `data/tag_site_contact_network_v1.tsv`
- `data/tag_site_hexamer_context_v1.tsv`
- `data/tag_site_integrated_perturbation_v1.tsv`
- `results/tag_site_modeling_005/cross_method_robustness.tsv`
- `docs/CONTINUOUS_TAG_SITE_MODELING_005_REPORT.md`

## Final state expected from current task

Return exactly one of:

- `READY_FOR_TARGETED_DYNAMIC_ANALYSIS`
- `NO_COMPUTATIONAL_CONSENSUS_SITE`
- `TAG_SITE_MODELING_PARTIALLY_COMPLETE`

Do not automatically escalate to long MD, final experimental construct recommendation, experimental protocol design, or final RNA/codon design.

## Required future user input

Before final construct recommendation, obtain the exact nucleotide sequence of the experimental HRV-A89 2C region / replicon plasmid. Protein back-translation is not an acceptable substitute for RNA/codon-level auditing.
