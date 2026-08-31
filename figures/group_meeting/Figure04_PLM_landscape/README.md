# Figure 4 — Tag-specific PLM landscape

## Scientific conclusion

Tag-specific PLM scoring reveals site × tag heterogeneity, supporting the decision to model tag identity and insertion position as separate variables. PLM remains secondary computational evidence and cannot override direct phenotype or hard biological constraints.

## Figure contract

- Archetype: asymmetric mixed-modality composite with Panel b as the hero evidence panel.
- Backend: R (`ggplot2`, `patchwork`, `svglite`, `ragg`).
- Final dimensions: 183 × 170 mm.
- Typography: Arial across panels; SVG uses natural font spacing without forced text-width attributes.
- Primary metric: `plm_delta_mean_pll_insert_minus_wt`.
- Color midpoint: exactly 0.
- Visual color limits: 2nd percentile = `-0.04909577`; 98th percentile = `0.007229815`.
- The color scale is visually capped with `scales::squish`; source values are unchanged.
- No PLM tolerance/favorable threshold is defined.

## Palette

The palette adapts the supplied scientific schematic: muted orange for negative/risk emphasis, teal-blue for protein/structural evidence, purple for model/matrix emphasis, near-white at the zero midpoint, and pale grey/lilac support tracks. Saturation was reduced for dense publication-scale data.

## QC summary

- 1,280/1,280 completed rows plotted.
- 320 unique ordered junctions (`1|2` through `320|321`).
- Four tags × 320 rows each; sequences and lengths verified against the input table.
- No duplicated site × tag rows.
- All annotation joins resolved.
- SVG word spacing is renderer-safe: editable Arial text with no forced width scaling.

Per-tag distributions:

- `G196_minimal`: median Δmean PLL = `-0.00567`
- `G196_practical_GS`: median Δmean PLL = `-0.01271`
- `HA`: median Δmean PLL = `-0.01274`
- `MAP8`: median Δmean PLL = `-0.01254`

`G196_minimal` has a less-negative median distribution, but this is not interpreted as universal superiority. Site ranking is also considered within each tag.

## Calibration examples

- `155|156 × G196_minimal`: high PLM rank does not rescue a hard functional negative.
- `248|249`: the same site shows substantially different compatibility across tag architectures.
- `256|257`: PLM-favorable for several tags, but biology remains conflicted.
- `289|290`: moderate and tag-dependent PLM support; it is not a universal top PLM site.

## Formal caption

**Figure 4 | Tag-specific PLM scoring reveals site × tag heterogeneity across HRV-A89 2C internal insertion junctions.** A total of 1,280 completed evaluations (320 peptide junctions × four tag architectures) were generated with ESM2 `esm2_t6_8M_UR50D` using full-sequence masked pseudo-log-likelihood. The global landscape uses the inserted-minus-wild-type mean PLL difference to reduce tag-length bias; the diverging color scale is centered exactly at zero and is visually capped at the 2nd and 98th percentiles, with source values unchanged. Within-tag percentiles are shown only in the focal matrix as relative ranks among the 320 positions for the same tag and are not used to compare absolute score distributions between tags. The heatmap and across-tag spread demonstrate substantial dependence on both junction and tag identity. Notably, the high within-tag PLM rank of 155|156 × G196 minimal does not rescue its hard functional exclusion, whereas 248|249 displays marked tag-dependent compatibility. PLM is therefore treated as a secondary computational evidence layer and does not constitute experimental tolerance, biological validation, or a basis for overriding direct homolog insertion phenotype or hard functional constraints.

## Reproduction

Run from the repository root:

```bash
Rscript scripts/plot_figure04_tag_specific_PLM_landscape.R
```

Generated files:

- `Figure04_tag_specific_PLM_landscape.svg`
- `Figure04_tag_specific_PLM_landscape.pdf`
- `Figure04_tag_specific_PLM_landscape_600dpi.png`
- `Figure04_tag_specific_PLM_landscape_source_data.tsv`
- `Figure04_tag_specific_PLM_landscape_qc.tsv`

## Boundary

This figure does not generate a composite score, define a safe insertion site, or provide experimental validation.
