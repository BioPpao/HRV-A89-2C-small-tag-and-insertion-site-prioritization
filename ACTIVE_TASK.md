# Active task

Current task: `GPU_RECOVERY_004` — **COMPLETED**

Branch: `analysis/conservation-002`

Task specification:

`tasks/GPU_RECOVERY_004.md`

## Why this task exists

`ONE_SHOT_COMPUTATIONAL_AUDIT_003` completed the CPU-side hardening stages but blocked at the PLM stage because it ran on the Slurm login node without an allocated GPU device.

The cluster does provide RTX 3090 resources through Slurm, so this task recovers only the previously blocked GPU/PLM work and reuses all completed upstream analyses.

## Current execution result

Final report:

- `docs/GPU_RECOVERY_004_REPORT.md`

Machine-readable GPU check:

- `results/gpu_recovery_004/gpu_visibility_check.tsv`

Final successful runtime:

- `hostname`: `gpu15`
- GPU: NVIDIA GeForce RTX 3090
- driver: 575.57.08
- CUDA visible device: `0`
- PyTorch: 2.4.1+cu118
- PLM: ESM2 `esm2_t6_8M_UR50D`
- completed PLM rows: 1,280 / 1,280

Earlier direct execution on `admin1` correctly recorded `GPU_RECOVERY_BLOCKED_NO_GPU`, but the task was then rerun through Slurm on `gpu15` and completed.

## Execution rule

At task start check GPU visibility with:

- `hostname`
- `nvidia-smi`
- `echo $CUDA_VISIBLE_DEVICES`
- `/dev/nvidia*`

If any CUDA-capable allocated GPU is visible and usable, proceed immediately. Do not require a specific node or physical GPU index.

If no GPU is visible, stop with `GPU_RECOVERY_BLOCKED_NO_GPU` and do not rerun the completed CPU pipeline.

## Authorized scope

1. GPU-capable PLM environment setup and smoke-test.
2. MAP8 / HA / G196 all-320 tag-specific PLM scans.
3. Cross-tag consensus/disagreement analysis.
4. New V5 integrated evidence matrix.
5. Revised computational review set.
6. Optional lightweight structural feasibility triage if a mature reproducible method is available.
7. Final report and repository state updates.

## Reuse, do not rerun by default

- EV-A71 substitution-tolerance integration.
- continuous/Pareto all-320 ranking.
- phylogeny-aware independent-indel analysis.
- non-PLM robustness/negative-control audit.
- V4 non-PLM matrix.
- current 17-row computational review set.

## Prohibited automatic escalation

Do not start:

- long MD;
- final experimental construct recommendation;
- experimental protocol design;
- final RNA/codon design without the exact experimental nucleotide construct.

No site may be called safe or validated for HRV-A89.

## Required final report

`docs/GPU_RECOVERY_004_REPORT.md`

## Final state

`READY_FOR_CONFLICT_AWARE_TAG_SITE_MODELING`
