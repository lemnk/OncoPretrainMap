# OncoPretrainMap Classification Guide

Use the strongest exposure class supported by public, checkpoint-specific
evidence. Missing disclosure is not evidence of independence. Evidence strength
is recorded separately from exposure scope.

## Exposure classes

- **D0 — documented disjoint:** a version-specific source explicitly excludes
  the evaluation dataset or cohort from model development.
- **D1 — unresolved or insufficiently disclosed:** public evidence does not
  establish D0 or D2-D4. D1 is not independence.
- **D2 — containing-repository exposure:** public evidence establishes that the
  development corpus contains the repository or cohort from which the
  evaluation set was drawn, but exact evaluated identifiers are unavailable.
- **D3 — exact named-dataset exposure:** the named evaluation dataset is
  explicitly included in model development, without exact case/slide/patch
  identifiers proving overlap.
- **D4 — exact case/slide/patch overlap:** released identifiers or equivalent
  evidence confirm that the same evaluation unit was used in model development.

Precedence is D4, D3, D2, D0, then D1. A conflict is retained when documented
exposure and documented disjointness coexist for the same checkpoint–dataset
relationship.

## Institutional co-provenance rule

**Same institution as the evaluation cohort, with no stated or demonstrated
corpus-containment relationship, is D1—not D2.** An institutional label defines
provenance, not set containment. A statement that overlap cannot be excluded may
be retained as `exposure_warning=overlap_cannot_be_excluded`, but the warning
does not establish D2-D4.

### Worked example

Virchow pretraining and the Campanella MSKCC evaluation cohorts share MSKCC
provenance. The benchmark source states that overlap cannot be excluded, but it
does not establish that the pretraining corpus contains those evaluation
cohorts. Therefore, the relationship is:

```text
Exposure class: D1 — unresolved or insufficiently disclosed
Exposure warning: overlap cannot be excluded
Not supported: D2 containing-repository exposure
```

This example was added after both initial extractors independently assigned D2.
A source-semantics audit showed that the assignment did not meet the frozen D2
definition. The clarification documents how to apply the unchanged rule to
Virchow2G, PLUTO, Atlas, H-optimus, and other institution-associated models; it
does not presume that any of them has the same evidence state.

## Minimum evidence questions

1. Is the model checkpoint/version resolved?
2. Is there an explicit, version-specific disjointness statement? If yes, D0
   unless stronger exposure evidence conflicts.
3. Are exact evaluation cases, slides, or patches confirmed in development? If
   yes, D4.
4. Is the exact named evaluation dataset explicitly in development? If yes, D3.
5. Is a containing repository or cohort relationship established? If yes, D2.
6. Otherwise assign D1, preserving any explicit overlap warning separately.

A source statement such as “most models were disjoint” establishes its claim at
aggregate scope. Without an enumerated checkpoint list, do not convert every
unnamed model to D0 in the primary registry. Document a row-level sensitivity
scenario if a broader reading could change the reported distribution.
