# BROAD_DYNAMICS_AND_RECOVERY_009

Status: **AUTHORIZED / PRE-DYNAMICS RECOVERY + BROAD REPLICATED DYNAMICS**

Date: 2026-08-24

Branch: `analysis/broad-dynamics-009`

## Mission

Convert the diversified candidate-panel checkpoint from `CANDIDATE_PANEL_EXPANSION_008` into a more robust, dynamics-informed experimental candidate panel while explicitly resolving the important unfinished technical items from task 008.

This task must **not** simply run MD on the existing nine-row proposal. It must first repair the remaining technical/QC gaps, correct C-terminal and tag-family selection bias, test a small number of additional realistic tag architectures, then execute broad replicated comparative dynamics on a balanced candidate/control set.

The final computational deliverable remains a **ranked, redundant, multi-junction × multi-tag candidate panel**, not one claimed best insertion site.

No result from this task may be described as experimentally validated or safe.

---

## Entering scientific state

`CANDIDATE_PANEL_EXPANSION_008` completed with:

`READY_FOR_BROAD_TARGETED_DYNAMICS`

Important inherited facts:

- draft panel: 8 Tier A, 8 Tier B, 2 controls;
- Tier A spans 6 junctions and 3 core tag systems, but 6/8 Tier A constructs come from the contiguous `287|288–290|291` C-terminal neighborhood;
- MAP8 is over-represented in the proposed dynamics panel;
- expanded ColabFold replication completed for 18 constructs / 36 model rows;
- OpenMM QC completed for 35/36 rows;
- one `248|249 × HA` model failed OpenMM with `Particle coordinate is nan`;
- local dimer/trimer tagged multimer modeling was deferred;
- disorder/disordered-binding prediction remained incomplete because IUPred2A/ANCHOR2 was unavailable;
- PA14 and AGIA were reviewed but did not yet enter real inserted-structure modeling;
- exact experimental nucleotide/RNA context remains unavailable and remains outside the present task.

---

# Core scientific decisions for task 009

## 1. Dynamics is comparative perturbation evidence, not biological validation

The purpose of dynamics is to compare the persistence of native-like structure, local flexibility, tag exposure and contact/network behavior between candidate constructs under one standardized computational state.

It is not evidence of viral replication competence, membrane localization, RNA translocation or successful antibody binding in cells.

## 2. Do not use full-length 2C in bulk aqueous MD as the primary screening system

The N-terminal region of full-length 2C is membrane-associated. A long unbiased full-length monomer simulation in bulk water would introduce a major non-physiological confound unrelated to the tag-selection question.

For broad comparative candidate screening, use a **soluble comparative segment containing native HRV-A89 2C residues 112–321**, with neutral terminal treatment/capping where technically supported and with the exact inserted tag retained.

Rationale:

- all 009 candidate/control insertion junctions are within this segment;
- it retains the ATPase core and C-terminal oligomer/RNA-related region;
- it avoids making the membrane-associated N terminus a dominant artifact;
- it is explicitly a comparative perturbation assay, not a model of the complete biological state.

Use an equivalent WT `112–321` reference system.

If robust neutral terminal capping cannot be implemented in the chosen GROMACS force-field workflow, document the issue and use the most defensible consistent terminal treatment across WT and all constructs. Do not mix terminal treatments between constructs.

## 3. Prefer independent replicas over one long trajectory

Use multiple independent replicas with randomized initial velocities.

Default screening target:

- **3 independent replicas × 50 ns production per construct** after standard minimization/equilibration;
- WT reference under the same protocol;
- if resource/time constraints materially prevent this, complete at least 3 × 20 ns for every panel member before extending selected systems;
- candidates with unstable/inconclusive rank may receive two additional replicas or continuation only after the broad panel has minimum coverage.

Never substitute one long single trajectory for replicate breadth.

## 4. Standardize the force field and solvent model

Use one protein force-field/water combination for the broad comparison.

Preferred primary choice: **CHARMM36m + the compatible GROMACS water model** when available in the current installation/environment because the candidate question includes flexible inserted peptides and native folded structure.

If CHARMM36m is not available reproducibly, use a mature widely accepted GROMACS protein force field consistently across all systems and document the exact choice and rationale.

Do not compare candidate rankings across mixed force fields in the primary table.

## 5. Broad screening is apo and comparative

Do not introduce ATP/Mg, RNA, membrane, antibody/nanobody or 9A5 into the broad screening systems unless a later explicitly authorized mechanistic task does so.

The current task measures tag-induced perturbation under one standardized protein-only state. Ligand/membrane/RNA states are later mechanism-specific sensitivity analyses.

---

# Stage 0 — repository, branch, storage, scheduler and software audit

Before computation:

1. confirm branch `analysis/broad-dynamics-009`;
2. verify task 008 outputs and checksums/row counts;
3. inspect storage, quota and inodes;
4. inspect Slurm GPU partitions/nodes;
5. inventory existing GROMACS, ColabFold, OpenMM, MDAnalysis, MDTraj, DSSP, US-align/TM-align and disorder-prediction tools;
6. reuse existing working environments and caches when possible rather than reinstalling functioning software.

Create:

- `results/broad_dynamics_009/environment_inventory.tsv`
- `results/broad_dynamics_009/input_integrity_qc.tsv`

Preferred scheduler behavior:

- orchestrate from the login node;
- use non-interactive `sbatch` jobs for GPU work;
- prefer a known working RTX3090 partition when current scheduler state is comparable;
- do not require GPU visibility on `admin1`;
- continue CPU work while jobs wait.

---

# Stage 1 — resolve the 008 OpenMM NaN failure

Target:

`248|249 × HA`

The 008 failure `Particle coordinate is nan` must be treated first as a numerical/structure-QC problem, not as biological evidence.

For the failing model:

1. identify the exact model/seed from the manifest;
2. validate all input coordinates for NaN/Inf and extreme coordinates;
3. check duplicate atoms, alternate locations, missing heavy atoms, abnormal residue naming, zero-length bonds, atom overlaps and topology-building warnings;
4. compare the failing model with the successful `248|249 × HA` model/seed;
5. attempt repair with open reproducible tools such as PDBFixer/OpenMM preparation or equivalent structural sanitation;
6. repeat minimization under a controlled CPU platform;
7. if needed, attempt a more conservative staged minimization before the original protocol;
8. preserve the original failure record.

Classify the final result as exactly one of:

- `NUMERICAL_INPUT_DEFECT_RESOLVED`
- `MODEL_SPECIFIC_GEOMETRY_FAILURE`
- `REPRODUCIBLE_GEOMETRY_INSTABILITY`
- `UNRESOLVED_OPENMM_NUMERICAL_FAILURE`

Create:

- `results/broad_dynamics_009/openmm_248_249_HA_root_cause.tsv`
- `docs/OPENMM_248_249_HA_FAILURE_AUDIT.md`

Do not promote or demote the biological candidate solely from an implementation error.

---

# Stage 2 — recover the missing disorder/flexibility layer

The 008 matrix retained missing disorder/disordered-binding fields because IUPred2A/ANCHOR2 was not present.

Attempt a reproducible user-space installation of IUPred2A/ANCHOR2 **only if it is available under acceptable non-restricted terms without manual credential/license acquisition**.

If that path is not practical, use a mature open disorder predictor such as `metapredict` or another documented open alternative.

Requirements:

- record exact method/version;
- calculate residue-level disorder probabilities for WT A89 2C;
- derive junction-level local-window disorder summaries for all 320 junctions;
- if an ANCHOR-like binding propensity cannot be reproduced, leave that specific column NA rather than fabricating a substitute;
- do not mix outputs from different predictors as if numerically equivalent.

Create:

- `data/hrvA89_2C_disorder_v1.tsv`
- `data/junction_feature_matrix_v7_pre_dynamics.tsv`
- `docs/DISORDER_LAYER_RECOVERY_V1.md`

This remains a supporting prior, not a hard exclusion layer.

---

# Stage 3 — complete local tagged multimer accommodation modeling

Task 008 deferred local dimer/trimer modeling. Recover this now using the already working open ColabFold environment.

Primary objective:

Test whether rigid placement into the WT hexamer systematically overestimates or underestimates local inter-protomer conflict.

Use a tractable focused panel including at minimum:

- `289|290 × MAP8`
- `289|290 × G196_minimal`
- `288|289 × HA`
- `224|225 × HA`
- `248|249 × MAP8`
- `256|257 × MAP8` as oligomer-disfavored control

Add additional constructs if resources permit.

Use local dimer and/or trimer contexts derived from the existing A89 hexamer hypotheses. Keep chain identities/protomer orientation auditable.

For each model record:

- multimer sequence composition;
- MSA pairing/unpaired mode;
- model type;
- seeds;
- interface confidence metrics when available;
- tagged-protomer native-domain deviation;
- tag-neighbor minimum distance;
- inter-protomer clash count;
- interface contact loss/gain;
- whether neighboring protomers accommodate the tag relative to rigid placement;
- consistency across the two existing hexamer hypotheses where applicable.

Create:

- `data/local_multimer_tag_context_v2.tsv`
- `results/broad_dynamics_009/local_multimer_manifest.tsv`
- `docs/LOCAL_MULTIMER_RECOVERY_V2.md`

A failed multimer method must not block later dynamics if adequate monomer and rigid-context evidence exists; record explicit status instead.

---

# Stage 4 — focused expansion of realistic tag diversity

Task 008 reviewed new tags but the actual modeled panel still uses only MAP8, HA and G196 forms.

Add a **focused exploratory structure screen** for two additional realistic tag systems with fixed sequences already documented in `data/tag_portfolio_v2.tsv`:

- `PA14` = `EGGVAMPGAEDDVV`
- `AGIA` = `EEAAGIARP`

Do not model them across all 320 sites.

Use representative junctions that span distinct site regions, preferably:

- `224|225`
- `248|249`
- `288|289`
- `289|290`

For each tag × site construct:

- run at least two ColabFold seeds/models if feasible;
- compute the same structural perturbation, OpenMM QC, tag exposure and rigid/local oligomer-context metrics used for core tags;
- annotate binder/reagent feasibility separately from structural tolerance;
- do not automatically promote PA14/AGIA into the dynamics panel merely because they are new.

Create:

- `data/exploratory_tag_structure_panel_v1.tsv`
- `data/exploratory_tag_structure_metrics_v1.tsv`
- `docs/EXPLORATORY_TAG_SCREEN_V1.md`

ALFA and HiBiT remain feasibility-only unless a concrete experimental detection strategy is explicitly chosen later.

---

# Stage 5 — rebalance the dynamics panel before execution

Do not use `data/proposed_targeted_dynamics_panel_v1.tsv` unchanged.

Construct a new balanced panel:

- `data/balanced_targeted_dynamics_panel_v2.tsv`

Panel design target:

- approximately **10–12 tagged constructs plus one WT reference**;
- at least **4 genuinely distinct site regions**, not merely adjacent junctions counted as independent sites;
- at least **3 tag systems**;
- no more than approximately half of candidate constructs from the `287–291` C-terminal neighborhood unless new evidence strongly justifies otherwise;
- at least one hard-negative/control and one mechanistic conflict control.

Mandatory or strongly preferred representatives:

### Current leaders / local tag comparison
- `289|290 × MAP8`
- `289|290 × G196_minimal`

### C-terminal neighborhood alternatives
Select only enough to test local positional sensitivity, for example:
- `288|289 × HA` and/or `288|289 × MAP8`
- `290|291 × MAP8`

### Independent non-C-terminal candidates
Include multiple of:
- `224|225 × HA`
- `224|225 × MAP8`
- `248|249 × MAP8`
- `248|249 × HA` only if the NaN audit supports valid geometry
- `203|204 × G196_minimal` as a mechanistically informative secondary/conflict candidate

### Controls
- `256|257 × MAP8` as oligomer-context conflict control
- `155|156 × MAP8` as hard-negative control if computational budget permits

### Exploratory new tags
If PA14 or AGIA clearly survives the focused structure/binder/oligomer screen, include at most one or two of the strongest new-tag constructs so that dynamics can test whether the broader tag family changes the ranking.

Every panel member must have a `selection_rationale_pre_MD` column frozen before MD results are generated.

---

# Stage 6 — install/configure the dynamics analysis stack

Use open/reproducible software only.

Required or recommended tools:

- GROMACS 2024.x or the best working cluster module;
- CHARMM36m-compatible topology files if available reproducibly;
- MDAnalysis;
- MDTraj;
- NumPy/SciPy/pandas;
- DSSP or MDTraj DSSP implementation;
- NetworkX for residue-network/community calculations;
- PyEMMA is optional and not required;
- PDBFixer/OpenMM for structure sanitation where needed;
- plotting/report dependencies as required.

Do not install large unnecessary databases.

Create:

- `envs/broad_dynamics_009.yml` or equivalent;
- `results/broad_dynamics_009/software_versions.tsv`.

---

# Stage 7 — prepare standardized WT and tagged dynamics systems

Primary comparative segment:

**native A89 2C residues 112–321**

For each tagged construct:

- preserve the inserted tag exactly at the intended junction;
- maintain an explicit mapping from simulation residue numbers to native A89 residue numbers and tag residues;
- use the same extraction/capping/terminal-treatment logic for WT and every tagged system;
- do not accidentally interpret inserted tag residue numbering as shifted native numbering.

System preparation requirements:

- consistent force field;
- consistent solvent model;
- explicit solvent;
- neutralization and consistent physiological-range ionic strength if used;
- sufficiently large periodic box to prevent self-interaction;
- steepest-descent minimization;
- short restrained NVT equilibration;
- short restrained NPT equilibration;
- independent randomized velocities per replica;
- production without artificial restraints on the insertion region.

Record all `.mdp` files, topology provenance and exact commands.

Create:

- `results/broad_dynamics_009/system_manifest.tsv`
- `results/broad_dynamics_009/residue_mapping.tsv`
- `results/broad_dynamics_009/preproduction_qc.tsv`

A system may proceed to production only if topology, finite coordinates, energy minimization, temperature and pressure QC pass.

---

# Stage 8 — broad replicated production dynamics

Primary target:

**3 independent replicas × 50 ns per system**.

If cluster availability or wall time prevents full 50 ns completion in one execution:

1. obtain at least 3 × 20 ns for every panel member first;
2. then extend all or the most informative systems consistently;
3. never leave one favored construct with dramatically deeper sampling while other candidates have only one short trajectory unless this is explicitly marked as an adaptive second phase.

Use Slurm job arrays or otherwise auditable non-interactive jobs.

Avoid holding GPUs while Codex is reasoning.

Store:

- compact logs;
- checkpoint files;
- trajectories required for analysis;
- no unnecessary duplicate trajectory formats.

Do not commit bulk trajectories to GitHub.

Commit manifests, scripts, compact metrics and reports only.

Create:

- `results/broad_dynamics_009/production_manifest.tsv`
- `results/broad_dynamics_009/replica_completion.tsv`

---

# Stage 9 — trajectory QC and convergence

Before biological interpretation, evaluate per replica:

- simulation completion and frame count;
- temperature and pressure stability;
- potential energy behavior;
- native-domain backbone RMSD;
- radius of gyration as a gross QC metric;
- finite coordinates/no PBC corruption;
- replica-to-replica consistency;
- time-block stability;
- effective comparison window after equilibration.

Exclude a trajectory from quantitative ranking only for explicit technical QC failure, and preserve the failure record.

Create:

- `data/dynamics_replica_qc_v1.tsv`
- `docs/DYNAMICS_QC_V1.md`

---

# Stage 10 — candidate-specific dynamics readouts

For every WT and tagged replica calculate, with native/tag mapping handled explicitly:

## Native structural persistence
- native 2C segment backbone RMSD;
- per-residue RMSF;
- local insertion-window RMSF;
- local secondary-structure persistence;
- native contact retention/loss;
- local contact retention/loss.

## Tag behavior
- tag RMSF;
- tag SASA/exposure over time;
- tag-native minimum distance distribution;
- tag collapse/burial frequency;
- local persistent clash/proximity events;
- end-to-end distance for tags where this is structurally meaningful.

## Functional-neighborhood context
Measure perturbation propagation toward relevant ATPase/RNA/oligomerization neighborhoods without claiming functional inhibition.

## Ensemble statistics
For every metric report:

- per-replica value;
- mean/median across replicas;
- dispersion;
- bootstrap confidence intervals where meaningful;
- effect relative to WT;
- effect relative to negative/conflict controls.

Create:

- `data/broad_dynamics_metrics_v1.tsv`
- `data/tag_exposure_dynamics_v1.tsv`
- `data/contact_persistence_dynamics_v1.tsv`

---

# Stage 11 — dynamic network and correlation analysis

For the balanced panel, perform a transparent dynamic network analysis using native-residue mappings.

At minimum:

- dynamic cross-correlation or covariance-based coupling;
- residue contact-network persistence;
- community structure changes where stable/reproducible;
- shortest/communication-path changes from insertion neighborhood toward ATPase/RNA/interface regions;
- replicate consistency of network conclusions.

Do not overinterpret small changes from one trajectory.

Create:

- `data/dynamic_network_perturbation_v1.tsv`
- `docs/DYNAMIC_NETWORK_ANALYSIS_V1.md`

---

# Stage 12 — integrate dynamics into candidate ranking

Update the candidate panel without using one hidden weighted total score.

Create:

- `data/final_candidate_panel_v2_dynamics.tsv`
- `results/broad_dynamics_009/ranking_robustness_v2.tsv`

Retain separate evidence axes for:

- hard biological constraints;
- direct homolog insertion phenotype;
- substitution/deletion context;
- conservation/natural indels;
- disorder/flexibility prior;
- RNA-holoenzyme context;
- protease/polyprotein risk;
- PLM;
- static inserted-structure ensemble;
- OpenMM QC;
- binder accessibility;
- rigid and local multimer context;
- replicated dynamics;
- dynamic network perturbation;
- unresolved conflicts.

Use:

- Pareto/non-dominated membership;
- evidence classes;
- leave-one-layer-out sensitivity;
- bootstrap/rank stability where meaningful;
- explicit site-region diversity checks;
- explicit tag-family diversity checks.

Do not let adjacent `287–291` junctions masquerade as many independent biological regions in the final diversity summary.

---

# Stage 13 — final panel format

The task should end with a revised candidate package, not one winner.

Target final draft:

- **Tier A:** approximately 6–10 primary constructs;
- **Tier B:** approximately 6–12 secondary/rescue constructs;
- **Controls:** approximately 4–6 conflict/hard-negative constructs.

Required views:

- junction-level ranking;
- site × tag ranking;
- site-region ranking;
- best tags per junction;
- best junctions per tag;
- candidate diversity summary;
- candidate uncertainty summary.

Create:

- `docs/BROAD_DYNAMICS_AND_RECOVERY_009_REPORT.md`

The report must answer:

1. Was the `248|249 × HA` OpenMM NaN failure numerical, model-specific or reproducible?
2. Was the missing disorder layer recovered, and with which method?
3. Did local multimer modeling materially change rigid-placement conclusions?
4. Did PA14 or AGIA produce any construct competitive with the core tags?
5. What balanced dynamics panel was actually simulated, and why?
6. Were at least 3 independent replicas obtained per system?
7. Which candidates remain stable across replicas rather than only in one trajectory?
8. Which constructs retain persistent tag exposure?
9. Which constructs show elevated local/native perturbation relative to WT?
10. Which candidates show dynamic/network perturbation reaching functional neighborhoods?
11. Did dynamics change the ordering among `288|289`, `289|290` and `290|291`?
12. Did non-C-terminal candidates such as `224|225` and `248|249` remain competitive?
13. Is the final Tier A still excessively C-terminal or MAP8-biased?
14. What are the final Tier A / Tier B / control sets after dynamics?
15. What remaining uncertainty can only be resolved by exact nucleotide/RNA context or HRV-A89 wet-lab phenotype?

---

# Continuity policy for long unattended execution

Do not stop the whole task because:

- one optional disorder tool fails;
- one ColabFold multimer job fails;
- one OpenMM structure fails;
- one GROMACS replica fails;
- one GPU partition is busy;
- one compute node lacks internet;
- GitHub push temporarily fails.

For each failure:

1. record it;
2. attempt reasonable recovery;
3. continue independent work;
4. resubmit only the failed job where appropriate;
5. preserve partial results;
6. never silently drop failed replicas from the ranking.

Use login-node network access for installs/downloads and Slurm compute nodes for GPU execution when needed.

Do not require the VSCode/Codex UI session itself to stay connected for already submitted Slurm jobs. Persist job IDs, logs, manifests and checkpoints in the repository/shared filesystem so work survives client disconnects.

---

# Repository updates

Before completion update consistently:

- `PROJECT_STATE.md`
- `ACTIVE_TASK.md`
- `TODO.md`
- `ANALYSIS_INDEX.md`
- `DECISIONS.md`

Commit scripts, configuration, compact results and reports.

Do not commit bulk MD trajectories, model checkpoints, software caches or large databases.

Push to:

`origin analysis/broad-dynamics-009`

when network access permits.

---

# Final task state

Return exactly one of:

- `READY_FOR_FINAL_CANDIDATE_PANEL_REVIEW`
- `READY_FOR_EXACT_NUCLEOTIDE_AUDIT`
- `BROAD_DYNAMICS_PARTIALLY_COMPLETE`

Do not automatically proceed to wet-lab construct design, RNA/codon design, membrane/RNA/ATP mechanistic MD or experimental protocol design after this task.
