# Frozen Protocol: Independent Benchmark Transport

Protocol date: 2026-09-28  
OncoPretrainMap rule freeze: Git commit `734b170839b1d97f79b3e58dba8d8b3f3943d70b`  
External benchmark: Campanella et al., *A clinical benchmark of public self-supervised pathology foundation models*, Nature Communications 16, 3640 (2025), DOI `10.1038/s41467-025-58796-1`  
Official benchmark repository freeze: `sinai-computational-pathology/SSL_tile_benchmarks`, commit `fbdf07f932d7302fd7bcb4a1e6b78bfb9d4a71f9`

## Purpose

This analysis tests whether the already-frozen OncoPretrainMap provenance framework can be transported to a benchmark created by an independent research group. It is an external transport test of the provenance-auditing framework, not clinical validation of a prediction model and not an estimate of contamination prevalence.

## Frozen rules

The D0-D4 exposure definitions, A-D evidence grades, dataset-lineage rules, precedence rules, conflict handling, and the rule that missing evidence is not independence are frozen at the OncoPretrainMap commit above. They will not be modified after detailed extraction of the external benchmark.

- D0: documented disjointness relevant to the evaluated model/checkpoint and benchmark cohort.
- D1: no detected evidence or insufficient disclosure.
- D2: exposure to a containing parent repository or institution-level corpus when exact benchmark-cohort membership is not established.
- D3: explicit exposure to the named evaluation dataset/cohort.
- D4: exact shared case, slide, patch, or content-hash identifiers.

Exposure scope and evidence strength remain separate. Institutional co-location alone is not exact overlap. A published exclusion or nonoverlap statement may support D0 only at the scope and version actually documented.

## Frozen external universe

The external universe is every distinct model/checkpoint-by-clinical-task result reported in the version-of-record article and its source-data archive, reconciled to the official repository commit above. Duplicate plotting rows, summaries, and ensembles that are not independently evaluated model/checkpoints will be excluded with a recorded reason.

## Prespecified workflow

1. Archive the benchmark citation, official repository revision, and source-data hashes.
2. Extract model/checkpoint labels, clinical tasks, contributing institution, evaluation cohort label, and reported result availability.
3. Resolve model/checkpoint and dataset aliases without changing the frozen normalization rules. Record unresolved labels rather than inventing mappings.
4. Apply the frozen D0-D4 and A-D rules to each model-task relationship.
5. Retain the original source assertion, inference path, conflict flag, and constrained independence statement.
6. Report canonical mapping success, D0-D4 counts and percentages, pathology-specific/general-purpose strata where applicable, unresolved mappings, conflicts, and any previously unmodeled lineage situation.
7. Compare the external transport results descriptively with the Bareja et al. application. No new performance regression is prespecified.
8. Generate a deterministic review sample for a blinded second human reviewer. Until returned, any second-reviewer reliability estimate will be explicitly marked pending and will not be fabricated.

## Success and failure criteria

Transport is considered technically successful if the frozen code and definitions can represent every relationship, even when the appropriate result is D1. Mapping failures and newly encountered lineage structures are outcomes, not reasons to alter the rules. Any necessary rule change will be logged as a post-freeze deviation and the original frozen-rule result will be preserved.

## Claims not permitted

The analysis will not claim that D1 means independent, that D2-D3 proves performance inflation, that institution-level exposure proves shared patients, or that two benchmarks establish universal coverage of pathology foundation models.
