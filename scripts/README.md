# scripts/

Reproducible analysis code for the HRV-A89 2C small-tag/insertion-site project.

## Current script

### `analyze_insertion_junctions.py`

Purpose:

- parse the two AlphaFold monomers and two representative hexamers;
- calculate residue-level structural descriptors;
- aggregate those descriptors to peptide junctions `i|i+1`;
- generate the all-junction structural feature table used in `docs/STRUCTURAL_SCREEN_V2.md`.

The analysis includes secondary-structure context, solvent accessibility, monomer-vs-hexamer burial/interface metrics, inter-protomer proximity/contact information and a model-dependent pore/radial proxy.

## Requirements for future scripts

- preserve exact input filenames or expose them as command-line arguments;
- write machine-readable TSV/CSV output;
- record software/library versions when they can affect numerical results;
- use deterministic behavior unless stochastic modeling is scientifically necessary;
- preserve random seeds when stochastic methods are used;
- fail loudly on residue-number/sequence mismatches;
- do not silently overwrite supplied structures or prior decision-changing outputs;
- keep literature-derived functional rules separate from purely geometric calculations when possible.

The next major script family should handle near-HRV sequence acquisition/QC/alignment/conservation and should retain accession metadata for every sequence.
