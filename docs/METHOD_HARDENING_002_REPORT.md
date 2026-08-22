# METHOD_HARDENING_002_REPORT

Status: **CPU modules completed; PLM module blocked**

Date: 2026-08-22

Final state contribution: `METHOD_HARDENING_BLOCKED`

## Outputs

- `data/evA71_2C_substitution_tolerance_to_A89_v1.tsv`
- `results/method_hardening_002/substitution_mapping_qc.tsv`
- `data/pareto_junction_frontier_v1.tsv`
- `results/method_hardening_002/pareto_sensitivity.tsv`
- `data/hrvA_independent_indel_events_v1.tsv`
- `results/method_hardening_002/phylogeny_qc.tsv`
- `docs/PHYLOGENY_AWARE_INDEL_V1.md`
- `data/tag_specific_plm_scores_v1.tsv`
- `results/method_hardening_002/plm_qc.tsv`
- `docs/TAG_SPECIFIC_PLM_SCAN_V1.md`
- `data/candidate_junctions_v4_method_hardening.tsv`

## Module 1 — EV-A71 substitution tolerance

Completed.

QC:

| Metric | Value |
|---|---:|
| EV-A71 2C substitution rows | 6,580 |
| A89 junction rows | 320 |
| exact-aligned rows | 315 |
| ambiguous rows | 5 |
| rows with flank/window scores | 320 |

Substitution tolerance did not overturn direct insertion conflict. Several regions have less-negative substitution windows, but EV-A71 handle insertion remains unfavorable at every mapped junction.

## Module 2 — continuous/Pareto ranking

Completed for non-PLM evidence.

`strict_structural_pass` is retained as annotation only. Hard functional exclusions are marked separately rather than deleted from V4.

Pareto sensitivity:

| Subset | Pareto rows |
|---|---:|
| structure_only | 18 |
| structure_plus_direct | 37 |
| no_conservation | 81 |
| no_substitution | 67 |
| full | 103 |

Many Pareto-reviewable rows remain direct-homolog-conflicted or high-risk. Therefore Pareto membership is not enough to authorize modeling.

## Module 3 — phylogeny-aware independent indels

Completed with FastTree + Fitch-parsimony lower-bound event counts.

QC:

| Metric | Value |
|---|---:|
| tree tips | 77 |
| A89 junction rows | 320 |
| insertion tip-presence junctions | 1 |
| insertion parsimony-change junctions | 1 |
| local-deletion tip-presence junctions | 12 |
| local-deletion parsimony-change junctions | 12 |

Main effect: natural-indel support is sparse after tree-aware event counting. `248|249` remains the strongest conflict/control row with independent indel lower bound 2, but it still has unfavorable EV-A71 insertion phenotype.

## Module 4 — tag-specific PLM scan

Blocked.

Rows for all planned MAP8/HA/G196 forms were generated with blocked status, but no PLM scores were fabricated.

Reason:

- no visible NVIDIA GPU runtime;
- no existing `torch`, `transformers` or `esm`;
- installation of PLM dependencies was rejected by platform usage-limit escalation.

## Integrated V4

`data/candidate_junctions_v4_method_hardening.tsv` has 320 rows.

Class counts:

| Class | Count |
|---|---:|
| direct_homolog_strongly_unfavorable | 151 |
| hard_excluded | 61 |
| pareto_reviewable_direct_conflicted | 49 |
| weak_pareto_reviewable_direct_conflicted | 46 |
| conflict_control | 8 |
| mapping_uncertain | 5 |

## Answers to required questions

1. Outside old strict 10 became Pareto-reviewable: yes, but all remain direct-homolog-conflicted and many are high-risk.
2. Substitution tolerance materially changed interpretation: no strong promotion; it adds context but does not overcome insertion conflict.
3. Phylogeny-aware indels changed V2 natural-indel interpretation: yes, support becomes sparse and mostly conflict-bearing.
4. MAP8/HA/G196 landscapes differ: cannot assess; PLM blocked.
5. `287|288-290|291` modeling value: only as conflict controls, not supported targeted sites.
6. `248|249` / `256|257`: retained as historical-conflict controls; `248|249` also has sparse independent-indel support.
7. Enough evidence to authorize reduced insertion-specific modeling: not from this run, because PLM is blocked and direct insertion evidence is globally unfavorable.
8. If not, project state should remain blocked/no-high-confidence until PLM or empirical A89 data resolves the gap.

## Decision

`METHOD_HARDENING_BLOCKED`
