"""Deterministic output extraction and review-gated baseline scoring."""

from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path
from typing import Any, Iterable, Mapping

from src.dataset import LABELS, LegalScenario

DECISION_RE = re.compile(r"(?im)^\s*DECISION\s*:\s*(APPLIES|DOES_NOT_APPLY|INSUFFICIENT_INFORMATION)\s*$")


def extract_label(response: object) -> str | None:
    """Extract a closed label from strict JSON or the legacy smoke-test format."""
    if not isinstance(response, str) or not response.strip():
        return None
    try:
        value = json.loads(response)
    except json.JSONDecodeError:
        value = None
    if isinstance(value, dict) and set(value).issuperset({"label"}):
        label = value.get("label")
        return label if label in LABELS else None
    match = DECISION_RE.search(response)
    return match.group(1) if match else None


def validate_exploratory_artifact(value: Mapping[str, Any]) -> dict[str, Any]:
    required = {"model", "timestamp", "question", "response"}
    if set(value) != required:
        raise ValueError(f"exploratory artifact must contain exactly {sorted(required)}")
    if not all(isinstance(value[key], str) and value[key].strip() for key in required):
        raise ValueError("exploratory artifact values must be non-empty strings")
    return {
        "model": value["model"],
        "timestamp": value["timestamp"],
        "extracted_label": extract_label(value["response"]),
        "score_eligible": False,
        "classification": "EXPLORATORY_SMOKE_TEST",
    }


def score_predictions(
    scenarios: Iterable[LegalScenario], predictions: Iterable[Mapping[str, Any]]
) -> dict[str, Any]:
    scenario_list = list(scenarios)
    eligible = {item.scenario_id: item for item in scenario_list if item.score_eligible}
    excluded = len(scenario_list) - len(eligible)
    by_id: dict[str, Mapping[str, Any]] = {}
    for prediction in predictions:
        scenario_id = prediction.get("scenario_id")
        if not isinstance(scenario_id, str):
            raise ValueError("prediction scenario_id must be a string")
        if scenario_id in by_id:
            raise ValueError(f"duplicate prediction for {scenario_id}")
        by_id[scenario_id] = prediction
    correct = 0
    parsed = 0
    confusion = {label: {candidate: 0 for candidate in sorted(LABELS)} for label in sorted(LABELS)}
    per_jurisdiction_total: Counter[str] = Counter()
    per_jurisdiction_correct: Counter[str] = Counter()
    for scenario_id, scenario in eligible.items():
        prediction = by_id.get(scenario_id, {})
        label = extract_label(prediction.get("response", prediction.get("raw_output")))
        per_jurisdiction_total[scenario.jurisdiction] += 1
        if label is not None:
            parsed += 1
            confusion[scenario.expected_label][label] += 1
        if label == scenario.expected_label:
            correct += 1
            per_jurisdiction_correct[scenario.jurisdiction] += 1
    count = len(eligible)
    if not count:
        return {
            "status": "NO_LEGAL_REVIEWED_SCENARIOS",
            "scored_count": 0,
            "excluded_pending_review": excluded,
            "accuracy": None,
            "macro_f1": None,
            "parse_rate": None,
            "per_label": {},
            "per_jurisdiction_accuracy": {},
            "confusion_matrix": confusion,
        }
    per_label: dict[str, dict[str, float]] = {}
    f1_values: list[float] = []
    for label in sorted(LABELS):
        true_positive = confusion[label][label]
        false_positive = sum(confusion[actual][label] for actual in LABELS if actual != label)
        actual_total = sum(1 for scenario in eligible.values() if scenario.expected_label == label)
        false_negative = actual_total - true_positive
        precision = true_positive / (true_positive + false_positive) if true_positive + false_positive else 0.0
        recall = true_positive / (true_positive + false_negative) if true_positive + false_negative else 0.0
        f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
        f1_values.append(f1)
        per_label[label] = {"precision": precision, "recall": recall, "f1": f1}
    return {
        "status": "SCORED",
        "scored_count": count,
        "excluded_pending_review": excluded,
        "accuracy": correct / count,
        "macro_f1": sum(f1_values) / len(f1_values),
        "parse_rate": parsed / count,
        "per_label": per_label,
        "per_jurisdiction_accuracy": {
            key: per_jurisdiction_correct[key] / total
            for key, total in sorted(per_jurisdiction_total.items())
        },
        "confusion_matrix": confusion,
    }


def save_metrics(path: str | Path, metrics: Mapping[str, Any]) -> None:
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(metrics, indent=2, sort_keys=True) + "\n", encoding="utf-8")
