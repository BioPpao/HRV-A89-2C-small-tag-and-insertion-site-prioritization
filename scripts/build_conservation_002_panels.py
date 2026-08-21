#!/usr/bin/env python3
"""Build ICTV-reconciled HRV-A 2C panels for CONSERVATION_002."""

from __future__ import annotations

import argparse
import csv
import re
import time
from pathlib import Path

import pandas as pd
import requests
from Bio import SeqIO

from hrv2c_conservation_lib import clean_seq, read_fasta, sw_extract, write_fasta


EFETCH = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"


def type_label(text: str) -> str:
    m = re.search(r"rhinovirus\s+A(\d+[A-Z]?)", str(text), re.I)
    if m:
        return "A" + m.group(1).upper()
    m = re.search(r"RV-A(\d+[A-Z]?)", str(text), re.I)
    if m:
        return "A" + m.group(1).upper()
    m = re.search(r"\bA(\d+[A-Z]?)\b", str(text), re.I)
    if m:
        return "A" + m.group(1).upper()
    return "ambiguous"


def canonical_label(label: str) -> str:
    # ICTV VMR MSL41 lists A1 and A1B. A1A records are mapped to A1 for
    # reconciliation and flagged in the table.
    return "A1" if label == "A1A" else label


def first_accession(value: str) -> str:
    text = str(value or "")
    text = re.split(r"[;\s,]+", text.strip())[0]
    return text


def read_vmr(path: Path) -> pd.DataFrame:
    df = pd.read_excel(path, sheet_name="VMR MSL41")
    mask = (
        (df["Species"].astype(str) == "Enterovirus alpharhino")
        & df["Virus name(s)"].astype(str).str.contains(r"rhinovirus A\d+", case=False, regex=True, na=False)
    )
    rows = df[mask].copy()
    rows["ictv_type_label"] = rows["Virus name(s)"].map(type_label)
    rows["vmr_primary_accession"] = rows["Virus GENBANK accession"].map(first_accession)
    rows = rows.sort_values(["ictv_type_label", "Isolate Sort"])
    return rows


def fasta_dict(path: Path) -> dict[str, str]:
    return {name: seq for name, seq in read_fasta(str(path))}


def metadata(path: Path) -> list[dict[str, str]]:
    with open(path) as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def choose_v1(rows: list[dict[str, str]], seqs: dict[str, str]) -> dict[str, dict[str, str]]:
    best: dict[str, tuple[tuple, dict[str, str]]] = {}
    for row in rows:
        if row.get("retain") != "True":
            continue
        label = canonical_label(row["type_label"])
        if row["sequence_id"] not in seqs:
            continue
        rank = (
            0 if row["extraction_method"] in ("repository_authoritative_2C", "uniprot_chain_exact") else 1,
            abs(int(row["sequence_length"]) - 321),
            row["sequence_id"],
        )
        if label not in best or rank < best[label][0]:
            best[label] = (rank, row)
    return {k: v[1] for k, v in best.items()}


def efetch_genbank(accessions: list[str]) -> list:
    records = []
    for i in range(0, len(accessions), 20):
        batch = [a for a in accessions[i : i + 20] if a]
        if not batch:
            continue
        r = requests.get(
            EFETCH,
            params={"db": "nuccore", "id": ",".join(batch), "rettype": "gb", "retmode": "text"},
            timeout=120,
        )
        r.raise_for_status()
        tmp = Path("data/ictv/_tmp_efetch.gb")
        tmp.write_text(r.text)
        records.extend(list(SeqIO.parse(str(tmp), "genbank")))
        tmp.unlink(missing_ok=True)
        time.sleep(0.4)
    return records


def polyprotein_translation(record) -> str:
    translations = []
    for feature in record.features:
        if feature.type != "CDS":
            continue
        quals = feature.qualifiers
        prod = " ".join(quals.get("product", [])).lower()
        if "translation" not in quals:
            continue
        seq = clean_seq(quals["translation"][0])
        if "polyprotein" in prod or len(seq) > 1500:
            translations.append(seq)
    if not translations:
        return ""
    return sorted(translations, key=len, reverse=True)[0]


def write_meta(rows: list[dict[str, str]], path: Path) -> None:
    fields = [
        "sequence_id",
        "type_label",
        "source_database",
        "source_accession",
        "organism",
        "sequence_length",
        "extraction_method",
        "boundary_confidence",
        "alignment_ref_coverage",
        "alignment_identity",
        "inferred_start",
        "inferred_end",
        "retain_reason",
        "provenance_note",
    ]
    with path.open("w") as out:
        w = csv.DictWriter(out, fieldnames=fields, delimiter="\t", lineterminator="\n")
        w.writeheader()
        w.writerows(rows)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--vmr-xlsx", required=True, type=Path)
    ap.add_argument("--reference-fasta", default="references/HRV_A89_2C_reference_sequence.fasta", type=Path)
    ap.add_argument("--v1-primary-fasta", default="data/hrvA_2C_sequences.fasta", type=Path)
    ap.add_argument("--v1-primary-metadata", default="data/hrvA_2C_sequence_metadata.tsv", type=Path)
    ap.add_argument("--v1-expanded-fasta", default="data/hrvA_2C_expanded_sequences.fasta", type=Path)
    ap.add_argument("--v1-expanded-metadata", default="data/hrvA_2C_expanded_metadata.tsv", type=Path)
    ap.add_argument("--out-prefix", default="data/hrvA_2C_v2")
    args = ap.parse_args()

    out_prefix = Path(args.out_prefix)
    ref_name, ref_seq = read_fasta(str(args.reference_fasta))[0]
    if len(ref_seq) != 321:
        raise SystemExit("authoritative A89 sequence length != 321")

    vmr = read_vmr(args.vmr_xlsx)
    vmr.to_csv("data/hrvA_type_universe_ictv.tsv", sep="\t", index=False)
    ictv_types = list(vmr["ictv_type_label"])
    if len(set(ictv_types)) != len(ictv_types):
        raise SystemExit("duplicate ICTV type labels in VMR extraction")

    v1p = metadata(args.v1_primary_metadata)
    v1e = metadata(args.v1_expanded_metadata)
    v1pseq = fasta_dict(args.v1_primary_fasta)
    v1eseq = fasta_dict(args.v1_expanded_fasta)
    best_v1 = choose_v1(v1e, v1eseq)

    records = efetch_genbank(list(vmr["vmr_primary_accession"]))
    by_acc = {r.id.split(".")[0]: r for r in records}
    by_acc.update({r.id: r for r in records})

    full_rows: list[dict[str, str]] = []
    full_fasta: list[tuple[str, str]] = []
    exact_rows: list[dict[str, str]] = []
    exact_fasta: list[tuple[str, str]] = []
    recon = []
    vmr_extract = {}

    for _, row in vmr.iterrows():
        label = row["ictv_type_label"]
        acc = row["vmr_primary_accession"]
        selected = None
        selected_seq = ""
        selected_note = ""
        method = ""
        confidence = ""
        cov = ""
        ident = ""
        start = ""
        end = ""

        if label == "A89":
            selected = "A89_REF|A89|repository_authoritative"
            selected_seq = ref_seq
            method = "repository_authoritative_2C"
            confidence = "authoritative"
            cov = ident = "1.0000"
            start, end = "1", "321"
            selected_note = "project A89 reference used as coordinate anchor"
        else:
            rec = by_acc.get(acc) or by_acc.get(acc.split(".")[0])
            pp = polyprotein_translation(rec) if rec else ""
            hit = sw_extract(ref_seq, pp) if pp else None
            if hit and hit["ref_coverage"] >= 0.95 and hit["identity"] >= 0.45 and 285 <= len(hit["sequence"]) <= 360:
                selected = f"VMR_{acc}|{label}|a89_local_alignment_provisional"
                selected_seq = hit["sequence"]
                method = "vmr_genbank_polyprotein_a89_local_alignment_provisional"
                confidence = "provisional"
                cov = f"{hit['ref_coverage']:.4f}"
                ident = f"{hit['identity']:.4f}"
                start, end = str(hit["target_start"]), str(hit["target_end"])
                selected_note = "VMR GenBank accession polyprotein extracted by A89 local alignment"
            elif label in best_v1:
                b = best_v1[label]
                selected = f"{b['sequence_id']}|v1_reused"
                selected_seq = v1eseq[b["sequence_id"]]
                method = b["extraction_method"]
                confidence = b["boundary_confidence"]
                cov = b["alignment_ref_coverage"]
                ident = b["alignment_identity"]
                start, end = b["boundary_start"], b["boundary_end"]
                selected_note = "V1 retained sequence reused because VMR extraction failed"
        if not selected_seq:
            recon.append({
                "ictv_type_label": label,
                "vmr_accession": acc,
                "v1_best_sequence_id": best_v1.get(label, {}).get("sequence_id", ""),
                "v1_expanded_count": sum(1 for x in v1e if canonical_label(x.get("type_label", "")) == label and x.get("retain") == "True"),
                "selected_full_panel_sequence_id": "",
                "selected_full_panel_method": "",
                "exact_subset_sequence_id": "",
                "mapping_status": "missing_no_passing_2C_extraction",
                "note": "No passing VMR/V1 2C extraction",
            })
            continue
        meta = {
            "sequence_id": selected,
            "type_label": label,
            "source_database": "ICTV_VMR+NCBI_GenBank" if selected.startswith("VMR_") else "project_or_UniProtKB",
            "source_accession": acc,
            "organism": row["Virus name(s)"],
            "sequence_length": str(len(selected_seq)),
            "extraction_method": method,
            "boundary_confidence": confidence,
            "alignment_ref_coverage": cov,
            "alignment_identity": ident,
            "inferred_start": start,
            "inferred_end": end,
            "retain_reason": "ictv_type_balanced_v2",
            "provenance_note": selected_note,
        }
        full_rows.append(meta)
        full_fasta.append((selected, selected_seq))
        vmr_extract[label] = meta

    # Exact/high-confidence subset from V1 exact rows, reconciled to ICTV labels.
    seen_exact = set()
    for row in v1e:
        if row.get("extraction_method") not in ("repository_authoritative_2C", "uniprot_chain_exact"):
            continue
        label = canonical_label(row["type_label"])
        if label not in set(ictv_types) or label in seen_exact:
            continue
        sid = row["sequence_id"]
        if sid not in v1eseq:
            continue
        eid = sid if label == row["type_label"] else sid.replace("|A1A|", "|A1|")
        meta = {
            "sequence_id": eid,
            "type_label": label,
            "source_database": row["source_database"],
            "source_accession": row["accession"],
            "organism": row["organism"],
            "sequence_length": row["sequence_length"],
            "extraction_method": row["extraction_method"],
            "boundary_confidence": row["boundary_confidence"],
            "alignment_ref_coverage": row["alignment_ref_coverage"],
            "alignment_identity": row["alignment_identity"],
            "inferred_start": row["boundary_start"],
            "inferred_end": row["boundary_end"],
            "retain_reason": "exact_or_authoritative_boundary_subset",
            "provenance_note": "A1A exact record reconciled to ICTV A1" if row["type_label"] == "A1A" else "exact mature 2C boundary",
        }
        exact_rows.append(meta)
        exact_fasta.append((eid, v1eseq[sid]))
        seen_exact.add(label)

    exact_by_label = {r["type_label"]: r["sequence_id"] for r in exact_rows}
    full_by_label = {r["type_label"]: r["sequence_id"] for r in full_rows}
    v1_counts = {label: sum(1 for x in v1e if canonical_label(x.get("type_label", "")) == label and x.get("retain") == "True") for label in ictv_types}
    for _, row in vmr.iterrows():
        label = row["ictv_type_label"]
        recon.append({
            "ictv_type_label": label,
            "vmr_accession": row["vmr_primary_accession"],
            "v1_best_sequence_id": best_v1.get(label, {}).get("sequence_id", ""),
            "v1_expanded_count": v1_counts.get(label, 0),
            "selected_full_panel_sequence_id": full_by_label.get(label, ""),
            "selected_full_panel_method": vmr_extract.get(label, {}).get("extraction_method", ""),
            "exact_subset_sequence_id": exact_by_label.get(label, ""),
            "mapping_status": "represented_v2" if label in full_by_label else "missing_v2",
            "note": "A1A V1 records map to ICTV A1" if label == "A1" else "",
        })

    # Expanded panel: full type-balanced panel plus retained V1 official-mapped sequences not duplicate IDs.
    exp_fasta = list(full_fasta)
    exp_rows = list(full_rows)
    seen_ids = {x[0] for x in exp_fasta}
    for row in v1e:
        if row.get("retain") != "True":
            continue
        label = canonical_label(row["type_label"])
        if label not in set(ictv_types):
            continue
        sid = row["sequence_id"]
        if sid not in v1eseq:
            continue
        eid = sid if label == row["type_label"] else sid.replace("|A1A|", "|A1|")
        if eid in seen_ids:
            continue
        seen_ids.add(eid)
        exp_fasta.append((eid, v1eseq[sid]))
        exp_rows.append({
            "sequence_id": eid,
            "type_label": label,
            "source_database": row["source_database"],
            "source_accession": row["accession"],
            "organism": row["organism"],
            "sequence_length": row["sequence_length"],
            "extraction_method": row["extraction_method"],
            "boundary_confidence": row["boundary_confidence"],
            "alignment_ref_coverage": row["alignment_ref_coverage"],
            "alignment_identity": row["alignment_identity"],
            "inferred_start": row["boundary_start"],
            "inferred_end": row["boundary_end"],
            "retain_reason": "expanded_v2_reconciled_retained_v1",
            "provenance_note": "V1 retained official-mapped sequence",
        })

    write_fasta(full_fasta, str(out_prefix.with_name(out_prefix.name + "_sequences.fasta")))
    write_meta(full_rows, out_prefix.with_name(out_prefix.name + "_sequence_metadata.tsv"))
    write_fasta(exp_fasta, str(out_prefix.with_name(out_prefix.name + "_expanded_sequences.fasta")))
    write_meta(exp_rows, out_prefix.with_name(out_prefix.name + "_expanded_metadata.tsv"))
    write_fasta(exact_fasta, str(out_prefix.with_name(out_prefix.name + "_exact_boundary_sequences.fasta")))
    write_meta(exact_rows, out_prefix.with_name(out_prefix.name + "_exact_boundary_metadata.tsv"))

    pd.DataFrame(recon).drop_duplicates(["ictv_type_label"]).sort_values("ictv_type_label").to_csv(
        "data/hrvA_type_reconciliation_v2.tsv", sep="\t", index=False
    )
    with open("results/conservation_002_panel_summary.tsv", "w") as out:
        out.write("metric\tvalue\n")
        out.write(f"ictv_vmr_types\t{len(ictv_types)}\n")
        out.write(f"full_panel_sequences\t{len(full_fasta)}\n")
        out.write(f"expanded_panel_sequences\t{len(exp_fasta)}\n")
        out.write(f"exact_boundary_subset_sequences\t{len(exact_fasta)}\n")
        out.write(f"missing_full_panel_types\t{len([x for x in ictv_types if x not in full_by_label])}\n")
        out.write("missing_full_panel_type_labels\t%s\n" % ",".join([x for x in ictv_types if x not in full_by_label]))


if __name__ == "__main__":
    main()
