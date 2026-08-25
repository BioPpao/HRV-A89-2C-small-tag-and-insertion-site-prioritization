# Tag Selection Rationale V1

Date: **2026-08-25**

Project: HRV-A89 2C internal small-tag insertion-site prioritization

## 1. Design principle

The relevant question is not “which tag is shortest?”. For HRV-A89 2C, a tag is attractive only if its total design burden is acceptable in a highly insertion-sensitive viral ATPase while still supporting the desired readout.

The project therefore evaluates tag forms across several dimensions:

1. peptide footprint;
2. sequence chemistry and avoidable physicochemical liabilities;
3. direct evidence for internal/loop insertion;
4. structural/conformational requirements for binder recognition;
5. orthogonality in human-cell experiments;
6. WB/IP/IF and/or quantitative readout utility;
7. reagent maturity;
8. compatibility with the specific ATPase/RNA/oligomer/Cys-Zn context of 2C.

The repository tag evidence screen treats **tag × site** as the real design unit. A tag that works at one site cannot automatically be assumed to behave similarly at another site.

---

# 2. Why 6×His was not prioritized

## 2.1 Why His-tag initially looks attractive

6×His is a reasonable question precisely because it has several obvious advantages:

- only six residues;
- one of the most mature recombinant-protein tagging systems;
- widely available anti-His antibodies;
- well-established Ni-NTA / Co-affinity workflows;
- familiar purification and detection protocols.

Therefore the decision not to prioritize 6×His is **not** based on the claim that His-tags are intrinsically poor tags.

The issue is that the intended use here is **internal tagging of HRV-A89 2C for a mechanistically constrained viral-protein problem**, not routine terminal tagging of a recombinant soluble protein.

## 2.2 Short does not mean chemically neutral

A polyhistidine sequence has distinctive chemistry. Histidine side chains have pH-dependent protonation behavior and can participate in metal coordination. This is useful for affinity purification, but it means a poly-His insert is not an inert six-residue spacer.

HRV-A89 2C already contains a functionally important Cys/Zn-related region in the C-terminal half of the protein. The current project does **not** have direct evidence that an internal 6×His insert would capture Zn and disrupt A89 2C. Such a statement would overreach the evidence.

The more defensible project-specific conclusion is:

> introducing an artificial polyhistidine patch creates an avoidable metal-coordination / protonation liability in a protein whose biology already contains a functionally relevant Cys/Zn context.

For minimal-perturbation candidate design, an avoidable chemistry-specific variable is a disadvantage even when the peptide is short.

## 2.3 Purification utility is not the same as mechanistic-tag utility

Ni-NTA makes His-tag exceptionally useful for purification. The current project, however, is interested in more than purification:

- detection of tagged 2C;
- WB;
- IF/localization-type readout if required;
- IP/complex-capture possibilities;
- tag accessibility in an internal insertion;
- comparison with the 9A5 mechanistic branch.

Dedicated epitope systems such as MAP8, HA or G196 more directly match those questions because the binder/tag pair itself defines the detection system.

## 2.4 Internal accessibility is still required

The fact that a terminal His-tag works well does not guarantee that an internal poly-His segment embedded in a constrained loop remains equally available to Ni-NTA or anti-His reagents.

Internal recognition can still depend on:

- solvent exposure;
- local folding;
- neighboring residues;
- tag collapse against the protein surface;
- oligomeric environment.

For MAP8 there is direct published evidence of successful internal/loop insertion, including structurally constrained settings. 6×His does not provide a comparable project-specific internal-loop advantage.

## 2.5 Orthogonality and interpretability

A dedicated peptide epitope plus a dedicated binder provides a cleaner mechanistic interpretation than relying on poly-His/metal-affinity chemistry in a complex cellular context.

This does not mean anti-His detection is unusable in mammalian lysate. It means that, when several other compact dedicated epitope systems are available, 6×His offers no compelling internal-2C advantage that compensates for its additional chemical liability.

## 2.6 Final His-tag decision

Current decision:

> **6×His is technically mature and compact, but it is not a first-line internal tag for HRV-A89 2C because polyhistidine chemistry introduces an avoidable metal-/charge-related variable, it lacks a specific constrained-loop insertion advantage, and its strongest traditional use—affinity purification—is not identical to the principal mechanistic readouts in this project.**

This is a prioritization decision, not a universal prohibition.

### When His-tag could be reconsidered

If a later objective becomes recombinant purification of an isolated 2C construct rather than internal viral tagging/mechanistic detection, a terminal His-tag could be considered under a separate design question.

---

# 3. MAP8

- Sequence: `GDGMVPPG`
- Length: 8 aa
- Binder: PMab-1 monoclonal antibody
- Current role: **primary internal-insertion candidate**

## Why advanced

MAP8 has one of the strongest combinations of compact footprint and direct internal-loop evidence among the tags considered in the project.

Published structure-guided MAP-tag work directly examined insertion into protein loops, including restricted structural contexts. The bound MAP8 peptide adopts a compact U-shaped conformation, which is conceptually attractive for an internal insert because the two flanking protein segments do not need to remain far apart.

The MAP system also offers useful human-cell orthogonality because PMab-1 is directed to a mouse podoplanin-derived epitope rather than the corresponding human antigen context.

## Main caveats

- internal insertion success in other proteins is not proof of HRV-A89 2C tolerance;
- the reagent ecosystem is less ubiquitous than HA;
- accessibility remains site-specific;
- linker-free insertion is a design hypothesis, not a universal rule.

## Project interpretation

MAP8 is currently the best **first-line internal-loop epitope hypothesis**, not a proven winner.

---

# 4. HA

- Sequence: `YPYDVPDYA`
- Length: 9 aa
- Current role: **primary experimental benchmark**

## Why retained

HA offers a mature, familiar reagent ecosystem for WB/IP/IF and related assays. It is therefore an excellent benchmark even if it is not structurally optimized specifically for a constrained viral loop.

Picornavirus insertion literature also reinforces the general point that tag identity can alter viral-protein fitness at the same site, making HA useful as an experimentally interpretable comparator rather than merely a historical default.

## Main caveats

- no direct evidence that HA is intrinsically safe in HRV-A89 2C;
- its linear epitope chemistry is not specifically designed around short internal-loop closure geometry;
- the 2C background remains highly insertion-sensitive.

## Project interpretation

HA is retained because it is experimentally mature and interpretable, not because it is assumed to be the least perturbing tag.

---

# 5. G196 minimal

- Minimal epitope: `DLVPR`
- Nominal length: 5 aa
- Binder: mAb G196
- Current role: **minimal-footprint exploratory primary**

## Why advanced

The five-residue minimal epitope is the smallest serious antibody-epitope footprint in the current primary set. This makes it valuable as a test of the hypothesis that reduced insertion length may matter in an unusually insertion-sensitive protein.

## Critical qualification

The practical published construct often includes GS flanks, e.g. `GSDLVPRGS`, to improve accessibility and reduce neighboring-sequence effects.

Therefore the nominal “5 aa” advantage must not be overstated. At a real 2C site, the functional insert may effectively approach nine residues if flanking residues are needed.

Direct evidence for successful insertion into highly constrained internal loops is also weaker than for MAP8 or PA12.

## Project interpretation

G196 is useful because it tests a **minimal-footprint branch** and provides tag-identity comparison at `289|290`, but it is not automatically superior simply because the nominal core is shorter.

---

# 6. AGIA

- Sequence: `EEAAGIARP`
- Length: 9 aa
- Binder: Ra48 rabbit monoclonal antibody
- Current role: **strong alternative**

## Advantages

AGIA is compact and was designed around a high-affinity binder. Its sequence avoids Ser, Thr, Tyr and Lys, reducing several common PTM liabilities within the tag itself. Published work reports sensitive detection and low background in tested systems.

## Why not in the first primary set

The project has less direct evidence that AGIA is specifically suited to constrained internal-loop insertion than MAP8. Its assay properties are attractive, but for this problem internal-loop behavior receives substantial weight.

## Project interpretation

AGIA remains a credible reserve option if the leading tag forms become experimentally or structurally unsuitable.

---

# 7. ALFA

- Core sequence: `SRLEEELRRRLTE` (13 aa)
- Common framed form: `PSRLEEELRRRLTEP` (15 aa)
- Binder: NbALFA nanobody
- Current role: **excellent assay system, secondary for minimal-perturbation 2C insertion**

## Advantages

ALFA has an exceptionally strong and orthogonal nanobody ecosystem and is highly versatile for imaging, detection and purification.

## Main project-specific concern

The tag is deliberately designed with stable alpha-helical propensity. That is an advantage for ALFA recognition, but may be a liability when inserted into a short native loop where the goal is to minimize imposed secondary-structure preferences.

Its 13–15 aa footprint is also clearly larger than MAP8, HA or minimal G196.

## Project interpretation

ALFA is an important example of why **excellent tag technology does not automatically equal ideal internal 2C tag**.

---

# 8. PA12

- Sequence: `GVAMPGAEDDVV`
- Length: 12 aa
- Binder: NZ-1
- Current role: **structurally compelling but context-limited**

## Advantages

PA12 has unusually strong direct structural precedent for internal insertion. The peptide forms a turn and its termini project outward, which is geometrically attractive for insertion into folded proteins and loop/turn regions.

## Why down-ranked in this project

The peptide is derived from human podoplanin and NZ-1 recognizes human podoplanin. This introduces a human-cell orthogonality/background concern that the MAP system was specifically useful in avoiding.

This does not prove every human-cell assay will show problematic background; it is a project-specific risk factor.

## Project interpretation

PA12 demonstrates that even very favorable insertion geometry can be outweighed by experimental-system compatibility.

---

# 9. HiBiT

- Sequence: `VSGWRLFKKIS`
- Length: 11 aa
- Detection principle: complementation with LgBiT to generate NanoLuc activity
- Current role: **orthogonal quantitative reporter**

## Advantages

HiBiT is highly sensitive and quantitative, making it excellent for abundance and kinetic measurements.

## Why it is not the default mechanistic epitope

HiBiT is a split-luciferase reporter rather than a conventional antibody epitope. It does not automatically replace a mature antibody-based system for every IP, IF or complex-capture question.

## Project interpretation

HiBiT is best viewed as a separate readout branch rather than a drop-in substitute for MAP8/HA/G196 in the current mechanistic design.

---

# 10. FLAG

Current status: **explicitly excluded from ranking**.

The exclusion is project-specific, not a judgment that FLAG is a poor tag.

The 9A5 antibody construct already uses FLAG, so using FLAG again on 2C would undermine orthogonal detection and complicate interpretation.

Therefore FLAG is excluded by a fixed experimental-design constraint.

---

# 11. Myc

Myc is a mature epitope tag but provides no clear project-specific internal-loop advantage over the leading candidates.

Picornavirus precedent also shows that similarly sized tags can have very different effects at the same viral-protein insertion site. There is therefore no scientific basis for assuming Myc would behave as an interchangeable substitute for HA/MAP8.

Current status: **not prioritized in the first experimental batch**.

---

# 12. V5

V5 has a larger footprint than the primary compact candidates and does not provide a compelling internal-insertion advantage that would justify the additional sequence burden for this 2C problem.

Current status: **not prioritized**.

---

# 13. Spot

Spot is useful as a nanobody-compatible tag system, but its current project evidence does not provide a clear advantage over MAP8 for constrained internal insertion. Its sequence origin/orthogonality context also needs to be considered in the experimental background.

Current status: **not prioritized in the first batch**.

---

# 14. C-tag / EPEA and other free-C-terminal recognition systems

These systems are chemically mismatched to the intended design because their recognition depends on the peptide being at a free C terminus.

The project requirement is **internal insertion**.

Current status: **unsuitable for the intended internal-tag strategy**, irrespective of how good they may be for terminal tagging.

---

# 15. UniTope and other emerging internal-tag systems

Emerging tag systems are scientifically interesting and may eventually offer attractive internal-loop solutions.

They were not prioritized because the current project favors a balance of:

- reagent maturity;
- published cross-protein validation;
- interpretability;
- direct internal-loop evidence;
- immediate experimental feasibility.

Current status: **future alternative rather than first-batch choice**.

---

# 16. Current qualitative tag hierarchy

| Tag | Approx. design length | Internal-loop evidence | Main strength | Main liability in this project | Current role |
|---|---:|---|---|---|---|
| MAP8 | 8 aa | very strong | compact + direct internal insertion precedent | 2C-specific tolerance unknown | primary |
| HA | 9 aa | moderate/indirect | mature WB/IP/IF ecosystem | not optimized for constrained-loop geometry | primary benchmark |
| G196 minimal | 5 aa core; often ~9 aa practical | limited | smallest nominal antibody epitope | flanks may erase nominal size advantage | primary exploratory |
| AGIA | 9 aa | limited | compact/high-affinity | less constrained-loop evidence | strong alternative |
| ALFA | 13–15 aa | moderate | excellent orthogonal nanobody system | larger footprint + helical tendency | secondary |
| PA12 | 12 aa | very strong | turn-forming internal insertion geometry | human podoplanin background context | context-limited |
| HiBiT | 11 aa | application-dependent | extremely sensitive quantitative readout | different assay class; not universal IP/IF replacement | orthogonal reporter |
| 6×His | 6 aa | no specific advantage | tiny, mature purification system | poly-His chemistry / metal-coordination liability; readout mismatch | not prioritized |
| FLAG | 8 aa | general precedent | mature ecosystem | conflicts with 9A5-FLAG orthogonality | excluded |
| Myc | ~10 aa | no clear advantage | mature antibodies | no compelling internal-loop edge | not prioritized |
| V5 | 14 aa | limited | mature detection | larger burden without unique benefit | not prioritized |
| Spot | compact | context-dependent | nanobody system | no current advantage over MAP8 | not prioritized |
| C-tag/EPEA | 4 aa terminal motif | terminal-specific | very compact | requires free C terminus | incompatible with internal insertion |
| UniTope/emerging | system-dependent | emerging | future potential | reagent/validation maturity | reserve/future |

---

# 17. Final interpretation

The project deliberately avoids a simplistic “shorter tag wins” rule.

A useful conceptual summary is:

> **footprint × chemistry × recognition geometry × internal-insertion precedent × experimental orthogonality × site context**

For HRV-A89 2C, MAP8 currently offers the strongest first-line balance; HA provides a mature experimental benchmark; G196 provides a minimal-footprint hypothesis. His-tag remains attractive for many conventional protein workflows but is not the preferred internal mechanistic tag for this particular viral 2C problem.

## Primary source in this repository

See `docs/TAG_CANDIDATE_SCREEN_V1.md` for the project evidence screen and references to the original tag-system literature.
