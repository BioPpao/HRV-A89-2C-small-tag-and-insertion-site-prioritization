# EXPERIMENTAL_REVIEW_SHORTLIST_V1

Date: 2026-08-25

Status: `READY_FOR_EXPERIMENTAL_DISCUSSION`

Priority method: `multi_evidence_expert_adjudication`
Algorithmic total score used: `no`

No construct is safe or experimentally validated.

## Recommended 4 + 2 shortlist

|   shortlist_order | construct_id                | junction   | tag_form     | panel_role   | design_role                       | corrected_protocol_md_status   | experimental_review_annotation                     | scientific_purpose                                                                                                                  |
|------------------:|:----------------------------|:-----------|:-------------|:-------------|:----------------------------------|:-------------------------------|:---------------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------|
|                 1 | A89_2C_289_290_MAP8         | 289\|290   | MAP8         | candidate    | primary_C_terminal_MAP8           | md_neutral_or_supportive       | none                                               | direct corrected-protocol validation; C-terminal site leader                                                                        |
|                 2 | A89_2C_289_290_G196_minimal | 289\|290   | G196_minimal | candidate    | same_site_tag_identity_comparator | not_directly_validated         | not_directly_corrected_protocol_validated          | same 289\|290 site with alternative tag identity; not directly corrected-protocol validated                                         |
|                 3 | A89_2C_248_249_HA           | 248\|249   | HA           | candidate    | primary_non_C_terminal_HA         | md_neutral_or_supportive       | replica_heterogeneous_nonlocal_tag_contact_caution | independent non-C-terminal region; directly corrected-protocol validated; retain replica-contact heterogeneity caution when present |
|                 4 | A89_2C_248_249_MAP8         | 248\|249   | MAP8         | candidate    | crossed_site_tag_comparator       | not_directly_validated         | not_directly_corrected_protocol_validated          | 248\|249 site with MAP8; enables site x tag comparison; not directly corrected-protocol validated                                   |
|                 5 | A89_2C_224_225_MAP8         | 224\|225   | MAP8         | control      | conflict_control_MD_caution       | md_caution                     | none                                               | reproduced high nonlocal tag-contact caution under corrected protocol                                                               |
|                 6 | A89_2C_155_156_MAP8         | 155\|156   | MAP8         | control      | hard_negative_control             | md_caution                     | none                                               | independent functional exclusion plus reproduced corrected-MD caution                                                               |

## Design logic

The four candidate constructs deliberately span two biological regions and two tag identities rather than treating adjacent C-terminal junctions as independent hypotheses.

- C-terminal site hypothesis: `289|290` with MAP8 and G196_minimal.
- Non-C-terminal site hypothesis: `248|249` with HA and MAP8.
- Conflict control: `224|225 x MAP8`.
- Hard-negative control: `155|156 x MAP8`.

`248|249 x HA` remains Priority A but carries a replica-heterogeneous nonlocal-contact caution. `289|290 x G196_minimal` and `248|249 x MAP8` remain useful tag/site comparators but were not directly included in the corrected-protocol validation subset.

## Interpretation boundary

This is an experimental-review shortlist, not a final construct sequence, not a wet-lab protocol, and not evidence of viral fitness compatibility.
