"""Render the candidate dataset as a substantive legal-review draft."""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATASET = ROOT / "data/train/candidates_v1.jsonl"
OUTPUT = ROOT / "TRAINING_DATA_LEGAL_REVIEW.md"

JURISDICTIONS = ("NIGERIA", "KENYA", "EU")
LABELS = ("APPLIES", "DOES_NOT_APPLY", "INSUFFICIENT_INFORMATION")

NEGATIVE_ROUTE_OMISSIONS = {
    "NG-TRN-N-02": "The facts say no Nigerian activity or establishment, but do not expressly negate domicile or residence using the section 2 terms.",
    "NG-TRN-N-03": "“No Nigerian operational connection” is vague and does not separately negate domicile, residence, and operation.",
    "NG-TRN-N-05": "No Nigerian business or processing is stated, but Nigerian domicile and residence are not expressly negated.",
    "NG-TRN-N-06": "No Nigerian entity or operation is stated, but domicile and residence are not expressly negated.",
    "NG-TRN-N-08": "The club and provider do not operate from Nigeria, but their domicile and residence are not expressly negated.",
    "NG-VAL-N-10": "No Nigerian customers, staff, systems, or processing are stated, but controller domicile, residence, and operation are not expressly negated.",
    "KE-VAL-N-10": "“No Kenyan connection” is conclusory and does not separately negate establishment or ordinary residence under section 4(b).",
}

DATA_QUALITY = {
    "EU-TRN-I-04": "The missing_facts field is malformed as one array element per character instead of one complete missing-fact string.",
    "KE-TRN-A-08": "The scenario contains replacement characters in “résumés”; correct the source encoding before review or export.",
    "KE-VAL-N-10": "The scenario contains a replacement character in “São Paulo”; correct the source encoding before review or export.",
    "EU-TRN-N-08": "The scenario contains a replacement character in “Bogotá”; correct the source encoding before review or export.",
}

LEGAL_AMBIGUITY = {
    "NG-VAL-I-09": "Pseudonymised information remains personal data when re-identification is possible; the scenario omits whether the consortium retains or can access identifying information.",
    "KE-TRN-I-02": "Temporary voice-assistant handling may itself involve automated recording or processing; clarify what is captured in memory and whether it is entered in a record.",
    "KE-TRN-I-07": "The described act is human recollection. Unless a structured record is actually consulted or updated, the facts may support DOES_NOT_APPLY rather than uncertainty.",
    "KE-VAL-I-09": "Automated facial detection may process a digital image even if it is immediately discarded; clarify whether the transient image or logs constitute a record under section 4(a).",
    "EU-VAL-A-10": "The scenario stipulates the Article 3(3) legal conclusion (“Spanish law applies”) rather than facts establishing why public international law produces that result.",
}

NG_NEGATIVE = {f"NG-TRN-N-{index:02d}" for index in range(1, 9)} | {"NG-VAL-N-09", "NG-VAL-N-10"}
KE_FOREIGN_NEGATIVE = {"KE-TRN-N-03", "KE-TRN-N-04", "KE-TRN-N-06", "KE-TRN-N-07", "KE-VAL-N-09", "KE-VAL-N-10"}
EU_NEGATIVE = {f"EU-TRN-N-{index:02d}" for index in range(1, 9)} | {"EU-VAL-N-09", "EU-VAL-N-10"}
NG_UNCERTAIN = {f"NG-TRN-I-{index:02d}" for index in range(1, 9)} | {"NG-VAL-I-09", "NG-VAL-I-10"}
KE_UNCERTAIN = {f"KE-TRN-I-{index:02d}" for index in range(1, 9)} | {"KE-VAL-I-09", "KE-VAL-I-10"}
EU_TARGETING_UNCERTAIN = {"EU-TRN-I-02", "EU-TRN-I-03", "EU-TRN-I-05", "EU-TRN-I-07", "EU-TRN-I-08", "EU-VAL-I-10"}


def load_records() -> list[dict[str, object]]:
    return [json.loads(line) for line in DATASET.read_text(encoding="utf-8").splitlines() if line.strip()]


def issues_for(candidate_id: str) -> list[tuple[str, str]]:
    issues: list[tuple[str, str]] = []
    if candidate_id in DATA_QUALITY:
        issues.append(("DATA_QUALITY", DATA_QUALITY[candidate_id]))
    if candidate_id in NEGATIVE_ROUTE_OMISSIONS:
        issues.append(("TERRITORIAL_ROUTE", NEGATIVE_ROUTE_OMISSIONS[candidate_id]))
    if candidate_id in LEGAL_AMBIGUITY:
        issues.append(("LEGAL_AMBIGUITY", LEGAL_AMBIGUITY[candidate_id]))
    if candidate_id in NG_NEGATIVE:
        issues.append(("CONCEPTUAL_OVERLAP", "Foreign-only negative pattern is conceptually close to NG-EVAL-003 and repeats a ten-record statutory-negation template."))
    if candidate_id in KE_FOREIGN_NEGATIVE:
        issues.append(("CONCEPTUAL_OVERLAP", "Foreign-only negative pattern is conceptually close to KE-EVAL-003; factual nouns change while the scope logic remains nearly identical."))
    if candidate_id in EU_NEGATIVE:
        issues.append(("CONCEPTUAL_OVERLAP", "Complete Article 3 negation is conceptually close to EU-EVAL-004 and repeatedly uses statutory/legal shorthand that may cue the label."))
    if candidate_id in NG_UNCERTAIN:
        issues.append(("CONCEPTUAL_OVERLAP", "Missing actor, processing, or data-subject location follows the same uncertainty structure as NG-EVAL-004; confirm this is not a superficial transformation."))
    if candidate_id in KE_UNCERTAIN:
        issues.append(("CONCEPTUAL_OVERLAP", "Missing record/filing-system and territorial facts follow the same uncertainty structure as KE-EVAL-004; confirm independent factual design."))
    if candidate_id in EU_TARGETING_UNCERTAIN:
        issues.append(("CONCEPTUAL_OVERLAP", "Unknown Union location, offering, or monitoring is conceptually close to EU-EVAL-005; confirm the factual pattern is sufficiently independent."))
    return issues


def render() -> str:
    records = load_records()
    by_id = {str(record["candidate_id"]): record for record in records}
    flagged = {candidate_id: issues_for(candidate_id) for candidate_id in by_id if issues_for(candidate_id)}
    categories = Counter(category for issues in flagged.values() for category, _ in issues)
    lines = [
        "# GeoLegal-AI Training Data Legal Review Draft",
        "",
        "> **Review status:** Draft only. All 90 records remain `PENDING_REVIEW` and `SYNTHETIC_UNVERIFIED`. This document does not approve any label, explanation, authority, or dataset record.",
        "",
        "## Flagged-scenario summary",
        "",
        f"- Candidate records reviewed: **{len(records)}**.",
        f"- Records with at least one specific flag: **{len(flagged)}**.",
        f"- Records without a specific drafting flag: **{len(records) - len(flagged)}**; these still require full human legal review.",
        f"- Flag instances: " + ", ".join(f"`{key}` {value}" for key, value in sorted(categories.items())) + ".",
        "- Automated leakage report result: no threshold-level ID, family, normalized-exact, token-trigram, or character-five-gram matches. That result does not clear conceptual overlap.",
        "- No dataset record, review status, held-out file, or prompt/completion export was changed or created by this review.",
        "",
        "### Critical data-quality flags",
        "",
    ]
    for candidate_id in sorted(DATA_QUALITY):
        lines.append(f"- `{candidate_id}` — {DATA_QUALITY[candidate_id]}")
    lines.extend(["", "### Negative applicability routes needing clarification", ""])
    for candidate_id in sorted(NEGATIVE_ROUTE_OMISSIONS):
        lines.append(f"- `{candidate_id}` — {NEGATIVE_ROUTE_OMISSIONS[candidate_id]}")
    lines.extend(["", "### Legally questionable or potentially conclusive assumptions", ""])
    for candidate_id in sorted(LEGAL_AMBIGUITY):
        lines.append(f"- `{candidate_id}` — {LEGAL_AMBIGUITY[candidate_id]}")
    lines.extend([
        "",
        "### Repetition and held-out conceptual overlap",
        "",
        "- All ten Nigeria negative records use the same foreign-only/no-Nigeria structure as `NG-EVAL-003`.",
        "- Six Kenya foreign-only negative records repeat the structure of `KE-EVAL-003`; four other Kenya negatives repeatedly test unrecorded human memory or loose notes.",
        "- All ten EU negative records repeat the full Article 3 negation structure of `EU-EVAL-004` and often state legal conclusions rather than neutral facts.",
        "- All ten Nigeria uncertainty records repeat the missing-geography structure of `NG-EVAL-004`.",
        "- All ten Kenya uncertainty records combine unknown record/filing-system facts with unknown geography, closely tracking `KE-EVAL-004`.",
        "- Six EU uncertainty records repeat the unknown location/offering/monitoring structure of `EU-EVAL-005`.",
        "- The question text is identical within each jurisdiction across all labels, and many explanations reuse a single statutory formula. Reviewers should assess whether this creates label cues or an artificially narrow training distribution.",
        "",
        "## Scenario-by-scenario review",
        "",
    ])
    for jurisdiction in JURISDICTIONS:
        lines.extend([f"## {jurisdiction.title() if jurisdiction != 'EU' else 'European Union'}", ""])
        for label in LABELS:
            lines.extend([f"### {label}", ""])
            selected = [record for record in records if record["jurisdiction"] == jurisdiction and record["expected_label"] == label]
            for record in selected:
                candidate_id = str(record["candidate_id"])
                issues = issues_for(candidate_id)
                flag = "PENDING_REVIEW — no specific drafting defect identified; substantive legal review still required."
                if issues:
                    flag = "PENDING_REVIEW — FLAGGED: " + " ".join(f"[{category}] {message}" for category, message in issues)
                basis = "; ".join(str(item) for item in record["statutory_basis"])
                lines.extend([
                    f"#### {candidate_id} — {record['split']}",
                    "",
                    f"- **Factual scenario:** {record['scenario']}",
                    f"- **Question:** {record['question']}",
                    f"- **Proposed label:** `{record['expected_label']}`",
                    f"- **Statutory provision:** {basis}",
                    f"- **Source URL:** {record['source_url']}",
                    f"- **Proposed statutory reasoning:** {record['statutory_explanation']}",
                    f"- **Review flag:** {flag}",
                    "",
                ])
    return "\n".join(lines)


if __name__ == "__main__":
    OUTPUT.write_text(render(), encoding="utf-8", newline="\n")
