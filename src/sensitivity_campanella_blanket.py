"""Post hoc sensitivity to the benchmark paper's broad nonoverlap statement.

This analysis leaves the source-specific transport classification untouched.
The paper says "most foundation models" had no overlap, without identifying
every covered checkpoint. The scenarios deliberately assign that sentence to
specified labels to show how much the D0/D1 distribution depends on its scope.
"""

from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "data" / "derived" / "campanella_transport_audit.csv"
OUTPUT = ROOT / "data" / "derived" / "campanella_blanket_statement_sensitivity.csv"
SUMMARY = ROOT / "reports" / "campanella_blanket_statement_sensitivity.json"
SOURCE = "https://www.nature.com/articles/s41467-025-58796-1"

D0 = "D0_documented_disjoint"
D1 = "D1_no_detected_evidence_or_insufficient_disclosure"
FOUNDATION_MODELS = {
    "CTransPath",
    "Phikon",
    "Phikon-v2",
    "Prov-GigaPath",
    "UNI",
    "h-optimus-0",
}
BASELINE = "tRes50"


def main() -> None:
    with AUDIT.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if len(rows) != 242 or len({r["transport_row_id"] for r in rows}) != 242:
        raise ValueError("Expected 242 unique external transport relationships")
    if {r["model_label"] for r in rows if r["model_label"] in FOUNDATION_MODELS} != FOUNDATION_MODELS:
        raise ValueError("The six scenario model labels were not all observed")

    scenarios = {
        "source_specific_primary": set(),
        "blanket_six_foundation_models": FOUNDATION_MODELS,
        "blanket_six_plus_tres50": FOUNDATION_MODELS | {BASELINE},
    }
    output_rows = []
    summary = {
        "analysis_status": "Post hoc sensitivity; primary transport classifications are unchanged.",
        "source_url": SOURCE,
        "source_scope_limit": "The article says most foundation models had no cohort overlap but does not identify every checkpoint covered by that statement.",
        "evidence_grade_interpretation": "The published nonoverlap sentence is an explicit primary-source statement (grade B) at aggregate scope. Assigning it to an unnamed checkpoint is a hypothetical scenario and is not independently grade B evidence for that checkpoint.",
        "scenario_interpretation": "Hypothetical assignment of the broad statement to specified model labels; not new checkpoint-specific D0 evidence.",
        "scenarios": {},
    }
    for name, additional_models in scenarios.items():
        counts: Counter[str] = Counter()
        changed = 0
        for row in rows:
            label = row["model_label"]
            primary = row["exposure_scope"]
            eligible = primary == D1 and label in additional_models
            scenario_class = D0 if eligible else primary
            changed += int(eligible)
            counts[scenario_class] += 1
            output_rows.append(
                {
                    "scenario": name,
                    "transport_row_id": row["transport_row_id"],
                    "model_label": label,
                    "task_id": row["task_id"],
                    "primary_class": primary,
                    "scenario_class": scenario_class,
                    "assumption_used": "broad_nonoverlap_statement" if eligible else "source_specific_primary",
                    "exposure_warning": row["exposure_warning"],
                }
            )
        summary["scenarios"][name] = {
            "rows": len(rows),
            "models_assumed_covered": sorted(additional_models),
            "reassigned_d1_to_d0": changed,
            "class_counts": dict(sorted(counts.items())),
            "class_percentages": {key: round(value * 100 / len(rows), 1) for key, value in sorted(counts.items())},
        }
    with OUTPUT.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(output_rows[0]))
        writer.writeheader()
        writer.writerows(output_rows)
    SUMMARY.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
