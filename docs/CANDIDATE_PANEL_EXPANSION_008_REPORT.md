# CANDIDATE_PANEL_EXPANSION_008_REPORT

Status: **READY_FOR_BROAD_TARGETED_DYNAMICS**

This CPU checkpoint completed literature/source records, all-320 feature integration, RNA-holoenzyme residue mapping, protease-boundary motif scanning, tag portfolio expansion, binder-accessibility proxies, preliminary ranking, robustness checks, a draft candidate panel and a proposed dynamics panel.

Expanded multi-seed ColabFold replication completed for 18 constructs with 36 model rows. OpenMM geometry QC completed for 35/36 rows; one `248|249 x HA` seed failed with `Particle coordinate is nan` and is retained as a QC failure. Local multimer modeling remains deferred. No long MD or final construct design was started.

## Key Counts

- preliminary site x tag rows: 18
- final draft panel counts: `{'Tier_A_primary': 8, 'Tier_B_secondary_rescue': 8, 'Control': 2}`
- Tier A distinct junctions: 6
- Tier A distinct tag systems: 3
- serious non-289/290 junctions retained: `['155|156', '203|204', '224|225', '248|249', '256|257', '287|288', '288|289']`

## Tier A Draft

| Construct | Junction | Tag | Main unresolved conflict |
|---|---|---|---|
| `A89_2C_289_290_MAP8` | `289|290` | `MAP8` | direct_homolog_conflict__functional_HIGH_RISK__structure_supported__detectability_supported;no_HRV_A89_specific_insertion_phenotype |
| `A89_2C_289_290_G196_minimal` | `289|290` | `G196_minimal` | direct_homolog_conflict__functional_HIGH_RISK__structure_supported;no_HRV_A89_specific_insertion_phenotype |
| `A89_2C_288_289_MAP8` | `288|289` | `MAP8` | direct_homolog_conflict__functional_HIGH_RISK__structure_supported__detectability_supported;no_HRV_A89_specific_insertion_phenotype |
| `A89_2C_288_289_HA` | `288|289` | `HA` | direct_homolog_conflict__functional_HIGH_RISK__structure_supported__detectability_supported;no_HRV_A89_specific_insertion_phenotype |
| `A89_2C_224_225_HA` | `224|225` | `HA` | direct_homolog_conflict__functional_CORE_CAUTION__structure_supported__detectability_supported;no_HRV_A89_specific_insertion_phenotype |
| `A89_2C_248_249_MAP8` | `248|249` | `MAP8` | direct_homolog_conflict__functional_CORE_CAUTION__structure_supported__detectability_supported;no_HRV_A89_specific_insertion_phenotype |
| `A89_2C_287_288_MAP8` | `287|288` | `MAP8` | direct_homolog_conflict__functional_HIGH_RISK__structure_supported;no_HRV_A89_specific_insertion_phenotype |
| `A89_2C_290_291_MAP8` | `290|291` | `MAP8` | direct_homolog_conflict__functional_HIGH_RISK__detectability_supported;no_HRV_A89_specific_insertion_phenotype |

## Deferred Methods

- Extra 008 ColabFold multi-seed replication: completed for the predeclared 18-construct panel; outputs are under `results/candidate_panel_008/expanded_colabfold/`.
- Local dimer/trimer multimer modeling: deferred to avoid blocking independent ranking outputs.
- IUPred2A/ANCHOR2 disorder/disordered-binding scores: tool not present in current environment; explicit NA status retained.
- Exact RNA/codon audit: blocked until the real experimental nucleotide construct is supplied.

## Final State

`READY_FOR_BROAD_TARGETED_DYNAMICS`

No site is safe or validated. Stop for review before targeted dynamics or construct design.
