"""Thin AlignTune SFT adapter for the isolated Python 3.12 GPU runtime."""

from __future__ import annotations

import platform
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Callable

from geolegal.baseline import MODEL_ID, MODEL_REVISION

TrainerFactory = Callable[..., Any]


@dataclass(frozen=True, slots=True)
class AlignTuneSFTConfig:
    dataset_name: str
    output_dir: str
    model_name: str = MODEL_ID
    expected_model_revision: str = MODEL_REVISION
    backend: str = "trl"
    num_epochs: int = 1
    batch_size: int = 1
    gradient_accumulation_steps: int = 8
    learning_rate: float = 1e-4
    max_seq_length: int = 2048
    max_samples: int | None = None
    seed: int = 42
    lora_r: int = 16
    lora_alpha: int = 32
    lora_dropout: float = 0.05

    def __post_init__(self) -> None:
        if not self.dataset_name.strip() or "/" not in self.dataset_name:
            raise ValueError("dataset_name must be a versioned Hugging Face repository identifier")
        if self.model_name != MODEL_ID:
            raise ValueError(f"Only the approved model is allowed: {MODEL_ID}")
        if self.expected_model_revision != MODEL_REVISION:
            raise ValueError("Model revision differs from the approved pinned revision")
        if self.backend not in {"trl", "unsloth"}:
            raise ValueError("backend must be 'trl' or 'unsloth'")
        if self.num_epochs < 1 or self.batch_size < 1 or self.max_seq_length < 1:
            raise ValueError("epochs, batch size, and sequence length must be positive")

    def public_manifest(self) -> dict[str, Any]:
        return asdict(self)


def require_aligntune_runtime(version: tuple[int, int] | None = None) -> None:
    actual = version or tuple(map(int, platform.python_version_tuple()[:2]))
    if actual < (3, 12):
        raise RuntimeError(
            "Current AlignTune package metadata requires Python 3.12; "
            "run this adapter only in the approved isolated Colab runtime"
        )


def _official_factory() -> TrainerFactory:
    try:
        from aligntune.core.backend_factory import create_sft_trainer
    except ImportError as exc:
        raise RuntimeError("AlignTune is not installed in this isolated training runtime") from exc
    return create_sft_trainer


def create_trainer(
    config: AlignTuneSFTConfig,
    *,
    factory: TrainerFactory | None = None,
    runtime_version: tuple[int, int] | None = None,
) -> Any:
    """Create an AlignTune trainer using only documented SFT parameters."""
    require_aligntune_runtime(runtime_version)
    trainer_factory = factory or _official_factory()
    return trainer_factory(
        model_name=config.model_name,
        dataset_name=config.dataset_name,
        backend=config.backend,
        output_dir=config.output_dir,
        num_epochs=config.num_epochs,
        batch_size=config.batch_size,
        learning_rate=config.learning_rate,
        max_seq_length=config.max_seq_length,
        max_samples=config.max_samples,
        task_type="instruction_following",
        column_mapping={"instruction": "prompt", "output": "completion"},
        auto_detect_fields=False,
        gradient_accumulation_steps=config.gradient_accumulation_steps,
        seed=config.seed,
        peft_enabled=True,
        lora_r=config.lora_r,
        lora_alpha=config.lora_alpha,
        lora_dropout=config.lora_dropout,
        completion_only_loss=True,
    )


def run_training(config: AlignTuneSFTConfig, *, factory: TrainerFactory | None = None) -> Any:
    """Run training and save the resulting adapter/model; GPU execution only."""
    trainer = create_trainer(config, factory=factory)
    trainer.train()
    return trainer.save_model(output_dir=config.output_dir)


def write_manifest(config: AlignTuneSFTConfig, path: str | Path) -> None:
    """Write a human-readable TOML-like manifest without secrets."""
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    lines = [f'{key} = "{value}"' if isinstance(value, str) else f"{key} = {value}" for key, value in config.public_manifest().items() if value is not None]
    destination.write_text("\n".join(lines) + "\n", encoding="utf-8")
