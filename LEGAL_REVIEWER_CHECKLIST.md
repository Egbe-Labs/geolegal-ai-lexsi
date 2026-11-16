# Concise Legal Reviewer Checklist

> Review aid only. Checking a box records reviewer work; it does not automatically modify the dataset or confer `LEGAL_REVIEWED` status.

## Per-scenario checks

- [ ] Confirm the scenario states facts rather than embedding a legal conclusion.
- [ ] Confirm the entity is correctly characterized as controller or processor.
- [ ] Confirm the information and activity qualify as personal data and processing where required.
- [ ] Confirm every element of the cited territorial/application provision is established for `APPLIES`.
- [ ] Confirm every relevant territorial route is expressly negated for `DOES_NOT_APPLY`.
- [ ] Confirm genuinely outcome-determinative facts are missing for `INSUFFICIENT_INFORMATION`.
- [ ] Confirm the proposed label is exactly `APPLIES`, `DOES_NOT_APPLY`, or `INSUFFICIENT_INFORMATION`.
- [ ] Confirm the statutory citation matches the official source and cited version date.
- [ ] Check whether later legislation, binding amendments, or authoritative interpretation changes the analysis.
- [ ] Record disagreements, qualifications, and required edits without changing `review_status` prematurely.

## Targeted checks for proposed v2

- [ ] **KE-EVAL-002:** Does automated collection, recording, storage, and processing in electronic customer records satisfy section 4(a), together with section 4(b)(ii)?
- [ ] **EU-EVAL-004:** Does the added public-international-law fact fully negate Article 3(3), alongside Articles 3(1) and 3(2)?
- [ ] **NG-EVAL-003:** Are domicile, residence, operation, processing location, and data-subject location stated sufficiently to test every section 2(2) route?
- [ ] **KE-EVAL-003:** Are establishment, ordinary residence, processing form/location, and data-subject location stated sufficiently to test every section 4 route?

## Dataset-level checks

- [ ] Verify all 15 IDs are preserved and unique.
- [ ] Verify the jurisdiction distribution remains 5 Nigeria, 5 Kenya, and 5 EU.
- [ ] Verify no label outside the three-label taxonomy appears.
- [ ] Verify all records remain `PENDING_REVIEW` until an authorized review workflow records approval.
- [ ] Freeze and hash the accepted dataset revision.
- [ ] Rerun every revised scenario—or preferably all 15—for a comparable baseline before scoring.
- [ ] Do not reuse predictions produced from `held_out_initial.jsonl` as predictions for `held_out_proposed_v2.jsonl`.

## Reviewer record

- Reviewer name/qualification: ______________________________
- Jurisdiction(s): __________________________________________
- Review date: ______________________________________________
- Dataset hash reviewed: ____________________________________
- Notes/adjudication reference: ______________________________
