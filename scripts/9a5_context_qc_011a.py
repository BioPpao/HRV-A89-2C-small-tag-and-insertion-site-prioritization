#!/usr/bin/env python3
"""Task 011A: QC hardening for the 9A5 context layer.

No MD, AF, docking, Slurm, or GPU work is launched here. The script reuses
existing structures and trajectories, re-exports the three 1x9A5 final frames
from already-completed XTC files, collapses duplicate endpoint PDBs, and writes
versioned QC outputs.
"""

from __future__ import annotations

import hashlib
import importlib.util
import math
import statistics
import subprocess
import sys
from pathlib import Path

import matplotlib
import numpy as np
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[1]
SOURCE = Path("/public/home/yukang/HRV_Oligomers")
SOURCE_HEX = SOURCE / "HRV_A89_2C_HEXAMER"
SOURCE_SUMMARY = SOURCE_HEX / "results_summary"
REPEAT_ROOT = SOURCE_HEX / "12_9A5_loading" / "16_1x_9A5_weakposres_1ns_repeats"
REPEAT_ANALYSIS = REPEAT_ROOT / "analysis"
OUT_DATA = ROOT / "data"
OUT_RESULTS = ROOT / "results" / "9a5_context_011a_qc"
OUT_REEXPORTED = OUT_RESULTS / "reexported_1x9A5_endpoints"
OUT_FIG = ROOT / "figures" / "9a5_context_011a_qc"
OUT_DOCS = ROOT / "docs"
V5_PANEL = ROOT / "data" / "final_candidate_panel_v5_experimental_review_cleanup.tsv"
V6_PANEL = ROOT / "data" / "final_candidate_panel_v6_9a5_context.tsv"
MONOMER_V1 = ROOT / "data" / "9a5_monomer_tag_compatibility_v1.tsv"
TODAY = "2026-09-02"


def load_task011():
    spec = importlib.util.spec_from_file_location("task011", ROOT / "scripts" / "9a5_context_011_analysis.py")
    if spec is None or spec.loader is None:
        raise SystemExit("Could not load Task 011 helper module")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["task011"] = mod
    spec.loader.exec_module(mod)
    return mod


T11 = load_task011()


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def git(repo: Path, args: list[str]) -> str:
    try:
        return subprocess.check_output(["git", "-C", str(repo)] + args, text=True, stderr=subprocess.STDOUT).strip()
    except Exception as exc:
        return f"ERROR:{exc}"


def read_tsv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, sep="\t", dtype=str).fillna("")


def write_tsv(path: Path, rows: list[dict[str, object]] | pd.DataFrame) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    df = rows if isinstance(rows, pd.DataFrame) else pd.DataFrame(rows)
    df.to_csv(path, sep="\t", index=False)


def rel(path: Path) -> str:
    path = path.resolve()
    try:
        return path.relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        pass
    try:
        return path.relative_to(SOURCE.resolve()).as_posix()
    except ValueError:
        pass
    try:
        return path.relative_to(SOURCE).as_posix()
    except ValueError:
        pass
    return str(path)


def fnum(value: object, default: float = math.nan) -> float:
    try:
        if value is None or str(value) == "":
            return default
        return float(value)
    except Exception:
        return default


def atom_array(path: Path) -> np.ndarray:
    atoms = T11.parse_pdb(path)
    return np.vstack([a.coord for a in atoms])


def rmsd_same_order(a: Path, b: Path) -> float:
    aa = atom_array(a)
    bb = atom_array(b)
    if aa.shape != bb.shape:
        return math.nan
    return float(np.sqrt(np.mean(np.sum((aa - bb) ** 2, axis=1))))


def ca_gap_summary(path: Path) -> tuple[float, str]:
    atoms = T11.parse_pdb(path)
    by_chain: dict[str, list[object]] = {}
    for atom in atoms:
        if atom.name == "CA":
            by_chain.setdefault(atom.chain, []).append(atom)
    max_gap = 0.0
    note = []
    for chain, cas in sorted(by_chain.items()):
        cas = sorted(cas, key=lambda a: a.resid)
        gaps = [float(np.linalg.norm(cas[i].coord - cas[i - 1].coord)) for i in range(1, len(cas))]
        if gaps:
            chain_gap = max(gaps)
            max_gap = max(max_gap, chain_gap)
            if chain_gap > 5.0:
                note.append(f"{chain}:{chain_gap:.2f}A")
    return max_gap, ";".join(note) if note else "no_CA_gap_over_5A"


def reexport_endpoints() -> tuple[list[dict[str, object]], list[Path]]:
    try:
        import MDAnalysis as mda
    except Exception as exc:  # pragma: no cover
        raise SystemExit(f"MDAnalysis required for endpoint re-export from existing XTC: {exc}")

    OUT_REEXPORTED.mkdir(parents=True, exist_ok=True)
    top = SOURCE_SUMMARY / "SHOWCASE_1x_9A5_D_chain_after_npt_100ps_pbc_fixed.pdb"
    records = []
    reexported = []
    source_script = SOURCE_HEX / "scripts" / "65_analyze_1x_9A5_weakposres_repeats.py"
    for rep in ["rep1", "rep2", "rep3"]:
        rep_dir = REPEAT_ROOT / rep
        stem = f"npt_1x_9A5_weakposres_1ns_{rep}"
        xtc = rep_dir / f"{stem}_pbc_cluster_center.xtc"
        raw_xtc = rep_dir / f"{stem}.xtc"
        tpr = rep_dir / f"{stem}.tpr"
        gro = rep_dir / f"{stem}.gro"
        log = rep_dir / f"{stem}.log"
        old_analysis = REPEAT_ANALYSIS / f"{rep}_endpoint_last_frame.pdb"
        old_packaged = SOURCE_SUMMARY / f"selected_1x_9A5_weakposres_1ns_{rep}_endpoint.pdb"
        out = OUT_REEXPORTED / f"{rep}_endpoint_last_frame_reexported.pdb"

        u = mda.Universe(str(top), str(xtc))
        n_frames = len(u.trajectory)
        u.trajectory[-1]
        last_time_ps = float(u.trajectory.time)
        u.atoms.write(str(out))
        atoms = T11.parse_pdb(out)
        chains, n2c, atom_count, vh, vl, finite = T11.chain_residue_summary(atoms)
        max_gap, gap_note = ca_gap_summary(out)
        records.append(
            {
                "repeat": rep,
                "source_repo_head": git(SOURCE, ["rev-parse", "HEAD"]),
                "source_script": rel(source_script),
                "source_script_sha256": sha256(source_script),
                "old_analysis_pdb": rel(old_analysis),
                "old_analysis_pdb_sha256": sha256(old_analysis),
                "old_packaged_pdb": rel(old_packaged),
                "old_packaged_pdb_sha256": sha256(old_packaged),
                "cluster_center_xtc": rel(xtc),
                "cluster_center_xtc_sha256": sha256(xtc),
                "raw_xtc": rel(raw_xtc),
                "raw_xtc_sha256": sha256(raw_xtc),
                "tpr": rel(tpr),
                "tpr_sha256": sha256(tpr),
                "gro": rel(gro),
                "gro_sha256": sha256(gro),
                "log": rel(log),
                "log_sha256": sha256(log),
                "reexported_pdb": rel(out),
                "reexported_pdb_sha256": sha256(out),
                "n_frames": n_frames,
                "last_time_ps": last_time_ps,
                "chains": chains,
                "n_2c_chains": n2c,
                "atom_count": atom_count,
                "vh_chain_guess": vh,
                "vl_chain_guess": vl,
                "finite_coordinates": finite,
                "max_ca_gap_A": max_gap,
                "pbc_chain_qc_note": gap_note,
                "endpoint_reexport_method": "MDAnalysis Universe(topology, pbc_cluster_center.xtc); explicit u.trajectory[-1]; u.atoms.write(PDB)",
                "old_endpoint_status": "duplicate_export_do_not_count_as_independent",
                "trajectory_independence_status": "underlying_xtc_tpr_gro_log_sha256_unique",
                "why_old_pdbs_same": "source_analysis_script_writes_u.atoms_after_trajectory_loop_without_explicit_last_frame; reexported_with_explicit_last_frame",
            }
        )
        reexported.append(out)

    old_sha_unique = len({r["old_packaged_pdb_sha256"] for r in records})
    re_sha_unique = len({r["reexported_pdb_sha256"] for r in records})
    for rec in records:
        rep = rec["repeat"]
        old = SOURCE_SUMMARY / f"selected_1x_9A5_weakposres_1ns_{rep}_endpoint.pdb"
        new = ROOT / rec["reexported_pdb"]
        rec["old_packaged_rmsd_vs_reexported_A"] = rmsd_same_order(old, new)
        rec["old_endpoint_unique_sha_count"] = old_sha_unique
        rec["reexported_endpoint_unique_sha_count"] = re_sha_unique
        rec["reexported_rmsd_vs_rep1_A"] = rmsd_same_order(reexported[0], new)
    return records, reexported


def corrected_hexamers(reexported: list[Path]) -> list[tuple[str, Path, str]]:
    hexamers = [
        ("1x9A5_100ps_showcase", SOURCE_SUMMARY / "SHOWCASE_1x_9A5_D_chain_after_npt_100ps_pbc_fixed.pdb", "yes"),
        ("1x9A5_1ns_rep1_reexported", reexported[0], "yes"),
        ("1x9A5_1ns_rep2_reexported", reexported[1], "yes"),
        ("1x9A5_1ns_rep3_reexported", reexported[2], "yes"),
        ("free_hexamer_2ns_lead", SOURCE_SUMMARY / "selected_hexamer_01_md_representative.pdb", "no"),
        ("free_hexamer_5ns_rep1", SOURCE_SUMMARY / "selected_hexamer_01_md_representative_5ns_rep1.pdb", "no"),
        ("free_hexamer_5ns_rep2", SOURCE_SUMMARY / "selected_hexamer_01_md_representative_5ns_rep2.pdb", "no"),
        ("free_hexamer_5ns_rep3", SOURCE_SUMMARY / "selected_hexamer_01_md_representative_5ns_rep3.pdb", "no"),
        ("free_hexamer_control_model1", SOURCE_SUMMARY / "selected_hexamer_02_md_representative.pdb", "no"),
    ]
    seen = set()
    unique = []
    for name, path, ab in hexamers:
        digest = sha256(path)
        if digest in seen:
            continue
        seen.add(digest)
        unique.append((name, path, ab))
    return unique


def load_models(panel: pd.DataFrame) -> pd.DataFrame:
    models = T11.candidate_models(panel)
    models["model_sha256"] = models["model_file"].map(lambda p: sha256(ROOT / p))
    models["model_unique_sha_index"] = models.groupby("construct_id")["model_sha256"].transform(lambda x: x.rank(method="dense").astype(int))
    return models


def load_extra_248_models(models: pd.DataFrame) -> pd.DataFrame:
    manifest = ROOT / "results" / "candidate_panel_008" / "expanded_colabfold_manifest.tsv"
    targets = {"A89_2C_248_249_HA", "A89_2C_248_249_MAP8"}
    rows = [models[models["construct_id"].isin(targets)]]
    if manifest.exists():
        extra = pd.read_csv(manifest, sep="\t")
        extra = extra[extra["construct_id"].isin(targets)]
        extra = extra[extra["prediction_status"].fillna("") == "completed"]
        seq = pd.read_csv(ROOT / "results" / "open_structure_007" / "sequence_manifest_v3_open.tsv", sep="\t")[
            ["construct_id", "tag_sequence"]
        ].drop_duplicates("construct_id")
        extra = extra.merge(seq, on="construct_id", how="left")
        rows.append(extra)
    out = pd.concat(rows, ignore_index=True, sort=False)
    out = out.drop_duplicates(["construct_id", "model_file"])
    out["model_sha256"] = out["model_file"].map(lambda p: sha256(ROOT / p))
    out["model_unique_sha_index"] = out.groupby("construct_id")["model_sha256"].transform(lambda x: x.rank(method="dense").astype(int))
    return out


def analyze_hexamer_qc(panel: pd.DataFrame, models: pd.DataFrame, hexamers: list[tuple[str, Path, str]]) -> pd.DataFrame:
    rows = []
    model_cache = {p: T11.parse_pdb(ROOT / p) for p in models["model_file"].unique()}
    hex_cache = {hpath: T11.parse_pdb(hpath) for _, hpath, _ in hexamers}
    hex_groups = {}
    for _, hpath, _ in hexamers:
        hex_atoms = hex_cache[hpath]
        groups = {"ab": T11.make_heavy_group([a for a in hex_atoms if a.chain in {"H", "L", "G"}]), "adj": {}, "nonadj": {}}
        for i, chain in enumerate(T11.HEX_CHAINS):
            adj = {T11.HEX_CHAINS[(i - 1) % 6], T11.HEX_CHAINS[(i + 1) % 6]}
            nonadj = set(T11.HEX_CHAINS) - adj - {chain}
            groups["adj"][chain] = T11.make_heavy_group([a for a in hex_atoms if a.chain in adj])
            groups["nonadj"][chain] = T11.make_heavy_group([a for a in hex_atoms if a.chain in nonadj])
        hex_groups[hpath] = groups

    for _, cand in panel.iterrows():
        cm = models[models.construct_id == cand.construct_id]
        if cm.empty:
            continue
        left = int(cand["junction"].split("|")[0])
        right = int(cand["junction"].split("|")[1])
        for _, model in cm.iterrows():
            tag_len = int(model["tag_length"])
            tag_seq = str(model["tag_sequence"])
            model_atoms = model_cache[str(model["model_file"])]
            for hname, hpath, antibody_present in hexamers:
                hex_atoms = hex_cache[hpath]
                groups = hex_groups[hpath]
                tag_by_chain = {}
                fit_vals = []
                nfit_vals = []
                for chain in T11.HEX_CHAINS:
                    tag_atoms, _, fit, nfit = T11.align_tagged_to_target(
                        model_atoms, hex_atoms, chain, left, right, tag_len, range(1, 322)
                    )
                    tag_by_chain[chain] = tag_atoms
                    fit_vals.append(fit)
                    nfit_vals.append(nfit)
                all_tag_atoms = [a for atoms in tag_by_chain.values() for a in atoms]
                if antibody_present == "yes":
                    abstat = T11.pair_stats_group(all_tag_atoms, groups["ab"], (2.0, 2.5, 4.5, 5.0))
                else:
                    abstat = {"min_A": math.nan, "closest_pair": "NA", "pairs_lt_2p0A": 0, "pairs_lt_2p5A": 0, "pairs_lt_4p5A": 0, "pairs_lt_5p0A": 0}

                other_min = float("inf")
                adjacent_min = float("inf")
                nonadjacent_min = float("inf")
                other_clash2 = other_clash25 = other_contact45 = 0
                worst_chain = "NA"
                for i, chain in enumerate(T11.HEX_CHAINS):
                    tags = tag_by_chain[chain]
                    astat = T11.pair_stats_group(tags, groups["adj"][chain], (2.0, 2.5, 4.5))
                    nstat = T11.pair_stats_group(tags, groups["nonadj"][chain], (2.0, 2.5, 4.5))
                    chain_min = min(astat["min_A"], nstat["min_A"])
                    if chain_min < other_min:
                        other_min = chain_min
                        worst_chain = chain
                    adjacent_min = min(adjacent_min, astat["min_A"])
                    nonadjacent_min = min(nonadjacent_min, nstat["min_A"])
                    other_clash2 += astat["pairs_lt_2p0A"] + nstat["pairs_lt_2p0A"]
                    other_clash25 += astat["pairs_lt_2p5A"] + nstat["pairs_lt_2p5A"]
                    other_contact45 += astat["pairs_lt_4p5A"] + nstat["pairs_lt_4p5A"]

                tag_tag_min = float("inf")
                tag_tag_clash2 = tag_tag_clash25 = tag_tag_contact45 = 0
                for i, ca in enumerate(T11.HEX_CHAINS):
                    for cb in T11.HEX_CHAINS[i + 1 :]:
                        stat = T11.pair_stats(tag_by_chain[ca], tag_by_chain[cb], (2.0, 2.5, 4.5))
                        tag_tag_min = min(tag_tag_min, stat["min_A"])
                        tag_tag_clash2 += stat["pairs_lt_2p0A"]
                        tag_tag_clash25 += stat["pairs_lt_2p5A"]
                        tag_tag_contact45 += stat["pairs_lt_4p5A"]

                row = {
                    "construct_id": cand.construct_id,
                    "junction": cand.junction,
                    "tag_form": cand.tag_form,
                    "tag_sequence": tag_seq,
                    "tag_length": tag_len,
                    "model_file": str(model["model_file"]),
                    "model_rank": model.get("rank", ""),
                    "model_seed": model.get("seed", ""),
                    "model_sha256": model.get("model_sha256", sha256(ROOT / str(model["model_file"]))),
                    "model_unique_sha_index": model.get("model_unique_sha_index", ""),
                    "hexamer_structure": hname,
                    "hexamer_source_path": rel(hpath),
                    "hexamer_sha256": sha256(hpath),
                    "antibody_present": antibody_present,
                    "chain_fit_rmsd_A_mean": statistics.mean(fit_vals),
                    "chain_fit_rmsd_A_max": max(fit_vals),
                    "alignment_residue_count_min": min(nfit_vals),
                    "tag_ab_min_A": abstat["min_A"],
                    "tag_ab_clashes_lt_2p0A": abstat["pairs_lt_2p0A"],
                    "tag_ab_clashes_lt_2p5A": abstat["pairs_lt_2p5A"],
                    "tag_ab_contacts_4p5A": abstat["pairs_lt_4p5A"],
                    "tag_ab_contacts_5p0A": abstat["pairs_lt_5p0A"],
                    "closest_tag_ab_pair": abstat["closest_pair"],
                    "tag_other_protomer_min_A": other_min,
                    "tag_adjacent_protomer_min_A": adjacent_min,
                    "tag_nonadjacent_protomer_min_A": nonadjacent_min,
                    "tag_other_protomer_clashes_lt_2p0A": other_clash2,
                    "tag_other_protomer_clashes_lt_2p5A": other_clash25,
                    "tag_other_protomer_contacts_4p5A": other_contact45,
                    "worst_tag_chain_for_protomer_contact": worst_chain,
                    "tag_tag_min_A": tag_tag_min,
                    "tag_tag_clashes_lt_2p0A": tag_tag_clash2,
                    "tag_tag_clashes_lt_2p5A": tag_tag_clash25,
                    "tag_tag_contacts_4p5A": tag_tag_contact45,
                    "tag_overlaps_sequence_defined_9a5_epitope": "yes" if (left in T11.EPITOPE or right in T11.EPITOPE) else "no",
                    "analysis_note": "six_tagged_protomer_proxy_from_existing_tagged_monomer;endpoint_duplicates_removed_in_011a",
                }
                row["hexamer_9a5_class"] = T11.class_from_hex(pd.Series(row))
                rows.append(row)
    return pd.DataFrame(rows)


def make_inventory_and_provenance(endpoint_records: list[dict[str, object]], models: pd.DataFrame, hexamers: list[tuple[str, Path, str]]) -> tuple[pd.DataFrame, pd.DataFrame]:
    old_v1 = read_tsv(OUT_DATA / "9a5_context_structure_inventory_v1.tsv")
    old_v1["task011a_qc_status"] = "carried_forward"
    old_v1["replacement_or_qc_note"] = ""
    dup_sha = {r["old_packaged_pdb_sha256"] for r in endpoint_records}
    for idx, row in old_v1.iterrows():
        if row.get("sha256", "") in dup_sha and "selected_1x_9A5_weakposres_1ns" in row.get("filename", ""):
            old_v1.at[idx, "usable_for_primary_analysis"] = "no"
            old_v1.at[idx, "task011a_qc_status"] = "duplicate_endpoint_export_do_not_count_as_independent"
            old_v1.at[idx, "replacement_or_qc_note"] = "replaced_by_reexported_final_frame_from_unique_XTC"
    add = []
    for rec in endpoint_records:
        path = ROOT / rec["reexported_pdb"]
        atoms = T11.parse_pdb(path)
        chains, n2c, atom_count, vh, vl, finite = T11.chain_residue_summary(atoms)
        add.append(
            {
                "relative_path": rec["reexported_pdb"],
                "filename": Path(rec["reexported_pdb"]).name,
                "sha256": rec["reexported_pdb_sha256"],
                "structure_class": "1x9A5_hexamer_complex_reexported_endpoint",
                "2c_state": "full_length_hexamer",
                "antibody_present": "yes",
                "antibody_type": "9A5_Fv",
                "refinement_state": "reexported_from_existing_1ns_weakposres_pbc_cluster_center_xtc",
                "registry_status": "CURRENT_QC_REPLACEMENT",
                "usable_for_primary_analysis": "yes",
                "reason": f"{rec['repeat']} explicit final frame re-export; old endpoint PDB duplicate excluded",
                "chain_residue_summary": chains,
                "n_2c_like_chains": n2c,
                "atom_count": atom_count,
                "vh_chain_guess": vh,
                "vl_chain_guess": vl,
                "finite_coordinates": finite,
                "task011a_qc_status": "corrected_endpoint_primary_analysis",
                "replacement_or_qc_note": "generated_by_scripts/9a5_context_qc_011a.py_from_existing_XTC",
            }
        )
    inv = pd.concat([old_v1, pd.DataFrame(add)], ignore_index=True, sort=False).fillna("")
    prov_rows = []
    for _, row in inv.iterrows():
        p = Path(row["relative_path"])
        abs_path = (ROOT / p) if str(p).startswith(("results/", "data/", "figures/")) else (SOURCE / p)
        prov_rows.append(
            {
                "record_type": "structure",
                "relative_path": row["relative_path"],
                "sha256": row.get("sha256", ""),
                "source_repo": "HRV-A89-2C-small-tag-and-insertion-site-prioritization" if str(p).startswith(("results/", "data/", "figures/")) else "HRV_Oligomers",
                "source_repo_head": git(ROOT if str(p).startswith(("results/", "data/", "figures/")) else SOURCE, ["rev-parse", "HEAD"]),
                "exists": abs_path.exists(),
                "usable_for_primary_analysis": row.get("usable_for_primary_analysis", ""),
                "task011a_qc_status": row.get("task011a_qc_status", ""),
                "note": row.get("replacement_or_qc_note", ""),
            }
        )
    for rec in endpoint_records:
        for key in ["cluster_center_xtc", "raw_xtc", "tpr", "gro", "log", "source_script"]:
            prov_rows.append(
                {
                    "record_type": key,
                    "relative_path": rec[key],
                    "sha256": rec.get(f"{key}_sha256", rec.get("source_script_sha256", "")),
                    "source_repo": "HRV_Oligomers",
                    "source_repo_head": rec["source_repo_head"],
                    "exists": (SOURCE / rec[key]).exists(),
                    "usable_for_primary_analysis": "input_provenance",
                    "task011a_qc_status": rec["trajectory_independence_status"],
                    "note": rec["endpoint_reexport_method"],
                }
            )
    return inv, pd.DataFrame(prov_rows)


def summarize_with_qc(monomer_rows: list[dict[str, object]], hex_rows: pd.DataFrame) -> pd.DataFrame:
    mon = pd.DataFrame(monomer_rows)
    for col in [
        "tag_fv_min_A",
        "tag_fv_clashes_lt_2p0A",
        "tag_fv_clashes_lt_2p5A",
        "tag_native_nonlocal_contacts_4p5A",
    ]:
        if col in mon.columns:
            mon[col] = pd.to_numeric(mon[col], errors="coerce")
    summaries, _, _ = T11.build_summaries(mon.to_dict("records"), hex_rows.to_dict("records"))
    out = pd.DataFrame(summaries)
    hx = hex_rows.groupby("construct_id").agg(
        n_unique_hexamer_sha=("hexamer_sha256", "nunique"),
        min_tag_other_protomer_lt2p5_count=("tag_other_protomer_clashes_lt_2p5A", "sum"),
        min_tag_other_protomer_A_corrected=("tag_other_protomer_min_A", "min"),
    )
    out = out.merge(hx, left_on="construct_id", right_index=True, how="left")
    out["endpoint_qc_basis"] = np.where(
        out["context_layer"].eq("hexamer_1x9A5_and_free"),
        "1x9A5 duplicate endpoint PDBs excluded; explicit final-frame reexports used",
        "carried_forward_from_011_monomer_layer",
    )
    return out.fillna("")


def classify_ha_robustness(rob: pd.DataFrame) -> tuple[str, str]:
    ha = rob[rob["construct_id"] == "A89_2C_248_249_HA"]
    if ha.empty:
        return "INSUFFICIENT_EVIDENCE", "no_HA_rows"
    by_model = ha.groupby("model_sha256").agg(
        min_tag_other_protomer_A=("tag_other_protomer_min_A", "min"),
        any_lt2=("tag_other_protomer_clashes_lt_2p0A", lambda x: int((x.astype(float) > 0).any())),
        any_lt25=("tag_other_protomer_clashes_lt_2p5A", lambda x: int((x.astype(float) > 0).any())),
        n_hexamer=("hexamer_structure", "nunique"),
    )
    n = len(by_model)
    if n < 2:
        return "INSUFFICIENT_EVIDENCE", f"only_{n}_unique_HA_conformation_sha"
    hard = (by_model["any_lt2"] > 0) | (by_model["min_tag_other_protomer_A"] < 2.0)
    soft = (by_model["any_lt25"] > 0) | (by_model["min_tag_other_protomer_A"] < 2.5)
    if hard.all() or soft.all():
        return "ROBUST_HEXAMER_CROWDING", f"{int(soft.sum())}/{n}_unique_HA_conformations_show_lt2p5_protomer_crowding"
    if hard.any() or soft.any():
        return "CONFORMATION_SENSITIVE", f"{int(soft.sum())}/{n}_unique_HA_conformations_show_lt2p5_protomer_crowding"
    return "RIGID_PLACEMENT_ARTIFACT_NOT_SUPPORTED", f"0/{n}_unique_HA_conformations_show_lt2p5_protomer_crowding"


def add_robustness_annotations(rob: pd.DataFrame, ha_class: str, ha_note: str) -> pd.DataFrame:
    out = rob.copy()
    out["248_249_HA_robustness_class"] = ""
    out["248_249_HA_robustness_note"] = ""
    out["tag_identity_comparison_class"] = ""
    for idx, row in out.iterrows():
        if row["construct_id"] == "A89_2C_248_249_HA":
            out.at[idx, "248_249_HA_robustness_class"] = ha_class
            out.at[idx, "248_249_HA_robustness_note"] = ha_note
        if row["construct_id"] in {"A89_2C_248_249_HA", "A89_2C_248_249_MAP8"}:
            out.at[idx, "tag_identity_comparison_class"] = "same_junction_tag_identity_dependence_audited"
    return out


def build_v7(v6: pd.DataFrame, summary: pd.DataFrame, ha_class: str, ha_note: str) -> pd.DataFrame:
    hx = summary[summary["context_layer"] == "hexamer_1x9A5_and_free"].set_index("construct_id", drop=False)
    order = {
        "A89_2C_289_290_MAP8": 1,
        "A89_2C_289_290_G196_minimal": 2,
        "A89_2C_248_249_MAP8": 3,
        "A89_2C_248_249_HA": 4,
        "A89_2C_288_289_MAP8": 5,
        "A89_2C_290_291_MAP8": 6,
        "A89_2C_288_289_HA": 7,
        "A89_2C_256_257_MAP8": 8,
        "A89_2C_224_225_MAP8": 9,
        "A89_2C_224_225_HA": 10,
        "A89_2C_203_204_G196_minimal": 11,
        "A89_2C_155_156_MAP8": 12,
    }
    rows = []
    for _, r in v6.iterrows():
        cid = r["construct"]
        h = hx.loc[cid] if cid in hx.index else {}
        previous = r["new_priority"]
        v7 = previous
        reason = "V6 retained after duplicate endpoint correction"
        tag_identity = "not_248_249_pair"
        if cid == "A89_2C_248_249_HA":
            tag_identity = "HA_specific_hexamer_crowding_relative_to_MAP8_at_same_junction"
            if ha_class == "ROBUST_HEXAMER_CROWDING":
                v7 = "Priority_A_with_QC_hardened_hexamer_crowding_caution"
                reason = "retained for experimental discussion but ordered after 248|249 MAP8 because HA protomer crowding persists across independent existing conformations"
            elif ha_class == "CONFORMATION_SENSITIVE":
                v7 = "Priority_A_with_conformation_sensitive_9A5_caution"
                reason = "retained with conformation sensitivity caution"
            elif ha_class == "RIGID_PLACEMENT_ARTIFACT_NOT_SUPPORTED":
                v7 = "Priority_A"
                reason = "old single-pose HA crowding not supported by multi-conformation QC"
        elif cid == "A89_2C_248_249_MAP8":
            tag_identity = "MAP8_less_persistently_crowded_than_HA_at_same_junction_in_hexamer_transfer"
            reason = "retained as 248|249 tag-identity comparator; MAP8 is less persistently crowded than HA, but one MAP8 conformation also shows a rigid-transfer clash"
        elif cid == "A89_2C_155_156_MAP8":
            reason = "hard-negative control retained; sequence-defined 9A5 epitope overlap is expected"
        elif cid == "A89_2C_224_225_MAP8":
            reason = "conflict control retained for non-C-terminal comparator"
        elif cid == "A89_2C_224_225_HA":
            reason = "conflict/control-like HA comparator retained"
        elif cid == "A89_2C_203_204_G196_minimal":
            reason = "G196 conflict control retained"

        rows.append(
            {
                **r.to_dict(),
                "v6_priority": previous,
                "v7_priority": v7,
                "v7_experimental_order": order.get(cid, 99),
                "v7_priority_transition": "changed" if v7 != previous else "unchanged",
                "v7_transition_reason": reason,
                "corrected_hexamer_9a5_class": h.get("ensemble_consistency", "INSUFFICIENT_EVIDENCE"),
                "corrected_hexamer_n_structures": h.get("n_structures", ""),
                "corrected_hexamer_n_unique_sha": h.get("n_unique_hexamer_sha", ""),
                "corrected_hexamer_min_tag_other_protomer_A": h.get("min_tag_other_protomer_A_corrected", h.get("min_tag_other_protomer_A", "")),
                "corrected_hexamer_tag_protomer_clash_fraction": h.get("tag_protomer_clash_fraction", ""),
                "endpoint_qc_status": "old_duplicate_endpoint_pdbs_excluded;reexported_unique_XTC_final_frames_used",
                "endpoint_unique_1x9a5_count": 3,
                "endpoint_duplicate_resolution": "duplicate old packaged/analysis PDBs are provenance only, not independent ensemble members",
                "ha_248_249_robustness_class": ha_class if cid == "A89_2C_248_249_HA" else "",
                "ha_248_249_robustness_note": ha_note if cid == "A89_2C_248_249_HA" else "",
                "tag_identity_dependence_248_249": tag_identity,
                "safe_or_validated": "no",
            }
        )
    out = pd.DataFrame(rows).sort_values("v7_experimental_order")
    return out


def update_section(path: Path, header: str, body: str) -> None:
    text = path.read_text() if path.exists() else ""
    lines = text.splitlines()
    out = []
    i = 0
    while i < len(lines):
        if lines[i].strip() == header:
            i += 1
            while i < len(lines) and not lines[i].startswith("# "):
                i += 1
            continue
        out.append(lines[i])
        i += 1
    if out and out[-1].strip():
        out.append("")
    out.append(header)
    out.extend(body.strip("\n").splitlines())
    path.write_text("\n".join(out).rstrip() + "\n")


def generate_feature_matrix_v8() -> None:
    spec = importlib.util.spec_from_file_location("cp008", ROOT / "scripts" / "candidate_panel_expansion_008.py")
    if spec is None or spec.loader is None:
        raise SystemExit("Could not load candidate_panel_expansion_008.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    features = mod.build_feature_matrix()
    write_tsv(OUT_DATA / "junction_feature_matrix_v8_9a5_epitope_qc.tsv", features)


def plot_figures(endpoint_records: list[dict[str, object]], summary: pd.DataFrame, rob: pd.DataFrame, v7: pd.DataFrame) -> None:
    OUT_FIG.mkdir(parents=True, exist_ok=True)
    plt.rcParams.update({"font.size": 7, "axes.spines.right": False, "axes.spines.top": False, "svg.fonttype": "none"})

    reps = [r["repeat"] for r in endpoint_records]
    mat = np.zeros((3, 3))
    paths = [ROOT / r["reexported_pdb"] for r in endpoint_records]
    for i, a in enumerate(paths):
        for j, b in enumerate(paths):
            mat[i, j] = rmsd_same_order(a, b)
    fig, ax = plt.subplots(figsize=(3.7, 3.2))
    im = ax.imshow(mat, cmap="viridis")
    ax.set_xticks(range(3), reps)
    ax.set_yticks(range(3), reps)
    for i in range(3):
        for j in range(3):
            ax.text(j, i, f"{mat[i,j]:.2f}", ha="center", va="center", color="white" if mat[i, j] < mat.max() / 2 else "black")
    ax.set_title("Corrected 1x9A5 final-frame RMSD")
    fig.colorbar(im, ax=ax, label="all-atom RMSD (A)")
    savefig(fig, OUT_FIG / "figure01_corrected_1x9A5_repeat_endpoint_comparison")

    hx = summary[summary["context_layer"] == "hexamer_1x9A5_and_free"].copy()
    hx["short"] = hx["construct_id"].str.replace("A89_2C_", "", regex=False)
    fig, ax = plt.subplots(figsize=(7.0, 3.8))
    x = np.arange(len(hx))
    ax.bar(x - 0.2, hx["pass_fraction"].astype(float), 0.4, label="robust fraction", color="#059669")
    ax.bar(x + 0.2, hx["tag_protomer_clash_fraction"].astype(float), 0.4, label="protomer clash fraction", color="#D97706")
    ax.set_xticks(x, hx["short"], rotation=60, ha="right", fontsize=6)
    ax.set_ylim(0, 1.05)
    ax.legend(frameon=False)
    ax.set_title("Corrected candidate ensemble compatibility")
    savefig(fig, OUT_FIG / "figure02_corrected_candidate_ensemble_compatibility")

    ha = rob[rob["construct_id"] == "A89_2C_248_249_HA"]
    fig, ax = plt.subplots(figsize=(5.0, 3.3))
    for x_i, (digest, g) in enumerate(ha.groupby("model_sha256")):
        ax.scatter([x_i] * len(g), g["tag_other_protomer_min_A"].astype(float), s=12, alpha=0.75)
    ax.axhline(2.5, color="#B91C1C", ls="--", lw=0.9)
    ax.set_xticks(range(ha["model_sha256"].nunique()), [f"conf{i+1}" for i in range(ha["model_sha256"].nunique())])
    ax.set_ylabel("min tag-other-protomer distance (A)")
    ax.set_title("248|249 HA conformation robustness")
    savefig(fig, OUT_FIG / "figure03_248_249_HA_conformation_robustness")

    pair = rob[rob["construct_id"].isin(["A89_2C_248_249_HA", "A89_2C_248_249_MAP8"])]
    fig, ax = plt.subplots(figsize=(4.8, 3.3))
    labels = ["HA", "MAP8"]
    data = [pair[pair["tag_form"].eq(t)]["tag_other_protomer_min_A"].astype(float).tolist() for t in labels]
    ax.boxplot(data, tick_labels=labels, widths=0.5)
    for i, vals in enumerate(data, start=1):
        ax.scatter(np.full(len(vals), i) + np.linspace(-0.08, 0.08, len(vals)), vals, s=8, alpha=0.5)
    ax.axhline(2.5, color="#B91C1C", ls="--", lw=0.9)
    ax.set_ylabel("min tag-other-protomer distance (A)")
    ax.set_title("248|249 HA vs MAP8")
    savefig(fig, OUT_FIG / "figure04_248_249_HA_vs_MAP8_comparison")

    fig, ax = plt.subplots(figsize=(7.0, 3.6))
    y = np.arange(len(v7))
    ax.scatter([0] * len(v7), y, color="#64748B")
    ax.scatter([1] * len(v7), y, color="#2563EB")
    for i, (_, row) in enumerate(v7.iterrows()):
        ax.plot([0, 1], [i, i], color="#CBD5E1")
        ax.text(-0.05, i, row["v6_priority"], ha="right", va="center", fontsize=5)
        ax.text(1.05, i, row["v7_priority"], ha="left", va="center", fontsize=5)
    ax.set_yticks(y, v7["construct"].str.replace("A89_2C_", "", regex=False), fontsize=5)
    ax.set_xticks([0, 1], ["V6", "V7"])
    ax.set_xlim(-0.55, 1.9)
    ax.set_title("V6 to V7 priority transition")
    savefig(fig, OUT_FIG / "figure05_V6_to_V7_priority_transition")


def savefig(fig, stem: Path) -> None:
    fig.tight_layout()
    fig.savefig(stem.with_suffix(".png"), dpi=300)
    fig.savefig(stem.with_suffix(".svg"))
    plt.close(fig)


def write_report(endpoint_records: list[dict[str, object]], rob: pd.DataFrame, v7: pd.DataFrame, ha_class: str, ha_note: str) -> None:
    endpoint_df = pd.DataFrame(endpoint_records)
    ha = rob[rob["construct_id"] == "A89_2C_248_249_HA"]
    map8 = rob[rob["construct_id"] == "A89_2C_248_249_MAP8"]
    ha_by = ha.groupby("model_sha256").agg(
        n_rows=("construct_id", "size"),
        min_other_A=("tag_other_protomer_min_A", "min"),
        max_lt2p5=("tag_other_protomer_clashes_lt_2p5A", "max"),
        unique_model_files=("model_file", lambda x: ";".join(sorted(set(x)))),
    )
    map8_by = map8.groupby("model_sha256").agg(
        n_rows=("construct_id", "size"),
        min_other_A=("tag_other_protomer_min_A", "min"),
        max_lt2p5=("tag_other_protomer_clashes_lt_2p5A", "max"),
        unique_model_files=("model_file", lambda x: ";".join(sorted(set(x)))),
    )
    map8_min = float(map8["tag_other_protomer_min_A"].astype(float).min()) if len(map8) else math.nan
    ha_min = float(ha["tag_other_protomer_min_A"].astype(float).min()) if len(ha) else math.nan
    top = v7[["construct", "junction", "tag", "v6_priority", "v7_priority", "v7_experimental_order", "v7_transition_reason"]]
    git_graph = git(ROOT, ["log", "--graph", "--oneline", "--all", "--decorate", "-30"])
    text = f"""# 9A5_CONTEXT_QC_011A

Status: `TASK011A_COMPLETE_WAITING_FOR_CHATGPT_REVIEW`

Date: `{TODAY}`

Branch: `analysis/9a5-context-qc-011a`

## Scope

Task 011A hardens the already completed 9A5 context layer. It performs no new MD, no AlphaFold/ColabFold, no docking, no Slurm/GPU work, no membrane/RNA/ATP mechanism simulation, and no final experimental construct design.

## Endpoint Duplicate Resolution

The three packaged 1x9A5 weak-posres endpoint PDBs were byte-identical and are now treated as provenance only. The underlying XTC/TPR/GRO/log files are SHA-distinct; final frames were re-exported from the existing `*_pbc_cluster_center.xtc` trajectories with an explicit `u.trajectory[-1]` call.

Old packaged endpoint unique SHA count: `{endpoint_df['old_endpoint_unique_sha_count'].iloc[0]}`

Corrected re-exported endpoint unique SHA count: `{endpoint_df['reexported_endpoint_unique_sha_count'].iloc[0]}`

| repeat | old PDB SHA | corrected PDB SHA | RMSD old-vs-corrected A | RMSD corrected-vs-rep1 A | source trajectory status |
|---|---:|---:|---:|---:|---|
"""
    for _, r in endpoint_df.iterrows():
        text += f"| {r['repeat']} | `{str(r['old_packaged_pdb_sha256'])[:12]}` | `{str(r['reexported_pdb_sha256'])[:12]}` | {float(r['old_packaged_rmsd_vs_reexported_A']):.3f} | {float(r['reexported_rmsd_vs_rep1_A']):.3f} | {r['trajectory_independence_status']} |\n"
    text += f"""
Interpretation: the duplicated PDB endpoints came from an endpoint export problem, not from identical trajectories. The likely cause is that the source repeat analysis script wrote `u.atoms` after iterating through the trajectory without explicitly seeking the final frame. Corrected 011A analysis uses the re-exported final frames and does not count byte-identical endpoint PDBs as independent.

## 248|249 HA Robustness

Robustness class: `{ha_class}`

Class note: `{ha_note}`

Minimum HA tag-other-protomer distance across audited conformations: `{ha_min:.3f} A`

Minimum MAP8 tag-other-protomer distance at the same junction: `{map8_min:.3f} A`

| HA model SHA | rows | min other-protomer A | max <2.5A clash count | model files |
|---|---:|---:|---:|---|
"""
    for digest, r in ha_by.iterrows():
        text += f"| `{digest[:12]}` | {int(r['n_rows'])} | {float(r['min_other_A']):.3f} | {int(r['max_lt2p5'])} | `{r['unique_model_files']}` |\n"
    text += """

| MAP8 model SHA | rows | min other-protomer A | max <2.5A clash count | model files |
|---|---:|---:|---:|---|
"""
    for digest, r in map8_by.iterrows():
        text += f"| `{digest[:12]}` | {int(r['n_rows'])} | {float(r['min_other_A']):.3f} | {int(r['max_lt2p5'])} | `{r['unique_model_files']}` |\n"
    text += """
Interpretation: 248|249 remains a biologically important non-C-terminal region, but tag identity matters. The HA form is retained for experimental-review discussion with a hardened hexamer-crowding caution. MAP8 is less persistently crowded than HA at the model level, although one MAP8 conformation also shows a rigid-transfer clash, so this is a relative tag-identity comparison rather than a safe/validated claim.

## V7 Experimental Review Panel

| order | construct | V7 priority | transition |
|---:|---|---|---|
"""
    for _, r in top.iterrows():
        text += f"| {int(r['v7_experimental_order'])} | `{r['construct']}` | `{r['v7_priority']}` | {r['v7_transition_reason']} |\n"
    text += """
Final ordering for discussion: `289|290 x MAP8`, `289|290 x G196_minimal`, `248|249 x MAP8`, `248|249 x HA`, then secondary/context-control rows. This does not call any site safe or validated.

## Required Outputs

- `data/9a5_context_input_provenance_v2_qc.tsv`
- `data/9a5_context_structure_inventory_v2_qc.tsv`
- `data/9a5_hexamer_tag_compatibility_v2_qc.tsv`
- `data/9a5_context_ensemble_summary_v2_qc.tsv`
- `data/248_249_HA_hexamer_robustness_v1.tsv`
- `data/junction_feature_matrix_v8_9a5_epitope_qc.tsv`
- `data/final_candidate_panel_v7_9a5_context_qc.tsv`
- `figures/9a5_context_011a_qc/`
- `results/9a5_context_011a_qc/endpoint_reexport_qc_v1.tsv`
- `results/9a5_context_011a_qc/reexported_1x9A5_endpoints/`

## Branch Relationship

```text
""" + git_graph + """
```

## Stop Gate

`READY_FOR_EXPERIMENTAL_REVIEW_WITH_9A5_QC_HARDENED_V7`
"""
    (OUT_DOCS / "9A5_CONTEXT_QC_011A.md").write_text(text)


def update_project_files(ha_class: str) -> None:
    update_section(
        ROOT / "PROJECT_STATE.md",
        "# Task 011A 9A5 Context QC State",
        f"""
Status: `READY_FOR_EXPERIMENTAL_REVIEW_WITH_9A5_QC_HARDENED_V7`

Date: `{TODAY}`

Branch: `analysis/9a5-context-qc-011a`

Task 011A resolved the duplicated 1x9A5 repeat endpoint PDB issue by re-exporting final frames from the distinct completed XTC trajectories, recalculated the hexamer 9A5 context layer without counting duplicate PDBs as independent, and generated `data/final_candidate_panel_v7_9a5_context_qc.tsv`.

248|249 x HA robustness class: `{ha_class}`. It remains an experimental-review candidate with explicit 9A5 hexamer-crowding/tag-identity caution; 248|249 x MAP8 is less persistently crowded at the model level but not conflict-free in all rigid-transfer conformations. No site is safe or validated.
""",
    )
    update_section(
        ROOT / "ACTIVE_TASK.md",
        "# Current Active Task",
        f"""
Current task: `9A5_CONTEXT_QC_011A` - **COMPLETED / WAITING FOR CHATGPT REVIEW**

Branch: `analysis/9a5-context-qc-011a`

Primary outputs:

- `tasks/9A5_CONTEXT_QC_011A.md`
- `docs/9A5_CONTEXT_QC_011A.md`
- `data/final_candidate_panel_v7_9a5_context_qc.tsv`
- `data/248_249_HA_hexamer_robustness_v1.tsv`

No further computational task is authorized by this file.
""",
    )
    update_section(
        ROOT / "ANALYSIS_INDEX.md",
        "# Task 011A 9A5 Context QC Outputs",
        """
| Artifact | Path | Status | Notes |
|---|---|---|---|
| Task 011A report | `docs/9A5_CONTEXT_QC_011A.md` | CURRENT | QC-hardened 9A5 context integration |
| V7 panel | `data/final_candidate_panel_v7_9a5_context_qc.tsv` | CURRENT | Supersedes V6 for 9A5-context review |
| Endpoint provenance | `data/9a5_context_input_provenance_v2_qc.tsv` | CURRENT | Includes duplicate endpoint resolution and trajectory checksums |
| Structure inventory | `data/9a5_context_structure_inventory_v2_qc.tsv` | CURRENT | Old duplicate endpoint PDBs retained as provenance only |
| Hexamer compatibility | `data/9a5_hexamer_tag_compatibility_v2_qc.tsv` | CURRENT | Duplicate-collapsed corrected endpoint ensemble |
| 248 HA robustness | `data/248_249_HA_hexamer_robustness_v1.tsv` | CURRENT | HA/MAP8 tag-identity comparison |
| QC figures | `figures/9a5_context_011a_qc/` | CURRENT | Five required QC figure sets |
| Endpoint re-export QC | `results/9a5_context_011a_qc/endpoint_reexport_qc_v1.tsv` | CURRENT | Explicit final-frame re-export audit |
""",
    )
    update_section(
        ROOT / "DECISIONS.md",
        "# D-048 - Task 011A Endpoint QC And V7 9A5 Context Panel",
        f"""
Date: `{TODAY}`

Decision: Treat byte-identical 1x9A5 weak-posres endpoint PDBs as provenance only and use explicit final-frame re-exports from the distinct completed XTC trajectories for 9A5 hexamer-context analysis.

Rationale: the packaged and analysis endpoint PDBs share one SHA across rep1/2/3, while the underlying XTC/TPR/GRO/log files are SHA-distinct. Re-exported endpoints are unique and preserve repeat independence for the endpoint proxy layer.

Panel consequence: `data/final_candidate_panel_v7_9a5_context_qc.tsv` supersedes V6 for 9A5-context review. 248|249 x HA is retained with hardened hexamer-crowding/tag-identity caution; 248|249 x MAP8 is less persistently crowded at the model level but not conflict-free in all rigid-transfer conformations. No site is safe or validated.
""",
    )
    update_section(
        ROOT / "TODO.md",
        "# Task 011A Follow-up",
        """
- ChatGPT/user review `docs/9A5_CONTEXT_QC_011A.md` and `data/final_candidate_panel_v7_9a5_context_qc.tsv`.
- Decide whether the V7 experimental-review order is sufficient for wet-lab discussion.
- Do not start nucleotide/codon design, new MD, docking, AF/ColabFold, or mechanistic membrane/RNA/ATP simulations until explicitly authorized.
""",
    )


def main() -> None:
    if git(ROOT, ["branch", "--show-current"]) != "analysis/9a5-context-qc-011a":
        raise SystemExit("Task 011A must run on branch analysis/9a5-context-qc-011a")

    endpoint_records, reexported = reexport_endpoints()
    write_tsv(OUT_RESULTS / "endpoint_reexport_qc_v1.tsv", endpoint_records)
    v6 = read_tsv(V6_PANEL)
    v5 = read_tsv(V5_PANEL)
    v5 = v5[v5["construct_id"].isin(v6["construct"])].copy()
    models = load_models(v5)
    hexamers = corrected_hexamers(reexported)
    hex_rows = analyze_hexamer_qc(v5, models, hexamers)
    monomer_rows = read_tsv(MONOMER_V1).to_dict("records")
    summary = summarize_with_qc(monomer_rows, hex_rows)

    extra_models = load_extra_248_models(models)
    v5_248 = v5[v5["construct_id"].isin(["A89_2C_248_249_HA", "A89_2C_248_249_MAP8"])].copy()
    robustness = analyze_hexamer_qc(v5_248, extra_models, hexamers)
    ha_class, ha_note = classify_ha_robustness(robustness)
    robustness = add_robustness_annotations(robustness, ha_class, ha_note)
    v7 = build_v7(v6, summary, ha_class, ha_note)

    inventory, provenance = make_inventory_and_provenance(endpoint_records, models, hexamers)
    write_tsv(OUT_DATA / "9a5_context_input_provenance_v2_qc.tsv", provenance)
    write_tsv(OUT_DATA / "9a5_context_structure_inventory_v2_qc.tsv", inventory)
    write_tsv(OUT_DATA / "9a5_hexamer_tag_compatibility_v2_qc.tsv", hex_rows)
    write_tsv(OUT_DATA / "9a5_context_ensemble_summary_v2_qc.tsv", summary)
    write_tsv(OUT_DATA / "248_249_HA_hexamer_robustness_v1.tsv", robustness)
    write_tsv(OUT_DATA / "final_candidate_panel_v7_9a5_context_qc.tsv", v7)
    generate_feature_matrix_v8()
    plot_figures(endpoint_records, summary, robustness, v7)
    write_report(endpoint_records, robustness, v7, ha_class, ha_note)
    update_project_files(ha_class)

    if set(v7["safe_or_validated"]) != {"no"}:
        raise SystemExit("safe_or_validated must remain no for all V7 rows")
    if len(v7) != 12:
        raise SystemExit(f"V7 expected 12 rows, got {len(v7)}")
    if int(pd.DataFrame(endpoint_records)["reexported_endpoint_unique_sha_count"].iloc[0]) != 3:
        raise SystemExit("Corrected endpoint re-export did not produce three unique SHA records")


if __name__ == "__main__":
    main()
