from __future__ import annotations

import json
import tempfile
import unittest
from datetime import UTC, datetime
from pathlib import Path

from geolegal.run_registry import RunMetadata, fingerprint, load_config


class RunRegistryTests(unittest.TestCase):
    def test_fingerprint_ignores_mapping_order(self) -> None:
        self.assertEqual(fingerprint({"a": 1, "b": 2}), fingerprint({"b": 2, "a": 1}))

    def test_run_identity_is_deterministic_for_fixed_time(self) -> None:
        kwargs = {
            "experiment_arm": "E2",
            "model_id": "model",
            "model_revision": "revision",
            "dataset_revision": "dataset",
            "prompt_version": "v1",
            "retrieval_revision": "retrieval",
            "config": {"seed": 42},
            "created_at": datetime(2026, 11, 16, tzinfo=UTC),
        }
        self.assertEqual(RunMetadata.create(**kwargs).run_id, RunMetadata.create(**kwargs).run_id)

    def test_arm_retrieval_invariants(self) -> None:
        common = {
            "model_id": "model",
            "model_revision": "revision",
            "dataset_revision": "dataset",
            "prompt_version": "v1",
            "config": {},
        }
        with self.assertRaisesRegex(ValueError, "E1 must not"):
            RunMetadata.create(experiment_arm="E1", retrieval_revision="retrieval", **common)
        with self.assertRaisesRegex(ValueError, "E3 requires"):
            RunMetadata.create(experiment_arm="E3", retrieval_revision=None, **common)

    def test_config_load_and_metadata_write(self) -> None:
        config = load_config("configs/base.toml")
        self.assertEqual(config["model_id"], "CohereLabs/tiny-aya-global")
        run = RunMetadata.create(
            experiment_arm="E1",
            model_id=config["model_id"],
            model_revision=config["model_revision"],
            dataset_revision="test",
            prompt_version=config["prompt_version"],
            retrieval_revision=None,
            config=config,
            created_at=datetime(2026, 11, 16, tzinfo=UTC),
        )
        with tempfile.TemporaryDirectory(dir="artifacts") as directory:
            destination = Path(directory) / "run.json"
            run.write(destination)
            self.assertEqual(json.loads(destination.read_text(encoding="utf-8"))["run_id"], run.run_id)


if __name__ == "__main__":
    unittest.main()
