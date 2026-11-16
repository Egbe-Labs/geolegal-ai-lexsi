from __future__ import annotations

import json
import unittest

from geolegal.baseline import build_messages, parse_output, run_scenario
from geolegal.retrieval import LexicalRetriever, prompt_passages
from geolegal.schema import Jurisdiction, SourceRecord, content_hash
from geolegal.schema import ParseStatus, ScenarioRecord
from test_schema import scenario_data, source_data


class FakeGenerator:
    model_id = "fake/model"
    model_revision = "test-revision"

    def __init__(self, output: str) -> None:
        self.output = output

    def generate(self, messages):
        return self.output, {"fake": True, "message_count": len(messages)}


def valid_output() -> str:
    return json.dumps(
        {
            "label": "INSUFFICIENT_INFORMATION",
            "jurisdiction": "EU",
            "legal_framework": "GDPR",
            "explanation": "The supplied facts do not establish the relevant nexus.",
            "statutory_references": [],
            "missing_facts": ["establishment"],
            "uncertainty": "Territorial facts are missing.",
        }
    )


class BaselineTests(unittest.TestCase):
    def setUp(self) -> None:
        self.scenario = ScenarioRecord.from_dict(scenario_data())

    def test_prompt_excludes_gold_label_and_evidence(self) -> None:
        messages = build_messages(self.scenario)
        user_content = messages[1]["content"]
        self.assertNotIn(self.scenario.expected_label.value, user_content)
        self.assertNotIn("unit-test", user_content)
        self.assertIn("NONE (baseline without retrieval)", user_content)

    def test_parser_rejects_prose_and_extra_keys(self) -> None:
        self.assertEqual(parse_output("Label: APPLIES")[0], ParseStatus.INVALID_JSON)
        value = json.loads(valid_output()) | {"extra": True}
        self.assertEqual(parse_output(json.dumps(value))[0], ParseStatus.INVALID_CONTRACT)

    def test_e1_fake_generation_produces_valid_prediction(self) -> None:
        prediction = run_scenario(
            self.scenario,
            FakeGenerator(valid_output()),
            experiment_id="E1",
            run_id="run-1",
            dataset_revision="dataset-1",
            prompt_version="v1",
        )
        self.assertEqual(prediction.parse_status, ParseStatus.VALID)
        self.assertIsNone(prediction.retrieval_revision)
        self.assertTrue(prediction.runtime_metadata["fake"])

    def test_e1_rejects_retrieval(self) -> None:
        with self.assertRaisesRegex(ValueError, "cannot receive retrieval"):
            run_scenario(
                self.scenario,
                FakeGenerator(valid_output()),
                experiment_id="E1",
                run_id="run-1",
                dataset_revision="dataset-1",
                prompt_version="v1",
                retrieval_revision="retrieval-1",
            )

    def test_e2_uses_fingerprinted_retrieval(self) -> None:
        text = "territorial establishment processing data"
        source = SourceRecord.from_dict(
            source_data()
            | {"text": text, "content_hash": content_hash(text)}
        )
        retriever = LexicalRetriever([source])
        passages = prompt_passages(retriever.retrieve("territorial establishment", Jurisdiction.EU))
        prediction = run_scenario(
            self.scenario,
            FakeGenerator(valid_output()),
            experiment_id="E2",
            run_id="run-2",
            dataset_revision="dataset-1",
            prompt_version="v1",
            retrieval_revision=retriever.revision,
            retrieved_passages=passages,
        )
        self.assertEqual(prediction.retrieved_passage_ids, ("src-1",))


if __name__ == "__main__":
    unittest.main()
