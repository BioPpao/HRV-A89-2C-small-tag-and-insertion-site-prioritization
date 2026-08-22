# CONTINUOUS_TAG_SITE_MODELING_005

Status: **AUTHORIZED / CONTINUITY-FIRST COMPUTATIONAL TASK**

Date: 2026-08-22

Branch: `analysis/conservation-002`

## Purpose

Advance from site-prioritization into conflict-aware, insertion-specific **computational perturbation modeling** for a reduced review set, while preserving task continuity when software, GPU, scheduler, or installation problems occur.

The goal is not to prove a safe insertion site. The goal is to identify which site × tag combinations are comparatively less structurally disruptive and which evidence conflicts remain unresolved.

## Scientific basis

Reuse all completed upstream layers:

- functional constraint map;
- four-structure WT structural metrics;
- HRV-A conservation V2;
- phylogeny-aware independent-indel analysis;
- EV-A71 insertion/deletion/substitution phenotype mapping;
- all-320 Pareto/robustness analysis;
- GPU ESM2 tag-specific PLM scoring;
- `data/candidate_junctions_v5_plm_gpu.tsv`;
- `data/computational_review_set_v2_plm_gpu.tsv`.

Do not restart global all-320 discovery unless a concrete QC error is found.

## Missing/underused computational methods to add now

### Method A — insertion-specific structure-prediction ensembles

For the reduced review set, generate multiple independent predictions for each selected site × tag construct rather than relying on one model.

Preferred mature options, in order of availability:

1. ColabFold/AlphaFold-compatible local workflow;
2. another mature AlphaFold-family local implementation;
3. if unavailable, continue to Method B/C/D rather than stopping the whole task.

Required comparisons:

- WT vs inserted construct;
- local backbone displacement around the junction;
- whole-domain RMSD/TM-style similarity where valid;
- native secondary-structure preservation;
- tag accessibility;
- model-to-model convergence;
- native 2C confidence separated from inserted-tag confidence.

### Method B — loop/backbone feasibility modeling

Use a mature loop-remodeling or conformer-sampling method if available, for example Rosetta Remodel/KIC-like workflows or another established loop-closure package.

Outputs should emphasize:

- closure success/failure;
- conformer diversity;
- local strain/energy proxies;
- severe steric clashes;
- preservation of native local geometry.

If Rosetta/PyRosetta installation is unavailable, do not stop the full task. Mark this method `DEFERRED_SOFTWARE` and proceed to Methods C/D/E.

### Method C — local energetic/frustration analysis

Add an orthogonal energetic perturbation layer using a mature method where available, such as:

- FoldX-like local stability/interaction analysis;
- Rosetta score terms on generated models;
- local frustration analysis or another established residue-level energetic diagnostic.

Use only as a relative secondary signal. Do not interpret energy values as direct viral fitness.

If one package fails, attempt another mature method or skip this module with explicit provenance; continue the task.

### Method D — oligomer-context compatibility

Place/compare the reduced inserted constructs in the existing A89 hexamer-context hypotheses and quantify relative changes in:

- inter-protomer steric clashes;
- insertion proximity to neighboring protomers;
- interface-contact loss/gain;
- local pore-facing orientation as a context metric only;
- C-terminal or other known interface-region disturbance.

Do not claim the current no-membrane/no-RNA hexamers are the native functional state.

### Method E — structural-neighborhood graph/network perturbation

Add a residue-contact-network comparison between WT and inserted models where practical.

Possible metrics:

- contact-map difference;
- local degree/betweenness changes;
- disruption of known functional-neighborhood connectivity;
- propagation of perturbation away from the insertion site.

This is an orthogonal topology layer and must not override direct functional/phenotype evidence.

### Method F — orthogonal evolutionary/statistical validation

Do not rerun the existing phylogeny pipeline blindly. Add only targeted orthogonal checks where useful, such as:

- phylogeny-aware site-rate estimation for the reduced local windows;
- coevolution/direct-coupling context if a mature method and adequate alignment depth are available;
- local disorder/flexibility propensity comparisons.

If alignment depth is insufficient for reliable coevolution, record that and continue.

## Initial reduced review set

Start from `data/computational_review_set_v2_plm_gpu.tsv`.

Do not automatically model every row at equal depth.

Create a transparent compact modeling panel spanning evidence classes, including representatives of:

- old strict C-terminal conflict cluster;
- historical insertion-support / modern-conflict controls;
- outside-strict relatively less-deleterious direct-insertion rows;
- strong PLM secondary-support rows if biologically interpretable;
- at least one hard-exclusion negative control for method calibration.

The panel should remain compact enough for ensemble modeling but broad enough to test conflicting evidence classes.

Create:

- `data/tag_site_modeling_panel_v1.tsv`

Each row must state why it is included and which evidence conflict it tests.

## Tag forms

Use the exact tag forms already fixed in GPU_RECOVERY_004:

- MAP8;
- HA;
- G196_minimal;
- G196_practical_GS where scientifically justified.

Do not silently change tag sequence definitions.

## Continuity-first execution policy

This section is mandatory.

The task must NOT stop merely because one resource, package, GPU, scheduler allocation, or preferred method is unavailable.

Use the following recovery ladder.

### 1. GPU unavailable in current shell

- Detect whether running on a Slurm login node.
- Inspect `sinfo`, `squeue`, and available GPU partitions.
- Submit or enter a suitable GPU allocation when needed.
- Any visible CUDA-capable GPU is acceptable unless a method has a specific hardware requirement.
- Continue CPU-capable analysis while waiting for GPU allocation when useful.

### 2. Preferred package unavailable

- Check whether it is already installed elsewhere in user/project paths or modules.
- Check environment modules where available.
- Install a reproducible user-space environment when practical.
- If installation fails because of network/proxy restrictions on compute nodes, prepare/download dependencies from a network-capable login context and reuse them inside the Slurm job.
- If the preferred package remains unavailable, try the next mature method in the same evidence class.
- If no mature substitute exists, mark only that module deferred and continue all independent modules.

### 3. Network unavailable on compute node

- Do not stop immediately.
- Reuse cached models/checkpoints/packages.
- Use the login node only for downloading software/checkpoints when permitted, then execute compute-heavy inference in the allocated GPU job.
- Record provenance/checksums.

### 4. Git push unavailable

- Continue analysis locally.
- Commit locally when possible.
- Record the push failure.
- Retry push at the end from a context with network access.
- Never discard completed scientific outputs solely because remote push temporarily fails.

### 5. One method fails

- Continue all independent methods.
- The final report must distinguish `COMPLETED`, `DEFERRED_SOFTWARE`, `DEFERRED_RESOURCE`, and `FAILED_QC` per method.
- Do not convert one local failure into a project-wide blocker unless it prevents any scientifically meaningful continuation.

## Stage 1 — panel construction and environment audit

Required:

- construct `data/tag_site_modeling_panel_v1.tsv`;
- record candidate rationale;
- inventory available GPU/CPU resources;
- inventory installed modeling packages/modules;
- create a method execution plan based on actual availability.

Create:

- `results/tag_site_modeling_005/environment_and_method_inventory.tsv`

## Stage 2 — insertion-specific model ensembles

Run the strongest available mature structure-prediction workflow for the compact panel.

Use multiple models/seeds where supported.

Create versioned structures and a compact metrics table. Do not commit bulk caches/checkpoints.

Primary table:

- `data/tag_site_structure_ensemble_metrics_v1.tsv`

## Stage 3 — loop/energy/network/oligomer analyses

Run as many of Methods B–E as scientifically valid and available.

Create separate outputs rather than mixing metrics into a hidden score, for example:

- `data/tag_site_loop_feasibility_v1.tsv`
- `data/tag_site_energy_context_v1.tsv`
- `data/tag_site_contact_network_v1.tsv`
- `data/tag_site_hexamer_context_v1.tsv`

If a method is deferred, create a small machine-readable status file recording why.

## Stage 4 — evidence integration

Create:

- `data/tag_site_integrated_perturbation_v1.tsv`

Retain separate columns for:

- direct homolog insertion phenotype;
- functional tier;
- structure/Pareto context;
- PLM tag-specific context;
- ensemble structural perturbation;
- loop feasibility;
- energetic context;
- network perturbation;
- oligomer-context perturbation;
- method/QC status;
- unresolved conflicts.

Do not collapse all evidence into a single opaque weighted scalar score.

Use explicit qualitative classes such as:

- `RELATIVELY_LOWER_PERTURBATION__DIRECT_EVIDENCE_CONFLICT`
- `STRUCTURALLY_DISFAVORED`
- `TAG_SPECIFIC_DISAGREEMENT`
- `METHOD_INCONCLUSIVE`
- `NEGATIVE_CONTROL`

## Stage 5 — robustness and cross-method agreement

Quantify whether rankings are stable across structural methods/models.

Required analyses where possible:

- model-seed consistency;
- method-to-method rank agreement;
- sensitivity to excluding one computational layer;
- identification of constructs supported only by one weak method;
- identification of constructs consistently disfavored.

Create:

- `results/tag_site_modeling_005/cross_method_robustness.tsv`

## Final report

Create:

- `docs/CONTINUOUS_TAG_SITE_MODELING_005_REPORT.md`

The report must answer:

1. Which site × tag constructs were actually modeled?
2. Which methods completed, which were deferred, and why?
3. Which constructs show the lowest relative native-2C perturbation across multiple methods?
4. Which constructs are strongly method-dependent or tag-dependent?
5. Do historical conflict sites remain structurally plausible or become clearly disfavored?
6. Do old `287|288–290|291` controls remain useful?
7. Do outside-strict rows such as `203|204` or `224|225` remain plausible after insertion-specific modeling?
8. Does G196_minimal materially reduce perturbation compared with MAP8/HA?
9. Did oligomer-context analysis change interpretation?
10. Is the remaining uncertainty now dominated by missing HRV-A89-specific phenotype rather than computation?

## Final state

Return exactly one of:

- `READY_FOR_TARGETED_DYNAMIC_ANALYSIS`
- `NO_COMPUTATIONAL_CONSENSUS_SITE`
- `TAG_SITE_MODELING_PARTIALLY_COMPLETE`

A partially complete state is valid only when some methods could not be run, but meaningful independent analyses were completed.

## Do not auto-escalate to

- long MD;
- final experimental construct recommendation;
- experimental protocol design;
- final RNA/codon design without the exact experimental construct sequence.

## Repository update requirements

Before completion, update consistently:

- `PROJECT_STATE.md`
- `ACTIVE_TASK.md`
- `TODO.md`
- `ANALYSIS_INDEX.md`
- `DECISIONS.md`

Commit scientifically meaningful outputs and push to `origin analysis/conservation-002` when possible. If push fails, preserve local commits and continue the scientific task.
