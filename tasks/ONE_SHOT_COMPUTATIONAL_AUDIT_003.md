# ONE_SHOT_COMPUTATIONAL_AUDIT_003

Status: **AUTHORIZED / LONG-RUN COMPUTATIONAL TASK**

Date: 2026-08-22

Branch: `analysis/conservation-002`

## Purpose

Execute the maximum scientifically justified **computational** work that can be completed unattended on the 3090 server, while preserving the current evidence hierarchy and stopping before experimental protocol design or any irreversible biological conclusion.

The task supersedes `METHOD_HARDENING_002` as the active execution wrapper but incorporates all of its modules.

Current project state:

`NO_HIGH_CONFIDENCE_TARGETED_SITE_YET`

## Read first

1. `AGENTS.md`
2. `WORKFLOW.md`
3. `PROJECT_STATE.md`
4. `ACTIVE_TASK.md`
5. `tasks/ONE_SHOT_COMPUTATIONAL_AUDIT_003.md`
6. `tasks/METHOD_HARDENING_002.md`
7. `docs/METHOD_GAP_AND_NEXT_EVIDENCE_AUDIT_V2.md`
8. `docs/EV71_2C_DIRECT_INDEL_MAPPING_V1.md`
9. `docs/CONSERVATION_SCREEN_V2.md`
10. `DECISIONS.md`
11. `ANALYSIS_INDEX.md`
12. `TODO.md`

## Global rules

- Work only on `analysis/conservation-002`.
- Reuse existing verified datasets and mappings whenever possible.
- Do not overwrite versioned V1/V2/V3 outputs.
- Do not label any junction safe, validated, or experimentally proven for HRV-A89.
- Do not treat the EV-A71 8-aa insertion phenotype as universal proof of A89 intolerance.
- Do not collapse all evidence into a single opaque weighted score.
- Do not begin experimental protocol design.
- Do not perform final RNA/codon design without the exact experimental nucleotide construct.
- Do not start long molecular dynamics simulations.
- If a mature standard package is required and missing, install it in user space with a reproducible environment; do not silently replace it with a materially weaker ad hoc approximation.
- Use the 3090 GPU when a mature PLM or structure-prediction step benefits from it; CPU-only tasks should not block on GPU availability.

# STAGE A — METHOD_HARDENING_002 IN FULL

Complete every module from `tasks/METHOD_HARDENING_002.md`.

## A1. EV-A71 substitution-tolerance integration

Required outputs:

- `data/evA71_2C_substitution_tolerance_to_A89_v1.tsv`
- `results/method_hardening_002/substitution_mapping_qc.tsv`

Requirements:

- substitution and insertion/deletion remain separate evidence layers;
- derive transparent flanking and local-window substitution summaries;
- preserve mapping confidence and missingness;
- audit focal regions and all 320 junctions.

## A2. Continuous/Pareto all-320 re-ranking

Required outputs:

- `data/pareto_junction_frontier_v1.tsv`
- `results/method_hardening_002/pareto_sensitivity.tsv`

Requirements:

- all 320 junctions retained except hard biological exclusions;
- `strict_structural_pass` remains annotation only;
- document directionality/scaling/missing-value handling;
- evaluate sensitivity across defensible metric subsets;
- report Pareto/non-dominated classes rather than one hidden score.

## A3. Phylogeny-aware independent natural-indel analysis

Required outputs:

- `data/hrvA_independent_indel_events_v1.tsv`
- `results/method_hardening_002/phylogeny_qc.tsv`
- `docs/PHYLOGENY_AWARE_INDEL_V1.md`

Requirements:

- use the curated CONSERVATION_002 HRV-A panel;
- build/reuse a defensible phylogeny;
- infer independent events rather than descendant counts only;
- explicitly mark uncertain ancestral-state calls.

## A4. MAP8 / HA / G196 tag-specific PLM insertion scan

Required outputs:

- `data/tag_specific_plm_scores_v1.tsv`
- `results/method_hardening_002/plm_qc.tsv`
- `docs/TAG_SPECIFIC_PLM_SCAN_V1.md`

Requirements:

- record exact tag amino-acid sequences/forms before scoring;
- if G196 form is ambiguous, represent minimal and practical/flanked forms separately rather than silently choosing one;
- generate all-320 WT-vs-inserted A89 sequences for each justified tag form;
- use a mature indel-aware PLM if feasible, otherwise a carefully documented ESM-family pseudo-log-likelihood method;
- keep tag-specific landscapes separate;
- record model/checkpoint/software/version/GPU details;
- perform internal reproducibility/QC checks on a subset of sequences.

## A5. Integrated V4 matrix and report

Required outputs:

- `data/candidate_junctions_v4_method_hardening.tsv`
- `docs/METHOD_HARDENING_002_REPORT.md`

The V4 matrix must retain separate evidence columns for:

- functional constraints;
- historical insertion/genetics evidence;
- EV-A71 insertion phenotype;
- EV-A71 deletion context;
- EV-A71 substitution tolerance;
- continuous structural metrics;
- HRV-A conservation;
- natural-indel category;
- phylogeny-aware independent-indel metrics;
- MAP8/HA/G196 PLM scores;
- strict structural annotation;
- Pareto class;
- mapping/QC flags;
- unresolved conflicts.

# STAGE B — ROBUSTNESS / NEGATIVE-CONTROL AUDIT

Do not stop after producing V4. Run a robustness audit designed to detect whether the ranking is unstable or driven by one arbitrary analysis choice.

Required work:

1. Compare candidate classes under multiple reasonable Pareto metric subsets.
2. Repeat ranking with and without descriptive conservation metrics.
3. Repeat ranking with and without EV-A71 substitution-tolerance summaries while keeping direct insertion evidence fixed.
4. Quantify how often each junction remains Pareto-reviewable across sensitivity settings.
5. Explicitly inspect known high-risk negative-control regions to verify that the framework does not spuriously promote them.
6. Explicitly inspect the old strict cluster and literature-rescue controls.

Required outputs:

- `results/one_shot_003/ranking_robustness.tsv`
- `results/one_shot_003/negative_control_audit.tsv`
- `docs/RANKING_ROBUSTNESS_AUDIT_V1.md`

# STAGE C — CROSS-TAG CONSENSUS / DISAGREEMENT ANALYSIS

Using the PLM results, quantify whether MAP8, HA and G196 prefer the same junction neighborhoods.

Required analyses:

- rank-correlation among tag-specific PLM landscapes;
- identify junctions consistently favorable across tags;
- identify tag-specific outliers;
- identify sites where minimal G196 differs substantially from larger tags;
- compare PLM tag-specific patterns against EV-A71 direct insertion phenotype and continuous structural metrics;
- do not interpret PLM agreement as proof of biological tolerance.

Required outputs:

- `data/tag_specific_consensus_v1.tsv`
- `results/one_shot_003/tag_landscape_correlations.tsv`
- `docs/TAG_SPECIFIC_CONSENSUS_V1.md`

# STAGE D — REDUCED COMPUTATIONAL REVIEW SET

After Stages A–C, construct a reduced **computational review set**, not an experimental recommendation.

The set should include distinct evidence classes, for example:

- Pareto-reviewable sites newly identified outside the old strict 10, if any;
- one or more old `287|288–290|291` conflict controls if they remain informative;
- `248|249` / `256|257` historical-conflict controls if still informative;
- at least one negative-control site or region;
- tag-specific outliers if they are scientifically interpretable.

Do not force a fixed number if evidence does not support it. Prefer a compact set suitable for future insertion-specific structural modeling.

Required outputs:

- `data/computational_review_set_v1.tsv`
- `docs/COMPUTATIONAL_REVIEW_SET_V1.md`

Each row must state why it is retained and what conflict/uncertainty it represents.

# STAGE E — OPTIONAL LIGHTWEIGHT STRUCTURAL FEASIBILITY TRIAGE

This stage is authorized only if Stages A–D identify a compact review set and the necessary mature software is already available or can be installed reproducibly without derailing the run.

Goal: perform **lightweight insertion-specific structural feasibility triage**, not final structural modeling.

Allowed scope:

- generate inserted protein sequences for the reduced computational review set;
- use a mature structure-prediction or loop-remodeling workflow to perform limited ensemble comparison;
- prioritize the 3090 GPU where useful;
- compare WT versus inserted constructs using local/global structural perturbation metrics;
- use current A89 hexamers only for comparative clash/interface context, not as proof of native pore geometry.

Do not launch long MD.

Suggested analyses:

- multiple seeds/models rather than one structure;
- local backbone displacement;
- native-domain RMSD;
- gross clash detection;
- tag exposure;
- interface proximity;
- convergence across models;
- separate inserted-tag confidence from native 2C perturbation.

If this stage cannot be performed with a mature/reproducible method, mark it `DEFERRED` rather than substituting a weak custom approximation.

Suggested outputs if completed:

- `data/lightweight_structural_triage_v1.tsv`
- `docs/LIGHTWEIGHT_STRUCTURAL_TRIAGE_V1.md`
- small selected derived structures only when justified and repository-size appropriate.

# STAGE F — FINAL SYNTHESIS

Create:

- `docs/ONE_SHOT_COMPUTATIONAL_AUDIT_003_REPORT.md`

This report must answer:

1. Did any junction outside the previous strict 10 become robustly Pareto-reviewable?
2. Did EV-A71 substitution tolerance materially change site interpretation?
3. Did phylogeny-aware independent-indel reconstruction change the earlier V2 indel conclusions?
4. How different are MAP8, HA and G196 tag-specific PLM landscapes?
5. Are the old `287|288–290|291` sites still scientifically useful as conflict controls?
6. Are `248|249` and `256|257` still useful historical-conflict controls?
7. Is the candidate landscape robust to reasonable metric choices?
8. What reduced computational review set should be taken into future structure modeling?
9. If lightweight structural triage ran, did it materially change the review set?
10. Does the evidence support `READY_FOR_CONFLICT_AWARE_TAG_SITE_MODELING`, `NO_HIGH_CONFIDENCE_TARGETED_SITE`, or `METHOD_HARDENING_BLOCKED`?
11. What exact unresolved uncertainties remain?

# REQUIRED REPOSITORY UPDATES

Before finishing, update consistently:

- `PROJECT_STATE.md`
- `ACTIVE_TASK.md`
- `TODO.md`
- `ANALYSIS_INDEX.md`
- `DECISIONS.md`

Add or update reproducibility metadata for environments, software, and commands.

# GIT / CHECKPOINT POLICY

Because this is intended as an unattended run, create logical checkpoint commits after major stages when appropriate, for example:

- Stage A completed
- Stage B/C completed
- Stage D/E completed
- Final synthesis completed

Do not commit package caches, model checkpoints, large temporary predictions, or bulk structure ensembles.

If remote push is available and already configured, push checkpoint commits to `origin analysis/conservation-002` after each major stage. If push fails, continue local work and record the exact failure in the final report; do not discard completed work.

# STOP CONDITIONS

Stop only after all mandatory Stages A–D and F are complete, or a documented blocker makes completion impossible.

Stage E is optional and may be deferred.

Do not start long MD, experimental protocol design, or final nucleotide/RNA construct design.

Final state must be exactly one of:

- `READY_FOR_CONFLICT_AWARE_TAG_SITE_MODELING`
- `NO_HIGH_CONFIDENCE_TARGETED_SITE`
- `METHOD_HARDENING_BLOCKED`

At task end, print a concise terminal summary containing:

- branch;
- `git status`;
- latest commit SHA;
- created/modified files;
- environments/software used;
- GPU usage where relevant;
- key QC results;
- main scientific findings;
- unresolved blockers;
- final decision state.
