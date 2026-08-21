# CONSERVATION_002 Data Sources

Retrieval date: `2026-08-21`.

## Official Type Universe

Source: ICTV Virus Metadata Resource current download.

- URL: `https://ictv.global/vmr/current`
- Resolved file: `https://ictv.global/sites/default/files/VMR/VMR_MSL41.v1.20260729.xlsx`
- Local copy: `data/ictv/VMR_current_2026-08-21.xlsx`
- Sheet: `VMR MSL41`
- Filter: `Species == Enterovirus alpharhino` and virus name matching `rhinovirus A#`
- Recognized HRV-A type rows extracted: 80

## Sequence Sources

Full type-balanced V2 panel:

- VMR GenBank nucleotide accessions were fetched from NCBI Nucleotide by E-utilities.
- Polyprotein translations were extracted from GenBank CDS annotations.
- 2C regions were inferred by local alignment of the authoritative A89 2C sequence to each VMR polyprotein translation.
- These records are marked `vmr_genbank_polyprotein_a89_local_alignment_provisional`.
- The project A89 reference sequence was used for ICTV type `A89` and as the coordinate anchor.

Exact/high-confidence subset:

- `repository_authoritative_2C` A89 reference.
- UniProt exact `Chain: Protein 2C` records retained from V1 for ICTV-reconciled types `A1`, `A1B`, `A2`, `A16` and `A89`.
- NCBI Protein mature-2C searches did not materially increase exact-boundary coverage; candidate hits were polyprotein records rather than standalone mature 2C products.

Missing ICTV types:

- `A106`: VMR accession `JQ245971` is a partial polyprotein record with a large unknown-residue block; no passing 2C extraction was accepted.
- `A107`: VMR accession `KC859319` is VP1 partial CDS only.
- `A108`: VMR accession `KC859318` is VP1 partial CDS only.

## Alignment Source

Primary V2 MSA:

- MAFFT v7.526 from conda-forge.
- Parameters: `--localpair --maxiterate 1000`.

The A89 reference sequence was mapped to alignment columns after MAFFT; it was not used to force independent pairwise alignment for each sequence.
