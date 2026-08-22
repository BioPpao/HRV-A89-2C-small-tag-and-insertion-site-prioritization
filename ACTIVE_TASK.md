# Active task

Current task: `CONTINUOUS_TAG_SITE_MODELING_005` — **AUTHORIZED / CONTINUITY-FIRST COMPUTATIONAL TASK**

Branch: `analysis/conservation-002`

Task specification:

`tasks/CONTINUOUS_TAG_SITE_MODELING_005.md`

## Entering state

`GPU_RECOVERY_004` is complete and the project state is:

`READY_FOR_CONFLICT_AWARE_TAG_SITE_MODELING`

The next task moves from all-320 site discovery into reduced, insertion-specific structural perturbation modeling.

## Continuity policy

This task must keep working when one tool, package, GPU allocation, scheduler context, network route, or preferred method is unavailable.

A local method failure is not a reason to stop the whole task.

Required behavior:

- if GPU is not visible in the current shell, inspect Slurm and request/submit GPU work as needed;
- continue CPU-capable modules while waiting where useful;
- if compute-node network access fails, download/cache dependencies from a network-capable login context and reuse them inside the job;
- if a preferred package fails, try another mature method in the same evidence class;
- if no mature replacement exists, mark only that module deferred and continue all independent modules;
- if Git push fails, continue local analysis and preserve commits/results for a later push;
- do not restart already completed global analyses unless a concrete QC failure is identified.

## Authorized scope

1. Build a compact conflict-aware site × tag modeling panel from V5/V2 review data.
2. Run insertion-specific structure-prediction ensembles using the strongest mature available workflow.
3. Add loop/backbone feasibility modeling where available.
4. Add local energetic/frustration analysis where available.
5. Add oligomer-context compatibility analysis.
6. Add residue-contact-network perturbation analysis.
7. Add targeted orthogonal evolutionary/statistical checks where technically defensible.
8. Integrate separate evidence layers without one opaque total score.
9. Run cross-method robustness analysis.
10. Produce a final report and update repository state.

## Reuse upstream evidence

Do not rerun by default:

- EV-A71 substitution/insertion/deletion integration;
- all-320 Pareto ranking;
- phylogeny-aware independent-indel analysis;
- GPU ESM2 all-320 tag-specific PLM scan;
- V5 PLM-integrated matrix;
- V2 computational review set.

## Do not auto-escalate to

- long MD;
- final experimental construct recommendation;
- experimental protocol design;
- final RNA/codon design without exact experimental nucleotide input.

No site may be called safe or experimentally validated for HRV-A89.

## Required final report

`docs/CONTINUOUS_TAG_SITE_MODELING_005_REPORT.md`

## Final state

Return exactly one of:

- `READY_FOR_TARGETED_DYNAMIC_ANALYSIS`
- `NO_COMPUTATIONAL_CONSENSUS_SITE`
- `TAG_SITE_MODELING_PARTIALLY_COMPLETE`
