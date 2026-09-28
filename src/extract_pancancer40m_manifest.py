"""Stream the pinned PanCancer40M coordinate archive into a slide-level manifest."""

from __future__ import annotations

import csv
import hashlib
import json
import re
import zipfile
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = ROOT / "data" / "source" / "manifests" / "phikon_pretraining_dataset_coordinates_057cc029.zip"
EXPECTED_SHA256 = "89b847f2c54329e2170955e73bf890b5b2682a17e492085a455766b22cb06705"
CASE_PATTERN = re.compile(r"^(TCGA-[A-Z0-9]{2}-[A-Z0-9]{4})-")


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> None:
    if not ARCHIVE.exists():
        raise FileNotFoundError(f"Missing pinned source archive: {ARCHIVE}")
    observed_hash = file_sha256(ARCHIVE)
    if observed_hash != EXPECTED_SHA256:
        raise ValueError(f"Archive SHA-256 mismatch: {observed_hash}")

    records: list[dict[str, object]] = []
    cohort_counts: Counter[str] = Counter()
    total_tiles = 0
    with zipfile.ZipFile(ARCHIVE) as archive:
        entries = sorted(
            name for name in archive.namelist()
            if name.endswith(".txt") and not name.startswith("__MACOSX/")
        )
        for entry in entries:
            current: dict[str, object] | None = None
            with archive.open(entry) as handle:
                for raw_line in handle:
                    line = raw_line.decode("utf-8").strip()
                    if not line:
                        continue
                    if line.endswith(":") and "/" in line:
                        if current is not None:
                            records.append(current)
                        cohort, slide_filename = line[:-1].split("/", 1)
                        match = CASE_PATTERN.match(slide_filename)
                        if not match:
                            raise ValueError(f"Unrecognized TCGA slide identifier: {slide_filename}")
                        current = {
                            "corpus_id": "pancancer40m",
                            "cohort_id": cohort,
                            "case_barcode": match.group(1),
                            "slide_filename": slide_filename,
                            "tile_count": 0,
                            "source_revision": "057cc0295895c2df3dd7681a89680da6015cbefe",
                            "source_archive_sha256": EXPECTED_SHA256,
                        }
                        cohort_counts[cohort] += 1
                    else:
                        if current is None:
                            raise ValueError(f"Tile appeared before slide header in {entry}")
                        current["tile_count"] = int(current["tile_count"]) + 1
                        total_tiles += 1
            if current is not None:
                records.append(current)

    slide_ids = [str(row["slide_filename"]) for row in records]
    if len(slide_ids) != len(set(slide_ids)):
        raise ValueError("Duplicate slide identifiers found in coordinate archive")

    output = ROOT / "data" / "derived" / "pancancer40m_training_slides.csv"
    with output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(records[0]))
        writer.writeheader()
        writer.writerows(records)

    summary = {
        "source_archive_sha256": observed_hash,
        "slide_count": len(records),
        "case_count": len({row["case_barcode"] for row in records}),
        "tile_count": total_tiles,
        "cohort_count": len(cohort_counts),
        "slides_by_cohort": dict(sorted(cohort_counts.items())),
        "interpretation": (
            "Primary training-manifest extraction only. D4 overlap requires an independently sourced "
            "evaluation-slide manifest and exact identifier intersection."
        ),
    }
    summary_path = ROOT / "reports" / "pancancer40m_manifest_summary.json"
    summary_path.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
