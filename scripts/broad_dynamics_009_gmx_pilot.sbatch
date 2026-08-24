#!/bin/bash
#SBATCH --job-name=bd009_wt_pilot
#SBATCH --partition=RTX3090
#SBATCH --gres=gpu:rtx3090:1
#SBATCH --cpus-per-task=8
#SBATCH --mem=32G
#SBATCH --time=02:00:00
#SBATCH --output=results/broad_dynamics_009/logs/slurm-gmx-pilot-%j.out
#SBATCH --error=results/broad_dynamics_009/logs/slurm-gmx-pilot-%j.err

set -euo pipefail
cd /public/home/yukang/wf/HRV-A89-2C-small-tag-and-insertion-site-prioritization
module load gromacs/2024.2

system_id="${1:-WT_112_321}"
base="results/broad_dynamics_009/gromacs"
sdir="$base/systems/$system_id"
mdp="$base/mdp"
mkdir -p "$sdir"
cd "$sdir"

{
  echo -e "record\tvalue"
  echo -e "system_id\t$system_id"
  echo -e "hostname\t$(hostname)"
  echo -e "cuda_visible_devices\t${CUDA_VISIBLE_DEVICES:-}"
  echo -e "date_start\t$(date -Iseconds)"
  echo -e "nvidia_smi\t$(nvidia-smi --query-gpu=name,driver_version,memory.total --format=csv,noheader | paste -sd ';' -)"
  echo -e "gromacs\t$(gmx --version | sed -n '1,3p' | paste -sd '|' -)"
} > pilot_runtime.tsv

gmx pdb2gmx -f input_112_321.pdb -o processed.gro -p topol.top -ff charmm36 -water tip3p -ignh
gmx editconf -f processed.gro -o boxed.gro -bt dodecahedron -d 1.0
gmx solvate -cp boxed.gro -cs spc216.gro -o solvated.gro -p topol.top
gmx grompp -f "../../mdp/em.mdp" -c solvated.gro -p topol.top -o ions.tpr -maxwarn 1
printf 'SOL\n' | gmx genion -s ions.tpr -o solv_ions.gro -p topol.top -pname SOD -nname CLA -neutral -conc 0.15
gmx grompp -f "../../mdp/em.mdp" -c solv_ions.gro -p topol.top -o em.tpr
gmx mdrun -deffnm em -ntmpi 1 -ntomp "${SLURM_CPUS_PER_TASK:-8}" -pin on
gmx grompp -f "../../mdp/nvt.mdp" -c em.gro -r em.gro -p topol.top -o nvt.tpr
gmx mdrun -deffnm nvt -ntmpi 1 -ntomp "${SLURM_CPUS_PER_TASK:-8}" -pin on -nb gpu
gmx grompp -f "../../mdp/npt.mdp" -c nvt.gro -r em.gro -t nvt.cpt -p topol.top -o npt.tpr
gmx mdrun -deffnm npt -ntmpi 1 -ntomp "${SLURM_CPUS_PER_TASK:-8}" -pin on -nb gpu
gmx grompp -f "../../mdp/prod_smoke.mdp" -c npt.gro -t npt.cpt -p topol.top -o prod_smoke.tpr
gmx mdrun -deffnm prod_smoke -ntmpi 1 -ntomp "${SLURM_CPUS_PER_TASK:-8}" -pin on -nb gpu

{
  echo -e "date_end\t$(date -Iseconds)"
  echo -e "outputs\tem.gro;nvt.gro;npt.gro;prod_smoke.xtc;prod_smoke.edr;prod_smoke.cpt"
} >> pilot_runtime.tsv
