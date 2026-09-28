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
or checkpoint, we extracted pretraining and model-development datasets from
primary papers, supplements, official model cards,
and developer repositories. A dataset-lineage graph linked parent repositories
to named cohorts and derivatives. Model–dataset pairs were classified as D0,
documented disjoint; D1, no detected evidence or insufficient disclosure; D2,
parent-repository exposure; D3, exact named-dataset exposure; or D4, exact
case/slide/patch overlap. Exposure scope and evidence strength were stored
separately. We mapped the registry to 1,312 published model–task results and
applied a benchmark-resolution sensitivity rule: TCGA and CPTAC exposure was
classified as repository-level unless exact evaluation-subset identifiers were
available.

**Results:** The development registry contains 49 dataset/corpus records, 52
primary-source assertions covering all 32 models, and 896 model–dataset pairs.
Eleven pairs were D0, 806 D1, 51 D2, and 28 D3; none met D4 criteria. All 1,312
benchmark rows resolved to canonical identifiers. Under the benchmark-resolution
rule, 204 were D2, four D3, 52 D0, and 1,052 D1. Among 943 rows for 23 pathology-
specific models, 204 (21.6%) were D2, four (0.4%) D3, 52 (5.5%) D0, and 683
(72.4%) D1; all 369 rows for nine general-purpose comparators were D1.
Caleb Yitna Ref reviewed the evidence for all 80 sampled relationships and
agreed with every classification within each sampled class. None of 23 sampled
D1 pairs was upgraded to D2 or D3.

**Conclusion:** Public cancer-pathology benchmark independence often cannot be
established from current disclosures. OncoPretrainMap converts heterogeneous
provenance statements into conservative, executable evidence classes without
treating missing evidence as independence. A blinded second reviewer reproduced
all 80 sampled classifications.

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
for a specific model–benchmark query.[1,4,6] We therefore developed
OncoPretrainMap as an auditable registry of model-development exposure. The resource separates the
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

### Training-manifest feasibility demonstration

We downloaded the PanCancer40M coordinate archive linked by the official
H0-mini documentation and verified its published SHA-256 digest. To minimize
storage, the compressed archive was streamed without expanding all tile records
to disk. TCGA slide filenames, case identifiers, cohort codes, and tile counts
were extracted. This demonstrated that exact training identifiers could be
recovered for one model corpus. It was not tied to the benchmark and was not an
overlap test. Exact evaluation overlap would require an independent evaluation
identifier manifest.

### Benchmark audit

All benchmark model labels and tasks were mapped to canonical registry
identifiers. The primary audit summarized exposure classes; it did not estimate
the prevalence of memorization or performance inflation.

The registry evidence class and benchmark-resolution class were retained as
separate fields. Benchmark tasks labelled TCGA or CPTAC were mapped to the
canonical parent repository because the published task matrix did not identify
the exact evaluation subset or slide identifiers. A model's explicit TCGA or
CPTAC assertion remained D3 in the registry but was D2 in the benchmark-
resolution sensitivity analysis. D3 in that analysis was reserved for an exact
named external evaluation dataset. D4 still required shared identifiers.

A post-protocol exploratory analysis of published AUROC and AUPRC used model and
task fixed effects with two-way clustered standard errors. It is reported only
in the supplement. With 32 model clusters, 41 task clusters, exposure concentrated
in TCGA tasks, and D1 combining unknown states, the analysis was considered
underpowered and uninformative for performance effects.

### Validation and reproducibility

The software included automated tests of alias resolution, lineage traversal,
classification precedence, conflicts, foreign keys, source coverage, and the
rule that missing evidence is not independence. A deterministic 80-pair sample
contained all 11 D0 pairs and 23 pairs sampled from each of D1, D2, and D3.
Caleb Yitna Ref reviewed the cited evidence for every relationship and recorded
a classification, evidence strength, source URLs, explanation, identity, date,
and blinding status. Caleb Yitna Ref was blinded to the development
classifications during the initial review and reported no use of AI. We report
the full confusion matrix, agreement within each sampled class, and the number
of D1 pairs upgraded to D2 or D3. The pre-review files were
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

Documented exposure was uneven across models and datasets (Figure 2). General
vision and language–vision models typically disclosed broad natural-image or
web corpora without pathology evaluation-dataset identifiers. Several
pathology-specific checkpoints explicitly named TCGA, CPTAC, PAIP, PANDA,
CAMELYON, or other public pathology datasets. Eleven version-specific UNI and
TITAN relationships had explicit evidence supporting D0.

### Published benchmark exposure audit

Every one of the 1,312 published model–task results resolved to a canonical
model and evaluation dataset. The registry field classified 208 rows as D3.
The benchmark-resolution sensitivity analysis reclassified 190 TCGA rows and
14 CPTAC rows as D2 because the benchmark did not disclose identifiers for the
exact evaluated subsets. The resulting audit contained 204 D2 rows (15.5%),
four D3 rows (0.3%), 52 D0 rows (4.0%), and 1,052 D1 rows (80.2%). The four D3
rows were GPFM evaluations on BACH, BRACS, LC25000, and SICAPv2. No documented
exposure was identified among out-of-domain tasks under the available sources
(Figure 1). A D1 label did not establish disjointness.

The overall 80.2% D1 fraction mixed pathology-specific models with general-
purpose comparators that did not claim pathology pretraining. Among the 943
rows from 23 pathology-specific models, 683 (72.4%) were D1, 204 (21.6%) D2,
four (0.4%) D3, and 52 (5.5%) D0. All 369 rows from nine general-purpose models were D1. These
strata, rather than the pooled percentage alone, define the disclosure gap.

### Training-manifest feasibility demonstration

The PanCancer40M archive digest matched the publisher-reported hash. Streaming
the archive recovered 6,093 unique TCGA slide filenames representing 5,671 cases
and 43,374,634 tile coordinates across 16 cancer cohorts. This one-model
pretraining manifest was not linked to a benchmark evaluation manifest and did
not test overlap. It is released only as a feasibility and reproducibility asset.

### Exploratory performance analysis

The post-protocol fixed-effects analysis is reported in the supplement. It was
underpowered and uninformative because exposure was concentrated in TCGA tasks,
D1 mixed unknown exposure states, and only 32 model and 41 task clusters were
available. No conclusion about performance inflation or absence of an exposure
effect was drawn (Supplementary Figure S1).

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
date, and blinding status. The initial review was blinded, and the reviewer did
not use AI. None of the 23 sampled D1 pairs was upgraded to D2 or D3 (observed
rate, 0%; exact one-sided 95% upper bound, 12.2%). Because the sample was
stratified rather than a simple random sample, the bound should not be projected
directly to the full registry. The registry classifications were unchanged after
adjudication; v2 added the benchmark-resolution sensitivity field.

## Discussion

OncoPretrainMap demonstrates that the obstacle to evaluating pathology
foundation-model independence is not simply a lack of model lists. It is the
lack of a versioned connection between model-development evidence, dataset
lineage, and the exact benchmark being interpreted. In the Bareja et al use
case, approximately one in six published result rows involved exposure to a
containing repository or exact named dataset. Among pathology-specific models,
72.4% remained unresolved rather than documented as disjoint; the higher pooled value partly reflected
general-purpose comparators. This finding supports routine provenance auditing
while also showing why a binary contamination label would exceed the available
evidence.

The registry was designed to audit provenance, not to estimate a performance
penalty or advantage from overlap. The post-protocol regression could not answer
that question: D1 may contain both exposed and unexposed models, exposure was
concentrated in TCGA tasks, and the cluster counts were small. We therefore
treat it as an underpowered, uninformative supplementary analysis rather than a
negative result. The audit provides no basis to adjust published scores or rank
models by presumed contamination.

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
unavailable. The 80-pair blinded review achieved 100% agreement, but its
stratified design oversampled D0, D2, and D3 relative to the registry and did
not establish diagnostic accuracy against an external gold standard. Finally,
the fixed-effects performance analysis was post-protocol, noncausal,
underpowered, and uninformative.

Future releases should prioritize public case/slide manifests, checkpoint-
specific data statements, independent curation, and expansion to additional
benchmarks. Benchmark authors can make the greatest immediate contribution by
publishing evaluation identifiers or privacy-preserving hashes and by stating
explicitly whether those identifiers were excluded from pretraining.

## Conclusion

OncoPretrainMap provides a conservative and reproducible method for auditing
pretraining–evaluation exposure in cancer pathology foundation models. Applied
to 1,312 benchmark results, it identified 204 containing-repository
relationships and four exact named-dataset relationships, but a still larger
zone where independence could not be established. The
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

**Figure 1. Benchmark-resolution exposure classifications across benchmark
groups.** Bars show the proportion of published model–task results classified
as documented disjoint (D0), unresolved/insufficiently disclosed (D1),
repository-level exposure (D2), or exact named evaluation-dataset exposure
(D3). D1 is not evidence of independence.

**Figure 2. Model–dataset exposure registry.** The 32 × 28 matrix displays D0-D3
classifications for each core model/checkpoint and evaluation dataset. Gray D1
cells indicate unresolved or insufficiently disclosed relationships, not
documented independence.

**Supplementary Figure S1. Exploratory associations between registry exposure
class and reported performance.** Points and 95% confidence intervals are from
a post-protocol model- and task-fixed-effects analysis with two-way clustered
standard errors. The analysis is underpowered and uninformative; estimates are
not causal contamination effects.

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
