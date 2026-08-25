# Integrated Scientific Synthesis V1

Date: **2026-08-25**

Status represented: **`EXPERIMENTAL_REVIEW_SHORTLIST_READY_FOR_DISCUSSION`**

## 1. Scientific question

The project asks which **internal peptide junction × small-tag combination** in HRV-A89 2C is sufficiently plausible to justify experimental testing while minimizing predicted perturbation of a highly constrained, multifunctional viral protein.

The question is deliberately not phrased as “find the safest loop”. A surface-exposed or flexible loop is only one layer of evidence. A useful internal tag must simultaneously remain detectable and avoid unacceptable interference with 2C functional architecture, oligomerization, RNA-related biology, ATPase-related structure/dynamics and the encoded viral RNA context.

The computational endpoint is therefore **prioritization under uncertainty**, not computational certification of safety.

---

## 2. Why HRV-A89 2C is a difficult internal-tag target

A89 2C is 321 aa and combines several overlapping biological constraints. The repository functional map includes:

- an N-terminal membrane-associated region, with strongest penalty near the amphipathic/membrane-binding portion;
- an SF3/AAA+-like ATPase core;
- Walker A/P-loop around A89 aa124–131;
- the project-defined 9A5-binding region aa148–160;
- Walker B around aa165–170;
- motif C around aa210–216;
- R-finger region around R233/R234;
- historical poliovirus insertion-tolerance mappings near A89 `248|249` and `256|257`, retained as literature-rescue conflicts rather than automatically favorable sites;
- a Cys/Zn-related region around aa262–278;
- C-terminal RNA-/oligomerization-related constraints.

This explains the central structural-screen result: a junction can be geometrically attractive while remaining biologically high-risk.

---

## 3. Evidence hierarchy

The report uses an explicit evidence hierarchy rather than one opaque total score.

A practical ordering is:

1. direct HRV-A89 phenotype, when available;
2. direct homolog insertion phenotype;
3. homolog genetics/biochemistry and experimentally established functional constraints;
4. experimentally supported structural motifs/functional regions;
5. A89-specific structural context;
6. evolution, conservation and indel context;
7. protein-language-model evidence;
8. inserted-structure/tag modeling;
9. comparative replicated MD.

Comparative MD is intentionally downstream. A construct cannot become biologically “safe” because its short fragment MD looks stable if stronger biological evidence remains unfavorable.

---

## 4. Global 320-junction search

All 320 internal peptide junctions were retained as the initial universe.

The four-structure all-atom structural funnel used two AF monomers plus two no-membrane/no-RNA hexamer hypotheses and evaluated:

- local secondary structure;
- AF and hexamer solvent exposure;
- burial upon oligomerization;
- inter-protomer heavy-atom proximity;
- a model-dependent pore-orientation proxy.

The sequential strict structural gates reduced 320 junctions to 10 geometrically clean junctions:

`155|156`, `174|175`, `175|176`, `216|217`, `217|218`, `218|219`, `287|288`, `288|289`, `289|290`, `290|291`.

However, none became a low-risk biological site because all overlap or neighbor functional constraints. The key conclusion is therefore:

> **Excellent surface-loop geometry is not sufficient evidence for internal tagging of 2C.**

The interactive 320-junction landscape in the HTML report is intended to preserve this global perspective and prevent the final shortlist from appearing to have been selected from only a few hand-picked locations.

---

## 5. Conservation and indel evidence

The hardened conservation analysis used an ICTV-defined HRV-A type universe, MAFFT L-INS-i and a 77-type full panel plus a 186-sequence expanded panel.

The V2 junction categories were:

- 69 conserved;
- 113 intermediate;
- 125 variable;
- 13 lineage-indel-supported.

The C-terminal `287–291` cluster remained reviewable after evolutionary QC but retained functional-context risk.

`248|249` remained particularly informative because it combines broader-lineage indel support and historical poliovirus insertion-tolerance mapping with unfavorable structural/functional context. It is therefore a genuine **conflict-rich hypothesis**, not a clean positive site.

---

## 6. Direct homolog insertion evidence changes the interpretation

Direct insertion fitness is more relevant to this project than ordinary substitution tolerance because the experimental manipulation is an insertion.

Current leading sites still carry unfavorable EV-A71 direct-insertion priors:

- `289|290`: direct insertion strongly deleterious, approximately log2 fitness `-3.52` in the project-integrated table;
- `248|249`: direct insertion strongly deleterious, approximately log2 fitness `-5.69`.

Therefore “Priority A” must never be read as “direct evidence says this site is tolerant”. It means that, among the remaining conflict-rich alternatives, the construct is sufficiently informative and comparatively favorable across other evidence layers to justify experimental testing.

---

## 7. Tag identity is an independent experimental variable

The project does not treat all short peptide tags as interchangeable.

Tag ranking considers:

- peptide footprint;
- sequence chemistry;
- direct internal-loop evidence;
- binder-recognition geometry;
- orthogonality in human cells;
- WB/IP/IF or quantitative-readout utility;
- reagent maturity;
- compatibility with the specific 2C mechanistic context.

The principal advanced tag forms are MAP8, HA and G196 minimal. AGIA, ALFA, PA12 and HiBiT remain meaningful alternatives with specific strengths and liabilities. FLAG, 6×His, Myc, V5, Spot, C-tag/EPEA and emerging systems were not advanced for distinct project-specific reasons.

A dedicated file in this report folder, `TAG_SELECTION_RATIONALE_V1.md`, records the detailed logic and gives 6×His special treatment because its very small size can otherwise make its exclusion seem counterintuitive.

---

## 8. Broad replicated MD and why it was not accepted at face value

Task 009 generated:

- WT + 12 tagged systems;
- 3 independent replicas per system;
- 39 trajectories;
- 20 ns per trajectory;
- 780 ns total legacy production sampling.

The trajectories remained valuable, but the first analysis layer had decision-relevant methodological problems:

- no explicit PBC make-whole/unwrap/center preprocessing;
- RMSD was primarily self-drift rather than deviation from a common WT reference;
- local RMSF lacked proper junction-matched WT baselines;
- contact retention preserved candidate-start contacts rather than a WT-defined native-contact graph;
- tag accessibility relied too heavily on distance/collapse proxies rather than true SASA;
- the old Tier A/B penalty system could over-interpret incomplete metrics;
- the CHARMM36 nonbonded settings needed correction before any new production extension.

This produced a deliberate project decision: **do not automatically extend all 39 trajectories to 50 ns; fix the analysis first.**

---

## 9. Task 010 corrected analysis and CHARMM36 validation

Task 010 repaired the key analysis semantics and performed a reduced corrected-protocol validation subset rather than blanket extension.

The corrected validation contained:

- WT;
- `289|290 × MAP8`;
- `248|249 × HA`;
- `256|257 × MAP8`;
- `224|225 × MAP8`;
- `155|156 × MAP8`;

with 3 independent replicas × 20 ns per system, for 18 trajectories / 360 ns.

All 18 trajectories passed trajectory-level integrity QC.

The corrected protocol used the GROMACS/CHARMM36 force-switch style settings documented in the repository, including `vdw-modifier = force-switch`, `rvdw-switch = 1.0`, `rlist = 1.2` and `DispCorr = no`.

Key corrected-validation results included:

- `289|290 × MAP8`: WT-reference RMSD ~1.94 Å, WT-defined contact retention ~0.902, nonlocal tag-contact fraction ~0.028; interpreted as MD-neutral/supportive at screening level;
- `248|249 × HA`: WT-reference RMSD ~1.60 Å, WT-defined contact retention ~0.910, mean nonlocal tag-contact fraction ~0.592; global perturbation remained mild but the replica-level contact behavior was heterogeneous;
- `224|225 × MAP8`: nonlocal tag-contact fraction 1.0; MD caution reproduced;
- `155|156 × MAP8`: nonlocal tag-contact fraction ~0.919; MD caution reproduced;
- `256|257 × MAP8`: comparatively MD-neutral despite biological/oligomer conflict, a useful demonstration that MD cannot replace higher-level biological evidence.

---

## 10. Why 20 ns was retained rather than forcing 50 ns

Task 010A separated three concepts that must not be conflated:

- **directional drift observed**;
- **threshold-crossing extension trigger**;
- **candidate-specific excess drift relative to WT**.

For `289|290 × MAP8`, late-minus-early values were:

- self-drift RMSD: candidate `+0.487 Å`, WT `+0.631 Å`, difference `-0.144 Å`;
- WT-reference RMSD: candidate `+0.416 Å`, WT `+0.364 Å`, difference `+0.052 Å`;
- WT-defined contact retention: candidate `-0.0338`, WT `-0.0060`, difference `-0.0278`.

Thus the trajectory shows real directional relaxation, but the project did not identify a decision-relevant multi-metric candidate-specific excess-drift pattern requiring further sampling.

`STOP_AT_20NS` means:

> sufficient for the current **screening-level prioritization objective**.

It does **not** mean complete molecular convergence, mechanistic proof or biological validation.

---

## 11. Replica heterogeneity matters: 248|249 × HA

The three corrected-protocol nonlocal tag-contact fractions were:

`0.761194`, `0.263682`, `0.751244`.

Mean = `0.592`; SD ≈ `0.284`.

The average alone would obscure the fact that two replicas show high nonlocal contact while one does not. Therefore the final interpretation is:

> **Priority A with accessibility/contact heterogeneity caution.**

The construct is retained because global perturbation metrics remain comparatively mild and it provides an independent non-C-terminal hypothesis, but the heterogeneity is shown explicitly rather than averaged away.

---

## 12. Current 4+2 experimental-review shortlist

### Candidate 1 — `289|290 × MAP8`

Role: primary C-terminal MAP8 hypothesis.

Supporting features:

- comparatively favorable C-terminal structural geometry;
- high tag exposure;
- low corrected nonlocal tag contact;
- directly corrected-protocol validated, 3 × 20 ns;
- no decision-relevant multi-metric excess drift after WT comparison.

Major conflicts:

- high-risk ATPase-to-Cys/Zn/C-terminal transition context;
- unfavorable direct EV-A71 insertion prior;
- no direct HRV-A89 insertion phenotype;
- fragment/no-membrane/no-RNA MD limitations.

### Candidate 2 — `289|290 × G196_minimal`

Role: same-site tag-identity comparator and minimal-footprint branch.

Strength:

- tests whether behavior at `289|290` depends on tag identity;
- smaller nominal peptide footprint than MAP8.

Boundary:

- not directly tested in the corrected-protocol 18-trajectory subset;
- the practical G196 construct may need flanking residues, so a nominal 5-aa footprint is not automatically the final biological footprint.

### Candidate 3 — `248|249 × HA`

Role: primary non-C-terminal HA hypothesis.

Strength:

- preserves regional diversity instead of collapsing the panel entirely onto `287–291`;
- historical insertion/literature-rescue logic plus lineage-indel support;
- high tag SASA;
- directly corrected-protocol validated;
- comparatively mild global structural perturbation.

Conflicts:

- strongly unfavorable direct EV-A71 insertion prior;
- structural/oligomer context conflict;
- replica-dependent nonlocal tag-contact heterogeneity.

### Candidate 4 — `248|249 × MAP8`

Role: cross-site MAP8 comparator.

This construct allows a direct site comparison while holding tag identity constant:

`289|290 × MAP8` versus `248|249 × MAP8`.

It is not directly corrected-protocol validated and retains the 248-region biological conflicts.

### Control — `224|225 × MAP8`

Role: MD conflict control.

The corrected simulations reproduce persistent nonlocal tag contact. It tests whether the computational contact-caution signal has experimental relevance.

### Hard negative — `155|156 × MAP8`

Role: hard-negative control.

This junction overlaps the project-defined 9A5 region and an aligned RNA/pore-related functional warning. It also reproduces high nonlocal tag-contact caution in corrected validation.

---

## 13. Experimental design logic

The four candidate constructs are best described as a **partially crossed two-site tag-comparison design**, not a full `2 × 2` factorial because three tag identities are present.

| Site | MAP8 bridge | Alternative tag |
|---|---|---|
| `289|290` | MAP8 | G196_minimal |
| `248|249` | MAP8 | HA |

This supports three useful comparisons:

1. site effect with MAP8 held constant: `289|290 MAP8` vs `248|249 MAP8`;
2. tag-identity effect at 289: MAP8 vs G196_minimal;
3. tag-identity effect at 248: MAP8 vs HA.

It does not estimate one universal tag effect across both sites and should not be described as a complete factorial interaction design.

---

## 14. What the project knows and does not know

### Current evidence supports

- a global, reproducible 320-junction prioritization framework;
- the conclusion that geometry alone is insufficient;
- explicit preservation of direct-homolog and functional conflicts;
- robust identification of a small experimental-review panel;
- evidence that `224|225 × MAP8` and `155|156 × MAP8` carry persistent tag-contact cautions in corrected validation;
- screening-level support for stopping blanket MD extension at 20 ns.

### Current evidence does not establish

- WT-like viral fitness for any tagged construct;
- preserved ATPase activity;
- preserved RNA-related function;
- correct behavior in the full native membrane/oligomer/RNA state;
- actual antibody/binder accessibility in the biological complex;
- absence of RNA/codon-level effects in the replicon;
- a computationally certified “safe insertion site”.

---

## 15. Highest-value next information

The next major uncertainty-reducing information is experimental rather than generic additional MD:

- direct HRV-A89 tagged-construct phenotype;
- detectability/accessibility of the selected tags;
- whether candidate constructs outperform the conflict/hard-negative controls;
- exact experimental replicon/plasmid nucleotide sequence for final codon/RNA-context audit.

Only after those data exist should broader mechanistic simulation be reconsidered for a specific experimental question.

---

## 16. Bottom-line interpretation

The current computational study does **not** identify a universally safe tag site. It produces a conflict-aware experimental strategy.

The leading C-terminal construct is `289|290 × MAP8`; `248|249 × HA` provides an intentionally independent non-C-terminal hypothesis with an explicit contact-heterogeneity caution. `289|290 × G196_minimal` and `248|249 × MAP8` allow tag/site comparisons, while `224|225 × MAP8` and `155|156 × MAP8` provide negative calibration.

The most important methodological achievement is not the name of one junction, but the preservation of contradictory evidence and the correction of the initial MD analysis before it was allowed to influence experimental prioritization.
