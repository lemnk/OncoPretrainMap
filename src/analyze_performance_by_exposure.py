"""Descriptive, noncausal analysis of benchmark performance by exposure class."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats


ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "data" / "derived" / "pathbench_exposure_audit_development.csv"
REPORTS = ROOT / "reports"
REFERENCE = "D1_no_detected_evidence_or_insufficient_disclosure"
CONTRASTS = ["D0_documented_disjoint", "D3_exact_dataset_exposure"]


def cluster_meat(x: np.ndarray, residual: np.ndarray, labels: np.ndarray) -> np.ndarray:
    meat = np.zeros((x.shape[1], x.shape[1]))
    for label in np.unique(labels):
        score = x[labels == label].T @ residual[labels == label]
        meat += np.outer(score, score)
    return meat


def fixed_effects_fit(frame: pd.DataFrame, outcome: str) -> list[dict[str, object]]:
    exposure = pd.DataFrame(
        {scope: (frame["exposure_scope"] == scope).astype(float) for scope in CONTRASTS}
    )
    model_dummies = pd.get_dummies(frame["model_id"], prefix="model", drop_first=True, dtype=float)
    task_dummies = pd.get_dummies(frame["task_id"], prefix="task", drop_first=True, dtype=float)
    design = pd.concat(
        [pd.Series(1.0, index=frame.index, name="intercept"), exposure, model_dummies, task_dummies],
        axis=1,
    )
    x = design.to_numpy(float)
    y = frame[outcome].to_numpy(float)
    bread = np.linalg.pinv(x.T @ x)
    beta = bread @ x.T @ y
    residual = y - x @ beta
    n, k = x.shape

    model_labels = frame["model_id"].to_numpy()
    task_labels = frame["task_id"].to_numpy()
    observation_labels = np.arange(n)
    gm = len(np.unique(model_labels))
    gt = len(np.unique(task_labels))
    model_correction = (gm / (gm - 1)) * ((n - 1) / (n - k))
    task_correction = (gt / (gt - 1)) * ((n - 1) / (n - k))
    observation_correction = n / (n - k)
    meat = (
        model_correction * cluster_meat(x, residual, model_labels)
        + task_correction * cluster_meat(x, residual, task_labels)
        - observation_correction * cluster_meat(x, residual, observation_labels)
    )
    covariance = bread @ meat @ bread
    degrees_freedom = min(gm, gt) - 1
    critical = stats.t.ppf(0.975, degrees_freedom)

    results: list[dict[str, object]] = []
    for scope in CONTRASTS:
        index = design.columns.get_loc(scope)
        variance = covariance[index, index]
        standard_error = float(np.sqrt(variance)) if variance >= 0 else float("nan")
        estimate = float(beta[index])
        statistic = estimate / standard_error if standard_error > 0 else float("nan")
        p_value = float(2 * stats.t.sf(abs(statistic), degrees_freedom))
        results.append(
            {
                "outcome": outcome,
                "contrast_scope": scope,
                "reference_scope": REFERENCE,
                "estimate": estimate,
                "two_way_clustered_se": standard_error,
                "ci95_low": estimate - critical * standard_error,
                "ci95_high": estimate + critical * standard_error,
                "p_value": p_value,
                "model_clusters": gm,
                "task_clusters": gt,
                "observations": n,
                "design_rank": int(np.linalg.matrix_rank(x)),
                "design_columns": k,
                "interpretation": "Descriptive model-and-task fixed-effects association; not a causal contamination effect.",
            }
        )
    return results


def main() -> None:
    frame = pd.read_csv(INPUT)
    frame["auroc"] = pd.to_numeric(frame["auroc"], errors="raise")
    frame["auprc"] = pd.to_numeric(frame["auprc"], errors="raise")
    frame["task_auroc_percentile"] = frame.groupby("task_id")["auroc"].rank(pct=True, method="average")

    summaries: list[dict[str, object]] = []
    for scope, group in frame.groupby("exposure_scope", sort=True):
        summaries.append(
            {
                "exposure_scope": scope,
                "rows": len(group),
                "models": group["model_id"].nunique(),
                "tasks": group["task_id"].nunique(),
                "mean_auroc": group["auroc"].mean(),
                "median_auroc": group["auroc"].median(),
                "mean_auprc": group["auprc"].mean(),
                "median_auprc": group["auprc"].median(),
                "mean_within_task_auroc_percentile": group["task_auroc_percentile"].mean(),
            }
        )
    summary_frame = pd.DataFrame(summaries)
    summary_frame.to_csv(REPORTS / "performance_by_exposure_summary.csv", index=False)

    estimates = fixed_effects_fit(frame, "auroc") + fixed_effects_fit(frame, "auprc")
    estimate_frame = pd.DataFrame(estimates)
    estimate_frame.to_csv(REPORTS / "performance_exposure_fixed_effects.csv", index=False)

    group_table = pd.crosstab(frame["dataset_group"], frame["benchmark_exposure_scope"])
    group_table.to_csv(REPORTS / "exposure_by_benchmark_group.csv")
    result = {
        "analysis_type": "post-protocol descriptive sensitivity analysis",
        "benchmark_rows": len(frame),
        "models": frame["model_id"].nunique(),
        "tasks": frame["task_id"].nunique(),
        "summary_records": summaries,
        "fixed_effects_records": estimates,
        "limitations": [
            "This post-protocol regression is underpowered and uninformative for performance effects.",
            "Only 32 model and 41 task clusters were available for two-way clustered inference.",
            "Registry D3 exposure is concentrated in TCGA tasks.",
            "Exposure was not randomized and disclosure quality determines classification.",
            "D1 means unresolved, not independent or unexposed.",
            "Fixed effects do not remove unmeasured model-by-task interactions.",
            "Associations must not be interpreted as performance inflation caused by exposure.",
        ],
    }
    (REPORTS / "performance_exposure_analysis.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
