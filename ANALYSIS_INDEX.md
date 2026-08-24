# Analysis Index

Last updated: 2026-08-25

Read `PROJECT_STATE.md` first.

## Current Authoritative Files

| Topic | Current file | Status | Use |
|---|---|---|---|
| Overall project state | `PROJECT_STATE.md` | CURRENT | authoritative checkpoint |
| Active task pointer | `ACTIVE_TASK.md` | CURRENT | Task 010 checkpoint and validation-running status |
| Task 010 specification | `tasks/DYNAMICS_ANALYSIS_AUDIT_AND_CANDIDATE_RERANK_010.md` | CURRENT ACTIVE | full autonomous server task |
| Task 010 final report | `docs/DYNAMICS_ANALYSIS_AUDIT_010_REPORT.md` | CURRENT PROVISIONAL | corrected reanalysis, rerank and validation submission state |
| Audited final candidate priority | `docs/FINAL_CANDIDATE_PRIORITY_V1_AUDITED.md` | CURRENT PROVISIONAL | construct-level Priority A/B/control panel |
| Final candidate panel V3 | `data/final_candidate_panel_v3_audited.tsv` | CURRENT PROVISIONAL | machine-readable audited candidate panel |
| Dynamic network V2 audited | `docs/DYNAMIC_NETWORK_ANALYSIS_V2_AUDITED.md` | CURRENT EXPLORATORY | corrected network interpretation boundary |
| Corrected broad dynamics metrics V2 | `data/broad_dynamics_metrics_v2_corrected.tsv` | CURRENT | PBC-corrected self/WT-reference/RMSF/Rg metrics |
| Corrected contact persistence V2 | `data/contact_persistence_dynamics_v2_corrected.tsv` | CURRENT | WT-defined and candidate-start contact metrics |
| Corrected tag SASA V2 | `data/tag_exposure_dynamics_v2_sasa.tsv` | CURRENT | tag SASA and corrected nonlocal tag-contact metrics |
| Corrected network perturbation V2 | `data/dynamic_network_perturbation_v2_corrected.tsv` | CURRENT EXPLORATORY | PBC-corrected DCCM/network metrics |
| Task 010 validation subset | `results/dynamics_audit_010/corrected_validation_subset.tsv` | SUBMITTED / PENDING | corrected CHARMM36 validation job `164594` |
| Task 009 posthoc audit | `docs/DYNAMICS_009_POSTHOC_AUDIT_V1.md` | CURRENT DECISION-CHANGING | why old dynamics ranking is provisional |
| Broad dynamics 009 report | `docs/BROAD_DYNAMICS_AND_RECOVERY_009_REPORT.md` | HISTORICAL COMPLETE / PROVISIONAL INTERPRETATION | legacy 009 interpretation |
| Broad dynamics 009 run log | `docs/BROAD_DYNAMICS_AND_RECOVERY_009_RUN_LOG.md` | HISTORICAL CURRENT PROVENANCE | execution/provenance log |
| Dynamics QC V1 | `docs/DYNAMICS_QC_V1.md` | HISTORICAL TECHNICAL QC | verifies 39 x 20 ns completion, not corrected scientific ranking |
| Dynamic network V1 | `docs/DYNAMIC_NETWORK_ANALYSIS_V1.md` | HISTORICAL SUPERSEDED | superseded by Task 010 V2 audited network report |
| Local multimer recovery | `docs/LOCAL_MULTIMER_RECOVERY_V2.md` | CURRENT INCONCLUSIVE | nonfinite local multimer output status |
| Final panel V2 dynamics | `data/final_candidate_panel_v2_dynamics.tsv` | HISTORICAL SUPERSEDED | do not use as final priority list |
| Ranking robustness V2 | `results/broad_dynamics_009/ranking_robustness_v2.tsv` | HISTORICAL PROVISIONAL | old 20 ns ranking summary |
| Replica QC V1 | `data/dynamics_replica_qc_v1.tsv` | CURRENT RAW/TECHNICAL INPUT | 39-replica technical QC |
| Broad dynamics metrics V1 | `data/broad_dynamics_metrics_v1.tsv` | HISTORICAL SUPERSEDED | PBC/reference issues; use V2 corrected |
| Tag exposure dynamics V1 | `data/tag_exposure_dynamics_v1.tsv` | HISTORICAL SUPERSEDED | distance proxy; use V2 SASA |
| Contact persistence V1 | `data/contact_persistence_dynamics_v1.tsv` | HISTORICAL SUPERSEDED | candidate-start contacts; use V2 corrected |
| Dynamic network perturbation V1 | `data/dynamic_network_perturbation_v1.tsv` | HISTORICAL SUPERSEDED | PBC/convergence sensitive; use V2 corrected |
| Production manifest | `results/broad_dynamics_009/production_manifest.tsv` | CURRENT RAW INPUT | paths/status/provenance |
| Replica completion | `results/broad_dynamics_009/replica_completion.tsv` | CURRENT RAW INPUT | paths/status/provenance |
| Balanced dynamics panel V2 | `data/balanced_targeted_dynamics_panel_v2.tsv` | CURRENT HISTORICAL PANEL | frozen panel that was simulated |
| Candidate-panel 008 report | `docs/CANDIDATE_PANEL_EXPANSION_008_REPORT.md` | COMPLETED CHECKPOINT | pre-dynamics candidate-panel context |
| Final candidate strategy | `docs/FINAL_CANDIDATE_PANEL_STRATEGY_V1.md` | CURRENT STRATEGY | diversified panel logic |
| Open structure pipeline | `docs/OPEN_STRUCTURE_PIPELINE_007_REPORT.md` | COMPLETED CHECKPOINT | inserted-structure evidence |
| Direct EV-A71 InDel evidence | `docs/EV71_2C_DIRECT_INDEL_MAPPING_V1.md` | CURRENT HIGH-WEIGHT EVIDENCE | homolog direct phenotype layer |
| Functional map | `docs/2C_FUNCTIONAL_EXCLUSION_MAP_V3.md` | CURRENT | hard/graded biological constraints |
| Conservation/indel | `docs/CONSERVATION_SCREEN_V2.md` | CURRENT | evolutionary supporting evidence |
| Literature evidence registry | `references/LITERATURE_EVIDENCE_REGISTRY.md` | CURRENT | claim provenance |
| Project decisions | `DECISIONS.md` | CURRENT | active interpretation rules |
| Next work | `TODO.md` | CURRENT | Task 010 execution backlog |

## Branch Provenance

```text
analysis/conservation-002
        ↓
analysis/candidate-panel-008
        ↓
analysis/broad-dynamics-009
        ↓
analysis/dynamics-audit-010   CURRENT
```

Do not rewrite old branch checkpoints. Corrected Task 010 outputs must use new paths/version names.

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
BROAD_DYNAMICS_AND_RECOVERY_009                           RAW MD COMPLETE
  ├─ 39/39 x 20 ns trajectories                           COMPLETE / PRESERVED
  ├─ old geometry analysis                                PROVISIONAL / PBC AUDIT FAILED
  ├─ old Tier A/B dynamics ranking                        PROVISIONAL / SUPERSEDED PENDING 010
  └─ local multimer recovery                              INCONCLUSIVE
        ↓
DYNAMICS_ANALYSIS_AUDIT_AND_CANDIDATE_RERANK_010         PROVISIONAL CHECKPOINT
  ├─ inventory/hash legacy trajectories                   COMPLETE
  ├─ PBC make-whole/center/fit repair                     COMPLETE
  ├─ GROMACS-vs-Python RMSD cross-validation              COMPLETE
  ├─ self-drift vs WT-reference RMSD                      COMPLETE
  ├─ junction-matched WT RMSF                             COMPLETE
  ├─ WT-defined contact retention                         COMPLETE
  ├─ true tag SASA + corrected nonlocal contacts          COMPLETE
  ├─ time-block/truncation/replica convergence            COMPLETE
  ├─ network evidence hardening/downgrade                 COMPLETE
  ├─ negative-control discrimination audit                COMPLETE
  ├─ CHARMM36 protocol correction                         COMPLETE
  ├─ reduced corrected-protocol validation subset         SUBMITTED AS JOB 164594
  ├─ adaptive more-replica / 50-ns decision               PENDING VALIDATION RESULTS
  └─ audited candidate panel V3                           COMPLETE / PROVISIONAL
        ↓
experimental candidate review                            TARGET
        ↓
exact experimental nucleotide/RNA audit                  INPUT REQUIRED
        ↓
final nucleotide-level construct set                     PENDING
        ↓
HRV-A89-specific experimental validation                 GOLD STANDARD
```

## Important Current Interpretation

The repository already contains substantial evidence for a preliminary multi-site wet-lab candidate panel, but the Task 009 dynamics-derived Tier A/B calls must not be treated as final until Task 010 corrects the analysis.

The 20 ns duration is not itself a failure. The scientific question is whether corrected observables and candidate ordering are stable across independent replicas and time windows.

Do not impose a blanket 50 ns requirement. Additional replicas/extension should be limited to decision-critical systems identified by Task 010.
