#!/usr/bin/env python3
"""Analyze real ColabFold inserted structures for OPEN_STRUCTURE_PIPELINE_007."""
from __future__ import annotations

import argparse
import itertools
import math
import re
import subprocess
from pathlib import Path

import mdtraj as md
import numpy as np
import pandas as pd
from Bio.PDB import MMCIFParser, PDBParser
from scipy.spatial import cKDTree

HEX1 = Path("/public/home/yukang/HRV Oligomers/HRV_A89_2C_HEXAMER/results_summary/selected_hexamer_01_md_representative.pdb")
HEX2 = Path("/public/home/yukang/HRV Oligomers/HRV_A89_2C_HEXAMER/results_summary/selected_hexamer_02_md_representative.pdb")


def parse_pdb(path: Path):
    structure = PDBParser(QUIET=True).get_structure(path.stem, str(path))
    atoms = []
    ca = {}
    bfac = {}
    for chain in structure[0]:
        for res in chain:
            het, resid, _ = res.id
            if het != " ":
                continue
            for atom in res:
                element = (atom.element or atom.name[0]).upper()
                rec = (chain.id, int(resid), atom.name.strip(), element, np.asarray(atom.coord, dtype=float), float(atom.bfactor))
                atoms.append(rec)
                if atom.name.strip() == "CA":
                    ca[int(resid)] = np.asarray(atom.coord, dtype=float)
                    bfac[int(resid)] = float(atom.bfactor)
    return atoms, ca, bfac


def kabsch(P: np.ndarray, Q: np.ndarray):
    pc = P.mean(axis=0)
    qc = Q.mean(axis=0)
    P0 = P - pc
    Q0 = Q - qc
    V, _, Wt = np.linalg.svd(P0.T @ Q0)
    d = np.sign(np.linalg.det(V @ Wt))
    D = np.diag([1.0, 1.0, d])
    U = V @ D @ Wt
    return U, pc, qc


def transform(X: np.ndarray, U: np.ndarray, src_center: np.ndarray, dst_center: np.ndarray) -> np.ndarray:
    return (X - src_center) @ U + dst_center


def rmsd(P: np.ndarray, Q: np.ndarray) -> float:
    return float(np.sqrt(np.mean(np.sum((P - Q) ** 2, axis=1))))


def native_tagged_resid(native_resid: int, left: int, tag_len: int) -> int:
    return native_resid if native_resid <= left else native_resid + tag_len


def detect_construct(path: Path, construct_ids: list[str]) -> str:
    name = path.stem.lower()
    for cid in sorted(construct_ids, key=len, reverse=True):
        if cid.lower() in name:
            return cid
    return ""


def collect_models(input_dirs: list[Path], panel: pd.DataFrame) -> pd.DataFrame:
    ids = panel["construct_id"].tolist()
    rows = []
    for d in input_dirs:
        if not d.exists():
            continue
        for pdb in sorted(d.rglob("*.pdb")):
            cid = detect_construct(pdb, ids)
            if not cid:
                continue
            rank = re.search(r"rank_(\d+)", pdb.stem)
            model = re.search(r"model_(\d+)", pdb.stem)
            seed = re.search(r"seed_(\d+)", pdb.stem)
            rows.append({
                "construct_id": cid,
                "model_file": str(pdb),
                "rank": rank.group(1) if rank else "",
                "model": model.group(1) if model else "",
                "seed": seed.group(1) if seed else "",
                "prediction_status": "completed",
            })
    return pd.DataFrame(rows)


def usalign(query: Path, ref: Path, exe: str) -> tuple[str, str]:
    if not exe:
        return "", "USalign_not_available"
    try:
        p = subprocess.run([exe, str(query), str(ref)], capture_output=True, text=True, timeout=60)
        txt = p.stdout + p.stderr
    except Exception as e:
        return "", f"USalign_failed:{e!r}"
    scores = re.findall(r"TM-score=\s*([0-9.]+)", txt)
    return (scores[0] if scores else ""), "completed" if scores else "parse_failed"


def contact_pairs(ca: dict[int, np.ndarray], residues: list[int], cutoff: float = 8.0) -> set[tuple[int, int]]:
    out = set()
    for a, b in itertools.combinations(residues, 2):
        if abs(a - b) <= 2 or a not in ca or b not in ca:
            continue
        if np.linalg.norm(ca[a] - ca[b]) <= cutoff:
            out.add((a, b))
    return out


def heavy_clashes(atoms, cutoff: float = 2.0) -> int:
    heavy = [(c, r, n, xyz) for c, r, n, e, xyz, _b in atoms if e != "H"]
    if len(heavy) < 2:
        return 0
    xyz = np.vstack([x[3] for x in heavy])
    tree = cKDTree(xyz)
    count = 0
    for i, js in enumerate(tree.query_ball_point(xyz, cutoff)):
        ci, ri, _ni, _ = heavy[i]
        for j in js:
            if j <= i:
                continue
            cj, rj, _nj, _ = heavy[j]
            if ci == cj and abs(ri - rj) <= 1:
                continue
            count += 1
    return count


def mdtraj_ss_sasa(path: Path, left: int, tag_len: int) -> dict[str, str | float]:
    try:
        t = md.load(str(path))
        ss = md.compute_dssp(t, simplified=True)[0]
        sasa = md.shrake_rupley(t, mode="residue")[0] * 100.0
        residues = list(t.topology.residues)
        tag_idxs = [i for i, r in enumerate(residues) if left < r.resSeq <= left + tag_len]
        local_native = [native_tagged_resid(r, left, tag_len) for r in range(max(1, left - 3), min(321, left + 4) + 1)]
        local_idxs = [i for i, r in enumerate(residues) if r.resSeq in local_native]
        return {
            "ss_status": "completed",
            "tag_mean_sasa_A2": float(np.mean(sasa[tag_idxs])) if tag_idxs else "",
            "local_coil_fraction": float(np.mean(ss[local_idxs] == "C")) if local_idxs else "",
            "local_helix_fraction": float(np.mean(ss[local_idxs] == "H")) if local_idxs else "",
            "local_sheet_fraction": float(np.mean(ss[local_idxs] == "E")) if local_idxs else "",
            "tag_coil_fraction": float(np.mean(ss[tag_idxs] == "C")) if tag_idxs else "",
        }
    except Exception as e:
        return {"ss_status": f"failed:{e!r}", "tag_mean_sasa_A2": "", "local_coil_fraction": "", "local_helix_fraction": "", "local_sheet_fraction": "", "tag_coil_fraction": ""}


def hexamer_atoms(path: Path):
    atoms, ca, _bf = parse_pdb(path)
    by_chain = {}
    for c, r, n, e, xyz, b in atoms:
        by_chain.setdefault(c, []).append((c, r, n, e, xyz, b))
    ca_by_chain = {}
    for c, rows in by_chain.items():
        ca_by_chain[c] = {r: xyz for _c, r, n, _e, xyz, _b in rows if n == "CA"}
    return by_chain, ca_by_chain


def hexamer_context(model_atoms, model_ca, left: int, tag_len: int, hex_path: Path) -> dict[str, float | str]:
    by_chain, ca_by_chain = hexamer_atoms(hex_path)
    tag_xyz = np.vstack([xyz for _c, r, _n, e, xyz, _b in model_atoms if left < r <= left + tag_len and e != "H"])
    native_res = [r for r in range(1, 322) if r in model_ca and native_tagged_resid(r, left, tag_len) in model_ca]
    if tag_xyz.size == 0 or not native_res:
        return {"status": "failed_no_tag_or_native_ca", "min_tag_neighbor_A": "", "tag_neighbor_clashes_2p5A": "", "tag_neighbor_contacts_5A": ""}
    vals = []
    for chain, chain_ca in ca_by_chain.items():
        common = [r for r in native_res if r in chain_ca]
        if len(common) < 50:
            continue
        P = np.vstack([model_ca[native_tagged_resid(r, left, tag_len)] for r in common])
        Q = np.vstack([chain_ca[r] for r in common])
        U, pc, qc = kabsch(P, Q)
        tag_t = transform(tag_xyz, U, pc, qc)
        other_xyz = np.vstack([xyz for c, _r, _n, e, xyz, _b in sum((v for k, v in by_chain.items() if k != chain), []) if e != "H"])
        d = cKDTree(other_xyz).query(tag_t, k=1)[0]
        vals.append((float(np.min(d)), int(np.sum(d < 2.5)), int(np.sum(d < 5.0))))
    if not vals:
        return {"status": "failed_no_hexamer_fit", "min_tag_neighbor_A": "", "tag_neighbor_clashes_2p5A": "", "tag_neighbor_contacts_5A": ""}
    return {
        "status": "completed",
        "min_tag_neighbor_A": min(v[0] for v in vals),
        "tag_neighbor_clashes_2p5A": max(v[1] for v in vals),
        "tag_neighbor_contacts_5A": max(v[2] for v in vals),
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--panel", type=Path, default=Path("data/tag_site_structure_panel_v3_open.tsv"))
    ap.add_argument("--input-dir", action="append", type=Path, default=[])
    ap.add_argument("--usalign", default=".tools/envs/open_structure_007/bin/USalign")
    args = ap.parse_args()
    panel = pd.read_csv(args.panel, sep="\t")
    models = collect_models(args.input_dir, panel)
    if models.empty:
        models = pd.DataFrame(columns=["construct_id", "model_file", "rank", "model", "seed", "prediction_status"])
    models = models.merge(panel, on="construct_id", how="left")
    models.to_csv("results/open_structure_007/prediction_manifest.tsv", sep="\t", index=False)

    wt_rows = models[models["construct_id"] == "A89_2C_WT"]
    if wt_rows.empty:
        for out in [
            "data/tag_site_structure_ensemble_metrics_v3_open.tsv",
            "data/tag_site_structure_perturbation_v3_open.tsv",
            "data/tag_site_openmm_qc_v1.tsv",
            "data/tag_site_secondary_structure_accessibility_v1.tsv",
            "data/tag_site_hexamer_context_v3_open.tsv",
            "data/tag_site_contact_network_v3_open.tsv",
            "data/tag_site_integrated_perturbation_v3_open.tsv",
            "results/open_structure_007/cross_method_robustness_v3.tsv",
        ]:
            pd.DataFrame([{"status": "failed_no_wt_colabfold_reference"}]).to_csv(out, sep="\t", index=False)
        return

    wt_file = Path(wt_rows.iloc[0]["model_file"])
    wt_atoms, wt_ca, wt_b = parse_pdb(wt_file)
    wt_pairs = contact_pairs(wt_ca, list(range(1, 322)))
    perturb_rows, ss_rows, openmm_rows, hex_rows, net_rows = [], [], [], [], []
    us_exe = args.usalign if Path(args.usalign).exists() else ""

    for _, r in models.iterrows():
        cid = r["construct_id"]
        model_file = Path(r["model_file"])
        atoms, ca, bf = parse_pdb(model_file)
        left = int(r["left_resid"]) if str(r.get("left_resid", "")).strip() not in {"", "nan"} else 0
        tag_len = int(r["tag_length"]) if str(r.get("tag_length", "")).strip() not in {"", "nan"} else 0
        is_wt = cid == "A89_2C_WT"
        if is_wt:
            native_map = {i: i for i in range(1, 322)}
        else:
            native_map = {i: native_tagged_resid(i, left, tag_len) for i in range(1, 322)}
        common = [i for i, j in native_map.items() if i in wt_ca and j in ca]
        P = np.vstack([ca[native_map[i]] for i in common])
        Q = np.vstack([wt_ca[i] for i in common])
        U, pc, qc = kabsch(P, Q)
        Paln = transform(P, U, pc, qc)
        local = [i for i in common if left and max(1, left - 3) <= i <= min(321, left + 4)]
        local_rms = ""
        if local:
            Pl = np.vstack([ca[native_map[i]] for i in local])
            Ql = np.vstack([wt_ca[i] for i in local])
            local_rms = rmsd(transform(Pl, U, pc, qc), Ql)
        tm, tm_status = usalign(model_file, wt_file, us_exe) if not is_wt else ("1.0", "WT_reference")
        native_plddt = np.mean([bf[native_map[i]] for i in common if native_map[i] in bf])
        wt_native_plddt = np.mean([wt_b[i] for i in common if i in wt_b])
        tag_b = [v for resid, v in bf.items() if left < resid <= left + tag_len]
        tag_xyz = [xyz for _c, resid, _n, e, xyz, _b in atoms if tag_len and left < resid <= left + tag_len and e != "H"]
        native_xyz = [xyz for _c, resid, _n, e, xyz, _b in atoms if e != "H" and not (tag_len and left < resid <= left + tag_len)]
        tag_min = ""
        if tag_xyz and native_xyz:
            tag_min = float(np.min(cKDTree(np.vstack(native_xyz)).query(np.vstack(tag_xyz), k=1)[0]))
        perturb_rows.append({
            "construct_id": cid, "junction": r.get("junction", ""), "tag_form": r.get("tag_form", ""),
            "model_file": str(model_file), "native_ca_count": len(common),
            "native_2c_ca_rmsd_to_wt_A": rmsd(Paln, Q),
            "local_window_ca_rmsd_A": local_rms,
            "usalign_tm_score": tm, "usalign_status": tm_status,
            "native_2c_mean_plddt": native_plddt,
            "wt_native_2c_mean_plddt": wt_native_plddt,
            "native_2c_plddt_delta_vs_wt": native_plddt - wt_native_plddt,
            "tag_mean_plddt": float(np.mean(tag_b)) if tag_b else "",
            "tag_native_min_heavy_atom_A": tag_min,
            "severe_clashes_2A_pre_openmm": heavy_clashes(atoms),
        })
        ss = mdtraj_ss_sasa(model_file, left, tag_len)
        ss_rows.append({"construct_id": cid, "junction": r.get("junction", ""), "tag_form": r.get("tag_form", ""), "model_file": str(model_file), **ss})
        openmm_rows.append({
            "construct_id": cid, "junction": r.get("junction", ""), "tag_form": r.get("tag_form", ""),
            "model_file": str(model_file), "openmm_status": "not_minimized_geometry_qc_only",
            "pre_openmm_severe_clashes_2A": heavy_clashes(atoms),
            "post_openmm_severe_clashes_2A": "",
            "method_limit": "OpenMM installed; minimization not run in this parser unless separately authorized for selected structures.",
        })
        if not is_wt:
            for hex_name, hex_path in [("hexamer_01", HEX1), ("hexamer_02", HEX2)]:
                hx = hexamer_context(atoms, ca, left, tag_len, hex_path)
                hex_rows.append({"construct_id": cid, "junction": r.get("junction", ""), "tag_form": r.get("tag_form", ""), "model_file": str(model_file), "hexamer_model": hex_name, **hx})
            tagged_native_ca = {i: ca[j] for i, j in native_map.items() if j in ca}
            tagged_pairs = contact_pairs(tagged_native_ca, list(range(1, 322)))
            local_set = set(range(max(1, left - 3), min(321, left + 4) + 1))
            lost = wt_pairs - tagged_pairs
            gained = tagged_pairs - wt_pairs
            net_rows.append({
                "construct_id": cid, "junction": r.get("junction", ""), "tag_form": r.get("tag_form", ""),
                "model_file": str(model_file), "wt_contact_count": len(wt_pairs),
                "tagged_native_contact_count": len(tagged_pairs),
                "native_contact_loss_count": len(lost),
                "native_contact_gain_count": len(gained),
                "local_contact_loss_count": sum(a in local_set or b in local_set for a, b in lost),
                "local_contact_gain_count": sum(a in local_set or b in local_set for a, b in gained),
            })

    pert = pd.DataFrame(perturb_rows)
    pert.to_csv("data/tag_site_structure_perturbation_v3_open.tsv", sep="\t", index=False)
    pd.DataFrame(ss_rows).to_csv("data/tag_site_secondary_structure_accessibility_v1.tsv", sep="\t", index=False)
    pd.DataFrame(openmm_rows).to_csv("data/tag_site_openmm_qc_v1.tsv", sep="\t", index=False)
    pd.DataFrame(hex_rows).to_csv("data/tag_site_hexamer_context_v3_open.tsv", sep="\t", index=False)
    pd.DataFrame(net_rows).to_csv("data/tag_site_contact_network_v3_open.tsv", sep="\t", index=False)

    nonwt = pert[pert["construct_id"] != "A89_2C_WT"].copy()
    agg = nonwt.groupby(["construct_id", "junction", "tag_form"], dropna=False).agg(
        model_count=("model_file", "count"),
        native_2c_ca_rmsd_mean_A=("native_2c_ca_rmsd_to_wt_A", "mean"),
        native_2c_ca_rmsd_max_A=("native_2c_ca_rmsd_to_wt_A", "max"),
        local_window_ca_rmsd_mean_A=("local_window_ca_rmsd_A", "mean"),
        native_2c_mean_plddt_mean=("native_2c_mean_plddt", "mean"),
        tag_mean_plddt_mean=("tag_mean_plddt", "mean"),
        tag_native_min_heavy_atom_A_min=("tag_native_min_heavy_atom_A", "min"),
        severe_clashes_2A_max=("severe_clashes_2A_pre_openmm", "max"),
    ).reset_index()
    agg["structure_ensemble_status"] = "completed_real_colabfold_models"
    agg.to_csv("data/tag_site_structure_ensemble_metrics_v3_open.tsv", sep="\t", index=False)

    hx = pd.DataFrame(hex_rows)
    net = pd.DataFrame(net_rows)
    hxagg = hx.groupby(["construct_id", "junction", "tag_form"], dropna=False).agg(
        min_tag_neighbor_A=("min_tag_neighbor_A", "min"),
        max_tag_neighbor_clashes_2p5A=("tag_neighbor_clashes_2p5A", "max"),
        max_tag_neighbor_contacts_5A=("tag_neighbor_contacts_5A", "max"),
    ).reset_index() if not hx.empty else pd.DataFrame()
    netagg = net.groupby(["construct_id", "junction", "tag_form"], dropna=False).agg(
        native_contact_loss_mean=("native_contact_loss_count", "mean"),
        local_contact_loss_mean=("local_contact_loss_count", "mean"),
        local_contact_gain_mean=("local_contact_gain_count", "mean"),
    ).reset_index() if not net.empty else pd.DataFrame()
    integrated = agg.merge(panel, on=["construct_id", "junction", "tag_form"], how="left")
    if not hxagg.empty:
        integrated = integrated.merge(hxagg, on=["construct_id", "junction", "tag_form"], how="left")
    if not netagg.empty:
        integrated = integrated.merge(netagg, on=["construct_id", "junction", "tag_form"], how="left")
    integrated["open_structure_interpretation"] = integrated.apply(
        lambda r: "STRUCTURE_MODEL_HIGH_PERTURBATION" if r["native_2c_ca_rmsd_mean_A"] > 4 or r.get("max_tag_neighbor_clashes_2p5A", 0) > 20
        else ("RELATIVELY_LOWER_STRUCTURE_PERTURBATION__DIRECT_CONFLICT" if r["native_2c_ca_rmsd_mean_A"] <= 2.5 and r.get("max_tag_neighbor_clashes_2p5A", 0) <= 5
              else "STRUCTURE_MODEL_MIXED_OR_METHOD_DEPENDENT"),
        axis=1,
    )
    integrated["unresolved_conflicts"] = integrated.apply(
        lambda r: ";".join(x for x in [
            "direct_homolog_insertion_unfavorable" if "deleterious" in str(r.get("insertion_direct_class", "")) else "",
            "functional_tier_" + str(r.get("functional_tier", "")) if str(r.get("functional_tier", "")) in {"EXCLUDE", "HIGH_RISK", "CORE_CAUTION"} else "",
            "no_HRV_A89_specific_insertion_phenotype",
        ] if x),
        axis=1,
    )
    keep = [
        "construct_id", "junction", "tag_form", "model_count", "functional_tier",
        "insertion_raw_log2_enrich2", "insertion_direct_class", "sub_window_mean",
        "independent_indel_event_lower_bound", "plm_percentile_within_tag",
        "native_2c_ca_rmsd_mean_A", "local_window_ca_rmsd_mean_A",
        "native_2c_mean_plddt_mean", "tag_mean_plddt_mean",
        "tag_native_min_heavy_atom_A_min", "severe_clashes_2A_max",
        "min_tag_neighbor_A", "max_tag_neighbor_clashes_2p5A",
        "native_contact_loss_mean", "local_contact_loss_mean",
        "open_structure_interpretation", "unresolved_conflicts",
    ]
    integrated[[c for c in keep if c in integrated.columns]].to_csv("data/tag_site_integrated_perturbation_v3_open.tsv", sep="\t", index=False)
    robust = integrated[["construct_id", "junction", "tag_form", "model_count", "open_structure_interpretation", "unresolved_conflicts"]].copy()
    robust["robustness_status"] = robust["model_count"].map(lambda n: "single_model_only" if n < 2 else "multi_model_available")
    robust.to_csv("results/open_structure_007/cross_method_robustness_v3.tsv", sep="\t", index=False)


if __name__ == "__main__":
    main()
