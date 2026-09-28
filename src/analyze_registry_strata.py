"""Summarize exposure classes by pathology-specific versus general models."""

from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def main() -> None:
    models = {
        row["model_id"]: row
        for row in read_csv(ROOT / "data" / "derived" / "pathbench_model_universe.csv")
    }
    registry = read_csv(ROOT / "data" / "derived" / "model_dataset_exposure_development.csv")
    audit = read_csv(ROOT / "data" / "derived" / "pathbench_exposure_audit_development.csv")

    def stratum(row: dict[str, str]) -> str:
        category = models[row["model_id"]]["model_category"]
        return "Pathology-specific" if category.startswith("Pathology") else "General-purpose"

    outputs = []
    summary: dict[str, object] = {
        "model_counts": dict(sorted(Counter(stratum({"model_id": key}) for key in models).items())),
        "registry": {},
        "benchmark_audit": {},
    }
    for table_name, rows in (("registry", registry), ("benchmark_audit", audit)):
        counts = Counter((stratum(row), row["exposure_scope"]) for row in rows)
        table_summary = {}
        for group in ("Pathology-specific", "General-purpose"):
            total = sum(value for (candidate, _), value in counts.items() if candidate == group)
            class_counts = {
                exposure: counts[(group, exposure)]
                for exposure in sorted({row["exposure_scope"] for row in rows})
            }
            table_summary[group] = {
                "total": total,
                "class_counts": class_counts,
                "d1_percent": round(
                    100 * class_counts.get("D1_no_detected_evidence_or_insufficient_disclosure", 0) / total,
                    1,
                ),
            }
            for exposure, count in class_counts.items():
                outputs.append(
                    {
                        "table": table_name,
                        "model_stratum": group,
                        "exposure_scope": exposure,
                        "count": count,
                        "percent_within_stratum": round(100 * count / total, 1),
                    }
                )
        summary[table_name] = table_summary

    cptac_d3 = [
        row for row in audit
        if row["dataset_group"] == "CPTAC" and row["exposure_scope"] == "D3_exact_dataset_exposure"
    ]
    summary["cptac_cross_check"] = {
        "d3_rows": len(cptac_d3),
        "models": dict(sorted(Counter(row["model_id"] for row in cptac_d3).items())),
        "expected_models_present": sorted({row["model_id"] for row in cptac_d3}) == ["gpfm", "phikon_v2"],
    }

    report_csv = ROOT / "reports" / "exposure_by_model_stratum.csv"
    with report_csv.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(outputs[0]))
        writer.writeheader()
        writer.writerows(outputs)
    (ROOT / "reports" / "exposure_by_model_stratum.json").write_text(
        json.dumps(summary, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
