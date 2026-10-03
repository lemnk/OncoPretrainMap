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
- Four publication figures in PNG and vector PDF
- Computational report
- Full manuscript draft, figure legends, declarations, and AI-use statement
- JCO CCI Resource Report abstract headings; 272 words by repository tokenizer
  (275-word limit)
- Main body (Introduction through Conclusion): 2,890 words by repository
  tokenizer (3,000-word limit; verify with journal submission counter)
- Completed 80-pair human-verification workbook with row-level evidence
- Class-specific confusion matrix and D1-upgrade analysis
- Model-stratified headline results and CPTAC cross-check
- Frozen pre-review v1 and regenerated post-verification v2 artifacts
- Prespecified Campanella et al external transport protocol
- Complete 242-row external benchmark audit with 100% canonical mapping
- Cross-benchmark comparison; no transport rule changes or conflicts
- Frozen 60-row blinded external-review packet
- Completed 60-row blinded external-transport review with row-level evidence,
  original decisions, adjudications, and dated reviewer attestation
- External-review record preserves 58/60 initial blinded inter-rater agreement
  and the subsequent 12-row D2-to-D1 source-semantics correction; concordance
  with the post-audit resolved classification is 46/60 (76.7%; descriptive
  kappa, 0.604) and is not presented as inter-rater reliability
- Post hoc blanket-statement sensitivity: primary 44 D0/198 D1; six-model
  scenario 176 D0/66 D1; including tRes50 198 D0/44 D1
- Review provenance consistently records that the blank blinded packet preceded
  the post-review integrated comparison workbook

## Validation interpretation to retain

- Caleb Yitna Ref completed all 80 rows with 100% agreement.
- Caleb Yitna Ref was blinded to the development classifications during initial
  review and did not use AI.
- Report the stratified confusion matrix and per-class agreement; do not use one
  pooled statistic as if the sample were representative of the full registry.
- The D1-upgrade bound applies to 23 sampled D1 pairs and should not be projected
  directly to the full registry.
- External transport results are 44 D0 and 198 D1. Twelve D1 rows carry an
  explicit source warning that overlap cannot be excluded; none establish D2.

## Required before journal upload

- Version 1.0.0 has been frozen and published as a GitHub release. Mint its
  Zenodo DOI through an authenticated deposit or the GitHub–Zenodo connection,
  then replace the two DOI placeholders in the manuscript.
- Confirm Jackson State University is the author's correct affiliation for this
  work and follow its authorship/publication policies.
- Format references and word count to the selected journal's current article
  type requirements.
- Supply title page, manuscript, figures, tables/supplement, data availability,
  funding statement, conflict-of-interest form, and any required cover letter.

## Optional high-value extension

If the Bareja et al benchmark releases evaluation case or slide identifiers, compare them with
the 6,093 PanCancer40M training-slide identifiers and report D4 results. Their
absence is currently a documented data-availability limitation, not a pipeline
failure.
