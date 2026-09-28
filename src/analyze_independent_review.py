"""Analyze a completed blinded duplicate-extraction file.

This script intentionally is not part of run_pipeline.ps1 because the released
sample is blank. Run it only on a real returned review file.
"""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "data" / "derived" / "model_dataset_exposure_development.csv"
ALLOWED = {
    "D0_documented_disjoint",
    "D1_no_detected_evidence_or_insufficient_disclosure",
    "D2_parent_repository_exposure",
    "D3_exact_dataset_exposure",
    "D4_exact_case_slide_or_patch_overlap",
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("review_file", type=Path)
    parser.add_argument("--output-dir", type=Path, default=ROOT / "reports" / "validation")
    args = parser.parse_args()

    reviews = read_csv(args.review_file)
    if len(reviews) != 80:
        raise ValueError(f"Expected 80 review rows, found {len(reviews)}")
    invalid = [row["audit_row"] for row in reviews if row["reviewer_exposure_scope"] not in ALLOWED]
    if invalid:
        raise ValueError(f"Missing or invalid reviewer classifications in rows: {invalid}")
    if any(not row["reviewer_label"] or not row["review_date"] for row in reviews):
        raise ValueError("Every row requires reviewer_label and review_date")

    registry = {
        (row["model_id"], row["evaluation_dataset_id"]): row["exposure_scope"]
        for row in read_csv(REGISTRY)
    }
    paired = []
    for row in reviews:
        key = (row["model_id"], row["evaluation_dataset_id"])
        if key not in registry:
            raise ValueError(f"Unknown pair in review file: {key}")
        paired.append((registry[key], row["reviewer_exposure_scope"]))

    labels = sorted(ALLOWED)
    confusion = Counter(paired)
    n = len(paired)
    observed = sum(first == second for first, second in paired) / n
    first_counts = Counter(first for first, _ in paired)
    second_counts = Counter(second for _, second in paired)
    expected = sum(first_counts[label] * second_counts[label] for label in labels) / (n * n)
    kappa = (observed - expected) / (1 - expected) if expected < 1 else float("nan")

    args.output_dir.mkdir(parents=True, exist_ok=True)
    with (args.output_dir / "independent_review_confusion_matrix.csv").open(
        "w", encoding="utf-8", newline=""
    ) as handle:
        writer = csv.writer(handle)
        writer.writerow(["development_class/reviewer_class", *labels])
        for first in labels:
            writer.writerow([first, *[confusion[(first, second)] for second in labels]])

    summary = {
        "review_file": str(args.review_file.resolve()),
        "rows": n,
        "exact_agreement_count": round(observed * n),
        "exact_agreement_proportion": observed,
        "unweighted_cohens_kappa": kappa,
        "development_class_counts": dict(sorted(first_counts.items())),
        "reviewer_class_counts": dict(sorted(second_counts.items())),
        "initially_blinded_values": dict(sorted(Counter(row["initially_blinded"] for row in reviews).items())),
        "note": "Agreement describes duplicate extraction; it is not diagnostic accuracy against a gold standard.",
    }
    (args.output_dir / "independent_review_summary.json").write_text(
        json.dumps(summary, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
