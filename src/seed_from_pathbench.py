"""Create a frozen discovery seed from the PathBench public repository."""

from __future__ import annotations

import csv
import hashlib
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "source" / "benchmarking-path-models"
DERIVED = ROOT / "data" / "derived"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", value.casefold()).strip("_")


def parse_markdown_table(readme: Path) -> list[dict[str, str]]:
    lines = readme.read_text(encoding="utf-8").splitlines()
    start = next(i for i, line in enumerate(lines) if line.startswith("| Category | Model Name |"))
    headers = [cell.strip() for cell in lines[start].strip().strip("|").split("|")]
    rows: list[dict[str, str]] = []
    for line in lines[start + 2 :]:
        if not line.startswith("|"):
            break
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) != len(headers):
            raise ValueError(f"Malformed model table row: {line}")
        rows.append(dict(zip(headers, cells)))
    return rows


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    readme = SOURCE / "README.md"
    results_path = SOURCE / "data" / "benchmarking_updated_ncomm.csv"
    if not readme.exists() or not results_path.exists():
        raise FileNotFoundError("Clone the frozen PathBench repository into data/source first.")

    model_rows = parse_markdown_table(readme)
    models: list[dict[str, object]] = []
    for row in model_rows:
        models.append(
            {
                "model_id": slug(row["Model Name"]),
                "display_name": row["Model Name"],
                "model_category": row["Category"],
                "weights_url": row["Weights / Source"],
                "pretraining_method": row["SSL / Pretraining Method"],
                "architecture": row["Model Architecture"],
                "parameters_m": row["Parameters (M)"],
                "reported_wsi_m": row["WSIs (M)"],
                "reported_patches_or_pairs_m": row["Patches / Image-Text Pairs (M)"],
                "reported_tissues": row["Cancer / Tissue Types"],
                "reported_data_source": row["Data Source"],
                "notes": row["Notes"],
                "discovery_source_id": "pathbench_2026_repository",
                "verification_status": "secondary_discovery_unverified",
            }
        )

    with results_path.open(encoding="utf-8-sig", newline="") as handle:
        results = list(csv.DictReader(handle))
    tasks_by_key: dict[tuple[str, ...], dict[str, object]] = {}
    matrix: list[dict[str, object]] = []
    for row in results:
        key = (
            row["Task_short"],
            row["Dataset"],
            row["Cancer"],
            row["tissue"],
            row["TaskCategory"],
            row["Slide_vs_patch_classification"],
        )
        tasks_by_key.setdefault(
            key,
            {
                "task_id": slug("__".join(key)),
                "task_name": row["Task_short"],
                "dataset_group": row["Dataset"],
                "cancer": row["Cancer"],
                "tissue": row["tissue"],
                "task_category": row["TaskCategory"],
                "analysis_level": row["Slide_vs_patch_classification"],
                "public_label": row["Public"],
                "verification_status": "benchmark_discovery_only",
            },
        )
        matrix.append(
            {
                "model_label": row["ModelName_short"],
                "task_id": tasks_by_key[key]["task_id"],
                "dataset_group": row["Dataset"],
                "auroc": row["AUROC"],
                "auprc": row["AUPRC"],
                "source_row_type": "published_benchmark_result",
            }
        )

    write_csv(DERIVED / "pathbench_model_universe.csv", list(models[0]), models)
    tasks = sorted(tasks_by_key.values(), key=lambda row: str(row["task_id"]))
    write_csv(DERIVED / "pathbench_task_universe.csv", list(tasks[0]), tasks)
    write_csv(DERIVED / "pathbench_model_task_matrix.csv", list(matrix[0]), matrix)
    hashes = {
        "source_repository_commit": "076ffcef84b7c3359a9ceaeb16e423e567fcd27a",
        "README.md": sha256(readme),
        "data/benchmarking_updated_ncomm.csv": sha256(results_path),
        "model_rows": len(models),
        "task_rows": len(tasks),
        "model_task_rows": len(matrix),
    }
    (DERIVED / "pathbench_source_hashes.json").write_text(
        json.dumps(hashes, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(hashes, indent=2))


if __name__ == "__main__":
    main()

