#!/usr/bin/env python3
"""Analyze CANDIDATE_PANEL_EXPANSION_008 expanded ColabFold models."""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

import open_structure_007_analyze_models as os7


def native_tagged_resid(native_resid: int, left: int, tag_len: int) -> int:
    return native_resid if native_resid <= left else native_resid + tag_len


def main() -> None:
    out = Path("results/candidate_panel_008")
    panel = pd.read_csv("data/expanded_structure_replication_panel_v1.tsv", sep="\t")
    models = os7.collect_models([Path("results/open_structure_007/wt_smoke"), Path("results/candidate_panel_008/expanded_colabfold")], panel)
    models = models.merge(panel, on="construct_id", how="left")
    models.to_csv(out / "expanded_prediction_manifest.tsv", sep="\t", index=False)
    wt = models[models["construct_id"] == "A89_2C_WT"]
    if wt.empty:
        # collect_models will not find WT because the expanded panel lacks it.
        wt_file = Path("results/open_structure_007/wt_smoke/A89_2C_WT_unrelaxed_rank_001_alphafold2_ptm_model_1_seed_007.pdb")
    else:
        wt_file = Path(wt.iloc[0]["model_file"])
    wt_atoms, wt_ca, wt_b = os7.parse_pdb(wt_file)
    wt_pairs = os7.contact_pairs(wt_ca, list(range(1, 322)))
    us_exe = ".tools/envs/open_structure_007/bin/USalign"
    us_exe = us_exe if Path(us_exe).exists() else ""

    perturb, ss_rows, hex_rows, net_rows = [], [], [], []
    for _, r in models.iterrows():
        if r["construct_id"] == "A89_2C_WT":
            continue
        model_file = Path(r["model_file"])
        atoms, ca, bf = os7.parse_pdb(model_file)
        left = int(r["left_resid"])
        tag_len = int(r["tag_length"])
        native_map = {i: native_tagged_resid(i, left, tag_len) for i in range(1, 322)}
        common = [i for i, j in native_map.items() if i in wt_ca and j in ca]
        P = np.vstack([ca[native_map[i]] for i in common])
        Q = np.vstack([wt_ca[i] for i in common])
        U, pc, qc = os7.kabsch(P, Q)
        Paln = os7.transform(P, U, pc, qc)
        local = [i for i in common if max(1, left - 3) <= i <= min(321, left + 4)]
        local_rms = ""
        if local:
            Pl = np.vstack([ca[native_map[i]] for i in local])
            Ql = np.vstack([wt_ca[i] for i in local])
            local_rms = os7.rmsd(os7.transform(Pl, U, pc, qc), Ql)
        tm, tm_status = os7.usalign(model_file, wt_file, us_exe)
        native_plddt = np.mean([bf[native_map[i]] for i in common if native_map[i] in bf])
        wt_native_plddt = np.mean([wt_b[i] for i in common if i in wt_b])
        tag_b = [v for resid, v in bf.items() if left < resid <= left + tag_len]
        tag_xyz = [xyz for _c, resid, _n, e, xyz, _b in atoms if left < resid <= left + tag_len and e != "H"]
        native_xyz = [xyz for _c, resid, _n, e, xyz, _b in atoms if e != "H" and not (left < resid <= left + tag_len)]
        tag_min = ""
        if tag_xyz and native_xyz:
            tag_min = float(np.min(os7.cKDTree(np.vstack(native_xyz)).query(np.vstack(tag_xyz), k=1)[0]))
        perturb.append({
            "construct_id": r["construct_id"], "junction": r["junction"], "tag_form": r["tag_form"],
            "model_file": str(model_file), "rank": r.get("rank", ""), "seed": r.get("seed", ""),
            "native_ca_count": len(common), "native_2c_ca_rmsd_to_wt_A": os7.rmsd(Paln, Q),
            "local_window_ca_rmsd_A": local_rms, "usalign_tm_score": tm, "usalign_status": tm_status,
            "native_2c_mean_plddt": native_plddt, "wt_native_2c_mean_plddt": wt_native_plddt,
            "native_2c_plddt_delta_vs_wt": native_plddt - wt_native_plddt,
            "tag_mean_plddt": float(np.mean(tag_b)) if tag_b else "",
            "tag_native_min_heavy_atom_A": tag_min,
            "severe_clashes_2A_pre_openmm": os7.heavy_clashes(atoms),
        })
        ss_rows.append({"construct_id": r["construct_id"], "junction": r["junction"], "tag_form": r["tag_form"], "model_file": str(model_file), **os7.mdtraj_ss_sasa(model_file, left, tag_len)})
        for hex_name, hex_path in [("hexamer_01", os7.HEX1), ("hexamer_02", os7.HEX2)]:
            hex_rows.append({"construct_id": r["construct_id"], "junction": r["junction"], "tag_form": r["tag_form"], "model_file": str(model_file), "hexamer_model": hex_name, **os7.hexamer_context(atoms, ca, left, tag_len, hex_path)})
        tagged_native_ca = {i: ca[j] for i, j in native_map.items() if j in ca}
        tagged_pairs = os7.contact_pairs(tagged_native_ca, list(range(1, 322)))
        local_set = set(range(max(1, left - 3), min(321, left + 4) + 1))
        lost = wt_pairs - tagged_pairs
        gained = tagged_pairs - wt_pairs
        net_rows.append({
            "construct_id": r["construct_id"], "junction": r["junction"], "tag_form": r["tag_form"],
            "model_file": str(model_file), "wt_contact_count": len(wt_pairs),
            "tagged_native_contact_count": len(tagged_pairs), "native_contact_loss_count": len(lost),
            "native_contact_gain_count": len(gained),
            "local_contact_loss_count": sum(a in local_set or b in local_set for a, b in lost),
            "local_contact_gain_count": sum(a in local_set or b in local_set for a, b in gained),
        })

    pert = pd.DataFrame(perturb)
    for col in [
        "native_2c_ca_rmsd_to_wt_A", "local_window_ca_rmsd_A", "usalign_tm_score",
        "native_2c_mean_plddt", "tag_mean_plddt", "severe_clashes_2A_pre_openmm",
    ]:
        pert[col] = pd.to_numeric(pert[col], errors="coerce")
    pert.to_csv("results/candidate_panel_008/expanded_structure_perturbation_model_rows_v1.tsv", sep="\t", index=False)
    pd.DataFrame(ss_rows).to_csv("results/candidate_panel_008/expanded_secondary_accessibility_model_rows_v1.tsv", sep="\t", index=False)
    pd.DataFrame(hex_rows).to_csv("results/candidate_panel_008/expanded_hexamer_context_model_rows_v1.tsv", sep="\t", index=False)
    pd.DataFrame(net_rows).to_csv("results/candidate_panel_008/expanded_contact_network_model_rows_v1.tsv", sep="\t", index=False)

    agg = pert.groupby(["construct_id", "junction", "tag_form"], dropna=False).agg(
        model_count=("model_file", "count"),
        native_domain_rmsd_mean_A=("native_2c_ca_rmsd_to_wt_A", "mean"),
        native_domain_rmsd_max_A=("native_2c_ca_rmsd_to_wt_A", "max"),
        local_window_rmsd_mean_A=("local_window_ca_rmsd_A", "mean"),
        local_window_rmsd_max_A=("local_window_ca_rmsd_A", "max"),
        usalign_tm_score_mean=("usalign_tm_score", "mean"),
        native_plddt_mean=("native_2c_mean_plddt", "mean"),
        tag_plddt_mean=("tag_mean_plddt", "mean"),
        severe_clashes_2A_pre_openmm_max=("severe_clashes_2A_pre_openmm", "max"),
    ).reset_index()
    hx = pd.DataFrame(hex_rows).groupby(["construct_id", "junction", "tag_form"], dropna=False).agg(
        min_tag_neighbor_A=("min_tag_neighbor_A", "min"),
        hexamer_tag_neighbor_clashes_2p5A_max=("tag_neighbor_clashes_2p5A", "max"),
    ).reset_index()
    net = pd.DataFrame(net_rows).groupby(["construct_id", "junction", "tag_form"], dropna=False).agg(
        native_contact_loss_mean=("native_contact_loss_count", "mean"),
        local_contact_loss_mean=("local_contact_loss_count", "mean"),
    ).reset_index()
    merged = panel.merge(agg, on=["construct_id", "junction", "tag_form"], how="left").merge(hx, on=["construct_id", "junction", "tag_form"], how="left").merge(net, on=["construct_id", "junction", "tag_form"], how="left")
    merged["structure_replication_status"] = "completed_candidate_panel_008_colabfold_2seed"
    merged["seed_robustness_status"] = merged["model_count"].map(lambda x: "multi_seed_completed" if int(x) >= 2 else "incomplete")
    merged.to_csv("data/expanded_structure_replication_metrics_v1.tsv", sep="\t", index=False)


if __name__ == "__main__":
    main()
