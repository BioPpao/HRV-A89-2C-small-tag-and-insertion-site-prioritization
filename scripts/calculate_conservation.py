#!/usr/bin/env python3
"""Calculate A89-anchored residue and junction conservation metrics."""

from __future__ import print_function

import argparse
import csv

from hrv2c_conservation_lib import AA, UNKNOWN, normalize_entropy, read_fasta, shannon_entropy


def read_meta(path):
    with open(path) as handle:
        return {r["sequence_id"]: r for r in csv.DictReader(handle, delimiter="\t")}


def read_mapping(path):
    rows = []
    with open(path) as handle:
        for r in csv.DictReader(handle, delimiter="\t"):
            rows.append((int(r["a89_residue"]), r["a89_aa"], int(r["alignment_column_1based"]) - 1))
    return rows


def weighted_metrics(chars, weights, ref_aa):
    total_weight = sum(weights)
    gap_weight = sum(w for c, w in zip(chars, weights) if c == "-")
    known = {}
    known_weight = 0.0
    identity = 0.0
    for c, w in zip(chars, weights):
        if c == "-" or c in UNKNOWN:
            continue
        if c not in AA:
            continue
        known[c] = known.get(c, 0.0) + w
        known_weight += w
        if c == ref_aa:
            identity += w
    ent = shannon_entropy(known)
    dominant = ""
    dom_freq = 0.0
    if known:
        dominant = sorted(known.items(), key=lambda x: (-x[1], x[0]))[0][0]
        dom_freq = known[dominant] / known_weight
    return {
        "total": total_weight,
        "effective": known_weight,
        "dominant": dominant,
        "dominant_frequency": dom_freq,
        "a89_identity_fraction": identity / known_weight if known_weight else 0.0,
        "entropy": ent,
        "normalized_entropy": normalize_entropy(ent),
        "gap_frequency": gap_weight / total_weight if total_weight else 0.0,
    }


def type_weights(records, meta):
    counts = {}
    for name, _ in records:
        t = meta[name]["type_label"]
        counts[t] = counts.get(t, 0) + 1
    return [1.0 / counts[meta[name]["type_label"]] for name, _ in records]


def equal_weights(records):
    return [1.0 for _ in records]


def residue_table(ref, primary, primary_map, primary_meta, expanded, expanded_map, expanded_meta):
    rows = []
    p_weights = equal_weights(primary)
    e_weights = equal_weights(expanded)
    tw_weights = type_weights(expanded, expanded_meta)
    for resid, aa, col in primary_map:
        p_chars = [seq[col] for _, seq in primary]
        e_col = expanded_map[resid - 1][2]
        e_chars = [seq[e_col] for _, seq in expanded]
        pm = weighted_metrics(p_chars, p_weights, aa)
        em = weighted_metrics(e_chars, e_weights, aa)
        tm = weighted_metrics(e_chars, tw_weights, aa)
        row = {
            "a89_residue": resid,
            "a89_aa": aa,
            "primary_total_sequences": len(primary),
            "primary_effective_sequences": "%.4f" % pm["effective"],
            "primary_dominant_aa": pm["dominant"],
            "primary_dominant_frequency": "%.6f" % pm["dominant_frequency"],
            "primary_a89_identity_fraction": "%.6f" % pm["a89_identity_fraction"],
            "primary_shannon_entropy": "%.6f" % pm["entropy"],
            "primary_normalized_entropy": "%.6f" % pm["normalized_entropy"],
            "primary_gap_frequency": "%.6f" % pm["gap_frequency"],
            "expanded_total_sequences": len(expanded),
            "expanded_effective_sequences": "%.4f" % em["effective"],
            "expanded_dominant_aa": em["dominant"],
            "expanded_dominant_frequency": "%.6f" % em["dominant_frequency"],
            "expanded_a89_identity_fraction": "%.6f" % em["a89_identity_fraction"],
            "expanded_shannon_entropy": "%.6f" % em["entropy"],
            "expanded_normalized_entropy": "%.6f" % em["normalized_entropy"],
            "expanded_gap_frequency": "%.6f" % em["gap_frequency"],
            "type_weighted_effective_sequences": "%.4f" % tm["effective"],
            "type_weighted_dominant_aa": tm["dominant"],
            "type_weighted_dominant_frequency": "%.6f" % tm["dominant_frequency"],
            "type_weighted_a89_identity_fraction": "%.6f" % tm["a89_identity_fraction"],
            "type_weighted_shannon_entropy": "%.6f" % tm["entropy"],
            "type_weighted_normalized_entropy": "%.6f" % tm["normalized_entropy"],
            "type_weighted_gap_frequency": "%.6f" % tm["gap_frequency"],
        }
        rows.append(row)
    return rows


def insertion_stats(records, mapping, junction_left):
    left_col = mapping[junction_left - 1][2]
    right_col = mapping[junction_left][2]
    insert_cols = list(range(left_col + 1, right_col))
    if not insert_cols:
        return 0, 0.0, "0"
    lengths = []
    for _, seq in records:
        n = sum(1 for c in (seq[i] for i in insert_cols) if c != "-")
        lengths.append(n)
    positive = sum(1 for n in lengths if n > 0)
    counts = {}
    for n in lengths:
        if n > 0:
            counts[n] = counts.get(n, 0) + 1
    return positive, positive / float(len(records)), ";".join("%s:%s" % (k, counts[k]) for k in sorted(counts)) or "0"


def junction_table(res_rows, primary, primary_map, expanded, expanded_map):
    rows = []
    for i in range(1, 321):
        left = res_rows[i - 1]
        right = res_rows[i]
        lo = max(1, i - 5)
        hi = min(321, i + 1 + 5)
        window = res_rows[lo - 1:hi]
        p_ent = [float(r["primary_shannon_entropy"]) for r in window]
        p_ident = [float(r["primary_a89_identity_fraction"]) for r in window]
        p_gap = [float(r["primary_gap_frequency"]) for r in window]
        tw_ent = [float(r["type_weighted_shannon_entropy"]) for r in window]
        tw_ident = [float(r["type_weighted_a89_identity_fraction"]) for r in window]
        tw_gap = [float(r["type_weighted_gap_frequency"]) for r in window]
        e_ent = [float(r["expanded_shannon_entropy"]) for r in window]
        e_ident = [float(r["expanded_a89_identity_fraction"]) for r in window]
        e_gap = [float(r["expanded_gap_frequency"]) for r in window]
        p_ins_n, p_ins_f, p_ins_len = insertion_stats(primary, primary_map, i)
        e_ins_n, e_ins_f, e_ins_len = insertion_stats(expanded, expanded_map, i)
        local_del_count = 0
        for _, seq in expanded:
            cols = [expanded_map[r - 1][2] for r in range(lo, hi + 1)]
            if any(seq[c] == "-" for c in cols):
                local_del_count += 1
        rows.append({
            "junction": "%s|%s" % (i, i + 1),
            "left_resid": i,
            "left_aa": left["a89_aa"],
            "right_resid": i + 1,
            "right_aa": right["a89_aa"],
            "primary_left_identity": left["primary_a89_identity_fraction"],
            "primary_right_identity": right["primary_a89_identity_fraction"],
            "primary_left_entropy": left["primary_shannon_entropy"],
            "primary_right_entropy": right["primary_shannon_entropy"],
            "primary_left_gap_frequency": left["primary_gap_frequency"],
            "primary_right_gap_frequency": right["primary_gap_frequency"],
            "primary_window_mean_entropy": "%.6f" % (sum(p_ent) / len(p_ent)),
            "primary_window_max_entropy": "%.6f" % max(p_ent),
            "primary_window_mean_identity": "%.6f" % (sum(p_ident) / len(p_ident)),
            "primary_window_min_identity": "%.6f" % min(p_ident),
            "primary_window_mean_gap_frequency": "%.6f" % (sum(p_gap) / len(p_gap)),
            "primary_window_max_gap_frequency": "%.6f" % max(p_gap),
            "primary_natural_insertion_count": p_ins_n,
            "primary_natural_insertion_frequency": "%.6f" % p_ins_f,
            "primary_natural_insertion_lengths": p_ins_len,
            "expanded_window_mean_entropy": "%.6f" % (sum(e_ent) / len(e_ent)),
            "expanded_window_max_entropy": "%.6f" % max(e_ent),
            "expanded_window_mean_identity": "%.6f" % (sum(e_ident) / len(e_ident)),
            "expanded_window_min_identity": "%.6f" % min(e_ident),
            "expanded_window_mean_gap_frequency": "%.6f" % (sum(e_gap) / len(e_gap)),
            "expanded_window_max_gap_frequency": "%.6f" % max(e_gap),
            "expanded_natural_insertion_count": e_ins_n,
            "expanded_natural_insertion_frequency": "%.6f" % e_ins_f,
            "expanded_natural_insertion_lengths": e_ins_len,
            "expanded_local_deletion_count": local_del_count,
            "expanded_local_deletion_frequency": "%.6f" % (local_del_count / float(len(expanded))),
            "type_weighted_window_mean_entropy": "%.6f" % (sum(tw_ent) / len(tw_ent)),
            "type_weighted_window_max_entropy": "%.6f" % max(tw_ent),
            "type_weighted_window_mean_identity": "%.6f" % (sum(tw_ident) / len(tw_ident)),
            "type_weighted_window_min_identity": "%.6f" % min(tw_ident),
            "type_weighted_window_mean_gap_frequency": "%.6f" % (sum(tw_gap) / len(tw_gap)),
            "type_weighted_window_max_gap_frequency": "%.6f" % max(tw_gap),
        })
    return rows


def write_rows(rows, path):
    with open(path, "w") as out:
        writer = csv.DictWriter(out, fieldnames=list(rows[0].keys()), delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def assert_range(rows, fields):
    for row in rows:
        for field in fields:
            v = float(row[field])
            if v < 0 or v > 1:
                raise SystemExit("%s outside [0,1] at %s" % (field, row.get("junction", row.get("a89_residue"))))


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
    if len(primary_map) != 321 or len(expanded_map) != 321:
        raise SystemExit("A89 mapping rows != 321")
    res = residue_table(ref, primary, primary_map, primary_meta, expanded, expanded_map, expanded_meta)
    jun = junction_table(res, primary, primary_map, expanded, expanded_map)
    if len(res) != 321:
        raise SystemExit("residue table rows != 321")
    if len(jun) != 320:
        raise SystemExit("junction table rows != 320")
    assert_range(res, ["primary_a89_identity_fraction", "primary_gap_frequency",
                       "expanded_a89_identity_fraction", "expanded_gap_frequency",
                       "type_weighted_a89_identity_fraction", "type_weighted_gap_frequency"])
    assert_range(jun, ["primary_natural_insertion_frequency", "expanded_natural_insertion_frequency",
                       "expanded_local_deletion_frequency", "type_weighted_window_mean_gap_frequency"])
    write_rows(res, args.residue_output)
    write_rows(jun, args.junction_output)


if __name__ == "__main__":
    main()
