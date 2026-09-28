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

`campanella_transport_blinded_review_packet.csv` contains a deterministic
60-relationship sample from the separately frozen Campanella transport
analysis. It omits the development class and evidence grade. A reviewer must
inspect the linked primary records without AI, complete every blank reviewer
field, and return the file before the separate key is opened. The reviewer must
enter `No` in `reviewer_used_ai` to certify that requirement. No external-
transport agreement statistic is reported while these fields remain blank.

`campanella_caleb_blinded_review_form.xlsx` is the formatted Excel version of
the same blank packet. It contains instructions, controlled class/evidence
lists, and no development decisions. It is the correct file for a human blinded
review; AI-generated decisions must not be transferred into it or attributed to
a human reviewer.
