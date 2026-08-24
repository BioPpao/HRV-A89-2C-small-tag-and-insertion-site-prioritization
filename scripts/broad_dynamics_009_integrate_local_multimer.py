#!/usr/bin/env python3
"""Parse focused local multimer ColabFold outputs into task 009 tables."""
from __future__ import annotations

import json
import math
import re
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.spatial import cKDTree

OUT = Path("results/broad_dynamics_009/local_multimer")


def fnum(x):
    try:
        return float(x)
    except Exception:
        return math.nan


def score_json(pdb: Path) -> dict:
    m = re.sub(r"_unrelaxed_", "_scores_", pdb.stem)
    js = pdb.with_name(m + ".json")
    if not js.exists():
        return {}
    try:
        data = json.loads(js.read_text())
    except Exception:
        return {}
    out = {}
    for k in ["iptm", "ptm", "ranking_confidence"]:
        v = data.get(k, "")
        if isinstance(v, float) and math.isnan(v):
            v = "NA"
        out[k] = v
    return out


def atoms(path: Path) -> list[dict]:
    rows = []
    for line in path.read_text(errors="ignore").splitlines():
        if not line.startswith("ATOM"):
            continue
        name = line[12:16].strip()
        element = (line[76:78].strip() or name[0]).upper()
        if element == "H":
            continue
        rows.append({
            "name": name,
            "chain": line[21].strip() or "A",
            "resid": int(line[22:26]),
            "xyz": np.array([float(line[30:38]), float(line[38:46]), float(line[46:54])], dtype=float),
        })
    return rows


def metrics(path: Path, left: int, tag_len: int) -> dict:
    a = atoms(path)
    if any(not np.all(np.isfinite(x["xyz"])) for x in a):
        return {
            "coordinate_status": "nonfinite_coordinates",
            "tag_neighbor_min_distance_A": "NA",
            "inter_protomer_clash_count_2p5A": "NA",
            "interface_contacts_8A": "NA",
            "chain_count": len(set(x["chain"] for x in a)) if a else "NA",
        }
    tag = [x for x in a if x["chain"] == "A" and left < x["resid"] <= left + tag_len]
    neigh = [x for x in a if x["chain"] != "A"]
    if not tag or not neigh:
        return {
            "coordinate_status": "finite_but_missing_tag_or_neighbor",
            "tag_neighbor_min_distance_A": "NA",
            "inter_protomer_clash_count_2p5A": "NA",
            "interface_contacts_8A": "NA",
            "chain_count": len(set(x["chain"] for x in a)),
        }
    tag_xyz = np.vstack([x["xyz"] for x in tag])
    neigh_xyz = np.vstack([x["xyz"] for x in neigh])
    tree = cKDTree(neigh_xyz)
    d, _ = tree.query(tag_xyz, k=1)
    clashes = sum(len(tree.query_ball_point(x, 2.5)) for x in tag_xyz)
    a_ca = [x for x in a if x["chain"] == "A" and x["name"] == "CA" and not (left < x["resid"] <= left + tag_len)]
    n_ca = [x for x in neigh if x["name"] == "CA"]
    contacts = 0
    if a_ca and n_ca:
        ntree = cKDTree(np.vstack([x["xyz"] for x in n_ca]))
        contacts = sum(len(ntree.query_ball_point(x["xyz"], 8.0)) for x in a_ca)
    return {
        "coordinate_status": "finite",
        "tag_neighbor_min_distance_A": float(np.min(d)),
        "inter_protomer_clash_count_2p5A": int(clashes),
        "interface_contacts_8A": int(contacts),
        "chain_count": len(set(x["chain"] for x in a)),
    }


def main() -> None:
    targets = pd.read_csv(OUT / "local_multimer_targets.tsv", sep="\t", dtype=str).fillna("")
    rows = []
    for _, t in targets.iterrows():
        target = t["target_id"]
        pdbs = sorted((OUT / "output").glob(f"{target}_unrelaxed_rank_*_*.pdb"))
        if not pdbs:
            rows.append({
                **t.to_dict(),
                "model_file": "",
                "rank": "",
                "seed": "",
                "prediction_status": "failed_no_pdb_found",
                "iptm": "NA",
                "ptm": "NA",
                "ranking_confidence": "NA",
                "coordinate_status": "NA",
                "tag_neighbor_min_distance_A": "NA",
                "inter_protomer_clash_count_2p5A": "NA",
                "interface_contacts_8A": "NA",
                "chain_count": "NA",
            })
            continue
        for pdb in pdbs:
            rank = re.search(r"rank_(\d+)", pdb.stem)
            seed = re.search(r"seed_(\d+)", pdb.stem)
            met = metrics(pdb, int(t["left_resid"]), int(t["tag_length"]))
            sc = score_json(pdb)
            rows.append({
                **t.to_dict(),
                "model_file": str(pdb),
                "rank": rank.group(1) if rank else "",
                "seed": seed.group(1) if seed else "",
                "prediction_status": "completed" if met.get("coordinate_status") == "finite" else f"completed_{met.get('coordinate_status', 'metric_warning')}",
                "iptm": sc.get("iptm", "NA"),
                "ptm": sc.get("ptm", "NA"),
                "ranking_confidence": sc.get("ranking_confidence", "NA"),
                **met,
            })
    model_df = pd.DataFrame(rows)
    model_df.to_csv(OUT / "local_multimer_model_metrics.tsv", sep="\t", index=False)

    agg = []
    for cid, g in model_df.groupby("construct_id", sort=False):
        first = g.iloc[0]
        ok = g[g["prediction_status"].eq("completed")]
        if len(ok):
            min_dist = min(fnum(x) for x in ok["tag_neighbor_min_distance_A"])
            max_clash = max(fnum(x) for x in ok["inter_protomer_clash_count_2p5A"])
            iptm_vals = [fnum(x) for x in ok["iptm"] if not math.isnan(fnum(x))]
            iptm = float(np.mean(iptm_vals)) if iptm_vals else "NA"
            status = "completed_single_sequence_multimer"
            accom = "tag_neighbor_contact_or_clash_detected" if (not math.isnan(min_dist) and min_dist < 2.5) or (not math.isnan(max_clash) and max_clash > 0) else "no_tag_neighbor_clash_in_model"
        else:
            min_dist = "NA"; max_clash = "NA"; iptm = "NA"
            if len(g) and g["prediction_status"].astype(str).str.contains("nonfinite_coordinates").all():
                status = "completed_all_models_nonfinite_coordinates"
                accom = "inconclusive_nonfinite_multimer_coordinates"
            else:
                status = "failed_no_pdb_found"
                accom = "not_assessable"
        agg.append({
            "construct_id": cid,
            "junction": first["junction"],
            "tag_form": first["tag_form"],
            "site_region": first.get("site_region", ""),
            "multimer_context": first["multimer_context"],
            "status": status,
            "ipTM": iptm,
            "tag_neighbor_min_distance_A": min_dist,
            "inter_protomer_clash_count": max_clash,
            "interface_contact_change": "NA_no_rigid_relaxed_pair",
            "accommodation_vs_rigid": accom,
            "hexamer_hypothesis_consistency": "not_tested_single_trimer_context",
            "boundary": "single_sequence_AF2_multimer_trimer; local accommodation cross-check only",
        })
    out = pd.DataFrame(agg)
    out.to_csv("data/local_multimer_tag_context_v2.tsv", sep="\t", index=False)
    out.to_csv("results/broad_dynamics_009/local_multimer_manifest.tsv", sep="\t", index=False)
    Path("docs/LOCAL_MULTIMER_RECOVERY_V2.md").write_text(
        "# Local Multimer Recovery V2\n\n"
        f"Focused local trimer modeling completed for {len(out)} constructs using single-sequence AlphaFold2 multimer.\n\n"
        "Context: tagged protomer plus two WT protomers. This is a tractable local accommodation cross-check, not a full A89 hexamer prediction and not biological validation.\n\n"
        "Outputs: `results/broad_dynamics_009/local_multimer/local_multimer_model_metrics.tsv` and `data/local_multimer_tag_context_v2.tsv`.\n"
    )


if __name__ == "__main__":
    main()
