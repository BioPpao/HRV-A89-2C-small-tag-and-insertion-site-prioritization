# Active task

Current task: `STRUCTURE_STACK_RECOVERY_006` — **AUTHORIZED / CONTINUITY-FIRST ENVIRONMENT + MODELING TASK**

Branch: `analysis/conservation-002`

Task specification:

`tasks/STRUCTURE_STACK_RECOVERY_006.md`

## Entering state

`CONTINUOUS_TAG_SITE_MODELING_005` completed all independent WT-anchor/context analyses that were possible with the available software, but primary insertion-specific structure/loop/energy methods remained deferred.

Current project state entering this task:

`TAG_SITE_MODELING_PARTIALLY_COMPLETE`

## Primary technical decision

Use **ColabFold / `colabfold_batch` as the required primary structure engine**.

Do not install standalone AlphaFold, OpenFold and ESMFold by default because they are largely redundant for the current evidence class and would add environment/storage complexity without proportionate information gain.

Install an alternative structure engine only if ColabFold cannot be made scientifically usable after reasonable recovery attempts.

## Additional methods

- configure OpenMM/structural-analysis utilities as open support tools;
- use Rosetta/PyRosetta for loop/backbone modeling only if an existing licensed installation is available or user-provided license access permits installation;
- use FoldX only if an existing licensed installation is available or user action provides legitimate access;
- missing licensed Rosetta/FoldX components must not stop ColabFold/tagged-structure/network/hexamer analyses.

## Continuity requirement

Do not stop because:

- login node has no GPU;
- one Slurm partition is busy or misconfigured;
- compute node has no internet;
- one package installation fails;
- Rosetta/FoldX requires user license action;
- Git push temporarily fails.

Recover by using Slurm, login-node download/cache, alternative mature methods, deferred-module status, and local commits as appropriate.

A single local method failure is not a project-wide blocker.

## Storage rule

Do not install a full local ColabFold/MMseqs sequence database for this targeted project unless clearly required and storage/quota has been explicitly verified.

Prefer public MSA-server generation from a network-capable login context, cache A3M/MSA inputs, and run GPU inference from cached resources on Slurm nodes.

## Authorized task scope

1. storage/quota and environment audit;
2. install/configure ColabFold GPU stack and prove it with a real WT A89 2C smoke test;
3. build a tiered tagged-construct structural panel;
4. run multi-model/multi-seed inserted-construct ensembles;
5. compute actual WT-vs-tagged structural perturbation metrics;
6. perform OpenMM relaxation/QC where useful;
7. perform Rosetta/PyRosetta loop modeling if legitimately available, otherwise defer only that module;
8. perform FoldX/Rosetta/local-frustration energy analysis if legitimately available, otherwise defer only that module;
9. replace WT-only hexamer proxies with tagged-structure clash/interface context where models exist;
10. replace WT-only contact-network proxies with WT-vs-tagged network deltas;
11. integrate evidence and run cross-method robustness;
12. produce final report and repository-state updates.

## Required final report

`docs/STRUCTURE_STACK_RECOVERY_006_REPORT.md`

## Final state

Return exactly one of:

- `READY_FOR_TARGETED_DYNAMIC_ANALYSIS`
- `NO_COMPUTATIONAL_CONSENSUS_SITE`
- `STRUCTURE_STACK_PARTIALLY_COMPLETE`

Do not automatically start long MD, final experimental construct recommendation, experimental protocol design, or final RNA/codon design.
