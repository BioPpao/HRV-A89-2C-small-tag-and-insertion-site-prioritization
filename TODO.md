# TODO

Last updated: 2026-08-21

Priority order is scientific, not cosmetic. Do not jump to tag modeling before the site layer is sufficiently reduced and methodologically hardened.

## P0 — CONSERVATION_001 completed, but V1 is provisional

The first conservation pass produced useful data and a complete 321-residue / 320-junction matrix, but it used an A89-guided Needleman–Wunsch fallback because MAFFT was not installed. It also exposed taxonomy/provenance and structural strict-flag issues.

Preserve all V1 outputs for provenance; do not treat them as final decision-grade evidence.

## P0 — CURRENT: CONSERVATION_002 decision-grade QC hardening

Execute `tasks/CONSERVATION_002.md`.

Required work:

- install MAFFT and required scientific packages in a reproducible user-space environment;
- reconcile the HRV-A type universe against current official ICTV taxonomy/VMR rather than using raw NCBI taxonomy labels as the sole type definition;
- build exact/high-confidence and full type-balanced 2C panels;
- rerun primary/expanded alignments with MAFFT high-accuracy mode;
- compare MAFFT V2 against the V1 custom NW alignment;
- perform exact-boundary vs provisional-boundary sensitivity analysis;
- refine natural-indel evidence so singleton/rare observations are not conflated with recurrent lineage-supported indels;
- regenerate the four-structure junction table and resolve all `strict_structural_pass` / gate-column mismatches;
- generate V2 residue, junction and integrated candidate tables;
- explicitly re-audit `223|224`, `245|246`, `248|249`, `250|251`, `256|257`, and `287|288` through `290|291`;
- produce `docs/CONSERVATION_SCREEN_V2.md` and `docs/CANDIDATE_JUNCTION_QC_V1.md`.

Do not start tag × site modeling automatically at the end. ChatGPT/user reviews V2 first.

## P1 — Candidate-junction shortlist

Only after CONSERVATION_002 is reviewed:

- reduce to a small number of junctions with stable structural + functional + evolutionary support;
- preserve literature-rescue conflicts rather than averaging them away;
- allow the valid result `NO_TARGETED_SITE` if high-quality QC still does not support a targeted site.

Planned deliverable:

- `docs/CANDIDATE_JUNCTION_PRIORITIZATION_V1.md`

## P1 — Tag × site modeling

Only after a small site set survives review:

- model MAP8;
- model HA;
- model G196 minimal and, if required by evidence, minimally flanked G196;
- retain AGIA as an alternate if leading systems conflict with local geometry;
- compare tagged vs WT local and global structure;
- inspect steric/interface/pore conflicts and tag exposure;
- treat tag flexibility/low confidence separately from native 2C perturbation.

Planned deliverables:

- `data/tag_site_perturbation_metrics_v1.tsv`
- `docs/TAG_SITE_MODELING_V1.md`
- selected lightweight structure snapshots if justified.

## P1 — Exact nucleotide/RNA audit

Blocked until the exact experimental nucleotide construct/context is supplied.

Do not infer the native nucleotide sequence by back-translation.

## Repository maintenance

- keep `PROJECT_STATE.md` current after every decision-changing phase;
- update `ANALYSIS_INDEX.md` whenever a new report supersedes an older version;
- append changes to `DECISIONS.md` rather than silently reversing them;
- store raw numerical outputs under `data/` or `results/`, not only inside prose reports;
- record source accession/DOI and evidence class for every new literature-derived constraint;
- record software/environment versions for decision-changing analyses;
- if appropriate software is absent, install it in user space rather than silently replacing it with a materially weaker method;
- do not commit software installations, package caches, bulk MD trajectories or restart files.
