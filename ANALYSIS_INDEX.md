# Analysis Index

Last updated: 2026-08-24

Read `PROJECT_STATE.md` first.

## Current Authoritative Files

| Topic | Current file | Status | Use |
|---|---|---|---|
| Overall project state | `PROJECT_STATE.md` | CURRENT | authoritative checkpoint |
| Active task pointer | `ACTIVE_TASK.md` | CURRENT | task gate, now waiting for review |
| Broad dynamics 009 report | `docs/BROAD_DYNAMICS_AND_RECOVERY_009_REPORT.md` | CURRENT COMPLETE | primary 009 interpretation |
| Broad dynamics 009 run log | `docs/BROAD_DYNAMICS_AND_RECOVERY_009_RUN_LOG.md` | CURRENT | execution/provenance log |
| Dynamics QC | `docs/DYNAMICS_QC_V1.md` | CURRENT | trajectory QC summary |
| Dynamic network | `docs/DYNAMIC_NETWORK_ANALYSIS_V1.md` | CURRENT | DCCM/contact-network summary |
| Local multimer recovery | `docs/LOCAL_MULTIMER_RECOVERY_V2.md` | CURRENT INCONCLUSIVE | nonfinite local multimer output status |
| Final panel V2 dynamics | `data/final_candidate_panel_v2_dynamics.tsv` | CURRENT REVIEW SET | dynamics-informed candidate/control table |
| Ranking robustness V2 | `results/broad_dynamics_009/ranking_robustness_v2.tsv` | CURRENT REVIEW SET | 20 ns robustness/caution labels |
| Replica QC | `data/dynamics_replica_qc_v1.tsv` | CURRENT REAL TRAJECTORY DATA | 39-replica QC |
| Broad dynamics metrics | `data/broad_dynamics_metrics_v1.tsv` | CURRENT REAL TRAJECTORY DATA | RMSD/RMSF/Rg metrics |
| Tag exposure dynamics | `data/tag_exposure_dynamics_v1.tsv` | CURRENT REAL TRAJECTORY DATA | nonlocal tag-distance proxy |
| Contact persistence | `data/contact_persistence_dynamics_v1.tsv` | CURRENT REAL TRAJECTORY DATA | CA contact retention |
| Dynamic network perturbation | `data/dynamic_network_perturbation_v1.tsv` | CURRENT REAL TRAJECTORY DATA | DCCM/network metrics |
| Production manifest | `results/broad_dynamics_009/production_manifest.tsv` | CURRENT | paths/status/provenance |
| Replica completion | `results/broad_dynamics_009/replica_completion.tsv` | CURRENT | paths/status/provenance |
| Balanced dynamics panel V2 | `data/balanced_targeted_dynamics_panel_v2.tsv` | CURRENT PRE-MD PANEL | frozen panel that was simulated |
| Candidate-panel 008 report | `docs/CANDIDATE_PANEL_EXPANSION_008_REPORT.md` | COMPLETED CHECKPOINT | pre-dynamics candidate-panel context |
| Open structure pipeline | `docs/OPEN_STRUCTURE_PIPELINE_007_REPORT.md` | COMPLETED CHECKPOINT | inserted-structure evidence |
| Direct EV-A71 InDel evidence | `docs/EV71_2C_DIRECT_INDEL_MAPPING_V1.md` | CURRENT HIGH-WEIGHT EVIDENCE | homolog direct phenotype layer |
| Functional map | `docs/2C_FUNCTIONAL_EXCLUSION_MAP_V3.md` | CURRENT | hard/graded biological constraints |
| Conservation/indel | `docs/CONSERVATION_SCREEN_V2.md` | CURRENT | evolutionary supporting evidence |
| Literature evidence registry | `references/LITERATURE_EVIDENCE_REGISTRY.md` | CURRENT | claim provenance |
| Project decisions | `DECISIONS.md` | CURRENT | active interpretation rules |
| Next work | `TODO.md` | CURRENT | review backlog |

## Branch Provenance

```text
analysis/conservation-002
        ↓
analysis/candidate-panel-008
        ↓
analysis/broad-dynamics-009
```

Do not rewrite older branch checkpoints for new 009 results.

## Current Analysis Funnel

```text
functional + WT structural + conservation evidence       COMPLETE
        ↓
EV-A71 direct insertion/deletion mapping                  COMPLETE
        ↓
all-320 hardening + Pareto + PLM                          COMPLETE
        ↓
OPEN_STRUCTURE_PIPELINE_007                               COMPLETE
        ↓
CANDIDATE_PANEL_EXPANSION_008                             COMPLETE
        ↓
BROAD_DYNAMICS_AND_RECOVERY_009                           COMPLETE / REVIEW READY
  ├─ 248|249 x HA OpenMM NaN audit                         COMPLETE
  ├─ disorder fallback                                     LOW-EVIDENCE
  ├─ local tagged multimer accommodation                   COMPLETE / NONFINITE / INCONCLUSIVE
  ├─ PA14/AGIA exploratory structure screen                COMPLETE / LOW CONFIDENCE
  ├─ balanced site/tag dynamics panel                      COMPLETE
  ├─ replicated comparative MD on A89 2C 112-321           39/39 x 20 ns COMPLETE
  ├─ tag exposure/contact/convergence analysis             COMPLETE
  ├─ dynamic correlation/network analysis                  COMPLETE
  └─ revised dynamics-informed candidate panel             COMPLETE / REVIEW REQUIRED
        ↓
final candidate-panel review                              CURRENT GATE
        ↓
exact experimental nucleotide/RNA audit                   INPUT REQUIRED
        ↓
final wet-lab construct set                               PENDING
        ↓
HRV-A89-specific experimental validation                  GOLD STANDARD
```

## Important Current Interpretation

The broad dynamics layer supports review of a diversified candidate package but does not validate any construct.

The C-terminal `288|289-290|291` region remains represented, but it must not be counted as multiple independent biological regions. Non-C-terminal rows `224|225`, `248|249 x MAP8` and `203|204 x G196_minimal` remain important for panel diversity.

All candidates retain direct homolog InDel conflict and exact nucleotide/RNA uncertainty.
