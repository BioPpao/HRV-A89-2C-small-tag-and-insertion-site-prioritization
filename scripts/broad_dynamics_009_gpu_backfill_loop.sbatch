#!/bin/bash
#SBATCH --job-name=bd009_gpu_fill
#SBATCH --partition=AMD
#SBATCH --cpus-per-task=1
#SBATCH --mem=2G
#SBATCH --time=12:00:00
#SBATCH --output=results/broad_dynamics_009/logs/slurm-gpu-backfill-%j.out
#SBATCH --error=results/broad_dynamics_009/logs/slurm-gpu-backfill-%j.err

set -euo pipefail
cd /public/home/yukang/wf/HRV-A89-2C-small-tag-and-insertion-site-prioritization

.tools/envs/open_structure_007/bin/python \
  scripts/broad_dynamics_009_gpu_backfill_submit.py \
  --loop \
  --interval 300 \
  --max-submit 4
