# METHOD_GAP_AND_NEXT_EVIDENCE_AUDIT_V1

Status: **CURRENT STRATEGIC REVIEW**

Date: 2026-08-22

## 1. Purpose

Reassess whether the current HRV-A89 2C insertion-site prioritization pipeline is sufficiently complete before Tag × Site modeling.

This audit deliberately searches for evidence that could overturn the current shortlist rather than merely confirm `287–291`.

## 2. Main conclusion

The current pipeline is scientifically useful but still biased toward **WT structural geometry + descriptive conservation as proxies for insertion tolerance**.

Before committing to tagged-structure modeling, the project should add a higher-value evidence layer: **direct experimental insertion/deletion fitness data from an enterovirus 2C homolog**, then remap that evidence to all 320 HRV-A89 junctions.

The highest-priority external dataset identified is the EV-A71 proteome-scale deep insertion/deletion scanning study by Bakhache et al. (Nature Microbiology; DOI / source details to be verified and registered during execution). The study includes 2C and directly measures viral fitness after insertion/deletion perturbations.

## 3. Current method strengths

Already decision-grade or mature enough for present use:

- authoritative A89 321-aa reference and junction numbering;
- A89-specific functional exclusion/caution map;
- two AF monomers + two hexamer ensembles;
- all-320-junction structural metrics regenerated as V2;
- ICTV-reconciled HRV-A conservation V2 using MAFFT L-INS-i;
- type-aware natural-indel categorization;
- independent tag evidence screen;
- explicit preservation of literature-rescue conflicts;
- repository provenance and reproducible environment policy.

## 4. Main scientific gaps

### Gap A — no direct homolog insertion-fitness landscape

Current structure/conservation layers are proxies. Direct experimental insertion fitness is a stronger evidence class.

Required action:

1. retrieve the EV-A71 deep insertion/deletion processed dataset and source metadata;
2. isolate the 2C measurements;
3. establish exact EV-A71 2C sequence and numbering;
4. map EV-A71 2C junctions to HRV-A89 using sequence alignment and, where useful, structural mapping;
5. project experimental insertion/deletion evidence onto all 320 A89 junctions;
6. explicitly quantify mapping confidence and ambiguous/gap-adjacent mappings;
7. re-evaluate the entire 320-junction landscape, not only the current shortlist.

### Gap B — structural hard-threshold bias

`strict_structural_pass` is useful as a reproducible screen but can create threshold artifacts. A junction immediately below one threshold may be nearly equivalent to one immediately above it.

Required future improvement:

- retain continuous metrics;
- add Pareto/non-dominated ranking across exposure, burial, interface, local secondary structure and functional penalties;
- use strict pass/fail as one view rather than the sole site-discovery funnel.

### Gap C — conservation is not insertion tolerance

Substitution variability and Shannon entropy do not establish tolerance of an added 5–10 aa peptide.

Required future improvement:

- consider phylogeny-aware site-rate analysis;
- distinguish independent natural indel events from one ancestral indel inherited by many descendants;
- retain conservation as supporting evidence only.

### Gap D — no insertion-specific conformational sampling

WT loop geometry does not directly answer whether two flanking residues can accommodate an inserted peptide without excessive strain.

Required later modeling layer:

- insertion-specific loop/conformer sampling;
- preferably an orthogonal ensemble approach such as Rosetta loop/remodel/KIC-like sampling plus AlphaFold/ColabFold ensemble comparison;
- compare closure success, local strain/energy, native-domain RMSD, clashes, interface effects and tag exposure.

### Gap E — no orthogonal sequence-model score

Protein language models may provide an independent sequence-level perturbation score, but must not override direct phenotype or functional evidence.

Possible later analysis:

- generic small-insertion scan over all 320 junctions;
- WT-vs-insert pseudo-log-likelihood / indel-effect score;
- use only as a secondary orthogonal ranking layer.

### Gap F — exact RNA-level constraint remains unresolved

Insertion adds nucleotides to an RNA-virus genome. Protein-level compatibility cannot guarantee RNA-level compatibility.

Final construct selection must include exact experimental nucleotide context and evaluate local RNA/codon effects. Do not back-translate the protein as a substitute.

## 5. Evidence hierarchy after this audit

Use the following order when conflicts arise:

1. direct HRV-A89 insertion/replicon phenotype, if generated;
2. direct homolog 2C insertion/deletion phenotype with high-confidence A89 mapping;
3. direct 2C genetics/biochemistry and experimentally established functional motifs;
4. experimental homolog structures and explicit A89 mapping;
5. A89 structural ensemble metrics;
6. phylogeny-aware near-HRV evolutionary evidence / natural indel history;
7. protein-language-model scores;
8. tagged-structure prediction and loop modeling as perturbation-ranking evidence.

No lower layer may silently override a stronger direct phenotype or hard functional constraint.

## 6. Candidate-confirmation-bias control

The current `287|288–290|291` cluster remains a useful working hypothesis, but the next analysis must be allowed to demote it.

The EV-A71 direct-fitness mapping must therefore be performed across **all 320 A89 junctions**.

Explicitly search for:

- current strict-pass sites contradicted by homolog experimental intolerance;
- current near-miss/non-strict sites with strong homolog experimental insertion tolerance;
- regions where structural and experimental evidence disagree;
- potential new candidates outside the current 10 strict structural passes.

## 7. Current candidate status pending direct InDel evidence

Do not finalize these as construct sites.

Working hypotheses only:

- `288|289` — strong current computational candidate;
- `289|290` — strong current computational candidate with C290/C-terminal-transition caution;
- `287|288`, `290|291` — secondary structural candidates;
- `248|249`, `256|257` — literature-rescue/conflict controls.

All may change after direct homolog InDel mapping.

## 8. Recommended next work order

### P0 — DIRECT_INDEL_001

Acquire and map EV-A71 2C direct insertion/deletion fitness to HRV-A89 all-320 junctions.

### P1 — integration / shortlist re-audit

Rebuild the candidate matrix using direct homolog phenotype as an independent evidence layer. Reconsider structural near-misses.

### P2 — optional method hardening

If the direct dataset materially changes rankings or leaves major ambiguity:

- phylogeny-aware evolutionary-rate / independent-indel-event analysis;
- continuous/Pareto structural ranking;
- protein-language-model insertion scan.

### P3 — insertion-specific Tag × Site modeling

Only after P0/P1:

- focused site × tag matrix;
- insertion-specific loop sampling plus AF/ColabFold ensemble;
- then hexamer compatibility analysis.

### P4 — targeted MD

Only for a reduced set of model-supported constructs; do not return to generic WT-only MD.

### P5 — RNA/codon gate

Mandatory before final construct recommendation once exact experimental nucleotide sequence/context is available.

## 9. Experimental gold-standard option

If experimental resources allow, the strongest future route is an HRV-A89-specific insertion-tolerance experiment rather than indefinite computational refinement.

Preferred levels:

1. full 2C deep insertion scan across 320 junctions;
2. if full DMS is impractical, a targeted 20–30-junction panel spanning structural-positive, conservation-positive, homolog-DMS-positive, literature-rescue and negative-control classes;
3. use replicon/viral fitness to create an A89-specific empirical training/validation set.

## 10. Decision

**Do not authorize TAG_SITE_MODELING_001 yet.**

The next execution task is `DIRECT_INDEL_001` because direct homolog phenotype has greater expected information gain and can challenge the present shortlist before expensive tag-specific structural work.
