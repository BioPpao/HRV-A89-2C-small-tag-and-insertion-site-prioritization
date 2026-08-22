# DIRECT_INDEL_001 run log

Task: `DIRECT_INDEL_001`

Branch: `analysis/conservation-002`

Starting commit: `b97f5a048af862fe186d5c9308d4059b2606c9e9`

Status: `IN_PROGRESS`

Date: 2026-08-22

## Scope

Acquire and verify EV-A71 direct insertion/deletion viral-fitness data, map mature EV-A71 2C perturbation evidence to all 320 HRV-A89 2C peptide junctions, and integrate with current V2 structure/function/conservation/literature-rescue evidence.

No Tag x Site modeling, long MD, RNA/codon design, construct recommendation, or HRV-A89 `safe`/validated-site claim is authorized in this task.

## Required read-order checkpoint

Read in order:

1. `WORKFLOW.md`
2. `AGENTS.md`
3. `PROJECT_STATE.md`
4. `DECISIONS.md`
5. `ANALYSIS_INDEX.md`
6. `ACTIVE_TASK.md`
7. `docs/METHOD_GAP_AND_NEXT_EVIDENCE_AUDIT_V1.md`
8. `tasks/DIRECT_INDEL_001.md`
9. `docs/CONSERVATION_SCREEN_V2.md`
10. `docs/CANDIDATE_JUNCTION_QC_V1.md`
11. `INPUT_PROVENANCE.md`
12. `references/LITERATURE_EVIDENCE_REGISTRY.md`
13. `TODO.md`

## Initial Git state

- `git fetch origin`: completed on 2026-08-22.
- Current branch: `analysis/conservation-002`.
- Remote comparison before edits: `0 0` for `HEAD...origin/analysis/conservation-002`.
- Working tree before edits: clean.

## Planned outputs

- `docs/EV71_2C_DIRECT_INDEL_MAPPING_V1.md`
- `data/evA71_2C_direct_indel_to_A89_v1.tsv`
- `data/candidate_junctions_v3_direct_indel.tsv`
- source/provenance/checksum records
- updates to `PROJECT_STATE.md`, `ANALYSIS_INDEX.md`, `TODO.md`

## Progress log

### 2026-08-22 initial source reconnaissance

Identified primary processed-data source to verify and acquire:

- Bakhache et al. Nature Microbiology 2024, DOI `10.1038/s41564-024-01871-y`.
- Dryad dataset DOI `10.5061/dryad.866t1g1xm`.
- Raw reads reported under SRA BioProject `PRJNA1066851`.
- Code repositories reported as `QVEU/eva71_dimple` and `QVEU/InDel_Toolkit`.

Next action: acquire source metadata and processed quantitative files from Dryad/GitHub, then record checksums and exact files used.
