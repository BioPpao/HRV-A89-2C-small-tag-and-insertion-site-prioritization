# CANDIDATE_PANEL_EXPANSION_008

Status: **AUTHORIZED / STRATEGIC EXPANSION BEFORE FINAL PANEL**

Date: 2026-08-23

Branch: `analysis/candidate-panel-008`

## Mission

Build a broader, more reliable HRV-A89 2C internal-tag candidate universe before any final wet-lab construct panel is selected.

This task must not collapse the project to one or two current structural leaders. It must identify multiple junctions, multiple tag identities, multiple evidence classes and explicit controls, then produce a ranked candidate panel suitable for subsequent deeper computation and eventual wet-lab testing.

Read first:

- `PROJECT_STATE.md`
- `ACTIVE_TASK.md`
- `docs/FINAL_CANDIDATE_PANEL_STRATEGY_V1.md`
- `docs/OPEN_STRUCTURE_PIPELINE_007_REPORT.md`
- `data/tag_site_integrated_perturbation_v3_open.tsv`
- `data/candidate_junctions_v5_plm_gpu.tsv`
- `data/computational_review_set_v2_plm_gpu.tsv`
- `DECISIONS.md`
- `ANALYSIS_INDEX.md`

## Core principles

1. The final goal is a **ranked experimental candidate panel**, not one best site.
2. Reopen all 320 junctions for supporting-feature review; only true hard biological exclusions remain hard exclusions.
3. Keep site ranking and tag ranking separate.
4. Preserve conflicting evidence rather than averaging it away.
5. Do not use one opaque weighted score.
6. Prefer multiple independent computational evidence classes and robustness analysis.
7. Targeted dynamics is one later layer, not the only next method.
8. No site may be called safe or validated without HRV-A89-specific experimental evidence.

## Stage 1 — literature/evidence-gap registry update

Update the project literature registry for evidence directly relevant to insertion-site selection and tag engineering.

At minimum include and classify:

- EV-A71 full-proteome substitution/InDel scanning (`10.1038/s41564-024-01871-y`);
- poliovirus non-structural insertion study, including the negative 2C result (PMCID `PMC2993843`);
- deep indel mutagenesis across protein domains (`10.1038/s41467-025-57510-5`);
- EpicTope non-disruptive tag-site feature framework;
- MAP8 internal insertion structural work (`10.1093/jb/mvaa054`);
- PA12/PA14 insertion structural work and NZ-1 binder geometry;
- ALFA-tag structural/binder literature;
- AGIA tag literature;
- 2026 picornaviral 2C:RNA holoenzyme preprint (`10.64898/2026.06.07.730651`);
- enteroviral 2C biochemical RNA/ATP mechanism literature.

For every source record:

- evidence type;
- directness to HRV-A89 2C insertion tolerance;
- whether peer reviewed or preprint;
- what conclusion it can and cannot support.

## Stage 2 — full-320 feature completion

For all 320 peptide junctions, add/harden open reproducible features where missing:

- secondary structure;
- distance to nearest helix/strand boundary;
- solvent accessibility/rSASA;
- local confidence/model disagreement;
- local disorder propensity;
- disordered-binding propensity where an open mature method is available;
- local flexibility proxies;
- structural insertion-prior annotations based on deep-indel literature;
- existing conservation/indel/Pareto/direct-phenotype evidence.

Create:

- `data/junction_feature_matrix_v6_candidate_panel.tsv`

## Stage 3 — 2C:RNA holoenzyme mapping

Map HRV-A89 junctions to the 2026 picornaviral 2C:RNA holoenzyme structure/model with explicit homolog alignment confidence.

Create junction-level annotations for:

- distance/proximity to RNA-contact residues;
- pore-facing context;
- ATPase/RNA-coupled neighborhoods;
- experimentally mutationally supported RNA-contact regions;
- whether the junction would plausibly project toward or away from the central RNA path.

This is homolog/preprint evidence and must not be treated as an absolute veto.

Create:

- `data/hrvA89_2C_RNA_holoenzyme_mapping_v1.tsv`
- `docs/RNA_HOLOENZYME_MAPPING_V1.md`

## Stage 4 — protease/polyprotein boundary-risk analysis

For every candidate site × tag sequence considered, scan tag boundaries for creation of plausible picornaviral protease-recognition motifs or unusual polyprotein-processing risk.

Create:

- `data/tag_boundary_protease_risk_v1.tsv`

Keep this as a risk annotation, not proof of cleavage.

## Stage 5 — tag portfolio review and expansion

Core tags:

- MAP8
- HA
- G196_minimal

Architecture comparison:

- G196_practical_GS

Literature/reagent feasibility review candidates:

- ALFA
- PA12/PA14
- AGIA
- HiBiT if the intended readout makes biological/experimental sense

For each tag record:

- exact sequence and length;
- cognate binder/readout;
- evidence for internal insertion;
- known bound conformation if available;
- expected structural footprint;
- assay compatibility;
- reagent availability/status;
- whether it should enter computational expansion now.

Create:

- `data/tag_portfolio_v2.tsv`
- `docs/TAG_PORTFOLIO_V2.md`

Do not model a tag broadly until its exact sequence and realistic experimental readout are fixed.

## Stage 6 — tag-recognition geometry / binder accessibility

For tags with known binder-bound structures, add a detectability-specific structural layer.

Where feasible evaluate:

- inserted-tag solvent accessibility;
- tag end-to-end geometry;
- similarity to known bound epitope conformation;
- whether antibody/nanobody/Fab placement is sterically compatible with the monomer;
- whether binder placement is compatible with existing hexamer hypotheses;
- tag-specific linker requirement or penalty.

Create:

- `data/tag_binder_accessibility_v1.tsv`
- `docs/TAG_BINDER_ACCESSIBILITY_V1.md`

This layer must remain distinct from target-protein structural perturbation.

## Stage 7 — expanded structural replication panel

Do not restrict deep structure replication to the four constructs used in OPEN_STRUCTURE_PIPELINE_007.

Select a diverse expanded panel that includes:

- current leaders;
- neighboring C-terminal sites;
- at least two non-C-terminal alternative junctions;
- historical insertion-conflict controls;
- direct-phenotype-relative-tolerance rows;
- tag-specific alternatives;
- at least one hard-negative control.

Use multiple ColabFold seeds/models for the expanded set.

Target a tractable but broader panel, approximately 12–24 site × tag constructs depending on computational burden.

Create:

- `data/expanded_structure_replication_panel_v1.tsv`
- `data/expanded_structure_replication_metrics_v1.tsv`

## Stage 8 — local oligomer-context prediction

For the most informative site × tag constructs, use open multimer modeling if tractable to test local neighboring-protomer accommodation.

Prefer dimer/trimer models over a prohibitively expensive full six-protomer prediction when they answer the local interface question.

Compare with rigid-placement hexamer metrics.

Create:

- `data/local_multimer_tag_context_v1.tsv`

If not technically tractable, record explicit status and continue.

## Stage 9 — candidate-panel preliminary ranking

Integrate all completed evidence without one hidden weighted score.

Produce separate dimensions for:

- hard biological constraint;
- direct homolog insertion phenotype;
- substitution/deletion context;
- conservation/indel evidence;
- secondary-structure/accessibility/disorder prior;
- 2C:RNA holoenzyme context;
- protease/polyprotein boundary risk;
- tag-specific PLM;
- real inserted-structure perturbation;
- binder accessibility;
- oligomer context;
- method/replicate robustness.

Use:

- Pareto/non-dominated membership;
- evidence classes;
- leave-one-layer-out sensitivity;
- rank stability/resampling where meaningful;
- explicit conflict labels.

Create:

- `data/candidate_panel_preliminary_v1.tsv`
- `results/candidate_panel_008/ranking_robustness_v1.tsv`

## Stage 10 — define broader dynamics panel

Only after preliminary panel ranking, define a **broader** targeted-dynamics subset rather than one or two constructs.

Aim for a diverse set such as:

- 6–10 site × tag constructs;
- multiple junctions;
- multiple tag identities;
- at least one conflict control.

Prefer multiple short independent replicas over one long trajectory per construct at this stage.

Do not execute dynamics unless separately authorized after this task's review gate.

Create:

- `data/proposed_targeted_dynamics_panel_v1.tsv`

## Stage 11 — final candidate-panel design specification

Produce a candidate-panel proposal with approximately:

- Tier A: 6–10 primary constructs;
- Tier B: 6–12 secondary/rescue constructs;
- Controls: 4–6 conflict/hard-negative constructs.

The exact numbers may vary if evidence strongly supports a smaller or larger set.

Required outputs:

- ranked junction-level table;
- ranked site × tag table;
- per-tag best junctions;
- per-junction best tags;
- explicit Tier A / Tier B / control membership;
- rationale and unresolved conflicts for every construct.

Create:

- `data/final_candidate_panel_draft_v1.tsv`
- `docs/CANDIDATE_PANEL_EXPANSION_008_REPORT.md`

## Stop gate

This task may propose but must not automatically execute:

- targeted dynamics;
- final wet-lab construct synthesis;
- final RNA/codon design;
- experimental protocol design.

Exact experimental nucleotide context remains mandatory before final construct design.

## Final task state

Return exactly one of:

- `READY_FOR_BROAD_TARGETED_DYNAMICS`
- `READY_FOR_CANDIDATE_PANEL_REVIEW`
- `CANDIDATE_PANEL_EXPANSION_PARTIALLY_COMPLETE`

Before completion update:

- `PROJECT_STATE.md`
- `ACTIVE_TASK.md`
- `TODO.md`
- `ANALYSIS_INDEX.md`
- `DECISIONS.md`
