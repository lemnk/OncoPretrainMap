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

**Methods:** We froze the 32-model, 41-task universe of PathBench at a pinned
repository commit. For each model/checkpoint, we extracted pretraining and model-
development datasets from primary papers, supplements, official model cards,
and developer repositories. A dataset-lineage graph linked parent repositories
to named cohorts and derivatives. Model–dataset pairs were classified as D0,
documented disjoint; D1, no detected evidence or insufficient disclosure; D2,
parent-repository exposure; D3, exact named-dataset exposure; or D4, exact
case/slide/patch overlap. Exposure scope and evidence strength were stored
separately. We mapped the registry to 1,312 published PathBench model–task
results. A secondary descriptive analysis used model and task fixed effects with
two-way clustered standard errors.

**Results:** The development registry contains 49 dataset/corpus records, 52
primary-source assertions covering all 32 models, and 896 model–dataset pairs.
Eleven pairs were D0, 806 D1, 51 D2, and 28 D3; none met D4 criteria. All 1,312
benchmark rows resolved to canonical identifiers: 208 were D3, 52 D0, and 1,052
D1. A hash-verified pretraining manifest yielded 6,093 TCGA slide identifiers,
but corresponding benchmark slide identifiers were unavailable. Documented D3
exposure was not associated with higher reported performance in the descriptive
analysis (AUROC difference vs D1, -0.0046; 95% CI, -0.0230 to 0.0137; AUPRC
difference, -0.0063; 95% CI, -0.0278 to 0.0152).

**Conclusion:** Public cancer-pathology benchmark independence often cannot be
established from current disclosures. OncoPretrainMap converts heterogeneous
provenance statements into conservative, executable evidence classes without
treating missing evidence as independence. Independent duplicate extraction of
a frozen validation sample remains required before a validated release.

## Introduction

Foundation models have expanded the scale and breadth of computational
pathology. Their pretraining corpora commonly combine public cancer repositories,
institutional archives, and web-derived material. The same public repositories,
especially The Cancer Genome Atlas (TCGA), are widely reused for downstream
evaluation. Recent reviews identify pretraining–evaluation overlap as an
unresolved threat to claims of independent generalization, and contemporary
benchmarks acknowledge that public-repository exposure cannot always be
excluded.[1-3]

The practical problem is not solved by labeling an evaluation set “external” or
by finding no identical dataset name in a model card. A model may have seen a
parent repository, an earlier version of a cohort, the same slide under a
different derivative name, or a reused image encoder. Conversely, repository-
level exposure does not demonstrate that a particular evaluation slide was
seen. Collapsing these situations into a binary contaminated/not-contaminated
label either overstates evidence or mistakes missing disclosure for
independence.

Existing model surveys summarize architectures, data scale, and broad corpus
names, but they are not designed as versioned evidence ledgers for a specific
model–benchmark query.[1,4] We therefore developed OncoPretrainMap as an
auditable registry of model-development exposure. The resource separates the
scope of possible overlap from the strength of the supporting evidence, traces
dataset lineage, retains source versions, and produces restrained, executable
answers to model–dataset queries. We demonstrate its use by auditing every
reported result in a 32-model computational-pathology benchmark.[2]

## Methods

### Study design and frozen universe

This metadata resource study used only public records and aggregate published
benchmark results. No patient-level clinical data were accessed. The protocol
was frozen on September 27, 2026, before registry analysis. The primary model
universe was the 32 model labels evaluated by PathBench, and the benchmark source
repository was pinned at commit
`076ffcef84b7c3359a9ceaeb16e423e567fcd27a`.[2,5] General vision and vision–
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

Initial primary-source extraction was completed for all 32 core model labels.
The general-model entries used their released checkpoint documentation rather
than assuming exposure from architecture names. For inherited encoders, exposure
was propagated only when the evaluated model explicitly reused a specified
checkpoint. Conflicting exposure and disjointness assertions were retained and
flagged rather than silently resolved.

### Dataset normalization and lineage

Dataset aliases were normalized to stable identifiers. Directed lineage edges
linked parent repositories to organ cohorts and named derivatives. For example,
TCGA was treated as the parent of cancer-specific TCGA cohorts. A lineage
inference could support repository exposure but could not establish exact slide
reuse. External and out-of-domain PathBench tasks were resolved from task labels
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

All PathBench model labels and tasks were mapped to canonical registry
identifiers. The primary audit summarized exposure classes; it did not estimate
the prevalence of memorization or performance inflation. As a post-protocol,
descriptive sensitivity analysis, we summarized published AUROC and AUPRC by
exposure class and fitted ordinary least-squares models with model and task fixed
effects. Standard errors were two-way clustered by model and task. D1 was the
reference category. Because exposure was not randomized and D1 combines unknown
states, coefficients were interpreted only as descriptive associations.

### Validation and reproducibility

The software included automated tests of alias resolution, lineage traversal,
classification precedence, conflicts, foreign keys, source coverage, and the
rule that missing evidence is not independence. A deterministic 80-pair sample
was generated for blinded duplicate extraction: all 11 D0 pairs and 23 pairs
sampled from each of D1, D2, and D3. The reviewer file omits the development
class and evidence. This sample was frozen after initial extraction, contrary to
the protocol's intended held-out timing, and is therefore described as an
independent duplicate-extraction sample rather than a held-out validation set.
Agreement and unweighted Cohen's kappa will be calculated only after a genuinely
independent second human review.

Separately, an AI-assisted verification pass re-derived classifications for all
80 sampled pairs from the frozen assertions, disjointness records, and lineage
graph. The AI system had access to the repository and was not blinded to the
project's methods. We therefore summarized agreement as a software-rule
reproduction check and did not interpret it as independent curator reliability,
source truth, or diagnostic accuracy.

OpenAI Codex (GPT-5.6 Sol; OpenAI; accessed September 27-28, 2026) assisted with
software development and automated retrieval and processing of public metadata.
The author checked source evidence and analytical outputs. The AI system was not
treated as an author, independent human reviewer, or source of primary
scientific evidence. Its separately reported verification pass used the frozen
curated evidence and is labeled as AI-assisted.

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

### PathBench exposure audit

Every one of the 1,312 published model–task results resolved to a canonical
model and evaluation dataset. Of these, 208 rows (15.9%) had D3 exposure, 52
(4.0%) were D0, and 1,052 (80.2%) remained D1. TCGA accounted for the largest
concentration of D3 rows, whereas no documented exposure was identified among
the out-of-domain tasks under the available sources (Figure 1). The absence of
a D3 label in these tasks did not establish disjointness.

### Identifier manifest

The PanCancer40M archive digest matched the publisher-reported hash. Streaming
the archive recovered 6,093 unique TCGA slide filenames representing 5,671 cases
and 43,374,634 tile coordinates across 16 cancer cohorts. No complete PathBench
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

Fourteen automated tests passed. The complete workflow regenerated the exposure
matrix, benchmark audit, descriptive models, blinded review file, three figures
in raster and vector formats, and a SHA-256 artifact manifest. The command-line
checker returns the exposure class, evidence strength, constrained independence
statement, and supporting sources for a requested model–dataset pair.

The AI-assisted verification reproduced all 80 development classifications
(80/80, 100%): 11 D0, 23 D1, 23 D2, and 23 D3. There were no D4 pairs. Because
the AI used the same curated evidence and had repository access, this complete
concordance shows deterministic reproduction of the frozen rules only. It does
not replace the pending independent human duplicate extraction.

## Discussion

OncoPretrainMap demonstrates that the obstacle to evaluating pathology
foundation-model independence is not simply a lack of model lists. It is the
lack of a versioned connection between model-development evidence, dataset
lineage, and the exact benchmark being interpreted. In the PathBench use case,
approximately one in six published result rows involved explicit named-dataset
exposure, but four in five remained unresolved rather than documented as
disjoint. This finding supports routine provenance auditing while also showing
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
unavailable. Most importantly, the 80-pair duplicate extraction has not yet
been completed by an independent reviewer. The current files therefore support
a complete development analysis, not a claim of independently validated
registry accuracy. The 100% AI-assisted verification agreement cannot address
this limitation because the AI was not blinded and used the same curated source
layer. Finally, fixed-effects associations are noncausal and may be underpowered
for class-specific effects.

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

A row-level AI-assisted verification workbook and the blank blinded human-review
file are prepared in the OncoPretrainMap repository with the source code,
curated tables, derived development results, tests, and figures.
A public repository URL and permanent archive DOI will be inserted after the
independent review and final release freeze. All underlying evidence sources are
publicly linked at row level. The 135-MB publisher archive used to derive the
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

None.

## Figure Legends

**Figure 1. Exposure classifications across PathBench benchmark groups.** Bars
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

1. Zhang Y, et al. Foundation Models in Cancer Pathology: Techniques,
   Applications, and Future Directions. 2026.
   https://pmc.ncbi.nlm.nih.gov/articles/PMC13305026/
2. Bareja R, et al. A benchmark study of vision and pathology foundation models
   for computational pathology. *Nature Communications*. 2026;17.
   https://doi.org/10.1038/s41467-026-76004-6
3. Campanella G, et al. A clinical benchmark of public self-supervised pathology
   foundation models. *Nature Communications*. 2025;16:3640.
   https://doi.org/10.1038/s41467-025-58796-1
4. Li D, et al. A survey on computational pathology foundation models: datasets,
   adaptation strategies, and evaluation tasks. *Knowledge and Information
   Systems*. 2026;68:209. https://doi.org/10.1007/s10115-026-02806-1
5. Gevaert Lab. Benchmarking Path Models repository, commit
   076ffcef84b7c3359a9ceaeb16e423e567fcd27a.
   https://github.com/gevaertlab/benchmarking-path-models
6. Xu H, et al. A whole-slide foundation model for digital pathology from real-
   world data. *Nature*. 2024. https://doi.org/10.1038/s41586-024-07441-w
7. Lu MY, et al. A visual-language foundation model for computational pathology.
   *Nature Medicine*. 2024. https://pmc.ncbi.nlm.nih.gov/articles/PMC11384335/
8. Ding T, et al. A generalizable pathology foundation model. *Nature Biomedical
   Engineering*. 2025. https://doi.org/10.1038/s41551-025-01488-4
