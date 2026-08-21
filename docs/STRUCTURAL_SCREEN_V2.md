# Four-structure all-atom insertion-junction screen V2

Status: quantitative structural screen; **not a final cloning recommendation**.

## Inputs

- `fold_hrv_2c_full_model_1.cif`
- `fold_hrv_2c_full_model_3.cif`
- `selected_hexamer_01_md_representative.pdb`
- `selected_hexamer_02_md_representative.pdb`

All structures contain the same HRV-A89 2C sequence and use residue numbering 1–321. Each hexamer contains chains A–F, each 1–321.

## Methods upgraded from V1

V1 used a simple C-alpha inter-protomer distance proxy. V2 replaces that with an all-atom screen:

1. DSSP simplified secondary structure (`H/E/C`) in both AF monomers and all six protomers in both hexamers.
2. Per-residue SASA using the Shrake–Rupley algorithm.
3. Relative SASA (rSASA) normalized with Tien et al. maximum ASA values.
4. For each hexamer chain, SASA was calculated both in the intact hexamer and in the isolated protomer.
5. `DeltaSASA = SASA_isolated - SASA_hexamer`; burial fraction = `DeltaSASA / SASA_isolated`.
6. Minimum heavy-atom distance from each residue to any other protomer.
7. Inter-protomer heavy-atom contacts within 4.5 Å.
8. Hexamer center/axis derived from the six aa112–321 C-alpha centers; per-residue radial distance was used only as a pore-orientation proxy.
9. Metrics were aggregated across all six chains and across both lead/control hexamers.
10. The screen operates on peptide junctions `i|i+1`, not on single residues.

The pore metric is a **model-dependent penalty**, not a hard functional conclusion.

## Structural funnel

Starting universe: 320 internal peptide junctions.

| Sequential structural gate | Junctions remaining |
|---|---:|
| both flanking residues are coil in both AF models | 88 |
| additionally coil in >=80% protomers in both hexamers | 82 |
| additionally minimum AF rSASA >=0.25 | 33 |
| additionally minimum mean hexamer rSASA >=0.25 | 20 |
| additionally maximum burial across any chain/model <0.10 | 10 |
| additionally minimum inter-protomer heavy-atom distance >4.5 Å | 10 |

This deliberately strict gate leaves **10 structurally clean junctions**.

## Ten junctions passing the strict structural gate

| Junction | Functional tier V3 | min AF rSASA | min hexamer rSASA | max burial | min inter-protomer distance (Å) | pore radial proxy (Å) |
|---|---|---:|---:|---:|---:|---:|
| 155|156 | EXCLUDE | 0.438 | 0.442 | 0.000 | 5.94 | 9.31 |
| 174|175 | HIGH_RISK | 0.274 | 0.288 | 0.000 | 6.62 | 14.61 |
| 175|176 | HIGH_RISK | 0.268 | 0.287 | 0.000 | 8.94 | 15.50 |
| 216|217 | EXCLUDE | 0.323 | 0.306 | 0.075 | 5.54 | 24.57 |
| 217|218 | HIGH_RISK | 0.346 | 0.329 | 0.000 | 7.91 | 24.57 |
| 218|219 | HIGH_RISK | 0.573 | 0.623 | 0.000 | 9.90 | 28.69 |
| 287|288 | HIGH_RISK | 0.267 | 0.273 | 0.000 | 7.98 | 35.35 |
| 288|289 | HIGH_RISK | 0.396 | 0.460 | 0.000 | 7.98 | 40.48 |
| 289|290 | HIGH_RISK | 0.396 | 0.460 | 0.000 | 11.41 | 45.22 |
| 290|291 | HIGH_RISK | 0.366 | 0.389 | 0.000 | 14.08 | 46.09 |

## Central result

**None of the 10 junctions that pass the strict structural gate survives as a low-risk biological site.**

- `155|156` is inside the 9A5 epitope and touches A89 Y156, the aligned CVB3 H163/FMDV H147-equivalent aromatic pore-loop position.
- `174|175` and `175|176` are immediately downstream of Walker B.
- `216|217` touches motif-C N216.
- `217|218` and `218|219` remain immediately adjacent to motif C.
- `287|288`, `288|289`, `289|290`, and `290|291` are geometrically attractive but lie in the Cys/Zn-to-C-terminal-bundle transition. This region is not promoted without conservation and tag-specific modeling.

This is the most important V2 conclusion: **excellent surface-loop geometry is not sufficient for 2C**.

## Newly resolved RNA-function conflict

The 2026 FMDV 2C:RNA preprint, together with direct alignment through CVB3 Nancy 2C, maps the conserved RNA-binding triad to A89:

- CVB3 A204 -> A89 A197
- CVB3 L206 -> A89 L199
- CVB3 K209 -> A89 K202

Therefore the V1 geometrically interesting junctions around `196|197`, `197|198`, `200|201` are now strongly disfavored for a new reason: they flank residues homologous to experimentally supported RNA-binding/replication determinants.

The same mapping places CVB3 H163 at A89 Y156, directly inside the 9A5 epitope. This strengthens exclusion of `155|156` beyond the antibody-confounding argument.

## A89-specific annotation resolves several previous uncertainties

UniProt P07210 gives A89-specific coordinates (mostly By similarity):

- membrane-binding aa1–70;
- oligomerization aa1–134;
- RNA-binding aa22–26;
- SF3 helicase domain aa94–254;
- ATP-binding aa124–131;
- structural Zn-binding C262/C273/C278, zinc-finger aa262–278;
- C-terminal RNA-binding aa305–312;
- C-terminal oligomerization aa316–321.

This explains why the structurally exposed aa113–117 loop should not be treated as benign: it is within both the A89 SF3-domain context and the N-terminal oligomerization annotation.

## Secondary exploratory junctions that do not pass the strict gate

A few junctions are worth retaining only for later comparison, not cloning:

- `223|224`: reproducible coil, but one hexamer/model shows meaningful burial (~15%) and it lies between motif C and the R-finger within the SF3 core.
- `245|246`: exposed and far from neighboring protomers but not a coil in the AF models; inserting a tag would disrupt structured backbone.
- `250|251`: coil/exposed in the monomer but reaches ~24% burial and ~2.85 Å inter-protomer proximity in at least one hexamer; interface risk is too high.
- `290|291`: best geometry among the C-terminal transition sites, but functional-context risk remains high because it immediately follows the Cys-rich region and precedes the long C-terminal helix/RNA/oligomerization system.

## What V2 does and does not establish

V2 establishes that:
- structural exposure can be quantified consistently across both AF monomers and both hexamers;
- monomer-only inspection would produce false positives;
- several attractive loops coincide with experimentally supported ATPase/RNA features;
- no junction is presently justified as a low-risk experimental construct on structural evidence alone.

V2 does **not** establish that internal tagging is impossible in HRV-A89 2C. The poliovirus transposon screen found 2C unusually insertion-sensitive, which increases the need for a conservative multi-construct experimental design rather than proving impossibility.

## Next gate

The next decisive layer is **near-HRV conservation**, not more MD.

Priorities:
1. build an HRV-A-focused 2C alignment;
2. quantify conservation and indel tolerance around the remaining structurally plausible loops;
3. use HRV-B/C and enteroviruses only as secondary homologous-functional context;
4. then perform tag-specific modeling on a small set of surviving junctions.

If no junction becomes convincingly low-risk after conservation, the project should explicitly report that outcome and move to an experimental insertion-library / minimal-epitope strategy rather than force a single computationally “safe” site.

## Reproducibility files

- `data/junction_structural_metrics_v1.tsv`: all 320 junctions and structural metrics.
- `data/CVB3_to_A89_functional_mapping_v1.tsv`: functional homolog mapping used in the V3 exclusion map.

## Method references

- Tien MZ et al. PLoS ONE. 2013;8:e80635. DOI: 10.1371/journal.pone.0080635.
- MDTraj Shrake–Rupley SASA and DSSP implementation/documentation.
- Pfuetzner RA et al. bioRxiv 2026. DOI: 10.64898/2026.06.07.730651. Preprint.
- UniProtKB P07210 and P03313.
