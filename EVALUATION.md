# Evaluation Specification

## Unit of evaluation

One record describes a legally reviewable factual scenario and one scoped applicability question. Records should isolate the facts needed to evaluate territorial applicability or cross-border governance under the named framework.

## Canonical dataset schema

Required fields:

| Field | Type | Meaning |
|---|---|---|
| `id` | string | Stable unique record identifier |
| `scenario` | string | Factual scenario without hidden answer cues |
| `jurisdiction` | enum | `NIGERIA`, `KENYA`, or `EU` |
| `question` | string | Applicability question |
| `expected_label` | enum | `APPLIES`, `DOES_NOT_APPLY`, or `INSUFFICIENT_INFORMATION` |
| `legal_framework` | string | NDPA 2023, Kenya DPA 2019, or GDPR |
| `statutory_basis` | array | Provision-level authoritative source records |
| `evidence` | array | Supporting excerpts linked to source/provision IDs |
| `effective_date` | ISO date | Date at which the expected analysis is framed |
| `uncertainty` | object | Missing facts, ambiguity, and rationale for abstention |
| `provenance` | object | Author, origin, source links, timestamps, content hashes |
| `review_status` | enum | `SYNTHETIC_UNVERIFIED`, `HUMAN_REVIEWED`, or `LEGAL_REVIEWED` |
| `split` | enum | `TRAIN`, `VALIDATION`, `EVALUATION_SMOKE`, or `EVALUATION_HELD_OUT` |

Each `statutory_basis` item should contain `source_id`, `provision`, `title`, `publisher`, `url`, `version_or_date`, `accessed_at`, and `content_hash`. Recommended fields include `language`, `scenario_family_id`, `difficulty`, `expected_missing_facts`, reviewer identifiers, review notes, and license/reuse metadata.

The answer key is not embedded in model-visible retrieval metadata. Synthetic origin and review status must never be inferred from file location alone.

## Prediction schema

Each experiment produces a record containing `scenario_id`, `experiment_id`, `run_id`, `model_id`, `model_revision`, `dataset_revision`, `prompt_version`, `retrieval_revision` or null, raw output, parse status, predicted label, jurisdiction, legal framework, explanation, statutory references, missing facts, uncertainty, retrieved passage IDs, and runtime metadata.

## Experimental protocol

### Preparation

1. Verify competition rules, eligible Tiny Aya identifier/license, and toolkit versions from official sources.
2. Create and legally review a small smoke-test set covering all jurisdictions and all three labels where defensible.
3. Validate schema and provenance, group related variants by `scenario_family_id`, create splits, and freeze the held-out manifest.
4. Build the authoritative retrieval corpus and freeze its revision.
5. Register prompts, parser, decoding settings, seeds, and metric/rubric versions.

### Experiment arms

- E1: approved base model; no retrieval context.
- E2: same base model and model revision; authoritative retrieval enabled.
- E3: fine-tuned model; retrieval identical to E2.

Use the same held-out evaluation records for all arms. Keep decoding deterministic where supported. If nondeterministic sampling is required, pre-register seeds and repeated-run aggregation. The model must not see expected labels, answer-key evidence annotations, or review notes at inference.

Run the smoke test first. Run the full held-out evaluation only after pipeline and parser checks pass. Do not tune prompts, retrieval, labels, or hyperparameters against held-out outcomes.

## Metrics

### Deterministic primary metrics

- Classification accuracy over the three closed labels; invalid/unparseable labels count as incorrect.
- Macro F1 across the three labels, with the averaging and zero-division behavior recorded.
- Per-jurisdiction accuracy for Nigeria, Kenya, and EU.

Report confusion matrices, class counts, parse-failure rate, and confidence intervals where sample size permits. Never hide a missing class or collapse `INSUFFICIENT_INFORMATION` into another label.

### Grounding and safety metrics

- Citation support: proportion of required legal propositions whose cited provision and evidence support the proposition, assessed against the source registry and review rubric.
- Unsupported claims: count/rate of material legal claims lacking support or contradicted by cited authority.
- Abstention quality: precision and recall for `INSUFFICIENT_INFORMATION`, plus rubric assessment of whether missing facts were correctly identified.

Citation existence or URL validity alone does not establish support. These metrics require deterministic source matching where possible and blinded human legal review for substantive entailment. Any model-assisted review is advisory and cannot be the sole correctness judge.

### Comparison

Compare E1 vs E2 to estimate retrieval contribution and E2 vs E3 to estimate the incremental fine-tuning contribution under identical retrieval. Use paired, row-level comparisons and report sample sizes and uncertainty. Do not claim improvement from point estimates alone.

## Leakage controls

- Split by scenario family, not only record ID, before generating close paraphrases.
- Prohibit exact, normalized, and substantial semantic duplicates across training and held-out evaluation.
- Hash source passages and scenario text; save a leakage report with every dataset release.
- Do not expose expected labels, answer explanations, reviewer notes, or gold evidence IDs through prompts or retrieval.
- Ensure fine-tuning data excludes all held-out scenarios and derived paraphrases.
- Freeze the evaluation manifest before training and restrict access during iteration where practical.
- Tune retrieval and prompts using training/validation or a distinct development set only.
- Record any suspected contamination in pretrained model knowledge as a limitation; it cannot be fully ruled out.
- Version datasets and indexes so E2 and E3 demonstrably share identical retrieval.

## Review protocol

Legal reviewers should be blinded to experiment arm when assessing support, unsupported claims, and abstention explanations. Disagreements are adjudicated and retained in an audit trail. Headline legal-correctness reporting should use `LEGAL_REVIEWED` records; other records are reported separately as development diagnostics.

## Reporting rules

Publish the frozen schema, revision identifiers, class/jurisdiction distribution, metric definitions, exclusions, leakage report, row-level errors where licensing permits, and limitations. State clearly if a stage was not run. Never backfill missing artifacts with inferred or invented results.

The official submission requires more than one before/after metric. At minimum, report classification accuracy and macro F1 for the same model before and after fine-tuning, alongside the specified jurisdiction, citation, unsupported-claim, and abstention analyses. Publish CuratorKIT filtering counts and reasons if that kit is used. Record model configuration/license, sources and dataset licenses, split sizes, leak-check methods, training hyperparameters, each kit's defaults, compute, known weaknesses, reproducibility instructions, outside-hackathon work, and an LLM-usage statement. Public row-level publication is allowed only for records and source excerpts cleared for ungated release.
