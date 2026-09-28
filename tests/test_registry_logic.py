from src.build_exposure_registry import ancestors, classify


def test_parent_repository_exposure():
    datasets = [
        {"dataset_id": "tcga", "parent_dataset_id": ""},
        {"dataset_id": "tcga_brca", "parent_dataset_id": "tcga"},
    ]
    scope, strength, conflict = classify("tcga", "tcga_brca", ancestors(datasets))
    assert scope == "D2_parent_repository_exposure"
    assert strength == "C_lineage_inference"
    assert conflict is False


def test_exact_dataset_exposure():
    scope, strength, conflict = classify("tcga_brca", "tcga_brca", {})
    assert scope == "D3_exact_dataset_exposure"
    assert strength == "B_explicit_primary_source_statement"
    assert conflict is False


def test_exact_identifier_overlap_overrides_disjoint_claim_and_flags_conflict():
    scope, strength, conflict = classify(
        "tcga", "tcga_brca", {"tcga_brca": {"tcga"}},
        documented_disjoint=True, exact_identifier_overlap=True
    )
    assert scope == "D4_exact_case_slide_or_patch_overlap"
    assert strength == "A_identifier_manifest"
    assert conflict is True


def test_missing_evidence_is_not_independence():
    scope, strength, conflict = classify(None, "panda", {})
    assert scope == "D1_no_detected_evidence_or_insufficient_disclosure"
    assert strength == "D_incomplete_or_ambiguous_disclosure"
    assert conflict is False


def test_documented_disjoint_when_no_conflicting_exposure():
    scope, strength, conflict = classify(None, "panda", {}, documented_disjoint=True)
    assert scope == "D0_documented_disjoint"
    assert strength == "B_explicit_primary_source_statement"
    assert conflict is False


def test_multilevel_lineage_closure():
    datasets = [
        {"dataset_id": "tcga", "parent_dataset_id": ""},
        {"dataset_id": "tcga_brca", "parent_dataset_id": "tcga"},
        {"dataset_id": "tcga_brca_patch", "parent_dataset_id": "tcga_brca"},
    ]
    lineage = ancestors(datasets)
    assert lineage["tcga_brca_patch"] == {"tcga", "tcga_brca"}
