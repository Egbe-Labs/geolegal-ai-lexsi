from __future__ import annotations

import json
import hashlib
import unittest
from collections import Counter
from pathlib import Path

from src.dataset import LegalScenario, load_scenarios
from src.evaluate import extract_label, score_predictions, validate_exploratory_artifact


class FirstMilestoneTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.scenarios = load_scenarios("data/eval/held_out_initial.jsonl")
        cls.proposed = load_scenarios("data/eval/held_out_proposed_v2.jsonl")
        cls.approved = load_scenarios("data/eval/held_out_approved_v1.jsonl")

    def test_dataset_has_five_scenarios_per_jurisdiction(self) -> None:
        self.assertEqual(len(self.scenarios), 15)
        self.assertEqual(Counter(item.jurisdiction for item in self.scenarios), {"NIGERIA": 5, "KENYA": 5, "EU": 5})
        self.assertTrue(all(item.review_status == "PENDING_REVIEW" for item in self.scenarios))

    def test_proposed_revision_preserves_ids_labels_and_status(self) -> None:
        original = {item.scenario_id: item for item in self.scenarios}
        proposed = {item.scenario_id: item for item in self.proposed}
        self.assertEqual(set(original), set(proposed))
        self.assertEqual(len(proposed), 15)
        self.assertEqual(Counter(item.jurisdiction for item in self.proposed), {"NIGERIA": 5, "KENYA": 5, "EU": 5})
        self.assertTrue(all(item.review_status == "PENDING_REVIEW" for item in self.proposed))
        self.assertTrue(all(proposed[key].expected_label == original[key].expected_label for key in original))

    def test_proposed_revision_changes_only_four_scenarios(self) -> None:
        original = {item.scenario_id: item for item in self.scenarios}
        proposed = {item.scenario_id: item for item in self.proposed}
        changed = {key for key in original if original[key].to_dict() != proposed[key].to_dict()}
        self.assertEqual(changed, {"NG-EVAL-003", "KE-EVAL-002", "KE-EVAL-003", "EU-EVAL-004"})
        self.assertIn("automatically collect, record, store", proposed["KE-EVAL-002"].scenario)
        self.assertIn("public international law", proposed["EU-EVAL-004"].scenario)

    def test_frozen_dataset_changes_only_review_status(self) -> None:
        proposed = {item.scenario_id: item.to_dict() for item in self.proposed}
        approved = {item.scenario_id: item.to_dict() for item in self.approved}
        self.assertEqual(set(approved), set(proposed))
        self.assertEqual(len(approved), 15)
        for scenario_id in proposed:
            self.assertEqual(approved[scenario_id]["review_status"], "LEGAL_REVIEWED")
            approved_without_status = approved[scenario_id] | {"review_status": "PENDING_REVIEW"}
            self.assertEqual(approved_without_status, proposed[scenario_id])

    def test_approval_manifest_matches_frozen_dataset(self) -> None:
        dataset_path = Path("data/eval/held_out_approved_v1.jsonl")
        manifest = json.loads(Path("data/eval/held_out_approved_v1.manifest.json").read_text(encoding="utf-8"))
        checksum = hashlib.sha256(dataset_path.read_bytes()).hexdigest()
        self.assertEqual(manifest["source_dataset"], "data/eval/held_out_proposed_v2.jsonl")
        self.assertEqual(manifest["record_count"], 15)
        self.assertEqual(manifest["approved_status"], "LEGAL_REVIEWED")
        self.assertEqual(manifest["approval_basis"], "user_reported")
        self.assertEqual(manifest["sha256"], checksum)

    def test_baseline_notebook_defaults_to_no_inference_and_versioned_outputs(self) -> None:
        notebook = json.loads(Path("notebooks/01_baseline.ipynb").read_text(encoding="utf-8"))
        source = "".join("".join(cell.get("source", [])) for cell in notebook["cells"])
        self.assertIn("DATASET_REVISION = 'held_out_approved_v1'", source)
        self.assertIn("RUN_INFERENCE = False", source)
        self.assertIn("baseline_predictions_{DATASET_REVISION}.jsonl", source)
        self.assertIn("baseline_metrics_{DATASET_REVISION}.json", source)
        self.assertIn("PREDICTIONS_PATH.open('x'", source)

    def test_schema_rejects_invalid_label(self) -> None:
        value = self.scenarios[0].to_dict() | {"expected_label": "MAYBE"}
        with self.assertRaisesRegex(ValueError, "expected_label"):
            LegalScenario.from_dict(value)

    def test_label_extraction_supports_json_and_legacy_smoke_shape(self) -> None:
        strict = json.dumps({"label": "APPLIES", "explanation": "test"})
        self.assertEqual(extract_label(strict), "APPLIES")
        self.assertEqual(extract_label("DECISION: DOES_NOT_APPLY\nEXPLANATION: test"), "DOES_NOT_APPLY")

    def test_malformed_outputs_are_not_coerced(self) -> None:
        self.assertIsNone(extract_label("The answer probably applies."))
        self.assertIsNone(extract_label('{"label":"MAYBE"}'))
        self.assertIsNone(extract_label("DECISION: APPLIES because reasons"))

    def test_real_exploratory_artifact_is_valid_but_not_scoreable(self) -> None:
        value = json.loads(Path("results/geolegal_baseline_test.json").read_text(encoding="utf-8"))
        validated = validate_exploratory_artifact(value)
        self.assertEqual(validated["extracted_label"], "INSUFFICIENT_INFORMATION")
        self.assertFalse(validated["score_eligible"])

    def test_pending_review_records_are_excluded_from_metrics(self) -> None:
        predictions = [
            {"scenario_id": item.scenario_id, "response": json.dumps({"label": item.expected_label})}
            for item in self.scenarios
        ]
        metrics = score_predictions(self.scenarios, predictions)
        self.assertEqual(metrics["status"], "NO_LEGAL_REVIEWED_SCENARIOS")
        self.assertEqual(metrics["scored_count"], 0)
        self.assertEqual(metrics["excluded_pending_review"], 15)
        self.assertIsNone(metrics["accuracy"])
        self.assertIsNone(metrics["macro_f1"])

    def test_legal_reviewed_record_can_be_scored(self) -> None:
        reviewed = LegalScenario.from_dict(self.scenarios[0].to_dict() | {"review_status": "LEGAL_REVIEWED"})
        metrics = score_predictions(
            [reviewed],
            [{"scenario_id": reviewed.scenario_id, "response": json.dumps({"label": reviewed.expected_label})}],
        )
        self.assertEqual(metrics["status"], "SCORED")
        self.assertEqual(metrics["accuracy"], 1.0)
        self.assertAlmostEqual(metrics["macro_f1"], 1 / 3)


if __name__ == "__main__":
    unittest.main()
