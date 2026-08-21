# Preliminary four-structure insertion-junction screen V1

Status: preliminary structural screen. This is **not** the final candidate list.

## Inputs checked

- `fold_hrv_2c_full_model_3.cif`: full-length HRV-A89 2C, chain A, residues 1–321.
- `fold_hrv_2c_full_model_1.cif`: full-length HRV-A89 2C, chain A, residues 1–321.
- `selected_hexamer_01_md_representative.pdb`: six chains A–F, each residues 1–321.
- `selected_hexamer_02_md_representative.pdb`: six chains A–F, each residues 1–321.

All four structural inputs use the same 321-aa reference sequence and residue numbering.

## Methods in this preliminary pass

This first pass intentionally uses metrics that can be computed robustly before the final SASA/conservation layer:

1. secondary structure from a DSSP-compatible geometric assignment on AF model_1 and model_3;
2. nearest inter-protomer C-alpha distance in both hexamer structures;
3. hard/strong functional-region filtering from `2C_FUNCTIONAL_EXCLUSION_MAP_V2.md`;
4. junction-level rather than residue-level screening: a junction is represented as `i|i+1`.

A junction passed this preliminary geometric gate only when both flanking residues were coil/loop in **both** AF models and both residues were >8 Å from the nearest C-alpha of another protomer in **both** hexamer structures. This >8 Å C-alpha criterion is only an interface-risk proxy; final interface burial must use all-atom contacts/SASA.

## AF structural consistency

The two AF models are highly consistent in the ATPase/C-terminal body. Secondary-structure assignment is also strongly concordant. The major model uncertainty remains the N-terminal placement rather than gross rearrangement of the ATPase core.

## Preliminary junctions passing the narrow geometry gate

The following 19 junctions pass only the loop + inter-protomer C-alpha-distance gate:

| Junction | Context note |
|---|---|
| 113|114 | immediately upstream of Walker-A region; high functional proximity |
| 114|115 | immediately upstream of Walker-A region; high functional proximity |
| 115|116 | immediately upstream of Walker-A region; high functional proximity |
| 116|117 | immediately upstream of Walker-A region; high functional proximity |
| 174|175 | immediately downstream of Walker B; high functional proximity |
| 175|176 | immediately downstream of Walker B; high functional proximity |
| 176|177 | immediately downstream of Walker B; high functional proximity |
| 187|188 | ATPase-core loop; requires nucleotide-pocket/homology audit |
| 196|197 | ATPase-core loop; requires nucleotide-pocket/homology audit |
| 197|198 | ATPase-core loop; requires nucleotide-pocket/homology audit |
| 200|201 | ATPase-core loop; requires nucleotide-pocket/homology audit |
| 206|207 | immediately upstream of motif-C candidate; high functional proximity |
| 207|208 | immediately upstream of motif-C candidate; high functional proximity |
| 219|220 | downstream of motif C and upstream of R-finger region; high functional proximity |
| 220|221 | downstream of motif C and upstream of R-finger region; high functional proximity |
| 221|222 | downstream of motif C and upstream of R-finger region; high functional proximity |
| 222|223 | downstream of motif C and upstream of R-finger region; high functional proximity |
| 223|224 | downstream of motif C and upstream of R-finger region; high functional proximity |
| 224|225 | downstream of motif C and upstream of R-finger region; high functional proximity |

## Interpretation

The most important result of this preliminary screen is **not** that these 19 sites are good candidates. In fact, most of them fall inside or immediately adjacent to the ATPase core and conserved catalytic architecture. They are expected to be heavily down-ranked or excluded after functional-homology and conservation analysis.

This is scientifically useful because it shows why a simple rule such as "choose an exposed loop" would fail for 2C: several geometrically accessible loops sit directly beside Walker A, Walker B, motif C or the R-finger architecture.

## C-terminal observations

The region after the cysteine-rich/Zn-associated segment is structurally constrained:

- residues 292–293 are beta-strand in both AF models;
- residue 294 is a short coil position;
- residues ~295–320 are predominantly helical in both AF models;
- the terminal helix approaches inter-protomer contacts in the hexamer, consistent with a C-terminal oligomerization role.

Thus the apparently exposed region around 291–294 is not yet a clean tag insertion loop: it sits directly next to the Zn-associated region and transitions into the long C-terminal helix/PBD system.

## N-terminal/core-boundary observations

Residues 113–117 form a reproducible loop in AF model_1 and model_3, but this loop lies immediately before the beta-strand and Walker-A/P-loop beginning at aa124. Its apparent exposure therefore cannot be interpreted as safety. A conservative first-batch strategy should treat this region as high-risk until active-site structural mapping is complete.

## Next required analyses before ranking any site

1. Explicit EV-A71/PV structure/sequence mapping for motif C, R finger, adenine-recognition and C-terminal PBD residues.
2. All-atom inter-protomer contacts and residue burial rather than C-alpha-distance proxy alone.
3. Residue/junction solvent accessibility and monomer-to-hexamer accessibility change.
4. Near-HRV conservation analysis; distant picornavirus homologs used for functional mapping, not pooled entropy.
5. Pore-facing orientation as a model-consistency penalty.
6. Only after these layers are complete should a shortlist of approximately 3–8 junctions be generated for tag-specific modeling.

## Current decision

No insertion site has yet been promoted to an experimental construct. The present 19-junction list is an intermediate geometry gate and should not be used directly for cloning.