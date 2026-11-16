from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from geolegal.finetune import AlignTuneSFTConfig, create_trainer, require_aligntune_runtime, write_manifest


class FakeTrainer:
    pass


class RecordingFactory:
    def __init__(self) -> None:
        self.kwargs = None

    def __call__(self, **kwargs):
        self.kwargs = kwargs
        return FakeTrainer()


class FineTuneTests(unittest.TestCase):
    def test_python_311_is_rejected_for_current_aligntune(self) -> None:
        with self.assertRaisesRegex(RuntimeError, "Python 3.12"):
            require_aligntune_runtime((3, 11))

    def test_only_approved_model_and_revision_are_allowed(self) -> None:
        with self.assertRaisesRegex(ValueError, "approved model"):
            AlignTuneSFTConfig(dataset_name="owner/data", output_dir="out", model_name="other/model")
        with self.assertRaisesRegex(ValueError, "pinned revision"):
            AlignTuneSFTConfig(dataset_name="owner/data", output_dir="out", expected_model_revision="main")

    def test_documented_factory_parameters(self) -> None:
        config = AlignTuneSFTConfig(dataset_name="owner/geolegal-train", output_dir="artifacts/adapter")
        factory = RecordingFactory()
        trainer = create_trainer(config, factory=factory, runtime_version=(3, 12))
        self.assertIsInstance(trainer, FakeTrainer)
        self.assertEqual(factory.kwargs["model_name"], "CohereLabs/tiny-aya-global")
        self.assertEqual(factory.kwargs["column_mapping"], {"instruction": "prompt", "output": "completion"})
        self.assertTrue(factory.kwargs["peft_enabled"])
        self.assertNotIn("revision", factory.kwargs)

    def test_manifest_contains_no_token_field(self) -> None:
        config = AlignTuneSFTConfig(dataset_name="owner/geolegal-train", output_dir="artifacts/adapter")
        with tempfile.TemporaryDirectory(dir="artifacts") as directory:
            path = Path(directory) / "training.toml"
            write_manifest(config, path)
            text = path.read_text(encoding="utf-8")
        self.assertIn("expected_model_revision", text)
        self.assertNotIn("token", text.casefold())


if __name__ == "__main__":
    unittest.main()
