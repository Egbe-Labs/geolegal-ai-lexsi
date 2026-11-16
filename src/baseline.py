"""Batch Tiny Aya baseline inference for Colab; imports model weights only once."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterable

from src.dataset import LegalScenario

MODEL_ID = "CohereLabs/tiny-aya-global"
MODEL_REVISION = "af89d219b53ed9b13b8a4645f9c8028973510324"

SYSTEM_PROMPT = """Return exactly one JSON object with keys label, jurisdiction, legal_framework, explanation, statutory_references, missing_facts, uncertainty. label must be APPLIES, DOES_NOT_APPLY, or INSUFFICIENT_INFORMATION. Do not invent legal provisions. This is research classification, not legal advice."""


def scenario_messages(record: LegalScenario) -> list[dict[str, str]]:
    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {
            "role": "user",
            "content": (
                f"Jurisdiction: {record.jurisdiction}\n"
                f"Scenario: {record.scenario}\n"
                f"Question: {record.question}"
            ),
        },
    ]


def load_model_once(model_id: str = MODEL_ID, revision: str = MODEL_REVISION):
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer

    tokenizer = AutoTokenizer.from_pretrained(model_id, revision=revision, trust_remote_code=False)
    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        revision=revision,
        torch_dtype="auto",
        device_map="auto",
        trust_remote_code=False,
    )
    model.eval()
    return tokenizer, model, torch


def generate_one(tokenizer, model, torch, record: LegalScenario, max_new_tokens: int = 384) -> dict[str, Any]:
    inputs = tokenizer.apply_chat_template(
        scenario_messages(record),
        tokenize=True,
        add_generation_prompt=True,
        return_dict=True,
        return_tensors="pt",
    ).to(model.device)
    with torch.inference_mode():
        output = model.generate(**inputs, max_new_tokens=max_new_tokens, do_sample=False)
    input_length = inputs["input_ids"].shape[-1]
    generated = output[0][input_length:]
    return {
        "scenario_id": record.scenario_id,
        "model": MODEL_ID,
        "model_revision": MODEL_REVISION,
        "response": tokenizer.decode(generated, skip_special_tokens=True).strip(),
        "input_tokens": int(input_length),
        "output_tokens": int(generated.shape[-1]),
    }


def run_baseline(records: Iterable[LegalScenario], output_path: str | Path) -> None:
    tokenizer, model, torch = load_model_once()
    destination = Path(output_path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("w", encoding="utf-8", newline="\n") as handle:
        for record in records:
            handle.write(json.dumps(generate_one(tokenizer, model, torch, record), ensure_ascii=False) + "\n")
