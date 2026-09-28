import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def rows():
    with (ROOT / "data" / "derived" / "campanella_transport_audit.csv").open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def test_external_transport_universe_and_mapping():
    audit = rows()
    assert len(audit) == 242
    assert len({row["model_id"] for row in audit}) == 11
    assert len({row["task_id"] for row in audit}) == 22
    assert all(row["dataset_label_resolvable"] == "Yes" for row in audit)
    assert all(row["rule_changed_after_freeze"] == "No" for row in audit)


def test_external_transport_frozen_class_counts():
    summary = json.loads((ROOT / "reports" / "campanella_transport_summary.json").read_text(encoding="utf-8"))
    assert summary["exposure_scope_counts"] == {
        "D0_documented_disjoint": 44,
        "D1_no_detected_evidence_or_insufficient_disclosure": 186,
        "D2_parent_repository_exposure": 12,
    }
    assert summary["rule_changes_after_freeze"] == 0
    assert summary["conflicts"] == 0


def test_external_review_packet_is_blinded_and_complete():
    packet_path = ROOT / "data" / "validation" / "campanella_transport_blinded_review_packet.csv"
    with packet_path.open(encoding="utf-8", newline="") as handle:
        packet = list(csv.DictReader(handle))
    assert len(packet) == 60
    assert "development_class" not in packet[0]
    assert all(row["initially_blinded"] == "Yes" for row in packet)
    assert all(row["reviewer_used_ai"] == "" for row in packet)
