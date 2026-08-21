# Candidate-junction QC gate V1

Status: **ready for ChatGPT/user review after CONSERVATION_002**.

Decision state: `READY_FOR_SHORTLIST`

## Bottom Line

CONSERVATION_002 hardens the site layer with ICTV VMR reconciliation, MAFFT L-INS-i alignments, type-aware indel categories, exact-boundary sensitivity and regenerated structural metrics.

No site is called low-risk. The next allowed action is only a ChatGPT/user decision on the reduced set; tag x site modeling is still not started.

## Decision-Grade Inputs

- `data/junction_structural_metrics_v2.tsv`
- `data/hrvA_conservation_per_residue_v2.tsv`
- `data/hrvA_conservation_per_junction_v2.tsv`
- `data/candidate_junctions_v2.tsv`
- `results/structural_v1_v2_gate_audit.tsv`
- `results/conservation_002_focal_junction_audit.tsv`
- `docs/CONSERVATION_SCREEN_V2.md`

## Recommended Review Set

Primary strict-pass review cluster:

- `287|288`
- `288|289`
- `289|290`
- `290|291`

Why: these remain strict structural passes after V2 regeneration and retain V2 HRV-A evolutionary support.

Main caveat: all remain HIGH_RISK because they sit in the Zn/Cys-rich-to-C-terminal transition context. `287|288` has conserved flanking residues despite a variable local window.

Literature-rescue controls/conflicts:

- `248|249`
- `256|257`

Why: historical poliovirus insertion-tolerance evidence remains preserved. `248|249` has broader-lineage indel support in V2; `256|257` is variable. Neither is promoted because structural/functional context remains unfavorable.

Optional outside-strict review controls:

- `223|224`
- `245|246`
- `250|251`

Why: these are not strict-pass sites but are useful contrast cases if ChatGPT wants to test how much weight to give near-miss/evolutionary evidence.

## Stable Exclusions / Down-Ranks

- `155|156`: hard 9A5/aromatic-pore-warning exclusion plus conserved context.
- `174|175`: conserved Walker-B-adjacent context.
- `216|217`: motif-C N216 contact dominates.
- `175|176`, `217|218`, `218|219`: unresolved, not rescued.

## Unresolved Issues

- Exact-boundary subset is only 5 sequences; it is sensitivity evidence, not a replacement panel.
- ICTV VMR types `A106`, `A107`, `A108` lack accepted 2C sequence in this run.
- The project still lacks exact experimental replicon nucleotide context.
- Conservation supports review, not biological tolerance of an artificial tag.

## Required Next Decision

Choose one:

1. approve a narrow modeling shortlist: `287|288`, `288|289`, `289|290`, `290|291`, plus `248|249` and `256|257` as rescue/conflict controls;
2. approve a broader comparison set by adding `223|224`, `245|246`, `250|251`;
3. decide `NO_TARGETED_SITE` and pivot to insertion-library/minimal-epitope strategy.
