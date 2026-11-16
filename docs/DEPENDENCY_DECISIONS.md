# Dependency Verification and Decisions

Checked against official sources on 2026-11-16. This record reports interfaces and constraints only; it does not claim any package, model, or experiment was run.

## Local environment

| Dependency | Observed state | Decision |
|---|---|---|
| Python | Default `python` is 3.12.10; `py -3.11` reports no installed Python 3.11 | Core remains specified for Python 3.11. Local clean-install verification is blocked until 3.11 is installed. Syntax/tests may also be exercised on 3.12 but cannot substitute for the required 3.11 check. |
| Git | 2.56.0.windows.4 | Suitable. Origin is `https://github.com/Egbe-Labs/geolegal-ai-lexsi.git`. |
| GitHub CLI | Not found in the checked command inventory | Publication can use Git or the web UI; authentication must remain outside repository files. |
| Hugging Face CLI | Not found in the checked command inventory | Install in the isolated project/Colab environment. Use `HF_TOKEN` or Colab secrets; never commit tokens. |
| GPU | Not checked locally and not assumed | Official hackathon guidance identifies Colab/Kaggle as possible Tiny Aya GPU environments. GPU work remains cloud-only until an actual runtime preflight succeeds. |

Secret handling: local secrets must use environment variables or an ignored `.env`; Colab must use its secrets store. Logs/configurations must record only whether credentials were available, never their values.

## Approved model

- Repository: [`CohereLabs/tiny-aya-global`](https://huggingface.co/CohereLabs/tiny-aya-global).
- Pinned revision for reproducible experiments: `af89d219b53ed9b13b8a4645f9c8028973510324` (Hugging Face model API value observed 2026-11-16).
- Competition eligibility: explicitly listed by the official Lexsi rules as Tiny Aya Global.
- Access: public repository with automatic gating; users must accept the terms and authenticate to download files.
- License: CC-BY-NC-4.0 plus Cohere Labs acceptable-use terms; the gate requires agreement to non-commercial use only.
- Model card: instruction-tuned `tiny-aya-it-global`, 3.35B parameters, 8K input context.
- Verified loading interface: Transformers `AutoTokenizer.from_pretrained`, `AutoModelForCausalLM.from_pretrained`, tokenizer `apply_chat_template`, and model `generate`.
- Publication decision: publish only original project adapters and metadata permitted by the model terms; do not redistribute base weights. Include base-model attribution, pinned revision, license, and non-commercial restriction.

## CuratorKIT

- Official repository: [`Lexsi-Labs/CuratorKIT`](https://github.com/Lexsi-Labs/CuratorKIT); official docs: <https://curatorkit.lexsi.ai/latest/>.
- Package/install: `curatorkit`; `pip install "curatorkit[all]"` or core installation for local JSONL/CSV.
- Python: `>=3.11` in the current `pyproject.toml`.
- License: LSAL-1.1, non-commercial with responsible-use conditions.
- Verified Python API: `from curatorkit import Curator, CuratorConfig`; construct `Curator(CuratorConfig(...)).run()`.
- Verified no-LLM use: cleaning and MinHash deduplication with `dedup="minhash"`, `clean=True`, and trainer-ready exports.
- Expected artifacts: `manifest.json`, `rejected.jsonl`, `dataset_card.md`, `lexsi_provenance.json`, `checksums.txt`, and export files.
- Decision: use a thin adapter for no-key cleaning/deduplication first. Synthetic generation remains opt-in and cannot confer legal-review status.

## AlignTune

- Official repository: [`Lexsi-Labs/aligntune`](https://github.com/Lexsi-Labs/aligntune); docs: <https://aligntune.lexsi.ai/>.
- Package/install: `aligntune`; repository README documents `pip install aligntune`.
- License: MIT.
- Verified API: `from aligntune.core.backend_factory import create_sft_trainer`; `create_sft_trainer(...)`, then `trainer.train()` and optionally `trainer.evaluate()`.
- Current package metadata observed: version `0.1.17`, `requires-python = ">=3.12"`; this conflicts with the repository README statement of Python 3.11+ and with this project's Python 3.11 requirement.
- Decision: project owner approved an isolated Python 3.12 Colab environment for AlignTune on 2026-11-16. The core package remains Python 3.11-compatible. The boundary uses versioned Hugging Face dataset/model identifiers, configuration, manifests, and checksums; no Python objects or hidden notebook state cross it. No substitute may be presented as AlignTune.

## AuditKIT

- Official repository: [`Lexsi-Labs/AuditKIT`](https://github.com/Lexsi-Labs/AuditKIT); docs: <https://auditkit.lexsi.ai/>.
- Package/install: `auditkit`; core `pip install auditkit`, Transformers backend via `auditkit[transformers]`.
- Current package metadata observed: version `1.1.11`, Python `>=3.10`, no core third-party dependencies.
- License: LSAL-1.2, source-available/non-commercial. Organizational use may require prior written permission or written acknowledgement to `support@lexsi.ai`; the project owner must determine which clause applies before execution/publication.
- Verified API: `import auditkit as ak`; `ak.Sample(...)`; `ak.evaluate(samples, model, metrics)`; `ak.compare(base, tuned)`.
- Tiny Aya is documented on the `hf:` backend, but the current docs require Transformers 5.15+ for that backend. Dependency resolution must be tested against the model before GPU execution.
- Decision: deterministic native label metrics remain authoritative. AuditKIT will be added through a thin adapter for experiment artifacts after license acknowledgement/permission and dependency compatibility are resolved.

## Publication allowlist

May be public and ungated only after automated and human checks:

- original source code, configuration, prompts, schemas, and tests without secrets;
- project-created adapters when the base-model and toolkit licenses permit;
- synthetic datasets clearly marked `SYNTHETIC_UNVERIFIED`, with source terms permitting redistribution;
- reviewed datasets only when every included excerpt and metadata record is cleared for public redistribution;
- redacted logs, run metadata, checksums, aggregate metrics, and row-level outputs that contain no restricted text, personal data, credentials, or confidential reviewer information.

Never publish base model weights copied into this project, credentials, personal/confidential data, restricted statutory-source text, unredacted private logs, or artifacts whose upstream license/permission is unresolved.

## Open gates

1. Project owner registration and finalist status.
2. Local Python 3.11 installation or a clean Python 3.11 CI environment.
3. AuditKIT organizational acknowledgement/permission determination.
4. Hugging Face access to the gated model and public collections.
5. Actual Colab Python 3.12/GPU/memory preflight.
