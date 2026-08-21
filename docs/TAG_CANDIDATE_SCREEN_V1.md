# Small-tag candidate screen V1

Project: **HRV-A89 2C small-tag and insertion-site prioritization**

Status: preliminary evidence screen; **not a final construct recommendation**.

## 1. Design question

The relevant question is not simply which epitope tag is shortest. For HRV-A89 2C, the preferred tag must minimize perturbation of a highly insertion-sensitive AAA+ ATPase while remaining accessible to a binder in an internal loop and supporting the downstream assays required for the project.

The ranking therefore considers:

1. peptide footprint and sequence chemistry;
2. direct evidence for **internal/loop insertion**;
3. structural conformation required for binder recognition;
4. orthogonality in human cells;
5. WB / IP / IF utility;
6. binder affinity and reagent availability;
7. compatibility with the 2C oligomerization / RNA / ATPase mechanism question.

**FLAG is excluded from all candidate ranking** because the 9A5 antibody construct already uses FLAG and the tagging system must remain orthogonal.

---

## 2. Critical prior evidence: picornavirus 2C is unusually insertion-sensitive

Teterina et al. used transposon-mediated insertion mutagenesis across poliovirus nonstructural proteins. At least one insertion-tolerant site was recovered in every nonstructural protein **except 2C**; no tested 2C site supported the minimum five-residue insertion used in that screen.

This does not prove that HRV-A89 2C cannot tolerate any internal peptide insertion, but it establishes a high prior risk. It also means that a computationally attractive loop must never be called a "safe site" before replicon-level validation.

The same poliovirus study also showed that tag identity matters independently of insertion site: HA, FLAG, c-Myc and tetracysteine inserts of similar size could have different effects at the same viral-protein location. Therefore **tag × site** must be evaluated jointly.

Reference:
- Teterina NL, et al. *Identification of tolerated insertion sites in poliovirus non-structural proteins.* Virology. 2011;409:1–11. DOI: 10.1016/j.virol.2010.09.028.

---

## 3. Candidate tags

### Tier 1 — MAP8

- Sequence: `GDGMVPPG`
- Length: 8 aa
- Binder: PMab-1 monoclonal antibody
- Parent antigen: mouse podoplanin MAP epitope
- Reported affinity of the MAP system: approximately low-nM (`KD ~3.7 nM` for PMab-1/MAP in the original system)
- Applications: WB, IP/purification, IHC/IF-related detection, flow cytometry depending reagent format

**Why it is currently ranked first**

The 2020 structure-guided MAP-tag study shortened the original MAP tag to eight residues and directly tested **internal insertion into protein loops**. MAP8 remained antibody-reactive when inserted into an extended Fn10 loop and, importantly, into a structurally restricted GPCR beta-hairpin. Plain MAP8 without an added linker could still work in the tested loops.

The peptide adopts a compact U-shaped bound conformation, which is intrinsically more compatible with bringing the two flanking protein segments back together than a long extended epitope would be.

PMab-1 is species-specific for mouse podoplanin and does not cross-react with human podoplanin, which is useful for a human-cell experimental background.

**Risks / caveats**

- Successful insertion in other proteins does not establish tolerance in picornavirus 2C.
- Linker-free insertion should be the default structural hypothesis, not a universal rule; local geometry may still require comparison with ±1 Gly or another minimal spacer.
- PMab-1 reagent ecosystem is smaller than the HA ecosystem, although commercial/research-grade reagents are available.

References:
- Wakasa A, et al. *Site-specific epitope insertion into recombinant proteins using the MAP tag system.* J Biochem. 2020;168:375–384. DOI: 10.1093/jb/mvaa054.
- Fujii Y, et al. *MAP Tag: A Novel Tagging System for Protein Purification and Detection.* Monoclon Antib Immunodiagn Immunother. 2016;35:293–299. DOI: 10.1089/mab.2016.0039.

**Current decision: PRIMARY candidate.**

---

### Tier 1 — HA

- Sequence: `YPYDVPDYA`
- Length: 9 aa
- Binder ecosystem: multiple mature monoclonal/polyclonal antibodies
- Applications: WB, IP, IF and related standard assays

**Why retained**

HA remains an excellent experimental benchmark because the reagent ecosystem is mature, sensitivity is well understood, and picornavirus literature shows that HA can sometimes be better tolerated than similarly sized tags at the same viral-protein insertion site.

**Risks / caveats**

- There is no evidence that HA is intrinsically safe inside HRV-A89 2C.
- HA contains two Tyr residues and a strongly recognizable linear epitope; its local conformational demand is not specifically optimized for internal loop insertion.
- The poliovirus insertion screen makes clear that 2C itself is highly insertion-sensitive.

**Current decision: PRIMARY benchmark candidate; not assumed winner.**

---

### Tier 1 / exploratory — G196 minimal tag

- Minimal epitope: `DLVPR`
- Minimal length: 5 aa
- Binder: mAb G196
- Reported `KD`: ~1.25 nM
- Demonstrated in human and yeast cells for WB / IF / IP-related applications

**Major advantage**

At five residues, the minimal epitope has the smallest peptide footprint among the current serious antibody-tag candidates.

**Important qualification**

The original study commonly used the practical nine-residue construct `GSDLVPRGS`, adding GS flanks to improve accessibility and reduce effects from neighboring sequence. Thus, the nominal 5-aa advantage may disappear if flanking residues are required at a given 2C site.

Direct evidence for insertion into constrained internal loops is currently weaker than for MAP8 or PA.

**Current decision: PRIMARY exploratory candidate, especially for the lowest-footprint branch.**

Reference:
- Tatsumi K, et al. *G196 epitope tag system: a novel monoclonal antibody, G196, recognizes the small, soluble peptide DLVPR with high affinity.* Sci Rep. 2017;7:43480. DOI: 10.1038/srep43480.

---

### Tier 2 — AGIA

- Sequence: `EEAAGIARP`
- Length: 9 aa
- Binder: rabbit monoclonal Ra48
- Reported `KD`: ~4.9 nM
- Applications: sensitive WB, immunostaining and IP

**Advantages**

AGIA was designed from the minimal Ra48 epitope and intentionally contains none of Ser, Thr, Tyr or Lys, reducing common PTM liabilities within the tag itself. Published experiments report low-background detection in animal and plant cells.

**Risks / caveats**

- The tag was not specifically developed around constrained internal-loop insertion geometry.
- The parent antigen is human dopamine receptor D1, so orthogonality depends on the experimental context even though widespread background was not seen in the original tested cell systems.

Reference:
- Yano T, et al. *AGIA Tag System Based on a High Affinity Rabbit Monoclonal Antibody against Human Dopamine Receptor D1 for Protein Analysis.* PLoS One. 2016;11:e0156716. DOI: 10.1371/journal.pone.0156716.

**Current decision: STRONG ALTERNATIVE.**

---

### Tier 2 — ALFA

- Minimal core: `SRLEEELRRRLTE` (13 aa)
- Common proline-framed form: `PSRLEEELRRRLTEP` (15 aa)
- Binder: NbALFA nanobody
- Affinity: low-picomolar range for the original high-affinity nanobody
- Applications: very sensitive WB, IP/purification, fixed-cell and live-cell imaging

**Advantages**

The tag/binder system is exceptionally sensitive and orthogonal, and has a compact nanobody binder. The tag can function at different protein positions and between folded domains.

**Structural concern for this project**

The ALFA sequence is deliberately designed to form a stable alpha helix. That feature is advantageous for the ALFA system but may be a liability when inserted into a short native 2C flexible loop, because the insert can impose its own secondary-structure preference. Its 13–15 aa footprint is also larger than MAP8, HA or minimal G196.

Reference:
- Götzke H, et al. *The ALFA-tag is a highly versatile tool for nanobody-based bioscience applications.* Nat Commun. 2019;10:4403. DOI: 10.1038/s41467-019-12301-7.

**Current decision: STRONG ASSAY SYSTEM but SECONDARY for minimal-perturbation 2C internal tagging.**

---

### Tier 2 / context-limited — PA12

- Sequence: `GVAMPGAEDDVV`
- Length: 12 aa
- Binder: NZ-1
- Affinity: sub-nM
- Strong direct evidence for insertion into turn/loop regions

**Advantages**

The NZ-1/PA complex structurally recognizes a turn-forming peptide whose N and C termini project outward, giving unusually strong evidence for internal insertion. PA-tag loop insertion has been used in structured proteins and membrane proteins.

**Major issue in this project**

The PA peptide is derived from human podoplanin and NZ-1 is an anti-human podoplanin antibody. The MAP-tag paper explicitly notes that this can cause background in human cells that express endogenous podoplanin. This does not mean every H1-HeLa experiment will necessarily show interference, but it creates a background risk that MAP8 avoids.

References:
- Fujii Y, et al. *PA tag: A versatile protein tagging system using a super high affinity antibody against a dodecapeptide derived from human podoplanin.* Protein Expr Purif. 2014;95:240–247. DOI: 10.1016/j.pep.2014.01.009.
- Tamura R, et al. *Tailored placement of a turn-forming PA tag into the structured domain of a protein to probe its conformational state.* J Cell Sci. 2016;129:1512–1522. DOI: 10.1242/jcs.176685.

**Current decision: STRUCTURALLY EXCELLENT, but DOWN-RANKED for human-cell orthogonality.**

---

### Orthogonal reporter — HiBiT

- Sequence: `VSGWRLFKKIS`
- Length: 11 aa
- Detection principle: complementation with LgBiT to generate NanoLuc luminescence

**Advantages**

Extremely sensitive and quantitative, useful for low-abundance proteins and kinetic measurements.

**Why it is not the default tag for the mechanism branch**

HiBiT is a split-luciferase reporter rather than a conventional antibody epitope. It is excellent for quantitative abundance measurements but does not replace a mature antibody tag for all WB / IP / IF / complex-capture questions.

**Current decision: ORTHOGONAL quantitative reporter, not the first mechanistic tag.**

---

## 4. Candidates not prioritized in the first experimental batch

- **FLAG** — explicitly excluded because the 9A5 construct already uses FLAG.
- **6xHis** — small but poly-His chemistry and metal-binding behavior are unattractive around a 2C protein with a functionally important Cys/Zn region; mammalian lysate detection is also less orthogonal than dedicated epitope tags.
- **Myc** — no clear internal-loop advantage; picornavirus precedent shows strong tag-identity-dependent fitness effects.
- **V5** — 14 aa and no compelling internal-insertion advantage over smaller candidates.
- **Spot** — useful nanobody tag but derived from a human protein sequence and currently lacks an advantage over MAP8 for this specific problem.
- **C-tag/EPEA and other free-C-terminal tags** — chemically dependent on a free C terminus and therefore unsuitable for the intended internal insertion strategy.
- **new/emerging systems such as UniTope** — scientifically interesting internal-loop concept, but reagent maturity and cross-protein validation are currently weaker than the leading candidates for this project.

---

## 5. Preliminary ranking for HRV-A89 2C

| Rank | Tag | Length used for design | Direct internal-loop evidence | Human-cell orthogonality | Mechanistic assay utility | Main concern |
|---:|---|---:|---|---|---|---|
| 1 | MAP8 | 8 aa | **very strong** | **strong** | strong | smaller reagent ecosystem than HA |
| 2 | HA | 9 aa | moderate / indirect | strong | **very strong** | not optimized for constrained internal loops |
| 3 | G196 | 5 aa minimal; often 9 aa with GS flanks | limited | strong | strong | accessibility may require flanks; loop evidence weaker |
| 4 | AGIA | 9 aa | limited | moderate–strong | strong | no dedicated constrained-loop validation |
| 5 | ALFA | 13 aa core / 15 aa framed | moderate | **very strong** | **very strong** | stable alpha-helical insert + larger footprint |
| 6 | PA12 | 12 aa | **very strong** | weak–context dependent in human cells | **very strong** | NZ-1 recognizes human podoplanin |
| — | HiBiT | 11 aa | application-dependent | strong | quantitative reporter | requires LgBiT; not a universal IP/IF epitope |

This ranking is intentionally **not a final construct ranking**. Once candidate 2C insertion windows are identified, each tag must be re-ranked at each site because local loop geometry can change the order.

---

## 6. Current recommendation

For the first structural-design round, explicitly model at least:

1. **MAP8** — main internal-insertion candidate;
2. **HA** — mature experimental benchmark;
3. **G196 minimal / minimally flanked form** — smallest-footprint exploratory branch.

AGIA should remain available as a fourth option if the first three show unfavorable local sequence/structure interactions.

Do not multiply constructs prematurely. First reduce HRV-A89 2C to a small set of plausible insertion windows using literature exclusion zones, conservation, monomer SASA/secondary structure, hexamer interfaces, pore orientation, 9A5 geometry and RNA-related constraints. Only then perform tag × site structural modelling.
