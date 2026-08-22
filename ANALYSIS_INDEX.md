# Analysis Index

Last updated: 2026-08-22

This file is the navigation layer for the project. Read `PROJECT_STATE.md` first, then use the table below to find the current scientific source for each question.

## Current authoritative files

| Topic | Current file | Status | Use |
|---|---|---|---|
| Overall project state | `PROJECT_STATE.md` | CURRENT | authoritative checkpoint and next step |
| Methodological self-audit | `docs/METHOD_LOGIC_AUDIT_V2.md` | CURRENT | corrected logic, evidence hierarchy, Phase 0 summary |
| Method-gap / next-evidence audit | `docs/METHOD_GAP_AND_NEXT_EVIDENCE_AUDIT_V1.md` | CURRENT STRATEGIC | identifies direct homolog InDel phenotype as the next higher-information layer and records remaining method gaps |
| Functional exclusion/constraint map | `docs/2C_FUNCTIONAL_EXCLUSION_MAP_V3.md` | CURRENT | latest A89-specific functional map |
| Direct-tolerance conflict / rescue logic | `docs/2C_FUNCTIONAL_CONSTRAINT_MAP_V2.md` | CURRENT SUPPORTING | preserves historical PV insertion-tolerance evidence and conflicts |
| Four-structure structural screen | `docs/STRUCTURAL_SCREEN_V2.md`, `data/junction_structural_metrics_v2.tsv` | CURRENT | all-atom 320-junction structural funnel regenerated in CONSERVATION_002 |
| Small-tag evidence screen | `docs/TAG_CANDIDATE_SCREEN_V1.md` | CURRENT | tag-level literature ranking; not a construct ranking |
| HRV-A conservation / indel tolerance | `docs/CONSERVATION_SCREEN_V2.md` | CURRENT | MAFFT/ICTV-hardened near-HRV evolutionary layer |
| Candidate QC gate | `docs/CANDIDATE_JUNCTION_QC_V1.md` | CURRENT SUPPORTING | shortlist state before direct homolog InDel integration |
| Candidate shortlist decision framework | `docs/CANDIDATE_SHORTLIST_001_DECISION.md` | SUPERSEDED AS SHORTLIST | working hypothesis retained as provenance; direct homolog InDel V1 requires shortlist revision |
| Direct homolog InDel task | `tasks/DIRECT_INDEL_001.md` | COMPLETE TASK | task specification for EV-A71 2C direct insertion/deletion mapping |
| EV-A71 direct InDel mapping | `docs/EV71_2C_DIRECT_INDEL_MAPPING_V1.md` | CURRENT DECISION LAYER | maps direct EV-A71 2C InDel phenotype to all 320 A89 junctions; final state `DIRECT_EVIDENCE_REQUIRES_SHORTLIST_REVISION` |
| All-junction metrics | `data/junction_structural_metrics_v2.tsv` | CURRENT DATA | regenerated quantitative structural metrics for all 320 junctions |
| Integrated candidate junction evidence | `data/candidate_junctions_v2.tsv` | CURRENT DATA | current V2 structure/function/conservation/rescue matrix; will not be overwritten by direct-evidence V3 |
| Integrated candidate junction evidence + direct InDel | `data/candidate_junctions_v3_direct_indel.tsv` | CURRENT DATA | V3 all-320 matrix with EV-A71 direct InDel layer appended; V2 preserved |
| EV-A71 direct InDel to A89 mapping | `data/evA71_2C_direct_indel_to_A89_v1.tsv` | CURRENT DATA | all-320 A89 junction projection of EV-A71 insertion/deletion/substitution context |
| EV-A71/A89 mature-2C alignment | `data/evA71_A89_2C_mafft_alignment_v1.fasta`, `data/evA71_A89_2C_alignment_map_v1.tsv` | CURRENT DATA | auditable mature-2C sequence alignment and residue mapping |
| HRV-A residue conservation | `data/hrvA_conservation_per_residue_v2.tsv` | CURRENT DATA | 321 A89-anchored V2 conservation rows |
| HRV-A junction conservation | `data/hrvA_conservation_per_junction_v2.tsv` | CURRENT DATA | 320 A89 junction rows with local-window and refined indel metrics |
| HRV-A/B/C context | `data/hrvABC_candidate_window_context.tsv` | CURRENT DATA | secondary broader-rhinovirus context; HRV-B/C sparse |
| CVB3→A89 functional mapping | `data/CVB3_to_A89_functional_mapping_v1.tsv` | CURRENT DATA | homolog mapping used for RNA/pore-function constraints |
| Structure integrity audit | `results/phase0_structure_integrity.tsv` | CURRENT RESULT | residue/chain/sequence integrity |
| Structure RMSD audit | `results/phase0_structure_rmsd.tsv` | CURRENT RESULT | monomer↔hexamer and model↔model structural correspondence |
| Junction analysis code | `scripts/analyze_insertion_junctions.py` | CURRENT SCRIPT | reproducible structural feature calculation |
| CONSERVATION_002 code | `scripts/build_conservation_002_panels.py`, `scripts/run_mafft_map_to_A89.py`, `scripts/calculate_conservation_v2.py`, `scripts/integrate_junction_evidence_v2.py` | CURRENT SCRIPT | VMR/MAFFT/conservation/integration hardening pipeline |
| DIRECT_INDEL_001 code | `scripts/direct_indel_001_map_ev71_to_a89.py` | CURRENT SCRIPT | source-table extraction, MAFFT mapping, direct InDel projection and V3 integration |
| Reference sequence | `references/HRV_A89_2C_reference_sequence.fasta` | CURRENT INPUT | authoritative 321-aa project sequence |
| Literature evidence registry | `references/LITERATURE_EVIDENCE_REGISTRY.md` | CURRENT | source-to-claim map and evidence boundaries; add verified EV-A71 direct InDel source during DIRECT_INDEL_001 |
| Direct InDel source records | `references/direct_indel_001/source_records_v1.tsv` | CURRENT PROVENANCE | source files, checksums and roles for DIRECT_INDEL_001 |
| Structure input provenance | `INPUT_PROVENANCE.md` | CURRENT | input role, checksums, storage policy |
| Project decisions | `DECISIONS.md` | CURRENT | decisions that should not silently drift |
| Next work | `TODO.md` | CURRENT | prioritized executable backlog |

## Superseded / provenance files

These remain in Git for scientific provenance. Do not use them as the current decision source unless comparing how the logic changed.

| File | Status | Superseded by / note |
|---|---|---|
| `docs/2C_FUNCTIONAL_EXCLUSION_MAP_V1.md` | SUPERSEDED | replaced by V2/V3 mapping and graded evidence logic |
| `docs/2C_FUNCTIONAL_EXCLUSION_MAP_V2.md` | SUPERSEDED | replaced by V3 A89-specific mapping |
| `docs/STRUCTURAL_SCREEN_PRELIMINARY_V1.md` | SUPERSEDED | replaced by V2 all-atom/rSASA/interface screen |
| `docs/CONSERVATION_SCREEN_V1.md` | PROVISIONAL / SUPERSEDED | replaced for decision-making by `docs/CONSERVATION_SCREEN_V2.md`; retained as CONSERVATION_001 provenance |
| `data/junction_structural_metrics_v1.tsv` | PROVENANCE DATA | regenerated as `data/junction_structural_metrics_v2.tsv`; V1 has 8 strict-flag/gate mismatches |
| `data/candidate_junctions_v1.tsv` | PROVISIONAL DATA | replaced for decision-making by `data/candidate_junctions_v2.tsv` |

`docs/2C_FUNCTIONAL_CONSTRAINT_MAP_V2.md` is intentionally retained as a supporting current document because it records direct positive-tolerance evidence and the literature-rescue track.

## Current analysis funnel

```text
4-structure input audit                       COMPLETE
        ↓
2C literature/function mapping                COMPLETE (working V3)
        ↓
320 peptide-junction WT structural screen     COMPLETE (V2)
        ↓
near-HRV conservation + natural indel         COMPLETE (V2)
        ↓
preliminary candidate shortlist               COMPLETE AS WORKING HYPOTHESIS
        ↓
EV-A71 direct 2C InDel fitness → A89 mapping  COMPLETE (V1)
        ↓
all-320 candidate re-audit                    CURRENT REVIEW GATE
        ↓
insertion-specific tag × site modeling        PENDING
        ↓
targeted MD of reduced constructs             LATER
        ↓
exact replicon nucleotide/RNA audit           PENDING / INPUT REQUIRED
        ↓
2–3 experimental constructs + controls        PENDING
        ↓
WT vs tagged replicon validation              EXPERIMENTAL GATE
```

## Current checkpoint result

The current structural/conservation analyses remain valid but are now treated as a preliminary site-discovery layer rather than the final shortlist authority.

The `287|288–290|291` cluster and `248|249` / `256|257` rescue controls remain working hypotheses. They must be allowed to be demoted or expanded after direct homolog insertion/deletion phenotype is mapped to all 320 A89 junctions.

DIRECT_INDEL_001 is complete with decision state `DIRECT_EVIDENCE_REQUIRES_SHORTLIST_REVISION`.

The current structural/conservation shortlist is no longer sufficient as a targeted modeling set because EV-A71 direct 2C handle-insertion scores are unfavorable for all mapped A89 junctions. Tag × Site modeling is not authorized until ChatGPT/user reviews this conflict and authorizes a reduced, revised task.
