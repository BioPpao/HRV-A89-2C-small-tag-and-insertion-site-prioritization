# FINAL_CANDIDATE_PANEL_STRATEGY_V1

Date: 2026-08-23

Branch: `analysis/candidate-panel-008`

## Final project goal

The final computational goal is **not** to identify one supposedly best insertion junction.

The goal is to build a **ranked, redundant, multi-junction × multi-tag experimental candidate panel** for HRV-A89 2C internal tagging, with enough diversity that downstream wet-lab testing does not depend on one computational hypothesis.

The final panel must:

- contain multiple independent junctions;
- contain multiple small-tag identities;
- retain evidence conflicts instead of averaging them away;
- include negative/conflict controls;
- distinguish protein-perturbation risk from tag-detectability risk;
- remain explicit that no computationally prioritized site is experimentally validated;
- be ranked by evidence class and robustness rather than one opaque scalar score.

## Why the strategy must broaden after OPEN_STRUCTURE_PIPELINE_007

`OPEN_STRUCTURE_PIPELINE_007` solved the major inserted-structure blocker and identified `289|290 × MAP8` and `289|290 × G196_minimal` as strong deep-replicated open-structure rows. However, the present structure panel remains intentionally narrow and many Tier1 rows were only single-model observations.

The literature argues strongly against collapsing candidate discovery to one or two geometrically attractive sites:

- Bakhache et al. 2024 (`10.1038/s41564-024-01871-y`) showed that Enterovirus A insertion/deletion fitness is sparse and strongly site-dependent; direct InDel phenotype should remain a high-weight evidence layer.
- Teterina et al. 2010 (PMCID `PMC2993843`) found no plaque-forming poliovirus 2C insertion mutants in their screen, while tolerated insertions in other non-structural proteins mapped preferentially to external loops/unstructured regions; importantly, not all apparently flexible loops tolerated insertions.
- Deep indel mutagenesis across 181 protein domains (Nature Communications 2025, `10.1038/s41467-025-57510-5`) showed that loops are on average more insertion-tolerant than structured regions, but the effect is modest and not sufficient by itself; secondary-structure boundaries provide additional information.
- EpicTope (2026) formalized conservation, secondary structure, solvent accessibility and disordered-binding features as useful predictors of non-disruptive epitope-tag positions.
- MAP-tag structural work (`10.1093/jb/mvaa054`) showed that inserted epitope recognition depends on local loop geometry and epitope-bound conformation, not only protein-fold preservation.
- PA14/NZ-1 work (2021) showed that epitope geometry and end-to-end configuration can materially affect whether an inserted tag perturbs the target and remains antibody-accessible.
- AlphaFold-family predictions should be treated as structural hypotheses, not dynamic ensembles or experimental truth.

Therefore the next stage must optimize **panel quality**, not one candidate.

## Target final deliverable

The desired final experimental candidate panel should contain approximately:

- **Tier A / primary panel:** 6–10 site × tag constructs spanning at least 4–6 distinct junctions and at least 3 tag systems;
- **Tier B / secondary panel:** 6–12 additional constructs spanning alternative evidence classes, near-neighbor sites and tag-specific rescues;
- **controls:** 4–6 hard-exclusion, direct-conflict or historical-conflict constructs.

This is a target scale, not a fixed quota. The final number should be driven by evidence diversity and wet-lab feasibility.

## Candidate-selection philosophy

### 1. Reopen the full junction universe

Do not define candidate membership only from the current `289|290–290|291` region.

Reuse the all-320 V5 landscape and the 33-junction V2 review set. Any non-hard-excluded junction can re-enter the panel if new orthogonal evidence materially improves its position.

### 2. Separate site ranking from tag ranking

Produce both:

- junction-level ranking independent of tag;
- tag-specific ranking within each junction;
- best-junction ranking within each tag.

A good site for MAP8 is not assumed to be a good site for HA, G196, PA/ALFA/AGIA or other tags.

### 3. Preserve evidence conflicts

Examples:

- structure-favored but direct-homolog-conflicted;
- historical insertion-supported but modern DMS-conflicted;
- low structural perturbation but poor tag accessibility;
- strong tag accessibility but high oligomer/RNA-context risk.

Conflicts are experimentally informative and should remain visible in the final panel.

## Expanded evidence program

### A. Full-320 open insertion-prior feature completion

Add or harden, for all 320 junctions where possible:

- secondary-structure class and distance to helix/strand boundaries;
- solvent exposure / rSASA;
- local disorder and disordered-binding propensity using an open reproducible method such as IUPred2A/ANCHOR2 if available;
- local backbone flexibility proxies;
- local structural confidence/model disagreement;
- insertion-tolerance structural priors derived from deep indel literature;
- junction-level natural-indel and conservation evidence already present.

These features are supporting priors, not direct fitness evidence.

### B. New 2C:RNA holoenzyme structural mapping

Map HRV-A89 2C junctions to the 2026 picornaviral `2C:RNA` holoenzyme preprint (`10.64898/2026.06.07.730651`) with explicit homolog alignment confidence.

Add comparative distances/annotations for:

- RNA-contacting residues;
- pore-facing residues;
- ATPase-coupled RNA-contact neighborhoods;
- residues implicated by mutational validation in the holoenzyme study;
- junction proximity to the central RNA path.

Because the source is a preprint and homologous system, this layer is supporting mechanistic evidence, not a hard veto by itself.

### C. Protease/polyprotein-context risk

Scan every candidate site × tag boundary for creation/disruption of plausible picornaviral protease-recognition motifs and local polyprotein-processing risk.

The output should explicitly distinguish:

- known canonical cleavage sites;
- cryptic cleavage-like sequence motifs introduced by tag boundaries;
- proximity to native precursor-processing regions.

Do not infer actual cleavage solely from motif sequence; use this as a risk flag.

### D. Tag-recognition geometry and detectability

The project must evaluate not only whether 2C tolerates the inserted peptide, but whether the inserted epitope is likely to remain detectable.

For tags with known bound structures, use open structural references to evaluate:

- inserted tag solvent exposure;
- tag end-to-end distance and local conformation;
- similarity to known antibody/nanobody-bound epitope geometry where meaningful;
- steric accessibility of the cognate binder in monomer and hexamer contexts;
- whether a minimal linker or native loop geometry is more appropriate.

This is particularly relevant for MAP8 and PA-type tags, where epitope-bound structures directly show loop-compatible conformations.

### E. Expand the tag portfolio carefully

Current core tags remain:

- MAP8;
- HA;
- G196_minimal.

`G196_practical_GS` is retained as a tag-architecture comparison but is not automatically preferred because OPEN_STRUCTURE_PIPELINE_007 found worse mean hexamer-clash behavior.

Evaluate additional tags only when exact sequence, detection reagent and intended assay are clear. High-priority candidates for literature/reagent review include:

- ALFA (15 aa; nanobody-based; strong structural definition);
- PA12/PA14 (12/14 aa; strong insertion-specific structural literature; PA14 may be more insertion-compatible than PA12 in some contexts);
- AGIA (9 aa; high-affinity antibody system);
- HiBiT (11 aa) if luminescent complementation is experimentally useful and orthogonal detection is desired.

Do not automatically model all tags at all 320 sites. First perform tag-level feasibility and reagent/assay review, then expand computational modeling only for tags that are realistically usable.

### F. Broaden multi-model structure replication

OPEN_STRUCTURE_PIPELINE_007 gave deep replication only to four constructs.

Before final ranking, perform multi-seed/model replication for a broader **diverse** subset, including:

- current leaders;
- neighboring C-terminal sites;
- at least two non-C-terminal alternative junctions;
- at least one historical-conflict site;
- at least one direct-phenotype-relative-tolerance site;
- tag-specific alternatives.

The objective is to reduce single-model selection bias.

### G. Local oligomer prediction beyond rigid placement

For the most informative constructs, consider open AlphaFold/ColabFold multimer modeling of a **local dimer or trimer context** rather than only rigidly placing tagged monomers into the full hexamer.

Use this only where computationally tractable. The aim is to test whether neighboring protomers relax around an insertion and whether rigid-placement clash estimates are overly pessimistic or optimistic.

### H. Targeted replicated dynamics as one evidence layer

Dynamics is not the whole next stage.

Use multiple short independent replicas for a **broader candidate subset**, not only one or two constructs.

Priority readouts:

- native-domain RMSD/RMSF;
- insertion-loop RMSF;
- tag exposure persistence;
- local secondary-structure persistence;
- contact-network persistence;
- interface-contact persistence where modeled;
- convergence across replicas.

Prefer replicate breadth over one very long trajectory at this stage.

### I. Dynamic/allosteric network analysis

For constructs that undergo targeted dynamics, derive:

- dynamic cross-correlation;
- residue-network/community changes;
- communication-path changes between insertion site and ATPase/RNA/interface neighborhoods;
- whether perturbation remains local or propagates into functional elements.

Treat this as mechanistic context, not direct viral fitness.

### J. Exact nucleotide/RNA design gate

Protein-level ranking may continue now.

Before the final wet-lab construct panel is issued, the exact experimental HRV-A89 nucleotide construct must be provided so the project can audit:

- codon-level design;
- local RNA secondary-structure perturbation;
- cryptic RNA signals;
- recombination/repeat risk;
- codon-resolved tag designs.

No protein back-translation should substitute for the real construct.

## Ranking framework

Do not use one hidden weighted total score.

Use a multi-objective framework with separate axes:

1. hard biological exclusion status;
2. direct HRV-A89 phenotype, if later available;
3. homolog direct insertion phenotype;
4. homolog substitution/deletion phenotype;
5. functional motif / RNA-holoenzyme proximity;
6. conservation / independent natural indel support;
7. PLM tag-specific perturbation;
8. real inserted-structure ensemble perturbation;
9. tag-recognition/accessibility geometry;
10. oligomer-context compatibility;
11. targeted dynamics / network stability;
12. protease/polyprotein-context risk;
13. nucleotide/RNA-context risk once exact sequence is supplied.

Final ranking should use:

- Pareto/non-dominated membership;
- evidence-class labels;
- leave-one-layer-out robustness;
- bootstrap/resampling rank stability where meaningful;
- explicit unresolved-conflict labels.

## Desired final candidate classes

### Tier A — primary experimental candidates

Require support from multiple independent computational layers, no hard biological exclusion and no major unresolved detectability problem.

Direct-homolog conflict may remain, but must be explicitly labeled.

### Tier B — secondary/rescue candidates

Include constructs with one important evidence conflict but substantial independent support or a distinct tag/site rationale.

### Conflict controls

Examples:

- historical insertion support vs modern homolog conflict;
- structure support vs direct insertion conflict;
- good tag accessibility vs poor oligomer context.

### Hard negative controls

Retain a small number of known functional exclusions to calibrate whether computational methods correctly distinguish biologically implausible insertions.

## Final report requirements

The eventual final report must provide:

- a ranked **junction-level** table;
- a ranked **site × tag** table;
- per-tag best junctions;
- per-junction best tags;
- Tier A / Tier B / conflict-control / hard-negative panels;
- evidence provenance for every recommendation;
- uncertainty and robustness for every construct;
- explicit wet-lab priority order without claiming validation.

## Current checkpoint

`OPEN_STRUCTURE_PIPELINE_007` is complete and the project is technically eligible for targeted dynamics, but targeted dynamics is only one part of the broader candidate-panel program.

The next execution task is `CANDIDATE_PANEL_EXPANSION_008`.
