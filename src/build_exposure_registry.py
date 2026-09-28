"""Derive model–dataset exposure classifications from curated assertions."""

from __future__ import annotations

import csv
import json
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CURATED = ROOT / "data" / "curated"
DERIVED = ROOT / "data" / "derived"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def ancestors(datasets: list[dict[str, str]]) -> dict[str, set[str]]:
    parent = {row["dataset_id"]: row["parent_dataset_id"] for row in datasets if row["parent_dataset_id"]}
    result: dict[str, set[str]] = defaultdict(set)
    for dataset_id in {row["dataset_id"] for row in datasets}:
        current = dataset_id
        seen: set[str] = set()
        while current in parent:
            current = parent[current]
            if current in seen:
                raise ValueError(f"Dataset-lineage cycle involving {dataset_id}")
            seen.add(current)
            result[dataset_id].add(current)
    return result


def classify(
    training_dataset: str | None,
    evaluation_dataset: str,
    lineage: dict[str, set[str]],
    documented_disjoint: bool = False,
    exact_identifier_overlap: bool = False,
) -> tuple[str, str, bool]:
    if exact_identifier_overlap:
        return "D4_exact_case_slide_or_patch_overlap", "A_identifier_manifest", documented_disjoint
    if training_dataset == evaluation_dataset and training_dataset:
        return "D3_exact_dataset_exposure", "B_explicit_primary_source_statement", documented_disjoint
    if training_dataset and training_dataset in lineage.get(evaluation_dataset, set()):
        return "D2_parent_repository_exposure", "C_lineage_inference", documented_disjoint
    if documented_disjoint:
        return "D0_documented_disjoint", "B_explicit_primary_source_statement", False
    return "D1_no_detected_evidence_or_insufficient_disclosure", "D_incomplete_or_ambiguous_disclosure", False


def main() -> None:
    datasets = read_csv(CURATED / "datasets.csv")
    lineage = ancestors(datasets)
    models = read_csv(DERIVED / "pathbench_model_universe.csv")
    scope = read_csv(CURATED / "evaluation_scope.csv")
    assertions = read_csv(CURATED / "model_dataset_assertions.csv")
    disjoint_rows = read_csv(CURATED / "documented_disjoint.csv")
    overlap_rows = read_csv(CURATED / "exact_overlap.csv")

    assertions_by_model: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in assertions:
        assertions_by_model[row["model_id"]].append(row)
    disjoint = {(row["model_id"], row["evaluation_dataset_id"]): row for row in disjoint_rows}
    overlaps = {(row["model_id"], row["evaluation_dataset_id"]): row for row in overlap_rows}

    output: list[dict[str, object]] = []
    for model in models:
        model_id = model["model_id"]
        model_assertions = assertions_by_model.get(model_id, [])
        for evaluation in scope:
            evaluation_id = evaluation["evaluation_dataset_id"]
            pair = (model_id, evaluation_id)
            exact_overlap = overlaps.get(pair)
            disjoint_row = disjoint.get(pair)
            exact_assertions = [row for row in model_assertions if row["dataset_id"] == evaluation_id]
            parent_assertions = [
                row for row in model_assertions
                if row["dataset_id"] in lineage.get(evaluation_id, set())
            ]
            conflict = False
            if exact_overlap:
                exposure_scope = "D4_exact_case_slide_or_patch_overlap"
                evidence_strength = "A_identifier_manifest"
                evidence_url = exact_overlap["evidence_url"]
                evidence_ids = exact_overlap["shared_identifier"]
                conflict = bool(disjoint_row)
                statement = "Exact shared content is documented; this benchmark is exposed."
            elif exact_assertions:
                exposure_scope = "D3_exact_dataset_exposure"
                evidence_strength = min(row["evidence_strength"] for row in exact_assertions)
                evidence_url = "; ".join(sorted({row["source_url"] for row in exact_assertions}))
                evidence_ids = "; ".join(row["assertion_id"] for row in exact_assertions)
                conflict = bool(disjoint_row)
                statement = "The named evaluation dataset is reported in model development; independence cannot be assumed."
            elif parent_assertions:
                exposure_scope = "D2_parent_repository_exposure"
                evidence_strength = "C_lineage_inference"
                evidence_url = "; ".join(sorted({row["source_url"] for row in parent_assertions}))
                evidence_ids = "; ".join(row["assertion_id"] for row in parent_assertions)
                conflict = bool(disjoint_row)
                statement = "A parent repository is reported in model development; exact slide exposure is unresolved."
            elif disjoint_row:
                exposure_scope = "D0_documented_disjoint"
                evidence_strength = disjoint_row["evidence_strength"]
                evidence_url = disjoint_row["evidence_url"]
                evidence_ids = "documented_disjoint"
                statement = "Version-specific disjointness is documented in the cited source."
            else:
                exposure_scope = "D1_no_detected_evidence_or_insufficient_disclosure"
                evidence_strength = "D_incomplete_or_ambiguous_disclosure"
                evidence_url = ""
                evidence_ids = ""
                statement = "No detected evidence; independence cannot be assumed."
            output.append(
                {
                    "model_id": model_id,
                    "model_name": model["display_name"],
                    "evaluation_dataset_id": evaluation_id,
                    "exposure_scope": exposure_scope,
                    "evidence_strength": evidence_strength,
                    "conflict_flag": str(conflict),
                    "independence_statement": statement,
                    "evidence_assertion_ids": evidence_ids,
                    "evidence_url": evidence_url,
                    "registry_status": "development_release_not_for_independence_certification",
                }
            )

    fields = list(output[0])
    write_csv(DERIVED / "model_dataset_exposure_development.csv", output, fields)
    counts: dict[str, int] = defaultdict(int)
    for row in output:
        counts[str(row["exposure_scope"])] += 1
    summary = {
        "dataset_records": len(datasets),
        "lineage_edges": sum(bool(row["parent_dataset_id"]) for row in datasets),
        "core_models": len(models),
        "evaluation_datasets": len(scope),
        "model_dataset_pairs": len(output),
        "primary_source_assertions": len(assertions),
        "models_with_primary_source_assertions": len(assertions_by_model),
        "model_source_coverage_percent": round(100 * len(assertions_by_model) / len(models), 1),
        "exposure_scope_counts": dict(sorted(counts.items())),
        "status": (
            "Development registry; initial primary-source extraction covers every core model, "
            "but identifier-level validation and independent duplicate extraction remain incomplete."
        ),
    }
    DERIVED.mkdir(parents=True, exist_ok=True)
    (DERIVED / "registry_build_summary.json").write_text(
        json.dumps(summary, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
