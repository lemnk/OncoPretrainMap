# Development Analysis Results

**Run date:** 2026-09-28

**Protocol:** v1, frozen 2026-09-27

## Frozen discovery universe

The pinned Bareja et al benchmark repository contributed 32 model labels, 41 task records,
and 1,312 model–task result rows. Source files were hashed before derivation.
The benchmark was used for discovery and the benchmark use case; every released
exposure assertion was checked against a primary paper, official repository,
official model card, or identifier manifest.

## Dataset and source registry

The registry contains 49 dataset or corpus records, six explicit lineage edges,
and 28 evaluation datasets. Fifty-two primary-source assertions cover all 32
core model labels. Assertions preserve model version, development stage, source
URL and version, retrieval date, evidence summary, and curator status.
Naol Beyene created all 52 assertions, verified each against its cited source,
and checked the benchmark labels against the recorded model/checkpoint versions.

Eleven UNI or TITAN model–dataset pairs have version-relevant primary-source
statements supporting documented disjointness. Inherited exposure was recorded
when a released model explicitly reused a pretrained encoder; the evaluated
MI-Zero checkpoints therefore inherit the reported TCGA and PAIP exposure of
their CTransPath image encoder.

The 896-pair development matrix contains:

- 11 documented-disjoint pairs (D0);
- 806 unresolved or insufficiently disclosed pairs (D1);
- 51 parent-repository exposures inferred through lineage (D2); and
- 28 exact named-dataset exposures (D3).

No pair was assigned D4 without exact shared identifiers. D1 must not be
interpreted as independent or unexposed.

## Published benchmark audit

All 1,312 benchmark model–task rows resolved to canonical model and evaluation-
dataset identifiers. The registry field contained 208 D3 rows. Under the
benchmark-resolution rule, 204 were D2, four D3, 52 D0, and 1,052 D1. These
counts describe disclosed exposure and disjointness, not
contamination prevalence or measured performance inflation.

Among 943 rows for 23 pathology-specific models, 683 (72.4%) were D1, 204
(21.6%) D2, four (0.4%) D3, and 52 (5.5%) D0. All 369 rows for nine general-
purpose comparators were D1. CPTAC contained 14 repository-level D2 rows, seven
each for GPFM and Phikon-v2.

## Descriptive performance sensitivity analysis

The post-protocol fixed-effects analysis used registry classes and is retained
only in the supplement. With 32 model clusters, 41 task clusters, exposure
concentrated in TCGA tasks, and heterogeneous D1 states, it was underpowered and
uninformative. No positive, negative, or null performance conclusion is drawn.

## Identifier-manifest feasibility

The PanCancer40M coordinate archive linked by the official H0-mini source was
downloaded and its publisher SHA-256 reproduced. Streaming the compressed
archive without extracting it yielded 6,093 unique TCGA slide filenames, 5,671
cases, 43,374,634 tile records, and 16 cancer cohorts. This one-model training-
manifest result is a feasibility demonstration. It was not tied to a benchmark
evaluation manifest and did not test overlap.

## Validation and software verification

Nineteen tests cover exposure precedence, multilevel lineage, conflict flags,
documented disjointness, task and model aliases, curated foreign keys, source
coverage, and the rule that missing evidence is not independence.

An 80-pair review sample was selected deterministically: all 11 D0 pairs and 23
pairs each from D1, D2, and D3. Caleb Yitna Ref reviewed the evidence for all 80
relationships and agreed with all 80 development classifications. The completed
reviewer was blinded to the development decisions during initial review and did
not use AI. No sampled D1 pair was upgraded to D2 or D3 (0/23; exact one-sided
95% upper bound, 12.2%). The registry classifications were unchanged; v2 added
the benchmark-resolution field.

## Remaining work before the final public release

1. If evaluation identifiers become available, compare them with the 6,093-slide
   training manifest for D4 overlap.
2. Freeze a numbered release and archive DOI.
