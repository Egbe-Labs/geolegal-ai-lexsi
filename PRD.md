# Product Requirements Document

## Product definition

GeoLegal-AI is a research interface and reproducible experimental pipeline that tests whether targeted fine-tuning improves closed-label legal applicability decisions within the fixed scope defined in `PROJECT.md`.

## Users

- hackathon reviewers examining scientific rigor and safety;
- researchers curating and auditing the dataset;
- legal reviewers validating statutory grounding;
- developers reproducing E1, E2, and E3.

It is not intended for people seeking legal advice.

## MVP features

### 1. Provenance-preserving data curation

- Store each scenario and expected answer using the schema in `EVALUATION.md`.
- Link every statutory basis and evidence excerpt to an authoritative source, version, effective date, and access record.
- Mark review state and synthetic origin explicitly.
- Validate required fields, controlled labels, dates, and unique identifiers.
- Produce a small smoke-test dataset before any larger dataset.

### 2. Three comparable experiment arms

- E1 runs the approved base model without retrieval.
- E2 runs the identical base model with authoritative retrieval.
- E3 runs the fine-tuned model with the exact E2 retrieval corpus, index, query method, and parameters.
- All arms use the same prompts where the experimental condition permits, decoding settings, output parser, and frozen evaluation set.

### 3. Contract-constrained output

- Produce one valid closed label.
- State jurisdiction and framework.
- Provide a concise explanation.
- Provide supported statutory references.
- State missing facts and uncertainty.
- Fail visibly when the response cannot be parsed; do not silently coerce ambiguous prose.

### 4. Deterministic and reviewable evaluation

- Compute classification accuracy, macro F1, and per-jurisdiction accuracy.
- Measure citation support, unsupported claims, and abstention quality using documented rubrics.
- Export row-level predictions, parse status, metrics, configuration, model revision, and dataset revision.
- Support human legal review without replacing deterministic label scoring.

### 5. Research demo

- Provide a Gradio interface clearly labeled as a research prototype, not legal advice.
- Show the selected experiment condition and retrieved sources where applicable.
- Display the structured response contract and provenance.
- Do not imply that demo outputs are validated merely because a citation is present.

### 6. Reproducibility and publication

- Run locally for validation and in Google Colab for GPU steps.
- Pin or record dependency, model, dataset, prompt, and configuration versions.
- Prepare GitHub and Hugging Face artifacts without publishing restricted source text or unreviewed claims.
- Publish all created submission models, adapters, logs, and datasets through public, ungated Hugging Face repositories and collections; exclude inputs whose terms or privacy constraints prevent that publication.

## Acceptance criteria

The MVP is acceptable only when:

- the approved Tiny Aya identifier, license, access conditions, and competition eligibility are recorded from official sources;
- CuratorKIT, AlignTune, and AuditKIT interfaces are verified against official repositories or documentation before use;
- at least two Track 1 repositories are genuinely chained in the executed pipeline, with all three target kits preferred and each use documented;
- the smoke-test dataset passes schema and provenance validation;
- training and evaluation records are disjoint, with an automated leakage report;
- every evaluation item has a reviewed expected label and statutory basis, or is explicitly excluded from headline legal-correctness metrics;
- E1, E2, and E3 run from saved configurations against the same frozen evaluation revision;
- every parsed prediction contains all required output fields;
- deterministic metrics and row-level results can be reproduced from saved artifacts;
- unsupported-claim and abstention assessments follow the rubric in `EVALUATION.md`;
- the demo displays safety limitations and authoritative sources;
- documentation distinguishes completed work from planned or unverified work.
- the results include more than one before/after metric and the write-up explains metric, dataset, task, model, and method choices;
- public, ungated Hugging Face model and dataset collections contain the created artifacts required by the official submission form;
- the public GitHub repository or notebooks include reproducibility notes and declare work done outside the hackathon.

## Out of scope for MVP

- additional jurisdictions or legal domains;
- open-ended legal chat;
- autonomous source collection without review;
- legal correctness determined solely by model-based grading;
- production hosting or use in consequential decisions.

## Dependencies and gates

Implementation is gated on team registration/finalist status, model-license compatibility, authoritative legal text whose terms permit public ungated artifact publication, verified toolkit APIs, legal review capacity, Hugging Face access, and a Colab GPU budget. Tiny Aya Global is on the official allowed-model list, but the precise revision and its downstream publication obligations still require recording.
