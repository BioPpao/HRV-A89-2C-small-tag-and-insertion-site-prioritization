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
- First full UniProt HRV-A retrieval timed out; script was patched to use smaller pages and retry/backoff.
- NCBI Taxonomy XML parsing initially included nested lineage taxons; script was patched to parse only direct returned `Taxon` elements.
- Existing `data/junction_structural_metrics_v1.tsv` contains 8 rows where current gate columns all pass but `strict_structural_pass=False`. The old table was not modified. `candidate_junctions_v1.tsv` records this as `strict_flag_gate_mismatch=True`; such rows are not called structural near-misses.

## Acquisition / QC

- HRV-A UniProtKB records seen: 212.
- HRV-A retained expanded sequences: 113.
- HRV-A primary type representatives: 78.
- HRV-A NCBI Taxonomy parsed type labels: 83.
- HRV-A missing parsed type labels in retained primary panel: A1, A105, A106, A107, A108.
- HRV-A QC: primary length range 320-322 aa; expanded length range 320-322 aa; internal stop records 0; unknown residues 10 primary / 15 expanded.
- HRV-B secondary context retained 3 primary / 3 expanded sequences.
- HRV-C secondary context retained 3 primary / 3 expanded sequences.

## Computation

- Alignment method used: A89 reference-guided Needleman-Wunsch fallback; MAFFT not available on `PATH`.
- Residue conservation table: 321 data rows.
- Junction conservation table: 320 data rows.
- Integrated candidate table: 320 data rows.
- Integrated junction key span: `1|2` through `320|321`; keys unique.

## Checkpoints

- Script/workflow checkpoint: `c2bb69b`, pushed.
- Dataset/alignment/metrics checkpoint: pending.

## Next Action

Write `docs/CONSERVATION_SCREEN_V1.md`, update project state/navigation files, then final checkpoint.
