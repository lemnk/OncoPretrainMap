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

The project is in the protocol-frozen registry-construction phase. The PathBench
core universe and source snapshot are reproducible. The development audit covers
all 1,312 published model–task rows: 121 currently have documented named-dataset
exposure, 52 are documented disjoint, and 1,139 remain unresolved. A primary
PanCancer40M manifest contains 6,093 exact training-slide identifiers, but no D4
claim is made without an independently sourced evaluation-slide manifest.
Primary-source extraction and independent blinded validation remain in progress.
