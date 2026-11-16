"""Generate synthetic review candidates and protected-set audit artifacts."""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from geolegal.training_data import (  # noqa: E402
    Candidate,
    dataset_manifest,
    leakage_report,
    protected_registry,
    validate_candidates,
    write_jsonl,
)

SOURCES = {
    "NIGERIA": {
        "framework": "Nigeria Data Protection Act 2023",
        "basis": ("Nigeria Data Protection Act 2023, section 2(1)-(2)",),
        "url": "https://ndpc.gov.ng/wp-content/uploads/2024/03/Nigeria_Data_Protection_Act_2023.pdf",
        "date": "2023-06-12",
        "prefix": "NG",
    },
    "KENYA": {
        "framework": "Kenya Data Protection Act 2019",
        "basis": ("Kenya Data Protection Act 2019, section 4(a)-(b)",),
        "url": "https://new.kenyalaw.org/akn/ke/act/2019/24/eng%402022-12-31/source",
        "date": "2022-12-31",
        "prefix": "KE",
    },
    "EU": {
        "framework": "General Data Protection Regulation (GDPR)",
        "basis": ("GDPR, Article 3(1)-(3)",),
        "url": "https://eur-lex.europa.eu/eli/reg/2016/679/oj",
        "date": "2016-04-27",
        "prefix": "EU",
    },
}

# Each tuple is (scenario, statutory explanation, missing facts). These are drafts,
# not legal conclusions, until a human legal reviewer changes review_status.
CATALOG: dict[str, dict[str, list[tuple[str, str, tuple[str, ...]]]]] = {
    "NIGERIA": {
        "APPLIES": [
            ("A Nigerian airline operating from Port Harcourt stores passenger contact and passport data on servers in Iceland for flights it manages from Nigeria.", "Section 2 is engaged because the controller operates in Nigeria and processes personal data, regardless of the offshore server location.", ()),
            ("A Japanese athletics platform collects heart-rate and identity data from competitors while they attend a tournament in Lagos, although the platform has no Nigerian office.", "Section 2 extends to an overseas controller processing personal data of data subjects in Nigeria.", ()),
            ("A records contractor working from Kano digitises employee files for a Ghanaian corporate client and uploads the resulting database to Accra.", "The processor operates and performs processing in Nigeria, supplying territorial connections under section 2.", ()),
            ("A United States telemedicine provider schedules video consultations specifically for patients physically present in Abuja and records their symptoms and contact details.", "The overseas provider processes personal data of data subjects in Nigeria, bringing the activity within section 2.", ()),
            ("A Nigerian university's Enugu admissions office scores applications from students throughout West Africa using a cloud service hosted in Singapore.", "The controller operates in Nigeria and the processing activity occurs through its Nigerian office.", ()),
            ("A freight company domiciled in Nigeria tracks its drivers in Benin and Togo using vehicle identifiers linked to named employees.", "The controller's Nigerian domicile is a sufficient section 2 connection even though tracking occurs abroad.", ()),
            ("A South African conference organiser scans attendee badges and stores dietary information during a three-day event in Calabar.", "The processing occurs in Nigeria and concerns identifiable attendees, engaging section 2.", ()),
            ("A payroll processor resident in Nigeria calculates salaries for remote workers employed by a company in Rwanda.", "Section 2 applies because the processor is resident in Nigeria while processing personal data.", ()),
            ("A Brazilian travel application obtains precise location data from tourists while they travel through Osun State, with no office in Nigeria.", "The controller processes personal data of individuals while they are in Nigeria, a connection addressed by section 2(2)(c).", ()),
            ("A charity operating a field office in Maiduguri enters beneficiary names and household details into a database administered from London.", "The charity operates in Nigeria and processes personal data through that operation, notwithstanding foreign administration.", ()),
        ],
        "DOES_NOT_APPLY": [
            ("A Chilean vineyard with no Nigerian domicile, residence, operations, customers, staff, or infrastructure records only the details of visitors physically in Chile; no processing occurs in Nigeria.", "None of the controller, processing-location, or data-subject-in-Nigeria connections in section 2 is present.", ()),
            ("A municipal library in Finland catalogues borrowing histories only for patrons in Finland, using systems located there, and has no Nigerian activity or establishment.", "The stated processing has no territorial connection described in section 2.", ()),
            ("A New Zealand farm records local employees' shift times entirely in New Zealand and neither the employer nor the workers have any Nigerian operational connection.", "The controller, processing, and affected data subjects are all outside Nigeria on the stated facts.", ()),
            ("A Peruvian clinic treats and records only patients located in Peru, stores the files in Lima, and neither operates nor is domiciled or resident in Nigeria.", "No section 2 territorial limb is satisfied by the stated facts.", ()),
            ("A Norwegian theatre keeps an Oslo-only membership list for local patrons and conducts no business, data collection, or processing in Nigeria.", "The scenario expressly excludes the Nigerian connections listed in section 2.", ()),
            ("A Thai manufacturer processes factory access logs solely for workers at its Bangkok site and has no Nigerian entity, operation, processor, or data subjects.", "The processing lacks a Nigerian controller, processor, location, or data-subject connection.", ()),
            ("An Argentine museum photographs ticket holders only at its Buenos Aires entrance, stores the images locally, and has no presence or processing activity in Nigeria.", "The facts negate each territorial basis in section 2.", ()),
            ("A Swiss hiking club maintains emergency contacts solely for members located in Switzerland and neither the club nor its service provider operates from Nigeria.", "No stated actor, processing operation, or data subject is connected to Nigeria under section 2.", ()),
            ("A Malaysian school processes attendance information only for pupils in Kuala Lumpur on Malaysian systems and has no Nigerian domicile, residence, or operation.", "The stated activity falls outside all section 2 territorial connectors.", ()),
            ("A Mexican repair shop keeps customer telephone numbers solely for jobs performed in Guadalajara, with no Nigerian customers, staff, systems, or processing.", "The facts affirmatively exclude the territorial circumstances specified in section 2.", ()),
        ],
        "INSUFFICIENT_INFORMATION": [
            ("A satellite communications company analyses subscriber identifiers aboard a vessel, but the record does not identify where the vessel, subscribers, controller, or processing equipment are located.", "Section 2 applicability cannot be resolved without a Nigerian connection through an actor, processing location, or data subject.", ("Controller or processor domicile, residence, or operations", "Processing location", "Data-subject location")),
            ("A global hotel group centralises guest profiles, but it is unclear whether its unnamed West African branch is in Nigeria or whether Nigerian guests are included.", "The facts do not establish any of the alternative section 2 territorial links.", ("Branch location", "Whether data subjects are in Nigeria", "Where processing occurs")),
            ("A wearable-device vendor receives emergency telemetry from a traveller whose country at the time of collection is not recorded; the vendor's operating locations are also unstated.", "The data-subject and controller locations needed for section 2 are missing.", ("Traveller's location during collection", "Vendor domicile, residence, and operations", "Processing location")),
            ("A regional payment switch processes cardholder names at an undisclosed data centre for banks in several unnamed countries.", "Neither the actors nor the processing or data-subject locations are sufficiently specified for section 2.", ("Data-centre location", "Actor locations", "Cardholder locations")),
            ("An employer uses a remote background-check vendor for a worker described only as being in West Africa, and neither organisation's place of operation is given.", "The record does not establish whether an actor operates in Nigeria or the data subject is in Nigeria.", ("Worker location", "Employer and vendor operations", "Processing location")),
            ("A cloud backup service restores a named person's files from an unspecified regional server, without identifying where the provider operates or where the person is located.", "Section 2 requires territorial facts that the scenario omits.", ("Provider domicile, residence, or operations", "Server and processing location", "Data-subject location")),
            ("A diaspora association compiles a membership directory, but the facts do not say where the association operates, where members are situated, or where compilation occurs.", "The available facts cannot select any section 2 territorial limb.", ("Association operations", "Member locations", "Processing location")),
            ("A mobile network analyses roaming records for a subscriber during an international trip, but the itinerary, operator residence, and analytics location are withheld.", "The relevant Nigerian territorial connections remain unknown.", ("Subscriber location", "Operator residence or operations", "Analytics location")),
            ("A research consortium pseudonymises participant records somewhere in Africa, but the participating institutions and subjects are not geographically identified.", "Pseudonymisation does not supply the missing territorial facts required by section 2.", ("Institution locations", "Participant locations", "Processing location")),
            ("An online marketplace investigates a named seller's account from an undisclosed office; the seller's current country and the marketplace's operating locations are not provided.", "The record lacks facts needed to determine a Nigerian actor, processing, or data-subject connection.", ("Marketplace operations", "Investigation location", "Seller location")),
        ],
    },
    "KENYA": {
        "APPLIES": [
            ("A Mombasa ferry operator automatically records named passengers' ticket and boarding data in an electronic manifest while operating in Kenya.", "Section 4 covers recorded automated processing by a controller established and processing in Kenya.", ()),
            ("A Canadian safari-booking service automatically stores passport and dietary details for travellers located in Kenya during their booked tours.", "The records are processed automatically for data subjects located in Kenya by a controller outside Kenya, satisfying section 4.", ()),
            ("A Kisumu hospital keeps alphabetised paper patient folders as part of its clinical filing system and updates them by hand in Kenya.", "Section 4 includes non-automated recorded data forming part of a filing system and processing by a Kenyan establishment.", ()),
            ("An Indian agronomy platform automatically records farm coordinates and farmer names from users located in Nakuru County.", "Automated records about data subjects located in Kenya bring the foreign controller within section 4.", ()),
            ("A processor ordinarily resident in Kenya scans and indexes pension forms for a Tanzanian fund at its Eldoret premises.", "The processor is ordinarily resident in Kenya, processes there, and creates automated records covered by section 4.", ()),
            ("A German language-testing company automatically records voice samples and identity documents from candidates taking examinations in Nairobi.", "The foreign controller processes recorded personal data of data subjects located in Kenya.", ()),
            ("A Kenyan wildlife conservancy maintains a structured paper register of named volunteers and emergency contacts at its Laikipia office.", "The non-automated records form part of a filing system and are processed by a controller established in Kenya.", ()),
            ("A Singapore recruitment portal stores electronic résumés submitted by applicants located in Kenya for jobs in Asia.", "The portal automatically processes recorded personal data of data subjects located in Kenya.", ()),
            ("A Nairobi laboratory automatically analyses coded samples while retaining a lookup table connecting each code to a named Kenyan patient.", "The retained link makes the records personal data processed automatically by a Kenyan establishment.", ()),
            ("A Ugandan bus company automatically records mobile numbers and seat selections from passengers while they are located at its Kenyan departure terminals.", "Recorded automated processing concerns data subjects located in Kenya, meeting section 4's scope conditions.", ()),
        ],
        "DOES_NOT_APPLY": [
            ("A Kenyan shopkeeper has an unrecorded face-to-face conversation about a customer's preferred colour and creates no electronic, written, audio, or filing-system record.", "Section 4(a) is not met because no personal data is entered in a record or processed as part of a filing system.", ()),
            ("A Kenyan tour guide remembers a visitor's first name without writing, recording, entering, or otherwise processing it in any record.", "The stated activity lacks the recorded processing required by section 4(a).", ()),
            ("A bakery in Portugal automatically stores customer accounts only for people located in Portugal, processes them there, and is neither established nor ordinarily resident in Kenya.", "The record condition is met, but neither territorial limb in section 4(b) is present.", ()),
            ("A Korean employer keeps structured personnel files only for workers in Seoul, performs all processing there, and has no Kenyan establishment or ordinary residence.", "The processing has no connection to Kenya under section 4(b).", ()),
            ("Loose handwritten reminders about unnamed neighbours are discarded by a Kenyan resident and never organised or intended to form part of a filing system.", "Non-automated material outside a filing system does not satisfy section 4(a).", ()),
            ("A Canadian sports club automatically records only Canadian members in Toronto and has no Kenyan establishment, residence, processing, or data subjects.", "Although automated records exist, section 4(b)'s territorial requirements are absent.", ()),
            ("A Moroccan dentist keeps structured patient records solely for patients in Rabat, with all processing in Morocco and no Kenyan establishment or ordinary residence.", "The facts negate both section 4(b) territorial alternatives.", ()),
            ("A person in Kenya silently recognises an acquaintance in a crowd but makes no record and uses no automated system.", "Mere unrecorded recognition is outside the recorded-processing condition in section 4(a).", ()),
            ("An Icelandic publisher automatically manages subscriber details only for readers located in Iceland and has no Kenyan operations, establishment, residence, or processing.", "The processing is recorded but lacks a section 4(b) Kenyan nexus.", ()),
            ("A Brazilian warehouse files named worker records at its São Paulo facility only; every worker and processing operation is in Brazil and the controller has no Kenyan connection.", "Neither establishment or residence in Kenya nor processing of data subjects located there is present.", ()),
        ],
        "INSUFFICIENT_INFORMATION": [
            ("A counsellor takes handwritten notes about a client, but it is unknown whether the notes are organised into or intended for a filing system and neither person's location is given.", "Both the non-automated filing-system condition and the territorial facts required by section 4 remain unresolved.", ("Whether notes form part of a filing system", "Controller location", "Data-subject location")),
            ("A voice assistant temporarily handles a person's request, but the facts do not say whether any personal data is recorded or where the person is located.", "Section 4 cannot be applied without knowing whether a record exists and whether Kenya is territorially connected.", ("Whether personal data is entered in a record", "Data-subject location", "Provider establishment or residence")),
            ("A paper index of donors is found at a regional office, but its filing structure, the office country, and the donors' locations are unknown.", "The record does not establish either the filing-system or territorial elements of section 4.", ("Whether the index forms a filing system", "Office location", "Donor locations")),
            ("A foreign application displays a user's profile during a trip, but it is unclear whether the profile is stored, whether the user is in Kenya, or where the provider is established.", "Material and territorial scope facts under section 4 are missing.", ("Whether data is recorded", "User location", "Provider establishment")),
            ("A business sorts customer cards by an undisclosed method at an unidentified branch, and the customers' countries are not stated.", "The scenario does not show whether the cards form a filing system or whether section 4(b) connects the processing to Kenya.", ("Filing-system structure", "Branch location", "Customer locations")),
            ("A wearable device computes a reading in memory, but the evidence does not establish whether it is retained as a record or where the wearer and controller are located.", "The recorded-processing and territorial requirements cannot be determined.", ("Record retention", "Wearer location", "Controller establishment or residence")),
            ("A school employee recalls pupil allergies while planning lunch, but it is unknown whether the information came from or is entered into a structured record and the school's country is omitted.", "The facts leave both section 4(a) and section 4(b) uncertain.", ("Existence of a record or filing system", "School location", "Pupil locations")),
            ("A regional call centre writes callers' names on forms, but the forms' organisation, the call-centre country, and callers' locations are not disclosed.", "The filing-system and territorial elements required by section 4 are unresolved.", ("Whether forms constitute a filing system", "Call-centre location", "Caller locations")),
            ("A camera system detects a face and immediately discards the image, but the technical logs, system operator location, and person's location are unknown.", "It is unclear whether recorded personal data exists and whether either territorial limb applies.", ("Whether any personal record is created", "Operator establishment", "Person location")),
            ("An archive contains labelled envelopes about individuals, but no facts show how they are indexed, who processes them, or whether anyone is located in Kenya.", "The scenario lacks facts about a filing system and Kenya-related territorial scope.", ("Archive organisation", "Controller or processor location", "Data-subject locations")),
        ],
    },
    "EU": {
        "APPLIES": [
            ("A retailer's Belgian branch designs a loyalty campaign and processes participant profiles through a database hosted in Morocco.", "Article 3(1) applies because processing occurs in the context of an EU establishment, irrespective of server location.", ()),
            ("A Turkish streaming service has no EU establishment but markets a French-language subscription specifically to viewers who are in Belgium and records their viewing accounts.", "The processing relates to offering services to data subjects in the Union under Article 3(2)(a).", ()),
            ("A Canadian advertising network with no EU office builds movement profiles from mobile devices while their users travel within Italy.", "Tracking behaviour taking place in the Union is monitoring within Article 3(2)(b).", ()),
            ("A processor's Polish establishment handles identity verification for its Australian controller, with the verification performed in India as part of the Polish office's client service.", "Article 3(1) turns on processing in the context of the EU establishment, not the physical processing location.", ()),
            ("A Brazilian examination provider offers remote certification specifically to candidates who are in Portugal and processes their identification and test recordings.", "The targeted service to people in the Union engages Article 3(2)(a).", ()),
            ("A Japanese analytics company without an EU establishment follows browsing paths of people while they use websites in Austria to predict their preferences.", "The activity monitors behaviour taking place within the Union under Article 3(2)(b).", ()),
            ("A controller operates a branch in the Netherlands that manages employee recruitment records, while its headquarters and servers remain in South Africa.", "Recruitment processing in the context of the Dutch establishment falls within Article 3(1).", ()),
            ("A United States language tutor with no EU establishment buys advertisements directed only at residents currently in Greece and enrols them in paid online lessons.", "Offering paid services to data subjects in the Union satisfies Article 3(2)(a).", ()),
            ("An Argentine fitness platform with no EU office continuously analyses running routes while subscribers exercise in Denmark.", "Systematic analysis of behaviour in Denmark is monitoring within Article 3(2)(b).", ()),
            ("A controller based outside the Union processes consular appointment data at premises where Spanish law applies by virtue of public international law.", "Article 3(3) supplies territorial scope where Member State law applies by virtue of public international law.", ()),
        ],
        "DOES_NOT_APPLY": [
            ("A South African grocer serves only shoppers in Cape Town, has no EU establishment, offering, or monitoring, and is not in a place governed by Member State law under public international law.", "The facts negate every territorial connection in Article 3(1)-(3).", ()),
            ("A Japanese rail operator processes only domestic commuter cards in Japan, has no Union establishment, does not target or monitor anyone in the Union, and has no Article 3(3) connection.", "None of Article 3's establishment, targeting, monitoring, or public-international-law grounds is present.", ()),
            ("A Canadian neighbourhood newspaper manages only local print subscribers, with no EU establishment, Union-directed offering, Union behaviour monitoring, or public-international-law nexus.", "The stated activity is outside all Article 3 territorial grounds.", ()),
            ("A Bolivian clinic treats only patients in La Paz and processes records there, with no EU establishment, Union targeting or monitoring, or place subject to Member State law.", "Article 3(1)-(3) is affirmatively excluded on the facts.", ()),
            ("An Indonesian cinema operates only in Jakarta and profiles only local patrons, without an EU establishment, EU-directed service, EU monitoring, or Article 3(3) connection.", "No Article 3 territorial criterion is satisfied.", ()),
            ("A Kenyan cooperative records only members in Kenya and neither establishes itself in the Union nor offers to or monitors people there; Member State law does not apply to its location.", "The processing lacks every territorial link specified by Article 3.", ()),
            ("A New Zealand sports league processes only local player registrations, has no Union establishment or targeting or monitoring in the Union, and has no public-international-law connection.", "The facts exclude Article 3(1), 3(2), and 3(3).", ()),
            ("A Colombian utility bills customers only in Bogotá, without an EU establishment, Union offering, Union behaviour monitoring, or location where Member State law applies.", "No territorial basis under Article 3 is present.", ()),
            ("A Philippine university manages only students studying in Manila and has no EU establishment, Union-directed services, Union monitoring, or Article 3(3) nexus.", "The scenario expressly negates the complete Article 3 test.", ()),
            ("A Tunisian taxi company tracks only journeys occurring in Tunis, with no EU establishment or Union market activity and no place governed by Member State law under international law.", "The processing is outside Article 3(1)-(3) on the stated facts.", ()),
        ],
        "INSUFFICIENT_INFORMATION": [
            ("A multinational's Caribbean office processes recruitment profiles for an unnamed European affiliate, but the facts do not show whether the processing is in the context of that affiliate's activities.", "Article 3(1) depends on the relationship between processing and an EU establishment, which is not supplied.", ("Identity and location of the affiliate", "Connection between processing and the affiliate's activities")),
            ("A Korean game is downloaded by people somewhere in Europe, but its marketing materials and the users' locations at the time of the offering are not available.", "Article 3(2)(a) cannot be resolved without evidence of an offering directed to data subjects in the Union.", ("Whether users were in the Union", "Evidence of intentional Union-directed offering")),
            ("A mapping company analyses device coordinates, but the evidence does not establish whether tracked behaviour takes place inside the Union or merely concerns past travel there.", "Article 3(2)(b) requires monitoring of behaviour taking place in the Union.", ("Location of behaviour during monitoring", "Nature of the tracking activity")),
            ("A controller works from premises outside the Union described only as having a special diplomatic status, without identifying which state's law applies there.", "Article 3(3) cannot be assessed without the public-international-law territorial connection.", ("Whether Member State law applies by public international law")),
            ("A website accepts euros and displays several languages, but the record does not show where users are located or whether the design intentionally targets people in the Union.", "Currency and language may be relevant but do not alone establish Article 3(2)(a) on these incomplete facts.", ("Data-subject location", "Evidence of intention to offer goods or services in the Union")),
            ("An overseas parent receives employee analytics from an office described only as European, without identifying whether that office is in the Union or how its activities relate to the processing.", "The establishment and contextual-activity elements of Article 3(1) are unresolved.", ("Whether the office is an EU establishment", "Connection between its activities and processing")),
            ("An application assigns advertising segments to travellers during a cross-border train journey, but no evidence identifies whether the monitored portion occurs inside or outside the Union.", "Article 3(2)(b) turns on where the monitored behaviour takes place.", ("Location of the monitored behaviour",)),
            ("A remote consultancy receives enquiries from unidentified countries, but no evidence shows whether it directs services to people in the Union or merely responds to unsolicited contact.", "The intentional offering element under Article 3(2)(a) remains uncertain.", ("Locations of prospective clients", "Evidence of Union-directed offering")),
            ("A processor has staff in an unnamed island territory and handles customer records abroad, but the territory's legal status and the relationship to any EU establishment are unknown.", "Neither Article 3(1) nor Article 3(3) can be determined from the territorial description.", ("Territory and applicable law", "Existence of an EU establishment", "Context of processing")),
            ("A behavioural-risk system scores internet activity from multiple continents, but logs do not reveal whether any scored behaviour occurs in the Union or where the controller is established.", "The establishment and Union-behaviour facts needed under Article 3 are missing.", ("Controller establishment", "Whether monitored behaviour occurs in the Union")),
        ],
    },
}


def build_candidates() -> list[Candidate]:
    candidates: list[Candidate] = []
    for jurisdiction, labels in CATALOG.items():
        source = SOURCES[jurisdiction]
        for label, rows in labels.items():
            if len(rows) != 10:
                raise ValueError(f"{jurisdiction}/{label} must contain ten candidates")
            for index, (scenario, explanation, missing_facts) in enumerate(rows, 1):
                split = "TRAIN" if index <= 8 else "VALIDATION"
                split_code = "TRN" if split == "TRAIN" else "VAL"
                label_code = {"APPLIES": "A", "DOES_NOT_APPLY": "N", "INSUFFICIENT_INFORMATION": "I"}[label]
                candidate_id = f"{source['prefix']}-{split_code}-{label_code}-{index:02d}"
                candidates.append(
                    Candidate(
                        candidate_id=candidate_id,
                        scenario_family_id=f"family::{candidate_id}",
                        split=split,
                        jurisdiction=jurisdiction,
                        legal_framework=source["framework"],
                        scenario=scenario,
                        question=f"Which closed label describes whether {source['framework']} applies on these facts?",
                        expected_label=label,
                        statutory_basis=source["basis"],
                        source_url=source["url"],
                        source_version_date=source["date"],
                        statutory_explanation=explanation,
                        missing_facts=missing_facts,
                    )
                )
    validate_candidates(candidates)
    return candidates


def main() -> None:
    registry = protected_registry(REPO_ROOT)
    candidates = build_candidates()
    candidate_path = REPO_ROOT / "data/train/candidates_v1.jsonl"
    registry_path = REPO_ROOT / "data/eval/protected_held_out_registry_v1.json"
    report_path = REPO_ROOT / "data/train/leakage_report_v1.json"
    manifest_path = REPO_ROOT / "data/train/candidate_manifest_v1.json"

    write_jsonl(candidate_path, [record.to_dict() for record in candidates])
    report = leakage_report(candidates, registry)
    registry_path.write_text(json.dumps(registry, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    report_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    manifest = dataset_manifest(candidates, candidate_path.relative_to(REPO_ROOT), report)
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print(json.dumps({"records": len(candidates), "manifest": manifest, "leakage": {k: report[k] for k in ("blocking_issue_count", "id_overlaps", "family_overlaps", "normalized_exact_matches", "flagged_near_matches")}}, indent=2))


if __name__ == "__main__":
    main()
