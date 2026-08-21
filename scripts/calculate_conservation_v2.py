#!/usr/bin/env python3
"""V2 conservation metrics with type-aware indel categories."""

from __future__ import annotations

import argparse
import csv

from calculate_conservation import read_mapping, read_meta, residue_table, junction_table, write_rows, assert_range
from hrv2c_conservation_lib import read_fasta


def insertion_type_set(records, meta, mapping, left_resid):
    left_col = mapping[left_resid - 1][2]
    right_col = mapping[left_resid][2]
    cols = list(range(left_col + 1, right_col))
    types = set()
    lengths = {}
    for name, seq in records:
        n = sum(1 for i in cols if seq[i] != "-")
        if n > 0:
            t = meta[name]["type_label"]
            types.add(t)
            lengths[n] = lengths.get(n, 0) + 1
    return types, lengths


def deletion_type_set(records, meta, mapping, left_resid):
    lo = max(1, left_resid - 5)
    hi = min(321, left_resid + 1 + 5)
    cols = [mapping[r - 1][2] for r in range(lo, hi + 1)]
    types = set()
    for name, seq in records:
        if any(seq[c] == "-" for c in cols):
            types.add(meta[name]["type_label"])
    return types


def category(type_count):
    if type_count == 0:
        return "none"
    if type_count == 1:
        return "singleton_or_rare"
    if type_count < 5:
        return "recurrent_across_types"
    return "broader_lineage_supported"


def add_indel_categories(rows, primary, primary_meta, primary_map, expanded, expanded_meta, expanded_map):
    for row in rows:
        left = int(row["left_resid"])
        p_ins, p_lengths = insertion_type_set(primary, primary_meta, primary_map, left)
        e_ins, e_lengths = insertion_type_set(expanded, expanded_meta, expanded_map, left)
        p_del = deletion_type_set(primary, primary_meta, primary_map, left)
        e_del = deletion_type_set(expanded, expanded_meta, expanded_map, left)
        max_types = max(len(e_ins), len(e_del))
        row["primary_natural_insertion_type_count"] = len(p_ins)
        row["primary_natural_insertion_types"] = ";".join(sorted(p_ins)) or "none"
        row["expanded_natural_insertion_type_count"] = len(e_ins)
        row["expanded_natural_insertion_types"] = ";".join(sorted(e_ins)) or "none"
        row["expanded_local_deletion_type_count"] = len(e_del)
        row["expanded_local_deletion_types"] = ";".join(sorted(e_del)) or "none"
        row["expanded_indel_category"] = category(max_types)
        row["expanded_indel_category_basis"] = "max(insertion_type_count,local_deletion_type_count)"
    return rows


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--reference-fasta", default="references/HRV_A89_2C_reference_sequence.fasta")
    ap.add_argument("--primary-alignment", required=True)
    ap.add_argument("--primary-mapping", required=True)
    ap.add_argument("--primary-metadata", required=True)
    ap.add_argument("--expanded-alignment", required=True)
    ap.add_argument("--expanded-mapping", required=True)
    ap.add_argument("--expanded-metadata", required=True)
    ap.add_argument("--residue-output", required=True)
    ap.add_argument("--junction-output", required=True)
    args = ap.parse_args()

    ref = read_fasta(args.reference_fasta)[0][1]
    if len(ref) != 321:
        raise SystemExit("authoritative A89 sequence length != 321")
    primary = read_fasta(args.primary_alignment)
    expanded = read_fasta(args.expanded_alignment)
    primary_meta = read_meta(args.primary_metadata)
    expanded_meta = read_meta(args.expanded_metadata)
    primary_map = read_mapping(args.primary_mapping)
    expanded_map = read_mapping(args.expanded_mapping)
    res = residue_table(ref, primary, primary_map, primary_meta, expanded, expanded_map, expanded_meta)
    jun = junction_table(res, primary, primary_map, expanded, expanded_map)
    jun = add_indel_categories(jun, primary, primary_meta, primary_map, expanded, expanded_meta, expanded_map)
    if len(res) != 321:
        raise SystemExit("residue table rows != 321")
    if len(jun) != 320:
        raise SystemExit("junction table rows != 320")
    assert_range(res, ["primary_a89_identity_fraction", "primary_gap_frequency",
                       "expanded_a89_identity_fraction", "expanded_gap_frequency",
                       "type_weighted_a89_identity_fraction", "type_weighted_gap_frequency"])
    write_rows(res, args.residue_output)
    write_rows(jun, args.junction_output)


if __name__ == "__main__":
    main()
