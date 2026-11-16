# Architecture

## Design constraints

The architecture must preserve experimental comparability, statutory provenance, and a hard boundary between unreviewed generation and legally reviewed evidence. Components should be replaceable through explicit interfaces rather than hidden notebook state.

## Components

### Configuration and run registry

Stores immutable run identifiers and the exact model revision, dataset revision, split manifest, prompt version, retrieval settings, decoding settings, random seed, dependency versions, hardware, and toolkit versions. E1–E3 must be reconstructible from these records.

### Source registry

Stores authoritative source metadata and immutable evidence passages. Each passage has a stable identifier, jurisdiction, framework, provision, source URL, publisher, effective date, access date, content hash, and license/reuse note. Retrieved text is evidence input, not automatically verified truth.

### Dataset curation and validation

Transforms reviewed scenarios into the canonical schema in `EVALUATION.md`. It validates controlled values, provenance, dates, duplicate IDs, review status, and split membership. Synthetic drafts remain in a separate partition until legal review changes their status.

Target integration: CuratorKIT, only after its actual official API and competition role are verified. A thin adapter should isolate toolkit-specific calls from the canonical dataset.

### Split and leakage control

Creates versioned train, validation, and held-out evaluation manifests. It detects exact and normalized duplicates, shared scenario families, substantial text overlap, evidence-answer leakage, and accidental reuse of evaluation IDs. The evaluation manifest is frozen before training.

### Retrieval

Indexes only approved, versioned authoritative passages. Input is a question plus jurisdictional constraints; output is an ordered list of passage IDs, text, metadata, and scores. E2 and E3 must share the same corpus revision, index build, query, filters, top-k, and ordering.

### Model runner

Exposes one logical interface:

```text
generate(model_revision, prompt_version, scenario, retrieved_passages, decoding_config)
  -> raw_text, token/runtime metadata
```

E1 receives no retrieved passages. E2 receives retrieval with the approved base model. E3 receives identical retrieval with the trained adapter/model. The runner must use an officially approved Tiny Aya identifier and documented loading interface.

### Fine-tuning

Consumes only the versioned training split and produces a versioned adapter or model artifact plus training configuration and logs. Validation data may guide training; the held-out evaluation split must never do so.

Target integration: AlignTune, only after its official repository, supported model path, configuration schema, and save/load behavior are verified. No compatibility is assumed.

### Output parser

Converts raw generation into the required contract:

```text
label
jurisdiction
legal_framework
explanation
statutory_references[]
missing_facts[]
uncertainty
```

It records parse errors and invalid labels rather than guessing the intended class.

### Evaluation and audit

Joins predictions with the frozen answer key, computes deterministic label metrics, verifies cited passage/source identifiers, and prepares row-level material for human review of unsupported claims and abstention quality.

Target integration: AuditKIT, only after its official API, supported artifacts, and competition requirements are verified. Native deterministic metrics remain the source of truth for the closed label.

### Gradio demo

Calls the same model, retrieval, parsing, and provenance interfaces as the experiment. It shows the experiment condition, structured output, retrieved passages, limitations, and not-legal-advice warning. It must not mutate evaluation data or silently collect user scenarios for training.

## Data flow

```text
Authoritative sources -> source registry -> reviewed evidence passages -> retrieval index
Human/synthetic drafts -> review + schema validation -> split manifests
train manifest -> fine-tuning -> E3 artifact
frozen evaluation manifest -> E1 / E2 / E3 runners -> output parser
parsed outputs + answer key + provenance -> deterministic metrics + legal review -> report
```

## Canonical interfaces

- Source record: stable source and provision metadata plus evidence text and hash.
- Scenario record: canonical fields defined in `EVALUATION.md`.
- Retrieval result: passage ID, rank, score, text, source metadata, corpus revision.
- Prediction record: scenario ID, experiment ID, raw output, parsed contract, retrieved passage IDs, run ID, parse status.
- Metric artifact: dataset/run revisions, aggregate and per-slice metrics, row-level errors, rubric version.

## Runtime boundaries

- Local Python 3.11: schema validation, smoke tests, leakage checks, deterministic scoring, and demo development.
- Google Colab GPU: approved model loading, baseline generation at scale, fine-tuning, and post-training inference. The core notebook/runtime remains Python 3.11-compatible where possible; AlignTune fine-tuning is isolated in a Python 3.12 environment because its verified current package metadata requires Python 3.12. Artifacts cross the boundary only through versioned dataset/model identifiers, configurations, manifests, and checksums.
- Hugging Face: public, ungated collections for all created models, adapters, logs, and datasets after license, provenance, privacy, and hackathon checks. Material that cannot lawfully be made public must be excluded before it reaches the pipeline.
- GitHub: code, documentation, configurations, and non-sensitive metadata; never secrets or restricted texts.

## Failure behavior

Missing sources, invalid output, unavailable model access, license ambiguity, toolkit incompatibility, or leakage must stop the affected stage and create an explicit error artifact. The pipeline must not fabricate fallback evidence or mark a skipped stage successful.

## Hackathon compliance interface

The run registry must also record which Track 1 kits were executed, their versions and artifacts, how they connect, before/after metric tables, compute used, and work performed outside the hackathon. Submission packaging must assemble public Hugging Face model and dataset collections plus the reproducible GitHub repository. Packaging is blocked unless at least two verified Track 1 kits were genuinely used together.
