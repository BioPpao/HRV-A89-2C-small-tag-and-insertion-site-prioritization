# Decision Log

Last updated: 2026-08-22

These are active decisions. Future analyses should change them only with explicit new evidence and should record the reason for the change.

## D-001 — Project is not HA-only

**Decision:** Treat the project as **small-tag identity × insertion-site prioritization**. HA is a benchmark, not the assumed winner.

**Reason:** tag chemistry and insertion-site geometry are independent variables; viral fitness can depend strongly on tag identity even at the same site.

## D-002 — FLAG is excluded

**Decision:** Do not rank or model FLAG as a 2C tag in the primary project.

**Reason:** the 9A5 antibody construct already uses FLAG; orthogonal detection is required.

## D-003 — Ranking unit is a peptide junction

**Decision:** Rank `i|i+1` junctions, not isolated residues.

**Implementation:** propagate both flanking-residue properties plus local sequence/structure-window information to the junction.

## D-004 — No monomer-only site calls

**Decision:** A site must be evaluated across both AF monomers and both hexamer models.

**Reason:** monomer exposure can become oligomer interface/pore exposure after assembly; model uncertainty must be retained.

## D-005 — No blanket N-terminal exclusion

**Decision:** Do not automatically exclude all aa1–110.

**Reason:** literature supports graded N-terminal membrane/RNA/oligomerization constraints, with the strongest evidence concentrated in defined subregions.

## D-006 — Do not automatically ban the entire C terminus

**Decision:** Treat Zn/Cys, RNA-binding and terminal oligomerization elements as high-risk/hard features, but preserve direct historical insertion-tolerance observations in a separate rescue track.

**Reason:** conflicting direct evidence should not be erased by a broad structural exclusion.

## D-007 — Functional evidence outranks attractive loop geometry

**Decision:** an exposed coil/loop is not sufficient for promotion.

**Reason:** the current strict structural screen found geometrically clean junctions that still neighbor biologically high-risk regions.

## D-008 — Pore geometry is a penalty, not direct proof

**Decision:** use project-hexamer pore orientation/radial metrics as context penalties only.

**Reason:** current A89 hexamers are no-RNA template-guided hypotheses; the experimental RNA-bound geometry is not identical to the project ring.

## D-009 — No final site before near-HRV conservation

**Decision:** do not select a final candidate junction until HRV-A-focused conservation and indel-tolerance analysis is complete.

**Status:** fulfilled by CONSERVATION_002, but later decisions below add a stronger direct-evidence gate.

## D-010 — Conservation is not a standalone safety criterion

**Decision:** use conservation hierarchically and as supporting evidence.

**Reason:** substitution variability does not demonstrate tolerance of an artificial 5–10 aa insertion.

## D-011 — No additional generic MD as the current priority

**Decision:** do not spend the next analysis cycle on longer generic no-membrane WT MD.

**Reason:** current uncertainty is dominated by insertion-tolerance evidence and construct-specific perturbation, not trajectory length of existing WT systems.

## D-012 — Tagged-structure prediction is a perturbation screen

**Decision:** AlphaFold/structural modeling of tagged constructs may rank perturbation risk but cannot validate a construct.

**Primary outputs:** native 2C fold deviation, local backbone displacement, interface/pore conflict, functional-feature distortion, tag accessibility.

**Not a failure criterion by itself:** low confidence/flexibility of the inserted tag peptide.

## D-013 — RNA audit requires the real construct sequence

**Decision:** do not back-translate the protein and treat it as the experimental RNA.

**Required input:** exact nucleotide sequence from the actual HRV-A89 replicon/plasmid around 2C, plus codon-resolved tag designs.

## D-014 — No computationally certified safe-site language

**Decision:** use `candidate`, `low-risk relative to alternatives`, `exclude`, `high risk`, or `literature-rescue`; do not use `safe` as a computational conclusion.

**Biological acceptance gate:** WT-like tagged replicon behavior, appropriate processing/expression/localization, then mechanism experiments.

## D-015 — Direct homolog insertion phenotype is a higher-information evidence layer

**Decision:** Before Tag × Site modeling, integrate direct experimental insertion/deletion fitness from an enterovirus 2C homolog where available and map it explicitly to HRV-A89.

**Reason:** WT structure, conservation and natural indels are proxies for insertion tolerance; direct viral-fitness measurements after insertion/deletion perturbation answer a more closely matched biological question.

## D-016 — DIRECT_INDEL_001 must cover all 320 A89 junctions

**Decision:** Do not use the EV-A71 direct-fitness dataset only to validate the existing `287–291` cluster.

**Reason:** the new evidence must be allowed to overturn the present shortlist, reveal structural-threshold bias and recover candidates outside the current strict structural gate.

## D-017 — Strict structural pass/fail is one view, not the sole discovery authority

**Decision:** retain `strict_structural_pass` for reproducibility but do not treat it as an absolute biological boundary.

**Reason:** hard metric thresholds can create artificial discontinuities. If direct phenotype conflicts with a near-miss site, continuous metrics and Pareto/non-dominated comparisons should be considered.

## D-018 — Phylogeny-aware evolution and independent-indel events are optional hardening layers

**Decision:** If direct InDel evidence leaves meaningful ambiguity, improve the evolutionary layer with phylogeny-aware site rates and independent natural-indel-event inference rather than relying only on entropy/sequence counts.

**Reason:** many descendant sequences carrying one ancestral event are not equivalent to repeated independent tolerance events.

## D-019 — Insertion-specific conformational sampling should precede expensive MD

**Decision:** When Tag × Site modeling begins, prefer insertion-specific loop/conformer ensembles and orthogonal methods rather than a single tagged AlphaFold model.

**Preferred logic:** focused Rosetta loop/remodel/KIC-like sampling + AlphaFold/ColabFold ensemble comparison where feasible, followed by hexamer compatibility analysis.

**Reason:** WT loop geometry does not directly measure whether an inserted peptide can close without strain.

## D-020 — RNA/codon analysis becomes a mandatory final construct gate

**Decision:** Protein-level ranking can proceed without the nucleotide sequence, but no final construct recommendation should be issued until exact experimental RNA/codon context is audited.

**Reason:** an insertion changes viral RNA as well as protein sequence.

## D-021 — HRV-A89-specific insertion fitness is the experimental gold standard

**Decision:** If experimental resources permit, prefer a full or targeted HRV-A89 2C insertion scan/replicon fitness panel over indefinite computational refinement.

**Reason:** direct A89 phenotype would outrank homolog mapping and computational proxies and can serve as an empirical validation/training set.

## D-022 — Current project state is `NO_HIGH_CONFIDENCE_TARGETED_SITE_YET`

**Decision:** Do not promote the previous `287|288–290|291` cluster as a targeted shortlist, but do not infer universal HRV-A89 insertion impossibility from EV-A71 alone.

**Reason:** EV-A71 direct 8-aa insertion fitness strongly contradicts the old structure/conservation shortlist, yet homolog transfer and insertion-sequence dependence remain material limitations.

## D-023 — EV-A71 direct insertion phenotype is a strong prior, not a universal binary veto

**Decision:** Treat the mapped EV-A71 insertion phenotype as a high-weight evidence layer. It can demote candidates, but it does not by itself prove that every MAP8/HA/G196 insertion at the homologous A89 junction will fail.

**Reason:** sequence background, local epistasis, insert identity/length and RNA/polyprotein context differ between the homolog dataset and the planned A89 constructs.

## D-024 — Global re-ranking must retain all 320 junctions with continuous metrics

**Decision:** The next site-discovery stage must re-rank the full 320-junction landscape. `strict_structural_pass` remains an annotation, not the membership rule.

**Method:** use transparent evidence classes and Pareto/non-dominated comparisons rather than a single opaque weighted score.

## D-025 — Add substitution tolerance, phylogeny-aware indels and tag-specific PLM before structural Tag × Site modeling

**Decision:** Authorize `METHOD_HARDENING_002` before Rosetta/AlphaFold/ColabFold tag modeling.

**Scope:**

- EV-A71 substitution-tolerance integration;
- continuous/Pareto all-320 ranking;
- independent natural-indel-event inference;
- MAP8/HA/G196-specific PLM insertion perturbation scans.

**Reason:** these layers have higher expected information gain than immediately modeling a shortlist that direct homolog phenotype has already challenged.

## D-026 — Reinterpret current candidate groups as conflict controls

**Decision:**

- `287|288`, `288|289`, `289|290`, `290|291` → `STRUCTURE_EVOLUTION_FAVORED__DIRECT_HOMOLOG_CONFLICT`;
- `248|249`, `256|257` → `HISTORICAL_INSERTION_SUPPORT__MODERN_CONFLICT_CONTROL`.

**Reason:** preserve informative contradictions rather than averaging them away or presenting them as preferred sites.

## D-027 — ONE_SHOT_COMPUTATIONAL_AUDIT_003 ended in `METHOD_HARDENING_BLOCKED`

**Decision:** Do not authorize automatic Tag × Site modeling from the current one-shot run.

**Reason:** EV-A71 substitution, Pareto and phylogeny-aware indel analyses completed, but the mandatory MAP8/HA/G196 PLM insertion scan was blocked by unavailable mature PLM/GPU software and rejected dependency installation. Cross-tag consensus is therefore unresolved.

## D-028 — V4 review set is not a modeling shortlist

**Decision:** Treat `data/computational_review_set_v1.tsv` as a conflict-aware review set only.

**Reason:** all reviewed rows remain either direct-homolog-conflicted, high-risk, mapping-uncertain, historically conflicted or negative controls. No row is validated or selected for experimental construct design.

## D-029 — direct login execution of GPU_RECOVERY_004 had no GPU visible

**Decision:** Preserve the initial direct-login GPU check as provenance only, not the final task state.

**Reason:** required checks on `admin1` showed no `nvidia-smi`, empty `CUDA_VISIBLE_DEVICES` and no `/dev/nvidia*`. The task was subsequently rerun through Slurm on `gpu15`.

## D-030 — GPU_RECOVERY_004 completed the tag-specific PLM layer

**Decision:** Treat `data/candidate_junctions_v5_plm_gpu.tsv` and `data/computational_review_set_v2_plm_gpu.tsv` as the current PLM-integrated computational state for ChatGPT/user review.

**Reason:** Slurm job `164151` ran on `gpu15` with NVIDIA GeForce RTX 3090 and completed ESM2 `esm2_t6_8M_UR50D` full-sequence masked pseudo-log-likelihood scoring for all 1,280 planned MAP8 / HA / G196 rows. PLM remains secondary computational evidence and does not validate any insertion site or override direct homolog phenotype.

## D-031 — CONTINUOUS_TAG_SITE_MODELING_005 is partial, not a final construct gate

**Decision:** Treat `docs/CONTINUOUS_TAG_SITE_MODELING_005_REPORT.md` and `data/tag_site_integrated_perturbation_v1.tsv` as the current conflict-aware tag-site perturbation state, with final state `TAG_SITE_MODELING_PARTIALLY_COMPLETE`.

**Reason:** The task completed the compact 33-junction x 4-tag panel, WT oligomer-context analysis, WT residue-contact-network anchor analysis, targeted reuse of V5/V2 direct/evolutionary/PLM evidence and cross-method robustness. Mature insertion-specific structure-prediction ensembles, Rosetta/KIC-like loop remodeling and FoldX/Rosetta/local-frustration energy analysis were not available and were explicitly deferred rather than fabricated.

**Interpretation:** `289|290` and `290|291` with MAP8 or G196_minimal are the lowest relative perturbation rows among completed layers, but they retain direct homolog insertion conflict and are not safe, validated, or final construct recommendations. `248|249`, `256|257`, `203|204` and `224|225` are structurally/context constrained in this panel. G196_minimal is locally useful but not globally less disruptive than MAP8/HA.
