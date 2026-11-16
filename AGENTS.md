# Instructions for Coding Agents

## Required reading

Before planning or changing implementation, read all of these files in full:

1. `PROJECT.md`
2. `PRD.md`
3. `ARCHITECTURE.md`
4. `EVALUATION.md`
5. `TASKS.md`

These documents preserve prior design decisions. Do not redesign the project, broaden its legal scope, or weaken the output contract without explicit user approval. If documents conflict, stop and surface the conflict.

## Working method

- Implement the shortest unblocked item in `TASKS.md` in a small, testable loop.
- State assumptions, change only what the task requires, and add proportionate tests.
- Run lightweight validation after each loop and record actual evidence; do not claim tests or experiments ran when they did not.
- Update `TASKS.md` in the same change: mark verified completion, link or name evidence artifacts, and record blockers or newly discovered dependencies.
- Preserve reproducibility: versions, revisions, seeds, configurations, and commands belong in artifacts or documentation.

## External APIs and competition dependencies

- Verify official competition requirements from an authoritative competition source before implementation.
- Treat the official rules recorded in `PROJECT.md` as hard gates: genuinely chain at least two Track 1 repositories (three preferred), report multiple before/after metrics, and prepare all created models, adapters, logs, and datasets for public ungated Hugging Face hosting.
- Inspect the official model card and repository before selecting a Tiny Aya identifier. Record license, gating, revision, context, loading interface, and competition eligibility.
- Inspect the actual official CuratorKIT, AlignTune, and AuditKIT repositories/documentation before importing or calling them.
- Never invent a package name, module, class, function, CLI, configuration key, compatibility claim, or toolkit result.
- Prefer a thin adapter around verified external APIs so the canonical interfaces in `ARCHITECTURE.md` remain stable.
- If an API or requirement cannot be verified, mark the task blocked and implement no fictional substitute under that toolkit's name.

## Legal and research integrity

- Never fabricate statutes, provisions, quotations, URLs, evidence, effective dates, reviews, metrics, training outcomes, or benchmark improvements.
- Preserve provenance and content hashes. Do not silently alter source excerpts.
- Keep `SYNTHETIC_UNVERIFIED`, `HUMAN_REVIEWED`, and `LEGAL_REVIEWED` data visibly separated.
- Do not treat synthetic or model-generated material as legally reviewed.
- Keep training, validation, and held-out evaluation data isolated and run leakage checks before training.
- Grade closed labels deterministically. An LLM judge cannot be the sole legal-correctness arbiter.
- Do not expose confidential material, personal data, access tokens, gated weights, or restricted source text.
- Do not admit data to the submission pipeline unless its terms and privacy status permit the public, ungated artifact release required by the competition.
- Maintain the not-legal-advice limitation in user-facing artifacts.

## Experiment invariants

- Preserve E1, E2, and E3 exactly as specified in `PROJECT.md`.
- Use the same frozen held-out evaluation set for all arms.
- E2 and E3 must use identical retrieval corpus, index, query logic, filters, and parameters.
- Output must satisfy the structured contract; parse errors remain errors.
- Do not tune on held-out results or claim causal improvement without the registered paired comparison.

## Stop conditions

Stop and request direction if a requested change would expand legal scope, change the experiment arms, contaminate evaluation, violate a source/model license, fabricate an integration, or present unreviewed outputs as legal advice. Safety and research integrity take precedence over demo convenience.
