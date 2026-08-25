# Report Provenance V1

Date: **2026-08-25**

Report archive: `reports/current_computational_results_report_v1/`

## 1. Scientific state represented

The report freezes the project at:

`EXPERIMENTAL_REVIEW_SHORTLIST_READY_FOR_DISCUSSION`

Current branch at report creation:

`analysis/experimental-review-cleanup-010a`

The report is a synthesis/presentation layer and does not supersede authoritative project files.

---

## 2. Primary repository sources used

### Project state / governance

- `PROJECT_STATE.md`
- `ACTIVE_TASK.md`
- `DECISIONS.md`
- `ANALYSIS_INDEX.md`
- `TODO.md`
- `INPUT_PROVENANCE.md`

### Functional / structural / evolutionary evidence

- `docs/2C_FUNCTIONAL_CONSTRAINT_MAP_V2.md`
- `docs/2C_FUNCTIONAL_EXCLUSION_MAP_V3.md`
- `docs/STRUCTURAL_SCREEN_V2.md`
- `docs/CONSERVATION_SCREEN_V2.md`
- `docs/CANDIDATE_JUNCTION_QC_V1.md`
- `data/junction_structural_metrics_v2.tsv`
- `data/hrvA_conservation_per_junction_v2.tsv`
- integrated candidate tables under `data/`

### Tag evidence

- `docs/TAG_CANDIDATE_SCREEN_V1.md`

### Broad dynamics / audit / corrected validation

- `docs/BROAD_DYNAMICS_AND_RECOVERY_009_REPORT.md`
- `docs/DYNAMICS_009_POSTHOC_AUDIT_V1.md`
- `data/broad_dynamics_metrics_v2_corrected.tsv`
- `docs/CORRECTED_PROTOCOL_VALIDATION_V1.md`
- `results/dynamics_audit_010/forcefield_protocol_audit.tsv`
- `results/dynamics_audit_010/corrected_validation_block_stability_v1.tsv`
- `results/dynamics_audit_010/protocol_sensitivity_v1.tsv`
- `data/corrected_validation_tag_exposure_v1.tsv`

### Final cleanup / shortlist

- `docs/FINAL_SCIENTIFIC_CLEANUP_010A.md`
- `docs/EXPERIMENTAL_REVIEW_SHORTLIST_V1.md`
- `results/dynamics_audit_010/differential_block_drift_vs_wt_v1.tsv`
- `results/dynamics_audit_010/final_sampling_decision_v2_cleanup.tsv`
- `results/dynamics_audit_010/tag_nonlocal_contact_replica_heterogeneity_v1.tsv`
- `data/final_candidate_panel_v5_experimental_review_cleanup.tsv`
- `data/experimental_review_shortlist_v1.tsv`

---

## 3. Important numerical values represented in the report

Examples include:

- 320 total internal junctions;
- 10 strict structural-pass junctions in the V2 four-structure screen;
- conservation V2 category counts: 69 conserved, 113 intermediate, 125 variable, 13 lineage-indel-supported;
- Task 009 broad MD: 39 trajectories × 20 ns = 780 ns;
- corrected validation: 6 systems × 3 replicas × 20 ns = 18 trajectories / 360 ns;
- total production sampling generated across legacy + corrected validation = ~1.14 μs, while the two protocol sets remain analytically distinct rather than concatenated as one ensemble;
- corrected `289|290 × MAP8` WT-reference RMSD ~1.94 Å, WT-defined contact retention ~0.902, nonlocal tag-contact fraction ~0.028;
- corrected `248|249 × HA` WT-reference RMSD ~1.60 Å, WT-defined contact retention ~0.910, mean nonlocal tag-contact fraction ~0.592;
- `248|249 × HA` replica nonlocal contact fractions: 0.761194, 0.263682, 0.751244;
- `289|290 × MAP8` candidate-minus-WT late-minus-early drift: self RMSD ~-0.144 Å, WT-reference RMSD ~+0.052 Å, WT-defined contact retention ~-0.0278.

Where exact machine-readable values matter, the upstream TSVs remain authoritative.

---

## 4. Literature / evidence references

The report relies on the project literature registry and tag-screen references. Important examples include:

- Teterina NL et al. *Identification of tolerated insertion sites in poliovirus non-structural proteins.* Virology. 2011. DOI: `10.1016/j.virol.2010.09.028`.
- Wakasa A et al. *Site-specific epitope insertion into recombinant proteins using the MAP tag system.* J Biochem. 2020. DOI: `10.1093/jb/mvaa054`.
- Fujii Y et al. MAP-tag literature.
- Tatsumi K et al. G196 epitope tag system. Sci Rep. 2017. DOI: `10.1038/srep43480`.
- Yano T et al. AGIA tag system. PLoS One. 2016.
- Götzke H et al. ALFA-tag. Nat Commun. 2019.
- Fujii Y / Tamura R et al. PA-tag work.
- Knapp B, Ospina L, Deane CM. *Avoiding False Positive Conclusions in Molecular Simulation: The Importance of Replicas.* J Chem Theory Comput. 2018.
- *Reliability and reproducibility checklist for molecular dynamics simulations.* Commun Biol. 2023.
- GROMACS 2024 CHARMM force-field documentation.

The repository file `references/LITERATURE_EVIDENCE_REGISTRY.md` is the preferred source-to-claim registry.

---

## 5. Visual-design reference

The report visual palette was inspired by the overall graphic language of:

Chen W-H et al. **Quantitative and interface-aware prediction of peptide–protein interactions by VITAL.** *Nature Machine Intelligence* (2026). DOI: `10.1038/s42256-026-01291-z`.

The uploaded paper was used only as a **visual palette / information-design reference**. The report does not reproduce the paper's figures as report content.

Design features adopted at a high level include:

- white paper-like background;
- teal/cyan structural elements;
- orange peptide/accent elements;
- violet model/matrix accents;
- blue quantitative plots;
- amber/red reserved for caution/conflict;
- thin gray/black scientific annotation lines.

---

## 6. HTML portability / self-contained design

The archived HTML is intended to be a single portable file.

Requirements:

- all CSS embedded;
- all JavaScript embedded;
- scientific diagrams rendered as inline SVG where possible;
- report data used for interactive figures embedded in the document;
- no required external image directory;
- no CDN or remote JavaScript dependency;
- no external font dependency.

Local notes/highlights, where enabled, use browser `localStorage` and therefore remain local to the browser/device rather than modifying the scientific source data.

---

## 7. Raw-data boundary

The ordinary Git repository intentionally does **not** contain all raw simulation binaries.

### GitHub contains

- analysis scripts;
- derived machine-readable TSVs;
- QC tables and manifests;
- force-field/protocol audit;
- final candidate panels;
- reports and decision records;
- file paths / trajectory existence / frame-count / completion metadata in inventories.

### Server-only / separately archived data include

Legacy Task 009 GROMACS production data under paths such as:

`results/broad_dynamics_009/gromacs/systems/...`

Corrected-validation production data under paths such as:

`results/dynamics_audit_010/gromacs/validation_systems/...`

Typical large or binary files include:

- `*.xtc`
- `*.tpr`
- `*.edr`
- `*.cpt`
- `*.gro`
- selected run logs

The local-multimer recovery also generated server-side raw outputs such as A3M/PDB/JSON/PNG files. That analysis was technically inconclusive because the completed local multimer models contained non-finite coordinates/confidence values, so the raw outputs do not carry ranking authority.

### Consequence

The GitHub repository is sufficient to understand, audit and report the **current scientific conclusions**, but is not by itself a complete binary archive from which every MD trajectory can be reanalyzed from scratch if the server data are lost.

A dedicated raw-data manifest with paths, sizes and SHA256 checksums is recommended before any server cleanup.

---

## 8. Scientific interpretation boundary

The report must not be cited internally as evidence that:

- `289|290` is a safe insertion site;
- `248|249` is biologically tolerated in HRV-A89;
- any tag preserves ATPase/RNA/replication function;
- 20 ns demonstrates full convergence;
- MD overrides the unfavorable direct EV-A71 insertion phenotype;
- the 112–321 fragment reproduces the full native membrane/RNA/oligomer state.

The valid report-level conclusion is that the project has produced a transparent, conflict-aware **experimental-review shortlist** suitable for the next biological validation stage.
