# OncoPretrainMap Computational Report

**Run date:** 2026-09-28

**Protocol:** v1, frozen 2026-09-27

**Status:** complete development analysis, 80-pair human verification, and
independent benchmark transport analysis

## Outcome

The metadata pipeline ran successfully from the pinned Bareja et al benchmark source snapshot
through registry derivation, benchmark linkage, descriptive analysis, figures,
validation-sample generation, tests, and file hashing. It did not train or run
foundation models and did not download whole-slide images or model weights.

The already-frozen framework was then applied to the independently published
Campanella et al clinical benchmark without modifying D0-D4, the evidence
grades, precedence, or the missing-evidence rule.

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
| External-transport encoders | 11 |
| External-transport clinical tasks | 22 |
| External-transport model–task rows | 242 |

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
5,671 cases, and 43,374,634 tile records across 16 cohorts. This one-model
training-manifest result is a feasibility demonstration. It was not tied to a
benchmark evaluation manifest and did not test overlap.

## Benchmark and performance audit

All 1,312 published results were canonically resolved. The registry field had
208 D3 rows. Under the benchmark-resolution rule, 204 were D2, four D3, 52 D0,
and 1,052 D1. D1 is not an unexposed control group.

The pooled D1 fraction was stratified because the benchmark mixed pathology-
specific and general-purpose models. Among 943 rows for 23 pathology-specific
models, 683 (72.4%) were D1, 204 (21.6%) D2, four (0.4%) D3, and 52 (5.5%) D0.
All 369 rows for nine general-purpose comparators were D1. CPTAC contained 14
repository-level D2 rows, seven for GPFM and seven for Phikon-v2.

The benchmark-resolution field treats TCGA and CPTAC assertions as repository-
level D2 because exact evaluated subsets and slide identifiers were unavailable.
Four external named datasets remained D3.

A post-protocol descriptive analysis fitted model- and task-fixed-effects
ordinary least-squares models with two-way clustered standard errors.

| Outcome and contrast vs D1 | Estimate | 95% CI | P value |
|---|---:|---:|---:|
| AUROC, D0 | 0.0086 | -0.0080 to 0.0252 | .301 |
| AUROC, D3 | -0.0046 | -0.0230 to 0.0137 | .611 |
| AUPRC, D0 | -0.0035 | -0.0347 to 0.0278 | .823 |
| AUPRC, D3 | -0.0063 | -0.0278 to 0.0152 | .554 |

This post-protocol regression used registry classes and is retained only as a
supplementary sensitivity analysis. With 32 model clusters, 41 task clusters,
TCGA-concentrated exposure, and heterogeneous D1 states, it was underpowered and
uninformative. No positive, negative, or null performance conclusion is drawn.

## Independent benchmark transport

The transport protocol was frozen against OncoPretrainMap commit
`734b170839b1d97f79b3e58dba8d8b3f3943d70b` before detailed extraction. The
Campanella et al source tables and official repository commit
`fbdf07f932d7302fd7bcb4a1e6b78bfb9d4a71f9` defined 242 distinct combinations
of 11 encoders and 22 clinical tasks. The publisher source-data ZIP had SHA-256
`0b1309f282352d15e3c13835539499a1fdb23febecf76c2148be8735b8dd14aa`.

All 242 rows mapped to canonical identifiers, no conflict was recorded, and no
rule change was required.

| Exposure class | Rows | Percent |
|---|---:|---:|
| D0 documented disjoint | 44 | 18.2% |
| D1 unresolved/insufficient disclosure | 198 | 81.8% |
| D2 parent/containing corpus | 0 | 0% |
| D3 exact named dataset | 0 | 0% |
| D4 exact identifier overlap | 0 | 0% |

The D0 rows were SP22M and SP85M across all 22 tasks, supported by the paper's
explicit benchmark nonoverlap statement. Twelve Virchow/MSKCC rows carry an
explicit warning that overlap cannot be excluded, but remain D1 because the
source does not establish that the pretraining corpus contains the evaluation
cohorts. Caleb Yitna Ref completed the 60-row blinded review without AI.
Initial agreement was 58/60 (96.7%; kappa, 0.948). After the source-semantics
correction, final agreement was 46/60 (76.7%; kappa, 0.604).

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

Caleb Yitna Ref was blinded to the development classifications during initial
review, did not use AI, and records `initially_blinded` as `Yes`. Exact agreement
was 80/80 (100%).
Per-class agreement was 11/11 for D0 and 23/23 for each of D1, D2, and D3. No
sampled D1 pair was upgraded to D2 or D3 (0/23; exact one-sided 95% upper bound,
12.2%). Because the sample was stratified, this is not a registry-wide missed-
exposure estimate. The registry classifications were unchanged; v2 added the
benchmark-resolution sensitivity field.
Row-level records are retained in
`data/validation/caleb_review_completed.xlsx` (SHA-256
`80a84201019f2fa6d65123daf1a88d4b54f4a2169940a29e24fb1f5d160ea66e`).

## Reproducibility verification

- Twenty-two automated tests passed.
- Four PNG and four vector PDF figures were generated.
- Analytical artifacts were SHA-256 hashed after the last complete run.
- Raw benchmark input hashes and the publisher PanCancer40M hash are retained.
- `run_pipeline.ps1` regenerates derived tables, analysis, validation sample,
  figures, tests, and the manifest.

## Remaining dependencies

1. D4 testing requires public evaluation case/slide identifiers not found in the
   available benchmark materials.
2. A permanent DOI should follow validation and release freeze.
3. The 60-row external-transport review is complete. The two tRes50
   disagreements were adjudicated under the frozen D0 requirement, and the
   original reviewer decisions remain in the completed workbook.

These limitations do not invalidate the registry or blinded human review, but
they prevent claiming exact slide-level overlap or performance effects.
