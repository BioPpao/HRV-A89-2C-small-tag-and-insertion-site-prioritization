# CONSERVATION_001 Run Log

Task: `CONSERVATION_001`

Branch: `analysis/conservation-001`

Starting commit: `f199651e9731e077e1b216cfde04816317d630bd`

Status: `IN_PROGRESS`

## Environment

Recorded in `results/conservation_001_environment.tsv`.

Initial observations:

- Python available: 3.6.8.
- `requests` available.
- Biopython not installed.
- `mafft`, `clustalo`, `muscle`, `kalign`, BLAST, EMBOSS `needle/water` not available on `PATH`.
- Alignment fallback selected: A89 reference-guided protein alignment using in-repository scripts.

## Source Checks

- `git fetch origin` succeeded with elevated permission.
- Local branch `analysis/conservation-001` matched `origin/analysis/conservation-001` at task start, ahead/behind `0/0`.
- Required source-of-truth files were read in order through `ACTIVE_TASK.md`, then task-specified reports/data/provenance.

## Failed Attempts / Fallbacks

- Initial NCBI request failed under sandbox network restriction: `Operation not permitted`; rerun with elevated permission succeeded.
- Initial UniProt probe had a shell quoting error; corrected and rerun.
- NCBI complete-genome GenBank probe found polyprotein CDS but no parseable `mat_peptide`/`Protein 2C` mature boundary in the sampled record.
- UniProt exact `Chain: Protein 2C` records exist but are sparse; records lacking exact chain annotations will be marked `a89_local_alignment_provisional` if they pass coverage/identity QC.

## Checkpoints

- Script/workflow checkpoint: pending.

## Next Action

Run acquisition for HRV-A primary/expanded panel and HRV-B/C secondary context.
