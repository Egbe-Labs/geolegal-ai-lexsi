# Implementation Path

This is the shortest dependency-ordered path from environment verification to public submission. A task is complete only with recorded evidence. No experiment is currently marked complete.

## Status legend

- `[ ]` not started
- `[~]` in progress
- `[x]` completed and verified
- `[!]` blocked; describe the blocker beneath the task

## 0. Governance baseline

- [x] Record the fixed project hypothesis, scope, experiment arms, output contract, evaluation protocol, architecture, agent rules, and implementation path.
  - Evidence: `PROJECT.md`, `PRD.md`, `ARCHITECTURE.md`, `EVALUATION.md`, `AGENTS.md`, and this file.
- [x] Obtain explicit approval to begin implementation.
  - Evidence: project owner instruction in this task on 2026-11-16 to begin at the first incomplete task.

## 1. Verify environment and official dependencies

- [x] Verify Python 3.11, Git, Colab GPU assumptions, GitHub/Hugging Face publication targets, and secret-handling approach.
  - Evidence: `docs/DEPENDENCY_DECISIONS.md`. Git 2.56.0 is available, but the local machine lacks Python 3.11 (default is 3.12.10); Colab GPU execution and HF authentication remain runtime preflights, not assumed successes.
- [x] Capture the official Lexsi Track 1 rules, allowed-model list, artifact requirements, submission structure, and deadlines.
  - Evidence: [official hackathon page](https://hackathon.lexsi.ai/), checked 2026-11-16; requirements summarized in `PROJECT.md` and `PRD.md`.
- [ ] Confirm that the project owner registered by the deadline and, because the initial deadline has passed, whether the team was shortlisted for the final stage ending 2026-11-22 at 11:59 PM AoE.
- [x] Record the exact Tiny Aya Global repository revision, license/AUP, gating, loading example, fine-tuning permission, and downstream public-artifact obligations from official sources.
  - Evidence: `docs/DEPENDENCY_DECISIONS.md`; pinned HF revision `af89d219b53ed9b13b8a4645f9c8028973510324`.
- [~] Locate the official CuratorKIT, AlignTune, and AuditKIT repositories/docs; record install instructions, versions/commits, Python support, APIs, licenses, and expected artifacts.
  - Evidence: `docs/DEPENDENCY_DECISIONS.md`. Official APIs and current package metadata are recorded. Exact toolkit commit pins remain to be selected; the project owner approved an isolated Python 3.12 Colab runtime for current AlignTune while retaining Python 3.11 core compatibility.
- [x] Produce a dependency decision record. Mark unverifiable or incompatible integrations blocked rather than approximating their APIs.
  - Evidence: `docs/DEPENDENCY_DECISIONS.md`.
- [x] Define a publication allowlist so every created model, adapter, log, and dataset can be released publicly and ungated as required.
  - Evidence: publication allowlist in `docs/DEPENDENCY_DECISIONS.md`.

## 2. Create the minimal tested repository skeleton

- [x] Add Python 3.11 project metadata, dependency strategy, configuration layout, source package, tests, data/artifact directories, and safe `.gitignore` rules.
  - Evidence: `pyproject.toml`, `.gitignore`, `.env.example`, `configs/base.toml`, `src/geolegal/`, `tests/`, `data/`, `artifacts/`, and `notebooks/`.
- [~] Add automated formatting/linting, compilation/import checks, and lightweight unit test commands.
  - Evidence: Ruff/pytest configuration is in `pyproject.toml`; stdlib compilation and 2 smoke tests passed on Python 3.12.10 on 2026-11-16. Ruff/pytest installation and Python 3.11 execution remain outstanding.
- [x] Define immutable run/config metadata and canonical interfaces from `ARCHITECTURE.md`.
  - Evidence: `src/geolegal/run_registry.py`, `configs/base.toml`, and `tests/test_run_registry.py`; 6 tests and compilation passed on Python 3.12.10 after correcting the test temp path for the Windows sandbox.
- [ ] Verify a clean environment can install and run local checks without downloading model weights.

## 3. Implement schema, provenance, and smoke-test curation

- [x] Implement canonical source, scenario, prediction, and run schemas from `EVALUATION.md` with validation tests.
  - Evidence: `src/geolegal/schema.py`, `src/geolegal/run_registry.py`, `tests/test_schema.py`, and `tests/test_run_registry.py`; 11 tests and compilation passed on Python 3.12.10.
- [~] Implement source hashing, review-state separation, date/license metadata checks, and an append-only provenance trail.
  - Evidence: source hash, date, non-empty license, framework/jurisdiction, and review-state invariants are enforced in `src/geolegal/schema.py`. Append-only provenance storage and publication-license policy checks remain.
- [ ] Integrate CuratorKIT only through its verified API; otherwise record the blocker and retain toolkit-neutral canonical data.
- [x] Draft the initial held-out candidate set with five scenarios per jurisdiction and only the three closed labels; keep all proposed keys excluded pending legal review.
  - Evidence: `data/eval/held_out_initial.jsonl` contains 15 source-linked `PENDING_REVIEW` scenarios grounded in NDPA 2023 section 2, Kenya DPA 2019 section 4, and GDPR Article 3. These are candidate answer keys, not validated legal conclusions.
- [ ] Obtain human/legal review and change status only with reviewer evidence.

## 4. Freeze splits and leakage controls

- [ ] Implement family-aware deterministic train/validation/evaluation manifests.
- [ ] Implement exact, normalized, overlap, and derived-scenario leakage checks with tests.
- [ ] Freeze and hash the held-out smoke evaluation manifest before training.
- [ ] Save a machine-readable leakage report and confirm zero unresolved leakage.

## 5. Build authoritative retrieval

- [ ] Acquire only authoritative, reusable, versioned source text for NDPA 2023, Kenya DPA 2019, and GDPR.
- [x] Create the provision-level passage interface with source metadata, dates, hashes, and license notes.
  - Evidence: `SourceRecord` in `src/geolegal/schema.py`. No real statutory passage is claimed or bundled yet.
- [x] Implement deterministic jurisdiction-filtered retrieval and provenance-rich results.
  - Evidence: `src/geolegal/retrieval.py` implements stable lexical ranking, jurisdiction filtering, source hashes, and provenance-bearing results.
- [~] Freeze the retrieval corpus/index/settings revision for both E2 and E3.
  - Evidence: `LexicalRetriever.revision` fingerprints algorithm, top-k, sorted source IDs, and source hashes. A real approved corpus has not been acquired or frozen.
- [x] Test missing evidence, wrong-jurisdiction exclusion, stable ordering, and prompt-injection handling.
  - Evidence: `tests/test_retrieval.py`; source delimiter escaping and all named cases pass.

## 6. Implement model runner and E1/E2 smoke runs

- [x] Implement the verified Tiny Aya load/generation path and structured prompt/output parser.
  - Evidence: `src/geolegal/baseline.py` uses the pinned official Transformers loading/chat-template/generation interface; it is lazy and no weights were downloaded. Fake-generator tests cover the runnable local path.
- [x] Fail explicitly on invalid labels or incomplete contracts.
  - Evidence: strict JSON parsing and contract validation in `src/geolegal/baseline.py` and `src/geolegal/schema.py`; invalid prose, extra fields, and incomplete valid predictions are tested.
- [~] Build E1 without retrieval and E2 with frozen retrieval using shared settings.
  - Evidence: E1 and E2 prompting/generation orchestration, retrieval fingerprinting, and arm invariants are implemented and tested with a fake generator. Batch CLI, real approved corpus, and gated-model execution remain.
- [x] Create a Colab notebook that installs verified versions, authenticates safely, runs opt-in smoke inference, saves outputs/configuration, and makes no result claims automatically.
  - Evidence: `notebooks/01_baseline.ipynb` loads the pinned Tiny Aya model once, reuses it across all scenarios, writes predictions, and asserts that pending keys produce zero scored records.
- [~] Run E1/E2 smoke tests on GPU and archive actual row-level outputs and runtime metadata.
  - Evidence: `results/geolegal_baseline_test.json` is one actual E1 exploratory Colab inference; `results/exploratory_manifest.json` records its SHA-256 and permanent metric exclusion. It predates the strict contract and held-out dataset. Full E1 and E2 held-out runs remain.

## 7. Fine-tune and run E3

- [x] Integrate AlignTune only through its verified API and supported approved-model path.
  - Evidence: `src/geolegal/finetune.py` wraps the documented `create_sft_trainer` interface, enforces Tiny Aya Global and the pinned expected revision, enables documented LoRA parameters, and calls documented `train()`/`save_model()` methods. No training was run.
- [~] Preflight the training split, license constraints, leakage report, GPU memory, and save/load behavior.
  - Evidence: Python 3.12 isolation, model/revision, public HF dataset identifier, parameter validation, and secret-free manifest tests are implemented. Real dataset/license/leakage/GPU/memory/save-load preflights await cloud artifacts.
- [ ] Run the smallest fine-tuning smoke job; archive logs, configuration, versions, and adapter/model artifact.
- [ ] Run E3 against the same frozen evaluation set and byte-identical E2 retrieval revision.
- [ ] Record failures and resource use; do not infer success from artifact existence alone.

## 8. Evaluate and audit

- [x] Implement deterministic accuracy, macro F1, per-jurisdiction accuracy, confusion matrices, parse failures, and paired comparisons.
  - Evidence: `src/geolegal/evaluation.py`, `src/evaluate.py`, and their tests; invalid/missing outputs count as incorrect, duplicates are rejected, paired deltas are tested, and pending-review keys are excluded from scoring.
- [ ] Implement citation/source matching and the human review workflow for citation support, unsupported claims, and abstention quality.
- [ ] Integrate AuditKIT only through its verified API without replacing deterministic scoring.
- [ ] Blind legal reviewers to experiment arm, adjudicate disagreements, and retain the audit trail.
- [ ] Produce smoke-test results with uncertainty and limitations; expand the dataset only after the pipeline passes.

## 9. Demo and reproducibility

- [ ] Build a Gradio research demo on the same interfaces, with condition visibility, provenance, structured output, uncertainty, and a not-legal-advice warning.
- [ ] Prevent evaluation mutation, secret leakage, silent user-data collection, and unsupported-source presentation.
- [ ] Add end-to-end smoke tests and a clean Colab reproduction run.

## 10. Public submission

- [ ] Review every source/model/toolkit license and remove material that cannot be published.
- [ ] Publish only reviewed dataset partitions and clearly label synthetic/unreviewed material.
- [ ] Publish all created submission models, adapters, logs, and datasets in public, ungated Hugging Face repositories and organize them into the required public model and dataset collections; exclude anything that cannot legally be published.
- [ ] Finalize README, model card, dataset card, experiment report, safety/limitations, reproducibility commands, and actual artifact links.
- [ ] Verify the public GitHub repository and Colab from a clean account/environment.
- [ ] Submit Track 1 artifacts and record the exact public revisions; never replace missing results with claims.

## Known unresolved dependencies

- Team registration and finalist status are unknown. The initial submission deadline passed on 2026-11-15; only shortlisted teams have the final stage through 2026-11-22.
- Tiny Aya Global is officially allowed, but the exact pinned revision and full license/publication implications are not yet recorded.
- CuratorKIT, AlignTune, and AuditKIT repository locations, APIs, versions, licenses, and Tiny Aya compatibility are unverified.
- Authoritative-text reuse terms and legal reviewer availability are unresolved.
- Hugging Face gating/publication permissions and Colab GPU capacity are unresolved.
- The local machine has Python 3.12.10 but no Python 3.11 installation.
- AlignTune current package metadata requires Python 3.12; an isolated Python 3.12 Colab training runtime was approved on 2026-11-16, while the core remains Python 3.11-compatible.
- AuditKIT LSAL-1.2 may require organizational acknowledgement or permission before use.
