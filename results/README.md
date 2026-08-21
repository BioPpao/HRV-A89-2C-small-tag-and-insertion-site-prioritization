# results/

Compact, directly reported outputs from completed analysis stages.

## Current files

- `phase0_structure_integrity.tsv` — structure/chain/residue/sequence integrity audit.
- `phase0_structure_rmsd.tsv` — C-alpha RMSD correspondence across AF monomers and hexamer protomers.

These outputs support `../docs/METHOD_LOGIC_AUDIT_V2.md` and the authoritative checkpoint in `../PROJECT_STATE.md`.

## Rules

- Store final stage-level result tables here when they are compact and directly interpretable.
- Keep larger feature matrices in `../data/`.
- Every result should have a corresponding method/script or clearly documented derivation.
- Do not overwrite previous decision-changing versions; version them explicitly.
