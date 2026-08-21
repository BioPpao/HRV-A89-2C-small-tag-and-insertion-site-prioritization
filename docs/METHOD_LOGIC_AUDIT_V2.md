# Method logic audit V2

Project: **HRV-A89 2C small-tag and insertion-site prioritization**

Date: 2026-08-21

## Bottom line

The overall strategy is sound, but the first draft contained several over-broad assumptions. They are corrected here before candidate ranking.

## Corrections

1. **Do not treat aa1–110 as a blanket insertion-exclusion zone.** Direct poliovirus work places the major N-terminal membrane-binding determinant in the first ~40–70 residues, and recent reconstitution work resolves amphipathic membrane-binding elements near the N terminus. The entire aa1–110 region should therefore be screened with graded evidence, not painted red by default.
2. **Do not treat the whole C-terminal region as forbidden.** C-terminal Zn/ZFER and PBD/PBL oligomerization elements are high-risk, but direct poliovirus genetics recovered viable linker insertions after 2C residues 255 and 263. These historical positive-tolerance observations must be mapped explicitly to HRV-A89 and retained as a separate evidence layer.
3. **A lack of insertion hits in a transposon screen is not proof that 2C cannot tolerate insertions.** Teterina et al. recovered no transposon insertion in 2C, but explicitly discussed earlier viable 4-aa and 6-aa insertions in 2C. We therefore model 2C as unusually insertion-sensitive, not insertion-intolerant in absolute terms.
4. **Pore risk must not be inferred from the project hexamer geometry alone.** The 2026 FMDV 2C:RNA cryo-EM preprint reports a spiral-staircase/split-ring holoenzyme. Our no-RNA template-guided HRV-A89 rings are structural hypotheses. Pore penalties therefore combine experimentally mapped homologous RNA-contact residues with geometric proxies from both A89 models.
5. **Conservation is supporting evidence, not a safety criterion by itself.** Conservation will be calculated hierarchically (HRV-A, HRV-A/B/C, enterovirus/picornavirus) because lineage-specific functions and indels can otherwise distort interpretation.
6. **The unit of insertion ranking is the peptide junction `i|i+1`, but every junction must carry the properties of both flanking residues and its local window.** A single-residue SASA value is insufficient.
7. **AlphaFold/structure prediction of tagged constructs is a perturbation screen, not validation.** Low confidence in the tag peptide itself is not failure; changes in native 2C fold, interfaces, pore geometry and functional motifs are the relevant outputs.
8. **RNA-level risk is more than local MFE.** Final constructs require the actual replicon nucleotide sequence, codon-resolved tag designs, local RNA folding and a check for plausible long-range/cis-acting effects and accidental protease-cleavage-like sequence context.
9. **Tag ranking must include experimental reagent practicality.** FLAG is excluded from this project. Other tags will be scored for internal-insertion evidence, sequence/structure footprint, orthogonality, WB/IF/IP performance and reagent requirements.
10. **Direct positive-tolerance evidence receives a separate literature-rescue score.** A junction can remain experimentally interesting even if one computational proxy is unfavorable, but conflicting evidence must be reported rather than averaged away.

## Phase 0 structure audit — completed

All four supplied structures were inspected before insertion-site ranking.

| structure | chain(s) | residues/chain | numbering | sequence |
|---|---|---:|---|---|
| `fold_hrv_2c_full_model_1.cif` | A | 321 | 1–321, no gaps | matches reference |
| `fold_hrv_2c_full_model_3.cif` | A | 321 | 1–321, no gaps | matches reference |
| `selected_hexamer_01_md_representative.pdb` | A–F | 321 | 1–321, no gaps | six copies match reference |
| `selected_hexamer_02_md_representative.pdb` | A–F | 321 | 1–321, no gaps | six copies match reference |

Key Cα RMSD after least-squares superposition:

| comparison | full 1–321 | aa112–258 | aa112–321 | aa148–160 |
|---|---:|---:|---:|---:|
| AF model 3 → lead hexamer chain A | 0.707 Å | 0.563 Å | 0.655 Å | 0.341 Å |
| AF model 1 → control hexamer chain A | 0.449 Å | 0.398 Å | 0.451 Å | 0.249 Å |
| AF model 3 ↔ AF model 1 | 1.474 Å | 0.135 Å | 0.157 Å | 0.045 Å |

Interpretation:

- The ATPase/C-terminal assembly region is essentially identical between AF model 1 and model 3; most AF ensemble variation comes from the full-length/N-terminal arrangement.
- The selected short-MD hexamers remain close to their source monomers after superposition.
- All six protomers are retained as an ensemble because MD introduces modest protomer-to-protomer asymmetry. Insertion-site metrics must therefore aggregate across both AF monomers and all 12 hexamer protomers rather than relying on chain A alone.

## Corrected evidence hierarchy

`direct 2C genetics/biochemistry > experimental homolog structures > explicit A89 sequence alignment > A89 monomer ensemble > A89 hexamer ensemble > conservation > tag-specific modelling`

No single layer can declare a site safe.

## Next executable stages

1. Build the homolog-mapped functional constraint table.
2. Compute the full 321-residue / 320-junction structural feature table.
3. Overlay direct functional constraints and direct insertion-tolerance evidence.
4. Add hierarchical conservation.
5. Produce a short list of candidate junctions before any tag is inserted.
6. Rank small tags independently, then evaluate tag × site combinations.
7. Perform tagged-construct perturbation modelling only on the reduced set.
8. Add replicon nucleotide/RNA checks before experimental construct selection.

## Primary references used for this correction

- Li JP, Baltimore D. *J Virol.* 1988. DOI: `10.1128/JVI.62.11.4016-4021.1988`.
- Teterina NL et al. *Virology.* 2011. DOI: `10.1016/j.virol.2010.09.028`.
- Guan H et al. *Sci Adv.* 2017. DOI: `10.1126/sciadv.1602573`.
- Chen P et al. *Nucleic Acids Res.* 2022. DOI: `10.1093/nar/gkac671`.
- Yeager C et al. *Nucleic Acids Res.* 2022. DOI: `10.1093/nar/gkac1054`.
- Sadeghipour S et al. *PLoS Pathog.* 2024. DOI: `10.1371/journal.ppat.1012388`.
- Pfuetzner RA et al. bioRxiv 2026. DOI: `10.64898/2026.06.07.730651` (preprint, not peer reviewed).