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

Caleb Yitna Ref independently reviewed all 80 sampled relationships while
blinded to the development classifications. For every row he recorded an
exposure class, evidence strength, source URLs, evidence note, reviewer label,
review date, and blinding status. The reviewer reported no AI use. Exact
agreement is reported by class and in a full confusion matrix. Because the sample was stratified,
agreement is reported separately within D0-D3 and as a
full confusion matrix. The missed-exposure check was the number of sampled D1
pairs upgraded to D2 or D3. For zero upgrades among 23 D1 pairs, the exact one-
sided 95% upper bound was calculated as `1 - 0.05^(1/23)`.

The pre-review registry and benchmark-audit tables were retained as v1. The
pipeline regenerated v2 tables after verification. No registry classification
changed; v2 added a benchmark-resolution field that treats TCGA and CPTAC task
rows as repository-level exposure without exact evaluation-subset identifiers.

## Supplementary Method 4: Independent benchmark transport

The framework was frozen at commit
`734b170839b1d97f79b3e58dba8d8b3f3943d70b` before detailed extraction of the
Campanella et al source tables. Its official repository was pinned at
`fbdf07f932d7302fd7bcb4a1e6b78bfb9d4a71f9`, and the publisher source-data ZIP
was verified by SHA-256. Distinct encoder–task pairs in Figures 1 and 2 defined
the external universe. The same D0-D4 definitions, A-D evidence grades,
precedence, conflict handling, and missing-evidence rule were applied. Adding
benchmark-specific model and task aliases was permitted; changing an exposure
definition or precedence rule was not.

A deterministic 60-row review packet was frozen before review. Under the
post-audit resolved classification it contains 20 D0 and 40 D1 relationships. The packet
omitted the initial class and evidence grade. Caleb Yitna Ref independently
reviewed all 60 relationships while blinded to the initial transport labels and
reported no AI use. Exact agreement, unweighted Cohen's kappa, and confusion
matrices were calculated from the original decisions. A later source-semantics
audit corrected 12 Virchow/MSKCC labels from D2 to D1 under the unchanged class
definitions. Original decisions and final adjudications were retained; no third
adjudicator was used.

The development blank packet was committed on September 28, 2026 before the
completed workbook. A draft written after the workbook was merged described
the development classifications as visible to the reviewer. The reviewer
reported initial blinding, and the blank packet has no development-class
column; the draft had confused the later comparison display with the initial
review interface. That wording was corrected later the same day. The record
does not document a fresh second pass, so none is claimed. The external blank
packet likewise preceded its completed workbook. These records and the dated
attestation document the review workflow, but cannot reconstruct what appeared
on the reviewer's screen. Neither review required an open-ended independent
search for missing source assertions.

The schema value `exposure_warning=overlap_cannot_be_excluded` was defined as an
orthogonal annotation for a primary-source warning that did not establish D2-D4.
It did not change the D1 classification or the precedence rules.

### Post hoc interpretation of the broad nonoverlap statement

Campanella et al state that most foundation models had no overlap with their
cohorts, but do not identify every checkpoint covered by that sentence.[3] We
retained source-specific classifications as primary. A post hoc sensitivity
scenario assigned the broad statement to the six other pathology foundation
model labels (CTransPath, Phikon, Phikon-v2, Prov-GigaPath, UNI, and h-optimus-0)
on all 22 tasks. A second scenario also assigned it to the ImageNet tRes50
baseline, which the paper distinguishes from the foundation models. Both are
maximal interpretive assumptions, not new version-specific evidence. Virchow
and Virchow2 stayed D1, and all 12 MSKCC warning rows remained D1. We retained
the original 242-row audit and stored scenario assignments separately. The
published sentence is explicit primary-source evidence (grade B) at aggregate
scope; extrapolation to a particular unnamed checkpoint is an ungraded
scenario assumption, not checkpoint-specific grade B evidence.

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
| S14 | `data/derived/campanella_transport_audit.csv` | Complete 242-row independent benchmark transport audit |
| S15 | `reports/cross_benchmark_exposure_comparison.csv` | Cross-benchmark D0-D4 comparison |
| S16 | `data/validation/campanella_transport_blinded_review_packet.csv` | Frozen blank 60-row blinded-review packet |
| S17 | `data/validation/campanella_caleb_blinded_review_completed.xlsx` | Completed blinded human review, comparison, adjudication, and attestation |
| S18 | `data/derived/campanella_blanket_statement_sensitivity.csv` | Row-level post hoc blanket-statement scenarios |
| S19 | `reports/campanella_blanket_statement_sensitivity.json` | Scenario definitions and counts |

## Supplementary Results

The post-protocol performance analysis used registry evidence classes rather
than the benchmark-resolution sensitivity field. D0 rows represented two models
and 26 tasks; registry-D3 rows represented 10 models and 30 tasks. Mean within-
task AUROC percentile was 0.6875 for D0, 0.5108 for D1, and 0.4973 for registry
D3. With 32 model clusters, 41 task clusters, TCGA-concentrated exposure, and
heterogeneous D1 states, the analysis was underpowered and uninformative. It
does not support a positive, negative, or null performance effect.

No exact-overlap table is provided because no evaluated pair met D4 criteria.
The empty D4 result is retained rather than weakening the identifier standard.

## Supplementary human verification

Caleb Yitna Ref agreed with 80 of 80 development classifications: 11 D0, 23 D1,
23 D2, and 23 D3. There were no D4 pairs. Row-level decisions, evidence notes,
URLs, reviewer identity, date, and blinding status are retained in
`data/validation/caleb_review_completed.xlsx`. The reviewer was blinded to the
development classifications during initial review and did not use AI. Per-class
agreement was 100% in each sampled class. No D1 pair was upgraded to D2 or D3
(0/23; exact one-sided 95% upper bound, 12.2%). Because the sample was
stratified, this bound is not a registry-wide false-negative estimate.

## Supplementary model-stratified and lineage results

The benchmark contained 943 rows from 23 pathology-specific models and 369 rows
from nine general-purpose comparators. Under the benchmark-resolution rule,
pathology-specific rows included 683 (72.4%) D1, 204 (21.6%) D2, four (0.4%)
D3, and 52 (5.5%) D0. All general-purpose rows
were D1. In the complete registry, 554 of 644 pathology-specific pairs (86.0%)
and all 252 general-purpose pairs were D1.

The registry field retained 208 D3 rows. The benchmark-resolution sensitivity
field reclassified 190 TCGA and 14 CPTAC rows as D2 because exposure to the
containing repository did not establish exposure to the exact evaluated subset.
Four external GPFM rows remained D3: BACH, BRACS, LC25000, and SICAPv2. The
CPTAC cross-check identified seven repository-level rows each for Phikon-v2 and
GPFM.

## Supplementary training-manifest feasibility demonstration

The PanCancer40M extraction recovered 6,093 TCGA training-slide identifiers for
one model corpus. No benchmark evaluation manifest was available for comparison.
This result demonstrates identifier recovery only; it is not an overlap test or
evidence of D4 exposure.

## Supplementary external-transport results

The frozen framework mapped all 242 Campanella et al relationships without a
rule change. Forty-four (18.2%) were D0 and 198 (81.8%) D1; no row met D2-D4.
Twelve Virchow/MSKCC D1 rows retained an explicit warning that overlap could not
be excluded, but the evidence did not establish a containing-corpus
relationship. These distributions describe benchmark-specific disclosure and
lineage, not contamination prevalence.

Initial blinded inter-rater agreement was 58/60 (96.7%; kappa, 0.948). After
the 12 D2-to-D1 source-semantics corrections, concordance with the post-audit
resolved classification was 46/60 (76.7%; descriptive kappa, 0.604):
20/20 D0 and 26/40 D1. The reviewer assigned D2 to the 12 Virchow/MSKCC warning
rows and D0 to two tRes50 rows; final adjudication retained D1 in all 14 cases.
The 46/60 comparison is not a clean inter-rater reliability statistic because
the resolved classification was jointly adjudicated and incorporated the
reviewer's initial decisions.

### Worked classification example: institutional co-provenance

Same-institution provenance alone does not establish a containing corpus.
Virchow pretraining and the Campanella MSKCC evaluation cohorts were associated
with MSKCC, and the primary source stated that overlap could not be excluded.
Because no public source established that the pretraining corpus contained the
evaluation cohorts, the frozen rule assigns D1 with an exposure warning—not D2.
This explicit rule was added to the classification guide after both initial
extractors independently overcalled these relationships as D2.

### Broad-statement sensitivity

| Interpretation | D0 | D1 | D2–D4 |
|---|---:|---:|---:|
| Source-specific primary audit | 44/242 (18.2%) | 198/242 (81.8%) | 0 |
| Blanket statement assigned to six other foundation models | 176/242 (72.7%) | 66/242 (27.3%) | 0 |
| Same assumption, plus tRes50 baseline | 198/242 (81.8%) | 44/242 (18.2%) | 0 |

The primary paper says “most” without naming all models. These alternative
counts show the effect of assigning that broad claim to specific checkpoints;
they do not show that those checkpoints were individually verified as disjoint.
The tRes50 extension is especially uncertain because the article describes it
as an ImageNet baseline separately from the pathology foundation models.[3]
