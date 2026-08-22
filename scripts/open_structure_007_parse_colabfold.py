#!/usr/bin/env python3
"""Parse ColabFold outputs into compact OPEN_STRUCTURE_PIPELINE_007 TSVs."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import pandas as pd


def mean_plddt_from_pdb(path: Path) -> float:
    vals = []
    seen = set()
    for line in path.read_text(errors="ignore").splitlines():
        if not line.startswith("ATOM"):
            continue
        atom = line[12:16].strip()
        chain = line[21].strip()
        resid = line[22:26].strip()
        if atom != "CA" or (chain, resid) in seen:
            continue
        seen.add((chain, resid))
        vals.append(float(line[60:66]))
    return sum(vals) / len(vals) if vals else float("nan")


def json_scores(path: Path) -> dict[str, float | str]:
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text())
    except Exception:
        return {}
    out = {}
    for key in ["plddt", "ptm", "iptm", "ranking_confidence"]:
        if key in data:
            val = data[key]
            if isinstance(val, list):
                out[key] = sum(map(float, val)) / len(val)
            else:
                out[key] = val
    return out


def collect(input_dir: Path, panel: pd.DataFrame) -> pd.DataFrame:
    panel = panel.set_index("construct_id", drop=False)
    rows = []
    for pdb in sorted(input_dir.rglob("*.pdb")):
        name = pdb.stem
        construct = None
        for cid in panel.index:
            if name.startswith(cid.lower()) or name.startswith(cid):
                construct = cid
                break
        if construct is None:
            for cid in panel.index:
                if cid.lower() in name.lower():
                    construct = cid
                    break
        rank = re.search(r"rank_(\d+)", name)
        model = re.search(r"model_(\d+)", name)
        seed = re.search(r"seed_(\d+)", name)
        json_path = pdb.with_suffix(".json")
        score = json_scores(json_path)
        p = panel.loc[construct] if construct in panel.index else {}
        rows.append({
            "construct_id": construct or name,
            "junction": p.get("junction", ""),
            "tag_form": p.get("tag_form", ""),
            "tag_length": p.get("tag_length", ""),
            "model_file": str(pdb),
            "json_file": str(json_path) if json_path.exists() else "",
            "rank": rank.group(1) if rank else "",
            "model": model.group(1) if model else "",
            "seed": seed.group(1) if seed else "",
            "mean_ca_plddt_from_pdb": mean_plddt_from_pdb(pdb),
            "ptm": score.get("ptm", ""),
            "ranking_confidence": score.get("ranking_confidence", ""),
            "prediction_status": "completed",
        })
    return pd.DataFrame(rows)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["smoke", "batch"], required=True)
    ap.add_argument("--input-dir", type=Path, required=True)
    ap.add_argument("--panel", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()
    panel = pd.read_csv(args.panel, sep="\t")
    df = collect(args.input_dir, panel)
    if args.mode == "smoke":
        if df.empty:
            df = pd.DataFrame([{
                "construct_id": "A89_2C_WT",
                "junction": "WT",
                "tag_form": "WT",
                "tag_length": 0,
                "model_file": "",
                "json_file": "",
                "rank": "",
                "model": "",
                "seed": "",
                "mean_ca_plddt_from_pdb": "",
                "ptm": "",
                "ranking_confidence": "",
                "prediction_status": "failed_no_pdb_found",
            }])
    args.out.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(args.out, sep="\t", index=False)


if __name__ == "__main__":
    main()
