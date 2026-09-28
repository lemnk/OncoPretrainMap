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

## Supplementary Method 3: Human verification sample

The deterministic sample contains all 11 D0 pairs and 23 randomly selected pairs
from each of D1, D2, and D3. Python's pseudorandom generator was initialized from
the first eight bytes of the SHA-256 digest of
`OncoPretrainMap-independent-review-v1-2026-09-28`. Selected rows were shuffled
and numbered. The generated file SHA-256 is
`ce7ee7d92beb26e2d140cdb1e7da37ba5737396550aa566b66093c2510c7ddb5`.

Caleb Yitna Ref reviewed all 80 sampled relationships. For every row he recorded
an exposure class, evidence strength, source URLs, evidence note, reviewer label,
review date, and blinding status. The completed workbook displayed the
development classification and therefore records the review as not initially
blinded. The reviewer reported no AI use during verification. Exact agreement
is reported as human verification of sampled records rather than diagnostic
accuracy or unbiased inter-rater reliability. Because the sample was stratified,
agreement is reported separately within D0-D3 and as a
full confusion matrix. The missed-exposure check was the number of sampled D1
pairs upgraded to D2 or D3. For zero upgrades among 23 D1 pairs, the exact one-
sided 95% upper bound was calculated as `1 - 0.05^(1/23)`.

The pre-review registry and benchmark-audit tables were retained as v1. The
pipeline regenerated post-verification v2 tables and compared their hashes. No
classification changed after verification.

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
| S9 | `data/validation/independent_review_sample_v1.csv` | Frozen blank sample retained for provenance |
| S10 | `data/validation/caleb_review_completed.xlsx` | Completed row-level human verification with evidence and blinding status |
| S11 | `reports/human_verification_confusion_matrix.csv` | Per-class confusion matrix and agreement |
| S12 | `reports/exposure_by_model_stratum.csv` | Registry and benchmark exposure classes stratified by model type |
| S13 | `release/v1_pre_review/` and `release/v2_post_review/` | Frozen pre-review and regenerated post-verification tables |

## Supplementary Results

The D0 benchmark rows represented two models and 26 tasks; D3 rows represented
10 models and 30 tasks. Mean within-task AUROC percentile was 0.6875 for D0,
0.5108 for D1, and 0.4973 for D3. These descriptive values are confounded by
model selection, task availability, and disclosure and are not evidence that
disjointness improves performance.

No exact-overlap table is provided because no evaluated pair met D4 criteria.
The empty D4 result is retained rather than weakening the identifier standard.

## Supplementary human verification

Caleb Yitna Ref agreed with 80 of 80 development classifications: 11 D0, 23 D1,
23 D2, and 23 D3. There were no D4 pairs. Row-level decisions, evidence notes,
URLs, reviewer identity, date, and blinding status are retained in
`data/validation/caleb_review_completed.xlsx`. Because the development class was
visible in the completed workbook, the result is described as complete human
verification and not as blinded independent validation. Per-class agreement
was 100% in each sampled class. No D1 pair was upgraded to D2 or D3 (0/23;
exact one-sided 95% upper bound, 12.2%); this bound is conditional on the non-
blinded verification design and is not a registry-wide false-negative estimate.

## Supplementary model-stratified and lineage results

The benchmark contained 943 rows from 23 pathology-specific models and 369 rows
from nine general-purpose comparators. Among pathology-specific rows, 683
(72.4%) were D1, 208 (22.1%) D3, and 52 (5.5%) D0. All general-purpose rows
were D1. In the complete registry, 554 of 644 pathology-specific pairs (86.0%)
and all 252 general-purpose pairs were D1.

The benchmark audit contained no D2 rows because TCGA and CPTAC task labels
were canonicalized to their parent repository. Exact TCGA or CPTAC assertions
therefore yielded D3 at the resolution of the published task matrix. The 51 D2
pairs in the complete registry relate to child datasets for which only exposure
to an ancestor repository was documented. The CPTAC cross-check identified 14
D3 rows: seven for Phikon-v2 and seven for GPFM.
