# AGENTS.md

Instructions for Codex/ChatGPT/other analysis agents working in this repository.

## Repository-as-memory rule

This repository is the persistent shared project memory between ChatGPT and server-side Codex.

- ChatGPT is responsible for scientific reasoning, evidence review and defining the next decision gate.
- Codex is responsible for execution, scripting, data/QC, reproducible computation, reporting and checkpoint Git updates.
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

This hierarchy is not an instruction to ignore lower layers; it is an instruction about how to resolve conflicts and how strongly to word conclusions.

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

## Current next task

Read `ACTIVE_TASK.md` for the executable task. The near-HRV conservation and indel-tolerance layer is complete in `docs/CONSERVATION_SCREEN_V1.md`. The next project decision is the reduced candidate-junction set for tag × site modeling, or whether to pivot to an experimental insertion-library/minimal-epitope strategy. Do not start tag modeling, long MD, RNA/codon design, or construct recommendations unless a later task specification explicitly authorizes it.
