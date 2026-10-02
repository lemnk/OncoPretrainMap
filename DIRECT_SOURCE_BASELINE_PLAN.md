# Direct-source baseline comparison plan

Date frozen: 2026-10-02

## Question

What classification value does OncoPretrainMap add beyond directly reading the
curated model papers and model cards for exact evaluation-dataset names?

## Baseline

The direct-source baseline uses the same frozen primary-source assertions but
does not traverse dataset lineage.

- D4 only when an exact identifier-overlap record exists for the model–dataset
  pair.
- D3 only when a development assertion names the exact canonical evaluation
  dataset.
- D0 only when a version-specific disjointness assertion names the exact
  canonical evaluation dataset and no stronger exposure evidence conflicts.
- D1 otherwise.

The baseline receives canonical model and evaluation-dataset identifiers. It
therefore isolates the contribution of lineage traversal rather than measuring
human search time, alias discovery, or source-extraction accuracy. It is a
stronger and more reproducible baseline than an informal claim about manually
reading papers.

## Comparisons

1. Compare the baseline with the frozen registry across all 32 models and 28
   evaluation datasets (896 pairs). Report the confusion matrix and every D1 to
   D2–D4 upgrade attributable to lineage.
2. Project the baseline to the published 1,312 Bareja model–task rows using the
   already-frozen model aliases and task-to-dataset mapping. Apply the same
   benchmark-resolution rule used in the manuscript: a TCGA or CPTAC repository
   assertion is D2 at benchmark resolution when exact evaluated-subset
   identifiers are unavailable.
3. Report identical baseline and registry results honestly. Do not claim that
   this analysis measures time saved, source-search completeness, or superiority
   to expert manual review.

## Outcomes

- class counts for baseline and registry;
- exact agreement and class-level confusion matrix;
- number of lineage-added exposure classifications;
- number of benchmark rows whose class changes;
- worked examples with assertion and lineage provenance.

This is a post-protocol resource-utility analysis. It does not validate D4,
estimate contamination, or replace external testing of D2–D4.
