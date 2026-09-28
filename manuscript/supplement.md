# Supplementary Methods and Data Index

## Supplementary Method 1: Registry decision procedure

For each model/checkpoint–evaluation-dataset pair, the software applies the
following ordered rules:

1. A shared case, slide, patch, or content hash establishes D4.
2. An explicit primary-source assertion for the named evaluation dataset
   establishes D3.
3. An assertion for an ancestor in the curated dataset-lineage graph establishes
   D2.
4. A version-relevant explicit exclusion establishes D0.
5. Otherwise the pair remains D1.

The software records conflicts when positive exposure evidence and a
documented-disjoint statement coexist. D4-D2 evidence is not discarded in favor
of a lower-priority exclusion. The independence statement is generated from the
derived class and never substitutes “independent” for D1.

## Supplementary Method 2: Performance model

Let `y_mt` denote AUROC or AUPRC for model `m` on task `t`. The descriptive model
was:

`y_mt = beta0 + beta1 I(D0_mt) + beta2 I(D3_mt) + alpha_m + gamma_t + error_mt`

D1 was the reference. Model and task indicators were included as fixed effects.
The covariance estimator used two-way clustering by model and task with the
intersection term subtracted. Degrees of freedom were the smaller cluster count
minus one. The design contained 1,312 observations, 32 model clusters, 41 task
clusters, and rank 74. No causal identification assumption was made.

## Supplementary Method 3: Independent duplicate extraction

The deterministic sample contains all 11 D0 pairs and 23 randomly selected pairs
from each of D1, D2, and D3. Python's pseudorandom generator was initialized from
the first eight bytes of the SHA-256 digest of
`OncoPretrainMap-independent-review-v1-2026-09-28`. Selected rows were shuffled
and numbered. The generated file SHA-256 is
`ce7ee7d92beb26e2d140cdb1e7da37ba5737396550aa566b66093c2510c7ddb5`.

The second reviewer must save an exposure class, evidence strength, source URLs,
evidence note, reviewer label, review date, and blinding status for every row.
The supplied analysis script rejects incomplete or invalid files and produces
the confusion matrix, exact agreement, and unweighted Cohen's kappa. Agreement
is interpreted as reproducibility of extraction, not diagnostic accuracy
against a gold standard.

## Supplementary Table Index

| Table | File | Description |
|---|---|---|
| S1 | `data/curated/datasets.csv` | Canonical datasets, corpora, versions, and parent lineage |
| S2 | `data/curated/model_dataset_assertions.csv` | Primary-source exposure assertions |
| S3 | `data/curated/documented_disjoint.csv` | Version-specific documented-disjoint evidence |
| S4 | `data/derived/model_dataset_exposure_development.csv` | Complete 896-pair registry |
| S5 | `data/derived/pathbench_exposure_audit_development.csv` | Complete 1,312-row benchmark audit |
| S6 | `reports/performance_by_exposure_summary.csv` | Unadjusted descriptive summaries |
| S7 | `reports/performance_exposure_fixed_effects.csv` | Fixed-effects coefficient estimates |
| S8 | `data/derived/pancancer40m_training_slides.csv` | Exact PanCancer40M training slide identifiers |
| S9 | `data/validation/independent_review_sample_v1.csv` | Frozen, blank duplicate-extraction sample |
| S10 | `data/validation/ai_assisted_review_v1.xlsx` | Row-level AI-assisted verification with evidence and limitations |

## Supplementary Results

The D0 benchmark rows represented two models and 26 tasks; D3 rows represented
10 models and 30 tasks. Mean within-task AUROC percentile was 0.6875 for D0,
0.5108 for D1, and 0.4973 for D3. These descriptive values are confounded by
model selection, task availability, and disclosure and are not evidence that
disjointness improves performance.

No exact-overlap table is provided because no evaluated pair met D4 criteria.
The empty D4 result is retained rather than weakening the identifier standard.

## Supplementary AI-assisted verification

OpenAI Codex GPT-5.6 Sol re-derived the 80 sampled classifications from the
frozen curated assertions, disjointness table, and dataset-lineage rules. It
agreed with 80 of 80 development classifications: 11 D0, 23 D1, 23 D2, and 23
D3. The AI had repository access and was not blinded. This analysis checks
reproducibility of rule application from the same evidence layer. It is not an
independent review, a gold-standard validation, or evidence that the underlying
public disclosures are complete or correct. Row-level decisions, evidence
notes, URLs, reviewer identity, date, and blinding status are retained in
`data/validation/ai_assisted_review_v1.xlsx`.
