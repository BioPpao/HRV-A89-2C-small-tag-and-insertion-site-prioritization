#!/bin/bash
#SBATCH --job-name=dyn010_val20
#SBATCH --partition=A40,RTX3090
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=8
#SBATCH --mem=32G
#SBATCH --time=24:00:00
#SBATCH --array=0-17
#SBATCH --output=results/dynamics_audit_010/logs/slurm-val20-%A_%a.out
#SBATCH --error=results/dynamics_audit_010/logs/slurm-val20-%A_%a.err

set -euo pipefail
cd /public/home/yukang/wf/HRV-A89-2C-small-tag-and-insertion-site-prioritization
module load gromacs/2024.2

row="$(awk -F'\t' 'NR==ENVIRON["SLURM_ARRAY_TASK_ID"]+2 {print $1"\t"$2"\t"$3"\t"$4"\t"$5"\t"$6"\t"$7"\t"$8"\t"$9}' results/dynamics_audit_010/corrected_validation_manifest.tsv)"
if [[ -z "$row" ]]; then
  echo "No validation row for array index ${SLURM_ARRAY_TASK_ID}" >&2
  exit 2
fi
IFS=$'\t' read -r array_index construct_id system_id junction tag_form replica source_dir out_dir seed <<< "$row"
mkdir -p "$out_dir"

if [[ -s "$out_dir/prod_20ns.xtc" ]] && grep -q "Finished mdrun" "$out_dir/prod_20ns.log" 2>/dev/null; then
  echo "Already complete: $out_dir"
  exit 0
fi
for f in solv_ions.gro topol.top posre.itp; do
  if [[ ! -s "$source_dir/$f" ]]; then
    echo "Missing source file $source_dir/$f" >&2
    exit 3
  fi
  cp -f "$source_dir/$f" "$out_dir/$f"
done

sed "s/^gen_seed = .*/gen_seed = ${seed}/" results/dynamics_audit_010/gromacs/mdp/nvt_corrected.mdp > "$out_dir/nvt_corrected_seeded.mdp"
{
  echo -e "record\tvalue"
  echo -e "system_id\t$system_id"
  echo -e "construct_id\t$construct_id"
  echo -e "junction\t$junction"
  echo -e "tag_form\t$tag_form"
  echo -e "replica\t$replica"
  echo -e "seed\t$seed"
  echo -e "hostname\t$(hostname)"
  echo -e "cuda_visible_devices\t${CUDA_VISIBLE_DEVICES:-}"
  echo -e "date_start\t$(date -Iseconds)"
} > "$out_dir/runtime.tsv"

gmx grompp -f results/dynamics_audit_010/gromacs/mdp/em_corrected.mdp -c "$out_dir/solv_ions.gro" -p "$out_dir/topol.top" -o "$out_dir/em.tpr"
gmx mdrun -deffnm "$out_dir/em" -ntmpi 1 -ntomp "${SLURM_CPUS_PER_TASK:-8}" -pin on -nb gpu
gmx grompp -f "$out_dir/nvt_corrected_seeded.mdp" -c "$out_dir/em.gro" -r "$out_dir/em.gro" -p "$out_dir/topol.top" -o "$out_dir/nvt.tpr"
gmx mdrun -deffnm "$out_dir/nvt" -ntmpi 1 -ntomp "${SLURM_CPUS_PER_TASK:-8}" -pin on -nb gpu
gmx grompp -f results/dynamics_audit_010/gromacs/mdp/npt_corrected.mdp -c "$out_dir/nvt.gro" -r "$out_dir/em.gro" -t "$out_dir/nvt.cpt" -p "$out_dir/topol.top" -o "$out_dir/npt.tpr"
gmx mdrun -deffnm "$out_dir/npt" -ntmpi 1 -ntomp "${SLURM_CPUS_PER_TASK:-8}" -pin on -nb gpu
gmx grompp -f results/dynamics_audit_010/gromacs/mdp/prod_20ns_corrected.mdp -c "$out_dir/npt.gro" -t "$out_dir/npt.cpt" -p "$out_dir/topol.top" -o "$out_dir/prod_20ns.tpr"
gmx mdrun -deffnm "$out_dir/prod_20ns" -ntmpi 1 -ntomp "${SLURM_CPUS_PER_TASK:-8}" -pin on -nb gpu

echo -e "date_end\t$(date -Iseconds)" >> "$out_dir/runtime.tsv"
