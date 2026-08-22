# Project State

Last updated: 2026-08-22

Project: **HRV-A89 2C small-tag and insertion-site prioritization**

## Scientific objective

Identify a small set of experimentally testable internal-tag constructs for HRV-A89 2C that minimize predicted perturbation of native 2C biology while remaining detectable in downstream mechanistic experiments.

The computational endpoint is **relative candidate prioritization**, not proof of a safe insertion site.

## Current project-level decision state

`NO_HIGH_CONFIDENCE_TARGETED_SITE_YET`

The previous `287|288–290|291` C-terminal cluster is no longer supported as a targeted shortlist after direct EV-A71 2C insertion-fitness mapping. However, the homolog 8-aa insertion result is not treated as universal proof that every HRV-A89-specific MAP8/HA/G196 insertion must fail.

## Current active task

`ONE_SHOT_COMPUTATIONAL_AUDIT_003`

Status: **AUTHORIZED / LONG-RUN COMPUTATIONAL TASK**

Branch: `analysis/conservation-002`

Task specification:

- `tasks/ONE_SHOT_COMPUTATIONAL_AUDIT_003.md`

This task is designed for an unattended 3090-server run. It supersedes `METHOD_HARDENING_002` as the active execution wrapper while preserving all of its mandatory scientific modules.

Authorized scope:

1. EV-A71 substitution-tolerance integration;
2. continuous/Pareto all-320 junction re-ranking;
3. phylogeny-aware independent natural-indel-event analysis;
4. MAP8/HA/G196 tag-specific PLM insertion scans;
5. ranking robustness and negative-control audits;
6. cross-tag consensus/disagreement analysis;
7. reduced computational review-set construction;
8. optional lightweight insertion-specific structural feasibility triage if a mature reproducible method is available;
9. final synthesis and repository-state updates.

Automatic escalation to long MD, experimental protocol design, final experimental construct selection, or RNA/codon design is not authorized.

## Fixed project constraints

- FLAG is excluded because the 9A5 antibody construct already uses FLAG; orthogonal detection is required.
- N- or C-terminal tagging is not assumed safe.
- The ranking unit is peptide junction `i|i+1`, not an isolated residue.
- Homologous functional residues must be explicitly mapped to HRV-A89.
- Monomer-only exposure is insufficient; current site metrics use two A89 monomer models and two hexamer ensembles.
- Current A89 hexamers are template-guided no-membrane/no-RNA hypotheses and cannot establish native RNA-pore geometry by themselves.
- Conservation is supporting evidence, not proof of artificial insertion tolerance.
- Direct homolog insertion phenotype is a strong prior, not an absolute A89-specific binary veto.
- Tagged-structure prediction is a perturbation screen, not biological validation.
- Exact RNA/codon analysis requires the real experimental nucleotide construct; protein back-translation is not an acceptable substitute.
- Decision-changing analyses must use mature reproducible software; missing tools should be installed in user space rather than silently replaced with weaker methods.

## Current structural/evolutionary/direct-evidence state

Ten junctions remain strict structural passes after V2 regeneration:

`155|156`, `174|175`, `175|176`, `216|217`, `217|218`, `218|219`, `287|288`, `288|289`, `289|290`, `290|291`.

`strict_structural_pass` is retained only as a reproducible annotation. It no longer defines candidate membership.

CONSERVATION_002 remains the current near-HRV evolutionary layer. DIRECT_INDEL_001 remains the current high-weight homolog phenotype layer.

Key direct-evidence interpretation:

- all 320 A89 junctions are mapped to EV-A71 mature 2C;
- 315 mappings are exact-aligned, 5 ambiguous, 0 unmapped;
- the direct insertion handle is 8 aa `SGRPGSLS`;
- no mapped A89 junction has EV-A71 2C insertion score `>0`;
- no outside-strict candidate is rescued by favorable direct insertion phenotype;
- the old `287|288–290|291` cluster is unfavorable in the homolog insertion dataset;
- the result is high-weight negative evidence, not universal proof of A89-specific tag failure.

## Current candidate/control roles

### `287|288`, `288|289`, `289|290`, `290|291`

`STRUCTURE_EVOLUTION_FAVORED__DIRECT_HOMOLOG_CONFLICT`

### `248|249`, `256|257`

`HISTORICAL_INSERTION_SUPPORT__MODERN_CONFLICT_CONTROL`

### Other non-hard-excluded junctions

Remain eligible for all-320 continuous/Pareto re-ranking regardless of the previous strict structural gate.

## Current evidence hierarchy

When evidence conflicts, use:

1. direct HRV-A89 insertion/replicon phenotype, if generated;
2. direct homolog 2C insertion phenotype with high-confidence A89 mapping;
3. direct homolog substitution/deletion phenotype and direct 2C genetics/biochemistry;
4. established functional motifs and experimental homolog structures with explicit A89 mapping;
5. A89 continuous structural-ensemble metrics;
6. phylogeny-aware HRV-A evolutionary / independent-indel evidence;
7. tag-specific PLM indel scores;
8. insertion-specific loop/structure ensembles;
9. targeted MD for a reduced construct set only.

No lower-level prediction may silently override stronger direct phenotype or a hard biological constraint.

## Required final outputs from current task

Primary final report:

- `docs/ONE_SHOT_COMPUTATIONAL_AUDIT_003_REPORT.md`

Core data products include:

- `data/candidate_junctions_v4_method_hardening.tsv`
- `data/pareto_junction_frontier_v1.tsv`
- `data/hrvA_independent_indel_events_v1.tsv`
- `data/tag_specific_plm_scores_v1.tsv`
- `data/tag_specific_consensus_v1.tsv`
- `data/computational_review_set_v1.tsv`

The unattended run must stop with exactly one of:

- `READY_FOR_CONFLICT_AWARE_TAG_SITE_MODELING`
- `NO_HIGH_CONFIDENCE_TARGETED_SITE`
- `METHOD_HARDENING_BLOCKED`

## Required future user input

Before final construct recommendation, obtain the exact nucleotide sequence of the experimental HRV-A89 2C region / replicon plasmid. Protein back-translation is not an acceptable substitute for RNA/codon-level auditing.
