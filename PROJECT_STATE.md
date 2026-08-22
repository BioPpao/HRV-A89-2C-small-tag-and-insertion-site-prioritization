# Project State

Last updated: 2026-08-22

Project: **HRV-A89 2C small-tag and insertion-site prioritization**

> The project is not HA-only. The core question is joint prioritization of **small tag identity × internal insertion junction** for HRV-A89 2C.

## Scientific objective

Identify a small set of experimentally testable internal-tag constructs for HRV-A89 2C that minimize predicted perturbation of native 2C biology while remaining detectable in downstream mechanistic experiments.

The computational endpoint is **candidate prioritization**, not proof of a safe insertion site.

## Fixed project constraints

- FLAG is excluded because the 9A5 antibody construct already uses FLAG; orthogonal detection is required.
- N- or C-terminal tagging is not assumed safe.
- The ranking unit is peptide junction `i|i+1`, not an isolated residue.
- Homologous functional residues must be explicitly mapped to HRV-A89.
- Monomer-only exposure is insufficient; current site metrics use two A89 monomer models and two hexamer ensembles.
- Current A89 hexamers are template-guided no-membrane/no-RNA hypotheses and cannot establish native RNA-pore geometry by themselves.
- Conservation is supporting evidence, not proof of artificial insertion tolerance.
- Tagged-structure prediction is a perturbation screen, not biological validation.
- Exact RNA/codon analysis requires the real experimental nucleotide construct; protein back-translation is not an acceptable substitute.
- Decision-changing analyses must use mature reproducible software; missing tools should be installed in user space rather than silently replaced with weaker methods.

## Current structural inputs

Four audited inputs use a common HRV-A89 2C sequence and residue numbering 1–321:

| Input | Role | Audit result |
|---|---|---|
| `fold_hrv_2c_full_model_3.cif` | AlphaFold monomer / lead hexamer source | 321 aa, chain A, no residue gaps, sequence matches reference |
| `fold_hrv_2c_full_model_1.cif` | AlphaFold monomer / companion hexamer source | 321 aa, chain A, no residue gaps, sequence matches reference |
| `selected_hexamer_01_md_representative.pdb` | lead no-membrane hexamer | chains A–F, each 321 aa |
| `selected_hexamer_02_md_representative.pdb` | companion no-membrane hexamer | chains A–F, each 321 aa |

## Phase status

| Phase | Status | Main deliverable | Current interpretation |
|---|---|---|---|
| 0. Input integrity / numbering / RMSD audit | **COMPLETE** | `results/phase0_structure_integrity.tsv`, `results/phase0_structure_rmsd.tsv` | four structures are compatible for residue-level comparison |
| 1. 2C functional constraint/exclusion map | **COMPLETE, working V3** | `docs/2C_FUNCTIONAL_EXCLUSION_MAP_V3.md` | A89 annotations + homolog genetics/structures define hard/high-risk regions |
| 2. All-320 WT structural junction screen | **COMPLETE, V2** | `docs/STRUCTURAL_SCREEN_V2.md`, `data/junction_structural_metrics_v2.tsv` | internally consistent; 10 strict-pass junctions retained |
| 3. Small-tag evidence screen | **COMPLETE, V1** | `docs/TAG_CANDIDATE_SCREEN_V1.md` | MAP8/HA/G196 lead the first modeling layer; tag ranking remains site-dependent |
| 4A. HRV-A conservation / natural-indel screen | **PROVISIONANCE V1** | `docs/CONSERVATION_SCREEN_V1.md` | historical/provisional only |
| 4B. Conservation/taxonomy/structural QC hardening | **COMPLETE, V2** | `docs/CONSERVATION_SCREEN_V2.md`, `data/candidate_junctions_v2.tsv` | MAFFT/ICTV/indel/structural QC is decision-grade as a proxy layer |
| 5. Preliminary candidate shortlist | **WORKING HYPOTHESIS ONLY** | `docs/CANDIDATE_SHORTLIST_001_DECISION.md` | current cluster is not final because direct homolog InDel phenotype has not yet been integrated |
| 5B. Direct homolog insertion/deletion phenotype | **CURRENT / READY TO EXECUTE** | `tasks/DIRECT_INDEL_001.md` | map EV-A71 2C direct InDel fitness to all 320 A89 junctions and allow current shortlist to be overturned |
| 5C. Candidate re-audit after direct evidence | **PENDING** | planned V3 integrated table/report | identify convergent support, experimental conflicts and new candidates outside current structural gate |
| 6. Tag × site insertion-specific modeling | **PENDING** | planned construct ensembles/metrics | only after direct-evidence review |
| 7. Targeted MD | **LATER** | reduced construct set only | do not return to generic WT-only MD |
| 8. RNA/codon audit | **BLOCKED ON INPUT** | planned nucleotide-level analysis | exact experimental sequence/context required |
| 9. Experimental construct recommendation | **PENDING** | primary/backup/control set | requires integrated computation and biological validation |

## Current WT structural result

Ten junctions are strict structural passes after V2 regeneration:

`155|156`, `174|175`, `175|176`, `216|217`, `217|218`, `218|219`, `287|288`, `288|289`, `289|290`, `290|291`.

None is called low-risk or validated.

The previous eight V1 strict-flag/gate mismatches were resolved as V1 table/data-version inconsistencies; V2 is internally consistent.

## Current conservation result — V2

CONSERVATION_002 used an ICTV VMR HRV-A type universe, a 77-type full panel, 186-sequence expanded panel, a 5-sequence exact-boundary sensitivity subset and MAFFT L-INS-i-equivalent alignment.

Stable interpretation:

- `155|156`, `174|175`, `216|217` remain strongly disfavored;
- `175|176`, `217|218`, `218|219` remain unresolved;
- `287|288–290|291` remain the only current strict-pass cluster with V2 evolutionary support;
- `248|249` and `256|257` remain literature-rescue/conflict controls;
- `223|224`, `245|246`, `250|251` remain optional outside-strict review cases.

Important nuance: do not describe `287–291` as uniformly variable. `287|288` has conserved flanking residues despite a variable local window; `288|289`, `289|290` and `290|291` include strongly variable flanking residues.

## Why the previous shortlist is no longer sufficient by itself

The current pipeline still relies mainly on proxies for insertion tolerance:

- WT structural exposure/packing/interface geometry;
- known functional constraints;
- evolutionary substitution variability;
- natural indel context.

A higher-information evidence layer has been identified: a published EV-A71 proteome-scale deep insertion/deletion fitness dataset that includes 2C and measures viral fitness directly after insertion/deletion perturbation.

This direct homolog phenotype must be integrated before Tag × Site modeling because it can:

- support current candidates;
- contradict current structural/conservation predictions;
- recover candidate junctions outside the current strict structural gate;
- expose structural-threshold or confirmation bias.

## Current method-gap assessment

See `docs/METHOD_GAP_AND_NEXT_EVIDENCE_AUDIT_V1.md`.

Key remaining gaps:

1. no direct homolog 2C insertion-fitness layer in the current A89 matrix;
2. strict structural pass/fail may introduce hard-threshold bias;
3. entropy/identity are not phylogeny-aware insertion-tolerance measures;
4. WT loop geometry does not directly measure whether an inserted peptide can close with low strain;
5. protein-language-model insertion scoring is not yet used as an orthogonal sequence layer;
6. exact RNA-level constraints remain unresolved until the real experimental nucleotide construct is supplied.

## Updated evidence hierarchy

When evidence conflicts, use:

1. direct HRV-A89 insertion/replicon phenotype, if generated;
2. direct homolog 2C insertion/deletion phenotype with high-confidence A89 mapping;
3. direct 2C genetics/biochemistry and experimentally established functional motifs;
4. experimental homolog structures + explicit A89 mapping;
5. A89 structural ensemble metrics;
6. phylogeny-aware near-HRV evolutionary / natural-indel evidence;
7. protein-language-model scores;
8. tagged-structure / loop-modeling outputs as perturbation-ranking evidence.

No lower-level prediction should silently override stronger direct phenotype or a hard functional constraint.

## Current tag layer

The tag layer remains independent from the site layer.

| Tag | Design length | Current role | Main reason | Main concern |
|---|---:|---|---|---|
| MAP8 | 8 aa | primary modeling candidate | direct structure-guided internal-loop insertion evidence | 2C-specific tolerance unknown |
| HA | 9 aa | primary benchmark | mature WB/IP/IF ecosystem | not optimized for constrained loop insertion |
| G196 | 5 aa minimal; often 9 aa practical form | primary exploratory | smallest antibody-epitope footprint | minimal form may require flanks; weaker loop-insertion evidence |
| AGIA | 9 aa | strong alternative | compact/high-affinity system | constrained-loop evidence limited |
| ALFA | 13 aa core / 15 aa framed | secondary | orthogonal/sensitive | larger footprint; alpha-helical propensity |
| PA12 | 12 aa | context-limited | strong direct loop insertion evidence | human podoplanin-derived binder background risk |
| HiBiT | 11 aa | orthogonal quantitative reporter | high-sensitivity luminescence | not a universal antibody/IP/IF replacement |

FLAG remains excluded.

## Current working candidate hypotheses

These are **not final sites** and must be allowed to change after DIRECT_INDEL_001:

- `288|289` — strong current computational candidate;
- `289|290` — strong current computational candidate with C290/C-terminal-transition caution;
- `287|288`, `290|291` — secondary structural candidates;
- `248|249`, `256|257` — literature-rescue/conflict controls.

The direct homolog analysis must cover all 320 junctions and explicitly search for better sites outside this set.

## Immediate next step

Execute `tasks/DIRECT_INDEL_001.md`.

Expected outputs include:

- verified source/provenance records;
- EV-A71 mature 2C perturbation data;
- EV-A71→A89 junction mapping with mapping confidence;
- `data/evA71_2C_direct_indel_to_A89_v1.tsv`;
- `data/candidate_junctions_v3_direct_indel.tsv`;
- `docs/EV71_2C_DIRECT_INDEL_MAPPING_V1.md`;
- a final state of `DIRECT_EVIDENCE_SUPPORTS_TARGETED_SHORTLIST`, `DIRECT_EVIDENCE_REQUIRES_SHORTLIST_REVISION`, or `DIRECT_EVIDENCE_INSUFFICIENT_OR_MAPPING_LIMITED`.

Do not start Tag × Site modeling automatically after completion; ChatGPT/user review remains the next decision gate.
