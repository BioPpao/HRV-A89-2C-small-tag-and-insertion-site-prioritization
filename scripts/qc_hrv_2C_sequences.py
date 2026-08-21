#!/usr/bin/env python3
"""QC acquired HRV 2C FASTA/metadata files."""

from __future__ import print_function

import argparse
import csv
import platform
import subprocess
import sys

from hrv2c_conservation_lib import read_fasta


def read_tsv(path):
    with open(path) as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def version(cmd):
    try:
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        text = (out + err).decode("utf-8", "replace").strip().splitlines()
        return text[0] if text else "not_available"
    except OSError:
        return "not_available"


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--reference-fasta", default="references/HRV_A89_2C_reference_sequence.fasta")
    ap.add_argument("--primary-fasta", required=True)
    ap.add_argument("--primary-metadata", required=True)
    ap.add_argument("--expanded-fasta", required=True)
    ap.add_argument("--expanded-metadata", required=True)
    ap.add_argument("--qc-summary", required=True)
    ap.add_argument("--environment", required=True)
    args = ap.parse_args()

    ref = read_fasta(args.reference_fasta)[0][1]
    if len(ref) != 321:
        raise SystemExit("authoritative A89 sequence length != 321")

    primary = read_fasta(args.primary_fasta)
    expanded = read_fasta(args.expanded_fasta)
    primary_meta = read_tsv(args.primary_metadata)
    expanded_meta = read_tsv(args.expanded_metadata)
    if len(primary) != len(primary_meta):
        raise SystemExit("primary FASTA/metadata count mismatch")
    if len(expanded) != len(expanded_meta):
        raise SystemExit("expanded FASTA/metadata count mismatch")
    if not any(name.startswith("A89_REF|") and seq == ref for name, seq in primary):
        raise SystemExit("authoritative A89 sequence missing/mismatched in primary FASTA")
    if not any(name.startswith("A89_REF|") and seq == ref for name, seq in expanded):
        raise SystemExit("authoritative A89 sequence missing/mismatched in expanded FASTA")

    def stats(records):
        lengths = [len(seq) for _, seq in records]
        unknown = sum(sum(1 for c in seq if c not in "ACDEFGHIKLMNPQRSTVWY") for _, seq in records)
        stops = sum(1 for _, seq in records if "*" in seq)
        return lengths, unknown, stops

    p_len, p_unknown, p_stops = stats(primary)
    e_len, e_unknown, e_stops = stats(expanded)
    with open(args.qc_summary, "w") as out:
        out.write("metric\tvalue\n")
        out.write("reference_length\t321\n")
        out.write("primary_sequences\t%s\n" % len(primary))
        out.write("expanded_sequences\t%s\n" % len(expanded))
        out.write("primary_min_length\t%s\n" % min(p_len))
        out.write("primary_max_length\t%s\n" % max(p_len))
        out.write("expanded_min_length\t%s\n" % min(e_len))
        out.write("expanded_max_length\t%s\n" % max(e_len))
        out.write("primary_internal_stop_records\t%s\n" % p_stops)
        out.write("expanded_internal_stop_records\t%s\n" % e_stops)
        out.write("primary_unknown_residues\t%s\n" % p_unknown)
        out.write("expanded_unknown_residues\t%s\n" % e_unknown)
        out.write("primary_type_labels\t%s\n" % len(set(r["type_label"] for r in primary_meta)))
        out.write("expanded_type_labels\t%s\n" % len(set(r["type_label"] for r in expanded_meta)))

    with open(args.environment, "w") as out:
        out.write("item\tvalue\n")
        out.write("python\t%s\n" % sys.version.replace("\n", " "))
        out.write("platform\t%s\n" % platform.platform())
        out.write("requests\t%s\n" % version([sys.executable, "-c", "import requests; print(requests.__version__)"]))
        out.write("mafft\t%s\n" % version(["mafft", "--version"]))
        out.write("alignment_method\tA89 reference-guided Needleman-Wunsch fallback; MAFFT not available on PATH\n")


if __name__ == "__main__":
    main()
