# GPU_RECOVERY_004_REPORT

Status: **GPU PLM recovery completed**

Final decision state: `READY_FOR_CONFLICT_AWARE_TAG_SITE_MODELING`

## Runtime

- Hostname: `gpu15`
- PyTorch: `2.4.1+cu118`
- CUDA available: `True`
- CUDA build: `11.8`
- CUDA device: `NVIDIA GeForce RTX 3090`

Execution notes:

- Direct login-node check on `admin1` had no visible GPU and is preserved in earlier Git provenance.
- Slurm job `164149` on `RTX3090-autoEM` remained unusable because of `PartitionConfig`; it was cancelled and preserved in Slurm logs.
- Slurm job `164150` reached `gpu15` but package installation from the compute node failed because pip was routed to an unavailable local proxy.
- PyTorch/fair-esm and ESM2 weights were then installed/downloaded in user space from the login context with network access; Slurm job `164151` reused that environment and completed.

## PLM method

- Model/checkpoint: `esm2_t6_8M_UR50D` from `fair-esm`.
- Scoring: full-sequence masked pseudo-log-likelihood.
- Raw score: full PLL sum.
- Normalized score: mean PLL per residue.
- V5 integration uses normalized insertion-minus-WT delta and preserves raw scores separately.
- Checkpoint source records and SHA256 checksums: `references/gpu_recovery_004_plm_source_records_v1.tsv`.
- Method limitation: ESM2 is not an experimental insertion-fitness assay and does not model RNA/polyprotein context.

## Completed rows

- Planned tag x junction rows: 1280.
- Completed rows: 1280.
- Tag forms: MAP8, HA, G196_minimal, G196_practical_GS.

## MAP8 / HA / G196 differences

Rank correlations are stored in `results/gpu_recovery_004/tag_landscape_correlations_v2.tsv`.

| tag_form_a | G196_minimal | G196_practical_GS | HA | MAP8 |
| --- | --- | --- | --- | --- |
| G196_minimal | 1 | 0.689825 | 0.506041 | 0.605315 |
| G196_practical_GS | 0.689825 | 1 | 0.600542 | 0.815687 |
| HA | 0.506041 | 0.600542 | 1 | 0.672132 |
| MAP8 | 0.605315 | 0.815687 | 0.672132 | 1 |

Top V5 PLM-context rows:

| junction | functional_tier | mapping_class | pareto_reviewable_subset_count | insertion_raw_log2_enrich2 | plm_percentile_mean | plm_percentile_min | best_tag_form | worst_tag_form | candidate_class_v5_plm_gpu |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 171|172 | HIGH_RISK | exact_aligned | 0 | -5.56995 | 0.990596 | 0.971787 | G196_minimal | HA | direct_homolog_conflicted_with_plm_context |
| 28|29 | HIGH_RISK | exact_aligned | 2 | -5.72522 | 0.971787 | 0.959248 | G196_practical_GS | MAP8 | plm_secondary_support_direct_homolog_conflicted |
| 172|173 | HIGH_RISK | exact_aligned | 0 | -5.67924 | 0.962382 | 0.902821 | MAP8 | HA | direct_homolog_conflicted_with_plm_context |
| 27|28 | HIGH_RISK | exact_aligned | 0 | -5.81951 | 0.954545 | 0.909091 | G196_minimal | HA | direct_homolog_conflicted_with_plm_context |
| 25|26 | HIGH_RISK | exact_aligned | 2 | -5.65543 | 0.953762 | 0.918495 | G196_minimal | HA | plm_secondary_support_direct_homolog_conflicted |
| 17|18 | HIGH_RISK | exact_aligned | 0 | -5.66024 | 0.934169 | 0.830721 | G196_minimal | HA | direct_homolog_conflicted_with_plm_context |
| 18|19 | HIGH_RISK | exact_aligned | 0 | -5.88673 | 0.924765 | 0.887147 | G196_minimal | MAP8 | direct_homolog_conflicted_with_plm_context |
| 24|25 | HIGH_RISK | exact_aligned | 2 | -5.74745 | 0.92163 | 0.890282 | G196_minimal | MAP8 | plm_secondary_support_direct_homolog_conflicted |
| 16|17 | HIGH_RISK | exact_aligned | 0 | -5.58039 | 0.920846 | 0.755486 | G196_minimal | HA | direct_homolog_conflicted_with_plm_context |
| 22|23 | HIGH_RISK | exact_aligned | 0 | -5.68861 | 0.914577 | 0.830721 | G196_minimal | HA | direct_homolog_conflicted_with_plm_context |

## Required re-audit rows

| junction | functional_tier | strict_structural_pass | insertion_raw_log2_enrich2 | plm_percentile_mean | plm_percentile_min | best_tag_form | worst_tag_form | candidate_class_v5_plm_gpu |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 203|204 | HIGH_RISK | False | -3.06114 | 0.18652 | 0.0752351 | MAP8 | G196_practical_GS | direct_homolog_conflicted_with_plm_context |
| 224|225 | CORE_CAUTION | False | -3.51897 | 0.148903 | 0.0376176 | MAP8 | G196_practical_GS | direct_homolog_conflicted_with_plm_context |
| 248|249 | CORE_CAUTION | False | -5.69326 | 0.646552 | 0.404389 | G196_minimal | G196_practical_GS | conflict_control_with_plm_context |
| 256|257 | HIGH_RISK | False | -5.52705 | 0.796238 | 0.601881 | G196_minimal | G196_practical_GS | conflict_control_with_plm_context |
| 287|288 | HIGH_RISK | True | -5.52155 | 0.657524 | 0.570533 | G196_minimal | MAP8 | conflict_control_with_plm_context |
| 288|289 | HIGH_RISK | True | -5.1526 | 0.643417 | 0.561129 | G196_minimal | MAP8 | conflict_control_with_plm_context |
| 289|290 | HIGH_RISK | True | -3.51897 | 0.548589 | 0.448276 | G196_minimal | HA | conflict_control_with_plm_context |
| 290|291 | HIGH_RISK | True | -5.2144 | 0.422414 | 0.354232 | G196_minimal | MAP8 | conflict_control_with_plm_context |

## Candidate ranking and review set

- Created `data/candidate_junctions_v5_plm_gpu.tsv` with all 320 junctions.
- Created `data/computational_review_set_v2_plm_gpu.tsv` as a revised computational review set.
- Direct homolog insertion phenotype remains a higher-weight conflicting evidence layer.
- No site is called safe or validated.

## Structural triage

Deferred. No mature reproducible structure-prediction or loop-remodeling workflow was installed without derailing the PLM recovery run.

## Blockers and uncertainties

- No remaining software/GPU blocker for the V2 GPU PLM scan.
- No HRV-A89-specific insertion phenotype exists.
- EV-A71 insertion data remain homolog and insertion-handle specific.
- Exact experimental RNA/codon context remains unavailable.
- PLM is secondary computational evidence and cannot validate a construct.

## Final decision state

`READY_FOR_CONFLICT_AWARE_TAG_SITE_MODELING`
