# OncoPretrainMap: An Auditable Registry of Pretraining–Evaluation Dataset Exposure in Cancer Pathology Foundation Models

Naol Beyene

Jackson State University, Jackson, Mississippi, USA

Corresponding author: Naol Beyene, Jackson State University, 1400 John R. Lynch
Street, Jackson, MS 39217, USA; naolzed6@gmail.com

## Abstract

**Purpose:** Cancer pathology foundation models are often pretrained on large
public repositories that also supply downstream benchmarks. Dataset names alone
cannot distinguish documented disjointness, repository-level exposure, and
exact case reuse. We developed OncoPretrainMap, a versioned provenance registry
and checker for evaluating pretraining–benchmark exposure claims.

**Methods:** We froze the 32-model, 41-task universe of a 2026 published
computational-pathology benchmark at a pinned repository commit. For each model
or checkpoint, we extracted pretraining and model-
development datasets from primary papers, supplements, official model cards,
and developer repositories. A dataset-lineage graph linked parent repositories
to named cohorts and derivatives. Model–dataset pairs were classified as D0,
documented disjoint; D1, no detected evidence or insufficient disclosure; D2,
parent-repository exposure; D3, exact named-dataset exposure; or D4, exact
case/slide/patch overlap. Exposure scope and evidence strength were stored
separately. We mapped the registry to 1,312 published model–task
results. A secondary descriptive analysis used model and task fixed effects with
two-way clustered standard errors.

**Results:** The development registry contains 49 dataset/corpus records, 52
primary-source assertions covering all 32 models, and 896 model–dataset pairs.
Eleven pairs were D0, 806 D1, 51 D2, and 28 D3; none met D4 criteria. All 1,312
benchmark rows resolved to canonical identifiers: 208 were D3, 52 D0, and 1,052
D1. Among 943 rows for 23 pathology-specific models, 208 (22.1%) were D3, 52
(5.5%) D0, and 683 (72.4%) D1; all 369 rows for nine general-purpose comparators
were D1. A hash-verified pretraining manifest yielded 6,093 TCGA slide identifiers,
but corresponding benchmark slide identifiers were unavailable. Documented D3
exposure was not associated with higher reported performance in the descriptive
analysis (AUROC difference vs D1, -0.0046; 95% CI, -0.0230 to 0.0137; AUPRC
difference, -0.0063; 95% CI, -0.0278 to 0.0152).
Caleb Yitna Ref reviewed the evidence for all 80 sampled relationships and
agreed with every classification within each sampled class. None of 23 sampled
D1 pairs was upgraded to D2 or D3.

**Conclusion:** Public cancer-pathology benchmark independence often cannot be
established from current disclosures. OncoPretrainMap converts heterogeneous
provenance statements into conservative, executable evidence classes without
treating missing evidence as independence. Human verification was complete, but
because the development classifications were visible, agreement should not be
interpreted as blinded inter-rater reliability.

## Introduction

Foundation models have expanded the scale and breadth of computational
pathology. Their pretraining corpora commonly combine public cancer repositories,
institutional archives, and web-derived material. The same public repositories,
especially The Cancer Genome Atlas (TCGA), are widely reused for downstream
evaluation. Recent reviews identify pretraining–evaluation overlap as an
unresolved threat to claims of independent generalization, and contemporary
benchmarks acknowledge that public-repository exposure cannot always be
excluded.[1-3] A recent WSI multimodal-benchmark audit demonstrated that
patient- and institution-level leakage can coexist and should be examined at
the identifier level.[5]

The practical problem is not solved by labeling an evaluation set “external” or
by finding no identical dataset name in a model card. A model may have seen a
parent repository, an earlier version of a cohort, the same slide under a
different derivative name, or a reused image encoder. Conversely, repository-
level exposure does not demonstrate that a particular evaluation slide was
seen. Collapsing these situations into a binary contaminated/not-contaminated
label either overstates evidence or mistakes missing disclosure for
independence.

Existing model surveys and public catalogs summarize architectures, data scale,
and broad corpus names, but they are not designed as versioned evidence ledgers
for a specific model–benchmark query.[1,4,6] We therefore developed OncoPretrainMap as an
auditable registry of model-development exposure. The resource separates the
scope of possible overlap from the strength of the supporting evidence, traces
dataset lineage, retains source versions, and produces restrained, executable
answers to model–dataset queries. We demonstrate its use by auditing every
reported result in the 32-model benchmark reported by Bareja et al.[2]

## Methods

### Study design and frozen universe

This metadata resource study used only public records and aggregate published
benchmark results. No patient-level clinical data were accessed. The protocol
was frozen on September 27, 2026, before registry analysis. The primary model
universe was the 32 model labels evaluated by Bareja et al, and the benchmark source
repository was pinned at commit
`076ffcef84b7c3359a9ceaeb16e423e567fcd27a`.[2,7] General vision and vision–
language comparators were retained because they were part of the published
comparison. The unit of registry analysis was a model/checkpoint version paired
with a specific evaluation dataset.

### Evidence acquisition

The source hierarchy was: (1) public training or evaluation identifier manifest;
(2) primary paper and supplement; (3) official model card or developer
repository; (4) benchmark paper; and (5) secondary reviews for discovery only.
We recorded model version, development stage, canonical dataset, source URL,
source version or repository revision, retrieval date, evidence summary, and
curation status. Development stages included pretraining, inherited image-
encoder pretraining, distillation, fine-tuning, and downstream training.

Naol Beyene, the sole author, created all 52 source assertions and verified each
against the cited primary paper, supplement, official model card, developer
repository, or identifier manifest. Initial primary-source extraction was
completed for all 32 core model labels.
The general-model entries used their released checkpoint documentation rather
than assuming exposure from architecture names. For inherited encoders, exposure
was propagated only when the evaluated model explicitly reused a specified
checkpoint. Conflicting exposure and disjointness assertions were retained and
flagged rather than silently resolved.

The sole author also matched the 32 benchmark model labels to the released
model or checkpoint named in the pinned benchmark repository and recorded the
corresponding paper, model-card revision, or repository commit. UNI and TITAN
were checked against their primary descriptions and official versioned
documentation, and GPFM exposure assertions were checked against its primary
article and supplement.[8-12]

### Dataset normalization and lineage

Dataset aliases were normalized to stable identifiers. Directed lineage edges
linked parent repositories to organ cohorts and named derivatives. For example,
TCGA was treated as the parent of cancer-specific TCGA cohorts. A lineage
inference could support repository exposure but could not establish exact slide
reuse. External and out-of-domain benchmark tasks were resolved from task labels
and the peer-reviewed Methods to their named public or institutional cohorts.[2]

### Exposure and evidence classes

We used five mutually exclusive exposure classes. D0 indicated a version-
relevant statement of documented disjointness. D1 indicated no detected evidence
or insufficient disclosure and was never interpreted as independence. D2
indicated exposure to a parent repository containing the evaluation cohort. D3
indicated explicit exposure to the named evaluation dataset. D4 required shared
case, slide, patch, or content-hash identifiers.

Evidence strength was recorded separately: A, identifier manifest; B, explicit
primary-source statement; C, lineage inference; and D, incomplete or ambiguous
disclosure. Classification precedence was D4, D3, D2, D0, then D1. D4 evidence
overrode a contradictory lower-level disjointness statement while preserving a
conflict flag.

### Exact-identifier feasibility check

We downloaded the PanCancer40M coordinate archive linked by the official
H0-mini documentation and verified its published SHA-256 digest. To minimize
storage, the compressed archive was streamed without expanding all tile records
to disk. TCGA slide filenames, case identifiers, cohort codes, and tile counts
were extracted. Exact evaluation overlap was to be called only if an independent
evaluation identifier manifest could be obtained.

### Benchmark audit and secondary analysis

All benchmark model labels and tasks were mapped to canonical registry
identifiers. The primary audit summarized exposure classes; it did not estimate
the prevalence of memorization or performance inflation. As a post-protocol,
descriptive sensitivity analysis, we summarized published AUROC and AUPRC by
exposure class and fitted ordinary least-squares models with model and task fixed
effects. Standard errors were two-way clustered by model and task. D1 was the
reference category. Because exposure was not randomized and D1 combines unknown
states, coefficients were interpreted only as descriptive associations.

Benchmark tasks labelled TCGA or CPTAC were mapped to the canonical parent
repository because the published task matrix did not identify a more specific
child dataset. Thus, an exact assertion for TCGA or CPTAC was D3 in this
benchmark audit. D2 remained available in the broader registry for a child
cohort whose parent repository, but not the child itself, was documented in
model development.

### Validation and reproducibility

The software included automated tests of alias resolution, lineage traversal,
classification precedence, conflicts, foreign keys, source coverage, and the
rule that missing evidence is not independence. A deterministic 80-pair sample
contained all 11 D0 pairs and 23 pairs sampled from each of D1, D2, and D3.
Caleb Yitna Ref reviewed the cited evidence for every relationship and recorded
a classification, evidence strength, source URLs, explanation, identity, date,
and blinding status. The completed workbook displayed the development
classification. The reviewer reported no use of AI during verification. We
therefore report a class-specific confusion matrix and the
number of D1 pairs upgraded to D2 or D3 as human verification, not as blinded
inter-rater reliability or diagnostic accuracy. The pre-review files were
frozen as v1; all outputs were regenerated after review as v2 while retaining
both releases.

OpenAI Codex (GPT-5.6 Sol; OpenAI; accessed September 27-28, 2026) assisted with
software development and automated retrieval and processing of public metadata.
The sole author checked all 52 source assertions, model-version mappings, and
analytical outputs. The AI system was not treated as an author, human reviewer,
or source of primary scientific evidence.

## Results

### Registry construction and disclosure status

The curated source layer contained 49 dataset or corpus records and 52 primary-
source assertions covering all 32 core model labels. The complete 32 × 28 grid
contained 896 model–dataset pairs. Eleven pairs (1.2%) were D0, 806 (90.0%) were
D1, 51 (5.7%) were D2, and 28 (3.1%) were D3. No pair met the D4 standard. The
large D1 fraction is a measure of unresolved provenance under conservative
rules, not evidence that 90% of relationships were independent.

Documented exposure was uneven across models and datasets (Figure 3). General
vision and language–vision models typically disclosed broad natural-image or
web corpora without pathology evaluation-dataset identifiers. Several
pathology-specific checkpoints explicitly named TCGA, CPTAC, PAIP, PANDA,
CAMELYON, or other public pathology datasets. Eleven version-specific UNI and
TITAN relationships had explicit evidence supporting D0.

### Published benchmark exposure audit

Every one of the 1,312 published model–task results resolved to a canonical
model and evaluation dataset. Of these, 208 rows (15.9%) had D3 exposure, 52
(4.0%) were D0, and 1,052 (80.2%) remained D1. TCGA accounted for the largest
concentration of D3 rows. CPTAC contributed 14 D3 rows—seven each for Phikon-v2
and GPFM—and four additional GPFM D3 rows occurred in external named datasets.
No documented exposure was identified among the out-of-domain tasks under the
available sources (Figure 1). The absence of a D3 label did not establish
disjointness.

The overall 80.2% D1 fraction mixed pathology-specific models with general-
purpose comparators that did not claim pathology pretraining. Among the 943
rows from 23 pathology-specific models, 683 (72.4%) were D1, 208 (22.1%) D3,
and 52 (5.5%) D0. All 369 rows from nine general-purpose models were D1. These
strata, rather than the pooled percentage alone, define the disclosure gap.

No D2 rows appeared in the benchmark audit because TCGA and CPTAC tasks were
canonicalized to the parent repository identifiers. The 51 D2 pairs in the
broader registry instead involve child datasets for which only parent-repository
exposure was documented; the distinction did not disappear from the registry.

### Identifier manifest

The PanCancer40M archive digest matched the publisher-reported hash. Streaming
the archive recovered 6,093 unique TCGA slide filenames representing 5,671 cases
and 43,374,634 tile coordinates across 16 cancer cohorts. No complete benchmark
evaluation-slide manifest was found in its public repository or article
materials. Consequently, the training identifiers were released as a
reproducibility asset, but no D4 benchmark-overlap claim was made.

### Descriptive performance findings

Mean AUROC was 0.8085 among 52 D0 rows, 0.7719 among 1,052 D1 rows, and 0.7687
among 208 D3 rows. These unadjusted groups differed in model and task
composition. After model and task fixed effects, the AUROC difference versus D1
was 0.0086 (95% CI, -0.0080 to 0.0252; P=.30) for D0 and -0.0046 (95% CI,
-0.0230 to 0.0137; P=.61) for D3. Corresponding AUPRC differences were -0.0035
(95% CI, -0.0347 to 0.0278; P=.82) and -0.0063 (95% CI, -0.0278 to 0.0152;
P=.55), respectively (Figure 2). Thus, this audit did not find evidence that
documented named-dataset exposure was associated with higher reported
performance. The intervals do not prove equivalence or exclude effects in
specific model–dataset pairs.

### Reproducibility checks

Nineteen automated tests passed. The complete workflow regenerated the exposure
matrix, benchmark audit, stratified summaries, descriptive models, frozen
review sample, three figures in raster and vector formats, and a SHA-256
artifact manifest. The command-line
checker returns the exposure class, evidence strength, constrained independence
statement, and supporting sources for a requested model–dataset pair.

Caleb Yitna Ref agreed with all 80 development classifications (80/80, 100%):
11 D0, 23 D1, 23 D2, and 23 D3. Per-class agreement was 11/11 for D0 and 23/23
for each of D1, D2, and D3; the full confusion matrix was diagonal. There were
no D4 pairs. Row-level records retain
the decision, evidence strength, source URLs, explanation, reviewer identity,
date, and blinding status. Because the development classifications were visible,
the result verifies the sampled records but does not estimate blinded inter-
rater reliability. None of the 23 sampled D1 pairs was upgraded to D2 or D3
(observed rate, 0%; exact one-sided 95% upper bound, 12.2%). Because the review
was not blinded, this bound describes the verification exercise and is not an
unbiased estimate of missed exposure in the full registry. The v1 and v2
registry classifications were identical after adjudication.

## Discussion

OncoPretrainMap demonstrates that the obstacle to evaluating pathology
foundation-model independence is not simply a lack of model lists. It is the
lack of a versioned connection between model-development evidence, dataset
lineage, and the exact benchmark being interpreted. In the Bareja et al use
case, approximately one in six published result rows involved explicit named-
dataset exposure. Among pathology-specific models, 72.4% remained unresolved
rather than documented as disjoint; the higher pooled value partly reflected
general-purpose comparators. This finding supports routine provenance auditing
while also showing
why a binary contamination label would exceed the available evidence.

The null descriptive performance result is important to interpret correctly.
The registry was designed to audit provenance, not to estimate a causal penalty
or advantage from overlap. D1 is shaped by disclosure quality and may contain
both exposed and unexposed models. D3 establishes dataset-level exposure but
does not show that the same slides were seen, that features were memorized, or
that evaluation scores were inflated. Accordingly, the analysis provides no
basis to adjust published scores or rank models by presumed contamination.

The resource offers three practical benefits for cancer informatics. First, it
gives benchmark designers a reproducible reason to avoid a dataset, accept it
with a caveat, or request identifiers from model developers. Second, it prevents
“not disclosed” from becoming “independent” through repetition. Third, it makes
provenance claims updateable: a new manifest can upgrade a pair from D2 or D3 to
D4, while an explicit exclusion can support D0 for a particular checkpoint.

Several limitations remain. Source disclosure is heterogeneous and may be
incomplete. The 32-model universe is tied to one frozen benchmark rather than
all pathology foundation models. Dataset lineage is necessarily curated and can
miss undisclosed derivatives. The recovered training-slide manifest could not
be matched to benchmark evaluation slides because the latter identifiers were
unavailable. The 80-pair human verification achieved 100% agreement, but the
development classifications were visible to the reviewer. It therefore does not
provide an unbiased estimate of independent inter-rater reliability. Finally,
fixed-effects associations are noncausal and may be underpowered for class-
specific effects.

Future releases should prioritize public case/slide manifests, checkpoint-
specific data statements, independent curation, and expansion to additional
benchmarks. Benchmark authors can make the greatest immediate contribution by
publishing evaluation identifiers or privacy-preserving hashes and by stating
explicitly whether those identifiers were excluded from pretraining.

## Conclusion

OncoPretrainMap provides a conservative and reproducible method for auditing
pretraining–evaluation exposure in cancer pathology foundation models. Applied
to 1,312 benchmark results, it identified substantial named-dataset exposure
but a still larger zone where independence could not be established. The
resource's central contribution is not a claim that exposure inflated
performance; it is an auditable boundary between what public evidence does and
does not support.

## Data and Code Availability

A row-level human-verification workbook is available in the OncoPretrainMap
repository with the source code, curated tables, derived results, tests, and
figures. A public repository URL and permanent archive DOI will be inserted
after the final release freeze. All underlying evidence sources are publicly
linked at row level. The 135-MB publisher archive used to derive the
PanCancer40M identifier manifest is excluded from version control; its URL and
hash are retained for reproducible acquisition.

## Ethics Statement

This study used public metadata and aggregate published results and did not
involve interaction with human participants or access to identifiable clinical
records. Institutional review board approval and informed consent were not
applicable.

## Funding

No external funding was received.

## Conflicts of Interest

The author reports no conflicts of interest.

## Author Contributions

Naol Beyene: conceptualization, methodology, investigation, data curation,
software, formal analysis, validation, visualization, writing, and project
administration.

## Acknowledgments

The author thanks Caleb Yitna Ref for reviewing the 80 sampled model–dataset
relationships. Caleb Yitna Ref did not develop the registry rules and is not
responsible for the analyses or conclusions.

## Figure Legends

**Figure 1. Exposure classifications across benchmark groups.** Bars
show the proportion of published model–task results classified as documented
disjoint (D0), unresolved/insufficiently disclosed (D1), or exact named-dataset
exposure (D3). D1 is not evidence of independence.

**Figure 2. Descriptive associations between exposure class and reported
performance.** Points and 95% confidence intervals are coefficients from model-
and task-fixed-effects models with two-way clustered standard errors. The D1
class is the reference. Estimates are not causal contamination effects.

**Figure 3. Model–dataset exposure registry.** The 32 × 28 matrix displays D0-D3
classifications for each core model/checkpoint and evaluation dataset. Gray D1
cells indicate unresolved or insufficiently disclosed relationships, not
documented independence.

## References

1. Zhang B, et al. Foundation Models in Cancer Pathology: Techniques,
   Applications, and Future Directions. *Research (Wash D C)*. 2026;9:1332.
   https://doi.org/10.34133/research.1332
2. Bareja R, et al. A benchmark study of vision and pathology foundation models
   for computational pathology. *Nature Communications*. 2026;17.
   https://doi.org/10.1038/s41467-026-76004-6
3. Campanella G, et al. A clinical benchmark of public self-supervised pathology
   foundation models. *Nature Communications*. 2025;16:3640.
   https://doi.org/10.1038/s41467-025-58796-1
4. Li D, et al. A survey on computational pathology foundation models: datasets,
   adaptation strategies, and evaluation tasks. *Knowledge and Information
   Systems*. 2026;68:209. https://doi.org/10.1007/s10115-026-02806-1
5. Zhang W, Zhou Z, Kang J, Li S. Auditing Data Leakage in Whole-Slide Image
   Multimodal Benchmarks. arXiv:2607.12278. 2026.
   https://doi.org/10.48550/arXiv.2607.12278
6. Wölflein G. List of pathology feature extractors and foundation models,
   commit 1acba67256af5cd08ebc9fd4cba3eb877871c6f9. Accessed September 28,
   2026. https://github.com/georg-wolflein/pathology-foundation-models
7. Gevaert Lab. Benchmarking Path Models repository, commit
   076ffcef84b7c3359a9ceaeb16e423e567fcd27a.
   https://github.com/gevaertlab/benchmarking-path-models
8. Chen RJ, Ding T, Lu MY, et al. Towards a general-purpose foundation model for
   computational pathology. *Nature Medicine*. 2024;30:850-862.
   https://doi.org/10.1038/s41591-024-02857-3
9. Ding T, Wagner SJ, Song AH, et al. A multimodal whole-slide foundation model
   for pathology. *Nature Medicine*. 2025;31:3749-3761.
   https://doi.org/10.1038/s41591-025-03982-3
10. Ding T, et al. A generalizable pathology foundation model using a unified
   knowledge distillation pretraining framework. *Nature Biomedical Engineering*.
   2025. https://doi.org/10.1038/s41551-025-01488-4
11. Mahmood Lab. UNI model card, revision
   b55a5ec6cade1a39edfe6534189a9b8ca7a022f0. Accessed September 27, 2026.
   https://huggingface.co/MahmoodLab/UNI/blob/b55a5ec6cade1a39edfe6534189a9b8ca7a022f0/README.md
12. Mahmood Lab. TITAN repository, commit
   9e34c66ff66445c6c590da0dbf7acc103d39a40b. Accessed September 27, 2026.
   https://github.com/mahmoodlab/TITAN/tree/9e34c66ff66445c6c590da0dbf7acc103d39a40b
