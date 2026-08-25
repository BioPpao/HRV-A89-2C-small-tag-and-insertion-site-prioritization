# Project State

Last updated: 2026-08-25

Project: **HRV-A89 2C small-tag and insertion-site prioritization**

## Final Scientific Objective

Build a ranked, redundant, multi-junction x multi-tag experimental candidate panel for HRV-A89 2C internal tagging.

No computational result may be described as safe or experimentally validated.

## Current Project-Level State

Task 010A has achieved:

`EXPERIMENTAL_REVIEW_SHORTLIST_READY_FOR_DISCUSSION`

## Current Branch And Task

Branch:

`analysis/experimental-review-cleanup-010a`

Task:

`FINAL_SCIENTIFIC_CLEANUP_AND_EXPERIMENTAL_SHORTLIST_010A`

Primary specification:

- `tasks/FINAL_SCIENTIFIC_CLEANUP_AND_EXPERIMENTAL_SHORTLIST_010A.md`

Execution script:

- `scripts/dynamics_audit_010a_cleanup.py`

Codex prompt:

- `codex/TASK_010A_CLEANUP_PROMPT.md`

## Completed Task 010 Evidence Base

Task 009 produced the broad comparative MD dataset:

- WT plus 12 tagged A89 2C `112-321` systems;
- 3 independent replicas per system;
- 39 / 39 replicas reached 20 ns;
- 780 ns total legacy production sampling.

Task 010 then corrected the decision-changing analysis/protocol issues:

- explicit PBC unwrap/center handling;
- GROMACS-native RMSD cross-validation;
- self-drift versus common WT-reference RMSD separation;
- junction-matched WT local RMSF;
- WT-defined contact retention;
- true tag SASA and corrected nonlocal tag contact;
- replica/time-block/truncation analysis;
- dynamic-network evidence downgraded to exploratory;
- CHARMM36 nonbonded protocol audit/correction.

Corrected-protocol validation added:

- 6 systems x 3 independent replicas x 20 ns;
- 18 / 18 trajectories completed and passed trajectory/energy QC;
- Slurm job `164594`;
- 360 ns corrected-protocol production sampling.

Legacy and corrected-protocol ensembles remain separate evidence sets and are not concatenated as if they were one homogeneous simulation ensemble.

## Current Task 010A Candidate Panel

Current V5 classes after 010A cleanup:

- Priority A: `289|290 x MAP8`, `289|290 x G196_minimal`, `248|249 x HA`, `248|249 x MAP8`.
- Priority B: `288|289 x MAP8`, `288|289 x HA`, `290|291 x MAP8`.
- Conflict controls: `224|225 x MAP8`, `224|225 x HA`, `203|204 x G196_minimal`, `256|257 x MAP8`.
- Hard-negative control: `155|156 x MAP8`.

Current authoritative files:

- `data/final_candidate_panel_v5_experimental_review_cleanup.tsv`
- `data/experimental_review_shortlist_v1.tsv`
- `docs/FINAL_SCIENTIFIC_CLEANUP_010A.md`
- `docs/EXPERIMENTAL_REVIEW_SHORTLIST_V1.md`
- `docs/DYNAMIC_NETWORK_ANALYSIS_V2_AUDITED.md`

V4/V2 corrected-validation files remain parent provenance and are superseded for experimental-review discussion by V5/shortlist outputs.

## Task 010A Cleanup Results

Generated cleanup outputs:

- `results/dynamics_audit_010/differential_block_drift_vs_wt_v1.tsv`
- `results/dynamics_audit_010/final_sampling_decision_v2_cleanup.tsv`
- `results/dynamics_audit_010/tag_nonlocal_contact_replica_heterogeneity_v1.tsv`
- `results/dynamics_audit_010/task010a_internal_consistency_audit_v1.tsv`
- `data/final_candidate_panel_v5_experimental_review_cleanup.tsv`
- `data/experimental_review_shortlist_v1.tsv`
- `docs/FINAL_SCIENTIFIC_CLEANUP_010A.md`
- `docs/EXPERIMENTAL_REVIEW_SHORTLIST_V1.md`

Key cleanup findings:

- Same-direction drift below extension threshold is now recorded separately from extension-trigger drift.
- `289|290 x MAP8` does not show decision-relevant candidate-specific excess drift after WT comparison.
- `248|249 x HA` shows replica-heterogeneous nonlocal tag-contact behavior and remains Priority A with an accessibility/contact heterogeneity caution.
- Priority A/B is explicitly `multi_evidence_expert_adjudication`; no algorithmic total score is used.
- `289|290 x G196_minimal` and `248|249 x MAP8` remain not directly corrected-protocol validated.
- Sampling decision remains `STOP_AT_20NS` at screening level; this is not a claim of full mechanistic convergence.

## Corrected-Protocol Validation Interpretation

Directly corrected-protocol validated:

- `289|290 x MAP8`: MD-neutral/supportive screening classification;
- `248|249 x HA`: MD-neutral/supportive global perturbation classification;
- `256|257 x MAP8`: MD-neutral/supportive but biologically conflicted;
- `224|225 x MAP8`: reproduced high nonlocal tag-contact caution;
- `155|156 x MAP8`: reproduced MD caution and retained as hard negative;
- WT baseline.

Not directly corrected-protocol validated:

- `289|290 x G196_minimal`;
- `248|249 x MAP8`;
- Priority B rows and other controls outside the six-system validation subset.

No corrected-protocol evidence may be imputed to those unsimulated constructs.

## Why Task 010A Is Needed

Scientific review after Task 010 identified four cleanup needs:

1. Same-direction late-vs-early drift can be present even when it does not cross the absolute extension threshold. `directional_drift_metrics=none` therefore overstates absence of drift.
2. For RMSD/contact metrics, candidate drift should be compared against WT fragment relaxation before being interpreted as candidate-specific.
3. `248|249 x HA` shows replica-level heterogeneity in nonlocal tag-contact behavior; a construct mean alone can obscure this.
4. Priority A/B is a multi-evidence expert adjudication framework, not a validated algorithmic total score.

Task 010A therefore creates:

- descriptive directional-drift fields separate from extension-trigger fields;
- candidate-minus-WT differential block drift;
- replica-level tag-contact heterogeneity audit;
- V5 priority-method provenance;
- a practical 4-candidate + 2-control experimental-review shortlist.

## Sampling Boundary

The current Task 010 sampling decision remains `STOP_AT_20NS` for all six directly validated systems unless Task 010A reveals a truly decision-changing candidate-specific excess drift after WT comparison.

Task 010A itself is analysis-only and must not submit new MD.

A 50 ns duration is not a project requirement. Additional sampling would only be justified by a specific unresolved decision-critical signal, not by a round-number duration target.

## Experimental-Review Shortlist

Frozen discussion set:

1. `289|290 x MAP8` — primary C-terminal MAP8 candidate; directly corrected-protocol validated.
2. `289|290 x G196_minimal` — same-site alternative tag comparator; not directly corrected-protocol validated.
3. `248|249 x HA` — primary non-C-terminal HA candidate; directly corrected-protocol validated; review replica contact heterogeneity explicitly.
4. `248|249 x MAP8` — crossed site/tag comparator; not directly corrected-protocol validated.

Controls:

5. `224|225 x MAP8` — corrected-MD conflict control.
6. `155|156 x MAP8` — hard-negative control.

This is intentionally a two-region x two-tag comparison rather than several adjacent C-terminal junctions being counted as independent hypotheses.

## Evidence Hierarchy

Interpret priorities using the existing evidence hierarchy:

1. direct HRV-A89 phenotype, if/when available;
2. direct homolog insertion phenotype;
3. homolog genetics/function;
4. experimentally established functional/structural constraints;
5. A89 structural context;
6. phylogeny/evolution/conservation;
7. PLM;
8. insertion-structure modeling;
9. comparative MD.

MD is downstream perturbation evidence and cannot override stronger direct biological evidence.

## Model Boundary

Current comparative MD is an apo protein-only `112-321` core-fragment screen with an artificial fragment N terminus. It does not represent full-length membrane/RNA/ATP/oligomer biology.

No generic trajectory extension removes that model limitation.

## Completed Task 010A Outputs

- `results/dynamics_audit_010/differential_block_drift_vs_wt_v1.tsv`
- `results/dynamics_audit_010/final_sampling_decision_v2_cleanup.tsv`
- `results/dynamics_audit_010/tag_nonlocal_contact_replica_heterogeneity_v1.tsv`
- `results/dynamics_audit_010/task010a_internal_consistency_audit_v1.tsv`
- `data/final_candidate_panel_v5_experimental_review_cleanup.tsv`
- `data/experimental_review_shortlist_v1.tsv`
- `docs/FINAL_SCIENTIFIC_CLEANUP_010A.md`
- `docs/EXPERIMENTAL_REVIEW_SHORTLIST_V1.md`

Completion state:

`EXPERIMENTAL_REVIEW_SHORTLIST_READY_FOR_DISCUSSION`

## Stop Boundary

Task 010A does not authorize:

- exact nucleotide/codon design;
- wet-lab procedural protocol design;
- additional MD or Slurm/GPU jobs;
- broad membrane/RNA/ATP/antibody mechanistic MD;
- claims of safety/validation;
- merge to `main`.

Before nucleotide-level construct design, obtain the exact experimental HRV-A89 2C/replicon/plasmid nucleotide context.
