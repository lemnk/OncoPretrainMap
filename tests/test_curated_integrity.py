import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read_csv(path):
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def test_curated_foreign_keys_and_identifiers_are_valid():
    datasets = read_csv(ROOT / "data" / "curated" / "datasets.csv")
    scope = read_csv(ROOT / "data" / "curated" / "evaluation_scope.csv")
    assertions = read_csv(ROOT / "data" / "curated" / "model_dataset_assertions.csv")
    disjoint = read_csv(ROOT / "data" / "curated" / "documented_disjoint.csv")
    models = read_csv(ROOT / "data" / "derived" / "pathbench_model_universe.csv")

    dataset_ids = [row["dataset_id"] for row in datasets]
    model_ids = [row["model_id"] for row in models]
    assertion_ids = [row["assertion_id"] for row in assertions]
    assert len(dataset_ids) == len(set(dataset_ids))
    assert len(model_ids) == len(set(model_ids))
    assert len(assertion_ids) == len(set(assertion_ids))

    dataset_set = set(dataset_ids)
    model_set = set(model_ids)
    assert {row["evaluation_dataset_id"] for row in scope} <= dataset_set
    assert {row["dataset_id"] for row in assertions} <= dataset_set
    assert {row["model_id"] for row in assertions} <= model_set
    assert {row["evaluation_dataset_id"] for row in disjoint} <= dataset_set
    assert {row["model_id"] for row in disjoint} <= model_set


def test_primary_assertions_are_versioned_and_cited():
    assertions = read_csv(ROOT / "data" / "curated" / "model_dataset_assertions.csv")
    for row in assertions:
        assert row["source_url"].startswith("https://")
        assert row["source_version"]
        assert row["retrieved_date"]
        assert row["evidence_summary"]


def test_every_core_model_has_primary_source_extraction():
    assertions = read_csv(ROOT / "data" / "curated" / "model_dataset_assertions.csv")
    models = read_csv(ROOT / "data" / "derived" / "pathbench_model_universe.csv")
    assert {row["model_id"] for row in assertions} == {row["model_id"] for row in models}


def test_no_unresolved_exposure_disjointness_conflicts_in_curated_inputs():
    assertions = read_csv(ROOT / "data" / "curated" / "model_dataset_assertions.csv")
    disjoint = read_csv(ROOT / "data" / "curated" / "documented_disjoint.csv")
    exposed = {(row["model_id"], row["dataset_id"]) for row in assertions}
    declared_disjoint = {(row["model_id"], row["evaluation_dataset_id"]) for row in disjoint}
    assert exposed.isdisjoint(declared_disjoint)


def test_pancancer40m_slide_manifest_is_complete_and_unique():
    rows = read_csv(ROOT / "data" / "derived" / "pancancer40m_training_slides.csv")
    slide_ids = [row["slide_filename"] for row in rows]
    assert len(rows) == 6093
    assert len(slide_ids) == len(set(slide_ids))
    assert len({row["case_barcode"] for row in rows}) == 5671
    assert sum(int(row["tile_count"]) for row in rows) == 43374634
    assert len({row["cohort_id"] for row in rows}) == 16
