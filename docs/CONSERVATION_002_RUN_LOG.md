# CONSERVATION_002 Run Log

Task: `CONSERVATION_002`

Branch: `analysis/conservation-002`

Starting commit: `817b9ecdfcb14e47e39888ca0f15598ec4ce3167`

Status: `IN_PROGRESS`

## Source Checks

- `git fetch origin` succeeded before work.
- Local `analysis/conservation-002` matched `origin/analysis/conservation-002`, ahead/behind `0/0`.
- Required files were read in order through `ACTIVE_TASK.md`, then `tasks/CONSERVATION_002.md`, V1 conservation report/run log, current reports, input provenance, evidence registry and TODO.

## Environment Setup

Existing state:

- No `conda`, `mamba`, `micromamba` or `mafft` on `PATH`.
- System Python 3.6.8 lacked Biopython, pandas, numpy and MDTraj.
- Existing env `/public/home/yukang/.conda/envs/hrv2c_hexamer` had Python 3.11.15, Biopython 1.87, pandas 2.3.3, numpy 2.4.6 and MDTraj 1.11.1, but no MAFFT and no conda/mamba executable.

Installation:

- Downloaded micromamba 2.9.0 from `https://micro.mamba.pm/api/micromamba/linux-64/latest` to `.tools/bin/micromamba`.
- Created project-local user-space environment `.tools/envs/hrv2c-conservation-qc`.
- Installed from conda-forge: Python 3.11, MAFFT, Biopython, pandas, numpy, MDTraj, gemmi and scipy.
- Added conda-forge `openpyxl` and `requests` for ICTV VMR Excel parsing and API retrieval.
- Network during installation had intermittent TLS EOF warnings; micromamba retried and installation completed.

Environment records:

- `results/conservation_002_environment.tsv`
- `results/conservation_002_micromamba_list.tsv`
- `envs/hrv2c-conservation-qc.yml`

## Data / QC Progress

- Downloaded ICTV current VMR `VMR_MSL41.v1.20260729.xlsx`.
- Extracted 80 HRV-A type rows under ICTV species `Enterovirus alpharhino`.
- Built V2 full type-balanced panel: 77 represented ICTV types.
- Built V2 expanded panel: 186 sequences.
- Built exact/high-confidence boundary subset: 5 sequences.
- Missing full-panel ICTV types: `A106`, `A107`, `A108`.
- Missing reasons: `A106` VMR record is partial polyprotein with extensive unknown residues; `A107` and `A108` VMR records are VP1 partial CDS only.
- Reconciled A1/A1A/A1B: VMR lists `A1` and `A1B`; V1 `A1A` exact UniProt record is mapped to ICTV `A1` and explicitly flagged.
- Ran MAFFT L-INS-i equivalent (`--localpair --maxiterate 1000`) for full, expanded and exact-boundary panels.
- Generated V2 residue/junction conservation tables and exact-boundary sensitivity tables.
- Regenerated structural metrics from the original structures after locating them under `/public/home/yukang/HRV Oligomers`.
- Structural V2 strict gate is internally consistent and returns the same 10 strict-pass junctions as the V1 report.
- Structural mismatch audit: 8 V1 rows had gate columns that computed as strict while stored `strict_structural_pass=False`; V2 recomputation is internally consistent and those rows are not strict.

## Current Blockers / Risks

- Exact/high-confidence boundary subset is small (`n=5`), so it is only a sensitivity layer and cannot replace the full ICTV type-balanced panel.
- Full V2 panel still has 3 missing ICTV types because source records did not contain acceptable 2C sequence.

## Checkpoints

- Environment + framework checkpoint: pending.
- Panel/alignment/metrics checkpoint: pending.

## Next Action

Write V2 reports and update project-state/navigation files.
