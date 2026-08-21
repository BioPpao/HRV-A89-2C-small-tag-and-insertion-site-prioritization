# HRV-A89 2C functional exclusion map V3

Status: literature- and sequence-audited working map for small-tag insertion-site prioritization.

## Major V3 corrections

V3 replaces several approximate homolog-only boundaries in V2 with direct HRV-A89 UniProt P07210 annotations where available. These UniProt annotations are mostly **By similarity** and therefore are not equivalent to direct HRV-A89 mutagenesis, but they are more appropriate than copying poliovirus/EV-A71 numbering.

The HRV-A89 2C chain is residues 1104–1424 of the P07210 polyprotein, corresponding to 2C aa1–321. UniProt annotates the 2B/2C cleavage at 1103|1104 and the 2C/3A cleavage at 1424|1425.

Important distinction: the project-defined structural analysis window `aa112–258` is retained for comparison with the previous hexamer project, but UniProt/PROSITE annotates the broader SF3 helicase domain as approximately **A89 aa94–254**. These are different concepts and should not be conflated.

## Evidence classes

- **EXCLUDE / hard exclusion**: do not place an internal tag across this feature in the first experimental batch.
- **HIGH RISK / strong penalty**: only retain if independent structural and conservation evidence is unusually favorable.
- **CORE CAUTION**: inside the SF3 ATPase domain but not currently assigned to a specific hard functional element.
- **CONTEXT PENALTY**: model-dependent interface/pore property; requires agreement across lead/control structures.

## Direct A89 annotations from UniProt P07210

Polyprotein coordinates were converted to 2C coordinates using 2C start = polyprotein residue 1104.

| P07210 polyprotein feature | A89 2C coordinate | Annotation | Tagging interpretation |
|---|---:|---|---|
| 1104–1173 | aa1–70 | membrane-binding, By similarity | HIGH RISK |
| 1104–1237 | aa1–134 | oligomerization, By similarity | HIGH RISK |
| 1125–1129 | aa22–26 | RNA-binding, By similarity | HIGH RISK / local exclusion |
| 1128 | aa25 | host RTN3 interaction, By similarity | HIGH RISK / local exclusion |
| 1197–1357 | aa94–254 | SF3 helicase domain, PROSITE-ProRule | CORE CAUTION unless a harder feature applies |
| 1227–1234 | aa124–131 | ATP-binding/P-loop | EXCLUDE |
| 1365 | aa262 | structural Zn-binding, By similarity | EXCLUDE |
| 1376 | aa273 | structural Zn-binding, By similarity | EXCLUDE |
| 1381 | aa278 | structural Zn-binding, By similarity | EXCLUDE |
| 1365–1381 | aa262–278 | degenerate C4-type zinc-finger, By similarity | HIGH RISK |
| 1408–1415 | aa305–312 | RNA-binding, By similarity | HIGH RISK |
| 1419–1424 | aa316–321 | oligomerization, By similarity | EXCLUDE for first batch |
| 1424–1425 | aa321|3A1 boundary | 2C/3A protease cleavage | terminal processing boundary; do not alter without explicit processing design |

Source: UniProtKB P07210, HRV-A89/HRV-89 strain 41467-Gallo.

## Sequence-defined A89 catalytic/antibody features

| A89 position | Sequence / feature | Rule |
|---|---|---|
| aa124–131 | `GSPGTGKS`, Walker A / P-loop | EXCLUDE |
| aa148–160 | `YSLPPDPKYFDGY`, 9A5 epitope | EXCLUDE |
| aa165–170 | `VVIMDD`, Walker B | EXCLUDE |
| aa210–216 | `FVLASTN`, motif-C neighborhood; N216 conserved | EXCLUDE |
| R233/R234 | conserved arginine-finger pair | EXCLUDE |
| C262/C273/C278 | A89 UniProt structural Zn-binding positions | EXCLUDE |
| aa316–321 | terminal oligomerization region; sequence `MEAIFQ` within terminal helix/PBD context | EXCLUDE for first batch |

## New 2026 RNA-holoenzyme mapping

The 2026 FMDV 2C:RNA cryo-EM preprint provides the strongest residue-level substrate-path evidence currently available. The structure used Δ33 FMDV 2C N207A, ATP/Mg and ssRNA; therefore it is not a direct HRV-A89 structure and is treated as homologous functional evidence.

The preprint identifies:
- FMDV H147 as a pore-loop-like aromatic residue important for replication;
- FMDV A188, L190 and K193 as a conserved core RNA-binding triad;
- FMDV K169 and R215 as more lineage-restricted RNA contacts;
- CVB3 orthologs H163, A204, L206 and K209 were tested in a more HRV-proximal enterovirus background.

Using the verified 329-aa CVB3 Nancy 2C sequence (UniProt P03313) aligned to the 321-aa A89 sequence:

| CVB3 residue | A89 homolog | Functional result / interpretation |
|---|---|---|
| D162 | K155 | D162A was WT-like in CVB3 replication; not conserved as the same chemistry |
| H163 | Y156 | H163A abolished replication; the preprint reports conservation of an aromatic residue at this structural position. A89 Y156 lies inside the 9A5 epitope |
| K185 | E178 | CVB3 K185A showed no appreciable defect; supports lineage-specific rather than universal importance |
| A204 | A197 | conserved RNA-binding triad; mutation inhibited CVB3 replication |
| L206 | L199 | conserved RNA-binding triad; mutation inhibited CVB3 replication |
| K209 | K202 | conserved RNA-binding triad; mutation inhibited CVB3 replication |
| N223 | N216 | motif-C homolog; exact sequence/position alignment |
| R240/R241 | R233/R234 | conserved R-finger homologs from EV/PV structural literature |

### Consequence for tagging

This mapping upgrades A89 residues **A197, L199 and K202** from generic ATPase-core residues to **direct homologs of an experimentally supported RNA-binding triad**. Junctions immediately adjacent to these residues must be strongly down-ranked or excluded.

It also provides a mechanistic warning for the 9A5 region: **A89 Y156 occupies the CVB3 H163/FMDV H147-equivalent aromatic pore-loop position**. This does not prove the A89 9A5 epitope adopts the identical RNA-bound geometry, but it makes insertion into or immediately adjacent to aa148–160 especially inappropriate.

## C-terminal interpretation

The A89 sequence/structure supports three nested C-terminal risk layers:

1. aa262–278: UniProt-annotated zinc-finger; C262/C273/C278 are structural Zn-binding positions by similarity.
2. aa279–304: Cys-rich-to-C-terminal-bundle transition; not a direct UniProt RNA/oligomerization feature but structurally constrained and includes additional C290.
3. aa305–312: C-terminal RNA-binding region by similarity.
4. aa316–321: extreme C-terminal oligomerization region by similarity; EV/PV crystal work independently shows terminal PBD residues are important for self-oligomerization.

Therefore an apparently exposed loop near aa287–291 is not automatically a low-risk insertion site.

## Current conservative junction tiers

For first-batch computational prioritization:

- `EXCLUDE`: junction touches Walker A, 9A5 epitope, Walker B, motif C, R finger, A197/L199/K202 RNA-binding homologs, structural Zn ligands, or aa316–321 oligomerization region.
- `HIGH_RISK`: junction lies in A89 aa1–134 N-terminal membrane/oligomerization context; near a hard feature; in aa255–290 ATPase-to-Zn/Cys-rich transition; or in aa291–315 C-terminal bundle/RNA-binding transition.
- `CORE_CAUTION`: remaining junctions within the UniProt/PROSITE SF3 domain aa94–254 that are not already EXCLUDE/HIGH_RISK.
- No junction is currently called `SAFE`.

## Evidence boundary

The A89 UniProt functional-region annotations are mostly transferred **By similarity**. The 2026 RNA-holoenzyme study is a preprint and uses FMDV plus a trapping mutation. The CVB3 replication data improve confidence for homologous residue importance but still do not replace direct HRV-A89 replicon testing.

The correct endpoint remains: rank low-risk constructs for experiment, not computationally certify a safe insertion site.

## Key references

- UniProtKB P07210, HRV-A89/HRV-89 strain 41467-Gallo.
- UniProtKB P03313, Coxsackievirus B3 strain Nancy.
- Guan H et al. Sci Adv. 2017;3:e1602573. DOI: 10.1126/sciadv.1602573.
- Yeager C et al. Nucleic Acids Res. 2022. DOI: 10.1093/nar/gkac1054.
- Pfuetzner RA et al. bioRxiv 2026. DOI: 10.64898/2026.06.07.730651. Preprint.
- Teterina NL et al. Virology. 2011;409:1-11. DOI: 10.1016/j.virol.2010.09.028.
