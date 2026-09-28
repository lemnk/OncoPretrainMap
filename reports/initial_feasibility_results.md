# Initial Feasibility Results

**Date:** 2026-09-27  
**Protocol:** v1

## Frozen discovery universe

The frozen PathBench repository contributed 32 model labels, 41 task records,
and 1,312 model–task result rows. The two source files were hashed before
derivation. The model table is a discovery source rather than final evidence;
every exposure assertion intended for release requires a primary paper, official
repository, model card, or identifier manifest.

## Dataset registry

The initial registry contains 31 dataset or corpus records and six explicit
parent–child lineage edges. Twenty-four datasets are in the initial evaluation
scope. This is a seed, not a claim of complete pathology-dataset coverage.

## Primary-source pilot

Fifteen primary-source assertions were entered for nine model versions:
CTransPath, Phikon, Phikon-v2, UNI, TITAN, Prov-GigaPath, Virchow, Virchow2, and
H-optimus-0. The sources include version-pinned official model cards,
version-pinned repositories, and peer-reviewed papers.

The development matrix contains 768 model–dataset pairs:

- 9 exact named-dataset exposures;
- 15 parent-repository exposures inferred through the lineage graph; and
- 744 pairs with no detected evidence or insufficient disclosure.

These counts are deliberately unfavorable: most model versions have not yet
completed primary-source extraction. They must not be interpreted as evidence
that 744 pairs are independent.

## Published-benchmark audit pilot

All 1,312 PathBench model–task rows were linked to canonical model identifiers.
TCGA and CPTAC rows were mapped at the repository level, and all eight named
public external tasks were resolved from their task labels. In total, 1,088
rows now have a canonical evaluation-dataset identifier. The 224 rows labeled
`Out of Domain` remain unresolved until their hospital cohorts are mapped from
the paper and supplements. This is a development audit, not a final contamination
estimate. Under the frozen rules,
64 rows had documented exact-dataset exposure and 1,248 remained D1 (no detected
evidence or insufficient disclosure). The 64 rows arose from CTransPath–TCGA
(19 tasks), Phikon–TCGA (19), Phikon-v2–TCGA (19), and Phikon-v2–CPTAC (7).
These counts describe disclosed exposure, not measured performance inflation.

## Software verification

Nine tests cover exact exposure, parent-repository lineage, multilevel lineage,
exact-identifier precedence, conflict flags, documented disjointness, and the
rule that missing evidence is not independence.

## Immediate next work

1. Complete primary-source extraction for the remaining 23 PathBench models.
2. Resolve the seven out-of-domain tasks to named cohorts and dataset versions.
3. Add a source-freeze downloader for papers and model cards where licensing
   permits local archival.
4. Preselect and freeze the blinded duplicate-extraction sample before reviewing
   its records.
5. Build the PathBench exposure audit and disclosure-completeness figures.
