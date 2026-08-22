# GPU_RECOVERY_004

Status: **AUTHORIZED / EXECUTE WHEN GPU IS VISIBLE**

Date: 2026-08-22

Branch: `analysis/conservation-002`

## Purpose

Recover only the computational stages that were blocked in `ONE_SHOT_COMPUTATIONAL_AUDIT_003` because that run executed on the Slurm login node rather than a GPU-allocated compute node.

This task must **not** rerun the completed CPU stages unless a concrete QC failure is discovered.

Current blocker reinterpretation:

The prior `METHOD_HARDENING_BLOCKED` state was caused by execution-context limitations: no allocated GPU device, no `nvidia-smi`, no `/dev/nvidia*`, and no usable PLM stack on the login node. The cluster does provide RTX 3090 Slurm resources.

## GPU execution policy

At task start, check:

- `hostname`
- `nvidia-smi`
- `echo $CUDA_VISIBLE_DEVICES`
- `/dev/nvidia*`

If at least one CUDA-capable GPU is visible, proceed immediately with GPU-capable work.

Do not require a specific physical GPU index or a specific RTX3090 node name. Any allocated CUDA-capable GPU that passes the runtime checks is acceptable.

If no GPU is visible, stop with `GPU_RECOVERY_BLOCKED_NO_GPU` and do not rerun the previous CPU pipeline.

## Completed upstream work to reuse

Reuse without recomputation unless QC proves invalid:

- EV-A71 substitution-tolerance integration;
- continuous/Pareto all-320 ranking;
- phylogeny-aware independent-indel analysis;
- ranking robustness / negative-control audit;
- V4 integrated non-PLM matrix;
- reduced 17-row computational review set.

Primary inputs include:

- `docs/ONE_SHOT_COMPUTATIONAL_AUDIT_003_REPORT.md`
- `data/candidate_junctions_v4_method_hardening.tsv`
- `data/computational_review_set_v1.tsv`
- `data/tag_specific_plm_scores_v1.tsv`
- `results/method_hardening_002/plm_qc.tsv`

## Stage 1 — GPU/PLM environment recovery

Create or repair a reproducible user-space environment for GPU PLM inference.

Requirements:

- install a CUDA-compatible PyTorch build appropriate to the visible driver/runtime;
- install the mature PLM package(s) required by the selected scoring method;
- record exact versions, checkpoints, commands and CUDA status;
- verify `torch.cuda.is_available()`;
- run a small inference smoke test before all-junction scoring;
- do not commit package caches or model weights.

Preferred approach:

Use a mature indel-capable protein-language-model scoring method if one is reproducibly available.

If not, use a documented ESM-family pseudo-log-likelihood insertion scoring workflow with explicit methodological limitations.

Do not invent a custom heuristic score in place of a mature PLM method.

## Stage 2 — complete tag-specific PLM scan

Target tags:

- MAP8
- HA
- G196

Before scoring, verify the exact amino-acid sequence/form used for each tag from repository evidence. If G196 has more than one scientifically justified form, keep them separate rather than silently selecting one.

Required work:

- generate all justified tag × 320-junction inserted A89 2C sequences;
- score every planned row;
- preserve raw and normalized scores separately;
- include batch/inference QC;
- rerun a reproducibility subset to confirm deterministic or acceptably stable results;
- retain missing/failed rows explicitly.

Do not overwrite the blocked V1 table without provenance. Create a completed versioned output, preferably:

- `data/tag_specific_plm_scores_v2_gpu.tsv`
- `results/gpu_recovery_004/plm_gpu_qc.tsv`
- `docs/TAG_SPECIFIC_PLM_SCAN_V2_GPU.md`

## Stage 3 — cross-tag consensus/disagreement

Using completed PLM scores:

- calculate rank correlations among MAP8/HA/G196 landscapes;
- identify junctions consistently favorable across tags;
- identify strong tag-specific outliers;
- compare minimal-footprint G196 behavior against MAP8/HA where justified;
- compare PLM patterns with EV-A71 insertion phenotype and continuous structural evidence;
- do not interpret PLM agreement as biological validation.

Create versioned outputs:

- `data/tag_specific_consensus_v2_gpu.tsv`
- `results/gpu_recovery_004/tag_landscape_correlations_v2.tsv`
- `docs/TAG_SPECIFIC_CONSENSUS_V2_GPU.md`

## Stage 4 — update integrated evidence and review set

Create a new integrated matrix rather than overwriting V4:

- `data/candidate_junctions_v5_plm_gpu.tsv`

Create a revised computational review set:

- `data/computational_review_set_v2_plm_gpu.tsv`

Requirements:

- preserve direct phenotype, functional constraints, structure, evolution, phylogeny-aware indels and PLM as separate columns/evidence classes;
- do not collapse all layers into one opaque scalar score;
- explicitly record where PLM agrees or conflicts with stronger evidence;
- re-audit `287|288–290|291`, `248|249`, `256|257`, and the outside-strict rows such as `203|204` and `224|225`;
- no site may be called safe or validated.

## Stage 5 — optional lightweight structural triage

If a mature reproducible structure-prediction or loop-remodeling workflow is already available or can be installed without derailing the run, perform lightweight triage only on the revised reduced review set.

Allowed:

- multiple-seed/model structure-prediction comparison;
- limited loop/insertion feasibility screening;
- local backbone perturbation;
- native-domain RMSD;
- gross clash checks;
- tag exposure;
- interface proximity/context;
- model convergence.

Do not start long MD.

If no mature workflow is available, mark this stage `DEFERRED` and continue to final synthesis.

Suggested outputs if completed:

- `data/lightweight_structural_triage_v2_gpu.tsv`
- `docs/LIGHTWEIGHT_STRUCTURAL_TRIAGE_V2_GPU.md`

## Final report

Create:

- `docs/GPU_RECOVERY_004_REPORT.md`

It must answer:

1. Which GPU/node/runtime was used?
2. Which PLM/model/checkpoint and scoring formulation were used?
3. How many planned tag × junction rows completed successfully?
4. How similar/different are MAP8, HA and G196 landscapes?
5. Did PLM materially change the 17-row review set?
6. Did any outside-strict site gain reproducible secondary support?
7. Do `287|288–290|291` remain only conflict controls?
8. Do `248|249` / `256|257` remain useful historical-conflict controls?
9. Did optional structural triage run, and did it change interpretation?
10. What uncertainties remain?

## Final decision state

Return exactly one of:

- `READY_FOR_CONFLICT_AWARE_TAG_SITE_MODELING`
- `NO_HIGH_CONFIDENCE_TARGETED_SITE`
- `GPU_RECOVERY_BLOCKED_NO_GPU`
- `GPU_RECOVERY_BLOCKED_SOFTWARE`

Do not start long MD or final experimental construct design automatically.

## Repository update requirements

Before completion, update consistently:

- `PROJECT_STATE.md`
- `ACTIVE_TASK.md`
- `TODO.md`
- `ANALYSIS_INDEX.md`
- `DECISIONS.md`

Commit scientifically meaningful outputs and push to `origin analysis/conservation-002` if remote access is available.
