# Results status

`geolegal_baseline_test.json` is the first actual Tiny Aya inference produced in Google Colab. It is preserved unchanged as an **exploratory smoke test**, not a held-out evaluation prediction and not a validated benchmark result.

Its outer artifact is valid JSON. Its `response` uses the legacy `DECISION:/EXPLANATION:` text format rather than the current structured JSON contract. The deterministic extractor recognizes the closed label for pipeline compatibility, but the artifact is permanently excluded from scored metrics because it has no reviewed scenario ID or legally reviewed answer key.

`baseline_predictions.jsonl` is an empty legacy output path. `baseline_metrics.json` is the earlier zero-scored placeholder created while evaluation answer keys were pending review; neither file is evidence for the current baseline claim.

The project owner reports a later Colab E1 result of 46.67% accuracy, 24.56% macro F1, and 66.67% parse rate on the frozen 15-record evaluation set. The corresponding versioned row-level predictions and metrics JSON are not present in this checkout. Until those exact artifacts are recovered, the figures must be labelled user-reported and provisional, not independently reproduced.

Do not reconstruct or invent missing row-level predictions from aggregate numbers. A comparable rerun must use `held_out_approved_v1`, the pinned model revision, the registered prompt and decoding settings, and new versioned output filenames.
