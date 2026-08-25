# Current Computational Results Report V1

Date: **2026-08-25**

Branch: **`analysis/experimental-review-cleanup-010a`**

Project state at report freeze: **`EXPERIMENTAL_REVIEW_SHORTLIST_READY_FOR_DISCUSSION`**

## Purpose

This folder archives the current integrated computational-results report for the HRV-A89 2C internal small-tag insertion-site prioritization project.

The report is intended to preserve the complete scientific narrative from the 320-junction global search through tag selection, structural/evolutionary evidence, broad replicated MD, Task 009 posthoc audit, corrected CHARMM36 validation, Task 010A statistical-semantics cleanup, and the final experimental-review shortlist.

The computational endpoint is **candidate prioritization for experimental discussion**, not proof that any insertion site or tagged construct is safe, functionally neutral, or biologically validated.

## Files

| File | Purpose |
|---|---|
| `HRV_A89_2C_small_tag_computational_results_report.html` | self-contained interactive HTML report; CSS, JavaScript, SVG figures and report data are embedded in one file |
| `ANALYSIS_SYNTHESIS_V1.md` | report-level scientific synthesis and interpretation framework |
| `TAG_SELECTION_RATIONALE_V1.md` | detailed rationale for MAP8/HA/G196 and alternatives; includes a dedicated explanation of why 6×His was not prioritized |
| `REPORT_PROVENANCE_V1.md` | source files, branch state, raw-data boundary, visual-design reference and reproducibility notes |

## Current experimental-review shortlist represented in the report

### Candidate hypotheses

1. `289|290 × MAP8`
2. `289|290 × G196_minimal`
3. `248|249 × HA`
4. `248|249 × MAP8`

### Controls

5. `224|225 × MAP8` — conflict control / MD caution
6. `155|156 × MAP8` — hard-negative control

The four candidate constructs are a **partially crossed two-site tag-comparison design**, not a full factorial experiment:

| Site | Shared comparator | Site-specific alternative |
|---|---|---|
| `289|290` | MAP8 | G196_minimal |
| `248|249` | MAP8 | HA |

MAP8 therefore provides the cross-site bridge, while G196 and HA provide within-site tag-identity comparisons.

## Important evidence boundary

Priority A/B in this project is **`multi_evidence_expert_adjudication`**. There is no validated algorithmic total score. Comparative MD is a downstream perturbation layer and does not override higher-weight evidence such as direct homolog insertion fitness, functional constraints or the absence of direct HRV-A89 phenotype data.

The report deliberately preserves conflicting evidence. For example, the current Priority A constructs still carry unfavorable direct EV-A71 homolog insertion priors.

## Offline / portability requirement

The HTML is designed as a single self-contained file:

- no CDN;
- no remote JavaScript;
- no external fonts;
- no required external images;
- interactive SVG/JavaScript embedded directly in the document;
- local browser notes use `localStorage` only.

The file can therefore be copied and opened directly on another computer, tablet or phone without the repository being present.

## Authoritative upstream sources

The report is a presentation/synthesis layer. Scientific authority remains with the versioned project files, especially:

- `PROJECT_STATE.md`
- `DECISIONS.md`
- `ANALYSIS_INDEX.md`
- `docs/2C_FUNCTIONAL_CONSTRAINT_MAP_V2.md`
- `docs/STRUCTURAL_SCREEN_V2.md`
- `docs/CONSERVATION_SCREEN_V2.md`
- `docs/TAG_CANDIDATE_SCREEN_V1.md`
- `docs/DYNAMICS_009_POSTHOC_AUDIT_V1.md`
- `docs/CORRECTED_PROTOCOL_VALIDATION_V1.md`
- `docs/FINAL_SCIENTIFIC_CLEANUP_010A.md`
- `data/final_candidate_panel_v5_experimental_review_cleanup.tsv`
- `data/experimental_review_shortlist_v1.tsv`

## Raw-data note

Large raw GROMACS trajectories and binary run products are intentionally not duplicated into ordinary Git. The report summarizes their QC and derived results, but raw `XTC/TPR/EDR/CPT/GRO` files remain server-side data and require separate archival management.
