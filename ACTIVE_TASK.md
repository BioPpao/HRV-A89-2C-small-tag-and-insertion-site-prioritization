# Active task

Current task: `METHOD_HARDENING_002` — **AUTHORIZED / NEXT EXECUTION TASK**

Branch: `analysis/conservation-002`

Task specification:

`tasks/METHOD_HARDENING_002.md`

Strategic basis:

`docs/METHOD_GAP_AND_NEXT_EVIDENCE_AUDIT_V2.md`

## Entering decision state

`NO_HIGH_CONFIDENCE_TARGETED_SITE_YET`

`DIRECT_INDEL_001` is complete and its direct EV-A71 2C 8-aa insertion phenotype demotes the previous `287|288–290|291` targeted shortlist. However, homolog-specific and insertion-sequence-specific transfer limits mean the result is a strong prior, not proof that every HRV-A89-specific tag insertion is impossible.

## Authorized scope

`METHOD_HARDENING_002` must execute four modules:

1. EV-A71 2C substitution-tolerance integration;
2. continuous/Pareto all-320 junction re-ranking, with strict structural pass retained only as an annotation;
3. phylogeny-aware independent natural-indel-event analysis;
4. tag-specific protein-language-model insertion scans for MAP8, HA and G196.

Primary integrated output:

- `data/candidate_junctions_v4_method_hardening.tsv`

Primary report:

- `docs/METHOD_HARDENING_002_REPORT.md`

## Important constraints

- Do not label any junction safe, validated or experimentally proven for HRV-A89.
- Do not treat EV-A71 direct insertion phenotype as a universal binary veto across all A89 tag sequences.
- Do not use `strict_structural_pass` as the sole candidate funnel.
- Do not collapse conflicting evidence into one opaque weighted score.
- Do not start Tag × Site Rosetta/AlphaFold/ColabFold modeling automatically.
- Do not start MD.
- Do not perform final RNA/codon design without the exact experimental nucleotide construct.
- Missing mature software should be installed in user space rather than silently replaced with a materially weaker method.

## Required stop gate

Return for ChatGPT/user review when:

- the four hardening modules are complete or a blocker is documented;
- `candidate_junctions_v4_method_hardening.tsv` exists;
- a Pareto/evidence-class candidate set is defined;
- the `287–291` cluster and `248|249` / `256|257` conflict controls are explicitly re-audited;
- `docs/METHOD_HARDENING_002_REPORT.md` is complete;
- no downstream structural modeling has started automatically.

Expected final state from this task:

- `READY_FOR_CONFLICT_AWARE_TAG_SITE_MODELING`, or
- `NO_HIGH_CONFIDENCE_TARGETED_SITE`, or
- `METHOD_HARDENING_BLOCKED`.
