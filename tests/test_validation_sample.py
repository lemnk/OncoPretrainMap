import csv
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_blinded_validation_sample_is_complete_and_unfilled():
    path = ROOT / "data" / "validation" / "independent_review_sample_v1.csv"
    with path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    assert len(rows) == 80
    assert [int(row["audit_row"]) for row in rows] == list(range(1, 81))
    assert len({(row["model_id"], row["evaluation_dataset_id"]) for row in rows}) == 80
    decision_fields = [
        "reviewer_exposure_scope",
        "reviewer_evidence_strength",
        "reviewer_source_urls",
        "reviewer_evidence_note",
        "reviewer_label",
        "review_date",
    ]
    assert all(not row[field] for row in rows for field in decision_fields)
    assert Counter(row["initially_blinded"] for row in rows) == {"Yes": 80}
