import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_blanket_statement_scenarios_preserve_primary_and_warnings():
    summary = json.loads((ROOT / "reports" / "campanella_blanket_statement_sensitivity.json").read_text(encoding="utf-8"))
    assert summary["scenarios"]["source_specific_primary"]["class_counts"] == {
        "D0_documented_disjoint": 44,
        "D1_no_detected_evidence_or_insufficient_disclosure": 198,
    }
    assert summary["scenarios"]["blanket_six_foundation_models"]["class_counts"] == {
        "D0_documented_disjoint": 176,
        "D1_no_detected_evidence_or_insufficient_disclosure": 66,
    }
    assert summary["scenarios"]["blanket_six_plus_tres50"]["class_counts"] == {
        "D0_documented_disjoint": 198,
        "D1_no_detected_evidence_or_insufficient_disclosure": 44,
    }
    with (ROOT / "data" / "derived" / "campanella_blanket_statement_sensitivity.csv").open(
        encoding="utf-8", newline=""
    ) as handle:
        rows = list(csv.DictReader(handle))
    assert len(rows) == 726
    assert all(
        row["scenario_class"] == "D1_no_detected_evidence_or_insufficient_disclosure"
        for row in rows
        if row["exposure_warning"] == "overlap_cannot_be_excluded"
    )
