#!/usr/bin/env python3
"""Task 010 corrected reanalysis of the Task 009 20 ns MD trajectories."""
from __future__ import annotations

import csv
import hashlib
import math
import os
import re
import subprocess
import tempfile
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

import MDAnalysis as mda
from MDAnalysis.transformations import center_in_box, unwrap
import mdtraj as md
import networkx as nx
import numpy as np
import pandas as pd
from scipy.spatial import cKDTree, distance

ROOT = Path(".")
BD009 = ROOT / "results/broad_dynamics_009"
OUT = ROOT / "results/dynamics_audit_010"
DATA = ROOT / "data"
MANIFEST = BD009 / "production_manifest.tsv"
MAPPING = BD009 / "residue_mapping.tsv"
PANEL = DATA / "balanced_targeted_dynamics_panel_v2.tsv"

BLOCKS = [(0, 5), (5, 10), (10, 15), (15, 20)]
TRUNCATIONS = [10, 15, 20]
BURNINS = [0, 2, 5]
CONTACT_CUTOFF_A = 8.0
TAG_CONTACT_CUTOFF_A = 4.5
WT_CONTACT_OCCUPANCY = 0.50
STABLE_CORE = set(range(122, 305))
FUNCTIONAL_SETS = {
    "walkerA_like_153_166": set(range(153, 167)),
    "walkerB_sensor_like_214_224_248_260": set(range(214, 225)) | set(range(248, 261)),
    "cterm_oligomer_rna_like_286_310": set(range(286, 311)),
}

AA3_TO_1 = {
    "ALA": "A", "ARG": "R", "ASN": "N", "ASP": "D", "CYS": "C",
    "GLN": "Q", "GLU": "E", "GLY": "G", "HIS": "H", "ILE": "I",
    "LEU": "L", "LYS": "K", "MET": "M", "PHE": "F", "PRO": "P",
    "SER": "S", "THR": "T", "TRP": "W", "TYR": "Y", "VAL": "V",
}

# Tien et al.-style empirical maximum ASA values in A^2.
MAX_ASA = {
    "A": 129.0, "R": 274.0, "N": 195.0, "D": 193.0, "C": 167.0,
    "Q": 225.0, "E": 223.0, "G": 104.0, "H": 224.0, "I": 197.0,
    "L": 201.0, "K": 236.0, "M": 224.0, "F": 240.0, "P": 159.0,
    "S": 155.0, "T": 172.0, "W": 285.0, "Y": 263.0, "V": 174.0,
}


@dataclass
class ReplicaData:
    row: dict[str, str]
    times_ns: np.ndarray
    native_a89: list[int]
    ca: np.ndarray
    stable_idx: np.ndarray
    rg_native_ca: np.ndarray
    tag_total_sasa_A2: np.ndarray
    tag_mean_rel_sasa: np.ndarray
    tag_exposed_residue_fraction: np.ndarray
    tag_nonlocal_min_distance_A: np.ndarray
    tag_nonlocal_contact_count: np.ndarray
    tag_end_to_end_A: np.ndarray
    dssp_local: dict[str, float]
    per_tag_sasa_mean_A2: str
    tag_contact_residue_summary: str


def write_tsv(path: Path, rows: list[dict] | pd.DataFrame) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(rows, pd.DataFrame):
        rows.to_csv(path, sep="\t", index=False, na_rep="NA")
        return
    pd.DataFrame(rows).to_csv(path, sep="\t", index=False, na_rep="NA")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def na(v) -> str:
    if v is None:
        return "NA"
    if isinstance(v, float) and not math.isfinite(v):
        return "NA"
    return str(v)


def local_window(junction: str) -> set[int]:
    if "|" not in junction:
        return set()
    left, right = [int(x) for x in junction.split("|")]
    return set(range(max(112, left - 5), min(321, right + 5) + 1))


def kabsch_fit(coords: np.ndarray, ref: np.ndarray, fit_idx: np.ndarray | None = None) -> np.ndarray:
    mob = coords if fit_idx is None else coords[fit_idx]
    tar = ref if fit_idx is None else ref[fit_idx]
    p = mob - mob.mean(axis=0)
    q = tar - tar.mean(axis=0)
    c = p.T @ q
    v, _s, wt = np.linalg.svd(c)
    d = np.sign(np.linalg.det(v @ wt))
    rot = v @ np.diag([1.0, 1.0, d]) @ wt
    return (coords - mob.mean(axis=0)) @ rot + tar.mean(axis=0)


def rmsd_series(aligned: np.ndarray, ref: np.ndarray) -> np.ndarray:
    return np.sqrt(np.mean(np.sum((aligned - ref) ** 2, axis=2), axis=1))


def rmsf(aligned: np.ndarray) -> np.ndarray:
    mean = aligned.mean(axis=0)
    return np.sqrt(np.mean(np.sum((aligned - mean) ** 2, axis=2), axis=0))


def mean_sd(vals: list[float]) -> tuple[float, float]:
    arr = np.array([v for v in vals if math.isfinite(v)], dtype=float)
    if arr.size == 0:
        return math.nan, math.nan
    return float(arr.mean()), float(arr.std(ddof=1) if arr.size > 1 else 0.0)


def bootstrap_ci(vals: list[float], seed: int = 10010) -> tuple[float, float]:
    arr = np.array([v for v in vals if math.isfinite(v)], dtype=float)
    if arr.size < 2:
        return math.nan, math.nan
    rng = np.random.default_rng(seed)
    means = [rng.choice(arr, arr.size, replace=True).mean() for _ in range(1000)]
    return float(np.percentile(means, 2.5)), float(np.percentile(means, 97.5))


def ess_diagnostic(series: np.ndarray) -> tuple[float, float]:
    x = np.asarray(series, dtype=float)
    x = x[np.isfinite(x)]
    if x.size < 8 or np.std(x) == 0:
        return math.nan, math.nan
    x = x - x.mean()
    ac = np.correlate(x, x, mode="full")[x.size - 1 :]
    ac = ac / ac[0]
    pos = []
    for v in ac[1:]:
        if v <= 0:
            break
        pos.append(v)
    tau = 1.0 + 2.0 * float(np.sum(pos))
    return tau, float(x.size / tau) if tau > 0 else math.nan


def block_stats(times: np.ndarray, values: np.ndarray, prefix: str) -> dict[str, float]:
    out = {}
    for a, b in BLOCKS:
        mask = (times >= a) & (times < b if b < 20 else times <= b)
        out[f"{prefix}_{a}_{b}ns_mean"] = float(np.nanmean(values[mask])) if mask.any() else math.nan
    out[f"{prefix}_late_minus_early"] = out.get(f"{prefix}_15_20ns_mean", math.nan) - out.get(f"{prefix}_0_5ns_mean", math.nan)
    return out


def trunc_mean(times: np.ndarray, values: np.ndarray, trunc: int, burnin: int = 0) -> float:
    mask = (times >= burnin) & (times <= trunc)
    return float(np.nanmean(values[mask])) if mask.any() else math.nan


def energy_summary(edr: Path, idx: str) -> dict[str, float | str]:
    if not edr.is_file():
        return {"energy_status": "missing_edr"}
    xvg = Path(tempfile.gettempdir()) / f"dyn010_energy_{idx}.xvg"
    script = (
        "module load gromacs/2024.2 >/dev/null 2>&1; "
        "printf 'Potential\\nKinetic-En.\\nTotal-Energy\\nTemperature\\nPressure\\n0\\n' "
        f"| gmx energy -f {edr} -o {xvg} >/dev/null 2>&1"
    )
    proc = subprocess.run(["bash", "-lc", script], text=True)
    if proc.returncode != 0 or not xvg.is_file():
        return {"energy_status": "gmx_energy_failed"}
    legends, arr = [], []
    for line in xvg.read_text(errors="ignore").splitlines():
        m = re.search(r'@\s+s\d+\s+legend\s+"(.+)"', line)
        if m:
            legends.append(m.group(1))
        if line.startswith(("#", "@")):
            continue
        vals = [float(x) for x in line.split()]
        if len(vals) >= 6:
            arr.append(vals[:6])
    if not arr:
        return {"energy_status": "energy_xvg_empty"}
    a = np.array(arr)
    cols = {name: a[:, i + 1] for i, name in enumerate(legends)}
    out = {"energy_status": "finite" if np.isfinite(a).all() else "nonfinite"}
    for name, key in [
        ("Temperature", "temperature_K"),
        ("Pressure", "pressure_bar"),
        ("Potential", "potential_kjmol"),
        ("Total Energy", "total_energy_kjmol"),
    ]:
        v = cols.get(name)
        if v is None:
            out[f"{key}_mean"] = math.nan
            out[f"{key}_sd"] = math.nan
            out[f"{key}_drift"] = math.nan
        else:
            out[f"{key}_mean"] = float(np.mean(v))
            out[f"{key}_sd"] = float(np.std(v, ddof=1))
            out[f"{key}_drift"] = float(v[-1] - v[0])
    return out


def load_mapping() -> dict[str, pd.DataFrame]:
    df = pd.read_csv(MAPPING, sep="\t", dtype=str).fillna("NA")
    return {sid: g.copy() for sid, g in df.groupby("system_id")}


def selections(u: mda.Universe, map_df: pd.DataFrame) -> dict:
    native = map_df[map_df["residue_class"].eq("native_A89_2C")].copy()
    tag = map_df[map_df["residue_class"].eq("inserted_tag")].copy()
    sim_to_a89 = dict(zip(native["sim_resid"].astype(int), native["native_A89_resid"].astype(int)))
    tag_sim = set(tag["sim_resid"].astype(int).tolist())
    ca_atoms = []
    native_a89 = []
    for atom in u.select_atoms("protein and name CA"):
        if atom.resid in sim_to_a89:
            ca_atoms.append(atom.index)
            native_a89.append(sim_to_a89[atom.resid])
    order = np.argsort(native_a89)
    ca_atoms = [ca_atoms[i] for i in order]
    native_a89 = [native_a89[i] for i in order]
    protein = u.select_atoms("protein")
    protein_resid_order = [res.resid for res in protein.residues]
    tag_residue_positions = [i for i, resid in enumerate(protein_resid_order) if resid in tag_sim]
    tag_atom_idx = [a.index for a in protein if a.resid in tag_sim and not a.name.startswith("H")]
    tag_ca_idx = [a.index for a in protein if a.resid in tag_sim and a.name == "CA"]
    return {
        "protein": protein,
        "native_ca": u.atoms[np.array(ca_atoms, dtype=int)],
        "native_a89": native_a89,
        "sim_to_a89": sim_to_a89,
        "tag_sim": tag_sim,
        "tag_heavy": u.atoms[np.array(tag_atom_idx, dtype=int)] if tag_atom_idx else None,
        "tag_ca": u.atoms[np.array(tag_ca_idx, dtype=int)] if tag_ca_idx else None,
        "protein_resid_order": protein_resid_order,
        "tag_residue_positions": tag_residue_positions,
    }


def process_replica(row: dict[str, str], map_df: pd.DataFrame) -> tuple[ReplicaData, dict]:
    idx = str(row["slurm_array_index"])
    traj = Path(row["trajectory_path"])
    rdir = traj.parent
    tpr = rdir / "prod_20ns.tpr"
    gro = rdir / "prod_20ns.gro"
    log = rdir / "prod_20ns.log"
    edr = Path(row["energy_path"])
    u = mda.Universe(str(tpr), str(traj))
    sel = selections(u, map_df)
    protein = sel["protein"]
    u.trajectory.add_transformations(unwrap(protein), center_in_box(protein, wrap=True))
    native_a89 = sel["native_a89"]
    stable_idx = np.array([i for i, r in enumerate(native_a89) if r in STABLE_CORE], dtype=int)
    win = local_window(row["junction"])
    nonlocal_native_heavy = [
        a.index
        for a in protein
        if (not a.name.startswith("H")) and a.resid in sel["sim_to_a89"] and sel["sim_to_a89"][a.resid] not in win
    ]
    nonlocal_resids = [sel["sim_to_a89"][protein.atoms[np.where(protein.indices == i)[0][0]].resid] for i in nonlocal_native_heavy] if nonlocal_native_heavy else []

    protein_idx = protein.indices.tolist()
    md_top_source = md.load(str(gro), top=str(gro), atom_indices=protein_idx, stride=100000)
    protein_coords = []
    ca_coords = []
    rg = []
    tag_min = []
    tag_contacts = []
    tag_contacted = defaultdict(int)
    tag_end = []
    times = []
    for ts in u.trajectory:
        times.append(ts.time / 1000.0)
        ca = sel["native_ca"].positions.astype(float).copy()
        ca_coords.append(ca)
        rg.append(float(np.sqrt(np.mean(np.sum((ca - ca.mean(axis=0)) ** 2, axis=1)))))
        protein_coords.append(protein.positions.astype(np.float32).copy() / 10.0)
        if sel["tag_heavy"] is not None and nonlocal_native_heavy:
            native_atoms = u.atoms[np.array(nonlocal_native_heavy, dtype=int)]
            tree = cKDTree(native_atoms.positions.astype(float))
            d, nearest = tree.query(sel["tag_heavy"].positions.astype(float), k=1)
            tag_min.append(float(np.min(d)))
            close = d < TAG_CONTACT_CUTOFF_A
            tag_contacts.append(int(np.sum(close)))
            for nidx in np.array(nearest)[close]:
                if nidx < len(nonlocal_resids):
                    tag_contacted[nonlocal_resids[int(nidx)]] += 1
        else:
            tag_min.append(math.nan)
            tag_contacts.append(math.nan)
        if sel["tag_ca"] is not None and len(sel["tag_ca"]) >= 2:
            tag_end.append(float(np.linalg.norm(sel["tag_ca"].positions[0] - sel["tag_ca"].positions[-1])))
        else:
            tag_end.append(math.nan)

    times_arr = np.array(times, dtype=float)
    ca_arr = np.array(ca_coords, dtype=float)
    protein_arr = np.array(protein_coords, dtype=np.float32)
    md_traj = md.Trajectory(protein_arr, md_top_source.topology)
    sasa_A2 = md.shrake_rupley(md_traj, mode="residue") * 100.0
    tag_positions = sel["tag_residue_positions"]
    if tag_positions:
        tag_sasa = sasa_A2[:, tag_positions]
        top_res = list(md_traj.topology.residues)
        rel_cols = []
        per_tag = []
        for pos in tag_positions:
            res = top_res[pos]
            aa = AA3_TO_1.get(res.name.upper(), "X")
            denom = MAX_ASA.get(aa, math.nan)
            rel = tag_sasa[:, tag_positions.index(pos)] / denom if math.isfinite(denom) else np.full(tag_sasa.shape[0], math.nan)
            rel_cols.append(rel)
            per_tag.append(f"{res.name}{pos+1}:{float(np.nanmean(tag_sasa[:, tag_positions.index(pos)])):.2f}")
        rel_arr = np.vstack(rel_cols).T if rel_cols else np.empty((len(times_arr), 0))
        total_sasa = np.sum(tag_sasa, axis=1)
        mean_rel = np.nanmean(rel_arr, axis=1)
        exposed_fraction = np.nanmean(rel_arr >= 0.25, axis=1)
        per_tag_sasa = ";".join(per_tag)
    else:
        total_sasa = np.full(len(times_arr), math.nan)
        mean_rel = np.full(len(times_arr), math.nan)
        exposed_fraction = np.full(len(times_arr), math.nan)
        per_tag_sasa = "WT_no_tag"

    dssp_local = {"local_dssp_H_fraction": math.nan, "local_dssp_E_fraction": math.nan, "local_dssp_C_fraction": math.nan}
    try:
        dssp = md.compute_dssp(md_traj, simplified=True)
        native_positions = [i for i, resid in enumerate(sel["protein_resid_order"]) if resid in sel["sim_to_a89"] and sel["sim_to_a89"][resid] in win]
        if native_positions:
            vals = dssp[:, native_positions].ravel()
            for code, name in [("H", "local_dssp_H_fraction"), ("E", "local_dssp_E_fraction"), ("C", "local_dssp_C_fraction")]:
                dssp_local[name] = float(np.mean(vals == code))
    except Exception:
        dssp_local = {"local_dssp_H_fraction": math.nan, "local_dssp_E_fraction": math.nan, "local_dssp_C_fraction": math.nan}

    contact_summary = ";".join(f"{k}:{v}" for k, v in sorted(tag_contacted.items(), key=lambda kv: (-kv[1], kv[0]))[:10]) or "NA"
    inv = {
        **{k: row.get(k, "") for k in ["system_id", "construct_id", "junction", "tag_form", "replica", "slurm_array_index"]},
        "tpr_path": str(tpr),
        "trajectory_path": str(traj),
        "gro_path": str(gro),
        "edr_path": str(edr),
        "cpt_path": row.get("checkpoint_path", ""),
        "log_path": str(log),
        "tpr_exists": tpr.is_file(),
        "xtc_exists": traj.is_file(),
        "gro_exists": gro.is_file(),
        "edr_exists": edr.is_file(),
        "cpt_exists": Path(row.get("checkpoint_path", "")).is_file(),
        "log_exists": log.is_file(),
        "xtc_size_bytes": traj.stat().st_size if traj.is_file() else 0,
        "final_time_ns": float(times_arr[-1]) if len(times_arr) else math.nan,
        "frame_count": len(times_arr),
        "native_ca_count": len(native_a89),
        "protein_atom_count": len(protein),
        "box_available": bool(np.isfinite(u.trajectory.ts.dimensions[:3]).all()),
        "completion_log_has_finished_mdrun": "Finished mdrun" in log.read_text(errors="ignore") if log.is_file() else False,
        "pbc_transform_status": "mdanalysis_unwrap_center_applied",
    }
    inv.update(energy_summary(edr, idx))
    rep = ReplicaData(
        row=row,
        times_ns=times_arr,
        native_a89=native_a89,
        ca=ca_arr,
        stable_idx=stable_idx,
        rg_native_ca=np.array(rg, dtype=float),
        tag_total_sasa_A2=np.array(total_sasa, dtype=float),
        tag_mean_rel_sasa=np.array(mean_rel, dtype=float),
        tag_exposed_residue_fraction=np.array(exposed_fraction, dtype=float),
        tag_nonlocal_min_distance_A=np.array(tag_min, dtype=float),
        tag_nonlocal_contact_count=np.array(tag_contacts, dtype=float),
        tag_end_to_end_A=np.array(tag_end, dtype=float),
        dssp_local=dssp_local,
        per_tag_sasa_mean_A2=per_tag_sasa,
        tag_contact_residue_summary=contact_summary,
    )
    return rep, inv


def build_wt_context(reps: list[ReplicaData]) -> dict:
    wt = [r for r in reps if r.row["construct_id"] == "WT_112_321"]
    wt = sorted(wt, key=lambda r: int(r.row["replica"]))
    ref_start = wt[0].ca[0]
    fit_idx = np.arange(len(wt[0].native_a89))
    stable_idx = wt[0].stable_idx
    aligned_all = []
    for r in wt:
        aligned_all.extend([kabsch_fit(x, ref_start, fit_idx) for x in r.ca])
    aligned_all = np.array(aligned_all)
    ref_mean = aligned_all.mean(axis=0)
    wt_rmsf_by_rep = {}
    for r in wt:
        aligned = np.array([kabsch_fit(x, ref_start, fit_idx) for x in r.ca])
        wt_rmsf_by_rep[int(r.row["replica"])] = rmsf(aligned)

    n = len(wt[0].native_a89)
    possible = []
    for i in range(n):
        for j in range(i + 4, n):
            possible.append((i, j))
    possible = np.array(possible, dtype=int)
    occ_num = np.zeros(len(possible), dtype=float)
    frame_total = 0
    for r in wt:
        for xyz in r.ca:
            d = np.linalg.norm(xyz[possible[:, 0]] - xyz[possible[:, 1]], axis=1)
            occ_num += d < CONTACT_CUTOFF_A
            frame_total += 1
    occ = occ_num / frame_total
    wt_contacts = possible[occ >= WT_CONTACT_OCCUPANCY]
    wt_contact_occ = occ[occ >= WT_CONTACT_OCCUPANCY]
    return {
        "wt_reps": wt,
        "ref_start": ref_start,
        "ref_mean": ref_mean,
        "fit_idx": fit_idx,
        "stable_idx": stable_idx,
        "wt_rmsf_by_rep": wt_rmsf_by_rep,
        "wt_contacts": wt_contacts,
        "wt_contact_occ": wt_contact_occ,
        "possible_pairs": possible,
        "native_a89": wt[0].native_a89,
    }


def contact_timeseries(ca: np.ndarray, pairs: np.ndarray) -> np.ndarray:
    if len(pairs) == 0:
        return np.full(ca.shape[0], math.nan)
    vals = []
    for xyz in ca:
        d = np.linalg.norm(xyz[pairs[:, 0]] - xyz[pairs[:, 1]], axis=1)
        vals.append(float(np.mean(d < CONTACT_CUTOFF_A)))
    return np.array(vals, dtype=float)


def candidate_start_contacts(ca0: np.ndarray) -> np.ndarray:
    n = ca0.shape[0]
    pairs = []
    for i in range(n):
        for j in range(i + 4, n):
            if np.linalg.norm(ca0[i] - ca0[j]) < CONTACT_CUTOFF_A:
                pairs.append((i, j))
    return np.array(pairs, dtype=int)


def dccm(aligned: np.ndarray) -> np.ndarray:
    disp = aligned - aligned.mean(axis=0)
    denom = np.sqrt(np.mean(np.sum(disp * disp, axis=2), axis=0))
    n = aligned.shape[1]
    out = np.eye(n)
    for i in range(n):
        for j in range(i + 1, n):
            den = denom[i] * denom[j]
            c = np.mean(np.sum(disp[:, i, :] * disp[:, j, :], axis=1)) / den if den else 0.0
            out[i, j] = out[j, i] = c
    return out


def metric_rows(reps: list[ReplicaData], wt_ctx: dict) -> tuple[list[dict], list[dict], list[dict], list[dict], list[dict], list[dict], dict]:
    broad, contact, tag, network, trunc, secondary = [], [], [], [], [], []
    dccm_by_construct = defaultdict(list)
    summary_source = defaultdict(lambda: defaultdict(list))
    wt_ref = wt_ctx["ref_start"]
    wt_mean = wt_ctx["ref_mean"]
    fit_idx = wt_ctx["fit_idx"]
    wt_contacts = wt_ctx["wt_contacts"]
    possible_pairs = wt_ctx["possible_pairs"]
    wt_pair_set = set(map(tuple, wt_contacts.tolist()))
    for rep in reps:
        row = rep.row
        base = {k: row.get(k, "") for k in ["system_id", "construct_id", "junction", "tag_form", "replica", "slurm_array_index"]}
        self_aligned = np.array([kabsch_fit(x, rep.ca[0], fit_idx) for x in rep.ca])
        wt_aligned = np.array([kabsch_fit(x, wt_ref, fit_idx) for x in rep.ca])
        wt_mean_aligned = np.array([kabsch_fit(x, wt_mean, fit_idx) for x in rep.ca])
        stable_self = rmsd_series(self_aligned[:, rep.stable_idx], rep.ca[0][rep.stable_idx])
        self_r = rmsd_series(self_aligned, rep.ca[0])
        wt_r = rmsd_series(wt_aligned, wt_ref)
        wt_mean_r = rmsd_series(wt_mean_aligned, wt_mean)
        rep_rmsf = rmsf(self_aligned)
        win = local_window(row["junction"])
        local_idx = np.array([i for i, r in enumerate(rep.native_a89) if r in win], dtype=int)
        cand_local_rmsf = float(np.mean(rep_rmsf[local_idx])) if len(local_idx) else math.nan
        if row["construct_id"] == "WT_112_321":
            wt_local = math.nan
            delta_local = math.nan
        else:
            wt_vals = [float(np.mean(v[local_idx])) for v in wt_ctx["wt_rmsf_by_rep"].values() if len(local_idx)]
            wt_local = float(np.mean(wt_vals)) if wt_vals else math.nan
            delta_local = cand_local_rmsf - wt_local if math.isfinite(wt_local) else math.nan
        wt_ret_ts = contact_timeseries(rep.ca, wt_contacts)
        local_wt_pairs = np.array([p for p in wt_contacts if rep.native_a89[p[0]] in win or rep.native_a89[p[1]] in win], dtype=int)
        local_wt_ret_ts = contact_timeseries(rep.ca, local_wt_pairs) if len(local_wt_pairs) else np.full(len(rep.times_ns), math.nan)
        cand_pairs = candidate_start_contacts(rep.ca[0])
        cand_start_ts = contact_timeseries(rep.ca, cand_pairs)
        occ = []
        for p in possible_pairs:
            d = np.linalg.norm(rep.ca[:, p[0], :] - rep.ca[:, p[1], :], axis=1)
            occ.append(float(np.mean(d < CONTACT_CUTOFF_A)))
        gain_count = sum(1 for p, o in zip(map(tuple, possible_pairs.tolist()), occ) if p not in wt_pair_set and o >= WT_CONTACT_OCCUPANCY)
        corr = dccm(self_aligned)
        dccm_by_construct[row["construct_id"]].append(corr)
        local_pos = [i for i, r in enumerate(rep.native_a89) if r in win]
        corr_vals, path_vals = [], []
        graph = nx.Graph()
        graph.add_nodes_from(rep.native_a89)
        for p, o in zip(possible_pairs, occ):
            if o >= WT_CONTACT_OCCUPANCY:
                graph.add_edge(rep.native_a89[p[0]], rep.native_a89[p[1]], weight=o)
        for residues in FUNCTIONAL_SETS.values():
            fpos = [i for i, r in enumerate(rep.native_a89) if r in residues]
            if local_pos and fpos:
                corr_vals.append(float(np.mean(np.abs(corr[np.ix_(local_pos, fpos)]))))
            sources = [r for r in rep.native_a89 if r in win and r in graph]
            targets = [r for r in rep.native_a89 if r in residues and r in graph]
            lengths = []
            for s in sources[:12]:
                for t in targets[:12]:
                    try:
                        lengths.append(nx.shortest_path_length(graph, s, t))
                    except nx.NetworkXNoPath:
                        pass
            if lengths:
                path_vals.append(float(np.mean(lengths)))

        tau_r, ess_r = ess_diagnostic(wt_mean_r)
        tau_sasa, ess_sasa = ess_diagnostic(rep.tag_total_sasa_A2)
        b = {
            **base,
            "row_type": "replica",
            "frame_count": len(rep.times_ns),
            "completed_ns": float(rep.times_ns[-1]),
            "pbc_preprocessing": "mdanalysis_unwrap_center_protein",
            "fit_selection": "native_A89_CA_112_321_tag_excluded",
            "stable_core_selection": "A89_122_304_CA",
            "self_drift_rmsd_mean_A": float(np.mean(self_r)),
            "self_drift_rmsd_final_block_A": block_stats(rep.times_ns, self_r, "tmp")["tmp_15_20ns_mean"],
            "self_drift_rmsd_late_minus_early_A": block_stats(rep.times_ns, self_r, "tmp")["tmp_late_minus_early"],
            "stable_core_self_drift_rmsd_mean_A": float(np.mean(stable_self)),
            "wt_reference_start_rmsd_mean_A": float(np.mean(wt_r)),
            "wt_reference_ensemble_rmsd_mean_A": float(np.mean(wt_mean_r)),
            "wt_reference_ensemble_rmsd_late_minus_early_A": block_stats(rep.times_ns, wt_mean_r, "tmp")["tmp_late_minus_early"],
            "native_ca_rg_mean_A": float(np.mean(rep.rg_native_ca)),
            "candidate_local_rmsf_mean_A": cand_local_rmsf,
            "wt_junction_matched_local_rmsf_mean_A": wt_local,
            "delta_local_rmsf_vs_wt_A": delta_local,
            "wt_reference_rmsd_integrated_autocorr_time_frames": tau_r,
            "wt_reference_rmsd_effective_sample_size_frames": ess_r,
        }
        b.update(block_stats(rep.times_ns, self_r, "self_drift_rmsd"))
        b.update(block_stats(rep.times_ns, wt_mean_r, "wt_reference_ensemble_rmsd"))
        broad.append(b)
        c = {
            **base,
            "row_type": "replica",
            "wt_defined_contact_count": len(wt_contacts),
            "wt_defined_contact_retention_mean": float(np.nanmean(wt_ret_ts)),
            "wt_defined_local_contact_count": len(local_wt_pairs),
            "wt_defined_local_contact_retention_mean": float(np.nanmean(local_wt_ret_ts)),
            "candidate_start_contact_count": len(cand_pairs),
            "candidate_start_contact_persistence_mean": float(np.nanmean(cand_start_ts)),
            "new_nonWT_contact_gain_count_occ_ge_0p5": int(gain_count),
        }
        c.update(block_stats(rep.times_ns, wt_ret_ts, "wt_defined_contact_retention"))
        contact.append(c)
        t = {
            **base,
            "row_type": "replica",
            "tag_sasa_method": "MDTraj_shrake_rupley_on_MDAnalysis_PBC_corrected_protein",
            "tag_total_sasa_mean_A2": float(np.nanmean(rep.tag_total_sasa_A2)),
            "tag_total_sasa_sd_A2": float(np.nanstd(rep.tag_total_sasa_A2, ddof=1)),
            "tag_mean_relative_sasa": float(np.nanmean(rep.tag_mean_rel_sasa)),
            "tag_exposed_residue_fraction_rel_sasa_ge_0p25": float(np.nanmean(rep.tag_exposed_residue_fraction)),
            "per_tag_residue_sasa_mean_A2": rep.per_tag_sasa_mean_A2,
            "nonlocal_native_exclusion_window": "junction_left_minus5_to_right_plus5",
            "tag_nonlocal_min_distance_mean_A": float(np.nanmean(rep.tag_nonlocal_min_distance_A)),
            "tag_nonlocal_contact_count_mean_lt_4p5A": float(np.nanmean(rep.tag_nonlocal_contact_count)),
            "tag_nonlocal_contact_fraction_any_lt_4p5A": float(np.nanmean(rep.tag_nonlocal_contact_count > 0)),
            "tag_end_to_end_mean_A": float(np.nanmean(rep.tag_end_to_end_A)),
            "recurrent_nonlocal_contacted_native_residues": rep.tag_contact_residue_summary,
            "tag_sasa_integrated_autocorr_time_frames": tau_sasa,
            "tag_sasa_effective_sample_size_frames": ess_sasa,
        }
        t.update(block_stats(rep.times_ns, rep.tag_total_sasa_A2, "tag_total_sasa"))
        tag.append(t)
        n = {
            **base,
            "row_type": "replica",
            "network_coordinate_basis": "PBC_corrected_native_CA_self_fitted",
            "local_to_functional_abs_dccm_mean": float(np.mean(corr_vals)) if corr_vals else math.nan,
            "persistent_contact_edges_occ_ge_0p5": graph.number_of_edges(),
            "network_components": nx.number_connected_components(graph),
            "local_to_functional_shortest_path_mean_edges": float(np.mean(path_vals)) if path_vals else math.nan,
        }
        network.append(n)
        secondary.append({**base, "row_type": "replica", **rep.dssp_local})
        for metric, values in [
            ("wt_reference_ensemble_rmsd_mean_A", wt_mean_r),
            ("self_drift_rmsd_mean_A", self_r),
            ("wt_defined_contact_retention", wt_ret_ts),
            ("tag_total_sasa_A2", rep.tag_total_sasa_A2),
            ("tag_nonlocal_contact_count", rep.tag_nonlocal_contact_count),
        ]:
            for trunc_to in TRUNCATIONS:
                for burnin in BURNINS:
                    trunc.append({**base, "metric": metric, "burnin_ns": burnin, "truncation_ns": trunc_to, "replica_mean": trunc_mean(rep.times_ns, values, trunc_to, burnin)})
        for key, val in {
            "wt_reference_ensemble_rmsd_mean_A": float(np.mean(wt_mean_r)),
            "self_drift_rmsd_mean_A": float(np.mean(self_r)),
            "delta_local_rmsf_vs_wt_A": delta_local,
            "wt_defined_contact_retention_mean": float(np.nanmean(wt_ret_ts)),
            "tag_total_sasa_mean_A2": float(np.nanmean(rep.tag_total_sasa_A2)),
            "tag_nonlocal_contact_fraction_any_lt_4p5A": float(np.nanmean(rep.tag_nonlocal_contact_count > 0)),
            "local_to_functional_abs_dccm_mean": n["local_to_functional_abs_dccm_mean"],
        }.items():
            summary_source[row["construct_id"]][key].append(val)

    # Append construct summaries to major output tables.
    def append_summary(rows: list[dict], keys: list[str]) -> None:
        by = defaultdict(list)
        for r in rows:
            if r["row_type"] == "replica":
                by[r["construct_id"]].append(r)
        for cid, group in by.items():
            first = group[0]
            s = {k: first.get(k, "") for k in ["system_id", "construct_id", "junction", "tag_form"]}
            s.update({"replica": "summary", "slurm_array_index": "summary", "row_type": "construct_summary", "replica_count": len(group)})
            for k in keys:
                vals = [float(g.get(k, math.nan)) for g in group if str(g.get(k, "NA")) != "NA"]
                m, sd = mean_sd(vals)
                lo, hi = bootstrap_ci(vals)
                s[k] = m
                s[f"{k}_sd_across_replicas"] = sd
                s[f"{k}_bootstrap_ci95_low_n3"] = lo
                s[f"{k}_bootstrap_ci95_high_n3"] = hi
            rows.append(s)

    append_summary(broad, ["self_drift_rmsd_mean_A", "wt_reference_ensemble_rmsd_mean_A", "native_ca_rg_mean_A", "delta_local_rmsf_vs_wt_A"])
    append_summary(contact, ["wt_defined_contact_retention_mean", "wt_defined_local_contact_retention_mean", "candidate_start_contact_persistence_mean", "new_nonWT_contact_gain_count_occ_ge_0p5"])
    append_summary(tag, ["tag_total_sasa_mean_A2", "tag_mean_relative_sasa", "tag_exposed_residue_fraction_rel_sasa_ge_0p25", "tag_nonlocal_contact_fraction_any_lt_4p5A", "tag_nonlocal_contact_count_mean_lt_4p5A"])
    append_summary(network, ["local_to_functional_abs_dccm_mean", "persistent_contact_edges_occ_ge_0p5", "local_to_functional_shortest_path_mean_edges"])
    append_summary(secondary, ["local_dssp_H_fraction", "local_dssp_E_fraction", "local_dssp_C_fraction"])

    # Network stability by construct.
    network_summary = []
    for cid, mats in dccm_by_construct.items():
        cors = []
        for i in range(len(mats)):
            for j in range(i + 1, len(mats)):
                cors.append(float(np.corrcoef(mats[i].ravel(), mats[j].ravel())[0, 1]))
        mean_corr = float(np.mean(cors)) if cors else math.nan
        status = "exploratory_replicated" if math.isfinite(mean_corr) and mean_corr >= 0.5 else "exploratory_unstable"
        network_summary.append({"construct_id": cid, "dccm_replica_pairwise_corr_mean": mean_corr, "dccm_replica_pairwise_corr_min": float(np.min(cors)) if cors else math.nan, "network_status": status, "candidate_tier_authority": "mechanistic_flag_only" if status == "exploratory_replicated" else "zero_tier_authority"})
    return broad, contact, tag, network, trunc, secondary, {k: dict(v) for k, v in summary_source.items()}, network_summary


def provenance() -> None:
    files = [
        MANIFEST,
        MAPPING,
        PANEL,
        DATA / "final_candidate_panel_v2_dynamics.tsv",
        ROOT / "scripts/broad_dynamics_009_analyze_md.py",
        ROOT / "scripts/broad_dynamics_009_gromacs_setup.py",
        ROOT / "scripts/broad_dynamics_009_gmx_production.sbatch",
        BD009 / "gromacs/mdp/prod_20ns.mdp",
        BD009 / "gromacs/mdp/nvt.mdp",
        BD009 / "gromacs/mdp/npt.mdp",
    ]
    rows = []
    for p in files:
        rows.append({"path": str(p), "exists": p.is_file(), "size_bytes": p.stat().st_size if p.is_file() else 0, "sha256": sha256(p) if p.is_file() else "NA"})
    write_tsv(OUT / "input_provenance.tsv", rows)


def write_forcefield_audit() -> None:
    old = BD009 / "gromacs/mdp/prod_20ns.mdp"
    text = old.read_text() if old.is_file() else ""
    required = {
        "constraints": "h-bonds",
        "cutoff-scheme": "Verlet",
        "vdwtype": "cutoff",
        "vdw-modifier": "force-switch",
        "rlist": "1.2",
        "rvdw-switch": "1.0",
        "rvdw": "1.2",
        "coulombtype": "PME",
        "rcoulomb": "1.2",
        "DispCorr": "no",
    }
    found = {}
    for line in text.splitlines():
        if "=" in line and not line.strip().startswith(";"):
            k, v = [x.strip() for x in line.split("=", 1)]
            found[k] = v
    rows = []
    for k, v in required.items():
        rows.append({"setting": k, "task009_value": found.get(k, "MISSING"), "task010_recommended_value": v, "status": "matches" if found.get(k) == v else "differs_or_missing"})
    write_tsv(OUT / "forcefield_protocol_audit.tsv", rows)
    mdp_dir = OUT / "gromacs/mdp"
    mdp_dir.mkdir(parents=True, exist_ok=True)
    common = """dt = 0.002
nsteps = {nsteps}
nstxout-compressed = {nstx}
nstenergy = {nste}
nstlog = {nste}
continuation = {continuation}
constraint_algorithm = lincs
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
tcoupl = V-rescale
tc-grps = Protein Non-Protein
tau_t = 1.0 1.0
ref_t = 300 300
pbc = xyz
gen_vel = {gen_vel}
gen_temp = 300
gen_seed = {seed}
"""
    (mdp_dir / "nvt_corrected.mdp").write_text("define = -DPOSRES\n" + common.format(nsteps=50000, nstx=5000, nste=500, continuation="no", gen_vel="yes", seed=10010) + "pcoupl = no\n")
    (mdp_dir / "npt_corrected.mdp").write_text("define = -DPOSRES\n" + common.format(nsteps=250000, nstx=5000, nste=500, continuation="yes", gen_vel="no", seed=-1) + """pcoupl = C-rescale
pcoupltype = isotropic
tau_p = 5.0
ref_p = 1.0
compressibility = 4.5e-5
refcoord_scaling = com
""")
    (mdp_dir / "prod_20ns_corrected.mdp").write_text(common.format(nsteps=10000000, nstx=50000, nste=5000, continuation="yes", gen_vel="no", seed=-1) + """pcoupl = C-rescale
pcoupltype = isotropic
tau_p = 5.0
ref_p = 1.0
compressibility = 4.5e-5
""")


def write_stability_tables(trunc_rows: list[dict], summary_source: dict, network_summary: list[dict]) -> None:
    trunc_df = pd.DataFrame(trunc_rows)
    grp = trunc_df.groupby(["construct_id", "junction", "tag_form", "metric", "burnin_ns", "truncation_ns"], dropna=False)["replica_mean"]
    trunc_summary = grp.agg(["mean", "std", "count"]).reset_index().rename(columns={"mean": "mean_across_replicas", "std": "sd_across_replicas", "count": "replica_count"})
    write_tsv(OUT / "time_truncation_stability.tsv", trunc_summary)
    rep_rows = []
    for cid, metrics in summary_source.items():
        for metric, vals in metrics.items():
            m, sd = mean_sd(vals)
            lo, hi = bootstrap_ci(vals)
            loro = []
            if len(vals) >= 3:
                for i in range(len(vals)):
                    sub = [v for j, v in enumerate(vals) if j != i]
                    loro.append(float(np.nanmean(sub)))
            rep_rows.append({
                "construct_id": cid,
                "metric": metric,
                "replica_count": len(vals),
                "mean": m,
                "sd_across_replicas": sd,
                "bootstrap_ci95_low_n3": lo,
                "bootstrap_ci95_high_n3": hi,
                "leave_one_replica_out_min": float(np.nanmin(loro)) if loro else math.nan,
                "leave_one_replica_out_max": float(np.nanmax(loro)) if loro else math.nan,
                "replica_agreement": "high_variance" if math.isfinite(m) and math.isfinite(sd) and abs(sd) > max(abs(m) * 0.5, 1e-9) else "moderate_or_better",
            })
    write_tsv(OUT / "replica_stability.tsv", rep_rows)
    write_tsv(OUT / "network_replica_stability.tsv", network_summary)


def write_rank_and_controls(summary_source: dict, network_summary: list[dict]) -> None:
    panel = pd.read_csv(PANEL, sep="\t", dtype=str).fillna("NA")
    net_status = {r["construct_id"]: r["network_status"] for r in network_summary}
    rows = []
    for _, p in panel.iterrows():
        cid = p["construct_id"]
        m = summary_source.get(cid, {})
        wt_rmsd = float(np.nanmean(m.get("wt_reference_ensemble_rmsd_mean_A", [math.nan])))
        drmsf = float(np.nanmean(m.get("delta_local_rmsf_vs_wt_A", [math.nan])))
        contact = float(np.nanmean(m.get("wt_defined_contact_retention_mean", [math.nan])))
        sasa = float(np.nanmean(m.get("tag_total_sasa_mean_A2", [math.nan])))
        nonlocal_frac = float(np.nanmean(m.get("tag_nonlocal_contact_fraction_any_lt_4p5A", [math.nan])))
        flags = []
        if math.isfinite(drmsf) and drmsf > 5:
            flags.append("high_local_RMSF_delta")
        if math.isfinite(contact) and contact < 0.75:
            flags.append("low_WT_contact_retention")
        if math.isfinite(sasa) and sasa < 120:
            flags.append("low_tag_SASA")
        if math.isfinite(nonlocal_frac) and nonlocal_frac > 0.75:
            flags.append("high_nonlocal_tag_contact")
        status = "md_caution" if flags else "md_neutral_or_supportive"
        rows.append({
            "construct_id": cid,
            "junction": p["junction"],
            "tag_form": p["tag_form"],
            "site_region": p["site_region"],
            "wt_reference_rmsd_mean_A": wt_rmsd,
            "delta_local_rmsf_vs_wt_A": drmsf,
            "wt_defined_contact_retention": contact,
            "tag_total_sasa_mean_A2": sasa,
            "tag_nonlocal_contact_fraction": nonlocal_frac,
            "network_status": net_status.get(cid, "NA"),
            "corrected_md_review_status": status,
            "md_caution_flags": ";".join(flags) if flags else "none",
        })
    write_tsv(OUT / "dynamics_rank_stability.tsv", rows)
    controls = []
    for cid in ["A89_2C_155_156_MAP8", "A89_2C_256_257_MAP8"]:
        r = next((x for x in rows if x["construct_id"] == cid), None)
        if r:
            controls.append({
                "construct_id": cid,
                "control_type": "hard_negative" if "155_156" in cid else "conflict_control",
                "corrected_md_review_status": r["corrected_md_review_status"],
                "md_caution_flags": r["md_caution_flags"],
                "interpretation": "md_identifies_perturbation" if r["corrected_md_review_status"] == "md_caution" else "md_does_not_strongly_discriminate_control",
            })
    overall = "partial_discrimination" if any(c["corrected_md_review_status"] == "md_caution" for c in controls) else "no_reliable_discrimination"
    for c in controls:
        c["overall_control_discrimination"] = overall
    write_tsv(OUT / "control_discrimination_audit.tsv", controls)
    ext_rows = []
    for r in rows:
        unstable = "high_local_RMSF_delta" in r["md_caution_flags"] or "low_WT_contact_retention" in r["md_caution_flags"]
        ext_rows.append({
            "construct_id": r["construct_id"],
            "system": f"{r['construct_id']}_112_321",
            "20ns_status": r["corrected_md_review_status"],
            "instability_reason": r["md_caution_flags"],
            "additional_replica_needed": "yes_if_candidate_remains_near_priority_boundary" if unstable else "no",
            "extension_to_50ns_needed": "no_blanket_extension;consider_only_if_corrected_validation_disagrees_or_slow_drift_persists",
            "decision_basis": "corrected_legacy_20ns_replica_block_review",
        })
    write_tsv(OUT / "extension_decision.tsv", ext_rows)


def gmx_cross_validation(reps: list[ReplicaData]) -> None:
    pick_ids = ["WT_112_321", "A89_2C_289_290_MAP8", "A89_2C_224_225_MAP8", "A89_2C_155_156_MAP8"]
    picks = []
    for cid in pick_ids:
        for r in reps:
            if r.row["construct_id"] == cid and r.row["replica"] == "1":
                picks.append(r)
                break
    rows = []
    for rep in picks:
        row = rep.row
        base = Path(row["trajectory_path"]).parent
        tpr = base / "prod_20ns.tpr"
        xtc = base / "prod_20ns.xtc"
        tmp = Path(tempfile.mkdtemp(prefix="dyn010_gmx_"))
        ndx = tmp / "native_ca.ndx"
        u = mda.Universe(str(tpr), str(xtc))
        map_df = load_mapping()[row["system_id"]]
        sim = set(map_df[map_df["residue_class"].eq("native_A89_2C")]["sim_resid"].astype(int))
        idx = [a.index + 1 for a in u.select_atoms("protein and name CA") if a.resid in sim]
        with ndx.open("w") as fh:
            fh.write("[ native_ca ]\n")
            for i, atom in enumerate(idx, 1):
                fh.write(f"{atom:6d}")
                if i % 15 == 0:
                    fh.write("\n")
            fh.write("\n")
        pbc_xtc = tmp / "pbc.xtc"
        first = tmp / "first.gro"
        xvg = tmp / "rmsd.xvg"
        cmds = [
            f"printf 'Protein\\nSystem\\n' | gmx trjconv -s {tpr} -f {xtc} -o {pbc_xtc} -pbc mol -center -ur compact >/dev/null 2>&1",
            f"printf 'System\\n' | gmx trjconv -s {tpr} -f {pbc_xtc} -o {first} -dump 0 >/dev/null 2>&1",
            f"printf 'native_ca\\nnative_ca\\n' | gmx rms -s {first} -f {pbc_xtc} -n {ndx} -o {xvg} -fit rot+trans >/dev/null 2>&1",
        ]
        ok = True
        for cmd in cmds:
            proc = subprocess.run(["bash", "-lc", "module load gromacs/2024.2 >/dev/null 2>&1; " + cmd])
            ok = ok and proc.returncode == 0
        gmx_vals = []
        if ok and xvg.is_file():
            for line in xvg.read_text(errors="ignore").splitlines():
                if line.startswith(("#", "@")):
                    continue
                parts = line.split()
                if len(parts) >= 2:
                    gmx_vals.append(float(parts[1]) * 10.0)
        self_aligned = np.array([kabsch_fit(x, rep.ca[0]) for x in rep.ca])
        py_vals = rmsd_series(self_aligned, rep.ca[0])
        n = min(len(gmx_vals), len(py_vals))
        diff = np.array(gmx_vals[:n]) - py_vals[:n] if n else np.array([])
        rows.append({
            "construct_id": row["construct_id"],
            "replica": row["replica"],
            "gromacs_status": "ok" if ok else "failed",
            "frame_count_compared": n,
            "python_self_rmsd_mean_A": float(np.mean(py_vals[:n])) if n else math.nan,
            "gromacs_self_rmsd_mean_A": float(np.mean(gmx_vals[:n])) if n else math.nan,
            "mean_abs_difference_A": float(np.mean(np.abs(diff))) if n else math.nan,
            "max_abs_difference_A": float(np.max(np.abs(diff))) if n else math.nan,
            "qualitative_agreement": "pass" if n and float(np.mean(np.abs(diff))) < 0.5 else "review_required",
            "note": "GROMACS rms uses trjconv pbc mol center and native_ca index; values converted nm_to_A",
        })
    write_tsv(OUT / "pbc_rmsd_crossvalidation.tsv", rows)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    provenance()
    write_forcefield_audit()
    manifest = pd.read_csv(MANIFEST, sep="\t", dtype=str).fillna("")
    maps = load_mapping()
    reps, inv = [], []
    for row in manifest.to_dict("records"):
        rep, invrow = process_replica(row, maps[row["system_id"]])
        reps.append(rep)
        inv.append(invrow)
        print(f"processed {row['slurm_array_index']} {row['construct_id']} rep{row['replica']}", flush=True)
    write_tsv(OUT / "input_trajectory_inventory.tsv", inv)
    wt_ctx = build_wt_context(reps)
    broad, contact, tag, network, trunc, secondary, summary_source, network_summary = metric_rows(reps, wt_ctx)
    write_tsv(DATA / "broad_dynamics_metrics_v2_corrected.tsv", broad)
    write_tsv(DATA / "contact_persistence_dynamics_v2_corrected.tsv", contact)
    write_tsv(DATA / "tag_exposure_dynamics_v2_sasa.tsv", tag)
    write_tsv(DATA / "dynamic_network_perturbation_v2_corrected.tsv", network)
    write_tsv(OUT / "secondary_structure_persistence.tsv", secondary)
    write_stability_tables(trunc, summary_source, network_summary)
    write_rank_and_controls(summary_source, network_summary)
    gmx_cross_validation(reps)


if __name__ == "__main__":
    main()
