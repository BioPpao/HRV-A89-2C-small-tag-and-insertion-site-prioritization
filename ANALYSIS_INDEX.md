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
| Four-structure structural screen | `docs/STRUCTURAL_SCREEN_V2.md` | CURRENT | all-atom 320-junction structural funnel |
| Small-tag evidence screen | `docs/TAG_CANDIDATE_SCREEN_V1.md` | CURRENT | tag-level literature ranking; not a construct ranking |
| All-junction metrics | `data/junction_structural_metrics_v1.tsv` | CURRENT DATA | quantitative metrics for all 320 junctions |
| CVB3→A89 functional mapping | `data/CVB3_to_A89_functional_mapping_v1.tsv` | CURRENT DATA | homolog mapping used for RNA/pore-function constraints |
| Structure integrity audit | `results/phase0_structure_integrity.tsv` | CURRENT RESULT | residue/chain/sequence integrity |
| Structure RMSD audit | `results/phase0_structure_rmsd.tsv` | CURRENT RESULT | monomer↔hexamer and model↔model structural correspondence |
| Junction analysis code | `scripts/analyze_insertion_junctions.py` | CURRENT SCRIPT | reproducible structural feature calculation |
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

`docs/2C_FUNCTIONAL_CONSTRAINT_MAP_V2.md` is intentionally retained as a **supporting current document**, not superseded, because it records direct positive-tolerance evidence and the literature-rescue track that should not be lost when applying stricter exclusion logic.

## Current analysis funnel

```text
4-structure input audit                       COMPLETE
        ↓
2C literature/function mapping                COMPLETE (working V3)
        ↓
320 peptide-junction all-atom screen          COMPLETE (V2)
        ↓
near-HRV conservation + indel tolerance       NEXT
        ↓
reduced candidate-junction shortlist          PENDING
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

The structural screen identifies 10 junctions with unusually clean four-structure geometry, but functional evidence prevents any of them from being called low-risk at this stage. No final insertion site and no final tag have been selected.

The next decision-changing analysis is near-HRV conservation; additional unconstrained MD is not the current priority.
