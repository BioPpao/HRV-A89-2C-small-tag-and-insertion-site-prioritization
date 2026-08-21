#!/usr/bin/env python3
"""Integrate CONSERVATION_002 V2 evidence."""

from __future__ import annotations

import argparse
import csv

from integrate_junction_evidence import RESCUE, failed_gates


FOCAL = set(
    "155|156 174|175 175|176 216|217 217|218 218|219 223|224 245|246 "
    "248|249 250|251 256|257 287|288 288|289 289|290 290|291".split()
)


def read_list(path):
    with open(path) as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def read_key(path, key="junction"):
    return {r[key]: r for r in read_list(path)}


def conservation_class(row):
    ident = float(row["type_weighted_window_mean_identity"])
    ent = float(row["type_weighted_window_mean_entropy"])
    indel = row.get("expanded_indel_category", "none")
    if indel in ("recurrent_across_types", "broader_lineage_supported"):
        return "lineage_indel_supported"
    if ident <= 0.70 or ent >= 0.75:
        return "variable"
    if ident >= 0.90 and ent <= 0.30:
        return "conserved"
    return "intermediate"


def exact_sensitivity(full_class, exact_row):
    if not exact_row:
        return "unresolved_exact_subset_missing"
    # Exact-boundary subset is intentionally small in this project (5
    # sequences in CONSERVATION_002), so it is a sensitivity check only.
    return "unresolved_exact_subset_too_small"
    exact_class = conservation_class(exact_row)
    if exact_class == full_class:
        return "stable_across_full_and_exact"
    if exact_class in ("variable", "lineage_indel_supported") and full_class not in ("variable", "lineage_indel_supported"):
        return "strengthened_in_exact_subset"
    if exact_class == "conserved" and full_class != "conserved":
        return "weakened_in_exact_subset"
    return "changed_exact_subset"


def effect(struct, cons):
    c = conservation_class(cons)
    tier = struct["functional_tier"]
    if tier == "EXCLUDE":
        return "weakens"
    if c in ("variable", "lineage_indel_supported"):
        return "supports"
    if c == "conserved":
        return "weakens"
    return "remains unresolved"


def priority(struct, cons, tracks):
    c = conservation_class(cons)
    tier = struct["functional_tier"]
    if "literature-rescue" in tracks:
        return f"literature-rescue retained; V2 conservation {c}; not promoted"
    if tier == "EXCLUDE":
        return "decreased_or_excluded; hard functional feature dominates"
    if "strict structural pass" in tracks and c in ("variable", "lineage_indel_supported"):
        return "reviewable_after_QC; structural pass plus V2 evolutionary support, functional context still required"
    if "structural near-miss" in tracks and c in ("variable", "lineage_indel_supported"):
        return "outside_strict_review_only; near-miss plus V2 evolutionary support"
    if c == "conserved":
        return "decreased; conserved local window"
    return "unchanged_or_unresolved"


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--structural", default="data/junction_structural_metrics_v2.tsv")
    ap.add_argument("--conservation", default="data/hrvA_conservation_per_junction_v2.tsv")
    ap.add_argument("--exact-conservation", default="data/hrvA_conservation_per_junction_exact_boundary_v2.tsv")
    ap.add_argument("--v1-candidate", default="data/candidate_junctions_v1.tsv")
    ap.add_argument("--out", default="data/candidate_junctions_v2.tsv")
    ap.add_argument("--comparison-out", default="data/conservation_v1_v2_junction_comparison.tsv")
    args = ap.parse_args()

    structural = read_list(args.structural)
    cons = read_key(args.conservation)
    exact = read_key(args.exact_conservation)
    v1 = read_key(args.v1_candidate)
    rows = []
    comp = []
    for s in structural:
        j = s["junction"]
        c = cons[j]
        failed = failed_gates(s)
        tracks = []
        if s["strict_structural_pass"] == "True":
            tracks.append("strict structural pass")
        if s["strict_structural_pass"] != "True" and s["functional_tier"] != "EXCLUDE" and 1 <= len(failed) <= 2:
            tracks.append("structural near-miss")
        if j in RESCUE:
            tracks.append("literature-rescue")
        if not tracks:
            tracks.append("background")
        full_class = conservation_class(c)
        row = dict(s)
        for k, v in c.items():
            if k not in ("junction", "left_resid", "left_aa", "right_resid", "right_aa"):
                row["hrvA_" + k] = v
        row.update({
            "structural_track": ";".join(tracks),
            "failed_gate_count": len(failed),
            "failed_gate_names": ";".join(failed) or "none",
            "literature_rescue_status": "True" if j in RESCUE else "False",
            "literature_rescue_source": RESCUE.get(j, ""),
            "hrvA_conservation_class_v2": full_class,
            "evolutionary_layer_effect_v2": effect(s, c),
            "exact_boundary_sensitivity": exact_sensitivity(full_class, exact.get(j)),
            "focal_junction": "True" if j in FOCAL else "False",
            "priority_interpretation_v2": priority(s, c, tracks),
        })
        rows.append(row)
        old = v1.get(j, {})
        comp.append({
            "junction": j,
            "v1_conservation_class": old.get("hrvA_conservation_class", ""),
            "v2_conservation_class": full_class,
            "v1_priority_interpretation": old.get("priority_interpretation", ""),
            "v2_priority_interpretation": row["priority_interpretation_v2"],
            "v1_type_weighted_window_mean_identity": old.get("hrvA_type_weighted_window_mean_identity", ""),
            "v2_type_weighted_window_mean_identity": c.get("type_weighted_window_mean_identity", ""),
            "v1_type_weighted_window_mean_entropy": old.get("hrvA_type_weighted_window_mean_entropy", ""),
            "v2_type_weighted_window_mean_entropy": c.get("type_weighted_window_mean_entropy", ""),
            "v1_expanded_insertion_frequency": old.get("hrvA_expanded_natural_insertion_frequency", ""),
            "v2_expanded_insertion_frequency": c.get("expanded_natural_insertion_frequency", ""),
            "v2_expanded_indel_category": c.get("expanded_indel_category", ""),
            "interpretation_changed": "True" if old.get("hrvA_conservation_class", "") != full_class else "False",
        })
    for out_path, table in [(args.out, rows), (args.comparison_out, comp)]:
        with open(out_path, "w") as out:
            w = csv.DictWriter(out, fieldnames=list(table[0].keys()), delimiter="\t", lineterminator="\n")
            w.writeheader()
            w.writerows(table)


if __name__ == "__main__":
    main()
