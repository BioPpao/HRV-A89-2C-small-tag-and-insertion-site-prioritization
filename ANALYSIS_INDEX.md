# Analysis Index

Last updated: 2026-08-24

Read `PROJECT_STATE.md` first.

## Current Authoritative Files

| Topic | Current file | Status | Use |
|---|---|---|---|
| Overall project state | `PROJECT_STATE.md` | CURRENT | authoritative checkpoint |
| Active task pointer | `ACTIVE_TASK.md` | CURRENT | Task 010 authorization and scope |
| Task 010 specification | `tasks/DYNAMICS_ANALYSIS_AUDIT_AND_CANDIDATE_RERANK_010.md` | CURRENT ACTIVE | full autonomous server task |
| Task 009 posthoc audit | `docs/DYNAMICS_009_POSTHOC_AUDIT_V1.md` | CURRENT DECISION-CHANGING | why old dynamics ranking is provisional |
| Broad dynamics 009 report | `docs/BROAD_DYNAMICS_AND_RECOVERY_009_REPORT.md` | HISTORICAL COMPLETE / PROVISIONAL INTERPRETATION | legacy 009 interpretation |
| Broad dynamics 009 run log | `docs/BROAD_DYNAMICS_AND_RECOVERY_009_RUN_LOG.md` | HISTORICAL CURRENT PROVENANCE | execution/provenance log |
| Dynamics QC V1 | `docs/DYNAMICS_QC_V1.md` | HISTORICAL TECHNICAL QC | verifies 39 x 20 ns completion, not corrected scientific ranking |
| Dynamic network V1 | `docs/DYNAMIC_NETWORK_ANALYSIS_V1.md` | HISTORICAL PROVISIONAL | must be recomputed after PBC/convergence audit |
| Local multimer recovery | `docs/LOCAL_MULTIMER_RECOVERY_V2.md` | CURRENT INCONCLUSIVE | nonfinite local multimer output status |
| Final panel V2 dynamics | `data/final_candidate_panel_v2_dynamics.tsv` | HISTORICAL PROVISIONAL | do not use as final priority list |
| Ranking robustness V2 | `results/broad_dynamics_009/ranking_robustness_v2.tsv` | HISTORICAL PROVISIONAL | old 20 ns ranking summary |
| Replica QC V1 | `data/dynamics_replica_qc_v1.tsv` | CURRENT RAW/TECHNICAL INPUT | 39-replica technical QC |
| Broad dynamics metrics V1 | `data/broad_dynamics_metrics_v1.tsv` | HISTORICAL REANALYSIS REQUIRED | PBC/reference issues |
| Tag exposure dynamics V1 | `data/tag_exposure_dynamics_v1.tsv` | HISTORICAL REANALYSIS REQUIRED | distance proxy; PBC-sensitive |
| Contact persistence V1 | `data/contact_persistence_dynamics_v1.tsv` | HISTORICAL REANALYSIS REQUIRED | candidate-start contacts, PBC-sensitive |
| Dynamic network perturbation V1 | `data/dynamic_network_perturbation_v1.tsv` | HISTORICAL REANALYSIS REQUIRED | PBC/convergence sensitive |
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
DYNAMICS_ANALYSIS_AUDIT_AND_CANDIDATE_RERANK_010         CURRENT ACTIVE TASK
  ├─ inventory/hash legacy trajectories                   REQUIRED
  ├─ PBC make-whole/center/fit repair                     REQUIRED
  ├─ GROMACS-vs-Python RMSD cross-validation              REQUIRED
  ├─ self-drift vs WT-reference RMSD                      REQUIRED
  ├─ junction-matched WT RMSF                             REQUIRED
  ├─ WT-defined contact retention                         REQUIRED
  ├─ true tag SASA + corrected nonlocal contacts          REQUIRED
  ├─ time-block/truncation/replica convergence            REQUIRED
  ├─ network evidence hardening/downgrade                 REQUIRED
  ├─ negative-control discrimination audit                REQUIRED
  ├─ CHARMM36 protocol correction                         REQUIRED
  ├─ reduced corrected-protocol validation subset         AUTHORIZED
  ├─ adaptive more-replica / 50-ns decision               AUTHORIZED, NOT AUTOMATIC
  └─ audited candidate panel V3                           REQUIRED
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
