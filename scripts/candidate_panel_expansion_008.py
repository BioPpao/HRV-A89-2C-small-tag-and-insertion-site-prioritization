#!/usr/bin/env python3
"""Build CANDIDATE_PANEL_EXPANSION_008 CPU-side evidence tables.

This script is intentionally conservative: it reuses completed repository
evidence, records unavailable methods as status columns, and does not collapse
the candidate panel into a single scalar score.
"""
from __future__ import annotations

import csv
import math
from collections import Counter, defaultdict
from pathlib import Path

import pandas as pd

OUT = Path("results/candidate_panel_008")
LOGS = OUT / "logs"

CORE_TAGS = {
    "MAP8": "GDGMVPPG",
    "HA": "YPYDVPDYA",
    "G196_minimal": "DLVPR",
    "G196_practical_GS": "GSDLVPRGS",
}

EXPANSION_TAGS = {
    "ALFA": "SRLEEELRRRLTE",
    "PA12": "GVAMPGAEDDVV",
    "PA14": "EGGVAMPGAEDDVV",
    "AGIA": "EEAAGIARP",
    "HiBiT": "VSGWRLFKKIS",
}

RNA_CONTACT_A89 = {
    155: "FMDV_D146/CVB3_D162 preprint homolog; mutationally tolerant in CVB3 context",
    156: "FMDV_H147/CVB3_H163 pore-loop aromatic position; CVB3 mutant inhibited replication",
    197: "FMDV_A188/CVB3_A204 conserved RNA-binding triad",
    199: "FMDV_L190/CVB3_L206 conserved RNA-binding triad",
    202: "FMDV_K193/CVB3_K209 conserved RNA-binding triad",
    216: "CVB3_N223/A89_N216 motif-C/RNA-coupled neighborhood",
    233: "conserved Arg-finger homolog",
    234: "conserved Arg-finger homolog",
}

HARD_NEGATIVE_JUNCTIONS = ["155|156", "216|217"]
PROJECT_9A5_EPITOPE_A89_2C = set(range(148, 161))


def read_tsv(path: str | Path) -> pd.DataFrame:
    return pd.read_csv(path, sep="\t", dtype=str).fillna("")


def read_refseq() -> str:
    return "".join(
        line.strip()
        for line in Path("references/HRV_A89_2C_reference_sequence.fasta").read_text().splitlines()
        if not line.startswith(">")
    )


def fnum(value: object, default: float = math.nan) -> float:
    try:
        if value is None or str(value) == "":
            return default
        return float(value)
    except Exception:
        return default


def has_record(value: object) -> bool:
    return hasattr(value, "get") and len(value) > 0


def safe_min(vals: list[float]) -> float:
    vals = [v for v in vals if not math.isnan(v)]
    return min(vals) if vals else math.nan


def nearest_distance(pos: int, targets: set[int]) -> int:
    return min(abs(pos - t) for t in targets)


def junction_mid(left: int, right: int) -> float:
    return (left + right) / 2.0


def project_9a5_epitope_context(left: int, right: int) -> str:
    if any(left <= pos <= right for pos in PROJECT_9A5_EPITOPE_A89_2C):
        return "within_or_touches_project_defined_9A5_epitope_A89_2C_148_160"
    return "outside_project_defined_9A5_epitope_A89_2C_148_160"


def insert_tag(seq: str, left_resid: int, tag: str) -> str:
    return seq[:left_resid] + tag + seq[left_resid:]


def load_plm_long() -> pd.DataFrame:
    plm = read_tsv("data/tag_specific_plm_scores_v2_gpu.tsv")
    return plm.rename(columns={"a89_junction": "junction"})


def literature_records() -> pd.DataFrame:
    rows = [
        {
            "source_id": "Bakhache_2025_EV_A71_DIMPLE",
            "citation": "Bakhache W et al. Nature Microbiology 10:158-168 (2025)",
            "doi_pmcid_accession": "10.1038/s41564-024-01871-y; Dryad 10.5061/dryad.866t1g1xm; GitHub QVEU/eva71_dimple c99331a60980f68bb0141506e750e8339f278d08",
            "peer_review_status": "peer_reviewed",
            "directness_to_HRV_A89": "direct_homolog_EV_A71_not_A89",
            "evidence_type": "viral fitness substitution/insertion/deletion scan",
            "supports": "direct homolog 2C insertion phenotype is unfavorable at mapped A89 junctions",
            "does_not_support": "does not validate or absolutely reject any HRV-A89 tag construct",
            "affects": "direct phenotype prior; conflict labels",
        },
        {
            "source_id": "Teterina_2011_PV_nonstructural_insertions",
            "citation": "Teterina NL et al. Virology 409:1-11 (2011)",
            "doi_pmcid_accession": "10.1016/j.virol.2010.09.028; PMCID PMC2993843",
            "peer_review_status": "peer_reviewed",
            "directness_to_HRV_A89": "poliovirus homolog",
            "evidence_type": "nonstructural protein insertion screen",
            "supports": "2C is insertion-sensitive; tag identity and site context matter",
            "does_not_support": "does not prove every HRV-A89 internal 2C insertion fails",
            "affects": "hard caution prior; controls",
        },
        {
            "source_id": "DeepIndel_2025_NatCommun",
            "citation": "Deep indel mutagenesis reveals the impact of amino acid insertions and deletions on protein stability and function. Nature Communications (2025)",
            "doi_pmcid_accession": "10.1038/s41467-025-57510-5",
            "peer_review_status": "peer_reviewed",
            "directness_to_HRV_A89": "general protein-domain evidence",
            "evidence_type": "deep indel mutagenesis across domains",
            "supports": "loops and secondary-structure termini are modestly enriched for indel tolerance; rSASA alone is weak for insertion tolerance",
            "does_not_support": "does not provide viral 2C-specific tolerance",
            "affects": "secondary-structure prior",
        },
        {
            "source_id": "EpicTope",
            "citation": "EpicTope non-disruptive epitope-tagging framework",
            "doi_pmcid_accession": "PMCID PMC10979891; PMCID PMC13006528",
            "peer_review_status": "peer_reviewed/tool_article",
            "directness_to_HRV_A89": "general epitope-tag site-prediction framework",
            "evidence_type": "feature framework",
            "supports": "combine conservation, secondary structure, solvent exposure and disordered-binding features",
            "does_not_support": "does not replace direct viral fitness or structure-specific modeling",
            "affects": "feature selection",
        },
        {
            "source_id": "MAP8_Wakasa_2020",
            "citation": "Wakasa A et al. Journal of Biochemistry 168:375-384 (2020)",
            "doi_pmcid_accession": "10.1093/jb/mvaa054; PMCID PMC7585734",
            "peer_review_status": "peer_reviewed",
            "directness_to_HRV_A89": "tag-system evidence",
            "evidence_type": "internal epitope insertion and antibody recognition",
            "supports": "MAP8 is realistic for loop insertion and structural/binder evaluation",
            "does_not_support": "does not establish HRV-A89 2C tolerance",
            "affects": "tag choice; binder geometry",
        },
        {
            "source_id": "PA14_NZ1_2021",
            "citation": "Moving toward generalizable NZ-1 labeling for 3D structure determination with optimized epitope-tag insertion",
            "doi_pmcid_accession": "PMCID PMC8098476",
            "peer_review_status": "peer_reviewed",
            "directness_to_HRV_A89": "tag-system evidence",
            "evidence_type": "PA12/PA14 inserted epitope and NZ-1 Fab structural work",
            "supports": "PA14 can adopt closed loop-like bound geometry and may reduce insertion-induced structural change relative to PA12",
            "does_not_support": "does not prove PA14 works inside HRV-A89 2C",
            "affects": "tag portfolio; binder geometry",
        },
        {
            "source_id": "ALFA_Gotzke_2019",
            "citation": "Gotzke H et al. Nature Communications 10:4403 (2019)",
            "doi_pmcid_accession": "10.1038/s41467-019-12301-7; PMCID PMC6764986",
            "peer_review_status": "peer_reviewed",
            "directness_to_HRV_A89": "tag-system evidence",
            "evidence_type": "nanobody tag structural and assay system",
            "supports": "ALFA has strong nanobody reagent and defined helical epitope sequence",
            "does_not_support": "helical 13-aa tag may be risky in short constrained loops; no A89 2C evidence",
            "affects": "tag portfolio; detectability",
        },
        {
            "source_id": "AGIA_Yano_2016",
            "citation": "Yano T et al. PLOS ONE 11:e0156716 (2016)",
            "doi_pmcid_accession": "10.1371/journal.pone.0156716",
            "peer_review_status": "peer_reviewed",
            "directness_to_HRV_A89": "tag-system evidence",
            "evidence_type": "AGIA antibody tag",
            "supports": "AGIA is compact and has high-affinity antibody detection",
            "does_not_support": "limited internal-insertion structural evidence for A89 2C",
            "affects": "tag portfolio",
        },
        {
            "source_id": "G196_Tatsumi_2017",
            "citation": "Tatsumi K et al. Scientific Reports 7:43480 (2017)",
            "doi_pmcid_accession": "10.1038/srep43480; PMCID PMC5339894",
            "peer_review_status": "peer_reviewed",
            "directness_to_HRV_A89": "tag-system evidence",
            "evidence_type": "small monoclonal antibody epitope tag",
            "supports": "minimal DLVPR epitope and GS-flanked practical form are experimentally defined",
            "does_not_support": "does not establish internal A89 2C tolerance",
            "affects": "tag choice; linker comparison",
        },
        {
            "source_id": "HiBiT_Schwinn_2018",
            "citation": "Schwinn MK et al. ACS Chemical Biology 13:467-474 (2018)",
            "doi_pmcid_accession": "10.1021/acschembio.7b00549",
            "peer_review_status": "peer_reviewed",
            "directness_to_HRV_A89": "tag-system evidence",
            "evidence_type": "NanoLuc complementation peptide",
            "supports": "HiBiT is an 11-aa quantitative luminescent tag with LgBiT complementation",
            "does_not_support": "not an antibody epitope and may not fit IP/IF/complex-capture goals",
            "affects": "tag portfolio only if luminescence readout is desired",
        },
        {
            "source_id": "Pfuetzner_2026_2C_RNA_holoenzyme",
            "citation": "Pfuetzner RA et al. The Structure of the Picornaviral 2C:RNA holoenzyme (2026 preprint)",
            "doi_pmcid_accession": "10.64898/2026.06.07.730651",
            "peer_review_status": "preprint",
            "directness_to_HRV_A89": "homolog/preprint",
            "evidence_type": "RNA-bound 2C structural and mutational evidence",
            "supports": "RNA pore/contact residues should be mapped as mechanistic risk context",
            "does_not_support": "not a direct HRV-A89 structure or binary veto",
            "affects": "RNA holoenzyme context",
        },
        {
            "source_id": "Yeager_2022_RNA_ATPase",
            "citation": "Yeager C et al. Nucleic Acids Research (2022)",
            "doi_pmcid_accession": "10.1093/nar/gkac1054; PMCID PMC9723501",
            "peer_review_status": "peer_reviewed",
            "directness_to_HRV_A89": "enterovirus homolog biochemical evidence",
            "evidence_type": "RNA-stimulated ATPase mechanism",
            "supports": "2C RNA binding and ATPase coupling are central functional constraints",
            "does_not_support": "does not identify A89 insertion-tolerant sites",
            "affects": "RNA/ATPase context",
        },
    ]
    return pd.DataFrame(rows)


def build_feature_matrix() -> pd.DataFrame:
    v5 = read_tsv("data/candidate_junctions_v5_plm_gpu.tsv")
    cons = read_tsv("data/hrvA_conservation_per_junction_v2.tsv")
    indel = read_tsv("data/hrvA_independent_indel_events_v1.tsv").rename(columns={"a89_left_residue": "left_resid", "a89_right_residue": "right_resid"})
    direct = read_tsv("data/evA71_2C_direct_indel_to_A89_v1.tsv").rename(columns={"a89_junction": "junction"})
    plm = read_tsv("data/tag_specific_consensus_v2_gpu.tsv").rename(columns={"a89_junction": "junction"})
    struct = read_tsv("data/junction_structural_metrics_v2.tsv")

    keep_direct = [
        "junction", "mapping_class", "mapping_confidence", "mapping_note", "insertion_design",
        "insertion_length_aa", "insertion_raw_log2_enrich2", "insertion_direct_class",
        "deletion_context_best_raw_log2_enrich2", "deletion_context_class",
        "substitution_flank_mean_raw_log2_enrich2",
    ]
    df = v5.copy()
    df = df.merge(cons, on=["junction", "left_resid", "right_resid"], how="left", suffixes=("", "_cons"))
    df = df.merge(indel[["left_resid", "right_resid", "independent_indel_event_lower_bound", "independent_indel_event_uncertainty"]], on=["left_resid", "right_resid"], how="left")
    df = df.merge(direct[keep_direct], on="junction", how="left", suffixes=("", "_direct"))
    df = df.merge(plm, on="junction", how="left", suffixes=("", "_plm_consensus"))
    df = df.merge(struct, on=["junction", "left_resid", "right_resid"], how="left", suffixes=("", "_struct2"))

    rna_targets = set(RNA_CONTACT_A89)
    rows = []
    for _, r in df.iterrows():
        left = int(r["left_resid"])
        right = int(r["right_resid"])
        mid = junction_mid(left, right)
        nearest = min(rna_targets, key=lambda x: abs(mid - x))
        nearest_dist = min(abs(left - nearest), abs(right - nearest))
        both_coil = str(r.get("both_AF_coil", "")).lower() == "true"
        min_hex_coil = fnum(r.get("min_hex_coil_fraction"))
        min_rsasa = fnum(r.get("min_AF_rSASA"))
        min_hex_rsasa = fnum(r.get("min_hexamer_mean_rSASA"))
        min_inter = fnum(r.get("min_interprotomer_heavy_atom_A"))
        pore_radial = fnum(r.get("min_mean_pore_radial_A"))
        functional = r.get("functional_tier", "")
        if both_coil and (math.isnan(min_hex_coil) or min_hex_coil >= 0.5):
            ss_prior = "loop_or_coil_supported"
        elif both_coil:
            ss_prior = "monomer_loop_hexamer_mixed"
        else:
            ss_prior = "structured_or_uncertain"
        if not math.isnan(min_rsasa) and min_rsasa >= 0.35:
            exposure_prior = "surface_exposed"
        elif not math.isnan(min_rsasa) and min_rsasa >= 0.15:
            exposure_prior = "partly_exposed"
        else:
            exposure_prior = "buried_or_unknown"
        if nearest_dist <= 2:
            rna_class = "near_mapped_RNA_contact"
        elif nearest_dist <= 6:
            rna_class = "RNA_contact_neighborhood"
        elif not math.isnan(pore_radial) and pore_radial < 18:
            rna_class = "pore_proximal_model_context"
        else:
            rna_class = "no_close_mapped_RNA_contact"
        if functional == "EXCLUDE":
            hard = "hard_exclusion"
        elif functional in {"HIGH_RISK"}:
            hard = "high_risk_not_hard_exclusion"
        else:
            hard = "not_hard_excluded"
        rows.append({
            "junction": r["junction"],
            "left_resid": left,
            "right_resid": right,
            "left_aa": r.get("left_aa", r.get("a89_left_aa", "")),
            "right_aa": r.get("right_aa", r.get("a89_right_aa", "")),
            "functional_tier": functional,
            "functional_reasons": r.get("functional_reasons", ""),
            "hard_constraint_class": hard,
            "atpase_core_context": "inside_PROSITE_SF3_like_94_254" if 94 <= left <= 254 or 94 <= right <= 254 else "outside_PROSITE_SF3_like_94_254",
            "motif_proximity_class": motif_proximity(left, right, functional, r.get("functional_reasons", "")),
            "nineA5_epitope_context": project_9a5_epitope_context(left, right),
            "sequence_defined_9A5_epitope_context": project_9a5_epitope_context(left, right),
            "3D_9A5_complex_context": "not_assessed_in_candidate_panel_expansion_008__see_9a5_context_qc_011a",
            "wt_secondary_structure_prior": ss_prior,
            "both_AF_coil": r.get("both_AF_coil", ""),
            "min_hex_coil_fraction": r.get("min_hex_coil_fraction", ""),
            "distance_to_nearest_helix_boundary_status": "NA_no_residue_level_segment_file",
            "distance_to_nearest_strand_boundary_status": "NA_no_residue_level_segment_file",
            "min_AF_rSASA": r.get("min_AF_rSASA", ""),
            "min_hexamer_mean_rSASA": r.get("min_hexamer_mean_rSASA", ""),
            "solvent_exposure_prior": exposure_prior,
            "max_any_chain_burial_fraction": r.get("max_any_chain_burial_fraction", ""),
            "min_interprotomer_heavy_atom_A": r.get("min_interprotomer_heavy_atom_A", ""),
            "interface_proximity_class": "interface_close" if not math.isnan(min_inter) and min_inter < 5 else "not_close_or_unknown",
            "min_mean_pore_radial_A": r.get("min_mean_pore_radial_A", ""),
            "pore_context_class": "pore_proximal_proxy" if not math.isnan(pore_radial) and pore_radial < 18 else "not_pore_proximal_or_unknown",
            "min_AF_CA_pLDDT": r.get("min_AF_CA_pLDDT", ""),
            "strict_structural_pass": r.get("strict_structural_pass", ""),
            "local_disorder_status": "NA_iupred_anchor_not_available_in_current_environment",
            "disordered_binding_status": "NA_iupred_anchor_not_available_in_current_environment",
            "flexibility_proxy": flexibility_proxy(ss_prior, exposure_prior, min_hex_coil),
            "local_contact_density_proxy": contact_density_proxy(r),
            "monomer_hexamer_disagreement_proxy": disagreement_proxy(r),
            "hrvA_primary_window_mean_entropy": r.get("primary_window_mean_entropy", r.get("hrvA_primary_window_mean_entropy", "")),
            "hrvA_primary_window_mean_identity": r.get("primary_window_mean_identity", r.get("hrvA_primary_window_mean_identity", "")),
            "hrvA_expanded_natural_insertion_count": r.get("expanded_natural_insertion_count", r.get("hrvA_expanded_natural_insertion_count", "")),
            "independent_indel_event_lower_bound": r.get("independent_indel_event_lower_bound", ""),
            "independent_indel_event_uncertainty": r.get("independent_indel_event_uncertainty", ""),
            "evA71_mapping_class": r.get("mapping_class", ""),
            "evA71_mapping_confidence": r.get("mapping_confidence", ""),
            "evA71_insertion_raw_log2_enrich2": r.get("insertion_raw_log2_enrich2", ""),
            "evA71_insertion_direct_class": r.get("insertion_direct_class", ""),
            "evA71_substitution_flank_mean_raw_log2_enrich2": r.get("substitution_flank_mean_raw_log2_enrich2", ""),
            "plm_percentile_mean": r.get("plm_percentile_mean", ""),
            "plm_percentile_min": r.get("plm_percentile_min", ""),
            "plm_percentile_range": r.get("plm_percentile_range", ""),
            "best_tag_form": r.get("best_tag_form", ""),
            "worst_tag_form": r.get("worst_tag_form", ""),
            "plm_consensus_class": r.get("plm_consensus_class", ""),
            "pareto_reviewable_subset_count": r.get("pareto_reviewable_subset_count", ""),
            "candidate_class_v5_plm_gpu": r.get("candidate_class_v5_plm_gpu", ""),
            "rna_holoenzyme_nearest_mapped_residue": nearest,
            "rna_holoenzyme_nearest_distance_residues": nearest_dist,
            "rna_holoenzyme_context_class": rna_class,
            "feature_completion_status": "completed_with_explicit_NA_for_unavailable_disorder_and_boundary_segments",
        })
    out = pd.DataFrame(rows)
    if len(out) != 320:
        raise SystemExit(f"feature matrix expected 320 rows, got {len(out)}")
    return out


def motif_proximity(left: int, right: int, functional: str, reasons: str) -> str:
    if functional == "EXCLUDE":
        return "hard_functional_motif_or_domain"
    if any(k in reasons.lower() for k in ["walker", "motif", "arg-finger", "rna", "zinc", "cys"]):
        return "annotated_functional_neighborhood"
    if 94 <= left <= 254 or 94 <= right <= 254:
        return "atpase_core_region"
    return "no_specific_motif_annotation"


def flexibility_proxy(ss_prior: str, exposure_prior: str, min_hex_coil: float) -> str:
    if ss_prior == "loop_or_coil_supported" and exposure_prior == "surface_exposed":
        return "higher_relative_flexibility_prior"
    if ss_prior.startswith("monomer_loop"):
        return "mixed_flexibility_prior"
    if not math.isnan(min_hex_coil) and min_hex_coil == 0:
        return "lower_flexibility_prior"
    return "unknown_or_moderate_flexibility_prior"


def contact_density_proxy(r: pd.Series) -> str:
    burial = fnum(r.get("max_any_chain_burial_fraction"))
    inter = fnum(r.get("min_interprotomer_heavy_atom_A"))
    if not math.isnan(burial) and burial >= 0.5:
        return "high_burial_contact_density_proxy"
    if not math.isnan(inter) and inter < 5:
        return "interface_contact_density_proxy"
    return "not_high_by_available_proxy"


def disagreement_proxy(r: pd.Series) -> str:
    both_coil = str(r.get("both_AF_coil", "")).lower() == "true"
    min_hex = fnum(r.get("min_hex_coil_fraction"))
    if both_coil and not math.isnan(min_hex) and min_hex < 0.5:
        return "monomer_loop_hexamer_not_consistently_loop"
    return "no_major_available_disagreement"


def build_rna_mapping(features: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for _, r in features.iterrows():
        left = int(r["left_resid"])
        right = int(r["right_resid"])
        nearest = int(r["rna_holoenzyme_nearest_mapped_residue"])
        rows.append({
            "junction": r["junction"],
            "left_resid": left,
            "right_resid": right,
            "nearest_A89_mapped_RNA_or_RNA_coupled_residue": nearest,
            "nearest_residue_evidence_note": RNA_CONTACT_A89[nearest],
            "nearest_distance_residues": r["rna_holoenzyme_nearest_distance_residues"],
            "rna_holoenzyme_context_class": r["rna_holoenzyme_context_class"],
            "pore_facing_orientation_status": "proxy_from_existing_A89_hexamer_radial_metric;no_preprint_coordinates_committed",
            "local_RNA_path_distance_A": "NA_preprint_coordinates_not_available_in_repository",
            "ATPase_RNA_coupling_neighborhood": "yes" if int(r["rna_holoenzyme_nearest_distance_residues"]) <= 6 else "no_close_mapped_neighborhood",
            "homolog_mapping_confidence": "medium_from_existing_CVB3_to_A89_explicit_mapping",
            "evidence_boundary": "homolog_preprint_supporting_context_not_binary_veto",
        })
    return pd.DataFrame(rows)


def tag_portfolio() -> pd.DataFrame:
    rows = [
        tag_row("MAP8", CORE_TAGS["MAP8"], "mouse monoclonal PMab-1/MAP binder", "antibody epitope", "Wakasa_2020", "direct internal-insertion structural literature", "loop-compatible peptide with demonstrated internal insertion", "core_proceed"),
        tag_row("HA", CORE_TAGS["HA"], "anti-HA antibodies", "antibody epitope", "conventional", "broad practical use; limited insertion-specific 2C evidence", "benchmark immunodetection tag", "core_proceed"),
        tag_row("G196_minimal", CORE_TAGS["G196_minimal"], "G196 monoclonal antibody", "antibody epitope", "Tatsumi_2017", "minimal DLVPR epitope defined", "shortest core antibody tag; accessibility may need context", "core_proceed"),
        tag_row("G196_practical_GS", CORE_TAGS["G196_practical_GS"], "G196 monoclonal antibody", "antibody epitope", "Tatsumi_2017", "GS-flanked practical architecture", "larger than minimal; OPEN_STRUCTURE_007 mean clash worse than minimal", "architecture_comparison_only"),
        tag_row("ALFA", EXPANSION_TAGS["ALFA"], "NbALFA nanobody", "nanobody epitope", "Gotzke_2019", "high-affinity nanobody and crystal structure", "helical 13-aa tag; structural footprint may be risky in short loops", "review_but_do_not_broadly_model_until_assay_chosen"),
        tag_row("PA12", EXPANSION_TAGS["PA12"], "NZ-1 antibody/Fab", "antibody epitope", "Fujii_2014_Tamura_2019", "PA tag/NZ-1 structural literature", "PA12 insertion can distort target locally; PA14 may be better", "secondary_review"),
        tag_row("PA14", EXPANSION_TAGS["PA14"], "NZ-1 antibody/Fab", "antibody epitope", "PA14_NZ1_2021", "inserted PA14 closed loop-like bound geometry", "14 aa footprint; promising insertion-specific binder geometry", "secondary_review"),
        tag_row("AGIA", EXPANSION_TAGS["AGIA"], "Ra48 anti-AGIA rabbit monoclonal antibody", "antibody epitope", "Yano_2016", "compact high-affinity antibody tag", "limited internal-insertion structural evidence", "secondary_review"),
        tag_row("HiBiT", EXPANSION_TAGS["HiBiT"], "LgBiT complementation", "luminescence complementation", "Schwinn_2018", "quantitative sensitive 11-aa luminescent readout", "not antibody tag; may not serve IP/IF; binder is 18 kDa LgBiT", "conditional_if_luminescence_readout_desired"),
    ]
    return pd.DataFrame(rows)


def tag_row(name, seq, binder, system, source, evidence, strengths, proceed):
    return {
        "tag_form": name,
        "tag_sequence": seq,
        "tag_length": len(seq),
        "recognition_reagent": binder,
        "detection_system": system,
        "key_source_id": source,
        "internal_insertion_evidence": evidence,
        "advantages": strengths,
        "weaknesses": tag_weakness(name),
        "reagent_feasibility": "realistic_literature_supported" if name != "HiBiT" else "realistic_if_luminescence_workflow_desired",
        "bound_conformation": tag_conformation(name),
        "should_enter_computational_expansion_now": "yes_core" if name in {"MAP8", "HA", "G196_minimal"} else proceed,
    }


def tag_weakness(name: str) -> str:
    return {
        "MAP8": "8 aa tag; binder geometry still requires exposure in A89 2C",
        "HA": "conventional but no A89 2C-specific internal tolerance evidence",
        "G196_minimal": "minimal epitope may require favorable exposure; possible endogenous motif background",
        "G196_practical_GS": "larger GS-flanked form had worse OPEN_STRUCTURE_007 mean clash behavior",
        "ALFA": "helical 13 aa sequence may impose secondary-structure preference",
        "PA12": "PA12 insertion may separate insertion ends and distort target loops",
        "PA14": "14 aa footprint is larger than current core tags",
        "AGIA": "limited bound/insertion-geometry evidence for constrained internal loops",
        "HiBiT": "requires LgBiT complementation and luminescence readout; not antibody IP/IF by itself",
    }[name]


def tag_conformation(name: str) -> str:
    return {
        "MAP8": "binder-compatible loop/turn epitope from MAP system literature",
        "HA": "linear peptide epitope; bound/internal geometry not explicitly modeled here",
        "G196_minimal": "short linear DLVPR epitope",
        "G196_practical_GS": "GS-flanked DLVPR architecture",
        "ALFA": "defined alpha-helical nanobody-bound epitope",
        "PA12": "bent PA/NZ-1 epitope; insertion can perturb loop",
        "PA14": "closed loop-like NZ-1-bound insertion geometry",
        "AGIA": "linear antibody epitope; bound geometry not modeled here",
        "HiBiT": "complementation peptide; binder geometry not antibody-like",
    }[name]


def select_expanded_panel(features: pd.DataFrame, open_struct: pd.DataFrame) -> pd.DataFrame:
    chosen = [
        ("289|290", "MAP8", "deep_leader_current"),
        ("289|290", "G196_minimal", "deep_leader_current"),
        ("289|290", "HA", "single_model_structure_strong_third_tag"),
        ("288|289", "MAP8", "neighbor_alternative_low_clash"),
        ("288|289", "G196_minimal", "neighbor_alternative_low_clash"),
        ("288|289", "HA", "neighbor_third_tag_comparison"),
        ("290|291", "MAP8", "deep_neighbor_weaker_RMSD_low_clash"),
        ("290|291", "G196_minimal", "deep_neighbor_weaker_RMSD_low_clash"),
        ("287|288", "MAP8", "upstream_neighbor_alternative"),
        ("287|288", "G196_minimal", "upstream_neighbor_G196"),
        ("224|225", "HA", "non_C_terminal_core_caution_low_clash"),
        ("224|225", "MAP8", "non_C_terminal_core_caution_MAP8"),
        ("224|225", "G196_minimal", "non_C_terminal_G196"),
        ("248|249", "MAP8", "historical_conflict_MAP8"),
        ("248|249", "HA", "historical_conflict_HA"),
        ("203|204", "G196_minimal", "high_risk_mixed_structure_control"),
        ("256|257", "MAP8", "oligomer_clash_disfavored_control"),
        ("155|156", "MAP8", "hard_negative_control"),
    ]
    seq = read_refseq()
    by_feature = features.set_index("junction", drop=False)
    plm = load_plm_long()
    plm_key = {(r["junction"], r["tag_form"]): r for _, r in plm.iterrows()}
    rows = []
    for rank, (j, tag, rationale) in enumerate(chosen, start=1):
        f = by_feature.loc[j]
        left = int(f["left_resid"])
        tag_seq = CORE_TAGS[tag]
        construct_id = f"A89_2C_{j.replace('|','_')}_{tag}"
        plmr = plm_key.get((j, tag), {})
        osr = open_struct[(open_struct["junction"] == j) & (open_struct["tag_form"] == tag)]
        rows.append({
            "construct_id": construct_id,
            "junction": j,
            "left_resid": left,
            "right_resid": int(f["right_resid"]),
            "tag_form": tag,
            "tag_sequence": tag_seq,
            "tag_length": len(tag_seq),
            "full_sequence": insert_tag(seq, left, tag_seq),
            "selection_rank_pre_prediction": rank,
            "selection_rationale_pre_prediction": rationale,
            "functional_tier": f["functional_tier"],
            "hard_constraint_class": f["hard_constraint_class"],
            "evA71_insertion_direct_class": f["evA71_insertion_direct_class"],
            "plm_percentile_within_tag": plmr.get("plm_percentile_within_tag", ""),
            "prior_open_structure_available": "yes" if not osr.empty else "no",
            "replication_plan": "two_additional_seeds_if_GPU_available;reuse_cached_A3M_when_present",
        })
    return pd.DataFrame(rows)


def protease_risk(panel: pd.DataFrame) -> pd.DataFrame:
    seq = read_refseq()
    rows = []
    for _, r in panel.iterrows():
        left = int(r["left_resid"])
        tag = r["tag_sequence"]
        native_left = seq[max(0, left - 6):left]
        native_right = seq[left:left + 6]
        inserted = native_left + tag + native_right
        motifs = cleavage_like_windows(inserted)
        if motifs:
            risk = "plausible_cleavage_like_motif_requiring_caution"
        elif tag_boundary_pair(native_left[-1:] + tag[:1]) or tag_boundary_pair(tag[-1:] + native_right[:1]):
            risk = "weak_cleavage_like_boundary_motif"
        else:
            risk = "no_obvious_motif_concern"
        rows.append({
            "construct_id": r["construct_id"],
            "junction": r["junction"],
            "tag_form": r["tag_form"],
            "native_left_window_6aa": native_left,
            "tag_sequence": tag,
            "native_right_window_6aa": native_right,
            "boundary_context_native_left_tag_native_right": inserted,
            "protease_motif_logic": "flags Q/E before G/S/A at or near tag boundaries as weak picornavirus-3C-like motif; not proof of cleavage",
            "motif_hits": ";".join(motifs),
            "protease_boundary_risk_class": risk,
            "interpretation_boundary": "motif-only risk annotation, not experimentally demonstrated cleavage",
        })
    return pd.DataFrame(rows)


def tag_boundary_pair(pair: str) -> bool:
    return len(pair) == 2 and pair[0] in {"Q", "E"} and pair[1] in {"G", "S", "A", "N"}


def cleavage_like_windows(seq: str) -> list[str]:
    hits = []
    for i in range(len(seq) - 1):
        pair = seq[i:i + 2]
        if tag_boundary_pair(pair):
            hits.append(f"{i+1}:{pair}")
    return hits


def binder_accessibility(panel: pd.DataFrame, open_struct: pd.DataFrame, portfolio: pd.DataFrame) -> pd.DataFrame:
    port = portfolio.set_index("tag_form", drop=False)
    rows = []
    for _, r in panel.iterrows():
        osr = open_struct[(open_struct["junction"] == r["junction"]) & (open_struct["tag_form"] == r["tag_form"])]
        tag = r["tag_form"]
        p = port.loc[tag]
        if osr.empty:
            status = "not_structurally_modeled_for_binder_accessibility"
            tag_plddt = tag_sasa = min_neighbor = hex_clash = ""
        else:
            row = osr.iloc[0]
            status = "geometry_proxy_completed_no_binder_docking"
            tag_plddt = row.get("tag_mean_plddt_mean", "")
            tag_sasa = ""
            min_neighbor = row.get("min_tag_neighbor_A", "")
            hex_clash = row.get("max_tag_neighbor_clashes_2p5A", "")
        rows.append({
            "construct_id": r["construct_id"],
            "junction": r["junction"],
            "tag_form": tag,
            "recognition_reagent": p["recognition_reagent"],
            "bound_conformation_reference": p["bound_conformation"],
            "accessibility_analysis_status": status,
            "tag_mean_plddt_proxy": tag_plddt,
            "tag_mean_sasa_A2": tag_sasa,
            "min_tag_neighbor_A_proxy": min_neighbor,
            "hexamer_tag_neighbor_clashes_2p5A_proxy": hex_clash,
            "binder_steric_compatibility_class": binder_class(tag, osr),
            "linker_need_annotation": linker_need(tag),
            "limitation": "no mature binder docking performed; solvent/hexamer proxies do not prove detectability",
        })
    return pd.DataFrame(rows)


def binder_class(tag: str, osr: pd.DataFrame) -> str:
    if osr.empty:
        return "unknown_no_inserted_model"
    clashes = fnum(osr.iloc[0].get("max_tag_neighbor_clashes_2p5A"))
    min_neighbor = fnum(osr.iloc[0].get("min_tag_neighbor_A"))
    if not math.isnan(clashes) and clashes > 10:
        return "hexamer_obstruction_likely"
    if tag == "G196_minimal":
        return "short_epitope_accessibility_requires_empirical_check"
    if tag == "MAP8" and (math.isnan(min_neighbor) or min_neighbor > 2.5):
        return "plausible_by_geometry_proxy"
    if tag == "HA" and (math.isnan(clashes) or clashes <= 1):
        return "plausible_by_geometry_proxy"
    return "mixed_or_uncertain"


def linker_need(tag: str) -> str:
    if tag == "G196_minimal":
        return "minimal_epitope_may_need_linker_but_linker_adds_perturbation"
    if tag == "G196_practical_GS":
        return "GS_linkers_present"
    if tag in {"PA14", "ALFA"}:
        return "do_not_add_linker_without_tag_specific_modeling"
    return "no_linker_added_in_current_design"


def expanded_metrics(panel: pd.DataFrame, open_struct: pd.DataFrame, robustness: pd.DataFrame) -> pd.DataFrame:
    rows = []
    rob = robustness.set_index(["junction", "tag_form"], drop=False)
    for _, r in panel.iterrows():
        osr = open_struct[(open_struct["junction"] == r["junction"]) & (open_struct["tag_form"] == r["tag_form"])]
        if osr.empty:
            rows.append({**r.to_dict(), "structure_replication_status": "pending_not_in_OPEN_STRUCTURE_007", "model_count_available": 0})
            continue
        o = osr.iloc[0].to_dict()
        key = (r["junction"], r["tag_form"])
        rr = rob.loc[key].to_dict() if key in rob.index else {}
        rows.append({
            **{k: r[k] for k in ["construct_id", "junction", "tag_form", "selection_rank_pre_prediction", "selection_rationale_pre_prediction"]},
            "structure_replication_status": "reused_OPEN_STRUCTURE_007_metrics_pending_extra_008_GPU_replicates",
            "model_count_available": o.get("model_count", ""),
            "native_domain_rmsd_mean_A": o.get("native_2c_ca_rmsd_mean_A", ""),
            "local_window_rmsd_mean_A": o.get("local_window_ca_rmsd_mean_A", ""),
            "native_plddt_mean": o.get("native_2c_mean_plddt_mean", ""),
            "tag_plddt_mean": o.get("tag_mean_plddt_mean", ""),
            "severe_clashes_2A_pre_openmm_max": o.get("severe_clashes_2A_max", ""),
            "openmm_status": o.get("openmm_status", ""),
            "openmm_post_clashes_2A_max": o.get("openmm_post_clashes_2A_max", ""),
            "tag_exposure_proxy_min_neighbor_A": o.get("min_tag_neighbor_A", ""),
            "hexamer_tag_neighbor_clashes_2p5A_max": o.get("max_tag_neighbor_clashes_2p5A", ""),
            "native_contact_loss_mean": o.get("native_contact_loss_mean", ""),
            "local_contact_loss_mean": o.get("local_contact_loss_mean", ""),
            "seed_robustness_status": rr.get("robustness_status", "single_model_or_not_available"),
            "interpretation": o.get("open_structure_interpretation", ""),
        })
    return pd.DataFrame(rows)


def local_multimer_context(panel: pd.DataFrame, metrics: pd.DataFrame) -> pd.DataFrame:
    rows = []
    informative = panel[panel["junction"].isin(["224|225", "248|249", "256|257", "288|289", "289|290", "290|291"])].head(10)
    for _, r in informative.iterrows():
        m = metrics[metrics["construct_id"] == r["construct_id"]]
        rigid = m.iloc[0].get("hexamer_tag_neighbor_clashes_2p5A_max", "") if not m.empty else ""
        rows.append({
            "construct_id": r["construct_id"],
            "junction": r["junction"],
            "tag_form": r["tag_form"],
            "rigid_hexamer_clash_proxy": rigid,
            "local_multimer_modeling_status": "deferred_not_run_in_CPU_checkpoint",
            "reason": "open multimer ColabFold dimer/trimer setup requires separate GPU job and careful sequence/protomer design; not allowed to block independent ranking outputs",
            "interpretation": "rigid hexamer context retained until local multimer modeling is explicitly completed",
        })
    return pd.DataFrame(rows)


def preliminary_ranking(panel: pd.DataFrame, features: pd.DataFrame, metrics: pd.DataFrame, binder: pd.DataFrame, protease: pd.DataFrame) -> pd.DataFrame:
    f = features.set_index("junction", drop=False)
    m = metrics.set_index("construct_id", drop=False)
    b = binder.set_index("construct_id", drop=False)
    p = protease.set_index("construct_id", drop=False)
    rows = []
    for _, r in panel.iterrows():
        fr = f.loc[r["junction"]]
        mr = m.loc[r["construct_id"]] if r["construct_id"] in m.index else {}
        br = b.loc[r["construct_id"]] if r["construct_id"] in b.index else {}
        pr = p.loc[r["construct_id"]] if r["construct_id"] in p.index else {}
        support, caution = evidence_labels(fr, mr, br, pr)
        rows.append({
            "construct_id": r["construct_id"],
            "junction": r["junction"],
            "tag_form": r["tag_form"],
            "hard_constraint_class": fr["hard_constraint_class"],
            "functional_tier": fr["functional_tier"],
            "direct_homolog_insertion_class": fr["evA71_insertion_direct_class"],
            "substitution_context": fr["evA71_substitution_flank_mean_raw_log2_enrich2"],
            "conservation_identity": fr["hrvA_primary_window_mean_identity"],
            "independent_indel_event_lower_bound": fr["independent_indel_event_lower_bound"],
            "secondary_structure_prior": fr["wt_secondary_structure_prior"],
            "solvent_exposure_prior": fr["solvent_exposure_prior"],
            "rna_holoenzyme_context_class": fr["rna_holoenzyme_context_class"],
            "protease_boundary_risk_class": pr.get("protease_boundary_risk_class", ""),
            "plm_percentile_within_tag": r.get("plm_percentile_within_tag", ""),
            "inserted_structure_status": mr.get("structure_replication_status", ""),
            "native_domain_rmsd_mean_A": mr.get("native_domain_rmsd_mean_A", ""),
            "hexamer_clash_proxy": mr.get("hexamer_tag_neighbor_clashes_2p5A_max", ""),
            "binder_accessibility_class": br.get("binder_steric_compatibility_class", ""),
            "oligomer_context_class": oligomer_context(mr),
            "model_seed_robustness": mr.get("seed_robustness_status", ""),
            "supporting_evidence_labels": ";".join(support),
            "negative_evidence_labels": ";".join(caution),
            "conflict_class": conflict_class(fr, mr, br),
            "pareto_non_dominated_within_panel": "",
            "tier_suggestion_pre_panel": tier_suggestion(fr, mr, br, pr),
        })
    out = pd.DataFrame(rows)
    out["pareto_non_dominated_within_panel"] = pareto_flags(out)
    return out


def evidence_labels(fr, mr, br, pr) -> tuple[list[str], list[str]]:
    support, caution = [], []
    if fr["hard_constraint_class"] != "hard_exclusion":
        support.append("not_hard_excluded")
    else:
        caution.append("hard_exclusion")
    if fr["wt_secondary_structure_prior"] in {"loop_or_coil_supported", "monomer_loop_hexamer_mixed"}:
        support.append(fr["wt_secondary_structure_prior"])
    if fr["solvent_exposure_prior"] == "surface_exposed":
        support.append("surface_exposed")
    if str(fr.get("independent_indel_event_lower_bound", "")) not in {"", "0", "0.0"}:
        support.append("natural_indel_event_support")
    if fnum(fr.get("plm_percentile_mean")) >= 0.6:
        support.append("PLM_above_panel_mean")
    if has_record(mr) and fnum(mr.get("native_domain_rmsd_mean_A")) < 1.6:
        support.append("low_inserted_structure_RMSD")
    if has_record(mr) and fnum(mr.get("hexamer_tag_neighbor_clashes_2p5A_max")) == 0:
        support.append("no_rigid_hexamer_tag_clash")
    if has_record(br) and br.get("binder_steric_compatibility_class") in {"plausible_by_geometry_proxy", "short_epitope_accessibility_requires_empirical_check"}:
        support.append("detectability_plausible_or_testable")
    if "strongly_deleterious" in str(fr.get("evA71_insertion_direct_class", "")):
        caution.append("direct_homolog_insertion_unfavorable")
    if fr["functional_tier"] == "HIGH_RISK":
        caution.append("functional_high_risk")
    if fr["rna_holoenzyme_context_class"] in {"near_mapped_RNA_contact", "RNA_contact_neighborhood"}:
        caution.append("RNA_holoenzyme_neighborhood")
    if has_record(mr) and fnum(mr.get("hexamer_tag_neighbor_clashes_2p5A_max")) > 10:
        caution.append("rigid_hexamer_clash")
    if has_record(pr) and pr.get("protease_boundary_risk_class") != "no_obvious_motif_concern":
        caution.append("protease_motif_caution")
    return support, caution


def oligomer_context(mr) -> str:
    if not has_record(mr):
        return "not_structurally_modeled"
    clash = fnum(mr.get("hexamer_tag_neighbor_clashes_2p5A_max"))
    if math.isnan(clash):
        return "unknown"
    if clash == 0:
        return "low_clash_rigid_hexamer_proxy"
    if clash <= 5:
        return "moderate_clash_rigid_hexamer_proxy"
    return "high_clash_rigid_hexamer_proxy"


def conflict_class(fr, mr, br) -> str:
    labels = []
    if "strongly_deleterious" in str(fr.get("evA71_insertion_direct_class", "")):
        labels.append("direct_homolog_conflict")
    if fr["functional_tier"] in {"HIGH_RISK", "CORE_CAUTION"}:
        labels.append(f"functional_{fr['functional_tier']}")
    if has_record(mr) and fnum(mr.get("native_domain_rmsd_mean_A")) < 1.6:
        labels.append("structure_supported")
    if has_record(br) and br.get("binder_steric_compatibility_class", "").startswith("plausible"):
        labels.append("detectability_supported")
    return "__".join(labels) if labels else "method_inconclusive"


def tier_suggestion(fr, mr, br, pr) -> str:
    if fr["hard_constraint_class"] == "hard_exclusion":
        return "control_hard_negative"
    clash = fnum(mr.get("hexamer_tag_neighbor_clashes_2p5A_max")) if has_record(mr) else math.nan
    rmsd = fnum(mr.get("native_domain_rmsd_mean_A")) if has_record(mr) else math.nan
    if not math.isnan(clash) and clash > 10:
        return "control_or_tierB_oligomer_disfavored"
    if fr["functional_tier"] == "CORE_CAUTION" and not math.isnan(clash) and clash <= 1:
        return "tierA_or_tierB_conflict_candidate"
    if not math.isnan(rmsd) and rmsd < 1.7 and (math.isnan(clash) or clash <= 1):
        return "tierA_primary_candidate_with_direct_conflict"
    return "tierB_secondary_or_rescue"


def pareto_flags(df: pd.DataFrame) -> list[str]:
    vals = []
    for _, r in df.iterrows():
        vals.append([
            -risk_rank(r["hard_constraint_class"]),
            fnum(r["plm_percentile_within_tag"], 0),
            -fnum(r["native_domain_rmsd_mean_A"], 9),
            -fnum(r["hexamer_clash_proxy"], 99),
            -rna_risk_rank(r["rna_holoenzyme_context_class"]),
        ])
    flags = []
    for i, vi in enumerate(vals):
        dominated = False
        for j, vj in enumerate(vals):
            if i == j:
                continue
            if all(a >= b for a, b in zip(vj, vi)) and any(a > b for a, b in zip(vj, vi)):
                dominated = True
                break
        flags.append("yes" if not dominated else "no")
    return flags


def risk_rank(x: str) -> int:
    return {"hard_exclusion": 3, "high_risk_not_hard_exclusion": 2, "not_hard_excluded": 1}.get(x, 2)


def rna_risk_rank(x: str) -> int:
    return {"near_mapped_RNA_contact": 3, "RNA_contact_neighborhood": 2, "pore_proximal_model_context": 1}.get(x, 0)


def ranking_robustness(prelim: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for _, r in prelim.iterrows():
        support = set(filter(None, r["supporting_evidence_labels"].split(";")))
        caution = set(filter(None, r["negative_evidence_labels"].split(";")))
        rows.append({
            "construct_id": r["construct_id"],
            "junction": r["junction"],
            "tag_form": r["tag_form"],
            "pareto_non_dominated_within_panel": r["pareto_non_dominated_within_panel"],
            "support_layer_count": len(support),
            "caution_layer_count": len(caution),
            "leave_out_direct_phenotype_effect": "would_improve_rank_but_conflict_must_remain_visible" if "direct_homolog_insertion_unfavorable" in caution else "little_effect",
            "leave_out_PLM_effect": "fragile_if_only_PLM_support" if support == {"PLM_above_panel_mean"} else "not_single_PLM_dependent",
            "leave_out_structure_effect": "fragile_if_structure_only" if "low_inserted_structure_RMSD" in support and len(support) <= 2 else "not_structure_only",
            "C_terminal_bias_check": "C_terminal_cluster" if int(str(r["junction"]).split("|")[0]) >= 280 else "non_C_terminal_or_control",
            "tag_family_bias_check": r["tag_form"],
            "robustness_class": robustness_class(support, caution, r),
        })
    return pd.DataFrame(rows)


def robustness_class(support: set[str], caution: set[str], r: pd.Series) -> str:
    if r["hard_constraint_class"] == "hard_exclusion":
        return "hard_negative_control"
    if len(support) >= 4 and len(caution) <= 2:
        return "broad_consensus_with_explicit_conflict"
    if "rigid_hexamer_clash" in caution:
        return "oligomer_disfavored"
    if len(support) >= 3:
        return "multi_layer_candidate"
    return "method_dependent_or_rescue"


def final_panel(prelim: pd.DataFrame) -> pd.DataFrame:
    picks = [
        ("A", "289|290", "MAP8"),
        ("A", "289|290", "G196_minimal"),
        ("A", "288|289", "MAP8"),
        ("A", "288|289", "HA"),
        ("A", "224|225", "HA"),
        ("A", "248|249", "MAP8"),
        ("A", "287|288", "MAP8"),
        ("A", "290|291", "MAP8"),
        ("B", "289|290", "HA"),
        ("B", "288|289", "G196_minimal"),
        ("B", "290|291", "G196_minimal"),
        ("B", "224|225", "MAP8"),
        ("B", "224|225", "G196_minimal"),
        ("B", "248|249", "HA"),
        ("B", "287|288", "G196_minimal"),
        ("B", "203|204", "G196_minimal"),
        ("control", "256|257", "MAP8"),
        ("control", "155|156", "MAP8"),
    ]
    key = {(r["junction"], r["tag_form"]): r for _, r in prelim.iterrows()}
    rows = []
    counters = Counter()
    for tier, j, tag in picks:
        r = key[(j, tag)]
        counters[tier] += 1
        rows.append({
            "construct_id": r["construct_id"],
            "junction": j,
            "tag_form": tag,
            "tier": "Tier_A_primary" if tier == "A" else ("Tier_B_secondary_rescue" if tier == "B" else "Control"),
            "priority_within_tier": counters[tier],
            "key_supporting_evidence": r["supporting_evidence_labels"],
            "key_negative_evidence": r["negative_evidence_labels"],
            "unresolved_conflicts": r["conflict_class"] + ";no_HRV_A89_specific_insertion_phenotype",
            "wet_lab_inclusion_rationale": wetlab_rationale(tier, j, tag),
            "dynamics_recommended_before_experiment": "yes" if tier in {"A", "B"} else "optional_for_control_calibration",
            "exact_nucleotide_audit_required": "yes",
        })
    return pd.DataFrame(rows)


def wetlab_rationale(tier: str, j: str, tag: str) -> str:
    if tier == "A":
        return "primary diverse panel member; balances structure/tag evidence with explicit homolog conflict"
    if tier == "B":
        return "secondary/rescue construct preserving alternative tag/site hypothesis"
    if j == "155|156":
        return "hard negative biological/control site"
    return "oligomer-disfavored or conflict-control construct"


def dynamics_panel(final: pd.DataFrame) -> pd.DataFrame:
    keep_ids = [
        "A89_2C_289_290_MAP8",
        "A89_2C_289_290_G196_minimal",
        "A89_2C_288_289_MAP8",
        "A89_2C_288_289_HA",
        "A89_2C_224_225_HA",
        "A89_2C_248_249_MAP8",
        "A89_2C_287_288_MAP8",
        "A89_2C_290_291_MAP8",
        "A89_2C_256_257_MAP8",
    ]
    rows = []
    for i, cid in enumerate(keep_ids, start=1):
        r = final[final["construct_id"] == cid].iloc[0]
        rows.append({
            "construct_id": cid,
            "junction": r["junction"],
            "tag_form": r["tag_form"],
            "dynamics_priority": i,
            "panel_role": r["tier"],
            "recommended_strategy": "multiple_short_independent_replicas_not_one_long_single_trajectory",
            "recommended_observables": "native_RMSD;local_RMSF;tag_RMSF;tag_exposure_persistence;secondary_structure_persistence;interface_persistence;contact_network_persistence;replica_convergence;dynamic_cross_correlation;community_network_changes",
            "do_not_execute_in_008": "true",
        })
    return pd.DataFrame(rows)


def qc_summary(paths: list[Path], final: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for p in paths:
        try:
            df = read_tsv(p)
            rows.append({"file": str(p), "status": "parsed", "rows": len(df), "columns": len(df.columns), "duplicate_construct_ids": duplicate_count(df, "construct_id"), "duplicate_junction_tag": duplicate_pair_count(df)})
        except Exception as e:
            rows.append({"file": str(p), "status": f"failed:{e}", "rows": "", "columns": "", "duplicate_construct_ids": "", "duplicate_junction_tag": ""})
    tier_a = final[final["tier"] == "Tier_A_primary"]
    rows.append({"file": "final_panel_tierA_distinct_junctions", "status": tier_a["junction"].nunique(), "rows": "", "columns": "", "duplicate_construct_ids": "", "duplicate_junction_tag": ""})
    rows.append({"file": "final_panel_tierA_distinct_tags", "status": tier_a["tag_form"].nunique(), "rows": "", "columns": "", "duplicate_construct_ids": "", "duplicate_junction_tag": ""})
    return pd.DataFrame(rows)


def duplicate_count(df: pd.DataFrame, col: str) -> int | str:
    return int(df[col].duplicated().sum()) if col in df.columns else "NA"


def duplicate_pair_count(df: pd.DataFrame) -> int | str:
    if {"junction", "tag_form"}.issubset(df.columns):
        return int(df[["junction", "tag_form"]].duplicated().sum())
    return "NA"


def write_docs(portfolio: pd.DataFrame, rna: pd.DataFrame, binder: pd.DataFrame, final: pd.DataFrame, prelim: pd.DataFrame) -> None:
    Path("docs/TAG_PORTFOLIO_V2.md").write_text(tag_portfolio_doc(portfolio))
    Path("docs/RNA_HOLOENZYME_MAPPING_V1.md").write_text(rna_doc(rna))
    Path("docs/TAG_BINDER_ACCESSIBILITY_V1.md").write_text(binder_doc(binder))
    Path("docs/CANDIDATE_PANEL_EXPANSION_008_REPORT.md").write_text(report_doc(final, prelim))


def tag_portfolio_doc(portfolio: pd.DataFrame) -> str:
    lines = ["# TAG_PORTFOLIO_V2", "", "Status: generated by `scripts/candidate_panel_expansion_008.py`.", "", "No tag is assumed safe for HRV-A89 2C.", "", "| Tag | Sequence | Length | Reagent | Status | Main limitation |", "|---|---|---:|---|---|---|"]
    for _, r in portfolio.iterrows():
        lines.append(f"| `{r.tag_form}` | `{r.tag_sequence}` | {r.tag_length} | {r.recognition_reagent} | {r.should_enter_computational_expansion_now} | {r.weaknesses} |")
    lines += ["", "FLAG remains excluded because the 9A5 construct already uses FLAG.", ""]
    return "\n".join(lines)


def rna_doc(rna: pd.DataFrame) -> str:
    counts = rna["rna_holoenzyme_context_class"].value_counts().to_dict()
    return "\n".join([
        "# RNA_HOLOENZYME_MAPPING_V1",
        "",
        "Evidence class: homolog/preprint supporting context.",
        "",
        "The 2026 picornaviral 2C:RNA holoenzyme evidence was mapped through the existing explicit CVB3/FMDV-to-A89 residue records in `data/CVB3_to_A89_functional_mapping_v1.tsv` and summarized for all 320 A89 peptide junctions.",
        "",
        "No preprint coordinate file is committed in this repository, so absolute RNA-path distances are marked unavailable. Residue-neighborhood distances are retained as auditable sequence-coordinate annotations.",
        "",
        f"Context counts: `{counts}`",
        "",
        "This layer is not a binary veto and does not validate any candidate.",
        "",
    ])


def binder_doc(binder: pd.DataFrame) -> str:
    counts = binder["binder_steric_compatibility_class"].value_counts().to_dict()
    return "\n".join([
        "# TAG_BINDER_ACCESSIBILITY_V1",
        "",
        "Binder accessibility is separate from 2C structural tolerance.",
        "",
        "This checkpoint uses inserted-tag geometry, tag-neighbor distances and rigid hexamer clash proxies where real OPEN_STRUCTURE_PIPELINE_007 structures exist. It does not perform mature antibody/nanobody docking.",
        "",
        f"Binder proxy class counts: `{counts}`",
        "",
        "Solvent exposure or low clash is not proof that an antibody/nanobody/LgBiT can bind in infected cells.",
        "",
    ])


def report_doc(final: pd.DataFrame, prelim: pd.DataFrame) -> str:
    tier_counts = final["tier"].value_counts().to_dict()
    tier_a = final[final["tier"] == "Tier_A_primary"]
    new_junctions = sorted(set(final["junction"]) - {"289|290", "290|291"})
    return "\n".join([
        "# CANDIDATE_PANEL_EXPANSION_008_REPORT",
        "",
        "Status: **CANDIDATE_PANEL_EXPANSION_PARTIALLY_COMPLETE**",
        "",
        "This CPU checkpoint completed literature/source records, all-320 feature integration, RNA-holoenzyme residue mapping, protease-boundary motif scanning, tag portfolio expansion, binder-accessibility proxies, preliminary ranking, robustness checks, a draft candidate panel and a proposed dynamics panel.",
        "",
        "Expanded multi-seed ColabFold replication and local multimer modeling are prepared/deferred at this checkpoint; no long MD or final construct design was started.",
        "",
        "## Key Counts",
        "",
        f"- preliminary site x tag rows: {len(prelim)}",
        f"- final draft panel counts: `{tier_counts}`",
        f"- Tier A distinct junctions: {tier_a['junction'].nunique()}",
        f"- Tier A distinct tag systems: {tier_a['tag_form'].nunique()}",
        f"- serious non-289/290 junctions retained: `{new_junctions}`",
        "",
        "## Tier A Draft",
        "",
        "| Construct | Junction | Tag | Main unresolved conflict |",
        "|---|---|---|---|",
        *[f"| `{r.construct_id}` | `{r.junction}` | `{r.tag_form}` | {r.unresolved_conflicts} |" for _, r in tier_a.iterrows()],
        "",
        "## Deferred Methods",
        "",
        "- Extra 008 ColabFold multi-seed replication: not yet completed in this CPU checkpoint; use `data/expanded_structure_replication_panel_v1.tsv` for predeclared panel.",
        "- Local dimer/trimer multimer modeling: deferred to avoid blocking independent ranking outputs.",
        "- IUPred2A/ANCHOR2 disorder/disordered-binding scores: tool not present in current environment; explicit NA status retained.",
        "- Exact RNA/codon audit: blocked until the real experimental nucleotide construct is supplied.",
        "",
        "## Final State",
        "",
        "`CANDIDATE_PANEL_EXPANSION_PARTIALLY_COMPLETE`",
        "",
        "No site is safe or validated. Stop for review before targeted dynamics or construct design.",
        "",
    ])


def update_registry(registry: Path, records: pd.DataFrame) -> None:
    text = registry.read_text()
    marker = "\n## Candidate-panel expansion 008 evidence additions\n"
    block = [marker.strip(), "", "| Source | Class | What it supports here | Boundary |", "|---|---|---|---|"]
    for _, r in records.iterrows():
        block.append(f"| {r.citation}; `{r.doi_pmcid_accession}` | {r.evidence_type}; {r.peer_review_status} | {r.supports} | {r.does_not_support} |")
    block.append("")
    if marker.strip() in text:
        text = text.split(marker.strip())[0].rstrip() + "\n\n" + "\n".join(block)
    else:
        text = text.rstrip() + "\n\n" + "\n".join(block)
    registry.write_text(text + "\n")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    LOGS.mkdir(parents=True, exist_ok=True)
    Path("references/candidate_panel_008").mkdir(parents=True, exist_ok=True)

    records = literature_records()
    records.to_csv("references/candidate_panel_008/literature_source_records_v1.tsv", sep="\t", index=False)
    update_registry(Path("references/LITERATURE_EVIDENCE_REGISTRY.md"), records)

    features = build_feature_matrix()
    features.to_csv("data/junction_feature_matrix_v6_candidate_panel.tsv", sep="\t", index=False)

    rna = build_rna_mapping(features)
    rna.to_csv("data/hrvA89_2C_RNA_holoenzyme_mapping_v1.tsv", sep="\t", index=False)

    portfolio = tag_portfolio()
    portfolio.to_csv("data/tag_portfolio_v2.tsv", sep="\t", index=False)

    open_struct = read_tsv("data/tag_site_integrated_perturbation_v3_open.tsv")
    robustness = read_tsv("results/open_structure_007/cross_method_robustness_v3.tsv")
    panel = select_expanded_panel(features, open_struct)
    panel.to_csv("data/expanded_structure_replication_panel_v1.tsv", sep="\t", index=False)

    protease = protease_risk(panel)
    protease.to_csv("data/tag_boundary_protease_risk_v1.tsv", sep="\t", index=False)

    binder = binder_accessibility(panel, open_struct, portfolio)
    binder.to_csv("data/tag_binder_accessibility_v1.tsv", sep="\t", index=False)

    metrics = expanded_metrics(panel, open_struct, robustness)
    metrics.to_csv("data/expanded_structure_replication_metrics_v1.tsv", sep="\t", index=False)

    multimer = local_multimer_context(panel, metrics)
    multimer.to_csv("data/local_multimer_tag_context_v1.tsv", sep="\t", index=False)

    prelim = preliminary_ranking(panel, features, metrics, binder, protease)
    prelim.to_csv("data/candidate_panel_preliminary_v1.tsv", sep="\t", index=False)

    robust = ranking_robustness(prelim)
    robust.to_csv("results/candidate_panel_008/ranking_robustness_v1.tsv", sep="\t", index=False)

    final = final_panel(prelim)
    final.to_csv("data/final_candidate_panel_draft_v1.tsv", sep="\t", index=False)

    dyn = dynamics_panel(final)
    dyn.to_csv("data/proposed_targeted_dynamics_panel_v1.tsv", sep="\t", index=False)

    qc_paths = [
        Path("data/junction_feature_matrix_v6_candidate_panel.tsv"),
        Path("data/hrvA89_2C_RNA_holoenzyme_mapping_v1.tsv"),
        Path("data/tag_boundary_protease_risk_v1.tsv"),
        Path("data/tag_portfolio_v2.tsv"),
        Path("data/tag_binder_accessibility_v1.tsv"),
        Path("data/expanded_structure_replication_panel_v1.tsv"),
        Path("data/expanded_structure_replication_metrics_v1.tsv"),
        Path("data/local_multimer_tag_context_v1.tsv"),
        Path("data/candidate_panel_preliminary_v1.tsv"),
        Path("results/candidate_panel_008/ranking_robustness_v1.tsv"),
        Path("data/proposed_targeted_dynamics_panel_v1.tsv"),
        Path("data/final_candidate_panel_draft_v1.tsv"),
    ]
    qc = qc_summary(qc_paths, final)
    qc.to_csv("results/candidate_panel_008/qc_summary_v1.tsv", sep="\t", index=False)

    write_docs(portfolio, rna, binder, final, prelim)

    run_log = "\n".join([
        "# CANDIDATE_PANEL_EXPANSION_008_RUN_LOG",
        "",
        "CPU checkpoint generated by `scripts/candidate_panel_expansion_008.py`.",
        "",
        "Completed: literature records, full-320 feature matrix, RNA mapping, protease-risk scan, tag portfolio, binder proxies, preliminary ranking, robustness, final draft panel, proposed dynamics panel.",
        "",
        "Deferred: extra GPU replication and local multimer modeling; disorder/ANCHOR unavailable.",
        "",
    ])
    Path("docs/CANDIDATE_PANEL_EXPANSION_008_RUN_LOG.md").write_text(run_log)


if __name__ == "__main__":
    main()
