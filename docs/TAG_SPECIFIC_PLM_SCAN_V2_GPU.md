# TAG_SPECIFIC_PLM_SCAN_V2_GPU

Status: **completed**

Method: ESM2 `esm2_t6_8M_UR50D` full-sequence masked pseudo-log-likelihood.

Primary machine-readable output:

- `data/tag_specific_plm_scores_v2_gpu.tsv`
- `results/gpu_recovery_004/plm_gpu_qc.tsv`
- `references/gpu_recovery_004_plm_source_records_v1.tsv`

Completed rows: 1280 / 1280.

Runtime: Slurm job `164151` on `gpu15`, NVIDIA GeForce RTX 3090, PyTorch 2.4.1+cu118, CUDA 11.8 build. Environment specification: `envs/hrv2c-gpu-plm.yml`.

Raw full-sequence PLL and length-normalized mean PLL are both retained. The integrated V5 table uses mean PLL deltas to reduce tag-length bias. PLM scores are secondary computational evidence, not biological validation.
