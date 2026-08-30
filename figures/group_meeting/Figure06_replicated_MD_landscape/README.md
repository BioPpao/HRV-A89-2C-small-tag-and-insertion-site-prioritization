# Figure 6 — Replicated MD perturbation landscape

Title: **Replicated MD identifies persistent nonlocal tag contacts as the most discriminating dynamic readout**

Subtitle: **Broad 3 x 20-ns screening and independent corrected-protocol validation reproduce the main candidate-control differences**

## Figure contract

- Core conclusion: persistent nonlocal tag contacts provide the clearest dynamic separation between leading candidate hypotheses and MD-caution controls across replicated short MD, and independent corrected-protocol validation reproduces the main candidate-control contact pattern.
- Evidence hierarchy: panel b is the hero broad-screen evidence; panel c exposes validation-replica behavior and heterogeneity; panel d tests protocol sensitivity without pooling ensembles; panel a establishes the workload and interpretation boundary.
- Archetype: quantitative grid with an asymmetric hero panel.
- Backend: R only for data assembly, plotting, preview, vector/raster export and visual QA.
- Final size: 183 x 190 mm.
- Export contract: editable SVG, vector PDF, 600-dpi PNG, machine-readable source data and machine-readable QC.
- Biological boundary: MD is downstream comparative perturbation evidence. No construct is called safe, compatible, fitness-neutral or experimentally validated.

The existing Figure 5 script contributed style-only inheritance: restrained semantic colours, Arial-first typography, thin axes, white background and compact panel labels. Figure 6 was built anew because its replicate structure, statistics and scientific questions differ.

## Scientific question

Which corrected replica-level MD observable most clearly separates current candidate hypotheses from MD-caution controls, and is the main pattern reproduced by an independent corrected-protocol ensemble?

The answer in the audited 20-ns screening framework is persistent nonlocal tag-contact fraction. WT-reference RMSD, junction-matched local RMSF and WT-defined contact retention remain useful perturbation/QC readouts, but they discriminate the candidate/control roles less clearly in this dataset.

## Authority files

Interpretation follows:

- `docs/BROAD_DYNAMICS_AND_RECOVERY_009_REPORT.md`
- `docs/DYNAMICS_ANALYSIS_AUDIT_010_REPORT.md`
- `docs/CORRECTED_PROTOCOL_VALIDATION_V1.md`
- `docs/FINAL_CANDIDATE_PRIORITY_V2_CORRECTED_VALIDATION.md`
- `docs/FINAL_SCIENTIFIC_CLEANUP_010A.md`

Numerical inputs are:

- `data/broad_dynamics_metrics_v2_corrected.tsv`
- `data/contact_persistence_dynamics_v2_corrected.tsv`
- `data/tag_exposure_dynamics_v2_sasa.tsv`
- `data/corrected_validation_broad_dynamics_v1.tsv`
- `data/corrected_validation_contact_persistence_v1.tsv`
- `data/corrected_validation_tag_exposure_v1.tsv`
- `data/final_candidate_panel_v5_experimental_review_cleanup.tsv` for current role/priority annotations and corrected-validation coverage.

## Superseded files not used as primary Figure 6 results

The following Task009 V1 files are historical/provenance inputs only and are not used for the plotted primary metrics:

- `data/broad_dynamics_metrics_v1.tsv`
- `data/tag_exposure_dynamics_v1.tsv`
- `data/contact_persistence_dynamics_v1.tsv`

The Task009 V1 interpretation was superseded because geometry-dependent analysis required PBC correction, self-drift had been overinterpreted as WT-like stability, local RMSF was not junction-matched, contact retention used the candidate start rather than WT-defined contacts, and tag exposure lacked true SASA.

## Metric definitions

1. **WT-reference ensemble RMSD (A):** `wt_reference_ensemble_rmsd_mean_A`; deviation of the native A89 core from a common WT-reference ensemble after audited PBC-aware preprocessing.
2. **Delta local RMSF versus matched WT (A):** `delta_local_rmsf_vs_wt_A`; local candidate RMSF minus the junction-matched WT local RMSF.
3. **WT-defined contact retention:** `wt_defined_contact_retention_mean`; fraction of WT-defined native contacts retained in the trajectory.
4. **Persistent nonlocal tag-contact fraction:** `tag_nonlocal_contact_fraction_any_lt_4p5A`; fraction of analyzed frames with any tag-to-nonlocal-native heavy-atom contact below 4.5 A, excluding the local junction window.
5. **Exposed tag-residue fraction:** `tag_exposed_residue_fraction_rel_sasa_ge_0p25`; fraction of tag residues with relative SASA at least 0.25.

No composite MD score, favorable quadrant or inferred good/bad threshold is used.

## Why nonlocal contact is emphasized

Persistent nonlocal tag-contact fraction gives the clearest separation in both ensembles: 289|290 x MAP8 remains low-contact, 224|225 x MAP8 remains at 1.0 in all three independent corrected-validation replicas, and 155|156 x MAP8 retains a high-contact caution. It also exposes the 248|249 x HA replica heterogeneity that a mean alone would hide. This is comparative dynamic evidence, not a measure of viral fitness, binder accessibility or biological compatibility.

## Why self-drift, Rg and DCCM/network are downweighted

Raw self-drift RMSD and global radius of gyration are nonspecific over this short protein-only screen. DCCM and dynamic-network outputs were PBC/convergence-sensitive and are not stable enough to drive candidate ranking. They were audited as exploratory/nonspecific over the short screening window. The main figure therefore focuses on replica-level construct comparisons rather than RMSD time-series clutter.

## Sampling interpretation

The broad corrected dataset contains WT plus 12 tagged constructs, with 3 replicas per system and 20 ns per replica: 39/39 usable trajectories, 0 technical exclusions and 780 ns of cumulative screening sampling.

The independent corrected-protocol validation contains six systems, with 3 replicas per system and 20 ns per replica: 18 trajectories and 360 ns of cumulative validation sampling.

The combined 57 trajectories are described only as **1.14 microseconds cumulative screening/validation sampling**. They are not a single converged 1.14-microsecond simulation.

Three independent 20-ns replicas are adequate for the current screening objective. They are not sufficient to claim mechanistic convergence.

## Why 50 ns is not currently triggered

No system currently requires 50 ns. No decision-relevant shared slow drift or protocol disagreement currently triggers blanket extension. This is not a claim that 20 ns is fully converged. If between-replica variance becomes the dominant decision-critical uncertainty, additional independent replicas should be considered before mechanically extending every system to 50 ns.

## Why the two ensembles are not pooled

Task009 corrected trajectories and corrected-protocol validation trajectories are independent 3 x 20-ns ensembles. They are displayed side-by-side for protocol sensitivity only. They are not concatenated into six replicas, are not treated as paired trajectories and are not analyzed with a paired test.

## Construct ordering logic

Panel b uses scientific role order, not an arbitrary metric score:

1. WT.
2. Priority A: 289|290 x MAP8, 289|290 x G196 minimal, 248|249 x HA, 248|249 x MAP8.
3. Priority B: 288|289 x MAP8, 288|289 x HA, 290|291 x MAP8.
4. Conflict controls: 256|257 x MAP8, 224|225 x MAP8, 224|225 x HA, 203|204 x G196 minimal.
5. Hard negative: 155|156 x MAP8.

The ordering preserves the evidence hierarchy. In particular, 256|257 x MAP8 is not biologically promoted merely because its MD contact behavior is neutral-like.

## Outputs

- `Figure06_replicated_MD_landscape.svg`
- `Figure06_replicated_MD_landscape.pdf`
- `Figure06_replicated_MD_landscape_600dpi.png`
- `Figure06_replicated_MD_landscape_source_data.tsv`
- `Figure06_replicated_MD_landscape_qc.tsv`
- `Figure06_replicated_MD_landscape_caption.md`
- `README.md`
- plotting script: `scripts/plot_figure06_replicated_MD_landscape.R`

## Reproduction

The verified environment is an isolated Conda R 4.3.3 environment. Package versions are recorded in the QC table. From the repository root:

```text
conda run -n figure06-r43 Rscript --vanilla scripts/plot_figure06_replicated_MD_landscape.R
```

The script fails loudly on missing columns, duplicate join keys, unexpected system sets, workload-count mismatches or failed exports. Because this Windows R build cannot write the 600-dpi PNG directly to the non-ASCII workspace path, the PNG is rendered by R to its ASCII temporary directory and copied by R to the requested output path; visual content and resolution are unchanged.

## Final QA

- [x] 39 broad trajectories represented correctly.
- [x] 18 independent corrected-validation trajectories represented correctly.
- [x] 57 total trajectories.
- [x] 1.14 microseconds stated only as cumulative screening/validation sampling.
- [x] All individual replicas retained; deterministic non-quantitative offsets reveal exact overlaps without changing metric values.
- [x] 248|249 x HA heterogeneity visible.
- [x] 224|225 x MAP8 validation replicas all show high contact.
- [x] 155|156 x MAP8 reproduced caution visible.
- [x] 289|290 x MAP8 low-contact behavior visible.
- [x] 256|257 x MAP8 is not falsely promoted biologically.
- [x] No legacy biased metric used for primary ranking.
- [x] No composite score, convergence claim or blanket 50-ns claim.
- [x] SVG/PDF vector outputs and 600-dpi PNG generated.

## Interpretation boundary

Persistent nonlocal tag contacts provide the clearest dynamic separation between leading candidate hypotheses and MD-caution controls across replicated short MD. Independent corrected-protocol validation reproduces the main candidate-control contact pattern. MD remains comparative downstream evidence and does not override direct homolog phenotype, hard functional constraints or the lack of direct HRV-A89 phenotype.
