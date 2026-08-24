# Active task

Current task: `BROAD_DYNAMICS_AND_RECOVERY_009` — **AUTHORIZED / PRE-DYNAMICS RECOVERY + BROAD REPLICATED DYNAMICS**

Branch: `analysis/broad-dynamics-009`

Task specification:

`tasks/BROAD_DYNAMICS_AND_RECOVERY_009.md`

## Entering state

`CANDIDATE_PANEL_EXPANSION_008` completed on `analysis/candidate-panel-008` with final state:

`READY_FOR_BROAD_TARGETED_DYNAMICS`

The 008 checkpoint is preserved unchanged. Task 009 proceeds on a new branch so the diversified candidate-panel checkpoint remains reproducible.

## Why 009 is not a simple MD launch

Task 008 left several important issues that must be resolved before or alongside broad replicated dynamics:

- one `248|249 × HA` OpenMM model failed with `Particle coordinate is nan`;
- local tagged dimer/trimer accommodation modeling was deferred;
- disorder/disordered-binding prediction remained incomplete;
- the proposed dynamics panel remained biased toward the contiguous `287–291` C-terminal neighborhood and MAP8;
- PA14/AGIA were reviewed but not actually structure-modeled;
- current rigid oligomer placement does not allow local neighboring-protomer accommodation.

Task 009 therefore first hardens these missing layers, freezes a balanced dynamics panel, then runs broad replicated comparative dynamics.

## Authorized scope

1. environment/storage/Slurm integrity audit;
2. root-cause and recover the `248|249 × HA` OpenMM NaN failure;
3. recover an open disorder/flexibility layer for all 320 junctions;
4. complete focused local tagged dimer/trimer ColabFold accommodation modeling;
5. perform focused real structure modeling for PA14 and AGIA at representative junctions;
6. redesign the dynamics panel to reduce C-terminal and MAP8 selection bias;
7. install/configure any necessary open dynamics/QC/analysis tools;
8. prepare a standardized comparative A89 2C `112–321` soluble-domain screening system for WT and tagged constructs;
9. run multiple independent explicit-solvent MD replicas per system using one consistent force field;
10. analyze structural persistence, local/tag flexibility, tag exposure, contact persistence and replicate convergence;
11. perform dynamic correlation/network analysis;
12. integrate dynamics with all prior evidence without an opaque weighted score;
13. produce a revised Tier A / Tier B / control candidate panel.

## Primary dynamics policy

Broad screening dynamics is a comparative perturbation assay, not a complete biological-state simulation.

Because full-length 2C contains a membrane-associated N terminus, the primary broad screen uses native A89 residues `112–321` with equivalent terminal treatment across WT and all tagged constructs. This retains all 009 insertion sites while avoiding a bulk-water full-length membrane-anchor artifact.

Default target:

- 3 independent replicas × 50 ns per system;
- minimum broad-coverage fallback: 3 × 20 ns before any selective extension;
- WT reference under the identical protocol.

Prefer replica breadth over one long trajectory.

## Stop gate

Do not automatically proceed after 009 to:

- final wet-lab construct design;
- exact RNA/codon design without the real nucleotide construct;
- membrane/RNA/ATP mechanistic MD;
- experimental protocol design.

## Final state

Return exactly one of:

- `READY_FOR_FINAL_CANDIDATE_PANEL_REVIEW`
- `READY_FOR_EXACT_NUCLEOTIDE_AUDIT`
- `BROAD_DYNAMICS_PARTIALLY_COMPLETE`
