# 9A5_COMPLEX_CONTEXT_INTEGRATION_V1

## Executive conclusion

The existing 9A5-bound context does not create a decision-changing direct antibody clash for the current 289|290 and 248|249 Priority A candidate logic; the 155|156 hard-negative control is correctly recognized as epitope/antibody-confounded.

Final state: `READY_FOR_EXPERIMENTAL_REVIEW_WITH_9A5_CONTEXT_LAYER`

Methods: existing C01/C04 9A5-core complexes and 1x9A5 full-length hexamer endpoints were reused; tagged ColabFold monomers were aligned by native 2C residues with explicit tag-residue exclusion; all metrics are heavy-atom geometric proxies. No new docking, AlphaFold, Slurm, GPU job, or MD was run.

No construct is safe, compatible, experimentally validated or fitness-neutral.

## Candidate Decision Table

| construct                   | previous_priority     | monomer_9a5_class                    | hexamer_9a5_class                    | hexamer_ensemble_consistency         | new_priority                        | complex_context_decision   |
|:----------------------------|:----------------------|:-------------------------------------|:-------------------------------------|:-------------------------------------|:------------------------------------|:---------------------------|
| A89_2C_289_290_MAP8         | Priority_A            | CONSISTENT_ROBUST_9A5_CONTEXT        | CONSISTENT_ROBUST_9A5_CONTEXT        | CONSISTENT_ROBUST_9A5_CONTEXT        | Priority_A                          | retained                   |
| A89_2C_289_290_G196_minimal | Priority_A            | CONSISTENT_ROBUST_9A5_CONTEXT        | CONSISTENT_ROBUST_9A5_CONTEXT        | CONSISTENT_ROBUST_9A5_CONTEXT        | Priority_A                          | retained                   |
| A89_2C_248_249_HA           | Priority_A            | CONSISTENT_ROBUST_9A5_CONTEXT        | CONSISTENT_HEXAMER_CONTEXT_SENSITIVE | CONSISTENT_HEXAMER_CONTEXT_SENSITIVE | Priority_A_with_9A5_context_caution | retained_with_caution      |
| A89_2C_248_249_MAP8         | Priority_A            | CONSISTENT_ROBUST_9A5_CONTEXT        | CONSISTENT_ROBUST_9A5_CONTEXT        | CONSISTENT_ROBUST_9A5_CONTEXT        | Priority_A                          | retained                   |
| A89_2C_288_289_MAP8         | Priority_B            | CONSISTENT_ROBUST_9A5_CONTEXT        | CONSISTENT_ROBUST_9A5_CONTEXT        | CONSISTENT_ROBUST_9A5_CONTEXT        | Priority_B                          | retained                   |
| A89_2C_288_289_HA           | Priority_B            | CONSISTENT_ROBUST_9A5_CONTEXT        | CONSISTENT_ROBUST_9A5_CONTEXT        | CONSISTENT_ROBUST_9A5_CONTEXT        | Priority_B                          | retained                   |
| A89_2C_290_291_MAP8         | Priority_B            | CONSISTENT_ROBUST_9A5_CONTEXT        | CONSISTENT_ROBUST_9A5_CONTEXT        | CONSISTENT_ROBUST_9A5_CONTEXT        | Priority_B                          | retained                   |
| A89_2C_256_257_MAP8         | Conflict_control      | CONSISTENT_ROBUST_9A5_CONTEXT        | CONSISTENT_HEXAMER_CONTEXT_SENSITIVE | CONSISTENT_HEXAMER_CONTEXT_SENSITIVE | Conflict_control                    | control_retained           |
| A89_2C_224_225_MAP8         | Conflict_control      | CONSISTENT_ROBUST_9A5_CONTEXT        | CONFLICT_ACROSS_STRUCTURES           | CONFLICT_ACROSS_STRUCTURES           | Conflict_control                    | control_retained           |
| A89_2C_224_225_HA           | Conflict_control      | CONSISTENT_ROBUST_9A5_CONTEXT        | CONFLICT_ACROSS_STRUCTURES           | CONFLICT_ACROSS_STRUCTURES           | Conflict_control                    | control_retained           |
| A89_2C_203_204_G196_minimal | Conflict_control      | CONFLICT_ACROSS_STRUCTURES           | CONSISTENT_HEXAMER_CONTEXT_SENSITIVE | CONSISTENT_HEXAMER_CONTEXT_SENSITIVE | Conflict_control                    | control_retained           |
| A89_2C_155_156_MAP8         | Hard_negative_control | CONSISTENT_EPITOPE_PERTURBATION_RISK | CONFLICT_ACROSS_STRUCTURES           | CONFLICT_ACROSS_STRUCTURES           | Hard_negative_control               | control_retained           |

## Direct Answers

- Candidate rows assessed: `12` current V5 Priority A/B/control/hard-negative constructs.
- Priority A retained or retained with 9A5-context caution: `A89_2C_289_290_MAP8; A89_2C_289_290_G196_minimal; A89_2C_248_249_HA; A89_2C_248_249_MAP8`.
- Candidates downgraded by 9A5 context: `none`.
- Priority B rows with cleaner 9A5-context metrics than at least one cautioned Priority A row: `A89_2C_288_289_MAP8; A89_2C_288_289_HA; A89_2C_290_291_MAP8` are cleaner than cautioned Priority A rows in the 9A5-context layer alone, but are not automatically promoted because the project priority hierarchy also includes direct homolog phenotype, functional constraints, diversity logic and prior structure/MD evidence.
- If ordering experimental discussion now, keep the 010A 4+2 design logic: 289|290 x MAP8, 289|290 x G196_minimal, 248|249 x HA, 248|249 x MAP8, with 224|225 x MAP8 and 155|156 x MAP8 as controls. The 9A5 layer adds caution/confirmation context rather than a new safe-site claim.

## Existing Data Reused

- C01/C04 historical 9A5-core complexes from HRV_Oligomers.
- Current full-length 1x9A5 hexamer showcase plus three 1 ns refined endpoints.
- Free hexamer lead/control and 5 ns repeat endpoints.
- Existing Open Structure 007 tagged monomer predictions.
- Existing V5 candidate panel, direct homolog evidence, conservation, PLM, binder-accessibility and MD context fields.

## Inventory Snapshot

- Inventory rows: `31` structures/models.
- Primary usable 1x9A5 hexamer structures: `4`.
- Tagged monomer model structures inventoried: `18`.

## Figures

- `figures/9a5_context_011/figure01_candidate_state_heatmap.svg`
- `figures/9a5_context_011/figure02_monomer_vs_hexamer_paired.svg`
- `figures/9a5_context_011/figure03_tag_9a5_clash_distance.svg`
- `figures/9a5_context_011/figure04_ensemble_reproducibility.svg`
- `figures/9a5_context_011/figure05_priority_transition.svg`
- `figures/9a5_context_011/figure06_representative_structure_projections.svg`

## Limitations

- Structural proxy only; no viral fitness, antibody-detection or replication compatibility is proven.
- C01/C04 monomer/core complexes contain 2C residues 112-258, not full-length 2C.
- C-terminal 289|290 monomer-layer geometry depends on core-based transfer and is less direct than full-length hexamer context.
- Six-tagged homohexamer context is a rigid transfer proxy, not a relaxed tagged homohexamer prediction.
- No membrane, RNA, ATP/Mg mechanistic MD, binder docking, nucleotide/codon design or wet-lab protocol was performed.

No additional generic long MD is required for the current tag-prioritization decision.
