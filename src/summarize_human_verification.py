"""Validate and summarize the completed 80-pair human verification."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "validation" / "human_verification_adjudication.json"
REPORT = ROOT / "reports" / "human_verification_summary.json"
CONFUSION = ROOT / "reports" / "human_verification_confusion_matrix.csv"
LABELS = [
    "D0_documented_disjoint",
    "D1_no_detected_evidence_or_insufficient_disclosure",
    "D2_parent_repository_exposure",
    "D3_exact_dataset_exposure",
    "D4_exact_case_slide_or_patch_overlap",
]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> None:
    source = json.loads(SOURCE.read_text(encoding="utf-8"))
    workbook = ROOT / source["workbook"]
    if sha256(workbook) != source["workbook_sha256"]:
        raise ValueError("Completed review workbook hash does not match the frozen adjudication record")

    confusion = source["confusion_matrix"]
    development_counts = source["development_class_counts"]
    reviewer_counts = source["reviewer_class_counts"]
    rows = sum(development_counts.values())
    agreement = sum(confusion.get(label, {}).get(label, 0) for label in LABELS)
    expected_agreement = sum(
        development_counts[label] * reviewer_counts[label] for label in LABELS
    ) / (rows * rows)
    observed_agreement = agreement / rows
    kappa = (observed_agreement - expected_agreement) / (1 - expected_agreement)
    d1_n = development_counts["D1_no_detected_evidence_or_insufficient_disclosure"]
    d1_upgrades = source["d1_upgraded_to_d2_or_d3"]
    # Exact one-sided 95% upper confidence bound when zero upgrades are observed.
    upper = 1 - 0.05 ** (1 / d1_n) if d1_upgrades == 0 else None

    with CONFUSION.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["development_class/reviewer_class", *LABELS, "per_class_agreement"])
        for first in LABELS:
            values = [confusion.get(first, {}).get(second, 0) for second in LABELS]
            denominator = development_counts[first]
            per_class = values[LABELS.index(first)] / denominator if denominator else "NA"
            writer.writerow([first, *values, per_class])

    summary = {
        "reviewer": source["reviewer"],
        "review_date": source["review_date"],
        "sampled_relationships": rows,
        "sample_design": "Stratified: all 11 D0 pairs and 23 sampled pairs from each of D1, D2, and D3.",
        "exact_agreement_count": agreement,
        "exact_agreement_proportion": agreement / rows,
        "unweighted_cohens_kappa": kappa,
        "disagreements": rows - agreement,
        "complete_row_records": rows,
        "development_class_counts": development_counts,
        "reviewer_class_counts": reviewer_counts,
        "per_class_agreement": {
            label: (confusion.get(label, {}).get(label, 0) / development_counts[label])
            if development_counts[label]
            else None
            for label in LABELS
        },
        "d1_reviewed": d1_n,
        "d1_upgraded_to_d2_or_d3": d1_upgrades,
        "d1_upgrade_proportion": d1_upgrades / d1_n,
        "d1_upgrade_exact_one_sided_95_percent_upper_bound": upper,
        "initially_blinded": source["initially_blinded"],
        "reviewer_used_ai": source["reviewer_used_ai"],
        "interpretation": (
            "No sampled D1 pair was upgraded to D2 or D3. The second reviewer was blinded to the "
            "development classifications during initial review and did not use AI. The stratified sample "
            "supports class-specific agreement but is not a simple random sample of the full registry."
        ),
        "workbook": source["workbook"],
        "workbook_sha256": source["workbook_sha256"],
    }
    REPORT.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
