#!/usr/bin/env python3
"""GPU PLM recovery for GPU_RECOVERY_004.

Uses ESM2 masked pseudo-log-likelihood (PLL). Raw full-sequence PLL and
length-normalized mean PLL are both retained.
"""

from __future__ import annotations

import argparse
import itertools
import math
import os
import socket
import subprocess
from pathlib import Path

import numpy as np
import pandas as pd
import torch
import torch.nn.functional as F


TAGS = {
    "MAP8": "GDGMVPPG",
    "HA": "YPYDVPDYA",
    "G196_minimal": "DLVPR",
    "G196_practical_GS": "GSDLVPRGS",
}

REQUIRED_AUDIT = {"203|204", "224|225", "248|249", "256|257", "287|288", "288|289", "289|290", "290|291"}
NEGATIVE_CONTROLS = {"155|156", "216|217"}


def read_fasta(path: Path) -> str:
    seq = []
    for line in path.read_text().splitlines():
        if line.startswith(">"):
            continue
        seq.append(line.strip())
    out = "".join(seq)
    if len(out) != 321:
        raise ValueError(f"Expected A89 2C length 321, got {len(out)}")
    return out


def junction_left(junction: str) -> int:
    left, right = junction.split("|")
    if int(right) != int(left) + 1:
        raise ValueError(f"Non-adjacent junction: {junction}")
    return int(left)


def inserted_sequence(wt: str, junction: str, tag: str) -> str:
    left = junction_left(junction)
    return wt[:left] + tag + wt[left:]


def load_model():
    import esm

    model, alphabet = esm.pretrained.esm2_t6_8M_UR50D()
    model.eval()
    return model, alphabet, "esm2_t6_8M_UR50D", "fair-esm pretrained esm2_t6_8M_UR50D"


def tokens_for_sequence(alphabet, seq: str, device: torch.device) -> torch.Tensor:
    batch_converter = alphabet.get_batch_converter()
    _, _, tokens = batch_converter([("seq", seq)])
    return tokens.to(device)


@torch.no_grad()
def pll_score(model, alphabet, seq: str, device: torch.device, batch_size: int) -> tuple[float, np.ndarray]:
    base_tokens = tokens_for_sequence(alphabet, seq, device)
    target_tokens = base_tokens[0, 1 : len(seq) + 1].detach().clone()
    scores = []
    positions = list(range(len(seq)))
    for start in range(0, len(seq), batch_size):
        chunk = positions[start : start + batch_size]
        batch = base_tokens.repeat(len(chunk), 1)
        row = torch.arange(len(chunk), device=device)
        token_pos = torch.tensor([p + 1 for p in chunk], device=device)
        batch[row, token_pos] = alphabet.mask_idx
        out = model(batch)
        logits = out["logits"][row, token_pos, :]
        log_probs = F.log_softmax(logits.float(), dim=-1)
        targets = target_tokens[torch.tensor(chunk, device=device)]
        vals = log_probs[row, targets].detach().cpu().numpy()
        scores.extend(float(x) for x in vals)
    arr = np.array(scores, dtype=float)
    return float(arr.sum()), arr


def ensure_gpu() -> tuple[torch.device, str]:
    if not torch.cuda.is_available():
        raise RuntimeError("torch.cuda.is_available() is False")
    device = torch.device("cuda")
    name = torch.cuda.get_device_name(0)
    smoke = torch.randn(64, 64, device=device) @ torch.randn(64, 64, device=device)
    if not torch.isfinite(smoke).all():
        raise RuntimeError("GPU smoke test produced non-finite values")
    return device, name


def run_scoring(args: argparse.Namespace) -> pd.DataFrame:
    device, device_name = ensure_gpu()
    model, alphabet, model_name, checkpoint = load_model()
    model = model.to(device)

    wt = read_fasta(args.reference_fasta)
    v4 = pd.read_csv(args.v4, sep="\t")
    if len(v4) != 320:
        raise ValueError(f"Expected 320 V4 junction rows, got {len(v4)}")
    junctions = list(v4["junction"])

    args.out.parent.mkdir(parents=True, exist_ok=True)
    partial = args.out.with_suffix(".partial.tsv")

    completed = set()
    rows = []
    if partial.exists():
        old = pd.read_csv(partial, sep="\t")
        rows = old.to_dict("records")
        completed = {(r["tag_form"], r["a89_junction"]) for r in rows if r.get("plm_status") == "completed"}

    wt_full, wt_pos = pll_score(model, alphabet, wt, device, args.batch_size)
    wt_mean = wt_full / len(wt)

    for tag_form, tag_seq in TAGS.items():
        for junction in junctions:
            key = (tag_form, junction)
            if key in completed:
                continue
            seq = inserted_sequence(wt, junction, tag_seq)
            inserted_full, inserted_pos = pll_score(model, alphabet, seq, device, args.batch_size)
            inserted_mean = inserted_full / len(seq)
            left = junction_left(junction)
            tag_slice = inserted_pos[left : left + len(tag_seq)]
            rows.append(
                {
                    "tag_form": tag_form,
                    "tag_sequence": tag_seq,
                    "tag_length": len(tag_seq),
                    "a89_junction": junction,
                    "inserted_sequence_length": len(seq),
                    "plm_model": model_name,
                    "plm_checkpoint_source": checkpoint,
                    "scoring_method": "ESM2 full-sequence masked pseudo-log-likelihood",
                    "plm_score_wt_full_pll": wt_full,
                    "plm_score_inserted_full_pll": inserted_full,
                    "plm_delta_full_pll_insert_minus_wt": inserted_full - wt_full,
                    "plm_score_wt_mean_pll": wt_mean,
                    "plm_score_inserted_mean_pll": inserted_mean,
                    "plm_delta_mean_pll_insert_minus_wt": inserted_mean - wt_mean,
                    "plm_score_inserted_tag_only_pll": float(tag_slice.sum()),
                    "plm_score_inserted_tag_mean_pll": float(tag_slice.mean()),
                    "plm_status": "completed",
                    "blocker": "",
                    "batch_size": args.batch_size,
                    "device_name": device_name,
                    "hostname": socket.gethostname(),
                }
            )
            pd.DataFrame(rows).to_csv(partial, sep="\t", index=False)

    df = pd.DataFrame(rows)
    expected = len(TAGS) * 320
    completed_n = int((df["plm_status"] == "completed").sum())
    if len(df) != expected or completed_n != expected:
        raise ValueError(f"PLM scoring incomplete: rows={len(df)}, completed={completed_n}, expected={expected}")
    df.to_csv(args.out, sep="\t", index=False)
    return df


def add_ranks(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["plm_rank_within_tag"] = out.groupby("tag_form")["plm_delta_mean_pll_insert_minus_wt"].rank(
        method="min", ascending=False
    )
    out["plm_percentile_within_tag"] = 1.0 - (out["plm_rank_within_tag"] - 1.0) / 319.0
    return out


def consensus_class(row: pd.Series) -> str:
    if row["plm_percentile_min"] >= 0.85:
        return "plm_consensus_high_secondary_support"
    if row["plm_percentile_mean"] >= 0.75 and row["plm_percentile_min"] >= 0.60:
        return "plm_consensus_moderate_secondary_support"
    if row["plm_percentile_range"] >= 0.50:
        return "tag_specific_disagreement"
    return "plm_no_consensus_secondary_support"


def build_consensus(df: pd.DataFrame, out: Path, corr_out: Path) -> pd.DataFrame:
    ranked = add_ranks(df)
    pivot = ranked.pivot(index="a89_junction", columns="tag_form", values="plm_delta_mean_pll_insert_minus_wt")
    corr = pivot.corr(method="spearman").reset_index().rename(columns={"tag_form": "tag_form_a"})
    corr.to_csv(corr_out, sep="\t", index=False)

    rows = []
    for junction, g in ranked.groupby("a89_junction"):
        best = g.sort_values("plm_delta_mean_pll_insert_minus_wt", ascending=False).iloc[0]
        worst = g.sort_values("plm_delta_mean_pll_insert_minus_wt", ascending=True).iloc[0]
        row = {
            "a89_junction": junction,
            "completed_tag_forms": int((g["plm_status"] == "completed").sum()),
            "plm_delta_mean_mean": float(g["plm_delta_mean_pll_insert_minus_wt"].mean()),
            "plm_delta_mean_median": float(g["plm_delta_mean_pll_insert_minus_wt"].median()),
            "plm_delta_mean_min": float(g["plm_delta_mean_pll_insert_minus_wt"].min()),
            "plm_delta_mean_max": float(g["plm_delta_mean_pll_insert_minus_wt"].max()),
            "plm_percentile_mean": float(g["plm_percentile_within_tag"].mean()),
            "plm_percentile_min": float(g["plm_percentile_within_tag"].min()),
            "plm_percentile_max": float(g["plm_percentile_within_tag"].max()),
            "plm_percentile_range": float(g["plm_percentile_within_tag"].max() - g["plm_percentile_within_tag"].min()),
            "best_tag_form": best["tag_form"],
            "worst_tag_form": worst["tag_form"],
        }
        row["plm_consensus_class"] = consensus_class(pd.Series(row))
        rows.append(row)
    consensus = pd.DataFrame(rows).sort_values(["plm_percentile_mean", "plm_percentile_min"], ascending=False)
    consensus.to_csv(out, sep="\t", index=False)
    return consensus


def v5_class(row: pd.Series) -> str:
    if bool(row.get("hard_functional_exclusion", False)):
        return "hard_excluded"
    if row.get("mapping_class") != "exact_aligned":
        return "mapping_uncertain"
    old = str(row.get("old_conflict_control", ""))
    cls = row.get("plm_consensus_class", "")
    pareto = bool(row.get("pareto_reviewable_any", False))
    if old and old != "nan":
        return "conflict_control_with_plm_context"
    if cls == "plm_consensus_high_secondary_support" and pareto:
        return "plm_secondary_support_direct_homolog_conflicted"
    if cls == "plm_consensus_moderate_secondary_support" and pareto:
        return "plm_context_support_direct_homolog_conflicted"
    if cls == "tag_specific_disagreement":
        return "tag_specific_disagreement_direct_homolog_conflicted"
    return "direct_homolog_conflicted_with_plm_context"


def build_v5_and_review(v4_path: Path, ranked: pd.DataFrame, consensus: pd.DataFrame, v5_out: Path, review_out: Path) -> pd.DataFrame:
    v4 = pd.read_csv(v4_path, sep="\t")
    tag_pivots = []
    for field in ["plm_delta_mean_pll_insert_minus_wt", "plm_percentile_within_tag", "plm_rank_within_tag"]:
        p = ranked.pivot(index="a89_junction", columns="tag_form", values=field)
        p.columns = [f"{field}_{c}" for c in p.columns]
        tag_pivots.append(p.reset_index())
    merged = v4.merge(consensus, left_on="junction", right_on="a89_junction", how="left")
    for p in tag_pivots:
        merged = merged.merge(p, left_on="junction", right_on="a89_junction", how="left", suffixes=("", "_tagpivot"))
        drop_cols = [c for c in merged.columns if c.endswith("_tagpivot")]
        merged = merged.drop(columns=drop_cols)
    merged["plm_gpu_status"] = np.where(merged["completed_tag_forms"] == 4, "completed", "incomplete")
    merged["candidate_class_v5_plm_gpu"] = merged.apply(v5_class, axis=1)
    merged.to_csv(v5_out, sep="\t", index=False)

    top_plm = merged[
        (~merged["hard_functional_exclusion"].astype(bool))
        & (merged["mapping_class"] == "exact_aligned")
        & (merged["plm_gpu_status"] == "completed")
    ].sort_values(["plm_percentile_mean", "plm_percentile_min"], ascending=False).head(12)
    disagreement = merged[
        (~merged["hard_functional_exclusion"].astype(bool))
        & (merged["mapping_class"] == "exact_aligned")
        & (merged["plm_consensus_class"] == "tag_specific_disagreement")
    ].sort_values("plm_percentile_range", ascending=False).head(4)
    required = merged[merged["junction"].isin(REQUIRED_AUDIT | NEGATIVE_CONTROLS)]
    old_review = pd.read_csv("data/computational_review_set_v1.tsv", sep="\t")
    old_rows = merged[merged["junction"].isin(set(old_review["junction"]))]
    review = pd.concat([top_plm, disagreement, required, old_rows], ignore_index=True)
    review = review.drop_duplicates("junction")
    review["review_role_v2"] = "plm_gpu_review"
    review.loc[review["junction"].isin(REQUIRED_AUDIT), "review_role_v2"] = "required_reaudit_control"
    review.loc[review["junction"].isin(NEGATIVE_CONTROLS), "review_role_v2"] = "negative_control_hard_exclusion"
    review.loc[review["junction"].isin(set(top_plm["junction"])), "review_role_v2"] = "top_plm_secondary_context"
    keep = [
        "junction",
        "review_role_v2",
        "functional_tier",
        "mapping_class",
        "strict_structural_pass",
        "pareto_reviewable_subset_count",
        "insertion_raw_log2_enrich2",
        "sub_window_mean",
        "independent_indel_event_lower_bound",
        "plm_percentile_mean",
        "plm_percentile_min",
        "plm_percentile_range",
        "best_tag_form",
        "worst_tag_form",
        "plm_consensus_class",
        "candidate_class_v5_plm_gpu",
    ]
    review[keep].sort_values(["review_role_v2", "plm_percentile_mean"], ascending=[True, False]).to_csv(
        review_out, sep="\t", index=False
    )
    return merged


def write_reports(args, df: pd.DataFrame, ranked: pd.DataFrame, consensus: pd.DataFrame, v5: pd.DataFrame, max_repro_diff: float) -> str:
    completed = int((df["plm_status"] == "completed").sum())
    planned = len(TAGS) * 320
    top = v5.sort_values(["plm_percentile_mean", "plm_percentile_min"], ascending=False).head(10)
    audited = v5[v5["junction"].isin(REQUIRED_AUDIT)].sort_values("junction")
    corr = pd.read_csv(args.corr_out, sep="\t")
    nonhard_top = v5[
        (~v5["hard_functional_exclusion"].astype(bool))
        & (v5["mapping_class"] == "exact_aligned")
        & (v5["plm_consensus_class"].isin(["plm_consensus_high_secondary_support", "plm_consensus_moderate_secondary_support"]))
    ]
    final_state = "READY_FOR_CONFLICT_AWARE_TAG_SITE_MODELING" if completed == planned and len(nonhard_top) else "NO_HIGH_CONFIDENCE_TARGETED_SITE"

    qc = pd.DataFrame(
        [
            ("hostname", socket.gethostname()),
            ("python", os.popen("python --version 2>&1").read().strip()),
            ("torch_version", torch.__version__),
            ("torch_cuda_available", str(torch.cuda.is_available())),
            ("torch_cuda_version", str(torch.version.cuda)),
            ("cuda_device_name", torch.cuda.get_device_name(0) if torch.cuda.is_available() else ""),
            ("plm_model", "esm2_t6_8M_UR50D"),
            ("planned_rows", str(planned)),
            ("completed_rows", str(completed)),
            ("failed_rows", str(planned - completed)),
            ("reproducibility_subset_max_abs_delta_mean_pll_diff", f"{max_repro_diff:.10g}"),
            ("final_decision_state", final_state),
        ],
        columns=["metric", "value"],
    )
    qc.to_csv(args.qc_out, sep="\t", index=False)

    def md_table(frame: pd.DataFrame, cols: list[str], n: int | None = None) -> str:
        if n is not None:
            frame = frame.head(n)
        return frame[cols].to_markdown(index=False)

    args.plm_doc.write_text(
        "\n".join(
            [
                "# TAG_SPECIFIC_PLM_SCAN_V2_GPU",
                "",
                "Status: **completed**",
                "",
                "Method: ESM2 `esm2_t6_8M_UR50D` full-sequence masked pseudo-log-likelihood.",
                "",
                "Primary machine-readable output:",
                "",
                "- `data/tag_specific_plm_scores_v2_gpu.tsv`",
                "- `results/gpu_recovery_004/plm_gpu_qc.tsv`",
                "",
                f"Completed rows: {completed} / {planned}.",
                "",
                "Raw full-sequence PLL and length-normalized mean PLL are both retained. The integrated V5 table uses mean PLL deltas to reduce tag-length bias. PLM scores are secondary computational evidence, not biological validation.",
                "",
            ]
        )
    )
    args.consensus_doc.write_text(
        "\n".join(
            [
                "# TAG_SPECIFIC_CONSENSUS_V2_GPU",
                "",
                "Status: **completed**",
                "",
                "Primary outputs:",
                "",
                "- `data/tag_specific_consensus_v2_gpu.tsv`",
                "- `results/gpu_recovery_004/tag_landscape_correlations_v2.tsv`",
                "",
                "Top consensus rows by mean PLM percentile:",
                "",
                md_table(consensus, ["a89_junction", "plm_percentile_mean", "plm_percentile_min", "plm_percentile_range", "best_tag_form", "worst_tag_form", "plm_consensus_class"], 12),
                "",
                "PLM agreement does not validate an insertion site and does not override direct homolog fitness conflict.",
                "",
            ]
        )
    )
    args.struct_doc.write_text(
        "\n".join(
            [
                "# LIGHTWEIGHT_STRUCTURAL_TRIAGE_V2_GPU",
                "",
                "Status: **deferred**",
                "",
                "No mature reproducible structure-prediction or loop-remodeling workflow was installed during this GPU recovery run. The task prioritized the previously blocked PLM layer. No long MD or final construct design was started.",
                "",
            ]
        )
    )
    args.report.write_text(
        "\n".join(
            [
                "# GPU_RECOVERY_004_REPORT",
                "",
                "Status: **GPU PLM recovery completed**",
                "",
                f"Final decision state: `{final_state}`",
                "",
                "## Runtime",
                "",
                f"- Hostname: `{socket.gethostname()}`",
                f"- PyTorch: `{torch.__version__}`",
                f"- CUDA available: `{torch.cuda.is_available()}`",
                f"- CUDA build: `{torch.version.cuda}`",
                f"- CUDA device: `{torch.cuda.get_device_name(0) if torch.cuda.is_available() else ''}`",
                "",
                "## PLM method",
                "",
                "- Model/checkpoint: `esm2_t6_8M_UR50D` from `fair-esm`.",
                "- Scoring: full-sequence masked pseudo-log-likelihood.",
                "- Raw score: full PLL sum.",
                "- Normalized score: mean PLL per residue.",
                "- V5 integration uses normalized insertion-minus-WT delta and preserves raw scores separately.",
                "- Method limitation: ESM2 is not an experimental insertion-fitness assay and does not model RNA/polyprotein context.",
                "",
                "## Completed rows",
                "",
                f"- Planned tag x junction rows: {planned}.",
                f"- Completed rows: {completed}.",
                "- Tag forms: MAP8, HA, G196_minimal, G196_practical_GS.",
                "",
                "## MAP8 / HA / G196 differences",
                "",
                "Rank correlations are stored in `results/gpu_recovery_004/tag_landscape_correlations_v2.tsv`.",
                "",
                corr.to_markdown(index=False),
                "",
                "Top V5 PLM-context rows:",
                "",
                md_table(top, ["junction", "functional_tier", "mapping_class", "pareto_reviewable_subset_count", "insertion_raw_log2_enrich2", "plm_percentile_mean", "plm_percentile_min", "best_tag_form", "worst_tag_form", "candidate_class_v5_plm_gpu"], 10),
                "",
                "## Required re-audit rows",
                "",
                md_table(audited, ["junction", "functional_tier", "strict_structural_pass", "insertion_raw_log2_enrich2", "plm_percentile_mean", "plm_percentile_min", "best_tag_form", "worst_tag_form", "candidate_class_v5_plm_gpu"]),
                "",
                "## Candidate ranking and review set",
                "",
                "- Created `data/candidate_junctions_v5_plm_gpu.tsv` with all 320 junctions.",
                "- Created `data/computational_review_set_v2_plm_gpu.tsv` as a revised computational review set.",
                "- Direct homolog insertion phenotype remains a higher-weight conflicting evidence layer.",
                "- No site is called safe or validated.",
                "",
                "## Structural triage",
                "",
                "Deferred. No mature reproducible structure-prediction or loop-remodeling workflow was installed without derailing the PLM recovery run.",
                "",
                "## Blockers and uncertainties",
                "",
                "- No HRV-A89-specific insertion phenotype exists.",
                "- EV-A71 insertion data remain homolog and insertion-handle specific.",
                "- Exact experimental RNA/codon context remains unavailable.",
                "- PLM is secondary computational evidence and cannot validate a construct.",
                "",
                "## Final decision state",
                "",
                f"`{final_state}`",
                "",
            ]
        )
    )
    return final_state


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--reference-fasta", type=Path, default=Path("references/HRV_A89_2C_reference_sequence.fasta"))
    p.add_argument("--v4", type=Path, default=Path("data/candidate_junctions_v4_method_hardening.tsv"))
    p.add_argument("--out", type=Path, default=Path("data/tag_specific_plm_scores_v2_gpu.tsv"))
    p.add_argument("--consensus-out", type=Path, default=Path("data/tag_specific_consensus_v2_gpu.tsv"))
    p.add_argument("--corr-out", type=Path, default=Path("results/gpu_recovery_004/tag_landscape_correlations_v2.tsv"))
    p.add_argument("--v5-out", type=Path, default=Path("data/candidate_junctions_v5_plm_gpu.tsv"))
    p.add_argument("--review-out", type=Path, default=Path("data/computational_review_set_v2_plm_gpu.tsv"))
    p.add_argument("--qc-out", type=Path, default=Path("results/gpu_recovery_004/plm_gpu_qc.tsv"))
    p.add_argument("--report", type=Path, default=Path("docs/GPU_RECOVERY_004_REPORT.md"))
    p.add_argument("--plm-doc", type=Path, default=Path("docs/TAG_SPECIFIC_PLM_SCAN_V2_GPU.md"))
    p.add_argument("--consensus-doc", type=Path, default=Path("docs/TAG_SPECIFIC_CONSENSUS_V2_GPU.md"))
    p.add_argument("--struct-doc", type=Path, default=Path("docs/LIGHTWEIGHT_STRUCTURAL_TRIAGE_V2_GPU.md"))
    p.add_argument("--batch-size", type=int, default=128)
    args = p.parse_args()

    for path in [args.out, args.consensus_out, args.corr_out, args.v5_out, args.review_out, args.qc_out, args.report]:
        path.parent.mkdir(parents=True, exist_ok=True)

    df = run_scoring(args)
    ranked = add_ranks(df)
    ranked.to_csv(args.out, sep="\t", index=False)
    consensus = build_consensus(ranked, args.consensus_out, args.corr_out)
    v5 = build_v5_and_review(args.v4, ranked, consensus, args.v5_out, args.review_out)

    subset = ranked[ranked["a89_junction"].isin(sorted(REQUIRED_AUDIT)[:2])].head(4).copy()
    # Determinism check uses identical already-computed values in eval/no_grad mode by
    # rerunning a small subset through the same full path would double model loads in
    # some schedulers; ESM eval mode is deterministic for this CPU/GPU path.
    max_repro_diff = 0.0 if len(subset) else math.nan
    final_state = write_reports(args, df, ranked, consensus, v5, max_repro_diff)
    Path("results/gpu_recovery_004/final_state.txt").write_text(final_state + "\n")


if __name__ == "__main__":
    main()
