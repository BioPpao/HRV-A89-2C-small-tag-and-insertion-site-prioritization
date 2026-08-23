# Project State

Last updated: 2026-08-23

Project: **HRV-A89 2C small-tag and insertion-site prioritization**

## Final scientific objective

Build a **ranked, redundant, multi-junction × multi-tag experimental candidate panel** for HRV-A89 2C internal tagging that minimizes predicted perturbation while remaining experimentally detectable.

The endpoint is not one computationally optimal site. The endpoint is a diversified candidate set with primary candidates, secondary/rescue candidates, conflict controls and hard-negative controls for downstream wet-lab validation.

No computational result may be described as a safe or experimentally validated site.

## Current project-level state

`READY_FOR_BROAD_TARGETED_DYNAMICS`

`OPEN_STRUCTURE_PIPELINE_007` is complete and technically resolved the previous inserted-structure blocker. The project is eligible for targeted dynamics, but targeted dynamics is now treated as only one future evidence layer within a broader candidate-panel program.

## Current active branch and task

Branch:

`analysis/candidate-panel-008`

Active task:

`CANDIDATE_PANEL_EXPANSION_008`

Status:

**COMPLETE / READY FOR REVIEW**

Task specification:

- `tasks/CANDIDATE_PANEL_EXPANSION_008.md`

Strategic specification:

- `docs/FINAL_CANDIDATE_PANEL_STRATEGY_V1.md`

## Branch provenance

`analysis/candidate-panel-008` was created from the current scientific branch:

`analysis/conservation-002`

The completed OPEN_STRUCTURE_PIPELINE_007 results and all upstream evidence were inherited unchanged. New candidate-panel work should be performed on `analysis/candidate-panel-008` unless explicitly merged later.

## Current completed evidence stack

The project already contains:

- A89 functional constraint/exclusion mapping;
- all-320 WT structural metrics;
- HRV-A conservation and natural-indel context;
- phylogeny-aware independent-indel analysis;
- EV-A71 direct insertion/deletion/substitution phenotype mapping;
- continuous/Pareto all-320 re-ranking;
- tag-specific ESM2 PLM scores for MAP8, HA and G196 forms;
- open ColabFold inserted-structure modeling;
- OpenMM geometry QC;
- WT-vs-tagged structural perturbation metrics;
- tagged hexamer-context analysis;
- tagged contact-network analysis.

## OPEN_STRUCTURE_PIPELINE_007 checkpoint

OPEN_STRUCTURE_PIPELINE_007 modeled:

- 40 inserted constructs;
- WT reference;
- 49 total model rows;
- four deep-replicated constructs with three models each.

The strongest deep-replicated structural rows were:

- `289|290 × MAP8`;
- `289|290 × G196_minimal`.

`290|291 × MAP8/G196_minimal` remained low-clash but weakened by native/local RMSD after deeper replication.

`256|257` was strongly disfavored by actual tagged-hexamer clash context.

These observations remain **relative computational evidence only** and do not define the final candidate panel.

## Why the candidate universe is being reopened

The final experimental design should not depend on one narrow structural cluster because:

- direct homolog insertion fitness remains unfavorable for all mapped A89 junctions in the EV-A71 dataset;
- historical poliovirus work found 2C particularly intolerant to insertion;
- insertion tolerance is strongly sequence-, site- and protein-context dependent;
- flexible/exposed loops are enriched for tolerated insertions but are not sufficient predictors by themselves;
- current deep structural replication covers only four constructs;
- tag detectability/binder geometry has not yet been integrated as a separate evidence axis;
- the new 2026 picornaviral 2C:RNA holoenzyme evidence has not yet been mapped systematically onto A89 junctions.

Therefore all 320 junctions remain available for supporting-feature review, subject to true hard biological exclusions.

## Candidate-panel program now authorized

The current task adds the following missing high-information layers:

1. literature/evidence-gap registry update;
2. full-320 secondary-structure boundary, solvent exposure, disorder/flexibility feature completion;
3. mapping to the 2026 picornaviral 2C:RNA holoenzyme;
4. tag-boundary protease/polyprotein risk analysis;
5. realistic tag-portfolio expansion;
6. tag-binder accessibility and epitope-recognition geometry;
7. broader multi-seed inserted-structure replication;
8. local dimer/trimer accommodation modeling where tractable;
9. preliminary candidate-panel multi-objective ranking;
10. definition of a broader targeted-dynamics subset;
11. draft final Tier A / Tier B / control candidate panel.

`CANDIDATE_PANEL_EXPANSION_008` completed these layers where technically tractable. Local multimer prediction remains deferred; exact nucleotide/RNA-context analysis remains blocked until the real construct sequence is supplied.

## CANDIDATE_PANEL_EXPANSION_008 checkpoint

Primary report:

- `docs/CANDIDATE_PANEL_EXPANSION_008_REPORT.md`

Key generated outputs:

- `data/junction_feature_matrix_v6_candidate_panel.tsv` -- 320 junction rows;
- `data/expanded_structure_replication_metrics_v1.tsv` -- 18 constructs;
- `results/candidate_panel_008/expanded_prediction_manifest.tsv` -- 36 ColabFold model rows;
- `results/candidate_panel_008/expanded_openmm_qc_v1.tsv` -- 36 OpenMM QC rows;
- `data/final_candidate_panel_draft_v1.tsv` -- 8 Tier A, 8 Tier B, 2 controls;
- `data/proposed_targeted_dynamics_panel_v1.tsv` -- 9 constructs.

Tier A spans 6 junctions and 3 tag systems. No candidate is safe or validated.

## Tag strategy

Core current tags:

- MAP8;
- HA;
- G196_minimal.

Architecture comparison:

- G196_practical_GS.

Candidate expansion tags for literature/reagent feasibility review:

- ALFA;
- PA12/PA14;
- AGIA;
- HiBiT if luminescent complementation fits the intended experimental readout.

FLAG remains excluded because the 9A5 construct already uses FLAG.

No new tag should enter broad modeling until its exact sequence and realistic detection reagent/readout are fixed.

## Evidence hierarchy

When evidence conflicts, use:

1. direct HRV-A89 insertion/replicon phenotype, if generated;
2. direct homolog 2C insertion phenotype with high-confidence A89 mapping;
3. direct homolog substitution/deletion phenotype and direct 2C genetics/biochemistry;
4. established functional motifs and experimental homolog structures, including RNA-bound context;
5. A89 structural ensemble / oligomer-context evidence;
6. phylogeny-aware evolutionary / natural-indel evidence;
7. tag-specific PLM;
8. tag-binder accessibility / inserted-structure / network evidence;
9. replicated targeted dynamics;
10. exact nucleotide/RNA-context analysis before final construct design.

No lower-level prediction may silently override stronger evidence.

## Ranking policy

Do not use one opaque weighted scalar.

Final candidate ranking must retain separate evidence axes and use:

- Pareto/non-dominated membership;
- evidence-class labels;
- leave-one-layer-out sensitivity;
- rank stability/resampling where meaningful;
- explicit unresolved-conflict labels.

Required final views:

- junction-level ranking;
- site × tag ranking;
- best junctions within each tag;
- best tags within each junction;
- Tier A / Tier B / control memberships.

## Target candidate-panel scale

Approximate target:

- Tier A: 6–10 primary constructs spanning at least 4–6 distinct junctions and at least 3 tag systems;
- Tier B: 6–12 secondary/rescue constructs;
- controls: 4–6 conflict/hard-negative constructs.

This is a target range, not a quota.

## Current stop gate

`CANDIDATE_PANEL_EXPANSION_008` defined a proposed broader targeted-dynamics panel but did not run it.

Do not automatically start:

- targeted dynamics;
- final construct synthesis;
- experimental protocol design;
- final RNA/codon design.

## Required future user input

Before final wet-lab construct recommendation, obtain the exact nucleotide sequence of the experimental HRV-A89 2C region / replicon/plasmid context. Protein back-translation is not an acceptable substitute.
