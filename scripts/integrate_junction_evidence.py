#!/usr/bin/env python3
"""Integrate structural, functional, conservation, and rescue evidence."""

from __future__ import print_function

import argparse
import csv


GATES = [
    ("AF_coil", lambda r: r["both_AF_coil"] == "True"),
    ("hexamer_coil_fraction_ge_0.8", lambda r: float(r["min_hex_coil_fraction"]) >= 0.8),
    ("AF_rSASA_ge_0.25", lambda r: float(r["min_AF_rSASA"]) >= 0.25),
    ("hexamer_rSASA_ge_0.25", lambda r: float(r["min_hexamer_mean_rSASA"]) >= 0.25),
    ("burial_lt_0.10", lambda r: float(r["max_any_chain_burial_fraction"]) < 0.10),
    ("interprotomer_distance_gt_4.5A", lambda r: float(r["min_interprotomer_heavy_atom_A"]) > 4.5),
]

RESCUE = {
    "248|249": "Li/Baltimore PV insertion after 2C residue 255; A89 mapped literature-rescue track",
    "256|257": "Li/Baltimore PV insertion after 2C residue 263; A89 mapped literature-rescue track",
}

REGIONS = set(["155|156", "174|175", "175|176", "216|217", "217|218", "218|219",
               "248|249", "256|257", "287|288", "288|289", "289|290", "290|291"])


def read_rows(path, key):
    with open(path) as handle:
        return {r[key]: r for r in csv.DictReader(handle, delimiter="\t")}


def read_list(path):
    with open(path) as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def failed_gates(row):
    failed = [name for name, ok in GATES if not ok(row)]
    return failed


def conservation_class(row):
    ident = float(row["type_weighted_window_mean_identity"])
    ent = float(row["type_weighted_window_mean_entropy"])
    ins = float(row["expanded_natural_insertion_frequency"])
    dele = float(row["expanded_local_deletion_frequency"])
    if ins > 0 or dele >= 0.05:
        return "indel_signal"
    if ident <= 0.70 or ent >= 0.75:
        return "variable"
    if ident >= 0.90 and ent <= 0.30 and dele < 0.01:
        return "conserved"
    return "intermediate"


def evolutionary_effect(struct, cons):
    c = conservation_class(cons)
    tier = struct["functional_tier"]
    if c in ("variable", "indel_signal") and tier != "EXCLUDE":
        return "supports"
    if c == "conserved" or tier == "EXCLUDE":
        return "weakens"
    return "remains unresolved"


def priority(row, cons, tracks):
    tier = row["functional_tier"]
    c = conservation_class(cons)
    if "literature-rescue" in tracks:
        return "literature-rescue retained; conservation %s; not promoted without functional/structure review" % c
    if tier == "EXCLUDE":
        return "decreased_or_excluded; hard functional feature dominates conservation"
    if "strict structural pass" in tracks and c in ("variable", "indel_signal"):
        return "increased_for_later_review; structural geometry plus evolutionary variability"
    if "strict structural pass" in tracks:
        return "unchanged; strict geometry but conservation does not clear functional risk"
    if "structural near-miss" in tracks and c in ("variable", "indel_signal"):
        return "new_outside_strict10_for_later_review; near-miss plus evolutionary variability"
    if c == "conserved":
        return "decreased; conserved local window"
    return "unchanged; no decisive evolutionary rescue"


def context_row(junction, a, b, c):
    out = {
        "junction": junction,
        "hrvA_type_weighted_window_mean_identity": a.get("type_weighted_window_mean_identity", ""),
        "hrvA_type_weighted_window_mean_entropy": a.get("type_weighted_window_mean_entropy", ""),
        "hrvA_expanded_insertion_frequency": a.get("expanded_natural_insertion_frequency", ""),
        "hrvA_expanded_local_deletion_frequency": a.get("expanded_local_deletion_frequency", ""),
        "hrvB_type_weighted_window_mean_identity": b.get("type_weighted_window_mean_identity", "") if b else "",
        "hrvB_type_weighted_window_mean_entropy": b.get("type_weighted_window_mean_entropy", "") if b else "",
        "hrvC_type_weighted_window_mean_identity": c.get("type_weighted_window_mean_identity", "") if c else "",
        "hrvC_type_weighted_window_mean_entropy": c.get("type_weighted_window_mean_entropy", "") if c else "",
    }
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--structural", default="data/junction_structural_metrics_v1.tsv")
    ap.add_argument("--hrva-junctions", required=True)
    ap.add_argument("--hrvb-junctions", default=None)
    ap.add_argument("--hrvc-junctions", default=None)
    ap.add_argument("--candidate-output", required=True)
    ap.add_argument("--abc-context-output", required=True)
    args = ap.parse_args()

    structural = read_list(args.structural)
    cons_a = read_rows(args.hrva_junctions, "junction")
    cons_b = read_rows(args.hrvb_junctions, "junction") if args.hrvb_junctions else {}
    cons_c = read_rows(args.hrvc_junctions, "junction") if args.hrvc_junctions else {}
    if len(structural) != 320:
        raise SystemExit("structural rows != 320")
    if len(cons_a) != 320:
        raise SystemExit("HRV-A junction rows != 320")

    rows = []
    ctx = []
    for s in structural:
        j = s["junction"]
        if j not in cons_a:
            raise SystemExit("missing conservation join for %s" % j)
        failed = failed_gates(s)
        tracks = []
        if s["strict_structural_pass"] == "True":
            tracks.append("strict structural pass")
        if s["strict_structural_pass"] != "True" and s["functional_tier"] != "EXCLUDE" and len(failed) <= 2:
            tracks.append("structural near-miss")
        if j in RESCUE:
            tracks.append("literature-rescue")
        if not tracks:
            tracks.append("background")
        c = cons_a[j]
        conflict = "True" if (
            ("literature-rescue" in tracks and (s["functional_tier"] != "LOW_RISK" or len(failed) > 0)) or
            ("strict structural pass" in tracks and s["functional_tier"] in ("EXCLUDE", "HIGH_RISK")) or
            (conservation_class(c) in ("variable", "indel_signal") and s["functional_tier"] == "EXCLUDE")
        ) else "False"
        evo = evolutionary_effect(s, c)
        row = dict(s)
        for k, v in c.items():
            if k not in ("junction", "left_resid", "left_aa", "right_resid", "right_aa"):
                row["hrvA_" + k] = v
        row.update({
            "structural_track": ";".join(tracks),
            "failed_gate_count": len(failed),
            "failed_gate_names": ";".join(failed) if failed else "none",
            "literature_rescue_status": "True" if j in RESCUE else "False",
            "literature_rescue_source": RESCUE.get(j, ""),
            "hrvA_conservation_class": conservation_class(c),
            "evolutionary_layer_effect": evo,
            "region_requiring_explicit_interpretation": "True" if j in REGIONS else "False",
            "evidence_conflict": conflict,
            "priority_interpretation": priority(s, c, tracks),
        })
        rows.append(row)
        ctx.append(context_row(j, c, cons_b.get(j), cons_c.get(j)))

    keys = [r["junction"] for r in rows]
    if len(set(keys)) != 320 or keys[0] != "1|2" or keys[-1] != "320|321":
        raise SystemExit("junction keys not unique or not full 1|2..320|321 span")

    with open(args.candidate_output, "w") as out:
        writer = csv.DictWriter(out, fieldnames=list(rows[0].keys()), delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    with open(args.abc_context_output, "w") as out:
        writer = csv.DictWriter(out, fieldnames=list(ctx[0].keys()), delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(ctx)


if __name__ == "__main__":
    main()
