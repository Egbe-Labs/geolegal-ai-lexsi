# GeoLegal-AI

**Jurisdiction-aware privacy-law applicability classification with Tiny Aya Global.**

> Submission status: research prototype and baseline-only evidence. Fine-tuning has not run. The repository does not yet demonstrate the required two-kit Track 1 chain or before/after improvement. It is not legal advice.

## For judges: one minute

GeoLegal-AI tests whether a small open-weight language model can make structured, jurisdiction-aware decisions about whether privacy law applies to a factual scenario. It focuses on Nigeria, Kenya, and the European Union and requires one of three closed labels: `APPLIES`, `DOES_NOT_APPLY`, or `INSUFFICIENT_INFORMATION`.

The repository provides a legally reviewed, frozen 15-scenario evaluation set, deterministic scoring, a reproducible Google Colab baseline for `CohereLabs/tiny-aya-global`, protected-set leakage controls, and a review-gated synthetic training-candidate pipeline. It does **not** claim completed fine-tuning or improvement.

User-reported Colab baseline results are 46.67% accuracy, 24.56% macro F1, and 66.67% parse rate. The row-level prediction file and scored metrics export that produced those values are not present in this checkout, so these figures are provisional and not independently reproduced from repository artifacts.

## Track and problem statements

- Track 1: Fine-tuning and Data Curation
- Problem 1: domain assistants for regulated industries
- Problem 3: grounded answers and fewer hallucinations
- Problem 5: structured output and extraction
- Problem 8: data-scarce domains

The official hackathon requires Track 1 submissions to use at least two track repositories together, prefers three, requires more than one before/after metric, and requires created models, adapters, logs, and datasets to be hosted publicly on Hugging Face. See the [official rules](https://hackathon.lexsi.ai/).

## Problem

Territorial applicability is an early and error-prone step in privacy analysis. A system must identify the relevant jurisdiction, apply its territorial-scope conditions, abstain when decisive facts are absent, and ground its answer in the governing statute. Generic legal chat can hide uncertainty or produce unsupported provisions.

GeoLegal-AI is deliberately narrower: it is a controlled research experiment, not a general legal chatbot. Its hypothesis is that provenance-preserving, leakage-controlled fine-tuning can improve closed-label applicability decisions without weakening abstention or statutory grounding.

## Solution

The planned comparison keeps the frozen held-out evaluation set constant:

- **E1:** approved Tiny Aya baseline, no retrieval.
- **E2:** the same baseline with authoritative legal retrieval.
- **E3:** fine-tuned Tiny Aya with retrieval identical to E2.

Current executable work covers the E1 runner, structured parser, deterministic evaluator, frozen evaluation set, and training-data preparation gates. E2 and E3 have not been executed.

Every evaluated response must contain:

1. one closed label;
2. jurisdiction and legal framework;
3. a short explanation;
4. supported statutory references;
5. missing facts and uncertainty where relevant.

## Model

- Model: [`CohereLabs/tiny-aya-global`](https://huggingface.co/CohereLabs/tiny-aya-global)
- Pinned revision: `af89d219b53ed9b13b8a4645f9c8028973510324`
- Model-card description: Tiny Aya Global instruction-tuned model, approximately 3.35B parameters
- License recorded by the project: CC-BY-NC-4.0 plus Cohere Labs acceptable-use terms
- Access: gated terms acceptance and Hugging Face authentication are required

Base weights are not redistributed by this repository.

## Jurisdictions and authoritative scope rules

| Jurisdiction | Framework | Core scope provision | Authoritative source |
|---|---|---|---|
| Nigeria | Nigeria Data Protection Act 2023 | Section 2 | [Nigeria Data Protection Commission PDF](https://ndpc.gov.ng/wp-content/uploads/2024/03/Nigeria_Data_Protection_Act_2023.pdf) |
| Kenya | Data Protection Act 2019 | Section 4 | [Kenya Law](https://new.kenyalaw.org/akn/ke/act/2019/24/eng%402022-12-31/source) |
| European Union | GDPR | Article 3 | [EUR-Lex](https://eur-lex.europa.eu/eli/reg/2016/679/oj) |

## Data

### Frozen evaluation set

- File: `data/eval/held_out_approved_v1.jsonl`
- Records: 15, five per jurisdiction
- Status: `LEGAL_REVIEWED`, based on project-owner-reported human legal approval
- SHA-256: `cb93baa88e390b1b264fb36e423e910bb4edb309c134f3fc9af3757a62feffad`
- Manifest: `data/eval/held_out_approved_v1.manifest.json`

The original and proposed revisions are protected alongside the frozen revision in `data/eval/protected_held_out_registry_v1.json`.

### Training candidates

- Candidate records: 90 total
- Candidate training split: 72
- Candidate validation split: 18
- Distribution: 30 per jurisdiction and 30 per label
- Status: all `PENDING_REVIEW` and `SYNTHETIC_UNVERIFIED`
- Prompt/completion export: blocked until legal review and leakage clearance pass

The legal-review draft flags repetitive templates, conceptual held-out overlap, territorial omissions, and data-quality issues. These candidates have not been approved for training.

## Leakage controls

`src/geolegal/training_data.py` and `scripts/prepare_training_data.py` protect all three evaluation revisions using:

- ID and scenario-family checks;
- normalized exact matching;
- token-trigram Jaccard similarity;
- character five-gram Jaccard similarity;
- family-disjoint train/validation splits;
- mandatory manual resolution of flagged near-matches;
- a hard approval gate before prompt/completion export.

The current automated report has no threshold-level collision. That does not clear conceptual similarity; the human review draft identifies 55 records needing specific attention.

## Evaluation method

Closed labels are extracted and scored deterministically. Invalid or unparseable outputs count as incorrect rather than being silently coerced. Metrics are:

- classification accuracy;
- macro F1 across all three labels;
- parse rate or parse-failure rate;
- per-jurisdiction accuracy;
- confusion matrix;
- citation support, unsupported claims, and abstention quality after human review.

An LLM judge is not the sole arbiter of legal correctness. E1, E2, and E3 must use the byte-identical frozen evaluation revision, and E2/E3 must share the same retrieval revision.

## Baseline results

| Experiment | Accuracy | Macro F1 | Parse rate | Evidence status |
|---|---:|---:|---:|---|
| E1 Tiny Aya, no retrieval | 46.67% | 24.56% | 66.67% | User-reported Colab result; row-level predictions and scored metrics artifact are not present in this repository checkout |
| E2 Tiny Aya + retrieval | Not run | Not run | Not run | Planned |
| E3 Fine-tuned Tiny Aya + identical retrieval | Not run | Not run | Not run | Planned |

The preserved `results/geolegal_baseline_test.json` is a separate one-example exploratory smoke test and is excluded from scored metrics. The existing `results/baseline_metrics.json` is an earlier zero-scored placeholder created while answer keys were pending review; it is not the source of the table above.

Because no post-training run exists, there is no before/after improvement claim.

## Reproduce locally

Local checks require Python 3.11 or 3.12. The project target remains Python 3.11; current AlignTune metadata requires an isolated Python 3.12 training runtime.

```bash
git clone https://github.com/Egbe-Labs/geolegal-ai-lexsi.git
cd geolegal-ai-lexsi
python -m venv .venv
```

Activate the environment, then:

```bash
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
python -m unittest discover -s tests -v
python scripts/prepare_training_data.py
```

The preparation command regenerates candidate manifests and leakage reports. It does not train a model and does not export prompt/completion data while review is pending.

## Reproduce the Tiny Aya baseline in Google Colab

1. Open `notebooks/01_baseline.ipynb` in a GPU Colab runtime.
2. Clone this repository to `/content/geolegal-ai-lexsi`.
3. Accept the Tiny Aya model terms on Hugging Face.
4. Add `HF_TOKEN` through Colab Secrets; never paste it into the notebook.
5. Keep `DATASET_REVISION = 'held_out_approved_v1'`.
6. Confirm the versioned output paths printed by the notebook.
7. Change `RUN_INFERENCE = True` only when intentionally starting a fresh run.
8. Run the model-loading, inference, and scoring cells once.
9. Download or commit the new versioned prediction and metrics files without replacing older results.

The notebook loads model weights once and opens the prediction output in exclusive-create mode to prevent silent overwrite.

## Repository layout

```text
configs/                 Reproducible model, dataset, and experiment settings
data/eval/               Frozen evaluation revisions and protected registry
data/train/              Review-gated candidate data, manifest, leakage report
docs/                    Dependency and license decisions
notebooks/01_baseline.ipynb
results/                 Exploratory and evaluation artifacts
scripts/                 Data preparation and legal-review rendering
src/geolegal/            Schemas, baseline runner, evaluator, retrieval, fine-tune adapter
tests/                    Lightweight deterministic tests
```

## Hackathon toolkit status

| Toolkit | Repository support | Actually executed in an end-to-end submission chain? |
|---|---|---|
| CuratorKIT | API and intended no-key deduplication path documented | No |
| AlignTune | Tested thin adapter around documented SFT factory | No training run |
| AuditKIT | API and intended evaluation role documented | No |

The official minimum two-repository Track 1 chain is therefore **not yet satisfied**. Native curation and deterministic evaluation code must not be represented as executed CuratorKIT or AuditKIT.

## Known limitations and submission blockers

- No completed fine-tuning, adapter, E2 run, or E3 run.
- No executed two-kit Track 1 chain.
- No before/after result table.
- User-reported E1 row-level predictions and scored metrics artifact are missing from the repository.
- No public Hugging Face model collection or dataset collection is recorded.
- Candidate training data still requires legal review and contains documented issues.
- Citation support, unsupported claims, and abstention-quality review are incomplete.
- Team registration/finalist status is not recorded. The initial deadline was November 15, 2026; only shortlisted teams have the November 22 final stage.
- This prototype is not suitable for professional legal advice or consequential decisions.

## Responsible use

GeoLegal-AI is a research classifier. It does not replace qualified counsel, does not provide comprehensive privacy-law analysis, and must not be used as the sole basis for legal or compliance decisions. Statutes, guidance, and interpretations can change; outputs require jurisdiction-specific human review.

## Documentation

- `PROJECT.md` — hypothesis and scope
- `PRD.md` — product requirements and acceptance criteria
- `ARCHITECTURE.md` — components and experiment flow
- `EVALUATION.md` — metrics and leakage controls
- `SUBMISSION_AUDIT.md` — requirement-by-requirement readiness audit
- `SUBMISSION.md` — copy-ready provisional submission text and missing links
- `TRAINING_DATA_LEGAL_REVIEW.md` — candidate-by-candidate legal-review draft

## Work and AI-use declarations

The project owner must provide the final declaration of work performed outside the hackathon, author contributions, and LLM/AI-assistance statement before submission. This repository does not invent those declarations.
