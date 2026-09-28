"""Annotate the published Bareja et al result matrix with exposure evidence."""

from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

TASK_DATASET_MAP = {
    "BACH": "bach",
    "BRACS": "bracs",
    "BreakHis": "breakhis",
    "LC25000": "lc25000",
    "MHIST": "mhist",
    "NCT-CRC-HE": "nct_crc_he_100k",
    "SICAPv2": "sicapv2",
    "UniToPatho": "unitopatho",
    "brain necrosis": "stanford_gbm",
    "lung grade": "nlst",
    "lung hist OOD1": "stanford_lung",
    "lung hist OOD2": "dhmc_lung",
    "lung stage OOD": "stanford_lung",
    "lung stage": "nlst",
    "MGMT OOD": "stanford_gbm",
}


def canonical_dataset_id(dataset_group: str, task_name: str) -> str:
    if dataset_group == "TCGA":
        return "tcga"
    if dataset_group == "CPTAC":
        return "cptac"
    return TASK_DATASET_MAP.get(task_name, "")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def main() -> None:
    matrix = read_csv(ROOT / "data" / "derived" / "pathbench_model_task_matrix.csv")
    task_names = {
        row["task_id"]: row["task_name"]
        for row in read_csv(ROOT / "data" / "derived" / "pathbench_task_universe.csv")
    }
    aliases = {
        row["pathbench_model_label"]: row["model_id"]
        for row in read_csv(ROOT / "data" / "curated" / "pathbench_model_aliases.csv")
    }
    registry = {
        (row["model_id"], row["evaluation_dataset_id"]): row
        for row in read_csv(ROOT / "data" / "derived" / "model_dataset_exposure_development.csv")
    }
    unknown_labels = sorted({row["model_label"] for row in matrix} - set(aliases))
    if unknown_labels:
        raise ValueError(f"Unmapped benchmark model labels: {unknown_labels}")

    annotated: list[dict[str, object]] = []
    for row in matrix:
        model_id = aliases[row["model_label"]]
        task_name = task_names[row["task_id"]]
        dataset_id = canonical_dataset_id(row["dataset_group"], task_name)
        evidence = registry.get((model_id, dataset_id)) if dataset_id else None
        if evidence:
            scope = evidence["exposure_scope"]
            strength = evidence["evidence_strength"]
            statement = evidence["independence_statement"]
            resolvable = "Yes"
        else:
            scope = "D1_no_detected_evidence_or_insufficient_disclosure"
            strength = "D_incomplete_or_ambiguous_disclosure"
            statement = "Benchmark dataset label is too coarse or exposure evidence is incomplete; independence cannot be assumed."
            resolvable = "No"
        benchmark_scope = scope
        benchmark_statement = statement
        if scope == "D3_exact_dataset_exposure" and dataset_id in {"tcga", "cptac"}:
            benchmark_scope = "D2_parent_repository_exposure"
            benchmark_statement = (
                "The model reports exposure to the containing TCGA or CPTAC repository, but the "
                "published benchmark row does not provide identifiers sufficient to establish "
                "exposure to its exact evaluation subset."
            )
        annotated.append(
            {
                **row,
                "model_id": model_id,
                "canonical_evaluation_dataset_id": dataset_id,
                "dataset_label_resolvable": resolvable,
                "exposure_scope": scope,
                "benchmark_exposure_scope": benchmark_scope,
                "evidence_strength": strength,
                "independence_statement": statement,
                "benchmark_independence_statement": benchmark_statement,
            }
        )

    output = ROOT / "data" / "derived" / "pathbench_exposure_audit_development.csv"
    with output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(annotated[0]))
        writer.writeheader()
        writer.writerows(annotated)

    group_counts = Counter(row["dataset_group"] for row in annotated)
    exposure_counts = Counter(row["exposure_scope"] for row in annotated)
    benchmark_exposure_counts = Counter(row["benchmark_exposure_scope"] for row in annotated)
    resolvable_counts = Counter(row["dataset_label_resolvable"] for row in annotated)
    summary = {
        "published_model_task_rows": len(annotated),
        "models": len({row["model_id"] for row in annotated}),
        "tasks": len({row["task_id"] for row in annotated}),
        "dataset_group_counts": dict(sorted(group_counts.items())),
        "dataset_label_resolvable_counts": dict(sorted(resolvable_counts.items())),
        "exposure_scope_counts": dict(sorted(exposure_counts.items())),
        "benchmark_exposure_scope_counts": dict(sorted(benchmark_exposure_counts.items())),
        "interpretation": (
            "The registry evidence class is retained in exposure_scope. The benchmark-resolution sensitivity "
            "in benchmark_exposure_scope treats TCGA and CPTAC assertions as repository-level exposure because "
            "the published task rows do not provide exact evaluation-subset identifiers. D1 is not evidence of independence."
        ),
    }
    summary_path = ROOT / "reports" / "pathbench_exposure_audit_development.json"
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
