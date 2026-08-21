# Project workflow: ChatGPT ↔ Codex ↔ GitHub

## Purpose

This repository is the shared source of truth for the HRV-A89 2C small-tag × internal insertion-junction project.

The collaboration model is:

- **ChatGPT**: scientific reasoning, evidence review, project-level decisions, and definition of the next analysis gate.
- **Codex on the server**: execution, scripting, data acquisition/QC, computation, reproducibility, reporting, and Git operations.
- **GitHub repository**: persistent shared project state between ChatGPT and Codex.

Do not rely on chat history as the authoritative state. Any information that can affect a later scientific decision must be recorded in the repository.

## Source-of-truth rule

Important results must not exist only in:

- Codex conversation history;
- terminal output;
- temporary files;
- local notebooks;
- uncommitted working-tree changes.

Decision-relevant information belongs in versioned repository files: scripts, machine-readable tables, reports, logs, provenance records, and project-state documents.

## Required read order for every new task

1. `WORKFLOW.md`
2. `AGENTS.md`
3. `PROJECT_STATE.md`
4. `DECISIONS.md`
5. `ANALYSIS_INDEX.md`
6. `ACTIVE_TASK.md`
7. the task file referenced by `ACTIVE_TASK.md`
8. current topic-specific reports referenced by `ANALYSIS_INDEX.md`
9. `INPUT_PROVENANCE.md`
10. `references/LITERATURE_EVIDENCE_REGISTRY.md`
11. `TODO.md`

Never infer current project state from an older report when a newer report is listed as authoritative.

## Scientific responsibility boundary

Codex executes the requested analysis but does not silently change project-level scientific assumptions.

If new evidence conflicts with an existing decision:

1. preserve the conflicting result;
2. document it explicitly;
3. do not erase or average away the conflict;
4. update `DECISIONS.md` only when the task explicitly authorizes a project-level decision change or when a new decision is required and clearly justified;
5. leave the final interpretation for repository review by ChatGPT/user.

The computational endpoint is candidate prioritization, not proof of a biologically safe insertion site.

## Branch and Git rules

- Do not develop directly on `main` unless explicitly instructed.
- Use the branch specified in `ACTIVE_TASK.md`.
- Before work: `git fetch origin`, inspect branch/status, and confirm the working tree.
- Never use `git reset --hard` or destructive cleanup on user work.
- Stage only explicit task files with `git add -- <paths>`.
- Do not use `git add .`, `git add -A`, or `git add --all`.
- Commit at meaningful scientific checkpoints rather than only at the end.
- Push each checkpoint so ChatGPT can inspect the repository while work is in progress.
- Do not force-push unless explicitly authorized.
- Do not merge the task branch into `main`; merge happens only after review.

## Checkpoint protocol

Every active task should maintain a run log under `docs/` or another task-defined path. The log should record:

- task ID;
- branch;
- starting commit;
- current phase/status;
- software/environment versions;
- data sources and retrieval dates;
- QC statistics;
- commands or reproducible entry points;
- generated files;
- failed attempts and fallbacks;
- warnings/limitations;
- checkpoint commit SHA and push status;
- next executable action.

Checkpoint commits should normally correspond to:

1. workflow/environment/source framework;
2. primary data acquisition and QC;
3. core computation and validation;
4. evidence integration and scientific report.

## Reproducibility

- Final numerical results must be reproducible from scripts.
- Keep machine-readable TSV/CSV outputs in addition to prose summaries.
- Record accessions, database sources, versions, filters, dates, and random seeds where relevant.
- Scripts should expose important inputs/thresholds as command-line arguments or clearly named constants.
- Programs should fail loudly on residue-number, sequence, row-count, or join-key mismatches.
- Do not fabricate unavailable accessions, structures, sequence records, literature claims, or numerical results.

## Repository maintenance after a decision-changing phase

When a phase changes the scientific state, update as appropriate:

- `PROJECT_STATE.md`
- `ANALYSIS_INDEX.md`
- `TODO.md`
- `README.md`
- `AGENTS.md`
- `DECISIONS.md` only for true project-level decisions
- evidence/provenance registries when new external sources are introduced

Do not mark downstream phases complete prematurely.

## Storage policy

Commit lightweight, decision-relevant artifacts such as:

- scripts;
- normalized FASTA files needed for reproducibility;
- metadata tables;
- alignments;
- small figures;
- result tables;
- reports;
- logs.

Do not commit bulk trajectories, caches, large raw database dumps, restart/state files, or unrelated temporary outputs.

## Handoff protocol

When the user says “检查仓库” or equivalent, the repository should contain enough information for ChatGPT to determine:

- what was attempted;
- what succeeded or failed;
- what data were used;
- what changed scientifically;
- the latest checkpoint commit;
- what decision is required next.

The repository, not the AI chat transcript, is the project memory.
