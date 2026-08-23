# Analysis Index

Last updated: 2026-08-23

This file is the navigation layer for the project. Read `PROJECT_STATE.md` first.

## Current authoritative files

| Topic | Current file | Status | Use |
|---|---|---|---|
| Overall project state | `PROJECT_STATE.md` | CURRENT | authoritative checkpoint and current branch/task |
| Final candidate-panel strategy | `docs/FINAL_CANDIDATE_PANEL_STRATEGY_V1.md` | **CURRENT STRATEGIC** | defines the final multi-junction × multi-tag experimental-panel goal and missing evidence layers |
| Current execution task | `tasks/CANDIDATE_PANEL_EXPANSION_008.md` | **COMPLETE** | broadened sites, tags and evidence; final state `READY_FOR_BROAD_TARGETED_DYNAMICS` |
| Active task pointer | `ACTIVE_TASK.md` | CURRENT | current task/stop gate for Codex and ChatGPT |
| Open structure pipeline report | `docs/OPEN_STRUCTURE_PIPELINE_007_REPORT.md` | CURRENT COMPLETED REPORT | real inserted ColabFold/OpenMM/hexamer/contact-network evidence; final state `READY_FOR_TARGETED_DYNAMIC_ANALYSIS` at that checkpoint |
| Open structure integrated perturbation | `data/tag_site_integrated_perturbation_v3_open.tsv` | CURRENT STRUCTURE DATA | 40 construct-level inserted-structure evidence rows |
| Open structure robustness | `results/open_structure_007/cross_method_robustness_v3.tsv` | CURRENT STRUCTURE DATA | identifies four multi-model constructs versus single-model rows |
| GPU PLM integrated matrix | `data/candidate_junctions_v5_plm_gpu.tsv` | CURRENT ALL-320 DATA | all-320 V5 matrix with tag-specific PLM context |
| Computational review set | `data/computational_review_set_v2_plm_gpu.tsv` | CURRENT REVIEW SET | 33-row conflict-aware review set; not final construct selection |
| EV-A71 direct InDel mapping | `docs/EV71_2C_DIRECT_INDEL_MAPPING_V1.md`, `data/evA71_2C_direct_indel_to_A89_v1.tsv` | CURRENT HIGH-WEIGHT EVIDENCE | direct homolog insertion/deletion/substitution context across all A89 junctions |
| Functional exclusion/constraint map | `docs/2C_FUNCTIONAL_EXCLUSION_MAP_V3.md` | CURRENT | A89-specific functional map |
| Four-structure WT structural screen | `docs/STRUCTURAL_SCREEN_V2.md`, `data/junction_structural_metrics_v2.tsv` | CURRENT | all-320 structural context |
| HRV-A conservation / indel tolerance | `docs/CONSERVATION_SCREEN_V2.md`, `data/hrvA_conservation_per_junction_v2.tsv` | CURRENT | near-HRV evolutionary evidence |
| Phylogeny-aware indels | `docs/PHYLOGENY_AWARE_INDEL_V1.md`, `data/hrvA_independent_indel_events_v1.tsv` | CURRENT | independent event lower-bound evidence |
| Tag-specific PLM | `docs/TAG_SPECIFIC_PLM_SCAN_V2_GPU.md`, `data/tag_specific_plm_scores_v2_gpu.tsv` | CURRENT | MAP8/HA/G196 sequence-context evidence |
| Tag consensus | `docs/TAG_SPECIFIC_CONSENSUS_V2_GPU.md`, `data/tag_specific_consensus_v2_gpu.tsv` | CURRENT | cross-tag PLM agreement/disagreement |
| Current tag-site modeling provenance | `docs/CONTINUOUS_TAG_SITE_MODELING_005_REPORT.md` | SUPPORTING | pre-open-structure tag-site context and deferred-method provenance |
| Literature evidence registry | `references/LITERATURE_EVIDENCE_REGISTRY.md` | CURRENT / TO BE EXPANDED IN 008 | source-to-claim map and evidence boundaries |
| Candidate panel 008 report | `docs/CANDIDATE_PANEL_EXPANSION_008_REPORT.md` | CURRENT REPORT | broad candidate-panel expansion and final state `READY_FOR_BROAD_TARGETED_DYNAMICS` |
| Final candidate panel draft | `data/final_candidate_panel_draft_v1.tsv` | CURRENT PANEL | 8 Tier A, 8 Tier B and 2 controls for review |
| Proposed broad dynamics panel | `data/proposed_targeted_dynamics_panel_v1.tsv` | CURRENT PROPOSAL | 9-construct broad targeted-dynamics proposal; not executed |
| Reference sequence | `references/HRV_A89_2C_reference_sequence.fasta` | CURRENT INPUT | authoritative 321-aa A89 2C sequence |
| Project decisions | `DECISIONS.md` | CURRENT | active decisions through candidate-panel strategy |
| Next work | `TODO.md` | CURRENT | prioritized executable backlog |

## Candidate-panel 008 planned outputs

| Output | Purpose |
|---|---|
| `data/junction_feature_matrix_v6_candidate_panel.tsv` | complete all-320 insertion-prior features |
| `data/hrvA89_2C_RNA_holoenzyme_mapping_v1.tsv` | map A89 junctions to 2026 2C:RNA holoenzyme context |
| `docs/RNA_HOLOENZYME_MAPPING_V1.md` | interpretation and mapping limitations |
| `data/tag_boundary_protease_risk_v1.tsv` | cryptic protease/polyprotein boundary-risk annotations |
| `data/tag_portfolio_v2.tsv` | realistic tag portfolio with sequence/reagent/readout status |
| `docs/TAG_PORTFOLIO_V2.md` | tag-level literature and experimental-feasibility review |
| `data/tag_binder_accessibility_v1.tsv` | distinguish epitope detectability from 2C structural tolerance |
| `docs/TAG_BINDER_ACCESSIBILITY_V1.md` | binder-geometry rationale and limitations |
| `data/expanded_structure_replication_panel_v1.tsv` | diverse multi-seed structural replication panel |
| `data/expanded_structure_replication_metrics_v1.tsv` | broader replicate-aware inserted-structure results |
| `data/local_multimer_tag_context_v1.tsv` | local dimer/trimer accommodation where tractable |
| `data/candidate_panel_preliminary_v1.tsv` | multi-objective preliminary site × tag ranking |
| `results/candidate_panel_008/ranking_robustness_v1.tsv` | leave-one-layer-out / rank-stability checks |
| `data/proposed_targeted_dynamics_panel_v1.tsv` | broad multi-site/multi-tag dynamics proposal; not auto-executed |
| `data/final_candidate_panel_draft_v1.tsv` | Tier A / Tier B / control draft |
| `docs/CANDIDATE_PANEL_EXPANSION_008_REPORT.md` | final synthesis for task 008 |

## Key branch provenance

Completed conservation/open-structure checkpoint:

`analysis/conservation-002`

Current candidate-panel branch:

`analysis/candidate-panel-008`

`analysis/candidate-panel-008` was branched from `analysis/conservation-002` after OPEN_STRUCTURE_PIPELINE_007 completion. The older branch remains a stable checkpoint and should not be rewritten for new candidate-panel development.

## Current analysis funnel

```text
4-structure input audit                         COMPLETE
        ↓
2C literature/function mapping                  COMPLETE
        ↓
320-junction WT structural metrics              COMPLETE
        ↓
HRV-A conservation + natural indels             COMPLETE
        ↓
EV-A71 direct 2C InDel fitness → A89            COMPLETE
        ↓
all-320 method hardening + Pareto                COMPLETE
        ↓
tag-specific PLM recovery                       COMPLETE
        ↓
open inserted-structure pipeline                COMPLETE
  ├─ ColabFold WT + inserted constructs
  ├─ OpenMM geometry QC
  ├─ tagged hexamer context
  ├─ tagged contact networks
  └─ 4 constructs deep replicated
        ↓
CANDIDATE_PANEL_EXPANSION_008                    COMPLETE
  ├─ literature/evidence-gap expansion
  ├─ full-320 insertion-prior feature completion
  ├─ 2026 2C:RNA holoenzyme mapping
  ├─ protease/polyprotein boundary-risk scan
  ├─ broader realistic tag portfolio
  ├─ binder-accessibility / epitope-geometry layer
  ├─ broader multi-seed structure replication
  ├─ local dimer/trimer accommodation deferred with status record
  ├─ multi-objective candidate ranking + robustness
  └─ draft Tier A / Tier B / control panel
        ↓
ChatGPT/user review gate
        ↓
broad targeted replicated dynamics              PENDING AUTHORIZATION
        ↓
exact experimental nucleotide/RNA audit          INPUT REQUIRED
        ↓
final wet-lab candidate panel                    PENDING
        ↓
HRV-A89-specific experimental validation         GOLD STANDARD
```

## Current checkpoint interpretation

OPEN_STRUCTURE_PIPELINE_007 resolved the inserted-structure blocker, and CANDIDATE_PANEL_EXPANSION_008 broadened the candidate set beyond one or two sites.

Current Tier A draft spans 6 junctions and 3 tag systems. `289|290 × MAP8/G196_minimal` remain important, but they are members of a broader candidate universe rather than final winners.

The candidate-panel stage must deliberately recover diversity across:

- junctions;
- tag identities;
- evidence classes;
- structural contexts;
- direct/historical conflict types;
- detectability strategies.

The eventual experimental panel should prioritize robustness and information gain, not only the top value from any single computational metric.
