"""Prompting, strict output parsing, and the verified Tiny Aya generation path."""

from __future__ import annotations

import json
import time
from dataclasses import dataclass
from typing import Any, Mapping, Protocol, Sequence

from geolegal.schema import (
    ApplicabilityLabel,
    Jurisdiction,
    ParseStatus,
    PredictionRecord,
    ScenarioRecord,
)

MODEL_ID = "CohereLabs/tiny-aya-global"
MODEL_REVISION = "af89d219b53ed9b13b8a4645f9c8028973510324"

SYSTEM_INSTRUCTION = """You are a research classifier for territorial applicability of privacy laws.
You are not a general legal chatbot and do not provide professional legal advice.
Use only the scenario and, when supplied, the authoritative source passages.
Do not invent statutes, provisions, citations, or missing facts.
Return one JSON object and no surrounding prose with exactly these keys:
label, jurisdiction, legal_framework, explanation, statutory_references, missing_facts, uncertainty.
label must be APPLIES, DOES_NOT_APPLY, or INSUFFICIENT_INFORMATION.
statutory_references and missing_facts must be JSON arrays of strings.
When necessary facts or support are absent, use INSUFFICIENT_INFORMATION and identify what is missing."""


class TextGenerator(Protocol):
    model_id: str
    model_revision: str

    def generate(self, messages: Sequence[Mapping[str, str]]) -> tuple[str, Mapping[str, Any]]: ...


def build_messages(
    scenario: ScenarioRecord,
    retrieved_passages: Sequence[Mapping[str, str]] = (),
) -> list[dict[str, str]]:
    sources = []
    for passage in retrieved_passages:
        sources.append(
            "\n".join(
                [
                    f"PASSAGE_ID: {passage['passage_id']}",
                    f"PROVISION: {passage['provision']}",
                    f"SOURCE_URL: {passage['url']}",
                    f"TEXT: {passage['text']}",
                ]
            )
        )
    source_block = "\n\n".join(sources) if sources else "NONE (baseline without retrieval)"
    user = (
        f"Scenario ID: {scenario.id}\n"
        f"Scenario: {scenario.scenario}\n"
        f"Jurisdiction under assessment: {scenario.jurisdiction.value}\n"
        f"Legal framework: {scenario.legal_framework}\n"
        f"Question: {scenario.question}\n\n"
        f"Authoritative source passages:\n{source_block}"
    )
    return [
        {"role": "system", "content": SYSTEM_INSTRUCTION},
        {"role": "user", "content": user},
    ]


def parse_output(raw_output: str) -> tuple[ParseStatus, dict[str, Any] | None]:
    try:
        value = json.loads(raw_output)
    except json.JSONDecodeError:
        return ParseStatus.INVALID_JSON, None
    if not isinstance(value, dict):
        return ParseStatus.INVALID_CONTRACT, None
    required = {
        "label",
        "jurisdiction",
        "legal_framework",
        "explanation",
        "statutory_references",
        "missing_facts",
        "uncertainty",
    }
    if set(value) != required:
        return ParseStatus.INVALID_CONTRACT, None
    try:
        label = ApplicabilityLabel(value["label"])
        jurisdiction = Jurisdiction(value["jurisdiction"])
        framework = value["legal_framework"]
        explanation = value["explanation"]
        references = value["statutory_references"]
        missing = value["missing_facts"]
        uncertainty = value["uncertainty"]
        if not isinstance(framework, str) or not framework.strip():
            raise ValueError
        if not isinstance(explanation, str) or not explanation.strip():
            raise ValueError
        if not isinstance(uncertainty, str):
            raise ValueError
        if not isinstance(references, list) or not all(isinstance(item, str) for item in references):
            raise ValueError
        if not isinstance(missing, list) or not all(isinstance(item, str) for item in missing):
            raise ValueError
    except (KeyError, TypeError, ValueError):
        return ParseStatus.INVALID_CONTRACT, None
    return ParseStatus.VALID, {
        "predicted_label": label,
        "jurisdiction": jurisdiction,
        "legal_framework": framework.strip(),
        "explanation": explanation.strip(),
        "statutory_references": tuple(references),
        "missing_facts": tuple(missing),
        "uncertainty": uncertainty.strip(),
    }


def run_scenario(
    scenario: ScenarioRecord,
    generator: TextGenerator,
    *,
    experiment_id: str,
    run_id: str,
    dataset_revision: str,
    prompt_version: str,
    retrieval_revision: str | None = None,
    retrieved_passages: Sequence[Mapping[str, str]] = (),
) -> PredictionRecord:
    if experiment_id == "E1" and (retrieval_revision or retrieved_passages):
        raise ValueError("E1 cannot receive retrieval context")
    if experiment_id in {"E2", "E3"} and not retrieval_revision:
        raise ValueError(f"{experiment_id} requires a retrieval revision")
    started = time.perf_counter()
    raw, runtime = generator.generate(build_messages(scenario, retrieved_passages))
    elapsed = time.perf_counter() - started
    status, parsed = parse_output(raw)
    return PredictionRecord(
        scenario_id=scenario.id,
        experiment_id=experiment_id,
        run_id=run_id,
        model_id=generator.model_id,
        model_revision=generator.model_revision,
        dataset_revision=dataset_revision,
        prompt_version=prompt_version,
        retrieval_revision=retrieval_revision,
        raw_output=raw,
        parse_status=status,
        retrieved_passage_ids=tuple(item["passage_id"] for item in retrieved_passages),
        runtime_metadata={**dict(runtime), "elapsed_seconds": elapsed},
        **(parsed or {}),
    )


@dataclass(slots=True)
class TinyAyaGenerator:
    """Lazy Transformers wrapper matching the official Tiny Aya model card."""

    model_id: str = MODEL_ID
    model_revision: str = MODEL_REVISION
    max_new_tokens: int = 384
    _tokenizer: Any = None
    _model: Any = None
    _torch: Any = None

    def load(self) -> None:
        if self._model is not None:
            return
        try:
            import torch
            from transformers import AutoModelForCausalLM, AutoTokenizer
        except ImportError as exc:
            raise RuntimeError("Install the verified model runtime before loading Tiny Aya") from exc
        self._tokenizer = AutoTokenizer.from_pretrained(
            self.model_id, revision=self.model_revision, trust_remote_code=False
        )
        self._model = AutoModelForCausalLM.from_pretrained(
            self.model_id,
            revision=self.model_revision,
            torch_dtype="auto",
            device_map="auto",
            trust_remote_code=False,
        )
        self._model.eval()
        self._torch = torch

    def generate(self, messages: Sequence[Mapping[str, str]]) -> tuple[str, Mapping[str, Any]]:
        self.load()
        inputs = self._tokenizer.apply_chat_template(
            list(messages),
            tokenize=True,
            add_generation_prompt=True,
            return_dict=True,
            return_tensors="pt",
        ).to(self._model.device)
        with self._torch.inference_mode():
            output = self._model.generate(
                **inputs,
                max_new_tokens=self.max_new_tokens,
                do_sample=False,
            )
        input_tokens = inputs["input_ids"].shape[-1]
        generated = output[0][input_tokens:]
        text = self._tokenizer.decode(generated, skip_special_tokens=True).strip()
        return text, {"input_tokens": input_tokens, "output_tokens": int(generated.shape[-1])}
