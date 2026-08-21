# Project State

Last updated: 2026-08-21

Project: **HRV-A89 2C small-tag and insertion-site prioritization**

> The repository slug is historical. The project is **not HA-only**. The current question is joint prioritization of **small tag identity × internal insertion junction** for HRV-A89 2C.

## Scientific objective

Identify a small set of experimentally testable internal-tag constructs for HRV-A89 2C that minimize predicted perturbation of native 2C biology while remaining detectable in downstream mechanistic experiments.

The computational endpoint is **candidate prioritization**, not proof of a "safe" insertion site.

## Fixed project constraints

- FLAG is excluded because the 9A5 antibody construct already uses FLAG; orthogonal detection is required.
- N- or C-terminal tagging is not assumed safe.
- The ranking unit is the peptide junction `i|i+1`, with both flanking residues and a local sequence/structure window evaluated.
- Homologous functional residues must be mapped to HRV-A89; residue numbers from PV/EV-A71/FMDV are not copied directly.
- Monomer-only exposure is insufficient. Candidate sites must be evaluated in both AlphaFold monomers and both hexamer ensembles.
- Current HRV-A89 hexamers are template-guided, no-membrane/no-RNA structural hypotheses and cannot by themselves establish native pore/RNA geometry.
- Final RNA-level design requires the exact experimental nucleotide sequence/context; protein back-translation is not an acceptable substitute.
- Decision-changing analyses must use appropriate mature methods. Missing software should be installed in a reproducible user-space environment rather than silently replaced by a weaker method.

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
| 2. Four-structure all-atom junction screen | **COMPLETE, V2 REGENERATED** | `docs/STRUCTURAL_SCREEN_V2.md`, `data/junction_structural_metrics_v2.tsv` | V2 strict gate is internally consistent; original 10 strict-pass junctions remain |
| 3. Small-tag evidence screen | **COMPLETE, V1** | `docs/TAG_CANDIDATE_SCREEN_V1.md` | MAP8/HA/G196 lead the first modeling set; ranking remains site-dependent |
| 4A. Near-HRV conservation / indel-tolerance layer | **PROVENANCE V1** | `docs/CONSERVATION_SCREEN_V1.md`, `data/candidate_junctions_v1.tsv` | preserved as provisional history |
| 4B. Conservation / taxonomy / structural QC hardening | **COMPLETE, V2** | `docs/CONSERVATION_SCREEN_V2.md`, `data/candidate_junctions_v2.tsv` | MAFFT/ICTV/indel/structural QC supports `READY_FOR_SHORTLIST` for review, not automatic modeling |
| 5. Candidate-junction shortlist | **NEXT / PENDING CHATGPT REVIEW** | `docs/CANDIDATE_JUNCTION_QC_V1.md` | choose narrow strict-pass cluster plus rescue controls, broaden to near-misses, or decide `NO_TARGETED_SITE` |
| 6. Tag × site structural perturbation modeling | **PENDING** | planned construct models/metrics | only after the site set is reduced and approved |
| 7. RNA/codon audit | **BLOCKED ON INPUT** | planned RNA/codon audit | requires exact experimental nucleotide sequence/context |
| 8. Experimental construct recommendation | **PENDING** | primary/backup construct set | requires later evidence integration and biological validation |

## Current structural result

Ten junctions are strict structural passes after V2 regeneration:

`155|156`, `174|175`, `175|176`, `216|217`, `217|218`, `218|219`, `287|288`, `288|289`, `289|290`, `290|291`.

None is currently promoted to a low-risk biological candidate.

CONSERVATION_002 resolved the eight V1 strict-flag/gate mismatches. They were V1 table/data-version inconsistencies; V2 is internally consistent and does not add new strict-pass rows.

## Current conservation result — V2

`CONSERVATION_002` installed a user-space MAFFT environment, used ICTV VMR MSL41 as the type universe, built a 77-type V2 full panel, a 186-sequence expanded panel and a 5-sequence exact-boundary sensitivity subset.

The V2 evolutionary overlay supports:

- `155|156`, `174|175` and `216|217` remain strongly disfavored;
- `175|176`, `217|218` and `218|219` remain unresolved;
- `248|249` and `256|257` remain literature-rescue conflicts;
- `287|288` through `290|291` remain the only strict-pass cluster with V2 evolutionary support;
- no outside-strict junction is promoted, though `223|224`, `245|246` and `250|251` remain optional review controls.

## Focal region nuance

Do not describe `287–291` as uniformly variable. V2 shows `287|288` has conserved flanking residues despite a variable local window, whereas `288|289`, `289|290` and `290|291` include strongly variable flanking residues.

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

## Literature-rescue track

Historical poliovirus genetics reported viable small insertions after PV 2C residues 255 and 263. Explicit alignment maps these approximately to A89 junctions `248|249` and `256|257`.

These junctions remain a separate conflict/rescue track and are not automatically preferred.

## Current tag shortlist

The tag layer remains independent from the site layer.

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

ChatGPT/user should review `docs/CONSERVATION_SCREEN_V2.md` and `docs/CANDIDATE_JUNCTION_QC_V1.md`, then choose:

1. narrow modeling shortlist: `287|288`, `288|289`, `289|290`, `290|291` plus `248|249` and `256|257` as rescue/conflict controls;
2. broader comparison set adding `223|224`, `245|246`, `250|251`;
3. `NO_TARGETED_SITE` and pivot to insertion-library/minimal-epitope strategy.

Do not start Tag × Site modeling until that decision is explicitly authorized.
