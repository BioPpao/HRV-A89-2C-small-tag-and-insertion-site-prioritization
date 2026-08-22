#!/usr/bin/env python3
"""OpenMM local minimization QC for OPEN_STRUCTURE_PIPELINE_007 models."""
from __future__ import annotations

import argparse
import tempfile
from pathlib import Path

import numpy as np
import pandas as pd
from openmm import LangevinIntegrator, Platform, unit
from openmm.app import ForceField, Modeller, NoCutoff, PDBFile, Simulation
from scipy.spatial import cKDTree


def openmm_ready_pdb(path: Path) -> Path:
    lines = path.read_text().splitlines()
    atoms = [line for line in lines if line.startswith("ATOM")]
    if not atoms:
        return path
    last = atoms[-1]
    chain = last[21]
    resid = int(last[22:26])
    resname = last[17:20]
    last_res = [line for line in atoms if line[21] == chain and int(line[22:26]) == resid]
    if any(line[12:16].strip() == "OXT" for line in last_res):
        return path
    coords = {}
    bfac = 0.0
    serial = 1
    for line in atoms:
        serial = max(serial, int(line[6:11]) + 1)
        if line[21] == chain and int(line[22:26]) == resid:
            name = line[12:16].strip()
            coords[name] = np.array([float(line[30:38]), float(line[38:46]), float(line[46:54])])
            bfac = float(line[60:66])
    if "C" not in coords or "O" not in coords:
        return path
    direction = coords["C"] - coords["O"]
    norm = np.linalg.norm(direction)
    if norm == 0:
        return path
    oxt = coords["C"] + direction / norm * 1.23
    oxt_line = (
        f"ATOM  {serial:5d}  OXT {resname:>3s} {chain}{resid:4d}    "
        f"{oxt[0]:8.3f}{oxt[1]:8.3f}{oxt[2]:8.3f}  1.00{bfac:6.2f}           O  "
    )
    out = []
    inserted = False
    for line in lines:
        if not inserted and line.startswith("TER"):
            out.append(oxt_line)
            inserted = True
        if not inserted and (line.startswith("ENDMDL") or line.startswith("END")):
            out.append(oxt_line)
            inserted = True
        out.append(line)
    if not inserted:
        out.append(oxt_line)
    tmp = tempfile.NamedTemporaryFile("w", suffix=".pdb", delete=False)
    tmp.write("\n".join(out) + "\n")
    tmp.close()
    return Path(tmp.name)


def heavy_atom_rows(pdb: PDBFile):
    rows = []
    pos = pdb.getPositions(asNumpy=True).value_in_unit(unit.angstrom)
    for atom in pdb.topology.atoms():
        if atom.element is not None and atom.element.symbol == "H":
            continue
        rows.append((atom.index, atom.residue.chain.id, int(atom.residue.id), atom.name, pos[atom.index]))
    return rows


def heavy_atom_rows_from_topology(topology, positions):
    rows = []
    pos = positions.value_in_unit(unit.angstrom)
    for atom in topology.atoms():
        if atom.element is not None and atom.element.symbol == "H":
            continue
        rows.append((atom.index, atom.residue.chain.id, int(atom.residue.id), atom.name, pos[atom.index]))
    return rows


def clash_count(rows, cutoff=2.0):
    if len(rows) < 2:
        return 0
    xyz = np.vstack([r[4] for r in rows])
    tree = cKDTree(xyz)
    count = 0
    for i, js in enumerate(tree.query_ball_point(xyz, cutoff)):
        _, ci, ri, ni, _ = rows[i]
        for j in js:
            if j <= i:
                continue
            _, cj, rj, nj, _ = rows[j]
            if ci == cj and abs(ri - rj) <= 1:
                continue
            count += 1
    return count


def ca_map(rows):
    return {(chain, resid): xyz for _idx, chain, resid, name, xyz in rows if name == "CA"}


def rmsd(a, b):
    return float(np.sqrt(np.mean(np.sum((a - b) ** 2, axis=1)))) if len(a) else ""


def ca_rmsd(pre_rows, post_rows, left=0, tag_len=0):
    pre = ca_map(pre_rows)
    post = ca_map(post_rows)
    common = sorted(set(pre) & set(post))
    native = [k for k in common if not (tag_len and left < k[1] <= left + tag_len)]
    local = [k for k in native if left and left - 3 <= k[1] <= left + tag_len + 4]
    out = {}
    for label, keys in [("native_ca_rmsd_pre_post_A", native), ("local_ca_rmsd_pre_post_A", local)]:
        if keys:
            out[label] = rmsd(np.vstack([pre[k] for k in keys]), np.vstack([post[k] for k in keys]))
        else:
            out[label] = ""
    return out


def minimize_one(model_file: Path, left: int, tag_len: int, max_iterations: int) -> dict:
    pre_pdb = PDBFile(str(model_file))
    pre_rows = heavy_atom_rows(pre_pdb)
    pre_clashes = clash_count(pre_rows)
    prepared = openmm_ready_pdb(model_file)
    pdb = PDBFile(str(prepared))
    ff = ForceField("amber14/protein.ff14SB.xml", "implicit/obc2.xml")
    modeller = Modeller(pdb.topology, pdb.positions)
    modeller.addHydrogens(ff, pH=7.0)
    system = ff.createSystem(modeller.topology, nonbondedMethod=NoCutoff, constraints=None)
    integrator = LangevinIntegrator(300 * unit.kelvin, 1.0 / unit.picosecond, 0.002 * unit.picoseconds)
    platform = Platform.getPlatformByName("CPU")
    sim = Simulation(modeller.topology, system, integrator, platform)
    sim.context.setPositions(modeller.positions)
    e0 = sim.context.getState(getEnergy=True).getPotentialEnergy().value_in_unit(unit.kilocalorie_per_mole)
    sim.minimizeEnergy(maxIterations=max_iterations)
    state = sim.context.getState(getPositions=True, getEnergy=True)
    e1 = state.getPotentialEnergy().value_in_unit(unit.kilocalorie_per_mole)
    post_rows = heavy_atom_rows_from_topology(modeller.topology, state.getPositions(asNumpy=True))
    post_clashes = clash_count(post_rows)
    return {
        "openmm_status": "completed_cpu_implicit_obc2_minimization",
        "pre_openmm_severe_clashes_2A": pre_clashes,
        "post_openmm_severe_clashes_2A": post_clashes,
        "openmm_energy_initial_kcal_mol": e0,
        "openmm_energy_minimized_kcal_mol": e1,
        "openmm_energy_delta_kcal_mol": e1 - e0,
        "openmm_max_iterations": max_iterations,
        **ca_rmsd(pre_rows, post_rows, left, tag_len),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", type=Path, default=Path("results/open_structure_007/prediction_manifest.tsv"))
    ap.add_argument("--out", type=Path, default=Path("data/tag_site_openmm_qc_v1.tsv"))
    ap.add_argument("--max-iterations", type=int, default=100)
    args = ap.parse_args()

    manifest = pd.read_csv(args.manifest, sep="\t")
    rows = []
    for _, r in manifest.iterrows():
        if r.get("prediction_status") != "completed":
            continue
        left = int(r["left_resid"]) if str(r.get("left_resid", "")).strip() not in {"", "nan"} else 0
        tag_len = int(r["tag_length"]) if str(r.get("tag_length", "")).strip() not in {"", "nan"} else 0
        base = {
            "construct_id": r["construct_id"],
            "junction": r.get("junction", ""),
            "tag_form": r.get("tag_form", ""),
            "model_file": r["model_file"],
        }
        try:
            rows.append({**base, **minimize_one(Path(r["model_file"]), left, tag_len, args.max_iterations)})
        except Exception as e:
            rows.append({
                **base,
                "openmm_status": f"failed:{type(e).__name__}:{e}",
                "pre_openmm_severe_clashes_2A": "",
                "post_openmm_severe_clashes_2A": "",
                "openmm_energy_initial_kcal_mol": "",
                "openmm_energy_minimized_kcal_mol": "",
                "openmm_energy_delta_kcal_mol": "",
                "openmm_max_iterations": args.max_iterations,
                "native_ca_rmsd_pre_post_A": "",
                "local_ca_rmsd_pre_post_A": "",
            })
        pd.DataFrame(rows).to_csv(args.out, sep="\t", index=False)
    pd.DataFrame(rows).to_csv(args.out, sep="\t", index=False)


if __name__ == "__main__":
    main()
