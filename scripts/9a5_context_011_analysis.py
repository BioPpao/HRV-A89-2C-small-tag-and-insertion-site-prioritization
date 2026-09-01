#!/usr/bin/env python3
"""Task 011: integrate existing 9A5-bound monomer/core and hexamer context.

This script deliberately reuses existing structures and prior candidate tables.
It performs no docking, AlphaFold, Slurm, GPU, or MD submission.
"""

from __future__ import annotations

import csv
import hashlib
import math
import os
import statistics
import subprocess
import sys
from dataclasses import dataclass, replace
from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd
import scipy

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

try:
    import mdtraj as md
except Exception:  # pragma: no cover - recorded in provenance if unavailable
    md = None

try:
    from scipy.spatial import cKDTree
except Exception as exc:  # pragma: no cover
    raise SystemExit(f"scipy.spatial.cKDTree is required for Task011 distance searches: {exc}")


ROOT = Path(__file__).resolve().parents[1]
SOURCE = Path("/public/home/yukang/HRV_Oligomers")
SOURCE_HEX = SOURCE / "HRV_A89_2C_HEXAMER"
SOURCE_SUMMARY = SOURCE_HEX / "results_summary"
SOURCE_CORE = SOURCE / "for_windows_download" / "current_candidate_structures"

OUT_DATA = ROOT / "data"
OUT_RESULTS = ROOT / "results" / "9a5_context_011"
OUT_DOCS = ROOT / "docs"
OUT_FIG = ROOT / "figures" / "9a5_context_011"
OUT_PROXY = OUT_RESULTS / "proxy_structures"
TODAY = "2026-09-02"

REF_FASTA = ROOT / "references" / "HRV_A89_2C_reference_sequence.fasta"
V5_PANEL = ROOT / "data" / "final_candidate_panel_v5_experimental_review_cleanup.tsv"
SHALLOW_MANIFEST = ROOT / "results" / "open_structure_007" / "tier1_shallow_manifest.tsv"
DEEP_MANIFEST = ROOT / "results" / "open_structure_007" / "deep_subset_manifest.tsv"
SEQ_MANIFEST = ROOT / "results" / "open_structure_007" / "sequence_manifest_v3_open.tsv"
TAG_BINDER = ROOT / "data" / "tag_binder_accessibility_v1.tsv"

EPITOPE = set(range(148, 161))
VH_CDRS = set(list(range(27, 35)) + list(range(52, 60)) + list(range(98, 108)))
VL_CDRS = set(list(range(27, 38)) + list(range(55, 58)) + list(range(94, 103)))
HEX_CHAINS = list("ABCDEF")
HEAVY_BACKBONE = {"N", "CA", "C", "O"}
AA3_TO_1 = {
    "ALA": "A",
    "ARG": "R",
    "ASN": "N",
    "ASP": "D",
    "CYS": "C",
    "GLN": "Q",
    "GLU": "E",
    "GLY": "G",
    "HIS": "H",
    "ILE": "I",
    "LEU": "L",
    "LYS": "K",
    "MET": "M",
    "PHE": "F",
    "PRO": "P",
    "SER": "S",
    "THR": "T",
    "TRP": "W",
    "TYR": "Y",
    "VAL": "V",
}


@dataclass(frozen=True)
class Atom:
    record: str
    serial: int
    name: str
    resname: str
    chain: str
    resid: int
    icode: str
    x: float
    y: float
    z: float
    occ: float
    bfac: float
    elem: str

    @property
    def coord(self) -> np.ndarray:
        return np.array([self.x, self.y, self.z], dtype=float)

    @property
    def key(self) -> tuple[str, int, str]:
        return (self.chain, self.resid, self.name)

    def label(self) -> str:
        return f"{self.chain}:{self.resname}{self.resid}:{self.name}"


def run_git(repo: Path, args: list[str]) -> str:
    try:
        return subprocess.check_output(["git", "-C", str(repo)] + args, text=True).strip()
    except Exception as exc:
        return f"ERROR:{exc}"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def read_fasta(path: Path) -> str:
    return "".join(line.strip() for line in path.read_text().splitlines() if not line.startswith(">"))


def parse_pdb(path: Path) -> list[Atom]:
    atoms: list[Atom] = []
    for line in path.read_text(errors="ignore").splitlines():
        if not line.startswith(("ATOM", "HETATM")):
            continue
        elem = line[76:78].strip().upper()
        if not elem:
            letters = "".join(ch for ch in line[12:16].strip() if ch.isalpha())
            elem = letters[:1].upper()
        try:
            atom = Atom(
                record=line[:6].strip(),
                serial=int(line[6:11]),
                name=line[12:16].strip(),
                resname=line[17:20].strip(),
                chain=(line[21].strip() or "_"),
                resid=int(line[22:26]),
                icode=line[26].strip(),
                x=float(line[30:38]),
                y=float(line[38:46]),
                z=float(line[46:54]),
                occ=float(line[54:60] or 0),
                bfac=float(line[60:66] or 0),
                elem=elem,
            )
        except ValueError:
            continue
        atoms.append(atom)
    return atoms


def is_heavy(a: Atom) -> bool:
    return a.elem != "H"


def coords(atoms: Iterable[Atom]) -> np.ndarray:
    arr = [a.coord for a in atoms]
    if not arr:
        return np.empty((0, 3), dtype=float)
    return np.vstack(arr)


def transform_atom(a: Atom, rot: np.ndarray, mov_centroid: np.ndarray, tgt_centroid: np.ndarray, chain: str | None = None) -> Atom:
    xyz = (a.coord - mov_centroid) @ rot + tgt_centroid
    return replace(a, chain=chain or a.chain, x=float(xyz[0]), y=float(xyz[1]), z=float(xyz[2]))


def kabsch(moving: np.ndarray, target: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray, float]:
    if moving.shape != target.shape or moving.shape[0] < 3:
        raise ValueError(f"Bad Kabsch input shapes: {moving.shape} vs {target.shape}")
    mc = moving.mean(axis=0)
    tc = target.mean(axis=0)
    cov = (moving - mc).T @ (target - tc)
    v, _, wt = np.linalg.svd(cov)
    d = np.sign(np.linalg.det(v @ wt))
    rot = v @ np.diag([1.0, 1.0, d]) @ wt
    aligned = (moving - mc) @ rot + tc
    rmsd = float(np.sqrt(np.mean(np.sum((aligned - target) ** 2, axis=1))))
    return rot, mc, tc, rmsd


def pair_stats(a_atoms: list[Atom], b_atoms: list[Atom], cutoffs=(2.0, 2.5, 4.5, 5.0)) -> dict[str, object]:
    a = [x for x in a_atoms if is_heavy(x)]
    b = [x for x in b_atoms if is_heavy(x)]
    if not a or not b:
        return {
            "min_A": math.nan,
            "closest_pair": "NA",
            **{f"pairs_lt_{str(c).replace('.', 'p')}A": 0 for c in cutoffs},
        }
    ca = coords(a)
    cb = coords(b)
    ta = cKDTree(ca)
    tb = cKDTree(cb)
    dists, idxs = tb.query(ca, k=1)
    min_i = int(np.argmin(dists))
    min_j = int(idxs[min_i])
    min_d = float(dists[min_i])
    counts = {c: int(ta.count_neighbors(tb, c)) for c in cutoffs}
    out = {
        "min_A": min_d,
        "closest_pair": f"{a[min_i].label()}--{b[min_j].label()}",
    }
    for c in cutoffs:
        out[f"pairs_lt_{str(c).replace('.', 'p')}A"] = counts[c]
    return out


def make_heavy_group(atoms: list[Atom]) -> dict[str, object]:
    heavy = [a for a in atoms if is_heavy(a)]
    if not heavy:
        return {"atoms": [], "coords": np.empty((0, 3)), "tree": None}
    c = coords(heavy)
    return {"atoms": heavy, "coords": c, "tree": cKDTree(c)}


def pair_stats_group(a_atoms: list[Atom], group: dict[str, object], cutoffs=(2.0, 2.5, 4.5, 5.0)) -> dict[str, object]:
    a = [x for x in a_atoms if is_heavy(x)]
    b = group["atoms"]
    tree = group["tree"]
    if not a or not b or tree is None:
        return {
            "min_A": math.nan,
            "closest_pair": "NA",
            **{f"pairs_lt_{str(c).replace('.', 'p')}A": 0 for c in cutoffs},
        }
    ca = coords(a)
    dists, idxs = tree.query(ca, k=1)
    min_i = int(np.argmin(dists))
    min_j = int(idxs[min_i])
    out = {"min_A": float(dists[min_i]), "closest_pair": f"{a[min_i].label()}--{b[min_j].label()}"}
    for c in cutoffs:
        out[f"pairs_lt_{str(c).replace('.', 'p')}A"] = int(sum(len(tree.query_ball_point(pt, c)) for pt in ca))
    return out


def rmsd_for_atom_names(a_atoms: list[Atom], b_atoms: list[Atom], residues: Iterable[int], names: set[str]) -> float:
    a_map = {(a.resid, a.name): a.coord for a in a_atoms if a.resid in residues and a.name in names}
    b_map = {(b.resid, b.name): b.coord for b in b_atoms if b.resid in residues and b.name in names}
    keys = sorted(set(a_map) & set(b_map))
    if len(keys) < 3:
        return math.nan
    aa = np.vstack([a_map[k] for k in keys])
    bb = np.vstack([b_map[k] for k in keys])
    return float(np.sqrt(np.mean(np.sum((aa - bb) ** 2, axis=1))))


def chain_residue_summary(atoms: list[Atom]) -> tuple[str, int, int, str, str, bool]:
    by_chain: dict[str, list[int]] = {}
    for a in atoms:
        by_chain.setdefault(a.chain, []).append(a.resid)
    ranges = []
    n2c = 0
    vh = "NA"
    vl = "NA"
    for ch, residues in sorted(by_chain.items()):
        uniq = sorted(set(residues))
        ranges.append(f"{ch}:{uniq[0]}-{uniq[-1]}({len(uniq)})")
        if len(uniq) >= 300 and uniq[0] == 1:
            n2c += 1
        elif uniq[0] <= 112 and uniq[-1] >= 258:
            n2c += 1
        if len(uniq) in range(116, 121):
            vh = ch
        if len(uniq) in range(109, 114):
            vl = ch
    finite = bool(all(np.isfinite([a.x, a.y, a.z]).all() for a in atoms))
    return ";".join(ranges), n2c, len(atoms), vh, vl, finite


def classify_source_structure(path: Path) -> dict[str, str]:
    name = path.name
    rel = str(path.relative_to(SOURCE) if str(path).startswith(str(SOURCE)) else path.relative_to(ROOT))
    status = "REFERENCE"
    usable = "yes"
    reason = "selected_for_task011_primary_or_context_analysis"
    sclass = "unknown"
    state = "unknown"
    refinement = "unknown"
    antibody = "no"
    antibody_type = "none"
    if "2x_9A5" in name:
        sclass = "2x9A5_hexamer_complex"
        state = "hexamer"
        antibody = "yes"
        antibody_type = "9A5_Fv"
        status = "NEGATIVE_OR_AUDIT_ONLY"
        usable = "audit_only"
        reason = "2x9A5_stress_test_not_primary_ranking"
    elif "1x_9A5" in name or "C01_chainD" in name or "SHOWCASE_1x_9A5" in name:
        sclass = "1x9A5_hexamer_complex"
        state = "full_length_hexamer"
        antibody = "yes"
        antibody_type = "9A5_Fv"
        status = "CURRENT" if "SHOWCASE" in name or "weakposres_1ns" in name else "DEPRECATED_OR_REFERENCE"
        refinement = "pbc_fixed_or_endpoint_refined"
    elif "C04" in name or "C01" in name:
        sclass = "1x9A5_core_complex"
        state = "2C_core_112_258"
        antibody = "yes"
        antibody_type = "9A5_Fv"
        status = "REFERENCE"
        refinement = "historical_30ns_core_complex"
    elif "selected_hexamer" in name or "SHOWCASE_no_membrane" in name:
        sclass = "free_hexamer"
        state = "full_length_hexamer"
        refinement = "selected_or_repeat_endpoint"
        status = "CURRENT_OR_REFERENCE"
    elif "A89_2C_" in name and name.endswith(".pdb"):
        sclass = "tagged_monomer"
        state = "full_length_tagged_monomer"
        status = "TAGGED_MODEL"
        refinement = "ColabFold_unrelaxed"
    return {
        "relative_path": rel,
        "filename": name,
        "structure_class": sclass,
        "2c_state": state,
        "antibody_present": antibody,
        "antibody_type": antibody_type,
        "refinement_state": refinement,
        "registry_status": status,
        "usable_for_primary_analysis": usable,
        "reason": reason,
    }


def native_model_resid(a89_resid: int, left: int, tag_len: int) -> int:
    return a89_resid if a89_resid <= left else a89_resid + tag_len


def get_ca_by_resid(atoms: list[Atom], chain: str) -> dict[int, Atom]:
    return {a.resid: a for a in atoms if a.chain == chain and a.name == "CA"}


def get_group(atoms: list[Atom], chain: str | set[str], residues: set[int] | None = None, names: set[str] | None = None) -> list[Atom]:
    chains = {chain} if isinstance(chain, str) else set(chain)
    out = []
    for a in atoms:
        if a.chain not in chains:
            continue
        if residues is not None and a.resid not in residues:
            continue
        if names is not None and a.name not in names:
            continue
        out.append(a)
    return out


def cdr_atoms(atoms: list[Atom], vh: str, vl: str) -> list[Atom]:
    out = []
    for a in atoms:
        if not is_heavy(a):
            continue
        if a.chain == vh and a.resid in VH_CDRS:
            out.append(a)
        elif a.chain == vl and a.resid in VL_CDRS:
            out.append(a)
    return out


def epitope_contact_retention(template_atoms: list[Atom], candidate_atoms: list[Atom], two_c_chain: str, vh: str, vl: str) -> float:
    cdr = cdr_atoms(template_atoms, vh, vl)
    epi = [a for a in template_atoms if a.chain == two_c_chain and a.resid in EPITOPE and is_heavy(a)]
    cand_epi = [a for a in candidate_atoms if a.resid in EPITOPE and is_heavy(a)]
    if not cdr or not epi or not cand_epi:
        return math.nan
    template_pairs = set()
    by_ab: dict[tuple[str, int], list[Atom]] = {}
    by_epi: dict[int, list[Atom]] = {}
    by_cand_epi: dict[int, list[Atom]] = {}
    for a in cdr:
        by_ab.setdefault((a.chain, a.resid), []).append(a)
    for a in epi:
        by_epi.setdefault(a.resid, []).append(a)
    for a in cand_epi:
        by_cand_epi.setdefault(a.resid, []).append(a)
    for ab_key, ab_atoms in by_ab.items():
        for e_res, e_atoms in by_epi.items():
            if pair_stats(ab_atoms, e_atoms, (5.0,))["pairs_lt_5p0A"] > 0:
                template_pairs.add((ab_key, e_res))
    if not template_pairs:
        return math.nan
    retained = 0
    for ab_key, e_res in template_pairs:
        if e_res not in by_cand_epi:
            continue
        if pair_stats(by_ab[ab_key], by_cand_epi[e_res], (5.0,))["pairs_lt_5p0A"] > 0:
            retained += 1
    return retained / len(template_pairs)


def static_tag_sasa(path: Path, tag_resids: set[int]) -> float:
    if md is None:
        return math.nan
    try:
        traj = md.load(str(path))
        sasa = md.shrake_rupley(traj, mode="atom")[0] * 100.0
        total = 0.0
        for atom in traj.topology.atoms:
            if atom.residue.resSeq in tag_resids:
                total += float(sasa[atom.index])
        return total
    except Exception:
        return math.nan


def parse_existing_tag_sasa(value: object) -> float:
    text = str(value)
    marker = "total_A2="
    if marker not in text:
        return math.nan
    try:
        return float(text.split(marker, 1)[1].split(";", 1)[0])
    except Exception:
        return math.nan


def summarize_numbers(values: list[float]) -> dict[str, float]:
    vals = [float(v) for v in values if pd.notna(v) and math.isfinite(float(v))]
    if not vals:
        return {"n": 0, "min": math.nan, "max": math.nan, "median": math.nan, "mean": math.nan, "sd": math.nan}
    return {
        "n": len(vals),
        "min": min(vals),
        "max": max(vals),
        "median": statistics.median(vals),
        "mean": statistics.mean(vals),
        "sd": statistics.stdev(vals) if len(vals) > 1 else 0.0,
    }


def class_from_monomer(row: pd.Series) -> str:
    if row["tag_overlaps_sequence_defined_9a5_epitope"] == "yes":
        return "EPITOPE_PERTURBATION_RISK"
    if row["tag_fv_clashes_lt_2p0A"] > 0 or row["tag_fv_min_A"] < 2.0:
        return "ANTIBODY_STERIC_CONFLICT"
    if row["tag_fv_min_A"] < 3.0 or row["tag_native_nonlocal_contacts_4p5A"] > 25:
        return "MONOMER_CONTEXT_SENSITIVE"
    return "ROBUST_9A5_CONTEXT"


def class_from_hex(row: pd.Series) -> str:
    if row["antibody_present"] == "yes" and (row["tag_ab_clashes_lt_2p0A"] > 0 or row["tag_ab_min_A"] < 2.0):
        return "ANTIBODY_STERIC_CONFLICT"
    if row["tag_tag_clashes_lt_2p0A"] > 0:
        return "TAG_TAG_HEXAMER_CONFLICT"
    if row["tag_other_protomer_clashes_lt_2p0A"] > 0 or row["tag_other_protomer_min_A"] < 2.5:
        return "HEXAMER_CONTEXT_SENSITIVE"
    return "ROBUST_9A5_CONTEXT"


def consistency_from_classes(classes: list[str]) -> str:
    unique = set(classes)
    if not unique:
        return "INSUFFICIENT_EVIDENCE"
    if len(unique) == 1:
        return "CONSISTENT_" + next(iter(unique))
    if any(c in unique for c in ["ANTIBODY_STERIC_CONFLICT", "EPITOPE_PERTURBATION_RISK", "TAG_TAG_HEXAMER_CONFLICT"]):
        return "CONFLICT_ACROSS_STRUCTURES"
    return "SENSITIVE_ACROSS_STRUCTURES"


def write_tsv(path: Path, rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        keys: list[str] = []
        for row in rows:
            for key in row:
                if key not in keys:
                    keys.append(key)
        fieldnames = keys
    with path.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames, delimiter="\t", extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def make_inventory(tagged_model_rows: pd.DataFrame) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    source_commit = run_git(SOURCE, ["rev-parse", "HEAD"])
    target_commit = run_git(ROOT, ["rev-parse", "HEAD"])
    paths = [
        SOURCE_CORE / "07_C04_LEAD_9A5_2C_final30_complex.pdb",
        SOURCE_CORE / "08_C01_COMPARATOR_9A5_2C_final30_complex.pdb",
        SOURCE_SUMMARY / "selected_hexamer_01_md_representative.pdb",
        SOURCE_SUMMARY / "selected_hexamer_02_md_representative.pdb",
        SOURCE_SUMMARY / "selected_hexamer_01_md_representative_5ns_rep1.pdb",
        SOURCE_SUMMARY / "selected_hexamer_01_md_representative_5ns_rep2.pdb",
        SOURCE_SUMMARY / "selected_hexamer_01_md_representative_5ns_rep3.pdb",
        SOURCE_SUMMARY / "SHOWCASE_1x_9A5_D_chain_after_npt_100ps_pbc_fixed.pdb",
        SOURCE_SUMMARY / "selected_1x_9A5_weakposres_1ns_rep1_endpoint.pdb",
        SOURCE_SUMMARY / "selected_1x_9A5_weakposres_1ns_rep2_endpoint.pdb",
        SOURCE_SUMMARY / "selected_1x_9A5_weakposres_1ns_rep3_endpoint.pdb",
        SOURCE_SUMMARY / "selected_2x_9A5_candidate_01_E_rigidbody_80_after_em2_rechained.pdb",
        SOURCE_SUMMARY / "selected_2x_9A5_top1_E_after_npt_100ps_rechained_pbc_fixed.pdb",
    ]
    paths += [ROOT / p for p in sorted(tagged_model_rows["model_file"].dropna().unique())]
    inv = []
    prov = []
    for path in paths:
        if not path.exists():
            inv.append(
                {
                    "source_repository": "BioPpao/HRV-Oligomers" if str(path).startswith(str(SOURCE)) else "BioPpao/HRV-A89-2C-small-tag-and-insertion-site-prioritization",
                    "source_commit": source_commit if str(path).startswith(str(SOURCE)) else target_commit,
                    "absolute_path": str(path),
                    "relative_path": "missing",
                    "filename": path.name,
                    "sha256": "missing",
                    "structure_class": "missing",
                    "2c_state": "missing",
                    "2c_residue_range": "missing",
                    "n_2c_chains": 0,
                    "antibody_present": "unknown",
                    "antibody_type": "unknown",
                    "VH_chain": "NA",
                    "VL_chain": "NA",
                    "refinement_state": "missing",
                    "registry_status": "MISSING",
                    "usable_for_primary_analysis": "no",
                    "reason": "file_missing",
                }
            )
            continue
        atoms = parse_pdb(path)
        ranges, n2c, atom_count, vh, vl, finite = chain_residue_summary(atoms)
        meta = classify_source_structure(path)
        repo = "BioPpao/HRV-Oligomers" if str(path).startswith(str(SOURCE)) else "BioPpao/HRV-A89-2C-small-tag-and-insertion-site-prioritization"
        commit = source_commit if repo.endswith("HRV-Oligomers") else target_commit
        inv.append(
            {
                "source_repository": repo,
                "source_commit": commit,
                "absolute_path": str(path),
                "relative_path": meta["relative_path"],
                "filename": path.name,
                "sha256": sha256(path),
                "structure_class": meta["structure_class"],
                "2c_state": meta["2c_state"],
                "2c_residue_range": ranges,
                "n_2c_chains": n2c,
                "antibody_present": meta["antibody_present"],
                "antibody_type": meta["antibody_type"],
                "VH_chain": vh if meta["antibody_present"] == "yes" else "NA",
                "VL_chain": vl if meta["antibody_present"] == "yes" else "NA",
                "refinement_state": meta["refinement_state"],
                "registry_status": meta["registry_status"],
                "usable_for_primary_analysis": meta["usable_for_primary_analysis"] if finite and atom_count else "no",
                "reason": meta["reason"] if finite else "nonfinite_or_unreadable_coordinates",
            }
        )
        prov.append(
            {
                "source_repository": repo,
                "source_commit": commit,
                "absolute_path": str(path),
                "relative_path": meta["relative_path"],
                "sha256": sha256(path),
                "role_in_task011": meta["structure_class"],
                "date_accessed": TODAY,
                "qc_status": "finite_coordinates" if finite else "nonfinite_coordinates",
            }
        )
    return inv, prov


def candidate_models(panel: pd.DataFrame) -> pd.DataFrame:
    manifests = []
    for path in [DEEP_MANIFEST, SHALLOW_MANIFEST]:
        df = pd.read_csv(path, sep="\t")
        df["manifest_source"] = path.relative_to(ROOT).as_posix()
        manifests.append(df)
    models = pd.concat(manifests, ignore_index=True)
    models = models[models["construct_id"].isin(panel["construct_id"])]
    models = models[models["prediction_status"].fillna("") == "completed"]
    models = models.drop_duplicates(["construct_id", "model_file"])
    seq = pd.read_csv(SEQ_MANIFEST, sep="\t")[["construct_id", "tag_sequence"]].drop_duplicates("construct_id")
    models = models.merge(seq, on="construct_id", how="left")
    return models


def align_tagged_to_target(
    model_atoms: list[Atom],
    target_atoms: list[Atom],
    target_chain: str,
    left: int,
    right: int,
    tag_len: int,
    residues: Iterable[int],
) -> tuple[list[Atom], list[Atom], float, int]:
    model_ca = get_ca_by_resid(model_atoms, "A")
    target_ca = get_ca_by_resid(target_atoms, target_chain)
    m = []
    t = []
    used = []
    for r in residues:
        mr = native_model_resid(r, left, tag_len)
        if mr in model_ca and r in target_ca:
            m.append(model_ca[mr].coord)
            t.append(target_ca[r].coord)
            used.append(r)
    rot, mc, tc, fit = kabsch(np.vstack(m), np.vstack(t))
    tag_resids = set(range(left + 1, left + tag_len + 1))
    tag_atoms = [transform_atom(a, rot, mc, tc, chain=target_chain) for a in model_atoms if a.chain == "A" and a.resid in tag_resids]
    native_atoms = []
    for a in model_atoms:
        if a.chain != "A" or a.resid in tag_resids:
            continue
        if a.resid <= left:
            a89_resid = a.resid
        else:
            a89_resid = a.resid - tag_len
        native_atoms.append(replace(transform_atom(a, rot, mc, tc, chain=target_chain), resid=a89_resid))
    return tag_atoms, native_atoms, fit, len(used)


def analyze_monomer(panel: pd.DataFrame, models: pd.DataFrame) -> list[dict[str, object]]:
    poses = [
        ("C04_core_reference", SOURCE_CORE / "07_C04_LEAD_9A5_2C_final30_complex.pdb", "C", "A", "B"),
        ("C01_core_reference", SOURCE_CORE / "08_C01_COMPARATOR_9A5_2C_final30_complex.pdb", "C", "A", "B"),
    ]
    rows = []
    model_cache = {p: parse_pdb(ROOT / p) for p in models["model_file"].unique()}
    pose_cache = {pose_path: parse_pdb(pose_path) for _, pose_path, _, _, _ in poses}
    pose_groups = {}
    for pose_name, pose_path, two_c_chain, vh, vl in poses:
        pose_atoms = pose_cache[pose_path]
        pose_groups[pose_path] = {
            "fv": make_heavy_group([a for a in pose_atoms if a.chain in {vh, vl}]),
            "vh": make_heavy_group([a for a in pose_atoms if a.chain == vh]),
            "vl": make_heavy_group([a for a in pose_atoms if a.chain == vl]),
            "cdr": make_heavy_group(cdr_atoms(pose_atoms, vh, vl)),
        }
    for _, cand in panel.iterrows():
        left = int(cand["junction"].split("|")[0])
        right = int(cand["junction"].split("|")[1])
        tag_len = int(models[models.construct_id == cand.construct_id]["tag_length"].iloc[0])
        tag_seq = str(models[models.construct_id == cand.construct_id]["tag_sequence"].iloc[0])
        for _, model in models[models.construct_id == cand.construct_id].iterrows():
            model_file = str(model["model_file"])
            model_atoms = model_cache[model_file]
            tag_resids = set(range(left + 1, left + tag_len + 1))
            for pose_name, pose_path, two_c_chain, vh, vl in poses:
                pose_atoms = pose_cache[pose_path]
                groups = pose_groups[pose_path]
                tag_atoms, native_atoms, fit, nfit = align_tagged_to_target(
                    model_atoms, pose_atoms, two_c_chain, left, right, tag_len, range(112, 259)
                )
                cdr = cdr_atoms(pose_atoms, vh, vl)
                epi_template = [a for a in pose_atoms if a.chain == two_c_chain and a.resid in EPITOPE]
                epi_native = [a for a in native_atoms if a.resid in EPITOPE]
                nonlocal_res = set(range(1, 322)) - set(range(max(1, left - 5), min(321, right + 5) + 1))
                nonlocal_native = [a for a in native_atoms if a.resid in nonlocal_res]
                fv = pair_stats_group(tag_atoms, groups["fv"])
                vhstat = pair_stats_group(tag_atoms, groups["vh"])
                vlstat = pair_stats_group(tag_atoms, groups["vl"])
                cdrstat = pair_stats_group(tag_atoms, groups["cdr"])
                nlc = pair_stats(tag_atoms, nonlocal_native, (4.5, 5.0))
                epi_min = pair_stats(cdr, epi_native, (4.5, 5.0))
                row = {
                    "construct_id": cand.construct_id,
                    "junction": cand.junction,
                    "tag_form": cand.tag_form,
                    "tag_sequence": tag_seq,
                    "tag_length": tag_len,
                    "model_file": model_file,
                    "model_rank": model["rank"],
                    "model_seed": model["seed"],
                    "monomer_pose": pose_name,
                    "pose_source_path": str(pose_path),
                    "pose_2c_range": "112-258",
                    "alignment_residue_count": nfit,
                    "native_core_fit_rmsd_A": fit,
                    "tag_fv_min_A": fv["min_A"],
                    "tag_fv_clashes_lt_2p0A": fv["pairs_lt_2p0A"],
                    "tag_fv_clashes_lt_2p5A": fv["pairs_lt_2p5A"],
                    "tag_fv_contacts_4p5A": fv["pairs_lt_4p5A"],
                    "tag_fv_contacts_5p0A": fv["pairs_lt_5p0A"],
                    "tag_vh_min_A": vhstat["min_A"],
                    "tag_vl_min_A": vlstat["min_A"],
                    "tag_cdr_min_A": cdrstat["min_A"],
                    "closest_tag_fv_pair": fv["closest_pair"],
                    "epitope_ca_rmsd_A": rmsd_for_atom_names(epi_native, epi_template, EPITOPE, {"CA"}),
                    "epitope_backbone_rmsd_A": rmsd_for_atom_names(epi_native, epi_template, EPITOPE, HEAVY_BACKBONE),
                    "cdr_epitope_contacts_4p5A_after_transfer": epi_min["pairs_lt_4p5A"],
                    "min_cdr_epitope_A_after_transfer": epi_min["min_A"],
                    "cdr_epitope_contact_retention_fraction": epitope_contact_retention(
                        pose_atoms, epi_native, two_c_chain, vh, vl
                    ),
                    "tag_static_sasa_A2": parse_existing_tag_sasa(cand.get("tag_SASA_exposure", "")),
                    "tag_native_nonlocal_contacts_4p5A": nlc["pairs_lt_4p5A"],
                    "tag_native_nonlocal_min_A": nlc["min_A"],
                    "tag_overlaps_sequence_defined_9a5_epitope": "yes" if (left in EPITOPE or right in EPITOPE) else "no",
                    "analysis_note": "core_pose_transfer_no_blind_docking",
                }
                row["monomer_9a5_class"] = class_from_monomer(pd.Series(row))
                rows.append(row)
    return rows


def analyze_hexamer(panel: pd.DataFrame, models: pd.DataFrame) -> list[dict[str, object]]:
    hexamers = [
        ("1x9A5_100ps_showcase", SOURCE_SUMMARY / "SHOWCASE_1x_9A5_D_chain_after_npt_100ps_pbc_fixed.pdb", "yes"),
        ("1x9A5_1ns_rep1", SOURCE_SUMMARY / "selected_1x_9A5_weakposres_1ns_rep1_endpoint.pdb", "yes"),
        ("1x9A5_1ns_rep2", SOURCE_SUMMARY / "selected_1x_9A5_weakposres_1ns_rep2_endpoint.pdb", "yes"),
        ("1x9A5_1ns_rep3", SOURCE_SUMMARY / "selected_1x_9A5_weakposres_1ns_rep3_endpoint.pdb", "yes"),
        ("free_hexamer_2ns_lead", SOURCE_SUMMARY / "selected_hexamer_01_md_representative.pdb", "no"),
        ("free_hexamer_5ns_rep1", SOURCE_SUMMARY / "selected_hexamer_01_md_representative_5ns_rep1.pdb", "no"),
        ("free_hexamer_5ns_rep2", SOURCE_SUMMARY / "selected_hexamer_01_md_representative_5ns_rep2.pdb", "no"),
        ("free_hexamer_5ns_rep3", SOURCE_SUMMARY / "selected_hexamer_01_md_representative_5ns_rep3.pdb", "no"),
        ("free_hexamer_control_model1", SOURCE_SUMMARY / "selected_hexamer_02_md_representative.pdb", "no"),
    ]
    rows = []
    model_cache = {p: parse_pdb(ROOT / p) for p in models["model_file"].unique()}
    hex_cache = {hpath: parse_pdb(hpath) for _, hpath, _ in hexamers}
    hex_groups = {}
    for _, hpath, _ in hexamers:
        hex_atoms = hex_cache[hpath]
        groups = {
            "ab": make_heavy_group([a for a in hex_atoms if a.chain in {"H", "L", "G"}]),
            "adj": {},
            "nonadj": {},
        }
        for i, chain in enumerate(HEX_CHAINS):
            adj = {HEX_CHAINS[(i - 1) % 6], HEX_CHAINS[(i + 1) % 6]}
            nonadj = set(HEX_CHAINS) - adj - {chain}
            groups["adj"][chain] = make_heavy_group([a for a in hex_atoms if a.chain in adj])
            groups["nonadj"][chain] = make_heavy_group([a for a in hex_atoms if a.chain in nonadj])
        hex_groups[hpath] = groups
    for _, cand in panel.iterrows():
        left = int(cand["junction"].split("|")[0])
        right = int(cand["junction"].split("|")[1])
        tag_len = int(models[models.construct_id == cand.construct_id]["tag_length"].iloc[0])
        tag_seq = str(models[models.construct_id == cand.construct_id]["tag_sequence"].iloc[0])
        for _, model in models[models.construct_id == cand.construct_id].iterrows():
            model_file = str(model["model_file"])
            model_atoms = model_cache[model_file]
            for hname, hpath, antibody_present in hexamers:
                hex_atoms = hex_cache[hpath]
                groups = hex_groups[hpath]
                tag_by_chain: dict[str, list[Atom]] = {}
                fit_vals = []
                nfit_vals = []
                for chain in HEX_CHAINS:
                    tag_atoms, _, fit, nfit = align_tagged_to_target(
                        model_atoms, hex_atoms, chain, left, right, tag_len, range(1, 322)
                    )
                    tag_by_chain[chain] = tag_atoms
                    fit_vals.append(fit)
                    nfit_vals.append(nfit)
                all_tag_atoms = [a for atoms in tag_by_chain.values() for a in atoms]
                abstat = pair_stats_group(all_tag_atoms, groups["ab"]) if antibody_present == "yes" else {
                    "min_A": math.nan,
                    "closest_pair": "NA",
                    "pairs_lt_2p0A": 0,
                    "pairs_lt_2p5A": 0,
                    "pairs_lt_4p5A": 0,
                    "pairs_lt_5p0A": 0,
                }
                other_min = float("inf")
                other_clash2 = other_contact45 = 0
                worst_chain = "NA"
                adjacent_min = float("inf")
                nonadjacent_min = float("inf")
                for i, chain in enumerate(HEX_CHAINS):
                    tags = tag_by_chain[chain]
                    astat = pair_stats_group(tags, groups["adj"][chain], (2.0, 2.5, 4.5))
                    nstat = pair_stats_group(tags, groups["nonadj"][chain], (2.0, 2.5, 4.5))
                    chain_min = min(astat["min_A"], nstat["min_A"])
                    if chain_min < other_min:
                        other_min = chain_min
                        worst_chain = chain
                    adjacent_min = min(adjacent_min, astat["min_A"])
                    nonadjacent_min = min(nonadjacent_min, nstat["min_A"])
                    other_clash2 += astat["pairs_lt_2p0A"] + nstat["pairs_lt_2p0A"]
                    other_contact45 += astat["pairs_lt_4p5A"] + nstat["pairs_lt_4p5A"]
                tag_tag_min = float("inf")
                tag_tag_clash2 = tag_tag_contact45 = 0
                for i, ca in enumerate(HEX_CHAINS):
                    for cb in HEX_CHAINS[i + 1 :]:
                        stat = pair_stats(tag_by_chain[ca], tag_by_chain[cb], (2.0, 2.5, 4.5))
                        tag_tag_min = min(tag_tag_min, stat["min_A"])
                        tag_tag_clash2 += stat["pairs_lt_2p0A"]
                        tag_tag_contact45 += stat["pairs_lt_4p5A"]
                row = {
                    "construct_id": cand.construct_id,
                    "junction": cand.junction,
                    "tag_form": cand.tag_form,
                    "tag_sequence": tag_seq,
                    "tag_length": tag_len,
                    "model_file": model_file,
                    "model_rank": model["rank"],
                    "model_seed": model["seed"],
                    "hexamer_structure": hname,
                    "hexamer_source_path": str(hpath),
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
                    "tag_other_protomer_contacts_4p5A": other_contact45,
                    "worst_tag_chain_for_protomer_contact": worst_chain,
                    "tag_tag_min_A": tag_tag_min,
                    "tag_tag_clashes_lt_2p0A": tag_tag_clash2,
                    "tag_tag_contacts_4p5A": tag_tag_contact45,
                    "tag_overlaps_sequence_defined_9a5_epitope": "yes" if (left in EPITOPE or right in EPITOPE) else "no",
                    "analysis_note": "six_tagged_protomer_proxy_from_existing_tagged_monomer",
                }
                row["hexamer_9a5_class"] = class_from_hex(pd.Series(row))
                rows.append(row)
    return rows


def build_summaries(monomer_rows: list[dict[str, object]], hex_rows: list[dict[str, object]]) -> tuple[list[dict[str, object]], dict[str, dict[str, object]], dict[str, dict[str, object]]]:
    rows = []
    mon_by: dict[str, dict[str, object]] = {}
    hex_by: dict[str, dict[str, object]] = {}
    mon = pd.DataFrame(monomer_rows)
    hx = pd.DataFrame(hex_rows)
    for cid, g in mon.groupby("construct_id"):
        nums = summarize_numbers(list(g["tag_fv_min_A"]))
        classes = list(g["monomer_9a5_class"])
        clash_fraction = float((g["tag_fv_clashes_lt_2p0A"] > 0).mean())
        pose_classes = g.groupby("monomer_pose")["monomer_9a5_class"].agg(lambda x: ";".join(sorted(set(x))))
        pose_sensitivity = "POSE_ROBUST" if len(set(pose_classes)) == 1 and nums["max"] - nums["min"] < 5 else "POSE_SENSITIVE"
        summary = {
            "construct_id": cid,
            "context_layer": "monomer_core_9A5",
            "n_structures": len(g),
            "min_tag_ab_distance_A": nums["min"],
            "median_tag_ab_distance_A": nums["median"],
            "mean_tag_ab_distance_A": nums["mean"],
            "sd_tag_ab_distance_A": nums["sd"],
            "max_tag_ab_distance_A": nums["max"],
            "clash_fraction": clash_fraction,
            "pass_fraction": float((g["monomer_9a5_class"] == "ROBUST_9A5_CONTEXT").mean()),
            "conflict_fraction": float(g["monomer_9a5_class"].isin(["ANTIBODY_STERIC_CONFLICT", "EPITOPE_PERTURBATION_RISK"]).mean()),
            "class_distribution": ";".join(f"{k}:{v}" for k, v in g["monomer_9a5_class"].value_counts().sort_index().items()),
            "ensemble_consistency": consistency_from_classes(classes),
            "pose_sensitivity": pose_sensitivity,
        }
        rows.append(summary)
        mon_by[cid] = summary
    for cid, g in hx.groupby("construct_id"):
        abg = g[g["antibody_present"] == "yes"]
        nums = summarize_numbers(list(abg["tag_ab_min_A"]))
        classes = list(g["hexamer_9a5_class"])
        ab_clash_fraction = float((abg["tag_ab_clashes_lt_2p0A"] > 0).mean()) if len(abg) else math.nan
        prot_clash_fraction = float((g["tag_other_protomer_clashes_lt_2p0A"] > 0).mean())
        tagtag_clash_fraction = float((g["tag_tag_clashes_lt_2p0A"] > 0).mean())
        summary = {
            "construct_id": cid,
            "context_layer": "hexamer_1x9A5_and_free",
            "n_structures": len(g),
            "n_antibody_bound_structures": len(abg),
            "min_tag_ab_distance_A": nums["min"],
            "median_tag_ab_distance_A": nums["median"],
            "mean_tag_ab_distance_A": nums["mean"],
            "sd_tag_ab_distance_A": nums["sd"],
            "max_tag_ab_distance_A": nums["max"],
            "tag_ab_clash_fraction": ab_clash_fraction,
            "tag_protomer_clash_fraction": prot_clash_fraction,
            "tag_tag_clash_fraction": tagtag_clash_fraction,
            "min_tag_other_protomer_A": float(g["tag_other_protomer_min_A"].min()),
            "min_tag_tag_A": float(g["tag_tag_min_A"].min()),
            "pass_fraction": float((g["hexamer_9a5_class"] == "ROBUST_9A5_CONTEXT").mean()),
            "conflict_fraction": float(g["hexamer_9a5_class"].isin(["ANTIBODY_STERIC_CONFLICT", "TAG_TAG_HEXAMER_CONFLICT"]).mean()),
            "class_distribution": ";".join(f"{k}:{v}" for k, v in g["hexamer_9a5_class"].value_counts().sort_index().items()),
            "ensemble_consistency": consistency_from_classes(classes),
            "pose_sensitivity": "not_applicable_hexamer_ensemble",
        }
        rows.append(summary)
        hex_by[cid] = summary
    return rows, mon_by, hex_by


def adjudicate(panel_row: pd.Series, mon: dict[str, object], hx: dict[str, object]) -> tuple[str, str, str]:
    prev = panel_row["priority_class_v5"]
    mon_cons = str(mon.get("ensemble_consistency", "INSUFFICIENT_EVIDENCE"))
    hx_cons = str(hx.get("ensemble_consistency", "INSUFFICIENT_EVIDENCE"))
    severe = (
        "ANTIBODY_STERIC_CONFLICT" in mon_cons
        or "EPITOPE_PERTURBATION_RISK" in mon_cons
        or "ANTIBODY_STERIC_CONFLICT" in hx_cons
    )
    tagtag = "TAG_TAG_HEXAMER_CONFLICT" in hx_cons
    sensitive = "SENSITIVE" in mon_cons or "HEXAMER_CONTEXT_SENSITIVE" in hx_cons or tagtag
    if prev == "Hard_negative_control":
        return "Hard_negative_control", "control_retained", "hard-negative remains a calibration control; 9A5 epitope overlap/conflict is expected"
    if prev == "Conflict_control":
        return "Conflict_control", "control_retained", "kept as conflict control; 9A5 context is recorded but does not promote a control"
    if severe:
        return "Priority_B_9A5_context_caution", "downgraded_by_9A5_context", "direct antibody/epitope conflict in existing 9A5-bound context"
    if sensitive:
        return "Priority_A_with_9A5_context_caution" if prev == "Priority_A" else "Priority_B_with_9A5_context_caution", "retained_with_caution", "no direct antibody clash, but hexamer/tag crowding or pose sensitivity is present"
    return prev, "retained", "no decision-changing 9A5-context conflict detected in existing structures"


def integrate_panel(panel: pd.DataFrame, mon_by: dict[str, dict[str, object]], hex_by: dict[str, dict[str, object]]) -> list[dict[str, object]]:
    rows = []
    for _, r in panel.iterrows():
        mon = mon_by.get(r.construct_id, {})
        hx = hex_by.get(r.construct_id, {})
        new_priority, decision, reason = adjudicate(r, mon, hx)
        rows.append(
            {
                "construct": r.construct_id,
                "junction": r.junction,
                "tag": r.tag_form,
                "previous_priority": r.priority_class_v5,
                "monomer_9a5_class": mon.get("ensemble_consistency", "INSUFFICIENT_EVIDENCE"),
                "monomer_pose_sensitivity": mon.get("pose_sensitivity", "INSUFFICIENT_EVIDENCE"),
                "monomer_min_tag_ab_distance": mon.get("min_tag_ab_distance_A", "NA"),
                "monomer_clash_fraction": mon.get("clash_fraction", "NA"),
                "monomer_epitope_effect": "sequence_defined_epitope_overlap" if r.junction in ["155|156"] else "epitope_interface_retention_audited",
                "hexamer_9a5_class": hx.get("ensemble_consistency", "INSUFFICIENT_EVIDENCE"),
                "hexamer_tag_ab_clash": "yes" if hx.get("tag_ab_clash_fraction", 0) not in ["NA", math.nan] and float(hx.get("tag_ab_clash_fraction", 0) or 0) > 0 else "no",
                "hexamer_tag_protomer_clash": "yes" if float(hx.get("tag_protomer_clash_fraction", 0) or 0) > 0 else "no",
                "hexamer_tag_tag_clash": "yes" if float(hx.get("tag_tag_clash_fraction", 0) or 0) > 0 else "no",
                "hexamer_ensemble_consistency": hx.get("ensemble_consistency", "INSUFFICIENT_EVIDENCE"),
                "existing_structural_class": r.inserted_structure_context,
                "existing_conservation_class": r.conservation_indel_context,
                "existing_homolog_evidence": r.EV_A71_direct_insertion_prior,
                "existing_md_context": r.corrected_MD_status,
                "existing_binder_accessibility": r.binder_accessibility_context,
                "complex_context_decision": decision,
                "new_priority": new_priority,
                "decision_reason": reason,
                "limitations": "rigid_coordinate_transfer_proxy;existing_9A5_structures_only;no_new_MD_or_docking;not_safe_or_validated",
                "safe_or_validated": "no",
            }
        )
    return rows


def plot_outputs(panel_rows: list[dict[str, object]], monomer_rows: list[dict[str, object]], hex_rows: list[dict[str, object]], summaries: list[dict[str, object]]) -> None:
    OUT_FIG.mkdir(parents=True, exist_ok=True)
    plt.rcParams.update(
        {
            "font.family": "sans-serif",
            "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans", "sans-serif"],
            "svg.fonttype": "none",
            "pdf.fonttype": 42,
            "font.size": 7,
            "axes.spines.right": False,
            "axes.spines.top": False,
            "axes.linewidth": 0.8,
        }
    )
    panel = pd.DataFrame(panel_rows)
    mon = pd.DataFrame(monomer_rows)
    hx = pd.DataFrame(hex_rows)
    summary = pd.DataFrame(summaries)
    constructs = list(panel["construct"])
    class_score = {"ROBUST_9A5_CONTEXT": 0, "MONOMER_CONTEXT_SENSITIVE": 1, "HEXAMER_CONTEXT_SENSITIVE": 1, "POSE_SENSITIVE": 1, "TAG_TAG_HEXAMER_CONFLICT": 2, "EPITOPE_PERTURBATION_RISK": 3, "ANTIBODY_STERIC_CONFLICT": 3}
    # 1 heatmap
    heat = []
    for cid in constructs:
        mclasses = mon[mon.construct_id == cid]["monomer_9a5_class"].map(class_score).fillna(2)
        hclasses = hx[hx.construct_id == cid]["hexamer_9a5_class"].map(class_score).fillna(2)
        heat.append([mclasses.mean(), hclasses.mean()])
    fig, ax = plt.subplots(figsize=(5.8, 3.8))
    im = ax.imshow(np.array(heat), aspect="auto", cmap="RdYlBu_r", vmin=0, vmax=3)
    ax.set_yticks(range(len(constructs)), [c.replace("A89_2C_", "") for c in constructs])
    ax.set_xticks([0, 1], ["monomer/core+9A5", "hexamer+9A5"])
    ax.set_title("9A5 context risk by construct")
    fig.colorbar(im, ax=ax, label="context risk class score")
    save_fig(fig, OUT_FIG / "figure01_candidate_state_heatmap")
    # 2 monomer vs hexamer paired
    fig, ax = plt.subplots(figsize=(5.2, 3.8))
    xs = []
    ys = []
    labs = []
    for cid in constructs:
        xs.append(float(mon[mon.construct_id == cid]["tag_fv_min_A"].median()))
        ys.append(float(hx[(hx.construct_id == cid) & (hx.antibody_present == "yes")]["tag_ab_min_A"].median()))
        labs.append(cid.replace("A89_2C_", ""))
    ax.scatter(xs, ys, s=24, color="#3B82F6")
    for x, y, lab in zip(xs, ys, labs):
        ax.text(x, y, lab, fontsize=5)
    ax.axvline(2.5, color="#DC2626", lw=0.8, ls="--")
    ax.axhline(2.5, color="#DC2626", lw=0.8, ls="--")
    ax.set_xlabel("monomer/core tag-Fv median min distance (A)")
    ax.set_ylabel("hexamer tag-9A5 median min distance (A)")
    ax.set_title("Monomer and hexamer antibody-context distances")
    save_fig(fig, OUT_FIG / "figure02_monomer_vs_hexamer_paired")
    # 3 distance/clash comparison
    g = hx[hx.antibody_present == "yes"].groupby("construct_id").agg(min_ab=("tag_ab_min_A", "min"), clashes=("tag_ab_clashes_lt_2p0A", "sum")).reindex(constructs)
    fig, ax1 = plt.subplots(figsize=(6.0, 3.4))
    x = np.arange(len(constructs))
    ax1.bar(x, g["min_ab"], color="#93C5FD", label="min distance")
    ax1.set_ylabel("min tag-9A5 distance (A)")
    ax1.set_xticks(x, [c.replace("A89_2C_", "") for c in constructs], rotation=60, ha="right", fontsize=5)
    ax2 = ax1.twinx()
    ax2.plot(x, g["clashes"], color="#B91C1C", marker="o", lw=1, label="<2A clashes")
    ax2.set_ylabel("tag-9A5 hard clashes")
    ax1.set_title("Tag-9A5 distance and hard-clash audit")
    save_fig(fig, OUT_FIG / "figure03_tag_9a5_clash_distance")
    # 4 ensemble reproducibility
    fig, ax = plt.subplots(figsize=(6.0, 3.4))
    s = summary[summary.context_layer == "hexamer_1x9A5_and_free"].set_index("construct_id").reindex(constructs)
    ax.bar(x - 0.18, s["pass_fraction"], width=0.35, color="#16A34A", label="pass fraction")
    ax.bar(x + 0.18, s["conflict_fraction"], width=0.35, color="#F97316", label="conflict fraction")
    ax.set_ylim(0, 1)
    ax.set_ylabel("fraction of ensemble structures")
    ax.set_xticks(x, [c.replace("A89_2C_", "") for c in constructs], rotation=60, ha="right", fontsize=5)
    ax.legend()
    ax.set_title("Hexamer-context ensemble reproducibility")
    save_fig(fig, OUT_FIG / "figure04_ensemble_reproducibility")
    # 5 old -> new priority
    pri = panel[["construct", "previous_priority", "new_priority"]]
    y = np.arange(len(pri))
    fig, ax = plt.subplots(figsize=(6.0, 3.6))
    ax.scatter([0] * len(pri), y, color="#64748B", s=24)
    ax.scatter([1] * len(pri), y, color="#2563EB", s=24)
    for i, row in pri.iterrows():
        ax.plot([0, 1], [i, i], color="#CBD5E1", lw=1)
        ax.text(-0.03, i, row.previous_priority, ha="right", va="center", fontsize=5)
        ax.text(1.03, i, row.new_priority, ha="left", va="center", fontsize=5)
    ax.set_yticks(y, [c.replace("A89_2C_", "") for c in pri["construct"]], fontsize=5)
    ax.set_xticks([0, 1], ["V5", "V6 9A5 context"])
    ax.set_xlim(-0.6, 1.8)
    ax.set_title("Priority state before and after 9A5-context layer")
    save_fig(fig, OUT_FIG / "figure05_priority_transition")
    # 6 representative structure projections from actual coordinates
    make_representative_structure_projection(panel, mon, hx)


def save_fig(fig, stem: Path) -> None:
    fig.tight_layout()
    fig.savefig(stem.with_suffix(".svg"), bbox_inches="tight")
    fig.savefig(stem.with_suffix(".pdf"), bbox_inches="tight")
    fig.savefig(stem.with_suffix(".png"), dpi=300, bbox_inches="tight")
    plt.close(fig)


def write_slim_proxy(cid: str, model_file: str, hex_path: Path, left: int, right: int, tag_len: int) -> Path:
    OUT_PROXY.mkdir(parents=True, exist_ok=True)
    model_atoms = parse_pdb(ROOT / model_file)
    hex_atoms = parse_pdb(hex_path)
    proxy_atoms = [a for a in hex_atoms if a.name == "CA"]
    serial = len(proxy_atoms) + 1
    for chain in HEX_CHAINS:
        tag_atoms, _, _, _ = align_tagged_to_target(model_atoms, hex_atoms, chain, left, right, tag_len, range(1, 322))
        for a in tag_atoms:
            if not is_heavy(a):
                continue
            proxy_atoms.append(replace(a, serial=serial, resid=900 + a.resid - left))
            serial += 1
    out = OUT_PROXY / f"{cid}_6x_tagged_1x9A5_CA_slim_proxy.pdb"
    with out.open("w") as fh:
        fh.write("REMARK Task011 slim proxy: original hexamer+9A5 CA atoms plus transformed tag heavy atoms only\n")
        fh.write(f"REMARK construct={cid}; model_file={model_file}; source_hexamer={hex_path}\n")
        for i, a in enumerate(proxy_atoms, start=1):
            fh.write(
                f"ATOM  {i:5d} {a.name[:4]:>4s} {a.resname:>3s} {a.chain:1s}{a.resid:4d}    "
                f"{a.x:8.3f}{a.y:8.3f}{a.z:8.3f}{a.occ:6.2f}{a.bfac:6.2f}          {a.elem:>2s}\n"
            )
        fh.write("END\n")
    return out


def make_representative_structure_projection(panel: pd.DataFrame, mon: pd.DataFrame, hx: pd.DataFrame) -> None:
    candidates = list(panel["construct"])
    retained = panel[panel["new_priority"].str.contains("Priority_A", na=False)]["construct"].tolist()
    severe = panel[panel["complex_context_decision"].str.contains("downgraded", na=False)]["construct"].tolist()
    hard = panel[panel["new_priority"].eq("Hard_negative_control")]["construct"].tolist()
    chosen = []
    if retained:
        chosen.append(retained[0])
    chosen.append(severe[0] if severe else candidates[-2])
    if hard:
        chosen.append(hard[0])
    chosen = list(dict.fromkeys(chosen))[:3]
    hex_path = SOURCE_SUMMARY / "SHOWCASE_1x_9A5_D_chain_after_npt_100ps_pbc_fixed.pdb"
    hex_atoms = parse_pdb(hex_path)
    fig, axes = plt.subplots(1, len(chosen), figsize=(2.4 * len(chosen), 2.5))
    if len(chosen) == 1:
        axes = [axes]
    proxy_paths = []
    for ax, cid in zip(axes, chosen):
        row = panel[panel.construct == cid].iloc[0]
        model_file = hx[hx.construct_id == cid]["model_file"].iloc[0]
        left, right = map(int, row.junction.split("|"))
        tag_len = int(hx[hx.construct_id == cid]["tag_length"].iloc[0])
        proxy = write_slim_proxy(cid, model_file, hex_path, left, right, tag_len)
        proxy_paths.append(proxy.relative_to(ROOT).as_posix())
        model_atoms = parse_pdb(ROOT / model_file)
        all_tag = []
        for chain in HEX_CHAINS:
            tags, _, _, _ = align_tagged_to_target(model_atoms, hex_atoms, chain, left, right, tag_len, range(1, 322))
            all_tag += [a for a in tags if is_heavy(a)]
        ca2c = coords([a for a in hex_atoms if a.chain in set(HEX_CHAINS) and a.name == "CA"])
        caab = coords([a for a in hex_atoms if a.chain in {"H", "L"} and a.name == "CA"])
        ctag = coords(all_tag)
        ax.scatter(ca2c[:, 0], ca2c[:, 1], s=1, color="#CBD5E1", rasterized=True)
        ax.scatter(caab[:, 0], caab[:, 1], s=4, color="#2563EB")
        ax.scatter(ctag[:, 0], ctag[:, 1], s=7, color="#DC2626")
        ax.set_aspect("equal", adjustable="box")
        ax.set_title(cid.replace("A89_2C_", ""), fontsize=6)
        ax.set_xticks([])
        ax.set_yticks([])
    fig.suptitle("Representative 1x9A5 hexamer projections; slim proxy PDBs written", fontsize=8)
    save_fig(fig, OUT_FIG / "figure06_representative_structure_projections")
    (OUT_PROXY / "proxy_structure_index.tsv").write_text("proxy_pdb\n" + "\n".join(proxy_paths) + "\n")


def write_reports(panel_rows: list[dict[str, object]], monomer_rows: list[dict[str, object]], hex_rows: list[dict[str, object]], summaries: list[dict[str, object]], inventory: list[dict[str, object]], provenance: list[dict[str, object]]) -> None:
    panel = pd.DataFrame(panel_rows)
    mon = pd.DataFrame(monomer_rows)
    hx = pd.DataFrame(hex_rows)
    summary = pd.DataFrame(summaries)
    inv = pd.DataFrame(inventory)
    n_candidates = len(panel)
    retained_a = panel[panel["new_priority"].str.contains("Priority_A", na=False)]["construct"].tolist()
    downgraded = panel[panel["complex_context_decision"].str.contains("downgraded", na=False)]["construct"].tolist()
    robust_b = panel[
        (panel["previous_priority"] == "Priority_B")
        & panel["monomer_9a5_class"].str.contains("ROBUST", na=False)
        & panel["hexamer_9a5_class"].str.contains("ROBUST", na=False)
    ]["construct"].tolist()
    cautioned_a = panel[(panel["previous_priority"] == "Priority_A") & panel["new_priority"].str.contains("caution", na=False)]["construct"].tolist()
    b_cleaner_note = (
        f"`{'; '.join(robust_b)}` are cleaner than cautioned Priority A rows in the 9A5-context layer alone, but are not automatically promoted because the project priority hierarchy also includes direct homolog phenotype, functional constraints, diversity logic and prior structure/MD evidence."
        if robust_b and cautioned_a
        else "`none_detected_by_current_proxy`."
    )
    exec_conclusion = (
        "The existing 9A5-bound context does not create a decision-changing direct antibody clash for the current 289|290 and 248|249 Priority A candidate logic; "
        "the 155|156 hard-negative control is correctly recognized as epitope/antibody-confounded."
        if not downgraded
        else "The existing 9A5-bound context introduces a decision-changing caution for one or more previously prioritized candidates."
    )
    common_methods = (
        "Methods: existing C01/C04 9A5-core complexes and 1x9A5 full-length hexamer endpoints were reused; tagged ColabFold monomers were aligned by native 2C residues with explicit tag-residue exclusion; all metrics are heavy-atom geometric proxies. "
        "No new docking, AlphaFold, Slurm, GPU job, or MD was run."
    )
    top_table = panel[["construct", "previous_priority", "monomer_9a5_class", "hexamer_9a5_class", "hexamer_ensemble_consistency", "new_priority", "complex_context_decision"]].to_markdown(index=False)
    (OUT_DOCS / "9A5_MONOMER_CONTEXT_V1.md").write_text(
        "\n".join(
            [
                "# 9A5_MONOMER_CONTEXT_V1",
                "",
                "Status: `TASK011_COMPLETE_MONOMER_LAYER`",
                "",
                common_methods,
                "",
                "The monomer layer used historical 9A5-bound 2C core complexes only. Full-length monomer+9A5 structures were not found, so C-terminal tag results are core-alignment transfer proxies with explicit limitations.",
                "",
                "Formal 9A5 epitope: A89 2C aa148-160. CDR definitions reused from the HRV_Oligomers 1x9A5 analysis scripts.",
                "",
                "## Monomer/Core Summary",
                "",
                summary[summary.context_layer == "monomer_core_9A5"].to_markdown(index=False),
                "",
                "## Key Interpretation",
                "",
                "- `155|156 x MAP8` overlaps the sequence-defined 9A5 epitope and is treated as expected epitope-perturbation risk.",
                "- Current 289|290 constructs are outside the C01/C04 core, so their monomer/core 9A5 distances are transfer-based and less informative than the full-length hexamer layer.",
                "- No monomer-layer result is a viral-fitness or antibody-binding validation claim.",
            ]
        )
        + "\n"
    )
    (OUT_DOCS / "9A5_HEXAMER_CONTEXT_V1.md").write_text(
        "\n".join(
            [
                "# 9A5_HEXAMER_CONTEXT_V1",
                "",
                "Status: `TASK011_COMPLETE_HEXAMER_LAYER`",
                "",
                common_methods,
                "",
                "The hexamer layer used the current 1x9A5 full-length hexamer and three independent 1 ns 1x9A5 refinement endpoints, plus free-hexamer lead/control endpoints for tag-protomer and tag-tag context.",
                "",
                "## Hexamer Summary",
                "",
                summary[summary.context_layer == "hexamer_1x9A5_and_free"].to_markdown(index=False),
                "",
                "## Key Interpretation",
                "",
                "- Antibody-bound and free hexamer metrics are reported separately in the raw TSV and summarized as an ensemble layer.",
                "- Rigid six-tagged-protomer proxy clashes are interpreted as screening cautions, not final structural rejection.",
                "- 2x9A5 structures are inventoried only as stress-test/audit-only provenance and are not used as primary candidate ranking evidence.",
            ]
        )
        + "\n"
    )
    (OUT_DOCS / "9A5_COMPLEX_CONTEXT_INTEGRATION_V1.md").write_text(
        "\n".join(
            [
                "# 9A5_COMPLEX_CONTEXT_INTEGRATION_V1",
                "",
                "## Executive conclusion",
                "",
                exec_conclusion,
                "",
                "Final state: `READY_FOR_EXPERIMENTAL_REVIEW_WITH_9A5_CONTEXT_LAYER`",
                "",
                common_methods,
                "",
                "No construct is safe, compatible, experimentally validated or fitness-neutral.",
                "",
                "## Candidate Decision Table",
                "",
                top_table,
                "",
                "## Direct Answers",
                "",
                f"- Candidate rows assessed: `{n_candidates}` current V5 Priority A/B/control/hard-negative constructs.",
                f"- Priority A retained or retained with 9A5-context caution: `{'; '.join(retained_a) if retained_a else 'none'}`.",
                f"- Candidates downgraded by 9A5 context: `{'; '.join(downgraded) if downgraded else 'none'}`.",
                f"- Priority B rows with cleaner 9A5-context metrics than at least one cautioned Priority A row: {b_cleaner_note}",
                "- If ordering experimental discussion now, keep the 010A 4+2 design logic: 289|290 x MAP8, 289|290 x G196_minimal, 248|249 x HA, 248|249 x MAP8, with 224|225 x MAP8 and 155|156 x MAP8 as controls. The 9A5 layer adds caution/confirmation context rather than a new safe-site claim.",
                "",
                "## Existing Data Reused",
                "",
                "- C01/C04 historical 9A5-core complexes from HRV_Oligomers.",
                "- Current full-length 1x9A5 hexamer showcase plus three 1 ns refined endpoints.",
                "- Free hexamer lead/control and 5 ns repeat endpoints.",
                "- Existing Open Structure 007 tagged monomer predictions.",
                "- Existing V5 candidate panel, direct homolog evidence, conservation, PLM, binder-accessibility and MD context fields.",
                "",
                "## Inventory Snapshot",
                "",
                f"- Inventory rows: `{len(inv)}` structures/models.",
                f"- Primary usable 1x9A5 hexamer structures: `{len(inv[(inv.structure_class == '1x9A5_hexamer_complex') & (inv.usable_for_primary_analysis == 'yes')])}`.",
                f"- Tagged monomer model structures inventoried: `{len(inv[inv.structure_class == 'tagged_monomer'])}`.",
                "",
                "## Figures",
                "",
                "- `figures/9a5_context_011/figure01_candidate_state_heatmap.svg`",
                "- `figures/9a5_context_011/figure02_monomer_vs_hexamer_paired.svg`",
                "- `figures/9a5_context_011/figure03_tag_9a5_clash_distance.svg`",
                "- `figures/9a5_context_011/figure04_ensemble_reproducibility.svg`",
                "- `figures/9a5_context_011/figure05_priority_transition.svg`",
                "- `figures/9a5_context_011/figure06_representative_structure_projections.svg`",
                "",
                "## Limitations",
                "",
                "- Structural proxy only; no viral fitness, antibody-detection or replication compatibility is proven.",
                "- C01/C04 monomer/core complexes contain 2C residues 112-258, not full-length 2C.",
                "- C-terminal 289|290 monomer-layer geometry depends on core-based transfer and is less direct than full-length hexamer context.",
                "- Six-tagged homohexamer context is a rigid transfer proxy, not a relaxed tagged homohexamer prediction.",
                "- No membrane, RNA, ATP/Mg mechanistic MD, binder docking, nucleotide/codon design or wet-lab protocol was performed.",
                "",
                "No additional generic long MD is required for the current tag-prioritization decision.",
            ]
        )
        + "\n"
    )
    (OUT_DOCS / "9A5_CONTEXT_011_RUN_LOG.md").write_text(
        "\n".join(
            [
                "# 9A5_CONTEXT_011_RUN_LOG",
                "",
                "Task: `9A5_MONOMER_HEXAMER_CONTEXT_011`",
                "",
                "Branch: `analysis/9a5-monomer-hexamer-context-011`",
                "",
                f"Starting target commit: `{run_git(ROOT, ['rev-parse', 'HEAD'])}`",
                f"Source HRV_Oligomers commit: `{run_git(SOURCE, ['rev-parse', 'HEAD'])}`",
                "",
                "## Required Context Read",
                "",
                "- WORKFLOW.md, AGENTS.md, PROJECT_STATE.md, DECISIONS.md, ANALYSIS_INDEX.md, ACTIVE_TASK.md, INPUT_PROVENANCE.md, TODO.md.",
                "- Task 010A parent task/report files and corrected-validation reports.",
                "- User-authorized Task 011 prompt copied to `tasks/9A5_MONOMER_HEXAMER_CONTEXT_011.md`.",
                "",
                "## Execution Environment",
                "",
                f"- Python executable: `{sys.executable}`",
                f"- Python version: `{sys.version.split()[0]}`",
                f"- pandas `{pd.__version__}`; numpy `{np.__version__}`; scipy `{scipy.__version__}`; matplotlib `{matplotlib.__version__}`",
                f"- mdtraj import available: `{'yes' if md is not None else 'no'}`",
                "- Distance searches used `scipy.spatial.cKDTree`.",
                "",
                "## Search And Reuse Record",
                "",
                "- Searched HRV_Oligomers for 9A5, C01, C04, complex, monomer, Fv/scFv, hexamer, selected, SHOWCASE, endpoint, registry and report assets.",
                "- Searched target repo for 9A5, tagged, monomer, hexamer, candidate, shortlist, structure, provenance, open-structure, binder, PLM, EV71, conservation and dynamics assets.",
                "- Reused existing structures and candidate tables; no new docking, AF/ColabFold, GPU, Slurm or MD job was started.",
                "- Historical untracked Task 009 local multimer outputs were left untouched and not staged.",
                "",
                "## Generated Outputs",
                "",
                "- `data/9a5_context_structure_inventory_v1.tsv`",
                "- `data/9a5_context_input_provenance_v1.tsv`",
                "- `data/9a5_monomer_tag_compatibility_v1.tsv`",
                "- `data/9a5_hexamer_tag_compatibility_v1.tsv`",
                "- `data/9a5_context_ensemble_summary_v1.tsv`",
                "- `data/final_candidate_panel_v6_9a5_context.tsv`",
                "- `docs/9A5_MONOMER_CONTEXT_V1.md`",
                "- `docs/9A5_HEXAMER_CONTEXT_V1.md`",
                "- `docs/9A5_COMPLEX_CONTEXT_INTEGRATION_V1.md`",
                "- `figures/9a5_context_011/figure01-06.*`",
                "",
                "## Result State",
                "",
                "`READY_FOR_EXPERIMENTAL_REVIEW_WITH_9A5_CONTEXT_LAYER`",
            ]
        )
        + "\n"
    )


def set_last_updated(text: str) -> str:
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if line.startswith("Last updated:"):
            lines[i] = f"Last updated: {TODAY}"
            return "\n".join(lines) + ("\n" if text.endswith("\n") else "")
    return text


def remove_markdown_section(text: str, heading: str) -> str:
    needle = f"\n{heading}"
    while True:
        start = text.find(needle)
        lead = 1
        if start == -1 and text.startswith(heading):
            start = 0
            lead = 0
        if start == -1:
            return text
        section_start = start + lead
        next_section = text.find("\n## ", section_start + len(heading))
        if next_section == -1:
            text = text[:start].rstrip() + "\n"
        else:
            text = text[:start].rstrip() + "\n\n" + text[next_section + 1 :].lstrip()


def remove_task011_index_rows(text: str) -> str:
    drop_prefixes = (
        "| Task 011 specification |",
        "| Task 011 integration report |",
        "| Task 011 monomer report |",
        "| Task 011 hexamer report |",
        "| Final candidate panel V6 |",
        "| 9A5 structure inventory |",
    )
    return "\n".join(
        line for line in text.splitlines() if not line.startswith(drop_prefixes)
    ) + "\n"


def update_project_files(final_panel: list[dict[str, object]]) -> None:
    final_state = "READY_FOR_EXPERIMENTAL_REVIEW_WITH_9A5_CONTEXT_LAYER"
    active = f"""# Active Task

Current task: `9A5_MONOMER_HEXAMER_CONTEXT_011` — **COMPLETED / WAITING FOR CHATGPT REVIEW**

Branch: `analysis/9a5-monomer-hexamer-context-011`

Primary specification:

- `tasks/9A5_MONOMER_HEXAMER_CONTEXT_011.md`

Primary outputs:

- `data/final_candidate_panel_v6_9a5_context.tsv`
- `docs/9A5_COMPLEX_CONTEXT_INTEGRATION_V1.md`
- `docs/9A5_MONOMER_CONTEXT_V1.md`
- `docs/9A5_HEXAMER_CONTEXT_V1.md`

Completion state:

`{final_state}`

No construct is safe, compatible, experimentally validated or fitness-neutral. Exact HRV-A89 nucleotide/replicon/plasmid context remains required before nucleotide/codon/RNA-level construct design.
"""
    (ROOT / "ACTIVE_TASK.md").write_text(active)
    # Keep edits minimal: prepend current-state blocks and leave history below.
    ps = set_last_updated((ROOT / "PROJECT_STATE.md").read_text())
    ps = remove_markdown_section(ps, "## Current Task 011 State")
    insert = f"""
## Current Task 011 State

Task 011 has achieved:

`{final_state}`

Branch:

`analysis/9a5-monomer-hexamer-context-011`

Task:

`9A5_MONOMER_HEXAMER_CONTEXT_011`

Authoritative files:

- `tasks/9A5_MONOMER_HEXAMER_CONTEXT_011.md`
- `data/final_candidate_panel_v6_9a5_context.tsv`
- `data/9a5_context_structure_inventory_v1.tsv`
- `data/9a5_context_input_provenance_v1.tsv`
- `data/9a5_monomer_tag_compatibility_v1.tsv`
- `data/9a5_hexamer_tag_compatibility_v1.tsv`
- `data/9a5_context_ensemble_summary_v1.tsv`
- `docs/9A5_COMPLEX_CONTEXT_INTEGRATION_V1.md`
- `docs/9A5_MONOMER_CONTEXT_V1.md`
- `docs/9A5_HEXAMER_CONTEXT_V1.md`

Task 011 reused existing C01/C04 9A5-core complexes, the current full-length 1x9A5 2C hexamer ensemble, free-hexamer endpoints and existing tagged monomer models. It did not run new docking, AF/ColabFold, Slurm/GPU work or MD.

The 9A5 context layer does not validate any construct. It is a structural-proxy evidence layer for experimental-review discussion.
"""
    ps = ps.replace("## Current Project-Level State", insert + "\n## Current Project-Level State", 1)
    ps = ps.replace("Task 010A has achieved:\n\n`EXPERIMENTAL_REVIEW_SHORTLIST_READY_FOR_DISCUSSION`", f"Task 011 has achieved:\n\n`{final_state}`", 1)
    ps = ps.replace("`analysis/experimental-review-cleanup-010a`", "`analysis/9a5-monomer-hexamer-context-011`", 1)
    ps = ps.replace("`FINAL_SCIENTIFIC_CLEANUP_AND_EXPERIMENTAL_SHORTLIST_010A`", "`9A5_MONOMER_HEXAMER_CONTEXT_011`", 1)
    (ROOT / "PROJECT_STATE.md").write_text(ps)
    idx = set_last_updated((ROOT / "ANALYSIS_INDEX.md").read_text())
    idx = remove_task011_index_rows(idx)
    idx = remove_markdown_section(idx, "## Task 011 Completion")
    idx_insert = """| Task 011 specification | `tasks/9A5_MONOMER_HEXAMER_CONTEXT_011.md` | CURRENT COMPLETE | authorized 9A5-bound context task |
| Task 011 integration report | `docs/9A5_COMPLEX_CONTEXT_INTEGRATION_V1.md` | CURRENT | final 9A5 monomer+hexamer context integration |
| Task 011 monomer report | `docs/9A5_MONOMER_CONTEXT_V1.md` | CURRENT | 9A5-bound monomer/core transfer layer |
| Task 011 hexamer report | `docs/9A5_HEXAMER_CONTEXT_V1.md` | CURRENT | 1x9A5 full-length hexamer and free-hexamer context layer |
| Final candidate panel V6 | `data/final_candidate_panel_v6_9a5_context.tsv` | CURRENT | V5 plus 9A5-bound complex context layer |
| 9A5 structure inventory | `data/9a5_context_structure_inventory_v1.tsv` | CURRENT PROVENANCE | source/target structure QC and checksums |
"""
    idx = idx.replace("| Task 010A specification |", idx_insert + "| Task 010A specification |", 1)
    idx += "\n## Task 011 Completion\n\n`READY_FOR_EXPERIMENTAL_REVIEW_WITH_9A5_CONTEXT_LAYER`\n\nTask 011 adds a 9A5-bound monomer/core and full-length hexamer structural-context layer to the current V5 experimental-review panel. It does not authorize or perform nucleotide design, wet-lab protocols, new MD, or safety/validation claims.\n"
    (ROOT / "ANALYSIS_INDEX.md").write_text(idx)
    dec = set_last_updated((ROOT / "DECISIONS.md").read_text())
    dec = remove_markdown_section(dec, "## D-046 — 9A5-bound complex context is an added structural-proxy layer")
    dec += """

## D-046 — 9A5-bound complex context is an added structural-proxy layer

**Decision:** Treat `data/final_candidate_panel_v6_9a5_context.tsv`, `docs/9A5_COMPLEX_CONTEXT_INTEGRATION_V1.md`, `docs/9A5_MONOMER_CONTEXT_V1.md` and `docs/9A5_HEXAMER_CONTEXT_V1.md` as the current 9A5-context review package.

**Reason:** Task 011 reused existing C01/C04 9A5-core complexes, the current 1x9A5 full-length hexamer ensemble, free-hexamer endpoints and existing tagged monomer models to audit whether antibody-bound monomer/hexamer context changes the experimental-review candidate logic.

**Boundary:** This is a structural proxy layer, not direct HRV-A89 insertion phenotype, antibody-detection validation, viral-fitness evidence, nucleotide/codon design or wet-lab protocol. No construct is safe, compatible or experimentally validated.
"""
    (ROOT / "DECISIONS.md").write_text(dec)
    todo = f"""# TODO

Last updated: {TODAY}

## Current Gate — Task 011 9A5 Context Integration

Status: `{final_state}`

Branch:

`analysis/9a5-monomer-hexamer-context-011`

Current authoritative output:

- `data/final_candidate_panel_v6_9a5_context.tsv`
- `docs/9A5_COMPLEX_CONTEXT_INTEGRATION_V1.md`
- `docs/9A5_MONOMER_CONTEXT_V1.md`
- `docs/9A5_HEXAMER_CONTEXT_V1.md`

## Completed In Task 011

- inventoried HRV_Oligomers and target-repo 9A5/free-hexamer/tagged-monomer assets;
- verified chain/residue ranges and checksums for primary structures;
- reused C01/C04 core 9A5 complexes and full-length 1x9A5 hexamer endpoints;
- generated monomer/core transfer compatibility metrics;
- generated six-tagged-protomer plus 1x9A5 hexamer proxy metrics;
- integrated V5 candidate/control evidence into V6 with 9A5-context fields;
- generated six data-driven figures and slim representative proxy PDBs.

## Next Scientific Review

ChatGPT/user should review whether the V6 9A5-context caution labels change the experimental discussion order, while preserving the evidence hierarchy.

No additional generic long MD is required for the current tag-prioritization decision.

## Still Not Authorized

- exact nucleotide/RNA/codon construct design;
- wet-lab procedural protocol design;
- membrane/RNA/ATP/antibody mechanistic MD;
- new Slurm/GPU/MD jobs by default;
- safety, compatibility or validation claims;
- merge to `main`.
"""
    (ROOT / "TODO.md").write_text(todo)
    readme = remove_markdown_section((ROOT / "README.md").read_text(), "## Current 9A5 Context Layer")
    readme += """

## Current 9A5 Context Layer

Task `9A5_MONOMER_HEXAMER_CONTEXT_011` adds a 9A5-bound monomer/core and full-length hexamer structural-proxy layer to the experimental-review panel.

Current files:

- `data/final_candidate_panel_v6_9a5_context.tsv`
- `docs/9A5_COMPLEX_CONTEXT_INTEGRATION_V1.md`
- `docs/9A5_MONOMER_CONTEXT_V1.md`
- `docs/9A5_HEXAMER_CONTEXT_V1.md`

No construct is computationally safe, compatible or experimentally validated.
"""
    (ROOT / "README.md").write_text(readme)
    # Append concise provenance registry entry.
    reg_path = ROOT / "references" / "LITERATURE_EVIDENCE_REGISTRY.md"
    reg = set_last_updated(reg_path.read_text())
    reg = remove_markdown_section(reg, "## Project 9A5-bound Structural-Proxy Evidence")
    reg += """

## Project 9A5-bound Structural-Proxy Evidence

| Source | Class | What it supports here | Boundary |
|---|---|---|---|
| HRV_Oligomers source repo commit `3385e069fa8469253d8776b3adb3361759094faa`; C01/C04 9A5-core complexes and 1x9A5 full-length hexamer endpoints inventoried in `data/9a5_context_structure_inventory_v1.tsv` | D / project structural model | Task 011 9A5-bound monomer/core and hexamer context proxies for current tag-insertion candidates | not experimental HRV-A89 insertion tolerance, not antibody-detection validation, not a safe-site claim |
"""
    (ROOT / "references" / "LITERATURE_EVIDENCE_REGISTRY.md").write_text(reg)


def main() -> None:
    for path in [OUT_DATA, OUT_RESULTS, OUT_DOCS, OUT_FIG, OUT_PROXY]:
        path.mkdir(parents=True, exist_ok=True)
    panel = pd.read_csv(V5_PANEL, sep="\t")
    panel = panel[panel["priority_class_v5"].isin(["Priority_A", "Priority_B", "Conflict_control", "Hard_negative_control"])].copy()
    models = candidate_models(panel)
    missing = sorted(set(panel["construct_id"]) - set(models["construct_id"]))
    if missing:
        raise SystemExit(f"Missing tagged model(s) for current panel constructs: {missing}")
    inventory, provenance = make_inventory(models)
    write_tsv(OUT_DATA / "9a5_context_structure_inventory_v1.tsv", inventory)
    write_tsv(OUT_DATA / "9a5_context_input_provenance_v1.tsv", provenance)
    monomer_rows = analyze_monomer(panel, models)
    write_tsv(OUT_DATA / "9a5_monomer_tag_compatibility_v1.tsv", monomer_rows)
    hex_rows = analyze_hexamer(panel, models)
    write_tsv(OUT_DATA / "9a5_hexamer_tag_compatibility_v1.tsv", hex_rows)
    summaries, mon_by, hex_by = build_summaries(monomer_rows, hex_rows)
    write_tsv(OUT_DATA / "9a5_context_ensemble_summary_v1.tsv", summaries)
    final_panel = integrate_panel(panel, mon_by, hex_by)
    write_tsv(OUT_DATA / "final_candidate_panel_v6_9a5_context.tsv", final_panel)
    plot_outputs(final_panel, monomer_rows, hex_rows, summaries)
    write_reports(final_panel, monomer_rows, hex_rows, summaries, inventory, provenance)
    update_project_files(final_panel)
    print("TASK011_COMPLETE")
    print(f"panel_rows={len(final_panel)}")
    print(f"monomer_rows={len(monomer_rows)}")
    print(f"hexamer_rows={len(hex_rows)}")


if __name__ == "__main__":
    main()
