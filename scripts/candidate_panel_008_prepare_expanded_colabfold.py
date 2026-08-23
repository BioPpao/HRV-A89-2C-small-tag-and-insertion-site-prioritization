#!/usr/bin/env python3
"""Prepare cached A3M inputs for CANDIDATE_PANEL_EXPANSION_008 replication."""
from pathlib import Path
import shutil

import pandas as pd


def main() -> None:
    panel = pd.read_csv("data/expanded_structure_replication_panel_v1.tsv", sep="\t")
    src = Path("results/open_structure_007/tier1_shallow")
    dst = Path("results/candidate_panel_008/expanded_colabfold_input")
    dst.mkdir(parents=True, exist_ok=True)
    missing = []
    targets = []
    for cid in panel["construct_id"]:
        a3m = src / f"{cid}.a3m"
        if not a3m.exists():
            missing.append(cid)
            continue
        shutil.copy2(a3m, dst / f"{cid}.a3m")
        targets.append(cid)
    Path("results/candidate_panel_008/expanded_colabfold_targets.txt").write_text("\n".join(targets) + "\n")
    if missing:
        Path("results/candidate_panel_008/expanded_colabfold_missing_a3m.txt").write_text("\n".join(missing) + "\n")
    if len(targets) < 12:
        raise SystemExit(f"Too few cached A3M targets prepared: {len(targets)}")


if __name__ == "__main__":
    main()
