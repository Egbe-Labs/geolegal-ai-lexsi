# Lexsi Submission Readiness Audit

Audit basis: official hackathon page checked on 2026-11-16. This is a repository audit, not organizer confirmation of eligibility.

## Executive result

GeoLegal-AI is publishable as a transparent baseline research prototype, but it does not currently meet the full Track 1 experiment requirements. Submit only if the form permits an incomplete/provisional entry or if an earlier valid submission is being updated. Do not claim fine-tuning, a chained toolkit pipeline, or before/after improvement.

## Requirements matrix

| Requirement | Repository evidence | Status | Immediate action |
|---|---|---|---|
| Team of 1–3; registration completed | No registration evidence in repository | Owner verification required | Confirm registered team email and finalist status |
| Track 1 project | Fixed in project documentation | Ready | None |
| Approved Cohere dense model | Tiny Aya Global pinned and baseline notebook provided | Ready | None |
| Chain at least two Track 1 repositories | AlignTune adapter exists; no executed CuratorKIT/AlignTune/AuditKIT chain | **Not met** | Do not describe native code as toolkit execution |
| Prefer three Track 1 repositories | No executed chain | Not met | Future: CuratorKIT → AlignTune → AuditKIT |
| More than one before/after metric | Only provisional E1 metrics; no post-training run | **Not met** | Fine-tune and evaluate later; do not fabricate |
| Public project/repository | GitHub origin configured | Public visibility not independently verified | Confirm in logged-out browser |
| Public, ungated HF model collection | `https://huggingface.co/collections/EA-Labs/geolegal-ai-models` supplied by project owner | Visibility not independently verified; no fine-tuned adapter claimed | Confirm while logged out |
| Public HF dataset/log collection | `https://huggingface.co/datasets/EA-Labs/geolegal-ai-dataset` supplied by project owner | Visibility not independently verified | Confirm while logged out |
| Abstract under 500 words | Draft in `SUBMISSION.md` | Ready after owner review | Review text |
| Write-up identifies track/problem statements | README | Ready | None |
| Model, configuration, version, license | README and dependency decisions | Ready | None |
| Dataset source, distribution, splits, leakage | README, manifests, leakage report | Partial: candidate data unreviewed | Complete human review later |
| CuratorKIT filtering counts | CuratorKIT not run | Not applicable yet | Do not claim |
| Metrics and rationale | Evaluation specification and README | Partial | Add actual row-level artifact |
| Training setup and hyperparameters | AlignTune adapter defaults documented; no actual run | Planned only | Do not claim execution |
| Same model before vs after table | No after model | **Missing** | Requires fine-tuning |
| Limitations and negative results | README | Ready | None |
| Repo layout and reproducibility | README | Ready | None |
| Work outside hackathon declaration | Not supplied | Owner action required | Supply truthful declaration |
| Author contributions and teammate tags | Not supplied | Owner action required | Supply details |
| LLM usage statement | Not supplied | Owner action required | Supply statement |

## Evidence integrity

- The frozen evaluation set contains 15 legally reviewed records and has a matching SHA-256 manifest.
- Candidate data is explicitly pending review and cannot be exported by the implemented gate.
- Automated leakage checks protect all three evaluation revisions.
- The reported 46.67% accuracy, 24.56% macro F1, and 66.67% parse rate were supplied by the project owner but are not reproducible from checked-in row-level artifacts.
- `results/baseline_metrics.json` is a historical unscored placeholder and must not be presented as the reported baseline.
- No fine-tuning or retrieval experiment has been claimed.

## Immediate owner-only submission actions

1. Confirm the team is eligible to submit now, especially whether it was shortlisted for the November 22 stage.
2. Supply the registered email and teammate/Hugging Face usernames directly to the submission form, not the repository.
3. Recover and add the exact Colab-generated row-level E1 prediction file and matching metrics JSON.
4. Confirm public visibility of GitHub from a logged-out session.
5. Confirm the supplied Hugging Face model collection and dataset repository are public and ungated from a logged-out browser; publish only artifacts cleared for release.
6. Provide truthful work-outside-hackathon, author-contribution, and LLM-use statements.
7. Submit the provisional baseline only with the limitations above; do not select fields implying completed fine-tuning or toolkit chaining.
