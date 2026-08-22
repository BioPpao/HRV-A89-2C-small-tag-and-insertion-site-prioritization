#!/usr/bin/env python3
"""Prepare cached A3M inputs for the OPEN_STRUCTURE_PIPELINE_007 deeper subset."""
from pathlib import Path
import shutil

TARGETS = [
    "A89_2C_289_290_MAP8",
    "A89_2C_289_290_G196_minimal",
    "A89_2C_290_291_MAP8",
    "A89_2C_290_291_G196_minimal",
]

src = Path("results/open_structure_007/tier1_shallow")
dst = Path("results/open_structure_007/deep_subset_input")
dst.mkdir(parents=True, exist_ok=True)
for cid in TARGETS:
    shutil.copy2(src / f"{cid}.a3m", dst / f"{cid}.a3m")
Path("results/open_structure_007/deep_subset_targets.txt").write_text("\n".join(TARGETS) + "\n")
