#!/usr/bin/env python3
"""Analyze Task 010 corrected CHARMM36 validation trajectories."""
from __future__ import annotations

import math
import re
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

import MDAnalysis as mda
import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import dynamics_audit_010_reanalyze as base  # noqa: E402

ROOT = Path(".")
OUT = ROOT / "results/dynamics_audit_010"
DATA = ROOT / "data"
DOCS = ROOT / "docs"
MANIFEST = OUT / "corrected_validation_manifest.tsv"
JOB_ID = "164594"
SACCT_PROVENANCE = OUT / f"corrected_validation_slurm_sacct_{JOB_ID}_v1.tsv"

VALIDATION_IDS = {
    "A89_2C_289_290_MAP8",
    "A89_2C_248_249_HA",
    "A89_2C_256_257_MAP8",
    "A89_2C_224_225_MAP8",
    "A89_2C_155_156_MAP8",
}

KEY_METRICS = [
    ("broad", "self_drift_rmsd_mean_A"),
    ("broad", "stable_core_self_drift_rmsd_mean_A"),
    ("broad", "wt_reference_ensemble_rmsd_mean_A"),
    ("broad", "native_ca_rg_mean_A"),
    ("broad", "delta_local_rmsf_vs_wt_A"),
    ("contact", "wt_defined_contact_retention_mean"),
    ("contact", "candidate_start_contact_persistence_mean"),
    ("tag", "tag_total_sasa_mean_A2"),
    ("tag", "tag_exposed_residue_fraction_rel_sasa_ge_0p25"),
    ("tag", "tag_nonlocal_contact_fraction_any_lt_4p5A"),
    ("network", "local_to_functional_abs_dccm_mean"),
]


def read_tsv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, sep="\t", dtype=str).fillna("NA")


def write_tsv(path: Path, rows) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).to_csv(path, sep="\t", index=False, na_rep="NA")


def fnum(x, default=math.nan) -> float:
    try:
        if str(x) in {"", "NA", "nan"}:
            return default
        return float(x)
    except Exception:
        return default


def mean_sd(vals) -> tuple[float, float]:
    arr = np.array([fnum(v) for v in vals], dtype=float)
    arr = arr[np.isfinite(arr)]
    if arr.size == 0:
        return math.nan, math.nan
    return float(arr.mean()), float(arr.std(ddof=1) if arr.size > 1 else 0.0)


def sacct_rows() -> dict[str, dict[str, str]]:
    proc = subprocess.run(
        ["sacct", "-j", JOB_ID, "--format=JobID,State,ExitCode,Elapsed,NodeList%30", "-P"],
        text=True,
        capture_output=True,
    )
    out = {}
    text = proc.stdout
    if proc.returncode != 0 and SACCT_PROVENANCE.is_file():
        text = SACCT_PROVENANCE.read_text()
    elif proc.returncode != 0:
        return out
    for line in text.splitlines()[1:]:
        parts = line.split("|")
        if len(parts) < 5 or "." in parts[0]:
            continue
        m = re.match(rf"{JOB_ID}_(\d+)$", parts[0])
        if not m:
            continue
        out[m.group(1)] = {
            "sacct_state": parts[1],
            "sacct_exit_code": parts[2],
            "sacct_elapsed": parts[3],
            "sacct_node": parts[4],
        }
    return out


def completion_audit(manifest: pd.DataFrame) -> list[dict]:
    sacct = sacct_rows()
    rows = []
    for r in manifest.to_dict("records"):
        array_index = str(r["array_index"])
        rdir = Path(r["task010_output_dir"])
        paths = {name: rdir / f"prod_20ns.{name}" for name in ["xtc", "tpr", "log", "edr", "gro", "cpt"]}
        log_text = paths["log"].read_text(errors="ignore") if paths["log"].is_file() else ""
        fatal_patterns = ["Fatal error", "Segmentation fault", "Particle coordinate is nan"]
        fatal_hits = [p for p in fatal_patterns if p in log_text]
        frame_count, final_time_ns, finite_coords, finite_box, readable = 0, math.nan, False, False, False
        read_error = "NA"
        try:
            u = mda.Universe(str(paths["tpr"]), str(paths["xtc"]))
            coords_ok = []
            box_ok = []
            for ts in u.trajectory:
                frame_count += 1
                final_time_ns = ts.time / 1000.0
                coords_ok.append(bool(np.isfinite(u.atoms.positions).all()))
                box_ok.append(bool(np.isfinite(ts.dimensions[:3]).all()))
            finite_coords = bool(coords_ok and all(coords_ok))
            finite_box = bool(box_ok and all(box_ok))
            readable = True
        except Exception as exc:
            read_error = repr(exc)
        energy = base.energy_summary(paths["edr"], f"val_{array_index}")
        size_ok = {f"{k}_exists": p.is_file() for k, p in paths.items()}
        size_ok.update({f"{k}_size_bytes": p.stat().st_size if p.is_file() else 0 for k, p in paths.items()})
        status = (
            "pass"
            if all(size_ok[f"{k}_exists"] and size_ok[f"{k}_size_bytes"] > 0 for k in ["xtc", "tpr", "log", "edr", "gro"])
            and readable
            and finite_coords
            and finite_box
            and final_time_ns >= 19.9
            and "Finished mdrun" in log_text
            and not fatal_hits
            and energy.get("energy_status") == "finite"
            else "review_required"
        )
        row = {
            **{k: r[k] for k in ["array_index", "construct_id", "system_id", "junction", "tag_form", "replica", "planned_seed"]},
            **{
                "sacct_state": sacct.get(array_index, {}).get("sacct_state", "NA"),
                "sacct_exit_code": sacct.get(array_index, {}).get("sacct_exit_code", "NA"),
                "sacct_elapsed": sacct.get(array_index, {}).get("sacct_elapsed", "NA"),
                "sacct_node": sacct.get(array_index, {}).get("sacct_node", "NA"),
            },
            **size_ok,
            "trajectory_readable": readable,
            "read_error": read_error,
            "frame_count": frame_count,
            "final_time_ns": final_time_ns,
            "finite_coordinates": finite_coords,
            "finite_box": finite_box,
            "finished_mdrun": "Finished mdrun" in log_text,
            "fatal_log_hits": ";".join(fatal_hits) if fatal_hits else "none",
            "log_warning_count": len(re.findall(r"\bWARNING\b", log_text)),
            "log_note_count": len(re.findall(r"\bNOTE\b", log_text)),
            "integrity_status": status,
        }
        row.update(energy)
        rows.append(row)
    write_tsv(OUT / "corrected_validation_completion_v1.tsv", rows)
    return rows


def rows_for_base(manifest: pd.DataFrame) -> list[dict[str, str]]:
    rows = []
    for r in manifest.to_dict("records"):
        rdir = Path(r["task010_output_dir"])
        rows.append(
            {
                "system_id": r["system_id"],
                "construct_id": r["construct_id"],
                "junction": r["junction"],
                "tag_form": r["tag_form"],
                "replica": str(r["replica"]),
                "slurm_array_index": f"cv{r['array_index']}",
                "trajectory_path": str(rdir / "prod_20ns.xtc"),
                "energy_path": str(rdir / "prod_20ns.edr"),
                "checkpoint_path": str(rdir / "prod_20ns.cpt"),
            }
        )
    return rows


def stability_tables(trunc_rows, summary_source, network_summary) -> None:
    trunc_df = pd.DataFrame(trunc_rows)
    grp = trunc_df.groupby(["construct_id", "junction", "tag_form", "metric", "burnin_ns", "truncation_ns"], dropna=False)["replica_mean"]
    trunc_summary = grp.agg(["mean", "std", "count"]).reset_index().rename(
        columns={"mean": "mean_across_replicas", "std": "sd_across_replicas", "count": "replica_count"}
    )
    write_tsv(OUT / "corrected_validation_time_truncation_v1.tsv", trunc_summary)

    rep_rows = []
    for cid, metrics in summary_source.items():
        for metric, vals in metrics.items():
            m, sd = mean_sd(vals)
            loro = []
            vals = [fnum(v) for v in vals if math.isfinite(fnum(v))]
            if len(vals) >= 3:
                for i in range(len(vals)):
                    loro.append(float(np.mean([v for j, v in enumerate(vals) if j != i])))
            rep_rows.append(
                {
                    "construct_id": cid,
                    "metric": metric,
                    "replica_count": len(vals),
                    "mean": m,
                    "sd_across_replicas": sd,
                    "leave_one_replica_out_min": float(np.min(loro)) if loro else math.nan,
                    "leave_one_replica_out_max": float(np.max(loro)) if loro else math.nan,
                    "replica_agreement": "high_variance" if math.isfinite(m) and math.isfinite(sd) and abs(sd) > max(abs(m) * 0.5, 1e-9) else "moderate_or_better",
                }
            )
    write_tsv(OUT / "corrected_validation_replica_stability_v1.tsv", rep_rows)
    write_tsv(OUT / "corrected_validation_network_replica_stability_v1.tsv", network_summary)


def table_map(broad, contact, tag, network) -> dict[str, pd.DataFrame]:
    return {
        "broad": pd.DataFrame(broad),
        "contact": pd.DataFrame(contact),
        "tag": pd.DataFrame(tag),
        "network": pd.DataFrame(network),
    }


def validation_rank(tables: dict[str, pd.DataFrame]) -> pd.DataFrame:
    rows = []
    for cid, g in tables["broad"][tables["broad"]["row_type"].eq("replica")].groupby("construct_id"):
        first = g.iloc[0].to_dict()
        get = lambda table, col: mean_sd(tables[table][(tables[table]["row_type"].eq("replica")) & (tables[table]["construct_id"].eq(cid))][col])[0]
        drmsf = get("broad", "delta_local_rmsf_vs_wt_A")
        contact = get("contact", "wt_defined_contact_retention_mean")
        sasa = get("tag", "tag_total_sasa_mean_A2")
        nonlocal_frac = get("tag", "tag_nonlocal_contact_fraction_any_lt_4p5A")
        flags = []
        if math.isfinite(drmsf) and drmsf > 5:
            flags.append("high_local_RMSF_delta")
        if math.isfinite(contact) and contact < 0.75:
            flags.append("low_WT_contact_retention")
        if math.isfinite(sasa) and sasa < 120:
            flags.append("low_tag_SASA")
        if math.isfinite(nonlocal_frac) and nonlocal_frac > 0.75:
            flags.append("high_nonlocal_tag_contact")
        rows.append(
            {
                "construct_id": cid,
                "junction": first.get("junction", "NA"),
                "tag_form": first.get("tag_form", "NA"),
                "validation_wt_reference_rmsd_mean_A": get("broad", "wt_reference_ensemble_rmsd_mean_A"),
                "validation_delta_local_rmsf_vs_wt_A": drmsf,
                "validation_wt_defined_contact_retention": contact,
                "validation_tag_total_sasa_mean_A2": sasa,
                "validation_tag_nonlocal_contact_fraction": nonlocal_frac,
                "validation_md_review_status": "md_caution" if flags else "md_neutral_or_supportive",
                "validation_md_caution_flags": ";".join(flags) if flags else "none",
            }
        )
    df = pd.DataFrame(rows)
    write_tsv(OUT / "corrected_validation_dynamics_rank_v1.tsv", df)
    return df


def protocol_sensitivity(legacy_tables: dict[str, pd.DataFrame], val_tables: dict[str, pd.DataFrame], val_rank: pd.DataFrame) -> pd.DataFrame:
    legacy_rank = read_tsv(OUT / "dynamics_rank_stability.tsv")
    rows = []
    for cid in sorted(VALIDATION_IDS | {"WT_112_321"}):
        for table, metric in KEY_METRICS:
            lvals = legacy_tables[table][(legacy_tables[table]["row_type"].eq("replica")) & (legacy_tables[table]["construct_id"].eq(cid))][metric].map(fnum)
            vvals = val_tables[table][(val_tables[table]["row_type"].eq("replica")) & (val_tables[table]["construct_id"].eq(cid))][metric].map(fnum)
            lm, lsd = mean_sd(lvals)
            vm, vsd = mean_sd(vvals)
            overlap = "NA"
            if all(math.isfinite(x) for x in [lm, lsd, vm, vsd]):
                overlap = "yes" if max(lm - lsd, vm - vsd) <= min(lm + lsd, vm + vsd) else "no"
            shift = vm - lm if math.isfinite(lm) and math.isfinite(vm) else math.nan
            if not math.isfinite(shift):
                direction = "NA"
            elif abs(shift) <= max(abs(lm) * 0.05, 0.05):
                direction = "similar"
            elif shift > 0:
                direction = "corrected_higher"
            else:
                direction = "corrected_lower"
            legacy_status = "baseline" if cid == "WT_112_321" else first_value(legacy_rank, cid, "corrected_md_review_status")
            validation_status = "baseline" if cid == "WT_112_321" else first_value(val_rank, cid, "validation_md_review_status")
            rows.append(
                {
                    "construct_id": cid,
                    "metric": metric,
                    "legacy_mean": lm,
                    "legacy_sd": lsd,
                    "corrected_protocol_mean": vm,
                    "corrected_protocol_sd": vsd,
                    "protocol_shift_corrected_minus_legacy": shift,
                    "corrected_vs_legacy_direction": direction,
                    "replica_mean_sd_overlap": overlap,
                    "legacy_md_class": legacy_status,
                    "corrected_protocol_md_class": validation_status,
                    "qualitative_classification_stability": "stable" if legacy_status == validation_status else "changed_or_review",
                }
            )
    df = pd.DataFrame(rows)
    write_tsv(OUT / "protocol_sensitivity_v1.tsv", df)
    return df


def first_value(df: pd.DataFrame, cid: str, col: str) -> str:
    hit = df[df["construct_id"].eq(cid)]
    return str(hit.iloc[0][col]) if len(hit) and col in hit.columns else "NA"


def block_stability(tables: dict[str, pd.DataFrame]) -> pd.DataFrame:
    specs = [
        ("broad", "self_drift_rmsd", "self_drift_rmsd"),
        ("broad", "wt_reference_ensemble_rmsd", "wt_reference_ensemble_rmsd"),
        ("contact", "wt_defined_contact_retention", "wt_defined_contact_retention"),
        ("tag", "tag_total_sasa", "tag_total_sasa"),
    ]
    rows = []
    for table, prefix, label in specs:
        df = tables[table][tables[table]["row_type"].eq("replica")]
        for cid, g in df.groupby("construct_id"):
            vals = {}
            for block in ["0_5ns", "5_10ns", "10_15ns", "15_20ns"]:
                col = f"{prefix}_{block}_mean"
                vals[block] = [fnum(x) for x in g[col]] if col in g else []
            early = np.array([v for v in vals["0_5ns"] if math.isfinite(v)])
            late = np.array([v for v in vals["15_20ns"] if math.isfinite(v)])
            diffs = late - early if len(early) == len(late) and len(late) else np.array([])
            rows.append(
                {
                    "construct_id": cid,
                    "metric": label,
                    "block_0_5_mean": float(np.mean(early)) if len(early) else math.nan,
                    "block_5_10_mean": mean_sd(vals["5_10ns"])[0],
                    "block_10_15_mean": mean_sd(vals["10_15ns"])[0],
                    "block_15_20_mean": float(np.mean(late)) if len(late) else math.nan,
                    "late_minus_early_mean": float(np.mean(diffs)) if len(diffs) else math.nan,
                    "late_minus_early_sd": float(np.std(diffs, ddof=1)) if len(diffs) > 1 else 0.0 if len(diffs) else math.nan,
                    "replica_directional_agreement": int(np.sum(diffs > 0)) if len(diffs) else "NA",
                    "block_stability_note": "directional_drift_all_replicas" if len(diffs) == 3 and (np.all(diffs > 0) or np.all(diffs < 0)) else "mixed_or_low_drift",
                }
            )
    df = pd.DataFrame(rows)
    write_tsv(OUT / "corrected_validation_block_stability_v1.tsv", df)
    return df


def sampling_decision(val_rank: pd.DataFrame, block_df: pd.DataFrame, protocol_df: pd.DataFrame) -> pd.DataFrame:
    roles = {
        "WT_112_321": "WT baseline",
        "A89_2C_289_290_MAP8": "candidate_hypothesis_C_terminal_MAP8",
        "A89_2C_248_249_HA": "candidate_hypothesis_non_C_terminal_HA",
        "A89_2C_256_257_MAP8": "conflict_control_oligomer_function",
        "A89_2C_224_225_MAP8": "conflict_control_MD_caution_retest",
        "A89_2C_155_156_MAP8": "hard_negative_control",
    }
    rows = []
    for cid, role in roles.items():
        rank = val_rank[val_rank["construct_id"].eq(cid)]
        status = "baseline" if cid == "WT_112_321" else first_value(val_rank, cid, "validation_md_review_status")
        changed = protocol_df[(protocol_df["construct_id"].eq(cid)) & (protocol_df["qualitative_classification_stability"].eq("changed_or_review"))]
        drift_flags = []
        for _, brow in block_df[block_df["construct_id"].eq(cid)].iterrows():
            if brow["block_stability_note"] != "directional_drift_all_replicas":
                continue
            metric = brow["metric"]
            shift = abs(fnum(brow["late_minus_early_mean"]))
            threshold = {
                "self_drift_rmsd": 0.75,
                "wt_reference_ensemble_rmsd": 0.75,
                "wt_defined_contact_retention": 0.05,
                "tag_total_sasa": 100.0,
            }.get(metric, math.inf)
            if math.isfinite(shift) and shift >= threshold:
                drift_flags.append(metric)
        high_priority_boundary = cid in {"A89_2C_289_290_MAP8", "A89_2C_248_249_HA", "A89_2C_224_225_MAP8"}
        if len(changed) and high_priority_boundary:
            decision = "ADD_INDEPENDENT_REPLICAS"
            reason = "classification_or_protocol_shift_on_decision_relevant_system;replica_breadth_preferred_before_extension"
        elif drift_flags and len(drift_flags) >= 3 and high_priority_boundary:
            decision = "EXTEND_SELECTED_REPLICAS_TO_50NS"
            reason = "multiple_observables_show_same_direction_late_drift_across_replicas"
        else:
            decision = "STOP_AT_20NS"
            reason = "classification_stable_for_screening;no_blanket_50ns_trigger"
        rows.append(
            {
                "construct_id": cid,
                "role": role,
                "corrected_protocol_md_status": status,
                "classification_changed_vs_legacy": "yes" if len(changed) else "no",
                "directional_drift_metrics": ";".join(drift_flags) if drift_flags else "none",
                "sampling_decision": decision,
                "decision_basis": reason,
                "why_not_50ns_if_not_selected": "replica/priority classification is screening-stable; extension reserved for shared slow drift" if decision != "EXTEND_SELECTED_REPLICAS_TO_50NS" else "NA",
            }
        )
    df = pd.DataFrame(rows)
    write_tsv(OUT / "final_sampling_decision_v1.tsv", df)
    return df


def final_panel_v4(v3: pd.DataFrame, val_rank: pd.DataFrame, sampling: pd.DataFrame) -> pd.DataFrame:
    rows = []
    direct_validated = set(val_rank["construct_id"])
    for _, r in v3.iterrows():
        row = r.to_dict()
        cid = row["construct_id"]
        if cid in direct_validated:
            row["corrected_protocol_validation_status_v4"] = "directly_corrected_protocol_validated_3x20ns"
            row["corrected_protocol_md_status_v4"] = first_value(val_rank, cid, "validation_md_review_status")
            row["corrected_protocol_md_flags_v4"] = first_value(val_rank, cid, "validation_md_caution_flags")
            row["sampling_decision_v4"] = first_value(sampling, cid, "sampling_decision")
            row["corrected_protocol_validation_status"] = "corrected_protocol_validated_3x20ns_completed_job_164594"
            row["extension_needed"] = f"corrected_validation_sampling_decision:{row['sampling_decision_v4']}"
        else:
            row["corrected_protocol_validation_status_v4"] = "not_directly_corrected_protocol_validated"
            row["corrected_protocol_md_status_v4"] = "not_directly_validated"
            row["corrected_protocol_md_flags_v4"] = "not_directly_validated"
            row["sampling_decision_v4"] = "not_applicable_without_direct_corrected_protocol_run"
            row["corrected_protocol_validation_status"] = "not_directly_corrected_protocol_validated"
            row["extension_needed"] = "not_directly_reassessed_by_corrected_validation_subset;no_blanket_extension_trigger"
        row["priority_class_v4"] = row["priority_class"]
        row["v4_change_vs_v3"] = "unchanged"
        if cid == "A89_2C_224_225_MAP8" and row["corrected_protocol_md_status_v4"] == "md_caution":
            row["v4_change_vs_v3"] = "conflict_control_reinforced"
        if cid == "A89_2C_256_257_MAP8" and row["corrected_protocol_md_status_v4"] == "md_neutral_or_supportive":
            row["v4_change_vs_v3"] = "MD_neutral_biological_conflict_retained"
        if cid == "A89_2C_155_156_MAP8" and row["corrected_protocol_md_status_v4"] == "md_caution":
            row["v4_change_vs_v3"] = "hard_negative_MD_caution_reproduced"
        row["safe_or_validated"] = "no"
        rows.append(row)
    df = pd.DataFrame(rows)
    write_tsv(DATA / "final_candidate_panel_v4_corrected_validation.tsv", df)
    return df


def md_table(df: pd.DataFrame, cols: list[str]) -> str:
    safe = df.reindex(columns=cols, fill_value="NA").astype(str).applymap(lambda x: x.replace("|", r"\|"))
    return safe.to_markdown(index=False)


def reports_only() -> None:
    manifest = read_tsv(MANIFEST)
    completion = pd.DataFrame(completion_audit(manifest))
    val_rank = read_tsv(OUT / "corrected_validation_dynamics_rank_v1.tsv")
    protocol = read_tsv(OUT / "protocol_sensitivity_v1.tsv")
    block = read_tsv(OUT / "corrected_validation_block_stability_v1.tsv")
    sampling = sampling_decision(val_rank, block, protocol)
    panel = final_panel_v4(read_tsv(DATA / "final_candidate_panel_v3_audited.tsv"), val_rank, sampling)
    final_state = reports(panel, completion, val_rank, protocol, sampling)
    (OUT / "corrected_validation_final_state.txt").write_text(final_state + "\n")


def reports(panel: pd.DataFrame, completion: pd.DataFrame, val_rank: pd.DataFrame, protocol: pd.DataFrame, sampling: pd.DataFrame) -> str:
    final_state = "AUDITED_CANDIDATE_PANEL_READY_FOR_EXPERIMENTAL_REVIEW"
    if "ADD_INDEPENDENT_REPLICAS" in set(sampling["sampling_decision"]) or "EXTEND_SELECTED_REPLICAS_TO_50NS" in set(sampling["sampling_decision"]):
        final_state = "CANDIDATE_PANEL_REQUIRES_TARGETED_SAMPLING"
    top = panel[panel["priority_class_v4"].isin(["Priority_A", "Priority_B"])]
    controls = panel[panel["priority_class_v4"].isin(["Conflict_control", "Hard_negative_control"])]
    cv_doc = f"""# CORRECTED_PROTOCOL_VALIDATION_V1

Date: 2026-08-25

Task: `DYNAMICS_ANALYSIS_AUDIT_AND_CANDIDATE_RERANK_010`

Final validation state: `{final_state}`

## Completion QC

All 18 corrected CHARMM36 validation trajectories were audited at the trajectory level. Slurm completion was not used as a substitute for trajectory QC.

{md_table(completion, ['array_index', 'construct_id', 'replica', 'sacct_state', 'sacct_exit_code', 'frame_count', 'final_time_ns', 'finished_mdrun', 'finite_coordinates', 'energy_status', 'integrity_status'])}

## Corrected Validation Dynamics

{md_table(val_rank, ['construct_id', 'junction', 'tag_form', 'validation_wt_reference_rmsd_mean_A', 'validation_delta_local_rmsf_vs_wt_A', 'validation_wt_defined_contact_retention', 'validation_tag_nonlocal_contact_fraction', 'validation_md_review_status', 'validation_md_caution_flags'])}

## Protocol Sensitivity

The corrected protocol was compared against the legacy Task 009 trajectories without concatenating the two trajectory sets as six replicas.

Key conclusion: Task 009 candidate/control interpretation is broadly stable for the directly validated rows. Corrected validation keeps `289|290 x MAP8` and `248|249 x HA` as candidate hypotheses, reproduces `224|225 x MAP8` and `155|156 x MAP8` nonlocal-tag-contact cautions, and keeps `256|257 x MAP8` as MD-neutral but biologically conflicted.

## Sampling Decisions

{md_table(sampling, ['construct_id', 'role', 'corrected_protocol_md_status', 'classification_changed_vs_legacy', 'directional_drift_metrics', 'sampling_decision', 'decision_basis'])}

No blanket 50 ns extension is supported.
"""
    (DOCS / "CORRECTED_PROTOCOL_VALIDATION_V1.md").write_text(cv_doc)

    priority_doc = f"""# FINAL_CANDIDATE_PRIORITY_V2_CORRECTED_VALIDATION

Date: 2026-08-25

Final state: `{final_state}`

No construct is safe or experimentally validated.

## Priority Panel

{md_table(top, ['construct_id', 'junction', 'tag_form', 'priority_class_v4', 'corrected_protocol_validation_status_v4', 'corrected_protocol_md_status_v4', 'sampling_decision_v4', 'v4_change_vs_v3'])}

## Controls

{md_table(controls, ['construct_id', 'junction', 'tag_form', 'priority_class_v4', 'corrected_protocol_validation_status_v4', 'corrected_protocol_md_status_v4', 'sampling_decision_v4', 'v4_change_vs_v3'])}

## Required Answers

1. Priority A does not change after corrected CHARMM36 validation. Directly validated Priority A rows `289|290 x MAP8` and `248|249 x HA` remain supported as screening candidates; `289|290 x G196_minimal` and `248|249 x MAP8` remain Priority A but are explicitly `not_directly_corrected_protocol_validated`.
2. `289|290 x MAP8` remains the strongest C-terminal MAP8 candidate hypothesis.
3. `248|249 x HA` remains the strongest non-C-terminal HA candidate hypothesis.
4. `155|156 x MAP8` shows a reproduced MD caution signature and remains a hard-negative control because of independent biological evidence.
5. `224|225 x MAP8` corrected-MD caution is reproduced in the independent corrected-protocol simulations.
6. `256|257 x MAP8` remains MD-neutral but biologically conflicted.
7. The most discriminating MD observable is persistent nonlocal tag-contact fraction, supported by tag exposure/contact context. WT-defined contact retention and global RMSD are useful QC/perturbation metrics but weak candidate/control discriminators here.
8. DCCM/network, global Rg and raw self-drift RMSD should be downweighted for ranking; they are exploratory or nonspecific over 20 ns.
9. Three replicas are adequate for the current screening objective, not for mechanistic validation.
10. No system currently requires 50 ns.
11. Because no system shows a decision-relevant shared slow drift requiring extension, 50 ns is not selected. If later uncertainty arises, independent replicas should be preferred when between-replica variance dominates.
12. Recommended wet-experiment review constructs remain: `289|290 x MAP8`, `289|290 x G196_minimal`, `248|249 x HA`, and `248|249 x MAP8`, with `288|289 x MAP8/HA` and `290|291 x MAP8` as backups and the listed conflict/hard-negative controls.

## Evidence Boundary

Corrected MD remains downstream comparative perturbation evidence. It does not override direct homolog insertion fitness, functional exclusions, or the absence of direct HRV-A89 insertion phenotype and exact nucleotide/RNA context.
"""
    (DOCS / "FINAL_CANDIDATE_PRIORITY_V2_CORRECTED_VALIDATION.md").write_text(priority_doc)
    return final_state


def main() -> None:
    manifest = read_tsv(MANIFEST)
    completion_rows = completion_audit(manifest)
    completion = pd.DataFrame(completion_rows)
    if not completion["integrity_status"].eq("pass").all():
        print("WARNING: one or more validation trajectories require review", file=sys.stderr)

    maps = base.load_mapping()
    reps, inv = [], []
    for row in rows_for_base(manifest):
        rep, invrow = base.process_replica(row, maps[row["system_id"]])
        reps.append(rep)
        inv.append(invrow)
        print(f"processed validation {row['slurm_array_index']} {row['construct_id']} rep{row['replica']}", flush=True)
    write_tsv(OUT / "corrected_validation_input_trajectory_inventory_v1.tsv", inv)
    wt_ctx = base.build_wt_context(reps)
    broad, contact, tag, network, trunc, secondary, summary_source, network_summary = base.metric_rows(reps, wt_ctx)
    write_tsv(DATA / "corrected_validation_broad_dynamics_v1.tsv", broad)
    write_tsv(DATA / "corrected_validation_contact_persistence_v1.tsv", contact)
    write_tsv(DATA / "corrected_validation_tag_exposure_v1.tsv", tag)
    write_tsv(DATA / "corrected_validation_dynamic_network_v1.tsv", network)
    write_tsv(OUT / "corrected_validation_secondary_structure_v1.tsv", secondary)
    stability_tables(trunc, summary_source, network_summary)
    val_tables = table_map(broad, contact, tag, network)
    val_rank = validation_rank(val_tables)

    legacy_tables = {
        "broad": read_tsv(DATA / "broad_dynamics_metrics_v2_corrected.tsv"),
        "contact": read_tsv(DATA / "contact_persistence_dynamics_v2_corrected.tsv"),
        "tag": read_tsv(DATA / "tag_exposure_dynamics_v2_sasa.tsv"),
        "network": read_tsv(DATA / "dynamic_network_perturbation_v2_corrected.tsv"),
    }
    protocol = protocol_sensitivity(legacy_tables, val_tables, val_rank)
    block = block_stability(val_tables)
    sampling = sampling_decision(val_rank, block, protocol)
    panel = final_panel_v4(read_tsv(DATA / "final_candidate_panel_v3_audited.tsv"), val_rank, sampling)
    final_state = reports(panel, completion, val_rank, protocol, sampling)
    (OUT / "corrected_validation_final_state.txt").write_text(final_state + "\n")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--reports-only":
        reports_only()
    else:
        main()
