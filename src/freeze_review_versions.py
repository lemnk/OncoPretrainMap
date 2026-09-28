"""Preserve pre-review v1 and regenerate post-verification v2 release tables."""

from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FILES = {
    "model_dataset_exposure.csv": ROOT / "data" / "derived" / "model_dataset_exposure_development.csv",
    "benchmark_exposure_audit.csv": ROOT / "data" / "derived" / "pathbench_exposure_audit_development.csv",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    v1 = ROOT / "release" / "v1_pre_review"
    v2 = ROOT / "release" / "v2_post_review"
    v1.mkdir(parents=True, exist_ok=True)
    v2.mkdir(parents=True, exist_ok=True)

    hashes = {"v1_pre_review": {}, "v2_post_review": {}}
    for name, source in FILES.items():
        frozen = v1 / name
        if frozen.exists() and sha256(frozen) != sha256(source):
            raise ValueError(f"Frozen v1 artifact changed: {name}")
        if not frozen.exists():
            shutil.copyfile(source, frozen)
        shutil.copyfile(source, v2 / name)
        hashes["v1_pre_review"][name] = sha256(frozen)
        hashes["v2_post_review"][name] = sha256(v2 / name)

    shutil.copyfile(
        ROOT / "reports" / "human_verification_summary.json",
        v2 / "human_verification_summary.json",
    )
    hashes["classifications_changed_after_review"] = any(
        hashes["v1_pre_review"][name] != hashes["v2_post_review"][name] for name in FILES
    )
    (ROOT / "release" / "review_version_comparison.json").write_text(
        json.dumps(hashes, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(hashes, indent=2))


if __name__ == "__main__":
    main()
