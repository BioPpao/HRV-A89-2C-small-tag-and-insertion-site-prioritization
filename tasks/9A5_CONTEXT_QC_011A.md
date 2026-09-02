# Task 011A — 9A5 context QC and hardening

Status: AUTHORIZED / READY FOR CODEX

Branch: `analysis/9a5-context-qc-011a`

Parent: `analysis/9a5-monomer-hexamer-context-011` at `8e84356eca097ee4f388fa92d6fc1f43c82100d5`

## Scientific objective

Harden Task 011 before freezing the 9A5-context candidate ranking. Do not start new long MD, blind docking, AlphaFold/ColabFold, membrane/RNA/ATP calculations, or unrelated expansion.

## Review findings that motivate Task 011A

1. The three packaged files
   - `selected_1x_9A5_weakposres_1ns_rep1_endpoint.pdb`
   - `selected_1x_9A5_weakposres_1ns_rep2_endpoint.pdb`
   - `selected_1x_9A5_weakposres_1ns_rep3_endpoint.pdb`
   have the same SHA256 in Task 011 provenance: `3c0083aa7091b4de51319e81d765fa159711a25ed7f5088f74c253ae38edb884`. They must not be treated as three independent coordinate endpoints until the original repeat outputs are verified.
2. `248|249 x HA` shows a persistent rigid six-tagged-hexamer tag-to-other-protomer clash in Task 011, including a minimum distance around 0.22 A. This may be a real crowding signal or an artifact of one unrelaxed HA conformation rigidly transferred into multiple hexamers.
3. `scripts/candidate_panel_expansion_008.py` still hardcodes `nineA5_epitope_context=unknown_no_verified_A89_9A5_internal_epitope_mapping`, despite the project-defined A89 2C 9A5 epitope being aa148-160.
4. Task 011 was based on the Task 010A scientific state before later report/figure commits on `analysis/experimental-review-cleanup-010a`. Preserve scientific provenance and avoid losing those later non-decision-changing report/figure commits when branches are eventually reconciled.

## Required work

### A. Recover the true 1x9A5 repeat endpoints

Search the local `HRV_Oligomers` repository and the exact server paths referenced by its scripts/reports for the original three independent weak-posres 1 ns repeats.

Preferred sources are the actual analysis outputs such as:
- `analysis/rep1_endpoint_last_frame.pdb`
- `analysis/rep2_endpoint_last_frame.pdb`
- `analysis/rep3_endpoint_last_frame.pdb`

or the corresponding trajectories from which those final frames can be exported without rerunning MD.

Verify:
- file SHA256
- chain identity/residue ranges
- finite coordinates
- each endpoint is genuinely unique
- the coordinates correspond to the intended repeat
- no PBC/rechaining defect

If the original trajectories exist but endpoint PDBs are wrong, re-export only the final frames. Do not rerun MD.

If the underlying trajectories are also duplicated or unavailable, document that explicitly and downgrade the 9A5-bound ensemble confidence rather than fabricating independence.

### B. Recalculate the Task 011 antibody-bound ensemble

Use the verified unique 1x9A5 structures and rerun only the affected structural proxy analysis.

Update or version:
- 9A5 provenance/inventory
- `9a5_hexamer_tag_compatibility`
- ensemble summary
- figures based on antibody-bound ensemble
- candidate integration

Do not count duplicate coordinate files as independent structures.

### C. Harden `248|249 x HA`

Audit whether its rigid-proxy clash is robust.

First reuse all already-existing tagged models for `248|249 x HA` in both repositories/server outputs. Search before computing.

If only one HA conformation exists, generate the minimum additional evidence necessary using one of:
- existing alternate ColabFold ranks/seeds if already present;
- local coordinate perturbation / alternative tag-conformation sampling that preserves the native 2C scaffold;
- restrained/local minimization of the transferred tag region with matched WT/tagged controls.

Do not launch new long MD or broad structure-prediction campaigns.

For each independent HA/tag conformation, evaluate:
- tag-to-adjacent-protomer minimum heavy-atom distance
- hard clash counts <2.0 and <2.5 A
- tag-tag distances
- tag-to-9A5 distances
- whether clashes persist across free and 1x9A5 hexamers

Classify the result as one of:
- ROBUST_HEXAMER_CROWDING
- CONFORMATION_SENSITIVE
- RIGID_PLACEMENT_ARTIFACT_NOT_SUPPORTED
- INSUFFICIENT_EVIDENCE

Do not remove `248|249 x HA` merely because one rigid pose clashes.

### D. Fix the stale 9A5 epitope field

Modify the source-generation code, not a TSV by hand.

Replace the obsolete unknown value with an explicit sequence-defined field based on the project-defined A89 2C 9A5 epitope aa148-160.

Keep sequence-defined epitope context separate from 3D complex compatibility.

Regenerate the affected feature matrix under a new version and document provenance.

### E. Candidate decision update

Produce a new candidate panel, preferably:
`data/final_candidate_panel_v7_9a5_context_qc.tsv`

Do not overwrite V6.

Explicitly compare:
- 289|290 x MAP8
- 289|290 x G196_minimal
- 248|249 x MAP8
- 248|249 x HA
- Priority B backups
- 224|225 controls
- 155|156 hard negative

Key decision question:
Does corrected 9A5-repeat QC and 248|249 HA robustness testing change the experimental ordering?

## Current provisional interpretation to test, not to force

- `289|290 x MAP8` is currently the strongest overall candidate.
- `289|290 x G196_minimal` remains strong but has less direct corrected-protocol MD support.
- `248|249 x MAP8` is structurally cleaner than `248|249 x HA` in the current Task 011 hexamer proxy.
- `248|249 x HA` should remain under review until rigid-clash robustness is resolved.
- `155|156 x MAP8` must remain a hard-negative calibration control.

Do not force the final results to match this provisional interpretation.

## Outputs

At minimum:
- `data/9a5_context_input_provenance_v2_qc.tsv`
- `data/9a5_context_structure_inventory_v2_qc.tsv`
- `data/9a5_hexamer_tag_compatibility_v2_qc.tsv`
- `data/9a5_context_ensemble_summary_v2_qc.tsv`
- `data/248_249_HA_hexamer_robustness_v1.tsv`
- regenerated 9A5 epitope feature matrix with a new version
- `data/final_candidate_panel_v7_9a5_context_qc.tsv`
- `docs/9A5_CONTEXT_QC_011A.md`
- updated figures under a new QC-specific directory
- necessary updates to PROJECT_STATE, DECISIONS, ANALYSIS_INDEX, TODO and ACTIVE_TASK

## Completion gate

Task 011A is complete only when:
1. duplicate endpoint provenance is resolved or explicitly downgraded;
2. the corrected antibody-bound ensemble has been recalculated;
3. `248|249 x HA` rigid-clash robustness has been tested with independent conformational evidence or clearly marked insufficient;
4. stale `nineA5_epitope_context` generation logic is fixed;
5. V7 candidate decisions are generated;
6. repository documentation is updated;
7. all changes are committed and pushed to `analysis/9a5-context-qc-011a`.

No generic long MD is authorized.
