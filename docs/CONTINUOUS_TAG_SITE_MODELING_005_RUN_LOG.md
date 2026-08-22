# CONTINUOUS_TAG_SITE_MODELING_005_RUN_LOG

Task: `CONTINUOUS_TAG_SITE_MODELING_005`

Branch: `analysis/conservation-002`

Date: 2026-08-22

## Starting State

- Repository branch matched required branch.
- `git fetch origin` completed.
- Local branch was synchronized with `origin/analysis/conservation-002` before analysis.
- Active task pointer: `ACTIVE_TASK.md`.
- Upstream inputs reused without rerunning global all-320 discovery:
  - `data/candidate_junctions_v5_plm_gpu.tsv`
  - `data/computational_review_set_v2_plm_gpu.tsv`
  - `data/tag_specific_plm_scores_v2_gpu.tsv`

## Required Files Read

- `WORKFLOW.md`
- `AGENTS.md`
- `PROJECT_STATE.md`
- `ACTIVE_TASK.md`
- `tasks/CONTINUOUS_TAG_SITE_MODELING_005.md`
- `docs/GPU_RECOVERY_004_REPORT.md`
- `data/candidate_junctions_v5_plm_gpu.tsv`
- `data/computational_review_set_v2_plm_gpu.tsv`
- `DECISIONS.md`
- `ANALYSIS_INDEX.md`
- `TODO.md`
- `INPUT_PROVENANCE.md`
- `references/LITERATURE_EVIDENCE_REGISTRY.md`

## Runtime And Inputs

Execution host: `admin1`

Analysis Python:

```bash
.tools/envs/hrv2c-one-shot/bin/python3.11
```

Structure inputs were located at:

- `/public/home/yukang/HRV Oligomers/hrv_2c_full/fold_hrv_2c_full_model_1.cif`
- `/public/home/yukang/HRV Oligomers/hrv_2c_full/fold_hrv_2c_full_model_3.cif`
- `/public/home/yukang/HRV Oligomers/HRV_A89_2C_HEXAMER/results_summary/selected_hexamer_01_md_representative.pdb`
- `/public/home/yukang/HRV Oligomers/HRV_A89_2C_HEXAMER/results_summary/selected_hexamer_02_md_representative.pdb`

Checksums matched `INPUT_PROVENANCE.md` for all four structures.

## GPU And Software Audit

Current shell GPU checks:

- hostname: `admin1`
- `nvidia-smi`: not found
- `CUDA_VISIBLE_DEVICES`: empty
- `/dev/nvidia*`: absent

Slurm GPU nodes were visible via `sinfo`, including A40 and RTX3090 nodes.

Mature method availability:

- ColabFold/AlphaFold/OpenFold/ESMFold executable: not found.
- Rosetta Remodel/KIC/PyRosetta executable: not found.
- FoldX/local-frustration workflow: not found.
- CUDA/PyTorch modules exist on the cluster, but this did not provide a mature insertion-specific structure-prediction or loop-remodeling workflow.

## Computation

Command:

```bash
.tools/envs/hrv2c-one-shot/bin/python3.11 scripts/continuous_tag_site_modeling_005.py
```

Generated:

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

## QC

- V5 matrix rows: 320.
- V2 review junctions: 33.
- Tag forms: 4.
- Modeled panel constructs: 132.
- Each required re-audit junction has 4 tag-form rows.
- Output row count for each construct-level table: 132 data rows plus header.

During QC, an initial string-suffix classification issue was found: `UNFAVORABLE` also matched `endswith("FAVORABLE")`. The script was corrected to exact class matching and all outputs were regenerated.

## Method Status

- Insertion-specific structure-prediction ensembles: `DEFERRED_SOFTWARE`.
- Mature loop/backbone remodeling: `DEFERRED_SOFTWARE`; WT-anchor loop proxy completed.
- Local energetic/frustration analysis: `DEFERRED_SOFTWARE`.
- Oligomer-context compatibility: completed as WT hexamer-context proxy.
- Residue-contact-network perturbation: completed as WT anchor network; tagged delta deferred.
- Targeted evolutionary/statistical checks: completed by V5/V2 reuse for panel.
- Cross-method robustness: completed with explicit deferred-method flags.

## Final Result

Final decision state:

`TAG_SITE_MODELING_PARTIALLY_COMPLETE`

No site was called safe or experimentally validated.
