# Independent Benchmark Transport Report

## Design

The OncoPretrainMap v2 classification framework was frozen at Git commit
`734b170839b1d97f79b3e58dba8d8b3f3943d70b` before detailed extraction of the
Campanella et al clinical benchmark. D0-D4 definitions, A-D evidence grades,
lineage rules, precedence, conflict handling, and the rule that missing evidence
is not independence were unchanged.

The external benchmark is Campanella et al, *Nature Communications* 2025,
DOI `10.1038/s41467-025-58796-1`. The official repository was pinned at commit
`fbdf07f932d7302fd7bcb4a1e6b78bfb9d4a71f9`. The publisher source-data archive
was verified by SHA-256
`0b1309f282352d15e3c13835539499a1fdb23febecf76c2148be8735b8dd14aa`.

## Results

The source tables contained 11 encoders, 22 clinical tasks, and 242 distinct
model–task relationships. All 242 mapped to canonical identifiers. No exposure
rule changed, no new class was introduced, and no conflict was recorded.

| Class | Rows | Percent | Interpretation |
|---|---:|---:|---|
| D0 | 44 | 18.2% | Explicit benchmark nonoverlap for SP22M/SP85M |
| D1 | 186 | 76.9% | Unresolved; not evidence of independence |
| D2 | 12 | 5.0% | Virchow/Virchow2 MSKCC containing-corpus exposure |
| D3 | 0 | 0% | No exact named evaluation-dataset exposure supported |
| D4 | 0 | 0% | No shared identifiers available |

The D2 result does not demonstrate that an evaluation patient or slide was used
in pretraining. It records the narrower public fact that the checkpoint used an
MSKCC pretraining corpus and the benchmark authors could not exclude overlap for
MSKCC tasks.

## Cross-benchmark interpretation

The Campanella distribution differed from the Bareja development application:
D0 was 18.2% versus 4.0%, D2 was 5.0% versus 15.5%, D3 was 0% versus 0.3%, and
D1 was 76.9% versus 80.2%. The important result is not equality of percentages;
it is successful representation of a different benchmark ecosystem without a
methodological rule change.

## Independent blinded review

A deterministic 60-row packet contained 20 D0, 28 D1, and all 12 D2
relationships. Caleb Yitna Ref independently reviewed every row while blinded
to the transport classifications and reported no AI use. Agreement was 58/60
(96.7%; unweighted Cohen's kappa, 0.948): 20/20 for D0, 26/28 for D1, and 12/12
for D2. No D1 relationship was upgraded to D2-D4. The two tRes50 disagreements
were adjudicated as D1 under the frozen requirement for an explicit
version-specific exclusion.
