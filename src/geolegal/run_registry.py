"""Immutable experiment configuration and run metadata."""

from __future__ import annotations

import hashlib
import json
import platform
import sys
import tomllib
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from types import MappingProxyType
from typing import Any, Mapping

EXPERIMENT_ARMS = frozenset({"E1", "E2", "E3"})


def _canonical_json(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def fingerprint(value: object) -> str:
    """Return a stable SHA-256 fingerprint for JSON-compatible data."""
    return hashlib.sha256(_canonical_json(value).encode("utf-8")).hexdigest()


def load_config(path: str | Path) -> Mapping[str, Any]:
    """Load TOML and return a read-only top-level mapping."""
    with Path(path).open("rb") as handle:
        config = tomllib.load(handle)
    return MappingProxyType(config)


@dataclass(frozen=True, slots=True)
class RunMetadata:
    run_id: str
    experiment_arm: str
    created_at: str
    model_id: str
    model_revision: str
    dataset_revision: str
    prompt_version: str
    retrieval_revision: str | None
    config_fingerprint: str
    python_version: str
    platform: str

    def __post_init__(self) -> None:
        if self.experiment_arm not in EXPERIMENT_ARMS:
            raise ValueError(f"Unknown experiment arm: {self.experiment_arm}")
        if self.experiment_arm == "E1" and self.retrieval_revision is not None:
            raise ValueError("E1 must not have a retrieval revision")
        if self.experiment_arm in {"E2", "E3"} and not self.retrieval_revision:
            raise ValueError(f"{self.experiment_arm} requires a retrieval revision")

    def to_dict(self) -> dict[str, str | None]:
        return asdict(self)

    @classmethod
    def create(
        cls,
        *,
        experiment_arm: str,
        model_id: str,
        model_revision: str,
        dataset_revision: str,
        prompt_version: str,
        retrieval_revision: str | None,
        config: Mapping[str, Any],
        created_at: datetime | None = None,
    ) -> RunMetadata:
        timestamp = (created_at or datetime.now(UTC)).astimezone(UTC).isoformat()
        identity = {
            "experiment_arm": experiment_arm,
            "model_id": model_id,
            "model_revision": model_revision,
            "dataset_revision": dataset_revision,
            "prompt_version": prompt_version,
            "retrieval_revision": retrieval_revision,
            "config": dict(config),
            "created_at": timestamp,
        }
        return cls(
            run_id=fingerprint(identity)[:16],
            experiment_arm=experiment_arm,
            created_at=timestamp,
            model_id=model_id,
            model_revision=model_revision,
            dataset_revision=dataset_revision,
            prompt_version=prompt_version,
            retrieval_revision=retrieval_revision,
            config_fingerprint=fingerprint(dict(config)),
            python_version=platform.python_version(),
            platform=f"{sys.platform}:{platform.machine()}",
        )

    def write(self, path: str | Path) -> None:
        destination = Path(path)
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(_canonical_json(self.to_dict()) + "\n", encoding="utf-8")
