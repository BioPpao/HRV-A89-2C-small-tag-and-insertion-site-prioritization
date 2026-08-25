# Analysis Index

Last updated: 2026-08-25

Read `PROJECT_STATE.md` and `ACTIVE_TASK.md` first.

## Current Authoritative Files

| Topic | Current file | Status | Use |
|---|---|---|---|
| Overall project state | `PROJECT_STATE.md` | CURRENT | authoritative checkpoint |
| Active task pointer | `ACTIVE_TASK.md` | CURRENT | Task 010A authorization and scope |
| Task 010A specification | `tasks/FINAL_SCIENTIFIC_CLEANUP_AND_EXPERIMENTAL_SHORTLIST_010A.md` | CURRENT ACTIVE | final scientific cleanup task |
| Task 010A execution script | `scripts/dynamics_audit_010a_cleanup.py` | CURRENT ACTIVE | analysis-only cleanup generator |
| Task 010A Codex prompt | `codex/TASK_010A_CLEANUP_PROMPT.md` | CURRENT ACTIVE | server execution instructions |
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

## Expected Task 010A Outputs

These paths become current after successful server verification:

| Topic | Expected file | Intended status |
|---|---|---|
| Candidate-vs-WT differential drift | `results/dynamics_audit_010/differential_block_drift_vs_wt_v1.tsv` | CURRENT CLEANUP |
| Revised sampling semantics | `results/dynamics_audit_010/final_sampling_decision_v2_cleanup.tsv` | CURRENT CLEANUP |
| Replica tag-contact heterogeneity | `results/dynamics_audit_010/tag_nonlocal_contact_replica_heterogeneity_v1.tsv` | CURRENT CLEANUP |
| V5 experimental-review panel | `data/final_candidate_panel_v5_experimental_review_cleanup.tsv` | CURRENT AFTER COMPLETION |
| 4+2 shortlist | `data/experimental_review_shortlist_v1.tsv` | CURRENT AFTER COMPLETION |
| Task 010A cleanup report | `docs/FINAL_SCIENTIFIC_CLEANUP_010A.md` | CURRENT AFTER COMPLETION |
| Experimental-review shortlist report | `docs/EXPERIMENTAL_REVIEW_SHORTLIST_V1.md` | CURRENT AFTER COMPLETION |

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
FINAL_SCIENTIFIC_CLEANUP_AND_EXPERIMENTAL_SHORTLIST_010A  CURRENT
  ├─ observed drift vs extension-trigger semantics         REQUIRED
  ├─ candidate-minus-WT block drift                        REQUIRED
  ├─ replica contact heterogeneity                         REQUIRED
  ├─ expert-adjudication provenance                        REQUIRED
  └─ 4 candidate + 2 control shortlist                     REQUIRED
        ↓
experimental discussion                                   TARGET
        ↓
exact nucleotide/RNA audit                                INPUT REQUIRED
        ↓
HRV-A89-specific experimental validation                  GOLD STANDARD
```

## Important Current Interpretation

Task 010 already supports experimental review. Task 010A is a precision cleanup, not an excuse to add more MD.

A same-direction drift below the extension threshold must still be reported as observed drift. Candidate-specific interpretation should use WT differential drift where possible. `248|249 x HA` should retain its priority hypothesis while explicitly carrying replica-level nonlocal-contact heterogeneity if confirmed.

Priority A/B is a multi-evidence expert adjudication framework, not a validated algorithmic score.
