"""Prepare review-gated training candidates without exposing held-out examples."""

from __future__ import annotations

import hashlib
import json
import re
import unicodedata
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

LABELS = {"APPLIES", "DOES_NOT_APPLY", "INSUFFICIENT_INFORMATION"}
SPLITS = {"TRAIN", "VALIDATION"}
PROTECTED_FILES = (
    "data/eval/held_out_initial.jsonl",
    "data/eval/held_out_proposed_v2.jsonl",
    "data/eval/held_out_approved_v1.jsonl",
)
TOKEN_NGRAM_SIZE = 3
CHAR_NGRAM_SIZE = 5
TOKEN_SIMILARITY_THRESHOLD = 0.45
CHAR_SIMILARITY_THRESHOLD = 0.55


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def normalize_text(value: str) -> str:
    normalized = unicodedata.normalize("NFKC", value).casefold()
    return " ".join(re.findall(r"[a-z0-9]+", normalized))


def _ngrams(parts: Sequence[str], size: int) -> set[tuple[str, ...]]:
    if not parts:
        return set()
    if len(parts) < size:
        return {tuple(parts)}
    return {tuple(parts[index : index + size]) for index in range(len(parts) - size + 1)}


def token_ngrams(value: str, size: int = TOKEN_NGRAM_SIZE) -> set[tuple[str, ...]]:
    return _ngrams(normalize_text(value).split(), size)


def char_ngrams(value: str, size: int = CHAR_NGRAM_SIZE) -> set[str]:
    compact = normalize_text(value).replace(" ", "_")
    if not compact:
        return set()
    if len(compact) < size:
        return {compact}
    return {compact[index : index + size] for index in range(len(compact) - size + 1)}


def jaccard(left: set[Any], right: set[Any]) -> float:
    if not left and not right:
        return 1.0
    if not left or not right:
        return 0.0
    return len(left & right) / len(left | right)


def read_jsonl(path: str | Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    with Path(path).open(encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, 1):
            if not line.strip():
                continue
            value = json.loads(line)
            if not isinstance(value, dict):
                raise ValueError(f"{path}:{line_number}: expected an object")
            records.append(value)
    return records


def write_jsonl(path: str | Path, records: Iterable[Mapping[str, Any]]) -> None:
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("w", encoding="utf-8", newline="\n") as handle:
        for record in records:
            handle.write(json.dumps(dict(record), ensure_ascii=False, sort_keys=True) + "\n")


def protected_registry(repo_root: str | Path) -> dict[str, Any]:
    root = Path(repo_root)
    datasets: list[dict[str, Any]] = []
    signatures: list[dict[str, Any]] = []
    for relative in PROTECTED_FILES:
        path = root / relative
        records = read_jsonl(path)
        datasets.append(
            {
                "path": relative,
                "record_count": len(records),
                "sha256": sha256_bytes(path.read_bytes()),
            }
        )
        for record in records:
            combined = f"{record['scenario']} {record['question']}"
            normalized = normalize_text(combined)
            signatures.append(
                {
                    "source_dataset": relative,
                    "scenario_id": record["scenario_id"],
                    "scenario_family_id": f"protected::{record['scenario_id']}",
                    "normalized_sha256": sha256_bytes(normalized.encode("utf-8")),
                    "scenario_sha256": sha256_bytes(record["scenario"].encode("utf-8")),
                    "normalized_text": normalized,
                }
            )
    return {
        "registry_version": "protected-held-out-v1",
        "protected_datasets": datasets,
        "signature_count": len(signatures),
        "unique_scenario_ids": len({item["scenario_id"] for item in signatures}),
        "signatures": signatures,
    }


@dataclass(frozen=True, slots=True)
class Candidate:
    candidate_id: str
    scenario_family_id: str
    split: str
    jurisdiction: str
    legal_framework: str
    scenario: str
    question: str
    expected_label: str
    statutory_basis: tuple[str, ...]
    source_url: str
    source_version_date: str
    statutory_explanation: str
    missing_facts: tuple[str, ...]
    review_status: str = "PENDING_REVIEW"
    origin: str = "SYNTHETIC_UNVERIFIED"

    @classmethod
    def from_dict(cls, value: Mapping[str, Any]) -> "Candidate":
        required = {
            "candidate_id", "scenario_family_id", "split", "jurisdiction",
            "legal_framework", "scenario", "question", "expected_label",
            "statutory_basis", "source_url", "source_version_date",
            "statutory_explanation", "missing_facts", "review_status", "origin",
        }
        if set(value) != required:
            raise ValueError(f"candidate fields must be exactly {sorted(required)}")
        if value["split"] not in SPLITS:
            raise ValueError(f"invalid split: {value['split']}")
        if value["expected_label"] not in LABELS:
            raise ValueError(f"invalid label: {value['expected_label']}")
        if value["review_status"] not in {"PENDING_REVIEW", "LEGAL_REVIEWED"}:
            raise ValueError("invalid review_status")
        if value["origin"] != "SYNTHETIC_UNVERIFIED":
            raise ValueError("candidate origin must remain SYNTHETIC_UNVERIFIED")
        for name in required - {"statutory_basis", "missing_facts"}:
            if not isinstance(value[name], str) or not value[name].strip():
                raise ValueError(f"{name} must be a non-empty string")
        if not isinstance(value["statutory_basis"], list) or not value["statutory_basis"]:
            raise ValueError("statutory_basis must be a non-empty list")
        if not isinstance(value["missing_facts"], list):
            raise ValueError("missing_facts must be a list")
        return cls(
            **{key: value[key] for key in required - {"statutory_basis", "missing_facts"}},
            statutory_basis=tuple(value["statutory_basis"]),
            missing_facts=tuple(value["missing_facts"]),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "candidate_id": self.candidate_id,
            "scenario_family_id": self.scenario_family_id,
            "split": self.split,
            "jurisdiction": self.jurisdiction,
            "legal_framework": self.legal_framework,
            "scenario": self.scenario,
            "question": self.question,
            "expected_label": self.expected_label,
            "statutory_basis": list(self.statutory_basis),
            "source_url": self.source_url,
            "source_version_date": self.source_version_date,
            "statutory_explanation": self.statutory_explanation,
            "missing_facts": list(self.missing_facts),
            "review_status": self.review_status,
            "origin": self.origin,
        }


def validate_candidates(records: Sequence[Candidate]) -> None:
    ids = [record.candidate_id for record in records]
    if len(ids) != len(set(ids)):
        raise ValueError("candidate IDs must be unique")
    split_by_family: dict[str, set[str]] = {}
    for record in records:
        split_by_family.setdefault(record.scenario_family_id, set()).add(record.split)
    crossing = sorted(family for family, splits in split_by_family.items() if len(splits) > 1)
    if crossing:
        raise ValueError(f"scenario families cross splits: {crossing}")


def leakage_report(records: Sequence[Candidate], registry: Mapping[str, Any]) -> dict[str, Any]:
    protected = list(registry["signatures"])
    protected_ids = {item["scenario_id"] for item in protected}
    protected_families = {item["scenario_family_id"] for item in protected}
    protected_normalized = {item["normalized_sha256"] for item in protected}
    id_overlaps: list[dict[str, str]] = []
    family_overlaps: list[dict[str, str]] = []
    normalized_matches: list[dict[str, str]] = []
    near_matches: list[dict[str, Any]] = []
    for record in records:
        combined = f"{record.scenario} {record.question}"
        normalized_hash = sha256_bytes(normalize_text(combined).encode("utf-8"))
        if record.candidate_id in protected_ids:
            id_overlaps.append({"candidate_id": record.candidate_id})
        if record.scenario_family_id in protected_families:
            family_overlaps.append({"candidate_id": record.candidate_id, "scenario_family_id": record.scenario_family_id})
        if normalized_hash in protected_normalized:
            normalized_matches.append({"candidate_id": record.candidate_id})
        candidate_token = token_ngrams(combined)
        candidate_char = char_ngrams(combined)
        for item in protected:
            protected_text = item["normalized_text"]
            token_score = jaccard(candidate_token, token_ngrams(protected_text))
            char_score = jaccard(candidate_char, char_ngrams(protected_text))
            if token_score >= TOKEN_SIMILARITY_THRESHOLD or char_score >= CHAR_SIMILARITY_THRESHOLD:
                near_matches.append(
                    {
                        "candidate_id": record.candidate_id,
                        "protected_scenario_id": item["scenario_id"],
                        "protected_source": item["source_dataset"],
                        "token_ngram_similarity": round(token_score, 4),
                        "character_ngram_similarity": round(char_score, 4),
                        "manual_review_status": "PENDING",
                    }
                )
    return {
        "report_version": "leakage-v1",
        "candidate_count": len(records),
        "protected_signature_count": len(protected),
        "thresholds": {
            "token_ngram_size": TOKEN_NGRAM_SIZE,
            "token_jaccard": TOKEN_SIMILARITY_THRESHOLD,
            "character_ngram_size": CHAR_NGRAM_SIZE,
            "character_jaccard": CHAR_SIMILARITY_THRESHOLD,
        },
        "id_overlaps": id_overlaps,
        "family_overlaps": family_overlaps,
        "normalized_exact_matches": normalized_matches,
        "flagged_near_matches": near_matches,
        "blocking_issue_count": len(id_overlaps) + len(family_overlaps) + len(normalized_matches) + len(near_matches),
        "export_allowed": False,
        "export_blockers": [
            "All candidate records require human legal review.",
            "Every flagged near-match requires documented manual resolution.",
        ],
    }


def dataset_manifest(records: Sequence[Candidate], dataset_path: str | Path, report: Mapping[str, Any]) -> dict[str, Any]:
    path = Path(dataset_path)
    split_jurisdiction_labels: dict[str, dict[str, dict[str, int]]] = {}
    for split in sorted(SPLITS):
        split_jurisdiction_labels[split] = {}
        for jurisdiction in sorted({record.jurisdiction for record in records}):
            counts = Counter(
                record.expected_label
                for record in records
                if record.split == split and record.jurisdiction == jurisdiction
            )
            split_jurisdiction_labels[split][jurisdiction] = {
                label: counts[label] for label in sorted(LABELS)
            }
    return {
        "dataset_revision": "candidate-training-v1",
        "candidate_file": path.as_posix(),
        "candidate_file_sha256": sha256_bytes(path.read_bytes()),
        "record_count": len(records),
        "split_distribution": dict(sorted(Counter(record.split for record in records).items())),
        "jurisdiction_distribution": dict(sorted(Counter(record.jurisdiction for record in records).items())),
        "label_distribution": dict(sorted(Counter(record.expected_label for record in records).items())),
        "split_jurisdiction_label_distribution": split_jurisdiction_labels,
        "review_status_distribution": dict(sorted(Counter(record.review_status for record in records).items())),
        "origin": "SYNTHETIC_UNVERIFIED",
        "held_out_registry_version": "protected-held-out-v1",
        "leakage_report_version": report["report_version"],
        "export_status": "BLOCKED_PENDING_LEGAL_REVIEW",
        "notes": "No prompt/completion files are exported until legal approval and leakage clearance are both recorded.",
    }


def export_prompt_completion(
    records: Sequence[Candidate],
    report: Mapping[str, Any],
    train_path: str | Path,
    validation_path: str | Path,
) -> None:
    pending = [record.candidate_id for record in records if record.review_status != "LEGAL_REVIEWED"]
    unresolved = [item for item in report["flagged_near_matches"] if item["manual_review_status"] != "CLEARED"]
    hard_overlap = sum(len(report[key]) for key in ("id_overlaps", "family_overlaps", "normalized_exact_matches"))
    if pending or unresolved or hard_overlap:
        raise RuntimeError(
            f"export blocked: pending_legal_review={len(pending)}, "
            f"unresolved_near_matches={len(unresolved)}, hard_overlaps={hard_overlap}"
        )
    output: dict[str, list[dict[str, str]]] = {"TRAIN": [], "VALIDATION": []}
    for record in records:
        prompt = (
            f"Jurisdiction: {record.jurisdiction}\nScenario: {record.scenario}\n"
            f"Question: {record.question}\nReturn the required structured legal-applicability JSON."
        )
        completion = json.dumps(
            {
                "label": record.expected_label,
                "jurisdiction": record.jurisdiction,
                "legal_framework": record.legal_framework,
                "explanation": record.statutory_explanation,
                "statutory_references": list(record.statutory_basis),
                "missing_facts": list(record.missing_facts),
                "uncertainty": bool(record.missing_facts),
            },
            ensure_ascii=False,
            sort_keys=True,
        )
        output[record.split].append({"prompt": prompt, "completion": completion})
    write_jsonl(train_path, output["TRAIN"])
    write_jsonl(validation_path, output["VALIDATION"])
