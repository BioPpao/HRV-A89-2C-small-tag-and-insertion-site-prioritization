# Analysis Index

Last updated: 2026-08-24

Read `PROJECT_STATE.md` first.

## Current authoritative files

| Topic | Current file | Status | Use |
|---|---|---|---|
| Overall project state | `PROJECT_STATE.md` | CURRENT | authoritative branch/task checkpoint |
| Current execution task | `tasks/BROAD_DYNAMICS_AND_RECOVERY_009.md` | **PARTIAL CHECKPOINT / CURRENT** | 009 recovery outputs and balanced panel exist; replicated MD remains pending |
| Active task pointer | `ACTIVE_TASK.md` | CURRENT | current Codex/ChatGPT task gate |
| Final candidate-panel strategy | `docs/FINAL_CANDIDATE_PANEL_STRATEGY_V1.md` | CURRENT STRATEGIC | diversified multi-junction × multi-tag final goal |
| Candidate-panel 008 report | `docs/CANDIDATE_PANEL_EXPANSION_008_REPORT.md` | CURRENT COMPLETED CHECKPOINT | 008 results and limitations |
| Candidate-panel draft V1 | `data/final_candidate_panel_draft_v1.tsv` | CURRENT PRE-DYNAMICS PANEL | 8 Tier A, 8 Tier B, 2 controls before dynamics |
| Proposed dynamics V1 | `data/proposed_targeted_dynamics_panel_v1.tsv` | SUPERSEDED AS EXECUTION PANEL | starting point only; 009 must rebalance site/tag bias before MD |
| Broad dynamics 009 report | `docs/BROAD_DYNAMICS_AND_RECOVERY_009_REPORT.md` | CURRENT PARTIAL | OpenMM NaN audit, disorder fallback, balanced panel, GROMACS preproduction complete, production MD running/queued |
| Broad dynamics 009 run log | `docs/BROAD_DYNAMICS_AND_RECOVERY_009_RUN_LOG.md` | CURRENT PARTIAL | execution record, Slurm job IDs and resume commands |
| Balanced dynamics panel V2 | `data/balanced_targeted_dynamics_panel_v2.tsv` | CURRENT PRE-MD PANEL | 12 tagged systems plus WT system manifest; not dynamics-informed yet |
| Final panel V2 dynamics | `data/final_candidate_panel_v2_dynamics.tsv` | PLACEHOLDER / NOT DYNAMICS-INFORMED | preserves explicit `not_completed` dynamics status |
| Ranking robustness V1 | `results/candidate_panel_008/ranking_robustness_v1.tsv` | CURRENT PRE-DYNAMICS ROBUSTNESS | multi-objective/leave-layer-out context |
| Expanded structure replication | `data/expanded_structure_replication_metrics_v1.tsv` | CURRENT PRE-DYNAMICS STRUCTURE DATA | 18 constructs, expanded multi-seed ColabFold/OpenMM evidence |
| Local multimer V1 | `data/local_multimer_tag_context_v1.tsv` | DEFERRED PROVENANCE | rigid-context status; local dimer/trimer prediction not run in 008 |
| Tag portfolio | `data/tag_portfolio_v2.tsv`, `docs/TAG_PORTFOLIO_V2.md` | CURRENT | core and exploratory tag systems |
| Binder accessibility | `data/tag_binder_accessibility_v1.tsv`, `docs/TAG_BINDER_ACCESSIBILITY_V1.md` | CURRENT PROXY | detectability geometry proxy, no mature binder docking |
| RNA holoenzyme mapping | `data/hrvA89_2C_RNA_holoenzyme_mapping_v1.tsv`, `docs/RNA_HOLOENZYME_MAPPING_V1.md` | CURRENT SUPPORTING | residue-neighborhood RNA/pore context from homolog/preprint evidence |
| Open structure pipeline | `docs/OPEN_STRUCTURE_PIPELINE_007_REPORT.md`, `data/tag_site_integrated_perturbation_v3_open.tsv` | CURRENT STRUCTURE CHECKPOINT | real inserted structures, OpenMM QC, rigid hexamer and contact-network evidence |
| All-320 PLM matrix | `data/candidate_junctions_v5_plm_gpu.tsv` | CURRENT ALL-320 DATA | tag-specific ESM2 context |
| Direct EV-A71 InDel evidence | `docs/EV71_2C_DIRECT_INDEL_MAPPING_V1.md`, `data/evA71_2C_direct_indel_to_A89_v1.tsv` | CURRENT HIGH-WEIGHT EVIDENCE | homolog direct insertion/deletion/substitution phenotype |
| Functional map | `docs/2C_FUNCTIONAL_EXCLUSION_MAP_V3.md` | CURRENT | hard/graded biological constraints |
| Conservation/indel | `docs/CONSERVATION_SCREEN_V2.md`, `data/hrvA_conservation_per_junction_v2.tsv`, `data/hrvA_independent_indel_events_v1.tsv` | CURRENT | near-HRV evolutionary evidence |
| Literature evidence registry | `references/LITERATURE_EVIDENCE_REGISTRY.md` | CURRENT | source-to-claim provenance |
| Project decisions | `DECISIONS.md` | CURRENT | active interpretation rules |
| Next work | `TODO.md` | CURRENT | executable backlog |

## Branch provenance

Stable completed checkpoint:

`analysis/conservation-002`

Candidate-panel checkpoint:

`analysis/candidate-panel-008`

Current recovery/dynamics branch:

`analysis/broad-dynamics-009`

Branch chain:

```text
analysis/conservation-002
        ↓
analysis/candidate-panel-008
        ↓
analysis/broad-dynamics-009
```

Do not rewrite the older branch checkpoints for new 009 results.

## Current analysis funnel

```text
functional + WT structural + conservation evidence       COMPLETE
        ↓
EV-A71 direct insertion/deletion mapping                  COMPLETE
        ↓
all-320 hardening + Pareto + PLM                          COMPLETE
        ↓
OPEN_STRUCTURE_PIPELINE_007                               COMPLETE
  ├─ real inserted ColabFold models
  ├─ OpenMM geometry QC
  ├─ rigid tagged-hexamer context
  └─ contact-network analysis
        ↓
CANDIDATE_PANEL_EXPANSION_008                             COMPLETE
  ├─ full-320 feature integration
  ├─ RNA-holoenzyme mapping
  ├─ protease boundary-risk scan
  ├─ tag portfolio and binder-accessibility proxy
  ├─ 18-construct expanded structural replication
  └─ diversified draft panel
        ↓
BROAD_DYNAMICS_AND_RECOVERY_009                           PARTIAL CHECKPOINT
  ├─ resolve 248|249×HA OpenMM NaN                  COMPLETE
  ├─ recover disorder layer                          PARTIAL / fallback
  ├─ run local tagged dimer/trimer accommodation      RUNNING under Slurm
  ├─ focused PA14/AGIA structure screen               COMPLETE / low confidence
  ├─ rebalance site/tag dynamics panel                COMPLETE pre-MD
  ├─ replicated comparative MD on A89 2C 112–321      PREPRODUCTION COMPLETE / PRODUCTION RUNNING OR QUEUED
  ├─ tag exposure/contact/convergence analysis        PENDING
  ├─ dynamic correlation/network analysis             PENDING
  └─ revise Tier A / Tier B / controls                PLACEHOLDER only
        ↓
final candidate-panel review                              PENDING
        ↓
exact experimental nucleotide/RNA audit                   INPUT REQUIRED
        ↓
final wet-lab construct set                               PENDING
        ↓
HRV-A89-specific experimental validation                  GOLD STANDARD
```

## Important current interpretation

The 008 draft should not be read as eight independent Tier A biological regions. Six of eight Tier A constructs came from the contiguous `287–291` C-terminal neighborhood. Task 009 explicitly performs site-region and tag-family diversity correction before dynamics.

Broad dynamics is a comparative perturbation layer, not a complete native-state simulation. The primary 009 screen uses A89 native residues `112–321` with consistent treatment across WT and tagged systems to avoid bulk-water artifacts from the membrane-associated N terminus.
