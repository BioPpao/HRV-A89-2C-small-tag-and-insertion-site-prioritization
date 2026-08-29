Warning: fs12 was declared with const; use let for reassignable variables.
#!/usr/bin/env Rscript

# Figure 4: Tag-specific PLM landscape of HRV-A89 2C internal insertion junctions
# R-only, deterministic, publication-oriented workflow.

suppressPackageStartupMessages({
  local_lib <- file.path(getwd(), ".r-lib", "4.4")
  if (dir.exists(local_lib)) .libPaths(c(local_lib, .libPaths()))
  library(readr)
  library(dplyr)
  library(tidyr)
  library(ggplot2)
  library(patchwork)
  library(scales)
})

options(stringsAsFactors = FALSE, scipen = 999)

repo_root <- normalizePath(getwd(), winslash = "/", mustWork = TRUE)
out_dir <- file.path(repo_root, "figures", "group_meeting", "Figure04_PLM_landscape")
dir.create(out_dir, recursive = TRUE, showWarnings = FALSE)

input_paths <- c(
  plm = file.path(repo_root, "data", "tag_specific_plm_scores_v2_gpu.tsv"),
  plm_doc = file.path(repo_root, "docs", "TAG_SPECIFIC_PLM_SCAN_V2_GPU.md"),
  tag_doc = file.path(repo_root, "docs", "TAG_PORTFOLIO_V2.md"),
  junctions = file.path(repo_root, "data", "candidate_junctions_v2.tsv"),
  direct = file.path(repo_root, "data", "evA71_2C_direct_indel_to_A89_v1.tsv"),
  final_panel = file.path(repo_root, "data", "final_candidate_panel_v5_experimental_review_cleanup.tsv")
)

missing_inputs <- names(input_paths)[!file.exists(input_paths)]
if (length(missing_inputs) > 0) {
  stop("Missing required input(s): ", paste(missing_inputs, collapse = ", "))
}

plm <- read_tsv(input_paths[["plm"]], show_col_types = FALSE, progress = FALSE)
junctions <- read_tsv(input_paths[["junctions"]], show_col_types = FALSE, progress = FALSE)
direct <- read_tsv(input_paths[["direct"]], show_col_types = FALSE, progress = FALSE)
final_panel <- read_tsv(input_paths[["final_panel"]], show_col_types = FALSE, progress = FALSE)
plm_doc <- readLines(input_paths[["plm_doc"]], warn = FALSE, encoding = "UTF-8")
tag_doc <- readLines(input_paths[["tag_doc"]], warn = FALSE, encoding = "UTF-8")

tag_order <- c("MAP8", "HA", "G196_minimal", "G196_practical_GS")
expected_tags <- tibble::tribble(
  ~tag_form, ~tag_sequence, ~tag_length,
  "MAP8", "GDGMVPPG", 8,
  "HA", "YPYDVPDYA", 9,
  "G196_minimal", "DLVPR", 5,
  "G196_practical_GS", "GSDLVPRGS", 9
)
focal_junctions <- c(
  "155|156", "203|204", "224|225", "248|249", "256|257",
  "287|288", "288|289", "289|290", "290|291"
)
focal_left <- as.integer(sub("\\|.*$", "", focal_junctions))
major_ticks <- c(1, 50, 100, 150, 200, 250, 300, 320)

# ---------- Hard data-integrity gate ----------
required_plm_cols <- c(
  "tag_form", "tag_sequence", "tag_length", "a89_junction",
  "plm_delta_mean_pll_insert_minus_wt", "plm_status",
  "plm_rank_within_tag", "plm_percentile_within_tag"
)
required_junction_cols <- c(
  "junction", "left_resid", "functional_tier", "strict_structural_pass",
  "structural_track", "hrvA_conservation_class_v2"
)
required_direct_cols <- c(
  "a89_junction", "insertion_raw_log2_enrich2", "insertion_direct_class"
)

stopifnot(all(required_plm_cols %in% names(plm)))
stopifnot(all(required_junction_cols %in% names(junctions)))
stopifnot(all(required_direct_cols %in% names(direct)))
stopifnot(nrow(plm) == 1280L)
stopifnot(n_distinct(plm$a89_junction) == 320L)
stopifnot(setequal(unique(plm$tag_form), tag_order))
stopifnot(all(count(plm, tag_form)$n == 320L))
stopifnot(all(count(plm, a89_junction)$n == 4L))
stopifnot(all(plm$plm_status == "completed"))
stopifnot(sum(duplicated(plm[c("a89_junction", "tag_form")])) == 0L)
stopifnot(any(grepl("1280 / 1280", plm_doc, fixed = TRUE)))
stopifnot(any(grepl("No tag is assumed safe", tag_doc, fixed = TRUE)))

observed_tags <- plm %>%
  distinct(tag_form, tag_sequence, tag_length) %>%
  arrange(match(tag_form, tag_order))
stopifnot(nrow(observed_tags) == 4L)
stopifnot(identical(observed_tags$tag_form, expected_tags$tag_form))
stopifnot(identical(observed_tags$tag_sequence, expected_tags$tag_sequence))
stopifnot(identical(as.integer(observed_tags$tag_length), as.integer(expected_tags$tag_length)))

plm <- plm %>%
  mutate(
    left_resid = as.integer(sub("\\|.*$", "", a89_junction)),
    right_resid = as.integer(sub("^.*\\|", "", a89_junction))
  )
stopifnot(all(plm$right_resid == plm$left_resid + 1L))
stopifnot(setequal(unique(plm$left_resid), 1:320))
stopifnot(all(plm$a89_junction[plm$left_resid == 1L] == "1|2"))
stopifnot(all(plm$a89_junction[plm$left_resid == 320L] == "320|321"))

tag_spread <- plm %>%
  group_by(a89_junction, left_resid) %>%
  summarise(
    across_tag_spread = max(plm_delta_mean_pll_insert_minus_wt) -
      min(plm_delta_mean_pll_insert_minus_wt),
    .groups = "drop"
  ) %>%
  arrange(left_resid)
stopifnot(identical(tag_spread$left_resid, 1:320))

junction_meta <- junctions %>%
  transmute(
    junction,
    left_resid = as.integer(left_resid),
    functional_tier,
    strict_structural_pass = as.logical(strict_structural_pass),
    structural_track,
    conservation_class = hrvA_conservation_class_v2
  )
direct_meta <- direct %>%
  transmute(
    junction = a89_junction,
    evA71_direct_insertion_score = insertion_raw_log2_enrich2,
    evA71_direct_insertion_class = insertion_direct_class
  )

source_data <- plm %>%
  transmute(
    junction = a89_junction,
    left_resid,
    tag_form,
    tag_sequence,
    tag_length,
    delta_mean_pll = plm_delta_mean_pll_insert_minus_wt,
    within_tag_percentile = plm_percentile_within_tag,
    within_tag_rank = plm_rank_within_tag
  ) %>%
  left_join(junction_meta, by = c("junction", "left_resid")) %>%
  left_join(direct_meta, by = "junction") %>%
  left_join(tag_spread, by = c("junction" = "a89_junction", "left_resid")) %>%
  arrange(match(tag_form, tag_order), left_resid)

stopifnot(nrow(source_data) == 1280L)
stopifnot(!any(is.na(source_data$functional_tier)))
stopifnot(!any(is.na(source_data$conservation_class)))
stopifnot(!any(is.na(source_data$evA71_direct_insertion_class)))

source_path <- file.path(out_dir, "Figure04_tag_specific_PLM_landscape_source_data.tsv")
write_tsv(source_data, source_path, na = "")

delta <- source_data$delta_mean_pll
visual_limits <- as.numeric(quantile(delta, probs = c(0.02, 0.98), na.rm = TRUE, names = FALSE))
stopifnot(visual_limits[1] < 0, visual_limits[2] > 0)

# ---------- Scientific calibration checks ----------
get_focal <- function(junction, tag) {
  source_data %>% filter(.data$junction == .env$junction, .data$tag_form == .env$tag)
}
cal_155 <- get_focal("155|156", "G196_minimal")
stopifnot(nrow(cal_155) == 1L)
stopifnot(abs(cal_155$delta_mean_pll - 0.00719) < 0.0006)
stopifnot(abs(cal_155$within_tag_percentile - 0.947) < 0.015)

cal_248 <- source_data %>% filter(junction == "248|249") %>% arrange(match(tag_form, tag_order))
stopifnot(max(abs(cal_248$within_tag_percentile - c(0.740, 0.639, 0.803, 0.404))) < 0.025)
cal_256 <- source_data %>% filter(junction == "256|257")
stopifnot(abs(cal_256$within_tag_percentile[cal_256$tag_form == "HA"] - 0.947) < 0.025)
cal_289 <- source_data %>% filter(junction == "289|290") %>% arrange(match(tag_form, tag_order))
stopifnot(max(abs(cal_289$within_tag_percentile - c(0.542, 0.473, 0.448, 0.730))) < 0.025)

expected_focal_constructs <- c(
  "A89_2C_289_290_MAP8", "A89_2C_289_290_G196_minimal",
  "A89_2C_248_249_HA", "A89_2C_248_249_MAP8",
  "A89_2C_224_225_MAP8", "A89_2C_155_156_MAP8"
)
stopifnot(all(expected_focal_constructs %in% final_panel$construct_id))

# ---------- Figure contract ----------
# Core conclusion: Tag-specific PLM scoring reveals site x tag heterogeneity,
# supporting separate treatment of insertion position and tag identity; PLM is
# secondary evidence and cannot override direct phenotype or hard constraints.
# Archetype: asymmetric mixed-modality figure with panel b as the hero panel.
# Final size: 183 x 170 mm; editable SVG/PDF plus 600 dpi PNG.

palette <- c(
  ink = "#222222",
  muted = "#6E7478",
  pale_grey = "#F0F1F2",
  warm = "#E57B35",
  warm_muted = "#D98258",
  warm_dark = "#C95D3A",
  teal = "#2A9DB0",
  teal_dark = "#1F7F83",
  teal_pale = "#E5F4F4",
  blue = "#1776C5",
  purple = "#8B35C8",
  purple_pale = "#F1E7FA",
  lilac = "#BE8BE3",
  near_white = "#FCFCFA"
)

tag_palette <- c(
  MAP8 = "#2B8CA8",
  HA = "#56A7B8",
  G196_minimal = "#7566B3",
  G196_practical_GS = "#A282D1"
)
functional_palette <- c(
  EXCLUDE = "#C95D3A",
  HIGH_RISK = "#E58A4A",
  CORE_CAUTION = "#F1C29F",
  other = "#E9ECEE"
)
conservation_palette <- c(
  conserved = "#5D6E7D",
  intermediate = "#A7B2BA",
  variable = "#4DA8B8",
  lineage_indel_supported = "#8D5BC7"
)

theme_nature <- function(base_size = 6.5) {
  theme_classic(base_size = base_size, base_family = "sans") +
    theme(
      axis.line = element_line(linewidth = 0.3, colour = palette[["ink"]]),
      axis.ticks = element_line(linewidth = 0.3, colour = palette[["ink"]]),
      axis.title = element_text(size = base_size, colour = palette[["ink"]]),
      axis.text = element_text(size = base_size - 0.5, colour = palette[["ink"]]),
      legend.title = element_text(size = 5.9),
      legend.text = element_text(size = 5.5),
      legend.key.height = grid::unit(2.5, "mm"),
      plot.title = element_text(size = 7.2, face = "bold", colour = palette[["ink"]]),
      plot.subtitle = element_text(size = 6.0, colour = palette[["muted"]], margin = margin(b = 2)),
      plot.caption = element_text(size = 5.4, colour = palette[["muted"]], hjust = 0),
      panel.grid = element_blank(),
      plot.margin = margin(2, 2, 2, 2)
    )
}
theme_set(theme_nature())

shared_x <- scale_x_continuous(
  limits = c(0.5, 320.5), breaks = major_ticks,
  expand = c(0, 0)
)

# ---------- Panel a: compact PLM design ----------
tag_cards <- expected_tags %>%
  mutate(
    display = c("MAP8", "HA", "G196 minimal", "G196 practical + GS"),
    y = c(4.5, 3.5, 2.5, 1.5),
    colour = unname(tag_palette[tag_form])
  )

p_a <- ggplot() +
  annotate("rect", xmin = 0.15, xmax = 2.05, ymin = 5.65, ymax = 6.55,
           fill = palette[["teal_pale"]], colour = palette[["teal"]], linewidth = 0.5) +
  annotate("text", x = 1.10, y = 6.10, label = "HRV-A89 2C\n321 aa", size = 2.25,
           fontface = "bold", colour = palette[["ink"]]) +
  annotate("segment", x = 1.10, xend = 1.10, y = 5.60, yend = 5.20,
           arrow = arrow(length = grid::unit(1.6, "mm")), linewidth = 0.4) +
  annotate("text", x = 1.10, y = 4.95, label = "320 internal junctions", size = 2.1) +
  annotate("text", x = 2.45, y = 3.00, label = "×", size = 3.4, fontface = "bold") +
  geom_rect(
    data = tag_cards,
    aes(xmin = 2.85, xmax = 5.90, ymin = y - 0.38, ymax = y + 0.38, colour = colour),
    fill = "white", linewidth = 0.55, show.legend = FALSE
  ) +
  geom_text(
    data = tag_cards,
    aes(x = 3.02, y = y + 0.12, label = display),
    hjust = 0, size = 2.15, fontface = "bold"
  ) +
  geom_text(
    data = tag_cards,
    aes(x = 3.02, y = y - 0.15, label = paste0(tag_sequence, "  ·  ", tag_length, " aa")),
    hjust = 0, size = 1.85, family = "mono", colour = palette[["muted"]]
  ) +
  scale_colour_identity() +
  annotate("segment", x = 6.10, xend = 6.10, y = 4.95, yend = 1.05,
           colour = palette[["purple"]], linewidth = 0.6) +
  annotate("segment", x = 6.10, xend = 6.75, y = 3.00, yend = 3.00,
           arrow = arrow(length = grid::unit(1.7, "mm")), linewidth = 0.45) +
  annotate("rect", xmin = 6.80, xmax = 9.65, ymin = 2.20, ymax = 3.80,
           fill = palette[["purple_pale"]], colour = palette[["purple"]], linewidth = 0.55) +
  annotate("text", x = 8.22, y = 3.25, label = "1,280 ESM2 evaluations",
           size = 2.25, fontface = "bold") +
  annotate("text", x = 8.22, y = 2.83, label = "esm2_t6_8M_UR50D", size = 1.9,
           colour = palette[["purple"]]) +
  annotate("text", x = 8.22, y = 2.43,
            label = "full-sequence masked\npseudo-log-likelihood", size = 1.75,
           colour = palette[["muted"]]) +
  coord_cartesian(xlim = c(0, 10), ylim = c(0.75, 6.75), clip = "off") +
  labs(title = "PLM design and tag architectures") +
  theme_void(base_family = "sans") +
  theme(
    plot.title = element_text(size = 7.2, face = "bold", margin = margin(b = 3)),
    plot.margin = margin(3, 4, 3, 3)
  )

# ---------- Panel b: hero landscape ----------
meta_320 <- junction_meta %>%
  mutate(
    functional_group = if_else(functional_tier %in% c("EXCLUDE", "HIGH_RISK", "CORE_CAUTION"),
                               functional_tier, "other"),
    strict_group = if_else(strict_structural_pass, "strict pass", "not strict pass")
  )

p_key <- ggplot() +
  annotate("text", x = 0.0, y = 2.55, label = "Functional tier", hjust = 0,
           size = 1.85, fontface = "bold") +
  annotate("rect", xmin = c(7.00, 11.50, 16.20, 22.50), xmax = c(7.42, 11.92, 16.62, 22.92),
           ymin = 2.30, ymax = 2.72, fill = unname(functional_palette), colour = NA) +
  annotate("text", x = c(7.55, 12.05, 16.75, 23.05), y = 2.51,
           label = c("EXCLUDE", "HIGH_RISK", "CORE_CAUTION", "other"),
           hjust = 0, size = 1.60) +
  annotate("text", x = 0.0, y = 1.55, label = "Conservation", hjust = 0,
           size = 1.85, fontface = "bold") +
  annotate("rect", xmin = c(7.00, 11.80, 17.20, 21.50), xmax = c(7.42, 12.22, 17.62, 21.92),
           ymin = 1.30, ymax = 1.72, fill = unname(conservation_palette), colour = NA) +
  annotate("text", x = c(7.55, 12.35, 17.75, 22.05), y = 1.51,
           label = c("conserved", "intermediate", "variable", "lineage-indel"),
           hjust = 0, size = 1.60) +
  annotate("text", x = 0.0, y = 0.55, label = "Structure", hjust = 0,
           size = 1.85, fontface = "bold") +
  annotate("rect", xmin = 7.00, xmax = 7.42, ymin = 0.30, ymax = 0.72,
           fill = palette[["teal_dark"]], colour = NA) +
  annotate("text", x = 7.55, y = 0.51, label = "strict structural pass", hjust = 0, size = 1.60) +
  coord_cartesian(xlim = c(0, 29), ylim = c(0, 3), clip = "off") +
  theme_void()

p_func <- ggplot(meta_320, aes(left_resid, 1, fill = functional_group)) +
  geom_tile(width = 1, height = 0.85) +
  shared_x +
  scale_fill_manual(values = functional_palette, drop = FALSE) +
  labs(y = "Function") +
  theme_void() +
  theme(axis.title.y = element_text(size = 5.4, angle = 0, hjust = 1), legend.position = "none")

p_struct <- ggplot(meta_320, aes(left_resid, 1, fill = strict_group)) +
  geom_tile(width = 1, height = 0.85) +
  shared_x +
  scale_fill_manual(values = c("strict pass" = palette[["teal_dark"]],
                               "not strict pass" = "#E9EEEF"), drop = FALSE) +
  labs(y = "Structure") +
  theme_void() +
  theme(axis.title.y = element_text(size = 5.4, angle = 0, hjust = 1), legend.position = "none")

p_cons <- ggplot(meta_320, aes(left_resid, 1, fill = conservation_class)) +
  geom_tile(width = 1, height = 0.85) +
  shared_x +
  scale_fill_manual(values = conservation_palette, drop = FALSE, na.value = "#E9ECEE") +
  labs(y = "Evolution") +
  theme_void() +
  theme(axis.title.y = element_text(size = 5.4, angle = 0, hjust = 1), legend.position = "none")

heat_df <- source_data %>%
  mutate(tag_plot = factor(tag_form, levels = rev(tag_order)))

p_heat <- ggplot(heat_df, aes(left_resid, tag_plot, fill = delta_mean_pll)) +
  geom_tile(width = 1, height = 0.92) +
  annotate("rect", xmin = 286.5, xmax = 291.5, ymin = -Inf, ymax = Inf,
           fill = palette[["teal"]], alpha = 0.08, colour = palette[["teal_dark"]], linewidth = 0.25) +
  geom_vline(xintercept = focal_left, colour = "#343434", linewidth = 0.18, alpha = 0.32) +
  shared_x +
  scale_fill_gradient2(
    low = palette[["warm_muted"]], mid = palette[["near_white"]], high = palette[["teal"]],
    midpoint = 0, limits = visual_limits, oob = squish,
    name = "Δ mean PLL\n(insert − WT)",
    guide = guide_colourbar(barwidth = grid::unit(23, "mm"), barheight = grid::unit(2.7, "mm"),
                            title.position = "top", title.hjust = 0.5)
  ) +
  labs(x = NULL, y = NULL) +
  theme_nature() +
  theme(
    axis.line = element_blank(), axis.ticks = element_blank(),
    axis.text.x = element_blank(),
    axis.text.y = element_text(size = 5.7, colour = palette[["ink"]]),
    legend.position = "bottom",
    plot.margin = margin(1, 2, 0, 2)
  )

p_spread <- ggplot(tag_spread, aes(left_resid, across_tag_spread)) +
  annotate("rect", xmin = 286.5, xmax = 291.5, ymin = -Inf, ymax = Inf,
           fill = palette[["teal_pale"]], colour = NA) +
  geom_area(fill = palette[["purple_pale"]], colour = NA) +
  geom_line(colour = palette[["purple"]], linewidth = 0.35) +
  geom_vline(xintercept = focal_left, colour = "#343434", linewidth = 0.18, alpha = 0.30) +
  shared_x +
  scale_y_continuous(expand = expansion(mult = c(0, 0.08)), breaks = pretty_breaks(2)) +
  labs(x = "A89 insertion junction (left residue)", y = "Across-tag\nPLM spread") +
  theme_nature() +
  theme(
    axis.title.y = element_text(size = 5.4), axis.text.y = element_text(size = 5.1),
    plot.margin = margin(0, 2, 2, 2)
  )

p_b_core <- (p_key / p_func / p_struct / p_cons / p_heat / p_spread) +
  plot_layout(heights = c(1.00, 0.34, 0.34, 0.34, 3.15, 1.05)) +
  plot_annotation(
    title = "Global 4 × 320 tag-specific PLM landscape",
    subtitle = "1,280 evaluations reveal site × tag heterogeneity",
    theme = theme(
      plot.title = element_text(size = 7.2, face = "bold", margin = margin(l = 5)),
      plot.subtitle = element_text(size = 6.0, colour = palette[["purple"]], margin = margin(l = 5))
    )
  )
p_b <- wrap_elements(full = p_b_core)

# ---------- Panel c: per-tag distributions ----------
summary_by_tag <- source_data %>%
  group_by(tag_form) %>%
  summarise(median_delta = median(delta_mean_pll), .groups = "drop") %>%
  mutate(tag_form = factor(tag_form, levels = tag_order))

p_c <- ggplot(source_data %>% mutate(tag_form = factor(tag_form, levels = tag_order)),
              aes(tag_form, delta_mean_pll, fill = tag_form)) +
  geom_hline(yintercept = 0, linetype = "dashed", linewidth = 0.3, colour = palette[["muted"]]) +
  geom_violin(width = 0.82, linewidth = 0.3, colour = "white", alpha = 0.82, trim = TRUE) +
  geom_boxplot(width = 0.16, outlier.shape = NA, linewidth = 0.32,
               fill = "white", colour = palette[["ink"]]) +
  geom_point(data = summary_by_tag, aes(y = median_delta), shape = 21, size = 1.7,
             stroke = 0.3, fill = "white", colour = palette[["ink"]]) +
  scale_fill_manual(values = tag_palette) +
  scale_x_discrete(labels = c("MAP8", "HA", "G196\nminimal", "G196 + GS")) +
  labs(
    title = "Per-tag Δmean-PLL distributions",
    x = NULL, y = "Δ mean PLL (insert − WT)",
    caption = "Tag architectures shift score distributions; site ranking is therefore also considered within each tag."
  ) +
  theme_nature() +
  theme(
    legend.position = "none",
    axis.text.x = element_text(size = 5.5),
    plot.caption = element_text(size = 5.1, lineheight = 0.95),
    plot.margin = margin(3, 4, 3, 3)
  )

# ---------- Panel d: focal site x tag evidence matrix ----------
focal_labels <- c(
  "155|156" = "155|156 †",
  "203|204" = "203|204",
  "224|225" = "224|225",
  "248|249" = "248|249 ‡",
  "256|257" = "256|257 §",
  "287|288" = "287|288",
  "288|289" = "288|289",
  "289|290" = "289|290 ¶",
  "290|291" = "290|291"
)

focal_df <- source_data %>%
  filter(junction %in% focal_junctions) %>%
  mutate(
    junction_plot = factor(junction, levels = rev(focal_junctions)),
    tag_plot = factor(tag_form, levels = tag_order),
    percentile_label = paste0(round(100 * within_tag_percentile), "%"),
    text_colour = if_else(
      delta_mean_pll < visual_limits[1] * 0.72 | delta_mean_pll > visual_limits[2] * 0.72,
      "white", palette[["ink"]]
    )
  )

p_d_heat <- ggplot(focal_df, aes(tag_plot, junction_plot, fill = delta_mean_pll)) +
  geom_tile(colour = "white", linewidth = 0.35) +
  geom_text(aes(label = percentile_label, colour = text_colour), size = 1.85, fontface = "bold") +
  scale_colour_identity() +
  scale_fill_gradient2(
    low = palette[["warm_muted"]], mid = palette[["near_white"]], high = palette[["teal"]],
    midpoint = 0, limits = visual_limits, oob = squish, guide = "none"
  ) +
  scale_x_discrete(labels = c("MAP8", "HA", "G196\nmin.", "G196 + GS"), position = "top") +
  scale_y_discrete(labels = focal_labels) +
  labs(
    title = "Focal site × tag evidence matrix",
    subtitle = "Cell text = within-tag percentile; fill = absolute Δ mean PLL",
    caption = paste(
      "† high PLM rank does not rescue a functional negative.",
      "‡ same junction, tag-dependent compatibility.",
      "§ PLM-favourable but biology-conflicted.  ¶ moderate/tag-dependent, not a universal top site.",
      sep = "\n"
    ),
    x = NULL, y = NULL
  ) +
  theme_minimal(base_size = 6.1, base_family = "sans") +
  theme(
    panel.grid = element_blank(),
    plot.title = element_text(size = 7.0, face = "bold", margin = margin(b = 1)),
    plot.subtitle = element_text(size = 5.2, colour = palette[["muted"]], margin = margin(b = 2)),
    plot.caption = element_text(size = 5.0, colour = palette[["purple"]], hjust = 0,
                                lineheight = 0.95, margin = margin(t = 2)),
    axis.text.x = element_text(size = 5.0, colour = palette[["ink"]]),
    axis.text.y = element_text(size = 5.2, colour = palette[["ink"]]),
    axis.ticks = element_blank(),
    plot.margin = margin(2, 1, 2, 2)
  )

focal_meta <- source_data %>%
  filter(junction %in% focal_junctions) %>%
  distinct(junction, functional_tier, strict_structural_pass, structural_track,
           conservation_class, evA71_direct_insertion_score, evA71_direct_insertion_class) %>%
  mutate(
    junction_plot = factor(junction, levels = rev(focal_junctions)),
    functional_group = if_else(functional_tier %in% names(functional_palette)[1:3],
                               functional_tier, "other"),
    strict_group = if_else(strict_structural_pass, "strict pass", "not strict pass")
  )

annotation_theme <- theme_void(base_family = "sans") +
  theme(
    plot.title = element_text(size = 5.3, face = "bold", hjust = 0.5, margin = margin(b = 2)),
    plot.margin = margin(2, 0.5, 2, 0.5),
    legend.position = "none"
  )

p_d_func <- ggplot(focal_meta, aes(1, junction_plot, fill = functional_group)) +
  geom_tile(colour = "white", linewidth = 0.35) +
  scale_fill_manual(values = functional_palette, drop = FALSE) +
  labs(title = "F") + annotation_theme

p_d_struct <- ggplot(focal_meta, aes(1, junction_plot, fill = strict_group)) +
  geom_tile(colour = "white", linewidth = 0.35) +
  scale_fill_manual(values = c("strict pass" = palette[["teal_dark"]],
                               "not strict pass" = "#E9EEEF"), drop = FALSE) +
  labs(title = "S") + annotation_theme

p_d_cons <- ggplot(focal_meta, aes(1, junction_plot, fill = conservation_class)) +
  geom_tile(colour = "white", linewidth = 0.35) +
  scale_fill_manual(values = conservation_palette, drop = FALSE, na.value = "#E9ECEE") +
  labs(title = "Evo") + annotation_theme

ev_limits <- range(focal_meta$evA71_direct_insertion_score, na.rm = TRUE)
p_d_ev <- ggplot(focal_meta, aes(1, junction_plot, fill = evA71_direct_insertion_score)) +
  geom_tile(colour = "white", linewidth = 0.35) +
  geom_text(aes(label = sprintf("%.1f", evA71_direct_insertion_score)), size = 1.45,
            colour = "white", fontface = "bold") +
  scale_fill_gradient(low = "#F1C7A8", high = palette[["warm_dark"]], limits = ev_limits,
                      guide = "none") +
  labs(title = "EV-A") + annotation_theme

p_d_core <- (p_d_heat | p_d_func | p_d_struct | p_d_cons | p_d_ev) +
  plot_layout(widths = c(6.0, 0.62, 0.62, 0.62, 1.00)) +
  plot_annotation()
p_d <- wrap_elements(full = p_d_core)

# Panel b occupies the dominant upper-right area (~55% of the full canvas).
figure <- (p_a | p_b) / (p_c | p_d) +
  plot_layout(widths = c(0.16, 0.84), heights = c(0.66, 0.34)) +
  plot_annotation(
    tag_levels = "a",
    theme = theme(
      plot.tag = element_text(size = 8, face = "bold", colour = palette[["ink"]]),
      plot.tag.position = c(0.004, 0.995)
    )
  )

width_mm = 183
height_mm = 170
base_name <- file.path(out_dir, "Figure04_tag_specific_PLM_landscape")

svg_path <- paste0(base_name, ".svg")
pdf_path <- paste0(base_name, ".pdf")
png_path <- paste0(base_name, "_600dpi.png")

if (requireNamespace("svglite", quietly = TRUE)) {
  svg_device <- "svglite"
  svglite::svglite(svg_path, width = width_mm / 25.4, height = height_mm / 25.4, bg = "white")
} else {
  stopifnot(capabilities("cairo"))
  svg_device <- "grDevices::svg (Cairo fallback)"
  grDevices::svg(svg_path, width = width_mm / 25.4, height = height_mm / 25.4,
                 family = "sans", bg = "white", onefile = TRUE)
}
print(figure)
dev.off()

cairo_pdf(pdf_path, width = width_mm / 25.4, height = height_mm / 25.4,
          family = "sans", bg = "white", onefile = TRUE)
print(figure)
dev.off()

if (requireNamespace("ragg", quietly = TRUE)) {
  png_device <- "ragg::agg_png"
  ragg::agg_png(png_path, width = width_mm / 25.4, height = height_mm / 25.4,
                units = "in", res = 600, background = "white")
} else {
  stopifnot(capabilities("cairo"))
  png_device <- "grDevices::png (Cairo fallback)"
  grDevices::png(png_path, width = width_mm / 25.4, height = height_mm / 25.4,
                 units = "in", res = 600, type = "cairo-png", bg = "white")
}
print(figure)
dev.off()

for (path in c(svg_path, pdf_path, png_path, source_path)) {
  stopifnot(file.exists(path), file.info(path)$size > 1000)
}

# ---------- QC output ----------
tag_stats <- source_data %>%
  group_by(tag_form) %>%
  summarise(
    n = n(),
    min = min(delta_mean_pll),
    median = median(delta_mean_pll),
    max = max(delta_mean_pll),
    .groups = "drop"
  )

qc <- bind_rows(
  tibble(section = "global", item = c(
    "total_plm_rows", "unique_junctions", "unique_tags", "missing_required_source_values",
    "duplicated_site_tag_rows", "color_limit_2nd_percentile", "color_limit_98th_percentile",
    "figure_width_mm", "figure_height_mm", "main_metric", "color_midpoint",
    "rows_plotted", "junction_order", "first_junction", "last_junction"
  ), value = as.character(c(
    nrow(plm), n_distinct(plm$a89_junction), n_distinct(plm$tag_form),
    sum(is.na(source_data[c("junction", "left_resid", "tag_form", "delta_mean_pll",
                             "functional_tier", "strict_structural_pass", "conservation_class",
                             "evA71_direct_insertion_class", "across_tag_spread")])),
    sum(duplicated(plm[c("a89_junction", "tag_form")])), visual_limits[1], visual_limits[2],
    width_mm, height_mm, "plm_delta_mean_pll_insert_minus_wt", 0, nrow(source_data),
    "left_residue_1_to_320_unclustered", "1|2", "320|321"
  )), status = "pass"),
  tag_stats %>% transmute(
    section = "per_tag",
    item = paste0(tag_form, ":n_min_median_max"),
    value = paste(n, signif(min, 8), signif(median, 8), signif(max, 8), sep = ";"),
    status = if_else(n == 320L, "pass", "fail")
  ),
  observed_tags %>% transmute(
    section = "tag_identity", item = tag_form,
    value = paste(tag_sequence, tag_length, sep = ";"), status = "pass"
  ),
  source_data %>%
    filter(junction %in% focal_junctions) %>%
    transmute(
      section = "focal_values",
      item = paste(junction, tag_form, sep = " x "),
      value = paste0("delta=", signif(delta_mean_pll, 8),
                     ";percentile=", signif(within_tag_percentile, 8),
                     ";functional=", functional_tier,
                     ";strict=", strict_structural_pass,
                     ";conservation=", conservation_class,
                     ";EV_A71=", evA71_direct_insertion_class),
      status = "pass"
    ),
  tibble(
    section = "scientific_calibration",
    item = c(
      "155|156_G196_minimal_high_rank_preserved",
      "248|249_tag_disagreement_preserved",
      "256|257_biology_conflict_preserved",
      "289|290_not_universally_top",
      "no_arbitrary_tolerance_threshold",
      "PLM_secondary_evidence_statement"
    ),
    value = c(
      "delta approximately +0.00719; within-tag percentile approximately 94.7%",
      paste0("within-tag percentiles=", paste(round(100 * cal_248$within_tag_percentile, 1), collapse = ";")),
      "PLM-favorable for several tags; structure/oligomer/function context remains conflicted",
      paste0("within-tag percentiles=", paste(round(100 * cal_289$within_tag_percentile, 1), collapse = ";")),
      "none defined",
      "PLM does not override direct phenotype or hard functional constraints"
    ),
    status = "pass"
  ),
  tibble(
    section = "export",
    item = c("svg_editable_vector", "pdf_vector", "png_600dpi", "source_data", "workflow_backend",
             "svg_device", "png_device"),
    value = c(basename(svg_path), basename(pdf_path), basename(png_path), basename(source_path),
              paste0("R ", getRversion()), svg_device, png_device),
    status = "pass"
  )
)

qc_path <- file.path(out_dir, "Figure04_tag_specific_PLM_landscape_qc.tsv")
write_tsv(qc, qc_path, na = "")

# ---------- README and formal caption ----------
median_lines <- paste0(
  "- `", tag_stats$tag_form, "`: median Δmean PLL = `",
  formatC(tag_stats$median, digits = 5, format = "f"), "`",
  collapse = "\n"
)

caption <- paste0(
  "**Figure 4 | Tag-specific PLM scoring reveals site × tag heterogeneity across HRV-A89 2C internal insertion junctions.** ",
  "A total of 1,280 completed evaluations (320 peptide junctions × four tag architectures) were generated with ESM2 `esm2_t6_8M_UR50D` using full-sequence masked pseudo-log-likelihood. ",
  "The global landscape uses the inserted-minus-wild-type mean PLL difference to reduce tag-length bias; the diverging color scale is centered exactly at zero and is visually capped at the 2nd and 98th percentiles, with source values unchanged. ",
  "Within-tag percentiles are shown only in the focal matrix as relative ranks among the 320 positions for the same tag and are not used to compare absolute score distributions between tags. ",
  "The heatmap and across-tag spread demonstrate substantial dependence on both junction and tag identity. ",
  "Notably, the high within-tag PLM rank of 155|156 × G196 minimal does not rescue its hard functional exclusion, whereas 248|249 displays marked tag-dependent compatibility. ",
  "PLM is therefore treated as a secondary computational evidence layer and does not constitute experimental tolerance, biological validation, or a basis for overriding direct homolog insertion phenotype or hard functional constraints."
)

readme <- c(
  "# Figure 4 — Tag-specific PLM landscape",
  "",
  "## Scientific conclusion",
  "",
  "Tag-specific PLM scoring reveals site × tag heterogeneity, supporting the decision to model tag identity and insertion position as separate variables. PLM remains secondary computational evidence and cannot override direct phenotype or hard biological constraints.",
  "",
  "## Figure contract",
  "",
  "- Archetype: asymmetric mixed-modality composite with Panel b as the hero evidence panel.",
  "- Backend: R (`ggplot2`, `patchwork`, `svglite`, `ragg`).",
  paste0("- Final dimensions: ", width_mm, " × ", height_mm, " mm."),
  "- Primary metric: `plm_delta_mean_pll_insert_minus_wt`.",
  "- Color midpoint: exactly 0.",
  paste0("- Visual color limits: 2nd percentile = `", signif(visual_limits[1], 7),
         "`; 98th percentile = `", signif(visual_limits[2], 7), "`."),
  "- The color scale is visually capped with `scales::squish`; source values are unchanged.",
  "- No PLM tolerance/favorable threshold is defined.",
  "",
  "## Palette",
  "",
  "The palette adapts the supplied scientific schematic: muted orange for negative/risk emphasis, teal-blue for protein/structural evidence, purple for model/matrix emphasis, near-white at the zero midpoint, and pale grey/lilac support tracks. Saturation was reduced for dense publication-scale data.",
  "",
  "## QC summary",
  "",
  "- 1,280/1,280 completed rows plotted.",
  "- 320 unique ordered junctions (`1|2` through `320|321`).",
  "- Four tags × 320 rows each; sequences and lengths verified against the input table.",
  "- No duplicated site × tag rows.",
  "- All annotation joins resolved.",
  "",
  "Per-tag distributions:",
  "",
  median_lines,
  "",
  "`G196_minimal` has a less-negative median distribution, but this is not interpreted as universal superiority. Site ranking is also considered within each tag.",
  "",
  "## Calibration examples",
  "",
  "- `155|156 × G196_minimal`: high PLM rank does not rescue a hard functional negative.",
  "- `248|249`: the same site shows substantially different compatibility across tag architectures.",
  "- `256|257`: PLM-favorable for several tags, but biology remains conflicted.",
  "- `289|290`: moderate and tag-dependent PLM support; it is not a universal top PLM site.",
  "",
  "## Formal caption",
  "",
  caption,
  "",
  "## Reproduction",
  "",
  "Run from the repository root:",
  "",
  "```bash",
  "Rscript scripts/plot_figure04_tag_specific_PLM_landscape.R",
  "```",
  "",
  "Generated files:",
  "",
  "- `Figure04_tag_specific_PLM_landscape.svg`",
  "- `Figure04_tag_specific_PLM_landscape.pdf`",
  "- `Figure04_tag_specific_PLM_landscape_600dpi.png`",
  "- `Figure04_tag_specific_PLM_landscape_source_data.tsv`",
  "- `Figure04_tag_specific_PLM_landscape_qc.tsv`",
  "",
  "## Boundary",
  "",
  "This figure does not generate a composite score, define a safe insertion site, or provide experimental validation."
)
writeLines(readme, file.path(out_dir, "README.md"), useBytes = TRUE)

message("Figure 4 completed: ", out_dir)
