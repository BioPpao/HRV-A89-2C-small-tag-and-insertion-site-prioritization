# HRV-A89 2C functional exclusion map V1

Project: **HRV-A89 2C small-tag and insertion-site prioritization**

Status: evidence mapping in progress. This document defines regions that should be excluded or strongly down-ranked before any tag × insertion-site modelling. It does **not** define a final permissive site.

## 1. Authoritative HRV-A89 2C sequence

The project reference sequence is the 321-aa HRV-A89 2C sequence copied from the AlphaFold input archived in `BioPpao/HRV-Oligomers` and stored locally as `references/HRV_A89_2C_reference_sequence.fasta`.

Residue blocks:

```text
  1 SDSWLKKFTE 10
 11 ACNAARGLEW 20
 21 IGQKISKFID 30
 31 WIKSMLPQAA 40
 41 LKIDYLTKLK 50
 51 QLNLLEKQIE 60
 61 TIRLAPASVQ 70
 71 EKIFIEINTL 80
 81 HDLSLKFLPL 90
 91 YASEARRIKN 100
101 LYIKCSNVIK 110
111 GGKRNEPVAV 120
121 LIHGSPGTGK 130
131 SLATSVLARM 140
141 LTVETDIYSL 150
151 PPDPKYFDGY 160
161 DQQSVVIMDD 170
171 IMQNPSGEDM 180
181 TLFCQMVSSV 190
191 PFIPPMADLP 200
201 DKGKPFTSKF 210
211 VLASTNHTLL 220
221 TPPTVSSLPA 230
231 MARRFYFDLD 240
241 IQVKKEYLLD 250
251 GKLDIAKSFR 260
261 PCDVNIKIGN 270
271 AKCCPFICGK 280
281 AVEFKDRNSC 290
291 TTLSLSQLYS 300
301 HIKEEDRRRS 310
311 SAAQAMEAIF 320
321 Q
```

## 2. High-confidence HRV-A89 sequence landmarks

### 2.1 Walker A / P-loop — hard exclusion

HRV-A89 residues **124–131**:

`GSPGTGKS`

This is the canonical P-loop/Walker A sequence and matches the highly conserved picornavirus 2C ATPase motif. Any insertion in this motif or its immediate structural neighborhood should be rejected.

### 2.2 Walker B — hard exclusion

HRV-A89 residues **165–170**:

`VVIMDD`

This sequence matches the conserved picornavirus 2C Walker B motif. The region participates directly in ATP hydrolysis and is a hard exclusion zone.

### 2.3 9A5-recognition region — hard exclusion for this project

HRV-A89 residues **148–160**:

`YSLPPDPKYFDGY`

This region must not be used for tagging because the downstream biological question involves 9A5 binding/action. Insertion here, or immediately adjacent to it, could change antibody recognition or local conformation and create a mechanism-study confounder.

### 2.4 Cys-rich / putative Zn-associated region — strong exclusion pending exact structural mapping

HRV-A89 residues approximately **261–290** contain the conspicuous Cys-rich segment:

`PCDVNIKIGNAKCCPFICGKAVEFKDRNSC`

Published enterovirus 2C structures identify a C-terminal Cys-rich zinc-binding region. The exact A89 Zn-coordination residues must still be mapped by sequence/structure alignment rather than assumed from heterologous numbering. Until that is complete, this entire segment should be strongly down-ranked for internal insertion.

## 3. Homolog-derived functional constraints that must be mapped to HRV-A89

The 2020 enterovirus 2C review summarizes the following experimentally supported regions, mainly using poliovirus and EV-A71 numbering:

| Functional feature | Published homolog numbering | Project treatment |
|---|---:|---|
| N-terminal membrane binding | PV 21–54 | hard/strong exclusion after A89 mapping |
| N-terminal RNA binding | PV 21–45 | hard/strong exclusion after A89 mapping |
| Walker A | PV 129–136 | already mapped to A89 124–131 |
| Walker B | PV 172–177 | already mapped to A89 165–170 |
| Motif C | PV 217–223 | exact A89 mapping pending |
| Arg finger | EV-A71/PV structural literature around R240/R241 | exact A89 mapping pending |
| Zn-binding region | PV ~269–286 | A89 Cys-rich region flagged; exact ligands pending |
| C-terminal RNA-binding region | PV 312–319 | exact A89 mapping pending |
| C-terminal pocket-binding / oligomerization residues | PV/EV-A71 L327/F328-related PBD | exact A89 structural mapping pending |

These residue numbers must **not** be copied directly to HRV-A89. HRV-A89 is 321 aa and contains indels relative to representative PV/EV-A71 sequences.

## 4. Direct evidence that homolog numbering cannot simply be transferred

A conserved rhinovirus peptide corresponding to the 9A5-recognition region provides a concrete example. In a published/patent HRV-C15 sequence, the homologous `YSLPPDPKYFDGY` peptide occurs at approximately **151–163**, whereas in the current HRV-A89 sequence it is **148–160**.

Likewise, an HRV-C15 conserved `FCQMVSTT` segment is around 186–193, while the related A89 `FCQMVSSV` segment starts at residue 183.

Therefore even locally conserved HRV sequences can be shifted by several residues. Functional constraints must be transferred by explicit alignment and, where possible, structural superposition.

## 5. Regions that are provisionally excluded before structural scanning

At this stage the following should not enter the first permissive-site candidate pool:

- N-terminal membrane/RNA-associated region until exact A89 boundary mapping is complete;
- Walker A and immediate neighboring ATPase geometry;
- the 9A5 148–160 region and a conservative neighboring buffer;
- Walker B and immediate neighboring catalytic geometry;
- motif C once exact A89 mapping is established;
- Arg-finger / intersubunit catalytic network once mapped;
- the Cys-rich/Zn-associated region;
- C-terminal RNA-binding and pocket-binding/oligomerization elements;
- any residue participating substantially in the current 2C–2C hexamer interface;
- any pore-facing/RNA-path residue identified by structure or literature;
- buried-core residues and stable secondary-structure elements where an insertion would require chain breakage in a helix or beta strand.

## 6. What is still unresolved

The following must be completed before naming exact insertion junctions:

1. Verify that chains A–F of the current lead and companion HRV-A89 hexamer structures contain the expected 1–321 sequence and consistent residue numbering.
2. Map A89 motif C, Arg finger, Zn ligands, C-terminal PBD/alpha6-related element, and N-/C-terminal RNA/membrane-associated regions by alignment plus structural superposition.
3. Compute per-residue monomer and hexamer metrics: secondary structure, relative SASA, local confidence/uncertainty, neighbor-chain distance, buried surface contribution, intersubunit contacts, pore orientation/distance and local crowding.
4. Build HRV-A/B/C multiple-sequence conservation scores and use them as an independent penalty, not as a substitute for functional evidence.
5. Overlay the 9A5-bound model as a late exclusion layer so the selected tag does not obstruct the antibody mechanism experiment.
6. Audit the exact inserted nucleotide sequence in the replicon for local RNA-structure/cis-element and polyprotein-processing effects.

## 7. Decision rule

A candidate insertion site will only advance if it satisfies all of the following in combination:

`not a known functional motif + low conservation + surface-exposed loop + low 2C–2C interface involvement + low pore/RNA-path risk + structurally compatible with the selected small tag + no obvious RNA/processing liability`

Even a top-ranked computational site remains a **candidate permissive site**, not a proven safe site. WT-like replicon behavior is the final biological gate.
