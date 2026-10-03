import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_direct_source_baseline_outputs_are_complete():
    summary = json.loads((ROOT / "reports/direct_source_baseline_summary.json").read_text(encoding="utf-8"))
    assert summary["registry_pair_universe"] == 896
    assert summary["published_benchmark_rows"] == 1312
    assert summary["pair_level_exact_agreement"] + summary["lineage_added_exposure_pairs"] == 896


def test_every_comparison_row_has_boolean_agreement():
    with (ROOT / "data/derived/direct_source_baseline_pairs.csv").open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    assert len(rows) == 896
    assert {row["agreement"] for row in rows} <= {"True", "False"}


def test_benchmark_comparison_is_complete():
    with (ROOT / "data/derived/pathbench_direct_source_baseline_comparison.csv").open(
        encoding="utf-8", newline=""
    ) as handle:
        rows = list(csv.DictReader(handle))
    assert len(rows) == 1312
