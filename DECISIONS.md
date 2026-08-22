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
