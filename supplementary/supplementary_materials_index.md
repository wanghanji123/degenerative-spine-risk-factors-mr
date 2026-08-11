# Supplementary Materials Index

Package date: 2026-07-28

Source version: Review3.9

## Final supplementary-table set

- Supplementary Table S1. GWAS metadata and endpoint hierarchy.
- Supplementary Table S2. Endpoint extraction and harmonisation status.
- Supplementary Table S3. Full MR results across available estimators.
- Supplementary Table S4. Heterogeneity results.
- Supplementary Table S5. MR-Egger intercept results.
- Supplementary Table S6. Steiger directionality results.
- Supplementary Table S7. MR-PRESSO global-test summary for the four primary structural pairs.
- Supplementary Table S8. MR-PRESSO main results for the four primary structural pairs.
- Supplementary Table S9. Cigarettes smoked per day IVW sensitivity results.
- Supplementary Table S10. Alternative adiposity and UKB body-composition sensitivity results.
- Supplementary Table S11. Reverse MR from structural FinnGen spine endpoints to BMI and smoking initiation.
- Supplementary Table S12. FinnGen endpoint definitions and ICD code rules.
- Supplementary Table S13. Formal binary-outcome Steiger directionality for the four primary pairs.
- Supplementary Table S14. MR power, MR-Egger NOME/I2GX, and detectable-effect calculations for the four primary pairs.
- Supplementary Table S15. Leave-one-out sensitivity summary for the four primary pairs.
- Supplementary Table S16. BMI plus smoking-initiation MVMR feasibility audit.
- Supplementary Table S16B. Union-SNP extraction template used to prepare formal BMI plus smoking-initiation MVMR.
- Supplementary Table S17. Primary sample-overlap matrix.
- Supplementary Table S18. Sample-overlap weak-instrument bias-boundary scenarios.
- Supplementary Table S19. BMI plus smoking-initiation MVMR primary results.
- Supplementary Table S20. BMI plus smoking-initiation MVMR harmonisation QC and conditional instrument-strength diagnostics.
- Supplementary Table S21. MRlap sensitivity results for the four primary pairs using HM3-plus summary statistics and European LD scores.
- Supplementary Table S22. Sex-stratified MR feasibility audit.
- Supplementary Table S23. GIANT male- and female-specific BMI exposure preparation manifest.
- Supplementary Table S24. FinnGen sex-specific IVDD and spinal-stenosis outcome request checklist.
- Supplementary Table S25. File-level manifest for the independently archived MR-PRESSO harmonized and analysis-ready SNP inputs, including SHA-256 hashes.
- Supplementary Table S26. Comparison of the original 500-simulation MR-PRESSO run, the independent fixed-seed 500-simulation rerun, and the historical 1,000-simulation sensitivity run.
- Supplementary Table S27. BMI plus smoking-initiation MVMR conditional-F stress test across assumed SNP-exposure error correlations from -0.90 to 0.90.
- Supplementary Table S28. Data-access and identifiability constraints for sex-stratified MR, exact MVMR covariance, participant overlap, and MR-PRESSO reproducibility.

## Version decisions and corrections

- S11: the `structural_to_BMI_smoking` file is the final submission version. The older `registry_to_BMI_smoking` file had identical SHA-256 content and was excluded to prevent duplicate numbering.
- S24: the final field in the endpoint-metadata row was enclosed in quotation marks so the row now has the same seven CSV columns as the header.
- S7-S8: MR-PRESSO used 500 simulations and is retained as an auxiliary sensitivity analysis, not primary causal evidence.
- S16B: this is an extraction/input template, not an independent result table.
- S18: bias-boundary scenarios are illustrative and are not a formal sample-overlap correction.
- S20: conditional F statistics use the documented zero SNP-exposure covariance assumption because exact covariance matrices were unavailable.
- S22-S24: these document feasibility and data requirements. They do not constitute completed sex-stratified MR results.
- S21: the original table remains traceable to the 2026-05-14 MRlap summary. A 2026-07-21 rerun with `set.seed(20260721)` reproduced all instrument counts, observed effects, corrected point estimates, and LDSC fields. Parametric-bootstrap SE/P-value differences did not change direction or statistical significance; the observed-versus-corrected difference test remains auxiliary.
- S25-S26: the original harmonized SNP-level files for all four primary pairs were recovered and independently rerun using the primary `NbDistribution = 500` specification and fixed pair-specific seeds 20260728-20260731. All four global tests remained significant and no outlier SNP was detected. Original inputs, analysis-ready inputs, full R objects, warnings, parameters, and `sessionInfo()` are retained in the reproducibility archive.
- S27: the correlation grid is a stress test, not an estimate of the true SNP-exposure covariance. BMI conditional F remained above 10 throughout the grid, whereas smoking-initiation conditional F remained below 10 throughout.
- S28: quantities absent from public summary data are labeled non-identifiable rather than imputed. Low expected exposure-outcome overlap is a design classification, not a measured participant-intersection count.

## Remaining external dependency

Formal sex-stratified MR still requires authorised FinnGen sex-specific IVDD and spinal-stenosis outcome summary statistics. No male- or female-specific causal estimate should be reported until those files are obtained and harmonised with the prepared GIANT exposure data.

Public repository deposition also remains external to this local table set. A credential-audited release candidate is provided under `03_Code_archive`, but a repository URL or DOI must not be reported until the authors approve ownership/licensing metadata and verify a public record.
