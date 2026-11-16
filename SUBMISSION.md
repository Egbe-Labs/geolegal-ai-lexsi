# GeoLegal-AI Provisional Submission Copy

## Title

GeoLegal-AI: jurisdiction-aware privacy-law applicability classification with Tiny Aya Global

## Track and problem statements

- Track 1 — Fine-tuning and Data Curation
- Problem 1 — regulated-industry domain assistants
- Problem 3 — grounded answers and fewer hallucinations
- Problem 5 — structured output and extraction
- Problem 8 — data-scarce domains

## Abstract

GeoLegal-AI is a jurisdiction-aware legal AI research prototype that tests whether a small open-weight model can identify when privacy and personal-data law applies to a factual scenario. It covers the Nigeria Data Protection Act 2023, Kenya Data Protection Act 2019, and EU GDPR, with a controlled output contract: APPLIES, DOES_NOT_APPLY, or INSUFFICIENT_INFORMATION; jurisdiction and framework; a short explanation; statutory references; and missing facts or uncertainty.

The project uses CohereLabs/tiny-aya-global at a pinned revision. It includes a legally reviewed and frozen 15-scenario held-out set, deterministic scoring, a Google Colab baseline notebook, and protected-set leakage controls across all evaluation revisions. A separate 90-record synthetic candidate set is balanced across jurisdictions and labels, split by scenario family, and blocked from training export until human legal review and leakage clearance are complete.

The project owner reports an E1 no-retrieval baseline of 46.67% classification accuracy, 24.56% macro F1, and 66.67% parse rate. The row-level prediction and scored metrics files are not currently checked into the repository, so these results are provisional and not independently reproducible from the submitted checkout. Fine-tuning, E2 retrieval evaluation, E3 evaluation, and an executed multi-toolkit chain have not been completed. GeoLegal-AI therefore makes no before/after improvement claim.

The project is a research classifier, not professional legal advice. Its main contribution at this stage is a transparent, reproducible baseline and a legally cautious data/evaluation pipeline that makes uncertainty, provenance, leakage, and incomplete evidence visible.

## Headline result

Tiny Aya E1 baseline, user-reported: **46.67% accuracy / 24.56% macro F1 / 66.67% parse rate** on 15 frozen scenarios. No post-training result exists.

## Model and method

`CohereLabs/tiny-aya-global` at revision `af89d219b53ed9b13b8a4645f9c8028973510324`; deterministic no-retrieval baseline with strict structured-output parsing.

## Artifact links

- GitHub: https://github.com/Egbe-Labs/geolegal-ai-lexsi
- Hugging Face model collection: **NOT YET PUBLISHED**
- Hugging Face dataset collection: **NOT YET PUBLISHED**
- Write-up: repository `README.md`
- Demo/Space: **NOT AVAILABLE**
- Video/slides: **NOT AVAILABLE**

## Required owner declarations before form submission

- Registered team email: **OWNER MUST SUPPLY IN FORM**
- Team members and Hugging Face usernames: **OWNER MUST SUPPLY**
- Work completed outside the hackathon: **OWNER MUST SUPPLY TRUTHFUL DECLARATION**
- Author contributions: **OWNER MUST SUPPLY**
- LLM/AI assistance statement: **OWNER MUST SUPPLY**
- Finalist/late-submission eligibility: **OWNER MUST CONFIRM**
