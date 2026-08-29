# Figure 05 file selection

Target branch: analysis/experimental-review-cleanup-010a.

| File | Selection reason | Figure use | Version rationale |
|---|---|---|---|
| data/tag_site_structure_perturbation_v3_open.tsv | Authoritative OPEN_STRUCTURE_007 model-level WT-vs-inserted comparison | Panel b global/local RMSD; Panel c per-model values; source data | V3 open supersedes the partial proxy-only 005 layer and retains all 48 tagged models |
| data/tag_site_openmm_qc_v1.tsv | Model-level geometry-processing status and pre/post-minimization diagnostics | QC, source data, Panel a workload | Matching model-level OpenMM QC table for OPEN_STRUCTURE_007 |
| data/tag_site_contact_network_v3_open.tsv | WT-defined native/local contact losses for every tagged model | Panel c native-contact-loss axis; source data | V3 open matches the selected model files |
| data/tag_site_hexamer_context_v3_open.tsv | Two project-hexamer evaluations per tagged model | Panel c oligomer-context axis; Panel a workload; QC | V3 open contains 96 model × hexamer rows for the 48 tagged models |
| data/tag_site_secondary_structure_accessibility_v1.tsv | Model-level tag SASA and local secondary structure | Optional tag-SASA source-data column | Matching accessibility table for the OPEN_STRUCTURE_007 model set |
| data/tag_site_structure_panel_v3_open.tsv | Construct/tag sequences, functional tier, direct-insertion class | Source-data annotations | Prediction panel used by the selected model set |
| data/final_candidate_panel_v5_experimental_review_cleanup.tsv | Current expert-adjudicated Priority A/B and control classes | Point colour/current interpretation | V5 is the current 010A review state; no composite score was used |
| data/candidate_junctions_v2.tsv | Junction-level structural track and conservation class | Source-data annotations | Required full 320-junction context, used only for non-model annotations |
| OPEN_STRUCTURE_007 WT and three rank-001 PDBs | Direct coordinates for fixed-view overlays | Panel d | Selected after quantitative review to show a lower-local-perturbation example, an adjacent-junction contrast and a global/local-discordant example |

The older CONTINUOUS_TAG_SITE_MODELING_005 report describes 132 proxy-layer constructs but explicitly lacked inserted 3D models. It was not used as the quantitative Figure 5 source. The complete OPEN_STRUCTURE_007 model-level tables were available, so no candidate-only fallback was required.

Field mapping:

- native_2c_ca_rmsd_to_wt_A → global/native C-alpha RMSD
- local_window_ca_rmsd_A → local-window RMSD
- native_contact_loss_count → native-contact-loss metric
- maximum tag_neighbor_clashes_2p5A across two project hexamers → oligomer-context metric

