# Analysis Index

Last updated: 2026-08-22

This file is the navigation layer for the project. Read `PROJECT_STATE.md` first, then use the table below to find the current scientific source for each question.

## Current authoritative files

| Topic | Current file | Status | Use |
|---|---|---|---|
| Overall project state | `PROJECT_STATE.md` | CURRENT | authoritative checkpoint and next step |
| Methodological logic audit | `docs/METHOD_LOGIC_AUDIT_V2.md` | CURRENT SUPPORTING | corrected logic, evidence hierarchy, Phase 0 summary |
| Post-direct-evidence method audit | `docs/METHOD_GAP_AND_NEXT_EVIDENCE_AUDIT_V2.md` | **CURRENT STRATEGIC** | reinterprets direct EV-A71 phenotype, rejects both premature shortlist promotion and universal-A89-intolerance claims, authorizes method hardening |
| Current execution task | `tasks/GPU_RECOVERY_004.md` | **BLOCKED / NO GPU VISIBLE** | attempted PLM GPU recovery but stopped before GPU work because no CUDA device was visible |
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
| Hardened all-junction matrix | `data/candidate_junctions_v4_method_hardening.tsv` | CURRENT DATA / PLM-BLOCKED | primary V4 matrix; PLM columns marked blocked |
| One-shot final report | `docs/ONE_SHOT_COMPUTATIONAL_AUDIT_003_REPORT.md` | CURRENT REPORT | final state `METHOD_HARDENING_BLOCKED` |
| Method hardening report | `docs/METHOD_HARDENING_002_REPORT.md` | CURRENT REPORT | CPU module results and PLM blocker |
| GPU recovery report | `docs/GPU_RECOVERY_004_REPORT.md` | CURRENT REPORT / BLOCKED | final state `GPU_RECOVERY_BLOCKED_NO_GPU`; records GPU visibility checks |
| GPU visibility check | `results/gpu_recovery_004/gpu_visibility_check.tsv` | CURRENT PROVENANCE | exact required GPU check commands, exit codes and outputs |
| Phylogeny-aware indel report | `docs/PHYLOGENY_AWARE_INDEL_V1.md` | CURRENT REPORT | FastTree/Fitch-parsimony independent indel lower-bound analysis |
| Tag-specific PLM report | `docs/TAG_SPECIFIC_PLM_SCAN_V1.md` | BLOCKED REPORT | MAP8/HA/G196 forms recorded; PLM scores unavailable |
| Ranking robustness audit | `docs/RANKING_ROBUSTNESS_AUDIT_V1.md` | CURRENT REPORT | non-PLM Pareto sensitivity and negative-control audit |
| Tag consensus report | `docs/TAG_SPECIFIC_CONSENSUS_V1.md` | BLOCKED REPORT | cross-tag consensus unavailable because PLM scores blocked |
| Computational review set | `docs/COMPUTATIONAL_REVIEW_SET_V1.md`, `data/computational_review_set_v1.tsv` | CURRENT REVIEW SET / NOT MODELING AUTHORIZATION | 17-row conflict-aware review set |
| Lightweight structural triage | `docs/LIGHTWEIGHT_STRUCTURAL_TRIAGE_V1.md` | DEFERRED | no mature reproducible structure workflow available in this session |
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
GPU_RECOVERY_004                                BLOCKED / NO GPU VISIBLE
  └─ required GPU visibility checks completed
        ↓
ChatGPT/user review                             REQUIRED STOP GATE
        ↓
insertion-specific loop + AF/ColabFold          BLOCKED PENDING REVIEW
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

`GPU_RECOVERY_BLOCKED_NO_GPU`

The EV-A71 direct 8-aa insertion phenotype is unfavorable across mapped A89 junctions and therefore demotes the prior `287|288–290|291` structure/conservation shortlist. The result is treated as a strong homolog prior rather than universal proof that every A89-specific tag sequence will fail.

Current candidate/control roles:

- `287|288–290|291`: `STRUCTURE_EVOLUTION_FAVORED__DIRECT_HOMOLOG_CONFLICT`;
- `248|249`, `256|257`: `HISTORICAL_INSERTION_SUPPORT__MODERN_CONFLICT_CONTROL`;
- near-miss/non-strict sites remain eligible for full 320-junction continuous/Pareto re-ranking unless hard-excluded biologically.

The next scientific question is whether to rerun `GPU_RECOVERY_004` inside a Slurm GPU allocation with visible `/dev/nvidia*`, accept the unresolved PLM blocker and pivot to HRV-A89-specific empirical validation, or explicitly authorize conflict-aware Tag x Site modeling despite absent PLM evidence.
