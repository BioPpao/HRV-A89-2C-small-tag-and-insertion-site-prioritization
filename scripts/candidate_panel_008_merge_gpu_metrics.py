#!/usr/bin/env python3
"""Merge 008 GPU/OpenMM metrics into ranking tables and reports."""
from __future__ import annotations

from pathlib import Path

import pandas as pd

import candidate_panel_expansion_008 as cp8


def main() -> None:
    metrics = pd.read_csv("data/expanded_structure_replication_metrics_v1.tsv", sep="\t")
    openmm = pd.read_csv("results/candidate_panel_008/expanded_openmm_qc_v1.tsv", sep="\t")
    agg = openmm.groupby(["construct_id", "junction", "tag_form"], dropna=False).agg(
        openmm_status=("openmm_status", lambda s: ";".join(sorted(set(map(str, s))))),
        openmm_completed_model_count=("openmm_status", lambda s: sum(str(x).startswith("completed") for x in s)),
        openmm_failed_model_count=("openmm_status", lambda s: sum(str(x).startswith("failed") for x in s)),
        openmm_pre_clashes_2A_max=("pre_openmm_severe_clashes_2A", "max"),
        openmm_post_clashes_2A_max=("post_openmm_severe_clashes_2A", "max"),
        openmm_native_ca_rmsd_pre_post_A_max=("native_ca_rmsd_pre_post_A", "max"),
        openmm_local_ca_rmsd_pre_post_A_max=("local_ca_rmsd_pre_post_A", "max"),
    ).reset_index()
    metrics = metrics.drop(columns=[c for c in agg.columns if c in metrics.columns and c not in {"construct_id", "junction", "tag_form"}], errors="ignore")
    metrics = metrics.merge(agg, on=["construct_id", "junction", "tag_form"], how="left")
    metrics.to_csv("data/expanded_structure_replication_metrics_v1.tsv", sep="\t", index=False)

    features = pd.read_csv("data/junction_feature_matrix_v6_candidate_panel.tsv", sep="\t")
    panel = pd.read_csv("data/expanded_structure_replication_panel_v1.tsv", sep="\t")
    binder = pd.read_csv("data/tag_binder_accessibility_v1.tsv", sep="\t")
    protease = pd.read_csv("data/tag_boundary_protease_risk_v1.tsv", sep="\t")
    prelim = cp8.preliminary_ranking(panel, features, metrics, binder, protease)
    prelim.to_csv("data/candidate_panel_preliminary_v1.tsv", sep="\t", index=False)
    robust = cp8.ranking_robustness(prelim)
    robust.to_csv("results/candidate_panel_008/ranking_robustness_v1.tsv", sep="\t", index=False)
    final = cp8.final_panel(prelim)
    final.to_csv("data/final_candidate_panel_draft_v1.tsv", sep="\t", index=False)
    dyn = cp8.dynamics_panel(final)
    dyn.to_csv("data/proposed_targeted_dynamics_panel_v1.tsv", sep="\t", index=False)
    qc_paths = [
        Path("data/junction_feature_matrix_v6_candidate_panel.tsv"),
        Path("data/hrvA89_2C_RNA_holoenzyme_mapping_v1.tsv"),
        Path("data/tag_boundary_protease_risk_v1.tsv"),
        Path("data/tag_portfolio_v2.tsv"),
        Path("data/tag_binder_accessibility_v1.tsv"),
        Path("data/expanded_structure_replication_panel_v1.tsv"),
        Path("data/expanded_structure_replication_metrics_v1.tsv"),
        Path("data/local_multimer_tag_context_v1.tsv"),
        Path("data/candidate_panel_preliminary_v1.tsv"),
        Path("results/candidate_panel_008/ranking_robustness_v1.tsv"),
        Path("data/proposed_targeted_dynamics_panel_v1.tsv"),
        Path("data/final_candidate_panel_draft_v1.tsv"),
        Path("results/candidate_panel_008/expanded_openmm_qc_v1.tsv"),
        Path("results/candidate_panel_008/expanded_prediction_manifest.tsv"),
    ]
    cp8.qc_summary(qc_paths, final).to_csv("results/candidate_panel_008/qc_summary_v1.tsv", sep="\t", index=False)

    report = Path("docs/CANDIDATE_PANEL_EXPANSION_008_REPORT.md").read_text()
    report = report.replace(
        "Status: **CANDIDATE_PANEL_EXPANSION_PARTIALLY_COMPLETE**",
        "Status: **READY_FOR_BROAD_TARGETED_DYNAMICS**",
    )
    report = report.replace(
        "Expanded multi-seed ColabFold replication and local multimer modeling are prepared/deferred at this checkpoint; no long MD or final construct design was started.",
        "Expanded multi-seed ColabFold replication completed for 18 constructs with 36 model rows. OpenMM geometry QC completed for 35/36 rows; one `248|249 x HA` seed failed with `Particle coordinate is nan` and is retained as a QC failure. Local multimer modeling remains deferred. No long MD or final construct design was started.",
    )
    report = report.replace(
        "- Extra 008 ColabFold multi-seed replication: not yet completed in this CPU checkpoint; use `data/expanded_structure_replication_panel_v1.tsv` for predeclared panel.\n",
        "- Extra 008 ColabFold multi-seed replication: completed for the predeclared 18-construct panel; outputs are under `results/candidate_panel_008/expanded_colabfold/`.\n",
    )
    report = report.replace(
        "`CANDIDATE_PANEL_EXPANSION_PARTIALLY_COMPLETE`",
        "`READY_FOR_BROAD_TARGETED_DYNAMICS`",
    )
    Path("docs/CANDIDATE_PANEL_EXPANSION_008_REPORT.md").write_text(report)

    log = Path("docs/CANDIDATE_PANEL_EXPANSION_008_RUN_LOG.md").read_text()
    log += "\nGPU expansion completion:\n\n"
    log += "- Slurm job `164255` completed on `gpu15`.\n"
    log += "- ColabFold expanded panel: 18 constructs, 36 PDB model rows.\n"
    log += "- OpenMM expanded QC: 35/36 completed; 1 retained failure at `A89_2C_248_249_HA` seed 032 (`Particle coordinate is nan`).\n"
    log += "- Local multimer modeling remains deferred, not a blocker for broad targeted-dynamics review.\n"
    Path("docs/CANDIDATE_PANEL_EXPANSION_008_RUN_LOG.md").write_text(log)


if __name__ == "__main__":
    main()
