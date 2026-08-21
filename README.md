# HRV-A89 2C small-tag and insertion-site prioritization

> **Repository slug note:** `HA-tag-insertion-site-prioritization` is a historical name. The current project is **not HA-only**. It jointly evaluates **small peptide tag identity × internal insertion junction** for HRV-A89 2C.

## Start here

For the current scientific state, read in this order:

1. [`PROJECT_STATE.md`](PROJECT_STATE.md) — authoritative project checkpoint.
2. [`DECISIONS.md`](DECISIONS.md) — active project-level decisions and evidence boundaries.
3. [`ANALYSIS_INDEX.md`](ANALYSIS_INDEX.md) — current vs superseded reports and data.
4. [`TODO.md`](TODO.md) — prioritized next analyses.
5. [`references/LITERATURE_EVIDENCE_REGISTRY.md`](references/LITERATURE_EVIDENCE_REGISTRY.md) — source-to-claim evidence map.

Codex/agent instructions are in [`AGENTS.md`](AGENTS.md).

## Scientific objective

Prioritize a small number of experimentally testable internal-tag constructs for **HRV-A89 2C (321 aa)** while minimizing predicted perturbation of:

- polyprotein processing;
- membrane-associated replication-complex behavior;
- SF3/AAA+-like ATPase function;
- 2C oligomerization;
- RNA-related function;
- the 9A5-binding/mechanism question;
- the viral RNA sequence/structure encoded by the final replicon construct.

The computational endpoint is **candidate prioritization**, not proof of a safe site. WT-like tagged-replicon behavior remains the decisive experimental acceptance gate.

## Fixed constraints

- **FLAG is excluded** because the 9A5 antibody construct already uses FLAG and orthogonal detection is required.
- HA is a benchmark, not the assumed best tag.
- Permanent N- or C-terminal tagging is not assumed safe.
- The ranking unit is the peptide junction `i|i+1`, not a single residue.
- Homolog residue numbers are explicitly mapped to HRV-A89 rather than copied directly.
- Monomer-only accessibility is insufficient: the current analysis uses **two AF monomers + two hexamer models**.
- Current project hexamers are no-membrane/no-RNA structural hypotheses, not experimentally solved native HRV-A89 assemblies.
- Final RNA/codon-level design requires the **exact experimental replicon nucleotide sequence**.

## Current status — 2026-08-21

### Completed

- **Phase 0:** four-structure integrity, numbering, sequence and RMSD audit.
- **Phase 1:** literature- and A89-annotation-informed 2C functional exclusion/constraint map.
- **Phase 2:** all-atom structural scan of all **320 internal peptide junctions**.
- **Tag layer V1:** evidence-based shortlist of MAP8, HA, G196, AGIA, ALFA, PA12 and HiBiT; FLAG removed.
- **Conservation layer V1:** HRV-A 2C conservation and indel-tolerance screen across all 321 residues / 320 junctions.

### Key checkpoint result

The strict four-structure structural funnel leaves **10 geometrically clean junctions**:

`155|156`, `174|175`, `175|176`, `216|217`, `217|218`, `218|219`, `287|288`, `288|289`, `289|290`, `290|291`.

However, **none is currently promoted to a low-risk biological site** because each conflicts with 2C functional evidence or high-risk structural context.

This is an important result: **a surface-exposed loop is not sufficient evidence for tagging 2C**.

The conservation layer used 78 primary type-balanced HRV-A representatives and 113 retained expanded HRV-A sequences. It supports later review of the variable `287|288` to `290|291` region, preserves `248|249` and `256|257` as literature-rescue conflicts, and does not promote a new outside-strict junction.

### Next decisive step

Decide the reduced site set for tag × site modeling, or decide that no targeted computational site is convincing enough and pivot to an insertion-library/minimal-epitope strategy.

Longer generic no-membrane MD is **not** the current priority.

## Current evidence hierarchy

`direct 2C genetics/biochemistry > experimental homolog structures > explicit A89 sequence mapping / A89 annotations > A89 monomer ensemble > A89 hexamer ensemble > near-HRV conservation > tag-specific modeling`

No single layer can certify a site as safe.

## Current tag evidence screen

| Tag | Length used for design | Current role | Main advantage | Main concern |
|---|---:|---|---|---|
| MAP8 | 8 aa | primary modeling candidate | direct internal-loop insertion evidence | 2C-specific tolerance unknown |
| HA | 9 aa | primary benchmark | mature WB/IP/IF ecosystem | not optimized specifically for constrained loops |
| G196 | 5 aa minimal; often 9 aa practical form | exploratory primary | smallest antibody-epitope footprint | minimal form may need flanks |
| AGIA | 9 aa | strong alternative | compact/high-affinity system | constrained-loop evidence limited |
| ALFA | 13 aa core / 15 aa framed | secondary | orthogonal/high-affinity | larger footprint and helical tendency |
| PA12 | 12 aa | context-limited | strong turn/loop insertion precedent | human podoplanin-derived background context |
| HiBiT | 11 aa | orthogonal reporter | very sensitive quantitative readout | not a universal IP/IF epitope replacement |

See [`docs/TAG_CANDIDATE_SCREEN_V1.md`](docs/TAG_CANDIDATE_SCREEN_V1.md) for the evidence and caveats.

## Repository layout

```text
.
├── README.md
├── PROJECT_STATE.md
├── ANALYSIS_INDEX.md
├── DECISIONS.md
├── TODO.md
├── INPUT_PROVENANCE.md
├── AGENTS.md
├── docs/
│   ├── METHOD_LOGIC_AUDIT_V2.md
│   ├── 2C_FUNCTIONAL_EXCLUSION_MAP_V3.md
│   ├── 2C_FUNCTIONAL_CONSTRAINT_MAP_V2.md
│   ├── STRUCTURAL_SCREEN_V2.md
│   ├── CONSERVATION_SCREEN_V1.md
│   ├── TAG_CANDIDATE_SCREEN_V1.md
│   └── older versioned reports retained for provenance
├── data/
│   ├── junction_structural_metrics_v1.tsv
│   ├── candidate_junctions_v1.tsv
│   ├── hrvA_conservation_per_residue.tsv
│   ├── hrvA_conservation_per_junction.tsv
│   ├── hrvABC_candidate_window_context.tsv
│   ├── CVB3_to_A89_functional_mapping_v1.tsv
│   └── README.md
├── results/
│   ├── phase0_structure_integrity.tsv
│   ├── phase0_structure_rmsd.tsv
│   └── README.md
├── scripts/
│   ├── analyze_insertion_junctions.py
│   └── README.md
└── references/
    ├── HRV_A89_2C_reference_sequence.fasta
    └── LITERATURE_EVIDENCE_REGISTRY.md
```

## Structural inputs and provenance

The current analysis uses:

- `fold_hrv_2c_full_model_3.cif` — AF source monomer of the lead hexamer;
- `fold_hrv_2c_full_model_1.cif` — AF source monomer of the companion/control;
- `selected_hexamer_01_md_representative.pdb` — lead no-membrane hexamer;
- `selected_hexamer_02_md_representative.pdb` — companion/control hexamer.

Exact sizes, SHA256 checksums and upstream provenance are recorded in [`INPUT_PROVENANCE.md`](INPUT_PROVENANCE.md). Large structures/trajectories are not duplicated into normal Git by default.

## Current scientific boundary

There is currently:

- **no computationally certified safe insertion site**;
- **no final tag winner**;
- **no final cloning recommendation**.

What is established is a reproducible filtering framework that preserves negative evidence and conflicts rather than forcing a convenient answer.
