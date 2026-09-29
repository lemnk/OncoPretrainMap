import csv
import json
import sys
from pathlib import Path

from src.check_pretraining_overlap import main as checker_main


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
        "D1_no_detected_evidence_or_insufficient_disclosure": 198,
    }
    assert summary["exposure_warning_count"] == 12
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


def test_mskcc_overlap_warning_does_not_overstate_containment():
    audit = rows()
    warned = [row for row in audit if row["exposure_warning"] == "overlap_cannot_be_excluded"]
    assert len(warned) == 12
    assert {row["model_label"] for row in warned} == {"Virchow", "Virchow2"}
    assert {row["evaluation_institution"] for row in warned} == {"MSKCC"}
    assert all(row["exposure_scope"] == "D1_no_detected_evidence_or_insufficient_disclosure" for row in warned)


def test_checker_reports_d1_plus_warning(monkeypatch, capsys):
    registry = ROOT / "data" / "derived" / "campanella_transport_audit.csv"
    monkeypatch.setattr(
        sys,
        "argv",
        ["check_pretraining_overlap.py", "virchow", "campanella_mskcc_luad_alk", "--registry", str(registry)],
    )
    assert checker_main() == 0
    output = capsys.readouterr().out
    assert "D1_no_detected_evidence_or_insufficient_disclosure" in output
    assert "Exposure warning: overlap cannot be excluded; D2-D4 are not established." in output
