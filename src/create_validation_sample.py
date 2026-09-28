"""Create a deterministic blinded sample for independent registry validation."""

from __future__ import annotations

import csv
import hashlib
import random
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "data" / "derived" / "model_dataset_exposure_development.csv"
OUTPUT = ROOT / "data" / "validation" / "independent_review_sample_v1.csv"
SEED_TEXT = "OncoPretrainMap-independent-review-v1-2026-09-28"
TARGETS = {
    "D0_documented_disjoint": 11,
    "D1_no_detected_evidence_or_insufficient_disclosure": 23,
    "D2_parent_repository_exposure": 23,
    "D3_exact_dataset_exposure": 23,
}


def main() -> None:
    with INPUT.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))

    seed = int.from_bytes(hashlib.sha256(SEED_TEXT.encode()).digest()[:8], "big")
    rng = random.Random(seed)
    selected: list[dict[str, str]] = []
    for scope, target in TARGETS.items():
        candidates = [row for row in rows if row["exposure_scope"] == scope]
        if len(candidates) < target:
            raise ValueError(f"Need {target} {scope} rows, found {len(candidates)}")
        selected.extend(rng.sample(candidates, target))
    rng.shuffle(selected)

    fields = [
        "audit_row",
        "model_id",
        "model_name",
        "evaluation_dataset_id",
        "reviewer_exposure_scope",
        "reviewer_evidence_strength",
        "reviewer_source_urls",
        "reviewer_evidence_note",
        "reviewer_label",
        "review_date",
        "initially_blinded",
    ]
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for index, row in enumerate(selected, start=1):
            writer.writerow(
                {
                    "audit_row": index,
                    "model_id": row["model_id"],
                    "model_name": row["model_name"],
                    "evaluation_dataset_id": row["evaluation_dataset_id"],
                    "reviewer_exposure_scope": "",
                    "reviewer_evidence_strength": "",
                    "reviewer_source_urls": "",
                    "reviewer_evidence_note": "",
                    "reviewer_label": "",
                    "review_date": "",
                    "initially_blinded": "Yes",
                }
            )
    digest = hashlib.sha256(OUTPUT.read_bytes()).hexdigest()
    print(f"Wrote {len(selected)} blinded rows to {OUTPUT}")
    print(f"SHA-256: {digest}")


if __name__ == "__main__":
    main()
