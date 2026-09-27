# Body mass index, smoking liability, and registry-based degenerative spine outcomes

Reproducibility materials for:

> Body mass index, smoking liability, and registry-based degenerative spine outcomes: a sample-overlap-aware Mendelian randomization study

## Overview

**Scientific correction, 27 September 2026:** Use [Review 4.4 corrected aggregate results](revisions/review4.4/README.md) for current interpretation. Historical files outside that directory remain unchanged for provenance and contain superseded values and claims. In particular, do not reuse the old I2GX diagnostics, 530-variant MVMR results, MRlap corrections, sample-overlap boundary calculations, UKB pain odds ratios, or the claim of no MR-PRESSO outliers. This correction is not author approval or a published article.

This repository contains publication-level aggregate results, supplementary tables, figures, reporting materials, and analysis scripts for a two-sample Mendelian randomization (MR) study of body mass index (BMI), smoking-initiation liability, and registry-based degenerative spine outcomes.

The design prioritizes FinnGen intervertebral disc disorders (IVDD) and spinal stenosis as registry-coded diagnoses, not uniform imaging-confirmed degeneration. The endpoint hierarchy was not prospectively registered. Symptom outcomes are contextual, and coronary artery disease is a systemic comparison rather than a negative control. UK Biobank chronic-back-pain quantitative estimates are withdrawn because their effect scale was not validated.

The primary IVW associations reproduce. BMI has more consistent sensitivity support than smoking. Revised joint-selection MVMR uses 429 SNPs per outcome; smoking conditional F of 4.24 limits interpretation of both direct effects. These genetic-liability estimates establish neither independent direct effects nor benefits of weight-loss or smoking-cessation interventions.

## Repository owner

- GitHub owner: [wanghanji123](https://github.com/wanghanji123)
- Repository: [wanghanji123/degenerative-spine-risk-factors-mr](https://github.com/wanghanji123/degenerative-spine-risk-factors-mr)

The manuscript author list was not present in the repository-preparation source document and has therefore not been inferred. Authors should update `CITATION.cff` before the final archival release.

## Contents

- `revisions/review4.4/`: current aggregate-only correction, four quantitative figures, portable figure builder, validation script and environment records. Start here. The folders listed below are historical unless separately updated.

- `supplementary/`: Supplementary Tables S1-S28, index, and integrity manifest.
- `figures/`: Figures 1-14 and the caption inventory used in Review4.0.
- `scripts/`: Portable audit, covariance-sensitivity, figure-generation, and MR-PRESSO rerun scripts.
- `results/`: Aggregate MR-PRESSO and MVMR covariance-sensitivity outputs.
- `reporting/`: STROBE-MR checklist.
- `environment/`: R session information and Python package requirements.
- `docs/`: Data access, reproducibility, limitations, AI/figure provenance, and submission metadata.

## Reproduction

For the current revision, first run `python revisions/review4.4/scripts/verify_public_revision.py`. Recreate its figures with the requirements and command in the revision README. These portable tasks were tested in a separate copied folder; they do not rerun source-SNP analyses.

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

The four Review 4.4 figures are programmatically drawn from audited results and contain no generative-image layers. The following paragraph describes historical figures only, not the current revision.

Figures 5 and 7 contain non-data-bearing illustration layers initially generated with OpenAI GPT Image 2; all labels, arrows, numerical statements, and caveats were added or verified by the authors. No external published figure or table was reproduced. See [docs/AI_USE_AND_FIGURE_PROVENANCE.md](docs/AI_USE_AND_FIGURE_PROVENANCE.md). Authors must apply the selected journal's current AI-image policy before submission and replace these layers when required.

## Citation

Use the metadata in [CITATION.cff](CITATION.cff) to cite this repository. When a journal-ready author list and an archival DOI become available, update the CFF file and create a versioned release.

## Scientific scope

MR-PRESSO is auxiliary and its archived 500-simulation individual-outlier flags are not reliable confirmatory outlier tests. All historical MRlap corrections and the numerical overlap-scenario analysis have been withdrawn from current inference. Exact MVMR exposure-error covariance and participant-overlap counts remain unknown. Matched authorized sex-specific FinnGen outcomes were unavailable, so no sex-stratified causal estimates are reported. The full source-level repair and manuscript review have remaining author-dependent and data-provenance requirements described in the private handover; this repository does not certify submission readiness.
