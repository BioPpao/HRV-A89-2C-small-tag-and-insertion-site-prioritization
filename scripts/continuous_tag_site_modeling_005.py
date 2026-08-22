#!/usr/bin/env python3
"""CONTINUOUS_TAG_SITE_MODELING_005 integration.

This script builds the reduced site x tag panel and completes the analyses that
can be run from existing WT A89 structures plus upstream V5/PLM evidence. It
does not fabricate inserted-structure models when mature predictors are absent.
"""
from __future__ import annotations

import argparse
import math
import os
import shutil
import socket
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np
import pandas as pd
from Bio.PDB import MMCIFParser, PDBParser
from scipy.spatial.distance import cdist


TAG_ORDER = ["MAP8", "HA", "G196_minimal", "G196_practical_GS"]
CONTACT_CUTOFF_A = 8.0
LOCAL_PAD = 3


def fnum(x: object, default: float = math.nan) -> float:
    try:
        if pd.isna(x):
            return default
        return float(x)
    except Exception:
        return default


def bstr(x: object) -> bool:
    return str(x).strip().lower() == "true"


def cmd_text(cmd: list[str], timeout: int = 20) -> tuple[int, str]:
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return p.returncode, (p.stdout + p.stderr).strip()
    except Exception as e:
        return 999, repr(e)


def read_reference_sequence(path: Path) -> str:
    seq = []
    for line in path.read_text().splitlines():
        if not line.startswith(">"):
            seq.append(line.strip())
    out = "".join(seq)
    if len(out) != 321:
        raise ValueError(f"Expected 321 aa A89 2C sequence, observed {len(out)}")
    return out


def load_ca_structure(path: Path, kind: str) -> dict[str, dict[int, np.ndarray]]:
    parser = MMCIFParser(QUIET=True) if path.suffix.lower() in {".cif", ".mmcif"} else PDBParser(QUIET=True)
    structure = parser.get_structure(path.stem, str(path))
    out: dict[str, dict[int, np.ndarray]] = {}
    for chain in structure[0]:
        residues: dict[int, np.ndarray] = {}
        for res in chain:
            het, resid, _icode = res.id
            if het != " " or not (1 <= resid <= 321) or "CA" not in res:
                continue
            residues[int(resid)] = np.asarray(res["CA"].coord, dtype=float)
        if residues:
            out[chain.id] = residues
    if not out:
        raise ValueError(f"No CA residues parsed from {path}")
    if kind == "monomer" and len(out) != 1:
        raise ValueError(f"Expected one chain in {path}, observed {len(out)}")
    return out


def structure_contact_context(paths: dict[str, Path], junctions: list[str]) -> pd.DataFrame:
    records = []
    parsed = {
        "af_model_1": load_ca_structure(paths["af1"], "monomer"),
        "af_model_3": load_ca_structure(paths["af3"], "monomer"),
        "hexamer_01": load_ca_structure(paths["hex1"], "hexamer"),
        "hexamer_02": load_ca_structure(paths["hex2"], "hexamer"),
    }
    for structure_name, chains in parsed.items():
        chain_ids = sorted(chains)
        coords_by_chain = {c: chains[c] for c in chain_ids}
        for junction in junctions:
            left = int(junction.split("|")[0])
            window = set(range(max(1, left - LOCAL_PAD), min(321, left + 1 + LOCAL_PAD) + 1))
            local_degrees = []
            local_cross = []
            flank_distances = []
            for chain_id in chain_ids:
                residues = coords_by_chain[chain_id]
                all_res = np.array(sorted(residues), dtype=int)
                all_xyz = np.vstack([residues[int(r)] for r in all_res])
                local_res = [r for r in sorted(window) if r in residues]
                if left in residues and left + 1 in residues:
                    flank_distances.append(float(np.linalg.norm(residues[left] - residues[left + 1])))
                for r in local_res:
                    d = np.linalg.norm(all_xyz - residues[r], axis=1)
                    intra = int(np.sum((d <= CONTACT_CUTOFF_A) & (np.abs(all_res - r) > 2)))
                    cross = 0
                    for other_id in chain_ids:
                        if other_id == chain_id:
                            continue
                        other = coords_by_chain[other_id]
                        other_xyz = np.vstack(list(other.values()))
                        cross += int(np.sum(np.linalg.norm(other_xyz - residues[r], axis=1) <= CONTACT_CUTOFF_A))
                    local_degrees.append(intra + cross)
                    local_cross.append(cross)
            if local_degrees:
                records.append({
                    "junction": junction,
                    "structure": structure_name,
                    "local_window": f"{min(window)}-{max(window)}",
                    "mean_local_ca_degree_8A": float(np.mean(local_degrees)),
                    "max_local_ca_degree_8A": int(np.max(local_degrees)),
                    "mean_cross_chain_ca_degree_8A": float(np.mean(local_cross)),
                    "max_cross_chain_ca_degree_8A": int(np.max(local_cross)),
                    "flanking_ca_distance_A": float(np.mean(flank_distances)) if flank_distances else math.nan,
                })
    df = pd.DataFrame(records)
    agg = df.groupby("junction").agg(
        mean_local_ca_degree_8A=("mean_local_ca_degree_8A", "mean"),
        max_local_ca_degree_8A=("max_local_ca_degree_8A", "max"),
        mean_cross_chain_ca_degree_8A=("mean_cross_chain_ca_degree_8A", "mean"),
        max_cross_chain_ca_degree_8A=("max_cross_chain_ca_degree_8A", "max"),
        mean_flanking_ca_distance_A=("flanking_ca_distance_A", "mean"),
        structures_evaluated=("structure", lambda x: ";".join(sorted(set(x)))),
    ).reset_index()
    return agg


def contact_class(row: pd.Series) -> str:
    if fnum(row["max_cross_chain_ca_degree_8A"]) > 0 or fnum(row["mean_local_ca_degree_8A"]) >= 9:
        return "WT_ANCHOR_NETWORK_CONSTRAINED"
    if fnum(row["mean_local_ca_degree_8A"]) >= 5:
        return "WT_ANCHOR_NETWORK_MIXED"
    return "WT_ANCHOR_NETWORK_LOWER_CONSTRAINT"


def loop_proxy(row: pd.Series, tag_len: int) -> str:
    if row["functional_tier"] == "EXCLUDE":
        return "FUNCTIONAL_NEGATIVE_CONTROL"
    coil = bstr(row["both_AF_coil"]) and fnum(row["min_hex_coil_fraction"], 0.0) >= 0.5
    exposed = fnum(row["min_AF_rSASA"], 0.0) >= 0.25 and fnum(row["min_hexamer_mean_rSASA"], 0.0) >= 0.20
    buried = fnum(row["max_any_chain_burial_fraction"], 1.0) >= 0.25
    if coil and exposed and not buried and tag_len <= 8:
        return "LOOP_PROXY_RELATIVELY_FAVORABLE"
    if exposed and not buried:
        return "LOOP_PROXY_MIXED"
    return "LOOP_PROXY_UNFAVORABLE"


def hexamer_class(row: pd.Series, tag_len: int) -> str:
    if row["functional_tier"] == "EXCLUDE":
        return "FUNCTIONAL_NEGATIVE_CONTROL"
    inter = fnum(row["min_interprotomer_heavy_atom_A"], 999.0)
    burial = fnum(row["max_any_chain_burial_fraction"], 1.0)
    radial = fnum(row["min_mean_pore_radial_A"], 999.0)
    if inter < 6.0 or burial >= 0.35 or radial < 8.0:
        return "OLIGOMER_CONTEXT_UNFAVORABLE"
    if inter < 10.0 or burial >= 0.15 or radial < 12.0 or tag_len > 8:
        return "OLIGOMER_CONTEXT_MIXED"
    return "OLIGOMER_CONTEXT_RELATIVELY_FAVORABLE"


def length_class(tag_len: int) -> str:
    if tag_len <= 5:
        return "shortest_tag"
    if tag_len <= 8:
        return "medium_tag"
    return "longer_flanked_tag"


def qualitative_integration(row: pd.Series) -> str:
    if row["functional_tier"] == "EXCLUDE" or row["candidate_class_v5_plm_gpu"] == "hard_excluded":
        return "NEGATIVE_CONTROL"
    if row["mapping_class"] != "exact_aligned":
        return "METHOD_INCONCLUSIVE_MAPPING_UNCERTAIN"
    if (
        row["loop_feasibility_class"] == "LOOP_PROXY_RELATIVELY_FAVORABLE"
        and row["hexamer_context_class"] == "OLIGOMER_CONTEXT_RELATIVELY_FAVORABLE"
        and row["network_context_class"] == "WT_ANCHOR_NETWORK_LOWER_CONSTRAINT"
    ):
        return "RELATIVELY_LOWER_PERTURBATION__DIRECT_EVIDENCE_CONFLICT"
    if fnum(row["plm_percentile_within_tag"], 0.0) >= 0.75 and row["hexamer_context_class"] != "OLIGOMER_CONTEXT_UNFAVORABLE":
        return "PLM_SUPPORTED_BUT_DIRECT_OR_FUNCTIONAL_CONFLICT"
    if row["hexamer_context_class"] == "OLIGOMER_CONTEXT_UNFAVORABLE" or row["network_context_class"] == "WT_ANCHOR_NETWORK_CONSTRAINED":
        return "STRUCTURALLY_DISFAVORED_OR_CONTEXT_CONSTRAINED"
    if row["best_tag_form"] != row["worst_tag_form"] and fnum(row["plm_percentile_range"], 0.0) >= 0.35:
        return "TAG_SPECIFIC_DISAGREEMENT"
    return "METHOD_INCONCLUSIVE"


def write_inventory(out: Path, paths: dict[str, Path], final_state_hint: str) -> None:
    rows = []
    commands = {
        "hostname": ["hostname"],
        "analysis_python": [sys.executable, "--version"],
        "nvidia-smi": ["bash", "-lc", "nvidia-smi 2>&1 || true"],
        "cuda_visible_devices": ["bash", "-lc", "printf '%s' \"$CUDA_VISIBLE_DEVICES\""],
        "dev_nvidia": ["bash", "-lc", "ls -l /dev/nvidia* 2>&1 || true"],
        "python": ["python3", "--version"],
        "colabfold_batch": ["bash", "-lc", "command -v colabfold_batch || true"],
        "alphafold": ["bash", "-lc", "command -v run_alphafold.py || command -v alphafold || true"],
        "rosetta": ["bash", "-lc", "command -v rosetta_scripts || command -v remodel.default.linuxgccrelease || true"],
        "foldx": ["bash", "-lc", "command -v foldx || true"],
        "esmfold": ["bash", "-lc", "command -v esm-fold || true"],
        "module_relevant": ["bash", "-lc", "module avail 2>&1 | grep -Ei 'rosetta|foldx|colab|alphafold|openfold|esm|pytorch|cuda|gromacs|amber|APBS' | head -80 || true"],
    }
    for label, cmd in commands.items():
        code, text = cmd_text(cmd)
        rows.append({
            "record_type": "environment_probe",
            "name": label,
            "status": "completed_probe",
            "value": text.replace("\t", " ").replace("\n", " | "),
            "exit_code": code,
            "method_consequence": "",
        })
    for name, path in paths.items():
        rows.append({
            "record_type": "input_structure",
            "name": name,
            "status": "available" if path.exists() else "missing",
            "value": str(path),
            "exit_code": "",
            "method_consequence": "WT context metrics only; no inserted structures generated",
        })
    method_rows = [
        ("insertion_specific_structure_prediction", "DEFERRED_SOFTWARE",
         "No ColabFold/AlphaFold/OpenFold/ESMFold executable found in PATH/modules; no inserted-construct model ensemble was generated."),
        ("loop_backbone_feasibility", "COMPLETED_PROXY_ONLY__PRIMARY_DEFERRED_SOFTWARE",
         "No Rosetta Remodel/KIC/PyRosetta loop workflow found; WT anchor geometric loop proxy reported separately."),
        ("local_energy_frustration", "DEFERRED_SOFTWARE",
         "No FoldX/Rosetta/local-frustration workflow found for inserted models; energy values not fabricated."),
        ("oligomer_context_compatibility", "COMPLETED_WT_CONTEXT_PROXY",
         "Existing A89 no-membrane/no-RNA hexamer hypotheses used to quantify anchor proximity/burial/pore context."),
        ("residue_contact_network", "COMPLETED_WT_ANCHOR_NETWORK__TAGGED_MAP_DEFERRED",
         "CA contact networks computed for WT monomer/hexamer structures; tagged contact-map deltas require inserted models."),
        ("targeted_evolutionary_statistical", "COMPLETED_REUSE_TARGETED",
         "Reused V5/V2 conservation, direct homolog phenotype, independent-indel and PLM metrics for panel only."),
        ("cross_method_robustness", "COMPLETED_WITH_DEFERRED_METHOD_FLAGS",
         "Robustness integrates completed layers and explicit software-deferred layers."),
    ]
    for name, status, consequence in method_rows:
        rows.append({
            "record_type": "method_status",
            "name": name,
            "status": status,
            "value": final_state_hint,
            "exit_code": "",
            "method_consequence": consequence,
        })
    pd.DataFrame(rows).to_csv(out, sep="\t", index=False)


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--v5", type=Path, default=Path("data/candidate_junctions_v5_plm_gpu.tsv"))
    p.add_argument("--review", type=Path, default=Path("data/computational_review_set_v2_plm_gpu.tsv"))
    p.add_argument("--plm", type=Path, default=Path("data/tag_specific_plm_scores_v2_gpu.tsv"))
    p.add_argument("--reference", type=Path, default=Path("references/HRV_A89_2C_reference_sequence.fasta"))
    p.add_argument("--af1", type=Path, default=Path("/public/home/yukang/HRV Oligomers/hrv_2c_full/fold_hrv_2c_full_model_1.cif"))
    p.add_argument("--af3", type=Path, default=Path("/public/home/yukang/HRV Oligomers/hrv_2c_full/fold_hrv_2c_full_model_3.cif"))
    p.add_argument("--hex1", type=Path, default=Path("/public/home/yukang/HRV Oligomers/HRV_A89_2C_HEXAMER/results_summary/selected_hexamer_01_md_representative.pdb"))
    p.add_argument("--hex2", type=Path, default=Path("/public/home/yukang/HRV Oligomers/HRV_A89_2C_HEXAMER/results_summary/selected_hexamer_02_md_representative.pdb"))
    p.add_argument("--outdir", type=Path, default=Path("results/tag_site_modeling_005"))
    a = p.parse_args()

    a.outdir.mkdir(parents=True, exist_ok=True)
    seq = read_reference_sequence(a.reference)
    v5 = pd.read_csv(a.v5, sep="\t")
    review = pd.read_csv(a.review, sep="\t")
    plm = pd.read_csv(a.plm, sep="\t")
    if len(v5) != 320:
        raise ValueError(f"V5 must have 320 junctions, observed {len(v5)}")
    if len(review) != 33:
        raise ValueError(f"Review set must have 33 rows, observed {len(review)}")

    tags = plm[["tag_form", "tag_sequence", "tag_length"]].drop_duplicates()
    tags = tags.set_index("tag_form").loc[TAG_ORDER].reset_index()
    plm_key = plm.set_index(["a89_junction", "tag_form"])
    v5_key = v5.set_index("junction")

    panel_rows = []
    for _, rr in review.iterrows():
        junction = rr["junction"]
        left = int(junction.split("|")[0])
        full = v5_key.loc[junction]
        for _, tag in tags.iterrows():
            pr = plm_key.loc[(junction, tag["tag_form"])]
            rationale = {
                "negative_control_hard_exclusion": "hard-exclusion negative control for calibration",
                "required_reaudit_control": "required re-audit/control junction from GPU_RECOVERY_004",
                "top_plm_secondary_context": "strong PLM secondary-support row retained despite direct/functional conflict",
                "plm_gpu_review": "PLM-updated conflict-aware review representative",
            }.get(rr["review_role_v2"], rr["review_role_v2"])
            panel_rows.append({
                "construct_id": f"A89_2C_{junction.replace('|','_')}_{tag['tag_form']}",
                "junction": junction,
                "left_resid": left,
                "right_resid": left + 1,
                "left_aa": seq[left - 1],
                "right_aa": seq[left],
                "tag_form": tag["tag_form"],
                "tag_sequence": tag["tag_sequence"],
                "tag_length": int(tag["tag_length"]),
                "review_role_v2": rr["review_role_v2"],
                "panel_inclusion_rationale": rationale,
                "candidate_class_v5_plm_gpu": rr["candidate_class_v5_plm_gpu"],
                "functional_tier": rr["functional_tier"],
                "mapping_class": rr["mapping_class"],
                "strict_structural_pass": rr["strict_structural_pass"],
                "insertion_design": full["insertion_design"],
                "insertion_length_aa": full["insertion_length_aa"],
                "insertion_raw_log2_enrich2": rr["insertion_raw_log2_enrich2"],
                "insertion_direct_class": full["insertion_direct_class"],
                "sub_window_mean": rr["sub_window_mean"],
                "independent_indel_event_lower_bound": rr["independent_indel_event_lower_bound"],
                "plm_percentile_within_tag": pr["plm_percentile_within_tag"],
                "plm_rank_within_tag": pr["plm_rank_within_tag"],
                "plm_delta_mean_pll_insert_minus_wt": pr["plm_delta_mean_pll_insert_minus_wt"],
                "plm_inserted_tag_mean_pll": pr["plm_score_inserted_tag_mean_pll"],
                "best_tag_form": rr["best_tag_form"],
                "worst_tag_form": rr["worst_tag_form"],
                "plm_percentile_mean": rr["plm_percentile_mean"],
                "plm_percentile_min": rr["plm_percentile_min"],
                "plm_percentile_range": rr["plm_percentile_range"],
                "plm_consensus_class": rr["plm_consensus_class"],
                "both_AF_coil": full["both_AF_coil"],
                "min_hex_coil_fraction": full["min_hex_coil_fraction"],
                "min_AF_rSASA": full["min_AF_rSASA"],
                "min_hexamer_mean_rSASA": full["min_hexamer_mean_rSASA"],
                "max_any_chain_burial_fraction": full["max_any_chain_burial_fraction"],
                "min_interprotomer_heavy_atom_A": full["min_interprotomer_heavy_atom_A"],
                "min_mean_pore_radial_A": full["min_mean_pore_radial_A"],
                "min_AF_CA_pLDDT": full["min_AF_CA_pLDDT"],
            })
    panel = pd.DataFrame(panel_rows)
    panel.to_csv("data/tag_site_modeling_panel_v1.tsv", sep="\t", index=False)

    paths = {"af1": a.af1, "af3": a.af3, "hex1": a.hex1, "hex2": a.hex2}
    write_inventory(a.outdir / "environment_and_method_inventory.tsv", paths, "TAG_SITE_MODELING_PARTIALLY_COMPLETE")

    structure = panel[["construct_id", "junction", "tag_form", "tag_length"]].copy()
    structure["method_status"] = "DEFERRED_SOFTWARE"
    structure["structure_prediction_method"] = "ColabFold/AlphaFold-family/ESMFold searched; not available"
    structure["tagged_model_count"] = 0
    structure["wt_reference_structures_available"] = 4
    structure["native_domain_rmsd_A"] = ""
    structure["local_backbone_displacement_A"] = ""
    structure["tag_accessibility"] = ""
    structure["model_convergence"] = ""
    structure["native_2c_confidence"] = ""
    structure["tag_confidence"] = ""
    structure["deferred_reason"] = "No mature local insertion-specific structure-prediction workflow found; no inserted-structure metrics fabricated."
    structure.to_csv("data/tag_site_structure_ensemble_metrics_v1.tsv", sep="\t", index=False)

    loop = panel.copy()
    loop["method_status"] = "COMPLETED_PROXY_ONLY__PRIMARY_LOOP_REMODEL_DEFERRED_SOFTWARE"
    loop["primary_loop_method"] = "Rosetta Remodel/KIC-like workflow searched; not available"
    loop["tag_extended_contour_length_A"] = loop["tag_length"].astype(float) * 3.8
    loop["tag_length_class"] = loop["tag_length"].map(length_class)
    loop["loop_feasibility_class"] = loop.apply(lambda r: loop_proxy(r, int(r["tag_length"])), axis=1)
    loop["closure_success_count"] = ""
    loop["conformer_diversity"] = ""
    loop["local_strain_energy"] = ""
    loop["severe_clash_count"] = ""
    loop["proxy_limit"] = "WT anchor geometry only; not a loop-closure ensemble."
    loop_cols = [
        "construct_id", "junction", "tag_form", "tag_sequence", "tag_length", "method_status",
        "primary_loop_method", "tag_extended_contour_length_A", "tag_length_class",
        "both_AF_coil", "min_hex_coil_fraction", "min_AF_rSASA",
        "min_hexamer_mean_rSASA", "max_any_chain_burial_fraction", "min_AF_CA_pLDDT",
        "loop_feasibility_class", "closure_success_count", "conformer_diversity",
        "local_strain_energy", "severe_clash_count", "proxy_limit",
    ]
    loop[loop_cols].to_csv("data/tag_site_loop_feasibility_v1.tsv", sep="\t", index=False)

    energy = panel[["construct_id", "junction", "tag_form", "tag_length", "functional_tier", "candidate_class_v5_plm_gpu"]].copy()
    energy["method_status"] = "DEFERRED_SOFTWARE"
    energy["energy_method"] = "FoldX/Rosetta/local-frustration searched; not available"
    energy["local_delta_energy"] = ""
    energy["interface_delta_energy"] = ""
    energy["frustration_change"] = ""
    energy["deferred_reason"] = "No mature energy/frustration workflow available for inserted models; WT-only APBS/Amber/Gromacs modules do not answer insertion energy without models."
    energy.to_csv("data/tag_site_energy_context_v1.tsv", sep="\t", index=False)

    contact_junction = structure_contact_context(paths, sorted(review["junction"].tolist(), key=lambda x: int(x.split("|")[0])))
    contact_junction["network_context_class"] = contact_junction.apply(contact_class, axis=1)
    contact = panel.merge(contact_junction, on="junction", how="left")
    contact["method_status"] = "COMPLETED_WT_ANCHOR_NETWORK__TAGGED_CONTACT_DELTA_DEFERRED"
    contact["tagged_contact_map_delta"] = ""
    contact["method_limit"] = "WT residue-contact context from CA maps; true WT-vs-tagged network perturbation requires inserted models."
    contact_cols = [
        "construct_id", "junction", "tag_form", "tag_length", "method_status",
        "structures_evaluated", "mean_local_ca_degree_8A", "max_local_ca_degree_8A",
        "mean_cross_chain_ca_degree_8A", "max_cross_chain_ca_degree_8A",
        "mean_flanking_ca_distance_A", "network_context_class",
        "tagged_contact_map_delta", "method_limit",
    ]
    contact[contact_cols].to_csv("data/tag_site_contact_network_v1.tsv", sep="\t", index=False)

    hexm = panel.copy()
    hexm["method_status"] = "COMPLETED_WT_HEXAMER_CONTEXT_PROXY"
    hexm["hexamer_models"] = "selected_hexamer_01_md_representative;selected_hexamer_02_md_representative"
    hexm["tag_extended_contour_length_A"] = hexm["tag_length"].astype(float) * 3.8
    hexm["tag_length_class"] = hexm["tag_length"].map(length_class)
    hexm["neighbor_reach_proxy"] = np.where(
        hexm["tag_extended_contour_length_A"].astype(float) >= hexm["min_interprotomer_heavy_atom_A"].astype(float),
        "extended_tag_can_geometrically_reach_neighbor",
        "neighbor_beyond_extended_tag_contour",
    )
    hexm["hexamer_context_class"] = hexm.apply(lambda r: hexamer_class(r, int(r["tag_length"])), axis=1)
    hexm["method_limit"] = "Existing no-membrane/no-RNA WT hexamers are context hypotheses; inserted hexamers were not predicted."
    hex_cols = [
        "construct_id", "junction", "tag_form", "tag_length", "method_status", "hexamer_models",
        "min_interprotomer_heavy_atom_A", "max_any_chain_burial_fraction",
        "min_hexamer_mean_rSASA", "min_mean_pore_radial_A",
        "tag_extended_contour_length_A", "tag_length_class", "neighbor_reach_proxy",
        "hexamer_context_class", "method_limit",
    ]
    hexm[hex_cols].to_csv("data/tag_site_hexamer_context_v1.tsv", sep="\t", index=False)

    integrated = panel.merge(loop[["construct_id", "loop_feasibility_class"]], on="construct_id")
    integrated = integrated.merge(hexm[["construct_id", "hexamer_context_class", "neighbor_reach_proxy"]], on="construct_id")
    integrated = integrated.merge(contact[["construct_id", "network_context_class"]], on="construct_id")
    integrated["structure_ensemble_status"] = "DEFERRED_SOFTWARE"
    integrated["energy_frustration_status"] = "DEFERRED_SOFTWARE"
    integrated["direct_homolog_evidence"] = integrated["insertion_direct_class"]
    integrated["unresolved_conflicts"] = integrated.apply(
        lambda r: ";".join([
            x for x in [
                "direct_homolog_insertion_unfavorable" if "deleterious" in str(r["insertion_direct_class"]) else "",
                "functional_tier_" + str(r["functional_tier"]) if r["functional_tier"] != "UNRESOLVED" else "",
                "structure_prediction_deferred",
                "energy_deferred",
                "tag_specific_plm_disagreement" if fnum(r["plm_percentile_range"], 0.0) >= 0.35 else "",
            ] if x
        ]),
        axis=1,
    )
    integrated["integrated_perturbation_class"] = integrated.apply(qualitative_integration, axis=1)
    integrated_cols = [
        "construct_id", "junction", "tag_form", "tag_sequence", "tag_length", "review_role_v2",
        "candidate_class_v5_plm_gpu", "functional_tier", "mapping_class", "strict_structural_pass",
        "direct_homolog_evidence", "insertion_raw_log2_enrich2", "sub_window_mean",
        "independent_indel_event_lower_bound", "plm_percentile_within_tag",
        "plm_delta_mean_pll_insert_minus_wt", "plm_consensus_class",
        "loop_feasibility_class", "hexamer_context_class", "network_context_class",
        "structure_ensemble_status", "energy_frustration_status", "neighbor_reach_proxy",
        "integrated_perturbation_class", "unresolved_conflicts",
    ]
    integrated[integrated_cols].to_csv("data/tag_site_integrated_perturbation_v1.tsv", sep="\t", index=False)

    robust = integrated.copy()
    support_cols = []
    disfavor_cols = []
    for _, r in robust.iterrows():
        support = []
        disfavor = []
        if fnum(r["plm_percentile_within_tag"], 0.0) >= 0.75:
            support.append("tag_specific_plm")
        elif fnum(r["plm_percentile_within_tag"], 0.0) < 0.25:
            disfavor.append("tag_specific_plm")
        if str(r["loop_feasibility_class"]) == "LOOP_PROXY_RELATIVELY_FAVORABLE":
            support.append("loop_proxy")
        elif str(r["loop_feasibility_class"]) == "LOOP_PROXY_UNFAVORABLE":
            disfavor.append("loop_proxy")
        if str(r["hexamer_context_class"]) == "OLIGOMER_CONTEXT_RELATIVELY_FAVORABLE":
            support.append("oligomer_context")
        elif str(r["hexamer_context_class"]) == "OLIGOMER_CONTEXT_UNFAVORABLE":
            disfavor.append("oligomer_context")
        if str(r["network_context_class"]).endswith("LOWER_CONSTRAINT"):
            support.append("contact_network")
        elif str(r["network_context_class"]).endswith("CONSTRAINED"):
            disfavor.append("contact_network")
        if "deleterious" in str(r["direct_homolog_evidence"]):
            disfavor.append("direct_homolog_insertion")
        if r["functional_tier"] in {"EXCLUDE", "HIGH_RISK"}:
            disfavor.append("functional_context")
        support_cols.append(";".join(support) if support else "none")
        disfavor_cols.append(";".join(disfavor) if disfavor else "none")
    robust["completed_method_count"] = 4
    robust["deferred_primary_method_count"] = 3
    robust["supporting_dimensions"] = support_cols
    robust["disfavoring_dimensions"] = disfavor_cols
    robust["robustness_class"] = robust.apply(
        lambda r: "CONSISTENTLY_DISFAVORED" if r["supporting_dimensions"] == "none" and r["disfavoring_dimensions"] != "none"
        else ("MULTI_METHOD_RELATIVE_SUPPORT_WITH_DIRECT_CONFLICT" if r["integrated_perturbation_class"] == "RELATIVELY_LOWER_PERTURBATION__DIRECT_EVIDENCE_CONFLICT"
              else "METHOD_DEPENDENT_OR_INCOMPLETE"),
        axis=1,
    )
    robust_cols = [
        "construct_id", "junction", "tag_form", "completed_method_count", "deferred_primary_method_count",
        "supporting_dimensions", "disfavoring_dimensions", "robustness_class",
        "integrated_perturbation_class", "unresolved_conflicts",
    ]
    robust[robust_cols].to_csv(a.outdir / "cross_method_robustness.tsv", sep="\t", index=False)

    summary = []
    summary.append({"metric": "v5_junction_rows", "value": len(v5)})
    summary.append({"metric": "review_junction_rows", "value": len(review)})
    summary.append({"metric": "modeled_construct_rows", "value": len(panel)})
    summary.append({"metric": "tag_forms", "value": ";".join(TAG_ORDER)})
    summary.append({"metric": "final_state", "value": "TAG_SITE_MODELING_PARTIALLY_COMPLETE"})
    pd.DataFrame(summary).to_csv(a.outdir / "summary_qc.tsv", sep="\t", index=False)


if __name__ == "__main__":
    main()
