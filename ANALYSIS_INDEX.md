# Analysis Index

Last updated: 2026-09-02

Read `PROJECT_STATE.md` and `ACTIVE_TASK.md` first.

## Current Authoritative Files

| Topic | Current file | Status | Use |
|---|---|---|---|
| Overall project state | `PROJECT_STATE.md` | CURRENT | authoritative checkpoint |
| Active task pointer | `ACTIVE_TASK.md` | CURRENT | Task 010A completed stop gate |
| Task 011 specification | `tasks/9A5_MONOMER_HEXAMER_CONTEXT_011.md` | CURRENT COMPLETE | authorized 9A5-bound context task |
| Task 011 integration report | `docs/9A5_COMPLEX_CONTEXT_INTEGRATION_V1.md` | CURRENT | final 9A5 monomer+hexamer context integration |
| Task 011 monomer report | `docs/9A5_MONOMER_CONTEXT_V1.md` | CURRENT | 9A5-bound monomer/core transfer layer |
| Task 011 hexamer report | `docs/9A5_HEXAMER_CONTEXT_V1.md` | CURRENT | 1x9A5 full-length hexamer and free-hexamer context layer |
| Final candidate panel V6 | `data/final_candidate_panel_v6_9a5_context.tsv` | CURRENT | V5 plus 9A5-bound complex context layer |
| 9A5 structure inventory | `data/9a5_context_structure_inventory_v1.tsv` | CURRENT PROVENANCE | source/target structure QC and checksums |
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

## Task 011 Completion

`READY_FOR_EXPERIMENTAL_REVIEW_WITH_9A5_CONTEXT_LAYER`

Task 011 adds a 9A5-bound monomer/core and full-length hexamer structural-context layer to the current V5 experimental-review panel. It does not authorize or perform nucleotide design, wet-lab protocols, new MD, or safety/validation claims.

# Task 011A 9A5 Context QC Outputs
| Artifact | Path | Status | Notes |
|---|---|---|---|
| Task 011A report | `docs/9A5_CONTEXT_QC_011A.md` | CURRENT | QC-hardened 9A5 context integration |
| V7 panel | `data/final_candidate_panel_v7_9a5_context_qc.tsv` | CURRENT | Supersedes V6 for 9A5-context review |
| Endpoint provenance | `data/9a5_context_input_provenance_v2_qc.tsv` | CURRENT | Includes duplicate endpoint resolution and trajectory checksums |
| Structure inventory | `data/9a5_context_structure_inventory_v2_qc.tsv` | CURRENT | Old duplicate endpoint PDBs retained as provenance only |
| Hexamer compatibility | `data/9a5_hexamer_tag_compatibility_v2_qc.tsv` | CURRENT | Duplicate-collapsed corrected endpoint ensemble |
| 248 HA robustness | `data/248_249_HA_hexamer_robustness_v1.tsv` | CURRENT | HA/MAP8 tag-identity comparison |
| QC figures | `figures/9a5_context_011a_qc/` | CURRENT | Five required QC figure sets |
| Endpoint re-export QC | `results/9a5_context_011a_qc/endpoint_reexport_qc_v1.tsv` | CURRENT | Explicit final-frame re-export audit |

# Synthesized Plasmid Batch

| Artifact | Path | Status | Use |
|---|---|---|---|
| Synthesized plasmid panel | `data/synthesized_plasmid_panel_v1.tsv` | CURRENT EXPERIMENTAL STATUS | machine-readable record of the eight already synthesized constructs |
| Synthesized panel note | `docs/SYNTHESIZED_PLASMID_PANEL_V1.md` | CURRENT | links experimental batch status to Task 011A interpretation without reopening construct selection |

Current batch gate: `NO_FURTHER_COMPUTATIONAL_CANDIDATE_SELECTION_OR_CONSTRUCT_REDESIGN_REQUIRED`.

## Final Task 011A Review

- `docs/TASK011A_CHATGPT_REVIEW_V1.md` — accepted scientific interpretation of Task 011A, including corrected endpoint QC, 248|249 tag-identity dependence, and the post-synthesis stop decision.
