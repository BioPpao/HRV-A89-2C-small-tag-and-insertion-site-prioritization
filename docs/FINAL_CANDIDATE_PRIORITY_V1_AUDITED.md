# FINAL_CANDIDATE_PRIORITY_V1_AUDITED

Date: 2026-08-25

Status: `CANDIDATE_PRIORITY_PROVISIONAL_PENDING_CORRECTED_PROTOCOL_VALIDATION`

No construct is safe or experimentally validated.

## Top Priority List

| construct_id                | junction   | tag_form     | priority_class   | corrected_MD_status      | network_status         | rationale                                                                                                                                                                                        |
|:----------------------------|:-----------|:-------------|:-----------------|:-------------------------|:-----------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| A89_2C_289_290_MAP8         | 289\|290   | MAP8         | Priority_A       | md_neutral_or_supportive | exploratory_replicated | C-terminal leader for MAP8: comparatively least-deleterious EV-A71 homolog insertion among the audited C-terminal rows, favorable prior structural context, corrected MD neutral, tag SASA high. |
| A89_2C_289_290_G196_minimal | 289\|290   | G196_minimal | Priority_A       | md_neutral_or_supportive | exploratory_replicated | C-terminal leader for G196_minimal: same junction as MAP8 leader, corrected MD neutral, lower nonlocal tag contact than MAP8, preserves tag-form diversity.                                      |
| A89_2C_248_249_HA           | 248\|249   | HA           | Priority_A       | md_neutral_or_supportive | exploratory_replicated | Strongest non-C-terminal HA option: natural-indel/historical-conflict region, high tag SASA, corrected MD neutral; retained to prevent C-terminal-only panel collapse.                           |
| A89_2C_248_249_MAP8         | 248\|249   | MAP8         | Priority_A       | md_neutral_or_supportive | exploratory_replicated | Strongest non-C-terminal MAP8 backup: same diversified region as 248\|249 HA, corrected MD neutral and moderate PLM percentile, but oligomer context remains a conflict.                         |

## Backup List

| construct_id        | junction   | tag_form   | priority_class   | corrected_MD_status      | network_status         | rationale                                                                                                                                 |
|:--------------------|:-----------|:-----------|:-----------------|:-------------------------|:-----------------------|:------------------------------------------------------------------------------------------------------------------------------------------|
| A89_2C_288_289_MAP8 | 288\|289   | MAP8       | Priority_B       | md_neutral_or_supportive | exploratory_replicated | C-terminal backup: corrected MD neutral and MAP8-supported, but adjacent to 289\|290 and not an independent biological region.            |
| A89_2C_288_289_HA   | 288\|289   | HA         | Priority_B       | md_neutral_or_supportive | exploratory_unstable   | HA C-terminal backup: very high tag SASA and corrected MD neutral, but DCCM is exploratory/unstable and the site is adjacent to 289\|290. |
| A89_2C_290_291_MAP8 | 290\|291   | MAP8       | Priority_B       | md_neutral_or_supportive | exploratory_replicated | C-terminal neighbor backup: corrected MD neutral, but lower PLM percentile and no diversity gain beyond the 287-291 region.               |

## Controls

| construct_id                | junction   | tag_form     | priority_class        | corrected_MD_status      | network_status         | rationale                                                                                                                                                          |
|:----------------------------|:-----------|:-------------|:----------------------|:-------------------------|:-----------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| A89_2C_256_257_MAP8         | 256\|257   | MAP8         | Conflict_control      | md_neutral_or_supportive | exploratory_replicated | Conflict control: corrected MD is neutral and PLM is relatively favorable, but oligomer/function context remains unfavorable.                                      |
| A89_2C_224_225_MAP8         | 224\|225   | MAP8         | Conflict_control      | md_caution               | exploratory_replicated | Conflict control and validation target: corrected MD nonlocal-contact caution despite previous non-C-terminal interest.                                            |
| A89_2C_224_225_HA           | 224\|225   | HA           | Conflict_control      | md_caution               | exploratory_replicated | Conflict control: prior draft candidate, but corrected MD shows persistent nonlocal tag contact and structural/PLM layers are unfavorable.                         |
| A89_2C_203_204_G196_minimal | 203\|204   | G196_minimal | Conflict_control      | md_caution               | exploratory_replicated | Conflict control: direct homolog insertion is less severe than many sites, but functional/PLM/loop context and corrected MD nonlocal-contact flag are unfavorable. |
| A89_2C_155_156_MAP8         | 155\|156   | MAP8         | Hard_negative_control | md_caution               | exploratory_replicated | Hard negative control: functional exclusion/pore-like context and corrected MD nonlocal-contact caution; retained only for calibration.                            |

## Per-Tag Best Options

- MAP8: `289|290 x MAP8` is the strongest C-terminal MAP8 option; `248|249 x MAP8` is the strongest non-C-terminal MAP8 option.
- HA: `248|249 x HA` is the strongest non-C-terminal HA option; `288|289 x HA` is a C-terminal backup with high tag SASA but lower regional diversity.
- G196_minimal: `289|290 x G196_minimal` is the strongest audited G196_minimal option. `203|204 x G196_minimal` is retained only as a conflict control.

## Why Obvious Alternatives Were Not Selected

- `224|225 x HA/MAP8`: corrected MD found persistent nonlocal tag contact; structure/PLM layers are also unfavorable, so these rows are controls rather than priority candidates.
- `203|204 x G196_minimal`: direct homolog insertion is relatively less severe, but functional/PLM/loop context and corrected MD are unfavorable.
- `256|257 x MAP8`: corrected MD is neutral and PLM is moderate, but oligomer/function context remains unfavorable; retained as conflict control.
- Adjacent C-terminal rows `288|289`, `289|290`, and `290|291` are one biological region for diversity reporting.

## Evidence Boundary

Direct HRV-A89 insertion phenotype is absent. EV-A71 direct insertion fitness is homolog evidence and remains unfavorable for all mapped A89 junctions. Corrected MD is comparative apo core-fragment perturbation evidence only and cannot establish viral fitness, tag detectability in cells, RNA compatibility, or safety.

## 20 ns And 50 ns

Corrected 20 ns reanalysis is sufficient for a provisional screening panel because all 39 legacy trajectories were usable after PBC correction and representative RMSD cross-validation passed. There is no scientific reason to extend all 39 systems to 50 ns. Further sampling should be limited to the corrected-protocol validation subset and only extended if drift, replica disagreement, or rank instability persists.

## Before Nucleotide-Level Design

The exact experimental HRV-A89 replicon/plasmid nucleotide sequence is still required for codon, RNA-structure, cryptic-processing and construct-boundary review.
