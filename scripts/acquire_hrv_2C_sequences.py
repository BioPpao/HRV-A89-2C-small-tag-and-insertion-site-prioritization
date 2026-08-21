#!/usr/bin/env python3
"""Acquire HRV 2C sequences from UniProtKB plus NCBI Taxonomy provenance."""

from __future__ import print_function

import argparse
import datetime
import json
import os
import sys
import time
import xml.etree.ElementTree as ET

import requests

from hrv2c_conservation_lib import clean_seq, parse_type_label, read_fasta, sw_extract, write_fasta


UNIPROT = "https://rest.uniprot.org/uniprotkb/search"
NCBI_ESEARCH = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
NCBI_EFETCH = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"


def get_json(url, params=None):
    r = requests.get(url, params=params, timeout=60)
    r.raise_for_status()
    return r


def uniprot_records(taxonomy_id, query_extra):
    query = "taxonomy_id:%s AND %s" % (taxonomy_id, query_extra)
    url = UNIPROT
    params = {"query": query, "format": "json", "size": "500"}
    while url:
        r = get_json(url, params=params)
        data = r.json()
        for item in data.get("results", []):
            yield item
        link = r.headers.get("Link", "")
        next_url = None
        for part in link.split(","):
            if 'rel="next"' in part:
                next_url = part.split(";")[0].strip()[1:-1]
        url = next_url
        params = None


def taxonomy_rows(taxonomy_id, species_prefix):
    r = get_json(NCBI_ESEARCH, {
        "db": "taxonomy",
        "term": "txid%s[Subtree]" % taxonomy_id,
        "retmode": "json",
        "retmax": "10000",
    })
    ids = r.json().get("esearchresult", {}).get("idlist", [])
    rows = []
    if not ids:
        return rows
    r = get_json(NCBI_EFETCH, {
        "db": "taxonomy",
        "id": ",".join(ids),
        "retmode": "xml",
    })
    root = ET.fromstring(r.text)
    for taxon in root.findall(".//Taxon"):
        tid = taxon.findtext("TaxId", "")
        name = taxon.findtext("ScientificName", "")
        rank = taxon.findtext("Rank", "")
        label = parse_type_label(name, species_prefix)
        rows.append({
            "taxonomy_id": tid,
            "scientific_name": name,
            "rank": rank,
            "type_label": label,
        })
    return rows


def chain_2c(record):
    seq = clean_seq(record.get("sequence", {}).get("value", ""))
    for feat in record.get("features", []):
        if feat.get("type") != "Chain":
            continue
        if feat.get("description") != "Protein 2C":
            continue
        loc = feat.get("location", {})
        start = loc.get("start", {})
        end = loc.get("end", {})
        if start.get("modifier") != "EXACT" or end.get("modifier") != "EXACT":
            continue
        s = int(start.get("value"))
        e = int(end.get("value"))
        return seq[s - 1:e], s, e, "uniprot_chain_exact", 1.0, 1.0
    return None


def record_meta(record, species_prefix):
    org = record.get("organism", {})
    organism = org.get("scientificName", "")
    taxon = str(org.get("taxonId", ""))
    accession = record.get("primaryAccession", "")
    entry_type = record.get("entryType", "")
    length = str(record.get("sequence", {}).get("length", ""))
    type_label = parse_type_label(organism + " " + record.get("uniProtkbId", ""), species_prefix)
    return accession, organism, taxon, entry_type, length, type_label


def unknown_fraction(seq):
    if not seq:
        return 1.0
    bad = sum(1 for c in seq if c not in "ACDEFGHIKLMNPQRSTVWY")
    return bad / float(len(seq))


def choose_primary(retained, reference_id):
    best = {}
    for row in retained:
        label = row["type_label"]
        rank = (
            0 if row["sequence_id"] == reference_id else 1,
            0 if row["extraction_method"] == "uniprot_chain_exact" else 1,
            0 if "reviewed" in row["entry_type"] else 1,
            abs(int(row["sequence_length"]) - 321),
            row["accession"],
        )
        if label not in best or rank < best[label][0]:
            best[label] = (rank, row)
    return [best[k][1] for k in sorted(best)]


def write_metadata(rows, path):
    fields = [
        "sequence_id", "accession", "source_database", "organism", "taxonomy_id",
        "type_label", "entry_type", "polyprotein_length", "sequence_length",
        "boundary_start", "boundary_end", "extraction_method", "boundary_confidence",
        "alignment_ref_coverage", "alignment_identity", "unknown_fraction",
        "completeness", "retain", "retain_reason", "exclude_reason",
        "retrieval_date",
    ]
    with open(path, "w") as out:
        out.write("\t".join(fields) + "\n")
        for row in rows:
            out.write("\t".join(str(row.get(f, "")) for f in fields) + "\n")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--species", required=True, choices=["A", "B", "C"])
    ap.add_argument("--taxonomy-id", required=True)
    ap.add_argument("--reference-fasta", default="references/HRV_A89_2C_reference_sequence.fasta")
    ap.add_argument("--out-prefix", required=True)
    ap.add_argument("--data-sources-md", default=None)
    ap.add_argument("--query-extra", default='protein_name:"Protein 2C"')
    args = ap.parse_args()

    retrieval_date = datetime.date.today().isoformat()
    ref_name, ref_seq = read_fasta(args.reference_fasta)[0]
    if len(ref_seq) != 321:
        raise SystemExit("authoritative A89 sequence length != 321")

    expected = taxonomy_rows(args.taxonomy_id, args.species)
    os.makedirs(os.path.dirname(args.out_prefix), exist_ok=True)
    with open(args.out_prefix + "_taxonomy.tsv", "w") as out:
        out.write("taxonomy_id\tscientific_name\trank\ttype_label\n")
        for row in expected:
            out.write("%s\t%s\t%s\t%s\n" % (
                row["taxonomy_id"], row["scientific_name"], row["rank"], row["type_label"]))

    all_rows = []
    retained = []
    seen_accessions = set()
    source_count = 0
    for rec in uniprot_records(args.taxonomy_id, args.query_extra):
        source_count += 1
        accession, organism, taxon, entry_type, poly_len, type_label = record_meta(rec, args.species)
        if accession in seen_accessions:
            continue
        seen_accessions.add(accession)
        seq = None
        start = ""
        end = ""
        method = ""
        coverage = ""
        identity = ""
        chain = chain_2c(rec)
        if chain:
            seq, start, end, method, coverage, identity = chain
            confidence = "high"
        else:
            target = clean_seq(rec.get("sequence", {}).get("value", ""))
            hit = sw_extract(ref_seq, target)
            if hit:
                seq = hit["sequence"]
                start = hit["target_start"]
                end = hit["target_end"]
                method = "a89_local_alignment_provisional"
                coverage = "%.4f" % hit["ref_coverage"]
                identity = "%.4f" % hit["identity"]
                confidence = "provisional"
            else:
                confidence = "none"
        retain = False
        exclude = []
        if not seq:
            exclude.append("no_2C_boundary_or_alignment_hit")
            seq = ""
        if "*" in seq:
            exclude.append("internal_stop")
        if len(seq) < 285 or len(seq) > 360:
            exclude.append("length_outside_285_360")
        if unknown_fraction(seq) > 0.05:
            exclude.append("unknown_fraction_gt_0.05")
        if type_label == "ambiguous":
            exclude.append("ambiguous_type_label")
        if method == "a89_local_alignment_provisional":
            try:
                if float(coverage) < 0.95 or float(identity) < 0.45:
                    exclude.append("weak_A89_alignment")
            except ValueError:
                exclude.append("weak_A89_alignment")
        if not exclude:
            retain = True
        seq_id = "%s|%s|%s" % (accession, type_label, method or "no_2C")
        row = {
            "sequence_id": seq_id,
            "accession": accession,
            "source_database": "UniProtKB",
            "organism": organism,
            "taxonomy_id": taxon,
            "type_label": type_label,
            "entry_type": entry_type,
            "polyprotein_length": poly_len,
            "sequence_length": len(seq),
            "boundary_start": start,
            "boundary_end": end,
            "extraction_method": method,
            "boundary_confidence": confidence,
            "alignment_ref_coverage": coverage,
            "alignment_identity": identity,
            "unknown_fraction": "%.4f" % unknown_fraction(seq),
            "completeness": "complete_2C" if retain else "excluded",
            "retain": "True" if retain else "False",
            "retain_reason": "traceable_2C_sequence" if retain else "",
            "exclude_reason": ";".join(exclude),
            "retrieval_date": retrieval_date,
            "sequence": seq,
        }
        all_rows.append(row)
        if retain:
            retained.append(row)
        time.sleep(0.02)

    reference_id = "A89_REF|A89|repository_authoritative"
    if args.species == "A":
        ref_row = {
            "sequence_id": reference_id,
            "accession": "repository_reference",
            "source_database": "project_repository",
            "organism": "HRV-A89 authoritative project 2C",
            "taxonomy_id": "650130",
            "type_label": "A89",
            "entry_type": "curated_project_reference",
            "polyprotein_length": "",
            "sequence_length": len(ref_seq),
            "boundary_start": "1",
            "boundary_end": "321",
            "extraction_method": "repository_authoritative_2C",
            "boundary_confidence": "authoritative",
            "alignment_ref_coverage": "1.0000",
            "alignment_identity": "1.0000",
            "unknown_fraction": "0.0000",
            "completeness": "complete_2C",
            "retain": "True",
            "retain_reason": "authoritative_A89_anchor",
            "exclude_reason": "",
            "retrieval_date": retrieval_date,
            "sequence": ref_seq,
        }
        retained.insert(0, ref_row)
        all_rows.insert(0, ref_row)

    primary = choose_primary(retained, reference_id) if args.species == "A" else choose_primary(retained, "")
    write_fasta([(r["sequence_id"], r["sequence"]) for r in primary], args.out_prefix + "_sequences.fasta")
    write_metadata(primary, args.out_prefix + "_sequence_metadata.tsv")
    write_fasta([(r["sequence_id"], r["sequence"]) for r in retained], args.out_prefix + "_expanded_sequences.fasta")
    write_metadata(retained, args.out_prefix + "_expanded_metadata.tsv")
    write_metadata(all_rows, args.out_prefix + "_all_retrieval_metadata.tsv")

    observed = set(r["type_label"] for r in primary)
    expected_types = sorted(set(r["type_label"] for r in expected if r["type_label"] != "ambiguous"))
    missing = [x for x in expected_types if x not in observed]
    summary_path = args.out_prefix + "_acquisition_summary.tsv"
    with open(summary_path, "w") as out:
        out.write("metric\tvalue\n")
        out.write("species\tHRV-%s\n" % args.species)
        out.write("taxonomy_id\t%s\n" % args.taxonomy_id)
        out.write("retrieval_date\t%s\n" % retrieval_date)
        out.write("uniprot_query\t%s\n" % args.query_extra)
        out.write("source_records_seen\t%s\n" % source_count)
        out.write("retained_expanded_sequences\t%s\n" % len(retained))
        out.write("primary_type_representatives\t%s\n" % len(primary))
        out.write("ncbi_taxonomy_subtree_rows\t%s\n" % len(expected))
        out.write("expected_type_labels\t%s\n" % len(expected_types))
        out.write("missing_expected_type_labels\t%s\n" % len(missing))
        out.write("missing_type_labels\t%s\n" % ",".join(missing[:200]))

    if args.data_sources_md:
        with open(args.data_sources_md, "w") as out:
            out.write("# CONSERVATION_001 data sources\n\n")
            out.write("Retrieval date: `%s`.\n\n" % retrieval_date)
            out.write("## Primary source\n\n")
            out.write("- UniProtKB REST API, query `%s AND %s`.\n" % (args.taxonomy_id, args.query_extra))
            out.write("- NCBI Taxonomy E-utilities subtree query `txid%s[Subtree]`.\n" % args.taxonomy_id)
            out.write("- Project A89 authoritative FASTA: `%s`.\n\n" % args.reference_fasta)
            out.write("## Boundary rule\n\n")
            out.write("Exact UniProt `Chain: Protein 2C` coordinates were used when present. ")
            out.write("For records lacking mature-chain features, a provisional A89 local-alignment extraction was used only when coverage and identity QC passed. ")
            out.write("This fallback is weaker than annotated mature products and is marked in metadata.\n\n")
            out.write("## Output metadata\n\n")
            out.write("- `%s_all_retrieval_metadata.tsv`\n" % args.out_prefix)
            out.write("- `%s_acquisition_summary.tsv`\n" % args.out_prefix)
            out.write("- `%s_taxonomy.tsv`\n" % args.out_prefix)


if __name__ == "__main__":
    main()
