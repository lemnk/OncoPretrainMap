# Independent review package

`independent_review_sample_v1.csv` is a deterministic 80-pair duplicate-
extraction sample. It was generated after the initial registry extraction, so it
must not be described as a held-out threshold-development set.

The second reviewer should independently search the primary paper, supplement,
official model card, official repository, and public identifier manifests for
each model–dataset pair. The reviewer must not inspect the derived exposure
registry until all initial decisions are saved.

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

Original reviewer decisions must be preserved. After unblinding, disagreements
may be discussed, but the initial decisions and a resolution note must remain in
the final audit file. Without a third reviewer, unresolved cases remain
unresolved instead of being forced into agreement.

## AI-assisted verification

`ai_assisted_review_v1.xlsx` is a separate, explicitly labeled AI review. OpenAI
Codex GPT-5.6 Sol re-derived all 80 classifications from the frozen curated
assertions, disjointness records, and lineage rules and agreed on 80/80 pairs.
The AI had access to the repository and was not blinded. This workbook documents
software-rule reproduction from the same evidence and must not be represented as
independent human validation.
