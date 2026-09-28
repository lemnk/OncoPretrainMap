# OncoPretrainMap Computational Report

**Run date:** 2026-09-28

**Protocol:** v1, frozen 2026-09-27

**Status:** complete development analysis and 80-pair human verification

## Outcome

The metadata pipeline ran successfully from the pinned Bareja et al benchmark source snapshot
through registry derivation, benchmark linkage, descriptive analysis, figures,
validation-sample generation, tests, and file hashing. It did not train or run
foundation models and did not download whole-slide images or model weights.

## Inputs and outputs

| Item | Count |
|---|---:|
| Core model labels | 32 |
| Evaluation tasks | 41 |
| Published model–task rows | 1,312 |
| Primary-source assertions | 52 |
| Dataset/corpus records | 49 |
| Evaluation datasets | 28 |
| Model–dataset pairs | 896 |

The benchmark repository was pinned at commit
`076ffcef84b7c3359a9ceaeb16e423e567fcd27a`. Every core model has at least one
primary-source extraction. Naol Beyene created all 52 assertions, verified them
against the cited sources, and matched the benchmark model labels to the
versioned model/checkpoint records.

## Registry derivation

Classification followed the frozen precedence rule: exact identifier overlap
(D4), exact named-dataset exposure (D3), parent-repository exposure (D2),
documented disjointness (D0), then unresolved/insufficient disclosure (D1).

| Exposure class | Pairs |
|---|---:|
| D0 documented disjoint | 11 |
| D1 unresolved/insufficient disclosure | 806 |
| D2 parent-repository exposure | 51 |
| D3 exact named-dataset exposure | 28 |
| D4 exact identifier overlap | 0 |

A hash-verified PanCancer40M archive yielded 6,093 TCGA training-slide names,
5,671 cases, and 43,374,634 tile records across 16 cohorts. The public benchmark
materials did not provide matching evaluation-slide identifiers, so no D4 claim
was made.

## Benchmark and performance audit

All 1,312 published results were canonically resolved: 208 were D3, 52 were D0,
and 1,052 were D1. D1 is not an unexposed control group.

The pooled D1 fraction was stratified because the benchmark mixed pathology-
specific and general-purpose models. Among 943 rows for 23 pathology-specific
models, 683 (72.4%) were D1, 208 (22.1%) D3, and 52 (5.5%) D0. All 369 rows for
nine general-purpose comparators were D1. CPTAC contained 14 D3 rows, seven for
GPFM and seven for Phikon-v2.

The benchmark audit had no D2 rows because TCGA and CPTAC task labels were
canonicalized to their parent repositories. At that resolution, exact TCGA or
CPTAC assertions are D3. The 51 D2 pairs remain in the full registry for child
datasets linked to an exposed parent repository.

A post-protocol descriptive analysis fitted model- and task-fixed-effects
ordinary least-squares models with two-way clustered standard errors.

| Outcome and contrast vs D1 | Estimate | 95% CI | P value |
|---|---:|---:|---:|
| AUROC, D0 | 0.0086 | -0.0080 to 0.0252 | .301 |
| AUROC, D3 | -0.0046 | -0.0230 to 0.0137 | .611 |
| AUPRC, D0 | -0.0035 | -0.0347 to 0.0278 | .823 |
| AUPRC, D3 | -0.0063 | -0.0278 to 0.0152 | .554 |

No contrast showed evidence that documented exact-dataset exposure was
associated with higher performance after adjustment. This does not establish
equivalence, absence of memorization, or a causal exposure effect because
disclosure drives classification and D1 is heterogeneous.

## Validation state

The deterministic 80-pair reviewer file used SHA-256 seed text
`OncoPretrainMap-independent-review-v1-2026-09-28`. It contains all 11 D0 pairs
and 23 each sampled from D1, D2, and D3. The file exposes model and dataset names
but leaves classifications, evidence, and sources blank.

The sample was frozen after initial extraction, a deviation from the planned
held-out timing. Caleb Yitna Ref reviewed all 80 sampled relationships and the
cited evidence. His decisions agreed with all 80 development classifications:
11 D0, 23 D1, 23 D2, and 23 D3. Each row retains the decision, evidence strength,
source URLs, explanation, reviewer identity, date, and blinding status.

The completed workbook displayed the development classifications and records
`initially_blinded` as `No`. The observed agreement was therefore 80/80 (100%),
but it is reported as human verification rather than a blinded inter-rater
reliability estimate. Cohen's kappa is not presented as independent evidence.
Per-class agreement was 11/11 for D0 and 23/23 for each of D1, D2, and D3. No
sampled D1 pair was upgraded to D2 or D3 (0/23; exact one-sided 95% upper bound,
12.2%). This bound is conditional on nonblinded verification and is not an
unbiased registry-wide missed-exposure estimate. The pre-review v1 and post-
verification v2 classification files have identical hashes.
Row-level records are retained in
`data/validation/caleb_review_completed.xlsx` (SHA-256
`cbf85e3e19e001e79f6b1c9025c9342d69efe9d863af8b691a01b60f76f0b396`).

## Reproducibility verification

- Automated tests passed.
- Three PNG and three vector PDF figures were generated.
- Analytical artifacts were SHA-256 hashed after the last complete run.
- Raw benchmark input hashes and the publisher PanCancer40M hash are retained.
- `run_pipeline.ps1` regenerates derived tables, analysis, validation sample,
  figures, tests, and the manifest.

## Remaining dependencies

1. A blinded independent duplicate extraction would strengthen reliability
   assessment but is not represented as completed.
2. D4 testing requires public evaluation case/slide identifiers not found in the
   available benchmark materials.
3. A permanent DOI should follow validation and release freeze.

These limitations do not invalidate the registry or completed human
verification, but they prevent claiming blinded independent reliability or exact
slide-level overlap.
