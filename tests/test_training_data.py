from __future__ import annotations

import hashlib
import json
import tempfile
import unittest
from collections import Counter
from dataclasses import replace
from pathlib import Path

from geolegal.training_data import (
    Candidate,
    export_prompt_completion,
    leakage_report,
    protected_registry,
    read_jsonl,
    validate_candidates,
)


class TrainingDataPreparationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.raw = read_jsonl("data/train/candidates_v1.jsonl")
        cls.candidates = [Candidate.from_dict(value) for value in cls.raw]
        cls.registry = json.loads(Path("data/eval/protected_held_out_registry_v1.json").read_text(encoding="utf-8"))
        cls.report = json.loads(Path("data/train/leakage_report_v1.json").read_text(encoding="utf-8"))
        cls.manifest = json.loads(Path("data/train/candidate_manifest_v1.json").read_text(encoding="utf-8"))

    def test_registry_covers_all_three_held_out_revisions_with_live_hashes(self) -> None:
        datasets = self.registry["protected_datasets"]
        self.assertEqual({item["path"] for item in datasets}, {
            "data/eval/held_out_initial.jsonl",
            "data/eval/held_out_proposed_v2.jsonl",
            "data/eval/held_out_approved_v1.jsonl",
        })
        self.assertEqual(self.registry["signature_count"], 45)
        self.assertEqual(self.registry["unique_scenario_ids"], 15)
        for item in datasets:
            self.assertEqual(hashlib.sha256(Path(item["path"]).read_bytes()).hexdigest(), item["sha256"])

    def test_candidate_counts_and_balanced_distributions(self) -> None:
        self.assertEqual(len(self.candidates), 90)
        self.assertEqual(Counter(item.split for item in self.candidates), {"TRAIN": 72, "VALIDATION": 18})
        self.assertEqual(Counter(item.jurisdiction for item in self.candidates), {"NIGERIA": 30, "KENYA": 30, "EU": 30})
        self.assertEqual(Counter(item.expected_label for item in self.candidates), {
            "APPLIES": 30, "DOES_NOT_APPLY": 30, "INSUFFICIENT_INFORMATION": 30,
        })
        for jurisdiction in ("NIGERIA", "KENYA", "EU"):
            for label in ("APPLIES", "DOES_NOT_APPLY", "INSUFFICIENT_INFORMATION"):
                self.assertEqual(sum(
                    item.jurisdiction == jurisdiction and item.expected_label == label and item.split == "TRAIN"
                    for item in self.candidates
                ), 8)
                self.assertEqual(sum(
                    item.jurisdiction == jurisdiction and item.expected_label == label and item.split == "VALIDATION"
                    for item in self.candidates
                ), 2)

    def test_all_candidates_remain_unapproved_and_source_grounded(self) -> None:
        self.assertTrue(all(item.review_status == "PENDING_REVIEW" for item in self.candidates))
        self.assertTrue(all(item.origin == "SYNTHETIC_UNVERIFIED" for item in self.candidates))
        self.assertTrue(all(item.statutory_basis for item in self.candidates))
        self.assertTrue(all(item.source_url.startswith("https://") for item in self.candidates))
        self.assertTrue(all(item.statutory_explanation for item in self.candidates))

    def test_scenario_families_do_not_cross_splits(self) -> None:
        validate_candidates(self.candidates)
        train = {item.scenario_family_id for item in self.candidates if item.split == "TRAIN"}
        validation = {item.scenario_family_id for item in self.candidates if item.split == "VALIDATION"}
        self.assertFalse(train & validation)

    def test_checked_candidate_set_has_no_automated_overlap(self) -> None:
        self.assertEqual(self.report["id_overlaps"], [])
        self.assertEqual(self.report["family_overlaps"], [])
        self.assertEqual(self.report["normalized_exact_matches"], [])
        self.assertEqual(self.report["flagged_near_matches"], [])
        self.assertEqual(self.report["blocking_issue_count"], 0)
        self.assertFalse(self.report["export_allowed"])

    def test_exact_id_family_and_text_collisions_are_detected(self) -> None:
        held_out = read_jsonl("data/eval/held_out_approved_v1.jsonl")[0]
        base = self.candidates[0]
        collision = replace(
            base,
            candidate_id=held_out["scenario_id"],
            scenario_family_id=f"protected::{held_out['scenario_id']}",
            scenario=held_out["scenario"],
            question=held_out["question"],
        )
        result = leakage_report([collision], self.registry)
        self.assertTrue(result["id_overlaps"])
        self.assertTrue(result["family_overlaps"])
        self.assertTrue(result["normalized_exact_matches"])

    def test_near_match_is_flagged_for_manual_review(self) -> None:
        held_out = read_jsonl("data/eval/held_out_approved_v1.jsonl")[0]
        base = self.candidates[0]
        near = replace(
            base,
            candidate_id="TEST-NEAR-001",
            scenario_family_id="family::test-near-001",
            scenario=held_out["scenario"] + " The retail opening hours are different.",
            question=held_out["question"],
        )
        result = leakage_report([near], self.registry)
        self.assertTrue(result["flagged_near_matches"])
        self.assertTrue(all(item["manual_review_status"] == "PENDING" for item in result["flagged_near_matches"]))

    def test_manifest_matches_candidate_file(self) -> None:
        checksum = hashlib.sha256(Path("data/train/candidates_v1.jsonl").read_bytes()).hexdigest()
        self.assertEqual(self.manifest["candidate_file_sha256"], checksum)
        self.assertEqual(self.manifest["record_count"], 90)
        self.assertEqual(self.manifest["export_status"], "BLOCKED_PENDING_LEGAL_REVIEW")

    def test_prompt_completion_export_is_blocked_without_approval(self) -> None:
        with tempfile.TemporaryDirectory(dir="artifacts") as directory:
            train = Path(directory) / "train.jsonl"
            validation = Path(directory) / "validation.jsonl"
            with self.assertRaisesRegex(RuntimeError, "pending_legal_review=90"):
                export_prompt_completion(self.candidates, self.report, train, validation)
            self.assertFalse(train.exists())
            self.assertFalse(validation.exists())


if __name__ == "__main__":
    unittest.main()
