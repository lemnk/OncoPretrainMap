import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_challenge80_summary_and_confusion_are_consistent():
    summary = json.loads((ROOT / "reports/challenge80_review_summary.json").read_text())
    assert summary["sampled_relationships"] == 80
    assert summary["exact_agreement_count"] == 80
    assert summary["unweighted_cohens_kappa"] == 1.0
    assert summary["initial_class_counts"] == {"D0": 10, "D1": 37, "D2": 28, "D3": 5}
    assert summary["d1_upgraded_to_d2_d3_d4"] == 0
    assert summary["d2_downgraded_to_d1"] == 0

    with (ROOT / "data/validation/challenge80_row_comparison_v1.csv").open(
        encoding="utf-8", newline=""
    ) as handle:
        rows = list(csv.DictReader(handle))
    assert len(rows) == 80
    assert len({row["review_id"] for row in rows}) == 80
    assert all(row["agreement"] == "Yes" for row in rows)
    assert all(row["reviewer_name"] == "Caleb Yitna Ref" for row in rows)
    assert all(row["reviewer_used_ai"] == "No" for row in rows)
