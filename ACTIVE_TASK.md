# Active Task

Current task: `BROAD_DYNAMICS_AND_RECOVERY_009` — **COMPLETED / WAITING FOR FINAL CANDIDATE PANEL REVIEW**

Branch: `analysis/broad-dynamics-009`

Primary task specification:

- `tasks/BROAD_DYNAMICS_AND_RECOVERY_009.md`
- `tasks/BROAD_DYNAMICS_AND_RECOVERY_009_CONTINUATION.md`

## Current State

`READY_FOR_FINAL_CANDIDATE_PANEL_REVIEW`

## Completion Evidence

- WT plus 12 tagged A89 2C `112-321` systems completed the 20 ns broad minimum-coverage screen.
- 39 / 39 replicas were analyzed.
- Total analyzed production sampling: 780 ns.
- Technical QC exclusions: 0 / 39.
- Focused local multimer recovery completed but was inconclusive because generated coordinates/confidence fields were non-finite.
- Dynamics, tag-exposure proxy, contact-persistence and dynamic-network outputs are now real trajectory-derived outputs, not placeholders.

## Primary Report

- `docs/BROAD_DYNAMICS_AND_RECOVERY_009_REPORT.md`

## Required Review Before Next Task

ChatGPT/user should review:

- `data/final_candidate_panel_v2_dynamics.tsv`
- `results/broad_dynamics_009/ranking_robustness_v2.tsv`
- `docs/BROAD_DYNAMICS_AND_RECOVERY_009_REPORT.md`
- `docs/DYNAMICS_QC_V1.md`
- `docs/DYNAMIC_NETWORK_ANALYSIS_V1.md`
- `docs/LOCAL_MULTIMER_RECOVERY_V2.md`

## Stop Gate

Do not automatically proceed to final construct design, RNA/codon design, long MD extension, membrane/RNA/ATP mechanistic MD, antibody/binder-state modeling or experimental protocol design.
