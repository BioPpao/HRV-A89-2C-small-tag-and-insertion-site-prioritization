#!/bin/bash
#SBATCH --job-name=bd009_multimer
#SBATCH --partition=RTX3090
#SBATCH --gres=gpu:rtx3090:1
#SBATCH --cpus-per-task=8
#SBATCH --mem=80G
#SBATCH --time=08:00:00
#SBATCH --output=results/broad_dynamics_009/logs/slurm-local-multimer-%j.out
#SBATCH --error=results/broad_dynamics_009/logs/slurm-local-multimer-%j.err

set -euo pipefail
cd /public/home/yukang/wf/HRV-A89-2C-small-tag-and-insertion-site-prioritization

export XLA_PYTHON_CLIENT_PREALLOCATE=false
export TF_CPP_MIN_LOG_LEVEL=0
export COLABFOLD_DATA="$PWD/.tools/colabfold"
export MPLBACKEND=Agg
export LD_LIBRARY_PATH="$PWD/.tools/envs/open_structure_007/lib:$PWD/.tools/envs/open_structure_007/lib/python3.10/site-packages/nvidia/cudnn/lib:$PWD/.tools/envs/open_structure_007/lib/python3.10/site-packages/nvidia/cublas/lib:${LD_LIBRARY_PATH:-}"
unset HTTP_PROXY HTTPS_PROXY http_proxy https_proxy ALL_PROXY all_proxy

mkdir -p results/broad_dynamics_009/local_multimer/output results/broad_dynamics_009/logs "$COLABFOLD_DATA"

{
  echo -e "record\tvalue"
  echo -e "hostname\t$(hostname)"
  echo -e "cuda_visible_devices\t${CUDA_VISIBLE_DEVICES:-}"
  echo -e "date_start\t$(date -Iseconds)"
  echo -e "nvidia_smi\t$(nvidia-smi --query-gpu=name,driver_version,memory.total --format=csv,noheader | paste -sd ';' -)"
  echo -e "model_type\talphafold2_multimer_v3"
  echo -e "msa_mode\tsingle_sequence"
  echo -e "num_models\t1"
  echo -e "num_recycle\t6"
  echo -e "num_seeds\t2"
  echo -e "random_seed\t51"
} > results/broad_dynamics_009/local_multimer/local_multimer_runtime.tsv

.tools/envs/open_structure_007/bin/colabfold_batch \
  --model-type alphafold2_multimer_v3 \
  --data "$COLABFOLD_DATA" \
  --msa-mode single_sequence \
  --num-models 1 \
  --num-recycle 6 \
  --num-seeds 2 \
  --random-seed 51 \
  --overwrite-existing-results \
  results/broad_dynamics_009/local_multimer/local_multimer_input.fasta \
  results/broad_dynamics_009/local_multimer/output

echo -e "date_end\t$(date -Iseconds)" >> results/broad_dynamics_009/local_multimer/local_multimer_runtime.tsv
