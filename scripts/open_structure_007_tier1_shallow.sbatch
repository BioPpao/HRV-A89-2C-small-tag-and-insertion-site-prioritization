#!/bin/bash
#SBATCH --job-name=os007_tier1
#SBATCH --partition=RTX3090
#SBATCH --gres=gpu:rtx3090:1
#SBATCH --cpus-per-task=8
#SBATCH --mem=64G
#SBATCH --time=08:00:00
#SBATCH --output=results/open_structure_007/slurm-tier1-%j.out
#SBATCH --error=results/open_structure_007/slurm-tier1-%j.err

set -euo pipefail
cd /public/home/yukang/wf/HRV-A89-2C-small-tag-and-insertion-site-prioritization

export XLA_PYTHON_CLIENT_PREALLOCATE=false
export TF_CPP_MIN_LOG_LEVEL=0
export COLABFOLD_DATA="$PWD/.tools/colabfold"
export MPLBACKEND=Agg
export LD_LIBRARY_PATH="$PWD/.tools/envs/open_structure_007/lib:$PWD/.tools/envs/open_structure_007/lib/python3.10/site-packages/nvidia/cudnn/lib:$PWD/.tools/envs/open_structure_007/lib/python3.10/site-packages/nvidia/cublas/lib:${LD_LIBRARY_PATH:-}"
unset HTTP_PROXY HTTPS_PROXY http_proxy https_proxy ALL_PROXY all_proxy
mkdir -p results/open_structure_007/tier1_shallow "$COLABFOLD_DATA"

{
  echo -e "record\tvalue"
  echo -e "hostname\t$(hostname)"
  echo -e "cuda_visible_devices\t${CUDA_VISIBLE_DEVICES:-}"
  echo -e "date\t$(date -Iseconds)"
  echo -e "nvidia_smi\t$(nvidia-smi --query-gpu=name,driver_version,memory.total --format=csv,noheader | paste -sd ';' -)"
} > results/open_structure_007/tier1_shallow_runtime.tsv

.tools/envs/open_structure_007/bin/colabfold_batch \
  --model-type alphafold2_ptm \
  --data "$COLABFOLD_DATA" \
  --msa-mode mmseqs2_uniref_env \
  --num-models 1 \
  --num-recycle 3 \
  --num-seeds 1 \
  --random-seed 11 \
  --overwrite-existing-results \
  results/open_structure_007/colabfold_tier1_input.fasta \
  results/open_structure_007/tier1_shallow

.tools/envs/open_structure_007/bin/python scripts/open_structure_007_parse_colabfold.py \
  --mode batch \
  --input-dir results/open_structure_007/tier1_shallow \
  --panel data/tag_site_structure_panel_v3_open.tsv \
  --out results/open_structure_007/tier1_shallow_manifest.tsv
