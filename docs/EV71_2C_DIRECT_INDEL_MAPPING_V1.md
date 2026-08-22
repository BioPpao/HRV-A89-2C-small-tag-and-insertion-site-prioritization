# EV71_2C_DIRECT_INDEL_MAPPING_V1

Status: **DIRECT_INDEL_001 complete**

Date: 2026-08-22

Decision state: `DIRECT_EVIDENCE_REQUIRES_SHORTLIST_REVISION`

## Bottom line

The EV-A71 direct experimental insertion/deletion dataset was acquired from processed source tables, verified against the experiment reference accession, aligned to HRV-A89 mature 2C with MAFFT, and projected onto all 320 HRV-A89 peptide junctions.

The direct insertion phenotype does **not** support the current HRV-A89 working shortlist. All 320 mapped A89 junctions have unfavorable EV-A71 2C insertional-handle scores; no mapped A89 junction has EV-A71 insertion score `>0`, and no new strict-gate-outside candidate is recovered by direct insertion fitness.

This is not an HRV-A89 validation result. It is a homolog direct-phenotype layer that argues the present shortlist must be reviewed before any Tag x Site modeling.

## Source verification

Primary publication:

- Bakhache W, Symonds-Orr W, McCormick L, Dolan PT. Deep mutation, insertion and deletion scanning across the Enterovirus A proteome reveals constraints shaping viral evolution. *Nature Microbiology* 10, 158-168. DOI `10.1038/s41564-024-01871-y`.

Processed data / code:

- Dryad dataset DOI `10.5061/dryad.866t1g1xm`, title `A comprehensive map of evolutionary constraints across the enterovirus A genome`.
- Dryad API version used: dataset version `311424`; file list includes `Dryad_Repository_InDel_Paper_v3.zip`, final resubmission zip, original zip and README.
- Source processed CSVs used from `https://github.com/QVEU/eva71_dimple.git`, commit `c99331a60980f68bb0141506e750e8339f278d08`, because Dryad individual file streams returned HTTP 401/403 in the execution environment.
- Read-mapping code provenance recorded from `https://github.com/QVEU/InDel_Toolkit.git`, commit `af12833cfc3644979bdbd20434a078dcc76d0bd0`.
- Raw read accession reported by publication: SRA BioProject `PRJNA1066851`.

Source records and checksums:

- `references/direct_indel_001/source_records_v1.tsv`
- `data/raw/direct_indel_001/`

## EV-A71 reference and 2C boundary

The source feature table `EV71_4643_Features.csv` identifies the experimental reference as:

- virus: `Enterovirus A71 Tainan/4643/98`
- accession: `MW298156`
- mature 2C nucleotide interval: `4079-5065`
- mature 2C length: 987 nt / 329 aa

The NCBI GenBank record was downloaded as `data/raw/direct_indel_001/MW298156.gb`. The extracted 2C sequence is stored at:

- `data/raw/direct_indel_001/MW298156_EV71_4643_2C.fasta`

The publication/source-script coordinate convention for 2C is:

- full polyprotein positions `1112-1440`
- mature EV-A71 2C coordinate = `full_polyprotein_position - 1111`

## Processed quantitative data used

The primary analysis used processed Enrich2 score tables rather than manually digitized figures:

| File | Role | Rows used for EV-A71 2C |
|---|---:|---:|
| `Scores_Insertional_Handle_Fullproteome.csv` | insertional-handle fitness | 329 |
| `Scores_Deletions_Fullproteome.csv` | `1AAdel`, `2AAdel`, `3AAdel` deletion fitness | 987 |
| `Fullproteome_P2_DMS_Enrich2_long.csv` | substitution context | 6,580 |
| `merged_df_indel_DMS.csv` | source merged cross-check/provenance | retained |

Insertion design is not mixed:

- primary insertion design: `SGRPGSLS`
- recorded as: `insertional_handle_SGRPGSLS`
- insertion length: 8 aa

Deletion lengths are stored separately as `1AAdel`, `2AAdel` and `3AAdel`. Substitution scores are kept as secondary context only.

## Alignment and mapping

Primary mature-2C alignment:

```text
mafft --localpair --maxiterate 1000 data/evA71_A89_2C_pair_v1.fasta
```

Outputs:

- `data/evA71_A89_2C_pair_v1.fasta`
- `data/evA71_A89_2C_mafft_alignment_v1.fasta`
- `data/evA71_A89_2C_alignment_map_v1.tsv`
- `results/direct_indel_001/evA71_A89_2C_mafft_v1.txt`

Mapping QC:

| Metric | Value |
|---|---:|
| A89 junction rows | 320 |
| `exact_aligned` | 315 |
| `gap_adjacent` | 0 |
| `ambiguous` | 5 |
| `unmapped` | 0 |
| A89 junctions with direct insertion score | 320 |

Ambiguous mapping rows are retained and not forced:

| A89 junction | EV-A71 source junctions | Note |
|---|---|---|
| `34|35` | `34|35;35|36` | multiple EV-A71 source junctions span the A89 junction |
| `70|71` | `71|72;72|73;73|74` | multiple EV-A71 source junctions span the A89 junction |
| `109|110` | `112|113;113|114;114|115` | multiple EV-A71 source junctions span the A89 junction |
| `142|143` | `147|148;148|149;149|150` | multiple EV-A71 source junctions span the A89 junction |
| `250|251` | `257|258;258|259` | current focal near-miss; mapping remains uncertain |

## Direct insertion evidence

The direct insertion score used here is the raw Enrich2 log2 score from the processed full-proteome table. The relative-fitness column is `2^score`.

Classification used only for review labels:

- `score > 0`: direct insertion tolerated in the source convention;
- `-2 <= score <= 0`: partly deleterious;
- `score < -2`: strongly deleterious.

Observed EV-A71 2C handle-insertion result after A89 mapping:

| Metric | Value |
|---|---:|
| A89 junctions with insertion score | 320 |
| Insertion score `>0` | 0 |
| Least-deleterious mapped A89 junction | `203|204` |
| Least-deleterious score | `-3.061137` |
| Least-deleterious relative fitness | `0.119814` |

Therefore there is no direct EV-A71 2C handle-insertion support for the existing HRV-A89 shortlist and no new direct-insertion-supported site outside the strict structural gate.

## Deletion context

Deletion evidence is included but not used alone to promote an insertion site.

Observed deletion-context summary:

| Metric | Value |
|---|---:|
| deletion context `score > 0` | 0 |
| deletion context between `-1` and `0` | 4 |
| deletion context strongly deleterious / unavailable | 316 |

The four partly deleterious deletion-context rows are:

| A89 junction | Best deletion context | Score | Insertion score |
|---|---|---:|---:|
| `167|168` | `1AAdel_right_residue` | `-0.924258` | `-5.595858` |
| `168|169` | `1AAdel_left_residue` | `-0.924258` | `-5.635963` |
| `248|249` | `1AAdel_right_residue` | `-0.288053` | `-5.693258` |
| `249|250` | `1AAdel_left_residue` | `-0.288053` | `-5.693258` |

This preserves the `248|249` conflict/rescue context but does not convert it into an insertion recommendation.

## Mandatory focal re-audit

| A89 junction | Structural track | Mapping | EV-A71 source junction | Insertion score | Relative fitness | Best deletion context | Integration |
|---|---|---|---|---:|---:|---|---|
| `223|224` | structural near-miss | exact | `230|231` | `-5.978036` | `0.015865` | `1AAdel_left_residue=-4.809236` | `experimental_conflict` |
| `245|246` | structural near-miss | exact | `252|253` | `-5.769187` | `0.018336` | `2AAdel_spanning_junction=-4.825452` | `experimental_conflict` |
| `248|249` | literature-rescue | exact | `255|256` | `-5.693258` | `0.019327` | `1AAdel_right_residue=-0.288053` | `experimental_conflict` |
| `250|251` | structural near-miss | ambiguous | `257|258;258|259` | `-5.711649` | `0.019082` | unavailable under ambiguous mapping | `mapping_uncertain` |
| `256|257` | literature-rescue | exact | `264|265` | `-5.527047` | `0.021687` | `1AAdel_right_residue=-5.067189` | `experimental_conflict` |
| `287|288` | strict structural pass | exact | `295|296` | `-5.521553` | `0.021769` | `1AAdel_right_residue=-4.781610` | `experimental_conflict` |
| `288|289` | strict structural pass | exact | `296|297` | `-5.152603` | `0.028113` | `1AAdel_left_residue=-4.781610` | `experimental_conflict` |
| `289|290` | strict structural pass | exact | `297|298` | `-3.518970` | `0.087234` | `3AAdel_spanning_option_2=-4.892835` | `experimental_conflict` |
| `290|291` | strict structural pass | exact | `298|299` | `-5.214399` | `0.026935` | `1AAdel_right_residue=-4.337596` | `experimental_conflict` |

`289|290` is the least deleterious of the current strict C-terminal cluster in EV-A71, but it remains strongly deleterious by the source score convention.

## Search outside the current strict structural set

The direct evidence was searched across all 320 A89 junctions.

No strict-gate-outside A89 junction had EV-A71 insertion score `>0`.

Least-deleterious outside-strict insertion rows:

| A89 junction | Functional tier | EV-A71 source junction | Insertion score | Relative fitness | Interpretation |
|---|---|---|---:|---:|---|
| `203|204` | HIGH_RISK | `210|211` | `-3.061137` | `0.119814` | least deleterious but still unfavorable |
| `224|225` | CORE_CAUTION | `231|232` | `-3.518970` | `0.087234` | unfavorable |
| `138|139` | HIGH_RISK | `143|144` | `-4.222270` | `0.053576` | unfavorable |
| `320|321` | EXCLUDE | `328|329` | `-4.644430` | `0.039984` | unfavorable and terminal/exclusion context |
| `214|215` | EXCLUDE | `221|222` | `-4.825647` | `0.035264` | unfavorable |

These are not promoted as candidates.

## Integrated V3 table

Main outputs:

- `data/evA71_2C_direct_indel_to_A89_v1.tsv`
- `data/candidate_junctions_v3_direct_indel.tsv`
- `results/direct_indel_001/direct_indel_001_focal_junctions.tsv`
- `results/direct_indel_001/direct_indel_001_outside_strict_candidates.tsv`
- `results/direct_indel_001/direct_indel_001_qc_summary.tsv`

Integration class counts:

| Class | Count |
|---|---:|
| `direct_experiment_unfavorable` | 301 |
| `experimental_conflict` | 14 |
| `mapping_uncertain` | 5 |
| `convergent_support` | 0 |
| `new_candidate_outside_strict_gate` | 0 |
| `no_direct_data` | 0 |

The V3 table preserves V2 structure/function/conservation/literature-rescue columns and appends direct InDel columns. No V2 file was overwritten.

## Interpretation boundaries

This task supports a review conclusion, not a construct conclusion:

- Direct EV-A71 2C insertion phenotype is stronger than WT structure/conservation proxies.
- It is still homolog evidence, not direct HRV-A89 replicon fitness.
- The insertional handle is 8 aa and has its own chemistry; it is informative for tag-sized insertions but is not identical to MAP8, HA, G196, AGIA, ALFA, PA12 or HiBiT.
- Ambiguous mappings remain marked and are not force-resolved by structure.
- Deletion tolerance is not equivalent to insertion tolerance.
- No HRV-A89 computational site is declared validated.

## Conclusion

`DIRECT_EVIDENCE_REQUIRES_SHORTLIST_REVISION`

Reason:

1. all 320 HRV-A89 junctions were covered;
2. 315/320 mappings are exact aligned and the mandatory focal strict cluster maps exactly;
3. every mapped EV-A71 2C handle-insertion score is unfavorable;
4. the current `287|288-290|291` cluster and `248|249` / `256|257` rescue controls lack direct homolog insertion support;
5. no new outside-strict candidate is strongly supported by direct insertion phenotype.

Recommended next review question for ChatGPT/user:

Should the project move to `NO_TARGETED_SITE` / targeted empirical insertion-library strategy, or keep a very small conflict-aware modeling set only as negative/contrast controls rather than supported candidates?
