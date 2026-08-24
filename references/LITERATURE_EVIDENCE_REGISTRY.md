# Literature Evidence Registry

Last updated: 2026-08-25

Purpose: map each literature source to the **specific claim it is allowed to support** in this project. This avoids silently turning homologous or computational evidence into direct HRV-A89 evidence.

## Evidence classes

- **A — direct 2C genetics/biochemistry**: strongest functional constraint evidence, but species/strain mapping still matters.
- **B — experimental homolog structure/function**: strong mechanistic evidence requiring explicit mapping to A89.
- **C — A89 database annotation / sequence evidence**: directly located on A89 sequence, but many annotations are transferred by similarity.
- **D — project structural model**: useful for ranking geometry; not direct biological proof.
- **E — tag-system evidence**: supports tag properties, not 2C tolerance.

## 2C insertion tolerance and genetics

| Source | Class | What it supports here | What it does **not** prove |
|---|---|---|---|
| Li JP, Baltimore D. *J Virol.* 1988. DOI `10.1128/JVI.62.11.4016-4021.1988` | A | historical evidence that some small insertions in poliovirus 2C can be viable; used to preserve a literature-rescue track | does not make the homologous A89 junction automatically safe |
| Teterina NL et al. *Virology.* 2011;409:1–11. DOI `10.1016/j.virol.2010.09.028` | A | 2C is unusually insertion-sensitive in a systematic poliovirus nonstructural-protein insertion screen; tag identity can affect fitness independently of site | does not prove all internal insertions in HRV-A89 2C are impossible |
| Bakhache W et al. *Nat Microbiol.* 2025;10:158–168. DOI `10.1038/s41564-024-01871-y`; Dryad DOI `10.5061/dryad.866t1g1xm`; GitHub `QVEU/eva71_dimple` commit `c99331a60980f68bb0141506e750e8339f278d08` | A / direct homolog phenotype | EV-A71 2C direct insertion/deletion/substitution viral-fitness layer mapped to all 320 A89 junctions in `docs/EV71_2C_DIRECT_INDEL_MAPPING_V1.md`; supports `DIRECT_EVIDENCE_REQUIRES_SHORTLIST_REVISION` because all mapped 2C handle-insertion scores are unfavorable | homolog EV-A71 evidence using 8 aa insertional handle `SGRPGSLS`; does not directly validate or reject an HRV-A89 construct or a different tag chemistry |

## 2C ATPase / oligomerization / structural-function evidence

| Source | Class | What it supports here | Boundary |
|---|---|---|---|
| Guan H et al. *Sci Adv.* 2017;3:e1602573. DOI `10.1126/sciadv.1602573` | B | enterovirus 2C ATPase architecture, Walker motifs, motif C, inter-subunit active-site logic, Arg-finger/PBD-related oligomerization constraints | EV-A71 structure; residue numbers must be aligned to A89 |
| Chen P et al. *Nucleic Acids Res.* 2022. DOI `10.1093/nar/gkac671` | B | picornavirus 2C oligomerization/PBD-pocket structural context used in the previous hexamer project | homolog structure, not direct A89 hexamer proof |
| Yeager C et al. *Nucleic Acids Res.* 2022. DOI `10.1093/nar/gkac1054` | A/B | modern 2C functional/genetic context used to refine residue-level constraints | exact claims must be taken from the paper, not generalized across all picornaviruses |
| Sadeghipour S et al. *PLoS Pathog.* 2024. DOI `10.1371/journal.ppat.1012388` | A/B | modern N-terminal/membrane-function context for 2C | does not justify painting all A89 aa1–110 as a hard exclusion zone |

## RNA / pore-function evidence

| Source | Class | What it supports here | Boundary |
|---|---|---|---|
| Pfuetzner RA et al. bioRxiv 2026. DOI `10.64898/2026.06.07.730651` | B, **preprint** | residue-level 2C:RNA holoenzyme/pore-contact hypotheses; motivates mapping of conserved RNA-contact residues and treating pore geometry cautiously | not peer reviewed; FMDV system and trapping conditions are not direct HRV-A89 evidence |
| CVB3 Nancy 2C sequence/functional mapping via UniProt P03313 and explicit alignment | B/C | maps homologous residues such as the A197/L199/K202 RNA-contact triad and R233/R234 Arg-finger pair to A89 | alignment must be preserved and auditable; chemistry is not assumed when non-conserved |

## HRV-A89-specific annotation

| Source | Class | What it supports here | Boundary |
|---|---|---|---|
| UniProtKB P07210 (HRV-A89/HRV-89 strain 41467-Gallo) | C | direct A89 coordinate framework for the 2C chain, membrane-binding/oligomerization/RNA-binding/Zn-related annotations and polyprotein cleavage boundaries | many features are annotated **By similarity**, not by direct A89 mutagenesis |
| PROSITE-ProRule annotation carried by P07210 | C | approximate SF3 helicase-domain context around A89 aa94–254 | domain context is not equivalent to a residue-by-residue hard exclusion map |

## Conservation data sources

| Source | Class | What it supports here | Boundary |
|---|---|---|---|
| UniProtKB REST API records under NCBI Taxonomy `147711` queried on 2026-08-21 | C / conservation dataset | HRV-A 2C sequence panel for residue/junction conservation and natural indel screen in `docs/CONSERVATION_SCREEN_V1.md` | many retained records used A89 local-alignment provisional extraction because exact mature-chain coordinates were sparse; see `references/CONSERVATION_DATA_SOURCES.md` and metadata |
| NCBI Taxonomy E-utilities subtree `txid147711[Subtree]` queried on 2026-08-21 | C / taxonomy source | source-state expected/observed/missing HRV-A type labels for CONSERVATION_001 | taxonomy subtree includes isolates and no-rank records; parsed labels are current-source bookkeeping, not ICTV manual curation |
| UniProtKB REST API records under NCBI Taxonomy `147712` and `463676` queried on 2026-08-21 | C / secondary context | sparse HRV-B/C context for candidate windows | only 3 HRV-B and 3 HRV-C retained sequences passed the same boundary/QC workflow; not used as primary entropy score |
| ICTV Virus Metadata Resource `VMR_MSL41.v1.20260729.xlsx` downloaded from `https://ictv.global/vmr/current` on 2026-08-21 | C / official taxonomy source | authoritative CONSERVATION_002 HRV-A type universe under species `Enterovirus alpharhino`; 80 HRV-A type rows | VMR provides exemplar/accession metadata, not mature 2C boundaries |
| NCBI Nucleotide GenBank records listed in ICTV VMR, retrieved on 2026-08-21 | C / sequence source | V2 full type-balanced panel via polyprotein CDS translation and A89-local 2C extraction | extraction is provisional unless mature 2C coordinates are explicit; A106-A108 did not yield accepted 2C sequence |
| UniProt exact `Chain: Protein 2C` records retained in CONSERVATION_002 exact-boundary subset | C / sequence source | exact-boundary sensitivity subset for A1/A1B/A2/A16/A89 context | subset N is 5 and too small to replace full ICTV type-balanced panel |

## Structural metric methodology

| Source | Class | Use |
|---|---|---|
| Tien MZ et al. *PLoS ONE.* 2013;8:e80635. DOI `10.1371/journal.pone.0080635` | method | maximum accessible surface areas used for relative SASA normalization |
| MDTraj Shrake–Rupley SASA / DSSP implementation | method | reproducible per-residue SASA and secondary-structure calculations in the structural screen |

## Molecular-dynamics audit methodology

| Source | Class | What it supports here | Boundary |
|---|---|---|---|
| Knapp B, Ospina L, Deane CM. *J Chem Theory Comput.* 2018. DOI `10.1021/acs.jctc.8b00391` | method | Task 010 emphasizes independent replicas and avoids treating frames as independent biological replicates | does not prescribe a universal number of replicas or make 20 ns mechanistically converged |
| *Reliability and reproducibility checklist for molecular dynamics simulations*. *Communications Biology.* 2023. DOI `10.1038/s42003-023-04653-0` | method/reporting | Task 010 reports protocol, inputs, validation status, convergence and limitations explicitly | checklist compliance does not validate any insertion site experimentally |
| GROMACS 2024 documentation, CHARMM force-field/nonbonded recommendations | method/software | Task 010 corrected MDP set uses force-switch style CHARMM36 settings and `DispCorr = no` as protocol validation target | software documentation is a simulation-protocol reference, not biological evidence |
| MDAnalysis 2.9.0 transformations | method/software | Task 010 PBC unwrap/center preprocessing for geometry-dependent metrics | preprocessing correctness was cross-checked only on representative RMSD cases |
| MDTraj 1.10.3 Shrake-Rupley and DSSP routines | method/software | Task 010 tag SASA and local secondary-structure persistence | SASA/DSSP are structural proxies and do not establish antibody binding or viral fitness |

## Tag-system evidence

| Tag/system | Key source | Class | Allowed project inference |
|---|---|---|---|
| MAP/MAP8 | Wakasa A et al. *J Biochem.* 2020;168:375–384. DOI `10.1093/jb/mvaa054`; Fujii Y et al. 2016 DOI `10.1089/mab.2016.0039` | E | MAP8 has direct structure-guided internal-loop insertion evidence in multiple proteins; useful primary modeling candidate |
| G196 | Tatsumi K et al. *Sci Rep.* 2017;7:43480. DOI `10.1038/srep43480` | E | minimal `DLVPR` epitope can be recognized with high affinity; practical constructs may use GS flanks |
| AGIA | Yano T et al. *PLoS One.* 2016;11:e0156716. DOI `10.1371/journal.pone.0156716` | E | compact antibody tag with strong detection performance; internal constrained-loop evidence is limited |
| ALFA | Götzke H et al. *Nat Commun.* 2019;10:4403. DOI `10.1038/s41467-019-12301-7` | E | highly orthogonal/high-affinity tag system; its helical tendency and larger footprint are structural concerns for short native loops |
| PA | Fujii Y et al. *Protein Expr Purif.* 2014;95:240–247. DOI `10.1016/j.pep.2014.01.009`; Tamura R et al. *J Cell Sci.* 2016;129:1512–1522. DOI `10.1242/jcs.176685` | E | strong turn/loop insertion precedent | human podoplanin-derived system can create context-dependent background concerns in human cells |
| HA | mature conventional epitope system; viral tagging precedent evaluated in the project literature | E | benchmark with strong WB/IP/IF practicality | no direct evidence that HA is safe inside HRV-A89 2C |
| HiBiT | NanoLuc complementation literature/product documentation | E | highly sensitive quantitative reporter branch | not equivalent to an antibody epitope for every IP/IF/complex-capture use case |

## Project-model evidence that must remain separate from literature

The following are **not literature evidence** and must not be cited as if experimentally demonstrated:

- `selected_hexamer_01_md_representative.pdb` and `selected_hexamer_02_md_representative.pdb` are project structural hypotheses derived from template-guided assembly and short MD screening.
- Pore radial distance, interface burial, rSASA and local geometry derived from those structures are ranking features.
- A favorable score does not establish native oligomerization, RNA translocation, membrane topology or tag tolerance.

## Citation practice for future reports

For every candidate-site claim, record at least:

1. the A89 junction/residue;
2. the direct structural metric(s);
3. the functional/homolog source supporting any exclusion or rescue;
4. whether the evidence is direct, by similarity, homologous, preprint or model-derived;
5. the unresolved contradiction if evidence layers disagree.

Do not collapse conflicting evidence into a single opaque score without preserving the components.

## Candidate-panel expansion 008 evidence additions

| Source | Class | What it supports here | Boundary |
|---|---|---|---|
| Bakhache W et al. Nature Microbiology 10:158-168 (2025); `10.1038/s41564-024-01871-y; Dryad 10.5061/dryad.866t1g1xm; GitHub QVEU/eva71_dimple c99331a60980f68bb0141506e750e8339f278d08` | viral fitness substitution/insertion/deletion scan; peer_reviewed | direct homolog 2C insertion phenotype is unfavorable at mapped A89 junctions | does not validate or absolutely reject any HRV-A89 tag construct |
| Teterina NL et al. Virology 409:1-11 (2011); `10.1016/j.virol.2010.09.028; PMCID PMC2993843` | nonstructural protein insertion screen; peer_reviewed | 2C is insertion-sensitive; tag identity and site context matter | does not prove every HRV-A89 internal 2C insertion fails |
| Deep indel mutagenesis reveals the impact of amino acid insertions and deletions on protein stability and function. Nature Communications (2025); `10.1038/s41467-025-57510-5` | deep indel mutagenesis across domains; peer_reviewed | loops and secondary-structure termini are modestly enriched for indel tolerance; rSASA alone is weak for insertion tolerance | does not provide viral 2C-specific tolerance |
| EpicTope non-disruptive epitope-tagging framework; `PMCID PMC10979891; PMCID PMC13006528` | feature framework; peer_reviewed/tool_article | combine conservation, secondary structure, solvent exposure and disordered-binding features | does not replace direct viral fitness or structure-specific modeling |
| Wakasa A et al. Journal of Biochemistry 168:375-384 (2020); `10.1093/jb/mvaa054; PMCID PMC7585734` | internal epitope insertion and antibody recognition; peer_reviewed | MAP8 is realistic for loop insertion and structural/binder evaluation | does not establish HRV-A89 2C tolerance |
| Moving toward generalizable NZ-1 labeling for 3D structure determination with optimized epitope-tag insertion; `PMCID PMC8098476` | PA12/PA14 inserted epitope and NZ-1 Fab structural work; peer_reviewed | PA14 can adopt closed loop-like bound geometry and may reduce insertion-induced structural change relative to PA12 | does not prove PA14 works inside HRV-A89 2C |
| Gotzke H et al. Nature Communications 10:4403 (2019); `10.1038/s41467-019-12301-7; PMCID PMC6764986` | nanobody tag structural and assay system; peer_reviewed | ALFA has strong nanobody reagent and defined helical epitope sequence | helical 13-aa tag may be risky in short constrained loops; no A89 2C evidence |
| Yano T et al. PLOS ONE 11:e0156716 (2016); `10.1371/journal.pone.0156716` | AGIA antibody tag; peer_reviewed | AGIA is compact and has high-affinity antibody detection | limited internal-insertion structural evidence for A89 2C |
| Tatsumi K et al. Scientific Reports 7:43480 (2017); `10.1038/srep43480; PMCID PMC5339894` | small monoclonal antibody epitope tag; peer_reviewed | minimal DLVPR epitope and GS-flanked practical form are experimentally defined | does not establish internal A89 2C tolerance |
| Schwinn MK et al. ACS Chemical Biology 13:467-474 (2018); `10.1021/acschembio.7b00549` | NanoLuc complementation peptide; peer_reviewed | HiBiT is an 11-aa quantitative luminescent tag with LgBiT complementation | not an antibody epitope and may not fit IP/IF/complex-capture goals |
| Pfuetzner RA et al. The Structure of the Picornaviral 2C:RNA holoenzyme (2026 preprint); `10.64898/2026.06.07.730651` | RNA-bound 2C structural and mutational evidence; preprint | RNA pore/contact residues should be mapped as mechanistic risk context | not a direct HRV-A89 structure or binary veto |
| Yeager C et al. Nucleic Acids Research (2022); `10.1093/nar/gkac1054; PMCID PMC9723501` | RNA-stimulated ATPase mechanism; peer_reviewed | 2C RNA binding and ATPase coupling are central functional constraints | does not identify A89 insertion-tolerant sites |
