# STROBE-MR Checklist Working File - Review4.0

Date: 2026-08-11

Source: STROBE-MR checklist of recommended items to address in reports of
Mendelian randomization studies [Skrivankova2021STROBEMR].

Status labels:

- Complete: covered in the manuscript or the assembled supplementary package.
- Partial: present but still requires author input, final pagination, or public deposition.
- Not applicable/unavailable: cannot be completed from the authorized summary-data environment and is transparently documented.

| Item | Section | Checklist focus | Current location | Status | Action before submission |
|---|---|---|---|---|---|
| 1 | Title/Abstract | Identify MR design and main exposure/outcome scope | Title and Abstract | Complete | Apply target-journal formatting only |
| 2 | Background | Scientific background, exposure, and rationale for MR | Background | Complete | Final language edit |
| 3 | Background | Clear objectives and causal hypotheses | Final Background paragraph; Methods MR assumptions | Complete | Retain liability-scale wording |
| 4 | Methods | Study design, sources, participants, variants, phenotypes, ethics | Methods; Table 1; Supplementary Tables S1-S2 and S12 | Complete | Confirm declarations wording |
| 5 | Methods | Relevance, independence, and exclusion-restriction assumptions | Methods: MR assumptions | Complete | None |
| 6 | Methods | Variant handling, estimators, missing data, multiplicity | Instrument selection and MR analyses | Complete | None |
| 7 | Methods | Methods/prior knowledge used to assess assumptions | Sensitivity analyses | Complete | None |
| 8 | Methods | Sensitivity/additional analyses | Methods; Supplementary Tables S10-S28 | Complete | None |
| 9 | Methods | Software versions and protocol/pre-registration | Software and reproducibility; Additional file 3 | Partial | Software and rerun versions are documented; retain the explicit statement that the endpoint hierarchy was not preregistered |
| 10 | Results | Descriptive data, sample sizes, overlap, exposure/outcome sources | Tables 1 and 4; Supplementary Tables S1-S2, S12, S17-S18, S28 | Complete | Exact participant intersections were not publicly reported and are labeled non-identifiable |
| 11 | Results | Main MR estimates and uncertainty on interpretable scale | Results; Table 2; Figure 2 | Complete | Target-journal styling only |
| 12 | Results | Assessment of assumptions, heterogeneity, instrument strength | Table 3; Supplementary Tables S4-S5, S14, S21, S25-S27 | Complete | None |
| 13 | Results | Sensitivity/additional analyses and directionality | Results; Supplementary Tables S6-S28 | Complete | Sex-stratified estimates remain unavailable without authorized matched outcomes |
| 14 | Discussion | Key results linked to objectives | Principal findings and novelty | Complete | None |
| 15 | Discussion | Limitations, bias direction/magnitude, imprecision | Limitations; Supplementary Tables S18, S27-S28 | Complete | Preserve non-identifiability and auxiliary-analysis wording |
| 16 | Discussion | Meaning, mechanisms, clinical relevance | Biological and clinical interpretation | Complete | Avoid intervention-effect overclaim |
| 17 | Discussion | Generalizability | Limitations and conclusion | Complete | None |
| 18 | Other | Funding and role of funders | Funding section | Partial | Requires author input |
| 19 | Other | Data/code sharing and access | Data availability; code availability; public repository and restricted author archive | Complete | Public repository v1.0.1 is verified; archival DOI remains optional until final authorship metadata are available |
| 20 | Other | Conflicts of interest | Competing interests | Partial | Requires author confirmation |

## Review3.9 Additions

- Recovered and archived original harmonized SNP-level inputs for all four primary MR-PRESSO pairs.
- Independently reran the primary 500-simulation MR-PRESSO specification with fixed pair-specific seeds and archived full outputs, warnings, checksums, parameters, and `sessionInfo()`.
- Added Supplementary Tables S25-S26 comparing the original, independent, and higher-simulation MR-PRESSO analyses.
- Added a prespecified MVMR covariance-assumption stress test over `rho = -0.90` to `0.90`; BMI conditional F remained above 10 and smoking-initiation conditional F remained below 10 throughout.
- Explicitly distinguished low expected sample overlap from a measured participant-intersection count.
- Explicitly documented that public marginal summary data cannot identify exact pair-specific overlap counts or per-SNP cross-exposure covariance.
- Clarified that male/female GIANT BMI exposure preparation is complete but authorized matched sex-specific FinnGen outcomes are unavailable; no pooled-outcome proxy was substituted.
- Updated Figure 12 to display both MVMR estimates and the conditional-F covariance stress test.

## Review4.0 Additions

- Updated Data Availability and Code Availability to the verified public repository.
- Added a more precise secondary-summary-data ethics statement, subject to submitting-institution confirmation.
- Added a transparent generative-AI disclosure and Figure 5/Figure 7 caption disclosures.
- Added target-journal AI-image-policy review as an explicit submission gate.

## Remaining Submission Tasks

1. Add final page and line numbers after selecting the target journal template.
2. Confirm author list/order, affiliations, ORCID, funding, CRediT contributions, and conflict-of-interest statements.
3. Confirm with the submitting institution whether secondary analysis of non-identifiable public/provider-controlled summary data requires an exemption or formal determination.
4. Apply the selected journal's current AI policy; replace the AI-assisted Figure 5/Figure 7 layers if generative-AI illustrations or graphical abstracts are not permitted.
5. Optionally archive the final public release in Zenodo after authorship metadata are complete.
6. Complete sex-stratified MR only if authorized matched FinnGen male/female outcome files are obtained; this is not required for the current claims.
