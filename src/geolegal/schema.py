"""Canonical, dependency-free records for data and model outputs."""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass, field
from datetime import date
from enum import StrEnum
from pathlib import Path
from typing import Any, Iterable, Mapping, TypeVar


class Jurisdiction(StrEnum):
    NIGERIA = "NIGERIA"
    KENYA = "KENYA"
    EU = "EU"


class ApplicabilityLabel(StrEnum):
    APPLIES = "APPLIES"
    DOES_NOT_APPLY = "DOES_NOT_APPLY"
    INSUFFICIENT_INFORMATION = "INSUFFICIENT_INFORMATION"


class ReviewStatus(StrEnum):
    SYNTHETIC_UNVERIFIED = "SYNTHETIC_UNVERIFIED"
    PENDING_REVIEW = "PENDING_REVIEW"
    HUMAN_REVIEWED = "HUMAN_REVIEWED"
    LEGAL_REVIEWED = "LEGAL_REVIEWED"


class Split(StrEnum):
    TRAIN = "TRAIN"
    VALIDATION = "VALIDATION"
    EVALUATION_SMOKE = "EVALUATION_SMOKE"
    EVALUATION_HELD_OUT = "EVALUATION_HELD_OUT"


class ParseStatus(StrEnum):
    VALID = "VALID"
    INVALID_JSON = "INVALID_JSON"
    INVALID_CONTRACT = "INVALID_CONTRACT"


FRAMEWORK_BY_JURISDICTION = {
    Jurisdiction.NIGERIA: "Nigeria Data Protection Act 2023",
    Jurisdiction.KENYA: "Kenya Data Protection Act 2019",
    Jurisdiction.EU: "GDPR",
}


def content_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _date(value: object, field_name: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be an ISO date string")
    try:
        date.fromisoformat(value)
    except ValueError as exc:
        raise ValueError(f"{field_name} must be an ISO date") from exc
    return value


def _nonempty(value: object, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string")
    return value.strip()


@dataclass(frozen=True, slots=True)
class SourceRecord:
    source_id: str
    jurisdiction: Jurisdiction
    legal_framework: str
    provision: str
    title: str
    publisher: str
    url: str
    version_or_date: str
    accessed_at: str
    text: str
    content_hash: str
    license: str

    @classmethod
    def from_dict(cls, value: Mapping[str, Any]) -> SourceRecord:
        text = _nonempty(value.get("text"), "text")
        declared_hash = _nonempty(value.get("content_hash"), "content_hash")
        if declared_hash != content_hash(text):
            raise ValueError("content_hash does not match source text")
        jurisdiction = Jurisdiction(value.get("jurisdiction"))
        framework = _nonempty(value.get("legal_framework"), "legal_framework")
        if framework != FRAMEWORK_BY_JURISDICTION[jurisdiction]:
            raise ValueError("legal_framework does not match jurisdiction")
        url = _nonempty(value.get("url"), "url")
        if not url.startswith("https://"):
            raise ValueError("url must use https")
        return cls(
            source_id=_nonempty(value.get("source_id"), "source_id"),
            jurisdiction=jurisdiction,
            legal_framework=framework,
            provision=_nonempty(value.get("provision"), "provision"),
            title=_nonempty(value.get("title"), "title"),
            publisher=_nonempty(value.get("publisher"), "publisher"),
            url=url,
            version_or_date=_nonempty(value.get("version_or_date"), "version_or_date"),
            accessed_at=_date(value.get("accessed_at"), "accessed_at"),
            text=text,
            content_hash=declared_hash,
            license=_nonempty(value.get("license"), "license"),
        )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class StatutoryBasis:
    source_id: str
    provision: str
    title: str
    publisher: str
    url: str
    version_or_date: str
    accessed_at: str
    content_hash: str

    @classmethod
    def from_dict(cls, value: Mapping[str, Any]) -> StatutoryBasis:
        return cls(
            source_id=_nonempty(value.get("source_id"), "source_id"),
            provision=_nonempty(value.get("provision"), "provision"),
            title=_nonempty(value.get("title"), "title"),
            publisher=_nonempty(value.get("publisher"), "publisher"),
            url=_nonempty(value.get("url"), "url"),
            version_or_date=_nonempty(value.get("version_or_date"), "version_or_date"),
            accessed_at=_date(value.get("accessed_at"), "accessed_at"),
            content_hash=_nonempty(value.get("content_hash"), "content_hash"),
        )


@dataclass(frozen=True, slots=True)
class Evidence:
    source_id: str
    provision: str
    excerpt: str

    @classmethod
    def from_dict(cls, value: Mapping[str, Any]) -> Evidence:
        return cls(
            source_id=_nonempty(value.get("source_id"), "source_id"),
            provision=_nonempty(value.get("provision"), "provision"),
            excerpt=_nonempty(value.get("excerpt"), "excerpt"),
        )


@dataclass(frozen=True, slots=True)
class ScenarioRecord:
    id: str
    scenario: str
    jurisdiction: Jurisdiction
    question: str
    expected_label: ApplicabilityLabel
    legal_framework: str
    statutory_basis: tuple[StatutoryBasis, ...]
    evidence: tuple[Evidence, ...]
    effective_date: str
    uncertainty: Mapping[str, Any]
    provenance: Mapping[str, Any]
    review_status: ReviewStatus
    split: Split
    scenario_family_id: str

    @classmethod
    def from_dict(cls, value: Mapping[str, Any]) -> ScenarioRecord:
        jurisdiction = Jurisdiction(value.get("jurisdiction"))
        framework = _nonempty(value.get("legal_framework"), "legal_framework")
        if framework != FRAMEWORK_BY_JURISDICTION[jurisdiction]:
            raise ValueError("legal_framework does not match jurisdiction")
        basis = tuple(StatutoryBasis.from_dict(item) for item in value.get("statutory_basis", []))
        evidence = tuple(Evidence.from_dict(item) for item in value.get("evidence", []))
        status = ReviewStatus(value.get("review_status"))
        if status is ReviewStatus.LEGAL_REVIEWED and (not basis or not evidence):
            raise ValueError("LEGAL_REVIEWED records require statutory_basis and evidence")
        return cls(
            id=_nonempty(value.get("id"), "id"),
            scenario=_nonempty(value.get("scenario"), "scenario"),
            jurisdiction=jurisdiction,
            question=_nonempty(value.get("question"), "question"),
            expected_label=ApplicabilityLabel(value.get("expected_label")),
            legal_framework=framework,
            statutory_basis=basis,
            evidence=evidence,
            effective_date=_date(value.get("effective_date"), "effective_date"),
            uncertainty=dict(value.get("uncertainty") or {}),
            provenance=dict(value.get("provenance") or {}),
            review_status=status,
            split=Split(value.get("split")),
            scenario_family_id=_nonempty(value.get("scenario_family_id"), "scenario_family_id"),
        )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class PredictionRecord:
    scenario_id: str
    experiment_id: str
    run_id: str
    model_id: str
    model_revision: str
    dataset_revision: str
    prompt_version: str
    retrieval_revision: str | None
    raw_output: str
    parse_status: ParseStatus
    predicted_label: ApplicabilityLabel | None = None
    jurisdiction: Jurisdiction | None = None
    legal_framework: str | None = None
    explanation: str | None = None
    statutory_references: tuple[str, ...] = field(default_factory=tuple)
    missing_facts: tuple[str, ...] = field(default_factory=tuple)
    uncertainty: str | None = None
    retrieved_passage_ids: tuple[str, ...] = field(default_factory=tuple)
    runtime_metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.parse_status is ParseStatus.VALID:
            required = (self.predicted_label, self.jurisdiction, self.legal_framework, self.explanation)
            if any(item is None or item == "" for item in required):
                raise ValueError("VALID predictions require the complete output contract")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


T = TypeVar("T")


def read_jsonl(path: str | Path, factory: type[T]) -> list[T]:
    records: list[T] = []
    with Path(path).open(encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, 1):
            if not line.strip():
                continue
            try:
                records.append(factory.from_dict(json.loads(line)))  # type: ignore[attr-defined]
            except (ValueError, TypeError, json.JSONDecodeError) as exc:
                raise ValueError(f"{path}:{line_number}: {exc}") from exc
    return records


def write_jsonl(path: str | Path, records: Iterable[object]) -> None:
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("w", encoding="utf-8", newline="\n") as handle:
        for record in records:
            value = record.to_dict()  # type: ignore[attr-defined]
            handle.write(json.dumps(value, ensure_ascii=False, sort_keys=True) + "\n")
