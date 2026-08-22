# CONTINUOUS_TAG_SITE_MODELING_005_REPORT

Status: **TAG_SITE_MODELING_PARTIALLY_COMPLETE**

Date: 2026-08-22

Branch: `analysis/conservation-002`

## Scope Completed

Built a compact conflict-aware panel from `data/computational_review_set_v2_plm_gpu.tsv`:

- 33 review junctions.
- 4 fixed tag forms per junction: MAP8, HA, G196_minimal, G196_practical_GS.
- 132 site x tag constructs total.
- All required re-audit junctions are covered with all four tags: `203|204`, `224|225`, `248|249`, `256|257`, `287|288`, `288|289`, `289|290`, `290|291`.

Primary generated files:

- `data/tag_site_modeling_panel_v1.tsv`
- `results/tag_site_modeling_005/environment_and_method_inventory.tsv`
- `data/tag_site_structure_ensemble_metrics_v1.tsv`
- `data/tag_site_loop_feasibility_v1.tsv`
- `data/tag_site_energy_context_v1.tsv`
- `data/tag_site_contact_network_v1.tsv`
- `data/tag_site_hexamer_context_v1.tsv`
- `data/tag_site_integrated_perturbation_v1.tsv`
- `results/tag_site_modeling_005/cross_method_robustness.tsv`
- `results/tag_site_modeling_005/summary_qc.tsv`

Reproducible entry point:

```bash
.tools/envs/hrv2c-one-shot/bin/python3.11 scripts/continuous_tag_site_modeling_005.py
```

## Environment And Method Status

Current shell: `admin1`; no direct `nvidia-smi`, no `CUDA_VISIBLE_DEVICES`, and no `/dev/nvidia*`.

Slurm GPU nodes are available on the cluster, but no mature local insertion-specific structure-prediction workflow was found in PATH/modules during this task. Available relevant modules included CUDA/PyTorch plus general MD/electrostatics tools, but not ColabFold/AlphaFold/OpenFold/ESMFold, Rosetta Remodel/KIC/PyRosetta, FoldX, or a local-frustration pipeline.

Completed methods:

- Panel construction from V5/V2 review evidence.
- WT A89 oligomer-context compatibility using the two existing no-membrane/no-RNA hexamer hypotheses.
- WT residue-contact-network anchor analysis across two AF monomers and two hexamer models.
- Targeted reuse of direct homolog phenotype, functional tier, conservation/indel, Pareto and GPU PLM evidence.
- Cross-method robustness with explicit deferred-method flags.

Deferred methods:

- Insertion-specific structure-prediction ensembles: `DEFERRED_SOFTWARE`.
- Mature loop/backbone remodeling: primary method `DEFERRED_SOFTWARE`; WT anchor loop proxy completed.
- Local energetic/frustration analysis: `DEFERRED_SOFTWARE`.

No inserted 3D structures, Rosetta/FoldX energies, or WT-vs-tagged contact-map deltas were fabricated.

## Integrated Result

Integrated class counts across 132 constructs:

| Class | Count |
|---|---:|
| `PLM_SUPPORTED_BUT_DIRECT_OR_FUNCTIONAL_CONFLICT` | 50 |
| `STRUCTURALLY_DISFAVORED_OR_CONTEXT_CONSTRAINED` | 44 |
| `TAG_SPECIFIC_DISAGREEMENT` | 12 |
| `METHOD_INCONCLUSIVE` | 10 |
| `NEGATIVE_CONTROL` | 8 |
| `METHOD_INCONCLUSIVE_MAPPING_UNCERTAIN` | 4 |
| `RELATIVELY_LOWER_PERTURBATION__DIRECT_EVIDENCE_CONFLICT` | 4 |

Lowest relative perturbation by completed non-fabricated layers:

| Construct | Junction | Tag | Main caveat |
|---|---|---|---|
| `A89_2C_289_290_MAP8` | `289|290` | MAP8 | direct homolog insertion evidence remains unfavorable |
| `A89_2C_289_290_G196_minimal` | `289|290` | G196_minimal | direct homolog insertion evidence remains unfavorable |
| `A89_2C_290_291_MAP8` | `290|291` | MAP8 | direct homolog insertion evidence remains unfavorable |
| `A89_2C_290_291_G196_minimal` | `290|291` | G196_minimal | direct homolog insertion evidence remains unfavorable |

These are not validated or safe sites. They are the least adverse among completed WT-anchor, hexamer-context, network and PLM layers, while still carrying direct homolog conflict and lacking inserted-structure ensembles.

## Required Junction Re-Audit

- `203|204`: all four tags are `STRUCTURALLY_DISFAVORED_OR_CONTEXT_CONSTRAINED`; PLM is low and WT anchor context is constrained.
- `224|225`: all four tags are `STRUCTURALLY_DISFAVORED_OR_CONTEXT_CONSTRAINED`; PLM is low and WT anchor context is constrained.
- `248|249`: all four tags are structurally/context constrained despite moderate PLM for some tags; remains a conflict control, not a low-perturbation row.
- `256|257`: all four tags are structurally/context constrained despite high PLM for MAP8/HA/G196_minimal; oligomer/contact context is the dominant penalty.
- `287|288`: mixed/inconclusive for MAP8/G196 forms; HA has PLM support but remains direct/functional conflict.
- `288|289`: similar to `287|288`; no robust low-perturbation consensus.
- `289|290`: MAP8 and G196_minimal are the strongest completed-layer rows; HA/G196_practical_GS are more method-dependent.
- `290|291`: MAP8 and G196_minimal are the strongest completed-layer rows; HA/G196_practical_GS are method-inconclusive.

## Tag Effects

G196_minimal is not consistently less disruptive than MAP8/HA across the whole panel.

Panel PLM percentile means:

| Tag | Mean PLM percentile |
|---|---:|
| MAP8 | 0.7145 |
| HA | 0.6883 |
| G196_minimal | 0.6785 |
| G196_practical_GS | 0.6440 |

Low relative perturbation class counts:

- MAP8: 2
- G196_minimal: 2
- HA: 0
- G196_practical_GS: 0

G196_minimal helps specifically at `289|290` and `290|291`, but the flanked practical G196 form is not favored by this panel.

## Oligomer And Network Interpretation

Oligomer-context analysis materially changes interpretation for `248|249` and `256|257`: both remain historical/modern conflict controls, but the WT hexamer and contact-network context make them structurally constrained rather than low-perturbation constructs.

The old `287|288-290|291` region remains useful as a conflict-control cluster. Within it, `289|290` and `290|291` are the only rows with multi-layer relative support in this task.

## Method Dependence And Remaining Uncertainty

Conclusions are method-dependent because the primary insertion-specific structure ensemble, mature loop remodeling and energy/frustration modules were deferred by software availability. Completed analyses are still useful for ranking WT-anchor and oligomer-context constraints, but they cannot replace inserted-construct predictions or direct phenotype.

Remaining uncertainty is dominated by two factors:

1. lack of HRV-A89-specific insertion phenotype;
2. absence of mature inserted-construct structural ensembles in this run.

The first factor is still the higher scientific limitation. Computation cannot validate a site without HRV-A89 experimental evidence.

## Final State

`TAG_SITE_MODELING_PARTIALLY_COMPLETE`

Stop here for ChatGPT/user review. Do not start long MD, final construct design, RNA/codon design, or experimental protocol design from this report alone.
