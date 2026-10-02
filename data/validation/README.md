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
decision columns after review. The blank packet was committed on September 28,
2026 before the completed workbook. Caleb completed the blank packet while
blinded to the development classifications. The side-by-side comparison was
created after his independent decisions were recorded and was not the review
interface. The review checked cited evidence and did not require an exhaustive
independent search for omitted assertions.

## Campanella external-transport review packet

`campanella_transport_blinded_review_packet.csv` contains the frozen blank
60-relationship sample from the separately frozen Campanella transport
analysis. It omits the development class and evidence grade.

`campanella_caleb_blinded_review_form.xlsx` is the formatted blank review form.
`campanella_caleb_blinded_review_completed.xlsx` contains Caleb Yitna Ref's
completed row-level review, the original reviewer decisions, the comparison
with the hidden key, final adjudications, and his dated attestation. Caleb was
blinded to the development classifications and reported no AI use. Agreement
with the initial labels was 58/60 (96.7%; unweighted Cohen's kappa, 0.948). A
subsequent source-semantics audit determined that the 12 Virchow/MSKCC warnings
did not establish a containing-corpus relationship and corrected those rows
from D2 to D1. Concordance with the post-audit resolved classification was
46/60 (76.7%; descriptive kappa, 0.604). The resolved classification was
jointly adjudicated, so this is not a second inter-rater reliability estimate.
The workbook preserves the original decisions and final adjudications. The
blank packet was committed before the completed workbook on September 28,
2026; no second pass is claimed.

## Challenge-80 post-clarification review

`challenge80_blinded_review_v1.xlsx` is a blank, frozen 80-relationship
challenge packet. Its reviewer instructions and prespecified analysis are in
`CHALLENGE80_REVIEW_INSTRUCTIONS.md` and `CHALLENGE80_ANALYSIS_PLAN.md`.
`challenge80_freeze_v1.json` records hashes of the packet, source tables,
classification guide, and prereview key commitment. No initial class or
evidence grade appears in the blank workbook. The packet contains only
relationships absent from both earlier review samples.

`challenge80_caleb_blinded_review_corrected_v1.xlsx` contains Caleb Yitna Ref's
completed review. An inherited editor-template label incorrectly identified the
reviewer and AI-use status; the administrative metadata were corrected based on
the sole author's report, while every row-level classification, evidence field,
URL, explanation, search log, date, and blinding entry was preserved. The
released key and row-level comparison retain the prereview classifications.
Caleb agreed on 80/80 relationships (kappa, 1.00): 10 D0, 37 D1, 28 D2, and
five D3. There were no D1-to-D2-D4 upgrades or D2-to-D1 downgrades. This is a
rule-reliability challenge using existing benchmark sources, not a new
independent benchmark, prevalence estimate, or D4 validation.
