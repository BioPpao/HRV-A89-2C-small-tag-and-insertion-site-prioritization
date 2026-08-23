# TODO

Last updated: 2026-08-23

Priority order is scientific, not cosmetic.

## OPEN_STRUCTURE_PIPELINE_007 — COMPLETE

Status: **READY_FOR_TARGETED_DYNAMIC_ANALYSIS**

Primary report:

- `docs/OPEN_STRUCTURE_PIPELINE_007_REPORT.md`

Current authoritative open-structure outputs include:

- `data/tag_site_integrated_perturbation_v3_open.tsv`
- `results/open_structure_007/cross_method_robustness_v3.tsv`

This result is retained, but targeted dynamics is no longer treated as the only next step.

## CANDIDATE_PANEL_EXPANSION_008 — COMPLETE

Status: **READY_FOR_BROAD_TARGETED_DYNAMICS**

Branch:

`analysis/candidate-panel-008`

Task:

- `tasks/CANDIDATE_PANEL_EXPANSION_008.md`

Strategy:

- `docs/FINAL_CANDIDATE_PANEL_STRATEGY_V1.md`

### Final objective

Build a ranked, redundant, multi-junction × multi-tag candidate panel for later wet-lab validation rather than selecting one or two computational winners.

### Completed work

1. update literature/evidence registry for insertion tolerance and tag engineering;
2. complete full-320 secondary-structure boundary, rSASA, disorder/flexibility and structural-prior features;
3. map A89 junctions to the 2026 picornaviral 2C:RNA holoenzyme evidence;
4. add tag-boundary protease/polyprotein risk annotations;
5. review/expand the realistic tag portfolio beyond MAP8/HA/G196 when justified;
6. add tag-binder accessibility and recognition-geometry analysis;
7. broaden multi-seed ColabFold replication beyond the current four deep constructs;
8. record local dimer/trimer accommodation as deferred where not tractable in this run;
9. perform multi-objective preliminary candidate-panel ranking and robustness;
10. define a broader targeted-dynamics panel without executing it;
11. produce a draft final candidate panel with Tier A / Tier B / controls.

### Core tags

- MAP8
- HA
- G196_minimal

Architecture comparison:

- G196_practical_GS

Expansion tags for feasibility review:

- ALFA
- PA12/PA14
- AGIA
- HiBiT if the intended readout is relevant

FLAG remains excluded.

### Expected outputs

- `data/junction_feature_matrix_v6_candidate_panel.tsv`
- `data/hrvA89_2C_RNA_holoenzyme_mapping_v1.tsv`
- `docs/RNA_HOLOENZYME_MAPPING_V1.md`
- `data/tag_boundary_protease_risk_v1.tsv`
- `data/tag_portfolio_v2.tsv`
- `docs/TAG_PORTFOLIO_V2.md`
- `data/tag_binder_accessibility_v1.tsv`
- `docs/TAG_BINDER_ACCESSIBILITY_V1.md`
- `data/expanded_structure_replication_panel_v1.tsv`
- `data/expanded_structure_replication_metrics_v1.tsv`
- `data/local_multimer_tag_context_v1.tsv`
- `data/candidate_panel_preliminary_v1.tsv`
- `results/candidate_panel_008/ranking_robustness_v1.tsv`
- `data/proposed_targeted_dynamics_panel_v1.tsv`
- `data/final_candidate_panel_draft_v1.tsv`
- `docs/CANDIDATE_PANEL_EXPANSION_008_REPORT.md`

All generated. Use `docs/CANDIDATE_PANEL_EXPANSION_008_REPORT.md`, `data/final_candidate_panel_draft_v1.tsv` and `data/proposed_targeted_dynamics_panel_v1.tsv` as the current review package.

### Ranking policy

Do not use one opaque total score.

Use:

- separate evidence axes;
- Pareto/non-dominated membership;
- evidence classes;
- leave-one-layer-out sensitivity;
- rank stability/resampling where meaningful;
- explicit conflict labels.

### Target panel scale

Approximate target:

- Tier A: 6–10 primary constructs;
- Tier B: 6–12 secondary/rescue constructs;
- controls: 4–6 conflict/hard-negative constructs.

The final panel should span multiple junctions and multiple tags.

## Later — broad targeted dynamics

Targeted dynamics is now ready for ChatGPT/user authorization. Use `data/proposed_targeted_dynamics_panel_v1.tsv` as the starting panel; prefer breadth of independent replicas across multiple constructs over one long trajectory.

## Later — exact nucleotide/RNA gate

Mandatory before final construct recommendation. Requires the exact experimental nucleotide construct/context.

## Repository maintenance

Keep `PROJECT_STATE.md`, `ACTIVE_TASK.md`, `ANALYSIS_INDEX.md`, `DECISIONS.md` and this file consistent. Preserve versioned historical outputs and record software/environment versions and commands.
