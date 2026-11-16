"""Validation and JSONL I/O for the first held-out evaluation dataset."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import date
from pathlib import Path
from typing import Iterable, Mapping, Any

LABELS = frozenset({"APPLIES", "DOES_NOT_APPLY", "INSUFFICIENT_INFORMATION"})
JURISDICTIONS = frozenset({"NIGERIA", "KENYA", "EU"})
REVIEW_STATUSES = frozenset({"PENDING_REVIEW", "LEGAL_REVIEWED"})


def _text(value: object, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name} must be a non-empty string")
    return value.strip()


@dataclass(frozen=True, slots=True)
class LegalScenario:
    scenario_id: str
    jurisdiction: str
    scenario: str
    question: str
    expected_label: str
    statutory_basis: tuple[str, ...]
    source_url: str
    source_version_date: str
    review_status: str

    @classmethod
    def from_dict(cls, value: Mapping[str, Any]) -> "LegalScenario":
        jurisdiction = _text(value.get("jurisdiction"), "jurisdiction")
        label = _text(value.get("expected_label"), "expected_label")
        status = _text(value.get("review_status"), "review_status")
        if jurisdiction not in JURISDICTIONS:
            raise ValueError(f"jurisdiction must be one of {sorted(JURISDICTIONS)}")
        if label not in LABELS:
            raise ValueError(f"expected_label must be one of {sorted(LABELS)}")
        if status not in REVIEW_STATUSES:
            raise ValueError(f"review_status must be one of {sorted(REVIEW_STATUSES)}")
        basis = value.get("statutory_basis")
        if not isinstance(basis, list) or not basis or not all(isinstance(item, str) and item.strip() for item in basis):
            raise ValueError("statutory_basis must be a non-empty list of strings")
        source_url = _text(value.get("source_url"), "source_url")
        if not source_url.startswith("https://"):
            raise ValueError("source_url must use https")
        version_date = _text(value.get("source_version_date"), "source_version_date")
        try:
            date.fromisoformat(version_date)
        except ValueError as exc:
            raise ValueError("source_version_date must be an ISO date") from exc
        return cls(
            scenario_id=_text(value.get("scenario_id"), "scenario_id"),
            jurisdiction=jurisdiction,
            scenario=_text(value.get("scenario"), "scenario"),
            question=_text(value.get("question"), "question"),
            expected_label=label,
            statutory_basis=tuple(item.strip() for item in basis),
            source_url=source_url,
            source_version_date=version_date,
            review_status=status,
        )

    @property
    def score_eligible(self) -> bool:
        return self.review_status == "LEGAL_REVIEWED"

    def to_dict(self) -> dict[str, Any]:
        result = asdict(self)
        result["statutory_basis"] = list(self.statutory_basis)
        return result


def load_scenarios(path: str | Path) -> list[LegalScenario]:
    records: list[LegalScenario] = []
    seen: set[str] = set()
    with Path(path).open(encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, 1):
            if not line.strip():
                continue
            try:
                record = LegalScenario.from_dict(json.loads(line))
            except (json.JSONDecodeError, TypeError, ValueError) as exc:
                raise ValueError(f"{path}:{line_number}: {exc}") from exc
            if record.scenario_id in seen:
                raise ValueError(f"{path}:{line_number}: duplicate scenario_id {record.scenario_id}")
            seen.add(record.scenario_id)
            records.append(record)
    return records


def write_scenarios(path: str | Path, records: Iterable[LegalScenario]) -> None:
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("w", encoding="utf-8", newline="\n") as handle:
        for record in records:
            handle.write(json.dumps(record.to_dict(), ensure_ascii=False, sort_keys=True) + "\n")
