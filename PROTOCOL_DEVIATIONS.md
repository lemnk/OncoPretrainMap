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

An earlier project note incorrectly inferred nonblinding from the integrated
workbook and has been corrected. The sample remains unsuitable as an untouched
validation set for developing the rules because the author had already completed
the source extraction before sampling. It does provide a blinded second-reviewer
agreement assessment for the sampled relationships.

No analytical thresholds or exposure rules were changed because of this
deviation.

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
