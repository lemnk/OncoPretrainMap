import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_human_verification_summary_matches_workbook_hash():
    summary = json.loads((ROOT / "reports" / "human_verification_summary.json").read_text(encoding="utf-8"))
    workbook = ROOT / summary["workbook"]
    assert workbook.exists()
    assert hashlib.sha256(workbook.read_bytes()).hexdigest() == summary["workbook_sha256"]
    assert summary["sampled_relationships"] == 80
    assert summary["exact_agreement_count"] == 80
    assert summary["exact_agreement_proportion"] == 1.0
    assert summary["disagreements"] == 0
    assert summary["complete_row_records"] == 80
    assert summary["initially_blinded"] is True
    assert sum(summary["reviewer_class_counts"].values()) == 80
