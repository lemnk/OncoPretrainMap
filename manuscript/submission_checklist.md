# Submission Readiness Checklist

## Complete

- Frozen protocol and source repository revision
- Primary-source extraction for all 32 core model labels
- Dataset aliases and lineage graph
- 896-pair exposure registry
- Complete 1,312-row published benchmark audit
- Exact training-manifest feasibility analysis
- Conservative secondary performance analysis
- Executable checker
- Automated tests and cryptographic manifest
- Three publication figures in PNG and vector PDF
- Computational report
- Full manuscript draft, figure legends, declarations, and AI-use statement

## Required before claiming independent validation

- A second human reviewer must complete all 80 rows of
  `data/validation/independent_review_sample_v1.csv` while blinded to the
  development classifications.
- Preserve the returned initial decisions. Calculate exact agreement and
  unweighted Cohen's kappa only after unblinding.
- Resolve disagreements transparently; do not overwrite either reviewer's
  original classification.
- Update the Abstract, Methods, Results, Discussion, and supplement with the
  actual agreement findings, including unfavorable findings.

## Required before journal upload

- Create a public GitHub repository and replace the repository placeholder.
- Mint a versioned Zenodo DOI after the final validation update.
- Confirm Jackson State University is the author's correct affiliation for this
  work and follow its authorship/publication policies.
- Format references and word count to the selected journal's current article
  type requirements.
- Supply title page, manuscript, figures, tables/supplement, data availability,
  funding statement, conflict-of-interest form, and any required cover letter.

## Optional high-value extension

If PathBench releases evaluation case or slide identifiers, compare them with
the 6,093 PanCancer40M training-slide identifiers and report D4 results. Their
absence is currently a documented data-availability limitation, not a pipeline
failure.
