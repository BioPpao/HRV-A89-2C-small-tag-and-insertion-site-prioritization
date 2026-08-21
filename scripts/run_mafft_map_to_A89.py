#!/usr/bin/env python3
"""Run MAFFT L-INS-i and map A89 residues to alignment columns."""

from __future__ import annotations

import argparse
import csv
import subprocess
from pathlib import Path

from hrv2c_conservation_lib import read_fasta


def map_a89(alignment: Path, out_tsv: Path, reference_fasta: Path) -> None:
    ref_seq = read_fasta(str(reference_fasta))[0][1]
    if len(ref_seq) != 321:
        raise SystemExit("authoritative A89 sequence length != 321")
    records = read_fasta(str(alignment))
    ref_records = [(name, seq) for name, seq in records if name.startswith("A89_REF|")]
    if len(ref_records) != 1:
        raise SystemExit("expected exactly one A89_REF record in MAFFT alignment")
    aligned = ref_records[0][1]
    rows = []
    pos = 0
    for col, aa in enumerate(aligned, start=1):
        if aa == "-":
            continue
        pos += 1
        if pos > 321:
            raise SystemExit("A89 alignment maps beyond residue 321")
        if aa != ref_seq[pos - 1]:
            raise SystemExit(f"A89 residue mismatch at {pos}: {aa} != {ref_seq[pos - 1]}")
        rows.append({"a89_residue": pos, "a89_aa": aa, "alignment_column_1based": col})
    if len(rows) != 321:
        raise SystemExit("A89 mapped residue count != 321")
    with out_tsv.open("w") as out:
        w = csv.DictWriter(out, fieldnames=["a89_residue", "a89_aa", "alignment_column_1based"], delimiter="\t", lineterminator="\n")
        w.writeheader()
        w.writerows(rows)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--mafft", default=".tools/envs/hrv2c-conservation-qc/bin/mafft")
    ap.add_argument("--input-fasta", required=True, type=Path)
    ap.add_argument("--alignment-fasta", required=True, type=Path)
    ap.add_argument("--mapping-tsv", required=True, type=Path)
    ap.add_argument("--reference-fasta", default="references/HRV_A89_2C_reference_sequence.fasta", type=Path)
    ap.add_argument("--mafft-log", required=True, type=Path)
    args = ap.parse_args()

    cmd = [args.mafft, "--localpair", "--maxiterate", "1000", str(args.input_fasta)]
    args.alignment_fasta.parent.mkdir(parents=True, exist_ok=True)
    args.mafft_log.parent.mkdir(parents=True, exist_ok=True)
    with args.alignment_fasta.open("w") as out, args.mafft_log.open("w") as err:
        proc = subprocess.run(cmd, stdout=out, stderr=err, text=True)
    if proc.returncode != 0:
        raise SystemExit(f"MAFFT failed: {proc.returncode}")
    map_a89(args.alignment_fasta, args.mapping_tsv, args.reference_fasta)


if __name__ == "__main__":
    main()
