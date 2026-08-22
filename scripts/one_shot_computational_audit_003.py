#!/usr/bin/env python3
"""CPU stages for ONE_SHOT_COMPUTATIONAL_AUDIT_003."""

from __future__ import annotations

import argparse
import csv
import math
import re
import subprocess
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
import pandas as pd
from Bio import Phylo, SeqIO


TAGS = {
    "MAP8": "GDGMVPPG",
    "HA": "YPYDVPDYA",
    "G196_minimal": "DLVPR",
    "G196_practical_GS": "GSDLVPRGS",
}

FOCAL = {"287|288", "288|289", "289|290", "290|291", "248|249", "256|257", "223|224", "245|246", "250|251"}


def split_positions(text: object) -> list[int]:
    if pd.isna(text) or not str(text):
        return []
    out: list[int] = []
    for part in str(text).split(";"):
        for token in part.split(","):
            token = token.strip()
            if not token:
                continue
            if "-" in token:
                a, b = token.split("-", 1)
                out.extend(range(int(a), int(b) + 1))
            else:
                out.append(int(token))
    return sorted(set(out))


def fmt_float(value: float | None, digits: int = 6) -> str:
    if value is None or pd.isna(value):
        return ""
    return f"{float(value):.{digits}f}"


def summarize_scores(scores: pd.Series) -> dict[str, object]:
    scores = pd.to_numeric(scores, errors="coerce").dropna()
    if scores.empty:
        return {
            "n": 0,
            "mean": np.nan,
            "median": np.nan,
            "max": np.nan,
            "min": np.nan,
            "frac_gt0": np.nan,
            "frac_ge_minus1": np.nan,
        }
    return {
        "n": int(scores.size),
        "mean": float(scores.mean()),
        "median": float(scores.median()),
        "max": float(scores.max()),
        "min": float(scores.min()),
        "frac_gt0": float((scores > 0).mean()),
        "frac_ge_minus1": float((scores >= -1).mean()),
    }


def make_substitution_table(raw_dir: Path, direct_path: Path, out: Path, qc: Path) -> pd.DataFrame:
    dms = pd.read_csv(raw_dir / "Fullproteome_P2_DMS_Enrich2_long.csv")
    dms = dms[(dms["position"] > 1111) & (dms["position"] < 1441)].copy()
    dms["ev71_2c_position"] = dms["position"] - 1111
    direct = pd.read_csv(direct_path, sep="\t")
    per_pos = {int(pos): summarize_scores(g["score"]) for pos, g in dms.groupby("ev71_2c_position")}
    rows = []
    for _, row in direct.iterrows():
        source_lefts = split_positions(row["eva71_source_left_positions"])
        flank_positions = sorted({p for left in source_lefts for p in (left, left + 1) if 1 <= p <= 329})
        if source_lefts:
            lo = max(1, min(source_lefts) - 2)
            hi = min(329, max(source_lefts) + 3)
            window_positions = list(range(lo, hi + 1))
        else:
            lo = hi = None
            window_positions = []
        flank_scores = dms[dms["ev71_2c_position"].isin(flank_positions)]["score"]
        window_scores = dms[dms["ev71_2c_position"].isin(window_positions)]["score"]
        flank = summarize_scores(flank_scores)
        window = summarize_scores(window_scores)
        left_summary = per_pos.get(source_lefts[0], {}) if len(source_lefts) == 1 else {}
        right_summary = per_pos.get(source_lefts[0] + 1, {}) if len(source_lefts) == 1 else {}
        rows.append(
            {
                "a89_junction": row["a89_junction"],
                "a89_left_residue": row["a89_left_residue"],
                "a89_right_residue": row["a89_right_residue"],
                "mapping_class": row["mapping_class"],
                "mapping_confidence": row["mapping_confidence"],
                "eva71_source_left_positions": row["eva71_source_left_positions"],
                "eva71_substitution_flank_positions": ",".join(map(str, flank_positions)),
                "eva71_substitution_window_positions": "" if lo is None else f"{lo}-{hi}",
                "sub_left_mean": left_summary.get("mean", np.nan),
                "sub_left_max": left_summary.get("max", np.nan),
                "sub_left_frac_gt0": left_summary.get("frac_gt0", np.nan),
                "sub_right_mean": right_summary.get("mean", np.nan),
                "sub_right_max": right_summary.get("max", np.nan),
                "sub_right_frac_gt0": right_summary.get("frac_gt0", np.nan),
                "sub_flank_n_scores": flank["n"],
                "sub_flank_mean": flank["mean"],
                "sub_flank_median": flank["median"],
                "sub_flank_max": flank["max"],
                "sub_flank_frac_gt0": flank["frac_gt0"],
                "sub_window_n_scores": window["n"],
                "sub_window_mean": window["mean"],
                "sub_window_median": window["median"],
                "sub_window_max": window["max"],
                "sub_window_frac_gt0": window["frac_gt0"],
                "substitution_mapping_note": "exact flank summaries" if len(source_lefts) == 1 else "ambiguous source positions summarized jointly",
            }
        )
    sub = pd.DataFrame(rows)
    if len(sub) != 320:
        raise ValueError(f"substitution rows != 320: {len(sub)}")
    sub.to_csv(out, sep="\t", index=False)
    qc_rows = [
        ("ev71_2c_substitution_rows", len(dms)),
        ("a89_junction_rows", len(sub)),
        ("exact_aligned_rows", int((sub["mapping_class"] == "exact_aligned").sum())),
        ("ambiguous_rows", int((sub["mapping_class"] == "ambiguous").sum())),
        ("rows_with_flank_scores", int((sub["sub_flank_n_scores"] > 0).sum())),
        ("rows_with_window_scores", int((sub["sub_window_n_scores"] > 0).sum())),
    ]
    pd.DataFrame(qc_rows, columns=["metric", "value"]).to_csv(qc, sep="\t", index=False)
    return sub


def sanitize_fasta_for_tree(in_fasta: Path, out_fasta: Path, name_map_out: Path) -> dict[str, str]:
    mapping = {}
    records = []
    for i, rec in enumerate(SeqIO.parse(str(in_fasta), "fasta"), start=1):
        sid = f"S{i:03d}"
        mapping[sid] = rec.id
        rec.id = sid
        rec.name = sid
        rec.description = sid
        records.append(rec)
    SeqIO.write(records, str(out_fasta), "fasta")
    pd.DataFrame([{"tree_id": k, "sequence_id": v} for k, v in mapping.items()]).to_csv(name_map_out, sep="\t", index=False)
    return mapping


def run_fasttree(fasttree: Path, alignment: Path, tree_out: Path, log_out: Path) -> None:
    cmd = [str(fasttree), "-wag", str(alignment)]
    proc = subprocess.run(cmd, check=True, text=True, capture_output=True)
    tree_out.write_text(proc.stdout)
    log_out.write_text(proc.stderr)


def fitch_count(tree, tip_states: dict[str, int | None]) -> tuple[int, int, int]:
    changes = 0
    uncertain_nodes = 0

    def post(clade):
        nonlocal changes, uncertain_nodes
        if clade.is_terminal():
            state = tip_states.get(clade.name)
            if state is None:
                clade._states = {0, 1}
            else:
                clade._states = {int(state)}
            return clade._states
        child_sets = [post(c) for c in clade.clades]
        states = child_sets[0].copy()
        for s in child_sets[1:]:
            inter = states & s
            if inter:
                states = inter
            else:
                states = states | s
                changes += 1
        if len(states) > 1:
            uncertain_nodes += 1
        clade._states = states
        return states

    post(tree.root)
    root_uncertain = int(len(tree.root._states) > 1)
    return changes, uncertain_nodes, root_uncertain


def make_indel_event_table(
    alignment: Path,
    a89_mapping: Path,
    fasttree: Path,
    sanitized_fasta: Path,
    name_map: Path,
    tree_out: Path,
    tree_log: Path,
    out: Path,
    qc: Path,
) -> pd.DataFrame:
    mapping = sanitize_fasta_for_tree(alignment, sanitized_fasta, name_map)
    if not tree_out.exists():
        run_fasttree(fasttree, sanitized_fasta, tree_out, tree_log)
    tree = Phylo.read(str(tree_out), "newick")
    records = {rec.id: str(rec.seq) for rec in SeqIO.parse(str(sanitized_fasta), "fasta")}
    amap = pd.read_csv(a89_mapping, sep="\t")
    col_by_a89 = dict(zip(amap["a89_residue"], amap["alignment_column_1based"]))
    rows = []
    for left in range(1, 321):
        right = left + 1
        left_col = int(col_by_a89[left]) - 1
        right_col = int(col_by_a89[right]) - 1
        between_cols = list(range(left_col + 1, right_col))
        window_res = list(range(max(1, left - 2), min(321, right + 2) + 1))
        window_cols = [int(col_by_a89[r]) - 1 for r in window_res]
        insertion_states = {}
        deletion_states = {}
        for sid, seq in records.items():
            insertion_states[sid] = int(any(seq[c] != "-" for c in between_cols)) if between_cols else 0
            deletion_states[sid] = int(any(seq[c] == "-" for c in window_cols))
        ins_changes, ins_uncertain, ins_root_uncertain = fitch_count(tree, insertion_states)
        del_changes, del_uncertain, del_root_uncertain = fitch_count(tree, deletion_states)
        rows.append(
            {
                "junction": f"{left}|{right}",
                "a89_left_residue": left,
                "a89_right_residue": right,
                "natural_insertion_tip_count": int(sum(insertion_states.values())),
                "natural_insertion_tip_frequency": sum(insertion_states.values()) / len(insertion_states),
                "natural_insertion_parsimony_change_count": ins_changes,
                "natural_insertion_uncertain_internal_nodes": ins_uncertain,
                "natural_insertion_root_state_uncertain": bool(ins_root_uncertain),
                "local_deletion_tip_count": int(sum(deletion_states.values())),
                "local_deletion_tip_frequency": sum(deletion_states.values()) / len(deletion_states),
                "local_deletion_parsimony_change_count": del_changes,
                "local_deletion_uncertain_internal_nodes": del_uncertain,
                "local_deletion_root_state_uncertain": bool(del_root_uncertain),
                "independent_indel_event_lower_bound": max(ins_changes, del_changes),
                "independent_indel_event_uncertainty": "uncertain" if (ins_uncertain or del_uncertain) else "resolved_by_parsimony",
            }
        )
    events = pd.DataFrame(rows)
    events.to_csv(out, sep="\t", index=False)
    qc_rows = [
        ("tree_method", "FastTree -wag"),
        ("tree_tip_count", len(records)),
        ("a89_junction_rows", len(events)),
        ("junctions_with_insertion_tip_presence", int((events["natural_insertion_tip_count"] > 0).sum())),
        ("junctions_with_insertion_parsimony_changes", int((events["natural_insertion_parsimony_change_count"] > 0).sum())),
        ("junctions_with_local_deletion_tip_presence", int((events["local_deletion_tip_count"] > 0).sum())),
        ("junctions_with_local_deletion_parsimony_changes", int((events["local_deletion_parsimony_change_count"] > 0).sum())),
    ]
    pd.DataFrame(qc_rows, columns=["metric", "value"]).to_csv(qc, sep="\t", index=False)
    return events


def normalize_good(df: pd.DataFrame, col: str, higher_is_better: bool = True) -> pd.Series:
    x = pd.to_numeric(df[col], errors="coerce")
    if not higher_is_better:
        x = -x
    if x.notna().sum() == 0:
        return pd.Series(0.5, index=df.index)
    lo, hi = x.min(), x.max()
    if math.isclose(float(lo), float(hi)):
        return pd.Series(0.5, index=df.index)
    return (x - lo) / (hi - lo)


def nondominated(mask_df: pd.DataFrame, metrics: list[str]) -> pd.Series:
    vals = mask_df[metrics].to_numpy(float)
    n = len(mask_df)
    dom = np.zeros(n, dtype=bool)
    for i in range(n):
        if dom[i]:
            continue
        better_or_equal = vals >= vals[i]
        strictly_better = vals > vals[i]
        dominates_i = better_or_equal.all(axis=1) & strictly_better.any(axis=1)
        dominates_i[i] = False
        if dominates_i.any():
            dom[i] = True
    return pd.Series(~dom, index=mask_df.index)


def make_pareto_and_v4(v3: Path, sub: pd.DataFrame, events: pd.DataFrame, out_v4: Path, frontier_out: Path, sensitivity_out: Path) -> pd.DataFrame:
    base = pd.read_csv(v3, sep="\t")
    v4 = base.merge(sub, left_on="junction", right_on="a89_junction", how="left", suffixes=("", "_sub"), validate="one_to_one")
    v4 = v4.merge(events, on="junction", how="left", validate="one_to_one")
    v4["hard_functional_exclusion"] = v4["functional_tier"].eq("EXCLUDE")
    v4["direct_insertion_penalty_class"] = v4["insertion_direct_class"]
    v4["old_conflict_control"] = np.where(
        v4["junction"].isin(["287|288", "288|289", "289|290", "290|291"]),
        "STRUCTURE_EVOLUTION_FAVORED__DIRECT_HOMOLOG_CONFLICT",
        np.where(v4["junction"].isin(["248|249", "256|257"]), "HISTORICAL_INSERTION_SUPPORT__MODERN_CONFLICT_CONTROL", ""),
    )
    scored = pd.DataFrame(index=v4.index)
    scored["af_exposure"] = normalize_good(v4, "min_AF_rSASA", True)
    scored["hex_exposure"] = normalize_good(v4, "min_hexamer_mean_rSASA", True)
    scored["low_burial"] = normalize_good(v4, "max_any_chain_burial_fraction", False)
    scored["interface_distance"] = normalize_good(v4, "min_interprotomer_heavy_atom_A", True)
    scored["pore_radial"] = normalize_good(v4, "min_mean_pore_radial_A", True)
    scored["coil_context"] = normalize_good(v4, "min_hex_coil_fraction", True)
    scored["direct_insertion_relative"] = normalize_good(v4, "insertion_relative_fitness_2pow_score", True)
    scored["substitution_window_mean"] = normalize_good(v4, "sub_window_mean", True)
    scored["substitution_window_max"] = normalize_good(v4, "sub_window_max", True)
    scored["evolution_variability"] = normalize_good(v4, "hrvA_type_weighted_window_mean_entropy", True)
    scored["evolution_low_identity"] = normalize_good(v4, "hrvA_type_weighted_window_mean_identity", False)
    scored["independent_indel_events"] = normalize_good(v4, "independent_indel_event_lower_bound", True)
    for col in scored.columns:
        v4[f"pareto_metric_{col}"] = scored[col]

    subsets = {
        "structure_only": ["af_exposure", "hex_exposure", "low_burial", "interface_distance", "pore_radial", "coil_context"],
        "structure_plus_direct": ["af_exposure", "hex_exposure", "low_burial", "interface_distance", "pore_radial", "coil_context", "direct_insertion_relative"],
        "no_conservation": ["af_exposure", "hex_exposure", "low_burial", "interface_distance", "pore_radial", "coil_context", "direct_insertion_relative", "substitution_window_mean"],
        "no_substitution": ["af_exposure", "hex_exposure", "low_burial", "interface_distance", "pore_radial", "coil_context", "direct_insertion_relative", "evolution_variability", "independent_indel_events"],
        "full": ["af_exposure", "hex_exposure", "low_burial", "interface_distance", "pore_radial", "coil_context", "direct_insertion_relative", "substitution_window_mean", "evolution_variability", "independent_indel_events"],
    }
    eligible = ~v4["hard_functional_exclusion"]
    sens_rows = []
    membership = defaultdict(int)
    for name, cols in subsets.items():
        nd = pd.Series(False, index=v4.index)
        nd.loc[eligible] = nondominated(scored.loc[eligible], cols)
        v4[f"pareto_{name}"] = nd
        for j in v4.loc[nd, "junction"]:
            membership[j] += 1
        sens_rows.append({"subset": name, "metrics": ";".join(cols), "eligible_rows": int(eligible.sum()), "pareto_rows": int(nd.sum())})
    v4["pareto_reviewable_subset_count"] = v4["junction"].map(membership).fillna(0).astype(int)
    v4["pareto_reviewable_any"] = v4["pareto_reviewable_subset_count"] > 0

    def review_class(row: pd.Series) -> str:
        if row["hard_functional_exclusion"]:
            return "hard_excluded"
        if row["mapping_class"] != "exact_aligned":
            return "mapping_uncertain"
        if row["junction"] in FOCAL:
            return "conflict_control"
        if row["pareto_reviewable_subset_count"] >= 3:
            return "pareto_reviewable_direct_conflicted"
        if row["pareto_reviewable_subset_count"] > 0:
            return "weak_pareto_reviewable_direct_conflicted"
        if row["insertion_direct_class"] == "direct_insert_strongly_deleterious":
            return "direct_homolog_strongly_unfavorable"
        return "unresolved"

    v4["method_hardening_candidate_class"] = v4.apply(review_class, axis=1)
    v4["plm_status"] = "blocked_software_unavailable"
    for tag in TAGS:
        v4[f"plm_delta_{tag}"] = np.nan
    v4.to_csv(out_v4, sep="\t", index=False)

    frontier_cols = [
        "junction",
        "functional_tier",
        "hard_functional_exclusion",
        "strict_structural_pass",
        "mapping_class",
        "insertion_raw_log2_enrich2",
        "sub_window_mean",
        "independent_indel_event_lower_bound",
        "pareto_reviewable_subset_count",
        "method_hardening_candidate_class",
        "old_conflict_control",
    ] + [f"pareto_{k}" for k in subsets]
    v4[frontier_cols].to_csv(frontier_out, sep="\t", index=False)
    pd.DataFrame(sens_rows).to_csv(sensitivity_out, sep="\t", index=False)
    return v4


def make_plm_blocker_tables(a89_fasta: Path, scores_out: Path, qc_out: Path) -> None:
    wt = str(next(SeqIO.parse(str(a89_fasta), "fasta")).seq)
    rows = []
    for tag_name, tag_seq in TAGS.items():
        for left in range(1, 321):
            rows.append(
                {
                    "tag_form": tag_name,
                    "tag_sequence": tag_seq,
                    "tag_length": len(tag_seq),
                    "a89_junction": f"{left}|{left+1}",
                    "inserted_sequence_length": len(wt) + len(tag_seq),
                    "plm_model": "",
                    "plm_score_wt": "",
                    "plm_score_inserted": "",
                    "plm_delta_insert_minus_wt": "",
                    "plm_status": "blocked_software_unavailable",
                    "blocker": "No visible GPU/torch/transformers/esm; torch-transformers install rejected by platform usage-limit escalation.",
                }
            )
    pd.DataFrame(rows).to_csv(scores_out, sep="\t", index=False)
    qc = pd.DataFrame(
        [
            ("tag_forms", len(TAGS)),
            ("planned_rows", len(rows)),
            ("completed_plm_rows", 0),
            ("plm_status", "blocked_software_unavailable"),
        ],
        columns=["metric", "value"],
    )
    qc.to_csv(qc_out, sep="\t", index=False)


def make_robustness(v4: pd.DataFrame, robust_out: Path, negative_out: Path) -> None:
    subset_cols = [c for c in v4.columns if c.startswith("pareto_") and c not in {"pareto_reviewable_any"} and c != "pareto_reviewable_subset_count"]
    rows = []
    for _, row in v4.iterrows():
        rows.append(
            {
                "junction": row["junction"],
                "functional_tier": row["functional_tier"],
                "strict_structural_pass": row["strict_structural_pass"],
                "mapping_class": row["mapping_class"],
                "pareto_reviewable_subset_count": row["pareto_reviewable_subset_count"],
                "pareto_reviewable_fraction": row["pareto_reviewable_subset_count"] / max(1, len(subset_cols)),
                "method_hardening_candidate_class": row["method_hardening_candidate_class"],
                "direct_insertion_class": row["insertion_direct_class"],
                "old_conflict_control": row["old_conflict_control"],
            }
        )
    pd.DataFrame(rows).to_csv(robust_out, sep="\t", index=False)
    neg = v4[
        v4["functional_tier"].eq("EXCLUDE")
        | v4["functional_reasons"].fillna("").str.contains("Walker|motif|9A5|Zn|Cys|RNA", case=False, regex=True)
        | v4["junction"].isin(["155|156", "174|175", "216|217", "287|288", "288|289", "289|290", "290|291", "248|249", "256|257"])
    ].copy()
    neg["negative_control_audit_flag"] = np.where(
        neg["method_hardening_candidate_class"].str.contains("pareto", na=False),
        "pareto_flagged_despite_high_risk_context_review_required",
        "not_promoted_or_retained_only_as_conflict_control",
    )
    neg.to_csv(negative_out, sep="\t", index=False)


def make_consensus_blocker(scores_out: Path, corr_out: Path, doc_table_out: Path) -> None:
    pd.DataFrame(
        [{"tag_form": tag, "tag_sequence": seq, "consensus_status": "blocked_no_plm_scores"} for tag, seq in TAGS.items()]
    ).to_csv(scores_out, sep="\t", index=False)
    pd.DataFrame(
        [{"comparison": "all_tag_pairs", "status": "blocked_no_plm_scores", "spearman_r": "", "pearson_r": ""}]
    ).to_csv(corr_out, sep="\t", index=False)
    doc_table_out.write_text("tag_form\ttag_sequence\tstatus\n" + "\n".join(f"{k}\t{v}\tblocked_no_plm_scores" for k, v in TAGS.items()) + "\n")


def make_review_set(v4: pd.DataFrame, out: Path) -> pd.DataFrame:
    selected = {
        "155|156",
        "203|204",
        "216|217",
        "223|224",
        "224|225",
        "245|246",
        "248|249",
        "250|251",
        "256|257",
        "287|288",
        "288|289",
        "289|290",
        "290|291",
    }
    candidates = v4[
        (~v4["hard_functional_exclusion"])
        & (~v4["junction"].isin(selected))
        & (v4["mapping_class"] == "exact_aligned")
        & (v4["pareto_reviewable_subset_count"] >= 3)
    ].copy()
    candidates["_functional_priority"] = candidates["functional_tier"].map({"CORE_CAUTION": 0, "HIGH_RISK": 1}).fillna(2)
    candidates["_insert_score"] = pd.to_numeric(candidates["insertion_raw_log2_enrich2"], errors="coerce")
    picked = candidates.sort_values(
        ["_functional_priority", "pareto_reviewable_subset_count", "_insert_score"],
        ascending=[True, False, False],
    )["junction"].head(4)
    selected.update(picked)
    selected = {j for j in selected if j in set(v4["junction"])}
    rows = []
    for _, row in v4[v4["junction"].isin(sorted(selected, key=lambda x: int(x.split("|")[0])))].iterrows():
        role = "pareto_reviewable_direct_conflicted" if row["pareto_reviewable_subset_count"] >= 3 else row["method_hardening_candidate_class"]
        if row["junction"] in {"155|156", "216|217"}:
            role = "negative_control_hard_exclusion"
        if row["junction"] in {"223|224", "245|246", "250|251"}:
            role = "near_miss_or_mapping_uncertain_control"
        if row["junction"] in {"203|204", "224|225"}:
            role = "least_deleterious_direct_insertion_outside_strict_control"
        if row["junction"] in {"287|288", "288|289", "289|290", "290|291"}:
            role = "old_strict_cluster_conflict_control"
        if row["junction"] in {"248|249", "256|257"}:
            role = "historical_conflict_control"
        rows.append(
            {
                "junction": row["junction"],
                "review_role": role,
                "functional_tier": row["functional_tier"],
                "mapping_class": row["mapping_class"],
                "strict_structural_pass": row["strict_structural_pass"],
                "pareto_reviewable_subset_count": row["pareto_reviewable_subset_count"],
                "insertion_raw_log2_enrich2": row["insertion_raw_log2_enrich2"],
                "sub_window_mean": row["sub_window_mean"],
                "independent_indel_event_lower_bound": row["independent_indel_event_lower_bound"],
                "plm_status": row["plm_status"],
                "rationale": "Retained for computational review only; not an experimental recommendation.",
            }
        )
    review = pd.DataFrame(rows)
    review.to_csv(out, sep="\t", index=False)
    return review


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--env-python", default=".tools/envs/hrv2c-one-shot/bin/python")
    args = ap.parse_args()
    root = Path(".")
    mh = root / "results/method_hardening_002"
    os3 = root / "results/one_shot_003"
    for p in [mh, os3, root / "data/plm_sequences_v1"]:
        p.mkdir(parents=True, exist_ok=True)
    sub = make_substitution_table(
        root / "data/raw/direct_indel_001",
        root / "data/evA71_2C_direct_indel_to_A89_v1.tsv",
        root / "data/evA71_2C_substitution_tolerance_to_A89_v1.tsv",
        mh / "substitution_mapping_qc.tsv",
    )
    events = make_indel_event_table(
        root / "data/hrvA_2C_alignment_v2.fasta",
        root / "data/hrvA_2C_alignment_a89_mapping_v2.tsv",
        root / ".tools/envs/hrv2c-one-shot/bin/FastTree",
        root / "data/hrvA_2C_alignment_v2_sanitized_for_tree.fasta",
        root / "data/hrvA_2C_tree_name_map_v1.tsv",
        root / "data/hrvA_2C_fasttree_v1.nwk",
        mh / "phylogeny_fasttree_v1.txt",
        root / "data/hrvA_independent_indel_events_v1.tsv",
        mh / "phylogeny_qc.tsv",
    )
    v4 = make_pareto_and_v4(
        root / "data/candidate_junctions_v3_direct_indel.tsv",
        sub,
        events,
        root / "data/candidate_junctions_v4_method_hardening.tsv",
        root / "data/pareto_junction_frontier_v1.tsv",
        mh / "pareto_sensitivity.tsv",
    )
    make_plm_blocker_tables(
        root / "references/HRV_A89_2C_reference_sequence.fasta",
        root / "data/tag_specific_plm_scores_v1.tsv",
        mh / "plm_qc.tsv",
    )
    make_robustness(v4, os3 / "ranking_robustness.tsv", os3 / "negative_control_audit.tsv")
    make_consensus_blocker(root / "data/tag_specific_consensus_v1.tsv", os3 / "tag_landscape_correlations.tsv", os3 / "tag_forms_planned.tsv")
    make_review_set(v4, root / "data/computational_review_set_v1.tsv")


if __name__ == "__main__":
    main()
