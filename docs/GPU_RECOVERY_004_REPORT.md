# GPU_RECOVERY_004_REPORT

Status: **blocked before GPU/PLM execution**

Date: 2026-08-22

Final decision state: `GPU_RECOVERY_BLOCKED_NO_GPU`

## Scope

`GPU_RECOVERY_004` was authorized only to recover the GPU/PLM stages blocked in `ONE_SHOT_COMPUTATIONAL_AUDIT_003`.

The task explicitly required stopping without rerunning the completed CPU pipeline if no CUDA-capable allocated GPU was visible.

## Required GPU visibility check

Recorded in machine-readable form:

- `results/gpu_recovery_004/gpu_visibility_check.tsv`

Results:

| Check | Result |
|---|---|
| `hostname` | `admin1` |
| `nvidia-smi` | exit 127; `/bin/bash: nvidia-smi: command not found` |
| `echo $CUDA_VISIBLE_DEVICES` | empty |
| `ls -l /dev/nvidia*` | exit 2; `No such file or directory` |

Interpretation:

- no CUDA-capable device was visible to this process;
- no NVIDIA device files were present;
- the session appears to be on `admin1`, not a GPU-allocated compute runtime;
- therefore GPU PLM recovery could not be started without violating the task's stop rule.

## Upstream data reuse status

No completed CPU analyses were rerun.

The following upstream outputs remain the current reusable inputs:

- `data/evA71_2C_substitution_tolerance_to_A89_v1.tsv`
- `data/pareto_junction_frontier_v1.tsv`
- `data/hrvA_independent_indel_events_v1.tsv`
- `results/one_shot_003/ranking_robustness.tsv`
- `results/one_shot_003/negative_control_audit.tsv`
- `data/candidate_junctions_v4_method_hardening.tsv`
- `data/computational_review_set_v1.tsv`

## Stage status

| Stage | Status | Notes |
|---|---|---|
| Stage 1 GPU/PLM environment recovery | blocked | no visible CUDA-capable GPU; no `nvidia-smi`; no `/dev/nvidia*` |
| PyTorch/CUDA installation | not attempted | task required stopping before GPU work when no GPU was visible |
| CUDA smoke test | not possible | no visible device |
| Stage 2 MAP8/HA/G196 PLM scan | not run | no PLM environment or GPU runtime |
| Stage 3 cross-tag consensus/disagreement | not run | no PLM scores |
| Stage 4 V5 matrix and V2 review set | not created | generating PLM-completed outputs without PLM scores would be misleading |
| Stage 5 lightweight structural triage | not run | revised PLM GPU review set was not produced |

## Required synthesis answers

1. GPU/node/runtime used: none. Host was `admin1`; no NVIDIA runtime was visible.
2. PLM/model/checkpoint/scoring formulation: none executed.
3. Planned tag by junction rows completed: 0 completed GPU PLM rows.
4. MAP8/HA/G196 landscape similarity/difference: cannot assess.
5. Did PLM materially change the 17-row review set: no PLM data were generated, so no change can be made.
6. Did any outside-strict site gain reproducible secondary support: not from this task.
7. Do `287|288-290|291` remain only conflict controls: unchanged from V4/V1 review-set interpretation.
8. Do `248|249` / `256|257` remain historical-conflict controls: unchanged.
9. Optional structural triage: not run because PLM GPU recovery failed before a revised reduced review set existed.
10. Remaining uncertainty: MAP8/HA/G196 tag-specific PLM landscapes and cross-tag consensus remain missing until the task is rerun inside a Slurm GPU allocation with visible CUDA device files.

## Files intentionally not created

These outputs require completed GPU PLM scores and were therefore not generated:

- `data/tag_specific_plm_scores_v2_gpu.tsv`
- `data/tag_specific_consensus_v2_gpu.tsv`
- `data/candidate_junctions_v5_plm_gpu.tsv`
- `data/computational_review_set_v2_plm_gpu.tsv`
- `docs/TAG_SPECIFIC_PLM_SCAN_V2_GPU.md`
- `docs/TAG_SPECIFIC_CONSENSUS_V2_GPU.md`

## Final decision state

`GPU_RECOVERY_BLOCKED_NO_GPU`

