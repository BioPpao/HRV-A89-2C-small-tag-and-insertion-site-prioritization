# SYNTHESIZED_PLASMID_PANEL_V1

Date: 2026-09-02

Status: `SYNTHESIZED_PLASMID_BATCH_FROZEN`

Source: user-confirmed synthesized plasmid panel.

## Purpose

Record the eight HRV-A89 2C internal-tag plasmids that have already been synthesized. This is an experimental-status record, not a new computational ranking exercise.

The Task 011/011A 9A5-context analyses remain valid as interpretation layers, but they will **not** be used to redesign, replace, or expand this already synthesized eight-plasmid batch unless the user explicitly reopens construct selection later.

## Synthesized panel

| Order | Junction | Tag | Tag sequence | Original positioning | Current computational note |
|---:|---|---|---|---|---|
| 1 | 289|290 | MAP8 | GDGMVPPG | 当前主候选 | strongest current primary candidate in Task 011A review |
| 2 | 289|290 | G196_minimal | DLVPR | 最小 footprint 对照 | strong same-site minimal-footprint comparator |
| 3 | 248|249 | HA | YPYDVPDYA | 独立非 C 端区域 | synthesized as planned; Task 011A adds robust rigid-proxy hexamer-crowding caution |
| 4 | 248|249 | MAP8 | GDGMVPPG | 跨位点 MAP8 对照 | synthesized as planned; less persistently crowded than HA but conformation-sensitive |
| 5 | 288|289 | MAP8 | GDGMVPPG | 新增首选 | synthesized backup construct; current V7 Priority B |
| 6 | 288|289 | HA | YPYDVPDYA | 新增首选 | synthesized backup construct; current V7 Priority B |
| 7 | 290|291 | MAP8 | GDGMVPPG | 新增首选 | synthesized backup construct; current V7 Priority B |
| 8 | 289|290 | HA | YPYDVPDYA | 新增首选 | synthesized and recorded; not part of the formal 12-row Task 011A V7 panel, so no formal V7 9A5-context class is assigned |

## Relationship to Task 011A

Task 011A remains the current QC-hardened computational interpretation:

- `289|290 x MAP8` remains the strongest overall candidate.
- `289|290 x G196_minimal` remains a strong same-site comparator.
- `248|249 x MAP8` remains useful as an independent-region comparator but is conformation-sensitive in the rigid hexamer-transfer layer.
- `248|249 x HA` shows reproducible rigid-proxy hexamer crowding across three existing HA conformations; this is a caution for interpretation, not a reason to redesign the already synthesized plasmid.
- No Task 011A result proves biological compatibility, tag detectability, viral fitness, or experimental success.

## Project decision

For this eight-plasmid batch:

`NO_FURTHER_COMPUTATIONAL_CANDIDATE_SELECTION_OR_CONSTRUCT_REDESIGN_REQUIRED`

Further computation should only be opened if it answers a new scientific question after experimental data become available.

Machine-readable record:

- `data/synthesized_plasmid_panel_v1.tsv`
