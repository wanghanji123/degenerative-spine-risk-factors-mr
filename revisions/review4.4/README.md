# Review 4.4 corrected aggregate results

27 September 2026. This directory supersedes conflicting historical summaries in the repository. It is a numerical correction snapshot, not a claim of publication, completed author approval, or validated causal assumptions. The study is original two-sample MR research, not a review article.

## Corrections that change interpretation

- The four primary IVW associations reproduce. BMI is more consistent than smoking across sensitivity estimators; neither establishes an intervention effect.
- Same-sign I2GX is 91.8% for BMI and 40.2% for smoking. Earlier values based on unoriented exposure effects must not be used.
- Joint-LD-selected MVMR uses 429 exact nonpalindromic variants per outcome. Smoking conditional F is 4.24 at zero covariance and remains below 10 across the assumed-correlation grid. This limits interpretation of both direct effects.
- Saved 500-simulation MR-PRESSO objects contain software flags and corrected estimates. They do not support the old statement of no outliers. Individual flag P values are simulation-limited. These outputs remain auxiliary historical diagnostics.
- All historical MRlap corrections are withdrawn from current inference because input sample-size/provenance and harmonization issues were unresolved. Lack of exact overlap counts alone is not the reason.
- The numerical overlap boundary calculation and the unverified UKB chronic-back-pain odds ratios are withdrawn.
- Minimum detectable ORs use binary-outcome information N*k*(1-k)*R2. Smoking power and mixed-scale directionality are not asserted.
- Alternative body-fat identifiers with identical retained numerical inputs are not independent replications. FinnGen diagnoses are not uniformly imaging-confirmed degeneration. No prospective preregistration, measured zero overlap, or sex-specific MR estimate is claimed.

## Reproduce the public outputs

From this directory, Python 3.11 or newer:

```text
python scripts/verify_public_revision.py
python -m pip install -r requirements-figures.txt
python scripts/build_figures.py
```

The first command checks stored file hashes and aggregate numerical consistency using only the standard library. Run it before regenerating figures, whose PDF timestamps may change file hashes. The figure builder uses the included S3/S10 tables and two aggregate MVMR files; it needs no network, tokens, or other projects. It recreates four figures, not the underlying MR fits.

Python and independent base-R checks agree on the repaired MVMR estimates. The 76 conditional-F scenario values also agree with independent R regressions. Runtime records distinguish this repair environment from the historical analyses. Shared assumptions or source-data errors can remain even when implementations agree.

## Scope of sharing

This is an aggregate-only subset, not the complete S1-S28 supplement. Included tables retain their manuscript numbering. Full private repair scripts and input manifests accompany the author handover. Original harmonized SNP associations and complete GWAS inputs must be obtained through their providers under applicable terms before rerunning the source analysis. No reference genotypes, participant identifiers, credentials, full-text article copies, or restricted source files are included here. Derived rsID software-flag summaries in S7-S8 are audit records, not participant-level data or a redistributed GWAS.

Historical files outside this revision directory remain for provenance. They must not be mixed with the new figures, denominators, diagnostics or conclusions. In particular, the older AI-assisted illustrations are not used in the revised quantitative figures.

## License and citation

Repository owner: wanghanji123. Code uses the repository MIT license; original aggregate outputs and figures use the repository CC BY 4.0 terms to the extent the owner holds the relevant rights. Third-party material is not relicensed. The root CITATION.cff lacks a verified final author list and must not be treated as manuscript authorship. Cite the correction release or immutable commit actually used, not an invented DOI. Author-level ethics, source-use compliance, funding, conflicts and final submission approval remain outside this numerical package.
