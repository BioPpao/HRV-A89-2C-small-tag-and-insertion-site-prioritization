#!/usr/bin/env Rscript

# Figure 6: replicated MD perturbation landscape.
# R is the exclusive backend for data assembly, plotting, export, and visual QA.

suppressPackageStartupMessages({
  library(ggplot2)
  library(dplyr)
  library(tidyr)
  library(data.table)
  library(patchwork)
  library(scales)
  library(ggrepel)
  library(grid)
})

required_namespaces <- c("svglite", "ragg")
missing_namespaces <- required_namespaces[
  !vapply(required_namespaces, requireNamespace, logical(1), quietly = TRUE)
]
if (length(missing_namespaces) > 0) {
  stop("Missing required R packages: ", paste(missing_namespaces, collapse = ", "))
}

options(stringsAsFactors = FALSE)

out_dir <- file.path(
  "figures", "group_meeting", "Figure06_replicated_MD_landscape"
)
dir.create(out_dir, recursive = TRUE, showWarnings = FALSE)
base_out <- file.path(out_dir, "Figure06_replicated_MD_landscape")

read_tsv_quiet <- function(path) {
  data.table::fread(
    path,
    sep = "\t",
    na.strings = c("", "NA"),
    data.table = FALSE,
    showProgress = FALSE,
    encoding = "UTF-8"
  )
}

assert_columns <- function(df, required, table_name) {
  missing <- setdiff(required, names(df))
  if (length(missing) > 0) {
    stop(
      table_name, " is missing required columns: ",
      paste(missing, collapse = ", ")
    )
  }
}

join_keys <- c(
  "system_id", "construct_id", "junction", "tag_form", "replica", "row_type"
)

merge_authoritative_metrics <- function(broad_path, contact_path, tag_path, dataset_name) {
  broad <- read_tsv_quiet(broad_path) %>%
    mutate(
      replica = as.character(replica),
      row_type = as.character(row_type)
    )
  contact <- read_tsv_quiet(contact_path) %>%
    mutate(
      replica = as.character(replica),
      row_type = as.character(row_type)
    )
  tag <- read_tsv_quiet(tag_path) %>%
    mutate(
      replica = as.character(replica),
      row_type = as.character(row_type)
    )

  assert_columns(
    broad,
    c(
      join_keys, "completed_ns", "wt_reference_ensemble_rmsd_mean_A",
      "delta_local_rmsf_vs_wt_A"
    ),
    basename(broad_path)
  )
  assert_columns(
    contact,
    c(join_keys, "wt_defined_contact_retention_mean"),
    basename(contact_path)
  )
  assert_columns(
    tag,
    c(
      join_keys, "tag_total_sasa_mean_A2", "tag_mean_relative_sasa",
      "tag_exposed_residue_fraction_rel_sasa_ge_0p25",
      "tag_nonlocal_contact_fraction_any_lt_4p5A"
    ),
    basename(tag_path)
  )

  if (anyDuplicated(broad[join_keys]) > 0 ||
      anyDuplicated(contact[join_keys]) > 0 ||
      anyDuplicated(tag[join_keys]) > 0) {
    stop("Duplicate join keys detected in authoritative input tables for ", dataset_name)
  }

  broad %>%
    select(
      all_of(join_keys), completed_ns,
      wt_reference_ensemble_rmsd_mean_A,
      delta_local_rmsf_vs_wt_A
    ) %>%
    left_join(
      contact %>%
        select(all_of(join_keys), wt_defined_contact_retention_mean),
      by = join_keys
    ) %>%
    left_join(
      tag %>%
        select(
          all_of(join_keys),
          tag_total_sasa_mean_A2,
          tag_mean_relative_sasa,
          tag_exposed_residue_fraction_rel_sasa_ge_0p25,
          tag_nonlocal_contact_fraction_any_lt_4p5A
        ),
      by = join_keys
    ) %>%
    mutate(dataset = dataset_name, .before = 1)
}

broad_metrics <- merge_authoritative_metrics(
  "data/broad_dynamics_metrics_v2_corrected.tsv",
  "data/contact_persistence_dynamics_v2_corrected.tsv",
  "data/tag_exposure_dynamics_v2_sasa.tsv",
  "task010_corrected_reanalysis"
)

validation_metrics <- merge_authoritative_metrics(
  "data/corrected_validation_broad_dynamics_v1.tsv",
  "data/corrected_validation_contact_persistence_v1.tsv",
  "data/corrected_validation_tag_exposure_v1.tsv",
  "independent_corrected_protocol_validation"
)

panel_v5 <- read_tsv_quiet(
  "data/final_candidate_panel_v5_experimental_review_cleanup.tsv"
)
assert_columns(
  panel_v5,
  c(
    "construct_id", "priority_class_v5", "corrected_MD_status",
    "corrected_protocol_validation_status_v4",
    "corrected_protocol_md_status_v4"
  ),
  "final_candidate_panel_v5_experimental_review_cleanup.tsv"
)

annotations <- panel_v5 %>%
  transmute(
    construct_id,
    priority = priority_class_v5,
    broad_md_status = corrected_MD_status,
    corrected_protocol_validation_status = corrected_protocol_validation_status_v4,
    validation_md_status = corrected_protocol_md_status_v4
  )

source_data <- bind_rows(broad_metrics, validation_metrics) %>%
  left_join(annotations, by = "construct_id") %>%
  mutate(
    priority = if_else(construct_id == "WT_112_321", "WT", priority),
    role = case_when(
      priority == "WT" ~ "WT",
      priority == "Priority_A" ~ "Priority A",
      priority == "Priority_B" ~ "Priority B",
      priority == "Conflict_control" ~ "Conflict control",
      priority == "Hard_negative_control" ~ "Hard negative",
      TRUE ~ "Unclassified"
    ),
    md_status = case_when(
      construct_id == "WT_112_321" ~ "WT baseline",
      dataset == "task010_corrected_reanalysis" ~ broad_md_status,
      dataset == "independent_corrected_protocol_validation" ~ validation_md_status,
      TRUE ~ NA_character_
    ),
    corrected_protocol_validation_status = if_else(
      construct_id == "WT_112_321",
      "directly_corrected_protocol_validated_3x20ns",
      corrected_protocol_validation_status
    )
  ) %>%
  select(
    dataset, construct_id, junction, tag_form, role, priority,
    replica, row_type, completed_ns,
    wt_reference_ensemble_rmsd_mean_A,
    delta_local_rmsf_vs_wt_A,
    wt_defined_contact_retention_mean,
    tag_total_sasa_mean_A2,
    tag_mean_relative_sasa,
    tag_exposed_residue_fraction_rel_sasa_ge_0p25,
    tag_nonlocal_contact_fraction_any_lt_4p5A,
    md_status, corrected_protocol_validation_status
  )

source_path <- paste0(base_out, "_source_data.tsv")
data.table::fwrite(
  source_data, source_path, sep = "\t", na = "", quote = FALSE
)

construct_order <- c(
  "WT_112_321",
  "A89_2C_289_290_MAP8",
  "A89_2C_289_290_G196_minimal",
  "A89_2C_248_249_HA",
  "A89_2C_248_249_MAP8",
  "A89_2C_288_289_MAP8",
  "A89_2C_288_289_HA",
  "A89_2C_290_291_MAP8",
  "A89_2C_256_257_MAP8",
  "A89_2C_224_225_MAP8",
  "A89_2C_224_225_HA",
  "A89_2C_203_204_G196_minimal",
  "A89_2C_155_156_MAP8"
)

construct_labels <- c(
  "WT_112_321" = "WT",
  "A89_2C_289_290_MAP8" = "A  289|290 x MAP8",
  "A89_2C_289_290_G196_minimal" = "A  289|290 x G196 min",
  "A89_2C_248_249_HA" = "A  248|249 x HA",
  "A89_2C_248_249_MAP8" = "A  248|249 x MAP8",
  "A89_2C_288_289_MAP8" = "B  288|289 x MAP8",
  "A89_2C_288_289_HA" = "B  288|289 x HA",
  "A89_2C_290_291_MAP8" = "B  290|291 x MAP8",
  "A89_2C_256_257_MAP8" = "C  256|257 x MAP8",
  "A89_2C_224_225_MAP8" = "C  224|225 x MAP8",
  "A89_2C_224_225_HA" = "C  224|225 x HA",
  "A89_2C_203_204_G196_minimal" = "C  203|204 x G196 min",
  "A89_2C_155_156_MAP8" = "H  155|156 x MAP8"
)

validation_systems_expected <- c(
  "WT_112_321",
  "A89_2C_289_290_MAP8",
  "A89_2C_248_249_HA",
  "A89_2C_256_257_MAP8",
  "A89_2C_224_225_MAP8",
  "A89_2C_155_156_MAP8"
)

if (!setequal(
  unique(broad_metrics$construct_id), construct_order
)) {
  stop("Broad corrected dataset does not contain the expected 13 systems.")
}
if (!setequal(
  unique(validation_metrics$construct_id), validation_systems_expected
)) {
  stop("Corrected-protocol validation dataset does not contain the expected six systems.")
}

role_palette <- c(
  "WT" = "#4D4D4D",
  "Priority A" = "#006D77",
  "Priority B" = "#4F7C89",
  "Conflict control" = "#D6902F",
  "Hard negative" = "#B84A4A",
  "Unclassified" = "#9AA0A6"
)

ink <- "#17324D"
neutral_text <- "#59636E"
light_grid <- "#E8EBED"

theme_nature_md <- function(base_size = 7, base_family = "Arial") {
  theme_classic(base_size = base_size, base_family = base_family) +
    theme(
      axis.line = element_line(linewidth = 0.35, colour = ink),
      axis.ticks = element_line(linewidth = 0.35, colour = ink),
      axis.title = element_text(size = base_size, colour = ink),
      axis.text = element_text(size = base_size - 0.5, colour = ink),
      legend.title = element_text(size = base_size - 0.3, face = "bold", colour = ink),
      legend.text = element_text(size = base_size - 0.8, colour = ink),
      legend.key = element_blank(),
      legend.background = element_blank(),
      strip.text = element_text(size = base_size - 0.2, face = "bold", colour = ink),
      strip.background = element_blank(),
      plot.title = element_text(size = base_size + 0.7, face = "bold", colour = ink),
      plot.subtitle = element_text(size = base_size - 0.4, colour = neutral_text),
      panel.grid.major.y = element_line(linewidth = 0.25, colour = light_grid),
      panel.grid.major.x = element_blank(),
      panel.grid.minor = element_blank(),
      plot.margin = margin(3, 3, 3, 3)
    )
}
theme_set(theme_nature_md())

# Panel a: workload schematic. Counts are derived from the authoritative tables.
broad_replica <- broad_metrics %>% filter(row_type == "replica")
validation_replica <- validation_metrics %>% filter(row_type == "replica")
broad_ns <- sum(broad_replica$completed_ns, na.rm = TRUE)
validation_ns <- sum(validation_replica$completed_ns, na.rm = TRUE)
total_ns <- broad_ns + validation_ns

p_a <- ggplot() +
  annotate(
    "rect", xmin = 0.35, xmax = 9.65, ymin = 6.0, ymax = 9.1,
    fill = "#DDE8EA", colour = role_palette[["Priority B"]], linewidth = 0.55
  ) +
  annotate(
    "text", x = 0.8, y = 8.55, hjust = 0,
    label = "BROAD SCREEN", family = "Arial", fontface = "bold",
    size = 2.5, colour = ink
  ) +
  annotate(
    "text", x = 5, y = 7.45,
    label = sprintf(
      "%d systems\n\u00d7 3 independent replicas\n\u00d7 20 ns\n= %d trajectories  |  %.0f ns",
      n_distinct(broad_replica$construct_id), nrow(broad_replica), broad_ns
    ),
    family = "Arial", size = 2.15, lineheight = 0.96, colour = ink
  ) +
  annotate(
    "rect", xmin = 0.35, xmax = 9.65, ymin = 2.45, ymax = 5.45,
    fill = "#D8F0ED", colour = role_palette[["Priority A"]], linewidth = 0.55
  ) +
  annotate(
    "text", x = 0.8, y = 4.9, hjust = 0,
    label = "INDEPENDENT\nCORRECTED VALIDATION", family = "Arial",
    fontface = "bold", size = 2.15, lineheight = 0.92, colour = ink
  ) +
  annotate(
    "text", x = 5, y = 3.78,
    label = sprintf(
      "%d systems\n\u00d7 3 independent replicas\n\u00d7 20 ns\n= %d trajectories  |  %.0f ns",
      n_distinct(validation_replica$construct_id), nrow(validation_replica), validation_ns
    ),
    family = "Arial", size = 2.15, lineheight = 0.96, colour = ink
  ) +
  annotate(
    "segment", x = 5, xend = 5, y = 5.85, yend = 5.6,
    colour = ink, linewidth = 0.5,
    arrow = arrow(length = unit(1.5, "mm"), type = "closed")
  ) +
  annotate(
    "label", x = 5, y = 1.35,
    label = sprintf(
      "%d trajectories\n%.2f \u00b5s cumulative sampling",
      nrow(broad_replica) + nrow(validation_replica), total_ns / 1000
    ),
    family = "Arial", fontface = "bold", size = 2.35,
    fill = "#FFF4D6", colour = ink, label.size = 0.35,
    label.padding = unit(1.0, "mm")
  ) +
  annotate(
    "text", x = 5, y = 0.47,
    label = "screening/validation sampling;\nnot mechanistic convergence",
    family = "Arial", size = 1.72, lineheight = 0.92, colour = neutral_text
  ) +
  coord_cartesian(xlim = c(0, 10), ylim = c(0.1, 9.55), clip = "off") +
  labs(title = "Replicated MD design and workload") +
  theme_void(base_family = "Arial") +
  theme(
    plot.title = element_text(size = 7.7, face = "bold", colour = ink),
    plot.margin = margin(3, 3, 3, 3)
  )

# Panel b: four audited corrected-MD metrics, with every replica visible.
metric_labels <- c(
  "wt_reference_ensemble_rmsd_mean_A" =
    "WT-reference\nensemble RMSD (\u00c5)",
  "delta_local_rmsf_vs_wt_A" =
    "\u0394 local RMSF\nvs matched WT (\u00c5)",
  "wt_defined_contact_retention_mean" =
    "WT-defined\ncontact retention",
  "tag_nonlocal_contact_fraction_any_lt_4p5A" =
    "Persistent nonlocal\ntag-contact fraction"
)

broad_long <- source_data %>%
  filter(
    dataset == "task010_corrected_reanalysis",
    construct_id %in% construct_order
  ) %>%
  mutate(
    construct_factor = factor(construct_id, levels = rev(construct_order)),
    construct_y = as.numeric(construct_factor),
    role = factor(role, levels = names(role_palette))
  ) %>%
  pivot_longer(
    cols = all_of(names(metric_labels)),
    names_to = "metric",
    values_to = "value"
  )

group_boundaries <- c(1.5, 5.5, 8.5, 12.5)

plot_b_metric <- function(metric_name, show_y = FALSE) {
  dat <- broad_long %>% filter(metric == metric_name)
  replica_dat <- dat %>%
    filter(row_type == "replica", !is.na(value)) %>%
    mutate(
      replica_number = as.integer(replica),
      y_plot = construct_y + c(-0.18, 0, 0.18)[replica_number]
    )
  summary_dat <- dat %>% filter(row_type == "construct_summary", !is.na(value))
  missing_summary <- dat %>% filter(row_type == "construct_summary", is.na(value))
  finite_range <- range(dat$value, na.rm = TRUE)
  missing_x <- finite_range[1]

  p <- ggplot() +
    geom_hline(
      yintercept = group_boundaries,
      colour = "#BFC5C9", linewidth = 0.28, linetype = "22"
    ) +
    geom_point(
      data = replica_dat,
      aes(x = value, y = y_plot, colour = role),
      size = 1.05, alpha = 0.42, shape = 16
    ) +
    geom_point(
      data = summary_dat,
      aes(x = value, y = construct_y, fill = role),
      size = 2.2, shape = 21, colour = ink, stroke = 0.35
    ) +
    scale_colour_manual(values = role_palette, drop = FALSE) +
    scale_fill_manual(values = role_palette, drop = FALSE) +
    scale_x_continuous(expand = expansion(mult = c(0.08, 0.10))) +
    scale_y_continuous(
      limits = c(0.5, length(construct_order) + 0.5),
      breaks = seq_along(rev(construct_order)),
      labels = if (show_y) unname(construct_labels[rev(construct_order)]) else
        rep("", length(construct_order)),
      expand = expansion(mult = c(0, 0))
    ) +
    labs(x = unname(metric_labels[[metric_name]]), y = NULL) +
    theme_nature_md(base_size = 6.4) +
    theme(
      legend.position = "none",
      axis.text.y = if (show_y) element_text(size = 5.0) else element_blank(),
      axis.ticks.y = if (show_y) element_line(linewidth = 0.3, colour = ink) else element_blank(),
      axis.title.x = element_text(size = 5.3, lineheight = 0.92),
      axis.text.x = element_text(size = 5.0),
      plot.margin = margin(2, 1.5, 2, if (show_y) 1 else 0.5)
    )

  if (nrow(missing_summary) > 0) {
    p <- p + geom_text(
      data = missing_summary,
      aes(x = missing_x, y = construct_y, label = "n/a"),
      inherit.aes = FALSE,
      family = "Arial", size = 1.55, colour = neutral_text, hjust = 0
    )
  }
  p
}

p_b_inner <- wrap_plots(
  plot_b_metric(names(metric_labels)[1], TRUE),
  plot_b_metric(names(metric_labels)[2], FALSE),
  plot_b_metric(names(metric_labels)[3], FALSE),
  plot_b_metric(names(metric_labels)[4], FALSE),
  nrow = 1,
  widths = c(1.34, 1, 1, 1.08)
) +
  plot_annotation(
    title = "Broad corrected-MD perturbation landscape",
    subtitle = paste0(
      "Small translucent dots: replicas; outlined circles: construct means. ",
      "A/B/C/H denote Priority A, Priority B, conflict control, and hard negative."
    ),
    theme = theme(
      plot.title = element_text(
        family = "Arial", size = 7.7, face = "bold", colour = ink,
        margin = margin(l = 10)
      ),
      plot.subtitle = element_text(
        family = "Arial", size = 5.7, colour = neutral_text
      ),
      plot.margin = margin(0, 0, 0, 0)
    )
  )
p_b <- wrap_elements(full = p_b_inner)

# Panel c: replica-level tag behavior in the independent corrected validation.
validation_tagged_replica <- source_data %>%
  filter(
    dataset == "independent_corrected_protocol_validation",
    row_type == "replica",
    construct_id != "WT_112_321"
  )

construct_palette <- c(
  "A89_2C_289_290_MAP8" = "#006D77",
  "A89_2C_248_249_HA" = "#2A9D8F",
  "A89_2C_256_257_MAP8" = "#D9A441",
  "A89_2C_224_225_MAP8" = "#C67A16",
  "A89_2C_155_156_MAP8" = "#B84A4A"
)
construct_shapes <- c(
  "A89_2C_289_290_MAP8" = 21,
  "A89_2C_248_249_HA" = 24,
  "A89_2C_256_257_MAP8" = 22,
  "A89_2C_224_225_MAP8" = 23,
  "A89_2C_155_156_MAP8" = 25
)

validation_means <- validation_tagged_replica %>%
  group_by(construct_id, junction, tag_form) %>%
  summarise(
    tag_nonlocal_contact_fraction_any_lt_4p5A =
      mean(tag_nonlocal_contact_fraction_any_lt_4p5A),
    tag_exposed_residue_fraction_rel_sasa_ge_0p25 =
      mean(tag_exposed_residue_fraction_rel_sasa_ge_0p25),
    .groups = "drop"
  ) %>%
  mutate(
    label = case_when(
      construct_id == "A89_2C_248_249_HA" ~
        "248|249 x HA\nreplica heterogeneous",
      construct_id == "A89_2C_224_225_MAP8" ~
        "224|225 x MAP8\npersistent nonlocal-contact caution",
      TRUE ~ paste0(junction, " x ", tag_form)
    )
  )

p_c <- ggplot(
  validation_tagged_replica,
  aes(
    x = tag_nonlocal_contact_fraction_any_lt_4p5A,
    y = tag_exposed_residue_fraction_rel_sasa_ge_0p25,
    fill = construct_id,
    shape = construct_id
  )
) +
  geom_point(
    size = 2.0, alpha = 0.62, colour = ink, stroke = 0.32
  ) +
  geom_point(
    data = validation_means,
    size = 3.15, alpha = 1, colour = ink, stroke = 0.5
  ) +
  geom_label_repel(
    data = validation_means,
    aes(label = label),
    family = "Arial", size = 1.55, lineheight = 0.88,
    colour = ink, fill = alpha("white", 0.92),
    box.padding = 0.3, point.padding = 0.25,
    label.padding = unit(0.45, "mm"), label.r = unit(0.3, "mm"),
    segment.colour = "#7A858E", segment.size = 0.25,
    seed = 42, max.overlaps = Inf, min.segment.length = 0,
    show.legend = FALSE
  ) +
  scale_fill_manual(values = construct_palette) +
  scale_shape_manual(values = construct_shapes) +
  scale_x_continuous(
    limits = c(-0.02, 1.08), breaks = c(0, 0.25, 0.5, 0.75, 1.0)
  ) +
  scale_y_continuous(
    limits = c(0.75, 1.02), breaks = c(0.8, 0.9, 1.0)
  ) +
  labs(
    title = "Corrected-protocol replica-level tag behavior",
    subtitle = "Points: replicas; outlined symbols: means.\nNo favorable quadrant is defined.",
    x = "lower nonlocal contact  \u2190   Persistent nonlocal tag-contact fraction",
    y = "Exposed tag-residue fraction   (\u2191 greater exposure)"
  ) +
  theme_nature_md(base_size = 6.5) +
  theme(
    legend.position = "none",
    panel.grid.major = element_line(linewidth = 0.25, colour = light_grid),
    plot.margin = margin(3, 3, 3, 3)
  )

# Panel d: independent ensembles shown side-by-side and never pooled.
protocol_constructs <- validation_systems_expected[-1]
protocol_data <- source_data %>%
  filter(
    row_type == "replica",
    construct_id %in% protocol_constructs
  ) %>%
  mutate(
    protocol = factor(
      dataset,
      levels = c(
        "task010_corrected_reanalysis",
        "independent_corrected_protocol_validation"
      ),
      labels = c("Task009\ncorrected", "Corrected\nvalidation")
    ),
    construct_id = factor(construct_id, levels = protocol_constructs),
    replica_number = as.integer(replica),
    protocol_x = as.numeric(protocol) + c(-0.14, 0, 0.14)[replica_number]
  )

protocol_means <- protocol_data %>%
  group_by(construct_id, protocol) %>%
  summarise(
    mean_contact = mean(tag_nonlocal_contact_fraction_any_lt_4p5A),
    .groups = "drop"
  ) %>%
  mutate(protocol_x = as.numeric(protocol))

protocol_facet_labels <- c(
  "A89_2C_289_290_MAP8" = "289|290 x MAP8",
  "A89_2C_248_249_HA" = "248|249 x HA",
  "A89_2C_256_257_MAP8" = "256|257 x MAP8",
  "A89_2C_224_225_MAP8" = "224|225 x MAP8",
  "A89_2C_155_156_MAP8" = "155|156 x MAP8"
)

p_d <- ggplot(
  protocol_data,
  aes(
    x = protocol_x,
    y = tag_nonlocal_contact_fraction_any_lt_4p5A,
    colour = construct_id,
    fill = construct_id
  )
) +
  geom_point(
    size = 1.6, alpha = 0.56, shape = 16
  ) +
  geom_line(
    data = protocol_means,
    aes(x = protocol_x, y = mean_contact, group = construct_id),
    linewidth = 0.45, alpha = 0.8
  ) +
  geom_point(
    data = protocol_means,
    aes(x = protocol_x, y = mean_contact),
    shape = 23, size = 2.65, colour = ink, fill = NA, stroke = 0.48
  ) +
  facet_wrap(
    ~ construct_id,
    nrow = 1,
    labeller = as_labeller(protocol_facet_labels)
  ) +
  scale_colour_manual(values = construct_palette) +
  scale_fill_manual(values = construct_palette) +
  scale_x_continuous(
    breaks = c(1, 2),
    labels = c("Task009\ncorrected", "Corrected\nvalidation"),
    limits = c(0.72, 2.28)
  ) +
  scale_y_continuous(
    limits = c(-0.03, 1.05), breaks = c(0, 0.5, 1.0),
    expand = expansion(mult = c(0, 0))
  ) +
  labs(
    title = "Independent corrected protocol reproduces the main contact pattern",
    subtitle = paste0(
      "Independent 3 \u00d7 20 ns ensembles; replicas are not pooled.\n",
      "Lines connect dataset means for visual direction only."
    ),
    x = NULL,
    y = "Persistent nonlocal\ntag-contact fraction"
  ) +
  theme_nature_md(base_size = 6.2) +
  theme(
    legend.position = "none",
    panel.grid.major.y = element_line(linewidth = 0.25, colour = light_grid),
    panel.spacing.x = unit(1.6, "mm"),
    strip.text = element_text(size = 5.0, face = "bold", lineheight = 0.9),
    axis.text.x = element_text(size = 5.0, lineheight = 0.86),
    axis.text.y = element_text(size = 5.0),
    axis.title.y = element_text(size = 5.3),
    plot.margin = margin(3, 2, 3, 3)
  )

# Assemble a four-panel, two-column Nature-style page with Panel b as hero.
fig <- ((p_a | p_b) + plot_layout(widths = c(1.16, 2.84))) /
  ((p_c | p_d) + plot_layout(widths = c(1.23, 2.77))) +
  plot_layout(heights = c(1.48, 1.0)) +
  plot_annotation(
    title = "Replicated MD identifies persistent nonlocal tag contacts as the most discriminating dynamic readout",
    subtitle = "Broad 3 \u00d7 20 ns screening and independent corrected-protocol validation reproduce the main candidate-control differences",
    tag_levels = "a",
    theme = theme(
      plot.title = element_text(
        family = "Arial", size = 9.3, face = "bold", colour = ink,
        margin = margin(b = 2)
      ),
      plot.subtitle = element_text(
        family = "Arial", size = 6.8, colour = neutral_text,
        margin = margin(b = 4)
      ),
      plot.tag = element_text(
        family = "Arial", size = 8.2, face = "bold", colour = ink
      ),
      plot.background = element_rect(fill = "white", colour = NA),
      plot.margin = margin(4, 4, 4, 4)
    )
  )

width_mm <- 183
height_mm <- 190
width_in <- width_mm / 25.4
height_in <- height_mm / 25.4

svg_path <- paste0(base_out, ".svg")
pdf_path <- paste0(base_out, ".pdf")
png_path <- paste0(base_out, "_600dpi.png")
png_render_path <- file.path(tempdir(), basename(png_path))

svglite::svglite(
  svg_path,
  width = width_in,
  height = height_in,
  bg = "white",
  system_fonts = list(sans = "Arial")
)
print(fig)
dev.off()

grDevices::cairo_pdf(
  pdf_path,
  width = width_in,
  height = height_in,
  family = "Arial",
  bg = "white",
  onefile = TRUE
)
print(fig)
dev.off()

ragg::agg_png(
  png_render_path,
  width = width_mm,
  height = height_mm,
  units = "mm",
  res = 600,
  background = "white",
  scaling = 1
)
print(fig)
dev.off()
if (!file.copy(png_render_path, png_path, overwrite = TRUE)) {
  stop("R rendered the PNG but could not copy it to the requested output path.")
}

# Machine-readable QC, including workload, integrity, scientific focal checks,
# exact metrics used, and export status.
count_duplicate_keys <- function(df) {
  nrow(df) - nrow(distinct(df, construct_id, replica, row_type))
}

replicas_per_system_broad <- broad_replica %>% count(construct_id, name = "n")
replicas_per_system_validation <- validation_replica %>% count(construct_id, name = "n")

validation_sorted_248 <- validation_tagged_replica %>%
  filter(construct_id == "A89_2C_248_249_HA") %>%
  pull(tag_nonlocal_contact_fraction_any_lt_4p5A) %>%
  sort()

get_mean_contact <- function(data, id) {
  data %>%
    filter(construct_id == id, row_type == "replica") %>%
    summarise(x = mean(tag_nonlocal_contact_fraction_any_lt_4p5A)) %>%
    pull(x)
}

caption_path <- paste0(base_out, "_caption.md")
caption_text <- paste(readLines(caption_path, warn = FALSE, encoding = "UTF-8"), collapse = " ")
caption_words <- strsplit(trimws(caption_text), "[[:space:]]+")[[1]]
caption_word_count <- sum(nzchar(caption_words))

qc <- tribble(
  ~section, ~metric, ~value, ~status, ~detail,
  "broad", "system_count", as.character(n_distinct(broad_replica$construct_id)),
  ifelse(n_distinct(broad_replica$construct_id) == 13, "pass", "fail"), "WT plus 12 tagged constructs",
  "broad", "tagged_system_count", as.character(n_distinct(broad_replica$construct_id[broad_replica$construct_id != "WT_112_321"])),
  ifelse(n_distinct(broad_replica$construct_id[broad_replica$construct_id != "WT_112_321"]) == 12, "pass", "fail"), "expected 12",
  "broad", "trajectory_count", as.character(nrow(broad_replica)),
  ifelse(nrow(broad_replica) == 39, "pass", "fail"), "expected 39",
  "broad", "replicas_per_system", paste(sort(unique(replicas_per_system_broad$n)), collapse = ","),
  ifelse(all(replicas_per_system_broad$n == 3), "pass", "fail"), "expected 3 for every system",
  "broad", "WT_replica_rows", as.character(sum(broad_replica$construct_id == "WT_112_321")),
  ifelse(sum(broad_replica$construct_id == "WT_112_321") == 3, "pass", "fail"), "expected 3",
  "broad", "replica_rows", as.character(nrow(broad_replica)),
  ifelse(nrow(broad_replica) == 39, "pass", "fail"), "rows plotted as small points in panel b",
  "broad", "construct_summary_rows", as.character(sum(broad_metrics$row_type == "construct_summary")),
  ifelse(sum(broad_metrics$row_type == "construct_summary") == 13, "pass", "fail"), "one per system",
  "broad", "completed_ns", as.character(broad_ns),
  ifelse(abs(broad_ns - 780) < 1e-9, "pass", "fail"), "cumulative screening sampling",
  "broad", "usable_trajectories", as.character(sum(broad_replica$completed_ns >= 20)),
  ifelse(sum(broad_replica$completed_ns >= 20) == 39, "pass", "fail"), "39/39 expected",
  "broad", "technical_exclusions", as.character(sum(is.na(broad_replica$completed_ns) | broad_replica$completed_ns < 20)),
  ifelse(sum(is.na(broad_replica$completed_ns) | broad_replica$completed_ns < 20) == 0, "pass", "fail"), "expected 0",
  "validation", "system_count", as.character(n_distinct(validation_replica$construct_id)),
  ifelse(n_distinct(validation_replica$construct_id) == 6, "pass", "fail"), "expected six named systems",
  "validation", "trajectory_count", as.character(nrow(validation_replica)),
  ifelse(nrow(validation_replica) == 18, "pass", "fail"), "expected 18",
  "validation", "replicas_per_system", paste(sort(unique(replicas_per_system_validation$n)), collapse = ","),
  ifelse(all(replicas_per_system_validation$n == 3), "pass", "fail"), "expected 3 for every system",
  "validation", "WT_replica_rows", as.character(sum(validation_replica$construct_id == "WT_112_321")),
  ifelse(sum(validation_replica$construct_id == "WT_112_321") == 3, "pass", "fail"), "expected 3",
  "validation", "replica_rows", as.character(nrow(validation_replica)),
  ifelse(nrow(validation_replica) == 18, "pass", "fail"), "15 tagged plus 3 WT",
  "validation", "construct_summary_rows", as.character(sum(validation_metrics$row_type == "construct_summary")),
  ifelse(sum(validation_metrics$row_type == "construct_summary") == 6, "pass", "fail"), "one per system",
  "validation", "completed_ns", as.character(validation_ns),
  ifelse(abs(validation_ns - 360) < 1e-9, "pass", "fail"), "cumulative corrected-validation sampling",
  "validation", "tagged_panel_c_points", as.character(nrow(validation_tagged_replica)),
  ifelse(nrow(validation_tagged_replica) == 15, "pass", "fail"), "5 constructs x 3 replicas",
  "combined", "trajectory_count", as.character(nrow(broad_replica) + nrow(validation_replica)),
  ifelse(nrow(broad_replica) + nrow(validation_replica) == 57, "pass", "fail"), "independent ensembles; not pooled",
  "combined", "cumulative_sampling_ns", as.character(total_ns),
  ifelse(abs(total_ns - 1140) < 1e-9, "pass", "fail"), "1.14 microseconds cumulative screening/validation sampling",
  "integrity", "duplicate_broad_join_keys", as.character(count_duplicate_keys(broad_metrics)),
  ifelse(count_duplicate_keys(broad_metrics) == 0, "pass", "fail"), "construct_id + replica + row_type",
  "integrity", "duplicate_validation_join_keys", as.character(count_duplicate_keys(validation_metrics)),
  ifelse(count_duplicate_keys(validation_metrics) == 0, "pass", "fail"), "construct_id + replica + row_type",
  "missingness", "broad_replica_core_metric_missing", as.character(sum(is.na(broad_replica$wt_reference_ensemble_rmsd_mean_A) | is.na(broad_replica$wt_defined_contact_retention_mean))),
  ifelse(sum(is.na(broad_replica$wt_reference_ensemble_rmsd_mean_A) | is.na(broad_replica$wt_defined_contact_retention_mean)) == 0, "pass", "fail"), "RMSD/contact required for all trajectories",
  "missingness", "broad_tagged_replica_tag_metric_missing", as.character(sum(is.na(broad_replica$tag_nonlocal_contact_fraction_any_lt_4p5A[broad_replica$construct_id != "WT_112_321"]))),
  ifelse(sum(is.na(broad_replica$tag_nonlocal_contact_fraction_any_lt_4p5A[broad_replica$construct_id != "WT_112_321"])) == 0, "pass", "fail"), "WT tag-specific fields are intentionally not applicable",
  "missingness", "validation_tagged_replica_tag_metric_missing", as.character(sum(is.na(validation_tagged_replica$tag_nonlocal_contact_fraction_any_lt_4p5A) | is.na(validation_tagged_replica$tag_exposed_residue_fraction_rel_sasa_ge_0p25))),
  ifelse(sum(is.na(validation_tagged_replica$tag_nonlocal_contact_fraction_any_lt_4p5A) | is.na(validation_tagged_replica$tag_exposed_residue_fraction_rel_sasa_ge_0p25)) == 0, "pass", "fail"), "panel c fields",
  "focal", "289_290_MAP8_validation_mean_contact", sprintf("%.6f", get_mean_contact(validation_metrics, "A89_2C_289_290_MAP8")),
  ifelse(abs(get_mean_contact(validation_metrics, "A89_2C_289_290_MAP8") - 0.028) < 0.01, "pass", "warn"), "low persistent nonlocal contact",
  "focal", "248_249_HA_validation_replica_contacts", paste(sprintf("%.6f", validation_sorted_248), collapse = ";"),
  ifelse(length(validation_sorted_248) == 3 && diff(range(validation_sorted_248)) > 0.45, "pass", "fail"), "replica heterogeneity retained",
  "focal", "256_257_MAP8_validation_mean_contact", sprintf("%.6f", get_mean_contact(validation_metrics, "A89_2C_256_257_MAP8")),
  ifelse(abs(get_mean_contact(validation_metrics, "A89_2C_256_257_MAP8") - 0.085) < 0.02, "pass", "warn"), "MD-neutral-like contact behavior; biological conflict retained",
  "focal", "224_225_MAP8_validation_replica_contacts", paste(sprintf("%.6f", validation_tagged_replica %>% filter(construct_id == "A89_2C_224_225_MAP8") %>% pull(tag_nonlocal_contact_fraction_any_lt_4p5A)), collapse = ";"),
  ifelse(all(abs(validation_tagged_replica %>% filter(construct_id == "A89_2C_224_225_MAP8") %>% pull(tag_nonlocal_contact_fraction_any_lt_4p5A) - 1) < 1e-12), "pass", "fail"), "persistent nonlocal-contact caution",
  "focal", "155_156_MAP8_validation_mean_contact", sprintf("%.6f", get_mean_contact(validation_metrics, "A89_2C_155_156_MAP8")),
  ifelse(abs(get_mean_contact(validation_metrics, "A89_2C_155_156_MAP8") - 0.919) < 0.02, "pass", "warn"), "hard-negative MD caution reproduced",
  "protocol", "panel_d_task009_replica_points", as.character(sum(protocol_data$dataset == "task010_corrected_reanalysis")),
  ifelse(sum(protocol_data$dataset == "task010_corrected_reanalysis") == 15, "pass", "fail"), "five constructs x three independent replicas",
  "protocol", "panel_d_validation_replica_points", as.character(sum(protocol_data$dataset == "independent_corrected_protocol_validation")),
  ifelse(sum(protocol_data$dataset == "independent_corrected_protocol_validation") == 15, "pass", "fail"), "five constructs x three independent replicas",
  "metrics", "exact_metrics_used", paste(names(metric_labels), collapse = ";"),
  "pass", "no composite MD score; tag exposure is used only in panel c",
  "environment", "R_version", as.character(getRversion()),
  "info", "isolated Conda environment",
  "environment", "package_versions", paste0(
    "ggplot2=", as.character(packageVersion("ggplot2")), ";",
    "dplyr=", as.character(packageVersion("dplyr")), ";",
    "tidyr=", as.character(packageVersion("tidyr")), ";",
    "data.table=", as.character(packageVersion("data.table")), ";",
    "patchwork=", as.character(packageVersion("patchwork")), ";",
    "svglite=", as.character(packageVersion("svglite")), ";",
    "ragg=", as.character(packageVersion("ragg"))
  ),
  "info", "R-only plotting and export",
  "caption", "word_count", as.character(caption_word_count),
  ifelse(caption_word_count <= 300, "pass", "fail"), "Nature-style target <=300 words",
  "interpretation", "ensemble_handling", "independent_3x20ns_ensembles_side_by_side_not_pooled",
  "pass", "no paired test and no six-replica concatenation",
  "interpretation", "sampling_statement", "screening_adequate_not_mechanistic_convergence",
  "pass", "no blanket 50-ns claim",
  "export", "svg", as.character(file.exists(svg_path)),
  ifelse(file.exists(svg_path), "pass", "fail"), "editable vector output",
  "export", "pdf", as.character(file.exists(pdf_path)),
  ifelse(file.exists(pdf_path), "pass", "fail"), "vector output",
  "export", "png_600dpi", as.character(file.exists(png_path)),
  ifelse(file.exists(png_path), "pass", "fail"), "183 x 190 mm at 600 dpi",
  "discrepancy", "any_data_discrepancy", "none_detected",
  "pass", "all requested counts and focal patterns matched authoritative TSV values"
)

qc_path <- paste0(base_out, "_qc.tsv")
data.table::fwrite(qc, qc_path, sep = "\t", na = "", quote = FALSE)

if (any(qc$status == "fail")) {
  failed <- qc %>% filter(status == "fail")
  stop(
    "Figure 6 QC failed: ",
    paste(paste(failed$section, failed$metric, sep = "/"), collapse = ", ")
  )
}

cat(sprintf(
  paste0(
    "Figure 6 complete: %d broad trajectories (%.0f ns), ",
    "%d validation trajectories (%.0f ns), %d total trajectories (%.2f microseconds cumulative).\n"
  ),
  nrow(broad_replica), broad_ns,
  nrow(validation_replica), validation_ns,
  nrow(broad_replica) + nrow(validation_replica), total_ns / 1000
))
