# OncoPretrainMap: An Auditable Registry of Pretraining–Evaluation Dataset Exposure in Cancer Pathology Foundation Models

Naol Beyene

Jackson State University, Jackson, Mississippi, USA

Corresponding author: Naol Beyene, Jackson State University, 1400 John R. Lynch
Street, Jackson, MS 39217, USA; naolzed6@gmail.com

## Abstract

**Background and Scope:** Cancer pathology models and benchmarks may draw from
the same repositories. We developed OncoPretrainMap, an auditable registry and
checker for pretraining–evaluation exposure claims.

**Solution:** Versioned primary-source assertions and dataset-lineage edges are
converted into five conservative classes: D0, documented disjoint; D1,
unresolved or insufficiently disclosed; D2, containing-repository exposure; D3,
exact named-dataset exposure; and D4, exact case/slide/patch overlap. Evidence
strength is stored separately, and missing evidence never implies independence.

**Evaluation:** In a 32-model, 41-task development benchmark, all 1,312 results
mapped to canonical identifiers; 52 (4.0%) were D0, 1,052 (80.2%) D1, 204
(15.5%) D2, and four (0.3%) D3. A blinded reviewer agreed on 80/80 sampled
development relationships. In a separate 11-model, 22-task benchmark, all 242
relationships mapped: 44 (18.2%) were D0 and 198 (81.8%) D1. Initial blinded
agreement was 58/60 (96.7%). Source review corrected 12 jointly assigned D2
labels to D1; reviewer concordance with the resolved classes was 46/60 (76.7%).
A subsequent stratified challenge of 80 previously unreviewed relationships had
80/80 agreement (kappa, 1.00), including 28 D2 and five D3 relationships.
Applying a broad nonoverlap statement to six additional models in a sensitivity
scenario reduced D1 to 66/242 (27.3%). The D2 corpus-containment requirement
remained frozen; the 12 labels were corrected as application errors after source
audit, without changing a definition or precedence rule.

**Relevance:** The checker identifies what public sources support for a proposed
model and evaluation cohort. External transport exercised D0 and D1 only;
the broad nonoverlap statement makes its class distribution interpretation
sensitive to source wording.

**How to Access/Use:** Source code, row-level evidence, frozen protocols, tests,
and the command-line checker are available at
https://github.com/lemnk/OncoPretrainMap; a versioned archive DOI will accompany
the final release.

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
reported result in the 32-model benchmark reported by Bareja et al and then
transporting the frozen framework to the independently developed clinical
benchmark reported by Campanella et al.[2,3]

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
We recorded checkpoint, development stage, dataset, source and revision, date,
and evidence summary.

Naol Beyene, the sole author, created all 52 source assertions and verified each
against the cited primary paper, supplement, official model card, developer
repository, or identifier manifest. All 32 benchmark labels were matched to
released checkpoints. Inherited encoder exposure required documented checkpoint
reuse. Conflicting assertions were retained and flagged.[8-12]

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

We verified and streamed the PanCancer40M archive linked by official H0-mini
documentation, extracting TCGA slide filenames, case identifiers, cohorts, and
tile counts. The extracted training identifiers could not be compared without
benchmark evaluation identifiers.

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

### Independent benchmark transport

After completing the v2 development application, we froze the definitions,
evidence hierarchy, lineage rules, precedence rules, and missing-evidence rule
at Git commit `734b170839b1d97f79b3e58dba8d8b3f3943d70b`. Before extracting detailed
external rows, we prespecified Campanella et al as the transport benchmark and
pinned its official repository at commit
`fbdf07f932d7302fd7bcb4a1e6b78bfb9d4a71f9`.[3] The publisher source-data
archive was verified by SHA-256 hash.

The external universe comprised every distinct encoder-by-task combination in
the version-of-record source tables: 11 encoders and 22 clinical tasks from
three health systems. We resolved models, tasks, institutions, and cohorts and
applied D0-D4 unchanged. The paper's explicit nonoverlap statement for SP22M and
SP85M supported D0. For MSKCC-trained Virchow models evaluated on MSKCC tasks,
the paper stated that overlap could not be excluded. We retained this as an
explicit overlap-warning field but assigned D1 because same-institution
provenance did not establish that the pretraining corpus contained the
evaluation cohorts. Other relationships also remained D1. Prespecified outcomes
were mapping success, class counts, warnings, conflicts, and rule changes.[3]
An exposure warning denoted a source statement that overlap could not be
excluded when the evidence did not satisfy D2-D4. It was an orthogonal
annotation, and the relationship remained D1.
Under the unchanged D2 definition, shared institutional provenance without
stated or demonstrated corpus containment is D1, not D2; same-institution
training and evaluation do not establish containment.
After reviewing the article's broader statement that “most foundation models”
had no cohort overlap, we performed a post hoc sensitivity analysis. We
assigned that statement to six other foundation models, then additionally to
the ImageNet tRes50 baseline. Neither scenario changed the primary audit.[3]

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

For the external transport, a deterministic 60-row review sample was frozen
before unblinding. Caleb Yitna Ref independently reviewed every relationship
while blinded to the initial transport classifications and reported no AI use.
We calculated exact agreement, unweighted Cohen's kappa, and a confusion matrix.
A subsequent source-semantics audit applied the unchanged class definitions to
the Virchow/MSKCC warnings. Original decisions, pre-audit labels, corrected
classes, and resolution notes were retained; no third adjudicator was used.
The blank review packets and completed workbooks document the review sequence;
the integrated comparison sheets display both classifications after review.
The reviewer completed the blank packet while blinded to the initial
classifications. The author created the integrated comparison sheets only after
the independent decisions had been recorded; those sheets were not the review
interface.

After correcting the 12 D2 application errors under the unchanged frozen
definition, we froze a SHA-256-seeded,
class-stratified challenge of 10 D0, 37 D1, 28 D2, and five D3 relationships,
excluding every pair in the earlier review packets. The reviewer independently
searched public sources and recorded checkpoint resolution, class, evidence
grade, URLs, rationale, search history, date, blinding, and AI-use status while
blinded to the key. We prespecified a confusion matrix, agreement, kappa,
class-specific agreement, D1 upgrades, and D2 downgrades. This tested rule
reliability, not a third benchmark, prevalence, or D4.

OpenAI Codex (GPT-5.6 Sol; OpenAI; accessed September 27-29, 2026) assisted with
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

### Independent clinical-benchmark transport

All 242 model–task relationships in the Campanella et al benchmark resolved to
canonical model and task identifiers (100% mapping success). The frozen rules
classified 44 relationships (18.2%) as D0 and 198 (81.8%) as D1; none met D2-D4
criteria (Figure 3). The 44 D0 relationships were SP22M and SP85M across the 22
tasks, reflecting the benchmark paper's explicit nonoverlap statement. Twelve
Virchow/MSKCC D1 relationships carried an explicit source warning that overlap
could not be excluded. They were not D2 because the evidence did not establish
that the pretraining corpus contained the evaluation cohorts. No exposure
definition, evidence grade, or precedence rule changed.

Initial blinded inter-rater agreement was 58/60 (96.7%; kappa, 0.948). An audit
corrected 12 jointly agreed Virchow/MSKCC D2 labels to D1. Concordance with the
post-audit resolved classification was 46/60 (76.7%; descriptive kappa, 0.604):
20/20 D0 and 26/40 D1. This was not a clean reliability estimate because the
resolved classification was jointly adjudicated and incorporated reviewer
decisions. The other two disagreements were tRes50 rows classified D0 by the reviewer; D1 was retained
because no explicit version-specific exclusion was documented.
This was erroneous application of the prespecified D2 definition, not a change
to the framework: institutional co-provenance alone did not satisfy the frozen
requirement that the development corpus be shown to contain the evaluation
cohort.

The distribution differed from the development application: the external
benchmark had more documented disjointness (18.2% vs 4.0%) and no D2 or D3.
D1 was largest in both (81.8% and 80.2%). Assigning the broad nonoverlap
statement to six additional foundation models changed external D0/D1 counts to
176/66 (72.7%/27.3%); including tRes50 changed them to 198/44
(81.8%/18.2%). These assumptions lack checkpoint-specific confirmation. The
transport classifications therefore depend strongly on how that statement is
interpreted.[3]

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

Automated tests passed. The complete workflow regenerated the exposure
matrix, benchmark audit, stratified summaries, descriptive models, frozen
review samples, four figures in raster and vector formats, and a SHA-256
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

### Post-correction rule-application challenge

The blinded reviewer agreed with all 80 frozen challenge classifications
(80/80, 100%; unweighted Cohen's kappa, 1.00): 10/10 D0, 37/37 D1, 28/28 D2,
and 5/5 D3. No D1 relationship was upgraded to D2-D4, and no D2 relationship
was downgraded to D1. Checkpoint/version resolution was recorded as resolved for
72 relationships and unclear for eight. No adjudication changed a class. These
results assess application of the frozen rules within existing source families;
they do not
establish registry completeness, third-benchmark transport, or D4 detection.

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

The transport application mapped every Campanella relationship using the frozen
class definitions. A post-review source audit identified and corrected a 12-row
application error without changing the D2 definition, evidence hierarchy, or
precedence rules. The final transport set exercised D0 and D1 only, leaving
external reproducibility of D2–D4 untested.

The post-correction challenge then exercised D0-D3 on 80 relationships not
used in either earlier review sample. Complete agreement, including 28 D2 and
five D3 relationships, shows that the frozen containing-corpus rule could be
applied consistently in this challenge. Because the sample reused the existing
source families and had no D4 cases, it does not replace external validation of
positive exposure classes or identifier-level overlap.

The audit does not estimate performance inflation. D1 mixes unknown states,
exposure clustered in TCGA tasks, and the post-protocol regression was
underpowered. Published model scores should not be adjusted from these results.

Before selecting a model for a cancer study, a researcher can query the exact
checkpoint and proposed validation dataset and receive the exposure class,
evidence grade, supporting source, and strongest independence statement the
public record permits. New identifiers can update that classification.

Several limitations define the resource's intended use. The registry reflects
two published benchmark model sets and the public evidence available at the
freeze date; classifications can change when new disclosures or identifiers
appear. The Campanella transport exercised D0 and D1, whereas the later
challenge tested reproducibility across D0-D3 within existing source families.
The human reviews therefore evaluate application of the evidence rules rather
than exhaustive registry completeness. D4 remains untested because paired
training and evaluation identifiers were unavailable. The exploratory
performance analysis was not used to infer performance inflation. Accordingly,
OncoPretrainMap supports evidence-qualified provenance screening and benchmark
selection, not certification of nonoverlap or estimation of performance effects.

Future releases should prioritize public case/slide manifests, checkpoint-
specific data statements, independent curation, and expansion to additional
benchmarks. Benchmark authors can make the greatest immediate contribution by
publishing evaluation identifiers or privacy-preserving hashes and by stating
explicitly whether those identifiers were excluded from pretraining.

## Conclusion

OncoPretrainMap provides a conservative and reproducible method for auditing
pretraining–evaluation exposure in cancer pathology foundation models. Applied
to 1,554 relationships across two independently developed benchmarks, it
distinguished documented disjointness, containing-corpus exposure, exact
named-dataset exposure, and a still larger zone where independence could not be
established. The
resource's central contribution is not a claim that exposure inflated
performance; it is an auditable boundary between what public evidence does and
does not support.

## Data and Code Availability

Row-level human-verification workbooks are available in the OncoPretrainMap
repository (https://github.com/lemnk/OncoPretrainMap) with the source code,
curated tables, derived results, tests, and figures. Software is licensed under
MIT; original metadata and documentation are licensed under CC BY 4.0. A
permanent archive DOI will be inserted after the final release freeze. All
underlying evidence sources are publicly linked at row level. The 135-MB
publisher archive used to derive the
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

The author thanks Caleb Yitna Ref for independently reviewing the 80 sampled
registry relationships, the 60 sampled external-transport relationships, and
the 80-relationship post-correction challenge.
Caleb Yitna Ref did not develop the registry rules and is not responsible for
the analyses or conclusions.

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

**Figure 3. Classification of two published benchmarks.**
Bars compare benchmark-resolution D0-D3 proportions in the Bareja et al
development application and Campanella et al external transport analysis. The
definitions were frozen before detailed extraction of the external benchmark;
the later source audit corrected 12 applications without changing the D2
definition. Campanella relationships
exercised D0 and D1 only.
Hatching identifies the 12 Campanella D1 relationships with an explicit source
warning that overlap could not be excluded; the warning did not establish D2.
Differences describe these benchmark ecosystems and are not field-wide
prevalence estimates.

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
