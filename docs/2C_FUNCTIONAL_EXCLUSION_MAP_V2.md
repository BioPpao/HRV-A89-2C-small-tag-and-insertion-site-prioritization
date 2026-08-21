# HRV-A89 2C functional exclusion map V2

Status: literature-audited working map for small-tag insertion-site prioritization.

## Scope and evidence policy

This document separates: (1) residues directly identifiable in the HRV-A89 sequence, (2) homologous functional features supported by enterovirus/picornavirus experiments and structure, and (3) conservative tagging penalties introduced because 2C is unusually insertion-sensitive. Homologous residue numbers are not copied blindly from poliovirus or EV-A71; sequence/structural equivalence is required before a residue is treated as an A89 functional residue.

The current HRV-A89 2C reference sequence is 321 aa.

## Evidence classes

- **HARD EXCLUDE**: do not place an internal epitope tag across this feature in the first experimental batch.
- **STRONG PENALTY**: candidate may be retained only if independent structural/conservation evidence is unusually favorable.
- **CONTEXT PENALTY**: model-dependent feature such as hexamer interface or pore orientation; requires agreement across lead/control models.

## Current A89 map

| A89 region/residue | Feature | Current tagging rule | Evidence basis |
|---|---|---|---|
| aa1–100 | N-terminal membrane-associated functional region | STRONG PENALTY | Poliovirus 2C N terminus is sufficient for membrane targeting; aa19–36 amphipathic helix is essential for membrane-related function, with additional N-terminal residues contributing to membrane/LD localization. HRV orthologous amphipathic helices can functionally substitute in poliovirus chimeras, supporting conservation but not exact A89 boundaries. |
| ~aa15–32 | conserved N-terminal amphipathic-helix core | HARD EXCLUDE for first batch | A89 sequence contains the highly conserved `RGLEWIGQKISKFIDWI`-like segment corresponding to the enterovirus N-terminal amphipathic membrane-binding helix. Exact A89 experimental boundaries remain to be established. |
| aa124–131 | Walker A / P-loop, `GSPGTGKS` | HARD EXCLUDE | Direct sequence identification; canonical SF3/AAA+ ATPase motif. |
| aa148–160 | 9A5 epitope, `YSLPPDPKYFDGY` | HARD EXCLUDE | Project-defined A89 9A5-binding region; inserting here would directly confound the antibody mechanism question. |
| aa165–170 | Walker B neighborhood, `VVIMDD` | HARD EXCLUDE | Direct sequence identification; matches conserved enteroviral Walker-B M/DD chemistry. |
| aa211–216 | motif-C candidate, `VLASTN` with N216 | HARD EXCLUDE pending final structural homolog check | SF3 motif C is a hydrophobic run followed by conserved Asn; poliovirus N223 and EV structures place motif C between beta4 and alpha3. A89 `VLASTN` is the sequence-consistent homologous candidate. |
| R233/R234 | R-finger candidate pair | HARD EXCLUDE pending final structural homolog check | Poliovirus/EV-A71 use the corresponding invariant Arg pair from the neighboring protomer for ATP hydrolysis. A89 contains `...MARRFY...` at aa231–236, consistent with the expected offset. |
| aa261–290 | cysteine-rich / Zn-associated region | HARD EXCLUDE for first batch | A89 contains C262, C273/C274, C278 and C290. EV-A71 C270/C281/C286 coordinate structural Zn and mutations of coordinating cysteines disrupt folding/solubility. Exact A89 Zn coordination still requires structural mapping. |
| aa310–321 | terminal alpha-helix / pocket-binding-domain candidate | HARD EXCLUDE for first batch | Enterovirus 2C C-terminal helix/PBD mediates 2C–2C oligomerization; EV-A71 residues 318–329 form the PBD and mutations of hydrophobic terminal residues disrupt oligomerization. A89 exact residue equivalence must be refined by alignment/structure. |
| any residue with strong inter-protomer burial/contact in both hexamer models | hexamer interface | CONTEXT PENALTY -> HARD if model-consistent | Oligomerization is coupled to ATPase function; a site that is exposed in the AF monomer can become functionally buried in the ring. |
| any model-consistent pore-facing loop | central pore/RNA-path risk | CONTEXT PENALTY | Pore orientation is important for the working hexamer/RNA hypothesis but the current A89 ring is a template-guided model, so pore-facing status alone is not yet a hard exclusion. |

## Important literature-derived constraints

### 1. 2C is unusually insertion-sensitive

Teterina et al. performed transposon-mediated insertion mutagenesis across the poliovirus nonstructural region. At least one site accepting an insertion of five or more residues was recovered in every nonstructural protein except 2C. This does not prove that HRV-A89 2C cannot tolerate an internal tag, but it raises the prior probability of functional disruption and justifies conservative filtering plus multiple backup constructs.

Reference: Teterina NL et al. Virology. 2011;409:1–11. DOI: 10.1016/j.virol.2010.09.028.

### 2. N-terminal membrane function is broader than one short helix

Poliovirus experiments show that the first 72–88 residues are sufficient to confer membrane association, while the amphipathic helix around aa19–36 is a critical core determinant. Later work also identified contributions from residues beyond the helix to lipid-droplet localization. Therefore, only excluding the 18-aa helix would be too permissive for tagging.

References include Paul et al., Virology 1994, DOI 10.1006/viro.1994.1111; Echeverri & Dasgupta, Virology 1995/1998 membrane-binding work; Teterina et al., J Virol 2006, DOI 10.1128/JVI.02684-05.

### 3. ATPase active sites are inter-subunit structures

EV-A71 and other picornavirus 2C structures show that Walker A/B and motif C come from one subunit, while an R finger is supplied by the neighboring subunit. Therefore insertion risk must be evaluated in the hexamer, not only in an isolated monomer.

Reference: Guan H et al. Sci Adv. 2017;3:e1602573. DOI: 10.1126/sciadv.1602573.

### 4. The C-terminal helix is an oligomerization element

EV-A71 2C self-oligomerization is mediated by a C-terminal pocket-binding motif binding a hydrophobic pocket on another 2C molecule. Mutations in terminal hydrophobic residues produce monomeric protein. Thus C-terminal tagging is mechanistically confounded for an oligomerization study.

Reference: Guan H et al. Sci Adv. 2017;3:e1602573.

### 5. RNA-related risk must be handled cautiously

Biochemical work shows enteroviral 2C binds RNA and RNA stimulates ATPase activity, but residue-level RNA-path assignments differ among constructs and the HRV-A89 hexamer/RNA geometry is not experimentally solved. The current project should therefore apply an RNA/pore penalty where multiple models agree rather than declare every pore-facing residue absolutely forbidden.

Reference: Yeager et al. Nucleic Acids Res. 2022/2023; enteroviral 2C is an RNA-stimulated ATPase. PMID: 36399514.

## Corrected workflow implication

The insertion-site screen is not a single-residue ranking. The unit is each peptide junction `i|i+1`. Before numerical ranking, junctions crossing hard-exclusion regions are removed or assigned a prohibitive penalty. Remaining junctions are evaluated by:

1. secondary-structure context in AF model_1/model_3 and both hexamer models;
2. local solvent exposure;
3. inter-protomer contact/burial;
4. pore-facing risk;
5. structural consistency across models;
6. sequence conservation, with near-HRV sequences used for quantitative conservation and distant picornaviruses used primarily for homologous functional mapping;
7. tag-specific steric/structural compatibility.

## Current unresolved items

- Confirm A89 motif C and R-finger by explicit sequence/structure alignment to EV-A71/PV experimental structures.
- Resolve A89 C-terminal PBD equivalence residue by residue rather than by length offset alone.
- Quantify per-junction exposure and interface metrics in both uploaded hexamer models.
- Quantify secondary-structure consensus across the four uploaded structures.
- Obtain the exact experimental replicon nucleotide sequence before the final construct decision; do not infer RNA-level safety from protein sequence alone.

## Decision boundary

No site in this map is called "safe" by computation. The output of this project is a ranked set of low-risk constructs for experimental validation against WT replicon behavior.