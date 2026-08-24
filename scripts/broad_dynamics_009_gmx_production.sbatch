#!/bin/bash
#SBATCH --job-name=bd009_prod20
#SBATCH --partition=RTX3090
#SBATCH --gres=gpu:rtx3090:1
#SBATCH --cpus-per-task=8
#SBATCH --mem=32G
#SBATCH --time=24:00:00
#SBATCH --array=0-38
#SBATCH --output=results/broad_dynamics_009/logs/slurm-gmx-prod20-%A_%a.out
#SBATCH --error=results/broad_dynamics_009/logs/slurm-gmx-prod20-%A_%a.err

set -euo pipefail
cd /public/home/yukang/wf/HRV-A89-2C-small-tag-and-insertion-site-prioritization
module load gromacs/2024.2

row="$(awk -F'\t' 'NR==ENVIRON["SLURM_ARRAY_TASK_ID"]+2 {print $1"\t"$2"\t"$3"\t"$4"\t"$5}' results/broad_dynamics_009/production_manifest.tsv)"
if [[ -z "$row" ]]; then
  echo "No production row for array index ${SLURM_ARRAY_TASK_ID}" >&2
  exit 2
fi
IFS=$'\t' read -r system_id construct_id junction tag_form replica <<< "$row"

base="results/broad_dynamics_009/gromacs"
sdir="$base/systems/$system_id"
rdir="$sdir/replica_${replica}"
mkdir -p "$rdir"

if [[ ! -s "$sdir/em.gro" || ! -s "$sdir/topol.top" ]]; then
  echo "Missing preproduction EM/topology for $system_id" >&2
  exit 3
fi

seed=$((9000 + SLURM_ARRAY_TASK_ID * 17 + replica))
sed "s/^gen_seed = .*/gen_seed = ${seed}/" "$base/mdp/nvt.mdp" > "$rdir/nvt_rep.mdp"

{
  echo -e "record\tvalue"
  echo -e "system_id\t$system_id"
  echo -e "construct_id\t$construct_id"
  echo -e "junction\t$junction"
  echo -e "tag_form\t$tag_form"
  echo -e "replica\t$replica"
  echo -e "hostname\t$(hostname)"
  echo -e "cuda_visible_devices\t${CUDA_VISIBLE_DEVICES:-}"
  echo -e "date_start\t$(date -Iseconds)"
  echo -e "gen_seed\t$seed"
  echo -e "nvidia_smi\t$(nvidia-smi --query-gpu=name,driver_version,memory.total --format=csv,noheader | paste -sd ';' -)"
} > "$rdir/production_runtime.tsv"

gmx grompp -f "$rdir/nvt_rep.mdp" -c "$sdir/em.gro" -r "$sdir/em.gro" -p "$sdir/topol.top" -o "$rdir/nvt.tpr"
gmx mdrun -deffnm "$rdir/nvt" -ntmpi 1 -ntomp "${SLURM_CPUS_PER_TASK:-8}" -pin on -nb gpu
gmx grompp -f "$base/mdp/npt.mdp" -c "$rdir/nvt.gro" -r "$sdir/em.gro" -t "$rdir/nvt.cpt" -p "$sdir/topol.top" -o "$rdir/npt.tpr"
gmx mdrun -deffnm "$rdir/npt" -ntmpi 1 -ntomp "${SLURM_CPUS_PER_TASK:-8}" -pin on -nb gpu
gmx grompp -f "$base/mdp/prod_20ns.mdp" -c "$rdir/npt.gro" -t "$rdir/npt.cpt" -p "$sdir/topol.top" -o "$rdir/prod_20ns.tpr"
if [[ -s "$rdir/prod_20ns.cpt" ]]; then
  gmx mdrun -deffnm "$rdir/prod_20ns" -ntmpi 1 -ntomp "${SLURM_CPUS_PER_TASK:-8}" -pin on -nb gpu -cpi "$rdir/prod_20ns.cpt" -append
else
  gmx mdrun -deffnm "$rdir/prod_20ns" -ntmpi 1 -ntomp "${SLURM_CPUS_PER_TASK:-8}" -pin on -nb gpu
fi

{
  echo -e "date_end\t$(date -Iseconds)"
  echo -e "trajectory\t$rdir/prod_20ns.xtc"
  echo -e "checkpoint\t$rdir/prod_20ns.cpt"
} >> "$rdir/production_runtime.tsv"
