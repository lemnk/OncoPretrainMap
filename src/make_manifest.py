"""Write hashes for version-controlled study artifacts."""

from __future__ import annotations

import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
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
            files.update(
                item for item in path.rglob("*")
                if item.is_file() and "__pycache__" not in item.parts
            )
    lines = [f"{digest(path)}  {path.relative_to(ROOT).as_posix()}" for path in sorted(files)]
    (ROOT / "MANIFEST.sha256").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {len(lines)} hashes")


if __name__ == "__main__":
    main()
