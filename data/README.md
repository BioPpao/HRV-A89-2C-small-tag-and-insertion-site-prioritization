# data/

Machine-readable analysis inputs and derived tables.

## Current files

- `junction_structural_metrics_v1.tsv` — structural metrics for all 320 HRV-A89 2C internal peptide junctions across the four-structure ensemble.
- `CVB3_to_A89_functional_mapping_v1.tsv` — explicit homolog mapping used for selected functional/RNA-related constraints.

## Planned files

See `../TODO.md` for the near-HRV conservation datasets and integrated candidate-junction table.

## Rules

- Keep raw numerical columns; do not store only a prose summary.
- Document the script/report that generated each dataset.
- Preserve accessions and sequence-filter metadata for downloaded conservation datasets.
- Version decision-changing datasets (`_v1`, `_v2`, ...).
- Do not treat model-derived columns as experimental evidence; the interpretation belongs in `docs/` and the evidence class in `references/LITERATURE_EVIDENCE_REGISTRY.md`.
