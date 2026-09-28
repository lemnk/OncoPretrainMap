# OncoPretrainMap Computational Report

**Run date:** 2026-09-28

**Protocol:** v1, frozen 2026-09-27

**Status:** complete development analysis; independent duplicate extraction pending

## Outcome

The metadata pipeline ran successfully from the pinned PathBench source snapshot
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

The PathBench repository was pinned at commit
`076ffcef84b7c3359a9ceaeb16e423e567fcd27a`. Every core model has at least one
primary-source extraction.

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
held-out timing. It is therefore a blinded independent duplicate-extraction
sample, not a held-out development test. A second human reviewer who did not
create the rules must complete it before exact agreement and Cohen's kappa can
be reported.

An additional AI-assisted verification was completed across all 80 sampled
pairs. OpenAI Codex GPT-5.6 Sol reproduced 80/80 classifications, comprising 11
D0, 23 D1, 23 D2, and 23 D3 pairs. The AI was not blinded and used the same
curated evidence layer and frozen decision rules. The result is therefore a
rule-reproduction check, not independent validation or an estimate of source
accuracy. Row-level evidence is retained in
`data/validation/ai_assisted_review_v1.xlsx`.

## Reproducibility verification

- Fourteen automated tests passed.
- Three PNG and three vector PDF figures were generated.
- Analytical artifacts were SHA-256 hashed after the last complete run.
- Raw PathBench input hashes and the publisher PanCancer40M hash are retained.
- `run_pipeline.ps1` regenerates derived tables, analysis, validation sample,
  figures, tests, and the manifest.

## Remaining dependencies

1. A real independent reviewer must complete the frozen validation file.
2. D4 testing requires public evaluation case/slide identifiers not found in the
   available PathBench materials.
3. A permanent DOI should follow validation and release freeze.

These limitations do not invalidate the development registry, but they prevent
claiming independent validation or exact slide-level overlap.
