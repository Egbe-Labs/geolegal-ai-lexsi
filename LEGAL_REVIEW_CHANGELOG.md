# Proposed Held-Out Dataset Revision: Before/After Change Log

> This log documents a proposed dataset revision only. It is not legal approval. The original `data/eval/held_out_initial.jsonl` remains unchanged, every proposed record remains `PENDING_REVIEW`, and revised scenarios must be rerun before any comparable baseline analysis.

## Files

- Original: `data/eval/held_out_initial.jsonl`
- Proposed: `data/eval/held_out_proposed_v2.jsonl`

All 15 scenario IDs, questions, labels, statutory-basis fields, source URLs, source version dates, and review statuses are preserved. Only four factual scenario texts are tightened.

## Requested corrections

### KE-EVAL-002

**Before**

> A controller not established or ordinarily resident in Kenya processes personal data of data subjects located in Kenya through an online service.

**After**

> A controller not established or ordinarily resident in Kenya uses an online service to automatically collect, record, store, and otherwise process personal data in electronic customer records about data subjects located in Kenya.

**Reason**

The revision expressly supplies Kenya Data Protection Act 2019 section 4(a)'s recorded-data and automated-processing condition while retaining section 4(b)(ii)'s foreign-controller/Kenyan-data-subject facts. The proposed label remains `APPLIES`, subject to legal review.

### EU-EVAL-004

**Before**

> A controller established only in Argentina processes personal data only about people in Argentina, does not offer goods or services to people in the European Union, and does not monitor behaviour in the European Union.

**After**

> A controller established only in Argentina processes personal data only about people in Argentina, does not offer goods or services to people in the European Union, and does not monitor behaviour in the European Union. The controller is not in a place where the law of an EU Member State applies by virtue of public international law.

**Reason**

The added sentence expressly negates GDPR Article 3(3), complementing the facts already negating Article 3(1) and Article 3(2). The proposed label remains `DOES_NOT_APPLY`, subject to legal review.

## Other negative-label review

### NG-EVAL-003

**Before**

> A company incorporated and operating only in Canada processes personal data only about individuals located in Canada, and no part of the processing occurs in Nigeria.

**After**

> A company is incorporated, domiciled, resident, and operating only in Canada; it is not domiciled in, resident in, or operating in Nigeria. It processes personal data only about data subjects located in Canada, and no part of the processing occurs in Nigeria.

**Reason**

The revision expressly negates each entity-nexus formulation in NDPA 2023 section 2(2)(a), retains the absence of Nigerian processing under section 2(2)(b), and expressly confines data subjects outside Nigeria for section 2(2)(c). The proposed label remains `DOES_NOT_APPLY`, subject to legal review.

### KE-EVAL-003

**Before**

> A controller established only in Brazil processes automated records only about data subjects located in Brazil, and no processing occurs in Kenya.

**After**

> A controller is established and ordinarily resident only in Brazil; it is not established or ordinarily resident in Kenya. It processes automated records only about data subjects located in Brazil, and no processing occurs in Kenya.

**Reason**

The revision expressly negates both “established” and “ordinarily resident” in Kenya under section 4(b)(i), while retaining section 4(a)'s automated-record facts and negating section 4(b)(ii)'s Kenyan-data-subject connection. The proposed label remains `DOES_NOT_APPLY`, subject to legal review.

## Unchanged records

`NG-EVAL-001`, `NG-EVAL-002`, `NG-EVAL-004`, `NG-EVAL-005`, `KE-EVAL-001`, `KE-EVAL-004`, `KE-EVAL-005`, `EU-EVAL-001`, `EU-EVAL-002`, `EU-EVAL-003`, and `EU-EVAL-005` are byte-for-byte equivalent at the record-field level between the two datasets.

## Comparability warning

The original and proposed datasets are different evaluation revisions. Predictions previously generated for any changed scenario are not comparable inputs for the proposed revision. At minimum, `NG-EVAL-003`, `KE-EVAL-002`, `KE-EVAL-003`, and `EU-EVAL-004` must be rerun. For a clean single-revision experiment, rerun all 15 scenarios and record a new dataset hash and run ID before scoring.
