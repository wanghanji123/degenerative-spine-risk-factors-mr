options(stringsAsFactors = FALSE)

args <- commandArgs(trailingOnly = TRUE)
project_root <- if (length(args) >= 1) args[[1]] else stop("project_root is required")
output_dir <- if (length(args) >= 2) args[[2]] else stop("output_dir is required")
nb_distribution <- if (length(args) >= 3) as.integer(args[[3]]) else 10000L
base_seed <- if (length(args) >= 4) as.integer(args[[4]]) else 20260728L
pair_filter <- if (length(args) >= 5) args[[5]] else ""

project_root <- normalizePath(project_root, winslash = "/", mustWork = TRUE)
dir.create(output_dir, recursive = TRUE, showWarnings = FALSE)
output_dir <- normalizePath(output_dir, winslash = "/", mustWork = TRUE)
raw_input_dir <- file.path(output_dir, "inputs", "original_harmonised")
analysis_input_dir <- file.path(output_dir, "inputs", "analysis_ready")
result_dir <- file.path(output_dir, "results")
log_dir <- file.path(output_dir, "logs")
dir.create(raw_input_dir, recursive = TRUE, showWarnings = FALSE)
dir.create(analysis_input_dir, recursive = TRUE, showWarnings = FALSE)
dir.create(result_dir, recursive = TRUE, showWarnings = FALSE)
dir.create(log_dir, recursive = TRUE, showWarnings = FALSE)

for (pkg in c("MRPRESSO", "digest")) {
  if (!requireNamespace(pkg, quietly = TRUE)) stop("Missing required package: ", pkg)
}

run_pairs <- data.frame(
  pair_id = c("BMI_IVDD", "BMI_STENOSIS", "SMOKING_IVDD", "SMOKING_STENOSIS"),
  exposure = c("BMI", "BMI", "Smoking initiation", "Smoking initiation"),
  run_folder = c("01_bmi", "01_bmi", "02_smoking_initiation", "02_smoking_initiation"),
  outcome = c("Intervertebral disc disorders", "Spinal stenosis",
              "Intervertebral disc disorders", "Spinal stenosis"),
  opengwas_id = c("finn-b-M13_INTERVERTEB", "finn-b-M13_SPINSTENOSIS",
                  "finn-b-M13_INTERVERTEB", "finn-b-M13_SPINSTENOSIS")
)
if (nzchar(pair_filter)) {
  run_pairs <- run_pairs[run_pairs$pair_id %in% strsplit(pair_filter, ",", fixed = TRUE)[[1]], , drop = FALSE]
  if (nrow(run_pairs) == 0) stop("pair_filter did not match a configured pair: ", pair_filter)
}

parse_p <- function(x) {
  if (length(x) == 0 || all(is.na(x))) return(NA_real_)
  suppressWarnings(as.numeric(gsub("^[<>]\\s*", "", as.character(x[[1]]))))
}

extract_p <- function(x) {
  if (is.null(x)) return(NA_real_)
  if (is.data.frame(x)) {
    pcol <- grep("P", names(x), ignore.case = TRUE, value = TRUE)
    if (length(pcol) == 0 || nrow(x) == 0) return(NA_real_)
    return(parse_p(x[[pcol[[1]]]]))
  }
  if (is.list(x)) {
    pcol <- grep("P", names(x), ignore.case = TRUE, value = TRUE)
    if (length(pcol) == 0) return(NA_real_)
    return(parse_p(x[[pcol[[1]]]]))
  }
  parse_p(x)
}

safe_file_copy <- function(source, destination) {
  ok <- file.copy(source, destination, overwrite = TRUE, copy.date = TRUE)
  if (!ok) stop("Failed to archive input: ", source)
}

manifest_rows <- list()
summary_rows <- list()
main_rows <- list()
warning_rows <- list()

for (i in seq_len(nrow(run_pairs))) {
  pair <- run_pairs[i, ]
  clean_id <- gsub("[^A-Za-z0-9_]+", "_", pair$opengwas_id)
  source_path <- file.path(
    project_root, "runs_endpoint_hierarchy", pair$run_folder,
    "data_processed", paste0("harmonised_", clean_id, ".csv")
  )
  if (!file.exists(source_path)) stop("Missing harmonised input: ", source_path)

  archived_path <- file.path(raw_input_dir, paste0(pair$pair_id, "__original_harmonised.csv"))
  safe_file_copy(source_path, archived_path)
  dat_all <- read.csv(source_path, check.names = FALSE)
  original_row <- seq_len(nrow(dat_all))
  keep_flag <- tolower(as.character(dat_all$mr_keep)) %in% c("true", "1")
  required <- c("beta.outcome", "beta.exposure", "se.outcome", "se.exposure")
  if (!all(required %in% names(dat_all))) {
    stop("Required beta/se columns missing from ", source_path)
  }
  finite_flag <- Reduce(`&`, lapply(dat_all[required], function(x) is.finite(suppressWarnings(as.numeric(x)))))
  dat <- dat_all[keep_flag & finite_flag, , drop = FALSE]
  dat$original_row_number <- original_row[keep_flag & finite_flag]
  if (nrow(dat) < 4) stop("Too few retained instruments for ", pair$pair_id)

  ready_path <- file.path(analysis_input_dir, paste0(pair$pair_id, "__mrpresso_analysis_ready.csv"))
  write.csv(dat, ready_path, row.names = FALSE)
  manifest_rows[[length(manifest_rows) + 1]] <- data.frame(
    pair_id = pair$pair_id,
    exposure = pair$exposure,
    outcome = pair$outcome,
    opengwas_id = pair$opengwas_id,
    source_path = normalizePath(source_path, winslash = "/", mustWork = TRUE),
    archived_original_path = normalizePath(archived_path, winslash = "/", mustWork = TRUE),
    analysis_ready_path = normalizePath(ready_path, winslash = "/", mustWork = TRUE),
    source_bytes = file.info(source_path)$size,
    source_sha256 = digest::digest(file = source_path, algo = "sha256", serialize = FALSE),
    archived_sha256 = digest::digest(file = archived_path, algo = "sha256", serialize = FALSE),
    analysis_ready_sha256 = digest::digest(file = ready_path, algo = "sha256", serialize = FALSE),
    rows_original = nrow(dat_all),
    rows_mr_keep = sum(keep_flag),
    rows_analysis_ready = nrow(dat),
    columns_original = ncol(dat_all),
    seed = base_seed + i - 1L,
    nb_distribution = nb_distribution
  )

  set.seed(base_seed + i - 1L)
  captured_warnings <- character()
  result <- withCallingHandlers(
    MRPRESSO::mr_presso(
      BetaOutcome = "beta.outcome",
      BetaExposure = "beta.exposure",
      SdOutcome = "se.outcome",
      SdExposure = "se.exposure",
      OUTLIERtest = TRUE,
      DISTORTIONtest = TRUE,
      data = as.data.frame(dat),
      NbDistribution = nb_distribution,
      SignifThreshold = 0.05
    ),
    warning = function(w) {
      captured_warnings <<- c(captured_warnings, conditionMessage(w))
      invokeRestart("muffleWarning")
    }
  )

  saveRDS(result, file.path(result_dir, paste0(pair$pair_id, "__full_mrpresso_result.rds")))
  global <- result[["MR-PRESSO results"]][["Global Test"]]
  outlier <- result[["MR-PRESSO results"]][["Outlier Test"]]
  distortion <- result[["MR-PRESSO results"]][["Distortion Test"]]
  main <- result[["Main MR results"]]
  outlier_n <- 0L
  if (is.data.frame(outlier) && nrow(outlier) > 0) {
    pcol <- grep("P", names(outlier), ignore.case = TRUE, value = TRUE)
    if (length(pcol) > 0) {
      pvals <- vapply(outlier[[pcol[[1]]]], parse_p, numeric(1))
      outlier_n <- sum(pvals < 0.05, na.rm = TRUE)
    }
  }

  summary_rows[[length(summary_rows) + 1]] <- data.frame(
    pair_id = pair$pair_id,
    exposure = pair$exposure,
    outcome = pair$outcome,
    opengwas_id = pair$opengwas_id,
    status = "ok",
    n_snps = nrow(dat),
    global_p = extract_p(global),
    outlier_n = outlier_n,
    distortion_p = extract_p(distortion),
    seed = base_seed + i - 1L,
    nb_distribution = nb_distribution,
    input_sha256 = digest::digest(file = ready_path, algo = "sha256", serialize = FALSE),
    interpretation = "Auxiliary pleiotropy sensitivity analysis; not primary causal evidence."
  )

  if (is.data.frame(main) && nrow(main) > 0) {
    names(main) <- make.names(names(main), unique = TRUE)
    main$pair_id <- pair$pair_id
    main$exposure_label <- pair$exposure
    main$outcome_label <- pair$outcome
    main$opengwas_id <- pair$opengwas_id
    main$seed <- base_seed + i - 1L
    main$nb_distribution <- nb_distribution
    main_rows[[length(main_rows) + 1]] <- main
  }
  if (length(captured_warnings) > 0) {
    warning_rows[[length(warning_rows) + 1]] <- data.frame(
      pair_id = pair$pair_id,
      warning = unique(captured_warnings)
    )
  }
}

manifest <- do.call(rbind, manifest_rows)
summary_out <- do.call(rbind, summary_rows)
main_out <- if (length(main_rows)) do.call(rbind, main_rows) else data.frame()
warnings_out <- if (length(warning_rows)) do.call(rbind, warning_rows) else data.frame(pair_id = character(), warning = character())

write.csv(manifest, file.path(output_dir, "mrpresso_input_manifest.csv"), row.names = FALSE)
write.csv(summary_out, file.path(result_dir, "mrpresso_independent_rerun_summary.csv"), row.names = FALSE)
write.csv(main_out, file.path(result_dir, "mrpresso_independent_rerun_main_results.csv"), row.names = FALSE)
write.csv(warnings_out, file.path(log_dir, "mrpresso_warnings.csv"), row.names = FALSE)
capture.output(sessionInfo(), file = file.path(log_dir, "sessionInfo.txt"))
capture.output(
  list(
    run_utc = format(Sys.time(), tz = "UTC", usetz = TRUE),
    project_root = project_root,
    output_dir = output_dir,
    nb_distribution = nb_distribution,
    base_seed = base_seed,
    pair_filter = pair_filter,
    MRPRESSO_version = as.character(utils::packageVersion("MRPRESSO")),
    digest_version = as.character(utils::packageVersion("digest"))
  ),
  file = file.path(log_dir, "run_parameters.txt")
)

cat("Independent MR-PRESSO rerun completed for", nrow(summary_out), "pairs.\n")
print(summary_out)
