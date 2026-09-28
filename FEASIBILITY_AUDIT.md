# Source and Dataset Feasibility Audit

**Audit date:** 2026-09-27  
**Decision:** Feasible; proceed with a high-ceiling resource and benchmark audit.

## Scientific need

Recent computational-pathology reviews identify pretraining/evaluation overlap
and benchmark contamination as unresolved threats to generalization claims.
The 2026 PathBench study evaluated 32 foundation models across 41 tasks and
explicitly separated TCGA from non-TCGA evaluations because public-repository
exposure cannot always be excluded. A 2025 clinical benchmark similarly noted
that overlap could not be excluded for models and evaluation cohorts drawn from
the same institution.

## Available source universe

The PathBench public repository provides:

- 32 evaluated model labels;
- 41 evaluation tasks;
- 1,312 model–task result rows;
- model-weight and implementation links;
- coarse pretraining corpus names and reported sizes; and
- TCGA, CPTAC, external-benchmark, and out-of-domain task labels.

Repository snapshot:

- URL: https://github.com/gevaertlab/benchmarking-path-models
- Commit: `076ffcef84b7c3359a9ceaeb16e423e567fcd27a`
- Commit date: 2026-05-09

Primary model papers and model cards are publicly accessible for many core
models. Exact case or slide manifests are expected to be uncommon, especially
for proprietary institutional corpora. Missing disclosure is therefore a
measurable result rather than a reason to stop.

## Existing resources and novelty boundary

Public catalogs already list pathology foundation models, architectures,
weights, and high-level pretraining datasets. OncoPretrainMap will not claim
novelty for creating another model list. Its distinct contribution must be:

1. version-specific model records;
2. dataset lineage from repository to cohort, slide subset, and patch derivative;
3. model–dataset exposure classifications with row-level evidence;
4. separate exposure-scope and evidence-strength axes;
5. conservative handling of incomplete disclosure;
6. an executable checker; and
7. a real audit of published benchmark matrices.

## Compute and storage feasibility

Registry construction is metadata-intensive rather than compute-intensive.
No foundation-model training or slide inference is required for the primary
study. The current machine has sufficient storage for metadata, papers,
manifests, and source snapshots. Whole-slide images and model weights are out of
scope unless a small identifier-only manifest is required for exact matching.

## Main risks

- Proprietary training corpora may be incompletely disclosed.
- Model families have multiple checkpoints and changing model cards.
- Dataset aliases can conceal lineage relationships.
- Repository-level exposure does not prove exact slide exposure.
- A registry without independent validation would be vulnerable to reviewer
  criticism.
- A catalog without a benchmark-level use case would have limited novelty.

## Mitigations

- Freeze source versions, retrieval dates, and cryptographic hashes.
- Treat the model version as part of the identifier.
- Preserve quoted evidence separately from normalized assertions.
- Use explicit conflict flags when disjointness claims and exposure evidence
  disagree.
- Conduct blinded duplicate extraction on a prespecified held-out subset.
- Confirm exact exposure only from identifiers or manifests.
- Audit at least one published benchmark matrix before manuscript freeze.

## Publication assessment

A simple catalog would be weak. A lineage-aware, independently validated
registry plus benchmark audit is suitable for a pathology-informatics or cancer-
informatics Resource Report. The project does not require a hospital partner,
new patient recruitment, or wet-laboratory work.

