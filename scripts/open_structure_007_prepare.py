#!/usr/bin/env python3
"""Prepare OPEN_STRUCTURE_PIPELINE_007 panel and ColabFold FASTA inputs."""
from __future__ import annotations

from pathlib import Path

import pandas as pd

TIER1 = ["203|204", "224|225", "248|249", "256|257", "287|288", "288|289", "289|290", "290|291"]
NEGATIVE = ["155|156", "216|217"]
TAGS = ["MAP8", "HA", "G196_minimal", "G196_practical_GS"]


def read_fasta(path: Path) -> str:
    return "".join(line.strip() for line in path.read_text().splitlines() if not line.startswith(">"))


def insert_tag(seq: str, left_resid: int, tag: str) -> str:
    return seq[:left_resid] + tag + seq[left_resid:]


def main() -> None:
    out = Path("results/open_structure_007")
    out.mkdir(parents=True, exist_ok=True)
    seq = read_fasta(Path("references/HRV_A89_2C_reference_sequence.fasta"))
    panel = pd.read_csv("data/tag_site_modeling_panel_v1.tsv", sep="\t")
    keep = panel[panel["junction"].isin(TIER1 + NEGATIVE) & panel["tag_form"].isin(TAGS)].copy()
    keep["modeling_tier"] = keep["junction"].map(lambda j: "negative_control" if j in NEGATIVE else "tier1_mandatory")
    keep["ensemble_plan"] = keep.apply(
        lambda r: "deep_followup" if r["junction"] in {"289|290", "290|291"} and r["tag_form"] in {"MAP8", "G196_minimal"} else "shallow_screen",
        axis=1,
    )
    keep["full_sequence"] = keep.apply(lambda r: insert_tag(seq, int(r["left_resid"]), r["tag_sequence"]), axis=1)
    keep["sequence_length"] = keep["full_sequence"].str.len()
    wt = {
        "construct_id": "A89_2C_WT",
        "junction": "WT",
        "left_resid": "",
        "right_resid": "",
        "left_aa": "",
        "right_aa": "",
        "tag_form": "WT",
        "tag_sequence": "",
        "tag_length": 0,
        "review_role_v2": "WT_control",
        "panel_inclusion_rationale": "WT A89 2C proof-of-life and structural reference",
        "candidate_class_v5_plm_gpu": "WT_control",
        "functional_tier": "WT_control",
        "mapping_class": "WT_control",
        "strict_structural_pass": "",
        "insertion_design": "",
        "insertion_length_aa": "",
        "insertion_raw_log2_enrich2": "",
        "insertion_direct_class": "",
        "sub_window_mean": "",
        "independent_indel_event_lower_bound": "",
        "plm_percentile_within_tag": "",
        "plm_rank_within_tag": "",
        "plm_delta_mean_pll_insert_minus_wt": "",
        "plm_inserted_tag_mean_pll": "",
        "best_tag_form": "",
        "worst_tag_form": "",
        "plm_percentile_mean": "",
        "plm_percentile_min": "",
        "plm_percentile_range": "",
        "plm_consensus_class": "",
        "both_AF_coil": "",
        "min_hex_coil_fraction": "",
        "min_AF_rSASA": "",
        "min_hexamer_mean_rSASA": "",
        "max_any_chain_burial_fraction": "",
        "min_interprotomer_heavy_atom_A": "",
        "min_mean_pore_radial_A": "",
        "min_AF_CA_pLDDT": "",
        "modeling_tier": "WT_control",
        "ensemble_plan": "smoke_and_reference",
        "full_sequence": seq,
        "sequence_length": len(seq),
    }
    final = pd.concat([pd.DataFrame([wt]), keep], ignore_index=True)
    final.to_csv("data/tag_site_structure_panel_v3_open.tsv", sep="\t", index=False)

    with (out / "colabfold_wt_input.fasta").open("w") as fh:
        fh.write(f">A89_2C_WT\n{seq}\n")
    with (out / "colabfold_tier1_input.fasta").open("w") as fh:
        for _, r in final.iterrows():
            if r["construct_id"] == "A89_2C_WT":
                continue
            fh.write(f">{r['construct_id']}\n{r['full_sequence']}\n")
    manifest = final[["construct_id", "junction", "tag_form", "tag_sequence", "sequence_length", "modeling_tier", "ensemble_plan"]].copy()
    manifest.to_csv(out / "sequence_manifest_v3_open.tsv", sep="\t", index=False)
    if len(final) != 41:
        raise SystemExit(f"Expected 41 panel rows, observed {len(final)}")
    if final["construct_id"].duplicated().any():
        raise SystemExit("Duplicate construct_id in structure panel")


if __name__ == "__main__":
    main()
