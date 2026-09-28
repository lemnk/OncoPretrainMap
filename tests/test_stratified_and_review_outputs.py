import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_pathology_specific_headline_and_cptac_cross_check():
    summary = json.loads(
        (ROOT / "reports" / "exposure_by_model_stratum.json").read_text(encoding="utf-8")
    )
    pathology = summary["benchmark_audit"]["Pathology-specific"]
    general = summary["benchmark_audit"]["General-purpose"]
    assert summary["model_counts"] == {"General-purpose": 9, "Pathology-specific": 23}
    assert pathology["total"] == 943
    assert pathology["class_counts"]["D1_no_detected_evidence_or_insufficient_disclosure"] == 683
    assert pathology["d1_percent"] == 72.4
    assert general["total"] == 369
    assert general["d1_percent"] == 100.0
    assert summary["cptac_cross_check"] == {
        "d3_rows": 14,
        "models": {"gpfm": 7, "phikon_v2": 7},
        "expected_models_present": True,
    }


def test_human_verification_targets_missed_exposure():
    summary = json.loads(
        (ROOT / "reports" / "human_verification_summary.json").read_text(encoding="utf-8")
    )
    assert summary["d1_reviewed"] == 23
    assert summary["d1_upgraded_to_d2_or_d3"] == 0
    assert 0.12 < summary["d1_upgrade_exact_one_sided_95_percent_upper_bound"] < 0.13
    assert summary["initially_blinded"] is False
    assert summary["reviewer_used_ai"] is False

    with (ROOT / "reports" / "human_verification_confusion_matrix.csv").open(
        encoding="utf-8", newline=""
    ) as handle:
        rows = list(csv.DictReader(handle))
    for row in rows[:4]:
        assert row[row["development_class/reviewer_class"]] in {"11", "23"}


def test_pre_and_post_review_versions_are_preserved():
    comparison = json.loads(
        (ROOT / "release" / "review_version_comparison.json").read_text(encoding="utf-8")
    )
    assert comparison["classifications_changed_after_review"] is False
    assert comparison["v1_pre_review"] == comparison["v2_post_review"]
