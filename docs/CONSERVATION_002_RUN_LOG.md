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
- Network during installation had intermittent TLS EOF warnings; micromamba retried and installation completed.

Environment records:

- `results/conservation_002_environment.tsv`
- `results/conservation_002_micromamba_list.tsv`
- `envs/hrv2c-conservation-qc.yml`

## Current Blockers / Risks

- The four original structural files listed in `INPUT_PROVENANCE.md` were not found in the current repository or under `/public/home/yukang/wf` at search depth 4. Structural V2 regeneration may be blocked unless the files are supplied or located elsewhere.

## Checkpoints

- Environment + framework checkpoint: pending.

## Next Action

Build V2 acquisition/taxonomy/MAFFT scripts and run sequence panels.
