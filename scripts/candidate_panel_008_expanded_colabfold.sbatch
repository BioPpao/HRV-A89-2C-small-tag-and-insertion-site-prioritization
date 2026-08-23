#!/bin/bash
#SBATCH --job-name=cp008_cf
#SBATCH --partition=RTX3090
#SBATCH --gres=gpu:rtx3090:1
#SBATCH --cpus-per-task=8
#SBATCH --mem=64G
#SBATCH --time=06:00:00
#SBATCH --output=results/candidate_panel_008/logs/slurm-expanded-colabfold-%j.out
#SBATCH --error=results/candidate_panel_008/logs/slurm-expanded-colabfold-%j.err

set -euo pipefail
cd /public/home/yukang/wf/HRV-A89-2C-small-tag-and-insertion-site-prioritization

export XLA_PYTHON_CLIENT_PREALLOCATE=false
export TF_CPP_MIN_LOG_LEVEL=0
export COLABFOLD_DATA="$PWD/.tools/colabfold"
export MPLBACKEND=Agg
export LD_LIBRARY_PATH="$PWD/.tools/envs/open_structure_007/lib:$PWD/.tools/envs/open_structure_007/lib/python3.10/site-packages/nvidia/cudnn/lib:$PWD/.tools/envs/open_structure_007/lib/python3.10/site-packages/nvidia/cublas/lib:${LD_LIBRARY_PATH:-}"
unset HTTP_PROXY HTTPS_PROXY http_proxy https_proxy ALL_PROXY all_proxy

mkdir -p results/candidate_panel_008/expanded_colabfold results/candidate_panel_008/logs "$COLABFOLD_DATA"

{
  echo -e "record\tvalue"
  echo -e "hostname\t$(hostname)"
  echo -e "cuda_visible_devices\t${CUDA_VISIBLE_DEVICES:-}"
  echo -e "date\t$(date -Iseconds)"
  echo -e "nvidia_smi\t$(nvidia-smi --query-gpu=name,driver_version,memory.total --format=csv,noheader | paste -sd ';' -)"
  echo -e "input_dir\tresults/candidate_panel_008/expanded_colabfold_input"
  echo -e "output_dir\tresults/candidate_panel_008/expanded_colabfold"
  echo -e "num_models\t1"
  echo -e "num_recycle\t6"
  echo -e "num_seeds\t2"
  echo -e "random_seed\t31"
} > results/candidate_panel_008/expanded_colabfold_runtime.tsv

.tools/envs/open_structure_007/bin/colabfold_batch \
  --model-type alphafold2_ptm \
  --data "$COLABFOLD_DATA" \
  --num-models 1 \
  --num-recycle 6 \
  --num-seeds 2 \
  --random-seed 31 \
  --overwrite-existing-results \
  results/candidate_panel_008/expanded_colabfold_input \
  results/candidate_panel_008/expanded_colabfold

.tools/envs/open_structure_007/bin/python scripts/open_structure_007_parse_colabfold.py \
  --mode batch \
  --input-dir results/candidate_panel_008/expanded_colabfold \
  --panel data/expanded_structure_replication_panel_v1.tsv \
  --out results/candidate_panel_008/expanded_colabfold_manifest.tsv
