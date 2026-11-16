from __future__ import annotations

import unittest

from geolegal.evaluation import evaluate, paired_comparison
from geolegal.schema import (
    ApplicabilityLabel,
    Jurisdiction,
    ParseStatus,
    PredictionRecord,
    ScenarioRecord,
)
from test_schema import scenario_data


def scenario(identifier: str, label: str, jurisdiction: str = "EU") -> ScenarioRecord:
    frameworks = {"EU": "GDPR", "KENYA": "Kenya Data Protection Act 2019", "NIGERIA": "Nigeria Data Protection Act 2023"}
    return ScenarioRecord.from_dict(
        scenario_data()
        | {
            "id": identifier,
            "scenario_family_id": f"family-{identifier}",
            "expected_label": label,
            "jurisdiction": jurisdiction,
            "legal_framework": frameworks[jurisdiction],
        }
    )


def prediction(item: ScenarioRecord, label: ApplicabilityLabel | None) -> PredictionRecord:
    valid = label is not None
    return PredictionRecord(
        scenario_id=item.id,
        experiment_id="E1",
        run_id="run",
        model_id="fake",
        model_revision="test",
        dataset_revision="data",
        prompt_version="v1",
        retrieval_revision=None,
        raw_output="{}" if valid else "invalid",
        parse_status=ParseStatus.VALID if valid else ParseStatus.INVALID_JSON,
        predicted_label=label,
        jurisdiction=item.jurisdiction if valid else None,
        legal_framework=item.legal_framework if valid else None,
        explanation="test" if valid else None,
    )


class EvaluationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.scenarios = [
            scenario("a", "APPLIES", "EU"),
            scenario("b", "DOES_NOT_APPLY", "KENYA"),
            scenario("c", "INSUFFICIENT_INFORMATION", "NIGERIA"),
        ]

    def test_perfect_metrics(self) -> None:
        predictions = [prediction(item, item.expected_label) for item in self.scenarios]
        result = evaluate(self.scenarios, predictions)
        self.assertEqual(result.metrics["accuracy"], 1.0)
        self.assertEqual(result.metrics["macro_f1"], 1.0)
        self.assertEqual(result.metrics["parse_failure_rate"], 0.0)

    def test_missing_and_invalid_predictions_count_as_incorrect(self) -> None:
        result = evaluate(self.scenarios, [prediction(self.scenarios[0], None)])
        self.assertEqual(result.metrics["accuracy"], 0.0)
        self.assertEqual(result.metrics["parse_failure_rate"], 1.0)

    def test_duplicate_predictions_are_rejected(self) -> None:
        item = prediction(self.scenarios[0], ApplicabilityLabel.APPLIES)
        with self.assertRaisesRegex(ValueError, "duplicate"):
            evaluate(self.scenarios, [item, item])

    def test_paired_comparison(self) -> None:
        before = evaluate(self.scenarios, [])
        after = evaluate(self.scenarios, [prediction(item, item.expected_label) for item in self.scenarios])
        comparison = paired_comparison(before, after, left_name="E1", right_name="E3")
        self.assertEqual(comparison["improved"], 3)
        self.assertEqual(comparison["accuracy_delta"], 1.0)


if __name__ == "__main__":
    unittest.main()
