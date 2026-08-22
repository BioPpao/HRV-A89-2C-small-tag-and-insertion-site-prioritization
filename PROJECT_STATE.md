# Project State

Last updated: 2026-08-22

Project: **HRV-A89 2C small-tag and insertion-site prioritization**

> The project is not HA-only. The core question is joint prioritization of **small tag identity × internal insertion junction** for HRV-A89 2C.

## Scientific objective

Identify a small set of experimentally testable internal-tag constructs for HRV-A89 2C that minimize predicted perturbation of native 2C biology while remaining detectable in downstream mechanistic experiments.

The computational endpoint is **relative candidate prioritization**, not proof of a safe insertion site.

## Current project-level decision state

`NO_HIGH_CONFIDENCE_TARGETED_SITE_YET`

The previous `287|288–290|291` C-terminal cluster is no longer supported as a targeted shortlist after direct EV-A71 2C insertion-fitness mapping. However, the homolog 8-aa insertion result is not treated as universal proof that every HRV-A89-specific MAP8/HA/G196 insertion must fail.

The next authorized phase is `METHOD_HARDENING_002`, which will re-rank all 320 junctions with continuous/Pareto evidence and add substitution-tolerance, phylogeny-aware independent-indel and tag-specific PLM layers before any Tag × Site structural modeling.

## Fixed project constraints

- FLAG is excluded because the 9A5 antibody construct already uses FLAG; orthogonal detection is required.
- N- or C-terminal tagging is not assumed safe.
- The ranking unit is peptide junction `i|i+1`, not an isolated residue.
- Homologous functional residues must be explicitly mapped to HRV-A89.
- Monomer-only exposure is insufficient; current site metrics use two A89 monomer models and two hexamer ensembles.
- Current A89 hexamers are template-guided no-membrane/no-RNA hypotheses and cannot establish native RNA-pore geometry by themselves.
- Conservation is supporting evidence, not proof of artificial insertion tolerance.
- Direct homolog insertion phenotype is a strong prior, not an absolute A89-specific binary veto.
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
| 2. All-320 WT structural junction screen | **COMPLETE, V2** | `docs/STRUCTURAL_SCREEN_V2.md`, `data/junction_structural_metrics_v2.tsv` | internally consistent; 10 strict-pass junctions retained as an annotation, not the future candidate funnel |
| 3. Small-tag evidence screen | **COMPLETE, V1** | `docs/TAG_CANDIDATE_SCREEN_V1.md` | MAP8/HA/G196 lead the first tag-specific layer; ranking remains site-dependent |
| 4A. HRV-A conservation / natural-indel screen | **PROVENANCE V1** | `docs/CONSERVATION_SCREEN_V1.md` | historical/provisional only |
| 4B. Conservation/taxonomy/structural QC hardening | **COMPLETE, V2** | `docs/CONSERVATION_SCREEN_V2.md`, `data/candidate_junctions_v2.tsv` | MAFFT/ICTV/indel/structural QC is decision-grade as a proxy layer |
| 5A. Preliminary candidate shortlist | **SUPERSEDED AS TARGETED SHORTLIST** | `docs/CANDIDATE_SHORTLIST_001_DECISION.md` | old C-terminal working cluster retained only as provenance/conflict controls |
| 5B. Direct homolog insertion/deletion phenotype | **COMPLETE, V1** | `docs/EV71_2C_DIRECT_INDEL_MAPPING_V1.md`, `data/candidate_junctions_v3_direct_indel.tsv` | all 320 A89 junctions mapped; EV-A71 8-aa insertion phenotype unfavorable across mapped landscape |
| 5C. Post-direct-evidence strategic review | **COMPLETE** | `docs/METHOD_GAP_AND_NEXT_EVIDENCE_AUDIT_V2.md` | direct evidence demotes old shortlist but does not prove universal A89 insertion impossibility |
| 5D. Method hardening / all-320 re-ranking | **AUTHORIZED / CURRENT** | `tasks/METHOD_HARDENING_002.md` | add substitution tolerance, continuous/Pareto ranking, independent-indel inference and tag-specific PLM |
| 6. Tag × site insertion-specific modeling | **BLOCKED PENDING 5D REVIEW** | planned loop/AF ensemble task | only after reduced conflict-aware set is authorized |
| 7. Targeted MD | **LATER** | reduced construct set only | do not return to generic WT-only MD |
| 8. RNA/codon audit | **BLOCKED ON INPUT** | planned nucleotide-level analysis | exact experimental sequence/context required |
| 9. Experimental construct recommendation | **PENDING** | primary/backup/control set | requires integrated computation and biological validation |

## Current WT structural result

Ten junctions are strict structural passes after V2 regeneration:

`155|156`, `174|175`, `175|176`, `216|217`, `217|218`, `218|219`, `287|288`, `288|289`, `289|290`, `290|291`.

None is called low-risk or validated.

The eight previous V1 strict-flag/gate mismatches were resolved as V1 data-version inconsistencies; V2 is internally consistent.

Important methodological change: `strict_structural_pass` is retained for reproducibility but will no longer determine candidate membership in the next all-320 analysis.

## Current conservation result — V2

CONSERVATION_002 used an ICTV VMR HRV-A type universe, a 77-type full panel, 186-sequence expanded panel, a 5-sequence exact-boundary sensitivity subset and MAFFT L-INS-i-equivalent alignment.

Stable interpretation:

- `155|156`, `174|175`, `216|217` remain strongly disfavored;
- `175|176`, `217|218`, `218|219` remain unresolved;
- `287|288–290|291` were the only strict-pass cluster with V2 evolutionary support before direct homolog phenotype was integrated;
- `248|249` and `256|257` remain literature-rescue/conflict controls;
- `223|224`, `245|246`, `250|251` remain useful near-miss examples for continuous re-ranking.

Conservation remains supporting evidence only. Type-aware V2 indel categories will be further hardened by independent-event inference in `METHOD_HARDENING_002`.

## Current direct homolog InDel result — V1

`DIRECT_INDEL_001` integrated the EV-A71 proteome-scale insertion/deletion/substitution phenotype before Tag × Site modeling.

Decision state from that task:

`DIRECT_EVIDENCE_REQUIRES_SHORTLIST_REVISION`

Key outputs:

- `docs/EV71_2C_DIRECT_INDEL_MAPPING_V1.md`
- `data/evA71_2C_direct_indel_to_A89_v1.tsv`
- `data/candidate_junctions_v3_direct_indel.tsv`
- `references/direct_indel_001/source_records_v1.tsv`
- `results/direct_indel_001/direct_indel_001_qc_summary.tsv`

Stable interpretation:

- EV-A71 reference verified as `MW298156` / Tainan/4643/98, mature 2C nt `4079-5065`, 329 aa;
- mature-2C MAFFT mapping covers all 320 HRV-A89 junctions;
- mapping classes: 315 `exact_aligned`, 5 `ambiguous`, 0 `unmapped`;
- ambiguous A89 junctions: `34|35`, `70|71`, `109|110`, `142|143`, `250|251`;
- the direct insertion design is the 8-aa handle `SGRPGSLS`;
- A89 junctions with EV-A71 2C insertion score `>0`: 0;
- no new outside-strict candidate is rescued by favorable direct insertion phenotype;
- the old `287|288–290|291` cluster maps exactly but is unfavorable by EV-A71 insertion phenotype;
- `248|249` retains historical/literature conflict but is not supported by the modern direct insertion layer.

Interpretation boundary:

This direct homolog phenotype is stronger than WT structure/conservation proxies, but it is not direct HRV-A89 validation and does not test MAP8/HA/G196 specifically. It is therefore a high-weight prior, not proof of universal A89 tag intolerance.

## Candidate roles after the full method audit

### `287|288`, `288|289`, `289|290`, `290|291`

Role:

`STRUCTURE_EVOLUTION_FAVORED__DIRECT_HOMOLOG_CONFLICT`

They remain informative conflict controls, not preferred targeted sites.

### `248|249`, `256|257`

Role:

`HISTORICAL_INSERTION_SUPPORT__MODERN_CONFLICT_CONTROL`

They preserve historical direct 2C insertion evidence but are not promoted as preferred A89 sites.

### Near-miss sites

`223|224`, `245|246`, `250|251` and all other non-hard-excluded junctions remain eligible for continuous/Pareto re-ranking. The previous strict gate alone will not permanently remove them from review.

## Current method-hardening task

See:

- `docs/METHOD_GAP_AND_NEXT_EVIDENCE_AUDIT_V2.md`
- `tasks/METHOD_HARDENING_002.md`

The task has four modules:

1. EV-A71 2C substitution-tolerance integration;
2. continuous/Pareto all-320 structural/evidence re-ranking;
3. phylogeny-aware independent natural-indel-event inference;
4. MAP8/HA/G196 tag-specific protein-language-model insertion scoring.

Primary planned output:

- `data/candidate_junctions_v4_method_hardening.tsv`

Primary report:

- `docs/METHOD_HARDENING_002_REPORT.md`

## Evidence hierarchy after audit V2

When evidence conflicts, use:

1. direct HRV-A89 insertion/replicon phenotype, if generated;
2. direct homolog 2C insertion phenotype with high-confidence A89 mapping;
3. direct homolog substitution/deletion phenotype and direct 2C genetics/biochemistry;
4. established functional motifs and experimental homolog structures with explicit A89 mapping;
5. A89 continuous structural-ensemble metrics;
6. phylogeny-aware HRV-A evolutionary / independent-indel evidence;
7. tag-specific PLM indel scores;
8. insertion-specific loop sampling and tagged AlphaFold/ColabFold ensembles;
9. targeted MD for a reduced construct set only.

No lower-level prediction may silently override stronger direct phenotype or a hard biological constraint.

## Current tag layer

| Tag | Design length | Current role | Main reason | Main concern |
|---|---:|---|---|---|
| MAP8 | 8 aa | primary tag-specific analysis candidate | direct structure-guided internal-loop insertion evidence | 2C-specific tolerance unknown |
| HA | 9 aa | primary benchmark | mature WB/IP/IF ecosystem | not optimized for constrained loop insertion |
| G196 | 5 aa minimal; often 9 aa practical form | primary minimal-footprint candidate | smallest antibody-epitope footprint | exact practical form/flanks must be fixed before PLM/structure work |
| AGIA | 9 aa | alternative | compact/high-affinity system | constrained-loop evidence limited |
| ALFA | 13 aa core / 15 aa framed | secondary | orthogonal/sensitive | larger footprint; alpha-helical propensity |
| PA12 | 12 aa | context-limited | strong direct loop insertion evidence | human podoplanin-derived binder background risk |
| HiBiT | 11 aa | orthogonal reporter | high-sensitivity luminescence | not a universal antibody/IP/IF replacement |

FLAG remains excluded.

## Immediate next step

Run `METHOD_HARDENING_002` on branch `analysis/conservation-002`.

Do not start Rosetta/AlphaFold/ColabFold Tag × Site modeling or MD automatically.

Return for ChatGPT/user review when the task reaches one of:

- `READY_FOR_CONFLICT_AWARE_TAG_SITE_MODELING`;
- `NO_HIGH_CONFIDENCE_TARGETED_SITE`;
- `METHOD_HARDENING_BLOCKED`.

## Required future user input

Before final construct recommendation, obtain the exact nucleotide sequence of the experimental HRV-A89 2C region / replicon plasmid. Protein back-translation is not an acceptable substitute for RNA/codon-level auditing.
