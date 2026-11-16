from __future__ import annotations

import unittest

from geolegal.schema import (
    ApplicabilityLabel,
    ParseStatus,
    PredictionRecord,
    ReviewStatus,
    ScenarioRecord,
    SourceRecord,
    content_hash,
)


def source_data() -> dict:
    text = "Illustrative source text; not a legal authority."
    return {
        "source_id": "src-1",
        "jurisdiction": "EU",
        "legal_framework": "GDPR",
        "provision": "test provision",
        "title": "Test source",
        "publisher": "Test publisher",
        "url": "https://example.test/source",
        "version_or_date": "test-only",
        "accessed_at": "2026-11-16",
        "text": text,
        "content_hash": content_hash(text),
        "license": "test-only",
    }


def scenario_data() -> dict:
    return {
        "id": "scenario-1",
        "scenario": "A deliberately fictional smoke-test scenario.",
        "jurisdiction": "EU",
        "question": "Does the named framework apply?",
        "expected_label": "INSUFFICIENT_INFORMATION",
        "legal_framework": "GDPR",
        "statutory_basis": [],
        "evidence": [],
        "effective_date": "2026-11-16",
        "uncertainty": {"missing_facts": ["establishment"]},
        "provenance": {"origin": "unit-test"},
        "review_status": "SYNTHETIC_UNVERIFIED",
        "split": "EVALUATION_SMOKE",
        "scenario_family_id": "family-1",
    }


class SchemaTests(unittest.TestCase):
    def test_source_hash_is_verified(self) -> None:
        source = SourceRecord.from_dict(source_data())
        self.assertEqual(source.jurisdiction.value, "EU")
        invalid = source_data() | {"content_hash": "0" * 64}
        with self.assertRaisesRegex(ValueError, "does not match"):
            SourceRecord.from_dict(invalid)

    def test_framework_must_match_jurisdiction(self) -> None:
        with self.assertRaisesRegex(ValueError, "does not match"):
            ScenarioRecord.from_dict(scenario_data() | {"legal_framework": "NDPA 2023"})

    def test_unreviewed_scenario_can_lack_gold_evidence(self) -> None:
        scenario = ScenarioRecord.from_dict(scenario_data())
        self.assertEqual(scenario.expected_label, ApplicabilityLabel.INSUFFICIENT_INFORMATION)
        self.assertEqual(scenario.review_status, ReviewStatus.SYNTHETIC_UNVERIFIED)

    def test_legal_review_requires_evidence(self) -> None:
        with self.assertRaisesRegex(ValueError, "require statutory_basis"):
            ScenarioRecord.from_dict(scenario_data() | {"review_status": "LEGAL_REVIEWED"})

    def test_valid_prediction_requires_complete_contract(self) -> None:
        common = {
            "scenario_id": "scenario-1",
            "experiment_id": "E1",
            "run_id": "run",
            "model_id": "model",
            "model_revision": "revision",
            "dataset_revision": "dataset",
            "prompt_version": "v1",
            "retrieval_revision": None,
            "raw_output": "{}",
        }
        with self.assertRaisesRegex(ValueError, "complete output contract"):
            PredictionRecord(parse_status=ParseStatus.VALID, **common)
        invalid = PredictionRecord(parse_status=ParseStatus.INVALID_JSON, **common)
        self.assertIsNone(invalid.predicted_label)


if __name__ == "__main__":
    unittest.main()
