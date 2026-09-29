"""Conservative command-line interface for exposure records."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REGISTRY = ROOT / "data" / "derived" / "model_dataset_exposure_development.csv"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("model_id")
    parser.add_argument("evaluation_dataset_id")
    parser.add_argument("--registry", type=Path, default=DEFAULT_REGISTRY)
    args = parser.parse_args()
    if not args.registry.exists():
        print("Registry file not found; independence cannot be assessed.")
        return 2
    with args.registry.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    matches = [
        row
        for row in rows
        if row["model_id"].casefold() == args.model_id.casefold()
        and (
            row.get("evaluation_dataset_id")
            or row.get("canonical_evaluation_dataset_id", "")
        ).casefold()
        == args.evaluation_dataset_id.casefold()
    ]
    if not matches:
        print("No detected evidence; independence cannot be assumed.")
        return 1
    for row in matches:
        if row.get("registry_status"):
            print(f"Registry status: {row['registry_status']}")
        print(f"Exposure scope: {row['exposure_scope']}")
        warning = row.get("exposure_warning", "")
        if warning == "overlap_cannot_be_excluded":
            print("Exposure warning: overlap cannot be excluded; D2-D4 are not established.")
        else:
            print("Exposure warning: none recorded.")
        print(f"Evidence strength: {row['evidence_strength']}")
        print(f"Benchmark independence: {row['independence_statement']}")
        print(f"Source: {row['evidence_url']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
