# TAG_SPECIFIC_PLM_SCAN_V1

Status: **blocked by PLM software/GPU availability**

Date: 2026-08-22

## Required scope

Scan MAP8, HA and G196 insertion effects across all 320 A89 2C junctions with a mature indel-aware PLM or documented ESM-family pseudo-log-likelihood method.

## Tag forms recorded

| Tag form | Sequence | Length |
|---|---|---:|
| MAP8 | `GDGMVPPG` | 8 |
| HA | `YPYDVPDYA` | 9 |
| G196_minimal | `DLVPR` | 5 |
| G196_practical_GS | `GSDLVPRGS` | 9 |

G196 was represented as both minimal and practical/flanked forms. No single form was silently chosen.

## Blocker

GPU/PLM environment check:

- `nvidia-smi`: not found.
- no `/dev/nvidia*` device files visible.
- no `/proc/driver/nvidia/gpus`.
- existing project/user environments lack `torch`, `transformers` and `esm`.
- attempted installation of `torch transformers safetensors` into `.tools/envs/hrv2c-one-shot`; platform escalation was rejected with usage-limit message.

Per repository method-quality policy, this stage was not replaced with a weak ad hoc sequence heuristic.

## Outputs

- `data/tag_specific_plm_scores_v1.tsv`
- `results/method_hardening_002/plm_qc.tsv`

`data/tag_specific_plm_scores_v1.tsv` contains all planned 1,280 tag x junction rows with `plm_status=blocked_software_unavailable` and no fabricated scores.

## Consequence

PLM-dependent cross-tag landscape conclusions remain unavailable. The final task decision therefore cannot be `READY_FOR_CONFLICT_AWARE_TAG_SITE_MODELING`.
