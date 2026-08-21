# Input Provenance

Last updated: 2026-08-21

This file records the exact structural inputs used for the current insertion-junction analysis. Large structure files are not duplicated into this repository by default; provenance, role and checksums are tracked here so the analysis remains auditable.

## HRV-A89 2C reference sequence

Authoritative project sequence: `references/HRV_A89_2C_reference_sequence.fasta`

Length: **321 aa**.

All four structures below were verified to match this sequence and to use residue numbering 1–321 without gaps in the analyzed chains.

## Structure inputs

| File | Size | SHA256 | Role | Relationship |
|---|---:|---|---|---|
| `fold_hrv_2c_full_model_3.cif` | 212,640 bytes | `72646194d3207461c2642d33c8d0203d80a4e470dfebf7340876115cfd7456ea` | AlphaFold monomer | source monomer for the current lead hexamer route |
| `fold_hrv_2c_full_model_1.cif` | 212,640 bytes | `f94552edba44bd01fedfe5ea74e8627cc8e9c6fe20bd415ed21a7d3819a614a1` | AlphaFold monomer | source monomer for the companion/control hexamer route |
| `selected_hexamer_01_md_representative.pdb` | 2,435,910 bytes | `d6daf2cd8aa7db784561e85c5169e006a4c04b98ff68aebcdc63c6e34cfdc292` | no-membrane hexamer lead | A–F = HRV-A89 2C; current lead from the `HRV-Oligomers` project |
| `selected_hexamer_02_md_representative.pdb` | 2,435,910 bytes | `be28894e60a05269dbf6ad02c070e56fad7f51fc8b1e8cc20b98406821fb5a78` | companion/control hexamer | A–F = HRV-A89 2C; retained model uncertainty control |

Checksums above were calculated on the exact files supplied for the 2026-08-21 analysis session.

## Upstream provenance

The previous repository `BioPpao/HRV-Oligomers` records:

- `selected_hexamer_01_md_representative.pdb` as the current no-membrane lead derived from the `HAV_JCV_model_3` route and short/staged MD screening.
- `selected_hexamer_02_md_representative.pdb` as the companion/control derived from the `HAV_JCV_model_1` route.
- the lead and control are structural hypotheses rather than experimentally solved HRV-A89 assemblies.

The current tagging project reuses these models only as an ensemble for interface/exposure/pore-risk ranking. It does not inherit mechanistic conclusions automatically.

## Phase 0 integrity checks

See:

- `results/phase0_structure_integrity.tsv`
- `results/phase0_structure_rmsd.tsv`
- `docs/METHOD_LOGIC_AUDIT_V2.md`

Summary:

- both CIF monomers: chain A, residues 1–321, no gaps;
- both PDB hexamers: chains A–F, each residues 1–321, no gaps;
- all analyzed chains match the project reference sequence;
- AF model 1 and model 3 are nearly identical over the ATPase/C-terminal core and differ mainly in full-length/N-terminal placement;
- the selected hexamer protomers remain close to their source monomers after superposition.

## Storage policy

Track in Git:

- reference sequence;
- scripts;
- small/medium TSV/CSV/JSON outputs;
- analysis reports;
- selected lightweight derived files when useful.

Keep large generated trajectories and restart/state data outside normal Git:

- `.xtc`, `.trr`, `.cpt`;
- bulk `.gro`, `.tpr`, `.edr`;
- full generated MD run directories.

Representative structure files may be added later by an explicit curation decision (or Git LFS) if this repository is moved onto the same server workspace. They should not be silently duplicated from the upstream 25-GB `HRV-Oligomers` project.
