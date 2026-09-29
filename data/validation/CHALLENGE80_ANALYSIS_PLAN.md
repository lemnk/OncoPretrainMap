# Challenge-80 analysis plan, frozen before reviewer decisions

This packet probes whether independent source search and the clarified
containing-corpus rule reduce the earlier D1/D2 failure. The source universe is
the development registry and the Campanella transport audit at commit
`ff1599c3e0464341496ac821b1115d61475da994`. No relationship in either
prior human-review packet is reused. Selection is SHA-256 seeded and
class-stratified; pairs are not a random sample of the full registry and must
not be used to estimate exposure prevalence, population accuracy, or patient-
level leakage.

The reviewer sees only the blank workbook and reviewer instructions. The
private `challenge80_key_v1.json` remains gitignored until the completed,
dated decisions are returned. Source/class assignments and the key may then
be released with both initial and resolved decisions preserved. Because the
public repository contains the original registry, procedural blinding must be
documented rather than assumed.

## Locked analysis

1. Check all 80 records for a class, evidence grade, source URL or explicit
   source-unavailable note, reason, independent search log, reviewer identity,
   date, and blinding/AI-use fields. Missing fields remain missing; do not
   silently complete them from the key.
2. Compare the reviewer's **initial** classes to the frozen initial classes
   in a full D0–D4 confusion matrix. Report exact agreement, descriptive
   unweighted Cohen kappa, and per-initial-class agreement with denominators.
   Because pairs share model sources and the design is stratified, do not
   present overall kappa as registry-wide reliability.
3. Specifically count initial D1 rows upgraded by the reviewer to D2–D4
   (candidate missed exposures), and initial D2 rows downgraded to D1
   (candidate unsupported containment). Review each of those against the
   primary quoted source and the institutional co-provenance rule. Report
   evidence grade and checkpoint-resolution discrepancies separately.
4. Conduct a source-semantics audit of every initial or reviewer D2/D3 row,
   and a prespecified source-search check of at least 10 D1 rows spanning
   different model families. Preserve the auditor, date, links, original
   decisions, final resolution, and reason. A single-author resolution is
   explicitly labeled as such; it is not an independent gold standard. If a
   third reviewer is available, have that person audit the disputed cases
   while blinded to both initial labels.
5. Report pair-level results and a model-family summary so repeated task
   rows sharing one model disclosure are not treated as independent
   replications. Show all failures, including any D1/D2 errors. Do not revise
   the original classification rules or overwrite either previous analysis.

The packet contains no known D4-positive validation set. Agreement here would
not establish D4 detection, clinical model validity, or performance effects.
A separate benchmark with public positive exposure evidence, and separately a
matched training/evaluation manifest, remain needed for those claims.

