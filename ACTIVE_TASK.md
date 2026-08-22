# Active task

Current task: `DIRECT_INDEL_001` — **COMPLETE / WAITING FOR CHATGPT-USER REVIEW**

Branch: `analysis/conservation-002`

Completed task specification:

`tasks/DIRECT_INDEL_001.md`

Primary completed outputs:

- `docs/DIRECT_INDEL_001_RUN_LOG.md`
- `docs/EV71_2C_DIRECT_INDEL_MAPPING_V1.md`
- `data/evA71_2C_direct_indel_to_A89_v1.tsv`
- `data/candidate_junctions_v3_direct_indel.tsv`
- `references/direct_indel_001/source_records_v1.tsv`

Decision state:

`DIRECT_EVIDENCE_REQUIRES_SHORTLIST_REVISION`

Repository role:

The GitHub repository is the shared project memory between ChatGPT and Codex. Decision-changing conclusions must be committed to the repository rather than left only in chat or terminal output.

Summary:

DIRECT_INDEL_001 mapped EV-A71 2C direct insertion/deletion/substitution phenotype to all 320 HRV-A89 peptide junctions.

Key result:

- EV-A71 reference/boundary verified: Tainan/4643/98, `MW298156`, mature 2C nt `4079-5065`, 329 aa.
- A89 mapping coverage: 320/320 junctions.
- Mapping classes: 315 `exact_aligned`, 5 `ambiguous`, 0 `unmapped`.
- Direct insertion design: 8 aa insertional handle `SGRPGSLS`.
- A89 junctions with EV-A71 2C insertion score `>0`: 0.
- New candidates outside strict structural gate with favorable direct insertion evidence: 0.
- Current strict C-terminal cluster `287|288-290|291` maps exactly but remains unfavorable by direct EV-A71 insertion phenotype.
- `250|251` remains mapping-uncertain.

Important constraints:

- Do not start Tag x Site modeling automatically.
- Do not start long MD, RNA/codon design, construct recommendation or experimental-final site selection.
- No candidate is considered safe, validated or experimentally proven for HRV-A89.
- A new task file is required before further execution.

Next gate:

ChatGPT/user review must decide whether to:

1. pivot to `NO_TARGETED_SITE` / targeted empirical insertion-library strategy;
2. retain only a small conflict-aware modeling/control set;
3. authorize a new optional method-hardening task.
