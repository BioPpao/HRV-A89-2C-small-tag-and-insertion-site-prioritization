# TODO

Last updated: 2026-09-02

## Current Gate

Status: `SYNTHESIZED_PLASMID_BATCH_FROZEN`

The current eight-plasmid batch has already been synthesized and is recorded in:

- `data/synthesized_plasmid_panel_v1.tsv`
- `docs/SYNTHESIZED_PLASMID_PANEL_V1.md`

## Computational status

Task 011A is scientifically closed for current candidate prioritization.

Current interpretation to retain:

- `289|290 x MAP8`: strongest current computational primary candidate.
- `289|290 x G196_minimal`: strong same-site minimal-footprint comparator.
- `248|249 x MAP8`: useful independent-region comparator with conformation-sensitive hexamer caution.
- `248|249 x HA`: keep as synthesized; robust rigid-proxy hexamer-crowding caution.
- `289|290 x HA`: synthesized, but not formally classified in the Task 011A V7 12-row panel.

## Stop gate

Do **not** perform additional candidate selection or redesign for this synthesized batch.

Do **not** start generic long MD, blind docking, AF/ColabFold reruns, membrane/RNA/ATP mechanistic simulations, or new construct-expansion work unless the user explicitly opens a new scientific question.

The next meaningful project input is experimental readout from the synthesized constructs.
