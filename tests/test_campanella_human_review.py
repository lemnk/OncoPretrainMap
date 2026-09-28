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
    assert summary["initial_preaudit_agreements"] == 58
    assert summary["corrected_final_agreements"] == 46
    assert summary["sampled_by_corrected_final_class"] == {
        "D0": 20, "D1": 40, "D2": 0, "D3": 0, "D4": 0
    }
    assert summary["agreement_by_corrected_final_class"] == {
        "D0": 20, "D1": 26, "D2": 0, "D3": 0, "D4": 0
    }
    assert summary["reviewer_d1_to_d2_d3_d4_assignments"] == 12
    assert summary["preaudit_disagreements"] == ["CAMP-232", "CAMP-236"]
    assert summary["postaudit_d2_to_d1_corrections"] == 12
    assert (ROOT / summary["completed_workbook"]).is_file()
