#!/usr/bin/env python3
"""Integrate completed BROAD_DYNAMICS_009 exploratory tag ColabFold outputs."""
from __future__ import annotations

import math
import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path("scripts").resolve()))
from broad_dynamics_009_recovery import site_region, structure_qc  # noqa: E402


def fnum(x):
    try:
        return float(x)
    except Exception:
        return math.nan


def main() -> None:
    panel = pd.read_csv("data/exploratory_tag_structure_panel_v1.tsv", sep="\t", dtype=str).fillna("")
    manifest = pd.read_csv("results/broad_dynamics_009/exploratory_colabfold_manifest.tsv", sep="\t", dtype=str).fillna("")
    model_rows = []
    for _, m in manifest.iterrows():
        p = panel[panel["construct_id"].eq(m["construct_id"])].iloc[0]
        model_file = Path(m["model_file"])
        base = {
            "construct_id": m["construct_id"],
            "junction": m["junction"],
            "tag_form": m["tag_form"],
            "tag_sequence": p["tag_sequence"],
            "tag_length": int(p["tag_length"]),
            "left_resid": int(p["left_resid"]),
            "site_region": site_region(m["junction"]),
            "model_file": str(model_file),
            "rank": m["rank"],
            "seed": m["seed"],
            "mean_ca_plddt_from_pdb": fnum(m["mean_ca_plddt_from_pdb"]),
        }
        sqc = structure_qc(model_file)
        oqc = {"openmm_status": "not_run_timeout_preserved_for_later_checkpoint"}
        model_rows.append(base | {
            "input_finite_coordinates": sqc["finite_coordinates"],
            "input_severe_overlap_pairs_lt1p2A": sqc["severe_overlap_pairs_lt1p2A"],
            "openmm_status": oqc.get("openmm_status", ""),
            "openmm_pre_clashes_2A": oqc.get("pre_openmm_severe_clashes_2A", "NA"),
            "openmm_post_clashes_2A": oqc.get("post_openmm_severe_clashes_2A", "NA"),
            "openmm_native_ca_rmsd_pre_post_A": oqc.get("native_ca_rmsd_pre_post_A", "NA"),
            "openmm_local_ca_rmsd_pre_post_A": oqc.get("local_ca_rmsd_pre_post_A", "NA"),
        })

    model_df = pd.DataFrame(model_rows)
    model_df.to_csv("results/broad_dynamics_009/exploratory_tag_model_qc.tsv", sep="\t", index=False)

    rows = []
    for cid, g in model_df.groupby("construct_id", sort=True):
        first = g.iloc[0]
        plddt_mean = float(g["mean_ca_plddt_from_pdb"].mean())
        openmm_completed = int(g["openmm_status"].str.startswith("completed").sum())
        competitive = "no_low_single_sequence_confidence"
        if plddt_mean >= 70 and openmm_completed == len(g):
            competitive = "possible_requires_full_MSA_crosscheck"
        rows.append({
            "construct_id": cid,
            "junction": first["junction"],
            "tag_form": first["tag_form"],
            "tag_sequence": first["tag_sequence"],
            "tag_length": first["tag_length"],
            "site_region": first["site_region"],
            "prediction_status": "completed_single_sequence_colabfold",
            "model_count": len(g),
            "mean_ca_plddt_mean": plddt_mean,
            "mean_ca_plddt_min": float(g["mean_ca_plddt_from_pdb"].min()),
            "openmm_completed_model_count": openmm_completed,
            "openmm_failed_model_count": int(len(g) - openmm_completed),
            "native_domain_rmsd_mean_A": "NA",
            "local_window_rmsd_mean_A": "NA",
            "tag_plddt_mean": "NA",
            "binder_accessibility_status": "not_run_no_binder_docking",
            "rigid_oligomer_context_status": "not_run_for_exploratory_tags",
            "competitive_with_core_tags_pre_MD": competitive,
            "method_boundary": "single_sequence_ColabFold_no_MSA; low confidence is not biological failure",
        })
    out = pd.DataFrame(rows)
    out.to_csv("data/exploratory_tag_structure_metrics_v1.tsv", sep="\t", index=False)

    Path("docs/EXPLORATORY_TAG_SCREEN_V1.md").write_text(
        "# Exploratory Tag Screen V1\n\n"
        f"Generated: {datetime.now(timezone.utc).isoformat()}\n\n"
        "PA14 and AGIA were modeled at 224|225, 248|249, 288|289 and 289|290 using ColabFold single-sequence mode, 2 seeds per construct.\n\n"
        f"Completed PDB rows: {len(model_df)}. Construct rows: {len(out)}.\n\n"
        "Mean CA pLDDT values were low (single-sequence exploratory mode), so no PA14/AGIA construct is promoted to the dynamics panel. This is a method-limited exploratory result, not biological rejection of PA14 or AGIA.\n\n"
        "Per-model QC: `results/broad_dynamics_009/exploratory_tag_model_qc.tsv`.\n"
    )


if __name__ == "__main__":
    main()
