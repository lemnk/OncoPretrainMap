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
23 D3. Caleb was blinded to the development classifications during his initial
review and reported no AI use. The integrated workbook retains both original
decision columns after review; their later side-by-side display does not describe
what the reviewer saw during initial classification.

## Campanella external-transport review packet

`campanella_transport_blinded_review_packet.csv` contains the frozen blank
60-relationship sample from the separately frozen Campanella transport
analysis. It omits the development class and evidence grade.

`campanella_caleb_blinded_review_form.xlsx` is the formatted blank review form.
`campanella_caleb_blinded_review_completed.xlsx` contains Caleb Yitna Ref's
completed row-level review, the original reviewer decisions, the comparison
with the hidden key, final adjudications, and his dated attestation. Caleb was
blinded to the development classifications and reported no AI use. Agreement
was 58/60 (96.7%; unweighted Cohen's kappa, 0.948): 20/20 for D0, 26/28 for D1,
and 12/12 for D2. No sampled D1 relationship was upgraded to D2-D4. The two
disagreements involved tRes50 rows classified by Caleb as D0; final adjudication
retained D1 because the frozen rule required an explicit version-specific
exclusion.
