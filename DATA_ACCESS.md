# Data access and redistribution boundaries

## Access classification

| Material | Access route | Included here |
|---|---|---|
| Supplementary Tables S1-S28 | Within repository | Yes |
| Figures 1-14 | Within repository | Yes |
| Aggregate MR-PRESSO and covariance-sensitivity outputs | Within repository | Yes |
| Analysis and audit scripts | Within repository | Yes |
| Public GWAS source metadata and identifiers | Reused public source | Yes |
| Raw GWAS summary statistics | Provider repositories | No |
| Harmonized SNP-level exposure-outcome inputs | Derived from third-party data; redistribution not assumed | No |
| Participant-level data | Controlled by source cohorts | No |
| Sex-specific FinnGen outcome summary statistics | Provider-controlled; not available in the audited environment | No |

## Primary GWAS resources

The source identifiers used by the manuscript are recorded in `supplementary/Supplementary_Table_S1_GWAS_metadata_and_endpoint_hierarchy.csv`. Key identifiers include:

- BMI exposure: OpenGWAS `ieu-b-40` (GIANT).
- Smoking initiation exposure: OpenGWAS `ieu-b-4877` (GSCAN).
- Intervertebral disc disorders: OpenGWAS `finn-b-M13_INTERVERTEB` (FinnGen).
- Spinal stenosis: OpenGWAS `finn-b-M13_SPINSTENOSIS` (FinnGen).
- Low back pain: OpenGWAS `finn-b-M13_LOWBACKPAIN` (FinnGen).
- Sciatica with lumbago: OpenGWAS `finn-b-M13_SCIATICA` (FinnGen).
- Lower back pain and/or sciatica: OpenGWAS `finn-b-M13_LOWBACKPAINORANDSCIATICA` (FinnGen).
- Chronic back pain sensitivity outcome: OpenGWAS `ukb-b-8463` (UK Biobank/MRC-IEU).
- Coronary artery disease comparison outcome: OpenGWAS `ieu-a-7` (CARDIoGRAMplusC4D).

OpenGWAS access: https://gwas.mrcieu.ac.uk/

FinnGen data and documentation: https://www.finngen.fi/en/access_results

Researchers must review the current provider terms, release documentation, ancestry, genome build, phenotype definition, sample counts, covariates, and allowed redistribution before downloading or using any source dataset.

## Restricted inputs

The independent MR-PRESSO rerun used four harmonized SNP-level inputs. The public S25 table retains pair identifiers, row counts, simulation settings, and SHA-256 checksums, but replaces local paths with explicit restricted-data markers. Checksums support author-side provenance verification without distributing the inputs.

The exact MVMR SNP-exposure error covariance and exact pair-specific participant intersections were not available from public marginal beta/standard-error files. The repository therefore includes a prespecified covariance stress test and an identifiability statement, not an exact-covariance or measured-overlap claim.

## Ready-to-paste Data Availability statement

GWAS summary data were obtained from the original consortia and the MRC Integrative Epidemiology Unit OpenGWAS platform using the identifiers listed in Supplementary Table S1. FinnGen endpoint definitions and access information are available from FinnGen. Public, aggregate study outputs, supplementary tables, figures, reporting materials, and analysis scripts are available at https://github.com/wanghanji123/degenerative-spine-risk-factors-mr. Raw and harmonized SNP-level summary-statistic files are not redistributed because they remain subject to the terms of the original data providers; qualified researchers should obtain them directly from the cited resources and reproduce harmonization using the documented identifiers and scripts. No participant-level data were accessed. Matched sex-specific FinnGen outcome summary statistics, exact SNP-exposure covariance, and exact pair-specific participant-overlap counts were unavailable, as detailed in Supplementary Table S28.

## Ready-to-paste Code Availability statement

Analysis, audit, and figure-generation scripts, together with version information and aggregate validation outputs, are available at https://github.com/wanghanji123/degenerative-spine-risk-factors-mr under the MIT License. Original repository documentation and eligible aggregate content are available under CC BY 4.0. Third-party data are excluded from these licenses and remain governed by their source terms.

