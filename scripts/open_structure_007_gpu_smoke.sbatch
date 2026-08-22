#!/bin/bash
#SBATCH --job-name=os007_gpu_smoke
#SBATCH --partition=RTX3090
#SBATCH --gres=gpu:rtx3090:1
#SBATCH --cpus-per-task=2
#SBATCH --mem=8G
#SBATCH --time=00:20:00
#SBATCH --output=results/open_structure_007/gpu-smoke-%j.out
#SBATCH --error=results/open_structure_007/gpu-smoke-%j.err

set -euo pipefail
cd /public/home/yukang/wf/HRV-A89-2C-small-tag-and-insertion-site-prioritization

export XLA_PYTHON_CLIENT_PREALLOCATE=false
export LD_LIBRARY_PATH="$PWD/.tools/envs/open_structure_007/lib:$PWD/.tools/envs/open_structure_007/lib/python3.10/site-packages/nvidia/cudnn/lib:$PWD/.tools/envs/open_structure_007/lib/python3.10/site-packages/nvidia/cublas/lib:${LD_LIBRARY_PATH:-}"
unset HTTP_PROXY HTTPS_PROXY http_proxy https_proxy ALL_PROXY all_proxy

.tools/envs/open_structure_007/bin/python - <<'PY'
import jax
import jax.numpy as jnp

print("hostname\t" + __import__("socket").gethostname())
print("devices\t" + ";".join(map(str, jax.devices())))
x = jnp.ones((512, 512), dtype=jnp.float32)
y = (x @ x).block_until_ready()
print("matmul_sum\t" + str(float(y.sum())))
PY
