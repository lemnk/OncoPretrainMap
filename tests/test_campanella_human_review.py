import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_campanella_human_review_summary():
    path = ROOT / "reports" / "campanella_human_review_summary.json"
    summary = json.loads(path.read_text(encoding="utf-8"))
    assert summary["reviewer"] == "Caleb Yitna Ref"
    assert summary["initially_blinded"] is True
    assert summary["reviewer_used_ai"] is False
    assert summary["rows_reviewed"] == 60
    assert summary["agreements"] == 58
    assert summary["sampled_by_development_class"] == {
        "D0": 20, "D1": 28, "D2": 12, "D3": 0, "D4": 0
    }
    assert summary["agreement_by_development_class"] == {
        "D0": 20, "D1": 26, "D2": 12, "D3": 0, "D4": 0
    }
    assert summary["d1_upgrades_to_d2_d3_d4"] == 0
    assert summary["disagreements"] == ["CAMP-232", "CAMP-236"]
    assert (ROOT / summary["completed_workbook"]).is_file()
