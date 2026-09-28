# OncoPretrainMap

OncoPretrainMap is a versioned, evidence-backed registry of possible
pretraining–evaluation dataset exposure in cancer computational pathology
foundation models.

The registry answers a narrow question:

> What evidence exists that a model was exposed to an evaluation dataset, its
> parent repository, or the same patients, cases, slides, or derived patches?

It does not infer independence from missing evidence and does not use the term
“contamination” unless exact patient-, case-, slide-, or patch-level overlap is
demonstrated.

## Initial scope

- Core model universe: the 32 model versions evaluated in the 2026 benchmark by
  Bareja et al.
- Expansion universe: pathology foundation models released by the frozen search
  date that have a paper, technical report, or public model card.
- Evaluation datasets: TCGA, CPTAC, PAIP, CAMELYON16/17, PCam, PANDA, BACH,
  BRACS, BreakHis, NCT-CRC-HE, CRC-VAL-HE, MHIST, SICAPv2, UniToPatho, HEST,
  GTEx, TCIA, and explicitly named derived subsets.
- Primary unit: model version × evaluation dataset version.

The frozen framework was subsequently transported, without a rule change, to
the independent 2025 clinical benchmark of Campanella et al: 11 encoders, 22
clinical tasks, and 242 model–task relationships.

## Evidence model

Exposure scope and evidence strength are recorded separately.

Exposure scope:

- `D0_documented_disjoint`
- `D1_no_detected_evidence_or_insufficient_disclosure`
- `D2_parent_repository_exposure`
- `D3_exact_dataset_exposure`
- `D4_exact_case_slide_or_patch_overlap`

Evidence strength:

- `A_identifier_manifest`
- `B_explicit_primary_source_statement`
- `C_lineage_inference`
- `D_incomplete_or_ambiguous_disclosure`

The checker never converts `D1` into a claim of independence.

## Access and licensing

The public repository is https://github.com/lemnk/OncoPretrainMap. Software is
released under the MIT License. Original curated metadata, derived tables,
protocols, documentation, and figures are released under CC BY 4.0. Third-party
source materials retain their original licenses and are fetched from the cited
authoritative locations when redistribution is inappropriate.

## Status

The protocol-frozen development release covers all 32 benchmark model labels,
28 evaluation datasets, 52 primary-source assertions, and 896 model–dataset
pairs. The 1,312-row benchmark-resolution audit contains 204 repository-level
D2 rows, four exact named-dataset D3 rows, 52 documented-disjoint D0 rows, and
1,052 unresolved D1 rows. Among 943 rows for 23 pathology-specific models,
72.4% were D1, 21.6% D2, 0.4% D3, and 5.5% D0. All 369 rows for nine general-
purpose comparators were D1. These are disclosure classifications, not
contamination prevalence estimates.

In the prespecified external transport analysis, all 242 Campanella et al
relationships mapped successfully. Forty-four (18.2%) were D0, 186 (76.9%) D1,
and 12 (5.0%) D2; none were D3 or D4. The 12 D2 rows were Virchow and Virchow2
on six MSKCC tasks and indicate exposure to a containing institutional corpus,
not proven patient or slide overlap. No classification rule changed after the
transport freeze.

A PanCancer40M feasibility demonstration recovered 6,093 TCGA training-slide
identifiers for one pretraining corpus. It was not tied to a benchmark
evaluation manifest and did not test overlap.

The post-protocol performance regression is retained only as an underpowered,
uninformative supplementary analysis. No performance-effect conclusion is drawn.

Caleb Yitna Ref reviewed all 80 sampled relationships and agreed with all 80
development classifications: 11 D0, 23 D1, 23 D2, and 23 D3. The review retained
row-level decisions, evidence strengths, URLs, explanations, reviewer identity,
date, and blinding status. Caleb was blinded to the development classifications
during initial review and did not use AI. No sampled D1 pair was upgraded to D2
or D3 (0/23). The registry classifications were unchanged; v2 added the
benchmark-resolution sensitivity field.

## Reproduce

From PowerShell with Python dependencies installed:

```powershell
powershell -ExecutionPolicy Bypass -File .\run_pipeline.ps1
```

Query a model–dataset pair with:

```powershell
python src\check_pretraining_overlap.py UNI tcga
```
