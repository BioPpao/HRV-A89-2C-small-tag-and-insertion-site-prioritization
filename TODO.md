# TODO

Last updated: 2026-08-21

Priority order is scientific, not cosmetic. Do not jump to tag modeling before the site layer is sufficiently reduced.

## P0 — Completed decisive analysis

### 1. Build HRV-A-focused 2C conservation dataset — COMPLETE

Completed in `docs/CONSERVATION_SCREEN_V1.md`.

Deliverables:

- `data/hrvA_2C_sequences.fasta`
- `data/hrvA_2C_sequence_metadata.tsv`
- `data/hrvA_2C_alignment.fasta`
- `data/hrvA_conservation_per_residue.tsv`
- `data/hrvA_conservation_per_junction.tsv`
- `docs/CONSERVATION_SCREEN_V1.md`

### 2. Add broader rhinovirus context without pooling it into one entropy score — COMPLETE / SPARSE

Completed as secondary context in `data/hrvABC_candidate_window_context.tsv`. HRV-B/C retained sequence counts are sparse after applying the same extraction/QC rules, so this context is weak.

Deliverables:

- `data/hrvABC_candidate_window_context.tsv`
- `docs/CONSERVATION_SCREEN_V1.md`

### 3. Integrate functional + structural + conservation evidence — COMPLETE

Produce a transparent candidate table with separate columns for:

- functional tier;
- direct literature insertion-tolerance/rescue evidence;
- AF secondary-structure consistency;
- AF rSASA;
- hexamer rSASA;
- DeltaSASA/burial;
- inter-protomer distance/contact metrics;
- pore/radial proxy;
- HRV-A conservation;
- HRV-A local gap/indel frequency;
- unresolved evidence conflicts.

Do **not** hide these components behind one opaque score.

Deliverables:

- `data/candidate_junctions_v1.tsv`
- `docs/CONSERVATION_SCREEN_V1.md`

## P0 — Next decision

ChatGPT/user should decide the reduced candidate-junction set before tag × site modeling:

- narrow set: `287|288`, `288|289`, `289|290`, `290|291`, with `248|249` and `256|257` retained as literature-rescue controls;
- broader review set: add selected near-misses such as `223|224`, `245|246`, `250|251`;
- alternative path: pivot to insertion-library/minimal-epitope strategy if no targeted site is convincing.

## P1 — Tag × site modeling

Only after a small site set survives P0:

- model MAP8;
- model HA;
- model G196 minimal and, if required by evidence, minimally flanked G196;
- retain AGIA as an alternate if leading systems conflict with local geometry;
- compare tagged vs WT local and global structure;
- inspect steric/interface/pore conflicts and tag exposure;
- treat tag flexibility/low confidence separately from native 2C perturbation.

Deliverables:

- `data/tag_site_perturbation_metrics_v1.tsv`
- `docs/TAG_SITE_MODELING_V1.md`
- selected lightweight structure snapshots if justified.

## P1 — Exact replicon nucleotide/RNA audit

Blocked until the exact experimental nucleotide construct is supplied.

Required:

- actual HRV-A89 2C nucleotide sequence from the replicon/plasmid;
- boundaries around 2B|2C and 2C|3A;
- intended codons for each tag construct.

Then evaluate:

- reading frame / polyprotein continuity;
- local RNA secondary-structure perturbation;
- broader plausible cis/long-range effects;
- accidental creation of problematic cleavage-like sequence contexts;
- codon-level design differences among synonymous tag encodings.

## P2 — Experimental construct set

Target outcome:

- 1 primary construct;
- 1 structurally/evolutionarily distinct backup site;
- 1 minimal-footprint or assay-system backup;
- WT replicon control;
- appropriate replication-defective/processing controls as required by the assay.

Do not enter 9A5 mechanism interpretation until tagged 2C shows sufficiently WT-like baseline behavior.

## Repository maintenance

- keep `PROJECT_STATE.md` current after every decision-changing phase;
- update `ANALYSIS_INDEX.md` whenever a new report supersedes an older version;
- append changes to `DECISIONS.md` rather than silently reversing them;
- store raw numerical outputs under `data/` or `results/`, not only inside prose reports;
- record source accession/DOI and evidence class for every new literature-derived constraint;
- do not commit bulk MD trajectories/restart files.
