# DIRECT_INDEL_001

Status: **READY TO EXECUTE**

## Scientific question

Does direct experimental insertion/deletion fitness from an enterovirus 2C homolog support, contradict, or expand the current HRV-A89 insertion-junction shortlist?

## Why this task comes before Tag × Site modeling

The current shortlist is based mainly on WT A89 structural geometry, functional constraints and near-HRV evolutionary context. These are useful proxies but do not directly measure insertion tolerance.

A published EV-A71 proteome-scale deep insertion/deletion scan includes 2C and provides direct viral-fitness measurements after insertion/deletion perturbation. This evidence has higher information value than another round of WT-only structural filtering and may reveal candidates outside the current strict-pass set.

## Execution requirements

### 1. Source verification and provenance

Locate and verify the primary publication, processed-data repository, code repository and any raw-read accession.

Record:

- DOI / publication citation;
- processed-data URL/DOI;
- raw-data accession if present;
- code repository and commit/tag if available;
- access date;
- license/usage notes if stated.

Do not rely on article prose alone if processed quantitative data are available.

### 2. Acquire the processed dataset

Prefer processed mutation-fitness tables over reprocessing raw sequencing reads unless required.

Store lightweight source data under an appropriate `references/`, `data/raw/` or documented external-cache path according to repository policy. Do not commit unnecessary bulk data if large; record checksum and retrieval command.

### 3. Identify EV-A71 2C coordinates and reference sequence

Establish the exact reference isolate / polyprotein accession used in the experiment and the mature 2C boundaries.

Create a machine-readable mapping table from experimental mutation coordinates to mature EV-A71 2C coordinates.

### 4. Extract 2C direct perturbation data

Where available, extract separately:

- insertion fitness, preserving insertion length and inserted sequence/design;
- deletion fitness;
- substitution fitness as secondary functional context.

Do not collapse different insertion designs into a single score without retaining raw design-specific values.

### 5. Map EV-A71 2C to HRV-A89 2C

Use mature sequences and an auditable alignment.

Preferred sequence mapping:

- MAFFT high-accuracy pairwise/alignment method using the established project environment or another reproducible mature method.

Add structure mapping only as a cross-check where it resolves or exposes ambiguous alignment around indels/loops. Do not use structure to force a sequence mapping across genuine alignment ambiguity.

For every mapped A89 junction record:

- EV-A71 residue/junction source coordinates;
- A89 junction;
- mapping class (`exact_aligned`, `gap_adjacent`, `ambiguous`, `unmapped`);
- local alignment context;
- confidence / caution note.

### 6. Project evidence across all 320 A89 junctions

This task must not inspect only the existing `287–291` cluster.

Generate an all-junction table so direct homolog phenotype can challenge the current structural funnel.

Required output candidate:

`data/evA71_2C_direct_indel_to_A89_v1.tsv`

Expected fields should include, when available:

- `a89_junction`
- `a89_left_residue`
- `a89_right_residue`
- `eva71_source_junction`
- `mapping_class`
- `mapping_confidence`
- insertion design/length
- raw/normalized insertion fitness
- deletion fitness/context
- substitution context
- source identifier

### 7. Integrate with current all-junction evidence

Create:

`data/candidate_junctions_v3_direct_indel.tsv`

Merge direct homolog phenotype into the current V2 matrix without overwriting V2.

Explicitly classify:

- `convergent_support`
- `experimental_conflict`
- `new_candidate_outside_strict_gate`
- `no_direct_data`
- `mapping_uncertain`

Do not invent a single arbitrary weighted score. Preserve the individual evidence columns and conflicts.

### 8. Re-audit the current shortlist

Mandatory focal review:

- `287|288`
- `288|289`
- `289|290`
- `290|291`
- `248|249`
- `256|257`
- `223|224`
- `245|246`
- `250|251`

Also report any outside-focal A89 junction with notably favorable direct homolog insertion phenotype.

## Required reports

- `docs/DIRECT_INDEL_001_RUN_LOG.md`
- `docs/EV71_2C_DIRECT_INDEL_MAPPING_V1.md`
- `data/evA71_2C_direct_indel_to_A89_v1.tsv`
- `data/candidate_junctions_v3_direct_indel.tsv`
- source/provenance/checksum records as appropriate

Update after completion:

- `PROJECT_STATE.md`
- `ANALYSIS_INDEX.md`
- `TODO.md`

## Decision states

At task completion choose one:

- `DIRECT_EVIDENCE_SUPPORTS_TARGETED_SHORTLIST`
- `DIRECT_EVIDENCE_REQUIRES_SHORTLIST_REVISION`
- `DIRECT_EVIDENCE_INSUFFICIENT_OR_MAPPING_LIMITED`

Do not start Tag × Site modeling automatically even if the first state is reached. ChatGPT/user review is required.

## Reproducibility / software policy

Use mature software and a reproducible environment. If required software is absent, install it in user space rather than replacing the intended method with a materially weaker custom fallback.

Commit and push meaningful checkpoints. Do not merge to `main` and do not force-push.
