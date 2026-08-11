# Reproducibility guide

## 1. Environment

The archived environment used R 4.6.0, MRPRESSO 1.0, digest 0.6.39, and Windows 10. See `environment/R_sessionInfo_MRPRESSO.txt`.

The current Python figure/audit environment is recorded in `environment/requirements.txt`.

## 2. Supplementary-table integrity audit

From the repository root:

```bash
python scripts/audit_supplementary_csvs.py
```

The script checks that all Supplementary Table CSV files have a consistent number of columns and regenerates SHA-256 manifests.

## 3. MVMR covariance-assumption stress test

The input directory must contain:

- `data_processed/mvmr_matrix_finn_b_M13_INTERVERTEB.csv`
- `data_processed/mvmr_matrix_finn_b_M13_SPINSTENOSIS.csv`

These files are not distributed. After obtaining and harmonizing the required source data:

```bash
python scripts/mvmr_covariance_sensitivity.py \
  --mvmr-dir PATH_TO_LOCAL_MVMR_DIRECTORY \
  --output-dir local_results/mvmr_covariance_sensitivity
```

The default grid is `rho=-0.90,-0.75,-0.50,-0.25,0,0.25,0.50,0.75,0.90`. This is a stress test of assumed cross-exposure estimation-error correlation. It does not estimate the true covariance.

## 4. Figure 12

```bash
python scripts/build_figure12_mvmr_covariance.py
```

The script reads Supplementary Table S27 by default and writes the figure to `figures/Figure12_MVMR_covariance_sensitivity.png`.

## 5. Independent MR-PRESSO rerun

Required R packages:

```r
install.packages("digest")
# Install MRPRESSO 1.0 from its authoritative source if it is not already available.
```

The project root supplied to the script must contain the documented `runs_endpoint_hierarchy` structure and locally obtained harmonized inputs:

```bash
Rscript scripts/run_independent_mrpresso_rerun.R \
  PATH_TO_LOCAL_PROJECT_ROOT \
  local_results/mrpresso_nb500 \
  500 \
  20260728
```

Pair-specific seeds increment from the base seed. MR-PRESSO is auxiliary sensitivity evidence; a significant global test does not identify a specific pleiotropic variant, and no detected outlier does not prove absence of horizontal pleiotropy.

## 6. Expected aggregate checks

- MR-PRESSO global P values for BMI-IVDD, BMI-stenosis, smoking-IVDD, and smoking-stenosis: 0.002, 0.002, 0.004, and 0.002.
- No outlier SNP was detected in the four 500-simulation reruns.
- Across the covariance stress-test grid, BMI conditional F: 15.58-285.02.
- Across the covariance stress-test grid, smoking-initiation conditional F: 5.79-8.75.

Compare reruns to the aggregate files in `results/` and the checksums in the supplementary manifest.

