# Analysis Index

Last updated: 2026-08-25

Read `PROJECT_STATE.md` and `ACTIVE_TASK.md` first.

## Current Authoritative Files

| Topic | Current file | Status | Use |
|---|---|---|---|
| Overall project state | `PROJECT_STATE.md` | CURRENT | authoritative checkpoint |
| Active task pointer | `ACTIVE_TASK.md` | CURRENT | Task 010A completed stop gate |
| Integrated computational-results report archive | `reports/current_computational_results_report_v1/` | CURRENT PRESENTATION ARCHIVE | self-contained interactive HTML + scientific synthesis + detailed tag rationale + provenance/data-boundary record |
| Task 010A specification | `tasks/FINAL_SCIENTIFIC_CLEANUP_AND_EXPERIMENTAL_SHORTLIST_010A.md` | CURRENT COMPLETE | final scientific cleanup task |
| Task 010A cleanup report | `docs/FINAL_SCIENTIFIC_CLEANUP_010A.md` | CURRENT | directional drift, WT differential drift, heterogeneity and method semantics |
| Experimental-review shortlist | `docs/EXPERIMENTAL_REVIEW_SHORTLIST_V1.md` | CURRENT | 4 candidate + 2 control discussion set |
| Experimental-review shortlist TSV | `data/experimental_review_shortlist_v1.tsv` | CURRENT | machine-readable 4+2 shortlist |
| Final candidate panel V5 | `data/final_candidate_panel_v5_experimental_review_cleanup.tsv` | CURRENT | V5 cleanup panel for experimental review |
| Candidate-vs-WT differential drift | `results/dynamics_audit_010/differential_block_drift_vs_wt_v1.tsv` | CURRENT CLEANUP | WT-subtracted block drift |
| Revised sampling semantics | `results/dynamics_audit_010/final_sampling_decision_v2_cleanup.tsv` | CURRENT CLEANUP | observed drift versus extension-trigger drift |
| Replica tag-contact heterogeneity | `results/dynamics_audit_010/tag_nonlocal_contact_replica_heterogeneity_v1.tsv` | CURRENT CLEANUP | replica-level nonlocal tag-contact audit |
| Task 010A internal audit | `results/dynamics_audit_010/task010a_internal_consistency_audit_v1.tsv` | CURRENT QC | consistency checks for V5/shortlist |
| Task 010A execution script | `scripts/dynamics_audit_010a_cleanup.py` | CURRENT PROVENANCE | analysis-only cleanup generator |
| Task 010A Codex prompt | `codex/TASK_010A_CLEANUP_PROMPT.md` | CURRENT PROVENANCE | server execution instructions |
| Task 010 corrected-validation report | `docs/CORRECTED_PROTOCOL_VALIDATION_V1.md` | CURRENT PARENT EVIDENCE | completed corrected CHARMM36 validation |
| Task 010 candidate priority V2 | `docs/FINAL_CANDIDATE_PRIORITY_V2_CORRECTED_VALIDATION.md` | CURRENT PARENT EVIDENCE | V4 construct-level priority panel before 010A cleanup |
| Task 010 final panel V4 | `data/final_candidate_panel_v4_corrected_validation.tsv` | CURRENT PARENT EVIDENCE | machine-readable V4 panel |
| Corrected-validation block stability | `results/dynamics_audit_010/corrected_validation_block_stability_v1.tsv` | CURRENT INPUT | source for WT-differential cleanup |
| Corrected-validation tag exposure | `data/corrected_validation_tag_exposure_v1.tsv` | CURRENT INPUT | source for replica contact heterogeneity |
| Corrected-validation protocol sensitivity | `results/dynamics_audit_010/protocol_sensitivity_v1.tsv` | CURRENT INPUT | legacy vs corrected-protocol comparison |
| Task 010 sampling decision V1 | `results/dynamics_audit_010/final_sampling_decision_v1.tsv` | CURRENT HISTORICAL | contains terminology to be clarified by 010A |
| Dynamic network V2 audited | `docs/DYNAMIC_NETWORK_ANALYSIS_V2_AUDITED.md` | CURRENT EXPLORATORY | network interpretation boundary |
| Task 009 posthoc audit | `docs/DYNAMICS_009_POSTHOC_AUDIT_V1.md` | CURRENT DECISION-CHANGING PROVENANCE | why Task 009 ranking was superseded |
| Literature evidence registry | `references/LITERATURE_EVIDENCE_REGISTRY.md` | CURRENT | claim provenance |
| Project decisions | `DECISIONS.md` | CURRENT | interpretation rules |
| Next work | `TODO.md` | CURRENT | Task 010A execution backlog |

## Current Integrated Report Archive

The current presentation/synthesis layer is stored separately from the versioned analysis outputs:

`reports/current_computational_results_report_v1/`

Contents:

| File | Role |
|---|---|
| `README.md` | archive index, scientific boundary and shortlist summary |
| `HRV_A89_2C_small_tag_computational_results_report.html` | self-contained interactive integrated report |
| `ANALYSIS_SYNTHESIS_V1.md` | long-form scientific synthesis from 320-junction discovery through Task 010A |
| `TAG_SELECTION_RATIONALE_V1.md` | detailed tag-selection reasoning, with dedicated 6×His analysis and explanations for other advanced/non-prioritized tags |
| `REPORT_PROVENANCE_V1.md` | source mapping, major values, visual-reference note and GitHub-vs-server raw-data boundary |

The report archive **does not replace the machine-readable scientific outputs**. When a report statement and an upstream TSV differ, the current versioned upstream TSV/report listed above remains authoritative and the presentation layer must be regenerated or corrected.

The HTML is intended for portable offline reading and embeds its report content rather than depending on CDN-hosted assets.

## Completed Task 010A Outputs

These paths are current after successful server verification:

| Topic | Expected file | Intended status |
|---|---|---|
| Candidate-vs-WT differential drift | `results/dynamics_audit_010/differential_block_drift_vs_wt_v1.tsv` | CURRENT CLEANUP |
| Revised sampling semantics | `results/dynamics_audit_010/final_sampling_decision_v2_cleanup.tsv` | CURRENT CLEANUP |
| Replica tag-contact heterogeneity | `results/dynamics_audit_010/tag_nonlocal_contact_replica_heterogeneity_v1.tsv` | CURRENT CLEANUP |
| Internal consistency audit | `results/dynamics_audit_010/task010a_internal_consistency_audit_v1.tsv` | CURRENT QC |
| V5 experimental-review panel | `data/final_candidate_panel_v5_experimental_review_cleanup.tsv` | CURRENT |
| 4+2 shortlist | `data/experimental_review_shortlist_v1.tsv` | CURRENT |
| Task 010A cleanup report | `docs/FINAL_SCIENTIFIC_CLEANUP_010A.md` | CURRENT |
| Experimental-review shortlist report | `docs/EXPERIMENTAL_REVIEW_SHORTLIST_V1.md` | CURRENT |

## Branch Provenance

```text
analysis/conservation-002
        ↓
analysis/candidate-panel-008
        ↓
analysis/broad-dynamics-009
        ↓
analysis/dynamics-audit-010
        ↓
analysis/experimental-review-cleanup-010a   CURRENT
```

Do not rewrite old branch checkpoints. Task 010A must create new versioned outputs and preserve V4/V2 corrected-validation provenance.

## Current Analysis Funnel

```text
functional / evolutionary / direct-homolog evidence       COMPLETE
        ↓
inserted-structure / PLM / accessibility evidence         COMPLETE
        ↓
BROAD_DYNAMICS_AND_RECOVERY_009                           RAW MD COMPLETE
        ↓
DYNAMICS_ANALYSIS_AUDIT_AND_CANDIDATE_RERANK_010         COMPLETE
  ├─ legacy 39 x 20 ns corrected reanalysis               COMPLETE
  ├─ corrected CHARMM36 18 x 20 ns validation             COMPLETE
  ├─ protocol sensitivity                                 COMPLETE
  ├─ V4 candidate panel                                   COMPLETE
  └─ screening decision STOP_AT_20NS                      COMPLETE
        ↓
FINAL_SCIENTIFIC_CLEANUP_AND_EXPERIMENTAL_SHORTLIST_010A  COMPLETE
  ├─ observed drift vs extension-trigger semantics         COMPLETE
  ├─ candidate-minus-WT block drift                        COMPLETE
  ├─ replica contact heterogeneity                         COMPLETE
  ├─ expert-adjudication provenance                        COMPLETE
  └─ 4 candidate + 2 control shortlist                     COMPLETE
        ↓
integrated computational-results HTML/report archive      COMPLETE
        ↓
experimental discussion                                   TARGET
        ↓
exact nucleotide/RNA audit                                INPUT REQUIRED
        ↓
HRV-A89-specific experimental validation                  GOLD STANDARD
```

## Important Current Interpretation

Task 010A produced the current experimental-review shortlist. It is a precision cleanup, not an excuse to add more MD.

A same-direction drift below the extension threshold must still be reported as observed drift. Candidate-specific interpretation should use WT differential drift where possible. `248|249 x HA` should retain its priority hypothesis while explicitly carrying replica-level nonlocal-contact heterogeneity if confirmed.

Priority A/B is a multi-evidence expert adjudication framework, not a validated algorithmic score. The current stop state is `EXPERIMENTAL_REVIEW_SHORTLIST_READY_FOR_DISCUSSION`.
