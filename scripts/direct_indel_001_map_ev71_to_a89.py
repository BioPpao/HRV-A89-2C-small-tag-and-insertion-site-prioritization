#!/usr/bin/env python3
"""Map EV-A71 2C direct InDel fitness data onto HRV-A89 2C junctions."""

from __future__ import annotations

import argparse
import csv
import hashlib
import math
import re
import subprocess
from pathlib import Path

import pandas as pd
from Bio import SeqIO


AA3_TO_1 = {
    "Ala": "A",
    "Cys": "C",
    "Asp": "D",
    "Glu": "E",
    "Phe": "F",
    "Gly": "G",
    "His": "H",
    "Ile": "I",
    "Lys": "K",
    "Leu": "L",
    "Met": "M",
    "Asn": "N",
    "Pro": "P",
    "Gln": "Q",
    "Arg": "R",
    "Ser": "S",
    "Thr": "T",
    "Val": "V",
    "Trp": "W",
    "Tyr": "Y",
}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def read_single_fasta(path: Path) -> tuple[str, str]:
    rec = next(SeqIO.parse(str(path), "fasta"))
    return rec.id, str(rec.seq).replace("-", "")


def write_pair_fasta(a89_fasta: Path, ev71_fasta: Path, out: Path) -> None:
    a89_id, a89_seq = read_single_fasta(a89_fasta)
    ev_id, ev_seq = read_single_fasta(ev71_fasta)
    out.write_text(f">{a89_id}\n{a89_seq}\n>{ev_id}\n{ev_seq}\n")


def run_mafft(mafft: Path, pair_fasta: Path, out_alignment: Path, out_log: Path) -> None:
    cmd = [str(mafft), "--localpair", "--maxiterate", "1000", str(pair_fasta)]
    proc = subprocess.run(cmd, check=True, text=True, capture_output=True)
    out_alignment.write_text(proc.stdout)
    out_log.write_text(proc.stderr)


def alignment_maps(alignment: Path) -> tuple[dict[str, str], dict[str, list[int | None]]]:
    records = list(SeqIO.parse(str(alignment), "fasta"))
    if len(records) != 2:
        raise ValueError(f"Expected 2 aligned records, observed {len(records)}")
    seqs = {rec.id: str(rec.seq) for rec in records}
    maps: dict[str, list[int | None]] = {}
    for rec in records:
        pos = 0
        cols: list[int | None] = []
        for aa in str(rec.seq):
            if aa == "-":
                cols.append(None)
            else:
                pos += 1
                cols.append(pos)
        maps[rec.id] = cols
    lengths = {rec.id: max(x for x in maps[rec.id] if x is not None) for rec in records}
    if sorted(lengths.values()) != [321, 329]:
        raise ValueError(f"Unexpected mature 2C lengths in alignment: {lengths}")
    return seqs, maps


def choose_ids(seqs: dict[str, str], maps: dict[str, list[int | None]]) -> tuple[str, str]:
    by_len = {max(x for x in maps[k] if x is not None): k for k in maps}
    return by_len[321], by_len[329]


def residue_columns(res_map: list[int | None]) -> dict[int, int]:
    return {pos: i for i, pos in enumerate(res_map) if pos is not None}


def compact_numbers(values: list[int]) -> str:
    if not values:
        return ""
    values = sorted(set(values))
    ranges = []
    start = prev = values[0]
    for v in values[1:]:
        if v == prev + 1:
            prev = v
            continue
        ranges.append(f"{start}" if start == prev else f"{start}-{prev}")
        start = prev = v
    ranges.append(f"{start}" if start == prev else f"{start}-{prev}")
    return ",".join(ranges)


def local_context(seq: str, center_left: int | None, span: int = 5) -> str:
    if center_left is None:
        return ""
    lo = max(1, center_left - span)
    hi = min(len(seq), center_left + 1 + span)
    text = seq[lo - 1 : hi]
    bar = center_left - lo + 1
    return f"{lo}:{text[:bar]}|{text[bar:]}:{hi}"


def parse_source_tables(raw_dir: Path) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    ins = pd.read_csv(raw_dir / "Scores_Insertional_Handle_Fullproteome.csv")
    dele = pd.read_csv(raw_dir / "Scores_Deletions_Fullproteome.csv")
    dms = pd.read_csv(raw_dir / "Fullproteome_P2_DMS_Enrich2_long.csv")
    ins = ins[(ins["indel"] > 1111) & (ins["indel"] < 1441)].copy()
    dele = dele[(dele["indel"] > 1111) & (dele["indel"] < 1441)].copy()
    dms = dms[(dms["position"] > 1111) & (dms["position"] < 1441)].copy()
    ins["ev71_2c_position"] = ins["indel"] - 1111
    dele["ev71_2c_position"] = dele["indel"] - 1111
    dms["ev71_2c_position"] = dms["position"] - 1111
    return ins, dele, dms


def score_at(df: pd.DataFrame, pos: int | None, design: str | None = None) -> float | None:
    if pos is None:
        return None
    sub = df[df["ev71_2c_position"] == pos]
    if design is not None:
        sub = sub[sub["dataset"] == design]
    if sub.empty:
        return None
    val = sub["score"].iloc[0]
    if pd.isna(val):
        return None
    return float(val)


def fmt_float(value: float | None, digits: int = 6) -> str:
    if value is None or (isinstance(value, float) and math.isnan(value)):
        return ""
    return f"{value:.{digits}f}"


def fmt_list(values: list[float]) -> str:
    return ";".join(fmt_float(v) for v in values if v is not None and not math.isnan(v))


def classify_insert(score: float | None) -> str:
    if score is None:
        return "no_direct_data"
    if score > 0:
        return "direct_insert_tolerated_score_gt0"
    if score >= -2:
        return "direct_insert_partly_deleterious"
    return "direct_insert_strongly_deleterious"


def classify_deletion_context(score: float | None) -> str:
    if score is None:
        return "no_direct_deletion_context"
    if score > 0:
        return "deletion_context_tolerated_score_gt0"
    if score >= -1:
        return "deletion_context_partly_deleterious"
    return "deletion_context_strongly_deleterious"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--raw-dir", type=Path, default=Path("data/raw/direct_indel_001"))
    ap.add_argument("--a89-fasta", type=Path, default=Path("references/HRV_A89_2C_reference_sequence.fasta"))
    ap.add_argument("--ev71-fasta", type=Path, default=Path("data/raw/direct_indel_001/MW298156_EV71_4643_2C.fasta"))
    ap.add_argument("--candidate-v2", type=Path, default=Path("data/candidate_junctions_v2.tsv"))
    ap.add_argument("--mafft", type=Path, default=Path(".tools/envs/hrv2c-conservation-qc/bin/mafft"))
    ap.add_argument("--pair-fasta", type=Path, default=Path("data/evA71_A89_2C_pair_v1.fasta"))
    ap.add_argument("--alignment", type=Path, default=Path("data/evA71_A89_2C_mafft_alignment_v1.fasta"))
    ap.add_argument("--alignment-log", type=Path, default=Path("results/direct_indel_001/evA71_A89_2C_mafft_v1.txt"))
    ap.add_argument("--alignment-map", type=Path, default=Path("data/evA71_A89_2C_alignment_map_v1.tsv"))
    ap.add_argument("--direct-out", type=Path, default=Path("data/evA71_2C_direct_indel_to_A89_v1.tsv"))
    ap.add_argument("--integrated-out", type=Path, default=Path("data/candidate_junctions_v3_direct_indel.tsv"))
    ap.add_argument("--source-records", type=Path, default=Path("references/direct_indel_001/source_records_v1.tsv"))
    ap.add_argument("--qc-out", type=Path, default=Path("results/direct_indel_001/direct_indel_001_qc_summary.tsv"))
    ap.add_argument("--focal-out", type=Path, default=Path("results/direct_indel_001/direct_indel_001_focal_junctions.tsv"))
    ap.add_argument("--new-candidates-out", type=Path, default=Path("results/direct_indel_001/direct_indel_001_outside_strict_candidates.tsv"))
    args = ap.parse_args()

    for path in [args.direct_out.parent, args.integrated_out.parent, args.alignment_log.parent, args.source_records.parent]:
        path.mkdir(parents=True, exist_ok=True)

    write_pair_fasta(args.a89_fasta, args.ev71_fasta, args.pair_fasta)
    run_mafft(args.mafft, args.pair_fasta, args.alignment, args.alignment_log)

    seqs, maps = alignment_maps(args.alignment)
    a89_id, ev_id = choose_ids(seqs, maps)
    a89_seq = seqs[a89_id].replace("-", "")
    ev_seq = seqs[ev_id].replace("-", "")
    a89_cols = residue_columns(maps[a89_id])
    ev_cols = residue_columns(maps[ev_id])

    with args.alignment_map.open("w", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["alignment_column_1based", "a89_residue", "a89_aa", "ev71_residue", "ev71_aa"],
            delimiter="\t",
        )
        writer.writeheader()
        for i in range(len(seqs[a89_id])):
            a_pos = maps[a89_id][i]
            e_pos = maps[ev_id][i]
            writer.writerow(
                {
                    "alignment_column_1based": i + 1,
                    "a89_residue": "" if a_pos is None else a_pos,
                    "a89_aa": "-" if a_pos is None else a89_seq[a_pos - 1],
                    "ev71_residue": "" if e_pos is None else e_pos,
                    "ev71_aa": "-" if e_pos is None else ev_seq[e_pos - 1],
                }
            )

    ins, dele, dms = parse_source_tables(args.raw_dir)
    ins_by_pos = dict(zip(ins["ev71_2c_position"], ins["score"]))

    rows = []
    exact = gap_adjacent = ambiguous = unmapped = 0
    for a_left in range(1, 321):
        a_right = a_left + 1
        left_col = a89_cols[a_left]
        right_col = a89_cols[a_right]
        e_left_same = maps[ev_id][left_col]
        e_right_same = maps[ev_id][right_col]
        ev_between = [maps[ev_id][c] for c in range(left_col, right_col + 1) if maps[ev_id][c] is not None]
        ev_before = max([maps[ev_id][c] for c in range(0, left_col + 1) if maps[ev_id][c] is not None], default=None)
        ev_after = min([maps[ev_id][c] for c in range(right_col, len(maps[ev_id])) if maps[ev_id][c] is not None], default=None)

        if e_left_same is not None and e_right_same is not None and e_right_same == e_left_same + 1:
            mapping_class = "exact_aligned"
            confidence = "high"
            source_lefts = [e_left_same]
            note = "A89 flanking residues align directly to adjacent EV-A71 2C residues"
            exact += 1
        elif ev_before is None or ev_after is None:
            mapping_class = "unmapped"
            confidence = "none"
            source_lefts = []
            note = "No bracketing EV-A71 residues in mature-2C alignment"
            unmapped += 1
        elif ev_after == ev_before + 1:
            mapping_class = "gap_adjacent"
            confidence = "medium"
            source_lefts = [ev_before]
            note = "A89 junction abuts an alignment gap but has one bracketing EV-A71 junction"
            gap_adjacent += 1
        else:
            mapping_class = "ambiguous"
            confidence = "low"
            source_lefts = list(range(ev_before, ev_after))
            note = "A89 junction spans multiple EV-A71 residues/junctions in the sequence alignment"
            ambiguous += 1

        insertion_scores = [ins_by_pos.get(e) for e in source_lefts if e in ins_by_pos]
        valid_insert = [float(x) for x in insertion_scores if x is not None and not pd.isna(x)]
        primary_insert = valid_insert[0] if len(valid_insert) == 1 else (max(valid_insert) if valid_insert else None)
        normalized = None if primary_insert is None else 2**primary_insert

        del_1_left = score_at(dele, source_lefts[0] if len(source_lefts) == 1 else None, "1AAdel")
        del_1_right = score_at(dele, (source_lefts[0] + 1) if len(source_lefts) == 1 else None, "1AAdel")
        del_2_span = score_at(dele, source_lefts[0] if len(source_lefts) == 1 else None, "2AAdel")
        del_3_spans: list[float] = []
        if len(source_lefts) == 1:
            for p in [source_lefts[0] - 1, source_lefts[0]]:
                v = score_at(dele, p, "3AAdel")
                if v is not None:
                    del_3_spans.append(v)
        deletion_candidates = [
            ("1AAdel_left_residue", del_1_left),
            ("1AAdel_right_residue", del_1_right),
            ("2AAdel_spanning_junction", del_2_span),
        ] + [(f"3AAdel_spanning_option_{i+1}", v) for i, v in enumerate(del_3_spans)]
        deletion_candidates = [(k, v) for k, v in deletion_candidates if v is not None and not math.isnan(v)]
        best_deletion_design = ""
        best_deletion_score = None
        if deletion_candidates:
            best_deletion_design, best_deletion_score = max(deletion_candidates, key=lambda kv: kv[1])

        flank_positions = []
        if len(source_lefts) == 1:
            flank_positions = [source_lefts[0], source_lefts[0] + 1]
        sub = dms[dms["ev71_2c_position"].isin(flank_positions)] if flank_positions else pd.DataFrame()
        sub_mean = None if sub.empty else float(sub["score"].mean(skipna=True))

        rows.append(
            {
                "a89_junction": f"{a_left}|{a_right}",
                "a89_left_residue": a_left,
                "a89_left_aa": a89_seq[a_left - 1],
                "a89_right_residue": a_right,
                "a89_right_aa": a89_seq[a_right - 1],
                "eva71_source_junctions": ";".join(f"{e}|{e+1}" for e in source_lefts),
                "eva71_source_left_positions": compact_numbers(source_lefts),
                "mapping_class": mapping_class,
                "mapping_confidence": confidence,
                "mapping_note": note,
                "a89_local_context": local_context(a89_seq, a_left),
                "eva71_local_context": local_context(ev_seq, source_lefts[0] if len(source_lefts) == 1 else None),
                "eva71_alignment_flank_left_same_column": "" if e_left_same is None else e_left_same,
                "eva71_alignment_flank_right_same_column": "" if e_right_same is None else e_right_same,
                "eva71_alignment_residues_between_a89_flanks": compact_numbers([x for x in ev_between if x is not None]),
                "insertion_design": "insertional_handle_SGRPGSLS",
                "insertion_length_aa": 8,
                "insertion_raw_log2_enrich2": fmt_float(primary_insert),
                "insertion_relative_fitness_2pow_score": fmt_float(normalized),
                "insertion_all_raw_log2_enrich2_for_mapped_sources": fmt_list(valid_insert),
                "insertion_direct_class": classify_insert(primary_insert),
                "deletion_1aa_left_raw_log2_enrich2": fmt_float(del_1_left),
                "deletion_1aa_right_raw_log2_enrich2": fmt_float(del_1_right),
                "deletion_2aa_spanning_raw_log2_enrich2": fmt_float(del_2_span),
                "deletion_3aa_spanning_raw_log2_enrich2_values": fmt_list(del_3_spans),
                "deletion_context_best_design": best_deletion_design,
                "deletion_context_best_raw_log2_enrich2": fmt_float(best_deletion_score),
                "deletion_context_class": classify_deletion_context(best_deletion_score),
                "substitution_flank_mean_raw_log2_enrich2": fmt_float(sub_mean),
                "source_identifier": "Bakhache_2024_NatMicrobiol_Dryad_10.5061_dryad.866t1g1xm_QVEU_eva71_dimple_c99331a6",
            }
        )

    direct = pd.DataFrame(rows)
    if len(direct) != 320 or direct["a89_junction"].nunique() != 320:
        raise ValueError("Direct mapping table must cover 320 unique A89 junctions")
    direct.to_csv(args.direct_out, sep="\t", index=False)

    v2 = pd.read_csv(args.candidate_v2, sep="\t")
    merged = v2.merge(direct, left_on="junction", right_on="a89_junction", how="left", validate="one_to_one")
    if len(merged) != 320:
        raise ValueError(f"Integrated table row count mismatch: {len(merged)}")

    def integrated_class(row: pd.Series) -> str:
        if row["mapping_class"] != "exact_aligned":
            return "mapping_uncertain"
        if row["insertion_direct_class"] == "no_direct_data":
            return "no_direct_data"
        if row["insertion_direct_class"] == "direct_insert_tolerated_score_gt0":
            if not bool(row.get("strict_structural_pass", False)):
                return "new_candidate_outside_strict_gate"
            return "convergent_support"
        if bool(row.get("strict_structural_pass", False)) or row.get("focal_junction", False):
            return "experimental_conflict"
        return "direct_experiment_unfavorable"

    merged["direct_indel_integration_class"] = merged.apply(integrated_class, axis=1)
    merged["direct_indel_final_state_contribution"] = merged["direct_indel_integration_class"]
    merged.to_csv(args.integrated_out, sep="\t", index=False)

    focal = ["287|288", "288|289", "289|290", "290|291", "248|249", "256|257", "223|224", "245|246", "250|251"]
    merged[merged["junction"].isin(focal)].to_csv(args.focal_out, sep="\t", index=False)
    merged[
        (merged["strict_structural_pass"] == False)
        & (merged["direct_indel_integration_class"] == "new_candidate_outside_strict_gate")
    ].to_csv(args.new_candidates_out, sep="\t", index=False)

    source_files = [
        "dryad_dataset_metadata.json",
        "dryad_version_311424_files.json",
        "crossref_10.1038_s41564-024-01871-y.json",
        "MW298156.gb",
        "MW298156_EV71_4643_2C.fasta",
        "EV71_4643_Features.csv",
        "Scores_Insertional_Handle_Fullproteome.csv",
        "Scores_Deletions_Fullproteome.csv",
        "Fullproteome_P2_DMS_Enrich2_long.csv",
        "merged_df_indel_DMS.csv",
        "Data_Generation_Markdown_InDel_Manuscript.r",
        "eva71_dimple_README.md",
    ]
    with args.source_records.open("w", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["local_path", "sha256", "size_bytes", "source_url_or_origin", "role"],
            delimiter="\t",
        )
        writer.writeheader()
        for fn in source_files:
            p = args.raw_dir / fn
            writer.writerow(
                {
                    "local_path": str(p),
                    "sha256": sha256(p) if p.exists() else "",
                    "size_bytes": p.stat().st_size if p.exists() else "",
                    "source_url_or_origin": "Dryad API/GitHub QVEU/eva71_dimple/NCBI/Crossref",
                    "role": "DIRECT_INDEL_001 source/provenance",
                }
            )

    qc = pd.DataFrame(
        [
            ("a89_junction_rows", len(direct)),
            ("mapping_exact_aligned", int((direct["mapping_class"] == "exact_aligned").sum())),
            ("mapping_gap_adjacent", int((direct["mapping_class"] == "gap_adjacent").sum())),
            ("mapping_ambiguous", int((direct["mapping_class"] == "ambiguous").sum())),
            ("mapping_unmapped", int((direct["mapping_class"] == "unmapped").sum())),
            ("source_ev71_2c_insertions", len(ins)),
            ("source_ev71_2c_deletions_all_lengths", len(dele)),
            ("source_ev71_2c_substitution_scores", len(dms)),
            ("a89_junctions_with_direct_insert_score", int((direct["insertion_raw_log2_enrich2"] != "").sum())),
            ("a89_junctions_insert_score_gt0", int((pd.to_numeric(direct["insertion_raw_log2_enrich2"], errors="coerce") > 0).sum())),
            ("a89_junctions_deletion_context_score_gt0", int((pd.to_numeric(direct["deletion_context_best_raw_log2_enrich2"], errors="coerce") > 0).sum())),
            ("integrated_rows", len(merged)),
            ("integrated_experimental_conflict", int((merged["direct_indel_integration_class"] == "experimental_conflict").sum())),
            ("integrated_new_candidate_outside_strict_gate", int((merged["direct_indel_integration_class"] == "new_candidate_outside_strict_gate").sum())),
        ],
        columns=["metric", "value"],
    )
    qc.to_csv(args.qc_out, sep="\t", index=False)


if __name__ == "__main__":
    main()
