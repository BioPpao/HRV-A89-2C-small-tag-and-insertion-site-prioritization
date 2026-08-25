# AGENTS.md

Instructions for Codex/ChatGPT/other analysis agents working in this repository.

## Repository-as-memory rule

This repository is the persistent shared project memory between ChatGPT and server-side Codex.

- ChatGPT is responsible for scientific reasoning, evidence review and defining the next decision gate.
- Codex is responsible for execution, scripting, data/QC, reproducible computation, software/environment setup, reporting and checkpoint Git updates.
- Decision-relevant information must be committed to the repository rather than left only in chat, terminal output or temporary files.
- Follow the full collaboration and checkpoint rules in `WORKFLOW.md`.

## Read order before making changes

1. `WORKFLOW.md`
2. `AGENTS.md`
3. `PROJECT_STATE.md`
4. `DECISIONS.md`
5. `ANALYSIS_INDEX.md`
6. `ACTIVE_TASK.md`
7. the task specification referenced by `ACTIVE_TASK.md`
8. the current topic-specific report linked by the index
9. `INPUT_PROVENANCE.md`
10. `references/LITERATURE_EVIDENCE_REGISTRY.md`
11. `TODO.md`

Do not infer the current state from an old `V1` report if a newer version is listed as authoritative.

## Method-quality rule

For a decision-changing analysis, do not silently substitute a materially weaker method just because the preferred software is missing.

- Install the appropriate mature tool in user space when feasible.
- Prefer reproducible Conda/Mamba/Micromamba/Miniforge environments; do not use `sudo` unless the user explicitly authorizes it.
- Record tool versions, install source/channels and environment specification.
- A custom or weaker fallback may be retained for sensitivity comparison, but it must not be promoted to the primary result when the preferred method can reasonably be installed.
- If the required method cannot be installed after reasonable attempts, record the blocker, push the current state and mark the task `BLOCKED` or result `PROVISIONAL` rather than claiming decision-grade completion.

## Scientific rules

- This is an **HRV-A89 2C small-tag × internal insertion-junction** project, not an HA-only project.
- FLAG is excluded from the tag set.
- Never call a computational site `safe`.
- Do not copy homolog residue numbers directly to A89. Preserve the alignment/mapping used.
- Distinguish direct A89 evidence, homolog evidence, database `By similarity` annotations, preprints and project-model evidence.
- Do not convert a favorable monomer loop into a recommendation without hexamer/interface context.
- Treat the current A89 hexamers as template-guided no-membrane/no-RNA hypotheses.
- Pore/radial metrics from the project hexamers are penalties/proxies, not proof of an RNA path.
- Preserve contradictory evidence. Direct literature rescue observations must remain visible even when structural metrics are unfavorable.
- Conservation is supporting evidence, not a standalone safety score.
- Tagged AlphaFold/structure prediction is perturbation modeling, not biological validation.
- Final RNA-level design requires the exact experimental replicon nucleotide sequence.

## Evidence hierarchy

Default hierarchy:

`direct 2C genetics/biochemistry > experimental homolog structures > explicit A89 sequence mapping / A89 annotations > A89 monomer ensemble > A89 hexamer ensemble > near-HRV conservation > tag-specific modeling`

For Task 010, corrected replicated MD remains a downstream supporting layer. It must not override direct phenotype or hard biological constraints.

## Current structural ensemble

- `fold_hrv_2c_full_model_3.cif`: lead-source AF monomer.
- `fold_hrv_2c_full_model_1.cif`: control-source AF monomer.
- `selected_hexamer_01_md_representative.pdb`: lead hexamer.
- `selected_hexamer_02_md_representative.pdb`: companion/control hexamer.

All use A89 2C numbering 1–321 and were integrity-audited. Checksums are in `INPUT_PROVENANCE.md`.

## Current quantitative analysis conventions

- Site unit: peptide junction `i|i+1`.
- Evaluate both flanking residues and a local window.
- Aggregate structural metrics across both AF monomers and all six protomers in both hexamers whenever applicable.
- Keep raw numerical outputs in TSV/CSV in addition to Markdown summaries.
- Do not hide evidence conflicts behind a single composite score.
- If a score is introduced later, retain its component columns and document the equation/weights.

## File/version rules

- New decision-changing reports use explicit versions: `*_V1.md`, `*_V2.md`, etc.
- When superseding a report, update `ANALYSIS_INDEX.md`; do not delete old scientific provenance without a reason.
- Update `PROJECT_STATE.md` after any phase that changes the scientific interpretation.
- Update `DECISIONS.md` when a project-level assumption is changed.
- Add literature sources/claim boundaries to `references/LITERATURE_EVIDENCE_REGISTRY.md`.
- Use `ACTIVE_TASK.md` as the single pointer to the currently authorized execution task.
- Keep reusable collaboration rules in `WORKFLOW.md`, not in transient chat prompts.

## Reproducibility rules

- Scripts must have deterministic inputs where possible and document dependencies.
- Do not overwrite user-supplied structure inputs.
- Record accessions, versions, dates and sequence filters for conservation datasets.
- Record random seeds for any stochastic modeling.
- Keep bulk trajectories/restart/state data out of normal Git.
- Do not fabricate unavailable PDB/EMDB/accession identifiers.
- Push meaningful task checkpoints so the repository remains inspectable from ChatGPT without relying on Codex conversation state.

## Task 010 dynamics-specific rules

During `DYNAMICS_ANALYSIS_AUDIT_AND_CANDIDATE_RERANK_010`:

- preserve all Task 009 trajectories and outputs;
- do not overwrite historical 009 analysis tables;
- repair periodic-boundary-condition handling before geometry-dependent analysis;
- cross-check representative RMSD with GROMACS-native analysis;
- distinguish self-drift from deviation from a common WT reference;
- use junction-matched WT local RMSF baselines;
- calculate WT-defined contact retention separately from candidate-start contact persistence;
- use true tag SASA in addition to nonlocal contact metrics;
- do not treat frames as independent statistical replicates;
- use replica/time-block/time-truncation robustness;
- dynamic-network evidence is exploratory unless stable across replicas and windows;
- audit/correct CHARMM36 nonbonded settings before any new production extension;
- do not automatically extend all legacy trajectories to 50 ns;
- select a reduced, biologically diverse corrected-protocol validation subset;
- prefer more replicas when between-replica variance dominates and longer trajectories when all replicas show shared slow drift;
- do not count adjacent C-terminal junctions as independent biological regions;
- do not create a new opaque weighted score to force a ranking.

## Current next task

Read `ACTIVE_TASK.md`.

The current completed task is:

`FINAL_SCIENTIFIC_CLEANUP_AND_EXPERIMENTAL_SHORTLIST_010A`

on branch:

`analysis/experimental-review-cleanup-010a`.

Primary files:

- `tasks/FINAL_SCIENTIFIC_CLEANUP_AND_EXPERIMENTAL_SHORTLIST_010A.md`
- `docs/FINAL_SCIENTIFIC_CLEANUP_010A.md`
- `docs/EXPERIMENTAL_REVIEW_SHORTLIST_V1.md`
- `codex/TASK_010A_CLEANUP_PROMPT.md`

Task 010A completed the analysis-only cleanup and froze the 4-candidate + 2-control experimental-review shortlist. It does not authorize exact nucleotide design, wet-lab procedural protocols, new Slurm/GPU/MD jobs, broad membrane/RNA/ATP/antibody mechanism simulations, safety/validation claims, or automatic merge to `main`.
