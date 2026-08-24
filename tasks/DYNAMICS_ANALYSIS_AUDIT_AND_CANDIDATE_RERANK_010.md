# DYNAMICS_ANALYSIS_AUDIT_AND_CANDIDATE_RERANK_010

Date: 2026-08-24

Branch: `analysis/dynamics-audit-010`

Task state at authorization: `AUTHORIZED_FOR_AUTONOMOUS_SERVER_EXECUTION`

## 0. Mission

Repair the Task 009 MD-analysis defects, reanalyze the existing 39 x 20 ns trajectories with a physically and statistically defensible workflow, audit the CHARMM36 production protocol, and produce a transparent prioritized experimental candidate panel for HRV-A89 2C internal small-tag testing.

The goal is **not** to prove a safe insertion site and **not** to force every trajectory to 50 ns.

The task succeeds when the repository contains a corrected, auditable, multi-evidence candidate priority list whose dynamics component has been repaired, statistically qualified and prevented from overriding stronger biological evidence.

Primary input audit:

- `docs/DYNAMICS_009_POSTHOC_AUDIT_V1.md`

Historical Task 009 outputs must remain preserved as provenance.

## 1. Read order

Before execution, read in this order:

1. `WORKFLOW.md`
2. `AGENTS.md`
3. `PROJECT_STATE.md`
4. `DECISIONS.md`
5. `ANALYSIS_INDEX.md`
6. `ACTIVE_TASK.md`
7. this task specification
8. `docs/DYNAMICS_009_POSTHOC_AUDIT_V1.md`
9. `docs/BROAD_DYNAMICS_AND_RECOVERY_009_REPORT.md`
10. `docs/DYNAMICS_QC_V1.md`
11. `docs/FINAL_CANDIDATE_PANEL_STRATEGY_V1.md`
12. `docs/EV71_2C_DIRECT_INDEL_MAPPING_V1.md`
13. `docs/2C_FUNCTIONAL_EXCLUSION_MAP_V3.md`
14. `data/balanced_targeted_dynamics_panel_v2.tsv`
15. `data/final_candidate_panel_v2_dynamics.tsv`
16. `scripts/broad_dynamics_009_analyze_md.py`
17. `scripts/broad_dynamics_009_gromacs_setup.py`
18. `scripts/broad_dynamics_009_gmx_production.sbatch`
19. `references/LITERATURE_EVIDENCE_REGISTRY.md`

Do not infer current authorization from old stop gates in historical 009 files. This Task 010 explicitly supersedes the 009 review stop gate for the limited scope defined here.

## 2. Non-negotiable scientific rules

1. Preserve all 009 trajectories and outputs. Do not overwrite them.
2. Write corrected outputs under new Task 010 paths/names.
3. No computational site may be called `safe`, `validated`, `functional`, or `WT-equivalent`.
4. Direct biological/genetic evidence outranks MD convenience metrics.
5. EV-A71 direct insertion DMS remains a strong homolog prior, not an absolute A89 veto.
6. `288|289`, `289|290`, and `290|291` are neighboring junctions in one C-terminal biological region and must not count as independent region diversity.
7. MD ranking must remain multi-objective. Do not replace the current heuristic with a new hidden weighted total score.
8. Dynamic-network/DCCM results may provide mechanistic flags only after stability checks.
9. No nucleotide/codon-level construct design without the real experimental sequence.
10. No wet-lab procedural protocol is part of this task.
11. Do not automatically launch membrane/RNA/ATP/antibody mechanistic MD.
12. Do not automatically extend all 39 existing trajectories to 50 ns.

## 3. Required literature/method references

At minimum, preserve these references in the final report and literature registry where absent:

- GROMACS Documentation, Release 2024, CHARMM section: recommended CHARMM36 nonbonded settings including force switching and no long-range dispersion correction for this protein-solvent use.
- Knapp B, Ospina L, Deane CM. J Chem Theory Comput. 2018. DOI `10.1021/acs.jctc.8b00391` — multiple independent replicas and false-positive control.
- Communications Biology MD reliability/reproducibility checklist. 2023. DOI `10.1038/s42003-023-04653-0` — convergence/time-course and at least three independent simulations with statistical analysis.
- Bakhache et al. Nature Microbiology. DOI `10.1038/s41564-024-01871-y` — direct EV-A71 InDel fitness evidence.
- Historical poliovirus 2C insertion-genetics source already registered in the repository.

Do not cite a method as proof that a specific A89 construct will work.

---

# PHASE A — Freeze and inventory Task 009

## A1. Create Task 010 output namespace

Create:

- `results/dynamics_audit_010/`
- `data/dynamics_audit_010/` if useful, otherwise use versioned top-level `data/*_v2.tsv` names consistently
- `docs/DYNAMICS_ANALYSIS_AUDIT_010_REPORT.md`
- `docs/DYNAMICS_ANALYSIS_AUDIT_010_RUN_LOG.md`
- `results/dynamics_audit_010/software_versions.tsv`
- `results/dynamics_audit_010/environment_inventory.tsv`

## A2. Inventory existing trajectories

Read the 009 production manifests and independently verify for every replica:

- trajectory exists and is non-zero;
- `tpr`, `xtc`, `edr`, `cpt`, log exist as applicable;
- final simulation time;
- frame count;
- temperature/pressure/energy finite;
- residue/atom mapping consistency;
- trajectory coordinate box information available;
- unique system, construct, junction, tag and replica identifiers.

Create:

`results/dynamics_audit_010/input_trajectory_inventory.tsv`

Do not treat `Finished mdrun` absence in a duplicate/latest scheduler log as trajectory failure when authoritative trajectory/log evidence proves completion.

## A3. Hash/provenance

Record hashes for the analysis-critical 009 inputs and scripts so later changes are traceable.

At minimum hash:

- production manifest;
- residue mapping;
- 009 analysis script;
- MDP files;
- candidate panel input table.

Create:

`results/dynamics_audit_010/input_provenance.tsv`

---

# PHASE B — Repair PBC and trajectory preprocessing

## B1. Core requirement

Every geometry-dependent Task 010 analysis must use a trajectory in which the protein is whole across periodic boundaries and translation/rotation treatment is explicit.

Do not calculate RMSD, Rg, tag-native Euclidean distance, contact maps, SASA, DCCM or network metrics on raw coordinates without validated PBC handling.

## B2. Preferred implementation

Implement a new analysis/preprocessing workflow rather than silently modifying historical 009 code.

Create:

`scripts/dynamics_audit_010_reanalyze.py`

and, if useful:

`scripts/dynamics_audit_010_preprocess.sh`

Acceptable primary strategy:

1. make each protein molecule whole using GROMACS `trjconv -pbc mol` or an equivalent validated MDAnalysis transformation;
2. center consistently;
3. perform rotational/translational fit only for analyses that require it;
4. retain an unfit but made-whole form for physical distance/SASA calculations where appropriate.

The inserted tag is covalently part of the same protein and must remain whole with the native chain.

## B3. Cross-validation gate

For at least:

- WT replica 1;
- one C-terminal candidate;
- one non-C-terminal candidate;
- one hard/conflict control;

compute RMSD independently with a GROMACS-native method and the new Python method.

Required output:

`results/dynamics_audit_010/pbc_rmsd_crossvalidation.tsv`

Acceptance target:

- same qualitative time series;
- small numerical discrepancy compatible with atom-selection/implementation differences;
- no unexplained multi-Angstrom systematic disagreement.

If disagreement remains, stop candidate ranking and debug preprocessing first.

---

# PHASE C — Correct structural dynamics metrics

## C1. Define fitting selections explicitly

Primary native-core fit should exclude inserted-tag atoms.

Use A89 native residue identity from the existing mapping.

Do not let an inserted peptide dominate the alignment.

Where the exact fit set materially affects results, compare:

- all native C-alpha residues in 112-321;
- a stable-core subset excluding highly flexible termini/loops.

Document the stable-core definition; do not choose it post hoc to favor candidates.

## C2. Self-drift RMSD

Calculate per replica:

- RMSD vs own first production frame;
- RMSD vs an equilibrated early-window reference if justified;
- full 20 ns mean;
- 0-5, 5-10, 10-15, 15-20 ns block means;
- final block mean;
- slope or simple early-vs-late drift diagnostic.

Name this metric clearly as self-drift.

Output:

`data/broad_dynamics_metrics_v2_corrected.tsv`

## C3. WT-reference RMSD

Define a transparent WT structural reference.

Preferred sensitivity pair:

1. WT starting/preproduction native structure after the same residue selection;
2. mean/representative WT ensemble structure from corrected WT trajectories.

For every candidate, calculate native-residue deviation from the WT reference after native-core fit.

Do not include inserted tag residues in WT-reference RMSD.

Output columns must distinguish:

- `self_drift_rmsd_*`
- `wt_reference_rmsd_*`

## C4. Junction-matched local RMSF

For each candidate junction `i|i+1`, define the candidate native window and exactly the same A89 native residue window in WT.

Recommended primary window:

`left-5 ... right+5`

with boundary handling documented.

Calculate per replica:

- candidate local RMSF;
- WT same-window RMSF from each WT replica;
- candidate-vs-WT difference;
- cross-replica summary.

Do not use a generic WT local-RMSF value.

## C5. Radius of gyration

Recalculate corrected native-chain Rg after PBC repair.

Use as a coarse global diagnostic only, not a decisive ranking axis.

## C6. Secondary-structure persistence

Add native local secondary-structure persistence around each insertion site using a reproducible DSSP-compatible implementation if feasible.

Report:

- fraction helix/strand/coil by native residue;
- WT-matched difference around the insertion window;
- any insertion-associated conversion of stable WT secondary structure.

If DSSP software installation becomes a blocker, record the blocker and continue other analyses; do not implement an ad-hoc secondary-structure algorithm and call it equivalent.

---

# PHASE D — Correct contact and tag-exposure analyses

## D1. WT-defined contact retention

Build a WT native-residue contact set from corrected WT coordinates.

Use a transparent definition, for example C-alpha or heavy-atom native contacts with documented sequence-separation and distance cutoffs.

Prefer an ensemble WT definition where a contact must be present above a stated WT occupancy threshold, rather than one arbitrary frame.

For every candidate calculate:

- retention of WT-defined contacts;
- loss of WT contacts;
- gain of new nonlocal contacts;
- local-window WT-contact retention;
- functional-neighborhood WT-contact retention where defensible.

Do not call candidate-first-frame contacts `native` without qualification.

Create:

`data/contact_persistence_dynamics_v2_corrected.tsv`

## D2. Candidate-start contact persistence

Retain candidate-specific starting-model contact persistence as a descriptive stability metric, but label it separately from WT-contact preservation.

## D3. Tag SASA

Calculate actual tag SASA per frame using a mature reproducible method.

Report:

- total tag SASA;
- per-residue tag SASA;
- exposed-residue fraction under a documented threshold/normalization method;
- cross-replica mean/SD or interval;
- time-block stability.

Create:

`data/tag_exposure_dynamics_v2_sasa.tsv`

## D4. Corrected tag collapse/contact metric

Recalculate tag-native contacts after PBC repair.

Exclude the immediate local flanking native window so unavoidable covalent/local proximity is not interpreted as collapse.

Report:

- minimum nonlocal heavy-atom distance;
- number of nonlocal contacts;
- fraction of frames with persistent nonlocal contacts;
- identity of recurrent contacted native residues.

Do not convert a single threshold into an automatic Tier penalty without context.

## D5. Detectability boundary

MD tag exposure cannot prove antibody/binder recognition.

Integrate but keep distinct the static binder-accessibility evidence already in the project.

The final table should have separate columns for:

- protein structural perturbation;
- tag solvent exposure;
- binder-accessibility/static recognition geometry;
- unresolved detectability concern.

---

# PHASE E — Convergence and statistical reliability

## E1. Independent experimental unit

Independent MD replicas are the primary independent computational replicates.

Do not treat trajectory frames as independent `n` for significance testing.

## E2. Time-block analysis

For every decision-relevant metric report block values for at least:

- 0-5 ns;
- 5-10 ns;
- 10-15 ns;
- 15-20 ns.

Also generate truncation summaries at:

- 10 ns;
- 15 ns;
- 20 ns.

Purpose:

- identify continuing relaxation;
- test whether candidate ordering depends on the last few ns;
- determine whether 20 ns is sufficient for screening-level use.

Create:

`results/dynamics_audit_010/time_truncation_stability.tsv`

## E3. Replica consistency

For each metric calculate:

- replica means;
- mean and SD across replica means;
- robust median where informative;
- bootstrap interval across independent replica means, with explicit caution that n=3 is small;
- leave-one-replica-out summary/ranking sensitivity.

Create:

`results/dynamics_audit_010/replica_stability.tsv`

## E4. Autocorrelation/effective sampling

For continuous time-series metrics where practical, estimate integrated autocorrelation time or effective sample size using a mature implementation.

At minimum apply this to representative RMSD and tag-exposure/contact time series.

Do not over-interpret formal ESS from short/nonstationary series; use it as a diagnostic.

## E5. Burn-in sensitivity

Do not discard an arbitrary fixed first segment without evidence.

Compare at least:

- full 0-20 ns;
- 2-20 ns;
- 5-20 ns;

for decision-relevant metrics.

If candidate conclusions change substantially with burn-in, mark the MD result unstable and trigger the extension/replication gate.

## E6. Ranking stability

Construct a dynamics-only review rank or Pareto classification using corrected metrics, then test:

- 10 vs 15 vs 20 ns;
- leave-one-replica-out;
- alternate fit/reference sensitivity;
- inclusion/exclusion of exploratory network metrics.

Create:

`results/dynamics_audit_010/dynamics_rank_stability.tsv`

Do not hide rank instability.

---

# PHASE F — Dynamic network analysis, downgraded and hardened

## F1. Recompute only on corrected fitted coordinates

DCCM/covariance/network analysis must use corrected made-whole and fitted native coordinates.

## F2. Replica-level network stability

For each construct, quantify whether DCCM/network conclusions replicate.

Possible diagnostics:

- pairwise matrix correlation between replicas;
- local-to-functional DCCM sign/magnitude consistency;
- community/network edge overlap;
- covariance/PCA subspace overlap if feasible.

## F3. Decision rule

If network signals are inconsistent across replicas or time windows:

`network_status = exploratory_unstable`

and assign **zero candidate-tier authority**.

If reasonably stable:

`network_status = exploratory_replicated`

and use only as a mechanistic caution/support flag, not a direct fitness predictor.

Create:

`data/dynamic_network_perturbation_v2_corrected.tsv`

and

`docs/DYNAMIC_NETWORK_ANALYSIS_V2_AUDITED.md`.

---

# PHASE G — Negative/conflict-control calibration without circular threshold tuning

Controls currently include:

- `155|156 x MAP8` — hard negative biological/RNA-pore/epitope context;
- `256|257 x MAP8` — oligomer/historical-conflict control.

Use these to assess method behavior.

Ask:

- do corrected MD metrics identify meaningful perturbation in the hard-negative control?
- if not, which metrics lack biological discriminative value?

Important:

Do **not** tune thresholds until controls are forced to look bad. That would be circular.

Instead, use controls to determine the evidence weight that MD deserves.

Create:

`results/dynamics_audit_010/control_discrimination_audit.tsv`

and report whether dynamics shows:

- useful discrimination;
- partial discrimination;
- no reliable discrimination.

---

# PHASE H — CHARMM36 protocol correction and validation subset

## H1. Do not continue existing 009 trajectories as the primary new evidence

Because Task 009 used a CHARMM36 nonbonded protocol that differs from the documented GROMACS recommendation, do not simply extend existing 009 production to 50 ns and label it corrected evidence.

The 009 trajectories remain useful legacy comparative data after reanalysis.

## H2. Create corrected MDP set

Create new Task 010 MDP files using the GROMACS-documented CHARMM36 settings, including:

```text
constraints = h-bonds
cutoff-scheme = Verlet
vdwtype = cutoff
vdw-modifier = force-switch
rlist = 1.2
rvdw-switch = 1.0
rvdw = 1.2
coulombtype = PME
rcoulomb = 1.2
DispCorr = no
```

Preserve the same temperature, pressure, water model and ionic-strength intent unless a documented reason requires a change.

Create:

`results/dynamics_audit_010/gromacs/mdp/`

and

`results/dynamics_audit_010/forcefield_protocol_audit.tsv`.

## H3. Equilibration

Use a more defensible restrained equilibration than the 009 minimum.

Preferred default for the validation subset unless system diagnostics require adjustment:

- energy minimization;
- restrained NVT approximately 100 ps;
- restrained NPT approximately 500 ps to 1 ns;
- verify temperature, density/volume and pressure behavior;
- production only after preparation is technically stable.

Do not claim that the duration itself proves equilibrium.

## H4. Validation subset selection

Only after corrected reanalysis, select a compact, diverse validation subset.

Target approximately 5 systems total:

1. WT;
2. strongest C-terminal candidate from corrected multi-evidence review;
3. strongest non-C-terminal candidate;
4. one additional candidate representing a different tag/site rationale or major evidence conflict;
5. `155|156 x MAP8` hard negative control.

If the corrected reanalysis strongly indicates another control is more informative, include it as a sixth system, but document the reason.

Do not choose three adjacent C-terminal junctions and call that biological diversity.

## H5. Replicas

Run at least 3 independent corrected-protocol replicas per validation system using independent velocity seeds.

If resources permit and the workflow is robust, 5 independent replicas are preferable for the most decision-critical systems because multiple replicas reduce false-positive inference; however, 5 replicas are not a mandatory stop criterion for this overnight task.

## H6. Initial production length

Start corrected validation at 20 ns per replica.

This is a **screening checkpoint**, not a magic convergence time.

If jobs finish, analyze immediately using the Task 010 corrected pipeline.

If jobs are still running at the final repository checkpoint, record submitted/running/completed state without fabricating results.

---

# PHASE I — Adaptive extension gate: decide whether 50 ns is needed

## I1. No blanket 50 ns rule

50 ns is not a universal requirement.

## I2. Extension triggers

A system becomes eligible for extension beyond 20 ns when one or more decision-relevant conditions hold after corrected analysis:

- major metric continues directional drift in 15-20 ns block;
- replica means disagree enough to change candidate class;
- 10/15/20 ns ranking is unstable;
- burn-in choice changes interpretation;
- corrected-protocol 20 ns result disagrees materially with legacy 009 result;
- network/mechanistic inference is explicitly required but not stable;
- candidate sits near the experimental priority boundary and additional sampling is likely to resolve the uncertainty.

## I3. Extension choices

Choose scientifically between:

- add independent replicas;
- extend existing corrected replicas to 50 ns;
- both for the small number of decision-critical systems.

Prefer replica breadth when the dominant uncertainty is between-replica variability.

Prefer extension when replicas show a shared ongoing slow drift.

Document the reason for each system.

Create:

`results/dynamics_audit_010/extension_decision.tsv`

with columns such as:

- system;
- 20ns_status;
- instability_reason;
- additional_replica_needed;
- extension_to_50ns_needed;
- decision_basis.

## I4. Overnight execution behavior

Within Task 010, Codex may submit the corrected validation subset jobs and continue all independent analysis/documentation while they run.

Use scheduler-safe recovery and avoid duplicate submissions.

Do not create an uncontrolled watcher that repeatedly resubmits finished jobs.

If implementing a watcher, it must:

- identify completed outputs before submission;
- use a lock/state file;
- submit at most one outstanding job per intended replica;
- terminate automatically when all intended jobs are complete or when a documented unrecoverable blocker occurs.

---

# PHASE J — Integrate non-MD evidence and produce final prioritized list

## J1. Evidence hierarchy

Use the project hierarchy, with explicit conflict preservation:

1. direct HRV-A89 phenotype if available — currently absent;
2. direct homolog 2C insertion phenotype with mapped position;
3. homolog substitution/deletion phenotype and direct 2C genetics/biochemistry;
4. hard functional motifs / experimentally supported structural-functional context;
5. A89 structural ensemble evidence;
6. phylogeny-aware evolution/natural indels;
7. tag-specific PLM;
8. inserted-structure ensemble perturbation;
9. binder/tag accessibility;
10. corrected replicated MD;
11. dynamic network, only as mechanistic context;
12. RNA/codon context once real sequence is supplied — currently blocked.

MD must not silently overrule a hard biological exclusion or stronger direct phenotype.

## J2. Required candidate categories

Produce at least:

### `Priority_A`

Constructs suitable for first experimental testing based on multiple independent computational evidence layers, no hard biological exclusion, no catastrophic corrected-MD flag, and a clear experimental rationale.

### `Priority_B`

Constructs with one important unresolved conflict/uncertainty but enough independent evidence to justify backup/rescue testing.

### `Conflict_control`

Constructs deliberately retained because evidence classes disagree.

### `Hard_negative_control`

Known/high-confidence biologically unfavorable insertion context used for method calibration.

No category means validated or safe.

## J3. Diversity constraint

The final priority panel should not collapse to the C-terminal 287-291 neighborhood.

Aim for Priority A to include multiple biological regions if supported.

Adjacent C-terminal junctions should be grouped as one region for diversity reporting.

## J4. Tag diversity

Do not assume one tag is universally best.

Report:

- best site(s) for MAP8;
- best site(s) for HA;
- best site(s) for G196_minimal;
- any other tag only if existing evidence is sufficiently mature.

## J5. No opaque total score

Create a table with component evidence columns and explicit interpretation labels.

Do not calculate one final scalar score unless it is clearly secondary and every component/weight/sensitivity is preserved. Prefer Pareto/evidence-class review.

## J6. Required final machine-readable table

Create:

`data/final_candidate_panel_v3_audited.tsv`

Required columns should include at minimum:

- construct_id;
- junction;
- site_region;
- tag_form;
- priority_class;
- hard_biological_constraint;
- EV_A71_direct_insertion_prior;
- homolog_substitution_deletion_context;
- conservation_indel_context;
- PLM_context;
- inserted_structure_context;
- oligomer_context;
- RNA_holoenzyme_context;
- binder_accessibility_context;
- corrected_MD_status;
- self_drift_effect;
- WT_reference_deviation;
- WT_matched_local_RMSF_effect;
- WT_defined_contact_retention;
- tag_SASA_exposure;
- corrected_nonlocal_tag_contact;
- convergence_status;
- replica_consistency;
- network_status;
- corrected_protocol_validation_status;
- extension_needed;
- unresolved_conflicts;
- rationale;
- safe_or_validated = `no`.

## J7. Required human-readable shortlist

Create:

`docs/FINAL_CANDIDATE_PRIORITY_V1_AUDITED.md`

It must contain:

1. concise top priority list;
2. backup list;
3. controls;
4. why each was selected;
5. why obvious alternatives were not selected;
6. what evidence is direct vs homolog vs computational;
7. what 20 ns can and cannot establish;
8. whether any system actually needs 50 ns and why;
9. exact unresolved issues before nucleotide-level design.

The final user-facing priority order must be experimentally actionable at the **candidate identity** level, but must not include wet-lab procedural steps.

---

# PHASE K — Robustness and sanity checks

## K1. Negative-control sanity check

Report whether the final framework gives the hard-negative control lower priority **because of independent biological evidence**, not because thresholds were tuned after seeing it.

## K2. C-terminal cluster sensitivity

Generate final priorities with:

- all C-terminal adjacent rows included;
- only one representative per C-terminal region.

Verify that panel diversity does not depend on duplicate counting of adjacent junctions.

## K3. Leave-one-layer-out sensitivity

For each Priority A construct, remove each non-hard evidence layer in turn and record whether the priority class changes.

Important layers include:

- direct homolog insertion;
- structural ensemble;
- conservation/indel;
- PLM;
- corrected MD;
- accessibility.

Create:

`results/dynamics_audit_010/final_panel_leave_one_layer_out.tsv`

## K4. MD-withheld final ranking

Produce a sensitivity panel with corrected MD completely withheld.

Purpose:

- determine whether MD is actually driving the candidate list;
- prevent an unstable dynamics layer from dominating.

Create:

`results/dynamics_audit_010/final_panel_without_md.tsv`

If the top candidate set changes dramatically only because of weak/unstable MD metrics, downgrade MD authority rather than presenting false precision.

---

# PHASE L — Repository state and final checkpoint

## L1. Update authoritative files

At completion update:

- `PROJECT_STATE.md`
- `DECISIONS.md`
- `ANALYSIS_INDEX.md`
- `TODO.md`
- `ACTIVE_TASK.md`
- `references/LITERATURE_EVIDENCE_REGISTRY.md` where required

Do not rewrite historical 009 files except to add an explicit superseded/provisional note if necessary and clearly provenance-preserving.

## L2. Required final report answers

`docs/DYNAMICS_ANALYSIS_AUDIT_010_REPORT.md` must explicitly answer:

1. Were the 009 trajectories technically usable after PBC correction?
2. How much did PBC correction change RMSD/Rg/tag-distance/contact/DCCM results?
3. Did the old Tier A/B classification change?
4. Which old 009 metrics were invalid, biased, or merely mislabeled?
5. What are the corrected candidate priorities?
6. Which candidate is the strongest C-terminal option?
7. Which candidate is the strongest non-C-terminal option?
8. What are the best options per tag?
9. Does the hard-negative control behave differently under corrected MD?
10. Does corrected MD have useful biological discrimination?
11. How stable are priorities at 10, 15 and 20 ns?
12. Are three replicas adequate for screening for each top candidate?
13. Which systems require more replicas?
14. Which systems require extension to 50 ns?
15. Is there any scientific reason to extend all systems to 50 ns? Expected default answer is `no` unless data unexpectedly prove otherwise.
16. Did corrected CHARMM36 validation agree with the reanalyzed legacy 009 results?
17. What remains blocked by absence of exact nucleotide/RNA context?
18. What is the recommended first experimental candidate panel at the construct-identity level?

## L3. Stop criteria

Task 010 is complete when:

- PBC bug is fixed and cross-validated;
- corrected structural/contact/exposure metrics exist;
- junction-matched WT baselines exist;
- convergence/replica/time-truncation analyses exist;
- old heuristic dynamics tier is explicitly superseded;
- CHARMM36 protocol audit is complete;
- corrected validation subset is at least prepared/submitted, and preferably analyzed if completed;
- adaptive 50 ns extension decisions are machine-readable;
- final candidate panel V3 is generated;
- final audited priority report is generated;
- authoritative repository state files are updated and pushed.

If corrected validation MD remains running, the task may checkpoint as:

`CANDIDATE_PRIORITY_PROVISIONAL_PENDING_CORRECTED_PROTOCOL_VALIDATION`

but only if the corrected 009 reanalysis and candidate ranking are otherwise complete.

If corrected validation finishes and does not materially overturn the ranking, the preferred final state is:

`AUDITED_CANDIDATE_PANEL_READY_FOR_EXPERIMENTAL_REVIEW`

## L4. Failure handling

For recoverable failures:

`diagnose -> repair/fallback -> record -> continue independent modules -> revisit`.

Do not stop the entire overnight task for one optional package or one failed replica if substantial independent work can continue.

Do not silently substitute a weak custom method for a mature available method.

Do not fabricate completed jobs/results.

## L5. Git checkpoint policy

Commit and push meaningful checkpoints, not every minor file touch.

Suggested checkpoints:

1. `task010: inventory and repair trajectory preprocessing`
2. `task010: corrected structural contact and exposure analysis`
3. `task010: convergence and robustness audit`
4. `task010: corrected CHARMM36 validation setup`
5. `task010: audited candidate rerank and final report`

At every checkpoint ensure the branch remains inspectable from GitHub.

---

# Final authorization boundary

Codex is authorized to execute this entire Task 010 autonomously on the server, including:

- user-space environment repair/install;
- trajectory preprocessing;
- corrected analysis scripting;
- GROMACS analysis;
- corrected-protocol validation MD setup;
- Slurm submission/restart/cancellation of jobs created by this task;
- adaptive decision on additional replicas versus extension for the reduced validation subset;
- statistical/robustness analysis;
- candidate re-ranking;
- reports and Git commits/pushes.

Codex is **not** authorized in this task to:

- design exact viral nucleotide constructs;
- write wet-lab procedural protocols;
- launch broad membrane/RNA/ATP/antibody mechanism simulations;
- claim biological safety or validation;
- merge the analysis branch into `main` without explicit user/ChatGPT review.
