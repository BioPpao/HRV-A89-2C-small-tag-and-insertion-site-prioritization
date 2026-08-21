# CONSERVATION_001 — HRV-A 2C conservation and indel-tolerance layer

## Status

**ACTIVE**

Branch: `analysis/conservation-001`

## Objective

Build the near-HRV evolutionary evidence layer required before tag × site modeling.

The task asks:

> Across HRV-A, which HRV-A89 2C peptide junctions show relatively low evolutionary constraint, natural sequence variation, or indel tolerance, and does that evidence support, weaken, or leave unresolved the existing structural and functional evidence?

This phase must analyze all **321 residues / 320 internal peptide junctions** before reducing to candidate subsets.

The endpoint is an auditable candidate-junction evidence matrix. It is **not** selection of a computationally “safe” site.

## Hard boundaries

Do not start:

- MAP8, HA, G196, AGIA, ALFA, PA, or HiBiT insertion modeling;
- tagged AlphaFold modeling;
- new long generic MD;
- membrane/RNA MD;
- final construct/codon design;
- experimental viral rescue, propagation, infection, or optimization procedures.

The RNA/codon layer remains blocked until the exact experimental replicon nucleotide sequence is supplied.

## Authoritative project inputs

Read current repository state before analysis, especially:

- `PROJECT_STATE.md`
- `DECISIONS.md`
- `ANALYSIS_INDEX.md`
- `docs/METHOD_LOGIC_AUDIT_V2.md`
- `docs/2C_FUNCTIONAL_EXCLUSION_MAP_V3.md`
- `docs/2C_FUNCTIONAL_CONSTRAINT_MAP_V2.md`
- `docs/STRUCTURAL_SCREEN_V2.md`
- `data/junction_structural_metrics_v1.tsv`
- `data/CVB3_to_A89_functional_mapping_v1.tsv`
- `references/HRV_A89_2C_reference_sequence.fasta`
- `references/LITERATURE_EVIDENCE_REGISTRY.md`

A89 residue numbering remains 1–321 and peptide-junction numbering remains `i|i+1`.

## Required analysis tracks

Conservation must not be restricted to the current strict structural 10.

Maintain at least three explicit tracks:

1. **strict structural pass** — existing `strict_structural_pass == True`;
2. **structural near-miss** — does not touch a hard `EXCLUDE` feature and fails only a limited number of existing structural gates; record `failed_gate_count` and `failed_gate_names` transparently;
3. **literature-rescue** — preserve historical positive insertion-tolerance evidence already mapped in the repository, including the current A89 `248|249` and `256|257` rescue track unless new auditable mapping evidence changes it.

Do not hide these tracks behind one composite score.

## Dataset design

### Primary HRV-A type-balanced panel

Build a representative HRV-A 2C dataset using current authoritative taxonomy and traceable sequence records.

Prefer, in order:

1. ICTV-recognized/reference exemplars when available;
2. NCBI RefSeq/high-quality complete records;
3. well-annotated complete genome/polyprotein records;
4. other high-quality complete records with traceable 2C boundaries.

Aim for one high-quality representative per recognized HRV-A type where feasible.

Do not hard-code an expected type count. Record expected/observed/missing/ambiguous types from the taxonomy/source state at execution time.

### HRV-A isolate-expanded panel

Build a second panel containing additional isolates for within-type variation and natural-indel checks.

Do not let heavily sampled types dominate the main conservation inference. Retain a type-balanced or type-weighted interpretation alongside unweighted expanded metrics.

### Secondary HRV-B/C context

After the HRV-A primary analysis, use HRV-B/C only as secondary context for candidate windows/regions. Do not pool A/B/C into one primary entropy score.

## Data sources and provenance

Use traceable authoritative sources such as:

- ICTV;
- NCBI RefSeq / GenBank / NCBI Virus / NCBI Datasets;
- UniProtKB.

Create:

`references/CONSERVATION_DATA_SOURCES.md`

Record source/database, query/retrieval method, retrieval date, accession, virus type, strain/isolate, completeness, 2C extraction method, retain/exclude reason, and any ambiguity.

Never invent an accession, type, boundary, sequence, or source.

If acquisition fails, record the failure and any fallback. Mark scientifically weaker fallbacks as provisional.

## Sequence extraction and QC

The repository A89 reference FASTA is authoritative and must remain 321 aa. External A89 records are cross-checks only.

Prefer annotated mature 2C products or explicitly annotated polyprotein coordinates. Do not guess 2C boundaries from approximate length.

QC should include at least:

- accession/type metadata presence;
- traceable 2C boundary;
- non-empty protein sequence;
- no internal stop;
- unknown residues;
- length/completeness;
- duplicate accession/sequence/isolate;
- partial records;
- alignment coverage against A89;
- extreme-divergence/taxonomic outliers.

A non-321-aa sequence is not automatically invalid: true natural indels are part of the question. Distinguish real indels from partial/truncated records and alignment artifacts.

## Alignment

Use a mature protein MSA method such as MAFFT and record its version and parameters.

The A89 authoritative reference must map unambiguously from residues 1–321 to alignment columns.

As an alignment QC check, inspect correct placement of established A89 features including:

- Walker A aa124–131;
- 9A5 epitope aa148–160;
- Walker B aa165–170;
- A197/L199/K202 homolog-mapped RNA-related region;
- motif C aa210–216;
- R233/R234;
- C262/C273/C278 Zn-related region;
- aa305–321 C-terminal region.

Severe misalignment of these core regions should trigger sequence/boundary/taxonomy review rather than silent acceptance.

## Residue-level conservation

Generate exactly 321 A89-anchored rows in:

`data/hrvA_conservation_per_residue.tsv`

At minimum retain:

- `a89_residue`, `a89_aa`;
- total/effective sequence counts;
- dominant amino acid and frequency;
- A89 identity fraction;
- Shannon entropy and normalized entropy;
- gap frequency;
- primary type-balanced metrics;
- expanded-panel metrics;
- type-weighted metrics.

Document the entropy formula and explicitly state how gaps and unknown residues are handled. Prefer amino-acid entropy and gap frequency as separate quantities.

## Junction-level conservation

Generate exactly 320 rows (`1|2` through `320|321`) in:

`data/hrvA_conservation_per_junction.tsv`

Each row should preserve both flanking residues and local-window statistics. Use a clearly defined primary local window, preferably junction ±5 residues; additional windows may be added but must be reported consistently.

Retain at least:

- left/right identity, entropy, gap frequency;
- local-window mean/max entropy;
- local-window mean/min identity;
- local-window gap statistics;
- natural insertion/deletion indicators and frequencies;
- type-balanced, expanded, and type-weighted variants.

## Natural indel analysis

Using A89 as the coordinate anchor, explicitly record whether HRV-A sequences contain natural insertions between A89 residues `i` and `i+1`, plus local deletions relative to A89.

At minimum record counts/frequencies and insertion lengths. Distinguish likely lineage indels from partial records or alignment artifacts.

Natural indels are supporting evidence only; do not infer tolerance of an artificial peptide tag directly from them.

## Evidence integration

Join evolutionary data to `data/junction_structural_metrics_v1.tsv` using the existing `junction` field as the key. Do not invent a second numbering system.

Generate:

`data/candidate_junctions_v1.tsv`

Prefer retaining all 320 junctions, with columns for:

- existing functional and structural metrics;
- structural track;
- failed structural gates;
- literature-rescue status/source;
- HRV-A conservation metrics;
- HRV-A indel metrics;
- HRV-B/C context where available;
- explicit `evidence_conflict`;
- concise `priority_interpretation`.

Default rule: **no opaque final composite score**. If an exploratory score is computed, keep every component, equation, and weight and state that weights are not experimentally calibrated.

## Regions requiring explicit interpretation

The final report must discuss, without limiting the genome-wide analysis to them:

- `155|156` — 9A5 epitope plus homologous RNA/pore-function warning;
- `174|175`, `175|176` — Walker B adjacency;
- `216|217`, `217|218`, `218|219` — motif-C adjacency;
- `248|249`, `256|257` — literature-rescue track;
- `287|288`, `288|289`, `289|290`, `290|291` — favorable geometry but Zn/Cys-rich-to-C-terminal transition risk.

For each conflict, classify the evolutionary layer as: `supports`, `weakens`, or `remains unresolved` relative to the prior interpretation.

## Required scripts and outputs

Implement reproducible scripts with clear `--help` interfaces. A reasonable layout is:

- `scripts/acquire_hrv_2C_sequences.py`
- `scripts/qc_hrv_2C_sequences.py`
- `scripts/map_alignment_to_A89.py`
- `scripts/calculate_conservation.py`
- `scripts/integrate_junction_evidence.py`

Names may be adjusted if responsibilities remain clear.

Expected lightweight data artifacts include:

- `data/hrvA_2C_sequences.fasta`
- `data/hrvA_2C_sequence_metadata.tsv`
- `data/hrvA_2C_expanded_sequences.fasta`
- `data/hrvA_2C_expanded_metadata.tsv`
- `data/hrvA_2C_alignment.fasta`
- `data/hrvA_2C_expanded_alignment.fasta`
- `data/hrvA_conservation_per_residue.tsv`
- `data/hrvA_conservation_per_junction.tsv`
- `data/hrvABC_candidate_window_context.tsv`
- `data/candidate_junctions_v1.tsv`

Create:

- `docs/CONSERVATION_001_RUN_LOG.md`
- `docs/CONSERVATION_SCREEN_V1.md`
- an environment/version record under `results/` or another documented path.

## Validation assertions

Automate at least these checks:

- authoritative A89 sequence length == 321;
- residue table rows == 321;
- junction table rows == 320;
- integrated junction rows == 320;
- junction keys are unique and span `1|2` to `320|321`;
- identity/gap frequencies are within [0,1];
- entropy is non-negative;
- no silent missing join;
- authoritative A89 sequence matches the repository FASTA.

Analysis programs should exit non-zero when critical assertions fail.

## Report requirements

`docs/CONSERVATION_SCREEN_V1.md` must cover:

1. scientific question;
2. dataset construction and provenance;
3. dataset/QC statistics;
4. alignment method and A89 mapping;
5. conservation and indel methods;
6. whole-protein evolutionary pattern;
7. functional-motif alignment sanity checks;
8. strict structural track;
9. near-miss track;
10. literature-rescue track;
11. HRV-B/C context;
12. integrated evidence conflicts;
13. junctions whose priority increased/decreased/remained unchanged after conservation;
14. whether any new candidate outside the strict 10 merits later review;
15. limitations;
16. the next scientific gate.

Do not force a positive result. `No convincing lower-risk junction emerged` is an acceptable outcome if supported by the data.

## Git checkpoints

Follow `WORKFLOW.md` and push meaningful checkpoints to `origin/analysis/conservation-001`.

Suggested commits:

1. `analysis: initialize CONSERVATION_001 workflow`
2. `analysis: add HRV-A 2C dataset and alignment`
3. `analysis: add HRV-A conservation and indel metrics`
4. `analysis: integrate conservation evidence into junction prioritization`

Stage only explicit paths. Do not merge into `main` and do not force-push.

## Completion updates

If the phase completes successfully, update current-state/navigation files as justified:

- `PROJECT_STATE.md`
- `ANALYSIS_INDEX.md`
- `TODO.md`
- `README.md`
- `AGENTS.md`

Update `DECISIONS.md` only if a genuine project-level decision changed.

The final run log must state `COMPLETE` or `BLOCKED`, not an ambiguous status.

## Final Codex handoff

At task end, return only a compact summary containing:

- status;
- branch;
- starting/latest commit;
- push status;
- primary/expanded dataset sizes and QC exclusions;
- confirmation of 321/320/320 output row counts;
- key priority changes;
- literature-rescue status for `248|249` and `256|257`;
- interpretation of the `287–291` region;
- any new candidate outside the strict 10;
- unresolved conflicts;
- important output paths;
- next decision required from ChatGPT/user.
