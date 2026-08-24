# DYNAMIC_NETWORK_ANALYSIS_V2_AUDITED

Date: 2026-08-25

Status: `AUDITED_EXPLORATORY_CONTEXT`

Task 010 recomputed DCCM/contact-network summaries on PBC-corrected, native-CA fitted trajectories. Network evidence is retained as mechanistic context only; it is not allowed to determine candidate priority alone.

## Construct-Level Network Status

| construct_id                | junction   | tag_form     | network_status         | corrected_md_review_status   | md_caution_flags          |
|:----------------------------|:-----------|:-------------|:-----------------------|:-----------------------------|:--------------------------|
| A89_2C_289_290_MAP8         | 289\|290   | MAP8         | exploratory_replicated | md_neutral_or_supportive     | none                      |
| A89_2C_289_290_G196_minimal | 289\|290   | G196_minimal | exploratory_replicated | md_neutral_or_supportive     | none                      |
| A89_2C_288_289_HA           | 288\|289   | HA           | exploratory_unstable   | md_neutral_or_supportive     | none                      |
| A89_2C_288_289_MAP8         | 288\|289   | MAP8         | exploratory_replicated | md_neutral_or_supportive     | none                      |
| A89_2C_290_291_MAP8         | 290\|291   | MAP8         | exploratory_replicated | md_neutral_or_supportive     | none                      |
| A89_2C_224_225_HA           | 224\|225   | HA           | exploratory_replicated | md_caution                   | high_nonlocal_tag_contact |
| A89_2C_224_225_MAP8         | 224\|225   | MAP8         | exploratory_replicated | md_caution                   | high_nonlocal_tag_contact |
| A89_2C_248_249_MAP8         | 248\|249   | MAP8         | exploratory_replicated | md_neutral_or_supportive     | none                      |
| A89_2C_248_249_HA           | 248\|249   | HA           | exploratory_replicated | md_neutral_or_supportive     | none                      |
| A89_2C_203_204_G196_minimal | 203\|204   | G196_minimal | exploratory_replicated | md_caution                   | high_nonlocal_tag_contact |
| A89_2C_256_257_MAP8         | 256\|257   | MAP8         | exploratory_replicated | md_neutral_or_supportive     | none                      |
| A89_2C_155_156_MAP8         | 155\|156   | MAP8         | exploratory_replicated | md_caution                   | high_nonlocal_tag_contact |

## Interpretation Boundary

`exploratory_replicated` means the pairwise DCCM pattern passed a coarse replica-consistency screen. It does not prove preserved allostery or RNA/ATP function. `exploratory_unstable` rows, such as `288|289 x HA`, cannot use network metrics as support for priority promotion.
