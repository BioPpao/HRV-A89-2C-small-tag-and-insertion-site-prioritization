# 9A5_CONTEXT_QC_011A

Status: `TASK011A_COMPLETE_WAITING_FOR_CHATGPT_REVIEW`

Date: `2026-09-02`

Branch: `analysis/9a5-context-qc-011a`

## Scope

Task 011A hardens the already completed 9A5 context layer. It performs no new MD, no AlphaFold/ColabFold, no docking, no Slurm/GPU work, no membrane/RNA/ATP mechanism simulation, and no final experimental construct design.

## Endpoint Duplicate Resolution

The three packaged 1x9A5 weak-posres endpoint PDBs were byte-identical and are now treated as provenance only. The underlying XTC/TPR/GRO/log files are SHA-distinct; final frames were re-exported from the existing `*_pbc_cluster_center.xtc` trajectories with an explicit `u.trajectory[-1]` call.

Old packaged endpoint unique SHA count: `1`

Corrected re-exported endpoint unique SHA count: `3`

| repeat | old PDB SHA | corrected PDB SHA | RMSD old-vs-corrected A | RMSD corrected-vs-rep1 A | source trajectory status |
|---|---:|---:|---:|---:|---|
| rep1 | `3c0083aa7091` | `d0478a7a5168` | 1.389 | 0.000 | underlying_xtc_tpr_gro_log_sha256_unique |
| rep2 | `3c0083aa7091` | `935684cc8c80` | 1.315 | 1.156 | underlying_xtc_tpr_gro_log_sha256_unique |
| rep3 | `3c0083aa7091` | `5188d4f8df2e` | 1.424 | 1.111 | underlying_xtc_tpr_gro_log_sha256_unique |

Interpretation: the duplicated PDB endpoints came from an endpoint export problem, not from identical trajectories. The likely cause is that the source repeat analysis script wrote `u.atoms` after iterating through the trajectory without explicitly seeking the final frame. Corrected 011A analysis uses the re-exported final frames and does not count byte-identical endpoint PDBs as independent.

## 248|249 HA Robustness

Robustness class: `ROBUST_HEXAMER_CROWDING`

Class note: `3/3_unique_HA_conformations_show_lt2p5_protomer_crowding`

Minimum HA tag-other-protomer distance across audited conformations: `0.061 A`

Minimum MAP8 tag-other-protomer distance at the same junction: `0.199 A`

| HA model SHA | rows | min other-protomer A | max <2.5A clash count | model files |
|---|---:|---:|---:|---|
| `6971c42204b9` | 9 | 0.191 | 213 | `results/candidate_panel_008/expanded_colabfold/A89_2C_248_249_HA_unrelaxed_rank_002_alphafold2_ptm_model_1_seed_031.pdb` |
| `c9aedd61dd46` | 9 | 0.061 | 211 | `results/open_structure_007/tier1_shallow/A89_2C_248_249_HA_unrelaxed_rank_001_alphafold2_ptm_model_1_seed_011.pdb` |
| `db1c19ccadcd` | 9 | 0.202 | 214 | `results/candidate_panel_008/expanded_colabfold/A89_2C_248_249_HA_unrelaxed_rank_001_alphafold2_ptm_model_1_seed_032.pdb` |


| MAP8 model SHA | rows | min other-protomer A | max <2.5A clash count | model files |
|---|---:|---:|---:|---|
| `8bf0a4380789` | 9 | 2.005 | 1 | `results/open_structure_007/tier1_shallow/A89_2C_248_249_MAP8_unrelaxed_rank_001_alphafold2_ptm_model_1_seed_011.pdb` |
| `c321bd76bade` | 9 | 0.199 | 105 | `results/candidate_panel_008/expanded_colabfold/A89_2C_248_249_MAP8_unrelaxed_rank_002_alphafold2_ptm_model_1_seed_031.pdb` |
| `df858a2641e2` | 9 | 3.725 | 0 | `results/candidate_panel_008/expanded_colabfold/A89_2C_248_249_MAP8_unrelaxed_rank_001_alphafold2_ptm_model_1_seed_032.pdb` |

Interpretation: 248|249 remains a biologically important non-C-terminal region, but tag identity matters. The HA form is retained for experimental-review discussion with a hardened hexamer-crowding caution. MAP8 is less persistently crowded than HA at the model level, although one MAP8 conformation also shows a rigid-transfer clash, so this is a relative tag-identity comparison rather than a safe/validated claim.

## V7 Experimental Review Panel

| order | construct | V7 priority | transition |
|---:|---|---|---|
| 1 | `A89_2C_289_290_MAP8` | `Priority_A` | V6 retained after duplicate endpoint correction |
| 2 | `A89_2C_289_290_G196_minimal` | `Priority_A` | V6 retained after duplicate endpoint correction |
| 3 | `A89_2C_248_249_MAP8` | `Priority_A` | retained as 248|249 tag-identity comparator; MAP8 is less persistently crowded than HA, but one MAP8 conformation also shows a rigid-transfer clash |
| 4 | `A89_2C_248_249_HA` | `Priority_A_with_QC_hardened_hexamer_crowding_caution` | retained for experimental discussion but ordered after 248|249 MAP8 because HA protomer crowding persists across independent existing conformations |
| 5 | `A89_2C_288_289_MAP8` | `Priority_B` | V6 retained after duplicate endpoint correction |
| 6 | `A89_2C_290_291_MAP8` | `Priority_B` | V6 retained after duplicate endpoint correction |
| 7 | `A89_2C_288_289_HA` | `Priority_B` | V6 retained after duplicate endpoint correction |
| 8 | `A89_2C_256_257_MAP8` | `Conflict_control` | V6 retained after duplicate endpoint correction |
| 9 | `A89_2C_224_225_MAP8` | `Conflict_control` | conflict control retained for non-C-terminal comparator |
| 10 | `A89_2C_224_225_HA` | `Conflict_control` | conflict/control-like HA comparator retained |
| 11 | `A89_2C_203_204_G196_minimal` | `Conflict_control` | G196 conflict control retained |
| 12 | `A89_2C_155_156_MAP8` | `Hard_negative_control` | hard-negative control retained; sequence-defined 9A5 epitope overlap is expected |

Final ordering for discussion: `289|290 x MAP8`, `289|290 x G196_minimal`, `248|249 x MAP8`, `248|249 x HA`, then secondary/context-control rows. This does not call any site safe or validated.

## Required Outputs

- `data/9a5_context_input_provenance_v2_qc.tsv`
- `data/9a5_context_structure_inventory_v2_qc.tsv`
- `data/9a5_hexamer_tag_compatibility_v2_qc.tsv`
- `data/9a5_context_ensemble_summary_v2_qc.tsv`
- `data/248_249_HA_hexamer_robustness_v1.tsv`
- `data/junction_feature_matrix_v8_9a5_epitope_qc.tsv`
- `data/final_candidate_panel_v7_9a5_context_qc.tsv`
- `figures/9a5_context_011a_qc/`
- `results/9a5_context_011a_qc/endpoint_reexport_qc_v1.tsv`
- `results/9a5_context_011a_qc/reexported_1x9A5_endpoints/`

## Branch Relationship

```text
* 5a42628 (HEAD -> analysis/9a5-context-qc-011a, origin/analysis/9a5-context-qc-011a) task011a: define QC worklist
* 6e21c83 task011a: activate 9A5 context QC
* 52ce9f9 task011a: add 9A5 context QC hardening task
* 8e84356 (origin/analysis/9a5-monomer-hexamer-context-011, analysis/9a5-monomer-hexamer-context-011) task011: integrate 9A5 context layer
| * ed42d10 (origin/analysis/experimental-review-cleanup-010a) Refine Figure 5 structural landscape by tag
| * 18cad42 Refine Figure 5 focal comparison bars and repeat display
| * ba05ef9 figure: render Figure 4 tag-specific PLM landscape [skip ci]
| * 8d97c6d fix: use Arial-first SVG font stack without forced spacing
| * e3d09cf fix: normalize Figure 4 typography and SVG word spacing
| * 96809fa Recolor_Figure06_to_orange_teal_purple_palette
| * 2b27ec7 Add_Figure06_replicated_MD_landscape
| * c0feaad Revise Figure 5 readability and focal comparison
| * 4b94fbe Add Figure 5 insertion-structure perturbation landscape
| * b8426cf figure: render Figure 4 tag-specific PLM landscape [skip ci]
| * a30377d fix: remove connector warning from Figure 4 R source
| * 67319c2 figure: add tag-specific PLM landscape and reproducible R workflow
| * c8872d6 report: clarify archived HTML portability requirement
| * de5f539 report: register integrated HTML report archive
| * 018d571 report: archive self-contained interactive HTML
| * 076d0c5 report: add report provenance and data-boundary record
| * b48160b report: archive detailed tag selection rationale
| * 67c9a0f report: add integrated scientific synthesis
| * 653dab5 report: add current computational results report archive index
|/  
* ffa8475 (analysis/experimental-review-cleanup-010a) task010a: finalize experimental review shortlist
* 7527ca8 task010a: update analysis index
* 0588310 task010a: update cleanup TODO
* 2e22ac4 task010a: update project state for cleanup
* d81c3af task010a: activate final scientific cleanup
* 2dfa9b1 task010a: add Codex cleanup prompt
* 1f6e182 task010a: add scientific cleanup analysis
```

## Stop Gate

`READY_FOR_EXPERIMENTAL_REVIEW_WITH_9A5_QC_HARDENED_V7`
