#!/usr/bin/env python3
"""Quantitative four-structure junction screen for HRV-A89 2C.

Inputs:
  - AlphaFold model_1 and model_3 CIFs
  - lead/control hexamer PDBs

Outputs a 320-row TSV. This is a structural-risk screen, not a proof of
biological tolerance.
"""
from __future__ import annotations
import argparse
from pathlib import Path

import gemmi
import mdtraj as md
import numpy as np
import pandas as pd
from scipy.spatial import cKDTree

MAX_ASA = {
    "ALA":129,"ARG":274,"ASN":195,"ASP":193,"CYS":167,"GLN":225,"GLU":223,
    "GLY":104,"HIS":224,"ILE":197,"LEU":201,"LYS":236,"MET":224,"PHE":240,
    "PRO":159,"SER":155,"THR":172,"TRP":285,"TYR":263,"VAL":174,
}

def ca_bfactor(path: Path) -> dict[int,float]:
    st = gemmi.read_structure(str(path))
    out = {}
    for ch in st[0]:
        for r in ch:
            if not (1 <= r.seqid.num <= 321):
                continue
            a = r.find_atom("CA", "\0")
            if a:
                out[r.seqid.num] = float(a.b_iso)
    return out

def monomer_metrics(traj: md.Trajectory, plddt: dict[int,float]) -> pd.DataFrame:
    dssp = md.compute_dssp(traj, simplified=True)[0]
    sasa = md.shrake_rupley(traj, mode="residue")[0] * 100.0
    rows = []
    for i, r in enumerate(traj.topology.residues):
        rows.append({
            "resid": r.resSeq,
            "aa3": r.name,
            "ss": dssp[i],
            "rsasa": float(sasa[i] / MAX_ASA[r.name]),
            "ca_plddt": plddt[r.resSeq],
        })
    return pd.DataFrame(rows)

def hexamer_metrics(traj: md.Trajectory) -> pd.DataFrame:
    top = traj.topology
    xyz = traj.xyz[0]
    chains = list(top.chains)
    sasa_complex = md.shrake_rupley(traj, mode="residue")[0] * 100.0
    dssp = md.compute_dssp(traj, simplified=True)[0]

    centers = []
    chain_reslists = []
    for ch in chains:
        rs = list(ch.residues)
        chain_reslists.append(rs)
        ca = [a.index for r in rs if 112 <= r.resSeq <= 321
              for a in r.atoms if a.name == "CA"]
        centers.append(xyz[ca].mean(axis=0))
    centers = np.asarray(centers)
    center = centers.mean(axis=0)
    vals, vecs = np.linalg.eigh(np.cov((centers-center).T))
    axis = vecs[:, np.argmin(vals)]
    axis /= np.linalg.norm(axis)

    rows = []
    for ci, ch in enumerate(chains):
        rs = chain_reslists[ci]
        atom_idx = np.asarray([a.index for r in rs for a in r.atoms], dtype=int)
        isolated = traj.atom_slice(atom_idx)
        sasa_iso = md.shrake_rupley(isolated, mode="residue")[0] * 100.0

        other_heavy = np.asarray([
            a.index for ch2 in chains if ch2.index != ch.index
            for r in ch2.residues for a in r.atoms
            if a.element is not None and a.element.symbol != "H"
        ], dtype=int)
        tree = cKDTree(xyz[other_heavy])

        for ri, r in enumerate(rs):
            heavy = np.asarray([
                a.index for a in r.atoms
                if a.element is not None and a.element.symbol != "H"
            ], dtype=int)
            pts = xyz[heavy]
            d, _ = tree.query(pts, k=1)
            neigh = tree.query_ball_point(pts, r=0.45)

            rel = pts - center
            axial = rel @ axis
            radial = np.linalg.norm(rel - np.outer(axial, axis), axis=1) * 10.0

            comp = float(sasa_complex[r.index])
            iso = float(sasa_iso[ri])
            delta = max(0.0, iso-comp)
            burial = delta / iso if iso > 1e-8 else 0.0

            rows.append({
                "chain": chr(ord("A")+ci),
                "resid": r.resSeq,
                "ss": dssp[r.index],
                "rsasa_complex": comp / MAX_ASA[r.name],
                "burial_fraction": burial,
                "min_inter_heavy_A": float(d.min()*10.0),
                "contact_pairs_4p5A": int(sum(len(x) for x in neigh)),
                "min_heavy_radial_A": float(radial.min()),
            })
    return pd.DataFrame(rows)

def aggregate_hex(df: pd.DataFrame, prefix: str) -> pd.DataFrame:
    g = df.groupby("resid").agg(
        ss_coil_frac=("ss", lambda x: float(np.mean(np.asarray(x)=="C"))),
        rsasa_mean=("rsasa_complex","mean"),
        burial_max=("burial_fraction","max"),
        min_inter_heavy_A=("min_inter_heavy_A","min"),
        contacts_mean=("contact_pairs_4p5A","mean"),
        min_radial_mean_A=("min_heavy_radial_A","mean"),
    ).reset_index()
    return g.rename(columns={c:f"{prefix}_{c}" for c in g.columns if c!="resid"})

def classify(i: int) -> tuple[str,str]:
    ends = {i, i+1}
    hard_ranges = [
        (124,131,"Walker_A/ATP_binding"),
        (148,160,"9A5_epitope_and_H163-equivalent_pore-loop"),
        (165,170,"Walker_B"),
        (210,216,"Motif_C_region"),
        (316,321,"A89_C-terminal_oligomerization_region_by_similarity"),
    ]
    hard_single = {
        189:"EV_T196-equivalent_cross-protomer_nucleotide_site",
        197:"CVB3_A204-equivalent_core_RNA_binding",
        199:"CVB3_L206-equivalent_core_RNA_binding",
        202:"CVB3_K209-equivalent_core_RNA_binding",
        233:"R_finger_R233", 234:"R_finger_R234",
        262:"A89_Zn-binding_C262_by_similarity",
        273:"A89_Zn-binding_C273_by_similarity",
        278:"A89_Zn-binding_C278_by_similarity",
    }
    hard = {}
    for a,b,lab in hard_ranges:
        for x in range(a,b+1):
            hard.setdefault(x,[]).append(lab)
    for x,lab in hard_single.items():
        hard.setdefault(x,[]).append(lab)
    if ends & set(hard):
        reasons = sorted({lab for x in ends & set(hard) for lab in hard[x]})
        return "EXCLUDE", ";".join(reasons)

    reasons = []
    strong = [
        (1,70,"A89_N-terminal_membrane-binding_by_similarity"),
        (1,134,"A89_N-terminal_oligomerization_by_similarity"),
        (22,26,"A89_N-terminal_RNA-binding/RTN3_site_by_similarity"),
        (255,290,"ATPase-to-Zn/Cys-rich_transition"),
        (291,315,"C-terminal_bundle/RNA-binding_transition"),
        (305,312,"A89_C-terminal_RNA-binding_by_similarity"),
    ]
    for a,b,lab in strong:
        if any(a <= x <= b for x in ends):
            reasons.append(lab)
    proximity = [
        (124,131,8,"near_Walker_A"),
        (165,170,6,"near_Walker_B"),
        (189,189,4,"near_cross-protomer_nucleotide_site"),
        (197,202,4,"near_conserved_RNA-binding_triad"),
        (210,216,6,"near_Motif_C"),
        (233,234,6,"near_R_finger"),
        (262,278,4,"near_Zn-coordination_sites"),
        (316,321,6,"near_C-terminal_oligomerization_region"),
    ]
    for a,b,pad,lab in proximity:
        if any(a-pad <= x <= b+pad for x in ends):
            reasons.append(lab)
    if reasons:
        return "HIGH_RISK", ";".join(sorted(set(reasons)))
    if any(94 <= x <= 254 for x in ends):
        return "CORE_CAUTION", "A89_SF3_helicase_domain_by_PROSITE"
    return "UNRESOLVED", ""

def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--af1", required=True, type=Path)
    p.add_argument("--af3", required=True, type=Path)
    p.add_argument("--hex1", required=True, type=Path)
    p.add_argument("--hex2", required=True, type=Path)
    p.add_argument("--out", required=True, type=Path)
    a = p.parse_args()

    af = {}
    for name,path in [("af1",a.af1),("af3",a.af3)]:
        t = md.load(str(path))
        af[name] = monomer_metrics(t, ca_bfactor(path))

    hx = {}
    for name,path in [("hex1",a.hex1),("hex2",a.hex2)]:
        hx[name] = aggregate_hex(hexamer_metrics(md.load(str(path))), name)

    r = af["af1"].rename(columns={"ss":"af1_ss","rsasa":"af1_rsasa","ca_plddt":"af1_plddt"})
    r = r[["resid","af1_ss","af1_rsasa","af1_plddt"]]
    x = af["af3"].rename(columns={"ss":"af3_ss","rsasa":"af3_rsasa","ca_plddt":"af3_plddt"})
    r = r.merge(x[["resid","af3_ss","af3_rsasa","af3_plddt"]], on="resid")
    r = r.merge(hx["hex1"],on="resid").merge(hx["hex2"],on="resid")

    rows = []
    for i in range(1,321):
        q1 = r[r.resid==i].iloc[0]
        q2 = r[r.resid==i+1].iloc[0]
        tier, why = classify(i)
        both_af_coil = all(x=="C" for x in [q1.af1_ss,q2.af1_ss,q1.af3_ss,q2.af3_ss])
        min_hex_coil = min(q1.hex1_ss_coil_frac,q2.hex1_ss_coil_frac,q1.hex2_ss_coil_frac,q2.hex2_ss_coil_frac)
        min_af_rsa = min(q1.af1_rsasa,q2.af1_rsasa,q1.af3_rsasa,q2.af3_rsasa)
        min_hex_rsa = min(q1.hex1_rsasa_mean,q2.hex1_rsasa_mean,q1.hex2_rsasa_mean,q2.hex2_rsasa_mean)
        max_burial = max(q1.hex1_burial_max,q2.hex1_burial_max,q1.hex2_burial_max,q2.hex2_burial_max)
        min_inter = min(q1.hex1_min_inter_heavy_A,q2.hex1_min_inter_heavy_A,q1.hex2_min_inter_heavy_A,q2.hex2_min_inter_heavy_A)
        min_radial = min(q1.hex1_min_radial_mean_A,q2.hex1_min_radial_mean_A,q1.hex2_min_radial_mean_A,q2.hex2_min_radial_mean_A)
        strict = (both_af_coil and min_hex_coil>=0.8 and min_af_rsa>=0.25
                  and min_hex_rsa>=0.25 and max_burial<0.10 and min_inter>4.5)
        rows.append({
            "junction":f"{i}|{i+1}",
            "left_resid":i,"right_resid":i+1,
            "functional_tier":tier,"functional_reasons":why,
            "both_AF_coil":both_af_coil,
            "min_hex_coil_fraction":min_hex_coil,
            "min_AF_rSASA":min_af_rsa,
            "min_hexamer_mean_rSASA":min_hex_rsa,
            "max_any_chain_burial_fraction":max_burial,
            "min_interprotomer_heavy_atom_A":min_inter,
            "min_mean_pore_radial_A":min_radial,
            "min_AF_CA_pLDDT":min(q1.af1_plddt,q2.af1_plddt,q1.af3_plddt,q2.af3_plddt),
            "strict_structural_pass":strict,
        })
    a.out.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).to_csv(a.out, sep="\t", index=False)

if __name__ == "__main__":
    main()
