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
    assert summary["initial_blinded_agreement_rows"] == 58
    assert summary["postaudit_resolved_concordant_rows"] == 46
    assert summary["postaudit_resolved_concordance_proportion"] == 46 / 60
    assert "not a clean inter-rater reliability statistic" in summary["postaudit_metric_note"]
    assert summary["sampled_by_postaudit_resolved_class"] == {
        "D0": 20, "D1": 40, "D2": 0, "D3": 0, "D4": 0
    }
    assert summary["concordant_by_postaudit_resolved_class"] == {
        "D0": 20, "D1": 26, "D2": 0, "D3": 0, "D4": 0
    }
    assert summary["reviewer_d1_to_d2_d3_d4_assignments"] == 12
    assert summary["initial_blinded_disagreements"] == ["CAMP-232", "CAMP-236"]
    assert summary["postaudit_d2_to_d1_corrections"] == 12
    assert (ROOT / summary["completed_workbook"]).is_file()
