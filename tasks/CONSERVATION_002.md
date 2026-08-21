# CONSERVATION_002 — decision-grade conservation/QC hardening

## Goal

Upgrade `CONSERVATION_001` from a provisional conservation result to a decision-grade analysis before any tag × site modeling.

This task exists because the first run used a reference-guided Needleman–Wunsch fallback when MAFFT was absent, mixed exact and provisional 2C extractions, used an NCBI taxonomy-derived type universe that needs reconciliation with current ICTV type definitions, and exposed eight structural strict-flag/gate mismatches.

Do not start tag modeling in this task.

## Mandatory software policy

Decision-changing analyses must use an appropriate mature method. Missing software is not permission to silently downgrade the method.

For this task:

1. inspect existing user-space Conda/Mamba/Micromamba/Miniforge installations;
2. if available, create a dedicated environment such as `hrv2c-conservation-qc`;
3. if no suitable environment manager exists, install a user-space manager (prefer Micromamba or Miniforge) under the user's home/project tools area; do not use `sudo`;
4. install at minimum a modern Python, MAFFT, Biopython, pandas, numpy, and MDTraj (for structural-table regeneration); add only genuinely required packages;
5. record exact versions, channels, install commands and environment export/lock information under `results/` and/or `envs/`;
6. if installation fails, diagnose and retry appropriately. Do not replace MAFFT with a weaker custom alignment and call the task complete. If the required method cannot be installed, mark the task `BLOCKED` and push the blocker report.

A fallback may be used only as a documented sensitivity comparison, never as the primary decision-grade result when the preferred method can reasonably be installed.

## Existing V1 status

Treat these as provisional inputs, not deleted history:

- `docs/CONSERVATION_SCREEN_V1.md`
- `data/hrvA_conservation_per_residue.tsv`
- `data/hrvA_conservation_per_junction.tsv`
- `data/candidate_junctions_v1.tsv`
- current reference-guided alignments

Preserve V1 for provenance. Write V2 outputs separately.

## Work package 1 — environment and reproducibility

Create/update:

- `docs/CONSERVATION_002_RUN_LOG.md`
- `results/conservation_002_environment.tsv`
- an environment specification/export under `envs/` if practical

Record Python, MAFFT, Biopython, pandas, numpy and MDTraj versions.

Primary protein MSA method for the HRV-A panel: MAFFT L-INS-i equivalent (`--localpair --maxiterate 1000`) unless a documented technical reason justifies another high-accuracy MAFFT mode. With the current ~80–120 proteins of ~321 aa, prioritize alignment quality over speed.

## Work package 2 — rebuild the HRV-A type universe

Use the current official ICTV taxonomy/VMR as the authoritative recognized-type universe for Rhinovirus A.

Do not simply equate every NCBI taxonomy subtree label with an ICTV-recognized type.

Create:

- `data/hrvA_type_universe_ictv.tsv`
- a reconciliation table between ICTV type names, NCBI taxonomy labels and retained sequence labels

Explicitly resolve naming cases such as A1/A1A/A1B and any high-number labels that are present in one source but not equivalent to current ICTV recognized types.

Report:

- number of ICTV-recognized HRV-A types at retrieval time;
- represented types;
- missing types;
- ambiguous mappings;
- reason for each unresolved/missing type.

Do not invent mappings.

## Work package 3 — improve 2C sequence provenance

Build at least two analysis panels.

### Panel A — high-confidence/exact-boundary subset

Prefer mature `Protein 2C` annotations or explicit authoritative mature-product coordinates from UniProt/NCBI. Retrieve additional NCBI Protein/RefSeq records if this materially increases exact-boundary coverage.

### Panel B — full type-balanced panel

One representative per reconciled ICTV HRV-A type where feasible. Provisional extraction may be retained only when no better record is available and when extraction passes stringent QC.

For provisional records preserve:

- extraction method;
- reference coverage;
- sequence identity;
- inferred start/end;
- source accession;
- confidence flag.

Do not silently treat provisional extraction as equivalent to exact annotation.

Create V2 metadata/FASTA outputs rather than overwriting V1.

## Work package 4 — MAFFT realignment

Realign both the primary type-balanced panel and expanded panel with MAFFT.

Use the authoritative repository A89 321-aa sequence as the coordinate anchor after alignment, but do not force pairwise alignment independently for every sequence.

Create V2 alignments and A89 column-mapping tables.

QC core motifs/features after alignment:

- Walker A aa124–131;
- 9A5 epitope aa148–160;
- Walker B aa165–170;
- A197/L199/K202 RNA-related mapped positions;
- motif C aa210–216;
- R233/R234;
- C262/C273/C278;
- aa305–321 C-terminal region.

If core motifs show suspicious shifts, investigate boundary/taxonomy/sequence quality before accepting the alignment.

## Work package 5 — V1 vs V2 alignment sensitivity

Quantify how MAFFT changes the V1 conclusions.

At minimum compare:

- A89 residue mapping;
- per-residue identity/entropy;
- gap frequencies;
- natural insertion positions and counts;
- candidate-junction local-window metrics.

Create a machine-readable V1-vs-V2 comparison table.

The key question is whether candidate interpretation changes because of the better MSA.

## Work package 6 — exact-boundary sensitivity analysis

Calculate conservation using both:

- full reconciled type-balanced panel;
- exact/high-confidence boundary subset.

Do not require the smaller exact subset to replace the full panel. Use it as a sensitivity layer.

For each focal junction report whether the evolutionary interpretation is:

- stable across both panels;
- weakened in the exact-only subset;
- strengthened in the exact-only subset;
- unresolved because exact subset N is too small.

## Work package 7 — refine indel evidence

Retain raw counts and frequencies. Replace the overly broad binary `indel_signal` interpretation with transparent categories.

At minimum distinguish:

- `none`;
- `singleton_or_rare` — isolated sequence/type observations;
- `recurrent_across_types` — same junction/slot supported by at least two distinct HRV-A types;
- `broader_lineage_supported` — repeated across multiple independent types with alignment/provenance review.

The category rules must be documented and raw type counts retained. Do not promote a junction because of a single possible alignment artifact.

## Work package 8 — regenerate the structural strict-pass table

The V1 integrated table reported eight rows where rounded/recorded gate columns appear to pass while `strict_structural_pass=False`.

Re-run `scripts/analyze_insertion_junctions.py` from the original four audited structures in an environment with the required mature dependencies.

Write:

- `data/junction_structural_metrics_v2.tsv`
- `results/structural_v1_v2_gate_audit.tsv`

Do not overwrite V1.

Determine the exact cause of every mismatch:

- full-precision threshold crossing vs rounded display;
- old script/table inconsistency;
- data-version mismatch;
- other reproducible cause.

The strict-pass definition must be internally consistent in V2.

## Work package 9 — rebuild conservation and integrated tables

Generate V2 equivalents:

- `data/hrvA_conservation_per_residue_v2.tsv`
- `data/hrvA_conservation_per_junction_v2.tsv`
- `data/candidate_junctions_v2.tsv`

Keep all 321 residues and all 320 internal junctions.

Do not collapse evidence into an opaque composite score.

## Focal junctions requiring explicit audit

At minimum inspect:

- `155|156`
- `174|175`, `175|176`
- `216|217`, `217|218`, `218|219`
- `223|224`
- `245|246`
- `248|249`
- `250|251`
- `256|257`
- `287|288`
- `288|289`
- `289|290`
- `290|291`

For `287–291`, do not describe the entire region as simply "variable". Report both local-window conservation and the conservation of the two residues flanking each specific junction. In particular, distinguish a variable window from highly conserved flanking residues.

## Required V2 report

Create `docs/CONSERVATION_SCREEN_V2.md` containing:

1. why V1 was provisional;
2. software/environment installation and versions;
3. ICTV type-universe reconciliation;
4. exact vs provisional sequence provenance;
5. MAFFT method and QC;
6. V1-vs-V2 sensitivity;
7. exact-boundary sensitivity;
8. refined indel evidence;
9. structural strict-flag mismatch resolution;
10. revised integrated evidence;
11. which junction interpretations are stable vs changed;
12. whether evidence is now strong enough to authorize a reduced site shortlist.

Also create a concise `docs/CANDIDATE_JUNCTION_QC_V1.md` focused on the final decision gate.

## Decision rule

The task may conclude one of three states:

- `READY_FOR_SHORTLIST`: decision-grade QC reproduces a small stable set worth modeling;
- `NOT_READY`: substantial methodological uncertainty remains;
- `NO_TARGETED_SITE`: high-quality analysis still yields no convincing targeted site.

Do not start MAP8/HA/G196 modeling automatically even if `READY_FOR_SHORTLIST`; ChatGPT/user must review the V2 evidence first.

## Git/checkpoint protocol

Work only on `analysis/conservation-002`.

Checkpoint and push after:

1. environment + MAFFT installation + taxonomy framework;
2. rebuilt panels + MAFFT alignments;
3. conservation/indel/structural V2 calculations;
4. integrated V2 report and project-state updates.

Every decision-relevant result, blocker, fallback, software version and failed attempt must be committed/pushed.

Do not merge `main`.
