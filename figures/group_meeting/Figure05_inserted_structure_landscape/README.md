# Figure 05 — Explicit insertion modeling reveals strong site × tag differences in local structural perturbation

Subtitle: **Global RMSD alone is insufficient to identify minimally disruptive constructs.**

## Figure contract

- Core conclusion: explicit insertion modeling reveals strong site × tag dependence in structural perturbation, and global RMSD alone is insufficient to identify minimally disruptive constructs.
- Archetype: asymmetric mixed-modality figure with Panel b as the hero evidence.
- Backend: R 4.4.2 for plotting, assembly, export and visual QA; local PyMOL is used only for coordinate rendering in Panel d.
- Final size: 183 × 158 mm.
- Export: editable SVG, vector PDF with embedded raster structure insets, and 600 dpi PNG.
- Biological boundary: comparative structural hypotheses only; no construct is called safe, compatible or experimentally validated.

## Automated data/QC summary

- Unique inserted constructs: 40.
- Tagged model rows used in Panels b/c: 48.
- Total structural rows including WT: 49.
- Geometry QC processed: 48 tagged / 49 including WT.
- Geometry QC completed tagged rows: 48; non-completed rows: 0.
- Oligomer-context evaluation rows: 96; tagged models without oligomer projection: 0.
- Duplicate construct-model rows: 0.
- Focal constructs present: 9/9.

The workload counts agree with docs/OPEN_STRUCTURE_PIPELINE_007_REPORT.md: 40 inserted constructs, 49 total model rows including one WT reference, 48 tagged model rows and 96 model × hexamer evaluations. The Figure source-data TSV excludes WT because Panel b represents inserted structural models only.

The earlier 005 report covered 132 proxy-layer constructs but explicitly lacked inserted 3D models. This is a scope difference, not an unexplained numerical discrepancy.

## Visual language

The requested American-comic influence is limited to flat high-contrast ink outlines, a compact halftone texture in the workflow, and restrained semantic colours. Panel c inherits only the visual grammar of the supplied reference: four pale-to-deep blue metric families, narrow vertical bars, black raw-model points and black min-max whiskers. Junction and tag are printed directly on the x axes. Panel d uses a light-grey WT, saturated blue inserted chain and orange tag to maximise structural contrast. Axes, labels, white background and data density follow publication-figure conventions. There are no shadows, glossy effects, rainbow colours, 3D bars, significance stars or decorative composite scores.

## Caption

**Fig. 5 | Explicit insertion modeling reveals strong site × tag differences in local structural perturbation.** **a,** Full-length inserted sequences were predicted, aligned to WT, quantified by global and local C-alpha RMSD, processed by OpenMM geometry QC, and projected into two project hexamer contexts. The workflow comprised 40 inserted constructs, 48 tagged structural models and 96 model × hexamer evaluations. **b,** Global/native C-alpha RMSD is plotted against local-window RMSD for every individual tagged model; point shape denotes tag identity and fill denotes the current expert-adjudicated construct class. Nine focal constructs are connected to fixed callout labels by dashed leaders. Dashed dataset medians are visual guides rather than structural pass/fail thresholds. **c,** Four blue metric panels compare focal constructs across global RMSD, local RMSD, WT native-contact loss and oligomer-context clash burden. Narrow bars show the model median; for the five constructs with one model, the bar is the single-model value. Black points and min-max whiskers are displayed only for the four constructs with three computational structure predictions (different seed/rank combinations). These model runs are not biological or experimental replicates, and no inferential statistics are applied. **d,** Fixed-view structural overlays show WT in light grey, inserted chains in saturated blue and tags in orange. Global and local perturbation can diverge, showing that global RMSD alone is insufficient. Relatively lower-perturbation constructs emerge from this comparative modeling layer, but geometry QC and oligomer-context evaluation do not constitute experimental validation, biological compatibility or safety. Source data are provided as a Source Data file.

## Reproducibility

1. Render each inset in a fresh process to avoid intermittent evaluation-build watermarks: D:\Pymol\python.exe scripts\render_figure05_structure_insets.py A89_2C_289_290_MAP8; repeat for A89_2C_290_291_MAP8 and A89_2C_248_249_MAP8.
2. Run D:\R-4.4.2\bin\Rscript.exe scripts\plot_figure05_inserted_structure_landscape.R from a pure-ASCII mirror of the repository if this Windows R build cannot decode the Chinese workspace path.
3. The R export packages are loaded from the recorded local ASCII-path library; final outputs are copied back without changing inputs or visual logic.
4. The 600 dpi PNG is globally quantized to 16 levels per colour channel in R after rendering to reduce Git storage overhead. Canvas dimensions, coordinates, labels and quantitative encodings are unchanged; SVG/PDF remain the vector masters.

## Final QA

- [x] Structural summary files discovered and read.
- [x] Panel b uses all individual tagged models rather than construct averages.
- [x] Panel c shows black points and min-max whiskers only for constructs with n=3 computational predictions; n=1 constructs are displayed as unadorned single-model bars.
- [x] Computational seed/rank repeats are explicitly separated from biological or experimental replication; no significance test or star annotation is shown.
- [x] Failed and missing rows are represented in QC; no tagged source row lacked a required model metric.
- [x] No arbitrary structural pass threshold or composite score was introduced.
- [x] Inset examples were chosen after quantitative review and use fixed orientation/zoom rules.
- [x] Structure insets were visually checked and contain no watermark.
- [x] SVG/PDF preserve vector text and quantitative marks; PyMOL snapshots are embedded raster images.
- [x] PNG exported at 600 dpi.

## Interpretation boundary

Relatively lower perturbation means lower values relative to the modeled comparison set. It must not be rewritten as stable, safe, tolerant, compatible or experimentally validated. The project hexamers are template-guided no-membrane/no-RNA hypotheses, and their clash metrics are contextual penalties rather than proof of a native RNA path.
