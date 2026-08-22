#!/usr/bin/env python3
"""Merge OpenMM QC fields into integrated OPEN_STRUCTURE_PIPELINE_007 table."""
import pandas as pd

integrated = pd.read_csv("data/tag_site_integrated_perturbation_v3_open.tsv", sep="\t")
openmm = pd.read_csv("data/tag_site_openmm_qc_v1.tsv", sep="\t")
openmm = openmm[openmm["junction"] != "WT"].copy()
agg = openmm.groupby(["construct_id", "junction", "tag_form"], dropna=False).agg(
    openmm_status=("openmm_status", lambda s: ";".join(sorted(set(map(str, s))))),
    openmm_pre_clashes_2A_max=("pre_openmm_severe_clashes_2A", "max"),
    openmm_post_clashes_2A_max=("post_openmm_severe_clashes_2A", "max"),
    openmm_native_ca_rmsd_pre_post_A=("native_ca_rmsd_pre_post_A", "max"),
    openmm_local_ca_rmsd_pre_post_A=("local_ca_rmsd_pre_post_A", "max"),
).reset_index()

drop = [c for c in agg.columns if c in integrated.columns and c not in {"construct_id", "junction", "tag_form"}]
integrated = integrated.drop(columns=drop, errors="ignore")
integrated = integrated.merge(agg, on=["construct_id", "junction", "tag_form"], how="left")
integrated.to_csv("data/tag_site_integrated_perturbation_v3_open.tsv", sep="\t", index=False)

robust = pd.read_csv("results/open_structure_007/cross_method_robustness_v3.tsv", sep="\t")
robust = robust.drop(columns=[c for c in agg.columns if c in robust.columns and c not in {"construct_id", "junction", "tag_form"}], errors="ignore")
robust = robust.merge(agg[["construct_id", "junction", "tag_form", "openmm_status", "openmm_post_clashes_2A_max"]], on=["construct_id", "junction", "tag_form"], how="left")
robust.to_csv("results/open_structure_007/cross_method_robustness_v3.tsv", sep="\t", index=False)
