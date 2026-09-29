"""Freeze an unlabelled challenge packet from previously unreviewed registry rows.

The private key is deliberately gitignored. Do not share it with the reviewer.
"""

from __future__ import annotations

import csv
import hashlib
import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SEED = "OncoPretrainMap-challenge-80-2026-09-28-v1"
OUT = ROOT / "data" / "validation"
PRIVATE = OUT / "private"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def order_key(item: dict[str, str]) -> str:
    return hashlib.sha256((SEED + "|" + item["source_id"]).encode()).hexdigest()


def balanced_pick(items: list[dict[str, str]], count: int, group: str) -> list[dict[str, str]]:
    """Seeded greedy round-robin minimizes repeated models before reusing one."""
    remaining = sorted(items, key=order_key)
    selected: list[dict[str, str]] = []
    usage: Counter[str] = Counter()
    while len(selected) < count:
        if not remaining:
            raise ValueError(f"Only {len(selected)} candidates for {group}; need {count}")
        least = min(usage[item[group]] for item in remaining)
        index = next(i for i, item in enumerate(remaining) if usage[item[group]] == least)
        item = remaining.pop(index)
        selected.append(item)
        usage[item[group]] += 1
    return selected


def main() -> None:
    dev = read_csv(ROOT / "data/derived/model_dataset_exposure_development.csv")
    dataset_names = {
        row["dataset_id"]: row["display_name"]
        for row in read_csv(ROOT / "data/curated/datasets.csv")
    }
    dev_reviewed = {
        (row["model_id"], row["evaluation_dataset_id"])
        for row in read_csv(OUT / "independent_review_sample_v1.csv")
    }
    camp = read_csv(ROOT / "data/derived/campanella_transport_audit.csv")
    camp_reviewed = {
        row["transport_row_id"]
        for row in read_csv(OUT / "campanella_transport_blinded_review_packet.csv")
    }
    candidates: list[dict[str, str]] = []
    for row in dev:
        if (row["model_id"], row["evaluation_dataset_id"]) in dev_reviewed:
            continue
        candidates.append({
            "source_id": f"DEV:{row['model_id']}:{row['evaluation_dataset_id']}",
            "benchmark_context": "Development registry (Bareja benchmark model universe)",
            "model_checkpoint": row["model_name"],
            "evaluation_dataset_or_task": (
                f"{dataset_names.get(row['evaluation_dataset_id'], row['evaluation_dataset_id'])} "
                f"[{row['evaluation_dataset_id']}]"
            ),
            "evaluation_institution": "",
            "initial_class": row["exposure_scope"],
            "initial_evidence_grade": row["evidence_strength"],
        })
    for row in camp:
        if row["transport_row_id"] in camp_reviewed:
            continue
        candidates.append({
            "source_id": f"CAMP:{row['transport_row_id']}",
            "benchmark_context": "Campanella clinical benchmark",
            "model_checkpoint": row["model_label"],
            "evaluation_dataset_or_task": row["task_name"],
            "evaluation_institution": row["evaluation_institution"],
            "initial_class": row["exposure_scope"],
            "initial_evidence_grade": row["evidence_strength"],
        })

    def pool(source: str, cls: str) -> list[dict[str, str]]:
        return [x for x in candidates if x["source_id"].startswith(source) and x["initial_class"].startswith(cls)]

    selected = (
        balanced_pick([x for x in pool("CAMP", "D0") if x["model_checkpoint"] == "SP22M"], 5, "model_checkpoint")
        + balanced_pick([x for x in pool("CAMP", "D0") if x["model_checkpoint"] == "SP85M"], 5, "model_checkpoint")
        + balanced_pick(pool("DEV", "D1"), 19, "model_checkpoint")
        + balanced_pick(pool("CAMP", "D1"), 18, "model_checkpoint")
        + balanced_pick(pool("DEV", "D2"), 28, "model_checkpoint")
        + balanced_pick(pool("DEV", "D3"), 5, "model_checkpoint")
    )
    assert len(selected) == 80
    assert len({x["source_id"] for x in selected}) == 80
    # Mix classes so worksheet order does not reveal the sampling strata.
    selected = sorted(selected, key=order_key)
    packet = []
    key = []
    for i, row in enumerate(selected, 1):
        rid = f"CH80-{i:03d}"
        packet.append({
            "review_id": rid,
            "benchmark_context": row["benchmark_context"],
            "model_checkpoint": row["model_checkpoint"],
            "evaluation_dataset_or_task": row["evaluation_dataset_or_task"],
            "evaluation_institution": row["evaluation_institution"],
        })
        key.append({"review_id": rid, **row})
    OUT.mkdir(parents=True, exist_ok=True)
    PRIVATE.mkdir(parents=True, exist_ok=True)
    # Refuse accidental replacement of a previously frozen sample.
    packet_path = OUT / "challenge80_packet_data_v1.json"
    key_path = PRIVATE / "challenge80_key_v1.json"
    for path in (packet_path, key_path):
        if path.exists():
            raise FileExistsError(path)
    packet_path.write_text(json.dumps(packet, indent=2) + "\n", encoding="utf-8")
    key_path.write_text(json.dumps(key, indent=2) + "\n", encoding="utf-8")
    print("Packet rows:", len(packet))
    print("Private source/class mix:", Counter((x["source_id"].split(":")[0], x["initial_class"].split("_")[0]) for x in key))


if __name__ == "__main__":
    main()
