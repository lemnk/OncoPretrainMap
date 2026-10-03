"""Compare the registry with exact-name direct-source reading baseline."""

from __future__ import annotations

import csv
import json
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CURATED = ROOT / "data" / "curated"
DERIVED = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"

D0 = "D0_documented_disjoint"
D1 = "D1_no_detected_evidence_or_insufficient_disclosure"
D2 = "D2_parent_repository_exposure"
D3 = "D3_exact_dataset_exposure"
D4 = "D4_exact_case_slide_or_patch_overlap"
ORDER = [D0, D1, D2, D3, D4]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fields: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows and fields is None:
        raise ValueError(f"No rows for {path}")
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields or list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    registry = read_csv(DERIVED / "model_dataset_exposure_development.csv")
    assertions = read_csv(CURATED / "model_dataset_assertions.csv")
    disjoint = read_csv(CURATED / "documented_disjoint.csv")
    overlaps = read_csv(CURATED / "exact_overlap.csv")

    asserted: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
    for row in assertions:
        asserted[(row["model_id"], row["dataset_id"])].append(row)
    disjoint_pairs = {(row["model_id"], row["evaluation_dataset_id"]) for row in disjoint}
    overlap_pairs = {(row["model_id"], row["evaluation_dataset_id"]) for row in overlaps}

    pair_rows: list[dict[str, object]] = []
    for row in registry:
        pair = (row["model_id"], row["evaluation_dataset_id"])
        if pair in overlap_pairs:
            baseline = D4
            basis = "exact identifier-overlap record"
        elif pair in asserted:
            baseline = D3
            basis = "exact named-dataset development assertion"
        elif pair in disjoint_pairs:
            baseline = D0
            basis = "exact named-dataset disjointness assertion"
        else:
            baseline = D1
            basis = "no exact named-dataset assertion"
        registry_class = row["exposure_scope"]
        pair_rows.append(
            {
                "model_id": row["model_id"],
                "model_name": row["model_name"],
                "evaluation_dataset_id": row["evaluation_dataset_id"],
                "direct_source_baseline_class": baseline,
                "baseline_basis": basis,
                "registry_class": registry_class,
                "agreement": baseline == registry_class,
                "registry_evidence_assertion_ids": row["evidence_assertion_ids"],
                "registry_evidence_url": row["evidence_url"],
                "lineage_added_exposure": baseline == D1 and registry_class in {D2, D3, D4},
            }
        )
    write_csv(DERIVED / "direct_source_baseline_pairs.csv", pair_rows)

    confusion = Counter(
        (str(row["direct_source_baseline_class"]), str(row["registry_class"]))
        for row in pair_rows
    )
    confusion_rows = [
        {
            "direct_source_baseline_class": baseline,
            "registry_class": registry_class,
            "pair_count": confusion[(baseline, registry_class)],
        }
        for baseline in ORDER
        for registry_class in ORDER
        if confusion[(baseline, registry_class)]
    ]
    write_csv(REPORTS / "direct_source_baseline_confusion.csv", confusion_rows)

    audit = read_csv(DERIVED / "pathbench_exposure_audit_development.csv")
    baseline_by_pair = {
        (str(row["model_id"]), str(row["evaluation_dataset_id"])): str(row["direct_source_baseline_class"])
        for row in pair_rows
    }
    benchmark_rows: list[dict[str, object]] = []
    for row in audit:
        pair = (row["model_id"], row["canonical_evaluation_dataset_id"])
        baseline = baseline_by_pair.get(pair, D1)
        baseline_at_benchmark_resolution = baseline
        if baseline == D3 and row["canonical_evaluation_dataset_id"] in {"tcga", "cptac"}:
            baseline_at_benchmark_resolution = D2
        registry_at_benchmark_resolution = row["benchmark_exposure_scope"]
        benchmark_rows.append(
            {
                "model_label": row["model_label"],
                "model_id": row["model_id"],
                "task_id": row["task_id"],
                "canonical_evaluation_dataset_id": row["canonical_evaluation_dataset_id"],
                "direct_source_baseline_class": baseline_at_benchmark_resolution,
                "registry_class": registry_at_benchmark_resolution,
                "agreement": baseline_at_benchmark_resolution == registry_at_benchmark_resolution,
            }
        )
    write_csv(DERIVED / "pathbench_direct_source_baseline_comparison.csv", benchmark_rows)

    baseline_counts = Counter(str(row["direct_source_baseline_class"]) for row in pair_rows)
    registry_counts = Counter(str(row["registry_class"]) for row in pair_rows)
    benchmark_baseline_counts = Counter(str(row["direct_source_baseline_class"]) for row in benchmark_rows)
    benchmark_registry_counts = Counter(str(row["registry_class"]) for row in benchmark_rows)
    lineage_rows = [row for row in pair_rows if row["lineage_added_exposure"]]
    benchmark_changes = [row for row in benchmark_rows if not row["agreement"]]
    summary = {
        "protocol": "DIRECT_SOURCE_BASELINE_PLAN.md",
        "registry_pair_universe": len(pair_rows),
        "direct_source_baseline_counts": dict(sorted(baseline_counts.items())),
        "registry_counts": dict(sorted(registry_counts.items())),
        "pair_level_exact_agreement": sum(bool(row["agreement"]) for row in pair_rows),
        "pair_level_exact_agreement_proportion": sum(bool(row["agreement"]) for row in pair_rows) / len(pair_rows),
        "lineage_added_exposure_pairs": len(lineage_rows),
        "lineage_added_exposure_examples": [
            {
                "model_id": row["model_id"],
                "evaluation_dataset_id": row["evaluation_dataset_id"],
                "registry_class": row["registry_class"],
                "assertion_ids": row["registry_evidence_assertion_ids"],
            }
            for row in lineage_rows[:10]
        ],
        "published_benchmark_rows": len(benchmark_rows),
        "published_benchmark_direct_source_counts": dict(sorted(benchmark_baseline_counts.items())),
        "published_benchmark_registry_counts": dict(sorted(benchmark_registry_counts.items())),
        "published_benchmark_changed_rows": len(benchmark_changes),
        "published_benchmark_exact_agreement": len(benchmark_rows) - len(benchmark_changes),
        "interpretation": (
            "The exact-name baseline isolates lineage traversal after canonical identifiers are supplied. "
            "It does not measure manual search time, source completeness, or expert review accuracy. "
            "Identical benchmark classifications indicate workflow/provenance value rather than incremental class discovery."
        ),
    }
    (REPORTS / "direct_source_baseline_summary.json").write_text(
        json.dumps(summary, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
