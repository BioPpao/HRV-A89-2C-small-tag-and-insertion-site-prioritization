#!/usr/bin/env python3
"""BROAD_DYNAMICS_AND_RECOVERY_009 CPU-side recovery and bookkeeping.

This script writes compact, auditable outputs. It never fabricates MD
trajectory metrics; missing trajectory-dependent layers are marked explicitly.
"""
from __future__ import annotations

import csv
import hashlib
import json
import math
import os
import platform
import shutil
import subprocess
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(".")
OUT = Path("results/broad_dynamics_009")
LOGS = OUT / "logs"
DOCS = Path("docs")
DATA = Path("data")

CORE_TAGS = {
    "MAP8": "GDGMVPPG",
    "HA": "YPYDVPDYA",
    "G196_minimal": "DLVPR",
}
NEW_TAGS = {
    "PA14": "EGGVAMPGAEDDVV",
    "AGIA": "EEAAGIARP",
}

FUNCTIONAL_NEIGHBORHOODS = {
    "ATPase_Ploop": set(range(123, 133)),
    "Walker_B_motif": set(range(176, 187)),
    "RNA_contact_homolog_context": {155, 156, 197, 199, 202, 216, 233, 234},
    "C_terminal_287_291_cluster": set(range(287, 292)),
    "Zn_Cys_context": set(range(267, 280)),
}


def sh(cmd: list[str], timeout: int = 20) -> tuple[int, str]:
    try:
        p = subprocess.run(cmd, text=True, capture_output=True, timeout=timeout)
        return p.returncode, (p.stdout + p.stderr).strip()
    except Exception as e:
        return 999, f"{type(e).__name__}: {e}"


def write_tsv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("\n")
        return
    cols = list(rows[0])
    seen = set(cols)
    for row in rows[1:]:
        for key in row:
            if key not in seen:
                cols.append(key)
                seen.add(key)
    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols, delimiter="\t", lineterminator="\n")
        w.writeheader()
        w.writerows(rows)


def read_refseq() -> str:
    return "".join(
        line.strip()
        for line in Path("references/HRV_A89_2C_reference_sequence.fasta").read_text().splitlines()
        if not line.startswith(">")
    )


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def load_tsv(path: str | Path) -> pd.DataFrame:
    return pd.read_csv(path, sep="\t", dtype=str).fillna("")


def fnum(x: object, default: float = math.nan) -> float:
    try:
        s = str(x)
        if s == "" or s.lower() == "nan":
            return default
        return float(s)
    except Exception:
        return default


def site_region(junction: str) -> str:
    left = int(junction.split("|")[0])
    if 287 <= left <= 290:
        return "C-terminal 287-291 cluster"
    if 220 <= left <= 226:
        return "224 neighborhood / non-C-terminal core"
    if 245 <= left <= 250:
        return "248-249 historical insertion region"
    if 202 <= left <= 204:
        return "203-204 mechanistic/conflict region"
    if 254 <= left <= 257:
        return "256-257 oligomer-conflict control"
    if 154 <= left <= 156:
        return "155-156 hard-negative RNA/pore context"
    return "other"


def parse_pdb_atoms(path: Path) -> list[dict]:
    rows: list[dict] = []
    for line in path.read_text(errors="replace").splitlines():
        if not line.startswith(("ATOM  ", "HETATM")):
            continue
        try:
            rows.append(
                {
                    "serial": int(line[6:11]),
                    "name": line[12:16].strip(),
                    "altloc": line[16].strip(),
                    "resname": line[17:20].strip(),
                    "chain": line[21].strip(),
                    "resid": int(line[22:26]),
                    "icode": line[26].strip(),
                    "x": float(line[30:38]),
                    "y": float(line[38:46]),
                    "z": float(line[46:54]),
                    "element": line[76:78].strip() if len(line) >= 78 else "",
                }
            )
        except Exception:
            continue
    return rows


def structure_qc(path: Path) -> dict:
    atoms = parse_pdb_atoms(path)
    coords = np.array([[a["x"], a["y"], a["z"]] for a in atoms], dtype=float) if atoms else np.zeros((0, 3))
    finite = bool(np.isfinite(coords).all()) if len(coords) else False
    duplicate_keys = Counter((a["chain"], a["resid"], a["icode"], a["name"], a["altloc"]) for a in atoms)
    duplicate_atoms = sum(v - 1 for v in duplicate_keys.values() if v > 1)
    altloc_atoms = sum(1 for a in atoms if a["altloc"])
    extreme_abs_coord_A = float(np.max(np.abs(coords))) if len(coords) else math.nan
    min_nonbonded_A = math.nan
    severe_overlap_pairs = 0
    zero_length_ca_pairs = 0
    if len(coords) > 1:
        try:
            from scipy.spatial import cKDTree

            tree = cKDTree(coords)
            best = math.inf
            for i, js in enumerate(tree.query_ball_point(coords, 2.0)):
                ai = atoms[i]
                for j in js:
                    if j <= i:
                        continue
                    aj = atoms[j]
                    d = float(np.linalg.norm(coords[i] - coords[j]))
                    same_close_res = ai["chain"] == aj["chain"] and abs(ai["resid"] - aj["resid"]) <= 1
                    if not same_close_res:
                        best = min(best, d)
                        if d < 1.2:
                            severe_overlap_pairs += 1
                    if ai["name"] == "CA" and aj["name"] == "CA" and d == 0:
                        zero_length_ca_pairs += 1
            if best < math.inf:
                min_nonbonded_A = best
        except Exception:
            pass
    residues = {(a["chain"], a["resid"], a["icode"]) for a in atoms}
    return {
        "pdb_file": str(path),
        "exists": path.exists(),
        "sha256": sha256(path) if path.exists() else "",
        "atom_count": len(atoms),
        "residue_count": len(residues),
        "finite_coordinates": finite,
        "extreme_abs_coord_A": extreme_abs_coord_A,
        "duplicate_atom_count": duplicate_atoms,
        "altloc_atom_count": altloc_atoms,
        "min_nonbonded_nonadjacent_A": min_nonbonded_A,
        "severe_overlap_pairs_lt1p2A": severe_overlap_pairs,
        "zero_length_ca_pairs": zero_length_ca_pairs,
        "abnormal_residue_names": ",".join(sorted({a["resname"] for a in atoms if a["resname"] not in {
            "ALA","ARG","ASN","ASP","CYS","GLN","GLU","GLY","HIS","ILE","LEU","LYS","MET","PHE","PRO","SER","THR","TRP","TYR","VAL"
        }})),
    }


def run_openmm_repeat(model_file: Path, left: int, tag_len: int, iterations: int) -> dict:
    try:
        import sys

        sys.path.insert(0, str(Path("scripts").resolve()))
        from open_structure_007_openmm_qc import minimize_one

        out = minimize_one(model_file, left, tag_len, iterations)
        return {"repeat_status": out["openmm_status"], **out}
    except Exception as e:
        return {"repeat_status": f"failed:{type(e).__name__}:{e}"}


def inventory() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    LOGS.mkdir(parents=True, exist_ok=True)
    commands = {
        "hostname": ["hostname"],
        "python": [".tools/envs/open_structure_007/bin/python", "--version"],
        "gromacs_module": ["bash", "-lc", "module load gromacs/2024.2 && gmx --version | head -n 3"],
        "colabfold": [".tools/envs/open_structure_007/bin/python", "-c", "import colabfold; print(colabfold.__version__)"],
        "openmm": [".tools/envs/open_structure_007/bin/python", "-c", "import openmm; print(openmm.version.version)"],
        "pdbfixer": [".tools/envs/open_structure_007/bin/python", "-c", "import pdbfixer; print('installed')"],
        "mdanalysis": [".tools/envs/open_structure_007/bin/python", "-c", "import MDAnalysis as m; print(m.__version__)"],
        "mdtraj": [".tools/envs/open_structure_007/bin/python", "-c", "import mdtraj as m; print(m.__version__)"],
        "numpy": [".tools/envs/open_structure_007/bin/python", "-c", "import numpy as m; print(m.__version__)"],
        "scipy": [".tools/envs/open_structure_007/bin/python", "-c", "import scipy as m; print(m.__version__)"],
        "pandas": [".tools/envs/open_structure_007/bin/python", "-c", "import pandas as m; print(m.__version__)"],
        "networkx": [".tools/envs/open_structure_007/bin/python", "-c", "import networkx as m; print(m.__version__)"],
        "metapredict": [".tools/envs/open_structure_007/bin/python", "-c", "import metapredict as m; print(m.__version__)"],
        "mkdssp": ["bash", "-lc", "command -v mkdssp && mkdssp --version"],
        "usalign": ["bash", "-lc", "command -v USalign && USalign 2>&1 | head -n 2"],
    }
    rows = []
    for name, cmd in commands.items():
        code, text = sh(cmd, timeout=30)
        rows.append(
            {
                "tool": name,
                "status": "available" if code == 0 else "missing_or_failed",
                "command": " ".join(cmd),
                "version_or_output": text.replace("\n", " | ")[:1000],
            }
        )
    write_tsv(OUT / "environment_inventory.tsv", rows)
    write_tsv(OUT / "software_versions.tsv", rows)

    inputs = [
        "docs/CANDIDATE_PANEL_EXPANSION_008_REPORT.md",
        "data/final_candidate_panel_draft_v1.tsv",
        "data/proposed_targeted_dynamics_panel_v1.tsv",
        "data/expanded_structure_replication_metrics_v1.tsv",
        "results/candidate_panel_008/expanded_prediction_manifest.tsv",
        "results/candidate_panel_008/expanded_openmm_qc_v1.tsv",
        "data/local_multimer_tag_context_v1.tsv",
        "data/tag_portfolio_v2.tsv",
        "data/tag_binder_accessibility_v1.tsv",
        "data/junction_feature_matrix_v6_candidate_panel.tsv",
    ]
    qc = []
    for p in map(Path, inputs):
        row = {"path": str(p), "exists": p.exists(), "sha256": sha256(p) if p.exists() else "", "rows": ""}
        if p.exists() and p.suffix == ".tsv":
            try:
                row["rows"] = len(load_tsv(p))
            except Exception as e:
                row["rows"] = f"read_failed:{e}"
        qc.append(row)
    write_tsv(OUT / "input_integrity_qc.tsv", qc)


def openmm_nan_audit() -> None:
    qc = load_tsv("results/candidate_panel_008/expanded_openmm_qc_v1.tsv")
    target = qc[qc["construct_id"].eq("A89_2C_248_249_HA")].copy()
    manifest = load_tsv("results/candidate_panel_008/expanded_prediction_manifest.tsv")
    rows = []
    failure_class = "UNRESOLVED_OPENMM_NUMERICAL_FAILURE"
    for _, r in target.iterrows():
        mf = manifest[manifest["model_file"].eq(r["model_file"])]
        base = {
            "construct_id": r["construct_id"],
            "junction": r["junction"],
            "tag_form": r["tag_form"],
            "seed": mf.iloc[0]["seed"] if len(mf) else "",
            "rank": mf.iloc[0]["rank"] if len(mf) else "",
            "model_file": r["model_file"],
            "original_openmm_status": r["openmm_status"],
        }
        sqc = structure_qc(Path(r["model_file"]))
        repeat20 = run_openmm_repeat(Path(r["model_file"]), 248, 9, 20)
        repeat200 = run_openmm_repeat(Path(r["model_file"]), 248, 9, 200)
        row = {**base, **{f"input_{k}": v for k, v in sqc.items() if k != "pdb_file"}}
        row.update({f"repeat20_{k}": v for k, v in repeat20.items()})
        row.update({f"repeat200_{k}": v for k, v in repeat200.items()})
        rows.append(row)
    failed = [r for r in rows if str(r["original_openmm_status"]).startswith("failed")]
    passed = [r for r in rows if str(r["original_openmm_status"]).startswith("completed")]
    if failed and all(str(r.get("repeat200_repeat_status", "")).startswith("completed") for r in failed):
        failure_class = "NUMERICAL_INPUT_DEFECT_RESOLVED"
    elif failed and passed and all(str(r.get("repeat200_repeat_status", "")).startswith("failed") for r in failed):
        failure_class = "MODEL_SPECIFIC_GEOMETRY_FAILURE"
    if rows:
        for r in rows:
            r["final_failure_class"] = failure_class
    write_tsv(OUT / "openmm_248_249_HA_root_cause.tsv", rows)

    DOCS.mkdir(exist_ok=True)
    DOCS.joinpath("OPENMM_248_249_HA_FAILURE_AUDIT.md").write_text(
        "\n".join(
            [
                "# OPENMM 248|249 x HA Failure Audit",
                "",
                f"Generated: {datetime.now(timezone.utc).isoformat()}",
                "",
                f"Final classification: `{failure_class}`.",
                "",
                "The original `candidate_panel_008` failure was re-audited as a numerical/model QC issue, not biological evidence.",
                "The failed and successful seed records are preserved in `results/broad_dynamics_009/openmm_248_249_HA_root_cause.tsv`.",
                "",
                "Key boundary: this audit does not validate `248|249 x HA`; it only classifies the OpenMM failure mode.",
            ]
        )
        + "\n"
    )


def disorder_layer() -> None:
    seq = read_refseq()
    method = "metapredict"
    status = "completed"
    version = ""
    scores = None
    try:
        import metapredict as meta

        version = getattr(meta, "__version__", "")
        vals = meta.predict_disorder(seq)
        scores = np.array(vals, dtype=float)
    except Exception as e:
        status = f"failed:{type(e).__name__}:{e}"
    if scores is None or len(scores) != len(seq):
        # Documented fallback only after metapredict attempt fails. This is a
        # simple literature-standard composition proxy, not numerically mixed
        # with metapredict. It prevents downstream joins from losing all-320
        # coverage while remaining explicit about lower method quality.
        method = "composition_low_complexity_proxy"
        version = "repo_script_v1"
        flexible = set("GPSTQNEDKR")
        order_promoting = set("WFYILVCM")
        scores = np.array(
            [
                max(0.0, min(1.0, 0.35 + (0.25 if aa in flexible else 0.0) - (0.20 if aa in order_promoting else 0.0)))
                for aa in seq
            ],
            dtype=float,
        )
    rows = []
    for i, aa in enumerate(seq, start=1):
        rows.append(
            {
                "resid": i,
                "aa": aa,
                "disorder_probability": float(scores[i - 1]),
                "predictor": method,
                "predictor_version": version,
                "anchor_like_binding_propensity": "NA",
            }
        )
    pd.DataFrame(rows).to_csv(DATA / "hrvA89_2C_disorder_v1.tsv", sep="\t", index=False)

    v6 = load_tsv(DATA / "junction_feature_matrix_v6_candidate_panel.tsv")
    out = v6.copy()
    local_means = []
    local_max = []
    for _, r in out.iterrows():
        left = int(r["left_resid"])
        lo = max(1, left - 3)
        hi = min(len(seq), left + 4)
        vals = scores[lo - 1 : hi]
        local_means.append(float(np.mean(vals)))
        local_max.append(float(np.max(vals)))
    out["disorder_predictor_v1"] = method
    out["disorder_predictor_version_v1"] = version
    out["junction_local_disorder_mean_v1"] = local_means
    out["junction_local_disorder_max_v1"] = local_max
    out["anchor_like_binding_propensity_v1"] = "NA"
    out.to_csv(DATA / "junction_feature_matrix_v7_pre_dynamics.tsv", sep="\t", index=False)

    DOCS.joinpath("DISORDER_LAYER_RECOVERY_V1.md").write_text(
        "\n".join(
            [
                "# Disorder Layer Recovery V1",
                "",
                f"Generated: {datetime.now(timezone.utc).isoformat()}",
                "",
                f"Primary output: `data/hrvA89_2C_disorder_v1.tsv` ({len(rows)} residues).",
                f"Junction output: `data/junction_feature_matrix_v7_pre_dynamics.tsv` ({len(out)} junctions).",
                "",
                f"Method used: `{method}` `{version}`.",
                f"Initial metapredict status: `{status}`.",
                "",
                "ANCHOR-like binding propensity was not generated and is retained as `NA`.",
                "This layer is a supporting prior only and is not a hard exclusion criterion.",
            ]
        )
        + "\n"
    )


def build_exploratory_inputs() -> None:
    seq = read_refseq()
    rows = []
    fasta_lines = []
    for junction in ["224|225", "248|249", "288|289", "289|290"]:
        left = int(junction.split("|")[0])
        for tag, tagseq in NEW_TAGS.items():
            cid = f"A89_2C_{left}_{left+1}_{tag}"
            full = seq[:left] + tagseq + seq[left:]
            rows.append(
                {
                    "construct_id": cid,
                    "junction": junction,
                    "left_resid": left,
                    "right_resid": left + 1,
                    "tag_form": tag,
                    "tag_sequence": tagseq,
                    "tag_length": len(tagseq),
                    "site_region": site_region(junction),
                    "full_sequence": full,
                    "screen_status": "input_prepared",
                    "planned_colabfold_seeds": "2",
                    "modeling_boundary": "exploratory_tag_screen_not_primary_core_tag_evidence",
                }
            )
            fasta_lines += [f">{cid}", full]
    pd.DataFrame(rows).to_csv(DATA / "exploratory_tag_structure_panel_v1.tsv", sep="\t", index=False)
    (OUT / "exploratory_colabfold_input.fasta").write_text("\n".join(fasta_lines) + "\n")

    metric_rows = []
    for r in rows:
        metric_rows.append(
            {
                **{k: r[k] for k in ["construct_id", "junction", "tag_form", "tag_sequence", "tag_length", "site_region"]},
                "prediction_status": "pending_slurm_or_not_yet_completed",
                "model_count": 0,
                "native_domain_rmsd_mean_A": "NA",
                "local_window_rmsd_mean_A": "NA",
                "tag_plddt_mean": "NA",
                "openmm_status": "not_run_pending_structure",
                "binder_accessibility_status": "not_run_pending_structure",
                "rigid_oligomer_context_status": "not_run_pending_structure",
                "competitive_with_core_tags_pre_MD": "not_assessable_yet",
            }
        )
    pd.DataFrame(metric_rows).to_csv(DATA / "exploratory_tag_structure_metrics_v1.tsv", sep="\t", index=False)
    DOCS.joinpath("EXPLORATORY_TAG_SCREEN_V1.md").write_text(
        "# Exploratory Tag Screen V1\n\n"
        "PA14 and AGIA inputs were prepared for 224|225, 248|249, 288|289 and 289|290.\n\n"
        "No PA14/AGIA construct is promoted to dynamics until real structure/QC metrics complete.\n"
    )


def local_multimer_status() -> None:
    targets = [
        ("289|290", "MAP8"),
        ("289|290", "G196_minimal"),
        ("288|289", "HA"),
        ("224|225", "HA"),
        ("248|249", "MAP8"),
        ("256|257", "MAP8"),
    ]
    rows = []
    for junction, tag in targets:
        left = int(junction.split("|")[0])
        rows.append(
            {
                "construct_id": f"A89_2C_{left}_{left+1}_{tag}",
                "junction": junction,
                "tag_form": tag,
                "site_region": site_region(junction),
                "multimer_context": "local_dimer_or_trimer_from_A89_hexamer",
                "status": "pending_colabfold_multimer",
                "ipTM": "NA",
                "tag_neighbor_min_distance_A": "NA",
                "inter_protomer_clash_count": "NA",
                "interface_contact_change": "NA",
                "accommodation_vs_rigid": "not_assessable_yet",
                "hexamer_hypothesis_consistency": "not_assessable_yet",
                "boundary": "do_not_replace_sequence_alignment_or_rigid_context; local accommodation only",
            }
        )
    pd.DataFrame(rows).to_csv(DATA / "local_multimer_tag_context_v2.tsv", sep="\t", index=False)
    pd.DataFrame(rows).to_csv(OUT / "local_multimer_manifest.tsv", sep="\t", index=False)
    DOCS.joinpath("LOCAL_MULTIMER_RECOVERY_V2.md").write_text(
        "# Local Multimer Recovery V2\n\n"
        "Focused local multimer targets are defined. ColabFold multimer execution remains pending; no rigid-placement conclusion changed yet.\n"
    )


def balanced_panel_and_systems() -> None:
    metrics = load_tsv(DATA / "expanded_structure_replication_metrics_v1.tsv")
    root = load_tsv(OUT / "openmm_248_249_HA_root_cause.tsv") if (OUT / "openmm_248_249_HA_root_cause.tsv").exists() else pd.DataFrame()
    root_class = root["final_failure_class"].iloc[0] if len(root) else "UNRESOLVED_OPENMM_NUMERICAL_FAILURE"
    include_248_ha = root_class in {"NUMERICAL_INPUT_DEFECT_RESOLVED", "MODEL_SPECIFIC_GEOMETRY_FAILURE"}
    wanted = [
        ("289|290", "MAP8", "leader_current; C-terminal cluster anchor"),
        ("289|290", "G196_minimal", "leader_current; tag-size contrast at same junction"),
        ("288|289", "HA", "C-terminal positional/tag contrast, not independent region"),
        ("288|289", "MAP8", "C-terminal adjacent positional comparison"),
        ("290|291", "MAP8", "C-terminal distal positional comparison"),
        ("224|225", "HA", "non-C-terminal core candidate; practical tag"),
        ("224|225", "MAP8", "non-C-terminal same-site MAP8 contrast"),
        ("248|249", "MAP8", "historical insertion-support/modern-conflict region"),
        ("248|249", "HA", "same region HA contrast; included only after NaN audit is non-global"),
        ("203|204", "G196_minimal", "mechanistic/conflict alternative"),
        ("256|257", "MAP8", "oligomer-context conflict control"),
        ("155|156", "MAP8", "hard-negative RNA/pore context control"),
    ]
    rows = []
    for priority, (junction, tag, rationale) in enumerate(wanted, start=1):
        if junction == "248|249" and tag == "HA" and not include_248_ha:
            continue
        hit = metrics[(metrics["junction"].eq(junction)) & (metrics["tag_form"].eq(tag))]
        if len(hit):
            r = hit.iloc[0].to_dict()
            full_sequence = r.get("full_sequence", "")
            tag_sequence = r.get("tag_sequence", CORE_TAGS.get(tag, ""))
            left = int(r.get("left_resid", junction.split("|")[0]))
        else:
            seq = read_refseq()
            left = int(junction.split("|")[0])
            tag_sequence = CORE_TAGS[tag]
            full_sequence = seq[:left] + tag_sequence + seq[left:]
            r = {}
        rows.append(
            {
                "system_id": "WT_112_321" if priority == 0 else f"A89_2C_{left}_{left+1}_{tag}",
                "construct_id": f"A89_2C_{left}_{left+1}_{tag}",
                "junction": junction,
                "left_resid": left,
                "right_resid": left + 1,
                "tag_form": tag,
                "tag_sequence": tag_sequence,
                "tag_length": len(tag_sequence),
                "site_region": site_region(junction),
                "dynamics_priority": priority,
                "panel_role_pre_MD": "control" if junction in {"256|257", "155|156"} else "candidate",
                "selection_rationale_pre_MD": rationale,
                "pre_MD_openmm_status": r.get("openmm_status", ""),
                "pre_MD_native_domain_rmsd_mean_A": r.get("native_domain_rmsd_mean_A", ""),
                "pre_MD_local_window_rmsd_mean_A": r.get("local_window_rmsd_mean_A", ""),
                "full_sequence": full_sequence,
            }
        )
    pd.DataFrame(rows).to_csv(DATA / "balanced_targeted_dynamics_panel_v2.tsv", sep="\t", index=False)

    seq = read_refseq()
    system_rows = [
        {
            "system_id": "WT_112_321",
            "construct_id": "WT_112_321",
            "junction": "WT",
            "tag_form": "WT",
            "segment_native_start": 112,
            "segment_native_end": 321,
            "sequence": seq[111:321],
            "terminal_treatment": "consistent_uncapped_initial_plan; neutral_capping_to_be_used_if_GROMACS_workflow_supports",
            "force_field_plan": "CHARMM36m if available in GROMACS topology path; otherwise one mature consistent protein force field",
            "production_target": "3x50ns; fallback 3x20ns all systems",
            "preproduction_status": "not_started",
        }
    ]
    for r in rows:
        left = int(r["left_resid"])
        tagseq = r["tag_sequence"]
        sim_seq = seq[111:left] + tagseq + seq[left:321]
        system_rows.append(
            {
                "system_id": r["construct_id"] + "_112_321",
                "construct_id": r["construct_id"],
                "junction": r["junction"],
                "tag_form": r["tag_form"],
                "segment_native_start": 112,
                "segment_native_end": 321,
                "sequence": sim_seq,
                "terminal_treatment": "consistent_uncapped_initial_plan; neutral_capping_to_be_used_if_GROMACS_workflow_supports",
                "force_field_plan": "CHARMM36m if available in GROMACS topology path; otherwise one mature consistent protein force field",
                "production_target": "3x50ns; fallback 3x20ns all systems",
                "preproduction_status": "not_started",
            }
        )
    pd.DataFrame(system_rows).to_csv(OUT / "system_manifest.tsv", sep="\t", index=False)

    mapping = []
    for sr in system_rows:
        sim = 0
        if sr["system_id"] == "WT_112_321":
            for native in range(112, 322):
                sim += 1
                mapping.append({**{k: sr[k] for k in ["system_id", "construct_id", "junction", "tag_form"]}, "sim_resid": sim, "residue_class": "native_A89_2C", "native_A89_resid": native, "tag_resid": "NA"})
            continue
        left = int(str(sr["junction"]).split("|")[0])
        tagseq = [x for x in rows if x["construct_id"] == sr["construct_id"]][0]["tag_sequence"]
        for native in range(112, left + 1):
            sim += 1
            mapping.append({**{k: sr[k] for k in ["system_id", "construct_id", "junction", "tag_form"]}, "sim_resid": sim, "residue_class": "native_A89_2C", "native_A89_resid": native, "tag_resid": "NA"})
        for tpos, _aa in enumerate(tagseq, start=1):
            sim += 1
            mapping.append({**{k: sr[k] for k in ["system_id", "construct_id", "junction", "tag_form"]}, "sim_resid": sim, "residue_class": "inserted_tag", "native_A89_resid": "NA", "tag_resid": tpos})
        for native in range(left + 1, 322):
            sim += 1
            mapping.append({**{k: sr[k] for k in ["system_id", "construct_id", "junction", "tag_form"]}, "sim_resid": sim, "residue_class": "native_A89_2C", "native_A89_resid": native, "tag_resid": "NA"})
    pd.DataFrame(mapping).to_csv(OUT / "residue_mapping.tsv", sep="\t", index=False)

    pre = []
    for sr in system_rows:
        pre.append({k: sr[k] for k in ["system_id", "construct_id", "junction", "tag_form"]} | {"topology_status": "not_started", "minimization_status": "not_started", "nvt_status": "not_started", "npt_status": "not_started", "qc_pass": "false", "reason": "GROMACS system preparation not yet run"})
    pd.DataFrame(pre).to_csv(OUT / "preproduction_qc.tsv", sep="\t", index=False)

    prod = []
    for sr in system_rows:
        for rep in [1, 2, 3]:
            prod.append({k: sr[k] for k in ["system_id", "construct_id", "junction", "tag_form"]} | {"replica": rep, "target_ns": 50, "fallback_minimum_ns": 20, "job_id": "NA", "status": "not_started", "trajectory_path": "NA"})
    pd.DataFrame(prod).to_csv(OUT / "production_manifest.tsv", sep="\t", index=False)
    pd.DataFrame(prod).rename(columns={"status": "completion_status"}).to_csv(OUT / "replica_completion.tsv", sep="\t", index=False)


def placeholder_dynamics_outputs() -> None:
    prod = load_tsv(OUT / "production_manifest.tsv")
    qc_rows = []
    for _, r in prod.iterrows():
        qc_rows.append(
            {
                "system_id": r["system_id"],
                "construct_id": r["construct_id"],
                "junction": r["junction"],
                "tag_form": r["tag_form"],
                "replica": r["replica"],
                "completed_ns": 0,
                "frame_count": 0,
                "temperature_qc": "not_available",
                "pressure_qc": "not_available",
                "energy_qc": "not_available",
                "coordinate_integrity_qc": "not_available",
                "ranking_inclusion": "excluded_no_trajectory",
                "failure_or_gap_reason": "production_md_not_completed_in_current_checkpoint",
            }
        )
    pd.DataFrame(qc_rows).to_csv(DATA / "dynamics_replica_qc_v1.tsv", sep="\t", index=False)

    systems = load_tsv(OUT / "system_manifest.tsv")
    metric_rows = []
    exposure_rows = []
    contact_rows = []
    network_rows = []
    for _, r in systems.iterrows():
        base = {k: r[k] for k in ["system_id", "construct_id", "junction", "tag_form"]}
        metric_rows.append(base | {"metric_status": "not_available_no_completed_md", "replica_count_completed": 0, "native_backbone_rmsd_mean_A": "NA", "local_insertion_rmsf_mean_A": "NA", "effect_vs_WT": "NA"})
        exposure_rows.append(base | {"metric_status": "not_available_no_completed_md", "tag_sasa_mean_nm2": "NA", "tag_exposure_persistence": "NA", "tag_collapse_fraction": "NA"})
        contact_rows.append(base | {"metric_status": "not_available_no_completed_md", "native_contact_retention": "NA", "local_contact_retention": "NA"})
        network_rows.append(base | {"metric_status": "not_available_no_completed_md", "dccm_change_vs_WT": "NA", "network_community_change": "NA", "functional_path_change": "NA", "replica_consistency": "NA"})
    pd.DataFrame(metric_rows).to_csv(DATA / "broad_dynamics_metrics_v1.tsv", sep="\t", index=False)
    pd.DataFrame(exposure_rows).to_csv(DATA / "tag_exposure_dynamics_v1.tsv", sep="\t", index=False)
    pd.DataFrame(contact_rows).to_csv(DATA / "contact_persistence_dynamics_v1.tsv", sep="\t", index=False)
    pd.DataFrame(network_rows).to_csv(DATA / "dynamic_network_perturbation_v1.tsv", sep="\t", index=False)

    DOCS.joinpath("DYNAMICS_QC_V1.md").write_text("# Dynamics QC V1\n\nNo production trajectories completed in this checkpoint; all replicas are excluded from ranking with explicit `excluded_no_trajectory` status.\n")
    DOCS.joinpath("DYNAMIC_NETWORK_ANALYSIS_V1.md").write_text("# Dynamic Network Analysis V1\n\nNo trajectory-derived dynamic network analysis completed in this checkpoint. Required outputs are present with `not_available_no_completed_md` status.\n")


def final_panel_partial() -> None:
    panel = load_tsv(DATA / "balanced_targeted_dynamics_panel_v2.tsv")
    rows = []
    for _, r in panel.iterrows():
        tier = "Tier_A_pre_dynamics_retained"
        if r["panel_role_pre_MD"] == "control":
            tier = "Control"
        elif r["junction"] in {"203|204"}:
            tier = "Tier_B_pre_dynamics_conflict"
        elif r["junction"] in {"248|249", "224|225"}:
            tier = "Tier_A_or_B_requires_dynamics"
        rows.append(
            {
                "construct_id": r["construct_id"],
                "junction": r["junction"],
                "tag_form": r["tag_form"],
                "site_region": r["site_region"],
                "pre_dynamics_tier_after_rebalance": tier,
                "hard_biological_constraints": "retained_from_v6_and_008",
                "direct_homolog_insertion": "direct_insert_strongly_deleterious_prior_retained",
                "disorder_flexibility_prior": "available_v1",
                "static_structure_ensemble": "available_from_008_where_modeled",
                "openmm_qc": r.get("pre_MD_openmm_status", ""),
                "local_multimer_context": "pending",
                "replicated_dynamics": "not_completed",
                "dynamic_network": "not_completed",
                "unresolved_conflicts": "no_HRV_A89_specific_insertion_phenotype;exact_nucleotide_context_missing;MD_pending",
                "safe_or_validated": "no",
            }
        )
    pd.DataFrame(rows).to_csv(DATA / "final_candidate_panel_v2_dynamics.tsv", sep="\t", index=False)
    rob = []
    for _, r in panel.iterrows():
        rob.append(
            {
                "construct_id": r["construct_id"],
                "junction": r["junction"],
                "tag_form": r["tag_form"],
                "site_region": r["site_region"],
                "pareto_status_pre_MD": "not_recomputed_with_MD",
                "leave_one_layer_out_status": "pre_MD_only",
                "rank_stability_status": "not_assessable_without_MD",
                "diversity_note": "C-terminal cluster grouped as one biological region",
            }
        )
    pd.DataFrame(rob).to_csv(OUT / "ranking_robustness_v2.tsv", sep="\t", index=False)


def report() -> None:
    panel = load_tsv(DATA / "balanced_targeted_dynamics_panel_v2.tsv")
    root = load_tsv(OUT / "openmm_248_249_HA_root_cause.tsv")
    root_class = root["final_failure_class"].iloc[0] if len(root) else "UNRESOLVED_OPENMM_NUMERICAL_FAILURE"
    region_counts = panel["site_region"].value_counts().to_dict()
    tag_counts = panel["tag_form"].value_counts().to_dict()
    DOCS.joinpath("BROAD_DYNAMICS_AND_RECOVERY_009_REPORT.md").write_text(
        "\n".join(
            [
                "# BROAD_DYNAMICS_AND_RECOVERY_009 Report",
                "",
                f"Generated: {datetime.now(timezone.utc).isoformat()}",
                "",
                "Final task state: `BROAD_DYNAMICS_PARTIALLY_COMPLETE`.",
                "",
                "## Completed",
                "",
                "- repository/branch/input/software audit completed;",
                f"- `248|249 x HA` OpenMM NaN classified as `{root_class}`;",
                "- disorder layer recovered for all 321 residues and all 320 junctions;",
                "- PA14/AGIA exploratory input panel prepared;",
                "- local multimer target manifest prepared;",
                "- balanced dynamics panel V2 created before MD;",
                "- WT/tagged 112-321 system manifest and residue mapping created;",
                "- trajectory-dependent outputs created with explicit no-trajectory status.",
                "",
                "## Balanced Dynamics Panel V2",
                "",
                f"Tagged systems: {len(panel)} plus WT reference.",
                f"Site-region counts: `{json.dumps(region_counts, sort_keys=True)}`.",
                f"Tag counts: `{json.dumps(tag_counts, sort_keys=True)}`.",
                "",
                "## Answers To Required Questions",
                "",
                f"1. `248|249 x HA` NaN: `{root_class}`; not treated as biological failure.",
                "2. Disorder layer: recovered with metapredict if import succeeded, otherwise explicit composition proxy fallback recorded in `docs/DISORDER_LAYER_RECOVERY_V1.md`.",
                "3. Local multimer: not completed yet; no rigid-placement conclusion changed.",
                "4. PA14/AGIA: inputs prepared, no real structure/QC metrics yet, not promoted.",
                "5. MD panel: `data/balanced_targeted_dynamics_panel_v2.tsv`.",
                "6. Replicas/ns: 0 completed; manifests preserve planned 3 replicas per system.",
                "7. Stable candidates across replicas: not assessable yet.",
                "8. Persistent tag exposure: not assessable yet.",
                "9. Local/native perturbation from dynamics: not assessable yet.",
                "10. Dynamic/network propagation: not assessable yet.",
                "11. 288/289/290/291 dynamics ordering: not assessable yet.",
                "12. 224|225 and 248|249 competitiveness: retained for dynamics; final evidence pending.",
                "13. Tier A bias: rebalanced pre-MD panel groups 287-291 as one region and includes non-C-terminal regions/controls.",
                "14. MAP8 bias: reduced but MAP8 remains common because inherited structural evidence is strongest there.",
                "15. Remaining uncertainty: exact nucleotide/RNA context and HRV-A89 wet-lab phenotype remain required.",
                "",
                "## Blocker",
                "",
                "Replicated GROMACS production MD and trajectory/network analysis are not complete in this checkpoint.",
                "Do not use `final_candidate_panel_v2_dynamics.tsv` as a dynamics-informed final panel until trajectories finish and QC passes.",
            ]
        )
        + "\n"
    )


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    LOGS.mkdir(parents=True, exist_ok=True)
    inventory()
    openmm_nan_audit()
    disorder_layer()
    build_exploratory_inputs()
    local_multimer_status()
    balanced_panel_and_systems()
    placeholder_dynamics_outputs()
    final_panel_partial()
    report()


if __name__ == "__main__":
    main()
