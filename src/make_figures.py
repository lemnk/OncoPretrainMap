"""Generate manuscript figures from reproducible tabular outputs."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "reports"
DERIVED = ROOT / "data" / "derived"
FIGURES = ROOT / "figures"
COLORS = {
    "D0_documented_disjoint": "#3B82A0",
    "D1_no_detected_evidence_or_insufficient_disclosure": "#B8BDC6",
    "D2_parent_repository_exposure": "#E0A43A",
    "D3_exact_dataset_exposure": "#B54A4A",
}
SHORT = {
    "D0_documented_disjoint": "D0 documented disjoint",
    "D1_no_detected_evidence_or_insufficient_disclosure": "D1 unresolved",
    "D2_parent_repository_exposure": "D2 parent repository",
    "D3_exact_dataset_exposure": "D3 exact dataset",
}


def save(fig: plt.Figure, stem: str) -> None:
    FIGURES.mkdir(parents=True, exist_ok=True)
    fig.savefig(FIGURES / f"{stem}.png", dpi=300, bbox_inches="tight")
    frozen_time = datetime(2026, 9, 28, tzinfo=timezone.utc)
    fig.savefig(
        FIGURES / f"{stem}.pdf",
        bbox_inches="tight",
        metadata={
            "Creator": "OncoPretrainMap",
            "Producer": "Matplotlib",
            "CreationDate": frozen_time,
            "ModDate": frozen_time,
        },
    )
    plt.close(fig)


def exposure_by_group() -> None:
    frame = pd.read_csv(DERIVED / "pathbench_exposure_audit_development.csv")
    frame["dataset_group"] = frame["dataset_group"].replace(
        {"External_benchmarking_cohort": "External benchmark", "Out of Domain": "Out of domain"}
    )
    table = pd.crosstab(frame["dataset_group"], frame["exposure_scope"])
    proportions = table.div(table.sum(axis=1), axis=0)
    scopes = [scope for scope in COLORS if scope in proportions.columns]
    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    left = np.zeros(len(proportions))
    for scope in scopes:
        values = proportions[scope].to_numpy()
        ax.barh(proportions.index, values, left=left, color=COLORS[scope], label=SHORT[scope])
        left += values
    ax.set_xlabel("Proportion of published model–task results")
    ax.set_xlim(0, 1)
    ax.xaxis.set_major_formatter(lambda value, _: f"{value:.0%}")
    ax.legend(frameon=False, loc="lower center", bbox_to_anchor=(0.5, 1.02), ncol=2)
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.grid(axis="x", color="#E6E8EB", linewidth=0.8)
    ax.set_axisbelow(True)
    fig.tight_layout()
    save(fig, "figure1_exposure_by_benchmark_group")


def coefficient_forest() -> None:
    frame = pd.read_csv(REPORTS / "performance_exposure_fixed_effects.csv")
    frame["label"] = frame["outcome"].str.upper() + " — " + frame["contrast_scope"].map(SHORT)
    frame = frame.iloc[::-1].reset_index(drop=True)
    y = np.arange(len(frame))
    fig, ax = plt.subplots(figsize=(8.4, 3.8))
    colors = [COLORS[scope] for scope in frame["contrast_scope"]]
    for position, (_, row) in zip(y, frame.iterrows()):
        color = COLORS[row["contrast_scope"]]
        ax.errorbar(
            row["estimate"], position,
            xerr=[[row["estimate"] - row["ci95_low"]], [row["ci95_high"] - row["estimate"]]],
            fmt="o", color=color, ecolor=color, elinewidth=2, capsize=4, markersize=6,
        )
    ax.axvline(0, color="#30343B", linewidth=1)
    ax.set_yticks(y, frame["label"])
    ax.set_xlabel("Adjusted difference versus D1 (95% CI)")
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.grid(axis="x", color="#E6E8EB", linewidth=0.8)
    ax.set_axisbelow(True)
    fig.tight_layout()
    save(fig, "figure2_performance_associations")


def exposure_heatmap() -> None:
    frame = pd.read_csv(DERIVED / "model_dataset_exposure_development.csv")
    code = {scope: index for index, scope in enumerate(COLORS)}
    matrix = frame.pivot(index="model_name", columns="evaluation_dataset_id", values="exposure_scope")
    numeric = matrix.apply(lambda column: column.map(code)).astype(float)
    from matplotlib.colors import ListedColormap
    fig, ax = plt.subplots(figsize=(14, 10))
    ax.imshow(numeric, aspect="auto", interpolation="nearest", cmap=ListedColormap(list(COLORS.values())), vmin=-0.5, vmax=3.5)
    ax.set_xticks(range(len(matrix.columns)), matrix.columns, rotation=60, ha="right", fontsize=7)
    ax.set_yticks(range(len(matrix.index)), matrix.index, fontsize=7)
    ax.set_xlabel("Evaluation dataset")
    ax.set_ylabel("Model/checkpoint")
    for spine in ax.spines.values():
        spine.set_visible(False)
    handles = [plt.Line2D([0], [0], marker="s", linestyle="", color=color, label=SHORT[scope], markersize=8) for scope, color in COLORS.items()]
    ax.legend(handles=handles, frameon=False, loc="lower center", bbox_to_anchor=(0.5, 1.01), ncol=4, fontsize=8)
    fig.tight_layout()
    save(fig, "figure3_registry_heatmap")


def main() -> None:
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10})
    exposure_by_group()
    coefficient_forest()
    exposure_heatmap()
    print(f"Wrote six figure files to {FIGURES}")


if __name__ == "__main__":
    main()
