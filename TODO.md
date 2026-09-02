# TODO

Last updated: 2026-09-02

## Current Gate — Task 011A 9A5 Context QC / Hardening

Status: `AUTHORIZED / READY FOR CODEX`

Branch:

`analysis/9a5-context-qc-011a`

Primary task:

- `tasks/9A5_CONTEXT_QC_011A.md`

## P0 — Correct the 1x9A5 endpoint provenance

- verify why the packaged rep1/rep2/rep3 endpoint PDB files share the same SHA256;
- recover genuine independent endpoints from existing analysis outputs or trajectories;
- if needed, re-export final frames only;
- do not rerun MD;
- do not count duplicate coordinates as independent ensemble members.

## P0 — Recalculate affected 9A5-bound ensemble metrics

- rerun Task 011 structural-proxy calculations using verified unique structures;
- version provenance, inventory, hexamer metrics and ensemble summary;
- regenerate affected figures.

## P0 — Harden 248|249 x HA

- search all existing tagged-model assets first;
- test whether the severe rigid six-tagged-hexamer tag-protomer clash persists across independent HA conformations / existing ranks or minimal local relaxation;
- distinguish real crowding from rigid-placement artifact.

## P1 — Fix stale sequence-defined 9A5 field

- repair source-generation logic for `nineA5_epitope_context`;
- keep sequence epitope context separate from 3D 9A5 complex compatibility;
- regenerate the affected feature matrix as a new version.

## P1 — Candidate integration

Expected main output:

- `data/final_candidate_panel_v7_9a5_context_qc.tsv`

Explicitly reassess the ordering of:
- 289|290 x MAP8
- 289|290 x G196_minimal
- 248|249 x MAP8
- 248|249 x HA
- Priority B backups
- 224|225 controls
- 155|156 hard negative

## Stop boundary

No generic long MD, new blind docking, AF/ColabFold reruns, membrane/RNA/ATP expansion, safety/validation claims, or merge to `main`.

# Task 011A Follow-up
- ChatGPT/user review `docs/9A5_CONTEXT_QC_011A.md` and `data/final_candidate_panel_v7_9a5_context_qc.tsv`.
- Decide whether the V7 experimental-review order is sufficient for wet-lab discussion.
- Do not start nucleotide/codon design, new MD, docking, AF/ColabFold, or mechanistic membrane/RNA/ATP simulations until explicitly authorized.
