# HRV-A 2C conservation and indel-tolerance screen V2

Status: **decision-grade QC hardening complete**.

Date: 2026-08-21

Decision state: `READY_FOR_SHORTLIST`

## 1. Why V1 Was Provisional

`CONSERVATION_001` produced useful full-length residue/junction tables, but it was not decision-grade because MAFFT was absent and the primary MSA used a custom A89-guided Needleman-Wunsch merge. It also used an NCBI-taxonomy-derived type universe, mixed exact and provisional 2C extractions, used an overly broad binary `indel_signal`, and exposed eight strict structural flag/gate mismatches in the V1 structural table.

V2 fixes the method-critical pieces before any tag x site modeling.

## 2. Software / Environment

Installed project-local user-space environment:

- prefix: `.tools/envs/hrv2c-conservation-qc`
- manager: micromamba 2.9.0
- channel: conda-forge
- Python 3.11.15
- MAFFT 7.526
- Biopython 1.88
- pandas 2.3.3
- numpy 2.4.6
- MDTraj 1.11.1
- gemmi 0.7.5
- scipy 1.17.1
- openpyxl 3.1.5
- requests 2.34.2

Records:

- `results/conservation_002_environment.tsv`
- `results/conservation_002_micromamba_list.tsv`
- `envs/hrv2c-conservation-qc.yml`

## 3. ICTV Type Universe

Source: ICTV current VMR, resolved on 2026-08-21 to `VMR_MSL41.v1.20260729.xlsx`.

Filter:

- sheet `VMR MSL41`
- `Species == Enterovirus alpharhino`
- virus name matching `rhinovirus A#`

Result:

- ICTV VMR HRV-A type rows: 80.
- V2 full type-balanced panel represented: 77.
- Missing full-panel types: `A106`, `A107`, `A108`.

Missing reasons:

- `A106`: VMR accession `JQ245971` is partial polyprotein with extensive unknown residues, so no passing 2C extraction was accepted.
- `A107`: VMR accession `KC859319` is VP1 partial CDS only.
- `A108`: VMR accession `KC859318` is VP1 partial CDS only.

A1/A1A/A1B reconciliation:

- VMR lists `A1` and `A1B`.
- V1 exact UniProt `A1A` was mapped to ICTV `A1` and explicitly flagged.
- `A1B` remains separate.

Outputs:

- `data/hrvA_type_universe_ictv.tsv`
- `data/hrvA_type_reconciliation_v2.tsv`

## 4. Sequence Provenance

V2 panels:

- Full type-balanced panel: 77 sequences.
- Expanded panel: 186 sequences.
- Exact/high-confidence boundary subset: 5 sequences.

Full panel provenance:

- 76 VMR GenBank polyprotein records with A89-local 2C extraction.
- 1 project authoritative A89 2C reference.

Expanded panel provenance:

- 76 VMR GenBank provisional extractions.
- 104 V1 retained provisional extractions reconciled to ICTV labels.
- 5 UniProt exact `Chain: Protein 2C` records.
- 1 project authoritative A89 reference.

Exact subset:

- A89 repository reference.
- UniProt exact-chain records for ICTV-reconciled `A1`, `A1B`, `A2`, `A16`, `A89`.

The exact subset is too small to replace the full panel. It is retained only as sensitivity evidence.

## 5. MAFFT Method and QC

Primary MSA method:

`mafft --localpair --maxiterate 1000`

Alignments:

- `data/hrvA_2C_alignment_v2.fasta`
- `data/hrvA_2C_expanded_alignment_v2.fasta`
- `data/hrvA_2C_exact_boundary_alignment_v2.fasta`

A89 mapping:

- `data/hrvA_2C_alignment_a89_mapping_v2.tsv`
- `data/hrvA_2C_expanded_alignment_a89_mapping_v2.tsv`
- `data/hrvA_2C_exact_boundary_alignment_a89_mapping_v2.tsv`

Core motif QC stayed anchored to the expected A89 coordinates. Conserved checks include Walker A G124/P126/G129/K130, 9A5 Y148/Y156, Walker B D170, RNA-related A197/L199/K202, motif-C N216, R233/R234, C262/C273/C278 and C-terminal Q321. Detailed values are in `results/conservation_002_motif_alignment_qc.tsv`.

## 6. V1 vs V2 Sensitivity

V2 keeps the main V1 interpretation stable while changing many old `indel_signal` labels after stricter indel categorization.

All-junction class counts in V2:

- `conserved`: 69
- `intermediate`: 113
- `variable`: 125
- `lineage_indel_supported`: 13

V1-vs-V2 table:

- `data/conservation_v1_v2_junction_comparison.tsv`
- 49 junctions changed categorical label, mostly because V1 `indel_signal` was split into transparent rare/recurrent categories.

The strict-pass focal interpretation is stable:

- `155|156` remains weakened/excluded.
- `174|175` remains weakened by conserved context.
- `175|176`, `217|218`, `218|219` remain unresolved.
- `216|217` remains weakened/excluded by motif C.
- `287|288` through `290|291` remain reviewable after QC, but still high-risk by C-terminal transition context.

## 7. Exact-Boundary Sensitivity

The exact/high-confidence subset has only 5 sequences, so exact-only metrics are not allowed to replace the full panel. V2 marks focal exact-boundary sensitivity as `unresolved_exact_subset_too_small`.

This does not invalidate the full-panel result; it means exact-boundary records are too sparse for independent quantitative confirmation.

## 8. Refined Indel Evidence

V2 replaces the broad V1 binary `indel_signal` with:

- `none`
- `singleton_or_rare`
- `recurrent_across_types`
- `broader_lineage_supported`

Rule:

`expanded_indel_category = category(max(insertion_type_count, local_deletion_type_count))`

where:

- 0 types: `none`
- 1 type: `singleton_or_rare`
- 2-4 types: `recurrent_across_types`
- 5 or more types: `broader_lineage_supported`

Raw type counts and type labels are retained in `data/hrvA_conservation_per_junction_v2.tsv`.

Important consequence: many V1 `indel_signal` calls were not recurrent after type-aware filtering. `248|249` remains lineage-indel-supported; `250|251` does not.

## 9. Structural Strict-Flag Mismatch Resolution

Structural metrics were regenerated from the original four audited structures found under `/public/home/yukang/HRV Oligomers`.

Outputs:

- `data/junction_structural_metrics_v2.tsv`
- `results/structural_v1_v2_gate_audit.tsv`

V2 strict-pass definition is internally consistent and returns the same 10 strict-pass junctions reported in `docs/STRUCTURAL_SCREEN_V2.md`:

`155|156`, `174|175`, `175|176`, `216|217`, `217|218`, `218|219`, `287|288`, `288|289`, `289|290`, `290|291`.

The eight V1 mismatch rows were:

`49|50`, `65|66`, `115|116`, `116|117`, `153|154`, `154|155`, `158|159`, `159|160`.

Audit conclusion: V1 stored gate columns computed as strict for these rows while stored `strict_structural_pass=False`. V2 recomputation is internally consistent and those rows fail V2 gates, so the mismatch is treated as a V1 table/data-version inconsistency rather than a new strict-pass set.

## 10. Revised Integrated Evidence

Integrated V2 table:

- `data/candidate_junctions_v2.tsv`

Priority counts:

- `reviewable_after_QC; structural pass plus V2 evolutionary support, functional context still required`: 4
- `literature-rescue retained`: 2
- `outside_strict_review_only`: 20
- `decreased_or_excluded; hard functional feature dominates`: 61
- `decreased; conserved local window`: 41
- `unchanged_or_unresolved`: 192

Focal junction summary:

| Junction | Track | Tier | V2 class | Effect | Flanking identity | Interpretation |
|---|---|---|---|---|---|---|
| 155|156 | strict | EXCLUDE | conserved | weakens | 1.000 / 0.987 | excluded; 9A5/aromatic warning dominates |
| 174|175 | strict | HIGH_RISK | conserved | weakens | 1.000 / 1.000 | conserved Walker-B-adjacent region |
| 175|176 | strict | HIGH_RISK | intermediate | unresolved | 1.000 / 0.494 | not rescued |
| 216|217 | strict | EXCLUDE | intermediate | weakens | 1.000 / 0.909 | motif-C N216 dominates |
| 217|218 | strict | HIGH_RISK | intermediate | unresolved | 0.909 / 0.195 | not rescued |
| 218|219 | strict | HIGH_RISK | intermediate | unresolved | 0.195 / 0.740 | not rescued |
| 223|224 | near-miss | CORE_CAUTION | variable | supports review only | 1.000 / 1.000 | outside-strict review only; SF3 core context |
| 245|246 | near-miss | CORE_CAUTION | variable | supports review only | 0.066 / 0.066 | outside-strict review only; structural issue remains |
| 248|249 | literature-rescue | CORE_CAUTION | lineage_indel_supported | supports conflict | 0.078 / 0.052 | rescue retained, not promoted |
| 250|251 | near-miss | CORE_CAUTION | variable | supports review only | 0.052 / 0.987 | outside-strict review only; interface risk remains |
| 256|257 | literature-rescue | HIGH_RISK | variable | supports conflict | 0.182 / 0.312 | rescue retained, not promoted |
| 287|288 | strict | HIGH_RISK | variable | supports review | 1.000 / 0.922 | reviewable; conserved flanks despite variable window |
| 288|289 | strict | HIGH_RISK | variable | supports review | 0.922 / 0.104 | reviewable; right flank variable |
| 289|290 | strict | HIGH_RISK | variable | supports review | 0.104 / 0.805 | reviewable; left flank variable |
| 290|291 | strict | HIGH_RISK | variable | supports review | 0.805 / 0.053 | reviewable; right flank variable |

## 11. Stable vs Changed Interpretations

Stable:

- The strict structural set remains 10 junctions.
- `155|156`, `174|175`, `216|217` remain weakened.
- `175|176`, `217|218`, `218|219` remain unresolved.
- `287|288` through `290|291` remain the only strict-pass region with V2 evolutionary support.
- `248|249` and `256|257` remain literature-rescue conflicts, not promoted sites.

Changed/refined:

- `248|249` now has explicit broader-lineage indel support.
- `250|251` loses the broad V1 `indel_signal`; it remains variable but not recurrent-indel-supported.
- Several V1 `indel_signal` calls are downgraded to `variable` or `intermediate` after type-aware filtering.
- `287–291` is not uniform: `287|288` has conserved flanking residues with a variable local window, while `288|289`, `289|290` and `290|291` include strongly variable flanking residues.

## 12. Shortlist Readiness

V2 supports `READY_FOR_SHORTLIST` in the narrow sense that the site layer is now methodologically hardened enough for ChatGPT/user to decide a reduced modeling set.

It does not authorize automatic tag modeling, and it does not declare any site low-risk.

Recommended review set for the next decision:

- Primary review cluster: `287|288`, `288|289`, `289|290`, `290|291`.
- Literature-rescue controls/conflicts: `248|249`, `256|257`.
- Optional outside-strict review controls if ChatGPT wants broader comparison: `223|224`, `245|246`, `250|251`.

If ChatGPT judges the C-terminal transition risk too high despite stable V2 support, `NO_TARGETED_SITE` remains a valid project-level conclusion.
