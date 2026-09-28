# Project Plan

## Phase 1 — Freeze the study

- Freeze the discovery date and core 32-model universe.
- Record source repository commits and document hashes.
- Freeze exposure and evidence taxonomies.
- Define versioning and dataset-lineage rules.

## Phase 2 — Build the registry

- Extract model versions and primary sources.
- Extract pretraining, fine-tuning, distillation, and evaluation datasets
  separately.
- Create canonical dataset records and alias mappings.
- Create repository → cohort → slide subset → patch derivative lineage edges.
- Store every assertion with a source URL, source version, retrieval date,
  evidence excerpt, and curator status.

## Phase 3 — Validate

- Unit-test aliases, lineages, conflict handling, and checker language.
- Double-extract a prespecified held-out set with a blinded second reviewer.
- Report exact agreement and Cohen's kappa where independence is genuine.
- Confirm a gold-standard subset using public case or slide manifests.
- Use post-cutoff or explicitly disjoint datasets as negative controls.

## Phase 4 — Benchmark audit

- Map every PathBench model–dataset combination to an exposure class.
- Quantify documented exposure, documented disjointness, and insufficient
  disclosure.
- Compare TCGA and non-TCGA claims without rerunning foundation models.
- If result files support it, perform an exposure-stratified sensitivity analysis
  of reported rankings without implying causation.

## Phase 5 — Release and manuscript

- Freeze release tables, hashes, tests, figures, and checker output.
- Archive a numbered release.
- Draft a Resource Report centered on evaluation validity and oncology AI
  governance.

