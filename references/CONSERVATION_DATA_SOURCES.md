# CONSERVATION_001 data sources

Retrieval date: `2026-08-21`.

## Primary source

- UniProtKB REST API, query `147711 AND protein_name:"Protein 2C"`.
- NCBI Taxonomy E-utilities subtree query `txid147711[Subtree]`.
- Project A89 authoritative FASTA: `references/HRV_A89_2C_reference_sequence.fasta`.

## Boundary rule

Exact UniProt `Chain: Protein 2C` coordinates were used when present. For records lacking mature-chain features, a provisional A89 local-alignment extraction was used only when coverage and identity QC passed. This fallback is weaker than annotated mature products and is marked in metadata.

## Output metadata

- `data/hrvA_2C_all_retrieval_metadata.tsv`
- `data/hrvA_2C_acquisition_summary.tsv`
- `data/hrvA_2C_taxonomy.tsv`
