# TODO

Last updated: 2026-08-24

Priority order is scientific, not cosmetic.

## Current Gate — Final Candidate Panel Review

Status: `READY_FOR_FINAL_CANDIDATE_PANEL_REVIEW`

Branch:

`analysis/broad-dynamics-009`

Completed task:

- `tasks/BROAD_DYNAMICS_AND_RECOVERY_009.md`
- `tasks/BROAD_DYNAMICS_AND_RECOVERY_009_CONTINUATION.md`

Primary report:

- `docs/BROAD_DYNAMICS_AND_RECOVERY_009_REPORT.md`

## Immediate Review Items For ChatGPT/User

1. Review the dynamics-informed panel:
   - `data/final_candidate_panel_v2_dynamics.tsv`
   - `results/broad_dynamics_009/ranking_robustness_v2.tsv`
2. Decide whether `248|249 x HA` should remain Tier B secondary after its dynamics penalty.
3. Decide how to balance C-terminal candidates against retained non-C-terminal rows `224|225`, `248|249 x MAP8` and `203|204 x G196_minimal`.
4. Decide whether high nonlocal tag-proximity/collapse proxy values for `224|225`, `203|204` and `155|156` require panel revision or just caution labels.
5. Decide whether additional controls are required before a final candidate-panel package.
6. Decide whether a 50 ns extension is scientifically needed, or whether the 20 ns broad screen is enough for the next review gate.

## Explicit Stop Gate

Do not start any new task until ChatGPT/user authorizes it.

Do not proceed automatically to:

- exact nucleotide/RNA/codon design;
- final wet-lab construct design;
- experimental protocol design;
- long MD extension;
- membrane/RNA/ATP/antibody mechanistic MD;
- antibody/binder-state modeling.

## Stable Previous Checkpoints

- `analysis/conservation-002`
- `analysis/candidate-panel-008`
- `analysis/broad-dynamics-009`

## Required Future Input

Before final nucleotide-level construct design, obtain the exact experimental HRV-A89 2C/replicon/plasmid nucleotide context.
