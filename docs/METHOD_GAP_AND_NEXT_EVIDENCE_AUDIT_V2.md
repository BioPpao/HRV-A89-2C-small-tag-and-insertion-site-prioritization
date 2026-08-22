# METHOD_GAP_AND_NEXT_EVIDENCE_AUDIT_V2

Status: **CURRENT STRATEGIC AUDIT**

Date: 2026-08-22

## 1. Purpose

Re-audit the HRV-A89 2C internal-tag insertion-site workflow after completion of `DIRECT_INDEL_001`, with explicit protection against both optimistic structural bias and over-interpretation of homolog insertion-fitness data.

The project goal remains **relative insertion-site prioritization**, not computational certification of a safe site.

## 2. Updated strategic conclusion

The present evidence does **not** justify either of the following extreme conclusions:

1. `287|288–290|291` is a supported targeted shortlist; or
2. no HRV-A89 2C internal insertion site can possibly work.

The correct current state is:

`NO_HIGH_CONFIDENCE_TARGETED_SITE_YET`

The EV-A71 direct 8-aa insertion phenotype is a stronger evidence class than WT structure/conservation and therefore demotes the previous C-terminal shortlist. However, it remains homolog-specific and insertion-sequence-specific. It should be treated as a strong prior, not as absolute proof that every HRV-A89-specific tag insertion will fail.

Before Tag × Site structure modeling, execute one focused method-hardening phase that re-ranks all 320 junctions with continuous evidence and adds orthogonal insertion-specific sequence/evolutionary layers.

## 3. Evidence that remains decision-grade

Retain without redesign:

- authoritative HRV-A89 2C reference sequence and `i|i+1` junction coordinate system;
- A89-specific functional exclusion/caution map;
- two AlphaFold monomers plus two hexamer structural ensembles;
- regenerated all-320 structural metrics V2;
- ICTV/MAFFT-hardened HRV-A conservation V2;
- explicit natural-indel categories;
- direct EV-A71 2C insertion/deletion/substitution dataset and mature-2C mapping to A89;
- historical poliovirus 2C insertion-tolerance evidence as a conflict/rescue track;
- independent tag evidence screen;
- provenance/versioning policy.

## 4. Main remaining methodological problems

### Gap A — direct homolog insertion phenotype is strong but not absolute

`DIRECT_INDEL_001` found no EV-A71 2C insertion score `>0` for the mapped A89 junction landscape using the 8-aa handle `SGRPGSLS`.

This is strong negative evidence, but it cannot be interpreted as universal HRV-A89 intolerance because:

- EV-A71 and HRV-A89 have different local sequence/epistatic contexts;
- insertion sequence, length, charge and conformational propensity matter;
- viral-fitness readout integrates protein, RNA and polyprotein-context effects;
- historical poliovirus data show that rare viable 2C insertion contexts can exist despite strong global constraint.

Therefore use direct homolog insertion fitness as a high-weight prior, not a universal binary veto.

### Gap B — strict structural gate creates threshold artifacts

The current `strict_structural_pass` is reproducible but should no longer define candidate membership.

Required change:

- retain all 320 junctions;
- use strict pass/fail as an annotation only;
- keep continuous rSASA, burial, interface, secondary-structure and geometric variables;
- use Pareto/non-dominated ranking rather than one opaque weighted score.

Only hard biological exclusions should remove junctions before ranking.

### Gap C — substitution tolerance is underused

The direct EV-A71 dataset contains substitution information in addition to insertion/deletion phenotypes.

Required analysis:

- derive local substitution-tolerance summaries around each mapped A89 junction;
- distinguish insertion phenotype from substitution tolerance rather than merging them;
- test whether relatively mutation-tolerant local windows identify sites missed by conservation alone;
- retain this as experimental homolog evidence below direct insertion phenotype but above descriptive conservation.

### Gap D — natural-indel counts are not yet phylogenetically independent events

V2 type-aware counting is better than raw sequence counting but can still count one ancestral event many times.

Required improvement:

- build or reuse an HRV-A phylogeny for the curated 2C panel;
- reconstruct presence/absence states for local insertion/deletion events;
- estimate independent indel-event counts per junction/window;
- separate recurrent independent events from inherited lineage-specific gaps.

### Gap E — no tag-specific sequence-model perturbation landscape

Generic homolog insertion phenotype does not answer whether MAP8, HA and G196 differ at the same A89 junction.

Required analysis:

- generate A89 WT and in-silico inserted sequences for MAP8, HA and G196 across all 320 junctions;
- score WT-vs-insert perturbation with an indel-capable protein-language-model method;
- prefer an indel-aware method where practical; otherwise use ESM-family pseudo-log-likelihood carefully;
- report per-tag, per-junction scores separately;
- treat PLM output as secondary evidence that cannot override direct phenotype or hard functional constraints.

### Gap F — WT loop geometry is not insertion-specific backbone feasibility

A WT exposed coil does not establish that 5–9 inserted residues can close with low strain.

Do not run expensive insertion-specific sampling over all 320 sites.

After the global re-ranking reduces the set, perform targeted loop/backbone sampling for approximately 10–20 site × tag pairs using a mature loop-remodeling approach such as Rosetta Remodel/KIC-like sampling, followed by AlphaFold/ColabFold ensemble comparison.

Metrics should include:

- closure success rate;
- local strain/energy proxy;
- native-domain RMSD;
- local backbone displacement;
- steric clashes;
- loss/gain of native contacts;
- oligomer-interface effects;
- tag solvent exposure;
- ensemble convergence.

### Gap G — current hexamers are useful interface hypotheses, not native-state proof

The two A89 hexamers remain no-membrane/no-RNA structural hypotheses.

Use them for comparative interface/exposure/clash risk only. Do not use them to claim absolute native pore geometry or full-length functional-state tolerance.

### Gap H — RNA/codon context remains mandatory before final construct recommendation

No protein-level computation can substitute for the exact experimental nucleotide construct.

Keep RNA/codon analysis blocked until the real replicon/plasmid sequence is supplied.

## 5. Revised evidence hierarchy

When evidence conflicts, use:

1. direct HRV-A89 insertion/replicon phenotype, if generated;
2. direct homolog 2C insertion phenotype with high-confidence A89 mapping;
3. direct homolog substitution/deletion phenotype and direct 2C genetics/biochemistry;
4. experimentally established functional motifs and homolog structures with explicit A89 mapping;
5. A89 continuous structural-ensemble metrics;
6. phylogeny-aware HRV-A natural-indel/evolutionary evidence;
7. tag-specific protein-language-model indel score;
8. insertion-specific loop sampling and tagged AlphaFold/ColabFold ensembles;
9. targeted MD for a reduced construct set only.

No lower-level signal may silently override a stronger direct phenotype or hard biological exclusion.

## 6. Candidate-state reinterpretation

### C-terminal strict cluster

`287|288`, `288|289`, `289|290`, `290|291`

New role:

`STRUCTURE_EVOLUTION_FAVORED__DIRECT_HOMOLOG_CONFLICT`

These remain useful conflict controls because WT geometry and HRV-A variability support review, but EV-A71 direct 8-aa insertion phenotype is unfavorable.

### Literature-rescue controls

`248|249`, `256|257`

New role:

`HISTORICAL_INSERTION_SUPPORT__MODERN_CONFLICT_CONTROL`

Do not promote them as preferred sites. Preserve them because they represent an orthogonal evidence class.

### Near-miss sites

Examples include `223|224`, `245|246`, `250|251`.

Do not promote or discard solely on the previous strict gate. Allow continuous/Pareto re-ranking and new substitution/PLM/phylogenetic layers to reassess them.

## 7. New global-ranking principle

Build a new all-320 table without collapsing the evidence into one weighted scalar score.

Recommended columns/classes:

- hard functional exclusion;
- graded functional risk;
- historical direct 2C insertion/genetics evidence;
- EV-A71 direct insertion phenotype;
- EV-A71 deletion context;
- EV-A71 local substitution tolerance;
- continuous monomer exposure;
- continuous hexamer exposure;
- burial/DeltaSASA;
- inter-protomer/interface metrics;
- local secondary-structure consistency;
- HRV-A conservation/site-rate evidence;
- natural-indel category;
- independent indel-event count;
- tag-specific PLM perturbation for MAP8;
- tag-specific PLM perturbation for HA;
- tag-specific PLM perturbation for G196;
- unresolved conflicts.

Use Pareto/non-dominated candidate discovery plus explicit evidence classes. Do not hide contradictions behind an opaque combined score.

## 8. Recommended next task: METHOD_HARDENING_002

Execute four modules before Tag × Site structure modeling:

1. **EV-A71 substitution-tolerance integration**
   - extract and summarize substitution tolerance around each mapped A89 junction;
   - add explicit columns to a new V4 all-junction matrix.

2. **Continuous/Pareto all-320 ranking**
   - remove strict-pass membership as the candidate funnel;
   - retain strict flags as annotations;
   - generate a Pareto frontier and evidence-class ranking.

3. **Phylogeny-aware natural-indel analysis**
   - estimate independent indel events rather than descendant counts only;
   - report mapping/event uncertainty explicitly.

4. **Tag-specific PLM insertion scan**
   - MAP8, HA and G196 across all 320 A89 junctions;
   - produce separate per-tag perturbation landscapes;
   - use only as an orthogonal secondary layer.

Do **not** start Rosetta/AlphaFold tag modeling inside this task unless the task explicitly reaches its stop criteria and a new modeling task is authorized.

## 9. Stop criteria for METHOD_HARDENING_002

Stop and return for ChatGPT/user review when:

- all four modules have completed or a documented blocker prevents completion;
- a new all-320 integrated matrix exists;
- a Pareto/evidence-class candidate set is defined;
- previous `287–291` and `248/256` hypotheses are explicitly re-evaluated;
- no site is labeled safe or validated;
- Tag × Site structural modeling has not started automatically.

## 10. Decision after METHOD_HARDENING_002

The next review should choose among:

1. a small conflict-aware computational modeling set for insertion-specific loop/AF analysis;
2. `NO_HIGH_CONFIDENCE_TARGETED_SITE` and transition to an empirical validation panel/library strategy;
3. additional method work only if a concrete unresolved decision-critical uncertainty remains.

## 11. Current decision

Authorize `METHOD_HARDENING_002`.

Do not authorize Tag × Site structural modeling or MD yet.
