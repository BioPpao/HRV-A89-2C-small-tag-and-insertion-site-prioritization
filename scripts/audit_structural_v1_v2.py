#!/usr/bin/env python3
"""Audit structural gate consistency and V1/V2 differences."""

from __future__ import annotations

import argparse
import csv


GATES = [
    ("both_AF_coil", lambda r: r["both_AF_coil"] == "True"),
    ("hexamer_coil_fraction_ge_0.8", lambda r: float(r["min_hex_coil_fraction"]) >= 0.8),
    ("AF_rSASA_ge_0.25", lambda r: float(r["min_AF_rSASA"]) >= 0.25),
    ("hexamer_rSASA_ge_0.25", lambda r: float(r["min_hexamer_mean_rSASA"]) >= 0.25),
    ("burial_lt_0.10", lambda r: float(r["max_any_chain_burial_fraction"]) < 0.10),
    ("interprotomer_distance_gt_4.5A", lambda r: float(r["min_interprotomer_heavy_atom_A"]) > 4.5),
]


def read(path):
    with open(path) as handle:
        return {r["junction"]: r for r in csv.DictReader(handle, delimiter="\t")}


def gate_status(row):
    failed = [name for name, ok in GATES if not ok(row)]
    computed = len(failed) == 0
    stored = row["strict_structural_pass"] == "True"
    return computed, stored, failed


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--v1", default="data/junction_structural_metrics_v1.tsv")
    ap.add_argument("--v2", default="data/junction_structural_metrics_v2.tsv")
    ap.add_argument("--out", default="results/structural_v1_v2_gate_audit.tsv")
    args = ap.parse_args()
    v1 = read(args.v1)
    v2 = read(args.v2)
    rows = []
    for j in [f"{i}|{i+1}" for i in range(1, 321)]:
        r1 = v1[j]
        r2 = v2[j]
        c1, s1, f1 = gate_status(r1)
        c2, s2, f2 = gate_status(r2)
        cause = "consistent"
        if c1 != s1 and c2 == s2:
            cause = "v1_table_strict_flag_inconsistent_with_v1_gate_columns"
        elif c1 != s1 and c2 != s2:
            cause = "both_versions_inconsistent"
        elif c1 == s1 and c2 != s2:
            cause = "v2_inconsistent"
        elif s1 != s2:
            cause = "strict_status_changed_after_regeneration"
        rows.append({
            "junction": j,
            "v1_stored_strict": r1["strict_structural_pass"],
            "v1_computed_strict_from_columns": str(c1),
            "v1_failed_gates": ";".join(f1) or "none",
            "v2_stored_strict": r2["strict_structural_pass"],
            "v2_computed_strict_from_columns": str(c2),
            "v2_failed_gates": ";".join(f2) or "none",
            "audit_cause": cause,
            "v1_min_AF_rSASA": r1["min_AF_rSASA"],
            "v2_min_AF_rSASA": r2["min_AF_rSASA"],
            "v1_min_hexamer_mean_rSASA": r1["min_hexamer_mean_rSASA"],
            "v2_min_hexamer_mean_rSASA": r2["min_hexamer_mean_rSASA"],
            "v1_max_any_chain_burial_fraction": r1["max_any_chain_burial_fraction"],
            "v2_max_any_chain_burial_fraction": r2["max_any_chain_burial_fraction"],
            "v1_min_interprotomer_heavy_atom_A": r1["min_interprotomer_heavy_atom_A"],
            "v2_min_interprotomer_heavy_atom_A": r2["min_interprotomer_heavy_atom_A"],
        })
    with open(args.out, "w") as out:
        w = csv.DictWriter(out, fieldnames=list(rows[0].keys()), delimiter="\t", lineterminator="\n")
        w.writeheader()
        w.writerows(rows)


if __name__ == "__main__":
    main()
