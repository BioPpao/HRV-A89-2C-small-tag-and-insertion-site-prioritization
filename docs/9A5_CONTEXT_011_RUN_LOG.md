# 9A5_CONTEXT_011_RUN_LOG

Task: `9A5_MONOMER_HEXAMER_CONTEXT_011`

Branch: `analysis/9a5-monomer-hexamer-context-011`

Starting target commit: `ffa847557a4bce2461c87e1869f9a45abf05ed4b`
Source HRV_Oligomers commit: `3385e069fa8469253d8776b3adb3361759094faa`

## Required Context Read

- WORKFLOW.md, AGENTS.md, PROJECT_STATE.md, DECISIONS.md, ANALYSIS_INDEX.md, ACTIVE_TASK.md, INPUT_PROVENANCE.md, TODO.md.
- Task 010A parent task/report files and corrected-validation reports.
- User-authorized Task 011 prompt copied to `tasks/9A5_MONOMER_HEXAMER_CONTEXT_011.md`.

## Execution Environment

- Python executable: `/public/home/yukang/wf/HRV-A89-2C-small-tag-and-insertion-site-prioritization/.tools/envs/open_structure_007/bin/python`
- Python version: `3.10.21`
- pandas `1.5.3`; numpy `1.26.4`; scipy `1.15.2`; matplotlib `3.10.9`
- mdtraj import available: `yes`
- Distance searches used `scipy.spatial.cKDTree`.

## Search And Reuse Record

- Searched HRV_Oligomers for 9A5, C01, C04, complex, monomer, Fv/scFv, hexamer, selected, SHOWCASE, endpoint, registry and report assets.
- Searched target repo for 9A5, tagged, monomer, hexamer, candidate, shortlist, structure, provenance, open-structure, binder, PLM, EV71, conservation and dynamics assets.
- Reused existing structures and candidate tables; no new docking, AF/ColabFold, GPU, Slurm or MD job was started.
- Historical untracked Task 009 local multimer outputs were left untouched and not staged.

## Generated Outputs

- `data/9a5_context_structure_inventory_v1.tsv`
- `data/9a5_context_input_provenance_v1.tsv`
- `data/9a5_monomer_tag_compatibility_v1.tsv`
- `data/9a5_hexamer_tag_compatibility_v1.tsv`
- `data/9a5_context_ensemble_summary_v1.tsv`
- `data/final_candidate_panel_v6_9a5_context.tsv`
- `docs/9A5_MONOMER_CONTEXT_V1.md`
- `docs/9A5_HEXAMER_CONTEXT_V1.md`
- `docs/9A5_COMPLEX_CONTEXT_INTEGRATION_V1.md`
- `figures/9a5_context_011/figure01-06.*`

## Result State

`READY_FOR_EXPERIMENTAL_REVIEW_WITH_9A5_CONTEXT_LAYER`
