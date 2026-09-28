"""Write hashes for version-controlled study artifacts."""

from __future__ import annotations

import hashlib
import os
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXCLUDED_PARTS = {"__pycache__", "node_modules", ".pytest_cache", "tmp"}
INCLUDE = [
    "README.md",
    "FEASIBILITY_AUDIT.md",
    "PROJECT_PLAN.md",
    "PROTOCOL_v1_20260927.md",
    "PROTOCOL_DEVIATIONS.md",
    "requirements.txt",
    "run_pipeline.ps1",
    "config",
    "data/curated",
    "data/derived",
    "data/validation",
    "figures",
    "src",
    "tests",
    "reports",
    "manuscript",
]


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def main() -> None:
    files: set[Path] = set()
    for relative in INCLUDE:
        path = ROOT / relative
        if path.is_file():
            files.add(path)
        elif path.is_dir():
            for directory, subdirectories, filenames in os.walk(path):
                subdirectories[:] = [name for name in subdirectories if name not in EXCLUDED_PARTS]
                files.update(Path(directory) / filename for filename in filenames)
    lines = [f"{digest(path)}  {path.relative_to(ROOT).as_posix()}" for path in sorted(files)]
    (ROOT / "MANIFEST.sha256").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {len(lines)} hashes")


if __name__ == "__main__":
    main()
