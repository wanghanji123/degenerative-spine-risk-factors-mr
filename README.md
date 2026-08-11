# Body mass index, smoking liability, and registry-based degenerative spine outcomes

Reproducibility materials for:

> Body mass index, smoking liability, and registry-based degenerative spine outcomes: a sample-overlap-aware Mendelian randomization study

## Overview

This repository contains publication-level aggregate results, supplementary tables, figures, reporting materials, and analysis scripts for a two-sample Mendelian randomization (MR) study of body mass index (BMI), smoking-initiation liability, and registry-based degenerative spine outcomes.

The design prioritizes FinnGen intervertebral disc disorders (IVDD) and spinal stenosis as structural registry endpoints. Low back pain, sciatica, a broader pain composite, UK Biobank chronic back pain, and coronary artery disease are used as secondary, sensitivity, exploratory, or specificity endpoints according to a prespecified endpoint hierarchy.

The primary findings were directionally consistent positive associations of genetically predicted BMI with IVDD and spinal stenosis. Smoking-initiation liability showed weaker positive evidence and did not retain the same degree of independence or instrument strength in multivariable MR. These genetic-liability estimates are not direct estimates of weight-loss or smoking-cessation interventions.

## Repository owner

- GitHub owner: [wanghanji123](https://github.com/wanghanji123)
- Repository: [wanghanji123/degenerative-spine-risk-factors-mr](https://github.com/wanghanji123/degenerative-spine-risk-factors-mr)

The manuscript author list was not present in the repository-preparation source document and has therefore not been inferred. Authors should update `CITATION.cff` before the final archival release.

## Contents

- `supplementary/`: Supplementary Tables S1-S28, index, and integrity manifest.
- `figures/`: Figures 1-14 and the caption inventory used in Review4.0.
- `scripts/`: Portable audit, covariance-sensitivity, figure-generation, and MR-PRESSO rerun scripts.
- `results/`: Aggregate MR-PRESSO and MVMR covariance-sensitivity outputs.
- `reporting/`: STROBE-MR checklist.
- `environment/`: R session information and Python package requirements.
- `docs/`: Data access, reproducibility, limitations, AI/figure provenance, and submission metadata.

## Reproduction

The analyses that can be reproduced from shareable aggregate inputs are documented in [docs/REPRODUCIBILITY.md](docs/REPRODUCIBILITY.md). The supplementary CSV integrity audit can be run without restricted data:

```bash
python scripts/audit_supplementary_csvs.py
```

MR-PRESSO reruns require locally obtained harmonized SNP-level inputs. Those inputs are not redistributed here. See [DATA_ACCESS.md](DATA_ACCESS.md).

## Data access

This repository does not redistribute raw GWAS summary statistics, harmonized SNP-level exposure-outcome files, FinnGen controlled-access resources, participant-level data, or credentials. It provides GWAS identifiers, source metadata, derived aggregate results, checksums, and retrieval guidance. See [DATA_ACCESS.md](DATA_ACCESS.md).

## Licenses

- Analysis code: [MIT License](LICENSE).
- Original documentation, figures, and aggregate outputs, to the extent the repository owner holds the relevant rights: [CC BY 4.0](LICENSE-CONTENT.md).
- Third-party data and metadata remain governed by their original provider terms and are not relicensed by this repository.

## AI and figure provenance

Figures 5 and 7 contain non-data-bearing illustration layers initially generated with OpenAI GPT Image 2; all labels, arrows, numerical statements, and caveats were added or verified by the authors. No external published figure or table was reproduced. See [docs/AI_USE_AND_FIGURE_PROVENANCE.md](docs/AI_USE_AND_FIGURE_PROVENANCE.md). Authors must apply the selected journal's current AI-image policy before submission and replace these layers when required.

## Citation

Use the metadata in [CITATION.cff](CITATION.cff) to cite this repository. When a journal-ready author list and an archival DOI become available, update the CFF file and create a versioned release.

## Scientific scope

MR-PRESSO was used as an auxiliary sensitivity analysis. The sample-overlap scenario analysis is illustrative rather than a measured pair-specific correction. Exact MVMR SNP-exposure covariance and exact participant-overlap counts were not identifiable from public marginal summary statistics. Matched sex-specific FinnGen outcomes were unavailable, so no sex-stratified causal estimates are reported.
