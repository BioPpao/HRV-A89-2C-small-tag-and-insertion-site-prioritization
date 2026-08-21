# HRV-A 2C conservation and indel-tolerance screen V1

Status: **current CONSERVATION_001 report**.

Date: 2026-08-21

## 1. Scientific Question

This analysis asks which HRV-A89 2C peptide junctions show relatively low HRV-A evolutionary constraint, natural sequence variation, or natural indel signal, and whether that evidence supports, weakens, or leaves unresolved the prior structural/functional interpretation.

The endpoint is an auditable evidence matrix for all 320 internal peptide junctions. It is not selection of a computationally certified insertion site.

## 2. Dataset Construction and Provenance

Primary source: UniProtKB REST API, queried on 2026-08-21 for records under NCBI Taxonomy `147711` (Rhinovirus A) matching `protein_name:"Protein 2C"`.

Taxonomy source: NCBI Taxonomy E-utilities subtree query `txid147711[Subtree]`.

Project anchor: `references/HRV_A89_2C_reference_sequence.fasta`, retained as the authoritative A89 321-aa sequence.

Exact UniProt `Chain: Protein 2C` coordinates were used when available. Because exact mature-chain features were sparse, records lacking that annotation were retained only if A89 local-alignment extraction of the 2C region passed coverage and identity QC. These records are marked `a89_local_alignment_provisional` in metadata and are weaker than exact annotated mature products.

Provenance files:

- `references/CONSERVATION_DATA_SOURCES.md`
- `data/hrvA_2C_all_retrieval_metadata.tsv`
- `data/hrvA_2C_sequence_metadata.tsv`
- `data/hrvA_2C_expanded_metadata.tsv`
- `data/hrvA_2C_taxonomy.tsv`

## 3. Dataset / QC Statistics

HRV-A acquisition:

- UniProtKB records seen: 212.
- Retained expanded HRV-A 2C sequences: 113.
- Primary type-balanced HRV-A representatives: 78.
- Parsed HRV-A type labels from NCBI Taxonomy subtree: 83.
- Missing parsed type labels in the retained primary panel: `A1`, `A105`, `A106`, `A107`, `A108`.

HRV-A QC:

- Reference A89 length: 321 aa.
- Primary length range: 320-322 aa.
- Expanded length range: 320-322 aa.
- Internal stop records: 0.
- Unknown residues: 10 in primary, 15 in expanded.
- Primary type labels: 78.
- Expanded type labels: 78.

Secondary HRV-B/C context was sparse after applying the same boundary/QC rules:

- HRV-B retained: 3 primary / 3 expanded sequences.
- HRV-C retained: 3 primary / 3 expanded sequences.

Therefore HRV-B/C values are recorded as context only and should not be treated as a robust cross-species conservation estimate.

## 4. Alignment Method and A89 Mapping

MAFFT, Clustal Omega, MUSCLE, Kalign, BLAST and EMBOSS pairwise tools were not available on `PATH` in this execution environment. The run therefore used an A89 reference-guided fallback:

1. Extract or provisionally infer each 2C sequence.
2. Globally align each mature 2C sequence to the authoritative A89 2C sequence using in-repository Needleman-Wunsch.
3. Merge pairwise alignments into an A89-anchored alignment.
4. Preserve every A89 residue position 1-321 as an unambiguous alignment column.
5. Represent natural insertions between A89 residues as gap-slot columns between the flanking A89 residue columns.

This is a limitation compared with a mature MSA tool, but it preserves the project-critical A89 coordinate system and records the fallback explicitly.

Alignment outputs:

- `data/hrvA_2C_alignment.fasta`
- `data/hrvA_2C_expanded_alignment.fasta`
- `data/hrvA_2C_alignment_a89_mapping.tsv`
- `data/hrvA_2C_expanded_alignment_a89_mapping.tsv`
- `results/hrvA_2C_alignment_pairwise_qc.tsv`
- `results/hrvA_2C_expanded_alignment_pairwise_qc.tsv`

## 5. Conservation and Indel Methods

Residue-level metrics were calculated for exactly 321 A89-anchored residues.

Junction-level metrics were calculated for exactly 320 peptide junctions, `1|2` through `320|321`.

Entropy formula:

`H = -sum_i p_i log2(p_i)`, where `p_i` is the amino-acid frequency among known non-gap amino acids at that A89-anchored column.

Normalized entropy:

`H_norm = H / log2(20)`.

Gaps and unknown residues:

- Gaps are not included in amino-acid entropy.
- Gap frequency is tracked separately.
- Unknown residues are excluded from the amino-acid distribution and reduce effective count.

Junction window:

- Primary local window: junction +/-5 residues, implemented as A89 residues `i-5` through `i+1+5`, clipped to 1-321.

Natural indel metrics:

- Insertions: non-gap residues in alignment slot columns between A89 residues `i` and `i+1`.
- Local deletions: any gap at A89 residue columns within the junction +/-5 residue window.
- Natural indels are supporting evidence only and do not directly imply tolerance of an artificial peptide tag.

## 6. Whole-Protein Evolutionary Pattern

The HRV-A layer separates highly constrained ATPase/RNA/metal-associated features from more variable surface and transition regions.

Across all 320 junctions:

- HRV-A conservation class `conserved`: 69 junctions.
- `intermediate`: 107 junctions.
- `variable`: 97 junctions.
- `indel_signal`: 47 junctions.

These classes are descriptive bins used for interpretation. They are not calibrated fitness scores.

## 7. Functional-Motif Alignment Sanity Checks

Core feature placement was consistent with A89 coordinates. Representative type-weighted HRV-A results:

| A89 position | Feature | A89 aa | Identity | Entropy | Gap frequency |
|---:|---|---|---:|---:|---:|
| 124 | Walker A | G | 1.000 | 0.000 | 0.000 |
| 126 | Walker A | P | 1.000 | 0.000 | 0.000 |
| 129 | Walker A | G | 1.000 | 0.000 | 0.000 |
| 130 | Walker A | K | 1.000 | 0.000 | 0.000 |
| 148 | 9A5 epitope | Y | 1.000 | 0.000 | 0.000 |
| 156 | 9A5 / mapped aromatic pore warning | Y | 0.987 | 0.099 | 0.000 |
| 170 | Walker B | D | 1.000 | 0.000 | 0.000 |
| 197 | mapped RNA-related triad | A | 1.000 | 0.000 | 0.000 |
| 199 | mapped RNA-related triad | L | 1.000 | 0.000 | 0.000 |
| 202 | mapped RNA-related triad | K | 1.000 | 0.000 | 0.000 |
| 216 | motif C | N | 1.000 | 0.000 | 0.000 |
| 233 | R finger | R | 1.000 | 0.000 | 0.000 |
| 234 | R finger | R | 1.000 | 0.000 | 0.000 |
| 262 | Zn-related Cys | C | 1.000 | 0.000 | 0.000 |
| 273 | Zn-related Cys | C | 1.000 | 0.000 | 0.000 |
| 278 | Zn-related Cys | C | 1.000 | 0.000 | 0.000 |
| 305 | C-terminal RNA-binding region | E | 1.000 | 0.000 | 0.000 |
| 321 | C terminus | Q | 1.000 | 0.000 | 0.000 |

This supports the A89 mapping for conserved core features. Variable positions inside motif neighborhoods, such as Walker A S125 and C-terminal region residues around 312/316, do not override the existing functional constraints.

## 8. Strict Structural Track

The existing strict structural track remains the same 10 junctions:

`155|156`, `174|175`, `175|176`, `216|217`, `217|218`, `218|219`, `287|288`, `288|289`, `289|290`, `290|291`.

Conservation overlay:

| Junction | Functional tier | HRV-A class | Evolutionary layer effect | Type-weighted local identity | Type-weighted local entropy |
|---|---|---|---|---:|---:|
| 155|156 | EXCLUDE | conserved | weakens | 0.979 | 0.115 |
| 174|175 | HIGH_RISK | conserved | weakens | 0.921 | 0.291 |
| 175|176 | HIGH_RISK | intermediate | remains unresolved | 0.884 | 0.381 |
| 216|217 | EXCLUDE | intermediate | weakens | 0.748 | 0.535 |
| 217|218 | HIGH_RISK | intermediate | remains unresolved | 0.749 | 0.526 |
| 218|219 | HIGH_RISK | intermediate | remains unresolved | 0.767 | 0.463 |
| 287|288 | HIGH_RISK | variable | supports later review | 0.579 | 1.131 |
| 288|289 | HIGH_RISK | variable | supports later review | 0.541 | 1.194 |
| 289|290 | HIGH_RISK | variable | supports later review | 0.619 | 0.954 |
| 290|291 | HIGH_RISK | variable | supports later review | 0.571 | 1.063 |

No strict-pass junction becomes low-risk by conservation alone.

## 9. Structural Near-Miss Track

Near-miss definition used here:

- `strict_structural_pass != True`;
- does not touch a hard `EXCLUDE` functional tier;
- fails 1 or 2 existing structural gates.

The integrated table records `failed_gate_count` and `failed_gate_names` for every junction.

There are 45 structural near-miss junctions. Sixteen have HRV-A `variable` or `indel_signal` classes and merit later review only if ChatGPT decides to broaden the site set:

`50|51`, `66|67`, `67|68`, `68|69`, `113|114`, `220|221`, `221|222`, `222|223`, `223|224`, `243|244`, `244|245`, `245|246`, `250|251`, `291|292`, `292|293`, `293|294`.

Notable examples:

- `223|224`: CORE_CAUTION, fails burial gate only; HRV-A class variable. It remains between motif C and the R-finger in the SF3 core.
- `245|246`: CORE_CAUTION, variable; fails AF/hexamer coil gates and would disrupt structured backbone.
- `250|251`: CORE_CAUTION, indel signal; fails burial and inter-protomer distance gates, consistent with interface risk noted before.

## 10. Literature-Rescue Track

The literature-rescue track is preserved:

| Junction | Functional tier | Failed structural gates | HRV-A class | Interpretation |
|---|---|---|---|---|
| 248|249 | CORE_CAUTION | AF coil; hexamer coil; burial; inter-protomer distance | variable | rescue retained; conservation supports relative evolutionary variability but structure remains unfavorable |
| 256|257 | HIGH_RISK | AF coil; hexamer coil; AF rSASA; hexamer rSASA; inter-protomer distance | variable | rescue retained; conservation supports relative variability but high-risk transition context remains |

Neither junction is promoted. The correct conclusion is preserved conflict: historical poliovirus insertion tolerance plus HRV-A variability versus unfavorable A89 structural/functional context.

## 11. HRV-B/C Context

HRV-B/C context is recorded in `data/hrvABC_candidate_window_context.tsv`.

Because only 3 HRV-B and 3 HRV-C sequences passed the same boundary/QC workflow, this layer is weak. It is useful only as a check that some windows are not uniquely variable in HRV-A.

For the 287-291 region, HRV-B/C also show low identity to A89 in local windows, but the sequence count is too small for a strong cross-rhinovirus inference.

## 12. Integrated Evidence Conflicts

The integrated table `data/candidate_junctions_v1.tsv` preserves separate evidence columns rather than using a composite score.

Conflict examples:

- `155|156`: geometry passes, but conservation is high and functional evidence is EXCLUDE.
- `216|217`: geometry passes, but touches motif-C N216; evolutionary layer weakens.
- `248|249` and `256|257`: literature-rescue plus HRV-A variability conflict with A89 structure/functional risk.
- `287|288` to `290|291`: geometry and HRV-A variability support later review, but Zn/Cys-to-C-terminal transition context remains unresolved.

## 13. Priority Changes After Conservation

Increased for later review:

- `287|288`, `288|289`, `289|290`, `290|291`: strict structural pass plus HRV-A variability.
- Near-miss examples for possible later review: `223|224`, `245|246`, `250|251`, plus the other near-miss/variable rows listed above.

Decreased or further weakened:

- `155|156`: conserved 9A5/aromatic-pore-warning region.
- `174|175`: conserved Walker-B-adjacent window.
- `216|217`: motif-C contact remains dominant.
- All hard `EXCLUDE` features remain excluded regardless of local variability.

Unchanged / unresolved:

- `175|176`, `217|218`, `218|219`: intermediate conservation does not clear Walker B or motif-C adjacency.
- Literature-rescue sites remain conflicts rather than direct candidates.

## 14. New Candidate Outside the Strict 10

No new outside-strict junction is promoted as a low-risk candidate.

However, if ChatGPT chooses to broaden the later modeling set, the most reviewable outside-strict examples are:

- `223|224`: one failed structural gate, CORE_CAUTION, variable, but SF3 core location between motif C and R finger.
- `245|246`: variable, CORE_CAUTION, but non-coil structural issue.
- `250|251`: indel signal, CORE_CAUTION, but interface/burial risk and prior structural warning.

These are review candidates only, not cloning recommendations.

## 15. Limitations

- MAFFT was unavailable; alignment used a reference-guided fallback.
- Many UniProt records lack exact mature-chain coordinates; most HRV-A records are alignment-derived provisional extractions.
- HRV-B/C context is sparse after applying the same extraction/QC rules.
- Natural indels in a viral lineage do not prove tolerance of an artificial tag.
- Conservation is supporting evidence and cannot override direct functional constraints.
- Existing structural metric table has 8 rows where gate columns all pass but `strict_structural_pass=False`; this was recorded as `strict_flag_gate_mismatch=True` and not silently corrected.

## 16. Next Scientific Gate

ChatGPT/user should decide whether the next modeling shortlist should:

1. focus narrowly on the 287-291 strict-pass variable region plus literature-rescue controls;
2. add one or more outside-strict near-miss review sites such as `223|224`, `245|246`, or `250|251`;
3. treat the outcome as insufficient for targeted design and move toward an experimental insertion-library/minimal-epitope strategy.

The RNA/codon layer remains blocked until the exact experimental replicon nucleotide sequence is supplied.
