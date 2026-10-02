# Protocol Deviations

## Independently frozen post-v2 transport extension

On 2026-09-28, after completion of the v2 development application, an authorized
external benchmark transport analysis was added. The D0-D4 rules and supporting
methodology were frozen at commit
`734b170839b1d97f79b3e58dba8d8b3f3943d70b` before detailed extraction of the
Campanella et al benchmark. The extension is not treated as part of the original
v1 protocol or as clinical validation. It is reported as a separately frozen
transport test of the provenance framework. No rule change was required after
opening the external benchmark.

## 2026-09-28 — Timing and documentation of duplicate extraction

Protocol v1 planned a prespecified held-out subset for blinded independent
extraction. Initial primary-source extraction for all 32 models was completed
before the deterministic 80-pair sample was frozen. The author had therefore
already encountered the source universe from which the sample was drawn.

The generated reviewer file omitted the development classifications. Caleb
Yitna Ref reviewed all 80 sampled relationships while blinded to those
classifications and did not use AI. After the review, the author integrated the
development and reviewer classifications into one comparison workbook. The
integrated workbook therefore displays both columns, but that post-review layout
does not describe what the reviewer saw during initial classification.

The sample remains unsuitable as an untouched validation set for developing the
rules because the author had already completed the source extraction before
sampling. It does provide a blinded second-reviewer agreement assessment for the
sampled relationships.

No analytical thresholds or exposure rules were changed because of this
deviation.

## 2026-09-28 — Campanella D2 application correction

An audit of the primary Campanella source found that its Virchow/MSKCC statement
established only that overlap could not be excluded. It did not establish that
the MSKCC pretraining corpus contained the evaluation cohorts. Under the frozen
D2 definition, the 12 affected relationships therefore remained D1 with an
explicit overlap-warning field. This corrected an application of the frozen
rule; it did not change the definition, evidence hierarchy, or precedence rule.
The prior labels, blinded reviewer decisions, corrected
classes, and adjudication notes were retained. External counts changed from 44
D0, 186 D1, and 12 D2 to 44 D0 and 198 D1.

The orthogonal value `exposure_warning=overlap_cannot_be_excluded` was added to
retain the primary source's warning without weakening D2. It means that a source
explicitly states that overlap cannot be excluded while available evidence does
not satisfy D2-D4. The relationship remains D1. This annotation does not alter
classification precedence.

The classification guide includes the existing boundary as a worked example: shared
institutional provenance without a stated or demonstrated corpus-containment
relationship is D1, not D2. The Virchow/MSKCC case is retained as a worked
example because both initial classifications overcalled it. This documents the
unchanged D2 requirement; it is not a new exposure class, rule revision, or
relaxation of the frozen rule.

## 2026-09-28 — Broad nonoverlap statement sensitivity

After the primary transport audit and human review, the version-of-record
Campanella discussion sentence that “most foundation models” lacked cohort
overlap was examined as a post hoc interpretation sensitivity. The primary
audit remains unchanged. Two scenarios assign the broad statement to six
other pathology foundation models, then additionally to the ImageNet tRes50
baseline. The article does not identify all checkpoints covered by “most,” so
these counts are explicitly hypothetical and are not new D0 evidence.

## 2026-09-28 — Benchmark-resolution sensitivity field

The registry classifies an explicit assertion for TCGA or CPTAC as D3 because
the named repository appears in model development. The published benchmark task
rows, however, do not provide identifiers for their exact evaluated subsets.
Reporting those rows as benchmark D3 would overstate the resolution of the
evidence. A post-protocol `benchmark_exposure_scope` field was therefore added:
TCGA and CPTAC rows are D2 unless exact evaluation-subset identifiers are
available, while the original registry class remains unchanged. This revision
changed the benchmark-resolution counts from 208 D3 rows to 204 D2 and four D3
rows. It was made to clarify evidence resolution, not in response to performance
results.

## 2026-09-29 — Post-correction rule-application challenge

After the Campanella source-semantics audit corrected the 12 D2 application
errors under the unchanged frozen definition, a second 80-relationship human-review challenge was added. The sample
was SHA-256 seeded, excluded every relationship in the two earlier review
packets, and was stratified as 10 D0, 37 D1, 28 D2, and five D3. The blank
packet and answer-key hash were frozen before review. Caleb Yitna Ref reviewed
the public sources while blinded to the key and reported no AI use. Agreement
was 80/80 (kappa, 1.00), with no D1-to-D2-D4 upgrades or D2-to-D1 downgrades.

This challenge was not part of protocol v1 and did not alter either benchmark
audit. It is reported as a post-correction assessment of rule application
within existing source families, not as a third independent benchmark,
registry-wide accuracy estimate, or D4 validation.
