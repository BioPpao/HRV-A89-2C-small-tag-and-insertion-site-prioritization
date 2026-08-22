# PHYLOGENY_AWARE_INDEL_V1

Status: **completed with parsimony uncertainty retained**

Date: 2026-08-22

## Purpose

Reassess the CONSERVATION_002 natural-indel layer using a phylogeny-aware lower-bound estimate of independent indel events rather than descendant/type counts alone.

## Inputs

- Curated HRV-A CONSERVATION_002 alignment: `data/hrvA_2C_alignment_v2.fasta`
- A89 alignment map: `data/hrvA_2C_alignment_a89_mapping_v2.tsv`
- V2 conservation table: `data/hrvA_conservation_per_junction_v2.tsv`

## Method

Tree:

- software: FastTree 2.2.0
- command: `FastTree -wag data/hrvA_2C_alignment_v2_sanitized_for_tree.fasta`
- output: `data/hrvA_2C_fasttree_v1.nwk`

Event inference:

- insertion state: any non-gap amino acid in alignment columns between A89 residues `i` and `i+1`;
- local deletion state: any gap in a +-2-residue A89 local window;
- independent-event proxy: Fitch parsimony change count on the FastTree topology;
- uncertainty retained as internal-node/root-state ambiguity flags.

This is a phylogeny-aware lower-bound event estimate, not a fully probabilistic indel-history model.

## Outputs

- `data/hrvA_independent_indel_events_v1.tsv`
- `results/method_hardening_002/phylogeny_qc.tsv`
- `data/hrvA_2C_alignment_v2_sanitized_for_tree.fasta`
- `data/hrvA_2C_tree_name_map_v1.tsv`
- `data/hrvA_2C_fasttree_v1.nwk`
- `results/method_hardening_002/phylogeny_fasttree_v1.txt`

## QC

| Metric | Value |
|---|---:|
| tree tip count | 77 |
| A89 junction rows | 320 |
| junctions with insertion tip presence | 1 |
| junctions with insertion parsimony changes | 1 |
| junctions with local deletion tip presence | 12 |
| junctions with local deletion parsimony changes | 12 |

## Main result

The phylogeny-aware analysis narrows the previous V2 natural-indel signal. Most V2 lineage/tip-support calls do not become repeated independent insertion events under this simple tree-aware lower-bound model.

`248|249` remains the strongest retained indel-conflict row:

- natural/local independent indel lower bound: 2;
- functional tier: `CORE_CAUTION`;
- EV-A71 handle insertion remains unfavorable;
- role remains historical/indel conflict control, not promoted candidate.

Rows around `263|264-266|267` show one inferred event but sit in high-risk or hard-exclusion Cys/Zn context. They are not promoted.

## Interpretation

Phylogeny-aware indel reconstruction does not rescue a high-confidence targeted site. It mostly strengthens the conclusion that natural-indel evidence is sparse and conflict-bearing rather than broadly recurrent.
