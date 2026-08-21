# Project State

Last updated: 2026-08-21

Project: **HRV-A89 2C small-tag and insertion-site prioritization**

> The repository slug is historical. The project is **not HA-only**. The current question is joint prioritization of **small tag identity × internal insertion junction** for HRV-A89 2C.

## Scientific objective

Identify a small set of experimentally testable internal-tag constructs for HRV-A89 2C that minimize predicted perturbation of native 2C biology while remaining detectable in cell-based replicon/mechanism experiments.

The computational endpoint is **candidate prioritization**, not proof of a "safe" insertion site. WT-like replicon behavior remains the decisive biological acceptance gate.

## Fixed project constraints

- FLAG is excluded because the 9A5 antibody construct already uses FLAG; orthogonal detection is required.
- N- or C-terminal tagging is not assumed safe.
- The ranking unit is the peptide junction `i|i+1`, with both flanking residues and a local sequence/structure window evaluated.
- Homologous functional residues must be mapped to HRV-A89; residue numbers from PV/EV-A71/FMDV are not copied directly.
- Monomer-only exposure is insufficient. Candidate sites must be evaluated in both AlphaFold monomers and both hexamer ensembles.
- Current HRV-A89 hexamers are template-guided, no-membrane/no-RNA structural hypotheses and cannot by themselves establish native pore/RNA geometry.
- Final construct design must include the exact replicon nucleotide sequence and RNA-level checks.

## Current structural inputs

Four supplied structures have been audited and use a common HRV-A89 2C sequence and residue numbering 1–321:

| Input | Role | Audit result |
|---|---|---|
| `fold_hrv_2c_full_model_3.cif` | AlphaFold monomer source of the current lead hexamer | 321 aa; chain A; no residue gaps; sequence matches reference |
| `fold_hrv_2c_full_model_1.cif` | AlphaFold monomer source of the companion/control hexamer | 321 aa; chain A; no residue gaps; sequence matches reference |
| `selected_hexamer_01_md_representative.pdb` | current no-membrane lead hexamer | chains A–F; each 321 aa; no residue gaps |
| `selected_hexamer_02_md_representative.pdb` | companion/control hexamer | chains A–F; each 321 aa; no residue gaps |

Key C-alpha RMSD checks are recorded in `results/phase0_structure_rmsd.tsv` and summarized in `docs/METHOD_LOGIC_AUDIT_V2.md`.

## Phase status

| Phase | Status | Main deliverable | Current interpretation |
|---|---|---|---|
| 0. Input integrity / numbering / sequence / RMSD audit | **COMPLETE** | `results/phase0_structure_integrity.tsv`, `results/phase0_structure_rmsd.tsv` | four structures are mutually compatible for residue-level comparison |
| 1. 2C functional constraint/exclusion mapping | **COMPLETE, working V3** | `docs/2C_FUNCTIONAL_EXCLUSION_MAP_V3.md` | A89-specific annotations + homolog genetics/structures define hard/high-risk regions |
| 2. Four-structure all-atom junction screen | **COMPLETE, V2** | `docs/STRUCTURAL_SCREEN_V2.md`, `data/junction_structural_metrics_v1.tsv` | 320 junctions screened; no structurally clean junction is yet biologically low-risk |
| 3. Small-tag evidence screen | **COMPLETE, V1** | `docs/TAG_CANDIDATE_SCREEN_V1.md` | MAP8/HA/G196 lead the first modeling set; ranking remains site-dependent |
| 4. Near-HRV conservation / indel-tolerance layer | **NEXT / NOT YET FINALIZED** | planned conservation tables and report | decisive next evidence layer before tag × site modeling |
| 5. Candidate-junction shortlist | **PENDING** | planned ranked junction table | no junction currently designated safe/final |
| 6. Tag × site structural perturbation modeling | **PENDING** | planned construct models/metrics | only after the site set is reduced |
| 7. Replicon nucleotide/RNA audit | **BLOCKED ON INPUT** | planned RNA/codon audit | requires exact experimental 2C nucleotide sequence / replicon context |
| 8. Experimental construct recommendation | **PENDING** | 2–3 primary/backup constructs | requires evidence integration and later WT-vs-tagged validation |

## Current main result

The strict structural funnel starts from all **320 internal peptide junctions** and applies reproducible coil/exposure/interface gates across both AF monomers and all protomers in both hexamers.

Ten junctions pass the strict structural geometry gate:

`155|156`, `174|175`, `175|176`, `216|217`, `217|218`, `218|219`, `287|288`, `288|289`, `289|290`, `290|291`.

**None is currently promoted to a low-risk biological candidate.**

Reasons include:

- `155|156`: inside the 9A5 epitope and adjacent to the homolog-mapped aromatic pore/RNA-function position.
- `174|175`, `175|176`: immediately downstream of Walker B.
- `216|217`: touches motif-C N216.
- `217|218`, `218|219`: immediately adjacent to motif C within the SF3 ATPase core.
- `287|288` through `290|291`: favorable geometry, but located in the Cys/Zn-to-C-terminal bundle transition and not yet cleared by conservation/tag-specific modeling.

This is a negative-but-informative result: **surface-loop geometry alone is insufficient for 2C**.

## Functional map currently treated as authoritative

Current HRV-A89 working constraints include:

- N-terminal membrane/RNA/oligomerization context: graded high risk, not a blanket aa1–110 exclusion.
- SF3 domain: approximately aa94–254 as A89 UniProt/PROSITE context; core caution unless a stronger feature applies.
- Walker A / P-loop: aa124–131 `GSPGTGKS` — exclude.
- 9A5 epitope: aa148–160 `YSLPPDPKYFDGY` — exclude.
- Walker B: aa165–170 `VVIMDD` — exclude.
- motif-C neighborhood: aa210–216 `FVLASTN`, including N216 — exclude.
- R finger: R233/R234 — exclude.
- homolog-mapped RNA-binding/replication triad: A197/L199/K202 — strong exclusion/down-ranking.
- structural Zn region: C262/C273/C278 and aa262–278 context — high risk/exclude ligands.
- C-terminal RNA-binding: approximately aa305–312 by similarity — high risk.
- terminal oligomerization region: aa316–321 — exclude for first batch.

Evidence strength and caveats are documented in `docs/2C_FUNCTIONAL_EXCLUSION_MAP_V3.md`.

## Literature-rescue track

Historical poliovirus genetics reported viable small insertions after PV 2C residues 255 and 263. Explicit alignment maps these approximately to A89 junctions `248|249` and `256|257`.

These junctions are **not automatically preferred** because current A89 structural evidence places them in ordered/interface-sensitive neighborhoods. They are retained as a separate literature-rescue track so conflicting evidence is preserved rather than averaged away or discarded.

See `docs/2C_FUNCTIONAL_CONSTRAINT_MAP_V2.md`.

## Current tag shortlist

The tag layer is independent from the site layer.

| Tag | Design length | Current role | Main reason | Main concern |
|---|---:|---|---|---|
| MAP8 | 8 aa | primary modeling candidate | direct structure-guided internal-loop insertion evidence | 2C-specific tolerance unknown |
| HA | 9 aa | primary benchmark | mature WB/IP/IF ecosystem | not optimized for constrained loop insertion |
| G196 | 5 aa minimal; often 9 aa practical form | primary exploratory | smallest antibody-epitope footprint | minimal form may require flanking residues; weaker internal-loop evidence |
| AGIA | 9 aa | strong alternative | compact/high-affinity antibody system | constrained-loop evidence limited |
| ALFA | 13 aa core / 15 aa framed | secondary | highly orthogonal and sensitive | larger footprint; strong alpha-helical propensity |
| PA12 | 12 aa | context-limited | excellent direct turn/loop insertion evidence | human podoplanin-derived binder background risk in human-cell contexts |
| HiBiT | 11 aa | orthogonal quantitative reporter | high-sensitivity luminescence | not a universal antibody/IP/IF replacement |

FLAG is not considered further.

## Evidence hierarchy

Current working hierarchy:

`direct 2C genetics/biochemistry > experimental homolog structures > explicit A89 sequence alignment / A89 annotations > A89 monomer ensemble > A89 hexamer ensemble > near-HRV conservation > tag-specific modeling`

Conservation is a supporting layer, not a standalone safety criterion. Structure prediction of tagged constructs is a perturbation screen, not biological validation.

## Immediate next step

The next decisive analysis is **near-HRV conservation and indel tolerance**, with this hierarchy:

1. HRV-A sequences for quantitative conservation.
2. HRV-A/B/C for broader rhinovirus context.
3. EV/PV/other picornavirus mainly for homologous functional interpretation rather than a single pooled entropy score.

After this layer, produce a reduced junction shortlist and only then model MAP8/HA/G196 (plus alternatives if justified) at specific sites.

## Required future user input

Before final experimental construct design, obtain the **exact nucleotide sequence of the experimental HRV-A89 2C region / replicon plasmid**. Protein back-translation is not an acceptable substitute for RNA-structure/codon-level auditing.

## Scientific conclusion at this checkpoint

There is currently **no computationally certified safe insertion site and no final tag winner**. The project has, however, converted a vague tagging question into a constrained, reproducible decision problem with explicit negative evidence, functional boundaries, quantitative structural metrics and a defined next gate.
