# ONE_SHOT_COMPUTATIONAL_AUDIT_003 run log

Task: `ONE_SHOT_COMPUTATIONAL_AUDIT_003`

Branch: `analysis/conservation-002`

Starting commit: `518a904`

Status: `IN_PROGRESS`

Date: 2026-08-22

## Scope

Execute the authorized unattended computational audit through mandatory stages A-D and F, with optional Stage E attempted only if a mature reproducible method is available without derailing the run.

No long MD, experimental protocol design, final construct recommendation, final RNA/codon design, or HRV-A89 safe/validated-site claim is authorized.

## Required read checkpoint

Read in the task-specified order:

1. `AGENTS.md`
2. `WORKFLOW.md`
3. `PROJECT_STATE.md`
4. `ACTIVE_TASK.md`
5. `tasks/ONE_SHOT_COMPUTATIONAL_AUDIT_003.md`
6. `tasks/METHOD_HARDENING_002.md`
7. `docs/METHOD_GAP_AND_NEXT_EVIDENCE_AUDIT_V2.md`
8. `docs/EV71_2C_DIRECT_INDEL_MAPPING_V1.md`
9. `docs/CONSERVATION_SCREEN_V2.md`
10. `DECISIONS.md`
11. `ANALYSIS_INDEX.md`
12. `TODO.md`

## Initial Git state

- `git fetch origin`: completed.
- Branch: `analysis/conservation-002`.
- Remote comparison: `0 0` for `HEAD...origin/analysis/conservation-002`.
- Starting working tree: clean.

## Software/environment setup

Created user-space environment:

- path: `.tools/envs/hrv2c-one-shot`
- manager: micromamba 2.9.0
- channels: conda-forge, bioconda
- environment export: `envs/hrv2c-one-shot.yml`
- package list: `results/one_shot_003/one_shot_003_micromamba_list.tsv`

Core tool versions:

- Python 3.11.15
- pandas 3.0.5
- Biopython 1.88
- numpy 2.4.6
- scipy 1.17.1
- scikit-learn 1.9.0
- MAFFT 7.526
- FastTree 2.2.0
- IQ-TREE 3.1.3

GPU/PLM check:

- `nvidia-smi`: not found in PATH.
- `/dev/nvidia*`: no visible NVIDIA device files.
- `/proc/driver/nvidia/gpus`: absent.
- Existing environments checked: no `torch`, no `transformers`, no `esm`.
- Attempted to install `torch transformers safetensors` into `.tools/envs/hrv2c-one-shot`; platform escalation was rejected with usage-limit message. This is recorded as a PLM software blocker unless an existing mature PLM becomes available later in the run.

Execution policy after PLM blocker:

- Continue all CPU-valid mandatory work.
- Do not replace the PLM stage with an ad hoc non-PLM heuristic.
- Mark Stage A4/C PLM-dependent outputs as blocked/deferred if no mature PLM can be run.

## Progress log

### 2026-08-22 setup

Repository synced, task files read, CPU/phylogeny environment installed. Next action: run Stage A1-A3/A5 CPU hardening using existing V3/direct/conservation/structure inputs.

Checkpoint attempt:

- `git add -- docs/ONE_SHOT_COMPUTATIONAL_AUDIT_003_RUN_LOG.md envs/hrv2c-one-shot.yml results/one_shot_003/one_shot_003_micromamba_list.tsv`
- result: rejected by platform escalation reviewer due usage-limit state.
- consequence: checkpoint commit/push could not be performed in this turn. Analysis continued locally and the failure is preserved here and in the final report.

### 2026-08-22 CPU hardening stages

Script:

- `scripts/one_shot_computational_audit_003.py`

Completed CPU outputs:

- `data/evA71_2C_substitution_tolerance_to_A89_v1.tsv`
- `results/method_hardening_002/substitution_mapping_qc.tsv`
- `data/hrvA_independent_indel_events_v1.tsv`
- `results/method_hardening_002/phylogeny_qc.tsv`
- `data/pareto_junction_frontier_v1.tsv`
- `results/method_hardening_002/pareto_sensitivity.tsv`
- `data/candidate_junctions_v4_method_hardening.tsv`
- `results/one_shot_003/ranking_robustness.tsv`
- `results/one_shot_003/negative_control_audit.tsv`
- `data/computational_review_set_v1.tsv`

QC:

- substitution rows: 6,580 EV-A71 2C scores; 320 A89 junction outputs.
- substitution mapping: 315 exact, 5 ambiguous.
- FastTree tips: 77.
- insertion parsimony-change junctions: 1.
- local-deletion parsimony-change junctions: 12.
- V4 rows: 320.

### 2026-08-22 blocked/deferred stages

PLM:

- generated planned all-tag/all-junction table `data/tag_specific_plm_scores_v1.tsv` with 1,280 blocked rows.
- generated `results/method_hardening_002/plm_qc.tsv`.
- no PLM score was fabricated.

Cross-tag consensus:

- generated blocked-status files `data/tag_specific_consensus_v1.tsv` and `results/one_shot_003/tag_landscape_correlations.tsv`.

Stage E:

- no mature reproducible `colabfold_batch`, Rosetta or PyRosetta workflow was available.
- no visible NVIDIA GPU runtime.
- deferred in `docs/LIGHTWEIGHT_STRUCTURAL_TRIAGE_V1.md` and `results/one_shot_003/lightweight_structural_triage_status.tsv`.

### 2026-08-22 final synthesis

Reports generated:

- `docs/METHOD_HARDENING_002_REPORT.md`
- `docs/PHYLOGENY_AWARE_INDEL_V1.md`
- `docs/TAG_SPECIFIC_PLM_SCAN_V1.md`
- `docs/RANKING_ROBUSTNESS_AUDIT_V1.md`
- `docs/TAG_SPECIFIC_CONSENSUS_V1.md`
- `docs/COMPUTATIONAL_REVIEW_SET_V1.md`
- `docs/LIGHTWEIGHT_STRUCTURAL_TRIAGE_V1.md`
- `docs/ONE_SHOT_COMPUTATIONAL_AUDIT_003_REPORT.md`

Project-state files updated:

- `PROJECT_STATE.md`
- `ACTIVE_TASK.md`
- `TODO.md`
- `ANALYSIS_INDEX.md`
- `DECISIONS.md`

Final decision state:

`METHOD_HARDENING_BLOCKED`

Reason:

- CPU-valid hardening completed.
- Mandatory PLM insertion scan blocked.
- Cross-tag consensus unavailable.
- Stage E mature structure triage deferred.
- No site is called safe, validated or experimentally proven.
