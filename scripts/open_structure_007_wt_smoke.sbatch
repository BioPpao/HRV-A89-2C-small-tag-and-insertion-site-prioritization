#!/bin/bash
#SBATCH --job-name=os007_wt
#SBATCH --partition=RTX3090-autoEM
#SBATCH --gres=gpu:rtx3090:1
#SBATCH --cpus-per-task=8
#SBATCH --mem=48G
#SBATCH --time=08:00:00
#SBATCH --output=results/open_structure_007/slurm-%j.out
#SBATCH --error=results/open_structure_007/slurm-%j.err

set -euo pipefail
cd /public/home/yukang/wf/HRV-A89-2C-small-tag-and-insertion-site-prioritization

export XLA_PYTHON_CLIENT_PREALLOCATE=false
export TF_CPP_MIN_LOG_LEVEL=0
export COLABFOLD_DATA="$PWD/.tools/colabfold"
export MPLBACKEND=Agg
export LD_LIBRARY_PATH="$PWD/.tools/envs/open_structure_007/lib:$PWD/.tools/envs/open_structure_007/lib/python3.10/site-packages/nvidia/cudnn/lib:$PWD/.tools/envs/open_structure_007/lib/python3.10/site-packages/nvidia/cublas/lib:${LD_LIBRARY_PATH:-}"
unset HTTP_PROXY HTTPS_PROXY http_proxy https_proxy ALL_PROXY all_proxy
mkdir -p results/open_structure_007/wt_smoke "$COLABFOLD_DATA"

{
  echo -e "record\tvalue"
  echo -e "hostname\t$(hostname)"
  echo -e "cuda_visible_devices\t${CUDA_VISIBLE_DEVICES:-}"
  echo -e "date\t$(date -Iseconds)"
  echo -e "pwd\t$(pwd)"
  echo -e "python\t$(.tools/envs/open_structure_007/bin/python --version 2>&1)"
  echo -e "colabfold_batch\t$(.tools/envs/open_structure_007/bin/colabfold_batch --help 2>&1 | head -1)"
  echo -e "nvidia_smi\t$(nvidia-smi --query-gpu=name,driver_version,memory.total --format=csv,noheader | paste -sd ';' -)"
  .tools/envs/open_structure_007/bin/python - <<'PY'
import jax, jaxlib
print(f"jax\t{jax.__version__}")
print(f"jaxlib\t{jaxlib.__version__}")
print("jax_devices\t" + ";".join(map(str, jax.devices())))
PY
} > results/open_structure_007/wt_smoke_runtime.tsv

.tools/envs/open_structure_007/bin/colabfold_batch \
  --model-type alphafold2_ptm \
  --data "$COLABFOLD_DATA" \
  --msa-mode mmseqs2_uniref_env \
  --num-models 1 \
  --num-recycle 3 \
  --num-seeds 1 \
  --random-seed 7 \
  --overwrite-existing-results \
  results/open_structure_007/wt_msa_only/A89_2C_WT.a3m \
  results/open_structure_007/wt_smoke

.tools/envs/open_structure_007/bin/python scripts/open_structure_007_parse_colabfold.py \
  --mode smoke \
  --input-dir results/open_structure_007/wt_smoke \
  --panel data/tag_site_structure_panel_v3_open.tsv \
  --out results/open_structure_007/colabfold_smoke_test.tsv
