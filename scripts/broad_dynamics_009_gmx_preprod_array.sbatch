#!/bin/bash
#SBATCH --job-name=bd009_preprod
#SBATCH --partition=RTX3090
#SBATCH --gres=gpu:rtx3090:1
#SBATCH --cpus-per-task=8
#SBATCH --mem=32G
#SBATCH --time=02:00:00
#SBATCH --array=0-12
#SBATCH --output=results/broad_dynamics_009/logs/slurm-gmx-preprod-%A_%a.out
#SBATCH --error=results/broad_dynamics_009/logs/slurm-gmx-preprod-%A_%a.err

set -euo pipefail
cd /public/home/yukang/wf/HRV-A89-2C-small-tag-and-insertion-site-prioritization

system_id="$(awk -F'\t' 'NR==ENVIRON["SLURM_ARRAY_TASK_ID"]+2 {print $1}' results/broad_dynamics_009/system_manifest.tsv)"
if [[ -z "$system_id" ]]; then
  echo "No system_id for array index ${SLURM_ARRAY_TASK_ID}" >&2
  exit 2
fi

bash scripts/broad_dynamics_009_gmx_pilot.sbatch "$system_id"
