import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read_csv(path):
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def test_every_pathbench_result_model_has_one_alias():
    matrix = read_csv(ROOT / "data" / "derived" / "pathbench_model_task_matrix.csv")
    aliases = read_csv(ROOT / "data" / "curated" / "pathbench_model_aliases.csv")
    labels = {row["model_label"] for row in matrix}
    alias_labels = [row["pathbench_model_label"] for row in aliases]
    assert len(alias_labels) == len(set(alias_labels))
    assert labels == set(alias_labels)


def test_alias_targets_exist_in_core_universe():
    models = read_csv(ROOT / "data" / "derived" / "pathbench_model_universe.csv")
    aliases = read_csv(ROOT / "data" / "curated" / "pathbench_model_aliases.csv")
    model_ids = {row["model_id"] for row in models}
    assert {row["model_id"] for row in aliases} == model_ids

