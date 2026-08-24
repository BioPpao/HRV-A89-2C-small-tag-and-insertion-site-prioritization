# Project State

Last updated: 2026-08-24

Project: **HRV-A89 2C small-tag and insertion-site prioritization**

## Final Scientific Objective

Build a ranked, redundant, multi-junction x multi-tag experimental candidate panel for HRV-A89 2C internal tagging.

No computational result may be described as safe or experimentally validated.

## Current Project-Level State

`READY_FOR_FINAL_CANDIDATE_PANEL_REVIEW`

## Current Branch And Task

Branch:

`analysis/broad-dynamics-009`

Task:

`BROAD_DYNAMICS_AND_RECOVERY_009`

Primary specification:

- `tasks/BROAD_DYNAMICS_AND_RECOVERY_009.md`
- `tasks/BROAD_DYNAMICS_AND_RECOVERY_009_CONTINUATION.md`

Primary report:

- `docs/BROAD_DYNAMICS_AND_RECOVERY_009_REPORT.md`

## What Changed In Task 009

Task 009 completed the broad minimum-coverage dynamics layer.

- `248|249 x HA` OpenMM NaN remained classified as `MODEL_SPECIFIC_GEOMETRY_FAILURE`, not biological rejection.
- Disorder recovery remains low-evidence/fallback and is not decision-grade.
- PA14/AGIA exploratory modeling remained low-confidence and did not enter the final dynamics-retained core.
- WT plus 12 tagged `112-321` systems passed GROMACS preproduction.
- 39 / 39 production replicas completed and were analyzed at 20 ns each.
- Total analyzed production sampling: 780 ns.
- Trajectory QC exclusions: 0 / 39.
- Dynamic CA correlation/contact-network metrics were generated.
- Focused local multimer modeling completed computationally, but all model coordinates/confidence values were non-finite; the result is inconclusive.

## Current Authoritative 009 Outputs

- `results/broad_dynamics_009/production_manifest.tsv`
- `results/broad_dynamics_009/replica_completion.tsv`
- `data/dynamics_replica_qc_v1.tsv`
- `data/broad_dynamics_metrics_v1.tsv`
- `data/tag_exposure_dynamics_v1.tsv`
- `data/contact_persistence_dynamics_v1.tsv`
- `data/dynamic_network_perturbation_v1.tsv`
- `data/final_candidate_panel_v2_dynamics.tsv`
- `results/broad_dynamics_009/ranking_robustness_v2.tsv`
- `docs/DYNAMICS_QC_V1.md`
- `docs/DYNAMIC_NETWORK_ANALYSIS_V1.md`
- `docs/LOCAL_MULTIMER_RECOVERY_V2.md`

## Dynamics-Informed Candidate State

From `data/final_candidate_panel_v2_dynamics.tsv`:

- Tier A dynamics retained: 9 constructs.
- Tier B dynamics secondary: 1 construct.
- Controls after dynamics: 2 constructs.

Tier A retained:

- `289|290 x MAP8`
- `289|290 x G196_minimal`
- `288|289 x HA`
- `288|289 x MAP8`
- `290|291 x MAP8`
- `224|225 x HA`
- `224|225 x MAP8`
- `248|249 x MAP8`
- `203|204 x G196_minimal`

Tier B secondary:

- `248|249 x HA`

Controls:

- `256|257 x MAP8`
- `155|156 x MAP8`

## Important Caveats

- All candidates retain direct homolog EV-A71 InDel conflict; this remains a high-weight prior.
- The 20 ns dynamics layer is comparative perturbation evidence, not viral fitness evidence.
- Local multimer modeling is inconclusive because generated coordinates were non-finite.
- Tag exposure was assessed with a nonlocal heavy-atom distance proxy, not mature SASA.
- Exact experimental nucleotide/RNA context is still unavailable.
- No site or construct is safe or validated.

## Scheduler State

At the completion checkpoint, `squeue -u yukang` returned no active jobs.

The previous CPU watcher submitted duplicate backfill attempts after outputs were complete. Codex canceled watcher job `164379` and duplicate jobs `164556_0`, `164557_1`, `164558_2`, `164559_3`. This complicates Slurm job attribution for some rows, but trajectory endpoints and GROMACS logs verify the 20 ns outputs.

## Stop Gate

Stop after this task and wait for ChatGPT/user review.

Do not automatically proceed to:

- wet-lab construct synthesis/design;
- exact RNA/codon design;
- membrane/RNA/ATP/antibody mechanistic MD;
- long MD extension;
- experimental protocol design.

Before final nucleotide-level construct design, obtain the exact experimental HRV-A89 2C/replicon/plasmid nucleotide context.
