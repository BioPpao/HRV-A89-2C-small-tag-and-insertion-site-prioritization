#!/usr/bin/env python3
"""Prepare focused local multimer ColabFold inputs for task 009."""
from __future__ import annotations

from pathlib import Path

import pandas as pd

OUT = Path("results/broad_dynamics_009/local_multimer")


def read_refseq() -> str:
    return "".join(
        line.strip()
        for line in Path("references/HRV_A89_2C_reference_sequence.fasta").read_text().splitlines()
        if not line.startswith(">")
    )


def main() -> None:
    wt = read_refseq()
    manifest = pd.read_csv("results/broad_dynamics_009/local_multimer_manifest.tsv", sep="\t", dtype=str).fillna("")
    panel = pd.read_csv("data/balanced_targeted_dynamics_panel_v2.tsv", sep="\t", dtype=str).fillna("")
    panel = panel.set_index("construct_id")
    OUT.mkdir(parents=True, exist_ok=True)
    lines = []
    rows = []
    for _, r in manifest.iterrows():
        cid = r["construct_id"]
        p = panel.loc[cid]
        full = p["full_sequence"]
        target = f"{cid}_trimer_tagged_WT_WT"
        lines += [f">{target}", f"{full}:{wt}:{wt}"]
        rows.append({
            "target_id": target,
            "construct_id": cid,
            "junction": r["junction"],
            "tag_form": r["tag_form"],
            "tag_sequence": p["tag_sequence"],
            "tag_length": p["tag_length"],
            "left_resid": p["left_resid"],
            "multimer_context": "tagged_protomer_plus_two_WT_protomers",
            "sequence_mode": "single_sequence_multimer",
            "chain_order": "A=tagged_full_2C;B=WT_full_2C;C=WT_full_2C",
        })
    (OUT / "local_multimer_input.fasta").write_text("\n".join(lines) + "\n")
    pd.DataFrame(rows).to_csv(OUT / "local_multimer_targets.tsv", sep="\t", index=False)


if __name__ == "__main__":
    main()
