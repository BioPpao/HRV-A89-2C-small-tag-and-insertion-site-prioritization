# HRV-A89 2C small-tag and insertion-site prioritization

## Project objective

Prioritize small peptide tags and internal insertion sites for HRV-A89 2C so that tagged 2C remains as close as possible to the native protein in polyprotein processing, membrane-associated replication-complex behavior, ATPase function, oligomerization, RNA-related function, and 9A5-mechanism experiments.

This project does **not** assume HA is optimal. Tag identity and insertion site are treated as two independent variables and ranked jointly.

## Explicit project constraints

- **FLAG is excluded from the candidate tag set** because the 9A5 antibody construct already uses FLAG and orthogonal detection is required.
- Permanent N- or C-terminal tagging is not assumed to be safe.
- Candidate sites must be evaluated in both monomeric and hexameric structural contexts.
- Published functional regions from poliovirus/enterovirus homologs must be mapped to HRV-A89 rather than copied by residue number.
- Replicon design must consider both protein-level and viral-RNA-level consequences of an inserted coding sequence.
- Computational ranking identifies candidates; WT-like replicon behavior remains the decisive validation criterion.

## Evidence sources

1. HRV-A89 2C AlphaFold input/structures and the current no-membrane hexamer lead from `BioPpao/HRV-Oligomers`.
2. Existing hexamer interface, clash, geometry, SASA, 9A5 and ATP/Mg analyses from `HRV-Oligomers`.
3. Published picornavirus 2C functional/structural literature.
4. Published internal epitope-tagging literature and tag–binder structural data.
5. Sequence conservation and structural mapping across homologous 2C proteins.
6. Viral RNA secondary-structure/cis-element checks for the exact nucleotide construct.

## Current preliminary tag shortlist

The first-pass literature screen currently prioritizes the following for deeper evaluation:

- **MAP8** — 8 aa; specifically developed and structurally validated for insertion into internal loops, including constrained beta-hairpins.
- **HA** — 9 aa; mature WB/IP/IF reagent ecosystem and useful viral precedent, retained as a benchmark rather than assumed winner.
- **G196** — 5 aa; extremely compact and high-affinity antibody system, but internal-loop evidence is currently weaker than MAP8/PA.
- **AGIA** — 9 aa; high-specificity/high-affinity rabbit monoclonal system with no Ser/Thr/Tyr/Lys in the tag, but internal insertion requires additional validation.
- **ALFA** — 13 aa core; very high-affinity nanobody system with strong imaging/IP/WB performance, but its stable helical architecture and greater length require site-specific structural caution.
- **PA12** — 12 aa; strongly supported for internal loop insertion, but the NZ-1 binder recognizes human podoplanin and therefore human-cell background must be considered.
- **HiBiT** — 11 aa; exceptionally sensitive quantitative reporter, considered mainly as an orthogonal quantification option rather than the default WB/IP/IF tag.

Lower-priority or exclusion candidates will be documented separately. FLAG is not considered further.

## Core workflow

`tag screen -> 2C functional exclusion map -> residue/window-level structural screen -> tag x insertion-site joint ranking -> tagged structural models -> RNA-level construct audit -> experimental candidate set`

## Status

Project initialized. Literature screening and reuse audit of `HRV-Oligomers` have started. No insertion site is currently designated as safe or final.
