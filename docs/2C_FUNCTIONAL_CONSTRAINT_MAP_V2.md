# HRV-A89 2C functional constraint map V2

Project: **HRV-A89 2C small-tag and insertion-site prioritization**

This version replaces the overly broad V1 exclusion logic. PV mappings are based on explicit full-length 2C sequence alignment. FMDV mappings are working sequence-alignment annotations and will be cross-checked structurally before final ranking.

| feature | homolog evidence | HRV-A89 mapping | treatment |
|---|---|---|---|
| N-terminal membrane/RNA region | PV 21–54; modern PV membrane-binding work | A89 ~21–53 by PV alignment; direct N-terminal amphipathic region receives strongest penalty | graded strong exclusion, not all aa1–110 |
| Walker A / P-loop | PV 129–136 | A89 124–131 `GSPGTGKS` | hard exclusion |
| 9A5-binding region | project-defined | A89 148–160 `YSLPPDPKYFDGY` | hard exclusion |
| Walker B | PV 172–177 | A89 165–170 `VVIMDD` | hard exclusion |
| Motif C | PV 217–223 | A89 210–216 `FVLASTN`; N216 corresponds to PV N223 | hard/strong exclusion |
| Arg finger | PV R240/R241 | A89 R233/R234 | hard/strong exclusion |
| historical tolerated insertion 1 | PV 4-aa insertion after residue 255 | A89 junction ~248|249 | literature-rescue candidate; not automatically preferred |
| PV K259 functional region | PV K259 | A89 K252 | strong neighborhood penalty |
| historical tolerated insertion 2 | PV 6-aa insertion after residue 263 | A89 junction ~256|257 | literature-rescue candidate; not automatically preferred |
| Zn/ZFER region | PV ~269–286 | A89 ~262–278 | strong exclusion pending exact ligand mapping |
| C-terminal RNA-binding region | PV 312–319 | A89 304–311 `EEDRRRSS` | strong exclusion |
| terminal PBD/PBL-related residues | PV L327/F328-related | A89 I319/F320 / terminal region | hard/strong exclusion |
| FMDV conserved pore-loop aromatic | FMDV H147 | A89 Y156 by sequence alignment | hard exclusion; already inside 9A5 region |
| FMDV RNA selectivity residue | FMDV A188 | A89 A197 | strong exclusion |
| FMDV RNA-contact residue | FMDV L190 | A89 L199 | strong exclusion |
| FMDV RNA-contact residue | FMDV K193 | A89 K202 | strong exclusion |
| FMDV lineage-variable RNA residue | FMDV K169 | A89 E178 | contextual penalty only |
| FMDV lineage-variable pore residue | FMDV R215 | A89 P223 | contextual penalty only |

## High-value conflict that must be preserved

Poliovirus provides two historical positive insertion-tolerance observations: a 4-aa insertion after PV 2C residue 255 and a 6-aa insertion after residue 263. Alignment maps those boundaries approximately to HRV-A89 **248|249** and **256|257**, respectively.

These are **not automatically good HRV-A89 tag sites**. In the current A89 structural ensemble, both mapped junctions lie in ordered/interface-sensitive neighborhoods. The literature and model evidence therefore conflict. These sites will remain in a separate **literature-rescue track** rather than being discarded or promoted prematurely.

## RNA-pore update from the 2026 FMDV 2C:RNA structure

The 2026 preprint reports FMDV H147, A188, L190 and K193 as conserved/important pore or RNA-contact positions. Sequence alignment maps these to A89 **Y156, A197, L199 and K202**. A89 Y156 lies inside the 9A5-binding region 148–160. This is relevant both for avoiding tag insertion there and for later mechanistic interpretation, but it is not proof that 9A5 blocks RNA translocation.

FMDV K169 and R215 are less conserved and map chemically non-conservatively to A89 E178 and P223, consistent with the preprint's lineage-specific interpretation. They are not treated as universal hard exclusions.

## Evidence boundaries

- PV/EV-A71 residues can be mapped with relatively high confidence because the ATPase/C-terminal region is strongly homologous.
- FMDV is more divergent; mapped RNA-contact positions are working annotations until structural superposition is completed.
- The current A89 hexamers are no-RNA, no-membrane structural hypotheses and cannot replace the experimental FMDV 2C:RNA geometry.
- A computationally top-ranked insertion remains a candidate only; WT-like replicon behavior is the biological acceptance gate.

## Primary references

- Li JP, Baltimore D. *J Virol.* 1988. DOI: `10.1128/JVI.62.11.4016-4021.1988`.
- Teterina NL et al. *Virology.* 2011. DOI: `10.1016/j.virol.2010.09.028`.
- Guan H et al. *Sci Adv.* 2017. DOI: `10.1126/sciadv.1602573`.
- Chen P et al. *Nucleic Acids Res.* 2022. DOI: `10.1093/nar/gkac671`.
- Yeager C et al. *Nucleic Acids Res.* 2022. DOI: `10.1093/nar/gkac1054`.
- Sadeghipour S et al. *PLoS Pathog.* 2024. DOI: `10.1371/journal.ppat.1012388`.
- Pfuetzner RA et al. bioRxiv 2026. DOI: `10.64898/2026.06.07.730651` (preprint; not peer reviewed).