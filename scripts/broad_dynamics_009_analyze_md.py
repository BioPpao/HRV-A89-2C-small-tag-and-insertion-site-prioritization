#!/usr/bin/env python3
"""Analyze completed BROAD_DYNAMICS_009 20 ns trajectories.

The script is deliberately compact and auditable: it reads the existing
GROMACS outputs, writes compact TSV metrics, and does not modify trajectories.
"""
from __future__ import annotations

import csv
import math
import re
import subprocess
import tempfile
from collections import defaultdict
from pathlib import Path

import MDAnalysis as mda
import networkx as nx
import numpy as np
import pandas as pd
from scipy.spatial import cKDTree, distance

ROOT = Path(".")
RESULT = ROOT / "results/broad_dynamics_009"
DATA = ROOT / "data"
MANIFEST = RESULT / "production_manifest.tsv"
COMPLETION = RESULT / "replica_completion.tsv"
MAPPING = RESULT / "residue_mapping.tsv"
LOGDIR = RESULT / "logs"

FUNCTIONAL_SETS = {
    "walkerA_like_153_166": range(153, 167),
    "walkerB_sensor_like_214_224_248_260": list(range(214, 225)) + list(range(248, 261)),
    "cterm_oligomer_rna_like_286_310": range(286, 311),
}


def na(v) -> str:
    if v is None:
        return "NA"
    try:
        if isinstance(v, float) and not math.isfinite(v):
            return "NA"
    except TypeError:
        pass
    return str(v)


def mean_sd(values: list[float]) -> tuple[float, float]:
    vals = np.array([v for v in values if math.isfinite(v)], dtype=float)
    if vals.size == 0:
        return math.nan, math.nan
    return float(vals.mean()), float(vals.std(ddof=1) if vals.size > 1 else 0.0)


def bootstrap_ci(values: list[float], seed: int = 9009) -> tuple[float, float]:
    vals = np.array([v for v in values if math.isfinite(v)], dtype=float)
    if vals.size < 2:
        return math.nan, math.nan
    rng = np.random.default_rng(seed)
    means = [rng.choice(vals, vals.size, replace=True).mean() for _ in range(1000)]
    return float(np.percentile(means, 2.5)), float(np.percentile(means, 97.5))


def atomgroup_from_indices(u: mda.Universe, indices: list[int]):
    return u.atoms[np.array(indices, dtype=int)]


def build_mapping() -> dict[str, pd.DataFrame]:
    df = pd.read_csv(MAPPING, sep="\t")
    return {sid: g.copy() for sid, g in df.groupby("system_id")}


def kabsch_align(coords: np.ndarray, ref: np.ndarray) -> np.ndarray:
    p = coords - coords.mean(axis=0)
    q = ref - ref.mean(axis=0)
    c = p.T @ q
    v, _s, wt = np.linalg.svd(c)
    d = np.sign(np.linalg.det(v @ wt))
    u = v @ np.diag([1.0, 1.0, d]) @ wt
    return p @ u + ref.mean(axis=0)


def infer_job_id(array_idx: int) -> tuple[str, str, str]:
    logs = sorted(LOGDIR.glob(f"slurm-gmx-prod20-*_{array_idx}.err"), key=lambda p: p.stat().st_mtime)
    finished: list[Path] = []
    for p in logs:
        txt = p.read_text(errors="ignore")
        if "Finished mdrun" in txt:
            finished.append(p)
    chosen = finished[-1] if finished else (logs[-1] if logs else None)
    if chosen is None:
        return "NA", "NA", "no_slurm_log_found"
    m = re.search(r"slurm-gmx-prod20-(\d+)_", chosen.name)
    jid = f"{m.group(1)}_{array_idx}" if m else "NA"
    note = "latest_finished_mdrun_log" if finished else "latest_log_without_finished_mdrun"
    if len(finished) > 1:
        note += f";duplicate_finished_logs={len(finished)}"
    return jid, str(chosen), note


def gmx_energy_stats(edr: Path, idx: int) -> dict[str, float | str]:
    if not edr.is_file() or edr.stat().st_size == 0:
        return {"energy_qc": "missing_edr"}
    xvg = Path(tempfile.gettempdir()) / f"bd009_energy_{idx}.xvg"
    script = (
        "module load gromacs/2024.2 >/dev/null 2>&1; "
        "printf 'Temperature\\nPressure\\nPotential\\nKinetic-En.\\nTotal-Energy\\n0\\n' "
        f"| gmx energy -f {edr} -o {xvg} >/dev/null 2>&1"
    )
    proc = subprocess.run(["bash", "-lc", script], text=True)
    if proc.returncode != 0 or not xvg.is_file():
        return {"energy_qc": "gmx_energy_failed"}
    legends: list[str] = []
    arr = []
    with xvg.open() as fh:
        for line in fh:
            m = re.search(r'@\s+s\d+\s+legend\s+"(.+)"', line)
            if m:
                legends.append(m.group(1))
            if line.startswith(("#", "@")):
                continue
            vals = [float(x) for x in line.split()]
            if len(vals) >= 6:
                arr.append(vals[:6])
    if not arr:
        return {"energy_qc": "energy_xvg_empty"}
    a = np.array(arr)
    cols = {name: a[:, i + 1] for i, name in enumerate(legends)}
    temp = cols.get("Temperature", np.full(a.shape[0], math.nan))
    press = cols.get("Pressure", np.full(a.shape[0], math.nan))
    pot = cols.get("Potential", np.full(a.shape[0], math.nan))
    total = cols.get("Total Energy", np.full(a.shape[0], math.nan))
    out = {
        "energy_qc": "pass_energy_terms_finite" if np.isfinite(a).all() else "nonfinite_energy_terms",
        "temperature_mean_K": float(np.nanmean(temp)),
        "temperature_sd_K": float(np.nanstd(temp, ddof=1)),
        "pressure_mean_bar": float(np.nanmean(press)),
        "pressure_sd_bar": float(np.nanstd(press, ddof=1)),
        "potential_mean_kjmol": float(np.nanmean(pot)),
        "potential_drift_kjmol": float(pot[-1] - pot[0]),
        "total_energy_mean_kjmol": float(np.nanmean(total)),
        "total_energy_drift_kjmol": float(total[-1] - total[0]),
    }
    return out


def selections(u: mda.Universe, map_df: pd.DataFrame, junction: str):
    native = map_df[map_df["residue_class"].eq("native_A89_2C")].copy()
    tag = map_df[map_df["residue_class"].eq("inserted_tag")].copy()
    sim_to_native = dict(zip(native["sim_resid"].astype(int), native["native_A89_resid"].astype(int)))
    native_ca_idx: list[int] = []
    native_a89: list[int] = []
    for atom in u.select_atoms("protein and name CA"):
        if atom.resid in sim_to_native:
            native_ca_idx.append(atom.index)
            native_a89.append(sim_to_native[atom.resid])
    order = np.argsort(native_a89)
    native_ca_idx = [native_ca_idx[i] for i in order]
    native_a89 = [native_a89[i] for i in order]
    tag_resids = set(tag["sim_resid"].astype(int).tolist())
    tag_heavy_idx = [a.index for a in u.select_atoms("protein and not name H*") if a.resid in tag_resids]
    tag_ca_idx = [a.index for a in u.select_atoms("protein and name CA") if a.resid in tag_resids]
    win = local_window(junction)
    native_heavy_idx = [
        a.index
        for a in u.select_atoms("protein and not name H*")
        if a.resid in sim_to_native and sim_to_native[a.resid] not in win
    ]
    return (
        atomgroup_from_indices(u, native_ca_idx),
        native_a89,
        atomgroup_from_indices(u, tag_heavy_idx) if tag_heavy_idx else None,
        atomgroup_from_indices(u, tag_ca_idx) if tag_ca_idx else None,
        atomgroup_from_indices(u, native_heavy_idx),
    )


def local_window(junction: str) -> set[int]:
    if "|" not in junction:
        return set()
    left, right = [int(x) for x in junction.split("|")]
    return set(range(left - 5, right + 6))


def analyze_replica(row: dict[str, str], map_df: pd.DataFrame) -> tuple[dict, dict, dict, dict, dict]:
    idx = int(row["slurm_array_index"])
    traj = Path(row["trajectory_path"])
    edr = Path(row["energy_path"])
    rdir = traj.parent
    tpr = rdir / "prod_20ns.tpr"
    log = rdir / "prod_20ns.log"
    job_id, slurm_log, job_note = infer_job_id(idx)
    base = {
        "system_id": row["system_id"],
        "construct_id": row["construct_id"],
        "junction": row["junction"],
        "tag_form": row["tag_form"],
        "replica": row["replica"],
        "slurm_array_index": row["slurm_array_index"],
        "job_id": job_id,
        "slurm_log": slurm_log,
        "job_id_provenance": job_note,
    }
    if not (traj.is_file() and tpr.is_file()):
        qc = {**base, "completed_ns": 0, "frame_count": 0, "ranking_inclusion": "excluded_no_trajectory"}
        return qc, {}, {}, {}, {}

    energy = gmx_energy_stats(edr, idx)
    u = mda.Universe(str(tpr), str(traj))
    native_ca, native_a89, tag_heavy, tag_ca, native_heavy = selections(u, map_df, row["junction"])
    frames, rg_vals, tag_min, tag_contacts, tag_end = [], [], [], [], []
    finite = True
    for ts in u.trajectory:
        native_pos = native_ca.positions.astype(float).copy()
        if not np.isfinite(native_pos).all() or not np.isfinite(ts.dimensions[:3]).all():
            finite = False
        frames.append(native_pos)
        rg_vals.append(float(native_ca.radius_of_gyration()))
        if tag_heavy is not None and len(tag_heavy):
            tree = cKDTree(native_heavy.positions.astype(float))
            d, _ = tree.query(tag_heavy.positions.astype(float), k=1)
            tag_min.append(float(np.min(d)))
            tag_contacts.append(int(np.sum(d < 4.5)))
        if tag_ca is not None and len(tag_ca) >= 2:
            tag_end.append(float(np.linalg.norm(tag_ca.positions[0] - tag_ca.positions[-1])))
    arr = np.array(frames)
    ref = arr[0]
    aligned = np.array([kabsch_align(x, ref) for x in arr])
    rmsd = np.sqrt(np.mean(np.sum((aligned - ref) ** 2, axis=2), axis=1))
    mean_pos = aligned.mean(axis=0)
    rmsf = np.sqrt(np.mean(np.sum((aligned - mean_pos) ** 2, axis=2), axis=0))
    last_ns = float(u.trajectory[-1].time / 1000.0)
    frame_count = len(u.trajectory)
    log_finished = log.is_file() and "Finished mdrun" in log.read_text(errors="ignore")
    temp_ok = abs(float(energy.get("temperature_mean_K", math.nan)) - 300.0) <= 8.0
    pressure_finite = math.isfinite(float(energy.get("pressure_mean_bar", math.nan)))
    ranking = "included_pass"
    gaps = []
    if last_ns < 19.95 or frame_count < 190:
        ranking = "excluded_incomplete"
        gaps.append("trajectory_shorter_than_20ns")
    if not finite:
        ranking = "excluded_nonfinite_coordinates"
        gaps.append("nonfinite_coordinates")
    if not log_finished:
        ranking = "included_with_caution"
        gaps.append("completion_log_missing_finished_mdrun")
    if "duplicate_finished_logs" in job_note:
        if ranking == "included_pass":
            ranking = "included_with_caution"
        gaps.append("duplicate_backfill_rerun_logs_present")

    pairs = []
    d0 = distance.squareform(distance.pdist(ref))
    for i in range(len(native_a89)):
        for j in range(i + 4, len(native_a89)):
            if d0[i, j] < 8.0:
                pairs.append((i, j))
    pair_arr = np.array(pairs, dtype=int) if pairs else np.empty((0, 2), dtype=int)
    contact_ret = math.nan
    local_ret = math.nan
    if len(pair_arr):
        vals = []
        lvals = []
        win = local_window(row["junction"])
        local_pair_mask = np.array([(native_a89[i] in win or native_a89[j] in win) for i, j in pair_arr])
        for xyz in aligned:
            d = np.linalg.norm(xyz[pair_arr[:, 0]] - xyz[pair_arr[:, 1]], axis=1)
            kept = d < 8.0
            vals.append(float(kept.mean()))
            if local_pair_mask.any():
                lvals.append(float(kept[local_pair_mask].mean()))
        contact_ret = float(np.mean(vals))
        local_ret = float(np.mean(lvals)) if lvals else math.nan

    # Dynamic cross-correlation and persistent contact network.
    disp = aligned - aligned.mean(axis=0)
    denom = np.sqrt(np.mean(np.sum(disp * disp, axis=2), axis=0))
    corr = np.eye(len(native_a89))
    for i in range(len(native_a89)):
        for j in range(i + 1, len(native_a89)):
            den = denom[i] * denom[j]
            c = np.mean(np.sum(disp[:, i, :] * disp[:, j, :], axis=1)) / den if den else 0.0
            corr[i, j] = corr[j, i] = c
    win = local_window(row["junction"])
    net = nx.Graph()
    net.add_nodes_from(native_a89)
    if len(pair_arr):
        persist = []
        for i, j in pair_arr:
            d = np.linalg.norm(aligned[:, i, :] - aligned[:, j, :], axis=1)
            p = float(np.mean(d < 8.0))
            persist.append(p)
            if p >= 0.5:
                net.add_edge(native_a89[i], native_a89[j], weight=p)
    path_vals = []
    corr_vals = []
    local_idx = [i for i, r in enumerate(native_a89) if r in win]
    for name, residues in FUNCTIONAL_SETS.items():
        fset = set(residues)
        f_idx = [i for i, r in enumerate(native_a89) if r in fset]
        if local_idx and f_idx:
            corr_vals.append(float(np.mean(np.abs(corr[np.ix_(local_idx, f_idx)]))))
        sources = [r for r in native_a89 if r in win and r in net]
        targets = [r for r in native_a89 if r in fset and r in net]
        lengths = []
        for s in sources[:12]:
            for t in targets[:12]:
                try:
                    lengths.append(nx.shortest_path_length(net, s, t))
                except nx.NetworkXNoPath:
                    pass
        if lengths:
            path_vals.append(float(np.mean(lengths)))
    local_rmsf = [float(rmsf[i]) for i, r in enumerate(native_a89) if r in win]
    qc = {
        **base,
        "completed_ns": round(last_ns, 4),
        "frame_count": frame_count,
        "temperature_qc": "pass" if temp_ok else "caution",
        "pressure_qc": "finite_pressure_series" if pressure_finite else "not_available",
        "energy_qc": energy.get("energy_qc", "not_available"),
        "coordinate_integrity_qc": "pass_finite_ca_and_box" if finite else "fail_nonfinite_coordinates_or_box",
        "native_ca_count": len(native_a89),
        "log_completion_qc": "finished_mdrun" if log_finished else "missing_finished_mdrun",
        "ranking_inclusion": ranking,
        "failure_or_gap_reason": ";".join(gaps) if gaps else "none",
        **{k: round(v, 6) if isinstance(v, float) else v for k, v in energy.items() if k != "energy_qc"},
    }
    dyn = {
        **base,
        "row_type": "replica",
        "replica_count_completed": 1,
        "native_backbone_rmsd_mean_A": float(rmsd.mean()),
        "native_backbone_rmsd_last_A": float(rmsd[-1]),
        "native_backbone_rmsd_block1_mean_A": float(rmsd[: len(rmsd) // 2].mean()),
        "native_backbone_rmsd_block2_mean_A": float(rmsd[len(rmsd) // 2 :].mean()),
        "native_ca_rg_mean_A": float(np.mean(rg_vals)),
        "local_insertion_rmsf_mean_A": float(np.mean(local_rmsf)) if local_rmsf else math.nan,
        "global_native_rmsf_mean_A": float(np.mean(rmsf)),
        "effect_vs_WT": "computed_after_summary",
    }
    expo = {
        **base,
        "row_type": "replica",
        "metric_status": "WT_no_tag" if row["tag_form"] == "WT" else "computed_tag_distance_exposure_proxy",
        "tag_sasa_mean_A2": "NA_method_not_used",
        "tag_native_min_distance_mean_A": float(np.mean(tag_min)) if tag_min else math.nan,
        "tag_native_min_distance_p10_A": float(np.percentile(tag_min, 10)) if tag_min else math.nan,
        "tag_collapse_fraction_min_distance_lt_4p5A": float(np.mean(np.array(tag_min) < 4.5)) if tag_min else math.nan,
        "tag_native_contacts_mean_count_lt_4p5A": float(np.mean(tag_contacts)) if tag_contacts else math.nan,
        "tag_end_to_end_mean_A": float(np.mean(tag_end)) if tag_end else math.nan,
        "exposure_method_note": "heavy_atom_min_distance_proxy;SASA_not_used_for_primary_ranking",
    }
    contact = {
        **base,
        "row_type": "replica",
        "metric_status": "computed_ca_native_contacts",
        "native_contact_retention": contact_ret,
        "local_contact_retention": local_ret,
        "native_contact_pair_count_reference": len(pair_arr),
    }
    network = {
        **base,
        "row_type": "replica",
        "metric_status": "computed_dccm_ca_and_persistent_contact_network",
        "local_to_functional_abs_dccm_mean": float(np.mean(corr_vals)) if corr_vals else math.nan,
        "persistent_contact_edges": net.number_of_edges(),
        "network_components": nx.number_connected_components(net),
        "local_to_functional_shortest_path_mean_edges": float(np.mean(path_vals)) if path_vals else math.nan,
        "replica_consistency": "computed_after_summary",
    }
    return qc, dyn, expo, contact, network


def summarize(rep_rows: list[dict], keys: list[str], wt_summary: dict | None = None) -> list[dict]:
    out = []
    by_construct = defaultdict(list)
    for r in rep_rows:
        by_construct[r["construct_id"]].append(r)
    for construct, rows in by_construct.items():
        first = rows[0]
        s = {
            "system_id": first["system_id"],
            "construct_id": construct,
            "junction": first["junction"],
            "tag_form": first["tag_form"],
            "row_type": "construct_summary",
            "replica": "summary",
            "replica_count_completed": len(rows),
        }
        for k in keys:
            vals = [float(r.get(k, math.nan)) for r in rows if str(r.get(k, "NA")) != "NA"]
            m, sd = mean_sd(vals)
            lo, hi = bootstrap_ci(vals)
            s[k] = m
            s[k + "_sd"] = sd
            s[k + "_bootstrap_ci95_low"] = lo
            s[k + "_bootstrap_ci95_high"] = hi
            if wt_summary and construct != "WT_112_321" and k in wt_summary:
                s[k + "_effect_vs_WT"] = m - wt_summary[k]
            else:
                s[k + "_effect_vs_WT"] = 0.0 if construct == "WT_112_321" and math.isfinite(m) else math.nan
        out.append(s)
    return out


def score_panel(dyn_sum: list[dict], expo_sum: list[dict], contact_sum: list[dict], net_sum: list[dict]) -> tuple[pd.DataFrame, pd.DataFrame]:
    panel = pd.read_csv(DATA / "balanced_targeted_dynamics_panel_v2.tsv", sep="\t")
    d = {r["construct_id"]: r for r in dyn_sum}
    e = {r["construct_id"]: r for r in expo_sum}
    c = {r["construct_id"]: r for r in contact_sum}
    n = {r["construct_id"]: r for r in net_sum}
    rows = []
    rob = []
    for _, p in panel.iterrows():
        cid = p["construct_id"]
        dm, em, cm, nm = d.get(cid, {}), e.get(cid, {}), c.get(cid, {}), n.get(cid, {})
        rmsd_eff = float(dm.get("native_backbone_rmsd_mean_A_effect_vs_WT", math.nan))
        local_eff = float(dm.get("local_insertion_rmsf_mean_A_effect_vs_WT", math.nan))
        contact_eff = float(cm.get("native_contact_retention_effect_vs_WT", math.nan))
        collapse = float(em.get("tag_collapse_fraction_min_distance_lt_4p5A", math.nan))
        net_eff = float(nm.get("local_to_functional_abs_dccm_mean_effect_vs_WT", math.nan))
        penalties = 0
        penalties += 2 if math.isfinite(rmsd_eff) and rmsd_eff > 1.0 else 0
        penalties += 1 if math.isfinite(local_eff) and local_eff > 1.5 else 0
        penalties += 1 if math.isfinite(contact_eff) and contact_eff < -0.08 else 0
        penalties += 1 if math.isfinite(collapse) and collapse > 0.40 else 0
        penalties += 1 if math.isfinite(net_eff) and net_eff > 0.08 else 0
        if p["panel_role_pre_MD"] == "control":
            tier = "Control_after_dynamics"
        elif penalties <= 1:
            tier = "Tier_A_dynamics_retained"
        elif penalties <= 3:
            tier = "Tier_B_dynamics_secondary"
        else:
            tier = "Tier_C_dynamics_deprioritized"
        unresolved = "no_HRV_A89_specific_insertion_phenotype;exact_nucleotide_context_missing;direct_homolog_InDel_conflict_retained"
        rows.append({
            "construct_id": cid,
            "junction": p["junction"],
            "tag_form": p["tag_form"],
            "site_region": p["site_region"],
            "pre_dynamics_role": p["panel_role_pre_MD"],
            "dynamics_tier": tier,
            "hard_biological_constraints": "retained_computational_screen_only",
            "direct_homolog_insertion": "direct_insert_strongly_deleterious_prior_retained",
            "disorder_flexibility_prior": "available_v1_supporting_prior",
            "static_structure_ensemble": "available_pre_dynamics",
            "openmm_qc": p.get("pre_MD_openmm_status", "available"),
            "local_multimer_context": "completed_but_nonfinite_coordinates_inconclusive",
            "replicated_dynamics": f"3x20ns_analyzed;penalty_count={penalties}",
            "dynamic_network": "analyzed_as_CA_DCCM_and_contact_network",
            "native_rmsd_effect_vs_WT_A": rmsd_eff,
            "native_rmsd_mean_A": dm.get("native_backbone_rmsd_mean_A", math.nan),
            "local_rmsf_mean_A": dm.get("local_insertion_rmsf_mean_A", math.nan),
            "local_rmsf_effect_vs_WT_A": local_eff,
            "native_contact_retention": cm.get("native_contact_retention", math.nan),
            "native_contact_retention_effect_vs_WT": contact_eff,
            "tag_native_min_distance_mean_A": em.get("tag_native_min_distance_mean_A", math.nan),
            "tag_collapse_fraction": collapse,
            "network_dccm_raw": nm.get("local_to_functional_abs_dccm_mean", math.nan),
            "network_dccm_effect_vs_WT": net_eff,
            "network_path_mean_edges": nm.get("local_to_functional_shortest_path_mean_edges", math.nan),
            "unresolved_conflicts": unresolved,
            "safe_or_validated": "no",
        })
        rob.append({
            "construct_id": cid,
            "junction": p["junction"],
            "tag_form": p["tag_form"],
            "dynamics_tier": tier,
            "replica_count": int(dm.get("replica_count_completed", 0) or 0),
            "rmsd_sd_A": dm.get("native_backbone_rmsd_mean_A_sd", math.nan),
            "local_rmsf_sd_A": dm.get("local_insertion_rmsf_mean_A_sd", math.nan),
            "leave_one_layer_sensitivity": "ranking_changes_possible_without_direct_homolog_conflict_layer",
            "site_region_diversity_note": p["site_region"],
            "tag_family_diversity_note": p["tag_form"],
            "twenty_ns_sufficiency": "minimum_screening_coverage_met_not_validation",
        })
    return pd.DataFrame(rows), pd.DataFrame(rob)


def write_tsv(path: Path, rows: list[dict] | pd.DataFrame) -> None:
    if isinstance(rows, pd.DataFrame):
        rows.to_csv(path, sep="\t", index=False, na_rep="NA")
        return
    df = pd.DataFrame(rows)
    df.to_csv(path, sep="\t", index=False, na_rep="NA")


def update_manifests(qc_rows: list[dict]) -> None:
    qc_by_idx = {str(r["slurm_array_index"]): r for r in qc_rows}
    for path in [MANIFEST, COMPLETION]:
        fields, rows = read_manifest_rows(path)
        extra = ["completion_log_qc", "job_id_provenance", "slurm_completion_log"]
        fields = list(dict.fromkeys(fields + extra))
        for r in rows:
            q = qc_by_idx.get(str(r["slurm_array_index"]), {})
            r["job_id"] = q.get("job_id", r.get("job_id", "NA"))
            r["achieved_ns"] = na(q.get("completed_ns", r.get("achieved_ns", "NA")))
            status = "completed_20ns_verified" if q.get("ranking_inclusion", "").startswith("included") else "output_present_but_completion_unverified"
            if "completion_status" in r:
                r["completion_status"] = status
            if "status" in r:
                r["status"] = status
            r["completion_log_qc"] = q.get("log_completion_qc", "NA")
            r["job_id_provenance"] = q.get("job_id_provenance", "NA")
            r["slurm_completion_log"] = q.get("slurm_log", "NA")
        with path.open("w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=fields, delimiter="\t", lineterminator="\n")
            w.writeheader()
            w.writerows(rows)


def forcefield_provenance() -> None:
    files = [
        Path("/public/apps/gromacs/2024.2/share/gromacs/top/charmm36.ff/forcefield.doc"),
        Path("/public/apps/gromacs/2024.2/share/gromacs/top/charmm36.ff/forcefield.itp"),
        Path("/public/apps/gromacs/2024.2/share/gromacs/top/charmm36.ff/tip3p.itp"),
        RESULT / "gromacs/mdp/prod_20ns.mdp",
    ]
    rows = []
    import hashlib

    for p in files:
        rows.append({
            "path": str(p),
            "exists": p.is_file(),
            "sha256": hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else "NA",
            "first_line": p.read_text(errors="ignore").splitlines()[0] if p.is_file() else "NA",
        })
    write_tsv(RESULT / "forcefield_provenance.tsv", rows)


def main() -> None:
    maps = build_mapping()
    fields, rows = read_manifest_rows(MANIFEST)
    qc_rows: list[dict] = []
    dyn_rows: list[dict] = []
    expo_rows: list[dict] = []
    contact_rows: list[dict] = []
    net_rows: list[dict] = []
    for row in rows:
        qc, dyn, expo, contact, net = analyze_replica(row, maps[row["system_id"]])
        qc_rows.append(qc)
        if dyn:
            dyn_rows.append(dyn)
            expo_rows.append(expo)
            contact_rows.append(contact)
            net_rows.append(net)
        print(f"analyzed {row['slurm_array_index']} {row['construct_id']} rep{row['replica']} {qc.get('ranking_inclusion')}", flush=True)

    wt_dyn = summarize([r for r in dyn_rows if r["construct_id"] == "WT_112_321"], ["native_backbone_rmsd_mean_A", "local_insertion_rmsf_mean_A", "global_native_rmsf_mean_A"])[0]
    wt_contact = summarize([r for r in contact_rows if r["construct_id"] == "WT_112_321"], ["native_contact_retention", "local_contact_retention"])[0]
    wt_net = summarize([r for r in net_rows if r["construct_id"] == "WT_112_321"], ["local_to_functional_abs_dccm_mean", "local_to_functional_shortest_path_mean_edges"])[0]
    dyn_sum = summarize(dyn_rows, ["native_backbone_rmsd_mean_A", "native_backbone_rmsd_last_A", "native_ca_rg_mean_A", "local_insertion_rmsf_mean_A", "global_native_rmsf_mean_A"], wt_dyn)
    expo_sum = summarize(expo_rows, ["tag_native_min_distance_mean_A", "tag_native_min_distance_p10_A", "tag_collapse_fraction_min_distance_lt_4p5A", "tag_native_contacts_mean_count_lt_4p5A", "tag_end_to_end_mean_A"])
    contact_sum = summarize(contact_rows, ["native_contact_retention", "local_contact_retention"], wt_contact)
    net_sum = summarize(net_rows, ["local_to_functional_abs_dccm_mean", "persistent_contact_edges", "network_components", "local_to_functional_shortest_path_mean_edges"], wt_net)

    write_tsv(DATA / "dynamics_replica_qc_v1.tsv", qc_rows)
    write_tsv(DATA / "broad_dynamics_metrics_v1.tsv", dyn_rows + dyn_sum)
    write_tsv(DATA / "tag_exposure_dynamics_v1.tsv", expo_rows + expo_sum)
    write_tsv(DATA / "contact_persistence_dynamics_v1.tsv", contact_rows + contact_sum)
    write_tsv(DATA / "dynamic_network_perturbation_v1.tsv", net_rows + net_sum)
    panel, robustness = score_panel(dyn_sum, expo_sum, contact_sum, net_sum)
    write_tsv(DATA / "final_candidate_panel_v2_dynamics.tsv", panel)
    write_tsv(RESULT / "ranking_robustness_v2.tsv", robustness)
    update_manifests(qc_rows)
    forcefield_provenance()


def read_manifest_rows(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(newline="") as fh:
        reader = csv.DictReader(fh, delimiter="\t")
        return reader.fieldnames or [], list(reader)


if __name__ == "__main__":
    main()
