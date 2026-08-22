# RANKING_ROBUSTNESS_AUDIT_V1

Status: **completed for non-PLM evidence layers**

Date: 2026-08-22

## Inputs

- `data/candidate_junctions_v4_method_hardening.tsv`
- `data/pareto_junction_frontier_v1.tsv`

## Sensitivity settings

Pareto/non-dominated membership was recalculated under five transparent metric subsets:

| Subset | Pareto rows |
|---|---:|
| structure_only | 18 |
| structure_plus_direct | 37 |
| no_conservation | 81 |
| no_substitution | 67 |
| full | 103 |

Metrics used are documented in `results/method_hardening_002/pareto_sensitivity.tsv`.

## Negative-control audit

Output:

- `results/one_shot_003/negative_control_audit.tsv`

Summary:

| Audit flag | Count |
|---|---:|
| not promoted or retained only as conflict control | 126 |
| pareto-flagged despite high-risk context, review required | 39 |

The framework can flag high-risk regions as Pareto-reviewable when continuous structural/substitution variables are favorable. This is expected behavior for a sensitivity audit, not promotion. Functional tier and direct homolog insertion conflict remain explicit columns in V4.

## Interpretation

The candidate landscape is not robust enough for direct targeted-site selection. Pareto membership changes substantially across metric subsets, and many Pareto-reviewable rows remain high-risk or direct-homolog-conflicted.

This supports a blocker/further-review state rather than automatic Tag x Site modeling.
