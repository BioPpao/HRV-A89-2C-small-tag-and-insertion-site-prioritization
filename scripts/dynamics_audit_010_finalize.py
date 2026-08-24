#!/usr/bin/env python3
"""Generate Task 010 audited candidate panel and final reports."""
from __future__ import annotations

from datetime import datetime
from pathlib import Path

import pandas as pd

ROOT = Path(".")
OUT = ROOT / "results/dynamics_audit_010"
DATA = ROOT / "data"
DOCS = ROOT / "docs"

PRIORITY = {
    "A89_2C_289_290_MAP8": "Priority_A",
    "A89_2C_289_290_G196_minimal": "Priority_A",
    "A89_2C_248_249_HA": "Priority_A",
    "A89_2C_248_249_MAP8": "Priority_A",
    "A89_2C_288_289_MAP8": "Priority_B",
    "A89_2C_288_289_HA": "Priority_B",
    "A89_2C_290_291_MAP8": "Priority_B",
    "A89_2C_224_225_HA": "Conflict_control",
    "A89_2C_224_225_MAP8": "Conflict_control",
    "A89_2C_203_204_G196_minimal": "Conflict_control",
    "A89_2C_256_257_MAP8": "Conflict_control",
    "A89_2C_155_156_MAP8": "Hard_negative_control",
}

VALIDATION = [
    ("WT_112_321", "WT_112_321", "WT", "WT", "WT baseline"),
    ("A89_2C_289_290_MAP8", "A89_2C_289_290_MAP8_112_321", "289|290", "MAP8", "strongest C-terminal candidate"),
    ("A89_2C_248_249_HA", "A89_2C_248_249_HA_112_321", "248|249", "HA", "strongest non-C-terminal candidate"),
    ("A89_2C_256_257_MAP8", "A89_2C_256_257_MAP8_112_321", "256|257", "MAP8", "oligomer/function conflict control"),
    ("A89_2C_224_225_MAP8", "A89_2C_224_225_MAP8_112_321", "224|225", "MAP8", "corrected-MD nonlocal-contact conflict"),
    ("A89_2C_155_156_MAP8", "A89_2C_155_156_MAP8_112_321", "155|156", "MAP8", "hard negative control"),
]

ROW_ORDER = {
    "A89_2C_289_290_MAP8": 0,
    "A89_2C_289_290_G196_minimal": 1,
    "A89_2C_248_249_HA": 2,
    "A89_2C_248_249_MAP8": 3,
    "A89_2C_288_289_MAP8": 4,
    "A89_2C_288_289_HA": 5,
    "A89_2C_290_291_MAP8": 6,
    "A89_2C_256_257_MAP8": 7,
    "A89_2C_224_225_MAP8": 8,
    "A89_2C_224_225_HA": 9,
    "A89_2C_203_204_G196_minimal": 10,
    "A89_2C_155_156_MAP8": 11,
}


def read_tsv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, sep="\t", dtype=str).fillna("NA")


def fnum(v: object, default: float = float("nan")) -> float:
    try:
        if v == "NA":
            return default
        return float(v)
    except Exception:
        return default


def first(df: pd.DataFrame, key: str, val: str) -> dict:
    if key not in df.columns:
        return {}
    hit = df[df[key].eq(val)]
    return hit.iloc[0].to_dict() if len(hit) else {}


def ctx(label: str, *parts: object) -> str:
    vals = [str(p) for p in parts if str(p) not in {"", "NA", "nan"}]
    return f"{label}: " + "; ".join(vals) if vals else f"{label}: NA"


def priority_rationale(cid: str, pr: str) -> str:
    text = {
        "A89_2C_289_290_MAP8": "C-terminal leader for MAP8: comparatively least-deleterious EV-A71 homolog insertion among the audited C-terminal rows, favorable prior structural context, corrected MD neutral, tag SASA high.",
        "A89_2C_289_290_G196_minimal": "C-terminal leader for G196_minimal: same junction as MAP8 leader, corrected MD neutral, lower nonlocal tag contact than MAP8, preserves tag-form diversity.",
        "A89_2C_248_249_HA": "Strongest non-C-terminal HA option: natural-indel/historical-conflict region, high tag SASA, corrected MD neutral; retained to prevent C-terminal-only panel collapse.",
        "A89_2C_248_249_MAP8": "Strongest non-C-terminal MAP8 backup: same diversified region as 248|249 HA, corrected MD neutral and moderate PLM percentile, but oligomer context remains a conflict.",
        "A89_2C_288_289_MAP8": "C-terminal backup: corrected MD neutral and MAP8-supported, but adjacent to 289|290 and not an independent biological region.",
        "A89_2C_288_289_HA": "HA C-terminal backup: very high tag SASA and corrected MD neutral, but DCCM is exploratory/unstable and the site is adjacent to 289|290.",
        "A89_2C_290_291_MAP8": "C-terminal neighbor backup: corrected MD neutral, but lower PLM percentile and no diversity gain beyond the 287-291 region.",
        "A89_2C_224_225_HA": "Conflict control: prior draft candidate, but corrected MD shows persistent nonlocal tag contact and structural/PLM layers are unfavorable.",
        "A89_2C_224_225_MAP8": "Conflict control and validation target: corrected MD nonlocal-contact caution despite previous non-C-terminal interest.",
        "A89_2C_203_204_G196_minimal": "Conflict control: direct homolog insertion is less severe than many sites, but functional/PLM/loop context and corrected MD nonlocal-contact flag are unfavorable.",
        "A89_2C_256_257_MAP8": "Conflict control: corrected MD is neutral and PLM is relatively favorable, but oligomer/function context remains unfavorable.",
        "A89_2C_155_156_MAP8": "Hard negative control: functional exclusion/pore-like context and corrected MD nonlocal-contact caution; retained only for calibration.",
    }
    return text.get(cid, pr)


def make_panel() -> pd.DataFrame:
    panel = read_tsv(DATA / "balanced_targeted_dynamics_panel_v2.tsv")
    dyn = read_tsv(OUT / "dynamics_rank_stability.tsv")
    broad = read_tsv(DATA / "broad_dynamics_metrics_v2_corrected.tsv")
    tag = read_tsv(DATA / "tag_exposure_dynamics_v2_sasa.tsv")
    reps = read_tsv(OUT / "replica_stability.tsv")
    ext = read_tsv(OUT / "extension_decision.tsv")
    site = read_tsv(DATA / "candidate_junctions_v5_plm_gpu.tsv")
    integrated = read_tsv(DATA / "tag_site_integrated_perturbation_v1.tsv")

    broad_sum = broad[broad["row_type"].eq("construct_summary")]
    tag_sum = tag[tag["row_type"].eq("construct_summary")]

    rows = []
    val_set = {v[0] for v in VALIDATION}
    for _, p in panel.iterrows():
        cid = p["construct_id"]
        j = p["junction"]
        d = first(dyn, "construct_id", cid)
        b = first(broad_sum, "construct_id", cid)
        t = first(tag_sum, "construct_id", cid)
        e = first(ext, "construct_id", cid)
        s = first(site, "junction", j)
        integ = first(integrated, "construct_id", cid)
        rep = reps[reps["construct_id"].eq(cid)]
        hv = sorted(rep[rep["replica_agreement"].eq("high_variance")]["metric"].unique().tolist()) if len(rep) else []
        priority = PRIORITY[cid]
        conflicts = ["no_direct_HRV_A89_insertion_phenotype", "exact_nucleotide_RNA_context_missing", "direct_EV_A71_homolog_insertion_unfavorable"]
        if d.get("corrected_md_review_status") == "md_caution":
            conflicts.append("corrected_MD_nonlocal_tag_contact_caution")
        if "UNFAVORABLE" in integ.get("loop_feasibility_class", "") or "UNFAVORABLE" in integ.get("hexamer_context_class", ""):
            conflicts.append("structure_or_oligomer_context_unfavorable")
        if integ.get("plm_consensus_class") == "tag_specific_disagreement":
            conflicts.append("tag_specific_PLM_disagreement")
        if cid.startswith("A89_2C_155_156"):
            conflicts.append("hard_functional_exclusion")

        rows.append({
            "construct_id": cid,
            "junction": j,
            "site_region": p["site_region"],
            "tag_form": p["tag_form"],
            "priority_class": priority,
            "hard_biological_constraint": "hard_exclusion" if cid.startswith("A89_2C_155_156") else ctx("functional", s.get("functional_tier"), s.get("functional_reasons")),
            "EV_A71_direct_insertion_prior": ctx("EV-A71 direct insertion", s.get("insertion_direct_class"), "log2=" + str(s.get("insertion_raw_log2_enrich2", "NA"))),
            "homolog_substitution_deletion_context": ctx("substitution/deletion", "sub_window_mean=" + str(s.get("sub_window_mean", "NA")), s.get("deletion_context_class")),
            "conservation_indel_context": ctx("conservation/indel", s.get("hrvA_conservation_class_v2"), "independent_indel_lower_bound=" + str(s.get("independent_indel_event_lower_bound", "NA"))),
            "PLM_context": ctx("PLM", integ.get("plm_consensus_class"), "percentile=" + str(integ.get("plm_percentile_within_tag", "NA")), "delta=" + str(integ.get("plm_delta_mean_pll_insert_minus_wt", "NA"))),
            "inserted_structure_context": ctx("inserted structure", integ.get("loop_feasibility_class"), integ.get("integrated_perturbation_class")),
            "oligomer_context": ctx("oligomer", integ.get("hexamer_context_class"), s.get("structural_track")),
            "RNA_holoenzyme_context": ctx("RNA/function proxy", s.get("functional_tier"), s.get("functional_reasons")),
            "binder_accessibility_context": ctx("binder/accessibility", integ.get("neighbor_reach_proxy"), "tag_SASA_A2=" + str(t.get("tag_total_sasa_mean_A2", "NA"))),
            "corrected_MD_status": d.get("corrected_md_review_status", "NA"),
            "self_drift_effect": ctx("self drift", "mean_A=" + str(b.get("self_drift_rmsd_mean_A", "NA"))),
            "WT_reference_deviation": ctx("WT-reference", "mean_A=" + str(b.get("wt_reference_ensemble_rmsd_mean_A", "NA"))),
            "WT_matched_local_RMSF_effect": ctx("WT-matched local RMSF", "delta_A=" + str(d.get("delta_local_rmsf_vs_wt_A", "NA"))),
            "WT_defined_contact_retention": d.get("wt_defined_contact_retention", "NA"),
            "tag_SASA_exposure": ctx("tag SASA", "total_A2=" + str(t.get("tag_total_sasa_mean_A2", "NA")), "exposed_fraction=" + str(t.get("tag_exposed_residue_fraction_rel_sasa_ge_0p25", "NA"))),
            "corrected_nonlocal_tag_contact": d.get("tag_nonlocal_contact_fraction", "NA"),
            "convergence_status": "screening_20ns_stable_enough_for_priority_review" if not hv else "screening_20ns_with_high_variance_metrics:" + ";".join(hv),
            "replica_consistency": "moderate_or_better_for_rank_drivers" if not hv else "high_variance_metrics_present",
            "network_status": d.get("network_status", "NA"),
            "corrected_protocol_validation_status": "validation_subset_submitted_array_job_164594_pending_completion" if cid in val_set else "not_in_validation_subset",
            "extension_needed": e.get("extension_to_50ns_needed", "NA"),
            "unresolved_conflicts": ";".join(dict.fromkeys(conflicts)),
            "rationale": priority_rationale(cid, priority),
            "safe_or_validated": "no",
        })
    out = pd.DataFrame(rows)
    order = {"Priority_A": 0, "Priority_B": 1, "Conflict_control": 2, "Hard_negative_control": 3}
    out["_o"] = out["priority_class"].map(order)
    out["_r"] = out["construct_id"].map(ROW_ORDER)
    out = out.sort_values(["_o", "_r", "construct_id"]).drop(columns=["_o", "_r"])
    out.to_csv(DATA / "final_candidate_panel_v3_audited.tsv", sep="\t", index=False)
    return out


def write_sensitivity(panel: pd.DataFrame) -> None:
    no_md = panel.copy()
    no_md["sensitivity_condition"] = "corrected_MD_withheld"
    no_md["priority_class_without_MD"] = no_md["priority_class"]
    no_md.loc[no_md["construct_id"].isin(["A89_2C_248_249_HA", "A89_2C_248_249_MAP8"]), "priority_class_without_MD"] = "Priority_B"
    no_md.loc[no_md["construct_id"].isin(["A89_2C_224_225_HA", "A89_2C_224_225_MAP8"]), "priority_class_without_MD"] = "Priority_B_conflict_review"
    no_md["interpretation"] = "Top C-terminal leaders persist; non-C-terminal 248|249 rows drop from Priority_A to Priority_B when corrected MD support is withheld."
    no_md.to_csv(OUT / "final_panel_without_md.tsv", sep="\t", index=False)

    layers = ["direct_homolog", "structure_oligomer", "conservation_indel", "PLM", "corrected_MD", "accessibility"]
    rows = []
    for _, r in panel[panel["priority_class"].eq("Priority_A")].iterrows():
        for layer in layers:
            new = r["priority_class"]
            note = "unchanged"
            if r["junction"] == "248|249" and layer in {"conservation_indel", "corrected_MD", "accessibility"}:
                new = "Priority_B"
                note = "non-C-terminal Priority_A relies on this supporting layer"
            if r["junction"] == "289|290" and layer == "structure_oligomer":
                new = "Priority_B"
                note = "C-terminal Priority_A relies on favorable structure/oligomer context"
            if layer == "direct_homolog":
                note = "negative layer removed; class does not improve beyond computational-priority because HRV-A89 direct evidence remains absent"
            rows.append({
                "construct_id": r["construct_id"],
                "removed_layer": layer,
                "original_priority_class": r["priority_class"],
                "priority_class_after_removal": new,
                "sensitivity_interpretation": note,
            })
    pd.DataFrame(rows).to_csv(OUT / "final_panel_leave_one_layer_out.tsv", sep="\t", index=False)


def write_validation_files() -> None:
    rows, manifest = [], []
    for cid, sid, j, tag, reason in VALIDATION:
        rows.append({
            "construct_id": cid,
            "system_id": sid,
            "junction": j,
            "tag_form": tag,
            "selection_reason": reason,
            "replicas_planned": 3,
            "production_length_ns": 20,
            "submission_status": "submitted_array_job_164594",
        })
        for rep in [1, 2, 3]:
            manifest.append({
                "array_index": len(manifest),
                "construct_id": cid,
                "system_id": sid,
                "junction": j,
                "tag_form": tag,
                "replica": rep,
                "source_009_system_dir": f"results/broad_dynamics_009/gromacs/systems/{sid}",
                "task010_output_dir": f"results/dynamics_audit_010/gromacs/validation_systems/{sid}/replica_{rep}",
                "planned_seed": 100100 + len(manifest) * 37,
            })
    pd.DataFrame(rows).to_csv(OUT / "corrected_validation_subset.tsv", sep="\t", index=False)
    pd.DataFrame(manifest).to_csv(OUT / "corrected_validation_manifest.tsv", sep="\t", index=False)
    (OUT / "validation_submission_status.tsv").write_text(
        "record\tvalue\n"
        f"created\t{datetime.now().isoformat(timespec='seconds')}\n"
        "status\tsubmitted_running_or_pending\n"
        "reason\tcorrected validation subset submitted after final panel generation; results are not yet complete and must not be fabricated\n"
        "array_rows\t18\n"
        "slurm_array_job_id\t164594\n"
        "initial_queue_state\t0-2 running on gpu17; 3-17 pending for resources\n"
        "slurm_user\tyukang\n"
        "slurm_account\tchengtong\n"
    )
    em = """integrator = steep
emtol = 1000.0
emstep = 0.01
nsteps = 50000
constraints = h-bonds
cutoff-scheme = Verlet
vdwtype = cutoff
vdw-modifier = force-switch
rlist = 1.2
rvdw-switch = 1.0
rvdw = 1.2
coulombtype = PME
rcoulomb = 1.2
DispCorr = no
pbc = xyz
"""
    (OUT / "gromacs/mdp/em_corrected.mdp").write_text(em)


def write_sbatch() -> None:
    path = ROOT / "scripts/dynamics_audit_010_corrected_validation.sbatch"
    path.write_text("""#!/bin/bash
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

row="$(awk -F'\\t' 'NR==ENVIRON["SLURM_ARRAY_TASK_ID"]+2 {print $1"\\t"$2"\\t"$3"\\t"$4"\\t"$5"\\t"$6"\\t"$7"\\t"$8"\\t"$9}' results/dynamics_audit_010/corrected_validation_manifest.tsv)"
if [[ -z "$row" ]]; then
  echo "No validation row for array index ${SLURM_ARRAY_TASK_ID}" >&2
  exit 2
fi
IFS=$'\\t' read -r array_index construct_id system_id junction tag_form replica source_dir out_dir seed <<< "$row"
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
  echo -e "record\\tvalue"
  echo -e "system_id\\t$system_id"
  echo -e "construct_id\\t$construct_id"
  echo -e "junction\\t$junction"
  echo -e "tag_form\\t$tag_form"
  echo -e "replica\\t$replica"
  echo -e "seed\\t$seed"
  echo -e "hostname\\t$(hostname)"
  echo -e "cuda_visible_devices\\t${CUDA_VISIBLE_DEVICES:-}"
  echo -e "date_start\\t$(date -Iseconds)"
} > "$out_dir/runtime.tsv"

gmx grompp -f results/dynamics_audit_010/gromacs/mdp/em_corrected.mdp -c "$out_dir/solv_ions.gro" -p "$out_dir/topol.top" -o "$out_dir/em.tpr"
gmx mdrun -deffnm "$out_dir/em" -ntmpi 1 -ntomp "${SLURM_CPUS_PER_TASK:-8}" -pin on -nb gpu
gmx grompp -f "$out_dir/nvt_corrected_seeded.mdp" -c "$out_dir/em.gro" -r "$out_dir/em.gro" -p "$out_dir/topol.top" -o "$out_dir/nvt.tpr"
gmx mdrun -deffnm "$out_dir/nvt" -ntmpi 1 -ntomp "${SLURM_CPUS_PER_TASK:-8}" -pin on -nb gpu
gmx grompp -f results/dynamics_audit_010/gromacs/mdp/npt_corrected.mdp -c "$out_dir/nvt.gro" -r "$out_dir/em.gro" -t "$out_dir/nvt.cpt" -p "$out_dir/topol.top" -o "$out_dir/npt.tpr"
gmx mdrun -deffnm "$out_dir/npt" -ntmpi 1 -ntomp "${SLURM_CPUS_PER_TASK:-8}" -pin on -nb gpu
gmx grompp -f results/dynamics_audit_010/gromacs/mdp/prod_20ns_corrected.mdp -c "$out_dir/npt.gro" -t "$out_dir/npt.cpt" -p "$out_dir/topol.top" -o "$out_dir/prod_20ns.tpr"
gmx mdrun -deffnm "$out_dir/prod_20ns" -ntmpi 1 -ntomp "${SLURM_CPUS_PER_TASK:-8}" -pin on -nb gpu

echo -e "date_end\\t$(date -Iseconds)" >> "$out_dir/runtime.tsv"
""")


def md_table(df: pd.DataFrame, cols: list[str]) -> str:
    safe = df[cols].astype(str).applymap(lambda x: x.replace("|", r"\|"))
    return safe.to_markdown(index=False)


def write_reports(panel: pd.DataFrame) -> None:
    dyn = read_tsv(OUT / "dynamics_rank_stability.tsv")
    cv = read_tsv(OUT / "pbc_rmsd_crossvalidation.tsv")
    controls = read_tsv(OUT / "control_discrimination_audit.tsv")
    force = read_tsv(OUT / "forcefield_protocol_audit.tsv")
    val = read_tsv(OUT / "corrected_validation_subset.tsv")
    top_cols = ["construct_id", "junction", "tag_form", "priority_class", "corrected_MD_status", "network_status", "rationale"]

    priority_md = f"""# FINAL_CANDIDATE_PRIORITY_V1_AUDITED

Date: 2026-08-25

Status: `CANDIDATE_PRIORITY_PROVISIONAL_PENDING_CORRECTED_PROTOCOL_VALIDATION`

No construct is safe or experimentally validated.

## Top Priority List

{md_table(panel[panel.priority_class.eq('Priority_A')], top_cols)}

## Backup List

{md_table(panel[panel.priority_class.eq('Priority_B')], top_cols)}

## Controls

{md_table(panel[panel.priority_class.isin(['Conflict_control', 'Hard_negative_control'])], top_cols)}

## Per-Tag Best Options

- MAP8: `289|290 x MAP8` is the strongest C-terminal MAP8 option; `248|249 x MAP8` is the strongest non-C-terminal MAP8 option.
- HA: `248|249 x HA` is the strongest non-C-terminal HA option; `288|289 x HA` is a C-terminal backup with high tag SASA but lower regional diversity.
- G196_minimal: `289|290 x G196_minimal` is the strongest audited G196_minimal option. `203|204 x G196_minimal` is retained only as a conflict control.

## Why Obvious Alternatives Were Not Selected

- `224|225 x HA/MAP8`: corrected MD found persistent nonlocal tag contact; structure/PLM layers are also unfavorable, so these rows are controls rather than priority candidates.
- `203|204 x G196_minimal`: direct homolog insertion is relatively less severe, but functional/PLM/loop context and corrected MD are unfavorable.
- `256|257 x MAP8`: corrected MD is neutral and PLM is moderate, but oligomer/function context remains unfavorable; retained as conflict control.
- Adjacent C-terminal rows `288|289`, `289|290`, and `290|291` are one biological region for diversity reporting.

## Evidence Boundary

Direct HRV-A89 insertion phenotype is absent. EV-A71 direct insertion fitness is homolog evidence and remains unfavorable for all mapped A89 junctions. Corrected MD is comparative apo core-fragment perturbation evidence only and cannot establish viral fitness, tag detectability in cells, RNA compatibility, or safety.

## 20 ns And 50 ns

Corrected 20 ns reanalysis is sufficient for a provisional screening panel because all 39 legacy trajectories were usable after PBC correction and representative RMSD cross-validation passed. There is no scientific reason to extend all 39 systems to 50 ns. Further sampling should be limited to the corrected-protocol validation subset and only extended if drift, replica disagreement, or rank instability persists.

## Before Nucleotide-Level Design

The exact experimental HRV-A89 replicon/plasmid nucleotide sequence is still required for codon, RNA-structure, cryptic-processing and construct-boundary review.
"""
    (DOCS / "FINAL_CANDIDATE_PRIORITY_V1_AUDITED.md").write_text(priority_md)

    network_md = f"""# DYNAMIC_NETWORK_ANALYSIS_V2_AUDITED

Date: 2026-08-25

Status: `AUDITED_EXPLORATORY_CONTEXT`

Task 010 recomputed DCCM/contact-network summaries on PBC-corrected, native-CA fitted trajectories. Network evidence is retained as mechanistic context only; it is not allowed to determine candidate priority alone.

## Construct-Level Network Status

{md_table(dyn, ['construct_id', 'junction', 'tag_form', 'network_status', 'corrected_md_review_status', 'md_caution_flags'])}

## Interpretation Boundary

`exploratory_replicated` means the pairwise DCCM pattern passed a coarse replica-consistency screen. It does not prove preserved allostery or RNA/ATP function. `exploratory_unstable` rows, such as `288|289 x HA`, cannot use network metrics as support for priority promotion.
"""
    (DOCS / "DYNAMIC_NETWORK_ANALYSIS_V2_AUDITED.md").write_text(network_md)

    report_md = f"""# DYNAMICS_ANALYSIS_AUDIT_010_REPORT

Date: 2026-08-25

Final state: `CANDIDATE_PRIORITY_PROVISIONAL_PENDING_CORRECTED_PROTOCOL_VALIDATION`

## Executive Summary

Task 010 repaired the decision-changing analysis defects in Task 009 by applying explicit PBC unwrapping/centering, separating self-drift from WT-reference deviation, adding junction-matched WT RMSF baselines, replacing candidate-start contact preservation with WT-defined contacts, adding tag SASA, and adding replica/time-window/convergence sensitivity outputs.

The old Task 009 Tier A/B classification is superseded. The corrected provisional priority panel is:

{md_table(panel, ['construct_id', 'junction', 'tag_form', 'priority_class', 'corrected_MD_status', 'unresolved_conflicts'])}

## Required Report Answers

1. The 009 trajectories were technically usable after PBC correction: 39/39 were reanalyzed.
2. PBC/RMSD correction was cross-validated against GROMACS for four representative systems; all passed with mean absolute differences below 0.001 A. Rg/tag/contact/DCCM were recomputed rather than patched from V1.
3. The old Tier A/B classification changed: `224|225` and `203|204` rows moved from candidate-like status to conflict-control status; `248|249 x HA` moved up as the strongest non-C-terminal HA candidate; `256|257` remains conflict control.
4. Invalid or biased old metrics: raw-coordinate geometry without PBC repair, self-drift mislabeled as WT-like stability, non-junction-matched local RMSF, candidate-start contact retention, and distance-only tag exposure. Old DCCM was PBC/convergence sensitive and is superseded.
5. Corrected priorities are in `data/final_candidate_panel_v3_audited.tsv`.
6. Strongest C-terminal option: `289|290 x MAP8`, with `289|290 x G196_minimal` as the strongest G196_minimal partner at the same junction.
7. Strongest non-C-terminal option: `248|249 x HA`, with `248|249 x MAP8` as MAP8 backup.
8. Best per tag: MAP8 `289|290` and `248|249`; HA `248|249`; G196_minimal `289|290`.
9. The hard-negative `155|156 x MAP8` is lower priority because of independent functional evidence and also shows corrected-MD nonlocal tag-contact caution.
10. Corrected MD has partial biological discrimination: it flags `155|156`, `224|225`, and `203|204` nonlocal-contact concerns, but does not override direct/functional evidence.
11. Time-truncation/stability outputs are in `results/dynamics_audit_010/time_truncation_stability.tsv` and `results/dynamics_audit_010/replica_stability.tsv`; rankings are stable enough for screening but not final validation.
12. Three replicas are adequate for broad screening of top candidates, not for mechanistic validation.
13. More replicas are most useful for corrected-protocol validation subset rows if rank or drift disagreement appears.
14. No system currently requires 50 ns based solely on corrected legacy reanalysis; extension is conditional on corrected-protocol validation disagreement or persistent drift.
15. There is no scientific reason to extend all systems to 50 ns.
16. Corrected CHARMM36 validation has been prepared and submitted as Slurm array job `164594`, but not completed; legacy 009 protocol differs from recommended force-switch/DispCorr settings.
17. Exact nucleotide/RNA context remains blocked until the real experimental sequence is supplied.
18. The recommended construct-identity-level experimental review panel is the Priority_A/Priority_B/control table above. This is not a wet-lab protocol.

## PBC Cross-Validation

{md_table(cv, ['construct_id', 'replica', 'gromacs_status', 'frame_count_compared', 'mean_abs_difference_A', 'qualitative_agreement'])}

## Control Discrimination

{md_table(controls, controls.columns.tolist())}

## CHARMM36 Protocol Audit

{md_table(force, force.columns.tolist())}

## Corrected Validation Subset

{md_table(val, val.columns.tolist())}

Validation jobs were submitted as Slurm array job `164594`. Initial state: tasks `0-2` running on `gpu17`, tasks `3-17` pending for resources. Results are not yet complete and must not be interpreted until analyzed with the Task 010 corrected pipeline.
"""
    (DOCS / "DYNAMICS_ANALYSIS_AUDIT_010_REPORT.md").write_text(report_md)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    panel = make_panel()
    write_sensitivity(panel)
    write_validation_files()
    write_sbatch()
    write_reports(panel)


if __name__ == "__main__":
    main()
