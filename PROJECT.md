# GeoLegal-AI Project Charter

## Purpose

GeoLegal-AI is a jurisdiction-aware legal AI research experiment for the Lexsi AI Safety & Alignment Hackathon, Track 1: Fine-tuning and Data Curation. It is not a general-purpose legal chatbot and must not be presented as professional legal advice.

The project aligns most directly with Track 1 problem statements 1 (regulated-industry domain assistants), 3 (grounded answers and fewer hallucinations), and 5 (structured output and extraction). The submission pipeline is intended to chain CuratorKIT, AlignTune, and AuditKIT, satisfying the official minimum of two Track 1 repositories and the preference for three or more, subject to verification of their actual APIs.

## Scientific hypothesis

Targeted, provenance-preserving fine-tuning will improve a small approved open-weight model's accuracy in identifying whether a privacy or personal data protection framework applies to a factual scenario, compared with the same approved model used without fine-tuning.

The experiment must distinguish the effect of fine-tuning from the effect of retrieval. It therefore compares:

- E1: approved baseline Cohere model without retrieval;
- E2: the same baseline model with authoritative legal retrieval;
- E3: the fine-tuned model with the identical retrieval system used in E2.

All three conditions use the same frozen, held-out evaluation set. No outcome or improvement is assumed before execution.

## Legal scope

The experiment is limited to:

- Nigeria — Nigeria Data Protection Act 2023;
- Kenya — Data Protection Act 2019;
- European Union — General Data Protection Regulation (GDPR).

Questions focus on territorial applicability, cross-border data governance, legal uncertainty, and statutory grounding. Adjacent laws, regulator guidance, case law, or amendments may be used only when their authority, version, date, and relevance are recorded. They do not silently expand the core scope.

## Required response contract

Every evaluated response must contain:

1. exactly one closed label: `APPLIES`, `DOES_NOT_APPLY`, or `INSUFFICIENT_INFORMATION`;
2. the identified jurisdiction and applicable legal framework;
3. a short explanation;
4. statutory source references where the evidence supports them;
5. missing facts or uncertainty where relevant.

## Research principles

- Preserve a verifiable chain from each legal proposition to authoritative source text.
- Prefer a small, reviewed dataset over a large weakly sourced dataset.
- Begin with a smoke-test dataset before scaling.
- Keep unverified synthetic examples visibly separate from legally reviewed examples.
- Grade closed labels deterministically; an LLM judge must never be the sole arbiter of legal correctness.
- Report negative and inconclusive results.
- Never invent authorities, toolkit integrations, benchmark results, or training outcomes.

## Intended deliverables

A reproducible Python 3.11 repository, Colab GPU workflow, source-verifiable dataset, fine-tuned approved Tiny Aya variant, deterministic evaluation artifacts, Gradio research demo, and Hugging Face/GitHub publication materials. The official rules require created models, adapters, logs, and datasets to be hosted publicly and ungated on Hugging Face; therefore no non-publishable input or artifact may enter the submission pipeline.

## Non-goals

- legal advice or automated legal decision-making;
- comprehensive coverage of privacy law;
- replacing qualified jurisdiction-specific review;
- generating uncited legal authorities;
- claiming production readiness, safety, or general legal competence.

## Current status

Implementation is in progress. Tiny Aya Global has loaded successfully in Google Colab and one preserved inference artifact exists as an exploratory smoke test. It is not a validated benchmark result and is excluded from scored metrics. Fifteen initial evaluation scenarios are drafted as `PENDING_REVIEW`; no answer key is legally reviewed, no held-out score is reported, and no model has been fine-tuned.

## Official hackathon constraints verified on 2026-11-16

The [official Lexsi hackathon page](https://hackathon.lexsi.ai/) confirms that Tiny Aya Global is an allowed dense Cohere Labs open-weights model; Track 1 uses CuratorKIT, AlignTune, and AuditKIT; at least two track repositories must be chained and three or more are preferred; submissions must show more than one before/after metric; and created artifacts must be public and ungated on Hugging Face. The original submission deadline was 2026-11-15 at 11:59 PM AoE. Only shortlisted teams proceed to the final proof stage ending 2026-11-22 at 11:59 PM AoE. Team/finalist eligibility remains a project-owner dependency.
