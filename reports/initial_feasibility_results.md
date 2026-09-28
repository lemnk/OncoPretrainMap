# Development Analysis Results

**Run date:** 2026-09-28

**Protocol:** v1, frozen 2026-09-27

## Frozen discovery universe

The pinned PathBench repository contributed 32 model labels, 41 task records,
and 1,312 model–task result rows. Source files were hashed before derivation.
PathBench was used for discovery and the benchmark use case; every released
exposure assertion was checked against a primary paper, official repository,
official model card, or identifier manifest.

## Dataset and source registry

The registry contains 49 dataset or corpus records, six explicit lineage edges,
and 28 evaluation datasets. Fifty-two primary-source assertions cover all 32
core model labels. Assertions preserve model version, development stage, source
URL and version, retrieval date, evidence summary, and curator status.

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

All 1,312 PathBench model–task rows resolved to canonical model and evaluation-
dataset identifiers. Under the frozen rules, 208 rows were D3, 52 were D0, and
1,052 were D1. These counts describe disclosed exposure and disjointness, not
contamination prevalence or measured performance inflation.

## Descriptive performance sensitivity analysis

The 208 D3 rows had mean AUROC 0.7687, compared with 0.7719 among 1,052 D1 rows.
In model- and task-fixed-effects analyses with two-way clustered standard
errors, the D3-versus-D1 difference was -0.0046 (95% CI, -0.0230 to 0.0137;
P=.61) for AUROC and -0.0063 (95% CI, -0.0278 to 0.0152; P=.55) for AUPRC.
The 52 D0 rows likewise showed no clear adjusted association. These are
descriptive associations, not causal estimates of a contamination effect.

## Identifier-manifest feasibility

The PanCancer40M coordinate archive linked by the official H0-mini source was
downloaded and its publisher SHA-256 reproduced. Streaming the compressed
archive without extracting it yielded 6,093 unique TCGA slide filenames, 5,671
cases, 43,374,634 tile records, and 16 cancer cohorts. This proves that exact
training identifiers can be recovered for this corpus. It does not establish
D4 overlap because no corresponding PathBench evaluation-slide manifest was
found in the public materials.

## Validation and software verification

Sixteen tests cover exposure precedence, multilevel lineage, conflict flags,
documented disjointness, task and model aliases, curated foreign keys, source
coverage, and the rule that missing evidence is not independence.

An 80-pair review sample was selected deterministically: all 11 D0 pairs and 23
pairs each from D1, D2, and D3. Caleb Yitna Ref reviewed the evidence for all 80
relationships and agreed with all 80 development classifications. The completed
workbook displayed the development decisions, so the 100% agreement is reported
as human verification rather than blinded independent reliability.

## Remaining work before the final public release

1. A blinded independent duplicate extraction could strengthen the reliability
   analysis but is not claimed in this release.
2. If evaluation identifiers become available, compare them with the 6,093-slide
   training manifest for D4 overlap.
3. Freeze a numbered release and archive DOI.
