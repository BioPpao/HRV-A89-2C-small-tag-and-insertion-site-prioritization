# Active task

Current task: `OPEN_STRUCTURE_PIPELINE_007` — **COMPLETE**

Branch: `analysis/conservation-002`

Task specification:

`tasks/OPEN_STRUCTURE_PIPELINE_007.md`

## Completion state

`OPEN_STRUCTURE_PIPELINE_007` completed the open-license inserted-structure recovery path.

Current project state after this task:

`READY_FOR_TARGETED_DYNAMIC_ANALYSIS`

Primary report:

`docs/OPEN_STRUCTURE_PIPELINE_007_REPORT.md`

## Primary route

Use an open/reproducible stack:

- ColabFold / `colabfold_batch` as the primary inserted-structure ensemble engine;
- OpenMM for geometry cleanup/QC only;
- US-align/TM-align for structural comparison;
- MDAnalysis/MDTraj for batch structural metrics;
- DSSP-compatible tooling for secondary-structure preservation;
- transparent contact-network analysis;
- existing A89 hexamer hypotheses for tagged oligomer-context comparison.

Do not require Rosetta, PyRosetta or FoldX. Do not stop to pursue restricted-license software.

## Continuity requirement

The task must continue despite login-node GPU absence, Slurm waiting, compute-node network restrictions, one package failure, or temporary Git push failure.

Use login-node download/MSA/cache plus Slurm GPU inference when appropriate. A single local failure is not a global blocker.

## Storage rule

Do not install a full local ColabFold/MMseqs database unless clearly necessary and storage/quota is explicitly verified.

Prefer public MSA-server generation from the network-capable login context, cache A3M/MSA and parameters, and run GPU inference on Slurm nodes from cached inputs.

## Authorized scope

1. storage/quota/environment audit;
2. install/configure ColabFold and prove it on WT A89 2C;
3. build a tiered tag × site structure panel;
4. generate real multi-model/multi-seed inserted ensembles;
5. compute WT-vs-tagged structural perturbation metrics;
6. perform OpenMM geometry cleanup/QC;
7. quantify secondary-structure/accessibility changes;
8. perform actual tagged hexamer clash/interface analysis;
9. perform actual WT-vs-tagged contact-network analysis;
10. integrate open-tool evidence and run robustness analysis;
11. update repository state and report.

## Required final report

`docs/OPEN_STRUCTURE_PIPELINE_007_REPORT.md`

Status: generated.

## Final state

Return exactly one of:

- `READY_FOR_TARGETED_DYNAMIC_ANALYSIS`
- `NO_COMPUTATIONAL_CONSENSUS_SITE`
- `OPEN_STRUCTURE_PIPELINE_PARTIALLY_COMPLETE`

Do not automatically start long MD, final experimental construct recommendation, experimental protocol design, or final RNA/codon design.

Stop here for ChatGPT/user review before authorizing any targeted dynamic analysis.
