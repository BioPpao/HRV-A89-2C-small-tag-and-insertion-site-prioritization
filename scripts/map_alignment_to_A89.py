#!/usr/bin/env python3
"""Build an A89-anchored reference-guided protein alignment."""

from __future__ import print_function

import argparse

from hrv2c_conservation_lib import nw_align, read_fasta, write_fasta


def slot_alignment(ref, records):
    slots = [[] for _ in range(len(ref) + 1)]
    residue_chars = {}
    pair_info = []
    for name, seq in records:
        ar, ase, score = nw_align(ref, seq)
        slot_strings = ["" for _ in range(len(ref) + 1)]
        chars = ["-"] * len(ref)
        pos = 0
        matches = 0
        comparable = 0
        for a, b in zip(ar, ase):
            if a == "-":
                slot_strings[pos] += b
            else:
                pos += 1
                chars[pos - 1] = b
                if b != "-":
                    comparable += 1
                    if a == b:
                        matches += 1
        for i, s in enumerate(slot_strings):
            slots[i].append(s)
        residue_chars[name] = chars
        pair_info.append((name, score, comparable / float(len(ref)), matches / float(comparable or 1)))
    max_slot = [max([len(x) for x in values] + [0]) for values in slots]
    aligned = []
    for idx, (name, seq) in enumerate(records):
        out = []
        for slot_index in range(len(ref)):
            s = slots[slot_index][idx]
            out.append(s + "-" * (max_slot[slot_index] - len(s)))
            out.append(residue_chars[name][slot_index])
        s = slots[len(ref)][idx]
        out.append(s + "-" * (max_slot[len(ref)] - len(s)))
        aligned.append((name, "".join(out)))
    mapping = []
    col = max_slot[0] + 1
    for i in range(1, len(ref) + 1):
        mapping.append((i, ref[i - 1], col))
        col += 1 + max_slot[i]
    return aligned, mapping, pair_info


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--reference-fasta", default="references/HRV_A89_2C_reference_sequence.fasta")
    ap.add_argument("--input-fasta", required=True)
    ap.add_argument("--alignment-fasta", required=True)
    ap.add_argument("--mapping-tsv", required=True)
    ap.add_argument("--pairwise-qc-tsv", required=True)
    args = ap.parse_args()

    ref = read_fasta(args.reference_fasta)[0][1]
    if len(ref) != 321:
        raise SystemExit("authoritative A89 sequence length != 321")
    records = read_fasta(args.input_fasta)
    if not records:
        raise SystemExit("no input records")
    aligned, mapping, pair_info = slot_alignment(ref, records)
    lengths = set(len(seq) for _, seq in aligned)
    if len(lengths) != 1:
        raise SystemExit("alignment sequence lengths differ")
    write_fasta(aligned, args.alignment_fasta)
    with open(args.mapping_tsv, "w") as out:
        out.write("a89_residue\ta89_aa\talignment_column_1based\n")
        for row in mapping:
            out.write("%s\t%s\t%s\n" % row)
    with open(args.pairwise_qc_tsv, "w") as out:
        out.write("sequence_id\talignment_score\tref_coverage\tpairwise_identity\n")
        for name, score, cov, ident in pair_info:
            out.write("%s\t%s\t%.4f\t%.4f\n" % (name, score, cov, ident))


if __name__ == "__main__":
    main()
