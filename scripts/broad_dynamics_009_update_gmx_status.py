#!/usr/bin/env python3
"""Update GROMACS manifests from on-disk task 009 outputs."""
from __future__ import annotations

from pathlib import Path

import pandas as pd

BASE = Path("results/broad_dynamics_009/gromacs")


def has(path: Path) -> bool:
    return path.exists() and path.stat().st_size > 0


def pre_status(system_id: str) -> dict:
    s = BASE / "systems" / system_id
    top = has(s / "topol.top")
    em = has(s / "em.gro")
    nvt = has(s / "nvt.gro")
    npt = has(s / "npt.gro")
    smoke = has(s / "prod_smoke.xtc") and has(s / "prod_smoke.edr") and has(s / "prod_smoke.cpt")
    return {
        "topology_status": "completed" if top else "not_completed",
        "minimization_status": "completed" if em else "not_completed",
        "nvt_status": "completed" if nvt else "not_completed",
        "npt_status": "completed" if npt else "not_completed",
        "smoke_production_status": "completed" if smoke else "not_completed",
        "qc_pass": "true" if top and em and nvt and npt and smoke else "false",
        "reason": "complete_preproduction_smoke" if top and em and nvt and npt and smoke else "missing_one_or_more_preproduction_outputs",
        "em_gro": str(s / "em.gro") if em else "NA",
        "npt_gro": str(s / "npt.gro") if npt else "NA",
        "prod_smoke_xtc": str(s / "prod_smoke.xtc") if smoke else "NA",
    }


def main() -> None:
    systems = pd.read_csv("results/broad_dynamics_009/system_manifest.tsv", sep="\t", dtype=str).fillna("")
    pre_rows = []
    for _, r in systems.iterrows():
        st = pre_status(r["system_id"])
        pre_rows.append({
            "system_id": r["system_id"],
            "construct_id": r["construct_id"],
            "junction": r["junction"],
            "tag_form": r["tag_form"],
            **st,
        })
    pd.DataFrame(pre_rows).to_csv("results/broad_dynamics_009/preproduction_qc.tsv", sep="\t", index=False)

    prod = pd.read_csv("results/broad_dynamics_009/production_manifest.tsv", sep="\t", dtype=str).fillna("")
    rows = []
    for _, r in prod.iterrows():
        r = r.to_dict()
        repdir = BASE / "systems" / r["system_id"] / f"replica_{r['replica']}"
        xtc = repdir / "prod_20ns.xtc"
        cpt = repdir / "prod_20ns.cpt"
        edr = repdir / "prod_20ns.edr"
        if has(xtc) and has(cpt) and has(edr):
            r["status"] = "completed_or_running_output_present"
            r["trajectory_path"] = str(xtc)
            r["checkpoint_path"] = str(cpt)
            r["energy_path"] = str(edr)
            r["achieved_ns"] = "20_or_check_log"
        elif has(cpt):
            r["status"] = "checkpoint_present_incomplete_or_running"
            r["trajectory_path"] = str(xtc) if has(xtc) else "NA"
            r["checkpoint_path"] = str(cpt)
            r["energy_path"] = str(edr) if has(edr) else "NA"
            r["achieved_ns"] = "unknown"
        else:
            r.setdefault("checkpoint_path", "NA")
            r.setdefault("energy_path", "NA")
            r.setdefault("achieved_ns", "0")
        rows.append(r)
    out = pd.DataFrame(rows)
    out.to_csv("results/broad_dynamics_009/production_manifest.tsv", sep="\t", index=False)
    out.rename(columns={"status": "completion_status"}).to_csv("results/broad_dynamics_009/replica_completion.tsv", sep="\t", index=False)


if __name__ == "__main__":
    main()
