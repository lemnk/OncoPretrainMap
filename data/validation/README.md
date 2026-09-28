# Human review package

`independent_review_sample_v1.csv` is a deterministic 80-pair duplicate-
extraction sample. It was generated after the initial registry extraction, so it
must not be described as a held-out threshold-development set.

The blank CSV preserves the originally generated review sample. The completed
human review is stored in `caleb_review_completed.xlsx`.

Allowed exposure values are exactly:

- `D0_documented_disjoint`
- `D1_no_detected_evidence_or_insufficient_disclosure`
- `D2_parent_repository_exposure`
- `D3_exact_dataset_exposure`
- `D4_exact_case_slide_or_patch_overlap`

Allowed evidence-strength values are exactly:

- `A_identifier_manifest`
- `B_explicit_primary_source_statement`
- `C_lineage_inference`
- `D_incomplete_or_ambiguous_disclosure`

Caleb Yitna Ref reviewed all 80 pairs and recorded the decision, evidence
strength, source URLs, explanation, identity, date, and blinding status. The
review agreed with all 80 development classifications: 11 D0, 23 D1, 23 D2, and
23 D3. The workbook displayed the development classifications and therefore
records `initially_blinded` as `No`. The result is human verification of every
sampled record, not an unbiased blinded inter-rater reliability estimate.
