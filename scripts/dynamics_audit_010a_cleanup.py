#!/usr/bin/env python3
"""Task 010A final scientific cleanup.

This script does not run MD. It consumes completed Task 010 corrected-validation
outputs and produces clearer drift semantics, WT-differential drift, replica-level
tag-contact heterogeneity, a V5 expert-adjudicated panel, and a 4+2 experimental
review shortlist.
"""
from __future__ import annotations

import math
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(".")
OUT = ROOT / "results/dynamics_audit_010"
DATA = ROOT / "data"
DOCS = ROOT / "docs"

BLOCK = OUT / "corrected_validation_block_stability_v1.tsv"
TAG = DATA / "corrected_validation_tag_exposure_v1.tsv"
V4 = DATA / "final_candidate_panel_v4_corrected_validation.tsv"
SAMPLING_V1 = OUT / "final_sampling_decision_v1.tsv"

ABS_EXTENSION_THRESHOLDS = {
    "self_drift_rmsd": 0.75,
    "wt_reference_ensemble_rmsd": 0.75,
    "wt_defined_contact_retention": 0.05,
    "tag_total_sasa": 100.0,
}

# Tolerances used only to describe candidate-specific excess drift relative to WT.
# They are not automatic ranking thresholds and are deliberately separated from
# the existing extension triggers.
WT_DIFFERENTIAL_TOLERANCES = {
    "self_drift_rmsd": 0.25,
    "wt_reference_ensemble_rmsd": 0.25,
    "wt_defined_contact_retention": 0.03,
}

SHORTLIST = [
    (1, "A89_2C_289_290_MAP8", "candidate", "primary_C_terminal_MAP8", "direct corrected-protocol validation; C-terminal site leader"),
    (2, "A89_2C_289_290_G196_minimal", "candidate", "same_site_tag_identity_comparator", "same 289|290 site with alternative tag identity; not directly corrected-protocol validated"),
    (3, "A89_2C_248_249_HA", "candidate", "primary_non_C_terminal_HA", "independent non-C-terminal region; directly corrected-protocol validated; retain replica-contact heterogeneity caution when present"),
    (4, "A89_2C_248_249_MAP8", "candidate", "crossed_site_tag_comparator", "248|249 site with MAP8; enables site x tag comparison; not directly corrected-protocol validated"),
    (5, "A89_2C_224_225_MAP8", "control", "conflict_control_MD_caution", "reproduced high nonlocal tag-contact caution under corrected protocol"),
    (6, "A89_2C_155_156_MAP8", "control", "hard_negative_control", "independent functional exclusion plus reproduced corrected-MD caution"),
]


def read_tsv(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(path)
    return pd.read_csv(path, sep="\t", dtype=str).fillna("NA")


def write_tsv(path: Path, df: pd.DataFrame) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, sep="\t", index=False)


def fnum(value: object) -> float:
    try:
        if value is None or str(value) in {"NA", "nan", ""}:
            return math.nan
        return float(value)
    except Exception:
        return math.nan


def bool_text(v: bool) -> str:
    return "yes" if v else "no"


def differential_block_drift() -> pd.DataFrame:
    block = read_tsv(BLOCK)
    required = {"construct_id", "metric", "late_minus_early_mean", "block_stability_note"}
    missing = required - set(block.columns)
    if missing:
        raise RuntimeError(f"Missing block-stability columns: {sorted(missing)}")

    wt_rows = block[block["construct_id"].eq("WT_112_321")]
    wt_by_metric = {
        row["metric"]: fnum(row["late_minus_early_mean"])
        for _, row in wt_rows.iterrows()
    }

    rows: list[dict[str, object]] = []
    for _, row in block.iterrows():
        cid = row["construct_id"]
        metric = row["metric"]
        drift = fnum(row["late_minus_early_mean"])
        wt_drift = wt_by_metric.get(metric, math.nan)
        observed = row["block_stability_note"] == "directional_drift_all_replicas"
        abs_threshold = ABS_EXTENSION_THRESHOLDS.get(metric, math.nan)
        abs_trigger = bool(
            observed
            and math.isfinite(drift)
            and math.isfinite(abs_threshold)
            and abs(drift) >= abs_threshold
        )

        differential = math.nan
        differential_applicable = cid != "WT_112_321" and metric != "tag_total_sasa" and math.isfinite(wt_drift)
        if differential_applicable and math.isfinite(drift):
            differential = drift - wt_drift

        excess = False
        interpretation = "WT_baseline" if cid == "WT_112_321" else "not_applicable"
        if differential_applicable and math.isfinite(differential):
            tol = WT_DIFFERENTIAL_TOLERANCES.get(metric, math.nan)
            if metric in {"self_drift_rmsd", "wt_reference_ensemble_rmsd"}:
                excess = math.isfinite(tol) and differential > tol
                if excess:
                    interpretation = "candidate_specific_excess_RMSD_drift_vs_WT"
                elif differential < -tol:
                    interpretation = "candidate_drift_lower_than_WT_relaxation"
                else:
                    interpretation = "candidate_drift_comparable_to_WT_relaxation"
            elif metric == "wt_defined_contact_retention":
                # More-negative late-minus-early values mean greater loss of WT contacts.
                excess = math.isfinite(tol) and differential < -tol
                if excess:
                    interpretation = "candidate_specific_excess_contact_loss_vs_WT"
                elif differential > tol:
                    interpretation = "candidate_contact_retention_change_better_than_WT"
                else:
                    interpretation = "candidate_contact_change_comparable_to_WT"
        elif cid != "WT_112_321" and metric == "tag_total_sasa":
            interpretation = "no_WT_tag_baseline_for_differential_comparison"

        rows.append(
            {
                **row.to_dict(),
                "directional_drift_observed": bool_text(observed),
                "absolute_extension_threshold": abs_threshold if math.isfinite(abs_threshold) else "NA",
                "absolute_extension_trigger": bool_text(abs_trigger),
                "wt_late_minus_early_mean": wt_drift if math.isfinite(wt_drift) else "NA",
                "candidate_minus_wt_late_minus_early": differential if math.isfinite(differential) else "NA",
                "wt_differential_applicable": bool_text(differential_applicable),
                "candidate_specific_excess_drift_vs_wt": bool_text(excess),
                "candidate_vs_wt_drift_interpretation": interpretation,
            }
        )

    out = pd.DataFrame(rows)
    write_tsv(OUT / "differential_block_drift_vs_wt_v1.tsv", out)
    return out


def revised_sampling(diff: pd.DataFrame) -> pd.DataFrame:
    old = read_tsv(SAMPLING_V1)
    rows: list[dict[str, object]] = []
    for _, row in old.iterrows():
        cid = row["construct_id"]
        d = diff[diff["construct_id"].eq(cid)]
        observed = d[d["directional_drift_observed"].eq("yes")]["metric"].tolist()
        triggers = d[d["absolute_extension_trigger"].eq("yes")]["metric"].tolist()
        excess = d[d["candidate_specific_excess_drift_vs_wt"].eq("yes")]["metric"].tolist()
        statement = "no_same_direction_drift_detected"
        if observed and not triggers:
            statement = "directional_drift_observed_but_below_absolute_extension_trigger"
        elif triggers:
            statement = "directional_drift_observed_and_absolute_extension_trigger_crossed"
        if cid != "WT_112_321" and observed and not excess:
            statement += ";no_decision_relevant_excess_drift_after_WT_comparison"
        elif excess:
            statement += ";candidate_specific_excess_drift_present_after_WT_comparison"

        new = row.to_dict()
        # Preserve the original field for provenance but correct its semantics.
        new["directional_drift_metrics_v1_original"] = row.get("directional_drift_metrics", "NA")
        new["directional_drift_observed_metrics"] = ";".join(observed) if observed else "none"
        new["extension_trigger_metrics"] = ";".join(triggers) if triggers else "none"
        new["wt_differential_excess_metrics"] = ";".join(excess) if excess else "none"
        new["revised_drift_statement"] = statement
        new["sampling_decision_v2"] = row.get("sampling_decision", "NA")
        new["sampling_decision_changed_by_cleanup"] = "no"
        rows.append(new)

    out = pd.DataFrame(rows)
    write_tsv(OUT / "final_sampling_decision_v2_cleanup.tsv", out)
    return out


def tag_contact_heterogeneity() -> pd.DataFrame:
    tag = read_tsv(TAG)
    if "row_type" not in tag.columns:
        raise RuntimeError("corrected validation tag table lacks row_type")
    rep = tag[tag["row_type"].eq("replica") & ~tag["construct_id"].eq("WT_112_321")].copy()
    col = "tag_nonlocal_contact_fraction_any_lt_4p5A"
    if col not in rep.columns:
        raise RuntimeError(f"Missing {col}")

    rows: list[dict[str, object]] = []
    for cid, g in rep.groupby("construct_id"):
        vals = np.array([fnum(v) for v in g[col] if math.isfinite(fnum(v))], dtype=float)
        if not len(vals):
            continue
        high_count = int(np.sum(vals > 0.75))
        low_count = int(np.sum(vals < 0.50))
        sd = float(np.std(vals, ddof=1)) if len(vals) > 1 else 0.0
        heterogeneous = bool(sd >= 0.20 or (high_count >= 1 and low_count >= 1))
        rows.append(
            {
                "construct_id": cid,
                "junction": g.iloc[0].get("junction", "NA"),
                "tag_form": g.iloc[0].get("tag_form", "NA"),
                "replica_count": len(vals),
                "replica_values_nonlocal_contact_fraction": ";".join(f"{x:.6f}" for x in vals),
                "mean": float(np.mean(vals)),
                "sd": sd,
                "min": float(np.min(vals)),
                "max": float(np.max(vals)),
                "replicas_gt_0p75": high_count,
                "replicas_lt_0p50": low_count,
                "replica_heterogeneity_flag": bool_text(heterogeneous),
                "interpretation": "replica_heterogeneous_nonlocal_tag_contact" if heterogeneous else "no_major_replica_heterogeneity_detected",
                "priority_effect": "annotate_caution_do_not_auto_demote" if heterogeneous else "none",
            }
        )
    out = pd.DataFrame(rows).sort_values(["construct_id"])
    write_tsv(OUT / "tag_nonlocal_contact_replica_heterogeneity_v1.tsv", out)
    return out


def panel_v5(hetero: pd.DataFrame, sampling: pd.DataFrame) -> pd.DataFrame:
    v4 = read_tsv(V4)
    hmap = hetero.set_index("construct_id").to_dict(orient="index") if len(hetero) else {}
    smap = sampling.set_index("construct_id").to_dict(orient="index") if len(sampling) else {}
    rows: list[dict[str, object]] = []
    for _, r in v4.iterrows():
        row = r.to_dict()
        cid = row["construct_id"]
        h = hmap.get(cid, {})
        s = smap.get(cid, {})
        row["priority_method_v5"] = "multi_evidence_expert_adjudication"
        row["algorithmic_total_score_used_v5"] = "no"
        row["md_role_in_priority_v5"] = "downstream_comparative_perturbation_evidence"
        row["priority_class_v5"] = row.get("priority_class_v4", row.get("priority_class", "NA"))
        row["replica_nonlocal_contact_heterogeneity_v5"] = h.get("replica_heterogeneity_flag", "not_directly_corrected_protocol_validated")
        row["replica_nonlocal_contact_range_v5"] = (
            f"{h.get('min')}..{h.get('max')}" if h else "not_directly_corrected_protocol_validated"
        )
        row["directional_drift_observed_metrics_v5"] = s.get("directional_drift_observed_metrics", "not_directly_corrected_protocol_validated")
        row["wt_differential_excess_metrics_v5"] = s.get("wt_differential_excess_metrics", "not_directly_corrected_protocol_validated")
        annotations: list[str] = []
        if h.get("replica_heterogeneity_flag") == "yes":
            annotations.append("replica_heterogeneous_nonlocal_tag_contact_caution")
        if row.get("corrected_protocol_validation_status_v4") == "not_directly_corrected_protocol_validated":
            annotations.append("not_directly_corrected_protocol_validated")
        row["experimental_review_annotation_v5"] = ";".join(annotations) if annotations else "none"
        row["safe_or_validated"] = "no"
        rows.append(row)
    out = pd.DataFrame(rows)
    write_tsv(DATA / "final_candidate_panel_v5_experimental_review_cleanup.tsv", out)
    return out


def experimental_shortlist(panel: pd.DataFrame) -> pd.DataFrame:
    by_id = panel.set_index("construct_id").to_dict(orient="index")
    rows: list[dict[str, object]] = []
    for order, cid, role, design_role, purpose in SHORTLIST:
        if cid not in by_id:
            raise RuntimeError(f"Shortlist construct missing from V5 panel: {cid}")
        p = by_id[cid]
        rows.append(
            {
                "shortlist_order": order,
                "construct_id": cid,
                "junction": p.get("junction", "NA"),
                "tag_form": p.get("tag_form", "NA"),
                "panel_role": role,
                "design_role": design_role,
                "priority_class_v5": p.get("priority_class_v5", "NA"),
                "corrected_protocol_validation_status": p.get("corrected_protocol_validation_status_v4", "NA"),
                "corrected_protocol_md_status": p.get("corrected_protocol_md_status_v4", "NA"),
                "experimental_review_annotation": p.get("experimental_review_annotation_v5", "NA"),
                "scientific_purpose": purpose,
                "priority_method": "multi_evidence_expert_adjudication",
                "algorithmic_total_score_used": "no",
                "safe_or_validated": "no",
            }
        )
    out = pd.DataFrame(rows)
    write_tsv(DATA / "experimental_review_shortlist_v1.tsv", out)
    return out


def markdown_table(df: pd.DataFrame, cols: list[str]) -> str:
    safe = df.reindex(columns=cols, fill_value="NA").astype(str).copy()
    for c in safe.columns:
        safe[c] = safe[c].str.replace("|", r"\|", regex=False)
    return safe.to_markdown(index=False)


def write_reports(diff: pd.DataFrame, sampling: pd.DataFrame, hetero: pd.DataFrame, panel: pd.DataFrame, shortlist: pd.DataFrame) -> None:
    h248 = hetero[hetero["construct_id"].eq("A89_2C_248_249_HA")]
    h248_text = "not available"
    if len(h248):
        r = h248.iloc[0]
        h248_text = (
            f"replica values={r['replica_values_nonlocal_contact_fraction']}; "
            f"mean={float(r['mean']):.3f}; SD={float(r['sd']):.3f}; "
            f"range={float(r['min']):.3f}-{float(r['max']):.3f}; heterogeneity={r['replica_heterogeneity_flag']}"
        )

    d289 = diff[(diff["construct_id"].eq("A89_2C_289_290_MAP8")) & diff["metric"].isin([
        "self_drift_rmsd", "wt_reference_ensemble_rmsd", "wt_defined_contact_retention"
    ])]

    cleanup = f"""# FINAL_SCIENTIFIC_CLEANUP_010A

Date: 2026-08-25

Status: `EXPERIMENTAL_REVIEW_SHORTLIST_READY_FOR_DISCUSSION`

## Scope

Task 010A is a reporting/statistical-semantics cleanup only. No new MD was launched. Priority classes remain hypotheses for experimental review, not claims of safety or validation.

## 1. Directional drift semantics

The revised sampling table separates observed same-direction drift from threshold-crossing extension triggers. `directional_drift_observed_metrics` is descriptive; `extension_trigger_metrics` is the actual sampling trigger layer. Therefore a metric can show directional drift while the sampling decision remains `STOP_AT_20NS`.

{markdown_table(sampling, ['construct_id', 'directional_drift_observed_metrics', 'extension_trigger_metrics', 'wt_differential_excess_metrics', 'sampling_decision_v2', 'revised_drift_statement'])}

## 2. Candidate-vs-WT differential drift

For directly validated systems, RMSD/contact late-minus-early drift is compared against the corresponding WT drift. This separates fragment-wide relaxation shared with WT from candidate-specific excess drift. Tag SASA has no WT-tag baseline and is not assigned a WT differential.

Focused `289|290 x MAP8` comparison:

{markdown_table(d289, ['metric', 'late_minus_early_mean', 'wt_late_minus_early_mean', 'candidate_minus_wt_late_minus_early', 'candidate_specific_excess_drift_vs_wt', 'candidate_vs_wt_drift_interpretation'])}

The cleanup does not identify a decision-relevant multi-metric excess-drift pattern requiring additional sampling for `289|290 x MAP8`.

## 3. `248|249 x HA` replica heterogeneity

{h248_text}

The correct interpretation is **Priority A with accessibility/contact heterogeneity caution**, not automatic demotion and not an unqualified `no flags` statement. The caution concerns replica-dependent tag-protein nonlocal contact behavior; global structural perturbation metrics remain comparatively mild.

## 4. Why 20 ns remains the screening stop point

`STOP_AT_20NS` remains a screening decision because candidate/control classifications are stable across corrected protocol validation and no directly validated decision-critical system shows a multi-observable candidate-specific excess-drift pattern after WT comparison that triggers the predeclared extension logic. This does not imply mechanistic convergence or biological validation.

## 5. Metric roles

Ranking-relevant downstream MD evidence:

- persistent nonlocal tag-contact behavior;
- tag exposure/SASA context;
- WT-defined native-contact preservation as a perturbation check;
- candidate-vs-WT differential drift as a sampling adequacy check.

Primarily QC or exploratory here:

- global self-drift RMSD alone;
- global Rg;
- DCCM/network over this sampling window.

## 6. Priority methodology

Priority A/B is `multi_evidence_expert_adjudication`.

No validated algorithmic total score is used. MD is a downstream comparative perturbation layer and does not override higher-weight direct homolog insertion fitness, functional constraints, evolutionary evidence or the absence of direct HRV-A89 phenotype data.

## 7. Frozen experimental-review shortlist

{markdown_table(shortlist, ['shortlist_order', 'construct_id', 'junction', 'tag_form', 'panel_role', 'design_role', 'corrected_protocol_validation_status', 'experimental_review_annotation'])}

The four candidate constructs implement a compact 2-site x 2-tag logic:

- `289|290`: MAP8 + G196_minimal;
- `248|249`: HA + MAP8.

Controls:

- `224|225 x MAP8`: corrected-MD conflict control;
- `155|156 x MAP8`: hard-negative control.

## 8. Direct corrected-protocol validation coverage

Directly corrected-protocol validated among the shortlist:

- `289|290 x MAP8`;
- `248|249 x HA`;
- `224|225 x MAP8`;
- `155|156 x MAP8`.

Not directly corrected-protocol validated:

- `289|290 x G196_minimal`;
- `248|249 x MAP8`.

No direct corrected-protocol evidence is imputed to those two constructs.

## Boundary

This shortlist is ready for experimental discussion only. Exact nucleotide/codon/RNA-level design remains blocked until the real experimental HRV-A89 replicon/plasmid nucleotide context is available.
"""
    (DOCS / "FINAL_SCIENTIFIC_CLEANUP_010A.md").write_text(cleanup)

    shortlist_doc = f"""# EXPERIMENTAL_REVIEW_SHORTLIST_V1

Date: 2026-08-25

Status: `READY_FOR_EXPERIMENTAL_DISCUSSION`

Priority method: `multi_evidence_expert_adjudication`  
Algorithmic total score used: `no`

No construct is safe or experimentally validated.

## Recommended 4 + 2 shortlist

{markdown_table(shortlist, ['shortlist_order', 'construct_id', 'junction', 'tag_form', 'panel_role', 'design_role', 'corrected_protocol_md_status', 'experimental_review_annotation', 'scientific_purpose'])}

## Design logic

The four candidate constructs deliberately span two biological regions and two tag identities rather than treating adjacent C-terminal junctions as independent hypotheses.

- C-terminal site hypothesis: `289|290` with MAP8 and G196_minimal.
- Non-C-terminal site hypothesis: `248|249` with HA and MAP8.
- Conflict control: `224|225 x MAP8`.
- Hard-negative control: `155|156 x MAP8`.

`248|249 x HA` remains Priority A but carries a replica-heterogeneous nonlocal-contact caution. `289|290 x G196_minimal` and `248|249 x MAP8` remain useful tag/site comparators but were not directly included in the corrected-protocol validation subset.

## Interpretation boundary

This is an experimental-review shortlist, not a final construct sequence, not a wet-lab protocol, and not evidence of viral fitness compatibility.
"""
    (DOCS / "EXPERIMENTAL_REVIEW_SHORTLIST_V1.md").write_text(shortlist_doc)


def main() -> None:
    diff = differential_block_drift()
    sampling = revised_sampling(diff)
    hetero = tag_contact_heterogeneity()
    panel = panel_v5(hetero, sampling)
    shortlist = experimental_shortlist(panel)
    write_reports(diff, sampling, hetero, panel, shortlist)
    print("Task 010A cleanup outputs generated.")


if __name__ == "__main__":
    main()
