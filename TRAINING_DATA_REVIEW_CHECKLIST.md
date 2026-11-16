# GeoLegal-AI Candidate Training Data Review Checklist

## Status and scope

This checklist applies to `data/train/candidates_v1.jsonl` (90 synthetic candidates: 72 `TRAIN`, 18 `VALIDATION`). Every record is `PENDING_REVIEW` and `SYNTHETIC_UNVERIFIED`. This document is a review aid, not evidence of approval.

The protected held-out set comprises all records and variants in:

- `data/eval/held_out_initial.jsonl`
- `data/eval/held_out_proposed_v2.jsonl`
- `data/eval/held_out_approved_v1.jsonl`

Reviewers must not use those scenarios to improve, rewrite, or derive training candidates.

## Per-record legal review

For every candidate, confirm and record separately:

- [ ] The scenario is genuinely new and is not a paraphrase, transformed version, role reversal, or superficial factual substitution of a protected held-out scenario.
- [ ] The facts establish or intentionally omit every condition needed for the proposed closed label.
- [ ] `APPLIES` records establish the relevant statutory scope conditions.
- [ ] `DOES_NOT_APPLY` records negate every relevant territorial or material-scope route addressed by the cited provision.
- [ ] `INSUFFICIENT_INFORMATION` records identify the genuinely outcome-relevant missing facts.
- [ ] The jurisdiction and legal framework are correct.
- [ ] The statutory provision exists in the linked authoritative legislation and supports the explanation.
- [ ] The explanation is accurate, short, and does not add facts absent from the scenario.
- [ ] The source URL and version date are correct and suitable for public dataset provenance.
- [ ] The scenario contains no personal, confidential, or restricted information.
- [ ] The record may be published publicly and ungated under applicable source and project terms.
- [ ] The scenario family belongs only to its assigned split.

## Jurisdiction-specific checks

### Nigeria

- [ ] Apply NDPA 2023 section 2(1)–(2) precisely: personal-data processing plus the stated controller/processor, processing-location, or data-subject-in-Nigeria connection.
- [ ] Do not infer Nigerian domicile, residence, operation, processing, or data-subject location from nationality alone.

### Kenya

- [ ] Confirm section 4(a)'s record requirement: automated processing, or non-automated processing that forms part of a filing system.
- [ ] Separately confirm section 4(b)'s establishment/ordinary-residence and location conditions.

### European Union

- [ ] Assess GDPR Article 3(1), 3(2)(a), 3(2)(b), and 3(3) where relevant.
- [ ] Do not equate accessibility, euros, language, citizenship, or historical travel with intentional offering or monitoring in the Union without supporting facts.

## Leakage review

- [ ] Re-run `python scripts/prepare_training_data.py` after any candidate text, ID, family, or split changes.
- [ ] Confirm there are no ID, protected-family, or normalized-exact overlaps.
- [ ] Manually inspect every entry in `flagged_near_matches` in `data/train/leakage_report_v1.json`.
- [ ] Record each flagged pair as `CLEARED` or remove/rewrite the candidate; an unexplained threshold adjustment is not clearance.
- [ ] Re-run checks after rewrites because a rewrite can create a new collision.

## Approval and export gate

- [ ] Record approval only from an identified authorized review process; do not infer it from this checklist.
- [ ] Change `review_status` only after substantive legal review is complete.
- [ ] Ensure every candidate is legally reviewed and every near-match is cleared before calling `export_prompt_completion`.
- [ ] Confirm train and validation prompt/completion files do not yet exist while any review remains pending.
- [ ] Preserve the frozen evaluation dataset and checksum unchanged.

Reviewer identity, credentials, review date, signature, decisions, and notes must be supplied by the actual reviewer or project owner. None are invented or pre-filled here.
