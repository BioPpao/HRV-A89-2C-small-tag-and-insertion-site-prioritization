# OPEN_STRUCTURE_PIPELINE_007 Report

Status: **READY_FOR_TARGETED_DYNAMIC_ANALYSIS**

Date: 2026-08-23

Branch: `analysis/conservation-002`

## Scope

This task replaced the blocked restricted-license structure stack with an open, reproducible workflow:

- ColabFold 1.5.3 for WT and inserted-construct structure prediction;
- OpenMM 7.7 CPU implicit-solvent minimization for local geometry QC only;
- US-align from the dedicated environment for WT-vs-tagged structural comparison;
- MDTraj / MDAnalysis / Biopython / SciPy / pandas for coordinate metrics, secondary-structure/accessibility and contact-network analysis;
- existing A89 hexamer hypotheses for comparative tagged-oligomer clash/interface context only.

No Rosetta, PyRosetta or FoldX method was used or required. No long MD, final construct design, RNA/codon design, or experimental protocol design was started.

## Environment And GPU

Primary environment:

`/public/home/yukang/wf/HRV-A89-2C-small-tag-and-insertion-site-prioritization/.tools/envs/open_structure_007`

Recorded files:

- `results/open_structure_007/environment_inventory.tsv`
- `results/open_structure_007/pip_freeze_open_structure_007.txt`
- `envs/open_structure_007.yml`
- `envs/open_structure_007_install_notes.md`

Observed versions:

- Python 3.10.21
- ColabFold 1.5.3
- JAX 0.4.14
- `jaxlib 0.4.14+cuda11.cudnn86`
- `dm-haiku 0.0.10`
- OpenMM 7.7
- CUDA inference used pip CUDA 11 JAX runtime with `nvidia-cudnn-cu11==8.6.0.163`

GPU/Slurm provenance:

- WT smoke job: `164179`
- Tier1 shallow job: `164180`
- deep subset job: `164182`
- node: `gpu15`
- GPU: NVIDIA GeForce RTX 3090, driver 575.57.08, 24576 MiB
- `CUDA_VISIBLE_DEVICES=0`

Storage audit found `/public` at 3.0P total, 2.9P used, 186T available, 94% used. Full local ColabFold/MMseqs databases were not installed. MSA inputs and AlphaFold parameters were cached under project-controlled paths; model parameter caches were not committed.

## ColabFold Proof Of Life

WT HRV-A89 2C, 321 aa, completed successfully:

- output: `results/open_structure_007/wt_smoke/A89_2C_WT_unrelaxed_rank_001_alphafold2_ptm_model_1_seed_007.pdb`
- mean CA pLDDT from PDB: 86.49
- record: `results/open_structure_007/colabfold_smoke_test.tsv`

The final successful ColabFold runs used cached MSA inputs, local AlphaFold parameters and no templates.

## Modeled Panel

Panel file:

- `data/tag_site_structure_panel_v3_open.tsv`

Panel contents:

- WT reference: 1
- mandatory Tier1 junctions: `203|204`, `224|225`, `248|249`, `256|257`, `287|288`, `288|289`, `289|290`, `290|291`
- negative controls: `155|156`, `216|217`
- tag forms: MAP8, HA, G196_minimal, G196_practical_GS
- inserted constructs: 40

Prediction manifest:

- `results/open_structure_007/prediction_manifest.tsv`
- total model rows: 49
- WT model rows: 1
- Tier1/negative-control shallow inserted models: 40
- deeper replicated subset: 4 constructs x 2 additional seeds = 8 additional models
- constructs with 3 total models: `289|290 x MAP8`, `289|290 x G196_minimal`, `290|291 x MAP8`, `290|291 x G196_minimal`

Deep subset provenance:

- `results/open_structure_007/deep_subset_manifest.tsv`
- `results/open_structure_007/deep_subset_runtime.tsv`
- `results/open_structure_007/deep_subset_targets.txt`
- `scripts/open_structure_007_deep_subset.sbatch`

## Generated Tables

Core outputs:

- `data/tag_site_structure_ensemble_metrics_v3_open.tsv` -- 40 construct-level rows
- `data/tag_site_structure_perturbation_v3_open.tsv` -- 49 model-level rows
- `data/tag_site_openmm_qc_v1.tsv` -- 49 model-level rows
- `data/tag_site_secondary_structure_accessibility_v1.tsv` -- 49 model-level rows
- `data/tag_site_hexamer_context_v3_open.tsv` -- 96 model x hexamer rows
- `data/tag_site_contact_network_v3_open.tsv` -- 48 tagged-model rows
- `data/tag_site_integrated_perturbation_v3_open.tsv` -- 40 construct-level rows
- `results/open_structure_007/cross_method_robustness_v3.tsv` -- 40 construct-level rows

US-align status:

- 48 tagged model rows completed;
- WT reference row recorded separately.

OpenMM QC:

- 49/49 rows completed with CPU implicit OBC2 minimization;
- post-minimization severe clash count maximum: 2;
- post-minimization severe clash count median: 0;
- OpenMM was used only as geometry cleanup/QC, not as dynamics or fitness evidence.

## Lowest Relative Perturbation Rows

The lowest structural perturbation rows after real inserted ColabFold models and OpenMM QC remain direct-homolog-conflicted. They are candidate rows for review, not validated sites.

Examples with favorable open-structure metrics:

| Junction | Tag | Models | Native 2C CA RMSD mean A | Local window RMSD mean A | Max tag-neighbor clashes 2.5 A | OpenMM post-clash max | Native contact loss mean | Interpretation |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| `289|290` | HA | 1 | 0.778 | 1.349 | 0 | 0 | 12.0 | lower structure perturbation, direct conflict |
| `289|290` | MAP8 | 3 | 1.166 | 2.555 | 0 | 0 | 15.0 | lower structure perturbation, direct conflict |
| `289|290` | G196_minimal | 3 | 1.301 | 2.000 | 0 | 0 | 12.3 | lower structure perturbation, direct conflict |
| `288|289` | MAP8 | 1 | 1.105 | 2.654 | 0 | 0 | 14.0 | lower structure perturbation, direct conflict |
| `248|249` | MAP8 | 1 | 1.077 | 5.253 | 0 | 0 | 10.0 | lower structure perturbation, direct conflict |

`290|291` retained low clash and contact-loss behavior but deep replicated models increased its native/local RMSD relative to `289|290`:

- `290|291 x MAP8`: 3 models, native RMSD 1.766 A, local RMSD 4.664 A, max tag-neighbor clashes 0, OpenMM post-clash max 0.
- `290|291 x G196_minimal`: 3 models, native RMSD 2.458 A, local RMSD 4.187 A, max tag-neighbor clashes 0, OpenMM post-clash max 0.

## Required Re-Audit Junctions

- `203|204`: strongly structure-disfavored for MAP8/HA/G196_practical_GS; G196_minimal remained mixed. This junction is not a low-perturbation target under open-structure modeling.
- `224|225`: open structures were comparatively low-clash, but the site remains function/direct-evidence conflicted. This is a conflict-control row, not a validated site.
- `248|249`: MAP8 was low-clash and low native RMSD, but other tags were mixed and this row remains historical/modern evidence-conflicted.
- `256|257`: all four tags were high perturbation because of severe tagged-hexamer clash context.
- `287|288`: MAP8/G196 rows were lower perturbation than HA, but still direct-homolog-conflicted.
- `288|289`: all four tags were comparatively low-clash; still direct-homolog-conflicted and less deeply replicated than `289|290`.
- `289|290`: strongest open-structure consensus among the previously favored region, especially MAP8 and G196_minimal with 3-model support.
- `290|291`: no severe tagged-hexamer clashes, but deeper replicated models weakened its rank by local/native RMSD relative to `289|290`.

## Tag-Specific Pattern

G196_minimal did not globally outperform MAP8 or HA.

Tag-level means across 10 junctions per tag:

| Tag | Mean native RMSD A | Mean max tag-neighbor clashes | Low-structure class count |
|---|---:|---:|---:|
| G196_minimal | 2.089 | 4.1 | 7 |
| G196_practical_GS | 1.830 | 10.5 | 5 |
| HA | 2.071 | 8.9 | 5 |
| MAP8 | 2.173 | 8.7 | 7 |

The practical GS-flanked G196 form had worse mean hexamer-clash behavior than G196_minimal. MAP8 and G196_minimal remain the more useful forms for the targeted deep subset, but tag performance is site-dependent.

## Hexamer And Contact-Network Impact

Actual tagged-hexamer placement changed interpretation most strongly for `256|257`, where all tags generated high tag-neighbor clash counts despite prior PLM support. It also preserved `248|249` as a conflict-control row rather than a clean low-risk row.

Contact-network analysis did not overturn the main `289|290` structural preference, but it prevented treating low RMSD alone as sufficient. Several low-RMSD rows still had nontrivial native-contact loss.

## Robustness

`results/open_structure_007/cross_method_robustness_v3.tsv` records:

- `multi_model_available`: 4 constructs;
- `single_model_only`: 36 constructs.

The four multi-model constructs are exactly the predefined deep subset:

- `289|290 x MAP8`
- `289|290 x G196_minimal`
- `290|291 x MAP8`
- `290|291 x G196_minimal`

Conclusions are strongest for comparisons within this four-construct deep subset and weaker for single-model Tier1 rows.

## Remaining Uncertainty

Open-structure computational evidence is no longer the main technical blocker for the current reduced panel. Remaining uncertainty is dominated by:

1. absent direct HRV-A89 insertion phenotype;
2. direct EV-A71 homolog insertion-fitness conflict;
3. template/MSA/AlphaFold-family model dependence;
4. no membrane/RNA/true experimental hexamer state;
5. no long MD;
6. no exact experimental RNA/codon context.

No HRV-A89 junction is called safe or validated by this task.

## Answers To Required Questions

1. The open ColabFold stack was installed and executed successfully.
2. ColabFold 1.5.3, Python 3.10.21, JAX 0.4.14, `jaxlib 0.4.14+cuda11.cudnn86`, OpenMM 7.7, node `gpu15`, RTX 3090, cached MSA inputs, local parameters, no templates.
3. 40 inserted constructs plus WT were modeled; 49 total model rows were analyzed.
4. `289|290 x MAP8` and `289|290 x G196_minimal` are the strongest deep-replicated open-structure rows; `289|290 x HA` is low in single-model structure metrics but was not in the predefined deep subset.
5. Seed/model consistency is available only for the 4 deep-subset constructs. `289|290` is more robust than `290|291` by RMSD/local-window metrics.
6. G196_minimal does not globally outperform MAP8/HA; it is useful locally and less clash-prone than G196_practical_GS.
7. Actual tagged-hexamer analysis strengthened penalties for `256|257` and preserved `248|249` as a conflict-control row.
8. Contact-network perturbation did not overturn the `289|290` preference but kept contact-loss caveats visible.
9. No required open module remained unavailable for this task. Long MD, final construct design and RNA/codon design were intentionally out of scope.
10. Remaining uncertainty is now dominated more by absent HRV-A89-specific phenotype and biological context than by missing inserted-structure computation for the reduced panel.

## Final State

`READY_FOR_TARGETED_DYNAMIC_ANALYSIS`

Stop here for ChatGPT/user review. Do not start long MD or final construct/RNA design without a new authorized task.
