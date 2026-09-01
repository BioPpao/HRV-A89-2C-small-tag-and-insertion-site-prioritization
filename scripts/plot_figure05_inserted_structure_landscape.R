#!/usr/bin/env Rscript

# Figure 5: explicit tag-insertion structural perturbation landscape.
# R is the exclusive plotting, assembly, export, and visual-QA backend.

local_lib <- "C:/Users/Paopao/.codex/visualizations/2026/08/29/01a04e3d-e408-7510-bbc4-a66261a423b2/r-lib/4.4"
.libPaths(c(local_lib, .libPaths()))

suppressPackageStartupMessages({
  library(ggplot2)
  library(dplyr)
  library(tidyr)
  library(patchwork)
  library(readr)
  library(scales)
  library(ggrepel)
  library(png)
  library(grid)
})

missing_export <- c("svglite", "ragg")[
  !vapply(c("svglite", "ragg"), requireNamespace, logical(1), quietly = TRUE)
]
if (length(missing_export) > 0) {
  stop("Missing required R export packages: ", paste(missing_export, collapse = ", "))
}

out_dir <- file.path("figures", "group_meeting", "Figure05_inserted_structure_landscape")
dir.create(out_dir, recursive = TRUE, showWarnings = FALSE)
base_out <- file.path(out_dir, "Figure05_inserted_structure_landscape")
read_tsv_quiet <- function(path) readr::read_tsv(
  path, show_col_types = FALSE, progress = FALSE
)

perturb_all <- read_tsv_quiet("data/tag_site_structure_perturbation_v3_open.tsv")
openmm_all <- read_tsv_quiet("data/tag_site_openmm_qc_v1.tsv")
panel <- read_tsv_quiet("data/tag_site_structure_panel_v3_open.tsv")
contact <- read_tsv_quiet("data/tag_site_contact_network_v3_open.tsv")
hexamer <- read_tsv_quiet("data/tag_site_hexamer_context_v3_open.tsv")
accessibility <- read_tsv_quiet("data/tag_site_secondary_structure_accessibility_v1.tsv")
integrated <- read_tsv_quiet("data/tag_site_integrated_perturbation_v3_open.tsv")
candidate_junctions <- read_tsv_quiet("data/candidate_junctions_v2.tsv")
final_v5 <- read_tsv_quiet("data/final_candidate_panel_v5_experimental_review_cleanup.tsv")

perturb <- perturb_all %>% filter(tag_form != "WT")
openmm <- openmm_all %>% filter(tag_form != "WT")

hex_model <- hexamer %>%
  group_by(construct_id, model_file) %>%
  summarise(
    oligomer_context_rows = n(),
    min_tag_neighbor_A = min(min_tag_neighbor_A, na.rm = TRUE),
    max_tag_neighbor_clashes_2p5A = max(tag_neighbor_clashes_2p5A, na.rm = TRUE),
    max_tag_neighbor_contacts_5A = max(tag_neighbor_contacts_5A, na.rm = TRUE),
    .groups = "drop"
  )

class_lookup <- final_v5 %>%
  transmute(
    construct_id,
    priority_raw = coalesce(priority_class_v5, priority_class),
    corrected_protocol_validation_status,
    experimental_review_annotation_v5
  )

normalize_class <- function(x, construct_id) {
  case_when(
    x == "Priority_A" ~ "Priority_A",
    x == "Priority_B" ~ "Priority_B",
    grepl("conflict", x, ignore.case = TRUE) ~ "Conflict_control",
    grepl("hard", x, ignore.case = TRUE) ~ "Hard_negative_control",
    construct_id == "A89_2C_155_156_MAP8" ~ "Hard_negative_control",
    TRUE ~ "Other"
  )
}

source_data <- perturb %>%
  left_join(
    panel %>% select(construct_id, tag_sequence, functional_tier, insertion_direct_class),
    by = "construct_id"
  ) %>%
  left_join(
    openmm %>% select(
      construct_id, model_file, openmm_status, post_openmm_severe_clashes_2A,
      native_ca_rmsd_pre_post_A, local_ca_rmsd_pre_post_A
    ),
    by = c("construct_id", "model_file")
  ) %>%
  left_join(
    contact %>% select(
      construct_id, model_file, wt_contact_count, tagged_native_contact_count,
      native_contact_loss_count, native_contact_gain_count,
      local_contact_loss_count, local_contact_gain_count
    ),
    by = c("construct_id", "model_file")
  ) %>%
  left_join(hex_model, by = c("construct_id", "model_file")) %>%
  left_join(
    accessibility %>% select(
      construct_id, model_file, tag_mean_sasa_A2, local_coil_fraction, tag_coil_fraction
    ),
    by = c("construct_id", "model_file")
  ) %>%
  left_join(
    integrated %>% select(construct_id, open_structure_interpretation),
    by = "construct_id"
  ) %>%
  left_join(class_lookup, by = "construct_id") %>%
  left_join(
    candidate_junctions %>% select(
      junction, structural_track, conservation_class = hrvA_conservation_class_v2
    ),
    by = "junction"
  ) %>%
  mutate(
    model_id = basename(model_file),
    seed_id = suppressWarnings(as.integer(sub(".*seed_([0-9]+).*", "\\1", model_file))),
    rank_id = suppressWarnings(as.integer(sub(".*rank_([0-9]+).*", "\\1", model_file))),
    global_rmsd = native_2c_ca_rmsd_to_wt_A,
    local_rmsd = local_window_ca_rmsd_A,
    contact_retention_or_loss_metric = native_contact_loss_count,
    contact_metric_definition = "native_contact_loss_count (lower = fewer WT contacts lost)",
    oligomer_context_metric_or_class = max_tag_neighbor_clashes_2p5A,
    oligomer_metric_definition = "maximum tag-neighbor clashes <2.5 A across two project hexamers",
    geometry_qc_status = openmm_status,
    tag_sasa_if_available = tag_mean_sasa_A2,
    exposed_fraction_if_available = NA_real_,
    construct_class = factor(
      normalize_class(priority_raw, construct_id),
      levels = c(
        "Priority_A", "Priority_B", "Conflict_control",
        "Hard_negative_control", "Other"
      )
    ),
    tag_form = factor(
      tag_form,
      levels = c("MAP8", "HA", "G196_minimal", "G196_practical_GS")
    ),
    direct_EV_A71_insertion_class = insertion_direct_class
  ) %>%
  select(
    construct_id, junction, tag_form, tag_sequence, model_id, seed_id, rank_id, model_file,
    global_rmsd, local_rmsd,
    contact_retention_or_loss_metric, contact_metric_definition,
    oligomer_context_metric_or_class, oligomer_metric_definition,
    min_tag_neighbor_A, max_tag_neighbor_contacts_5A,
    geometry_qc_status, post_openmm_severe_clashes_2A,
    tag_sasa_if_available, exposed_fraction_if_available,
    construct_class, functional_tier, structural_track, conservation_class,
    direct_EV_A71_insertion_class, corrected_protocol_validation_status,
    experimental_review_annotation_v5, open_structure_interpretation
  )

source_path <- paste0(base_out, "_source_data.tsv")
readr::write_tsv(source_data, source_path, na = "")

# Automated QC with summary, per-construct, per-tag, per-junction, and focal checks.
focal_ids <- c(
  "A89_2C_289_290_MAP8", "A89_2C_289_290_G196_minimal",
  "A89_2C_290_291_MAP8", "A89_2C_290_291_G196_minimal",
  "A89_2C_248_249_MAP8", "A89_2C_248_249_HA",
  "A89_2C_256_257_MAP8", "A89_2C_224_225_MAP8",
  "A89_2C_155_156_MAP8"
)

required_metric_missing <- sum(!complete.cases(source_data %>% select(
  global_rmsd, local_rmsd, contact_retention_or_loss_metric,
  oligomer_context_metric_or_class, geometry_qc_status
)))
duplicate_rows <- nrow(source_data) - n_distinct(
  paste(source_data$construct_id, source_data$model_file)
)

summary_qc <- tibble(
  section = "summary", entity = "all",
  metric = c(
    "unique_constructs", "unique_structural_model_rows_tagged",
    "total_structural_model_rows_including_WT", "geometry_qc_processed_tagged",
    "geometry_qc_processed_including_WT", "geometry_qc_success_tagged",
    "geometry_qc_failure_tagged", "rows_with_missing_global_or_local_rmsd",
    "rows_with_missing_structure_metrics_any", "duplicate_construct_model_rows",
    "models_without_oligomer_context", "oligomer_context_evaluation_rows",
    "focal_constructs_expected", "focal_constructs_present", "focal_constructs_missing"
  ),
  value = as.character(c(
    n_distinct(source_data$construct_id), n_distinct(source_data$model_file),
    nrow(perturb_all), nrow(openmm), nrow(openmm_all),
    sum(grepl("^completed", source_data$geometry_qc_status)),
    sum(!grepl("^completed", source_data$geometry_qc_status)),
    sum(is.na(source_data$global_rmsd) | is.na(source_data$local_rmsd)),
    required_metric_missing, duplicate_rows,
    sum(is.na(source_data$oligomer_context_metric_or_class)), nrow(hexamer),
    length(focal_ids), sum(focal_ids %in% source_data$construct_id),
    sum(!focal_ids %in% source_data$construct_id)
  )),
  status = c(
    rep("info", 5),
    ifelse(sum(grepl("^completed", source_data$geometry_qc_status)) == nrow(source_data), "pass", "warn"),
    ifelse(sum(!grepl("^completed", source_data$geometry_qc_status)) == 0, "pass", "warn"),
    ifelse(sum(is.na(source_data$global_rmsd) | is.na(source_data$local_rmsd)) == 0, "pass", "warn"),
    ifelse(required_metric_missing == 0, "pass", "warn"),
    ifelse(duplicate_rows == 0, "pass", "fail"),
    ifelse(sum(is.na(source_data$oligomer_context_metric_or_class)) == 0, "pass", "warn"),
    "info", "info",
    ifelse(sum(focal_ids %in% source_data$construct_id) == length(focal_ids), "pass", "warn"),
    ifelse(sum(!focal_ids %in% source_data$construct_id) == 0, "pass", "warn")
  ),
  detail = ""
)

per_construct_qc <- source_data %>%
  group_by(construct_id) %>%
  summarise(
    value = as.character(n_distinct(model_file)),
    detail = paste0(
      "seeds=", paste(sort(unique(seed_id)), collapse = ","),
      "; junction=", first(junction), "; tag=", first(tag_form)
    ),
    .groups = "drop"
  ) %>%
  transmute(
    section = "per_construct", entity = construct_id,
    metric = "models_or_seeds_per_construct", value, status = "info", detail
  )

per_tag_qc <- source_data %>%
  distinct(construct_id, tag_form) %>%
  count(tag_form, name = "n_constructs") %>%
  transmute(
    section = "per_tag", entity = tag_form, metric = "unique_constructs_per_tag",
    value = as.character(n_constructs), status = "info", detail = ""
  )

per_junction_qc <- source_data %>%
  distinct(construct_id, junction) %>%
  count(junction, name = "n_constructs") %>%
  transmute(
    section = "per_junction", entity = junction,
    metric = "unique_constructs_per_junction",
    value = as.character(n_constructs), status = "info", detail = ""
  )

focal_qc <- tibble(
  section = "focal_construct", entity = focal_ids,
  metric = "focal_construct_present",
  value = ifelse(focal_ids %in% source_data$construct_id, "1", "0"),
  status = ifelse(focal_ids %in% source_data$construct_id, "pass", "fail"),
  detail = ""
)

qc <- bind_rows(summary_qc, per_construct_qc, per_tag_qc, per_junction_qc, focal_qc)
qc_path <- paste0(base_out, "_qc.tsv")
readr::write_tsv(qc, qc_path)

# Visual contract: restrained semantic colours with flat comic-ink accents.
ink <- "#17324D"
cream <- "#FFF9ED"
palette_class <- c(
  Priority_A = "#006D77", Priority_B = "#2A9D8F",
  Conflict_control = "#D6902F", Hard_negative_control = "#B84A4A",
  Other = "#9AA0A6"
)
shape_tag <- c(MAP8 = 21, HA = 22, G196_minimal = 24, G196_practical_GS = 23)

theme_nature_comic <- function(base_size = 7, base_family = "Arial") {
  theme_classic(base_size = base_size, base_family = base_family) +
    theme(
      axis.line = element_line(linewidth = 0.35, colour = ink),
      axis.ticks = element_line(linewidth = 0.35, colour = ink),
      axis.title = element_text(size = base_size, colour = ink),
      axis.text = element_text(size = base_size - 0.5, colour = ink),
      legend.title = element_text(size = base_size - 0.3, face = "bold", colour = ink),
      legend.text = element_text(size = base_size - 0.8, colour = ink),
      legend.key.height = unit(3.5, "mm"),
      plot.title = element_text(size = base_size + 0.6, face = "bold", colour = ink),
      plot.subtitle = element_text(size = base_size - 0.5, colour = "#59636E"),
      strip.text = element_text(size = base_size - 0.4, face = "bold", colour = ink),
      strip.background = element_rect(fill = cream, colour = ink, linewidth = 0.35),
      panel.grid = element_blank(),
      plot.margin = margin(3, 4, 3, 3)
    )
}
theme_set(theme_nature_comic())

# Panel a: vertical workflow with measured workload.
workflow <- tibble(
  x = 1, y = 7:1,
  label = c(
    "SELECTED SITE x TAG\nCONSTRUCTS", "FULL-LENGTH INSERTED\nSEQUENCES",
    "STRUCTURE\nPREDICTION", "ALIGNMENT\nTO WT",
    "GLOBAL + LOCAL\nPERTURBATION", "OPENMM\nGEOMETRY QC",
    "HEXAMER / OLIGOMER\nPROJECTION"
  ),
  fill = rep(c("#D8F0ED", "#DDE8F4"), length.out = 7)
)
halftone <- expand_grid(x = seq(0.15, 1.85, by = 0.14), y = seq(0.45, 7.55, by = 0.18))

p_a <- ggplot() +
  geom_point(data = halftone, aes(x, y), colour = ink, alpha = 0.055, size = 0.22) +
  geom_segment(
    data = tibble(x = 1, xend = 1, y = 6.63:1.63, yend = 6.37:1.37),
    aes(x, y, xend = xend, yend = yend), colour = ink, linewidth = 0.55,
    arrow = arrow(length = unit(1.35, "mm"), type = "closed")
  ) +
  geom_rect(
    data = workflow,
    aes(xmin = x - 0.70, xmax = x + 0.70, ymin = y - 0.34, ymax = y + 0.34, fill = fill),
    colour = ink, linewidth = 0.55
  ) +
  geom_text(
    data = workflow, aes(x, y, label = label), family = "Arial",
    fontface = "bold", colour = ink, size = 1.72, lineheight = 0.84
  ) +
  annotate(
    "label", x = 1, y = 7.80,
    label = sprintf(
      "%d constructs  |  %d inserted models\n%d hexamer evaluations",
      n_distinct(source_data$construct_id), nrow(source_data), nrow(hexamer)
    ),
    size = 1.48, lineheight = 0.92, family = "Arial", fontface = "bold",
    fill = "#F2C14E", colour = ink, linewidth = 0.35,
    label.padding = unit(0.85, "mm")
  ) +
  scale_fill_identity() +
  coord_cartesian(xlim = c(0, 2), ylim = c(0.35, 8.02), clip = "off") +
  labs(
    title = "Explicit insertion-modeling workflow",
    subtitle = sprintf(
      "%d/%d tagged models completed geometry QC",
      sum(grepl("^completed", source_data$geometry_qc_status)), nrow(source_data)
    )
  ) +
  theme_void(base_family = "Arial") +
  theme(
    plot.title = element_text(size = 7.6, face = "bold", colour = ink),
    plot.subtitle = element_text(size = 6.2, colour = "#59636E"),
    plot.margin = margin(3, 4, 3, 3)
  )

# Panel b: hero scatter using all individual inserted models.
x_med <- median(source_data$global_rmsd, na.rm = TRUE)
y_med <- median(source_data$local_rmsd, na.rm = TRUE)
x_rng <- range(source_data$global_rmsd, na.rm = TRUE)
y_rng <- range(source_data$local_rmsd, na.rm = TRUE)
label_ids <- focal_ids

label_data <- source_data %>%
  filter(construct_id %in% label_ids) %>%
  group_by(construct_id) %>%
  mutate(
    distance_to_construct_median =
      abs(global_rmsd - median(global_rmsd, na.rm = TRUE)) +
      abs(local_rmsd - median(local_rmsd, na.rm = TRUE))
  ) %>%
  slice_min(distance_to_construct_median, n = 1, with_ties = FALSE) %>%
  ungroup() %>%
  mutate(
    label = case_when(
      tag_form == "G196_minimal" ~ paste0(junction, " - G196 min"),
      TRUE ~ paste0(junction, " - ", tag_form)
    )
  ) %>%
  left_join(
    tribble(
      ~construct_id,                    ~label_x, ~label_y, ~label_hjust,
      "A89_2C_224_225_MAP8",               3.58,      7.0,            0,
      "A89_2C_248_249_MAP8",               3.58,      6.2,            0,
      "A89_2C_155_156_MAP8",               3.58,      5.4,            0,
      "A89_2C_290_291_MAP8",               3.58,      4.6,            0,
      "A89_2C_290_291_G196_minimal",       3.58,      3.8,            0,
      "A89_2C_256_257_MAP8",               3.58,      3.0,            0,
      "A89_2C_289_290_MAP8",               3.58,      2.2,            0,
      "A89_2C_248_249_HA",                 3.58,      1.4,            0,
      "A89_2C_289_290_G196_minimal",       3.58,      0.6,            0
    ),
    by = "construct_id"
  )

p_b <- ggplot(
  source_data,
  aes(x = global_rmsd, y = local_rmsd, fill = construct_class, shape = tag_form)
) +
  annotate("rect", xmin = -Inf, xmax = x_med, ymin = -Inf, ymax = y_med,
           fill = "#CFE8E4", alpha = 0.25) +
  annotate("rect", xmin = -Inf, xmax = x_med, ymin = y_med, ymax = Inf,
           fill = "#F2D49B", alpha = 0.16) +
  geom_vline(xintercept = x_med, linetype = "22", linewidth = 0.35, colour = "#7C8791") +
  geom_hline(yintercept = y_med, linetype = "22", linewidth = 0.35, colour = "#7C8791") +
  geom_point(colour = ink, stroke = 0.30, size = 1.72, alpha = 0.90) +
  geom_segment(
    data = label_data,
    aes(x = global_rmsd, y = local_rmsd, xend = label_x, yend = label_y),
    inherit.aes = FALSE, colour = "#687784", linewidth = 0.26, linetype = "22"
  ) +
  geom_label(
    data = label_data,
    aes(x = label_x, y = label_y, label = label, hjust = label_hjust),
    inherit.aes = FALSE, family = "Arial", size = 1.26,
    colour = ink, fill = "white", linewidth = 0.18,
    label.padding = unit(0.32, "mm"), label.r = unit(0.25, "mm"),
    lineheight = 0.88, show.legend = FALSE
  ) +
  scale_fill_manual(
    values = palette_class, drop = FALSE,
    breaks = names(palette_class),
    labels = c("Priority A", "Priority B", "Conflict control", "Hard-negative control", "Other")
  ) +
  scale_shape_manual(
    values = shape_tag, drop = FALSE,
    breaks = names(shape_tag),
    labels = c("MAP8", "HA", "G196 minimal", "G196 practical GS")
  ) +
  scale_x_continuous(expand = expansion(mult = c(0.08, 0.25))) +
  scale_y_continuous(expand = expansion(mult = c(0.14, 0.10))) +
  guides(
    fill = guide_legend(
      title = "Construct class", order = 1,
      override.aes = list(shape = 21, size = 1.55)
    ),
    shape = guide_legend(
      title = "Tag identity", order = 2,
      override.aes = list(fill = "white", size = 1.35, stroke = 0.30)
    )
  ) +
  labs(
    title = "Global structural perturbation landscape",
    subtitle = "Each point is one inserted model; dashed medians are visual guides, not pass/fail cut-offs.",
    x = "Global/native C-alpha RMSD (A)", y = "Local-window C-alpha RMSD (A)"
  ) +
  theme_nature_comic() +
  theme(
    legend.position = "right", legend.box = "vertical",
    legend.key.height = unit(2.8, "mm"),
    legend.margin = margin(0, 0, 0, 1), plot.margin = margin(3, 2, 3, 3)
  )

# Panel c: four reference-inspired vertical bar panels. Bars are deliberately
# narrow; computational repeat points and min-max whiskers appear only for n=3.
focal_labels <- c(
  "A89_2C_289_290_MAP8" = "289|290 MAP8",
  "A89_2C_289_290_G196_minimal" = "289|290 G196 min",
  "A89_2C_290_291_MAP8" = "290|291 MAP8",
  "A89_2C_290_291_G196_minimal" = "290|291 G196 min",
  "A89_2C_248_249_MAP8" = "248|249 MAP8",
  "A89_2C_248_249_HA" = "248|249 HA",
  "A89_2C_256_257_MAP8" = "256|257 MAP8",
  "A89_2C_224_225_MAP8" = "224|225 MAP8",
  "A89_2C_155_156_MAP8" = "155|156 MAP8"
)
metric_labels <- c(
  global_rmsd = "Global RMSD (A)", local_rmsd = "Local RMSD (A)",
  contact_retention_or_loss_metric = "Native contacts lost",
  oligomer_context_metric_or_class = "Max oligomer clashes"
)

focal_long <- source_data %>%
  filter(construct_id %in% names(focal_labels)) %>%
  mutate(
    construct_label = unname(focal_labels[construct_id]),
    construct_label = factor(construct_label, levels = unname(focal_labels))
  ) %>%
  pivot_longer(
    cols = all_of(names(metric_labels)), names_to = "metric", values_to = "value"
  ) %>%
  mutate(
    metric_label = factor(unname(metric_labels[metric]), levels = unname(metric_labels))
  )

focal_summary <- focal_long %>%
  group_by(construct_id, construct_label, construct_class, tag_form, metric_label) %>%
  summarise(
    value_min = min(value, na.rm = TRUE), value_max = max(value, na.rm = TRUE),
    value_median = median(value, na.rm = TRUE), n_models = n(), .groups = "drop"
  )

metric_palette <- c(
  "Global RMSD (A)" = "#C7D9EC",
  "Local RMSD (A)" = "#9FC9E8",
  "Native contacts lost" = "#79A5CA",
  "Max oligomer clashes" = "#4E72AE"
)

repeated_ids <- focal_summary %>%
  filter(n_models > 1) %>%
  distinct(construct_id) %>%
  pull(construct_id)

metric_bar_panel <- function(metric_name, colour, strip_text_colour = ink) {
  summary_metric <- focal_summary %>% filter(metric_label == metric_name)
  repeat_summary <- summary_metric %>% filter(n_models > 1)
  repeat_models <- focal_long %>%
    filter(metric_label == metric_name, construct_id %in% repeated_ids)

  ggplot(summary_metric, aes(x = construct_label, y = value_median)) +
    geom_col(width = 0.42, fill = colour, colour = ink, linewidth = 0.24) +
    geom_errorbar(
      data = repeat_summary, aes(ymin = value_min, ymax = value_max),
      width = 0.10, colour = "black", linewidth = 0.38
    ) +
    geom_point(
      data = repeat_models, aes(y = value),
      position = position_jitter(width = 0.075, height = 0, seed = 42),
      shape = 16, size = 1.00, colour = "black", alpha = 0.96
    ) +
    facet_wrap(~metric_label, nrow = 1) +
    scale_y_continuous(expand = expansion(mult = c(0, 0.16))) +
    labs(x = NULL, y = NULL) +
    theme_nature_comic(base_size = 6.2) +
    theme(
      legend.position = "none",
      axis.text.x = element_text(size = 5.0, angle = 67, hjust = 1, vjust = 1),
      axis.text.y = element_text(size = 5.0),
      axis.ticks.x = element_blank(),
      strip.background = element_rect(fill = colour, colour = ink, linewidth = 0.35),
      strip.text = element_text(size = 5.1, face = "bold", colour = strip_text_colour),
      plot.margin = margin(1.5, 1.5, 2.0, 1.5)
    )
}

p_c_metrics <- Map(
  metric_bar_panel,
  metric_name = names(metric_palette),
  colour = unname(metric_palette),
  strip_text_colour = c(ink, ink, ink, "white")
)

p_c_inner <- wrap_plots(p_c_metrics, nrow = 1) +
  plot_layout(widths = rep(1, 4)) +
  plot_annotation(
    title = "        Focal construct comparison",
    subtitle = paste0(
      "        Bars: model median; n=1 bars are single-model values.\n",
      "        Black dots + min-max whiskers: n=3 computational predictions only."
    )
  )
p_c <- wrap_elements(full = p_c_inner)

# Panel d: trim PyMOL white margins and assemble the three fixed-view snapshots in R.
trim_white <- function(img, threshold = 0.985, margin = 20) {
  rgb <- img[, , seq_len(min(3, dim(img)[3])), drop = FALSE]
  content <- apply(rgb < threshold, c(1, 2), any)
  rows <- which(rowSums(content) > 0)
  cols <- which(colSums(content) > 0)
  if (length(rows) == 0 || length(cols) == 0) return(img)
  r1 <- max(1, min(rows) - margin)
  r2 <- min(dim(img)[1], max(rows) + margin)
  c1 <- max(1, min(cols) - margin)
  c2 <- min(dim(img)[2], max(cols) + margin)
  img[r1:r2, c1:c2, , drop = FALSE]
}

structure_panel <- function(filename, title, accent) {
  img <- trim_white(png::readPNG(file.path(out_dir, filename)))
  ggplot() +
    annotation_custom(rasterGrob(img, interpolate = TRUE), -Inf, Inf, -Inf, Inf) +
    annotate("segment", x = 0.03, xend = 0.28, y = 0.96, yend = 0.96,
             colour = accent, linewidth = 1.5) +
    coord_cartesian(xlim = c(0, 1), ylim = c(0, 1), expand = FALSE) +
    labs(title = title) +
    theme_void(base_family = "Arial") +
    theme(
      plot.title = element_text(size = 5.8, face = "bold", colour = ink, hjust = 0),
      plot.margin = margin(1.0, 1.0, 1.0, 1.0)
    )
}

p_d1 <- structure_panel(
  "inset_289_290_MAP8.png", "289|290 x MAP8 | lower local perturbation",
  palette_class[["Priority_A"]]
)
p_d2 <- structure_panel(
  "inset_290_291_MAP8.png", "290|291 x MAP8 | adjacent-junction contrast",
  palette_class[["Priority_B"]]
)
p_d3 <- structure_panel(
  "inset_248_249_MAP8.png", "248|249 x MAP8 | global/local discordance",
  palette_class[["Priority_A"]]
)
p_d_inner <- (p_d1 / p_d2 / p_d3) +
  plot_layout(heights = c(1, 1, 1)) +
  plot_annotation(
    title = "    Representative WT overlays",
    subtitle = "WT light grey; inserted chain blue; tag orange."
  )
p_d <- wrap_elements(full = p_d_inner)

layout_design <- "
AAABBBBB
AAABBBBB
CCCCCDDD
CCCCCDDD
"
fig <- p_a + p_b + p_c + p_d +
  plot_layout(design = layout_design, heights = c(1, 1, 1.22, 1.22)) +
  plot_annotation(tag_levels = "a") &
  theme(
    plot.tag = element_text(family = "Arial", size = 8.2, face = "bold", colour = ink),
    plot.background = element_rect(fill = "white", colour = NA)
  )

width_mm <- 183
height_mm <- 158
width_in <- width_mm / 25.4
height_in <- height_mm / 25.4

svglite::svglite(paste0(base_out, ".svg"), width = width_in, height = height_in, bg = "white")
print(fig)
dev.off()

grDevices::cairo_pdf(
  paste0(base_out, ".pdf"), width = width_in, height = height_in,
  family = "Arial", bg = "white", onefile = TRUE
)
print(fig)
dev.off()

png_out <- paste0(base_out, "_600dpi.png")
ragg::agg_png(
  png_out, width = width_mm, height = height_mm,
  units = "mm", res = 600, background = "white"
)
print(fig)
dev.off()

# Preserve the 600-dpi canvas while reducing lossless Git storage overhead.
# Sixteen channel levels are visually indistinguishable at final size and
# do not change positions, labels, categories, or quantitative encodings.
png_image <- png::readPNG(png_out)
png::writePNG(round(png_image * 15) / 15, png_out, dpi = 600)

cat(sprintf(
  "Figure05 complete: %d tagged models, %d constructs, %d focal constructs present.\n",
  nrow(source_data), n_distinct(source_data$construct_id),
  sum(focal_ids %in% source_data$construct_id)
))
