"""Deterministic closed-label metrics for frozen evaluation records."""

from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass
from typing import Any, Iterable, Mapping

from geolegal.schema import ApplicabilityLabel, ParseStatus, PredictionRecord, ScenarioRecord

LABELS = tuple(ApplicabilityLabel)


@dataclass(frozen=True, slots=True)
class EvaluationResult:
    metrics: Mapping[str, Any]
    rows: tuple[Mapping[str, Any], ...]


def _safe_divide(numerator: int, denominator: int) -> float:
    return numerator / denominator if denominator else 0.0


def evaluate(
    scenarios: Iterable[ScenarioRecord],
    predictions: Iterable[PredictionRecord],
) -> EvaluationResult:
    gold = {scenario.id: scenario for scenario in scenarios}
    predicted = list(predictions)
    if len({item.scenario_id for item in predicted}) != len(predicted):
        raise ValueError("Predictions contain duplicate scenario IDs")
    prediction_by_id = {item.scenario_id: item for item in predicted}
    unknown = set(prediction_by_id) - set(gold)
    if unknown:
        raise ValueError(f"Predictions reference unknown scenario IDs: {sorted(unknown)}")

    confusion = {actual.value: {label.value: 0 for label in LABELS} for actual in LABELS}
    confusion_invalid = {actual.value: 0 for actual in LABELS}
    jurisdiction_totals: Counter[str] = Counter()
    jurisdiction_correct: Counter[str] = Counter()
    rows: list[dict[str, Any]] = []
    true_positive: Counter[ApplicabilityLabel] = Counter()
    false_positive: Counter[ApplicabilityLabel] = Counter()
    false_negative: Counter[ApplicabilityLabel] = Counter()
    correct = 0
    parse_failures = 0

    for scenario_id, scenario in gold.items():
        prediction = prediction_by_id.get(scenario_id)
        actual = scenario.expected_label
        jurisdiction_totals[scenario.jurisdiction.value] += 1
        valid = prediction is not None and prediction.parse_status is ParseStatus.VALID
        label = prediction.predicted_label if valid else None
        is_correct = label == actual
        correct += is_correct
        jurisdiction_correct[scenario.jurisdiction.value] += is_correct
        if label is None:
            parse_failures += 1
            confusion_invalid[actual.value] += 1
            false_negative[actual] += 1
        else:
            confusion[actual.value][label.value] += 1
            if label == actual:
                true_positive[actual] += 1
            else:
                false_positive[label] += 1
                false_negative[actual] += 1
        rows.append(
            {
                "scenario_id": scenario_id,
                "jurisdiction": scenario.jurisdiction.value,
                "expected_label": actual.value,
                "predicted_label": label.value if label else None,
                "parse_status": prediction.parse_status.value if prediction else "MISSING",
                "correct": is_correct,
            }
        )

    per_label = {}
    f1_values = []
    for label in LABELS:
        precision = _safe_divide(true_positive[label], true_positive[label] + false_positive[label])
        recall = _safe_divide(true_positive[label], true_positive[label] + false_negative[label])
        f1 = _safe_divide(2 * precision * recall, precision + recall)
        f1_values.append(f1)
        per_label[label.value] = {"precision": precision, "recall": recall, "f1": f1}

    count = len(gold)
    insufficient = ApplicabilityLabel.INSUFFICIENT_INFORMATION
    metrics = {
        "count": count,
        "accuracy": _safe_divide(correct, count),
        "macro_f1": sum(f1_values) / len(LABELS),
        "parse_failure_rate": _safe_divide(parse_failures, count),
        "per_jurisdiction_accuracy": {
            name: _safe_divide(jurisdiction_correct[name], total)
            for name, total in sorted(jurisdiction_totals.items())
        },
        "per_label": per_label,
        "abstention": {
            "precision": per_label[insufficient.value]["precision"],
            "recall": per_label[insufficient.value]["recall"],
        },
        "confusion_matrix": confusion,
        "invalid_or_missing_by_actual_label": confusion_invalid,
    }
    return EvaluationResult(metrics=metrics, rows=tuple(rows))


def paired_comparison(
    left: EvaluationResult,
    right: EvaluationResult,
    *,
    left_name: str,
    right_name: str,
) -> Mapping[str, Any]:
    left_rows = {row["scenario_id"]: row for row in left.rows}
    right_rows = {row["scenario_id"]: row for row in right.rows}
    if set(left_rows) != set(right_rows):
        raise ValueError("Paired comparisons require identical scenario IDs")
    improved = regressed = unchanged = 0
    for scenario_id in left_rows:
        before = bool(left_rows[scenario_id]["correct"])
        after = bool(right_rows[scenario_id]["correct"])
        improved += not before and after
        regressed += before and not after
        unchanged += before == after
    return {
        "left": left_name,
        "right": right_name,
        "count": len(left_rows),
        "accuracy_delta": right.metrics["accuracy"] - left.metrics["accuracy"],
        "macro_f1_delta": right.metrics["macro_f1"] - left.metrics["macro_f1"],
        "improved": improved,
        "regressed": regressed,
        "unchanged": unchanged,
    }
