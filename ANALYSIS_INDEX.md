# Analysis Index

Last updated: 2026-08-22

This file is the navigation layer for the project. Read `PROJECT_STATE.md` first, then use the table below to find the current scientific source for each question.

## Current authoritative files

| Topic | Current file | Status | Use |
|---|---|---|---|
| Overall project state | `PROJECT_STATE.md` | CURRENT | authoritative checkpoint and next step |
| Methodological logic audit | `docs/METHOD_LOGIC_AUDIT_V2.md` | CURRENT SUPPORTING | corrected logic, evidence hierarchy, Phase 0 summary |
| Post-direct-evidence method audit | `docs/METHOD_GAP_AND_NEXT_EVIDENCE_AUDIT_V2.md` | **CURRENT STRATEGIC** | reinterprets direct EV-A71 phenotype, rejects both premature shortlist promotion and universal-A89-intolerance claims, authorizes method hardening |
| Current execution task | `tasks/CONTINUOUS_TAG_SITE_MODELING_005.md` | **COMPLETE / PARTIAL** | compact conflict-aware tag x site perturbation modeling; final state `TAG_SITE_MODELING_PARTIALLY_COMPLETE` |
| Active task pointer | `ACTIVE_TASK.md` | CURRENT | current task/stop gate for Codex and ChatGPT |
| Functional exclusion/constraint map | `docs/2C_FUNCTIONAL_EXCLUSION_MAP_V3.md` | CURRENT | latest A89-specific functional map |
| Historical insertion-tolerance conflict logic | `docs/2C_FUNCTIONAL_CONSTRAINT_MAP_V2.md` | CURRENT SUPPORTING | preserves historical PV insertion-tolerance evidence and literature-rescue conflicts |
| Four-structure structural screen | `docs/STRUCTURAL_SCREEN_V2.md`, `data/junction_structural_metrics_v2.tsv` | CURRENT DATA/REPORT | all-320 WT structural metrics; strict pass is now annotation rather than sole candidate funnel |
| Small-tag evidence screen | `docs/TAG_CANDIDATE_SCREEN_V1.md` | CURRENT SUPPORTING | tag-level literature ranking; not construct ranking |
| HRV-A conservation / indel tolerance | `docs/CONSERVATION_SCREEN_V2.md` | CURRENT | MAFFT/ICTV-hardened near-HRV evolutionary layer |
| Candidate QC gate | `docs/CANDIDATE_JUNCTION_QC_V1.md` | CURRENT SUPPORTING | shortlist state before direct homolog InDel integration |
| Preliminary shortlist | `docs/CANDIDATE_SHORTLIST_001_DECISION.md` | SUPERSEDED AS TARGETED SHORTLIST | retained as working-hypothesis provenance only |
| Direct homolog InDel task | `tasks/DIRECT_INDEL_001.md` | COMPLETE TASK | EV-A71 2C direct insertion/deletion mapping specification |
| EV-A71 direct InDel mapping | `docs/EV71_2C_DIRECT_INDEL_MAPPING_V1.md` | CURRENT HIGH-WEIGHT EVIDENCE | maps EV-A71 direct 2C phenotype to all 320 A89 junctions; requires shortlist revision |
| Current integrated direct-evidence matrix | `data/candidate_junctions_v3_direct_indel.tsv` | CURRENT DATA | all-320 V3 matrix before METHOD_HARDENING_002 |
| Hardened all-junction matrix | `data/candidate_junctions_v4_method_hardening.tsv` | SUPERSEDED BY V5 / PROVENANCE | primary non-PLM V4 matrix; PLM columns marked blocked |
| GPU PLM integrated matrix | `data/candidate_junctions_v5_plm_gpu.tsv` | CURRENT DATA | all-320 V5 matrix with completed ESM2 tag-specific PLM layer |
| Tag-site modeling report | `docs/CONTINUOUS_TAG_SITE_MODELING_005_REPORT.md` | CURRENT REPORT | 33-junction x 4-tag panel; WT anchor/context modeling completed; structure/loop/energy primary methods deferred by software availability |
| Tag-site modeling run log | `docs/CONTINUOUS_TAG_SITE_MODELING_005_RUN_LOG.md` | CURRENT PROVENANCE | commands, software audit, QC and deferred-method records |
| Tag-site modeling panel | `data/tag_site_modeling_panel_v1.tsv` | CURRENT DATA | 132 site x tag constructs from V2 review set and fixed MAP8/HA/G196 forms |
| Tag-site integrated perturbation | `data/tag_site_integrated_perturbation_v1.tsv` | CURRENT DATA | separate direct/function/PLM/loop-proxy/hexamer/network/status dimensions without a hidden total score |
| Tag-site robustness | `results/tag_site_modeling_005/cross_method_robustness.tsv` | CURRENT DATA | cross-method support/disfavor flags with deferred primary methods preserved |
| One-shot final report | `docs/ONE_SHOT_COMPUTATIONAL_AUDIT_003_REPORT.md` | CURRENT REPORT | final state `METHOD_HARDENING_BLOCKED` |
| Method hardening report | `docs/METHOD_HARDENING_002_REPORT.md` | CURRENT REPORT | CPU module results and PLM blocker |
| GPU recovery report | `docs/GPU_RECOVERY_004_REPORT.md` | CURRENT REPORT | final state `READY_FOR_CONFLICT_AWARE_TAG_SITE_MODELING`; records GPU runtime and PLM results |
| GPU visibility check | `results/gpu_recovery_004/gpu_visibility_check.tsv` | CURRENT PROVENANCE | exact required GPU check commands, exit codes and outputs |
| GPU PLM source records | `references/gpu_recovery_004_plm_source_records_v1.tsv` | CURRENT PROVENANCE | ESM2 checkpoint source paths and SHA256 checksums |
| Phylogeny-aware indel report | `docs/PHYLOGENY_AWARE_INDEL_V1.md` | CURRENT REPORT | FastTree/Fitch-parsimony independent indel lower-bound analysis |
| Tag-specific PLM report | `docs/TAG_SPECIFIC_PLM_SCAN_V2_GPU.md` | CURRENT REPORT | completed GPU ESM2 PLM scan for MAP8, HA and two G196 forms |
| Ranking robustness audit | `docs/RANKING_ROBUSTNESS_AUDIT_V1.md` | CURRENT REPORT | non-PLM Pareto sensitivity and negative-control audit |
| Tag consensus report | `docs/TAG_SPECIFIC_CONSENSUS_V2_GPU.md`, `data/tag_specific_consensus_v2_gpu.tsv` | CURRENT REPORT/DATA | cross-tag PLM consensus and disagreement after GPU scoring |
| Computational review set | `data/computational_review_set_v2_plm_gpu.tsv` | CURRENT REVIEW SET | 33-row PLM-updated conflict-aware review set; not final construct selection |
| Lightweight structural triage | `docs/LIGHTWEIGHT_STRUCTURAL_TRIAGE_V2_GPU.md` | DEFERRED | no mature reproducible structure workflow installed without derailing GPU PLM recovery |
| EV-A71 direct InDel to A89 mapping | `data/evA71_2C_direct_indel_to_A89_v1.tsv` | CURRENT DATA | all-320 A89 projection of direct homolog insertion/deletion/substitution context |
| EV-A71/A89 mature-2C alignment | `data/evA71_A89_2C_mafft_alignment_v1.fasta`, `data/evA71_A89_2C_alignment_map_v1.tsv` | CURRENT DATA | auditable mature-2C sequence alignment and mapping |
| HRV-A residue conservation | `data/hrvA_conservation_per_residue_v2.tsv` | CURRENT DATA | 321 A89-anchored conservation rows |
| HRV-A junction conservation | `data/hrvA_conservation_per_junction_v2.tsv` | CURRENT DATA | 320 A89 junction rows with local-window/refined indel metrics |
| HRV-A/B/C context | `data/hrvABC_candidate_window_context.tsv` | CURRENT DATA | secondary broader-rhinovirus context |
| CVB3→A89 functional mapping | `data/CVB3_to_A89_functional_mapping_v1.tsv` | CURRENT DATA | homolog mapping used for RNA/pore-function constraints |
| Structure integrity audit | `results/phase0_structure_integrity.tsv` | CURRENT RESULT | residue/chain/sequence integrity |
| Structure RMSD audit | `results/phase0_structure_rmsd.tsv` | CURRENT RESULT | monomer↔hexamer and model↔model correspondence |
| Junction analysis code | `scripts/analyze_insertion_junctions.py` | CURRENT SCRIPT | reproducible WT structural feature calculation |
| CONSERVATION_002 code | `scripts/build_conservation_002_panels.py`, `scripts/run_mafft_map_to_A89.py`, `scripts/calculate_conservation_v2.py`, `scripts/integrate_junction_evidence_v2.py` | CURRENT SCRIPT | VMR/MAFFT/conservation/integration hardening pipeline |
| DIRECT_INDEL_001 code | `scripts/direct_indel_001_map_ev71_to_a89.py` | CURRENT SCRIPT | direct homolog phenotype extraction/mapping/V3 integration |
| Reference sequence | `references/HRV_A89_2C_reference_sequence.fasta` | CURRENT INPUT | authoritative 321-aa sequence |
| Literature evidence registry | `references/LITERATURE_EVIDENCE_REGISTRY.md` | CURRENT | source-to-claim map and evidence boundaries |
| Direct InDel source records | `references/direct_indel_001/source_records_v1.tsv` | CURRENT PROVENANCE | source files/checksums/roles for DIRECT_INDEL_001 |
| Structure input provenance | `INPUT_PROVENANCE.md` | CURRENT | input role, checksums, storage policy |
| Project decisions | `DECISIONS.md` | CURRENT | active decisions; includes post-direct-evidence decisions D-022–D-026 |
| Next work | `TODO.md` | CURRENT | prioritized executable backlog |

## Superseded / provenance files

These remain in Git for scientific provenance. Do not use them as the current decision source unless comparing how the logic changed.

| File | Status | Superseded by / note |
|---|---|---|
| `docs/2C_FUNCTIONAL_EXCLUSION_MAP_V1.md` | SUPERSEDED | replaced by V2/V3 mapping and graded evidence logic |
| `docs/2C_FUNCTIONAL_EXCLUSION_MAP_V2.md` | SUPERSEDED | replaced by V3 A89-specific mapping |
| `docs/STRUCTURAL_SCREEN_PRELIMINARY_V1.md` | SUPERSEDED | replaced by V2 all-atom/rSASA/interface screen |
| `docs/CONSERVATION_SCREEN_V1.md` | PROVISIONAL / SUPERSEDED | replaced for decision-making by `docs/CONSERVATION_SCREEN_V2.md` |
| `docs/METHOD_GAP_AND_NEXT_EVIDENCE_AUDIT_V1.md` | SUPERSEDED STRATEGIC AUDIT | correctly prioritized DIRECT_INDEL_001 before it was run; post-result interpretation now comes from V2 |
| `data/junction_structural_metrics_v1.tsv` | PROVENANCE DATA | regenerated as V2; V1 contained 8 strict-flag/gate inconsistencies |
| `data/candidate_junctions_v1.tsv` | PROVISIONAL DATA | replaced by V2/V3 for decision-making |
| `data/candidate_junctions_v2.tsv` | PRE-DIRECT-EVIDENCE DATA | preserved; direct phenotype added in V3 |

`docs/2C_FUNCTIONAL_CONSTRAINT_MAP_V2.md` remains current supporting evidence because it records direct positive-tolerance literature and the rescue/conflict track.

## Current analysis funnel

```text
4-structure input audit                         COMPLETE
        ↓
2C literature/function mapping                  COMPLETE (working V3)
        ↓
320-junction WT structural metrics              COMPLETE (V2)
        ↓
HRV-A conservation + natural indel              COMPLETE (V2)
        ↓
preliminary candidate shortlist                 SUPERSEDED AS TARGETED SET
        ↓
EV-A71 direct 2C InDel fitness → A89            COMPLETE (V1)
        ↓
post-direct-evidence strategic audit             COMPLETE (Audit V2)
        ↓
ONE_SHOT_COMPUTATIONAL_AUDIT_003                COMPLETE WITH BLOCKER
  ├─ EV-A71 substitution tolerance
  ├─ continuous/Pareto all-320 re-ranking
  ├─ phylogeny-aware independent indel events
  └─ MAP8/HA/G196 tag-specific PLM scan BLOCKED
        ↓
GPU_RECOVERY_004                                COMPLETE
  ├─ GPU/PyTorch/ESM2 environment recovered
  ├─ MAP8/HA/G196 PLM scan completed
  ├─ cross-tag consensus completed
  └─ V5 matrix + V2 review set completed
        ↓
CONTINUOUS_TAG_SITE_MODELING_005                COMPLETE / PARTIAL
  ├─ compact 33-junction x 4-tag panel
  ├─ WT oligomer-context compatibility
  ├─ WT residue-contact-network anchor analysis
  ├─ targeted V5/V2 direct/evolutionary/PLM reuse
  └─ insertion-specific structure / loop / energy DEFERRED_SOFTWARE
        ↓
ChatGPT/user review                             REQUIRED STOP GATE
        ↓
dedicated mature structure/loop recovery or targeted dynamics  PENDING DECISION
        ↓
targeted MD                                     LATER
        ↓
exact replicon nucleotide/RNA audit             INPUT REQUIRED
        ↓
experimental construct/control set              PENDING
        ↓
HRV-A89 biological validation                   EXPERIMENTAL GOLD STANDARD
```

## Current checkpoint result

Current project state:

`TAG_SITE_MODELING_PARTIALLY_COMPLETE`

CONTINUOUS_TAG_SITE_MODELING_005 evaluated 132 constructs from the V2 review set. Completed WT-anchor/context layers identify `289|290` and `290|291` with MAP8 or G196_minimal as the lowest relative perturbation rows, but all retain direct homolog insertion conflict and no inserted-structure ensemble or energy calculation was completed.

Current candidate/control roles:

- `289|290`, `290|291` with MAP8/G196_minimal: `RELATIVELY_LOWER_PERTURBATION__DIRECT_EVIDENCE_CONFLICT` under completed layers only;
- `287|288`, `288|289`: mixed/inconclusive within the old conflict cluster;
- `248|249`, `256|257`: `HISTORICAL_INSERTION_SUPPORT__MODERN_CONFLICT_CONTROL` with unfavorable WT oligomer/contact context;
- `203|204`, `224|225`: structurally/context disfavored in the current panel.

The next scientific question is whether ChatGPT/user authorizes a dedicated mature structure-prediction/loop-remodeling recovery task, targeted dynamics from the partial reduced set, or prioritization of HRV-A89-specific insertion phenotype. This is not final construct recommendation and does not bypass exact RNA/codon requirements.
