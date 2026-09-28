"""Apply the frozen OncoPretrainMap rules to an independent clinical benchmark."""

from __future__ import annotations

import csv
import hashlib
import json
import random
import re
from collections import Counter
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw" / "campanella_source_data"
DERIVED = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
VALIDATION = ROOT / "data" / "validation"

ARTICLE_URL = "https://pmc.ncbi.nlm.nih.gov/articles/PMC12003829/"
MODEL_IDS = {
    "CTransPath": "ctranspath",
    "Phikon": "phikon",
    "Phikon-v2": "phikon_v2",
    "Prov-GigaPath": "prov_gigapath",
    "SP22M": "sp22m",
    "SP85M": "sp85m",
    "UNI": "uni",
    "Virchow": "virchow",
    "Virchow2": "virchow2",
    "h-optimus-0": "h_optimus_0",
    "tRes50": "tres50_imagenet",
}


def slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_")


def institution(task: str) -> str:
    prefix = task.split()[0]
    if prefix not in {"MSHS", "MSKCC", "SUH"}:
        raise ValueError(f"Unrecognized task institution: {task}")
    return prefix


def classify(model: str, site: str) -> tuple[str, str, str, str]:
    if model in {"SP22M", "SP85M"}:
        return (
            "D0_documented_disjoint",
            "B_explicit_primary_source_statement",
            "The benchmark article states that the in-house model pretraining data did not overlap the clinical benchmarking data.",
            f"{ARTICLE_URL}#Par70",
        )
    if model in {"Virchow", "Virchow2"} and site == "MSKCC":
        return (
            "D2_parent_repository_exposure",
            "B_explicit_primary_source_statement",
            "The checkpoint was pretrained on an MSKCC slide corpus, and the benchmark article states that overlap with MSKCC clinical tasks cannot be excluded; exact benchmark identifiers are unavailable.",
            f"{ARTICLE_URL}#Par69",
        )
    return (
        "D1_no_detected_evidence_or_insufficient_disclosure",
        "D_incomplete_or_ambiguous_disclosure",
        "The frozen public evidence does not document disjointness or a containing-corpus relationship for this model-task pair; independence cannot be assumed.",
        ARTICLE_URL,
    )


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def create_review_sample(rows: list[dict[str, object]]) -> None:
    strata = {
        "D0_documented_disjoint": 20,
        "D1_no_detected_evidence_or_insufficient_disclosure": 28,
        "D2_parent_repository_exposure": 12,
    }
    selected: list[dict[str, object]] = []
    for exposure_scope, target in strata.items():
        candidates = [row for row in rows if row["exposure_scope"] == exposure_scope]
        seed = int(hashlib.sha256(f"campanella-transport|{exposure_scope}".encode()).hexdigest()[:16], 16)
        random.Random(seed).shuffle(candidates)
        selected.extend(candidates[: min(target, len(candidates))])
    selected.sort(key=lambda row: str(row["transport_row_id"]))

    key_rows = [
        {
            "transport_row_id": row["transport_row_id"],
            "development_class": row["exposure_scope"],
            "development_evidence_strength": row["evidence_strength"],
        }
        for row in selected
    ]
    packet_rows = [
        {
            "transport_row_id": row["transport_row_id"],
            "model_label": row["model_label"],
            "task_name": row["task_name"],
            "evaluation_institution": row["evaluation_institution"],
            "article_url": ARTICLE_URL,
            "official_repository": "https://github.com/sinai-computational-pathology/SSL_tile_benchmarks/tree/fbdf07f932d7302fd7bcb4a1e6b78bfb9d4a71f9",
            "reviewer_class": "",
            "reviewer_evidence_strength": "",
            "reviewer_explanation": "",
            "reviewer_source_urls": "",
            "reviewer_identity": "",
            "review_date": "",
            "initially_blinded": "Yes",
            "reviewer_used_ai": "",
        }
        for row in selected
    ]
    write_csv(VALIDATION / "campanella_transport_review_key.csv", key_rows)
    write_csv(VALIDATION / "campanella_transport_blinded_review_packet.csv", packet_rows)


def main() -> None:
    frames = []
    for filename, task_type in (("figure_1.csv", "disease_detection"), ("figure_2.csv", "biomarker_prediction")):
        frame = pd.read_csv(RAW / filename)
        frame["source_table"] = filename
        frame["task_type"] = task_type
        frames.append(frame)
    source = pd.concat(frames, ignore_index=True)
    pairs = source[["Encoder", "Task", "source_table", "task_type"]].drop_duplicates()
    if len(pairs) != 242:
        raise ValueError(f"Expected 242 model-task pairs; observed {len(pairs)}")
    unknown = sorted(set(pairs["Encoder"]) - set(MODEL_IDS))
    if unknown:
        raise ValueError(f"Unmapped model labels: {unknown}")

    rows: list[dict[str, object]] = []
    for index, record in enumerate(pairs.sort_values(["Encoder", "Task"]).to_dict("records"), start=1):
        model = record["Encoder"]
        task = record["Task"]
        site = institution(task)
        scope, strength, statement, evidence_url = classify(model, site)
        rows.append(
            {
                "transport_row_id": f"CAMP-{index:03d}",
                "benchmark_id": "campanella_2025_clinical",
                "model_label": model,
                "model_id": MODEL_IDS[model],
                "task_name": task,
                "task_id": slug(task),
                "task_type": record["task_type"],
                "evaluation_institution": site,
                "canonical_evaluation_dataset_id": f"campanella_{slug(task)}",
                "source_table": record["source_table"],
                "dataset_label_resolvable": "Yes",
                "exposure_scope": scope,
                "benchmark_exposure_scope": scope,
                "evidence_strength": strength,
                "conflict_flag": "False",
                "independence_statement": statement,
                "evidence_url": evidence_url,
                "rule_changed_after_freeze": "No",
            }
        )

    write_csv(DERIVED / "campanella_transport_audit.csv", rows)
    create_review_sample(rows)

    counts = Counter(str(row["benchmark_exposure_scope"]) for row in rows)
    sites = Counter(str(row["evaluation_institution"]) for row in rows)
    summary = {
        "benchmark_id": "campanella_2025_clinical",
        "model_task_rows": len(rows),
        "models": len({row["model_id"] for row in rows}),
        "tasks": len({row["task_id"] for row in rows}),
        "canonical_mapping_success_count": sum(row["dataset_label_resolvable"] == "Yes" for row in rows),
        "canonical_mapping_success_proportion": sum(row["dataset_label_resolvable"] == "Yes" for row in rows) / len(rows),
        "exposure_scope_counts": dict(sorted(counts.items())),
        "evaluation_institution_counts": dict(sorted(sites.items())),
        "rule_changes_after_freeze": sum(row["rule_changed_after_freeze"] != "No" for row in rows),
        "conflicts": sum(row["conflict_flag"] != "False" for row in rows),
        "second_reviewer_status": "Pending; deterministic blinded packet generated. No reliability estimate is reported.",
        "interpretation": "The frozen framework represented all relationships without a rule change. D1 is unresolved and is not evidence of independence. D2 on MSKCC tasks is institution-level containing-corpus exposure, not proof of shared patients or slides.",
    }
    REPORTS.mkdir(parents=True, exist_ok=True)
    (REPORTS / "campanella_transport_summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")

    primary = json.loads((REPORTS / "pathbench_exposure_audit_development.json").read_text(encoding="utf-8"))
    primary_counts = primary["benchmark_exposure_scope_counts"]
    labels = [
        "D0_documented_disjoint",
        "D1_no_detected_evidence_or_insufficient_disclosure",
        "D2_parent_repository_exposure",
        "D3_exact_dataset_exposure",
        "D4_exact_case_slide_or_patch_overlap",
    ]
    comparison = []
    for name, total, values in (
        ("Bareja et al. development application", primary["published_model_task_rows"], primary_counts),
        ("Campanella et al. external transport", len(rows), counts),
    ):
        comparison.append({"benchmark": name, "models": primary["models"] if name.startswith("Bareja") else summary["models"], "tasks": primary["tasks"] if name.startswith("Bareja") else summary["tasks"], "model_task_rows": total, **{label: int(values.get(label, 0)) for label in labels}})
    write_csv(REPORTS / "cross_benchmark_exposure_comparison.csv", comparison)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
