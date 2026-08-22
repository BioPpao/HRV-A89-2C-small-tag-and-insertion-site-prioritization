#!/bin/bash
#SBATCH --job-name=gpu_rec_004
#SBATCH --partition=RTX3090-autoEM
#SBATCH --gres=gpu:rtx3090:1
#SBATCH --cpus-per-task=4
#SBATCH --mem=32G
#SBATCH --time=08:00:00
#SBATCH --output=results/gpu_recovery_004/slurm-%j.out
#SBATCH --error=results/gpu_recovery_004/slurm-%j.err

set -euo pipefail

REPO=/public/home/yukang/wf/HRV-A89-2C-small-tag-and-insertion-site-prioritization
cd "$REPO"

mkdir -p results/gpu_recovery_004 envs

{
  echo -e "check\tcommand\texit_code\tstdout\tstderr"
  HOST=$(hostname)
  echo -e "hostname\thostname\t0\t${HOST}\t"
  if OUT=$(nvidia-smi 2>&1); then
    echo -e "nvidia_smi\tnvidia-smi\t0\t${OUT//$'\n'/; }\t"
  else
    EC=$?
    echo -e "nvidia_smi\tnvidia-smi\t${EC}\t\t${OUT//$'\n'/; }"
    exit 20
  fi
  echo -e "cuda_visible_devices\techo CUDA_VISIBLE_DEVICES\t0\t${CUDA_VISIBLE_DEVICES:-}\t"
  if OUT=$(ls -l /dev/nvidia* 2>&1); then
    echo -e "dev_nvidia\tls -l /dev/nvidia*\t0\t${OUT//$'\n'/; }\t"
  else
    EC=$?
    echo -e "dev_nvidia\tls -l /dev/nvidia*\t${EC}\t\t${OUT//$'\n'/; }"
    exit 21
  fi
} > results/gpu_recovery_004/gpu_visibility_check.tsv

ENV=.tools/envs/hrv2c-gpu-plm
MM=.tools/bin/micromamba

if [ ! -x "$ENV/bin/python" ]; then
  "$MM" create -y -p "$ENV" -c conda-forge python=3.11 pip pandas numpy scipy
fi

PY="$ENV/bin/python"
"$PY" -m pip install --upgrade pip

if ! "$PY" -c "import torch, esm" >/dev/null 2>&1; then
  "$PY" -m pip install torch==2.4.1 --index-url https://download.pytorch.org/whl/cu118
  "$PY" -m pip install fair-esm==2.0.0
fi

"$PY" - <<'PY'
import torch
print("python smoke ok")
print("torch", torch.__version__)
print("cuda_available", torch.cuda.is_available())
print("cuda_version", torch.version.cuda)
print("device", torch.cuda.get_device_name(0) if torch.cuda.is_available() else "")
x = torch.randn(32, 32, device="cuda")
y = x @ x.T
print("smoke_sum", float(y.sum().detach().cpu()))
PY

"$PY" scripts/gpu_recovery_004_plm_scan.py --batch-size 128

"$PY" -m pip freeze > results/gpu_recovery_004/pip_freeze_v2_gpu.txt
"$MM" env export -p "$ENV" > envs/hrv2c-gpu-plm.yml
