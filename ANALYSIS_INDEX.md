# Analysis Index

Last updated: 2026-08-21

This file is the navigation layer for the project. Read `PROJECT_STATE.md` first, then use the table below to find the current scientific source for each question.

## Current authoritative files

| Topic | Current file | Status | Use |
|---|---|---|---|
| Overall project state | `PROJECT_STATE.md` | CURRENT | authoritative checkpoint and next step |
| Methodological self-audit | `docs/METHOD_LOGIC_AUDIT_V2.md` | CURRENT | corrected logic, evidence hierarchy, Phase 0 summary |
| Functional exclusion/constraint map | `docs/2C_FUNCTIONAL_EXCLUSION_MAP_V3.md` | CURRENT | latest A89-specific functional map |
| Direct-tolerance conflict / rescue logic | `docs/2C_FUNCTIONAL_CONSTRAINT_MAP_V2.md` | CURRENT SUPPORTING | preserves historical PV insertion-tolerance evidence and conflicts |
| Four-structure structural screen | `docs/STRUCTURAL_SCREEN_V2.md`, `data/junction_structural_metrics_v2.tsv` | CURRENT | all-atom 320-junction structural funnel regenerated in CONSERVATION_002 |
| Small-tag evidence screen | `docs/TAG_CANDIDATE_SCREEN_V1.md` | CURRENT | tag-level literature ranking; not a construct ranking |
| HRV-A conservation / indel tolerance | `docs/CONSERVATION_SCREEN_V2.md` | CURRENT | MAFFT/ICTV-hardened near-HRV evolutionary layer |
| Candidate QC gate | `docs/CANDIDATE_JUNCTION_QC_V1.md` | CURRENT | concise next-decision gate after CONSERVATION_002 |
| All-junction metrics | `data/junction_structural_metrics_v2.tsv` | CURRENT DATA | regenerated quantitative structural metrics for all 320 junctions |
| Integrated candidate junction evidence | `data/candidate_junctions_v2.tsv` | CURRENT DATA | all 320 junctions with structural/function/conservation/rescue columns |
| HRV-A residue conservation | `data/hrvA_conservation_per_residue_v2.tsv` | CURRENT DATA | 321 A89-anchored V2 conservation rows |
| HRV-A junction conservation | `data/hrvA_conservation_per_junction_v2.tsv` | CURRENT DATA | 320 A89 junction rows with local-window and refined indel metrics |
| HRV-A/B/C context | `data/hrvABC_candidate_window_context.tsv` | CURRENT DATA | secondary broader-rhinovirus context; HRV-B/C sparse |
| CVB3→A89 functional mapping | `data/CVB3_to_A89_functional_mapping_v1.tsv` | CURRENT DATA | homolog mapping used for RNA/pore-function constraints |
| Structure integrity audit | `results/phase0_structure_integrity.tsv` | CURRENT RESULT | residue/chain/sequence integrity |
| Structure RMSD audit | `results/phase0_structure_rmsd.tsv` | CURRENT RESULT | monomer↔hexamer and model↔model structural correspondence |
| Junction analysis code | `scripts/analyze_insertion_junctions.py` | CURRENT SCRIPT | reproducible structural feature calculation |
| CONSERVATION_002 code | `scripts/build_conservation_002_panels.py`, `scripts/run_mafft_map_to_A89.py`, `scripts/calculate_conservation_v2.py`, `scripts/integrate_junction_evidence_v2.py` | CURRENT SCRIPT | VMR/MAFFT/conservation/integration hardening pipeline |
| Reference sequence | `references/HRV_A89_2C_reference_sequence.fasta` | CURRENT INPUT | authoritative 321-aa project sequence |
| Literature evidence registry | `references/LITERATURE_EVIDENCE_REGISTRY.md` | CURRENT | source-to-claim map and evidence boundaries |
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

`docs/2C_FUNCTIONAL_CONSTRAINT_MAP_V2.md` is intentionally retained as a **supporting current document**, not superseded, because it records direct positive-tolerance evidence and the literature-rescue track that should not be lost when applying stricter exclusion logic.

## Current analysis funnel

```text
4-structure input audit                       COMPLETE
        ↓
2C literature/function mapping                COMPLETE (working V3)
        ↓
320 peptide-junction all-atom screen          COMPLETE (V2)
        ↓
near-HRV conservation + indel tolerance       COMPLETE (V2, READY_FOR_SHORTLIST review)
        ↓
reduced candidate-junction shortlist          NEXT / PENDING CHATGPT DECISION
        ↓
small-tag × site perturbation modeling        PENDING
        ↓
exact replicon nucleotide/RNA audit           PENDING / INPUT REQUIRED
        ↓
2–3 experimental constructs + controls        PENDING
        ↓
WT vs tagged replicon validation              EXPERIMENTAL GATE
```

## Current checkpoint result

The regenerated structural screen identifies the same 10 strict-pass junctions. MAFFT/ICTV V2 conservation supports later review of `287|288` through `290|291` and preserves the `248|249` / `256|257` literature-rescue conflicts, but no final insertion site and no final tag have been selected.

The next decision is the reduced site set for tag × site modeling, or whether to pivot away from targeted computational site selection. Tag modeling is not authorized until ChatGPT/user reviews V2.
