# COMPUTATIONAL_REVIEW_SET_V1

Status: **computational review set constructed; not an experimental recommendation**

Date: 2026-08-22

## Purpose

Create a compact set of junctions for ChatGPT/user review after CPU method hardening, while preserving conflicts and blocked PLM status.

## Output

- `data/computational_review_set_v1.tsv`

Rows: 17.

## Included evidence classes

- least-deleterious EV-A71 handle-insertion outside-strict controls: `203|204`, `224|225`;
- old strict C-terminal conflict controls: `287|288`, `288|289`, `289|290`, `290|291`;
- historical/indel conflict controls: `248|249`, `256|257`;
- near-miss or mapping-uncertain controls: `223|224`, `245|246`, `250|251`;
- negative-control hard exclusions: `155|156`, `216|217`;
- Pareto-reviewable direct-conflicted rows near `249|250`, `251|252`, plus representative high-risk Pareto rows.

## Boundary

Because PLM scoring is blocked and EV-A71 direct insertion phenotype is unfavorable across all mapped junctions, this is not a ready modeling shortlist. It is a review set for deciding whether additional computation is worth authorizing.
