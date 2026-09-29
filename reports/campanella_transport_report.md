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
| D1 | 198 | 81.8% | Unresolved; includes 12 explicit overlap warnings |
| D2 | 0 | 0% | No containing-corpus relationship established |
| D3 | 0 | 0% | No exact named evaluation-dataset exposure supported |
| D4 | 0 | 0% | No shared identifiers available |

The broad statement that “most foundation models” had no cohort overlap does
not enumerate covered checkpoints. A post hoc sensitivity assigning it to six
other pathology foundation models yielded 176 D0 (72.7%) and 66 D1 (27.3%).
Extending the assumption to the ImageNet tRes50 baseline yielded 198 D0 (81.8%)
and 44 D1 (18.2%). These are interpretation scenarios, not individually
verified disjointness. The source-specific primary audit remains 44 D0 and 198
D1. See `reports/campanella_blanket_statement_sensitivity.json` and the
row-level scenario file for reproducibility.

The 12 warning rows record the narrower public fact that the checkpoint used an
MSKCC pretraining corpus and the benchmark authors could not exclude overlap for
MSKCC tasks. They do not establish a containing corpus, shared patient, or
shared slide and therefore remain D1.

## Cross-benchmark interpretation

The Campanella distribution differed from the Bareja development application:
D0 was 18.2% versus 4.0%, D1 was 81.8% versus 80.2%, D2 was 0% versus 15.5%,
and D3 was 0% versus 0.3%. External application exercised only D0 and D1.
The definitions were unchanged; guidance on corpus containment was clarified
after review. External behavior of D2-D4 remains untested.

## Independent blinded review

A deterministic 60-row packet contained 20 D0 and 40 relationships ultimately
classified D1. Caleb Yitna Ref independently reviewed every row while blinded
to the initial transport classifications and reported no AI use. Initial
blinded inter-rater agreement was 58/60 (96.7%; kappa, 0.948). A subsequent source-semantics audit
corrected 12 Virchow/MSKCC rows from D2 to D1 because the evidence warned that
overlap could not be excluded but did not establish a containing-corpus
relationship. Concordance with the post-audit resolved classification was 46/60
(76.7%; descriptive kappa, 0.604). This is not a clean inter-rater reliability
statistic because the resolved classification was jointly adjudicated and
incorporated the reviewer's initial decisions. Original decisions and final
adjudications are retained.
