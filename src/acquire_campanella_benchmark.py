"""Acquire and verify the frozen Campanella et al. benchmark source data."""

from __future__ import annotations

import hashlib
import json
import shutil
import urllib.request
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "config" / "campanella_transport_source.json"
RAW = ROOT / "data" / "raw"
SUPPLEMENTARY_ZIP = RAW / "campanella_supplementary_all.zip"
SUPPLEMENTARY_DIR = RAW / "campanella_supplementary"
SOURCE_DIR = RAW / "campanella_source_data"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> None:
    config = json.loads(CONFIG.read_text(encoding="utf-8"))
    RAW.mkdir(parents=True, exist_ok=True)
    source_zip = SUPPLEMENTARY_DIR / config["source_data_filename"]

    if not source_zip.exists() or sha256(source_zip) != config["source_data_sha256"]:
        if not SUPPLEMENTARY_ZIP.exists():
            request = urllib.request.Request(
                config["supplementary_archive_url"],
                headers={"User-Agent": "OncoPretrainMap/1.0 (public-data reproducibility)"},
            )
            with urllib.request.urlopen(request, timeout=180) as response:
                with SUPPLEMENTARY_ZIP.open("wb") as output:
                    shutil.copyfileobj(response, output)
        SUPPLEMENTARY_DIR.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(SUPPLEMENTARY_ZIP) as archive:
            archive.extractall(SUPPLEMENTARY_DIR)

    observed = sha256(source_zip)
    if observed != config["source_data_sha256"]:
        raise ValueError(f"Campanella source-data hash mismatch: {observed}")

    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(source_zip) as archive:
        archive.extractall(SOURCE_DIR)
    required = {"figure_1.csv", "figure_2.csv"}
    missing = required - {path.name for path in SOURCE_DIR.iterdir()}
    if missing:
        raise ValueError(f"Missing expected benchmark source tables: {sorted(missing)}")
    print(f"Verified Campanella source data: {observed}")


if __name__ == "__main__":
    main()
