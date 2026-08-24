#!/usr/bin/env python3
"""Prepare GROMACS inputs for BROAD_DYNAMICS_AND_RECOVERY_009."""
from __future__ import annotations

import csv
import re
from pathlib import Path

import pandas as pd

OUT = Path("results/broad_dynamics_009/gromacs")
WT_PDB = Path("results/open_structure_007/wt_smoke/A89_2C_WT_unrelaxed_rank_001_alphafold2_ptm_model_1_seed_007.pdb")


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


def read_refseq() -> str:
    return "".join(
        line.strip()
        for line in Path("references/HRV_A89_2C_reference_sequence.fasta").read_text().splitlines()
        if not line.startswith(">")
    )


def best_model_map() -> dict[str, str]:
    manifest = pd.read_csv("results/candidate_panel_008/expanded_prediction_manifest.tsv", sep="\t", dtype=str).fillna("")
    openmm = pd.read_csv("results/candidate_panel_008/expanded_openmm_qc_v1.tsv", sep="\t", dtype=str).fillna("")
    merged = manifest.merge(openmm[["model_file", "openmm_status"]], on="model_file", how="left")
    out = {}
    for cid, g in merged.groupby("construct_id"):
        g = g.copy()
        g["rank_num"] = pd.to_numeric(g["rank"], errors="coerce").fillna(999)
        ok = g[g["openmm_status"].str.startswith("completed")]
        pick = (ok if len(ok) else g).sort_values(["rank_num", "seed"]).iloc[0]
        out[cid] = pick["model_file"]
    return out


def residue_ranges_for_system(row: dict) -> tuple[int, int]:
    if row["construct_id"] == "WT_112_321":
        return 112, 321
    left = int(row["junction"].split("|")[0])
    tag_len = int(row["tag_length"])
    return 112, 321 + tag_len


def clean_atom_line(line: str, new_serial: int) -> str:
    # GROMACS pdb2gmx is happier with one chain and blank altloc.
    return f"{line[:6]}{new_serial:5d}{line[11:16]} {line[17:21]}A{line[22:]}"


def extract_segment(src: Path, dst: Path, start: int, end: int) -> dict:
    serial = 1
    residues = set()
    atoms = 0
    lines = []
    for line in src.read_text(errors="ignore").splitlines():
        if not line.startswith("ATOM"):
            continue
        try:
            resid = int(line[22:26])
        except ValueError:
            continue
        if start <= resid <= end:
            lines.append(clean_atom_line(line, serial))
            serial += 1
            atoms += 1
            residues.add(resid)
    lines.append("TER")
    lines.append("END")
    write(dst, "\n".join(lines) + "\n")
    return {"source_pdb": str(src), "prepared_pdb": str(dst), "atom_count": atoms, "residue_count": len(residues), "source_resid_start": start, "source_resid_end": end}


def mdp_files() -> None:
    write(OUT / "mdp" / "em.mdp", """integrator = steep
emtol = 1000.0
emstep = 0.01
nsteps = 50000
cutoff-scheme = Verlet
coulombtype = PME
rcoulomb = 1.2
rvdw = 1.2
pbc = xyz
""")
    common = """dt = 0.002
nsteps = {nsteps}
nstxout-compressed = {nstx}
nstenergy = {nste}
nstlog = {nste}
continuation = {continuation}
constraint_algorithm = lincs
constraints = h-bonds
cutoff-scheme = Verlet
coulombtype = PME
rcoulomb = 1.2
rvdw = 1.2
DispCorr = EnerPres
tcoupl = V-rescale
tc-grps = Protein Non-Protein
tau_t = 1.0 1.0
ref_t = 300 300
pbc = xyz
gen_vel = {gen_vel}
gen_temp = 300
gen_seed = {seed}
"""
    write(OUT / "mdp" / "nvt.mdp", "define = -DPOSRES\n" + common.format(nsteps=25000, nstx=5000, nste=500, continuation="no", gen_vel="yes", seed=1001) + "pcoupl = no\n")
    write(OUT / "mdp" / "npt.mdp", "define = -DPOSRES\n" + common.format(nsteps=25000, nstx=5000, nste=500, continuation="yes", gen_vel="no", seed=-1) + """pcoupl = C-rescale
pcoupltype = isotropic
tau_p = 5.0
ref_p = 1.0
compressibility = 4.5e-5
refcoord_scaling = com
""")
    write(OUT / "mdp" / "prod_smoke.mdp", common.format(nsteps=50000, nstx=5000, nste=500, continuation="yes", gen_vel="no", seed=-1) + """pcoupl = C-rescale
pcoupltype = isotropic
tau_p = 5.0
ref_p = 1.0
compressibility = 4.5e-5
""")
    write(OUT / "mdp" / "prod_20ns.mdp", common.format(nsteps=10000000, nstx=50000, nste=5000, continuation="yes", gen_vel="no", seed=-1) + """pcoupl = C-rescale
pcoupltype = isotropic
tau_p = 5.0
ref_p = 1.0
compressibility = 4.5e-5
""")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    mdp_files()
    panel = pd.read_csv("data/balanced_targeted_dynamics_panel_v2.tsv", sep="\t", dtype=str).fillna("")
    systems = [{"system_id": "WT_112_321", "construct_id": "WT_112_321", "junction": "WT", "tag_form": "WT", "tag_length": "0"}]
    for r in panel[["construct_id", "junction", "tag_form", "tag_length"]].to_dict("records"):
        r["system_id"] = f"{r['construct_id']}_112_321"
        systems.append(r)
    model_map = best_model_map()
    rows = []
    for row in systems:
        sid = row["system_id"]
        sdir = OUT / "systems" / sid
        src = WT_PDB if sid == "WT_112_321" else Path(model_map[row["construct_id"]])
        start, end = residue_ranges_for_system(row)
        prep = sdir / "input_112_321.pdb"
        rec = extract_segment(src, prep, start, end)
        rows.append({
            "system_id": sid,
            "construct_id": row["construct_id"],
            "junction": row["junction"],
            "tag_form": row["tag_form"],
            "source_pdb": rec["source_pdb"],
            "prepared_pdb": rec["prepared_pdb"],
            "source_resid_start": rec["source_resid_start"],
            "source_resid_end": rec["source_resid_end"],
            "atom_count": rec["atom_count"],
            "residue_count": rec["residue_count"],
            "force_field": "charmm36",
            "water_model": "tip3p",
            "terminal_policy": "GROMACS pdb2gmx default charged termini, applied consistently",
            "box_policy": "dodecahedron, 1.0 nm minimum image distance",
            "ion_policy": "neutralize and add 0.15 M NaCl via genion",
        })
    pd.DataFrame(rows).to_csv(OUT / "system_build_inputs.tsv", sep="\t", index=False)


if __name__ == "__main__":
    main()
