# Decision Log

Last updated: 2026-08-21

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

**Reason:** literature supports graded N-terminal membrane/RNA/oligomerization constraints, with the strongest evidence concentrated in defined subregions. The region is high risk but not uniformly equivalent.

## D-006 — Do not automatically ban the entire C terminus

**Decision:** treat Zn/Cys, RNA-binding and terminal oligomerization elements as high-risk/hard features, but preserve direct historical insertion-tolerance observations in a separate rescue track.

**Reason:** poliovirus literature reports viable small insertions at defined 2C positions; conflicting direct evidence should not be erased by a broad structural exclusion.

## D-007 — Functional evidence outranks attractive loop geometry

**Decision:** an exposed coil/loop is not sufficient for promotion.

**Reason:** the current strict structural screen found 10 geometrically clean junctions, yet all overlap or neighbor biologically high-risk regions.

## D-008 — Pore geometry is a penalty, not direct proof

**Decision:** use project-hexamer pore orientation/radial metrics as context penalties only.

**Reason:** current A89 hexamers are no-RNA template-guided hypotheses; the experimental 2C:RNA holoenzyme geometry is from a homolog and must not be conflated with the project ring.

## D-009 — No final site before near-HRV conservation

**Decision:** do not select a final candidate junction until HRV-A-focused conservation and indel-tolerance analysis is complete.

**Reason:** the remaining plausible loops need lineage-relevant evolutionary context.

## D-010 — Conservation is not a standalone safety criterion

**Decision:** use conservation hierarchically and as supporting evidence.

**Hierarchy:** HRV-A quantitative conservation > HRV-A/B/C context > enterovirus/picornavirus homologous functional mapping.

## D-011 — No additional generic MD as the current priority

**Decision:** do not spend the next analysis cycle on longer generic no-membrane MD.

**Reason:** current decision uncertainty is dominated by functional/conservation/site evidence, not by insufficient extension of the existing short no-membrane trajectories.

## D-012 — Tagged-structure prediction is a perturbation screen

**Decision:** AlphaFold/structural modeling of tagged constructs may rank perturbation risk but cannot validate a construct.

**Primary outputs:** native 2C fold deviation, local backbone displacement, interface/pore conflict, functional-feature distortion, tag accessibility.

**Not a failure criterion by itself:** low confidence/flexibility of the inserted tag peptide.

## D-013 — RNA audit requires the real construct sequence

**Decision:** do not back-translate the protein and treat it as the experimental RNA.

**Required input:** exact nucleotide sequence from the actual HRV-A89 replicon/plasmid around 2C, plus codon-resolved tag designs.

## D-014 — No computationally certified “safe site” language

**Decision:** use `candidate`, `low-risk relative to alternatives`, `exclude`, `high risk`, or `literature-rescue`; do not use `safe` as a computational conclusion.

**Biological acceptance gate:** WT-like tagged replicon behavior, appropriate processing/expression/localization, and then mechanism experiments.
