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

- Core model universe: the 32 model versions evaluated by the 2026 PathBench
  study.
- Expansion universe: pathology foundation models released by the frozen search
  date that have a paper, technical report, or public model card.
- Evaluation datasets: TCGA, CPTAC, PAIP, CAMELYON16/17, PCam, PANDA, BACH,
  BRACS, BreakHis, NCT-CRC-HE, CRC-VAL-HE, MHIST, SICAPv2, UniToPatho, HEST,
  GTEx, TCIA, and explicitly named derived subsets.
- Primary unit: model version × evaluation dataset version.

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

## Status

The protocol-frozen development release covers all 32 PathBench model labels,
28 evaluation datasets, 52 primary-source assertions, and 896 model–dataset
pairs. In the 1,312-row published benchmark audit, 208 rows have documented
named-dataset exposure, 52 are documented disjoint, and 1,052 remain unresolved.
These are disclosure classifications, not contamination prevalence estimates.

A primary PanCancer40M manifest contains 6,093 exact TCGA training-slide
identifiers. No D4 claim is made because PathBench evaluation slide identifiers
were not publicly recoverable. An 80-pair deterministic blinded validation file
is frozen for a genuinely independent second reviewer; it is intentionally
unfilled. Until that review is returned, this is a development release rather
than an independently validated registry.

The secondary, noncausal performance audit found no clear association between
documented exact-dataset exposure and AUROC or AUPRC after model and task fixed
effects. This does not demonstrate absence of an exposure effect.

## Reproduce

From PowerShell with Python dependencies installed:

```powershell
powershell -ExecutionPolicy Bypass -File .\run_pipeline.ps1
```

Query a model–dataset pair with:

```powershell
python src\check_pretraining_overlap.py UNI tcga
```
