# GeoLegal-AI Training Data Legal Review Draft

> **Review status:** Draft only. All 90 records remain `PENDING_REVIEW` and `SYNTHETIC_UNVERIFIED`. This document does not approve any label, explanation, authority, or dataset record.

## Flagged-scenario summary

- Candidate records reviewed: **90**.
- Records with at least one specific flag: **55**.
- Records without a specific drafting flag: **35**; these still require full human legal review.
- Flag instances: `CONCEPTUAL_OVERLAP` 52, `DATA_QUALITY` 4, `LEGAL_AMBIGUITY` 5, `TERRITORIAL_ROUTE` 7.
- Automated leakage report result: no threshold-level ID, family, normalized-exact, token-trigram, or character-five-gram matches. That result does not clear conceptual overlap.
- No dataset record, review status, held-out file, or prompt/completion export was changed or created by this review.

### Critical data-quality flags

- `EU-TRN-I-04` — The missing_facts field is malformed as one array element per character instead of one complete missing-fact string.
- `EU-TRN-N-08` — The scenario contains a replacement character in “Bogotá”; correct the source encoding before review or export.
- `KE-TRN-A-08` — The scenario contains replacement characters in “résumés”; correct the source encoding before review or export.
- `KE-VAL-N-10` — The scenario contains a replacement character in “São Paulo”; correct the source encoding before review or export.

### Negative applicability routes needing clarification

- `KE-VAL-N-10` — “No Kenyan connection” is conclusory and does not separately negate establishment or ordinary residence under section 4(b).
- `NG-TRN-N-02` — The facts say no Nigerian activity or establishment, but do not expressly negate domicile or residence using the section 2 terms.
- `NG-TRN-N-03` — “No Nigerian operational connection” is vague and does not separately negate domicile, residence, and operation.
- `NG-TRN-N-05` — No Nigerian business or processing is stated, but Nigerian domicile and residence are not expressly negated.
- `NG-TRN-N-06` — No Nigerian entity or operation is stated, but domicile and residence are not expressly negated.
- `NG-TRN-N-08` — The club and provider do not operate from Nigeria, but their domicile and residence are not expressly negated.
- `NG-VAL-N-10` — No Nigerian customers, staff, systems, or processing are stated, but controller domicile, residence, and operation are not expressly negated.

### Legally questionable or potentially conclusive assumptions

- `EU-VAL-A-10` — The scenario stipulates the Article 3(3) legal conclusion (“Spanish law applies”) rather than facts establishing why public international law produces that result.
- `KE-TRN-I-02` — Temporary voice-assistant handling may itself involve automated recording or processing; clarify what is captured in memory and whether it is entered in a record.
- `KE-TRN-I-07` — The described act is human recollection. Unless a structured record is actually consulted or updated, the facts may support DOES_NOT_APPLY rather than uncertainty.
- `KE-VAL-I-09` — Automated facial detection may process a digital image even if it is immediately discarded; clarify whether the transient image or logs constitute a record under section 4(a).
- `NG-VAL-I-09` — Pseudonymised information remains personal data when re-identification is possible; the scenario omits whether the consortium retains or can access identifying information.

### Repetition and held-out conceptual overlap

- All ten Nigeria negative records use the same foreign-only/no-Nigeria structure as `NG-EVAL-003`.
- Six Kenya foreign-only negative records repeat the structure of `KE-EVAL-003`; four other Kenya negatives repeatedly test unrecorded human memory or loose notes.
- All ten EU negative records repeat the full Article 3 negation structure of `EU-EVAL-004` and often state legal conclusions rather than neutral facts.
- All ten Nigeria uncertainty records repeat the missing-geography structure of `NG-EVAL-004`.
- All ten Kenya uncertainty records combine unknown record/filing-system facts with unknown geography, closely tracking `KE-EVAL-004`.
- Six EU uncertainty records repeat the unknown location/offering/monitoring structure of `EU-EVAL-005`.
- The question text is identical within each jurisdiction across all labels, and many explanations reuse a single statutory formula. Reviewers should assess whether this creates label cues or an artificially narrow training distribution.

## Scenario-by-scenario review

## Nigeria

### APPLIES

#### NG-TRN-A-01 — TRAIN

- **Factual scenario:** A Nigerian airline operating from Port Harcourt stores passenger contact and passport data on servers in Iceland for flights it manages from Nigeria.
- **Question:** Which closed label describes whether Nigeria Data Protection Act 2023 applies on these facts?
- **Proposed label:** `APPLIES`
- **Statutory provision:** Nigeria Data Protection Act 2023, section 2(1)-(2)
- **Source URL:** https://ndpc.gov.ng/wp-content/uploads/2024/03/Nigeria_Data_Protection_Act_2023.pdf
- **Proposed statutory reasoning:** Section 2 is engaged because the controller operates in Nigeria and processes personal data, regardless of the offshore server location.
- **Review flag:** PENDING_REVIEW — no specific drafting defect identified; substantive legal review still required.

#### NG-TRN-A-02 — TRAIN

- **Factual scenario:** A Japanese athletics platform collects heart-rate and identity data from competitors while they attend a tournament in Lagos, although the platform has no Nigerian office.
- **Question:** Which closed label describes whether Nigeria Data Protection Act 2023 applies on these facts?
- **Proposed label:** `APPLIES`
- **Statutory provision:** Nigeria Data Protection Act 2023, section 2(1)-(2)
- **Source URL:** https://ndpc.gov.ng/wp-content/uploads/2024/03/Nigeria_Data_Protection_Act_2023.pdf
- **Proposed statutory reasoning:** Section 2 extends to an overseas controller processing personal data of data subjects in Nigeria.
- **Review flag:** PENDING_REVIEW — no specific drafting defect identified; substantive legal review still required.

#### NG-TRN-A-03 — TRAIN

- **Factual scenario:** A records contractor working from Kano digitises employee files for a Ghanaian corporate client and uploads the resulting database to Accra.
- **Question:** Which closed label describes whether Nigeria Data Protection Act 2023 applies on these facts?
- **Proposed label:** `APPLIES`
- **Statutory provision:** Nigeria Data Protection Act 2023, section 2(1)-(2)
- **Source URL:** https://ndpc.gov.ng/wp-content/uploads/2024/03/Nigeria_Data_Protection_Act_2023.pdf
- **Proposed statutory reasoning:** The processor operates and performs processing in Nigeria, supplying territorial connections under section 2.
- **Review flag:** PENDING_REVIEW — no specific drafting defect identified; substantive legal review still required.

#### NG-TRN-A-04 — TRAIN

- **Factual scenario:** A United States telemedicine provider schedules video consultations specifically for patients physically present in Abuja and records their symptoms and contact details.
- **Question:** Which closed label describes whether Nigeria Data Protection Act 2023 applies on these facts?
- **Proposed label:** `APPLIES`
- **Statutory provision:** Nigeria Data Protection Act 2023, section 2(1)-(2)
- **Source URL:** https://ndpc.gov.ng/wp-content/uploads/2024/03/Nigeria_Data_Protection_Act_2023.pdf
- **Proposed statutory reasoning:** The overseas provider processes personal data of data subjects in Nigeria, bringing the activity within section 2.
- **Review flag:** PENDING_REVIEW — no specific drafting defect identified; substantive legal review still required.

#### NG-TRN-A-05 — TRAIN

- **Factual scenario:** A Nigerian university's Enugu admissions office scores applications from students throughout West Africa using a cloud service hosted in Singapore.
- **Question:** Which closed label describes whether Nigeria Data Protection Act 2023 applies on these facts?
- **Proposed label:** `APPLIES`
- **Statutory provision:** Nigeria Data Protection Act 2023, section 2(1)-(2)
- **Source URL:** https://ndpc.gov.ng/wp-content/uploads/2024/03/Nigeria_Data_Protection_Act_2023.pdf
- **Proposed statutory reasoning:** The controller operates in Nigeria and the processing activity occurs through its Nigerian office.
- **Review flag:** PENDING_REVIEW — no specific drafting defect identified; substantive legal review still required.

#### NG-TRN-A-06 — TRAIN

- **Factual scenario:** A freight company domiciled in Nigeria tracks its drivers in Benin and Togo using vehicle identifiers linked to named employees.
- **Question:** Which closed label describes whether Nigeria Data Protection Act 2023 applies on these facts?
- **Proposed label:** `APPLIES`
- **Statutory provision:** Nigeria Data Protection Act 2023, section 2(1)-(2)
- **Source URL:** https://ndpc.gov.ng/wp-content/uploads/2024/03/Nigeria_Data_Protection_Act_2023.pdf
- **Proposed statutory reasoning:** The controller's Nigerian domicile is a sufficient section 2 connection even though tracking occurs abroad.
- **Review flag:** PENDING_REVIEW — no specific drafting defect identified; substantive legal review still required.

#### NG-TRN-A-07 — TRAIN

- **Factual scenario:** A South African conference organiser scans attendee badges and stores dietary information during a three-day event in Calabar.
- **Question:** Which closed label describes whether Nigeria Data Protection Act 2023 applies on these facts?
- **Proposed label:** `APPLIES`
- **Statutory provision:** Nigeria Data Protection Act 2023, section 2(1)-(2)
- **Source URL:** https://ndpc.gov.ng/wp-content/uploads/2024/03/Nigeria_Data_Protection_Act_2023.pdf
- **Proposed statutory reasoning:** The processing occurs in Nigeria and concerns identifiable attendees, engaging section 2.
- **Review flag:** PENDING_REVIEW — no specific drafting defect identified; substantive legal review still required.

#### NG-TRN-A-08 — TRAIN

- **Factual scenario:** A payroll processor resident in Nigeria calculates salaries for remote workers employed by a company in Rwanda.
- **Question:** Which closed label describes whether Nigeria Data Protection Act 2023 applies on these facts?
- **Proposed label:** `APPLIES`
- **Statutory provision:** Nigeria Data Protection Act 2023, section 2(1)-(2)
- **Source URL:** https://ndpc.gov.ng/wp-content/uploads/2024/03/Nigeria_Data_Protection_Act_2023.pdf
- **Proposed statutory reasoning:** Section 2 applies because the processor is resident in Nigeria while processing personal data.
- **Review flag:** PENDING_REVIEW — no specific drafting defect identified; substantive legal review still required.

#### NG-VAL-A-09 — VALIDATION

- **Factual scenario:** A Brazilian travel application obtains precise location data from tourists while they travel through Osun State, with no office in Nigeria.
- **Question:** Which closed label describes whether Nigeria Data Protection Act 2023 applies on these facts?
- **Proposed label:** `APPLIES`
- **Statutory provision:** Nigeria Data Protection Act 2023, section 2(1)-(2)
- **Source URL:** https://ndpc.gov.ng/wp-content/uploads/2024/03/Nigeria_Data_Protection_Act_2023.pdf
- **Proposed statutory reasoning:** The controller processes personal data of individuals while they are in Nigeria, a connection addressed by section 2(2)(c).
- **Review flag:** PENDING_REVIEW — no specific drafting defect identified; substantive legal review still required.

#### NG-VAL-A-10 — VALIDATION

- **Factual scenario:** A charity operating a field office in Maiduguri enters beneficiary names and household details into a database administered from London.
- **Question:** Which closed label describes whether Nigeria Data Protection Act 2023 applies on these facts?
- **Proposed label:** `APPLIES`
- **Statutory provision:** Nigeria Data Protection Act 2023, section 2(1)-(2)
- **Source URL:** https://ndpc.gov.ng/wp-content/uploads/2024/03/Nigeria_Data_Protection_Act_2023.pdf
- **Proposed statutory reasoning:** The charity operates in Nigeria and processes personal data through that operation, notwithstanding foreign administration.
- **Review flag:** PENDING_REVIEW — no specific drafting defect identified; substantive legal review still required.

### DOES_NOT_APPLY

#### NG-TRN-N-01 — TRAIN

- **Factual scenario:** A Chilean vineyard with no Nigerian domicile, residence, operations, customers, staff, or infrastructure records only the details of visitors physically in Chile; no processing occurs in Nigeria.
- **Question:** Which closed label describes whether Nigeria Data Protection Act 2023 applies on these facts?
- **Proposed label:** `DOES_NOT_APPLY`
- **Statutory provision:** Nigeria Data Protection Act 2023, section 2(1)-(2)
- **Source URL:** https://ndpc.gov.ng/wp-content/uploads/2024/03/Nigeria_Data_Protection_Act_2023.pdf
- **Proposed statutory reasoning:** None of the controller, processing-location, or data-subject-in-Nigeria connections in section 2 is present.
- **Review flag:** PENDING_REVIEW — FLAGGED: [CONCEPTUAL_OVERLAP] Foreign-only negative pattern is conceptually close to NG-EVAL-003 and repeats a ten-record statutory-negation template.

#### NG-TRN-N-02 — TRAIN

- **Factual scenario:** A municipal library in Finland catalogues borrowing histories only for patrons in Finland, using systems located there, and has no Nigerian activity or establishment.
- **Question:** Which closed label describes whether Nigeria Data Protection Act 2023 applies on these facts?
- **Proposed label:** `DOES_NOT_APPLY`
- **Statutory provision:** Nigeria Data Protection Act 2023, section 2(1)-(2)
- **Source URL:** https://ndpc.gov.ng/wp-content/uploads/2024/03/Nigeria_Data_Protection_Act_2023.pdf
- **Proposed statutory reasoning:** The stated processing has no territorial connection described in section 2.
- **Review flag:** PENDING_REVIEW — FLAGGED: [TERRITORIAL_ROUTE] The facts say no Nigerian activity or establishment, but do not expressly negate domicile or residence using the section 2 terms. [CONCEPTUAL_OVERLAP] Foreign-only negative pattern is conceptually close to NG-EVAL-003 and repeats a ten-record statutory-negation template.

#### NG-TRN-N-03 — TRAIN

- **Factual scenario:** A New Zealand farm records local employees' shift times entirely in New Zealand and neither the employer nor the workers have any Nigerian operational connection.
- **Question:** Which closed label describes whether Nigeria Data Protection Act 2023 applies on these facts?
- **Proposed label:** `DOES_NOT_APPLY`
- **Statutory provision:** Nigeria Data Protection Act 2023, section 2(1)-(2)
- **Source URL:** https://ndpc.gov.ng/wp-content/uploads/2024/03/Nigeria_Data_Protection_Act_2023.pdf
- **Proposed statutory reasoning:** The controller, processing, and affected data subjects are all outside Nigeria on the stated facts.
- **Review flag:** PENDING_REVIEW — FLAGGED: [TERRITORIAL_ROUTE] “No Nigerian operational connection” is vague and does not separately negate domicile, residence, and operation. [CONCEPTUAL_OVERLAP] Foreign-only negative pattern is conceptually close to NG-EVAL-003 and repeats a ten-record statutory-negation template.

#### NG-TRN-N-04 — TRAIN

- **Factual scenario:** A Peruvian clinic treats and records only patients located in Peru, stores the files in Lima, and neither operates nor is domiciled or resident in Nigeria.
- **Question:** Which closed label describes whether Nigeria Data Protection Act 2023 applies on these facts?
- **Proposed label:** `DOES_NOT_APPLY`
- **Statutory provision:** Nigeria Data Protection Act 2023, section 2(1)-(2)
- **Source URL:** https://ndpc.gov.ng/wp-content/uploads/2024/03/Nigeria_Data_Protection_Act_2023.pdf
- **Proposed statutory reasoning:** No section 2 territorial limb is satisfied by the stated facts.
- **Review flag:** PENDING_REVIEW — FLAGGED: [CONCEPTUAL_OVERLAP] Foreign-only negative pattern is conceptually close to NG-EVAL-003 and repeats a ten-record statutory-negation template.

#### NG-TRN-N-05 — TRAIN

- **Factual scenario:** A Norwegian theatre keeps an Oslo-only membership list for local patrons and conducts no business, data collection, or processing in Nigeria.
- **Question:** Which closed label describes whether Nigeria Data Protection Act 2023 applies on these facts?
- **Proposed label:** `DOES_NOT_APPLY`
- **Statutory provision:** Nigeria Data Protection Act 2023, section 2(1)-(2)
- **Source URL:** https://ndpc.gov.ng/wp-content/uploads/2024/03/Nigeria_Data_Protection_Act_2023.pdf
- **Proposed statutory reasoning:** The scenario expressly excludes the Nigerian connections listed in section 2.
- **Review flag:** PENDING_REVIEW — FLAGGED: [TERRITORIAL_ROUTE] No Nigerian business or processing is stated, but Nigerian domicile and residence are not expressly negated. [CONCEPTUAL_OVERLAP] Foreign-only negative pattern is conceptually close to NG-EVAL-003 and repeats a ten-record statutory-negation template.

#### NG-TRN-N-06 — TRAIN

- **Factual scenario:** A Thai manufacturer processes factory access logs solely for workers at its Bangkok site and has no Nigerian entity, operation, processor, or data subjects.
- **Question:** Which closed label describes whether Nigeria Data Protection Act 2023 applies on these facts?
- **Proposed label:** `DOES_NOT_APPLY`
- **Statutory provision:** Nigeria Data Protection Act 2023, section 2(1)-(2)
- **Source URL:** https://ndpc.gov.ng/wp-content/uploads/2024/03/Nigeria_Data_Protection_Act_2023.pdf
- **Proposed statutory reasoning:** The processing lacks a Nigerian controller, processor, location, or data-subject connection.
- **Review flag:** PENDING_REVIEW — FLAGGED: [TERRITORIAL_ROUTE] No Nigerian entity or operation is stated, but domicile and residence are not expressly negated. [CONCEPTUAL_OVERLAP] Foreign-only negative pattern is conceptually close to NG-EVAL-003 and repeats a ten-record statutory-negation template.

#### NG-TRN-N-07 — TRAIN

- **Factual scenario:** An Argentine museum photographs ticket holders only at its Buenos Aires entrance, stores the images locally, and has no presence or processing activity in Nigeria.
- **Question:** Which closed label describes whether Nigeria Data Protection Act 2023 applies on these facts?
- **Proposed label:** `DOES_NOT_APPLY`
- **Statutory provision:** Nigeria Data Protection Act 2023, section 2(1)-(2)
- **Source URL:** https://ndpc.gov.ng/wp-content/uploads/2024/03/Nigeria_Data_Protection_Act_2023.pdf
- **Proposed statutory reasoning:** The facts negate each territorial basis in section 2.
- **Review flag:** PENDING_REVIEW — FLAGGED: [CONCEPTUAL_OVERLAP] Foreign-only negative pattern is conceptually close to NG-EVAL-003 and repeats a ten-record statutory-negation template.

#### NG-TRN-N-08 — TRAIN

- **Factual scenario:** A Swiss hiking club maintains emergency contacts solely for members located in Switzerland and neither the club nor its service provider operates from Nigeria.
- **Question:** Which closed label describes whether Nigeria Data Protection Act 2023 applies on these facts?
- **Proposed label:** `DOES_NOT_APPLY`
- **Statutory provision:** Nigeria Data Protection Act 2023, section 2(1)-(2)
- **Source URL:** https://ndpc.gov.ng/wp-content/uploads/2024/03/Nigeria_Data_Protection_Act_2023.pdf
- **Proposed statutory reasoning:** No stated actor, processing operation, or data subject is connected to Nigeria under section 2.
- **Review flag:** PENDING_REVIEW — FLAGGED: [TERRITORIAL_ROUTE] The club and provider do not operate from Nigeria, but their domicile and residence are not expressly negated. [CONCEPTUAL_OVERLAP] Foreign-only negative pattern is conceptually close to NG-EVAL-003 and repeats a ten-record statutory-negation template.

#### NG-VAL-N-09 — VALIDATION

- **Factual scenario:** A Malaysian school processes attendance information only for pupils in Kuala Lumpur on Malaysian systems and has no Nigerian domicile, residence, or operation.
- **Question:** Which closed label describes whether Nigeria Data Protection Act 2023 applies on these facts?
- **Proposed label:** `DOES_NOT_APPLY`
- **Statutory provision:** Nigeria Data Protection Act 2023, section 2(1)-(2)
- **Source URL:** https://ndpc.gov.ng/wp-content/uploads/2024/03/Nigeria_Data_Protection_Act_2023.pdf
- **Proposed statutory reasoning:** The stated activity falls outside all section 2 territorial connectors.
- **Review flag:** PENDING_REVIEW — FLAGGED: [CONCEPTUAL_OVERLAP] Foreign-only negative pattern is conceptually close to NG-EVAL-003 and repeats a ten-record statutory-negation template.

#### NG-VAL-N-10 — VALIDATION

- **Factual scenario:** A Mexican repair shop keeps customer telephone numbers solely for jobs performed in Guadalajara, with no Nigerian customers, staff, systems, or processing.
- **Question:** Which closed label describes whether Nigeria Data Protection Act 2023 applies on these facts?
- **Proposed label:** `DOES_NOT_APPLY`
- **Statutory provision:** Nigeria Data Protection Act 2023, section 2(1)-(2)
- **Source URL:** https://ndpc.gov.ng/wp-content/uploads/2024/03/Nigeria_Data_Protection_Act_2023.pdf
- **Proposed statutory reasoning:** The facts affirmatively exclude the territorial circumstances specified in section 2.
- **Review flag:** PENDING_REVIEW — FLAGGED: [TERRITORIAL_ROUTE] No Nigerian customers, staff, systems, or processing are stated, but controller domicile, residence, and operation are not expressly negated. [CONCEPTUAL_OVERLAP] Foreign-only negative pattern is conceptually close to NG-EVAL-003 and repeats a ten-record statutory-negation template.

### INSUFFICIENT_INFORMATION

#### NG-TRN-I-01 — TRAIN

- **Factual scenario:** A satellite communications company analyses subscriber identifiers aboard a vessel, but the record does not identify where the vessel, subscribers, controller, or processing equipment are located.
- **Question:** Which closed label describes whether Nigeria Data Protection Act 2023 applies on these facts?
- **Proposed label:** `INSUFFICIENT_INFORMATION`
- **Statutory provision:** Nigeria Data Protection Act 2023, section 2(1)-(2)
- **Source URL:** https://ndpc.gov.ng/wp-content/uploads/2024/03/Nigeria_Data_Protection_Act_2023.pdf
- **Proposed statutory reasoning:** Section 2 applicability cannot be resolved without a Nigerian connection through an actor, processing location, or data subject.
- **Review flag:** PENDING_REVIEW — FLAGGED: [CONCEPTUAL_OVERLAP] Missing actor, processing, or data-subject location follows the same uncertainty structure as NG-EVAL-004; confirm this is not a superficial transformation.

#### NG-TRN-I-02 — TRAIN

- **Factual scenario:** A global hotel group centralises guest profiles, but it is unclear whether its unnamed West African branch is in Nigeria or whether Nigerian guests are included.
- **Question:** Which closed label describes whether Nigeria Data Protection Act 2023 applies on these facts?
- **Proposed label:** `INSUFFICIENT_INFORMATION`
- **Statutory provision:** Nigeria Data Protection Act 2023, section 2(1)-(2)
- **Source URL:** https://ndpc.gov.ng/wp-content/uploads/2024/03/Nigeria_Data_Protection_Act_2023.pdf
- **Proposed statutory reasoning:** The facts do not establish any of the alternative section 2 territorial links.
- **Review flag:** PENDING_REVIEW — FLAGGED: [CONCEPTUAL_OVERLAP] Missing actor, processing, or data-subject location follows the same uncertainty structure as NG-EVAL-004; confirm this is not a superficial transformation.

#### NG-TRN-I-03 — TRAIN

- **Factual scenario:** A wearable-device vendor receives emergency telemetry from a traveller whose country at the time of collection is not recorded; the vendor's operating locations are also unstated.
- **Question:** Which closed label describes whether Nigeria Data Protection Act 2023 applies on these facts?
- **Proposed label:** `INSUFFICIENT_INFORMATION`
- **Statutory provision:** Nigeria Data Protection Act 2023, section 2(1)-(2)
- **Source URL:** https://ndpc.gov.ng/wp-content/uploads/2024/03/Nigeria_Data_Protection_Act_2023.pdf
- **Proposed statutory reasoning:** The data-subject and controller locations needed for section 2 are missing.
- **Review flag:** PENDING_REVIEW — FLAGGED: [CONCEPTUAL_OVERLAP] Missing actor, processing, or data-subject location follows the same uncertainty structure as NG-EVAL-004; confirm this is not a superficial transformation.

#### NG-TRN-I-04 — TRAIN

- **Factual scenario:** A regional payment switch processes cardholder names at an undisclosed data centre for banks in several unnamed countries.
- **Question:** Which closed label describes whether Nigeria Data Protection Act 2023 applies on these facts?
- **Proposed label:** `INSUFFICIENT_INFORMATION`
- **Statutory provision:** Nigeria Data Protection Act 2023, section 2(1)-(2)
- **Source URL:** https://ndpc.gov.ng/wp-content/uploads/2024/03/Nigeria_Data_Protection_Act_2023.pdf
- **Proposed statutory reasoning:** Neither the actors nor the processing or data-subject locations are sufficiently specified for section 2.
- **Review flag:** PENDING_REVIEW — FLAGGED: [CONCEPTUAL_OVERLAP] Missing actor, processing, or data-subject location follows the same uncertainty structure as NG-EVAL-004; confirm this is not a superficial transformation.

#### NG-TRN-I-05 — TRAIN

- **Factual scenario:** An employer uses a remote background-check vendor for a worker described only as being in West Africa, and neither organisation's place of operation is given.
- **Question:** Which closed label describes whether Nigeria Data Protection Act 2023 applies on these facts?
- **Proposed label:** `INSUFFICIENT_INFORMATION`
- **Statutory provision:** Nigeria Data Protection Act 2023, section 2(1)-(2)
- **Source URL:** https://ndpc.gov.ng/wp-content/uploads/2024/03/Nigeria_Data_Protection_Act_2023.pdf
- **Proposed statutory reasoning:** The record does not establish whether an actor operates in Nigeria or the data subject is in Nigeria.
- **Review flag:** PENDING_REVIEW — FLAGGED: [CONCEPTUAL_OVERLAP] Missing actor, processing, or data-subject location follows the same uncertainty structure as NG-EVAL-004; confirm this is not a superficial transformation.

#### NG-TRN-I-06 — TRAIN

- **Factual scenario:** A cloud backup service restores a named person's files from an unspecified regional server, without identifying where the provider operates or where the person is located.
- **Question:** Which closed label describes whether Nigeria Data Protection Act 2023 applies on these facts?
- **Proposed label:** `INSUFFICIENT_INFORMATION`
- **Statutory provision:** Nigeria Data Protection Act 2023, section 2(1)-(2)
- **Source URL:** https://ndpc.gov.ng/wp-content/uploads/2024/03/Nigeria_Data_Protection_Act_2023.pdf
- **Proposed statutory reasoning:** Section 2 requires territorial facts that the scenario omits.
- **Review flag:** PENDING_REVIEW — FLAGGED: [CONCEPTUAL_OVERLAP] Missing actor, processing, or data-subject location follows the same uncertainty structure as NG-EVAL-004; confirm this is not a superficial transformation.

#### NG-TRN-I-07 — TRAIN

- **Factual scenario:** A diaspora association compiles a membership directory, but the facts do not say where the association operates, where members are situated, or where compilation occurs.
- **Question:** Which closed label describes whether Nigeria Data Protection Act 2023 applies on these facts?
- **Proposed label:** `INSUFFICIENT_INFORMATION`
- **Statutory provision:** Nigeria Data Protection Act 2023, section 2(1)-(2)
- **Source URL:** https://ndpc.gov.ng/wp-content/uploads/2024/03/Nigeria_Data_Protection_Act_2023.pdf
- **Proposed statutory reasoning:** The available facts cannot select any section 2 territorial limb.
- **Review flag:** PENDING_REVIEW — FLAGGED: [CONCEPTUAL_OVERLAP] Missing actor, processing, or data-subject location follows the same uncertainty structure as NG-EVAL-004; confirm this is not a superficial transformation.

#### NG-TRN-I-08 — TRAIN

- **Factual scenario:** A mobile network analyses roaming records for a subscriber during an international trip, but the itinerary, operator residence, and analytics location are withheld.
- **Question:** Which closed label describes whether Nigeria Data Protection Act 2023 applies on these facts?
- **Proposed label:** `INSUFFICIENT_INFORMATION`
- **Statutory provision:** Nigeria Data Protection Act 2023, section 2(1)-(2)
- **Source URL:** https://ndpc.gov.ng/wp-content/uploads/2024/03/Nigeria_Data_Protection_Act_2023.pdf
- **Proposed statutory reasoning:** The relevant Nigerian territorial connections remain unknown.
- **Review flag:** PENDING_REVIEW — FLAGGED: [CONCEPTUAL_OVERLAP] Missing actor, processing, or data-subject location follows the same uncertainty structure as NG-EVAL-004; confirm this is not a superficial transformation.

#### NG-VAL-I-09 — VALIDATION

- **Factual scenario:** A research consortium pseudonymises participant records somewhere in Africa, but the participating institutions and subjects are not geographically identified.
- **Question:** Which closed label describes whether Nigeria Data Protection Act 2023 applies on these facts?
- **Proposed label:** `INSUFFICIENT_INFORMATION`
- **Statutory provision:** Nigeria Data Protection Act 2023, section 2(1)-(2)
- **Source URL:** https://ndpc.gov.ng/wp-content/uploads/2024/03/Nigeria_Data_Protection_Act_2023.pdf
- **Proposed statutory reasoning:** Pseudonymisation does not supply the missing territorial facts required by section 2.
- **Review flag:** PENDING_REVIEW — FLAGGED: [LEGAL_AMBIGUITY] Pseudonymised information remains personal data when re-identification is possible; the scenario omits whether the consortium retains or can access identifying information. [CONCEPTUAL_OVERLAP] Missing actor, processing, or data-subject location follows the same uncertainty structure as NG-EVAL-004; confirm this is not a superficial transformation.

#### NG-VAL-I-10 — VALIDATION

- **Factual scenario:** An online marketplace investigates a named seller's account from an undisclosed office; the seller's current country and the marketplace's operating locations are not provided.
- **Question:** Which closed label describes whether Nigeria Data Protection Act 2023 applies on these facts?
- **Proposed label:** `INSUFFICIENT_INFORMATION`
- **Statutory provision:** Nigeria Data Protection Act 2023, section 2(1)-(2)
- **Source URL:** https://ndpc.gov.ng/wp-content/uploads/2024/03/Nigeria_Data_Protection_Act_2023.pdf
- **Proposed statutory reasoning:** The record lacks facts needed to determine a Nigerian actor, processing, or data-subject connection.
- **Review flag:** PENDING_REVIEW — FLAGGED: [CONCEPTUAL_OVERLAP] Missing actor, processing, or data-subject location follows the same uncertainty structure as NG-EVAL-004; confirm this is not a superficial transformation.

## Kenya

### APPLIES

#### KE-TRN-A-01 — TRAIN

- **Factual scenario:** A Mombasa ferry operator automatically records named passengers' ticket and boarding data in an electronic manifest while operating in Kenya.
- **Question:** Which closed label describes whether Kenya Data Protection Act 2019 applies on these facts?
- **Proposed label:** `APPLIES`
- **Statutory provision:** Kenya Data Protection Act 2019, section 4(a)-(b)
- **Source URL:** https://new.kenyalaw.org/akn/ke/act/2019/24/eng%402022-12-31/source
- **Proposed statutory reasoning:** Section 4 covers recorded automated processing by a controller established and processing in Kenya.
- **Review flag:** PENDING_REVIEW — no specific drafting defect identified; substantive legal review still required.

#### KE-TRN-A-02 — TRAIN

- **Factual scenario:** A Canadian safari-booking service automatically stores passport and dietary details for travellers located in Kenya during their booked tours.
- **Question:** Which closed label describes whether Kenya Data Protection Act 2019 applies on these facts?
- **Proposed label:** `APPLIES`
- **Statutory provision:** Kenya Data Protection Act 2019, section 4(a)-(b)
- **Source URL:** https://new.kenyalaw.org/akn/ke/act/2019/24/eng%402022-12-31/source
- **Proposed statutory reasoning:** The records are processed automatically for data subjects located in Kenya by a controller outside Kenya, satisfying section 4.
- **Review flag:** PENDING_REVIEW — no specific drafting defect identified; substantive legal review still required.

#### KE-TRN-A-03 — TRAIN

- **Factual scenario:** A Kisumu hospital keeps alphabetised paper patient folders as part of its clinical filing system and updates them by hand in Kenya.
- **Question:** Which closed label describes whether Kenya Data Protection Act 2019 applies on these facts?
- **Proposed label:** `APPLIES`
- **Statutory provision:** Kenya Data Protection Act 2019, section 4(a)-(b)
- **Source URL:** https://new.kenyalaw.org/akn/ke/act/2019/24/eng%402022-12-31/source
- **Proposed statutory reasoning:** Section 4 includes non-automated recorded data forming part of a filing system and processing by a Kenyan establishment.
- **Review flag:** PENDING_REVIEW — no specific drafting defect identified; substantive legal review still required.

#### KE-TRN-A-04 — TRAIN

- **Factual scenario:** An Indian agronomy platform automatically records farm coordinates and farmer names from users located in Nakuru County.
- **Question:** Which closed label describes whether Kenya Data Protection Act 2019 applies on these facts?
- **Proposed label:** `APPLIES`
- **Statutory provision:** Kenya Data Protection Act 2019, section 4(a)-(b)
- **Source URL:** https://new.kenyalaw.org/akn/ke/act/2019/24/eng%402022-12-31/source
- **Proposed statutory reasoning:** Automated records about data subjects located in Kenya bring the foreign controller within section 4.
- **Review flag:** PENDING_REVIEW — no specific drafting defect identified; substantive legal review still required.

#### KE-TRN-A-05 — TRAIN

- **Factual scenario:** A processor ordinarily resident in Kenya scans and indexes pension forms for a Tanzanian fund at its Eldoret premises.
- **Question:** Which closed label describes whether Kenya Data Protection Act 2019 applies on these facts?
- **Proposed label:** `APPLIES`
- **Statutory provision:** Kenya Data Protection Act 2019, section 4(a)-(b)
- **Source URL:** https://new.kenyalaw.org/akn/ke/act/2019/24/eng%402022-12-31/source
- **Proposed statutory reasoning:** The processor is ordinarily resident in Kenya, processes there, and creates automated records covered by section 4.
- **Review flag:** PENDING_REVIEW — no specific drafting defect identified; substantive legal review still required.

#### KE-TRN-A-06 — TRAIN

- **Factual scenario:** A German language-testing company automatically records voice samples and identity documents from candidates taking examinations in Nairobi.
- **Question:** Which closed label describes whether Kenya Data Protection Act 2019 applies on these facts?
- **Proposed label:** `APPLIES`
- **Statutory provision:** Kenya Data Protection Act 2019, section 4(a)-(b)
- **Source URL:** https://new.kenyalaw.org/akn/ke/act/2019/24/eng%402022-12-31/source
- **Proposed statutory reasoning:** The foreign controller processes recorded personal data of data subjects located in Kenya.
- **Review flag:** PENDING_REVIEW — no specific drafting defect identified; substantive legal review still required.

#### KE-TRN-A-07 — TRAIN

- **Factual scenario:** A Kenyan wildlife conservancy maintains a structured paper register of named volunteers and emergency contacts at its Laikipia office.
- **Question:** Which closed label describes whether Kenya Data Protection Act 2019 applies on these facts?
- **Proposed label:** `APPLIES`
- **Statutory provision:** Kenya Data Protection Act 2019, section 4(a)-(b)
- **Source URL:** https://new.kenyalaw.org/akn/ke/act/2019/24/eng%402022-12-31/source
- **Proposed statutory reasoning:** The non-automated records form part of a filing system and are processed by a controller established in Kenya.
- **Review flag:** PENDING_REVIEW — no specific drafting defect identified; substantive legal review still required.

#### KE-TRN-A-08 — TRAIN

- **Factual scenario:** A Singapore recruitment portal stores electronic résumés submitted by applicants located in Kenya for jobs in Asia.
- **Question:** Which closed label describes whether Kenya Data Protection Act 2019 applies on these facts?
- **Proposed label:** `APPLIES`
- **Statutory provision:** Kenya Data Protection Act 2019, section 4(a)-(b)
- **Source URL:** https://new.kenyalaw.org/akn/ke/act/2019/24/eng%402022-12-31/source
- **Proposed statutory reasoning:** The portal automatically processes recorded personal data of data subjects located in Kenya.
- **Review flag:** PENDING_REVIEW — FLAGGED: [DATA_QUALITY] The scenario contains replacement characters in “résumés”; correct the source encoding before review or export.

#### KE-VAL-A-09 — VALIDATION

- **Factual scenario:** A Nairobi laboratory automatically analyses coded samples while retaining a lookup table connecting each code to a named Kenyan patient.
- **Question:** Which closed label describes whether Kenya Data Protection Act 2019 applies on these facts?
- **Proposed label:** `APPLIES`
- **Statutory provision:** Kenya Data Protection Act 2019, section 4(a)-(b)
- **Source URL:** https://new.kenyalaw.org/akn/ke/act/2019/24/eng%402022-12-31/source
- **Proposed statutory reasoning:** The retained link makes the records personal data processed automatically by a Kenyan establishment.
- **Review flag:** PENDING_REVIEW — no specific drafting defect identified; substantive legal review still required.

#### KE-VAL-A-10 — VALIDATION

- **Factual scenario:** A Ugandan bus company automatically records mobile numbers and seat selections from passengers while they are located at its Kenyan departure terminals.
- **Question:** Which closed label describes whether Kenya Data Protection Act 2019 applies on these facts?
- **Proposed label:** `APPLIES`
- **Statutory provision:** Kenya Data Protection Act 2019, section 4(a)-(b)
- **Source URL:** https://new.kenyalaw.org/akn/ke/act/2019/24/eng%402022-12-31/source
- **Proposed statutory reasoning:** Recorded automated processing concerns data subjects located in Kenya, meeting section 4's scope conditions.
- **Review flag:** PENDING_REVIEW — no specific drafting defect identified; substantive legal review still required.

### DOES_NOT_APPLY

#### KE-TRN-N-01 — TRAIN

- **Factual scenario:** A Kenyan shopkeeper has an unrecorded face-to-face conversation about a customer's preferred colour and creates no electronic, written, audio, or filing-system record.
- **Question:** Which closed label describes whether Kenya Data Protection Act 2019 applies on these facts?
- **Proposed label:** `DOES_NOT_APPLY`
- **Statutory provision:** Kenya Data Protection Act 2019, section 4(a)-(b)
- **Source URL:** https://new.kenyalaw.org/akn/ke/act/2019/24/eng%402022-12-31/source
- **Proposed statutory reasoning:** Section 4(a) is not met because no personal data is entered in a record or processed as part of a filing system.
- **Review flag:** PENDING_REVIEW — no specific drafting defect identified; substantive legal review still required.

#### KE-TRN-N-02 — TRAIN

- **Factual scenario:** A Kenyan tour guide remembers a visitor's first name without writing, recording, entering, or otherwise processing it in any record.
- **Question:** Which closed label describes whether Kenya Data Protection Act 2019 applies on these facts?
- **Proposed label:** `DOES_NOT_APPLY`
- **Statutory provision:** Kenya Data Protection Act 2019, section 4(a)-(b)
- **Source URL:** https://new.kenyalaw.org/akn/ke/act/2019/24/eng%402022-12-31/source
- **Proposed statutory reasoning:** The stated activity lacks the recorded processing required by section 4(a).
- **Review flag:** PENDING_REVIEW — no specific drafting defect identified; substantive legal review still required.

#### KE-TRN-N-03 — TRAIN

- **Factual scenario:** A bakery in Portugal automatically stores customer accounts only for people located in Portugal, processes them there, and is neither established nor ordinarily resident in Kenya.
- **Question:** Which closed label describes whether Kenya Data Protection Act 2019 applies on these facts?
- **Proposed label:** `DOES_NOT_APPLY`
- **Statutory provision:** Kenya Data Protection Act 2019, section 4(a)-(b)
- **Source URL:** https://new.kenyalaw.org/akn/ke/act/2019/24/eng%402022-12-31/source
- **Proposed statutory reasoning:** The record condition is met, but neither territorial limb in section 4(b) is present.
- **Review flag:** PENDING_REVIEW — FLAGGED: [CONCEPTUAL_OVERLAP] Foreign-only negative pattern is conceptually close to KE-EVAL-003; factual nouns change while the scope logic remains nearly identical.

#### KE-TRN-N-04 — TRAIN

- **Factual scenario:** A Korean employer keeps structured personnel files only for workers in Seoul, performs all processing there, and has no Kenyan establishment or ordinary residence.
- **Question:** Which closed label describes whether Kenya Data Protection Act 2019 applies on these facts?
- **Proposed label:** `DOES_NOT_APPLY`
- **Statutory provision:** Kenya Data Protection Act 2019, section 4(a)-(b)
- **Source URL:** https://new.kenyalaw.org/akn/ke/act/2019/24/eng%402022-12-31/source
- **Proposed statutory reasoning:** The processing has no connection to Kenya under section 4(b).
- **Review flag:** PENDING_REVIEW — FLAGGED: [CONCEPTUAL_OVERLAP] Foreign-only negative pattern is conceptually close to KE-EVAL-003; factual nouns change while the scope logic remains nearly identical.

#### KE-TRN-N-05 — TRAIN

- **Factual scenario:** Loose handwritten reminders about unnamed neighbours are discarded by a Kenyan resident and never organised or intended to form part of a filing system.
- **Question:** Which closed label describes whether Kenya Data Protection Act 2019 applies on these facts?
- **Proposed label:** `DOES_NOT_APPLY`
- **Statutory provision:** Kenya Data Protection Act 2019, section 4(a)-(b)
- **Source URL:** https://new.kenyalaw.org/akn/ke/act/2019/24/eng%402022-12-31/source
- **Proposed statutory reasoning:** Non-automated material outside a filing system does not satisfy section 4(a).
- **Review flag:** PENDING_REVIEW — no specific drafting defect identified; substantive legal review still required.

#### KE-TRN-N-06 — TRAIN

- **Factual scenario:** A Canadian sports club automatically records only Canadian members in Toronto and has no Kenyan establishment, residence, processing, or data subjects.
- **Question:** Which closed label describes whether Kenya Data Protection Act 2019 applies on these facts?
- **Proposed label:** `DOES_NOT_APPLY`
- **Statutory provision:** Kenya Data Protection Act 2019, section 4(a)-(b)
- **Source URL:** https://new.kenyalaw.org/akn/ke/act/2019/24/eng%402022-12-31/source
- **Proposed statutory reasoning:** Although automated records exist, section 4(b)'s territorial requirements are absent.
- **Review flag:** PENDING_REVIEW — FLAGGED: [CONCEPTUAL_OVERLAP] Foreign-only negative pattern is conceptually close to KE-EVAL-003; factual nouns change while the scope logic remains nearly identical.

#### KE-TRN-N-07 — TRAIN

- **Factual scenario:** A Moroccan dentist keeps structured patient records solely for patients in Rabat, with all processing in Morocco and no Kenyan establishment or ordinary residence.
- **Question:** Which closed label describes whether Kenya Data Protection Act 2019 applies on these facts?
- **Proposed label:** `DOES_NOT_APPLY`
- **Statutory provision:** Kenya Data Protection Act 2019, section 4(a)-(b)
- **Source URL:** https://new.kenyalaw.org/akn/ke/act/2019/24/eng%402022-12-31/source
- **Proposed statutory reasoning:** The facts negate both section 4(b) territorial alternatives.
- **Review flag:** PENDING_REVIEW — FLAGGED: [CONCEPTUAL_OVERLAP] Foreign-only negative pattern is conceptually close to KE-EVAL-003; factual nouns change while the scope logic remains nearly identical.

#### KE-TRN-N-08 — TRAIN

- **Factual scenario:** A person in Kenya silently recognises an acquaintance in a crowd but makes no record and uses no automated system.
- **Question:** Which closed label describes whether Kenya Data Protection Act 2019 applies on these facts?
- **Proposed label:** `DOES_NOT_APPLY`
- **Statutory provision:** Kenya Data Protection Act 2019, section 4(a)-(b)
- **Source URL:** https://new.kenyalaw.org/akn/ke/act/2019/24/eng%402022-12-31/source
- **Proposed statutory reasoning:** Mere unrecorded recognition is outside the recorded-processing condition in section 4(a).
- **Review flag:** PENDING_REVIEW — no specific drafting defect identified; substantive legal review still required.

#### KE-VAL-N-09 — VALIDATION

- **Factual scenario:** An Icelandic publisher automatically manages subscriber details only for readers located in Iceland and has no Kenyan operations, establishment, residence, or processing.
- **Question:** Which closed label describes whether Kenya Data Protection Act 2019 applies on these facts?
- **Proposed label:** `DOES_NOT_APPLY`
- **Statutory provision:** Kenya Data Protection Act 2019, section 4(a)-(b)
- **Source URL:** https://new.kenyalaw.org/akn/ke/act/2019/24/eng%402022-12-31/source
- **Proposed statutory reasoning:** The processing is recorded but lacks a section 4(b) Kenyan nexus.
- **Review flag:** PENDING_REVIEW — FLAGGED: [CONCEPTUAL_OVERLAP] Foreign-only negative pattern is conceptually close to KE-EVAL-003; factual nouns change while the scope logic remains nearly identical.

#### KE-VAL-N-10 — VALIDATION

- **Factual scenario:** A Brazilian warehouse files named worker records at its São Paulo facility only; every worker and processing operation is in Brazil and the controller has no Kenyan connection.
- **Question:** Which closed label describes whether Kenya Data Protection Act 2019 applies on these facts?
- **Proposed label:** `DOES_NOT_APPLY`
- **Statutory provision:** Kenya Data Protection Act 2019, section 4(a)-(b)
- **Source URL:** https://new.kenyalaw.org/akn/ke/act/2019/24/eng%402022-12-31/source
- **Proposed statutory reasoning:** Neither establishment or residence in Kenya nor processing of data subjects located there is present.
- **Review flag:** PENDING_REVIEW — FLAGGED: [DATA_QUALITY] The scenario contains a replacement character in “São Paulo”; correct the source encoding before review or export. [TERRITORIAL_ROUTE] “No Kenyan connection” is conclusory and does not separately negate establishment or ordinary residence under section 4(b). [CONCEPTUAL_OVERLAP] Foreign-only negative pattern is conceptually close to KE-EVAL-003; factual nouns change while the scope logic remains nearly identical.

### INSUFFICIENT_INFORMATION

#### KE-TRN-I-01 — TRAIN

- **Factual scenario:** A counsellor takes handwritten notes about a client, but it is unknown whether the notes are organised into or intended for a filing system and neither person's location is given.
- **Question:** Which closed label describes whether Kenya Data Protection Act 2019 applies on these facts?
- **Proposed label:** `INSUFFICIENT_INFORMATION`
- **Statutory provision:** Kenya Data Protection Act 2019, section 4(a)-(b)
- **Source URL:** https://new.kenyalaw.org/akn/ke/act/2019/24/eng%402022-12-31/source
- **Proposed statutory reasoning:** Both the non-automated filing-system condition and the territorial facts required by section 4 remain unresolved.
- **Review flag:** PENDING_REVIEW — FLAGGED: [CONCEPTUAL_OVERLAP] Missing record/filing-system and territorial facts follow the same uncertainty structure as KE-EVAL-004; confirm independent factual design.

#### KE-TRN-I-02 — TRAIN

- **Factual scenario:** A voice assistant temporarily handles a person's request, but the facts do not say whether any personal data is recorded or where the person is located.
- **Question:** Which closed label describes whether Kenya Data Protection Act 2019 applies on these facts?
- **Proposed label:** `INSUFFICIENT_INFORMATION`
- **Statutory provision:** Kenya Data Protection Act 2019, section 4(a)-(b)
- **Source URL:** https://new.kenyalaw.org/akn/ke/act/2019/24/eng%402022-12-31/source
- **Proposed statutory reasoning:** Section 4 cannot be applied without knowing whether a record exists and whether Kenya is territorially connected.
- **Review flag:** PENDING_REVIEW — FLAGGED: [LEGAL_AMBIGUITY] Temporary voice-assistant handling may itself involve automated recording or processing; clarify what is captured in memory and whether it is entered in a record. [CONCEPTUAL_OVERLAP] Missing record/filing-system and territorial facts follow the same uncertainty structure as KE-EVAL-004; confirm independent factual design.

#### KE-TRN-I-03 — TRAIN

- **Factual scenario:** A paper index of donors is found at a regional office, but its filing structure, the office country, and the donors' locations are unknown.
- **Question:** Which closed label describes whether Kenya Data Protection Act 2019 applies on these facts?
- **Proposed label:** `INSUFFICIENT_INFORMATION`
- **Statutory provision:** Kenya Data Protection Act 2019, section 4(a)-(b)
- **Source URL:** https://new.kenyalaw.org/akn/ke/act/2019/24/eng%402022-12-31/source
- **Proposed statutory reasoning:** The record does not establish either the filing-system or territorial elements of section 4.
- **Review flag:** PENDING_REVIEW — FLAGGED: [CONCEPTUAL_OVERLAP] Missing record/filing-system and territorial facts follow the same uncertainty structure as KE-EVAL-004; confirm independent factual design.

#### KE-TRN-I-04 — TRAIN

- **Factual scenario:** A foreign application displays a user's profile during a trip, but it is unclear whether the profile is stored, whether the user is in Kenya, or where the provider is established.
- **Question:** Which closed label describes whether Kenya Data Protection Act 2019 applies on these facts?
- **Proposed label:** `INSUFFICIENT_INFORMATION`
- **Statutory provision:** Kenya Data Protection Act 2019, section 4(a)-(b)
- **Source URL:** https://new.kenyalaw.org/akn/ke/act/2019/24/eng%402022-12-31/source
- **Proposed statutory reasoning:** Material and territorial scope facts under section 4 are missing.
- **Review flag:** PENDING_REVIEW — FLAGGED: [CONCEPTUAL_OVERLAP] Missing record/filing-system and territorial facts follow the same uncertainty structure as KE-EVAL-004; confirm independent factual design.

#### KE-TRN-I-05 — TRAIN

- **Factual scenario:** A business sorts customer cards by an undisclosed method at an unidentified branch, and the customers' countries are not stated.
- **Question:** Which closed label describes whether Kenya Data Protection Act 2019 applies on these facts?
- **Proposed label:** `INSUFFICIENT_INFORMATION`
- **Statutory provision:** Kenya Data Protection Act 2019, section 4(a)-(b)
- **Source URL:** https://new.kenyalaw.org/akn/ke/act/2019/24/eng%402022-12-31/source
- **Proposed statutory reasoning:** The scenario does not show whether the cards form a filing system or whether section 4(b) connects the processing to Kenya.
- **Review flag:** PENDING_REVIEW — FLAGGED: [CONCEPTUAL_OVERLAP] Missing record/filing-system and territorial facts follow the same uncertainty structure as KE-EVAL-004; confirm independent factual design.

#### KE-TRN-I-06 — TRAIN

- **Factual scenario:** A wearable device computes a reading in memory, but the evidence does not establish whether it is retained as a record or where the wearer and controller are located.
- **Question:** Which closed label describes whether Kenya Data Protection Act 2019 applies on these facts?
- **Proposed label:** `INSUFFICIENT_INFORMATION`
- **Statutory provision:** Kenya Data Protection Act 2019, section 4(a)-(b)
- **Source URL:** https://new.kenyalaw.org/akn/ke/act/2019/24/eng%402022-12-31/source
- **Proposed statutory reasoning:** The recorded-processing and territorial requirements cannot be determined.
- **Review flag:** PENDING_REVIEW — FLAGGED: [CONCEPTUAL_OVERLAP] Missing record/filing-system and territorial facts follow the same uncertainty structure as KE-EVAL-004; confirm independent factual design.

#### KE-TRN-I-07 — TRAIN

- **Factual scenario:** A school employee recalls pupil allergies while planning lunch, but it is unknown whether the information came from or is entered into a structured record and the school's country is omitted.
- **Question:** Which closed label describes whether Kenya Data Protection Act 2019 applies on these facts?
- **Proposed label:** `INSUFFICIENT_INFORMATION`
- **Statutory provision:** Kenya Data Protection Act 2019, section 4(a)-(b)
- **Source URL:** https://new.kenyalaw.org/akn/ke/act/2019/24/eng%402022-12-31/source
- **Proposed statutory reasoning:** The facts leave both section 4(a) and section 4(b) uncertain.
- **Review flag:** PENDING_REVIEW — FLAGGED: [LEGAL_AMBIGUITY] The described act is human recollection. Unless a structured record is actually consulted or updated, the facts may support DOES_NOT_APPLY rather than uncertainty. [CONCEPTUAL_OVERLAP] Missing record/filing-system and territorial facts follow the same uncertainty structure as KE-EVAL-004; confirm independent factual design.

#### KE-TRN-I-08 — TRAIN

- **Factual scenario:** A regional call centre writes callers' names on forms, but the forms' organisation, the call-centre country, and callers' locations are not disclosed.
- **Question:** Which closed label describes whether Kenya Data Protection Act 2019 applies on these facts?
- **Proposed label:** `INSUFFICIENT_INFORMATION`
- **Statutory provision:** Kenya Data Protection Act 2019, section 4(a)-(b)
- **Source URL:** https://new.kenyalaw.org/akn/ke/act/2019/24/eng%402022-12-31/source
- **Proposed statutory reasoning:** The filing-system and territorial elements required by section 4 are unresolved.
- **Review flag:** PENDING_REVIEW — FLAGGED: [CONCEPTUAL_OVERLAP] Missing record/filing-system and territorial facts follow the same uncertainty structure as KE-EVAL-004; confirm independent factual design.

#### KE-VAL-I-09 — VALIDATION

- **Factual scenario:** A camera system detects a face and immediately discards the image, but the technical logs, system operator location, and person's location are unknown.
- **Question:** Which closed label describes whether Kenya Data Protection Act 2019 applies on these facts?
- **Proposed label:** `INSUFFICIENT_INFORMATION`
- **Statutory provision:** Kenya Data Protection Act 2019, section 4(a)-(b)
- **Source URL:** https://new.kenyalaw.org/akn/ke/act/2019/24/eng%402022-12-31/source
- **Proposed statutory reasoning:** It is unclear whether recorded personal data exists and whether either territorial limb applies.
- **Review flag:** PENDING_REVIEW — FLAGGED: [LEGAL_AMBIGUITY] Automated facial detection may process a digital image even if it is immediately discarded; clarify whether the transient image or logs constitute a record under section 4(a). [CONCEPTUAL_OVERLAP] Missing record/filing-system and territorial facts follow the same uncertainty structure as KE-EVAL-004; confirm independent factual design.

#### KE-VAL-I-10 — VALIDATION

- **Factual scenario:** An archive contains labelled envelopes about individuals, but no facts show how they are indexed, who processes them, or whether anyone is located in Kenya.
- **Question:** Which closed label describes whether Kenya Data Protection Act 2019 applies on these facts?
- **Proposed label:** `INSUFFICIENT_INFORMATION`
- **Statutory provision:** Kenya Data Protection Act 2019, section 4(a)-(b)
- **Source URL:** https://new.kenyalaw.org/akn/ke/act/2019/24/eng%402022-12-31/source
- **Proposed statutory reasoning:** The scenario lacks facts about a filing system and Kenya-related territorial scope.
- **Review flag:** PENDING_REVIEW — FLAGGED: [CONCEPTUAL_OVERLAP] Missing record/filing-system and territorial facts follow the same uncertainty structure as KE-EVAL-004; confirm independent factual design.

## European Union

### APPLIES

#### EU-TRN-A-01 — TRAIN

- **Factual scenario:** A retailer's Belgian branch designs a loyalty campaign and processes participant profiles through a database hosted in Morocco.
- **Question:** Which closed label describes whether General Data Protection Regulation (GDPR) applies on these facts?
- **Proposed label:** `APPLIES`
- **Statutory provision:** GDPR, Article 3(1)-(3)
- **Source URL:** https://eur-lex.europa.eu/eli/reg/2016/679/oj
- **Proposed statutory reasoning:** Article 3(1) applies because processing occurs in the context of an EU establishment, irrespective of server location.
- **Review flag:** PENDING_REVIEW — no specific drafting defect identified; substantive legal review still required.

#### EU-TRN-A-02 — TRAIN

- **Factual scenario:** A Turkish streaming service has no EU establishment but markets a French-language subscription specifically to viewers who are in Belgium and records their viewing accounts.
- **Question:** Which closed label describes whether General Data Protection Regulation (GDPR) applies on these facts?
- **Proposed label:** `APPLIES`
- **Statutory provision:** GDPR, Article 3(1)-(3)
- **Source URL:** https://eur-lex.europa.eu/eli/reg/2016/679/oj
- **Proposed statutory reasoning:** The processing relates to offering services to data subjects in the Union under Article 3(2)(a).
- **Review flag:** PENDING_REVIEW — no specific drafting defect identified; substantive legal review still required.

#### EU-TRN-A-03 — TRAIN

- **Factual scenario:** A Canadian advertising network with no EU office builds movement profiles from mobile devices while their users travel within Italy.
- **Question:** Which closed label describes whether General Data Protection Regulation (GDPR) applies on these facts?
- **Proposed label:** `APPLIES`
- **Statutory provision:** GDPR, Article 3(1)-(3)
- **Source URL:** https://eur-lex.europa.eu/eli/reg/2016/679/oj
- **Proposed statutory reasoning:** Tracking behaviour taking place in the Union is monitoring within Article 3(2)(b).
- **Review flag:** PENDING_REVIEW — no specific drafting defect identified; substantive legal review still required.

#### EU-TRN-A-04 — TRAIN

- **Factual scenario:** A processor's Polish establishment handles identity verification for its Australian controller, with the verification performed in India as part of the Polish office's client service.
- **Question:** Which closed label describes whether General Data Protection Regulation (GDPR) applies on these facts?
- **Proposed label:** `APPLIES`
- **Statutory provision:** GDPR, Article 3(1)-(3)
- **Source URL:** https://eur-lex.europa.eu/eli/reg/2016/679/oj
- **Proposed statutory reasoning:** Article 3(1) turns on processing in the context of the EU establishment, not the physical processing location.
- **Review flag:** PENDING_REVIEW — no specific drafting defect identified; substantive legal review still required.

#### EU-TRN-A-05 — TRAIN

- **Factual scenario:** A Brazilian examination provider offers remote certification specifically to candidates who are in Portugal and processes their identification and test recordings.
- **Question:** Which closed label describes whether General Data Protection Regulation (GDPR) applies on these facts?
- **Proposed label:** `APPLIES`
- **Statutory provision:** GDPR, Article 3(1)-(3)
- **Source URL:** https://eur-lex.europa.eu/eli/reg/2016/679/oj
- **Proposed statutory reasoning:** The targeted service to people in the Union engages Article 3(2)(a).
- **Review flag:** PENDING_REVIEW — no specific drafting defect identified; substantive legal review still required.

#### EU-TRN-A-06 — TRAIN

- **Factual scenario:** A Japanese analytics company without an EU establishment follows browsing paths of people while they use websites in Austria to predict their preferences.
- **Question:** Which closed label describes whether General Data Protection Regulation (GDPR) applies on these facts?
- **Proposed label:** `APPLIES`
- **Statutory provision:** GDPR, Article 3(1)-(3)
- **Source URL:** https://eur-lex.europa.eu/eli/reg/2016/679/oj
- **Proposed statutory reasoning:** The activity monitors behaviour taking place within the Union under Article 3(2)(b).
- **Review flag:** PENDING_REVIEW — no specific drafting defect identified; substantive legal review still required.

#### EU-TRN-A-07 — TRAIN

- **Factual scenario:** A controller operates a branch in the Netherlands that manages employee recruitment records, while its headquarters and servers remain in South Africa.
- **Question:** Which closed label describes whether General Data Protection Regulation (GDPR) applies on these facts?
- **Proposed label:** `APPLIES`
- **Statutory provision:** GDPR, Article 3(1)-(3)
- **Source URL:** https://eur-lex.europa.eu/eli/reg/2016/679/oj
- **Proposed statutory reasoning:** Recruitment processing in the context of the Dutch establishment falls within Article 3(1).
- **Review flag:** PENDING_REVIEW — no specific drafting defect identified; substantive legal review still required.

#### EU-TRN-A-08 — TRAIN

- **Factual scenario:** A United States language tutor with no EU establishment buys advertisements directed only at residents currently in Greece and enrols them in paid online lessons.
- **Question:** Which closed label describes whether General Data Protection Regulation (GDPR) applies on these facts?
- **Proposed label:** `APPLIES`
- **Statutory provision:** GDPR, Article 3(1)-(3)
- **Source URL:** https://eur-lex.europa.eu/eli/reg/2016/679/oj
- **Proposed statutory reasoning:** Offering paid services to data subjects in the Union satisfies Article 3(2)(a).
- **Review flag:** PENDING_REVIEW — no specific drafting defect identified; substantive legal review still required.

#### EU-VAL-A-09 — VALIDATION

- **Factual scenario:** An Argentine fitness platform with no EU office continuously analyses running routes while subscribers exercise in Denmark.
- **Question:** Which closed label describes whether General Data Protection Regulation (GDPR) applies on these facts?
- **Proposed label:** `APPLIES`
- **Statutory provision:** GDPR, Article 3(1)-(3)
- **Source URL:** https://eur-lex.europa.eu/eli/reg/2016/679/oj
- **Proposed statutory reasoning:** Systematic analysis of behaviour in Denmark is monitoring within Article 3(2)(b).
- **Review flag:** PENDING_REVIEW — no specific drafting defect identified; substantive legal review still required.

#### EU-VAL-A-10 — VALIDATION

- **Factual scenario:** A controller based outside the Union processes consular appointment data at premises where Spanish law applies by virtue of public international law.
- **Question:** Which closed label describes whether General Data Protection Regulation (GDPR) applies on these facts?
- **Proposed label:** `APPLIES`
- **Statutory provision:** GDPR, Article 3(1)-(3)
- **Source URL:** https://eur-lex.europa.eu/eli/reg/2016/679/oj
- **Proposed statutory reasoning:** Article 3(3) supplies territorial scope where Member State law applies by virtue of public international law.
- **Review flag:** PENDING_REVIEW — FLAGGED: [LEGAL_AMBIGUITY] The scenario stipulates the Article 3(3) legal conclusion (“Spanish law applies”) rather than facts establishing why public international law produces that result.

### DOES_NOT_APPLY

#### EU-TRN-N-01 — TRAIN

- **Factual scenario:** A South African grocer serves only shoppers in Cape Town, has no EU establishment, offering, or monitoring, and is not in a place governed by Member State law under public international law.
- **Question:** Which closed label describes whether General Data Protection Regulation (GDPR) applies on these facts?
- **Proposed label:** `DOES_NOT_APPLY`
- **Statutory provision:** GDPR, Article 3(1)-(3)
- **Source URL:** https://eur-lex.europa.eu/eli/reg/2016/679/oj
- **Proposed statutory reasoning:** The facts negate every territorial connection in Article 3(1)-(3).
- **Review flag:** PENDING_REVIEW — FLAGGED: [CONCEPTUAL_OVERLAP] Complete Article 3 negation is conceptually close to EU-EVAL-004 and repeatedly uses statutory/legal shorthand that may cue the label.

#### EU-TRN-N-02 — TRAIN

- **Factual scenario:** A Japanese rail operator processes only domestic commuter cards in Japan, has no Union establishment, does not target or monitor anyone in the Union, and has no Article 3(3) connection.
- **Question:** Which closed label describes whether General Data Protection Regulation (GDPR) applies on these facts?
- **Proposed label:** `DOES_NOT_APPLY`
- **Statutory provision:** GDPR, Article 3(1)-(3)
- **Source URL:** https://eur-lex.europa.eu/eli/reg/2016/679/oj
- **Proposed statutory reasoning:** None of Article 3's establishment, targeting, monitoring, or public-international-law grounds is present.
- **Review flag:** PENDING_REVIEW — FLAGGED: [CONCEPTUAL_OVERLAP] Complete Article 3 negation is conceptually close to EU-EVAL-004 and repeatedly uses statutory/legal shorthand that may cue the label.

#### EU-TRN-N-03 — TRAIN

- **Factual scenario:** A Canadian neighbourhood newspaper manages only local print subscribers, with no EU establishment, Union-directed offering, Union behaviour monitoring, or public-international-law nexus.
- **Question:** Which closed label describes whether General Data Protection Regulation (GDPR) applies on these facts?
- **Proposed label:** `DOES_NOT_APPLY`
- **Statutory provision:** GDPR, Article 3(1)-(3)
- **Source URL:** https://eur-lex.europa.eu/eli/reg/2016/679/oj
- **Proposed statutory reasoning:** The stated activity is outside all Article 3 territorial grounds.
- **Review flag:** PENDING_REVIEW — FLAGGED: [CONCEPTUAL_OVERLAP] Complete Article 3 negation is conceptually close to EU-EVAL-004 and repeatedly uses statutory/legal shorthand that may cue the label.

#### EU-TRN-N-04 — TRAIN

- **Factual scenario:** A Bolivian clinic treats only patients in La Paz and processes records there, with no EU establishment, Union targeting or monitoring, or place subject to Member State law.
- **Question:** Which closed label describes whether General Data Protection Regulation (GDPR) applies on these facts?
- **Proposed label:** `DOES_NOT_APPLY`
- **Statutory provision:** GDPR, Article 3(1)-(3)
- **Source URL:** https://eur-lex.europa.eu/eli/reg/2016/679/oj
- **Proposed statutory reasoning:** Article 3(1)-(3) is affirmatively excluded on the facts.
- **Review flag:** PENDING_REVIEW — FLAGGED: [CONCEPTUAL_OVERLAP] Complete Article 3 negation is conceptually close to EU-EVAL-004 and repeatedly uses statutory/legal shorthand that may cue the label.

#### EU-TRN-N-05 — TRAIN

- **Factual scenario:** An Indonesian cinema operates only in Jakarta and profiles only local patrons, without an EU establishment, EU-directed service, EU monitoring, or Article 3(3) connection.
- **Question:** Which closed label describes whether General Data Protection Regulation (GDPR) applies on these facts?
- **Proposed label:** `DOES_NOT_APPLY`
- **Statutory provision:** GDPR, Article 3(1)-(3)
- **Source URL:** https://eur-lex.europa.eu/eli/reg/2016/679/oj
- **Proposed statutory reasoning:** No Article 3 territorial criterion is satisfied.
- **Review flag:** PENDING_REVIEW — FLAGGED: [CONCEPTUAL_OVERLAP] Complete Article 3 negation is conceptually close to EU-EVAL-004 and repeatedly uses statutory/legal shorthand that may cue the label.

#### EU-TRN-N-06 — TRAIN

- **Factual scenario:** A Kenyan cooperative records only members in Kenya and neither establishes itself in the Union nor offers to or monitors people there; Member State law does not apply to its location.
- **Question:** Which closed label describes whether General Data Protection Regulation (GDPR) applies on these facts?
- **Proposed label:** `DOES_NOT_APPLY`
- **Statutory provision:** GDPR, Article 3(1)-(3)
- **Source URL:** https://eur-lex.europa.eu/eli/reg/2016/679/oj
- **Proposed statutory reasoning:** The processing lacks every territorial link specified by Article 3.
- **Review flag:** PENDING_REVIEW — FLAGGED: [CONCEPTUAL_OVERLAP] Complete Article 3 negation is conceptually close to EU-EVAL-004 and repeatedly uses statutory/legal shorthand that may cue the label.

#### EU-TRN-N-07 — TRAIN

- **Factual scenario:** A New Zealand sports league processes only local player registrations, has no Union establishment or targeting or monitoring in the Union, and has no public-international-law connection.
- **Question:** Which closed label describes whether General Data Protection Regulation (GDPR) applies on these facts?
- **Proposed label:** `DOES_NOT_APPLY`
- **Statutory provision:** GDPR, Article 3(1)-(3)
- **Source URL:** https://eur-lex.europa.eu/eli/reg/2016/679/oj
- **Proposed statutory reasoning:** The facts exclude Article 3(1), 3(2), and 3(3).
- **Review flag:** PENDING_REVIEW — FLAGGED: [CONCEPTUAL_OVERLAP] Complete Article 3 negation is conceptually close to EU-EVAL-004 and repeatedly uses statutory/legal shorthand that may cue the label.

#### EU-TRN-N-08 — TRAIN

- **Factual scenario:** A Colombian utility bills customers only in Bogotá, without an EU establishment, Union offering, Union behaviour monitoring, or location where Member State law applies.
- **Question:** Which closed label describes whether General Data Protection Regulation (GDPR) applies on these facts?
- **Proposed label:** `DOES_NOT_APPLY`
- **Statutory provision:** GDPR, Article 3(1)-(3)
- **Source URL:** https://eur-lex.europa.eu/eli/reg/2016/679/oj
- **Proposed statutory reasoning:** No territorial basis under Article 3 is present.
- **Review flag:** PENDING_REVIEW — FLAGGED: [DATA_QUALITY] The scenario contains a replacement character in “Bogotá”; correct the source encoding before review or export. [CONCEPTUAL_OVERLAP] Complete Article 3 negation is conceptually close to EU-EVAL-004 and repeatedly uses statutory/legal shorthand that may cue the label.

#### EU-VAL-N-09 — VALIDATION

- **Factual scenario:** A Philippine university manages only students studying in Manila and has no EU establishment, Union-directed services, Union monitoring, or Article 3(3) nexus.
- **Question:** Which closed label describes whether General Data Protection Regulation (GDPR) applies on these facts?
- **Proposed label:** `DOES_NOT_APPLY`
- **Statutory provision:** GDPR, Article 3(1)-(3)
- **Source URL:** https://eur-lex.europa.eu/eli/reg/2016/679/oj
- **Proposed statutory reasoning:** The scenario expressly negates the complete Article 3 test.
- **Review flag:** PENDING_REVIEW — FLAGGED: [CONCEPTUAL_OVERLAP] Complete Article 3 negation is conceptually close to EU-EVAL-004 and repeatedly uses statutory/legal shorthand that may cue the label.

#### EU-VAL-N-10 — VALIDATION

- **Factual scenario:** A Tunisian taxi company tracks only journeys occurring in Tunis, with no EU establishment or Union market activity and no place governed by Member State law under international law.
- **Question:** Which closed label describes whether General Data Protection Regulation (GDPR) applies on these facts?
- **Proposed label:** `DOES_NOT_APPLY`
- **Statutory provision:** GDPR, Article 3(1)-(3)
- **Source URL:** https://eur-lex.europa.eu/eli/reg/2016/679/oj
- **Proposed statutory reasoning:** The processing is outside Article 3(1)-(3) on the stated facts.
- **Review flag:** PENDING_REVIEW — FLAGGED: [CONCEPTUAL_OVERLAP] Complete Article 3 negation is conceptually close to EU-EVAL-004 and repeatedly uses statutory/legal shorthand that may cue the label.

### INSUFFICIENT_INFORMATION

#### EU-TRN-I-01 — TRAIN

- **Factual scenario:** A multinational's Caribbean office processes recruitment profiles for an unnamed European affiliate, but the facts do not show whether the processing is in the context of that affiliate's activities.
- **Question:** Which closed label describes whether General Data Protection Regulation (GDPR) applies on these facts?
- **Proposed label:** `INSUFFICIENT_INFORMATION`
- **Statutory provision:** GDPR, Article 3(1)-(3)
- **Source URL:** https://eur-lex.europa.eu/eli/reg/2016/679/oj
- **Proposed statutory reasoning:** Article 3(1) depends on the relationship between processing and an EU establishment, which is not supplied.
- **Review flag:** PENDING_REVIEW — no specific drafting defect identified; substantive legal review still required.

#### EU-TRN-I-02 — TRAIN

- **Factual scenario:** A Korean game is downloaded by people somewhere in Europe, but its marketing materials and the users' locations at the time of the offering are not available.
- **Question:** Which closed label describes whether General Data Protection Regulation (GDPR) applies on these facts?
- **Proposed label:** `INSUFFICIENT_INFORMATION`
- **Statutory provision:** GDPR, Article 3(1)-(3)
- **Source URL:** https://eur-lex.europa.eu/eli/reg/2016/679/oj
- **Proposed statutory reasoning:** Article 3(2)(a) cannot be resolved without evidence of an offering directed to data subjects in the Union.
- **Review flag:** PENDING_REVIEW — FLAGGED: [CONCEPTUAL_OVERLAP] Unknown Union location, offering, or monitoring is conceptually close to EU-EVAL-005; confirm the factual pattern is sufficiently independent.

#### EU-TRN-I-03 — TRAIN

- **Factual scenario:** A mapping company analyses device coordinates, but the evidence does not establish whether tracked behaviour takes place inside the Union or merely concerns past travel there.
- **Question:** Which closed label describes whether General Data Protection Regulation (GDPR) applies on these facts?
- **Proposed label:** `INSUFFICIENT_INFORMATION`
- **Statutory provision:** GDPR, Article 3(1)-(3)
- **Source URL:** https://eur-lex.europa.eu/eli/reg/2016/679/oj
- **Proposed statutory reasoning:** Article 3(2)(b) requires monitoring of behaviour taking place in the Union.
- **Review flag:** PENDING_REVIEW — FLAGGED: [CONCEPTUAL_OVERLAP] Unknown Union location, offering, or monitoring is conceptually close to EU-EVAL-005; confirm the factual pattern is sufficiently independent.

#### EU-TRN-I-04 — TRAIN

- **Factual scenario:** A controller works from premises outside the Union described only as having a special diplomatic status, without identifying which state's law applies there.
- **Question:** Which closed label describes whether General Data Protection Regulation (GDPR) applies on these facts?
- **Proposed label:** `INSUFFICIENT_INFORMATION`
- **Statutory provision:** GDPR, Article 3(1)-(3)
- **Source URL:** https://eur-lex.europa.eu/eli/reg/2016/679/oj
- **Proposed statutory reasoning:** Article 3(3) cannot be assessed without the public-international-law territorial connection.
- **Review flag:** PENDING_REVIEW — FLAGGED: [DATA_QUALITY] The missing_facts field is malformed as one array element per character instead of one complete missing-fact string.

#### EU-TRN-I-05 — TRAIN

- **Factual scenario:** A website accepts euros and displays several languages, but the record does not show where users are located or whether the design intentionally targets people in the Union.
- **Question:** Which closed label describes whether General Data Protection Regulation (GDPR) applies on these facts?
- **Proposed label:** `INSUFFICIENT_INFORMATION`
- **Statutory provision:** GDPR, Article 3(1)-(3)
- **Source URL:** https://eur-lex.europa.eu/eli/reg/2016/679/oj
- **Proposed statutory reasoning:** Currency and language may be relevant but do not alone establish Article 3(2)(a) on these incomplete facts.
- **Review flag:** PENDING_REVIEW — FLAGGED: [CONCEPTUAL_OVERLAP] Unknown Union location, offering, or monitoring is conceptually close to EU-EVAL-005; confirm the factual pattern is sufficiently independent.

#### EU-TRN-I-06 — TRAIN

- **Factual scenario:** An overseas parent receives employee analytics from an office described only as European, without identifying whether that office is in the Union or how its activities relate to the processing.
- **Question:** Which closed label describes whether General Data Protection Regulation (GDPR) applies on these facts?
- **Proposed label:** `INSUFFICIENT_INFORMATION`
- **Statutory provision:** GDPR, Article 3(1)-(3)
- **Source URL:** https://eur-lex.europa.eu/eli/reg/2016/679/oj
- **Proposed statutory reasoning:** The establishment and contextual-activity elements of Article 3(1) are unresolved.
- **Review flag:** PENDING_REVIEW — no specific drafting defect identified; substantive legal review still required.

#### EU-TRN-I-07 — TRAIN

- **Factual scenario:** An application assigns advertising segments to travellers during a cross-border train journey, but no evidence identifies whether the monitored portion occurs inside or outside the Union.
- **Question:** Which closed label describes whether General Data Protection Regulation (GDPR) applies on these facts?
- **Proposed label:** `INSUFFICIENT_INFORMATION`
- **Statutory provision:** GDPR, Article 3(1)-(3)
- **Source URL:** https://eur-lex.europa.eu/eli/reg/2016/679/oj
- **Proposed statutory reasoning:** Article 3(2)(b) turns on where the monitored behaviour takes place.
- **Review flag:** PENDING_REVIEW — FLAGGED: [CONCEPTUAL_OVERLAP] Unknown Union location, offering, or monitoring is conceptually close to EU-EVAL-005; confirm the factual pattern is sufficiently independent.

#### EU-TRN-I-08 — TRAIN

- **Factual scenario:** A remote consultancy receives enquiries from unidentified countries, but no evidence shows whether it directs services to people in the Union or merely responds to unsolicited contact.
- **Question:** Which closed label describes whether General Data Protection Regulation (GDPR) applies on these facts?
- **Proposed label:** `INSUFFICIENT_INFORMATION`
- **Statutory provision:** GDPR, Article 3(1)-(3)
- **Source URL:** https://eur-lex.europa.eu/eli/reg/2016/679/oj
- **Proposed statutory reasoning:** The intentional offering element under Article 3(2)(a) remains uncertain.
- **Review flag:** PENDING_REVIEW — FLAGGED: [CONCEPTUAL_OVERLAP] Unknown Union location, offering, or monitoring is conceptually close to EU-EVAL-005; confirm the factual pattern is sufficiently independent.

#### EU-VAL-I-09 — VALIDATION

- **Factual scenario:** A processor has staff in an unnamed island territory and handles customer records abroad, but the territory's legal status and the relationship to any EU establishment are unknown.
- **Question:** Which closed label describes whether General Data Protection Regulation (GDPR) applies on these facts?
- **Proposed label:** `INSUFFICIENT_INFORMATION`
- **Statutory provision:** GDPR, Article 3(1)-(3)
- **Source URL:** https://eur-lex.europa.eu/eli/reg/2016/679/oj
- **Proposed statutory reasoning:** Neither Article 3(1) nor Article 3(3) can be determined from the territorial description.
- **Review flag:** PENDING_REVIEW — no specific drafting defect identified; substantive legal review still required.

#### EU-VAL-I-10 — VALIDATION

- **Factual scenario:** A behavioural-risk system scores internet activity from multiple continents, but logs do not reveal whether any scored behaviour occurs in the Union or where the controller is established.
- **Question:** Which closed label describes whether General Data Protection Regulation (GDPR) applies on these facts?
- **Proposed label:** `INSUFFICIENT_INFORMATION`
- **Statutory provision:** GDPR, Article 3(1)-(3)
- **Source URL:** https://eur-lex.europa.eu/eli/reg/2016/679/oj
- **Proposed statutory reasoning:** The establishment and Union-behaviour facts needed under Article 3 are missing.
- **Review flag:** PENDING_REVIEW — FLAGGED: [CONCEPTUAL_OVERLAP] Unknown Union location, offering, or monitoring is conceptually close to EU-EVAL-005; confirm the factual pattern is sufficiently independent.
